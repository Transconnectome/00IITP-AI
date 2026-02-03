#!/usr/bin/env python3
"""
IITP-AI Ingestion Script (Library Mode)
Runs NV-Ingest locally using the user's installed python package, bypassing Docker registry issues.
Supports .env for NVIDIA_API_KEY configuration.
"""

import sys
import os
import json
import logging
import argparse
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("NV-Ingest-Library")

def main():
    parser = argparse.ArgumentParser(description="Ingest PDFs to JSONL using NV-Ingest Library Mode")
    parser.add_argument("--pdf-list", type=Path, help="Path to file containing list of PDFs")
    parser.add_argument("--file", type=Path, help="Single PDF/File to ingest")
    parser.add_argument("--output-jsonl", type=Path, default="iitp_ai_chunks_library.jsonl", help="Output JSONL file")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(), help="Project root for relative paths")
    args = parser.parse_args()

    # --- File Selection ---
    files_to_ingest = []
    if args.file:
        files_to_ingest.append(args.file)
    if args.pdf_list and args.pdf_list.exists():
        with open(args.pdf_list, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    files_to_ingest.append(Path(line))

    if not files_to_ingest:
        logger.error("No files specified. Use --file or --pdf-list.")
        return

    valid_files = [f for f in files_to_ingest if f.exists()]
    if not valid_files:
        logger.error("No valid existing files found.")
        return
    
    logger.info(f"Preparing to ingest {len(valid_files)} files...")

    # --- Config & Env ---
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        logger.warning("python-dotenv not found, ensure environment variables are set.")

    api_key = os.getenv("NVIDIA_API_KEY")
    use_nim = bool(api_key and "nvapi-" in api_key)
    if use_nim:
        logger.info("NVIDIA_API_KEY found. Advanced Table/Chart extraction ENABLED.")
    else:
        logger.warning("NVIDIA_API_KEY not found. Advanced extraction DISABLED (Text-only).")

    # --- Library Mode Setup ---
    try:
        from nv_ingest.framework.orchestration.ray.util.pipeline.pipeline_runners import run_pipeline
        from nv_ingest_api.util.message_brokers.simple_message_broker import SimpleClient
        from nv_ingest_client.client import Ingestor, NvIngestClient
    except ImportError as e:
        logger.error(f"Failed to import NV-Ingest library components: {e}")
        return

    # Start local pipeline in-process
    logger.info("Starting local NV-Ingest pipeline...")
    # run_in_subprocess=False prevents segfaults on exit in some envs
    try:
        run_pipeline(block=False, disable_dynamic_scaling=True, run_in_subprocess=False)
    except Exception as e:
        logger.error(f"Failed to start pipeline: {e}")
        return

    client = NvIngestClient(
        message_client_allocator=SimpleClient,
        message_client_port=7671,
        message_client_hostname="localhost",
    )

    ingestor = (
        Ingestor(client=client)
        .files([str(p) for p in valid_files])
        .extract(
            extract_text=True,
            extract_tables=use_nim,
            extract_charts=use_nim,
            table_output_format="markdown",
            text_depth="page",
        )
        .split(chunk_size=1024, chunk_overlap=150)
    )

    logger.info("Submitting jobs...")
    try:
        results, failures = ingestor.ingest(show_progress=True, return_failures=True)
        
        if failures:
            logger.warning(f"{len(failures)} failures reported.")
            for f in failures:
                logger.warning(f"Failure: {f}")

        # Helper import
        try:
            from nv_ingest_client.util.process_json_files import ingest_json_results_to_blob
        except ImportError:
            ingest_json_results_to_blob = None

        out_chunks = []
        for path, res in zip(valid_files, results):
            try:
                rel_path = str(path.relative_to(args.project_root))
            except ValueError:
                rel_path = str(path)
            
            title = path.stem
            chunks_list = []
            
            # Robust parsing strategy
            if isinstance(res, dict) and "chunks" in res:
                chunks_list = res["chunks"]
            elif isinstance(res, list):
                chunks_list = res
            elif ingest_json_results_to_blob:
                 blob = ingest_json_results_to_blob(res)
                 if isinstance(blob, dict) and "chunks" in blob:
                     chunks_list = blob["chunks"]
                 elif isinstance(blob, list):
                     chunks_list = blob

            for idx, c in enumerate(chunks_list):
                content = ""
                if isinstance(c, dict):
                    content = c.get("text") or c.get("content") or ""
                else:
                    content = str(c)
                
                out_chunks.append({
                    "source_path": rel_path,
                    "doc_title": title,
                    "chunk_index": idx,
                    "content": content,
                    "category": "literature" if "02_literature" in rel_path else "general"
                })

        # Write output
        with open(args.output_jsonl, 'w', encoding='utf-8') as f:
            for c in out_chunks:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        
        logger.info(f"Successfully processed {len(valid_files)} files.")
        logger.info(f"Wrote {len(out_chunks)} chunks to {args.output_jsonl}")

    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
