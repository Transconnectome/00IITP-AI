# ChromaDB iitp_ai_L0 인덱스 현황

**갱신**: 2026-01-28  
**경로**: `data/vector_db_iitp_ai` / 컬렉션 `iitp_ai_L0`

---

## 요약

| 항목 | 값 |
|------|-----|
| **총 청크(문서) 수** | 3,451 |
| **고유 소스 파일 수** | 109 |
| **PDF 소스 수** | 59 |
| **MD 소스 수** | 50 |

---

## 스캔 범위

현재 빌드 스크립트(`build_iitp_ai_rag.py`) 기본값은 **`--docs-dir docs`** 이므로 **`docs/` 하위만** 스캔됨.  
**`tmp/` 폴더는 스캔 대상에 포함되지 않음** → tmp 내 PDF/MD는 ingest 완료되지 않음.

---

## PDF 논문/문서 목록 (소스별 청크 수)

### 02_literature (문헌)

- eeg_fm_prospective_2024.pdf (573)
- analog_training_algorithms_2024.pdf (122)
- mehonic_2024_neuromorphic_roadmap.pdf (107)
- mamba_foundation_2024.pdf (103)
- mentality_eeg_mamba_2025.pdf (103)
- csbrain_2025_eeg_fm.pdf (95)
- Zhao_2025_CodeBrain.pdf (93)
- ibm_2025_analog_foundation_models.pdf (92)
- brainomni_2025_eeg_meg_fm.pdf (64)
- dfmg_2025_snn_algo.pdf (62)
- EdgeAI_Neuroscience_2025.pdf (60)
- brain_jepa_2024.pdf (57)
- braingfm_2024.pdf (57)
- BrainGFM_2025.pdf (56)
- Moussa_2025_BrainTuning.pdf (53)
- 00공고문-bfm.pdf (48)
- zhou_2025_brain_foundation_models.pdf (46)
- brain_mamba_2024.pdf (46)
- omnifield.pdf (44)
- ibm_2024_analog_transformer_attention.pdf (42)
- staci.pdf (37)
- Jiang_2025_ALFEE.pdf (36)
- fm4npp.pdf (33)
- cbramod_2024_eeg_fm.pdf (33)
- Causal_DigitalTwin_2024.pdf (30)
- eegmamba_2024.pdf (26)
- brain_lm_2024.pdf (25)
- mamba_ginr.pdf (24)
- Chen_2025_VNS_EEG.pdf (20)
- HuBERT_EEG_2025.pdf (18)
- neuro_gpt_2024.pdf (15)
- vns.pdf (12)
- Neuro_Distillation_2025.pdf (12)
- brain_tuned_speech.pdf (8)
- lu_2023_digital_twin_brain.pdf (8)
- dtb_whole_human_brain_2023.pdf (8)
- rfp-kneuromind.pdf (5)
- Neuromorphic_Edge_2024.pdf (4)

### 03_proposal/references/proposals (샘플 제안서)

- 샘플-발달연구.pdf (293)
- 샘플-brainlink.pdf (256)
- 샘플-incite.pdf (76)
- 샘플-arpa.pdf (35)
- 샘플-삼성 발달.pdf (4)

### 00_task_description (공고/참고자료)

- 2-1_인공지능.pdf (101)
- 공고문.pdf (36)
- 과제목록.pdf (27)
- [참고자료 4] 국가과학기술표준분류체계.pdf (122)
- [참고자료 2] ~ [참고자료 10], IRIS 매뉴얼 등 (1~21 chunks each)

---

## tmp/ 폴더 (미포함)

| 파일 | 비고 |
|------|------|
| 2504.12262v1.pdf | ChromaDB 미포함 |
| 32_Mamba_GINR_A_Scalable_Frame.pdf | ChromaDB 미포함 |
| 7782_FM4NPP_A_Scaling_Foundati (1).pdf | ChromaDB 미포함 |
| prompt.md | ChromaDB 미포함 |

**tmp 포함하려면**: `python3 scripts/build_iitp_ai_rag.py --docs-dir tmp` 로 tmp만 추가 빌드하거나, 스크립트에서 `docs`와 `tmp` 둘 다 스캔하도록 변경 후 전체 재빌드.

---

## MD 파일 내용 요약 (대부분 어떤 내용인지)

ChromaDB에 인덱싱된 **50개 MD**는 대략 아래처럼 나뉩니다.

### 1. 과제/공고·요약 (00_task_description, summary)

- **RFP 요약**: `2-1_인공지능_cognitive_ai_keypoints.md` — 2026-인공지능-010~014 품목, 세부과제명·예산·TRL·핵심 포인트.
- **README**: 과제 설명서·붙임 자료 구조 안내.

### 2. 프로젝트 기획 (01_project_planning)

- **비전**: Connectome 기반 뇌 원리 + AI → 저전력·저지연 Neuromorphic 로드맵.
- **전략**: `06_iitp_cognitive_ai_strategy.md` — 2026-인공지능-014(세부5) “데이터 의미화” 집중, 인지적 수집·의미 연결망·Titans/SSM·Predictive Coding 등.
- **데이터 시맨틱화**: `07_iitp_2026_ai_014_data_semanticization_plan.md` — 데이터 의미화 파이프라인.
- **KPI·타임라인·리스크**: WP, 마일스톤, 윤리.
- **이메일/NotebookLM**: `email_analysis_and_insights.md`, `notebooklm_usage_strategy.md` — 내부 인사이트·도구 사용 전략.

### 3. 문헌·브리핑 (02_literature)

- **AI 기술 동향**: Flamingo/VLM, LeCun 월드모델·JEPA, 최예진 LLM 수수께끼, 터널 효과, NeuroX-Fusion·발달장애 AI 등.
- **기술 동향**: 뉴로모픽·양자 컴퓨팅, SNN·멤리스터, 하이브리드 컴퓨팅.
- **브리핑**: 뉴로모픽·AI·신경과학 융합 요약.
- **Neuromorphic & Analog KB**: Brain Foundation Models(BFM)·Digital Twin Brain(DTB)·Mamba/SSM·EEG FM·아날로그 하드웨어 논문 목록과 그랜트 서사(알고리즘·하드웨어·시뮬레이션).
- **Reading notes**: Inside-Out AI Revolution, 뇌에서 하이퍼코그니션까지 등 읽기 노트.

### 4. 제안서 (03_proposal)

- **아웃라인**: 2026-인공지능-014 타깃, 배경·목표·기술 접근·WP·리스크.
- **본문 초안**: `LLM 정렬 기반 멀티모달 뇌 파운데이션 모델 구축 연구 제안서.md` — 배경·목표(92B/125B/155B)·세부 목표·아키텍처(ViT, LTC, GNW, Titans SSM, MoE)·검증.
- **샘플 제안서**: ARPA, BrainLink, INCITE, QuantERA, 발달연구, 삼성 발달 등 참고용 요약/본문(MD).
- **README/template**: 제안서 폴더 구조·섹션 템플릿.

### 5. 컨텍스트·아이디어 (docs 루트)

- **CONTEXT.md**: IITP 014 과제 목표, 핵심 전략(선택적 수집, LTC, GNW, Titans, Predictive Coding), RFP·제안서 초안·기획 문서 경로, 팀 구조, 코딩 제약.
- **IdeaDeck_Summary.md**: “강건·효율적 다중감각 통합 지능”, LTC·GNW·Titans·멀티센서 동기화·Digital Brain Twin·평가 프레임.

### 6. 운영·설계 (06_admin)

- **DESIGN_RAG_NVINGEST_AI_COSCIENTIST.md**: 00IITP-AI ↔ k-bfm RAG·AI-CoScientist·nv-ingest 연동 설계.
- **notebooklm_capture_plan.md**, **source_registry.md**: NotebookLM 캡처 계획, 외부 근거자료 등록.

**한 줄 요약**:  
MD들은 **IITP 2026-인공지능-014(인지 기반 데이터 의미화)** 제안을 위한 **RFP 요약, 비전·전략·기획, AI/뉴로모픽 문헌 브리핑, BFM/SSM 논문 KB, 제안서 아웃라인·본문 초안, 컨텍스트·아이디어덱 요약, RAG 연동 설계** 등이 주 내용입니다.
