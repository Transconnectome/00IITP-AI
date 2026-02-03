# 🧑‍🔬 연구원 협업 가이드 (Overleaf Only Mode)
**Project**: IITP 2026 Embodied Neuro-AI Proposal

---

## 🚨 정책 변경: Overleaf 단일화
**2026.02.03 부로 모든 제안서 작업(텍스트, 그림)은 `Overleaf`에서 직접 수행합니다.**
Git/Markdown 기반의 작업은 중단되었습니다.

---

## 1. 작업 방법 (How to Work)

### A. 텍스트 및 수식 (Text & Math)
*   **접속**: Team Overleaf 프로젝트에 접속합니다.
*   **수정**: `.tex` 파일을 직접 수정합니다.
    *   `main.tex`: 전체 구조 관리.
    *   `sections/`: 챕터별 내용 (`01_architecture.tex` 등).

### B. 그림 (Figures)
*   **업로드**: Overleaf 웹사이트의 'Upload' 버튼을 사용하여 `graphics/` 폴더에 이미지를 직접 올립니다.
*   **Git 사용 안 함**: 그림을 Git에 올리고 스크립트로 동기화하던 기존 방식은 **더 이상 사용하지 않습니다.** (원한다면 백업용으로 Git에 올릴 수는 있지만, Overleaf에 자동으로 들어가지 않습니다).

---

## 2. Git 저장소의 역할 (00IITP-AI)
이 저장소(`00IITP-AI`)는 이제 **"코드 및 실험 데이터 아카이브"**의 역할만 수행합니다.
*   **제안서 백업**: 정기적으로 Overleaf 내용을 이 저장소로 **백업(Pull)**합니다.
*   **코드**: 모델 구현 코드, 실험 스크립트는 여전히 여기서 관리합니다.

### 백업 방법 (Backup)
Overleaf의 최신 내용을 로컬 Git으로 가져와서 안전하게 보관하고 싶다면:
```bash
./scripts/backup_from_overleaf.sh
```
*(기존 `universal_push.sh`는 이 스크립트로 대체되었습니다)*

---

## 3. 금지 사항
*   ❌ **`deploy_to_overleaf.sh` 실행 절대 금지**: 로컬의 낡은 Markdown 내용으로 Overleaf의 최신 작업을 덮어씌우게 됩니다. 절대 실행하지 마십시오.
