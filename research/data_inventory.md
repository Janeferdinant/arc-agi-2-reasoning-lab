# ARC Prize 2026 — ARC-AGI-2: Dataset Inventory & Data Quality Report

## 1. Verified Competition Files

| Filename | Size (bytes) | SHA-256 Checksum (first 16) | Tasks | Status | Description |
|---|---|---|---|---|---|
| `arc-agi_training_challenges.json` | 4,010,050 | `779eaba89790ebad...` | 1,000 | VERIFIED | 1,000 public training tasks (demonstration pairs & test inputs) |
| `arc-agi_training_solutions.json` | 658,743 | `9f07a38bd25af5e8...` | 1,000 | VERIFIED | 1,000 public training task solutions (ground-truth test outputs) |
| `arc-agi_evaluation_challenges.json` | 984,679 | `e7c62a4bd211867c...` | 120 | VERIFIED | 120 public evaluation tasks without test solutions |
| `arc-agi_evaluation_solutions.json` | 223,838 | `84be4f4f39b79e82...` | 120 | VERIFIED | 120 public evaluation task solutions (ground-truth test outputs) |
| `arc-agi_test_challenges.json` | 1,015,295 | `232264c58f825ee7...` | 240 | VERIFIED | Hidden competition test inputs (eval tasks or unseen challenges) |
| `sample_submission.json` | 19,936 | `6b372dce41ad86a9...` | 240 | VERIFIED | Official Kaggle sample submission schema demonstration |

## 2. Dataset Metrics & Integrity Checks
- **All Files Present & Verified**: `True`
- **All JSON Parsed Successfully**: `True`
- **All Grid Values Valid (Integers in [0, 9])**: `True`
- **Grid Dimension Bounds**: Height [1 to 30], Width [1 to 30]
- **Total Training Tasks**: 1,000
- **Total Evaluation Tasks**: 120
- **Total Test Challenges**: 240 (with 259 test inputs)
- **Detected Anomalies / Corruptions**: 0

## 3. Official ARC Color Palette Mapping
| ID | Color Name | Hex Code | Visual Meaning / Usage |
|---|---|---|---|
| 0 | Black | `#000000` | Typically background / void |
| 1 | Blue | `#0074D9` | Object primary / accent |
| 2 | Red | `#FF4136` | Target / obstacle / marker |
| 3 | Green | `#2ECC40` | Goal / active segment |
| 4 | Yellow | `#FFDC00` | Highlight / connection |
| 5 | Grey | `#AAAAAA` | Border / separator / frame |
| 6 | Magenta / Fuchsia | `#F012BE` | Transformation indicator |
| 7 | Orange | `#FF851B` | Secondary entity |
| 8 | Teal / Cyan | `#7FDBFF` | Water / fill / symmetry axis |
| 9 | Maroon / Brown | `#870C25` | Special anchor / base |
