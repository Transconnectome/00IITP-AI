# Acceptance criteria — run tw-20261030-topic1 (Topic 1, steps 1–4)

Project root: /home/juke/git/00IITP-AI (branch feature/topic1-lag-motif-v2)
Python: /home/juke/superclaude-env/bin/python3 (has numpy/pandas/networkx/pytest; check before assuming others)

## Outcomes required (ALL)
A1 Extractor v2 (new code; existing src/*.py and tests/* must remain byte-identical):
  - Uses only the valid (non-padded) portion of each subject's series; reports valid T per subject.
  - Lag is defined in seconds, consistent across sites with TR 0.7–2.0 s; the method and its parameters are documented.
  - Uses all 304 ROIs (no arbitrary subsampling).
  - Null model preserves each node's in/out degree AND never creates reciprocal (mutual) edges or self-loops; the
    significance profile is computed only over triad classes that the oriented real graph can contain; this restriction is documented.
  - Works on the real data paths read-only (mmap cache and/or npy directory in /home/juke/git/enigma_ocd_mbbn/data).
  - No synthetic fallback can silently replace a missing real subject (missing subject → explicit error).
A2 Synthetic ground-truth fixtures (pytest, fast, CPU) that PASS and that would FAIL on the defect they target:
  - Injected lagged directed 3-cycle among known nodes is detected (030C significance clearly above null), and absent in a no-injection control.
  - Time reversal of the input flips the sign of the net-flow matrix.
  - Every null graph: zero reciprocal edges, zero self-loops, in/out degree sequences identical to the real graph.
  - Padding: appending zero rows does not change the extracted features.
  - Lag-in-seconds: the same underlying signal sampled at two different TRs yields consistent net-flow direction.
  - Spurious-direction control: independent signals that differ only in autocorrelation (e.g., AR(1) with different φ, or
    HRF-smoothed vs not) — quantify the false net-flow/motif signal this produces and either show it is controlled
    (e.g., autocorrelation-matched surrogate null) or report the bias magnitude explicitly as an open limitation.
A3 Timing on 5 real subjects (local CPU only; no GPU): per-subject wall time per channel at the planned null count, peak RAM,
  extrapolated full-cohort CPU-hours for 1,706 subjects × planned channels (labelled 추정). Raw timing log saved.
  Reports must NOT print participant IDs (use positional index or salted hash).
A4 Frozen analysis card (pre-registration), new dated file under docs/03_empirical_analysis/topic1/, written BEFORE any
  full-cohort result exists, containing: hypotheses; primary endpoint (null-corrected Z/SP of 030C and a 030C-vs-030T contrast);
  population (N ceiling 1,706; exclusion of TR>2.0 s sites stated); confound handling (site via ComBat and/or LMM random
  effect, age, sex, valid T, motion if available — state whether FD exists); site-held-out CV for OCD vs HC classification;
  kill criterion |d|<0.15 or p≥0.05 on primary endpoint; baselines (static FC, existing MBBN AUROC≈0.63 with exact source path
  and number verified from file); Y-BOCS regression; medication analysis only within OCD with coding source cited and HC coding
  flagged; CSTC subnetwork handled honestly (either verified ROI labels with source, or dropped/marked exploratory);
  multiple-comparison policy; the card's sha256 recorded.
A5 Safety: existing 86 tests still pass; protected files unchanged (sentinel/PROTECTED_HASHES.txt); no edits in external repos;
  no full-cohort run; no Slurm/ssh job submission; no git commit/push; no GPU use; no data or IDs sent to external services.
A6 Open issues recorded (not fixed in this run): report-vs-JSON discrepancy (APPROVED_PROPOSAL.md), any limitation found.

## Output ownership (production paths, outside metadata)
- Worker of iteration N: src/topic1_lagmotif/ (new package), tests/topic1_lagmotif/ (new), scripts/topic1_timing.py (new),
  results/topic1/2026-10-30/ (timing logs, small JSON), docs/03_empirical_analysis/topic1/ (analysis card).
- Reviewers/challengers/auditors: only verification/<identity>/ for probes; read-only elsewhere.
