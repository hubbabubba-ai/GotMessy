#!/usr/bin/env python3
"""Check that brand tokens in CLAUDE.md match the :root block in each HTML deliverable.

Source of truth per CLAUDE.md: the :root CSS block in any HTML deliverable.
This script enforces that the Markdown table in CLAUDE.md stays in lockstep.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
HTML_GLOB = "Final/*.html"

TABLE_ROW = re.compile(r"^\|\s*`(--[a-z0-9-]+)`\s*\|\s*`([^`]+)`\s*\|")
ROOT_BLOCK = re.compile(r":root\s*\{([^}]+)\}", re.DOTALL)
DECL = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;]+);")


def parse_claude_md(path: Path) -> dict[str, str]:
    tokens: dict[str, str] = {}
    for line in path.read_text().splitlines():
        m = TABLE_ROW.match(line)
        if m:
            tokens[m.group(1)] = m.group(2).strip().lower()
    return tokens


def parse_html_root(path: Path) -> dict[str, str]:
    text = path.read_text()
    m = ROOT_BLOCK.search(text)
    if not m:
        return {}
    return {
        name: value.strip().lower()
        for name, value in DECL.findall(m.group(1))
    }


def main() -> int:
    if not CLAUDE_MD.exists():
        print(f"check-token-drift: {CLAUDE_MD} not found", file=sys.stderr)
        return 2

    md_tokens = parse_claude_md(CLAUDE_MD)
    if not md_tokens:
        print("check-token-drift: no brand-token table found in CLAUDE.md", file=sys.stderr)
        return 2

    html_files = sorted(REPO_ROOT.glob(HTML_GLOB))
    if not html_files:
        print("check-token-drift: no HTML deliverables to compare against; skipping")
        return 0

    drift = 0
    for html in html_files:
        css_tokens = parse_html_root(html)
        if not css_tokens:
            print(f"{html.relative_to(REPO_ROOT)}:1: no :root block found")
            drift += 1
            continue

        rel = html.relative_to(REPO_ROOT)
        # Only enforce that tokens listed in CLAUDE.md match the HTML.
        # Extra tokens in HTML (e.g. typography like --mono) are allowed —
        # the CLAUDE.md table documents the colour palette, not every token.
        for name, md_value in md_tokens.items():
            css_value = css_tokens.get(name)
            if css_value is None:
                print(f"{rel}: token {name} listed in CLAUDE.md but absent from this file's :root")
                drift += 1
            elif css_value != md_value:
                print(f"{rel}: token {name} drift — HTML={css_value} CLAUDE.md={md_value}")
                drift += 1

    if drift:
        print(f"\ncheck-token-drift: {drift} drift(s)", file=sys.stderr)
        return 1

    print("check-token-drift: tokens in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
