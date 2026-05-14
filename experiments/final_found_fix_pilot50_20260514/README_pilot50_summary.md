# final_found_fix_pilot50_20260514 Summary

Fixed 50-episode pilot after preserving `found` as a final decision in `qwen_utils_goat.py`. Do not treat this as Minimum Submission scale.

## Pilot Table

| selector | SR | SPL | avg steps | steps/s | terminal_found_eps | failures | not_reached_goal | path_planning_failed | max GPU MiB | wall time sec |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| recent_k | 0.18 | 0.022534 | 505.92 | 11.046 | 23 | 41 | 40 | 1 | 24081 | 2397.0 |
| uniform_k | 0.18 | 0.022534 | 505.92 | 10.980 | 23 | 41 | 40 | 1 | 24081 | 2415.0 |
| scm | 0.18 | 0.022534 | 505.92 | 11.320 | 23 | 41 | 40 | 1 | 24081 | 2369.7 |

## Notes

- All three selectors produced identical SR/SPL/failure counts on this run; this should be treated as a pilot finding and a selector-effectiveness audit target, not as a final paper conclusion.
- `terminal_found_eps` is non-zero after the root fix, and `path_planning_failed` is reduced to 1 failure row per selector in this 50-episode pilot.
- `episodes_with_step_logs` is 49 while `metrics.num_episodes` is 50, so one episode likely completed without a model step log; keep this noted in the audit trail.
- Next step before Minimum Submission: audit `selected_indices`/selected frame contents across selectors and expand failure taxonomy on this fixed run.
