# BACKLOG-MVP-0.1

**Project:** OpenLFCP  
**Status:** Authoritative Working Backlog  
**Scope:** Secure MVP 0.1  
**Revision date:** 2026-10-05

> This backlog replaces the earlier `LFCP-001...050` draft and the temporary `BACKLOG-MVP-0.1-PATCH.md`. Issue numbers may be rewritten while the project is still in early implementation. Dependencies, not numeric adjacency, determine execution order.

---

# 1. MVP definition

MVP 0.1 is a **secure LFCP vertical slice**, not a plaintext CRDT synchronization demo.

A networked path claiming MVP 0.1 behavior MUST use:

```text
Shared Objects / Automerge change
        ↓
profile framing
        ↓
LFCP Data Unit plaintext
        ↓
per-actor key derivation
        ↓
ChaCha20-Poly1305
        ↓
canonical COSE_Sign1
        ↓
LFCP Wire
        ↓
reference server
```

The MVP also includes the minimum Control Plane needed for real invitations, capabilities, Data Epochs, Control Head ordering, HPKE Key Packages, handshake, anti-entropy, and snapshots.

Deferred features are listed in `MVP-0.1-PROTOCOL-SCOPE.md`.

---

# 2. Milestones

```text
M0  Specification and vectors
M1  TypeScript LFCP core/security
M2  Shared Objects and local client
M3  Reference server (TypeScript) and Rust protocol core
M4  Obsidian product slice
M5  Cross-language conformance and release
```

---

# M0. Specification and vectors

## LFCP-001 - Bootstrap OpenLFCP repositories

Create the initial organization/repository skeleton.

Repositories:

```text
.github
spec
sdk-ts
sdk-rs
server
obsidian
examples
```

Acceptance:

- repositories build from clean checkout;
- standard licenses/readmes present;
- CI skeleton exists;
- repository ownership boundaries match `AGENT-OPERATING-GUIDE.md`.

---

## LFCP-002 - Shared GitHub engineering conventions

Define project-wide conventions.

Acceptance:

- branch/PR policy;
- commit style;
- issue labels;
- versioning policy;
- security-reporting path;
- normative-spec change process;
- Working Draft documents are mutable in place until Stable.

Depends on: `LFCP-001`.

---

## LFCP-003 - Import normative project documents

Populate `openlfcp/spec` and project docs with current artifacts.

At minimum:

```text
LFCP-WIRE-01.md
LFCP-TEST-VECTORS-01.*
SHARED-OBJECTS-PROFILE-01.md
SHARED-OBJECTS-TEST-VECTORS-01.*
MARKDOWN-REFS-01.md
MVP-0.1-PROTOCOL-SCOPE.md
PROJECT-NARRATIVE.md
AGENT-OPERATING-GUIDE.md
```

Acceptance:

- no active references to `LFCP-WIRE-01.1`;
- no contradictory Markdown-ref examples in active docs;
- source-of-truth links are explicit.

Depends on: `LFCP-001`.

---

## LFCP-004 - Define machine-readable test-vector format

Standardize JSON structure for protocol/profile vectors.

Acceptance:

- suite metadata;
- deterministic inputs;
- exact bytes where normative;
- expected success/error;
- behavioral expected state where byte identity is not normative;
- schema validation.

Depends on: `LFCP-003`.

---

## LFCP-005 - LFCP Wire CDDL schema

Extract/maintain machine-checkable CDDL for `LFCP-WIRE-01`.

Acceptance:

- core types;
- Control Records;
- Data Units;
- snapshots;
- message envelope;
- message bodies;
- validation fixtures.

Depends on: `LFCP-003`.

---

## LFCP-006 - Shared Objects structural schema contract

Define machine-checkable structural validation around `SHARED-OBJECTS-PROFILE-01` where practical.

Acceptance:

- Task required fields;
- UUIDv7 validation;
- PrincipalRef validation;
- LocalDate validation;
- tags/assignees map shape;
- profile framing fixtures.

Depends on: `LFCP-003`.

---

## LFCP-007 - Protocol vector validator

Build a small validator for published vector JSON.

Acceptance:

- detects malformed hex/Base64url;
- checks required vector fields;
- verifies expected hashes where possible;
- runs in CI;
- supports Wire and Shared Objects suites.

Depends on: `LFCP-004`.

---

## LFCP-008 - Complete LFCP Wire positive vectors

Finish missing positive vectors, including the consolidated Snapshot rules.

Acceptance:

- `SNAPSHOT-01` byte-exact vector;
- canonical frontier;
- Snapshot AAD;
- encryption/signature/id;
- handshake messages;
- Control/Data/Key Package examples all match `LFCP-WIRE-01`.

Depends on: `LFCP-004`, `LFCP-005`, `LFCP-007`.

---

## LFCP-009 - Complete LFCP Wire negative vectors

Expand rejection cases.

Include:

- non-canonical CBOR;
- tagged COSE object where forbidden;
- invalid signature;
- wrong `kid`;
- AEAD failure;
- stale Control Head;
- Control fork;
- bad actor sequence;
- equivocation;
- bad HPKE recipient;
- malformed Have ranges;
- stale-epoch cutoff violation.

Depends on: `LFCP-008`.

---

## LFCP-010 - Freeze MVP 0.1 protocol baseline

Declare the current Working Draft set the implementation baseline for MVP 0.1.

This is not Stable protocol publication.

Acceptance:

- `LFCP-WIRE-01` + scope + vectors are internally consistent;
- Shared Objects profile/vectors are internally consistent;
- Markdown refs have two conforming placements;
- implementation agents have one unambiguous source-of-truth set.

Current baseline: `spec` tag `mvp-0.1-baseline.3` (SPEC-PATCH-03, `spec: adr/0002-mvp-0.1-protocol-decisions-2.md`), which supersedes `mvp-0.1-baseline.2`. Implementations move to it deliberately; the Key Package vectors changed (G-KP2).

Depends on: `LFCP-008`, `LFCP-009`.

---

# M1. TypeScript LFCP core/security

## LFCP-011 - Bootstrap TypeScript SDK

Create `openlfcp/sdk-ts` workspace/packages.

Acceptance:

- build/test/lint;
- package boundaries for core/wire/client/storage/profile;
- no Obsidian dependency.

Depends on: `LFCP-001`.

---

## LFCP-012 - Identifier primitives and UUIDv7

Implement identifier types and validation.

Include:

```text
ResourceId
PrincipalId
Hash32
ControlRecordId
DataUnitId
ObjectId UUIDv7
```

Important rule:

> UUIDv7 is used for Shared Object identity and convenient generation. Its timestamp/order properties are not LFCP causality, conflict precedence, or authorization ordering.

Acceptance:

- canonical UUIDv7 string validation;
- Resource/Principal raw 32-byte validation;
- Base64url helpers for application refs;
- vectors/tests.

Depends on: `LFCP-011`.

---

## LFCP-013 - Deterministic CBOR

Implement exact deterministic CBOR rules from `LFCP-WIRE-01`.

Acceptance:

- shortest integer/length encodings;
- definite lengths;
- deterministic map ordering;
- duplicate-key rejection;
- exact-byte tests.

Depends on: `LFCP-011`, `LFCP-005`.

---

## LFCP-014 - Principal cryptographic identity

Implement LFCP Principal keys and descriptors.

Acceptance:

- Ed25519 signing keys;
- X25519 key-agreement keys;
- Principal Descriptor;
- deterministic Principal ID;
- import/export boundaries;
- no private-key logging.

Depends on: `LFCP-012`.

---

## LFCP-015 - Canonical COSE_Sign1

Implement persistent LFCP signatures.

Acceptance:

- untagged four-element COSE_Sign1;
- protected header exactly required fields;
- empty unprotected map;
- empty external AAD;
- Ed25519 sign/verify;
- object ID from exact bytes;
- vector parity.

Depends on: `LFCP-013`, `LFCP-014`.

---

## LFCP-016 - LFCP Wire decoder and validation

Implement strict structural decoding for LFCP persistent objects and wire values.

Acceptance:

- rejects malformed/non-canonical forms where required;
- does not re-encode received signed bytes before hashing;
- stable typed errors;
- CDDL/vector tests.

Depends on: `LFCP-012`, `LFCP-013`, `LFCP-015`.

---

## LFCP-017 - TypeScript conformance test runner

Run official Wire vectors against `sdk-ts`.

Acceptance:

- positive vectors pass;
- negative vectors fail with expected class;
- CI entry point;
- useful diff output for byte mismatches.

Depends on: `LFCP-007`, `LFCP-016`.

---

## LFCP-018 - Resource DEK and actor-key derivation

Implement Data Epoch key material.

Acceptance:

- random 32-byte DEK;
- commitment;
- epoch representation;
- HKDF actor-key derivation;
- nonce derivation from actor sequence;
- nonce-reuse protection.

Depends on: `LFCP-013`, `LFCP-014`.

---

## LFCP-019 - Genesis and Control Record codec

Implement signed Control Plane objects.

Acceptance:

- Genesis;
- Control Record payload;
- control sequence;
- previous head reference;
- owner/profile/initial route/coordinator fields;
- exact signed IDs.

Depends on: `LFCP-015`, `LFCP-018`.

---

## LFCP-020 - Control Chain validation

Implement Control Chain verification.

Acceptance:

- linear sequence validation;
- hash linkage;
- signature verification;
- Control Head;
- fork detection;
- `CONTROL_CONFLICT` representation.

Depends on: `LFCP-019`.

---

## LFCP-021 - Capability engine

Implement MVP Resource capabilities.

Acceptance:

- owner implicit abilities;
- grant;
- revoke;
- delegation-subset validation;
- invite claim capability;
- evaluation at a referenced Control Head;
- no server-account shortcut.

Depends on: `LFCP-020`.

---

## LFCP-022 - Control transition and CAS semantics

Implement reusable validation for serialized Control transitions.

Acceptance:

- expected-head check;
- exactly one successor from a given head under coordinator serialization;
- stale-head result;
- one-time claim semantics;
- deterministic transition validation.

This task defines reusable logic. Durable server CAS is implemented later.

Depends on: `LFCP-020`, `LFCP-021`.

---

## LFCP-023 - Data Epoch rotation and strict cutoff

Implement revocation/key-rotation rules required by MVP.

Acceptance:

- next epoch;
- fresh DEK;
- commitment;
- previous-epoch final Have frontier;
- cutoff evaluation;
- stale-unit quarantine/rejection rules.

Depends on: `LFCP-018`, `LFCP-020`, `LFCP-021`.

---

## LFCP-024 - HPKE Key Packages

Implement DEK delivery.

Acceptance:

- X25519-based HPKE profile from WIRE;
- exact info/AAD;
- recipient binding;
- sender authorization hook;
- DEK commitment verification;
- positive/negative vectors.

Depends on: `LFCP-013`, `LFCP-014`, `LFCP-021`, `LFCP-023`.

---

## LFCP-025 - Encrypted and signed Data Unit

Implement the real LFCP Data Unit.

Acceptance:

- exact payload/AAD;
- ChaCha20-Poly1305;
- COSE signature;
- Data Unit ID;
- actor sequence;
- previous-unit hash chain;
- profile plaintext hook;
- AEAD/signature/equivocation tests.

Depends on: `LFCP-015`, `LFCP-018`, `LFCP-020`.

---

## LFCP-026 - LFCP wire message codec

Implement WebSocket message envelope and MVP message bodies.

Include at minimum:

```text
HELLO CHALLENGE AUTH READY
RESOURCE_HOST RESOURCE_OPEN RESOURCE_OPENED RESOURCE_CLOSE
CONTROL_HAVE CONTROL_GET CONTROL_PUT CONTROL_RECORD
DATA_HAVE DATA_GET DATA_PUT DATA_UNIT
KEY_PACKAGE_GET KEY_PACKAGE_PUT KEY_PACKAGE
SNAPSHOT_GET SNAPSHOT_PUT SNAPSHOT
ACK NACK ERROR PING PONG
```

Acceptance:

- deterministic encoding;
- strict decode;
- correlation IDs;
- message-size checks.

Depends on: `LFCP-013`, `LFCP-016`.

---

## LFCP-027 - Session handshake

Implement `HELLO → CHALLENGE → AUTH → READY`.

Acceptance:

- nonce challenge;
- server ID;
- Principal descriptor validation;
- signed auth proof;
- selected Wire profile;
- hosting credential remains separate from Resource authority.

Depends on: `LFCP-014`, `LFCP-015`, `LFCP-026`.

---

## LFCP-028 - Have Vector and anti-entropy

Implement Data Plane holdings/range logic.

Acceptance:

- highest contiguous sequence;
- extra ranges above contiguous;
- canonical normalization;
- holes;
- difference computation;
- missing-range requests;
- idempotent repeated sync.

Depends on: `LFCP-012`, `LFCP-026`.

---

## LFCP-029 - Encrypted Snapshot codec

Implement consolidated Snapshot rules.

Acceptance:

- canonical frontier;
- snapshot key derivation;
- nonce;
- exact Snapshot AAD;
- encryption/decryption;
- COSE signature;
- Snapshot ID;
- `SNAPSHOT-01` vector.

Depends on: `LFCP-015`, `LFCP-018`, `LFCP-028`.

---

# M2. Shared Objects and local client

## LFCP-030 - Shared Task semantic model

Implement `org.openlfcp.shared-objects.v1` Task API.

Acceptance:

- required fields;
- UUIDv7 Object ID;
- lifecycle;
- title/status/dates/priority;
- tags/assignees;
- unknown extension preservation;
- profile validation.

Depends on: `LFCP-012`.

---

## LFCP-031 - Automerge mapping

Bind Shared Objects v1 to Automerge.

Acceptance:

- deterministic Resource+Principal actor derivation;
- one semantic transaction per Automerge change where specified;
- scalar conflicts preserved;
- tombstone behavior;
- add-wins collections;
- exact profile framing.

Depends on: `LFCP-030`.

---

## LFCP-032 - Shared Objects conformance runner

Run `SHARED-OBJECTS-TEST-VECTORS-01` against TypeScript profile implementation.

Acceptance:

- deterministic vectors byte-match;
- reference Automerge corpus loads;
- conflicts match expected sets;
- unknown fields/types survive;
- snapshot round trip.

Depends on: `LFCP-031`.

---

## LFCP-033 - Data Unit application and idempotency

Connect decrypted LFCP Data Units to the selected application profile.

Acceptance:

- verify before apply;
- decrypt;
- profile dispatch;
- apply once;
- duplicate exact unit harmless;
- same actor+seq with different unit treated as equivocation;
- profile-invalid object isolated.

Depends on: `LFCP-025`, `LFCP-031`.

---

## LFCP-034 - Storage abstraction

Define reusable local LFCP storage interfaces.

Store:

```text
Control Records
Control Head
Data Units
Key Packages
Snapshots
routes
Resource metadata
pending outbound state
secret references
```

Acceptance:

- SDK has no Obsidian filesystem dependency;
- exact received signed bytes can be retained.

Depends on: `LFCP-019`, `LFCP-025`, `LFCP-029`.

---

## LFCP-035 - Node persistence adapter

Implement a durable desktop/headless storage adapter.

Acceptance:

- restart-safe actor/control state;
- atomic enough to prevent sequence reuse;
- exact object bytes preserved;
- deterministic test fixture cleanup.

Depends on: `LFCP-034`.

---

## LFCP-036 - Pending outbound queue and sync state

Persist unsent LFCP objects/messages.

Acceptance:

- offline write queues exact immutable object;
- retry does not regenerate a Data Unit with same sequence and different ciphertext;
- ACK processing;
- restart recovery;
- retry/backoff hooks.

Depends on: `LFCP-025`, `LFCP-035`.

---

## LFCP-037 - CRDT convergence/property test suite

Test Shared Objects merge semantics independently from network transport.

Include:

- independent field concurrency;
- done vs cancelled;
- due conflicts;
- tags add/add;
- add/remove add-wins;
- delete/edit;
- delete/restore;
- conflict resolution.

Depends on: `LFCP-031`, `LFCP-032`.

---

## LFCP-038 - Persistence/restart recovery tests

Prove local state is safe across abrupt restart.

Acceptance:

- no actor sequence reuse;
- no loss of pending outbound units;
- Control Head preserved;
- keys and epoch state recover safely;
- CRDT state reconstructs from snapshot/changes.

Depends on: `LFCP-035`, `LFCP-036`.

---

## LFCP-039 - Headless Todo CLI

Build a simple client over the real SDK.

Commands should demonstrate:

```text
create resource
task add/list/complete
resource info
sync
invite/join later when server exists
```

Network mode MUST use the real encrypted/signed LFCP path.

Depends on: `LFCP-033`, `LFCP-035`.

---

# M3. Reference server (TypeScript) and Rust protocol core

## LFCP-040 - Bootstrap Rust SDK

Create `openlfcp/sdk-rs` workspace.

Acceptance:

- build/test/lint;
- core/wire/crypto modules;
- no application/editor dependency.

Depends on: `LFCP-001`, `LFCP-010`.

---

## LFCP-041 - Rust protocol primitives and vectors

Implement independent Rust primitives.

Acceptance:

- identifiers;
- deterministic CBOR;
- Principal IDs;
- canonical COSE;
- official vectors.

Depends on: `LFCP-040`.

---

## LFCP-042 - Rust crypto, Control Plane, and Data Unit implementation

Implement the MVP security core independently in Rust.

Acceptance:

- DEK/actor keys;
- Control Records/Chain;
- capabilities;
- epoch rotation;
- HPKE Key Packages;
- encrypted/signed Data Units;
- snapshots;
- official vector compatibility.

Depends on: `LFCP-041`.

---

## LFCP-043 - Rust wire/session implementation

Implement LFCP messages, handshake, Have Vector, and sync primitives in Rust.

Acceptance:

- Wire message codec;
- handshake;
- anti-entropy structures;
- error model;
- vector/fixture parity.

Depends on: `LFCP-041`, `LFCP-042`.

---

## LFCP-044 - Bootstrap LFCP reference server

Create `openlfcp/server` as a TypeScript/Node application. The server does not depend on `sdk-rs`; `sdk-rs` remains the independent Rust interoperability implementation (`LFCP-040`…`LFCP-043`, `LFCP-069`, `LFCP-070`).

Acceptance:

- one process;
- configuration;
- stable server ID;
- health endpoint;
- minimal dependency footprint.

Depends on: `LFCP-011`.

---

## LFCP-045 - Server SQLite persistence model

Implement durable opaque LFCP storage.

At minimum:

```text
resources
control_records
control_head
data_units
key_packages
snapshots
hosting metadata
```

Acceptance:

- exact bytes retained;
- indexes separated from opaque payload;
- server never needs Shared Objects plaintext.

Depends on: `LFCP-044`.

---

## LFCP-046 - Server setup/admin HTTP surface

Implement only infrastructure/admin HTTP needed for self-hosting.

Include:

- `/health`;
- first-run setup/pairing;
- minimal server settings/admin API.

Resource synchronization remains LFCP WebSocket, not an alternate HTTP protocol.

Depends on: `LFCP-044`.

---

## LFCP-047 - WebSocket transport

Implement LFCP WebSocket endpoint and subprotocol.

Acceptance:

- binary frames only;
- one LFCP message per WebSocket message;
- limits;
- ping/pong;
- connection cleanup.

Depends on: `LFCP-026`, `LFCP-044`.

---

## LFCP-048 - Session authentication and Resource open/host

Implement server side of handshake and Resource session lifecycle.

Acceptance:

- challenge/auth/ready;
- hosting credential separated from LFCP Resource capability;
- resource host/open/opened/close;
- server ID persistence.

Depends on: `LFCP-027`, `LFCP-045`, `LFCP-047`.

---

## LFCP-049 - Durable Control Coordinator CAS

Implement per-resource serialized Control mutation.

Acceptance:

- compare expected Control Head;
- validate successor;
- atomic commit;
- stale-head rejection;
- one-time claim serialization;
- restart-safe current head.

Coordinator recovery is deferred.

Depends on: `LFCP-022`, `LFCP-045`.

---

## LFCP-050 - Server LFCP authorization and ingest validation

Validate persistent objects without application semantics.

Acceptance:

- structural/canonical checks;
- signatures where required;
- capability/control checks;
- Control CAS;
- stable IDs;
- quotas/hosting policy remain separate;
- no DEK or Task parsing required.

Depends on: `LFCP-021`, `LFCP-025`, `LFCP-048`, `LFCP-049`.

---

## LFCP-051 - Sync catch-up and anti-entropy

Implement Control/Data synchronization using WIRE-01 structures.

Acceptance:

- Control Have/Get/Record;
- Actor Have Vector;
- holes/ranges;
- Data Get/Put/Unit;
- Key Package sync;
- Snapshot retrieval;
- repeated catch-up safe.

Depends on: `LFCP-028`, `LFCP-029`, `LFCP-050`.

---

## LFCP-052 - Server duplicate/equivocation handling

Acceptance:

- exact replay deduplicated;
- repeated put returns stable result;
- same actor+seq with different Data Unit detected;
- object IDs indexed correctly;
- fan-out does not duplicate semantic apply.

Depends on: `LFCP-050`, `LFCP-051`.

---

## LFCP-053 - Secure invitation and capability claim flow

Implement actual WIRE-01 invitation flow.

Acceptance:

```text
Invitation Principal
→ Capability Grant
→ invitation Key Package
→ lfcp://join URI
→ recipient Principal
→ CAPABILITY_CLAIM through coordinator
→ recipient authorization
→ DEK delivery
→ RESOURCE_OPEN
→ initial sync
```

Second claim against a one-time invitation must fail deterministically.

Depends on: `LFCP-021`, `LFCP-024`, `LFCP-049`, `LFCP-051`.

---

## LFCP-054 - Server restart durability

Acceptance:

- abrupt restart preserves Resource state;
- Control Head preserved;
- committed Data Units preserved;
- snapshots/key packages preserved;
- reconnect/catch-up works without duplicates.

Depends on: `LFCP-045`, `LFCP-051`, `LFCP-053`.

---

## LFCP-055 - Docker image and compose environment

Acceptance:

- reproducible image;
- persistent volume;
- health check;
- first-run setup path;
- restart durability test.

Depends on: `LFCP-054`.

---

## LFCP-056 - Two-headless-client secure network E2E

Use two real clients against the reference server.

Scenario:

- create Principal/Resource;
- invite/join;
- exchange encrypted/signed Task changes;
- disconnect/reconnect;
- catch-up;
- converge;
- server never receives Task plaintext.

Depends on: `LFCP-039`, `LFCP-053`, `LFCP-055`.

---

## LFCP-057 - Network chaos/reconnect tests

Include randomized or table-driven:

- disconnect after send before ACK;
- duplicate delivery;
- message reordering;
- Have holes;
- server restart;
- stale Control Head;
- invalid signature;
- AEAD failure;
- stale previous-epoch write.

Depends on: `LFCP-056`.

---

# M4. Obsidian product slice

## LFCP-058 - Bootstrap Obsidian plugin

Create `openlfcp/obsidian` plugin project.

Acceptance:

- install/load in clean vault;
- commands/settings scaffolding;
- test harness;
- no protocol reimplementation.

Depends on: `LFCP-001`.

---

## LFCP-059 - Integrate TypeScript LFCP SDK into Obsidian

Wire generic client/storage/profile packages into plugin lifecycle.

Acceptance:

- Principal initialization;
- local Resource registry;
- storage adapter;
- session lifecycle;
- no Obsidian dependency leaks into generic SDK.

Depends on: `LFCP-035`, `LFCP-058`.

---

## LFCP-060 - Parse `lfcp-ref` markers

Implement `MARKDOWN-REFS-01` exactly.

Required behavior:

- parse inline form;
- parse child-line form;
- normalize both to the same binding;
- detect duplicates, including inline+child;
- detect malformed/orphan refs;
- ignore fenced examples;
- preserve placement metadata;
- Obsidian serializer defaults to child-line;
- serializer can emit inline when configured.

Depends on: `LFCP-059`, `MARKDOWN-REFS-01.md`.

---

## LFCP-061 - Markdown Task to Shared Object projection

Convert local Markdown semantic edits into Shared Objects intents.

Acceptance:

- title/status first;
- Task without ref remains local-only;
- both ref placements supported;
- unrelated Markdown untouched;
- semantic intent, not raw-line sync.

Depends on: `LFCP-031`, `LFCP-060`.

---

## LFCP-062 - Shared Object to Markdown projection

Apply local/remote CRDT changes back into Markdown.

Acceptance:

- update represented Task fields;
- preserve surrounding private text;
- preserve existing inline/child ref placement;
- mutation guard prevents echo loop;
- conflict indicator hook.

Depends on: `LFCP-061`.

---

## LFCP-063 - Golden projection fixture suite

Create exact before/event/after fixtures.

Include:

- inline ref;
- child-line ref;
- Tasks-style due metadata;
- rename;
- complete/reopen;
- moved Task;
- multiple projections;
- duplicate refs;
- private surrounding text.

Depends on: `LFCP-061`, `LFCP-062`.

---

## LFCP-064 - Minimal-diff Markdown updater

Acceptance:

- changes smallest safe range;
- preserves line endings;
- preserves unrelated tokens;
- preserves ref placement;
- does not rewrite whole file for one field change.

Depends on: `LFCP-062`, `LFCP-063`.

---

## LFCP-065 - Obsidian Resource and invite UI

Implement minimal product UI.

Include:

```text
Create collaboration
Join collaboration
Share task under cursor
Insert shared object
Invite collaborator
Resource status
Detach task
```

Depends on: `LFCP-053`, `LFCP-059`, `LFCP-060`.

---

## LFCP-066 - Automated two-vault E2E scenario

Canonical product test.

Acceptance:

- two clean vaults;
- create Resource;
- invite/join;
- same Task in different files;
- remote completion updates other projection;
- private Markdown never synchronizes;
- both inline and child-line projections covered;
- offline edit + reconnect;
- semantic conflict surfaced/resolved.

Depends on: `LFCP-056`, `LFCP-064`, `LFCP-065`.

---

## LFCP-067 - Obsidian restart recovery

Acceptance:

- plugin/Obsidian restart with pending offline changes;
- projection index reconstructs;
- no sequence reuse;
- queued LFCP Data Units synchronize afterward;
- no duplicate semantic action.

Depends on: `LFCP-066`.

---

## LFCP-068 - Desktop platform smoke matrix

Run release-blocking smoke scenarios on:

```text
macOS
Windows
Linux
```

Acceptance:

- plugin installation;
- key/storage behavior;
- WebSocket connection;
- two-vault basic sync;
- restart recovery.

Depends on: `LFCP-067`.

---

# M5. Cross-language conformance and release

## LFCP-069 - Rust Shared Objects profile interoperability

Implement enough Shared Objects v1 in Rust to independently consume/produce the profile corpus.

Acceptance:

- actor derivation;
- Task state;
- conflict visibility;
- tombstones;
- add-wins sets;
- reference Automerge corpus compatibility.

Depends on: `LFCP-032`, `LFCP-040`.

---

## LFCP-070 - Cross-language protocol conformance

Run TypeScript and Rust against the same official vectors and each other.

Acceptance:

- byte-exact outputs match where normative;
- TS accepts valid Rust objects;
- Rust accepts valid TS objects;
- malformed cases rejected consistently;
- compatibility matrix published.

Depends on: `LFCP-017`, `LFCP-042`, `LFCP-043`, `LFCP-069`.

---

## LFCP-071 - MVP security/privacy vertical-slice E2E

Create one release-blocking end-to-end security scenario.

Scenario includes:

1. Principal creation;
2. Resource Genesis + DEK;
3. server hosting;
4. secure invite and claim;
5. authenticated sessions;
6. encrypted/signed Shared Objects changes;
7. offline edit and Have catch-up;
8. restart durability;
9. revocation + Data Epoch rotation;
10. stale post-cutoff write rejection/quarantine;
11. Snapshot load + catch-up;
12. assertion that server storage contains no configured private Markdown fixture or Task plaintext fixture.

Depends on: `LFCP-057`, `LFCP-066`, `LFCP-070`.

---

## LFCP-072 - Cross-language conformance, release, and canonical demo

Prepare OpenLFCP MVP 0.1 release candidate.

Acceptance:

- all release-blocking CI green;
- TS/Rust conformance published;
- server Docker image;
- headless Todo demo;
- canonical two-vault Obsidian demo;
- specs/vectors published;
- known deferred WIRE-01 features documented;
- README clearly says MVP 0.1 implements the scoped subset, not every deferred WIRE-01 feature.

Depends on all release-blocking tasks, especially `LFCP-068`, `LFCP-070`, `LFCP-071`.

---

# 3. Critical dependency spine

Approximate critical path:

```text
001 → 003 → 010
            │
            ▼
011 → 013 → 014 → 015
                  │
                  ├→ 019 → 020 → 021 → 022
                  │                    │
                  │                    ├→ 023 → 024
                  │                    │
                  └→ 018 → 025 ────────┘
                           │
                           ▼
                    026 → 027 → 028 → 029
                           │
                    030 → 031 → 033
                           │
                    034 → 035 → 036 → 039

040 → 041 → 042 → 043   (Rust, feeds 069/070)

011 → 044 → 045 → 047 → 048 → 049 → 050 → 051   (server consumes sdk-ts 021/022/025/026/027/028/029)
                                       │
                                       ▼
                                    053 → 056 → 057

058 → 059 → 060 → 061 → 062 → 064 → 065 → 066 → 067 → 068

017 + 042/043 + 069 → 070
057 + 066 + 070 → 071 → 072
```

Parallel work is encouraged where dependencies permit.

---

# 4. Explicit anti-shortcuts

Agents MUST NOT:

- introduce a plaintext network Data Unit and call it LFCP;
- make server accounts the source of Resource authority;
- skip Control Chain/capability validation in the secure E2E path;
- use a simple global sync cursor instead of WIRE-01 Control/Data anti-entropy;
- generate invitation tokens disconnected from the Control Plane;
- treat UUIDv7 timestamp order as causality;
- make the server parse Shared Objects plaintext;
- invent a third Markdown-ref placement;
- support only inline or only child-line refs;
- rewrite one ref placement into the other during unrelated synchronization.

---

# 5. Definition of MVP 0.1 done

MVP 0.1 is complete only when the following is automated:

```text
Two independent Obsidian vaults
        +
portable Shared Task
        +
secure invitation
        +
real LFCP cryptography
        +
Control Plane authorization
        +
reference server
        +
offline edits
        +
anti-entropy reconnect
        +
semantic conflict resolution
        +
snapshot recovery
        +
private Markdown leakage test
```

A CRDT demo without these properties is a useful development fixture but is not the OpenLFCP MVP 0.1 release gate.
