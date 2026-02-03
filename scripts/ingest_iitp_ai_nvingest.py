#!/usr/bin/env python3
"""
00IITP-AI 문서 → nv-ingest(선택) 또는 로컬 추출 → 청크 JSONL → build_iitp_ai_rag 호출.

nv-ingest 서비스가 없으면 build_iitp_ai_rag.py만 실행 (docs/ 스캔).
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def _nv_ingest_available(host: str, port: int) -> bool:
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        r = s.connect_ex((host, port))
        s.close()
        return r == 0
    except Exception:
        return False


def run_build_script(
    vector_db: Path,
    project_root: Path,
    chunks_jsonl: Optional[Path] = None,
    docs_dirs: Optional[str] = None,
) -> int:
    """Invoke build_iitp_ai_rag.py. docs_dirs: comma-separated e.g. 'docs,tmp'."""
    script = project_root / "scripts" / "build_iitp_ai_rag.py"
    if not script.exists():
        logger.error("Not found: %s", script)
        return 2
    cmd = [sys.executable, str(script), "--vector-db", str(vector_db)]
    if chunks_jsonl and chunks_jsonl.exists():
        cmd += ["--chunks-jsonl", str(chunks_jsonl)]
    elif docs_dirs:
        cmd += ["--docs-dir", docs_dirs]
    logger.info("Run: %s", " ".join(cmd))
    r = subprocess.run(cmd, cwd=str(project_root))
    return r.returncode


def try_nv_ingest(
    pdf_paths: List[Path],
    host: str,
    port: int,
    output_jsonl: Path,
    project_root: Path,
) -> bool:
    """Call nv-ingest client; write chunks to output_jsonl. Returns True if success."""
    try:
        from nv_ingest_api.util.message_brokers.simple_message_broker import SimpleClient
        from nv_ingest_client.client import Ingestor, NvIngestClient
    except ImportError as e:
        logger.warning("nv-ingest client not available: %s", e)
        return False

    if not pdf_paths:
        return False

    client = NvIngestClient(
        message_client_allocator=SimpleClient,
        message_client_port=port,
        message_client_hostname=host,
    )
    paths_str = [str(p) for p in pdf_paths]
    ingestor = (
        Ingestor(client=client)
        .files(paths_str)
        .extract(
            extract_text=True,
            extract_tables=True,
            extract_charts=True,
            table_output_format="markdown",
            text_depth="page",
        )
        .split(chunk_size=1024, chunk_overlap=150)
    )
    # No .embed() — we use SciBERT in build_iitp_ai_rag for k-bfm compatibility
    try:
        results, failures = ingestor.ingest(show_progress=True, return_failures=True)
    except Exception as e:
        logger.warning("nv-ingest ingest failed: %s", e)
        return False

    # Convert results to our JSONL format (source_path, doc_title, chunk_index, content, category)
    try:
        from nv_ingest_client.util.process_json_files import ingest_json_results_to_blob
    except ImportError:
        ingest_json_results_to_blob = None

    out_chunks: List[dict] = []
    for i, (path, res) in enumerate(zip(pdf_paths, results)):
        try:
            rel = str(path.relative_to(project_root))
        except ValueError:
            rel = str(path)
        title = path.stem
        if ingest_json_results_to_blob is not None:
            try:
                blob = ingest_json_results_to_blob(res)
                if isinstance(blob, dict) and "chunks" in blob:
                    for idx, ch in enumerate(blob["chunks"]):
                        content = ch.get("text", ch.get("content", "")) if isinstance(ch, dict) else str(ch)
                        out_chunks.append({
                            "source_path": rel,
                            "doc_title": title,
                            "chunk_index": idx,
                            "content": content,
                            "category": "literature" if "02_literature" in rel else "general",
                        })
                elif isinstance(blob, list):
                    for idx, item in enumerate(blob):
                        content = item.get("text", item.get("content", str(item))) if isinstance(item, dict) else str(item)
                        out_chunks.append({
                            "source_path": rel,
                            "doc_title": title,
                            "chunk_index": idx,
                            "content": content,
                            "category": "literature" if "02_literature" in rel else "general",
                        })
            except Exception as e:
                logger.debug("Parse result for %s: %s", path, e)
        else:
            # Fallback: assume res is list of chunk dicts
            if isinstance(res, list):
                for idx, item in enumerate(res):
                    c = item.get("text", item.get("content", str(item))) if isinstance(item, dict) else str(item)
                    out_chunks.append({
                        "source_path": rel,
                        "doc_title": title,
                        "chunk_index": idx,
                        "content": c,
                        "category": "literature" if "02_literature" in rel else "general",
                    })

    if not out_chunks:
        logger.warning("No chunks parsed from nv-ingest results; fallback to local build.")
        return False

    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with output_jsonl.open("w", encoding="utf-8") as f:
        for c in out_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    logger.info("Wrote %d chunks to %s", len(out_chunks), output_jsonl)
    return True


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    default_vector_db = project_root / "data" / "vector_db_iitp_ai"

    ap = argparse.ArgumentParser(description="IITP-AI ingest: nv-ingest or local → ChromaDB (docs+tmp)")
    ap.add_argument("--pdf-list", type=Path, help="File with one PDF path per line")
    ap.add_argument("--vector-db", type=Path, default=default_vector_db, help="ChromaDB directory")
    ap.add_argument("--nv-host", default="localhost", help="nv-ingest host")
    ap.add_argument("--nv-port", type=int, default=7671, help="nv-ingest HTTP port")
    ap.add_argument("--output-jsonl", type=Path, default=None, help="Chunks JSONL (default: tmp/iitp_ai_chunks.jsonl)")
    ap.add_argument("--skip-nvingest", action="store_true", help="Skip nv-ingest, run local build only")
    args = ap.parse_args()

    output_jsonl = args.output_jsonl or project_root / "tmp" / "iitp_ai_chunks.jsonl"
    pdf_paths: List[Path] = []
    if args.pdf_list and args.pdf_list.exists():
        for line in args.pdf_list.read_text(encoding="utf-8").splitlines():
            p = line.strip()
            if not p or p.startswith("#"):
                continue
            path = Path(p)
            if not path.is_absolute():
                path = project_root / path
            if path.exists():
                pdf_paths.append(path)
        logger.info("Loaded %d PDFs from %s", len(pdf_paths), args.pdf_list)

    used_nvingest = False
    if not args.skip_nvingest and pdf_paths and _nv_ingest_available(args.nv_host, args.nv_port):
        logger.info("Trying nv-ingest at %s:%s", args.nv_host, args.nv_port)
        if try_nv_ingest(pdf_paths, args.nv_host, args.nv_port, output_jsonl, project_root):
            used_nvingest = True

    if used_nvingest:
        return run_build_script(args.vector_db, project_root, chunks_jsonl=output_jsonl)
    # Local path: scan docs + tmp
    return run_build_script(args.vector_db, project_root, docs_dirs="docs,tmp")


if __name__ == "__main__":
    sys.exit(main())
