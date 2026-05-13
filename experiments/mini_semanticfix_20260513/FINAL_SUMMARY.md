# mini_semanticfix_20260513 Final Summary

## Smoke rerun
- episodes: 10
- success_count: 3
- avg_sr: 0.3
- avg_spl: 0.04084268111399202
- avg_steps: 429.4
- avg_steps_per_sec: 12.742827280312714
- avg_gpu_mem_used_mib: 18427.0
- max_gpu_mem_used_mib: 24067

## Parsing signal
- logged_steps: 99
- raw_nonempty_steps: 99
- parsed_coord_steps: 92
- parsed_found_steps: 7
- false_found_candidate_steps: 7

## Pilot table
| selector | episodes | avg_sr | avg_spl | avg_steps | avg_steps_per_sec | avg_gpu_mem_used_mib | max_gpu_mem_used_mib | wall_time_sec | success_count |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| recent_k | 50 | 0.18 | 0.022534310070694112 | 505.92 | 10.352893230140205 | 22949.42 | 24081 | 2545.7964589595795 | 9 |
| uniform_k | 50 | 0.18 | 0.022534310070694112 | 505.92 | 10.003681018224768 | 22949.42 | 24081 | 2690.3632094860077 | 9 |
| scm | 50 | 0.18 | 0.022534310070694112 | 505.92 | 11.418852226658212 | 22801.1 | 24081 | 2315.5147635936737 | 9 |

## Failure cases sample
- recent_k episode 1237 scene 00869-MHPLjHsuG27 goal dishwasher reason path_planning_failed step 276
- recent_k episode 6989 scene 00844-q5QZSEeHe5g goal exercise bike reason path_planning_failed step 263
- recent_k episode 3693 scene 00823-7MXmsvcQjpJ goal guitar reason path_planning_failed step 496
- recent_k episode 5908 scene 00873-bxsVRursffK goal refrigerator reason path_planning_failed step 304
- recent_k episode 3983 scene 00823-7MXmsvcQjpJ goal guitar reason path_planning_failed step 353
- recent_k episode 666 scene 00802-wcojb4TFT35 goal picture reason path_planning_failed step 209
- recent_k episode 4175 scene 00800-TEEsavR23oF goal pillow reason not_reached_goal step 678
- recent_k episode 1054 scene 00824-Dd4bFSTQ8gi goal pillow reason not_reached_goal step 641
- recent_k episode 810 scene 00824-Dd4bFSTQ8gi goal flower vase reason not_reached_goal step 617
- recent_k episode 2188 scene 00813-svBbv1Pavdk goal flower vase reason not_reached_goal step 635

## Takeaway
- The repaired semantic pipeline is active and stable in the rerun smoke and pilot.
- Selector outcome metrics remain identical across recent_k / uniform_k / scm on this 50-episode pilot, while SCM is the fastest of the three.
- In the 10 sampled failure cases, the dominant visible reasons are path_planning_failed and not_reached_goal.
