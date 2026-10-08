# MVP-0.2-TEST-AND-RELEASE-PLAN

**Project:** OpenLFCP / Shared Tasks, by OpenLFCP  
**Date:** 2026-10-07  
**Status:** Reviewed, 2026-10-08 (owner-approved review of the planning batch); acceptance requirements and proposed qualification budgets  
**Companions:** MVP-0.2-SCOPE.md; MVP-0.2-ROADMAP.md; BACKLOG-MVP-0.2.md. The test-vector and fixture documents named below are to be published with LFCP-02-007/083

## 1. Release decision

Release MVP 0.2 only when an exact candidate build set satisfies G01–G12 from MVP-0.2-SCOPE, retains the secure 0.1 subset, and completes the declared desktop/pilot checks. A green reference generator, a successful demo or a merged PR alone is insufficient.

This document is a test plan. No product tests or benchmarks were executed while writing it. Numerical budgets and pilot thresholds below are proposed initial release criteria, not measured performance or statements that the user has already approved a calendar commitment. Freeze their reviewed values at M02-0/M02-1 before candidate qualification; record any later adjustment with rationale and affected scope. Never adjust a threshold silently to turn a failing result green.

Test statuses: NOT_RUN, PASS, FAIL, BLOCKED or NOT_APPLICABLE. NOT_APPLICABLE requires a documented reason consistent with scope. Missing evidence is not PASS. A must-have scope gate cannot become NOT_APPLICABLE merely because implementation is late.

## 2. Evidence baseline

Existing planning-batch evidence (reproduced byte for byte by the review): 28 JavaScript Automerge scenarios replayed from actual stored bytes, reverse delivery/duplicates, snapshot continuation and reproducible JSON generation; 29 static/lexical Markdown fixtures, including three narrow projection smoke operations. This evidence is useful but does not prove production SDK, independent Rust, Wire security or native Obsidian behavior.

Required independent execution:

- Production sdk-ts consumes the section corpus through its own model/validator.
- sdk-rs consumes it and authors changes that sdk-ts accepts; sdk-ts authors changes that sdk-rs accepts.
- The actual parser/reconciler consumes Markdown fixtures through an implementation adapter.
- Real Obsidian Source, Live Preview and Reading surfaces exercise editor events, selection, undo and clipboard.
- The actual client/server secure flow exercises encrypted/signed section payloads, control, keys, restart and snapshots.

Keep deterministic vector hashes distinct from logical interoperability. Supplied byte records must match their hashes; independently authored equivalent CRDT history need not have byte-identical save images. Preserve reference expected values unless a reviewed specification correction requires a new corpus.

## 3. Environments and version matrix

Freeze exact OS, hardware, runtime, Obsidian, Tasks, plugin, SDK, server and dependency versions in the release record. Filling them from actual builds is an M02-0 prerequisite (LFCP-02-005), not a reason to invent version numbers here.

Review decision V4 (2026-10-08): native editor checks run on macOS; the CI harness (LFCP-02-096) runs on macOS, Windows and Linux; Windows and Linux also get a manual smoke. The performance budgets of section 10 are measured on macOS only; Windows and Linux are claimed "functional, not performance-qualified".

| Environment ID | Planned target | Required use |
| --- | --- | --- |
| E-MAC-ARM | macOS on Apple Silicon, exact supported OS/model recorded | Native editor, keyboard/clipboard, upgrade/recovery, performance |
| E-WIN-X64 | Windows on x64, exact supported OS/model recorded | Same native/editor/upgrade/performance obligations |
| E-LINUX-X64 | Linux desktop on x64, exact distribution/display system recorded | Same obligations; clipboard behavior on the tested display stack |
| E-HEADLESS | Pinned Node + Rust toolchains in reproducible CI | Model, parser, independent exchange, fault injection and security tests |
| E-SERVER | Linux reference-server process/container with persistent volume | Secure integration, crash/restart, limits and restore rehearsal |

The initial claim is the tested desktop matrix. Other CPU architectures, Linux display stacks, OS versions and mobile are not certified by implication. If the existing 0.1 release promises a broader supported matrix, carry its regression obligations forward or explicitly resolve the release-claim change before qualification.

Choose at least one lower-capacity machine/profile (4 CPU cores, 8 GiB RAM and SSD as an initial qualification target) and record the real hardware. Do not count an artificially powerful CI host as proof of responsiveness on it. Budgets apply separately to every supported native test environment; do not average a slow platform away.

Plugin matrix: current candidate with Tasks disabled and with the selected supported Tasks version enabled; default light/dark themes; Source/Live Preview/Reading; one and two simultaneous views. Also test upgrade from the last supported legacy release, coexistence of old/new Resources, and the documented unsupported downgrade/unknown-profile path. Pin the minimum supported Obsidian build and the chosen additional compatibility build if release claims cover both.

No unbounded OS × theme × community-plugin Cartesian product is required. Mandatory axes above are recorded; other plugins/themes are targeted regression cases when an observed defect justifies them.

## 4. Test families and ownership

| Family | Primary owner/layer | Required checks | Evidence |
| --- | --- | --- | --- |
| T01 Baseline security/regression | SDKs/server | Retained 0.1 crypto/control/invite/epoch/handshake/snapshot obligations | Actual version-pinned automated reports |
| T02 Section model | SDKs | Schema, IDs, placement slots, Text/scalar, tree/cycles, lifecycle and retained edits | SS01–SS28 through production adapters; extra negatives |
| T03 Independent interoperability | sdk-ts/sdk-rs | Both author/consume directions, concurrent branches, snapshots/tails, continued actors | Logical-state/conflict comparisons and actual bytes exchanged |
| T04 Markdown ownership | Parser/reconciler | All fixture cases, boundary lexing, identity association, CRLF/Unicode/private canaries | Adapter results plus golden before/after/intents |
| T05 Native projection | Obsidian | Transactions, IME, undo/redo, open/closed files, other-plugin writes, split views | Native runs with source/model/caret assertions |
| T06 Secure section E2E | SDKs/server/Obsidian | Share/join/edit/offline/reconnect/restart/snapshot and secure access changes | Two independently initialized vaults and server logs/assertions |
| T07 Durability/races | SDK storage + editor journal | Crash points, lost ACK, duplicate/reordered delivery, stale patches | Fault-injection reports and recovery invariants |
| T08 Access/compatibility | SDKs/plugin | CM01–CM14, effective grants, read-only, revoke/cutoff, old/new coexistence | Actual old/candidate builds; no inferred compatibility |
| T09 Status/UX/accessibility | Obsidian + SDK facts | UX01–UX18, SI01–SI20, keyboard/focus/themes/zoom/reduced motion | Pure reducer tests plus native UI verification |
| T10 Privacy/clipboard/diagnostics | Parser/plugin/SDK | Extraction boundary, MIME purity, no secrets/private content in diagnostics | Synthetic canaries before encryption and at serialization boundaries |
| T11 Scale/performance/limits | SDKs/plugin/server | Defined workloads, budgets, retained history and over-limit handling | Raw samples, percentiles, runtime/hardware and memory data |
| T12 Packaging/operations/pilot | Release/product | Install/upgrade, immutable manifests, backup/restore, release smoke and user outcomes | Exact artifact checksums, rehearsal and pilot report |

The 29 Markdown fixtures include expanded/suffixed cases, not simply numeric MS01…MS29. Use the fixture manifest as the inventory. UX and SI definitions remain in their canonical companion files; this plan does not silently rewrite them.

## 5. Model, interoperability and negative tests

Consume all 28 stored cases, including the 200-Task case, through real implementations. In addition, cover malformed/canonical IDs, wrong actor domain, scalar-versus-Text mismatch, unknown extension retention, missing dependencies, invalid immutable placement edits and duplicate slots. Correctly accepting Automerge bytes is not sufficient if the application history is profile-invalid.

Bidirectional authored scenarios must include concurrent sibling inserts; same Task field conflicts; independent Task/child edits; moves to same and different parents; parent cycle; delete versus child edit/add/move-out; explicit same-value restore; Unicode Text edits; paragraph split/join; repeated moves; snapshots and post-snapshot authoring. Compare all conflict alternatives and retained hidden content, not only visible JSON values.

Add deterministic randomized schedules for supported intent sequences with a recorded seed and failure minimization. Initial target: 100 seeds covering three independent actors, partitions, duplicate delivery and reordering. Check convergence only once replicas possess the same valid history; temporary divergence during partitions is expected. Exclude invalid intent generation from convergence claims and test invalid histories separately.

No fuzz pass can replace a specified counterexample. Preserve every discovered corruption/privacy/identity bug as a deterministic regression fixture. Do not demand arbitrary different concurrent text histories produce the same history bytes.

## 6. Native editor and privacy scenarios

Use synthetic notes with recognizable private canaries before, after and beside each section; separate canaries for two Resources in one file. Include identical-looking Tasks inside and outside the section, fenced marker examples, malformed/overlapping boundaries and foreign refs.

Observe extracted application state/intents **before encryption**, serialized outbound objects, model contents and server stored data. Server ciphertext not containing a canary is not proof that private content was never encrypted and uploaded. Assert the private canaries never enter shared plaintext or imported shared extensions, and that all application payloads traverse the encrypted/signed path. Also test outgoing diagnostics and clipboard separately.

Mandatory native interactions:

1. Add Task, child paragraph, ordinary item and subtask; move/reparent; preserve IDs and minimal source diffs.
2. Change title, due/scheduled/completion fields and list indentation with Tasks enabled/disabled.
3. Edit Cyrillic/emoji and multi-code-unit characters through IME/selection; verify Text index conversion.
4. Receive a remote patch during local typing, composition, undo, file rename and external modification.
5. Remove a marker, introduce unsupported syntax and lose the projection base; preserve candidates and prevent unsafe publication/overwrite.
6. Copy a complete section to another file, duplicate a node, cut/paste a subtree, detach one projection and delete a host file.
7. Edit a standalone Task projection from a section Resource without interpreting omitted children as deletion.
8. Disable/re-enable/restart the plugin while source changes locally; reconcile from a trusted base or show explicit comparison.

For copy/cut, inspect actual text/plain and text/html in each supported mode and OS. Use selection ranges containing only shared content, mixed private/shared content, part of a Task, an entire section and nearby controls. No SVG, check glyph, status text, participant list or card content may be added. Native source-copy bindings remain as selected; readable copy strips the specified LFCP metadata. Cut must not create an extra delete transaction through the serializer.

For status-only transitions, compare exact source bytes, write-event counts and text undo entries before/after. A screenshot is insufficient for source/clipboard purity. Verify folding, viewport scrolling and split panes cannot hide all indications of a relevant problem or attach a control to the wrong identity.

## 7. Secure two-vault acceptance run

Initialize two separate test Principals and clean vaults; do not clone actor/key state to simulate two people. Retain an existing legacy Task Resource alongside the new section.

1. A previews a private 200-Task section with child content and surrounding canaries; creates a dedicated section Resource.
2. A waits for complete creation/hosting readiness, issues one invitation, and B joins via the actual one-time claim/key-delivery flow.
3. B inserts the section into a different private note. No full host note is transmitted.
4. Each user creates/edits supported nodes; both see updates and correct status facts.
5. Partition the clients. Both edit independent fields/text and also create a selected conflict.
6. Restart one client with pending work; reconnect with duplicates, holes and reordered delivery; verify actor safety and model convergence/conflict visibility.
7. Resolve the conflict causally; preserve local pending candidates and apply safe projections.
8. Restart the server with persisted Control/Data/Key Package state; load a snapshot and apply the post-frontier tail.
9. Revoke one identity and rotate the epoch through the baseline control path. Retain and quarantine/reject stale post-cutoff offline work as specified; do not erase the local candidate.
10. Detach one local projection; verify other authorized projections and the Resource remain intact.
11. Inspect extraction, server opacity, source boundaries, status evidence and diagnostics. Re-run the legacy Task secure smoke scenario.

Negative security tests retain 0.1 obligations: invalid signature/AEAD, unauthorized writer or control record, wrong epoch/cutoff, equivocation, invalid Key Package/commitment, replay/duplicate handling and one-time invite double claim. Clients validate before model application regardless of server behavior. Use protocol test fixtures; do not replace cryptography with mocks in the evidence that closes T01/T06.

## 8. Fault injection and recovery

Inject deterministic interruption at the following boundaries. Preserve test state to prove recovery instead of resetting the store until tests pass.

| Fault point | Required recovered outcome |
| --- | --- |
| Journal prepared before SDK commit | Reconcile candidate once; reuse allocated IDs |
| SDK commit complete before source metadata patch | Receipt identifies existing intent; no duplicate node/Task |
| Source patch complete before journal finalization | Recognize generated revision; no feedback-loop change |
| Server persisted unit, ACK lost | Exact immutable retry/reconciliation; same pending batch identity |
| Client restart during queued send | Actor sequence/ciphertext safety; queue retained |
| Server restart during ingest/control CAS | Contract-consistent atomicity; exact state recovered; no falsely durable ACK |
| Snapshot loaded with missing tail | Catch-up remains incomplete; no current/empty-section claim |
| Remote patch prepared, local source changes | Stale patch cannot overwrite new text; rebase or recovery |
| Access revoked during offline editing | Rejected work retained, authorization enforced, UI honest |
| Disk-full/write error or key store unavailable | No saved-local claim without evidence; no state purge; retry/export path |
| Import target hosted before source replacement | Resume same target IDs; changed source blocks stale replacement |
| Index/base metadata lost | Recover refs but do not invent causal intent; preserve local/shared comparison |

Crash/restart and disk-full simulations use isolated test storage. No test deletes real user data or rotates real production access. Include multiple views and external file events in race tests; in-memory-only tests cannot prove filesystem/editor ordering.

## 9. Scale workloads

Generate deterministic synthetic fixtures with recorded seeds, lengths and encoded sizes. The workload identifiers below are new test-plan labels, not additional already-generated corpus files.

| Workload | Definition | Purpose |
| --- | --- | --- |
| W20 | 20 Tasks, 20 child paragraphs, 10 ordinary items | Fast smoke and two-vault functional checks |
| W100 | 100 Tasks, 100 paragraphs, 25 ordinary items; nesting up to 4 levels | Typical working section |
| W200 | 200 Tasks total, including 50 nested Tasks; 200 child/root paragraphs of about 200 Unicode scalars each; 50 ordinary items; nesting up to 4 levels; Cyrillic/Latin/emoji and supported dates | Primary release workload |
| W200-P | W200 projected twice in one vault plus 20 standalone projections of its Tasks; private host file up to 1 MiB | Projection/viewport/attribution costs |
| W200-H | W200 after 10,000 deterministic supported edits/moves/deletes/restores, including retained old placement slots | History/anchor growth; no unauthorized physical GC |
| W2000 | Tenfold content scale, same supported syntax | Stress and safe degradation; not a promised supported maximum |

Snapshot and pending backlog sizes are measured, never inferred from Task counts. Record maximum encoded unit/frame/save sizes and the tested server limits. W200 content must fit the supported secure creation path; if one atomic unit exceeds a real limit, resolve transaction/chunking/publication semantics in the owning spec/SDK before shipping. Do not publish half a section or silently omit child content.

Select and document an actual supported nesting limit at baseline. Test that depth, depth + 1, and adversarial excessive depth with an explicit non-destructive result. The protocol already bounds value nesting (64 levels, §30), document depth (256 levels, §11.2) and change expansion (§11.1); a section limit stays within them. Creation of W200 uses the multi-change import of decision P3. Over-limit source remains preserved; no stack overflow, partial publication or truncated rendering presented as complete.

## 10. Proposed performance budgets and method

Budgets below apply to W200/W200-P on the recorded native qualification machines, with server tests on the recorded reference host. They are starting acceptance targets to freeze before qualification, not published capacity guarantees.

| Metric | Measurement boundary | Initial target |
| --- | --- | --- |
| Input responsiveness | Native key action to next painted result while editing a healthy visible node | p95 ≤ 100 ms; added p95 versus same note/plugin-disabled baseline ≤ 30 ms |
| Durable local update | Supported stable edit event to recoverable SDK/journal commit; excludes active IME/incomplete syntax | p95 ≤ 300 ms |
| Remote projection | Validated model update available locally to correct visible source/render application | p95 ≤ 250 ms; network delay excluded |
| Cached section open | Open note with cached replica to usable section and truthful state | p95 ≤ 2 s |
| Details card | Activation to usable status/access card from cached validated facts | p95 ≤ 200 ms; no network wait for opening |
| Reconnect backlog | Reconnection session ready to reconciled model/current eligible projections; 500 queued changes, total transfer ≤ 5 MiB | p95 ≤ 10 s at 100 ms RTT, 10 Mbit/s each way, no packet loss |
| Main-thread blocking | LFCP-attributable task during normal W200 editing/status updates | No task > 200 ms; record all > 50 ms for investigation |
| Incremental memory | Settled process memory versus same note/plugin-disabled baseline, with Resource and two projections active | ≤ 150 MiB additional; method and GC caveats recorded |
| Lifecycle cleanup | 20 open/close cycles after warm-up, followed by settling/GC where available | No retained view/listener growth; investigate > 10 MiB retained growth between settled checkpoints |

Measure each platform separately. Use at least 200 editing samples and 30 samples for open/card/remote/reconnect operations, after five warm-up runs. Also record five cold-start runs separately; do not combine cold and warm data into one favorable percentile. Publish sample count, p50, p95 and maximum, plus failing outliers and instrumentation overhead. Do not call a single timing a percentile.

W200-H must preserve correctness, run the same functional operations without crashes, and report performance/encoded-size growth; investigate results exceeding twice the corresponding fresh-W200 latency or memory budget. A history-growth issue affecting plausible normal use is blocking until fixed or bounded with an explicit reviewed limit and non-destructive behavior. W2000 is exploratory for latency but mandatory for safe failure/no data loss. Do not turn either case into authorization to garbage-collect retained CRDT history.

Use separately shaped loss/reordering/disconnect tests for correctness; the clean-network latency target above does not apply to them. If a source conflict requires human action, measure time until a truthful actionable state, not time until the model is falsely labeled synchronized.

## 11. Scope-gate traceability

| Scope gate | Required families/evidence | Completion milestone |
| --- | --- | --- |
| G01 Baseline | Exact component/host manifest, commands and inherited gap classification | M02-0; re-pin at candidate |
| G02 Contracts | T02–T04; pinned specs/corpus and resolved incompatibilities | M02-1 |
| G03 Onboarding | T06/T08; safe share/invite/join/insert retries | M02-3 |
| G04 Content | T02/T04/T05/T06; nested content and automatic additions | M02-3 |
| G05 Identity | T02/T03/T05; move/reparent/multiple projections/standalone Task | M02-3 |
| G06 Concurrency | T02/T03/T06/T07; alternatives/retained work/recovery | M02-3 |
| G07 Durability | T01/T06/T07/T08; client/server restart, snapshots, queues and actors | M02-3 |
| G08 Privacy | T01/T04/T06/T10; pre-encryption canaries and opaque server path | M02-3; retain regression |
| G09 Access | T01/T06/T08/T09; validated membership/invite/revoke evidence | M02-4 |
| G10 UX | T05/T09/T10; UX/SI, keyboard, three modes and MIME purity | M02-4 |
| G11 Compatibility | T01/T08/T12; legacy/coexistence/import/upgrade/unknown-profile | M02-4/M02-5 |
| G12 Release | T11/T12; full desktop qualification, limits, pilot and release record | M02-6 |

No gate is closed solely by a document review. Tests that cover several gates should run once and link the same evidence, rather than be duplicated under multiple names.

## 12. Candidate runs and regression policy

Per change, run tests that prove the changed contract plus the owning component's required CI. Changes in shared Task, Wire, storage or authorization code require legacy regression as well as section checks. Parser changes require private-boundary and fixture regression; renderer changes require mode/clipboard/source-purity checks; status changes require reducer races and evidence mapping.

At candidate cut, run the full mandatory matrix against the exact manifest. Store reports with commands, exit results, hashes, seeds, environment and evidence locations. A product fix produces a new candidate; rerun the affected family and mandatory integrated smoke/security/legacy gates. Reuse unchanged evidence only with an explicit impact rationale and identical relevant build inputs. Do not expand testing indefinitely once the required gates and concrete risks are resolved.

Quarantine a flaky noncritical test only with an owner and an independent replacement assertion. A flaky privacy, corruption, authorization, actor-safety or clipboard-purity gate cannot be waived as harmless instability.

Severity:

- Blocker: private disclosure, corruption/loss, unauthorized access, key/nonce/actor safety violation, destructive projection, false durability/current claim with user-impacting loss risk, failure of a required flow/platform or no safe upgrade/rollback.
- Major: a required UX/content/recovery criterion fails even if data remains safe; blocks 0.2 completion until fixed or the scope is explicitly revised.
- Minor: cosmetic or nonessential inconvenience with a documented workaround and no misleading state/access. May ship with an owner and release note.

## 13. Pilot design

Pilot (decision V2): 3–5 opt-in pairs, at least two of them non-developer users, at least 7 days of ordinary usage, including at least two pairs using W100/W200-scale real workflows. An early dogfood with 2–3 pairs precedes it (LFCP-02-105). Betas reach both through BRAT pre-releases. This is a validation window, not an engineering delivery estimate. Do not artificially force users to share sensitive personal notes.

Each pair should complete share/join, add child content, edit offline/reconnect, inspect access/status, copy readable content and detach one projection. Exercise a conflict/recovery scenario with synthetic content during onboarding rather than inducing risky conflicts in valuable notes.

Initial outcome targets (drafted for 5–10 pairs; LFCP-02-005 re-derives the counts for 3–5 pairs before the pilot):

- At least 10 observed end-to-end onboarding attempts across the pilot; at least 8 completed without developer intervention using the supplied instructions.
- Every participating pair completes a two-vault edit/reconnect cycle; unexplained missing/duplicated content is investigated as a blocker.
- At least 8 of 10 short comprehension checks correctly distinguish shared boundary, local-save/server-acceptance, detach and access removal. Capture which concept failed, not just a single satisfaction score.
- No unresolved blocker/major defect; no private-content publication or unrecoverable data loss.

Repeated attempts by one expert do not substitute for independent usability evidence; record attempt distribution and help provided. If targets fail, fix the cause and repeat the affected observation. The pilot is a small product check, not statistical proof of broad market fit.

Collect minimal consented data: build/environment, workflow outcome, elapsed time, intervention needed, issue code and optional sanitized feedback. No automatic vault upload, participant directory collection, note text or invitation secrets. Diagnostics are previewed and manually shared by the user when needed.

## 14. Release stages and operational checks

| Stage | Entry | Allowed claim / exit |
| --- | --- | --- |
| Development | Pinned working draft and isolated test data | Incomplete internal build; no release-ready claim |
| Internal alpha | Secure W20/W200 slice and safety gates passing | Team-only exploration; remaining required gaps listed |
| Release candidate | Full technical matrix, documented limits, upgrade/rollback rehearsal | Exact artifacts eligible for opt-in pilot |
| Pilot-qualified candidate | Pilot outcomes and all G01–G12 evidence | Release owner/product owner review concrete evidence |
| Public 0.2 | Approved version-pinned artifact set and distribution checks | Claims limited to tested subset/platforms/content |

Shared Tasks is listed in the Obsidian community plugins since 0.3.1: a release whose bare `X.Y.Z` tag matches `manifest.json` on `main` updates every user. Betas and the pilot therefore use pre-release tags `0.4.0-beta.N` installed through BRAT, and `manifest.json` on `main` moves to 0.4.0 only at the public release (LFCP-02-094). Check the current directory requirements at execution time.

Before a demo-server rollout, verify backup/restore for persisted Control/Data/Key Packages/snapshots and configuration; do not copy logs containing secrets into evidence. Separate staging Resources and credentials. Deploy a tested image/configuration only if needed. Preserve existing legacy Resources and hosting state. After rollout, run encrypted section and legacy smoke tests and confirm durable reconnect. Website/profile changes describe the actual released build and demo status.

## 15. Rollback and incident response

Maintain the last known-good **section-capable** build and its compatible storage/schema manifest. An arbitrary 0.1 plugin downgrade is not a safe rollback for section data.

On a suspected unsafe projection/publication issue: pause the affected synchronization/projection path using a tested mechanism, preserve source candidates/replicas/exact queues, and show the user an honest blocked state. Do not wipe a cache, regenerate identity or erase queues to make the UI healthy. If disabling the plugin is the only safe stop, explain that edits made while disabled remain local until reconciliation after recovery.

Choose forward-fix or rollback based on tested storage compatibility. If new storage is incompatible with the old build, do not run the old writer against it. Restore to an isolated copy for comparison or provide a tested forward repair. Never reuse stale actor/nonce state from a backup while continuing to publish as the same actor. Server restoration must preserve/control consistency and reconcile client holdings before claims of current state.

A deployment rollback does not undo shared mutations, invitations already claimed or content already disclosed. Access removal follows the protocol; local detach does not revoke anyone. Preserve affected evidence privately, repair in the owning layer and add a regression case before resuming.

## 16. Release record and final check

The release record is built from `scripts/rc-verify.py` manifests and reports (LFCP-02-102), which carry the fields of the planning batch's evidence template. Replace unknown values with actual observations; attach exact artifact/evidence paths or URLs. It is not a signed certification or a passing report.

The final release record includes:

- Component/spec/corpus commits, dependency locks, toolchains and build checksums.
- Exact desktop/server environments and distribution path.
- G01–G12 statuses, T01–T12 reports, native UX/SI/CM results and performance samples.
- Verified ACK/catch-up/durability semantics and implementation limits.
- Pilot outcomes, remaining minor issues and owner decisions.
- Safe upgrade/rollback target, rehearsal result, deployment smoke and accurate public claims.

No release entry should say only “tests passed.” The record must identify what ran, on which builds, what did not run and why. Preserve product-version, profile-ID and Wire-subset distinctions in release notes: 0.2 adds the section profile/product behavior and retains the declared LFCP MVP security subset; it does not imply full LFCP-WIRE-01 conformance.
