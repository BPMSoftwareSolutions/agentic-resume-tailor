# Hybrid HTML Resume Generation

## Overview

The hybrid HTML resume generation system creates professional, print-ready resumes using HTML and CSS. This approach provides:

- **Perfect rendering** - HTML/CSS renders consistently across browsers and PDF converters
- **Easy customization** - Multiple themes with simple CSS modifications
- **Print-ready output** - Optimized for printing and PDF conversion
- **Semantic markup** - Clean, accessible HTML structure
- **No dependencies** - Pure HTML/CSS, no external libraries needed for viewing

## Architecture

The hybrid system consists of three main components:

### 1. **HybridResumeProcessor** (`src/hybrid_resume_processor.py`)
Generates semantic HTML structure from resume JSON data.

**Features:**
- Automatic date sorting (most recent first)
- Semantic HTML5 tags (header, section, article)
- Data attributes for programmatic access
- Support for both string and object bullet formats
- Handles technical proficiencies and areas of expertise

**Key Methods:**
- `generate_html()` - Main entry point, generates complete HTML structure
- `_generate_header_html()` - Creates header with name and contact info
- `_generate_summary_html()` - Creates professional summary section
- `_generate_skills_html()` - Creates two-column skills section
- `_generate_experience_html()` - Creates experience section with bullets
- `_generate_education_html()` - Creates education and certifications section

### 2. **HybridCSSGenerator** (`src/hybrid_css_generator.py`)
Generates CSS stylesheets from theme configurations.

**Features:**
- Three built-in themes: Professional, Modern, Executive
- Responsive layout using CSS Grid and Flexbox
- Print-optimized styles (@media print)
- Consistent typography and spacing
- Professional color palettes

**Themes:**
- **Professional** - Clean, traditional corporate style (blue/gray)
- **Modern** - Contemporary design with subtle accents (indigo)
- **Executive** - Premium, executive-level presentation (black/gray)

### 3. **HybridHTMLAssembler** (`src/hybrid_html_assembler.py`)
Assembles complete HTML documents from components.

**Features:**
- Combines HTML structure and CSS into self-contained document
- Adds proper HTML5 doctype and meta tags
- Includes viewport settings for responsive display
- Embeds CSS inline for portability

## Usage

### Command Line Interface

#### Generate from Master Resume
```bash
python src/generate_hybrid_resume.py \
  --input data/master_resume.json \
  --output out/resume.html \
  --theme professional
```

#### Generate from Tailored Resume
```bash
python src/generate_hybrid_resume.py \
  --input out/tailored_resume.json \
  --output out/resume.html \
  --theme modern
```

#### Available Themes
- `professional` - Clean, traditional corporate style (default)
- `modern` - Contemporary design with subtle accents
- `executive` - Premium, executive-level presentation

### Integration with Tailor Pipeline

The hybrid HTML generation is integrated into the main tailor pipeline:

```bash
# Generate HTML resume directly from job description
python src/tailor.py \
  --resume data/master_resume.json \
  --jd job_description.txt \
  --out out/tailored_resume.html \
  --format html \
  --theme professional
```

**Options:**
- `--format markdown` - Generate Markdown (default)
- `--format html` - Generate HTML
- `--theme professional|modern|executive` - Choose HTML theme

### Programmatic Usage

```python
from hybrid_resume_processor import HybridResumeProcessor
from hybrid_css_generator import HybridCSSGenerator
from hybrid_html_assembler import HybridHTMLAssembler

# Generate HTML
processor = HybridResumeProcessor('data/master_resume.json', 'professional')
html_content = processor.generate_html()

# Generate CSS
css_generator = HybridCSSGenerator('professional')
css = css_generator.generate_css()

# Assemble complete document
assembler = HybridHTMLAssembler('professional')
complete_html = assembler.assemble_html(html_content, css, 'Sidney Jones')

# Save to file
assembler.save_html(complete_html, 'out/resume.html')
```

## Converting to PDF

### Method 1: Browser Print (Recommended)
1. Open the HTML file in your browser
2. Press `Ctrl+P` (Windows) or `Cmd+P` (Mac)
3. Select "Save as PDF" or "Microsoft Print to PDF"
4. Click Save

**Advantages:**
- Best quality output
- Preserves all styling
- No additional dependencies
- Works on all platforms

### Method 2: Command Line Tools (Optional)

#### Using wkhtmltopdf
```bash
wkhtmltopdf out/resume.html out/resume.pdf
```

#### Using Playwright (Python)
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('file:///path/to/resume.html')
    page.pdf(path='resume.pdf', format='Letter')
    browser.close()
```

## File Structure

```
src/
├── hybrid_resume_processor.py    # HTML structure generator
├── hybrid_css_generator.py       # CSS theme generator
├── hybrid_html_assembler.py      # HTML document assembler
├── generate_hybrid_resume.py     # CLI script
└── tailor.py                     # Main pipeline (updated)

out/
├── hybrid_resume_professional.html
├── hybrid_resume_modern.html
└── hybrid_resume_executive.html
```

## Theme Customization

To create a custom theme, add a new theme configuration to `HybridCSSGenerator.THEMES`:

```python
'custom': {
    'colors': {
        'primary': '#1A237E',
        'secondary': '#283593',
        'accent': '#3F51B5',
        'text': '#212121',
        'text_light': '#757575',
        'background': '#FAFAFA',
        'section_bg': '#FFFFFF'
    },
    'typography': {
        'fontFamily': 'Calibri, Arial, sans-serif',
        'baseFontSize': '10pt',
        'headingFontSize': '11pt',
        'nameFontSize': '18pt'
    }
}
```

## Features

### ✅ Automatic Date Sorting
Experiences are automatically sorted by most recent first, with "Present" jobs at the top.

### ✅ Responsive Layout
Two-column layout for skills section, responsive header with contact info.

### ✅ Print Optimization
- Proper page breaks
- Print-specific styles
- Letter size (8.5" x 11")
- 0.5" margins

### ✅ Semantic HTML
- Proper heading hierarchy (h1, h2, h3)
- Data attributes for programmatic access
- Accessible markup

### ✅ Professional Typography
- Calibri font family (ATS-friendly)
- Consistent font sizes (10pt body, 11pt headings, 18pt name)
- Proper line heights and spacing

## Advantages Over DOCX

1. **Consistent Rendering** - HTML/CSS renders identically across all browsers
2. **Easy Customization** - Simple CSS changes for styling
3. **Version Control Friendly** - Text-based format works well with Git
4. **No Dependencies** - No need for python-docx or complex libraries
5. **Print-Ready** - Optimized for printing and PDF conversion
6. **Portable** - Single HTML file contains everything

## Testing

All existing tests pass with the hybrid HTML integration:

```bash
python -m pytest tests/ -v
# 159 passed in 4.19s
```

## Migration from DOCX

The hybrid HTML system complements the existing DOCX generation:

- **DOCX** - Use for ATS systems that require .docx format
- **HTML** - Use for printing, PDF conversion, and visual presentation

Both formats are generated from the same JSON data, ensuring consistency.

## Future Enhancements

Potential improvements:
- Additional themes (creative, technical, academic)
- SVG graphics for visual elements
- Interactive features (collapsible sections)
- Dark mode support
- Responsive mobile layout
- Export to other formats (LaTeX, PDF)

## Troubleshooting

### HTML file doesn't display correctly
- Ensure the file is saved with UTF-8 encoding
- Check that all CSS is embedded in the `<style>` tag
- Verify the resume JSON has all required fields

### PDF conversion issues
- Use browser print for best results
- Ensure print margins are set to 0.5"
- Check that "Print backgrounds" is enabled

### Styling issues
- Verify the theme name is correct (professional, modern, executive)
- Check that CSS is being generated correctly
- Inspect the HTML in browser developer tools

## Support

For issues or questions:
1. Check the documentation in `docs/`
2. Review example output in `out/`
3. Run tests to verify installation: `python -m pytest tests/`

