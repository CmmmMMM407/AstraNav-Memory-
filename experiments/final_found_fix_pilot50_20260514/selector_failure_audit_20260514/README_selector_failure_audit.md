# Selector Effectiveness and Failure Audit

Scope: fixed 50-episode pilot `final_found_fix_pilot50_20260514` after preserving `found` as a final decision. This is an audit before any Minimum Submission expansion.

## Selector Effectiveness

- Common aligned step keys across all selectors: 507.
- recent_k__vs__uniform_k: selected_indices same 454/507 (89.5%); raw_model_output same 507/507 (100.0%); action_target same 507/507 (100.0%).
- recent_k__vs__scm: selected_indices same 99/507 (19.5%); raw_model_output same 507/507 (100.0%); action_target same 507/507 (100.0%).
- uniform_k__vs__scm: selected_indices same 99/507 (19.5%); raw_model_output same 507/507 (100.0%); action_target same 507/507 (100.0%).
- SCM does change `selected_indices` substantially, but output/action remain identical on every aligned step. Recent-K vs Uniform-K differ only when memory exceeds K; they still produce identical output/action.
- Existing step logs contain selected indices/types, not actual image hashes or saved selected frame images. Therefore this audit can verify selector index differences, but cannot prove image-content differences from the completed pilot alone.
- The generation path uses constrained decoding over coordinate candidates / `found`, so raw outputs may be dominated by identical frontier candidate sets even when memory selection differs. This is the main suspected reason selector metrics are identical.

## Failure Taxonomy

### recent_k
- controller_planner: 1 (2.4%)
- search_or_grounding_no_terminal_found: 22 (53.7%)
- terminal_found_false_positive_or_goal_check_mismatch: 18 (43.9%)
### uniform_k
- controller_planner: 1 (2.4%)
- search_or_grounding_no_terminal_found: 22 (53.7%)
- terminal_found_false_positive_or_goal_check_mismatch: 18 (43.9%)
### scm
- controller_planner: 1 (2.4%)
- search_or_grounding_no_terminal_found: 22 (53.7%)
- terminal_found_false_positive_or_goal_check_mismatch: 18 (43.9%)

## Files

- `selector_memory_stats.csv`: per-selector memory length/type statistics.
- `selector_pairwise_summary.csv`: pairwise equality rates for selected indices, raw output, parsed coord, action target, and frontier candidates.
- `selector_step_alignment.csv`: step-level aligned selector comparison for all common steps.
- `failure_taxonomy_all_selectors.csv`: conservative failure labels for all failed rows across selectors.
- `failure_taxonomy_recentk_canonical_41.csv`: canonical 41 failed episodes, because all selectors share the same failure taxonomy on this pilot.

## Recommendation

Do not expand to Minimum Submission yet. First run a small instrumented audit that logs selected image hashes / prompt fingerprints and optionally disables or relaxes constrained coordinate decoding for an ablation. If selector differences still do not affect raw outputs under that audit, the current selector comparison is not experimentally meaningful.
