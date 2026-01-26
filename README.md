# SNU Connectome · IITP Brain × AI → Neuromorphic Research Repo

이 저장소는 **IITP 연구 그랜트 지원(과제 기획 · 문헌 연구 · 제안서 작성 · 연구관리)**을 위해 만든 “단일 작업공간”입니다.  
목표는 **"강건하고 효율적인 다중감각 통합 지능(Robust and Efficient Multisensory Integrated Intelligence)"** 연구를 기반으로, 장기적으로 Neuromorphic Computing까지 확장 가능한 연구 로드맵을 설계·제안·실행하는 것입니다.

> 현재 폴더가 비어 있어 “과제 설명서” 파일을 아직 읽지 못했습니다.  
> 설명서를 `docs/00_task_description/`에 넣어주면, 요구사항(평가항목/산출물/기간/예산/형식)을 반영해 README와 템플릿을 즉시 업데이트합니다.

---

## Quick Start

- **과제 설명서 넣기**: `docs/00_task_description/`에 공고/제안요청서(RFP)/양식/평가기준 파일을 추가
- **요약 작성**: `docs/00_task_description/README.md`의 체크리스트/요약표를 채우기
- **기획 시작**: `docs/01_project_planning/`에서 연구 목표·세부과제·WP·일정·리스크를 정리
- **문헌 파이프라인**: `docs/02_literature/`에 논문 메모/주제별 종합노트를 축적
- **제안서 작성**: `docs/03_proposal/`에서 아웃라인→섹션별 초안→그림/표를 완성

---

## Repository Structure

- **`docs/00_task_description/`**: 공고/과제 설명서/제출 양식/평가기준 + 내부 요약
- **`docs/01_project_planning/`**: 비전, 연구질문, WP(Work Packages), 일정, 리스크, KPI
- **`docs/02_literature/`**: 문헌 메모(논문 단위), 주제별 종합(synthesis), 참고문헌 관리
- **`docs/03_proposal/`**: 제안서 아웃라인/섹션별 초안/그림
- **`docs/04_experiments/`**: 초기 PoC/실험 설계/재현 로그(후속)
- **`docs/05_meetings/`**: 회의록/결정사항/액션아이템
- **`docs/06_admin/`**: 예산/인력/윤리·IRB/데이터 거버넌스/대외 문서
- **`templates/`**: 논문 메모, WP 설계, 제안서 섹션 템플릿

---

## How We Work (권장 흐름)

1. **설명서 기반 제약조건 확정**: 평가항목, 산출물, 제출 형식/분량/마감, 참여조건
2. **문제정의 → 가설 → 방법론**: Connectome/brain data/AI 모델/학습·추론/하드웨어 확장
3. **WP로 쪼개기**: 데이터·모델·검증·시스템·확산(성과)·관리
4. **Neuromorphic까지의 단계적 로드맵**: (알고리즘/표현: LTC, Titans) → (에너지/지연 최적화) → (spiking/이벤트기반) → (HW co-design)

---

## Next Needed from You

- **과제 설명서 파일 위치**: 이 폴더에 없다면, 실제 위치(경로) 또는 파일을 이 저장소로 복사해 주세요.
- **원격 git repo 위치**: “snuconnectome”가 GitHub org인지/내부 서버인지 확인이 필요합니다.
  - GitHub org라면: repo 이름(예: `iitp-brain-ai-neuromorphic`)을 알려주시면, 생성 커맨드까지 맞춰드릴게요.
