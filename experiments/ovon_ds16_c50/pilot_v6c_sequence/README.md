# Pilot v6c sequence summary (2026-05-13)

This directory stores the remote experiment artifacts synced from the cloud server for the ordered `pilot_v6c_sequence` run.

## Required order executed

1. Fix output chain so `raw_model_output` is non-empty.
2. Re-run parser audit on `recent_k` source logs.
3. Because parseable outputs became non-zero, run the fixed 50-episode pilot for `recent_k`, `uniform_k`, and `scm`.
4. Re-run `scm` in chunked mode after the original monolithic run hit CUDA OOM.

## Fixed episode set

- Source list: `episode_lists/pilot_50_val_unseen.json`
- All three selectors use the same 50-episode list.

## Parser audit gate

Source: `parser_audit/parser_audit_summary.csv`

- `empty_output_steps = 0 / 668`
- `parsed_found_steps = 668 / 668`
- `parsed_coord_steps = 0 / 668`
- `valid_coord_steps = 0 / 668`

Interpretation:

- The gate "non-zero parseable outputs" passed.
- The current repaired output chain is pathological: outputs collapse to `found`, with zero coordinate predictions.
- The replay summary covers 49 episodes with logged steps from the `recent_k` source logs.

## Pilot metrics

| selector | episodes | avg_sr | avg_spl | avg_steps | avg_steps_per_sec |
| --- | ---: | ---: | ---: | ---: | ---: |
| recent_k | 50 | 0.22 | 0.03246377576820025 | 442.5 | 12.80235130710833 |
| uniform_k | 50 | 0.22 | 0.03246377576820025 | 442.5 | 13.317177383982585 |
| scm | 50 | 0.22 | 0.03246377576820025 | 442.5 | 19.489178639739766 |

Interpretation:

- `recent_k`, `uniform_k`, and `scm` have identical SR/SPL/steps on this pilot.
- `scm` differs only in throughput after the chunked rerun.
- Because parser outputs collapse to `found`, this pilot should be treated as a gate/pipeline result, not a final method comparison.

## SCM OOM trace and rerun

- Original partial OOM artifacts: `scm_partial_oom_20260513_0248/`
- Chunked rerun log: `scm_chunked.out`
- Chunked rerun note: `scm_chunked_note.txt`
- Final merged SCM result: `scm/`

The chunked rerun preserved the methodology:

- same selector: `scm`
- same `K=50`
- same fixed 50 episodes
- only changed execution strategy to 5-episode chunks with `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`

## Main caveat for next stage

Do not expand to budget study or minimum submission from these numbers alone. The next blocker is still the output behavior: coordinates never appear, so selector differences are not meaningfully exercised yet.
