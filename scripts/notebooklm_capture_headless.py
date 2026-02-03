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
    "https://notebooklm.google.com/notebook/644472d6-3a23-45a7-8d7c-7f218e7c14b4"
]

def sanitize_filename(name):
    s = re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_").strip()
    return s[:50]

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
            page.goto(url, wait_until='domcontentloaded', timeout=60000)
            time.sleep(5) 
        
        # 1. Main Page Text
        text_path = os.path.join(notebook_dir, f"content.txt")
        content = page.inner_text("body")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f" - Saved content text to {text_path}")
        
        # 2. HTML Snapshot
        html_path = os.path.join(notebook_dir, "snapshot.html")
        with open(html_path, "w", encoding="utf-8") as f:
                f.write(page.content())
        print(f" - Saved HTML snapshot to {html_path}")
        
    except Exception as e:
        print(f"Error processing {title}: {e}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    print("Starting NotebookLM Knowledge Base Builder (Headless)...")
    
    with sync_playwright() as p:
        # Headless launch
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,  # Set to True for headless execution
            viewport={"width": 1280, "height": 900}
        )
        
        if browser.pages:
            page = browser.pages[0]
        else:
            page = browser.new_page()
        
        try:
            page.goto("https://notebooklm.google.com/", wait_until='domcontentloaded')
            time.sleep(3)
            
            # Check login status
            if "accounts.google.com" in page.url or "Sign in" in page.title():
                print("ERROR: Login required. Cannot proceed in headless mode without valid session.")
                # Dump HTML for debug
                with open("login_fail_debug.html", "w", encoding="utf-8") as f:
                    f.write(page.content())
                return

            print("Login check passed (or skipped). Proceeding to capture...")
            
            # Direct capture of target URL
            target_url = FALLBACK_URLS[0]
            capture_notebook(page, {"url": target_url, "title": "Target_Notebook_644472d6"})
            
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
        finally:
            print("\nAll done!")
            browser.close()

if __name__ == "__main__":
    main()
