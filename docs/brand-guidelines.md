# Got Messy — Brand Guidelines

Operational rules for applying the **Got Messy** identity. This document **extends** the canonical *Brand Identity Kit* (`Final/gotmessy-brand-kit-final.html`) — it does not duplicate it. The kit covers the *what* (logos, palette, typography, voice). This document covers the *how, when, and where not* — the day-to-day decisions a designer, marketer, or engineer has to make.

If anything here contradicts the kit, the kit wins. Update both together.

---

## 1. Wordmark and logo usage

### Wordmark anatomy

The wordmark is a single typographic lockup, not three separate elements:

```text
got Messy.
└─┬─┘ └─┬─┘ └┬┘
  │     │    └─ Clay terminal dot — never any other colour
  │     └────── Bold Lora 700 — always "Messy"
  └──────────── Italic Lora 400 — always lowercase "got"
```

**Never** rebuild the wordmark in Poppins, sans-serif, or all-caps. The dot is a load-bearing brand element — it carries the "permission to be imperfect" idea. Do not omit, recolour, or animate it independently of the wordmark.

### Clear space

Reserve a clear space around the wordmark equal to the **cap-height of "M"** in *Messy*. No other text, image, edge, or chrome may enter this zone.

### Minimum sizes

| Surface | Minimum height of "M" in *Messy* |
|---|---|
| Print | 14 pt |
| Screen — desktop | 18 px |
| Screen — mobile | 16 px |
| Favicon / app icon | use the icon mark (`gotmessy-icon.svg`), not the wordmark |

Below these sizes, switch to the icon mark. Don't compress, condense, or letter-space the wordmark to make it fit.

### Logo selection

| Variant | When to use |
|---|---|
| **Logo A** *(lead)* | Default everywhere — site headers, app splash, marketing, PDFs. |
| Logo B | Use only when Logo A's proportions don't fit (narrow stacks, square crops). Document the decision; A should be the answer 90% of the time. |
| Logo C | Reserved for the contexts indicated in the brand kit. Don't repurpose. |
| `-transparent` | Overlay on photography or coloured fields. Re-test contrast every time. |
| `gotmessy-app-icon` | App stores, OS launchers, taskbar pins. Never inline in body copy. |

### What you must not do

- Don't recolour the wordmark. The dot is `--clay`; the lockup is `--cream` on dark or `--ink` on light. No exceptions.
- Don't add drop-shadows, glows, gradients, bevels, or outlines.
- Don't place the wordmark over busy photography without the transparent variant + a contrast scrim.
- Don't rotate, skew, or arc the wordmark.
- Don't pair the wordmark with a separate icon lockup — pick one.
- Don't animate "Got" and "Messy" as if they were words being typed. They're a single mark.

---

## 2. Colour usage

The full palette lives in `Final/gotmessy-color-sheet-final.png` and the `:root` block of every HTML deliverable. Treat the rules below as the *application* layer.

### Role hierarchy

| Role | Token(s) | Notes |
|---|---|---|
| Page background (default — dark) | `--ink` | Almost everything ships dark. Default surface. |
| Card / elevated surface | `--card` over `--ink`, border `--card-bd` | Use sparingly — flat is the norm, cards for groupings only. |
| Body text on dark | `--cream` | Never pure white (`#FFF`). |
| Muted text / labels / metadata | `--dust` | Use for everything secondary; do not pile up four shades of grey. |
| Primary action / link | `--clay` (rest), `--clay-dk` (hover/pressed), `--clay-lt` (focus ring or large hero accents) | One clay action per view ideally. |
| Success / live status | `--sage` | Reserved for *positive* state, not generic confirmation chrome. |
| Highlight / annotation | `--yellow` | Use like a marker — sparingly, on emphasis only. |
| Secondary accents | `--lav`, `--sky` | For categorisation (tags, model identifiers, secondary chips). Don't use as link colour. |

### Accent budget per view

A single screen should contain **at most three of the accents** (`--clay`, `--sage`, `--lav`, `--sky`, `--yellow`). When you find yourself using all five, you're probably substituting decoration for hierarchy — collapse back to clay + dust and re-introduce one accent only where it earns its place.

### Light surfaces

Light mode is permitted but secondary. Use `--warm` (`#F2EDE4`) as the page background and `--ink` for body text. **Pure white (`#FFFFFF`) is forbidden** as a background — the brand kit calls this out and it's load-bearing. The cream tints carry the warmth that distinguishes Got Messy from clinical, hyper-saturated AI tools.

### Forbidden colours

- Pure white backgrounds.
- Electric blues, teals, cyans (`#00BFFF`-ish) — tech-brand cliché.
- High-saturation neons (e.g. `#39FF14`, `#FF00FF`).
- Any pure black (`#000`) — use `--ink` (`#1A1612`).

---

## 3. Accessibility

Accessibility is brand. A messy-friendly product that's hostile to readers is off-brand by definition.

### Contrast targets

All text must meet **WCAG 2.2 AA** at minimum, AAA for body copy where achievable.

| Pair | Ratio | Verdict |
|---|---|---|
| `--cream` on `--ink` | ~14.7:1 | AAA — default body |
| `--dust` on `--ink` | ~6.3:1 | AA — fine for labels and metadata; avoid for long-form body |
| `--clay` on `--ink` | ~4.6:1 | AA for large text and UI components only — **do not** use clay for body paragraphs |
| `--clay-lt` on `--ink` | ~6.9:1 | AA — preferred for interactive accents on dark |
| `--ink` on `--warm` | ~13.5:1 | AAA — light-mode default |

Re-validate every time the palette is touched. The repo's color sheet is the source — if you adjust a hex, regenerate the contrast table here.

### Other a11y requirements

- **Focus state** — visible outline on every interactive element. Use `outline: 2px solid var(--clay-lt); outline-offset: 2px;`. Never `outline: none` without an alternative indicator.
- **Touch targets** — 44×44 px minimum on mobile (Got Messy is mobile-first per the architecture infographic).
- **Motion** — honour `prefers-reduced-motion: reduce`. The blinking `--sage` "live" dot in the hub sidebar must freeze at 100% opacity in reduced-motion mode.
- **Forms** — never rely on placeholder text as a label.
- **Alt text** — every logo/icon image must have meaningful alt; decorative chrome must be `alt=""` or `aria-hidden="true"`.

---

## 4. Typography in practice

The kit defines the families (Lora serif, Poppins sans). The rules below cover *application*.

### Type scale (rem-based, 16px root)

| Level | Family / weight / style | Size | Use |
|---|---|---|---|
| Display | Lora 700, italic on accent words | clamp(3rem, 7vw, 5.5rem) | Hero only — once per page |
| H1 | Lora 700 | 2.25rem | Page title |
| H2 | Lora 700 | 1.5rem | Section heading |
| H3 | Lora 600 | 1.15rem | Sub-section |
| Eyebrow / kicker | Poppins 600, uppercase, letter-spacing 0.06em | 0.72rem | Above H1 / section labels |
| Body | Poppins 300–400 | 0.875–1rem (14–16px) | Default copy |
| Caption / meta | Poppins 300 | 0.75rem | Timestamps, attribution, helper text |
| Wordmark *(special case)* | Lora 400 italic + Lora 700 | as required | See §1 |

### Italics

Italic Lora is the *brand inflection* — use it for:

- The word "Got" in the wordmark.
- One emphasised noun per heading where it lifts the line ("You already know what *great output looks like.*").
- Pull quotes.

Don't italicise long passages of body copy. Italic is seasoning, not the dish.

### Numerals

Use **tabular-nums** (`font-variant-numeric: tabular-nums`) anywhere numbers stack — pricing, dashboards, the Hub stats grid. Otherwise use the default proportional figures.

### Line lengths

Body copy: 60–75 characters per line. Don't let containers stretch wider on desktop without an inner `max-width` of ~620px for prose blocks.

---

## 5. Voice and tone

The kit states the personality in a single line: *"a brilliant friend who happens to be great with words. Not a tutor. Not a robot. Not a hustle-culture coach."* The rules below operationalise that.

### Always / never

<!-- brand-lint-allow: table rows below quote forbidden vocabulary as cautionary "Never" examples -->
| Always | Never |
|---|---|
| "You already know what good looks like." | <!-- brand-lint-allow -->"Unleash your AI superpowers!" |
| "Drop your mess in." | <!-- brand-lint-allow -->"Begin your prompt-engineering journey." |
| "We'll sort the structure." | "Let our advanced NLP pipeline analyse..." |
| "Save it. Re-use it tomorrow." | <!-- brand-lint-allow -->"Empower your workflow at scale." |
| Plain present tense, second person | <!-- brand-lint-allow -->Future tense, marketing-deck future-perfect ("you will have unlocked") |
| Contractions ("you're", "we'll") | Stiff full forms in UI copy |
| Acknowledge the mess as normal | Apologise for the mess or imply the user "needs help" |

### Do not use

These words are *off-brand* in product UI and marketing copy:
<!-- brand-lint-allow: bullet list below enumerates the forbidden vocabulary itself -->
- *journey*, *unlock*, *unleash*, *supercharge*, *next-level*, *game-changer* <!-- brand-lint-allow -->
- *empower*, *enable* (when used as marketing filler) <!-- brand-lint-allow -->
- *AI-powered* (we know — say what it does) <!-- brand-lint-allow -->
- *cutting-edge*, *state-of-the-art* <!-- brand-lint-allow -->
- *leverage* (as a verb) <!-- brand-lint-allow -->
- *learning curve* — the brand explicitly rejects this framing <!-- brand-lint-allow -->

### Tone by surface

| Surface | Tone | Example |
|---|---|---|
| Onboarding | Warm, concrete, confident | "First thing — drop something messy in. Anything. We'll show you what to do with it." |
| Empty states | Acknowledge + invite | "No saved prompts yet. Make one — Mirror It can copy a style you already like." |
| Error states | Plain, no blame | "That didn't paste cleanly. Try the URL or the text directly." (Not: *"Oops! Something went wrong!"*) |
| Success states | Quiet, not exclamatory | "Saved." (Not: *"Awesome! 🎉 You did it!"*) |
| Long-form (blog, kit) | A little more lyrical, italic Lora pull quotes welcome | See the brand kit hero copy. |

### Punctuation

- **Em dashes** — yes, use them. The brand kit and infographic use them throughout.
- **Exclamation marks** — almost never. One per page maximum, and only when the user just shipped something.
- **Emoji** — sparing and flat. The kit uses them as section markers (🪞, 🧬, ✦). Don't decorate body copy with strings of emoji.

---

## 6. Iconography

- Style: **outlined, 1.5px stroke, rounded joins, 24×24 grid** for UI. Match the line weight of Poppins 500.
- Source set: pick one library (recommend Lucide or Phosphor outline) and stick to it. Don't mix stroke icons with filled icons in the same view.
- Brand icon (`gotmessy-icon.svg`) is reserved for app identity surfaces — never reuse it as a generic symbol inside the product.
- Section markers in the brand kit (🪞, 🧬, ✦, 🪄) are *editorial decoration*, not iconography. Don't import them into UI components.

---

## 7. Imagery and texture

- **No tech stock photography.** No glowing circuit boards, no robot hands, no neural-network meshes. The brand explicitly opposes these tropes.
- Photography (when used) should feel domestic and warm — desks, notebooks, hands writing, coffee — colour-graded to sit alongside `--warm` and `--ink`. Avoid high-contrast b&w.
- Texture: subtle paper/grain overlays at 3–6% opacity are on-brand. Heavy noise, halftone, or glitch effects are off-brand.
- Illustrations: hand-drawn, off-rule, slightly imperfect. The kit's "Permission to be imperfect" line applies here too.

---

## 8. Motion

- **Default duration**: 160ms (`transition: all .16s` is the value already in use across the HTML deliverables — keep it).
- **Easing**: `cubic-bezier(0.4, 0, 0.2, 1)` (Material standard) for most UI; `cubic-bezier(0.16, 1, 0.3, 1)` for hero/page-level reveals.
- The `--sage` "live" status dot blinks at 2s — that's the canonical brand pulse. Don't invent a second pulse rate.
- Page transitions: avoid horizontal slides. Use 8px Y-axis fades. Mess is unpredictable; navigation shouldn't be.
- Honour `prefers-reduced-motion`. See §3.

---

## 9. Domain and naming

- **`gotmessy.com`** is the only consumer-facing domain. Marketing, product, docs all live under it.
- **`cloudcomb.com`** is held for the enterprise/team edition. Do not link to it from gotmessy.com until the team product launches; do not borrow Cloud Comb tone for Got Messy or vice versa. The contrast is the point.
- Product feature names use **Title Case** ("The Architect", "The Drop", "Mirror It", "My Good Stuff", "User DNA", "The Vault"). Internal codenames (e.g. `MirrorMind`, `Intent2Flow`) are fine in technical docs but should not surface in UI.

---

## 10. Asset versioning

Per `CLAUDE.md`, assets live in two parallel sets: working copies and `-final` variants. The `-final` files are canonical.

When you ship a new asset:

1. Drop the working file (no suffix) into `Final/`.
2. Once approved, copy it to its `-final` counterpart and update the matching PDF where one exists.
3. Re-run any contrast/legibility checks if a token changed.
4. If the asset replaces an existing canonical file, capture *why* in the commit message — terse history is no longer acceptable for design changes (see CLAUDE.md workflow conventions).

---

## 11. Open questions / TBD

These are explicitly unresolved — flag them when they come up rather than inventing an answer:

- Dark/light theme switching policy in the product (current default is dark only).
- Localisation rules for the wordmark — is "Got Messy" translated, transliterated, or held in English?
- Email/transactional template design system.
- Cloud Comb's relationship to Got Messy in shared sign-in / billing surfaces.

When any of these resolve, update this file in the same commit as the implementation.
