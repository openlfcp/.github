# Engineering conventions

How work is done across the `openlfcp` repositories. The rules here describe
what the project actually does today (**bootstrap mode**) and the policy it
moves to once the repositories are on GitHub (**target mode**). Agents also
follow [AGENT-OPERATING-GUIDE.md](AGENT-OPERATING-GUIDE.md); this document
links to it rather than repeating it.

## 1. Where these files live

This `.github` repository provides organization-wide defaults. GitHub serves
its `CONTRIBUTING.md`, `SECURITY.md`, issue templates and pull request
template to every `openlfcp` repository that has none of its own, so the
other repositories do **not** carry copies.

Two files are *not* inherited by other repositories:

- `.github/CODEOWNERS` applies to this repository only. A repository that
  needs code owners adds its own when it goes to GitHub.
- `.github/labels.yml` is the source of truth for issue labels. Labels must
  be created in each repository, by hand or by a label-sync tool, once
  remotes exist.

## 2. Working modes

### Bootstrap mode (current)

- Repositories are local only: no remotes, no pull requests.
- An orchestrator assigns one LFCP issue at a time to a coding agent, which
  reports back in the BASE PROMPT final-response format.
- Commits go directly to `main`.
- Every commit must pass the repository's validation command (section 4)
  **before** it is made: `./scripts/validate.sh && committer …`, never with
  `;`.
- The validation runs on the working tree, not on the commit. After
  committing, `git status` must show no leftover change that belongs to the
  same logical change, such as a regenerated file left unstaged.
- History is never rewritten: no amend, squash, rebase or force-push of
  published commits.
- A commit that slips through red is not repaired by rewriting. It is fixed
  by the next commit, reported, and recorded so `git bisect skip` can step
  over it. Known red commits:

  | Repository | Commit | Fixed by |
  | --- | --- | --- |
  | `spec` | `12732bb` | `353c946` |
  | `spec` | `bb81131` | `3e4cb79` |

### Target mode (later)

- One branch per issue: `lfcp-NNN-short-slug`, for example
  `lfcp-013-deterministic-cbor`.
- Parallel agents each work in their own git worktree on their own branch.
- Changes land through pull requests that use the template.
- History stays linear: rebase or fast-forward, no merge commits.
- `main` stays green. CI runs the same validation command as bootstrap mode.

**Switching from bootstrap to target mode is a decision for the project
owner**, taken per repository when its remote is created.

## 3. Commits

- **Conventional Commits**: `type(scope): summary`.
  - Types in use: `feat`, `fix`, `docs`, `test`, `build`, `refactor`,
    `chore`.
  - Scope is the area or component, for example `spec`, `wire`, `vectors`,
    `schemas`, `profiles`, `scripts`, `backlog`, `bootstrap`.
- The summary is one clean sentence in the imperative. Do not join two
  changes with "and"; make two commits.
- The body explains why. It names the LFCP issue (`LFCP-007.`) and any spec
  gap it touches.
- **Atomic**: one logical change per commit, and every commit builds and
  validates on its own, so `git bisect` works. Refactors and behavior changes
  are separate commits.
- Commits are made with `committer`, which stages exactly the listed paths.
  `git add` is not used, so parallel work is never swept in.
- Agent commits end with a `Co-Authored-By:` trailer naming the model.

## 4. Validation commands

| Repository | From a clean checkout |
| --- | --- |
| `spec` | `pnpm install --frozen-lockfile && bundle install && ./scripts/validate.sh` |
| `.github` | `./scripts/validate.sh` |
| `sdk-ts`, `server`, `obsidian`, `examples` | `pnpm install --frozen-lockfile && pnpm run build && pnpm test` |
| `sdk-rs` | `cargo fmt --all --check && cargo clippy --workspace --all-targets -- -D warnings && cargo test --workspace` |

`spec` also needs its full Git history, because it checks vector values
against the commit they were migrated from.

## 5. Issue labels

[`../.github/labels.yml`](../.github/labels.yml) lists every label with its
color and meaning. The dimensions are:

- `area:*`: protocol, wire, crypto, control-plane, data-plane, profile,
  storage, server, obsidian, interop, ci;
- `type:*`: feature, test, docs, infra, bug;
- `priority:*`: p0, p1, p2;
- status: `blocked`, `agent-ready`, `needs-protocol-decision`.

## 6. Versioning

| Thing | Rule |
| --- | --- |
| **Working Draft** specification (e.g. `LFCP-WIRE-01`, `SHARED-OBJECTS-PROFILE-01` today) | Mutable in place. Corrections go into the canonical document; Git history is the changelog. No `.1` or errata files. |
| **Stable** specification | Never silently rewritten. Compatible clarifications use errata; incompatible changes get a new identifier (e.g. `LFCP-WIRE-02`) through an RFC. |
| **Implementation and package versions** (`sdk-ts`, `sdk-rs`, `server`, `obsidian`) | Semantic Versioning. `0.x` while pre-1.0, so breaking changes may land in minor versions. |
| **MVP 0.1 baseline** | A frozen, tagged commit of `spec` (planned tag `mvp-0.1-baseline`, created by LFCP-010) that implementations pin. |

**MVP 0.1 does not make LFCP-WIRE-01 Stable.** The baseline is a snapshot of
Working Drafts that the first implementations agree to build against.
Stabilization is a separate, later decision.

Implementations pin the specification and its vectors to a `spec` commit or
tag, never to a moving branch. The pinning mechanism belongs to LFCP-017.

## 7. Changing a normative specification

For a **Working Draft**, one coordinated change updates everything that
depends on the text:

1. the canonical document (`wire/LFCP-WIRE-01.md`,
   `profiles/SHARED-OBJECTS-PROFILE-01.md`, …);
2. the vector generator, then the regenerated vectors (`.json` and `.md`).
   Vector bytes are never written by hand;
3. derived artifacts: the extracted CDDL (`node scripts/extract-cddl.mjs`),
   the supplement, schemas and fixtures;
4. the migration mapping, only when a published value changes on purpose
   and that change is approved.

The reproducibility checks in `./scripts/validate.sh` must stay green: the
generators reproduce the committed files byte for byte, the extracted CDDL
matches the prose, and every published value is accounted for.

A **Stable** specification is changed only by errata, a new version or an
RFC (section 6).

## 8. Specification gaps

AGENT-OPERATING-GUIDE.md §10 defines the gap protocol. In practice:

1. An agent that finds ambiguous or contradictory normative text **does not
   choose**. It reports the gap with the exact location, the options and a
   recommendation, and keeps working on everything else.
2. The orchestrator records the gap under a stable ID (for example `C1`,
   `G2`, `SO-G4`) and routes it to the project owner.
3. **The project owner decides**, as protocol owner.
4. A spec-patch task applies the decision as one Working Draft change
   (section 7). Only then may implementations depend on it.

Use the "Protocol / spec gap" issue form once issues are on GitHub.

## 9. Security

Report vulnerabilities privately through GitHub's private vulnerability
reporting, as described in [`../SECURITY.md`](../SECURITY.md).
