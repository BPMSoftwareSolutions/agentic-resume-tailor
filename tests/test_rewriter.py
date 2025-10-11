"""Unit tests for rewriter.py - STAR-style bullet rewriting."""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import unittest
from rewriter import rewrite_star


class TestRewriteStar(unittest.TestCase):
    """Test the rewrite_star function."""
    
    def test_adds_period_if_missing(self):
        """Should add period at end if missing."""
        result = rewrite_star("Built CI/CD pipeline")
        self.assertTrue(result.endswith('.'))
    
    def test_preserves_existing_period(self):
        """Should not add extra period if already present."""
        result = rewrite_star("Built CI/CD pipeline.")
        self.assertEqual(result.count('.'), 1)
    
    def test_strips_whitespace(self):
        """Should strip leading/trailing whitespace."""
        result = rewrite_star("  Built pipeline  ")
        self.assertFalse(result.startswith(' '))
        self.assertTrue(result.endswith('.'))
    
    def test_no_generic_text_with_percentage(self):
        """Should not add generic text when bullet has percentage."""
        text = "Improved deployment frequency by 50%"
        result = rewrite_star(text)
        
        self.assertNotIn("improved reliability and delivery speed", result)
        self.assertIn("50%", result)
    
    def test_no_generic_text_with_reduced(self):
        """Should not add generic text when bullet has 'reduced'."""
        text = "Reduced deployment time significantly"
        result = rewrite_star(text)
        
        self.assertNotIn("improved reliability and delivery speed", result)
        self.assertIn("Reduced", result)
    
    def test_no_generic_text_with_improved(self):
        """Should not add generic text when bullet has 'improved'."""
        text = "Improved system performance"
        result = rewrite_star(text)

        # Should not add the generic "improved reliability" text
        # The word "Improved" at start gets preserved (case-sensitive in output)
        self.assertIn("Improved", result)
        self.assertNotIn("improved reliability and delivery speed", result)
    
    def test_no_generic_text_with_increased(self):
        """Should not add generic text when bullet has 'increased'."""
        text = "Increased team productivity"
        result = rewrite_star(text)
        
        self.assertNotIn("improved reliability and delivery speed", result)
        self.assertIn("Increased", result)
    
    def test_no_generic_text_with_accelerated(self):
        """Should not add generic text when bullet has 'accelerated'."""
        text = "Accelerated delivery cycles"
        result = rewrite_star(text)
        
        self.assertNotIn("improved reliability and delivery speed", result)
        self.assertIn("Accelerated", result)
    
    def test_no_generic_text_with_cut(self):
        """Should not add generic text when bullet has 'cut'."""
        text = "Cut setup time from days to hours"
        result = rewrite_star(text)
        
        self.assertNotIn("improved reliability and delivery speed", result)
        self.assertIn("Cut", result)
    
    def test_no_generic_text_with_enabling(self):
        """Should not add generic text when bullet has 'enabling'."""
        text = "Built pipeline enabling faster releases"
        result = rewrite_star(text)
        
        self.assertNotIn("improved reliability and delivery speed", result)
        self.assertIn("enabling", result)
    
    def test_no_generic_text_with_multiplier(self):
        """Should not add generic text when bullet has multiplier like '2x'."""
        text = "Made deployments 3x faster"
        result = rewrite_star(text)
        
        self.assertNotIn("improved reliability and delivery speed", result)
        self.assertIn("3x", result)
    
    def test_no_generic_text_with_time_range(self):
        """Should not add generic text when bullet has time mentions."""
        text = "Completed migration in 3 months"
        result = rewrite_star(text)
        
        self.assertNotIn("improved reliability and delivery speed", result)
        self.assertIn("3 months", result)
    
    def test_no_generic_text_with_from_to(self):
        """Should not add generic text when bullet has 'from X to Y' pattern."""
        text = "Reduced errors from 100 to 10"
        result = rewrite_star(text)
        
        # Has both 'from...to' and 'reduced'
        self.assertNotIn("improved reliability and delivery speed", result)
    
    def test_adds_generic_text_when_no_quantification(self):
        """Should add generic impact text when no quantification present."""
        text = "Standardized deployment process"
        result = rewrite_star(text)
        
        self.assertIn("improved reliability and delivery speed", result)
    
    def test_adds_generic_text_with_em_dash(self):
        """Should add generic text with em dash separator."""
        text = "Built automation framework"
        result = rewrite_star(text)
        
        self.assertIn("—", result)
        self.assertIn("improved reliability and delivery speed", result)
    
    def test_case_insensitive_detection(self):
        """Should detect impact words case-insensitively."""
        text = "IMPROVED system reliability"
        result = rewrite_star(text)

        # Should not add generic text since "IMPROVED" is present (detected case-insensitively)
        self.assertIn("IMPROVED", result)
        self.assertNotIn("improved reliability and delivery speed", result)
    
    def test_handles_empty_string(self):
        """Should handle empty string gracefully."""
        result = rewrite_star("")
        # Empty string gets generic text added
        self.assertTrue(result.endswith('.'))

    def test_handles_whitespace_only(self):
        """Should handle whitespace-only string."""
        result = rewrite_star("   ")
        # Whitespace-only gets generic text added
        self.assertTrue(result.endswith('.'))
    
    def test_preserves_original_content(self):
        """Should preserve the original bullet content."""
        text = "Led microservices transition improving deployment frequency 50%"
        result = rewrite_star(text)
        
        self.assertIn("Led microservices transition", result)
        self.assertIn("50%", result)
    
    def test_real_world_example_1(self):
        """Test with real resume bullet - quantified."""
        text = "Led microservices + micro-frontend transition for 'Online Access', improving deployment frequency 50% and enabling independent team releases"
        result = rewrite_star(text)
        
        # Should not add generic text (has percentage and 'enabling')
        self.assertNotIn("improved reliability and delivery speed", result)
        self.assertTrue(result.endswith('.'))
    
    def test_real_world_example_2(self):
        """Test with real resume bullet - no quantification."""
        text = "Hardened pipelines with linting (ESLint), SAST, and gating; standardized rollback playbooks"
        result = rewrite_star(text)
        
        # Should add generic text (no quantification)
        self.assertIn("improved reliability and delivery speed", result)
        self.assertTrue(result.endswith('.'))
    
    def test_real_world_example_3(self):
        """Test with real resume bullet - time range."""
        text = "Delivered cloud/automation workshops and built CI/CD templates that cut setup time from days to hours"
        result = rewrite_star(text)
        
        # Should not add generic text (has 'from...to' and 'cut')
        self.assertNotIn("improved reliability and delivery speed", result)
        self.assertTrue(result.endswith('.'))


if __name__ == '__main__':
    unittest.main()

