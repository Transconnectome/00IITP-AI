# Knowledge Base (KB)

이 폴더는 repo 안의 문서/PDF/캡처본을 **검색 가능한 데이터**로 쓰기 위해, 로컬에서 만드는 **SQLite FTS(전문검색) 인덱스**를 관리합니다.

## 목표

- `docs/`에 쌓이는 근거자료(브리핑/논문/PDF/NotebookLM 캡처/과제 설명서 파싱)를 **한 번에 검색**
- 제안서 작성 시 “근거 문장”을 빠르게 찾아 **인용/재진술** 가능
- 외부 서비스 없이 **로컬에서 재현 가능**

## 구성

- **DB(로컬 생성)**: `knowledge_base/kb.sqlite` (git에 커밋하지 않음; `knowledge_base/.gitignore`로 제외)
- **인덱싱 스크립트**: `scripts/kb_ingest.py`
- **검색 스크립트**: `scripts/kb_query.py`

## 사용법

### 1) 인덱스 생성/갱신

```bash
python3 scripts/kb_ingest.py
```

기본값으로 아래 경로를 스캔합니다:

- `docs/00_task_description/parsed/`
- `docs/02_literature/` (briefings/reading-notes/papers 포함)
- `docs/03_proposal/references/`

### 2) 검색

```bash
python3 scripts/kb_query.py "neuromorphic energy efficiency"
```

## PDF(OCR) 주의사항

최근 추가된 일부 PDF는 **텍스트 레이어가 없는 이미지 기반(PDF 스캔/슬라이드)**입니다.  
이 경우 `pdftotext`로는 텍스트가 나오지 않아 **OCR이 필요**합니다.

- 현재 머신에 설치된 OCR 언어 확인:

```bash
tesseract --list-langs
```

- OCR 활성화(옵션):

```bash
python3 scripts/kb_ingest.py --ocr --ocr-lang eng
```

> 한글 OCR을 원하면 `--ocr-lang kor+eng`가 필요하며, 로컬 tesseract에 `kor` 언어 데이터가 설치돼 있어야 합니다.


