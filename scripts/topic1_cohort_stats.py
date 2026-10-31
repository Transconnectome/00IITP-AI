#!/usr/bin/env python3
"""Topic 1 cohort statistics: frozen card 2026-10-30 sections 3-7, implemented exactly.

Governing documents (read-only):
  docs/03_empirical_analysis/topic1/2026-10-30_topic1_analysis_card.md      sha256 1e589f0b...75aa (frozen)
  docs/03_empirical_analysis/topic1/2026-10-31_topic1_prelabel_addendum.md  (settles gaps the card leaves open)

Card rules implemented here
  * Primary model (card 4): dx (1 = OCD, 0 = HC) + age + C(sex) + log(duration_s) + site.
      - site-FE OLS t for dx; two-sided Freedman-Lane permutation p (reduced-model residuals permuted WITHIN
        site, B = 9,999, seed 20261031, p = (1 + #{|t*| >= |t|}) / (B + 1));
      - MixedLM (ML, site random intercept) with Mundlak site means of dx, age, sex, log duration;
        stop for review unless |beta_LMM - beta_FE| < 0.01 * SE_FE;
      - d = beta_LMM / sqrt(level-1 residual variance of that MixedLM) (sign OCD - HC);
      - LMM Wald p secondary; raw pooled Cohen d and Welch p DESCRIPTIVE ONLY.
  * Decision (card 5): Holm over exactly E1 = Z030C and E2 = Z030C - Z030T; an endpoint survives iff
    p_Holm < 0.05 AND |d| >= 0.15; Topic 1 is killed iff neither survives.
  * Degeneracy fallback (card 3): if > 10 % of subjects are degenerate for E1 or for E2 at density 0.10,
    the primary density becomes 0.15 and 0.10 is reported as a sensitivity.
  * Secondary families (card 6), BH-FDR within family: (1) site-held-out classification (descriptive,
    no p-value), (2) Y-BOCS within OCD, (3) medication code 1 vs code 2 within OCD.
  * Sensitivity analyses (card 7) for surviving endpoints only.

Subcommands
  validate   synthetic outcomes on the REAL design (site x dx x age x sex x log-duration structure;
             no imaging feature is read) -> validation.json
  decide     label-free degeneracy-fallback decision from the primary extraction -> fallback_decision.json
  analyze    real-label primary + secondary analysis; refuses to run unless this file's sha256 equals the
             value recorded in results/topic1/2026-10-31/stats_script_sha256.txt
  sensitivity  card 7 analyses for surviving endpoints (needs the variant extraction files)

No participant ID is printed or written: subjects are positional indices (manifest order).
"""
from __future__ import annotations

import os

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENIGMA = "/home/juke/git/enigma_ocd_mbbn"
NPY_DIR = os.path.join(ENIGMA, "data", "MBBN_data_304_ROIs_0.25")
META = os.path.join(ENIGMA, "data", "metadata", "ENIGMA_QC_final_subject_list.csv")
OUTDIR_DEFAULT = os.path.join(ROOT, "results", "topic1", "2026-10-31")

ALPHA = 0.05
D_MIN = 0.15
B_PERM = 9999
SEED_PERM = 20261031
SEED_BOOT = 20261032
N_BOOT = 2000
FALLBACK_RATE = 0.10
DENSITY_PRIMARY = 0.10
DENSITY_FALLBACK = 0.15
STOP_TOL_SE = 0.01
ENDPOINTS = ("E1", "E2")
CLASSES = ("021D", "021U", "021C", "030T", "030C")


class StopForReview(RuntimeError):
    """A card stop rule fired (e.g. Mundlak equality failed, rank-deficient design)."""


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ============================================================================================ design
def rank_guard(Zm: np.ndarray, label: str) -> None:
    """QR rank guard (addendum P4): full column rank required, else stop."""
    r = np.linalg.matrix_rank(Zm)
    if r < Zm.shape[1]:
        raise StopForReview(f"{label}: design rank {r} < {Zm.shape[1]} columns")


def nuisance_matrix(age, sex2, logdur, site_codes, extra=None, include_logdur: bool = True) -> np.ndarray:
    """Columns: one dummy per site (absorbs the intercept and TR), age, sex (code 2 indicator), log duration,
    then optional extra covariates (e.g. gradient share).  dx is NEVER part of this matrix."""
    site_codes = np.asarray(site_codes)
    levels = np.unique(site_codes)
    D = (site_codes[:, None] == levels[None, :]).astype(float)
    cols = [D, np.asarray(age, float)[:, None], np.asarray(sex2, float)[:, None]]
    if include_logdur:   # dropped only for the common-200 s truncation row (duration constant within site there)
        cols.append(np.asarray(logdur, float)[:, None])
    if extra is not None:
        cols.append(np.asarray(extra, float).reshape(len(site_codes), -1))
    return np.hstack(cols)


def within_site_permutations(site_codes, B: int, rng: np.random.Generator) -> np.ndarray:
    """B x n index array; each row permutes indices only within each site (exchangeability blocks)."""
    site_codes = np.asarray(site_codes)
    n = site_codes.size
    P = np.empty((B, n), dtype=np.int64)
    for s in np.unique(site_codes):
        g = np.flatnonzero(site_codes == s)
        keys = rng.random((B, g.size))
        P[:, g] = g[np.argsort(keys, axis=1)]
    return P


class FreedmanLane:
    """Vectorised Freedman-Lane test for the coefficient of ``x`` in y ~ x + Z (Z = nuisance incl. site FE).

    Algorithm (Freedman & Lane 1983; Winkler et al. 2014, Table 2):
      1. fit the reduced model y ~ Z: fitted yhat_r, residuals e_r = M_Z y;
      2. for each permutation P (within site): y* = yhat_r + P e_r;
      3. refit the full model y* ~ x + Z and take the OLS t of x.
    Because M_Z yhat_r = 0, the t of x in step 3 depends on y* only through M_Z P e_r, which this class
    evaluates for all permutations at once (exact, no approximation)."""

    def __init__(self, x, Z):
        x = np.asarray(x, float)
        Z = np.asarray(Z, float)
        rank_guard(np.column_stack([x, Z]), "full model")
        self.n = x.size
        self.Q, _ = np.linalg.qr(Z)
        self.xt = x - self.Q @ (self.Q.T @ x)
        self.sxx = float(self.xt @ self.xt)
        self.dfres = self.n - Z.shape[1] - 1
        if self.sxx <= 1e-12 * max(1.0, float(x @ x)):
            raise StopForReview("tested regressor is (numerically) in the nuisance column space")

    def _t(self, V):
        num = self.xt @ V
        QtV = self.Q.T @ V
        ss = np.einsum("ij,ij->j", V, V) - np.einsum("ij,ij->j", QtV, QtV)
        rss = ss - num ** 2 / self.sxx
        return (num / self.sxx) / np.sqrt(rss / self.dfres / self.sxx)

    def reduced_residuals(self, y):
        y = np.asarray(y, float)
        return y - self.Q @ (self.Q.T @ y)

    def t_obs(self, y) -> float:
        return float(self._t(self.reduced_residuals(y)[:, None])[0])

    def t_perm(self, y, P, chunk: int = 2000) -> np.ndarray:
        e = self.reduced_residuals(y)
        out = np.empty(P.shape[0])
        for a in range(0, P.shape[0], chunk):
            out[a:a + chunk] = self._t(e[P[a:a + chunk]].T)
        return out

    def test(self, y, P) -> dict:
        t0 = self.t_obs(y)
        tb = self.t_perm(y, P)
        p = (1.0 + float(np.sum(np.abs(tb) >= abs(t0)))) / (P.shape[0] + 1.0)
        return {"t": t0, "p_fl": p, "B": int(P.shape[0])}


def fe_ols(y, x, Z) -> dict:
    """Site-FE OLS coefficient of x with classical SE (the model whose t Freedman-Lane permutes)."""
    X = np.column_stack([np.asarray(x, float), np.asarray(Z, float)])
    beta, *_ = np.linalg.lstsq(X, np.asarray(y, float), rcond=None)
    resid = y - X @ beta
    dfres = X.shape[0] - X.shape[1]
    s2 = float(resid @ resid) / dfres
    XtX_inv = np.linalg.inv(X.T @ X)
    se = math.sqrt(s2 * XtX_inv[0, 0])
    return {"beta": float(beta[0]), "se": se, "t": float(beta[0] / se), "sigma": math.sqrt(s2), "df": dfres}


def mixedlm_mundlak(y, dx, age, sex2, logdur, site_codes, mundlak: bool = True,
                    include_logdur: bool = True, extra=None) -> dict:
    """statsmodels MixedLM, ML (reml=False), default optimizer, site random intercept, with Mundlak site means
    of every within-site regressor.  Warnings are recorded, never turned into errors (addendum P5)."""
    import statsmodels.formula.api as smf
    d = pd.DataFrame({"y": np.asarray(y, float), "dx": np.asarray(dx, float), "age": np.asarray(age, float),
                      "sex2": np.asarray(sex2, float), "logdur": np.asarray(logdur, float),
                      "site": np.asarray(site_codes)})
    covs = ("dx", "age", "sex2", "logdur") if include_logdur else ("dx", "age", "sex2")
    if extra is not None:   # e.g. gradient share (card 7); gets its own Mundlak site mean like every regressor
        ex = np.asarray(extra, float).reshape(len(d), -1)
        for j in range(ex.shape[1]):
            d[f"x{j}"] = ex[:, j]
        covs = covs + tuple(f"x{j}" for j in range(ex.shape[1]))
    rhs = " + ".join(covs)
    if mundlak:
        for c in covs:
            d["m_" + c] = d.groupby("site")[c].transform("mean")
        rhs += " + " + " + ".join("m_" + c for c in covs)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        res = smf.mixedlm("y ~ " + rhs, d, groups=d["site"]).fit(reml=False)
    mle = getattr(res, "mle_retvals", None) or {}
    return {"beta": float(res.params["dx"]), "se_wald": float(res.bse["dx"]), "p_wald": float(res.pvalues["dx"]),
            "scale": float(res.scale), "re_var": float(np.asarray(res.cov_re)[0, 0]),
            "converged": bool(res.converged), "n_warnings": len(w),
            "warning_kinds": sorted({f"{x.category.__name__}: {str(x.message)[:90]}" for x in w}),
            "mle_retvals": {k: (v if isinstance(v, (bool, int, float, str)) else str(v))
                            for k, v in mle.items() if k in ("converged", "iterations", "warnflag")}}


def descriptive_raw(y, dx) -> dict:
    """Raw pooled Cohen d and Welch p: DESCRIPTIVE ONLY (miscalibrated under site x dx imbalance)."""
    y = np.asarray(y, float)
    dx = np.asarray(dx)
    a, b = y[dx == 1], y[dx == 0]
    sp = math.sqrt(((a.size - 1) * a.var(ddof=1) + (b.size - 1) * b.var(ddof=1)) / (a.size + b.size - 2))
    return {"raw_cohen_d_DESCRIPTIVE": float((a.mean() - b.mean()) / sp),
            "welch_p_DESCRIPTIVE": float(stats.ttest_ind(a, b, equal_var=False).pvalue),
            "mean_ocd": float(a.mean()), "mean_hc": float(b.mean()), "sd_ocd": float(a.std(ddof=1)),
            "sd_hc": float(b.std(ddof=1)), "n_ocd": int(a.size), "n_hc": int(b.size)}


def dx_effect(y, D: pd.DataFrame, B: int = B_PERM, seed: int = SEED_PERM, extra=None, mundlak: bool = True,
              include_logdur: bool = True,
              with_lmm: bool = True) -> dict:
    """Card section 4 primary model for one outcome vector aligned with design frame D
    (columns dx, age, sex2, logdur, site).  A fresh default_rng(seed) per analysis (addendum P3)."""
    y = np.asarray(y, float)
    if not np.all(np.isfinite(y)):
        raise ValueError("outcome has non-finite entries; complete cases must be selected before")
    Zn = nuisance_matrix(D["age"], D["sex2"], D["logdur"], D["site"], extra=extra, include_logdur=include_logdur)
    fl = FreedmanLane(D["dx"].values, Zn)
    P = within_site_permutations(D["site"].values, B, np.random.default_rng(seed))
    flr = fl.test(y, P)
    fe = fe_ols(y, D["dx"].values, Zn)
    out = {"n": int(y.size), "n_ocd": int(D["dx"].sum()), "n_hc": int((1 - D["dx"]).sum()),
           "n_sites": int(D["site"].nunique()), "beta_fe": fe["beta"], "se_fe": fe["se"], "t_fe": fe["t"],
           "d_fe": fe["beta"] / fe["sigma"], "t_fl": flr["t"], "p_fl": flr["p_fl"], "B": flr["B"],
           "perm_seed": seed, "include_logdur": include_logdur}
    if with_lmm:
        lm = mixedlm_mundlak(y, D["dx"], D["age"], D["sex2"], D["logdur"], D["site"], mundlak=mundlak,
                             include_logdur=include_logdur, extra=extra)
        out.update({"beta_lmm": lm["beta"], "se_lmm_wald": lm["se_wald"], "p_lmm_wald_secondary": lm["p_wald"],
                    "sigma_eps_lmm": math.sqrt(lm["scale"]), "re_var_site": lm["re_var"],
                    "d": lm["beta"] / math.sqrt(lm["scale"]), "lmm_converged_flag": lm["converged"],
                    "lmm_n_warnings": lm["n_warnings"], "lmm_warning_kinds": lm["warning_kinds"],
                    "lmm_mle_retvals": lm["mle_retvals"],
                    "scale_ratio_lmm_over_fe": lm["scale"] / fe["sigma"] ** 2,
                    "mundlak_equality_ratio": abs(lm["beta"] - fe["beta"]) / fe["se"], "mundlak": mundlak})
        if mundlak and not out["mundlak_equality_ratio"] < STOP_TOL_SE:
            raise StopForReview(f"|beta_LMM - beta_FE| = {out['mundlak_equality_ratio']:.3g} SE >= {STOP_TOL_SE} SE")
    else:
        out["d"] = out["d_fe"]   # only for sensitivity rows where the card's LMM is not refitted (labelled)
        out["d_source"] = "FE OLS sigma (no LMM in this row)"
    out.update(descriptive_raw(y, D["dx"].values))
    return out


def assoc_effect(y, x, D: pd.DataFrame, B: int = B_PERM, seed: int = SEED_PERM) -> dict:
    """y ~ x + age + sex + log duration + C(site) (secondary families 2 and 3): OLS beta of x, FL p within site,
    standardized beta = beta * SD(x) / SD(y) (addendum P6)."""
    y = np.asarray(y, float)
    x = np.asarray(x, float)
    Zn = nuisance_matrix(D["age"], D["sex2"], D["logdur"], D["site"])
    fl = FreedmanLane(x, Zn)
    P = within_site_permutations(D["site"].values, B, np.random.default_rng(seed))
    flr = fl.test(y, P)
    fe = fe_ols(y, x, Zn)
    return {"n": int(y.size), "n_sites": int(D["site"].nunique()), "beta": fe["beta"], "se": fe["se"],
            "t": fe["t"], "p_fl": flr["p_fl"], "B": flr["B"], "perm_seed": seed,
            "std_beta": fe["beta"] * float(np.std(x, ddof=1)) / float(np.std(y, ddof=1))}


# ============================================================================================ decisions
def holm(pvals) -> list:
    p = np.asarray(pvals, float)
    m = p.size
    order = np.argsort(p, kind="stable")
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p[i]))
        adj[i] = running
    return adj.tolist()


def bh(pvals) -> list:
    p = np.asarray(pvals, float)
    m = p.size
    order = np.argsort(p, kind="stable")
    adj = np.empty(m)
    running = 1.0
    for rank in range(m - 1, -1, -1):
        i = order[rank]
        running = min(running, p[i] * m / (rank + 1))
        adj[i] = min(1.0, running)
    return adj.tolist()


def endpoint_survives(p_holm: float, d: float) -> bool:
    return bool(p_holm < ALPHA and abs(d) >= D_MIN)


def primary_verdict(res: dict) -> dict:
    """res: {"E1": {...p_fl, d...}, "E2": {...}} -> Holm + survival + Topic 1 kill rule (card 5)."""
    ps = [res[e]["p_fl"] for e in ENDPOINTS]
    ph = holm(ps)
    per = {}
    for e, p_h in zip(ENDPOINTS, ph):
        d = res[e]["d"]
        surv = endpoint_survives(p_h, d)
        per[e] = {"p_fl": res[e]["p_fl"], "p_holm": p_h, "d": d, "survives": surv,
                  "reason": ("p_Holm < 0.05 and |d| >= 0.15" if surv else
                             "; ".join(([] if p_h < ALPHA else ["p_Holm >= 0.05"]) +
                                       ([] if abs(d) >= D_MIN else ["|d| < 0.15"])))}
    killed = not any(v["survives"] for v in per.values())
    return {"endpoints": per, "topic1_killed": killed,
            "verdict": "Topic 1 KILLED (neither endpoint survives)" if killed else
            "Topic 1 SURVIVES on " + ", ".join(e for e in ENDPOINTS if per[e]["survives"])}


def degeneracy_rates(units: list) -> dict:
    """units: list of per-subject unit dicts (one density/channel).  Denominator = subjects with a successful
    extraction (contract-passing, included).  E1 degenerate iff null SD(030C) == 0; E2 iff SD(030C) == 0 or
    SD(030T) == 0 (addendum P2)."""
    n = len(units)
    e1 = sum(bool(u["degenerate"]["030C"]) for u in units)
    e2 = sum(bool(u["degenerate"]["030C"] or u["degenerate"]["030T"]) for u in units)
    return {"n": n, "n_degenerate_E1": e1, "n_degenerate_E2": e2,
            "rate_E1": e1 / n if n else float("nan"), "rate_E2": e2 / n if n else float("nan")}


def fallback_decision(rates_at_010: dict) -> dict:
    trig = bool(rates_at_010["rate_E1"] > FALLBACK_RATE or rates_at_010["rate_E2"] > FALLBACK_RATE)
    return {"fallback_triggered": trig, "primary_density": DENSITY_FALLBACK if trig else DENSITY_PRIMARY,
            "rule": "fallback iff rate_E1 > 0.10 or rate_E2 > 0.10 at broadband@0.10 (card 3)",
            "rates_broadband_010": rates_at_010}


def endpoint_value(unit: dict, e: str) -> float:
    return float(unit["E1_Z030C"] if e == "E1" else unit["E2_Z030C_minus_Z030T"])


# ============================================================================================ data join
def load_extraction(path: str) -> dict:
    recs = {}
    with open(path) as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                recs[r["position"]] = r
    return recs


def load_design(manifest: dict) -> pd.DataFrame:
    """Per-position design from metadata (dx, age, sex, Y-BOCS, medication, site) and manifest (log duration).
    Index = position.  Names are used only for the join and dropped."""
    names = sorted(os.listdir(NPY_DIR))
    if len(names) != manifest["n"]:
        raise StopForReview("cohort size differs from manifest")
    meta = pd.read_csv(META, usecols=["Unique_ID", "Sample", "OCD", "Age", "Sex", "Y-BOCS", "Medication"])
    meta = meta.set_index(meta["Unique_ID"].astype(str))
    if meta.index.duplicated().any():
        raise StopForReview("duplicate metadata rows")
    m = meta.loc[names].reset_index(drop=True).drop(columns=["Unique_ID"])
    rows = {r["position"]: r for r in manifest["rows"]}
    m["position"] = np.arange(len(names))
    if not all(rows[p].get("site") == s for p, s in zip(m["position"], m["Sample"].astype(str))):
        raise StopForReview("site mismatch between metadata and manifest")
    m["site"] = m["Sample"].astype(str)
    m["dx"] = np.where(m["OCD"] == 1, 1.0, np.where(m["OCD"] == 2, 0.0, np.nan))
    m["age"] = m["Age"].astype(float)
    m["sex2"] = np.where(m["Sex"] == 2, 1.0, np.where(m["Sex"] == 1, 0.0, np.nan))
    m["logdur"] = [math.log(rows[p]["duration_s"]) if rows[p].get("contract_ok") else np.nan for p in m["position"]]
    m["ybocs"] = m["Y-BOCS"].astype(float)
    m["med"] = m["Medication"]
    return m.set_index("position")[["site", "dx", "age", "sex2", "logdur", "ybocs", "med"]]


def complete_design(D: pd.DataFrame) -> pd.DataFrame:
    return D[D[["dx", "age", "sex2", "logdur"]].notna().all(axis=1)]


# ============================================================================================ secondary family 1
def site_bootstrap_auc(y, score, site, n_boot=N_BOOT, seed=SEED_BOOT) -> list:
    from sklearn.metrics import roc_auc_score
    rng = np.random.default_rng(seed)
    sites = np.unique(site)
    idx_by = {s: np.flatnonzero(site == s) for s in sites}
    vals = []
    for _ in range(n_boot):
        pick = rng.choice(sites, size=sites.size, replace=True)
        ii = np.concatenate([idx_by[s] for s in pick])
        if np.unique(y[ii]).size == 2:
            vals.append(roc_auc_score(y[ii], score[ii]))
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5)), len(vals)]


def logo_classification(X, y, site, model: str) -> dict:
    """LeaveOneGroupOut over sites; L2 logistic regression C = 1; preprocessing fit on training folds only."""
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import LeaveOneGroupOut
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    oof = np.full(y.size, np.nan)
    for tr, te in LeaveOneGroupOut().split(X, y, site):
        if model == "lagmotif":
            clf = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=5000))
        else:
            clf = make_pipeline(PCA(n_components=50, svd_solver="randomized", random_state=SEED_BOOT),
                                LogisticRegression(C=1.0, max_iter=5000))
        clf.fit(X[tr], y[tr])
        oof[te] = clf.predict_proba(X[te])[:, 1]
    per_site = []
    for s in np.unique(site):
        ii = site == s
        if np.unique(y[ii]).size == 2:
            per_site.append(roc_auc_score(y[ii], oof[ii]))
    return {"pooled_oof_auroc": float(roc_auc_score(y, oof)), "pooled_auroc_ci95_site_bootstrap":
            site_bootstrap_auc(y, oof, site), "mean_per_site_auroc": float(np.mean(per_site)),
            "n_sites_with_both_classes": len(per_site), "n": int(y.size)}


# ============================================================================================ validate
def _synth_design(seed=0, n_sites=8, sizes=None):
    """Small synthetic design with imbalanced site x dx structure (for unit tests)."""
    rng = np.random.default_rng(seed)
    sizes = sizes or [30, 50, 40, 60, 35, 45, 55, 25][:n_sites]
    rows = []
    for s, n in enumerate(sizes):
        frac = 0.2 + 0.6 * s / max(1, n_sites - 1)
        dx = (rng.random(n) < frac).astype(float)
        dur = rng.choice([300.0, 360.0], size=n) if s % 2 == 0 else np.full(n, 300.0 + 20 * s)
        for i in range(n):
            rows.append({"site": f"S{s}", "dx": dx[i], "age": rng.uniform(10, 60), "sex2": float(rng.random() < 0.5),
                         "logdur": math.log(dur[i])})
    return pd.DataFrame(rows)


def _scenario_y(scn, D, rng, d_true=0.0):
    """Synthetic outcomes on design D.  sigma_eps = 1 (level-1); d_true in sigma_eps units."""
    n = len(D)
    sc = pd.Categorical(D["site"]).codes
    ns = sc.max() + 1
    ocdfrac = D.groupby("site")["dx"].transform("mean").values
    if scn == "S1_aligned_icc03":          # site effect = function of site OCD fraction (confounded with dx)
        u = math.sqrt(0.3 / 0.7) * (ocdfrac - ocdfrac.mean()) / ocdfrac.std()
        e = rng.standard_normal(n)
    elif scn == "S2_indep_icc03_hetero":   # independent site intercepts, site-specific noise SD (0.6x..1.7x)
        u = math.sqrt(0.3 / 0.7) * rng.standard_normal(ns)[sc]
        e = np.exp(rng.uniform(-0.5, 0.5, ns))[sc] * rng.standard_normal(n)
    elif scn == "S3_icc01_t4":             # heavy-tailed noise, t(4) scaled to unit variance
        u = math.sqrt(0.1 / 0.9) * rng.standard_normal(ns)[sc]
        e = stats.t.rvs(4, size=n, random_state=rng) / math.sqrt(2.0)
    elif scn == "S4_indep_icc03":          # independent site intercepts, homoscedastic (planted-effect runs)
        u = math.sqrt(0.3 / 0.7) * rng.standard_normal(ns)[sc]
        e = rng.standard_normal(n)
    else:
        raise ValueError(scn)
    return d_true * D["dx"].values + u + 0.01 * (D["age"].values - 30) + e


def cmd_validate(a):
    t_start = time.time()
    man = json.load(open(os.path.join(a.outdir, "manifest.json")))
    D = complete_design(load_design(man))
    D = D[[c for c in ("site", "dx", "age", "sex2", "logdur")]]
    out = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "script_sha256": sha256_file(os.path.abspath(__file__)),
           "design": {"n": len(D), "n_ocd": int(D["dx"].sum()), "n_sites": int(D["site"].nunique()),
                      "note": "real site x dx x age x sex x log-duration design; outcomes synthetic; no feature read"}}
    sc = D["site"].values
    Zn = nuisance_matrix(D["age"], D["sex2"], D["logdur"], sc)
    out["design"]["rank_full"] = [int(np.linalg.matrix_rank(np.column_stack([D["dx"], Zn]))), Zn.shape[1] + 1]
    fl = FreedmanLane(D["dx"].values, Zn)

    # V1 structural oracles
    import statsmodels.api as sm
    rng = np.random.default_rng(1)
    y = _scenario_y("S2_indep_icc03_hetero", D, rng)
    P = within_site_permutations(sc, 20, np.random.default_rng(2))
    same_site = bool(all((sc[P[b]] == sc).all() for b in range(P.shape[0])))
    Xf = np.column_stack([D["dx"].values, Zn])
    red = sm.OLS(y, Zn).fit()
    naive = np.array([sm.OLS(red.fittedvalues + red.resid[P[b]], Xf).fit().tvalues[0] for b in range(20)])
    vec = fl.t_perm(y, P)
    out["V1_structural"] = {"perms_stay_within_site": same_site,
                            "max_abs_t_vectorised_minus_statsmodels_refit": float(np.max(np.abs(vec - naive))),
                            "abs_t_obs_minus_statsmodels": float(abs(fl.t_obs(y) - sm.OLS(y, Xf).fit().tvalues[0])),
                            "dx_not_in_reduced_design": bool(fl.sxx > 0)}
    out["V1_structural"]["pass"] = bool(same_site and out["V1_structural"]["max_abs_t_vectorised_minus_statsmodels_refit"] < 1e-8
                                        and out["V1_structural"]["abs_t_obs_minus_statsmodels"] < 1e-8)

    # V2 null FPR, R reps at B = 999 (two-sided 3-SE band), Welch as defect fixture
    R, Bv = a.R, 999
    band = 3 * math.sqrt(0.05 * 0.95 / R)
    out["V2_null_fpr"] = {"R": R, "B": Bv, "band": [0.05 - band, 0.05 + band], "scenarios": {}}
    for k, scn in enumerate(("S1_aligned_icc03", "S2_indep_icc03_hetero", "S3_icc01_t4")):
        rng = np.random.default_rng(1000 + k)
        hits = welch = across = 0
        t0 = time.time()
        for _ in range(R):
            yy = _scenario_y(scn, D, rng)
            Pm = within_site_permutations(sc, Bv, rng)
            r = fl.test(yy, Pm)
            hits += r["p_fl"] < ALPHA
            welch += descriptive_raw(yy, D["dx"].values)["welch_p_DESCRIPTIVE"] < ALPHA
            Pa = np.argsort(rng.random((Bv, len(D))), axis=1)        # DEFECT: permutation across sites
            across += fl.test(yy, Pa)["p_fl"] < ALPHA
        fpr, fw, fa = hits / R, welch / R, across / R
        out["V2_null_fpr"]["scenarios"][scn] = {
            "fpr_freedman_lane_within_site": fpr, "pass": bool(abs(fpr - 0.05) <= band),
            "fpr_welch_DEFECT": fw, "welch_outside_band": bool(abs(fw - 0.05) > band),
            "fpr_across_site_permutation_DEFECT": fa, "across_outside_band": bool(abs(fa - 0.05) > band),
            "sec": round(time.time() - t0, 1)}
        print(scn, out["V2_null_fpr"]["scenarios"][scn], flush=True)
    # confirmation at the real B = 9,999
    Rc = a.Rc
    rng = np.random.default_rng(1999)
    hits = 0
    for _ in range(Rc):
        yy = _scenario_y("S1_aligned_icc03", D, rng)
        hits += fl.test(yy, within_site_permutations(sc, B_PERM, rng))["p_fl"] < ALPHA
    bc = 3 * math.sqrt(0.05 * 0.95 / Rc)
    out["V2b_confirm_B9999"] = {"scenario": "S1_aligned_icc03", "R": Rc, "B": B_PERM, "fpr": hits / Rc,
                                "band": [0.05 - bc, 0.05 + bc], "pass": bool(abs(hits / Rc - 0.05) <= bc)}
    print("V2b", out["V2b_confirm_B9999"], flush=True)

    # V3 planted effects, independent site intercepts ICC 0.3; card d vs defect definitions
    out["V3_planted"] = {}
    for d_true in (0.0, 0.15, 0.30):
        rng = np.random.default_rng(3000 + int(d_true * 100))
        dh, dtot, dre, dfe, surv, eq, conv = [], [], [], [], 0, [], 0
        for _ in range(a.Rp):
            yy = _scenario_y("S4_indep_icc03", D, rng, d_true=d_true)
            lm = mixedlm_mundlak(yy, D["dx"], D["age"], D["sex2"], D["logdur"], sc)
            fe = fe_ols(yy, D["dx"].values, Zn)
            dh.append(lm["beta"] / math.sqrt(lm["scale"]))
            dtot.append(lm["beta"] / float(np.std(yy, ddof=1)))                    # DEFECT: total SD
            dre.append(lm["beta"] / math.sqrt(lm["scale"] + lm["re_var"]))          # DEFECT: scale + re_var
            dfe.append(fe["beta"] / fe["sigma"])
            eq.append(abs(lm["beta"] - fe["beta"]) / fe["se"])
            conv += lm["converged"]
            p = fl.test(yy, within_site_permutations(sc, 999, rng))["p_fl"]
            surv += endpoint_survives(min(1.0, 2 * p), dh[-1])                   # Holm upper bound for one of 2
        dh, dtot, dre, dfe = map(np.array, (dh, dtot, dre, dfe))
        se = dh.std(ddof=1) / math.sqrt(a.Rp)
        out["V3_planted"][f"d={d_true:.2f}"] = {
            "R": a.Rp, "mean_d_card": float(dh.mean()), "mc_se": float(se),
            "recovered_within_3se": bool(abs(dh.mean() - d_true) <= 3 * se),
            "mean_d_totalSD_DEFECT": float(dtot.mean()), "totalSD_outside_3se": bool(abs(dtot.mean() - d_true) > 3 * se),
            "mean_d_scale_plus_re_DEFECT": float(dre.mean()),
            "scale_plus_re_outside_3se": bool(abs(dre.mean() - d_true) > 3 * se),
            "mean_d_fe": float(dfe.mean()), "max_mundlak_equality_ratio": float(np.max(eq)),
            "n_converged_flag_true": int(conv), "share_surviving_card_rule": surv / a.Rp}
        print(f"d={d_true}", out["V3_planted"][f"d={d_true:.2f}"], flush=True)

    # V4 deterministic decision-rule checks
    out["V4_rules"] = {
        "holm_[0.01,0.04]": holm([0.01, 0.04]), "holm_[0.04,0.01]": holm([0.04, 0.01]),
        "holm_[0.03,0.02]": holm([0.03, 0.02]),
        "survive(0.049,0.151)": endpoint_survives(0.049, 0.151), "survive(0.049,0.149)": endpoint_survives(0.049, 0.149),
        "survive(0.050,0.30)": endpoint_survives(0.050, 0.30), "survive(0.01,-0.20)": endpoint_survives(0.01, -0.20),
        "fallback(0.09,0.09)": fallback_decision({"rate_E1": 0.09, "rate_E2": 0.09})["primary_density"],
        "fallback(0.09,0.11)": fallback_decision({"rate_E1": 0.09, "rate_E2": 0.11})["primary_density"],
        "fallback(0.10,0.10)": fallback_decision({"rate_E1": 0.10, "rate_E2": 0.10})["primary_density"]}
    v = out["V4_rules"]
    out["V4_rules"]["pass"] = bool(np.allclose(v["holm_[0.01,0.04]"], [0.02, 0.04]) and
                                   np.allclose(v["holm_[0.04,0.01]"], [0.04, 0.02]) and
                                   np.allclose(v["holm_[0.03,0.02]"], [0.04, 0.04]) and
                                   v["survive(0.049,0.151)"] and not v["survive(0.049,0.149)"] and
                                   not v["survive(0.050,0.30)"] and v["survive(0.01,-0.20)"] and
                                   v["fallback(0.09,0.09)"] == 0.10 and v["fallback(0.09,0.11)"] == 0.15 and
                                   v["fallback(0.10,0.10)"] == 0.10)
    out["all_pass"] = bool(out["V1_structural"]["pass"] and
                           all(s["pass"] for s in out["V2_null_fpr"]["scenarios"].values()) and
                           out["V2b_confirm_B9999"]["pass"] and
                           all(v["recovered_within_3se"] for v in out["V3_planted"].values()) and
                           out["V3_planted"]["d=0.30"]["totalSD_outside_3se"] and
                           out["V3_planted"]["d=0.30"]["scale_plus_re_outside_3se"] and
                           out["V2_null_fpr"]["scenarios"]["S1_aligned_icc03"]["welch_outside_band"] and
                           all(v["max_mundlak_equality_ratio"] < STOP_TOL_SE for v in out["V3_planted"].values()) and
                           out["V4_rules"]["pass"])
    out["elapsed_s"] = round(time.time() - t_start, 1)
    path = os.path.join(a.outdir, a.out)
    json.dump(out, open(path, "w"), indent=1)
    print("all_pass", out["all_pass"], "->", path, sha256_file(path))


# ============================================================================================ decide
def cmd_decide(a):
    """Label-free: reads only the primary extraction (no metadata phenotype)."""
    recs = load_extraction(os.path.join(a.outdir, "extract_primary.jsonl"))
    ok = [r for r in recs.values() if r["ok"]]
    rates = {f"{ch}@{d:.2f}": degeneracy_rates([r["units"][f"{ch}@{d:.2f}"] for r in ok])
             for ch in ("broadband", "curl") for d in (0.05, 0.10, 0.15)}
    dec = fallback_decision(rates["broadband@0.10"])
    dec.update({"created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "labels_read": False,
                "n_extraction_records": len(recs), "n_ok": len(ok),
                "n_failed": len(recs) - len(ok), "rates_all_units": rates,
                "extract_primary_jsonl_sha256": sha256_file(os.path.join(a.outdir, "extract_primary.jsonl")),
                "script_sha256": sha256_file(os.path.abspath(__file__))})
    path = os.path.join(a.outdir, "fallback_decision.json")
    json.dump(dec, open(path, "w"), indent=1)
    with open(os.path.join(a.outdir, "fallback_decision_sha256.txt"), "w") as f:
        f.write(f"{sha256_file(path)}  fallback_decision.json  {dec['created_utc']}\n")
    print(json.dumps({k: dec[k] for k in ("fallback_triggered", "primary_density", "rates_broadband_010")}, indent=1))


# ============================================================================================ analyze
def _check_recorded_hashes(outdir):
    rec = open(os.path.join(outdir, "stats_script_sha256.txt")).read().split()[0]
    mine = sha256_file(os.path.abspath(__file__))
    if rec != mine:
        raise StopForReview(f"stats script sha256 {mine[:12]} differs from the recorded {rec[:12]}: stop")
    dec_path = os.path.join(outdir, "fallback_decision.json")
    drec = open(os.path.join(outdir, "fallback_decision_sha256.txt")).read().split()[0]
    if sha256_file(dec_path) != drec:
        raise StopForReview("fallback decision file changed after it was recorded")
    return mine


def _units_frame(recs, key, D):
    rows = []
    for p, r in recs.items():
        if r["ok"] and p in D.index:
            u = r["units"][key]
            rows.append({"position": p, "E1": endpoint_value(u, "E1"), "E2": endpoint_value(u, "E2"),
                         "Z030T": u["Z"]["030T"], "Z030C": u["Z"]["030C"], "log_ratio_030C": u["log_ratio_030C"],
                         "deg_E1": bool(u["degenerate"]["030C"]),
                         "deg_E2": bool(u["degenerate"]["030C"] or u["degenerate"]["030T"]),
                         "acceptance": u["acceptance_mean"], "gradient_share": r["gradient_share"],
                         "grid_len": r["grid_len"]})
    return pd.DataFrame(rows).set_index("position")


def _rates_by(D, U):
    J = D.join(U, how="inner")
    J["group"] = np.where(J["dx"] == 1, "OCD", "HC")
    def summ(g):
        return {"n": int(len(g)), "deg_E1_rate": float(g["deg_E1"].mean()), "deg_E2_rate": float(g["deg_E2"].mean()),
                "acceptance_mean": float(g["acceptance"].mean()), "acceptance_p10": float(g["acceptance"].quantile(0.1)),
                "grid_len_median": float(g["grid_len"].median()), "grid_len_min": int(g["grid_len"].min()),
                "gradient_share_mean": float(g["gradient_share"].mean())}
    return {"by_group": {k: summ(g) for k, g in J.groupby("group")},
            "by_site": {k: summ(g) for k, g in J.groupby("site")},
            "by_site_group": {f"{s}|{gname}": summ(g) for (s, gname), g in J.groupby(["site", "group"])}}


CARD_COUNTS = {"n_on_disk": 1706, "n_ocd_code1": 869, "n_hc_code2": 837, "n_sites": 23, "ybocs_nonnull_ocd": 856,
               "med_code1_ocd": 203, "med_code2_ocd": 212}   # card sections 3 and 6 (verified 2026-10-30)


def card_count_check(D_all) -> dict:
    """Stop if the metadata no longer gives the card's counts (a changed or mis-typed metadata file)."""
    obs = {"n_on_disk": len(D_all), "n_ocd_code1": int((D_all["dx"] == 1).sum()),
           "n_hc_code2": int((D_all["dx"] == 0).sum()), "n_sites": int(D_all["site"].nunique()),
           "ybocs_nonnull_ocd": int(((D_all["dx"] == 1) & D_all["ybocs"].notna()).sum()),
           "med_code1_ocd": int(((D_all["dx"] == 1) & (D_all["med"] == 1)).sum()),
           "med_code2_ocd": int(((D_all["dx"] == 1) & (D_all["med"] == 2)).sum())}
    out = {k: (obs[k], CARD_COUNTS[k]) for k in CARD_COUNTS}
    bad = sorted(k for k, v in out.items() if v[0] != v[1])
    if bad:
        raise StopForReview(f"metadata counts differ from card sections 3/6: {bad}")
    return out


def check_nan_flag_agreement(U) -> None:
    """Card 3 excludes 'degenerate (Z NaN)'; addendum P2 defines degenerate by null SD == 0.  They must agree."""
    for e in ENDPOINTS:
        isn = ~np.isfinite(U[e].values.astype(float))
        if not np.array_equal(isn, U["deg_" + e].values.astype(bool)):
            raise StopForReview(f"{e}: non-finite endpoint values do not coincide with the degeneracy flags")


def exclusions_by(D_all, recs, U, key) -> dict:
    """Every exclusion class, by group and site (card 3: 'both counts are reported by group and site')."""
    rows = []
    for p in D_all.index:
        r = recs.get(p)
        rows.append({"position": p, "site": D_all.loc[p, "site"],
                     "group": {1.0: "OCD", 0.0: "HC"}.get(D_all.loc[p, "dx"], "dx_missing"),
                     "extraction_failed": bool(r is None or not r["ok"]),
                     "covariate_missing": bool(D_all.loc[p, ["dx", "age", "sex2", "logdur"]].isna().any()),
                     "degenerate_E1": bool(p in U.index and U.loc[p, "deg_E1"]),
                     "degenerate_E2": bool(p in U.index and U.loc[p, "deg_E2"])})
    X = pd.DataFrame(rows)
    cols = ["extraction_failed", "covariate_missing", "degenerate_E1", "degenerate_E2"]
    def agg(g):
        return {"n": int(len(g)), **{c: int(g[c].sum()) for c in cols}}
    return {"unit": key, "total": agg(X), "by_group": {k: agg(g) for k, g in X.groupby("group")},
            "by_site": {k: agg(g) for k, g in X.groupby("site")},
            "by_site_group": {f"{s}|{gname}": agg(g) for (s, gname), g in X.groupby(["site", "group"])}}


def run_primary(D, U, label) -> dict:
    check_nan_flag_agreement(U)
    res = {}
    for e in ENDPOINTS:
        sel = U[e].replace([np.inf, -np.inf], np.nan).dropna()
        Dd = D.loc[D.index.intersection(sel.index)]
        res[e] = dx_effect(sel.loc[Dd.index].values, Dd)
        res[e]["n_excluded_degenerate"] = int(len(U) - len(sel))
    res["decision"] = primary_verdict(res)
    # reported beside the verdict (addendum P5): would the same rule with d_FE give the same survival?
    res["decision"]["same_rule_with_d_fe_DESCRIPTIVE"] = {
        e: endpoint_survives(res["decision"]["endpoints"][e]["p_holm"], res[e]["d_fe"]) for e in ENDPOINTS}
    res["decision"]["lmm_converged_flags"] = {e: res[e]["lmm_converged_flag"] for e in ENDPOINTS}
    res["label"] = label
    return res


def cmd_analyze(a):
    t0 = time.time()
    mine = _check_recorded_hashes(a.outdir)
    logp = os.path.join(a.outdir, "analyze.log")
    logf = open(logp, "a")

    def log(msg):
        line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {msg}"
        logf.write(line + "\n")
        logf.flush()
        print(line, flush=True)

    log(f"analyze start script_sha256={mine}")
    man = json.load(open(os.path.join(a.outdir, "manifest.json")))
    dec = json.load(open(os.path.join(a.outdir, "fallback_decision.json")))
    recs = load_extraction(os.path.join(a.outdir, "extract_primary.jsonl"))
    for r in recs.values():
        if r["ok"] and r["params_sha256"] != "86863ffad95cbd852ae4e187490e2112183dd38632166bb417158b62bfea15c6":
            raise StopForReview("primary extraction row with a non-frozen params hash")
    D_all = load_design(man)                       # FIRST label read in the analysis chain
    D = complete_design(D_all)
    card_counts = card_count_check(D_all)
    log(f"labels joined: n_design={len(D)} n_extracted_ok={sum(r['ok'] for r in recs.values())}")
    dens = dec["primary_density"]
    key = f"broadband@{dens:.2f}"
    U = _units_frame(recs, key, D)
    out = {"script_sha256": mine, "manifest_sha256": sha256_file(os.path.join(a.outdir, "manifest.json")),
           "fallback_decision": {k: dec[k] for k in ("fallback_triggered", "primary_density")},
           "extract_primary_jsonl_sha256": sha256_file(os.path.join(a.outdir, "extract_primary.jsonl")),
           "primary_unit": key}
    out["card_count_checks"] = {k: {"observed": v[0], "card": v[1]} for k, v in card_counts.items()}
    out["exclusions_primary_unit"] = exclusions_by(D_all, recs, U, key)
    out["primary"] = run_primary(D, U, f"PRIMARY {key}")
    log(f"primary verdict: {out['primary']['decision']['verdict']}")
    if dec["fallback_triggered"]:
        U10 = _units_frame(recs, "broadband@0.10", D)
        out["density_010_after_fallback_SENSITIVITY"] = run_primary(D, U10, "SENSITIVITY broadband@0.10 (fallback)")
    out["descriptives_primary_unit"] = _rates_by(D, U)
    out["descriptives_all_units"] = {k: _rates_by(D, _units_frame(recs, k, D))["by_group"]
                                     for k in next(r for r in recs.values() if r["ok"])["units"].keys()}
    out["log_ratio_030C_secondary"] = dx_effect(U["log_ratio_030C"].loc[D.index.intersection(U.index)].values,
                                                D.loc[D.index.intersection(U.index)])
    # acceptance-stratified sensitivity (post-freeze, addendum F.34): primary endpoints in subjects above the
    # pooled 10th percentile of acceptance at the primary unit
    thr = float(U["acceptance"].quantile(0.10))
    out["acceptance_stratified_POSTFREEZE"] = {"threshold_acceptance_p10": thr}
    for e in ENDPOINTS:
        sel = U[(U["acceptance"] > thr)][e].replace([np.inf, -np.inf], np.nan).dropna()
        Dd = D.loc[D.index.intersection(sel.index)]
        out["acceptance_stratified_POSTFREEZE"][e] = dx_effect(sel.loc[Dd.index].values, Dd)
    log("primary + descriptives done")

    # ---- secondary family 2: Y-BOCS within OCD
    fam2 = {}
    Do = D[(D["dx"] == 1) & D["ybocs"].notna()]
    for e in ENDPOINTS:
        sel = U[e].replace([np.inf, -np.inf], np.nan).dropna()
        ii = Do.index.intersection(sel.index)
        fam2[e] = assoc_effect(Do.loc[ii, "ybocs"].values, sel.loc[ii].values, Do.loc[ii])
    for e, q in zip(ENDPOINTS, bh([fam2[e]["p_fl"] for e in ENDPOINTS])):
        fam2[e]["q_bh"] = q
    # ---- secondary family 3: medication code 1 vs code 2 within OCD, sites with both codes
    fam3 = {}
    Dm = D[(D["dx"] == 1) & D["med"].isin([1, 2])]
    both = Dm.groupby("site")["med"].nunique()
    Dm = Dm[Dm["site"].isin(both[both == 2].index)]
    for e in ENDPOINTS:
        sel = U[e].replace([np.inf, -np.inf], np.nan).dropna()
        ii = Dm.index.intersection(sel.index)
        x = (Dm.loc[ii, "med"].values == 1).astype(float)
        fam3[e] = assoc_effect(sel.loc[ii].values, x, Dm.loc[ii])
        fam3[e]["contrast"] = "code 1 minus code 2 (coding direction unconfirmed; no medication interpretation)"
        fam3[e]["n_code1"] = int(x.sum())
        fam3[e]["n_code2"] = int((1 - x).sum())
        fam3[e]["d_fe"] = fam3[e]["beta"] / fe_ols(sel.loc[ii].values, x, nuisance_matrix(
            Dm.loc[ii, "age"], Dm.loc[ii, "sex2"], Dm.loc[ii, "logdur"], Dm.loc[ii, "site"].values))["sigma"]
    for e, q in zip(ENDPOINTS, bh([fam3[e]["p_fl"] for e in ENDPOINTS])):
        fam3[e]["q_bh"] = q
    out["secondary_family2_ybocs"] = fam2
    out["secondary_family3_medication"] = fam3
    log("families 2-3 done")
    # ---- secondary family 1: site-held-out classification (descriptive)
    fam1 = {}
    sel = U[["Z030C", "Z030T", "gradient_share"]].replace([np.inf, -np.inf], np.nan).dropna()
    ii = D.index.intersection(sel.index)
    y = D.loc[ii, "dx"].values.astype(int)
    site = D.loc[ii, "site"].values
    fam1["lagmotif"] = logo_classification(sel.loc[ii].values, y, site, "lagmotif")
    fam1["lagmotif_unit"] = key
    if dec["fallback_triggered"]:
        # card 6 names broadband@0.10 literally; after a fallback the decided density is used (addendum P7)
        # and the literal 0.10 result is reported beside it
        U10 = _units_frame(recs, "broadband@0.10", D)
        s10 = U10[["Z030C", "Z030T", "gradient_share"]].replace([np.inf, -np.inf], np.nan).dropna()
        i10 = D.index.intersection(s10.index)
        fam1["lagmotif_broadband@0.10_literal_card_unit"] = logo_classification(
            s10.loc[i10].values, D.loc[i10, "dx"].values.astype(int), D.loc[i10, "site"].values, "lagmotif")
    fc_path = os.path.join(a.outdir, "derived", "static_fc_upper_f32.npy")
    if os.path.exists(fc_path):
        FC = np.load(fc_path, mmap_mode="r")
        Xfc = np.asarray(FC[np.asarray(ii, dtype=int)], dtype=np.float64)
        if not np.all(np.isfinite(Xfc)):
            raise StopForReview("static FC has missing rows for analysed subjects")
        fam1["static_fc_comparator_same_subjects_same_folds"] = logo_classification(Xfc, y, site, "staticfc")
        fam1["static_fc_sha256"] = sha256_file(fc_path)
    fam1["note"] = "descriptive (no p-value); external baselines in card 6 are not comparable folds"
    out["secondary_family1_classification"] = fam1
    out["elapsed_s"] = round(time.time() - t0, 1)
    path = os.path.join(a.outdir, "stats_results.json")
    json.dump(out, open(path, "w"), indent=1, default=float)
    log(f"done -> {path} sha256={sha256_file(path)}")


# ============================================================================================ sensitivity
def rank_inverse_normal(y):
    r = stats.rankdata(y)
    return stats.norm.ppf((r - 0.5) / len(y))


def cmd_sensitivity(a):
    mine = _check_recorded_hashes(a.outdir)
    res = json.load(open(os.path.join(a.outdir, "stats_results.json")))
    dec = json.load(open(os.path.join(a.outdir, "fallback_decision.json")))
    surv = [e for e in ENDPOINTS if res["primary"]["decision"]["endpoints"][e]["survives"]]
    out = {"script_sha256": mine, "surviving_endpoints": surv}
    if not surv:
        out["note"] = "no endpoint survives: card 7 sensitivity analyses are not interpreted and were not run"
        json.dump(out, open(os.path.join(a.outdir, "stats_sensitivity.json"), "w"), indent=1)
        print(out["note"])
        return
    man = json.load(open(os.path.join(a.outdir, "manifest.json")))
    D = complete_design(load_design(man))
    recs = load_extraction(os.path.join(a.outdir, "extract_primary.jsonl"))
    dens = dec["primary_density"]
    key = f"broadband@{dens:.2f}"
    U = _units_frame(recs, key, D)

    def fit(series, Dsub, **kw):
        s = series.replace([np.inf, -np.inf], np.nan).dropna()
        ii = Dsub.index.intersection(s.index)
        return dx_effect(s.loc[ii].values, Dsub.loc[ii], **kw)

    for e in surv:
        rows = {}
        for d2 in (0.05, 0.10, 0.15):
            if abs(d2 - dens) > 1e-9:
                rows[f"density_{d2:.2f}"] = fit(_units_frame(recs, f"broadband@{d2:.2f}", D)[e], D)
        gs = U["gradient_share"]
        s = U[e].replace([np.inf, -np.inf], np.nan).dropna()
        ii = D.index.intersection(s.index)
        rows["gradient_share_covariate"] = dx_effect(s.loc[ii].values, D.loc[ii], extra=gs.loc[ii].values)
        rows["curl_channel_DESCRIPTIVE"] = fit(_units_frame(recs, f"curl@{dens:.2f}", D)[e], D)
        for var in ("dct128", "trunc200", "af40"):
            pth = os.path.join(a.outdir, f"extract_{var}_d{int(round(dens * 1000)):03d}.jsonl")
            if os.path.exists(pth):
                # trunc200: every analysed series is 200 s, so log duration is constant within site and is
                # dropped from the model (addendum P9); the other variants keep the card covariates
                rows[var] = fit(_units_frame(load_extraction(pth), key, D)[e], D,
                                include_logdur=(var != "trunc200"))
            else:
                rows[var] = {"missing": pth}
        rows["rank_inverse_normal"] = dx_effect(rank_inverse_normal(s.loc[ii].values), D.loc[ii])
        rows["mixedlm_without_mundlak"] = dx_effect(s.loc[ii].values, D.loc[ii], mundlak=False)
        rows["log_ratio_030C"] = fit(U["log_ratio_030C"], D)
        adults = D[D["age"] >= 18]
        rows["excluding_under_18"] = fit(U[e], adults)
        loso = {}
        for site in sorted(D["site"].unique()):
            Ds = D.loc[ii][D.loc[ii, "site"] != site]
            fe = fe_ols(s.loc[Ds.index].values, Ds["dx"].values,
                        nuisance_matrix(Ds["age"], Ds["sex2"], Ds["logdur"], Ds["site"].values))
            loso[site] = {"beta_fe": fe["beta"], "d_fe": fe["beta"] / fe["sigma"]}
        rows["leave_one_site_out_beta"] = loso
        out[e] = rows
    path = os.path.join(a.outdir, "stats_sensitivity.json")
    json.dump(out, open(path, "w"), indent=1, default=float)
    print("->", path, sha256_file(path))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate")
    v.add_argument("--outdir", default=OUTDIR_DEFAULT)
    v.add_argument("--R", type=int, default=2000)
    v.add_argument("--Rc", type=int, default=300)
    v.add_argument("--Rp", type=int, default=300)
    v.add_argument("--out", default="stats_validation.json")
    for name in ("decide", "analyze", "sensitivity"):
        p = sub.add_parser(name)
        p.add_argument("--outdir", default=OUTDIR_DEFAULT)
    a = ap.parse_args()
    {"validate": cmd_validate, "decide": cmd_decide, "analyze": cmd_analyze, "sensitivity": cmd_sensitivity}[a.cmd](a)


if __name__ == "__main__":
    main()
