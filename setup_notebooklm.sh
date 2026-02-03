#!/bin/bash
source .venv/bin/activate
echo "Starting NotebookLM MCP initialization (Attempt 2 with fixed dependencies)..."
echo "A browser window will open. Please log in to your Google account."
echo "IMPORTANT: After logging in, verify you can see the notebook content."
echo "Then return to this terminal and press Enter."
notebooklm-mcp init https://notebooklm.google.com/notebook/7acc2737-c783-43ff-af4c-e360ad02cf2c
