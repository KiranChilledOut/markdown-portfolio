# Markdown basics (write nice pages without coding)

**Markdown** is a simple way to write text that turns into styled web pages.
You type a few easy symbols and the website turns them into headings, **bold**,
lists, links, and pictures. This guide shows everything you'll actually need.
5 minutes, promise.

> In your portfolio, you write Markdown in the `.md` files inside `content/`.

---

## Paragraphs

Just write. Press Enter twice to start a new paragraph.

```markdown
This is one paragraph.

This is a new paragraph because there's a blank line above it.
```

---

## Headings

Put `#` (a hash) and a space before text. More hashes = smaller heading.

```markdown
# Big heading

## Medium heading

### Smaller heading
```

Use one `#` only once per page, at the top.

---

## Bold and italic

```markdown
This is **bold** text.
This is *italic* text.
This is ***bold and italic***.
```

---

## Lists

**Bullet lists** — start each line with `-` and a space:

```markdown
- Apples
- Bananas
- Oranges
```

**Numbered lists** — start each line with a number and a dot:

```markdown
1. First step
2. Second step
3. Third step
```

You can nest lists with spaces:

```markdown
- Fruit
  - Apples
  - Bananas
- Drinks
  - Water
```

---

## Links

Put the text in `[brackets]` and the address in `(parentheses)` right after.

```markdown
Here is [my GitHub](https://github.com/your-handle).
```

---

## Images

Like a link, but starts with `!`. Put the image file in the same folder, or use
a web address.

```markdown
![Description of the image](my-photo.jpg)
```

> Tip: keep images small (under ~500 KB) so pages load fast.

---

## Code blocks

If you want to show a snippet of code (or any fixed-width text), put three
backticks on the line above and below:

````markdown
```python
print("Hello, world!")
```
````

The word `python` is optional — it just adds color highlighting. Use `bash`,
`javascript`, `html`, or leave it out.

For a short bit of code "inline" in a sentence, use single backticks:

```markdown
Run the `collectstatic` command.
```

---

## Block quotes

Use `>` to make a quoted/note box:

```markdown
> This is a helpful tip that stands out.
```

---

## Horizontal line

Three dashes on their own line draw a divider:

```markdown
---
```

---

## Tables (optional)

Use `|` to separate columns. The second row sets the alignment.

```markdown
| Project      | Year | Link                |
|--------------|------|---------------------|
| My site      | 2026 | [link](https://...) |
| Other        | 2025 | [link](https://...) |
```

---

## The "settings" at the top of each page

Every content file starts with a block between two `---` lines. This isn't
normal Markdown — it's the page's **settings** (called "front matter"). Example:

```markdown
---
title: "My First Website"
summary: "A short one-line description shown on cards and lists."
tech: [HTML, CSS]
date: 2026-06-01
draft: false
---

# My First Website

Your content starts here, after the second --- line.
```

- `title` — the page title (shown big at the top).
- `summary` — a one-line description, shown on listing pages.
- `tech` — optional, a list of tools used (for projects).
- `tags` — optional, a list of tags (for blog/tutorials).
- `date` — `YYYY-MM-DD` format. Newest shows first.
- `draft` — `true` to hide the page, `false` to publish it.

Only `title` is required. Skip what you don't need.

---

## That's it

You now know enough Markdown to write your whole portfolio. When in doubt, copy
an example file from `content.example/` and change the words. ✦
