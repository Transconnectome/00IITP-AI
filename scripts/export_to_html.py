#!/usr/bin/env python3
import glob
from pathlib import Path
from markdown_it import MarkdownIt

def main():
    # Order of files
    files = [
        "00_executive_summary.md",
        "01_architecture.md",
        "02_methodology.md",
        "03_allostasis.md",
        "04_validation.md",
        "99_red_team_review.md"
    ]
    
    base_dir = Path("docs/03_proposal/drafts")
    full_md = ""
    
    # Merge Markdown
    for fname in files:
        fpath = base_dir / fname
        if fpath.exists():
            print(f"Adding {fname}...")
            full_md += f"\n\n<!-- FILE: {fname} -->\n\n"
            full_md += fpath.read_text(encoding="utf-8")
        else:
            print(f"Warning: {fname} not found.")

    # Convert to HTML
    md = MarkdownIt()
    html_body = md.render(full_md)
    
    # Wrap in simple HTML for browser viewing
    html_doc = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>IITP Proposal Export</title>
<style>
    body {{
        font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
        line-height: 1.6;
        max_width: 800px;
        margin: 0 auto;
        padding: 20px;
    }}
    h1, h2, h3 {{ color: #2c3e50; }}
    code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
    img {{ max_width: 100%; }}
    blockquote {{ border-left: 4px solid #aaf; padding-left: 10px; color: #555; }}
</style>
</head>
<body>
{html_body}
</body>
</html>
    """
    
    output_path = Path("IITP_Proposal_Full.html")
    output_path.write_text(html_doc, encoding="utf-8")
    print(f"✅ Generated {output_path.absolute()}")

if __name__ == "__main__":
    main()
