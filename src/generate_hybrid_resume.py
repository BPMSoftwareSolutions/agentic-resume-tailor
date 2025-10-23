"""
Generate Hybrid Resume - CLI for HTML resume generation.

This script generates professional resumes using HTML with CSS styling.
Default input is data/master_resume.json.

Usage:
    python src/generate_hybrid_resume.py --output resume.html --theme creative
    python src/generate_hybrid_resume.py --all-themes --output-dir ./output
    python src/generate_hybrid_resume.py --output resume.html --docx
    python src/generate_hybrid_resume.py --output resume.html --jd data/sample_jd.txt --use-rag
"""

import argparse
import json
import sys
from pathlib import Path

from docx_resume_exporter import DOCXResumeExporter
from hybrid_css_generator import HybridCSSGenerator
from hybrid_html_assembler import HybridHTMLAssembler
from hybrid_resume_processor import HybridResumeProcessor
from jd_parser import extract_keywords
from tailor import retrieve_rag_context, select_and_rewrite


def generate_hybrid_resume(
    resume_json_path: str,
    output_html_path: str,
    theme: str = "creative",
    export_docx: bool = False,
    jd_path: str = None,
    use_rag: bool = False,
    use_llm_rewriting: bool = False,
    show_rag_context: bool = False,
    vector_store_path: str = "data/rag/vector_store.json",
) -> bool:
    """
    Generate hybrid HTML+SVG resume with optional RAG tailoring.

    Args:
        resume_json_path: Path to resume JSON file
        output_html_path: Path for output HTML file
        theme: Theme name (professional, modern, executive, creative)
        export_docx: Whether to also export to DOCX format
        jd_path: Path to job description for RAG retrieval
        use_rag: Whether to use RAG for tailoring
        use_llm_rewriting: Whether to use LLM for rewriting
        show_rag_context: Whether to display RAG context
        vector_store_path: Path to RAG vector store

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\n{'='*80}")
        print(f"HYBRID RESUME GENERATION - {theme.upper()} THEME")
        if use_rag:
            print("(RAG-Enhanced Tailoring Enabled)")
        print(f"{'='*80}\n")

        # Load resume data
        with open(resume_json_path, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)

        # Step 1: Apply RAG tailoring if requested
        if use_rag and jd_path:
            print("🧠 Applying RAG-enhanced tailoring...")
            try:
                # Extract keywords from job description
                from jd_fetcher import ingest_jd
                jd_path_resolved, jd_text = ingest_jd(jd_path)
                keywords = extract_keywords(jd_text)
                print(f"   Extracted {len(keywords)} keywords from job description")

                # Retrieve RAG context
                if Path(vector_store_path).exists():
                    rag_context = retrieve_rag_context(keywords, vector_store_path)
                    if rag_context.get("success"):
                        print(f"   ✅ Retrieved RAG context for {len(rag_context.get('context', {}))} keywords")
                        if show_rag_context:
                            print(f"\n   RAG Context Summary:")
                            for keyword, context in list(rag_context.get('context', {}).items())[:3]:
                                print(f"     - {keyword}: {len(context.get('documents', []))} documents")
                    else:
                        print(f"   ⚠️  RAG retrieval failed: {rag_context.get('error')}")
                        rag_context = None
                else:
                    print(f"   ⚠️  Vector store not found at {vector_store_path}")
                    rag_context = None

                # Tailor experience with RAG
                if "experience" in resume_data:
                    resume_data["experience"] = select_and_rewrite(
                        resume_data["experience"],
                        keywords,
                        rag_context=rag_context,
                        use_llm_rewriting=use_llm_rewriting
                    )
                    print(f"   ✅ Tailored {len(resume_data['experience'])} experience entries\n")

            except Exception as e:
                print(f"   ⚠️  RAG tailoring failed: {e}")
                print(f"   Continuing with original resume data\n")

        # Step 2: Process resume data and generate HTML structure
        print("Processing resume data and generating HTML structure...")

        # Save tailored data to temp file for processing
        temp_json = output_html_path.replace(".html", "_temp.json")
        with open(temp_json, 'w', encoding='utf-8') as f:
            json.dump(resume_data, f, indent=2)

        processor = HybridResumeProcessor(temp_json, theme)
        html_content = processor.generate_html()
        print(f"HTML structure generated\n")

        # Step 3: Generate CSS from theme configuration
        print("Generating CSS from theme configuration...")
        css_generator = HybridCSSGenerator(theme)
        css = css_generator.generate_css()
        print(f"CSS generated\n")

        # Step 4: Assemble complete HTML document
        print("Assembling complete HTML document...")
        assembler = HybridHTMLAssembler(theme)
        resume_name = resume_data.get("name", "Resume")
        complete_html = assembler.assemble_html(html_content, css, resume_name)
        print(f"HTML document assembled\n")

        # Step 5: Save to file
        print(f"Saving to {output_html_path}...")
        success = assembler.save_html(complete_html, output_html_path)

        # Clean up temp file
        Path(temp_json).unlink(missing_ok=True)

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
            print(f"Name: {resume_name}")
            if use_rag:
                print(f"RAG-Enhanced: Yes")
            print()
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
    resume_json_path: str,
    output_dir: str,
    export_docx: bool = False,
    jd_path: str = None,
    use_rag: bool = False,
    use_llm_rewriting: bool = False,
    show_rag_context: bool = False,
    vector_store_path: str = "data/rag/vector_store.json",
) -> dict:
    """
    Generate resume in all available themes.

    Args:
        resume_json_path: Path to resume JSON file
        output_dir: Directory for output files
        export_docx: Whether to also export to DOCX format
        jd_path: Path to job description for RAG retrieval
        use_rag: Whether to use RAG for tailoring
        use_llm_rewriting: Whether to use LLM for rewriting
        show_rag_context: Whether to display RAG context
        vector_store_path: Path to RAG vector store

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
    if use_rag:
        print("(RAG-Enhanced Tailoring Enabled)")
    print(f"{'='*80}\n")

    for theme in themes:
        output_file = output_path / f"resume_{theme}.html"
        print(f"Generating {theme} theme...")
        success = generate_hybrid_resume(
            resume_json_path,
            str(output_file),
            theme,
            export_docx,
            jd_path=jd_path,
            use_rag=use_rag,
            use_llm_rewriting=use_llm_rewriting,
            show_rag_context=show_rag_context,
            vector_store_path=vector_store_path,
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
        description="Generate professional resume using hybrid HTML+SVG approach with optional RAG tailoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate single theme (uses data/master_resume.json by default)
  python src/generate_hybrid_resume.py --output out/resume.html --theme creative

  # Generate all themes with custom input
  python src/generate_hybrid_resume.py --input data/master_resume.json --all-themes --output-dir ./out

  # Generate with DOCX export
  python src/generate_hybrid_resume.py --output out/resume.html --docx

  # Generate with RAG-enhanced tailoring
  python src/generate_hybrid_resume.py --output out/resume.html --jd data/sample_jd.txt --use-rag

  # Generate with RAG and LLM rewriting
  python src/generate_hybrid_resume.py --output out/resume.html --jd data/sample_jd.txt --use-rag --use-llm-rewriting

  # Generate all themes with RAG
  python src/generate_hybrid_resume.py --all-themes --jd data/sample_jd.txt --use-rag --show-rag-context
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
    parser.add_argument(
        "--jd", help="Path to job description for RAG-enhanced tailoring"
    )
    parser.add_argument(
        "--use-rag",
        action="store_true",
        help="Use RAG to retrieve relevant experiences from vector store",
    )
    parser.add_argument(
        "--use-llm-rewriting",
        action="store_true",
        help="Use LLM for evidence-constrained bullet rewriting (requires --use-rag)",
    )
    parser.add_argument(
        "--show-rag-context",
        action="store_true",
        help="Display RAG context during generation",
    )
    parser.add_argument(
        "--vector-store",
        default="data/rag/vector_store.json",
        help="Path to RAG vector store (default: data/rag/vector_store.json)",
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

    # Validate RAG arguments
    if args.use_llm_rewriting and not args.use_rag:
        print("⚠️  Warning: --use-llm-rewriting requires --use-rag. Enabling RAG.")
        args.use_rag = True

    if args.use_rag and not args.jd:
        print("⚠️  Warning: --use-rag requires --jd. RAG will be skipped.")
        args.use_rag = False

    # Determine export formats
    export_docx = args.docx

    # Generate resume(s)
    if args.all_themes:
        results = generate_all_themes(
            str(input_path),
            args.output_dir,
            export_docx,
            jd_path=args.jd,
            use_rag=args.use_rag,
            use_llm_rewriting=args.use_llm_rewriting,
            show_rag_context=args.show_rag_context,
            vector_store_path=args.vector_store,
        )
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
            str(input_path),
            args.output,
            args.theme,
            export_docx,
            jd_path=args.jd,
            use_rag=args.use_rag,
            use_llm_rewriting=args.use_llm_rewriting,
            show_rag_context=args.show_rag_context,
            vector_store_path=args.vector_store,
        )
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
