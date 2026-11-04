#!/usr/bin/env python3
"""Open Graph cards (1200×630) for link previews on X, LinkedIn, WhatsApp and the like.

Usage: python3 tools/og.py [--force]

Writes assets/og/home.png and assets/og/<date>.png for every episode in episodes.json,
in the cover's look (dark #0e1117, cream #f3efe6, amber #f59e0b, Inter). build.py uses a
card as og:image when it exists and falls back to the cover otherwise. The Pages
workflow runs this before build.py; the PNGs are build output and are not committed.
Needs Pillow and the Inter font (fonts-inter), with DejaVu as a fallback.
"""
import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from pages import short_title, tr_date  # noqa: E402

W, H = 1200, 630
BG, INK, MUTED, ACCENT = "#0e1117", "#f3efe6", "#9aa0ad", "#f59e0b"
FONTS = {
    "black": ["/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", "/usr/share/fonts/truetype/inter/Inter-ExtraBold.ttf",
              "/usr/share/fonts/opentype/inter/Inter-Bold.otf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "bold": ["/usr/share/fonts/opentype/inter/Inter-Bold.otf", "/usr/share/fonts/truetype/inter/Inter-Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "medium": ["/usr/share/fonts/opentype/inter/Inter-Medium.otf", "/usr/share/fonts/truetype/inter/Inter-Medium.ttf",
               "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
}
PAD = 72


def font(kind, size):
    from PIL import ImageFont
    for p in FONTS[kind]:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    raise SystemExit("no usable font; install fonts-inter or fonts-dejavu")


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_title(draw, text, width, max_h):
    """Largest size (72 → 40) at which the title fits in ≤4 lines; ellipsis as a last resort."""
    for size in range(68, 38, -4):
        fnt = font("black", size)
        lines = wrap(draw, text, fnt, width)
        lh = int(size * 1.12)
        if len(lines) <= 4 and lh * len(lines) <= max_h:
            return fnt, lines, lh
    fnt = font("black", 40)
    lines = wrap(draw, text, fnt, width)[:4]
    lines[-1] = lines[-1].rstrip(",;: ") + "…"
    return fnt, lines, 45


def waveform(draw, x0, y_mid, width, n=46):
    step = width / n
    for i in range(n):
        h = 14 + 54 * abs(math.sin(i * 1.7) * math.cos(i * 0.43))
        x = x0 + i * step
        color = ACCENT if i in (13, 31) else "#3a3f4b"
        draw.rounded_rectangle([x, y_mid - h / 2, x + step * 0.42, y_mid + h / 2], radius=4, fill=color)


def brand(draw, x, y, size=34):
    f = font("black", size)
    draw.text((x, y), "HAL", font=f, fill=ACCENT)
    x2 = x + draw.textlength("HAL", font=f)
    draw.text((x2, y), "'imiz Ne Olacak?", font=f, fill=INK)


def card(kicker, title, out, footer="halimiz.derinbay.com"):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    # soft amber glow, top right, like the cover
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    for r in range(320, 0, -8):
        gd.ellipse([W - 160 - r, -120 - r, W - 160 + r, -120 + r], fill=int(38 * (1 - r / 320)))
    im.paste(Image.new("RGB", (W, H), "#3b2a0a"), (0, 0), glow)
    d = ImageDraw.Draw(im)
    d.text((PAD, PAD - 6), kicker.replace("i", "İ").upper(), font=font("bold", 24), fill=ACCENT, spacing=4)
    fnt, lines, lh = fit_title(d, title, W - 2 * PAD, 300)
    y = PAD + 52
    for line in lines:
        d.text((PAD, y), line, font=fnt, fill=INK)
        y += lh
    waveform(d, PAD, H - 150, W - 2 * PAD)
    brand(d, PAD, H - 92)
    f = font("medium", 24)
    d.text((W - PAD - d.textlength(footer, font=f), H - 84), footer, font=f, fill=MUTED)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    show = json.loads((ROOT / "podcast.json").read_text(encoding="utf-8"))
    eps = json.loads((ROOT / "episodes.json").read_text(encoding="utf-8"))
    og = ROOT / "assets" / "og"
    made = 0
    if a.force or not (og / "home.png").exists():
        card("Günlük yapay zekâ ve teknoloji podcasti", show["tagline"], og / "home.png", "Derinbay Labs · halimiz.derinbay.com")
        made += 1
    for ep in eps:
        out = og / f"{ep['date']}.png"
        if out.exists() and not a.force:
            continue
        kicker = f"{tr_date(ep['date'], weekday=True)} · {round(ep['duration_seconds'] / 60)} dk"
        card(kicker, short_title(ep["title"]), out)
        made += 1
    print(f"og cards: {made} written, {len(eps) + 1 - made} up to date")


if __name__ == "__main__":
    main()
