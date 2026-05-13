AstraNav-Memory Environment Status
Date: 2026-05-13
Host: connect.bjb2.seetacloud.com
Goal: Align runtime with official AstraNav-Memory README Habitat requirements.

Official README target
- habitat-sim: clone official facebookresearch/habitat-sim and checkout v0.2.3
- habitat-lab: clone official chongchong2025/habitat-lab and checkout v0.2.3_waypoint
- install habitat-lab and habitat-baselines from that source tree

Source provenance used on server
- habitat-sim source: /root/autodl-tmp/AstraNav-Memory/train_code/habitat-sim
  origin: https://github.com/facebookresearch/habitat-sim.git
  commit: fffa54376766602c4f12e30d0ee6100d56dd7a96
  describe: v0.2.3
- habitat-lab clean source export: /root/autodl-tmp/AstraNav-Memory/train_code/_official_deps/habitat-lab_v0.2.3_waypoint
  exported from: /root/autodl-tmp/AstraNav-Memory/train_code/habitat-lab_bak_20260511
  origin of exported tree: https://github.com/chongchong2025/habitat-lab
  source commit: 0ed0f8374d71e5a85b7d8b23bea8d3b7598cd65f
  source branch: v0.2.3_waypoint
  note: clean export was used to avoid dirty untracked files in the backup checkout.

Runtime package state after alignment
- python: 3.9.23
- cmake: 3.31.10
- numpy: 1.26.4
- transformers: 4.57.1
- habitat-sim: 0.2.3
- habitat-lab: 0.2.3
- habitat-baselines: 0.2.3

Resolved issue
- Previous runtime had habitat_sim 0.2.5 and habitat-lab 0.2.5-era compatibility handling, which did not match the official README target.
- During official alignment, NumPy had drifted to 2.0.2. That broke quaternion and habitat-sim imports because this Habitat 0.2.3 stack is built against NumPy 1.x ABI.
- NumPy was cleaned and pinned back to 1.26.4 so the official Habitat stack can actually run.

Live import verification
- import quaternion: OK
- import habitat_sim: OK, version 0.2.3
- import habitat: OK, path /root/autodl-tmp/AstraNav-Memory/train_code/_official_deps/habitat-lab_v0.2.3_waypoint/habitat-lab/habitat/__init__.py
- import habitat_baselines: OK, path /root/autodl-tmp/AstraNav-Memory/train_code/_official_deps/habitat-lab_v0.2.3_waypoint/habitat-baselines/habitat_baselines/__init__.py
- python ovon_nav_experiment.py --help: OK

Script path cleanup
- Added /root/autodl-tmp/experiments/_tools/astranav_env_official.sh
- Updated these scripts to source the official env helper instead of exporting the old habitat-lab_bak_20260511 path:
  - /root/autodl-tmp/experiments/_tools/run_pilot_v6c_sequence.sh
  - /root/autodl-tmp/experiments/_tools/run_scm_chunked_v6c.sh
  - /root/autodl-tmp/run_astranav_batch.sh
- Result: experiment entry scripts no longer inject the old backup habitat path through PYTHONPATH.

Smoke execution proof
- command: python ovon_nav_experiment.py --selector recent_k --memory-k 50 --episodes-file /root/autodl-tmp/episode_lists/smoke_10_val_unseen.json --max-episodes 1 --max-steps 5 --experiment-dir /root/autodl-tmp/experiments/_smoke_official_align_20260513/recent_k_1ep --checkpoint ./checkpoint-20000 --name official_align_recent_k_1ep
- result: exit 0
- observed output: sr=1.0, spl=0.6158940732557917, steps=30, avg_steps_per_sec=5.457278745765191, mem=9196MiB

Caveats
- habitat-lab emits a gym deprecation warning at import time. This is expected for the official older stack and does not indicate a mismatch.
- habitat-baselines import emits an ifcfg warning because network interface utilities are absent in the container. This does not block import or the experiment CLI help path.
