#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse feature_list.json → colored DAG with status indicators."""
from __future__ import annotations

import json
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    # Enable ANSI on Windows
    import os
    os.system("")

# ── ANSI ──
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
ORANGE = "\033[38;5;208m"
DIM = "\033[90m"
BOLD = "\033[1m"
RST = "\033[0m"
BG_GREEN = "\033[42;30m"
BG_RED = "\033[41;37m"
BG_YELLOW = "\033[43;30m"
BG_ORANGE = "\033[48;5;208;30m"


def idx_str(idx: float) -> str:
    return str(int(idx)) if idx == int(idx) else str(idx)


def main() -> None:
    # ── Load ──
    p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("feature_list.json")
    if not p.exists():
        print(f"{RED}ERR: {p} not found{RST}", file=sys.stderr)
        sys.exit(1)
    raw = json.loads(p.read_text("utf-8"))

    # ── Parse ──
    tasks: dict[float, dict] = {}
    for f in raw:
        st = f.get("passes")
        if st in ("archived", "skipped"):
            continue
        idx = f["index"]
        desc = f["description"]
        # Shorten: take part before first colon
        for sep in ("\uff1a", ":"):
            if sep in desc:
                desc = desc.split(sep)[0]
                break
        if len(desc) > 28:
            desc = desc[:25] + "..."
        if st is True:
            status = "done"
        elif isinstance(st, str):
            status = "discuss"
        else:
            status = "todo"
        tasks[idx] = {
            "desc": desc,
            "st": status,
            "deps": list(f.get("depends_on", [])),
            "mod": f["module"],
        }

    # ── Classify blocked ──
    for idx, t in tasks.items():
        if t["st"] == "todo" and t["deps"]:
            if any(tasks.get(d, {}).get("st") != "done" for d in t["deps"]):
                t["st"] = "blocked"

    # ── Build graph ──
    downstream: dict[float, list[float]] = {i: [] for i in tasks}
    for idx, t in tasks.items():
        for d in t["deps"]:
            if d in downstream:
                downstream[d].append(idx)

    in_graph = set()
    for idx, t in tasks.items():
        if t["deps"] or downstream[idx]:
            in_graph.add(idx)
            for d in t["deps"]:
                in_graph.add(d)

    # ── Helpers ──
    status_cfg = {
        "done":    (GREEN,  " DONE "),
        "todo":    (RED,    " TODO "),
        "blocked": (YELLOW, " WAIT "),
        "discuss": (ORANGE, " ???  "),
    }

    def badge(st: str) -> str:
        color, label = status_cfg[st]
        bg = {"done": BG_GREEN, "todo": BG_RED, "blocked": BG_YELLOW, "discuss": BG_ORANGE}[st]
        return f"{bg}{label}{RST}"

    def node_line(idx: float, prefix: str = "") -> str:
        t = tasks[idx]
        color = status_cfg[t["st"]][0]
        mod_tag = f"{DIM}({t['mod']}){RST}"
        return f"{prefix}{badge(t['st'])} {color}#{idx_str(idx)} {t['desc']}{RST} {mod_tag}"

    # ── Print header ──
    print()
    print(f"  {BOLD}Feature Progress DAG{RST}")
    print(f"  {BG_GREEN} DONE {RST} = completed  "
          f"{BG_RED} TODO {RST} = ready  "
          f"{BG_YELLOW} WAIT {RST} = blocked  "
          f"{BG_ORANGE} ???  {RST} = discuss")
    print()

    # ── Print dependency tree ──
    printed: set[float] = set()

    def print_tree(idx: float, prefix: str = "  ", connector: str = "") -> None:
        if idx not in tasks or idx in printed:
            return
        printed.add(idx)
        print(f"{connector}{node_line(idx)}")
        children = sorted(downstream.get(idx, []))
        for i, child in enumerate(children):
            is_last = (i == len(children) - 1)
            if prefix:
                child_prefix = prefix + ("    " if is_last else "|   ")
                child_conn = prefix + ("`-- " if is_last else "|-- ")
            else:
                child_prefix = "    "
                child_conn = "|-- "
            print_tree(child, child_prefix, child_conn)

    # Roots of dependency chains
    roots = sorted(idx for idx in in_graph if not tasks.get(idx, {}).get("deps"))
    if roots:
        print(f"  {BOLD}Dependency Chains{RST}")
        print()
        for r in roots:
            print_tree(r, "  ", "  ")
            print()

    # ── Standalone (not in any chain) ──
    standalone = sorted(idx for idx in tasks if idx not in in_graph)
    standalone_todo = [i for i in standalone if tasks[i]["st"] != "done"]
    standalone_done = [i for i in standalone if tasks[i]["st"] == "done"]

    if standalone_todo:
        print(f"  {BOLD}Independent Tasks{RST}")
        print()
        for idx in standalone_todo:
            print(f"  {node_line(idx)}")
        print()

    if standalone_done:
        print(f"  {DIM}+ {len(standalone_done)} completed independent tasks{RST}")
        print()

    # ── Stats bar ──
    counts: dict[str, int] = {}
    for t in tasks.values():
        counts[t["st"]] = counts.get(t["st"], 0) + 1
    total = sum(counts.values())
    done_n = counts.get("done", 0)
    pct = done_n * 100 // total if total else 0

    bar_w = 30
    filled = pct * bar_w // 100
    bar = f"{GREEN}{'=' * filled}{RST}{DIM}{'.' * (bar_w - filled)}{RST}"

    print(f"  {BOLD}Progress{RST}  [{bar}] {BOLD}{pct}%{RST}  ({done_n}/{total})")

    parts = []
    for key, label in [("done", "done"), ("todo", "ready"), ("blocked", "blocked"), ("discuss", "discuss")]:
        n = counts.get(key, 0)
        if n:
            color = status_cfg[key][0]
            parts.append(f"{color}{n} {label}{RST}")
    print(f"            {' | '.join(parts)}")
    print()


if __name__ == "__main__":
    main()
