#!/usr/bin/env python3
import json

data = json.load(open('data/resumes/8630031a-5870-4c7f-a3a9-ee4cb035493e.json'))

print(f"✓ Resume Structure:")
print(f"  Total experiences: {len(data['experience'])}\n")

for i, exp in enumerate(data['experience'], 1):
    print(f"{i}. {exp.get('employer', 'N/A')} - {exp.get('role', 'N/A')}")
    print(f"   Dates: {exp.get('dates', 'N/A')}")
    print(f"   Bullets: {len(exp.get('bullets', []))}")
    if 'tags' in exp:
        print(f"   Tags: {', '.join(exp['tags'][:3])}...")
    else:
        print(f"   Tags: {[b.get('tags', []) for b in exp.get('bullets', [])][:1]}")
    print()

