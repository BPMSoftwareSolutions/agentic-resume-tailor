#!/usr/bin/env python3
"""
Test BPM consolidation by regenerating resume from experience log.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.build_resume_from_experience_log import build_resume_from_experience_log


def main():
    print("=" * 80)
    print("TEST BPM CONSOLIDATION")
    print("=" * 80 + "\n")
    
    print("Regenerating resume from experience log...")
    resume = build_resume_from_experience_log()
    
    # Find BPM entries
    bpm_entries = [e for e in resume['experience'] if e['employer'] == 'BPM Software Solutions']
    
    print(f"BPM entries in generated resume: {len(bpm_entries)}\n")
    
    if len(bpm_entries) == 1:
        print("✅ SUCCESS: BPM appears only once")
        entry = bpm_entries[0]
        print(f"   Role: {entry['role']}")
        print(f"   Dates: {entry['dates']}")
        print(f"   Location: {entry['location']}")
        print(f"   Bullets: {len(entry['bullets'])}")
        print(f"   Skills: {len(entry['skills'])}")
        print(f"   Technologies: {len(entry['technologies'])}")
        return 0
    else:
        print(f"❌ FAILED: BPM appears {len(bpm_entries)} times")
        for i, entry in enumerate(bpm_entries):
            print(f"   {i+1}. {entry['role']} ({len(entry['bullets'])} bullets)")
        return 1


if __name__ == "__main__":
    exit(main())

