#!/usr/bin/env python3
import csv, json, os, collections, glob
from pathlib import Path
BASE=Path('/root/autodl-tmp/experiments/minimum_submission_p0_main120_chunked_20260514')
SELECTORS=['recent_k','uniform_k','scm']
print('base', BASE)
pid=BASE/'run.sequence.pid'
if pid.exists():
    p=pid.read_text().strip()
    print('sequence_pid', p, 'alive', Path('/proc') .joinpath(p).exists())
meta=BASE/'run_metadata.txt'
if meta.exists():
    print('metadata_tail')
    print('\n'.join(meta.read_text().strip().splitlines()[-10:]))
status=BASE/'sequence_status.log'
if status.exists():
    lines=status.read_text().strip().splitlines()
    print('sequence_status_tail')
    print('\n'.join(lines[-25:]))
skip=BASE/'skipped_episodes.csv'
if skip.exists():
    rows=list(csv.DictReader(skip.open()))
    print('skipped_count', len(rows))
    if rows:
        print('skipped_tail')
        for r in rows[-10:]: print(r)
for sel in SELECTORS:
    print('\nselector', sel)
    root=BASE/sel
    if not root.exists():
        print('state not_started')
        continue
    run_dirs=sorted(root.glob('chunk_*/run')) + sorted(root.glob('chunk_*/fallback_single_episodes/episode_*'))
    metrics=[]; failures=[]; steps=[]; statuses=[]
    for d in run_dirs:
        st=d/'run_status.json'
        if st.exists():
            try: statuses.append((str(d.relative_to(BASE)), json.load(st.open())))
            except Exception: pass
        mp=d/'metrics.json'
        if mp.exists():
            try: metrics.append((str(d.relative_to(BASE)), json.load(mp.open())))
            except Exception: pass
        fp=d/'failures.csv'
        if fp.exists():
            try:
                failures.extend(list(csv.DictReader(fp.open())))
            except Exception: pass
        sp=d/'step_logs.jsonl'
        if sp.exists():
            for line in sp.open():
                if line.strip():
                    try: steps.append(json.loads(line))
                    except Exception: pass
    completed_eps=[]
    for _,m in metrics:
        completed_eps.extend(m.get('episodes',[]))
    by_ep=collections.defaultdict(list)
    for r in steps: by_ep[str(r.get('episode_id'))].append(r)
    reasons=collections.Counter((r.get('reason') or r.get('failure_reason') or '').strip() for r in failures)
    timed_out=sum(1 for _,s in statuses if s.get('timed_out'))
    nonzero=sum(1 for _,s in statuses if s.get('status') not in (0,None) and not s.get('timed_out'))
    print('run_units', len(run_dirs), 'metrics_units', len(metrics), 'completed_metric_episodes', len(completed_eps), 'episodes_with_steps', len(by_ep))
    print('step_rows', len(steps), 'terminal_found_eps', sum(1 for ep,rs in by_ep.items() if any(r.get('is_final_decision') for r in rs)), 'hash_field_rows', sum(1 for r in steps if 'selection_fingerprint' in r))
    print('failure_rows', len(failures), 'failure_reasons', dict(reasons))
    print('timed_out_units', timed_out, 'nonzero_units', nonzero)
    if completed_eps:
        avg_sr=sum(e.get('sr',0) for e in completed_eps)/len(completed_eps)
        avg_spl=sum(e.get('spl',0) for e in completed_eps)/len(completed_eps)
        print('aggregate_so_far avg_sr', avg_sr, 'avg_spl', avg_spl)
