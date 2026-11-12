Audit of the witness verification scripts
Reviewed November 11, 2026. This is an addendum to the earlier source review. It does not replace or edit the original files or the earlier handoff.
Decision
The expanded witness engine is sufficiently supported for a website demonstration of the declared finite, ideal-probability model. The original two checking scripts are not sufficient as the website's sole acceptance tests.

The unchanged engine passed new checks of complete returned records, independent hand-calculated examples, all 448 combinations of retained-axis set / nonempty target-axis set / offered-axis set, targeted boundary cases, input errors, and JSON command-line behavior. No incorrect result was found in the unchanged expanded engine in these tests. The results remain finite mathematical examples; they do not validate hardware, noisy measurements, a deployed web service, or the wider prime-lattice theory.

The original verifier missed eight deliberately introduced defects. The comparison script returned success even when its own report showed different results. These are demonstrated weaknesses of the verification evidence, not eight defects found in the current engine.

Recommended source: the unchanged 18,458-byte geometry_quantum_witness.py, SHA-256 57cab884c7ddb457b96f6b86dba469fe5168d0dcb708e18e347d53e6bfc90d5b. Keep the 10,637-byte predecessor as history. This audit addresses the supplied files by hash and adds no new evidence about the previously unavailable (10) attachment name.
Scope and preservation
The two primary targets were:
File	SHA-256
verify_witness.py	3063c5d22ffaafa2f9877763d6e90192cd13273ae498f0dc4150de5e4ab45dc9
compare_revisions.py	ae04bf0f9e1e1b045cb1b8870a9575811c5c80c544bad4bd1a2bd0520f525c34


Both witness source versions, both saved JSON receipts, and the four supplied text outputs were also inspected. All ten originals were copied to a separate audit workspace before execution. Their contents and modification times were checked against an initial manifest afterward. Faults were inserted only into separately labeled test specimens. The report, companion checkers, and evidence archive are new deliverables; neither original checking script was patched.

The original verifier was rerun from copies under normal and optimized Python 3.12.14. Both reproduced its 500-case / 974-returned-option pass. That establishes reproducibility of what the script actually checks, not completeness of its checks.

Line references below refer to the original files, not the new companion checkers.
Findings
1. Returned measurement options are not checked for completeness or correct metadata
Location: verify_witness.py, lines 51–60, especially 54–56.

The independent routine calculates an expected options list, but the caller never compares it with the returned list. Instead, it iterates over whatever the engine returns and checks only each returned loss. It does not require every allowed subset, prohibit duplicates, or independently check each option's cost and repairs_witness flag. For a full-repair recommendation it checks axes and cost, but the random-case checks omit the reported post-repair loss; the engine's own self-tests cover that field only in a few fixed examples.

Demonstrated: returning no measurement options still reports pass: true, with zero option checks. Duplicating the entire list also passes and raises the reported count to 1,948. Changing all displayed option costs to 999 and reversing all their repair flags also passes.

Consequence: a website could display an empty, duplicated, or incorrectly priced comparison table while this verifier passes. The earlier description “974 measurement-option checks” should be read as 974 loss comparisons on returned objects, not full verification of the option table.

Required acceptance check: build the complete expected set of 2^k batches, where k is the number of offered axes not already retained; compare unique subsets, exact costs, losses, flags, and the declared deterministic ordering.
2. Loss agreement does not verify the probability values or explanatory records
Location: verify_witness.py, lines 18–28 and 51–63.

The loss oracle is useful and mathematically valid. It does not call the engine's loss, grouping, or probability functions. However, the random-case checks do not compare the returned probability signatures, fibers, conflict descriptions, or unrepairable-pair explanations. Squared differences are invariant under a common probability offset, and equality-based groups are unchanged by that offset.

Demonstrated: replacing the engine's probability formula (1+r)/2 with (2+r)/2 still passes the whole original verifier, including its self-test invocations. The altered source can report a probability of 3/2, yet its losses and repair choices remain unchanged. Separately, deleting every fiber, conflict, and unrepairable-pair explanation also passes.

Consequence: correct loss numbers do not certify the values or explanations shown to a visitor. The mutation is not present in the actual source; it exposes a class of errors the test cannot see.

Required acceptance check: compare retained and target probabilities against independent expected values and verify the complete grouped-state, conflict, and unresolved-pair records. Hand-derived probability anchors are needed in addition to variance checks.
3. Frontier comparison discards the recommended actions
Location: verify_witness.py, line 63.

Both sides are converted to sets of (cost, loss) pairs. This discards axes, repair flags, duplicate entries, order, and the chosen representative when several batches have equal cost and loss. The original frontier oracle also uses essentially the same dominance predicate as the engine, giving less protection against a shared mistake in that predicate than a different construction would.

Demonstrated: replacing every frontier entry's axes with ['INVALID'] and reversing its repair flag still passes, provided the cost/loss coordinates are unchanged. Returning a false budget value also passes the original random-case checks.

Required acceptance check: compare complete frontier records and budget records, including legal axes, costs, losses, flags, and the documented cost/axis-count/alphabetical tie rules. The new checker constructs the frontier differently: at each cost it selects the minimum loss, then retains strict record-low losses as cost increases.
4. Command-line success does not establish a usable response
Location: verify_witness.py, lines 65–74.

The script checks only the child process's return code. It stores stdout without parsing JSON or comparing its contents with independent expectations. It does not exercise the custom --input path or its structured error behavior. The optimized child invocation checks the engine's own self-test, not all possible optimized-runtime behavior.

Demonstrated: making the --json success branch print THIS IS NOT JSON still produces an overall pass.

Required acceptance check: parse success output, compare its full data contract, test custom input files and command-line budget overrides, and check exit status, stdout, and structured error output for malformed inputs.
5. Revision comparison is informative, but is not an independent correctness gate
Location: compare_revisions.py, lines 13–27.

The AST comparison accurately reports identical function definitions in these files. It examines only top-level functions; it does not report module-level assignments, classes, imports, or removed functions. Identical function syntax does not guarantee identical behavior when a referenced global changes.

For execution it calls each revision's own example() function. The inputs are not frozen externally, and the mathematical core is identical between these revisions. Agreement is evidence of compatibility for those fixtures, not independent evidence of correctness. The decimal test records two values but does not assert the expected values.

Demonstrated:
- Changing the newer engine's reported loss to 999 makes the report's equality flags false, but the script still exits 0.
- Putting the same invalid probability offset into both engines retains matching core-function ASTs and matching common outputs. The comparison reports agreement despite the shared error.
- Changing only the newer module's AXES assignment leaves its function-AST equality list unchanged, even though its behavior changes.
This is appropriate for an informational comparison report if its findings are read. It must not be interpreted as a passing regression test merely because the process succeeded.

Required acceptance check: feed the same external fixtures to both revisions; assert independent expected values; check the common output schema; report relevant global/class/import changes; make unexpected differences fail an acceptance run. Intentional parser differences must have explicit expectations rather than blanket equality requirements.
6. A failed run can leave a stale successful receipt
Location: verify_witness.py, lines 76–78.

The script writes its JSON receipt only after success. If it is rerun in a directory containing a previous success and then fails, the old file remains.

Demonstrated: a good run was followed by a deliberately broken loss implementation in a separate copy. The second process exited 1, but fresh_verification.json remained byte-identical and still said pass: true. Its source hash no longer matched the failing source, so a consumer checking both exit status and current source hash would catch the mismatch.

Required acceptance check: tie a receipt to the current source and checker hashes and an identifiable run, replace a prior success with a running/failure state, and only publish a success after the entire run completes. The new companion checker does this, and a source-mismatch test confirmed that it replaces a historical success with an explicit failure.
7. The generated input domain is narrower than “500 cases” suggests
Location: verify_witness.py, lines 41–50.

The original generator uses coordinates with reduced denominators 1, 2, or 4; half-integer costs from 0 to 3; budgets from 0 to 4; and retained axes always in canonical XYZ order. Every random input is valid and every random call supplies an explicit budget. Its 500 cases do include useful edge coverage: 38 singleton populations, 80 populations containing repeated vectors, 56 cases with a free offered measurement, and 50 zero budgets. In 210 cases there are no unretained offered axes.

Missing from that random loop are non-dyadic fractions, high-precision decimal input, unsorted retained axes, an absent budget, input-budget versus argument precedence, malformed state records and schemas, and the actual custom-input command-line path. Some invalid-budget/decimal behavior is covered by the engine's own fixed self-tests, but that is narrower than an independent input-validation audit.

The original expected output is also calculated after engine.run(data, budget) on the same input object. The current engine does not mutate its input, but the verifier does not protect against a future implementation modifying the expected test data in place. The new checks freeze independent expectations before calling the engine and test that caller input remains unchanged.
What is independent, and what is circular?
The original loss check is not circular in the ordinary sense of using the engine's answer as its expected answer. For a group of m vectors,

sum over i<j of ||y_i-y_j||² = m × sum over i of ||y_i-mean(y)||².

The engine uses squared deviations from group means; the original verifier uses the left-hand pairwise identity and divides by m and then the total population. Both are exact rational calculations, and grouping raw retained Bloch coordinates is equivalent to grouping (1+r)/2, because that affine map is injective. Those parts of the original audit provide real evidence.

The limits are shared model assumptions, a closely shared frontier predicate, incomplete output checks, and the old/new comparison of largely identical code. The existence of two revisions, two passing self-tests, or matching functions does not make them independent correctness implementations.

The new loss oracle uses a third form, on raw coordinates: one quarter of sum(r²) − sum(r)²/m per target axis and group, divided by the total population. It builds batches with bit masks and the frontier with cost-group record lows. It never calls the engine to produce expected values or fixtures. This improves computational confidence; it still tests the declared model, not the empirical truth of a physical interpretation.
Fresh stronger checks
New companion programs are included in the evidence package. They are separate files, not edits to either supplied verifier.
Check	Fresh outcome
Unmodified original verifier	Normal and optimized runs reproduce 500 cases / 974 returned-option loss checks.
Deliberate faults against original verifier	Eight defects escape; a ninth positive control, incorrect loss normalization, is detected. This is a targeted diagnostic set, not a statistical mutation score.
Full-output valid cases	474 cases, including all 448 axis-set combinations, pass; 974 option records checked completely. The repeated number 974 is coincidental; these are different cases from the original random run.
Hand-derived checks	Four anchor checks pass, including two-state 1/16, seven-state 1/7, budget-one 1/14, and repeated-record weighting giving 1/18.
Invalid API inputs	53 cases reject with the expected controlled error type.
Transformation checks	9 cases cover axis relabeling, reversing record order, and replicating the complete population.
CLI input/output contract	18 cases pass: 8 valid cases and 10 controlled-error cases, including exact JSON decimals, exponent notation, fractions, UTF-8 BOM, duplicate keys, invalid states, missing files, and overrides.
New checks on fault specimens	All nine original-verifier fault specimens are detected.
Old/new common behavior	474 identical external-input cases, checking 11 shared fields against independent expectations, pass. All three comparison fault specimens are detected.
Optimized execution	The new full checker passes under -O; its required checks use explicit exceptions, not removable assertions.


The final package includes normal and optimized receipts for the companion full checker. The tests are not a complete proof over arbitrarily large rational inputs. The targeted mutation set was chosen after reading the original code; it is a way to demonstrate specific coverage gaps, not an unbiased estimate of all possible defects.
Numerical confidence for the website
For the two-state example, retained Z probabilities are both 1/2, while target X probabilities are 1 and 1/2. The best common prediction is 3/4. Both squared errors are 1/16, so their average is 1/16.

In the seven-state fixture, the two Z poles are individually identified. The five states in the remaining Z group contribute total squared probability error 1 across X and Y, yielding 1/7 over seven records. Adding Y leaves total squared error 1/2, yielding 1/14. Adding both X and Y makes the target exactly recoverable. With the stated costs, Y costs 1, X costs 2, and the full batch costs 3. These numbers are not inferred solely from old/new agreement.

The objective is uniform over supplied records, not unique physical states. Duplicating only the mixed-state record changes the two-state population into three records and the loss to 1/18. Duplicating the entire population leaves the loss unchanged. Both behaviors were checked and are consistent with the documented objective.
Developer acceptance boundary
Approve the pinned expanded engine and these fixtures for an educational/model demonstration. Preserve the exact source hash and use the new full-contract checks, alongside the compatibility checks, when porting or changing it. The old scripts remain useful historical evidence and an informational revision report; they should not be the only release checks.

The website must preserve:
- Exact fractions and decimal input semantics, the three offered axes X/Y/Z, the target-axis order, declared measurement costs, and all budget/tie rules.
- Uniform weighting over supplied records and exact equality of ideal probabilities. Tiny exact differences can separate records in this model; this says nothing about distinguishability with noisy or finite-shot measurements.
- The distinction between a full-repair recommendation and a best affordable partial repair.
- Complete and correctly labeled probability, conflict, option, and frontier data.
- Successful parsing and validation of actual frontend/backend input and output. The website itself and any JavaScript port were not supplied or tested here.
For unrestricted visitor input, establish input-size limits and resource budgets before deployment. The current engine constructs pair lists, which can grow quadratically with the number of records, and accepts exact rational numbers without a small fixed size cap. This audit did not benchmark large-input performance. A bounded fixture demonstration does not depend on that untested capacity.

This audit supports the numerical demonstration. It does not support claims of one-shot tomography, quantum advantage, a physical detector result, prime-driven geometry, or an operational autonomous engine.
Evidence map
- original_manifest.json and originals/: preserved copies and identities of the ten supplied files.
- existing_verifier_audit.json: original reruns, actual generator coverage, and deliberately altered-code results.
- receipt_lifecycle_results.json: stale-success demonstration and the companion checker's explicit failure receipt.
- contract_results_final/results.json and contract_results_optimized/results.json: complete-output validation receipts.
- revision_contract_results.json: same-input compatibility and independent common-field checks.
- audit_existing_verifiers.py, audit_receipt_lifecycle.py: the review experiments.
- check_witness_contract.py, check_revision_contract.py: the new reusable companion checks.
- specimens/: deliberately altered test copies. Do not use these as application code.
All judgments are about the exact supplied bytes and the stated finite model. Passing more tests narrows uncertainty; it does not turn a finite audit into proof of every future implementation or physical claim.
