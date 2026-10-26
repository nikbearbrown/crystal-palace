"""
Build renders/compare.png: the reference photograph's Farnese Bull crop
beside the model's photomatch render (the album photograph was taken
from an elevated rear-left viewpoint; the photomatch camera approximates
that viewpoint). Run with system python3 (PIL) after the build script.
"""

import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

album = Image.open(os.path.join(ROOT, "refs", "album-DP323102.jpg"))
W, H = album.size
# Farnese Bull group close-up within the bottom-left album photograph
ref = album.crop((int(0.240 * W), int(0.660 * H), int(0.395 * W), int(0.820 * H)))
ref = ref.convert("RGB")

model = Image.open(os.path.join(ROOT, "renders", "photomatch.png")).convert("RGB")

th = 900
ref = ref.resize((int(ref.width * th / ref.height), th))
model = model.resize((int(model.width * th / model.height), th))

bar = 34
canvas = Image.new("RGB", (ref.width + model.width + 24, th + bar), (245, 245, 245))
canvas.paste(ref, (0, bar))
canvas.paste(model, (ref.width + 24, bar))
d = ImageDraw.Draw(canvas)
d.text((8, 10), "REFERENCE: Delamotte album photo, Greek & Roman Court (CC0) - group seen from rear-left", fill=(20, 20, 20))
d.text((ref.width + 32, 10), "MODEL: photomatch view - MASSING ONLY, loose interpretation", fill=(20, 20, 20))
canvas.save(os.path.join(ROOT, "renders", "compare.png"))
print("wrote renders/compare.png", canvas.size)
