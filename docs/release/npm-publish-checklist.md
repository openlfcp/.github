# npm publish checklist: @openlfcp/*

**For:** the project owner, who publishes by hand. Nothing in any
repository publishes automatically, and agents never run `npm publish` or
`npm login`.

**What:** the eight sdk-ts packages, `0.1.0-rc.1`, under the npm dist-tag
`next`. On a package's first publish npm also sets `latest`, whatever
`--tag` says: `latest` always exists once a package does, and can only be
moved, never removed (see [Promotion](#promotion)).

**Published:** `0.1.0-rc.1` of all eight, from sdk-ts 98efaab, on
2026-10-06. Being their first publish, `next` and `latest` both name it.

**Final:** `0.1.0` of all eight, from sdk-ts 4e1b02f, under `latest`. See
[Final release 0.1.0](#final-release-010). Sections 1 to 5 describe the
release-candidate publish; the final release reuses them.

## 1. Prerequisites

- [ ] An npm account with two-factor authentication on (auth and writes).
- [ ] Membership of the `openlfcp` npm organization with publish rights
      for the `@openlfcp` scope. Check with `npm org ls openlfcp <your-user>`.
- [ ] Logged in on this machine: `npm login`, then `npm whoami`.
- [ ] Node 24 or later and pnpm 10, as in sdk-ts `packageManager`.
- [ ] An authenticator ready: every publish asks for a one-time code (`--otp`).

## 2. Pre-flight

- [ ] The release-candidate commit of sdk-ts is on `main` and pushed. Its
      version is `0.1.0-rc.1` in all eight `packages/*/package.json`.
- [ ] CI is green on that commit, and the release-candidate verification
      (`.github: scripts/rc-verify.py`, see [rc-verification.md](rc-verification.md))
      passed for the RC that contains it.
- [ ] A clean checkout at exactly that commit: `git status` shows nothing,
      and `git rev-parse HEAD` is the commit you checked.
- [ ] `pnpm install --frozen-lockfile && pnpm build` succeeds.
- [ ] `pnpm release:check` prints `release check PASSED`. It checks, without
      publishing:
  - the files of each tarball (`dist/` JavaScript and declarations,
    README, LICENSE, package.json only);
  - the rewritten `@openlfcp/*` dependency ranges (`^0.1.0-rc.1`);
  - publishConfig (`access: public`, `tag: next`);
  - a fresh-project install with a smoke import of every package.
- [ ] None of the versions exists yet: `npm view @openlfcp/core@0.1.0-rc.1`
      should answer 404. A published version can never be published again.

## 3. Publish, in dependency order

From the sdk-ts root, one package at a time, each with a fresh one-time
code. Every package also has `publishConfig.tag: "next"`; the explicit
`--tag next` is a second guard. `pnpm publish` rewrites `workspace:^`
dependencies to `^0.1.0-rc.1` and refuses a dirty tree or a branch other
than `main`. Do not bypass that with `--no-git-checks`.

| # | Package | Command |
| --- | --- | --- |
| 1 | `@openlfcp/core` | `pnpm --filter @openlfcp/core publish --tag next --otp=<code>` |
| 2 | `@openlfcp/crypto` | `pnpm --filter @openlfcp/crypto publish --tag next --otp=<code>` |
| 3 | `@openlfcp/storage` | `pnpm --filter @openlfcp/storage publish --tag next --otp=<code>` |
| 4 | `@openlfcp/wire` | `pnpm --filter @openlfcp/wire publish --tag next --otp=<code>` |
| 5 | `@openlfcp/storage-node` | `pnpm --filter @openlfcp/storage-node publish --tag next --otp=<code>` |
| 6 | `@openlfcp/storage-idb` | `pnpm --filter @openlfcp/storage-idb publish --tag next --otp=<code>` |
| 7 | `@openlfcp/shared-objects` | `pnpm --filter @openlfcp/shared-objects publish --tag next --otp=<code>` |
| 8 | `@openlfcp/client` | `pnpm --filter @openlfcp/client publish --tag next --otp=<code>` |

Each package comes after every `@openlfcp/*` package it depends on:
- crypto, storage → core;
- wire → core, crypto;
- storage-node, storage-idb → core, storage;
- shared-objects → core, crypto;
- client → core, crypto, storage, wire.

`pnpm release:check` fails if a package depends on one published after it.

To see exactly what a command will upload before running it, add
`--dry-run` (no code needed).

## 4. Verify

- [ ] Each package is on `next`:

  ```sh
  for p in core crypto storage wire storage-node storage-idb shared-objects client; do
    npm view @openlfcp/$p dist-tags --json
  done
  ```

  Expect `"next": "0.1.0-rc.1"` for each. On a first publish expect
  `"latest": "0.1.0-rc.1"` too (npm always creates `latest`); for a package
  that already had a `latest`, it is unchanged.
- [ ] The metadata looks right:
  `npm view @openlfcp/client@next version dependencies license repository`.
- [ ] A fresh project installs and imports everything from the registry:

  ```sh
  mkdir /tmp/openlfcp-npm-check && cd /tmp/openlfcp-npm-check && npm init -y >/dev/null
  npm pkg set type=module
  npm install @openlfcp/core@next @openlfcp/crypto@next @openlfcp/storage@next \
    @openlfcp/wire@next @openlfcp/storage-node@next @openlfcp/storage-idb@next \
    @openlfcp/shared-objects@next @openlfcp/client@next
  node --input-type=module -e 'for (const p of ["core","crypto","storage","wire","storage-node","storage-idb","shared-objects","client"]) await import(`@openlfcp/${p}`); console.log("all eight import")'
  ```

- [ ] Record the published versions and the sdk-ts commit in the release
      notes ([mvp-0.1-release-notes.md](mvp-0.1-release-notes.md)).

## 5. If a publish fails midway

Packages already published stay published, and their version can never be
reused.

- **Rejected before upload** (wrong or expired code, network, not logged
  in): fix the cause and run the same command again for that package, then
  continue with the next one in order. Nothing was published for it.
- **Some packages are out, a later one cannot be published at all** (e.g.
  a broken tarball): the ones already out are on `next`, and on a first
  publish also on `latest`, so a plain `npm install` gets them too.
  - Do not unpublish.
  - Fix the cause in sdk-ts and move all eight packages to the next
    prerelease (`0.1.0-rc.2`), so versions stay aligned.
  - Run `pnpm release:check` again and publish all eight in order.
  - Mark the incomplete set: `npm deprecate @openlfcp/<pkg>@0.1.0-rc.1 "incomplete release; use 0.1.0-rc.2"`.
- **A package published with a defect:** the same, a new prerelease for
  all eight, and deprecate the bad version. Unpublishing is limited by npm
  (72 hours, no dependents) and breaks anyone who installed it.

## Promotion

`0.1.0-rc.1` is on `next`, and, being the first publish, on `latest` too,
which is harmless while it is the only version. The final `0.1.0` goes
straight to `latest` (below), and `next` then moves to it too.

A later release candidate of a package that is already published
(`0.1.0-rc.2` …) goes out with `--tag next` as above, and then `latest`
stays where it was: only the first publish of a package sets `latest`
regardless of `--tag`.

## Final release 0.1.0

The final release publishes `0.1.0` of all eight packages from sdk-ts
4e1b02f, under `latest`. Every package there has `version: "0.1.0"` and
`publishConfig.tag: "latest"`; `pnpm release:check` expects `latest` for a
final version and `next` for a prerelease.

1. **Prerequisites and pre-flight:** sections 1 and 2, with these values:
   - sdk-ts at 4e1b02f (tag `v0.1.0`), pushed, CI green;
   - `pnpm release:check` prints `version 0.1.0, dist-tag latest` and
     `release check PASSED`;
   - `npm view @openlfcp/core@0.1.0` answers 404.
2. **Publish, in the same order,** each with a fresh one-time code:

   | # | Package | Command |
   | --- | --- | --- |
   | 1 | `@openlfcp/core` | `pnpm --filter @openlfcp/core publish --tag latest --otp=<code>` |
   | 2 | `@openlfcp/crypto` | `pnpm --filter @openlfcp/crypto publish --tag latest --otp=<code>` |
   | 3 | `@openlfcp/storage` | `pnpm --filter @openlfcp/storage publish --tag latest --otp=<code>` |
   | 4 | `@openlfcp/wire` | `pnpm --filter @openlfcp/wire publish --tag latest --otp=<code>` |
   | 5 | `@openlfcp/storage-node` | `pnpm --filter @openlfcp/storage-node publish --tag latest --otp=<code>` |
   | 6 | `@openlfcp/storage-idb` | `pnpm --filter @openlfcp/storage-idb publish --tag latest --otp=<code>` |
   | 7 | `@openlfcp/shared-objects` | `pnpm --filter @openlfcp/shared-objects publish --tag latest --otp=<code>` |
   | 8 | `@openlfcp/client` | `pnpm --filter @openlfcp/client publish --tag latest --otp=<code>` |

3. **Move `next` to 0.1.0 too**, so `next` never lags behind `latest`, in
   the same order:

   ```sh
   npm dist-tag add @openlfcp/core@0.1.0 next --otp=<code>
   npm dist-tag add @openlfcp/crypto@0.1.0 next --otp=<code>
   npm dist-tag add @openlfcp/storage@0.1.0 next --otp=<code>
   npm dist-tag add @openlfcp/wire@0.1.0 next --otp=<code>
   npm dist-tag add @openlfcp/storage-node@0.1.0 next --otp=<code>
   npm dist-tag add @openlfcp/storage-idb@0.1.0 next --otp=<code>
   npm dist-tag add @openlfcp/shared-objects@0.1.0 next --otp=<code>
   npm dist-tag add @openlfcp/client@0.1.0 next --otp=<code>
   ```

4. **Verify:**

   ```sh
   for p in core crypto storage wire storage-node storage-idb shared-objects client; do
     printf '%s ' "@openlfcp/$p"
     npm view "@openlfcp/$p" dist-tags --json | tr -d ' \n'
     echo
   done
   ```

   Expect `"latest":"0.1.0","next":"0.1.0"` for each. Then run the
   fresh-project install of section 4 with `@latest` in place of `@next`,
   and check the metadata with
   `npm view @openlfcp/client@latest version dependencies license repository`:
   every `@openlfcp/*` dependency is `^0.1.0`.
5. **If a publish fails midway:** section 5 applies, with `0.1.1` as the
   next version (a final version cannot be republished either), and
   `npm deprecate @openlfcp/<pkg>@0.1.0 "incomplete release; use 0.1.1"`
   for the incomplete set.

## Patch release 0.1.1

The patch release publishes `0.1.1` of all eight packages from sdk-ts
ab0a49a, under `latest`. It adds POST-017, the terminal refusal of a
Resource, in `@openlfcp/client`; the Shared Tasks plugin needs it in order
to depend on published packages. What changed is in
`sdk-ts: CHANGELOG.md`. Nothing is removed or renamed. Two changes may
matter to an existing client:
- a Resource refused with a terminal code is no longer opened again after
  a reconnect;
- `SyncEvent` has a new member, `resource-refused`.

1. **Pre-flight**, from a clean sdk-ts checkout at ab0a49a, pushed and CI
   green:

   ```sh
   git status --short                          # empty
   git log -1 --format=%h                      # ab0a49a
   pnpm install --frozen-lockfile
   pnpm release:check                          # "version 0.1.1, dist-tag latest", "release check PASSED"
   npm whoami                                  # the account that owns @openlfcp
   npm view @openlfcp/core@0.1.1 version       # E404: not published yet
   ```

   `release:check` was PASSED on a fresh clone of ab0a49a on 2026-10-07.
   Every `@openlfcp/*` dependency packs as `^0.1.1`, and the total is
   277.9 KiB.
2. **Publish, in dependency order,** each with a fresh one-time code:

   | # | Package | Command |
   | --- | --- | --- |
   | 1 | `@openlfcp/core` | `pnpm --filter @openlfcp/core publish --tag latest --otp=<code>` |
   | 2 | `@openlfcp/crypto` | `pnpm --filter @openlfcp/crypto publish --tag latest --otp=<code>` |
   | 3 | `@openlfcp/storage` | `pnpm --filter @openlfcp/storage publish --tag latest --otp=<code>` |
   | 4 | `@openlfcp/wire` | `pnpm --filter @openlfcp/wire publish --tag latest --otp=<code>` |
   | 5 | `@openlfcp/storage-node` | `pnpm --filter @openlfcp/storage-node publish --tag latest --otp=<code>` |
   | 6 | `@openlfcp/storage-idb` | `pnpm --filter @openlfcp/storage-idb publish --tag latest --otp=<code>` |
   | 7 | `@openlfcp/shared-objects` | `pnpm --filter @openlfcp/shared-objects publish --tag latest --otp=<code>` |
   | 8 | `@openlfcp/client` | `pnpm --filter @openlfcp/client publish --tag latest --otp=<code>` |

   `publishConfig.access` is `public` in every package, so `pnpm publish`
   needs no `--access public`.
3. **Move `next` to 0.1.1 too**, so that `next` never lags `latest`:

   ```sh
   for p in core crypto storage wire storage-node storage-idb shared-objects client; do
     npm dist-tag add "@openlfcp/$p@0.1.1" next --otp=<code>
   done
   ```

4. **Verify:**

   ```sh
   for p in core crypto storage wire storage-node storage-idb shared-objects client; do
     printf '%s ' "@openlfcp/$p"
     npm view "@openlfcp/$p" dist-tags --json | tr -d ' \n'
     echo
   done                                        # each: "latest":"0.1.1","next":"0.1.1"
   npm view @openlfcp/client@0.1.1 version dependencies   # every @openlfcp/* dependency ^0.1.1

   mkdir /tmp/openlfcp-npm-011 && cd /tmp/openlfcp-npm-011 && npm init -y >/dev/null
   npm pkg set type=module
   npm install @openlfcp/core@0.1.1 @openlfcp/crypto@0.1.1 @openlfcp/storage@0.1.1 \
     @openlfcp/wire@0.1.1 @openlfcp/storage-node@0.1.1 @openlfcp/storage-idb@0.1.1 \
     @openlfcp/shared-objects@0.1.1 @openlfcp/client@0.1.1
   node --input-type=module -e 'for (const p of ["core","crypto","storage","wire","storage-node","storage-idb","shared-objects","client"]) await import(`@openlfcp/${p}`); const { TERMINAL_RESOURCE_CODES } = await import("@openlfcp/client"); console.log("all eight import; RESOURCE_NOT_HOSTED terminal:", TERMINAL_RESOURCE_CODES.has("RESOURCE_NOT_HOSTED"))'
   ```

   The last line prints `all eight import; RESOURCE_NOT_HOSTED terminal: true`.
5. **Tag the release commit**, as for 0.1.0:

   ```sh
   git tag -a v0.1.1 ab0a49a -m "OpenLFCP sdk-ts 0.1.1"
   git push origin v0.1.1
   ```

6. **If a publish fails midway:** section 5 applies, with `0.1.2` as the
   next version, and
   `npm deprecate @openlfcp/<pkg>@0.1.1 "incomplete release; use 0.1.2"`
   for the incomplete set.

## Patch release 0.1.2

The patch release publishes `0.1.2` of all eight packages from sdk-ts
5bf4036, under `latest`. It is the 0.1.x sustaining release of MVP 0.2
wave W0: spec `mvp-0.1-baseline.9` (ADR 0008, recovery after server data
loss; POST-001, held actor-sequence collisions) and the profile check of
`acceptInvitation` (LFCP-02-086), which Shared Tasks 0.3.2 needs. What
changed is in `sdk-ts: CHANGELOG.md`. Nothing is removed or renamed. What
may matter to an existing client:
- a server that lacks objects the client holds is sent them again, and a
  Resource a route lost is hosted again from its Genesis (new `rehost`
  event);
- `ApplyOutcome` has the new member `profile-held`, the storage status
  `profile-held`, `NackOutcome` the member `needs-offer`, and
  `AcceptedInvitation` the member `profile-unsupported` (only with the new
  `dataProfiles` option): a `switch` that checks exhaustiveness needs a
  case for each;
- a Shared Objects change whose actor and sequence number another change
  has is held, no longer refused with `ACTOR_EQUIVOCATION`.

Its CI needs the spec tag `mvp-0.1-baseline.9` (f42533c) and server
30f592d (0.3.0, `server.lock`) pushed first.

1. **Pre-flight**, from a clean sdk-ts checkout at 5bf4036, pushed and CI
   green:

   ```sh
   git status --short                          # empty
   git log -1 --format=%h                      # 5bf4036
   pnpm install --frozen-lockfile
   pnpm release:check                          # "version 0.1.2, dist-tag latest", "release check PASSED"
   npm whoami                                  # the account that owns @openlfcp
   npm view @openlfcp/core@0.1.2 version       # E404: not published yet
   ```

   `release:check` was PASSED at 5bf4036 on 2026-10-08. Every
   `@openlfcp/*` dependency packs as `^0.1.2`, and the total is 283.6 KiB.
2. **Publish, in dependency order,** each with a fresh one-time code:

   | # | Package | Command |
   | --- | --- | --- |
   | 1 | `@openlfcp/core` | `pnpm --filter @openlfcp/core publish --tag latest --otp=<code>` |
   | 2 | `@openlfcp/crypto` | `pnpm --filter @openlfcp/crypto publish --tag latest --otp=<code>` |
   | 3 | `@openlfcp/storage` | `pnpm --filter @openlfcp/storage publish --tag latest --otp=<code>` |
   | 4 | `@openlfcp/wire` | `pnpm --filter @openlfcp/wire publish --tag latest --otp=<code>` |
   | 5 | `@openlfcp/storage-node` | `pnpm --filter @openlfcp/storage-node publish --tag latest --otp=<code>` |
   | 6 | `@openlfcp/storage-idb` | `pnpm --filter @openlfcp/storage-idb publish --tag latest --otp=<code>` |
   | 7 | `@openlfcp/shared-objects` | `pnpm --filter @openlfcp/shared-objects publish --tag latest --otp=<code>` |
   | 8 | `@openlfcp/client` | `pnpm --filter @openlfcp/client publish --tag latest --otp=<code>` |

3. **Move `next` to 0.1.2 too:**

   ```sh
   for p in core crypto storage wire storage-node storage-idb shared-objects client; do
     npm dist-tag add "@openlfcp/$p@0.1.2" next --otp=<code>
   done
   ```

4. **Verify:**

   ```sh
   for p in core crypto storage wire storage-node storage-idb shared-objects client; do
     printf '%s ' "@openlfcp/$p"
     npm view "@openlfcp/$p" dist-tags --json | tr -d ' \n'
     echo
   done                                        # each: "latest":"0.1.2","next":"0.1.2"
   npm view @openlfcp/client@0.1.2 version dependencies   # every @openlfcp/* dependency ^0.1.2

   mkdir /tmp/openlfcp-npm-012 && cd /tmp/openlfcp-npm-012 && npm init -y >/dev/null
   npm pkg set type=module
   npm install @openlfcp/core@0.1.2 @openlfcp/crypto@0.1.2 @openlfcp/storage@0.1.2 \
     @openlfcp/wire@0.1.2 @openlfcp/storage-node@0.1.2 @openlfcp/storage-idb@0.1.2 \
     @openlfcp/shared-objects@0.1.2 @openlfcp/client@0.1.2
   node --input-type=module -e 'for (const p of ["core","crypto","storage","wire","storage-node","storage-idb","shared-objects","client"]) await import(`@openlfcp/${p}`); const { ERROR_CODE, haveDifference } = await import("@openlfcp/wire"); console.log("all eight import; UNKNOWN_PREVIOUS:", ERROR_CODE.UNKNOWN_PREVIOUS, typeof haveDifference)'
   ```

   The last line prints `all eight import; UNKNOWN_PREVIOUS: 23n function`.
5. **Tag the release commit:**

   ```sh
   git tag -a v0.1.2 5bf4036 -m "OpenLFCP sdk-ts 0.1.2"
   git push origin v0.1.2
   ```

6. **If a publish fails midway:** section 5 applies, with `0.1.3` as the
   next version, and
   `npm deprecate @openlfcp/<pkg>@0.1.2 "incomplete release; use 0.1.3"`
   for the incomplete set.
