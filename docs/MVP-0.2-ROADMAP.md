# MVP-0.2-ROADMAP

**Project:** OpenLFCP / Shared Tasks, by OpenLFCP  
**Date:** 2026-10-07  
**Status:** Reviewed, 2026-10-08 (owner-approved review of the planning batch); proposed delivery sequence, not a progress audit  
**Companions:** MVP-0.2-SCOPE.md; MVP-0.2-TEST-AND-RELEASE-PLAN.md; BACKLOG-MVP-0.2.md

## 1. Destination

MVP 0.2 is complete when two people can share a realistic task section in different private Obsidian notes, continue editing offline, safely recover after interruptions, and understand the sharing boundary, access and synchronization state.

The shared content includes Tasks, nested Tasks, supporting paragraphs, ordinary lists, ordering and future supported additions inside the section. The acceptance workload includes 100–200 Tasks with child content. The visual layer includes a persistent compact section indicator, quiet per-item pending/problem cues, tooltips and a details/access card. These are part of this milestone, not optional polish to move to a later release.

This roadmap does not reopen the agreed profile or invent a new product tier. A dedicated section Resource uses `org.openlfcp.shared-sections.v1`; legacy Task Resources remain supported. Explicit import creates new identities and an independent collaboration. Existing cryptography, authorization, restart safety and snapshots remain release obligations.

## 2. Starting evidence

Facts as of 2026-10-08, from the repositories, tags, CI and the npm registry.

| Area | What is established | What remains open |
| --- | --- | --- |
| MVP 0.1.0 release | Released 2026-10-06 as rc7: spec tag `mvp-0.1-baseline.8` (da3977f), sdk-rs c9132b1, server 896bbab, sdk-ts 4e1b02f, examples 943a6ad, obsidian e8e212f; tag `v0.1.0` in each repository; all eight `rc-verify.py` gates PASS (`release/rc-verification.md`, `release/rc7-manifest.json`) | Gates were run on macOS (Darwin arm64) only; CI covers the other systems |
| Server and public service | Server 0.2.0 (rc8, d6cd820) with abuse limits, quotas and memory bounds, image `ghcr.io/openlfcp/lfcp-server:0.2.0`; `wss://sync.openlfcp.org` in beta since 2026-10-06; `lfcp-admin` merged after 0.2.0 | Recovery after server data loss (ADR 0008, LFCP-02-088); backup retention and a restore test of the public server |
| Libraries | `@openlfcp/*` 0.1.1 on npm (`latest`); sdk-rs by git tag only (`publish = false`) | Section profile in both SDKs (E03, E04) |
| Plugin | Shared Tasks 0.3.1 (`shared-tasks`) listed in the Obsidian community plugins after the directory review of 2026-10-07; releases built by CI from bare `X.Y.Z` tags with attested assets; SDK taken from npm at exact versions; `minAppVersion` 1.13.1; available on mobile (`isDesktopOnly: false`) | A beta channel that does not update catalog users (LFCP-02-094); 0.3.1 spends a one-time invitation before checking the Data Profile (LFCP-02-086/087) |
| CI and platforms | CI green on every repository; the plugin's automated platform smoke runs on macOS, Windows and Linux; the TS↔Rust conformance run and live interop against the Rust server | Native Obsidian checks exist only as a manual macOS run (LFCP-02-096; POST-002) |
| Security | Pre-release review: H1–H7 fixed (H5, H6 in server 0.2.0); exact admission limits in the spec (§11.1, §11.2, §30, §31) | M10, plaintext local checkpoints (LFCP-02-098); POST-001, actor/sequence collisions (LFCP-02-089); POST-007, Snapshot publishing by the plugin (LFCP-02-097) |
| Protocol facts | An unknown Data Profile is verified and kept, never decrypted (sdk-ts `PROFILE_UNSUPPORTED`); the server is profile-agnostic; ACK reports durable persistence | An ACK does not survive a server restore from backup until ADR 0008 ships |
| Section contracts | Scope, architecture, profile, Markdown bindings and compatibility drafts, settled by the review decisions (`BACKLOG-MVP-0.2.md` §3) | Publication with LFCP-02-007/083 and the baseline `mvp-0.2-baseline.N` |
| Model corpus | 28 generated Automerge cases; the review reproduced them byte for byte | Regeneration on Automerge 3.5.0 (decision P6); production SDK conformance and Rust interoperability |
| Markdown corpus | 29 static/lexical fixtures; reproduced byte for byte | Actual editor transactions, clipboard, Tasks integration and external-file behavior |
| Obsidian design | Architecture, UX and indicator contracts; UX01–UX18, SI01–SI20 | Implementation and execution of those 38 acceptance scenarios |
| Delivery planning | This roadmap, the test and release plan, and `BACKLOG-MVP-0.2.md` (105 tasks, waves W0–W8) | Execution |

A document or fixture being present is not a completed product gate. Use the current source files, not superseded backlog patches. This roadmap introduces milestone labels M02-0 through M02-6 solely for 0.2 planning; it does not renumber LFCP-001… items from MVP 0.1.

## 3. Milestones and exit evidence

| Milestone | Observable outcome | Main outputs | Exit evidence |
| --- | --- | --- | --- |
| M02-0 — Baseline | We know what is built and which inherited obligations remain | Component/version manifest, repository map, baseline defect list, actual ACK/catch-up semantics | G01; no unclassified security/durability gap; exact test commands recorded |
| M02-1 — Tested contracts | Section behavior is implementable consistently across SDKs and Markdown | Pinned specs/corpus, TS/Rust model adapters, parser/reconciliation interface contracts | G02; model/negative/interop checks; ambiguities resolved in canonical drafts and fixtures |
| M02-2 — Safe local sections | One vault can edit a complete section and project it elsewhere without losing identities or private text | Parser, source maps, journal, guarded projection, basic attention UI | Local portions of G04–G08; restart/undo/boundary tests on real editor integration |
| M02-3 — Secure two-vault slice | Share, invite, join, edit and reconnect work through the actual server | End-to-end section flow and legacy coexistence | G03–G09 secure path; client/server restart, snapshot/cutoff and two-vault evidence |
| M02-4 — Everyday UX | Users understand access and state and can recover from ordinary failures | Indicators, tooltips/card, recovery actions, copy/detach/import, compatibility behavior | G10–G11; UX01–UX18 and SI01–SI20; all three editor modes |
| M02-5 — Release candidate | One reproducible build set passes the supported desktop and load matrix | Signed-off test evidence, limits, release notes, pilot build | G01–G11 revalidated on exact candidate; technical portions of G12 and rollback rehearsal |
| M02-6 — Pilot and release | Real pairs can use the section workflow; release claims match evidence | Pilot findings/fixes, final manifest, distribution and accurate public docs | Full G12; no unresolved blocking defect; all G01–G12 satisfied |

G01–G12 retain their meanings from MVP-0.2-SCOPE. The test/release companion gives the crosswalk and pass criteria. Internal development builds may be incomplete; they must be labeled as such and cannot claim the milestone release is ready.

## 4. Dependency order and parallel preparation

The critical path is baseline → tested contracts → safe local reconciliation → secure two-vault behavior → real UX/recovery → candidate qualification → pilot/release.

Useful overlap reduces waiting without bypassing dependencies:

- During baseline, review UX flows and prepare acceptance harnesses against frozen sample facts.
- Once a profile draft is pinned, TypeScript and Rust model work can progress independently against the same corpus; compare authored changes in both directions before freezing that contract.
- Parser/fixture work and server opacity/limit/ACK audits can proceed alongside SDK model work. Editor writes wait for agreed intent/receipt contracts.
- The pure indicator reducer and visual prototypes can use explicit mock evidence early. They must later be bound to actual durable/ACK/control facts; mock screenshots do not close G10.
- Release documentation structure and examples can be prepared early. Public capability claims and installation requirements wait for verified release builds.

Do not put every future feature on the critical path. Do not postpone source privacy or crash ordering until after visual polish. A minimal attention indicator is required as soon as the editor can encounter unsafe source/model state; full visual refinement follows at M02-4.

## 5. Demonstrations at each review

| Milestone | Short review demonstration |
| --- | --- |
| M02-0 | Show exact component revisions, one inherited secure Task flow, and a classified list of any missing evidence |
| M02-1 | TS creates a nested section, Rust edits it, TS consumes it; show a concurrent move conflict and retained deleted-child edit |
| M02-2 | Edit a 200-Task section; add child text; move a subtree; restart; damage a marker next to a private canary and show no publication |
| M02-3 | Two clean vaults join through one invite; partition, edit both, reconnect, resolve conflict; restart server and resume via snapshot plus tail |
| M02-4 | Show one/two-check semantics, offline access staleness, pending revocation, clean plain/rich copy, detach of only one projection and keyboard recovery |
| M02-5 | Replay exact build/test matrix and a safe rollback to a section-capable build; show measured performance and declared limits |
| M02-6 | Present pair-level pilot outcomes and remaining nonblocking issues; release only the claims supported by evidence |

A demonstration supplements automated evidence; it does not replace security, concurrency, crash or cross-language checks.

## 6. Scope priorities and tradeoffs

The required core consists of secure section creation/join; full supported section content; automatic additions; identity-preserving moves; safe local/remote reconciliation; offline durability; explicit conflicts; accurate access/status; clipboard purity; legacy coexistence and explicit import; desktop qualification.

If delivery is slow, simplify the presentation before changing semantics:

| Can remain simple | Must remain complete |
| --- | --- |
| One compact card instead of a new dashboard | Effective access, pending invitations and honest freshness |
| Quiet row indicators instead of per-row healthy badges | Section sharing remains visible and attention remains reachable |
| Native editing/cut/paste with explicit ambiguity diagnostics | Identity and text are never guessed away or silently discarded |
| Plain but accessible conflict forms | All supported alternatives and retained work are available |
| One tested primary sync endpoint | Existing secure transport and durable recovery |

A scope reduction affecting an agreed gate requires an explicit scope revision before claiming 0.2 completion. A schedule estimate is not permission to waive privacy, data retention or authorization.

Still excluded: federation/P2P, active-active hosting, ownership transfer, server migration, presence/read receipts, per-node ACL, threaded discussions, attachment transfer, arbitrary full-document Markdown, new recurrence, mobile certification and new editor products.

## 7. Risk register and early resolution

| Risk | First detection point | Required response |
| --- | --- | --- |
| Old clients mutate unknown profiles | M02-0/M02-1 | The SDK keeps unknown profiles undecrypted, but 0.3.1 spends the invitation first: sdk-ts `acceptInvitation` option and plugin 0.3.2 before section onboarding (LFCP-02-086/087) |
| CRDT Text/scalar or placement behavior differs across SDKs | M02-1 | Correct canonical draft/implementation and add independent exchange cases |
| Boundary repair exposes private text | M02-2 | Block publication, retain source; regression canary tests; release blocker |
| Crash duplicates intent or reuses actor sequence | M02-2/M02-3 | Durable correlation and exact-object replay; fault-injection proof |
| ACK does not prove assumed persistence | M02-0 | Document real semantics; show uncertainty until adequate evidence; do not invent wire behavior |
| Native undo/external edits overwrite newer state | M02-2 | Base-aware reconciliation and explicit recovery; test races |
| Rich clipboard includes indicators/cards | M02-4, spike earlier | Tested selection serializer and clean UI ownership; CSS alone insufficient |
| 200-Task section becomes slow or noisy | Instrument at M02-2; qualify M02-5 | Incremental work/viewport rendering; measure against frozen budgets |
| Upgrade/downgrade loses section or pending state | M02-3/M02-4 | Journaled coexistence/import and safe unsupported-version behavior |
| Demo server changes disrupt existing users | M02-5 | Stage and qualify; explicit deployment/restore plan; preserve legacy path |

## 8. Schedule and ownership

This roadmap intentionally uses dependency-based milestones instead of invented calendar promises. At M02-0, record the named technical owner, product owner, QA/release owner, available implementer capacity and measured baseline gaps. Then estimate the critical path using actual work remaining and integration capacity.

Suggested responsibility split: product owner accepts user journeys and any scope/budget changes; technical owner owns cross-repository contracts and baseline decisions; component owners own changes and tests; release owner assembles evidence and coordinates qualification. These are roles to assign, not assumptions that specific people or teams already exist.

Track each milestone as NOT_STARTED, IN_PROGRESS, BLOCKED or EVIDENCE_COMPLETE. An agent's completed PR is not enough to change a cross-repository milestone to EVIDENCE_COMPLETE. Link the exact integrating build and required results.

## 9. Beyond 0.2

The immediate post-release step is a maintenance/learning cycle: fix observed reliability and onboarding defects, inspect limits and pilot feedback, and decide the next highest-value problem. Do not automatically expand to every previously discussed protocol capability.

Possible later tracks include broader Markdown support, identity/device provisioning, another editor, or routing/ownership operations. Choose a track using user evidence, interoperability cost and security/recovery requirements. These are options, not commitments for an already-approved 0.3 scope.

## 10. Next planning artifact

The detailed backlog is `BACKLOG-MVP-0.2.md`, with its execution map. It keeps legacy issue identities, adds the review tasks 083–105 and the W0 follow-up 106, and sets the waves W0–W8; wave W0 ships the 0.1.x sustaining set (spec `mvp-0.1-baseline.9`, server 0.3.0, sdk-ts 0.1.3, plugin 0.3.2) before 0.2 work starts. sdk-ts 0.1.2 went to npm without build output and is deprecated; 0.1.3 is the same code, published by CI through npm Trusted Publishing.

Release versions (decision V1): Shared Tasks 0.4.0 (betas `0.4.0-beta.N` through BRAT), `@openlfcp/*` 0.2.0 (`0.2.0-rc.N` on npm `next` before), sdk-rs and examples `v0.2.0`, spec `mvp-0.2-baseline.N`; the server gets a release only if it changes. Release notes call the set "MVP 0.2" and list each component's version.
