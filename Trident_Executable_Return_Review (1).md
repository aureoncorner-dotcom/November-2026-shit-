# Executable return found: Corner Relay α

Review of the three ZIPs supplied in the 11 November 2026 conversation. Originals were not modified. This report distinguishes supplied code, fresh executions, and a new review harness.

## Finding

The Toroidal repository already contains a working deterministic **O / Λ / S send-and-acknowledgment round trip** with separate endpoint identities, retained state, and append-only histories. The earlier blanket description that an executable return was still missing was too broad. This component supplies executable return and state carry-forward; it is not merely a visualization.

The exact source location is:

```text
Toroidal_scrotal_posturing-main(6).zip
└── Toroidal_scrotal_posturing-main/
    └── Corner_Relay_Alpha_C6_Reference_v0.1.zip
        └── Corner_Relay_Alpha_C6_Reference_v0.1/
            ├── corner_relay.py
            ├── test_corner_relay.py
            ├── reference_trace.py
            ├── run_with_provenance.py
            ├── FROZEN_PACKET.txt
            └── source_binding.json
```

The outer repository also contains copies of the core relay files. The internally coherent nested package, rather than the mixed repository-root README, was used for execution.

## Fresh verification

| Check performed in this review | Result |
|---|---|
| Supplied `run_with_provenance.py` | Exit 0; all **20 supplied tests pass** |
| Supplied deterministic `reference_trace.json` | Reproduced **byte-for-byte** |
| New `check_two_returns.py`, using unchanged relay code | **22 checks pass** |
| Two fresh executions of the new trace | Identical deterministic content |
| Original relay source, tests, documentation and binding files | Unchanged in the run copy |
| Prime audit `python run_all.py` | All three workers complete successfully |

Runtime: Python **3.13.5**. Exact commands, runtime metadata, stdout/stderr and hashes are preserved in `review_receipt.json` and the runnable evidence bundle. The fresh outputs are not substituted for historical receipts.

The supplied 20 tests cover sends, acknowledgments, idempotent retries, duplicate delivery, reordering, partitions, exit, endpoint/key-label separation, opaque payload routing, witness fields and tamper detection. Passing these finite tests does not constitute a general proof of every possible implementation behavior.

## Two successive returns, without reset

The new harness creates `Endpoint(Actor.O)`, `Endpoint(Actor.S)` and `LambdaTransport` once. It schedules two SEND/ACK exchanges on those same instances. It does not replace endpoint states, modify the engine, or compute a substitute return by hand.

| Checkpoint | Harness action index | O RAW records | S RAW records | O sends | O acknowledgments received |
|---|---:|---:|---:|---:|---:|
| Initial state | 0 | 0 | 0 | 0 | 0 |
| First completed return | 4 | 2 | 2 | 1 | 1 |
| Second completed return | 8 | 4 | 4 | 2 | 2 |
| Retry and duplicate delivery | 10 | 5 | 5 | 2 | 2 |

The harness explicitly checks that the pre-state of the second SEND equals the first returned O VIEW, and that both first-cycle RAW histories remain exact prefixes of the second-cycle histories. Both returned O VIEWs differ from their predecessors. Both endpoint hash chains verify.

After the second return, an idempotent retry adds one RAW record to O and one to S, while **both operational VIEWs remain unchanged**. This is a concrete distinction between replaying an effect and recording that another invocation occurred. It does not imply that every unchanged VIEW requires a different future law.

The second round is **externally scheduled** by the new harness. The supplied engine carries state and enforces transition preconditions; it does not independently decide when to initiate another round or choose its payload. The harness is new review code, not a rediscovered historical DECURSE runner.

## Connection to the current DECURSE notation

The following is an interpretation for integration, not an alteration of the source specification:

| Current architectural role | Concrete supplied mechanism | Qualification |
|---|---|---|
| O and S remain distinct | Separate `Endpoint` instances, actor tags, key labels and RAW ledgers | Structural identity model, not production cryptographic authentication |
| λ contact | `LambdaTransport.route` and `deliver` | Routes the declared event; opaque payload |
| S changes | `receive` appends an accepted event; `acknowledge` creates a separate ACK | The modeled change is event/state bookkeeping, not arbitrary payload semantics |
| Return toward O | ACK is routed back and received by O | Same transport instance, reverse message direction; no separate evolving λ′ state |
| O₂ | O's changed retained state following the ACK | Not a newly created endpoint and not a fusion with S |
| Another passage | Same O/S instances accept a second declared exchange | Demonstrated state carry-forward under an external schedule |

**Time notation must remain explicit.** The archived `FROZEN_PACKET.txt` calls **T the transition relation**. The user's current DECURSE notation calls **T the time axis**. These are not silently identified. In an adapter, the relay transition could be denoted U, while its actual native temporal evidence consists of local `record_no` order and previous-witness links. The harness additionally records a global logical `t_index` for its prescribed schedule. Neither source nor harness supplies a physical sampling interval.

This component does not integrate the 367° phase code, all 13 chamber operations, a changed λ′ relation, or a recursive-versus-progressive outcome classifier. The stateful-return requirement is supplied; those wider identifications still need an explicit interface/mapping. They are not prerequisites for recognizing the demonstrated relay behavior.

## Prime/phase/witness audit rerun

The separate prime audit was copied into a run directory and executed without changing its inputs.

- Workbook: 2,701 checked cells, zero discrepancies; central value 11,159.
- Double-key counts over 529 / 913 / 14,351 positions: **43 / 74 / 732**.
- Coordinate CSV: 732 rows and 5,124 checked fields, zero discrepancies.
- Repeat CSV: 14,351 rows and 172,212 checked fields, zero discrepancies.
- 367° exact periods: relative phase **30,240** integer steps; both absolute orientations **332,640** steps.
- 0–924 intersection histograms: 360° gives {2: 408, 4: 517}; 367° gives {0: 4, 2: 435, 4: 479, 6: 7}.
- Finite witness worker: **11 checks pass**.

These are reruns of the supplied audit implementations, not new independent implementations of all their checks. The archived image/source mismatch and wording issue remain in that audit's scope; successful execution does not erase them. This run did not modify a website or establish that the relay imports the phase audit.

## Input identity and inspection coverage

The three latest archives are byte-identical to earlier mounted uploads:

| Latest ZIP | Earlier identical ZIP | Outer file count |
|---|---|---:|
| `prime_lattice_independent_python_audit (1)(5).zip` | `prime_lattice_independent_python_audit (1)(2).zip` | 22 |
| `Toroidal_scrotal_posturing-main(6).zip` | `Toroidal_scrotal_posturing-main(5).zip` | 310 |
| `Math_n_shiz-main (1)(4).zip` | `Math_n_shiz-main (1)(3).zip` | 216 |

Consequently this is a **new focused execution/review of existing material**, not a new source release or independent historical corroboration. Archive members were read with ZIP integrity checking; paths were checked before extraction. Inspection inventoried 548 outer files and 1,748 member occurrences including nested duplicates, through depth 4. Text/code search and targeted close reading were used; this is not a claim to have closely reviewed every binary/document or all deeper nested content.

## Source locations and fingerprints

`corner_relay.py`:

- Lines 217–277: independent endpoint initialization and deterministic VIEW construction.
- Lines 283–335: append-only before/after witness record.
- Lines 400–472: SEND and exact-retry behavior.
- Lines 508–582: ACK created from an already received SEND.
- Lines 638–698: event receipt and state effect.
- Lines 710–772: keyless route-only transport.

`test_corner_relay.py` lines 103–111 already contain a one-round-trip test. Lines 68–83 check equal final VIEWs with six retained delivery orders. The new two-return harness extends the exercised schedule without changing these originals.

- Unchanged `corner_relay.py` SHA-256: `28ccc31b4304222d5d2429c6054a64ca366316167e8162aeb63d91bba24a4a97`
- Reproduced reference trace file SHA-256: `17d4c355bc81c422ec7121cba0a411e37aec42cff96da87949ef9d83f72f64b1`
- New two-return trace file SHA-256: `83559f23f1f2c74d6ae52be7db1f042ffa67ce0afbd36b5a56d2e26eac792e16`

Full input/source/checker hashes and execution records are in `review_receipt.json` and `SHA256SUMS.json`.

## Reproduce the focused return check

The evidence ZIP includes unchanged relay source files and a separately identified new harness. From its `corner_relay/` directory:

```bash
python run_with_provenance.py
python check_two_returns.py
```

The first command reruns the supplied 20 tests and regenerates its reference trace and execution receipt. The second command reruns the new 22-check review and writes `two_return_results/two_return_trace.json` plus its receipt. Python's standard library is sufficient. Rerunning deliberately replaces generated files in the unpacked evidence copy; original uploaded archives remain untouched.

## Updated status

**Executable O/S return and state carry-forward: demonstrated for the supplied Corner Relay model.**

**Full DECURSE/Trident naming and cross-component integration: not established by this relay test alone.**

The next integration target is specific: the interface between this existing relay/state history and the phase/witness modules. Finding any working return from scratch is no longer the task.
