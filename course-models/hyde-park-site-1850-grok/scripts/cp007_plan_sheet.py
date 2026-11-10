"""Draw the interpretive ground-plan sheet for the CP007 table (our own line drawing from cp007_committee_layout,
after the 1850 lithographed plan; NOT a facsimile). -> textures/cp007_committee_plan_sheet.png (3000 x 2000)."""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cp007_committee_layout as Lo
W, H = 3000, 2000; random.seed(1850)
im = Image.new("RGB", (W, H), (226, 214, 186)); d = ImageDraw.Draw(im)
# paper mottling
for _ in range(900):
    x, y, r = random.randint(0, W), random.randint(0, H), random.randint(20, 160)
    c = random.randint(-9, 6); d.ellipse((x - r, y - r, x + r, y + r), fill=(226 + c, 213 + c, 184 + c))
im = im.filter(ImageFilter.GaussianBlur(40)); d = ImageDraw.Draw(im)
S = 1.22; OX, OY = 158, 1330                       # px per ft, origin (u=0, v=0)
def P(u, v): return (OX + u * S, OY - v * S)
INK = (52, 40, 30); RED = (140, 52, 38); WASH = (196, 176, 150)
def line(a, b, w=3, c=INK): d.line([P(*a), P(*b)], fill=c, width=w)
# roads (dashed) and Rotten Row
for v in (Lo.ROAD_DRIVE_V - 18, Lo.ROAD_DRIVE_V + 18):
    for u in range(-60, 2260, 40): line((u, v), (u + 24, v), 3)
for v in (Lo.ROAD_KENS_V - 25, Lo.ROAD_KENS_V + 25): line((-60, v), (2260, v), 4)
for v in (Lo.ROTTEN_ROW_V + 20, Lo.ROTTEN_ROW_V + 90): line((-60, v), (2260, v + 25), 4)
# building fill + outline
poly = [(0, 0), (Lo.L, 0)]
for (a, b, v) in reversed(Lo.NORTH): poly += [(b, v), (a, v)]
d.polygon([P(*p) for p in poly], fill=WASH, outline=INK)
d.line([P(*p) for p in poly + [poly[0]]], fill=INK, width=7)
# avenue strips with columns at 24 ft
for (u0, u1, v0, v1) in Lo.strips():
    line((u0, v0), (u0, v1), 2)
    for v in range(int(v0), int(v1), 24):
        for u in (u0 + 24, u0 + 0.5):
            x, y = P(u, v); d.rectangle((x - 3, y - 3, x + 3, y + 3), fill=INK)
# main avenue
line((20, Lo.MAIN_V[0]), (Lo.ROT_U - 97, Lo.MAIN_V[0]), 4); line((20, Lo.MAIN_V[1]), (Lo.ROT_U - 97, Lo.MAIN_V[1]), 4)
line((Lo.ROT_U + 97, Lo.MAIN_V[0]), (Lo.L - 20, Lo.MAIN_V[0]), 4); line((Lo.ROT_U + 97, Lo.MAIN_V[1]), (Lo.L - 20, Lo.MAIN_V[1]), 4)
# rotunda
cx, cy = P(Lo.ROT_U, Lo.ROT_V); r = Lo.ROT_R * S
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(232, 222, 198), outline=INK, width=8)
d.ellipse((cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14), outline=INK, width=3)
# courts
for (a, b, c, e, k) in Lo.COURTS:
    d.rectangle((P(a, e)[0], P(a, e)[1], P(b, c)[0], P(b, c)[1]), fill=(218, 206, 178), outline=INK, width=5)
for (u, v, cr, h) in Lo.TREES:
    x, y = P(u, v); rr = cr * S
    d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=(70, 80, 50), width=3)
    for k in range(-int(rr), int(rr), 9): d.line((x + k - rr * 0.3, y - rr * 0.5, x + k + rr * 0.3, y + rr * 0.5), fill=(90, 98, 70), width=2)
# pavilions
for (u, v, f, w, *_r) in Lo.PAVILIONS:
    if f in "SN": a = P(u - w / 2, v + (12 if f == "N" else -24)); b = P(u + w / 2, v + (12 + 16 if f == "N" else 0))
    else: a = P(u - (20 if f == "W" else 0), v + w / 2); b = P(u + (20 if f == "E" else 0), v - w / 2)
    d.rectangle((min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])), fill=RED, outline=INK, width=4)
# pent roof line along the south front
line((0, -15), (Lo.L, -15), 2, RED)
try:
    F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 70); F2 = ImageFont.truetype("/usr/share/fonts/truetype/sand-box/google/IBM Plex Serif/IBMPlexSerif-SemiBoldItalic.ttf", 50)
except OSError:
    F = F2 = ImageFont.load_default()
d.text((W / 2, 110), "GROUND PLAN OF THE BUILDING COMMITTEE'S DESIGN", fill=INK, font=F, anchor="mm")
d.text((W / 2, 190), "Hyde Park, June 1850  --  interpretive study drawing, not a facsimile", fill=INK, font=F2, anchor="mm")
# scale bar 0-500 ft
x0, y0 = 1950, 1880
for k in range(6):
    d.rectangle((x0 + k * 100 * S, y0, x0 + (k + 1) * 100 * S, y0 + 18), fill=INK if k % 2 == 0 else (226, 214, 186), outline=INK)
d.text((x0, y0 - 40), "0", fill=INK, font=F2, anchor="mm"); d.text((x0 + 600 * S, y0 - 40), "600 ft", fill=INK, font=F2, anchor="mm")
d.rectangle((40, 40, W - 40, H - 40), outline=INK, width=6)
out = os.path.join(os.path.dirname(HERE), "textures", "cp007_committee_plan_sheet.png"); im.save(out); print("SHEET", out)
