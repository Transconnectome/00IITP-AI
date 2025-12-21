# NotebookLM → Proposal Evidence: Capture Plan (MCP/Playwright)

NotebookLM 노트는 “제안서 근거(문헌/요약/인사이트)”로 매우 유용하지만, 보통 **로그인 기반**이고 내용이 동적으로 로드됩니다.  
따라서 제안서 작업에 쓰려면 **(a) 링크**, **(b) 캡처본(텍스트/스크린샷/HTML)**, **(c) 사용 위치(제안서 섹션)**를 함께 관리해야 합니다.

관련 원본 링크:

- [NotebookLM notebook 644472d6-3a23-45a7-8d7c-7f218e7c14b4](https://notebooklm.google.com/notebook/644472d6-3a23-45a7-8d7c-7f218e7c14b4)
- [NotebookLM notebook 7acc2737-c783-43ff-af4c-e360ad02cf2c](https://notebooklm.google.com/notebook/7acc2737-c783-43ff-af4c-e360ad02cf2c)

---

## 목표

- NotebookLM의 핵심 내용을 **제안서에 인용 가능한 증거(evidence)**로 변환
- 팀 내부에서 **재현 가능**하고 **버전 관리 가능**하게 저장
- 평가항목/주장/차별성에 **직접 연결**되도록 태깅

---

## 저장 위치(레포 규칙)

- 캡처 결과물: `docs/03_proposal/references/notebooklm/`
- 출처 등록: `docs/06_admin/source_registry.md`

권장 파일명:

- `YYYY-MM-DD_notebooklm_<notebook-id>_snapshot.html`
- `YYYY-MM-DD_notebooklm_<notebook-id>_screenshot.png`
- `YYYY-MM-DD_notebooklm_<notebook-id>_extracted.txt`
- `YYYY-MM-DD_notebooklm_<notebook-id>_evidence.md` (제안서용 요약/인용문)

---

## 접근 방식 A (권장/가장 안정): 수동 Export + 레포 정리

1. NotebookLM에서 **필요한 텍스트/요약/인용문**을 “복사”
2. `docs/03_proposal/references/notebooklm/`에 `..._evidence.md`로 정리
3. 스크린샷을 함께 저장(핵심 근거 화면)
4. `docs/06_admin/source_registry.md`에서 해당 근거가 쓰인 제안서 섹션을 연결

장점: UI 변화/자동화 실패에 강함  
단점: 수작업

---

## 접근 방식 B: Playwright(자동화)로 캡처본 생성 (옵션)

**상황**: NotebookLM은 로그인/동적 로드라서 단순 `curl`/스크래핑이 불안정합니다.  
따라서 Playwright를 쓸 때는 **Persistent profile**(브라우저 프로필 디렉터리)을 사용합니다.

### B-1. 운영 원칙

- **계정/비밀번호/토큰을 레포에 저장하지 않기**
- 최초 1회는 `headless=false`로 실행해 **사용자가 직접 로그인**
- 이후에는 동일한 `user-data-dir`로 세션을 재사용(로그인 유지)

### B-2. 산출물

스크립트가 URL마다 아래를 생성:

- screenshot (`.png`)
- page HTML (`.html`)
- body text (`.txt`)

추가로 사람이 `..._evidence.md`로 “제안서에 들어갈 형태”로 정리

### B-3. 스크립트 위치

- `scripts/notebooklm_capture.py` (추가됨)

---

## 접근 방식 C: Cursor MCP 브라우저(Playwright 유사)로 캡처 (옵션)

Cursor의 브라우저 MCP 도구로도 동일하게 할 수 있습니다:

- `browser_navigate`로 NotebookLM 페이지 열기
- (로그인이 필요하면) 브라우저 세션에서 로그인 상태 확보
- `browser_snapshot`/스크린샷으로 핵심 내용을 캡처
- 레포에 `..._evidence.md`로 정리

> 실무적으로는 **A(수동 정리)** + **B/C(자동 캡처 보조)** 조합이 가장 안정적입니다.


