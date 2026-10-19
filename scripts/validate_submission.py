#!/usr/bin/env python3
"""
scripts/validate_submission.py - Standalone strict validator for submission.json.
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.submission.validator import validate_submission_dict
TEST_CHALLENGES = BASE_DIR / "data" / "arc-agi_test_challenges.json"
SUBMISSION_PATH = BASE_DIR / "submission.json"

def main():
    target_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SUBMISSION_PATH
    if not target_path.exists():
        print(f"[-] Submission file not found: {target_path}")
        sys.exit(1)

    if not TEST_CHALLENGES.exists():
        print(f"[-] Reference test challenges file not found: {TEST_CHALLENGES}")
        sys.exit(1)

    with open(TEST_CHALLENGES, "r", encoding="utf-8") as f:
        challenges = json.load(f)
    expected_tasks = {tid: len(tdata.get("test", [])) for tid, tdata in challenges.items()}

    try:
        with open(target_path, "r", encoding="utf-8") as f:
            sub_data = json.load(f)
    except Exception as e:
        print(f"[-] Failed to parse submission JSON: {e}")
        sys.exit(1)

    is_valid, errors = validate_submission_dict(sub_data, expected_tasks)
    print(f"\n--- Submission Validation Report for {target_path.name} ---")
    print(f"Target Tasks: {len(expected_tasks)}")
    print(f"Submitted Tasks: {len(sub_data)}")
    if is_valid:
        print("[+] STATUS: PASS - All tasks, attempts, and grid matrices are strictly valid.")
        sys.exit(0)
    else:
        print(f"[-] STATUS: FAIL - Found {len(errors)} validation errors:")
        for err in errors[:20]:
            print(f"    - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
