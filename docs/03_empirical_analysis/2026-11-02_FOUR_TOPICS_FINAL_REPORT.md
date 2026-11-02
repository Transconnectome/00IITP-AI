# 2028 IITP 다중감각 통합 지능 과제: 손운규 교수님 4대 연구 주제 실증 분석 최종 통합 보고서

- **작성 일자**: 2026-11-02 (KST)
- **실행 워크플로**: `tw-20261031-four-topics` (Workflow A/B/C 통합 완결본; 정본 상태 기록: `.agents/teamwork/tw-20261031-four-topics/orchestrator/GATE_STATUS.md`, PI 의사결정 기록: `.agents/teamwork/tw-20261031-four-topics/orchestrator/PI_DECISIONS_2026-11-01.md`)
- **연구 기원**: 손운규 교수님 이메일에서 제안된 4대 뇌-영감 인공지능·신경과학 실증 가설 (1: 미시적 방향성 지연 모티프, 2: 중시적 커넥톰 박스-커버링 재규격화군 풀링, 3: 거시적 층별 재규격화군 스펙트럼 흐름 및 참여비 진단, 4: 역전파 없는 국소 시냅스 학습 규칙)
- **증거 및 데이터 거버넌스 준칙 (C1–C8)**: 본 보고서의 모든 실증 수치는 사전 동결(pre-frozen) 분석 카드 이후 생성된 본 실행의 날짜별 정본 결과 파일(`results/topic1/2026-10-31/`, `results/topic2/2026-11-01/`, `results/topic2/2026-11-02_fu_{a,b,c,d,e}/`, `results/topic3/2026-10-31/`, `results/topic3/2026-11-02_h2/`, `results/topic4/2026-11-01/`, `results/gpu_ledger_2026-10-31.md`)에서만 인용하였다. 과거 예비 문서(`EMPIRICAL_ANALYSIS_REPORT.md`, `2026-11-01_FOUR_TOPICS_CONSOLIDATED_STATUS.md`)의 수치는 결과 근거로 인용하지 않는다(C8). 참가자 식별자·BIDS 접두어·비염처리 해시는 일절 포함하지 않는다(C4).

---

## 1. 1페이지 총괄 요약표 (Executive Summary Table)

| 주제 / 마일스톤 | 핵심 연구 질문 (손운규 교수님 제안) | 사전 동결 카드 및 임계치 ($\delta$) | 데이터셋 및 표본 구성 | 연산 자원 (GPU-h / 상한) | 사전 등록 규칙에 따른 최종 판정 | 핵심 주효과 수치 및 95% 구간 | 5인 검증 게이트 및 독립 승리 감사 | 정본 결과 파일 경로 |
|---|---|---|---|---|---|---|---|---|
| **Topic 1 (`M1`)**<br>미시적 방향성 지연 모티프 | ENIGMA-OCD $N=304$ ROI 광대역 fMRI의 2.0 s 지연 반대칭 교차상관($F=C-C^\top$, 상위 10% 방향성 간선)에서 3-노드 순환 모티프 $Z_{\text{030C}}$(`E1`) 및 $Z_{\text{030C}}-Z_{\text{030T}}$(`E2`)가 강박증(OCD)과 건강대조군(HC) 간에 차이를 보이는가? | `docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md`<br>(`1e589f0b…75aa`)<br>$p_{\text{Holm}}<0.05$ **및** $\|d\|\ge 0.15$ | ENIGMA-OCD 23개 기관 $N=1,706$ (OCD $869$, HC $837$), 304 ROIs, 2.0 s 격자 | `0.000` / `0.0` GPU-h<br>(DGX-Spark CPU `1.19 h`) | **`Topic 1 KILLED`**<br>(두 일차 종점 모두 기각 기준 미달) | **`E1` ($Z_{\text{030C}}$)**: $d = 0.113$ (Wald 95% CI $[0.015, 0.212]$), $p_{\text{FL}} = 0.0223$, $p_{\text{Holm}} = 0.0446$ ($\|d\| < 0.15$ 미달)<br>**`E2` ($Z_{\text{030C}}-Z_{\text{030T}}$)**: $d = 0.038$ ($[-0.061, 0.136]$), $p_{\text{FL}} = 0.4416$, $p_{\text{Holm}} = 0.4416$ | r1 5인 게이트 PASS<br>`victory_M1_b`: **`VERIFIED_COMPLETE`**<br>(88 tests, 변이 23/23 + 24/24 사살) | `results/topic1/2026-10-31/stats_results.json`<br>`results/topic1/2026-10-31/fallback_decision.json`<br>`results/topic1/2026-10-31/report_derived_numbers.json` |
| **Topic 2 본실험 (`M3`)**<br>커넥톰 박스 풀링 (1× 예산, 5 시드, E36) | SwiFT ver11 `E36_d2262`(38.7M) Stage-0 병합(`M0`, $16^3\to 8^3$)에서 $2\times 2\times 2$ 유클리드 큐브(`E`) 대신 학습군 FC 기반 커넥톰 박스(`C`)로 12 mm 셀을 묶으면 홀드아웃 2 mm 복셀 SimMIM 재구성 NMSE가 $\ge 1\%$ 감소하는가? | `docs/03_empirical_analysis/topic2/2026-11-01_topic2_card.md`<br>(`c9bfc60a…c41f5`)<br>$\delta = 1.00\%$ (`0.01`), 5 시드 (`df=4`) | HCP-YA S1200 OA `REST1_LR` $N=88$ (`64` train / `8` val / `16` test; 위치 인덱스 `h00..h87`), 140k 샘플 (`8,750` 스텝) | `11.990` / `14.0` GPU-h<br>(B300: 작업자 `11.730`, 탐색 `0.142`, 검증 `0.118`) | **`stop` (killed)**<br>($\text{hi}(I_1) = +0.361\% < \delta = 1.00\%$; 실용적 이득 배제) | **$F^+$ 게이트**: $C$ vs $E$ $+3.06\%$, $C$ vs $S$ $+2.93\%$ (`pass`)<br>**$F^-$ 게이트**: $C$ vs $E$ $-1.74\%$ (`pass`)<br>**Stage-1 $I_1$ ($C$ vs $E$)**: 평균 $+0.147\%$, 95% $t$-CI $[-0.068\%, +0.361\%]$, $p = 0.1302$<br>**Stage-1 $I_2$ ($C$ vs $S$)**: 평균 $+0.473\%$, 95% $t$-CI $[+0.001\%, +0.946\%]$, $p = 0.0497$ | r3 5인 게이트 PASS<br>`victory_M3_r3`: **`VERIFIED_COMPLETE`**<br>(116 tests, 변이 102/102 + r3 22/23 + 승리 38/40 사살) | `results/topic2/2026-11-01/verdict.json`<br>`results/topic2/2026-11-01/stage0_hcp.json`<br>`results/topic2/2026-11-01/posthoc_sensitivity_without_seed2.json` |
| **Topic 2 후속 A (`FU_A`)**<br>저잡음 12 mm 셀-평균 타깃 | 2 mm 복셀 잡음 바닥(NMSE $\approx 0.99$) 대신 저잡음 12 mm 셀-평균장($y_{v,t} = \kappa m_{c(v),t}$, $NF = 0.2085$)을 재구성할 때 `C`가 `E`보다 $\ge 1\%$ 우월한가? | `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_a_card.md`<br>(`72be3e83…618fb`)<br>$\delta = 1.00\%$ (`0.01`), 시드 0 $F^+$ 선행 게이트 | 합성 $F^+$ ($\sigma_v = 6.5459$ 보정); HCP Stage-1 미실행 | `0.952` / `8.0` GPU-h<br>(B300 Slurm `507`: 작업자 `0.822`, 탐색 `0.130`) | **`inconclusive` (measurement capacity)**<br>(보정 잡음에서 $F^+$ 게이트 미달로 Stage-1 미실행) | **$F^+$ 게이트 (시드 0)**: `E` NMSE $0.77468$, `C` NMSE $0.77041$, 상대 이득 $g(C\text{ vs }E) = +0.5511\% < \delta = 1.00\%$ (`fail`)<br>**Stage-1 HCP**: 카드 §7.3/§8.3에 따라 미실행 | r1 5인 게이트 PASS<br>`victory_FU_A_r1`: **`VERIFIED_COMPLETE`**<br>(69p/1s tests, 변이 31/31 + 승리 25/26 사살) | `results/topic2/2026-11-02_fu_a/verdict.json`<br>`results/topic2/2026-11-02_fu_a/partitions/fixture_build.json` |
| **Topic 2 후속 B (`FU_B`)**<br>4× 학습 예산 (560k 샘플) | 학습 예산을 4배(`35,000` 스텝 = 560,000 샘플)로 확장할 때 `E36`에서 `C`가 `E` 대비 2 mm 복셀 NMSE를 $\ge 1\%$ 낮추는가? | `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md`<br>(v2 `994f0144…4daae`)<br>$\delta = 1.00\%$ (`0.01`), 5 시드 (`df=4`) | HCP-YA OA $N=88$ (`64`/`8`/`16`), 560k 샘플 (`35,000` 스텝 × 배치 16) | `30.720` / `33.0` GPU-h<br>(B300 Slurm `490, 509, 516`: 작업자 `30.580`, 탐색 `0.140`) | **`stop` (killed)**<br>($\text{hi}(I_1) = +0.425\% < \delta = 1.00\%$; 4× 예산에서도 실용적 이득 배제) | **4× $F^+$ 게이트**: $C$ vs $E$ $+3.73\%$, $C$ vs $S$ $+3.70\%$ (`pass`)<br>**Stage-1 $I_1$ ($C$ vs $E$)**: 평균 $+0.063\%$, 95% $t$-CI $[-0.299\%, +0.425\%]$, $p = 0.6534$<br>**Stage-1 $I_2$ ($C$ vs $S$)**: 평균 $-0.092\%$, 95% $t$-CI $[-0.646\%, +0.461\%]$<br>**비정체 시드 1–4 ($n=4$)**: $I_1 = -0.067\%$ ($[-0.091\%, -0.043\%]$, $p=0.0029$) | r1 5인 게이트 PASS<br>`victory_FU_B_r1`: **`VERIFIED_COMPLETE`**<br>(128 tests, 변이 44/44 사살) | `results/topic2/2026-11-02_fu_b/verdict.json`<br>`results/topic2/2026-11-02_fu_b/gate_4x.json` |
| **Topic 2 후속 C (`FU_C`)**<br>8개 신규 독립 시드 (`s10..17`) | 동일 1× 설정(`E36`, 140k 샘플)에서 8개의 신규 독립 시드(`10..17`, `df=7`)로 신뢰구간 폭을 좁힐 때 `C`가 `E` 대비 $\ge 1\%$ 우월한가? | `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_c_card.md`<br>(`fc2d0672…44ecb`)<br>$\delta = 1.00\%$ (`0.01`), 8 시드 (`df=7`) | HCP-YA OA $N=88$ (`64`/`8`/`16`), 시드 `10..17` (24개 Stage-1 실행) | `10.697` / `13.0` GPU-h<br>(B300 Slurm `501`, `512..562`: 작업자 `10.422`, 탐색 `0.262`, 검증 `0.013`) | **`stop` (killed)**<br>($\text{hi}(I_1) = +0.272\% < \delta = 1.00\%$; r1 `stop`이 8개 독립 시드에서 재현됨) | **Stage-1 $I_1$ ($C$ vs $E$, `df=7`)**: 평균 $-0.113\%$, 95% $t$-CI $[-0.499\%, +0.272\%]$<br>**Stage-1 $I_2$ ($C$ vs $S$, `df=7`)**: 평균 $+0.008\%$, 95% $t$-CI $[-0.520\%, +0.537\%]$<br>**비정체 6시드 (`df=5`)**: $I_1 = +0.040\%$ ($[-0.213\%, +0.293\%]$)<br>**통합 13시드 (`df=12`)**: $I_1 = -0.013\%$ ($[-0.248\%, +0.222\%]$) | r3 5인 게이트 PASS<br>`victory_FU_C_r3`: **`VERIFIED_COMPLETE`**<br>(210 tests, 변이 217/221 + 승리 12/12 사살) | `results/topic2/2026-11-02_fu_c/verdict.json`<br>`results/topic2/2026-11-02_fu_c/anchor/anchor.json` |
| **Topic 2 후속 D (`FU_D`)**<br>`E192_d22182` 대규모 모델 (474.2M) | 모델 용량을 12.2배 키운 SwiFT `E192_d22182`(474,226,176 파라미터, 최종 토큰 1536차원)에서 `C`가 `E` 대비 $\ge 1\%$ 우월한가? | `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_card.md`<br>(`1b7fee6c…6001b`)<br>$\delta = 1.00\%$ (`0.01`), 시드 0 $F^+$ 선행 게이트 | 합성 $F^+$ (`E192`, 140k 샘플); HCP Stage-1 미실행 | `3.720` / `25.0` GPU-h<br>(B300 Slurm `511, 534..536`: 작업자 `3.575`, 탐색 `0.097`, 검증 `0.048`) | **`inconclusive` (measurement capacity)**<br>(`E192`에서 $F^+$ 게이트 미달로 Stage-1 미실행; r1 `E36` `stop` 단독 유지) | **$F^+$ 게이트 (`E192`, 시드 0)**: `E` $0.65585$, `C` $0.65347$, `S` $0.65777$<br>$g(C\text{ vs }E) = +0.3631\% < 1.00\%$, $g(C\text{ vs }S) = +0.6546\% < 1.00\%$ (`pass: false`) | r3 5인 게이트 PASS<br>`victory_FU_D_r3`: **`VERIFIED_COMPLETE`**<br>(389 tests, 통합 변이 1,511/1,675 사살, 결과 변경 생존 0) | `results/topic2/2026-11-02_fu_d/verdict.json`<br>`results/topic2/2026-11-02_fu_d/smoke/equiv.json` |
| **Topic 2 후속 E (`FU_E`)**<br>동결 인코더 하류 개인식별력 ($I_{\text{diff}}$) | 저장된 r1 Stage-1 15개 동결 인코더(`E, C, S` × 5 시드)의 채널 공분산(`cov2`) 표현에서 홀드아웃 $N=24$명의 반분할 개인식별력 $I_{\text{diff}}$가 `C`에서 $\ge 1\%$ 높은가? | `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_e_card.md`<br>(`072553b0…6b88f`)<br>$\delta = 1.00\%$ (`0.01`), 전 슬롯 $F^+$ 게이트 | HCP-YA OA 홀드아웃 $N=24$ (`16` test + `8` val), 공통 마스크 `190,382` 복셀, 전/후반 각 580 TR | `0.330` / `1.5` GPU-h<br>(B300 Slurm `499, 524, 558, 570`: 작업자 `0.282`, 탐색 `0.015`, 검증/승리 `0.033`) | **`inconclusive` (measurement capacity)**<br>(정체 체크포인트 `S_s2`의 합성 $F^+$ 미달; 반사실적 본분석 $J_1$도 0과 $\delta$를 동시에 포함하여 `inconclusive`) | **$F^+$ 게이트**: `S_s2` $I_{\text{diff}} = 5.76 \le p_{95} = 10.59$ (`fail`; 나머지 14/15 통과)<br>**본분석 $I_{\text{diff}}$ 시드 평균**: `E` $61.07$, `C` $65.42$, `S` $56.92$ (`cellfc` $64.13$)<br>**$J_1$ ($C$ vs $E$)**: $+8.11\%$, 95% $t$-CI $[-6.60\%, +22.81\%]$<br>**$J_2$ ($C$ vs $S$)**: $+15.00\%$, 95% $t$-CI $[+9.80\%, +20.21\%]$ | r1 5인 게이트 PASS<br>`victory_FU_E_r1`: **`VERIFIED_COMPLETE`**<br>(71 tests, 변이 20/24 사살, GPU 재실행 확인) | `results/topic2/2026-11-02_fu_e/verdict.json`<br>`results/topic2/2026-11-02_fu_e/run_524/extract.json` |
| **Topic 3 본분석 (`M2`)**<br>층별 PR 및 멱법칙 스펙트럼 진단 | SwiFT `E192` 및 뇌 파운데이션 모델(BrainLM, BrainJEPA, NeuroSTORM)의 층별 유효 차원(PR) 및 멱법칙 지수 $\alpha$에 관한 기존 주장(`J1, R1–R7`)이 중심화(centered) 추정량·표본수 보정·토큰 수준 검증에서 유지되는가? | `docs/03_empirical_analysis/topic3/2026-10-31_topic3_analysis_card.md`<br>(`68337456…1b8e0`)<br>쌍대 부표본($m=28, 12$), 부호반전 순열($B=9999$), Holm 보정 | VRABES Remission $N=57$ (NeuroSTORM $n=25$), SwiFT `E192` 4개 체크포인트 × $57\times 7$ 프레임 | `0.000` / `0.0` GPU-h<br>(DGX-Spark CPU + `connectome` CPU Slurm `217845`) | **`J1` FAILS (`stop`)**<br>**`R1` 기술통계 전용 (`inconclusive`)**<br>**`R2` 기전 FAILS (`stop`) / 피험자 수준 `D1` HOLDS (`keep`) / 토큰 수준 `H1a` 역방향(`L3>LN0(L2)`) HOLDS, `H1b` 미재현**<br>**`R3` 순서(`D3`) HOLDS (`keep`), 원인 귀속 불가**<br>**`R4, R6` NOT SUPPORTED (`stop`)**<br>**`R5` UNTESTABLE / `R7` 비교 불가** | **피험자 수준 `D1` ($\Delta\text{PR}_{28}(L2-L3)$)**: cov $+5.34$ ($[+3.22, +7.46]$), corr $+6.04$ ($[+4.28, +7.80]$); `A1b` ($L3-\text{LN}_0(L2)$ corr): $-6.08$ ($[-7.98, -4.18]$)<br>**토큰 수준 `H1a`**: 주 체크포인트 $+0.0228$ ($\times 1.023$, $[+0.0207, +0.0248]$, $p_{\text{Holm}}=0.0002$), zoo 2/3 동부호(유효 상한 $\le 7$)<br>**교차모델 `D3` ($m=12$ cov)**: `JEPA-LM` $+2.08$ ($[+0.77, +3.40]$), `STORM-LM` $+3.36$ ($[+1.72, +5.01]$) | r4 고정범위 게이트 PASS<br>`victory_M2`: **`VERIFIED_COMPLETE`**<br>(138 tests, Family A 300/300 재현, 변이 150/151 + r4 사살) | `results/topic3/2026-10-31/t3_1_provenance_repro.json`<br>`results/topic3/2026-10-31/family_A_subject_level.json`<br>`results/topic3/2026-10-31/family_B_token_level.json` |
| **Topic 3 대조군 (`M2H2`)**<br>무작위 초기화(`H2`) 대조 실험 | 동일 57명 × 7 프레임에서 학습된 SwiFT `E192`의 층간 대비(`H1a`, `H1b`, `D1`)와 층별 PR이 무작위 초기화 네트워크(10 시드)와 유의하게 다른가? | `docs/03_empirical_analysis/topic3/2026-11-02_topic3_addendum_07_h2_card.md`<br>(`09b45220…dd84b`)<br>Gate G + $\delta_C = 0.5\|\text{trained}\|$, $\delta_L = \log(1.10)$ | `connectome` VRABES `ses-01` $57\times 7 = 399$ 윈도우, `R0`(학습) + `R1..R10`(무작위 초기화 10 시드) | `0.891` / `6.0` GPU-h<br>(`connectome` A5000 Slurm `218063, 218064` 외: 작업자 `0.458`, 탐색 `0.058`, 검증/승리 `0.375`) | **Gate G: `PASS`**<br>**`C1` (`H1a` DiD): `INC` (`inconclusive`)**<br>**`C2` (`H1b` DiD): `INC` (`inconclusive`)**<br>**`C3` (`D1` cov DiD): `TE+` (`keep`)**<br>**`C4` (`D1` corr DiD): `TE+` (`keep`)**<br>**Family L**: 피험자 수준 `L1..L3` 모두 `TE-`(학습에 의한 강한 차원 압축), `L0`는 `INC` | **`C1` (`H1a` DiD)**: $+0.0124$ ($[+0.0104, +0.0145]$, $\delta=0.0114$ 걸침)<br>**`C2` (`H1b` DiD)**: $+0.0295$ ($[+0.0256, +0.0334]$, $\delta=0.0223$, 2개 시드 $\le\delta$)<br>**`C3` (`D1` cov DiD)**: $+5.09$ ($[+2.93, +7.25] > \delta=2.67$)<br>**`C4` (`D1` corr DiD)**: $+5.79$ ($[+4.01, +7.57] > \delta=3.02$) | r2 5인 게이트 PASS<br>`victory_M2H2_r2`: **`VERIFIED_COMPLETE`**<br>(167 tests in `topic3_h2` + 138 in `topic3_spectral`, GPU 비트일치 재현) | `results/topic3/2026-11-02_h2/gate/gate_decision.json`<br>`results/topic3/2026-11-02_h2/h2_results.json`<br>`results/topic3/2026-11-02_h2/r2/2026-11-02_topic3_h2_addendum_08_r2.md` |
| **Topic 4 (`M4`)**<br>역전파 없는 국소 학습 (Masked-Lateral PSP) | 25% 희소 측방 억제 마스크(69/276 간선, $k=24$)를 갖는 엄밀 국소 유사도 매칭(PSP)에서 Mode II 허브-반발 프랙탈 위상(`C4`)이 동밀도 Erdős–Rényi 무작위 위상(`C1`)보다 48-ROI 1-스텝(2.0 s) BOLD 예측 $R^2$를 $\ge 0.01$ 높이는가? | `docs/03_empirical_analysis/topic4/2026-11-01_topic4_analysis_card.md`<br>(`2b535c39…5934`)<br>$\delta = 0.01$ ($R^2$), 교차 백분위 부트스트랩($B=2000$) | ENIGMA-OCD $\text{TR}=2.0\text{ s}$ $N=1,195$ (13개 기관; 튜닝 $181$명, 5-겹 확증 $1,014$명), 48 ROIs | `0.000` / `0.0` GPU-h<br>(DGX-Spark CPU 확증 `6.63 min`) | **`H1` (`C4 - C1`): `stop` (killed)**<br>**`S1` (`C4 - C4DP`): `killed`**<br>**`S2` (`C5 - randlin24`): `supported`**<br>**`S3` (`C5 - MLPenc`): `non-inferior`** (단, 역전파 `MLPenc`가 $+0.0047$ 높음)<br>**`C3` (Rich Club)**: `inconclusive (execution integrity)` ($10/50 = 20\%$ 불안정) | **`H1` ($\Delta_1 = S_{\text{C4}} - S_{\text{C1}}$)**: $-0.0022$, 95% CI $[-0.0041, -0.0004] < \delta = 0.01$<br>**`S1` ($S_{\text{C4}} - S_{\text{C4DP}}$)**: $-0.0016$, 98.33% CI $[-0.0038, +0.0005]$<br>**`S2` ($S_{\text{C5}} - S_{\text{randlin24}}$)**: $+0.0306$, 98.33% CI $[+0.0288, +0.0324]$<br>**`S3` ($S_{\text{C5}} - S_{\text{MLPenc}}$)**: $-0.0047$, 98.33% CI $[-0.0050, -0.0043] > -0.01$ | r1 5인 게이트 PASS<br>`victory_M4`: **`VERIFIED_COMPLETE`**<br>(전 과정 독립 재실행 바이트 일치) | `results/topic4/2026-11-01/verdict.json`<br>`results/topic4/2026-11-01/t41_counterfactual.json`<br>`results/topic4/2026-11-01/qualification.json` |

---

## 2. Topic 1 (`M1`): ENIGMA-OCD 방향성 지연 모티프(Directed Lag-Motif) 농축 실증 분석

### 2.1 연구 질문 및 기원
손운규 교수님이 제안한 제1주제는 복잡계 네트워크의 3-노드 방향성 삼각 모티프 유의성 프로파일($\vec{SP}$, Superfamily 2: 피드포워드 루프 `030T` 대 3-순환 루프 `030C`; Milo et al., *Science* 2002, 2004)을 뇌 기능 연결성에 적용하여 강박장애(OCD)의 피질-선조체-시상-피질(CSTC) 재귀 루프 과활성 가설을 검증하는 것이다.
- **일차 가설 H1 (`E1`, $Z_{\text{030C}}$)**: $N=304$ 피질·피질하 ROI의 2.0 s 재표본화 광대역 휴지기 fMRI 시계열에서 지연-1(2.0 s) 교차상관 $C_{ij} = \text{mean}_t\, z_i(t)z_j(t+1)$의 반대칭 성분 $F = C - C^\top$으로 방향을 부여한 상위 10% 밀도($k = \text{round}(0.10 \times \binom{304}{2}) = 4,606$개 방향성 간선) 그래프에서, 상호간선 보존 유향 이중 간선 교환 MCMC 영모형($M=200$) 대비 3-순환 모티프 표준화 점수 $Z_{\text{030C}}$(`E1`)가 OCD와 HC 간에 차이를 보이는가? (단, 디스크에 304-ROI 해부학 매핑 테이블이 존재하지 않아 전뇌 304-ROI 그래프만 평가하며 CSTC 부분망 국소화는 사전 배제됨; `docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md` §1, §8).
- **일차 가설 H2 (`E2`, $Z_{\text{030C}} - Z_{\text{030T}}$)**: 순환 대 피드포워드 대비 $\text{E2} = Z_{\text{030C}} - Z_{\text{030T}}$가 OCD와 HC 간에 차이를 보이는가?
- **이차 분석**: (1) 퇴화 안전 로그비 $\log((\text{obs}_{030C}+1)/(\text{null\_mean}_{030C}+1))$, (2) Family 1: 23개 기관 Leave-One-Site-Out(LOSO) 교차검증에서 3-특성 지연 모티프($[Z_{\text{030C}}, Z_{\text{030T}}, \text{gradient share}]$) 대 동일 폴드 정적 기능연결성(Static FC, 46,056개 Fisher-$z$ $\to$ 50-PCA + L2 로지스틱 회귀) 분류 AUROC, (3) Family 2: OCD 군 내 `Y-BOCS` 총점과 `E1, E2`의 연관성, (4) Family 3: OCD 군 내 약물 코드(`Medication == 1` 대 `2`) 대비.

### 2.2 사전 동결 분석 카드 및 판정·기각 규칙
- **동결 분석 카드**: `docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md` (`sha256 = 1e589f0ba5a866088a3ce93ed049163860f222edb148acc044254275d5bb75aa`, 동결 시각 `2026-10-30T12:12Z`; 영수증 `results/topic1/2026-10-30/card_sha256.txt` 및 `results/topic1/2026-10-31/manifest.json`).
- **추출 파라미터 및 라벨 결합 전 동결 부록**:
  - 추출 파라미터 해시(`params_sha256`): `86863ffad95cbd852ae4e187490e2112183dd38632166bb417158b62bfea15c6` (`src/topic1_lagmotif/pipeline.py`, `results/topic1/2026-10-31/manifest.json`).
  - 라벨 결합 전 세부 규격 부록: `docs/03_empirical_analysis/topic1/2026-10-31_topic1_prelabel_addendum.md` (`sha256 = 7ccb983ed9dedd50d9c74b433e2578a7007b11ee5397a276832382a39f55e90e`, `2026-10-31T11:14:46Z`; 영수증 `results/topic1/2026-10-31/prelabel_addendum_sha256.txt`).
  - 코호트 통계 스크립트: `scripts/topic1_cohort_stats.py` (`sha256 = 33e2757690c1dd948cf82478efbe067aa37296a05db0ab081a2073113b396e02`, 라벨 결합 전인 `2026-10-31T11:14:46Z` 동결; 영수증 `results/topic1/2026-10-31/stats_script_sha256.txt`).
- **사전 등록 판정 및 기각(Kill) 규칙** (`2026-10-30_topic1_analysis_card.md` §3–§5):
  1. **퇴화 대체 규칙(§3)**: 라벨 결합 전 `broadband@0.10`에서 $\sigma_{\text{null},m}=0$으로 인한 `E1` 또는 `E2` 퇴화 비율이 **엄밀히 $> 10\%$**(`rate > 0.10`)이면 일차 밀도를 `0.15`로 전환한다.
  2. **통계 모형 및 효과크기(§4)**: 기관 임의절편 $(1|\text{site})$과 Mundlak 기관 평균 공변량($\overline{\text{dx}}_s, \overline{\text{age}}_s, \overline{\text{sex}}_s, \overline{\log(\text{duration})}_s$)을 포함한 선형혼합모형(ML 적합)에서 $d = \hat{\beta}_{\text{dx,LMM}} / \hat{\sigma}_{\varepsilon,\text{LMM}}$ (부호: $\text{OCD} - \text{HC}$)을 산출하고, 동치인 기관 고정효과 OLS 모형에서 $|\hat{\beta}_{\text{LMM}} - \hat{\beta}_{\text{FE}}|/\text{SE}_{\text{FE}} < 0.01$ 정합성 게이트를 확인한다.
  3. **유의확률 및 다중비교(§4–§5)**: 기관 내 축소모형 잔차를 치환하는 양측 Freedman–Lane 순열검정($B=9,999$, 시드 `20261031`)으로 $p_{\text{FL}}$을 구하고, 두 일차 종점(`E1`, `E2`)에 대해 Holm–Bonferroni 보정($p_{\text{Holm}}$)을 적용한다.
  4. **생존 및 기각 기준(§5)**: 종점 $E_i$는 **$p_{\text{Holm}}(E_i) < 0.05$ 이고 동시에 $|d(E_i)| \ge 0.15$**일 때만 생존(`survives = true`)한다. **`E1`과 `E2` 중 어느 것도 생존하지 못하면 Topic 1은 즉시 기각(`KILLED`)**되며, 카드 §7 민감도 분석은 기각된 종점을 부활시킬 수 없으므로 실행·해석하지 않는다.

### 2.3 데이터셋, 표본 구성 및 연산 자원
- **데이터 원천 및 전처리** (`results/topic1/2026-10-31/manifest.json`, `results/topic1/2026-10-31/stats_results.json`):
  - 원천 경로: `/home/juke/git/enigma_ocd_mbbn/data/MBBN_data_304_ROIs_0.25/` (읽기 전용).
  - 메타데이터 총 `2,095`행 중 디스크 미존재 `389`행(설계상 배제된 $\text{TR} > 2.0\text{ s}$ 6개 기관 `388`명 + `Vancouver-BCCHR` 누락 `1`명)을 제외한 **`N = 1,706`명(OCD `869`명, HC `837`명, `23`개 기관, `46`개 기관×진단 셀)** 전원이 품질 계약을 통과하였다(`contract_error = 0`, 2.0 s 격자 최소 길이 100 샘플 [200 s] 미만 `0`명, 필수 공변량 결측 `0`명).
  - 전처리: 후단 0-패딩 제거 $\to$ 선두 $\lceil 40\text{ s}/\text{TR}\rceil$ 샘플 절단 $\to$ 원시 TR에서 선형 추세 제거 $\to$ 항에일리어싱 다상 필터(`resample_poly`)로 공통 $2.0\text{ s}$ 격자($f_N = 0.25\text{ Hz}$) 재표본화 $\to$ ROI별 표준화($\text{ddof}=0$). 2.0 s 격자 길이 범위는 `100`~`340` 샘플(중앙값 OCD `160.0`, HC `160.0`).
- **연산 자원**: GPU `0.000 GPU-h` (`results/gpu_ledger_2026-10-31.md`). 로컬 DGX-Spark CPU 14 워커(`nice 10`)에서 6개 단위(`broadband`/`curl` × 밀도 `0.05, 0.10, 0.15` = `10,236` 단위) 추출에 `4,292.26 s` (`1.19 h`), 사전 검증에 `868.47 s`, 코호트 통계 분석에 `77.77 s` 소요.

### 2.4 사전 등록 규칙에 따른 최종 판정
- **퇴화 대체 판정** (`results/topic1/2026-10-31/fallback_decision.json`): `broadband@0.10`에서 `deg_E1 = 0`, `deg_E2 = 0` (`rate_E1 = 0.0`, `rate_E2 = 0.0` $\le 0.10$)이므로 대체 규칙이 발동하지 않았으며(`fallback_triggered = false`), 일차 분석 단위는 `broadband@0.10`으로 확정되었다. (`broadband@0.05`에서만 $2/1,706 = 0.117\%$ 퇴화 발생, 나머지 5개 단위는 $0\%$).
- **일차 종점 및 주제 최종 판정** (`results/topic1/2026-10-31/stats_results.json` → `primary.decision`):
  - **`E1` ($Z_{\text{030C}}$)**: `survives = false` (`reason = "|d| < 0.15"`). Holm 보정 유의확률($p_{\text{Holm}} = 0.0446 < 0.05$)은 통과했으나, 효과크기 $d = 0.1131 < 0.15$로 사전 등록된 최소 실용 효과크기 기준에 미달하였다.
  - **`E2` ($Z_{\text{030C}} - Z_{\text{030T}}$)**: `survives = false` (`reason = "p_Holm >= 0.05; |d| < 0.15"`). $p_{\text{Holm}} = 0.4416 \ge 0.05$ 및 $d = 0.0377 < 0.15$로 두 기준 모두 미달하였다.
  - **최종 판정**: **`"Topic 1 KILLED (neither endpoint survives)"`** (`topic1_killed = true`).

### 2.5 핵심 실증 수치 및 신뢰구간

| 분석 범주 및 지표 | 추정치 (Point Estimate) | 구간 추정 / 표준오차 (95% CI 또는 SE) | 유의확률 ($p_{\text{FL}}$ / $p_{\text{Holm}}$ / $q_{\text{BH}}$) | 판정 및 비고 | 정본 결과 파일 및 JSON 키 |
|---|---|---|---|---|---|
| **일차 종점 `E1` ($Z_{\text{030C}}$, `broadband@0.10`, $N=1,706$)** | **$d = 0.113131$** (`0.113`)<br>$\hat{\beta}_{\text{LMM}} = 0.548815$ | 근사 Wald 95% CI: **$[0.014590, 0.211671]$** (`se_d = 0.050276`)<br>$\text{SE}_{\text{LMM}} = 0.243702$, $\hat{\sigma}_\varepsilon = 4.851160$ | $p_{\text{FL}} = \mathbf{0.0223}$<br>$p_{\text{Holm}} = \mathbf{0.0446}$<br>($p_{\text{Wald}} = 0.0243$) | **기각 (`survives: false`)**<br>$\|d\| = 0.113 < 0.15$<br>Mundlak 비율 $1.34\times 10^{-13} < 0.01$ | `results/topic1/2026-10-31/stats_results.json` (`primary.E1`)<br>`results/topic1/2026-10-31/report_derived_numbers.json` (`E1`) |
| **`E1` 군별 비보정 기술통계** | OCD: $-1.557729 \pm 5.306716$<br>HC: $-2.002134 \pm 4.886956$ | 비보정 Cohen's $d = 0.087051$ | Welch $p = 0.0720$ | 두 군 모두 영모형 대비 $Z_{\text{030C}} < 0$ (구배 지배) | `results/topic1/2026-10-31/stats_results.json` (`primary.E1`) |
| **일차 종점 `E2` ($Z_{\text{030C}} - Z_{\text{030T}}$, `broadband@0.10`, $N=1,706$)** | **$d = 0.037689$** (`0.038`)<br>$\hat{\beta}_{\text{LMM}} = 0.343871$ | 근사 Wald 95% CI: **$[-0.060873, 0.136251]$** (`se_d = 0.050287`)<br>$\text{SE}_{\text{LMM}} = 0.458350$, $\hat{\sigma}_\varepsilon = 9.123959$ | $p_{\text{FL}} = \mathbf{0.4416}$<br>$p_{\text{Holm}} = \mathbf{0.4416}$<br>($p_{\text{Wald}} = 0.4531$) | **기각 (`survives: false`)**<br>$p_{\text{Holm}} \ge 0.05$ 및 $\|d\| < 0.15$<br>Mundlak 비율 $1.97\times 10^{-13} < 0.01$ | `results/topic1/2026-10-31/stats_results.json` (`primary.E2`)<br>`results/topic1/2026-10-31/report_derived_numbers.json` (`E2`) |
| **`E2` 군별 비보정 기술통계** | OCD: $+6.375704 \pm 9.659078$<br>HC: $+6.183636 \pm 9.674975$ | 비보정 Cohen's $d = 0.019869$ | Welch $p = 0.6817$ | $Z_{\text{030T}}$ 평균: OCD $-7.9334$, HC $-8.1858$ | `results/topic1/2026-10-31/stats_results.json` (`primary.E2`, `descriptives_all_units`) |
| **이차: 퇴화 안전 로그비** ($\log((\text{obs}_{030C}+1)/(\text{null}+1))$, $N=1,706$) | **$d = 0.089710$** (`0.090`)<br>$\hat{\beta}_{\text{LMM}} = 0.045331$ | $\text{SE}_{\text{LMM}} = 0.025384$, $t_{\text{FE}} = 1.784585$ | $p_{\text{FL}} = \mathbf{0.0665}$<br>($p_{\text{Wald}} = 0.0741$) | 유의하지 않음 (OCD $-0.2020 \pm 0.5344$, HC $-0.2224 \pm 0.5415$) | `results/topic1/2026-10-31/stats_results.json` (`log_ratio_030C_secondary`) |
| **Family 1: 23-기관 LOSO 분류 — 지연 모티프 (3 특성)** | 합산 OOF AUROC = **`0.515685`** (`0.516`)<br>기관 평균 AUROC = `0.555433` | 기관 군집 부트스트랩(2,000회) 95% CI: **`[0.468092, 0.559912]`** | 기술통계 전용 (`Pre-Label Addendum P11`) | 우연 수준(0.50)을 벗어나지 못함 | `results/topic1/2026-10-31/stats_results.json` (`secondary_family1_classification.lagmotif`) |
| **Family 1: 23-기관 LOSO 분류 — 정적 FC 기준선 (50-PCA + L2)** | 합산 OOF AUROC = **`0.563024`** (`0.563`)<br>기관 평균 AUROC = `0.558911` | 기관 군집 부트스트랩(2,000회) 95% CI: **`[0.523933, 0.600355]`** | 기술통계 전용 | 동일 피험자·폴드에서 정적 FC가 지연 모티프보다 높음 | `results/topic1/2026-10-31/stats_results.json` (`secondary_family1_classification.static_fc_comparator_same_subjects_same_folds`) |
| **Family 2: OCD 내 Y-BOCS 중증도 ($n=856$, 23개 기관)** | `E1`: $\beta_{\text{std}} = 0.031925$ ($\beta = 0.040085$)<br>`E2`: $\beta_{\text{std}} = 0.028837$ ($\beta = 0.019977$) | `E1`: $\text{SE} = 0.040132, t = 0.9988$<br>`E2`: $\text{SE} = 0.022556, t = 0.8857$ | `E1`: $p_{\text{FL}} = 0.3073, q_{\text{BH}} = 0.3609$<br>`E2`: $p_{\text{FL}} = 0.3609, q_{\text{BH}} = 0.3609$ | 임상 중증도와 무관 | `results/topic1/2026-10-31/stats_results.json` (`secondary_family2_ybocs`) |
| **Family 3: OCD 내 약물 코드 1 vs 2 ($n=301$: $180$ vs $121$, 11개 기관)** | `E1`: $d_{\text{FE}} = -0.085564$ ($\beta = -0.552382$)<br>`E2`: $d_{\text{FE}} = -0.198656$ ($\beta = -2.162068$) | `E1`: $\text{SE} = 0.839688, t = -0.6578$<br>`E2`: $\text{SE} = 1.415586, t = -1.5273$ | `E1`: $p_{\text{FL}} = 0.5682, q_{\text{BH}} = 0.5682$<br>`E2`: $p_{\text{FL}} = 0.1550, q_{\text{BH}} = 0.3100$ | 유의한 약물 차이 없음 | `results/topic1/2026-10-31/stats_results.json` (`secondary_family3_medication`) |
| **동결 후 기술적 민감도: 영모형 수락률 하위 10%($\le 0.4836$) 제외 ($n=1,535$)** | `E1`: **$d = 0.129631$** (`0.130`)<br>`E2`: **$d = 0.094895$** (`0.095`) | `E1`: $\hat{\beta}_{\text{LMM}} = 0.553556, \text{SE} = 0.225548$<br>`E2`: $\hat{\beta}_{\text{LMM}} = 0.755011, \text{SE} = 0.420166$ | `E1`: $p_{\text{FL}} = 0.0143$<br>`E2`: $p_{\text{FL}} = 0.0666$ | `E1` 효과크기 여전히 $\|d\| < 0.15$ 미달 | `results/topic1/2026-10-31/stats_results.json` (`acceptance_stratified_POSTFREEZE`) |

### 2.6 5인 검증 게이트 및 독립 승리 감사 상태
- **5인 검증 게이트 (`M1_r1`)**: `reviewer_M1_r1_1` (`APPROVE`), `reviewer_M1_r1_2` (`APPROVE`), `challenger_M1_r1_1` (`CONFIRMED`), `challenger_M1_r1_2` (`CONFIRMED`), `auditor_M1_r1` (`CLEAN`) 전원 통과.
- **독립 승리 감사 (`victory_M1_b`)**: `.agents/teamwork/tw-20261031-four-topics/victory_M1_b/handoff.md` (`2026-11-01T00:58Z`)에서 **`VERIFIED_COMPLETE` (`VICTORY CONFIRMED`)** 판정.
  - 테스트 스위트: `tests/topic1_lagmotif` **88 passed**, 기존 4토픽+E2E 스위트 **86 passed**.
  - 변이 테스트(`results/topic1/2026-10-31/t1_1_mutation/v3_final_tree/`): T1.1 추출 변이 `19/19` + 추가 변이 `4/4` = **`23/23` 전수 사살(`0` 생존)**, T1.2 통계 변이 **`24/24` 전수 사살(`0` 생존)**.
  - 독립 재검증: 7개 TR을 대표하는 8개 피험자 원시 `.npy` 재추출 시 저장된 JSON과 바이트 단위 일치 확인; 클린룸 독립 재구현(`probe_independent_stats.py`)에서 $d(\text{E1}) = 0.113131$, $d(\text{E2}) = 0.037689$ 동일 재현.

### 2.7 일탈 사항 및 부록(Addenda) 정오표
1. **카드 §12 실행 전 외부 리뷰 요건 일탈 (`docs/03_empirical_analysis/topic1/2026-10-31_topic1_deviations_addendum.md` 항목 1)**: 카드 §12는 `analyze` 실행 전 `trinity review --difficulty hard` 완료를 요구했으나 당시 `codex` 바이너리 부재로 부분 실행에 그쳤고, 실행 후 5인 검증 게이트와 독립 승리 감사(`victory_M1_b`)로 대체 검증되었다. 이는 PI 의사결정 제4항(`PI_DECISIONS_2026-11-01.md`: `"승인 (권장)"`)으로 공식 승인되었다.
2. **라벨 비결합 추출 선행 (`D1`) 및 2회 합성 검증 (`D2, D4`)**: 라벨을 읽지 않는 1차 특성 추출(`08:16Z–09:27Z`)이 통계 스크립트 최종 바이트 동결(`11:14:46Z`)보다 먼저 수행되었으나, 진단 라벨과의 결합(`analyze`, `11:15:03Z`)은 모든 스크립트·부록 동결 및 합성 검증(`stats_validation_final.json`, `11:13:02Z`) 완료 이후에 수행되었다.

### 2.8 미검증 항목 및 후속 연구 요구 조건
- **미검증 항목**: (1) 일차 종점이 생존하지 못함에 따라 카드 §5/§7 규칙에 의해 실행하지 않은 민감도 분석 일체(밀도 $5\%, 15\%$, 구배 점유율 공변량 보정, `curl` 전용 채널, DCT 128 s 고역통과 `V1`, 200 s 공통 절단 `V3`, 순위 역정규 변환, 성인 전용 $\text{age}\ge 18$, 스왑 시도 계수 40배 `V2` 등; `results/topic1/2026-10-31/stats_sensitivity.json`), (2) 304-ROI 해부학 매핑 부재로 인한 CSTC 회로 특이적 모티프 분석, (3) 원본 저장소 문서 상충으로 인한 약물 코드 1 대 2의 실제 투약 방향. 또한 `E1`의 점추정치($d=0.113$)는 기각 기준($0.15$) 미만이나 근사 95% 신뢰구간($[0.015, 0.212]$) 상한은 $0.15$를 포함한다.
- **후속 연구 요구 조건** (`docs/03_empirical_analysis/topic1/2026-10-31_topic1_result_report.md` §5–§6): 두 군 모두에서 관찰된 대규모 음의 $Z_{\text{030T}} \approx -8.0$ 및 $Z_{\text{030C}} \approx -1.8$ 편향은 공통 무지연 전역 신호(global signal)와 영역별 혈류역학 지연(HRF latency SD $\approx 1\text{–}2\text{ s}$)의 결합이 지연-1 교차상관에 위상 구배(potential flow)를 유도하기 때문이다(카드 §9). 따라서 후속 연구는 **신규 사전 동결 카드** 하에서 (i) 블라인드 HRF 디컨볼루션 또는 영역별 지연 보정, (ii) 프레임별 변위(FD) 머리 움직임 공변량 확보, (iii) 304-ROI 해부학적 CSTC 조회표 및 약물 코드북 검증을 선결해야 한다.

---

## 3. Topic 2 (`M3` 및 후속 `FU-A`~`FU-E`): SwiFT 커넥톰 박스-커버링 재규격화군(RG) 풀링 실증 분석

### 3.1 연구 질문, 아키텍처 실측(T2.1) 및 실험 설계
손운규 교수님이 제안한 제2주제는 뇌 커넥톰의 박스-커버링 프랙탈 차원($N_B \sim l_B^{-d_B}$) 및 허브-반발(Mode II disassortative fractality; Song, Havlin & Makse, *Nature* 2005, *Nature Physics* 2006) 원리를 4D fMRI 파운데이션 모델 SwiFT의 공간 병합(spatial pooling) 연산에 도입하여 유클리드 격자 병합을 대체하는 것이다.

#### 3.1.1 아키텍처 코드 실측 결과 (`T2.1`, `docs/03_empirical_analysis/topic2/2026-11-01_topic2_architecture.md`)
- **과거 전제 기각**: 기존 문헌·예비 보고서는 `layer_2`와 `layer_3`(모두 1536차원) 사이에 `PatchMerging`이 존재한다고 가정했으나, `simmim_swin4d_transformer_ver11.py` (`SwiFT_v2` 커밋 `f0dc7aca`, `sha256 = de132387f64d98cbe9b15876351a7b33f9bec112df3df8f4718327d06e95052a`, `src/topic2_rgpool/vendor_swift_ver11/`에 벤더링) 1068행(`downsample=down_sample_mod if (i_layer < self.num_layers - 1) else None`)과 1382–1412행을 실측한 결과 **`layer_2`와 `layer_3` 사이에는 공간 병합이 존재하지 않는다.**
- **실제 공간 병합 위치**: `PatchMergingV2`(41–88행)는 시간을 병합하지 않고($t_{\text{out}} = t_{\text{in}} = 20$) 공간 $2\times 2\times 2$ 자식 토큰 8개를 연결(`8C`)한 뒤 `LayerNorm(8C) + Linear(8C → 2C, bias=False)`를 적용하며, 오직 **Stage 0 끝(`M0`: $16^3 \to 8^3$, $12\text{ mm} \to 24\text{ mm}$), Stage 1 끝(`M1`: $8^3 \to 4^3$, $24\text{ mm} \to 48\text{ mm}$), Stage 2 끝(`M2`: $4^3 \to 2^3$, $48\text{ mm} \to 96\text{ mm}$)**의 세 곳에만 존재한다.
- **`M0` 단독·팔분체(octant) 내부 개입의 필연성**: (i) `M0` 입력 격자($16^3 = 4,096$개 12 mm 셀)만이 재그룹화할 수 있는 충분한 뇌 내부 셀(`1,442`개 뇌 접촉 셀, `1,195`개 신호 셀[$\ge 54/216$ 뇌 복셀], `234/512`개 뇌 접촉 $2\times 2\times 2$ 블록; `results/topic2/2026-11-01/partitions/partitions_hcp.json`)을 보유하며, (ii) Stage 1 기본 윈도우($(4,4,4,10)$), `M1/M2`, 그리고 `decoder_type='mlp'` 디코더(각 최종 토큰이 자신의 $48^3$ 복셀 팔분체만 독립 복원)가 모두 $8\times 8\times 8$ 팔분체 단위로 정렬되어 있으므로, `ConnectomeRGBoxPooling`(`src/topic2_rgpool/merge.py`)은 **`M0`의 `PatchMergingV2` 직전에 배치되는 무파라미터 팔분체-내부 순열 연산자 $\pi$**로 설계되었다. $\pi = \text{identity}$(`E` 암)일 때 순정 `PatchMergingV2`와 비트 단위로 동일하며, 파라미터 수·토큰 격자·FLOPs가 모든 암(`E, C, S`)에서 완전히 동일하다.

#### 3.1.2 본실험(`M3`) 및 5대 후속 실험(`FU-A`~`FU-E`) 설계 총괄
PI 의사결정 제7항(`PI_DECISIONS_2026-11-01.md`: `"+ 후속 A–E 전부"`, 총 GPU 상한 `95.0 GPU-h` 승인)에 따라 본실험 `M3`의 r2 게이트 보수(`r3`)와 결과 보고서 §7에 비용 추산된 5개 후속 실험(`FU-A`~`FU-E`)이 각각 독립된 날짜별 사전 동결 카드 하에 B300 Slurm에서 수행되었다:
1. **`M3` (본실험, `r1–r3`)**: SwiFT `E36_d2262`(`38,712,096` 파라미터), 2 mm 복셀 타깃, 1× 예산(`8,750` 스텝 × 배치 16 = `140,000` 샘플), 3개 암(`E`: 유클리드 큐브, `C`: 학습군 Fisher-$z$ 평균 FC 상관거리 $\sqrt{2(1-r)}$ 기반 크기-8 균형 박스 [231개 행 / 1,512개 셀 재그룹화], `S`: 팔분체 내 거리-구간 보존 FC 셔플 대리군) × 5개 시드(`0..4`).
2. **`FU_A` (후속 A — 저잡음 12 mm 셀-평균 타깃)**: `E36_d2262`, 1× 예산(140k 샘플), SimMIM 입력·타깃을 12 mm 셀-평균장 $y_{v,t} = \kappa \cdot m_{c(v),t}$ ($\kappa = 1/\sqrt{Q} = 5.699892$, 학습군 잡음 바닥 비율 $NF = 0.208508$, 합성 보정 잡음 $\sigma_v = 6.545925$)로 교체.
3. **`FU_B` (후속 B — 4× 학습 예산)**: `E36_d2262`, 2 mm 복셀 타깃, 4× 예산(`35,000` 스텝 × 배치 16 = `560,000` 샘플, 5% = `1,750` 스텝 워밍업 코사인 감쇠), `E, C, S` × 5개 시드(`0..4`).
4. **`FU_C` (후속 C — 8개 신규 독립 시드)**: `E36_d2262`, 2 mm 복셀 타깃, 1× 예산(140k 샘플), 신규 시드 `10..17` ($n=8, \text{df}=7$, 24개 Stage-1 실행)로 $t$-신뢰구간 폭 축소 검증.
5. **`FU_D` (후속 D — `E192_d22182` 모델 스케일 확장)**: SwiFT `E192_d22182`(`474,226,176` 파라미터, $\approx 12.2\times$ E36; `embed_dim=192`, `depths=(2,2,18,2)`, `num_heads=(6,12,24,48)`, `M0` 투영 $1536\to 384$, 최종 토큰 1536차원), 1× 예산(140k 샘플), 시드 0 $F^+$ 게이트 선행.
6. **`FU_E` (후속 E — 동결 인코더 하류 개인식별력 프로브)**: 저장된 r1 Stage-1 15개 동결 체크포인트(`hcp_{E,C,S}_s{0..4}/model_final.pt`)에서 홀드아웃 $N=24$명(`16` test + `8` val, 공통 마스크 `190,382` 복셀)의 스캔 전/후반(각 580 TR, 40-TR 간격, 반분할별 독립 재표준화) 288채널 공분산 상삼각(`cov2`, `41,328` 특성) 기반 개인식별력 $I_{\text{diff}} = 100\times(\text{mean diag } R - \text{mean off-diag } R)$ 비교.

### 3.2 사전 동결 분석 카드 및 판정·기각 규칙 (`M3` 및 `FU-A`~`FU-E`)
모든 마일스톤은 PI 의사결정 제3항에 따라 최소 실용 효과크기 임계치를 **$\delta = 0.01$ (`1.00%` 상대 이득)**로 동결하였다.

| 마일스톤 | 사전 동결 카드 경로 및 SHA256 | 동결 시각 (UTC) 및 영수증 경로 | 합성 게이트 ($F^+, F^-$) 규칙 | Stage-1 주 판정 및 기각(Kill) 규칙 |
|---|---|---|---|---|
| **`M3`** | `docs/03_empirical_analysis/topic2/2026-11-01_topic2_card.md`<br>`c9bfc60af87f45d4541f10b1f5e074215e235d3e4fd99f001f69f8d8585c41f5` | `2026-11-01T03:14:34Z`<br>`results/topic2/2026-11-01/card_sha256.txt`<br>`code_sha256_at_freeze.txt` (`33/33`) | **$F^+$** (시드 0,1): $(E-C)/E \ge 1\%$ 및 $(S-C)/S \ge 1\%$<br>**$F^-$** (시드 0,1): $(E-C)/E < 1\%$ | $I_1 = (E-C)/E$, $I_2 = (S-C)/S$ (5 시드 95% $t$-CI, `df=4`):<br>• **`stop` (killed)**: $\text{hi}(I_1) < 0.01$<br>• **`keep`**: $\text{mean}(I_1)\ge 0.01 \land \text{lo}(I_1)>0 \land \text{lo}(I_2)>0$ ($F^-$ 통과)<br>• **`modify`**: $\text{mean}(I_1)\ge 0.01 \land \text{lo}(I_1)>0 \land \text{lo}(I_2)\le 0$<br>• **`inconclusive`**: 그 외 또는 $F^+$ 실패 |
| **`FU_A`** | `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_a_card.md`<br>`72be3e83c43f17990d6ed4ab8e2f254894c083f697dfe18557866866623618fb` | `2026-11-01T16:06:01Z` (작업 `507` 제출 `16:12:31Z` 이전)<br>`results/topic2/2026-11-02_fu_a/card_sha256.txt` (`8/8`) | **$F^+$** (시드 0, $\sigma_v=6.5459$): $(E-C)/E \ge 1\%$. 미달 시 Stage-1 미실행 및 즉시 **`inconclusive` (measurement capacity)** | $F^+$ 통과 시에만 Stage-1 실행; $\text{hi}(I_1) < 0.01$ 및 전제 $M$ ($\text{val NMSE}_E \le 0.90909$) 충족 시 `stop` |
| **`FU_B`** | `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_card.md`<br>v1: `a9c4cab0…6e0726` (`16:05:18Z`)<br>v2: `994f01446d35b706de899ef00af1ce65db8c55c45da7891f4011f17485c4daae` | v2 `2026-11-01T16:20:25Z` (`509_0` 시작 `16:20:41Z` 이전)<br>`results/topic2/2026-11-02_fu_b/card_sha256_v2.txt` (`31/31`) | **4× $F^+$** (시드 0, 35k 스텝): $(E-C)/E \ge 1\%$ 및 $(S-C)/S \ge 1\%$<br>**$F^-$**: r1 `verdict.json`에서 상속(`true`) | `M3`와 동일 (`df=4`): $\text{hi}(I_1) < 0.01 \implies$ **`stop` (killed)** |
| **`FU_C`** | `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_c_card.md`<br>`fc2d0672de2bb3163f80b06079ad973c7332cd8b46808bdd59c6456164944ecb` | `2026-11-01T16:13:23Z` (첫 시작 `16:35:09Z` 이전)<br>`results/topic2/2026-11-02_fu_c/card_sha256.txt` | 앵커 작업 `501`에서 스텝 100/200 손실 비트 일치 입증 후 r1 12개 $F^+/F^-$ 기록을 참조로 재검증 | 신규 시드 `10..17` ($n=8, \text{df}=7$) 양측 95% $t$-CI:<br>$\text{hi}(I_1) < 0.01 \implies$ **`stop` (killed)** |
| **`FU_D`** | `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_d_card.md`<br>`1b7fee6c2dcee404998200810237235cbf4d28bdae642dc9171905825036001b` | `2026-11-01T16:06:07Z` (스모크 `511` 제출 `16:13:50Z` 이전)<br>`results/topic2/2026-11-02_fu_d/card_sha256.txt` | **`E192` $F^+$** (시드 0, 8,750 스텝): $(E-C)/E \ge 1\%$ 및 $(S-C)/S \ge 1\%$. 미달 시 Stage-1 미실행 및 **`inconclusive` (measurement capacity)** | 8단계 규칙(§8): Step 2에서 $F^+$ 실패 시 `inconclusive`; 통과 시 비용 기반 시드 수 $n\in\{5,4,0\}$ 결정 후 $\text{hi}(I_1) < 0.01 \implies$ `stop` |
| **`FU_E`** | `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_e_card.md`<br>`072553b0912a86ee786e82f13d9fdc873a6681c9ba6feb5ffc5d8e0ddc36b88f` | `2026-11-01T16:22:56Z` (작업 `524` 제출 `16:24:31Z` 이전)<br>`results/topic2/2026-11-02_fu_e/card_sha256.txt` | **`G0`**(15개 체크포인트 재채점 `rtol<=1e-5`), **`F+`**(15개 전 슬롯 $I_{\text{diff}} > p_{95}$ 및 암 평균 $\ge 2.0$), **`F-`**(해부학 교란 $< p_{95}$), **`G2`**(실데이터 용량), **`G3`**(원시 `cellfc` $> p_{95}$) | `F+`, `G2`, `G3` 중 하나라도 실패 시 **`inconclusive`**; 모두 통과 시 $J_{1,s} = (I_{\text{diff},C,s}-I_{\text{diff},E,s})/I_{\text{diff},E,s}$ (`df=4`)에서 $\text{hi}(J_1) < 0.01 \implies$ `stop` |

### 3.3 데이터셋, 표본 구성, C4 비식별화 및 연산 자원
- **HCP-YA Open Access 표본 및 분할** (`results/topic2/2026-11-01/hcp_manifest.json`, `results/topic2/2026-11-01/split.json`):
  - B300 `b300-01`(`61.107.201.98`)의 `/scratch/data/hcp/download_HCP_REST1_filtered`에 스테이징된 `rfMRI_REST1_LR_hp2000_clean.nii.gz`(PI 의사결정 제2항에 의해 공개 데이터셋으로 승인, 원시 텐서·체크포인트 외부 반출 0건).
  - 총 `93`개의 `REST1_LR` 중 탐색 에이전트가 개발에 사용한 `5`명을 염처리 해시로 영구 배제(burn)하고, 형상 `91×109×91×1200` QC를 통과한 **`88`명**을 결정론적 해시(`topic2-m3-split-2026-11-01`)로 **`64`명 TRAIN (`7,616`개 윈도우, 20 TR stride 10), `8`명 VAL (`480`개 윈도우), `16`명 TEST (`960`개 비중첩 20 TR 윈도우; `h13, h23, h39, h40, h42, h44, h47, h48, h49, h51, h53, h57, h59, h70, h73, h85`)**으로 분할하였다.
- **C4 개인식별정보 위생 조치 및 봉인** (`docs/03_empirical_analysis/topic2/2026-11-01_topic2_addendum_05.md`, `2026-11-02_topic2_addendum_06.md`, `2026-11-02_topic2_fu_c_addendum_02.md`, `addendum_03.md`):
  - `M3` r2에서 저장소 내 19개 파일의 비염처리 16자리 콘텐츠 해시 및 파일 크기 지문을 위치 인덱스 `h00..h87`로 치환(`results/topic2/2026-11-01/c4_sanitized_sha256.txt`, `19/19 OK`)하고 원본 19개 파일을 저장소 외부(`~/.local/share/00IITP-AI_sealed/topic2/sealed_c4_from_b300`, `0700`)에 봉인하였다.
  - 개발용 5명 배제 솔트 파일 역시 저장소 외부(`~/.local/share/00IITP-AI_sealed/topic2/dev_subject_salt.txt`, `0400`)로 격리되었으며(`v02_salt_scan.out.json`: 0건), `FU-C` r1/r2의 근접 사본 302개 파일도 `~/.local/share/00IITP-AI_sealed/topic2/fu_c_r2_nearcopy_2026-11-02/`에 봉인되어 작업 트리와 git 블롭 전수 스캔에서 C4 위반 `0`건이 확인되었다(`c4_check_r3_by_victory.out.json`).
- **Topic 2 연산 자원 합계** (`results/gpu_ledger_2026-10-31.md`):
  - B300 총 사용량 **`58.409 GPU-h`**: `M3` `11.990 GPU-h` (상한 14.0) + `FU-A` `0.952 GPU-h` (상한 8.0) + `FU-B` `30.720 GPU-h` (상한 33.0) + `FU-C` `10.697 GPU-h` (상한 13.0) + `FU-D` `3.720 GPU-h` (상한 25.0) + `FU-E` `0.330 GPU-h` (상한 1.5). 모든 항목이 개별 상한 이내에서 완료되었다.

### 3.4 사전 등록 규칙에 따른 최종 판정 (`M3` 및 `FU-A`~`FU-E`)
1. **`M3` (본실험, `E36`, 1× 예산, 5 시드)**: **`stop` (killed)** (`results/topic2/2026-11-01/verdict.json`, `sha256 = 59af05e5…af68`). $F^+$(`+3.06%, +2.93%`)와 $F^-$(`-1.74%`) 게이트를 모두 통과한 상태에서 Stage-1 $I_1$의 95% $t$-구간 상한(`+0.361%`)이 $\delta = 1.00\%$ 미만이다.
2. **`FU_A` (12 mm 셀-평균 타깃, `E36`, 1× 예산)**: **`inconclusive` (measurement capacity)** (`results/topic2/2026-11-02_fu_a/verdict.json`, `sha256 = 57b98f0d…9656`). 실제 HCP 학습군 잡음 바닥($NF=0.2085$)에 맞춘 합성 $F^+$ 게이트(시드 0)에서 $g(C\text{ vs }E) = +0.5511\% < \delta = 1.00\%$로 측정 용량 게이트를 통과하지 못해 카드 §7.3/§8.3 규칙에 따라 HCP Stage-1을 실행하지 않았다.
3. **`FU_B` (4× 학습 예산 = 560k 샘플, `E36`, 5 시드)**: **`stop` (killed)** (`results/topic2/2026-11-02_fu_b/verdict.json`, `sha256 = 262b9c79…e142`). 4× $F^+$ 게이트(`+3.73%, +3.70%`)를 통과하고 13/15개 실행에서 1× 대비 시험 NMSE가 감소(`E_improved = true`)했으나, Stage-1 $I_1$의 95% $t$-구간 상한(`+0.425%`)이 여전히 $\delta = 1.00\%$ 미만이다.
4. **`FU_C` (8개 신규 독립 시드 `10..17`, `E36`, 1× 예산)**: **`stop` (killed)** (`results/topic2/2026-11-02_fu_c/verdict.json`, `sha256 = 4d793102…480f5`). 8개 신규 시드(`df=7`)에서 $I_1 = -0.113\%$, 95% $t$-CI $[-0.499\%, +0.272\%]$로 상한이 $\delta = 1.00\%$ 미만이며, r1의 `stop` 판정이 독립 시드들에서 그대로 재현되었다.
5. **`FU_D` (`E192_d22182` 스케일 확장, 1× 예산)**: **`inconclusive` (measurement capacity)** (`results/topic2/2026-11-02_fu_d/verdict.json`, `sha256 = f6b295d9…59fc`). `E192`(474.2M)에서 `E` 암 자체가 합성 $F^+$ 신호를 강하게 학습(`0.6769 -> 0.6558`)하여 `C`와 `E`의 격차가 $+0.3631\% < 1.00\%$로 축소되었고, 카드 §7.1/§8 Step 2에 따라 HCP Stage-1을 실행하지 않았다(r1 `E36` `stop` 단독 유지).
6. **`FU_E` (동결 인코더 하류 개인식별력 $I_{\text{diff}}$)**: **`inconclusive` (measurement capacity)** (`results/topic2/2026-11-02_fu_e/verdict.json`, `sha256 = d4d92a98…`). r1에서 정체되었던 `hcp_S_s2` 체크포인트가 합성 $F^+$ 게이트에서 $I_{\text{diff}} = 5.76 \le p_{95} = 10.59$로 탈락하여 전 슬롯 통과 규칙을 충족하지 못했다. 설령 `F+`가 통과했더라도 본분석 $J_1 = +8.11\%$의 95% $t$-CI($[-6.60\%, +22.81\%]$)가 $0$과 $\delta = 1.00\%$를 모두 포함하므로 반사실적 판정 역시 `inconclusive`이다.

### 3.5 핵심 실증 수치 및 신뢰구간 (`M3` 및 `FU-A`~`FU-E`)

#### 표 3.5a: Stage-0 무학습 박스 응집도 지표 (`M3`, HCP 홀드아웃 $n=16$ 시험군, 기저는 $n=64$ 학습군에서 적합)
*정본 출처*: `results/topic2/2026-11-01/stage0_hcp.json`

| 암 / 대비 | 박스 내 평균 상관 (`r_mean`) | 상위 2개 주성분 설명분산비 (`pca2`) | 공간 분산도 (`dispersion`, 12 mm 셀 단위) | 95% 쌍대 피험자 부트스트랩 CI ($n=16$) | 정본 JSON 키 |
|---|---|---|---|---|---|
| **`E` (유클리드 $2\times 2\times 2$ 큐브)** | `0.257015` (`0.257`) | `0.529554` (`0.530`) | `0.7838` | 기준선 (이동 셀 0개) | `arm_means.E` |
| **`C` (커넥톰 균형 박스)** | `0.260925` (`0.261`) | `0.477987` (`0.478`) | `1.4693` | 231/234 블록, 1,512개 셀 재그룹화 | `arm_means.C` |
| **`S_mean` (거리보존 대리군 5시드 평균)** | `0.189437` (`0.189`) | `0.446837` (`0.447`) | `1.5570–1.6737` | 231–232 블록, 1,514–1,574개 셀 재그룹화 | `arm_means.S_mean` |
| **`G` (유클리드 탐욕 성장)** / **`R` (무작위)** | `G`: `0.232798` / `R`: `0.132206` | `G`: `0.473519` / `R`: `0.400388` | `G`: `1.1121` / `R`: `2.4567` | 기술적 비교군 | `arm_means.{G,R}` |
| **대비 `C - E`** | **`+0.003910`** (`11/16`명에서 `C > E`) | **`-0.051567`** (`0/16`명에서 `C > E`) | $+0.6855$ | `r_mean`: **`[+0.000474, +0.007384]`**<br>`pca2`: **`[-0.053458, -0.049758]`** | `contrasts["r_mean:C-E"]`, `contrasts["pca2:C-E"]` |
| **대비 `C - S_mean`** | **`+0.071489`** (`16/16`명에서 `C > S`) | **`+0.031150`** (`16/16`명에서 `C > S`) | $-0.088\sim -0.204$ | `r_mean`: **`[+0.066758, +0.076195]`**<br>`pca2`: **`[+0.028847, +0.033665]`** | `contrasts["r_mean:C-S_mean"]`, `contrasts["pca2:C-S_mean"]` |

#### 표 3.5b: `M3` 및 `FU-A`~`FU-E` 합성 게이트 및 Stage-1 / 하류 프로브 핵심 수치 총괄

| 마일스톤 / 분석 구분 | 암별 평균 시험 지표 (`E` / `C` / `S`) | 일차 대비 $I_1$ 또는 $J_1$ ($C$ vs $E$) [95% $t$-CI] | 이차 대비 $I_2$ 또는 $J_2$ ($C$ vs $S$) [95% $t$-CI] | 부트스트랩 / 비정체 민감도 분석 [95% CI] | 정본 결과 파일 및 JSON 키 |
|---|---|---|---|---|---|
| **`M3` 합성 게이트 ($F^+$ / $F^-$, 시드 0–1)** | **$F^+$ NMSE**: `E` `0.678617`, `C` `0.657846`, `S` `0.677736`<br>**$F^-$ NMSE**: `E` `0.239336`, `C` `0.243494`, `S` `0.243729` | **$F^+$**: $+3.061\%$ (`+0.030607`, `pass`)<br>**$F^-$**: $-1.737\%$ (`-0.017373`, `pass`) | **$F^+$**: $+2.935\%$ (`+0.029347`, `pass`)<br>**$F^-$**: $+0.096\%$ (`+0.000963`) | 모든 게이트 기준 충족 | `results/topic2/2026-11-01/verdict.json` (`fixture_gates`) |
| **`M3` Stage-1 본분석 (5 시드 `0..4`, `df=4`)** | **시험 NMSE**:<br>`E`: `0.988922`<br>`C`: `0.987467`<br>`S`: `0.992175` (`S_s2 = 1.000001` 정체) | **`+0.147%`** (`+0.001468`, SE `0.000773`)<br>**95% $t$-CI: `[-0.068%, +0.361%]`** (`[-0.000677, +0.003614]`, $p=0.1302$) | **`+0.473%`** (`+0.004733`, SE `0.001701`)<br>**95% $t$-CI: `[+0.001%, +0.946%]`** (`[+9.82e-06, +0.009455]`, $p=0.0497$) | **계층 부트스트랩**: $I_1$ `[+0.025%, +0.292%]`, $I_2$ `[+0.256%, +0.825%]`<br>**시드 2 제외(`df=3`)**: $I_1 = +0.083\%$ `[-0.095%, +0.261%]`, $I_2 = +0.307\%$ `[+0.160%, +0.454%]` (`stop`) | `results/topic2/2026-11-01/verdict.json` (`primary_t`, `secondary_bootstrap`)<br>`results/topic2/2026-11-01/posthoc_sensitivity_without_seed2.json` |
| **`FU_A` 합성 게이트 (시드 0, 12 mm 셀-평균, $\sigma_v=6.5459$)** | **$F^+$ 시험 NMSE**:<br>`E`: `0.774678`<br>`C`: `0.770409`<br>(`S`: 미실행) | **$F^+$ 이득**: **`+0.5511%`** (`+0.005511 < 0.01`, **`fail`**) | 미실행 (`not_run`) | Stage-0 CPU $F^+$ 박스 내 $r$: `E` `0.071`, `C` `0.338` (순도 `1.00`); 실현 잡음비 `0.248` vs 보정 `0.2085` | `results/topic2/2026-11-02_fu_a/verdict.json`<br>`results/topic2/2026-11-02_fu_a/runs/Fplus_{E,C}_s0/run.json` |
| **`FU_B` 4× 합성 게이트 (시드 0, 35,000 스텝)** | **4× $F^+$ 시험 NMSE**:<br>`E`: `0.655099`<br>`C`: `0.630692`<br>`S`: `0.654914` | **4× $F^+$**: **`+3.726%`** (`+0.037257`, `pass`)<br>**$F^-$**: r1 상속 (`pass: true`) | **4× $F^+$**: **`+3.699%`** (`+0.036986`, `pass`) | 1× 대비 $F^+$ 이득 소폭 확대 (`+3.06% -> +3.73%`) | `results/topic2/2026-11-02_fu_b/gate_4x.json`<br>`results/topic2/2026-11-02_fu_b/verdict.json` (`fplus_gate_4x`) |
| **`FU_B` Stage-1 본분석 (4× 예산, 5 시드 `0..4`, `df=4`)** | **시험 NMSE**:<br>`E`: `0.988111` (`E_s0 = 1.000000` 정체)<br>`C`: `0.987472` (`C_s0 = 0.994161`)<br>`S`: `0.986563` | **`+0.063%`** (`+0.000631`, SE `0.001303`)<br>**95% $t$-CI: `[-0.299%, +0.425%]`** (`[-0.002987, +0.004250]`, $p=0.6534$) | **`-0.092%`** (`-0.000925`, SE `0.001995`)<br>**95% $t$-CI: `[-0.646%, +0.461%]`** (`[-0.006463, +0.004614]`, $p=0.6670$) | **계층 부트스트랩**: $I_1$ `[-0.078%, +0.338%]`, $I_2$ `[-0.496%, +0.228%]`<br>**시드 0 제외(`df=3`)**: $I_1 = -0.067\%$ **`[-0.091%, -0.043%]`** ($p=0.0029$, `E` 우세), $I_2 = +0.091\%$ `[-0.229%, +0.412%]` (`stop`) | `results/topic2/2026-11-02_fu_b/verdict.json` (`stage1`, `stall_sensitivity`, `r1_pairing`) |
| **`FU_C` Stage-1 본분석 (신규 8 시드 `10..17`, `df=7`)** | **시험 NMSE**:<br>`E`: `0.988422` (정체 0)<br>`C`: `0.989538` (`C_s16 = 1.000001` 정체)<br>`S`: `0.989637` (`S_s15 = 1.000001` 정체) | **`-0.113%`** (`-0.001132`, SE `0.001630`)<br>**95% $t$-CI: `[-0.499%, +0.272%]`** (`[-0.004985, +0.002721]`) | **`+0.008%`** (`+8.29e-05`, SE `0.002234`)<br>**95% $t$-CI: `[-0.520%, +0.537%]`** (`[-0.005200, +0.005366]`) | **계층 부트스트랩**: $I_1$ `[-0.450%, +0.143%]`, $I_2$ `[-0.422%, +0.437%]`<br>**비정체 6시드(`df=5`)**: $I_1 = +0.040\%$ `[-0.213%, +0.293%]`, $I_2 = +0.022\%$ `[-0.091%, +0.135%]`<br>**통합 13시드(`df=12`)**: $I_1 = -0.013\%$ `[-0.248%, +0.222%]`, $I_2 = +0.187\%$ `[-0.163%, +0.538%]` | `results/topic2/2026-11-02_fu_c/verdict.json` (`stage1`, `secondary`) |
| **`FU_D` 합성 게이트 (`E192_d22182`, 시드 0)** | **$F^+$ 시험 NMSE**:<br>`E`: `0.655849`<br>`C`: `0.653468`<br>`S`: `0.657774` | **$F^+$ $C$ vs $E$**: **`+0.3631%`** (`+0.003631 < 0.01`, **`fail`**) | **$F^+$ $C$ vs $S$**: **`+0.6546%`** (`+0.006546 < 0.01`, **`fail`**) | 스모크 `511`: r1 `hcp_E_s0` 재채점 오차 `0.0` (`0.990871`); `E192` 1실행 예상 소요 `1.213 h` | `results/topic2/2026-11-02_fu_d/verdict.json` (`decision.fplus_gate`)<br>`results/topic2/2026-11-02_fu_d/smoke/{equiv,run}.json` |
| **`FU_E` 하류 개인식별력 ($N=24$ 홀드아웃, `cov2`, 5 시드 `df=4`)** | **$I_{\text{diff}}$ (Top-1 정확도)**:<br>`E`: `61.07` (`0.592`)<br>`C`: `65.42` (`0.713`)<br>`S`: `56.92` (`0.512`)<br>원시 `cellfc`: `64.13` (`1.000`) | **$J_1 = (C-E)/E$**: **`+8.11%`** (`+0.081053`, SE `0.052977`)<br>**95% $t$-CI: `[-6.60%, +22.81%]`** (`[-0.066034, +0.228140]`) | **$J_2 = (C-S)/S$**: **`+15.00%`** (`+0.150047`, SE `0.018759`)<br>**95% $t$-CI: `[+9.80%, +20.21%]`** (`[+0.097963, +0.202131]`) | **합성 $F^+$**: 시드 평균 `E 16.02, C 22.71, S 16.48`이나 `S_s2 = 5.76 <= p95(10.59)`로 **실패**<br>**시드 2 제외(`df=3`)**: $J_1 = +8.93\%$ `[-12.57%, +30.43%]`, $J_2 = +16.29\%$ `[+10.68%, +21.90%]`<br>**무작위 초기화 쌍둥이**: `E 53.82, C 54.16, S 54.45` (Top-1 `0.996`), init $J_1 = +0.66\%$ `[-0.28%, +1.59%]` | `results/topic2/2026-11-02_fu_e/verdict.json` (`gates`, `primary`, `descriptive`) |

### 3.6 5인 검증 게이트 및 독립 승리 감사 상태 (`M3` 및 `FU-A`~`FU-E`)
- **`M3` (`r3`)**: 5인 검증 게이트 전원 통과 후 `victory_M3_r3`(`.agents/teamwork/tw-20261031-four-topics/victory_M3_r3/handoff.md`)가 **`VERIFIED_COMPLETE`** 판정 (`tests/topic2_rgpool` **116 passed**, 기존 스위트 **86 passed**, r2 변이 `102/102` + 데이터 변이 `7/7` + r3 신규 변이 `22/23` + 승리 감사 변이 `38/40` 사살 [생존 `W09, X18` 수학적 동치 증명]).
- **`FU_A` (`r1`)**: 1차 시도에서 5인 게이트 및 `victory_FU_A_r1`(`victory_FU_A_r1/handoff.md`) **`VERIFIED_COMPLETE`** (`tests/topic2_fu_a` **69 passed, 1 skipped**, 작업자 변이 `31/31` 사살, 승리 감사 변이 `25/26` 사살).
- **`FU_B` (`r1`)**: 보고서 §2.3(`train_loss_last100` 14개 행) 및 §1.1 참조 행 반올림을 원본 `run.json` 수치로 교정하고 `output_sha256.txt`(`50/50 OK`)를 갱신한 뒤 5인 게이트 전원 통과 및 `victory_FU_B_r1`(`victory_FU_B_r1/handoff.md`) **`VERIFIED_COMPLETE`** (`tests/topic2_fu_b` **128 passed**, 변이 `44/44` 전수 사살, B300 원격 체크포인트 39/39 바이트 일치).
- **`FU_C` (`r3`)**: C4 테스트 리터럴 퇴역·봉인 및 r3 가드 추가 후 5인 게이트 전원 통과 및 `victory_FU_C_r3`(`victory_FU_C_r3/handoff.md`) **`VERIFIED_COMPLETE`** (`tests/topic2_fu_c` **210 passed**, 작업자 변이 `217/221` 사살[4개 동치], 승리 감사 변이 `12/12` 사살, B300 48/48 파일 해시 일치).
- **`FU_D` (`r3`)**: `B1`(Step-7 정체 민감도 분기 및 스크립트 배선)과 `B2`(비정규 디렉터리 별칭 덮어쓰기 정오표 `E5`) 해결 후 5인 게이트 전원 통과 및 `victory_FU_D_r3`(`victory_FU_D_r3/handoff.md`, `verification/victory_FU_D_r3/verify_victory_fu_d.out.json`) **`VERIFIED_COMPLETE`** (`tests/topic2_fu_d` **389 passed**, 3,000개 오라클 시나리오 통과, 통합 변이 `1,675`개 중 `1,511`개 사살·`164`개 동치/불변 증명·출력을 바꾸는 `515/515`개 변이 100% 사살).
- **`FU_E` (`r1`)**: 1차 시도에서 5인 게이트 및 `victory_FU_E_r1`(`victory_FU_E_r1/handoff.md`) **`VERIFIED_COMPLETE`** (`tests/topic2_fu_e` **71 passed**, 작업자/승리 변이 검증 및 Slurm `570` 독립 GPU 재실행에서 $|\Delta R| \le 0.0031$ 확인).

### 3.7 일탈 사항 및 부록(Addenda) 정오표
1. **`M3` 부록 01–06 (`docs/03_empirical_analysis/topic2/2026-11-01_topic2_addendum_01.md` ~ `2026-11-02_topic2_addendum_06.md`)**:
   - 부록 02–03: 카드 §9의 Stage-0 대표 지표(`r` 대 `pca2` 부호 반대) 및 Stage-1 결합 판독 규칙의 다의성을 명시하고 4가지 조합을 모두 병기.
   - 부록 04: `hcp_S_s2` 정체(`test_nmse = 1.000001`)에 대한 사후 시드-2 제외 민감도 분석(`I1 = +0.083%`, 여전히 `stop`) 기록.
   - 부록 05: 저장소 내 19개 파일의 `h00..h87` 위치 인덱스 비식별화 및 원본 오프레포 봉인, 그리고 $I_2$($C$ vs $S$)가 박스 공간 조밀도(`1.469` vs `1.557–1.674` 셀)와 교란되어 있음을 명시.
   - 부록 06 (`T2.4` 정오표 `E1–E5`): 동결된 `scripts/topic2_verdict.py`가 미도달 분기에서 카드 문언과 다른 점(`E1`: $F^+$ 실패 시 카드 §7.2는 `inconclusive`이나 스크립트는 Stage-1 미존재로 `no_verdict` 반환; `E2–E5`: 누락/중복 키 및 `assert` 처리)을 정오표로 기록하고, 실제 출하된 `verdict.json`은 해당 분기에 전혀 해당하지 않아 `card_reading(verdict.json) == "stop"`이 불변임을 증명.
2. **`FU-B` 부록 01 (`2026-11-02_topic2_fu_b_addendum_01.md`)**: 실행 시작 전(`ElapsedRaw = 0`) 카드 41행의 하이픈 영어 단어 하나가 BIDS 접두어 정규식과 충돌하여 `"not be optimal"`로 치환 후 `card_sha256_v2.txt`로 재동결.
3. **`FU-C` 부록 01–03 (`2026-11-02_topic2_fu_c_addendum_01.md` ~ `03.md`)**: r1 테스트 파일 내 6자리 리터럴을 봉인·퇴역시키고 대체 영수증 뷰(`scripts/topic2fu_c_verdict_r2.py`)로 `verdict.json`을 바이트 단위로 재현. 또한 결과 보고서 §2 항목 2의 정오표로, 정체된 `C_s16`을 제외하더라도 7시드 $I_1$ SD는 `0.220%`(반폭 `0.204%`)로서 r1의 5시드 표본이 시드 간 분산을 과소추정했음을 기록.
4. **`FU-D` 부록 01–02 (`2026-11-02_topic2_fu_d_addendum_01.md`, `02.md`)**: 동결 코드 수정 없이 미도달 분기 정오표 `E1–E9`(비정규 디렉터리 별칭 `E5`, 비유한/음수 항 `E2'`, `seed_plan` 순서 `E6`, 비-`keep` 상태의 `F-` 디렉터리 `E7`, 사이드카 코드 해시 `E8` 등) 및 문구 정오표 `W1–W5`, 그리고 대수적 보조정리 `P1`($n=5, k\in\{3,4\}$에서 Step 7이 `stop`을 `keep`/`modify`로 뒤집을 수 없음)을 증명.

### 3.8 미검증 항목 및 후속 연구 요구 조건
- **미검증 항목**: (1) `FU-A`(12 mm 셀-평균 타깃)와 `FU-D`(`E192` 스케일)는 각각의 합성 $F^+$ 측정 용량 게이트 미달(`+0.551%`, `+0.363% < 1.00%`)로 인해 실제 HCP Stage-1 학습이 수행되지 않았다. (2) `FU-E`에서 교차 세션(`REST1` 대 `REST2`) 지문 인식은 B300에 `REST1_LR`만 스테이징되어 있어 측정 불가(`untestable`)였고, 연령/성별 예측 프로브는 공개 행동 데이터에 매칭되는 홀드아웃 피험자가 $\le 7$명(AUC 표집 SD $\approx 0.09\text{–}0.10 \gg \delta=0.01$)이어서 카드 §10에서 사전 배제되었다. (3) 모든 Stage-1 실험은 동일한 $N=88$(시험군 $16$명) 분할과 팔분체-내부 `M0` 개입에 국한되며, $I_2$($C$ vs $S$)는 공간 조밀도 차이를 완전히 통제하지 못한다(공간 조밀도 통제 대조군 `G`는 Stage-0에서만 평가됨).
- **후속 연구 요구 조건 및 비용 추산**:
  - `FU-A` 후속(`2026-11-02_topic2_fu_a_result_report.md` §9): 12 mm 셀-평균 타깃에서 게이트 측정 용량을 확보하려면 4× 예산(`A'2`: 게이트 `3.4 GPU-h` + Stage-1 `25.5 GPU-h`) 또는 `E192` 스케일(`A'3`: 게이트 `2.5–2.7 GPU-h` + Stage-1 `18–20 GPU-h`) 결합이 필요하다.
  - `FU-D` 후속(`2026-11-02_topic2_fu_d_result_report.md` §5): `E192` $F^+$ 추가 시드 검증(`D-gate-seeds`: 시드 1, 2 6개 실행 $\approx 7.1\text{ GPU-h}$) 또는 중간 스케일 `E96`(`D-mid`: $\approx 11\text{–}12\text{ GPU-h}$) 탐색이 필요하며, `src/topic2_fu_d` 재사용 시 부록 02의 `E1–E9` 코드 패치를 동결 전에 선행해야 한다.
  - optimization 안정화: `E36`/`FU-B`/`FU-C`에서 관찰된 간헐적 초기 고원 정체(plateau stall: `M3` 1/15, `FU-B` 1/15, `FU-C` 2/24)를 제거하기 위한 워밍업·학습률 재설계 및 `G`(유클리드 탐욕 성장) 암의 Stage-1 포함이 요구된다.

---

## 4. Topic 3 (`M2` 및 `M2H2`): 층별 재규격화군(RG) 스펙트럼 흐름, 유효 차원(PR) 및 무작위 초기화(`H2`) 대조 실증 분석

### 4.1 연구 질문, 출처·추정량 실측(T3.1) 및 실험 설계
손운규 교수님이 제안한 제3주제는 심층 신경망의 층별 표현을 재규격화군(RG) 조악화(coarse-graining) 흐름으로 해석하고(Mehta & Schwab 2014; Martin & Mahoney 2019, *Nature Comms* 2021; Bae et al. 2026), SwiFT `E192` 및 뇌 파운데이션 모델(BrainLM, BrainJEPA, NeuroSTORM)의 층별 참여비(Participation Ratio, $\text{PR} = (\sum \lambda_i)^2 / \sum \lambda_i^2$)와 멱법칙 꼬리 지수 $\alpha$를 통해 표현 압축·붕괴를 진단하는 것이다.

#### 4.1.1 출처 및 추정량 결함 실측 (`T3.1`, `docs/03_empirical_analysis/topic3/2026-10-31_topic3_provenance.md`, `results/topic3/2026-10-31/t3_1_provenance_repro.json`)
- **과거 수치 불일치(`J1`: $\text{PR} \approx 1.00\text{–}1.07$ 대 $2.78\text{–}12.51$)의 원인 규명**:
  - `src/spectral_rg_flow_diagnostic.py:55-64`(`compute_participation_ratio`)는 **비중심화(uncentered)** 행렬 $X$에 직접 SVD를 수행하였다. 7개 풀링 행렬에서 열 평균 벡터 $\sqrt{n}\bar{x}$가 전체 프로베니우스 에너지 $\|X\|_F^2$의 **`96.45%`~`99.92%`**(`mean_vector_energy_fraction`: `L0` `0.9992`, `L1` `0.9973`, `L2` `0.9645`, `L3` `0.9832`, `BrainLM` `0.9985`, `BrainJEPA` `0.9721`, `NeuroSTORM` `0.9948`)를 차지하므로 제1특이값 $\sigma_1^2$이 지배하여 비중심화 PR이 `1.0014`~`1.0743`으로 붕괴한 것이다(추정량 아티팩트).
  - 반면 `src/empirical_connectome_ablation.py:143-159`는 열 중심화(`X_c = X - X.mean(axis=0)`) 후 공분산 고윳값으로 PR을 계산하여 `2.7773`~`12.5070`을 산출하였다(`report_reproduced = true`, `json_reproduced = true`).
- **SwiFT `layer_2` $\to$ `layer_3` 아키텍처 실측**:
  - 로컬 HEAD(`de132387…`)와 `connectome` 실제 추출 포크(`SwiFT_v2` 커밋 `cd87338`/`63367643`, `sha256 = 5bc444690490dbbed27b43382c0621b869b80bfa305232273c030b4798752d3b`; `docs/03_empirical_analysis/topic3/2026-11-02_topic3_addendum_07_h2_card.md` §11) 모두 Stage 3(`i_layer = 3`)에서 `downsample = None`이다.
  - `layer_0`($1280$ 토큰, $D=384$), `layer_1`($160$ 토큰, $D=768$), `layer_2`($160$ 토큰, $D=1536$)는 `PatchMergingV2`의 `Linear` 직후(비정규화)에서 후킹되는 반면, `layer_3`($160$ 토큰, $D=1536$)는 Stage-3 Swin 블록(주 모델 및 `HCP_N400`은 2개 블록 [`2-2-18-2`], 두 `deepE192` 모델은 4개 블록 [`2-2-42-4`])과 최종 `self.norm`(`LayerNorm(1536, eps=1e-5)`)을 거친 출력이다. 즉 **`layer_2`와 `layer_3` 사이에는 공간 토큰 병합(`PatchMerging`)이 전혀 없으며**, 최종 `LayerNorm` 유무의 교란을 제거하기 위해 토큰별 무파라미터 $\text{LN}_0(L2)$ 대조군(`A1b`, `H1a`)이 도입되었다.

#### 4.1.2 실험 설계 (`M2` 및 `M2H2`)
1. **Family A (피험자 수준, 로컬 풀링 행렬, 시드 `20261031`)**: 중심화 공분산 `pr_cov` 및 표준화 상관 `pr_corr`(열 $\text{SD} < 10^{-3}\times\text{median SD}$ 제거), LOO 잭나이프 SE, iid 가우시안 기준치 $\text{PR}_{\text{iid}}(n,D)$($B=200$), 열-순열 영모형($B=1000$, `D2`), SwiFT 내부 쌍대 부표본($m = \lfloor 57/2\rfloor = 28$, $S=2000$, 유한모집단 보정 $\text{SE} = \text{sd}(\Delta^{(s)})\sqrt{m/(n-m)}$, `A1`/`D1`), LN-정합 피험자 수준 대비 $L3 - \text{LN}_0(L2)$(`A1b`), NeuroSTORM 동일 25명 부분집합($n=25$, $m = \lfloor 25/2\rfloor = 12$, $S=2000$) 교차모델 비교(`A2`/`D3`).
2. **Family B (피험자 내 토큰 수준, `connectome` 원시 프레임, $N=57$, 4개 체크포인트)**: 주 체크포인트(`NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4`, `2-2-18-2`)와 3개 zoo 체크포인트(`HCP_N400_T2400_E192` [`2-2-18-2`], `NewUAH_deepE192_L1e-4` [`2-2-42-4`], `NewUAH_deepE192_L5e-5` [`2-2-42-4`])에서 피험자당 7개 프레임 연결($L0$: $8960$ 토큰, $L1/L2/\text{LN}_0(L2)/L3$: $1120$ 토큰) 및 160-토큰 부표본(`sub160`) 스펙트럼 추출. 일차 대비는 **`H1a`** = $\log\text{corrPR}(L3) - \log\text{corrPR}(\text{LN}_0(L2))$ 및 **`H1b`** = $\log\text{covPR}(L3) - \log\text{covPR}(L2)$ (양측 부호반전 순열검정 $B=9,999$, 피험자 부트스트랩 95% CI $B=9,999$, 체크포인트별 Holm 보정).
3. **Topic 3 H2 (`M2H2`, 무작위 초기화 대조군, PI 의사결정 제8항)**: `connectome`의 `/storage/bigdata/VRABES/03_MNI_to_TRs/ses-01` 동일 $57\times 7 = 399$개 윈도우에서 주 체크포인트 재추출 암(`R0`, Gate G 검증용)과 생성자 기본 초기화(`trunc_normal_(std=0.02)`)를 사용한 10개 무작위 시드(`R1..R10`, `seed_model(1..10)`)를 추출하여 학습 효과(trained minus random-init mean)를 **Family C**(`C1`: `H1a` DiD, `C2`: `H1b` DiD, `C3`: `D1` cov DiD, `C4`: `D1` corr DiD) 및 **Family L**(5개 층 변형 × `{cov, corr}` × `{token, subject}` = 20개 셀)에서 검정.

### 4.2 사전 동결 분석 카드 및 판정·기각 규칙 (`M2` 및 `M2H2`)
- **`M2` 동결 분석 카드**: `docs/03_empirical_analysis/topic3/2026-10-31_topic3_analysis_card.md` (`sha256 = 683374565d806454800a0d9ccfb2b49a7bb43d699f81ad86cb6090fb26d1b8e0`, 동결 시각 `2026-10-31T08:48:29Z`; 영수증 `results/topic3/2026-10-31/card_sha256.txt`, `code_sha256_at_freeze.txt`, `output_sha256.txt` [42개 항목]).
  - **`D1` ($L2 - L3$ 피험자 수준)**: $m=28$ 95% 구간 $\text{covPR lo}_{95} > 0$이고 $\text{corrPR lo}_{95} > 0$이면 `"drop robust and not a per-channel-scale effect"`.
  - **`D2` (독립 열 초과 구조)**: 열-순열 영모형 $p_{\text{low}} < 0.025$ ($B=1000$).
  - **`D3` (교차모델 순서)**: $n=25, m=12$에서 $\text{BrainJEPA} - \text{BrainLM}$과 $\text{NeuroSTORM} - \text{BrainLM}$ 모두 $\text{covPR lo}_{95} > 0$이면 `"ordering reproduces"`.
  - **`H1a` / `H1b` (토큰 수준 재현 규칙)**: 주 체크포인트에서 $p_{\text{Holm}} < 0.05$ 및 95% 부트스트랩 CI가 0을 배제하고, 동시에 3개 zoo 체크포인트 중 **$\ge 2$개**가 주 체크포인트와 **동일 부호**로 $p_{\text{Holm}} < 0.05$일 때만 `"holds"`(미충족 시 `"not replicated"` 또는 `"killed"`).
  - **$\alpha$ 추정량 편향 게이트**: 합성 멱법칙 스펙트럼($\alpha_{\text{true}} \in \{1.5, 2.0, 2.5, 3.0\}$)에서 $|\text{median}(\hat{\alpha}) - \alpha_{\text{true}}| \le 0.15$를 통과해야 하며, 미달 시 $\alpha$ 기반 체제 분류(`R4`)는 기각된다.
- **`M2H2` 동결 카드 (부록 07)**: `docs/03_empirical_analysis/topic3/2026-11-02_topic3_addendum_07_h2_card.md` (`sha256 = 09b45220205bce814c4e07d4494d586b95f63f97dbfcddeb716fafcdc5edd84b`, 동결 시각 `2026-11-01T15:57:40Z`; 영수증 `results/topic3/2026-11-02_h2/addendum_07_sha256.txt`, Gate 작업 `218063` 제출 `16:22:19Z` 및 무작위 초기화 작업 `218064` 제출 `16:32:19Z` 이전).
  - **Gate G (5대 사전 복제 관문)**: `G1`(399개 전 윈도우×4개 층 $\text{rel\_fro}\le 10^{-5}$, $\max|\Delta|\le 10^{-4}$), `G2`(.npz 해시·정렬·재풀링 `allclose` $10^{-5}$), `G3`($57\times 5\times 6$ 통계량 상대오차 $\le 10^{-6}$), `G4`(`best.pt` 해시 `5fd8a56c…`, 568 텐서, TF32 off), `G5`(3개 음성 대조군 `shift_plus1_frame`, `pad_value_0`, `input_scaling_none`이 모두 `G1` 실패) 전원 통과 시에만 무작위 초기화를 실행한다.
  - **4분류 판정 규칙 (`TE+`, `TE-`, `EQ`, `INC`)**:
    - Family C 임계치: $\delta_C = 0.5 \times |\text{pinned trained effect}|$ (`C1`: `0.011375`, `C2`: `0.022336`, `C3`: `2.671927`, `C4`: `3.019404`; `{C1, C2}`에 Holm 보정).
    - Family L 임계치: $\delta_L = \log(1.10) = 0.095310$ (토큰 10개 셀 Holm 보정).
    - **`TE+` (`keep`)**: $\text{lo}_{95} > \delta \land (p_{\text{Holm}}<0.05\text{ 또는 피험자 수준}) \land \min_s e_s > \delta$.
    - **`TE-` (`keep`)**: $\text{hi}_{95} < -\delta \land (p_{\text{Holm}}<0.05\text{ 또는 피험자 수준}) \land \max_s e_s < -\delta$.
    - **`EQ` (`stop`)**: $\text{lo}_{90} > -\delta \land \text{hi}_{90} < \delta \land \max_s |e_s| < \delta$.
    - **`INC` (`inconclusive`)**: 그 외 모든 경우.

### 4.3 데이터셋, 표본 구성 및 연산 자원
- **데이터**: 로컬 `/home/juke/git/VRABES/RemissionAnalysis/`의 7개 풀링 `.npz` 행렬($N=57$, NeuroSTORM은 $n=25$ 부분집합) 및 `connectome` 서버의 4개 SwiFT `E192` 체크포인트 토큰 덤프($57\text{명}\times 7\text{프레임}$)와 원시 입력 프레임(`/storage/bigdata/VRABES/03_MNI_to_TRs/ses-01`, $57\times 7 = 399$개 윈도우). 원시 프레임과 개별 피험자 표현은 `connectome` 외부로 반출되지 않았으며(C6), `57`개 실제 디렉터리 이름에 대한 C4 스캔에서 식별자 노출 `0`건이 확인되었다.
- **연산 자원** (`results/gpu_ledger_2026-10-31.md`):
  - **`M2` (r1–r4)**: **`0.000 GPU-h`** (로컬 CPU + `connectome` `node2` CPU Slurm 배열 작업 `217845_0..3` 각 `101–121 s`).
  - **`M2H2` (r1–r2 + 승리 감사)**: `connectome` `node1`(RTX A5000 24 GB 1기)에서 총 **`0.891 GPU-h`** 사용 (상한 `6.0 GPU-h`의 `14.85%`; 탐색 스모크 `218004, 218007, 218041` 합계 `0.058 GPU-h` + 본작업 Gate G `218063` `0.135 GPU-h` + 무작위 10시드 `218064` `0.323 GPU-h` + r1 검증자 재실행 `218065..218069` `0.303 GPU-h` + 승리 감사 `218072` 시드 5·10 비트일치 재현 `0.072 GPU-h`).

### 4.4 사전 등록 규칙에 따른 최종 판정 (`J1, R1–R7`, `Family A/B`, `H2`)

| 검증 항목 / 가설 | 사전 등록 규칙에 따른 최종 판정 | 판정 근거 요약 및 `H2`(무작위 초기화 대조) 결합 결론 | 정본 결과 파일 및 JSON 키 |
|---|---|---|---|
| **`J1`** (구 JSON $\text{PR} = 1.001\text{–}1.074$ "계급 붕괴") | **`FAILS` (`stop`)** | 열 평균 벡터($96.45\%\text{–}99.92\%$ 에너지)를 제거하지 않은 비중심화 SVD 아티팩트. 중심화 `pr_cov`는 `2.78–12.51`. | `results/topic3/2026-10-31/t3_1_provenance_repro.json` |
| **`R1`** (SwiFT $L0/L1 \to L2$ PR "4배 팽창") | **기술통계 전용 (`inconclusive`)** | $\Delta\text{PR}_{28}(L2-L1) = +4.67$ `[+2.96, +6.39]`(cov)이나 차원 $D$($768\to 1536$) 교란 및 $L1$ 단일 이상치(LOO 시 `2.78 -> 6.39`)가 존재. `H2`에서도 trained$-$init $\Delta_{28}(L2-L1)$이 `-1.61 [-3.77, +0.56]`(cov), `-0.74 [-3.18, +1.71]`(corr)로 0을 포함하여 학습 효과 여부가 미결정(부록 08 정오표 `E2`). | `results/topic3/2026-10-31/family_A_subject_level.json` (`A1_swift_pairs.L2_minus_L1`)<br>`results/topic3/2026-11-02_h2/r2/2026-11-02_topic3_h2_addendum_08_r2.md` (`E2`) |
| **`R2` 기전** ("유클리드 `PatchMerging`에 의한 $L2\to L3$ 붕괴") | **`FAILS` (`stop`)** | SwiFT ver11 코드상 `layer_2`와 `layer_3` 사이에 `PatchMerging`이 존재하지 않음(`downsample = None`). | `docs/03_empirical_analysis/topic3/2026-10-31_topic3_provenance.md` |
| **`R2` 피험자 수준 (`D1` / `A1b` 및 `H2` `C3, C4`)** | **`D1` HOLDS (`keep`)**<br>**`C3, C4` = `TE+` (`keep`)** | 피험자 수준 $\Delta\text{PR}_{28}(L2-L3) = +5.34$ `[+3.22, +7.46]`(cov), $+6.04$ `[+4.28, +7.80]`(corr) 및 LN-정합 `A1b` $-6.08$ `[-7.98, -4.18]`(corr)로 강건함. **`H2` 결과**: 무작위 초기화에서는 감소폭이 $+0.26$/$+0.25$에 불과하여 학습 효과 `C3 = +5.09 [+2.93, +7.25]`(`TE+`), `C4 = +5.79 [+4.01, +7.57]`(`TE+`)가 입증됨(단, 생성자 기본 초기화 기준이며 `C3`는 $\delta \le 0.548\times|\text{trained}|$에서 유지; 부록 08 `E1, E6`). | `results/topic3/2026-10-31/family_A_subject_level.json` (`verdicts.D1_verdict`)<br>`results/topic3/2026-11-02_h2/h2_results.json` (`family_C.C3`, `family_C.C4`) |
| **`R2` 토큰 수준 (`H1a, H1b` 및 `H2` `C1, C2`)** | **`H1a` 역방향(`L3 higher`) HOLDS**<br>**`H1b` `not replicated`**<br>**`C1, C2` = `INC` (`inconclusive`)** | 토큰 수준에서는 붕괴가 아니라 반대로 `L3 > LN0(L2)`(`H1a` 주 모델 $+2.3\%$, deepE192 2개 $+3.9\%, +5.0\%$; 단 유일한 동깊이 `HCP_N400`은 $-12.8\%$)가 성립하며, 8개 정적 공간 셀이 분산의 $\ge 99.994\%$를 차지해 유효 상한이 $\le 7$임(부록 03 §1). **`H2` 결과**: `H1a`의 약 $45\%$($+1.03\%$ vs $+2.28\%$)가 무작위 초기화에 이미 존재하여 `C1`($+0.0124 [+0.0104, +0.0145]$ vs $\delta=0.0114$)과 `C2`($+0.0295$, 2개 시드 $\le \delta=0.0223$) 모두 **`INC`**로 판정됨. | `results/topic3/2026-10-31/family_B_token_level.json` (`replication`)<br>`results/topic3/2026-11-02_h2/h2_results.json` (`family_C.C1`, `family_C.C2`) |
| **`R3` 교차모델 비교 (`D3`)** | **순서(`D3`) HOLDS (`keep`)**<br>**원인 귀속 `UNTESTABLE` (`inconclusive`)** | 동일 $n=25, m=12$에서 `BrainJEPA - BrainLM` $= +2.08$ `[+0.77, +3.40]`, `NeuroSTORM - BrainLM` $= +3.36$ `[+1.72, +5.01]`(cov)로 순서가 재현되나($m=12$ 비율 $1.47\times, 1.77\times$; 전체 $n=25$ `covPR` `5.36 / 9.66 / 12.51`, 비율 $1.80\times, 2.34\times$), 풀링 방식(CLS 대 토큰평균 대 GAP)·차원 $D$·사전학습 데이터가 교란되어 자기지도 학습 방법론 차이로 귀속할 수 없음. | `results/topic3/2026-10-31/family_A_subject_level.json` (`verdicts.D3_ordering_reproduces`, `results.A2_matched25`, `results.A2_pairs`) |
| **`R4`** (멱법칙 $\alpha$ 기반 체제 진단) | **`NOT SUPPORTED` (`stop`)** | HTSR 이론은 가중치 행렬 $W$에 적용되는 이론이며 $n=57$ 활성화 공분산 행렬에서는 $\alpha_{\text{rank}}$와 $\alpha_{\text{Clauset}}$ 모두 합성 보정 게이트(편향 $\le 0.15$)를 전 형상에서 실패함(`alpha_calibration_synthetic.json`). | `results/topic3/2026-10-31/alpha_calibration_synthetic.json` |
| **`R5`** (최적 OOD 층 = `L2`) / **`R6`** ($d_B, R_{\text{hub}}$) / **`R7`** (450-ROI) | **`R5` `UNTESTABLE`** / **`R6` `NOT SUPPORTED` (`stop`)** / **`R7` 비교 불가** | `R5`는 코드(`spectral_rg_flow_diagnostic.py:217-222`)에 하드코딩된 문자열이며 OOD 전이 데이터가 없음; `R6`는 비중심화 코사인 유사도(중앙값 $0.970\text{–}0.9995$) 그래프 아티팩트; `R7`은 행이 피험자가 아닌 450개 ROI 파셀임. | `docs/03_empirical_analysis/topic3/2026-10-31_topic3_result_report.md` (§1, §5) |

### 4.5 핵심 실증 수치 및 신뢰구간 (`M2` 및 `M2H2`)

#### 표 4.5a: Family A 피험자 수준 전체 표본 스펙트럼 및 쌍대 부표본 대비 (`results/topic3/2026-10-31/family_A_subject_level.json`)

| 행렬 / 대비 | 형상 ($n\times D$ 또는 $m$) | 중심화 `pr_cov` (Jackknife SE) | 표준화 `pr_corr` (SE) | $\text{PR}_{\text{iid}}(n, D)$ 평균 (`pr_cov / PR_iid`) | 95% 구간 `[lo, hi]` 또는 영모형 $p_{\text{low}}$ | 정본 JSON 키 및 정오표 반영 |
|---|---|---|---|---|---|---|
| **`L0`** (SwiFT Stage 0) | $57 \times 384$ | `2.777344` (`0.276257`) | `4.791938` | `48.769399` (`0.056948`) | 열-순열 영모형 평균 `45.43` (`q025 = 44.77`), $p_{\text{low}} = 0.000999$ (`D2: true`) | `results.E1_full.L0` |
| **`L1`** (SwiFT Stage 1) | $57 \times 768$ | `2.778188` (`3.576676`*) | `5.235213` | `52.135146` (`0.053288`) | 열-순열 영모형 평균 `50.07` (`q025 = 49.30`), $p_{\text{low}} = 0.000999$ (*단일 이상치 제거 시 `pr_cov = 6.3898` [`6.39`], SE `0.1488` [`0.149`]) | `results.E1_full.L1`<br>`2026-10-31_topic3_addendum_03.md` (§3) |
| **`L2`** (SwiFT Stage 2) | $57 \times 1536$ | `11.020186` (`1.295550`) | `13.187853` | `53.995679` (`0.204094`) | 열-순열 영모형 평균 `53.76` (`q025 = 53.61`), $p_{\text{low}} = 0.000999$ (`D2: true`) | `results.E1_full.L2` |
| **`L3`** (SwiFT Stage 3 + LN) | $57 \times 1536$ | `3.578647` (`0.285604`) | `4.779337` | `53.992891` (`0.066280`) | 열-순열 영모형 평균 `53.21` (`q025 = 52.97`), $p_{\text{low}} = 0.000999$ (`D2: true`) | `results.E1_full.L3` |
| **`BrainLM`** / **`BrainJEPA`** / **`NeuroSTORM`** (전체 $n$) | $57\times 768$ / $57\times 768$ / $25\times 288$ | `4.318772` / `11.785055` / `12.507023` | `6.513417` / `13.929926` / `13.980857` | 비율: `0.0828` / `0.2261` / `0.5662` | 3개 모델 모두 $p_{\text{low}} = 0.000999 < 0.025$ (`D2: true`) | `results.E1_full.{BrainLM,BrainJEPA,NeuroSTORM}` |
| **`D1`: $\Delta\text{PR}_{28}(L2 - L3)$** | $m=28, S=2000$ | **`+5.343855`** (`1.081055`) | **`+6.038809`** (`0.899083`) | — | cov: **`[+3.224986, +7.462723]` (`[+3.22, +7.46]`**, 부록 03 §5 정오표 반영)<br>corr: **`[+4.276607, +7.801011]` (`[+4.28, +7.80]`)** | `results.A1_swift_pairs.L2_minus_L3` |
| **`R1`: $\Delta\text{PR}_{28}(L2 - L1)$** / **$L1 - L0$** | $m=28, S=2000$ | `L2-L1`: `+4.672146` (`0.875055`)<br>`L1-L0`: `+1.241349` (`1.755698`) | `L2-L1`: `+4.387901` (`1.295447`)<br>`L1-L0`: `+1.587189` (`1.918358`) | — | `L2-L1` cov `[+2.957, +6.387]`, corr `[+1.849, +6.927]`<br>`L1-L0` cov `[-2.200, +4.683]`, corr `[-2.173, +5.347]` | `results.A1_swift_pairs.{L2_minus_L1,L1_minus_L0}` |
| **`D3`: 교차모델 $n=25, m=12$ 대비** | $m=12, S=2000$ | `JEPA-LM`: **`+2.083916`** (`0.671449`)<br>`STORM-LM`: **`+3.362626`** (`0.839386`) | `JEPA-LM`: **`+1.726812`** (`0.564809`)<br>`STORM-LM`: **`+2.723041`** (`0.649202`) | $m=12$ `covPR`: `LM` `4.40` (`4.395`), `JEPA` `6.48` (`6.479`), `STORM` `7.76` (`7.758`) | `JEPA-LM` cov **`[+0.767877, +3.399956]`**, corr `[+0.620, +2.834]`<br>`STORM-LM` cov **`[+1.717431, +5.007822]`**, corr `[+1.451, +3.995]` | `results.A2_matched25`, `results.A2_pairs` |

#### 표 4.5b: Family B 토큰 수준(`H1a`, `H1b`) 및 LN-정합 피험자 수준(`A1b`) 4개 체크포인트 결과 (`results/topic3/2026-10-31/family_B_token_level.json`)

| 체크포인트 (깊이) | `A1b` 피험자 수준 $\Delta\text{corrPR}_{28}(L3-\text{LN}_0(L2))$ [95% CI] | `H1a` 토큰 수준 $\log\text{corrPR}(L3/\text{LN}_0(L2))$ [95% 부트스트랩 CI] ($p_{\text{Holm}}$) | `H1b` 토큰 수준 $\log\text{covPR}(L3/L2)$ [95% 부트스트랩 CI] ($p_{\text{Holm}}$) | 토큰 `cat_corrpr` 중앙값 (`L0 / L1 / L2 / LN0L2 / L3`) | 정본 JSON 키 및 정오표 반영 |
|---|---|---|---|---|---|
| **`E192_primary`** (`2-2-18-2`) | **`-6.077532`**<br>`[-7.977351, -4.177713]` | **`+0.022751`** (`×1.0230`)<br>**`[+0.020722, +0.024776]`** (`0.0002`) | **`+0.044673`** (`×1.0457`)<br>**`[+0.040775, +0.048499]`** (`0.0002`) | `4.75 / 5.15 / 5.88 / 5.99 / 6.14`<br>(`cat_covpr`: `2.36 / 3.23 / 5.41 / 5.54 / 5.67`) | `A1b_ln_matched_subject_level.E192_primary`<br>`per_checkpoint.E192_primary.primary` |
| **`zoo_HCP_N400_T2400_E192`** (`2-2-18-2`) | **`-7.636432`**<br>`[-8.554125, -6.718739]` | **`-0.136753`** (`×0.8722`, 역부호)<br>**`[-0.141094, -0.132341]`** (`0.0002`) | **`-0.112961`** (`×0.8932`, 역부호)<br>**`[-0.120388, -0.105174]`** (`0.0002`) | 동깊이 독립 사전학습에서는 토큰 PR이 감소함 (`57/57`명 음수) | `per_checkpoint.zoo_HCP_N400_T2400_E192` |
| **`zoo_NewUAH_deepE192_L1e-4`** (`2-2-42-4`) | **`-1.358313`**<br>`[-2.184348, -0.532279]` | **`+0.037809`** (`×1.0385`, 동부호)<br>**`[+0.027529, +0.046756]`** (`0.0002`) | **`-0.032966`** (`×0.9676`, 역부호)<br>**`[-0.048461, -0.019624]`** (`0.0002`) | `H1a` 동부호(1/2), `H1b` 역부호 | `per_checkpoint.zoo_NewUAH_deepE192_L1e-4` |
| **`zoo_NewUAH_deepE192_L5e-5`** (`2-2-42-4`) | **`-3.284892`** (**`-3.28`**, 부록 03 §5 정오표)<br>`[-4.089687, -2.480098]` | **`+0.048867`** (`×1.0501`, 동부호)<br>**`[+0.042912, +0.054822]`** (`0.0002`) | **`+0.079215`** (`×1.0824`, 동부호)<br>**`[+0.071592, +0.086636]`** (`0.0002`) | `H1a` 동부호(2/2 $\to$ `holds`), `H1b` 동부호(1/3 $\to$ `not replicated`) | `A1b_ln_matched_subject_level.zoo_NewUAH_deepE192_L5e-5`<br>`per_checkpoint.zoo_NewUAH_deepE192_L5e-5` |

#### 표 4.5c: Topic 3 `H2` (`M2H2`) 무작위 초기화 대조 실험 핵심 결과 (`results/topic3/2026-11-02_h2/h2_results.json`, `gate/gate_decision.json`)
- **Gate G 복제 검증 (`gate_decision.json`)**: `gate_verdict = "PASS"` (`G1` 399개 윈도우 최대 상대 오차 $\le 7.8\times 10^{-7}$, `G2` 57명 재풀링 일치, `G3` 1,710개 스칼라 상대오차 $\le 7.3\times 10^{-8}$, `G4` `best.pt` 568 텐서 일치, `G5` 3개 음성 대조군 모두 정상 기각).
- **Family C (층간 대비의 학습 효과 DiD = 학습 $T$ $-$ 무작위 10시드 평균)**:

| 엔드포인트 | 학습 모델 값 (`trained_mean`) | 무작위 10시드 평균 (`random_mean`) | 학습 효과 DiD (`point`) | 95% CI (`ci95`) / 90% CI (`ci90`) | 임계치 $\delta$ ($0.5\|\text{trained}\|$) | 10개 시드별 효과 범위 ($\min_s e_s \sim \max_s e_s$) | $p_{\text{Holm}}$ | 최종 판정 (`label` / `G8`) | 정본 키 (`h2_results.json`) |
|---|---|---|---|---|---|---|---|---|---|
| **`C1` (`H1a` 토큰 DiD)** | `+0.022751` | `+0.010301` | **`+0.012449`** | **`[+0.010379, +0.014476]`**<br>(`90%`: `[+0.010700, +0.014139]`) | `0.011375` | `+0.003583 ~ +0.023149` (4개 시드 $\le \delta$) | `0.0002` | **`INC` (`inconclusive`)**<br>(`interval reaches +-delta`) | `family_C.C1` |
| **`C2` (`H1b` 토큰 DiD)** | `+0.044673` | `+0.015141` | **`+0.029531`** | **`[+0.025616, +0.033409]`**<br>(`90%`: `[+0.026192, +0.032790]`) | `0.022336` | `+0.020461 ~ +0.049652` (시드 3, 8이 $\le \delta$) | `0.0002` | **`INC` (`inconclusive`)**<br>(`a seed effect <= delta`) | `family_C.C2` |
| **`C3` (`D1` 피험자 cov DiD)** | `+5.343855` | `+0.255370` | **`+5.088484`** (SE `1.101134`) | **`[+2.930262, +7.246707]`**<br>(`90%`: `[+3.277119, +6.899850]`) | `2.671927` | `+4.926507 ~ +5.285145` (10개 전 시드 $> \delta$) | `null` (피험자 수준) | **`TE+` (`keep`)**<br>($f \le 0.5483$에서 유지; 부록 08 `E1`) | `family_C.C3` |
| **`C4` (`D1` 피험자 corr DiD)** | `+6.038809` | `+0.251823` | **`+5.786985`** (SE `0.908123`) | **`[+4.007065, +7.566906]`**<br>(`90%`: `[+4.293123, +7.280847]`) | `3.019404` | `+5.537227 ~ +5.936608` (10개 전 시드 $> \delta$) | `null` (피험자 수준) | **`TE+` (`keep`)**<br>($f \le 0.6636$에서 유지; 부록 08 `E1`) | `family_C.C4` |

- **Family L (층별 PR 수준의 학습 효과, $\delta_L = \log(1.10) = 0.095310$, `h2_results.json::family_L` 및 `E1_per_arm`)**:
  - **피험자 수준 (`family_L.subject`)**: 무작위 초기화(`R1..R10`)의 전체 표본($n=57$) 중심화 `pr_cov`는 `L1`에서 **`17.61–20.87`** (`17.6128–20.8686`), `L2`에서 **`31.93–34.02` (`31.9–34.0`)**, `L3`에서 **`30.95–33.12` (`31.0–33.1`; `L2/L3` 합산 `31.0–34.0`**, H2 보고서 §3의 `30.9` 오타를 `victory_M2H2_r2` 정오표에 따라 `31.0`으로 교정)인 반면, 재추출 학습 모델(`R0`, 부록 08 `E4`)은 `L1 = 2.7782`, `L2 = 11.0202`, `L3 = 3.5786`이다. 따라서 $m=28$ 로그비 $\log(\text{PR}_T / \text{PR}_R)$에서 **`L1_cov`(`-1.424 [-2.441, -0.407]`), `L1_corr`(`-1.049 [-1.829, -0.269]`), `L2_cov`(`-0.869 [-1.185, -0.554]`), `L2_corr`(`-0.706 [-0.947, -0.465]`), `LN0L2_cov`(`-0.872 [-1.203, -0.541]`), `LN0L2_corr`(`-0.703 [-0.955, -0.451]`), `L3_cov`(`-1.839 [-2.087, -1.591]`), `L3_corr`(`-1.549 [-1.769, -1.328]`) 8개 셀 모두 `TE-` (`keep`, 학습에 의한 강한 차원 압축)**로 판정되었다. 반면 **`L0_cov`(`-0.061 [-0.330, +0.208]`)와 `L0_corr`(`-0.131 [-0.396, +0.134]`)는 90% 구간이 $\pm\delta_L$을 넘어 `INC`(미결정, 부록 08 `E3`)**이다.
  - **토큰 수준 (`family_L.token`, 10개 셀 = `2 TE-`, `4 EQ`, `4 INC`)**: **`L1_cov`(`-0.2770 [-0.2932, -0.2599]`, $p_{\text{Holm}}=0.001$)와 `L1_corr`(`-0.3055 [-0.3180, -0.2919]`, $p_{\text{Holm}}=0.001$) 2개 셀은 `TE-`**, **`L2_corr`(`-0.0745 [-0.0771, -0.0716]`), `LN0L2_corr`(`-0.0556 [-0.0582, -0.0529]`), `L3_cov`(`-0.0707 [-0.0743, -0.0670]`), `L3_corr`(`-0.0431 [-0.0456, -0.0406]`) 4개 셀은 `EQ` (`stop`, $\pm 10\%$ 이내 동등)**, 그리고 **`L0_cov`(`-0.0556 [-0.0634, -0.0465]`, $p_{\text{Holm}}=0.001$), `L0_corr`(`-0.0091 [-0.0161, -0.0013]`, $p_{\text{Holm}}=0.0149$), `L2_cov`(`-0.1002 [-0.1040, -0.0963]`, `ci95`는 $-\delta_L$ 너머이나 5개 시드 효과가 $\ge -\delta_L$), `LN0L2_cov`(`-0.0754 [-0.0791, -0.0717]`, 시드 최대 절대값 `0.1057` $\ge \delta_L$) 4개 셀은 시드별 일관성 조건 미충족으로 `INC`**이다.

### 4.6 5인 검증 게이트 및 독립 승리 감사 상태 (`M2` 및 `M2H2`)
- **`M2` (`r4`)**: PI 의사결정 제6항(`"범위 고정 마지막 1회"`: Family A 300개 리프 전체 출력 회귀 테스트, `token_job` 입력 검증 `T01/T02`, 주 종점 Holm 대 Bonferroni `N01`, `D1` corr-전용 분기 `VA01/VA02`)에 따라 `reviewer_M2_r4_1` (`APPROVE`), `auditor_M2_r4_1` (`CLEAN`) 게이트 통과 후 `victory_M2`(`.agents/teamwork/tw-20261031-four-topics/victory_M2/handoff.md`)가 **`VERIFIED_COMPLETE` (`VICTORY CONFIRMED`)** 판정 (`tests/topic3_spectral` **138 passed**, 기존 스위트 **86 passed**, Family A 300/300 리프 및 Family B 전 항목 상대오차 $\le 5.5\times 10^{-16}$ 독립 재현).
- **`M2H2` (`r2`)**: 부록 08(`results/topic3/2026-11-02_h2/r2/2026-11-02_topic3_h2_addendum_08_r2.md`) 및 97개 추가 테스트(`tests/topic3_h2` 총 **167 passed**)로 r1 검증자 지적 사항을 모두 종결한 뒤 r2 5인 검증 게이트 전원 통과 및 `victory_M2H2_r2`(`victory_M2H2_r2/handoff.md`) **`VERIFIED_COMPLETE` (`VICTORY CONFIRMED`)** 판정 (독립 SVD/부표본 재구현에서 24/24 라벨 일치 및 최대 상대오차 $8.3\times 10^{-16}$, `connectome` Slurm `218072`에서 시드 5·10 재실행 시 `.npz` 바이트 단위 완전 일치 확인).

### 4.7 일탈 사항 및 부록(Addenda) 정오표
1. **`M2` 부록 01–06 (`docs/03_empirical_analysis/topic3/2026-10-31_topic3_addendum.md` ~ `2026-11-01_topic3_addendum_06.md`)**:
   - 부록 01: `scripts/topic3_launch_connectome.py` 1개 파일의 동결 후 수정 고지.
   - 부록 02: 두 `deepE192` zoo 체크포인트의 깊이가 `2-2-18-2`가 아닌 `2-2-42-4`(Stage 3 블록 4개)임을 명시.
   - 부록 03: (i) $L2/L3$ 160개 토큰이 8개 정적 공간 셀 $\times$ 20 시간 프레임이어서 중심화 후 유효 계수가 $8-1=7$(상위 7개 고윳값이 분산의 $\ge 99.9942\%$ 차지)로 상한됨을 규명, (ii) $L1$ 잭나이프 SE(`3.58`)를 유발한 단일 이상치 피험자 분석, (iii) 결과 보고서 §2의 반올림 오기 2건(`D1` cov 하한 `+3.23 -> +3.22`, `deepE192 L5e-5` `A1b` `-3.29 -> -3.28`) 교정.
   - 부록 04–06: 변이 테스트 가드 확장(`test_verdict_rules_r2b.py`, `test_verdict_rules_r3.py`, `test_token_stats_wiring_r3.py`, `test_token_level_r4.py`, `test_regression_r4.py`, 총 138개 테스트) 및 잔여 등가/비차단 변이(`U127, VX04, VX06`) 문서화.
2. **`M2H2` 부록 08 정오표 `E1–E8` 및 승리 감사 정오표 (`results/topic3/2026-11-02_h2/r2/2026-11-02_topic3_h2_addendum_08_r2.md` §5, `victory_M2H2_r2/handoff.md`)**:
   - `E1`: $\delta$ 경계에 가장 가까운 항목은 `C1`($f\in[0.1575, 1.0175)$에서 `INC` 불변)이 아니라 **`C3` ($f \le 0.5483$에서만 `TE+` 유지, 여유폭 약 10%)**임.
   - `E2`: `R1`($L2-L1$)의 trained$-$init 차이(`-1.61 [-3.77, +0.56]` cov)는 0을 포함하므로 학습 효과 부재로 단정할 수 없고 기술통계(`inconclusive`)로 유지됨.
   - `E3`: `L0` 피험자 수준은 `EQ`가 아니라 **`INC`**임.
   - `E4`: H2 보고서 §3/§4의 학습군 전체-$n$ `pr_cov` 및 토큰 $\alpha$ 중앙값은 `R0`(재추출 학습 모델)에서 산출된 값임.
   - `E6`: `C3/C4`의 학습 효과(`TE+`)는 추출 생성자 기본 초기화(`trunc_normal_(std=0.02)`) 대비 결론임.
   - `E8`: 단일 시드($K=1$) 대비 시 `C3/C4`는 10개 시드 개별적으로도 모두 `TE+`이나, `C1`은 시드별 `EQ`(3개)·`TE+`(4개)·`INC`(3개)로 갈림.
   - 승리 감사 반올림 교정: 무작위 초기화 `L2/L3` 전체-$n$ `pr_cov` 최소값은 `R5/L3 = 30.9530`이므로 `30.9–34.0`이 아닌 **`31.0–34.0`**임.

### 4.8 미검증 항목 및 후속 연구 요구 조건
- **미검증 항목**: (1) `R3` 교차모델 차원 차이의 원인 귀속(동일 코호트·동일 풀링·동일 차원 $D$에서 대조 학습 대 마스크 재구성 직접 비교 미수행), (2) `R5` 실제 하류 과제 OOD 일반화 성능과 층별 PR 간의 상관, (3) 3개 zoo 체크포인트(`HCP_N400`, `deepE192`) 및 타 파운데이션 모델(BrainLM, BrainJEPA, NeuroSTORM)에 대한 무작위 초기화(`H2`) 대조군, (4) 생성자 기본 초기화가 아닌 실제 사전학습 시작 시점 초기화 분포(또는 가중치 셔플 영모형)에서의 `H2` 비교.
- **후속 연구 요구 조건**: (1) `C3`의 $\delta = 0.5\times|\text{trained}|$ 임계치는 작업자가 부록 07에서 사전 동결하고 부록 08 §5 `E1` 민감도 경계($f \le 0.5483$)와 함께 보고하여 PI가 최종 추인 완료(2026-11-02, PI 의사결정 제9항; 부록 08 §8)하였으며, 추가적인 임계치 기준은 사후 민감도로만 해석해야 한다. (2) 토큰 수준에서 시간 차원이 붕괴($\le 5.8\times 10^{-5}$ 분산)된 원인이 시공간 패치 임베딩 구조인지 학습 손실 함수인지 규명하기 위해 프레임 내 시간 변동을 보존하는 대조 실험이 필요하다.

---

## 5. Topic 4 (`M4`): 역전파 없는 국소 시냅스 학습(Masked-Lateral PSP Similarity Matching) 실증 분석

### 5.1 연구 질문, 과거 포화 버그 규명(T4.1) 및 실험 설계
손운규 교수님이 제안한 제4주제는 신경 유사도 매칭(Neural Similarity Matching / Principal Subspace Projection, PSP; Pehlevan, Sengupta & Chklovskii, *Neural Computation* 2015, 2018) 및 순환 시냅스 가소성(ReSU; Chklovskii et al. 2026, arXiv:2512.23146) 원리에 기반하여, 역전파(backpropagation) 없이 오직 국소 헤비안/반헤비안 규칙과 희소 측방 억제(lateral inhibition) 마스크만으로 4D 뇌 시계열 예측 표현을 학습할 때 Mode II 허브-반발 프랙탈 측방 연결(`C4`)이 무작위 연결(`C1`)이나 Mode I 부자 클럽(`C3`)보다 우월한지 검증하는 것이다.

#### 5.1.1 과거 $R^2 = 1.0$ 포화 현상의 원인 규명 (`T4.1`, `docs/03_empirical_analysis/topic4/2026-11-01_topic4_T41_diagnosis.md`, `results/topic4/2026-11-01/t41_counterfactual.json`)
- **근본 원인(`D1–D3`)**: 과거 벤치마크(`empirical_results.json`)에서 `C0`~`C5` 전 조건이 동일하게 예측 $R^2 = 1.0$과 비중심화 $\text{PR} \approx 1.005$를 기록한 이유는 다음과 같다:
  1. **`D1` (후단 0-패딩 구간에서의 시험 평가)**: 과거 코드는 전체 코호트 중 오직 단일 피험자(`position 0`, Amsterdam-VUmc, 원시 $\text{TR}=1.8\text{ s}$, 유효 시점 `197`개 $\to$ 선두 20샘플 절단 후 유효 길이 `177`, VMD 캐시에서 길이 `464`로 0-패딩됨)만 평가하면서 시점 `324`에서 `70/30` 분할을 수행하였다. 그 결과 **시험 구간 139개 행(`325..463`) 전부가 0으로 채워진 후단 패딩 영역(`test_target_rows_inside_valid_portion = 0`, `ss_tot_test = 2.517e-45`)에 위치**하여 분모 언더플로 가드(`1.0 - 0.0 = 1.0`)가 상수 $1.0$을 반환하였다.
  2. **`D2` (IMF1 협대역 과평활화)**: 유효 길이가 464를 채우는 피험자(`position 932`)에서도 VMD IMF1 협대역 신호는 지속성 기준선($\hat{X}_{t+1}=X_t$)만으로 $R^2 = 0.9916$에 달해 위상 변별력이 없다.
  3. **`D3` (학습 규칙 결함 및 시험 데이터 유출)**: 측방 가중치 업데이트 $dM$에서 $-M$ 감쇠항이 누락되었고 신경 좌표하강(neural coordinate descent) 없이 단일 스텝만 수행했으며, 리지 회귀 판독기를 시험 데이터 타깃에 직접 재적합하였다.
- **재설계 및 명칭 정립 (`D4`, 카드 §4)**: Chklovskii et al.(2026)의 ReSU는 배치 CCA 목적함수로서 측방 억제 행렬 $M$을 포함하지 않으므로, 피드포워드 행렬 $W$(헤비안)와 대칭 양정치 측방 억제 행렬 $M$(반헤비안, 대각 성분 $D = \text{diag}(M)$, 안정적인 감쇠 정점 반복 $Z = Z_{\text{prev}}(I - \tau D^{-1}(M - D)) + \tau X W D^{-1}$)을 갖는 본 엔진을 **Masked-Lateral PSP Similarity Matching**(`src/topic4_resu/psp_engine.py`, 카드 문서상 별칭 `src/topic4_local_learning`)으로 명명하고 `autograd` 역전파 부재를 단위 테스트로 강제하였다.

#### 5.1.2 실험 설계 (`2026-11-01_topic4_analysis_card.md` §1–§6)
- **과제 및 모델 구조**: $d=48$개 ROI(304개 ROI 중 등간격 `np.linspace(0, 303, 48, dtype=int)`)의 광대역($\text{TR}=2.0\text{ s}$) 시계열에서 $k=24$ 은닉 유닛으로 1-스텝(2.0 s) 앞선 미래($\hat{X}_{t+1} = Z_t W_{\text{out}} + b$, 폴드 내 `inner_train`에서 학습하고 `inner_val`에서 $\lambda\in\{10^{-2},10^{-1},1,10,100\}$을 선택한 공통 리지 판독기)를 예측할 때의 피험자별 가드된 시험 $R^2$($S_c(s)$)를 비교한다.
- **7개 국소 PSP 위상 조건 ($k=24$, 간선 수 25% 밀도 = $69/276$개로 통제)**:
  - `C0`: 비연결 영모형 (0개 측방 간선, 모든 유닛이 제1주성분으로 수렴).
  - `C1`: Erdős–Rényi 무작위 그래프 (69개 간선, 폴드당 30개 그래프 인스턴스).
  - `C2`: Watts–Strogatz 소세계 그래프 ($k_{\text{ring}}=6, p=0.2$, 69개 간선으로 절단, 폴드당 30개 인스턴스).
  - `C3`: **Mode I Rich Club** (6개 허브 `{0..5}` 완전 클리크[15개 허브-허브 간선] + 54개 허브-주변부 간선 = 69개 간선, 폴드당 10개 초기화 시드).
  - `C4`: **Mode II Hub-Repelling Fractal** (6노드 모듈 4개, 모듈당 차수 7인 허브 1개 `{0,6,12,18}`, **허브-허브 간선 0개**, 69개 간선, 폴드당 30개 인스턴스).
  - `C4DP`: `C4`의 차수 분포($[7\times 4, 5\times 20]$, 69개 간선)를 정확히 보존하면서 1,000회 이중 간선 교환으로 허브 반발만 파괴한 대조군 (폴드당 30개 인스턴스).
  - `C5`: 완전 연결 밀집 그래프 ($K_{24}$, 276개 간선, 폴드당 10개 시드; 무제약 PSP 부분공간).
- **비-PSP 기준선**: `constant`(훈련 평균), `persistence`($\hat{X}_{t+1}=X_t$), `identity`(48차원 리지 상한), `pca24`(상위 24-PCA), `rrr24`(계수-24 축소계수회귀 선형 병목 이론적 상한), `randlin24`(비학습 가우시안 $48\times 24$ 투영), `randrelu24`(비학습 ReLU), `mlpenc`(역전파로 학습된 $48\to 24\to\text{ReLU}\to 48$ MLP의 24차원 인코더 + 동일 공통 리지 판독기), `mlp_e2e`(역전파 MLP 직접 출력).

### 5.2 사전 동결 분석 카드 및 판정·기각 규칙
- **동결 분석 카드**: `docs/03_empirical_analysis/topic4/2026-11-01_topic4_analysis_card.md` (`sha256 = 2b535c3978094bee65e95938ff9d1f93beb440309297265bc278f5cb60695934`, 동결 시각 `2026-11-01T02:04:41Z`; 튜닝 시작 `02:04:52Z` 및 확증 시작 `02:07:43Z` 이전; 영수증 `results/topic4/2026-11-01/card_sha256.txt`, `code_sha256_at_freeze.txt` [36개 파일], `split_manifest_sha256.txt`, `output_sha256.txt`).
- **최소 실용 효과크기($\delta$) 및 추론 방법**: $\delta = 0.01$ 절대 $R^2$(선형 상한 $\approx 0.14$의 약 7%; PI 의사결정 제3항으로 확정). 확증 표본($n=1,014$)을 기관 층화 복원추출하고 각 조건 내 그래프/초기화 인스턴스를 독립 복원추출하는 **교차 백분위 부트스트랩**($B=2,000$, 시드 `20261101`)을 사용한다.
- **일차 및 이차 판정 규칙 (카드 §5–§6)**:
  - **일차 가설 `H1` ($\Delta_1 = S_{\text{C4}} - S_{\text{C1}}$, 95% CI)**: $\text{CI}_{\text{lo}} > 0 \land \Delta_1 \ge 0.01 \land \text{S1.CI}_{\text{lo}} > 0 \implies$ `keep`; $\text{CI}_{\text{lo}} > 0 \land \Delta_1 \ge 0.01 \land \text{S1.CI}_{\text{lo}} \le 0 \implies$ `modify`; **$\text{CI}_{\text{hi}} < 0.01 \implies$ `stop` (killed)**; 그 외 `inconclusive`.
  - **이차 대비 (3개 대비 Bonferroni 보정 98.33% CI)**:
    - **`S1` ($S_{\text{C4}} - S_{\text{C4DP}}$)** 및 **`S2` ($S_{\text{C5}} - S_{\text{randlin24}}$)**: $\text{CI}_{\text{lo}} > 0 \land \text{point} \ge 0.01 \implies$ `supported`; $\text{CI}_{\text{hi}} < 0.01 \implies$ `killed`; 그 외 `inconclusive`.
    - **`S3` ($S_{\text{C5}} - S_{\text{MLPenc}}$)**: $\text{CI}_{\text{lo}} > -0.01 \implies$ `non-inferior`; $\text{CI}_{\text{hi}} < -0.01 \implies$ `inferior`; 그 외 `inconclusive`.
  - **실행 무결성 규칙 (카드 §4, §6)**: 200 미니배치마다 및 최종 6,000 스텝에서 $\rho(I - D^{-1}M) < 1$, $\lambda_{\min}(M) > 0$, 유한성을 점검하여 불안정 실행 비율이 **$> 10\%$**인 클래스가 포함된 모든 대비는 자동으로 **`"inconclusive (execution integrity)"`**로 판정한다.

### 5.3 데이터셋, 표본 구성 및 연산 자원
- **데이터 및 분할** (`results/topic4/2026-11-01/split_manifest.json`, `sha256 = 3e56210f…0436`):
  - 디스크 내 1,706명 중 원시 $\text{TR} = 2.0\text{ s}$ 정확 일치 및 후단 패딩 제거·선두 20샘플(40 s) 절단 후 유효 길이 $\text{valid\_T} \ge 100$ 샘플(200 s)을 만족하는 **13개 기관 `N = 1,195`명**(유효 시점 합계 `191,209`개, 중앙값 `133` 샘플; 탐색 단계에서 소진된 13명[`positions 0..11, 932`]은 모두 $\text{TR}\ne 2.0\text{ s}$이어서 일차 모집단과 중첩 `0`명).
  - **튜닝 세트(기관별 15%, 시드 `20261101`)**: **`181`명** (`tune_train = 145`, `tune_val = 36`). 튜닝 게이트 `G-a`~`G-d` 전원 통과(`identity` $R^2 = 0.1455 < 0.9$, `persistence` $R^2 = -0.3085 < 0.9$, $\eta_0 = 0.02$에서 21/21 안정; `results/topic4/2026-11-01/tuning.json`).
  - **확증 세트(기관별 85%, 5-겹 기관 층화 교차적합)**: **`1,014`명** (튜닝 세트와 중첩 `0`명; 폴드 0~4 시험 피험자 수 `207, 206, 204, 201, 196`명; 총 55개 확증 과업 `n_ok = 55`).
- **연산 자원**: GPU **`0.000 GPU-h`** (`results/gpu_ledger_2026-10-31.md`). 로컬 DGX-Spark CPU(4 워커, `OMP_NUM_THREADS=2`)에서 합성 자격검증 `205.04 s`, 튜닝 `15.32 s`, 5-겹 확증 실행 `397.9 s`(`6.63 min`) 소요.

### 5.4 사전 등록 규칙에 따른 최종 판정 (`M4`)
*정본 출처*: `results/topic4/2026-11-01/verdict.json` (`sha256 = 437161ed8f44ce3ccc6f65ccf2e654ebdc6c6187ebccf32de9377737f5185c22`)
1. **일차 가설 `H1` (`C4 - C1`)**: **`"stop"` (killed)**. $\Delta_1 = -0.002231$, 95% CI $[-0.004125, -0.000424]$로서 상한($-0.000424$)이 $\delta = 0.01$ 미만일 뿐 아니라 $0$보다도 작다. 즉 25% 희소 측방 억제 하에서 Mode II 허브-반발 프랙탈 위상(`C4`)은 동밀도 무작위 그래프(`C1`)보다 예측 $R^2$가 오히려 소폭 낮다.
2. **이차 가설 `S1` (`C4 - C4DP`)**: **`"killed"`**. $\Delta_{\text{S1}} = -0.001597$, 98.33% CI $[-0.003837, +0.000526]$로서 상한이 $\delta = 0.01$ 미만이다.
3. **이차 가설 `S2` (`C5 - randlin24`)**: **`"supported"`**. $\Delta_{\text{S2}} = +0.030616$, 98.33% CI $[+0.028799, +0.032419]$로서 하한이 $0$보다 크고 점추정치가 $\delta = 0.01$ 이상이다(국소 시냅스 가소성이 비학습 무작위 투영 대비 $+0.0306$ $R^2$ 향상 제공).
4. **이차 가설 `S3` (`C5 - MLPenc`)**: **`"non-inferior"`** (사전 등록 마진 $\delta = 0.01$ 기준). $\Delta_{\text{S3}} = -0.004669$, 98.33% CI $[-0.005025, -0.004258]$로서 하한($-0.005025$)이 $-\delta = -0.01$보다 크므로 비열등성 기준을 통과한다(동시에 상한이 $0$ 미만이므로 역전파 `MLPenc`가 $+0.0047$만큼 통계적으로 유의하게 높으며, 밀집 국소 PSP `C5`[$0.1369$]는 24-주성분 PCA `pca24`[$0.1370$]와 동등한 선형 부분공간에 수렴한다).
5. **실행 무결성 (`C3` Mode I Rich Club)**: `C0, C1, C2, C4, C4DP, C5`는 불안정 실행이 `0%`(`0/50` 또는 `0/150`)였으나, **`C3`는 `10/50`개 실행(`20.0% > 10%` 임계치)에서 $\rho(I - D^{-1}M) \ge 1$ 불안정이 발생**하여 `C3` 관련 대비는 사전 등록 규칙에 따라 **`"inconclusive (execution integrity)"`**로 판정되었다.

### 5.5 핵심 실증 수치 및 신뢰구간 (`M4`)

#### 표 5.5a: 일차·이차 대비 및 민감도 분석 (`results/topic4/2026-11-01/verdict.json`, $N_{\text{confirm}} = 1,014$)

| 대비 / 민감도 항목 | 점추정치 ($\Delta R^2$) | 부트스트랩 신뢰구간 (`[lo, hi]`) | 신뢰수준 (`level`) | 무결성 (`integrity_ok`) | 최종 판정 (`verdict`) | 정본 JSON 키 (`verdict.json`) |
|---|---|---|---|---|---|---|
| **일차 `H1`: `C4 - C1` ($h=1$ [2 s], 교차 부트스트랩)** | **`-0.002231`** (`-0.0022`) | **`[-0.004125, -0.000424]`** | `0.95` | `true` | **`stop` (killed)** | `H1_C4_minus_C1` |
| **이차 `S1`: `C4 - C4DP` (배치 효과 vs 차수분포)** | **`-0.001597`** (`-0.0016`) | **`[-0.003837, +0.000526]`** | `0.9833` | `true` | **`killed`** | `S1_C4_minus_C4DP` |
| **이차 `S2`: `C5 - randlin24` (국소 가소성 이득)** | **`+0.030616`** (`+0.0306`) | **`[+0.028799, +0.032419]`** | `0.9833` | `true` | **`supported`** | `S2_C5_minus_randomlinear24` |
| **이차 `S3`: `C5 - MLPenc` (국소 PSP vs 역전파 MLP)** | **`-0.004669`** (`-0.0047`) | **`[-0.005025, -0.004258]`** | `0.9833` | `true` | **`non-inferior`** ($\delta=0.01$) | `S3_C5_minus_MLPenc` |
| **민감도 1: 피험자 단독 부트스트랩 (`H1`)** | `-0.002231` | `[-0.002343, -0.002122]` | `0.95` | `true` | `stop` 유지 | `sensitivity.H1_subject_only_bootstrap` |
| **민감도 2: 기관 군집 부트스트랩 (`H1`, 13개 기관)** | `-0.002231` | `[-0.002768, -0.001658]` | `0.95` | `true` | `stop` 유지 | `sensitivity.H1_site_cluster_bootstrap` |
| **민감도 3: 2-스텝 예측 지평 ($h=2$ [4 s], `C4 - C1`)** | `-0.000611` | `[-0.001126, -0.000126]` | `0.95` | `true` | `stop` 유지 | `sensitivity.H1_horizon_4s` |
| **민감도 4: 지속성 대비 예측 스킬 점수 (`C4 - C1`)** | `-0.002003` | `[-0.003678, -0.000417]` | `0.95` | `true` | `stop` 유지 | `sensitivity.H1_skill_vs_persistence` |

#### 표 5.5b: 전체 조건별 확증 시험 성능 및 스펙트럼·그래프 불변량 (`results/topic4/2026-11-01/verdict.json` → `descriptive`, `execution_integrity`)

| 조건 / 모델 (`k=24` 또는 기준선) | 불안정 실행 (`n_unstable / n_runs`) | $h=1$ (2 s) 시험 $R^2$ 평균 [95% CI] | $h=2$ (4 s) 시험 $R^2$ 평균 | 시험 표현 중심화 PR (`centred_pr_test_mean`) | 전달 행렬 평균 계수 (`rank_F_mean`) | 독립집합 수 $\alpha(G)$ (`independence_number`) | 최대 반복 스펙트럼 반경 (`max_rho_iter`) |
|---|---|---|---|---|---|---|---|
| **`constant`** (훈련 평균 기준선) | — | `-0.000050` `[-0.000052, -0.000049]` | `-0.000132` | — | — | — | — |
| **`persistence`** ($\hat{X}_{t+1}=X_t$) | — | `-0.286230` `[-0.297145, -0.275622]` | `-0.655695` | — | — | — | — |
| **`identity`** (48-ROI 전체 리지 상한) | — | **`0.152511`** `[0.148358, 0.156537]` | `0.040316` | — | — | — | — |
| **`rrr24`** (계수-24 선형 병목 상한) | — | **`0.142465`** `[0.138727, 0.146167]` | `0.038962` | — | — | — | — |
| **`mlpenc`** (역전파 MLP-24 + 공통 리지) | — | **`0.141527`** `[0.137832, 0.145187]` | `0.038904` | — | — | — | — |
| **`mlp_e2e`** (역전파 MLP-24 종단간 출력) | — | **`0.140428`** `[0.136719, 0.144100]` | — | — | — | — | — |
| **`pca24`** (상위 24-주성분 PCA) | — | **`0.136961`** `[0.133340, 0.140573]` | `0.037930` | — | — | — | — |
| **`psp_C5`** (밀집 $K_{24}$, 276 간선 국소 PSP) | `0 / 50` (`0.0%`) | **`0.136858`** `[0.133229, 0.140466]` | `0.037908` | `13.989705` | `24.000` | `[1]` | `0.933677` |
| **`psp_C3`** (Mode I Rich Club, 69 간선)* | **`10 / 50` (`20.0%`)* | `0.107733`* `[0.104899, 0.110650]` | `0.031914`* | `1.294864`* | `8.000`* | `[17]` | `0.956472`* |
| **`randlin24`** (비학습 선형 무작위 투영) | — | **`0.106242`** `[0.103231, 0.109254]` | `0.029338` | — | — | — | — |
| **`psp_C1`** (Erdős–Rényi 무작위, 69 간선) | `0 / 150` (`0.0%`) | **`0.092453`** `[0.090014, 0.094940]` | `0.027960` | `2.604554` | `4.900` | `[8, 9, 10, 11]` | `0.859018` |
| **`psp_C2`** (Watts–Strogatz 소세계, 69 간선) | `0 / 150` (`0.0%`) | **`0.092292`** `[0.089840, 0.094782]` | `0.027927` | `3.004049` | `4.887` | `[7, 8, 9]` | `0.835931` |
| **`psp_C4DP`** (차수보존 재배선 `C4`, 69 간선) | `0 / 150` (`0.0%`) | **`0.091820`** `[0.089361, 0.094313]` | `0.027790` | `2.641901` | `4.833` | `[8, 9, 10]` | `0.825802` |
| **`psp_C4`** (Mode II 허브-반발 프랙탈, 69 간선) | `0 / 150` (`0.0%`) | **`0.090222`** `[0.087832, 0.092699]` | `0.027349` | `2.805852` | `4.547` | `[8]` | `0.821183` |
| **`randrelu24`** (비학습 ReLU 무작위 특성) | — | `0.076958` `[0.074682, 0.079249]` | `0.021674` | — | — | — | — |
| **`psp_C0`** (비연결 영모형, 0 간선) | `0 / 50` (`0.0%`) | **`0.021686`** `[0.020356, 0.023120]` | `0.007021` | `1.000000` | `1.000` | `[24]` | `4.44e-16` |

*\*주: `psp_C3` 기술통계는 안정적으로 수렴한 40/50개 실행만의 평균이며, 20% 불안정 발생으로 인해 추론 판정에서는 `inconclusive (execution integrity)`로 분류된다. 구조적 메커니즘 측면에서, 희소 마스크 $A$ 하에서 측방 억제가 없는 독립집합(크기 $\alpha(G)$)의 유닛들은 모두 동일한 제1주성분 방향 $v_1$으로 중복 수렴하여 유효 전달 계수(`rank_F_mean`)를 잠식한다(130개 안정 희소 인스턴스에서 $\alpha(G)$와 $R^2$ 간 탐색적 Spearman $\rho = 0.2804$; `verdict.json::exploratory_spearman_r2_vs_independence_number`).*

### 5.6 5인 검증 게이트 및 독립 승리 감사 상태 (`M4`)
- **5인 검증 게이트 (`M4_r1`)**: `reviewer_M4_r1_1` (`APPROVE`), `reviewer_M4_r1_2` (`APPROVE`), `challenger_M4_r1_1` (`CONFIRMED`), `challenger_M4_r1_2` (`CONFIRMED`), `auditor_M4_r1_1` (`CLEAN`) 전원 1차 통과.
- **독립 승리 감사 (`victory_M4`)**: `.agents/teamwork/tw-20261031-four-topics/victory_M4/handoff.md` (`2026-11-01T03:38Z`)에서 **`VERIFIED_COMPLETE` (`VICTORY CONFIRMED`)** 판정.
  - 동결 코드 36개 파일 해시 `36/36 OK`, `PROTECTED_HASHES.txt` `67/67 OK`.
  - 독립 재실행(`verification/victory_M4/rerun/`): 튜닝 $\to$ 55개 확증 과업 $\to$ 통계 분석 전 과정을 별도 캐시에서 처음부터 재실행한 결과 **55/55개 `confirm/*.json` 및 `verdict.json`(`437161ed…5c22`)이 원본과 바이트 단위로 100% 일치**하였다.
  - 클린룸 독립 재구현(`recompute_victory.py`, 시드 `777`): `H1 = -0.00223 [-0.00412, -0.00043]`(`stop`), `S1` `killed`, `S2 = +0.0306`(`supported`), `S3 = -0.00467`(`non-inferior`), `C3` 실패율 `10/50 (20%)` 전 항목 동일 재현.

### 5.7 일탈 사항 및 부록(Addenda) 정오표
- **사전 등록 규칙 및 코드 불변성**: `M4`는 사전 동결된 카드(`2b535c39…5934`)와 동결 코드(`code_sha256_at_freeze.txt`, 36개 파일)로부터 확증 판정에 영향을 미치는 사후 코드 수정 없이 1차 실행에서 완결되었다. (용어 정립 `D4`—Chklovskii et al. 2026 ReSU와 Pehlevan et al. 2015/2018 PSP의 구분—는 동결 전 카드 §4와 `2026-11-01_topic4_T41_diagnosis.md`에 사전 반영되었다.)
- **부록 01 및 승리 감사 비차단 고지 사항 (`docs/03_empirical_analysis/topic4/2026-11-01_topic4_addendum_01.md`, `victory_M4/handoff.md` Caveat 7)**: (1) 부록 01은 $h=2$(4 s) 예측 지평에서 개별 조건 평균 점추정치만 저장되고 조건별 개별 부트스트랩 구간은 생략된 점(`H1_horizon_4s` 차이 구간은 정상 산출) 및 `test_vendored_source_hashes_recorded`의 64자리 16진수 길이 검사가 동어반복적이었던 점을 투명하게 기록하였다. (2) `victory_M4` Caveat 7은 $\eta_0$ 튜닝 단계(`tuning.py`)에서 리지 판독기 평가 시 `refit_on_val=True`가 사용되었으나 모든 후보 $\eta_0$에 동일하게 적용되어 최적 $\eta_0 = 0.02$(`MLP` $\eta_0 = 10^{-3}$), 튜닝 게이트(`G-a`~`G-d`), 및 분리된 확증 세트($n=1,014$, `refit_on_val=False`) 판정에는 영향이 없음을 확인하였다.

### 5.8 미검증 항목 및 후속 연구 요구 조건
- **미검증 항목**: (1) `C3`(Mode I Rich Club)는 기본 학습률 $\eta_0 = 0.02$에서 20% 실행이 $\rho(I-D^{-1}M) \ge 1$로 발산하여 `C4` 대 `C3`의 직접 우열 비교가 `inconclusive (execution integrity)`로 남았다. (2) 선형 PSP 규칙의 이론적 특성상 완전 연결 `C5`조차 비지도 주성분 부분공간(`pca24`, $R^2=0.1370$)에 수렴하며 예측 관련 방향을 선택하는 지도/자기지도 축소계수회귀(`rrr24`, $R^2=0.1425$)나 역전파(`mlpenc`, $R^2=0.1415$)의 예측 특화 이득($+0.0047$)까지는 도달하지 못한다. (3) 전체 304-ROI 또는 복셀 수준, 그리고 비선형 정류(ON/OFF rectification) 결합 시의 거동은 평가되지 않았다.
- **후속 연구 요구 조건**:
  1. **이종 차수(heterogeneous-degree) 그래프를 위한 안정화 규칙**: `C3`의 6-허브 클리크에서 발생하는 야코비안 스펙트럼 반경 폭발을 막기 위해 노드 차수 $d_i$에 반비례하는 국소 학습률 스케일링($\eta_{M,ij} \propto 1/\sqrt{d_i d_j}$) 또는 대각 감쇠 보강을 사전 등록한 후 `C4` 대 `C3`를 재검정해야 한다.
  2. **독립집합 축퇴(degeneracy) 해소 및 과거-미래 교차공분산 결합**: 희소 그래프의 비연결 노드 쌍이 모두 제1주성분 $v_1$으로 중복 붕괴하는 현상을 막기 위해 2-홉 이상 간접 억제 또는 ReSU의 과거-미래 교차공분산 목적함수를 국소 3-인자(three-factor) 시냅스 규칙으로 변환하는 연구가 요구된다.

---

## 6. 전체 실행 연산 자원 원장(GPU Ledger) 및 거버넌스 감사 요약

### 6.1 마일스톤별 GPU 사용량 정산 (`results/gpu_ledger_2026-10-31.md`)
PI 의사결정 제7항으로 승인된 전체 실행 상한 **`95.000 GPU-h`**(초기 기본 상한 `64.000 GPU-h`) 대비 본 실행의 최종 누적 사용량은 **`59.300 GPU-h`**(기본 64 GPU-h 상한의 `92.66%`, 확장 95 GPU-h 상한의 `62.42%`)이다:

| 마일스톤 | 실행 클러스터 | 승인 상한 (GPU-h) | 작업자 (Worker) | 탐색자 (Explorer) | 검증자 / 승리 감사 | 합계 (GPU-h) | 정본 원장 및 영수증 경로 |
|---|---|---|---|---|---|---|---|
| **`M1` (Topic 1)** | DGX-Spark (CPU) | `0.0` | `0.000` | `0.000` | `0.000` | **`0.000`** | `results/topic1/2026-10-31/manifest.json` |
| **`M2` (Topic 3 r1–r4)** | DGX-Spark + `connectome` (CPU) | `0.0` | `0.000` | `0.000` | `0.000` | **`0.000`** | `results/topic3/2026-10-31/family_B_token_level.json` |
| **`M3` (Topic 2 r1–r3)** | B300 (`b300-01`) | `14.0` | `11.730` | `0.142` | `0.118` | **`11.990`** | `results/topic2/2026-11-01/gpu_hours_m3.txt`, `results/gpu_ledger_2026-10-31.md` |
| **`FU_A` (Topic 2 후속 A)** | B300 (`b300-01` Slurm) | `8.0` | `0.822` | `0.130` | `0.000` | **`0.952`** | `results/topic2/2026-11-02_fu_a/gpu_hours_fu_a.txt` |
| **`FU_B` (Topic 2 후속 B)** | B300 (`b300-01` Slurm) | `33.0` | `30.580` | `0.140` | `0.000` | **`30.720`** | `docs/03_empirical_analysis/topic2/2026-11-02_topic2_fu_b_result_report.md` (§5.1) |
| **`FU_C` (Topic 2 후속 C)** | B300 (`b300-01` Slurm) | `13.0` | `10.422` | `0.262` | `0.013` | **`10.697`** | `verification/victory_FU_C_r3/sacct_fu_c.txt`, `results/gpu_ledger_2026-10-31.md` |
| **`FU_D` (Topic 2 후속 D)** | B300 (`b300-01` Slurm) | `25.0` | `3.575` | `0.097` | `0.048` | **`3.720`** | `verification/victory_FU_D_r3/verify_victory_fu_d.out.json` |
| **`FU_E` (Topic 2 후속 E)** | B300 (`b300-01` Slurm) | `1.5` | `0.282` | `0.015` | `0.033` | **`0.330`** | `results/topic2/2026-11-02_fu_e/run_524/sacct_524.txt` |
| **`M2H2` (Topic 3 H2)** | `connectome` (`node1` A5000 Slurm) | `6.0` | `0.458` | `0.058` | `0.375` | **`0.891`** | `results/topic3/2026-11-02_h2/r2/2026-11-02_topic3_h2_addendum_08_r2.md` (D4) |
| **`M4` (Topic 4)** | DGX-Spark (CPU) | `0.0` | `0.000` | `0.000` | `0.000` | **`0.000`** | `results/topic4/2026-11-01/run_ledger.jsonl` |
| **총계 (Grand Total)** | **B300 `58.409` + connectome `0.891`** | **`95.0` (`64.0`)** | **`57.869`** | **`0.844`** | **`0.587`** | **`59.300`** | `results/gpu_ledger_2026-10-31.md` |

### 6.2 무결성 및 거버넌스(C1–C8) 최종 검증 요약
- **C1 (보호 해시 불변성)**: `.agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt`의 67개 보호 파일 전수가 `LC_ALL=C sha256sum -c`에서 `67/67 OK` (`rc = 0`)를 유지하였다.
- **C2 (회귀 및 단위 테스트)**: 기존 86개 테스트 스위트(`STRICT_E2E=1`) **86 passed**, `tests/topic1_lagmotif` **88 passed**, `tests/topic2_rgpool` **116 passed**, `tests/topic2_fu_a` **69 passed (1 skipped)**, `tests/topic2_fu_b` **128 passed**, `tests/topic2_fu_c` **210 passed**, `tests/topic2_fu_d` **389 passed**, `tests/topic2_fu_e` **71 passed**, `tests/topic3_spectral` **138 passed**, `tests/topic3_h2` **167 passed**, `tests/topic4_resu` **67 passed** 전수 통과.
- **C3 (사전 동결 및 시간 순서)**: 10개 모든 마일스톤에서 분석 카드 해시 영수증이 실데이터 통계 산출 이전에 기록되었음이 파일 타임스탬프·Slurm `sacct` 기록·git 스냅샷 커밋으로 교차 입증되었다.
- **C4 (참가자 식별정보 비노출)**: 본 보고서 및 모든 정본 산출물에서 HCP 6자리 ID, BIDS 피험자 접두어, ENIGMA 원시 피험자 ID, 비염처리 콘텐츠 해시 노출이 `0`건임을 확인하였다.
