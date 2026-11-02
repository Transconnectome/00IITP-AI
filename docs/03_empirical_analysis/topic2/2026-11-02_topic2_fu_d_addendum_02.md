# Topic 2 follow-up D (FU-D) — addendum 02 (2026-11-02 KST, worker_FU_D_r3, written AFTER all FU-D results)

Everything below is post hoc. No governed computation changed: no training, evaluation, seed plan or verdict
computation was rerun to produce a new governed output, and no frozen or receipt-pinned file was edited. Untouched:
the FU-D card (`2026-11-02_topic2_fu_d_card.md`, sha256 1b7fee6c…001b), the 29 files of
`results/topic2/2026-11-02_fu_d/code_sha256_at_freeze.txt`, the runs, `verdict.json` (sha256 f6b295d9…59fc), the
result report, addendum 01, `tests/topic2_fu_d/test_fud_r2_guards.py` and every existing receipt. The FU-D verdict
stays **`inconclusive` (measurement capacity at E192)**: F+ gate gains (E−C)/E = 0.363 % and (S−C)/S = 0.655 %, both
< δ = 1 %; Stage 1 not run; the r1 E36 `stop` stands alone. GPU used for this addendum: 0 GPU-h.

## 1. Why this addendum exists: the FU-D r2 gate

The FU-D r2 gate failed because challenger_FU_D_r2_2 returned REFUTED on two blocking items; the other four verifiers
passed (reviewer ×2 APPROVE, challenger_FU_D_r2_1 CONFIRMED, auditor CLEAN). No verifier disputed the shipped
verdict; several recomputed it independently.

1. **B1 (C12).** In `src/topic2_fu_d/verdict.py::_stage1_category`, `if c2 != cat:` changed to
   `if c2 != cat and c2 != "inconclusive":` survived the whole 195-test suite. On a Stage-1 input where all seeds give
   `stop` and the seeds without the stalled run give `inconclusive`, the frozen code returns `inconclusive`
   (stall-sensitive), as card §8 step 7 requires; the mutant returns `stop (killed)`. The only step-7 flip test covered
   one ordered pair (all seeds `inconclusive`, without stalled seeds `stop`). challenger_FU_D_r2_1 reported the same
   class (CV09) and its script-level sibling (CP01/CP02: stall detection restricted to arm S or to arms C and S) as
   nonblocking.
2. **B2 (alias run directories).** `design.DIR_RE` (`\d+` and `$`) together with `int()` maps non-canonical
   directory names to planned run keys, and `records.load_runs` lets the later-sorted alias overwrite the canonical
   record, also under `strict=True`. Card §8 calls duplicate or mismatching records protocol errors; addendum 01
   did not list this departure.

Both are coverage or disclosure gaps; neither is reachable on the shipped data, and neither changes a shipped output
(§3, §5, §6). The r3 explorers (explorer_FU_D_r3_1/2/3) found the B1 class wider than C12 (other step-7 conjuncts, the
script's stall wiring) and further survivors in operator classes no earlier sweep had used; all are addressed below.

## 2. Correction of addendum 01 §4

Addendum 01 §4 states, for its final rerun, "each of the 8 is equivalent", and the r2 worker's report says
"0 non-equivalent survivors remain". That statement is true only for addendum 01's own 423-mutant set (157 collected
r1/r2 mutants and a 266-mutant sweep). It is false as a statement about the verdict code in general: C12/CV09 and the
other r2 verifier survivors listed in §5 are non-equivalent mutants outside that set. Addendum 01 is receipt-pinned and
is not edited; this paragraph is the correction. Every mutation statement in this addendum is scoped to the mutant
set named with it.

## 3. Errata: where the frozen code departs from the card (new in this addendum)

The card governs. The frozen code is not edited (a code change after the result would need a new card). Each item
gives a reading rule for any `verdict.json` the frozen script writes, and the shipped-data evidence that the shipped
verdict is outside the defect. The frozen-code behaviour was reproduced on synthetic records in a temporary
directory outside the repository (`verification/worker_FU_D_r3/probes/errata_probe.py`, output
`errata_probe.out.json`); no alias, newline or Unicode directory name was ever created inside the repository.

**E5 (B2). Alias run directory names are accepted and override the canonical record, on the gate path and on the
Stage-1 path, also with `strict=True`.** `DIR_RE = ^(hcp|Fplus|Fminus)_([ECS])_s(\d+)(_a1)?$` followed by `int()`
accepts, as aliases of `Fplus_C_s0`: zero-padded digits (`Fplus_C_s00`, `Fplus_C_s000`), non-ASCII decimal digits
(Arabic-Indic, full-width) and a trailing newline (`$` matches before a final newline). `load_runs` stores records in
a dict keyed by (run key, attempt), so the later-sorted name wins and becomes `used_dir`. Probe: with a canonical
gate record that fails the gate (C-vs-E gain 0.14 %) and an alias holding C = 0.60, every one of the five alias forms
is loaded under strict load, the gate passes (gain 14 %) and the script exits 0 (verdict `no_verdict` "seed plan
missing" instead of `inconclusive`); on the Stage-1 path an alias `hcp_C_s00` turns a canonical `stop` into
`inconclusive` (rc 0, `used_dir` = the alias). *Reading rule:* every directory in `runs/` must satisfy
`run_name(*parse_dir(name)) == name` exactly, in ASCII; any other name that parses is a duplicate record and voids the
verdict (protocol error, `no_verdict`). Zero-padding, Unicode digits and newlines are instances of this rule, not an
exhaustive list. *Shipped:* `runs/` holds exactly `Fplus_C_s0`, `Fplus_E_s0`, `Fplus_S_s0`; each is ASCII, has no
surrounding whitespace, round-trips through `run_name(*parse_dir(name))`, and is its own `used_dir` in the shipped
`verdict.json` (test `test_shipped_run_dir_names_round_trip_exactly_and_are_the_dirs_used`).

**E2′ (widens addendum 01 E2). Non-finite, negative and zero error terms are accepted.** `validate_completed` checks
only that `Σnum/Σden` is finite and equals `test_nmse`. An infinite denominator entry gives `Σnum/Σden = 0`, which is
finite, so the record is accepted with `test_nmse = 0` (a gate C record with one infinite denominator makes the gate
pass); negated numerators are accepted with `test_nmse = −0.7`; all-zero numerators are accepted. A NaN error term is
rejected (the pooled ratio is NaN), and a NaN `test_nmse` with finite terms is accepted (addendum 01 E2). *Reading
rule:* a completed record is valid only if every `test_num` entry is finite and ≥ 0, every `test_den` entry is
finite and > 0, and `test_nmse` is finite; otherwise the verdict is void (protocol error). *Shipped:* every gate record
has 16 finite numerators ≥ 0, 16 finite denominators > 0 and 0 < `test_nmse` < 1
(`test_shipped_error_terms_are_finite_nonnegative_squared_errors_over_positive_denominators`).

**E6. The `seeds` list of `seed_plan.json` is not checked against `n_seeds`.** The script reads only `n_seeds` and
derives seeds 0..n−1; card §10.2 says seeds are always 0..n−1. Probe: a plan `{"n_seeds": 4, "seeds": [3, 5, 7, 9]}`
with a valid receipt is accepted and Stage-1 seeds 0–3 are read. *Reading rule:* a plan whose `seeds` is not
`list(range(n_seeds))` is a protocol error. *Shipped:* no `seed_plan.json` exists (the gate failed before planning;
`test_shipped_results_dir_has_no_seed_plan_and_no_fminus_or_stage1_dirs`).

**E7. F− records without a would-be keep are flagged, not stopped; a lone completed F− record is ignored; on the
failed-gate path F− records are skipped.** Card §8: F− runs only for a would-be keep, and unplanned runs are protocol
errors. The script raises `protocol_flag_fminus` (and still writes a verdict) when the F− group state is not
`missing` and the Stage-1 category is not `keep`. A single completed F− record whose partner is absent gives group
state `missing`, so it is neither read nor flagged. When the gate fails or is incomplete, F− directories are skipped
by the non-strict gate read and never flagged (the same mechanism as addendum 01 E1). *Reading rule:* any `Fminus_*`
directory present without a would-be keep is a protocol error, whatever flag the script wrote. *Shipped:* no
`Fminus_*` directory exists.

**E8. The sidecar `fud_code_sha256` is never validated.** `validate_completed` checks the frozen r1 code hashes of
the record and (with `--wrapper-sha256`) the wrapper hash of the sidecar, but never the sidecar's FU-D code hashes; a
sidecar with a wrong `fud_code_sha256` is accepted. *Reading rule:* a run counts only if its sidecar `fud_code_sha256`
equals the `src/topic2_fu_d/*.py` entries of `code_sha256_at_freeze.txt`. *Shipped:* all three gate sidecars carry
exactly those 8 hashes and the freeze wrapper hash, with `post_checks_ok` true
(`test_shipped_sidecars_carry_the_frozen_fud_code_and_wrapper_hashes`).

**E9 (minor, no shipped effect).** A record whose `seed` is `False` (or `0.0`) equals the integer 0 and is accepted;
symlinked run directories are followed; a plain file whose name starts with `hcp_` in `runs/` raises the Stage-1
`protocol_flag` when the gate fails. *Reading rule:* run keys are integers, run directories are real directories, and
the flag means "some `hcp_*` entry exists". *Shipped:* three real directories with integer seed 0.

**Wording errata (no effect on any category).**
- **W4, card §9 (a) vs step 6.** When the capacity floor applies (step 6), the frozen code returns before step 7, so
  `stall_sensitivity` is not written although §9 (a) says the stall sensitivity is reported. The category
  (`inconclusive`, floor) is the card's. *Reading rule:* under the floor the stall sensitivity is unreported, not
  absent. The tests pin only that the floor reason wins over a stall that would flip the category; they do not pin
  the absence.
- **W5, card §10.3 vs the reason text.** With the gate passed, a seed plan with n ≥ 4 and no Stage-1 run launched
  (cost guard), the reason reads "Stage 1 incomplete after one rerun (software failure)". Card §8 step 4 and §10.3 give
  the same category (`no_verdict`) and call such a run missing. *Reading rule:* in that case read the reason as
  "Stage 1 not launched under the cost guard". The tests pin the reason only for the incomplete case.

**Reuse condition.** Any future follow-up card (such as result report §5 options D′, D-gate-seeds or D-mid) that
reuses `src/topic2_fu_d` must replace `design.parse_dir`, `records.load_runs` and `records.validate_completed` under
its own pre-result freeze so that E1, E2′, E3, E4, E5, E6, E7, E8 and E9 are enforced directly in code rather than by
post-hoc reading rules.

## 4. Additive r3 test suite (`test_fud_r3_guards.py`, `test_fud_r3_oracle.py`, `test_fud_r3_full_output.py`)

Three additive files (194 new tests total; `tests/topic2_fu_d` grows from 195 passed in r2 to 389 passed in r3) close
B1, every non-equivalent r2 verifier survivor, and the operator-sweep survivor classes found by the r3 explorers. No
existing test file is edited, and the verdict script is always invoked with `--out` inside `tmp_path`.

| file / group | what it pins | key mutants killed |
|---|---|---|
| `test_fud_r3_guards.py` — B1 step-7 matrix (28 fixtures × 3 levels + 16-pair table + C12 witness) | Every reachable ordered pair `(cat_all, cat_without_stalled)` for `n = 5` with `stalled = (4,)` (all 14 reachable pairs) and `stalled = (3, 4)` (12 pairs), verified against an independent card-§8 oracle (`scipy.stats.t.ppf(0.975, df)`, literal `δ = 0.01`) at `_stage1_category` and `decide`; an exhaustive 4×4 = 16-pair decision table over all `(cat_all, cat_wo)` pairs; a direct C12 witness (`stop` with all 5 seeds, `inconclusive` without stalled seed 4); `< 2` unstalled seeds (`category: None`); deduplicated/sorted `dropped_seeds` | `cha2_2:C12`, `cha2_1:CV09`, `exp3_1:own:E7a`–`E7f`, `exp3_1:own:E7i`, `exp3_2:own:N01`, `N04`–`N08`, `N18`, `N19`, `exp3_3:T01`–`T08`, `r3:conj*` on `c2 != cat` |
| `test_fud_r3_guards.py` — B1 script stall wiring | Script-level stall detection in each of arms `E`, `C`, and `S` individually (flipping `stop` to `inconclusive`), two-seed / two-arm stalls (`hcp_E_s3` + `hcp_S_s4` and `hcp_E_s1` + `hcp_C_s3`), and the unstalled control on identical numbers | `cha2_1:CP01`, `cha2_1:CP02`, `exp3_1:own:W1`, `exp3_2:own:N09`, `N12`, `N14`, `exp3_3:T09`–`T11` |
| `test_fud_r3_guards.py` — gate isolation & missing `runs/` | Missing gate run, gate run awaiting rerun, or gate run failed after rerun with a seed plan and complete Stage-1 `keep` records → `no_verdict` with Stage 1 unread; failed gate value with Stage-1 `keep` records → `inconclusive` with `protocol_flag`; stray `hcp_C_s3` (non-seed-0) raises `protocol_flag`; missing `runs/` folder → `no_verdict` (rc 0) | `rev2_1:R31`, `cha2_2:S11`, `cha2_1:CP12`, `exp3_3:T15`, `exp3_3:W560`, `exp3_3:W703` |
| `test_fud_r3_guards.py` — record & design pins | `post_checks_ok` literally `True` (missing, `None`, `False`, `1`, `"true"`, `1.0` rejected); exact 2-digit `hNN` tokens and non-string token rejection; all 6 `HP_FIELDS` (`steps`, `batch`, `lr`, `wd`, `warmup_frac`, `mask_ratio`); NaN numerator rejected; wrapper sha checked iff expectation given; `perm_key` rejects unknown arms | `cha2_1:CR13`/`cha2_2:R07`, `cha2_1:CR01`/`cha2_2:R04`, `exp3_3:T18`, `T19`, `exp3_3:W351`, `W352`, `W365`, `W369`, `W413`, `W417`, `W419` |
| `test_fud_r3_guards.py` — F− flag & would-be-keep rules | F− records (completed or failed, one or both arms) without a would-be `keep` raise `protocol_flag_fminus`; F− records on a would-be `keep` are read, set `fminus_gate` and `needs_fminus: True`, and never raise `protocol_flag_fminus`; would-be `keep` with F− missing sets `needs_fminus: True` | `cha2_1:CP07`/`cha2_2:S05`, `cha2_1:CP14`, `exp3_3:T20`, `exp3_3:W076`, `W212`, `W569`, `W646`, `W690`, `W746` |
| `test_fud_r3_guards.py` — secondary pins & stdout summary | Script default `B = 10,000`, `seed = 0`, `num/den` argument order, explicit `--n-boot` forwarding, per-subject seed-mean axis (`axis=0`, 16 subjects), `val_curves` keys/values, and stdout JSON summary on Stage-1 and gate paths | `rev2_1:R34`/`cha2_1:CP03`/`cha2_2:S07`, `cha2_1:CP04`/`cha2_2:S08`, `cha2_1:CP05`, `cha2_1:CP11`/`cha2_2:S09`, `exp3_1:own:W2`, `exp3_3:T21`–`T24`, `exp3_3:W498`, `W601`, `W640`, `W643`, `W658`–`W660`, `W662`, `W697`–`W701`, `W723`, `W725`–`W727`, `W737`–`W739`, `W752`–`W757` |
| `test_fud_r3_guards.py` — `decide()` reasons, `δ` forwarding, floor & shipped invariants | All 17 `decide()` verdict/reason branches, `n_seeds` and `primary_reason` outputs; explicit `delta` forwarded to `fplus_gate`, `primary_category`, `_stage1_category` and `fminus_gate`; capacity floor short-circuits before stall flip; shipped directory round-trip (E5), positive finite error terms (E2′), sidecar `fud_code_sha256` and `wrapper_sha256` (E8), no seed plan / F− / Stage-1 dirs (E6, E7), default `--out` path in a temp dir | `rev2_2:R35`, `cha2_1:CV15`, `cha2_2:C23`, `cha2_1:CV19`, `exp3_3:T16`, `T17`, `exp3_3:W032`, `W037`, `W051`, `W100`, `W123`, `W139`, `W166`, `W167`, `W196` |
| `test_fud_r3_oracle.py` (2 tests, 3,000 scenarios) | Independent card-§8 step 1–8 oracle (`scipy.stats.t.ppf(0.975, df)`, literal `δ = 0.01`, `floor = 0.999`) compared against `V.decide()` across 3,000 seeded scenarios reaching all 5 verdicts, all 4 primary categories, floor, stall flips, and F− states | Class-level guard against any category-changing mutation in `verdict.py` |
| `test_fud_r3_full_output.py` (18 tests) | Whole-`verdict.json` and stdout-summary deep equality (exact key sets at every level, exact strings/ints/bools, independent arithmetic) across 17 synthetic script scenarios plus a discriminating self-test | Any structural or value mutation of `verdict.json` across gate, Stage-1, stall, floor, F−, rerun, and cost-cap paths |

**P1 (why `stop → keep` and `stop → modify` are algebraically unreachable in step 7 for `n = 5` with 1 or 2 stalled
seeds).** For `n` all-seed I1 gains with sample mean $\bar x_n$ and sample SD $s_n$, step 5 assigns `stop` only when
$\bar x_n + t_{0.975, n-1} s_n / \sqrt{n} < \delta$. Dropping $n - k$ stalled seeds leaves $k \in \{3, 4\}$ kept seeds
with mean $\bar x_k$; for the kept seeds to reach `keep` or `modify`, step 5 requires $\bar x_k \ge \delta > \bar x_n$.
Writing $d = \bar x_k - \bar x_{\text{drop}} > 0$, we have $\bar x_n = \bar x_k - \frac{n-k}{n} d$, and by the
between-group variance decomposition $(n - 1) s_n^2 \ge \frac{k(n-k)}{n} d^2$, so
$$
\text{hi}_n = \bar x_n + t_{0.975, n-1} \frac{s_n}{\sqrt{n}}
\ge \bar x_k + d \left( t_{0.975, n-1} \sqrt{\frac{k(n-k)}{n^2(n-1)}} - \frac{n-k}{n} \right).
$$
For $n = 5, k = 4$, $t_{0.975, 4} \sqrt{4 / (25 \cdot 4)} = 2.7764 / 5 = 0.5553 > 1/5 = 0.20$; for $n = 5, k = 3$,
$t_{0.975, 4} \sqrt{6 / (25 \cdot 4)} = 0.6801 > 2/5 = 0.40$. Hence $\text{hi}_n > \bar x_k \ge \delta$, contradicting
$\text{hi}_n < \delta$. (The 16-pair decision table in `test_fud_r3_guards.py` also exercises both pairs directly via a
`primary_category` stub so that no conjunct on `cat` or `c2` can hide behind P1.)

**File set.** The `tests/topic2_fu_d/` directory now holds 16 files: the 12 freeze-pinned files of
`code_sha256_at_freeze.txt`, `test_fud_r2_guards.py` (pinned in `addendum_01_sha256.txt`), and the 3 new r3 files
pinned in `addendum_02_sha256.txt`.

## 5. Union mutation verification (`verification/worker_FU_D_r3/mutation/union_r3.out.json`)

**Scope and sources.** `collect_mutants.py` collects every FU-D mutant list written in r1, r2 and r3 (11 lists, 1,518
entries in `collected.json`):
- `worker_FU_D_r2/union`: 157 (all 6 r1 verifier lists and all 3 r2 explorer probes)
- `worker_FU_D_r2/sweep`: 266
- `reviewer_FU_D_r2_1`: 44 (`rev2_1`)
- `reviewer_FU_D_r2_2`: 35 (`rev2_2`, its 36 entries minus its no-change control)
- `challenger_FU_D_r2_1`: 65 (`cha2_1`)
- `challenger_FU_D_r2_2`: 62 (`cha2_2`)
- `auditor_FU_D_r2_1`: 20 (`aud2_1`)
- `explorer_FU_D_r3_1`: 31 (`exp3_1`)
- `explorer_FU_D_r3_2`: 50 (`exp3_2`)
- `explorer_FU_D_r3_3/targeted.json`: 30 (`exp3_3:T01`–`T30`)
- `explorer_FU_D_r3_3/sweep3.json`: 758 (`exp3_3:W000`–`W757`)

To these, `sweep_r3.py` adds 533 AST-located mutants (`sweep_r3.json`) over `src/topic2_fu_d/{verdict,records,design}.py`
and `scripts/topic2fu_d_verdict.py` across 8 operator classes (`conj`: 121, `member`: 92, `cmp`: 92, `ifnot`: 69,
`argswap`: 57, `negop`: 49, `index`: 29, `kwconst`: 24).

**Protocol (`run_union_r3.py`, resumed to completion after checkpoint 1,225 by `resume_union_r3.py`).** Across the
2,051 raw entries, 1 entry (`rev2_1:R42`, which specified `scripts/topic2fu_d_verdict.py` for a line in
`src/topic2_fu_d/verdict.py::needs_fminus`; the intended `verdict.py` edit is in the union as `rev2_1:R43` and
`exp3_3:W107`) does not apply, and the remaining 2,050 entries deduplicate by byte-identical mutated file contents to
**1,675 distinct mutants**. Each distinct mutant runs on a fresh copy of the base tree (never symlinked, repo untouched;
at most 2 concurrent pytest processes, timeout 900 s):
- **Leg A (full r3 semantic suite):** all of `tests/topic2_fu_d` (globbed, ordered fast-first by
  `plugin/fud_order_plugin.py` without adding or dropping any test) minus `test_e192_model.py` (CPU model build) and
  minus the r2 receipt belt test `test_fud_frozen_card_and_code_match_their_freeze_receipts`.
- **Leg B (pre-r3 suite attribution, run for listed non-sweep mutants killed in Leg A):** the same suite with the three
  `test_fud_r3_*.py` files ignored.
- **Leg C (shipped output):** `scripts/topic2fu_d_verdict.py` on the copied shipped runs (`--out` in the work copy),
  deep-compared against the pinned `results/topic2/2026-11-02_fu_d/verdict.json`.

**Headline summary (`union_r3.out.json`).**
- Baseline control (`CTRL`): **SURVIVED** (`383 passed, 1 deselected` in Leg A; `189 passed, 1 deselected` in Leg B;
  `shipped_changed = False`).
- `raw`: **2,051** | `distinct`: **1,675** | `not_applied`: **1** (`rev2_1:R42`) | `invalid`: **0** (`[]`).
- `killed`: **1,511** | `survived`: **164**.
- `shipped_changing`: **515** — all 515 are **KILLED** in Leg A.
- **`survivors_changing_shipped_output`: 0 (`[]`).**
- **`killed_only_by_r3_files` (Leg A KILLED, Leg B SURVIVED): 34 distinct listed mutants** (representing 91 raw aliases
  across the r2 verifier and r3 explorer lists):
  - **B1 step-7 rule (`verdict.py:96`):** `cha2_1:CV09` (= `cha2_2:C12`, `exp3_1:c2:C12`, `exp3_2:chal2_1:CV09`,
    `exp3_2:chal2_2:C12`, `exp3_3:T01`), `exp3_1:own:E7a` (= `exp3_2:own:N01`, `exp3_3:T03`), `exp3_1:own:E7b`,
    `exp3_1:own:E7c` (= `exp3_3:T04`), `exp3_1:own:E7d` (= `exp3_2:own:N05`, `exp3_3:T05`), `exp3_1:own:E7e`
    (= `exp3_3:T06`), `exp3_1:own:E7f` (= `exp3_3:T07`), `exp3_1:own:E7i` (= `exp3_2:own:N19`), `exp3_2:own:N04`,
    `exp3_2:own:N06`, `exp3_2:own:N07`, `exp3_2:own:N08`, `exp3_2:own:N18`.
  - **B1 script stall wiring (`topic2fu_d_verdict.py:90`):** `cha2_1:CP01` (= `exp3_1:c1:CP01`, `exp3_2:chal2_1:CP01`,
    `exp3_3:T09`, `r3:member0501`), `cha2_1:CP02` (= `exp3_1:c1:CP02`, `exp3_2:chal2_1:CP02`, `exp3_3:T10`,
    `r3:member0504`), `exp3_1:own:W1` (= `exp3_2:own:N09`, `exp3_3:T11`, `r3:member0503`), `exp3_2:own:N12`,
    `exp3_2:own:N14`.
  - **All remaining non-equivalent r2 verifier and r3 targeted survivors:** `rev2_1:R31` (= `cha2_2:S11`,
    `exp3_3:T15`), `rev2_1:R34` (= `cha2_1:CP03`, `cha2_2:S07`, `exp3_3:T21`, `exp3_3:W722`, `r3:kwconst0491`),
    `exp3_1:r2:R35` (= `rev2_2:R35`), `cha2_1:CV15` (= `exp3_3:T16`), `cha2_1:CV19` (= `exp3_3:T17`), `cha2_1:CR01`
    (= `cha2_2:R04`, `exp3_3:T18`), `cha2_1:CR13` (= `cha2_2:R07`, `exp3_3:T19`), `cha2_1:CP04` (= `cha2_2:S08`,
    `exp3_3:T22`), `cha2_1:CP05` (= `exp3_3:T23`, `r3:argswap0490`), `cha2_1:CP07` (= `cha2_2:S05`, `exp3_3:T20`),
    `cha2_1:CP11` (= `cha2_2:S09`, `exp3_3:W752`, `r3:index0526`), `cha2_1:CP12`, `cha2_1:CP14`, `cha2_2:C23`
    (= `exp3_3:W032`), `exp3_1:own:W2`, `exp3_3:T24`.
  - In addition, every one of the 50 non-equivalent `exp3_3:W*` sweep survivors identified in `explorer_FU_D_r3_3` O5
    (`W037`, `W051`, `W076`, `W100`, `W123`, `W139`, `W166`, `W167`, `W196`, `W212`, `W351`, `W352`, `W365`, `W369`,
    `W413`, `W417`, `W419`, `W498`, `W560`, `W569`, `W601`, `W640`, `W643`, `W646`, `W658`–`W660`, `W662`, `W690`,
    `W697`–`W701`, `W703`, `W723`, `W725`–`W727`, `W737`–`W739`, `W746`, `W753`–`W757`) is **KILLED** in Leg A.

**Complete classification of all 164 surviving distinct mutants in `union_r3.out.json`.** Every survivor is accounted
for below (61 + 41 + 9 + 9 + 6 + 3 + 6 + 14 + 7 + 8 = 164); 0 change `verdict.json`, and 0 alter any decision category,
reason, or numeric output on any valid input.

| class (count) | distinct UIDs | why equivalent or decision-invariant |
|---|---|---|
| 1. Boolean tautology `(x == A) and x != B` with `A != B`, or duplicate conjunct (61) | `r3:conj0019`, `0021`–`0029` (10, `verdict.py:136` `cat == "keep"`); `r3:conj0053`–`0057`, `0059`–`0063` (10, `verdict.py:138` `st == "completed"`); `r3:conj0259`–`0263`, `0265`–`0269` (10, `records.py:131` `st == "completed"`); `r3:conj0271`–`0275`, `0277`–`0281` (10, `records.py:137` `st == "completed"`); `r3:conj0393` (1, `topic2fu_d_verdict.py:110` duplicates `fmst != "missing"`); `r3:conj0438`–`0442`, `0444`–`0448` (10, `topic2fu_d_verdict.py:80` `fst == "completed"`); `r3:conj0450`–`0454`, `0456`–`0460` (10, `topic2fu_d_verdict.py:104` `fmst == "completed"`) | If `x == A`, then `x != B` for any distinct literal `B` is identically `True`; repeating an existing conjunct `fmst != "missing"` is idempotent. |
| 2. Disjoint-domain `!=` conjunct (41) | `r3:conj0095`–`0101`, `0106`–`0112` (14, `verdict.py:96` `c2 != cat` conjoined with `c2 != L` or `cat != L` for `L` in `{"no_verdict", "completed", "missing", "failed", "failed_pending_rerun", "absent", "incomplete"}`); `r3:conj0303`–`0313` (11, `records.py:134` `sst != "COMPLETED"` conjoined with `sst != L` for lowercase `L`); `r3:conj0373`–`0377`, `0381`–`0383` (8, `topic2fu_d_verdict.py:66` `gst != L`); `r3:conj0387`–`0391`, `0395`–`0397` (8, `topic2fu_d_verdict.py:110` `fmst != L`) | `primary_category` returns only `{"stop", "keep", "modify", "inconclusive"}`, so `cat` and `c2` never take a run-state literal; `sst = str(...).upper()` is uppercase and never equals a lowercase literal; `group_state` returns only `{"completed", "failed", "missing"}` (mapping `"failed_pending_rerun"` to `"failed"`), so `gst` and `fmst` never take any of those 8 literals. |
| 3. `needs_fminus` conjunct / dummy-arg equivalence (9) | `wr2:S023`, `wr2:S025`, `rev2_1:R43` (= `exp3_2:revi2_1:R43`), `exp3_3:W105`, `exp3_3:W106`, `exp3_3:W107`, `exp3_3:W149`, `exp3_3:W184`, `exp3_3:W185` (`verdict.py:153–155`) | `needs_fminus` calls `decide(..., {"state": "missing", "nmse": None}, delta)`. When `fminus["state"]` is not `"completed"` or in `FAILED_STATES`, `fminus["nmse"]` is unread (`W149`, `W184`) and `"missing ~"` takes the same `else` branch (`W185`). On that call, `stage1.category == "keep"`, `verdict == "inconclusive"` with `reason.endswith("(keep pending F-)")`, and that suffix occur if and only if steps 1–7 yield `keep`. |
| 4. Unread `stage1` dict fields when Stage 1 is not `"completed"` (9) | `wr2:S181` (= `r3:cmp0525`), `exp3_3:W563`, `exp3_3:W564`, `exp3_3:W593`, `exp3_3:W594`, `exp3_3:W596`, `exp3_3:W677`, `exp3_3:W678`, `exp3_3:W751` (`topic2fu_d_verdict.py:83, 87`) | When Stage 1 is not completed, `decide()` checks only `stage1["state"] != "completed"` and returns `no_verdict` without reading `"nmse"` or `"stalled_seeds"`, and `stage1` is not written to `verdict.json`. Any non-`"completed"` state label (`"absent"`, `"incomplete"`, `"absent ~"`, `"incomplete ~"`) yields the identical output. |
| 5. Script token-order check subsumed by `validate_completed` (6) | `wr2:U075` (`Q19`), `wr2:S207`, `rev2_1:R36` (= `exp3_2:revi2_1:R36`), `exp3_3:W512`, `exp3_3:W522`, `exp3_3:W682` (`topic2fu_d_verdict.py:93–94`) | Reached only when all Stage-1 `hcp` records have `state == "completed"`; every completed record has passed `validate_completed`, which requires `test_pseudonyms == list(exp["test_tokens"])`, so `len(orders)` is always 1. |
| 6. Second completed attempt unreachable in `load_runs` (3) | `wr2:S160`, `exp3_3:W335`, `exp3_3:W342` (`records.py:138–139`) | Attempts are in `{0, 1}` and processed in sorted order; if attempt 0 completed and attempt 1 exists, line 127 raises `RecordError("rerun of a completed run")` before attempt 1 can reach `if chosen is not None:`. |
| 7. Stage-1 arm-length loop subset subsumed by `contrasts` (6) | `r3:member0012`–`0017` (`verdict.py:130` `for a in ("E", "C", "S"):` reduced to any non-empty subset) | Checking `len(stage1["nmse"][a]) != plan_n` on at least one arm together with `contrasts` on line 76 (`if not (len(e) == len(c) == len(s)): raise ValueError`) raises `ValueError` on the exact same inputs. |
| 8. Dead code, unreachable branch, commutative arg, or pinned-constant identity (14) | `wr2:U064` (`Q08`, dead `plan_n = 5` before `return`), `wr2:U077` (`Q21`, `failed_pending_rerun` always has `rec = None`), `rev2_1:R40` (r1 verdict is pinned `"stop"`), `aud2_1:P19_delta_in_out` (`K.DELTA == 0.01`), `exp3_3:W296` (`return None` → `pass` at end of function), `exp3_3:W373` (`len(parts) == 2` redundant on 2-column freeze receipt), `exp3_3:W376` (`not toks` caught on line 80 by `toks != list(exp["test_tokens"])`), `exp3_3:W499` (`return 0` → `pass` under `sys.exit(main())`), `exp3_3:W529` (`sys.path.insert(1, ROOT)`), `exp3_3:W644` (`seed=0` is already the frozen default of `hierarchical_bootstrap`), `exp3_3:W667` & `W709` (unread `"rec": None` in `missing` placeholder), `exp3_3:W671` (`all_possible_runs(plan_n)` tests `if plan_n:`, identical for `0` and `None`), `r3:argswap0319` (`max(1.0, abs(pooled))` is commutative) | Each produces identical control flow, return values, and `verdict.json` bytes on all valid inputs. |
| 9. `argparse` default / help-string equivalence (7) | `exp3_3:W542`–`W544`, `exp3_3:W623`, `r3:kwconst0400`–`0402` (`topic2fu_d_verdict.py:49–50`) | `default=None` is already `argparse`'s default (`W542`, `W543`); `default=0` (`kwconst0400`, `0401`) is falsy and treated identically by `a.out or ...` and `if exp.get("wrapper_sha256"):`; `--help` text (`W544`, `W623`, `kwconst0402`) never affects execution. |
| 10. Internal exception message text or stdout indentation only (8) | `exp3_3:W152`, `exp3_3:W193`, `exp3_3:W211`, `exp3_3:W235` (= `r3:index0163`), `r3:index0164`, `exp3_3:W664` (exception message string in `ValueError` / `AssertionError` / `SystemExit`); `exp3_3:W621`, `exp3_3:W702` (= `r3:kwconst0464`, `indent=1` dropped or changed to `indent=2` in stdout `print(json.dumps(...))`) | Exception types (`ValueError`, `AssertionError`, `SystemExit`) and exit codes are unchanged; the parsed stdout JSON object (`json.loads(stdout)`) and the written `verdict.json` file are 100 % identical. |

## 6. Integrity, C4 scan, and receipt verification

Run on 2026-11-02 after all r3 files and the union mutation run completed (logs and outputs in
`verification/worker_FU_D_r3/final/`):

| check | result |
|---|---|
| C1 protected hashes (`sentinel/PROTECTED_HASHES.txt`) | rc 0, 67/67 OK |
| FU-D receipts `card_sha256.txt` / `code_sha256_at_freeze.txt` / `output_sha256.txt` / `addendum_01_sha256.txt` | 1/1, 29/29, 34/34, 23/23 OK (all untouched) |
| New FU-D receipt `results/topic2/2026-11-02_fu_d/addendum_02_sha256.txt` | rc 0, all 102 pinned files OK |
| r1 receipts `code_sha256_at_freeze.txt` / `output_sha256_r2.txt` / `addendum_06_sha256.txt` | 33/33, 156/156, 31/31 OK |
| Shipped `results/topic2/2026-11-02_fu_d/verdict.json` | sha256 f6b295d9…59fc, unchanged; regenerates byte for byte into a temporary path |
| `tests/topic2_fu_d` (all 16 files, incl. the CPU E192 build and all 3 r3 files) | 389 passed (129 freeze + 66 r2 + 194 r3) |
| Old suite (`tests/test_empirical_four_topics.py tests/test_pilot_connectome.py tests/e2e`, `STRICT_E2E=1`) | 86 passed |
| `tests/topic2_rgpool` and `tests/topic1_lagmotif` (`CUDA_VISIBLE_DEVICES=`) | 204 passed (116 + 88) |
| FU-D C4 scan, frozen paths (`scripts/topic2fu_d_c4scan.py`) | 84 files, 0 token hits, 0 BIDS-label hits |
| C4 scan of r3 paths (`verification/worker_FU_D_r3/c4_scan_r3.py`, output `final/c4scan_r3.json`) | 0 token hits, 0 BIDS-label hits, 0 six-digit hits |
| Whole-run `audit_layout.py` | findings `[]` |

GPU used: 0 GPU-h (FU-D total remains 3.672 / 25 GPU-h). No B300 or connectome job was launched; no git write command
was run.
