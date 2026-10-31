#!/usr/bin/env bash
# ==============================================================================
# 2028 IITP AI Wonchun: Pilot Simulation Standalone Runner Script
# Milestone M4: Local Learning & Connectome Dynamics
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"

echo "[INFO] Running 2028 IITP AI Wonchun Pilot Simulation..."
python3 "${REPO_ROOT}/src/pilot_local_learning_connectome.py" "$@"
