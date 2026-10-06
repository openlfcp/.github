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
```

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
   - `sdk-ts.lock` and `server.lock` in obsidian;
   - `server.lock` in sdk-ts (the server its live tests run against);
   - `conformance/pins.json` in examples.

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
   | examples | install, build, typecheck, lint, test, `conformance/dist/run.js --strict` |
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
