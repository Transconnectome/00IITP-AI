# AI 연구 활용 소명서 — 인수인계

2026-11-04 | 최신 검토 후보: **쉬운 설명 v3, A4 1쪽**

**작성·검증 완료 / 연구책임자 승인 대기 / Teams 미발송 / 회계 시스템 미제출.**
이번 handoff-push 요청은 Git 보관 승인이다. 보고서 내용 승인이나 수신자 전달 승인과 구분한다.

## 목적과 편집 기준

회계 점검 요청은 “동 과제와의 직접적인 관련성을 확인할 수 있도록 활용 목적과 활용 방법 등을 구체적으로 소명”하는 것이다. 연구 목적과 실제 활용 방법을 먼저 설명하고 복수 구독·사용량·경제성은 보조한다.

- 비전문 회계 담당자용 한 장을 유지한다. 연구·모델 고유명사와 상세 방법론을 본문에 다시 넣지 않는다.
- 뇌 정보 처리 연구, 불완전한 측정자료 보완, 개발 방법의 성능·신뢰성 검증 수준에서 설명한다.
- 토큰은 처리 규모이며 연구 성과, 청구서, 해당 과제 전용 사용량 또는 구독 한 개의 실적이 아니다.
- 구독별 실제 절감액이나 제공 한도를 추정하지 않는다. 비용은 관측 구성에 따른 조건부 종량제 비교다.

## 산출물

| 파일 | 용도·상태 |
|---|---|
| [연구용_AI서비스_활용소명서_쉬운설명_1쪽.pdf](연구용_AI서비스_활용소명서_쉬운설명_1쪽.pdf) | 우선 검토본. 이전 8쪽·연구중심 v2를 대체하는 후보 |
| [summary_plain_v3.md](summary_plain_v3.md), [summary_plain_v3.html](summary_plain_v3.html) | 편집 원본·출력용 HTML |
| [render_plain_summary.py](render_plain_summary.py) | PDF·로컬 미리보기 생성, 한 쪽/텍스트 경계 검사 |
| [PLAIN_V3_SHA256SUMS](PLAIN_V3_SHA256SUMS) | PDF·Markdown·HTML 보존 해시 |
| [cost_calculation.json](cost_calculation.json), [subscription_scenarios.csv](subscription_scenarios.csv) | 비용 계산·조건부 비교 |
| [public_rate_sources.json](public_rate_sources.json) | 2026-11-04 확인한 공식 가격 출처·가정 |
| [analysis/README.md](analysis/README.md) | 집계 방법·기간·누락 및 중복 처리 한계 |
| `analysis/*_deduplicated.json` | 대화 내용·개별 요청 ID를 제외한 집계 스냅샷 |
| `analysis/aggregate_usage.py`, `analysis/check_usage.py` | 로컬 재집계·저장 집계 산술 검증 |

## 수치와 증거의 경계

- 10월 한 로컬 사용환경의 Claude 처리량: **42,737,586,105 토큰**, 31일. 반복 자료 읽기 포함. 연구실 전체나 특정 구독·과제 전용이 아니다.
- 점검 기간은 4–9월이지만 보존 로그는 7월 28일–9월 30일 중 37일만 확인된다. 약 189억 토큰을 6개월 전수로 해석하지 않는다. Codex 10월 기록도 25–30일 중 5일만 확인되어 월 전체로 환산하지 않는다.
- 관측 주력 모델의 입력·캐시·출력 구성과 공개 단가로 10억 토큰당 **$488.714620**. 같은 양을 월 $200 구독 안에서 추가 요금 없이 처리한다는 조건에서 차액 **$288.714620(약 59%)**. 실제 구독별 절감액은 미확정이다.
- 캐시 유지시간 불명확 기록은 낮은 5분 단가 적용. 모든 캐시 쓰기를 5분 단가로 바꾸면 10억 토큰당 약 $407.68.
- 기존 대시보드는 Claude 분할 기록 중복 및 Codex 부분집합 이중 합산이 확인되어 원래 총량을 사용하지 않았다. 운영 집계기는 수정하지 않았다.
- 결제 9건은 계정 9개 또는 한 달 구독료를 뜻하지 않는다. 개별 이용자·기간·담당 연구 대조가 남아 있다.

연구 설명은 제출 연구계획서의 연구 내용·역할 배분, 10월 29일 과제 보고자료, 실제 프로그램·문서 변경 및 연구책임자 요청에 근거한다. 일부 사례는 점검 기간 이후이므로 해당 기간 지출 증명과 혼동하지 않는다. 세부 연결표와 원문은 아래 로컬 자료에 남아 있다.

## 검증·재시작

패키지 폴더에서 실행한다.

```bash
python3 analysis/check_usage.py
sha256sum -c PLAIN_V3_SHA256SUMS
```

저장 집계의 중복 처리·부분집합·시간대 경계·모델별/일별 합계 검산 통과. PDF A4 1쪽, 텍스트 경계 및 화면 미리보기 확인 완료. 비용 귀속이나 실제 구독 절감액을 확정하는 검증은 아니다.

편집 후 `python3 render_plain_summary.py`로 재생성한다. `markdown`, `weasyprint`, `PyMuPDF`, Noto Sans CJK KR 폰트가 필요하다. 재생성 후 화면·한 쪽 여부를 확인하고 해시도 갱신한다. 원로그 재집계는 원래 호스트에서만 가능하며 기존 스냅샷을 보존하도록 별도 출력 파일을 사용한다.

## 로컬 전용 자료·다음 행동

원래 폴더: `/home/juke/git/00IITP-AI/docs/06_admin/2026-11-04_ai_usage_audit`.

Git 제외: `private_sources/`(점검 원문), `source_register.json`(메일 식별자·결제), `research_usage_evidence.md`·`original_request_reference.md`(세부 근거·요청 이력), `delivery_status.json`·`teams_message_draft.txt`(수신자·대화방·이전 초안), 이전 보고서·대시보드 스냅샷·화면 미리보기.

1. 최신 v3 PDF를 연구책임자에게 확인받고 피드백을 반영한다.
2. 승인 후 로컬 `delivery_status.json`의 확인된 수신 대화방으로 전달한다. 이전 메시지 초안은 v3에 맞춰 갱신한다.
3. Teams 커넥터는 메시지를 지원하지만 파일 첨부 인자가 없다. 수신자 접근이 확인된 파일 링크 또는 승인된 업로드 경로를 사용하고 메시지·접근 결과를 확인한다.
4. 전달 결과를 기록한다. Teams 전달과 회계 시스템 제출은 별도 상태다.

## Git 범위

비공개 원격 `snuprivate`의 `feature/topic1-lag-motif-v2` 기준 커밋 `3bdbc9cff34e63d2f1457d8c4080c67cd0448683`에서 `codex/ai-usage-audit-handoff`를 분리했다. 원래 작업 공간의 무관한 연구 커밋·미추적 자료와 루트 인수인계 문서는 포함하지 않았다. 공개 원격 `origin`으로 이 자료를 보내지 않는다.

작업 공간: `/home/juke/git/00IITP-AI-audit-handoff`. 이 README가 본 작업의 인수인계 정본이다. 최종 커밋 SHA·원격 반영 결과는 완료 응답에서 확인한다.
