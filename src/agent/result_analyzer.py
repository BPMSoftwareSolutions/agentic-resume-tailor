#!/usr/bin/env python3
"""
Result Analyzer - Intelligent analysis of command execution results.
Related to GitHub Issue #24 - Phase 1: Auto-Verification & Result Analysis

This module provides:
- Automatic parsing of command outputs for success/failure indicators
- Extraction of key information (IDs, names, counts, paths)
- Data integrity verification
- Intelligent next-step suggestions
- Error analysis and fix recommendations
"""

import re
from typing import Dict, Any, List, Optional, Tuple


class ResultAnalyzer:
    """Analyzes command execution results and provides intelligent feedback."""
    
    # Success indicators
    SUCCESS_PATTERNS = [
        r'\[SUCCESS\]',
        r'✅',
        r'Successfully',
        r'completed successfully',
        r'created successfully',
        r'updated successfully',
        r'deleted successfully',
    ]
    
    # Error indicators
    ERROR_PATTERNS = [
        r'\[ERROR\]',
        r'❌',
        r'Error:',
        r'Failed',
        r'Exception:',
        r'Traceback',
        r'not found',
        r'does not exist',
    ]
    
    # Information extraction patterns
    INFO_PATTERNS = {
        'resume_id': r'(?:Resume ID|ID|resume_id):\s*([a-f0-9\-]{36})',
        'resume_name': r'(?:Resume Name|Name|resume_name):\s*(.+?)(?:\n|$)',
        'count': r'(?:Found|Created|Updated|Deleted)\s+(\d+)\s+(?:resume|item|entry|entries)',
        'file_path': r'(?:File|Path|Output):\s*([^\n]+\.(?:json|html|pdf|docx|md))',
    }
    
    def __init__(self):
        """Initialize the result analyzer."""
        pass
    
    def analyze(self, command: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze command execution result.
        
        Args:
            command: The command that was executed
            result: Execution result dictionary with 'success', 'output', 'error' keys
            
        Returns:
            Analysis dictionary with:
                - success: bool
                - status: 'success' | 'error' | 'warning'
                - message: formatted message
                - extracted_info: dict of extracted information
                - suggestions: list of next-step suggestions
        """
        output = result.get('output', '')
        error = result.get('error', '')
        success = result.get('success', False)
        
        # Determine actual status by analyzing output
        actual_status = self._determine_status(output, error, success)
        
        # Extract key information
        extracted_info = self._extract_information(output, error)
        
        # Generate formatted message
        message = self._format_message(actual_status, output, error, extracted_info)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(command, actual_status, extracted_info)
        
        return {
            'success': actual_status == 'success',
            'status': actual_status,
            'message': message,
            'extracted_info': extracted_info,
            'suggestions': suggestions
        }
    
    def _determine_status(self, output: str, error: str, return_code_success: bool) -> str:
        """
        Determine the actual status of the command execution.
        
        Args:
            output: Standard output
            error: Standard error
            return_code_success: Whether return code was 0
            
        Returns:
            Status string: 'success', 'error', or 'warning'
        """
        combined = output + error
        
        # Check for explicit error indicators
        for pattern in self.ERROR_PATTERNS:
            if re.search(pattern, combined, re.IGNORECASE):
                return 'error'
        
        # Check for explicit success indicators
        for pattern in self.SUCCESS_PATTERNS:
            if re.search(pattern, combined, re.IGNORECASE):
                return 'success'
        
        # Fall back to return code
        if return_code_success:
            return 'success'
        else:
            return 'error'
    
    def _extract_information(self, output: str, error: str) -> Dict[str, Any]:
        """
        Extract key information from command output.
        
        Args:
            output: Standard output
            error: Standard error
            
        Returns:
            Dictionary of extracted information
        """
        combined = output + error
        extracted = {}
        
        for key, pattern in self.INFO_PATTERNS.items():
            match = re.search(pattern, combined, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                extracted[key] = value
        
        # Extract counts from various formats
        count_matches = re.findall(r'(\d+)\s+(?:resume|item|entry|entries|file)', combined, re.IGNORECASE)
        if count_matches:
            extracted['counts'] = [int(c) for c in count_matches]
        
        return extracted
    
    def _format_message(self, status: str, output: str, error: str, 
                       extracted_info: Dict[str, Any]) -> str:
        """
        Format a user-friendly message based on the analysis.
        
        Args:
            status: Status string ('success', 'error', 'warning')
            output: Standard output
            error: Standard error
            extracted_info: Extracted information dictionary
            
        Returns:
            Formatted message string
        """
        if status == 'success':
            message = "✅ Command executed successfully\n\n"
            
            # Add extracted information
            if extracted_info:
                message += self._format_extracted_info(extracted_info)
            
            # Add relevant output (first 500 chars)
            if output:
                clean_output = output.strip()[:500]
                if clean_output:
                    message += f"\n{clean_output}"
        
        elif status == 'error':
            message = "❌ Command failed\n\n"
            
            # Add error details
            if error:
                clean_error = error.strip()[:500]
                message += f"[ERROR] {clean_error}\n"
            elif output:
                clean_output = output.strip()[:500]
                message += f"{clean_output}\n"
        
        else:  # warning
            message = "⚠️  Command completed with warnings\n\n"
            if output:
                message += output.strip()[:500]
        
        return message
    
    def _format_extracted_info(self, extracted_info: Dict[str, Any]) -> str:
        """
        Format extracted information for display.
        
        Args:
            extracted_info: Dictionary of extracted information
            
        Returns:
            Formatted string
        """
        lines = []
        
        if 'resume_id' in extracted_info:
            lines.append(f"[INFO]    New Resume ID: {extracted_info['resume_id']}")
        
        if 'resume_name' in extracted_info:
            lines.append(f"[INFO]    New Resume Name: {extracted_info['resume_name']}")
        
        if 'count' in extracted_info:
            lines.append(f"[INFO]    Count: {extracted_info['count']}")
        
        if 'file_path' in extracted_info:
            lines.append(f"[INFO]    File: {extracted_info['file_path']}")
        
        if 'counts' in extracted_info and extracted_info['counts']:
            lines.append(f"[INFO]    Items processed: {', '.join(map(str, extracted_info['counts']))}")
        
        return '\n'.join(lines) if lines else ''
    
    def _generate_suggestions(self, command: str, status: str, 
                             extracted_info: Dict[str, Any]) -> List[str]:
        """
        Generate intelligent next-step suggestions.
        
        Args:
            command: The command that was executed
            status: Status string ('success', 'error', 'warning')
            extracted_info: Extracted information dictionary
            
        Returns:
            List of suggestion strings
        """
        suggestions = []
        
        if status == 'success':
            # Suggest next steps based on command type
            if 'duplicate_resume.py' in command:
                suggestions = [
                    "Update specific sections (experience, skills, summary)",
                    "Tailor it to a job posting",
                    "List all your resumes",
                    "Export to PDF or DOCX"
                ]
            
            elif 'update_resume_experience.py' in command:
                suggestions = [
                    "Review the updated resume",
                    "Export to DOCX or PDF",
                    "Update other sections (skills, summary)",
                    "List all resumes"
                ]
            
            elif 'tailor.py' in command:
                suggestions = [
                    "Review the tailored resume",
                    "Export to PDF",
                    "Make additional customizations",
                    "Create another tailored version"
                ]
            
            elif 'crud/' in command:
                suggestions = [
                    "Review the changes",
                    "Update other sections",
                    "Export the resume",
                    "List all resumes"
                ]
            
            else:
                suggestions = [
                    "Review the output",
                    "Run related commands",
                    "Check the results"
                ]
        
        elif status == 'error':
            # Suggest fixes based on error type
            if 'not found' in command.lower() or 'does not exist' in command.lower():
                suggestions = [
                    "List all available resumes: python src/crud/list_resumes.py",
                    "Check the resume name spelling",
                    "Use the resume UUID instead of name"
                ]
            else:
                suggestions = [
                    "Check the command syntax",
                    "Verify input file paths exist",
                    "Review error message for details",
                    "Try with different parameters"
                ]
        
        return suggestions

