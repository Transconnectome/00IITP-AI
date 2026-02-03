import sys
import os
try:
    import pypdf
except ImportError:
    print("Error: pypdf not installed. Run 'pip install pypdf'")
    sys.exit(1)

def parse_pdf(pdf_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        # Get first 5 pages for summary/idea generation
        for page in reader.pages[:5]:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error parsing {pdf_path}: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_pdf_metadata.py <pdf_path>")
        sys.exit(1)
        
    pdf_file = sys.argv[1]
    text = parse_pdf(pdf_file)
    if text:
        output_file = os.path.splitext(pdf_file)[0] + ".txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted partial content to {output_file}")
