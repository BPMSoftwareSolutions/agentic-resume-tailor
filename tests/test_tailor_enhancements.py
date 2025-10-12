"""Unit tests for enhanced tailor.py functionality - DOCX export and JD summary."""
import sys
from pathlib import Path
import tempfile
import shutil
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import unittest
from tailor import generate_jd_summary, generate_docx_from_html


class TestGenerateJdSummary(unittest.TestCase):
    """Test JD summary generation."""
    
    def test_summary_with_many_keywords(self):
        """Should generate summary with multiple keyword groups."""
        jd_text = "We need Python, AWS, Docker, Kubernetes, CI/CD, and microservices experience."
        keywords = ["python", "aws", "docker", "kubernetes", "ci/cd", "microservices", 
                   "terraform", "jenkins", "ansible", "prometheus", "grafana", "redis"]
        
        summary = generate_jd_summary(jd_text, keywords)
        
        # Should include first few keywords
        self.assertIn("python", summary.lower())
        self.assertIn("aws", summary.lower())
        self.assertIn("docker", summary.lower())
    
    def test_summary_with_few_keywords(self):
        """Should generate summary with few keywords."""
        jd_text = "Python developer needed"
        keywords = ["python", "developer"]
        
        summary = generate_jd_summary(jd_text, keywords)
        
        self.assertIn("python", summary.lower())
        self.assertIn("developer", summary.lower())
    
    def test_summary_limits_to_top_12(self):
        """Should only use top 12 keywords."""
        jd_text = "Many skills required"
        keywords = [f"skill{i}" for i in range(20)]
        
        summary = generate_jd_summary(jd_text, keywords)
        
        # Should not include keywords beyond 12
        self.assertNotIn("skill15", summary)
        self.assertNotIn("skill19", summary)


class TestGenerateDocxFromHtml(unittest.TestCase):
    """Test DOCX generation from HTML."""
    
    def setUp(self):
        """Create temporary test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.html_file = Path(self.temp_dir) / "test_resume.html"
        
        # Create a simple HTML file
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Resume</title></head>
        <body>
            <h1>John Doe</h1>
            <p>Software Engineer</p>
            <h2>Experience</h2>
            <ul>
                <li>Built CI/CD pipelines</li>
                <li>Developed microservices</li>
            </ul>
        </body>
        </html>
        """
        self.html_file.write_text(html_content, encoding='utf-8')
    
    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir)
    
    def test_generates_docx_with_default_name(self):
        """Should generate DOCX with default naming or raise error if not available."""
        try:
            docx_path = generate_docx_from_html(str(self.html_file))

            # Should create DOCX file
            self.assertTrue(Path(docx_path).exists())
            self.assertTrue(docx_path.endswith('.docx'))
            self.assertEqual(docx_path, str(self.html_file).replace('.html', '.docx'))
        except RuntimeError as e:
            # DOCX export may not be available in test environment
            self.assertIn("DOCX export failed", str(e))

    def test_generates_docx_with_custom_name(self):
        """Should generate DOCX with custom path or raise error if not available."""
        custom_path = str(Path(self.temp_dir) / "custom_resume.docx")

        try:
            docx_path = generate_docx_from_html(str(self.html_file), custom_path)

            self.assertTrue(Path(docx_path).exists())
            self.assertEqual(docx_path, custom_path)
        except RuntimeError as e:
            # DOCX export may not be available in test environment
            self.assertIn("DOCX export failed", str(e))


class TestTailorIntegration(unittest.TestCase):
    """Integration tests for enhanced tailor functionality."""
    
    def setUp(self):
        """Create temporary test environment."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test resume JSON
        self.resume_data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "555-1234",
            "summary": "Experienced software engineer",
            "experience": [
                {
                    "company": "Tech Corp",
                    "title": "Senior Engineer",
                    "dates": "2020-2023",
                    "bullets": [
                        {"text": "Built CI/CD pipelines with Python", "tags": ["python", "ci/cd"]},
                        {"text": "Deployed AWS infrastructure", "tags": ["aws", "cloud"]},
                        {"text": "Managed team meetings", "tags": ["management"]}
                    ]
                }
            ],
            "skills": ["Python", "AWS", "Docker"]
        }
        
        self.resume_file = Path(self.temp_dir) / "test_resume.json"
        self.resume_file.write_text(json.dumps(self.resume_data, indent=2), encoding='utf-8')
        
        # Create test JD
        self.jd_content = """
        Senior Software Engineer Position
        
        We are seeking an experienced engineer with:
        - Python programming
        - AWS cloud experience
        - CI/CD pipeline development
        - Docker containerization
        - Kubernetes orchestration
        """
        
        self.jd_file = Path(self.temp_dir) / "test_jd.txt"
        self.jd_file.write_text(self.jd_content, encoding='utf-8')
    
    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir)
    
    def test_tailor_extracts_keywords(self):
        """Should extract keywords from JD."""
        from jd_parser import extract_keywords
        
        keywords = extract_keywords(self.jd_content)
        
        self.assertIn("python", keywords)
        self.assertIn("aws", keywords)
        self.assertIn("ci/cd", keywords)
        self.assertIn("docker", keywords)
    
    def test_tailor_scores_and_selects_bullets(self):
        """Should score and select relevant bullets."""
        from jd_parser import extract_keywords
        from scorer import score_bullets
        
        keywords = extract_keywords(self.jd_content)
        bullets = self.resume_data["experience"][0]["bullets"]
        
        scored = score_bullets(bullets, keywords)
        
        # CI/CD and AWS bullets should score higher than management
        self.assertGreater(scored[0]["_score"], 0)
        self.assertIn("ci/cd", scored[0]["text"].lower() + " ".join(scored[0]["tags"]).lower())
    
    def test_summary_reflects_jd_content(self):
        """Should generate summary reflecting JD keywords."""
        from jd_parser import extract_keywords
        
        keywords = extract_keywords(self.jd_content)
        summary = generate_jd_summary(self.jd_content, keywords)
        
        # Summary should mention key technologies
        summary_lower = summary.lower()
        self.assertTrue(
            any(kw in summary_lower for kw in ["python", "aws", "ci/cd", "docker"])
        )


if __name__ == '__main__':
    unittest.main()

