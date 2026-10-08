# sdk-ts shared sections conformance (LFCP-02-018)

**Date:** 2026-10-09
**Status:** Evidence for MVP 0.2 task LFCP-02-018; not a release qualification

The TypeScript SDK's section model was run against the full shared sections
reference corpus, SHARED-SECTIONS-TEST-VECTORS-01, at the spec baseline
`mvp-0.2-baseline.1`. The machine-readable record, with the build hashes, is
[mvp-0.2-sdk-ts-sections-evidence.json](mvp-0.2-sdk-ts-sections-evidence.json).

## What ran

| Item | Value |
| --- | --- |
| sdk-ts | `728734a1b931` (main) |
| spec | `mvp-0.2-baseline.1` (`96e21d62b97a`) |
| Engine | `@automerge/automerge` 3.5.0 |
| Toolchain | Node.js v24.4.0, pnpm 10.33.4, macOS arm64 |

1. **The reference verifier with the sdk-ts adapter.** From a spec checkout at
   the tag, `generator/verify-vectors.mjs --adapter` loaded
   `conformance/shared-sections/adapter.mjs` from sdk-ts. The adapter replays
   each case's changes through the production `SectionReplica.receiveChanges`
   (the inherited admission and the section rules of
   SHARED-SECTIONS-PROFILE-01 §14.1) and reports the state from the
   production tree, validation and document; it reads no expected value.
   Result: **56 of 56 cases pass**, every expected field compared except the
   reference's internal error strings. The verifier ran without the `CI`
   variable, so its own replay of SS55 and SS56 ran once, as spec's CI does.
2. **sdk-ts's own runs** (`pnpm exec vitest run conformance/shared-sections`):
   - the adapter on every case in three deliveries: in order, every change
     twice in reverse order, and the base Snapshot plus the branches' changes
     (168 tests);
   - schema validation, the effective tree and the receive path on every case
     (61 tests);
   - authoring: SS01, SS02, SS03, SS06 to SS09, SS11, SS14 to SS18, SS24 to
     SS27, SS40 and SS47 to SS51 written through the SDK's intents reach the
     reference state (23 tests).

## What it shows, and what it does not

The production model reaches the corpus's classification, tree, hidden
nodes, recovery facts, invalid nodes, collisions, retained concurrent edits,
scalar conflicts, Texts, Tasks, counts, types, Snapshot counts and the
refused and held changes, for every case and every delivery.

Not exercised: LFCP signatures, encryption and transport, a server, the
Rust SDK and the cross-language comparison (LFCP-02-023, 024), and the
Obsidian plugin. Logical states are compared; identical save bytes are not
required (SHARED-SECTIONS-TEST-VECTORS-01 §5).
