#!/usr/bin/env python3
"""Build assets/og.png — the 1200x630 social/OG card, from site assets.

Run:  python3 tools/make_og.py    (needs Pillow: uv pip install Pillow)

Uses the real photo set and the reverse (light-on-dark) logo lockup, so the card
matches the site. Regenerate whenever the photos or brand change.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "og.png")
PHOTO = os.path.join(ROOT, "assets", "img", "downtown-skyline.jpg")
LOGO = os.path.join(ROOT, "assets", "img", "logo", "png", "logo-horizontal-reverse-700.png")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1200, 630
INK = (12, 20, 30)
BRAND = (11, 92, 173)
ACCENT = (249, 178, 92)

HEADLINE = "Moving to Huntsville?"
SUBHEAD = "Schools, commute times, cost of living — on real data."
DOMAIN = "movetohuntsville.net"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    if not os.path.exists(path):
        sys.exit(f"make_og: missing font {path}")
    return ImageFont.truetype(path, size)


def cover(path, size):
    """Center-crop the photo to fill `size` without distortion."""
    img = Image.open(path).convert("RGB")
    tw, th = size
    scale = max(tw / img.width, th / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left = (img.width - tw) // 2
    top = (img.height - th) // 3          # bias toward the skyline, not the asphalt
    return img.crop((left, top, left + tw, top + th))


def scrim(size):
    """Navy wash, heavier on the left so the headline always has contrast."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    tw, th = size
    for x in range(tw):
        t = x / (tw - 1)
        alpha = int(212 - 92 * t)          # 212 -> 120 across the width
        draw.line([(x, 0), (x, th)], fill=INK + (alpha,))
    return layer


def bottom_band(size):
    """Extra darkening across the footer row, where the logo and domain sit.

    Composited as its own layer so it multiplies with the column wash instead of
    replacing it (a single layer would leave the corners lighter than the column
    alpha alone).
    """
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    tw, th = size
    for y in range(int(th * 0.66), th):
        t = max(0.0, (y - th * 0.66) / (th * 0.34))
        draw.line([(0, y), (tw, y)], fill=INK + (int(196 * t ** 0.7),))
    return layer


def main():
    for path in (PHOTO, LOGO):
        if not os.path.exists(path):
            sys.exit(f"make_og: missing {path}")

    card = cover(PHOTO, (W, H)).convert("RGBA")
    card.alpha_composite(scrim((W, H)))
    card.alpha_composite(bottom_band((W, H)))

    # Faint brand rule down the left edge.
    ImageDraw.Draw(card).rectangle([0, 0, 10, H], fill=BRAND + (255,))

    draw = ImageDraw.Draw(card)
    f_kick = font("DejaVuSans-Bold.ttf", 24)
    f_head = font("DejaVuSans-Bold.ttf", 82)
    f_sub = font("DejaVuSans.ttf", 32)
    f_dom = font("DejaVuSans-Bold.ttf", 26)

    pad = 76
    kicker = "MOVE TO HUNTSVILLE"
    draw.text((pad, 108), spaced(kicker), font=f_kick, fill=ACCENT)
    draw.text((pad, 158), HEADLINE, font=f_head, fill=(255, 255, 255))
    draw.text((pad, 268), SUBHEAD, font=f_sub, fill=(226, 236, 246))

    logo = Image.open(LOGO).convert("RGBA")
    lw = 300
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    card.alpha_composite(logo, (pad, H - 130))

    dw = draw.textlength(DOMAIN, font=f_dom)
    draw.text((W - pad - dw, H - 104), DOMAIN, font=f_dom, fill=(255, 255, 255))

    card.convert("RGB").save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes, {W}x{H})")


def spaced(text, gap=" "):
    return gap.join(text)


if __name__ == "__main__":
    main()
