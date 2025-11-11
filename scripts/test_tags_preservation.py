#!/usr/bin/env python3
"""Test that tags are preserved when using surgical_resume_update.py"""

import json
from pathlib import Path

# Create a test resume with some old experiences
test_resume = {
    "name": "Test Resume",
    "title": "Software Engineer",
    "summary": "Old summary",
    "experience": [
        {
            "employer": "Old Company",
            "role": "Old Role",
            "dates": "2020-2021",
            "location": "Old City",
            "bullets": [
                {
                    "text": "Old bullet point",
                    "tags": ["OldTag1", "OldTag2"]
                }
            ]
        }
    ]
}

# Save it
resume_file = Path('data/resumes/test-tags-preservation.json')
with open(resume_file, 'w', encoding='utf-8') as f:
    json.dump(test_resume, f, indent=2, ensure_ascii=False)

# Add to index
index_file = Path('data/resumes/index.json')
with open(index_file, 'r', encoding='utf-8') as f:
    index = json.load(f)

index['resumes'].append({
    "id": "test-tags-preservation",
    "name": "Test Tags Preservation",
    "created_at": "2025-11-11T00:00:00Z",
    "updated_at": "2025-11-11T00:00:00Z",
    "job_listing_id": None,
    "is_master": False,
    "description": "Test resume for tags preservation"
})

with open(index_file, 'w', encoding='utf-8') as f:
    json.dump(index, f, indent=2, ensure_ascii=False)

print("✓ Created test resume: test-tags-preservation")

