# 🧑‍🔬 연구원 협업 가이드 (Overleaf First)
**Project**: IITP 2026 Embodied Neuro-AI Proposal

---

## 🚨 핵심 변경 사항 (Overleaf First Policy)
이제부터 **제안서 텍스트의 원본(Source of Truth)**은 **Overleaf**입니다.
Markdown 파일은 더 이상 원본이 아니며, 단순 백업/참조용으로 전락합니다.

---

## 1. 작업 프로세스

### A. 텍스트 수정 (Text)
*   **어디서?**: **Overleaf 웹사이트**에서 직접 수정하십시오.
*   **주의**: 로컬의 Markdown 파일(`docs/03_proposal/drafts`)을 수정해도 반영되지 않습니다 (오히려 Overleaf 내용에 의해 덮어씌워질 수 있습니다).

### B. 그림 추가 (Figures)
그림은 여전히 로컬 Git에서 관리합니다.
1.  **생성**: `docs/05_figures/` 폴더에 이미지 파일(PNG/PDF)을 넣습니다.
2.  **업로드**: 터미널에서 다음 스크립트를 실행합니다.
    ```bash
    ./scripts/upload_figures.sh
    ```
3.  **사용**: Overleaf에서 `\includegraphics{graphics/filename.png}` 로 사용합니다.

### C. 최신 내용 가져오기 (Sync)
Overleaf에서 다른 사람이 수정한 내용을 내 로컬 저장소로 백업하려면:
```bash
./scripts/pull_from_overleaf.sh
```
> 이 명령은 Overleaf의 `.tex` 파일들을 내 로컬 `tex/` 폴더로 다운로드합니다.

---

## 2. 금지 사항 (Do Not Do This)
*   ❌ **`deploy_to_overleaf.sh` 실행 금지**: 이 스크립트는 로컬 Markdown 내용을 강제로 Overleaf에 덮어씌웁니다. **Overleaf에서 작업한 내용이 전부 삭제됩니다.** (정말 초기화가 필요한 경우에만 경고 메시지 확인 후 사용하세요).

---

## 3. GitHub 저장소 구조
*   `00IITP-AI` (이 저장소): 코드, 실험 데이터, 그림 원본, 그리고 **Overleaf 백업본**.
*   `IITP-2026-Proposal` (Overleaf 연동): Overleaf와 실시간 동기화되는 저장소. (직접 건드리지 마세요).
