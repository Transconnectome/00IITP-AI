"""Topic 3 — ship the token-job code (code only) to connectome and submit / collect the Slurm array.

  submit : verify the frozen card, tar src/topic3_spectral + scripts/topic3_token_job.py to
           connectome:~/iitp4_topic3_m2_20261031/code, write the sbatch file there and sbatch it.
  collect: copy back the small position-keyed outputs into results/topic3/2026-10-31/token_job/.
Data never leave connectome except those outputs. No GPU is requested.
Run: cd /home/juke/git/00IITP-AI && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
     /home/juke/superclaude-env/bin/python3 scripts/topic3_launch_connectome.py submit|collect
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.dont_write_bytecode = True
from topic3_common import OUT, verify_card  # noqa: E402

HOST = "connectome"
RDIR = "iitp4_topic3_m2_20261031"
# Cluster policy (sbatch refusal 2026-10-31): node1/node3 are GPU-only; CPU jobs go to node2/node4.
# node4 has no numpy and home dirs are node-local, so code is staged onto node2 via srun stdin.
NODE = "node2"
SRUN = "srun -p debug -w %s -c 1 -t 00:05:00 --nice=100" % NODE
E = "/storage/bigdata/VRABES/04_embedding"
PRIMARY = E + "/swift_E192/NewUAH_newE192_TP1_SL20_MR_0p8_L1e-4/VRABES"
CKPTS = [("E192_primary", PRIMARY, "--check-npz-root /storage/bigdata/VRABES/05_pooled_embedding/pooled_E192_layers"),
         ("zoo_HCP_N400_T2400_E192", E + "/swift_zoo_ses-01/HCP_N400_T2400_E192/VRABES", "--reference-root " + PRIMARY),
         ("zoo_NewUAH_deepE192_L1e-4", E + "/swift_zoo_ses-01/NewUAH_deepE192_L1e-4/VRABES", "--reference-root " + PRIMARY),
         ("zoo_NewUAH_deepE192_L5e-5", E + "/swift_zoo_ses-01/NewUAH_deepE192_L5e-5/VRABES", "--reference-root " + PRIMARY)]

SBATCH = """#!/bin/bash
#SBATCH --job-name=t3_tokspec
#SBATCH --partition=debug
#SBATCH --nodelist=%(node)s
#SBATCH --cpus-per-task=12
#SBATCH --mem=40G
#SBATCH --time=04:00:00
#SBATCH --nice=100
#SBATCH --array=0-3%%1
#SBATCH --output=%(rd)s/logs/t3_tokspec_%%A_%%a.out
set -euo pipefail
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
LABELS=(%(labels)s)
ROOTS=(%(roots)s)
EXTRA=(%(extra)s)
i=$SLURM_ARRAY_TASK_ID
cd %(rd)s/code
echo "task $i label ${LABELS[$i]} start $(date -u +%%FT%%TZ)"
python3 scripts/topic3_token_job.py --frames-root "${ROOTS[$i]}" --label "${LABELS[$i]}" --out-dir %(rd)s/out --workers 12 ${EXTRA[$i]}
echo "task $i end $(date -u +%%FT%%TZ)"
"""


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=True, check=True, **kw)


def submit():
    verify_card()
    home = subprocess.run(["ssh", "-o", "BatchMode=yes", HOST, "echo $HOME"], capture_output=True, text=True,
                          check=True).stdout.strip()
    rd = home + "/" + RDIR
    text = SBATCH % {"rd": rd, "node": NODE, "labels": " ".join('"%s"' % c[0] for c in CKPTS),
                     "roots": " ".join('"%s"' % c[1] for c in CKPTS), "extra": " ".join('"%s"' % c[2] for c in CKPTS)}
    sh("cd %s && tar cf - src/topic3_spectral/*.py scripts/topic3_token_job.py | ssh -o BatchMode=yes %s "
       "\"%s bash -c 'rm -rf %s/code && mkdir -p %s/code %s/logs %s/out && cd %s/code && tar xf - && ls -R | wc -l'\""
       % (ROOT, HOST, SRUN, rd, rd, rd, rd, rd))
    sh("ssh -o BatchMode=yes %s 'mkdir -p %s'" % (HOST, rd))
    p = subprocess.run(["ssh", "-o", "BatchMode=yes", HOST, "cat > %s/t3_tokspec.sbatch && sbatch %s/t3_tokspec.sbatch" % (rd, rd)],
                       input=text, capture_output=True, text=True, check=True)
    print(p.stdout.strip())


def collect():
    dst = os.path.join(OUT, "token_job")
    os.makedirs(dst, exist_ok=True)
    rd = "~/" + RDIR
    sh("ssh -o BatchMode=yes %s \"%s bash -c 'cd %s/out && tar cf - .'\" | tar xf - -C %s" % (HOST, SRUN, rd, dst))
    logs = os.path.join(OUT, "logs", "connectome")
    os.makedirs(logs, exist_ok=True)
    sh("ssh -o BatchMode=yes %s \"%s bash -c 'cd %s && tar cf - logs'\" | tar xf - -C %s" % (HOST, SRUN, rd, logs))
    sh("ssh -o BatchMode=yes %s 'cat %s/t3_tokspec.sbatch' > %s/t3_tokspec.sbatch" % (HOST, rd, logs))
    print(sorted(os.listdir(dst)))


if __name__ == "__main__":
    {"submit": submit, "collect": collect}[sys.argv[1]]()
