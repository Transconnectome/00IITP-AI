#!/bin/bash
# Sync drafts from Research Repo (00IITP-AI) to Publication Repo (IITP-2026-Proposal)

# 1. Convert latest MD to TeX
python3 scripts/sync_md_to_tex.py

# 2. Setup Export Folder
mkdir -p export_pkg/graphics
mkdir -p export_pkg/src

# 3. Copy files to export_pkg
cp -r tex export_pkg/
cp -r docs/03_proposal/drafts export_pkg/docs/03_proposal/
cp -r src export_pkg/
cp README.md export_pkg/

# 4. Copy Graphics
mkdir -p export_pkg/tex/graphics
if ls docs/05_figures/*.png 1> /dev/null 2>&1; then
    cp docs/05_figures/*.png export_pkg/tex/graphics/
fi

# 5. Commit and Push in Export Repo
cd export_pkg
git add .
git commit -m "Auto-deploy: Updates and Graphics from NeuroX Agent"
git push origin main

echo "✅ Successfully deployed to IITP-2026-Proposal (Overleaf)"
