import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


class _HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []
        self._skip_depth = 0  # inside <script>/<style>

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data):
        if self._skip_depth:
            return
        text = data.strip()
        if text:
            self._parts.append(text)

    def text(self) -> str:
        return "\n".join(self._parts)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _run(args: list[str], timeout_s: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout_s,
    )


def _pdfinfo(pdf_path: Path) -> dict:
    cp = _run(["pdfinfo", str(pdf_path)], timeout_s=60)
    if cp.returncode != 0:
        return {}
    meta: dict[str, object] = {}
    for line in cp.stdout.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        if k == "Pages":
            try:
                meta["pages"] = int(v)
            except Exception:
                pass
        elif k == "Title":
            if v:
                meta["title"] = v
        elif k == "File size":
            meta["file_size_human"] = v
    return meta


def _extract_text_md_or_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _extract_text_html(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    parser = _HTMLTextExtractor()
    parser.feed(raw)
    return parser.text()


def _extract_text_pdf_pdftotext(path: Path) -> str:
    cp = _run(["pdftotext", "-layout", str(path), "-"], timeout_s=120)
    if cp.returncode != 0:
        return ""
    return cp.stdout or ""


def _ocr_pdf(path: Path, lang: str, dpi: int) -> tuple[str, dict]:
    """
    OCR a (likely image-based) PDF via:
    - pdftoppm -> PNG pages
    - tesseract -> text per page
    """
    meta: dict[str, object] = {"ocr_lang": lang, "ocr_dpi": dpi}
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        prefix = td_path / "page"

        cp = _run(["pdftoppm", "-r", str(dpi), "-png", str(path), str(prefix)], timeout_s=600)
        if cp.returncode != 0:
            meta["ocr_error"] = cp.stderr.strip() or "pdftoppm failed"
            return "", meta

        images = sorted(td_path.glob("page-*.png"))
        if not images:
            meta["ocr_error"] = "no images produced by pdftoppm"
            return "", meta

        parts: list[str] = []
        for img in images:
            # Use a conservative PSM; many docs are multi-line blocks.
            t = _run(
                ["tesseract", str(img), "stdout", "-l", lang, "--psm", "6"],
                timeout_s=600,
            )
            if t.returncode != 0:
                meta.setdefault("ocr_page_errors", []).append(
                    {"image": img.name, "error": (t.stderr or "").strip() or "tesseract failed"}
                )
                continue
            if t.stdout:
                parts.append(t.stdout)

        return ("\n\n".join(parts)).strip(), meta


def _guess_title(path: Path, extracted_text: str) -> str:
    if path.suffix.lower() == ".md":
        for line in extracted_text.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                return line.lstrip("#").strip() or path.stem
            return line[:120]
    return path.stem


def _tags_for_path(rel_path: str) -> str:
    tags: list[str] = []
    if rel_path.startswith("docs/00_task_description/"):
        tags += ["task_description"]
    if rel_path.startswith("docs/02_literature/"):
        tags += ["literature"]
        if "/briefings/" in rel_path:
            tags += ["briefing"]
        if "/papers/" in rel_path:
            tags += ["paper"]
        if "/reading-notes/" in rel_path:
            tags += ["reading_note"]
    if rel_path.startswith("docs/03_proposal/"):
        tags += ["proposal"]
        if "/references/" in rel_path:
            tags += ["reference"]
        if "/notebooklm/" in rel_path:
            tags += ["notebooklm"]
        if "/proposals/" in rel_path:
            tags += ["proposal_reference"]
    if rel_path.startswith("scripts/"):
        tags += ["automation"]
    return ",".join(dict.fromkeys(tags))  # stable dedupe


def _chunk_text(text: str, chunk_chars: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paras:
        return [text[:chunk_chars]]

    chunks: list[str] = []
    cur: list[str] = []
    cur_len = 0
    for p in paras:
        add_len = len(p) + (2 if cur else 0)
        if cur and cur_len + add_len > chunk_chars:
            chunks.append("\n\n".join(cur))
            cur = [p]
            cur_len = len(p)
        else:
            cur.append(p)
            cur_len += add_len
    if cur:
        chunks.append("\n\n".join(cur))
    return chunks


def _init_db(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sources (
          path TEXT PRIMARY KEY,
          sha256 TEXT NOT NULL,
          mtime REAL NOT NULL,
          size INTEGER NOT NULL,
          title TEXT,
          kind TEXT NOT NULL,
          needs_ocr INTEGER NOT NULL DEFAULT 0,
          indexed_at TEXT NOT NULL,
          meta_json TEXT
        )
        """
    )
    # path/title/tags are stored for display/filtering; content is indexed.
    conn.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks
        USING fts5(
          path UNINDEXED,
          title,
          tags,
          chunk_index UNINDEXED,
          content,
          tokenize='unicode61'
        )
        """
    )


def _should_index(existing_row: tuple | None, sha: str, mtime: float, force: bool) -> bool:
    if force or existing_row is None:
        return True
    old_sha, old_mtime = existing_row
    return not (old_sha == sha and float(old_mtime) == float(mtime))


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    default_db = project_root / "knowledge_base" / "kb.sqlite"
    default_roots = [
        project_root / "docs" / "00_task_description" / "parsed",
        project_root / "docs" / "02_literature",
        project_root / "docs" / "03_proposal" / "references",
    ]

    ap = argparse.ArgumentParser(description="Build a local SQLite FTS knowledge base index.")
    ap.add_argument("--db", default=str(default_db), help="SQLite DB path (default: knowledge_base/kb.sqlite)")
    ap.add_argument(
        "--roots",
        default=",".join(str(p) for p in default_roots),
        help="Comma-separated root directories to scan",
    )
    ap.add_argument(
        "--ext",
        default="md,txt,pdf,html,htm",
        help="Comma-separated file extensions to include (no dots)",
    )
    ap.add_argument("--chunk-chars", type=int, default=3000, help="Chunk size (characters)")
    ap.add_argument("--force", action="store_true", help="Re-index all files")
    ap.add_argument("--ocr", action="store_true", help="Attempt OCR for image-based PDFs")
    ap.add_argument("--ocr-lang", default="eng", help="Tesseract language(s), e.g. 'eng' or 'kor+eng'")
    ap.add_argument("--ocr-dpi", type=int, default=200, help="DPI for pdftoppm during OCR")
    args = ap.parse_args()

    exts = {("." + e.strip().lower()).replace("..", ".") for e in args.ext.split(",") if e.strip()}

    db_path = Path(args.db).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    try:
        _init_db(conn)

        roots: list[Path] = [Path(p.strip()).resolve() for p in args.roots.split(",") if p.strip()]
        candidates: list[Path] = []
        for r in roots:
            if not r.exists():
                continue
            for p in r.rglob("*"):
                if p.is_file() and p.suffix.lower() in exts:
                    candidates.append(p)
        candidates.sort(key=lambda p: str(p))

        indexed = 0
        skipped = 0
        needs_ocr = 0
        errors = 0

        for path in candidates:
            try:
                rel_path = str(path.resolve().relative_to(project_root))
            except Exception:
                # Fallback: store absolute path if outside the project root.
                rel_path = str(path.resolve())

            st = path.stat()
            sha = _sha256(path)

            existing = conn.execute(
                "SELECT sha256, mtime FROM sources WHERE path = ?",
                (rel_path,),
            ).fetchone()
            if not _should_index(existing, sha, st.st_mtime, args.force):
                skipped += 1
                continue

            kind = path.suffix.lower().lstrip(".")
            meta: dict[str, object] = {"source_rel_path": rel_path}

            extracted_text = ""
            needs_ocr_flag = 0

            if kind in ("md", "txt"):
                extracted_text = _extract_text_md_or_txt(path)
            elif kind in ("html", "htm"):
                extracted_text = _extract_text_html(path)
            elif kind == "pdf":
                meta.update(_pdfinfo(path))
                extracted_text = _extract_text_pdf_pdftotext(path)
                if len(extracted_text.strip()) < 50:
                    needs_ocr_flag = 1
                    if args.ocr:
                        ocr_text, ocr_meta = _ocr_pdf(path, lang=args.ocr_lang, dpi=args.ocr_dpi)
                        meta.update(ocr_meta)
                        if ocr_text:
                            extracted_text = ocr_text
                            needs_ocr_flag = 0
            else:
                # Unknown kind (shouldn't happen due to filtering)
                extracted_text = ""

            if needs_ocr_flag:
                needs_ocr += 1

            title = _guess_title(path, extracted_text)
            tags = _tags_for_path(rel_path)

            # Rebuild chunks for this path
            conn.execute("DELETE FROM chunks WHERE path = ?", (rel_path,))

            chunks = _chunk_text(extracted_text, chunk_chars=args.chunk_chars)
            for idx, chunk in enumerate(chunks):
                conn.execute(
                    "INSERT INTO chunks(path, title, tags, chunk_index, content) VALUES (?, ?, ?, ?, ?)",
                    (rel_path, title, tags, idx, chunk),
                )

            indexed_at = datetime.now(timezone.utc).isoformat()
            conn.execute(
                """
                INSERT INTO sources(path, sha256, mtime, size, title, kind, needs_ocr, indexed_at, meta_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                  sha256=excluded.sha256,
                  mtime=excluded.mtime,
                  size=excluded.size,
                  title=excluded.title,
                  kind=excluded.kind,
                  needs_ocr=excluded.needs_ocr,
                  indexed_at=excluded.indexed_at,
                  meta_json=excluded.meta_json
                """,
                (
                    rel_path,
                    sha,
                    float(st.st_mtime),
                    int(st.st_size),
                    title,
                    kind,
                    int(needs_ocr_flag),
                    indexed_at,
                    json.dumps(meta, ensure_ascii=False),
                ),
            )

            indexed += 1
            if indexed % 20 == 0:
                conn.commit()

        conn.commit()
        print(f"DB: {db_path}")
        print(f"Indexed: {indexed}, Skipped: {skipped}, Needs OCR: {needs_ocr}, Errors: {errors}")
        return 0 if errors == 0 else 2
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())


