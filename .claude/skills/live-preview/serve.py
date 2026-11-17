#!/usr/bin/env python3
"""Live preview server for Huddle. Standard library only.

Serves the repo over http://localhost:<port>/ and injects a small script into
every HTML page that reloads the tab whenever a file in the repo changes, then
shows a toast naming the file that changed.

Usage:
  python3 .claude/skills/live-preview/serve.py [--port 4173] [--open PATH] [--no-open]

If a preview server is already running on the port, this just opens the page
in the browser and exits, so it is always safe to run again.
"""
import argparse
import json
import os
import sys
import urllib.request
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WATCH_EXT = {".html", ".css", ".js", ".json", ".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp"}
SKIP_DIRS = {".git", ".claude", "node_modules", "__pycache__"}
STAMP_PATH = "/__live/stamp"

CLIENT = """
<script>
(function () {
  var KEY = '__live_preview';
  var last = null;
  function toast(text) {
    var el = document.createElement('div');
    el.textContent = text;
    el.style.cssText = 'position:fixed;left:50%;bottom:20px;transform:translateX(-50%);z-index:2147483647;' +
      'background:#1B1A2E;color:#fff;font:600 13px/1.3 system-ui,sans-serif;padding:9px 14px;border-radius:999px;' +
      'box-shadow:0 6px 24px rgba(0,0,0,.35);border:1px solid #3DDC97;pointer-events:none;transition:opacity .4s';
    document.body.appendChild(el);
    setTimeout(function () { el.style.opacity = '0'; }, 2600);
    setTimeout(function () { el.remove(); }, 3100);
  }
  try {
    var saved = JSON.parse(sessionStorage.getItem(KEY) || 'null');
    sessionStorage.removeItem(KEY);
    if (saved) {
      window.addEventListener('load', function () {
        window.scrollTo(saved.x, saved.y);
        toast('Claude edited ' + saved.file);
      });
    }
  } catch (e) {}
  function poll() {
    fetch('__STAMP__', { cache: 'no-store' }).then(function (r) { return r.json(); }).then(function (s) {
      if (last !== null && s.stamp !== last) {
        try {
          sessionStorage.setItem(KEY, JSON.stringify({ x: scrollX, y: scrollY, file: s.file }));
        } catch (e) {}
        location.reload();
        return;
      }
      last = s.stamp;
      setTimeout(poll, 400);
    }).catch(function () { setTimeout(poll, 1500); });
  }
  poll();
})();
</script>
""".replace("__STAMP__", STAMP_PATH)

SLIDE_WRAP = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400..700&display=swap">
<link rel="stylesheet" href="/deck/project/deck.css">
<style>html,body{{margin:0}}</style>
</head><body>
{body}
</body></html>"""


def newest():
    """Return (mtime_ns, relative path) of the most recently changed watched file."""
    best, best_file = 0, ""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if Path(name).suffix.lower() not in WATCH_EXT:
                continue
            full = os.path.join(dirpath, name)
            try:
                m = os.stat(full).st_mtime_ns
            except OSError:
                continue
            if m > best:
                best, best_file = m, os.path.relpath(full, ROOT)
    return best, best_file


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        pass

    def send_bytes(self, body, ctype):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        if path == STAMP_PATH:
            stamp, changed = newest()
            body = json.dumps({"stamp": str(stamp), "file": changed, "app": "huddle-live-preview"})
            return self.send_bytes(body.encode(), "application/json")

        local = Path(self.translate_path(path))
        if local.is_dir():
            local = local / "index.html"
        if local.suffix.lower() == ".html" and local.is_file():
            html = local.read_text(encoding="utf-8")
            if "<html" not in html.lower():
                # Deck slides are bare <section> fragments: give them a page and the deck styles.
                html = SLIDE_WRAP.format(title=local.stem, body=html)
            lower = html.lower()
            at = lower.rfind("</body>")
            html = html[:at] + CLIENT + html[at:] if at != -1 else html + CLIENT
            return self.send_bytes(html.encode("utf-8"), "text/html; charset=utf-8")
        return super().do_GET()

    def end_headers(self):
        if not any(h.lower().startswith(b"cache-control") for h in self._headers_buffer):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()


def already_running(port):
    try:
        with urllib.request.urlopen("http://127.0.0.1:%d%s" % (port, STAMP_PATH), timeout=1) as r:
            return json.load(r).get("app") == "huddle-live-preview"
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=4173)
    ap.add_argument("--open", default="prototype/index.html", help="repo-relative page to open")
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()

    url = "http://localhost:%d/%s" % (args.port, args.open.lstrip("/"))
    if already_running(args.port):
        if not args.no_open:
            webbrowser.open(url)
        print("Live preview already running: " + url)
        return 0

    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    except OSError as e:
        print("Port %d is in use by something else (%s). Try --port %d." % (args.port, e, args.port + 1))
        return 1
    print("Live preview: " + url, flush=True)
    if not args.no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
