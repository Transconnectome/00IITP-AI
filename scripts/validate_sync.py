#!/usr/bin/env python3
import os
import sys

def check_file(path, description):
    if not os.path.exists(path):
        print(f"❌ MISSING: {description} not found at {path}")
        return False
    # print(f"✅ FOUND: {description}")
    return True

def check_content(path, keyword, description):
    if not os.path.exists(path):
        return False
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if keyword not in content:
        print(f"❌ INVALID: {description} missing keyword '{keyword}' in {path}")
        return False
    # print(f"✅ VALID: {description} contains '{keyword}'")
    return True

def main():
    print("🔍 [Pre-flight Check] Verifying Sync Integrity...")
    errors = 0
    
    # 1. Check References
    if not check_file("tex/references.bib", "Bibliography File"): errors += 1
    
    # 2. Check Main TeX Config
    if not check_content("tex/main.tex", "\\bibliography{references}", "Main TeX Bibliography"): errors += 1
    if not check_content("tex/main.tex", "\\graphicspath", "Main TeX Graphicspath"): errors += 1

    # 3. Check README Link
    if not check_content("README.md", "overleaf.com", "README Overleaf Link"): errors += 1

    # 4. Check Figures (Sample)
    if not check_file("docs/05_figures/dual_encoder_titans_architecture.png", "Core Arch Figure"): 
        print("⚠️ Warning: Core Arch Figure missing in docs/05_figures.")
        # Not a fatal error, maybe just renamed

    if errors > 0:
        print(f"🚨 FAILED: Found {errors} critical issues. Sync aborted.")
        sys.exit(1)
    
    print("✅ System Healthy. Proceeding to Sync.")
    sys.exit(0)

if __name__ == "__main__":
    main()
