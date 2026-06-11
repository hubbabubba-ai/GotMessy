# Got Messy — repository consolidation

This file is the authoritative record of the Got Messy repository consolidation.
The work had fragmented across **nine repositories in two GitHub accounts**
(`hubbabubba-ai` and `gotmessy`): one complete monorepo, an exact mirror, two
partial exports, an unrelated template, a separate UI-kit repo, and three
untouched upstream forks. That made it unclear where the source of truth lived
and produced duplicate, drifting copies.

**This repository — `hubbabubba-ai/GotMessy` — is the single canonical home.**
The genuinely-unique content from the other copies has been folded in here; the
redundant repos are being marked deprecated and point back here.

## Why `GotMessy` and not a brand-new repo

The original intent was a fresh, clean repo. The automation driving this
consolidation runs through a GitHub integration that is **scoped to the nine
existing repositories and cannot create new ones** (repo creation returns
`403 Resource not accessible by integration`). Rather than block, the
consolidation targets the most complete existing repository — this one — which
already held the full monorepo (`brand`, `prompts`, `tokens`) and green CI. If a
differently-named canonical repo is still wanted, create it in the GitHub UI and
push this branch's tree into it; nothing here is lost by doing so later.

## Repository landscape and disposition

| Repository | What it is | Disposition |
|---|---|---|
| **`hubbabubba-ai/GotMessy`** | Full monorepo: `packages/{brand,prompts,tokens}` + CI/tooling. Most complete, green CI. | **Canonical** — kept; UI kit + brand assets folded in |
| `gotmessy/currentmess` | Byte-identical mirror of GotMessy (same HEAD `70997ce`) | Deprecated → archive |
| `hubbabubba-ai/gotmessy.zoe` | Stripped partial export (tokens only, flattened `Final/`), 1 commit | Deprecated → archive |
| `hubbabubba-ai/messy` | Oldest snapshot — brand assets as `Final.zip` + stub docs | Deprecated → archive (assets migrated, see below) |
| `gotmessy/messyy` | Unrelated Cloudflare Workers template | Deprecated as unrelated → keep or move separately |
| `gotmessy/GotMessy` | Separate repo holding only the app UI kit (`ui_kits/app/`) | UI kit migrated here → deprecated → archive |
| `hubbabubba-ai/clerk-docs` | Untouched fork of `clerk/clerk-docs` | Out of scope — left untouched |
| `hubbabubba-ai/anthropic-quickstarts` | Untouched fork of Anthropic quickstarts | Out of scope — left untouched |
| `hubbabubba-ai/registry-hubbabubba` | Untouched fork of the shadcn registry template | Out of scope — left untouched |

## What was folded into this repo

- **App UI kit → `packages/ui-kit/`.** The clickable six-tool product mock
  (The Drop, Mirror It, Sort It Out, Make It, Just Tell Me, My Good Stuff) came
  from `gotmessy/GotMessy`, which only ever held this kit. It is self-contained
  (`app/index.html`, its own `colors_and_type.css`, and `assets/gotmessy-icon.svg`)
  so it renders standalone and sits outside the brand-asset CI scope.
- **Binary brand assets → `packages/brand/Final/`.** Logos (A/B/C, SVG + PNG +
  `@2x` + transparent variants), app icons, colour/type reference sheets, and the
  brand-kit / hub / infographic PDFs were extracted from `hubbabubba-ai/messy`'s
  `Final.zip` (the only place they lived) and added alongside the existing HTML
  deliverables. Every working asset has its `-final` sibling, so the asset-pair
  CI check passes. (The zip's HTML pages were intentionally **not** copied — the
  maintained HTML deliverables already live in `packages/brand/Final/`.)

## Manual follow-up (GitHub UI — cannot be done by the integration)

The integration cannot archive or delete repositories. Once the deprecation PRs
below are merged, archive these in the GitHub UI (Settings → Archive):

- [ ] `gotmessy/currentmess` — exact mirror, fully superseded
- [ ] `hubbabubba-ai/gotmessy.zoe` — partial export, fully superseded
- [ ] `hubbabubba-ai/messy` — brand assets migrated here
- [ ] `gotmessy/GotMessy` — UI kit migrated to `packages/ui-kit/`
- [ ] `gotmessy/messyy` — unrelated Workers app; archive **or** move it out of the Got Messy set

Leave the three upstream forks (`clerk-docs`, `anthropic-quickstarts`,
`registry-hubbabubba`) as they are.

## Deprecation PRs

Each redundant repo gets a branch `claude/consolidation-planning-1CBXN` adding a
`README` banner + `CONSOLIDATION-NOTICE.md` pointing here, opened as a PR. See the
session summary for the live PR links.
