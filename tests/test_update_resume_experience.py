"""
Unit tests for update_resume_experience.py

Tests the helper script that updates resume experience from markdown files.
"""

import pytest
import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from update_resume_experience import (
    load_resume_index,
    find_resume_by_identifier,
    parse_experience_from_markdown,
    update_resume_experience
)


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary data directory with test files."""
    data_dir = tmp_path / "data"
    resumes_dir = data_dir / "resumes"
    resumes_dir.mkdir(parents=True)
    
    # Create test resume index
    index_data = {
        "resumes": [
            {
                "id": "test-resume-1",
                "name": "Sidney_Jones_Senior_Software_Engineer_Ford",
                "created_at": "2025-10-12T00:00:00",
                "updated_at": "2025-10-12T00:00:00",
                "job_listing_id": None,
                "is_master": False,
                "description": "Test Ford resume"
            },
            {
                "id": "test-resume-2",
                "name": "Sidney_Jones_Senior_Software_Engineer_GM",
                "created_at": "2025-10-12T00:00:00",
                "updated_at": "2025-10-12T00:00:00",
                "job_listing_id": None,
                "is_master": False,
                "description": "Test GM resume"
            }
        ]
    }
    
    index_file = resumes_dir / "index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2)
    
    # Create test resume file
    test_resume = {
        "name": "Sidney Jones",
        "title": "Senior Software Engineer",
        "experience": [
            {
                "employer": "Old Company",
                "role": "Old Role",
                "dates": "2020-2021",
                "location": "Old Location",
                "bullets": [
                    {"text": "Old bullet 1", "tags": []}
                ]
            }
        ]
    }
    
    resume_file = resumes_dir / "test-resume-1.json"
    with open(resume_file, 'w', encoding='utf-8') as f:
        json.dump(test_resume, f, indent=2)
    
    # Create test markdown file
    md_content = """
# Test Experience

### Edward Jones — Senior Application Architect (2021–2024)

* Led modernization of enterprise platform
* Directed cross-functional teams
* Established technical delivery governance

**Tags:** Cloud Modernization, Microservices, Leadership

---

### BPM Software Solutions — Senior Software Architect (2017–2021)

* Spearheaded cloud-first modernization initiatives
* Designed scalable distributed architectures

**Tags:** Leadership, Cloud Architecture, AWS
"""
    
    md_file = data_dir / "test_experience.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return {
        'data_dir': data_dir,
        'resumes_dir': resumes_dir,
        'index_file': index_file,
        'resume_file': resume_file,
        'md_file': md_file,
        'index_data': index_data
    }


class TestLoadResumeIndex:
    """Tests for load_resume_index function."""
    
    def test_load_existing_index(self, temp_data_dir):
        """Test loading an existing resume index."""
        index_data = load_resume_index(temp_data_dir['data_dir'])
        
        assert 'resumes' in index_data
        assert len(index_data['resumes']) == 2
        assert index_data['resumes'][0]['name'] == 'Sidney_Jones_Senior_Software_Engineer_Ford'
    
    def test_load_nonexistent_index(self, tmp_path):
        """Test error when index doesn't exist."""
        with pytest.raises(FileNotFoundError):
            load_resume_index(tmp_path)


class TestFindResumeByIdentifier:
    """Tests for find_resume_by_identifier function."""
    
    def test_find_by_company_name(self, temp_data_dir):
        """Test finding resume by company name."""
        index_data = temp_data_dir['index_data']
        
        resume = find_resume_by_identifier(index_data, "Ford")
        assert resume is not None
        assert resume['id'] == 'test-resume-1'
        assert 'Ford' in resume['name']
    
    def test_find_by_full_name(self, temp_data_dir):
        """Test finding resume by full name."""
        index_data = temp_data_dir['index_data']
        
        resume = find_resume_by_identifier(index_data, "Sidney_Jones_Senior_Software_Engineer_GM")
        assert resume is not None
        assert resume['id'] == 'test-resume-2'
    
    def test_find_case_insensitive(self, temp_data_dir):
        """Test case-insensitive search."""
        index_data = temp_data_dir['index_data']
        
        resume = find_resume_by_identifier(index_data, "ford")
        assert resume is not None
        assert resume['id'] == 'test-resume-1'
    
    def test_find_nonexistent(self, temp_data_dir):
        """Test searching for nonexistent resume."""
        index_data = temp_data_dir['index_data']
        
        resume = find_resume_by_identifier(index_data, "Nonexistent")
        assert resume is None


class TestParseExperienceFromMarkdown:
    """Tests for parse_experience_from_markdown function."""
    
    def test_parse_valid_markdown(self, temp_data_dir):
        """Test parsing valid markdown file."""
        experiences = parse_experience_from_markdown(temp_data_dir['md_file'])
        
        assert len(experiences) == 2
        
        # Check first experience
        exp1 = experiences[0]
        assert exp1['employer'] == 'Edward Jones'
        assert exp1['role'] == 'Senior Application Architect'
        assert exp1['dates'] == '2021–2024'
        assert len(exp1['bullets']) == 3
        
        # Check second experience
        exp2 = experiences[1]
        assert exp2['employer'] == 'BPM Software Solutions'
        assert exp2['role'] == 'Senior Software Architect'
        assert exp2['dates'] == '2017–2021'
        assert len(exp2['bullets']) == 2
    
    def test_parse_nonexistent_file(self, tmp_path):
        """Test error when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            parse_experience_from_markdown(tmp_path / "nonexistent.md")


class TestUpdateResumeExperience:
    """Tests for update_resume_experience function."""
    
    def test_prepend_experience(self, temp_data_dir):
        """Test prepending new experience to resume."""
        experiences = parse_experience_from_markdown(temp_data_dir['md_file'])
        
        update_resume_experience(
            temp_data_dir['data_dir'],
            'test-resume-1',
            experiences,
            replace=False
        )
        
        # Load updated resume
        with open(temp_data_dir['resume_file'], 'r', encoding='utf-8') as f:
            updated_resume = json.load(f)
        
        # Should have 3 experiences (2 new + 1 old)
        assert len(updated_resume['experience']) == 3
        assert updated_resume['experience'][0]['employer'] == 'Edward Jones'
        assert updated_resume['experience'][2]['employer'] == 'Old Company'
    
    def test_replace_experience(self, temp_data_dir):
        """Test replacing all experience in resume."""
        experiences = parse_experience_from_markdown(temp_data_dir['md_file'])
        
        update_resume_experience(
            temp_data_dir['data_dir'],
            'test-resume-1',
            experiences,
            replace=True
        )
        
        # Load updated resume
        with open(temp_data_dir['resume_file'], 'r', encoding='utf-8') as f:
            updated_resume = json.load(f)
        
        # Should have only 2 experiences (old one replaced)
        assert len(updated_resume['experience']) == 2
        assert updated_resume['experience'][0]['employer'] == 'Edward Jones'
        assert updated_resume['experience'][1]['employer'] == 'BPM Software Solutions'
    
    def test_update_timestamp(self, temp_data_dir):
        """Test that timestamp is updated in index."""
        experiences = parse_experience_from_markdown(temp_data_dir['md_file'])
        
        # Get original timestamp
        index_data = load_resume_index(temp_data_dir['data_dir'])
        original_timestamp = index_data['resumes'][0]['updated_at']
        
        # Update resume
        update_resume_experience(
            temp_data_dir['data_dir'],
            'test-resume-1',
            experiences,
            replace=False
        )
        
        # Check timestamp was updated
        updated_index = load_resume_index(temp_data_dir['data_dir'])
        new_timestamp = updated_index['resumes'][0]['updated_at']
        
        assert new_timestamp != original_timestamp
    
    def test_update_nonexistent_resume(self, temp_data_dir):
        """Test error when resume doesn't exist."""
        experiences = []
        
        with pytest.raises(FileNotFoundError):
            update_resume_experience(
                temp_data_dir['data_dir'],
                'nonexistent-id',
                experiences,
                replace=False
            )

