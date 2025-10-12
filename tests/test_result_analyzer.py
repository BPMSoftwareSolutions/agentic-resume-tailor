#!/usr/bin/env python3
"""
Unit tests for ResultAnalyzer module.
Related to GitHub Issue #24 - Phase 1: Auto-Verification & Result Analysis
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent.result_analyzer import ResultAnalyzer


class TestResultAnalyzer:
    """Test suite for ResultAnalyzer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = ResultAnalyzer()
    
    def test_analyze_successful_command(self):
        """Test analysis of successful command execution."""
        command = "python src/duplicate_resume.py --resume Ford --new-name Test"
        result = {
            'success': True,
            'output': '[SUCCESS] Successfully duplicated resume!\nNew Resume ID: abc-123\nNew Resume Name: Test',
            'error': ''
        }
        
        analysis = self.analyzer.analyze(command, result)
        
        assert analysis['success'] is True
        assert analysis['status'] == 'success'
        assert 'Successfully' in analysis['message']
        assert len(analysis['suggestions']) > 0
    
    def test_analyze_failed_command(self):
        """Test analysis of failed command execution."""
        command = "python src/duplicate_resume.py --resume NonExistent --new-name Test"
        result = {
            'success': False,
            'output': '',
            'error': '[ERROR] Resume not found: NonExistent'
        }
        
        analysis = self.analyzer.analyze(command, result)
        
        assert analysis['success'] is False
        assert analysis['status'] == 'error'
        assert 'failed' in analysis['message'].lower()
        assert len(analysis['suggestions']) > 0
    
    def test_extract_resume_id(self):
        """Test extraction of resume ID from output."""
        output = "Successfully created resume!\nResume ID: a04640bf-d6bb-4d7f-a949-69026acdb212"
        error = ""
        
        extracted = self.analyzer._extract_information(output, error)
        
        assert 'resume_id' in extracted
        assert extracted['resume_id'] == 'a04640bf-d6bb-4d7f-a949-69026acdb212'
    
    def test_extract_resume_name(self):
        """Test extraction of resume name from output."""
        output = "Resume Name: Sidney_Jones_Senior_Engineer_Ford\nCreated successfully"
        error = ""
        
        extracted = self.analyzer._extract_information(output, error)
        
        assert 'resume_name' in extracted
        assert 'Sidney_Jones_Senior_Engineer_Ford' in extracted['resume_name']
    
    def test_extract_count(self):
        """Test extraction of count from output."""
        output = "Found 5 resumes in the database"
        error = ""
        
        extracted = self.analyzer._extract_information(output, error)
        
        assert 'count' in extracted
        assert extracted['count'] == '5'
    
    def test_extract_file_path(self):
        """Test extraction of file path from output."""
        output = "Output: out/tailored_resume.html\nGenerated successfully"
        error = ""
        
        extracted = self.analyzer._extract_information(output, error)
        
        assert 'file_path' in extracted
        assert 'tailored_resume.html' in extracted['file_path']
    
    def test_determine_status_success(self):
        """Test status determination for successful execution."""
        output = "✅ Successfully completed the operation"
        error = ""
        
        status = self.analyzer._determine_status(output, error, True)
        
        assert status == 'success'
    
    def test_determine_status_error(self):
        """Test status determination for failed execution."""
        output = ""
        error = "❌ Error: File not found"
        
        status = self.analyzer._determine_status(output, error, False)
        
        assert status == 'error'
    
    def test_suggestions_for_duplicate_resume(self):
        """Test suggestions for duplicate resume command."""
        command = "python src/duplicate_resume.py --resume Ford --new-name Test"
        
        suggestions = self.analyzer._generate_suggestions(command, 'success', {})
        
        assert len(suggestions) > 0
        assert any('tailor' in s.lower() for s in suggestions)
    
    def test_suggestions_for_update_experience(self):
        """Test suggestions for update experience command."""
        command = "python src/update_resume_experience.py --resume Ford --experience file.md"
        
        suggestions = self.analyzer._generate_suggestions(command, 'success', {})
        
        assert len(suggestions) > 0
        assert any('review' in s.lower() or 'export' in s.lower() for s in suggestions)
    
    def test_suggestions_for_tailor(self):
        """Test suggestions for tailor command."""
        command = "python src/tailor.py --resume data/resume.json --jd job.md"
        
        suggestions = self.analyzer._generate_suggestions(command, 'success', {})
        
        assert len(suggestions) > 0
        assert any('review' in s.lower() or 'export' in s.lower() for s in suggestions)
    
    def test_suggestions_for_crud(self):
        """Test suggestions for CRUD command."""
        command = "python src/crud/technical_skills.py --resume Ford --add Python"
        
        suggestions = self.analyzer._generate_suggestions(command, 'success', {})
        
        assert len(suggestions) > 0
    
    def test_error_suggestions_not_found(self):
        """Test error suggestions for 'not found' errors."""
        command = "python src/duplicate_resume.py --resume NonExistent"
        
        suggestions = self.analyzer._generate_suggestions(command, 'error', {})
        
        assert len(suggestions) > 0
        assert any('list' in s.lower() or 'check' in s.lower() for s in suggestions)
    
    def test_format_message_with_extracted_info(self):
        """Test message formatting with extracted information."""
        extracted_info = {
            'resume_id': 'abc-123',
            'resume_name': 'Test_Resume',
            'count': '5'
        }
        
        message = self.analyzer._format_message('success', 'Operation completed', '', extracted_info)
        
        assert 'abc-123' in message
        assert 'Test_Resume' in message
        assert '5' in message
    
    def test_multiple_success_indicators(self):
        """Test detection of multiple success indicators."""
        output = "[SUCCESS] Operation completed successfully ✅"
        
        status = self.analyzer._determine_status(output, '', True)
        
        assert status == 'success'
    
    def test_multiple_error_indicators(self):
        """Test detection of multiple error indicators."""
        error = "[ERROR] Failed to execute ❌ Exception occurred"
        
        status = self.analyzer._determine_status('', error, False)
        
        assert status == 'error'

