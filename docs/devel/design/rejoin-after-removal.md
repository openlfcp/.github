# Rejoining a section after removal

**Status:** design note for MVP 0.3 (sdk-ts and the Obsidian plugin); in
0.4.0-beta.15 the plugin only says that rejoining is not supported yet.
**Date:** 2026-10-13. **Base:** LFCP-WIRE-01 at `mvp-0.2-baseline.12`;
sdk-ts 0.2.0-beta.7; server 0.3.2 (138030a); Obsidian plugin 0.4.0-beta.14.

## 1. Problem

The owner removes a member with "Remove access…" and later wants them
back. The only path the plugin offers is a new invitation. Opened by the
removed member, it answered "this device is already in that
collaboration" and did nothing. Pilots read that as "the owner cannot take
back a removal".

## 2. What the specification allows

A removed member may rejoin with a new invitation. Nothing in WIRE-01 or
the profiles keeps a Principal out after a removal:

- §17.3 revokes **grants**, not Principals. A grant is active while it
  and its parent are not revoked (§17.2). There is no deny list.
- §18.1's claim rules concern the Invitation Grant: active, grants
  `invite/claim`, claims left, the abilities, the issuer. None looks at
  the claimant's earlier grants. A successful claim "creates a new
  capability grant to the claimant": an active one.
- The removal rotated the Data Epoch (§19, reason "member revoked"). The
  claimant gets the current epoch's DEK through the Invitation
  Principal's Key Package (§18.1, §25.2), and §18.1 asks the inviter to
  seal one to the claimant as well.
- The server's checks of a claim (sdk-rs `wire/control/authority.rs`,
  §18.1 rules 1–5) have no rule about a revoked subject either.

SDK-SECTIONS-INTEGRATION-01 and the profiles say nothing about rejoining.

## 3. Evidence

A headless probe ran on 2026-10-13: two plugin cores (the native harness's
`peer`) against the reference server at 138030a, with the member behind a
TCP proxy so that it alone could go offline. Owner A shares a section,
member B joins, A removes B with `revokeSectionAccess`, A invites again.

### 3a. Nothing pending at the removal

| Step | Result |
| --- | --- |
| B joins with the new link (plugin `Collaboration.join`) | `already-member`, answered locally |
| The same, past the plugin's local check | `joined`: the server accepted the claim |
| B's write access right after | still `server-refused`, with the old Control Head and time: the running runtime keeps the Resource closed |
| After B's runtime restarts (same device, storage, notes) | write access allowed |
| B edits | committed, merged at A |
| An edit B made while removed (kept locally, `access-refused`) | committed by the next pass, merged at A |

So with nothing pending, rejoining works end to end except for two
plugin gaps.

### 3b. Work pending at the removal

B, offline, commits an edit ("Beta pending at removal"); A removes B; B
comes back.

| Step | Result |
| --- | --- |
| After the removal | B's pending unit leaves its outbound queue; it never reaches the server |
| After the rejoin and a restart | B's replica still contains the change, and its note still shows it |
| B edits | committed and accepted by the server; at A the unit is stored as `held` and never merged |
| Later edits of B | also never shown at A |

B believes it synced, but A never shows anything B writes again.

### 3c. Control: work going stale without a rejoin

A, B and C are members. B, offline, commits an edit; A removes C (the
epoch rotates); B comes back. B's pending unit is discarded **and B's
replica is rebuilt without it**, and B's next edit merges at A. This is
the §19.1 path working. (B's offline text also left B's note. Whether
the plugin surfaces it as stale work, as §19.1 asks, was not checked
here: see §7.)

## 4. Root causes

1. **The plugin answers locally.** `Collaboration.join()`
   (`obsidian: src/core/collab/service.ts`) checks
   `runtime.hasResource(R)` and answers `already-member` before any network
   call. A removed member keeps its Resource by design ("your local copy
   stays"), so every later invitation is answered that way. The SDK's
   `acceptInvitation` has no membership check, and the server does not
   list B.
2. **No reopen after a claim on a known Resource.** The runtime keeps a
   Resource it was refused (`server-refused`, CLOSED) until a restart; a
   new claim does not reopen it.
3. **A stale unit is kept in the rejoining member's replica.** WIRE-01
   §19.1: once a receiver knows the Key Epoch Record, a unit of the closed
   epoch beyond its final frontier is stale; "the replica rebuilds its
   state without that unit and surfaces the unit as stale". §26.2: after a
   stale unit at sequence `N`, the writer's unit at `N+1` names the unit at
   `N-1`. In 3c the client does both. In 3b the pending unit was dropped
   while B was refused, before B could learn the Key Epoch Record. After
   the rejoin, nothing rebuilt the replica. B's next unit names the stale
   one as `previous` (and its Automerge change depends on it), so every
   other replica holds it as not linking (§26.2): held for good.

Causes 1 and 2 are plugin work. Cause 3 is a conformance gap in the
client's stale-work handling on the removal-then-rejoin path.

## 5. Decision for 0.4.0-beta.15

Fixing 1 and 2 alone would make 3b reachable: a member whose work was
pending at the removal would rejoin and then be silently held at everyone
else, which is worse than a clear refusal. So beta.15 only says what
happens (`rw/removed-member-msg`):

- `join()` on a Resource whose access is revoked or server-refused, or
  that the server refuses with `AUTHORIZATION_FAILED`, answers a new
  outcome, `removed`, before any claim. The link is not used and nothing
  changes. The notice reads: "You were removed from this section.
  Rejoining a section you were removed from isn't supported yet; your
  local copy stays on this device."
- The section card of such a vault no longer says "Current as last checked
  with the server"; it says it is not synced and that its waiting updates
  are not sent.

## 6. Options for the stale work (3b)

Re-sealing the refused unit under the new epoch is **not** an option:
§19.1 says "the stale unit itself is never re-encrypted, re-signed or
merged". What stays open is when and how the rejoining client applies
§19.1 and §26.2:

- **A. Rebuild on the Key Epoch Record, wherever it is learned.** When the
  client learns, by any route (catch-up after a claim included), a Key
  Epoch Record that closes an epoch, it treats each of its own units of
  that epoch beyond the final frontier as stale. It does that whether the
  unit is still queued or was already dropped. It rebuilds the replica
  without them (the Data Profile's rebuild) and names `N-1` as `previous`
  for its next unit. It also keeps the stale units (or their changes)
  quarantined, for §7. Recommended: it is what §19.1 already requires,
  one code path for 3b and 3c.
- **B. Start a fresh replica state from the accepted units after a
  refusal.** When the client is refused a Resource, it marks every unit
  of its own not known as accepted as suspect. On reopening it rebuilds
  from accepted units only and re-plans from the note: the plugin's
  three-way pass sends the note's text again as new changes. That is
  simpler to reason about, but broader: it also discards work that later
  turns out to be within the frontier, so the note must keep it and send
  it again.

Either way the stale change's text must not be lost: the plugin keeps the
note's text and offers the stale work for review (§19.1 "surfaced to the
application as stale offline work").

## 7. Work for MVP 0.3

- sdk-ts: option A in the stale-work path (rebuild and `previous` after a
  Key Epoch Record learned late), with a test for 3b. Then a reopen after
  a claim on a known Resource (cause 2).
- Obsidian plugin: `join()` claims for a removed member once the SDK
  handles 3b; the stale work is shown for review, and its text kept in
  the note. Check 3c's text loss in the note at the same time.
- Spec note (WIRE-01 §19.1 and §26.2): say that a writer which learns a
  Key Epoch Record only after it was refused, or after a new claim,
  applies the same rule to units it no longer has queued.
- Tests: the probe as an sdk-ts live test (3a, 3b, 3c), and a native spec
  in which the owner re-invites a removed member who had work pending.

Changing a member's role (read only, read and write), or restoring access
without a new invitation, has no path either (no grant to an existing
member in the SDK or the plugin). That is a separate MVP 0.3 item on top
of this one.
