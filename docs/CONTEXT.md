# Project Context: IITP-AI Grant Proposal

## 1. Goal

**IITP 2026-인공지능-014 (세부5) "인공지능을 위한 인간 인지 기반의 데이터 의미화 및 표현 기술 개발"** 과제 수주를 위한 제안서 작성.

- **핵심 컨셉**: `Robust and Efficient Multisensory Integrated Intelligence` (예측적 잠재표상 주도의 선택적 주의 지각 모사)
- **최종 목표**: 멀티모달 뇌 데이터와 LLM을 정렬하여, 불확실한 환경에서도 감각 결순을 스스로 복원하는 "통합 지능" 파운데이션 모델 구축.

## 2. Key Strategy (@06_iitp_cognitive_ai_strategy.md)

우리는 단순 LLM 확장이 아닌, **"뇌과학적 원리"를 통한 효율성**을 강조합니다.

1. **선택적 수집 (Cognitive Acquisition)**: 목표(Goal)와 주의(Attention)에 기반한 데이터 선별.
2. **Multiscale Primitives**: **LTC (Liquid Time-Constant)** 뉴런 모델과 **GNW (Global Neural Workspace)** 아키텍처 활용.
3. **동적 갱신 및 선택적 기억**: **Titans (Long-term Memory SSM)** 와 Bayesian surprisal을 통한 효율적 메모리 관리.
4. **검증**: 불확실성 환경에서의 강건성 및 인지적 타당성(Predictive Coding) 평가.

## 3. Critical Documents Map

AI는 작업 시 다음 문서들을 우선적으로 참조해야 합니다.

- **📜 RFP (Requirements)**: `docs/00_task_description/summary/2-1_인공지능_cognitive_ai_keypoints.md`
  - *Action*: 과제 제약조건(예산 23억/년, 기간 4년, 필수 목표) 확인 시 최우선 참조.
- **📝 Proposal Draft (Source of Truth)**: `docs/03_proposal/references/notes/LLM 정렬 기반 멀티모달 뇌 파운데이션 모델 구축 연구 제안서.md`
  - *Action*: 현재 연구 내용, 아키텍처, 마일스톤의 기준 문서.
- **📅 Planning**: `docs/01_project_planning/`
  - *Action*: WP 구성, 타임라인, 비전 확인.

## 4. Team Structure (SNU Connectome & Partners)

- **PI**: 차지욱 (서울대) - 총괄, 파운데이션 모델
- **Co-PIs**:
  - 홍석준 (성균관대) - 뇌 네트워크 모델링
  - 백세범 (KAIST) - 시각 피질/학습 원리
  - 강형률 (서울대병원/서울대) - 베이지안/공간 탐색
  - 유승범 (성균관대) - 영장류 전기생리
- **Persona**: "Reviewer #2" (논리적 허점과 재현 가능성을 엄격하게 검증).

## 5. Coding & Tools

- **Scripts**: `scripts/` 내의 Python 스크립트 활용 (자료 수집, 검색).
- **Constraints**:
  - `scripts/chrome_user_data/` 등 대용량 데이터 폴더는 읽지 않음.
  - Python 3.10+, PyTorch 2.x, BIDS 표준 준수.

---
*This file is maintained to provide context for AI assistants.*
