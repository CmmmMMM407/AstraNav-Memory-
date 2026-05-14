#!/usr/bin/env python3
import csv
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT = Path('/root/autodl-tmp/AstraNav-Memory/inference_code/hm3d-online')
BASE = Path('/root/autodl-tmp/experiments/minimum_submission_p0_main120_chunked_20260514')
SOURCE = Path('/root/autodl-tmp/episode_lists/minimum_main120_val_unseen_20260514.json')
CHECKPOINT = './checkpoint-20000'
SELECTORS = ['recent_k', 'uniform_k', 'scm']
CHUNK_SIZE = 20
MAX_STEPS = 600
MEMORY_K = 50
CHUNK_TIMEOUT_SEC = 3600
EPISODE_TIMEOUT_SEC = 1200

BASE.mkdir(parents=True, exist_ok=True)
STATUS = BASE / 'sequence_status.log'
SKIP = BASE / 'skipped_episodes.csv'
MANIFEST = BASE / 'chunk_manifest.csv'

def now():
    return datetime.now().astimezone().isoformat(timespec='seconds')

def log(msg):
    line = f'[{now()}] {msg}'
    print(line, flush=True)
    with STATUS.open('a') as f:
        f.write(line + '\n')

def ep_key(ep):
    return f"{ep.get('scan_id')}|{ep.get('episode_index')}|{ep.get('object_category')}"

def load_skips():
    if not SKIP.exists():
        return set()
    with SKIP.open(newline='') as f:
        return {row['skip_key'] for row in csv.DictReader(f) if row.get('skip_key')}

def append_skip(ep, selector, chunk_id, reason):
    exists = SKIP.exists()
    with SKIP.open('a', newline='') as f:
        fieldnames = ['skip_key','scan_id','scan_id_suffix','episode_index','object_category','first_selector','chunk_id','reason','timestamp']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            w.writeheader()
        w.writerow({
            'skip_key': ep_key(ep),
            'scan_id': ep.get('scan_id'),
            'scan_id_suffix': ep.get('scan_id_suffix'),
            'episode_index': ep.get('episode_index'),
            'object_category': ep.get('object_category'),
            'first_selector': selector,
            'chunk_id': chunk_id,
            'reason': reason,
            'timestamp': now(),
        })

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def run_ovon(selector, episode_file, out_dir, name, timeout_sec):
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, 'ovon_nav_experiment.py',
        '--selector', selector,
        '--memory-k', str(MEMORY_K),
        '--episodes-file', str(episode_file),
        '--max-episodes', '999999',
        '--max-steps', str(MAX_STEPS),
        '--experiment-dir', str(out_dir),
        '--checkpoint', CHECKPOINT,
        '--name', name,
    ]
    with (out_dir / 'command.json').open('w') as f:
        json.dump({'cmd': cmd, 'timeout_sec': timeout_sec, 'started_at': now()}, f, indent=2)
    with (out_dir / 'run.log').open('w') as logf:
        try:
            res = subprocess.run(cmd, cwd=str(PROJECT), stdout=logf, stderr=subprocess.STDOUT, timeout=timeout_sec)
            status = res.returncode
            timed_out = False
        except subprocess.TimeoutExpired as e:
            status = 124
            timed_out = True
            logf.write(f'\n[TIMEOUT] timeout_sec={timeout_sec} at {now()}\n')
        except Exception as e:
            status = 255
            timed_out = False
            logf.write(f'\n[EXCEPTION] {type(e).__name__}: {e} at {now()}\n')
    with (out_dir / 'run_status.json').open('w') as f:
        json.dump({'status': status, 'timed_out': timed_out, 'finished_at': now()}, f, indent=2)
    return status, timed_out

def fallback_per_episode(selector, original_eps, chunk_id, chunk_dir):
    log(f'FALLBACK_START selector={selector} chunk={chunk_id} episodes={len(original_eps)}')
    fb_base = chunk_dir / 'fallback_single_episodes'
    for global_i, ep in original_eps:
        if ep_key(ep) in load_skips():
            log(f'FALLBACK_SKIP_ALREADY selector={selector} chunk={chunk_id} global_index={global_i} key={ep_key(ep)}')
            continue
        ep_file = fb_base / f'episode_{global_i:03d}.json'
        out_dir = fb_base / f'episode_{global_i:03d}'
        write_json(ep_file, [ep])
        log(f'EPISODE_START selector={selector} chunk={chunk_id} global_index={global_i} key={ep_key(ep)}')
        status, timed_out = run_ovon(selector, ep_file, out_dir, f'minimum_p0_chunked_{selector}_ep{global_i:03d}', EPISODE_TIMEOUT_SEC)
        log(f'EPISODE_END selector={selector} chunk={chunk_id} global_index={global_i} status={status} timed_out={timed_out}')
        if timed_out:
            append_skip(ep, selector, chunk_id, 'single_episode_timeout_after_chunk_timeout')
            log(f'EPISODE_MARK_SKIPPED selector={selector} chunk={chunk_id} global_index={global_i} key={ep_key(ep)}')

def main():
    episodes = json.load(SOURCE.open())
    if not SKIP.exists():
        with SKIP.open('w', newline='') as f:
            csv.DictWriter(f, fieldnames=['skip_key','scan_id','scan_id_suffix','episode_index','object_category','first_selector','chunk_id','reason','timestamp']).writeheader()
    with (BASE / 'run_metadata.txt').open('w') as f:
        f.write(f'run_name=minimum_submission_p0_main120_chunked_20260514\n')
        f.write(f'started_at={now()}\n')
        f.write(f'source_interrupted=/root/autodl-tmp/experiments/minimum_submission_p0_main120_20260514\n')
        f.write(f'source_episodes={SOURCE}\n')
        f.write(f'total_source_episodes={len(episodes)}\n')
        f.write(f'selectors={",".join(SELECTORS)}\n')
        f.write(f'chunk_size={CHUNK_SIZE}\n')
        f.write(f'chunk_timeout_sec={CHUNK_TIMEOUT_SEC}\n')
        f.write(f'episode_timeout_sec={EPISODE_TIMEOUT_SEC}\n')
        f.write(f'memory_k={MEMORY_K}\n')
        f.write(f'max_steps={MAX_STEPS}\n')
        f.write('resource_cleanup=sim.close + del large objects + gc.collect + torch.cuda.empty_cache per completed episode\n')
        f.write('skip_policy=global skip after single-episode timeout; skipped episode excluded for all later selector/chunk runs\n')
    if not MANIFEST.exists():
        with MANIFEST.open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['chunk_id','start','end_exclusive','num_source_episodes'])
            w.writeheader()
            for start in range(0, len(episodes), CHUNK_SIZE):
                end = min(start + CHUNK_SIZE, len(episodes))
                w.writerow({'chunk_id': f'{start:03d}_{end-1:03d}', 'start': start, 'end_exclusive': end, 'num_source_episodes': end-start})
    log('RUN_START')
    for start in range(0, len(episodes), CHUNK_SIZE):
        end = min(start + CHUNK_SIZE, len(episodes))
        chunk_id = f'{start:03d}_{end-1:03d}'
        indexed_eps = list(enumerate(episodes[start:end], start))
        for selector in SELECTORS:
            skipped = load_skips()
            filtered = [(i, ep) for i, ep in indexed_eps if ep_key(ep) not in skipped]
            chunk_root = BASE / selector / f'chunk_{chunk_id}'
            chunk_root.mkdir(parents=True, exist_ok=True)
            write_json(chunk_root / 'source_chunk.json', [ep for _, ep in indexed_eps])
            write_json(chunk_root / 'episodes_filtered.json', [ep for _, ep in filtered])
            with (chunk_root / 'chunk_info.json').open('w') as f:
                json.dump({'chunk_id': chunk_id, 'selector': selector, 'start': start, 'end_exclusive': end, 'num_source': len(indexed_eps), 'num_filtered': len(filtered), 'skips_at_start': sorted(skipped)}, f, indent=2)
            if not filtered:
                log(f'CHUNK_EMPTY selector={selector} chunk={chunk_id}')
                continue
            out_dir = chunk_root / 'run'
            log(f'CHUNK_START selector={selector} chunk={chunk_id} num_episodes={len(filtered)}')
            status, timed_out = run_ovon(selector, chunk_root / 'episodes_filtered.json', out_dir, f'minimum_p0_chunked_{selector}_{chunk_id}', CHUNK_TIMEOUT_SEC)
            log(f'CHUNK_END selector={selector} chunk={chunk_id} status={status} timed_out={timed_out}')
            if timed_out:
                fallback_per_episode(selector, filtered, chunk_id, chunk_root)
            elif status != 0:
                with (chunk_root / 'NONZERO_STATUS.txt').open('w') as f:
                    f.write(f'status={status}\nfinished_at={now()}\n')
                log(f'CHUNK_NONZERO selector={selector} chunk={chunk_id} status={status}')
    with (BASE / 'run_metadata.txt').open('a') as f:
        f.write(f'finished_at={now()}\n')
        f.write('exit_status=0\n')
    log('RUN_END exit_status=0')

if __name__ == '__main__':
    main()
