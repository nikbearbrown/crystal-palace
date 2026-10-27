#!/usr/bin/env python3
"""Comparison image for alhambra-lion-fountain:
left  — the fountain region of the coloured print "Entrance to the
        Alhambra Court" (enlarged from refs/Crystal_Palace_Alhambra_Court.jpg)
right — the front render.
Run AFTER renders exist.
"""
import os
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(BASE, "refs")
OUT = os.path.join(BASE, "renders")


def side_by_side(left_path, right_path, out_path, height=1500):
    L = Image.open(left_path).convert("RGB")
    R = Image.open(right_path).convert("RGB")
    L = L.resize((round(L.width * height / L.height), height))
    R = R.resize((round(R.width * height / R.height), height))
    canvas = Image.new("RGB", (L.width + R.width + 12, height), (128, 128, 128))
    canvas.paste(L, (0, 0))
    canvas.paste(R, (L.width + 12, 0))
    canvas.save(out_path, quality=88)
    print("wrote", out_path, canvas.size)


crop = os.path.join(REFS, "crop-fountain-region.png")
if not os.path.exists(crop):
    im = Image.open(os.path.join(REFS, "Crystal_Palace_Alhambra_Court.jpg"))
    w, h = im.size
    c = im.crop((int(w * 0.06), int(h * 0.48), int(w * 0.52), int(h * 0.94)))
    c = c.resize((c.width * 4, c.height * 4), Image.LANCZOS)
    c.save(crop)

side_by_side(crop, os.path.join(OUT, "front.png"),
             os.path.join(OUT, "compare.jpg"))
print("COMPARE DONE")
