#!/usr/bin/env python3
import logging
logging.basicConfig(level=logging.INFO)

print("Importing pipeline runner...")
try:
    from nv_ingest.framework.orchestration.ray.util.pipeline.pipeline_runners import run_pipeline
except ImportError as e:
    print(f"Import failed: {e}")
    exit(1)

print("Starting pipeline (in-process)...")
try:
    # run_in_subprocess=False to keep it in this process and see errors
    run_pipeline(block=False, disable_dynamic_scaling=True, run_in_subprocess=False)
    print("Pipeline started successfully.")
except Exception as e:
    print(f"Pipeline start failed: {e}")
    import traceback
    traceback.print_exc()

print("Done.")
