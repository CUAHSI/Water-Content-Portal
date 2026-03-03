#!/usr/bin/env python3
"""
Insert the Heap base snippet into every built HTML page.
Run this after the static site build so Heap is present on all pages.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


HEAP_APP_ID = os.environ.get("HEAP_APP_ID") or "902525459" # TODO: remove after testing
OUTPUT_ROOTS = [Path("book/_build/html"), Path("book/_build/site/public")]

SNIPPET = """
<script>
  window.heap = window.heap || [];
  heap.load = function (appid, config) {
    window.heap.appid = appid;
    window.heap.config = config = config || {};
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.async = true;
    script.src = "https://cdn.heapanalytics.com/js/heap-" + appid + ".js";
    var firstScript = document.getElementsByTagName("script")[0];
    firstScript.parentNode.insertBefore(script, firstScript);
    var methods = [
      "addEventProperties",
      "addUserProperties",
      "clearEventProperties",
      "identify",
      "resetIdentity",
      "removeEventProperty",
      "setEventProperties",
      "track",
      "unsetEventProperty"
    ];
    function factory(method) {
      return function () {
        heap.push([method].concat(Array.prototype.slice.call(arguments, 0)));
      };
    }
    for (var i = 0; i < methods.length; i++) {
      heap[methods[i]] = factory(methods[i]);
    }
  };
  heap.load("%s");
</script>"""


def inject(html_path: Path, snippet: str, marker: str) -> bool:
    text = html_path.read_text(encoding="utf-8")

    # Skip if any Heap snippet/config is already present
    existing_markers = (
        marker,
        "cdn.heapanalytics.com/js/heap-",
        "cdn.us.heap-api.com/config",
        "window.heapReadyCb",
    )
    if any(m in text for m in existing_markers):
        return False

    if "</head>" not in text:
        return False

    updated = text.replace("</head>", f"{snippet}\n</head>", 1)
    html_path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    snippet = SNIPPET % HEAP_APP_ID
    marker = f"heap-{HEAP_APP_ID}.js"
    roots_found = False
    modified = 0

    for root in OUTPUT_ROOTS:
        if not root.exists():
            continue
        roots_found = True
        for html_file in root.rglob("*.html"):
            if inject(html_file, snippet, marker):
                modified += 1

    if not roots_found:
        print("No built HTML directories found.", file=sys.stderr)
        return 1

    print(f"Injected Heap snippet into {modified} file(s) using HEAP_APP_ID={HEAP_APP_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
