#!/usr/bin/env python3
"""
scripts/generate_iiss824_worklogs.py

Purpose
-------
Scans ml-rpa-status-llm-agent and core-smart-rpa-llm-ecr-image for commits
authored by Bhavik Bhagat (bbhagat@citco.com) after 2026-03-15 (internship
start) and writes/updates daily work-log .md files under
smu/work-logs/<year-month>/<date>.md.

Rules
-----
- Author filter  : only bbhagat@citco.com (both name variants)
- Skip patterns  : version bumps, merge-to-release commits
- Deduplicates   : by (repo, message) per day
- JIRA           : IISS-824 on every row
- Existing files : old IISS-824 rows replaced; all other rows kept, renumbered
- Git flow       : checkout feature/work-logs → commit → return to original branch

Usage
-----
    uv run python scripts/generate_iiss824_worklogs.py
"""

import re
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

# ── config ────────────────────────────────────────────────────────────────────

REPO_ROOT        = Path(__file__).resolve().parent.parent
LOGS_ROOT        = REPO_ROOT / "smu" / "work-logs"
INTERNSHIP_START = date(2026, 3, 15)
WORK_LOG_BRANCH  = "feature/work-logs"

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

JIRA       = "IISS-824"
MY_EMAIL   = "bbhagat@citco.com"   # both author-name variants share this email

SKIP_PATTERNS = [
    "chore: bump version",
    "Merge branch 'release",
    "Merge branch 'main",
    "Merge pull request",
]

REPO_NAMES = {r["name"] for r in REPOS}


# ── helpers ───────────────────────────────────────────────────────────────────

def git(args: list[str], cwd: Path) -> str:
    r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip()


def git_repo(args: list[str]) -> str:
    return git(args, cwd=REPO_ROOT)


def should_skip(msg: str) -> bool:
    return any(pat.lower() in msg.lower() for pat in SKIP_PATTERNS)


def week_label(d: date) -> str:
    delta = (d - INTERNSHIP_START).days
    return f"W{max(delta // 7 + 1, 1)}" if delta >= 0 else "Pre"


# ── gather commits (author-filtered) ─────────────────────────────────────────

def gather_commits() -> dict[str, list[dict]]:
    """Returns {date_str: [{repo, jira, msg}]} — only MY commits."""
    by_date: dict[str, list[dict]] = defaultdict(list)

    for repo in REPOS:
        # %ae = author email; filter server-side with --author
        raw = git(
            ["log", "--all",
             f"--author={MY_EMAIL}",
             "--format=%ad|%ae|%s",
             "--date=short",
             f"--after={INTERNSHIP_START.isoformat()}"],
            cwd=repo["path"],
        )
        seen: set[tuple[str, str]] = set()
        for line in raw.splitlines():
            if not line.strip():
                continue
            parts = line.split("|", 2)
            if len(parts) < 3:
                continue
            day_str, _email, msg = parts[0].strip(), parts[1].strip(), parts[2].strip()
            if should_skip(msg):
                continue
            key = (repo["name"], msg)
            if key in seen:
                continue
            seen.add(key)
            by_date[day_str].append({"repo": repo["name"], "jira": JIRA, "msg": msg})

    return by_date


# ── work-log file helpers ─────────────────────────────────────────────────────

def build_log_file(day_str: str, rows: list[dict], existing_lines: list[str]) -> str:
    d = date.fromisoformat(day_str)
    dow = d.strftime("%A")
    week = week_label(d)

    # ── Fresh file ──────────────────────────────────────────────────────────
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

    # ── Existing file: strip old IISS-824/LLM-repo rows, keep everything else
    # Find table header + separator
    header_idx = sep_idx = None
    for i, line in enumerate(existing_lines):
        if re.match(r"^\|\s*#", line) and header_idx is None:
            header_idx = i
        if header_idx is not None and re.match(r"^\|[-|]+\|", line) and sep_idx is None:
            sep_idx = i
            break

    if header_idx is None:
        # No table — append a fresh section
        kept = list(existing_lines)
        while kept and kept[-1].strip() == "":
            kept.pop()
        kept += ["", "| # | JIRA | Repository | Branch | Commit |",
                 "|---|------|------------|--------|--------|"]
        for i, row in enumerate(rows, 1):
            kept.append(f"| {i} | {row['jira']} | {row['repo']} | --- | {row['msg']} |")
        kept += ["", "**Daily Total: 8 hrs**", ""]
        return "\n".join(kept)

    pre_table   = existing_lines[:header_idx]
    tbl_header  = existing_lines[header_idx]
    tbl_sep     = existing_lines[sep_idx]

    # Data rows to KEEP (not from these two repos, not IISS-824 for these repos)
    keep_rows = []
    after_table = []
    in_table = True
    for line in existing_lines[sep_idx + 1:]:
        if in_table:
            if not line.startswith("|"):
                in_table = False
                after_table.append(line)
                continue
            drop = any(rn in line for rn in REPO_NAMES) and JIRA in line
            if not drop:
                keep_rows.append(line)
        else:
            after_table.append(line)

    # Renumber and append new rows
    all_rows = []
    counter = 1
    for row_line in keep_rows:
        row_line = re.sub(r"^\|\s*\d+\s*\|", f"| {counter} |", row_line)
        all_rows.append(row_line)
        counter += 1
    for row in rows:
        all_rows.append(f"| {counter} | {row['jira']} | {row['repo']} | --- | {row['msg']} |")
        counter += 1

    result_lines = (
        pre_table
        + [tbl_header, tbl_sep]
        + all_rows
        + [""]
        + after_table
    )
    # Ensure single trailing newline
    while result_lines and result_lines[-1].strip() == "":
        result_lines.pop()
    result_lines.append("")
    return "\n".join(result_lines)


# ── write logs ────────────────────────────────────────────────────────────────

def write_logs(by_date: dict[str, list[dict]]) -> list[Path]:
    written = []
    for day_str in sorted(by_date):
        rows = by_date[day_str]
        d = date.fromisoformat(day_str)
        month_dir = LOGS_ROOT / d.strftime("%Y-%m")
        month_dir.mkdir(parents=True, exist_ok=True)
        log_path  = month_dir / f"{day_str}.md"

        existing = log_path.read_text(encoding="utf-8").splitlines() if log_path.exists() else []
        content  = build_log_file(day_str, rows, existing)
        log_path.write_text(content, encoding="utf-8")
        action = "updated" if existing else "created"
        print(f"  {action}: smu/work-logs/{d.strftime('%Y-%m')}/{day_str}.md  ({len(rows)} rows)")
        written.append(log_path)
    return written


# ── git ops ───────────────────────────────────────────────────────────────────

def switch_and_commit(written: list[Path], original_branch: str):
    print(f"\n── Switching to {WORK_LOG_BRANCH} ──")
    print(git_repo(["checkout", WORK_LOG_BRANCH]))

    for p in written:
        git_repo(["add", str(p.relative_to(REPO_ROOT))])
    git_repo(["add", "scripts/generate_iiss824_worklogs.py"])

    staged = git_repo(["diff", "--cached", "--name-only"])
    if not staged.strip():
        print("  Nothing to commit — already up to date.")
    else:
        msg = (
            "feat(work-logs): IISS-824 ML/LLM agent commits (author-filtered)\n\n"
            "- Scanned ml-rpa-status-llm-agent and core-smart-rpa-llm-ecr-image\n"
            "- Only commits by bbhagat@citco.com included\n"
            "- Internship period: 2026-03-15 onwards\n"
            f"- {len(written)} daily work-log files updated\n"
        )
        print(git_repo(["commit", "-m", msg]))
        print("  ✓ Committed.")

    print(f"\n── Returning to {original_branch} ──")
    print(git_repo(["checkout", original_branch]))
    print("  ✓ Done.")


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    original_branch = git_repo(["branch", "--show-current"])
    print(f"Repo       : {REPO_ROOT}")
    print(f"On branch  : {original_branch}")
    print(f"Author     : {MY_EMAIL}")
    print(f"Start date : {INTERNSHIP_START}")
    print()

    print("── Gathering your commits ──")
    by_date = gather_commits()
    total   = sum(len(v) for v in by_date.values())
    print(f"  {total} commit rows across {len(by_date)} days (author-filtered)")

    if not by_date:
        print("  Nothing to write.")
        return

    print("\n── Writing work logs ──")
    written = write_logs(by_date)

    switch_and_commit(written, original_branch)
    print(f"\n✓ {len(written)} files written/updated on {WORK_LOG_BRANCH}.")


if __name__ == "__main__":
    main()
