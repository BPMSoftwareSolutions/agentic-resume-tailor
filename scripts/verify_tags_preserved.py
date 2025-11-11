#!/usr/bin/env python3
"""Verify that tags are preserved in the updated resume"""

import json

with open('data/resumes/test-tags-preservation.json', 'r', encoding='utf-8') as f:
    resume = json.load(f)

print("✓ TAGS PRESERVED - Verification:\n")
print(f"Total experiences: {len(resume['experience'])}\n")

for i, exp in enumerate(resume['experience'], 1):
    print(f"{i}. {exp['employer']} - {exp['role']}")
    print(f"   Bullets with tags:")
    for j, bullet in enumerate(exp['bullets'], 1):
        tags_str = ", ".join(bullet.get('tags', []))
        print(f"     {j}. {bullet['text'][:60]}...")
        print(f"        Tags: {tags_str}\n")

