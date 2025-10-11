import argparse, re
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path

def md_to_docx(md_path, docx_path):
    """Convert Markdown resume to ATS-friendly DOCX format."""
    md_text = Path(md_path).read_text(encoding='utf-8')
    doc = Document()

    # Set default font for ATS compatibility
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)

    lines = md_text.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # H1 - Name (centered, larger)
        if line.startswith('# '):
            p = doc.add_paragraph(line[2:])
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.runs[0]
            run.font.size = Pt(18)
            run.font.bold = True

        # H2 - Section headers (bold, larger)
        elif line.startswith('## '):
            p = doc.add_paragraph(line[3:])
            run = p.runs[0]
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Bold text for job titles (e.g., **Role — Company**)
        elif line.startswith('**') and line.endswith('**)'):
            # Extract text between ** markers
            text = line[2:-2]
            p = doc.add_paragraph(text)
            run = p.runs[0]
            run.font.bold = True
            run.font.size = Pt(11)

        # Bullet points
        elif line.startswith('- '):
            text = line[2:]
            p = doc.add_paragraph(text, style='List Bullet')
            run = p.runs[0]
            run.font.size = Pt(11)

        # Regular text (contact info, summary, etc.)
        else:
            # Handle inline bold/italic markdown
            p = doc.add_paragraph()

            # Simple inline formatting parser
            parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', line)
            for part in parts:
                run = None
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part[2:-2])
                    run.font.bold = True
                elif part.startswith('*') and part.endswith('*'):
                    run = p.add_run(part[1:-1])
                    run.font.italic = True
                elif part:
                    run = p.add_run(part)

                if run:
                    run.font.size = Pt(11)

        i += 1

    doc.save(docx_path)
    print(f"Saved ATS-friendly DOCX: {docx_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True)
    ap.add_argument("--docx", required=True)
    args = ap.parse_args()
    md_to_docx(args.md, args.docx)
