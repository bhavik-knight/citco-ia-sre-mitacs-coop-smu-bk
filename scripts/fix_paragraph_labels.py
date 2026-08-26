"""
fix_paragraph_labels.py
-----------------------
Adds a line break after paragraph-opening \textbf{Label:} patterns
in specified chapter files so content starts on a new line.

Only affects labels whose content ends with ':' (paragraph labels).
Skips inline bold (e.g. \textbf{Ask Citco RPA}, \textbf{Critical}).
"""

import os

BACKSLASH_PAIR = "\\\\"  # the string \\

files = [
    "latex-report/chapters/new_ch06_project_goals.tex",
    "latex-report/chapters/new_ch14_challenges.tex",
]

total = 0
for fpath in files:
    content = open(fpath, encoding="utf-8").read()
    lines = content.split("\n")
    new_lines = []
    count = 0

    for line in lines:
        stripped = line.lstrip()

        if not stripped.startswith(r"\textbf{"):
            new_lines.append(line)
            continue

        # Find closing } of \textbf{ by brace counting
        depth = 0
        close_idx = -1
        for i, ch in enumerate(stripped):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    close_idx = i
                    break

        if close_idx < 0:
            new_lines.append(line)
            continue

        label = stripped[8:close_idx]  # content between \textbf{ and }

        # Only fix paragraph labels (end with :)
        if not label.rstrip().endswith(":"):
            new_lines.append(line)
            continue

        after = stripped[close_idx + 1:].lstrip(" ")

        # Already has \\ — skip
        if after.startswith(BACKSLASH_PAIR) or after == "":
            new_lines.append(line)
            continue

        # Add \\ after closing } and content on next line
        indent = line[: len(line) - len(stripped)]
        new_lines.append(indent + stripped[: close_idx + 1] + BACKSLASH_PAIR)
        new_lines.append(indent + after)
        count += 1
        continue

    total += count
    open(fpath, "w", encoding="utf-8").write("\n".join(new_lines))
    print(f"  {fpath}: {count} labels fixed")

print(f"\nTotal labels fixed: {total}")
