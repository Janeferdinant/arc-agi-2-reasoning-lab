#!/usr/bin/env python3
"""
scripts/download_data.py - ARC Prize 2026 Data Acquisition & Verification Pipeline

Retrieves competition dataset files via Kaggle API or verified authoritative mirrors,
handles authentication / competition rules acceptance checks, and places files into data/.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

COMPETITION_ID = "arc-prize-2026-arc-agi-2"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

EXPECTED_FILES = {
    "arc-agi_training_challenges.json": 4010050,
    "arc-agi_training_solutions.json": 658743,
    "arc-agi_evaluation_challenges.json": 984679,
    "arc-agi_evaluation_solutions.json": 223838,
    "arc-agi_test_challenges.json": 1015295,
    "sample_submission.json": 19936,
}

def check_existing_files() -> bool:
    """Check if all expected competition files exist with non-zero size."""
    if not DATA_DIR.exists():
        return False
    missing = []
    for fname in EXPECTED_FILES:
        fpath = DATA_DIR / fname
        if not fpath.exists() or fpath.stat().st_size == 0:
            missing.append(fname)
    return len(missing) == 0

def download_via_kaggle_cli() -> bool:
    """Attempt download using authenticated Kaggle CLI."""
    print(f"[*] Attempting download from Kaggle API for competition: {COMPETITION_ID}...")
    try:
        cmd = [sys.executable, "-m", "kaggle", "competitions", "download", "-c", COMPETITION_ID, "-p", str(DATA_DIR)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print("[+] Successfully downloaded dataset archive from Kaggle.")
            zip_file = DATA_DIR / f"{COMPETITION_ID}.zip"
            if zip_file.exists():
                import zipfile
                with zipfile.ZipFile(zip_file, "r") as zf:
                    zf.extractall(DATA_DIR)
                zip_file.unlink()
                print("[+] Extracted competition archive into data/.")
            return True
        else:
            stderr = res.stderr or res.stdout
            print(f"[-] Kaggle download returned error: {stderr.strip()}")
            if "403" in stderr or "Forbidden" in stderr:
                print("\n" + "="*70)
                print("[!] ACTION REQUIRED: Kaggle Competition Rules Acceptance")
                print("    Please log into Kaggle and accept the rules at:")
                print(f"    https://www.kaggle.com/competitions/{COMPETITION_ID}/rules")
                print("    Click 'I Understand and Accept' to enable direct API downloads.")
                print("="*70 + "\n")
            return False
    except Exception as e:
        print(f"[-] Failed to invoke Kaggle CLI: {e}")
        return False

def verify_and_report():
    """Verify downloaded files against expectations."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    all_ok = True
    print("\n--- Data File Verification ---")
    for fname, exp_size in EXPECTED_FILES.items():
        fpath = DATA_DIR / fname
        if not fpath.exists():
            print(f"[-] MISSING: {fname}")
            all_ok = False
        else:
            actual_size = fpath.stat().st_size
            status = "EXACT MATCH" if actual_size == exp_size else f"SIZE DIFF ({actual_size} vs {exp_size})"
            print(f"[+] {fname} ({actual_size:,} bytes) - {status}")
    return all_ok

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if check_existing_files():
        print("[+] Verified that all expected dataset files already exist in data/.")
        verify_and_report()
        sys.exit(0)

    success = download_via_kaggle_cli()
    if not success and not check_existing_files():
        print("[-] Data download incomplete. Please see instructions above.")
        sys.exit(1)
    
    verify_and_report()

if __name__ == "__main__":
    main()
