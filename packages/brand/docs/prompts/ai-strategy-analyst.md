# AI Strategy Analyst — System Prompt

Built-in persona for the Got Messy **Analyze** tool variant.
Also deployable standalone via the Anthropic API or Claude.ai Projects.

---

## Deployment

| Target | How to use |
|---|---|
| Got Messy Analyze variant | Import from `@gotmessy/prompts` — see `AI_STRATEGY_ANALYST_CONFIG` |
| Anthropic API | Pass as `system` parameter in `/v1/messages` |
| Claude.ai Projects | Paste into Project Instructions field |

**Recommended settings**

| Setting | Value |
|---|---|
| Model | `claude-sonnet-4-6` |
| Max tokens | `8096` |
| Tools | `web_search` (enable for tool evaluation tasks requiring current pricing or capability data) |

---

## Purpose

This prompt configures an AI as a **senior AI strategy analyst** — an intellectual peer and challenger, not a validator. Designed for non-technical creators who need rigorous, framework-driven analysis of AI tools, workflows, and architectures without dense implementation jargon.

---

## Analyst modes

The prompt instructs the model to silently select a mode before responding:

| Mode | When it applies |
|---|---|
| Tool Evaluator | Comparing platforms, APIs, vendors; build-vs-buy; capability benchmarking |
| Architecture Reviewer | System design critique; pipeline structure; agent patterns |
| Workflow Designer | Mapping AI into human workflows; automation opportunities; handoff design |
| Prompt Strategist | Prompt engineering critique; instruction library design |
| Product Strategist | AI product development; feature scoping; user mental model analysis |
| Risk & Constraints Analyst | Failure mode identification; vendor lock-in risks; ethical constraints |

When a request spans multiple modes, the model sequences them with explicit section headers.

---

## Response format conventions

- **Evaluations**: Framework → scored comparison → recommendation with explicit trade-off
- **Architecture reviews**: Current state → risks/gaps → alternatives → recommended path
- **Strategy**: Problem reframe → options with trade-offs → decision criteria → direction
- **Prompt critiques**: Structural assessment → failure modes → improvement recommendations

---

## Source

The canonical prompt text and config object live in:

```
packages/prompts/src/ai-strategy-analyst.ts
```

Exports: `AI_STRATEGY_ANALYST_SYSTEM_PROMPT` (string), `AI_STRATEGY_ANALYST_CONFIG` (full config object).

Do not edit the prompt text in this file — edit the TypeScript source and keep this document's metadata sections in sync.
