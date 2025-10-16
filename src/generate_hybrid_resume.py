"""
Generate Hybrid Resume - CLI for HTML resume generation.

This script generates professional resumes using HTML with CSS styling.
Default input is data/master_resume.json.

Usage:
    python src/generate_hybrid_resume.py --output resume.html --theme creative
    python src/generate_hybrid_resume.py --all-themes --output-dir ./output
    python src/generate_hybrid_resume.py --output resume.html --docx
"""

import argparse
import sys
from pathlib import Path

from docx_resume_exporter import DOCXResumeExporter
from hybrid_css_generator import HybridCSSGenerator
from hybrid_html_assembler import HybridHTMLAssembler
from hybrid_resume_processor import HybridResumeProcessor


def generate_hybrid_resume(
    resume_json_path: str,
    output_html_path: str,
    theme: str = "creative",
    export_docx: bool = False,
) -> bool:
    """
    Generate hybrid HTML+SVG resume.

    Args:
        resume_json_path: Path to resume JSON file
        output_html_path: Path for output HTML file
        theme: Theme name (professional, modern, executive, creative)
        export_docx: Whether to also export to DOCX format

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\n{'='*80}")
        print(f"HYBRID RESUME GENERATION - {theme.upper()} THEME")
        print(f"{'='*80}\n")

        # Step 1: Process resume data and generate HTML structure
        print("Processing resume data and generating HTML structure...")
        processor = HybridResumeProcessor(resume_json_path, theme)
        html_content = processor.generate_html()
        print(f"HTML structure generated\n")

        # Step 2: Generate CSS from theme configuration
        print("Generating CSS from theme configuration...")
        css_generator = HybridCSSGenerator(theme)
        css = css_generator.generate_css()
        print(f"CSS generated\n")

        # Step 3: Assemble complete HTML document
        print("Assembling complete HTML document...")
        assembler = HybridHTMLAssembler(theme)
        resume_name = processor.resume_data.get("name", "Resume")
        complete_html = assembler.assemble_html(html_content, css, resume_name)
        print(f"HTML document assembled\n")

        # Step 4: Save to file
        print(f"Saving to {output_html_path}...")
        success = assembler.save_html(complete_html, output_html_path)

        if success:
            print(f"Resume saved successfully\n")

            # Convert to DOCX if requested
            docx_success = True
            if export_docx:
                docx_path = output_html_path.replace(".html", ".docx")
                exporter = DOCXResumeExporter()
                docx_success = exporter.export_to_docx(output_html_path, docx_path)
                if docx_success:
                    print(f"DOCX: {docx_path}\n")

            print(f"{'='*80}")
            print("HYBRID RESUME GENERATION COMPLETE!")
            print(f"{'='*80}\n")
            print(f"HTML: {output_html_path}")
            if export_docx and docx_success:
                print(f"DOCX: {docx_path}")
            print(f"Theme: {theme}")
            print(f"Name: {resume_name}\n")
            return True
        else:
            print(f"Failed to save resume\n")
            return False

    except Exception as e:
        print(f"\nError generating hybrid resume: {e}")
        import traceback

        traceback.print_exc()
        return False


def generate_all_themes(
    resume_json_path: str, output_dir: str, export_docx: bool = False
) -> dict:
    """
    Generate resume in all available themes.

    Args:
        resume_json_path: Path to resume JSON file
        output_dir: Directory for output files
        export_docx: Whether to also export to DOCX format

    Returns:
        Dictionary mapping theme names to success status
    """
    from pathlib import Path

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    themes = ["professional", "modern", "executive", "creative"]
    results = {}

    print(f"\n{'='*80}")
    print("GENERATING ALL THEMES")
    print(f"{'='*80}\n")

    for theme in themes:
        output_file = output_path / f"resume_{theme}.html"
        print(f"Generating {theme} theme...")
        success = generate_hybrid_resume(
            resume_json_path, str(output_file), theme, export_docx
        )
        results[theme] = success

        if success:
            print(f"✅ {theme.capitalize()} theme generated successfully\n")
        else:
            print(f"❌ {theme.capitalize()} theme generation failed\n")

    # Print summary
    print(f"\n{'='*80}")
    print("GENERATION SUMMARY")
    print(f"{'='*80}\n")

    for theme, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status}: {theme.capitalize()}")

    print()

    return results


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Generate professional resume using hybrid HTML+SVG approach",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate single theme (uses data/master_resume.json by default)
  python src/generate_hybrid_resume.py --output out/resume.html --theme creative

  # Generate all themes with custom input
  python src/generate_hybrid_resume.py --input data/master_resume.json --all-themes --output-dir ./out

  # Generate with DOCX export
  python src/generate_hybrid_resume.py --output out/resume.html --docx
        """,
    )

    parser.add_argument(
        "--input",
        default="data/master_resume.json",
        help="Path to resume JSON file (default: data/master_resume.json)",
    )
    parser.add_argument(
        "--output", help="Path for output HTML file (required unless --all-themes)"
    )
    parser.add_argument(
        "--theme",
        default="creative",
        choices=["professional", "modern", "executive", "creative"],
        help="Resume theme (default: creative)",
    )
    parser.add_argument(
        "--all-themes", action="store_true", help="Generate all theme variations"
    )
    parser.add_argument(
        "--output-dir",
        default="./resume_output",
        help="Output directory for all themes (default: ./resume_output)",
    )
    parser.add_argument(
        "--docx", action="store_true", help="Also generate DOCX version"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.all_themes and not args.output:
        parser.error("--output is required unless --all-themes is specified")

    # Resolve input path relative to repository root
    script_dir = Path(__file__).parent.parent  # Get repository root
    input_path = script_dir / args.input

    # Check if input file exists
    if not input_path.exists():
        print(f"❌ Error: Input file not found: {input_path}")
        print(f"   (Searched relative to: {script_dir})")
        sys.exit(1)

    # Determine export formats
    export_docx = args.docx

    # Generate resume(s)
    if args.all_themes:
        results = generate_all_themes(str(input_path), args.output_dir, export_docx)
        success_count = sum(1 for s in results.values() if s)

        if success_count == len(results):
            print("✅ All themes generated successfully!")
            sys.exit(0)
        elif success_count > 0:
            print(f"⚠️  {success_count}/{len(results)} themes generated successfully")
            sys.exit(1)
        else:
            print("❌ All theme generations failed")
            sys.exit(1)
    else:
        success = generate_hybrid_resume(
            str(input_path), args.output, args.theme, export_docx
        )
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
