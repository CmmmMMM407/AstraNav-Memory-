# Selector Hash Audit

Small 5-episode audit with `selected_image_hashes`, `selected_pose_hashes`, and `selection_fingerprint` added to step logs. Purpose: verify whether selector differences change actual selected memory content before expanding experiments.

## Pairwise Summary

- recent_k__vs__uniform_k: selection_fingerprint same 34/34 (100.0%); selected_image_hashes same 34/34 (100.0%); raw_model_output same 34/34 (100.0%); action_target same 34/34 (100.0%).
- recent_k__vs__scm: selection_fingerprint same 10/34 (29.4%); selected_image_hashes same 10/34 (29.4%); raw_model_output same 34/34 (100.0%); action_target same 34/34 (100.0%).
- uniform_k__vs__scm: selection_fingerprint same 10/34 (29.4%); selected_image_hashes same 10/34 (29.4%); raw_model_output same 34/34 (100.0%); action_target same 34/34 (100.0%).

## Interpretation

- The hash fields confirm whether selected memory content is identical or different, not just whether selected indices differ.
- If fingerprints differ while raw outputs/actions remain identical, selector logic is active but the current generation/action pipeline is insensitive to selector changes under constrained coordinate decoding.
- This audit is deliberately small and should not be used as paper-scale performance evidence.
