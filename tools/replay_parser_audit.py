#!/usr/bin/env python3
import argparse
import csv
import json
import os
import re
from pathlib import Path


COORD_RE = re.compile(r"<coordinate>\s*(\[.*?\])\s*</coordinate>", re.IGNORECASE)
STRICT_FOUND_RE = re.compile(r"^\s*found\s*$", re.IGNORECASE)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--source-step-logs", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--source-selector", default="recent_k")
    p.add_argument("--note", default="Replay audit from recent_k pilot step logs; parser-only comparison on fixed raw outputs.")
    return p.parse_args()


def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def parse_coord(raw_text):
    if not raw_text:
        return None
    m = COORD_RE.search(raw_text)
    if not m:
        return None
    try:
        parsed = json.loads(m.group(1))
    except Exception:
        return None
    if not isinstance(parsed, list) or len(parsed) != 2:
        return None
    return parsed


def audit_row(row, parser_mode):
    raw_text = str(row.get("raw_model_output") or "")
    empty_output = (raw_text.strip() == "")
    coord = parse_coord(raw_text)
    if parser_mode == "strict_found":
        found = bool(STRICT_FOUND_RE.match(raw_text))
    else:
        found = ("found" in raw_text.lower())
    frontier_candidates = row.get("frontier_candidates") or []
    valid_coord = coord is not None and len(frontier_candidates) > 0
    return {
        "episode_id": row.get("episode_id"),
        "scene_id": row.get("scene_id"),
        "goal": row.get("goal"),
        "source_selector": row.get("selector") or row.get("source_selector"),
        "parser_mode": parser_mode,
        "step": row.get("step"),
        "raw_model_output": raw_text,
        "empty_output": empty_output,
        "audit_found": found,
        "audit_coord": coord,
        "audit_valid_coord": valid_coord,
        "frontier_candidate_count": len(frontier_candidates),
    }


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_yaml_like(path, data):
    with open(path, "w", encoding="utf-8") as f:
        for key, value in data.items():
            if value is None:
                f.write(f"{key}: null\n")
            elif isinstance(value, bool):
                f.write(f"{key}: {'true' if value else 'false'}\n")
            elif isinstance(value, (int, float)):
                f.write(f"{key}: {value}\n")
            else:
                f.write(f'{key}: "{value}"\n')


def summarize(rows, parser_mode, source_selector, note):
    num_steps = len(rows)
    episode_ids = {str(r.get("episode_id")) for r in rows}
    empty_steps = sum(1 for r in rows if r["empty_output"])
    found_steps = sum(1 for r in rows if r["audit_found"])
    coord_steps = sum(1 for r in rows if r["audit_coord"] is not None)
    valid_coord_steps = sum(1 for r in rows if r["audit_valid_coord"])
    denom = float(num_steps) if num_steps else 1.0
    return {
        "source_selector": source_selector,
        "parser_mode": parser_mode,
        "num_episodes": len(episode_ids),
        "num_steps": num_steps,
        "empty_output_steps": empty_steps,
        "empty_output_rate": empty_steps / denom,
        "parsed_found_steps": found_steps,
        "parsed_found_rate": found_steps / denom,
        "parsed_coord_steps": coord_steps,
        "parsed_coord_rate": coord_steps / denom,
        "valid_coord_steps": valid_coord_steps,
        "valid_coord_rate": valid_coord_steps / denom,
        "note": note,
    }


def main():
    args = parse_args()
    source_path = Path(args.source_step_logs)
    out_root = Path(args.output_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    source_rows = load_jsonl(source_path)
    parser_modes = ["original", "strict_found", "coord_validator"]
    summary_rows = []

    write_yaml_like(
        out_root / "config.yaml",
        {
            "run_name": None,
            "benchmark": "hm3d_ovon",
            "checkpoint": "",
            "selector": None,
            "memory_k": 50,
            "episodes_file": None,
            "save_video": False,
            "notes": "",
        },
    )
    write_json(out_root / "metrics.json", {})
    (out_root / "failures.csv").write_text("episode_id,scene_id,goal,reason,step\n", encoding="utf-8")

    for parser_mode in parser_modes:
        mode_rows = [audit_row(row, parser_mode) for row in source_rows]
        summary = summarize(mode_rows, parser_mode, args.source_selector, args.note)
        summary_rows.append(summary)

        mode_dir = out_root / parser_mode
        mode_dir.mkdir(parents=True, exist_ok=True)
        write_yaml_like(
            mode_dir / "config.yaml",
            {
                "run_name": f"experiments__parser_audit__{parser_mode}",
                "benchmark": "hm3d_ovon",
                "entrypoint": "",
                "checkpoint": "",
                "selector": args.source_selector,
                "parser_mode": parser_mode,
                "memory_k": 50,
                "episodes_file": "",
                "save_video": False,
                "status": "completed",
                "notes": args.note,
            },
        )
        write_json(mode_dir / "metrics.json", summary)
        write_jsonl(mode_dir / "step_logs.jsonl", mode_rows)
        (mode_dir / "failures.csv").write_text("episode_id,scene_id,goal,reason,step\n", encoding="utf-8")

    with open(out_root / "parser_audit_summary.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "source_selector",
                "parser_mode",
                "num_episodes",
                "num_steps",
                "empty_output_steps",
                "empty_output_rate",
                "parsed_found_steps",
                "parsed_found_rate",
                "parsed_coord_steps",
                "parsed_coord_rate",
                "valid_coord_steps",
                "valid_coord_rate",
                "note",
            ],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"wrote parser audit to {out_root}")


if __name__ == "__main__":
    main()
