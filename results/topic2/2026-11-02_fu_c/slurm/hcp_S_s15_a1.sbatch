#!/bin/bash
#SBATCH --job-name=fuc_hcp_S_s15_a1
#SBATCH --partition=gpu
#SBATCH --nodelist=b300-01
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=00:36:00
#SBATCH --output=/scratch/iitp4/fu_c/runs/hcp_S_s15_a1/slurm-%j.out
set -u
mkdir -p /scratch/iitp4/fu_c/runs/hcp_S_s15_a1
cd /scratch/iitp4/fu_c/code
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=4
echo "start $(date -u +%FT%TZ) host=$(hostname) job=${SLURM_JOB_ID} cvd=${CUDA_VISIBLE_DEVICES:-unset}"
/scratch/iitp4/fu_c/venv/bin/python -B scripts/topic2_train.py --source hcp --arm S --seed 15 --perm-file /scratch/iitp4/fu_c/partitions/perms_fu_c.npz --perm-key S_seed15 --data-dir /scratch/iitp4/fu_c/hcp_pos --split-file /scratch/iitp4/fu_c/inputs/split.json --out /scratch/iitp4/fu_c/runs/hcp_S_s15_a1 --max-run-hours 0.55 --save-model
echo "end rc=$? $(date -u +%FT%TZ)"
