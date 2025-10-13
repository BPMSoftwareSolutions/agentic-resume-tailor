"""
Integration tests for orchestration workflow

Tests the complete flow:
1. Parse job posting
2. Match with resume
3. Generate CRUD operations
4. Execute operations (dry run)
"""

import pytest
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from parsers.job_posting_parser import JobPostingParser
from parsers.experience_parser import ExperienceParser
from parsers.nl_command_parser import NLCommandParser
from orchestrator.resume_matcher import ResumeMatcher
from orchestrator.crud_orchestrator import CRUDOrchestrator


class TestJobPostingToOperations:
    """Test complete flow from job posting to CRUD operations"""
    
    def test_parse_and_match_workflow(self):
        """Test parsing job posting and matching with resume"""
        # Create sample job posting
        job_text = """Software Engineering Manager - job post
Tech Company
San Francisco, CA

This is a hybrid role.

What You'll Do

Lead engineering teams to build scalable systems.
Implement CI/CD pipelines and DevOps practices.
Mentor junior engineers and promote best practices.

Your Skills & Abilities (Required Qualifications)

5+ years of managerial experience in software development.
Strong experience with Python and Java.
Experience with AWS and Docker.
Excellent leadership and communication skills.
"""

        # Parse job posting
        parser = JobPostingParser()
        parser.content = job_text
        parser.lines = job_text.split('\n')

        job_data = {
            'title': parser._extract_title(),
            'company': parser._extract_company(),
            'location': parser._extract_location(),
            'work_arrangement': parser._extract_work_arrangement(),
            'required_skills': parser._extract_required_skills(),
            'responsibilities': parser._extract_responsibilities(),
            'experience_years': parser._extract_experience_years(),
            'management_experience': parser._extract_management_experience()
        }

        # Verify job data
        assert job_data['title'] == 'Software Engineering Manager'
        assert job_data['company'] == 'Tech Company'
        assert job_data['work_arrangement'] == 'hybrid'
        assert job_data['experience_years'] == 5
        
        # Create sample resume
        resume_data = {
            'basic_info': {
                'name': 'John Doe',
                'title': 'Senior Software Engineer',
                'email': 'john@example.com'
            },
            'technical_skills': {
                'languages': 'Python, JavaScript',
                'cloud': 'AWS',
                'devops': 'Docker'
            },
            'expertise': [
                'Software Development',
                'Team Leadership'
            ],
            'experience': [
                {
                    'employer': 'Previous Company',
                    'role': 'Senior Engineer',
                    'dates': '2020-2023',
                    'bullets': [
                        'Led team of 5 engineers using Python and AWS',
                        'Implemented Docker containerization',
                        'Mentored junior developers'
                    ]
                }
            ]
        }
        
        # Match resume with job
        matcher = ResumeMatcher()
        match_result = matcher.match(job_data, resume_data)
        
        # Verify match results
        assert 'score' in match_result
        assert 'matching_skills' in match_result
        assert 'missing_skills' in match_result
        assert match_result['score'] > 0
        
        # Verify some skills matched
        assert 'python' in match_result['matching_skills']
        assert 'aws' in match_result['matching_skills']
        assert 'docker' in match_result['matching_skills']
    
    def test_generate_operations_workflow(self):
        """Test generating CRUD operations from match results"""
        job_data = {
            'title': 'Engineering Manager',
            'company': 'Test Corp',
            'required_skills': ['python', 'java', 'kubernetes'],
            'responsibilities': ['Lead teams', 'Implement DevOps'],
            'compliance_requirements': ['SOX']
        }
        
        match_result = {
            'score': 60.0,
            'matching_skills': ['python'],
            'missing_skills': ['java', 'kubernetes'],
            'relevant_experience': [
                {
                    'employer': 'Previous Corp',
                    'role': 'Senior Engineer',
                    'relevance_score': 5.0,
                    'matching_bullets': []
                }
            ]
        }
        
        # Generate operations
        orchestrator = CRUDOrchestrator(dry_run=True)
        operations = orchestrator.generate_operations(job_data, match_result, "Test Resume")
        
        # Verify operations were generated
        assert len(operations) > 0
        
        # Verify operation structure
        for op in operations:
            assert 'command' in op
            assert 'description' in op
            assert 'priority' in op
            assert 'type' in op
        
        # Verify title update operation exists
        title_ops = [op for op in operations if op['type'] == 'basic_info']
        assert len(title_ops) > 0
        assert 'Engineering Manager' in title_ops[0]['command']
        
        # Verify skill addition operations exist
        skill_ops = [op for op in operations if op['type'] == 'technical_skills']
        assert len(skill_ops) > 0
    
    def test_execute_operations_dry_run(self):
        """Test executing operations in dry run mode"""
        operations = [
            {
                'command': 'python src/crud/basic_info.py --resume "Test" --update-title "Manager"',
                'description': 'Update title',
                'priority': 1,
                'type': 'basic_info'
            },
            {
                'command': 'python src/crud/technical_skills.py --resume "Test" --append-to-category "languages" "Python"',
                'description': 'Add Python skill',
                'priority': 2,
                'type': 'technical_skills'
            },
            {
                'command': '# Manual: Update summary',
                'description': 'Update summary',
                'priority': 3,
                'type': 'summary',
                'manual': True
            }
        ]
        
        orchestrator = CRUDOrchestrator(dry_run=True)
        results = orchestrator.execute_operations(operations)
        
        # Verify results structure
        assert 'total' in results
        assert 'successful' in results
        assert 'failed' in results
        assert 'skipped' in results
        assert 'results' in results
        
        # Verify counts
        assert results['total'] == 3
        assert results['successful'] == 2  # 2 automated operations
        assert results['skipped'] == 1  # 1 manual operation
        assert results['failed'] == 0


class TestExperienceParserIntegration:
    """Test experience parser integration"""
    
    def test_parse_and_format_experience(self):
        """Test parsing experience and formatting for CRUD"""
        text = """
### **Company A - Senior Engineer (2020-2023)**

* Led development of microservices platform
* Implemented CI/CD pipelines
* Mentored team of 5 engineers

**Tags:** Leadership, Microservices, CI/CD

### **Company B - Software Engineer (2018-2020)**

* Developed REST APIs using Python
* Deployed applications to AWS

**Tags:** Python, AWS, REST
"""
        
        parser = ExperienceParser()
        experiences = parser.parse_text(text)
        
        # Verify parsing
        assert len(experiences) == 2
        assert experiences[0]['employer'] == 'Company A'
        assert experiences[0]['role'] == 'Senior Engineer'
        assert len(experiences[0]['bullets']) == 3
        assert len(experiences[0]['tags']) == 3
        
        # Test formatting for CRUD
        formatted = parser.format_for_crud(experiences)
        assert 'Company A' in formatted
        assert 'Senior Engineer' in formatted
        assert '2020-2023' in formatted


class TestNLCommandParserIntegration:
    """Test natural language command parser integration"""
    
    def test_parse_multiple_commands(self):
        """Test parsing various natural language commands"""
        parser = NLCommandParser()
        
        commands = [
            "Add Python and Java to my technical skills",
            "Update my title to Senior Architect",
            "List my certifications",
            "Duplicate the Ford resume as GM Resume"
        ]
        
        for cmd in commands:
            result = parser.parse(cmd, default_resume="Master Resume")
            
            # Verify all commands parse successfully
            assert result['intent'] != 'unknown'
            assert result['entity'] != 'unknown'
            assert result['command'] is not None
            assert len(result['command']) > 0


class TestSkillCategorization:
    """Test skill categorization in orchestrator"""
    
    def test_categorize_technical_skills(self):
        """Test categorizing skills into appropriate categories"""
        orchestrator = CRUDOrchestrator()

        skills = ['python', 'java', 'aws', 'azure', 'docker', 'kubernetes', 'sql', 'mongodb', 'zuora']
        categories = orchestrator._categorize_skills(skills)

        # Verify categorization
        assert 'languages' in categories
        assert 'python' in categories['languages']
        assert 'java' in categories['languages']

        assert 'cloud' in categories
        assert 'aws' in categories['cloud']
        assert 'azure' in categories['cloud']

        assert 'devops' in categories
        assert 'docker' in categories['devops']
        assert 'kubernetes' in categories['devops']

        assert 'databases' in categories
        assert 'sql' in categories['databases'] or 'mongodb' in categories['databases']

        assert 'billing' in categories
        assert 'zuora' in categories['billing']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

