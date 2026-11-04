#!/bin/bash
#SBATCH -J fub-smoke
#SBATCH -p debug
#SBATCH -w b300-01
#SBATCH --gres=gpu:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH --time=00:20:00
#SBATCH -o /scratch/iitp4/fu_b/logs/%x_%j.log
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=4
cd /scratch/iitp4/fu_b/code
echo "start $(date -u +%FT%TZ) host=$(hostname) job=${SLURM_JOB_ID}"
nice /scratch/iitp4/fu_b/venv/bin/python -B scripts/topic2fu_b_smoke.py --base /scratch/iitp4/fu_b
echo "end $(date -u +%FT%TZ)"
