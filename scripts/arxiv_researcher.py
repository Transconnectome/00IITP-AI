import arxiv
import sys
import os
import subprocess

def search_and_download(query, max_results=3, download_dir="docs/02_literature/papers"):
    print(f"--- [Autonomous Agent] Searching arXiv for: '{query}' ---")
    
    # Ensure directory exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    search = arxiv.Search(
        query = query,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.Relevance
    )

    downloaded_files = []

    for result in search.results():
        print(f"Found: {result.title} ({result.published.year})")
        # Sanitize filename
        safe_title = "".join([c for c in result.title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        filename = f"{safe_title}.pdf"
        filepath = os.path.join(download_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Downloading to {filepath}...")
            result.download_pdf(dirpath=download_dir, filename=filename)
            downloaded_files.append(filepath)
        else:
            print(f"File already exists: {filepath}")
            downloaded_files.append(filepath)

    return downloaded_files

def ingest_to_rag(files):
    print("\n--- [Autonomous Agent] Ingesting to RAG ---")
    # Using kb_ingest.py as identified earlier
    # It requires --roots and --force (optional)
    
    # In a real scenario, we might want to be more selective, but for now we re-index the folder
    # Or strict ingestion of specific files if kb_ingest supported it. 
    # Current kb_ingest scans directories.
    
    cmd = ["python3", "scripts/kb_ingest.py", "--roots", "docs/02_literature/papers", "--ext", "pdf", "--force"]
    
    try:
        subprocess.check_call(cmd)
        print("Ingestion Complete.")
    except subprocess.CalledProcessError as e:
        print(f"Ingestion failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/arxiv_researcher.py 'query_string'")
        sys.exit(1)
        
    query = sys.argv[1]
    files = search_and_download(query)
    if files:
        ingest_to_rag(files)
    else:
        print("No papers found or downloaded.")
