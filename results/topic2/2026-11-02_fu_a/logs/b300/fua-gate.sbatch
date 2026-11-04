#!/bin/bash
#SBATCH -J fua-gate
#SBATCH -p gpu
#SBATCH -w b300-01
#SBATCH --gres=gpu:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 01:00:00
#SBATCH --array=0-1%2
#SBATCH -o /scratch/iitp4/fu_a/logs/%x_%A_%a.out
set -euo pipefail
cd /scratch/iitp4/fu_a/code
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=8
ARGS=$(/scratch/iitp4/fu_a/env/venv/bin/python -c 'import json,shlex,sys; j=json.load(open(sys.argv[1]))[int(sys.argv[2])]; print(shlex.join(j["args"]))' /scratch/iitp4/fu_a/logs/jobs_gate.json $SLURM_ARRAY_TASK_ID)
echo "task $SLURM_ARRAY_TASK_ID host $(hostname) gpu $CUDA_VISIBLE_DEVICES start $(date -u +%FT%TZ)"
eval timeout 3300 /scratch/iitp4/fu_a/env/venv/bin/python -B scripts/topic2fu_a_train.py $ARGS
echo "end $(date -u +%FT%TZ)"
