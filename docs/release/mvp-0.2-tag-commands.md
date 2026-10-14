# MVP 0.2 tag commands (owner)

**Status:** DRAFT (LFCP-02-093), not run. This is the owner's copy-paste
list for tagging the MVP 0.2 release once the go decision is made. Nothing
here is executed by a worker; the owner runs it. `<…>` marks a value the
release settles.

## Before you tag

- The go decision is made (owner checklist §5) and the final candidate's
  record is green (LFCP-02-073: `scripts/rc-verify.py`, G01–G12).
- The final commits are pinned in `rcN-manifest.json`; use those exact SHAs
  below. One tag per repository, on the commit the candidate verified.
- Tags are **annotated, never signed**: `-a`, never `-s`. The owner does not
  sign tags.
- Replace `<repos>` with your local checkout root. Do not commit a path that
  names a home directory.
- Push each tag on its own line, never through a pipe.

## Version tags: `v0.2.0`

`spec`, `sdk-rs`, `examples` and `.github` take `v0.2.0` on the candidate's
commit: the rc17 commits (`<rc17-manifest.json>`) for `spec`, `sdk-rs`
and `examples`. `.github` takes it on the commit that holds
the published MVP 0.2 release notes: the `main` head at release, after the
notes are merged.

```sh
# spec (content is mvp-0.2-baseline.12; v0.2.0 is the release tag)
git -C <repos>/spec    tag -a v0.2.0 -m "OpenLFCP MVP 0.2" <rc17 spec commit>
git -C <repos>/spec    push origin v0.2.0

# sdk-rs
git -C <repos>/sdk-rs  tag -a v0.2.0 -m "OpenLFCP MVP 0.2" <rc17 sdk-rs commit>
git -C <repos>/sdk-rs  push origin v0.2.0

# examples
git -C <repos>/examples tag -a v0.2.0 -m "OpenLFCP MVP 0.2" <rc17 examples commit>
git -C <repos>/examples push origin v0.2.0

# .github
git -C <repos>/.github tag -a v0.2.0 -m "OpenLFCP MVP 0.2" <.github main head at release, after the release notes merge>
git -C <repos>/.github push origin v0.2.0
```

## sdk-ts: npm, not a `v0.2.0` git tag here

`@openlfcp/*` `0.2.0` (rc17's sdk-ts commit, `<rc17 sdk-ts commit>`) is
published under the dist-tag **`latest`** from `sdk-ts` through its own
release flow (the `npm-publish` environment, owner-approved),
driven by the tag that repository's release process expects. It is listed
here only so the set is complete; it is **not** part of the `v0.2.0`
command block above. Follow `sdk-ts`'s release doc for its exact tag and
the npm approval step.

## server: tag only if it changed

MVP 0.2 ships the deployed reference server `0.3.2`
([notes](server-0.3.2-release-notes.md)). rc17's server commit
(`<rc17 server commit>`) is `0.3.2` plus pin-only commits, so **no new server tag is expected** (V1: "server
only if it changed"). Tag the server only if the candidate pins a server
commit past `v0.3.2`:

```sh
# only if the candidate's server commit is past v0.3.2
git -C <repos>/server tag -a <server tag> -m "OpenLFCP server <version>" <server commit>
git -C <repos>/server push origin <server tag>
```

## plugin: its own `0.4.0` tag

The Obsidian plugin carries its own version tag, not `v0.2.0`. Tagging
`0.4.0` and moving `manifest.json` / `versions.json` on `main` to `0.4.0`
happen in the same step, or catalog users never receive the update.

```sh
# plugin release tag (scheme per obsidian docs/devel/release.md)
git -C <repos>/obsidian tag -a 0.4.0 -m "Shared Tasks 0.4.0" <rc17 obsidian commit: Shared Tasks 0.4.0 on @openlfcp/* 0.2.0>
git -C <repos>/obsidian push origin 0.4.0
```

- After tagging, confirm `manifest.json` and `versions.json` on `main`
  read `0.4.0` (see
  [obsidian docs/devel/release.md](https://github.com/openlfcp/obsidian/blob/main/docs/devel/release.md)).

## After pushing

- `git -C <repos>/<repo> ls-remote --tags origin` shows each new tag on the
  remote.
- Publish the release notes and the organization profile, and update the
  website (owner checklist §6).
