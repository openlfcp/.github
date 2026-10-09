# Release-candidate verification (local)

**Status:** LFCP-072 tooling. Until CI runs on the pushed repositories, this
is the local evidence that every release-blocking check is green for one
pinned set of commits.

## Run

From this repository, with the seven checkouts side by side (`spec`,
`.github`, `sdk-ts`, `sdk-rs`, `server`, `examples`, `obsidian`):

```sh
scripts/rc-verify.py --from-heads --write-manifest /tmp/rc-manifest.json
scripts/rc-verify.py --manifest docs/release/rc-manifest.json   # a pinned set
scripts/rc-verify.py --from-heads --consistency-only            # pins only
scripts/rc-verify.py --from-heads --only sdk-rs,server          # some gates
scripts/rc-verify.py --from-heads --baseline mvp-0.2-baseline   # an MVP 0.2 candidate
scripts/rc-verify.py --from-heads --with website                 # plus an optional gate
scripts/rc-verify.py --from-heads --assemble /tmp/candidate --repro  # build the artifacts, twice
```

The spec baseline tag is the nearest `mvp-*-baseline.*` tag in spec HEAD's
history (`mvp-0.1-baseline.9` for the 0.1.x sustaining releases,
`mvp-0.2-baseline.N` for MVP 0.2); `--baseline <series>` requires one
series and stops when spec HEAD has none of its tags.

Optional gates run only when asked for with `--with`:

- `website`: the website checkout (next to the others) joins the
  manifest, and `scripts/website-check.py` checks that every local link and
  asset of its committed HTML and CSS exists;
- `native`: the obsidian native harness (`pnpm run native`, real Obsidian,
  LFCP-02-096). It needs a desktop session and takes long.

Every run also writes `release-evidence-<time>.json` next to the report.
It is the MVP 0.2 release-evidence template
([mvp-0.2-release-evidence-template.json](mvp-0.2-release-evidence-template.json))
with the fields this run can fill:

- each component's repository, commit, version, lockfile hash and toolchain;
- each component's gate commands and status;
- the host, the pins and the rc-verify gates (logs by their path under the
  RC directory);
- with `--assemble`, the build commands, the artifact checksums and the
  corpora.

Its status is always `NOT_QUALIFIED`: scope gates, test families, budgets,
the pilot and release operations are reviewed by people. The record holds
no local paths.

## Candidate artifacts (`--assemble`)

`--assemble DIR` (LFCP-02-073, `scripts/rc_assemble.py`) builds the
candidate's installable artifacts into the empty directory `DIR`. The build
uses fresh clones at the manifest's commits, laid out side by side as CI lays
them out, never the RC worktrees. It builds:

- **npm:** `pnpm pack` of the eight `@openlfcp/*` packages of sdk-ts, in
  publish order, after `pnpm install --frozen-lockfile` and `pnpm build`;
- **server:** the `lfcp-server` and `lfcp-admin` release binaries
  (`cargo build --release --locked`, against sdk-rs at the manifest commit).
  Their source paths are remapped to those of the image build (`/src`,
  `/usr/local/cargo`), so a binary carries no path of the machine that built
  it;
- **obsidian:** `main.js`, `manifest.json` and `styles.css`, built against the
  sdk-ts clone;
- **spec:** each `test-vectors/<corpus>`, as its git tree ID and the sha256
  of its `git archive`. These sha256 fill `scope.corpus_sha256`.

Every artifact's sha256 is in `DIR/artifacts/SHA256SUMS`, in the report and
in the evidence record. The artifacts are the immutable candidate: a
release publishes these files, never a rebuild.

`--repro` builds everything a second time: fresh clones and an empty
target at the same paths, the first build moved aside meanwhile, then each
checksum is compared. pnpm may write the dependencies it rewrites in a
packed `package.json` in another order, so a tarball whose bytes differ but
whose files are equal (`package.json` compared as JSON) is reported as
"same content, other bytes". Any other difference is reported as not
reproduced.

`--from-heads` pins every repository's committed HEAD. For the spec it
also records the newest `mvp-0.1-baseline.*` tag in HEAD's history and
that tag's commit: the spec gate tests HEAD, and the implementations' spec
pins must name the tag's commit. Uncommitted work in a checkout is never
part of the RC, because the gates run in separate worktrees at the pinned
commits.

## What it does

1. **Disk check.** Stops if less than 3 GB is free, before and during the
   run.
2. **RC directory.** Uses ONE persistent directory, `$LFCP_RC_DIR` (default
   `openlfcp-rc` next to the checkouts). It holds a git worktree of each
   checkout, moved to the pinned commit only when clean; it never resets or
   forces. Reruns reuse it, along with its `node_modules` and the shared
   Cargo target.
3. **Pins.** Every pin must name the RC commit, exist, and be an ancestor of
   the local HEAD:
   - `spec.lock` in sdk-ts, sdk-rs, server and obsidian;
   - `sdk-rs.lock` in server;
   - `server.lock` in obsidian;
   - `server.lock` in sdk-ts (the server its live tests run against);
   - `conformance/pins.json` in examples.

   obsidian's SDK pin is a version, not a commit. Since 0.3.1 it depends on
   the published `@openlfcp/*` npm packages: each must be the exact version
   that sdk-ts package has at the RC commit, and, when the npm registry can
   be reached, `npm view` must find it published (the report marks it
   "unchecked" offline). Before 0.3.1, obsidian linked `../sdk-ts` at
   `sdk-ts.lock`, a commit pin like the others; manifests of that time are
   checked that way.

   `spec-sections.lock` in sdk-ts and sdk-rs, while MVP 0.2 is before its
   first baseline tag, is a development pin of the shared sections corpus,
   not of the RC's spec: it names a spec commit and no tag. It is listed
   apart, as "dev pin, pre-baseline", and must exist in spec, descend from
   the pinned baseline tag, and be the same in every SDK that has one. It
   goes away when `mvp-0.2-baseline.1` is tagged and `spec.lock` moves to it.

   Spec commits after the pinned tag are listed in the report. ADRs and
   other docs there are fine; a commit touching `wire/`, `profiles/`,
   `integration/`, `schemas/`, `test-vectors/` or a `.cddl` file makes the
   pins inconsistent: a normative change needs a new baseline.

   Every pin that lags its repository's HEAD is listed with the commits in
   the gap.
4. **Gates.** Each runs in its worktree and is logged to `logs/<gate>.log`:

   | Gate | Steps |
   | --- | --- |
   | spec | `pnpm install --frozen-lockfile`, `bundle check`, `scripts/validate.sh` |
   | .github | `scripts/validate.sh` |
   | docs | `scripts/doccheck.py` across the seven worktrees, each at its pinned commit (see [Documentation check](#documentation-check)) |
   | sdk-rs | `cargo fmt --check`; `clippy -D warnings` and `test`, each with `--all-features` and `--no-default-features` |
   | server | `cargo fmt --check`, `clippy -D warnings`, `test` |
   | sdk-ts | install, build, typecheck, lint, `pnpm test` (live tests against the server included), `pnpm release:check` (pack, check and install the npm packages; nothing is published) |
   | examples | install (with `npm ci` of the released 0.1.3 client in `qualification/legacy-0.1.3`, from the npm registry, and the obsidian worktree's dependencies, which `two-vault/` imports), build, typecheck, lint, test, `conformance/dist/run.js --strict` |
   | obsidian | install, build, lint, typecheck, `vitest run`, the E2E included; it fails if any test is skipped |

   Every gate runs with `LFCP_REQUIRE_LIVE=1`, so live tests may not skip,
   and Cargo uses the shared target directory (`$LFCP_SERVER_TARGET_DIR`,
   default `<tmp>/openlfcp-sdk-ts-server-target`). A gate fails if it leaves
   a tracked file changed.
5. **Report.** `report-<time>.md` and `.json` in the RC directory record:
   - PASS or FAIL per gate, with its duration and log;
   - the last lines of each failure;
   - the pin table;
   - every commit;
   - the tool versions (OS, git, node, pnpm, rustc, cargo, ruby, python).

The exit status is 0 only when the pins are consistent and every gate
passed.

## Documentation check

`scripts/doccheck.py` checks the committed Markdown of the seven checkouts
next to this repository (or of the repositories named, under `--root DIR`):

- every relative link and `#anchor` resolves, links into a sibling
  checkout included;
- every file under `docs/` is linked from that repository's
  `docs/NAVIGATOR.md`;
- `docs/` file names are kebab-case or the established upper-case
  artifact names.

```sh
scripts/doccheck.py                               # all seven checkouts
scripts/doccheck.py --root ../openlfcp-rc obsidian
```

It prints one line per problem and exits 1 when there is any. Links in
code spans and fenced blocks, and uncommitted files, are not checked.

## Requirements

Python 3, git, Node 24 with pnpm, a Rust toolchain, and Ruby with bundler
for the spec's CDDL check. The spec gate reuses the main checkout's
`vendor/bundle` gems when they are there.

## Runs

| RC | Manifest | Result |
| --- | --- | --- |
| rc1 | [rc1-manifest.json](rc1-manifest.json) | All seven gates PASS on Darwin 25.5.0 arm64. The spec gate passed on a rerun after the bundler fix in rc-verify. Pins are consistent with no lag. Excludes in-flight LFCP-067 and LFCP-071 work. |
| rc2 | [rc2-manifest.json](rc2-manifest.json) | All eight gates PASS (the docs gate is new) on Darwin 25.5.0 arm64, at spec `mvp-0.1-baseline.8`. Pins are consistent with no lag. The first run failed one examples test on a random Resource ID starting with "-" (fixed in examples 2a686a3); a rerun then failed four gates on a damaged build-script output in the shared Cargo target directory (repaired, not a code change); the third run passed. Excludes obsidian cfcb7a5 (rc3). |
| rc3 | [rc3-manifest.json](rc3-manifest.json) | All eight gates PASS on Darwin 25.5.0 arm64, at spec `mvp-0.1-baseline.8`, on the first run. Pins are consistent with no lag. rc2 plus obsidian cfcb7a5 (collaborators whose edits cannot be applied). |
| rc4 | [rc4-manifest.json](rc4-manifest.json) | All eight gates PASS on Darwin 25.5.0 arm64 on the first run, the sdk-ts gate now including `pnpm release:check` (the eight @openlfcp packages at 0.1.0-rc.1 packed, checked, installed and imported; nothing published). Spec HEAD is 509c1c1, the owner's ADR approvals after `mvp-0.1-baseline.8`, with no normative change; every pin names the tag's commit and is consistent. The commit set the owner pushes and publishes from. |
| rc5 | [rc5-manifest.json](rc5-manifest.json) | All eight gates PASS on Darwin 25.5.0 arm64 on the first run, `pnpm release:check` included. rc4 plus: server f1fcf29 (connections close without discarding the final ERROR; the LFCP-055 deploy check), sdk-ts d60e491 (property-test timeouts for slow CI runners, `server.lock`, live interop in its CI), and the pins moved to them. Every pin is consistent, sdk-ts `server.lock` checked for the first time. The set for the owner's second push. |
| rc6 | [rc6-manifest.json](rc6-manifest.json) | All eight gates PASS on Darwin 25.5.0 arm64 on the first run, `pnpm release:check` included. rc5 plus server e84fa74 (the server starts on Windows, 4cfa5f4; a Windows CI job, 96027a1; the Windows state-file ACL note), with sdk-ts 98efaab, obsidian 3cc9915 and examples fe3de90 pinned to it and the Windows limitation in the release notes. Every pin is consistent. |
| rc7 | [rc7-manifest.json](rc7-manifest.json) | All eight gates PASS on Darwin 25.5.0 arm64 on the first run, `pnpm release:check` included (the eight packages at 0.1.0, dist-tag `latest`). The MVP 0.1.0 release: rc6 with the versions set to 0.1.0 (sdk-rs c9132b1, server 896bbab, sdk-ts 4e1b02f, obsidian e8e212f, examples 943a6ad, with obsidian faaf020's secret-ID fix and the macOS smoke record) and every pin moved to them; the docs are the final release notes (.github 71d0552). Every pin is consistent. Each repository tags its commit `v0.1.0`. Known flaky test: sdk-ts `conformance/security/engine-trap.test.ts` can hit its 60 s child-process timeout on a loaded machine; it passed here and on a rerun alone. |
| rc8 | [rc8-manifest.json](rc8-manifest.json) | All eight gates PASS on Darwin 25.5.0 arm64 on the first run, `pnpm release:check` included, with CARGO_BUILD_JOBS=4 and two Rust test threads. The server 0.2.0 release: rc7 plus server POST-003 (abuse limits, quotas, revocation at quota), POST-004 (memory bounds, WebSocket fragments) and the ghcr image workflow, with the version set to 0.2.0 (server d6cd820). sdk-ts 98519b5, obsidian 2fd6890 and examples b189806 are pinned to it; sdk-rs, sdk-ts, the plugin and the examples stay at 0.1.0. The docs are the server 0.2.0 release notes (.github 7acab55). Every pin is consistent. Only the server tags its commit, `v0.2.0`. |
| rc9 | [rc9-manifest.json](rc9-manifest.json) | All seven gates run PASS on Darwin 25.5.0 arm64 (spec, .github, docs, sdk-rs, server, sdk-ts, examples), with CARGO_BUILD_JOBS=4, two Rust test threads and two vitest workers; the obsidian gate was not run. The 0.1.x sustaining release of MVP 0.2 wave W0: spec `mvp-0.1-baseline.9` (f42533c; ADR 0008, POST-001), sdk-rs 259a688, server 0.3.0 (09c9132), sdk-ts 0.1.2 (777f36e: `pnpm test` in full, live tests included, and `pnpm release:check`), examples 9a26d33 (`conformance/dist/run.js --strict`). The run used a local `mvp-0.1-baseline.9` tag, before the owner's push. Pins are consistent except obsidian's (`spec.lock`, `server.lock`, `@openlfcp/*` 0.1.1), which move with Shared Tasks 0.3.2 after the npm publish of 0.1.2. An earlier rc9 run failed sdk-ts on the seeded chaos test (seed 3) against server 0.3.0; sdk-ts 777f36e fixes it. |
| rc10 | [rc10-manifest.json](rc10-manifest.json) | The Shared Tasks 0.3.2 release: obsidian 1cfce1e on the published `@openlfcp/*` 0.1.3 (exact versions, all found on npm), spec `mvp-0.1-baseline.9` (f42533c), server 0.3.0 (09c9132), sdk-ts 0.1.3 (7e9462f), sdk-rs 259a688, examples 892be03. An explicit manifest, not `--from-heads`: the sdk-ts and server HEADs have moved to `mvp-0.2-baseline.1`. Every pin is consistent. Gates run on Darwin 25.5.0 arm64 with two vitest workers: obsidian (747/747, no skips), docs and .github PASS; the other gates were not rerun, their commits being those of the 0.1.3 and 0.3.0 releases. The plugin's own gate on a clean clone also ran its live tests against server 0.3.0 and the native harness on Obsidian 1.13.4 and 1.14.4. |
