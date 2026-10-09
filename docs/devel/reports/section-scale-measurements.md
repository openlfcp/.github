# Shared section scale: history growth, admission and server storage

**Task:** LFCP-02-067, its SDK and server side (the plugin's measurements
are the task's own). **Date:** 2026-10-09. **Audience:** obsidian
(LFCP-02-067, -068), sdk-ts (LFCP-02-025 coalescing), sdk-rs.

## 1. How to reproduce

| Part | Command | Source |
| --- | --- | --- |
| History growth, admission, authoring | `cargo run --release -p lfcp --features shared-sections --example section_scale -- [growth\|admission\|authoring\|all] [--quick]` | sdk-rs `crates/lfcp/examples/section_scale.rs` (`b693197`) |
| Server storage and transfer | `cargo test --release -p lfcp-server --test section_scale -- --ignored --nocapture` | server `crates/lfcp-server/tests/section_scale.rs` (`e1ba366`) |

Each prints a table and one JSON line per part. Measured on an Apple M3 Pro
(11 cores, 18 GiB), macOS 26.5.2, rustc 1.99.0, release builds, one
thread, sdk-rs `9c6e639`, server `8193b06` (built against the sdk-rs
checkout).

**Workload.** One writer types into one paragraph of a shared section.
The text is prose-like: words from a fixed vocabulary in a fixed xorshift
stream with punctuation, because a repeated sentence compresses to almost
nothing in a save and would understate it. `k` is the coalescing: the
characters one change (one Data Unit) carries. Typing is written as
Automerge `splice_text` on the section document, the operations
`SectionsDoc::text_edit` writes (§5 explains why not through it). W200 is
the import of 200 Task nodes, each with a paragraph of about 200
characters, one change per node.

## 2. History growth (PS-10: long typing)

| Characters | k | Changes (units) | Data Unit bytes | Bytes per character | Save bytes | §13.1 largest column | §13.1 group sum |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10,000 | 1 | 10,002 | 4,102,838 | 410 | 3,758 | 10,027 | 10,001 |
| 10,000 | 16 | 627 | 268,751 | 26.9 | 3,750 | 10,027 | 626 |
| 10,000 | 128 | 81 | 44,786 | 4.5 | 3,752 | 10,027 | 80 |
| 10,000 | 1,024 | 12 | 15,746 | 1.6 | 3,745 | 10,027 | 11 |
| 10,000 | 8,192 | 4 | 12,390 | 1.2 | 3,744 | 10,027 | 3 |
| 50,000 | 1 | 50,002 | 20,610,101 | 412 | 14,480 | 50,027 | 50,001 |
| 50,000 | 16 | 3,127 | 1,343,353 | 26.9 | 14,471 | 50,027 | 3,126 |
| 50,000 | 128 | 393 | 217,124 | 4.3 | 14,475 | 50,027 | 392 |
| 50,000 | 1,024 | 51 | 72,226 | 1.4 | 14,466 | 50,027 | 50 |
| 250,000 | 1 | 250,002 | 103,579,035 | 414 | 64,549 | 250,027 | 250,001 |
| 250,000 | 16 | 15,627 | 6,718,353 | 26.9 | 64,548 | 250,027 | 15,626 |
| 250,000 | 128 | 1,956 | 1,081,392 | 4.3 | 64,543 | 250,027 | 1,955 |
| 250,000 | 1,024 | 247 | 355,254 | 1.4 | 64,544 | 250,027 | 246 |
| 250,000 | 8,192 | 33 | 264,812 | 1.1 | 64,536 | 250,027 | 32 |
| 50,000, every 10th key a backspace | 16 | 3,127 | 1,332,970 | 26.7 | 16,355 | 40,027 | 3,126 |

Findings:

- **The Snapshot floor is reached by typed characters, not by changes.**
  The largest column of the save (SHARED-OBJECTS-PROFILE-01 §13.1) is the
  number of characters ever inserted plus 27 (the section and paragraph),
  whatever the coalescing; a deleted character stays an operation (the
  backspace run counts the 40,000 inserted ones). The group sum is the
  number of changes (their dependencies). So a section reaches the floor
  of 262,144 after about **262,100 inserted characters of history**, with
  any k ≥ 1; at k = 1 the group sum reaches it at about the same point.
  Beyond it, a receiver with floor limits rejects the section's Snapshot
  and replays every unit (SOP §13.1); §16.4 forbids pruning history, so the
  section stays past the floor.
- **A Data Unit costs about 277 bytes beyond its plaintext** (header,
  signature, AEAD tag, framing): 133 bytes of plaintext and 410 bytes of
  unit for one character. Coalescing decides the bytes per character:
  410 at k = 1, 27 at k = 16, 4.3 at k = 128, 1.4 at k = 1,024.
- The save stays small (64 KiB for 250,000 characters): the history's cost
  is in the units and in the column counts, not in the save's bytes.

## 3. Server: storage, quota and transfer

| Characters | k | Units | Data Unit bytes | Quota bytes (Resource) | DATA_PUT, 1 unit per message | DATA_PUT, 64 per message | DATA_GET of all |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10,000 | 1 | 10,002 | 4,102,838 | 4,103,273 | 345 µs/unit | 109 µs/unit | 18 ms |
| 50,000 | 16 | 3,127 | 1,343,353 | 1,343,788 | 336 µs/unit | 117 µs/unit | 6 ms |
| 50,000 | 128 | 393 | 217,124 | 217,559 | 329 µs/unit | 123 µs/unit | 0.9 ms |
| 50,000 | 1,024 | 51 | 72,226 | 72,661 | 336 µs/unit | 124 µs/unit | 0.4 ms |

- The Resource quota counts the stored objects' bytes: the units plus the
  Genesis (435 bytes). The SQLite files grew by up to about twice that
  (indexes, WAL; the figure varies with checkpoints and is not reported as
  a measurement).
- A DATA_PUT with one unit costs about 0.34 ms on the server, including
  its durable commit (`synchronous = FULL`, not measured apart); batching
  amortizes it to about 0.12 ms per unit. Live typing sends far fewer than the default limit of
  50 messages per second (raised here to measure the server, not the
  limiter).

**When does the 128 MiB Resource quota fill?** Bytes per character from §2;
2,000 characters a day is a steady writer in one section, 10,000 a heavy
one:

| k | Characters to fill 128 MiB | At 2,000 a day | At 10,000 a day |
| ---: | ---: | ---: | ---: |
| 1 | 327,000 | 5.4 months | 1.1 months |
| 16 | 5.0 million | 6.8 years | 1.4 years |
| 128 | 31 million | decades | 8.5 years |
| 1,024 | 95 million | decades | decades |

The Snapshot floor comes first at any k ≥ 16: 262,100 characters are
**4.3 months at 2,000 a day, 26 days at 10,000 a day.**

## 4. Admission: `SectionsReplica::receive` (sdk-rs, after `d2a2b77`)

| Workload | Units | Total | p50 per unit | p99 per unit | Last tenth, mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| W200 import, in order | 401 | 40.3 s | 101 ms | 201 ms | 194 ms |
| W200 import, reversed with duplicates | 802 | 40.3 s | 0.05 ms (waiting) | 0.09 ms | 497 ms |
| Typing 50,000 characters, k = 16 | 3,127 | 25.0 s | 7.9 ms | 17.0 ms | 14.9 ms |
| Typing 50,000 characters, k = 128 | 393 | 3.5 s | 8.7 ms | 17.9 ms | 16.4 ms |

**Admission is linear in the document per change, so a catch-up is
quadratic.** A profile of the W200 run puts about 98% of the time in the
structural rules (§14.1, `structural_refusal`): they collect every node of
the document before and after the change (`SectionsDoc::nodes`) and look
up each node's fields in both (`get_for`). The §11.3/§11.4 checks
(`History`) are about 5%. The SDK's authoring of the import is quadratic
for the same reason: `create_node` computes the effective tree
(`insertion_index` → `effective`) on every node.

## 5. Authoring: `SectionsDoc::text_edit`

| Text length | Time per one-character edit |
| ---: | ---: |
| 1,000 | 59 µs |
| 10,000 | 350 µs |
| 50,000 | 1.7 ms |
| 200,000 | 6.4 ms |

`text_edit` reads the node's Text at the base heads and compares it with
the current Text on every call (the stale-base check), so each edit costs
the Text's length; typing 250,000 characters one per change through it
would take hours. That is why §2 types with `splice_text`.

## 6. Recommendations

For sdk-ts (LFCP-02-025) and the plugin:

1. **Coalesce Text edits into one change per typing burst**, not per key:
   flush after an idle pause of 1–2 s, at a paragraph boundary, before a
   structural intent, and at least every 256 characters while typing
   continues; the §16.2 Text budget (8,192 operations) is the hard cap.
   This keeps the bytes per character near 4–27 instead of 410 (100× less
   quota, server writes and catch-up units) and the group sum far below
   the floor. Per-key changes (k = 1) fill the quota in months.
2. **Coalescing cannot move the Snapshot floor.** At about 262,000 inserted
   characters of history a section's Snapshot is past the floor. The plugin
   should report a section's history size (inserted characters, from the
   largest column count) and, past roughly 200,000, suggest starting a new
   section for new material; that is a product decision for the owner
   (pruning is out of the protocol, §16.4; raising the floor is a spec
   change).
3. **Catch-up cost is per unit and grows with the document** in the Rust
   section model (§4); the sdk-ts model should be measured the same way by
   the plugin (LFCP-02-067 item 4). Fewer, larger changes (point 1) cut it
   proportionally.

For sdk-rs (a follow-up next to LFCP-02-109): decide the structural rules
from the nodes and objects the change's operations touch, not from every
node of the document, and give `create_node`'s insertion an index that is
not the whole effective tree; `text_edit`'s stale-base check can compare
the heads of the Text's last change instead of the whole Text. Each turns a
quadratic catch-up or import linear; none changes what is admitted.
