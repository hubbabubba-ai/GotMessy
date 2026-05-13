# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a repo in the **hubbabubba-ai** GitHub organisation for the **Got Messy** brand — an AI-powered prompt-engineering app for non-technical creators ("real people with real chaos"). The repository currently holds brand/design assets and product planning documentation. No shipping application code has landed yet.

**Current contents:**

| Path | Description |
|---|---|
| `README.md` | Project overview — deliverables index, CI quick-start |
| `package.json` | npm workspaces root (`packages/*`); node ≥20 engine pin |
| `tsconfig.json` | Root TypeScript config — bundler resolution, `react-native` JSX, `@gotmessy/tokens` path alias |
| `.env.example` | Environment variable template — Clerk keys (Next.js + Expo), LLM providers, database, R2 |
| `packages/brand/` | Brand-asset workspace package (`@gotmessy/brand`) — see below |
| `packages/brand/index.html` | Landing page deployed at the Pages root; links to all HTML deliverables |
| `packages/brand/Final/` | HTML deliverables — brand guidelines, system design, app architecture infographic |
| `packages/brand/docs/brand-guidelines.md` | Operational brand rules |
| `packages/brand/docs/system-design.md` | Full system architecture document |
| `packages/brand/docs/app-structure.md` | App surfaces, Architect phases, feature priority — paired with `packages/brand/Final/prompt-architect-infographic-final.html` |
| `packages/brand/scripts/brand-lint.sh` | Forbidden-words / forbidden-colors / exclamation-budget checker (rules sourced from this file) |
| `packages/brand/scripts/check-token-drift.py` | Asserts brand-token table here matches the `:root` block in each HTML deliverable **and** the TS package |
| `packages/brand/scripts/generate-tokens.py` | Regenerates `packages/tokens/src/colors.ts` and `css.ts` from the HTML source of truth |
| `packages/tokens/` | Shared design-token package (`@gotmessy/tokens`) — see "Tokens package" below |
| `.github/workflows/quality.yml` | **Quality CI** — TypeScript typecheck, HTML validation, link check, accessibility (pa11y, WCAG 2.1 AA), Markdown lint, brand-rule lint, brand-token drift, asset-pair check |
| `.github/workflows/static.yml` | **Deployment** — publishes `packages/brand/index.html`, `Final/`, and `docs/` to GitHub Pages on every push to the default branch |
| `.claude/settings.json` | Enables the `superpowers@claude-plugins-official` plugin |

Treat this repo as a brand/design package until application code is added. The build/lint/test surface today is asset-quality only — see "Quality checks" below.

## Quality checks

`quality.yml` runs on every push and PR to `main`. To reproduce locally from the repo root:

```bash
npx html-validate@9 "packages/brand/Final/**/*.html" "packages/brand/index.html"
npx markdownlint-cli2@0.13 "packages/brand/docs/**/*.md" "CLAUDE.md" "README.md"
bash packages/brand/scripts/brand-lint.sh
python3 packages/brand/scripts/check-token-drift.py
# Link check (requires lychee):
npx lychee --no-progress --exclude-mail --accept 200,206,403,429 'packages/brand/Final/**/*.html' 'packages/brand/docs/**/*.md' 'packages/brand/index.html' 'CLAUDE.md'
# Accessibility audit (serves repo on :8080 then audits):
npx http-server@14 -p 8080 -s & sleep 1 && npx pa11y-ci@3 --config .pa11yci ; kill %1
```

Brand-rule details:

- **Forbidden words** (case-insensitive, word-boundary): `journey`, `unlock`, `unleash`, `supercharge`, `empower`, `AI-powered`, `cutting-edge`, `leverage`, `learning curve`. Per-line override: append `<!-- brand-lint-allow -->` to the line (e.g. cautionary "Never" examples in `packages/brand/docs/brand-guidelines.md`).
- **Forbidden colors**: pure white (`#FFF`/`#FFFFFF`) and pure black (`#000`/`#000000`) in HTML/CSS contexts. Use `--cream` / `--ink` instead.
- **Exclamation budget**: at most one `!` per HTML page (excluding `!important`, `!=`, `!DOCTYPE`, comments, and `brand-lint-allow` lines).
- **Token drift**: every token in the colour table below must match (1) the `:root { ... }` block in each `packages/brand/Final/*.html`, (2) the `colors` object in `packages/tokens/src/colors.ts`, and (3) the `:root` block in `packages/tokens/src/css.ts`. The HTML is the source of truth — when they diverge, run `python3 packages/brand/scripts/generate-tokens.py` to regenerate the TS package, then update CLAUDE.md.
- **Asset-pair check**: every working asset (`logo-A.png`, etc.) must have a `-final` sibling. Skipped silently if `packages/brand/Final/` contains only HTML.

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

Read `packages/brand/docs/system-design.md` for the full engineering spec. Summary:

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
| Identity | **Clerk** (chosen — see "Identity" below) |
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

See `packages/brand/docs/system-design.md §9` for phase exit criteria. Each phase ships behind a feature flag.

## Brand assets (`packages/brand/`)

All brand deliverables live in `packages/brand/`:

| Path | Description |
|---|---|
| `Final/gotmessy-brand-guidelines.html` | Brand Identity Kit — logos, colours, type, voice, domains |
| `Final/gotmessy-system-design.html` | Engineering system design |
| `Final/prompt-architect-infographic-final.html` | App architecture infographic (canonical `-final` version) |
| `Final/prompt-architect-infographic.html` | Working copy of the infographic |
| `docs/brand-guidelines.md` | Paired Markdown source for brand guidelines HTML |
| `docs/system-design.md` | Paired Markdown source for system design HTML |
| `docs/app-structure.md` | App surfaces, Architect phases, and feature priority |
| `index.html` | Pages landing page — links to all HTML deliverables |

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

`static.yml` assembles a `_site/` directory from `packages/brand/` and deploys it to GitHub Pages on every push to the default branch. Only the public-facing files are published:

- `packages/brand/index.html` → `_site/index.html`
- `packages/brand/Final/` → `_site/Final/`
- `packages/brand/docs/` → `_site/docs/`

Config files, scripts, `.github/`, and `CLAUDE.md` are excluded — none of these need to be publicly browseable. Do not commit secrets, private drafts, or unlicensed assets — they will be public once merged to the default branch.

A green `static.yml` check = site is live.

## Workflow conventions

- **Branch**: develop on the `claude/...` branch explicitly assigned to this task. Never push directly to the default branch or to another session's branch without explicit permission.
- **Commits**: write descriptive messages that explain the *why*. Match the style of recent merged history ("Add CLAUDE.md with brand-asset repo overview", "Add GitHub Pages deployment workflow"). Terse messages like "Update file" are no longer acceptable for design changes.
- **PRs**: open new work as a **draft PR** after the first push. All changes land on the default branch via PR — never direct push.
- **Asset changes**: when adding or updating a brand asset, capture *why* in the commit message. Re-run contrast/legibility checks if a colour token changed.
- **Paired docs**: `packages/brand/docs/brand-guidelines.md` and `packages/brand/Final/gotmessy-brand-guidelines.html` are paired — update both together. Same for `docs/system-design.md` and `Final/gotmessy-system-design.html`. If anything contradicts the Brand Identity Kit (`gotmessy-brand-kit-final.html`), the Kit wins — update both.
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
python3 packages/brand/scripts/generate-tokens.py   # rewrites colors.ts and css.ts
```

Then update the CLAUDE.md colour table to match. The drift check will catch any mismatch in CI.

**Adding a new token:** add it to the HTML `:root` block first (source of truth), run `generate-tokens.py`, then update the CLAUDE.md colour table row.

## Identity (Clerk)

**Clerk** is the chosen IdP. Decision rationale: best-in-class React Native / Expo support, pre-built UI components (magic links, social login, MFA), generous free tier (10k MAUs), and no self-hosted infrastructure to maintain.

**Environment variables** — copy `.env.example` → `.env.local` (never commit `.env.local`):

| Variable | Where used | Notes |
|---|---|---|
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Next.js web | Safe for browser bundles |
| `CLERK_SECRET_KEY` | Next.js server / API routes | Keep server-side only |
| `EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY` | Expo / React Native | Prefix required by Expo |
| `NEXT_PUBLIC_CLERK_SIGN_IN_URL` | Next.js | Default `/sign-in` |
| `NEXT_PUBLIC_CLERK_SIGN_UP_URL` | Next.js | Default `/sign-up` |
| `NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL` | Next.js | Post-auth redirect |
| `NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL` | Next.js | Post-auth redirect |

Get API keys from [dashboard.clerk.com](https://dashboard.clerk.com) → your app → API Keys.

**When adding Clerk to a new package/app:** install `@clerk/nextjs` (web) or `@clerk/clerk-expo` (mobile). Wrap the root layout in `<ClerkProvider publishableKey={…}>`. Protect routes with Clerk's `auth()` middleware (Next.js) or `useAuth()` hook (Expo).

## When application code lands

Asset-quality CI exists today (see "Quality checks"). When code is added:

1. Update this file with actual commands: build, test, lint, run-dev, run-single-test.
2. Add a short architecture overview for what has actually been built (distinct from the planned architecture above).
3. Add real test/build steps to `quality.yml` (or split into a separate `tests.yml`).
4. ~~If a `packages/tokens/` shared package is added~~ Done — see "Tokens package" below.
5. ~~Document the IdP choice (Clerk vs Auth0) and any env vars required~~ Done — see "Identity (Clerk)" above.
