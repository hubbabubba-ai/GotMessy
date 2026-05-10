# Got Messy &mdash; App Architecture & Structure

Product counterpart to `docs/system-design.md`. The system design is the **engineering** view; this document is the **product** view &mdash; what the user experiences, how the surfaces connect, and which features ship first.

HTML deliverable: [`Final/prompt-architect-infographic-final.html`](../Final/prompt-architect-infographic-final.html)

---

## 1. Hub & Spoke Overview

Got Messy uses a Hub & Spoke layout navigated by a single bottom tab bar.

| ID | Surface | Role |
|---|---|---|
| 1.0 | Home Dashboard *(Hub)* | Quick Actions, Recent Projects, Daily Challenge |
| 2.0 | The Architect *(Core Spoke &mdash; MVP)* | Four-phase prompt builder |
| 3.0 | The Vault | My Templates, Community Recipes, Favourites |
| 4.0 | Settings & Profile | API Config, Default Persona, Credits |

The Architect is the engine. Everything else orbits it.

---

## 2. The Architect &mdash; Four Phases

### Phase 1 &mdash; Input (Smart Paste)

| Component | ID | Purpose |
|---|---|---|
| The Dump Zone | 2.1.1 | Accept raw text, no format required. Share-sheet compatible. |
| Intent Classifier | 2.1.2 | NLP detection maps content to Persona / Task / Format signals. |

### Phase 2 &mdash; Structure (Triple-Pillar Editor)

| Component | ID | Purpose |
|---|---|---|
| Persona Selector | 2.2.1 | Role picker or free-text custom persona. |
| Task Definer | 2.2.2 | Single action phrase per prompt. |
| Format Gallery | 2.2.3 | Card-based visual picker (paragraph, list, table, JSON, email, script). |
| Context Manager | 2.2.4 | Optional attachments: constraints, examples, reference material. |

### Phase 3 &mdash; Validation (Test Flight)

| Component | ID | Purpose |
|---|---|---|
| Split-Screen Simulator | 2.3.1 | Run prompt against selected model; SSE streaming output. |
| Variable Injector | 2.3.2 | Replace `{{variable}}` tokens with real values before running. |
| Hallucination Check | 2.3.3 | Risk score. **V2 only &mdash; not in MVP scope.** |

### Phase 4 &mdash; Export

| Component | ID | Purpose |
|---|---|---|
| Copy to Clipboard | 2.4.1 | One tap &mdash; full assembled prompt, variables injected. |
| Save to Library | 2.4.2 | Saves to The Vault (My Good Stuff, private by default). |
| Share | 2.4.3 | Deep links to ChatGPT, Claude, Gemini; mobile share sheet. |

---

## 3. Feature Priority Hierarchy

### Critical &mdash; must ship at launch

- **Smart Paste / Intent Classifier** &mdash; turns raw input into structured pillars.
- **Triple-Pillar Editor** &mdash; Persona, Task, Format with validation before Test Flight.

### High &mdash; launch window

- **Smart Start** &mdash; one-tap guided session for first-time users.
- **Visual Format Gallery** &mdash; card-based format picker.
- **Test Flight Simulator** &mdash; split-screen output view inside the app.

### Medium &mdash; post-launch

- **Recent Projects** &mdash; last five drafts on Dashboard with Resume.
- **Variable Injection** &mdash; token replacement for repeatable templates.
- **Recipe Book** &mdash; Community Recipes in The Vault (requires moderation).

### V2 &mdash; deferred

- **Hallucination Scorer** &mdash; dual-model risk scoring; needs human-eval validation first.
- **Model Toggle** &mdash; provider selection in Settings; blocked on LLM Gateway readiness.

---

## 4. Strategic Recommendations

**1. MVP Focus: Ship Smart Paste + Triple-Pillar Editor first.**
Phases 2.1 and 2.2 are the product. The Vault and Dashboard only have value when there is prior work to surface. Do not build those surfaces before the core engine works reliably.

**2. Navigation: bottom tab bar with four destinations.**
Dashboard, Architect, Library, Settings. Four tabs map exactly to the four surfaces. Keep the structure flat at launch; nested navigation can wait until The Vault needs filtering.

**3. Onboarding: first launch goes straight to The Architect.**
A guided session on first open, bypassing the Dashboard entirely. The Dashboard depends on prior work; show it when there is something to show.

---

## 5. Sitemap hierarchy

```text
App
├── 1.0 Home Dashboard
│   ├── 1.1 Quick Actions
│   │   ├── 1.1.1 New Project
│   │   └── 1.1.2 Paste from Clipboard
│   ├── 1.2 Recent Projects (last 5 drafts)
│   └── 1.3 Daily Challenge
├── 2.0 The Architect
│   ├── 2.1 Input / Smart Paste
│   │   ├── 2.1.1 The Dump Zone
│   │   └── 2.1.2 Intent Classifier
│   ├── 2.2 Structure / Triple-Pillar Editor
│   │   ├── 2.2.1 Persona Selector
│   │   ├── 2.2.2 Task Definer
│   │   ├── 2.2.3 Format Gallery
│   │   └── 2.2.4 Context Manager
│   ├── 2.3 Validation / Test Flight
│   │   ├── 2.3.1 Split-Screen Simulator
│   │   ├── 2.3.2 Variable Injector
│   │   └── 2.3.3 Hallucination Check (V2)
│   └── 2.4 Export
│       ├── 2.4.1 Copy to Clipboard
│       ├── 2.4.2 Save to Library
│       └── 2.4.3 Share
├── 3.0 The Vault
│   ├── 3.1 My Good Stuff (private templates)
│   ├── 3.2 Community Recipes (public, moderated)
│   └── 3.3 Favourites
└── 4.0 Settings & Profile
    ├── 4.1 API Config / Model Toggles
    ├── 4.2 Default Persona
    └── 4.3 Subscription / Credits
```

---

See `docs/system-design.md` for the engineering architecture that implements these surfaces.
