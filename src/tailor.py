import argparse
import json
import os
import sys
from pathlib import Path

from jinja2 import Template

from jd_fetcher import ingest_jd
from jd_parser import extract_keywords
from rewriter import rewrite_star
from scorer import score_bullets
from rag.retriever import Retriever
from rag.rag_indexer import RAGIndexer

# Fix Windows console encoding for emoji support
if sys.platform == "win32":
    try:
        # Set console to UTF-8 mode
        os.system("chcp 65001 > nul")
        # Reconfigure stdout/stderr to use UTF-8
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        # If reconfiguration fails, continue without emoji support
        pass


def load_resume_index(data_dir: Path):
    """Load the resume index file."""
    index_file = data_dir / "resumes" / "index.json"
    if not index_file.exists():
        raise FileNotFoundError(f"Resume index not found: {index_file}")

    with open(index_file, "r", encoding="utf-8") as f:
        return json.load(f)


def find_resume_by_identifier(index_data, identifier: str):
    """
    Find a resume by name or company identifier.

    Args:
        index_data: Resume index data
        identifier: Company name or resume name to search for

    Returns:
        Resume metadata dict or None if not found
    """
    identifier_lower = identifier.lower()

    for resume in index_data.get("resumes", []):
        name = resume.get("name", "").lower()

        # Check for exact match or partial match
        if identifier_lower in name or name in identifier_lower:
            return resume

    return None


def load_resume(path_or_identifier):
    """
    Load resume by file path or identifier (company name).

    Args:
        path_or_identifier: Either a file path or a resume identifier

    Returns:
        Resume data dict
    """
    # Check if it's a file path
    path = Path(path_or_identifier)
    if path.exists() and path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))

    # Otherwise, try to find by identifier
    data_dir = Path("data")
    try:
        index_data = load_resume_index(data_dir)
        resume_meta = find_resume_by_identifier(index_data, path_or_identifier)

        if not resume_meta:
            raise FileNotFoundError(
                f"Resume not found: '{path_or_identifier}'. "
                f"Provide either a valid file path or a resume name/company identifier."
            )

        resume_id = resume_meta["id"]
        resume_file = data_dir / "resumes" / f"{resume_id}.json"

        if not resume_file.exists():
            raise FileNotFoundError(f"Resume file not found: {resume_file}")

        print(f"📂 Found resume: {resume_meta['name']}")
        return json.loads(resume_file.read_text(encoding="utf-8"))

    except FileNotFoundError:
        raise
    except Exception as e:
        raise FileNotFoundError(f"Could not load resume '{path_or_identifier}': {e}")


def retrieve_rag_context(keywords, vector_store_path, top_k=5):
    """
    Retrieve relevant experiences from RAG vector store based on keywords.

    Args:
        keywords: List of keywords from job description
        vector_store_path: Path to vector store
        top_k: Number of results per keyword

    Returns:
        Dictionary with retrieved context
    """
    try:
        retriever = Retriever(vector_store_path)
        rag_context = {}

        for keyword in keywords[:10]:  # Use top 10 keywords
            result = retriever.retrieve(keyword, top_k=top_k)
            rag_context[keyword] = result

        return {
            "success": True,
            "context": rag_context,
            "keywords_searched": keywords[:10],
        }
    except Exception as e:
        print(f"⚠️  RAG retrieval failed: {e}")
        return {"success": False, "error": str(e)}


def select_and_rewrite(experience, keywords, per_job=3, rag_context=None):
    tailored = []
    for job in experience:
        top = score_bullets(job["bullets"], keywords)[:per_job]
        rewritten = [rewrite_star(b["text"]) for b in top]
        job_data = {**job, "selected_bullets": rewritten}

        # Add RAG context if available
        if rag_context and rag_context.get("success"):
            job_data["rag_context"] = rag_context.get("context", {})

        tailored.append(job_data)
    return tailored


def render_markdown(data, template_path, out_path):
    tpl = Template(Path(template_path).read_text(encoding="utf-8"))
    md = tpl.render(**data)
    Path(out_path).write_text(md, encoding="utf-8")
    return out_path


def generate_html_resume(data, out_path, theme="professional"):
    """Generate HTML resume using hybrid approach."""
    from hybrid_css_generator import HybridCSSGenerator
    from hybrid_html_assembler import HybridHTMLAssembler
    from hybrid_resume_processor import HybridResumeProcessor

    # Save tailored data to temp JSON
    temp_json = out_path.replace(".html", "_temp.json")
    Path(temp_json).write_text(json.dumps(data, indent=2), encoding="utf-8")

    # Generate HTML
    processor = HybridResumeProcessor(temp_json, theme)
    html_content = processor.generate_html()

    css_generator = HybridCSSGenerator(theme)
    css = css_generator.generate_css()

    assembler = HybridHTMLAssembler(theme)
    resume_name = data.get("name", "Resume")
    complete_html = assembler.assemble_html(html_content, css, resume_name)

    assembler.save_html(complete_html, out_path)

    # Clean up temp file
    Path(temp_json).unlink(missing_ok=True)

    return out_path


def generate_docx_from_html(html_path, docx_path=None):
    """Generate DOCX from HTML using DOCXResumeExporter."""
    from docx_resume_exporter import DOCXResumeExporter

    if docx_path is None:
        docx_path = html_path.replace(".html", ".docx")

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
        description="Tailor resume to job description with keyword extraction and rewriting"
    )
    ap.add_argument(
        "--resume",
        default="data/master_resume.json",
        help='Resume file path OR resume name/company identifier (e.g., "Ford", "Master Resume")',
    )
    ap.add_argument("--jd", required=True, help="Path to job description file or URL")
    ap.add_argument(
        "--template",
        default="templates/resume.md.j2",
        help="Path to Jinja2 template (for markdown format)",
    )
    ap.add_argument("--out", required=True, help="Output file path")
    ap.add_argument(
        "--format",
        choices=["markdown", "html"],
        default="markdown",
        help="Output format: markdown or html (default: markdown)",
    )
    ap.add_argument(
        "--theme",
        choices=["professional", "modern", "executive", "creative"],
        default="professional",
        help="HTML theme (only used with --format html)",
    )
    ap.add_argument(
        "--docx",
        action="store_true",
        help="Also generate DOCX file (only works with HTML format)",
    )
    ap.add_argument(
        "--use-rag",
        action="store_true",
        help="Use RAG to retrieve relevant experiences from vector store",
    )
    ap.add_argument(
        "--vector-store",
        default="data/rag/vector_store.json",
        help="Path to RAG vector store (default: data/rag/vector_store.json)",
    )
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

    # Retrieve RAG context if requested
    rag_context = None
    if args.use_rag:
        print("🧠 Retrieving relevant experiences from RAG...")
        if Path(args.vector_store).exists():
            rag_context = retrieve_rag_context(keywords, args.vector_store)
            if rag_context.get("success"):
                print(f"✅ Retrieved RAG context for {len(rag_context.get('context', {}))} keywords")
            else:
                print(f"⚠️  RAG retrieval failed: {rag_context.get('error')}")
        else:
            print(f"⚠️  Vector store not found at {args.vector_store}")
            print("   Run: python -m src.rag.rag_indexer to create vector store")

    # Load and tailor resume
    print("📝 Tailoring resume...")
    data = load_resume(args.resume)
    data["experience"] = select_and_rewrite(data["experience"], keywords, rag_context=rag_context)

    # Generate output
    if args.format == "html":
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
    print("\n" + "=" * 60)
    print("📊 JOB DESCRIPTION ANALYSIS")
    print("=" * 60)
    print(f"\n🎯 Top Keywords ({len(keywords[:12])}):")
    print(f"   {', '.join(keywords[:12])}")

    summary = generate_jd_summary(jd_text, keywords)
    print(f"\n💡 Summary:")
    print(f"   {summary}")
    print("\n" + "=" * 60)

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
