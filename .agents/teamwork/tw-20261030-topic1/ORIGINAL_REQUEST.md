# Original User Request

## Initial Request — 2026-10-30 (same session, received before this run; exact receipt time not recorded)

/home/juke/git/00IITP-AI 레포지토리에서 커넥톰 모티프(Milo et al., 2002/2004), 박스 커버링 재규격화군 및 허브 반발(Song et al., 2005/2006), 오차역전파 없는 생물학적 국소 학습(Chklovskii et al., 2026 ReSU; Buzsáki, 2019)을 결합한 4대 실증 연구를 이어서 진행하자.

먼저 다음 인수인계 및 산출물 문서들을 읽고 현재 상태를 파악해 줘:
1. /home/juke/git/00IITP-AI/docs/03_empirical_analysis/NEXT_SESSION_HANDOFF_AND_PROMPTS.md
2. /home/juke/git/00IITP-AI/docs/03_empirical_analysis/EMPIRICAL_ANALYSIS_REPORT.md
3. /home/juke/git/00IITP-AI/docs/03_empirical_analysis/LOCAL_REPO_INTEGRATION_SPEC.md
4. /home/juke/git/00IITP-AI/docs/03_empirical_analysis/LAB_SEMINAR_BRAINSTORMING_GUIDE.md

주의사항:
- 제안서/행정 문서가 아니라 실제 연구실 데이터와 코드에 기반한 실증 분석(Empirical Analysis)과 논문용 실험에 집중할 것.
- /home/juke/git/00IITP-AI 내 기존 미커밋 파일(그랜트아이디어.md, 아이디어.txt, HANDOFF.md 등)은 절대 수정하거나 건드리지 말 것.
- 대규모 GPU 학습/스윕은 반드시 1순위 connectome 서버(ssh connectome, Slurm 8xA5000) 또는 dgx1(ssh dgx1, 8xV100)에 먼저 배치하고, 로컬 dgx-spark는 가벼운 검증에만 사용할 것.

문서를 읽은 뒤, Topic 1(ENIGMA-OCD 1,706명 전수 분석), Topic 2(a-SwiFT RG Box Pooling 이식), Topic 3(VRABES/DIVER 스펙트럼-RG 5대 지표 진단), Topic 4(FM-ReSU 뉴로모픽 무역전파 학습) 중 오늘 바로 실행할 첫 번째 실험 단계를 제안해 줘.

## Follow-up — 2026-10-30T11:09Z (approx., KST 20:09)

워크플로 이용해서 진행 /teamwork

(Context: this follow-up approves the assistant's proposal of steps 0–4 recorded in sentinel/APPROVED_PROPOSAL.md. Step 5 (connectome Slurm full-cohort job) was explicitly deferred for separate approval and is NOT authorized by this message. The skill invocation args were: "Topic 1 (ENIGMA-OCD directed lag motif) 1–4단계: 추출기 수정 4종, 합성 정답 고정구, 5명 시간 측정, 분석 카드 동결 — Workflow 이용")
