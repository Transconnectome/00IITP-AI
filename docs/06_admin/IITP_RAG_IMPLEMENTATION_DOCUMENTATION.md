# IITP-AI RAG 연동 구현 문서

**문서 유형**: Implementation Documentation (API Reference + Runbook + Changelog)  
**관련 설계**: [DESIGN_RAG_NVINGEST_AI_COSCIENTIST.md](./DESIGN_RAG_NVINGEST_AI_COSCIENTIST.md)  
**최종 갱신**: 2026-01-28

---

## 1. 변경 사항 요약 (Changelog)

### 1.1 00IITP-AI 저장소

| 유형 | 경로 | 설명 |
|------|------|------|
| **신규** | `scripts/build_iitp_ai_rag.py` | docs/ PDF·MD 스캔 → 청킹 → SciBERT 임베딩 → ChromaDB `iitp_ai_L0` 구축 |
| **신규** | `scripts/ingest_iitp_ai_nvingest.py` | nv-ingest(선택) 또는 로컬 추출 → 청크 JSONL → build 스크립트 호출 |
| **신규** | `scripts/run_iitp_rag_build.sh` | Idempotent 실행: 디렉터리·PDF 목록 → ingest/build 호출 |
| **신규** | `scripts/README_IITP_RAG_NVINGEST.md` | 스크립트 가이드·환경 변수·AI-CoScientist 연동 요약 |
| **신규** | `docs/06_admin/DESIGN_RAG_NVINGEST_AI_COSCIENTIST.md` | 설계 명세 (아키텍처·컴포넌트·코드 스펙) |
| **신규** | `docs/06_admin/IITP_RAG_IMPLEMENTATION_DOCUMENTATION.md` | 본 구현 문서 |
| **수정** | `.gitignore` | `data/vector_db_iitp_ai/`, `tmp/iitp_ai_pdf_list.txt` 추가 |

### 1.2 k-bfm 저장소

| 유형 | 경로 | 설명 |
|------|------|------|
| **신규** | `ai_coscientist_src/services/rag/iitp_ai_rag_strategy.py` | `IITPAIRAGStrategy` 구현 (RAGStrategyInterface) |
| **수정** | `ai_coscientist_src/services/rag/unified_rag_orchestrator.py` | `RAGStrategy.IITP_AI` enum·config·초기화 블록, `Path`/`os` import 추가 |

### 1.3 AI-CoScientist 저장소

| 유형 | 경로 | 설명 |
|------|------|------|
| **수정** | `src/services/rag/unified_rag_orchestrator.py` | `RAGStrategy.IITP_AI` enum 및 `RAGStrategyConfig` 항목 추가 |
| **수정** | `src/services/rag/multi_strategy_search.py` | `ChromaDBConfig.iitp_ai_path`, `IITPAIRAGStrategy` 클래스, `create_real_strategies`/`strategy_classes` 등록, iitp_ai 768차원 처리 |

---

## 2. API 레퍼런스

### 2.1 build_iitp_ai_rag.py

**역할**: docs/ 또는 JSONL 청크 → ChromaDB `iitp_ai_L0` 구축 (SciBERT 768차원).

**CLI 인자**:

| 인자 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `--vector-db` | Path | `project_root/data/vector_db_iitp_ai` | ChromaDB 저장 디렉터리 |
| `--docs-dir` | Path | `project_root/docs` | PDF·MD 스캔 경로 |
| `--chunks-jsonl` | Path | None | 사용 시 스캔 생략, 해당 JSONL에서 청크 로드 |
| `--chunk-size` | int | 1024 | 청크 최대 문자 수 |
| `--chunk-overlap` | int | 150 | 청크 겹침 문자 수 |
| `--embedding-model` | str | `allenai/scibert_scivocab_uncased` | SentenceTransformer 모델명 |

**JSONL 한 줄 형식** (chunks-jsonl):

```json
{"source_path": "docs/02_literature/...", "doc_title": "...", "chunk_index": 0, "content": "...", "category": "literature"}
```

**의존성**: `chromadb`, `sentence-transformers`. PDF 추출 시 `pdftotext` 필요.

**동작**: 기존 `iitp_ai_L0` 컬렉션이 있으면 삭제 후 재생성 (idempotent는 “전체 재구축” 기준).

---

### 2.2 ingest_iitp_ai_nvingest.py

**역할**: PDF 목록 → (선택) nv-ingest 호출 → 청크 JSONL 작성 → `build_iitp_ai_rag.py` 실행. nv-ingest 미사용 시 로컬 빌드만 수행.

**CLI 인자**:

| 인자 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `--pdf-list` | Path | None | 한 줄에 하나씩 PDF 경로가 있는 파일 |
| `--vector-db` | Path | `project_root/data/vector_db_iitp_ai` | ChromaDB 디렉터리 |
| `--nv-host` | str | localhost | nv-ingest 호스트 |
| `--nv-port` | int | 7671 | nv-ingest HTTP 포트 |
| `--output-jsonl` | Path | `project_root/tmp/iitp_ai_chunks.jsonl` | nv-ingest 결과 청크 JSONL 경로 |
| `--skip-nvingest` | flag | False | True면 nv-ingest 생략, docs 스캔 빌드만 수행 |

**의존성**: nv-ingest 사용 시 `nv_ingest_client` 등. 로컬 전용 시 `build_iitp_ai_rag.py`와 동일.

---

### 2.3 run_iitp_rag_build.sh

**역할**: Idempotent 진입점. 벡터 DB 디렉터리 생성, docs/ 하위 PDF 목록 수집, nv-ingest 연결 확인 후 Python 스크립트 호출.

**환경 변수**:

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `IITP_AI_VECTOR_DB` | `project_root/data/vector_db_iitp_ai` | ChromaDB 경로 |
| `NVINGEST_HOST` | localhost | nv-ingest 호스트 |
| `NVINGEST_PORT` | 7671 | nv-ingest 포트 |

**호출 순서**: `ingest_iitp_ai_nvingest.py` 존재 시 해당 스크립트 실행, 없으면 `build_iitp_ai_rag.py`만 실행.

---

### 2.4 IITPAIRAGStrategy (k-bfm)

**모듈**: `k-bfm/ai_coscientist_src/services/rag/iitp_ai_rag_strategy.py`

**인터페이스**: `RAGStrategyInterface` (UnifiedRAGOrchestrator 사용).

**생성자**:

- `IITPAIRAGStrategy(db_path: Optional[Path] = None, embedding_model: str = "allenai/scibert_scivocab_uncased")`
- `db_path` 미지정 시: `project_root/00IITP-AI/data/vector_db_iitp_ai` (k-bfm 기준 형제 레포 가정).

**주요 메서드**:

- `is_available() -> bool`: ChromaDB 및 `iitp_ai_L0` 존재 여부
- `get_strategy_name() -> RAGStrategy`: `RAGStrategy.IITP_AI`
- `estimate_performance(query_context: QueryContext) -> float`: IITP 관련 키워드/도메인에 따라 0.6~0.9
- `async search(query_context: QueryContext) -> RAGResponse`: 쿼리 임베딩 → `iitp_ai_L0` 검색 → 소스·요약·confidence 반환

**메타데이터**: `source_path`, `doc_title`, `chunk_index`, `category` (sensory_encoder, titans_memory, task_description, literature, proposal, general).

---

### 2.5 IITPAIRAGStrategy (AI-CoScientist)

**모듈**: `AI-CoScientist/src/services/rag/multi_strategy_search.py`

**설정**: `ChromaDBConfig.iitp_ai_path: str = "chromadb_iitp_ai"` (기본 상대 경로). 00IITP-AI 벡터 DB를 쓰려면 절대 경로로 오버라이드.

**사용 예**:

```python
from src.services.rag.multi_strategy_search import ChromaDBConfig, create_search_engine

cfg = ChromaDBConfig(iitp_ai_path="/path/to/00IITP-AI/data/vector_db_iitp_ai")
engine = await create_search_engine(cfg)
result = await engine.search("SSM sensory encoder", strategies=["IITP_AI"])
```

**임베딩 차원**: iitp_ai DB는 768(SciBERT)로 자동 감지 (`_detect_collection_dimension`).

---

## 3. 사용 가이드 (Runbook)

### 3.1 00IITP-AI에서 벡터 DB 최초/재구축

```bash
cd /path/to/00IITP-AI
python3 scripts/build_iitp_ai_rag.py
# 또는 한 번에
./scripts/run_iitp_rag_build.sh
```

### 3.2 nv-ingest 사용 (선택)

1. nv-ingest 서비스 기동 (예: `docker-compose -f docker-compose.nv-ingest.yml up -d`).
2. PDF 목록 파일 생성: `find docs -name "*.pdf" > tmp/iitp_ai_pdf_list.txt`
3. `python3 scripts/ingest_iitp_ai_nvingest.py --pdf-list tmp/iitp_ai_pdf_list.txt`
4. nv-ingest 미동작 시 자동으로 로컬 빌드만 수행됨.

### 3.3 k-bfm에서 IITP-AI 전략으로 검색

- 00IITP-AI가 k-bfm과 형제 디렉터리면 별도 설정 없이 `IITP_AI` 전략 사용 가능.
- 다른 경로면 `IITP_AI_VECTOR_DB` 환경 변수에 `data/vector_db_iitp_ai` 절대 경로 설정.

### 3.4 AI-CoScientist에서 IITP-AI 전략 사용

- `ChromaDBConfig(iitp_ai_path="/path/to/00IITP-AI/data/vector_db_iitp_ai")` 로 엔진 생성 후 `strategies=["IITP_AI"]` 로 검색.

---

## 4. ChromaDB 스키마 (iitp_ai_L0)

| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | str | `{source_path}_{chunk_index}` |
| `embedding` | list[float] | 768차원 (SciBERT) |
| `document` | str | 청크 본문 |
| `source_path` | str | 상대 경로 |
| `doc_title` | str | 문서 제목 (최대 200자 반영) |
| `chunk_index` | int | 청크 인덱스 |
| `category` | str | task_description | literature | proposal | sensory_encoder | titans_memory | general |

---

## 5. 관련 문서 인덱스

| 문서 | 용도 |
|------|------|
| [DESIGN_RAG_NVINGEST_AI_COSCIENTIST.md](./DESIGN_RAG_NVINGEST_AI_COSCIENTIST.md) | 아키텍처·데이터 흐름·코드 스펙·체크리스트 |
| [IITP_RAG_IMPLEMENTATION_DOCUMENTATION.md](./IITP_RAG_IMPLEMENTATION_DOCUMENTATION.md) | 본 문서: 구현 요약·API·Runbook |
| [scripts/README_IITP_RAG_NVINGEST.md](../../scripts/README_IITP_RAG_NVINGEST.md) | 스크립트 요약·환경 변수·빠른 사용법 |
