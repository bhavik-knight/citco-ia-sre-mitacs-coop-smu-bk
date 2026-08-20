#!/usr/bin/env python3
"""
scripts/generate_llm_repo_worklogs.py

Purpose
-------
Creates dedicated work-log files for ml-rpa-status-llm-agent and
core-smart-rpa-llm-ecr-image commits (author: bbhagat@citco.com,
internship period only).

Output
------
  smu/work-logs/2026-08/2026-08-05-llm-agent.md   ← one file per date
  smu/work-logs/2026-08/2026-08-06-llm-agent.md
  ...

Format
------
  # Work Log — 2026-08-05 (Wednesday) — LLM Agent (IISS-824)
  **Week:** W22 | **Total Hours:** 8 hrs
  | # | JIRA | Repository | Commit |
  |---|------|------------|--------|
  | 1 | IISS-824 | ml-rpa-status-llm-agent | ... |
  ...
  **Daily Total: 8 hrs**

Stays on feature/work-logs — commits at the end.

Usage
-----
    uv run python scripts/generate_llm_repo_worklogs.py
"""

import re
import subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path

# ── config ────────────────────────────────────────────────────────────────────

REPO_ROOT        = Path(__file__).resolve().parent.parent
LOGS_ROOT        = REPO_ROOT / "smu" / "work-logs"
INTERNSHIP_START = date(2026, 3, 15)
MY_EMAIL         = "bbhagat@citco.com"
JIRA             = "IISS-824"

REPOS = [
    {
        "path": Path(r"C:\Users\bbhagat\dev_work\AWS_Projects\ml-rpa-status-llm-agent"),
        "name": "ml-rpa-status-llm-agent",
    },
    {
        "path": Path(r"C:\Users\bbhagat\dev_work\AWS_Projects\core-smart-rpa-llm-ecr-image"),
        "name": "core-smart-rpa-llm-ecr-image",
    },
]

SKIP_PATTERNS = [
    "chore: bump version",
    "Merge branch 'release",
    "Merge branch 'main",
    "Merge pull request",
]

# ── helpers ───────────────────────────────────────────────────────────────────

def git(args: list[str], cwd: Path) -> str:
    r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip()

def git_repo(args: list[str]) -> str:
    return git(args, cwd=REPO_ROOT)

def should_skip(msg: str) -> bool:
    return any(p.lower() in msg.lower() for p in SKIP_PATTERNS)

def week_label(d: date) -> str:
    delta = (d - INTERNSHIP_START).days
    return f"W{max(delta // 7 + 1, 1)}" if delta >= 0 else "Pre"


# ── gather ────────────────────────────────────────────────────────────────────

def gather() -> dict[str, list[dict]]:
    """Returns {date_str: [{repo, msg}]}  — only my commits, deduped."""
    by_date: dict[str, list[dict]] = defaultdict(list)

    for repo in REPOS:
        raw = git(
            ["log", "--all",
             f"--author={MY_EMAIL}",
             "--format=%ad|%s",
             "--date=short",
             f"--after={INTERNSHIP_START.isoformat()}"],
            cwd=repo["path"],
        )
        seen: set[tuple[str, str]] = set()
        for line in raw.splitlines():
            if not line.strip():
                continue
            parts = line.split("|", 1)
            if len(parts) < 2:
                continue
            day_str, msg = parts[0].strip(), parts[1].strip()
            if should_skip(msg):
                continue
            key = (repo["name"], msg)
            if key in seen:
                continue
            seen.add(key)
            by_date[day_str].append({"repo": repo["name"], "msg": msg})

    return by_date


# ── write ─────────────────────────────────────────────────────────────────────

def write_logs(by_date: dict[str, list[dict]]) -> list[Path]:
    written = []
    for day_str in sorted(by_date):
        rows = by_date[day_str]
        d = date.fromisoformat(day_str)
        month_dir = LOGS_ROOT / d.strftime("%Y-%m")
        month_dir.mkdir(parents=True, exist_ok=True)

        log_path = month_dir / f"{day_str}-llm-agent.md"

        lines = [
            f"# Work Log — {day_str} ({d.strftime('%A')}) — LLM Agent ({JIRA})",
            "",
            f"**Week:** {week_label(d)} | **JIRA:** {JIRA} | **Repos:** ml-rpa-status-llm-agent, core-smart-rpa-llm-ecr-image",
            "",
            "| # | Repository | Commit |",
            "|---|------------|--------|",
        ]
        for i, row in enumerate(rows, 1):
            lines.append(f"| {i} | {row['repo']} | {row['msg']} |")
        lines += ["", f"**Total commits this day: {len(rows)}**", ""]

        log_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  written: smu/work-logs/{d.strftime('%Y-%m')}/{day_str}-llm-agent.md  ({len(rows)} commits)")
        written.append(log_path)
    return written


# ── git ops ───────────────────────────────────────────────────────────────────

def commit_files(written: list[Path]):
    print("\n── Staging and committing ──")
    for p in written:
        git_repo(["add", str(p.relative_to(REPO_ROOT))])
    git_repo(["add", "scripts/generate_llm_repo_worklogs.py"])

    staged = git_repo(["diff", "--cached", "--name-only"])
    if not staged.strip():
        print("  Nothing new to commit.")
        return

    msg = (
        f"feat(work-logs): dedicated LLM agent work logs ({JIRA})\n\n"
        "Standalone -llm-agent.md files per date in 2026-08/\n"
        "Repos: ml-rpa-status-llm-agent, core-smart-rpa-llm-ecr-image\n"
        f"Author filter: {MY_EMAIL} | Period: {INTERNSHIP_START} onwards\n"
        f"{len(written)} files created\n"
    )
    print(git_repo(["commit", "-m", msg]))
    print("  ✓ Committed.")


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    branch = git_repo(["branch", "--show-current"])
    if branch != "feature/work-logs":
        print(f"ERROR: must be on feature/work-logs (currently on {branch})")
        print("       run: git checkout feature/work-logs")
        return

    print(f"Branch    : {branch}")
    print(f"Author    : {MY_EMAIL}")
    print(f"Start     : {INTERNSHIP_START}")
    print()

    print("── Gathering commits ──")
    by_date = gather()
    total = sum(len(v) for v in by_date.values())
    print(f"  {total} commits across {len(by_date)} days")

    print("\n── Writing dedicated LLM agent work logs ──")
    written = write_logs(by_date)

    commit_files(written)
    print(f"\n✓ Done. {len(written)} -llm-agent.md files in smu/work-logs/")


if __name__ == "__main__":
    main()
