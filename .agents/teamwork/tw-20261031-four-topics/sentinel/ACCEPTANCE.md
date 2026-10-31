# Acceptance criteria — run tw-20261031-four-topics
Project root /home/juke/git/00IITP-AI (branch feature/topic1-lag-motif-v2, uncommitted). Python /home/juke/superclaude-env/bin/python3.
Methodology reference (read): /home/juke/.claude/skills/sci-pipeline/SKILL.md (frozen card before results, synthetic ground truth, run records, verdict taxonomy).

## Common (all milestones)
C1 Protected files byte-identical: `cd /home/juke/git/00IITP-AI && LC_ALL=C sha256sum -c .agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt` rc 0. This includes the frozen Topic 1 card (2026-10-30), its r1 results, the existing docs/03_empirical_analysis/*.md and empirical_results.json, old src/*.py, old tests, HANDOFF.md, 그랜트아이디어.md, 아이디어.txt, docs/qa_prep_*.md, docs/05_meetings/.
C2 Old suite 86 passed (explicit list) and tests/topic1_lagmotif passes; each milestone's new tests pass.
C3 Each new experiment: dated analysis card frozen (sha256 recorded) BEFORE any real-data result it governs; synthetic ground-truth fixtures that fail on the targeted defect; raw run logs; results in new dated paths; deviations recorded in a dated addendum, never by editing a frozen card.
C4 No participant IDs printed or written (positional index or salted hash). No git commit/push/stash/reset/checkout. No package installs into shared/system envs on DGX-Spark (project-local venvs on remote servers are allowed). Never read ~/.claude/settings.json or secrets.
C5 Compute: GPU training → B300 (NIPA, 4 nodes × 8 B300; ssh 61.107.201.98/.99/.101/.103 user connectome, currently via ProxyJump dgx1,connectome). Before using a B300 GPU check nvidia-smi; use only idle GPUs; never kill others' processes. Cap for this run without further approval: 64 GPU-hours total, logged in results/gpu_ledger_2026-10-31.md (node, GPUs, start/end, purpose). B300 has no torch/scheduler: create a project-local env under /scratch/iitp4/ (not system-wide). CPU jobs: local DGX-Spark (≤16 processes, nice) or connectome.
C6 Data governance: ENIGMA-OCD participant data (/home/juke/git/enigma_ocd_mbbn/data) must NOT be copied to B300 or any non-lab machine. On B300 only: synthetic data, public datasets, UK Biobank derivatives (PI-approved 10/31), model weights/representations without participant IDs. If a task needs ENIGMA on GPU, use connectome/dgx1 or stop and report.
C7 External repos read-only (enigma_ocd_mbbn, VRABES, SwiFT*, paper-review, etc.). Copy what you need into this project.
C8 Report numbers in EMPIRICAL_ANALYSIS_REPORT.md must not be cited as results; new results come from this run's dated outputs only.

## M1 Topic 1 — hardening then step 5 (full cohort)
T1.1 Tests for extract_subject's return contract (304 ROIs, valid_T, curl ≠ plain F, seed rule per position/channel/density, SP normalisation). Kill the 5 mutants that survived the victory audit: verification/victory_auditor_1/mutants.py (ROI-loss in extract_subject) and mutants_extra.py (4/4) — rerun them and show 0 survivors.
T1.2 Cohort statistics script implementing frozen card §4–§6 exactly (site-adjusted d, Freedman–Lane permutation p, Holm over E1/E2, degeneracy fallback rule, kill rule, secondary analyses). Validated on synthetic cohorts with the real site×diagnosis structure: null FPR within MC error of 0.05; planted effect recovered. Script sha256 recorded BEFORE first real-label analysis.
T1.3 Pinned subject manifest (positions/hashed), minimum length on the 2 s grid, per-group and per-site acceptance and degeneracy rates reported.
T1.4 Full-cohort feature extraction with the frozen parameters (card sha 1e589f0b…75aa unchanged), run locally on CPU or on connectome (lab-controlled only), raw run log with params hash. Then statistics → verdict per card (killed / survives per endpoint) stated exactly by the card's rules, with the spurious-direction limitation and degeneracy rates beside it. Results in results/topic1/2026-10-31/ and a dated result report in docs/03_empirical_analysis/topic1/.
T1.5 If card §2 degeneracy fallback triggers or any deviation occurs, record in a dated addendum and report both.

## M2 Topic 3 — rerun layerwise PR / spectral diagnostics
T3.1 Locate real inputs (e.g. /home/juke/git/VRABES/RemissionAnalysis, SwiFT E192 layer representations, BrainLM/BrainJEPA/NeuroSTORM) read-only; document provenance; resolve why empirical_results.json PR≈1 vs report (centered vs uncentered) with a fixture.
T3.2 Frozen card (hypotheses, estimators: centered participation ratio, heavy-tail α with method stated, null/controls such as shuffled/random-init representations, decision rules) before the real rerun.
T3.3 Fixtures: known-rank synthetic matrices give known PR; α estimator recovers known tail index; centering defect caught.
T3.4 Rerun on real representations; dated results + report; state which earlier claims hold or fail. GPU (B300) only if representations must be regenerated.

## M3 Topic 2 — redesign (connectome box-covering RG pooling for SwiFT)
T2.1 Establish the actual SwiFT architecture where spatial merging happens (from code, not docs); the old premise (PatchMerging between layer_2 and layer_3, both 1536-d) is broken — document what is true.
T2.2 Redesigned, falsifiable question + frozen card (baseline Euclidean PatchMerging vs ConnectomeRGBoxPooling, same data/seeds/budget, metric, kill criterion). Implementation with unit tests (shape, permutation/box-assignment invariants, gradient flow) and a synthetic fixture where RG pooling should help and one where it should not.
T2.3 Pilot training on B300 within the C5 cap on data allowed by C6; results + verdict per card. If the redesign finds the question not testable within the cap, deliver the card + implementation + a costed plan and say so.

## M4 Topic 4 — redesign (backprop-free local learning FM-ReSU)
T4.1 Diagnose why all conditions incl. C0 reach forecast R²=1.0 (task too easy/leak/bug) with evidence.
T4.2 Redesigned task where a trivial baseline does not saturate; frozen card (conditions, backprop baseline, metric, seeds, kill criterion).
T4.3 Implementation + fixtures (local rule stability e.g. spectral radius of M < 1, no gradient leak — prove no autograd backprop in the local-learning path); run (CPU or B300 within cap); results + verdict per card.
