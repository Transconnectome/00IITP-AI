# [IITP 다중감각 통합 지능 과제] 1차년도 정기 줌 미팅 발표 슬라이드 (3장)

- **일시**: 2026-10-29 (목) 14:00–15:00 KST (Zoom, 성균관대 홍석준 교수 주관)
- **과제**: 정보통신기획평가원(IITP) 다중감각 통합 지능 과제 (`RS-2026-25518389`)
- **발표 단위**: 연구 1-4 (서울대학교 뇌인지과학과·심리학과 차지욱 교수팀)

## 1. 이메일 요청 및 회신 현황 (2026-10-21 ~ 2026-10-29)

1. **슬라이드 3장 작성 요청 메일** (`threadId: 1a15dd046792af65`, 제목: `[다중감각 통합 지능 과제] 1차년도 회의 발표 슬라이드 3장 작성 요청`, 2026-10-21 18:34 발송)
   - **수신자**: 배상윤 선생님 (`stellasybae@snu.ac.kr`, 슬라이드 1 `PIMSM`), 이세빈 선생님 (`wallen@snu.ac.kr`) · 이태양 선생님 (`rlaxodid5539@snu.ac.kr`, 슬라이드 2 `GINR`), 왕희환 선생님 (`dhkdgmlghks@snu.ac.kr`, 슬라이드 3 `VLM`)
   - **참고**: 최주빈 선생님 (`wnqlszoq123@snu.ac.kr`)은 해당 메일 수신자에 포함되지 않았으며, 2026-10-19 `Transconnectome/SwiFT_v2` PR #80 (`SwiFT V2` 미팅 Google Slides: https://docs.google.com/presentation/d/1s4q0xGuS7BhbnsDxarKag0RuuhBKXrpFuZnp4XQ_yeI/edit) 및 2026-10-21 NVIDIA AI for Science Forum 스레드(`1a15cbc6aa76ce0b`)에서 슬라이드·발표 관련 연락이 확인됨.
2. **학생 연구원 회신 현황 (질문 대기 상태)**
   - **배상윤 선생님** (`1a15e080304917b8`, 2026-10-21 19:35): *"PIMSM은 내용이 많이 변경된 상태이고 (just re-framing and additional theory touch-up), arxiv에는 인당 한 달에 2개 제출 제한에 걸려서 11월에 수정본을 올려야 하는 상황인데 수정본 (ICLR 2027 제출본)을 기준으로 하면 될까요?"* → **본 통합본에서는 ICLR 2027 제출본(`PALM`, #39398) 및 기존 사전공개본(`arXiv:2605.16351`)을 모두 아울러 반영함.**
   - **이태양 선생님** (`1a15e7e40ce0445e`, 2026-10-21 21:44): *"말씀주신 GINR의 정의에 온전히 맞는 것은 세빈썜의 Signerd이고 기존 SOLID-EEG의 경우 GINR이라는 개념에 완벽히 들어맞지는 않습니다. GINR의 정의에 딱 맞는 Signerd 내용만 넣으면 되는 것일까요? 아니면 정의상으로는 약간 다르더라도 SOLID도 함께 넣는 것이 나을까요?"* → **본 통합본에서는 트랙 A(`NeuroX-Field / SigNerd`, 순수 생성형 신경장)와 트랙 B(`NeuroX-EEG / SOLID-EEG`, 기초모델 정렬 확산 초해상화 + `fMRI-GINR`)를 두 상보적 트랙으로 함께 수록함.**
   - **왕희환 선생님**: 별도 이메일 회신 없었으나, 연구실 레포 및 ICLR 2027 제출본(`CALIBRA-fMRI / BrainVLM`, #26688), `Mind the Gap` (`arXiv:2502.12771`), `SwiFT V2` (최주빈·왕희환 선생님) 원고·슬라이드에서 정본 수치를 추출하여 슬라이드 3에 통합함.

## 2. 슬라이드 구성 (전면 한글 · 약어 풀어쓰기 · 비전공자 친화 16:9 3장)

| 슬라이드 | 세부 주제 | 담당 연구원 | 수록 핵심 연구 및 논문 상태 |
|---|---|---|---|
| **Slide 1** | 뇌 고유 리듬을 이식한 물리 정보 기반 뇌 동역학 모델 (`PALM / 구 PIMSM`) | 배상윤 선생님 | `PALM` (ICLR 2027 #39398 심사 중, `arXiv:2605.16351`), `MBBN` (*Communications Biology* 심사 중, `arXiv:2503.23394`), `INCAMA` (*Nature Communications* 준비, `arXiv:2510.17318`) |
| **Slide 2** | 생성형 내재 신경 표현 기반 뇌신호 초해상화·결측 복원 (`GINR: SigNerd & SOLID`) | 이세빈 · 이태양 선생님 | `NeuroX-Field / SigNerd` (ICML 2027 준비, SNU-BNL 공동연구), `NeuroX-EEG / SOLID-EEG` (ICLR 2027 #53005 심사 중), `fMRI/dMRI GINR` (*Nature Methods* 준비) |
| **Slide 3** | 시각언어모델 연계 뇌 해독 (`BrainVLM`) 및 대규모 뇌 기초모델 (`SwiFT V2`) | 왕희환 · 최주빈 선생님 | `BrainVLM / CALIBRA-fMRI` (ICLR 2027 #26688 심사 중), `Mind the Gap` (`arXiv:2502.12771`), `SwiFT V2` (*Nature Communications* 준비, 선행 NeurIPS `arXiv:2307.05916`) |

## 3. 산출물 파일 및 Google Slides 링크

- **Google Slides (텍스트·표·도형 직접 편집본 — 간결 개조식 + 발표자 노트 포함)**: https://docs.google.com/presentation/d/1vdUSFLc4JQ2ED45ndICzY2mVzb-CuSjqmvBq7VwWmBE/edit
- **Google Slides (고해상도 레이아웃 고정본 — 간결 개조식 + 발표자 노트 포함)**: https://docs.google.com/presentation/d/1BTERJq6zJGULP6Wz0q2g8c8y_URba0i3pltqgNUnCyI/edit
- [slides.md](./slides.md): `cha-marp` (`cha-editorial` 테마) 정본 마크다운
- [output/slides.pdf](./output/slides.pdf): 고해상도 발표용 PDF (Pretendard 폰트 임베딩, PDF QA 통과)
- [output/IITP_1차년도_연구1-4_서울대_차지욱팀_편집용.pptx](./output/IITP_1차년도_연구1-4_서울대_차지욱팀_편집용.pptx): 텍스트·표·도형 직접 편집이 가능한 PowerPoint 파일 (`python-pptx` 생성)
- [output/slides.pptx](./output/slides.pptx): 레이아웃 100% 고정형(래스터) PowerPoint 파일
- [output/slides.html](./output/slides.html): 브라우저 발표용 단독 HTML 파일
- `output/preview/page-001.png` ~ `page-003.png`: 슬라이드별 시각 검수용 PNG
