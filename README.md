# 🧠 IITP Brain × AI: Robust & Efficient Multisensory Intelligence
>
> **Project Code**: 00IITP-AI (NeuroX)  
> **Core Strategy**: Two-Part Model (Sensory Encoder + Titans Memory SSM) 
> **Links**:
> - **[📝 Current Working Document (Overleaf)](https://www.overleaf.com/1388485975djyxnxqtntmp#15280b)** 👈 **Main Paper**
> - **[GitHub (Research Hub)](https://github.com/Transconnectome/00IITP-AI)**
> - **[GitHub (Proposal Sync)](https://github.com/snuconnectome/IITP-2026-Proposal)**
> **Knowledge Base**: [NotebookLM Link](https://notebooklm.google.com/notebook/7acc2737-c783-43ff-af4c-e360ad02cf2c)

이 저장소는 **2026 IITP 인간 인지 기반 인공지능** 과제 제안서 작성을 위한 **"Agentic Proposal Operating System (NeuroX-OS)"**입니다. 단순한 파일 저장소를 넘어, AI 에이전트가 문헌 조사, 전략 검증, 초안 작성, 레드팀 리뷰를 수행하는 능동형 워크스페이스입니다.

---

## 📜 Master Plan (Start Here!!)

**"모든 전략과 계획은 이 문서에서 시작됩니다."**

**[📄 PROPOSAL_PLAN.md (제안서 마스터 플랜)](docs/03_proposal/PROPOSAL_PLAN.md)**

이 파일은 본 과제(2026-014)의 **가장 중요한 설계도**이자 **나침반**입니다. 제안서 작업에 착수하기 전 반드시 필독해야 합니다.

*   **핵심 철학**: **DIVER-Neuro** 파운데이션 모델의 정의 ("Ground Truth는 뇌에 있다").
*   **아키텍처 정의**:
    *   **Part 1 (Dual Encoders & Titans)**: 시각/언어/신체(Proprioception)와 뇌 신호(LTC)를 통합하는 메커니즘.
    *   **Part 3 (Allostatic Neuro-Twin)**: 단순 웰니스 에이전트를 넘어선 예측적 항상성(Homeostasis) 조절 원리.
*   **검증 논리**: "Tubularity", "Manifold Alignment" 등 학술적 근거(Bertram et al., 2026)와 Titans Memory(Surprise-based)의 타당성.
*   **실행 로드맵**: Phase 1(이론) $\rightarrow$ Phase 2(마이크로 구현) $\rightarrow$ Phase 3(통합) $\rightarrow$ Phase 4(초안 작성).

---

## 🧠 Knowledge Base (NotebookLM)

**[NotebookLM 바로가기](https://notebooklm.google.com/notebook/7acc2737-c783-43ff-af4c-e360ad02cf2c)**

이 Notebook는 NeuroX 프로젝트의 **"지식 베이스(Knowledge Base)"**이자 **"Agentic Red Teamer"** 역할을 수행합니다.

*   **Source Grounding**: RFP 원문 및 최신 논문에 기반한 엄밀한 팩트 체크.
*   **Audio Briefing**: 이동 중 제안서의 논리적 흐름을 청각적으로 점검.
*   **Deep Q&A**: "SSM vs Transformer" 등 심층적인 기술적 차별점 논리 생성.

---

## 🏗️ Core Architecture: "The Two-Part Model"

이 과제의 핵심 기술 전략은 **"인간 기억 기전(Hippocampus/Prefrontal Cortex)을 모사한 차세대 AI"**입니다.

1. **Part 1: Sensory Encoder (감각 처리)**
    * **기능**: 시각, 청각, 촉각 등 다중 감각을 효율적으로 압축 및 표현.
    * **기술**: Predictive Coding, Clockwork VAE, JEPA (Joint Embedding Predictive Architecture).
2. **Part 2: Titans Memory Core (통합 및 기억)**
    * **기능**: 예측 불가능한 정보(Surprisal) 위주로 장기 기억을 형성하고, 불필요한 정보는 망각.
    * **기술**: **State Space Model (SSM)**, Neural Memory, Linear Attention.

---

## 🛠️ NeuroX-OS Capabilities (Skills & Workflows)

이 시스템에는 제안서 작성을 돕는 6가지 특수 능력(Skill)과 5가지 자동화 흐름(Workflow)이 탑재되어 있습니다.

### 1. 🤖 Available Skills (`.agent/skills/`)
AI 에이전트는 상황에 따라 아래 스킬을 자동으로 로드하여 작업을 수행합니다.

| Skill Name | 설명 (Goal) | 산출물 (Output) |
| :--- | :--- | :--- |
| **`embodied-neuro-proposal-writer`** | **[New]** IITP 제안서(LTC, Proprioception) 전용 고품질 초안 작성. | `docs/03_proposal/drafts/` |
| **`embodied-neuro-reviewer`** | **[New]** RFP-013(신체성) 및 IdeaDeck 정합성을 엄격히 심사. | `docs/99_reviews/` |
| **`evidence-synthesis-ssm`** | 문헌 조사 및 근거 매트릭스 생성. | `evidence_matrix_ssm.md` |
| **`figure-architecture-blueprint`** | 아키텍처 다이어그램 설계. | `docs/05_figures/` |

### 2. ⚡ Automated Workflows (`.agent/workflows/`)
채팅창에 아래 명령어를 입력하세요.

* **`@/draft-proposal`**: **전체 초안 작성 루프**. (Write -> Review -> Refine).
* **`@/fig-arch`**: **그림 설계**. 아키텍처 다이어그램 업데이트.

---

## 📂 Repository Structure

* **`/.agent/`**: NeuroX-OS의 두뇌 (Skills, Rules, Workflows).
* **`/_ops/`**: 운영 로그, 진단 리포트 (`diagnostics/`), 체크리스트.
* **`docs/`**: 프로젝트 실제 산출물.
  * `00_task_description/`: RFP 원문, 양식.
  * `01_project_planning/`: 전략 문서 (`email_analysis_and_insights.md`), 아웃라인.
  * `02_literature/`: 논문 PDF, 요약, 근거 매트릭스.
  * `03_proposal/`: 제안서 본문 초안 (`drafts/`).
  * `04_review/`: 레드팀 리뷰 리포트 (`redteam_report.md`).
  * **`05_figures/`**: [New] 아키텍처 그림, 도표 소스.
  * `07_submission/`: [New] 최종 제출용 패키지.

---

## 🚀 Usage Scenarios (How-to)

### Situation 1: "새로운 아이디어가 문헌적으로 타당한지 확인하고 싶어."
>
> **User**: "SSM이 Transformer보다 Long-term memory에서 유리하다는 근거 좀 찾아줘."  
> **System Action**: `evidence-synthesis-ssm` 스킬 발동 → arXiv 검색 → `evidence_matrix_ssm.md` 업데이트.

### Situation 2: "제안서 1세부(Encoder) 초안을 빨리 써야 해."
>
> **User**: "1세부 초안 작성해줘." (또는 `@/draft-part1`)  
> **System Action**: `draft-writer-neurox` 스킬 발동 → 아웃라인 로드 → "Predictive Coding" 중심으로 본문 작성 → `drafts/part1_sensory_encoder.md` 저장.

### Situation 3: "내가 쓴 내용이 너무 약한 것 같아. 비판해줘."
>
> **User**: "지금까지 쓴 초안 레드팀 리뷰해줘."  
> **System Action**: `redteam-reviewer-impact` 스킬 발동 → 심사위원 모드 진입 → **"구체적인 경쟁 기술 대비 우위가 부족함"** 등 지적.

### Situation 4: "아키텍처 그림을 그려야 해."
>
> **User**: "Two-Part Model 개념도 그려줘." (또는 `@/fig-arch`)  
> **System Action**: `figure-architecture-blueprint` 스킬 발동 → Mermaid 코드 생성 → SVG 저장.

---

## 🔗 References & Credits

* **Repo**: [https://github.com/Transconnectome/00IITP-AI](https://github.com/Transconnectome/00IITP-AI)
* **Lead PI**: Hong Seok Jun (Architecture Strategy)
* **Co-PI (User)**: Cha Jiook (Scaling & Multimodal SSM)
* **Partners**: ETRI, SNU, SKKU, KBRI.
