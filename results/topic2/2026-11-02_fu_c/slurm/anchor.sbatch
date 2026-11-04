#!/bin/bash
#SBATCH --job-name=fuc_anchor
#SBATCH --partition=debug
#SBATCH --nodelist=b300-01
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=00:15:00
#SBATCH --output=/scratch/iitp4/fu_c/anchor/slurm-%j.out
set -u
mkdir -p /scratch/iitp4/fu_c/anchor
cd /scratch/iitp4/fu_c/code
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=4
echo "start $(date -u +%FT%TZ) host=$(hostname) job=${SLURM_JOB_ID} cvd=${CUDA_VISIBLE_DEVICES:-unset}"
/scratch/iitp4/fu_c/venv/bin/python -B scripts/topic2fu_c_anchor.py --python /scratch/iitp4/fu_c/venv/bin/python --data-dir /scratch/iitp4/fu_c/hcp_pos --split-file /scratch/iitp4/fu_c/inputs/split.json --r1-perms /scratch/iitp4/fu_c/inputs/perms_hcp.npz --fplus-perms /scratch/iitp4/fu_c/inputs/perms_Fplus.npz --r1-logs /scratch/iitp4/fu_c/inputs/r1_logs --out /scratch/iitp4/fu_c/anchor
echo "end rc=$? $(date -u +%FT%TZ)"
