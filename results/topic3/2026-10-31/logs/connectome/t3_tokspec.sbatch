#!/bin/bash
#SBATCH --job-name=t3_tokspec
#SBATCH --partition=debug
#SBATCH --nodelist=node2
#SBATCH --cpus-per-task=12
#SBATCH --mem=40G
#SBATCH --time=04:00:00
#SBATCH --nice=100
#SBATCH --array=0-3%1
#SBATCH --output=/home/connectome/connectome1/iitp4_topic3_m2_20261031/logs/t3_tokspec_%A_%a.out
set -euo pipefail
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
LABELS=("E192_primary" "zoo_HCP_N400_T2400_E192" "zoo_NewUAH_deepE192_L1e-4" "zoo_NewUAH_deepE192_L5e-5")
ROOTS=("/storage/bigdata/VRABES/04_embedding/swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES" "/storage/bigdata/VRABES/04_embedding/swift_zoo_ses-01/HCP_N400_T2400_E192/VRABES" "/storage/bigdata/VRABES/04_embedding/swift_zoo_ses-01/NewUAH_deepE192_L1e-4/VRABES" "/storage/bigdata/VRABES/04_embedding/swift_zoo_ses-01/NewUAH_deepE192_L5e-5/VRABES")
EXTRA=("--check-npz-root /storage/bigdata/VRABES/05_pooled_embedding/pooled_E192_layers" "--reference-root /storage/bigdata/VRABES/04_embedding/swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES" "--reference-root /storage/bigdata/VRABES/04_embedding/swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES" "--reference-root /storage/bigdata/VRABES/04_embedding/swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES")
i=$SLURM_ARRAY_TASK_ID
cd /home/connectome/connectome1/iitp4_topic3_m2_20261031/code
echo "task $i label ${LABELS[$i]} start $(date -u +%FT%TZ)"
python3 scripts/topic3_token_job.py --frames-root "${ROOTS[$i]}" --label "${LABELS[$i]}" --out-dir /home/connectome/connectome1/iitp4_topic3_m2_20261031/out --workers 12 ${EXTRA[$i]}
echo "task $i end $(date -u +%FT%TZ)"
