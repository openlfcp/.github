# MVP-0.1-PROTOCOL-SCOPE

**Project:** OpenLFCP  
**Status:** Implementation Scope 0.1  
**Wire specification:** `LFCP-WIRE-01` Working Draft  
**Revision date:** 2026-10-05

## 1. Decision

MVP 0.1 is a **secure LFCP vertical slice**, not a plaintext CRDT synchronization demo.

The MVP MUST implement the cryptographic and Control Plane foundations required for the first two-user Obsidian scenario.

MVP 0.1 does **not** yet claim complete `LFCP-WIRE-01` conformance. Features explicitly deferred below may remain unimplemented until the next milestone.

This distinction prevents two opposite errors:

- silently omitting security while claiming LFCP;
- expanding the first MVP into every future LFCP feature at once.

---

## 2. MVP topology

The required initial topology is:

```text
Client A
   \
    \          one LFCP Resource
     +------ Reference Server
    /
   /
Client B
```

Assumptions for MVP 0.1:

- one current Control Coordinator per Resource;
- one primary sync endpoint is sufficient;
- clients remain local-first and may edit offline;
- Data Plane is encrypted end-to-end;
- server stores opaque encrypted application payloads;
- link invitation joins a second Principal;
- restart durability is required;
- reconnection and anti-entropy are required.

---

## 3. Wire features REQUIRED in MVP 0.1

### 3.1 Binary and cryptographic foundation

Required:

- deterministic CBOR;
- SHA-256;
- Resource IDs;
- Principal descriptors and Principal IDs;
- Ed25519 signing;
- X25519 key agreement;
- HKDF-SHA256;
- ChaCha20-Poly1305;
- HPKE Base mode required by WIRE-01;
- canonical untagged COSE_Sign1;
- exact signed-object hashing rules.

There is no plaintext Data Unit mode in MVP 0.1.

### 3.2 Resource encryption

Required:

- Resource DEK generation;
- DEK commitment;
- Data Epoch 0;
- per-actor Data Plane key derivation;
- nonce construction from actor sequence;
- Data Unit AEAD AAD;
- encrypted Data Unit payloads.

### 3.3 Signed Data Units

Required:

- actor sequence persistence;
- previous-actor-unit hash chain;
- COSE signature;
- Data Unit ID;
- signature verification;
- decryption;
- Data Profile validation hook;
- duplicate handling;
- equivocation detection for `(resource, actor, seq)`.

### 3.4 Minimal Control Plane

Required:

- Genesis Record;
- linear Control Chain;
- Control Sequence;
- previous Control Record hash;
- Control Head persistence;
- signed Control Records;
- fork detection;
- Control Coordinator compare-and-swap;
- capability evaluation.

### 3.5 Capabilities required for first collaboration

Required:

- owner implicit authority;
- `data/read`;
- `data/write`;
- `capability/grant`;
- `capability/revoke`;
- `key/distribute`;
- `key/rotate`;
- `invite/claim`.

The implementation MAY internally support the remaining standard ability codes, but UI for them is not required in MVP 0.1.

### 3.6 Invitations

Required:

- Invitation Principal;
- Capability Grant to invitation Principal;
- one-time `CAPABILITY_CLAIM` through the Control Coordinator;
- canonical `lfcp://join/...` parsing;
- invitation fragment secret handling;
- claimant capability creation;
- Key Package for invitation Principal;
- Key Package for final claimant where required by the join flow.

### 3.7 Key Packages

Required:

- HPKE encryption of DEK;
- HPKE decryption;
- exact `info` and AAD from WIRE-01;
- Key Package signature;
- authorization validation;
- DEK commitment verification.

### 3.8 Revocation and epoch rotation

Required before MVP 0.1 is considered complete:

- Capability Revocation;
- new Data Epoch;
- new DEK commitment;
- final previous-epoch frontier;
- strict stale-epoch cutoff;
- Key Package redistribution to remaining readers;
- quarantine of stale offline writes beyond cutoff.

A polished member-management UI is not required. Protocol/library tests and one end-to-end revocation scenario are required.

### 3.9 Session handshake

Required:

```text
HELLO
CHALLENGE
AUTH
READY
```

The server must authenticate the connecting Principal according to WIRE-01.

A hosting/account credential may be omitted in local/self-hosted MVP mode.

### 3.10 Resource session

Required:

```text
RESOURCE_HOST
RESOURCE_HOSTED
RESOURCE_OPEN
RESOURCE_OPENED
RESOURCE_CLOSE
```

### 3.11 Control synchronization

Required:

```text
CONTROL_HAVE
CONTROL_GET
CONTROL_BATCH
CONTROL_PUT
```

Clients independently validate the chain.

### 3.12 Data synchronization

Required:

```text
DATA_HAVE
DATA_GET
DATA_BATCH
DATA_PUT
```

Required behavior:

- Have Vector contiguous ranges;
- extra ranges for holes;
- anti-entropy catch-up;
- at-least-once delivery tolerance;
- deduplication;
- reconnect synchronization.

### 3.13 Key Package transport

Required:

```text
KEY_PACKAGE_GET
KEY_PACKAGE_BATCH
KEY_PACKAGE_PUT
```

### 3.14 Snapshots

Required before MVP 0.1 is declared complete:

```text
SNAPSHOT_GET
SNAPSHOT
SNAPSHOT_PUT
```

Required behavior:

- canonical frontier;
- exact Snapshot AAD;
- derived Snapshot key;
- ChaCha20-Poly1305 encryption;
- COSE signature;
- snapshot load plus post-frontier Data Units.

The first development slices may run without snapshots, but snapshots are part of the MVP 0.1 completion gate.

### 3.15 Errors and state machines

Required:

- `ACK` / `NACK` where specified;
- `ERROR` and relevant error codes, as LFCP-WIRE-01 assigns them to each rejection (decisions recorded in `spec: adr/0001-mvp-0.1-protocol-decisions.md`);
- client-local rejection of Data Units that fail AEAD authentication and of Key Packages that do not open or do not match their commitment; these have no wire error code;
- client connection state machine;
- server session state machine;
- per-Resource sync state machine;
- deterministic offline/reconnect behavior.

---

## 4. Explicitly DEFERRED from MVP 0.1

The following WIRE-01 features are not required for the first secure Obsidian MVP:

### Ownership transfer

Deferred: creating and driving a transfer (UI and flow):

```text
owner.transfer-offer
owner.transfer-accept
OWNER_TRANSFER_COMMIT
```

The creator remains owner in MVP 0.1 as far as MVP clients are concerned. Verification is NOT deferred: an MVP 0.1 implementation MUST validate a received `OWNER_TRANSFER_COMMIT` and its offer and acceptance as LFCP-WIRE-01 §23 specifies, and apply the resulting owner change (project-owner decision of 2026-10-05, `spec: adr/0002-mvp-0.1-protocol-decisions-2.md`).

### Coordinator recovery

Deferred:

```text
COORDINATOR_RECOVERY
```

If the single MVP coordinator is permanently lost, manual recovery/recreation is acceptable during this milestone.

An MVP 0.1 implementation MUST refuse a Control Chain that contains a `COORDINATOR_RECOVERY` (type 7) record, with `PROTOCOL_UNSUPPORTED` (DV1).

### Resource tombstone

Deferred:

```text
RESOURCE_TOMBSTONE
```

Shared Object tombstones remain part of the Shared Objects Profile and are unrelated to this deferral.

An MVP 0.1 implementation MUST refuse a Control Chain that contains a `RESOURCE_TOMBSTONE` (type 8) record, with `PROTOCOL_UNSUPPORTED` (DV1).

### Route migration and multi-home routing

Deferred:

- `ROUTE_UPDATE` mutation UI;
- server migration flow;
- multiple active endpoints;
- anti-rollback route recovery beyond initial route state.

Genesis still contains the initial endpoint and coordinator.

### Server federation

Deferred:

- server-to-server replication;
- active-active hosting;
- multi-home reconciliation.

### Presence

Deferred.

Presence is optional in WIRE-01 and is not needed to validate shared Tasks.

### Public hosting accounts

Deferred:

- email registration;
- billing;
- quotas beyond simple local policy;
- OAuth/passkeys for hosted service UX.

The LFCP cryptographic handshake remains required.

### Direct P2P transports

Deferred.

WebSocket to the reference LFCP server is the only required transport for MVP 0.1.

---

## 5. What MVP 0.1 may claim

Before deferred features are implemented, software SHOULD say:

```text
Implements the OpenLFCP MVP 0.1 subset of LFCP-WIRE-01.
```

It SHOULD NOT claim:

```text
Fully conforming LFCP-WIRE-01 implementation.
```

Full WIRE-01 conformance is a later milestone.

The exact documents, vectors and schemas that make up the MVP 0.1 baseline are listed in `spec: MVP-0.1-BASELINE.md` at the current `spec` baseline tag, `mvp-0.1-baseline.2` (the manifest names the current tag).

---

## 6. MVP security invariant

The server must never need Shared Objects plaintext to perform normal sync.

For every application Data Unit in the two-user end-to-end demo:

```text
Shared Objects change
      ↓
profile framing
      ↓
ChaCha20-Poly1305 encryption
      ↓
signed Data Unit
      ↓
server stores/forwards opaque bytes
```

A test MUST demonstrate that known plaintext from a Task is not present in the server's stored Data Unit ciphertext representation.

---

## 7. MVP Control Plane invariant

A client MUST NOT accept a Data Unit merely because the server sent it.

Before merge, the client validates:

```text
signature
actor identity
data/write capability at referenced Control Head
Control Chain membership
Data Epoch
cutoff if epoch is closed
AEAD authentication
Data Profile payload
```

The server is a synchronization peer, not the root of trust.

---

## 8. MVP completion gate

MVP 0.1 is complete when automated tests demonstrate:

1. two independently initialized clients create/load Principals;
2. one client creates a Resource with Genesis and DEK epoch 0;
3. invitation Principal flow authorizes the second client;
4. second client obtains the DEK through HPKE Key Package flow;
5. both connect through `HELLO → CHALLENGE → AUTH → READY`;
6. shared Task changes travel only inside encrypted, signed Data Units;
7. Have Vector catch-up works after disconnection;
8. server restart preserves Control/Data/Key Package state;
9. client restart preserves actor sequence and local replica safety;
10. concurrent Shared Objects changes converge according to the profile;
11. semantic conflicts remain visible;
12. capability revocation + Data Epoch rotation blocks automatic acceptance of post-cutoff stale writes;
13. Snapshot publish/load plus post-frontier catch-up works;
14. private surrounding Markdown never enters LFCP payloads.
