# README scope statements for MVP 0.1

**Status:** draft for LFCP-072. Each repository README gets a short
"Scope" section near the top, so that nobody reads MVP 0.1 software as a
full LFCP-WIRE-01 implementation (`MVP-0.1-PROTOCOL-SCOPE.md` §5). The
sections below are the text per repository.

## spec

> **Scope.** These are Working Drafts. The tag `mvp-0.1-baseline.6` is the
> MVP 0.1 implementation baseline (`MVP-0.1-BASELINE.md`), not a Stable
> LFCP-WIRE-01. MVP 0.1 software implements a subset of it; the deferred
> features are listed in `.github: docs/release/deferred-wire-01-features.md`.

## sdk-ts

> **Scope.** sdk-ts implements the OpenLFCP MVP 0.1 subset of LFCP-WIRE-01
> at `mvp-0.1-baseline.6`, not every deferred WIRE-01 feature (coordinator
> recovery, Resource tombstones, route migration, presence, mirror
> seeding and others; see `.github: docs/release/deferred-wire-01-features.md`).
> It does not claim full LFCP-WIRE-01 conformance.

## sdk-rs

> **Scope.** sdk-rs implements the OpenLFCP MVP 0.1 subset of LFCP-WIRE-01
> at `mvp-0.1-baseline.6`, not every deferred WIRE-01 feature; it has no
> invitation URI codec yet. See
> `.github: docs/release/deferred-wire-01-features.md`. It does not claim
> full LFCP-WIRE-01 conformance.

## server

> **Scope.** The reference server implements the server side of the
> OpenLFCP MVP 0.1 subset of LFCP-WIRE-01 at `mvp-0.1-baseline.6`: one
> coordinator per Resource, one endpoint, no federation, mirror seeding or
> presence. See `.github: docs/release/deferred-wire-01-features.md`. It does
> not claim full LFCP-WIRE-01 conformance.

## obsidian

> **Scope.** The plugin implements the OpenLFCP MVP 0.1 product slice on
> sdk-ts: sharing Tasks between vaults over the MVP 0.1 subset of
> LFCP-WIRE-01 at `mvp-0.1-baseline.6`, not every deferred WIRE-01 feature
> (see `.github: docs/release/deferred-wire-01-features.md`). Desktop only is
> tested; mobile is not.

## examples

> **Scope.** The examples run on sdk-ts and sdk-rs at their pinned commits.
> They use only the OpenLFCP MVP 0.1 subset of LFCP-WIRE-01 at
> `mvp-0.1-baseline.6`.
