"""
Unit tests for parser modules

Tests for:
- JobPostingParser
- ExperienceParser
- NLCommandParser
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from parsers.job_posting_parser import JobPostingParser
from parsers.experience_parser import ExperienceParser
from parsers.nl_command_parser import NLCommandParser


class TestJobPostingParser:
    """Tests for JobPostingParser"""
    
    def test_parse_title(self):
        """Test extracting job title"""
        parser = JobPostingParser()
        parser.content = "Software Engineering Manager - job post\nGeneral Motors"
        parser.lines = parser.content.split('\n')
        
        title = parser._extract_title()
        assert title == "Software Engineering Manager"
    
    def test_parse_company(self):
        """Test extracting company name"""
        parser = JobPostingParser()
        parser.content = "Job Title\nGeneral Motors\n4.0\nWarren, MI"
        parser.lines = parser.content.split('\n')
        
        company = parser._extract_company()
        assert company == "General Motors"
    
    def test_parse_location(self):
        """Test extracting location"""
        parser = JobPostingParser()
        parser.content = "Job Title\nCompany\nWarren, MI\nFull-time"
        parser.lines = parser.content.split('\n')
        
        location = parser._extract_location()
        assert location == "Warren, MI"
    
    def test_parse_work_arrangement(self):
        """Test extracting work arrangement"""
        parser = JobPostingParser()
        parser.content = "This is a hybrid role requiring 3 days in office"
        parser.lines = parser.content.split('\n')
        
        arrangement = parser._extract_work_arrangement()
        assert arrangement == "hybrid"
    
    def test_parse_required_skills(self):
        """Test extracting required skills"""
        parser = JobPostingParser()
        parser.content = """
        Required Qualifications:
        - Experience with Python and Java
        - Knowledge of AWS and Azure
        - Proficiency in Docker and Kubernetes
        """
        parser.lines = parser.content.split('\n')
        
        skills = parser._extract_required_skills()
        assert 'python' in skills
        assert 'java' in skills
        assert 'aws' in skills
        assert 'azure' in skills
        assert 'docker' in skills
        assert 'kubernetes' in skills
    
    def test_parse_experience_years(self):
        """Test extracting years of experience"""
        parser = JobPostingParser()
        parser.content = "5+ years of managerial experience required"
        parser.lines = parser.content.split('\n')
        
        years = parser._extract_experience_years()
        assert years == 5
    
    def test_parse_management_experience(self):
        """Test extracting management experience"""
        parser = JobPostingParser()
        parser.content = "3+ years of managerial experience in software development"
        parser.lines = parser.content.split('\n')
        
        years = parser._extract_management_experience()
        assert years == 3
    
    def test_parse_soft_skills(self):
        """Test extracting soft skills"""
        parser = JobPostingParser()
        parser.content = """
        We're looking for someone with strong leadership and communication skills.
        Mentorship and stakeholder management experience is required.
        """
        parser.lines = parser.content.split('\n')
        
        skills = parser._extract_soft_skills()
        assert 'leadership' in skills
        assert 'communication' in skills
        assert 'mentorship' in skills
        assert 'stakeholder management' in skills
    
    def test_parse_compliance_requirements(self):
        """Test extracting compliance requirements"""
        parser = JobPostingParser()
        parser.content = "Experience with SOX compliance and audit processes required"
        parser.lines = parser.content.split('\n')
        
        compliance = parser._extract_compliance_requirements()
        assert 'SOX' in compliance
        assert 'audit' in compliance
        assert 'compliance' in compliance


class TestExperienceParser:
    """Tests for ExperienceParser"""
    
    def test_parse_experience_entry(self):
        """Test parsing a single experience entry"""
        parser = ExperienceParser()
        text = """
### **Edward Jones - Senior Application Architect (2021-2024)**

* Led modernization of enterprise platform
* Directed cross-functional teams
* Established technical delivery governance

**Tags:** Cloud Modernization, Microservices, Leadership
"""
        experiences = parser.parse_text(text)
        
        assert len(experiences) == 1
        exp = experiences[0]
        assert exp['employer'] == 'Edward Jones'
        assert exp['role'] == 'Senior Application Architect'
        assert exp['dates'] == '2021-2024'
        assert len(exp['bullets']) == 3
        assert len(exp['tags']) == 3
        assert 'Cloud Modernization' in exp['tags']
    
    def test_parse_multiple_experiences(self):
        """Test parsing multiple experience entries"""
        parser = ExperienceParser()
        text = """
### **Company A - Role A (2020-2023)**

* Bullet 1
* Bullet 2

**Tags:** Tag1, Tag2

### **Company B - Role B (2018-2020)**

* Bullet 3
* Bullet 4

**Tags:** Tag3, Tag4
"""
        experiences = parser.parse_text(text)
        
        assert len(experiences) == 2
        assert experiences[0]['employer'] == 'Company A'
        assert experiences[1]['employer'] == 'Company B'
    
    def test_parse_experience_with_location(self):
        """Test parsing experience with location in role"""
        parser = ExperienceParser()
        text = """
### **Company - Senior Engineer / Remote (2020-2023)**

* Bullet 1

**Tags:** Tag1
"""
        experiences = parser.parse_text(text)
        
        assert len(experiences) == 1
        assert experiences[0]['role'] == 'Senior Engineer'


class TestNLCommandParser:
    """Tests for NLCommandParser"""
    
    def test_identify_add_intent(self):
        """Test identifying 'add' intent"""
        parser = NLCommandParser()
        result = parser.parse("Add Python to my technical skills")
        
        assert result['intent'] == 'add'
    
    def test_identify_update_intent(self):
        """Test identifying 'update' intent"""
        parser = NLCommandParser()
        result = parser.parse("Update my title to Principal Architect")
        
        assert result['intent'] == 'update'
    
    def test_identify_list_intent(self):
        """Test identifying 'list' intent"""
        parser = NLCommandParser()
        result = parser.parse("List my certifications")
        
        assert result['intent'] == 'list'
    
    def test_identify_duplicate_intent(self):
        """Test identifying 'duplicate' intent"""
        parser = NLCommandParser()
        result = parser.parse("Duplicate the Ford resume")
        
        assert result['intent'] == 'duplicate'
    
    def test_identify_technical_skills_entity(self):
        """Test identifying technical_skills entity"""
        parser = NLCommandParser()
        result = parser.parse("Add Python to my technical skills")
        
        assert result['entity'] == 'technical_skills'
    
    def test_identify_expertise_entity(self):
        """Test identifying expertise entity"""
        parser = NLCommandParser()
        result = parser.parse("Add AI/ML Engineering to my expertise")
        
        assert result['entity'] == 'expertise'
    
    def test_identify_certification_entity(self):
        """Test identifying certification entity"""
        parser = NLCommandParser()
        result = parser.parse("List my certifications")
        
        assert result['entity'] == 'certification'
    
    def test_identify_summary_entity(self):
        """Test identifying summary entity"""
        parser = NLCommandParser()
        result = parser.parse("Show my summary")
        
        assert result['entity'] == 'summary'
    
    def test_extract_skill_params(self):
        """Test extracting skill parameters"""
        parser = NLCommandParser()
        result = parser.parse("Add Python to my technical skills")
        
        assert 'skills' in result['parameters']
        assert 'python' in result['parameters']['skills']
    
    def test_extract_multiple_skills(self):
        """Test extracting multiple skills"""
        parser = NLCommandParser()
        result = parser.parse("Add Python and Stripe to my technical skills")
        
        assert 'skills' in result['parameters']
        assert 'python' in result['parameters']['skills']
        assert 'stripe' in result['parameters']['skills']
    
    def test_extract_title_params(self):
        """Test extracting title parameters"""
        parser = NLCommandParser()
        result = parser.parse("Update my title to Principal Architect")
        
        assert result['parameters']['field'] == 'title'
        assert result['parameters']['value'] == 'principal architect'
    
    def test_generate_technical_skills_command(self):
        """Test generating technical skills CRUD command"""
        parser = NLCommandParser()
        result = parser.parse("Add Python to my technical skills", default_resume="Master Resume")
        
        assert 'python src/crud/technical_skills.py' in result['command']
        assert '--append-to-category' in result['command']
    
    def test_generate_list_command(self):
        """Test generating list CRUD command"""
        parser = NLCommandParser()
        result = parser.parse("List my certifications", default_resume="Master Resume")
        
        assert 'python src/crud/certifications.py' in result['command']
        assert '--list' in result['command']
    
    def test_generate_duplicate_command(self):
        """Test generating duplicate resume command"""
        parser = NLCommandParser()
        result = parser.parse("Duplicate the Ford resume as GM_Resume")
        
        assert 'python src/duplicate_resume.py' in result['command']
        assert 'ford' in result['command'].lower()
        assert 'gm_resume' in result['command'].lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

