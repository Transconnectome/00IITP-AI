---
marp: true
theme: cha-editorial
paginate: true
size: 16:9
html: true
header: "다중감각 통합 지능 과제 (RS-2026-25518389) · 1차년도 연구 1-4 서울대 차지욱 교수팀"
footer: "서울대학교 뇌인지과학과·심리학과 커넥톰 연구실 (Transconnectome Lab)"
style: |
  section {
    padding: 40px 44px 30px 44px !important;
    font-size: 15px !important;
  }
  header {
    top: 12px !important;
    left: 44px !important;
    right: 44px !important;
    font-size: 11px !important;
  }
  footer {
    bottom: 10px !important;
    left: 44px !important;
    font-size: 10.5px !important;
  }
  section::after {
    bottom: 10px !important;
    right: 44px !important;
    font-size: 10.5px !important;
  }
  .slide-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid #003380;
    padding-bottom: 6px;
    margin-bottom: 10px;
  }
  .slide-kicker {
    font-size: 12px;
    font-weight: 700;
    color: #0072B2;
    letter-spacing: 0.03em;
    margin-bottom: 2px;
  }
  .slide-title {
    font-size: 24px;
    font-weight: 700;
    color: #282945;
    line-height: 1.22;
    letter-spacing: -0.02em;
    margin: 0;
  }
  .slide-badge {
    background: #EDF6FC;
    border: 1px solid #56B4E9;
    color: #003380;
    font-size: 12px;
    font-weight: 700;
    padding: 5px 12px;
    border-radius: 4px;
    white-space: nowrap;
  }
  .lead-box {
    background: #EDF6FC;
    border-left: 4px solid #003380;
    padding: 9px 14px;
    font-size: 14.5px;
    line-height: 1.35;
    color: #282945;
    margin-bottom: 12px;
    border-radius: 0 4px 4px 0;
  }
  .grid-2col {
    display: grid;
    grid-template-columns: 1.05fr 1.15fr;
    gap: 14px;
    align-items: stretch;
    margin-bottom: 10px;
  }
  .panel {
    background: #FFFFFF;
    border: 1px solid #E5DDD0;
    border-radius: 6px;
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .panel-title {
    font-size: 14px;
    font-weight: 700;
    color: #003380;
    border-bottom: 1px solid #E5DDD0;
    padding-bottom: 5px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .panel-sub {
    font-size: 11px;
    font-weight: 500;
    color: #5A5A6E;
  }
  table.res-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5px !important;
    margin: 2px 0 8px 0 !important;
  }
  table.res-table th {
    background: #003380 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    padding: 6px 8px !important;
    font-size: 12px !important;
    border: none !important;
    text-align: left;
  }
  table.res-table td {
    padding: 6.5px 8px !important;
    border-bottom: 1px solid #E5DDD0 !important;
    color: #282945 !important;
    line-height: 1.3 !important;
    vertical-align: middle;
  }
  table.res-table tr.hi td {
    background: #FDEFE0 !important;
    font-weight: 700 !important;
    color: #282945 !important;
  }
  .win {
    color: #D55E00;
    font-weight: 700;
  }
  .sub-cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-top: 2px;
  }
  .sub-card {
    background: #EDF6FC;
    border: 1px solid #E5DDD0;
    border-radius: 4px;
    padding: 7px 10px;
    font-size: 12px;
    line-height: 1.36;
    color: #282945;
  }
  .sub-card strong {
    color: #003380;
  }
  .status-bar {
    background: #1E3A5F;
    color: #FFFFFF;
    border-radius: 5px;
    padding: 7px 14px;
    font-size: 12px;
    line-height: 1.4;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }
  .status-bar a {
    color: #F0E442 !important;
    text-decoration: underline;
    font-weight: 700;
  }
  .status-tag {
    display: inline-block;
    background: #D55E00;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 10.5px;
    padding: 1px 7px;
    border-radius: 3px;
    margin-right: 6px;
  }
  .status-tag.blue {
    background: #0072B2;
  }
---

<!-- Slide 1: PIMSM / PALM -->
<div class="slide-top">
  <div>
    <div class="slide-kicker">연구 1-4 (서울대 차지욱 교수팀) · 세부주제 1: 뇌 물리법칙 기반 인공지능</div>
    <h1 class="slide-title">뇌 고유 리듬 이식 물리 정보 기반 뇌 동역학 모델 (PALM / 구 PIMSM)</h1>
  </div>
  <div class="slide-badge">담당: 배상윤 연구원 (서울대)</div>
</div>

<div class="lead-box">
  <strong>핵심 요약:</strong> 기존 AI(단순 숫자열 학습 → 짧은 촬영 시 붕괴) &nbsp;➔&nbsp; <strong>뇌 주파수 꺾임점(무릎 주파수)에서 고유 기억 시간척도 추출·고정</strong> &nbsp;➔&nbsp; <strong>단축 촬영·1% 데이터에서도 고성능 유지</strong>
</div>

<div class="grid-2col">
  <div class="panel">
    <div class="panel-title">
      <span>핵심 개념도: 뇌 주파수 물리법칙 이식 상태공간모델</span>
      <span class="panel-sub">약어 풀어쓰기 포함</span>
    </div>
    <img src="figures/s01_concept.svg" style="width:100%; height:auto;" alt="PALM 개념도" />
  </div>
  <div class="panel">
    <div class="panel-title">
      <span>주요 정량 성과: 4대 분포 변화(Shift) 성능 비교</span>
      <span class="panel-sub">인간 커넥톰 프로젝트(HCP) 1,086명</span>
    </div>
    <table class="res-table">
      <thead>
        <tr>
          <th>평가 과제 (임상·센서 제약)</th>
          <th>기존 최신 모델</th>
          <th>제안 모델 (PALM, 598만)</th>
          <th>개선 폭</th>
        </tr>
      </thead>
      <tbody>
        <tr class="hi">
          <td><strong>① 단축 촬영</strong> (1.44초, 2시점 관측)</td>
          <td>91.4% (표현유사도 0.73)</td>
          <td><span class="win">93.3% (표현유사도 0.81)</span></td>
          <td>표현 일관성 <strong>+10.8%</strong></td>
        </tr>
        <tr class="hi">
          <td><strong>② 소수 라벨 전이</strong> (1% 라벨 학습)</td>
          <td>Mamba2 75.2%</td>
          <td><span class="win">정확도 79.7% (±4.0%)</span></td>
          <td>정확도 <strong>+4.5%p</strong></td>
        </tr>
        <tr>
          <td><strong>③ 뇌 상태 교차</strong> (휴지기 → 운동)</td>
          <td>Mamba2 59.1%</td>
          <td><span class="win">정확도 63.2% (±1.3%)</span></td>
          <td>정확도 <strong>+4.1%p</strong></td>
        </tr>
        <tr>
          <td><strong>④ 미관측 센서 외삽</strong> (기상 5천 곳)</td>
          <td>기초모델 오차(MSE) 0.40</td>
          <td><span class="win">전 구간 1위 (오차 0.35)</span></td>
          <td>예측 오차 <strong>-15.2%</strong></td>
        </tr>
      </tbody>
    </table>
    <div class="sub-cards">
      <div class="sub-card">
        <strong>선행 1 (다중주파수 기초모델, MBBN):</strong><br>49,673명 주파수 분해 학습 · 자폐 분류 AUROC <strong>0.810</strong> (최대 <strong>+41.4%</strong>)
      </div>
      <div class="sub-card">
        <strong>선행 2 (물리 역변환 인과추론, INCAMA):</strong><br>혈류지연·전극섞임 역변환 · 뇌파 인과 AUROC <strong>0.833</strong> (연산 <strong>2,000배</strong> 단축)
      </div>
    </div>
  </div>
</div>

<div class="status-bar">
  <div><span class="status-tag">ICLR 2027 심사 중</span> <strong>본 연구 (PALM / 구 PIMSM):</strong> 논문 #39398 심사 중 · 사전공개본 <a href="https://arxiv.org/abs/2605.16351">arXiv:2605.16351</a> (11월 개정본 업데이트)</div>
  <div><span class="status-tag blue">연계 논문</span> <strong>MBBN:</strong> <em>Communications Biology</em> 심사 중 (<a href="https://arxiv.org/abs/2503.23394">arXiv:2503.23394</a>) &nbsp;|&nbsp; <strong>INCAMA:</strong> <em>Nature Communications</em> 투고 준비 (<a href="https://arxiv.org/abs/2510.17318">arXiv:2510.17318</a>)</div>
</div>

---

<!-- Slide 2: GINR -->
<div class="slide-top">
  <div>
    <div class="slide-kicker">연구 1-4 (서울대 차지욱 교수팀) · 세부주제 2: 연속 시공간 뇌 표현 및 초해상도 복원</div>
    <h1 class="slide-title">생성형 내재 신경 표현 기반 뇌신호 초해상화·결측 복원 (GINR: SigNerd &amp; SOLID)</h1>
  </div>
  <div class="slide-badge">담당: 이세빈 · 이태양 연구원 (서울대)</div>
</div>

<div class="lead-box">
  <strong>핵심 요약:</strong> 장비별 뇌파 전극 차이·뇌영상 움직임 결측 &nbsp;➔&nbsp; <strong>연속 3D 시공간 함수(생성형 신경장) + 기초모델 정렬 확산</strong> &nbsp;➔&nbsp; <strong>8개 센서로 62채널 뇌파 복원 · 결측 뇌영상 재생</strong>
</div>

<div class="grid-2col">
  <div class="panel">
    <div class="panel-title">
      <span>핵심 개념도: 연속 신경장(SigNerd) + 기초모델 정렬 확산(SOLID)</span>
      <span class="panel-sub">양대 상보적 복원 트랙</span>
    </div>
    <img src="figures/s02_concept.svg" style="width:100%; height:auto;" alt="GINR 개념도" />
  </div>
  <div class="panel">
    <div class="panel-title">
      <span>주요 정량 성과: 뇌파 초해상화(2×~8×) 및 뇌영상 결측 복원</span>
      <span class="panel-sub">정규화제곱오차(NMSE, 낮을수록 우수) · 상관계수(PCC)</span>
    </div>
    <table class="res-table">
      <thead>
        <tr>
          <th>모달리티 및 복원 과제</th>
          <th>기존 보간법 / 비교군</th>
          <th>제안 모델 (SigNerd / SOLID)</th>
          <th>개선 폭</th>
        </tr>
      </thead>
      <tbody>
        <tr class="hi">
          <td><strong>① 뇌파 8배 초해상화</strong> (8 → 62채널)</td>
          <td>구면보간(SSI) 오차 2.204</td>
          <td><span class="win">SigNerd 오차 0.726 (상관 0.70)</span></td>
          <td>복원 오차 <strong>-67.1%</strong></td>
        </tr>
        <tr class="hi">
          <td><strong>② 뇌파 4배 초해상화</strong> (16 → 62채널)</td>
          <td>SSI 1.090 / TransINR 0.713</td>
          <td><span class="win">SEED 0.643 / PhysioNet 0.497</span></td>
          <td>뇌-컴퓨터 분류 <strong>1위 (47%)</strong></td>
        </tr>
        <tr>
          <td><strong>③ 측두엽 전체 결측 복원</strong> (SEED-V)</td>
          <td>SSI 1.364 / 확산(SRGDiff) 0.922</td>
          <td><span class="win">SOLID 오차 0.625 (상관 0.63)</span></td>
          <td>7개 설정 중 <strong>6개 세계 1위</strong></td>
        </tr>
        <tr>
          <td><strong>④ 뇌영상(fMRI) 움직임 결측 복원</strong></td>
          <td>스플라인 오차 4.26 (17% 폐기)</td>
          <td><span class="win">fMRI-GINR 오차 1.05 (r = 0.94)</span></td>
          <td>오차 <strong>-75.3%</strong> · <strong>100% 구제</strong></td>
        </tr>
      </tbody>
    </table>
    <div class="sub-cards">
      <div class="sub-card">
        <strong>트랙 A (순수 생성형 신경장, SigNerd):</strong><br>미 브룩헤이븐(BNL) 공동연구 · 3D 전극 좌표 무관 제로샷 연속 뇌전위 생성
      </div>
      <div class="sub-card">
        <strong>트랙 B (기초모델 유도 확산, SOLID):</strong><br>자체 뇌파 기초모델(DIVER-1) 의미 정렬 · 고주파 뇌파 생리학적 복원
      </div>
    </div>
  </div>
</div>

<div class="status-bar">
  <div><span class="status-tag">ICLR 2027 심사 중</span> <strong>NeuroX-EEG (SOLID-EEG):</strong> 논문 #53005 심사 중 (이태양 1저자·이세빈 공저, 뇌파 기초모델 정렬 확산 초해상화)</div>
  <div><span class="status-tag blue">투고 준비</span> <strong>NeuroX-Field (SigNerd):</strong> ICML 2027 준비 (이세빈 1저자·이태양 공저, SNU-BNL) &nbsp;|&nbsp; <strong>fMRI/dMRI GINR:</strong> <em>Nature Methods</em> 투고 준비</div>
</div>

---

<!-- Slide 3: VLM & SwiFT V2 -->
<div class="slide-top">
  <div>
    <div class="slide-kicker">연구 1-4 (서울대 차지욱 교수팀) · 세부주제 3: 뇌 기초모델 및 시각-언어-행동 정렬</div>
    <h1 class="slide-title">시각언어모델 연계 뇌 해독 (BrainVLM) 및 대규모 뇌 기초모델 (SwiFT V2)</h1>
  </div>
  <div class="slide-badge">담당: 왕희환 · 최주빈 연구원 (서울대)</div>
</div>

<div class="lead-box">
  <strong>핵심 요약:</strong> 수만 복셀 주의집중 분산·진폭 소실 &nbsp;➔&nbsp; <strong>424개 해부학 뇌영역 압축 + 다중 턴 비교(BrainVLM) + 5만 명 기초모델(SwiFT V2)</strong> &nbsp;➔&nbsp; <strong>인지·임상 예후 정밀 해독</strong>
</div>

<div class="grid-2col">
  <div class="panel">
    <div class="panel-title">
      <span>핵심 개념도: 대규모 뇌 기초모델 + 동결 시각언어모델 추론</span>
      <span class="panel-sub">뇌신호 · 음성 · 언어 · 행동 정렬</span>
    </div>
    <img src="figures/s03_concept.svg" style="width:100%; height:auto;" alt="BrainVLM 및 SwiFT V2 개념도" />
  </div>
  <div class="panel">
    <div class="panel-title">
      <span>주요 정량 성과: 과제 해독 · 표현형 회귀 · 다중감각 · 임상 예후</span>
      <span class="panel-sub">HCP 1,081명 · ABCD · 7개 외부 임상 코호트</span>
    </div>
    <table class="res-table">
      <thead>
        <tr>
          <th>세부 연구 및 평가 과제</th>
          <th>기존 뇌 기초모델 / 비교군</th>
          <th>제안 모델 (BrainVLM / SwiFT V2)</th>
          <th>개선 폭</th>
        </tr>
      </thead>
      <tbody>
        <tr class="hi">
          <td><strong>① 뇌 과제 해독</strong> (운동 5종 / 작업기억 8종)</td>
          <td>BrainLM 34.4% / 32.2%</td>
          <td><span class="win">BrainVLM 98.6% / 90.4%</span></td>
          <td>정확도 <strong>약 3배 도약</strong></td>
        </tr>
        <tr class="hi">
          <td><strong>② 다중 턴 비교 표현형 회귀</strong> (ABCD)</td>
          <td>단일 턴 결정계수(R²) -0.19 (실패)</td>
          <td><span class="win">3-턴 비교 R² +0.79 · 성별 97%</span></td>
          <td>참조 뇌 비교 <strong>정밀 보정</strong></td>
        </tr>
        <tr>
          <td><strong>③ 자연 발화 청취 뇌 반응 예측</strong></td>
          <td>단일모달 선형 결합 (음성/언어)</td>
          <td><span class="win">음성+언어 비선형 정렬 (Mind the Gap)</span></td>
          <td>예측 상관 <strong>+17.9% 향상</strong></td>
        </tr>
        <tr>
          <td><strong>④ 7개 코호트 14개 임상·인지 과제</strong></td>
          <td>BrainLM(6.3억) 0.586</td>
          <td><span class="win">SwiFT V2(900만) AUPRC 0.686</span></td>
          <td>임상 예후 <strong>0.734 (1위)</strong></td>
        </tr>
      </tbody>
    </table>
    <div class="sub-cards">
      <div class="sub-card">
        <strong>BrainVLM 핵심 기전:</strong><br>원시 진폭 + 표준화(z) 이중 경로 결합 → 부위별 진폭 손실 방지(운동 <strong>+24.5%p</strong>)
      </div>
      <div class="sub-card">
        <strong>SwiFT V2(5만 명) 뇌과학 검증:</strong><br>어휘 과제 뇌 차폐 분석 → 좌반구 언어 네트워크 편측화(<strong>76%</strong>, 브로카 영역) 규명
      </div>
    </div>
  </div>
</div>

<div class="status-bar">
  <div><span class="status-tag">ICLR 2027 심사 중</span> <strong>BrainVLM (CALIBRA-fMRI):</strong> 논문 #26688 심사 중 (왕희환 1저자, 해부학 영역 집계 및 다중 턴 비교 보정)</div>
  <div><span class="status-tag blue">사전공개 · 투고 준비</span> <strong>Mind the Gap:</strong> <a href="https://arxiv.org/abs/2502.12771">arXiv:2502.12771</a> (한동엽·조윤주) &nbsp;|&nbsp; <strong>SwiFT V2 (5만 명 기초모델):</strong> <em>Nature Communications</em> 준비 (최주빈·왕희환, 선행 <a href="https://arxiv.org/abs/2307.05916">arXiv:2307.05916</a>)</div>
</div>
