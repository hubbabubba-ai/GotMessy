# Got Messy

A mobile-first prompt-engineering app for non-technical creators. Paste your messy raw thinking; get back a clean, reusable prompt template you can run on any LLM.

No app code has shipped yet — this repo holds brand/design assets and Phase 0 scaffolding.

## Live deliverables

| File | What it is |
|---|---|
| [`Final/gotmessy-brand-guidelines.html`](Final/gotmessy-brand-guidelines.html) | Brand Identity Kit — colours, type, voice, logos |
| [`Final/gotmessy-system-design.html`](Final/gotmessy-system-design.html) | Engineering system design |
| [`Final/prompt-architect-infographic-final.html`](Final/prompt-architect-infographic-final.html) | App architecture — surfaces, phases, feature priorities |
| [`Final/gotmessy-hub.html`](Final/gotmessy-hub.html) | Project Hub — daily asset index |

## Run CI locally

```bash
npx html-validate@9 "Final/**/*.html" "index.html"
npx markdownlint-cli2@0.13 "docs/**/*.md" "CLAUDE.md" "README.md"
bash scripts/brand-lint.sh
python3 scripts/check-token-drift.py
```

See `CLAUDE.md` for full quality-check details, brand token reference, and the planned tech stack.
