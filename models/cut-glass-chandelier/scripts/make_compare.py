#!/usr/bin/env python3
"""Side-by-side compare: engraving (left) vs front render (right),
matched by height. Output: renders/compare.png"""
import os
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
eng = Image.open(os.path.join(BASE, "refs", "Crystal_Palace00.jpg")).convert("RGB")
ren = Image.open(os.path.join(BASE, "renders", "front.png")).convert("RGB")

H = 1200
eng = eng.resize((int(eng.width * H / eng.height), H), Image.LANCZOS)
ren = ren.resize((int(ren.width * H / ren.height), H), Image.LANCZOS)
gap = 24
canvas = Image.new("RGB", (eng.width + gap + ren.width, H), (255, 255, 255))
canvas.paste(eng, (0, 0))
canvas.paste(ren, (eng.width + gap, 0))
canvas.save(os.path.join(BASE, "renders", "compare.png"))
print("compare.png", canvas.size)
