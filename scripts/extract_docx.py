import sys
import os
try:
    from docx import Document
except ImportError:
    print("Error: python-docx not installed. Run 'pip install python-docx'")
    sys.exit(1)

def extract_docx(docx_path):
    if not os.path.exists(docx_path):
        print(f"Error: {docx_path} not found.")
        return None
    
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_docx.py <docx_path>")
        sys.exit(1)
        
    docx_file = sys.argv[1]
    text = extract_docx(docx_file)
    if text:
        output_file = os.path.splitext(docx_file)[0] + ".txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted content to {output_file}")
