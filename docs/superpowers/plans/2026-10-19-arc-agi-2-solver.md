# ARC Prize 2026 — ARC-AGI-2 Solver, Research Pipeline & Vercel Dashboard Implementation Plan

> **For agentic workers:** Native execution mode. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, evaluate, and package a competitive, reproducible ARC-AGI-2 reasoning solver, research pipeline, valid Kaggle submission generator, research documentation, interactive Next.js dashboard, and publish to GitHub and deploy to Vercel.

**Architecture:** Hybrid neuro-symbolic and DSL-based program synthesis solver with exact grid-match evaluation, Pass@2 candidate generation, confidence ranking, strict schema validation, offline Kaggle-compatible pipeline, and a modern Next.js/Tailwind/Recharts research dashboard visualizing genuine benchmark experiments and interactive task inspection.

**Tech Stack:** Python 3.14 (NumPy, SciPy, Kaggle SDK, Pytest), Next.js 15+ / React 19, TypeScript, Tailwind CSS, Lucide Icons, Recharts, GitHub API / Git CLI, Vercel CLI.

**Spec:** User Master Prompt for ARC Prize 2026 — ARC-AGI-2.

## Global Constraints
- Python 3.14 compatible, no unnecessary GPU dependencies for symbolic solver.
- Offline inference compatible for Kaggle (no internet access during evaluation).
- Exact grid format matching Kaggle ARC schema: `{"attempt_1": [[...]], "attempt_2": [[...]]}` for each test input.
- Valid 2D integer grids, 10 allowed colors (0-9).
- Clean separation between frontend (static/API Next.js) and Python reasoning engine.
- Zero secret leaks: tokens stored in environment or WCM, never committed to git.
- Only genuine measured metrics reported in research docs and dashboard.

## Review Focus
1. Non-square grids and dimension changes between input and output.
2. Tasks with multiple test pairs per task ID (preserving test input order).
3. Candidate ranking and Pass@2 diversity (attempt_1 vs attempt_2 must not be duplicate if alternative valid candidates exist).
4. Edge cases in connected components: diagonal connectivity vs 4-connectivity, background color determination.
5. Missing or corrupt challenge entries in Kaggle dataset.

---

### Task 1: Environment & Credentials Setup, Kaggle Data Acquisition & Verification
- Retrieve Kaggle, GitHub, and Vercel credentials from Windows Credential Manager.
- Download official competition dataset files: `arc-agi_training_challenges.json`, `arc-agi_training_solutions.json`, `arc-agi_evaluation_challenges.json`, `arc-agi_evaluation_solutions.json`, `arc-agi_test_challenges.json`, `sample_submission.json`.
- Implement `scripts/download_data.py` and `scripts/verify_data.py`.
- Generate `research/competition_requirements.md`, `research/data_inventory.md`, and `research/data_quality_report.json`.

### Task 2: Public Research & Competitive Solution Study
- Investigate official ARC-AGI-2 repo (`arcprize/ARC-AGI-2`), `jaywang172/ARC-Prize-2026---ARC-AGI-2`, `sufian07/arc-prize-2026`, and `Vitalcheffe/arc-agi2`.
- Formulate synthesis of DSL primitives, object extraction, cellular automata, candidate ranking, and search strategies.
- Create `research/solution_comparison.md` and `research/experimental_protocol.md`.

### Task 3: Core Grid Primitives, Object Model & DSL Transformations (TDD)
- Implement `src/arc_solver/grid.py`: grid representation, color masks, bounding boxes, crops, rotations, reflections, scaling, translations, symmetries.
- Implement `src/arc_solver/objects.py`: connected components (4-way and 8-way), background color inference, object properties (size, shape, color, position, bounding box).
- Implement `src/arc_solver/transforms.py`: composable transformation primitives (color mapping, flood fill, object alignment, gravity, tiling, symmetry completion).
- Write comprehensive unit tests in `tests/test_grid.py`, `tests/test_objects.py`, `tests/test_transforms.py`.

### Task 4: Multi-Family Hybrid Solver & Bounded Search Engine
- Implement solver families:
  1. Identity / Direct geometric symmetries (rotations, reflections, translations).
  2. Color remapping & frequency-based palette transformations.
  3. Object-centric transforms (scale, crop to bounding box, gravity/drop, align).
  4. Cellular/Pattern propagation & tiling.
  5. Fallback heuristics.
- Implement candidate evaluation against demonstration pairs (strict demonstration consistency check).
- Implement Pass@2 candidate generation and diversity ranking (`attempt_1` vs `attempt_2`).
- Implement `src/arc_solver/solver.py` with search budgets and timeouts.
- Unit tests in `tests/test_solver.py`.

### Task 5: Evaluation Framework, Experiments & Error Analysis
- Implement exact grid-match evaluation and Pass@2 scorer in `src/evaluation/evaluator.py`.
- Run benchmarking experiments on training and evaluation tasks.
- Record results in `research/experiment_results.csv`, `research/error_analysis.md`.
- Implement CLI runners `scripts/train.py`, `scripts/predict.py`, `scripts/evaluate.py`, `scripts/run_experiments.py`.

### Task 6: Kaggle Submission Pipeline & Strict Submission Validator
- Implement `src/submission/generator.py` and `scripts/build_submission.py`.
- Implement `src/submission/validator.py` and `scripts/validate_submission.py`.
- Write unit tests in `tests/test_submission.py` testing malformed inputs, missing tasks, incorrect dims, ragged grids, out-of-range colors.
- Generate and validate `submission.json` against `arc-agi_test_challenges.json`.

### Task 7: Interactive Research Dashboard (Next.js, TypeScript, Tailwind, Recharts)
- Build responsive, professional dark-mode research lab UI in `dashboard/`:
  - Page A: Overview (KPIs, best validation score, pass@2, verified data status, submission status).
  - Page B: Dataset Explorer (task counts, grid visualizer with official 10-color palette, input/output inspection).
  - Page C: Experiment Tracker (experiment history, ablation comparison, runtime, filter/sort).
  - Page D: Solver Analysis (solver family accuracy, failure modes, ranking calibration).
  - Page E: Interactive ARC Playground (load task, run solver, visual comparison, explanation).
  - Page F: Submission Center (file validation status, JSON schema checks, download submission).
  - Page G: Research & Documentation (markdown render of research docs).
- Test dashboard build locally (`npm run build`).

### Task 8: GitHub Repository & Vercel Production Deployment
- Initialize Git remote for `https://github.com/Janeferdinant/arc-agi-2-reasoning-lab.git`.
- Create GitHub repo via API if needed, commit all files, push branch `main`.
- Deploy dashboard to Vercel via Vercel CLI with Vercel token from WCM.
- Verify live deployment URL and check routes.
- Produce comprehensive README.md and final verification report.
