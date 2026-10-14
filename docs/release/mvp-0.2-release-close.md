# MVP 0.2 release close-out

**Status:** CLOSED (LFCP-02-082), 2026-10-15. MVP 0.2 was released on
2026-10-14/15 after the signed GO in
[mvp-0.2-go-no-go.md](mvp-0.2-go-no-go.md). This record confirms that what
went out matches what was approved, that the public surfaces are correct,
and that every loose end has an owner. The checks below were read from the
public remotes, npm, GitHub and openlfcp.org on 2026-10-15; nothing was
sent to the production sync server.

## What was released

| Component | Released | Commit |
| --- | --- | --- |
| spec | tag `v0.2.0` (content `mvp-0.2-baseline.12`) | `bf1c78c` |
| sdk-rs | tag `v0.2.0` | `0a8239b` |
| examples | tag `v0.2.0` | `e7c3d27` |
| .github | tag `v0.2.0`, with the release notes and the organization profile | `53a6433` |
| sdk-ts | tag `v0.2.0`; npm `@openlfcp/*` 0.2.0 on `latest`, all 8 packages (release run 38616796278) | `2a34beb` |
| obsidian | Shared Tasks `0.4.0`: tag `0.4.0`, GitHub Release with three files; `main` is the tag commit | `ce0660a` |
| server | no new tag: 0.3.2 deployed; `main` adds only the deploy configuration (the sync.openlfcp.org limits as defaults) | `b96721f` |
| website | openlfcp.org, `main` | `0141bd5` |

The tags of spec, sdk-rs, examples, sdk-ts and obsidian point at the
commits of the final candidate,
[rc17-manifest.json](rc17-manifest.json). .github's tag is on the commit
that holds the published release notes, after rc17's `.github` commit.

## 1. Released artifacts

- [x] The git tags point at the candidate commits: annotated tags, peeled
      on the remote to the commits above.
- [x] Plugin release `0.4.0` on GitHub: published, not a pre-release, with
      `main.js`, `manifest.json`, `styles.css`:
      - `main.js` sha256 `c93f1a88352a7faf0ca800854ea8c70b3a2dafefdcfb8272513ebb2cd1ddc0e4`
      - `manifest.json` sha256 `28df943d4903e29a91154c0b1562d78fadff49db76456bfbea261ddd16441f0f`
      - `styles.css` sha256 `4cd5bf6b733ea5c3237649bfd3a461a298ede39802c6beb2c1c92b320ef4c2d1`
- [x] npm `@openlfcp/*` 0.2.0: core, wire, crypto, storage, storage-idb,
      storage-node, shared-objects, client, each with build output and SLSA
      provenance.
- [x] Server image: no server release, as planned
      ([mvp-0.2-server-no-change.md](mvp-0.2-server-no-change.md)).
- The immutable candidate set (`--assemble --repro`) was **waived** in the
  go/no-go record: npm was built and published in CI, and the plugin files
  by its tag workflow (dry run 38618407889). The digests above are the
  record of what was published.

## 2. Public links

- [x] [Release notes](mvp-0.2-release-notes.md) published with the
      `.github` `v0.2.0` tag and linked from the organization profile.
- [x] Organization profile: `profile/README.md` is the MVP 0.2 text
      (LFCP-02-079), live on `main` `53a6433`.
- [x] Website `openlfcp.org` on MVP 0.2 (LFCP-02-078): website `main`
      `0141bd5`, deployed by Cloudflare Pages; the live page shows the
      final limits.
- [x] The plugin's GitHub Release page for 0.4.0 is public.
- [x] doccheck passes on `.github` `main`.

## 3. Sync server

- [x] `sync.openlfcp.org` runs server 0.3.2 (the owner's record); its
      limits are those in the release notes (B15 closed), and server
      `deploy/server.toml` carries them as defaults (`b96721f`).
- [ ] The version is not observable from outside (B17): open, the owner's.
- [ ] The restore test of the public server (B16): open, the owner's. The
      restore rehearsal on a staging copy passed (LFCP-02-074,
      [record](mvp-0.2-restore-rehearsal.json)).
- [x] No production data, secrets or logs were copied into the release
      evidence.

## 4. npm

- [x] `@openlfcp/*` 0.2.0 is on **`latest`** for all 8 packages; `beta`
      stays at `0.2.0-beta.10`.
- [x] No empty tarball: every package carries `dist`, with the same or
      more files than 0.1.5.

## 5. Catalog

- [x] `manifest.json` on obsidian `main` reads `0.4.0`, and
      `versions.json` maps `0.4.0` to Obsidian 1.13.4, so catalog users
      receive the update.
- [x] Shared Tasks (`shared-tasks`, `openlfcp/obsidian`) is listed in the
      community plugins directory.
- [x] The BRAT pre-release channel stays for later betas (B14).

## 6. Post-release smoke

Not run against the live server in this close-out. Before the release, the
owner checked two Obsidian vaults by hand on 0.4.0-beta.20, the same code
as 0.4.0 (steps 0–13, PASS). The first use of the released build on
`sync.openlfcp.org` by people other than the developers is the pilot, below.

## 7. Deferred work and owners

Owner of every row: the OpenLFCP maintainers.

| Item | Tracking | Target |
| --- | --- | --- |
| Pair pilot on Shared Tasks 0.4.0, 5 pairs, frozen thresholds; operations and dogfood with it | LFCP-02-075, 103, 105; defects 076 | about two weeks after the release; results feed 0.2.x and MVP 0.3 |
| Restore test of sync.openlfcp.org | B16 | the owner, before the next server deploy |
| Deployed server version observable from outside | B17 | MVP 0.3 |
| Cross-language check of the epoch cutoff | B19 (examples `known-gaps.json`) | MVP 0.3 |
| storage-idb: wait on a blocked open, close on versionchange | LFCP-02-120 | 0.2.x |
| Serialise receipt release with the batch reports | LFCP-02-121 | 0.2.x |
| No IndexedDB transaction per idle tick | LFCP-02-122 | 0.2.x |
| A newcomer inserts a section with an open structural conflict | LFCP-02-123 | 0.2.x |
| Repair re-renders damaged bindings from the shared model | LFCP-02-124 | 0.2.x |
| Automatic compaction of a section's history | LFCP-02-118 | after 0.2 |
| Cross-category ID reuse at admission (A6) | LFCP-02-108 | decision after the pilot |
| Windows and Linux performance qualification | — | MVP 0.3 |

**Owner decisions for MVP 0.3**, still open:

- the conflict scope of a section beyond the frozen set (MS14);
- invitation expiry;
- a newcomer's access to a section's earlier history;
- rejoining after removal
  ([design note](../devel/design/rejoin-after-removal.md));
- spec `mvp-0.2-baseline.13` or the next baseline.

## 8. Incident process

- [x] The incident and rollback process:
      [MVP-0.2-TEST-AND-RELEASE-PLAN.md](../MVP-0.2-TEST-AND-RELEASE-PLAN.md)
      §15 and
      [mvp-0.2-rollback-and-restore.md](../operations/mvp-0.2-rollback-and-restore.md).
- [x] The last known-good section-capable build is Shared Tasks 0.4.0 on
      `@openlfcp/*` 0.2.0 (`storage-idb` database version 2). Going back to
      0.3.x or 0.1.x is not a safe rollback for section data.
- On a suspected unsafe projection or publication: pause the affected path
  with a tested mechanism, preserve queues and replicas, and show an honest
  blocked state. Never wipe caches or regenerate identity to make the UI
  look healthy.
- Security reports go to `security@openlfcp.org`, never to a public issue.

## Close

- Release closed by: OpenLFCP maintainers  **Date:** 2026-10-15
- Outstanding items: section 7, in the MVP 0.2 backlog
  ([BACKLOG-MVP-0.2.md](../BACKLOG-MVP-0.2.md)) and the MVP 0.3 planning.
