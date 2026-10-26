#!/usr/bin/env python3
"""Procedural painted textures for sy-egyptian-column-pair.

Run with system python3 (needs PIL) BEFORE the bpy build script.
The glyphs are decorative glyph-LIKE marks drawn from simple shapes;
they are not copied hieroglyphic inscriptions (see NOTES.md).
Palette: restrained Owen Jones-era polychromy, labelled interpretive.
"""
from PIL import Image, ImageDraw
import math, os, random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "textures")
os.makedirs(OUT, exist_ok=True)
random.seed(1854)

SAND = (203, 178, 138)
SAND_D = (188, 160, 118)
BLUE = (52, 92, 138)
GREEN = (70, 122, 84)
RED = (158, 66, 44)
GOLD = (196, 156, 74)
DARK = (74, 56, 40)
CREAM = (226, 208, 170)


def glyph(d, x, y, s, col):
    """One abstract glyph-like mark in an s-by-s box."""
    k = random.randrange(8)
    if k == 0:  # eye
        d.ellipse([x + 2, y + s * .3, x + s - 2, y + s * .7], outline=col, width=3)
        d.ellipse([x + s * .4, y + s * .4, x + s * .6, y + s * .6], fill=col)
    elif k == 1:  # ankh-like
        d.ellipse([x + s * .35, y + 2, x + s * .65, y + s * .4], outline=col, width=3)
        d.line([x + s * .5, y + s * .4, x + s * .5, y + s - 2], fill=col, width=3)
        d.line([x + s * .2, y + s * .55, x + s * .8, y + s * .55], fill=col, width=3)
    elif k == 2:  # reed strokes
        for i in range(3):
            d.line([x + 6 + i * s * .3, y + s - 2, x + 10 + i * s * .3, y + 2], fill=col, width=3)
    elif k == 3:  # star
        cx, cy, r = x + s / 2, y + s / 2, s * .38
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * .45
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(pts, fill=col)
    elif k == 4:  # water zigzag
        for j in range(2):
            yy = y + s * (.3 + .3 * j)
            d.line([x + 2, yy, x + s * .3, yy - s * .15, x + s * .6, yy, x + s - 2, yy - s * .15], fill=col, width=3)
    elif k == 5:  # sun disc
        d.ellipse([x + s * .2, y + s * .2, x + s * .8, y + s * .8], outline=col, width=3)
    elif k == 6:  # feather
        d.line([x + s * .5, y + s - 2, x + s * .5, y + 2], fill=col, width=3)
        d.arc([x + s * .18, y + 2, x + s * .82, y + s * .8], 270, 90, fill=col, width=3)
        d.arc([x + s * .18, y + 2, x + s * .82, y + s * .8], 90, 270, fill=col, width=3)
    else:  # seated-bird blob
        d.ellipse([x + s * .15, y + s * .45, x + s * .75, y + s * .8], fill=col)
        d.ellipse([x + s * .6, y + s * .2, x + s * .9, y + s * .5], fill=col)
        d.line([x + s * .3, y + s * .8, x + s * .3, y + s - 2], fill=col, width=3)
        d.line([x + s * .6, y + s * .8, x + s * .6, y + s - 2], fill=col, width=3)


def figure(d, cx, base, h, col):
    """Stylised profile figure (flat, relief-like, low contrast)."""
    w = h * 0.30
    hy = base - h
    # profile head with skull-cap/back sweep
    d.ellipse([cx - w * .05, hy, cx + w * .22, hy + h * .12], fill=col)
    d.polygon([(cx + w * .05, hy + h * .02), (cx - w * .20, hy + h * .10),
               (cx + w * .10, hy + h * .14)], fill=col)
    # torso, slightly forward
    d.polygon([(cx - w * .18, hy + h * .13), (cx + w * .20, hy + h * .13),
               (cx + w * .14, base - h * .46), (cx - w * .14, base - h * .46)], fill=col)
    # broad collar
    d.rectangle([cx - w * .22, hy + h * .13, cx + w * .24, hy + h * .20], fill=col)
    # kilt
    d.polygon([(cx - w * .14, base - h * .46), (cx + w * .14, base - h * .46),
               (cx + w * .26, base - h * .24), (cx - w * .26, base - h * .24)], fill=col)
    # striding legs: one forward, one back
    d.polygon([(cx - w * .10, base - h * .24), (cx + w * .02, base - h * .24),
               (cx + w * .30, base - 2), (cx + w * .16, base - 2)], fill=col)
    d.polygon([(cx - w * .02, base - h * .24), (cx + w * .10, base - h * .24),
               (cx - w * .18, base - 2), (cx - w * .30, base - 2)], fill=col)
    # rear arm down, front arm to a staff
    d.rectangle([cx - w * .26, hy + h * .15, cx - w * .16, base - h * .30], fill=col)
    d.line([cx + w * .42, hy + h * .10, cx + w * .42, base], fill=col, width=max(3, int(h * .02)))
    d.polygon([(cx + w * .16, hy + h * .16), (cx + w * .24, hy + h * .16),
               (cx + w * .44, base - h * .38), (cx + w * .36, base - h * .42)], fill=col)


def shaft_texture():
    W, H = 1024, 2048
    img = Image.new("RGB", (W, H), SAND)
    d = ImageDraw.Draw(img)
    # subtle vertical shading streaks
    for i in range(300):
        x = random.randrange(W)
        d.line([x, 0, x, H], fill=SAND_D, width=1)
    # texture v: v=1 (top of image = top?) PIL y down; Blender UV v0 at bottom.
    # Registers: 4 figure registers separated by glyph bands.
    bands = []  # (y_top, y_bot) in image coords; image top = shaft top
    reg_h = H // 5
    for i in range(5):
        y0 = i * reg_h
        # glyph band at the top of each register (except very top handled by necking)
        band_h = 64
        d.rectangle([0, y0, W, y0 + band_h], fill=CREAM)
        d.rectangle([0, y0, W, y0 + 6], fill=DARK)
        d.rectangle([0, y0 + band_h - 6, W, y0 + band_h], fill=DARK)
        n = 12
        for gI in range(n):
            col = [BLUE, RED, GREEN, DARK][gI % 4]
            glyph(d, gI * (W // n) + 8, y0 + 8, band_h - 16, col)
        # figure register below the band
        fy0, fy1 = y0 + band_h + 26, y0 + reg_h - 18
        d.rectangle([0, fy1, W, fy1 + 5], fill=DARK)
        for fI in range(4):
            cx = (fI + 0.5) * (W / 4)
            col = (148, 112, 78) if fI % 2 == 0 else (134, 106, 74)
            figure(d, cx, fy1 - 8, (fy1 - fy0) * 0.96, col)
        bands.append((y0, y0 + reg_h))
    # plain baseline at the very bottom (the petal collar is geometry)
    d.rectangle([0, H - 10, W, H], fill=DARK)
    img.save(os.path.join(OUT, "shaft_paint.png"))
    print("shaft_paint.png")


def capital_texture():
    W, H = 1024, 512
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    ribs = 18
    cols = [BLUE, GREEN, RED, GOLD]
    for i in range(ribs):
        x0 = i * W / ribs
        d.rectangle([x0, 0, x0 + W / ribs, H], fill=cols[i % 4])
        d.rectangle([x0, 0, x0 + 4, H], fill=DARK)
    # neck ring dots at bottom
    d.rectangle([0, H - 70, W, H], fill=DARK)
    for i in range(24):
        cx = (i + .5) * W / 24
        d.ellipse([cx - 9, H - 52, cx + 9, H - 34], fill=GOLD)
    img.save(os.path.join(OUT, "capital_paint.png"))
    print("capital_paint.png")


def abacus_texture():
    W, H = 1024, 128
    img = Image.new("RGB", (W, H), (196, 168, 124))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=DARK); d.rectangle([0, H - 8, W, H], fill=DARK)
    n = 12
    for gI in range(n):
        glyph(d, gI * (W // n) + 8, 14, H - 28, [BLUE, RED, GREEN][gI % 3])
    img.save(os.path.join(OUT, "abacus_paint.png"))
    print("abacus_paint.png")


if __name__ == "__main__":
    shaft_texture(); capital_texture(); abacus_texture()
