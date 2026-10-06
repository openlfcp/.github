#!/usr/bin/env python3
"""Local release-candidate verification for OpenLFCP MVP 0.1 (LFCP-072).

Checks out the seven repositories at the commits a manifest pins, into ONE
persistent RC directory (git worktrees of the sibling checkouts, reused on
every run), checks that their pins agree, runs every release-blocking gate
and writes a report. See docs/release/rc-verification.md.

    scripts/rc-verify.py --from-heads [--write-manifest FILE]   # pin the committed HEADs
    scripts/rc-verify.py --manifest FILE                        # pin a given manifest
    options: --rc-dir DIR (default $LFCP_RC_DIR or ../openlfcp-rc next to the
             checkouts), --only GATE[,GATE...], --consistency-only

Rules it keeps: worktrees are only ever moved between commits when clean
(never reset, never forced); one shared Cargo target directory
($LFCP_SERVER_TARGET_DIR, default <tmp>/openlfcp-sdk-ts-server-target); live
tests may not skip (LFCP_REQUIRE_LIVE=1); it stops below 3 GB of free disk.
Logs are kept per gate under <rc-dir>/logs; nothing is pushed or published.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPOS = [".github", "spec", "sdk-rs", "server", "sdk-ts", "examples", "obsidian"]
MIN_FREE_BYTES = 3 * 1024**3
ROOT = Path(__file__).resolve().parents[2]  # the directory holding the checkouts


def run(cmd: list[str], cwd: Path, env: dict | None = None, log=None) -> int:
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        stdout=log if log is not None else subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return proc.returncode


def out(cmd: list[str], cwd: Path) -> str:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def git(repo: Path, *args: str) -> str:
    return out(["git", "-C", str(repo), *args], repo)


def free_bytes(path: Path) -> int:
    return shutil.disk_usage(path).free


def require_disk(path: Path) -> None:
    free = free_bytes(path)
    if free < MIN_FREE_BYTES:
        sys.exit(f"rc-verify: only {free / 1024**3:.1f} GB free; stopping (the limit is 3 GB)")


# ------------------------------------------------------------------ manifest


def manifest_from_heads() -> dict:
    m: dict = {"created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    for repo in REPOS:
        path = ROOT / repo
        entry = {"commit": git(path, "rev-parse", "HEAD")}
        if repo == "spec":
            tags = git(path, "tag", "--points-at", "HEAD").split()
            baseline = sorted(t for t in tags if t.startswith("mvp-0.1-baseline"))
            if not baseline:
                sys.exit("rc-verify: spec HEAD carries no mvp-0.1-baseline tag")
            entry["tag"] = baseline[-1]
        dirty = git(path, "status", "--porcelain", "--untracked-files=no")
        if dirty:
            entry["note"] = "uncommitted changes in the checkout are not part of this RC"
        m[repo] = entry
    return m


# ------------------------------------------------------------------ worktrees


def prepare(rc: Path, manifest: dict) -> None:
    rc.mkdir(parents=True, exist_ok=True)
    for repo in REPOS:
        source = ROOT / repo
        target = rc / repo
        commit = manifest[repo]["commit"]
        if not target.exists():
            git(source, "worktree", "add", "--detach", str(target), commit)
        else:
            if git(target, "status", "--porcelain", "--untracked-files=no"):
                sys.exit(f"rc-verify: {target} has tracked changes; clean it by hand first")
            git(target, "switch", "--detach", "--quiet", commit)
        if git(target, "rev-parse", "HEAD") != commit:
            sys.exit(f"rc-verify: {target} is not at {commit}")
    spec = manifest["spec"]
    resolved = git(rc / "spec", "rev-parse", f"refs/tags/{spec['tag']}^{{commit}}")
    if resolved != spec["commit"]:
        sys.exit(f"rc-verify: tag {spec['tag']} is {resolved}, the manifest says {spec['commit']}")


# ------------------------------------------------------------------ consistency


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def consistency(rc: Path, manifest: dict) -> tuple[bool, list[dict]]:
    """Every pin agrees with the manifest; and, against the local HEADs, what lags."""
    m = {r: manifest[r]["commit"] for r in REPOS}
    spec_tag = manifest["spec"]["tag"]
    pins = []

    def pin(owner: str, file: str, field: str, target: str, value: str) -> None:
        pins.append({"owner": owner, "file": file, "field": field, "target": target, "value": value})

    for owner in ["sdk-ts", "sdk-rs", "server", "obsidian"]:
        lock = read_json(rc / owner / "spec.lock")
        pin(owner, "spec.lock", "commit", "spec", lock["commit"])
        pins[-1]["tag"] = lock.get("tag")
    pin("server", "sdk-rs.lock", "commit", "sdk-rs", read_json(rc / "server" / "sdk-rs.lock")["commit"])
    pin("obsidian", "sdk-ts.lock", "commit", "sdk-ts", read_json(rc / "obsidian" / "sdk-ts.lock")["commit"])
    pin("obsidian", "server.lock", "commit", "server", read_json(rc / "obsidian" / "server.lock")["commit"])
    pins_json = read_json(rc / "examples" / "conformance" / "pins.json")
    pin("examples", "conformance/pins.json", "sdk_rs", "sdk-rs", pins_json["sdk_rs"])
    pin("examples", "conformance/pins.json", "sdk_ts", "sdk-ts", pins_json["sdk_ts"])
    pin("examples", "conformance/pins.json", "spec", "spec", pins_json["spec"])

    ok = True
    for p in pins:
        target = ROOT / p["target"]
        value = p["value"]
        p["matches_manifest"] = value == m[p["target"]] and (
            p.get("tag") is None or p["tag"] == spec_tag
        )
        ok = ok and p["matches_manifest"]
        exists = run(["git", "cat-file", "-e", f"{value}^{{commit}}"], target) == 0
        p["exists"] = exists
        head = git(target, "rev-parse", "HEAD")
        p["local_head"] = head
        if not exists:
            p["ancestor_of_head"] = False
            p["gap"] = []
            ok = False
            continue
        p["ancestor_of_head"] = (
            run(["git", "merge-base", "--is-ancestor", value, head], target) == 0
        )
        ok = ok and p["ancestor_of_head"]
        p["gap"] = git(target, "log", "--oneline", f"{value}..{head}").splitlines()
    return ok, pins


# ------------------------------------------------------------------ gates


def gates(rc: Path, target_dir: Path) -> list[dict]:
    base = dict(os.environ)
    base.update(
        {
            "LFCP_REQUIRE_LIVE": "1",
            "LFCP_SERVER_TARGET_DIR": str(target_dir),
            "LFCP_SERVER_DIR": str(rc / "server"),
            "LFCP_SPEC_DIR": str(rc / "spec"),
            "CI": "1",
        }
    )
    base.pop("LFCP_SERVER_BIN", None)
    cargo = dict(base, CARGO_TARGET_DIR=str(target_dir))
    spec_env = dict(base)
    # The spec's .bundle/config installs gems into vendor/bundle (and wins
    # over BUNDLE_PATH): link the main checkout's gems there instead of
    # installing them again.
    vendored = ROOT / "spec" / "vendor" / "bundle"
    link = rc / "spec" / "vendor" / "bundle"
    if vendored.is_dir() and not link.exists():
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(vendored)
    vitest_json = rc / "logs" / "obsidian-vitest.json"
    return [
        {"name": "spec", "cwd": rc / "spec", "env": spec_env, "steps": [
            ["pnpm", "install", "--frozen-lockfile"],
            ["bundle", "check"],
            ["./scripts/validate.sh"],
        ]},
        {"name": ".github", "cwd": rc / ".github", "env": base, "steps": [["./scripts/validate.sh"]]},
        # Links, anchors and NAVIGATOR coverage across all seven worktrees,
        # each at its pinned commit (the checker reads committed files).
        {"name": "docs", "cwd": rc / ".github", "env": base, "steps": [
            ["python3", "scripts/doccheck.py", "--root", str(rc), *REPOS],
        ]},
        {"name": "sdk-rs", "cwd": rc / "sdk-rs", "env": cargo, "steps": [
            ["cargo", "fmt", "--all", "--check"],
            ["cargo", "clippy", "--workspace", "--all-targets", "--all-features", "--", "-D", "warnings"],
            ["cargo", "clippy", "--workspace", "--all-targets", "--no-default-features", "--", "-D", "warnings"],
            ["cargo", "test", "--workspace", "--all-features"],
            ["cargo", "test", "--workspace", "--no-default-features"],
        ]},
        {"name": "server", "cwd": rc / "server", "env": cargo, "steps": [
            ["cargo", "fmt", "--all", "--check"],
            ["cargo", "clippy", "--workspace", "--all-targets", "--", "-D", "warnings"],
            ["cargo", "test", "--workspace"],
        ]},
        {"name": "sdk-ts", "cwd": rc / "sdk-ts", "env": cargo, "steps": [
            ["pnpm", "install", "--frozen-lockfile"],
            ["pnpm", "build"],
            ["pnpm", "typecheck"],
            ["pnpm", "lint"],
            ["pnpm", "test"],
        ]},
        {"name": "examples", "cwd": rc / "examples", "env": cargo, "steps": [
            ["pnpm", "install", "--frozen-lockfile"],
            ["pnpm", "build"],
            ["pnpm", "typecheck"],
            ["pnpm", "lint"],
            ["pnpm", "test"],
            ["node", "conformance/dist/run.js", "--strict"],
        ]},
        {"name": "obsidian", "cwd": rc / "obsidian", "env": cargo, "steps": [
            ["pnpm", "install", "--frozen-lockfile"],
            ["pnpm", "run", "build"],
            ["pnpm", "run", "lint"],
            ["pnpm", "run", "typecheck"],
            ["pnpm", "exec", "vitest", "run", "--reporter=default", "--reporter=json",
             f"--outputFile={vitest_json}"],
        ], "no_skips": vitest_json},
    ]


def run_gate(gate: dict, logs: Path, disk: Path) -> dict:
    log_path = logs / f"{gate['name'].strip('.')}.log"
    started = time.monotonic()
    result = {"name": gate["name"], "log": str(log_path), "steps": []}
    with open(log_path, "w") as log:
        for step in gate["steps"]:
            require_disk(disk)
            log.write(f"\n$ {' '.join(step)}\n")
            log.flush()
            t0 = time.monotonic()
            code = run(step, gate["cwd"], gate["env"], log)
            result["steps"].append({"cmd": " ".join(step), "code": code, "seconds": round(time.monotonic() - t0, 1)})
            if code != 0:
                break
    result["ok"] = all(s["code"] == 0 for s in result["steps"]) and len(result["steps"]) == len(gate["steps"])
    skips = gate.get("no_skips")
    if result["ok"] and skips is not None:
        report = read_json(Path(skips))
        skipped = report.get("numPendingTests", 0) + report.get("numTodoTests", 0)
        if skipped:
            result["ok"] = False
            result["steps"].append({"cmd": "fail on skip", "code": 1, "seconds": 0, "note": f"{skipped} skipped or todo"})
    # A gate must not leave tracked files changed.
    dirty = git(gate["cwd"], "status", "--porcelain", "--untracked-files=no")
    if dirty:
        result["ok"] = False
        result["steps"].append({"cmd": "tree clean after the gate", "code": 1, "seconds": 0, "note": dirty[:500]})
    result["seconds"] = round(time.monotonic() - started, 1)
    if not result["ok"]:
        lines = log_path.read_text(errors="replace").splitlines()
        result["tail"] = lines[-25:]
    return result


def versions() -> dict:
    def v(cmd: list[str]) -> str:
        try:
            return out(cmd, ROOT).splitlines()[0]
        except Exception:  # noqa: BLE001 — a missing tool is reported as such
            return "(not available)"

    return {
        "os": f"{platform.system()} {platform.release()} {platform.machine()}",
        "python": platform.python_version(),
        "git": v(["git", "--version"]),
        "node": v(["node", "--version"]),
        "pnpm": v(["pnpm", "--version"]),
        "rustc": v(["rustc", "--version"]),
        "cargo": v(["cargo", "--version"]),
        "ruby": v(["ruby", "--version"]),
    }


# ------------------------------------------------------------------ report


def write_report(rc: Path, manifest: dict, consistent: bool, pins: list[dict], results: list[dict], tools: dict) -> Path:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    all_ok = consistent and all(r["ok"] for r in results)
    lines = [
        f"# OpenLFCP release-candidate verification: {'PASS' if all_ok else 'FAIL'}",
        "",
        f"Run {stamp} on {tools['os']}. Local evidence: these gates ran here, not in CI.",
        "",
        "## Commits",
        "",
        "| Repository | Commit | Note |",
        "| --- | --- | --- |",
    ]
    for repo in REPOS:
        e = manifest[repo]
        note = e.get("tag", "") + (f" {e['note']}" if "note" in e else "")
        lines.append(f"| {repo} | {e['commit']} | {note.strip()} |")
    lines += ["", "## Gates", "", "| Gate | Result | Duration | Log |", "| --- | --- | --- | --- |"]
    for r in results:
        lines.append(f"| {r['name']} | {'PASS' if r['ok'] else '**FAIL**'} | {r['seconds']} s | {r['log']} |")
    for r in results:
        if not r["ok"]:
            failed = [s for s in r["steps"] if s["code"] != 0]
            lines += ["", f"### {r['name']}: failed at `{failed[0]['cmd'] if failed else '?'}`", ""]
            if failed and "note" in failed[0]:
                lines.append(f"{failed[0]['note']}")
            lines += ["```text", *r.get("tail", []), "```"]
    lines += [
        "",
        f"## Pins: {'consistent' if consistent else '**INCONSISTENT**'}",
        "",
        "Every pin must name the manifest's commit, exist, and be an ancestor of (or equal to) the local HEAD.",
        "",
        "| Pin | Value | = manifest | Ancestor of local HEAD | Commits it lags local HEAD |",
        "| --- | --- | --- | --- | --- |",
    ]
    for p in pins:
        gap = "; ".join(p["gap"]) if p["gap"] else "none"
        lines.append(
            f"| {p['owner']} `{p['file']}` {p['field']} → {p['target']} | {p['value'][:12]} | "
            f"{'yes' if p['matches_manifest'] else '**no**'} | {'yes' if p['ancestor_of_head'] else '**no**'} | {gap} |"
        )
    lines += ["", "## Tools", ""] + [f"- {k}: {v}" for k, v in tools.items()]
    lines += ["", f"Free disk at the end: {free_bytes(rc) / 1024**3:.1f} GB", ""]
    report = rc / f"report-{stamp}.md"
    report.write_text("\n".join(lines))
    (rc / f"report-{stamp}.json").write_text(
        json.dumps({"ok": all_ok, "manifest": manifest, "pins": pins, "gates": results, "tools": tools}, indent=2)
    )
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--manifest", type=Path)
    src.add_argument("--from-heads", action="store_true")
    ap.add_argument("--write-manifest", type=Path)
    ap.add_argument("--rc-dir", type=Path, default=Path(os.environ.get("LFCP_RC_DIR", ROOT / "openlfcp-rc")))
    ap.add_argument("--only", default="")
    ap.add_argument("--consistency-only", action="store_true")
    args = ap.parse_args()

    rc: Path = args.rc_dir.resolve()
    require_disk(ROOT)
    manifest = read_json(args.manifest) if args.manifest else manifest_from_heads()
    if args.write_manifest:
        args.write_manifest.write_text(json.dumps(manifest, indent=2) + "\n")
    prepare(rc, manifest)
    consistent, pins = consistency(rc, manifest)
    target_dir = Path(os.environ.get("LFCP_SERVER_TARGET_DIR", Path(tempfile.gettempdir()) / "openlfcp-sdk-ts-server-target"))
    results = []
    if not args.consistency_only:
        (rc / "logs").mkdir(exist_ok=True)
        only = {g for g in args.only.split(",") if g}
        for gate in gates(rc, target_dir):
            if only and gate["name"] not in only:
                continue
            print(f"rc-verify: {gate['name']} …", flush=True)
            r = run_gate(gate, rc / "logs", ROOT)
            print(f"rc-verify: {gate['name']} {'PASS' if r['ok'] else 'FAIL'} ({r['seconds']} s)", flush=True)
            results.append(r)
    report = write_report(rc, manifest, consistent, pins, results, versions())
    print(f"rc-verify: report {report}")
    ok = consistent and all(r["ok"] for r in results)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
