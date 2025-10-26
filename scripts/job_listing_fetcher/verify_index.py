#!/usr/bin/env python3
"""Verify the job listings index."""

import json

index_path = "data/job_listings/index.json"

with open(index_path, "r", encoding="utf-8") as f:
    index = json.load(f)

listings = index.get("job_listings", [])
print(f"\n{'='*70}")
print(f"Job Listings Index Verification")
print(f"{'='*70}\n")

print(f"Total entries: {len(listings)}\n")

print("Latest 5 entries:")
print("-" * 70)
for i, entry in enumerate(listings[-5:], 1):
    print(f"\n{i}. {entry['title']}")
    print(f"   Company: {entry.get('company', 'N/A')}")
    print(f"   Location: {entry.get('location', 'N/A')}")
    print(f"   File: {entry.get('file', 'N/A')}")
    print(f"   ID: {entry['id']}")
    print(f"   Created: {entry.get('created_at', 'N/A')}")

print(f"\n{'='*70}\n")

