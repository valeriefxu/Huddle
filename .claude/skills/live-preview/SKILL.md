---
name: live-preview
description: Open the Huddle app in the browser with live reload so the user watches every edit land as it is made. Use BEFORE the first edit whenever you are about to change the prototype (prototype/index.html), the deck slides or deck.css, or any other visual file in this repo, and when the user asks to see, open, preview or watch the app.
---

# Live preview

The user wants to watch the app change while you edit it. Before your first edit to any visual file, start the preview; then edit normally. Every saved change reloads the open tab within half a second and shows a "Claude edited <file>" toast.

## Start it (once per session, before editing)

Run this from the repo root as a **background** command (`run_in_background: true`), since the server keeps running:

```bash
python3 .claude/skills/live-preview/serve.py --open prototype/index.html
```

- It opens `http://localhost:4173/prototype/index.html` in the user's default browser.
- It is safe to run again: if the server is already up it only opens the page and exits.
- If port 4173 is taken by something else, pass `--port 4174`.
- Python standard library only; nothing to install.

Tell the user in one line that the preview is open and will update as you edit.

## Pick the page that matches what you are editing

| Editing | `--open` value |
| --- | --- |
| The app prototype | `prototype/index.html` (default) |
| A deck slide | `deck/project/slides/<name>.html` (for example `deck/project/slides/cover.html`) |
| `deck/project/deck.css` | the slide you are styling |

Slides are bare `<section>` fragments; the server wraps them in a page with `deck.css` so they render on their own. This is a single-slide preview, not the full deck player.

If you move to a different page mid-session, run the command again with the new `--open` value; it reuses the running server.

## While editing

- Make changes in small, visible steps (one Edit per meaningful change) rather than one giant rewrite, so the user can follow along.
- A reload resets the prototype's in-page state (selected tab, demo scenario). Scroll position is kept. If the change is on a screen that is not the default one, tell the user where to click to see it.
- Do not edit the injected reload script into the project files; it is added by the server at serve time only.

## Stop it

The server stops when the session's background command is stopped. To stop it by hand: `lsof -ti :4173 | xargs kill`.
