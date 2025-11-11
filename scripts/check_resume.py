#!/usr/bin/env python3
import json
import sys

resume_id = sys.argv[1] if len(sys.argv) > 1 else "8919f18f-d46a-4cc5-807d-8a4618e80ddd"
resume_file = f'data/resumes/{resume_id}.json'

try:
    data = json.load(open(resume_file))
    
    print(f"✓ Resume: {resume_id}")
    print(f"  Name: {data.get('name', 'N/A')}")
    print(f"  Title: {data.get('title', 'N/A')}")
    print(f"  Total Experiences: {len(data.get('experience', []))}\n")
    
    for i, exp in enumerate(data.get('experience', []), 1):
        print(f"{i}. {exp.get('employer', 'N/A')} - {exp.get('role', 'N/A')}")
        print(f"   Dates: {exp.get('dates', 'N/A')}")
        print(f"   Bullets: {len(exp.get('bullets', []))}")
        
        # Check tag structure (expected: tags at EXPERIENCE level)
        has_bullet_tags = any(b.get('tags') for b in exp.get('bullets', []))
        has_exp_tags = 'tags' in exp

        if has_exp_tags and not has_bullet_tags:
            print(f"   ✓ Tags at experience level (expected)")
        elif has_exp_tags and has_bullet_tags:
            print(f"   ✓ Tags at experience level; ⓘ bullet-level tags also present")
        elif has_bullet_tags and not has_exp_tags:
            print(f"   ✗ Only bullet-level tags found (should promote to experience level)")
        else:
            print(f"   ✗ No tags found")
        print()
        
except FileNotFoundError:
    print(f"❌ Resume not found: {resume_file}")
    sys.exit(1)

