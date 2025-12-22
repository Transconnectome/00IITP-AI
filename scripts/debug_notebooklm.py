import os
import time
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_DIR = os.path.join(SCRIPT_DIR, "chrome_user_data")

def main():
    print("Starting Debug Dump...")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            viewport={"width": 1400, "height": 1000}
        )
        page = browser.pages[0]
        page.goto("https://notebooklm.google.com/")
        
        # Wait for user to be logged in (heuristic)
        print("Waiting for dashboard...")
        time.sleep(5)
        if "Sign in" in page.title():
             print("Please log in...")
             time.sleep(15) 
        
        # Dump HTML
        content = page.content()
        with open("dashboard_dump.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Dumped dashboard_dump.html")
        
        # Screenshot for good measure
        page.screenshot(path="dashboard_debug.png")
        print("Scenshot saved.")
        
        browser.close()

if __name__ == "__main__":
    main()
