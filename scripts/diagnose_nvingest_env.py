#!/usr/bin/env python3
import sys
import os
import socket
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NV-Ingest-Diagnosis")

def check_import():
    try:
        import nv_ingest_client
        print(f"PASS: nv_ingest_client imported successfully. file: {nv_ingest_client.__file__}")
    except ImportError as e:
        print(f"FAIL: nv_ingest_client import failed. Error: {e}")
        return False
    except Exception as e:
        print(f"FAIL: Unexpected error importing nv_ingest_client: {e}")
        return False
    return True

def check_service(host="localhost", port=7671):
    print(f"Checking connection to {host}:{port}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        r = s.connect_ex((host, port))
        s.close()
        if r == 0:
            print(f"PASS: Connection to {host}:{port} successful.")
            return True
        else:
            print(f"FAIL: Connection to {host}:{port} failed with code {r}.")
            return False
    except Exception as e:
        print(f"FAIL: Connection check failed with exception: {e}")
        return False

if __name__ == "__main__":
    print(f"Python executable: {sys.executable}")
    print(f"Environment: {os.environ.get('CONDA_DEFAULT_ENV', 'Unknown')}")
    
    import_ok = check_import()
    service_ok = check_service()
    
    if import_ok and service_ok:
        print("\nALL CHECKS PASSED. The fundamental environment seems okay.")
    else:
        print("\nFUNDAMENTAL CHECKS FAILED.")
