import PyPDF2
import glob
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def main():
    # Look for email*.pdf in the current directory
    pdf_files = sorted(glob.glob("email*.pdf"))
    
    if not pdf_files:
        print("No email*.pdf files found.")
        return

    for pdf_file in pdf_files:
        print(f"--- START OF {pdf_file} ---")
        content = extract_text_from_pdf(pdf_file)
        print(content)
        print(f"--- END OF {pdf_file} ---\n\n")

if __name__ == "__main__":
    main()
