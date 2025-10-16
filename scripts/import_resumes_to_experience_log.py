#!/usr/bin/env python3
"""Import experience bullets from selected resume JSON files into the ExperienceLog.

This script looks up the resume index to find the resume ids for the following names:
- Master Resume
- Sidney_Jones_Senior_Software_Engineer_Credibly
- Sidney_Jones_Senior_Software_Engineer_GM

For each resume, it collects all bullet `text` values, deduplicates them, and creates
an `Experience` entry with bullets populated and tags/technologies left empty (tags
could be populated from the bullet `tags` if desired).
"""
from pathlib import Path
import json
import sys
from typing import List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.experience_log import ExperienceLog, Experience


def load_index(index_path: Path) -> dict:
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_resume(resume_path: Path) -> dict:
    with open(resume_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_bullets(resume: dict) -> List[str]:
    bullets = []
    for exp in resume.get("experience", []):
        for b in exp.get("bullets", []):
            text = b.get("text") if isinstance(b, dict) else b
            if text:
                bullets.append(text.strip())
    # deduplicate while preserving order
    seen = set()
    unique = []
    for t in bullets:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique


def main():
    data_resumes = Path(ROOT) / "data" / "resumes"
    index = load_index(data_resumes / "index.json")

    target_names = [
        "Master Resume",
        "Sidney_Jones_Senior_Software_Engineer_Credibly",
        "Sidney_Jones_Senior_Software_Engineer_GM",
    ]

    name_to_id = {r["name"]: r["id"] for r in index.get("resumes", [])}

    log = ExperienceLog()

    added_count = 0

    for name in target_names:
        rid = name_to_id.get(name)
        if not rid:
            print(f"Warning: resume named '{name}' not found in index")
            continue

        resume_file = data_resumes / f"{rid}.json"
        if not resume_file.exists():
            print(f"Warning: resume file missing: {resume_file}")
            continue

        resume = load_resume(resume_file)
        bullets = extract_bullets(resume)
        if not bullets:
            print(f"No bullets found for {name}")
            continue

        exp = Experience(
            id="",
            employer=resume.get("experience", [{}])[0].get("employer", name),
            role=resume.get("experience", [{}])[0].get("role", ""),
            dates=resume.get("experience", [{}])[0].get("dates", ""),
            location=resume.get("location", ""),
            bullets=bullets,
            skills=[],
            technologies=[],
            techniques=[],
            principles=[],
            notes=f"Imported from resume: {name}",
        )

        try:
            log.add(exp)
            print(f"Added experience from '{name}' with {len(bullets)} bullets")
            added_count += 1
        except ValueError as ve:
            print(f"Skipped duplicate experience for '{name}': {ve}")
        except Exception as e:
            print(f"Error adding experience for '{name}': {e}")

    print(f"Done. Experiences added: {added_count}")


if __name__ == "__main__":
    main()
