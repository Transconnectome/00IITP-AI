import fitz  # pymupdf
import arxiv
import sys
import os
import re
import requests
import subprocess
from urllib.parse import quote

try:
    from docx import Document
except ImportError:
    Document = None

def extract_text_from_docx(docx_path):
    if not Document:
        print("Error: python-docx not installed. Run 'pip install python-docx'")
        return ""
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def extract_references_text(file_path):
    """
    Extracts text from the References section of a PDF or DOCX.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
    elif ext == ".docx":
        full_text = extract_text_from_docx(file_path)
    else:
        print(f"Unsupported file type: {ext}")
        return ""

    # Common headers for references section
    ref_headers = ["References", "REFERENCES", "Bibliography", "BIBLIOGRAPHY", "참고문헌"]
    
    # Try to find the header
    # We look for a line that is exactly one of the headers, or close to it
    lines = full_text.split('\n')
    start_idx = -1
    
    for i, line in enumerate(lines):
        clean_line = line.strip()
        # Remove simple numbering or formatting if present
        clean_line = re.sub(r'^\d+\.?\s*', '', clean_line)
        
        if clean_line in ref_headers:
            start_idx = i
            break
            
    if start_idx != -1:
        print(f"Found References section at line {start_idx}")
        return "\n".join(lines[start_idx:])
    else:
        print("Warning: Could not find explicit 'References' section header. Returning last 20% of text.")
        cut_off = int(len(lines) * 0.8)
        return "\n".join(lines[cut_off:])

def parse_titles(text):
    """
    Parses potential paper titles from the reference text.
    """
    # Normalize
    text = text.replace('\n', ' ')
    
    # Split by reference markers like [1], [2] or 1., 2.
    refs = []
    
    # Try [1] style
    markers = list(re.finditer(r'\[\d+\]', text))
    if len(markers) < 3:
        # Try 1. style (more risky, matches "Fig 1." etc)
        # Look for "1." at start of line (but we merged? No, we have text)
        # Let's try heuristic: Number followed by dot and space, then Capital letter?
        markers = list(re.finditer(r'\s\d+\.\s+[A-Z]', text))
        
    if not markers:
         # Fallback for unnumbered references (e.g. APA)
         # Split by (Year). 
         # Author (Year). Title.
         # Regex for (19\d\d|20\d\d)
         years = list(re.finditer(r'\((19|20)\d{2}[a-z]?\)', text))
         if len(years) > 5:
             # Looks like APA style
             # Split roughly by year? No, year is early in the ref.
             # Split by double newline? (if we had them)
             # Let's return the segments around the years
             for i in range(len(years)):
                 # approximate start/end
                 start = years[i].start() - 50 # Look back for authors
                 end = years[i+1].start() - 50 if i < len(years)-1 else len(text)
                 ref_segment = text[start:end].strip()
                 refs.append(ref_segment)
             return refs
         return []

    # Extract text between markers
    for i in range(len(markers)):
        start_idx = markers[i].end() if markers[i].group().strip().endswith(']') else markers[i].start()
        # For "1. Author", we want to keep the content, but skip the "1. "
        
        end_idx = markers[i+1].start() if i < len(markers) - 1 else len(text)
        ref_segment = text[start_idx:end_idx].strip()
        
        # Cleanup
        ref_segment = re.sub(r'^\d+\.\s*', '', ref_segment)
        refs.append(ref_segment)
        
    return refs

def clean_title_for_search(ref_segment):
    """
    Attempts to extract the most 'title-like' part of a reference string.
    """
    # Remove leading specific chars
    ref_segment = ref_segment.strip(' .[]')
    
    # Heuristic: Title is usually between Author string and Year/Conference.
    # OR: Title is the quoted part
    quoted = re.findall(r'“([^”]+)”', ref_segment)
    if quoted: return quoted[0]
    quoted = re.findall(r'"([^"]+)"', ref_segment)
    if quoted: return quoted[0]

    # Split by period
    parts = ref_segment.split('.')
    # Sort by length descending, pick checking for "validity"
    # (not just a list of names)
    candidates = [p.strip() for p in parts if len(p.strip()) > 15]
    
    if candidates:
        # Avoid the one with year?
        return candidates[0] # Usually the first long segment after authors (if authors are short) or THE long segment
            
    return ref_segment[:200]

def save_abstract_as_pdf(result, output_dir, safe_title):
    try:
        abstract_text = f"Title: {result.title}\n\nAuthors: {', '.join([a.name for a in result.authors])}\n\nAbstract:\n{result.summary}"
        txt_filename = f"{result.published.year}_{safe_title}_Abstract.txt"
        pdf_filename = f"{result.published.year}_{safe_title}_Abstract.pdf"
        txt_path = os.path.join(output_dir, txt_filename)
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(abstract_text)
            
        # Convert to PDF using textutil (macOS built-in)
        subprocess.run(["textutil", "-convert", "pdf", "-output", pdf_path, txt_path], check=True, capture_output=True)
        
        # Cleanup txt
        if os.path.exists(txt_path):
            os.remove(txt_path)
            
        print(f"Saved Abstract: {pdf_filename}")
        return True
    except Exception as e:
        print(f"Error saving abstract for {result.title}: {e}")
        return False

def calculate_similarity(s1, s2):
    """Simple token-based similarity ratio"""
    def tokenize(s):
        return set(re.findall(r'\w+', s.lower()))
    
    t1 = tokenize(s1)
    t2 = tokenize(s2)
    if not t1 or not t2: return 0
    intersection = t1.intersection(t2)
    # Focus on how many of the query tokens are in the result title
    return len(intersection) / len(t1)

def download_arxiv(query, output_dir):
    try:
        search = arxiv.Search(
            query = query,
            max_results = 2, # Check top 2
            sort_by = arxiv.SortCriterion.Relevance
        )
        
        for result in search.results():
            # Verification Step
            similarity = calculate_similarity(query, result.title)
            print(f"   - Match Check: '{result.title[:50]}...' (Score: {similarity:.2f})")
            
            if similarity < 0.3: # Lowered threshold slightly because medical titles might differ a bit but want to stay safe
                print(f"   - Skipping: Similarity too low.")
                continue

            safe_title = "".join([c for c in result.title if c.isalnum() or c==' ']).strip()
            safe_title = safe_title.replace(" ", "_")[:50]
            filename = f"{result.published.year}_{safe_title}.pdf"
            filepath = os.path.join(output_dir, filename)
            
            if os.path.exists(filepath):
                print(f"   - Exists: {filename}")
                return True
                
            try:
                print(f"   - Downloading: {filename}")
                result.download_pdf(dirpath=output_dir, filename=filename)
                return True
            except Exception as e:
                print(f"   - PDF Download failed: {e}. Saving abstract.")
                return save_abstract_as_pdf(result, output_dir, safe_title)

    except Exception as e:
        print(f"Error searching/downloading '{query}': {e}")
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 download_references.py <file_path> [output_dir]")
        sys.exit(1)
        
    file_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "references"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Processing {file_path}...")
    ref_text = extract_references_text(file_path)
    print(f"Extracted approx {len(ref_text)} characters from reference section.")
    
    raw_refs = parse_titles(ref_text)
    print(f"Found {len(raw_refs)} potential references.")
    
    downloaded_count = 0
    for i, ref in enumerate(raw_refs):
        # clean text
        query = clean_title_for_search(ref)
        if len(query) < 10: 
            continue
            
        print(f"[{i+1}/{len(raw_refs)}] Searching: {query[:60]}...")
        if download_arxiv(query, output_dir):
            downloaded_count += 1
            
    print(f"Done. Downloaded {downloaded_count} papers to {output_dir}/")

if __name__ == "__main__":
    main()
