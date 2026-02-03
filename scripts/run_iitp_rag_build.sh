#!/usr/bin/env bash
# Idempotent: 00IITP-AI docs PDF → nv-ingest → ChromaDB (IITP-AI RAG) 구축
# 설계: docs/06_admin/DESIGN_RAG_NVINGEST_AI_COSCIENTIST.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VECTOR_DB_DIR="${IITP_AI_VECTOR_DB:-$PROJECT_ROOT/data/vector_db_iitp_ai}"
NVINGEST_HOST="${NVINGEST_HOST:-localhost}"
NVINGEST_PORT="${NVINGEST_PORT:-7671}"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

# --- 1. 디렉터리 확인 ---
log "Project root: $PROJECT_ROOT"
log "Vector DB dir: $VECTOR_DB_DIR"

if [[ ! -d "$PROJECT_ROOT/docs" ]]; then
    log "ERROR: docs/ not found. Abort."
    exit 1
fi

mkdir -p "$VECTOR_DB_DIR"
log "Vector DB directory ready: $VECTOR_DB_DIR"

# --- 2. PDF 목록 수집 (docs + tmp) ---
PDF_LIST="$PROJECT_ROOT/tmp/iitp_ai_pdf_list.txt"
mkdir -p "$(dirname "$PDF_LIST")"
find "$PROJECT_ROOT/docs" "$PROJECT_ROOT/tmp" -type f -name "*.pdf" 2>/dev/null | sort -u > "$PDF_LIST"
PDF_COUNT=$(wc -l < "$PDF_LIST")
log "Found $PDF_COUNT PDFs under docs/ + tmp/"

if [[ "$PDF_COUNT" -eq 0 ]]; then
    log "No PDFs found. Skip ingest. You can run kb_ingest.py for existing MD/txt."
    exit 0
fi

# --- 3. nv-ingest 서비스 연결 확인 (선택) ---
if command -v nc &>/dev/null; then
    if ! nc -z "$NVINGEST_HOST" "$NVINGEST_PORT" 2>/dev/null; then
        log "WARN: nv-ingest not reachable at $NVINGEST_HOST:$NVINGEST_PORT. Run ingest step manually when service is up."
        log "Tip: docker-compose -f /path/to/docker-compose.nv-ingest.yml up -d"
    fi
fi

# --- 4. Python 빌드 스크립트 호출 (있으면) ---
BUILD_SCRIPT="$SCRIPT_DIR/build_iitp_ai_rag.py"
INGEST_SCRIPT="$SCRIPT_DIR/ingest_iitp_ai_nvingest.py"

if [[ -x "$SCRIPT_DIR/venv/bin/python" ]]; then
    PYTHON="$SCRIPT_DIR/venv/bin/python"
elif [[ -n "${VIRTUAL_ENV:-}" ]]; then
    PYTHON="${VIRTUAL_ENV}/bin/python"
else
    PYTHON="python3"
fi

if [[ -f "$INGEST_SCRIPT" ]]; then
    log "Running ingest script: $INGEST_SCRIPT"
    "$PYTHON" "$INGEST_SCRIPT" \
        --pdf-list "$PDF_LIST" \
        --vector-db "$VECTOR_DB_DIR" \
        --nv-host "$NVINGEST_HOST" \
        --nv-port "$NVINGEST_PORT" \
        || log "WARN: ingest script failed (exit $?). Fix and re-run."
elif [[ -f "$BUILD_SCRIPT" ]]; then
    log "Running build script (docs+tmp, no nv-ingest): $BUILD_SCRIPT"
    "$PYTHON" "$BUILD_SCRIPT" --vector-db "$VECTOR_DB_DIR" --docs-dir "docs,tmp" || true
else
    log "No build_iitp_ai_rag.py or ingest_iitp_ai_nvingest.py found. Create them per design doc."
    log "Quick test: python scripts/kb_query.py 'SSM sensory' --db knowledge_base/kb.sqlite"
fi

log "Done. Vector DB path: $VECTOR_DB_DIR"
