# 🧑‍🔬 연구원 협업 가이드 (Researcher Collaboration Guide)
**Project**: IITP 2026 Embodied Neuro-AI Proposal

본 가이드는 연구원들이 제안서 작업에 참여할 때 **"어디서 작업하고, 어떻게 동기화하는지"**에 대한 표준 절차를 정의합니다.

---

## 1. 🚀 필수 Git Repository
연구원이 작업해야 할 **유일한** 저장소는 다음과 같습니다:
*   **Repo Name**: `00IITP-AI` (The Research Hub)
*   **Role**: 코드, 실험, 제안서 초안(Markdown), 이미지 원본 관리.
*   **Clone**:
    ```bash
    git clone https://github.com/StartUp-Research/00IITP-AI.git
    cd 00IITP-AI
    ```
    > ⚠️ **주의**: `IITP-2026-Proposal` 저장소는 Overleaf 연동용이므로 직접 건드리지 마십시오.

## 2. ✍️ 제안서 작성 방법 (Markdown First)
우리는 **"Markdown 우선 정책"**을 따릅니다. Overleaf에서 직접 텍스트를 수정하면, 나중에 Markdown 변환본에 의해 덮어씌워져 내용이 유실될 수 있습니다.

### 작업 위치 (Files to Edit)
텍스트는 아래 경로의 Markdown 파일들을 수정합니다:
*   `docs/03_proposal/drafts/00_executive_summary.md` (요약)
*   `docs/03_proposal/drafts/01_architecture.md` (1장 아키텍처)
*   `docs/03_proposal/drafts/02_methodology.md` (2장 방법론)
*   `docs/03_proposal/drafts/03_allostasis.md` (3장 알로스태시스)
*   `docs/03_proposal/drafts/04_validation.md` (4장 검증계획)

### 작업 순서
1.  `00IITP-AI` 저장소에서 `git pull` 로 최신본 받기.
2.  `docs/03_proposal/drafts/` 내의 Markdown 파일 수정.
3.  수정이 끝나면 동기화 스크립트 실행.

## 3. 🔄 Overleaf 동기화 및 직접 수정 (Sync Policy)
기본적으로 **"Markdown First"**를 권장하지만, 표(Table)나 수식(Math) 등 정교한 작업이 필요한 경우 **Overleaf에서 직접 수정**해도 됩니다.

### [Option A] Markdown 위주 작업 (권장)
*   내용 작성은 Markdown에서 하고, `./scripts/universal_push.sh`로 Overleaf에 반영합니다.
*   **장점**: 버전 관리가 쉽고 충돌이 적음.

### [Option B] Overleaf 직접 수정 (Phase Shift)
Overleaf의 **"Push Overleaf changes to GitHub"** 버튼을 사용하여 작업을 저장할 수 있습니다.
*   💰 **유료 기능**: 이 기능은 Overleaf **Premium (Paid)** 계정 사용자만 가능할 수 있습니다. (Guest나 Free 유저는 버튼이 안 보일 수 있음).
*   ✅ **가능합니다**: 만약 가능하다면, 이 기능을 써서 `IITP-2026-Proposal` 저장소를 업데이트할 수 있습니다.
*   ⚠️ **중요한 점 (One-Way Door)**: Overleaf에서 수정한 내용은 **LaTeX 파일(.tex)**입니다. 이것이 우리 로컬의 **Markdown 파일(.md)**을 자동으로 수정해주지는 않습니다.
    *   즉, 이 기능을 본격적으로 쓰기 시작하면 **"Markdown 편집을 중단하고 LaTeX 체제(Overleaf)로 완전히 넘어가는 것"**을 의미합니다.
    *   Markdown과 Overleaf를 오가며 작업하려면, Overleaf 수정본을 보고 Markdown을 수동으로 고쳐야 합니다.

### [Option C] 하이브리드 동기화 (고급)
Overleaf에서 수정한 내용을 로컬로 가져오려면:
```bash
cd export_pkg
git pull origin main  # Overleaf에서 Push한 내용을 가져옴
# (주의: 가져온 내용은 .tex 파일이며, .md 파일은 여전히 옛날 상태임)
```

## 4. 📄 Overleaf 사용 규칙
Overleaf 사이트에서는 **PDF 확인 및 레이아웃 조정**만 수행하십시오.

*   **참고문헌**: `tex/references.bib`는 양쪽 어디서든 수정 가능하지만, 되도록 Git(`00IITP-AI`)에서 관리하는 것을 추천합니다.


## 5. 🆘 문제 해결
*   **Sync 실패?**: `git pull`을 먼저 해서 충돌을 해결하십시오.
*   **이미지 안 보임?**: `docs/05_figures/`에 파일이 있는지, 파일명이 영어인지 확인하십시오.

## 6. 🤝 외부 협업자 (External Collaborators) 대응
Git 사용이 어렵거나 Overleaf 계정이 없는 외부 연구원들과 협업할 때의 원칙입니다.

### Case A: PDF 검토 (권장)
*   **View**: Overleaf의 **"Read-Only Link"**나 **PDF 파일**을 공유하십시오.
*   **Integrate**: 수정 사항을 메일/Word로 받아 내부 연구원이 Markdown에 반영합니다. (가장 안전)

### Case B: Overleaf Guest 직접 수정
만약 Guest가 Overleaf에서 직접 수정했다면, 우리는 어떻게 저장소로 가져옵니까?
1.  **Sync (Owner)**: 프로젝트 소유자(Premium 유저)가 Overleaf에서 **"Push to GitHub"** 버튼을 눌러야 합니다. (Guest는 못 함)
2.  **Pull (Local)**:
    ```bash
    cd export_pkg
    git pull origin main  # Overleaf에서 Push된 내용을 로컬 LaTeX로 가져옴
    ```
3.  **Merge**: 가져온 `.tex` 파일 변경분을 확인하고, 로컬의 `.md` 파일에 수동으로 반영합니다.
    *   (⚠️ 매우 번거로우므로 Case A를 권장합니다)
