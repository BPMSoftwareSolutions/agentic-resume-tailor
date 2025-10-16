"""Unit tests for jd_parser.py - Job Description keyword extraction."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import unittest

from jd_parser import DEFAULT_SKILLS, extract_keywords, normalize


class TestNormalize(unittest.TestCase):
    """Test the normalize function."""

    def test_normalize_lowercase(self):
        """Should convert text to lowercase."""
        result = normalize("Python Developer")
        self.assertEqual(result, "python developer")

    def test_normalize_special_chars(self):
        """Should remove special characters except allowed ones."""
        result = normalize("CI/CD & DevOps!")
        self.assertEqual(result, "ci/cd   devops ")

    def test_normalize_preserves_allowed_chars(self):
        """Should preserve +, /, #, and spaces."""
        result = normalize("C# and C++")
        self.assertEqual(result, "c# and c++")


class TestExtractKeywords(unittest.TestCase):
    """Test the extract_keywords function."""

    def test_extract_default_skills(self):
        """Should extract skills from DEFAULT_SKILLS list."""
        jd_text = "We need Python and Terraform experience with CI/CD pipelines."
        keywords = extract_keywords(jd_text)

        self.assertIn("python", keywords)
        self.assertIn("terraform", keywords)
        self.assertIn("ci/cd", keywords)

    def test_extract_multi_word_phrases(self):
        """Should extract multi-word technical phrases."""
        jd_text = "Experience with GitHub Actions and Azure DevOps required."
        keywords = extract_keywords(jd_text)

        self.assertIn("github actions", keywords)
        self.assertIn("azure devops", keywords)

    def test_extract_frequent_tokens(self):
        """Should extract frequently occurring tokens."""
        jd_text = "Cloud cloud cloud experience with deployment deployment deployment."
        keywords = extract_keywords(jd_text)

        # Should include frequent words
        self.assertTrue(any("cloud" in k for k in keywords))
        self.assertTrue(any("deployment" in k for k in keywords))

    def test_extract_with_extra_skills(self):
        """Should include extra skills provided."""
        jd_text = "We need React and Vue.js developers."
        extra = ["react", "vue.js"]
        keywords = extract_keywords(jd_text, extra=extra)

        self.assertIn("react", keywords)

    def test_no_duplicates(self):
        """Should not return duplicate keywords."""
        jd_text = "Python Python Python developer needed."
        keywords = extract_keywords(jd_text)

        # Count occurrences of 'python'
        python_count = sum(1 for k in keywords if k == "python")
        self.assertEqual(python_count, 1)

    def test_empty_jd(self):
        """Should handle empty job description."""
        keywords = extract_keywords("")
        self.assertIsInstance(keywords, list)

    def test_case_insensitive_matching(self):
        """Should match keywords case-insensitively."""
        jd_text = "PYTHON and Python and python all required."
        keywords = extract_keywords(jd_text)

        # Should only appear once
        python_count = sum(1 for k in keywords if k == "python")
        self.assertEqual(python_count, 1)

    def test_longer_phrases_matched_first(self):
        """Should match longer phrases before shorter ones."""
        jd_text = "GitHub Actions experience required."
        keywords = extract_keywords(jd_text)

        # Should match "github actions" not just "github"
        self.assertIn("github actions", keywords)


class TestDefaultSkills(unittest.TestCase):
    """Test the DEFAULT_SKILLS list."""

    def test_default_skills_not_empty(self):
        """DEFAULT_SKILLS should contain skills."""
        self.assertGreater(len(DEFAULT_SKILLS), 0)

    def test_default_skills_lowercase(self):
        """All DEFAULT_SKILLS should be lowercase."""
        for skill in DEFAULT_SKILLS:
            self.assertEqual(skill, skill.lower())

    def test_common_devops_skills_present(self):
        """Should include common DevOps skills."""
        expected_skills = ["ci/cd", "terraform", "kubernetes", "python"]
        for skill in expected_skills:
            self.assertIn(skill, DEFAULT_SKILLS)


if __name__ == "__main__":
    unittest.main()
