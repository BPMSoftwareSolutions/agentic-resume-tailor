import json, argparse
from jinja2 import Template
from jd_parser import extract_keywords
from scorer import score_bullets
from rewriter import rewrite_star
from jd_fetcher import ingest_jd
from pathlib import Path

def load_resume(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def select_and_rewrite(experience, keywords, per_job=3):
    tailored = []
    for job in experience:
        top = score_bullets(job["bullets"], keywords)[:per_job]
        rewritten = [rewrite_star(b["text"]) for b in top]
        tailored.append({**job, "selected_bullets": rewritten})
    return tailored

def render_markdown(data, template_path, out_path):
    tpl = Template(Path(template_path).read_text(encoding='utf-8'))
    md = tpl.render(**data)
    Path(out_path).write_text(md, encoding='utf-8')
    return out_path

def generate_html_resume(data, out_path, theme='professional'):
    """Generate HTML resume using hybrid approach."""
    from hybrid_resume_processor import HybridResumeProcessor
    from hybrid_css_generator import HybridCSSGenerator
    from hybrid_html_assembler import HybridHTMLAssembler

    # Save tailored data to temp JSON
    temp_json = out_path.replace('.html', '_temp.json')
    Path(temp_json).write_text(json.dumps(data, indent=2), encoding='utf-8')

    # Generate HTML
    processor = HybridResumeProcessor(temp_json, theme)
    html_content = processor.generate_html()

    css_generator = HybridCSSGenerator(theme)
    css = css_generator.generate_css()

    assembler = HybridHTMLAssembler(theme)
    resume_name = data.get('name', 'Resume')
    complete_html = assembler.assemble_html(html_content, css, resume_name)

    assembler.save_html(complete_html, out_path)

    # Clean up temp file
    Path(temp_json).unlink(missing_ok=True)

    return out_path


def generate_docx_from_html(html_path, docx_path=None):
    """Generate DOCX from HTML using DOCXResumeExporter."""
    from docx_resume_exporter import DOCXResumeExporter

    if docx_path is None:
        docx_path = html_path.replace('.html', '.docx')

    exporter = DOCXResumeExporter()
    success = exporter.export_to_docx(html_path, docx_path)

    if not success:
        raise RuntimeError("DOCX export failed - no export methods available")

    return docx_path


def generate_jd_summary(jd_text, keywords):
    """
    Generate a brief summary of the job description based on keywords.

    Args:
        jd_text: Full job description text
        keywords: List of extracted keywords

    Returns:
        Summary string
    """
    # Get top keywords
    top_keywords = keywords[:12]

    # Create a natural language summary
    if len(top_keywords) >= 5:
        summary = f"This role emphasizes {', '.join(top_keywords[:3])}"
        if len(top_keywords) > 3:
            summary += f", {', '.join(top_keywords[3:6])}"
        if len(top_keywords) > 6:
            summary += f", and {', '.join(top_keywords[6:])}"
    else:
        summary = f"Key skills: {', '.join(top_keywords)}"

    return summary

def main():
    ap = argparse.ArgumentParser(
        description='Tailor resume to job description with keyword extraction and rewriting'
    )
    ap.add_argument("--resume", default="data/master_resume.json",
                   help='Path to resume JSON file')
    ap.add_argument("--jd", required=True,
                   help='Path to job description file or URL')
    ap.add_argument("--template", default="templates/resume.md.j2",
                   help='Path to Jinja2 template (for markdown format)')
    ap.add_argument("--out", required=True,
                   help='Output file path')
    ap.add_argument("--format", choices=['markdown', 'html'], default='markdown',
                   help='Output format: markdown or html (default: markdown)')
    ap.add_argument("--theme", choices=['professional', 'modern', 'executive', 'creative'],
                   default='professional',
                   help='HTML theme (only used with --format html)')
    ap.add_argument("--docx", action='store_true',
                   help='Also generate DOCX file (only works with HTML format)')
    args = ap.parse_args()

    # Ingest JD (supports URL or local file)
    print("📋 Processing job description...")
    try:
        jd_path, jd_text = ingest_jd(args.jd)
    except Exception as e:
        print(f"❌ Error loading job description: {e}")
        return 1

    # Extract keywords
    print("🔍 Extracting keywords...")
    keywords = extract_keywords(jd_text)

    # Load and tailor resume
    print("📝 Tailoring resume...")
    data = load_resume(args.resume)
    data["experience"] = select_and_rewrite(data["experience"], keywords)

    # Generate output
    if args.format == 'html':
        print(f"🎨 Generating HTML resume with '{args.theme}' theme...")
        generate_html_resume(data, args.out, args.theme)
        print(f"✅ Tailored HTML resume written to {args.out}")

        # Generate DOCX if requested
        if args.docx:
            print("📄 Generating DOCX from HTML...")
            docx_path = generate_docx_from_html(args.out)
            print(f"✅ DOCX resume written to {docx_path}")
    else:
        print("📝 Generating Markdown resume...")
        render_markdown(data, args.template, args.out)
        print(f"✅ Tailored markdown written to {args.out}")

        if args.docx:
            print("⚠️  Warning: --docx flag only works with --format html")

    # Display summary
    print("\n" + "="*60)
    print("📊 JOB DESCRIPTION ANALYSIS")
    print("="*60)
    print(f"\n🎯 Top Keywords ({len(keywords[:12])}):")
    print(f"   {', '.join(keywords[:12])}")

    summary = generate_jd_summary(jd_text, keywords)
    print(f"\n💡 Summary:")
    print(f"   {summary}")
    print("\n" + "="*60)

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
