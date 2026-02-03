#!/bin/bash
# Pull changes from Overleaf (via export_pkg) to Lab Repo (00IITP-AI)
# This is the PRIMARY sync mechanism for text edits.

echo "⬇️  Pulling changes from Overleaf..."

# 1. Update export_pkg (The Gateway)
cd export_pkg || { echo "❌ 'export_pkg' directory not found!"; exit 1; }
echo ">> [1/3] Git Pull in export_pkg..."
git pull origin main
cd ..

# 2. Copy .tex files BACK to Lab Repo
# We only sync .tex files because .md is now secondary/archived.
echo ">> [2/3] Syncing .tex files to local repo..."
cp -r export_pkg/tex/* tex/

# 3. Commit Lab Repo
echo ">> [3/3] Committing backup to Lab Repo..."
git add tex/
if ! git diff-index --quiet HEAD --; then
    git commit -m "Sync: Received updates from Overleaf"
    # Optional: git push origin main
    echo "✅ Lab Repo updated with latest Overleaf content."
else
    echo "ℹ️  No changes to commit in Lab Repo."
fi

echo "✅ Pull Complete."
