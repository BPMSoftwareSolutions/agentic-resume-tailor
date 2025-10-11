import json, argparse
from jinja2 import Template
from jd_parser import extract_keywords
from scorer import score_bullets
from rewriter import rewrite_star
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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resume", default="data/master_resume.json")
    ap.add_argument("--jd", required=True)
    ap.add_argument("--template", default="templates/resume.md.j2")
    ap.add_argument("--out", required=True)
    ap.add_argument("--format", choices=['markdown', 'html'], default='markdown',
                   help='Output format: markdown or html (default: markdown)')
    ap.add_argument("--theme", choices=['professional', 'modern', 'executive'],
                   default='professional',
                   help='HTML theme (only used with --format html)')
    args = ap.parse_args()

    jd_text = Path(args.jd).read_text(encoding='utf-8')
    keywords = extract_keywords(jd_text)
    data = load_resume(args.resume)
    data["experience"] = select_and_rewrite(data["experience"], keywords)

    if args.format == 'html':
        generate_html_resume(data, args.out, args.theme)
        print(f"Tailored HTML resume written to {args.out}\nKeywords: {keywords[:12]} ...")
    else:
        render_markdown(data, args.template, args.out)
        print(f"Tailored markdown written to {args.out}\nKeywords: {keywords[:12]} ...")

if __name__ == "__main__":
    main()
