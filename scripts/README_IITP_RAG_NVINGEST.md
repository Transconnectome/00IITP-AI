# 00IITP-AI RAG + nv-ingest 연동 스크립트 가이드

- **설계**: [docs/06_admin/DESIGN_RAG_NVINGEST_AI_COSCIENTIST.md](../docs/06_admin/DESIGN_RAG_NVINGEST_AI_COSCIENTIST.md)
- **구현 문서 (API·Runbook·Changelog)**: [docs/06_admin/IITP_RAG_IMPLEMENTATION_DOCUMENTATION.md](../docs/06_admin/IITP_RAG_IMPLEMENTATION_DOCUMENTATION.md)

## 사전 요구사항

- Python 3.10+
- nv-ingest 사용 시: 서비스 실행 (Docker: `docker-compose -f docker-compose.nv-ingest.yml up -d`), 포트 gRPC 7670 / HTTP 7671
- 패키지: `chromadb`, `sentence-transformers` (필수). nv-ingest 사용 시 `nv_ingest_client`

## 스크립트 역할

| 스크립트 | 역할 |
|----------|------|
| `run_iitp_rag_build.sh` | Idempotent 실행: 디렉터리 확인 → PDF 목록 → ingest 또는 build 호출 |
| `ingest_iitp_ai_nvingest.py` | nv-ingest(선택)로 PDF ingest → 청크 JSONL → build 호출. 미사용 시 로컬 빌드만 수행 |
| `build_iitp_ai_rag.py` | docs/ 스캔 또는 `--chunks-jsonl` → ChromaDB `iitp_ai_L0` 구축, IITP-AI 카테고리 태깅 |
| `kb_ingest.py` / `kb_query.py` | 기존 SQLite FTS KB (유지, 벡터 RAG와 병행) |

## 실행 순서 (수동)

1. `./run_iitp_rag_build.sh` 한 번 실행 (또는 아래 단계별 실행)
2. k-bfm / AI-CoScientist에서 `IITP_AI` 전략 등록 후 쿼리 테스트

## 환경 변수 (선택)

- `IITP_AI_VECTOR_DB`: ChromaDB 저장 경로 (기본: `../data/vector_db_iitp_ai`)
- `NVINGEST_HOST`, `NVINGEST_PORT`: nv-ingest 서버 (기본: localhost, 7671)

## AI-CoScientist에서 IITP-AI DB 사용

AI-CoScientist의 `ChromaDBConfig.iitp_ai_path`를 00IITP-AI 벡터 DB 절대 경로로 설정하면 IITP_AI 전략으로 검색 가능:

```python
from src.services.rag.multi_strategy_search import ChromaDBConfig, create_search_engine

cfg = ChromaDBConfig(iitp_ai_path="/path/to/00IITP-AI/data/vector_db_iitp_ai")
engine = await create_search_engine(cfg)
result = await engine.search("SSM sensory encoder", strategies=["IITP_AI"])
```
