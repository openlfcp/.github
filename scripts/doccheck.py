#!/usr/bin/env python3
"""Documentation consistency gate for the OpenLFCP checkouts.

  scripts/doccheck.py [--root DIR] [REPO ...]

Checks the committed Markdown (git ls-files) of each repository:

- every relative link resolves to a committed file or directory, and a
  link into a sibling checkout (../<repo>/...) to an existing path;
- every #anchor names a heading (GitHub's anchor rules) or an
  <a name>/<a id> of the target Markdown file;
- every docs/**/*.md (and every other file under docs/) is listed in that
  repository's docs/NAVIGATOR.md, which must exist when docs/ does;
- file names under docs/ are lower-case kebab-case (version dots allowed),
  or the established all-upper-case artifact names (BACKLOG-MVP-0.1.md).

Links in code spans and fenced blocks are ignored. Uncommitted files are
not checked. REPO defaults to the seven checkouts next to this repository
(--root: the directory that holds them). Exit status 0 when nothing is
wrong; otherwise every problem is printed, one per line, and the status
is 1.
"""

import argparse
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

REPOS = [".github", "spec", "sdk-rs", "server", "sdk-ts", "examples", "obsidian"]
LINK = re.compile(r'(?<!!)\[(?:[^\]\[]|\[[^\]]*\])*\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)')
KEBAB = re.compile(r"[a-z0-9]+(?:[-.][a-z0-9]+)*")
UPPER = re.compile(r"[A-Z0-9]+(?:[-.][A-Z0-9]+)*")
FENCE = ("```", "~~~")


def slug(text: str) -> str:
    """GitHub's heading anchor."""
    t = re.sub(r"<[^>]+>", "", text).strip().lower().replace("`", "")
    t = "".join(
        c
        for c in t
        if c.isalnum() or c in " -_" or unicodedata.category(c).startswith("L")
    )
    return t.replace(" ", "-")


_anchors: dict[Path, set[str]] = {}


def anchors(path: Path) -> set[str]:
    if path not in _anchors:
        found: set[str] = set()
        seen: dict[str, int] = {}
        fenced = False
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.lstrip().startswith(FENCE):
                fenced = not fenced
                continue
            if fenced:
                continue
            m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
            if m:
                s = slug(m.group(2))
                n = seen.get(s, 0)
                seen[s] = n + 1
                found.add(s if n == 0 else f"{s}-{n}")
            found.update(re.findall(r'<a\s+(?:name|id)="([^"]+)"', line))
        _anchors[path] = found
    return _anchors[path]


def tracked(repo: Path) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(repo), "ls-files"], capture_output=True, text=True, check=True
    )
    return out.stdout.splitlines()


def check(repo: Path, name: str) -> list[str]:
    problems: list[str] = []
    files = tracked(repo)
    present = set(files)
    dirs = {str(Path(f).parent) for f in files}
    while True:
        more = {str(Path(d).parent) for d in dirs} - dirs
        if not more:
            break
        dirs |= more

    for f in (x for x in files if x.endswith(".md")):
        path = repo / f
        fenced = False
        for no, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(), 1
        ):
            if line.lstrip().startswith(FENCE):
                fenced = not fenced
                continue
            if fenced:
                continue
            for target in LINK.findall(re.sub(r"`[^`]*`", "", line)):
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("//"):
                    continue
                part, _, frag = target.partition("#")
                part = unquote(part)
                where = f"{name}/{f}:{no}"
                if part == "":
                    dest = path
                else:
                    rel = os.path.normpath(os.path.join(os.path.dirname(f), part))
                    dest = repo / rel
                    if rel.startswith(".."):
                        if not dest.exists():
                            problems.append(f"{where}: missing {target}")
                        continue
                    if rel not in present and rel.rstrip("/") not in dirs:
                        problems.append(f"{where}: missing {target}")
                        continue
                if (
                    frag
                    and dest.suffix == ".md"
                    and dest.is_file()
                    and unquote(frag).lower() not in anchors(dest)
                ):
                    problems.append(f"{where}: no anchor #{frag} in {os.path.relpath(dest, repo)}")

    docs = [f for f in files if f.startswith("docs/")]
    navigator = repo / "docs/NAVIGATOR.md"
    if docs:
        if not navigator.is_file():
            problems.append(f"{name}: docs/ has {len(docs)} files but no docs/NAVIGATOR.md")
        else:
            text = navigator.read_text(encoding="utf-8")
            for d in docs:
                if d == "docs/NAVIGATOR.md" or Path(d).suffix in (".png", ".svg", ".css", ".js"):
                    continue
                if f"({os.path.relpath(d, 'docs')})" not in text:
                    problems.append(f"{name}: {d} is not linked from docs/NAVIGATOR.md")
    for d in docs:
        stem = Path(d).name.rsplit(".", 1)[0]
        if not (KEBAB.fullmatch(stem) or UPPER.fullmatch(stem)):
            problems.append(f"{name}: {d}: not a kebab-case (or upper-case artifact) name")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("repos", nargs="*", default=REPOS)
    args = parser.parse_args()
    problems: list[str] = []
    for name in args.repos:
        repo = args.root / name
        if not (repo / ".git").exists():
            problems.append(f"{name}: no checkout at {repo}")
            continue
        problems += check(repo, name)
    for p in problems:
        print(p)
    print(f"doccheck: {len(args.repos)} repositories, {len(problems)} problem(s)", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
