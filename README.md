# Agentic Resume Tailor

[![CI/CD Pipeline](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/actions/workflows/ci.yml/badge.svg)](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

AI‑assisted tooling to customize your resume to a target job description (Phase 1).

## Features (Phase 1)
- Parse a Job Description (JD) and extract skills/keywords.
- Score your achievements vs. the JD.
- Select and rewrite the strongest bullets using STAR‑style phrasing.
- Render a tailored resume using a Jinja2 template to Markdown, HTML, and DOCX.
- **NEW:** Hybrid HTML/CSS resume generation with multiple professional themes.
- **NEW:** Web-based resume editor for managing master_resume.json ([Issue #2](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/issues/2))

## Roadmap (Phase 2 – optional & ToS‑aware)
- Integrations with job boards that **offer APIs or explicit automation permissions** (e.g., Greenhouse/Lever postings on employer sites).
- Human‑in‑the‑loop Playwright flows for sites that require manual review/submit. **Do not bypass CAPTCHAs or site anti‑bot controls.**

## Quickstart

### Web-Based Resume Editor (NEW! ✨)
```bash
# Install dependencies
pip install -r requirements.txt

# Start the resume editor (API + Web UI)
python start_resume_editor.py

# Or start manually:
# 1. Start API server
python src/api/app.py

# 2. Open src/web/index.html in your browser
```

**Features:**
- ✅ Visual editor for all resume sections
- ✅ Automatic backups on save
- ✅ Backup history and restoration
- ✅ Real-time validation
- ✅ Responsive design (mobile, tablet, desktop)

See [Resume Editor Documentation](docs/RESUME_EDITOR_WEB_INTERFACE.md) for details.

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
python src/generate_hybrid_resume.py --input data/master_resume.json --output out/resume.html --theme creative

# Generate all themes at once
python src/generate_hybrid_resume.py --input data/master_resume.json --all-themes --output-dir out

# Generate with DOCX export (requires pandoc or python-docx)
python src/generate_hybrid_resume.py --input data/master_resume.json --output out/resume.html --docx
```

**Available Themes:** `professional`, `modern`, `executive`, `creative`

**Theme Features:**
- **Professional**: Clean, traditional corporate style (Blue/Gray)
- **Modern**: Contemporary design with subtle accents (Indigo)
- **Executive**: Premium, executive-level presentation (Black/Gray)
- **Creative**: Vibrant, creative industry style (Pink/Orange) ✨ NEW!

**Convert to PDF:** Open the HTML file in your browser and use Print → Save as PDF

**DOCX Export:** Requires `pandoc` (preferred) or `pip install python-docx beautifulsoup4 lxml`

## Documentation

- **[Resume Editor Web Interface](docs/RESUME_EDITOR_WEB_INTERFACE.md)** - Web-based resume editor guide (NEW!)
- **[CI/CD Pipeline](docs/CI_CD_PIPELINE.md)** - Continuous integration and deployment guide (NEW!)
- **[Hybrid HTML Resume Generation](docs/HYBRID_HTML_RESUME_GENERATION.md)** - Complete guide to HTML resume generation
- **[Quality Tests Summary](docs/QUALITY_TESTS_GREEN_SUMMARY.md)** - Test suite documentation
- **[TDD Validation Summary](docs/TDD_VALIDATION_SUMMARY.md)** - TDD approach documentation

## Test Suite

All 159 tests passing ✅

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ -v --cov=src --cov-report=html

# Run specific test suites
python -m pytest tests/test_api.py -v
python -m pytest tests/test_integration.py -v
python -m pytest tests/test_comprehensive_quality_suite.py -v
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment:

- **Automated Testing**: All tests run automatically on every push and pull request
- **Multi-Python Support**: Tests run on Python 3.8, 3.9, 3.10, 3.11, and 3.12
- **Code Quality**: Automated linting with flake8, black, and isort
- **Security Scanning**: Automated security checks with safety and bandit
- **Coverage Reports**: Test coverage tracking with pytest-cov
- **Integration Tests**: Comprehensive quality suite validation

The pipeline ensures code quality and prevents regressions before merging.
