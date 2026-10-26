"""Gridded crop of a plate in full-resolution plate coordinates, for reading a figure by eye.

  python3 -I tools/gridcrop.py plate-015.jpg X0 Y0 X1 Y1 SCALE OUT.jpg [GRID]

Crops the working JPEG (source-scans/plates/<plate>) to x X0..X1, y Y0..Y1, scales it by SCALE and draws a tick and a
number every GRID plate pixels (default 100) along the top (red, x) and left (blue, y). Read positions off the numbers,
not off the picture's own pixels, and then put them in a script. The numbers are PLATE pixels at any SCALE, so a reading
never needs correcting for the zoom. Write OUT outside the repo (a scratch folder).
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None
PLATES = Path(__file__).resolve().parents[2] / "source-scans" / "plates"
if len(sys.argv) < 8:
    sys.exit(__doc__)
plate, x0, y0, x1, y1 = sys.argv[1], *(int(v) for v in sys.argv[2:6])
scale, out = float(sys.argv[6]), sys.argv[7]
step = int(sys.argv[8]) if len(sys.argv) > 8 else 100
im = Image.open(PLATES / plate).convert("RGB").crop((x0, y0, x1, y1))
im = im.resize((int((x1 - x0) * scale), int((y1 - y0) * scale)), Image.LANCZOS)
d = ImageDraw.Draw(im)
for x in range((x0 // step + 1) * step, x1, step):
    X = (x - x0) * scale
    d.line([(X, 0), (X, 14)], fill=(255, 0, 0), width=2)
    d.text((X + 2, 14), str(x), fill=(255, 0, 0))
for y in range((y0 // step + 1) * step, y1, step):
    Y = (y - y0) * scale
    d.line([(0, Y), (14, Y)], fill=(0, 0, 255), width=2)
    d.text((16, Y - 5), str(y), fill=(0, 0, 255))
im.save(out, quality=88)
print(out, im.size)
