#!/usr/bin/env python3
"""
Fix lstlisting centering: replace \begin{center}\begin{lstlisting}
with a version that uses \hspace to truly center the fixed-width listing.
Strategy: add xleftmargin=\dimexpr(\linewidth-CONTENT_WIDTH)/2\relax
to each lstlisting so LaTeX auto-centres the block.
"""
import re
from pathlib import Path

path = Path("latex-report/chapters/new_ch10_implementation.tex")
content = path.read_text(encoding="utf-8")

# The listings are already wrapped in \begin{center}...\end{center}
# Add xleftmargin=\dimexpr(\linewidth - X pt)/2\relax to each lstlisting
# inside a center block so the box is genuinely centred.
# We measure the max line length inside each listing to set the right width.

def add_centering(m):
    """Add xleftmargin to a lstlisting options string."""
    full = m.group(0)
    # Find the lstlisting options
    full = re.sub(
        r'(\\begin\{lstlisting\}\[)([^\]]+)(\])',
        lambda o: o.group(1) + o.group(2) +
                  r', xleftmargin=\dimexpr(\linewidth-0.75\linewidth)/2\relax' +
                  o.group(3),
        full,
        count=1
    )
    return full

# Apply to each center+lstlisting block
pattern = re.compile(
    r'\\begin\{center\}\s*\n(\\begin\{lstlisting\}.*?\\end\{lstlisting\})\s*\n\\end\{center\}',
    re.DOTALL
)

def rewrap(m):
    inner = m.group(1)
    # Find the widest line inside the listing to set an appropriate minipage width
    lines = inner.split('\n')
    max_len = max((len(l) for l in lines if not l.startswith('\\')), default=65)
    # Use a minipage at the right size, then center it
    return (
        '\\begin{center}\n'
        '\\begin{minipage}{0.92\\textwidth}\n'
        + inner + '\n'
        '\\end{minipage}\n'
        '\\end{center}'
    )

new_content, n = pattern.subn(rewrap, content)
path.write_text(new_content, encoding="utf-8")
print(f"Done — updated {n} lstlisting block(s).")
