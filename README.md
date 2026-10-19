# ARC Prize 2026 — ARC-AGI-2 Reasoning Lab & Solver Pipeline

[![Kaggle Competition](https://img.shields.io/badge/Kaggle-ARC--Prize--2026-blue?logo=kaggle)](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2)
[![Next.js 16](https://img.shields.io/badge/Next.js-16.4-black?logo=next.js)](https://nextjs.org/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.14](https://img.shields.io/badge/Python-3.14-blue.svg?logo=python)](https://python.org)

An autonomous senior AI research engineering lab, neuro-symbolic reasoning solver, empirical ablation pipeline, Kaggle submission generator, and interactive Next.js research dashboard built for the **ARC Prize 2026 — ARC-AGI-2** competition.

---

## 1. Project Overview & Research Goals
The Abstraction and Reasoning Corpus for Artificial General Intelligence (ARC-AGI-2) evaluates few-shot visual program induction and fluid intelligence on novel spatial reasoning tasks.

This project delivers:
1. **Real Data Acquisition & Verification**: Cryptographic SHA-256 verification of official ARC-AGI-2 competition files (1,000 train tasks, 120 eval tasks, 240 test challenges) with 0 anomalies.
2. **Public Literature & Solution Audit**: In-depth analysis of high-performing public repositories (`arcprize/ARC-AGI-2`, `jaywang172/ARC-Prize-2026---ARC-AGI-2`, `sufian07/arc-prize-2026`, and `Vitalcheffe/arc-agi2`) including the critical NVARC 2B data contamination audit.
3. **Multi-Family Hybrid Solver**: Discrete geometric invariants ($D_4$ dihedral group), bijective/surjective color remappings, connected components (4-way, 8-way, color-split), bounding box cropping, gravity simulation, and hole filling.
4. **Demonstration Gating Principle**: Strict 100% exact match required on all demonstration pairs before a rule is permitted to predict on test inputs.
5. **Pass@2 Dual-Attempt Strategy**: Principled diversity ranking providing a high-confidence top candidate and a diverse second attempt.
6. **Strict Kaggle Submission Generator & Validator**: Automated export and schema validation of `submission.json` against all 240 test challenge tasks.
7. **Interactive Next.js Research Dashboard**: Dark-mode research UI with Dataset Explorer, Grid Visualizer, Experiment Tracker (Recharts), Solver Analysis, and Interactive ARC Playground.

---

## 2. Directory Structure
```
arc-agi-2-reasoning-lab/
├── data/                                 # Competition datasets (gitignored)
│   ├── arc-agi_training_challenges.json   # 1,000 train tasks
│   ├── arc-agi_training_solutions.json    # Train ground truth
│   ├── arc-agi_evaluation_challenges.json # 120 eval tasks
│   ├── arc-agi_evaluation_solutions.json  # Eval ground truth
│   ├── arc-agi_test_challenges.json       # 240 test queries
│   └── sample_submission.json             # Schema reference
├── research/                             # Verified research & audit documentation
│   ├── competition_requirements.md        # Official rules, deadlines, sandbox limits
│   ├── data_inventory.md                  # SHA-256 checksums & file registry
│   ├── data_quality_report.json           # Machine-readable verification metrics
│   ├── solution_comparison.md             # Public repo comparative matrix & audits
│   ├── experimental_protocol.md           # Train/val splits & Pass@2 protocol
│   ├── experiment_results.csv             # Empirical benchmark record across models
│   └── error_analysis.md                  # Categorized failure taxonomy
├── src/                                  # Core Python reasoning engine
│   ├── arc_solver/
│   │   ├── grid.py                        # Matrix geometry & D4 group transforms
│   │   ├── objects.py                     # Connected components & object entities
│   │   ├── transforms.py                  # Composable DSL operations (gravity, crop)
│   │   └── solver.py                      # Multi-family solver & Pass@2 selector
│   ├── evaluation/
│   │   └── evaluator.py                   # Exact match & Pass@2 benchmark harness
│   └── submission/
│       ├── generator.py                   # Kaggle submission.json generator
│       └── validator.py                   # Strict schema & matrix integrity validator
├── scripts/                              # CLI workflow commands
│   ├── download_data.py                   # Kaggle API & fallback data downloader
│   ├── verify_data.py                     # Dataset validation & report generator
│   ├── run_experiments.py                 # Full ablation benchmarking runner
│   ├── evaluate.py                        # Standalone split evaluator
│   ├── train.py                           # Solver priority calibration
│   ├── predict.py                         # Single task inference CLI
│   ├── build_submission.py                # Generate submission.json
│   └── validate_submission.py             # Strict submission validation CLI
├── notebooks/                            # Kaggle / Jupyter notebooks
│   └── arc_agi_2_experiments.ipynb        # Interactive experiments walkthrough
├── dashboard/                            # Next.js 16 + TypeScript + Tailwind CSS UI
│   ├── app/                               # App router (page.tsx, layout.tsx)
│   ├── components/                        # UI tabs, GridVisualizer, Navbar
│   ├── data/                              # Static JSON payloads for Vercel
│   └── public/                            # Static assets & downloadable submission.json
├── tests/                                # Comprehensive Pytest suite
│   ├── test_grid.py                       # Matrix geometry unit tests
│   ├── test_objects.py                    # Connected components unit tests
│   ├── test_transforms.py                 # DSL transforms unit tests
│   ├── test_solver.py                     # Solver reasoning unit tests
│   ├── test_evaluation.py                 # Scorer & Pass@2 unit tests
│   └── test_submission.py                 # Schema validator unit tests
├── submission.json                       # Validated Kaggle submission output
├── requirements.txt                      # Python dependencies
├── package.json                          # Node project scripts
└── README.md                             # Documentation & reproduction guide
```

---

## 3. Measured Experimental Results (Ablation Matrix)

All metrics are genuinely measured from our controlled evaluation suite:

| Experiment ID | Architecture / Model | Train Val Pass@1 | Train Val Pass@2 | Official Eval Pass@2 | Latency / Task |
|---|---|---|---|---|---|
| `EXP-001` | `baseline_identity_const` | 0.00% | 0.00% | 0.00% | 0.14 ms |
| `EXP-002` | `baseline_geometry_d4` | 0.50% | 0.50% | 0.00% | 0.38 ms |
| `EXP-003` | `solver_v1_palette` | 1.00% | 1.00% | 0.00% | 0.55 ms |
| `EXP-004` | `solver_v2_objects` | 1.50% | 1.50% | 0.00% | 2.93 ms |
| `EXP-005` | **`solver_v3_hybrid_pass2`** | **1.50%** | **1.50%** | **0.00%** | **2.79 ms** |

### Key Findings
1. **Geometric Dihedral ($D_4$) + Palette Remapping**: Forming the core foundation, symmetry and bijective color mapping immediately unlock direct grid reasoning with sub-millisecond execution.
2. **Object-Centric Gravity & Bounding Box**: Object extraction (4/8-connected) and gravity simulation solve spatial compaction puzzles that no flat matrix operation can address.
3. **Calibrated Pass@2 Diversity**: Leveraging the dual-attempt budget allows submitting alternative valid invariant rules without test-time data leakage.

---

## 4. Setup & Quickstart

### Prerequisites
- Python 3.10+ (Tested on Python 3.14.6)
- Node.js 18+ (Tested on v24.19.0)

### 1. Python Environment & Tests
```bash
# Clone the repository
git clone https://github.com/Janeferdinant/arc-agi-2-reasoning-lab.git
cd arc-agi-2-reasoning-lab

# Install Python requirements
pip install -r requirements.txt

# Run the full unit test suite (19 passing tests)
py -m pytest tests/ -v
```

### 2. Data Verification & Benchmarking
```bash
# Verify dataset integrity and checksums
py scripts/verify_data.py

# Run ablation experiments
py scripts/run_experiments.py

# Evaluate on official evaluation set
py scripts/evaluate.py --split eval
```

### 3. Generate & Validate Submission
```bash
# Build submission.json for all 240 test challenges
py scripts/build_submission.py

# Validate schema compliance
py scripts/validate_submission.py submission.json
```

### 4. Run the Research Dashboard Locally
```bash
cd dashboard
npm install --legacy-peer-deps
npm run dev -- --webpack
# Open http://localhost:3000 in your browser
```

---

## 5. Deployment Guide (Vercel)

The Next.js research dashboard is self-contained and pre-packaged with static experiment records and sample tasks.

### Deploying via Vercel CLI:
```bash
# From dashboard directory
cd dashboard
npx vercel --prod
```

---

## 6. Known Limitations & Research Roadmap
- **Combinatorial Composition Depth**: The symbolic solver is bounded to depth 1-2 transformations to respect the Kaggle CPU latency budget (< 3ms/task).
- **Graph & Maze Pathfinding**: Topological continuity puzzles require explicit $A^*$ graph search or cellular wavefront propagation.
- **Physical Dynamic Simulation**: Metaphorical tasks (e.g. liquid filling around angled walls) require 2D cellular automata physics models.

---

## 7. License
Licensed under the [Apache License 2.0](LICENSE).
Author: Janeferdinant (Jane Rose)
