# PI decisions — run tw-20261031-four-topics, 2026-11-01 ~11:2x KST (human answers to root's questions, verbatim labels)

1. M2 (Topic 3) iteration 3 after the r2b gate failure: "3회차 진행 (권장)" — additive guard tests + addendum_05, no src/scripts change, no rerun; 5-verifier gate, then victory audit.
2. M3 (Topic 2) data under C6: "포함한다 (권장)" — HCP-YA Open Access (staged on B300 .98) counts as a public dataset for this run, subject to the HCP Data Use Terms (no redistribution, no re-identification).
3. δ (minimum practically meaningful effect): "둘 다 1% / 0.01 (권장)" — M4 keeps its frozen card value δ = 0.01; M3 freezes δ = 1% (relative, held-out masked NMSE).
4. M1 (Topic 1) deviation (card §12 independent review of the stats script was not done before execution; only post-execution reviews): "승인 (권장)" — accepted and recorded; M1 closed as VERIFIED_COMPLETE with this deviation.

5. (2026-11-01 ~14:3x KST, human message verbatim) "enigma 자료도 b300 사용 가능하다" — C6 is relaxed by the PI: ENIGMA-OCD data may be used on B300. Consequences recorded by root: the ENIGMA copies in ~/enigma_ocd/data on the four B300 nodes are not a C6 violation; verifiers must not treat ENIGMA data or ENIGMA-derived files on B300 as an integrity violation. Running work is not moved: M4 stays on local CPU (frozen card, run in progress, no GPU needed).
