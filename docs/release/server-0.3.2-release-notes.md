# OpenLFCP server 0.3.2: release notes

**Status:** Draft until the project owner tags `v0.3.2`. The reference
server `0.3.2` (server d0ae2e9, on sdk-rs 74c3a71, spec
`mvp-0.2-baseline.10`), 2026-10-12. A patch release of
[server 0.3.1](server-0.3.1-release-notes.md) with one wire fix: finding
S2 of the server fuzzing.

## What this is

Server 0.3.2 checks the Have Vector a client sends in `RESOURCE_OPEN`, as
it already checked the one in `DATA_HAVE`. A malformed Have is answered
with `NACK(MALFORMED_MESSAGE)` instead of `RESOURCE_OPENED`.

The store format, the configuration and the admin API are unchanged.

## Upgrade notes

- **No store migration and no configuration change.** The store schema is
  the same as in 0.3.0 and 0.3.1: a 0.3.1 state directory works as it is.
- **Rollback to 0.3.1 is possible.** 0.3.1 opens a state directory that
  0.3.2 has used, because 0.3.2 adds no migration.
- **Back up the state directory first** anyway, as for every upgrade.
- **Image:** `ghcr.io/openlfcp/lfcp-server:0.3.2` (linux/amd64,
  linux/arm64), published by the `v0.3.2` tag. `lfcp-admin` is built from
  source as before (`cargo build --release -p lfcp-admin`); its behaviour
  is unchanged.
- **Clients:** unchanged from 0.3.1; every 0.1.x client works. A client
  always sends a normalized Have (LFCP-WIRE-01 §28), so a conformant client
  never meets the new refusal.

## What changed

**A malformed live Have in `RESOURCE_OPEN` is refused** (fuzzing finding
S2; server c4aa885). LFCP-WIRE-01 §48 rejects a range with `start > end`,
or one that includes sequence `0`, in every live Have Vector, and §41
gives `RESOURCE_OPEN` one. 0.3.1 did not read the Have of `RESOURCE_OPEN`
at all and answered `RESOURCE_OPENED`. 0.3.2 checks it first, with the
same check as `DATA_HAVE`, and answers `NACK(MALFORMED_MESSAGE)`. A Have
that is valid but not normalized (unsorted, overlapping or adjacent
ranges) still opens the Resource. Spec `mvp-0.2-baseline.11` (prepared)
adds the matching negative vectors.

**Dependencies and tests.** The locks move from `mvp-0.2-baseline.4` and
sdk-rs 7edbd5f to `mvp-0.2-baseline.10` and sdk-rs 74c3a71 (server
814e913). Between those commits sdk-rs changes only `shared_objects` and
`shared_sections`, behind features the server's build does not enable, so
the server binary does not change with them.

## Operator changes

- None. A client that sends a malformed Have in `RESOURCE_OPEN` now gets
  `NACK(MALFORMED_MESSAGE)` and is not subscribed to the Resource.

## Compatibility

- LFCP-WIRE-01 at `mvp-0.2-baseline.10` (spec a3161f7), on sdk-rs 74c3a71.
  No wire change beyond the refusal above, which §48 already required.
- Clients: as with [server 0.3.0](server-0.3.0-release-notes.md#compatibility).

## Security

No change in the security model. In 0.3.1 the message ignored the Have:
it opened the Resource only for a session allowed to read it, and wrote
nothing.

## Known limitations

- The limitations of [server 0.3.1](server-0.3.1-release-notes.md#known-limitations)
  stand.
