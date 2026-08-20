#!/usr/bin/env python3
"""
scripts/generate_iiss824_worklogs.py

Purpose
-------
Scans ml-rpa-status-llm-agent and core-smart-rpa-llm-ecr-image for all commits
after 2026-03-15 (internship start) and writes/updates daily work-log .md files
under smu/work-logs/<year-month>/<date>.md.

- Skips: pure merge commits, version bumps, and chore: bump version
- Deduplicates by (repo, message) per day
- Adds JIRA: IISS-824 to every row
- Creates the year-month folder if it doesn't exist
- If a work-log file already exists, REPLACES rows that reference either repo
  (leaves all other rows intact)
- Switches the working tree to feature/work-logs, commits, then returns

Usage
-----
    uv run python scripts/generate_iiss824_worklogs.py
"""

import subprocess
import sys
from collections import defaultdict
from datetime import datetime, date
from pathlib import Path

# ── config ────────────────────────────────────────────────────────────────────

REPO_ROOT   = Path(__file__).resolve().parent.parent
LOGS_ROOT   = REPO_ROOT / "smu" / "work-logs"
INTERNSHIP_START = date(2026, 3, 15)

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

JIRA = "IISS-824"

SKIP_PATTERNS = [
    "chore: bump version",
    "Merge branch 'release",
    "Merge branch 'main",
]

# ── helpers ───────────────────────────────────────────────────────────────────

def git(args: list[str], cwd: Path) -> str:
    r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip()


def should_skip(msg: str) -> bool:
    for pat in SKIP_PATTERNS:
        if pat.lower() in msg.lower():
            return True
    return False


def week_label(d: date) -> str:
    """Map date to internship week label (W1 starts Mar 15 2026)."""
    delta = (d - INTERNSHIP_START).days
    if delta < 0:
        return "Pre"
    week_num = delta // 7 + 1
    return f"W{week_num}"


# ── gather commits ────────────────────────────────────────────────────────────

def gather_commits() -> dict[str, list[dict]]:
    """Returns {date_str: [{repo, jira, msg}]} for internship period only."""
    by_date: dict[str, list[dict]] = defaultdict(list)

    for repo in REPOS:
        raw = git(
            ["log", "--all",
             "--format=%ad|%s|%D",
             "--date=short",
             f"--after={INTERNSHIP_START.isoformat()}"],
            cwd=repo["path"],
        )
        seen: set[tuple[str, str]] = set()
        for line in raw.splitlines():
            if not line.strip():
                continue
            parts = line.split("|", 2)
            if len(parts) < 2:
                continue
            day_str, msg = parts[0].strip(), parts[1].strip()
            if should_skip(msg):
                continue
            key = (repo["name"], msg)
            if key in seen:
                continue
            seen.add(key)
            by_date[day_str].append({"repo": repo["name"], "jira": JIRA, "msg": msg})

    return by_date


# ── work-log file helpers ─────────────────────────────────────────────────────

def read_existing_log(path: Path) -> list[str]:
    if path.exists():
        return path.read_text(encoding="utf-8").splitlines()
    return []


def build_log_file(day_str: str, rows: list[dict], existing_lines: list[str]) -> str:
    """
    Build the full content of a work-log file.

    Strategy:
    - If the file is empty/new: write a fresh file with only the IISS-824 rows.
    - If the file exists: keep all non-IISS-824 rows, strip old IISS-824 rows,
      append the new IISS-824 rows at the end of the table, renumber the # column.
    """
    d = date.fromisoformat(day_str)
    dow = d.strftime("%A")
    week = week_label(d)

    # ── Fresh file ──
    if not existing_lines:
        lines = [
            f"# Work Log — {day_str} ({dow})",
            "",
            f"**Week:** {week} | **Total Hours:** 8 hrs",
            "",
            "| # | JIRA | Repository | Branch | Commit |",
            "|---|------|------------|--------|--------|",
        ]
        for i, row in enumerate(rows, 1):
            lines.append(f"| {i} | {row['jira']} | {row['repo']} | --- | {row['msg']} |")
        lines += ["", "**Daily Total: 8 hrs**", ""]
        return "\n".join(lines)

    # ── Existing file — strip old IISS-824 rows, keep everything else ──
    # Find table boundaries
    header_idx = None
    sep_idx = None
    for i, line in enumerate(existing_lines):
        if line.startswith("| #") or line.startswith("|#"):
            header_idx = i
        if header_idx is not None and line.startswith("|---") and sep_idx is None:
            sep_idx = i
            break

    if header_idx is None:
        # No table found — append a new table section
        kept = list(existing_lines)
        while kept and kept[-1].strip() == "":
            kept.pop()
        kept += [
            "",
            "## IISS-824 — ML/LLM Agent",
            "",
            "| # | JIRA | Repository | Branch | Commit |",
            "|---|------|------------|--------|--------|",
        ]
        for i, row in enumerate(rows, 1):
            kept.append(f"| {i} | {row['jira']} | {row['repo']} | --- | {row['msg']} |")
        kept += ["", "**Daily Total: 8 hrs**", ""]
        return "\n".join(kept)

    # Rebuild: keep header + sep, strip IISS-824 data rows, keep others, append new
    pre_table = existing_lines[:header_idx]
    table_header = existing_lines[header_idx]
    table_sep = existing_lines[sep_idx]

    # Collect existing data rows that are NOT IISS-824 entries from these two repos
    repo_names = {r["name"] for r in REPOS}
    data_rows_keep = []
    for line in existing_lines[sep_idx + 1:]:
        if not line.startswith("|"):
            break  # end of table
        # Skip rows that reference either repo
        skip = any(rn in line for rn in repo_names) or JIRA in line
        if not skip:
            data_rows_keep.append(line)

    # Everything after the table
    post_table = []
    in_table = True
    for line in existing_lines[sep_idx + 1:]:
        if in_table and not line.startswith("|"):
            in_table = False
        if not in_table:
            post_table.append(line)

    # Renumber all rows
    all_data = []
    counter = 1
    for row_line in data_rows_keep:
        # Replace leading | N | with | counter |
        import re
        row_line = re.sub(r"^\|\s*\d+\s*\|", f"| {counter} |", row_line)
        all_data.append(row_line)
        counter += 1
    for row in rows:
        all_data.append(f"| {counter} | {row['jira']} | {row['repo']} | --- | {row['msg']} |")
        counter += 1

    result = (
        pre_table
        + [table_header, table_sep]
        + all_data
        + [""]
        + [l for l in post_table if l.strip() or l == ""]
    )
    return "\n".join(result)


# ── write logs ────────────────────────────────────────────────────────────────

def write_logs(by_date: dict[str, list[dict]]) -> list[Path]:
    written = []
    for day_str in sorted(by_date):
        rows = by_date[day_str]
        d = date.fromisoformat(day_str)
        month_dir = LOGS_ROOT / d.strftime("%Y-%m")
        month_dir.mkdir(parents=True, exist_ok=True)
        log_path = month_dir / f"{day_str}.md"

        existing = read_existing_log(log_path)
        content = build_log_file(day_str, rows, existing)
        log_path.write_text(content, encoding="utf-8")
        action = "updated" if existing else "created"
        print(f"  {action}: {log_path.relative_to(REPO_ROOT)} ({len(rows)} IISS-824 rows)")
        written.append(log_path)
    return written


# ── git ops ───────────────────────────────────────────────────────────────────

def git_repo(args: list[str]) -> str:
    return git(args, cwd=REPO_ROOT)


def switch_and_commit(written: list[Path]):
    print("\n── Switching to feature/work-logs ──")
    git_repo(["checkout", "feature/work-logs"])

    print("── Staging work-log files ──")
    for p in written:
        git_repo(["add", str(p.relative_to(REPO_ROOT))])

    # Also stage the script itself
    git_repo(["add", "scripts/generate_iiss824_worklogs.py"])

    status = git_repo(["diff", "--cached", "--name-only"])
    if not status.strip():
        print("  Nothing to commit — work logs already up to date.")
        return

    commit_msg = (
        "feat(work-logs): add IISS-824 ML/LLM agent commits to daily work logs\n\n"
        "Scanned ml-rpa-status-llm-agent and core-smart-rpa-llm-ecr-image\n"
        "for all commits after internship start (2026-03-15).\n"
        "Each day's work log updated with repo name, commit message, JIRA: IISS-824.\n"
        "Skipped: version bumps, merge commits.\n"
    )
    git_repo(["commit", "-m", commit_msg])
    print("  ✓ Committed to feature/work-logs.")


def return_to_feature():
    print("\n── Returning to feature/report-chapters ──")
    git_repo(["checkout", "feature/report-chapters"])
    print("  ✓ Back on feature/report-chapters.")


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Repo root : {REPO_ROOT}")
    print(f"Logs root : {LOGS_ROOT}")
    print(f"Internship start: {INTERNSHIP_START}")
    print()

    print("── Gathering commits ──")
    by_date = gather_commits()
    total = sum(len(v) for v in by_date.values())
    print(f"  Found {total} commit rows across {len(by_date)} days")

    print("\n── Writing work logs ──")
    written = write_logs(by_date)

    switch_and_commit(written)
    return_to_feature()

    print(f"\n✓ Done. {len(written)} work-log files written/updated.")


if __name__ == "__main__":
    main()
