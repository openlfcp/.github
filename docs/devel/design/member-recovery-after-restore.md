# Member recovery after a server restore (LFCP-02-106)

**Status:** design note for sdk-ts (implementation: LFCP-02-106) and the
Obsidian plugin. **Date:** 2026-10-08. **Base:** LFCP-WIRE-01 at
`mvp-0.2-baseline.1`; server 0.3.0; ADR 0008 (spec).

## 1. Problem

A server restored from an older copy of its store may have lost Control
Records: for example the `CAPABILITY_GRANT` that made Bob a member. Until a
holder re-supplies them (W §68.1), the server's Control Head is behind, and
Bob's `RESOURCE_OPEN` is refused with `AUTHORIZATION_FAILED`: the server
checks `data/read` at its own head (server `session.rs`, `readable`). sdk-ts
treats that refusal as final (POST-017), so Bob stays closed until the
application reopens the Resource or restarts, even after the owner has
re-supplied the grant.

Bob holds the whole chain the server lost, validated. He could re-supply it
himself.

## 2. What the server allows today

Read from server 0.3.0 (`session.rs`, `coordinator.rs`) and W §47, §84:

| Request | Needs the session's `data/read` | Notes |
| --- | --- | --- |
| `RESOURCE_OPEN`, `CONTROL_HAVE`, `CONTROL_GET`, `DATA_GET` | yes | refused with `AUTHORIZATION_FAILED` after the loss |
| `CONTROL_PUT` | no | the server authorizes the record by its issuer, not the uploader (§84); only hosting quotas and rate limits apply to the session |

A `CONTROL_PUT` whose expected head is not the server's current head is
answered `NACK(CONTROL_HEAD_MISMATCH)` with the current head's Control
Record ID as details (§47). So a member who cannot read can still learn
the server's head and upload the records it lacks. No server change is
needed.

## 3. Options

- **A. Retry the open.** Wait for another holder (usually the owner) to
  re-supply, then reopen: bounded retries with backoff, only when the
  member's own chain grants it `data/read`. Simple, but the member stays
  closed for as long as no holder connects, which after a restore may be
  long: the owner's device may be off.
- **B. Re-supply the own chain, then reopen** (recommended). The member
  pushes the records the server lacks with `CONTROL_PUT`, oldest first,
  and opens again. It recovers as soon as it connects, without the owner,
  and it uses only what W §68.1 and §84 already allow.

B falls back to a bounded A when the push cannot proceed for a transient
reason (rate limit, connection loss).

## 4. Algorithm (B)

Preconditions, all required; otherwise the refusal stays final, as today:

1. `RESOURCE_OPEN` was refused with `AUTHORIZATION_FAILED`;
2. the client holds a validated Control Chain of the Resource, with head
   `L` at sequence `n`, and that chain grants the session's Principal
   `data/read` at `L` (the same check the client already makes before it
   trusts its own access);
3. no recovery attempt for this Resource on this route has failed finally
   in the current session.

Steps:

1. Send `CONTROL_PUT(record n, expected = record n−1)`.
2. On the answer:
   - `ACK`: the server had `n−1` and now has `n`: go to step 4;
   - `NACK(CONTROL_HEAD_MISMATCH, H)` and `H` is a record of the local chain
     at sequence `h`:
     - `h = n`: the server already holds the whole chain; the refusal is
       not caused by a loss. Stop; the refusal is final;
     - `h < n`: the server lost `h+1 … n`. Go to step 3;
   - `NACK(CONTROL_HEAD_MISMATCH, H)` and `H` is not in the local chain:
     the server's chain has records the client does not know (a newer
     revocation, or a fork after the restore). Stop; the refusal is final,
     and the client fetches nothing it cannot read. A fork is reported as
     `CONTROL_CONFLICT` once the client can read again (ADR 0008, option (d)
     deferred);
   - a transient refusal (`RATE_LIMITED`, a closed connection): back off,
     at most 3 attempts with the client's usual backoff, then final;
   - any other refusal: stop; final.
3. Send `CONTROL_PUT(record k, expected = record k−1)` for `k = h+1 … n`, in
   order, one at a time (a server need not accept `CONTROL_BATCH` from a
   client, W §68.1). A `CONTROL_HEAD_MISMATCH` here means another holder is
   re-supplying at the same time: re-read the reported head and continue
   from it as in step 2.
4. Send `RESOURCE_OPEN` again, once. On `RESOURCE_OPENED`, the normal
   anti-entropy of W §68.1 re-supplies the Data Units and Key Packages the
   server lacks. A second `AUTHORIZATION_FAILED` is final.

At most one recovery runs per Resource and route at a time; its outcome is
recorded for the session, so a Resource the server refuses is not retried
in a loop.

## 5. Security rationale

- **Nothing is forged or learned.** The member uploads only records it
  holds, each signed by its issuer; the server validates each as if its
  issuer had uploaded it (W §84). The only thing the member learns is the
  server's current head ID, which any session already learns from a
  `CONTROL_PUT` mismatch; it learns no data and no membership it does not
  already hold.
- **No brute force.** There is nothing to guess: the push sends the
  member's own chain, in order, a bounded number of times per session, and
  every request counts against the server's per-connection and per-address
  limits. Precondition 2 means a client never tries with a chain that does
  not grant it access.
- **A revoked member stays refused.** If the revocation is on the member's
  validated chain, precondition 2 fails and nothing is sent. If the
  revocation is only on the server's chain, the server's head is unknown to
  the member (step 2, third case): it stops and sends nothing more.
- **No new authority.** Re-supplying a record never changes who may do
  what: the record was already valid and accepted once, and the server
  re-checks it. A member cannot remove records from the server, only add
  the ones that extend its head.
- **Privacy.** The records are signed Control Records the server held
  before the loss; re-supplying them discloses nothing new to the server.

## 6. Plugin status (obsidian)

While the recovery runs: "Waiting for the server to recover access". On
success: the normal open. On a final refusal: the existing "No access"
message, unchanged. The status never claims that access was restored
before `RESOURCE_OPENED`.

## 7. Tests

Against the Rust server (live interop, sdk-ts):

| Case | Expected |
| --- | --- |
| Restore before the member's grant; the member connects first | it pushes the lost records, reopens and reaches LIVE without the owner |
| The owner re-supplies first | the member's first push answers `CONTROL_HEAD_MISMATCH` with a head at `n`: it reopens and reaches LIVE (no duplicate records) |
| The member and the owner push at the same time | each continues from the reported head; one chain, no fork |
| The member's own chain revokes it | no `CONTROL_PUT` is sent; the refusal is final |
| The server's chain revokes it, the member has not seen it | one `CONTROL_PUT`, a mismatch with an unknown head, then final |
| Rate limited | at most 3 attempts with backoff, then final |
| A genuine refusal (no loss) | one `CONTROL_PUT` answered with the member's own head; final |

Unit tests: the preconditions, the head classification of step 2, the
bound on attempts.

## 8. Spec and effort

- No Wire or profile change: the steps use `CONTROL_PUT` as W §47, §68.1
  and §84 define it. An informative paragraph in W §68.1 ("a member
  refused on open may re-supply the records that grant it access") can go
  into the next spec batch; it is not required to implement.
- sdk-ts: about 2 days, most of it the live tests (the push already
  exists for anti-entropy; the new parts are the trigger on the refused
  open, the head classification and the bound). Obsidian: the status text.
