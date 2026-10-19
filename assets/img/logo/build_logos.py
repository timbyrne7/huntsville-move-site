#!/usr/bin/env python3
"""Generate the round "Move to Huntsville" badge.

One geometry source of truth -> five files:
  logo-round.svg              primary, brand blue
  logo-round-light.svg        white ground (print / light UI)
  logo-round-mono-white.svg   one-colour, transparent (over photography)
  logo-round-compact.svg      no text, for avatars
  logo-round-mark.svg         rocket only, for favicons at 16-32px

Run:  python3 assets/img/logo/build_logos.py
"""
from pathlib import Path

OUT = Path(__file__).parent

# ----------------------------------------------------------------- emblem ---
ROCKET = """
    <path d="M256 146 C273 173 281 197 281 216 L281 293 C281 307 277 316 271 322
             L241 322 C235 316 231 307 231 293 L231 216 C231 197 239 173 256 146 Z"
          fill="url(#bodyFill)"/>
    <path d="M256 148 C265 160 271 170 274 181 L238 181 C241 170 247 160 256 148 Z" fill="{accent}"/>
    <circle cx="256" cy="236" r="13.5" fill="{window}" stroke="#ffffff" stroke-width="4.5"/>
    <circle cx="251" cy="232" r="4.5" fill="#ffffff" opacity="0.5"/>
    <path d="M231 274 L207 318 C204 324 206 329 211 328 L231 317 Z" fill="{fin}"/>
    <path d="M281 274 L305 318 C308 324 306 329 301 328 L281 317 Z" fill="{fin}"/>
    <path d="M241 322 C241 348 249 366 256 386 C263 366 271 348 271 322 Z" fill="url(#flameFill)"/>
    <path d="M249 322 C249 342 253 354 256 368 C259 354 263 342 263 322 Z" fill="{core}"/>
"""

ORBIT = """
    <ellipse cx="256" cy="256" rx="150" ry="112" transform="rotate(-16 256 256)" fill="none"
             stroke="{orbit}" stroke-width="2.5" opacity="{orbit_op}"/>
    <path d="M151 404 Q256 380 361 404" fill="none" stroke="{horizon}" stroke-width="3"
          stroke-linecap="round" opacity="0.55"/>
"""

STARS = """
    <g fill="{star}">
      <path d="M150 176 l3.4 8.6 8.6 3.4 -8.6 3.4 -3.4 8.6 -3.4 -8.6 -8.6 -3.4 8.6 -3.4 z"/>
      <path d="M357 166 l2.7 6.8 6.8 2.7 -6.8 2.7 -2.7 6.8 -2.7 -6.8 -6.8 -2.7 6.8 -2.7 z"/>
      <circle cx="133" cy="300" r="2.6"/><circle cx="381" cy="264" r="2.2"/><circle cx="197" cy="142" r="1.9"/>
    </g>
"""

SEPS = """
    <g fill="{accent}">
      <path d="M44 256 l2.8 7 7 2.8 -7 2.8 -2.8 7 -2.8 -7 -7 -2.8 7 -2.8 z"/>
      <path d="M468 256 l2.8 7 7 2.8 -7 2.8 -2.8 7 -2.8 -7 -7 -2.8 7 -2.8 z"/>
    </g>
"""


def badge(*, disc, disc_dark, ink, accent, rim, inner_ring, window, fin, core,
          orbit, orbit_op, horizon, star, text=True, simple=False,
          body=("#ffffff", "#e8f0fa", "#b9cde3"), flame=("#ffd27a", "#f59e0b", "#c2410c"),
          transparent=False, rim_width=3, sheen_on=True):
    canvas = ""
    if text:
        canvas = f"""
  <g font-family="Liberation Sans, Arial, Helvetica, sans-serif" font-weight="700"
     fill="{ink}" text-anchor="middle">
    <text font-size="32" letter-spacing="7">
      <textPath href="#arcTop" startOffset="50%">MOVE TO</textPath>
    </text>
    <text font-size="30" letter-spacing="4.4">
      <textPath href="#arcBottom" startOffset="50%">HUNTSVILLE</textPath>
    </text>
  </g>"""

    sheen = '' if not sheen_on else '<circle cx="256" cy="256" r="256" fill="url(#sheen)"/>'
    ground = "" if transparent else f"""
  <circle cx="256" cy="256" r="256" fill="url(#discFill)"/>
  {sheen}"""

    rings = f"""
  <circle cx="256" cy="256" r="{248 if transparent else 250}" fill="none" stroke="{rim}"
          stroke-width="{6 if transparent else rim_width}" opacity="{1 if transparent else 0.5}"/>"""

    if not simple:
        rings += f"""
  <circle cx="256" cy="256" r="180" fill="none" stroke="{inner_ring}" stroke-width="{4 if transparent else 2}" opacity="{0.9 if transparent else 0.45}"/>"""

    emblem = ""
    if not simple:
        emblem += ORBIT.format(orbit=orbit, orbit_op=orbit_op, horizon=horizon)
        emblem += STARS.format(star=star)
    emblem += ROCKET.format(accent=accent, window=window, fin=fin, core=core)

    scale = (' transform="translate(256 262) scale(1.46) translate(-256 -262)"' if simple
             else ' transform="translate(256 258) scale(1.18) translate(-256 -258)"')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512"
     role="img" aria-label="Move to Huntsville, Alabama">
  <title>Move to Huntsville</title>
  <defs>
    <linearGradient id="discFill" x1="0.1" y1="0" x2="0.62" y2="1">
      <stop offset="0" stop-color="{disc}"/>
      <stop offset="58%" stop-color="{disc_dark}"/>
      <stop offset="100%" stop-color="{disc_dark}" stop-opacity="0.9"/>
    </linearGradient>
    <radialGradient id="sheen" cx="36%" cy="24%" r="74%">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.20"/>
      <stop offset="62%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="bodyFill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{body[0]}"/>
      <stop offset="62%" stop-color="{body[1]}"/>
      <stop offset="100%" stop-color="{body[2]}"/>
    </linearGradient>
    <linearGradient id="flameFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{flame[0]}"/>
      <stop offset="45%" stop-color="{flame[1]}"/>
      <stop offset="100%" stop-color="{flame[2]}" stop-opacity="0.2"/>
    </linearGradient>
    <path id="arcTop" d="M256 256 m -212,0 a 212,212 0 1,1 424,0"/>
    <path id="arcBottom" d="M256 256 m -236,0 a 236,236 0 1,0 472,0"/>
  </defs>
{ground}{rings}{canvas}
  <g transform="translate(0 -6)"><g{scale}>{emblem}
  </g></g>
</svg>
"""


BLUE = dict(disc="#0d63b8", disc_dark="#072f57", ink="#ffffff", accent="#f97316",
            rim="#ffffff", inner_ring="#ffb27a", window="#0b3a6b", fin="#f97316",
            core="#fff3c4", orbit="#ffd9a8", orbit_op="0.26", horizon="#ffffff",
            star="#ffd9a8")

VARIANTS = {
    "logo-round.svg": dict(BLUE, text=True),
    "logo-round-light.svg": dict(disc="#ffffff", disc_dark="#eaf2fa", ink="#0b3a6b",
                                 accent="#c2410c", rim="#0b3a6b", inner_ring="#c2410c",
                                 window="#0b3a6b", fin="#c2410c", core="#ffe9b0",
                                 orbit="#0b5cad", orbit_op="0.32", horizon="#0b3a6b",
                                 star="#c2410c", text=True, rim_width=6, sheen_on=False,
                                 body=("#ffffff", "#dce8f4", "#9fbdd8")),
    "logo-round-mono-white.svg": dict(BLUE, ink="#ffffff", accent="#ffffff", rim="#ffffff",
                                      inner_ring="#ffffff", window="#072f57", fin="#ffffff",
                                      core="#ffffff", orbit="#ffffff", orbit_op="0.6",
                                      horizon="#ffffff", star="#ffffff", text=True,
                                      body=("#ffffff", "#ffffff", "#ffffff"),
                                      flame=("#ffffff", "#ffffff", "#ffffff"),
                                      transparent=True),
    "logo-round-compact.svg": dict(BLUE, text=False),
    "logo-round-mark.svg": dict(BLUE, text=False, simple=True, rim_width=13),
}

if __name__ == "__main__":
    for name, cfg in VARIANTS.items():
        svg = badge(**cfg)
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"wrote {name}  ({len(svg)} bytes)")
