
import markdown
import os
import subprocess

# Paths
base_dir = "/home/juke/git/00IITP-AI/docs/03_proposal"
md_file = os.path.join(base_dir, "executive_summary_neuro_ginr.md")
html_file = os.path.join(base_dir, "executive_summary_neuro_ginr.html")
pdf_file = os.path.join(base_dir, "executive_summary_neuro_ginr.pdf")

# Read MD
with open(md_file, "r", encoding="utf-8") as f:
    text = f.read()

# Convert to HTML
html_body = markdown.markdown(text, extensions=['tables'])

# Add minimal CSS for PDF rendering
html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        font-family: "Malgun Gothic", "Apple SD Gothic Neo", sans-serif;
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }}
    h1, h2, h3 {{ color: #333; }}
    img {{ max-width: 100%; height: auto; }}
    blockquote {{
        border-left: 4px solid #ddd;
        padding-left: 10px;
        color: #555;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 20px;
    }}
    th, td {{
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }}
    th {{ background-color: #f2f2f2; }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

# Write HTML
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated HTML: {html_file}")

# Convert to PDF using LibreOffice
# Note: LibreOffice output dir defaults to source dir if not specified, or we use --outdir
cmd = [
    "libreoffice", "--headless", "--convert-to", "pdf", 
    html_file, "--outdir", base_dir
]

print("Running LibreOffice conversion...")
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print(f"Successfully generated PDF: {pdf_file}")
else:
    print("LibreOffice conversion failed:")
    print(result.stderr)
