#!/usr/bin/env python3
"""Deploy the portfolio site to PythonAnywhere via its API.

PythonAnywhere has no webhook, so this drives a deploy with only an API token
(no SSH keys to manage — important for the markdown-only target audience).
Flow:

  1. POST /consoles/            -> create a fresh bash console, get its id.
  2. POST /consoles/{id}/send_input/  -> run the deploy command heredoc.
  3. GET  /consoles/{id}/get_latest_output/  -> poll until the prompt returns.
  4. POST /webapps/{domain}/reload/   -> reload the WSGI app.

Usage:
  python scripts/pa_deploy.py                       # real deploy
  python scripts/pa_deploy.py --dry-run             # print planned calls, hit nothing

Required env (or CLI flags):
  PA_USERNAME   PythonAnywhere username
  PA_API_TOKEN  API token from the Account page
  PA_DOMAIN     e.g. yourname.pythonanywhere.com
  PA_REPO_PATH  absolute path to the repo on the PA filesystem
                (defaults to /home/<username>/<repo-name>)

The token is never logged. Intended to run from the GitHub Action workflow;
secrets come from the runner env.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import urllib.error
import urllib.request

API_BASE = "https://www.pythonanywhere.com/api"


def _req(method: str, path: str, token: str, body: dict | None = None) -> tuple[int, dict, str]:
    url = f"{API_BASE}{path}"
    data = None
    headers = {"Authorization": f"Token {token}"}
    if body is not None:
        import json

        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode(errors="replace")
            parsed = {}
            if raw:
                try:
                    import json

                    parsed = json.loads(raw)
                except ValueError:
                    pass
            return resp.status, parsed, raw
    except urllib.error.HTTPError as exc:
        return exc.code, {}, exc.read().decode(errors="replace")


def deploy_command(repo_path: str) -> str:
    """The shell heredoc sent into the PA console."""
    return (
        f"cd {repo_path} && "
        "git pull && "
        "pip install -r requirements.txt && "
        "python manage.py migrate --no-input && "
        "python manage.py collectstatic --noinput && "
        "echo PA_DEPLOY_DONE_$?\n"
    )


def run(username: str, token: str, domain: str, repo_path: str, *, dry_run: bool) -> int:
    # NOTE: never log the token.
    print(f"[pa_deploy] user={username} domain={domain} repo={repo_path} dry_run={dry_run}")

    cmd = deploy_command(repo_path)
    steps = [
        ("POST", f"/api/v0/user/{username}/consoles/", {"executable": "/bin/bash"}),
        ("send_input", f"/api/v0/user/{username}/consoles/<ID>/send_input/", {"input": cmd}),
        ("GET", f"/api/v0/user/{username}/consoles/<ID>/get_latest_output/", None),
        ("POST", f"/api/v0/user/{username}/webapps/{domain}/reload/", None),
    ]

    if dry_run:
        print("[pa_deploy] DRY RUN — no API calls will be made. Planned steps:")
        for method, path, body in steps:
            print(f"  {method:10s} {path}")
        print(f"[pa_deploy] command that would be sent:\n    {cmd!r}")
        return 0

    # 1. Create console.
    code, data, raw = _req("POST", f"/api/v0/user/{username}/consoles/", token, {"executable": "/bin/bash"})
    if code not in (200, 201):
        print(f"[pa_deploy] console create failed: {code} {raw[:200]}", file=sys.stderr)
        return 1
    console_id = data.get("id")
    if not console_id:
        print(f"[pa_deploy] no console id in response: {raw[:200]}", file=sys.stderr)
        return 1
    print(f"[pa_deploy] created console id={console_id}")

    # 2. Send the deploy command.
    code, _, raw = _req(
        "POST", f"/api/v0/user/{username}/consoles/{console_id}/send_input/", token, {"input": cmd}
    )
    if code not in (200, 201):
        print(f"[pa_deploy] send_input failed: {code} {raw[:200]}", file=sys.stderr)
        return 1

    # 3. Poll output until the done marker appears (bounded).
    deadline = time.time() + 180
    success = False
    last = ""
    while time.time() < deadline:
        time.sleep(3)
        code, _, raw = _req(
            "GET", f"/api/v0/user/{username}/consoles/{console_id}/get_latest_output/", token, None
        )
        if code != 200:
            continue
        last = raw
        if "PA_DEPLOY_DONE_" in raw:
            # Non-zero exit code is surfaced as PA_DEPLOY_DONE_<code>.
            tail = raw[raw.rfind("PA_DEPLOY_DONE_"):]
            success = tail.strip().endswith("PA_DEPLOY_DONE_0")
            break
    if not success:
        print(f"[pa_deploy] deploy command did not complete cleanly. Output tail:\n{last[-800:]}", file=sys.stderr)
        # Still attempt reload below? No -- a failed migrate/collectstatic should
        # surface and stop. Return non-zero.
        return 2

    # 4. Reload the webapp.
    code, _, raw = _req("POST", f"/api/v0/user/{username}/webapps/{domain}/reload/", token, None)
    if code not in (200, 201):
        print(f"[pa_deploy] reload failed: {code} {raw[:200]}", file=sys.stderr)
        return 1
    print("[pa_deploy] reloaded webapp. Deploy complete.")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="print planned API calls and exit")
    p.add_argument("--username", default=os.environ.get("PA_USERNAME"))
    p.add_argument("--token", default=os.environ.get("PA_API_TOKEN"))
    p.add_argument("--domain", default=os.environ.get("PA_DOMAIN"))
    p.add_argument(
        "--repo-path",
        default=os.environ.get("PA_REPO_PATH", ""),
        help="absolute path to the repo on the PA host",
    )
    args = p.parse_args(argv)

    if args.dry_run:
        # In dry-run, tolerate missing token so it can be tested without one.
        return run(args.username or "<user>", "dry-run-token", args.domain or "<domain>.pythonanywhere.com",
                   args.repo_path or "/home/<user>/portfolio", dry_run=True)

    missing = [n for n, v in (("PA_USERNAME", args.username), ("PA_API_TOKEN", args.token),
                              ("PA_DOMAIN", args.domain), ("PA_REPO_PATH", args.repo_path)) if not v]
    if missing:
        print(f"[pa_deploy] missing required inputs: {', '.join(missing)}", file=sys.stderr)
        return 2
    return run(args.username, args.token, args.domain, args.repo_path, dry_run=False)


if __name__ == "__main__":
    raise SystemExit(main())
