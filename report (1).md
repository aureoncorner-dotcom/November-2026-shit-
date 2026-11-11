**Villain next-sector law: approximate adaptive-acquisition sweep**

Executed 11 November 2026. **PASS across all 13 unchanged benchmark configurations.** The input state tables, evaluation priors, target laws, available measurements, and prices are byte-bound to the preceding exact-recovery benchmark. Only the recovery requirement changes: every declared state must receive a probability-law estimate within worst-case total variation ε.

**The answer depends on both the comparator and the cost objective.** In the primary weighted B=7 case, sequential decisions cease to improve on a label-conditioned batch in worst-case cost at ε = 4095/2^41 ≈ 1.86219×10⁻⁹. Adaptation to the initial label can still improve on a fixed batch. The sequential-versus-fixed worst-cost advantage first vanishes around 1.19209×10⁻⁷, returns around 7.62939×10⁻⁶, and disappears permanently at ε = (2^36−1)/2^47 ≈ 4.88281249993×10⁻⁴. Expected-cost savings against a fixed batch persist until ε = 24577/131072 = 0.18750762939453125.

Use [explore.html](explore.html) to select a configuration, switch the cost objective, and step through exact tolerance intervals. [cost-frontiers.csv](cost-frontiers.csv) gives every cost change; [advantage-intervals.csv](advantage-intervals.csv) lists every interval with strict savings, including returns after a tie. Decimal displays are guides; exact fractions define boundaries.

**The recovery contract is explicit.** The target remains the complete distribution of the next sector after one scheduled elementary x-sector attempt, with equally likely positive and negative orientations. The initial q is already known. The two possible outcomes are q and q xor 1, with toggle probability p(A), where A is the sum of the three reference-loop link currents. The 3×3×3 lattice, M=0, source-free domain, and coupling J=1/(2 log 2) are unchanged:

\[
p(A)=\tfrac12\left[2^{-\max(0,3+2A)}+2^{-\max(0,3-2A)}\right].
\]

For two distributions on these same outcomes,

\[
\operatorname{TV}(\operatorname{Bern}(p),\operatorname{Bern}(\widehat p))=|p-\widehat p|.
\]

The decoder is allowed to return **any valid probability** 0≤p̂≤1, including a value not attained by an input state. For a measurement record R, write p_min and p_max for the smallest and largest compatible toggle probabilities. Its minimax estimate and error are

\[
\widehat p_R=(p_{\min}+p_{\max})/2,\qquad r(R)=(p_{\max}-p_{\min})/2.
\]

The triangle inequality gives the lower bound, and this midpoint attains it within the probability interval. Therefore a record is admissible **if and only if p_max−p_min≤2ε**. Equality is admitted. This special two-outcome setting supplies the center required by the repositories' general recovery-radius discussion. Half-diameter is not universally achievable for arbitrary metric answer spaces or for decoders restricted to an attained target value.

The error bound is uniform over all listed states in every run. Expected cost is minimized under that same uniform constraint; it does not average away errors on rare states. Worst-cost and expected-cost sequential trees are optimized separately. At ε=0, all original optimum costs are reproduced exactly.

**States, costs, and priors were held fixed.** The cycle family has I=aΓx+qyΓy+qzΓz, −B≤a≤B, qx=a mod 2. Put k=|a|, so |A|=3k. There are 4(2B+1) full states, including both signs and all eight initial sectors. The target probabilities simplify to

\[
p_0=1/8,\qquad p_k=1/2+2^{-(4+6k)}\quad(k\ge1).
\]

Queries T_j reveal 1[|A|≥3j]. Uniform scenarios price every threshold at 1. The weighted B=7 scenario prices odd j at 1 and even j at 3. Its direct-read controls additionally offer the exact current on one reference link, which reveals a on this family, at prices 1, 2, 3, 4, or 8. Every invocation pays the declared price.

The local-link family remains the same 64 full current states I=qxΓx+qyΓy+qzΓz+2Σb_i∂P_i, b_i∈{−1,+1}. Each of the three reference x-link currents can be read at price 1. Here A=3qx+2Σb_i; its target need not be determined by signed winding. All local states have equal prior weight. For the ordinary cycle runs k is uniform, qy and qz are fair, and the sign is fair when k>0. The skew run retains its 0.7 / 0.1 / 0.1 / 0.1 conditional prior in each parity class. These are evaluation priors, not equilibrium distributions.

A fixed batch uses one selected query set for every q, but its decoder may use q. A label-conditioned batch selects a set using q alone. A sequential policy may also use previous query identities and answers to choose another query or stop. All are deterministic; queries observe the same unchanged state. The initial-label cost is common and already paid. The declared prices are acquisition-model assumptions, not measured physical times or energy.

**The primary weighted case has seven cost regimes.** Define the following exact boundaries. Here p_k means the probability for magnitude k, not a probability associated with label k.

| Boundary | Exact value | Decimal guide | Probability range merged |
| --- | --- | --- | --- |
| α₁ | 4095/140737488355328 | 2.90967250294e-11 | (p₅−p₇)/2 |
| α₂ | 4095/2199023255552 | 1.86219040188e-9 | (p₄−p₆)/2 |
| α₃ | 16777215/140737488355328 | 1.19209282445e-7 | (p₃−p₇)/2 |
| α₄ | 16777215/2199023255552 | 7.62939407650e-6 | (p₂−p₆)/2 |
| α₅ | 68719476735/140737488355328 | 4.88281249993e-4 | (p₁−p₇)/2 |
| α₆ | 24577/131072 | 0.187507629395 | (p₂−p₀)/2 |

The following are optimal costs. Each row includes its left endpoint and ends just before the next boundary; the last includes ε=1.

| Tolerance interval | Fixed cost | Label worst | Sequential worst | Label expected | Sequential expected |
| --- | --- | --- | --- | --- | --- |
| 0 ≤ ε < α₁ | 4 | 3 | 2 | 3 | 2 |
| α₁ ≤ ε < α₂ | 3 | 3 | 2 | 5/2 | 7/4 |
| α₂ ≤ ε < α₃ | 3 | 2 | 2 | 2 | 3/2 |
| α₃ ≤ ε < α₄ | 2 | 2 | 2 | 3/2 | 5/4 |
| α₄ ≤ ε < α₅ | 2 | 1 | 1 | 1 | 1 |
| α₅ ≤ ε < α₆ | 1 | 1 | 1 | 1/2 | 1/2 |
| α₆ ≤ ε ≤ 1 | 0 | 0 | 0 | 0 | 0 |

Several conclusions are different and should not be collapsed into one “adaptive advantage” number:

- **Sequential versus label-conditioned, worst cost:** strictly better on [0,α₂); permanently equal from α₂ onward.
- **Sequential versus label-conditioned, expected cost:** strictly better on [0,α₄); permanently equal from α₄ onward.
- **Sequential versus fixed, worst cost:** strictly better on [0,α₃) and [α₄,α₅). The first tie is temporary; the permanent disappearance is α₅.
- **Label-conditioned versus fixed, worst cost:** strictly better on [0,α₁), [α₂,α₃), and [α₄,α₅).
- **Either adaptive class versus fixed, expected cost:** strictly better throughout [0,α₆), with permanent disappearance at α₆.

Each optimal cost is nonincreasing with ε. Their differences need not be monotone: different policy classes lose different required distinctions at different boundaries.

There is a concrete explanation for the returned advantage at α₄. Given qx=0, a single cheap T1 separates k=0 from {2,4,6}; given qx=1, a single cheap T3 separates k=1 from {3,5,7}. Each remaining group now fits inside an allowed probability interval. The adaptive worst cost is 1, while a fixed batch needs both cheap queries, costing 2. A shared T2 would cost 3. From α₅ onward the whole odd-parity label needs no queries, while the even label still needs one. Worst costs are then all 1, but expected adaptive cost is 1/2 because each parity has prior mass 1/2. From α₆ onward both labels need no acquisition at all.

**The controls show what persists.** All 13 configurations appear below. “Permanent” means that no strict advantage returns at any larger tolerance. “Never strictly better” describes the entire sweep, not just ε=0.

| Configuration | States | Exact costs: fixed / label / sequential worst | Sequential vs fixed: permanent worst-cost disappearance | Sequential vs label: permanent expected-cost disappearance |
| --- | --- | --- | --- | --- |
| Local links; unit costs | 64 | 3 / 3 / 3 | Never strictly better | ≈ 0.117675781250 |
| B=7; unit thresholds | 60 | 3 / 3 / 2 | ≈ 1.86219040188e-9 | ≈ 7.62939407650e-6 |
| B=7; weighted thresholds | 60 | 4 / 3 / 2 | ≈ 4.88281249993e-4 | ≈ 7.62939407650e-6 |
| B=7; weighted + direct cost 1 | 60 | 1 / 1 / 1 | Never strictly better | Never strictly better |
| B=31; unit thresholds | 252 | 15 / 15 / 4 | ≈ 1.86264514923e-9 | ≈ 7.62939453125e-6 |
| B=7; unit thresholds, skew prior | 60 | 3 / 3 / 2 | ≈ 1.86219040188e-9 | ≈ 7.62939407650e-6 |
| B=7; weighted + direct cost 2 | 60 | 2 / 2 / 2 | ≈ 4.88281249993e-4 | ≈ 7.62939407650e-6 |
| B=7; weighted + direct cost 3 | 60 | 3 / 3 / 2 | ≈ 4.88281249993e-4 | ≈ 7.62939407650e-6 |
| B=7; weighted + direct cost 4 | 60 | 4 / 3 / 2 | ≈ 4.88281249993e-4 | ≈ 7.62939407650e-6 |
| B=7; weighted + direct cost 8 | 60 | 4 / 3 / 2 | ≈ 4.88281249993e-4 | ≈ 7.62939407650e-6 |
| B=3; unit thresholds | 28 | 1 / 1 / 1 | Never strictly better | Never strictly better |
| B=15; unit thresholds | 124 | 7 / 7 / 3 | ≈ 1.86264514923e-9 | ≈ 7.62939453125e-6 |
| B=63; unit thresholds | 508 | 31 / 31 / 5 | ≈ 1.86264514923e-9 | ≈ 7.62939453125e-6 |

For unit-cost B=7 thresholds the worst-cost sequence is (3,3,2) → (3,3,2) → (2,2,2) → (2,2,2) → (1,1,1) → (1,1,1) → (0,0,0) at the same α boundaries. The sequential worst-cost advantage disappears permanently at α₂. Its expected-cost advantage over the label-conditioned batch lasts until α₄. Against the fixed batch, expected savings hold on [0,α₄), disappear on [α₄,α₅), and return on [α₅,α₆). The skew prior changes expected optimum values but leaves these disappearance boundaries and all worst costs unchanged.

For the tested unit-cost B∈{7,15,31,63}, the exact worst-cost disappearance threshold is

\[
\rho_B=\frac{p_4-p_{B-1}}2=2^{-29}-2^{-(6B-1)}.
\]

The exact incremental expected-cost disappearance for sequential versus label-conditioned is

\[
\sigma_B=\frac{p_2-p_{B-1}}2=2^{-17}-2^{-(6B-1)}.
\]

These rational identities match the four computed frontiers. The first approaches 1.86264514923×10⁻⁹ and the second approaches 7.62939453125×10⁻⁶. Decimal precision can make different B values appear equal; their exact fractions remain distinct. Thus the larger exact separation, reaching 31 versus 5 at B=63, does not survive even a 2×10⁻⁹ worst-case TV allowance in these menus. The many distinct positive-magnitude laws accumulate exponentially close to 1/2.

With a direct read priced at 1 there is no worst-cost adaptive advantage anywhere, and no incremental sequential advantage over a label-conditioned batch under either objective. However, label conditioning acquires an expected-cost benefit on [α₅,α₆): it skips the now-unnecessary read on odd parity. With direct cost 2 all three classes tie at exact recovery, but approximation **creates** a worst-cost adaptive advantage on [α₄,α₅), where their costs are 2,1,1. A statement that approximation always weakens or monotonically eliminates every adaptive gap would therefore be false even in this fixed set of controls.

**Local readings have a different pattern.** This family never has a worst-cost separation, at any tolerance. All three worst costs remain 3 until ε=241/2048, then become 0. Expected acquisition still benefits from sequential stopping:

| Starting ε (inclusive) | Fixed / label / sequential worst | Label expected | Sequential expected |
| --- | --- | --- | --- |
| 0 = 0 | 3 / 3 / 3 | 3 | 11/4 |
| 255/8388608 = 3.03983688354e-5 | 3 / 3 / 3 | 3 | 21/8 |
| 255/131072 = 0.00194549560547 | 3 / 3 / 3 | 3/2 | 11/8 |
| 3841/32768 = 0.117218017578 | 3 / 3 / 3 | 3/2 | 7/8 |
| 241/2048 = 0.117675781250 | 0 / 0 / 0 | 0 | 0 |

Each row applies through the next row's starting tolerance, excluding that upper boundary. At ε=255/131072 the entire qx=0 class needs no readings, reducing label expected cost from 3 to 3/2. Sequential expected cost is strictly below label expected cost for every ε<241/2048. Its permanent disappearance is therefore 0.11767578125, the no-acquisition boundary. This differs greatly from the threshold-family incremental sequential boundary near 10⁻⁶.

**The sweep is exhaustive in tolerance, not a sampled grid.** For each configuration I enumerated zero and every distinct |p(x)−p(y)|/2 among states sharing an initial label. These are all possible changes in record feasibility. Between consecutive such boundaries every possible measurement record has unchanged admissibility, so every optimum cost is constant. All arithmetic for feasibility, decoded probabilities, costs, and expected costs uses exact integer fractions. Floating-point values are only display annotations.

Fixed and label-conditioned batches can equivalently be characterized by a separating-set constraint for each same-label pair with |p(x)−p(y)|>2ε. All such pairs must be separated. In the ordered threshold family, a batch partitions k into contiguous intervals; a shared fixed batch checks the within-parity diameter in each interval. A dynamic program considers every last interval and cut price. Label batches use the same recurrence restricted to one parity. A direct read, when available, is a terminal exact alternative.

Sequential optimization uses the original causal cost recurrences with one change: a candidate state set is a zero-cost leaf whenever its probability diameter is at most 2ε. Otherwise it considers every informative threshold partition (or every local reading in the local family). Worst remaining cost uses query price plus the largest child cost; unnormalized expected cost uses query price times the current prior mass plus child totals. Ordered threshold queries preserve intervals, making interval recursion exhaustive. Equivalent cuts retain the cheapest query. Since a direct read already identifies the law exactly, using additional queries after it is dominated. These observations justify the optimization reductions; they are not heuristics or learning from a sample.

All current states and target laws are loaded from the exact benchmark. This run rechecks p from each full current array and uses fresh query answers from those arrays when replaying policies. It also verifies the parity and unused-sector symmetries required for optimization. The previous package contains the physical-validity and independent full-energy calculations for these identical state tables.

The execution receipt records:

- **1,096** full-state target-probability rechecks across seven domain/prior records.
- **1,406** configuration/tolerance boundaries, covering all intervening intervals and every ε∈[0,1].
- **2,316,320** policy/state replays with exact worst-case TV verification.
- **220,084** batch-record diameter checks.
- **65,160** exhaustive batch-mask checks and **12,892** recursively enumerated tree candidates in the small-case cross-checks. Large threshold cases use the exhaustive interval recurrences justified above.
- **1,393** nonzero boundary checks: the witness pair admits a center exactly at half-diameter and admits none immediately below it.
- Exact agreement with all ε=0 costs in the previous 13 configurations and monotonicity of each optimized cost with increasing tolerance.

An additional checker imports **no optimizer code**. It reads the serialized batches, probability decoders, trees, full state arrays, and unchanged priors from disk and independently replays all 676 saved policies, comprising 180,800 state evaluations. It verifies recovered errors and costs, checks input hashes and prices, rejects a deliberately corrupted decoder, and rejects an approximate policy evaluated below its attained error. These are finite verification-work counts, not independent statistical samples.

**What this establishes and what remains to test.** This is an exact finite optimization result for the already-declared states and acquisition interfaces. It establishes a mathematical connection between the Villain sufficient witness and the v2.6 recovery-radius/acquisition framework. It also shows that exact distinctions in exponentially small probability tails can drive large acquisition gaps that disappear under a very small prediction tolerance.

The next applied tests should replace assumed query prices with measured implementation costs, introduce a stated noisy-measurement model, or broaden the source-state family while holding the target and error guarantee explicit. This experiment leaves those assumptions unchanged as requested. It provides a one-attempt probability-law guarantee, with no claim that the finite family is invariant under dynamics or that a compressed state evolves autonomously. The repositories' multi-step path bound requires a uniform premise for every reachable full state under the relevant kernel; these finite one-step checks do not supply that premise for the unbounded physical model. Allowing randomized policies with expected-error guarantees, or restricting decoders to attained target laws, would also define different optimization problems.

**Exact sources and provenance.** The mathematical inputs were read from the two confirmed repositories:

- `Toroidal_scrotal_posturing-main/geomas_2.9.md`, lines 518–529: the orientation-averaged Villain toggle law and sufficient refinement (q,|A|). Exact copy: [source/geomas_2.9.md](source/geomas_2.9.md).
- The same file, lines 187–201: recovery radius, the required answer-space/center qualification, and the separate uniform path guarantee; lines 747–795: declared acquisition assumptions, batch classes, sequential recurrences, and tool-scope limits.
- `Math_n_shiz-main/GEOMETRY_Working_Master_v2.6.md`, lines 101–145: policy classes and acquisition formulations; lines 159–171: recovery radius, attainable midpoint for real witnesses, and uniform TV premise. Exact copy: [source/GEOMETRY_Working_Master_v2.6.md](source/GEOMETRY_Working_Master_v2.6.md).

The preserved extraction root is `C:/Users/Andrew/Documents/Codex/2026-11-03/files-mentioned-by-the-user-faaakyou/work/archives/`. The previous state tables and query-price receipt are copied byte-for-byte under [input/](input/), from `C:/Users/Andrew/Documents/Codex/2026-11-11/referenced-chatgpt-conversation-this-is-an-3/outputs/villain-acquisition-test/`. Their SHA-256 values appear in [results.json](results.json). The approximate sweep, policies, disappearance intervals, and executable checks are new results from this follow-up, not pre-existing repository experiments.

See [README.md](README.md) for local reproduction with Node.js. The package includes all required inputs; it needs no downloads or third-party libraries. [policies.json](policies.json) contains a valid optimum policy at the beginning of each cost regime; it remains valid throughout that regime. [sweep-events.csv](sweep-events.csv) includes every critical tolerance, including boundaries that do not change an optimum cost. The selected expected-optimal tree's worst cost is recorded separately; it is not substituted for the independently optimized worst-case objective.
