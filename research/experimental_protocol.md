# ARC Prize 2026 — Experimental Protocol & Evaluation Methodology

## 1. Experimental Integrity & Data Splitting
To prevent data contamination and overfitting:
1. **Internal Development Split**:
   - The 1,000 tasks from `arc-agi_training_challenges.json` are partitioned into:
     - `train_dev` (800 tasks, fixed seed 42): Used for rule synthesis, DSL operator discovery, and parameter exploration.
     - `train_val` (200 tasks, fixed seed 42): Held-out validation partition used for candidate ranking calibration and ablation testing.
2. **Official Evaluation Split**:
   - The 120 tasks from `arc-agi_evaluation_challenges.json` (and `arc-agi_evaluation_solutions.json`) serve as the benchmark validation set.
   - Evaluated periodically to assess out-of-distribution generalization without repeatedly tuning rules directly on it.
3. **Hidden Test Set**:
   - The 240 tasks in `arc-agi_test_challenges.json` represent competition test queries with hidden labels.

## 2. Evaluation Metrics

### Exact Match Accuracy (Pass@1)
For a task with $M$ test inputs, each test input $i \in \{1, \dots, M\}$ has prediction $P_i$ and ground truth $Y_i$.
$$\text{Match}(P_i, Y_i) = \begin{cases} 1 & \text{if } P_i = Y_i \text{ (every cell identical)} \\ 0 & \text{otherwise} \end{cases}$$
Per-task solved criterion:
$$\text{TaskSolved}(P, Y) = \prod_{i=1}^M \text{Match}(P_i, Y_i)$$

### Pass@2 Exact Match Accuracy
Each test input receives two predictions: $P_i^{(1)}$ (attempt 1) and $P_i^{(2)}$ (attempt 2).
$$\text{MatchPass@2}(P_i, Y_i) = \max\left(\text{Match}(P_i^{(1)}, Y_i), \text{Match}(P_i^{(2)}, Y_i)\right)$$
$$\text{TaskSolvedPass@2}(P, Y) = \prod_{i=1}^M \text{MatchPass@2}(P_i, Y_i)$$

## 3. Benchmarking Protocol & Ablation Matrix
Experiments compare the following incremental solver configurations:
1. **Baseline 0: Identity & Constant** (`baseline_identity_const`):
   - Only identity passthrough and constant-output detectors.
2. **Baseline 1: Geometric Symmetry ($D_4$)** (`baseline_geometry`):
   - Identity, rotations (90°, 180°, 270°), horizontal/vertical reflections, transpose, anti-transpose.
3. **Solver V1: Global Color & Direct Invariants** (`solver_v1_palette`):
   - Geometric symmetries + Bijective color mappings + Global scaling & tiling.
4. **Solver V2: Object-Centric DSL** (`solver_v2_objects`):
   - V1 + Connected components (4-way, 8-way, color-split) + Bounding box crops + Gravity simulation + Hole filling.
5. **Solver V3: Full Hybrid & Pass@2 Diversity Ranking** (`solver_v3_hybrid_pass2`):
   - V2 + Cellular propagation + Dual-candidate diversity ranking + Strict demonstration consistency gating.

## 4. Resource & Latency Limits
- Max timeout per task: 2.0 seconds.
- Memory ceiling: 500 MB RSS.
- Exact tracking of runtime (ms), candidate generation count, and failure categorization.
