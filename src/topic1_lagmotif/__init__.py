"""Topic 1 (ENIGMA-OCD) directed lag-motif extractor v2.

Modules: tr_table (site->TR), data (read-only positional npy loader), preprocess
(detrend -> resample to 2.0 s grid -> z-score), flow (lagged net flow, oriented
fixed-density graph, Hodge gradient share), motifs (closed-form oriented census,
orientation/degree-preserving null, Z/SP), pipeline (frozen PARAMS, extractor),
synthetic (ground-truth generators), spurious (spurious-direction characterization).
"""
