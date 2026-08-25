#!/usr/bin/env python3
"""Remove red border from ASCII diagram figures in ch10."""
import re
from pathlib import Path

path = Path("latex-report/chapters/new_ch10_implementation.tex")
content = path.read_text(encoding="utf-8")

# Replace frame=single + rulecolor with frame=none for lstlisting blocks
# Pattern: frame=single,\n  rulecolor=\color{smubrand}, backgroundcolor=\color{white}
content = re.sub(
    r'frame=single,\s*\n\s*rulecolor=\\color\{smubrand\},\s*backgroundcolor=\\color\{white\}',
    lambda m: 'frame=none, backgroundcolor=\\color{white}',
    content
)

# Also handle inline version without newline
content = content.replace(
    'frame=single, rulecolor=\\color{smubrand}, backgroundcolor=\\color{white}',
    'frame=none, backgroundcolor=\\color{white}'
)

path.write_text(content, encoding="utf-8")
print("Done.")
# Verify
matches = re.findall(r'frame=\w+', content)
print("Remaining frame settings:", set(matches))
