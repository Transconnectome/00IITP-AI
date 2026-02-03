#!/usr/bin/env python3
"""
IITP-AI ChromaDB RAG 구축: docs/ PDF·MD → 청크 → SciBERT 임베딩 → iitp_ai_L0.

설계: docs/06_admin/DESIGN_RAG_NVINGEST_AI_COSCIENTIST.md
Idempotent: 기존 컬렉션 삭제 후 재생성.
"""

import argparse
import json
import logging
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Optional deps
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


def _run(args: List[str], timeout_s: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout_s)


def extract_text_pdf(path: Path) -> str:
    cp = _run(["pdftotext", "-layout", str(path), "-"], timeout_s=120)
    return (cp.stdout or "").strip() if cp.returncode == 0 else ""


def extract_text_md(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace").strip()


def chunk_text(text: str, chunk_size: int = 1024, overlap: int = 150) -> List[str]:
    text = text.strip()
    if not text:
        return []
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paras:
        return [text[:chunk_size]] if text else []

    chunks: List[str] = []
    cur: List[str] = []
    cur_len = 0
    for p in paras:
        add_len = len(p) + (2 if cur else 0)
        if cur and cur_len + add_len > chunk_size:
            chunks.append("\n\n".join(cur))
            overlap_text = "\n\n".join(cur[-2:]) if len(cur) >= 2 else cur[-1]
            overlap_len = min(len(overlap_text), overlap)
            if overlap_len > 0:
                cur = [overlap_text[-overlap_len:].strip() or p]
                cur_len = len(cur[0])
            else:
                cur = [p]
                cur_len = len(p)
        else:
            cur.append(p)
            cur_len += add_len
    if cur:
        chunks.append("\n\n".join(cur))
    return chunks


def path_to_category(rel_path: str, content_lower: str = "") -> str:
    """IITP-AI category from path and optional content keywords."""
    if "00_task_description" in rel_path:
        return "task_description"
    if "02_literature" in rel_path:
        if "neuromorphic" in rel_path or "library" in rel_path:
            return "literature"
        return "literature"
    if "03_proposal" in rel_path:
        return "proposal"
    # Keyword-based for generic paths
    if any(k in content_lower for k in ("sensory encoder", "predictive coding", "jepa", "감각")):
        return "sensory_encoder"
    if any(k in content_lower for k in ("titans memory", "ssm", "mamba", "state space", "기억")):
        return "titans_memory"
    return "general"


def guess_title(path: Path, text: str) -> str:
    if path.suffix.lower() == ".md":
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                return line.lstrip("#").strip() or path.stem
            return line[:120]
    return path.stem


def scan_and_chunk(
    docs_root: Path,
    project_root: Path,
    chunk_size: int = 1024,
    chunk_overlap: int = 150,
    extensions: Tuple[str, ...] = (".pdf", ".md"),
) -> List[dict]:
    """Scan docs_root for PDF/MD, extract text, chunk; return list of {source_path, doc_title, chunk_index, content, category}."""
    out: List[dict] = []
    for ext in extensions:
        for path in docs_root.rglob(f"*{ext}"):
            if not path.is_file():
                continue
            try:
                rel = str(path.relative_to(project_root))
            except ValueError:
                rel = str(path.resolve())

            if ext == ".pdf":
                text = extract_text_pdf(path)
            else:
                text = extract_text_md(path)

            if len(text.strip()) < 50:
                logger.debug("Skip short: %s", rel)
                continue

            title = guess_title(path, text)
            chunks = chunk_text(text, chunk_size=chunk_size, overlap=chunk_overlap)
            for idx, content in enumerate(chunks):
                content_lower = content.lower()
                category = path_to_category(rel, content_lower)
                out.append({
                    "source_path": rel,
                    "doc_title": title,
                    "chunk_index": idx,
                    "content": content,
                    "category": category,
                })
            logger.info("Chunked %s -> %d chunks", rel, len(chunks))
    return out


def load_chunks_jsonl(path: Path) -> List[dict]:
    chunks = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            chunks.append(json.loads(line))
    return chunks


def build_chromadb(
    chunks: List[dict],
    vector_db_dir: Path,
    collection_name: str = "iitp_ai_L0",
    embedding_model: str = "allenai/scibert_scivocab_uncased",
) -> None:
    if not CHROMADB_AVAILABLE:
        raise RuntimeError("chromadb not installed. pip install chromadb")
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        raise RuntimeError("sentence-transformers not installed. pip install sentence-transformers")

    vector_db_dir = Path(vector_db_dir)
    vector_db_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Loading embedding model: %s", embedding_model)
    model = SentenceTransformer(embedding_model)
    texts = [c["content"] for c in chunks]
    logger.info("Embedding %d chunks...", len(texts))
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    client = chromadb.PersistentClient(path=str(vector_db_dir), settings=Settings(anonymized_telemetry=False))
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass
    coll = client.create_collection(
        name=collection_name,
        metadata={"description": "IITP-AI docs chunks (SciBERT 768)"},
    )

    ids = [f"{c['source_path']}_{c['chunk_index']}" for c in chunks]
    metadatas = [
        {
            "source_path": c["source_path"],
            "doc_title": c["doc_title"][:200],
            "chunk_index": c["chunk_index"],
            "category": c["category"],
        }
        for c in chunks
    ]
    coll.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
    logger.info("ChromaDB collection %s: %d documents", collection_name, len(chunks))


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    default_docs = project_root / "docs"
    default_vector_db = project_root / "data" / "vector_db_iitp_ai"

    ap = argparse.ArgumentParser(description="Build IITP-AI ChromaDB RAG (iitp_ai_L0).")
    ap.add_argument("--vector-db", type=Path, default=default_vector_db, help="ChromaDB directory")
    ap.add_argument("--docs-dir", type=str, default="docs", help="Comma-separated dirs to scan (e.g. docs,tmp)")
    ap.add_argument("--chunks-jsonl", type=Path, default=None, help="Use chunks from JSONL instead of scanning")
    ap.add_argument("--chunk-size", type=int, default=1024, help="Chunk size in characters")
    ap.add_argument("--chunk-overlap", type=int, default=150, help="Chunk overlap")
    ap.add_argument("--embedding-model", default="allenai/scibert_scivocab_uncased", help="SentenceTransformer model")
    args = ap.parse_args()

    if args.chunks_jsonl and args.chunks_jsonl.exists():
        logger.info("Loading chunks from %s", args.chunks_jsonl)
        chunks = load_chunks_jsonl(args.chunks_jsonl)
    else:
        docs_dirs = [d.strip() for d in args.docs_dir.split(",") if d.strip()]
        chunks = []
        for d in docs_dirs:
            docs_path = project_root / d if not (Path(d).is_absolute()) else Path(d)
            if not docs_path.exists():
                logger.warning("Docs dir not found: %s (skip)", docs_path)
                continue
            logger.info("Scanning %s", docs_path)
            chunks.extend(
                scan_and_chunk(
                    docs_path,
                    project_root,
                    chunk_size=args.chunk_size,
                    chunk_overlap=args.chunk_overlap,
                )
            )
        if not chunks:
            logger.warning("No chunks from any docs dir. Check --docs-dir=%s", args.docs_dir)
            return 0

    if not chunks:
        logger.warning("No chunks to index.")
        return 0

    try:
        build_chromadb(chunks, args.vector_db, embedding_model=args.embedding_model)
    except Exception as e:
        logger.exception("%s", e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
