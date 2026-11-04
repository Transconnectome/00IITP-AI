# HANDOFF — IITP 다중감각 통합 지능 과제 (`RS-2026-25518389`) 1차년도 회의 준비

> 최종 갱신 **2026-10-29**. 이 문서부터 읽고 시작할 것.
> 🔴 정본 = `main` (`e380802`) · `/home/juke/git/00IITP-AI`. 워크트리 1개 확인(`git worktree list`, 2026-10-29 11:30 KST 실측).
> 읽기 순서: 이 파일 → `/home/juke/git/00IITP-AI/docs/05_meetings/2026-10-29_y1_slides/README.md`(오늘 14:00 줌 미팅용 3장 통합 슬라이드) → `/home/juke/.agents/registry/onboarding/iitp-brain-ai/r1/brief.md`(미팅 브리프 정본) → `/home/juke/git/00IITP-AI/_proposal_[제출]1_신청용연구개발계획서(기술개발사업)_[표지][요약][본문1][본문2]_FN.pdf`(최종 제출 계획서 89쪽). `/home/juke/git/00IITP-AI/docs/03_proposal/PROPOSAL_PLAN.md`는 서울대 내부 초기 기획본(이력 참고용).

## 0. 한 줄 상태 ★

**2026-10-29 (목) 14:00–15:00 IITP 정기 줌 미팅(`연구 1-4`, 서울대 차지욱 교수팀)을 위해, 이메일 스레드(`1a15dd046792af65`)의 학생 질문 사항(배상윤 선생님 `PALM` ICLR 2027 개정본 기준 여부, 이태양 선생님 `SigNerd + SOLID` 병기 여부)과 연구실 최신 원고·슬라이드(`SwiFT V2` 최주빈·왕희환 선생님 포함)를 모두 반영한 전면 한글·약어 풀어쓰기 3장 통합 발표 슬라이드(`PDF`, `편집용 PPTX`, `고정형 PPTX`, `HTML`) 제작 및 시각 검수를 완료했다.**

- ✅ **1차년도(`연구 1-4`) 3장 통합 발표 슬라이드 제작 완료** (2026-10-29 11:30 KST, `build_pdf.py` PDF QA PASS): `/home/juke/git/00IITP-AI/docs/05_meetings/2026-10-29_y1_slides/output/slides.pdf` (`519 KB`), 편집용 PowerPoint `output/IITP_1차년도_연구1-4_서울대_차지욱팀_편집용.pptx` (`929 KB`), 고정형 `output/slides.pptx` (`1.8 MB`), `output/slides.html` (`4.2 MB`).
- ✅ **차교수 미팅 온보딩 브리프 및 인포그래픽 생성 완료** (2026-10-21 11:57 KST, `onboarding.py render iitp-brain-ai` exit 0 통과): `/home/juke/.agents/registry/onboarding/iitp-brain-ai/r1/brief.html`.
- ✅ **슬라이드 요청 메일 스레드(`1a15dd046792af65`) 실측 결과**: 2026-10-21 18:34 발송 메일 수신자는 배상윤·이세빈·이태양·왕희환 선생님 4명(최주빈 선생님은 미포함이나 10/19 `SwiFT V2` 미팅 슬라이드 PR #80 및 10/21 NVIDIA 포럼 메일에서 확인)이었으며, 10/21 저녁 배상윤 선생님(19:35, `PALM` ICLR 2027 수정본 기준 여부 질문)과 이태양 선생님(21:44, `SigNerd` 단독 vs `SOLID` 병기 질문)의 문의 메일 이후 답장이 대기 중이어서 학생 개별 슬라이드 첨부본은 아직 수신되지 않음. 이에 두 질문에 대한 포괄적 해답(`PALM` ICLR 2027 본 + `SigNerd & SOLID` 양대 트랙 + `BrainVLM & SwiFT V2`)으로 3장 통합본을 직접 구성함.
- 🔴 **워킹트리 미커밋 변경 잔존** (`git -C /home/juke/git/00IITP-AI status --short`): `M docs/qa_prep_차지욱_20260309.md`, `?? .agent/workflows/k-bfm-exec.md`, `?? docker-compose-chatbot.yml`, `?? HANDOFF.md`, `?? docs/05_meetings/2026-10-29_y1_slides/`.

## 1. 사실 표 (과제·연차별 과업·슬라이드 배정)

| 항목 | 값 | 출처 |
|---|---|---|
| 과제번호 / 과제명 | `RS-2026-25518389` (RFP `2026-AI-014`) / 「강건하고 효율적인 다중감각 통합 지능: 개념 주도의 선택적 주의 기반 지각 모사 접근법 개발」 | `/home/juke/git/00IITP-AI/_proposal_[제출]1_신청용연구개발계획서(기술개발사업)_[표지][요약][본문1][본문2]_FN.pdf` p.2 |
| 기간 / 예산 / 컨소시엄 | 2026.04.01 ~ 2029.12.31 (4년, 총 114.5억 원) / 주관 성균관대(홍석준), 공동1 서울대(최명환·차지욱·김성연), 공동2 연세대(김병훈), 공동3 ETRI(김성환), 공동4 한국뇌연구원(김기범) | 위 계획서 PDF p.2, p.48 |
| 1차년도 차지욱 교수 과업 (`연구 1-4`) | ① `Multi-Scale SSM(Mamba)+GINR 기반 Vision-Language FM 프로토타입 v0.1 구축` (단독: 차지욱) / ② `VLM FM 튜닝/통합 및 모델/데이터 핸드오프 규격 확정` (공동: 차지욱·김병훈) + 항상성 RL 제어기 | 위 계획서 PDF p.20–21, p.26–27, p.43 |
| 2~4차년도 차지욱 교수 과업 | • 2차년도(`연구 1-12`): `Vision-Language-Neural FM (NeuroX)` 구축 + Brain Signal-Driven Tuning(SwiFT V2, NeuroMamba, DIVER) + Titans 장기기억<br>• 3차년도(`연구 2-4`): 설치류-영장류-인간 비쌍 데이터 종간 정렬(GINR+CEBRA+GWOT, RSA $> 0.5$, Zero-shot $> 60\%$)<br>• 4차년도(`연구 2-7`): Multi-Billion 스케일업, 연산 50% 절감 및 실시간($< 50\text{ms}$) Sim-to-Real 전이 | 위 계획서 PDF p.21–23, p.33–34, p.43–44 |
| **Slide 1 (PIMSM 연구)** | **배상윤** (`stellasybae@snu.ac.kr`) — `PIMSM / PALM` (ICLR 2027 `#39398` 투고, `https://arxiv.org/abs/2605.16351`), 선행 `MBBN` (`https://arxiv.org/abs/2503.23394`), `INCAMA` (`https://arxiv.org/abs/2510.17318`) | Gmail `1a15dd046792af65` / `/home/juke/git/paper-review/HANDOFF_ICLR2027_FINAL_TOUCH.md` |
| **Slide 2 (GINR 연구)** | **이세빈** (`wallen@snu.ac.kr`), **이태양** (`rlaxodid5539@snu.ac.kr`) — `NeuroX-Field` (`Transconnectome/SigNerd`, CVPR/ICML 2027 및 arXiv 준비), `NeuroX-EEG` (ICLR 2027 `#53005` 투고), `fmri_stsr` | Gmail `1a15dd046792af65` / `/home/juke/.agents/registry/student_progress/latest.json` |
| **Slide 3 (VLM 연구)** | **왕희환** (`dhkdgmlghks@snu.ac.kr`) — `BrainVLM / CALIBRA-fMRI` (ICLR 2027 `#26688` 투고), `Mind the Gap` (`https://arxiv.org/abs/2502.12771`), `SwiFT V2` (`Transconnectome/SwiFT_v2_paper`) | Gmail `1a15dd046792af65` / `/home/juke/.agents/registry/student_progress/latest.json` |

## 2. 사용자 철학·결정

- **슬라이드 3장 분담 및 작성 원칙 (2026-10-21 확정)**:
  - "슬라이드 3장에 각각 한장씩 작업하면 되겠다. pimsm 연구--배상윤, ginr--이세빈 이태양, vlm--왕희환 에게 요청하자. 페이퍼 진행 상황과 preprint link도 포함해서"
  - "잘 모르는 사람들도 이해할 수 있도록 풀어서 설명해주시고, 한글로, 모든 acronym은 풀어서 쓰던가 일반적인 설명으로 대체 해달라고 수정"
- 이에 따라 각 슬라이드(16:9, 1장)는 ① **비전공자·타 세부 연구진도 직관적으로 이해할 수 있는 쉬운 설명**, ② **전면 한글 작성**, ③ **모든 영문 약어(acronym) 풀어 쓰기 또는 쉬운 일반 설명 대체**, ④ **핵심 개념도 1개 + 주요 결과 표/그래프 1개 + 하단 논문 진행 상황 및 사전공개본(preprint) 링크 포함**을 필수 요건으로 지정하여 발송함.

## 3. 산출물 지도 ★

| 파일 | 내용 | 상태 |
|---|---|---|
| `https://docs.google.com/presentation/d/1vdUSFLc4JQ2ED45ndICzY2mVzb-CuSjqmvBq7VwWmBE/edit` | 2026-10-29 14:00 1차년도 회의용 Google Slides 3장 (간결 개조식 · 텍스트·표·도형 직접 편집본 + 발표자 노트) | ✅ 정본 (Google Slides) |
| `https://docs.google.com/presentation/d/1BTERJq6zJGULP6Wz0q2g8c8y_URba0i3pltqgNUnCyI/edit` | 2026-10-29 14:00 1차년도 회의용 Google Slides 3장 (간결 개조식 · 고해상도 레이아웃 고정본 + 발표자 노트) | ✅ 정본 (Google Slides) |
| `/home/juke/git/00IITP-AI/docs/05_meetings/2026-10-29_y1_slides/output/slides.pdf` | 2026-10-29 14:00 1차년도 회의용 3장 통합 발표 슬라이드 PDF (`PALM`, `GINR: SigNerd & SOLID`, `BrainVLM & SwiFT V2`) | ✅ 정본 (`build_pdf.py` PDF QA PASS) |
| `/home/juke/git/00IITP-AI/docs/05_meetings/2026-10-29_y1_slides/output/IITP_1차년도_연구1-4_서울대_차지욱팀_편집용.pptx` | 텍스트·표·도형 직접 편집이 가능한 PowerPoint 3장 (`python-pptx`) | ✅ 정본 (편집용 PPTX) |
| `/home/juke/git/00IITP-AI/docs/05_meetings/2026-10-29_y1_slides/slides.md` | `cha-marp` (`cha-editorial`) 3장 슬라이드 마크다운 원본 + `figures/s01~s03_concept.svg` | ✅ 정본 |
| `/home/juke/git/00IITP-AI/_proposal_[제출]1_신청용연구개발계획서(기술개발사업)_[표지][요약][본문1][본문2]_FN.pdf` | 5개 기관 컨소시엄 최종 제출 연구개발계획서 (89쪽) | ✅ 정본 (커밋됨 `d04ff01`) |
| `/home/juke/.agents/registry/onboarding/iitp-brain-ai/r1/brief.html` | IITP 미팅 온보딩 브리프 HTML + 인포그래픽 2종(`S1.png`, `S2.png`) | ✅ 정본 (`onboarding.py render` 통과, 서고 보관) |
| `/home/juke/.agents/registry/onboarding/iitp-brain-ai/r1/brief.md` | 미팅 브리프 마크다운 원본 (3,915자, 근거 참조 34건) | ✅ 정본 (서고 보관) |
| `/home/juke/.agents/registry/onboarding/iitp-brain-ai/meetings.md` | 2026-10-21 미팅 결정 로그 (`onboarding.py log`) | ✅ 정본 (서고 보관) |
| `/home/juke/.gemini/antigravity-cli/brain/be86b22d-07cb-4052-8a05-0d945b3e23c9/scratch/iitp_slide_request_email.txt` | 학생 4명 앞 발송된 슬라이드 3장 요청 메일 원문 (`cleaner.py --check-email --internal` exit 0) | ✅ 발송 완료 (`messageId: 1a15dd046792af65`) |
| `/home/juke/git/00IITP-AI/docs/qa_prep_차지욱_20260309.md` | 2026-03-09 발표평가용 22문항 심층 기술 Q&A 방어집 | ⚠️ 워킹트리 미커밋 수정 있음 (`+352/-22 lines`) |
| `/home/juke/git/00IITP-AI/docs/03_proposal/PROPOSAL_PLAN.md` | 서울대 내부 초기 기획안 (3-Part 내수용성 루프: Neuro-GINR + Drive-Managed Titans + SWR Replay) | 이력 참고용 · 최종 제출 계획서(89쪽)와 구분 |
| `/home/juke/git/proposals/proposals/2026-iitp-ai-wonchun-intent/reader_eval/final_fields.json` | 2028 IITP AI 미래도약 원천기술개발사업 참여의향서 최종 문안 (폐루프 가설 생성 학습 원리) | ✅ 정본 (`proposals` 레포 `0748416`) |

## 4. 🔴 지금 막혀 있는 것 ★

### ① 학생 4명의 슬라이드 3장 회신 대기 (사람 전용)
- **무엇이 막혔나**: 배상윤(Slide 1: PIMSM), 이세빈·이태양(Slide 2: GINR), 왕희환(Slide 3: VLM)에게 2026-10-21 18:34 KST에 요청 메일(`threadId: 1a15dd046792af65`)을 발송했으며, 학생들의 슬라이드 제작 및 회신이 도착해야 통합 덱(3장) 검수·취합이 가능함.
- **누가 풀 수 있나**: 배상윤, 이세빈, 이태양, 왕희환 (회신 도착 시 에이전트가 취합 및 약어·가독성 검수 수행 가능).

### ② `00IITP-AI` 및 `proposals` 워킹트리 미커밋 파일 정리 여부 (PI 결정 필요)
- **무엇이 막혔나**:
  - `/home/juke/git/00IITP-AI`: 2026년 3월 발표평가 당시 수정된 `docs/qa_prep_차지욱_20260309.md` (`+352/-22 lines`) 및 미추적 파일(`.agent/workflows/k-bfm-exec.md`, `docker-compose-chatbot.yml`, `HANDOFF.md`)이 미커밋 상태임.
  - `/home/juke/git/proposals`: `proposals/2026-iitp-ai-wonchun-intent/submission/final/` 등 미추적 폴더 4건이 남아 있음.
- **누가 풀 수 있나**: PI 승인 후 선별 `git add` 및 커밋.

## 5. 다음 단계 ★

1. **슬라이드 회신 확인 및 4대 기준 검수 (에이전트 + PI)**:
   - Gmail 스레드 `1a15dd046792af65` (`gog gmail get 1a15dd046792af65` 또는 `gog gmail search "threadId:1a15dd046792af65"`)에서 4명의 회신(PPTX 또는 Google Slides 링크) 수신 여부 확인.
   - 도착한 슬라이드 3장이 ① 비전공자 눈높이 설명, ② 한글 작성, ③ 모든 영문 약어 풀어쓰기/일반 설명 대체, ④ 핵심 도식 1개 + 결과 표/그래프 1개 + 논문 진행 상황 및 preprint 링크 포함 조건을 충족하는지 점검 후 3장 통합본 제작.
2. **1차년도 VLM 데이터/모델 핸드오프 규격 점검 (회의 안건)**:
   - 계획서 `연구 1-4` 두 번째 과업(`VLM FM 튜닝/통합 및 모델/데이터 핸드오프 규격 확정`)에 맞춰 공동2(연세대 김병훈 교수팀 `연구 1-5`) 및 주관(성균관대 홍석준 교수팀 `연구 1-2`)과의 입출력 인터페이스 논의.
3. **워킹트리 정본 커밋 정리**:
   - `/home/juke/git/00IITP-AI/HANDOFF.md` 및 `/home/juke/git/proposals/proposals/2026-iitp-ai-wonchun-intent/submission/final/` 커밋 여부 확정.

## 6. 함정 (실측된 것만) ★

### 사실 관계
- **초기 서울대 내부 기획안(`PROPOSAL_PLAN.md`, `그랜트아이디어.md`)과 최종 제출 컨소시엄 계획서(`_proposal_..._FN.pdf`)의 구분**:
  - 초기 기획안은 차지욱·김성연 교수의 `Inside-Out + 3-Part 내수용성 루프(Neuro-GINR + Drive-Managed Titans + SWR Replay)` 중심이나, 5개 기관이 합쳐진 최종 제출 계획서(89쪽)에서는 차지욱 교수팀 과업이 연차별로 **1차년도(`연구 1-4`: PIMSM + GINR + 항상성 RL 기반 Vision-Language FM 프로토타입 v0.1)** → **2차년도(`연구 1-12`: SwiFT V2/NeuroMamba/DIVER 뇌 신호 튜닝 `NeuroX` + Titans)** → **3차년도(`연구 2-4`: 설치류-영장류-인간 종간 정렬)** → **4차년도(`연구 2-7`: Multi-Billion 스케일업 및 $<50\text{ms}$ Sim-to-Real)**로 구조화되어 있음.
- **타 레포 인벤토리의 표기 불일치 주의**:
  - `/home/juke/git/proposals/proposals/2026-iitp-ai-wonchun-intent/evidence/inventory.md`(L15) 및 `/home/juke/git/tenure-review-2027/HANDOFF.md`(L22, L49)에는 본 과제가 '선정 미확인 / 미선정 Co-PI 과제'로 적혀 있으나, 실제 1차년도 회의 및 슬라이드 준비가 진행 중이므로 대외 제안서 인벤토리 표기와 실제 컨소시엄 회의 일정을 혼동하지 말 것.

### 도구
- **`cha-onboarding` 검사기(`onboarding.py check`) 규칙**:
  - `brief.md`에서 ` 축`(앞에 공백이 있는 명사 '축')은 AI 상투어 정규식(`AI_TONE`)에 걸려 실패(exit 2)하므로 '영역', '과업', '모듈'로 대체해야 하며, 인포그래픽 `레이블:` 구분자는 쉼표(`,`)가 아니라 파이프(`|`)를 써야 함.
- **`cha-writer` 이메일 검사기(`cleaner.py --check-email`) 규칙**:
  - 한 문장이 120자를 넘으면 즉시 `exit 2`로 실패하므로 개조식 항목도 마침표 단위로 120자 이내 단문으로 쪼개야 통과함.

## 7. 재료 정본 (읽기 전용)

| 재료 | 경로 |
|---|---|
| 2026 IITP 다중감각 통합 지능 최종 제출 계획서 (89쪽 PDF) | `/home/juke/git/00IITP-AI/_proposal_[제출]1_신청용연구개발계획서(기술개발사업)_[표지][요약][본문1][본문2]_FN.pdf` |
| 발표평가용 압축 슬라이드 (2.4MB PDF) | `/home/juke/git/00IITP-AI/_presentation_0304_발표자료_강건하고효율적인다중감각통합지능_홍석준_compressed.pdf` |
| 차지욱 교수 전담 22문항 Q&A 방어집 | `/home/juke/git/00IITP-AI/docs/qa_prep_차지욱_20260309.md` |
| 차교수 온보딩 서고 (브리프·인포그래픽·리더 JSON·미팅 로그) | `/home/juke/.agents/registry/onboarding/iitp-brain-ai/r1/` |
| 지도 학생 연구 진도 및 레포 현황 정본 | `/home/juke/.agents/registry/student_progress/latest.json` |
| ICLR 2027 투고 논문 목록 및 상태 정본 | `/home/juke/git/paper-review/HANDOFF_ICLR2027_FINAL_TOUCH.md` |
