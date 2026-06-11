# Intent Classifier — System Prompt

Built-in classification prompt for Got Messy's **Smart Paste** feature (The Architect, Phase 1).

---

## Deployment

| Target | How to use |
|---|---|
| Got Messy Smart Paste service | Import from `@gotmessy/prompts` — see `INTENT_CLASSIFIER_CONFIG` |
| Anthropic API | Pass as `system` parameter in `/v1/messages` with `temperature: 0` |

**Recommended settings**

| Setting | Value |
|---|---|
| Model | `claude-haiku-4-5-20251001` |
| Max tokens | `256` |
| Temperature | `0` (deterministic classification) |
| Tools | None |

---

## Purpose

This prompt turns raw, unstructured user input (text, extracted PDF text, scraped URL content) into a validated **Triple-Pillar suggestion** — a `{ persona, task, format }` JSON object that hydrates the Triple-Pillar editor.

It is the core of the **Intent Classifier** stage in the Smart Paste flow:

```text
The Drop → Intent Classifier → Sanity Check → Pillar Mapping → Triple-Pillar Editor
```

---

## Output schema

```json
{
  "persona": "string — role the AI should adopt",
  "task": "string — single action-verb directive",
  "format": "paragraph | list | table | json | email | script",
  "confidence": {
    "persona": "high | medium | low",
    "task": "high | medium | low",
    "format": "high | medium | low"
  }
}
```

The `confidence` field drives UX: high-confidence pillars auto-fill; low-confidence ones open with a helper prompt in the editor so the user knows to review before running Test Flight.

---

## TypeScript type

```ts
import { type TriplePillarSuggestion } from '@gotmessy/prompts';
```

---

## Source

```text
packages/prompts/src/intent-classifier.ts
```

Exports: `INTENT_CLASSIFIER_SYSTEM_PROMPT` (string), `INTENT_CLASSIFIER_CONFIG` (full config object), `TriplePillarSuggestion` (output type).

Do not edit the prompt text in this file — edit the TypeScript source and keep this document's metadata sections in sync.
