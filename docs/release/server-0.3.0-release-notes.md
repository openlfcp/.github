# OpenLFCP server 0.3.0: release notes

**Status:** Draft until the project owner tags `v0.3.0`. The reference
server `0.3.0` (server 09c9132, on sdk-rs 259a688), 2026-10-08. It is part
of the MVP 0.1.x sustaining release of wave W0
([BACKLOG-MVP-0.2.md](../BACKLOG-MVP-0.2.md), tasks 088 and 089), together
with spec `mvp-0.1-baseline.9`, sdk-ts `0.1.2` and the Obsidian plugin
`0.3.2`.

## What this is

Server 0.3.0 makes a restore of the server's store recoverable. Before it, a
server restored from a backup accepted a writer's next Data Unit over the
unit it had lost, and every replica that fetched it then waited for the
lost unit forever ("no progress"). Now the server refuses such a unit, and
clients re-supply what the server lost. This applies
[ADR 0008](https://github.com/openlfcp/spec/blob/main/adr/0008-recovery-after-server-data-loss.md),
option (c), accepted by the project owner on 2026-10-08.

The release also ships the `lfcp-admin` administration CLI (POST-014).

It is a minor version: the server answers a new error code. The store, the
configuration and the admin API are unchanged.

## Upgrade notes

- **No store migration and no configuration change.** A 0.2.0 state
  directory and configuration work as they are, and 0.2.0 can open them
  again after a rollback.
- **Back up the state directory first** anyway, as for every upgrade.
- **Image:** `ghcr.io/openlfcp/lfcp-server:0.3.0` (linux/amd64,
  linux/arm64), published by the `v0.3.0` tag.
- **Clients:** the server works with every 0.1.x client. The recovery
  itself needs clients that re-supply lost objects: sdk-ts `0.1.2` and the
  Obsidian plugin `0.3.2` (see Compatibility).

## What changed

**The `previous` link check** (LFCP-WIRE-01 §51.1; server 2f29cfb). Under
the Resource lock, after the equivocation check, every Data Unit of a
`DATA_PUT` whose `previous` is not `null` must name one of these:
- a unit of the same actor, at a lower sequence, that the server stores
  (equivocation evidence included);
- an earlier unit of the same `DATA_PUT`;
- a unit covered by a Snapshot the server stores (its frontier covers
  sequence `m < N` of the actor, and no stored unit lies between `m` and
  `N`).

Otherwise nothing of the put is stored, and the answer is
`NACK(UNKNOWN_PREVIOUS)` (code 23). Its details are the 32-byte
`previous` that the server does not hold. The check uses sdk-rs
`check_put_previous` and costs one indexed lookup per unit; Snapshots are
read only when a `previous` is not stored.

**Relay is a rule now** (LFCP-WIRE-01 §84). The server authorizes an
uploaded object, not the session that uploads it. It already behaved so;
it is now specified and tested: any authenticated session may upload
another Principal's validly signed Data Unit, Control Record, Key Package
or Snapshot. That is how clients re-supply a restored server.

**`lfcp-admin`** (POST-014; server 4644302, 36805ed, 740e589). The
administration CLI for the setup and admin HTTP API:
- `keygen`: the administrator's key file (mode 0600, never printed);
- `pair`: pairing with the setup code, read from stdin or a file;
- `status`, `hosting get|set`, `quota list|get|set|clear`.

It signs with the server's own proof format and speaks plain `http://` to
the loopback admin port over an SSH tunnel; `https://` is refused. Build it
with `cargo build --release -p lfcp-admin`; it is not in the container
image. See server `README.md`, "lfcp-admin".

**Tests** (server 2f29cfb):
- the eight `data_put_previous` vectors of LFCP-TEST-VECTORS-01 through a
  real session;
- the restore drill of ADR 0008: units 1–3 backed up, unit 4 acknowledged
  and lost, unit 5 refused until another Principal relays unit 4;
- relay of a Control Record, a Key Package and a Snapshot by a session that
  is not their author.

The live interop of sdk-ts against this server passes 29/29, including a
restore after an acknowledged unit and a restore that lost the whole
Resource (sdk-ts `conformance/interop/rust-server-recovery.test.ts`).

## Compatibility

- LFCP-WIRE-01 at `mvp-0.1-baseline.9` (spec f42533c), on sdk-rs 259a688.
  The only wire change is the new refusal and its code.
- **sdk-ts `0.1.2` and the Obsidian plugin `0.3.2`** reconcile in both
  directions: they upload what the server lacks, relay other actors'
  units, and re-host a Resource the server lost. Against a restored 0.3.0
  server they recover by themselves.
- **sdk-ts `0.1.1` and the plugin `0.3.1`** still work with 0.3.0, with
  the same behaviour as before except after a restore. Then:
  - a 0.1.1 writer whose next unit names a lost one gets `NACK(23)`, which
    it does not know; it retries with backoff and does not send the lost
    unit itself. Its new edits stay local until any 0.1.2 client of the
    collaboration relays the lost unit. Other members are no longer
    stalled by it;
  - a 0.1.1 client does not re-host a lost Resource.
- The server can be deployed before the clients are upgraded: the new
  rule only refuses what a 0.2.0 server would have accepted and served as
  a stall.

## Security

No change in the security model. The server sees nothing new: actor,
sequence and `previous` are metadata it already stored. A relayed object
must be validly signed and authorized as if its author had uploaded it,
and uploads count against the uploading session's limits and the hosting
Principal's quotas.

## Known limitations

- **Restore still loses data no client holds.** An acknowledged object that
  no connected client keeps is gone with the store. Back up often, or
  stream the store off the machine.
- **A Control Chain fork after a restore** stays possible: if a member
  proposes a new Control Record before a holder re-supplies a lost one, the
  chains diverge and clients stop at `CONTROL_CONFLICT`. Fork recovery is
  deferred (ADR 0008, option (d)).
- **A future operator removal of a Resource** would need a lasting refusal
  (`RESOURCE_TOMBSTONED` or a denylist): clients re-host a Resource that a
  server answers with `RESOURCE_NOT_HOSTED`. There is no removal today
  (ADR 0008, "Known limitation").
- There is still no API to ban a Principal or purge its Resources
  (POST-015); a zero quota stops a Principal's hosting and writes.
- The other limitations of [server 0.2.0](server-0.2.0-release-notes.md)
  stand.
