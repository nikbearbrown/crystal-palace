#!/usr/bin/env python3
"""Side-by-side compare: the model's photomatch render against the
Garrett calotype crop (reference). Pure PIL, no Blender needed:
  python3 scripts/make_compare.py
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ref = Image.open(os.path.join(ROOT, 'refs', 'garrett-side.jpg')).convert('RGB')
W, H = ref.size
# crop to the engine only (as measured during the build)
crop = ref.crop((int(0.375 * W), int(0.295 * H), int(0.785 * W), int(0.80 * H)))
model = Image.open(os.path.join(ROOT, 'renders', 'photomatch.png')).convert('RGB')

th = 620
def fit(im):
    return im.resize((int(im.width * th / im.height), th), Image.LANCZOS)
crop, model = fit(crop), fit(model)
out = Image.new('RGB', (crop.width + model.width + 12, th), (255, 255, 255))
out.paste(crop, (0, 0))
out.paste(model, (crop.width + 12, 0))
out.save(os.path.join(ROOT, 'renders', 'compare.png'))
print('compare.png', out.size)
