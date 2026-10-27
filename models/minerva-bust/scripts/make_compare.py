#!/usr/bin/env python3
"""Compose renders/compare.jpg: the stereograph crop (left) beside the
photomatch render (right), same height."""
import os
from PIL import Image

BASE = os.path.expanduser("~/workspace/cp-models/minerva-bust")
photo = Image.open(os.path.join(BASE, "refs", "crop-minerva-bust.png")).convert("RGB")
render = Image.open(os.path.join(BASE, "renders", "photomatch.png")).convert("RGB")
h = 1100
photo = photo.resize((int(photo.width * h / photo.height), h), Image.LANCZOS)
render = render.resize((int(render.width * h / render.height), h), Image.LANCZOS)
out = Image.new("RGB", (photo.width + render.width + 12, h), (24, 24, 24))
out.paste(photo, (0, 0))
out.paste(render, (photo.width + 12, 0))
out.save(os.path.join(BASE, "renders", "compare.jpg"), quality=88)
print("compare.jpg", out.size)
