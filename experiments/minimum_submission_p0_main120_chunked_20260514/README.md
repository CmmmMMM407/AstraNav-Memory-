# minimum_submission_p0_main120_chunked_20260514

Chunked P0 main selector run for AstraNav-Memory PRCV experiments.

Generated files:

- `aggregate_main120_summary.csv` / `.md`: compact selector-level metrics.
- `selector_hash_action_alignment_audit.json` / `.md`: selected-memory versus downstream-action alignment audit.
- `skipped_episodes.csv`: global skip ledger. Empty except header for this run.
- `{recent_k,uniform_k,scm}/chunk_*/run/`: raw chunk metrics, logs, failures, and step logs.

Bottom line: all chunks finished without timeout/skips; metrics are identical across selectors, while the selector audit confirms memory selection differs but downstream model/action outputs remain identical.
