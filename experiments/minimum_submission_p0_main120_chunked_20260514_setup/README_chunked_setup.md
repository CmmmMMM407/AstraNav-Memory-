# minimum_submission_p0_main120_chunked_20260514 Setup

This setup replaces the stalled long-process run `minimum_submission_p0_main120_20260514`, which was synced as `minimum_submission_p0_main120_20260514_interrupted_recentk64`.

Changes:
- Added per-episode Habitat/resource cleanup: `sim.close()`, delete large episode-local objects, `gc.collect()`, and `torch.cuda.empty_cache()`.
- Switched to 20-episode chunks.
- Added chunk watchdog timeout: 3600 seconds.
- Added single-episode fallback watchdog: 1200 seconds.
- Added global `skipped_episodes.csv`; an episode that times out in fallback is skipped for all later selectors/chunks.

Scope:
- DS16-C50, HM3D-OVON val_unseen, K=50.
- Selectors: recent_k, uniform_k, scm.
- This is the P0 main-selector subset, not full document Minimum Submission with budget/compression/parser studies.
