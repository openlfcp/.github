"""Immutable candidate artifacts for rc-verify --assemble (MVP 0.2: LFCP-02-073).

Builds a release candidate's installable artifacts from fresh clones at the
commits a manifest pins, laid out side by side as CI lays them out, and
records each artifact's sha256:

- npm: `pnpm pack` of every @openlfcp/* package of sdk-ts, in publish order;
- server: the `lfcp-server` and `lfcp-admin` release binaries (`cargo build
  --release --locked`, against sdk-rs at the manifest commit);
- obsidian: the plugin's `main.js`, `manifest.json` and `styles.css`, built
  against the sdk-ts clone (the plugin links `../sdk-ts` at `sdk-ts.lock`);
- spec: the corpora (`test-vectors/<corpus>`) as their git tree IDs and the
  sha256 of their `git archive`.

With `repro`, everything is built a second time in other fresh clones and
other build directories, and each artifact's two checksums are compared.
Nothing is published, pushed or tagged. The clones and the build
directories stay under `<out>/build*`; the artifacts and `SHA256SUMS` under
`<out>/artifacts`.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import time
from pathlib import Path

# The repositories the artifacts are built from, and what each needs beside it.
BUILD_REPOS = ["spec", "sdk-rs", "server", "sdk-ts", "obsidian"]
SERVER_BINARIES = ["lfcp-server", "lfcp-admin"]
PLUGIN_FILES = ["main.js", "manifest.json", "styles.css"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class Builder:
    def __init__(self, root: Path, manifest: dict, out: Path, log_dir: Path):
        self.root = root
        self.manifest = manifest
        self.out = out
        self.log_dir = log_dir
        self.commands: dict[str, list[str]] = {}

    def run(
        self, component: str, cmd: list[str], cwd: Path, env: dict | None = None, note: str = ""
    ) -> None:
        # Recorded relative to the assembly directory: the record carries no local paths.
        shown = note + " ".join(cmd).replace(f"{self.out}/", "")
        self.commands.setdefault(component, [])
        if shown not in self.commands[component]:
            self.commands[component].append(shown)
        log = self.log_dir / f"assemble-{component}.log"
        with log.open("a") as f:
            f.write(f"$ (cd {cwd.name}) {shown}\n")
            f.flush()
            code = subprocess.run(
                cmd, cwd=cwd, env={**os.environ, **(env or {})}, stdout=f, stderr=subprocess.STDOUT
            ).returncode
        if code != 0:
            raise RuntimeError(f"assemble: {component}: `{shown}` failed ({code}); see {log}")

    def layout(self, src: Path) -> None:
        """Fresh clones of the build repositories at the manifest commits, side by side."""
        src.mkdir(parents=True, exist_ok=True)
        for repo in BUILD_REPOS:
            commit = self.manifest[repo]["commit"]
            target = src / repo
            if target.exists():
                raise RuntimeError(f"assemble: {target} exists; use an empty --assemble directory")
            subprocess.run(["git", "clone", "--quiet", str(self.root / repo), str(target)], check=True)
            subprocess.run(["git", "checkout", "--quiet", "--detach", commit], cwd=target, check=True)

    def build(self, src: Path, target_dir: Path, into: Path) -> dict[str, dict[str, str]]:
        """Builds every artifact in the layout `src`; copies them under `into`; returns their sha256 by component."""
        sums: dict[str, dict[str, str]] = {}

        # sdk-ts: the npm packages, in publish order.
        sdk = src / "sdk-ts"
        self.run("sdk-ts", ["pnpm", "install", "--frozen-lockfile"], sdk)
        self.run("sdk-ts", ["pnpm", "build"], sdk)
        order = re.findall(r'"([a-z-]+)"', (sdk / "scripts" / "packages.mjs").read_text().split("[", 1)[1])
        npm = into / "npm"
        npm.mkdir(parents=True, exist_ok=True)
        for name in order:
            self.run("sdk-ts", ["pnpm", "pack", "--pack-destination", str(npm)], sdk / "packages" / name)
        sums["sdk-ts"] = {f"npm/{p.name}": sha256(p) for p in sorted(npm.glob("*.tgz"))}

        # server: release binaries against sdk-rs at the manifest commit.
        server = src / "server"
        cmd = ["cargo", "build", "--release", "--locked"]
        for b in SERVER_BINARIES:
            cmd += ["-p", b]
        # Source paths in the binary (panic locations) as the image build
        # (server/deploy/Dockerfile) has them, not this machine's: the
        # sources under /src, the Cargo home at /usr/local/cargo.
        cargo_home = os.environ.get("CARGO_HOME", str(Path.home() / ".cargo"))
        remap = f"--remap-path-prefix={src}=/src\x1f--remap-path-prefix={cargo_home}=/usr/local/cargo"
        self.run(
            "server",
            cmd,
            server,
            {"CARGO_TARGET_DIR": str(target_dir), "CARGO_ENCODED_RUSTFLAGS": remap},
            note="RUSTFLAGS='--remap-path-prefix=<sources>=/src --remap-path-prefix=<cargo home>=/usr/local/cargo' ",
        )
        triple = f"{platform.system().lower()}-{platform.machine().lower()}"
        bins = into / "server" / triple
        bins.mkdir(parents=True, exist_ok=True)
        sums["server"] = {}
        for b in SERVER_BINARIES:
            shutil.copy2(target_dir / "release" / b, bins / b)
            sums["server"][f"server/{triple}/{b}"] = sha256(bins / b)

        # obsidian: the plugin files, built against the sdk-ts clone.
        plugin = src / "obsidian"
        self.run("obsidian", ["pnpm", "install", "--frozen-lockfile"], plugin)
        self.run("obsidian", ["pnpm", "build"], plugin)
        files = into / "obsidian"
        files.mkdir(parents=True, exist_ok=True)
        sums["obsidian"] = {}
        for name in PLUGIN_FILES:
            shutil.copy2(plugin / name, files / name)
            sums["obsidian"][f"obsidian/{name}"] = sha256(files / name)
        return sums


def same_content(a: Path, b: Path) -> bool:
    """Two npm tarballs with the same files, each package.json equal as JSON
    (pnpm pack may order the dependencies it rewrites differently)."""
    import tarfile

    def files(p: Path) -> dict[str, object]:
        out: dict[str, object] = {}
        with tarfile.open(p) as t:
            for m in t.getmembers():
                if m.isfile():
                    data = t.extractfile(m).read()
                    out[m.name] = json.loads(data) if m.name.endswith("package.json") else data
        return out

    return files(a) == files(b)


def corpora(spec: Path, commit: str) -> dict[str, dict[str, str]]:
    """Each test-vector corpus at `commit`: its git tree ID and the sha256 of its git archive."""
    names = subprocess.run(
        ["git", "ls-tree", "-d", "--name-only", f"{commit}:test-vectors"],
        cwd=spec, check=True, capture_output=True, text=True,
    ).stdout.split()
    out = {}
    for name in names:
        path = f"test-vectors/{name}"
        tree = subprocess.run(
            ["git", "rev-parse", f"{commit}:{path}"], cwd=spec, check=True, capture_output=True, text=True
        ).stdout.strip()
        archive = subprocess.run(
            ["git", "archive", "--format=tar", commit, "--", path], cwd=spec, check=True, capture_output=True
        ).stdout
        out[path] = {"git_tree": tree, "archive_sha256": hashlib.sha256(archive).hexdigest()}
    return out


def assemble(root: Path, manifest: dict, out: Path, repro: bool, log_dir: Path) -> dict:
    """Builds the candidate's artifacts (twice with `repro`); returns the assembly record."""
    out.mkdir(parents=True, exist_ok=True)
    if any((out / d).exists() for d in ("artifacts", "build", "build-repro", "build-first", "build-repro-artifacts")):
        raise RuntimeError(f"assemble: {out} already holds an assembly; use an empty directory")
    log_dir.mkdir(parents=True, exist_ok=True)
    started = time.time()
    builder = Builder(root, manifest, out, log_dir)
    builder.layout(out / "build" / "src")
    artifacts = out / "artifacts"
    sums = builder.build(out / "build" / "src", out / "build" / "target", artifacts)
    record: dict = {
        "artifacts": sums,
        "build_commands": builder.commands,
        "corpora": corpora(out / "build" / "src" / "spec", manifest["spec"]["commit"]),
        "reproducibility": None,
    }
    if repro:
        # The second build is a clean one at the same paths (fresh clones,
        # an empty target), as a verifier rebuilds: the first build is moved
        # aside meanwhile, then back; the second ends in build-repro.
        (out / "build").rename(out / "build-first")
        again = Builder(root, manifest, out, log_dir)
        again.layout(out / "build" / "src")
        second = out / "build-repro-artifacts"
        sums2 = again.build(out / "build" / "src", out / "build" / "target", second)
        (out / "build").rename(out / "build-repro")
        (out / "build-first").rename(out / "build")
        second = second.rename(out / "build-repro" / "artifacts")
        record["reproducibility"] = {}
        for component, files in sums.items():
            record["reproducibility"][component] = {}
            for name, digest in files.items():
                other = sums2.get(component, {}).get(name)
                entry: dict = {"same": other == digest, "second_sha256": other}
                if other != digest and name.endswith(".tgz") and other is not None:
                    entry["same_content"] = same_content(artifacts / name, second / name)
                record["reproducibility"][component][name] = entry
    lines = [f"{d}  {name}" for files in sums.values() for name, d in sorted(files.items())]
    (artifacts / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    record["sha256sums"] = sha256(artifacts / "SHA256SUMS")
    record["seconds"] = round(time.time() - started)
    (out / "assembly.json").write_text(json.dumps(record, indent=2) + "\n")
    return record
