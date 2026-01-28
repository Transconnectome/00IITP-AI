# 🧠 IITP Brain × AI: Robust & Efficient Multisensory Intelligence
>
> **Project Code**: 00IITP-AI (NeuroX)  
> **Core Strategy**: Two-Part Model (Sensory Encoder + Titans Memory SSM)  
> **System**: NeuroX-OS v1.0

이 저장소는 **2026 IITP 인간 인지 기반 인공지능** 과제 제안서 작성을 위한 **"Agentic Proposal Operating System (NeuroX-OS)"**입니다. 단순한 파일 저장소를 넘어, AI 에이전트가 문헌 조사, 전략 검증, 초안 작성, 레드팀 리뷰를 수행하는 능동형 워크스페이스입니다.

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
| **`strategy-titans-alignment`** | 제안서 내용이 **"Titans 전략"** 및 **R&R(이메일 분석)**과 일치하는지 검증합니다. | `strategy_alignment_report.md` |
| **`evidence-synthesis-ssm`** | arXiv/Semantic Scholar에서 **SSM, Mamba, Titans** 관련 최신 논문을 수집하고 근거 매트릭스를 만듭니다. | `evidence_matrix_ssm.md` |
| **`proposal-outline-iitp`** | IITP 평가 지표(기술성, 연구능력 등)에 맞춘 **MECE 아웃라인**을 생성합니다. | `outline_iitp_v1.md` |
| **`draft-writer-neurox`** | "세계 최고/최초" 톤앤매너로 **정부 제안서 스타일**의 초안을 작성합니다. | `docs/03_proposal/drafts/` |
| **`figure-architecture-blueprint`** | Two-Part Model의 구조를 **Mermaid/Draw.io 다이어그램**으로 설계합니다. | `docs/05_figures/` |
| **`redteam-reviewer-impact`** | 심사위원 페르소나를 장착하여 **"혁신성 부족", "실현 가능성"** 등을 혹독하게 비판합니다. | `redteam_report.md` |

### 2. ⚡ Automated Workflows (`.agent/workflows/`)

복잡한 작업을 한 번의 명령으로 수행할 수 있습니다. 채팅창에 아래 명령어를 입력하세요.

* **`@/align`**: **전략 정렬**. 최신 이메일/회의록을 분석하여 제안서 방향 수정 제안.
* **`@/lit-ssm`**: **문헌 조사**. 최신 SSM/Titans 논문 10편 수집 → 요약 → 근거 추가.
* **`@/draft-part1`**: **1세부 초안 작성**. "Sensory Encoder" 파트 자동 작성.
* **`@/draft-part2`**: **2세부 초안 작성**. "Titans Memory" 파트 자동 작성.
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
