# Pilot Screening Summary

- Fixed 50-episode pilot completed for `recent_k`, `uniform_k`, and `scm`.
- All three selectors achieved identical top-line pilot metrics: `SR=0.18`, `SPL=0.05238`.
- Replay parser audit on the fixed `recent_k` pilot logs shows `empty_output_rate=1.0` for `original`, `strict_found`, and `coord_validator`.
- This indicates the current bottleneck is upstream of selector comparison: the model emits empty text outputs, so parser variants cannot recover usable coordinates.
- Recommendation: do not expand to Minimum Submission yet. First stabilize the language-action interface / output generation path, then rerun pilot and parser audit.
