#!/usr/bin/env python3
"""
scripts/git_release_and_worklogs.py

Purpose
-------
1. Stage and commit all pending changes on feature/report-chapters.
2. Merge feature/report-chapters into release/v1.0 (--no-ff).
3. Ensure feature/work-logs exists (create off release/v1.0 if not).
4. Merge release/v1.0 into feature/work-logs so it has the latest report changes.
5. Leave the working tree on feature/work-logs ready for work-log edits.

Usage
-----
    uv run python scripts/git_release_and_worklogs.py

Requirements
------------
- Run from the repo root (or any subdirectory; the script resolves the root).
- No unstaged conflicts outside of intentionally staged files.
"""

import subprocess
import sys
from pathlib import Path

# ── helpers ──────────────────────────────────────────────────────────────────

REPO = Path(__file__).resolve().parent.parent  # repo root

def run(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command in REPO; print stdout/stderr; optionally raise on failure."""
    print(f"  $ {' '.join(args)}")
    result = subprocess.run(args, cwd=REPO, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        # git prints informational messages to stderr — show them but don't treat as errors
        print(result.stderr.strip())
    if check and result.returncode not in (0, 1):
        # exit code 1 from git often means "nothing to do" — tolerate it
        sys.exit(f"ERROR: command exited {result.returncode}: {' '.join(args)}")
    return result


def current_branch() -> str:
    return run(["git", "branch", "--show-current"], check=True).stdout.strip()


def branch_exists(name: str) -> bool:
    result = run(["git", "branch", "--list", name], check=False)
    return bool(result.stdout.strip())


# ── step 1: commit pending changes on feature/report-chapters ────────────────

def step1_commit_pending():
    print("\n── Step 1: Commit pending changes on feature/report-chapters ──")

    branch = current_branch()
    if branch != "feature/report-chapters":
        sys.exit(f"ERROR: expected feature/report-chapters, got {branch}. Aborting.")

    # Stage everything that's tracked (modified + renamed) plus the new ch03 file
    files_to_stage = [
        "knowledge-base/",
        "latex-report/",
        "src/report_pipeline/builder.py",
        "src/report_pipeline/logs_generator.py",
        "pyproject.toml",
        "uv.lock",
    ]
    run(["git", "add"] + files_to_stage)

    # Also stage the new untracked team composition chapter and spec dirs
    run(["git", "add",
         "latex-report/chapters/new_ch03_team_composition.tex",
         ".kiro/specs/"], check=False)

    # Check if there's anything staged
    status = run(["git", "diff", "--cached", "--name-only"], check=False)
    if not status.stdout.strip():
        print("  Nothing staged — skipping commit (already up to date).")
        return

    commit_msg = (
        "report: team composition chapter + formatting, table, and content fixes\n\n"
        "- Extract Team Structure & My Role from ch01 into new ch03\n"
        "- ch03-ch14 renumbered to ch04-ch15 (team chapter inserted after exec summary)\n"
        "- Chapter titles restored to SMU brand maroon (smubrand color)\n"
        "- Dashboard row table updated from AMG repo main branch (17 rows, rows 1-15)\n"
        "- 6 budget code environments corrected throughout (was 5)\n"
        "- meridian/citcoworks lowercased to match other budget code identifiers\n"
        "- NFR Achieved column maroon color removed (plain text now)\n"
        "- neeyatimaroon renamed to smubrand throughout\n"
        "- Stakeholder table: names, roles, column widths updated\n"
        "- FR/NFR tables: ID narrow, widths adjusted\n"
        "- JIRA scope table: Status/Repo column removed\n"
        "- Weekly delivery tables (ch10) removed\n"
        "- Section 3.6 (MS Teams/Office) removed\n"
        "- Out-of-scope: Prometheus and Pyroscope added\n"
        "- Section 7.4 replaced with forward ref to ch13\n"
        "- ch13 Challenges: SEARCH() visibility gap added as Challenge 1\n"
        "- pdflatex restored (was xelatex), Inconsolata monospace font\n"
        "- Table inter-row borders removed; header row white text fixed\n"
    )

    run(["git", "commit", "-m", commit_msg])
    print("  ✓ Committed.")


# ── step 2: merge into release/v1.0 ──────────────────────────────────────────

def step2_merge_to_release():
    print("\n── Step 2: Merge feature/report-chapters → release/v1.0 ──")

    run(["git", "checkout", "release/v1.0"])
    run(["git", "merge", "--no-ff", "feature/report-chapters",
         "-m", "Merge feature/report-chapters: team chapter, formatting, content fixes"])
    print("  ✓ Merged into release/v1.0.")


# ── step 3: ensure feature/work-logs exists ───────────────────────────────────

def step3_setup_work_logs_branch():
    print("\n── Step 3: Set up feature/work-logs ──")

    if branch_exists("feature/work-logs"):
        print("  Branch feature/work-logs already exists — checking it out.")
        run(["git", "checkout", "feature/work-logs"])
        print("  Merging latest release/v1.0 into feature/work-logs…")
        run(["git", "merge", "--no-ff", "release/v1.0",
             "-m", "Merge release/v1.0 into feature/work-logs: latest report changes"])
    else:
        print("  Branch feature/work-logs does not exist — creating off release/v1.0.")
        run(["git", "checkout", "-b", "feature/work-logs", "release/v1.0"])

    print("  ✓ Now on feature/work-logs and up to date with release/v1.0.")


# ── step 4: return to feature/report-chapters ────────────────────────────────

def step4_return_to_feature():
    print("\n── Step 4: Return to feature/report-chapters ──")
    run(["git", "checkout", "feature/report-chapters"])
    print("  ✓ Back on feature/report-chapters.")


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Repo: {REPO}")
    print(f"Current branch: {current_branch()}")

    step1_commit_pending()
    step2_merge_to_release()
    step3_setup_work_logs_branch()
    step4_return_to_feature()

    print("\n✓ All done.")
    print("  • release/v1.0 is up to date")
    print("  • feature/work-logs is ready for work-log commits")
    print("  • Working tree is on feature/report-chapters")


if __name__ == "__main__":
    main()
