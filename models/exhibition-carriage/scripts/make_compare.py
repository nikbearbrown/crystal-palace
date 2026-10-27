#!/usr/bin/env python3
"""Side-by-side compare: side render vs the cropped plate-XXIV region that
holds the only carriage legible in the plate (small, occluded, seen through
the curtained opening at the left of the view)."""
from PIL import Image, ImageDraw

BASE = '/home/hatch/workspace/cp-models/exhibition-carriage'
render = Image.open(f'{BASE}/renders/side.png').convert('RGB')
ref = Image.open(f'{BASE}/refs/plate-xxiv-carriage-crop-4x.jpg').convert('RGB')

H = 750
render = render.resize((1000, H))
ref = ref.resize((int(ref.width * H / ref.height), H))

out = Image.new('RGB', (render.width + ref.width + 12, H + 34), (40, 40, 40))
out.paste(render, (0, 34))
out.paste(ref, (render.width + 12, 34))
d = ImageDraw.Draw(out)
d.text((10, 10), 'MODEL — side (round 3)', fill=(255, 255, 255))
d.text((render.width + 22, 10), 'PLATE XXIV crop — the carriage as drawn (occluded, distant)', fill=(255, 255, 255))
out.save(f'{BASE}/renders/compare.png')
print('compare saved', out.size)
