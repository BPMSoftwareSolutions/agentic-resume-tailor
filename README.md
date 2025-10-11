# Agentic Resume Tailor

AI‑assisted tooling to customize your resume to a target job description (Phase 1).

## Features (Phase 1)
- Parse a Job Description (JD) and extract skills/keywords.
- Score your achievements vs. the JD.
- Select and rewrite the strongest bullets using STAR‑style phrasing.
- Render a tailored resume using a Jinja2 template to Markdown, HTML, and DOCX.
- **NEW:** Hybrid HTML/CSS resume generation with multiple professional themes.

## Roadmap (Phase 2 – optional & ToS‑aware)
- Integrations with job boards that **offer APIs or explicit automation permissions** (e.g., Greenhouse/Lever postings on employer sites).
- Human‑in‑the‑loop Playwright flows for sites that require manual review/submit. **Do not bypass CAPTCHAs or site anti‑bot controls.**

## Quickstart

### Generate Markdown Resume
```bash
pip install -r requirements.txt
python src/tailor.py --jd data/sample_jd.txt --out out/Sidney_Resume_DEVOPS.md
python src/export_docx.py --md out/Sidney_Resume_DEVOPS.md --docx out/Sidney_Resume_DEVOPS.docx
```

### Generate HTML Resume (NEW!)
```bash
# Generate HTML resume with professional theme
python src/tailor.py --jd data/sample_jd.txt --out out/Sidney_Resume_DEVOPS.html --format html --theme professional

# Or generate directly from master resume
python src/generate_hybrid_resume.py --input data/master_resume.json --output out/resume.html --theme modern
```

**Available Themes:** `professional`, `modern`, `executive`

**Convert to PDF:** Open the HTML file in your browser and use Print → Save as PDF

## Documentation

- **[Hybrid HTML Resume Generation](docs/HYBRID_HTML_RESUME_GENERATION.md)** - Complete guide to HTML resume generation
- **[Quality Tests Summary](docs/QUALITY_TESTS_GREEN_SUMMARY.md)** - Test suite documentation
- **[TDD Validation Summary](docs/TDD_VALIDATION_SUMMARY.md)** - TDD approach documentation

## Test Suite

All 159 tests passing ✅

```bash
python -m pytest tests/ -v
```
