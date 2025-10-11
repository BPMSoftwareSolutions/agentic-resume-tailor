"""
Generate Hybrid Resume - CLI for HTML resume generation.

This script generates professional resumes using HTML with CSS styling.
Integrates with the agentic resume tailor pipeline.

Usage:
    python src/generate_hybrid_resume.py --input data/master_resume.json --output out/resume.html
    python src/generate_hybrid_resume.py --input out/tailored_resume.json --output out/resume.html --theme modern
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from hybrid_resume_processor import HybridResumeProcessor
from hybrid_css_generator import HybridCSSGenerator
from hybrid_html_assembler import HybridHTMLAssembler


def generate_hybrid_resume(resume_json_path: str, output_html_path: str, theme: str = "professional") -> bool:
    """
    Generate hybrid HTML resume.
    
    Args:
        resume_json_path: Path to resume JSON file
        output_html_path: Path for output HTML file
        theme: Theme name (professional, modern, executive)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\n{'='*80}")
        print(f"HYBRID RESUME GENERATION - {theme.upper()} THEME")
        print(f"{'='*80}\n")
        
        # Step 1: Process resume data and generate HTML structure
        print("📋 Processing resume data and generating HTML structure...")
        processor = HybridResumeProcessor(resume_json_path, theme)
        html_content = processor.generate_html()
        print(f"✓ HTML structure generated\n")
        
        # Step 2: Generate CSS from theme configuration
        print("🎨 Generating CSS from theme configuration...")
        css_generator = HybridCSSGenerator(theme)
        css = css_generator.generate_css()
        print(f"✓ CSS generated\n")
        
        # Step 3: Assemble complete HTML document
        print("🔧 Assembling complete HTML document...")
        assembler = HybridHTMLAssembler(theme)
        resume_name = processor.resume_data.get('name', 'Resume')
        complete_html = assembler.assemble_html(html_content, css, resume_name)
        print(f"✓ HTML document assembled\n")
        
        # Step 4: Save to file
        print(f"💾 Saving to {output_html_path}...")
        success = assembler.save_html(complete_html, output_html_path)
        
        if success:
            print(f"✓ Resume saved successfully\n")
            print(f"{'='*80}")
            print("✅ HYBRID RESUME GENERATION COMPLETE!")
            print(f"{'='*80}\n")
            print(f"📄 HTML: {output_html_path}")
            print(f"🎨 Theme: {theme}")
            print(f"👤 Name: {resume_name}\n")
            print("💡 To convert to PDF:")
            print("   1. Open the HTML file in your browser")
            print("   2. Press Ctrl+P (Windows) or Cmd+P (Mac)")
            print("   3. Select 'Save as PDF' or 'Microsoft Print to PDF'")
            print("   4. Click Save\n")
            return True
        else:
            print(f"❌ Failed to save resume\n")
            return False
            
    except Exception as e:
        print(f"\n❌ Error generating hybrid resume: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Generate professional resume using hybrid HTML approach',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generate from master resume
  python src/generate_hybrid_resume.py --input data/master_resume.json --output out/resume.html
  
  # Generate from tailored resume with modern theme
  python src/generate_hybrid_resume.py --input out/tailored_resume.json --output out/resume.html --theme modern
  
  # Generate with executive theme
  python src/generate_hybrid_resume.py --input data/master_resume.json --output out/resume.html --theme executive
        '''
    )
    
    parser.add_argument('--input', required=True, help='Path to resume JSON file')
    parser.add_argument('--output', required=True, help='Path for output HTML file')
    parser.add_argument('--theme', default='professional', 
                       choices=['professional', 'modern', 'executive'],
                       help='Resume theme (default: professional)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: Input file not found: {input_path}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate resume
    success = generate_hybrid_resume(str(input_path), str(output_path), args.theme)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

