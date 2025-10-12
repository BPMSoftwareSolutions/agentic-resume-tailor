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
- **NEW:** Multi-resume support with job listing management and automated tailoring ([Issue #6](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/issues/6))
- **NEW:** Local AI Agent for interactive automation and command execution ([Issue #8](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/issues/8))
- **NEW:** AI Agent Web Integration - Chat with the agent directly from your browser ([Issue #12](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/issues/12))

## Roadmap (Phase 2 – optional & ToS‑aware)
- Integrations with job boards that **offer APIs or explicit automation permissions** (e.g., Greenhouse/Lever postings on employer sites).
- Human‑in‑the‑loop Playwright flows for sites that require manual review/submit. **Do not bypass CAPTCHAs or site anti‑bot controls.**

## Quickstart

### Multi-Resume Dashboard (NEW! ✨✨)
```bash
# Install dependencies
pip install -r requirements.txt

# Migrate existing master resume (first time only)
python src/migrate_to_multi_resume.py

# Start the API server
python src/api/app.py

# Open the dashboard in your browser
# Navigate to: src/web/dashboard.html
```

**Features:**
- ✅ Create and manage multiple tailored resumes
- ✅ Add and track job listings
- ✅ Automatically tailor resumes to job listings
- ✅ Visual dashboard with statistics
- ✅ Duplicate and edit resumes
- ✅ Export resumes in HTML/DOCX format

See [Multi-Resume Support Documentation](docs/MULTI_RESUME_SUPPORT.md) for details.

### Local AI Agent (NEW! 🤖)
```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'

# Run the agent
python agent.py
```

**Features:**
- 🤖 Interactive chat with OpenAI models
- 🔧 Execute local commands with `run:` prefix
- 💾 Persistent conversation memory
- 🎯 Simple command-line interface

**Example Usage:**
```
💬 > What files are in this directory?
🤖 You can check with: run: ls

💬 > run: ls
✅ Command executed successfully:
agent.py  data/  src/  tests/  ...

💬 > run: git status
✅ Command executed successfully:
On branch main
nothing to commit, working tree clean
```

See [Local AI Agent Documentation](docs/LOCAL_AI_AGENT.md) for details.

### AI Agent Web Interface (NEW! 🌐🤖)
```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'

# Start the API server
python src/api/app.py

# Open the agent interface in your browser
# Navigate to: src/web/agent.html
```

**The agent now has a knowledge base system** that understands the codebase structure! You can give natural language commands like:

```
💬 > Update the Ford resume with this experience: "data/job_listings/Tailored Experience Summary for Ford.md"
🤖 I'll update the Ford resume with that experience file.

run: python src/update_resume_experience.py --resume "Ford" --experience "data/job_listings/Tailored Experience Summary for Ford.md"

✅ Successfully updated resume d474d761-18f2-48ab-99b5-9f30c54f75b2
   Found resume: Sidney_Jones_Senior_Software_Engineer_Ford
   Added 5 experience entries
```

The agent automatically:
- Finds resumes by company name (e.g., "Ford", "GM", "Credibly")
- Locates the correct files using `data/resumes/index.json`
- Executes the appropriate helper scripts
- Updates timestamps and metadata

See [Agent Knowledge Base Documentation](docs/AGENT_KNOWLEDGE_BASE.md) for details.

**Features:**
- 🌐 Browser-based chat interface
- 🔧 Execute commands from the web UI
- 💾 Persistent conversation memory
- 🔒 Command whitelisting and security controls
- ⚡ Quick action shortcuts
- 📜 View and manage conversation history

**Quick Actions:**
- Tailor resume to job posting
- Check git status
- Run tests
- View job listings

See [Agent Web Integration Documentation](docs/AGENT_WEB_INTEGRATION.md) for details.

### Web-Based Resume Editor
```bash
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
- ✅ Edit specific resumes via URL parameter

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

- **[Local AI Agent](docs/LOCAL_AI_AGENT.md)** - Interactive AI agent with command execution (NEW! 🤖)
- **[Resume Editor Web Interface](docs/RESUME_EDITOR_WEB_INTERFACE.md)** - Web-based resume editor guide
- **[Multi-Resume Support](docs/MULTI_RESUME_SUPPORT.md)** - Multi-resume management guide
- **[CI/CD Pipeline](docs/CI_CD_PIPELINE.md)** - Continuous integration and deployment guide
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
