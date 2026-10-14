# MVP 0.3 baseline manifest

**Task:** LFCP-03-001 (M03-0, gate G03-A). **Date:** 2026-10-15.
**Method:** read-only audit of the `openlfcp/*` repositories at the commits
below, plus CI results reused from the MVP 0.2 release. One targeted
reproducer ran for a disputed fact (see the
[gap register](gap-register.md#whole-projection-deletion-versus-body-deletion)).
No full test run and no native Obsidian run was made for this task.

MVP 0.3 starts from the **released MVP 0.2**. The research that produced
the MVP 0.3 package looked at an older build (plugin 0.4.0-beta.8, see
[Researched build](#researched-build-superseded)). Work for 0.3 is
planned against the commits here, not against beta.8.

## Released baseline

| Repository | Version / tag | Commit (full SHA) | Notes |
| --- | --- | --- | --- |
| `openlfcp/obsidian` | Shared Tasks `0.4.0` (tag `0.4.0`) | `ce0660a519cdce089630e63e1d390009c6148284` | `main` is the tag commit; `manifest.json` and `manifest-beta.json` both 0.4.0, `minAppVersion` 1.13.4 |
| `openlfcp/sdk-ts` | `@openlfcp/*` 0.2.0 (tag `v0.2.0`, npm `latest`) | `2a34beb2c3ae3a4cfc9f4d5333cee5f85ca587fd` | 8 packages; npm `beta` stays at 0.2.0-beta.10 |
| `openlfcp/spec` | `mvp-0.2-baseline.12` (also tag `v0.2.0`) | `bf1c78c596eef85e272c04a8a35661f814c23a40` | Normative wire, profiles and Markdown bindings |
| `openlfcp/server` | 0.3.2 (no new tag) | `138030ae6582197193cd4c041726683bcc206bef` | The code that was tested; the build the sibling locks pin |
| `openlfcp/server` | `main` | `b96721fdd104657fa1859c54ceb1ce7b4e69c285` | 0.3.2 plus `deploy/server.toml` limits only (`v0.3.2-2-gb96721f`) |
| `openlfcp/sdk-rs` | tag `v0.2.0` | `0a8239bc86f64d07fc0fcddca8d03d6ec0a9fd94` | Crate version 0.1.0 |
| `openlfcp/examples` | tag `v0.2.0` | `e7c3d2764a3a1cf17ca87a97e72bb0c235f1c7b0` | |
| `openlfcp/.github` | `main` (after tag `v0.2.0`) | `67aa1ce175a6cde9b7fb47e425556de66fa72794` | This task branches from here |
| `openlfcp/website` | `main` | `0141bd578da91a05391f3f31ac232ca9f89abea7` | openlfcp.org |

The pin set is the MVP 0.2 final candidate
[rc17](../release/rc17-manifest.json). The release close-out record is
[mvp-0.2-release-close.md](../release/mvp-0.2-release-close.md).

### Published plugin assets (0.4.0)

| File | sha256 |
| --- | --- |
| `main.js` | `c93f1a88352a7faf0ca800854ea8c70b3a2dafefdcfb8272513ebb2cd1ddc0e4` |
| `manifest.json` | `28df943d4903e29a91154c0b1562d78fadff49db76456bfbea261ddd16441f0f` |
| `styles.css` | `4cd5bf6b733ea5c3237649bfd3a461a298ede39802c6beb2c1c92b320ef4c2d1` |

Source: the release close-out, read from the GitHub Release. This task did
not rebuild `main.js`.

## Sibling locks and dependency pins

Each repository builds its siblings at the commits its lock files name,
not at their `HEAD`.

| Repository | Lock file | Pins |
| --- | --- | --- |
| obsidian | `spec.lock` | spec `mvp-0.2-baseline.12` = `bf1c78c596eef85e272c04a8a35661f814c23a40` |
| obsidian | `server.lock` | server `138030ae6582197193cd4c041726683bcc206bef` |
| obsidian | `package.json` | `@openlfcp/{client,core,crypto,shared-objects,storage,storage-idb,wire}` `0.2.0` exact |
| sdk-ts | `spec.lock` | spec `mvp-0.2-baseline.12` = `bf1c78c…` |
| sdk-ts | `server.lock` | server `138030a…` |
| server | `spec.lock` | spec `mvp-0.2-baseline.12` = `bf1c78c…` |
| server | `sdk-rs.lock` | sdk-rs `0a8239bc86f64d07fc0fcddca8d03d6ec0a9fd94` |
| sdk-rs | `spec.lock` | spec `mvp-0.2-baseline.12` = `bf1c78c…` |

### Package lockfiles

Each sha256 below was recomputed from the checkout at the commit above. It
equals the hash in
[mvp-0.2-release-evidence-rc17.json](../release/mvp-0.2-release-evidence-rc17.json).

| Repository | File | sha256 |
| --- | --- | --- |
| obsidian | `pnpm-lock.yaml` | `e183c40db1c66d034cc2a6048394c09dd218fff7be7a30f76a4c0aa720d3360e` |
| sdk-ts | `pnpm-lock.yaml` | `5c691aa8029e2858068e4e976246d1c783a6ad1932d985605f59a32dec8cbb84` |
| spec | `pnpm-lock.yaml` | `867d1a1684adf2a4793d7e57246636ce32387eaeb9a9a959124c955118b7ca64` |
| examples | `pnpm-lock.yaml` | `438f14bb4e05be822edcc9f6df0eb6e065178425ad70500fb11876ad742335d2` |
| sdk-rs | `Cargo.lock` | `1acfa2aac6d37579bcb370dd1554c6d64bf407d06f47a4a88a9c2fa2cab729de` |
| server | `Cargo.lock` | `046b6d132454d07229537f00f80586657f05e3e017f419aa68af7a5ea88f3eab` (same at `138030a` and `b96721f`) |

### Toolchain

| Tool | Declared | Used by the rc17 gate |
| --- | --- | --- |
| Node | `engines.node >=24` (obsidian, sdk-ts); CI `node-version: 24` | v24.4.0 |
| pnpm | `packageManager: pnpm@10.33.4` (obsidian, sdk-ts) | 10.34.1 |
| Rust | `rust-toolchain.toml`: `stable` + rustfmt, clippy (sdk-rs, server; no exact version) | rustc 1.99.0 |
| Ruby | spec `Gemfile.lock` | 4.0.5 |
| Python | `.github` scripts | 3.14.6 |

## Working tree state

Every checkout was on `origin/main` at the commit above when this audit
ran. No tracked file had changes. The untracked paths were only other
tasks' git worktrees under `.worktrees/` (shown as untracked in every
repository except obsidian, whose `.gitignore` lists them). Build outputs such as
obsidian `main.js` are covered by `.gitignore`. **There are no dirty
changes to separate from the baseline.**

## Host matrix

| Host | Covered by | Evidence |
| --- | --- | --- |
| Obsidian desktop **1.13.4** and **1.14.4**, Linux | Native harness (`pnpm native`, real Obsidian with WebdriverIO), run locally | 74/74 native specs at the candidate (G10); obsidian `docs/devel/testing/support-matrix-0.2.md` (themes, views, install and upgrade 0.3.4 and 0.4.0-beta.15 → 0.4.0) |
| Linux, macOS, Windows (CI runners) | Platform smoke workflow: vitest suite plus `test:security`, no GUI | Run 38636817316 on `ce0660a`: success on all three |
| macOS desktop, Obsidian 1.14.4, light theme, 1280×820 | The MVP 0.3 research walkthrough (one GUI vault, headless peer), on **beta.8** | `LFCP-MVP-0.3-BASELINE` package, ui-walkthrough; not repeated on 0.4.0 |
| Windows and macOS GUI | Not run natively | B12 (Windows manual smoke) and B13 (IME) were WAIVED in the go/no-go record |
| Tasks plugin | Native spec `tasks-plugin`; the research had Tasks 8.4.0 installed and **disabled** | Enabled-Tasks qualification is MVP 0.3 work (G03-F) |
| Mobile | Shared sections are read-only on mobile (a 0.4.0 documented limit) | Not certified; out of 0.3 scope |
| Native harness in GitHub CI | `native.yml` (3 OS × 2 Obsidian versions) has `workflow_dispatch` only | **No run recorded**, so the native results are local Linux only |

## Build and test commands

These are the gate commands that rc-verify ran for rc17 (all PASS). They are
listed so MVP 0.3 tasks use the same entry points.

| Repository | Commands |
| --- | --- |
| obsidian | `pnpm install --frozen-lockfile` · `pnpm run build` · `pnpm run lint` (exit code, not the tail) · `pnpm run typecheck` · `pnpm test` (needs `LFCP_SPEC_DIR` = a spec checkout at `spec.lock`; live tests also need `LFCP_REQUIRE_LIVE=1` and `LFCP_SERVER_BIN` built at `server.lock`) · `pnpm native` (real Obsidian, only when a task allows it) |
| sdk-ts | `pnpm install --frozen-lockfile` · `pnpm build` · `pnpm typecheck` · `pnpm lint` · `pnpm test` · `pnpm release:check` |
| spec | `pnpm install --frozen-lockfile` · `bundle check` · `./scripts/validate.sh` |
| sdk-rs | `cargo fmt --all --check` · `cargo clippy --workspace --all-targets --all-features -- -D warnings` · `cargo clippy --workspace --all-targets --no-default-features -- -D warnings` · `cargo test --workspace --all-features` · `cargo test --workspace --no-default-features` |
| server | `cargo fmt --all --check` · `cargo clippy --workspace --all-targets -- -D warnings` · `cargo test --workspace` |
| .github | `python3 scripts/doccheck.py` |

## CI results reused

| Repository | Commit | Workflow, run ID | Result |
| --- | --- | --- | --- |
| obsidian | `ce0660a` | CI 38636817368 (build, lint, typecheck, `pnpm test` at `spec.lock`) | success |
| obsidian | `ce0660a` | Platform smoke 38636817316 (ubuntu, macos, windows) | success |
| obsidian | `ce0660a` | Release 38635498492 (tag `0.4.0`); dry run 38618407889 | success |
| sdk-ts | `2a34beb` | CI 38615123485; Release 38616796278 (tag `v0.2.0`, npm) | success |
| spec | `bf1c78c` | CI 38365606327 | success |
| server | `138030a` | CI 38366695310 | success |
| server | `b96721f` | CI 38616386477 | success |
| sdk-rs | `0a8239b` | CI 38366689558 | success |
| examples | `e7c3d27` | CI 38618925062 | success |
| .github | `67aa1ce` | CI 38637343383 | success |

## What "baseline PASS" does and does not mean

The MVP 0.2 go/no-go record marks G01–G12 PASS. These items were waived or
did not run, and **MVP 0.3 must not count them as PASS**:

- The rc17 RELEASE-EVIDENCE record says `candidate_status: NOT_QUALIFIED`
  and `decision: NOT_REVIEWED`. rc-verify fills only the machine gates. The
  signed decision is the go/no-go record.
- The pilot (LFCP-02-075) was **WAIVED** for the release and runs after GA.
  There is no usability evidence for 0.2.
- B12 (Windows manual smoke) and B13 (IME) were **WAIVED**. On Windows and
  macOS only the headless Platform smoke ran.
- The immutable candidate set (`--assemble --repro`) was **WAIVED**. The
  artifacts were built in CI.
- The research's "everything passes" summary rested on one GUI vault, a
  headless peer, Tasks disabled and some inputs as CodeMirror
  transactions. Restart and claim interruption, structural and retained
  conflicts in the UI, the revoked member's own UI, and a held edit
  reaching the peer after repair were **NOT_RUN** there.

## Researched build (superseded)

The MVP 0.3 package and its baseline reports describe these commits:

| Repository | Researched | Full SHA | Now |
| --- | --- | --- | --- |
| obsidian | 0.4.0-beta.8 | `5c7f44bc72bda06d8bb725ee1ce5ec8eecdbe936` | 168 commits later at 0.4.0 (beta.9 to beta.20, then GA); 0.4.0-beta.16 and beta.18 have no tag |
| sdk-ts | 0.2.0-beta.6 | `d213de8e882a89aa66fee4e122c731d5eee061da` | 15 commits later at 0.2.0 |
| server | 0.3.1 | `814e913db156a1f2378ade79f907cd349fc654e9` | 0.3.2 (`138030a`), deploy limits `b96721f` |
| spec | `mvp-0.2-baseline.10` | `a3161f7a29f42462eac7e13c37e2d57db65866c1` | `mvp-0.2-baseline.12` |

What changed in that range and what it means for the 0.3 findings is in the
[gap register](gap-register.md).
