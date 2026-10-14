# MVP 0.2 go / no-go record (draft)

**Status:** DRAFT (LFCP-02-077), owner decisions of 2026-10-14 recorded;
awaiting the owner's signature and date. This is the record the release
owner signs to release MVP 0.2 or to hold it. It gathers the gate evidence,
the pilot outcome and the known issues into one decision. `<…>` marks what
the owner or a pending step settles. Nothing here is a release approval until
the final decision line is signed.

## Candidate under review

Final candidate: **rc17** (LFCP-02-073), pins [rc17-manifest.json](rc17-manifest.json),
evidence [mvp-0.2-release-evidence-rc17.json](mvp-0.2-release-evidence-rc17.json). rc17 carries the release
versions: sdk-ts `@openlfcp/*` **0.2.0** (npm, `latest`) and Shared Tasks
**0.4.0**. The previous candidate, rc16
([rc-verification.md](rc-verification.md),
[evidence JSON](mvp-0.2-release-evidence-rc16.json),
[rc16-manifest.json](rc16-manifest.json)), had the same code at
0.2.0-beta.10 and 0.4.0-beta.20.

| Repository | rc17 commit | Version / tag |
| --- | --- | --- |
| spec | `bf1c78c` | mvp-0.2-baseline.12 |
| sdk-rs | `0a8239b` | — |
| server | `138030a` | 0.3.2 plus a pin-only commit (`main` `b96721f` adds only the deploy configuration) |
| sdk-ts | `2a34beb` | 0.2.0 (npm, `latest`), tag `v0.2.0` |
| examples | `e7c3d27` | — |
| obsidian | `ce0660a` | Shared Tasks 0.4.0 (branch `rw/plugin-0.4.0`) |
| .github | `1be6b96` | — |

## rc-verify gates (automated)

rc17 passed all eight rc-verify gates on the first full run
(`report-20261014T191116Z`, Darwin arm64), `LFCP_REQUIRE_LIVE=1`: spec,
.github, docs, sdk-rs, server, sdk-ts, examples, obsidian. Pins consistent
(server `main` is one deploy-configuration commit past the pin). sdk-ts
2470/2470, obsidian 1652/1652, both 0 skips; `release:check` at 0.2.0 under
`latest`; examples `--strict` 282 PASS, 2 N/A. rc16 had passed them too
(`report-20261014T162853Z`, Linux). See the
[candidate report](mvp-0.2-candidate-report.md).

## Scope gates G01–G12

Automated evidence is green (below). **Owner verdicts, 2026-10-14: all
twelve gates PASS**, no blockers.

| Gate | Name | Evidence | Owner verdict | Blocker |
| --- | --- | --- | --- | --- |
| G01 | Baseline | spec gate at baseline.12 (official vectors, 49 fixtures); SDK/server baseline tests ([candidate report](mvp-0.2-candidate-report.md#scope-gates-g01g12)) | PASS | none |
| G02 | Contracts | both SDKs pass the vectors and cross-consume: examples `--strict` 282 PASS, 2 N/A ([compatibility matrix](../conformance/compatibility-matrix.md), [sections conformance](mvp-0.2-sdk-ts-sections-conformance.md)) | PASS | none |
| G03 | Onboarding | invitation/claim/handshake: sdk-ts live interop + examples E2E ([candidate report](mvp-0.2-candidate-report.md#scope-gates-g01g12)) | PASS | none |
| G04 | Content | Shared Objects + Shared Sections through baseline.12 (equal concurrent values agree; 94 vector cases): sdk-ts sections conformance, obsidian gate and native suite ([sections conformance](mvp-0.2-sdk-ts-sections-conformance.md)) | PASS | none |
| G05 | Identity | principal/actor derivation, control chain: sdk-ts, sdk-rs gates | PASS | none |
| G06 | Concurrency | convergence under faults: sdk-ts live chaos/access recovery (2470/2470); obsidian peer-structure property test (seeds 1–10000), its divergence detector, and a soak of three plugin peers (offline periods, server restarts, a removal) | PASS | none |
| G07 | Durability | storage, crash/restart, snapshots ([restore rehearsal](mvp-0.2-restore-rehearsal.json), [integrated recovery](mvp-0.2-integrated-recovery-qualification.md)); obsidian restart-mid-pass and stale-epoch re-apply (native) | PASS | none |
| G08 | Privacy | zero plaintext/keys on the wire: examples two-vault wire-tap; sdk-ts crypto | PASS | none |
| G09 | Access | grants, revocation, access recovery: sdk-ts live access recovery, examples; offline work across an access change re-applied (§19.1, §26.2) | PASS | none |
| G10 | UX | obsidian gate 1652/1652, 0 skips; native 74/74 on Obsidian 1.13.4 and 1.14.4; the desktop support matrix (obsidian `docs/devel/testing/support-matrix-0.2.md`) | PASS — Windows and macOS checked by Platform smoke in CI only | none |
| G11 | Compatibility | compatibility matrix and the released 0.1.3 client ([two-vault](mvp-0.2-two-vault-qualification.md)); plugin upgrade-install: 0.3.4 and 0.4.0-beta.15 updated to the candidate | PASS | none |
| G12 | Release | rc-verify green, `release:check` (0.2.0-beta.10: pack+install+import), npm published under `beta`; this record | PASS | none |

**Owner checks not covered by rc-verify** (from
[mvp-0.2-owner-checklist.md](mvp-0.2-owner-checklist.md)):

- Manual check in two Obsidian vaults on 0.4.0-beta.20, steps 0–13
  (owner): **PASS**.
- Obsidian native acceptance harness (LFCP-02-096): the plugin's native suite
  at the candidate (`4ce8e77`), all 37 specs on Obsidian 1.13.4 and 1.14.4,
  74/74 runs green on the first pass (run by the plugin author, Linux).
- Desktop matrix (LFCP-02-069), Linux, native: install and upgrade, themes
  and views, split view, the Tasks plugin, the clipboard (obsidian
  `docs/devel/testing/support-matrix-0.2.md`). Windows/macOS: Platform smoke
  in CI.
- B12 (manual smoke on Windows) and B13 (IME): **WAIVED** — Platform smoke
  is green in CI on all three operating systems.
- Immutable candidate artifacts assembled (`--assemble --repro`): `<…>`.

## Pilot outcome (LFCP-02-075)

Against the frozen thresholds of
[MVP-0.2-TEST-AND-RELEASE-PLAN.md](../MVP-0.2-TEST-AND-RELEASE-PLAN.md) §13
and the pilot protocol (`docs/release/pilot/pilot-protocol.md`,
LFCP-02-103). Pilot: **WAIVED for the release** (owner, 2026-10-14). It
runs about two weeks after the release, on the GA build Shared Tasks 0.4.0,
with employees of the owner's company. The thresholds do not change: at
least 10 onboarding attempts, so 5 pairs. Its results feed 0.2.x and
MVP 0.3; the table is filled then.

| Threshold | Target | Observed | Met? |
| --- | --- | --- | --- |
| End-to-end onboarding attempts | ≥10 | `<…>` | `<…>` |
| …without developer intervention | ≥8 | `<…>` | `<…>` |
| Pairs completing edit/reconnect | all | `<…>` | `<…>` |
| Comprehension checks correct | ≥8/10 | `<…>` | `<…>` |
| Unresolved blocker/major; private-content publication; data loss | none | `<…>` | `<…>` |

Report: the sanitised pilot report (`docs/release/pilot/pilot-report-template.md`)
when run. Unmet targets become blockers for 0.2.x / MVP 0.3, not for this
release.

## Known issues carried into GA

Accepted as documented limits of 0.2, not blockers unless the owner says so.

From the [0.4.0 notes](https://github.com/openlfcp/obsidian/blob/main/docs/releases/0.4.0.md)
limits and the 0.4.0-beta "Good to know":

- **Size / performance.** ~200 tasks per section is the qualified size; a much
  larger section (2,000) works but blocks the editor for seconds per edit;
  performance measured on macOS only (Windows/Linux functional, not
  performance-qualified).
- **Long history.** A section slows after many thousands of edits; past
  ~200,000 characters the card suggests a new section (no automatic action;
  history growth policy deferred, LFCP-02-112).
- **Mobile.** Shared sections are read-only on mobile.
- **Project server limits** (sync.openlfcp.org, B15, the deployed
  configuration): 200 collaborations per identity, 50 new/day per network
  address, 256 MiB per identity, 128 MiB per collaboration; 3 GiB of storage in all,
  keeping at least 2 GiB of disk free; 8 open connections and 20 new
  connections a minute per network address; 50 messages a second per
  connection (bursts of 200); messages up to 1 MiB.

MVP 0.3 open decisions (not addressed in 0.2; the owner decides them for
0.3):

- **Rejoin after removal.** A removed member cannot rejoin; the plugin says
  so. Design note:
  [rejoin-after-removal.md](../devel/design/rejoin-after-removal.md).
- **MS14 freeze scope.** The frozen conflict scope for the Markdown-sections
  cases (MS14 "remote parent cycle": preserve last safe source, show a
  conflict); anything beyond the frozen set is MVP 0.3.
- **Invitation expiry.** Time-based invitation expiry is server policy and is
  not enforced in 0.2 (WIRE-01: expiry MAY be enforced by servers; Resource
  state is ordered by Control Sequence, not timestamps).

## Final decision

The release owner records the decision for the final candidate:

- **Candidate:** rc17 ([rc17-manifest.json](rc17-manifest.json)), with sdk-ts `@openlfcp/*` 0.2.0 and Shared Tasks 0.4.0
- **Decision:** **GO** (owner, 2026-10-14), pending the signature below
- **Conditions or waivers:** B12 and B13 WAIVED (Platform smoke green in CI on three operating systems); the pilot (LFCP-02-075) WAIVED for the release, run after it on 0.4.0; G10 PASS with Windows and macOS covered by Platform smoke only
- **Open blockers at decision:** none
- **Release owner:** `<name>`  **Date:** `<date>`

A GO authorises the public release steps
([owner checklist](mvp-0.2-owner-checklist.md) §6, and the tag commands in
`docs/release/mvp-0.2-tag-commands.md`, LFCP-02-093); close-out follows in
[mvp-0.2-release-close.md](mvp-0.2-release-close.md).
