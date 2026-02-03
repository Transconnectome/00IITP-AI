#!/usr/bin/env python3
import sys
import os
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NV-Ingest-Process-Test")

def test_ingestion():
    try:
        from nv_ingest_api.util.message_brokers.simple_message_broker import SimpleClient
        from nv_ingest_client.client import Ingestor, NvIngestClient
    except ImportError as e:
        logger.error(f"Import failed: {e}")
        return

    file_path = "dummy_ingest_test.txt"
    if not os.path.exists(file_path):
        logger.error(f"Test file {file_path} not found.")
        return

    logger.info("Initializing NvIngestClient...")
    client = NvIngestClient(
        message_client_allocator=SimpleClient,
        message_client_port=7671,
        message_client_hostname="localhost",
    )
    
    logger.info(f"Submitting {file_path} for ingestion...")
    ingestor = (
        Ingestor(client=client)
        .files([file_path])
        .extract(extract_text=True, extract_tables=False, extract_charts=False)
        .split(chunk_size=1024, chunk_overlap=150)
    )

    try:
        results, failures = ingestor.ingest(show_progress=True, return_failures=True)
        if failures:
            logger.error("Ingestion reported failures:")
            for f in failures:
                logger.error(f)
        
        if results:
            logger.info(f"Ingestion successful. Received {len(results)} results.")
            for res in results: 
                # Decode or print snippet
                print(f"Result snippet: {str(res)[:200]}")
        else:
            logger.warning("Ingestion finished but returned no results.")

    except Exception as e:
        logger.error(f"Ingestion process threw exception: {e}")

if __name__ == "__main__":
    test_ingestion()
