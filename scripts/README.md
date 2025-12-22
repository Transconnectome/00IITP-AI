# Scripts Directory

This directory contains automation scripts for the project.

## notebooklm_capture.py

This script automates the capture of NotebookLM notebooks into the `docs/03_proposal/references/notebooklm` directory.

### Prerequisites

1. Python 3.8+
2. Playwright

### Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

### Usage

```bash
python notebooklm_capture.py
```

### Notes

- The script runs in **headed** mode (visible browser) initially to allow you to log in to your Google Account.
- Login state is saved in `scripts/chrome_user_data`, so subsequent runs might skip login.
- Outputs (HTML, PNG, TXT) are saved to `docs/03_proposal/references/notebooklm`.

## KB (knowledge base)

로컬에서 `docs/` 자료를 전문검색(FTS) 가능한 형태로 만들기 위한 스크립트입니다.

- 인덱싱: `python3 scripts/kb_ingest.py`
- 검색: `python3 scripts/kb_query.py "your query"`

