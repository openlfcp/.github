# LFCP-WIRE-01 features deferred from MVP 0.1

**Status:** draft for LFCP-072, not published. The owner decides.
**Baseline:** `spec: mvp-0.1-baseline.8` (da3977f).

MVP 0.1 implements the OpenLFCP MVP 0.1 subset of LFCP-WIRE-01, not full
conformance (`MVP-0.1-PROTOCOL-SCOPE.md` §1, §5). This list is everything
WIRE-01 or the profiles describe that MVP 0.1 software does not implement,
or implements only partly, so that nobody mistakes it for an omission. It
comes from three sources:
- `MVP-0.1-PROTOCOL-SCOPE.md` §4;
- the spec's deferred markers (WIRE-01 Part XXXI, §108; SHARED-OBJECTS-PROFILE-01);
- what the MVP repositories refuse or leave out.

## 1. Deferred by the MVP scope

| Feature | WIRE-01 | MVP 0.1 behavior |
| --- | --- | --- |
| Ownership transfer: creating and driving offer, accept and commit | §23, §76 | No UI or flow creates a transfer. A received `OWNER_TRANSFER_COMMIT` is verified and applied (not deferred, ADR 0002). |
| Coordinator recovery (`COORDINATOR_RECOVERY`, type 7) | §22, §78 | A chain containing it is refused with `PROTOCOL_UNSUPPORTED` (DV1). A lost coordinator is recovered by hand. |
| Resource tombstone (`RESOURCE_TOMBSTONE`, type 8) | §24 | A chain containing it is refused with `PROTOCOL_UNSUPPORTED` (DV1). Shared Object tombstones (`lifecycle = deleted`) are unaffected. |
| Route migration and multi-home routing | §20 | One endpoint and one coordinator from Genesis. No `ROUTE_UPDATE` UI, no server migration flow, no multiple active endpoints. Received route updates are validated. |
| Server federation | — | No server-to-server replication or active-active hosting. |
| Mirror seeding | §46 | The reference server answers client `CONTROL_BATCH`, `DATA_BATCH`, `KEY_PACKAGE_BATCH` and `SNAPSHOT` with `NACK(PROTOCOL_UNSUPPORTED)`. |
| Presence | §58 | Not implemented. Optional in WIRE-01. |
| Public hosting accounts | §36, §39 | No registration, billing, OAuth or passkeys. The hosting credential is opaque server policy; the self-hosted server accepts any authenticated Principal. The LFCP handshake is always required. |
| Direct P2P transports | Part VII | WebSocket to an LFCP server is the only transport. |

## 2. Deferred by WIRE-01 itself (Part XXXI, §108)

These are future extensions, not MVP gaps:

- multi-device root identity: one human identity with revocable device
  Principals (§108.1);
- multi-owner governance: N-of-M, organization keys, threshold
  cryptography (§108.2);
- MLS group key management in place of per-recipient HPKE Key Packages
  (§108.3);
- attachments and large binary blobs (§108.4);
- public identity discovery (handles that resolve to Principal
  Descriptors) (§108.5);
- privacy transports: metadata hiding, onion routing, PIR (§108.6);
- owner recovery (a future threshold or recovery extension).

## 3. Deferred by the Shared Objects profile

- Physically removing tombstoned objects (outside profile version 1).
- Relationships between objects, until companion specifications define
  them.
- Change batching: version 1 carries exactly one Automerge change per Data
  Unit (§12).

## 4. Partial in MVP 0.1 software

| Area | What is not there | Where |
| --- | --- | --- |
| Invitation URI codec in sdk-rs | sdk-rs checks the URI's components but has no `lfcp://join` parser or writer. The `invite_uri_*` validation vectors are deferred there, with this reason. | sdk-rs |
| Capability UI | Only the Read and Read + Write invitation presets have UI. The other abilities exist in the SDKs but have no UI. Revocation and key rotation run in the SDKs and tests, without member-management UI (scope §3.8). | obsidian |
| Snapshots in the Obsidian plugin | The plugin loads Snapshots but never publishes one. | obsidian |
| Mobile | The plugin keeps mobile portability boundaries, but iOS and Android are not tested (LFCP-068). | obsidian |
| Invitation sharing | No QR code or share sheet; copy only. | obsidian |
| Deployment | The Docker deployment (`server: deploy/`) is written but not yet verified end to end. | server |

## 5. What software may say

Every MVP 0.1 repository says, in its README:

> Implements the OpenLFCP MVP 0.1 subset of LFCP-WIRE-01 at
> `mvp-0.1-baseline.8`, not every deferred WIRE-01 feature. It does not
> claim full LFCP-WIRE-01 conformance.

The wording per repository is in
[readme-scope-statements.md](readme-scope-statements.md).
