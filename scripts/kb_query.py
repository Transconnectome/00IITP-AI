import argparse
import sqlite3
from pathlib import Path


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    default_db = project_root / "knowledge_base" / "kb.sqlite"

    ap = argparse.ArgumentParser(description="Query the local SQLite FTS knowledge base.")
    ap.add_argument("query", help="FTS query string (e.g. \"neuromorphic energy\")")
    ap.add_argument("--db", default=str(default_db), help="SQLite DB path (default: knowledge_base/kb.sqlite)")
    ap.add_argument("--limit", type=int, default=10, help="Max results")
    args = ap.parse_args()

    db_path = Path(args.db).resolve()
    if not db_path.exists():
        print(f"DB not found: {db_path}")
        print("Run: python3 scripts/kb_ingest.py")
        return 2

    conn = sqlite3.connect(str(db_path))
    try:
        rows = conn.execute(
            """
            SELECT
              path,
              title,
              snippet(chunks, 4, '[', ']', ' … ', 12) AS snippet,
              bm25(chunks) AS score
            FROM chunks
            WHERE chunks MATCH ?
            ORDER BY score
            LIMIT ?
            """,
            (args.query, args.limit),
        ).fetchall()

        if not rows:
            print("No results.")
            return 0

        for i, (path, title, snippet, score) in enumerate(rows, start=1):
            print(f"{i}. {title}  ({path})")
            print(f"   score: {score:.4f}")
            if snippet:
                print(f"   {snippet}")
            print()
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())


