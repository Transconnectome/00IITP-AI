# progress — explorer_FU_D_r3_3
Last visited: 2026-11-01T22:14:23Z
- read role/adapters/request/acceptance/decisions/gate/resume; read FU-D verdict code + card §8-10
- wrote DISPATCH.md, BRIEFING.md
Last visited: 2026-11-01T22:24:36Z
- C1 rc 0; FU-D receipts card/code/output/addendum_01 OK
- workflow_C_script: MAX_ITER = 3 -> r3 is the LAST FU_D iteration; gate needs all 5 verifiers positive
- targeted 30 mutants vs current suite: 19 SURVIVED / 11 KILLED (control 189 passed)
- probe alias_and_terms: zero-padded alias also flips a Stage-1 category (stop -> inconclusive, rc 0); inf den and negative terms accepted
- sweep3 (758 AST mutants) started then stopped by me to reorder (log kept *_ABORTED_reorder.log); first proposal run INVALID (file not collected: proposed_ prefix) — log kept *_INVALID_*; runner fixed to strip prefix
- targeted vs current+proposal: control 224 passed (35 proposal tests green on frozen code); running
- rm of work_s/work_t leftovers denied by harness; not worked around
Last visited: 2026-11-01T22:46:52Z
- targeted 30 vs current+proposal: 30/30 KILLED (control 224 passed)
- sweep3 (758) vs current+proposal running; interim survivors are output-structure deletions (sens category None, n_seeds, fminus_gate, stage1 dict entry) + needs_fminus bool drops
