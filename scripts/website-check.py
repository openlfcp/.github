#!/usr/bin/env python3
"""Checks the static website (openlfcp.org) for rc-verify's optional gate.

    scripts/website-check.py <website checkout>

Every local link and asset its committed HTML and CSS files reference exists:
href and src attributes, srcset entries and CSS url(...). Root-relative paths
resolve from the site root, others from the referencing file; a directory
means its index.html. External URLs, fragments, mailto:, tel: and data: are
not checked. Prints one line per problem and exits 1 when there is any.
"""

from __future__ import annotations

import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKIP = ("http:", "https:", "mailto:", "tel:", "data:", "javascript:", "//")
CSS_URL = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")


class Refs(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value is None:
                continue
            if name in ("href", "src"):
                self.refs.append(value)
            elif name == "srcset":
                self.refs += [part.strip().split(" ")[0] for part in value.split(",") if part.strip()]
            elif name == "style":
                self.refs += CSS_URL.findall(value)


def committed(root: Path) -> list[Path]:
    out = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True, check=True)
    return [root / f for f in out.stdout.splitlines()]


def target(root: Path, source: Path, ref: str) -> Path | None:
    if ref.startswith(SKIP) or ref.startswith("#") or ref == "":
        return None
    path = unquote(urlsplit(ref).path)
    if path == "":
        return None
    base = root if path.startswith("/") else source.parent
    t = (base / path.lstrip("/")).resolve()
    return t / "index.html" if t.is_dir() else t


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[2].strip())
        return 2
    root = Path(sys.argv[1]).resolve()
    files = committed(root)
    tracked = {f.resolve() for f in files}
    problems = []
    for f in files:
        if f.suffix == ".html":
            parser = Refs()
            parser.feed(f.read_text(encoding="utf-8"))
            refs = parser.refs
        elif f.suffix == ".css":
            refs = CSS_URL.findall(f.read_text(encoding="utf-8"))
        else:
            continue
        for ref in refs:
            t = target(root, f, ref)
            if t is not None and t not in tracked:
                problems.append(f"{f.relative_to(root)}: {ref} does not resolve to a committed file")
    for p in problems:
        print(p)
    print(f"website-check: {len(files)} files, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
