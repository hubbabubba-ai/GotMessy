# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`GotMessy` is **not a code project** — there is no source tree, build system, or test suite. The repository currently contains:

- `README.md` — a single-line placeholder (`# GotMessy`).
- `Final.zip` — a bundle of brand assets and standalone HTML/PDF deliverables for the **Got Messy** brand (an AI tool for "real people with real chaos" — messy notes, half-finished ideas, drafts that need to sound professional).
- `.github/workflows/blank.yml` — a **placeholder** GitHub Actions workflow that only runs `echo Hello, world!` on push/PR to `main`. It is not a real build or test; do not treat a green check here as validation of anything. Replace it (don't extend it) when actual CI is needed.
- `.claude/settings.json` — enables the `superpowers@claude-plugins-official` plugin for this repo.

Treat this repo as a brand/design package until code is added. Do not invent build, lint, or test commands; none exist.

## Inspecting the assets

Everything lives inside `Final.zip`. To work with it:

```bash
unzip -l Final.zip                       # list contents (44 files under Final/)
unzip -o Final.zip -d /tmp/gotmessy      # extract for inspection / editing
```

After editing, repackage with `zip -r Final.zip Final/` from the directory containing the `Final/` folder. Do not commit the extracted directory alongside the zip — pick one source of truth and stick with it.

## Bundle contents (`Final/`)

Three categories, all flat in one directory:

1. **Logos & icons** — `gotmessy-logo-{A,B,C}` (SVG + PNG + `@2x` PNG, plus transparent variants for A), `gotmessy-icon.svg`, `gotmessy-app-icon.png` (+ `@2x`). Logo `A` is the lead.
2. **Reference sheets** — `gotmessy-color-sheet.png`, `gotmessy-type-sheet.png`.
3. **Standalone HTML/PDF deliverables** (each has both an `.html` and a `.pdf`):
   - `gotmessy-hub` — *Got Messy · Project Hub v2.0*. Daily dashboard / index of all assets.
   - `gotmessy-brand-kit` — *Brand Identity Kit*. Canonical reference for name rationale, logos, colors, type, voice, domains, tooling.
   - `prompt-architect-infographic` — *App Architecture* infographic.

### `-final` naming convention

Most assets exist twice: a base name and a `-final` (or `-final.<ext>`) variant — e.g. `gotmessy-logo-A.png` and `gotmessy-logo-A-final.png`. The `-final` files are the **canonical, shippable** versions; the un-suffixed files are working copies. The HTML deliverables are byte-identical between the two variants today, but treat `-final` as the source of truth when they diverge. When adding new assets, mirror this pairing.

## Brand tokens (use these verbatim if generating UI/HTML)

Pulled from the inline CSS `:root` block in the HTML deliverables — keep these in sync if you edit any of the HTML files.

**Colors**

| Token | Hex | Role |
|---|---|---|
| `--cream` | `#FAF7F2` | primary text on dark |
| `--warm` | `#F2EDE4` | warm neutral |
| `--ink` | `#1A1612` | page background (dark) |
| `--ink-soft` | `#3D3530` | secondary background |
| `--dust` | `#C4B5A0` | muted text / labels |
| `--clay` / `--clay-dk` / `--clay-lt` | `#C4673A` / `#9B4A28` / `#E8896A` | accent (the dot, links, primary buttons) |
| `--sage` | `#5C7A62` | success / live status |
| `--lav` | `#8B7BAB` | secondary accent |
| `--sky` | `#5B8FA8` | secondary accent |
| `--yellow` | `#E8C84A` | highlight |
| `--card` / `--card-bd` | `#1E1A16` / `rgba(255,255,255,0.08)` | card surface + border |

**Typography** — Google Fonts: `Lora` (serif, used italic for "Got" and bold for headings/wordmarks) and `Poppins` (sans, body & UI). Wordmark pattern: `Got` in *italic Lora 400*, `Messy` in **bold Lora 700**, terminal `.` in `--clay`.

**Voice** — "brilliant friend who happens to be great with words. Not a tutor. Not a robot. Not a hustle-culture coach." Avoid tech jargon and learning-curve language.

**Domains** — `gotmessy.com` is the lead brand. `cloudcomb.com` is held for an enterprise/team edition (deliberately opposite tone — orderly, systematic).

**Avoid** — pure white backgrounds, electric blues/teals, high-saturation neons.

## Workflow conventions

- **Branch**: develop on whatever `claude/...` branch the task explicitly assigns (e.g. past sessions used `claude/add-claude-documentation-gXwtx`, `claude/install-superpowers-plugin-t4hXQ`). Never push to `main` or to a different session's branch without explicit permission.
- **Commits**: the early history has terse messages (`Initial commit`, `Add files via upload`); more recent merged work uses descriptive ones (`Add CLAUDE.md with brand-asset repo overview`, `Add basic CI workflow configuration`, `Enable superpowers plugin from claude-plugins-official`). Match the descriptive style — explain the *why*, not just the *what*.
- **PRs**: changes land on `main` via PRs from `claude/...` branches (see merged PRs #1, #2). Open new work as a draft PR after the first push.
- **GitHub scope**: MCP tools are restricted to `hubbabubba-ai/gotmessy`.

## When code does land here

There is no precedent for build/test tooling yet. If you add code, also extend this file with the actual commands (build, lint, test, run-single-test) and a short architecture overview — don't leave future instances guessing.
