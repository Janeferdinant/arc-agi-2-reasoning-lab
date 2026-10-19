#!/usr/bin/env python3
"""
scripts/build_submission.py - Generate the official Kaggle submission.json file.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.submission.generator import generate_submission
from src.submission.validator import validate_submission_dict
TEST_CHALLENGES = BASE_DIR / "data" / "arc-agi_test_challenges.json"
SUBMISSION_PATH = BASE_DIR / "submission.json"

def main():
    if not TEST_CHALLENGES.exists():
        print(f"[-] Test challenges file not found at {TEST_CHALLENGES}")
        sys.exit(1)

    print("=== ARC Prize 2026: Building Submission ===")
    generate_submission(TEST_CHALLENGES, SUBMISSION_PATH)

    # Validate output
    import json
    with open(TEST_CHALLENGES, "r", encoding="utf-8") as f:
        challenges = json.load(f)
    expected_tasks = {tid: len(tdata.get("test", [])) for tid, tdata in challenges.items()}

    with open(SUBMISSION_PATH, "r", encoding="utf-8") as f:
        sub_data = json.load(f)

    is_valid, errors = validate_submission_dict(sub_data, expected_tasks)
    if is_valid:
        print("[+] SUCCESS: submission.json passed all strict schema checks!")
    else:
        print(f"[-] FAILED: submission.json has {len(errors)} validation errors:")
        for err in errors[:10]:
            print(f"    - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
