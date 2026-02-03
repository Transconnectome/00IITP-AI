#!/bin/bash
# Universal Sync Script
# Updates BOTH the Research Hub (00IITP-AI) and the Proposal Export (IITP-2026-Proposal)

echo "🚀 Starting Universal Sync..."

# 0. Pre-flight Validation
python3 scripts/validate_sync.py
if [ $? -ne 0 ]; then
    echo "❌ Validation Failed. Fix errors before syncing."
    exit 1
fi

# 1. Deploy to Overleaf Repo (Proposal Only)
echo ">> [1/2] Syncing to Overleaf (IITP-2026-Proposal)..."
./scripts/deploy_to_overleaf.sh

# 2. Sync Local Research Repo (Full Context)
echo ">> [2/2] Syncing Research Hub (00IITP-AI)..."
git add .
# Commit only if changes exist
if ! git diff-index --quiet HEAD --; then
    git commit -m "Auto-Sync: Unified update for Drafts and Figures"
    git push origin main
    echo "✅ Research Hub updated."
else
    echo "ℹ️  No changes to commit in Research Hub."
fi

echo "🎉 Universal Sync Complete! Both repositories are up to date."
