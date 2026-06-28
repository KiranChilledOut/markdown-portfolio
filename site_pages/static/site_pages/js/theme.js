// Dark/light theme toggle. Persists choice in localStorage; falls back to the
// OS preference. Runs before paint via the inline bootstrap in base.html? No —
// to avoid a flash we apply the stored theme ASAP on DOMContentLoaded. For a
// truly flash-free load, set <html data-theme> server-side or via an inline
// <head> script; here we keep it simple and accept a brief paint.
(function () {
  "use strict";

  var root = document.documentElement;
  var store = "krr-theme";

  function systemDark() {
    return window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function stored() {
    try { return localStorage.getItem(store); } catch (e) { return null; }
  }

  function apply(theme) {
    var resolved = theme === "dark" || theme === "light"
      ? theme
      : (systemDark() ? "dark" : "light");
    root.setAttribute("data-theme", resolved);
  }

  // Initial apply.
  apply(stored());

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.querySelector(".theme-toggle");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var current = root.getAttribute("data-theme") === "dark" ? "dark" : "light";
      var next = current === "dark" ? "light" : "dark";
      apply(next);
      try { localStorage.setItem(store, next); } catch (e) {}
    });

    // React to OS changes when the user hasn't picked explicitly.
    if (window.matchMedia) {
      window.matchMedia("(prefers-color-scheme: dark)")
        .addEventListener("change", function () {
          if (!stored()) apply("auto");
        });
    }
  });
})();
