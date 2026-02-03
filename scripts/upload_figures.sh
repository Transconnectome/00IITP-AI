#!/bin/bash
# Upload Figures Only to Overleaf
# USE THIS to update graphics without overwriting text edits in Overleaf.

echo "🖼️  Starting Figure Upload..."

# 1. Validation
if [ ! -d "docs/05_figures" ]; then
    echo "❌ Source directory 'docs/05_figures' not found."
    exit 1
fi

if [ ! -d "export_pkg/tex/graphics" ]; then
    echo "Creating graphics directory in export_pkg..."
    mkdir -p export_pkg/tex/graphics
fi

# 2. Sync Figures
echo ">> [1/2] Copying figures to export_pkg..."
cp docs/05_figures/*.png export_pkg/tex/graphics/

# 3. Push to Overleaf
echo ">> [2/2] Pushing to Overleaf..."
cd export_pkg || exit
git add tex/graphics/
git commit -m "Assets: Update figures from Lab Repo"
git push origin main

echo "✅ Figures uploaded successfully."
