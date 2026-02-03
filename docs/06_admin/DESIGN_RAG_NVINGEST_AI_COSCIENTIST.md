# Design: 00IITP-AI 문서 ↔ k-bfm RAG · AI-CoScientist · nv-ingest 연동

**문서 버전**: 1.0  
**작성 목적**: 00IITP-AI 코드베이스 문서를 k-bfm RAG 및 AI-CoScientist와 연동하고, nv-ingest로 PDF를 수집해 IITP-AI 주제에 맞게 업그레이드하기 위한 설계 명세.

---

## 1. 개요 및 목표

| 목표 | 설명 |
|------|------|
| **문서 연동** | 00IITP-AI `docs/`(PDF·MD)를 k-bfm이 쓰는 RAG 및 AI-CoScientist 검색 파이프라인에서 사용 |
| **nv-ingest 활용** | PDF → nv-ingest(추출·청크·임베딩) → 벡터 DB로 이관해 품질 향상 |
| **IITP-AI 정렬** | Two-Part Model, Sensory Encoder, Titans Memory, SSM 등 주제에 맞는 메타데이터·카테고리 적용 |

---

## 2. 현재 구조 요약

### 2.1 00IITP-AI

- **문서 위치**: `docs/00_task_description/`, `docs/02_literature/`, `docs/03_proposal/` 등
- **지식 저장소**: `knowledge_base/kb.sqlite` (SQLite FTS), `scripts/kb_ingest.py` / `scripts/kb_query.py`
- **특징**: 벡터 RAG 없음. pdftotext/OCR 기반 텍스트 → FTS만 사용.

### 2.2 k-bfm

- **RAG**: ChromaDB `data/vector_db_kneuromind` (RAPTOR L0/L1), SciBERT 임베딩
- **빌드**: `scripts/build_kneuromind_rag.py` (CSV 메타데이터 → LangChain → Chroma)
- **오케스트레이션**: `ai_coscientist_src.services.rag.unified_rag_orchestrator`  
  - `RAGStrategy.K_NEUROMIND`, `KNeuroMindRAGStrategy`
- **추가 KB**: `scripts/kb_ingest.py` → SQLite FTS (벡터 DB와 별개)

### 2.3 AI-CoScientist

- **벡터 DB**: ChromaDB 경로들 (`chromadb_data_dd`, `chromadb_grants_fixed_*` 등)
- **설정**: `ChromaDBConfig` (dd_raptor_path, grants_path, esm3_papers_path 등)
- **검색**: `MultiStrategySearchEngine`, `RealRAGStrategy` 계열, `UnifiedRAGOrchestrator`와 연동 가능

### 2.4 nv-ingest

- **역할**: PDF 등 문서 → 추출(텍스트/표/차트) → 청킹 → 임베딩 → (선택) VDB 업로드
- **접근**: Docker `docker-compose.nv-ingest.yml` (gRPC 7670, HTTP 7671) 또는 Library mode
- **클라이언트**: `nv_ingest_client.client.Ingestor`, `NvIngestClient`

---

## 3. 아키텍처 (데이터 흐름)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  00IITP-AI docs/                                                             │
│  (00_task_description/*.pdf, 02_literature/**/*.pdf, 03_proposal/**/*.pdf)  │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  nv-ingest Pipeline                                                          │
│  Ingestor(client).files(...).extract(...).split(...).embed()                 │
│  → chunks + embeddings (GPU, 고품질 추출/임베딩)                             │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼
┌───────────────────────────────┐   ┌───────────────────────────────────────┐
│  ChromaDB (IITP-AI 전용)       │   │  기존 SQLite FTS (선택 유지)            │
│  data/vector_db_iitp_ai/      │   │  knowledge_base/kb.sqlite               │
│  - iitp_ai_L0 (chunks)        │   │  (kb_ingest.py로 계속 수집 가능)         │
│  - iitp_ai_L1 (doc summary)   │   └───────────────────────────────────────┘
│  metadata: category, source  │
└───────────────┬───────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  RAG 전략 계층                                                                │
│  • k-bfm: IITPAIRAGStrategy (RAGStrategy.IITP_AI) → UnifiedRAGOrchestrator   │
│  • AI-CoScientist: ChromaDBConfig.iitp_ai_path + RealRAGStrategy 확장       │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  AI-CoScientist / 제안서 에이전트                                             │
│  QueryContext → Orchestrator.search() → IITP_AI 전략으로 00IITP-AI 문서 검색 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. 컴포넌트 설계

### 4.1 nv-ingest 파이프라인 (00IITP-AI용)

- **입력**: `00IITP-AI/docs/` 하위 PDF (및 필요 시 MD 경로 목록).
- **단계**:
  1. `Ingestor(client).files(glob_or_list)`
  2. `.extract(extract_text=True, extract_tables=True, extract_charts=True, table_output_format="markdown", text_depth="page")`
  3. `.split(chunk_size=1024, chunk_overlap=150)` (IITP-AI 문맥에 맞게 조정 가능)
  4. `.embed()` (nv-ingest 기본 임베딩)
- **출력**:
  - **Option A**: nv-ingest `.vdb_upload(collection_name="iitp_ai", milvus_uri=...)` → Milvus 사용 시.
  - **Option B (권장)**: `.ingest(return_failures=True)` 로 결과만 수신 → 별도 스크립트가 ChromaDB `iitp_ai_L0`에 삽입 (임베딩 차원 맞추기: 384 또는 768, SciBERT 호환 시 768).

### 4.2 ChromaDB 스키마 (IITP-AI 컬렉션)

| 컬렉션 | 용도 | 메타데이터 필드 |
|--------|------|------------------|
| `iitp_ai_L0` | 청크 단위 검색 | `source_path`, `category`, `doc_title`, `chunk_index`, `page` |
| `iitp_ai_L1` | (선택) 문서/섹션 요약 | `source_path`, `category`, `doc_title` |

- **category** 값 예: `sensory_encoder`, `titans_memory`, `ssm`, `predictive_coding`, `jepa`, `task_description`, `literature`, `proposal`.
- **임베딩**: k-bfm/AI-CoScientist와 공유 시 **SciBERT 768차원** 권장 (KNeuroMind와 동일).

### 4.3 IITP-AI RAG 전략 (k-bfm 쪽)

- **이름**: `RAGStrategy.IITP_AI`, 구현체 `IITPAIRAGStrategy`.
- **위치**: `k-bfm/ai_coscientist_src/services/rag/iitp_ai_rag_strategy.py` (신규).
- **인터페이스**: `RAGStrategyInterface` (기존 `KNeuroMindRAGStrategy`와 동일).
- **DB 경로**: 환경변수 또는 설정으로 `00IITP-AI/data/vector_db_iitp_ai` 지정 (또는 공유 볼륨 경로).
- **도메인**: `QueryDomain.NEUROSCIENCE`, `QueryDomain.GENERAL`; IITP-AI 관련 쿼리(SSM, 감각 인코더, 기억 모델 등)에서 우선 선택되도록 `estimate_performance` 설계.

### 4.4 AI-CoScientist 연동

- **ChromaDBConfig** 확장: `iitp_ai_path: str = "chromadb_iitp_ai"` (또는 절대경로).
- **RealRAGStrategy** 계열: `IITPAIStrategy` 클래스 추가, `_get_relevant_databases()`에 `iitp_ai` 포함.
- **UnifiedRAGOrchestrator**: `RAGStrategy.IITP_AI` 설정 및 `IITPAIRAGStrategy` 등록 (k-bfm과 동일 인터페이스 사용 시).

### 4.5 IITP-AI 주제 정렬 (업그레이드)

- **자동 태깅**: 청크/문서에 키워드 기반으로 `category` 부여.
  - 예: "Sensory Encoder", "Predictive Coding", "JEPA" → `sensory_encoder`; "SSM", "Mamba", "Titans Memory" → `titans_memory` 또는 `ssm`.
- **메타데이터**: `source_path`에 `docs/02_literature/`, `docs/03_proposal/` 등 구분 유지 → 검색 시 필터로 활용.
- **기존 kb_ingest.py**: 유지 가능. FTS와 벡터 RAG 병행 시, “IITP-AI 전용 질의”는 벡터 RAG, “전체 문서 키워드 검색”은 FTS로 분리.

---

## 5. 구현 단계 (체크리스트)

| # | 단계 | 담당 레포/경로 | 비고 |
|---|------|----------------|------|
| 1 | 00IITP-AI에 `data/vector_db_iitp_ai` 디렉토리 생성 | 00IITP-AI | .gitignore에 추가 |
| 2 | nv-ingest 서비스 기동 (Docker 또는 Library mode) | AI-CoScientist 또는 00IITP-AI | 7670/7671 포트 |
| 3 | 스크립트: 00IITP-AI docs PDF 목록 수집 → nv-ingest 호출 → 결과 수신 | 00IITP-AI/scripts/ | `ingest_iitp_ai_nvingest.py` |
| 4 | nv-ingest 결과 → ChromaDB 삽입 (임베딩 768 사용 시 SciBERT로 재임베딩 또는 nv 기본 차원에 맞춘 컬렉션) | 00IITP-AI/scripts/ | build_iitp_ai_rag.py 또는 ingest 스크립트 내 |
| 5 | IITP-AI용 카테고리/메타데이터 규칙 적용 (키워드 기반 자동 태깅) | 00IITP-AI/scripts/ | 위 스크립트 또는 후처리 |
| 6 | k-bfm에 `RAGStrategy.IITP_AI` 및 `IITPAIRAGStrategy` 추가 | k-bfm/ai_coscientist_src/services/rag/ | unified_rag_orchestrator 수정 포함 |
| 7 | AI-CoScientist에 `iitp_ai_path` 및 IITP 전략 등록 | AI-CoScientist/src/services/rag/ | ChromaDBConfig, multi_strategy_search |
| 8 | 연동 테스트: QueryContext(domain=NEUROSCIENCE, query="SSM sensory encoder") → IITP_AI 전략으로 검색 | k-bfm / AI-CoScientist | 단위 테스트 또는 수동 쿼리 |

---

## 6. 파일/경로 정리

| 항목 | 경로 |
|------|------|
| 00IITP-AI 벡터 DB | `00IITP-AI/data/vector_db_iitp_ai/` |
| 00IITP-AI PDF 소스 | `00IITP-AI/docs/00_task_description/`, `02_literature/`, `03_proposal/` |
| k-bfm RAG 전략 | `k-bfm/ai_coscientist_src/services/rag/iitp_ai_rag_strategy.py` (신규) |
| k-bfm 오케스트레이터 | `k-bfm/ai_coscientist_src/services/rag/unified_rag_orchestrator.py` |
| AI-CoScientist ChromaDB 설정 | `AI-CoScientist/src/services/rag/multi_strategy_search.py` (ChromaDBConfig) |
| nv-ingest Docker | `AI-CoScientist/docker-compose.nv-ingest.yml` |

---

## 7. Idempotent 설치/빌드 스크립트 요약

- **전제**: nv-ingest 서비스 실행 중, Python 환경에 chromadb, sentence-transformers, nv_ingest_client 등 설치.
- **순서**:
  1. 00IITP-AI `data/vector_db_iitp_ai` 존재 여부 확인, 없으면 생성.
  2. PDF 목록 수집 (docs 하위 glob).
  3. nv-ingest 호출 (extract → split → embed) → 결과 청크/임베딩 수신.
  4. 기존 `iitp_ai_L0` 컬렉션이 있으면 “같은 source_path+chunk_index”는 스킵 또는 덮어쓰기 정책으로 업데이트.
  5. ChromaDB에 삽입 (메타데이터 category 등 적용).
  6. (선택) k-bfm/AI-CoScientist에서 해당 경로를 바라보는지 설정 확인.

이 순서를 한 번에 수행하는 bash 스크립트: `00IITP-AI/scripts/run_iitp_rag_build.sh`. 가이드: `00IITP-AI/scripts/README_IITP_RAG_NVINGEST.md`.

---

## 8. 코드 스펙 (k-bfm · AI-CoScientist)

### 8.1 k-bfm: RAGStrategy enum 확장

`k-bfm/ai_coscientist_src/services/rag/unified_rag_orchestrator.py`:

```python
class RAGStrategy(Enum):
    # ... 기존 ...
    K_NEUROMIND = "kneuromind"
    IITP_AI = "iitp_ai"  # 00IITP-AI 제안서 전용
```

`RAGStrategyConfig.strategy_configs`에 추가:

```python
RAGStrategy.IITP_AI: {
    "enabled": True,
    "priority": 1,
    "domains": [QueryDomain.NEUROSCIENCE, QueryDomain.GENERAL],
    "complexity_range": [QueryComplexity.SIMPLE, QueryComplexity.MEDIUM, QueryComplexity.COMPLEX],
    "max_concurrent": 5
}
```

오케스트레이터 초기화 블록에 추가 (K-NeuroMind 다음):

```python
# IITP-AI RAG Strategy (00IITP-AI 문서)
if self.config.get_config(RAGStrategy.IITP_AI).get("enabled", False):
    try:
        from src.services.rag.iitp_ai_rag_strategy import IITPAIRAGStrategy
        iitp_db_path = os.environ.get("IITP_AI_VECTOR_DB", "") or str(Path(__file__).resolve().parents[4] / "00IITP-AI" / "data" / "vector_db_iitp_ai")
        iitp_strategy = IITPAIRAGStrategy(db_path=Path(iitp_db_path))
        if iitp_strategy.is_available():
            self.strategies[RAGStrategy.IITP_AI] = iitp_strategy
            logger.info("✅ ENABLED: IITP-AI RAG Strategy initialized")
    except Exception as e:
        logger.warning(f"IITP-AI RAG not available: {e}")
```

### 8.2 AI-CoScientist: ChromaDBConfig 확장

`AI-CoScientist/src/services/rag/multi_strategy_search.py`:

```python
@dataclass
class ChromaDBConfig:
    # ... 기존 ...
    iitp_ai_path: str = "chromadb_iitp_ai"  # 또는 절대 경로
```

`_get_relevant_databases()`를 오버라이드하는 IITP 전략 클래스에서:

```python
"iitp_ai": self.config.iitp_ai_path
```

---

## 9. IITP-AI 카테고리 키워드 (자동 태깅 참고)

| category | 키워드 예 |
|----------|-----------|
| sensory_encoder | Sensory Encoder, Predictive Coding, JEPA, Clockwork VAE, 감각 처리 |
| titans_memory | Titans Memory, SSM, Mamba, State Space Model, 기억, 망각 |
| foundation | foundation model, pretraining, brain decoding |
| task_description | RFP, 공고문, 과제명 |
| literature | 논문, paper, briefing |
| proposal | 제안서, references |
