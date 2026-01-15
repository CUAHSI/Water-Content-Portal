#!/usr/bin/env python3
"""
Dev server for the built site with clean-URL fallback.

Behavior:
- Serves from book/_build/html
- If the requested path is missing, tries "<path>.html"
- If still missing, falls back to "index.html" (SPA-style)

Usage:
    PORT=3001 python3 scripts/serve_with_fallback.py
"""

from __future__ import annotations

import http.server
import os
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent.parent / "book" / "_build" / "html"


class FallbackHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        path = unquote(path.split("?", 1)[0].split("#", 1)[0])
        return str(ROOT / path.lstrip("/"))

    def send_head(self):
        path = Path(self.translate_path(self.path))

        # Existing file/dir
        if path.is_dir():
            index = path / "index.html"
            if index.exists():
                path = index
            else:
                return super().send_head()
        elif not path.exists():
            html_path = Path(f"{path}.html")
            if html_path.exists():
                path = html_path
            else:
                path = ROOT / "index.html"

        ctype = self.guess_type(str(path))
        try:
            f = open(path, "rb")
        except OSError:
            return self.send_error(404, "File not found")

        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def log_message(self, format, *args):
        pass  # quiet


def run(port: int = 3001):
    os.chdir(ROOT)
    http.server.test(HandlerClass=FallbackHandler, port=port)


if __name__ == "__main__":
    port_env = os.environ.get("PORT")
    try:
        port = int(port_env) if port_env else 3001
    except ValueError:
        port = 3001
    run(port)
