"""
Hybrid HTML Assembler - Assemble complete HTML document.

This module combines HTML structure, CSS, and SVG graphics into a
complete, self-contained HTML document.
"""

from typing import Dict, Any


class HybridHTMLAssembler:
    """
    Assemble complete HTML document from components.
    """
    
    def __init__(self, theme: str = "creative"):
        """
        Initialize the HTML assembler.
        
        Args:
            theme: Theme name (professional, modern, executive, creative)
        """
        self.theme = theme
    
    def assemble_html(self, html_content: str, css: str, resume_name: str = "Resume") -> str:
        """
        Create complete HTML document.
        
        Structure:
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <title>{name} - Resume</title>
          <style>{css}</style>
        </head>
        <body>
          <div class="resume-container">
            {html_content}
          </div>
        </body>
        </html>
        
        Args:
            html_content: Generated HTML content from HybridResumeProcessor
            css: Generated CSS from HybridCSSGenerator
            resume_name: Name for the document title
            
        Returns:
            Complete HTML document as string
        """
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{resume_name} - Resume</title>
  <meta name="description" content="Professional resume generated with hybrid HTML+SVG approach">
  <meta name="generator" content="SVG Lab Hybrid Resume Generator">
  <meta name="theme" content="{self.theme}">
  <style>
{css}
  </style>
</head>
<body>
  <div class="resume-container">
{html_content}
  </div>
</body>
</html>'''
    
    def save_html(self, html: str, output_path: str) -> bool:
        """
        Save HTML document to file.
        
        Args:
            html: Complete HTML document
            output_path: Path for output file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            return True
        except Exception as e:
            print(f"Error saving HTML: {e}")
            return False

