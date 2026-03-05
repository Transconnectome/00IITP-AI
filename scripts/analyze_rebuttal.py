import fitz
import sys
import os
import re

try:
    from docx import Document
except ImportError:
    Document = None

def clean_text(text):
    # Remove excessive newlines but keep paragraph structure
    return re.sub(r'\n\s*\n', '\n\n', text).strip()

def extract_text_from_docx(docx_path):
    if not Document:
        print("Error: python-docx not installed. Run 'pip install python-docx'")
        return ""
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def extract_rebuttal_structure(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    full_text = ""
    
    if ext == ".pdf":
        doc = fitz.open(file_path)
        for page in doc:
            full_text += page.get_text()
    elif ext == ".docx":
        full_text = extract_text_from_docx(file_path)
    else:
        print(f"Unsupported file type: {ext}")
        return ""
        
    # Heuristic parsing
    lines = full_text.split('\n')
    output_lines = []
    
    current_reviewer = "General"
    output_lines.append(f"# Rebuttal Analysis: {os.path.basename(file_path)}\n")
    
    for line in lines:
        clean = line.strip()
        if not clean: continue
        
        # Detect Reviewer Header
        if re.search(r'Reviewer\s*#?\d+', clean, re.IGNORECASE):
            current_reviewer = clean
            output_lines.append(f"\n## {current_reviewer}")
            continue
            
        # Detect Comment/Response
        if re.match(r'(Comment|Point|Q)\s*\d+[:.]', clean, re.IGNORECASE):
            output_lines.append(f"\n**{clean}**")
        elif re.match(r'(Response|Answer|A)[:.]', clean, re.IGNORECASE):
            output_lines.append(f"\n> **Response**: {clean}")
        else:
            output_lines.append(clean)
            
    return "\n".join(output_lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_rebuttal.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    # Correctly name output file
    output_md = os.path.splitext(file_path)[0] + "_analysis.md"
    
    print(f"Analyzing {file_path}...")
    markdown_content = extract_rebuttal_structure(file_path)
    
    if markdown_content:
        with open(output_md, "w") as f:
            f.write(markdown_content)
            
        print(f"Saved specific analysis to {output_md}")
    else:
        print("No content extracted.")

if __name__ == "__main__":
    main()
