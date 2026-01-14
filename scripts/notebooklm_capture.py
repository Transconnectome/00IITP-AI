import os
import time
import re
from playwright.sync_api import sync_playwright

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs", "02_literature", "notebooklm_kb")
USER_DATA_DIR = os.path.join(SCRIPT_DIR, "chrome_user_data_clean_2")

FALLBACK_URLS = [
    "https://notebooklm.google.com/notebook/644472d6-3a23-45a7-8d7c-7f218e7c14b4",
    "https://notebooklm.google.com/notebook/7acc2737-c783-43ff-af4c-e360ad02cf2c"
]

def ensure_login(page):
    """Check if logged in, otherwise wait for user."""
    print("Checking login status...")
    
    # Check if we are potentially strictly on login page
    if "accounts.google.com" in page.url or "Sign in" in page.title():
        print("\n" + "="*50)
        print("ACTION REQUIRED: Please log in to your Google Account in the browser window.")
        print("The script will wait for you to log in.")
        print("="*50 + "\n")
        
        while True:
            # Check for dashboard indicators
            if "notebooklm.google.com" in page.url:
                 # Minimal check: URL is correct. 
                 # We can also check for "Create new" or assume if user is on this domain they are likely logged in or handling it.
                 if not "accounts.google.com" in page.url:
                     break
            time.sleep(1)
        
        print("Login flow passed! Waiting for dashboard to settle...")
        time.sleep(5)
    else:
        print("Already logged in.")

def sanitize_filename(name):
    s = re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_").strip()
    return s[:50]

def discover_notebooks(page):
    print("Discovering notebooks on dashboard...")
    if "/notebook/" in page.url:
         return [{"url": page.url, "title": "Current_Notebook"}]

    page.goto("https://notebooklm.google.com/", wait_until='domcontentloaded')
    time.sleep(5)
    
    # Scroll
    try:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
    except:
        pass
    
    notebooks = []
    # Broad selector: any links matching /notebook/
    links = page.query_selector_all("a[href*='/notebook/']")
    
    seen_urls = set()
    for link in links:
        href = link.get_attribute("href")
        if not href: continue
        
        url = f"https://notebooklm.google.com{href}" if href.startswith("/") else href
        url = url.split('?')[0]
        
        if url in seen_urls: continue
        seen_urls.add(url)
        
        title = "Untitled_Notebook"
        try:
             txt = link.inner_text().strip()
             if txt: title = txt.split('\n')[0]
        except: pass
        
        notebooks.append({"url": url, "title": title})
        print(f"Found notebook: {title} ({url})")
        
    if not notebooks:
        print("DEBUG: No notebooks found. Dumping dashboard HTML for inspection.")
        try:
            with open("dashboard_miss_debug.html", "w", encoding="utf-8") as f:
                f.write(page.content())
        except: pass
        
    return notebooks

def capture_notebook(page, notebook_meta):
    url = notebook_meta["url"]
    title = notebook_meta["title"]
    safe_title = sanitize_filename(title)
    
    print(f"\nProcessing Notebook: {title}")
    
    notebook_dir = os.path.join(OUTPUT_DIR, safe_title)
    if not os.path.exists(notebook_dir):
        os.makedirs(notebook_dir)
    
    try:
        if page.url != url:
            # Use domcontentloaded which is faster and less prone to waiting forever on tracking pixels
            page.goto(url, wait_until='domcontentloaded', timeout=60000)
            time.sleep(5) 
        
        # 1. Main Page Text
        text_path = os.path.join(notebook_dir, f"content.txt")
        content = page.inner_text("body")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f" - Saved content text")
        
        # 2. HTML Snapshot
        html_path = os.path.join(notebook_dir, "snapshot.html")
        with open(html_path, "w", encoding="utf-8") as f:
                f.write(page.content())
        print(f" - Saved HTML snapshot")

        # 3. Source List Extraction (from text or specific elements)
        # We try to extract list of sources from the content
        sources_path = os.path.join(notebook_dir, "sources_list.txt")
        # Heuristic: Find section "Sources"
        # Since we can't easily click, we rely on the text content usually listing them or the HTML structure.
        # This update focuses on stability first.
        
    except Exception as e:
        print(f"Error processing {title}: {e}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    print("Starting NotebookLM Knowledge Base Builder...")
    
    with sync_playwright() as p:
        # Simple launch
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            viewport={"width": 1280, "height": 900}
        )
        
        if browser.pages:
            page = browser.pages[0]
        else:
            page = browser.new_page()
        
        try:
            page.goto("https://notebooklm.google.com/", wait_until='domcontentloaded')
            ensure_login(page)
            
            notebooks = discover_notebooks(page)
            
            # Fallbacks
            found_urls = {nb['url'] for nb in notebooks}
            for fb_url in FALLBACK_URLS:
                if fb_url not in found_urls:
                    notebooks.append({"url": fb_url, "title": f"Fallback_{fb_url.split('/')[-1][:8]}"})
            
            print(f"Total notebooks to process: {len(notebooks)}")
            
            for nb in notebooks:
                capture_notebook(page, nb)
                
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
        finally:
            print("\nAll done!")
            browser.close()

if __name__ == "__main__":
    main()
