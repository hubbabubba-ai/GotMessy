# Got Messy

A mobile-first prompt-engineering app for non-technical creators. Paste your messy raw thinking; get back a clean, reusable prompt template you can run on any LLM.

No app code has shipped yet — this repo holds brand/design assets, the app UI kit, and Phase 0 scaffolding.

> **Canonical repo.** This is the consolidated home for Got Messy. It supersedes the duplicate and partial copies (`currentmess`, `gotmessy.zoe`, `messy`, and the UI-kit-only `gotmessy/GotMessy`). See [`CONSOLIDATION.md`](CONSOLIDATION.md) for the full map and the archive checklist.

## Live deliverables

| File | What it is |
|---|---|
| [`packages/brand/Final/gotmessy-brand-guidelines.html`](packages/brand/Final/gotmessy-brand-guidelines.html) | Brand Identity Kit — colours, type, voice, logos |
| [`packages/brand/Final/gotmessy-system-design.html`](packages/brand/Final/gotmessy-system-design.html) | Engineering system design |
| [`packages/brand/Final/prompt-architect-infographic-final.html`](packages/brand/Final/prompt-architect-infographic-final.html) | App architecture — surfaces, phases, feature priorities |
| [`packages/ui-kit/app/index.html`](packages/ui-kit/app/index.html) | App UI kit — clickable six-tool product mock |

## Run CI locally

```bash
npx html-validate@9 "packages/brand/Final/**/*.html" "packages/brand/index.html"
npx markdownlint-cli2@0.13 "packages/brand/docs/**/*.md" "CLAUDE.md" "README.md"
bash packages/brand/scripts/brand-lint.sh
python3 packages/brand/scripts/check-token-drift.py
```

See `CLAUDE.md` for full quality-check details, brand token reference, and the planned tech stack.
