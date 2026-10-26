#!/usr/bin/env python3
"""Procedural painted textures for sy-alhambra-ornament-panel.

Patterns are drawn from the evidence in ../refs/ (see NOTES.md):
- diamond-lattice tile dado, zigzag dentil band, dark inscription-style
  band: read from the 1856 guide p.66 woodcut "Entrance to Alhambra Court"
  (the same view as the coloured lead print, catalogue 0108).
- sebka diamond net with a small palmette in each diamond: the upper-wall
  field of the entrance view; also the interior pier diaper in the woodcut.
- roundel frieze: the band of circles above the arches in the woodcut's
  interior view.
- stacked quatrefoil medallions: the entrance pier panels in the woodcut.

Colours: warm gold/ivory stucco ground and dark blue-black bands are what
the coloured lead print (0108) attests; blue/red/gold accents follow Owen
Jones's published primary scheme for the court and are INTERPRETIVE
(see NOTES.md). The "inscription" bands are abstract interlaced knot
blocks -- decorative geometry, NOT copied letterforms.

Run with system python3 + PIL before the Blender build script.
Outputs ../textures/panel_front.png, panel_bump.png, strip_front.png,
strip_bump.png.
"""
import math, os, random
from PIL import Image, ImageDraw

random.seed(1854)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "textures")
os.makedirs(OUT, exist_ok=True)

# --- palette (sRGB) -------------------------------------------------------
IVORY   = (219, 193, 141)   # warm stucco ground
IVORY_D = (198, 168, 112)   # shaded stucco
GOLD    = (178, 134, 54)
GOLD_L  = (214, 172, 92)
BLUE    = (32, 54, 104)     # Jones blue
DARK    = (17, 24, 46)      # blue-black band ground (lead print: near-black)
RED     = (148, 45, 33)
GREEN   = (53, 93, 63)
TEAL    = (19, 63, 68)      # dado diamond glaze
TEAL_D  = (13, 46, 52)
CREAM   = (233, 219, 182)   # lattice lines / light ornament
INK     = (43, 34, 22)      # pattern outline

PANEL_W_M = 3.60
S = 2048                    # panel texture px (square panel)
PXM = S / PANEL_W_M         # px per metre

def z2py(z):                # metres above floor -> texture y (down)
    return S - z * PXM

# =========================================================================
# PANEL FRONT
# =========================================================================
img = Image.new("RGB", (S, S), IVORY)
bmp = Image.new("L", (S, S), 96)
d = ImageDraw.Draw(img)
b = ImageDraw.Draw(bmp)

# ---- zone boundaries (m) ----
SKIRT_T   = 0.12
DADO_T    = 0.86
ZIG_T     = 0.98
INSC_T     = 1.16
FIELD_T   = 3.10
FRIEZE_T  = 3.43
TOP       = 3.60

def zone(z0, z1, fill, bfill=None):
    d.rectangle([0, z2py(z1), S, z2py(z0)], fill=fill)
    if bfill is not None:
        b.rectangle([0, z2py(z1), S, z2py(z0)], fill=bfill)

# skirting
zone(0.0, SKIRT_T, (74, 55, 34), 40)
d.line([0, z2py(SKIRT_T), S, z2py(SKIRT_T)], fill=GOLD_L, width=5)

# ---- dado: diamond lattice (woodcut: dark diamonds, light lattice) ----
zone(SKIRT_T, DADO_T, CREAM, 60)
dw, dh = 0.36 * PXM, 0.185 * PXM          # diamond w x h (2:1, as drawn)
y_top, y_bot = z2py(DADO_T), z2py(SKIRT_T)
_clip = Image.new("L", (S, S), 0)
ImageDraw.Draw(_clip).rectangle([0, y_top, S, y_bot], fill=255)
_dl = Image.new("RGB", (S, S), CREAM); _db = Image.new("L", (S, S), 60)
dd, db_ = ImageDraw.Draw(_dl), ImageDraw.Draw(_db)
row = 0
cy = y_top + dh / 2
while cy < y_bot + dh:
    off = (dw / 2) if row % 2 else 0.0
    cx = -dw + off
    while cx < S + dw:
        jit = random.randint(-9, 9)
        fill = (TEAL[0] + jit, TEAL[1] + jit, TEAL[2] + jit)
        pts = [(cx, cy - dh / 2 + 7), (cx + dw / 2 - 7, cy),
               (cx, cy + dh / 2 - 7), (cx - dw / 2 + 7, cy)]
        dd.polygon(pts, fill=fill)
        db_.polygon(pts, fill=150)
        cx += dw
    cy += dh
    row += 1
img.paste(_dl, (0, 0), _clip)
bmp.paste(_db, (0, 0), _clip)
d = ImageDraw.Draw(img); b = ImageDraw.Draw(bmp)
# tiny gold dot at lattice crossings
yy = y_top
while yy < y_bot:
    xx = 0.0
    while xx < S:
        d.ellipse([xx - 4, yy - 4, xx + 4, yy + 4], fill=GOLD_L)
        xx += dw / 2
    yy += dh / 2
d.line([0, y_top, S, y_top], fill=INK, width=4)
d.line([0, y_bot, S, y_bot], fill=INK, width=4)

# ---- zigzag dentil band (woodcut: dark triangles on light) ----
zone(DADO_T, ZIG_T, IVORY_D, 110)
pitch = 0.12 * PXM
x = 0.0
yt, yb = z2py(ZIG_T), z2py(DADO_T)
while x < S:
    d.polygon([(x + 3, yb - 3), (x + pitch - 3, yb - 3), (x + pitch / 2, yt + 3)], fill=DARK)
    b.polygon([(x + 3, yb - 3), (x + pitch - 3, yb - 3), (x + pitch / 2, yt + 3)], fill=170)
    x += pitch
d.line([0, yt, S, yt], fill=INK, width=4)
d.line([0, yb, S, yb], fill=INK, width=4)

# ---- inscription-style band: abstract kufesque knot blocks (NOT script) ----
zone(ZIG_T, INSC_T, DARK, 30)
unit = 0.30 * PXM
yt, yb = z2py(INSC_T), z2py(ZIG_T)
ymid = (yt + yb) / 2
x = 0.0
while x < S:
    # interlaced square-knot glyph: vertical stems + square spirals
    d.line([x + unit * 0.30, yb - 10, x + unit * 0.30, yt + 10], fill=CREAM, width=9)
    d.line([x + unit * 0.70, yb - 10, x + unit * 0.70, yt + 10], fill=CREAM, width=9)
    d.rectangle([x + unit * 0.30, ymid - 16, x + unit * 0.70, ymid + 16], outline=CREAM, width=8)
    d.line([x + 4, ymid, x + unit * 0.30, ymid], fill=CREAM, width=8)
    d.line([x + unit * 0.70, ymid, x + unit - 4, ymid], fill=CREAM, width=8)
    d.ellipse([x + unit / 2 - 7, ymid - 7, x + unit / 2 + 7, ymid + 7], fill=GOLD_L)
    b.line([x + unit * 0.30, yb - 10, x + unit * 0.30, yt + 10], fill=200, width=9)
    b.line([x + unit * 0.70, yb - 10, x + unit * 0.70, yt + 10], fill=200, width=9)
    x += unit
d.line([0, yt, S, yt], fill=GOLD_L, width=5)
d.line([0, yb, S, yb], fill=GOLD_L, width=5)

# ---- sebka field: painted palmettes; net shadow lines (ribs are geometry)
zone(INSC_T, FIELD_T, IVORY, 96)
sdw, sdh = 0.45 * PXM, 0.485 * PXM
y0 = z2py(FIELD_T)          # top of field in px
rows = int(round((FIELD_T - INSC_T) / 0.2425))
# faint net shadow (aligns with geometry ribs)
for j in range(rows + 1):
    cy = y0 + j * sdh / 2
    off = (sdw / 2) if j % 2 else 0.0
    cx = -sdw + off
    while cx < S + sdw:
        d.line([cx - sdw / 2, cy, cx, cy - sdh / 2], fill=(172, 148, 102), width=5)
        d.line([cx, cy - sdh / 2, cx + sdw / 2, cy], fill=(172, 148, 102), width=5)
        d.line([cx - sdw / 2, cy, cx, cy + sdh / 2], fill=(172, 148, 102), width=5)
        d.line([cx, cy + sdh / 2, cx + sdw / 2, cy], fill=(172, 148, 102), width=5)
        cx += sdw
# palmette at each diamond centre
ACCENTS = [RED, BLUE, GREEN]
def palmette(cx, cy, s, accent):
    # central teardrop
    d.polygon([(cx, cy - s), (cx + s * 0.42, cy + s * 0.25), (cx, cy + s * 0.55),
               (cx - s * 0.42, cy + s * 0.25)], fill=GOLD_L, outline=INK)
    d.ellipse([cx - s * 0.13, cy - s * 0.30, cx + s * 0.13, cy - s * 0.04], fill=accent)
    # side curls
    for sgn in (-1, 1):
        d.arc([cx + sgn * s * 0.72 - s * 0.30, cy - s * 0.05,
               cx + sgn * s * 0.72 + s * 0.30, cy + s * 0.55],
              start=90, end=330, fill=INK, width=6)
    d.ellipse([cx - 5, cy + s * 0.68, cx + 5, cy + s * 0.68 + 10], fill=accent)
for j in range(rows):
    cy = y0 + (j + 0.5) * sdh / 2
    if cy > z2py(INSC_T) - 20:
        continue
    off = (sdw / 2) if j % 2 else 0.0
    i = 0
    cx = off
    while cx < S:
        palmette(cx, cy, 52, ACCENTS[(i + j) % 3])
        cx += sdw
        i += 1
# field bump: strong net lines
for j in range(rows + 1):
    cy = y0 + j * sdh / 2
    off = (sdw / 2) if j % 2 else 0.0
    cx = -sdw + off
    while cx < S + sdw:
        b.line([cx - sdw / 2, cy, cx, cy - sdh / 2], fill=235, width=16)
        b.line([cx, cy - sdh / 2, cx + sdw / 2, cy], fill=235, width=16)
        b.line([cx - sdw / 2, cy, cx, cy + sdh / 2], fill=235, width=16)
        b.line([cx, cy + sdh / 2, cx + sdw / 2, cy], fill=235, width=16)
        cx += sdw

# ---- roundel frieze (interior view: row of circles above the arches) ----
zone(FIELD_T, FRIEZE_T, IVORY_D, 110)
yt, yb = z2py(FRIEZE_T), z2py(FIELD_T)
ymid = (yt + yb) / 2
r_out, r_in = 0.135 * PXM, 0.088 * PXM
x = 0.225 * PXM
k = 0
while x < S:
    d.ellipse([x - r_out, ymid - r_out, x + r_out, ymid + r_out], fill=BLUE)
    d.ellipse([x - r_in, ymid - r_in, x + r_in, ymid + r_in], fill=GOLD_L)
    # six-petal flower
    for p in range(6):
        a = math.radians(p * 60)
        px_, py_ = x + math.cos(a) * r_in * 0.52, ymid + math.sin(a) * r_in * 0.52
        col = RED if (p + k) % 2 == 0 else BLUE
        d.ellipse([px_ - 15, py_ - 15, px_ + 15, py_ + 15], fill=col)
    d.ellipse([x - 10, ymid - 10, x + 10, ymid + 10], fill=IVORY)
    b.ellipse([x - r_out, ymid - r_out, x + r_out, ymid + r_out], outline=235, width=14)
    x += 0.45 * PXM
    k += 1
d.line([0, yt, S, yt], fill=INK, width=4)
d.line([0, yb, S, yb], fill=INK, width=4)

# ---- cornice ----
zone(FRIEZE_T, TOP, IVORY_D, 130)
d.line([0, z2py(3.515), S, z2py(3.515)], fill=GOLD, width=6)
d.line([0, z2py(TOP) + 3, S, z2py(TOP) + 3], fill=INK, width=4)

img.save(os.path.join(OUT, "panel_front.png"))
bmp.save(os.path.join(OUT, "panel_bump.png"))

# =========================================================================
# MEDALLION STRIP FRONT  (0.56 m wide x 3.60 m high)
# =========================================================================
SW, SH = 1024, 2048
simg = Image.new("RGB", (SW, SH), IVORY_D)
sbmp = Image.new("L", (SW, SH), 96)
sd = ImageDraw.Draw(simg)
sb = ImageDraw.Draw(sbmp)

# ground: fine star diaper
step = 64
for gy in range(-step, SH + step, step):
    for gx in range(-step, SW + step, step):
        ox = (step // 2) if (gy // step) % 2 else 0
        cx, cy = gx + ox, gy
        r = 15
        pts = []
        for p in range(16):
            a = math.radians(p * 22.5 - 90)
            rr = r if p % 2 == 0 else r * 0.45
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        sd.polygon(pts, outline=(120, 100, 66))
        sd.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(120, 100, 66))

def quatrefoil_pts(cx, cy, rx, ry, n=160):
    """Union outline of four overlapping lobes (polar max-radius)."""
    lobes = [(rx * 0.40, 0, rx * 0.55), (-rx * 0.40, 0, rx * 0.55),
             (0, ry * 0.40, ry * 0.55), (0, -ry * 0.40, ry * 0.55),
             (0, 0, rx * 0.46)]
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        ux, uy = math.cos(a), math.sin(a)
        best = 0.0
        for (lx, ly, lr) in lobes:
            # scale y for elliptical lobes
            cu = lx * ux + ly * uy
            cross = abs(lx * uy - ly * ux)
            if cross < lr:
                r = cu + math.sqrt(max(lr * lr - cross * cross, 0.0))
                best = max(best, r)
        pts.append((cx + ux * best, cy + uy * best))
    return pts

N_MED = 7
pitch_px = SH / N_MED
med_rx, med_ry = SW * 0.335, pitch_px * 0.415
for m in range(N_MED):
    cy = pitch_px * (m + 0.5)
    cx = SW / 2
    pts = quatrefoil_pts(cx, cy, med_rx, med_ry)
    sd.polygon(pts, fill=DARK)
    sb.polygon(pts, fill=60)
    # outline: thick ivory line with blue edge (drawn as successive outlines)
    for wdt, col in ((26, CREAM), (14, GOLD_L)):
        for i in range(len(pts)):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % len(pts)]
            sd.line([x1, y1, x2, y2], fill=col, width=wdt)
            sb.line([x1, y1, x2, y2], fill=235, width=10)
    # arabesque fill: central 8-point star + lobe palmettes + scroll curls
    r0 = med_ry * 0.44
    star = []
    for p in range(16):
        a = math.radians(p * 22.5 - 90)
        rr = r0 if p % 2 == 0 else r0 * 0.48
        star.append((cx + math.cos(a) * rr * 1.25, cy + math.sin(a) * rr))
    sd.polygon(star, fill=RED, outline=CREAM)
    sd.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=GOLD_L)
    for (dx, dy, col) in ((0.55, 0, BLUE), (-0.55, 0, BLUE), (0, 0.58, GREEN), (0, -0.58, GREEN)):
        px_, py_ = cx + dx * med_rx, cy + dy * med_ry
        sd.polygon([(px_, py_ - 36), (px_ + 24, py_ + 20), (px_, py_ + 36),
                    (px_ - 24, py_ + 20)], fill=col, outline=CREAM)
    # scroll curls in the four diagonal fields
    for (dx, dy) in ((0.33, 0.36), (-0.33, 0.36), (0.33, -0.36), (-0.33, -0.36)):
        px_, py_ = cx + dx * med_rx, cy + dy * med_ry
        sd.arc([px_ - 34, py_ - 34, px_ + 34, py_ + 34], start=40, end=320,
               fill=CREAM, width=8)
        sd.ellipse([px_ - 8, py_ - 8, px_ + 8, py_ + 8], fill=GOLD_L)
    # dot ring
    for p in range(12):
        a = math.radians(p * 30)
        px_, py_ = cx + math.cos(a) * med_rx * 0.80, cy + math.sin(a) * med_ry * 0.80
        sd.ellipse([px_ - 7, py_ - 7, px_ + 7, py_ + 7], fill=CREAM)

# side border lines
for bx in (26, SW - 26):
    sd.line([bx, 0, bx, SH], fill=BLUE, width=10)
    sb.line([bx, 0, bx, SH], fill=200, width=8)

simg.save(os.path.join(OUT, "strip_front.png"))
sbmp.save(os.path.join(OUT, "strip_bump.png"))
print("textures written to", OUT)
