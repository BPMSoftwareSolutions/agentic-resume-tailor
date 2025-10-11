"""
Comprehensive test suite runner for document quality validation.
This module runs all document quality tests and provides a summary report.
"""
import sys
from pathlib import Path
import tempfile
import os
import unittest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from tests.test_export_docx import TestMdToDocx
from tests.test_docx_structure_validation import TestDocxStructureValidation
from tests.test_visual_formatting_validation import TestVisualFormattingValidation
from tests.test_content_accuracy_validation import TestContentAccuracyValidation
from tests.test_document_quality_regression import TestDocumentQualityRegression
from tests.test_visual_appearance_validation import TestVisualAppearanceValidation


class DocumentQualityTestSuite:
    """Comprehensive test suite for document quality validation."""
    
    @staticmethod
    def run_all_tests():
        """Run all document quality tests and return results."""
        # Create test suite
        suite = unittest.TestSuite()
        
        # Add all test classes
        test_classes = [
            TestMdToDocx,
            TestDocxStructureValidation,
            TestVisualFormattingValidation,
            TestContentAccuracyValidation,
            TestDocumentQualityRegression,
            TestVisualAppearanceValidation
        ]
        
        for test_class in test_classes:
            tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
            suite.addTests(tests)
        
        # Run tests with detailed results
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        return result
    
    @staticmethod
    def generate_quality_report():
        """Generate a comprehensive quality report."""
        print("="*80)
        print("DOCUMENT QUALITY VALIDATION REPORT")
        print("="*80)
        
        result = DocumentQualityTestSuite.run_all_tests()
        
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        
        total_tests = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)
        skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
        passed = total_tests - failures - errors - skipped
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed}")
        print(f"Failed: {failures}")
        print(f"Errors: {errors}")
        print(f"Skipped: {skipped}")
        
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        print("\nTEST CATEGORIES:")
        print("- Basic functionality (export_docx)")
        print("- Document structure validation")
        print("- Visual formatting validation")
        print("- Content accuracy validation")
        print("- Quality regression prevention")
        print("- Visual appearance validation")
        
        if failures > 0:
            print(f"\n⚠️  FAILURES DETECTED ({failures}):")
            for test, traceback in result.failures:
                print(f"  - {test}")
        
        if errors > 0:
            print(f"\n❌ ERRORS DETECTED ({errors}):")
            for test, traceback in result.errors:
                print(f"  - {test}")
        
        if failures == 0 and errors == 0:
            print("\n✅ ALL TESTS PASSED - Document quality is acceptable")
        else:
            print(f"\n❌ QUALITY ISSUES DETECTED - {failures + errors} tests failed")
            print("   Fix these issues to ensure professional document appearance")
        
        return result


if __name__ == '__main__':
    DocumentQualityTestSuite.generate_quality_report()