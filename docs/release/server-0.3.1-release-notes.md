# OpenLFCP server 0.3.1: release notes

**Status:** Draft until the project owner tags `v0.3.1`. The reference
server `0.3.1` (server aa398d9, on sdk-rs 7edbd5f, spec
`mvp-0.2-baseline.4`), 2026-10-10. A patch release of
[server 0.3.0](server-0.3.0-release-notes.md) with two store fixes:
LFCP-02-116 ([BACKLOG-MVP-0.2.md](../BACKLOG-MVP-0.2.md)) and finding S1
of the server fuzzing.

## What this is

Server 0.3.1 makes the store fail safely in two cases where 0.3.0 did not:
- a state directory written by a newer server is refused at start, before
  anything is written to it;
- a damaged database answers the read that meets the damage with an error,
  instead of panicking the store thread and taking the whole store down.

The wire protocol, the store format, the configuration and the admin API
are unchanged.

## Upgrade notes

- **No store migration and no configuration change.** The store schema is
  the same as in 0.3.0: a 0.3.0 state directory works as it is.
- **Rollback to 0.3.0 is possible.** 0.3.0 opens a state directory that
  0.3.1 has used, because 0.3.1 adds no migration.
- **Back up the state directory first** anyway, as for every upgrade.
- **Image:** `ghcr.io/openlfcp/lfcp-server:0.3.1` (linux/amd64,
  linux/arm64), published by the `v0.3.1` tag. `lfcp-admin` is built from
  source as before (`cargo build --release -p lfcp-admin`); its behaviour
  is unchanged.
- **Clients:** unchanged from 0.3.0; every 0.1.x client works.

## What changed

**A store written by a newer server is refused** (LFCP-02-116; server
e49f595). When the database's schema version is above every migration
this server knows, opening it fails with `StoreError::NewerSchema` and the
server exits with:

```text
the store is at schema version N, newer than this server supports (M); it was
left unchanged: run a server version that supports it, or restore a backup
made by this version
```

The version is read on a read-only connection (immutable when there is no
write-ahead log), so the refused store keeps its files byte for byte.
Before, an older server would have run on a schema it did not know. A
future rollback across a schema change therefore needs a backup made by
the older version. It does not apply to this release: 0.3.0 and 0.3.1
share one schema.

**A damaged ID column is reported as corrupt, not a panic** (fuzzing
finding S1; server 1abba1e). The schema checks that IDs are 32 bytes only
when a row is written, so a damaged file can hold an ID of another length.
0.3.0 panicked on the store thread when it read one: every later call
failed with "store closed", and a restart panicked again at the same read.
0.3.1 fails only that read, with:

```text
the store is corrupt (an ID of N bytes, not 32); restore server.sqlite3 from a backup
```

The store keeps answering every other read. The check covers all 18 reads
of an ID. SQLite's `PRAGMA quick_check` and `PRAGMA integrity_check` both
find this damage (about 0.7 s for a 600 MB store with a warm cache); the
server does not run them at start.

**Dependencies and tests.** The locks move to `mvp-0.2-baseline.4` and
sdk-rs 7edbd5f (server 79c240e). The server reads only the MVP 0.1
vectors, which that baseline leaves unchanged. Tests and tools that are
not part of the binary or the image:
- the end-to-end tests of a shared sections Resource and its storage and
  transfer at scale;
- fuzz targets for the wire decoding, sessions and store open, with the S1
  reproducer (`fuzz/`).

## Operator changes

- **A refusal at start.** If the server exits with "newer than this server
  supports", the state directory comes from a newer server. Run that
  version again, or restore a backup made by this one. Do not edit the
  database.
- **`Corrupt` instead of a crash.** A request that meets damaged data fails
  with the "store is corrupt" error in the server log, and the server keeps
  running. Stop it, restore `server.sqlite3` from a backup, and check the
  copy with `sqlite3 server.sqlite3 'PRAGMA integrity_check'` before
  starting again.

## Compatibility

- LFCP-WIRE-01 at `mvp-0.2-baseline.4` (spec 1e548f7), on sdk-rs 7edbd5f.
  No wire change.
- Clients: as with [server 0.3.0](server-0.3.0-release-notes.md#compatibility).

## Security

No change in the security model. A damaged or hostile `server.sqlite3` no
longer stops the whole store from serving; the store file is still trusted
operator data, and the server still does not validate it as a whole at
start.

## Known limitations

- Integrity checks do not run at start; damage is found when a read meets
  it.
- The limitations of [server 0.3.0](server-0.3.0-release-notes.md#known-limitations)
  stand.
