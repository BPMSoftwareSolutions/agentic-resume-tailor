#!/usr/bin/env python3
"""
Test script for auto-execution feature
"""

import re
from typing import Optional


def extract_command_from_response(response: str) -> Optional[str]:
    """
    Extract command from agent response (looks for 'run:' pattern).
    
    Args:
        response: Agent response text
        
    Returns:
        Command string if found, None otherwise
    """
    pattern = r'run:\s*(.+?)(?:\n|$)'
    match = re.search(pattern, response, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


# Test cases
test_cases = [
    {
        "name": "Simple command",
        "response": "I'll update the Ford resume.\n\nrun: python src/update_resume_experience.py --resume \"Ford\" --experience \"data/job_listings/Tailored Experience Summary for Ford.md\"",
        "expected": "python src/update_resume_experience.py --resume \"Ford\" --experience \"data/job_listings/Tailored Experience Summary for Ford.md\""
    },
    {
        "name": "Command at end of response",
        "response": "Let me check your resumes.\n\nrun: cat data/resumes/index.json",
        "expected": "cat data/resumes/index.json"
    },
    {
        "name": "Command with multiple lines after",
        "response": "I'll tailor your resume.\n\nrun: python src/tailor.py --resume data/master_resume.json --jd \"data/job_listings/GM.md\" --out out/resume.html\n\nThis will create a tailored resume.",
        "expected": "python src/tailor.py --resume data/master_resume.json --jd \"data/job_listings/GM.md\" --out out/resume.html"
    },
    {
        "name": "No command",
        "response": "I understand you want to update your resume. Can you provide more details?",
        "expected": None
    },
    {
        "name": "Case insensitive",
        "response": "Sure!\n\nRUN: ls data/resumes/",
        "expected": "ls data/resumes/"
    }
]

print("Testing command extraction...")
print("=" * 60)

all_passed = True
for test in test_cases:
    result = extract_command_from_response(test["response"])
    passed = result == test["expected"]
    all_passed = all_passed and passed
    
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"\n{status}: {test['name']}")
    print(f"  Expected: {test['expected']}")
    print(f"  Got:      {result}")

print("\n" + "=" * 60)
if all_passed:
    print("✅ All tests passed!")
else:
    print("❌ Some tests failed!")

exit(0 if all_passed else 1)

