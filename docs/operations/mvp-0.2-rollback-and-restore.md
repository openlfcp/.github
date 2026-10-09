# Rollback and restore for the MVP 0.2 candidate (LFCP-02-074)

**Status:** DRAFT for the owner. The rehearsal ran on 2026-10-09 at the
`mvp-0.2-baseline.2` pins and passed; the evidence is
[mvp-0.2-restore-rehearsal.json](../release/mvp-0.2-restore-rehearsal.json).
The candidate builds of LFCP-02-073 are not assembled yet. Run the rehearsal
again on them before the first users get the candidate.

This page covers what can be rolled back if the MVP 0.2 candidate goes
wrong, what cannot, and how to restore the server's state. The public
server's own procedures (backup, restore, upgrade) are in the
[sync server runbook](sync-server-runbook.md) and the stack runbook it
points to. The public restore drill is
[sync-server-restore-test.md](sync-server-restore-test.md).

## Who acts

- **The owner** runs the public server, `wss://sync.openlfcp.org`, on the
  owner's box:
  - deploys an image from `ghcr.io/openlfcp/lfcp-server:<version>`;
  - takes and restores the backups;
  - tags releases and publishes npm packages and plugin builds.
- **Agents** never touch the public stack. They rehearse on a local
  compose stack (below) and prepare fixes for the owner to release.

## The last good builds

| Component | Last good | Section-capable | Storage |
| --- | --- | --- | --- |
| Server | `v0.3.0` (`09c9132`), image `lfcp-server:0.3.0` | Yes. The server is opaque to Data Profiles, and the candidate pin `7f7eb99` changes no server source since `v0.3.0` (tests, docs and locks only). | Store schema 3, the same since `v0.2.0` |
| SDK, legacy line | `@openlfcp/*@0.1.3` on npm (`0.1.4` prepared, not tagged) | No | SQLite schema 3, IndexedDB version 1 |
| SDK, candidate | sdk-ts `b92f701` (0.2 line, unreleased) | Yes | SQLite schema 4, IndexedDB version 2 |
| Plugin | Shared Tasks `0.3.2` (on SDK 0.1.3) | No | the SDK's |
| Plugin, candidate | obsidian 0.4 line (unreleased) | Yes | the SDK's |

No section-capable client has been released, so the only client rollback
target is the legacy line.

**Unsafe: a client downgrade from 0.2 to 0.1.** The candidate SDK upgrades
the vault's storage when it first opens it, and the 0.1 line cannot read the
result:

- A 0.1.3 client refuses an upgraded vault: "the database is at schema
  version 4, newer than this code (3)". It changes no byte of it (CM10 in
  [the 070 evidence](../release/mvp-0.2-integrated-recovery-qualification.md)).
- IndexedDB at version 2 gives 0.1.x a `VersionError`.

A user cannot go back to plugin 0.3.x with the same vault state. Removing
the state to get there would lose unsent work. **This path is excluded.**

## Choices when the candidate goes wrong

| Situation | Choice | What it costs |
| --- | --- | --- |
| A client defect (SDK or plugin) | **Pause, then forward-fix:** stop handing out the candidate, keep existing users where they are, and release a fixed 0.2.x/0.4.x. Never ask users to downgrade. | Users wait for the fix. Their vaults and queues stay as they are. |
| A section defect that must not spread | **Pause sharing:** users are asked, in a release note, to stop creating or joining section Resources. Legacy Tasks keep working; the server and the 0.1 path are untouched. | Sections wait. |
| A server defect in a new server release | **Roll the server back** to the previous image on the same volume. This is safe only while the store schema is unchanged between the two versions: it is 3 for `v0.2.0`, `v0.3.0` and the candidate. | A short restart. |
| Server data lost or corrupted | **Restore** the volume from the last good backup (below). Clients re-supply what the server lost (ADR 0008, LFCP-02-088; SDK 0.1.3 and later). | A restart. Units written after the backup by a client that has since lost its own state are gone. |

**Server change needed for 0.2: none.** One finding to fix before the
server's first schema change:

- The server migrates its store forward on start, but it does not refuse a
  store newer than its code (`store/schema.rs`, `migrate`).
- An older image started on a newer store would therefore run on it without
  a warning.
- **Proposal:** a server task to refuse a store whose schema version exceeds
  the code's, as the SDK already does. Until then, a server rollback must
  check the schema version first.

## Restore procedure (local staging, rehearsed)

The staging stack is the server's own deploy compose with a persistent
volume, plus an overlay that publishes the server on loopback with a
rehearsal configuration. It never uses the public stack.

```sh
examples/qualification/rehearsal/rehearse-restore.sh <evidence dir>
```

It needs Docker with Compose v2 and the CI layout: `server/`, `sdk-rs/`
(at `server/sdk-rs.lock`) and `examples/` side by side, with examples
installed and built. The script runs these steps:

1. Build the image from `server/deploy/Dockerfile`, and start the server on an
   empty volume (project `lfcp-rehearsal`, `127.0.0.1:17830`).
2. **populate:** A hosts a section Resource and a legacy Shared Objects
   Resource; B joins both through invitations.
3. **Back up**, with the server stopped:
   - `docker run --rm -v <volume>:/state:ro … tar -C /state -cf state.tar .`
   - The tar holds `server.sqlite3`, `server-id` and `setup-code`, or the
     pairing record on a paired server. Keep it private (0600).
4. **after-backup:** B commits a section batch and A writes a legacy edit;
   both are accepted.
5. **Restore:**
   - stop the server;
   - empty the volume and untar the backup;
   - `up -d --force-recreate` with the same image and configuration. The
     script checks that the image ID did not change.
6. **reconcile:** A and B restart from their vaults.
   - B emits `reoffered` (`have-gap`) for its lost batch, and A re-supplies
     its lost legacy unit. Every queue empties.
   - C, a new member, joins both Resources and reads both writes made after
     the backup: the encrypted legacy and section smoke.
   - B's and A's next writes are accepted. Each actor's sequence continues
     (B 1, 2; A 1–4 on C), so no sequence or nonce is reused.

On the public stack, the backup and the restore follow the stack runbook.
Steps 2, 4 and 6 are the checks to run there with throwaway data, as in
[sync-server-restore-test.md](sync-server-restore-test.md).

## Rehearsal result (2026-10-09)

The run used fresh clones: examples `7e7b8fc`, sdk-ts `b92f701`, server
`7f7eb99`, sdk-rs `c05309b`, spec `mvp-0.2-baseline.2`. The tools were
Docker 29.1.3 and Node.js v24.4.0, on macOS arm64.

| Phase | Result |
| --- | --- |
| populate | pass |
| backup | `state.tar`, sha256 in the record |
| after-backup | pass: B's section unit 1 and A's legacy unit 3 accepted |
| restore | the image is unchanged; the volume holds the backup |
| reconcile | pass: B reoffered 1 unit (`have-gap`); C reads B's units 1–2 and A's 1–4; no client error |

The compose project and its volume were removed afterwards; no production
state was touched.

## Not covered

- **Online backup:** the rehearsal stops the server for the copy. The
  public stack's nightly encrypted backup is described in the stack
  runbook, and its consistency is not checked here.
- **A server rollback across a schema change:** none exists yet (see the
  finding above).
- **Native clients:** the plugin's restore behaviour in Obsidian belongs to
  LFCP-02-066.
