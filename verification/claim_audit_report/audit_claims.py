#!/usr/bin/env python3
"""Adversarial claim and governance audit of 2026-11-02_FOUR_TOPICS_FINAL_REPORT.md.

Checks:
1. C1 protected hashes (67/67 OK).
2. Genre & Voice: Korean objective third-person report voice (zero occurrences of
   first-person pronouns/verbs 나는, 내가, 저는, 생각한다, 믿는다) and proper honorific
   손운규 교수님 (zero occurrences of 손운규 씨 or bare 손운규 without 교수님/교수).
3. Verdict Fidelity: every killed/stop and inconclusive verdict across all 10 milestones
   (M1, M3, FU_A, FU_B, FU_C, FU_D, FU_E, M2, M2H2, M4) matches its governing card and
   result JSONs, with zero reframing of killed results as partial success/trend/promising.
4. Card Rule & Structural Completeness (R1): 1-page executive summary table first, plus
   all 9 required subsections for each of the 4 topics.
5. Addenda & Victory Caveat Alignment:
   - M2 Addendum 03 §5 errata (+3.22, -3.28, effective ceiling <= 7, single outlier at L1)
   - M2H2 Addendum 08 §5 E1-E8 & victory_M2H2_r2 (C3 f<=0.5483, R1 -1.61 [-3.77, +0.56],
     L0 subject INC, untrained L2/L3 pr_cov 31.0-34.0)
   - M3 Addendum 06 (V01-V11, E1-E5 F+ failure card-vs-code erratum)
   - FU_B Addendum 01 (v2 card re-freeze before run start)
   - FU_C Addendum 01-03 (C4 retired test literal sealed, 7-seed SD 0.220% / half-width 0.204%)
   - FU_D Addendum 01-02 (E1-E9, W1-W5, algebraic proof P1)
   - FU_E result report & card (S_s2 F+ failure 5.76 <= 10.59, counterfactual J1 +8.11% [-6.60%, +22.81%] still inconclusive, age/sex untestable at delta=0.01)
   - M4 result report, addendum_01, and victory_M4 caveats
6. C4 Participant-ID Hygiene & C8 Forbidden Source Check:
   - Zero BIDS subject prefixes, 6-digit HCP IDs, ENIGMA IDs, or unsalted 16-hex tokens
   - Zero citations of EMPIRICAL_ANALYSIS_REPORT.md or 2026-11-01_FOUR_TOPICS_CONSOLIDATED_STATUS.md as results.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path("/home/juke/git/00IITP-AI")
REPORT_PATH = ROOT / "docs/03_empirical_analysis/2026-11-02_FOUR_TOPICS_FINAL_REPORT.md"
PROTECTED_HASHES = ROOT / ".agents/teamwork/tw-20261031-four-topics/sentinel/PROTECTED_HASHES.txt"
OUT_JSON = ROOT / "verification/claim_audit_report/audit_claims.out.json"
OUT_JSON_R2 = ROOT / "verification/claim_audit_report/audit_claims_r2.out.json"


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check_c1_protected_hashes() -> dict:
    proc = subprocess.run(
        ["sha256sum", "-c", str(PROTECTED_HASHES)],
        cwd=str(ROOT),
        env={"LC_ALL": "C", "PATH": "/usr/bin:/bin"},
        capture_output=True,
        text=True,
        check=False,
    )
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    ok_count = sum(1 for ln in lines if ln.endswith(": OK"))
    return {
        "rc": proc.returncode,
        "total_lines": len(lines),
        "ok_count": ok_count,
        "pass": proc.returncode == 0 and ok_count == 67,
        "stderr": proc.stderr.strip(),
    }


def check_genre_and_voice(text: str) -> dict:
    forbidden_first_person = [
        (r"(?<![가-힣])나는(?![가-힣])", "나는"),
        (r"(?<![가-힣])내가(?![가-힣])", "내가"),
        (r"(?<![가-힣])저는(?![가-힣])", "저는"),
        (r"(?<![가-힣])제가(?![가-힣])", "제가"),
        (r"(?<![가-힣])우리의(?![가-힣])", "우리의"),
        (r"생각한다", "생각한다"),
        (r"믿는다", "믿는다"),
    ]
    # Remove literal meta-mentions where the report quotes the rule if any, though none should exist
    hits = {}
    for pat, label in forbidden_first_person:
        matches = list(re.finditer(pat, text))
        hits[label] = len(matches)

    honorific_hits = len(re.findall(r"손운규\s*교수님", text))
    improper_honorific = len(re.findall(r"손운규\s*씨", text))
    bare_name = len(re.findall(r"손운규(?!\s*교수님)", text))

    return {
        "forbidden_first_person_hits": hits,
        "total_forbidden_voice_hits": sum(hits.values()),
        "son_professor_honorific_count": honorific_hits,
        "improper_honorific_count": improper_honorific,
        "bare_name_without_honorific_count": bare_name,
        "pass": sum(hits.values()) == 0 and honorific_hits >= 1 and improper_honorific == 0 and bare_name == 0,
    }


def check_verdict_fidelity(text: str) -> dict:
    # Load canonical JSON verdicts to cross-verify exact alignment
    m1_stats = json.loads((ROOT / "results/topic1/2026-10-31/stats_results.json").read_text())
    m3_verdict = json.loads((ROOT / "results/topic2/2026-11-01/verdict.json").read_text())
    fua_verdict = json.loads((ROOT / "results/topic2/2026-11-02_fu_a/verdict.json").read_text())
    fub_verdict = json.loads((ROOT / "results/topic2/2026-11-02_fu_b/verdict.json").read_text())
    fuc_verdict = json.loads((ROOT / "results/topic2/2026-11-02_fu_c/verdict.json").read_text())
    fud_verdict = json.loads((ROOT / "results/topic2/2026-11-02_fu_d/verdict.json").read_text())
    fue_verdict = json.loads((ROOT / "results/topic2/2026-11-02_fu_e/verdict.json").read_text())
    m2_famA = json.loads((ROOT / "results/topic3/2026-10-31/family_A_subject_level.json").read_text())
    m2_famB = json.loads((ROOT / "results/topic3/2026-10-31/family_B_token_level.json").read_text())
    m2h2_gate = json.loads((ROOT / "results/topic3/2026-11-02_h2/gate/gate_decision.json").read_text())
    m2h2_res = json.loads((ROOT / "results/topic3/2026-11-02_h2/h2_results.json").read_text())
    m4_verdict = json.loads((ROOT / "results/topic4/2026-11-01/verdict.json").read_text())

    checks = {
        "M1_killed": (
            m1_stats["primary"]["decision"]["topic1_killed"] is True
            and 'Topic 1 KILLED (neither endpoint survives)' in text
            and "survives = false" in text
        ),
        "M3_stop": (
            m3_verdict["verdict"]["verdict"] == "stop"
            and "**`stop` (killed)**" in text
            and "+0.361%" in text
        ),
        "FU_A_inconclusive": (
            fua_verdict["verdict"] == "inconclusive"
            and "**`inconclusive` (measurement capacity)**" in text
            and "+0.5511%" in text
        ),
        "FU_B_stop": (
            fub_verdict["verdict"]["verdict"] == "stop"
            and "+0.425%" in text
        ),
        "FU_C_stop": (
            fuc_verdict["verdict"]["verdict"] == "stop"
            and "+0.272%" in text
        ),
        "FU_D_inconclusive": (
            fud_verdict["decision"]["verdict"] == "inconclusive"
            and "+0.3631%" in text
            and "+0.6546%" in text
        ),
        "FU_E_inconclusive": (
            fue_verdict["verdict"]["verdict"] == "inconclusive"
            and "5.76" in text
            and "10.59" in text
            and "+8.11%" in text
        ),
        "M2_verdicts": (
            "`J1` FAILS (`stop`)" in text
            and "`R1` 기술통계 전용 (`inconclusive`)" in text
            and "`D1` HOLDS (`keep`)" in text
            and "`H1a` 역방향(`L3>LN0(L2)`) HOLDS" in text
            and "`H1b` 미재현" in text
            and "`R4, R6` NOT SUPPORTED (`stop`)" in text
            and "`R5` UNTESTABLE" in text
        ),
        "M2H2_verdicts": (
            m2h2_gate["gate_verdict"] == "PASS"
            and m2h2_res["family_C"]["C1"]["label"] == "INC"
            and m2h2_res["family_C"]["C2"]["label"] == "INC"
            and m2h2_res["family_C"]["C3"]["label"] == "TE+"
            and m2h2_res["family_C"]["C4"]["label"] == "TE+"
            and "`C1` (`H1a` DiD): `INC` (`inconclusive`)" in text
            and "`C2` (`H1b` DiD): `INC` (`inconclusive`)" in text
            and "`C3` (`D1` cov DiD): `TE+` (`keep`)" in text
            and "`C4` (`D1` corr DiD): `TE+` (`keep`)" in text
        ),
        "M4_verdicts": (
            m4_verdict["H1_C4_minus_C1"]["verdict"] == "stop"
            and m4_verdict["S1_C4_minus_C4DP"]["verdict"] == "killed"
            and m4_verdict["S2_C5_minus_randomlinear24"]["verdict"] == "supported"
            and m4_verdict["S3_C5_minus_MLPenc"]["verdict"] == "non-inferior"
            and "`H1` (`C4 - C1`): `stop` (killed)" in text
            and "`S1` (`C4 - C4DP`): `killed`" in text
            and "`S2` (`C5 - randlin24`): `supported`" in text
            and "`S3` (`C5 - MLPenc`): `non-inferior`" in text
            and "`inconclusive (execution integrity)`" in text
        ),
    }

    # Check for forbidden spin / overclaim phrases on killed results
    spin_patterns = [
        r"부분적\s*성공",
        r"유망한\s*신호",
        r"경향성\s*확인",
        r"긍정적\s*경향",
        r"잠재적\s*이득을\s*입증",
        r"가설을\s*지지",
    ]
    spin_hits = {}
    for pat in spin_patterns:
        spin_hits[pat] = len(re.findall(pat, text))

    return {
        "milestone_verdict_checks": checks,
        "all_milestone_verdicts_match": all(checks.values()),
        "spin_phrase_hits": spin_hits,
        "zero_spin_phrases": sum(spin_hits.values()) == 0,
        "pass": all(checks.values()) and sum(spin_hits.values()) == 0,
    }


def check_structure_and_completeness(text: str) -> dict:
    required_headings = [
        "## 1. 1페이지 총괄 요약표 (Executive Summary Table)",
        "## 2. Topic 1 (`M1`):",
        "### 2.1 연구 질문",
        "### 2.2 사전 동결 분석 카드 및 판정·기각 규칙",
        "### 2.3 데이터셋, 표본 구성 및 연산 자원",
        "### 2.4 사전 등록 규칙에 따른 최종 판정",
        "### 2.5 핵심 실증 수치 및 신뢰구간",
        "### 2.6 5인 검증 게이트 및 독립 승리 감사 상태",
        "### 2.7 일탈 사항 및 부록(Addenda) 정오표",
        "### 2.8 미검증 항목 및 후속 연구 요구 조건",
        "## 3. Topic 2 (`M3` 및 후속 `FU-A`~`FU-E`):",
        "### 3.1 연구 질문",
        "### 3.2 사전 동결 분석 카드 및 판정·기각 규칙",
        "### 3.3 데이터셋, 표본 구성, C4 비식별화 및 연산 자원",
        "### 3.4 사전 등록 규칙에 따른 최종 판정",
        "### 3.5 핵심 실증 수치 및 신뢰구간",
        "### 3.6 5인 검증 게이트 및 독립 승리 감사 상태",
        "### 3.7 일탈 사항 및 부록(Addenda) 정오표",
        "### 3.8 미검증 항목 및 후속 연구 요구 조건",
        "## 4. Topic 3 (`M2` 및 `M2H2`):",
        "### 4.1 연구 질문",
        "### 4.2 사전 동결 분석 카드 및 판정·기각 규칙",
        "### 4.3 데이터셋, 표본 구성 및 연산 자원",
        "### 4.4 사전 등록 규칙에 따른 최종 판정",
        "### 4.5 핵심 실증 수치 및 신뢰구간",
        "### 4.6 5인 검증 게이트 및 독립 승리 감사 상태",
        "### 4.7 일탈 사항 및 부록(Addenda) 정오표",
        "### 4.8 미검증 항목 및 후속 연구 요구 조건",
        "## 5. Topic 4 (`M4`):",
        "### 5.1 연구 질문",
        "### 5.2 사전 동결 분석 카드 및 판정·기각 규칙",
        "### 5.3 데이터셋, 표본 구성 및 연산 자원",
        "### 5.4 사전 등록 규칙에 따른 최종 판정",
        "### 5.5 핵심 실증 수치 및 신뢰구간",
        "### 5.6 5인 검증 게이트 및 독립 승리 감사 상태",
        "### 5.7 일탈 사항 및 부록(Addenda) 정오표",
        "### 5.8 미검증 항목 및 후속 연구 요구 조건",
        "## 6. 전체 실행 연산 자원 원장(GPU Ledger) 및 거버넌스 감사 요약",
    ]
    missing = [h for h in required_headings if h not in text]
    return {
        "required_headings_count": len(required_headings),
        "missing_headings": missing,
        "pass": len(missing) == 0,
    }


def check_addenda_and_caveats(text: str) -> dict:
    checks = {
        "M2_addendum03_D1_cov_lo_3_22": "+3.22, +7.46" in text and "+3.23 -> +3.22" in text,
        "M2_addendum03_A1b_L5e5_neg_3_28": "-3.284892" in text and "-3.29 -> -3.28" in text,
        "M2_addendum03_effective_ceiling_7_and_L1_LOO": "유효 상한" in text and "6.3898" in text and "0.1488" in text,
        "M2H2_addendum08_E1_C3_f_0_5483": "0.5483" in text,
        "M2H2_addendum08_E2_R1_descriptive_interval": "-1.61 [-3.77, +0.56]" in text,
        "M2H2_addendum08_E3_L0_subject_INC": "`L0_cov`(`-0.061 [-0.330, +0.208]`)" in text and "부록 08 `E3`" in text,
        "M2H2_victory_untrained_pr_cov_31_0_to_34_0": "31.0–34.0" in text and "30.9530" in text,
        "M3_addendum06_V01_V11_and_E1_Fplus": "E1–E5" in text and "no_verdict" in text and "card_reading" in text,
        "FU_C_addendum01_03_disclosures": "0.220%" in text and "0.204%" in text and "topic2fu_c_verdict_r2.py" in text,
        "FU_D_addendum01_02_E1_E9_W1_W5_P1": "E1–E9" in text and "W1–W5" in text and "P1" in text,
        "FU_E_counterfactual_J1_and_S_s2": "+8.11%" in text and "[-6.60%, +22.81%]" in text and "S_s2" in text,
        "R2_fix_BLOCKING1_M1_log_ratio_means": "-0.2020" in text and "-0.2224" in text,
        "R2_fix_BLOCKING2_M2_colperm_null_means": "45.43" in text and "50.07" in text and "53.76" in text and "53.21" in text,
        "R2_fix_BLOCKING3_M2_D3_m12_covPR": "4.395" in text and "6.479" in text and "7.758" in text and "1.47\\times, 1.77\\times" in text,
        "R2_fix_BLOCKING4_M2H2_FamilyL_subject": "17.61–20.87" in text and "-1.424 [-2.441, -0.407]" in text and "-1.839 [-2.087, -1.591]" in text,
        "R2_fix_BLOCKING4_M2H2_FamilyL_token": (
            "`2 TE-`, `4 EQ`, `4 INC`" in text
            and "-0.0556 [-0.0634, -0.0465]" in text
            and "-0.0091 [-0.0161, -0.0013]" in text
            and "0.1057" in text
        ),
        "R2_fix_M4_addendum01_and_victory_caveat7": "2026-11-01_topic4_addendum_01.md" in text and "refit_on_val=True" in text and "test_vendored_source_hashes_recorded" in text,
        "R2_fix_M4_package_and_test_paths": "src/topic4_resu/psp_engine.py" in text and "tests/topic4_resu" in text,
    }
    return {
        "checks": checks,
        "pass": all(checks.values()),
    }


def check_c4_and_c8_hygiene(text: str) -> dict:
    # 1. BIDS subject prefix check: literal 's' + 'u' + 'b' + '-' followed by alphanumeric
    bids_pat = re.compile("s" + "u" + "b" + r"-[A-Za-z0-9]")
    bids_hits = [m.group(0) for m in bids_pat.finditer(text)]

    # 2. Standalone 6-digit numbers with leading 1-9 not part of decimal fraction, comma-formatted integer, or hex hash
    six_digit_matches = []
    for m in re.finditer(r"(?<![0-9a-fA-F.,])[1-9][0-9]{5}(?![0-9a-fA-F])", text):
        start, end = m.span()
        ctx = text[max(0, start - 25) : min(len(text), end + 25)].replace("\n", " ")
        six_digit_matches.append({"token": m.group(0), "context": ctx})

    # Allowed known scientific quantities (560000 samples, and connectome Slurm job IDs 217845, 218004, 218007, 218041, 218063, 218064, 218065, 218069, 218072)
    allowed_six_digits = {
        "560000",
        "217845",
        "218004",
        "218007",
        "218041",
        "218063",
        "218064",
        "218065",
        "218069",
        "218072",
    }
    unexpected_six_digits = [x for x in six_digit_matches if x["token"] not in allowed_six_digits]

    # 3. Standalone 16-hex token check (not part of 64-hex SHA256 or 8-hex...4-hex abbreviated SHA)
    hex16_matches = []
    for m in re.finditer(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", text):
        val = m.group(0)
        if any(c in val for c in "abcdef"):
            hex16_matches.append(val)

    # 4. C8 check: EMPIRICAL_ANALYSIS_REPORT.md and 2026-11-01_FOUR_TOPICS_CONSOLIDATED_STATUS.md
    # Only allowed in the governance disclaimer on line 6 stating they are NOT cited
    c8_mentions = []
    for i, line in enumerate(text.splitlines(), 1):
        if "EMPIRICAL_ANALYSIS_REPORT.md" in line or "2026-11-01_FOUR_TOPICS_CONSOLIDATED_STATUS.md" in line:
            c8_mentions.append({"line": i, "text": line})

    return {
        "bids_prefix_hits": bids_hits,
        "six_digit_tokens": six_digit_matches,
        "unexpected_six_digit_tokens": unexpected_six_digits,
        "hex16_tokens": hex16_matches,
        "c8_mentions": c8_mentions,
        "pass": (
            len(bids_hits) == 0
            and len(unexpected_six_digits) == 0
            and len(hex16_matches) == 0
            and len(c8_mentions) == 1
            and c8_mentions[0]["line"] == 6
        ),
    }


def main() -> int:
    text = REPORT_PATH.read_text(encoding="utf-8")
    report_sha = sha256_file(REPORT_PATH)

    c1 = check_c1_protected_hashes()
    voice = check_genre_and_voice(text)
    verdicts = check_verdict_fidelity(text)
    structure = check_structure_and_completeness(text)
    addenda = check_addenda_and_caveats(text)
    hygiene = check_c4_and_c8_hygiene(text)

    out = {
        "report_path": str(REPORT_PATH),
        "report_sha256": report_sha,
        "report_lines": len(text.splitlines()),
        "report_bytes": len(text.encode("utf-8")),
        "c1_protected_hashes": c1,
        "genre_and_voice": voice,
        "verdict_fidelity": verdicts,
        "structure_and_completeness": structure,
        "addenda_and_caveats": addenda,
        "c4_and_c8_hygiene": hygiene,
        "all_automated_checks_pass": all([
            c1["pass"],
            voice["pass"],
            verdicts["pass"],
            structure["pass"],
            addenda["pass"],
            hygiene["pass"],
        ]),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    OUT_JSON.write_text(payload, encoding="utf-8")
    OUT_JSON_R2.write_text(payload, encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out["all_automated_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
