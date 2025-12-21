# 샘플-incite.pdf 요약 (레퍼런스)

- **원본**: `샘플-incite.pdf` (41p)
- **텍스트**: `parsed/샘플-incite.txt`

## TL;DR

HPC(대규모 계산자원) 할당/연구제안서 스타일로, “멀티모달 MRI + electrophysiology를 하나의 latent로 통합하는 foundation model(NeuroX‑Fusion)”을 제시합니다.  
강점은 **(1) Executive Summary가 매우 선명**, **(2) Grand Challenge → Breakthrough Approach → Scientific Payoff**의 논리 흐름, **(3) 단계적(pillars) 연구계획**, **(4) 오픈소스/플랫폼 배포 계획**이 한 덩어리로 묶여 있다는 점입니다.

## 구조/패턴(가져올 만한 것)

- **짧고 강한 Executive Summary**: “문제(통합 프레임 부재) → 해결(통합 foundation model) → 무엇이 가능해짐(가설검증/perturbation/rapid testing)”
- **Pillar 구조**: Pillar I/II/III로 단계적 구축(먼저 단일 모델 → 정렬/융합 → 응용)
- **배포/재현성**: 모델/데이터 파이프라인을 오픈 플랫폼에 통합해 확산한다는 문장 패턴

## 2026-인공지능-014(데이터 의미화) 관점 재사용 포인트

- 014는 “통합 모델”이 아니라 **데이터 의미화 프레임워크**가 핵심이므로:
  - “absence of framework” → “meaning-aware data framework”로 서사만 바꿔 쓰기 좋습니다.
  - Pillar 구조를 014의 단계로 치환:
    - Pillar I: attention/goal-driven acquisition
    - Pillar II: semantic linkage + abstraction/generalization
    - Pillar III: dynamic curation/forgetting + benchmark + OSS release
- **오픈소스/재현성 섹션 문장**은 IITP(공개SW/연구데이터 공개 요구)와 매우 궁합이 좋습니다.

## 주의(그대로 가져오면 안 좋은 것)

- HPC 자원(노드-아워 등) 중심 서사는 IITP 제안서에서 비중/톤을 조절해야 합니다.
- 영문 스타일이라, 국내 제안서에서는 “평가항목/KPI/연차별 산출물” 형태로 재배치가 필요합니다.


