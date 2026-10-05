# OpenLFCP compatibility matrix

Generated 2026-10-05T21:11:02.413Z by examples/conformance (LFCP-070).

- Spec baseline: mvp-0.1-baseline.5 (spec dfd5db24c8cade7397737145a062c1ba5bc8a354).
- sdk-rs: 170629577f21a6c7cc074c26e7271abcbe539962.
- sdk-ts: eb3581782a99f4da81c7bf6ec058619a98bda252.
- pins.json: sdk-rs 1706295, sdk-ts eb35817, spec dfd5db2 (strict run: the SDKs are these commits).

## A. Official vectors (byte-exact where the vectors fix every input)

| SDK | Suites | Result | Source |
| --- | --- | --- | --- |
| ts | LFCP-TEST-VECTORS-01/01 | PASS 116/116 | sdk-ts conformance runner at mvp-0.1-baseline.5 (584/584 checks) |
| ts | SHARED-OBJECTS-TEST-VECTORS-01/01 | PASS 29/29 | sdk-ts conformance runner at mvp-0.1-baseline.5 (80/80 checks) |
| rust | LFCP-TEST-VECTORS-01, SHARED-OBJECTS-TEST-VECTORS-01, corpus, schema fixtures | PASS 215/215 | sdk-rs cargo test --all-features (every test; vectors read at spec.lock) |

## B and C. Cross-consumption, negatives and Shared Objects

Fresh objects with production randomness, exchanged as protocol bytes. Exact bytes are
required only for message re-encoding (deterministic codec); Automerge changes are compared
by logical state and conflict sets, never by bytes.

| Check | Category | Rust → TS | TS → Rust | Rust → Rust | TS → TS |
| --- | --- | --- | --- | --- | --- |
| principal.bob | principal | PASS | PASS | PASS | PASS |
| principal.carol | principal | PASS | PASS | PASS | PASS |
| principal.dave | principal | PASS | PASS | PASS | PASS |
| principal.invite | principal | PASS | PASS | PASS | PASS |
| principal.owner | principal | PASS | PASS | PASS | PASS |
| control.chain | control | PASS | PASS | PASS | PASS |
| control.head | control | PASS | PASS | PASS | PASS |
| control.owner | control | PASS | PASS | PASS | PASS |
| control.abilities.bob | control | PASS | PASS | PASS | PASS |
| control.abilities.carol | control | PASS | PASS | PASS | PASS |
| control.abilities.dave | control | PASS | PASS | PASS | PASS |
| control.abilities.invite | control | PASS | PASS | PASS | PASS |
| control.abilities.owner | control | PASS | PASS | PASS | PASS |
| control.epoch | control | PASS | PASS | PASS | PASS |
| control.dek_commitments | control | PASS | PASS | PASS | PASS |
| control.cutoff | control | PASS | PASS | PASS | PASS |
| key_package.kp_bob_e0 | hpke | PASS | PASS | PASS | PASS |
| key_package.kp_invite_e0 | hpke | PASS | PASS | PASS | PASS |
| key_package.kp_bob_e1 | hpke | PASS | PASS | PASS | PASS |
| key_package.kp_carol_e1 | hpke | PASS | PASS | PASS | PASS |
| data_unit.u1 | data | PASS | PASS | PASS | PASS |
| data_unit.u2 | data | PASS | PASS | PASS | PASS |
| data_unit.u3 | data | PASS | PASS | PASS | PASS |
| data_unit.u4 | data | PASS | PASS | PASS | PASS |
| snapshot.s1 | snapshot | PASS | PASS | PASS | PASS |
| message.HELLO | message | PASS | PASS | PASS | PASS |
| message.CHALLENGE | message | PASS | PASS | PASS | PASS |
| message.AUTH | message | PASS | PASS | PASS | PASS |
| message.READY | message | PASS | PASS | PASS | PASS |
| message.RESOURCE_OPEN | message | PASS | PASS | PASS | PASS |
| message.CONTROL_BATCH | message | PASS | PASS | PASS | PASS |
| message.DATA_BATCH | message | PASS | PASS | PASS | PASS |
| message.KEY_PACKAGE_BATCH | message | PASS | PASS | PASS | PASS |
| message.SNAPSHOT | message | PASS | PASS | PASS | PASS |
| message.ACK | message | PASS | PASS | PASS | PASS |
| message.NACK | message | PASS | PASS | PASS | PASS |
| message.ERROR | message | PASS | PASS | PASS | PASS |
| message.AUTH.verify | message | PASS | PASS | PASS | PASS |
| negative.unit_tampered | negative | PASS | PASS | PASS | PASS |
| negative.unit_unauthorized | negative | PASS | PASS | PASS | PASS |
| negative.unit_stale | negative | PASS | PASS | PASS | PASS |
| negative.unit_unknown_epoch | negative | PASS | PASS | PASS | PASS |
| negative.unit_aead | negative | PASS | PASS | PASS | PASS |
| negative.unit_equivocation | negative | PASS | PASS | PASS | PASS |
| negative.record_unauthorized | negative | PASS | PASS | PASS | PASS |
| negative.record_claim_used | negative | PASS | PASS | PASS | PASS |
| negative.record_fork | negative | PASS | PASS | PASS | PASS |
| negative.kp_unauthorized | negative | PASS | PASS | PASS | PASS |
| negative.snapshot_unauthorized | negative | PASS | PASS | PASS | PASS |
| negative.snapshot_beyond_cutoff | negative | PASS | PASS | PASS | PASS |
| shared_objects.changes | shared_objects | PASS | PASS | PASS | PASS |
| shared_objects.validate | shared_objects | PASS | PASS | PASS | PASS |
| shared_objects.snapshot | shared_objects | PASS | PASS | PASS | PASS |
| shared_objects.negative.change_signer | shared_objects | PASS | PASS | PASS | PASS |
| shared_objects.negative.change_checksum | shared_objects | PASS | PASS | PASS | PASS |
| shared_objects.negative.snapshot_change_chunk | shared_objects | PASS | PASS | PASS | PASS |
| shared_objects.negative.state_problems | shared_objects | PASS | N/A | PASS | N/A |

## Known gaps

- `shared_objects.negative.state_problems` (N/A in some directions): Only the Rust adapter produces this negative: it writes profile-invalid changes with raw Automerge, while the TypeScript adapter writes through the profile API, which refuses them. Both consumers check the Rust-produced case.
- Mode A counts per suite come from sdk-ts only. sdk-rs reports one count over its whole `cargo test --all-features` run, which includes both vector suites, the Automerge corpus and the schema fixtures.
- The G-EP7 cross-check (rebuilding the state without a unit that a later Key Epoch Record places beyond its cutoff) is deferred: the run does not compare the two SDKs on it.

No blocking problems.
