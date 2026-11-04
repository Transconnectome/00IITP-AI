# Safety Gate Certification & Environment Attestation Report

- **Document Version**: 1.0.0
- **Attestation Date**: 2026-10-29T15:58:00Z
- **Target Repository**: `/home/juke/git/00IITP-AI`
- **Lead Attester**: Teamwork Implementation Worker (`teamwork_worker_m1_m3_1`)
- **Orchestrator Session ID**: `5cc83bee-523a-42f4-bc87-32c8c023ecf6`
- **Compliance Status**: VERIFIED & CERTIFIED (ALL GATES PASSED)

---

## 1. Executive Summary & Objective

This document provides formal, cryptographically backed attestation of repository integrity, safety compliance, and runtime readiness for the **2028 IITP AI Wonchun Project** (*Brain-Inspired Neuromorphic Computing & Non-Backprop Learning*). Prior to initiating the theoretical foundations (M2), research whitepaper (M3), and pilot simulation (M4), all pre-existing research assets, idea notes, and active project materials were audited to guarantee zero corruption, loss, or unauthorized modification.

---

## 2. Cryptographic Integrity & File Preservation Attestation

### 2.1 Preserved Core Idea Files
Professor Jiook Cha's foundational ideation files for "Inside-Out Neuroscience Research and Neuromorphic Design" reside in the root of `/home/juke/git/00IITP-AI`. Independent SHA-256 cryptographic verification confirms that these files are completely unmodified, bit-for-bit identical to their origin commits:

| File Name | File Size (Bytes) | Git Commit Source | SHA-256 Checksum | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| `그랜트아이디어.md` | 11,920 | `a9cfc924` (2026-01-26) | `07b87092de558b6d85d0a25fa7e652ec4acea009e720f508efb2f35f433a2541` | **PASS (UNTOUCHED)** |
| `아이디어.txt` | 11,243 | `378a0b1e` (2026-02-03) | `035a94e6a8e13ccb064937a48c4e37d60039bccfb5389463e174241519140362` | **PASS (UNTOUCHED)** |

### 2.2 Active 1st-Year Evaluation & Meeting Artifacts
The repository concurrently hosts active 1st-year project deliverables for IITP grant `RS-2026-25518389`. These files remain protected under strict read-only boundary constraints:
- `docs/qa_prep_차지욱_20260309.md`: 79,768 bytes, modified in local working tree for the 2026-03 defense evaluation. Strictly preserved; no restore or checkout operations were performed.
- `HANDOFF.md` & `docs/05_meetings/2026-10-29_y1_slides/`: Active meeting artifacts from 2026-10-29 14:00 KST consortium session. Completely preserved.

---

## 3. Git Repository Status & Tracking

- **Working Directory**: `/home/juke/git/00IITP-AI`
- **Active Branch**: `main`
- **Remote Origin**: `https://github.com/Transconnectome/00IITP-AI.git`
- **HEAD Commit**: `e38080205d762f0f42b36a188f635c03cbe3189e` (*Jiookui-MacBookPro.local 2026-3-9:10:26:18*)
- **Working Tree Policy**:
  - All new deliverables for the 2028 AI Wonchun project are strictly contained within new, dedicated subdirectories:
    - `docs/00_safety/`
    - `docs/01_foundations/`
    - `docs/02_proposal/`
    - `src/` (for M4 pilot code)
    - `tests/` (for unit and E2E verification)
    - `scripts/` (for execution shell scripts)
  - Zero modifications to root configuration files (`.cursorrules`, `.gitignore`, `docker-compose.nv-ingest.yml`).

---

## 4. Chavis Repository Registry Activation

In accordance with Chavis Project Receptionist and Anti-Sycophancy protocol (`skills/secretary/SKILL.md` §6), `00IITP-AI` was formally activated in the central registry:

```json
{
  "status": "ok",
  "target": {
    "repo": "00IITP-AI",
    "path": "/home/juke/git/00IITP-AI",
    "session_id": "5cc83bee-523a-42f4-bc87-32c8c023ecf6",
    "activated_at": "2026-10-29T15:44:35+00:00",
    "expires_at": "2026-10-30T15:44:35+00:00"
  }
}
```

- **Registry CLI Tool**: `/home/juke/git/chavis/tools/repo_registry/registry.py`
- **Active Target State Path**: `~/.local/state/chavis/active_target/5cc83bee-523a-42f4-bc87-32c8c023ecf6.json`
- **Card Association**: Onboarding dossier `iitp-brain-ai` (Round 1, final).

---

## 5. Execution Environment & Compute Priority Protocol

### 5.1 Host Hardware Specifications
- **Architecture**: `aarch64` (ARM64, Linux kernel 6.8.0-1017-nvidia-64k)
- **Host CPU**: 20 Cores (ARM Cortex-X925 / Cortex-A725)
- **Host Memory**: 119 GiB Unified LPDDR5X (85 GiB Available)
- **Local Accelerator**: NVIDIA GB10 (CUDA 13.0, Compute Capability 12.1)
- **Active Python Environment**: `/home/juke/superclaude-env/bin/python3` (Python 3.12.3)
  - PyTorch: `2.11.0.dev20251230+cu130`
  - NetworkX: `3.4.2`
  - SciPy: `1.15.3`
  - SymPy: `1.14.0`
  - NumPy: `2.3.5`

### 5.2 GPU Pipeline Priority Enforcement
To adhere to the lab-wide computing resource allocation policy:
1. **1st Priority — Server Cluster (`connectome`)**: Slurm partition with 8× NVIDIA RTX A5000 GPUs and `/storage` NFS. Verified operational via BatchMode SSH (`node1`). Primary target for heavy parameter sweeps and large-scale graph simulations ($N > 10^5$).
2. **1st Priority — DGX-1 (`dgx1`)**: Dedicated cluster with 8× NVIDIA Tesla V100-SXM2-16GB GPUs. Verified operational via BatchMode SSH (`azdgx-1`).
3. **Last Resort — Local DGX-Spark**: Local NVIDIA GB10 GPU. Bound by host unified memory constraints (`MemAvailable`). Strictly reserved for rapid local smoke testing, pilot simulation verification ($N \le 2000$), and unit testing.

---

## 6. Safety Attestation Checklist

- [x] `그랜트아이디어.md` checksum verified: `07b87092...` (Identical)
- [x] `아이디어.txt` checksum verified: `035a94e6...` (Identical)
- [x] `docs/qa_prep_차지욱_20260309.md` preserved without regression
- [x] Chavis repository registry activated for current orchestrator session
- [x] Dedicated output directories initialized (`docs/00_safety/`, `docs/01_foundations/`, `docs/02_proposal/`)
- [x] Execution runtime validated (Python 3.12, PyTorch 2.11, NetworkX 3.4.2)
- [x] Remote cluster dispatch pathways (`connectome`, `dgx1`) validated

**Safety Gate Status: GRANTED — Proceed to Milestone M2.**
