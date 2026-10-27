#!/usr/bin/env python3
"""Stack the side photomatch render against the Talbot calotype crop.
  python3 scripts/make_compare.py
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ref = Image.open(os.path.join(
    ROOT, 'refs', 'Great_Exhibition_No_136_Folkstone_by_HF_Talbot_1851.jpg')).convert('RGB')
ref = ref.crop((210, 400, 2220, 1470))           # engine only
ren = Image.open(os.path.join(ROOT, 'renders', 'photomatch.png')).convert('RGB')

H = 620
def fit(im):
    return im.resize((int(im.width * H / im.height), H), Image.LANCZOS)
ref, ren = fit(ref), fit(ren)
W = max(ref.width, ren.width)
canvas = Image.new('RGB', (W, H * 2 + 46), (30, 30, 30))
canvas.paste(ref, ((W - ref.width) // 2, 0))
canvas.paste(ren, ((W - ren.width) // 2, H + 46))
d = ImageDraw.Draw(canvas)
d.text((12, H + 14), 'TOP: Talbot calotype, 1851 (PD)    BOTTOM: model, side photomatch',
       fill=(230, 230, 230))
canvas.save(os.path.join(ROOT, 'renders', 'compare.png'))
print('compare saved', canvas.size)
