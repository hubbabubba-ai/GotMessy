#!/usr/bin/env python3
"""Regenerate packages/tokens/src/colors.ts and css.ts from the HTML source of truth.

Source of truth: the :root CSS block in Final/*.html deliverables.
Run from the repo root: python3 scripts/generate-tokens.py

The script picks the first HTML file found in Final/ that has a :root block.
If multiple files disagree, check-token-drift.py will flag the drift.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HTML_GLOB = "Final/*.html"
COLORS_OUT = REPO_ROOT / "packages/tokens/src/colors.ts"
CSS_OUT = REPO_ROOT / "packages/tokens/src/css.ts"

ROOT_BLOCK = re.compile(r":root\s*\{([^}]+)\}", re.DOTALL)
DECL = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;]+);")


def css_to_camel(name: str) -> str:
    """Convert --clay-dk to clayDk, --card-bd to cardBd, etc."""
    name = name.lstrip("-")
    parts = name.split("-")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


ROLE_COMMENTS: dict[str, str] = {
    "--cream":    "Primary text on dark backgrounds",
    "--warm":     "Warm neutral / light-mode page background",
    "--ink":      "Default page background (dark)",
    "--ink-soft": "Secondary background",
    "--dust":     "Muted text / labels / metadata",
    "--clay":     "Primary accent — links, buttons, terminal dot",
    "--clay-dk":  "Clay hover / pressed state",
    "--clay-lt":  "Clay focus ring / large hero accents",
    "--sage":     "Success / live status",
    "--lav":      "Secondary accent (categorisation)",
    "--sky":      "Secondary accent (categorisation)",
    "--yellow":   "Highlight — use sparingly",
    "--card":     "Card surface",
    "--card-bd":  "Card border",
}


def main() -> int:
    html_files = sorted(REPO_ROOT.glob(HTML_GLOB))
    if not html_files:
        print("generate-tokens: no HTML deliverables found in Final/", file=sys.stderr)
        return 1

    tokens: dict[str, str] = {}
    source_file: str = ""
    for html in html_files:
        text = html.read_text()
        m = ROOT_BLOCK.search(text)
        if m:
            tokens = {name: value.strip() for name, value in DECL.findall(m.group(1))}
            source_file = html.name
            break

    if not tokens:
        print("generate-tokens: no :root block found in any HTML file", file=sys.stderr)
        return 1

    print(f"generate-tokens: reading from {source_file} ({len(tokens)} tokens)")

    # Write colors.ts
    lines = [
        '/**',
        ' * Got Messy brand color tokens.',
        f' * Source of truth: the :root block in Final/{source_file}',
        ' * Regenerate with: python3 scripts/generate-tokens.py',
        ' * Drift check runs in CI via scripts/check-token-drift.py.',
        ' */',
        '',
        'export const colors = {',
    ]
    for css_name, value in tokens.items():
        camel = css_to_camel(css_name)
        comment = ROLE_COMMENTS.get(css_name, "")
        if comment:
            lines.append(f"  /** {comment} */")
        lines.append(f"  {camel}: '{value}',")
    lines += [
        '} as const;',
        '',
        'export type ColorToken = keyof typeof colors;',
        'export type ColorValue = (typeof colors)[ColorToken];',
        '',
        '/**',
        ' * Accent budget: at most three of clay / sage / lav / sky / yellow per screen.',
        " * Never use pure white (#FFF) or pure black (#000) backgrounds.",
        ' */',
        "export const accentTokens = ['clay', 'sage', 'lav', 'sky', 'yellow'] as const satisfies ColorToken[];",
        'export const ACCENT_BUDGET = 3;',
        '',
    ]
    COLORS_OUT.write_text("\n".join(lines))
    print(f"generate-tokens: wrote {COLORS_OUT.relative_to(REPO_ROOT)}")

    # Write css.ts
    css_decls = "\n".join(f"  {name}: {value};" for name, value in tokens.items())
    css_lines = [
        '/**',
        ' * CSS custom properties string for web contexts.',
        ' * Inject this into a <style> tag or a CSS-in-JS global style.',
        ' * Values are kept in lockstep with colors.ts via check-token-drift.py.',
        ' */',
        'export const cssVars = `:root {',
        css_decls,
        '}`;',
        '',
    ]
    CSS_OUT.write_text("\n".join(css_lines))
    print(f"generate-tokens: wrote {CSS_OUT.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
