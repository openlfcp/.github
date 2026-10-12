# OpenLFCP server 0.3.2: release notes

**Status:** Draft until the project owner tags `v0.3.2`. The reference
server `0.3.2` (server 7afa509, on sdk-rs d31d4d8, spec
`mvp-0.2-baseline.11`), 2026-10-12. A patch release of
[server 0.3.1](server-0.3.1-release-notes.md) with two wire fixes:
findings S2 and W3 of the fuzzing.

## What this is

Server 0.3.2 checks the Have Vector a client sends in `RESOURCE_OPEN`, as
it already checked the one in `DATA_HAVE`. A malformed Have is answered
with `NACK(MALFORMED_MESSAGE)` instead of `RESOURCE_OPENED`.

It also checks a message's envelope before its type: a message with a
bad envelope now gets `ERROR(MALFORMED_MESSAGE)`, whatever its type.

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
  always sends a normalized Have (LFCP-WIRE-01 §28) and a full envelope,
  so a conforming client never meets either new refusal.

## What changed

**A malformed live Have in `RESOURCE_OPEN` is refused** (fuzzing finding
S2; server c4aa885). LFCP-WIRE-01 §48 rejects a range with `start > end`,
or one that includes sequence `0`, in every live Have Vector, and §41
gives `RESOURCE_OPEN` one. 0.3.1 did not read the Have of `RESOURCE_OPEN`
at all and answered `RESOURCE_OPENED`. 0.3.2 checks it first, with the
same check as `DATA_HAVE`, and answers `NACK(MALFORMED_MESSAGE)`. A Have
that is valid but not normalized (unsorted, overlapping or adjacent
ranges) still opens the Resource. Spec `mvp-0.2-baseline.11` adds the
matching negative vectors (`resource_open_reversed_range`,
`resource_open_range_sequence_zero`, `resource_opened_reversed_range`);
server 7afa509 sends the published bytes of the two client-to-server ones
and gets `NACK(MALFORMED_MESSAGE)`.

**A bad envelope is malformed, whatever the message type** (fuzzing
finding W3; sdk-rs ba72d8d, server 10b02f0). A message of an unassigned
type without a Message ID, or with another broken envelope field (field
0, 1 or 4 missing, a field not as its CDDL says, an unknown field from 0
to 15), now gets `ERROR(MALFORMED_MESSAGE)` instead of
`ERROR(PROTOCOL_UNSUPPORTED)`. LFCP-WIRE-01 §32 and §33
(`mvp-0.2-baseline.11`) check the envelope before the type; sdk-rs
decoded the body by type first. An unknown type with a valid envelope
still gets `PROTOCOL_UNSUPPORTED`. Vector:
`unassigned_type_without_message_id`, whose exact bytes the server's
websocket test sends.

**Dependencies and tests.** The locks move from `mvp-0.2-baseline.4` and
sdk-rs 7edbd5f to `mvp-0.2-baseline.11` and sdk-rs d31d4d8 (server
7afa509), in three steps:

- sdk-rs 74c3a71 (server 814e913, baseline.10): since 7edbd5f it changes
  only `shared_objects` and `shared_sections`, behind features the
  server's build does not enable, so the server binary does not change
  with it.
- sdk-rs ba72d8d (server 10b02f0): the W3 fix above, which changes the
  server's behaviour.
- sdk-rs d31d4d8 (server 7afa509, baseline.11): tests and README only;
  `git -C sdk-rs diff ba72d8d..d31d4d8 -- crates/lfcp/src` is empty.

## Operator changes

- None. A client that sends a malformed Have in `RESOURCE_OPEN` now gets
  `NACK(MALFORMED_MESSAGE)` and is not subscribed to the Resource.
  A message with a bad envelope gets `ERROR(MALFORMED_MESSAGE)`, also
  when its type is unassigned.

## Compatibility

- LFCP-WIRE-01 at `mvp-0.2-baseline.11` (spec 31ce592), on sdk-rs d31d4d8.
  No wire change beyond the two refusals above, which §48 and §32/§33
  require.
- Clients: as with [server 0.3.0](server-0.3.0-release-notes.md#compatibility).

## Security

No change in the security model. In 0.3.1 the message ignored the Have:
it opened the Resource only for a session allowed to read it, and wrote
nothing.

## Known limitations

- The limitations of [server 0.3.1](server-0.3.1-release-notes.md#known-limitations)
  stand.
