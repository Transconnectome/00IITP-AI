---
description: Connects to dgx-spark k-bfm context, runs tasks, and retrieves results.
---
# k-bfm Execution Workflow

This workflow automates the context setup for working on the `k-bfm` project on the `dgx-spark` server.

## Step 1: Context Switching
Navigate to the project root and verify the environment.

```bash
cd /home/juke/git/k-bfm
echo "Current Directory: $(pwd)"
echo "Checking Git Status..."
git status -sb
```

## Step 2: Environment Check
Ensure strict python path and environment variables are set (crucial for NV-Ingest/RAG tasks).

```bash
# Check for .env file
ls -la .env
# Verify python path
echo $PYTHONPATH
```

## Step 3: Script Discovery
List available automation scripts in the project.

```bash
echo "Available Python Scripts:"
find . -maxdepth 2 -name "*.py" | grep -v "venv" | grep -v "tests"
```

## Step 4: Execution & Results
User should execute their specific command here.
Common commands:
- `python run_coscientist.py` (AI-CoScientist Main Loop)
- `python scripts/ingest_data.py` (RAG Ingestion)

**Result Retrieval:**
Outputs are typically found in:
- `/home/juke/git/k-bfm/output/`
- `/home/juke/git/k-bfm/docs/`

```bash
echo "Recent Outputs:"
ls -lt output/ | head -n 5
```
