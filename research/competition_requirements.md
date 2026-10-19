# ARC Prize 2026 — ARC-AGI-2: Competition Requirements & Protocol

## 1. Executive Summary & Competition Overview
- **Competition Name**: ARC Prize 2026 — ARC-AGI-2
- **URL**: [https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2)
- **Rules URL**: [https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/rules](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/rules)
- **Official Benchmark Repository**: [https://github.com/arcprize/ARC-AGI-2](https://github.com/arcprize/ARC-AGI-2)
- **Prize Pool**: $700,000 USD (Part of ARC Prize 2026 series, total $1,550,000+)
- **Final Deadline**: November 02, 2026, 23:59:00 UTC

## 2. Benchmark Formulation & Core Knowledge Priors
ARC-AGI (Abstraction and Reasoning Corpus for Artificial General Intelligence v2) measures an AI system's ability to acquire new skills and solve novel visual/spatial reasoning problems without relying on internet-scale memorization.

### Task Specifications
- **Input/Output Representation**: 2D discrete grid of integers $\{0, 1, \dots, 9\}$, visualized as 10 distinct colors.
- **Grid Dimensions**: From $1 \times 1$ up to $30 \times 30$.
- **Dimensions Flexibility**: The output grid does NOT necessarily match the input grid dimensions (e.g. cropping, tiling, scale transformations).
- **Demonstrations**: Each task provides $N$ demonstration input/output pairs (typically 2 to 5 pairs) under the `"train"` key.
- **Test Invocations**: Each task provides 1 or more test queries under the `"test"` key. For each test query, the model receives `"input"` and must construct the exact integer grid for `"output"`.

### Evaluation Metric: Pass@2 Exact Match
- **Allowed Attempts**: 2 attempts per test query (`attempt_1` and `attempt_2`).
- **Scoring**: A test input is solved if **either** `attempt_1` or `attempt_2` matches the true output grid **exactly** across every single cell.
- **Task Success Criterion**: A task is considered solved if and only if **all** test inputs within that task are correctly predicted. Partial credit within a task is 0.

## 3. Dataset Composition
The ARC-AGI-2 corpus comprises:
1. **Public Training Set (`training`)**: 1,000 tasks with full demonstration pairs and test solutions.
2. **Public Evaluation Set (`evaluation`)**: 120 tasks verified by controlled human testing (average human score: 66%).
3. **Semi-Private Evaluation Set**: Held by the benchmark organizers for commercial model evaluation.
4. **Fully-Private Competition Test Set**: Hidden Kaggle test set of ~100-200 tasks evaluated completely offline in a sandbox.

## 4. Kaggle Submission Schema
The submission must be exported as `submission.json` formatted as a single JSON object mapping each task ID in `arc-agi_test_challenges.json` to a list of prediction objects (one for each test query in the exact order):

```json
{
  "task_id_001": [
    {
      "attempt_1": [[0, 1], [2, 3]],
      "attempt_2": [[1, 0], [3, 2]]
    }
  ],
  "task_id_002": [
    {
      "attempt_1": [[0]],
      "attempt_2": [[1]]
    }
  ]
}
```

### Strict Submission Requirements
1. **Key Completeness**: All task IDs present in the test challenge file must be present in `submission.json`.
2. **Order Preservation**: If a task has multiple test inputs, the prediction array must preserve the exact index order.
3. **Dual Attempts**: Exactly two attempts (`attempt_1`, `attempt_2`) must be provided for every test input.
4. **Grid Validity**: 2D array of integers, $H \times W$ where $1 \le H, W \le 30$, and all cell values $c \in \{0, \dots, 9\}$. No ragged rows, no non-integer floats, no null values.
5. **No Internet Access**: The notebook evaluation environment is strictly offline (`Internet Disabled`). All weights, dependencies, and code must be pre-packaged.
6. **Execution Budget**: 9 hours CPU/GPU runtime limit on Kaggle Notebooks.

## 5. Account Access & Kaggle Rules Acceptance Notice
When accessing the dataset via the Kaggle API with an authenticated token, Kaggle enforces a one-time terms acceptance:
- **Action Required by Account Owner**: Visit [https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/rules](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/rules), ensure you are logged into your Kaggle account, and click **"I Understand and Accept"**.
- Until accepted, Kaggle API calls to download dataset files return `403 Forbidden`.
- Our pipeline automatically detects this condition, advises the user, and mirrors the identical official dataset directly from the authoritative open-source release `https://github.com/arcprize/ARC-AGI-2`.
