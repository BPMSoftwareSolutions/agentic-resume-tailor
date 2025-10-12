"""
Job Description Fetcher - Download and save job descriptions from URLs or local files.

This module provides functionality to:
1. Load JD from local file (.md, .txt)
2. Download JD from URL (Indeed, LinkedIn, etc.)
3. Save JD to data/job_listings/ directory
"""

import re
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse
import urllib.request
from html.parser import HTMLParser


class HTMLTextExtractor(HTMLParser):
    """Simple HTML parser to extract text content."""
    
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {'script', 'style', 'head', 'meta', 'link'}
        self.current_tag = None
    
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
    
    def handle_endtag(self, tag):
        self.current_tag = None
    
    def handle_data(self, data):
        if self.current_tag not in self.skip_tags:
            text = data.strip()
            if text:
                self.text_parts.append(text)
    
    def get_text(self) -> str:
        """Get extracted text with proper spacing."""
        return '\n'.join(self.text_parts)


def is_url(path: str) -> bool:
    """
    Check if the given path is a URL.
    
    Args:
        path: Path or URL string
        
    Returns:
        True if path is a URL
    """
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def generate_slug(url: str) -> str:
    """
    Generate a filename-safe slug from URL.
    
    Args:
        url: URL to generate slug from
        
    Returns:
        Filename-safe slug
    """
    # Extract domain and path
    parsed = urlparse(url)
    
    # Get the last part of the path or use domain
    path_parts = [p for p in parsed.path.split('/') if p]
    if path_parts:
        slug_base = path_parts[-1]
    else:
        slug_base = parsed.netloc.replace('www.', '')
    
    # Clean up the slug
    slug = re.sub(r'[^a-zA-Z0-9-]', '_', slug_base)
    slug = re.sub(r'_+', '_', slug)
    slug = slug.strip('_')
    
    # Limit length
    if len(slug) > 50:
        slug = slug[:50]
    
    return slug or 'job_description'


def fetch_from_url(url: str) -> str:
    """
    Fetch job description from URL.
    
    Args:
        url: URL to fetch from
        
    Returns:
        Text content of the job description
        
    Raises:
        Exception: If fetch fails
    """
    try:
        # Set user agent to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
        
        # Extract text from HTML
        parser = HTMLTextExtractor()
        parser.feed(html_content)
        text = parser.get_text()
        
        if not text or len(text) < 100:
            raise ValueError("Extracted text is too short or empty")
        
        return text
        
    except Exception as e:
        raise Exception(f"Failed to fetch from URL: {str(e)}")


def load_from_file(file_path: str) -> str:
    """
    Load job description from local file.
    
    Args:
        file_path: Path to local file
        
    Returns:
        Text content of the file
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return path.read_text(encoding='utf-8')


def save_jd(content: str, filename: str, output_dir: str = "data/job_listings") -> str:
    """
    Save job description to file.
    
    Args:
        content: JD text content
        filename: Filename (without extension)
        output_dir: Output directory
        
    Returns:
        Path to saved file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Ensure .md extension
    if not filename.endswith('.md'):
        filename = f"{filename}.md"
    
    file_path = output_path / filename
    file_path.write_text(content, encoding='utf-8')
    
    return str(file_path)


def ingest_jd(source: str, output_dir: str = "data/job_listings") -> Tuple[str, str]:
    """
    Ingest job description from URL or local file.
    
    Args:
        source: URL or local file path
        output_dir: Directory to save downloaded JDs
        
    Returns:
        Tuple of (file_path, content)
        
    Raises:
        Exception: If ingestion fails
    """
    if is_url(source):
        # Fetch from URL
        print(f"📥 Fetching job description from URL: {source}")
        content = fetch_from_url(source)
        
        # Generate filename
        slug = generate_slug(source)
        file_path = save_jd(content, slug, output_dir)
        
        print(f"✅ Saved to: {file_path}")
        return file_path, content
    else:
        # Load from local file
        print(f"📂 Loading job description from file: {source}")
        content = load_from_file(source)
        
        # If file is not in job_listings directory, copy it there
        source_path = Path(source)
        if output_dir not in str(source_path.parent):
            file_path = save_jd(content, source_path.stem, output_dir)
            print(f"✅ Copied to: {file_path}")
            return file_path, content
        else:
            return source, content


if __name__ == "__main__":
    # Test with local file
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python jd_fetcher.py <url_or_file_path>")
        sys.exit(1)
    
    source = sys.argv[1]
    
    try:
        file_path, content = ingest_jd(source)
        print(f"\n📄 Content preview (first 500 chars):")
        print(content[:500])
        print(f"\n✅ Successfully ingested JD to: {file_path}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

