#!/usr/bin/env python3
"""Compose renders/compare.png: render beside photograph, for both faces."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(BASE, "renders")
REFS = os.path.join(BASE, "refs")
CELL = 760

def disc_crop(path, box=None):
    im = Image.open(path).convert("RGB")
    if box:
        im = im.crop(box)
    # centre-crop to square then resize
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
    return im.resize((CELL, CELL))

panels = [
    (disc_crop(os.path.join(R, "front.png"), box=(115, 195, 785, 865)), "Model - obverse render"),
    (disc_crop(os.path.join(REFS, "1851_Medal_Crystal_Palace_World_Expo_London,_obverse.jpg")),
     "Photograph - obverse (CC BY-SA 3.0)"),
    (disc_crop(os.path.join(R, "reverse.png"), box=(115, 195, 785, 865)), "Model - reverse render"),
    (disc_crop(os.path.join(REFS, "1851_Medal_Crystal_Palace_World_Expo_London,_reverse.jpg")),
     "Photograph - reverse (CC BY-SA 3.0)"),
]
sheet = Image.new("RGB", (CELL * 2, (CELL + 34) * 2), (24, 24, 24))
d = ImageDraw.Draw(sheet)
try:
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except Exception:
    f = ImageFont.load_default()
for i, (im, label) in enumerate(panels):
    x = (i % 2) * CELL
    y = (i // 2) * (CELL + 34)
    sheet.paste(im, (x, y + 34))
    d.text((x + 12, y + 6), label, font=f, fill=(235, 235, 235))
sheet.save(os.path.join(R, "compare.png"))
print("compare.png saved", sheet.size)
