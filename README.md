# Agentic Resume Tailor

AI‑assisted tooling to customize your resume to a target job description (Phase 1).

## Features (Phase 1)
- Parse a Job Description (JD) and extract skills/keywords.
- Score your achievements vs. the JD.
- Select and rewrite the strongest bullets using STAR‑style phrasing.
- Render a tailored resume using a Jinja2 template to Markdown and DOCX.

## Roadmap (Phase 2 – optional & ToS‑aware)
- Integrations with job boards that **offer APIs or explicit automation permissions** (e.g., Greenhouse/Lever postings on employer sites).
- Human‑in‑the‑loop Playwright flows for sites that require manual review/submit. **Do not bypass CAPTCHAs or site anti‑bot controls.**

## Quickstart
```bash
pip install -r requirements.txt
python src/tailor.py --jd data/sample_jd.txt --out out/Sidney_Resume_DEVOPS.md
python src/export_docx.py --md out/Sidney_Resume_DEVOPS.md --docx out/Sidney_Resume_DEVOPS.docx
```
