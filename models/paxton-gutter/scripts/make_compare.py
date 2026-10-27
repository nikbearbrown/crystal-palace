#!/usr/bin/env python3
"""Side-by-side compares: render end sections vs the Downes plate sections."""
from PIL import Image, ImageDraw

BASE = "/home/hatch/workspace/cp-models/paxton-gutter/"
H = 950

def panel(path, label):
    im = Image.open(path).convert("RGB")
    im = im.resize((int(im.width * H / im.height), H))
    canvas = Image.new("RGB", (im.width, H + 44), (24, 24, 24))
    canvas.paste(im, (0, 44))
    ImageDraw.Draw(canvas).text((12, 14), label, fill=(255, 255, 255))
    return canvas

def compare(render, plate, label_r, label_p, out):
    a = panel(render, label_r)
    b = panel(plate, label_p)
    both = Image.new("RGB", (a.width + b.width + 12, H + 44), (24, 24, 24))
    both.paste(a, (0, 0))
    both.paste(b, (a.width + 12, 0))
    both.save(BASE + "renders/" + out, quality=90)
    print("wrote", out, both.size)

compare(BASE + "renders/end-section-paxton.png",
        BASE + "refs/plate-012-fig10-gutter-section.png",
        "Model: Paxton gutter end section",
        "Downes Plate XII Fig. 10 (detail)",
        "compare-paxton-section.jpg")
compare(BASE + "renders/end-section-main.png",
        BASE + "refs/plate-013-fig2-main-gutter-section.png",
        "Model: main gutter end section",
        "Downes Plate XIII Fig. 2, section at i.i",
        "compare-main-section.jpg")
