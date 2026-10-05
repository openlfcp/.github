# AGENT-OPERATING-GUIDE

**Project:** OpenLFCP  
**Status:** Working Guide 0.1  
**Audience:** Orchestrator agents, coding agents, review agents, human contributors  
**Purpose:** Define how work on OpenLFCP is decomposed, where decisions belong, what artifacts are authoritative, and how agents should hand work to one another.

---

## 1. Why this guide exists

OpenLFCP spans several layers:

- protocol design;
- cryptography and wire encoding;
- CRDT application semantics;
- reusable SDKs;
- a reference server;
- Obsidian integration;
- future VS Code and other editor integrations;
- examples and interoperability tooling.

Without explicit boundaries, agents will naturally solve a local problem in the wrong layer.

Typical failure modes include:

- putting Obsidian-specific concepts into LFCP Core;
- putting Task semantics into the server;
- treating server accounts as LFCP identities;
- fixing a specification ambiguity only inside one implementation;
- requiring byte-identical Automerge output where the profile only requires behavioral interoperability;
- changing Markdown syntax to work around a CRDT problem;
- silently choosing a winner for a semantic conflict.

This guide exists to prevent those mistakes.

The core rule is:

> **Solve every problem at the lowest correct layer, and never make an upper layer authoritative over a lower-layer protocol contract.**

---

# 2. Project in one paragraph

OpenLFCP is an open local-first collaboration stack.

Users keep their local files and personal workspace. They explicitly share selected collaborative Resources or Shared Objects. Those Resources have portable identities, cryptographic authorization, encryption, local replicas, and replaceable synchronization endpoints. Servers coordinate and persist encrypted replication data but are not the semantic owners of the Resources.

The first product validates this model through shared Tasks embedded inside private Obsidian Markdown files.

---

# 3. Current first-product use case

Two people have different Obsidian vaults.

Andrey may have:

```text
Projects/Alpha/Launch.md
```

Pavel may have:

```text
Work/This Week.md
```

Both files can contain a projection of the same shared Task:

```md
- [ ] Prepare API contract
  <!-- lfcp-ref: lfcp1:RESOURCE#task:OBJECT -->
```

The surrounding Markdown remains private and unrelated.

When Pavel completes the Task:

```md
- [x] Prepare API contract
  <!-- lfcp-ref: ... -->
```

the shared CRDT state changes and Andrey's local projection updates.

The Markdown files themselves are not shared.

This is the initial product experiment.

---

# 4. Source-of-truth hierarchy

Agents MUST determine which artifact governs the task before changing code.

The hierarchy is:

```text
Protocol architecture
        ↓
LFCP Wire specification
        ↓
LFCP Wire test vectors
        ↓
Application Profile specification
        ↓
Application Profile test vectors
        ↓
Client architecture documents
        ↓
Implementation code
        ↓
UI behavior
```

More concretely:

## 4.1 LFCP network, security, routing, identity, transport

Authoritative artifacts:

```text
LFCP-WIRE-01.md
LFCP-TEST-VECTORS-01.*
```

These govern:

- Resource identity;
- Principal identity;
- cryptography;
- COSE;
- CBOR;
- Control Plane;
- Data Plane;
- Control Coordinator;
- routing;
- invitations at protocol level;
- key packages;
- ownership transfer;
- sync messages;
- WebSocket framing;
- server migration;
- snapshots at LFCP level.

An implementation MUST NOT contradict these documents.

## 4.2 Shared Object and Task semantics

Authoritative artifacts:

```text
SHARED-OBJECTS-PROFILE-01.md
SHARED-OBJECTS-TEST-VECTORS-01.*
```

These govern:

- Automerge binding;
- Shared Object model;
- Task schema;
- Object IDs;
- actor derivation;
- conflict semantics;
- add-wins collections;
- tombstones;
- intents;
- snapshot framing inside the application profile;
- unknown-field preservation.

LFCP Wire itself does not know what a Task means.

## 4.3 Obsidian behavior

Authoritative artifacts:

```text
MARKDOWN-REFS-01.md
OBSIDIAN-ARCHITECTURE-01.md
```

This governs:

- Markdown projections;
- plugin responsibilities;
- Markdown-to-CRDT flow;
- CRDT-to-Markdown flow;
- mutation guards;
- local projection index;
- Resource Explorer;
- commands;
- compatibility with Obsidian Tasks;
- local storage adapter;
- conflict UI;
- vault behavior.

Obsidian behavior MUST respect the protocol and Shared Objects Profile.

## 4.4 Test vectors versus prose

If a byte-exact normative test vector and prose disagree:

1. do not silently choose one;
2. identify the inconsistency;
3. open a specification issue;
4. if the specification is still a Working Draft, patch the canonical document in place and record the change in Git;
5. if the specification is already Stable, determine whether an errata or new version is required;
6. update vectors and implementations together.

Do not make one implementation the de facto specification by accident.

---

## 4.5 Markdown projection binding

Authoritative artifact:

```text
MARKDOWN-REFS-01.md
```

This governs the portable `lfcp-ref` grammar and placement. Task projections support two semantically equivalent forms: inline and immediate child-line. Parsers MUST support both. Obsidian SHOULD emit child-line by default for compatibility with suffix-sensitive task plugins, while other clients MAY prefer inline when safe. Editor architecture documents and examples MUST defer to this grammar.

# 4.6 Current execution backlog

The authoritative implementation sequence for MVP 0.1 is:

```text
BACKLOG-MVP-0.1.md
```

Agents MUST use its current issue numbers and dependencies. The earlier `LFCP-001...050` draft and temporary `BACKLOG-MVP-0.1-PATCH.md` are superseded.

The backlog is planning authority, but it does not override normative protocol/profile specifications. If a backlog acceptance criterion conflicts with a normative spec, raise the inconsistency rather than coding to the backlog blindly.

# 4.7 MVP 0.1 baseline

The canonical document set for MVP 0.1 implementation is listed in:

```text
spec: MVP-0.1-BASELINE.md        (at spec tag mvp-0.1-baseline.3; mvp-0.1-baseline and mvp-0.1-baseline.2 are superseded)
```

It names every normative document, vector suite, generator, CDDL file and schema that implementations build against. The protocol decisions applied to the Working Drafts for this baseline are recorded in `spec: adr/0001-mvp-0.1-protocol-decisions.md` and `spec: adr/0002-mvp-0.1-protocol-decisions-2.md`.

The baseline is an implementation baseline only. It is not a Stable publication of `LFCP-WIRE-01`, and it is not a full-conformance claim. The documents remain Working Drafts. A later approved correction produces a new tag (for example `mvp-0.1-baseline.4`); an existing tag is never moved.

# 5. Repository model

The intended GitHub organization is:

```text
github.com/openlfcp
```

Logical repositories:

```text
openlfcp/spec
openlfcp/sdk-ts
openlfcp/sdk-rs
openlfcp/server
openlfcp/obsidian
openlfcp/vscode
openlfcp/examples
```

Later:

```text
openlfcp/interop
openlfcp/cli
openlfcp/inspector
openlfcp/website
```

The boundaries matter more than the exact initial repository count.

---

# 6. Repository responsibilities

## 6.1 `openlfcp/spec`

Contains normative documents and interoperability fixtures.

Expected contents:

```text
wire/
profiles/
test-vectors/
registries/
rfcs/
adr/
```

Must NOT contain production application logic.

## 6.2 `openlfcp/sdk-ts`

Reusable TypeScript implementation.

Contains:

```text
LFCP core
wire codec
crypto adapters
Control Plane validation
client sync engine
routing
storage interfaces
Shared Objects Profile implementation
```

Must NOT depend on Obsidian.

## 6.3 `openlfcp/sdk-rs`

Independent Rust implementation.

Its purpose is both practical and architectural.

It proves that LFCP is an interoperable protocol rather than a TypeScript convention.

## 6.4 `openlfcp/server`

Reference LFCP server.

It is implemented in TypeScript for Node.js and does not depend on `sdk-rs`, which remains the independent Rust interoperability implementation. It MUST remain application-agnostic.

It MUST NOT understand:

```text
Markdown
Obsidian Tasks
Task status
Automerge object semantics
```

It stores and coordinates LFCP objects according to Wire.

## 6.5 `openlfcp/obsidian`

Obsidian adapter and product UI.

It consumes:

```text
sdk-ts
Shared Objects Profile
Markdown ref format
```

It owns:

```text
Markdown scanning
projection engine
CodeMirror integration
commands
Resource Explorer
plugin settings
editor conflict presentation
```

## 6.6 `openlfcp/vscode`

Future editor adapter.

It should reuse the same protocol, Shared Objects Profile, and Markdown reference format.

## 6.7 `openlfcp/examples`

Minimal understandable examples.

Expected examples:

```text
shared-counter
todo-web
todo-cli
offline-conflict
multi-server
server-migration
```

These are part of protocol education and interoperability testing.

---

# 7. Layer model

Every task should be assigned to one primary layer.

```text
L0  Specification
L1  LFCP Core
L2  Application Profile
L3  Reusable Client SDK
L4  Reference Server
L5  Editor Adapter
L6  Product UI
L7  Examples / tooling
```

Agents should avoid solving a problem by crossing layers unnecessarily.

---

# 8. Task routing rules for the orchestrator

The orchestrator should classify every task before assignment.

## 8.1 Send to Protocol / Spec agent when the task concerns

- wire message format;
- cryptographic encoding;
- Resource IDs;
- Principal IDs;
- authorization;
- Control Chain;
- routing;
- invitations at protocol level;
- ownership transfer;
- server migration;
- snapshot envelope;
- interoperability ambiguity;
- a missing normative rule.

Expected output:

```text
spec change
errata proposal
test-vector update
compatibility analysis
```

## 8.2 Send to Shared Objects agent when the task concerns

- Task schema;
- Task lifecycle;
- object identity;
- Automerge document structure;
- CRDT conflict behavior;
- tags;
- assignees;
- tombstones;
- intents;
- object validation;
- application-level snapshot content.

Expected output:

```text
profile code
profile tests
profile spec proposal if necessary
```

## 8.3 Send to LFCP SDK agent when the task concerns

- CBOR / COSE implementation;
- message codec;
- WebSocket session;
- local replica manager;
- Have Vector sync;
- route manager;
- LFCP persistence interfaces;
- Control Chain verification;
- generic invitation processing.

Expected output:

```text
reusable library code
unit tests
interop tests
```

## 8.4 Send to Server agent when the task concerns

- LFCP WebSocket endpoint;
- resource hosting;
- object persistence;
- Control Coordinator CAS;
- snapshots;
- Key Package storage;
- invite claim coordination;
- presence;
- hosting account/quota;
- self-hosted setup UI.

Expected output:

```text
server code
migration/storage tests
protocol conformance tests
```

The server agent MUST NOT implement Task semantics.

## 8.5 Send to Obsidian agent when the task concerns

- Markdown parsing;
- Markdown refs;
- projection index;
- editor commands;
- Task line rewriting;
- Tasks plugin compatibility;
- Obsidian settings;
- CodeMirror decorations;
- Resource Explorer;
- vault scanning.

Expected output:

```text
plugin code
fixtures
editor integration tests
```

## 8.6 Send to Interop / QA agent when the task concerns

- official vectors;
- independent implementation comparison;
- malformed input;
- fuzz cases;
- cross-language behavior;
- compatibility matrix;
- regression corpus.

---

# 9. Mandatory reading set by task type

Agents should not read every project document by default.

Read the smallest authoritative set.

## Protocol task

Read:

```text
LFCP-WIRE-01.md
LFCP-TEST-VECTORS-01.md
MVP-0.1-PROTOCOL-SCOPE.md  # when implementing the MVP subset
```

## Shared Objects task

Read:

```text
SHARED-OBJECTS-PROFILE-01.md
SHARED-OBJECTS-TEST-VECTORS-01.md
```

Read Wire only when LFCP framing matters.

## Obsidian task

Read:

```text
MARKDOWN-REFS-01.md
OBSIDIAN-ARCHITECTURE-01.md
SHARED-OBJECTS-PROFILE-01.md
```

Read Wire only when dealing directly with LFCP connectivity, identity, routes, or storage.

## Server task

Read:

```text
LFCP-WIRE-01.md
LFCP-TEST-VECTORS-01.md
```

Do not require the Obsidian architecture document.

---

# 10. Specification gap protocol

When an agent finds a behavior not fully defined:

DO NOT:

```text
pick a convenient behavior
implement it
document it only in code
```

Instead:

1. state the ambiguity explicitly;
2. identify affected artifacts;
3. present the smallest normative options;
4. recommend one;
5. for a Working Draft, create or request a direct canonical spec patch; for Stable specs, create or request errata/RFC/versioning as appropriate;
6. add a test vector;
7. only then make the implementation depend on it.

A specification ambiguity discovered by implementation is useful output.

Do not hide it.

---

# 11. Implementation bug versus specification bug

Use this decision process:

```text
Does the specification clearly define the expected behavior?
        │
       yes
        │
        ▼
implementation bug

        no
        │
        ▼
Can existing normative invariants determine one behavior?
        │
       yes
        │
        ▼
document reasoning + implement + add test

        no
        │
        ▼
specification gap
```

Agents should not label every difficult implementation issue as a protocol ambiguity.

---

# 12. Test-first rules

Every normative behavior should have the strongest feasible test.

Priority:

```text
1. byte-exact vector
2. cross-implementation interoperability test
3. deterministic state assertion
4. unit test
5. UI integration test
```

The right test type depends on the layer.

---

# 13. Byte-exact versus behavioral interoperability

This distinction is critical.

## Byte-exact cases

Examples:

- actor ID derivation;
- Principal ID derivation;
- deterministic CBOR;
- canonical COSE;
- LFCP message encoding where normative;
- hashes;
- signed object IDs;
- profile framing.

Expected result:

```text
same input
→ exact same bytes
```

## Behavioral interoperability cases

Automerge may allow different valid binary histories that converge to equivalent state.

Expected requirement:

```text
implementation A change
→ B accepts it

implementation B change
→ A accepts it

same valid change set
→ same logical state
→ same conflicts
```

Agents MUST NOT invent byte equality requirements that the profile does not define.

---

# 14. Security rules

Agents working on security-sensitive code MUST preserve these boundaries.

Never log:

```text
private signing keys
X25519 private keys
DEKs
invitation fragment secrets
plaintext secret-store contents
hosting passwords
```

Resource authorization is client-verifiable.

The server is never the sole authorization oracle.

Hosting credentials and LFCP capabilities are different concepts.

Do not collapse:

```text
server user
LFCP Principal
Resource owner
```

into one database entity.

---

# 15. Data privacy invariant

The most important Obsidian privacy test is:

> Sharing a Task MUST NOT upload the host Markdown document.

Any implementation path that requires sending surrounding Markdown to LFCP infrastructure violates the initial architecture unless a whole-document collaborative mode was explicitly enabled.

Agents should create regression tests for this property.

---

# 16. Resource boundary rule

An LFCP Resource is a collaboration/security boundary.

Objects inside one Resource normally share:

```text
participants
routes
encryption epoch
authorization context
```

Do not create one Resource per Task by default.

Create a new Resource when there is a distinct:

```text
participant set
ownership boundary
privacy boundary
hosting policy
collaboration context
```

---

# 17. Server independence rule

Never encode the sync server into permanent application identity.

Correct:

```text
Resource ID
+
Route Manifest
```

Incorrect:

```text
Resource identity = server URL + document path
```

Server migration MUST preserve Resource IDs and Shared Object references.

---

# 18. Shared Object identity rule

A Shared Object must remain the same object when:

- a Markdown file is renamed;
- a note moves folders;
- it is inserted in a second note;
- a user switches from Obsidian to VS Code;
- the LFCP Resource migrates servers.

File location is projection metadata, not object identity.

---

# 19. Markdown projection rules

The Obsidian plugin should treat Markdown as an editable projection.

A remote change should result in the smallest safe local Markdown diff.

Do not regenerate entire files.

Do not delete unknown local formatting.

Do not rewrite unrelated note content.

Projection code should distinguish:

```text
shared semantic fields
```

from:

```text
local presentation
```

---

# 20. Feedback loop prevention

All editor adapters need a mutation guard.

Without it:

```text
remote change
→ write Markdown
→ file watcher fires
→ treated as local user edit
→ duplicate CRDT operation
```

Generated projection mutations must be recognizable as generated mutations.

The same principle will apply to VS Code and other editors.

---

# 21. Conflict rules

CRDT convergence is not permission to hide semantic conflict.

For important scalar fields such as:

```text
status
title
lifecycle
```

concurrent incompatible values remain semantically conflicted.

The UI may choose one provisional rendering, but must expose the unresolved alternatives.

Conflict resolution is a new causal write based on merged state.

Do not implement arbitrary "last writer wins" for fields whose profile semantics preserve conflicts.

---

# 22. Deletion rule

Shared Objects v1 uses tombstones.

```text
lifecycle = deleted
```

Do not physically remove an object from the CRDT merely because it is currently deleted.

Offline replicas may still contain relevant concurrent changes.

Physical garbage collection requires a future explicit protocol/profile rule.

---

# 23. Unknown-data preservation

A conforming client should preserve:

```text
unknown object fields
unknown extension namespaces
unknown supported-by-CRDT object types
```

whenever it can safely do so.

An older client must not destroy future data merely because it cannot render it.

This is necessary for long-lived local-first data.

---

# 24. Minimalism rule

Do not add infrastructure because it might be useful later.

For the first reference server, prefer:

```text
single process
SQLite
filesystem
WebSocket
```

Avoid mandatory:

```text
Kafka
Redis
PostgreSQL cluster
S3
service mesh
```

until measurements or concrete requirements justify them.

The architecture should permit scaling later without requiring it now.

---

# 25. Current implementation priorities

Priority order:

## P0: Protocol conformance

- wire codec;
- cryptographic objects;
- vectors;
- TypeScript implementation;
- Rust independent verification.

## P1: Minimal server

- WebSocket connection;
- Resource hosting;
- Control storage/coordinator;
- Data Unit storage;
- snapshots;
- key packages;
- sync.

## P2: Shared Objects implementation

- Automerge profile;
- Task;
- intents;
- conflicts;
- tombstones;
- sets;
- snapshot behavior.

## P3: Obsidian local projection

- Task parsing;
- refs;
- projection index;
- Markdown ↔ Shared Object updates;
- mutation guard.

## P4: Two-user end-to-end

- Resource creation;
- invitation;
- join;
- live sync;
- offline sync;
- conflict resolution.

## P5: Federation demo

- multiple servers;
- independent Resource failure;
- server migration.

---

# 26. First product milestone

The first meaningful milestone is not "plugin installs."

It is this end-to-end scenario:

```text
Vault A
Vault B
LFCP Server
```

1. User A creates a Resource.
2. User A shares a local Task.
3. User B joins via invitation.
4. User B inserts the same Task into another Markdown file.
5. User B edits the Task.
6. User A's projection updates.
7. Both go offline or partition.
8. Both make changes.
9. They reconnect.
10. Compatible changes merge.
11. Semantic conflicts are surfaced.
12. User resolves conflict.
13. Both converge.
14. Surrounding private Markdown is never uploaded.

Until this scenario works reliably, avoid spending significant time on secondary UI polish.

---

# 27. Orchestrator workflow

For every task, the orchestrator should follow:

```text
1. Classify layer
2. Identify authoritative artifacts
3. Define acceptance criteria
4. Assign smallest capable agent
5. Require tests
6. Review boundary violations
7. Record spec gaps separately
8. Merge only with handoff notes
```

---

# 28. Orchestrator task template

Recommended task brief:

```text
Goal:
What observable capability should exist?

Layer:
Spec / Core / Profile / Server / Obsidian / Interop

Read first:
Exact source-of-truth artifacts.

Do not modify:
Explicit neighboring layers.

Acceptance criteria:
Concrete tests and behavior.

Interop requirement:
Byte-exact or behavioral.

Known constraints:
Offline, privacy, compatibility, etc.

Expected deliverables:
Code / tests / spec proposal / diagnostics.
```

---

# 29. Agent handoff format

Every agent completing nontrivial work should return:

```text
Summary
What was changed.

Files
Exact files changed/created.

Behavior
What now works.

Tests
What was run and result.

Spec compliance
Which normative sections were implemented.

Open issues
Anything unresolved.

Spec gaps
Any ambiguities discovered.

Follow-up
Smallest logical next task.
```

Do not return only:

```text
Done.
```

---

# 30. Review checklist

A reviewer should ask:

### Architecture

- Is this implemented at the correct layer?
- Did editor concerns leak into the protocol?
- Did Task semantics leak into the server?
- Did hosting account logic become Resource authorization?

### Interoperability

- Are normative encodings covered by vectors?
- Could an independent implementation reproduce the behavior?
- Does the code assume a private undocumented convention?

### Local-first

- Does offline work continue where expected?
- Is a central service unnecessarily required?
- Can data identity survive server migration?

### Privacy

- Is unrelated local content uploaded?
- Are secrets logged or serialized into Markdown?

### CRDT

- Are meaningful conflicts preserved?
- Are unknown fields preserved?
- Is deletion safely tombstoned?

### Scope

- Did the agent introduce unnecessary future infrastructure?

---

# 31. Naming conventions

Normative protocol artifacts use uppercase names:

```text
LFCP-WIRE-01.md
LFCP-TEST-VECTORS-01.md
SHARED-OBJECTS-PROFILE-01.md
```

New incompatible protocol/profile generations use a new identifier.

Working Draft corrections are incorporated directly into the canonical document and tracked by Git. After Stable publication, compatible corrections use an errata revision when appropriate.

Do not silently rewrite a published Stable specification.

---

# 32. RFC versus errata

For a **Working Draft**, do not create a separate errata file. Patch the canonical draft and its vectors directly.

After a specification is **Stable**, use **errata** when:

- wording is ambiguous;
- canonical encoding needs clarification;
- the intended behavior is unchanged;
- existing valid implementation direction remains compatible.

Use **new profile/version/RFC** when:

- semantics change incompatibly;
- wire representation changes incompatibly;
- conflict policy changes;
- identity rules change;
- old clients would interpret valid new data incorrectly.

---

# 33. Examples are normative teaching tools, not normative protocol

Examples should be simple enough to read.

But implementation agents MUST NOT infer protocol rules solely from examples when a normative specification exists.

If an example contradicts a spec, fix the example.

---

# 34. Human-readable code preference

The reference implementations should optimize for:

```text
clarity
auditability
interop correctness
small dependency surface
```

before micro-optimization.

Protocol and crypto code should be boring in the best possible way.

Avoid clever abstractions that obscure the exact bytes or state transitions.

---

# 35. Error handling philosophy

Do not silently repair security-critical invalid state.

Differentiate:

```text
malformed input
unauthorized input
unsupported input
temporarily unavailable input
semantically conflicted state
profile-invalid object
```

Preserve enough diagnostics for tooling and interop debugging.

---

# 36. Observability

Reference clients and servers should expose machine-readable diagnostics for:

```text
Resource ID
Control Head
Data Epoch
Have Vector
routes
session state
sync state
object IDs
error codes
```

without exposing secret material.

This will later power `openlfcp/inspector`.

---

# 37. Compatibility philosophy

OpenLFCP should permit applications and infrastructure to evolve independently.

A Resource should outlive:

```text
one server
one editor
one vendor
one UI
```

Therefore avoid coupling identity to transient implementation details.

---

# 38. Things agents should explicitly NOT do

Unless a task specifically changes architecture, agents should not:

- upload whole Markdown files for a shared Task;
- make server URL part of Resource identity;
- require an OpenLFCP cloud account;
- use server database rows as the only ACL source;
- implement Task merge semantics in the LFCP server;
- replace conflicts with timestamp-based LWW;
- physically delete Shared Objects in v1;
- put private keys in Markdown/frontmatter;
- invent a new crypto primitive;
- change normative encoding without updating vectors;
- make Obsidian APIs a dependency of `sdk-ts`;
- create one WebSocket per Task;
- create one LFCP Resource per Task by default;
- rewrite entire notes for a one-field remote update;
- treat unavailable server as making the entire vault unavailable.

---

# 39. Decision heuristic

When uncertain, ask:

> Does this decision belong to identity, transport, authorization, application semantics, projection, or UI?

Then put it there.

Second question:

> Would VS Code need the same behavior?

If yes, it probably does not belong only in the Obsidian plugin.

Third question:

> Would a server need to know this if all payloads were encrypted?

If no, it probably does not belong in the server.

Fourth question:

> Does changing server infrastructure change the identity of the user's data?

If yes, the design is probably wrong for OpenLFCP.

---

# 40. Agent mental model

The simplest useful mental model is:

```text
PERSONAL LOCAL WORLD
        │
        │ contains references
        ▼
PORTABLE SHARED OBJECTS
        │
        │ grouped into Resources
        ▼
LOCAL CRDT REPLICAS
        │
        │ encrypted replication
        ▼
REPLACEABLE LFCP SERVERS
```

Applications project shared objects into whatever local workflow is natural.

Obsidian Markdown is the first projection surface, not the final architecture.

---

# 41. Final operating principle

Every contribution should reinforce this property:

> **The collaboration relationship belongs to the participants and their portable data, not to a particular editor, cloud workspace, or synchronization server.**

If a proposed implementation makes that statement less true, it requires architectural scrutiny before acceptance.
