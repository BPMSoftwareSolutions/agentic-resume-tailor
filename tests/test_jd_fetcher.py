"""Unit tests for jd_fetcher.py - Job Description ingestion."""

import shutil
import sys
import tempfile
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import unittest

from jd_fetcher import (HTMLTextExtractor, generate_slug, ingest_jd, is_url,
                        load_from_file, save_jd)


class TestIsUrl(unittest.TestCase):
    """Test URL detection."""

    def test_valid_http_url(self):
        """Should recognize HTTP URLs."""
        self.assertTrue(is_url("http://example.com"))

    def test_valid_https_url(self):
        """Should recognize HTTPS URLs."""
        self.assertTrue(is_url("https://example.com/job/123"))

    def test_local_file_path(self):
        """Should not recognize local paths as URLs."""
        self.assertFalse(is_url("data/job.txt"))
        self.assertFalse(is_url("/home/user/job.md"))
        self.assertFalse(is_url("C:\\Users\\job.txt"))

    def test_invalid_url(self):
        """Should not recognize invalid URLs."""
        self.assertFalse(is_url("not a url"))
        self.assertFalse(is_url(""))


class TestGenerateSlug(unittest.TestCase):
    """Test slug generation from URLs."""

    def test_slug_from_path(self):
        """Should generate slug from URL path."""
        slug = generate_slug("https://example.com/jobs/senior-engineer")
        # Hyphens are preserved in slugs
        self.assertEqual(slug, "senior-engineer")

    def test_slug_from_domain(self):
        """Should use domain if no path."""
        slug = generate_slug("https://example.com")
        self.assertEqual(slug, "example_com")

    def test_slug_removes_special_chars(self):
        """Should remove special characters."""
        slug = generate_slug("https://example.com/job-posting-#123!")
        self.assertNotIn("#", slug)
        self.assertNotIn("!", slug)

    def test_slug_length_limit(self):
        """Should limit slug length."""
        long_url = "https://example.com/" + "a" * 100
        slug = generate_slug(long_url)
        self.assertLessEqual(len(slug), 50)


class TestHTMLTextExtractor(unittest.TestCase):
    """Test HTML text extraction."""

    def test_extract_simple_text(self):
        """Should extract text from simple HTML."""
        html = "<html><body><p>Hello World</p></body></html>"
        parser = HTMLTextExtractor()
        parser.feed(html)
        text = parser.get_text()
        self.assertIn("Hello World", text)

    def test_skip_script_tags(self):
        """Should skip script tag content."""
        html = "<html><body><p>Content</p><script>alert('test')</script></body></html>"
        parser = HTMLTextExtractor()
        parser.feed(html)
        text = parser.get_text()
        self.assertIn("Content", text)
        self.assertNotIn("alert", text)

    def test_skip_style_tags(self):
        """Should skip style tag content."""
        html = "<html><head><style>body { color: red; }</style></head><body>Text</body></html>"
        parser = HTMLTextExtractor()
        parser.feed(html)
        text = parser.get_text()
        self.assertIn("Text", text)
        self.assertNotIn("color", text)


class TestLoadFromFile(unittest.TestCase):
    """Test loading JD from local file."""

    def setUp(self):
        """Create temporary test file."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test_jd.txt"
        self.test_content = "Test job description content"
        self.test_file.write_text(self.test_content, encoding="utf-8")

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir)

    def test_load_existing_file(self):
        """Should load content from existing file."""
        content = load_from_file(str(self.test_file))
        self.assertEqual(content, self.test_content)

    def test_load_nonexistent_file(self):
        """Should raise FileNotFoundError for missing file."""
        with self.assertRaises(FileNotFoundError):
            load_from_file("nonexistent_file.txt")


class TestSaveJd(unittest.TestCase):
    """Test saving JD to file."""

    def setUp(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir)

    def test_save_with_md_extension(self):
        """Should save file with .md extension."""
        content = "Job description"
        file_path = save_jd(content, "test_job", self.temp_dir)

        self.assertTrue(Path(file_path).exists())
        self.assertTrue(file_path.endswith(".md"))
        self.assertEqual(Path(file_path).read_text(encoding="utf-8"), content)

    def test_save_adds_md_extension(self):
        """Should add .md extension if missing."""
        content = "Job description"
        file_path = save_jd(content, "test_job", self.temp_dir)

        self.assertTrue(file_path.endswith(".md"))

    def test_save_creates_directory(self):
        """Should create output directory if it doesn't exist."""
        new_dir = Path(self.temp_dir) / "new_subdir"
        content = "Job description"
        file_path = save_jd(content, "test_job", str(new_dir))

        self.assertTrue(new_dir.exists())
        self.assertTrue(Path(file_path).exists())


class TestIngestJd(unittest.TestCase):
    """Test JD ingestion from file or URL."""

    def setUp(self):
        """Create temporary test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test_jd.txt"
        self.test_content = "Test job description for software engineer"
        self.test_file.write_text(self.test_content, encoding="utf-8")

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir)

    def test_ingest_from_local_file(self):
        """Should ingest JD from local file."""
        file_path, content = ingest_jd(str(self.test_file), self.temp_dir)

        self.assertEqual(content, self.test_content)
        self.assertTrue(Path(file_path).exists())

    def test_ingest_copies_to_output_dir(self):
        """Should copy file to output directory if not already there."""
        output_dir = Path(self.temp_dir) / "job_listings"
        file_path, content = ingest_jd(str(self.test_file), str(output_dir))

        self.assertTrue(output_dir.exists())
        self.assertIn("job_listings", file_path)


if __name__ == "__main__":
    unittest.main()
