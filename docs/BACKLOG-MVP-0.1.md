# BACKLOG-MVP-0.1

**Project:** OpenLFCP  
**Status:** Authoritative Working Backlog  
**Scope:** Secure MVP 0.1  
**Revision date:** 2026-10-07

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
M3  Rust protocol core and reference server
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

Current baseline: `spec` tag `mvp-0.1-baseline.9` (SPEC-PATCH-09, `spec: adr/0008-recovery-after-server-data-loss.md`), which supersedes `mvp-0.1-baseline.8`. Implementations move to it deliberately; no vector value changed. A server refuses a Data Unit whose `previous` it does not hold (`UNKNOWN_PREVIOUS`, code 23); clients reconcile in both directions, relay accepted objects and re-host a Resource a route lost; a change whose Automerge actor and sequence number are taken is held and retried (POST-001). The new `data_put_previous`, `have_difference` and corpus `collision` cases need runners. The project owner accepted ADR 0008 on 2026-10-08.

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
RESOURCE_HOST RESOURCE_HOSTED RESOURCE_OPEN RESOURCE_OPENED RESOURCE_CLOSE
CONTROL_HAVE CONTROL_GET CONTROL_BATCH CONTROL_PUT
DATA_HAVE DATA_GET DATA_BATCH DATA_PUT
KEY_PACKAGE_GET KEY_PACKAGE_BATCH KEY_PACKAGE_PUT
SNAPSHOT_GET SNAPSHOT SNAPSHOT_PUT
ACK NACK ERROR PING PONG
```

The names and codes are those of the `spec: LFCP-WIRE-01` §33 registry, which is authoritative.

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

## LFCP-039a - TypeScript client WebSocket transport and sync session

Implement the client side of WIRE-01 §63–§69 in sdk-ts: drive the
connection, session and per-Resource state machines over a real
WebSocket against the reference server.

Acceptance:

- binary frames only, one LFCP message per WebSocket message, size limits;
- HELLO / CHALLENGE / AUTH / READY through the handshake of `LFCP-027`;
- RESOURCE_OPEN / OPENED / CLOSE and the §65 per-Resource state machine;
- Control and Data catch-up with the Have Vectors of `LFCP-028`, then live
  sync;
- pending outbound queue (`LFCP-036`) flushed and acknowledged;
- reconnect with backoff; connection loss closes every open Resource
  (§65);
- no Obsidian dependency.

Depends on: `LFCP-026`, `LFCP-027`, `LFCP-028`, `LFCP-033`, `LFCP-036`.

---

## LFCP-039b - TypeScript invite URI and invitation-secret codec

Implement the WIRE-01 §18.2 invitation URI in sdk-ts.

Acceptance:

- `lfcp://join/<resource-b64url>?endpoint=…&grant=…` with one or more
  endpoints, and the bearer form with `#secret=…`;
- canonical unpadded Base64url Resource and grant IDs;
- endpoint percent-encoding of everything outside the RFC 3986
  unreserved set, upper-case hex (G-RS4);
- the deterministic CBOR invite secret, and recomputation of the
  Invitation Principal descriptor, which must match the subject of the
  referenced Invitation Grant before the secret is used;
- the secret is never logged or sent to a server;
- the `invite_uri` vector reproduced byte for byte.

Depends on: `LFCP-014`, `LFCP-021`, `LFCP-024`.

---

# M3. Rust protocol core and reference server

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

Create `openlfcp/server` in Rust, on `sdk-rs`. The server uses the `lfcp` crate's protocol core without its `shared-objects` feature, so it never links Automerge or Task semantics.

Acceptance:

- one process;
- configuration;
- stable server ID;
- health endpoint;
- minimal dependency footprint.

Depends on: `LFCP-043`.

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

Depends on: `LFCP-043`, `LFCP-044`.

---

## LFCP-048 - Session authentication and Resource open/host

Implement server side of handshake and Resource session lifecycle.

Acceptance:

- challenge/auth/ready;
- hosting credential separated from LFCP Resource capability;
- resource host/open/opened/close;
- server ID persistence.

Depends on: `LFCP-045`, `LFCP-047`.

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

Depends on: `LFCP-042`, `LFCP-045`.

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

Depends on: `LFCP-048`, `LFCP-049`.

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

Depends on: `LFCP-021`, `LFCP-024`, `LFCP-039a`, `LFCP-039b`, `LFCP-049`, `LFCP-051`.

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

Depends on: `LFCP-039`, `LFCP-039a`, `LFCP-053`, `LFCP-055`.

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

Depends on: `LFCP-039a`, `LFCP-056`.

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
                                 │
                    026/027/028/033/036 → 039a   (TS client transport)
                    014/021/024 → 039b           (TS invite URI codec)

040 → 041 → 042 → 043 → 044 → 045 → 047 → 048 → 049 → 050 → 051
                                                         │
                                                         ▼
                                       039a + 039b → 053 → 056 → 057

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

# 6. Post-MVP 0.1 work

Work decided for after MVP 0.1, each with its decision record or source.

## POST-001 - Hold and retry Automerge (actor, seq) collisions

Decision: the project owner, 2026-10-06
(`.github: docs/release/open-decision-actor-seq-collision.md`, option B).

Today both SDKs refuse a change whose Automerge actor and sequence number
match a different change the replica holds (`ACTOR_EQUIVOCATION`). In sdk-ts
the unit is marked `profile-rejected` for good. In the equivocation corner
the replica therefore stops showing that collaborator's later edits, with no
notice. MVP 0.1 ships with this, which is safe by default.

Deliver, as a spec patch and new baseline, then an alignment in each SDK:

- SHARED-OBJECTS-PROFILE-01 §14.1: a replica never merges two changes with
  the same actor and sequence number. It holds the later one (not refused)
  and retries it after any rebuild that removes changes;
- vectors: a held change that applies after the rebuild that removes the
  change it collided with;
- sdk-ts: the profile's `ACTOR_EQUIVOCATION` becomes a held unit instead
  of `profile-rejected`, retried after `exclude`/rebuild;
- sdk-rs: the same;
- the Obsidian plugin: surface a refused or held change to the user.

Acceptance:

- the equivocation corner converges once the replica learns of the
  equivocation, on both SDKs (a live interop case);
- no new abuse: a malicious writer still affects only its own history and
  the work built on it.

## POST-002 - Manual Obsidian smoke on Windows, Linux and a cross-OS pair

Source: `obsidian: docs/devel/testing/platform-smoke-runs.md` ("Status by
platform") and `obsidian: docs/devel/testing/platform-smoke.md`.

MVP 0.1.0 shipped with the manual checklist run on macOS only, through the
two-vault demo. The automated platform smoke passes on all three systems.

Deliver:

- the manual checklist on Windows (CRLF check included) and on Linux;
- one D and E run pairing two operating systems over `wss://`;
- on macOS, the checks the demo did not exercise: A1, C1, C4, E1, E2 and
  Paths;
- a record per run in `platform-smoke-runs.md`.

Acceptance:

- every platform row reads PASS for both parts, with no NOT RUN left;
- the cross-OS pair is recorded with both platform records.

## POST-003 - Server hosting abuse limits

**State:** done. Shipped in server 0.2.0: e825c30..1e59dcf, plus 2a4d5c7
and 24f013d (revocation and key rotation through at quota, the control
reserve).

Source: `.github: docs/release/security-review-mvp-0.1.md`, H5 and the
known limitations under "Follow-up: server hardening".

Hosting is open by default (`IngestPolicy` defaults to `Unlimited`), with no
quotas. The connection cap is global, there are no rate limits, and a flood
can fill the admin challenge cap.

Deliver:

- the allow-list hosting policy as the default, or quotas (Resources,
  bytes) per hosting credential;
- a per-IP connection cap that sees the client address behind the proxy;
- rate limits on WebSocket messages and the admin HTTP API;
- admin challenges that a flood cannot exhaust for the administrator.

Acceptance:

- a fresh server refuses hosting from an unknown key, or enforces its
  quota, with tests;
- each limit has a test that crosses it and gets the documented refusal.

## POST-004 - Server memory bounds

**State:** done. Shipped in server 0.2.0: bb9677c..0aa4dab.

Source: `.github: docs/release/security-review-mvp-0.1.md`, H6 and M5 after
READY.

`DATA_GET`, `KEY_PACKAGE_GET` and `CONTROL_GET` replies are built fully in
memory. The outbound queue counts 256 messages, not bytes, so a connection
can hold up to 256 × `max_message_bytes`. Admin request bodies have no read
timeout.

Deliver:

- streamed or paged GET replies;
- outbound queue accounting in bytes, with a per-connection byte cap;
- a read timeout for admin request bodies.

Acceptance:

- a test with a large Resource shows peak memory per connection bounded by
  the configured byte cap;
- a slow admin body is closed after the timeout.

## POST-005 - Owner-only state files on Windows

Source: `.github: docs/release/mvp-0.1-release-notes.md`, Known limitations
("Windows: no owner-only state files").

On Windows the server's state files (server ID, setup code, the database)
inherit the state directory's ACL. On Unix the directory is 0700 and the
files 0600.

Deliver: the server restricts the state directory and files to its own
user on Windows, at creation and at every start, as on Unix.

Acceptance: a Windows CI test reads the ACLs and finds only the server's
user (and SYSTEM, if Windows requires it).

## POST-006 - Encrypt local checkpoints at rest

Source: `.github: docs/release/security-review-mvp-0.1.md`, M10 and
"Secret flow (sdk-ts, obsidian)".

Decrypted Shared Objects state (checkpoints) is stored as plaintext in
IndexedDB or SQLite.

Deliver: checkpoints encrypted with a device key held in the secret store
(Obsidian `secretStorage`, the Node `FileSecretStore`), in sdk-ts storage
and the plugin; a migration of existing plaintext checkpoints.

Acceptance: no task text appears in the IndexedDB or SQLite files (a test
greps them); a lost device key means a resync, not a crash.

## POST-007 - Snapshot publishing in the Obsidian plugin

Source: `.github: docs/release/deferred-wire-01-features.md`, §4 "Partial in
MVP 0.1 software" ("The plugin loads Snapshots but never publishes one").

Deliver: the plugin publishes Snapshots through the SDK, on a documented
trigger (size or change count), with the writer capability it requires.

Acceptance: a new joiner catches up from the plugin's Snapshot in the
two-vault E2E; the §4 row is removed from the deferred list.

## POST-008 - Invitation URI codec in sdk-rs

Source: `.github: docs/release/deferred-wire-01-features.md`, §4
("Invitation URI codec in sdk-rs").

sdk-rs checks an invitation URI's components but has no `lfcp://join`
parser or writer, so its `invite_uri_*` validation vectors are skipped.

Deliver: a parser and writer in sdk-rs; the skipped vectors enabled.

Acceptance: every `invite_uri_*` vector passes in sdk-rs; the conformance
harness exchanges invitation URIs between sdk-ts and sdk-rs in both
directions.

## POST-009 - Invitation sharing UX

Source: `.github: docs/release/deferred-wire-01-features.md`, §4
("Invitation sharing"); `obsidian: docs/OBSIDIAN-ARCHITECTURE-01.md`
(copyable text, QR code, OS share sheet). Deferred from LFCP-065.

Deliver: a QR code for the invitation link, and the OS share sheet where
Obsidian offers one, without logging or storing the link.

Acceptance: a second device joins by scanning the QR code; the link never
appears in logs, settings or the vault.

## POST-010 - Deterministic engine-trap test

Source: `.github: docs/release/rc-verification.md`, the rc7 row.

`sdk-ts: conformance/security/engine-trap.test.ts` can hit its 60 s
child-process timeout on a loaded machine. The failure then shows no
stderr.

Deliver: a test that does not depend on machine load, for example a
smaller trap input, a longer timeout reported as such, or its own
serialized run; on timeout, the error says it timed out.

Acceptance: 20 consecutive full `pnpm test` runs under parallel load pass.

## POST-011 - Obsidian plugin distribution

**State:** in the community directory review, which **passed** for 0.3.1
on 2026-10-07:
- verified attestations for `main.js` and `styles.css`;
- "Build reproduced the release main.js byte-for-byte";
- no vulnerable dependencies.

Only the review's notes on enumerating the vault's files and on the
disclosures remain, and the README answers them ("What the plugin
accesses", "Network use"). Releases since 0.2.0: 0.3.0 and 0.3.1. The
reproducible build comes from sdk-ts 0.1.1 on npm: the plugin now takes
the `@openlfcp/*` packages from npm at exact versions instead of a sibling
checkout.

Earlier: released 0.2.0. The obsidian tag `0.2.0` has its GitHub
release with 4 assets
(https://github.com/openlfcp/obsidian/releases/tag/0.2.0); CI and the
platform smoke on 3 OS are green at a620051; the BRAT beta install passed
(owner, 2026-10-07). It contains:
- the rename to Shared Tasks / `shared-tasks` (ae3747a), with the
  device-local state keys unchanged, so a 0.1.0 identity survives;
- version 0.2.0 (3cc9279);
- the release workflow for bare version tags (2953e19), with the 0.2.0 notes;
- the install, release and directory-submission docs (289bf7a).

Next, by the owner: the listing once the directory accepts it
(`obsidian: docs/devel/community-submission.md`).

Source: `obsidian: manifest.json`, `versions.json`; the Obsidian community
plugin submission rules.

The plugin is released as source and commits only; users build it.

Deliver:

- a GitHub release per version with `main.js`, `manifest.json` and
  `styles.css` as assets, built by CI from the tagged commit;
- `manifest.json` and `versions.json` kept in step with each release;
- a BRAT beta first, then a submission to the community plugin directory;
- the rename to the decided name and ID in `manifest.json` (today the ID is
  `openlfcp`), with its consequences for existing installs.

Name and ID: **decided** (project owner, 2026-10-06). The display name is
"Shared Tasks" and the plugin ID `shared-tasks`. Both were free in the
directory's `community-plugins.json` on 2026-10-06 ("Relay" and "Tandem"
are taken), and they respect Obsidian's rules: no "Obsidian" or "Plugin"
in the name, a lowercase ID.

Acceptance: a clean vault installs the plugin from the release (BRAT, then
the directory) without building it.

## POST-012 - Deprecate the npm placeholder versions (owner)

Source: npm: `@openlfcp/crypto` and `@openlfcp/storage-idb` both have a
`0.0.0-stage` version from before MVP 0.1.

Deliver: `npm deprecate @openlfcp/<pkg>@0.0.0-stage "placeholder; use 0.1.0 or later"`
for both packages.

Acceptance: `npm view @openlfcp/<pkg>@0.0.0-stage deprecated` prints the
message for both.

## POST-013 - Recovery after server data loss (restore wedge)

Source: `.github: docs/operations/sync-server-runbook.md` ("Gaps for the
owner") and the restore drill in `devbox-asstnt: stacks/openlfcp/README.md`
(2026-10-06).

**Blocks the public server leaving POC/beta status (owner to confirm).**

**State:** designed, not decided. The draft ADR 0008 (`spec:
adr/0008-recovery-after-server-data-loss.md`, spec 0d0d68b) is Proposed;
the project owner's decision is pending.

After a server is restored from a backup, the Data Units it had
acknowledged after the backup are gone. The client that wrote them never
re-sends them, because they were acknowledged. Its next unit is accepted
over the sequence gap, and every other client stops at that actor with
`NO_PROGRESS`, seeing neither the lost unit nor anything after it. In the
drill the server held one actor's sequences 1, 2, 3 and 5.

Deliver:

- a spec design note with the options:
  - (a) client anti-entropy: compare the server's per-actor heads with
    its own and re-upload what the server is missing;
  - (b) the server refuses a sequence gap with a defined error, which
    triggers a re-upload;
  - (c) both;
- then a spec patch and a new baseline, and the alignment in sdk-ts and
  sdk-rs;
- a live interop test that reproduces the drill: back up, write, restore,
  write again, and a second client catches up.

Acceptance: the drill scenario converges, and no acknowledged unit that
any client still holds is lost.

## POST-014 - lfcp-admin CLI

**State:** done. Merged on server main (4644302, 36805ed, 740e589), ships
in the next server release. Docs: `devbox-asstnt` c2ca4b3 (stack admin
section), `.github` 5f43154 (runbook abuse section).

Source: `.github: docs/operations/sync-server-runbook.md` ("Gaps for the
owner"); `server: README.md` ("Administration").

Pairing and every `/admin` call need a COSE proof signed by the
administrator's Principal. Today only the server's tests can produce one,
with test-vector keys.

Deliver: a CLI, run on a machine that holds the admin key, for the first-run
pairing (`/setup/pair`) and signed admin calls: the hosting policy,
per-Principal quota overrides, and status. It works over an SSH tunnel to
the server's loopback port.

Acceptance: a fresh server is paired with it and its hosting policy and a
quota override are set and read back, in a test against the real server.

## POST-015 - Ban and purge in the admin API

Source: `.github: docs/operations/sync-server-runbook.md` ("Abuse
handling", "Gaps for the owner").

Server 0.1.0 has no ban and no delete. Today an IP is blocked in nginx, and
a Resource is purged by hand with SQL while the server is stopped.

Deliver: admin API calls to ban a Principal or an IP address (refused at
connect or at authentication), and to purge a Resource (every row of it,
in one transaction), replacing the manual SQL; `lfcp-admin` (POST-014)
commands for them.

Acceptance: tests for a banned Principal and a banned IP being refused, and
for a purge, including a server restart after the purge with the other
Resources intact.

## POST-016 - Spec clarification: batched GET answers

Source: the POST-004 work (streamed and paged GET replies in the server).

`spec: wire/LFCP-WIRE-01.md` §49 says "A peer MAY answer in multiple
`DATA_BATCH` messages." §45 (`CONTROL_GET`) and §52 (`KEY_PACKAGE_GET`) say
nothing about it, though a paging server answers them in several
`CONTROL_BATCH` and `KEY_PACKAGE_BATCH` messages too.

Deliver: the same sentence in §45 and §52, as an informative
clarification (no normative change, no new baseline needed on its own).

Acceptance: §45, §49 and §52 read alike; the change log of the next spec
revision lists it as informative.

## POST-017 - Client UX: a Resource the server no longer hosts

**State:** done. Local, not pushed:
- sdk-ts cae7434: a terminal, typed refusal — `resourceRefusal`, the
  `resource-refused` event, `TERMINAL_RESOURCE_CODES` — and transient
  refusals retried with backoff;
- examples b5f9ce0: `lfcp-todo sync` and `watch` exit 1 with the server, the
  Resource and the code;
- obsidian 51ea77d: one notice and the reason in "Resource status".

Each has a live test against server d6cd820. It ships with the next
sdk-ts and Shared Tasks releases.

Source: `.github: docs/operations/sync-server-runbook.md` ("Purge a
Resource", the rehearsal on server 0.2.0; `.github` c87c16b).

After a purge, the server answers `RESOURCE_OPEN` of that Resource with
`NACK(RESOURCE_NOT_HOSTED)`, but `lfcp-todo sync` waits without an error
until it is killed. The client treats the refusal as something to retry
instead of a final state. The same happens to any client whose server lost
or removed a Resource.

Deliver:

- sdk-ts: `RESOURCE_NOT_HOSTED` for an open Resource becomes a terminal,
  typed sync state with an event, instead of a retry;
- `lfcp-todo`: `sync` and `watch` exit non-zero with a message that names
  the Resource and the server;
- the Obsidian plugin: a notice, and the state in "Resource status".

Acceptance: a test for each of the three against a server that does not
host the Resource: the SDK reaches the terminal state without hanging,
`lfcp-todo` exits non-zero with the message, and the plugin shows the
notice and the status.

## POST-018 - Share and insert many tasks at once

**State:** done; released in Shared Tasks 0.3.0 (b2779e9, 876d40a,
c9a8b05, cc797dd, eeb6a99). Owner request 2026-10-07. Inside MVP 0.2
sections these commands are disabled or redirected (LFCP-02-100).
Plugin only; no protocol change.

A collaboration (Resource) already holds any number of Tasks, and one
invitation covers all of them, including Tasks added later
(SHARED-OBJECTS-PROFILE-01 §15; OBSIDIAN-ARCHITECTURE-01 §8). The plugin
only lets a user share one Task line at a time, and the collaborator
inserts each Task into a note one by one. Sharing a list or a section of a
note therefore takes one command per line on both sides.

Deliver, in the Obsidian plugin:

- **"Share selected tasks"**: shares every Task line in the editor
  selection. With no selection, it shares the Task lines under the heading
  at the cursor, down to the next heading of the same or a higher level.
  One collaboration pick for the whole batch, as "Share task under cursor"
  does, with "create a new collaboration" offered. Each Task becomes its own
  `task.create` intent and its own change. Its ref uses the configured
  placement. All refs of one note go in one `vault.process`, so lines that
  move in between are still found.
- Lines that already carry a valid ref are skipped. Lines with a blocked
  (malformed or duplicated) ref are refused. Nested Task lines are shared
  as Tasks of their own; nesting stays local presentation (§24). One
  summary notice says how many were shared, skipped and refused.
- **"Insert all tasks from collaboration"**: picks a collaboration and
  inserts, at the cursor, a projection of every live Task that this note
  does not already show, ordered by `created_at` and then Object ID. The
  notice says how many were inserted.
- A batch is capped at 200 Tasks per command. Above that, the command
  refuses before writing anything. The dialog states that everyone invited
  to the collaboration sees every Task in it.
- `docs/architecture/collaboration.md` and the user README list the new
  commands. Command names follow the Obsidian guidelines (sentence case, no
  plugin prefix).

Acceptance:

- Unit tests for the range: selection, heading at the cursor, nested
  lists, child-line and inline refs, CRLF, already shared and blocked lines.
- A live test against a local server: share three Tasks under a heading in
  vault A, then "Insert all" in vault B gives three refs. Edits then sync
  both ways.
- The existing suite stays green, and `eslint-plugin-obsidianmd` reports 0
  errors.

Live sections, where the order, the heading and new Tasks follow
automatically, are NEXT-001 and need the protocol.

## Launch track (owner-led, orchestrator assists)

### LAUNCH-001 - GitHub organization profile

Deliver: `openlfcp/.github` `profile/README.md`, the organization
description and links, and the pinned repositories.

Acceptance: the organization page explains OpenLFCP in one screen and
links the spec, the SDKs, the server, the plugin and the release notes.

### LAUNCH-002 - Marketing materials

Deliver: landing page copy, a one-pager, and a demo video or GIF of the
two-vault demo. Positioning: local-first, end-to-end encrypted, the server
cannot read your tasks.

Acceptance: every claim matches the release notes and their known
limitations.

### LAUNCH-003 - Public sync server

A public server at `wss://sync.openlfcp.org/v1/ws`.

**State:** live since 2026-10-06, as a beta. Server 0.2.0 (POST-003 and
POST-004 included) runs as the stack `openlfcp` of the owner's machine
(`devbox-asstnt: stacks/openlfcp/`, nginx with getssl in front, the image
`ghcr.io/openlfcp/lfcp-server:0.2.0`).
- A two-home `lfcp-todo` sync through it passed; the administrator is
  paired; the client IP reaches the server through nginx.
- TLS from Let's Encrypt; nginx logs rotated after 14 days; external
  monitoring by Better Stack on `/health`.
- The privacy note, terms and runbook in `docs/operations/` are final.
  Contacts: `abuse@`, `privacy@` and `security@openlfcp.org`.

Open, and done when both are recorded:
- (a) the S3 lifecycle rule that keeps backups 30 days is not applied yet
  (owner); the privacy note promises 30 days;
- (b) the restore test on the machine (`devbox-asstnt:
  stacks/openlfcp/README.md`, "Восстановить") has not been run yet.

Deliver:

- a deployment from `server: deploy/` (Caddy, `wss://`);
- a hosting policy and quotas;
- backups, monitoring and uptime checks;
- a privacy note and terms, stating the metadata the server sees;
- an abuse contact;
- the plugin settings docs on switching the default server.

Acceptance: two vaults sync through it; restore from a backup is tested;
the privacy note matches what the server stores.

### LAUNCH-004 - Website openlfcp.org

The domain is bought; there is no site yet. Hosting is TBD.

Deliver: a landing page with:
- the product promise, "Shared tasks inside your private notes";
- the two-vault demo GIF;
- two routes: Obsidian users and developers;
- links to the spec, the SDKs and the server;
- the status and the known limitations.

Acceptance: every claim on the page matches the release notes and their
known limitations; the page is reachable at `https://openlfcp.org`.

### LAUNCH-005 - The Obsidian plugin README as the trust document

Deliver: a user-facing README for `obsidian`:
- a GIF of the plugin in use;
- installing from zero, including how to get a sync server;
- what is shared, what stays local, and what the server sees;
- offline and conflict behaviour, with an example;
- the tested Obsidian versions and platforms, and how it works with the
  Tasks plugin;
- the release limitations, with only verified claims;
- support channels.

Acceptance: a new user installs and shares a first task from the README
alone; every claim in it is backed by a test, a smoke-run record or the
release notes.

### LAUNCH-006 - Visual identity

Deliver: a logo or mark that stays readable as a small GitHub avatar; one
accent colour that works in light and dark themes; the spelling
"OpenLFCP" used consistently; a minimal set of README badges.

Acceptance: the organization avatar, the website and the READMEs use the
same mark, colour and spelling.

## Next MVP planning (owner)

### NEXT-001 - Shared sections (an ordered list of Tasks)

**State:** → superseded by MVP 0.2 (ADR 0009 pending). The plan is
`BACKLOG-MVP-0.2.md`; the owner chose a new profile,
`org.openlfcp.shared-sections.v1`, over a list type inside Shared Objects
(decision P1; ADR 0009 is LFCP-02-083). Owner request 2026-10-07.

Users want to share a whole section of a note: a heading with its Tasks, in
order, where a Task one person adds appears in the other person's section by
itself. Shared Objects v1 cannot say this. `objects` is an unordered map,
nothing groups Tasks, and a heading is local presentation
(OBSIDIAN-ARCHITECTURE-01 §24). POST-018 covers the batch commands without
a protocol change. This entry is what remains.

Design questions:

- **Object model.** One option is a new object type: a standard `list`, or a
  namespaced `org.openlfcp.list` first, with a `title` and ordered
  membership. Ordered membership is either an Automerge list of Object IDs
  or a fractional position per member.
- **Conflicts.** Concurrent moves; a member that is deleted; one Task in two
  lists; a list deleted while a peer adds to it.
- **Markdown.** A ref on the heading (MARKDOWN-REFS-01 would need a `list`
  object type) and a managed block below it. Also: what happens to
  unshared lines inside the block, and how the plugin appends Tasks that
  arrive from a peer without fighting the user's edits.
- **Compatibility.** Clients that only know Tasks keep the Tasks and ignore
  the list.

Deliver first: a design note and a proposed ADR in `spec`, for an owner
decision. Then the profile change, vectors, SDK and plugin.
