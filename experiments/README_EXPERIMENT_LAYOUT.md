# PRCV2026 Experiment Layout

Aligned with official AstraNav-Memory README inference entry points:
- OVON: inference_code/hm3d-online/ovon-nav.py
- GOAT: inference_code/hm3d-online/goat-nav.py

Folders:
- ovon_ds16_c50/: main selector comparison
- budget_study/: K in {20,35,50}
- parser_audit/: original/strict_found/coord_validator
- compression_sensitivity/: DS16-C50 vs DS64-C100
- goat_small/: optional GOAT subset

Every runnable leaf contains: config.yaml / metrics.json / step_logs.jsonl / failures.csv
