# MVP 0.2 baseline inventory (LFCP-02-001)

**Status:** Evidence for LFCP-02-001, 2026-10-08. Read-only: nothing was
pushed, published or deployed to collect it.
**Manifest:** [mvp-0.2-baseline-manifest.json](mvp-0.2-baseline-manifest.json),
written by `scripts/rc-verify.py --from-heads --consistency-only --with
website` (rc-verify of LFCP-02-102) from the local committed HEADs.

The base of MVP 0.2 is the W0 sustaining release set: spec
`mvp-0.1-baseline.9`, server 0.3.0, sdk-ts 0.1.3 and Shared Tasks 0.3.2,
verified together as rc9 ([rc9-manifest.json](rc9-manifest.json),
[rc-verification.md](rc-verification.md)). Commits after it on `main` are
the start of MVP 0.2 work.

## 1. Components

| Component | Canonical repository | Base commit (manifest) | Version | Lockfile (SHA-256) | Released artifacts |
| --- | --- | --- | --- | --- | --- |
| spec | github.com/openlfcp/spec | 1e87206 | tag `mvp-0.1-baseline.9` (f42533c); later commits carry the 0.2 drafts | pnpm-lock.yaml 867d1a16… | tags `v0.1.0`, `mvp-0.1-baseline.1`…`.9` |
| sdk-rs | github.com/openlfcp/sdk-rs | 259a688 | 0.1.0 (crate `lfcp`, `publish = false`) | Cargo.lock 1acfa2aa… | tag `v0.1.0`; v0.2.0 comes with MVP 0.2 |
| server | github.com/openlfcp/server | 09c9132 | 0.3.0 | Cargo.lock 09938460… | tags `v0.1.0`, `v0.2.0`, `v0.3.0`; images `ghcr.io/openlfcp/lfcp-server:0.2.0` (sha256:a30e0151…f8207) and `:0.3.0` (sha256:a428fb83…eaa01) |
| sdk-ts | github.com/openlfcp/sdk-ts | e9cdb43 (0.1.3 is 7e9462f) | 0.1.3 | pnpm-lock.yaml 9e30866e… | npm `@openlfcp/*` 0.1.1 on `latest` and `next` (`@openlfcp/core` integrity sha512-GJIdgrKq…, 17 files; `@openlfcp/client` sha512-VLLbRXXQ…, 29 files); 0.1.2 deprecated (no build output); 0.1.3 waits for the first CI release |
| examples | github.com/openlfcp/examples | 892be03 | private root package | pnpm-lock.yaml e33ed197… | tag `v0.1.0` |
| obsidian | github.com/openlfcp/obsidian | 3142eb2 (uncommitted work in the checkout is not part of it) | 0.3.1 released; 0.3.2 in preparation | pnpm-lock.yaml b22656ba… | GitHub release 0.3.1 (2026-10-07): `main.js` sha256:f8e534b6…74d41, `manifest.json` sha256:55feb7e8…bf88e, `styles.css` sha256:2d5c26e6…17141, with attestations; listed in the Obsidian community plugins |
| .github | github.com/openlfcp/.github | 26e09db | — | — | project documentation, organization profile `profile/README.md` |
| website | github.com/openlfcp/website (private) | f6be919 | — | none (no build step) | <https://openlfcp.org>, Cloudflare Pages (website `README.md`, "Deploy") |

Owner of every component: the project owner. The modules of MVP 0.2
(worker A: sdk-ts, examples, release tooling; worker B: spec, sdk-rs,
server; worker C: obsidian) are in
[BACKLOG-MVP-0.2.md](../BACKLOG-MVP-0.2.md) §4.

## 2. Build and test commands

The release gates are those of rc-verify ([rc-verification.md](rc-verification.md),
"What it does"), run from worktrees at the manifest's commits:

| Component | Commands |
| --- | --- |
| spec | `pnpm install --frozen-lockfile`, `bundle check`, `scripts/validate.sh` |
| .github | `scripts/validate.sh`; docs: `scripts/doccheck.py` over the seven checkouts |
| sdk-rs | `cargo fmt --check`; `clippy -D warnings` and `test`, each with `--all-features` and `--no-default-features` |
| server | `cargo fmt --check`, `clippy -D warnings`, `cargo test` |
| sdk-ts | `pnpm install --frozen-lockfile`, `build`, `typecheck`, `lint`, `test` (live interop against the server at `server.lock`; the engine-trap project last), `release:check` |
| examples | `pnpm install --frozen-lockfile`, `build`, `typecheck`, `lint`, `test`, `node conformance/dist/run.js --strict` |
| obsidian | `pnpm install --frozen-lockfile`, `build`, `lint`, `typecheck`, `vitest run` (no skips); native harness `pnpm run native` (optional gate) |
| website | `scripts/website-check.py` (optional gate) |

Every gate runs with `LFCP_REQUIRE_LIVE=1`, so live tests cannot pass by
skipping. Each repository also has CI on push (`.github/workflows/ci.yml`;
obsidian adds `platform-smoke.yml` on three systems, server `image.yml`).

Release paths:

| Component | Path |
| --- | --- |
| sdk-ts | a `vX.Y.Z` tag runs `release.yml`: npm Trusted Publishing after an approval in the environment `npm-publish` ([npm-publish-checklist.md](npm-publish-checklist.md), "Trusted publishing"); the manual path is the fallback |
| server | a `vX.Y.Z` tag runs `image.yml`: `ghcr.io/openlfcp/lfcp-server:X.Y.Z` |
| obsidian | a bare `X.Y.Z` tag runs `release.yml`: a GitHub release with attested assets; the catalog follows `manifest.json` on `main`; betas through BRAT pre-releases (LFCP-02-094) |
| spec, sdk-rs, examples | tags only |
| .github, website | push to `main` (the website deploys from it) |

## 3. Website, organization profile and demo deployment

| Source | Where | Missing access or metadata |
| --- | --- | --- |
| Website | `openlfcp/website` (private), static, Cloudflare Pages; <https://openlfcp.org> answers 200 | the Cloudflare project is the owner's |
| Organization profile | `openlfcp/.github`, `profile/README.md` | none |
| Demo sync server | `wss://sync.openlfcp.org/v1/ws`, beta since 2026-10-06, on the owner's server stack ([operations/sync-server-runbook.md](../operations/sync-server-runbook.md)); deployment recipe in server `deploy/` | **the version it runs**: `/health` answers `{"status":"ok"}` and names none; whether 0.3.0 is deployed is known only to the owner. Backup retention and a restore test: LAUNCH-003 (a), (b) |

## 4. Identities and superseded documents

The MVP 0.1 task IDs (LFCP-001…072, POST-, LAUNCH-, NEXT-) stay as they
are in [BACKLOG-MVP-0.1.md](../BACKLOG-MVP-0.1.md); MVP 0.2 uses
LFCP-02-NNN.

| Superseded | By |
| --- | --- |
| BACKLOG-MVP-0.1.md as the current backlog | [BACKLOG-MVP-0.2.md](../BACKLOG-MVP-0.2.md) (AGENT-OPERATING-GUIDE §4.6) |
| NEXT-001 | ADR 0009, the shared sections profile (spec `adr/`) |
| The planning batch's specification drafts and its spec snapshot (spec 8f1cc79) | spec `profiles/SHARED-SECTIONS-PROFILE-01.md`, `integration/MARKDOWN-SECTIONS-01.md` and `test-vectors/shared-sections-01/`, after `mvp-0.1-baseline.9` (normative changes listed in the manifest run, before a `mvp-0.2-baseline.N` tag) |
| The planning batch's agent prompts | the task cards with the brief rules of BACKLOG-MVP-0.2.md §5 |
| "SDK alignment pending" for H1, H7, M1 in [security-review-mvp-0.1.md](security-review-mvp-0.1.md) | shipped: [mvp-0.1-release-notes.md](mvp-0.1-release-notes.md) (sdk-ts 68ce58d, af6e6f1, 9b61644; sdk-rs 50cb6bf, b1d08bd) |
| npm `@openlfcp/*` 0.1.2 | 0.1.3, the same code ([npm-publish-checklist.md](npm-publish-checklist.md)) |

## 5. Pins at the base

All pins agree with the manifest except:

- **obsidian** `spec.lock`, `server.lock` and the `@openlfcp/*` 0.1.1
  dependencies: they move with Shared Tasks 0.3.2 to baseline.9, server
  09c9132 and npm 0.1.3 (LFCP-02-087);
- **examples** `conformance/pins.json` `sdk_ts` names 7e9462f (0.1.3);
  sdk-ts e9cdb43 after it changes tests only;
- **spec** has normative commits after `mvp-0.1-baseline.9`: the MVP 0.2
  drafts and section corpus, to be tagged `mvp-0.2-baseline.N`
  (LFCP-02-090). The implementations stay on baseline.9 until then.
