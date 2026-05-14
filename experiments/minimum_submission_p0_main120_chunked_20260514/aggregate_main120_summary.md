# Minimum Submission P0 Main120 Chunked Summary

This run covers the P0 main selector subset: Recent-K / Uniform-K / SCM, K=50, 120 HM3D-OVON val_unseen episodes. It is not the full PRCV minimum package.

## Run Status

- started_at: `2026-05-14T19:49:03+08:00`
- finished_at: `2026-05-14T23:36:04+08:00`
- exit_status: `0`
- chunk_size: `20`
- chunk_timeout_sec: `3600`
- episode_timeout_sec: `1200`
- skipped episodes: `0`

## Compact Table

| selector | episodes | SR | SPL | success | failures | avg steps | weighted steps/s | wall min | max GPU MiB | step rows | parsed coord | terminal found | timeouts | failure reasons |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| recent_k | 120 | 0.1500 | 0.0180 | 18 | 102 | 528.6 | 14.12 | 76.4 | 14206 | 1251 | 1207 | 44 | 0 | `{"not_reached_goal": 99, "path_planning_failed": 3}` |
| uniform_k | 120 | 0.1500 | 0.0180 | 18 | 102 | 528.6 | 14.12 | 76.4 | 14206 | 1251 | 1207 | 44 | 0 | `{"not_reached_goal": 99, "path_planning_failed": 3}` |
| scm | 120 | 0.1500 | 0.0180 | 18 | 102 | 528.6 | 15.11 | 71.5 | 13454 | 1251 | 1207 | 44 | 0 | `{"not_reached_goal": 99, "path_planning_failed": 3}` |

## Notes

- All three selectors completed all 120 episodes with `exit_status=0`.
- No chunk watchdog timeout and no globally skipped episode were recorded.
- The three selectors produced identical SR/SPL/failure counts in this run. Treat that as a debugging signal, not a final scientific conclusion.
