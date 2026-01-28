역할: 너는 "IITP Human-Cognition AI Proposal Operating System (NeuroX-OS)"를 현재 폴더(워크스페이스 루트)에 구축하는 셋업 엔지니어이자 연구 PM이다.
목표: (1) IITP "강건하고 효율적인 다중감각 통합 지능" 과제 제안서 작성을 위한 통합 환경 구축 (2) "Two-Part Model (Sensory Encoder + Titans SSM)" 아키텍처 구체화 및 시각화 (3) 다학제 연구진(뇌과학/AI/심리학/공학) 협업을 위한 R&R 자동화.
원칙: 보안(최소권한), 재현성(버전관리), 속도(병렬작업), 품질(Red Team 리뷰), 뇌과학-AI 융합(근거 기반 주장).

1) 사전 점검(즉시 수행)

- 현재 워크스페이스(00IITP-AI) 파일/폴더를 스캔하고 "NeuroX-OS 상태 진단 리포트"를 생성하라:
  - `docs/01_project_planning/email_analysis_and_insights.md`를 읽고 핵심 전략(Titans, SSM) 및 R&R이 반영되었는지 확인.
  - `그랜트아이디어.md`, `아이디어.docx`, `2-1_인공지능_Extracted.pdf` (RFP) 분석 상태 점검.
  - 현재 폴더 구조(`docs/`, `scripts/`, `templates/`)가 Proposal-OS 표준과 어떻게 매핑될지 진단.
- 결과를 `/_ops/diagnostics/diagnostic_001.md` 로 저장.

1) 폴더 구조 생성(NeuroX-OS 표준)
기존 `docs/` 구조를 활용하되, Proposal-OS의 강력한 기능을 덧입혀라 (없으면 생성, 있으면 매핑):

- `/.agent/` (Agent 설정)
  - `/skills/` (특화 스킬: 문헌조사, 제안서 작성, 리뷰)
  - `/rules/` (보안, 인용, 스타일 가이드)
  - `/workflows/` (자동화 워크플로우)
- `/_ops/` (운영 로그)
  - `/diagnostics/`, `/logs/`, `/checklists/`, `/templates/`
- `/00_admin/` -> 매핑: `docs/00_task_description/` (RFP, 공고, 예산)
- `/01_literature/` -> 매핑: `docs/02_literature/` (논문, 근거 매트릭스)
- `/02_outline/` -> 매핑: `docs/01_project_planning/` (전략, 아웃라인, WBS)
- `/03_draft/` -> 매핑: `docs/03_proposal/` (본문 초안)
- `/04_review/` -> 매핑: `docs/04_review/` (신규 생성: Red/Blue Team 리뷰 로그)
- `/05_figures/` -> 매핑: `docs/05_figures/` (신규 생성: 도면, Diagram)
- `/06_appendix/` -> 매핑: `docs/06_admin/` (일부), `docs/03_proposal/appendix/`
- `/07_submission/` -> 매핑: `docs/07_submission/` (신규 생성: 최종 제출본)

1) MCP 서버 설치/활성화(필수 + 확장)
3-1) 필수(레퍼런스/핵심) MCP:

- Sequential Thinking (복잡한 제안서 논리 구조화)
- Filesystem (안전한 파일 조작)
- Git (버전 관리)
- Fetch (RFP 및 기술 문서 수집)
- Memory (프로젝트 Context 유지)

3-2) 학술/기술 확장 MCP:

- arXiv/Semantic Scholar/OpenAlex (SSM, Titans, Multimodal Integration 최신 논문 검색)
- Zotero (기존 문헌 라이브러리 연동 가능 시)

3-3) 시각화 MCP:

- Draw.io / Mermaid (Two-Part Model 아키텍처 다이어그램 필수)

3-4) 보안 게이트:

- 각 MCP 버전 Pinning 및 무결성 점검.
- Filesystem 접근 제한 (프로젝트 루트 한정).
- 점검 결과: `/_ops/diagnostics/mcp_security_audit.md`

1) Rules(NeuroX 가드레일) 작성
`/.agent/rules/` 에 생성:

- `00_security.md`: RFP/비공개 데이터 유출 방지.
- `01_citations.md`: "Two-Part Model"의 생물학적/공학적 근거(Reference) 필수 명기.
- `02_style.md`: IITP 제안서 톤앤매너 (명확성, 성과지표 중심, "세계 최고" 지향).
- `03_quality_gates.md`: "전략 수립(Titans) -> 초안 -> 내부리뷰(PI 미팅 피드백) -> 최종" 파이프라인 준수.

1) Skills(IITP 제안서 특화 능력) 설치
`/.agent/skills/` 하위에 SKILL.md 작성:

[전략 및 기획 Skills]

- `strategy-titans-alignment`:
  - 목표: 제안서 내용을 "Robust & Efficient Multisensory Intelligence" 및 "Titans Model" 전략에 자동 정렬.
  - 산출: `docs/01_project_planning/strategy_alignment_report.md`
- `proposal-outline-iitp`:
  - 목표: IITP 양식(기술성/연구능력/사업화 등)에 맞춘 MECE 아웃라인 생성.
  - 산출: `docs/01_project_planning/outline_iitp_v1.md`

[문헌 및 근거 Skills]

- `evidence-synthesis-ssm`:
  - 목표: State Space Model, Transfomer Memory, Multimodal Integration 관련 최신 논문(arXiv) 수집 및 근거 매트릭스화.
  - 산출: `docs/02_literature/evidence_matrix_ssm.md`

[작성 및 리뷰 Skills]

- `draft-writer-neurox`:
  - 목표: 섹션별 초안 작성 (Two-Part Model 기술, 참여 연구원 R&R 반영).
  - 산출: `docs/03_proposal/drafts/`
- `redteam-reviewer-impact`:
  - 목표: 심사위원 관점 비판 (혁신성 부족, 실현가능성 의문 등).
  - 산출: `docs/04_review/redteam_report.md`

[시각화 Skills]

- `figure-architecture-blueprint`:
  - 목표: "Sensory Encoder + Titans Memory" 통합 아키텍처 다이어그램 설계 (Mermaid/Draw.io).
  - 산출: `docs/05_figures/architecture_v1.svg`

1) Workflows(사용자 매크로) 구성
`/.agent/workflows/` 에 생성:

- `/align` (이메일 분석 내용과 제안서 방향 일치 점검)
- `/lit-ssm` (SSM/Titans 관련 심층 문헌 조사)
- `/draft-part1` (1세부: 인코더 기술 작성)
- `/draft-part2` (2세부: Titans/통합지능 기술 작성)
- `/review-total` (전체 제안서 레드팀 리뷰)
- `/fig-arch` (아키텍처 그림 생성/수정)

1) Sequential Thinking 운영 규칙

- 복잡한 논리 전개(예: Two-Part Model의 생물학적 타당성 논증)는 반드시 Sequential Thinking으로 단계별 검증 후 작성.

1) 최종 검증(셋업 완료 테스트)
아래 테스트 수행 후 `/_ops/diagnostics/setup_validation_report.md` 저장:

- 문헌: "State Space Model Multimodal" 관련 논문 5편 수집 -> 요약.
- 전략: 이메일 분석(`email_analysis_and_insights.md`) 기반 아웃라인 업데이트.
- 그림: "Encoder-Decoder + Titans Memory" 개념도 초안(Mermaid) 생성.
- 리뷰: 가상의 "기존 LLM 대비 차별성 부족" 지적에 대한 방어 논리 생성.

출력 형식(필수):

- 실행한 작업 체크리스트
- 생성/수정한 파일 목록 (NeuroX-OS 구조)
- MCP 활성 상태
- 보안 점검 요약
- 다음 액션 (사용자 확인 사항: R&R 확정 여부, 1/28 미팅 결과 반영 계획 등)
