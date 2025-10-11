"""Integration tests for the complete resume tailoring pipeline."""
import sys
from pathlib import Path
import tempfile
import os
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import unittest
from tailor import load_resume, select_and_rewrite, render_markdown
from jd_parser import extract_keywords
from export_docx import md_to_docx
from docx import Document


class TestEndToEndPipeline(unittest.TestCase):
    """Test the complete resume tailoring pipeline."""
    
    def setUp(self):
        """Create temporary directory and test files."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a sample resume
        self.resume_data = {
            "name": "Test User",
            "title": "DevOps Engineer",
            "location": "Test City, ST",
            "contact": {
                "email": "test@example.com",
                "phone": "(123) 456-7890"
            },
            "summary": "Experienced DevOps engineer.",
            "skills": ["CI/CD", "Python", "Terraform"],
            "experience": [
                {
                    "employer": "Tech Company",
                    "role": "Senior DevOps Engineer",
                    "dates": "2020 – 2024",
                    "bullets": [
                        {
                            "text": "Built CI/CD pipelines with Python and Terraform",
                            "tags": ["CI/CD", "Python", "Terraform"]
                        },
                        {
                            "text": "Managed Kubernetes clusters",
                            "tags": ["Kubernetes"]
                        },
                        {
                            "text": "Improved deployment frequency by 50%",
                            "tags": ["DevOps", "Metrics"]
                        },
                        {
                            "text": "Wrote documentation",
                            "tags": ["Documentation"]
                        }
                    ]
                }
            ],
            "education": [
                {
                    "school": "Test University",
                    "degree": "Bachelor of Science",
                    "year": "2015"
                }
            ]
        }
        
        self.resume_path = Path(self.temp_dir) / "resume.json"
        self.resume_path.write_text(json.dumps(self.resume_data), encoding='utf-8')
        
        # Create a sample job description
        self.jd_text = """
        We are seeking a DevOps Engineer with strong Python and CI/CD experience.
        Must have experience with Terraform and cloud infrastructure.
        Kubernetes knowledge is a plus.
        """
        
        self.jd_path = Path(self.temp_dir) / "jd.txt"
        self.jd_path.write_text(self.jd_text, encoding='utf-8')
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_complete_pipeline(self):
        """Test the complete pipeline from JD to tailored resume."""
        # Step 1: Extract keywords from JD
        keywords = extract_keywords(self.jd_text)
        
        self.assertIn("python", keywords)
        self.assertIn("ci/cd", keywords)
        self.assertIn("terraform", keywords)
        
        # Step 2: Load resume
        resume_data = load_resume(str(self.resume_path))
        
        self.assertEqual(resume_data["name"], "Test User")
        self.assertGreater(len(resume_data["experience"]), 0)
        
        # Step 3: Select and rewrite bullets
        tailored_experience = select_and_rewrite(
            resume_data["experience"], 
            keywords, 
            per_job=3
        )
        
        self.assertEqual(len(tailored_experience), 1)
        self.assertIn("selected_bullets", tailored_experience[0])
        self.assertEqual(len(tailored_experience[0]["selected_bullets"]), 3)
        
        # Step 4: Render markdown
        template_path = Path(__file__).parent.parent / "templates" / "resume.md.j2"
        md_path = Path(self.temp_dir) / "resume.md"
        
        resume_data["experience"] = tailored_experience
        render_markdown(resume_data, str(template_path), str(md_path))
        
        self.assertTrue(md_path.exists())
        md_content = md_path.read_text(encoding='utf-8')
        self.assertIn("Test User", md_content)
        self.assertIn("DevOps Engineer", md_content)
        
        # Step 5: Convert to DOCX
        docx_path = Path(self.temp_dir) / "resume.docx"
        md_to_docx(str(md_path), str(docx_path))
        
        self.assertTrue(docx_path.exists())
        
        # Verify DOCX content (H1 name is skipped per template format)
        doc = Document(str(docx_path))
        text = "\n".join([p.text for p in doc.paragraphs])
        # Name (H1) is skipped, but title and other content is present
        self.assertIn("DevOps Engineer", text)
        self.assertIn("Test City", text)
    
    def test_top_bullets_selected(self):
        """Test that top 3 most relevant bullets are selected."""
        keywords = extract_keywords(self.jd_text)
        tailored = select_and_rewrite(self.resume_data["experience"], keywords, per_job=3)
        
        # Should have exactly 3 bullets
        self.assertEqual(len(tailored[0]["selected_bullets"]), 3)
        
        # The most relevant bullets should be selected
        bullets_text = " ".join(tailored[0]["selected_bullets"])
        self.assertIn("CI/CD", bullets_text)
        self.assertIn("Python", bullets_text)
    
    def test_star_phrasing_applied(self):
        """Test that STAR-style phrasing is applied to bullets."""
        keywords = extract_keywords(self.jd_text)
        tailored = select_and_rewrite(self.resume_data["experience"], keywords, per_job=3)
        
        # All bullets should end with period
        for bullet in tailored[0]["selected_bullets"]:
            self.assertTrue(bullet.endswith('.'))
    
    def test_quantified_results_preserved(self):
        """Test that quantified results are preserved and not modified."""
        keywords = extract_keywords(self.jd_text)
        tailored = select_and_rewrite(self.resume_data["experience"], keywords, per_job=3)
        
        bullets_text = " ".join(tailored[0]["selected_bullets"])
        
        # Should preserve the 50% metric
        self.assertIn("50%", bullets_text)
    
    def test_utf8_encoding_throughout(self):
        """Test that UTF-8 encoding is preserved throughout the pipeline."""
        # Add special characters to resume
        self.resume_data["name"] = "José García"
        self.resume_data["experience"][0]["dates"] = "2020 – 2024"  # en-dash
        
        resume_path = Path(self.temp_dir) / "resume_utf8.json"
        resume_path.write_text(json.dumps(self.resume_data), encoding='utf-8')
        
        keywords = extract_keywords(self.jd_text)
        resume_data = load_resume(str(resume_path))
        tailored = select_and_rewrite(resume_data["experience"], keywords, per_job=3)
        
        template_path = Path(__file__).parent.parent / "templates" / "resume.md.j2"
        md_path = Path(self.temp_dir) / "resume_utf8.md"
        
        resume_data["experience"] = tailored
        render_markdown(resume_data, str(template_path), str(md_path))
        
        md_content = md_path.read_text(encoding='utf-8')
        
        # Should preserve special characters
        self.assertIn("José García", md_content)
        self.assertIn("–", md_content)  # en-dash
    
    def test_empty_experience(self):
        """Test handling of empty experience list."""
        keywords = extract_keywords(self.jd_text)
        tailored = select_and_rewrite([], keywords, per_job=3)
        
        self.assertEqual(len(tailored), 0)
    
    def test_fewer_bullets_than_requested(self):
        """Test when job has fewer bullets than per_job limit."""
        # Create experience with only 2 bullets
        experience = [{
            "employer": "Company",
            "role": "Engineer",
            "dates": "2020 – 2024",
            "bullets": [
                {"text": "Built CI/CD pipelines", "tags": ["CI/CD"]},
                {"text": "Managed infrastructure", "tags": ["Infrastructure"]}
            ]
        }]
        
        keywords = ["ci/cd", "infrastructure"]
        tailored = select_and_rewrite(experience, keywords, per_job=3)
        
        # Should return all 2 bullets, not fail
        self.assertEqual(len(tailored[0]["selected_bullets"]), 2)


if __name__ == '__main__':
    unittest.main()

