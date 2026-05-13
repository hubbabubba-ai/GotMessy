#!/usr/bin/env bash
# Brand-rule lint for Got Messy assets.
# Source of truth for all rules: CLAUDE.md (Brand tokens / Voice sections).
#
# Rules:
#   1. Forbidden words: never appear in shipped copy.
#   2. Forbidden colors: pure white (#FFF/#FFFFFF) and pure black (#000/#000000).
#   3. Exclamation budget: at most one `!` per HTML page (excluding code-like
#      contexts: !important, !=, !DOCTYPE).
#
# Per-line override: append `<!-- brand-lint-allow -->` to the line, or
# `<!-- brand-lint-allow: word -->` to allow a specific word. Markdown also
# supports the same comment.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$REPO_ROOT"

violations=0

forbidden_words=(
  "journey" "unlock" "unleash" "supercharge" "empower"
  "AI-powered" "cutting-edge" "leverage" "learning curve"
)

scan_paths=()
[[ -d packages/brand/Final ]] && while IFS= read -r f; do scan_paths+=("$f"); done < <(find packages/brand/Final -type f \( -name "*.html" -o -name "*.md" \))
[[ -d packages/brand/docs ]]  && while IFS= read -r f; do scan_paths+=("$f"); done < <(find packages/brand/docs  -type f -name "*.md")

if [[ ${#scan_paths[@]} -eq 0 ]]; then
  echo "brand-lint: no files to scan"
  exit 0
fi

# Rule 1: forbidden words (case-insensitive, word-boundary).
for word in "${forbidden_words[@]}"; do
  while IFS= read -r hit; do
    [[ -z "$hit" ]] && continue
    file="${hit%%:*}"
    rest="${hit#*:}"
    line="${rest%%:*}"
    content="${rest#*:}"
    # Skip if line carries an allow comment for this word or any word.
    if echo "$content" | grep -qiE "brand-lint-allow(:\s*${word}\b)?" ; then
      continue
    fi
    echo "$file:$line: forbidden word '$word'"
    violations=$((violations + 1))
  done < <(grep -rniIE "\\b${word}\\b" "${scan_paths[@]}" 2>/dev/null || true)
done

# Rule 2: forbidden colors. Only check HTML/CSS contexts.
html_files=()
for f in "${scan_paths[@]}"; do [[ "$f" == *.html ]] && html_files+=("$f"); done
if [[ ${#html_files[@]} -gt 0 ]]; then
  while IFS= read -r hit; do
    [[ -z "$hit" ]] && continue
    file="${hit%%:*}"
    rest="${hit#*:}"
    line="${rest%%:*}"
    content="${rest#*:}"
    if echo "$content" | grep -qE "brand-lint-allow" ; then
      continue
    fi
    echo "$file:$line: forbidden color (pure white/black) — use --cream or --ink"
    violations=$((violations + 1))
  done < <(grep -rniIE "#(fff(fff)?|000(000)?)\\b" "${html_files[@]}" 2>/dev/null || true)
fi

# Rule 3: exclamation budget per HTML page.
# Excludes code-like contexts (!important, !=, !DOCTYPE, comment markers)
# and any line marked with `brand-lint-allow` (e.g. "this is what NOT to do" examples).
for f in "${html_files[@]}"; do
  count=$(grep -v "brand-lint-allow" "$f" \
          | sed -E 's/!important//g; s/!DOCTYPE//gI; s/!=//g; s/!--/__/g; s/--!/__/g' \
          | tr -cd '!' | wc -c | tr -d ' ')
  if (( count > 1 )); then
    echo "$f:1: $count exclamation marks (max 1 per page; excludes !important, !=, !DOCTYPE, comments, and brand-lint-allow lines)"
    violations=$((violations + 1))
  fi
done

if (( violations > 0 )); then
  echo ""
  echo "brand-lint: $violations violation(s)"
  exit 1
fi

echo "brand-lint: clean"
