# Design System

Inspired by [harshita-ux-profile.vercel.app](https://harshita-ux-profile.vercel.app) — clean, minimal, typographic.

---

## Colours

| Token | Hex | Usage |
|---|---|---|
| `--navy` | `#1B1A3B` | Primary text, headings, buttons |
| `--navy-dark` | `#2d2c5e` | Button hover state |
| `--purple` | `#7C6FCD` | Accent, links, badges, icons |
| `--purple-deep` | `#7C3AED` | Gradient end, avatar |
| `--white` | `#ffffff` | Background, cards |
| `--surface` | `#F0EDF9` | Hover state on fields, icon backgrounds |
| `--surface-alt` | `rgba(27,26,59,0.03)` | Subtle card backgrounds, disclaimer |
| `--border` | `rgba(27,26,59,0.07–0.15)` | Card borders, input borders |
| `--text-muted` | `rgba(27,26,59,0.5)` | Subtitles, secondary text |
| `--text-faint` | `rgba(27,26,59,0.35–0.4)` | Labels, hints |
| `--error` | `#C2185B` | Error messages |

**Never use blue** (`#2b6cb0`, `#3182ce`). The primary accent is `#7C6FCD` purple.

---

## Typography

- **Font**: `Inter` (Google Fonts, weights 400/500/600/700/800)
- **Antialiasing**: always `-webkit-font-smoothing: antialiased`
- **Headings** (`h1`): 800 weight, `letter-spacing: -0.03em`, fluid size with `clamp()`
- **Section labels**: 600 weight, `uppercase`, `letter-spacing: 0.12–0.15em`, `0.6875rem`
- **Body / values**: 500 weight, `letter-spacing: -0.01em`, `0.9375rem`
- **Hints / captions**: 400 weight, `0.72–0.75rem`, `rgba(27,26,59,0.35)`
- **Monospace** (document numbers): `ui-monospace, 'Courier New', monospace`

---

## Border Radius

| Context | Value |
|---|---|
| Page cards | `1.25rem` |
| Login card | `1.5rem` |
| Buttons (pill) | `9999px` |
| Buttons (rect) | `0.65rem` |
| Fields on hover | `0.75rem` |
| Badges | `9999px` |
| Inputs | `0.65rem` |
| Icon containers | `0.75rem` |

---

## Shadows

- **Card**: `0 1px 3px rgba(27,26,59,0.06), 0 8px 24px rgba(27,26,59,0.08)`
- **Login card**: `0 1px 3px rgba(27,26,59,0.06), 0 20px 60px rgba(27,26,59,0.1)`
- **Tab active**: `0 1px 6px rgba(27,26,59,0.1)`
- **No coloured shadows** (no blue glow)

---

## Buttons

### Primary (dark pill)
```css
background: #1B1A3B;
color: #ffffff;
border-radius: 9999px;
font-weight: 600;
letter-spacing: -0.01em;
/* hover → background: #2d2c5e */
/* active → transform: scale(0.97) */
```

### Secondary (outline pill)
```css
background: transparent;
color: #7C6FCD;
border: 1.5px solid rgba(124,111,205,0.35);
border-radius: 9999px;
/* hover → background: rgba(124,111,205,0.07) */
```

### Rect button (e.g. Download CSV)
```css
background: #1B1A3B;
border-radius: 0.65rem;
/* same hover/active as primary */
```

---

## Cards

```css
background: #ffffff;
border-radius: 1.25rem;
border: 1px solid rgba(27,26,59,0.07);
box-shadow: 0 1px 3px rgba(27,26,59,0.06), 0 8px 24px rgba(27,26,59,0.08);
padding: 2rem;
max-width: 680px;
width: 100%;
```

Subtle surface variant (disclaimer, metadata blocks):
```css
background: rgba(27,26,59,0.03);
border: 1px solid rgba(27,26,59,0.07);
border-radius: 0.75rem;
```

---

## Navigation / Auth Bar

- Height: `64px`, sticky, `z-index: 50`
- Background: `rgba(255,255,255,0.92)` + `backdrop-filter: blur(12px)`
- Bottom border: `1px solid rgba(27,26,59,0.08)`

---

## Tabs

```css
/* Track */
background: rgba(27,26,59,0.05);
border-radius: 9999px;
padding: 0.25rem;

/* Active tab */
background: #ffffff;
border-radius: 9999px;
box-shadow: 0 1px 6px rgba(27,26,59,0.1);
color: #1B1A3B;

/* Inactive tab */
color: rgba(27,26,59,0.5);
```

---

## Inputs

```css
border: 1.5px solid rgba(27,26,59,0.15);
border-radius: 0.65rem;
font-family: Inter, inherit;
color: #1B1A3B;
background: #ffffff;
/* focus → border-color: #7C6FCD */
```

---

## Spacing Scale

Follow 0.25rem (4px) increments. Common values:
- `0.5rem` gap between small elements
- `1rem` internal padding for small components
- `1.5–2rem` card padding
- `2.5–3rem` section spacing
- `5rem` page bottom padding

---

## Transitions

- Default: `transition: <prop> 0.2s` with `cubic-bezier(0.4, 0, 0.2, 1)`
- Fast (hover fills): `0.15s`
- Never use bounce or spring for UI chrome

---

## Do / Don't

| Do | Don't |
|---|---|
| Use `#1B1A3B` for all primary actions | Use blue (`#3182ce`, `#2b6cb0`) |
| Use `#7C6FCD` for accents and highlights | Use green for success states |
| Inter font, tight headings | Mix multiple fonts |
| Pill buttons for primary CTAs | Square corners on buttons |
| Subtle borders on cards (`rgba` opacity) | Heavy `1px solid #e2e8f0` everywhere |
| Soft navy shadows | Bright coloured glow shadows |
| Uppercase + wide tracking for section labels | Uppercase body text |

---

## Adding a New Page or Section

1. Add your section inside the `.page` container in `app.html`
2. Wrap content in a `.card` div
3. Use `.section-title` for group headers within a card
4. Use `.field-grid` + `.field` for data display rows
5. Add new CSS classes to `app.css` following the tokens above
6. Test on mobile — `field-grid` should collapse to 1 column at `≤500px`
