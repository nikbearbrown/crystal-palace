#!/usr/bin/env python3
"""Generate the plate textures for the Folkestone model:
nameplate.png, makersplate.png, panel_lining.png (in ../textures/).
Plate corners are transparent so the textures sit on curved/flat
surfaces without a visible rectangular halo.
  python3 scripts/make_textures.py
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'textures')
os.makedirs(OUT, exist_ok=True)
FD = '/usr/share/fonts/truetype/dejavu'
SERIF_B = os.path.join(FD, 'DejaVuSerif-Bold.ttf')

# ---------- nameplate ----------
W, H = 1024, 512
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.ellipse([26, 26, W - 26, H - 26], fill=(196, 172, 120, 255), outline=(90, 72, 40, 255), width=10)
d.ellipse([52, 52, W - 52, H - 52], outline=(120, 98, 55, 255), width=4)
ink = (38, 30, 18, 255)
d.text((W / 2, 208), 'FOLKSTONE', font=ImageFont.truetype(SERIF_B, 118), fill=ink, anchor='mm')
d.text((W / 2, 356), '1851', font=ImageFont.truetype(SERIF_B, 96), fill=ink, anchor='mm')
for sx in (92, W - 92):
    d.ellipse([sx - 13, 196, sx + 13, 222], fill=ink)
img.save(os.path.join(OUT, 'nameplate.png'))

# ---------- maker's plate ----------
W, H = 1024, 660
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.ellipse([22, 22, W - 22, H - 22], fill=(198, 176, 124, 255), outline=(90, 72, 40, 255), width=10)
d.ellipse([48, 48, W - 48, H - 48], outline=(120, 98, 55, 255), width=4)
ink = (38, 30, 18, 255)
cx, cy = W / 2, H / 2

def ellipse_points(a, b, phi0, phi1, steps=400):
    return [(cx + a * math.cos(phi0 + (phi1 - phi0) * i / steps),
             cy - b * math.sin(phi0 + (phi1 - phi0) * i / steps))
            for i in range(steps + 1)]

def place_along(pts, text, font):
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    total = cum[-1]
    n = len(text)
    for i, ch in enumerate(text):
        target = total * (i + 0.5) / n
        j = min(range(len(cum)), key=lambda k: abs(cum[k] - target))
        x, y = pts[j]
        j2 = min(j + 1, len(pts) - 1); j1 = max(j - 1, 0)
        ang = math.degrees(math.atan2(pts[j2][1] - pts[j1][1], pts[j2][0] - pts[j1][0]))
        tile = Image.new('RGBA', (110, 110), (0, 0, 0, 0))
        ImageDraw.Draw(tile).text((55, 55), ch, font=font, fill=ink, anchor='mm')
        tile = tile.rotate(-ang, resample=Image.BICUBIC, center=(55, 55))
        img.paste(tile, (int(x - 55), int(y - 55)), tile)

fa = ImageFont.truetype(SERIF_B, 38)
place_along(ellipse_points(384, 210, math.radians(156), math.radians(24)),
            'STEPHENSON & Co ENGINEERS NEWCASTLE', fa)
place_along(ellipse_points(384, 210, math.radians(204), math.radians(336)),
            'CRAMPTON PATENTEE', fa)
fl = ImageFont.truetype(SERIF_B, 46)
for txt, dy in [('SOUTH EASTERN RAILWAY', -62), ('LONDON TO PARIS', -8),
                ('FOLKSTONE & BOULOGNE', 42), ('& DOVOR & CALAIS', 88)]:
    d.text((cx, cy + dy), txt, font=fl, fill=ink, anchor='mm')
img.save(os.path.join(OUT, 'makersplate.png'))

# ---------- splasher panel lining ----------
W, H = 1400, 560
img = Image.new('RGB', (W, H), (13, 20, 16))
d = ImageDraw.Draw(img)
line = (196, 178, 128)
d.rectangle([30, 30, W - 30, H - 30], outline=line, width=5)
d.rectangle([58, 58, W - 58, H - 58], outline=line, width=3)
for (x0, y0, x1, y1, st) in [(58, 58, 190, 190, 180), (W - 190, 58, W - 58, 190, 270),
                             (W - 190, H - 190, W - 58, H - 58, 0), (58, H - 190, 190, H - 58, 90)]:
    d.arc([x0, y0, x1, y1], start=st, end=st + 90, fill=line, width=3)
img.save(os.path.join(OUT, 'panel_lining.png'))
print('textures written to', OUT)
