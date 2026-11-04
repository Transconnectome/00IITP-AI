#!/bin/bash
#SBATCH -J fub-s1
#SBATCH -p gpu
#SBATCH -w b300-01
#SBATCH --gres=gpu:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH --time=02:30:00
#SBATCH -o /scratch/iitp4/fu_b/logs/%x_%A_%a.log
#SBATCH --array=0-14%4
#SBATCH --dependency=afterany:509
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=4
cd /scratch/iitp4/fu_b/code
echo "start $(date -u +%%FT%%TZ) host=$(hostname) job=${SLURM_JOB_ID} task=${SLURM_ARRAY_TASK_ID:-none}"
nice /scratch/iitp4/fu_b/venv/bin/python -B scripts/topic2fu_b_run.py --base /scratch/iitp4/fu_b --role stage1 --task-index $SLURM_ARRAY_TASK_ID --attempt 1
echo "end $(date -u +%FT%TZ)"
