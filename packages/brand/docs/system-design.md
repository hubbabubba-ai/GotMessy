# Got Messy — System Design

Engineering counterpart to the *App Architecture* infographic (`Final/prompt-architect-infographic-final.html`). The infographic is the **product** view — what the user experiences. This document is the **system** view — what we build, how the pieces talk, and where the risk lives.

If the infographic and this document disagree, this document wins for engineering decisions; the infographic wins for product naming and user-facing structure. Update both together.

---

## 1. Product summary (one-screen recap)

Got Messy is a **mobile-first prompt-engineering app** for non-technical creators. It accepts messy raw input (text, PDFs, URLs) and produces validated, reusable prompt templates the user can run on the LLM of their choice.

The infographic defines the surface in **Hub & Spoke**:

| ID | Surface | Purpose |
|---|---|---|
| 1.0 | Home Dashboard *(Hub)* | Index, recent activity, quick start |
| 2.0 | The Architect *(core spoke, MVP)* | The four-phase prompt builder |
| 3.0 | The Vault | My Good Stuff, Community Recipes, Favourites |
| 4.0 | Settings | Model toggle, User DNA, billing/keys |

The Architect is the core engine. Everything else is scaffolding around it.

---

## 2. Architecture at a glance

```text
┌───────────────────────────────────────────────────────────────────┐
│                        Mobile / Web Client                        │
│   (React Native + React Native Web, or Expo + Next.js shell)      │
└──────────────────────┬──────────────────────────┬─────────────────┘
                       │ HTTPS / JSON             │ Auth (OAuth + email)
                       ▼                          ▼
              ┌─────────────────┐        ┌──────────────────┐
              │   API Gateway   │◄──────►│  Identity (IdP)  │
              │ (Edge / BFF)    │        │  e.g. Clerk/Auth0│
              └────────┬────────┘        └──────────────────┘
                       │
   ┌───────────────────┼─────────────────────────────┐
   ▼                   ▼                             ▼
┌─────────┐    ┌─────────────────┐         ┌──────────────────┐
│  Smart  │    │   Architect /   │         │   Vault / Tags   │
│  Paste  │◄──►│   Triple-Pillar │◄───────►│   (CRUD store)   │
│ Service │    │   Service       │         └────────┬─────────┘
└────┬────┘    └────────┬────────┘                  │
     │                  │                           │
     │   ┌──────────────┴─────────────┐             │
     ▼   ▼                            ▼             ▼
┌────────────┐              ┌──────────────────┐  ┌──────────┐
│ NLP/Intent │              │  LLM Gateway     │  │ Postgres │
│ Classifier │              │  (multi-provider │  │  + pgvec │
│ + PII guard│              │   router/cache)  │  │          │
└─────┬──────┘              └────────┬─────────┘  └──────────┘
      │                              │
      │                  ┌───────────┼───────────┐
      ▼                  ▼           ▼           ▼
┌────────────┐    ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Object     │    │  Gemini  │ │  OpenAI  │ │ Anthropic│
│ store      │    │   API    │ │   API    │ │   API    │
│ (S3/R2)    │    └──────────┘ └──────────┘ └──────────┘
└────────────┘
```

The single non-obvious piece is the **LLM Gateway** — see §6.

---

## 3. Components

### 3.1 Client

- **Stack**: React Native (Expo) + React Native Web for the marketing/site shell. One codebase, three targets (iOS, Android, Web). Mobile is the primary design target per the infographic.
- **Routing**: Expo Router (file-based) on native, Next.js for `gotmessy.com` marketing pages.
- **State**: server state via TanStack Query; UI state via Zustand. No Redux.
- **Design tokens**: pulled from the brand kit's `:root` CSS into a shared theme file (`/packages/tokens/`). Source of truth: the kit. Do not redefine hex values in component code.
- **Editor surface**: the Triple-Pillar editor is a custom form, not a rich-text editor. Treat it as three controlled fields (Persona, Task, Format) plus an optional Context attachment list.

### 3.2 API Gateway / BFF

A thin edge layer (Hono on Cloudflare Workers, or Next.js API routes co-located with the marketing site) that:

- Terminates auth (validates the IdP-issued session/JWT).
- Rate-limits per user/IP (default: 60 req/min, burst 20).
- Adds request IDs and structured logs.
- Forwards to the right downstream service.

The BFF *does not* call LLM providers directly — it always goes through the LLM Gateway (§6) so we keep one place to track tokens, redact PII, and enforce model routing.

### 3.3 Smart Paste service

Implements the Smart Paste flow from the infographic:

```text
The Drop  →  Intent Classifier  →  Sanity Check (PII)  →  Pillar Mapping
```

| Stage | Responsibility | Tech |
|---|---|---|
| The Drop | Accept text/PDF/URL. Extract text from PDFs (pdfjs / pdf-parse) and HTML (Readability for URL fetches). | Node service |
| Intent Classifier | NLP pass: detect Action Verbs (Task), Role signals (Persona), Output keywords (Format). Phase 1: a small LLM call (Haiku/Flash) with a strict JSON schema. Phase 2: distilled model for cost. | Calls LLM Gateway |
| Sanity Check | Detect and redact PII (emails, phone numbers, names, addresses). Two modes: **Strict** (drop the field), **Standard** (replace with placeholders like `{{email}}`). Uses regex + an NER pass for names. | Local (no LLM call required for the regex tier) |
| Pillar Mapping | Emit the Triple-Pillar JSON the editor will hydrate. | Pure function |

The service is stateless. Inputs and outputs are persisted via the Vault service if the user explicitly saves.

### 3.4 Architect / Triple-Pillar service

Owns the lifecycle of a *Prompt Draft*:

- Create from Smart Paste output, or from scratch, or from a Vault template.
- Validate that all three pillars are present before "Test Flight" is allowed.
- Run **Test Flight**: send the assembled prompt + variables to the LLM Gateway, return the response, score it (Phase 2: Hallucination Risk Score).
- Export: produce shareable artifacts (clipboard string, deep link to ChatGPT/Claude/Gemini, save-to-Vault).

State machine for a draft:

```text
empty → drafting → ready (3 pillars filled) → flight_pending → flight_done → exported
                            ▲                                     │
                            └─────────── revise ──────────────────┘
```

### 3.5 Vault service

CRUD over user-owned and community resources:

- **My Good Stuff** — user-owned templates (private by default).
- **Community Recipes** — public, moderated templates.
- **Favourites** — soft references to either of the above.
- **Tags** — a flat tag space; supports search (full-text + vector — see §4).

### 3.6 Identity

External IdP (Clerk or Auth0). Required because:

- Mobile + web with shared sessions is painful to roll ourselves.
- Social sign-in is table stakes for the target audience.
- Multi-LLM flows mean we'll handle bring-your-own-API-key — outsourcing identity lets us focus that energy on the BYOK vault.

User identity = IdP `sub`. We store our own user row keyed on that, never the email.

---

## 4. Data model

Postgres (Neon or Supabase) with `pgvector` for embeddings.

```text
users              prompt_drafts             vault_templates
─────              ─────────────             ───────────────
id (pk)            id (pk)                   id (pk)
idp_sub            owner_id  → users         owner_id   → users (nullable for community)
created_at         persona   text            visibility  enum(private|community)
user_dna jsonb     task      text            title       text
                   format    text            persona/task/format
                   context_files  jsonb      variables   jsonb
                   variables jsonb           tags        text[]
                   state     enum            embedding   vector(1536)
                   created_at, updated_at    fork_of     → vault_templates (nullable)
                                             created_at, updated_at

flight_runs                   model_keys (BYOK)
───────────                   ─────────────────
id (pk)                       id (pk)
draft_id  → prompt_drafts     owner_id → users
provider  enum                provider enum
model_id  text                ciphertext bytea  -- envelope encrypted, see §7
input_tokens int              created_at
output_tokens int             revoked_at
latency_ms int
risk_score numeric(3,2)
output_text text
created_at
```

**`user_dna`** is a free-form JSONB blob: `{role, life_status, location, interests, default_persona}`. The infographic treats it as global context that auto-prefixes prompts; the schema treats it as opaque key/value the Architect service knows how to render into the system message.

**Embeddings** on `vault_templates.embedding` power semantic search and "more like this" in My Good Stuff. Use `text-embedding-3-small` (1536d) for cost.

---

## 5. API surface (sketch)

REST/JSON over the BFF. Versioned at `/v1/`.

| Method | Path | Notes |
|---|---|---|
| `POST` | `/v1/paste` | Smart Paste: accepts `{text?, pdf_url?, url?}`. Returns Triple-Pillar suggestion. |
| `POST` | `/v1/drafts` | Create draft (from Smart Paste payload or scratch). |
| `PATCH` | `/v1/drafts/{id}` | Update pillars / context / variables. |
| `POST` | `/v1/drafts/{id}/flight` | Test Flight — runs against selected provider. SSE stream for tokens. |
| `POST` | `/v1/drafts/{id}/export` | Returns export bundle (clipboard string, provider-specific deep link). |
| `POST` | `/v1/vault` | Save a template (from a draft or from scratch). |
| `GET` | `/v1/vault?q=&tags=` | Search My Good Stuff + favourites. |
| `GET` | `/v1/community?q=` | Search community recipes. |
| `POST` | `/v1/keys` | BYOK — store an encrypted provider key. |
| `GET` | `/v1/me/dna` / `PUT` | Read/write User DNA. |

Auth on every route except marketing. Rate-limit `/v1/paste` and `/v1/flight` more strictly — they're the expensive ones.

---

## 6. LLM Gateway (the load-bearing piece)

A single internal service that all three downstream callers (Smart Paste, Architect, Vault embeddings) use to reach the providers.

### Why a gateway

- One place to redact PII before egress.
- One place to count tokens, attribute cost to a user, enforce per-user quotas.
- Provider-agnostic interface — adding a fourth provider is one adapter, not a re-plumb.
- Caching: response cache keyed on `(provider, model, deterministic-prompt-hash)` for prompts run with `temperature=0` and no User DNA — saves cost on repeated Test Flights.
- Failover: if Gemini Flash 429s, fall back to Haiku for the same intent class.

### Routing policy (default, when user hasn't pinned a model)

| Job | Default model | Why |
|---|---|---|
| Intent classification (Smart Paste) | Gemini Flash *or* Claude Haiku | Cheap, fast, JSON-mode reliable. |
| Embeddings | OpenAI `text-embedding-3-small` | Cheapest/best 1536d. |
| Test Flight | User's selected model (Settings 4.0) | We're a multi-LLM tool — never silently swap on the user. |
| Hallucination Risk Score (V2) | Same provider as Test Flight, smaller sibling | Avoid confirmation bias from the same model size. |

### Provider adapters

Each adapter implements `complete()`, `stream()`, `embed()`, returns a normalised `{tokens_in, tokens_out, finish_reason, content, raw}`. Provider-specific quirks (system message support, image inputs, JSON mode flags) live inside the adapter, not leaked.

### Token budgeting

Every gateway call is logged to `flight_runs` (or an aggregate table for non-flight calls). Free-tier users hit a monthly cap; BYOK users are billed by their own provider and tracked for quota only.

---

## 7. Security and PII

The product handles user-pasted content that is **likely to contain sensitive material** (emails, contracts, drafts of personal letters). Treat this as a hot path.

### PII rules

- **Outbound to LLM providers**: Sanity Check (§3.3) runs *before* every outbound call. Strict mode is the default for free tier; Standard mode is opt-in per draft.
- **Storage**: never store provider responses keyed by raw PII. The `flight_runs.output_text` column is encrypted at rest at the column level.
- **Logging**: structured logs redact known PII patterns. Drop request bodies from logs entirely above DEBUG.

### BYOK

User-supplied API keys are stored with **envelope encryption**: a per-user data key (encrypted with a KMS-managed master key) wraps the actual provider key. The plaintext provider key is decrypted only inside the LLM Gateway process at call time, never returned to the client.

### Auth

- IdP-issued JWTs, short-lived (15 min) + refresh.
- All endpoints require auth except marketing pages and `/v1/health`.
- CORS: `gotmessy.com` and `*.gotmessy.com` only. No wildcard origins.
- CSRF: use `SameSite=Lax` cookies; mutation endpoints require an explicit `Origin` check.

---

## 8. Mobile-first considerations

The infographic states "Mobile-First Design" as a first-class stat. That implies:

- The Triple-Pillar editor must be usable one-handed. Persona/Task/Format are not three columns — they're three vertically-stacked steppers on phones.
- The Drop must accept share-sheet input from iOS/Android (Share to Got Messy → opens directly in The Drop).
- Test Flight responses stream — long waits on a mobile connection without progress feedback are unacceptable.
- Offline: the Vault is read-cached locally so My Good Stuff is browseable without a connection; new drafts queue and replay.
- Push: opt-in. One use case: long-running Community Recipe runs.

---

## 9. Build & release roadmap

The infographic outlines a Build Roadmap; this is the engineering version with explicit gates.

| Phase | Scope | Exit criteria |
|---|---|---|
| **0 — Foundations** | Repo scaffolding, IdP integration, design tokens shared package, CI on PRs. | Auth round-trip works on web + native; tokens import in both apps. |
| **1 — Architect MVP** | Smart Paste (text only), Triple-Pillar editor, single provider Test Flight (one of Gemini/OpenAI/Anthropic), basic Vault save. | A target user can paste an email, get pillars, run Test Flight, save the result. |
| **2 — Multi-LLM** | LLM Gateway with all three providers, Settings model toggle, BYOK. | User can pick a provider in Settings and Test Flight uses it. BYOK round-trip works. |
| **3 — Smart Paste full** | PDF and URL inputs, Sanity Check (Strict + Standard), Intent Classifier production model. | PDF and URL inputs end-to-end; PII redaction validated against test corpus. |
| **4 — Vault expansion** | Community Recipes (public + moderation), tags, semantic search via embeddings. | A second user can discover and fork a public template. |
| **5 — User DNA** | Onboarding capture, persistence, auto-injection at flight time. | DNA injection visibly improves outputs on a benchmark set. |
| **6 — Risk scoring (V2)** | Hallucination Risk Score, citation extraction. | Score correlates (rank-order) with human eval on a held-out set. |
| **7 — Life OS edition** | Long-running workflows, scheduled prompts, share-sheet integration. | Out of scope for this doc — re-design before starting. |

Each phase ships behind a feature flag and rolls out to a percentage cohort before general release.

---

## 10. Observability

- **Tracing**: OpenTelemetry, propagated from client → BFF → services → LLM Gateway. The full path of a Test Flight should appear as one trace.
- **Metrics**: per-provider latency, token cost per user per day, Smart Paste pillar-detection success rate, Test Flight failure rate.
- **Logs**: structured JSON, level-gated PII redaction (see §7).
- **Errors**: Sentry on client + server. Group by `idp_sub` so we can find affected users without storing emails in error context.

---

## 11. Cost model (rough)

The single biggest variable cost is LLM tokens. Approximate per-flight cost at MVP scale:

| Operation | Tokens (typical) | Cost (USD, mid-tier model) |
|---|---|---|
| Intent classification | 500 in / 200 out | ~$0.0015 |
| Test Flight (default model) | 800 in / 1.2k out | ~$0.012 |
| Embedding for Vault save | 500 in | ~$0.00001 |

A free-tier user doing 20 flights/day costs ~$0.30/day in LLM tokens. The free-tier cap should fit inside that.

BYOK users cost us approximately zero in LLM tokens — just gateway compute and Postgres rows. This is why BYOK is a Phase 2 deliverable, not Phase 5.

---

## 12. Open questions / decisions to resolve

These are explicitly **not decided** — flag the trade-off when they come up rather than picking silently.

- **IdP**: Clerk vs Auth0 vs Supabase Auth. Lean Clerk for DX, but pricing tiers warrant a comparison at scale.
- **Hosting**: Cloudflare Workers + Neon, or a single Vercel/Railway stack. Workers is cheaper at scale, more friction for long-running jobs.
- **Mobile distribution**: Expo Go for early testers, then EAS-built bare RN. App Store vs PWA-first is a product call.
- **Moderation for Community Recipes**: human review queue vs automated classifier with reports. Probably both, but order of build matters.
- **Risk Score (V2) methodology**: dual-model agreement, fact-checking via search, or human-eval-trained classifier. Each has different cost shapes.
- **Subscription tiers**: free / pro / team — pricing not set; impacts BYOK quota design.

When any of these resolve, update this file in the same commit as the implementation.
