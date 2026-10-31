# Next-Session Handoff & Copy-Paste Continuation Prompts
**(Building Blocks + Renormalization Group + Backprop-Free Neuromorphic AI 4대 실증 연구 인계 문서)**

- **기준 일시**: 2026-10-30 19:08 KST
- **기준 워크스페이스**: `/home/juke/git/00IITP-AI` (연동 대상 레포: `enigma_ocd_mbbn`, `SwiFT_v2`, `SwiFT-LLM`, `SwiFT-LLM-isotok`, `VRABES`, `DIVER`, `paper-review/bae_spectral_arxiv_v1_20261020`, `iclr2027_structure_transfer_39525`)
- **검증 상태**: 독립 Victory Audit **PASS (`VICTORY CONFIRMED`)**, 전체 자동화 테스트 **86/86 통과** (`STRICT_E2E=1 PYTHONPATH=/home/juke/git/00IITP-AI python3 -m pytest tests/ -q`)

---

## 1. 현재까지 완료된 산출물 및 코드 인벤토리

### 1.1 핵심 문서 (`docs/`)
1. [`docs/01_foundations/structural_connectomes_and_local_learning.md`](file:///home/juke/git/00IITP-AI/docs/01_foundations/structural_connectomes_and_local_learning.md)
   - Milo et al. (2002/2004) 모티프·슈퍼패밀리($\vec{SP}$), Song et al. (2005/2006) Box-Covering 재규격화군($\mathcal{R}_{l_B}, d_B$) 및 허브 반발성($R_{\text{hub}} \ll 1$), Chklovskii et al. (2026 ReSU / NSM) 무역전파 국소 가소성, Buzsáki (2019) 내재 리듬 골격의 통합 수리물리 모노그래프.
2. [`docs/03_empirical_analysis/REFERENCE_PACKS_FOUR_TOPICS.md`](file:///home/juke/git/00IITP-AI/docs/03_empirical_analysis/REFERENCE_PACKS_FOUR_TOPICS.md)
   - 4대 실증 연구 주제별 핵심 수식 정의, 선행 연구 한계점, 구체적 가설 및 증명 경로.
3. [`docs/03_empirical_analysis/LOCAL_REPO_INTEGRATION_SPEC.md`](file:///home/juke/git/00IITP-AI/docs/03_empirical_analysis/LOCAL_REPO_INTEGRATION_SPEC.md)
   - 7개 로컬 대상 저장소의 실제 데이터 경로, 텐서 형상(`(B, C, D, H, W, T)` 등), 백본 클래스(`PatchMerging4D`, `SwinTransformer4D`, `ENIGMA_OCD_fMRI_timeseries` 등) 및 코드 장착 인터페이스 명세.
4. [`docs/03_empirical_analysis/LAB_SEMINAR_BRAINSTORMING_GUIDE.md`](file:///home/juke/git/00IITP-AI/docs/03_empirical_analysis/LAB_SEMINAR_BRAINSTORMING_GUIDE.md)
   - 연구실 선생님들과 세미나에서 바로 토의할 수 있는 4대 주제별 반증 기준(Wrong-If-X), 모델 붕괴 위험 요소(Failure Modes), 대조군 설계 및 확장 아젠다.
5. [`docs/03_empirical_analysis/EMPIRICAL_ANALYSIS_REPORT.md`](file:///home/juke/git/00IITP-AI/docs/03_empirical_analysis/EMPIRICAL_ANALYSIS_REPORT.md) & [`docs/03_empirical_analysis/empirical_results.json`](file:///home/juke/git/00IITP-AI/docs/03_empirical_analysis/empirical_results.json)
   - 연구실 실제 데이터(`ENIGMA-OCD`, `SwiFT-LLM`, `VRABES`, *C. elegans* connectome) 기반 4대 파일럿 실증 결과 및 직렬화 JSON.

### 1.2 실행 가능한 실증 연구 모듈 (`src/` & `tests/`)
- **Topic 1 (`ENIGMA-OCD` 방향성 모티프 $\vec{SP}$ & 다중대역 허브 반발 바이오마커)**:
  - [`src/mbbn_connectome_biomarker.py`](file:///home/juke/git/00IITP-AI/src/mbbn_connectome_biomarker.py)
- **Topic 2 (`a-SwiFT` / `SwiFT v3`용 PyTorch Connectome Box-Covering RG Pooling)**:
  - [`src/rg_box_pooling.py`](file:///home/juke/git/00IITP-AI/src/rg_box_pooling.py)
- **Topic 3 (뇌 파운데이션 모델 층별 RG 흐름 & Heavy-Tailed 스펙트럼 진단)**:
  - [`src/spectral_rg_flow_diagnostic.py`](file:///home/juke/git/00IITP-AI/src/spectral_rg_flow_diagnostic.py)
- **Topic 4 (뉴로모픽 칩을 위한 무역전파 Fractal-Motif ReSU `FM-ReSU`)**:
  - [`src/fractal_motif_resu.py`](file:///home/juke/git/00IITP-AI/src/fractal_motif_resu.py)
- **기초 토폴로지·국소학습 엔진 & 통합 러너**:
  - [`src/connectome_topology.py`](file:///home/juke/git/00IITP-AI/src/connectome_topology.py), [`src/local_learning_engine.py`](file:///home/juke/git/00IITP-AI/src/local_learning_engine.py), [`src/empirical_connectome_ablation.py`](file:///home/juke/git/00IITP-AI/src/empirical_connectome_ablation.py), [`src/run_all_empirical_experiments.py`](file:///home/juke/git/00IITP-AI/src/run_all_empirical_experiments.py)
- **자동화 테스트 스위트 (86/86 통과)**:
  - [`tests/test_empirical_four_topics.py`](file:///home/juke/git/00IITP-AI/tests/test_empirical_four_topics.py) (38 tests)
  - [`tests/test_pilot_connectome.py`](file:///home/juke/git/00IITP-AI/tests/test_pilot_connectome.py) (11 tests)
  - [`tests/e2e/test_pilot_simulation_e2e.py`](file:///home/juke/git/00IITP-AI/tests/e2e/test_pilot_simulation_e2e.py) (37 tests)

---

## 2. 새 세션 시작 시 즉시 상태 확인 명령어 (Quick Sanity Check)

```bash
cd /home/juke/git/00IITP-AI
STRICT_E2E=1 PYTHONPATH=/home/juke/git/00IITP-AI /home/juke/superclaude-env/bin/python3 -m pytest tests/ -q
```

---

## 3. 다른 세션에 복사해 붙여넣을 이어받기 프롬프트 (Copy-Paste Prompts)

### [프롬프트 A — 통합 마스터 세션용 (4대 실증 연구 전체 이어받기)]

```text
/home/juke/git/00IITP-AI 레포에서 진행 중인 "Building Blocks (Milo 2002/2004) + Renormalization Group (Song 2005/2006) + Backprop-Free Local Learning (Chklovskii 2026 ReSU)" 기반 4대 실증 연구를 이어서 진행한다.

먼저 아래 인수인계 및 핵심 문서를 읽고 현재 구현된 코드와 실측 결과를 파악해:
1. /home/juke/git/00IITP-AI/docs/03_empirical_analysis/NEXT_SESSION_HANDOFF_AND_PROMPTS.md
2. /home/juke/git/00IITP-AI/docs/03_empirical_analysis/EMPIRICAL_ANALYSIS_REPORT.md
3. /home/juke/git/00IITP-AI/docs/03_empirical_analysis/LOCAL_REPO_INTEGRATION_SPEC.md
4. /home/juke/git/00IITP-AI/docs/03_empirical_analysis/REFERENCE_PACKS_FOUR_TOPICS.md
5. /home/juke/git/00IITP-AI/docs/03_empirical_analysis/LAB_SEMINAR_BRAINSTORMING_GUIDE.md

핵심 실행 모듈(/home/juke/git/00IITP-AI/src/):
- Topic 1 (ENIGMA-OCD 방향성 모티프 SP & 4-Band VMD 허브 반발): src/mbbn_connectome_biomarker.py
- Topic 2 (SwiFT 차원 붕괴 해결용 PyTorch Connectome Box-Covering RG Pooling): src/rg_box_pooling.py
- Topic 3 (파운데이션 모델 층별 RG Flow & Heavy-Tailed Spectrum 진단): src/spectral_rg_flow_diagnostic.py
- Topic 4 (뉴로모픽 무역전파 Fractal-Motif ReSU): src/fractal_motif_resu.py
- 통합 러너 및 테스트: src/run_all_empirical_experiments.py, tests/test_empirical_four_topics.py

필수 준수 규칙:
1. 제안서(Grant Proposal) 양식이 아니라 실제 데이터와 코드를 연결해 학습을 돌리고 실험을 검증하는 실증 연구로만 진행할 것.
2. 무거운 GPU 학습/스윕은 반드시 1순위 연구실 서버(ssh connectome, Slurm 8xA5000) 및 DGX-1(ssh dgx1, 8xV100)에 먼저 배치하고 로컬 dgx-spark GPU는 최후 수단으로만 사용할 것.
3. 연구실 학생 및 연구원 호칭은 항상 "OO 선생님" + 존댓말을 사용할 것.
4. /home/juke/git/00IITP-AI 내 기존 미커밋 파일(그랜트아이디어.md, 아이디어.txt, docs/qa_prep_차지욱_20260309.md, HANDOFF.md, docs/05_meetings/)은 절대 수정하거나 삭제하지 말 것.

문서들을 읽고 테스트(86 passed) 상태를 확인한 뒤, 4대 실증 연구 중 본 실험 확장을 바로 시작할 준비가 되었음을 보고해.
```

---

### [프롬프트 B — 연구 1 전용 세션 (`ENIGMA-OCD` 1,706~2,095명 전수 코호트 본 실험)]

```text
/home/juke/git/00IITP-AI/src/mbbn_connectome_biomarker.py 와 /home/juke/git/00IITP-AI/docs/03_empirical_analysis/LOCAL_REPO_INTEGRATION_SPEC.md (§Topic 1)를 읽고, /home/juke/git/enigma_ocd_mbbn 의 실제 다기관 데이터를 대상으로 "연구 1: ENIGMA-OCD Directed Lag Motif (13-Triad SP) & 4-Band VMD Hub Repulsion 바이오마커" 전수 코호트 본 실험을 진행해.

수행할 작업:
1. /home/juke/git/enigma_ocd_mbbn/data/MBBN_data_304_ROIs_0.25/ 내 디스크에 존재하는 1,706명 전체 피험자 .npy 시계열과 /home/juke/git/enigma_ocd_mbbn/data/metadata/ENIGMA_QC_final_subject_list.csv (OCD==1 환자, OCD==2 정상 대조군), 그리고 UKB_imf1..4_comm_ROI_order_304.npy 를 병렬 로드하여 전수 피험자의 13차원 Triad Significance Profile (SP), CSTC 회로 3-Cycle/FFL 비율, 대역별 Hub Repulsion R_hub 피처 행렬을 추출 및 캐싱해.
2. 다기관 사이트 효과(Sample 컬럼)를 ComBat / 혼합효과 모형(LMM)으로 통제한 뒤, (a) OCD vs HC 진단 분류(Stratified 10-fold CV, 사이트 홀드아웃), (b) 약물 복용군(Medicated) vs 비복용군(Unmedicated) 하위집단 효과 크기(Cohen's d), (c) Y-BOCS 증상 심각도 회귀 예측력을 정적 Pearson 상관 베이스라인과 정량 비교해.
3. 추출된 전수 코호트 바이오마커 피처를 /home/juke/git/enigma_ocd_mbbn 의 MBBN 모델 입력/보조 손실과 결합하는 실험을 설계하고 실행해.
```

---

### [프롬프트 C — 연구 2 전용 세션 (`SwiFT_v2` / `SwiFT-LLM` 내 `ConnectomeRGBoxPooling` 장착 및 학습)]

```text
/home/juke/git/00IITP-AI/src/rg_box_pooling.py 와 /home/juke/git/00IITP-AI/docs/03_empirical_analysis/LOCAL_REPO_INTEGRATION_SPEC.md (§Topic 2)를 읽고, "연구 2: SwiFT 유클리드 PatchMerging 차원 붕괴 해결을 위한 Connectome Box-Covering RG Pooling (a-SwiFT)" 본 실험을 진행해.

수행할 작업:
1. /home/juke/git/SwiFT-LLM-isotok/data/neuroprior_aligned/aligned_resources.npz (schaefer_fp, tian_fp) 및 npe_mine.npz (450-ROI NeuroPrior 그래디언트)에서 Song et al. (2005) Greedy Box-Covering RG + Fiedler 스펙트럼 분할 기반의 다중 스케일 슈퍼노드 계층 트리(450 -> 112 -> 28 -> 7 및 304 -> 76 -> 19)를 생성해.
2. ConnectomeRGBoxPooling 레이어를 기존 Euclidean PatchMerging4D와 동일한 입출력 인터페이스로 구성하여, 실제 fMRI 시계열 학습 시 Layer 0 -> 1 -> 2 -> 3 진행에 따른 유효 차원(Participation Ratio PR), 공분산 멱법칙 스펙트럼 지수 왜곡(|Delta alpha|), 그리고 하류 과제(OCD 분류 / VRABES 관해 예측 / 성별·연령 예측) 성능을 Euclidean PatchMerging 대비 Ablation 실험으로 검증해. (무거운 GPU 학습은 ssh connectome 또는 ssh dgx1 에 배치할 것.)
```

---

### [프롬프트 D — 연구 3 전용 세션 (뇌 파운데이션 모델 층별 RG Flow & Heavy-Tailed Spectrum 진단)]

```text
/home/juke/git/00IITP-AI/src/spectral_rg_flow_diagnostic.py 와 /home/juke/git/00IITP-AI/docs/03_empirical_analysis/LOCAL_REPO_INTEGRATION_SPEC.md (§Topic 3), 그리고 배상윤 선생님의 스펙트럼 구조 연구 레포(/home/juke/git/paper-review/bae_spectral_arxiv_v1_20261020 및 /home/juke/git/iclr2027_structure_transfer_39525)를 읽고 "연구 3: 뇌·AI 파운데이션 모델의 층별 Renormalization Flow & Heavy-Tailed Spectrum 무감독 진단" 본 실험을 진행해.

수행할 작업:
1. /home/juke/git/VRABES/RemissionAnalysis/ 의 실제 파운데이션 모델 층별 임베딩(SwiFT E192 Layer 0~3, BrainLM, BrainJEPA, NeuroSTORM)과 /home/juke/git/SwiFT-LLM-isotok/data/neuroprior_aligned/npe_mine.npz, 그리고 /home/juke/git/DIVER 체크포인트에서 5대 물리 지표 퀸텟(스펙트럼 지수 alpha, 유효 차원 PR, 프랙탈 차원 d_B, 허브 결합비 R_hub, 차수 동류성 r)을 전수 측정해.
2. 레이블 없이 계산한 무감독 임계성 점수(alpha in [1.5, 2.0], 음의 동류성 r < 0, 높은 d_B)로 예측한 최적 전이 레이어(예: SwiFT Layer 2 vs 과압축된 Layer 3)가 실제 하류 임상 과제(VRABES 우울증 관해 예측, HCP/ENIGMA 사이트 간 전이)의 선형 프로빙 및 파인튜닝 성능 순위와 정확히 일치하는지 통계적으로 검증해.
```

---

### [프롬프트 E — 연구 4 전용 세션 (뉴로모픽 `FM-ReSU` 무역전파 시공간 학습 아키텍처)]

```text
/home/juke/git/00IITP-AI/src/fractal_motif_resu.py 와 /home/juke/git/00IITP-AI/docs/03_empirical_analysis/LOCAL_REPO_INTEGRATION_SPEC.md (§Topic 4)를 읽고, "연구 4: 뉴로모픽 칩을 위한 무역전파 Fractal-Motif ReSU (FM-ReSU) 신경망" 본 실험을 진행해.

수행할 작업:
1. 2D 뉴로모픽 칩의 희소 배선 예산(10%~25% 밀도) 하에서 6가지 측면 억제 커넥톰 위상(C0 Unconnected, C1 Erdos-Renyi, C2 Watts-Strogatz, C3 Mode I Rich-Club, C4 Mode II Bio-Fractal Hub-Repelling + Milo cFFL/iFFL 지연 뱅크, C5 Dense All-to-All) 및 해부학적 C. elegans 성체 vs 다우어(Dauer) 재배선 커넥톰을 비교해.
2. 실제 인간 다채널 뇌 신호(ENIGMA-OCD fMRI 및 DIVER iEEG/EEG 스트림) 입력에 대해 전역 역전파(Backprop/BPTT) 없이 순수 국소 Oja + 측면 반-헤비안 가소성만으로 온라인 학습을 수행하고, 표준 BPTT RNN/MLP 대비 (a) 수용장 직교성 및 유효 차원(PR), (b) 다중 스텝 미래 상태 예측 R^2, (c) 폭주 안정성 임계치(lambda_crit), (d) 시냅스 연산 에너지(SOPs 및 100시냅스당 PR 효율)를 벤치마킹해.
```
