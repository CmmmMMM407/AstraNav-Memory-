# Selector Hash / Action Alignment Audit

- common aligned step keys: `1248`
- union step keys: `1248`
- skipped episodes: `0`
- success sets identical: `True`

## Pairwise Differences

| pair | selection fingerprint diff | selected image hash diff | raw output diff | parsed coord diff | action target diff | frontier diff |
|---|---:|---:|---:|---:|---:|---:|
| recent_k vs uniform_k | 138/1248 (11.1%) | 138/1248 (11.1%) | 0/1248 (0.0%) | 0/1248 (0.0%) | 0/1248 (0.0%) | 0/1248 (0.0%) |
| recent_k vs scm | 1011/1248 (81.0%) | 1011/1248 (81.0%) | 0/1248 (0.0%) | 0/1248 (0.0%) | 0/1248 (0.0%) | 0/1248 (0.0%) |
| uniform_k vs scm | 1011/1248 (81.0%) | 1011/1248 (81.0%) | 0/1248 (0.0%) | 0/1248 (0.0%) | 0/1248 (0.0%) | 0/1248 (0.0%) |

## Interpretation

- The selectors are active: `selected_indices`, selected image hashes, and selection fingerprints change.
- The downstream decision chain is flattened in this configuration: `raw_model_output`, parsed coordinates, and final `action_target` are identical across selectors on every aligned step.
- This means the current main120 run is useful as a stable pipeline/logging baseline, but selector-performance claims need an additional decoding/frontier or prompt-sensitivity ablation before being used as the paper conclusion.
