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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resume", default="data/master_resume.json")
    ap.add_argument("--jd", required=True)
    ap.add_argument("--template", default="templates/resume.md.j2")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    jd_text = Path(args.jd).read_text(encoding='utf-8')
    keywords = extract_keywords(jd_text)
    data = load_resume(args.resume)
    data["experience"] = select_and_rewrite(data["experience"], keywords)
    render_markdown(data, args.template, args.out)
    print(f"Tailored markdown written to {args.out}\nKeywords: {keywords[:12]} ...")

if __name__ == "__main__":
    main()
