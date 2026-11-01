# BRIEFING — 2026-11-01T00:45Z

## Mission
M4 (Topic 4 FM-ReSU redesign, ACCEPTANCE T4.1–T4.3): give the worker a concrete, verifiable strategy; primary lens = scientific design (falsifiable question, card, controls, kill criterion, permitted/usable data). Recommend only; no production code.

## 🔒 My Identity
- Archetype: Teamwork explorer (General route), explorer 1 of 2 for M4
- Roles: read-only investigation + cheap probes
- Working directory (metadata): /home/juke/git/00IITP-AI/.agents/teamwork/tw-20261031-four-topics/explorer_M4_r1_1/
- Probe directory (only place for code): /home/juke/git/00IITP-AI/verification/explorer_M4_r1_1/
- Original parent: root coordinator (workflow B, run tw-20261031-four-topics); no native conversation ID given
- Milestone: M4
- Host: claude-code; model Opus 5.5; nested spawning NOT available; final report = StructuredOutput return

## 🔒 Key Constraints
- Read-only investigation — do NOT implement production code; probes only under verification/explorer_M4_r1_1/
- C1 protected hashes must stay rc 0; never edit src/*.py, tests, docs/03_empirical_analysis/*.md, empirical_results.json, HANDOFF.md, 그랜트아이디어.md, 아이디어.txt
- C4: no participant IDs printed/written (positions only); no git writes of any kind; no installs on DGX-Spark
- C6: ENIGMA stays on DGX-Spark/connectome/dgx1; never on B300; never read ~/enigma_ocd/data on B300
- ≤5 real subjects read-only for probes; ≤4 local CPU procs, nice, OMP_NUM_THREADS=2, PYTHONDONTWRITEBYTECODE=1
- B300: at most 0.25 GPU-h smoke test, ledgered; M4 needs none → plan 0 GPU-h
- C8: old report/JSON numbers are not results
- Work independently of peer explorer_M4_r1_2 (do not read its outputs)

## Current Parent
- Root coordinator; Updated: not yet

## Investigation State
- **Explored paths**: ORIGINAL_REQUEST, ACCEPTANCE, RESUME_2026-11-01, role/runtime adapters, sci-pipeline SKILL, survey_2/3 handoffs, src/fractal_motif_resu.py (protected), Topic1 loader/preprocess/tr_table, results/topic1/2026-10-31/manifest.json (aggregates only), topic3 estimators index, local env
- **Key findings**: see progress.md; ReSU (arXiv:2512.23146) = batch past–future CCA + rectification, no lateral connections, no local rule → old code is not ReSU
- **Unexplored areas**: probes A–D pending

## Key Decisions Made
- Planned real subjects: positions 0,1,2 (already burned by survey) + 2 new by declared rule → 5 total, all declared dev/burned
- 0 GPU-h; no B300 contact needed for M4

## Artifact Index
- DISPATCH.md — dispatch verbatim
- progress.md — heartbeat
- handoff.md — final 5-component report (pending)
