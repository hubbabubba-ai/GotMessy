# App — UI Kit

High-fidelity, **clickable** mock of the Got Messy app — the six-tool product
surface. Light theme (cream page, white cards, ink text), built on
`colors_and_type.css` tokens.

> Open `index.html` directly in a browser. Click any tool in the left rail
> to switch. Deep-links work too: `index.html#mirror`, `#sort`, `#make`, etc.

## What's inside

Single self-contained file, structured around:

| Block | What it is |
|---|---|
| **Sidebar** | Wordmark + tool rail (with hue dot + stage badge) + Library + Help/Settings. |
| **Topbar** | Active-tool crumb (with hue swatch), Search (⌘K), avatar. |
| **Content** | A scrollable panel per tool, shown/hidden by the rail. |

Six tool panels in one file:

| Panel | Hue | Slug | The story it tells |
|---|---|---|---|
| **The Drop** | Clay 🟧 | `#drop` (default) | Big paste zone → auto-detected Persona/Task/Format/Context → clean prompt + copy actions. |
| **Mirror It** | Lavender 🟪 | `#mirror` | Paste an output you loved → detected structure → "the prompt that made it" + Save as template. |
| **Sort It Out** | Sage 🟩 | `#sort` | Drop a pile of tasks → grouped weekly plan with numbered steps → Send to Make It. |
| **Make It** | Sky 🟦 | `#make` | Form: Persona / Task / Tone chips / Creative↔Precise slider / Format → live prompt preview. |
| **Just Tell Me** | Yellow 🟨 | `#just` | Plain-language goal → "We chose [tool]" badge → finished prompt. |
| **My Good Stuff** | Dust 🟫 | `#library` | Filter chips + grid of saved prompt cards from all five tools, tagged by life area. |

## How the tool switching works

Each panel is a `<div class="panel" data-panel="...">`. The rail buttons
have matching `data-tool="..."` attributes. The script at the bottom:

1. Toggles `.active` on the right rail link + right panel.
2. Updates the topbar crumb text + the hue swatch dot.
3. Writes the slug into the URL hash so links are shareable.

To add a 7th tool: copy a panel, add a rail button with matching `data-tool`,
and add an entry to the `TOOLS` object in the script.

## File dependencies

```text
packages/ui-kit/
├── colors_and_type.css       ← token foundation (fonts, colors, radii, shadows, motion)
├── assets/
│   └── gotmessy-icon.svg     ← brand iconmark (favicon)
└── app/
    └── index.html            ← this file
```

## Testing this

Because everything is in one HTML file with vanilla JS, you can:

- Open it in any browser (Mac: double-click; or serve locally with `python3 -m http.server`).
- Share a link to a specific tool: `index.html#mirror`.
