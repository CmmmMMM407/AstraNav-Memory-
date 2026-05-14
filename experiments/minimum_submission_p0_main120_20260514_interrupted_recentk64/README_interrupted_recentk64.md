# Interrupted Snapshot: minimum_submission_p0_main120_20260514

This directory is a synced partial snapshot of the stalled long-process run before switching to chunked execution. It is not a completed main120 result.

## Interruption

```text
interrupted_label=interrupted_recentk64
interrupted_at=2026-05-14T18:54:48+08:00
reason=recent_k long-process stall after 64 episodes; GPU util 0 while python held GPU/CPU memory; switching to chunked watchdog runner
next_action=sync partial logs, stop stuck process, patch resource cleanup, run 20-episode chunks with timeout/skip policy
```

## Partial Progress

- Selector in progress: `recent_k`
- Episodes with step logs: 64 / 120
- Step rows: 676
- terminal_found_eps: 22
- raw_found_eps: 22
- parsed_coord_steps: 654
- hash_field_rows: 676
- failure_rows: 55
- failure_reasons: {'not_reached_goal': 53, 'path_planning_failed': 2}

## Last Logged Step

- episode_id: `614`
- scene_id: `00835-q3zU7Yy5E5s`
- goal: `picture`
- step: `445`
- raw_model_output: `found`
- is_final_decision: `True`

## Follow-up

The run should be replaced by 20-episode chunked execution with per-chunk watchdog timeout and synchronized skip policy across selectors.
