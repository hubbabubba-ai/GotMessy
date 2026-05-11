#!/usr/bin/env python3
"""Check that brand tokens in CLAUDE.md, HTML deliverables, and the TS package stay in sync.

Source of truth per CLAUDE.md: the :root CSS block in any HTML deliverable.
Three checks run in sequence:
  1. CLAUDE.md colour table  vs. each HTML :root block
  2. packages/tokens/src/colors.ts  vs. the first HTML :root block
  3. packages/tokens/src/css.ts     vs. the first HTML :root block
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
HTML_GLOB = "Final/*.html"
COLORS_TS = REPO_ROOT / "packages/tokens/src/colors.ts"
CSS_TS = REPO_ROOT / "packages/tokens/src/css.ts"

TABLE_ROW = re.compile(r"^\|\s*`(--[a-z0-9-]+)`\s*\|\s*`([^`]+)`\s*\|")
ROOT_BLOCK = re.compile(r":root\s*\{([^}]+)\}", re.DOTALL)
DECL = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;]+);")
TS_ENTRY = re.compile(r"^\s+(\w+):\s+'([^']+)'", re.MULTILINE)


def camel_to_css(name: str) -> str:
    """Convert camelCase token names back to CSS variable names: inkSoft -> --ink-soft."""
    result = re.sub(r"([A-Z])", lambda m: "-" + m.group(1).lower(), name)
    return "--" + result


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
    return {name: value.strip().lower() for name, value in DECL.findall(m.group(1))}


def parse_colors_ts(path: Path) -> dict[str, str]:
    """Parse the colors object from packages/tokens/src/colors.ts."""
    text = path.read_text()
    tokens: dict[str, str] = {}
    for camel, value in TS_ENTRY.findall(text):
        css_name = camel_to_css(camel)
        tokens[css_name] = value.strip().lower()
    return tokens


def parse_css_ts(path: Path) -> dict[str, str]:
    """Parse the :root block out of the cssVars template literal in css.ts."""
    text = path.read_text()
    m = ROOT_BLOCK.search(text)
    if not m:
        return {}
    return {name: value.strip().lower() for name, value in DECL.findall(m.group(1))}


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

    # ── Check 1: CLAUDE.md vs. each HTML :root ────────────────────────────────
    canonical_tokens: dict[str, str] = {}
    for html in html_files:
        css_tokens = parse_html_root(html)
        if not css_tokens:
            print(f"{html.relative_to(REPO_ROOT)}:1: no :root block found")
            drift += 1
            continue

        rel = html.relative_to(REPO_ROOT)
        if not canonical_tokens:
            canonical_tokens = css_tokens  # first file becomes the reference for TS checks

        for name, md_value in md_tokens.items():
            css_value = css_tokens.get(name)
            if css_value is None:
                print(f"{rel}: token {name} listed in CLAUDE.md but absent from :root")
                drift += 1
            elif css_value != md_value:
                print(f"{rel}: token {name} drift — HTML={css_value} CLAUDE.md={md_value}")
                drift += 1

    # ── Check 2: packages/tokens/src/colors.ts vs. HTML ──────────────────────
    if COLORS_TS.exists() and canonical_tokens:
        ts_colors = parse_colors_ts(COLORS_TS)
        rel = COLORS_TS.relative_to(REPO_ROOT)
        for name, html_value in md_tokens.items():
            ts_value = ts_colors.get(name)
            if ts_value is None:
                print(f"{rel}: token {name} missing from colors object")
                drift += 1
            elif ts_value != html_value:
                print(f"{rel}: token {name} drift — TS={ts_value} HTML={html_value}")
                drift += 1

    # ── Check 3: packages/tokens/src/css.ts vs. HTML ─────────────────────────
    if CSS_TS.exists() and canonical_tokens:
        css_ts_tokens = parse_css_ts(CSS_TS)
        rel = CSS_TS.relative_to(REPO_ROOT)
        for name, html_value in md_tokens.items():
            css_ts_value = css_ts_tokens.get(name)
            if css_ts_value is None:
                print(f"{rel}: token {name} missing from cssVars block")
                drift += 1
            elif css_ts_value != html_value:
                print(f"{rel}: token {name} drift — css.ts={css_ts_value} HTML={html_value}")
                drift += 1

    if drift:
        print(f"\ncheck-token-drift: {drift} drift(s)", file=sys.stderr)
        return 1

    print("check-token-drift: tokens in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
