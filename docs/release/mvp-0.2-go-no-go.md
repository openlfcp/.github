# MVP 0.2 go / no-go record (draft)

**Status:** DRAFT (LFCP-02-077), unsigned. This is the record the release
owner signs to release MVP 0.2 or to hold it. It gathers the gate evidence,
the pilot outcome and the known issues into one decision. `<…>` marks what
the owner or a pending step settles. Nothing here is a release approval until
the final decision line is signed.

## Candidate under review

Final automated evidence: **rc14** (LFCP-02-073,
[candidate report](mvp-0.2-candidate-report.md),
[evidence JSON](mvp-0.2-release-evidence-rc14.json), pins
[rc14-manifest.json](rc14-manifest.json)). rc14's recorded status is
`NOT_QUALIFIED` / `decision: NOT_REVIEWED`: the automated gates are green for
one pinned commit set; the scope verdicts, the owner checks and the pilot are
people's to review here.

| Repository | rc14 commit | Version / tag |
| --- | --- | --- |
| spec | `bf1c78c` | mvp-0.2-baseline.12 |
| sdk-rs | `0a8239b` | — |
| server | `138030a` | 0.3.2 plus a pin-only commit |
| sdk-ts | `695cd08` | 0.2.0-beta.9 (npm, `beta`) |
| examples | `2345c56` | — |
| obsidian | `af16007` | plugin 0.4.0-beta.18, the 0.4.0 candidate |
| .github | `83e5f87` | — |

> **At release.** sdk-ts publishes `0.2.0` from rc14's code, and the plugin
> moves to `0.4.0` (its version commits and the `@openlfcp/*` 0.2.0 pin
> commit). These commits come after rc14: `<sdk-ts 0.2.0 commit>`,
> `<obsidian 0.4.0 commit>`.

## rc-verify gates (automated)

All eight rc-verify gates PASS for rc14 in one full run
(`report-20261014T082452Z`, Linux), `LFCP_REQUIRE_LIVE=1`: spec, .github,
docs, sdk-rs, server, sdk-ts, examples, obsidian. Pins consistent with no
lag. sdk-ts 2465/2465, obsidian 1638/1638, examples `--strict` 282 PASS,
2 N/A, all 0 skips. See the [candidate report](mvp-0.2-candidate-report.md).

## Scope gates G01–G12

Automated evidence is green (below); the **owner verdict** is each gate's to
set here as **PASS / OPEN / WAIVED** with a reason. Evidence is reviewed by
people — the evidence record's `decision` is `NOT_REVIEWED`.

| Gate | Name | Evidence | Owner verdict | Blocker |
| --- | --- | --- | --- | --- |
| G01 | Baseline | spec gate at baseline.12 (official vectors, 49 fixtures); SDK/server baseline tests ([candidate report](mvp-0.2-candidate-report.md#scope-gates-g01g12)) | `<PASS/OPEN/WAIVED>` | `<…>` |
| G02 | Contracts | both SDKs pass the vectors and cross-consume: examples `--strict` 282 PASS, 2 N/A ([compatibility matrix](../conformance/compatibility-matrix.md), [sections conformance](mvp-0.2-sdk-ts-sections-conformance.md)) | `<…>` | `<…>` |
| G03 | Onboarding | invitation/claim/handshake: sdk-ts live interop + examples E2E ([candidate report](mvp-0.2-candidate-report.md#scope-gates-g01g12)) | `<…>` | `<…>` |
| G04 | Content | Shared Objects + Shared Sections through baseline.12 (equal concurrent values agree; 94 vector cases): sdk-ts sections conformance, obsidian gate and native suite ([sections conformance](mvp-0.2-sdk-ts-sections-conformance.md)) | `<…>` | `<…>` |
| G05 | Identity | principal/actor derivation, control chain: sdk-ts, sdk-rs gates | `<…>` | `<…>` |
| G06 | Concurrency | convergence under faults: sdk-ts live chaos/access recovery (2465/2465); obsidian peer-structure property test (seeds 1–10000), its divergence detector, and a soak of three plugin peers (offline periods, server restarts, a removal) | `<…>` | `<…>` |
| G07 | Durability | storage, crash/restart, snapshots ([restore rehearsal](mvp-0.2-restore-rehearsal.json), [integrated recovery](mvp-0.2-integrated-recovery-qualification.md)); obsidian restart-mid-pass and stale-epoch re-apply (native) | `<…>` | `<…>` |
| G08 | Privacy | zero plaintext/keys on the wire: examples two-vault wire-tap; sdk-ts crypto | `<…>` | `<…>` |
| G09 | Access | grants, revocation, access recovery: sdk-ts live access recovery, examples; offline work across an access change re-applied (§19.1, §26.2) | `<…>` | `<…>` |
| G10 | UX | obsidian gate 1638/1638, 0 skips; native 70/70 on Obsidian 1.13.4 and 1.14.4; the desktop support matrix (obsidian `docs/devel/testing/support-matrix-0.2.md`) | `<…>` | `<…>` |
| G11 | Compatibility | compatibility matrix and the released 0.1.3 client ([two-vault](mvp-0.2-two-vault-qualification.md)); plugin upgrade-install: 0.3.4 and 0.4.0-beta.15 updated to the candidate | `<…>` | `<…>` |
| G12 | Release | rc-verify green, `release:check` (0.2.0-beta.9: pack+install+import), npm published under `beta`; this record | `<…>` | `<…>` |

**Owner checks not covered by rc-verify** (from
[mvp-0.2-owner-checklist.md](mvp-0.2-owner-checklist.md)):

- Obsidian native acceptance harness (LFCP-02-096): the plugin's native suite
  at the candidate (`af16007`), all 35 specs on Obsidian 1.13.4 and 1.14.4,
  70/70 runs green (69 on the first pass, one spec green on its rerun
  under load; run by the plugin author, Linux).
- Desktop matrix (LFCP-02-069), Linux, native: install and upgrade, themes
  and views, split view, the Tasks plugin, the clipboard (obsidian
  `docs/devel/testing/support-matrix-0.2.md`). Windows/macOS: Platform smoke
  in CI; manual smoke (B12) and IME (B13): `<…>`.
- Immutable candidate artifacts assembled (`--assemble --repro`): `<…>`.

## Pilot outcome (LFCP-02-075)

Against the frozen thresholds of
[MVP-0.2-TEST-AND-RELEASE-PLAN.md](../MVP-0.2-TEST-AND-RELEASE-PLAN.md) §13
and the pilot protocol (`docs/release/pilot/pilot-protocol.md`,
LFCP-02-103). Pilot: `<NOT RUN>`.

| Threshold | Target | Observed | Met? |
| --- | --- | --- | --- |
| End-to-end onboarding attempts | ≥10 | `<…>` | `<…>` |
| …without developer intervention | ≥8 | `<…>` | `<…>` |
| Pairs completing edit/reconnect | all | `<…>` | `<…>` |
| Comprehension checks correct | ≥8/10 | `<…>` | `<…>` |
| Unresolved blocker/major; private-content publication; data loss | none | `<…>` | `<…>` |

Report: the sanitised pilot report (`docs/release/pilot/pilot-report-template.md`)
when run. Unmet targets are explicit blockers (LFCP-02-076).

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
- **Project server quotas** (sync.openlfcp.org): 200 collaborations, 50 new/day
  per network, 256 MiB total, 128 MiB per collaboration `<B15 final values>`.

MVP 0.3 open decisions (not addressed in 0.2):

- **Rejoin after removal.** A removed member cannot rejoin; the plugin says
  so. Design note:
  [rejoin-after-removal.md](../devel/design/rejoin-after-removal.md).
- **MS14 freeze scope.** The frozen conflict scope for the Markdown-sections
  cases (MS14 "remote parent cycle": preserve last safe source, show a
  conflict); anything beyond the frozen set is MVP 0.3. `<owner confirms the
  exact frozen scope>`
- **Invitation expiry.** Time-based invitation expiry is server policy and is
  not enforced in 0.2 (WIRE-01: expiry MAY be enforced by servers; Resource
  state is ordered by Control Sequence, not timestamps). `<owner decision for
  0.3>`

## Final decision

The release owner records the decision for the final candidate:

- **Candidate:** rc14 ([rc14-manifest.json](rc14-manifest.json)), with sdk-ts 0.2.0 and Shared Tasks 0.4.0 at `<their release commits>`
- **Decision:** `<GO / NO-GO>`
- **Conditions or waivers:** `<…>`
- **Open blockers at decision:** `<none / list>`
- **Release owner:** `<name>`  **Date:** `<date>`

A GO authorises the public release steps
([owner checklist](mvp-0.2-owner-checklist.md) §6, and the tag commands in
`docs/release/mvp-0.2-tag-commands.md`, LFCP-02-093); close-out follows in
[mvp-0.2-release-close.md](mvp-0.2-release-close.md).
