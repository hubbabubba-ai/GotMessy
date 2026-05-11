# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a repo in the **hubbabubba-ai** GitHub organisation for the **Got Messy** brand — an AI-powered prompt-engineering app for non-technical creators ("real people with real chaos"). The repository currently holds brand/design assets and product planning documentation. No shipping application code has landed yet.

**Current contents:**

| Path | Description |
|---|---|
| `README.md` | Single-line placeholder (`# GotMessy`) |
| `Final.zip` | Brand-asset bundle (~1.9 MB, 44 files) |
| `Final/` | Extracted bundle — tracked on `claude/brand-guidelines-system-design`, not yet on the default branch |
| `docs/brand-guidelines.md` | Operational brand rules (on `claude/brand-guidelines-system-design`) |
| `docs/system-design.md` | Full system architecture document (on `claude/brand-guidelines-system-design`) |
| `.github/workflows/quality.yml` | **Quality CI** — HTML validation, link check, accessibility (pa11y, WCAG 2.1 AA), Markdown lint, brand-rule lint, brand-token drift, asset-pair check. See "Quality checks" below. |
| `.github/workflows/static.yml` | **Real deployment** — publishes `_site/` (only `index.html`, `Final/`, `docs/`) to GitHub Pages on every push to the default branch |
| `index.html` | Landing page deployed at the Pages root; links to the brand guidelines and system design deliverables |
| `scripts/brand-lint.sh` | Forbidden-words / forbidden-colors / exclamation-budget checker (rules sourced from this file) |
| `scripts/check-token-drift.py` | Asserts brand-token table here matches the `:root` block in each HTML deliverable **and** the TS package |
| `scripts/generate-tokens.py` | Regenerates `packages/tokens/src/colors.ts` and `css.ts` from the HTML source of truth |
| `packages/tokens/` | Shared design-token package (`@gotmessy/tokens`) — see "Tokens package" below |
| `.claude/settings.json` | Enables the `superpowers@claude-plugins-official` plugin |

Treat this repo as a brand/design package until application code is added. The build/lint/test surface today is asset-quality only — see "Quality checks" below.

## Quality checks

`quality.yml` runs on every push and PR to `main`. To reproduce locally from the repo root:

```bash
npx html-validate "Final/**/*.html" "index.html"
npx markdownlint-cli2 "docs/**/*.md" "CLAUDE.md"
bash scripts/brand-lint.sh
python3 scripts/check-token-drift.py
# Link check (requires lychee):
npx lychee --no-progress --exclude-mail --accept 200,206,403,429 'Final/**/*.html' 'docs/**/*.md' 'index.html' 'CLAUDE.md'
# Accessibility audit (serves repo on :8080 then audits):
npx http-server -p 8080 -s & sleep 1 && npx pa11y-ci --config .pa11yci ; kill %1
```

Brand-rule details:

- **Forbidden words** (case-insensitive, word-boundary): `journey`, `unlock`, `unleash`, `supercharge`, `empower`, `AI-powered`, `cutting-edge`, `leverage`, `learning curve`. Per-line override: append `<!-- brand-lint-allow -->` to the line (e.g. cautionary "Never" examples in `docs/brand-guidelines.md`).
- **Forbidden colors**: pure white (`#FFF`/`#FFFFFF`) and pure black (`#000`/`#000000`) in HTML/CSS contexts. Use `--cream` / `--ink` instead.
- **Exclamation budget**: at most one `!` per HTML page (excluding `!important`, `!=`, `!DOCTYPE`, comments, and `brand-lint-allow` lines).
- **Token drift**: every token in the colour table below must match (1) the `:root { ... }` block in each `Final/*.html`, (2) the `colors` object in `packages/tokens/src/colors.ts`, and (3) the `:root` block in `packages/tokens/src/css.ts`. The HTML is the source of truth — when they diverge, run `python3 scripts/generate-tokens.py` to regenerate the TS package, then update CLAUDE.md.
- **Asset-pair check**: every working asset (`logo-A.png`, etc.) must have a `-final` sibling. Skipped silently if `Final/` contains only HTML.

## Related repositories

The `hubbabubba-ai` org contains several repos within Claude's MCP scope:

| Repo | Notes |
|---|---|
| `gotmessy` | Canonical repo; has the full brand commit history |
| `messy` | Mirror of the same brand assets |
| `zoe` | Mirror of the same brand assets |
| `your-promptness` | Empty — no content yet |

When MCP scope permits access to multiple repos, apply consistent CLAUDE.md updates across all of them.

## Product overview

Read `docs/system-design.md` (on `claude/brand-guidelines-system-design`) for the full engineering spec. Summary:

**Got Messy** is a **mobile-first prompt-engineering app** for non-technical creators. It accepts messy raw input (text, PDFs, URLs) and produces validated, reusable prompt templates the user can run on the LLM of their choice.

### Product surfaces (Hub & Spoke)

| ID | Surface | Role |
|---|---|---|
| 1.0 | Home Dashboard *(Hub)* | Index, recent activity, quick start |
| 2.0 | The Architect *(MVP core)* | Four-phase prompt builder |
| 3.0 | The Vault | My Good Stuff, Community Recipes, Favourites |
| 4.0 | Settings | Model toggle, User DNA, billing / BYOK |

**The Architect's four phases**: The Drop (paste raw input) → Intent Classifier (NLP: detect persona/task/format signals) → Triple-Pillar editor (Persona / Task / Format fields) → Test Flight (run assembled prompt against chosen LLM).

### Planned tech stack

| Layer | Tech |
|---|---|
| Client | React Native (Expo) + React Native Web; Next.js for `gotmessy.com` marketing |
| API Gateway / BFF | Hono on Cloudflare Workers (or Next.js API routes) |
| Database | Postgres (Neon or Supabase) + pgvector for embeddings |
| Identity | Clerk or Auth0 (external IdP) |
| LLM providers | Gemini, OpenAI, Anthropic — user-selectable + BYOK |
| Object storage | S3 / Cloudflare R2 |
| Observability | OpenTelemetry + Sentry |

**LLM Gateway**: a single internal service all callers use to reach providers — one place for PII redaction before egress, token counting, per-user quotas, response caching (deterministic prompts), and provider failover.

### Build phases

| Phase | Scope |
|---|---|
| 0 — Foundations | Repo scaffolding, IdP integration, shared design tokens package, CI on PRs |
| 1 — Architect MVP | Smart Paste (text only), Triple-Pillar editor, single-provider Test Flight, basic Vault save |
| 2 — Multi-LLM | LLM Gateway (all 3 providers), model toggle in Settings, BYOK |
| 3 — Smart Paste full | PDF + URL inputs, PII Sanity Check (Strict/Standard), production Intent Classifier |
| 4 — Vault expansion | Community Recipes, tags, semantic search via pgvector embeddings |
| 5 — User DNA | Onboarding capture, persistence, auto-injection at Test Flight time |
| 6 — Risk scoring | Hallucination Risk Score, citation extraction |

See `docs/system-design.md §9` for phase exit criteria. Each phase ships behind a feature flag.

## Inspecting the brand assets

Everything lives inside `Final.zip`:

```bash
unzip -l Final.zip                       # list contents (44 files under Final/)
unzip -o Final.zip -d /tmp/gotmessy      # extract for inspection / editing
```

After editing, repackage with `zip -r Final.zip Final/` from the directory containing the `Final/` folder. Do not commit the extracted directory alongside the zip — pick one source of truth. The `claude/brand-guidelines-system-design` branch tracks `Final/` directly; if that pattern merges, drop the zip from future commits.

### Bundle contents (`Final/`)

1. **Logos & icons** — `gotmessy-logo-{A,B,C}` (SVG + PNG + `@2x`; transparent variants for A; Logo A is the lead), `gotmessy-icon.svg`, `gotmessy-app-icon.png` (+ `@2x`)
2. **Reference sheets** — `gotmessy-color-sheet.png`, `gotmessy-type-sheet.png`
3. **Standalone HTML/PDF deliverables**:
   - `gotmessy-hub` — *Project Hub v2.0* (daily dashboard / asset index)
   - `gotmessy-brand-kit` — *Brand Identity Kit* (logos, colours, type, voice, domains)
   - `prompt-architect-infographic` — *App Architecture* infographic (product-view counterpart to `docs/system-design.md`)

The `claude/brand-guidelines-system-design` branch additionally tracks `Final/gotmessy-brand-guidelines.html` and `Final/gotmessy-system-design.html`.

### `-final` naming convention

Most assets exist twice: a working copy (no suffix) and a canonical `-final` variant — e.g. `gotmessy-logo-A.png` and `gotmessy-logo-A-final.png`. **The `-final` files are the shippable source of truth.** When they diverge, follow `-final`. Mirror this pairing when adding new assets.

## Brand tokens

Use these verbatim when generating UI or HTML. Source of truth: the `:root` CSS block in any HTML deliverable. Keep in sync when editing those files.

**Colours**

| Token | Hex | Role |
|---|---|---|
| `--cream` | `#FAF7F2` | Primary text on dark |
| `--warm` | `#F2EDE4` | Warm neutral / light-mode page background |
| `--ink` | `#1A1612` | Default page background (dark) |
| `--ink-soft` | `#3D3530` | Secondary background |
| `--dust` | `#C4B5A0` | Muted text / labels / metadata |
| `--clay` | `#C4673A` | Primary accent — links, buttons, terminal dot |
| `--clay-dk` | `#9B4A28` | Clay hover / pressed state |
| `--clay-lt` | `#E8896A` | Clay focus ring / large hero accents |
| `--sage` | `#5C7A62` | Success / live status |
| `--lav` | `#8B7BAB` | Secondary accent (categorisation) |
| `--sky` | `#5B8FA8` | Secondary accent (categorisation) |
| `--yellow` | `#E8C84A` | Highlight — use sparingly |
| `--card` | `#1E1A16` | Card surface |
| `--card-bd` | `rgba(255,255,255,0.08)` | Card border |

Accent budget: at most **three** of `--clay`, `--sage`, `--lav`, `--sky`, `--yellow` per screen.

**Forbidden**: pure white (`#FFF`) backgrounds, pure black (`#000`), electric blues/teals, high-saturation neons. Never recolour the terminal dot.

**Typography** — Google Fonts: `Lora` (serif) and `Poppins` (sans).

Wordmark: `got` in *Lora 400 italic* + `Messy` in **Lora 700** + terminal `.` in `--clay`. Never rebuild in Poppins or all-caps. Never recolour, rotate, skew, or animate the wordmark components independently.

Type scale (rem, 16px root): Display `clamp(3rem,7vw,5.5rem)` Lora 700 → H1 `2.25rem` → H2 `1.5rem` → H3 `1.15rem` → Body `0.875–1rem` Poppins → Caption `0.75rem`.

**Voice** — "A brilliant friend who happens to be great with words. Not a tutor. Not a robot. Not a hustle-culture coach."

Never use: *journey*, *unlock*, *unleash*, *supercharge*, *empower* (as filler), *AI-powered*, *cutting-edge*, *leverage* (verb), *learning curve*. One exclamation mark per page maximum, and only on genuine user wins.

**Domains** — `gotmessy.com` is the only consumer-facing domain. `cloudcomb.com` is held for the enterprise/team edition (deliberately different tone — do not cross-pollinate).

## GitHub Pages deployment

`static.yml` deploys the **entire repository** to GitHub Pages on every push to the default branch. This means:

- Every tracked file becomes publicly accessible at the Pages URL after merge to the default branch.
- Do not commit secrets, private drafts, or unlicensed assets — they will be public.
- HTML files in `Final/` (if the extracted directory ever merges) will be directly browseable.
- A green `static.yml` check = site is live. A green `blank.yml` check = nothing (placeholder only — ignore it).
- When a dedicated `site/` or `docs/` build step exists, scope `static.yml` to that output directory rather than deploying the whole repo root.

## Workflow conventions

- **Branch**: develop on the `claude/...` branch explicitly assigned to this task. Never push directly to the default branch or to another session's branch without explicit permission.
- **Commits**: write descriptive messages that explain the *why*. Match the style of recent merged history ("Add CLAUDE.md with brand-asset repo overview", "Add GitHub Pages deployment workflow"). Terse messages like "Update file" are no longer acceptable for design changes.
- **PRs**: open new work as a **draft PR** after the first push. All changes land on the default branch via PR — never direct push.
- **Asset changes**: when adding or updating a brand asset, capture *why* in the commit message. Re-run contrast/legibility checks if a colour token changed.
- **Paired docs**: `docs/brand-guidelines.md` and `Final/gotmessy-brand-guidelines.html` are paired — update both together. Same for `docs/system-design.md` and `Final/gotmessy-system-design.html`. If anything contradicts the Brand Identity Kit (`gotmessy-brand-kit-final.html`), the Kit wins — update both.
- **GitHub scope**: MCP tools in this session are restricted to the `hubbabubba-ai` repos listed in "Related repositories" above.

## Tokens package

`packages/tokens/` holds the shared `@gotmessy/tokens` package — the single place all app code imports brand values from.

**File layout:**

| File | Purpose |
|---|---|
| `src/colors.ts` | `colors` object (camelCase keys), `ColorToken` type, `accentTokens`, `ACCENT_BUDGET` |
| `src/typography.ts` | `fonts`, `fontWeights`, `typeScale`, `lineHeights`, `wordmark` |
| `src/css.ts` | `cssVars` — the full `:root { … }` string for web injection |
| `src/index.ts` | Barrel re-export |
| `package.json` | `@gotmessy/tokens`, `"type": "module"`, no build step (source TypeScript) |
| `tsconfig.json` | `NodeNext` module resolution, strict mode |

**Importing in app code:**

```ts
import { colors, typeScale, cssVars } from '@gotmessy/tokens';

// React Native style sheet
const styles = StyleSheet.create({
  heading: { fontFamily: typeScale.h1.font, fontSize: typeScale.h1.px, color: colors.cream },
});

// Web / Next.js — inject CSS vars once at the root
<style>{cssVars}</style>
```

**Regenerating tokens** (after editing the HTML source of truth):

```bash
python3 scripts/generate-tokens.py   # rewrites colors.ts and css.ts
```

Then update the CLAUDE.md colour table to match. The drift check will catch any mismatch in CI.

**Adding a new token:** add it to the HTML `:root` block first (source of truth), run `generate-tokens.py`, then update the CLAUDE.md colour table row.

## When application code lands

Asset-quality CI exists today (see "Quality checks"). When code is added:

1. Update this file with actual commands: build, test, lint, run-dev, run-single-test.
2. Add a short architecture overview for what has actually been built (distinct from the planned architecture above).
3. Add real test/build steps to `quality.yml` (or split into a separate `tests.yml`).
4. ~~If a `packages/tokens/` shared package is added~~ Done — see "Tokens package" below.
5. Document the IdP choice (Clerk vs Auth0) and any env vars required once the decision is made.
