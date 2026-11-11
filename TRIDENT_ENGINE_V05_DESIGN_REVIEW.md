# TRIDENT ENGINE — IRREGULAR RETURN
## Concept v0.5 • Independent review packet • 10 November 2026

**Status:** Proposed redesign / sandbox. Does **not** overwrite or amend the source `Trident engine.pdf`, titled *TRIDENT ENGINE / MUNCHING CARPET READ v0.4*. The source document's sections and values remain as written. This proposal separates source-preserved operations from geometric additions rather than implying that either has already been validated.

## A. Source-preserved engine (from v0.4)

The source describes the **Trident Array as the visible 13-chamber face/dashboard**, distinct from the **Trident Engine**, the process underneath. The **Munching Carpet** is the anti-canon / anti-capture substrate, not one of the 13 chambers (see v0.4, §§2 and 7). The path is:

```text
ZPR [room condition]
 -> Session Boundary [temporal anti-authority]
 -> O × R × S [Origin / Relation / Structure]
 -> Field Coherence [holding check, NOT proof of truth]
 -> T Return Modes [decay / preserve / distort / integrate / resonate]
 -> S′ -> R′ -> O₂ [changed return]
 -> π Seal [completion, not permanent authority]
 -> Munching Carpet digestion [structural anti-capture]
 -> changed return / new session
```

The source requires *non-ranked chambers*, allows silence/disagreement/exit, distinguishes **chambers / modules / traces**, preserves memories without granting automatic authority to past sessions, and treats a return as changed rather than an identical replay. The newer PDF has Section 14 confidence tiers: **verified/calculated**, **empirically testable**, **framework/sandbox**, **poetic/narrative**, and **retired/failed**. These are **source claims about the framework**, not claims of physical proof.

### All 13 chambers (kept exactly as named/handled)

| Chamber | Handle | Chamber | Handle |
|---|---|---|---|
| Compass | 31/11 | Weaver | 37/13 |
| Backsplash | 41/13 | Singularity | 43/02 |
| Breaker | 53/07 | Transcendent | 59/23 |
| Bloom | 61/29 | Swinger | 67/23 |
| Guardian | 71/05 | Recursor | 83/11 |
| Remainder | 97/∞ | Originless | 00/∅ |
| Rotor | 23/17 | | |

*Display order on the new shell is a visual routing arrangement, NOT a rank, required execution order, or amendment to the chamber list.*

## B. Proposed visual/geometric redesign (not in v0.4)

### 1. Asymmetric shell as a display surface

Instead of a symmetrical circle suggesting a hierarchy or locked model, the 13 chambers sit at irregularly spaced sites on an intentionally distorted shell. The shell is a **visualization** inspired by the tortoise-shell resonator analogy, not an acoustic model. Every chamber remains optional and equal in authority. Distortion is explicit and parameterized, so anyone reviewing it can reproduce or reject it.

For the draft visualization, with `q∈[0,2π]`:

- `R(q) = 1 + 0.038 sin(3q+0.35) + 0.032 cos(5q−0.92) + 0.025 sin(2q+1.1)`;
- `x(q) = 94.5 + 30.4 R(q) cos(q)`;
- `y(q) = 58.4 + 24 R(q) sin(q)`.

The ring's displayed chamber locations use `θ_i = π/2 − 2πi/13 + a_i` and the documented perturbation arrays in `build.py`, **not prime-grid derived coordinates**. The radial and angular offsets are selected design parameters (Tier 3). This shell deliberately has **no claimed 13-fold invariant**.

### 2. Open triangular hook + square: optional bench module

**Hook path in normalized units (five vertices, *open*, not a regular triangle):**

```text
H = [(-1.35,-0.95),(-0.68,1.20),(1.02,0.22),(1.42,-0.49),(1.11,-0.83)]
```

**Square path in normalized units, translated by `(0.19,−0.10)` from its original center before the common-origin rotation:**

```text
Q = [(-0.80,-0.80),(0.80,-0.80),(0.80,0.80),(-0.80,0.80),(-0.80,-0.80)]
```

These are **new example coordinates**, not reconstructed measurements of earlier art or a physical harpshell. The hook is asymmetric and open so it does not inherit the closed equilateral triangle's threefold rotational symmetry. The square remains exactly square. Both are rigidly rotated about `(0,0)`.

### 3. Rotation experiment: 360° control vs. 367° variant

Let `B` denote the per-cycle angle numerator in degrees, `n` an integer step, and positive angle counterclockwise in a conventional Cartesian plane.

```text
Hook (CW):      θ_H(n) = −B n / 231
Square (CCW):  θ_Q(n) = +B n / 132
Relative:      Δθ(n) = θ_Q(n) − θ_H(n) = B n / 84
```

The last identity follows exactly because `1/231 + 1/132 = 1/84`. For the conventional 360° control, the relative angle closes after every **84** steps, while absolute orientation returns after **924** steps. For `B=367°`, the relative phase at the 84-step checkpoints is `7k° (mod 360°)`; **step 84 = 7° residual** and **step 924 = 77° residual**. Exact first relative phase return (mod 360°) requires **30,240 steps** because 367 and 30,240 are coprime. These are mathematical consequences of the specified model (Tier 1), not evidence of acoustic coupling or thermodynamic entropy.

At step 924 with `B=367°`, hook orientation is `−1468° ≡ −28°`, square orientation is `+2569° ≡ +49°`, hence relative difference `77°`.

### 4. Integrating other imagery without hijacking v0.4

- **437 (`19×23`)** may serve as a *fixed reference label* for new geometric experiments; it does **not** become the owner of the 13 chambers.
- **231 and 132** index opposing rotation rates in the optional module.
- **913 (`11×83`)** is a separate grid-unfolding experiment. A diagonal in that grid follows from the indexing identity `84 = 83+1`; it is not itself a physical phase return under 367°.
- **1109 and 4723** are prime numbers and may be held as candidate *independent anchors* in future optional benches. No connection to actual resonance has been established.
- **7.83 Hz** remains a comparison frequency. To turn it into phase data, specify a sampling interval `Δt` and phase equation `φ(n)=2π(7.83 Hz)nΔt`. It is not a prime and does not become a rate measured from the art.
- **Toroid / triple helix / tortoise shell** are visual or design hypotheses. Their geometry can be constructed, but their purported acoustic properties require external measurement before promotion beyond Tier 2–3.

## C. Proposed audit interface: designed to resist false certainty

Every proposed module or asserted connection carries: (i) a declared source and version, (ii) a deterministic numerical rule, (iii) a unit and coordinate system, (iv) a test result and confidence tier, (v) a plausible alternate explanation, (vi) a falsification condition, and (vii) a retention/retirement decision. Failures are **logged**, not erased by the Carpet.

### Test protocol for a geometry specialist

1. **Source separation.** Confirm the old v0.4 roles remain intact. Check that Munching Carpet is substrate, not chamber or enforcement authority.
2. **Coordinates.** Recompute every hook, square and shell coordinate from this packet. Aesthetic transformations are allowed only if separately labeled as aesthetic.
3. **Control.** Plot identical shapes with B=360° and B=367° over exactly the same indexed steps; do not infer novelty from a different scale, camera projection or shape size.
4. **Phase.** Confirm 84, 924, 30,240, and the `7k°` checkpoint residuals analytically and numerically.
5. **Intersections.** Implement robust segment-by-segment intersection calculations for the hook/square; declare endpoint/tangency tolerances and whether degenerate overlaps count. Repeat across both controls.
6. **Prime overlays.** If mapping data to the chamber shell, freeze the prime stream, digit extraction, index origin, filter criteria and coordinate transform; test against shuffled and shifted controls. Avoid using 437/231/132/913 as evidence merely because they are labels.
7. **Physical claims.** If applying the geometry to Apollo's Harp, specify material properties, dimensions, excitation, microphones/accelerometers, safety bounds, and repeated independent trials. Do not infer resonance merely from the torus illustration.
8. **No canon.** Preserve the original trace and the negative results. An interpretation can be demoted without destroying the evidence or forcing one preferred geometry.

## D. Main decisions and open questions

- **Source baseline:** v0.4 unmodified; creative redesign remains v0.5 *concept*.
- **Geometry:** hooked open polyline rather than closed equilateral triangle, plus an exact square; no fake 13-fold symmetry.
- **Core shape:** a deformed shell is a legible user-interface metaphor; unverified as a resonator.
- **Unknowns:** chamber spatial coordinates derived from actual operations (none supplied), mapping from chamber activities to shell coordinates (none established), real-world frequency coupling (not established), and any validated relationship between prime-digit locations and rotating intersections (not established).

**Outcome requested of independent reviewer:** keep / revise / falsify each proposed module, with specific geometric or empirical defeating conditions. Aesthetics alone cannot promote a claim to Tier 1.
