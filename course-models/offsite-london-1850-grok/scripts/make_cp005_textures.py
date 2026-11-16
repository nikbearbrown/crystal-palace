#!/usr/bin/env python3
"""CP005 CANDIDATE plan textures (PIL, seeded, deterministic). 1849-Jan 1850: the exhibition is planned but the BUILDING is
not designed yet (Paxton's scheme is June 1850), so no Crystal Palace drawings appear (D-LN-CP005-03). Sheets carry no
legible wording: every 'label' is an illegible pen scribble (storyboard CP005: "No fabricated document wording is legible").
  cp005_siteplan.png    Hyde Park south strip with the large rectangle marked in red for the exhibition (the shot's subject)
  cp005_allocation.png  floor allocation: one long rectangle divided into washed blocks per exhibiting nation / class
  cp005_schedule.png    ruled schedule of goods (columns + scribbled entries)
  cp005_londonmap.png   framed wall map of London: Thames, street grain, parks
usage: python3 make_cp005_textures.py [outdir=textures]"""
import sys, math, random, os
from PIL import Image, ImageDraw, ImageFilter
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "textures")
PAPER = (222, 210, 182); INK = (52, 44, 38); RED = (160, 52, 40)

def paper(w, h, seed, base=PAPER):
    r = random.Random(seed); im = Image.new("RGB", (w, h), base); px = im.load()
    noise = Image.effect_noise((w // 8, h // 8), 22).resize((w, h), Image.BICUBIC)
    n = noise.load()
    for y in range(h):
        for x in range(w):
            d = (n[x, y] - 128) * 0.10
            e = min(x, y, w - 1 - x, h - 1 - y); edge = max(0, 30 - e) * 0.6   # foxed edges
            px[x, y] = tuple(max(0, min(255, int(c + d - edge))) for c in base)
    return im

def scribble(d, x, y, length, h, r, col=INK, w=2):
    """illegible pen line: wavy stroke with pen lifts, reads as handwriting but no letters"""
    cx = x
    while cx < x + length:
        seg = r.uniform(18, 60); pts = []
        for k in range(int(seg / 3)):
            xx = cx + k * 3; pts.append((xx, y + math.sin(xx * 0.9 + r.random()) * h * r.uniform(0.3, 1.0)))
        if len(pts) > 1: d.line(pts, fill=col, width=w)
        cx += seg + r.uniform(6, 14)

def wash(im, poly, col, alpha):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).polygon(poly, fill=(*col, alpha))
    ov = ov.filter(ImageFilter.GaussianBlur(2)); im.paste(Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"))

def siteplan():
    W, H = 1800, 1250; r = random.Random(1849); im = paper(W, H, 1)
    wash(im, [(60, 60), (W - 60, 60), (W - 60, H - 210), (60, H - 210)], (120, 150, 90), 70)          # park
    wash(im, [(60, 60), (520, 60), (430, 200), (260, 260), (60, 230)], (90, 120, 140), 110)            # Serpentine tail
    d = ImageDraw.Draw(im)
    d.rectangle([40, 40, W - 40, H - 40], outline=INK, width=4); d.rectangle([52, 52, W - 52, H - 52], outline=INK, width=1)
    d.line([(60, H - 200), (W - 60, H - 200)], fill=INK, width=3); d.line([(60, H - 150), (W - 60, H - 150)], fill=INK, width=3)  # Kensington Road
    d.line([(60, 330), (W - 60, 300)], fill=INK, width=2); d.line([(60, 352), (W - 60, 322)], fill=INK, width=2)              # Rotten Row
    for _ in range(420):                                                                                       # trees
        x, y = r.uniform(80, W - 80), r.uniform(80, H - 230)
        if 300 < x < 1500 and 420 < y < 920: continue
        rr = r.uniform(7, 15); d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=(60, 80, 45), width=2)
    for x in (560, 1000, 1240):   # three elms kept inside the marked ground (cf. CP008)
        d.ellipse([x - 22, 640 - 22, x + 22, 640 + 22], outline=(60, 80, 45), width=3)
    # the large space marked for exhibits: red ink rectangle, faint diagonal hatching, dimension ticks
    x0, y0, x1, y1 = 300, 430, 1500, 910
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for k in range(-H, W, 26): od.line([(k, y1), (k + (y1 - y0), y0)], fill=(*RED, 40), width=2)
    mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).rectangle([x0, y0, x1, y1], fill=255)
    im.paste(Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"), mask=mask); d = ImageDraw.Draw(im)
    d.rectangle([x0, y0, x1, y1], outline=RED, width=7)
    for xx in range(x0, x1 + 1, 100): d.line([(xx, y1 + 18), (xx, y1 + 34)], fill=INK, width=2)
    d.line([(x0, y1 + 26), (x1, y1 + 26)], fill=INK, width=2)
    d.polygon([(W - 150, 120), (W - 135, 200), (W - 150, 185), (W - 165, 200)], fill=INK)                      # north arrow
    for i in range(4): scribble(d, W - 520, H - 120 + i * 18, 400 - i * 60, 5, r)                              # title block
    d.rectangle([W - 540, H - 135, W - 90, H - 55], outline=INK, width=2)
    for xx in range(100, 500, 40): d.rectangle([xx, H - 100, xx + 40, H - 90], fill=INK if (xx // 40) % 2 else None, outline=INK)
    im.save(os.path.join(OUT, "cp005_siteplan.png"))

def allocation():
    W, H = 1600, 1100; r = random.Random(1850); im = paper(W, H, 2, (226, 216, 192)); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 90, 260, W - 90, 760
    cols = [(170, 70, 60), (70, 100, 150), (190, 160, 70), (90, 130, 80), (140, 90, 130), (190, 120, 60), (110, 110, 110)]
    for yy0, yy1 in ((y0, (y0 + y1) / 2 - 22), ((y0 + y1) / 2 + 22, y1)):
        x = x0
        while x < x1 - 10:
            w = min(r.choice((70, 90, 120, 160, 210)), x1 - x)
            wash(im, [(x + 3, yy0 + 3), (x + w - 3, yy0 + 3), (x + w - 3, yy1 - 3), (x + 3, yy1 - 3)], r.choice(cols), r.randint(70, 120))
            x += w
    d = ImageDraw.Draw(im); d.rectangle([x0, y0, x1, y1], outline=INK, width=4)
    d.line([(x0, (y0 + y1) / 2 - 22), (x1, (y0 + y1) / 2 - 22)], fill=INK, width=2); d.line([(x0, (y0 + y1) / 2 + 22), (x1, (y0 + y1) / 2 + 22)], fill=INK, width=2)
    d.line([((x0 + x1) / 2 - 30, y0), ((x0 + x1) / 2 - 30, y1)], fill=INK, width=2); d.line([((x0 + x1) / 2 + 30, y0), ((x0 + x1) / 2 + 30, y1)], fill=INK, width=2)
    for i in range(3): scribble(d, 120, 90 + i * 32, 900 - i * 200, 7, r, w=3)
    for i in range(9): scribble(d, 120 + (i % 3) * 470, 830 + (i // 3) * 60, 380, 5, r)
    d.rectangle([40, 40, W - 40, H - 40], outline=INK, width=3)
    im.save(os.path.join(OUT, "cp005_allocation.png"))

def schedule():
    W, H = 1000, 1350; r = random.Random(1851); im = paper(W, H, 3, (230, 224, 204)); d = ImageDraw.Draw(im)
    for i in range(2): scribble(d, 120, 80 + i * 34, 700 - i * 250, 8, r, w=3)
    for x in (80, 180, 640, 800, 920): d.line([(x, 170), (x, H - 80)], fill=(150, 60, 50), width=2)
    for k in range(34):
        y = 200 + k * 34; d.line([(80, y), (920, y)], fill=(140, 150, 170), width=1)
        if k < 30:
            scribble(d, 95, y - 10, 60, 4, r); scribble(d, 195, y - 10, r.uniform(150, 420), 5, r); scribble(d, 655, y - 10, 110, 4, r)
    im.save(os.path.join(OUT, "cp005_schedule.png"))

def londonmap():
    W, H = 1800, 1200; r = random.Random(1666); im = paper(W, H, 4, (214, 200, 166))
    for _ in range(9):                                              # parks
        cx, cy, rr = r.uniform(150, W - 150), r.uniform(120, 520), r.uniform(50, 130)
        wash(im, [(cx + rr * math.cos(a) * r.uniform(0.7, 1.2), cy + rr * 0.7 * math.sin(a) * r.uniform(0.7, 1.2)) for a in [i * math.pi / 6 for i in range(12)]], (110, 140, 85), 90)
    d = ImageDraw.Draw(im)
    river = [(x, 760 + 140 * math.sin(x / 300.0) + 60 * math.sin(x / 97.0)) for x in range(0, W + 1, 10)]
    for _ in range(1400):                                           # street grain: short ink strokes, denser east
        x, y = r.uniform(70, W - 70), r.uniform(70, H - 70)
        ry = 760 + 140 * math.sin(x / 300.0) + 60 * math.sin(x / 97.0)
        if abs(y - ry) < 50: continue
        a = r.choice((0, math.pi / 2)) + r.uniform(-0.35, 0.35); L = r.uniform(25, 90)
        d.line([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], fill=(90, 76, 62), width=2)
    up = [(x, y - 34) for x, y in river]; dn = [(x, y + 34) for x, y in reversed(river)]
    d.polygon(up + dn, fill=(120, 140, 150)); d.line(up, fill=INK, width=3); d.line([p for p in reversed(dn)], fill=INK, width=3)
    for x in (520, 820, 1100, 1380):                                # bridges
        y = 760 + 140 * math.sin(x / 300.0) + 60 * math.sin(x / 97.0); d.rectangle([x - 6, y - 44, x + 6, y + 44], fill=(90, 76, 62))
    d.rectangle([30, 30, W - 30, H - 30], outline=INK, width=6)
    for k in range(30, W - 30, 40): d.rectangle([k, 30, k + 20, 44], fill=INK)                             # graduated border
    for k in range(30, H - 30, 40): d.rectangle([30, k, 44, k + 20], fill=INK)
    d.rectangle([W - 560, 70, W - 80, 230], fill=(226, 214, 184), outline=INK, width=3)
    for i in range(3): scribble(d, W - 530, 110 + i * 40, 400 - i * 90, 9 - i * 2, r, w=3)                 # cartouche (illegible)
    im.save(os.path.join(OUT, "cp005_londonmap.png"))

os.makedirs(OUT, exist_ok=True)
for f in (siteplan, allocation, schedule, londonmap): f(); print("TEX", f.__name__)
