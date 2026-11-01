# FU-B addendum 01: one-word wording fix in the card before any FU-B run started (re-freeze v2)

Date: 2026-11-01 ~16:2x UTC. Author: worker_FU_B_r1. Governs: `2026-11-02_topic2_fu_b_card.md`.

## What happened

- The card was frozen at 2026-11-01T16:05:18Z (receipt `results/topic2/2026-11-02_fu_b/card_sha256.txt`, card sha256 `a9c4cab0…0726`; that receipt is kept unchanged, read-only).
- At 16:1x UTC the frozen r1 C4 test `tests/topic2_rgpool/test_outputs_no_ids.py::test_outputs_have_no_id_bearing_paths_and_only_manifest_pseudonyms` failed. Its BIDS-label detector (a lowercase "sub" followed by a hyphen and an alphanumeric character) scans `docs/03_empirical_analysis/topic2/` and matched the ordinary English word in §2 of the card ("…the r1 recipe may be [that word] at 4×…"). It is not an identifier, but the frozen test must stay green and cannot be edited.
- **No FU-B run had started.** `TZ=UTC sacct -j 509,516` at 2026-11-01T16:19:52Z: gate array 509 PENDING (QOSMaxGRESPerUser), Stage-1 array 516 PENDING (Dependency), Start = Unknown, ElapsedRaw 0. The only FU-B GPU use so far is the pre-freeze smoke (job 490, no FU-B outcome).

## Change (the only one)

§2, "Learning-rate handling": "may be [hyphenated word] at 4×" → "may not be optimal at 4×". No rule, number, threshold, design element or reading changes.

- v1 card bytes preserved: `verification/worker_FU_B_r1/card_v1_frozen_20261101T160518Z.md.txt` (sha256 `a9c4cab03ac99305e44b0aa2ab550fbe402f7f4b74ac3c239d082021e76e0726`, identical to the v1 receipt).
- `diff` v1 → v2: exactly one line (line 41) differs, by that phrase.
- v2 card sha256 `994f01446d35b706de899ef00af1ce65db8c55c45da7891f4011f17485c4daae`, recorded with all other v1 entries (unchanged) in `results/topic2/2026-11-02_fu_b/card_sha256_v2.txt`, written before any FU-B task started.

## Effect

None on the design or on any result (none exists). The card governs from v2; the v1 receipt documents the first freeze time. Future documents in FU-B paths avoid that hyphenated prefix.
