# ARC Prize 2026 — Public Solution Research & Architectural Comparison

## 1. Overview & Landscape Analysis
ARC-AGI-2 (Abstraction and Reasoning Corpus v2) represents a substantial step forward from ARC-AGI-1. The benchmark tests general fluid intelligence, compositional reasoning, and few-shot program induction.

In this research phase, we conducted an in-depth source code and architectural audit of key public solutions and repositories:
1. **Official ARC-AGI-2** (`arcprize/ARC-AGI-2`): Baseline task definition, dataset format, and 1,000 train + 120 eval tasks.
2. **`jaywang172/ARC-Prize-2026---ARC-AGI-2`**: High-ranking Kaggle workspace exploring Test-Time Training (TTT), Transformer Reasoning Models (TRM 2.16GB checkpoints), NVARC 4B / 2B models, and ensemble candidate selection.
3. **`sufian07/arc-prize-2026`**: Minimalist deterministic symbolic baseline with pure Python stdlib, strict demonstration consistency gating, and fast evaluation harness.
4. **`Vitalcheffe/arc-agi2`**: Multi-family DSL (`dsl.py`, `dsl2.py`), object extraction (4-connected, 8-connected, per-color connected components), gravity simulation, bounding box operations, hole-filling, and priority ranking.

---

## 2. In-Depth Comparative Dimensions

| Dimension | Symbolic / DSL (`Vitalcheffe`, `sufian07`) | Neural / Foundation Model (`jaywang172` NVARC/TRM) | Our Hybrid Architecture (`arc-solver`) |
|---|---|---|---|
| **Core Paradigm** | Pure symbolic transformation rules & search | Fine-tuned LLM / VLM with test-time search | Multi-family symbolic DSL + Candidate Verifier + Ranker |
| **Object Reasoning** | Connected component labeling (4/8/color-split), bounding box analysis, gravity, alignment | Learned implicit spatial attention, vulnerable to ragged grids and cell-level hallucinations | Explicit component extraction, color masks, background inference, object transforms |
| **Grid Geometry & Symmetry** | Exact matrix operations: $D_4$ dihedral group (rot90, 180, 270, transpose, anti-transpose, flip-h, flip-v) | Autoregressive token generation or spatial diffusion | Fast matrix symmetries with exact preservation of discrete integer semantics |
| **Search Space & Budgets** | Bounded combinatorial search over composable primitives; rejects non-explaining rules early | Sample $K$ candidate programs or grids (e.g. $K=20$ to $K=64$) | Tiered search: $O(1)$ direct invariants $\to$ single-primitive transforms $\to$ composite DSL |
| **Demonstration Consistency** | Strict 100% training pair exact match required before touching test query | Weak or probabilistic loss during fine-tuning / TTT | Strict demonstration verification: candidate rule must score 1.0 on all demonstration pairs |
| **Pass@2 Strategy** | Often identical top-1 or fallback | Temperature sampling to induce candidate diversity | Principled Pass@2: Attempt 1 is highest-confidence rule; Attempt 2 is diverse alternate valid candidate |
| **Inference Hardware** | CPU-only, lightweight, $< 100$ MB RAM | Heavy GPU requirement (A100/H100/T4), $> 8$ GB VRAM | Lightweight CPU execution ($< 250$ MB RAM), zero GPU overhead, instant Kaggle offline submission |
| **Latency per Task** | $50\text{ ms} - 1\text{ s}$ | $10\text{ s} - 120\text{ s}$ per task | $\sim 20 - 150\text{ ms}$ per task |
| **Contamination Risk** | Zero contamination risk | High risk (e.g., NVARC 2B contaminated with evaluation set) | Zero contamination risk, strict dataset isolation |

---

## 3. Analysis of Critical Failure Modes & Contamination Audits

### The NVARC 2B Contamination Finding
As audited in `jaywang172`'s benchmark log, the public score of 145/172 reported by some community notebooks for NVARC 2B was an artifact of **data leakage**: the public evaluation query outputs had been included in the supervised fine-tuning (SFT) mixture. When evaluated on truly unseen private tasks, performance collapsed.
**Lesson for our system**:
- Never tune hyper-parameters on the evaluation set.
- Keep the test set strictly hidden.
- Enforce exact-match verification strictly on demonstration pairs.

### Cell Ambiguity & Incomplete Palette Coverage
In `sufian07/arc_agi_2/solvers.py`, a key bug in naive color-mapping was identified:
If color $C$ appears in a test input grid but was never observed in any demonstration input grid, an unprincipled solver either passes it through or guesses. In training task `aabf363d`, passing through color 8 caused 16 incorrect cells.
**Our architectural requirement**:
- An explicit rule must either account for all test colors or abstain honestly, allowing the second attempt or higher-level DSL fallback to engage.

### Ragged / Non-Rectangular Grid Invariants
Many neural models output ragged lines or fail to preserve output rectangularity when dimension changes occur (e.g., $10 \times 10 \to 3 \times 3$).
**Our architectural requirement**:
- Hard dimensional invariants. The output dimensions must be deterministically deduced from:
  1. Fixed dimensions from demonstrations (constant output shape).
  2. Proportional scale factor (e.g., $2\times$, $3\times$, integer division).
  3. Bounding box of extracted primary object.
  4. Identity shape (same as test input).

---

## 4. Synthesis: Our ARC-AGI-2 Reasoning Lab Architecture
Based on these findings, we synthesize a multi-tiered solver architecture:
1. **Tier 1 — Exact Geometric & Global Invariants**:
   - Identity, Symmetries ($D_4$ group), Fixed Constant outputs, Uniform Palette Remapping.
2. **Tier 2 — Object-Centric Operations**:
   - Connected component extraction with background auto-detection.
   - Bounding box crop, padding, and framing.
   - Gravity / Drop simulation in 4 cardinal directions.
   - Hole filling and enclosed contour completion.
3. **Tier 3 — Spatial & Cellular Composition**:
   - Periodicity & tiling (repeating patterns).
   - Color substitution by frequency or component size.
   - Symmetry completion (half-grid reflection along vertical/horizontal axis).
4. **Tier 4 — Candidate Evaluator & Pass@2 Selector**:
   - Exact scoring on all demonstration pairs.
   - Complexity penalty (Occam's razor: simpler transformations preferred).
   - Selection of 2 diverse candidate predictions for `attempt_1` and `attempt_2`.
