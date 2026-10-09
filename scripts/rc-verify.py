#!/usr/bin/env python3
"""Local release-candidate verification for OpenLFCP (LFCP-072; MVP 0.2: LFCP-02-102).

Checks out the seven repositories at the commits a manifest pins, into ONE
persistent RC directory (git worktrees of the sibling checkouts, reused on
every run), checks that their pins agree, runs every release-blocking gate
and writes a report. See docs/release/rc-verification.md.

    scripts/rc-verify.py --from-heads [--write-manifest FILE]   # pin the committed HEADs
    scripts/rc-verify.py --manifest FILE                        # pin a given manifest
    options: --rc-dir DIR (default $LFCP_RC_DIR or ../openlfcp-rc next to the
             checkouts), --only GATE[,GATE...], --consistency-only,
             --baseline mvp-0.N-baseline (default: the nearest mvp-*-baseline.*
             tag in spec HEAD's history), --with website,native (optional
             gates: the website checkout, and the obsidian native harness),
             --assemble DIR [--repro] (build and checksum the candidate's artifacts)

A release-evidence JSON (the MVP 0.2 RELEASE-EVIDENCE template,
docs/release/mvp-0.2-release-evidence-template.json, with the fields this
run can fill) is written next to every report. With --assemble DIR, the
candidate's installable artifacts are built from fresh clones at the
pinned commits into DIR (scripts/rc_assemble.py: the @openlfcp/* npm
tarballs, the server binaries, the plugin files; --repro builds them twice
and compares), and their sha256 go into that record.

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
# Checkouts added to the manifest only when an optional gate needs them (--with).
OPTIONAL_REPOS = {"website": ["website"], "native": []}
# Optional gates, run only when asked for with --with.
OPTIONAL_GATES = ("website", "native")
# Spec baseline tags: mvp-0.1-baseline.N (MVP 0.1 and its sustaining
# releases), mvp-0.2-baseline.N (MVP 0.2), and later series alike.
BASELINE_GLOB = "mvp-*-baseline.*"
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


def manifest_from_heads(baseline: str | None = None, extra: tuple[str, ...] = ()) -> dict:
    """The committed HEADs. The spec's baseline tag is the nearest one of the
    series `baseline` (e.g. mvp-0.2-baseline), or of any series."""
    m: dict = {"created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    match = f"{baseline}.*" if baseline else BASELINE_GLOB
    for repo in (*REPOS, *extra):
        path = ROOT / repo
        entry = {"commit": git(path, "rev-parse", "HEAD")}
        if repo == "spec":
            # The implementations pin a baseline tag; spec HEAD may carry
            # later commits (ADRs, docs). The spec gate tests HEAD (`commit`);
            # the pins are checked against the tag's commit (`tag_commit`).
            if run(["git", "describe", "--tags", "--abbrev=0", "--match", match, "HEAD"], path) != 0:
                sys.exit(f"rc-verify: spec HEAD has no {match} tag in its history")
            entry["tag"] = git(path, "describe", "--tags", "--abbrev=0", "--match", match, "HEAD")
            entry["tag_commit"] = git(path, "rev-parse", f"refs/tags/{entry['tag']}^{{commit}}")
        dirty = git(path, "status", "--porcelain", "--untracked-files=no")
        if dirty:
            entry["note"] = "uncommitted changes in the checkout are not part of this RC"
        m[repo] = entry
    return m


# ------------------------------------------------------------------ worktrees


def manifest_repos(manifest: dict) -> list[str]:
    """The checkouts a manifest pins: the seven, then any optional ones."""
    return [r for r in (*REPOS, *(r for rs in OPTIONAL_REPOS.values() for r in rs)) if r in manifest]


def prepare(rc: Path, manifest: dict) -> None:
    rc.mkdir(parents=True, exist_ok=True)
    for repo in manifest_repos(manifest):
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
    tag_commit = spec_tag_commit(manifest)
    resolved = git(rc / "spec", "rev-parse", f"refs/tags/{spec['tag']}^{{commit}}")
    if resolved != tag_commit:
        sys.exit(f"rc-verify: tag {spec['tag']} is {resolved}, the manifest says {tag_commit}")
    if run(["git", "merge-base", "--is-ancestor", tag_commit, spec["commit"]], rc / "spec") != 0:
        sys.exit(f"rc-verify: tag {spec['tag']} is not in the history of spec {spec['commit']}")


# ------------------------------------------------------------------ consistency

# Spec paths whose change after a baseline tag needs a new baseline: the
# normative documents, their schemas and CDDL, and the test vectors.
NORMATIVE = ("wire/", "profiles/", "integration/", "schemas/", "test-vectors/")


def spec_tag_commit(manifest: dict) -> str:
    """The commit the spec pins name: the baseline tag's (older manifests: the spec commit)."""
    spec = manifest["spec"]
    return spec.get("tag_commit", spec["commit"])


def spec_after_tag(rc: Path, manifest: dict) -> tuple[bool, list[dict]]:
    """The spec commits after the pinned baseline tag: docs and ADRs are
    fine; one touching a normative path means a new baseline is due."""
    spec = manifest["spec"]
    tag_commit = spec_tag_commit(manifest)
    out = []
    for line in git(rc / "spec", "log", "--format=%H %s", f"{tag_commit}..{spec['commit']}").splitlines():
        commit, subject = line.split(" ", 1)
        files = git(rc / "spec", "show", "--name-only", "--format=", commit).splitlines()
        normative = [f for f in files if f.startswith(NORMATIVE) or f.endswith(".cddl")]
        out.append({"commit": commit, "subject": subject, "normative": normative})
    return all(not c["normative"] for c in out), out


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def consistency(rc: Path, manifest: dict) -> tuple[bool, list[dict]]:
    """Every pin agrees with the manifest; and, against the local HEADs, what lags."""
    m = {r: manifest[r]["commit"] for r in REPOS}
    m["spec"] = spec_tag_commit(manifest)
    spec_tag = manifest["spec"]["tag"]
    pins = []

    def pin(owner: str, file: str, field: str, target: str, value: str) -> None:
        pins.append({"owner": owner, "file": file, "field": field, "target": target, "value": value})

    for owner in ["sdk-ts", "sdk-rs", "server", "obsidian"]:
        lock = read_json(rc / owner / "spec.lock")
        pin(owner, "spec.lock", "commit", "spec", lock["commit"])
        pins[-1]["tag"] = lock.get("tag")
    pin("server", "sdk-rs.lock", "commit", "sdk-rs", read_json(rc / "server" / "sdk-rs.lock")["commit"])
    # Before 0.3.1 obsidian linked ../sdk-ts at sdk-ts.lock; since, it
    # depends on the published @openlfcp/* packages, pinned by version.
    if (rc / "obsidian" / "sdk-ts.lock").exists():
        pin("obsidian", "sdk-ts.lock", "commit", "sdk-ts", read_json(rc / "obsidian" / "sdk-ts.lock")["commit"])
    else:
        pins.extend(npm_pins(rc))
    pin("obsidian", "server.lock", "commit", "server", read_json(rc / "obsidian" / "server.lock")["commit"])
    # sdk-ts pins the server its live tests run against (absent before rc5).
    if (rc / "sdk-ts" / "server.lock").exists():
        pin("sdk-ts", "server.lock", "commit", "server", read_json(rc / "sdk-ts" / "server.lock")["commit"])
    pins_json = read_json(rc / "examples" / "conformance" / "pins.json")
    pin("examples", "conformance/pins.json", "sdk_rs", "sdk-rs", pins_json["sdk_rs"])
    pin("examples", "conformance/pins.json", "sdk_ts", "sdk-ts", pins_json["sdk_ts"])
    pin("examples", "conformance/pins.json", "spec", "spec", pins_json["spec"])

    ok = dev_pins(rc, m["spec"], pins)
    for p in pins:
        if p.get("kind") == "npm":
            ok = ok and p["matches_manifest"] and p["published"] is not False
            continue
        if p.get("kind") == "dev":
            continue
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


def dev_pins(rc: Path, tag_commit: str, pins: list[dict]) -> bool:
    """spec-sections.lock: the MVP 0.2 development pin of the section corpus,
    before the first mvp-0.2 baseline tag. It names no tag and is not the
    manifest's spec: it must exist in spec, descend from the pinned
    baseline, and be the same in every SDK that has one."""
    found = []
    for owner in ["sdk-ts", "sdk-rs"]:
        path = rc / owner / "spec-sections.lock"
        if not path.exists():
            continue
        value = read_json(path)["commit"]
        spec = ROOT / "spec"
        exists = run(["git", "cat-file", "-e", f"{value}^{{commit}}"], spec) == 0
        descends = exists and run(["git", "merge-base", "--is-ancestor", tag_commit, value], spec) == 0
        found.append(
            {"kind": "dev", "owner": owner, "file": "spec-sections.lock", "field": "commit", "target": "spec",
             "value": value, "exists": exists, "descends_from_baseline": descends}
        )
    agree = len({p["value"] for p in found}) <= 1
    for p in found:
        p["agrees"] = agree
    pins.extend(found)
    return all(p["exists"] and p["descends_from_baseline"] and p["agrees"] for p in found)


def npm_published(name: str, version: str) -> bool | None:
    """Whether npm has name@version; None when the registry cannot be reached."""
    try:
        r = subprocess.run(
            ["npm", "view", f"{name}@{version}", "version"], capture_output=True, text=True, timeout=60
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if r.returncode == 0:
        return r.stdout.strip() == version
    return False if "E404" in r.stderr else None


def npm_pins(rc: Path) -> list[dict]:
    """obsidian's @openlfcp/* dependencies: each must be the exact version of
    that sdk-ts package at the manifest commit, and published on npm."""
    sdk = {}
    for manifest in sorted((rc / "sdk-ts" / "packages").glob("*/package.json")):
        pkg = read_json(manifest)
        sdk[pkg["name"]] = pkg["version"]
    pkg = read_json(rc / "obsidian" / "package.json")
    deps = {**pkg.get("devDependencies", {}), **pkg.get("dependencies", {})}
    pins = []
    for name, value in sorted(deps.items()):
        if not name.startswith("@openlfcp/"):
            continue
        published = npm_published(name, value)
        pins.append({
            "kind": "npm", "owner": "obsidian", "file": "package.json", "field": name,
            "target": "sdk-ts", "value": value, "expected": sdk.get(name),
            "matches_manifest": value == sdk.get(name), "published": published,
        })
    return pins


# ------------------------------------------------------------------ gates


def gates(rc: Path, target_dir: Path, extra: tuple[str, ...] = ()) -> list[dict]:
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
            # The npm packages as they would be published (nothing is):
            # clean build, pack, tarball contents and manifests, install the
            # tarballs into a fresh project and import them.
            ["pnpm", "release:check"],
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
    ] + [g for g in optional_gates(rc, base, cargo) if g["name"] in extra]


def optional_gates(rc: Path, base: dict, cargo: dict) -> list[dict]:
    """Gates run only with --with: they need a checkout or a desktop."""
    return [
        # The static website: every local link and asset it references exists.
        {"name": "website", "cwd": rc / "website", "env": base, "steps": [
            # The checker that ships with this rc-verify (a tool, not a pinned input).
            ["python3", str(Path(__file__).resolve().parent / "website-check.py"), str(rc / "website")],
        ]},
        # The obsidian native harness (real Obsidian, LFCP-02-096): needs a
        # desktop session; long, so never part of the default run.
        {"name": "native", "cwd": rc / "obsidian", "env": cargo, "steps": [
            ["pnpm", "install", "--frozen-lockfile"],
            ["pnpm", "run", "native"],
        ]},
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


def write_report(
    rc: Path,
    manifest: dict,
    consistent: bool,
    pins: list[dict],
    after_tag: list[dict],
    results: list[dict],
    tools: dict,
    assembly: dict | None = None,
) -> Path:
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
    for repo in manifest_repos(manifest):
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
        if p.get("kind") in ("npm", "dev"):
            continue
        gap = "; ".join(p["gap"]) if p["gap"] else "none"
        lines.append(
            f"| {p['owner']} `{p['file']}` {p['field']} → {p['target']} | {p['value'][:12]} | "
            f"{'yes' if p['matches_manifest'] else '**no**'} | {'yes' if p['ancestor_of_head'] else '**no**'} | {gap} |"
        )
    npm = [p for p in pins if p.get("kind") == "npm"]
    if npm:
        lines += [
            "",
            "Package pins: each obsidian `@openlfcp/*` dependency is the exact version of that sdk-ts package at the manifest commit, published on npm.",
            "",
            "| Pin | Value | sdk-ts at the manifest | Published on npm |",
            "| --- | --- | --- | --- |",
        ]
        published = {True: "yes", False: "**no**", None: "unchecked (registry unreachable)"}
        for p in npm:
            lines.append(
                f"| obsidian `package.json` {p['field']} | {p['value']} | "
                f"{p['expected'] or '**not in sdk-ts**'}{'' if p['matches_manifest'] else ' **≠**'} | {published[p['published']]} |"
            )
    dev = [p for p in pins if p.get("kind") == "dev"]
    if dev:
        lines += [
            "",
            "Dev pins, pre-baseline: `spec-sections.lock` pins the section corpus to a spec commit before the first "
            "MVP 0.2 baseline tag. It is not the manifest's spec; it must exist in spec, descend from the pinned "
            "baseline, and be the same in every SDK.",
            "",
            "| Pin | Value | Exists in spec | Descends from the baseline | Same in every SDK |",
            "| --- | --- | --- | --- | --- |",
        ]
        yes = {True: "yes", False: "**no**"}
        for p in dev:
            lines.append(
                f"| {p['owner']} `{p['file']}` → spec | {p['value'][:12]} | {yes[p['exists']]} | "
                f"{yes[p['descends_from_baseline']]} | {yes[p['agrees']]} |"
            )
    if after_tag:
        lines += [
            "",
            f"## Spec after {manifest['spec']['tag']}",
            "",
            "Spec commits after the pinned baseline tag. Docs and ADRs are fine; a normative change needs a new baseline.",
            "",
            "| Commit | Subject | Normative files |",
            "| --- | --- | --- |",
        ]
        for c in after_tag:
            normative = ", ".join(c["normative"]) if c["normative"] else "none"
            if c["normative"]:
                normative = f"**{normative}**"
            lines.append(f"| {c['commit'][:12]} | {c['subject']} | {normative} |")
    if assembly is not None:
        lines += ["", "## Artifacts (--assemble)", "", "| Artifact | sha256 | Rebuilt the same |", "| --- | --- | --- |"]
        for component, files in assembly["artifacts"].items():
            for name, digest in files.items():
                same = "not rebuilt"
                if assembly["reproducibility"] is not None:
                    r = assembly["reproducibility"][component][name]
                    same = "yes" if r["same"] else ("same content, other bytes" if r.get("same_content") else "**no**")
                lines.append(f"| {name} | `{digest[:16]}…` | {same} |")
        lines += ["", f"`SHA256SUMS` sha256: `{assembly['sha256sums']}`"]
    lines += ["", "## Tools", ""] + [f"- {k}: {v}" for k, v in tools.items()]
    lines += ["", f"Free disk at the end: {free_bytes(rc) / 1024**3:.1f} GB", ""]
    report = rc / f"report-{stamp}.md"
    report.write_text("\n".join(lines))
    (rc / f"report-{stamp}.json").write_text(
        json.dumps(
            {"ok": all_ok, "manifest": manifest, "pins": pins, "spec_after_tag": after_tag, "gates": results, "tools": tools, "assembly": assembly},
            indent=2,
        )
    )
    (rc / f"release-evidence-{stamp}.json").write_text(
        json.dumps(release_evidence(rc, manifest, consistent, results, tools, stamp, assembly), indent=2) + "\n"
    )
    return report


# ------------------------------------------------------------------ release evidence


def sha256_file(path: Path) -> str | None:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def component_version(path: Path) -> str | None:
    """A component's own version: a package.json, or a Cargo workspace."""
    for f in (path / "packages" / "core" / "package.json", path / "package.json"):
        if f.is_file():
            v = read_json(f).get("version")
            if v:
                return v
    cargo = path / "Cargo.toml"
    if cargo.is_file():
        import tomllib

        data = tomllib.loads(cargo.read_text())
        return (data.get("workspace", {}).get("package", {}) or data.get("package", {})).get("version")
    return None


TEMPLATE = Path(__file__).resolve().parents[1] / "docs" / "release" / "mvp-0.2-release-evidence-template.json"


def release_evidence(
    rc: Path,
    manifest: dict,
    consistent: bool,
    results: list[dict],
    tools: dict,
    stamp: str,
    assembly: dict | None = None,
) -> dict:
    """The MVP 0.2 RELEASE-EVIDENCE template with the fields this run can fill:
    components (commits, versions, lockfiles, toolchains, gate commands and,
    with --assemble, build commands and artifact checksums), the corpora,
    the host and the rc-verify gates. Scope gates G01-G12, test families
    T01-T12, budgets, the pilot and release operations need people and
    other runs: they stay as the template has them."""
    import copy

    record = copy.deepcopy(read_json(TEMPLATE))
    by_gate = {r["name"]: r for r in results}
    built = {} if assembly is None else assembly["artifacts"]
    commands = {} if assembly is None else assembly["build_commands"]
    filled = []
    for repo in manifest_repos(manifest):
        path = rc / repo
        lock = next((f for f in ("pnpm-lock.yaml", "Cargo.lock", "Gemfile.lock") if (path / f).is_file()), None)
        try:
            url = git(ROOT / repo, "remote", "get-url", "origin")
        except subprocess.CalledProcessError:
            url = None
        gate = by_gate.get(repo)
        filled.append({
            "component": repo,
            "repository_or_deployment": url,
            "commit_or_image_digest": manifest[repo]["commit"],
            # The spec's version is its baseline tag; a private root package's 0.0.0 is none.
            "version": manifest[repo].get("tag") if repo == "spec" else (
                None if component_version(path) in (None, "0.0.0") else component_version(path)
            ),
            "lockfile_hash": None if lock is None else {lock: sha256_file(path / lock)},
            "toolchain": {k: v for k, v in tools.items() if k in ("node", "pnpm", "rustc", "cargo", "ruby", "python")},
            "build_command": commands.get(repo) or None,
            "test_commands": [] if gate is None else [s["cmd"] for s in gate["steps"]],
            "gate_status": "NOT_RUN" if gate is None else ("PASS" if gate["ok"] else "FAIL"),
            "artifact_checksums": built.get(repo, {}),
            "owner": None,
        })
    # The template's components first (filled when this run knows them), then the others.
    known = {c["component"]: c for c in filled}
    record["components"] = [known.pop(c["component"], c) for c in record["components"]] + list(known.values())
    spec = manifest["spec"]
    record.update({
        "record_type": "release_evidence_from_rc_verify",
        "candidate_id": stamp,
        "candidate_status": "NOT_QUALIFIED",
        "instructions": "Filled by rc-verify from this run only. Null and NOT_RUN are not passing evidence; scope gates, families, budgets, pilot and release operations are reviewed by people.",
        "pins_consistent": consistent,
    })
    record["scope"].update({"wire_subset_revision": spec.get("tag"), "spec_commit": spec["commit"], "spec_tag_commit": spec_tag_commit(manifest)})
    if assembly is not None:
        record["scope"]["corpus_sha256"] = {k: v["archive_sha256"] for k, v in assembly["corpora"].items()}
        record["assembly"] = {
            "sha256sums_sha256": assembly["sha256sums"],
            "corpora": assembly["corpora"],
            "reproducibility": assembly["reproducibility"],
            "seconds": assembly["seconds"],
        }
    record["environments"].append({
        "id": "rc-verify-host",
        "status": "PINNED",
        "os_build": tools.get("os"),
        "architecture": platform.machine(),
        "runtime_versions": {k: v for k, v in tools.items() if k != "os"},
    })
    # Logs by their path under the RC directory: the record carries no local paths.
    record["rc_gates"] = [
        {"gate": r["name"], "status": "PASS" if r["ok"] else "FAIL", "seconds": r["seconds"], "log": f"logs/{Path(r['log']).name}"}
        for r in results
    ]
    return record


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--manifest", type=Path)
    src.add_argument("--from-heads", action="store_true")
    ap.add_argument("--write-manifest", type=Path)
    ap.add_argument("--rc-dir", type=Path, default=Path(os.environ.get("LFCP_RC_DIR", ROOT / "openlfcp-rc")))
    ap.add_argument("--only", default="")
    ap.add_argument("--consistency-only", action="store_true")
    ap.add_argument("--baseline", default=None, help="baseline tag series, e.g. mvp-0.2-baseline")
    ap.add_argument("--with", dest="extra", default="", help=f"optional gates: {','.join(OPTIONAL_GATES)}")
    ap.add_argument("--assemble", type=Path, default=None, help="build the candidate's artifacts into this empty directory")
    ap.add_argument("--repro", action="store_true", help="with --assemble: build twice and compare the checksums")
    args = ap.parse_args()
    extra = tuple(g for g in args.extra.split(",") if g)
    unknown = [g for g in extra if g not in OPTIONAL_GATES]
    if unknown:
        sys.exit(f"rc-verify: unknown optional gate(s) {', '.join(unknown)}; known: {', '.join(OPTIONAL_GATES)}")
    extra_repos = tuple(r for g in extra for r in OPTIONAL_REPOS[g])

    rc: Path = args.rc_dir.resolve()
    require_disk(ROOT)
    manifest = read_json(args.manifest) if args.manifest else manifest_from_heads(args.baseline, extra_repos)
    if args.write_manifest:
        args.write_manifest.write_text(json.dumps(manifest, indent=2) + "\n")
    prepare(rc, manifest)
    consistent, pins = consistency(rc, manifest)
    # A normative spec change after the pinned tag makes the pins inconsistent.
    spec_ok, after_tag = spec_after_tag(rc, manifest)
    consistent = consistent and spec_ok
    target_dir = Path(os.environ.get("LFCP_SERVER_TARGET_DIR", Path(tempfile.gettempdir()) / "openlfcp-sdk-ts-server-target"))
    results = []
    if not args.consistency_only:
        (rc / "logs").mkdir(exist_ok=True)
        only = {g for g in args.only.split(",") if g}
        for gate in gates(rc, target_dir, extra):
            if only and gate["name"] not in only:
                continue
            print(f"rc-verify: {gate['name']} …", flush=True)
            r = run_gate(gate, rc / "logs", ROOT)
            print(f"rc-verify: {gate['name']} {'PASS' if r['ok'] else 'FAIL'} ({r['seconds']} s)", flush=True)
            results.append(r)
    assembly = None
    if args.assemble is not None:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from rc_assemble import assemble

        require_disk(ROOT)
        print(f"rc-verify: assemble into {args.assemble} …", flush=True)
        try:
            assembly = assemble(ROOT, manifest, args.assemble.resolve(), args.repro, rc / "logs")
        except RuntimeError as e:
            print(f"rc-verify: {e}", flush=True)
            assembly = None
            results.append({"name": "assemble", "ok": False, "seconds": 0, "log": str(rc / "logs" / "assemble.log"), "steps": [], "tail": [str(e)]})
        else:
            print(f"rc-verify: assembled in {assembly['seconds']} s", flush=True)
            if assembly["reproducibility"] is not None:
                differ = [
                    n for files in assembly["reproducibility"].values() for n, r in files.items()
                    if not r["same"] and not r.get("same_content")
                ]
                if differ:
                    print(f"rc-verify: not reproduced: {', '.join(differ)}", flush=True)
    elif args.repro:
        sys.exit("rc-verify: --repro needs --assemble DIR")
    report = write_report(rc, manifest, consistent, pins, after_tag, results, versions(), assembly)
    print(f"rc-verify: report {report}")
    ok = consistent and all(r["ok"] for r in results)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
