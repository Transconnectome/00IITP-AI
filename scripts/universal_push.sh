#!/bin/bash
# Universal Sync Script (Overleaf-First Edition)
# Default behavior:
# 1. Pull Text FROM Overleaf (Safe)
# 2. Push Figures TO Overleaf (Safe)
# 3. Backup everything to Lab Repo

echo "🔄 Starting Universal Sync (Overleaf-First)..."

# 1. Pull latest text (The new Source of Truth)
./scripts/pull_from_overleaf.sh

# 2. Upload new figures (if any)
./scripts/upload_figures.sh

# 3. Local Backup Commit
echo ">> Backing up to Lab Repo..."
git add .
if ! git diff-index --quiet HEAD --; then
    git commit -m "Auto-Sync: Sync with Overleaf"
    git push origin main
    echo "✅ Lab Repo synced."
else
    echo "ℹ️  No changes to backup."
fi

echo "🎉 Sync Complete."
