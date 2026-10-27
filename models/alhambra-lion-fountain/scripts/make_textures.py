#!/usr/bin/env python3
"""Generate the basin fascia texture for alhambra-lion-fountain.

Abstract stepped-knot block pattern (NO letterforms): the 1856 guide
(p.69) says an Arabic poem runs round the Granada basin; the Sydenham
print shows a patterned band but resolves no characters. Following the
sy-alhambra-ornament-panel precedent in this repo, the band is drawn as
interlocking stepped knot-blocks, not invented calligraphy.
Output: textures/fascia_band.png (colour) — also used as bump source.
"""
import os
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "textures")
os.makedirs(OUT, exist_ok=True)

W, H = 1024, 160  # one repeat = one basin side (texture repeats 12x around)
img = Image.new("RGB", (W, H), (168, 148, 118))  # warm stone band
d = ImageDraw.Draw(img)

# border rules top and bottom
d.rectangle([0, 0, W, 10], fill=(96, 78, 58))
d.rectangle([0, H - 10, W, H], fill=(96, 78, 58))
d.rectangle([0, 16, W, 20], fill=(120, 98, 70))
d.rectangle([0, H - 20, W, H - 16], fill=(120, 98, 70))

ink = (88, 68, 48)
lite = (196, 176, 140)

def knot(cx, cy, s):
    """Stepped square-knot motif: nested stepped squares + centre diamond."""
    # outer stepped square
    pts = [(cx - s, cy - s // 2), (cx - s // 2, cy - s // 2), (cx - s // 2, cy - s),
           (cx + s // 2, cy - s), (cx + s // 2, cy - s // 2), (cx + s, cy - s // 2),
           (cx + s, cy + s // 2), (cx + s // 2, cy + s // 2), (cx + s // 2, cy + s),
           (cx - s // 2, cy + s), (cx - s // 2, cy + s // 2), (cx - s, cy + s // 2)]
    d.polygon(pts, outline=ink, width=7)
    d.polygon([(cx, cy - s // 2), (cx + s // 2, cy), (cx, cy + s // 2), (cx - s // 2, cy)],
              outline=lite, width=5)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=ink)

# three knot blocks per side, linked by a running stepped fret
for i, cx in enumerate((170, 512, 854)):
    knot(cx, H // 2, 52)
for x in range(0, W, 64):
    d.polygon([(x, H // 2 - 14), (x + 32, H // 2 + 14), (x + 64, H // 2 - 14)],
              outline=(120, 98, 70), width=4)

img.save(os.path.join(OUT, "fascia_band.png"))
print("wrote", os.path.join(OUT, "fascia_band.png"), img.size)
