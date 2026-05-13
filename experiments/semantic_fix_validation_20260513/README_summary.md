# Semantic Annotation Fix Validation (2026-05-13)

## Goal
Fix the HM3D semantic annotation loading risk mentioned in analysis notes, and verify the fix both in a minimal semantic probe and in the real `ovon_nav_experiment.py` entrypoint.

## What was fixed
1. The code path now passes HM3D scenes as dataset-relative stage handles such as `00824-Dd4bFSTQ8gi/Dd4bFSTQ8gi.basis.glb` instead of bypassing the dataset config with direct absolute scene files.
2. `simulator.py` now honors `scene_dataset_config_file` and `load_semantic_mesh`.
3. Official HM3D validation semantic assets were added to the server under `dataset/hm3d/val/<scene_id>/`:
   - `*.semantic.glb`
   - `*.semantic.txt`
4. The official-style scene dataset config is present at:
   - `dataset/hm3d/val/hm3d_annotated_val_basis.scene_dataset_config.json`

## Validation result
### 1. Minimal probe
Artifacts:
- `semantic_probe_fixed.out`

Key evidence:
- semantic descriptor loaded successfully
- semantic mesh loaded successfully
- `scene_dataset_config_file` points to the HM3D val annotated config
- `load_semantic_mesh=True`
- `semantic_scene_nonnull=True`
- semantic object count is non-zero (`393` for the checked scene)

### 2. Real experiment smoke
Artifacts:
- `semantic_fix_smoke.out`
- `metrics.json`
- `step_logs.jsonl`
- `failures.csv`

Command behavior:
- `ovon_nav_experiment.py` ran 1 HM3D-OVON episode successfully using the patched semantic path.
- The log shows `Dd4bFSTQ8gi.semantic.txt` found and loaded.
- The log shows `Dd4bFSTQ8gi.semantic.glb` loaded as the semantic stage mesh.
- The previous warning `The active scene does not contain semantic annotations : activeSemanticSceneID_ = 0` does not appear in this validation smoke log.

Smoke metrics:
- selector: `recent_k`
- memory_k: `50`
- episodes: `1`
- SR: `0.0`
- SPL: `0.0`
- steps: `38`
- steps/sec: `4.36`
- GPU memory: `9250 MiB`

## Remaining notes
- Habitat still prints `No Glob path result for *.basis.scene_instance.json` for many scenes because those scene-instance JSON files are not present in this server copy.
- That warning is not blocking semantic loading anymore for the validated HM3D val scene: the semantic descriptor and semantic mesh are both loaded successfully, and the semantic scene is non-empty.

## Conclusion
The specific risk "semantic annotation was not loaded correctly" is fixed for the validated HM3D val pipeline and is now supported by both a direct semantic probe and a real experiment smoke run.
