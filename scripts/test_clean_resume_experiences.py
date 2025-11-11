#!/usr/bin/env python3
"""
Unit tests for clean_resume_experiences.py

Tests that the cleanup script:
1. Keeps only the first 3 experiences
2. Preserves all tags in those experiences
3. Removes duplicate/old experiences
4. Handles edge cases (< 3 experiences, > 3 experiences)
"""

import json
import tempfile
from pathlib import Path
import sys

def create_test_resume_with_duplicates():
    """Create a test resume with duplicate experiences (like the real problem)."""
    return {
        "name": "Test User",
        "title": "Software Engineer",
        "summary": "Test summary",
        "experience": [
            # First 3 - the clean ones with proper tags
            {
                "employer": "Company A",
                "role": "Senior Engineer",
                "dates": "2021-2024",
                "location": "City A",
                "bullets": [
                    {
                        "text": "Built microservices",
                        "tags": ["Go", "Python", "AWS"]
                    }
                ]
            },
            {
                "employer": "Company B",
                "role": "Architect",
                "dates": "2019-2021",
                "location": "City B",
                "bullets": [
                    {
                        "text": "Designed systems",
                        "tags": ["Kubernetes", "Docker"]
                    }
                ]
            },
            {
                "employer": "Company C",
                "role": "Lead",
                "dates": "2017-2019",
                "location": "City C",
                "bullets": [
                    {
                        "text": "Led team",
                        "tags": ["Leadership", "Mentorship"]
                    }
                ]
            },
            # Next 3 - old duplicates that should be removed
            {
                "employer": "Old Company",
                "role": "Old Role",
                "dates": "2024-2025",
                "location": "Old City",
                "bullets": [
                    {"text": "Old bullet"}
                ],
                "tags": ["OldTag1", "OldTag2"]  # Wrong structure - tags at experience level
            },
            {
                "employer": "Company A",  # Duplicate!
                "role": "Old Role",
                "dates": "2020-2021",
                "location": "City A",
                "bullets": [
                    {"text": "Old work"}
                ],
                "tags": ["OldTech"]
            },
            {
                "employer": "Company B",  # Duplicate!
                "role": "Old Role",
                "dates": "2018-2019",
                "location": "City B",
                "bullets": [
                    {"text": "Old work"}
                ],
                "tags": ["OldTech"]
            }
        ]
    }


def test_cleanup_removes_duplicates():
    """Test that cleanup removes duplicate experiences."""
    print("\n" + "="*70)
    print("TEST 1: Cleanup removes duplicates")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        resume_file = Path(tmpdir) / "test_resume.json"
        
        # Create test resume with 6 experiences
        test_data = create_test_resume_with_duplicates()
        with open(resume_file, 'w') as f:
            json.dump(test_data, f)
        
        print(f"✓ Created test resume with {len(test_data['experience'])} experiences")
        
        # Run cleanup
        from clean_resume_experiences import clean_resume
        clean_resume(resume_file)
        
        # Verify
        with open(resume_file, 'r') as f:
            cleaned = json.load(f)
        
        assert len(cleaned['experience']) == 3, f"Expected 3 experiences, got {len(cleaned['experience'])}"
        print(f"✓ Cleanup reduced to {len(cleaned['experience'])} experiences")
        
        # Verify the right ones were kept
        employers = [exp['employer'] for exp in cleaned['experience']]
        assert employers == ["Company A", "Company B", "Company C"], f"Wrong employers kept: {employers}"
        print(f"✓ Correct experiences kept: {employers}")
        
        print("✅ TEST PASSED\n")


def test_tags_preserved():
    """Test that tags are preserved in the first 3 experiences."""
    print("="*70)
    print("TEST 2: Tags are preserved")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        resume_file = Path(tmpdir) / "test_resume.json"
        
        # Create test resume
        test_data = create_test_resume_with_duplicates()
        with open(resume_file, 'w') as f:
            json.dump(test_data, f)
        
        # Run cleanup
        from clean_resume_experiences import clean_resume
        clean_resume(resume_file)
        
        # Verify tags
        with open(resume_file, 'r') as f:
            cleaned = json.load(f)
        
        # Check first experience tags
        exp1_tags = cleaned['experience'][0]['bullets'][0]['tags']
        assert exp1_tags == ["Go", "Python", "AWS"], f"Wrong tags for exp1: {exp1_tags}"
        print(f"✓ Experience 1 tags preserved: {exp1_tags}")
        
        exp2_tags = cleaned['experience'][1]['bullets'][0]['tags']
        assert exp2_tags == ["Kubernetes", "Docker"], f"Wrong tags for exp2: {exp2_tags}"
        print(f"✓ Experience 2 tags preserved: {exp2_tags}")
        
        exp3_tags = cleaned['experience'][2]['bullets'][0]['tags']
        assert exp3_tags == ["Leadership", "Mentorship"], f"Wrong tags for exp3: {exp3_tags}"
        print(f"✓ Experience 3 tags preserved: {exp3_tags}")
        
        print("✅ TEST PASSED\n")


def test_fewer_than_3_experiences():
    """Test cleanup with fewer than 3 experiences."""
    print("="*70)
    print("TEST 3: Fewer than 3 experiences")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        resume_file = Path(tmpdir) / "test_resume.json"
        
        # Create test resume with only 2 experiences
        test_data = {
            "name": "Test User",
            "title": "Engineer",
            "summary": "Test",
            "experience": [
                {
                    "employer": "Company A",
                    "role": "Role A",
                    "dates": "2021-2024",
                    "location": "City A",
                    "bullets": [{"text": "Work", "tags": ["Tag1"]}]
                },
                {
                    "employer": "Company B",
                    "role": "Role B",
                    "dates": "2019-2021",
                    "location": "City B",
                    "bullets": [{"text": "Work", "tags": ["Tag2"]}]
                }
            ]
        }
        
        with open(resume_file, 'w') as f:
            json.dump(test_data, f)
        
        print(f"✓ Created test resume with {len(test_data['experience'])} experiences")
        
        # Run cleanup
        from clean_resume_experiences import clean_resume
        clean_resume(resume_file)
        
        # Verify - should keep all 2
        with open(resume_file, 'r') as f:
            cleaned = json.load(f)
        
        assert len(cleaned['experience']) == 2, f"Expected 2 experiences, got {len(cleaned['experience'])}"
        print(f"✓ Kept all {len(cleaned['experience'])} experiences (< 3)")
        
        print("✅ TEST PASSED\n")


def test_more_than_3_experiences():
    """Test cleanup with more than 3 experiences."""
    print("="*70)
    print("TEST 4: More than 3 experiences")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        resume_file = Path(tmpdir) / "test_resume.json"
        
        # Create test resume with 5 experiences
        test_data = {
            "name": "Test User",
            "title": "Engineer",
            "summary": "Test",
            "experience": [
                {
                    "employer": f"Company {i}",
                    "role": f"Role {i}",
                    "dates": f"202{i}-202{i+1}",
                    "location": f"City {i}",
                    "bullets": [{"text": f"Work {i}", "tags": [f"Tag{i}"]}]
                }
                for i in range(5)
            ]
        }
        
        with open(resume_file, 'w') as f:
            json.dump(test_data, f)
        
        print(f"✓ Created test resume with {len(test_data['experience'])} experiences")
        
        # Run cleanup
        from clean_resume_experiences import clean_resume
        clean_resume(resume_file)
        
        # Verify - should keep only first 3
        with open(resume_file, 'r') as f:
            cleaned = json.load(f)
        
        assert len(cleaned['experience']) == 3, f"Expected 3 experiences, got {len(cleaned['experience'])}"
        print(f"✓ Reduced to {len(cleaned['experience'])} experiences (kept first 3 of 5)")
        
        employers = [exp['employer'] for exp in cleaned['experience']]
        assert employers == ["Company 0", "Company 1", "Company 2"], f"Wrong employers: {employers}"
        print(f"✓ Correct experiences kept: {employers}")
        
        print("✅ TEST PASSED\n")


if __name__ == "__main__":
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  UNIT TESTS: clean_resume_experiences.py".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        test_cleanup_removes_duplicates()
        test_tags_preserved()
        test_fewer_than_3_experiences()
        test_more_than_3_experiences()
        
        print("="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

