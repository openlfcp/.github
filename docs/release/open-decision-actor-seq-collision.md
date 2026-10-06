# Open decision: two changes with the same actor and sequence number

**Status:** decided by the project owner on 2026-10-06 (see Decision). It
was the one open spec question left after SPEC-PATCH-08
(`mvp-0.1-baseline.8`). Prepared 2026-10-06.

## Decision

The project owner accepted the recommendation on 2026-10-06:
- MVP 0.1 ships with today's behaviour: refuse, which is safe by default.
- Option B (hold and retry) is adopted for the next baseline, with the spec
  text, vectors and both SDKs. It is tracked as POST-001 in
  `BACKLOG-MVP-0.1.md` §6.

**Question.** A replica holds an Automerge change from actor X with
sequence number *n*. It then receives a *different* change from X, also
numbered *n*, in a later LFCP Data Unit that otherwise validates. Which one
does it keep?

**Today.** Both SDKs refuse the second change (`ACTOR_EQUIVOCATION`), and the
spec says nothing. Nothing is merged and nothing crashes: every change is
checked before the Automerge engine sees it (§11.1).

## How it happens

1. **The honest corner.** It needs an equivocation and partial visibility.
   - Writer A equivocates: two different units at one LFCP sequence, for
     example after restoring a device from a backup.
   - Collaborator C saw only one of them, X, and wrote change *c* on top
     of it.
   - C later sees both. §26.2 excludes X and Y, and §14.1 also excludes
     *c*, because it depends on X.
   - C re-issues its work as *c′*. Since baseline.6 (§9), *c′* may reuse
     *c*'s Automerge sequence number.
   - Replica R, which still has X and *c*, receives *c′*: a collision.

   Nothing else produces one for honest writers. In the epoch-cutoff case, a
   replica must know the Key Epoch Record before it can accept the
   re-issued unit, so it has already dropped the old change.
2. **A malicious writer.** It sends two units whose changes share an
   Automerge sequence number. A malicious writer can already split replicas
   one level lower, by forking its own LFCP chain: two units with the same
   `previous`, each replica keeping whichever arrives first. So no
   Automerge-level rule can make its history converge. The goal is
   convergence for honest writers and contained damage for malicious ones.

## Options

| | A. Refuse (status quo, written down) | B. Hold and retry (recommended) | C. Lowest LFCP sequence wins |
| --- | --- | --- | --- |
| Rule | The first change merged keeps the number. Any later change with it is refused for good | A replica never merges two changes with the same number. The later one is *held*, not refused, and retried whenever a rebuild (§14.1) removes changes | Among accepted units carrying changes with the same number, only the one with the lowest LFCP sequence that is not excluded is merged; the others are held |
| Honest corner | Never heals. R keeps *c* and refuses *c′* even after it learns of Y, and C's later edits depend on *c′*, so R never shows them | Heals once R learns of the equivocation, like the LFCP rule itself: the rebuild drops *c*, and the held *c′* applies | Heals in the same way |
| Malicious writer | The order of arrival decides, per replica. Damage stays within that writer's own history and the work built on it | Same as A | Deterministic across replicas (a function of the accepted set). But it needs an index of numbers over accepted, not yet decoded units, and it holds a later change behind an earlier one that may never apply |
| Spec text | One sentence in §14.1: "a receiver refuses a change whose actor and sequence number match a different change it holds" | One paragraph in §14.1: never merge two changes with one number; hold the later one; retry after any rebuild | About half a page in §14.1, plus vectors, and a definition of "claims a number" for units the profile has not merged |
| Cost per SDK | None | About one day. sdk-ts: map the profile's `ACTOR_EQUIVOCATION` to a held unit instead of `profile-rejected`, and retry held units after `exclude`/rebuild (the hooks exist). sdk-rs: the same. Plus vectors (a held change applying after the rebuild) | Two to three days each, plus vectors. The re-evaluation on every exclusion is where bugs hide |

**Rejected: the latest unit wins.** Letting a re-issued change replace a
merged one would let any writer erase everyone's later work. Every change
that depends on the replaced one, in practice all later history, would be
excluded.

## Recommendation

**Ship MVP 0.1 with today's behaviour, and adopt B in the next baseline.**
B fixes the only honest case, costs about a day per SDK, and adds no new
abuse.

**What C adds over B.** Determinism against a malicious writer. That writer
can already break convergence at the LFCP level, so C buys little for
real cost.

**One cheap step whichever option is chosen.** Surface the refusal or hold
to the user ("a change from <collaborator> could not be applied"). Today it
is silent.

## If MVP 0.1 ships as it is

**Is it safe by default?** Yes:
- nothing invalid is merged, the engine never sees the colliding change,
  and nothing crashes;
- the stored unit is kept, marked `profile-rejected` (sdk-ts);
- the security properties hold: authenticity, confidentiality and
  authorization are unaffected.

**What a user sees.** Only in the corner above:
- one replica (R) stops showing one collaborator's edits to the shared
  tasks;
- there is no error or notice; the Obsidian plugin does not surface
  `profile-rejected`;
- the other replicas are unaffected.

**How it recovers.** It may not:
- the refusal is permanent on that replica;
- re-joining from a fresh install rebuilds from the same units, and can hit
  the same collision while the server serves only one side of the
  equivocation;
- with B, R heals by itself once it learns of the equivocation.

**How likely.** It needs a writer who equivocates (a device restored from a
backup or cloned, or a malicious writer), and a replica that saw only one
side. That is rare in MVP use. The release notes list it as a known
limitation.
