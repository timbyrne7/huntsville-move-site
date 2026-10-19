# Logo — "Move to Huntsville"

Two marks, each generated from a single geometry file so nothing drifts out of alignment.

```bash
python3 assets/img/logo/build_logos.py        # the round badge (5 SVGs)
python3 assets/img/logo/build_horizontal.py   # the horizontal lockup (3 SVGs)
```

Preview both, on light and dark, at every size: `logo-preview.html` in the project root.

---

## 1. Horizontal lockup — skyline left, wordmark right

Canvas 1040 × 280 (3.71:1). The city scene occupies x 24–300, the wordmark starts at x=344, and
both sit on a shared baseline at y=248 — the skyline grounds the type instead of floating beside it.

The scene is Huntsville-specific, not a generic skyline: Monte Sano ridge behind, a Saturn V in
front of it (the one silhouette the city is known by), then low-rise blocks with lit windows and a
burnt-orange band on the tallest.

| File | Use |
| --- | --- |
| `logo-horizontal.svg` | Primary on light backgrounds: navy wordmark, navy rocket, orange accents |
| `logo-horizontal-reverse.svg` | Dark backgrounds: white wordmark, lifted skyline, white rocket |
| `logo-horizontal-mono.svg` | Single colour: stamps, faxes, one-colour print, engraving |
| `png/logo-horizontal*-{1400,1040,700,520,400,300,220}.png` | RGBA exports, height = width × 0.269 |

Type: "MOVE TO" 26px, 700, 9 tracking, `#c2410c` (light) / `#ffd9a8` (reverse); "HUNTSVILLE"
94px, 700, −2 tracking, `#0b3a6b` / `#ffffff`. Minimum width on screen: 220px (below that the
skyline compresses into noise — use the round badge instead).

---

## 2. Round badge

512 × 512 canvas. Disc r=256 · rim r=250 · text ring 210–236 · inner rule r=180 · emblem inside
r=180. Text is set on two circular paths: "MOVE TO" at r=212 (32px, 7 tracking) and "HUNTSVILLE"
at r=236 (30px, 4.4 tracking), both centred on a 50% offset.

| File | Use |
| --- | --- |
| `logo-round.svg` | Primary. Brand-blue disc, white type, orange flame |
| `logo-round-light.svg` | White ground: print, invoices, light UI |
| `logo-round-mono-white.svg` | One colour, transparent ground: over photography |
| `logo-round-compact.svg` | Text removed, full emblem: social avatars, app icon (≥48px) |
| `logo-round-mark.svg` | Rocket only, enlarged and thickened: favicons 16–32px |
| `favicon.ico` | 16/32/48 multi-resolution icon |
| `png/logo-round*.png` | 1024, 512, 256, 128, 64, 48, 32, 16 — all RGBA with transparent corners |

---

## Palette

| Hex | Role |
| --- | --- |
| `#0b3a6b` | Wordmark navy / skyline near-blocks |
| `#0f3d6e` · `#1b4f8a` | Skyline mid-blocks |
| `#dbe9f8` | Monte Sano ridge, window glazing |
| `#0d63b8` → `#072f57` | Badge disc gradient (the site's `--brand` family) |
| `#f97316` | Skyline and badge accent: rocket bands, lit sign |
| `#c2410c` | "MOVE TO" on light ground (the site's `--accent`) |
| `#ffd9a8` / `#fff3c4` | Reverse-mode sub-type, orbit, flame core |

## Production notes

- **Text is live type, not outlines.** Both generators use `<text>` / `<textPath>`, so they need
  Liberation Sans / Arial / Helvetica at render time — fine for web and for the PNGs here. Before
  a print run, signage or a trademark filing, convert the type to paths (Illustrator: Type →
  Create Outlines) so the letterforms cannot substitute.
- **Minimum sizes.** Horizontal lockup: 220px wide on screen, 45mm in print. Round badge: 48px /
  20mm; below that use `logo-round-compact.svg`, then `logo-round-mark.svg` under 48px.
- **Clear space.** Horizontal: at least the height of the "M" on every side. Round: 12% of the
  diameter. The rim is part of the mark, not padding.
- **Backgrounds.** Never place the light-background lockup on a mid-tone photograph — use the
  reverse version on anything darker than 40% grey, or the mono version on busy imagery.
