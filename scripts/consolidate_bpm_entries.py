#!/usr/bin/env python3
"""
Consolidate BPM Software Solutions Experience Entries

This script consolidates 4 duplicate BPM entries into 1 comprehensive entry.

The 4 entries to consolidate:
- 0defdac1-d9bd-457f-904a-4c0609b84c32 (45 bullets, full-stack)
- 363bf2ac-eab2-43ba-8c01-28f834a53799 (30 bullets, financial systems)
- 3395fe5a-c811-4c31-8847-7a08431cca2f (18 bullets, automotive/embedded)
- 6ebb7a67-7a4c-4124-9941-ce5e29ec9f7c (5 bullets, leadership) - PRIMARY

The consolidated entry will use ID: 6ebb7a67-7a4c-4124-9941-ce5e29ec9f7c
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Set

# IDs of entries to consolidate
DUPLICATE_IDS = [
    "0defdac1-d9bd-457f-904a-4c0609b84c32",
    "363bf2ac-eab2-43ba-8c01-28f834a53799",
    "3395fe5a-c811-4c31-8847-7a08431cca2f",
]
PRIMARY_ID = "6ebb7a67-7a4c-4124-9941-ce5e29ec9f7c"


def load_experiences(path: str = "data/experiences.json") -> List[Dict[str, Any]]:
    """Load experiences from JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_experiences(experiences: List[Dict[str, Any]], path: str = "data/experiences.json"):
    """Save experiences to JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(experiences, f, indent=2, ensure_ascii=False)


def deduplicate_list(items: List[str]) -> List[str]:
    """Remove duplicates while preserving order."""
    seen: Set[str] = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def consolidate_bpm_entries(experiences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Consolidate 4 BPM entries into 1."""
    
    # Find all BPM entries
    bpm_entries = {e["id"]: e for e in experiences if e["employer"] == "BPM Software Solutions"}
    
    print(f"Found {len(bpm_entries)} BPM entries")
    for entry_id in bpm_entries:
        role = bpm_entries[entry_id]["role"]
        bullets_count = len(bpm_entries[entry_id]["bullets"])
        print(f"  - {entry_id}: {role} ({bullets_count} bullets)")
    
    # Collect all unique bullets
    all_bullets: List[str] = []
    for entry_id in DUPLICATE_IDS + [PRIMARY_ID]:
        if entry_id in bpm_entries:
            all_bullets.extend(bpm_entries[entry_id]["bullets"])
    
    # Deduplicate bullets
    unique_bullets = deduplicate_list(all_bullets)
    print(f"\nTotal bullets before dedup: {len(all_bullets)}")
    print(f"Total bullets after dedup: {len(unique_bullets)}")
    
    # Collect all unique skills
    all_skills: List[str] = []
    for entry_id in DUPLICATE_IDS + [PRIMARY_ID]:
        if entry_id in bpm_entries:
            all_skills.extend(bpm_entries[entry_id].get("skills", []))
    unique_skills = deduplicate_list(all_skills)
    print(f"\nTotal skills before dedup: {len(all_skills)}")
    print(f"Total skills after dedup: {len(unique_skills)}")
    
    # Collect all unique technologies
    all_techs: List[str] = []
    for entry_id in DUPLICATE_IDS + [PRIMARY_ID]:
        if entry_id in bpm_entries:
            all_techs.extend(bpm_entries[entry_id].get("technologies", []))
    unique_techs = deduplicate_list(all_techs)
    print(f"\nTotal technologies before dedup: {len(all_techs)}")
    print(f"Total technologies after dedup: {len(unique_techs)}")
    
    # Get primary entry as base
    primary_entry = bpm_entries[PRIMARY_ID].copy()
    
    # Update with consolidated data
    primary_entry["bullets"] = unique_bullets
    primary_entry["skills"] = unique_skills
    primary_entry["technologies"] = unique_techs
    primary_entry["role"] = "Senior Software Architect / Engineering Lead"
    primary_entry["notes"] = "Consolidated from 4 duplicate entries (IDs: 0defdac1-d9bd-457f-904a-4c0609b84c32, 363bf2ac-eab2-43ba-8c01-28f834a53799, 3395fe5a-c811-4c31-8847-7a08431cca2f)"
    
    # Remove duplicate entries and update primary
    result = []
    for exp in experiences:
        if exp["id"] in DUPLICATE_IDS:
            continue  # Skip duplicates
        elif exp["id"] == PRIMARY_ID:
            result.append(primary_entry)
        else:
            result.append(exp)
    
    return result


def main():
    """Main function."""
    print("=" * 80)
    print("CONSOLIDATE BPM SOFTWARE SOLUTIONS EXPERIENCE ENTRIES")
    print("=" * 80 + "\n")
    
    # Load experiences
    experiences = load_experiences()
    print(f"Loaded {len(experiences)} experience entries\n")
    
    # Consolidate
    consolidated = consolidate_bpm_entries(experiences)
    
    print(f"\nResult: {len(consolidated)} experience entries (removed {len(experiences) - len(consolidated)} duplicates)")
    
    # Save
    save_experiences(consolidated)
    print(f"✅ Saved consolidated experiences to data/experiences.json")


if __name__ == "__main__":
    main()

