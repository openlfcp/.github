# ARTIFACTS-INDEX

**Project:** OpenLFCP  
**Purpose:** Catalog the current OpenLFCP design and protocol artifacts and where each one lives.  
**Status:** Working index

Locations are given as `repository: path`. The repositories are siblings in the `openlfcp` organization, so a location such as `spec: wire/LFCP-WIRE-01.md` means the file `wire/LFCP-WIRE-01.md` in the `openlfcp/spec` repository.

---

## 1. Protocol specifications

### `LFCP-WIRE-01.md`

**Location:** `spec: wire/LFCP-WIRE-01.md`  
**Status:** NORMATIVE (Working Draft)

**Purpose:** First detailed LFCP wire-protocol specification.

**Contains:**

- LFCP binary conventions;
- Resource and Principal identifiers;
- cryptographic profile;
- COSE and deterministic CBOR rules;
- Control Plane records;
- Data Plane units;
- capabilities;
- invitation flow;
- key packages;
- routing;
- ownership transfer;
- Have Vectors;
- snapshots;
- WebSocket messages;
- client/server state machines;
- Control Coordinator;
- server migration;
- minimal client/server conformance rules.

This is the primary normative network-protocol document. It directly incorporates the former Working Draft errata for canonical COSE, deterministic CBOR, canonical Snapshot frontiers, and exact Snapshot AAD. There is no separate `LFCP-WIRE-01.1` document.

---

## 2. LFCP wire interoperability artifacts

All files in this section live in `spec: test-vectors/lfcp-wire-01/`.

### `LFCP-TEST-VECTORS-01.md`

**Location:** `spec: test-vectors/lfcp-wire-01/LFCP-TEST-VECTORS-01.md`  
**Status:** TEST VECTORS

**Purpose:** Human-readable LFCP wire interoperability vectors.

**Contains:**

- deterministic fixture keys and IDs;
- CBOR encodings;
- COSE_Sign1 vectors;
- Control Records;
- ownership transfer;
- invitations;
- HPKE Key Packages;
- Data Units;
- hash chains;
- WebSocket frames;
- negative validation cases.

Used by independent implementations to prove protocol compatibility.

---

### `LFCP-TEST-VECTORS-01.json`

**Location:** `spec: test-vectors/lfcp-wire-01/LFCP-TEST-VECTORS-01.json`  
**Status:** TEST VECTORS

**Purpose:** Machine-readable form of the LFCP wire vectors.

**Contains:**

The structured data consumed by automated conformance tests in TypeScript, Rust, or other implementations.

---

### `generate_lfcp_test_vectors_01.py`

**Location:** `spec: test-vectors/lfcp-wire-01/generate_lfcp_test_vectors_01.py`

**Purpose:** Deterministic generator for LFCP test-vector artifacts.

**Contains:**

- fixture generation;
- cryptographic test data;
- binary encodings;
- hash/signature calculations;
- vector export logic.

Used to reproduce and verify the published vectors.

---

## 3. Shared Objects application profile

### `SHARED-OBJECTS-PROFILE-01.md`

**Location:** `spec: profiles/SHARED-OBJECTS-PROFILE-01.md`  
**Status:** NORMATIVE (Working Draft)

**Purpose:** Normative application-profile specification for collaborative structured objects over LFCP.

**Contains:**

- profile ID `org.openlfcp.shared-objects.v1`;
- Automerge binding;
- deterministic LFCP Principal → Automerge actor mapping;
- Data Unit plaintext framing;
- Snapshot plaintext framing;
- Shared Object identity;
- UUIDv7 Object IDs;
- Task schema;
- scalar conflict semantics;
- add-wins tags and assignees;
- tombstone lifecycle;
- semantic intent model;
- unknown-field preservation;
- profile validation;
- future object-type rules;
- conformance scenarios.

This defines what a collaborative Task means independently of Obsidian.

---

## 4. Shared Objects interoperability artifacts

All files in this section live in `spec: test-vectors/shared-objects-01/`.

### `SHARED-OBJECTS-TEST-VECTORS-01.md`

**Location:** `spec: test-vectors/shared-objects-01/SHARED-OBJECTS-TEST-VECTORS-01.md`  
**Status:** TEST VECTORS

**Purpose:** Human-readable interoperability suite for the Shared Objects Profile.

**Contains:**

- deterministic Resource/Principal fixtures;
- actor-ID derivation;
- PrincipalRef rules;
- UUIDv7 validation;
- Task creation;
- concurrent edits;
- `done` versus `cancelled` conflicts;
- conflict resolution;
- due-date conflicts;
- add-wins tags;
- add-wins assignees;
- tombstone/delete/edit behavior;
- unknown-field preservation;
- unknown-object preservation;
- Object ID collision cases;
- snapshot scenarios;
- malformed-profile negative cases.

Separates byte-exact profile rules from behavioral CRDT interoperability.

---

### `SHARED-OBJECTS-TEST-VECTORS-01.json`

**Location:** `spec: test-vectors/shared-objects-01/SHARED-OBJECTS-TEST-VECTORS-01.json`  
**Status:** TEST VECTORS

**Purpose:** Machine-readable Shared Objects test suite.

**Contains:**

Structured fixtures and expected states for automated TypeScript/Rust conformance testing.

---

### `generate_shared_objects_test_vectors_01.py`

**Location:** `spec: test-vectors/shared-objects-01/generate_shared_objects_test_vectors_01.py`

**Purpose:** Generator for deterministic non-Automerge portions of Shared Objects vectors.

**Contains:**

Fixture generation, IDs, references, validation cases, expected logical states, and machine-readable vector output.

---

### `generate_automerge_reference_01.mjs`

**Location:** `spec: test-vectors/shared-objects-01/generate_automerge_reference_01.mjs`

**Purpose:** Reference Automerge corpus generator.

**Contains:**

A JavaScript generator targeting the selected Automerge compatibility version, producing real Automerge changes/save images for:

- initialization;
- Task creation;
- concurrent status changes;
- merge/conflict state;
- snapshots;
- additional profile scenarios.

This avoids inventing synthetic Automerge bytes.

---

## 5. Obsidian architecture

### `OBSIDIAN-ARCHITECTURE-01.md`

**Location:** `obsidian: docs/OBSIDIAN-ARCHITECTURE-01.md`  
**Status:** ARCHITECTURE

**Purpose:** Architecture specification for the first real OpenLFCP product client.

**Contains:**

- Host Document / Resource / Shared Object / Projection model;
- Obsidian plugin layering;
- recommended repository layout;
- Task projection model;
- Markdown reference syntax direction;
- Markdown → CRDT pipeline;
- CRDT → Markdown pipeline;
- mutation guards;
- projection index;
- multiple projections of one object;
- compatibility with Obsidian Tasks;
- minimal-diff rewriting;
- Resource creation/join/invite flows;
- Resource Explorer;
- local storage;
- route cache;
- connection pooling;
- offline behavior;
- semantic conflict UI;
- privacy invariants;
- startup reconciliation;
- external file changes;
- VS Code portability constraints;
- MVP acceptance scenario;
- implementation phases.

This is the main source of truth for Obsidian-specific implementation work.

---

## 6. Markdown projection reference format

### `MARKDOWN-REFS-01.md`

**Location:** `spec: integration/MARKDOWN-REFS-01.md`  
**Status:** NORMATIVE (Working Draft)

**Purpose:** Normative portable grammar for binding Markdown projections to LFCP Shared Objects.

**Contains:**

- two conforming placements: inline and immediate child-line;
- identical object-reference semantics for both forms;
- child-line as the recommended Obsidian/Tasks-compatible default;
- inline as an allowed compact form where safe;
- placement-preservation rules;
- Base64url Resource ID encoding;
- Shared Object reference grammar;
- indentation and association rules;
- duplicate detection, including inline + child duplicates;
- malformed/orphan diagnostics;
- detach/copy behavior;
- fenced-code protection;
- exact acceptance contract for `LFCP-060`.

This resolves placement without forcing every editor to spend an extra physical line when inline metadata is harmless.

---

## 7. MVP implementation scope and backlog

### `MVP-0.1-PROTOCOL-SCOPE.md`

**Location:** `.github: docs/MVP-0.1-PROTOCOL-SCOPE.md`  
**Status:** GUIDE

**Purpose:** Define exactly which parts of `LFCP-WIRE-01` are required for the first secure MVP.

**Contains:**

- mandatory cryptographic foundation;
- signed/encrypted Data Units;
- minimal Control Plane;
- capabilities and invite claims;
- HPKE Key Packages;
- revocation/key rotation;
- handshake;
- Have Vector synchronization;
- snapshots;
- explicit deferred features such as ownership transfer, federation, presence, and coordinator recovery;
- MVP completion gate.

### `BACKLOG-MVP-0.1.md`

**Location:** `.github: docs/BACKLOG-MVP-0.1.md`  
**Status:** GUIDE (authoritative planning source)

**Purpose:** Authoritative, renumbered MVP 0.1 implementation backlog.

**Contains:**

- `LFCP-001…072` arranged by real dependency layers;
- specification/vector foundation;
- TypeScript crypto, Control Plane, Data Plane and handshake work;
- Shared Objects/local-client work;
- independent Rust protocol core;
- Rust reference server on `sdk-rs`;
- secure invitation, anti-entropy, snapshots and restart durability;
- Obsidian projection tasks, with `LFCP-060` governed by `MARKDOWN-REFS-01`;
- cross-language conformance;
- final security/privacy vertical-slice release gate.

The earlier temporary backlog patch has been superseded and removed.

---

## 8. Project context

### `AGENT-OPERATING-GUIDE.md`

**Location:** `.github: docs/AGENT-OPERATING-GUIDE.md`  
**Status:** GUIDE

**Purpose:** Operating manual for orchestrators, coding agents, reviewers, and contributors.

**Contains:**

- source-of-truth hierarchy;
- repository boundaries;
- layer model;
- task-routing rules;
- mandatory reading sets;
- specification-gap procedure;
- test strategy;
- byte-exact vs behavioral interoperability rules;
- security/privacy rules;
- implementation priorities;
- orchestrator task template;
- agent handoff format;
- review checklist;
- explicit anti-patterns.

This should be provided to agents working on the project.

---

### `PROJECT-NARRATIVE.md`

**Location:** `.github: docs/PROJECT-NARRATIVE.md`  
**Status:** GUIDE

**Purpose:** Human/agent-readable project narrative.

**Contains:**

- project history;
- original Obsidian problem;
- product vision;
- local-first philosophy;
- Shared Objects model;
- LFCP architecture;
- federation;
- server independence;
- identity/auth/encryption/routing separation;
- CRDT philosophy;
- first implementation plan;
- first end-to-end milestone;
- long-term direction.

---

### `engineering-conventions.md`

**Location:** `.github: docs/engineering-conventions.md`
**Status:** GUIDE

**Purpose:** Branches, commits, validation commands, labels, versioning, the Working Draft change process and the spec-gap procedure.

---

### `ARTIFACTS-INDEX.md`

**Location:** `.github: docs/ARTIFACTS-INDEX.md`

This index.

---

## 8a. MVP 0.1 baseline and decisions

### `MVP-0.1-BASELINE.md`

**Location:** `spec: MVP-0.1-BASELINE.md` (current tag `mvp-0.1-baseline.8`)
**Status:** GUIDE

**Purpose:** The exact set of documents, vectors, generators, CDDL files and schemas that MVP 0.1 implementations build against. It is not a Stable publication.

### `adr/0001-mvp-0.1-protocol-decisions.md`

**Location:** `spec: adr/0001-mvp-0.1-protocol-decisions.md`
**Status:** ARCHITECTURE

**Purpose:** The protocol decisions the project owner made for MVP 0.1 (2026-10-05), with the sections and vectors each one changed.

### `adr/0002-mvp-0.1-protocol-decisions-2.md`

**Location:** `spec: adr/0002-mvp-0.1-protocol-decisions-2.md`
**Status:** ARCHITECTURE

**Purpose:** The second batch of project-owner decisions for MVP 0.1 (2026-10-05, SPEC-PATCH-03), with the sections and vectors each one changed and the vector values that changed.

### `adr/0003-mvp-0.1-protocol-decisions-3.md`

**Location:** `spec: adr/0003-mvp-0.1-protocol-decisions-3.md`
**Status:** ARCHITECTURE

**Purpose:** The third batch of project-owner decisions for MVP 0.1 (2026-10-05, SPEC-PATCH-04): the Data Epoch rules, the general error-code rule, connection limits, Shared Objects validation and the Markdown reference grammar, with the sections and vectors each one changed and the vector values that changed.

### `adr/0004-mvp-0.1-protocol-decisions-4.md`

**Location:** `spec: adr/0004-mvp-0.1-protocol-decisions-4.md`
**Status:** ARCHITECTURE

**Purpose:** The fourth batch of MVP 0.1 protocol decisions (SPEC-PATCH-05): G-DP1-GAP (actor chains across abandoned sequences), approved by the project owner, and orchestrator decisions pending owner review (Snapshot cutoff rebuild, invitation query parameters, claimant Key Packages, server and message clarifications, per-value profile diagnostics, `INVALID_AUTOMERGE_BYTES`), each with its status, sections and vectors.

### `adr/0005-mvp-0.1-protocol-decisions-5.md`

**Location:** `spec: adr/0005-mvp-0.1-protocol-decisions-5.md`
**Status:** ARCHITECTURE

**Purpose:** The fifth batch of MVP 0.1 protocol decisions (SPEC-PATCH-06), all orchestrator decisions pending owner review: the writer's previous unit is its latest own unit still accepted, clients retransmit after a request timeout, the invitation read rule uses the §25.2 active grant, a writer keeps writing after a rebuild removes its own changes, scalar conflicts stay profile-valid (S15, S16), SO-STRINGS pointer cases in the Automerge corpus, and Obsidian plugin state kept out of the vault-synced folder, each with its status, sections and vectors.

### `adr/0006-mvp-0.1-protocol-decisions-6.md`

**Location:** `spec: adr/0006-mvp-0.1-protocol-decisions-6.md`
**Status:** ARCHITECTURE

**Purpose:** The sixth batch of MVP 0.1 protocol decisions (SPEC-PATCH-07), all orchestrator decisions pending owner review: exact change expansion limits and structural checks before the Automerge engine, uncompressed changes only, local Snapshot limits with a floor, the value nesting bound, request bounds (KEY_PACKAGE_GET epochs, DATA_GET ranges) and the client receive limit, each with its status, sections and vectors.

### `adr/0007-mvp-0.1-protocol-decisions-7.md`

**Location:** `spec: adr/0007-mvp-0.1-protocol-decisions-7.md`
**Status:** ARCHITECTURE

**Purpose:** The seventh batch of MVP 0.1 protocol decisions (SPEC-PATCH-08), an orchestrator decision pending owner review: the document depth bound (no object deeper than 256 levels below the root, checked before the Automerge engine for changes and Snapshots), with its measurements, sections and vectors.

---

## 8b. Machine-checkable artifacts

| Artifact | Location | Purpose |
| --- | --- | --- |
| Extracted Wire CDDL | `spec: wire/LFCP-WIRE-01.cddl`, `wire/LFCP-WIRE-01.summary.cddl` | Generated from the CDDL blocks of `LFCP-WIRE-01.md` |
| CDDL supplement | `spec: wire/LFCP-WIRE-01.supplement.cddl` | Typed signed-object, Control Record and message rules |
| CDDL fixtures | `spec: wire/fixtures/` | Vector bytes and structural mismatches checked against the CDDL |
| Vector format schema | `spec: schemas/lfcp-vector-format-1.schema.json` | `lfcp-vector-format/1` JSON Schema for both vector suites |
| Vector format fixtures | `spec: schemas/fixtures/` | Format examples and validator self-tests |
| Shared Objects state schema | `spec: profiles/shared-objects-01/schema/` | Structural contract for Shared Objects logical state, with fixtures |
| Migration mapping | `spec: migrations/vector-format-1/` | Proof that the vector-format migration changed no value, plus approved changes |
| Compatibility matrix | `.github: docs/conformance/compatibility-matrix.md` | Dated snapshot of the sdk-rs ⇄ sdk-ts conformance run at a baseline, naming the spec tag, SDK commits and known gaps; generated by `examples: conformance/` (`run.js --strict --write-matrix`), never edited by hand |
| MVP 0.1 release notes (draft) | `.github: docs/release/mvp-0.1-release-notes-draft.md` | Draft release notes for MVP 0.1 (LFCP-072); not published |
| Deferred WIRE-01 features | `.github: docs/release/deferred-wire-01-features.md` | What MVP 0.1 does not implement, or implements partly, and how it behaves instead (LFCP-072 draft) |
| RC verification | `.github: scripts/rc-verify.py`, `docs/release/rc-verification.md` | Local release-candidate check: pins every repository, checks their locks agree, runs every release-blocking gate, writes a report (LFCP-072) |
| README scope statements | `.github: docs/release/readme-scope-statements.md` | The "Scope" section each repository README carries (LFCP-072 draft) |
| Security review (MVP 0.1) | `.github: docs/release/security-review-mvp-0.1.md` | Pre-release security review: findings by severity, fixed vs routed, server hostile-client limits, dependency audit |

---

# 9. Repository placement

```text
openlfcp/spec/
├── wire/
│   └── LFCP-WIRE-01.md
│
├── test-vectors/
│   ├── lfcp-wire-01/
│   │   ├── LFCP-TEST-VECTORS-01.md
│   │   ├── LFCP-TEST-VECTORS-01.json
│   │   └── generate_lfcp_test_vectors_01.py
│   │
│   └── shared-objects-01/
│       ├── SHARED-OBJECTS-TEST-VECTORS-01.md
│       ├── SHARED-OBJECTS-TEST-VECTORS-01.json
│       ├── generate_shared_objects_test_vectors_01.py
│       └── generate_automerge_reference_01.mjs
│
├── profiles/
│   └── SHARED-OBJECTS-PROFILE-01.md
│
└── integration/
    └── MARKDOWN-REFS-01.md
```

Obsidian-specific architecture:

```text
openlfcp/obsidian/docs/
└── OBSIDIAN-ARCHITECTURE-01.md
```

Cross-project context:

```text
openlfcp/.github/docs/
├── PROJECT-NARRATIVE.md
├── AGENT-OPERATING-GUIDE.md
├── MVP-0.1-PROTOCOL-SCOPE.md
├── BACKLOG-MVP-0.1.md
├── ARTIFACTS-INDEX.md
├── conformance/
│   └── compatibility-matrix.md
└── release/
    ├── mvp-0.1-release-notes-draft.md
    ├── deferred-wire-01-features.md
    ├── readme-scope-statements.md
    └── rc-verification.md
```

---

# 10. Status legend

```text
NORMATIVE
    Defines required interoperable behavior.

ERRATA
    Corrects/clarifies a Stable normative artifact.
    Working Drafts are corrected in place instead.

TEST VECTORS
    Machine/verifier-oriented interoperability contract.

ARCHITECTURE
    Defines implementation boundaries and intended structure.

GUIDE
    Defines contributor or agent workflow.

PROTOTYPE
    Historical/experimental implementation, non-normative.

VISUAL
    Human-readable explanatory diagram.
```

---

# 11. Current artifact map

```text
OpenLFCP
│
├── Protocol                               (spec)
│   ├── LFCP-WIRE-01.md
│   └── LFCP-TEST-VECTORS-01.*
│
├── Application Profile                    (spec)
│   ├── SHARED-OBJECTS-PROFILE-01.md
│   └── SHARED-OBJECTS-TEST-VECTORS-01.*
│
├── Product Architecture
│   ├── OBSIDIAN-ARCHITECTURE-01.md        (obsidian)
│   └── MARKDOWN-REFS-01.md                (spec)
│
└── Agent / Project Context                (.github)
    ├── AGENT-OPERATING-GUIDE.md
    ├── MVP-0.1-PROTOCOL-SCOPE.md
    ├── BACKLOG-MVP-0.1.md
    ├── PROJECT-NARRATIVE.md
    └── ARTIFACTS-INDEX.md
```
