#!/usr/bin/env python3
"""Side-by-side compare: 3/4 render vs the source engraving."""
from PIL import Image

base = '/home/hatch/workspace/cp-models/glazing-wagon'
eng = Image.open(f'{base}/refs/Glazing_waggon.png').convert('RGB')
ren = Image.open(f'{base}/renders/compare.png').convert('RGB')

h = 560
def fit(im):
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)

eng, ren = fit(eng), fit(ren)
canvas = Image.new('RGB', (eng.width + ren.width + 12, h), (255, 255, 255))
canvas.paste(eng, (0, 0))
canvas.paste(ren, (eng.width + 12, 0))
canvas.save(f'{base}/renders/compare-engraving.jpg', quality=88)
print('compare saved', canvas.size)
