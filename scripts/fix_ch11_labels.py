"""
fix_ch11_labels.py
------------------
Ensures every \textbf{Label:} that acts as a section heading in chapter 11
has a line break after it so content starts on a new line.

Rules:
- Only process \textbf{} blocks whose content ends with : or :} pattern
  (i.e. they are paragraph-opening labels, not inline bold)
- The \textbf{} must be the FIRST \textbf on its line (heading, not inline)
- If \\ already follows, skip it
- Replace \textbf{Label:} <space> text  →  \textbf{Label:}\\\\ \ntext
"""

import re

FPATH = "latex-report/chapters/new_ch11_weekly_breakdown.tex"

content = open(FPATH, encoding="utf-8").read()
lines = content.split("\n")
new_lines = []
count = 0

for line in lines:
    # Skip lines that already have \\ right after a \textbf closing }
    # Only process lines where \textbf{ appears as the FIRST token (heading lines)
    stripped = line.lstrip()
    if not stripped.startswith(r"\textbf{"):
        new_lines.append(line)
        continue

    # Find the matching closing } of \textbf{ by counting brace depth
    # Start from position of the opening {
    start = line.index(r"\textbf{") + len(r"\textbf{")
    depth = 1
    i = start
    while i < len(line) and depth > 0:
        if line[i] == "{":
            depth += 1
        elif line[i] == "}":
            depth -= 1
        i += 1
    close_idx = i  # position AFTER the closing }

    label_content = line[start : close_idx - 1]  # content inside \textbf{}

    # Only treat as a heading label if content ends with : or ) or similar
    # (not inline bold like \textbf{597 tests} or \textbf{version v728})
    # Heuristic: label ends with : or .:
    if not label_content.rstrip().endswith(":"):
        new_lines.append(line)
        continue

    # What comes after the closing }?
    after = line[close_idx:]  # e.g. "  The week opened on" or "\\" or ""

    # Already has \\ — skip
    if after.lstrip().startswith("\\\\") or after.lstrip().startswith(r"\\"):
        new_lines.append(line)
        continue

    # Strip leading spaces from after
    after_stripped = after.lstrip(" ")

    if after_stripped:
        # There is text after the label on the same line — add \\ and newline
        label_part = line[:close_idx]
        new_lines.append(label_part + r"\\")
        new_lines.append(after_stripped)
        count += 1
    else:
        # Nothing after the label (text is already on next line) — just add \\
        new_lines.append(line.rstrip() + r"\\")
        count += 1

print(f"Labels fixed: {count}")
open(FPATH, "w", encoding="utf-8").write("\n".join(new_lines))
print("Done.")
