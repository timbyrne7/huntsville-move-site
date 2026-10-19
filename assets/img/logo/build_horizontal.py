#!/usr/bin/env python3
"""Horizontal "Move to Huntsville" lockup: city scene left, stacked wordmark right.

Artwork canvas: viewBox 14 94 910 180 (5.06:1), cropped to the measured drawing
bounds so the mark carries no dead margin when placed inline in a header.
The scene is compressed into the same optical band as the
wordmark (y 108-252) and both sit on a shared baseline at y=248, so the skyline
grounds the type instead of floating next to it.

Run:  python3 assets/img/logo/build_horizontal.py
"""
from pathlib import Path

OUT = Path(__file__).parent
G = 248.0  # ground line and text baseline


def scene(*, ridge, mid, near, dark, rocket, band, window, accent):
    return f"""
    <!-- Monte Sano ridge, low behind everything -->
    <path d="M24 {G} L24 206 C46 196 62 182 84 186 C104 190 112 176 132 178
             C156 180 166 170 188 176 C210 182 222 172 242 178 C264 184 280 190 300 186
             L300 {G} Z" fill="{ridge}"/>
    <!-- Saturn V: the silhouette that says Huntsville -->
    <g>
      <path d="M38 240 L38 136 L62 136 L62 240 Z" fill="{rocket}"/>
      <path d="M38 136 L50 104 L62 136 Z" fill="{rocket}"/>
      <rect x="38" y="140" width="24" height="7" fill="{accent}"/>
      <rect x="38" y="168" width="24" height="8" fill="{band}"/>
      <rect x="38" y="196" width="24" height="8" fill="{band}"/>
      <path d="M38 224 L28 240 L38 240 Z" fill="{rocket}"/>
      <path d="M62 224 L72 240 L62 240 Z" fill="{rocket}"/>
      <rect x="36" y="238" width="28" height="10" fill="{rocket}"/>
    </g>
    <!-- blocks, front of the rocket -->
    <rect x="88" y="176" width="40" height="{G-176}" fill="{mid}"/>
    <rect x="100" y="166" width="16" height="10" fill="{mid}"/>
    <rect x="130" y="152" width="34" height="{G-152}" fill="{near}"/>
    <rect x="138" y="142" width="18" height="10" fill="{near}"/>
    <rect x="174" y="186" width="44" height="{G-186}" fill="{mid}"/>
    <rect x="228" y="164" width="44" height="{G-164}" fill="{near}"/>
    <rect x="238" y="154" width="24" height="10" fill="{near}"/>
    <rect x="282" y="196" width="18" height="{G-196}" fill="{mid}"/>
    <!-- windows -->
    <g fill="{window}">
      <rect x="96" y="186" width="6" height="9"/><rect x="108" y="186" width="6" height="9"/>
      <rect x="120" y="186" width="6" height="9"/><rect x="96" y="203" width="6" height="9"/>
      <rect x="108" y="203" width="6" height="9"/><rect x="120" y="203" width="6" height="9"/>
      <rect x="137" y="162" width="6" height="9"/><rect x="150" y="162" width="6" height="9"/>
      <rect x="137" y="179" width="6" height="9"/><rect x="150" y="179" width="6" height="9"/>
      <rect x="137" y="196" width="6" height="9"/><rect x="150" y="196" width="6" height="9"/>
      <rect x="236" y="174" width="6" height="9"/><rect x="250" y="174" width="6" height="9"/>
      <rect x="264" y="174" width="6" height="9"/><rect x="236" y="191" width="6" height="9"/>
      <rect x="250" y="191" width="6" height="9"/><rect x="264" y="191" width="6" height="9"/>
      <rect x="236" y="208" width="6" height="9"/><rect x="250" y="208" width="6" height="9"/>
      <rect x="264" y="208" width="6" height="9"/>
    </g>
    <rect x="228" y="234" width="44" height="4" fill="{accent}"/>
    <!-- ground -->
    <rect x="24" y="{G}" width="276" height="4.5" fill="{dark}"/>
"""


def lockup(*, ink, sub, scene_colors):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="14 94 910 180" width="910" height="180"
     role="img" aria-label="Move to Huntsville — city skyline with wordmark">
  <title>Move to Huntsville</title>
{scene(**scene_colors)}
  <g font-family="Liberation Sans, Arial, Helvetica, sans-serif">
    <text x="348" y="152" font-size="26" font-weight="700" letter-spacing="9"
          fill="{sub}">MOVE TO</text>
    <text x="344" y="248" font-size="94" font-weight="700" letter-spacing="-2"
          fill="{ink}">HUNTSVILLE</text>
  </g>
</svg>
"""


NAVY, DEEP, BLUE, ORANGE, RUST = "#0b3a6b", "#0f3d6e", "#1b4f8a", "#f97316", "#c2410c"

VARIANTS = {
    # light backgrounds: navy type, coloured skyline, navy rocket
    "logo-horizontal.svg": dict(
        ink=NAVY, sub=RUST,
        scene_colors=dict(ridge="#dbe9f8", mid=BLUE, near=DEEP, dark=NAVY,
                          rocket=NAVY, band="#ffffff", window="#a8c9e8", accent=ORANGE)),
    # dark backgrounds: white type, lifted skyline, white rocket
    "logo-horizontal-reverse.svg": dict(
        ink="#ffffff", sub="#ffd9a8",
        scene_colors=dict(ridge="#123f6b", mid="#7aa6cf", near="#a8c6e4", dark="#dbe9f8",
                          rocket="#ffffff", band="#0b3a6b", window="#0b3a6b", accent=ORANGE)),
    # single colour
    "logo-horizontal-mono.svg": dict(
        ink="#000000", sub="#000000",
        scene_colors=dict(ridge="#dcdcdc", mid="#000000", near="#000000", dark="#000000",
                          rocket="#000000", band="#ffffff", window="#ffffff", accent="#000000")),
}

if __name__ == "__main__":
    for name, cfg in VARIANTS.items():
        svg = lockup(**cfg)
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"wrote {name}  ({len(svg)} bytes)")
