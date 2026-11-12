# Corner Relay α C6 → Civilization / Abundance v7.1b
## Independent integration and limitation note (19 October 2026)

**Decision: integrate as a reproduced finite *construction* and a witnessed information-loss example. Do not promote to production decentralization, authenticated authorization, or general governance validation.**

### 1. Artifact identity and original construction boundary

`Corner_Relay_Alpha_C6_Reference_v0.1.zip` implements a deterministic Python 3 protocol for two endpoints O and S, exactly two *symbolic* key slots, and Λ as a route-only transport object. It implements SEND, RECEIVE, ACK, RETRY, EXIT, rejection records, duplicate delivery, reordering, and a queue-retaining modeled partition. RAW events preserve attempts, identities, preconditions, before/after state hashes, and witness links. VIEW is a deterministic, sorted summary of accepted local effects.

The frozen source explicitly says that O/S independence, exit and retry must be enforced and that Λ may not become an authority. The README states that this code is a reference model, not a cryptographic authentication scheme. Its C6_RESULT self-rates CF, SC, WF and FV all 3; those rubric values are author-assigned evidence descriptions, not a separately validated scoring scale.

### 2. Independent verification performed now

| Check | Fresh result | Meaning |
|---|---:|---|
| SHA-256 expected hashes for packaged source/documentation | 9 of 9 | Exact artifact provenance consistency |
| Unit-test suite | 20 of 20 PASS | Reproduced implemented acceptance tests |
| Reference trace | Identical bytes | Regenerated deterministic trace |
| All six permutations of three independent deliveries | 6 RAW orderings / 1 VIEW | Constructive non-descent witness |
| Unsigned, self-consistent S-labelled ACK without any S RAW | Accepted at O | Sender-origin authentication is absent |

The two Drive source records named in the supplied `source_binding.json` were also read through the connected Drive source. The source document contains the frozen architecture clauses, and the independent call-question document contains the exact C6 challenge. This provides textual source agreement at their recorded 2026-08-31 versions, not a cryptographic attribution of the document's author.

### 3. The mathematical seam

Set the six histories H to be the six possible delivery orders of three *distinct independent* SENDs. Let `π_VIEW: H → Q` return S's derived VIEW, and `W_order: H → Y` return the ordered RAW delivery-event sequence. Code enumerates `|π_VIEW(H)|=1` and `|W_order(H)|=6`. Thus at least one pair of histories has identical VIEW but different ordered RAW; in the v7.1 geometry's notation, `N_{W_order}(π_VIEW) ≠ ∅` on this stated finite domain.

This proves precisely one thing: the tested VIEW projection loses the ordering witness. It does *not* prove that the VIEW fails to preserve the declared deduplicated operational state. Indeed the entire point of its sorting and idempotence is to preserve that reduced result under reordering. This is a claim-relative, rather than blanket, failure.

### 4. Source authenticity is a separate witness

The Python `Event.build` constructor computes the event ID and payload hash using public fields and a fixed label such as `corner-relay:key:S`. An adversarial caller can construct an ACK with a self-consistent S label referring to O's real local SEND. O's `receive` accepts that ACK even though S has not locally received the SEND or produced an ACK. The accepted event can pass `verify_raw_ledger`, because that checks log consistency, not authenticated origin.

The existing test for a mismatched actor/key **does** reject a label mismatch. That is valuable input validation but is different from unforgeable source authentication. This additional probe is not a surprise production-security failure because the README explicitly excludes cryptographic keys; it is a hard barrier to treating the reference model as an enforcing federation protocol in an adversarial environment.

### 5. Architectural translation without category collapse

**Corner vocabulary:** O and S are endpoint names in C6, not automatically personhood categories. The older Corner/CTA Triad uses a relational R for which mediator replaceability is load-bearing. C6 Λ is a concrete transport queue, not a proof that the earlier R is replaceable. No test removes Λ and reconstructs its outstanding queues. Its partition toggles influence availability even though its methods never choose the meaning of a message.

**Geometry vocabulary:** A derived endpoint state, a received event's authenticated origin, a history of attempted transitions, an endpoint's exit status, and a reliable delivery path are different witnesses. The existence of one VIEW does not imply they can all descend through it.

**Civilization vocabulary:** The Abundance Engine should separately score served material outputs, local decision rights, verified identity/authorization, audit recovery, route replaceability, and exit. The C6 test cases can become a small synthetic protocol oracle for governance prototypes. They are not a new cohort of the previously frozen civilizational simulation nor a test of global celestial coherence.

### 6. Design gates before stronger claims

1. Establish real per-endpoint signing credentials, trusted public-key binding, and tamper-resistant receipt handling; test forged but internally self-consistent SEND/ACK/EXIT input.
2. Decide and prove semantics for replay, nonce/sequence scope, simultaneous events, and late delivery after exit, under honest and Byzantine participants.
3. Test relay crash/replacement and queue reconstruction from authorized endpoint RAW; test irrecoverable loss, prolonged partitions, fairness, and divergent views.
4. Persist histories durably and define independent anchors/retention rules when evidentiary integrity matters. Hash consistency alone does not resist rewriting the entire ledger.
5. Keep the original 20-case acceptance suite intact, add new cases with separate identifiers, and publish positive, negative, and missing evidence distinctly.

### 7. Exact disposition

**Reproduced:** original executable checks and deterministic trace; finite RAW/VIEW collision.

**New independent failure under stronger threat model:** claimed remote actor origin is not authenticated by public structural key labels.

**Unresolved:** Byzantine/production guarantees, relay replacement, distributed liveness, durable provenance, long-run civilizational performance, and causal relationship to other model families.

**Source files are untouched.** This note and v7.1b supplement are new derivatives. The v7.1a work and prior numerical experiments remain independently preserved.
