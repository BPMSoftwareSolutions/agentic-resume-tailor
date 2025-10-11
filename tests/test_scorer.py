"""Unit tests for scorer.py - Resume bullet scoring."""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import unittest
from scorer import score_bullets


class TestScoreBullets(unittest.TestCase):
    """Test the score_bullets function."""
    
    def test_score_by_text_content(self):
        """Should score bullets based on text content matching keywords."""
        bullets = [
            {"text": "Built CI/CD pipelines with Python", "tags": []},
            {"text": "Managed team meetings", "tags": []},
        ]
        keywords = ["ci/cd", "python", "pipelines"]
        
        scored = score_bullets(bullets, keywords)
        
        # First bullet should score higher
        self.assertGreater(scored[0]["_score"], scored[1]["_score"])
        self.assertEqual(scored[0]["text"], "Built CI/CD pipelines with Python")
    
    def test_score_by_tags(self):
        """Should score bullets based on tags."""
        bullets = [
            {"text": "Did something", "tags": ["Python", "CI/CD"]},
            {"text": "Did something else", "tags": ["Marketing"]},
        ]
        keywords = ["python", "ci/cd"]
        
        scored = score_bullets(bullets, keywords)
        
        # First bullet should score higher
        self.assertGreater(scored[0]["_score"], scored[1]["_score"])
    
    def test_text_scores_higher_than_tags(self):
        """Text matches should be weighted higher than tag matches."""
        bullets = [
            {"text": "Built Python automation", "tags": []},
            {"text": "Did something", "tags": ["Python", "Automation"]},
        ]
        keywords = ["python", "automation"]
        
        scored = score_bullets(bullets, keywords)
        
        # Text match should score higher than tag match
        self.assertGreater(scored[0]["_score"], scored[1]["_score"])
    
    def test_quantified_results_bonus(self):
        """Should give bonus for quantified results."""
        bullets = [
            {"text": "Improved performance by 50%", "tags": []},
            {"text": "Improved performance", "tags": []},
        ]
        keywords = ["performance"]
        
        scored = score_bullets(bullets, keywords)
        
        # Quantified result should score higher
        self.assertGreater(scored[0]["_score"], scored[1]["_score"])
    
    def test_multiplier_bonus(self):
        """Should give bonus for multiplier expressions like '2x'."""
        bullets = [
            {"text": "Increased speed 3x faster", "tags": []},
            {"text": "Increased speed", "tags": []},
        ]
        keywords = ["speed"]
        
        scored = score_bullets(bullets, keywords)
        
        # Multiplier should score higher
        self.assertGreater(scored[0]["_score"], scored[1]["_score"])
    
    def test_improvement_range_bonus(self):
        """Should give bonus for 'from X to Y' improvement ranges."""
        bullets = [
            {"text": "Cut deployment time from days to hours", "tags": []},
            {"text": "Cut deployment time", "tags": []},
        ]
        keywords = ["deployment"]
        
        scored = score_bullets(bullets, keywords)
        
        # Range should score higher
        self.assertGreater(scored[0]["_score"], scored[1]["_score"])
    
    def test_time_scale_bonus(self):
        """Should give bonus for time/scale mentions."""
        bullets = [
            {"text": "Managed 13 teams across the organization", "tags": []},
            {"text": "Managed teams", "tags": []},
        ]
        keywords = ["teams"]
        
        scored = score_bullets(bullets, keywords)
        
        # Specific number should score higher
        self.assertGreater(scored[0]["_score"], scored[1]["_score"])
    
    def test_length_bonus(self):
        """Should give bonus for longer, more detailed statements."""
        bullets = [
            {"text": "Built comprehensive CI/CD automation framework with extensive testing coverage", "tags": []},
            {"text": "Built CI/CD", "tags": []},
        ]
        keywords = ["ci/cd"]
        
        scored = score_bullets(bullets, keywords)
        
        # Longer statement should score higher
        self.assertGreater(scored[0]["_score"], scored[1]["_score"])
    
    def test_multi_word_keyword_weight(self):
        """Should give higher weight to longer, more specific keywords."""
        bullets = [
            {"text": "Experience with GitHub Actions", "tags": []},
            {"text": "Experience with GitHub", "tags": []},
        ]
        keywords = ["github actions", "github"]
        
        scored = score_bullets(bullets, keywords)
        
        # Multi-word match should score higher
        self.assertGreater(scored[0]["_score"], scored[1]["_score"])
    
    def test_empty_bullets(self):
        """Should handle empty bullets list."""
        scored = score_bullets([], ["python"])
        self.assertEqual(len(scored), 0)
    
    def test_empty_keywords(self):
        """Should handle empty keywords list."""
        bullets = [{"text": "Some text", "tags": []}]
        scored = score_bullets(bullets, [])
        
        # Should still return scored bullets
        self.assertEqual(len(scored), 1)
        self.assertIn("_score", scored[0])
    
    def test_sorted_descending(self):
        """Should return bullets sorted by score descending."""
        bullets = [
            {"text": "Low relevance", "tags": []},
            {"text": "High relevance with Python and CI/CD and 50% improvement", "tags": []},
            {"text": "Medium relevance with Python", "tags": []},
        ]
        keywords = ["python", "ci/cd"]
        
        scored = score_bullets(bullets, keywords)
        
        # Should be sorted highest to lowest
        for i in range(len(scored) - 1):
            self.assertGreaterEqual(scored[i]["_score"], scored[i+1]["_score"])
    
    def test_case_insensitive_matching(self):
        """Should match keywords case-insensitively."""
        bullets = [
            {"text": "PYTHON and Python and python", "tags": []},
        ]
        keywords = ["python"]
        
        scored = score_bullets(bullets, keywords)
        
        # Should match regardless of case
        self.assertGreater(scored[0]["_score"], 0)
    
    def test_preserves_original_data(self):
        """Should preserve all original bullet data."""
        bullets = [
            {"text": "Some text", "tags": ["Tag1"], "custom_field": "value"},
        ]
        keywords = ["text"]
        
        scored = score_bullets(bullets, keywords)
        
        # Should preserve all fields
        self.assertEqual(scored[0]["text"], "Some text")
        self.assertEqual(scored[0]["tags"], ["Tag1"])
        self.assertEqual(scored[0]["custom_field"], "value")
        self.assertIn("_score", scored[0])


if __name__ == '__main__':
    unittest.main()

