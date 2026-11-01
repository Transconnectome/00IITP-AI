# Provenance of the vendored SwiFT ver11 files (ACCEPTANCE C7: external repo read-only, copy what you need)

Copied 2026-11-01 by worker_M3_r1 from the read-only checkout /home/juke/git/SwiFT_v2, byte-identical (no edits).

| file | source path in SwiFT_v2 | sha256 | last commit touching file |
|---|---|---|---|
| simmim_swin4d_transformer_ver11.py | project/module/models/simmim_swin4d_transformer_ver11.py | de132387f64d98cbe9b15876351a7b33f9bec112df3df8f4718327d06e95052a | 6061dc6d306bd96dc8ae9da362533f6b31cb1234 (2026-10-18) |
| patchembedding.py | project/module/models/patchembedding.py | c889eebb6da13cdc4393a9f1d5d341077c7af5a2e0a28108a3ec2ca5dbab7ca7 | 1e76f3eb7c77ccff957e04504b218126aa184277 (2025-04-16) |

- SwiFT_v2 HEAD at copy time: f0dc7acad9dae8d7252e3b05f56202b96d1a94ab.
- `git diff --quiet` on both source files returned 0 (no uncommitted modification) at copy time.
- `tests/topic2_rgpool/test_vendor_provenance.py` re-checks both sha256 values, so any edit to the vendored files fails the suite.
- The perlmutter fork of SwiFT that produced older VRABES representations was not inspected; claims here are about this file only.
- Topic 2 code never edits these files. The connectome box grouping is injected through ver11's own `downsample` argument
  (a callable is accepted at line 1036 and called at line 904), see `src/topic2_rgpool/merge.py`.
