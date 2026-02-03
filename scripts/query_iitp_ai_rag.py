#!/usr/bin/env python3
"""
RAG Query Tool for Agentic Interaction
Usage: python3 scripts/query_iitp_ai_rag.py "What is the role of Titans memory?"
"""

import argparse
import sys
from pathlib import Path
try:
    import chromadb
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Error: Missing dependencies. pip install chromadb sentence-transformers")
    sys.exit(1)

def query_rag(query_text: str, vector_db_path: Path, n_results: int = 5):
    if not vector_db_path.exists():
        print(f"Error: Vector DB not found at {vector_db_path}")
        return

    # Load Model (Same as Build)
    model_name = "allenai/scibert_scivocab_uncased"
    try:
        model = SentenceTransformer(model_name)
    except Exception as e:
        # Fallback if specific model fails (though it should be cached)
        print(f"Warning: Could not load {model_name}, using default. Error: {e}")
        model = SentenceTransformer("all-MiniLM-L6-v2")

    # Embed Query
    query_embedding = model.encode([query_text]).tolist()

    # Query DB
    client = chromadb.PersistentClient(path=str(vector_db_path))
    coll = client.get_collection("iitp_ai_L0")

    results = coll.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )

    print(f"\n=== Query: {query_text} ===\n")
    if not results["documents"]:
        print("No results found.")
        return

    for i, (doc, meta, dist) in enumerate(zip(results["documents"][0], results["metadatas"][0], results["distances"][0])):
        print(f"--- Result {i+1} (Dist: {dist:.4f}) ---")
        print(f"Source: {meta.get('source_path', 'N/A')}")
        print(f"Title: {meta.get('doc_title', 'N/A')}")
        print(f"Content Snippet: {doc[:300]}...")
        print("------------------------------------------\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query IITP-AI RAG")
    parser.add_argument("query", type=str, help="Question to ask")
    parser.add_argument("--db", type=str, default="data/vector_db_iitp_ai", help="Path to ChromaDB")
    
    args = parser.parse_args()
    query_rag(args.query, Path(args.db))
