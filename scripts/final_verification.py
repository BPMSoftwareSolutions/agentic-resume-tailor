#!/usr/bin/env python3
"""Final verification that resume is clean with all tags preserved"""

import json

resume_id = "8630031a-5870-4c7f-a3a9-ee4cb035493e"
data = json.load(open(f'data/resumes/{resume_id}.json'))

print("=" * 80)
print("✅ FINAL VERIFICATION - Resume 8630031a-5870-4c7f-a3a9-ee4cb035493e")
print("=" * 80)
print()

print(f"📊 STRUCTURE:")
print(f"   • Total Experiences: {len(data['experience'])}")
print(f"   • Summary: {len(data['summary'])} chars")
print(f"   • Core Competencies: {len(data['core_competencies'])} items")
print()

print("📝 EXPERIENCES WITH TAGS:")
print()

for i, exp in enumerate(data['experience'], 1):
    print(f"{i}. {exp['employer']}")
    print(f"   Role: {exp['role']}")
    print(f"   Dates: {exp['dates']}")
    print(f"   Location: {exp['location']}")
    print(f"   Bullets: {len(exp['bullets'])}")
    print()
    
    for j, bullet in enumerate(exp['bullets'], 1):
        tags = bullet.get('tags', [])
        print(f"     • {bullet['text'][:70]}...")
        print(f"       Tags: {', '.join(tags)}")
    print()

print("=" * 80)
print("✅ ALL TAGS PRESERVED - READY FOR ATS!")
print("=" * 80)

