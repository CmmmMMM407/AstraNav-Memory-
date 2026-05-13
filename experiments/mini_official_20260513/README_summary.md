# Mini Run Summary (2026-05-13)

## Scope
- Official README aligned Habitat environment
- DS16-C50 checkpoint
- HM3D-OVON smoke test: 10 episodes, video off
- Fixed pilot: same 50 episodes for `recent_k`, `uniform_k`, `scm`

## Smoke Test
- Directory: `smoke_recent_k_10ep/`
- Episodes: 10
- `avg_sr`: 0.0
- `avg_spl`: 0.0
- `avg_steps_per_sec`: 13.7767
- `avg_gpu_mem_used_mib`: 18189.9
- `max_gpu_mem_used_mib`: 23858

### Step-level logging validation
From `smoke_recent_k_10ep/step_log_validation.json`:
- `raw_model_output`: present on all 118 logged decision steps
- `selected_indices`: present on all 118 steps
- `pose`: present on all 118 steps
- `frontier_candidates`: present on all 118 steps
- `parsed_coord_steps`: 0
- `false_found_candidate_steps`: 118

Interpretation:
- Logging chain is working.
- The current output chain still emits non-empty `raw_model_output`, but those outputs are effectively `found` without parseable coordinates in the smoke run.

## Pilot (50 fixed episodes)
See `pilot_50/pilot_table.csv`.

| selector | episodes | avg_sr | avg_spl | avg_steps | avg_steps_per_sec | max_gpu_mem_used_mib | wall_time_sec |
|---|---:|---:|---:|---:|---:|---:|---:|
| recent_k | 50 | 0.22 | 0.03246 | 442.5 | 17.2932 | 17789 | 1307.16 |
| uniform_k | 50 | 0.22 | 0.03246 | 442.5 | 17.2583 | 17789 | 1309.74 |
| scm | 50 | 0.22 | 0.03246 | 442.5 | 19.1630 | 17415 | 1180.38 |

### Success counts
- `recent_k`: 11 / 50
- `uniform_k`: 11 / 50
- `scm`: 11 / 50

### Failure reason counts
All three selectors currently have the same aggregate failure counts:
- `path_planning_failed`: 24
- `not_reached_goal`: 13
- `empty_goto_sequence`: 2

## Main takeaway
- The mini run is operationally complete: environment, checkpoint, smoke, step logs, selectors, fixed 50-episode pilot, pilot table, and 10 failure cases are all produced.
- However, the selector comparison currently shows no separation signal at pilot scale.
- Combined with the smoke validation (`parsed_coord_steps = 0`, `false_found_candidate_steps = 118`), the most likely blocker is still the output/decision chain rather than selector design.

## Artifacts
- Smoke metrics: `smoke_recent_k_10ep/metrics.json`
- Smoke log validation: `smoke_recent_k_10ep/step_log_validation.json`
- Pilot summary table: `pilot_50/pilot_table.csv`
- Pilot 10 failure cases: `pilot_50/failure_cases_10.csv`
- Full pilot logs per selector: `pilot_50/recent_k/`, `pilot_50/uniform_k/`, `pilot_50/scm/`
- Chunk-level logs: `pilot_50/chunks/`
- Full run log: `pilot_50_run.log`
