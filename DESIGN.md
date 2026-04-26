# Design System

**Mark2PDF — Obsidian Terminal**

A high-contrast, technical-editorial dark UI inspired by [Mermaid Studio](https://github.com/mermaid-js/mermaid). Built around tonal surface shifts, kinetic accents, and zero-noise chrome.

---

## Principles

1. **No grey shadows** — depth via tonal background shifts, not drop-shadows
2. **No border lines for separation** — use ghost borders (15% opacity green) sparingly
3. **Monospace for technical text** — code, version tags, status indicators
4. **Display sans for headings/UI labels** — uppercase, wide letter-spacing
5. **Body sans for prose** — Manrope for legibility at 15px+
6. **Glow over shadow** — accent colors emit, never darken

---

## Color Tokens

### Surfaces — tonal ladder

```css
--surface-lowest:  #0e0e0e   /* toolbar, pane-bar, code blocks */
--surface:         #131313   /* body */
--surface-low:     #191919   /* editor pane */
--surface-mid:     #1f1f1f   /* (reserved) */
--surface-high:    #2a2a2a   /* select, danger button, scrollbar thumb */
--surface-highest: #3a3a3a   /* button hover */
```

### Kinetic accents

```css
--primary:      #A6FF00   /* Matrix Green — primary action, headings */
--primary-dark: #467000   /* gradient endpoint, scrollbar hover */
--primary-dim:  #8ad800
--secondary:    #00E0FF   /* Electric Blue — links, inline code */
--caution:      #FF8A00   /* Caution Orange — destructive hover */
```

### Text

```css
--on-surface:        #e2e2e2   /* primary body */
--on-surface-muted:  #8a8a8a   /* labels, dimmed prose */
--on-surface-faint:  #555555   /* captions, dividers, version tags */
--on-primary:        #0a1000   /* text on green button */
```

### Ghost borders

```css
--ghost:        rgba(65, 74, 52, 0.15)   /* default — pane separator */
--ghost-strong: rgba(65, 74, 52, 0.35)   /* select border */
```

Tinted green instead of neutral grey — keeps the system cohesive.

### Glow

```css
--glow-primary: 0 0 12px rgba(166, 255, 0, 0.30)
--glow-caution: 0 0 12px rgba(255, 138, 0, 0.30)
```

Used on logo, accent button hover, danger button hover. Never on text.

---

## Typography

```css
--font-display: 'Space Grotesk'    /* UI labels, headings, buttons */
--font-body:    'Manrope'          /* preview prose */
--font-mono:    'JetBrains Mono'   /* editor, code, status, version */
```

### Scale & tracking

| Use | Size | Weight | Tracking | Transform |
|-----|------|--------|----------|-----------|
| Toolbar title | 14px | 700 | 1.5px | UPPERCASE |
| Toolbar subtitle | 10px | 500 | 0.5px | none (mono) |
| Pane label | 10px | 600 | 2.5px | UPPERCASE |
| Pulse label | 10px | 600 | 1.5px | UPPERCASE (mono) |
| Button | 11.5px | 600 | 1.2px | UPPERCASE |
| Editor | 13px | 400 | — | none (mono) |
| Body prose | 15px | 400 | — | none |

Wide tracking on UI labels signals "system chrome." Body prose stays untracked for readability.

---

## Geometry

```css
--radius-xs: 0.125rem   /* 2px — buttons, logo, scrollbar */
--radius-sm: 0.25rem    /* 4px — code blocks */
--radius-md: 0.375rem   /* 6px — max */
```

Hard, technical look. Nothing rounder than 6px.

```css
--transition: 160ms cubic-bezier(0.2, 0, 0, 1)
```

Snappy, ease-out. Used on every interactive element.

---

## Components

### Toolbar (48px)

Brand left, actions right. `surface-lowest` background, no border.

```
[M] MARK2PDF  STUDIO // v1.0          [select] [PDF] [delete]
```

- `M` logo: 30px square, primary→primary-dark gradient, glow shadow
- Title: display font, uppercase, wide tracking
- Subtitle: mono, faint color, no transform

### Pane Bar (36px)

Three label groups. `surface-lowest`, hairline ghost borders top + bottom.

```
EDITOR              ● LIVE  VORSCHAU              SCROLL SYNC
```

- Live dot: 4px primary core, 14px animated pulse ring (1.6s loop)
- All labels uppercase except mono `LIVE` indicator

### Buttons

**Accent (primary action):**
- Gradient `primary → primary-dark`
- `on-primary` text (near-black green-tint)
- Glow on hover
- `scale(0.97)` on active

**Ghost (secondary/destructive):**
- `surface-high` background
- `on-surface-muted` text
- Hover: `surface-highest` + caution color (destructive only)
- Same scale-down on active

### Select

Looks like a ghost button. Border `ghost-strong`, hover lifts surface tone.

### Scrollbars

8px wide, square (`border-radius: 0`), `surface-high` thumb, `primary-dark` on hover. Track transparent. Custom only for `-webkit-` (Firefox uses native dimmed).

### Pulse Indicator

Two-layer:
- Inner dot: 4px, primary, 6px primary glow
- Outer ring: animated `scale(0.3 → 1)` with `opacity(0.5 → 0)` over 1.6s

---

## Theme System (Preview)

The preview pane carries a separate themeable layer for rendered Markdown. Three themes ship:

| Theme | Use | Headings | Code BG |
|-------|-----|----------|---------|
| `theme-light` (Obsidian) | default | primary green | tinted green |
| `theme-dark` (Monochrom) | minimal | white | white 6% |
| `theme-github` | familiarity | black, border-bottom | `#f6f8fa` |

Theme = single class on `#html-preview`. CSS scoped to `.theme-X` selectors.

---

## PDF Output

PDF rendering uses a **separate inline `<style>` block** in `app.py`. Light, print-optimized:
- A4, 2cm margins
- System sans serif body
- `page-break-after: avoid` on headings
- `break-inside: avoid` on tables and code blocks (planned)

The PDF is intentionally NOT styled like the dark UI — print needs different ink economy.

---

## Anti-Patterns

Avoid:
- Drop shadows (use glow or tonal shifts)
- Border lines for separation (use background contrast or ghost borders)
- Border radius > 6px (breaks technical aesthetic)
- Tracking on body prose (kills readability)
- Lowercase UI labels (breaks system chrome)
- Neutral grey accents (clashes with green-tinted ghosts)

---

## File Map

| File | Concern |
|------|---------|
| `static/style.css` | Live preview + UI chrome |
| `app.py` (inline `<style>`) | PDF output styling |
| `templates/index.html` | DOM structure, font loading |

Markdown extension parity (preview vs PDF) requires updating both `marked.js` config and `markdown.markdown(extensions=[...])`.
