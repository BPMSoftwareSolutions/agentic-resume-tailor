#!/usr/bin/env python3
"""
Restore missing experiences to a target resume by copying from a source resume
based on employer names. Defaults to dry-run (no changes written) unless --apply is set.

Usage:
  python scripts/restore_missing_experiences.py \
    --target-resume-id 8919f18f-d46a-4cc5-807d-8a4618e80ddd \
    --source-resume-id 3f288368-84c3-4de2-b9d3-573719ff6134 \
    --employers "BPM Software Solutions" "Interactive Business Solutions" \
               "John Deere Landscapes" "Soave Enterprises" "Compuware" \
               "ParTech, Inc." "Nexiq Technologies (formerly MPSI)" \
    [--apply]
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path("data")


def normalize(name: str) -> str:
    return (
        name.lower().replace("–", "-").replace("—", "-").replace("−", "-")
        if isinstance(name, str)
        else ""
    )


def load_resume(resume_id: str) -> Dict[str, Any]:
    p = DATA_DIR / "resumes" / f"{resume_id}.json"
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save_resume(resume_id: str, data: Dict[str, Any]) -> None:
    p = DATA_DIR / "resumes" / f"{resume_id}.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser(description="Restore missing experiences from a source resume")
    ap.add_argument("--target-resume-id", required=True)
    ap.add_argument("--source-resume-id", required=True)
    ap.add_argument("--employers", nargs="+", required=True)
    ap.add_argument("--apply", action="store_true", help="Write changes to disk")
    args = ap.parse_args()

    target = load_resume(args.target_resume_id)
    source = load_resume(args.source_resume_id)

    target_exps = target.get("experience", [])
    source_exps = source.get("experience", [])

    target_emp_set = {normalize(e.get("employer", "")) for e in target_exps}

    to_copy: List[Dict[str, Any]] = []
    for emp in args.employers:
        key = normalize(emp)
        match = next(
            (e for e in source_exps if normalize(e.get("employer", "")) == key),
            None,
        )
        if not match:
            print(f"⚠ Not found in source: {emp}")
            continue
        if key in target_emp_set:
            print(f"✓ Already present in target: {emp}")
            continue
        to_copy.append(match)

    if not to_copy:
        print("No experiences to restore.")
        return

    print("Will restore the following experiences:")
    for e in to_copy:
        print(f"  • {e.get('employer')} — {e.get('role')}")

    if args.apply:
        target_exps.extend(to_copy)
        target["experience"] = target_exps
        save_resume(args.target_resume_id, target)
        print("\n[SUCCESS] Experiences restored and file updated.")
    else:
        print("\n(Dry run) Use --apply to write changes.")


if __name__ == "__main__":
    main()

