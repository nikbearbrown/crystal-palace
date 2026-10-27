#!/usr/bin/env python3
"""Assemble renders/compare.jpg: Delamotte facade photograph (crop) beside the
photo-match render, same height, labelled."""
from PIL import Image, ImageDraw
import os

BASE = os.path.expanduser("~/workspace/cp-models/assyrian-lamassu")
photo = Image.open(os.path.join(BASE, "refs/album-sheet-MET_DP323102.jpg"))
# facade photograph, then tighten on the nearest bull (right-hand bull of the row)
facade = photo.crop((375, 485, 1315, 1415))
bull = facade.crop((250, 120, 720, 880))
render = Image.open(os.path.join(BASE, "renders/photo-match.png")).convert("RGB")

H = 760
def fit(im):
    w = int(im.size[0] * H / im.size[1])
    return im.resize((w, H), Image.LANCZOS)

bull = fit(bull)
render = fit(render)
W = bull.size[0] + render.size[0] + 30
canvas = Image.new("RGB", (W, H + 34), (40, 40, 40))
canvas.paste(bull, (0, 34))
canvas.paste(render, (bull.size[0] + 30, 34))
d = ImageDraw.Draw(canvas)
d.text((10, 10), "REFERENCE: Delamotte photograph, Nineveh Court facade (CC0)", fill=(255, 255, 255))
d.text((bull.size[0] + 40, 10), "MODEL: photo-match render", fill=(255, 255, 255))
canvas.save(os.path.join(BASE, "renders/compare.jpg"), quality=90)
print("compare.jpg", canvas.size)
