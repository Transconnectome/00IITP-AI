# IITP 인공지능 제안서 전체 계획 (2026-014)

## 📌 현재 상태 (Status Dashboard)
| Phase | Task | Status | Note |
| :--- | :--- | :--- | :--- |
| **Phase 1** | 전략 및 아키텍처 수립 | ✅ **완료** | Two-Part Model, Allostasis |
| **Phase 2** | 제안서 초안 작성 (Drafting) | ✅ **완료** | Parts 1, 2, 3, 4 작성 및 Overleaf 연동 완료 |
| **Phase 2.5** | Overleaf 검수 & 시각화 | ✅ **완료** | 그림 삽입, 참고문헌 연동 완료 |
| **Phase 3** | **과학적 검증 (Validation)** | 🚀 **진행 중** | **Toy Model 구현 (Code)** |
| **Phase 4** | 최종 수정 (Refinement) | 📅 대기 중 | 학생 실험 결과 반영 예정 |

---

## 🏗️ Phase 3: Scientific Validation (Student Task)
현재 가장 시급한 과제는 **Toy Model** 구현입니다.

### **목표: "Dual Encoder + Titans Memory" 검증**
이 아키텍처가 단순한 이론이 아니라 실제 코드로 동작함을 보여줘야 합니다.

1.  **Repo**: [`snuconnectome/IITP-2026-Proposal`](https://github.com/snuconnectome/IITP-2026-Proposal) Clone.
2.  **Instruction**: `src/README_STUDENTS.md` 필독.
3.  **To-Do**:
    *   `src/titans_demo.py` 작성.
    *   **Input**: Moving MNIST + Synthetic Brain Signal (Sine+Noise).
    *   **Architecture**: CNN + LTC -> Features -> Titans Memory.
    *   **Evaluation**: Novelty Detection (Surprise High?) & Recall Accuracy.

---

## 📜 문서 구조 및 상태 확인

### **제1장: 듀얼 인코더 & Titans 통합 아키텍처**
-   **Status**: ✅ Drafted (`drafts/01_architecture.md`)
-   **내용**: Sensory-Motor + Brain Encoder 구조 및 GNW(Global Neural Workspace) 이론적 배경 기술.
-   **보완점**: 실제 코드 기반의 Block Diagram이 있으면 더 좋음 (학생 Toy Model 결과물 활용).

### **제2장: 검증 및 방법론**
-   **Status**: ✅ Drafted (`drafts/02_methodology.md`)
-   **내용**: Tubularity, Manifold Alignment, BERTRAM-2026 인용.
-   **보완점**: "왜 Tubularity가 Robustness를 보장하는가?"에 대한 실험적 근거 보강 필요.

### **제3장: 내수용 감각장 및 알로스태틱 뉴로-트윈**
-   **Status**: ✅ Drafted (`drafts/03_allostasis.md`)
-   **내용**: Predictive Allostasis, Neuro-Twin Loop.
-   **보완점**: 웨어러블 데이터 처리 파이프라인 구체화.

### **제4장: 행동 및 디코딩 (구현 계획)**
-   **Status**: ✅ Drafted (`drafts/04_validation.md`)
-   **내용**: Phase별 검증 로드맵 (Micro to Macro).
-   **보완점**: 이 계획대로 Phase 3(Toy Model)가 수행되어야 함.

---

## 🔗 관련 문서 링크
*   **[Overleaf 제안서 (Paper)](https://www.overleaf.com/1388485975djyxnxqtntmp#15280b)**
*   **[GitHub: Proposal Repo](https://github.com/snuconnectome/IITP-2026-Proposal)**
*   **[NotebookLM (RAG)](https://notebooklm.google.com/notebook/7acc2737-c783-43ff-af4c-e360ad02cf2c)**
