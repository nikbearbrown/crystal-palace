"""interpretive engineering sheet for CP009 (column / connecting piece / girder elevation), Grok. python3 scripts/make_drawing.py"""
from PIL import Image, ImageDraw, ImageFont
import os
W, H = 2400, 1600; im = Image.new("RGB", (W, H), (226, 219, 198)); d = ImageDraw.Draw(im)
ink = (40, 44, 62); red = (150, 50, 40)
try: F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 44); f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 30)
except Exception: F = f2 = ImageFont.load_default()
d.rectangle([40, 40, W - 40, H - 40], outline=ink, width=6); d.rectangle([60, 60, W - 60, H - 60], outline=ink, width=2)
s = 26  # px per inch-ish: column 8 in = 208 px
cx = 700; top = 250
# column, connecting piece and stub (elevation)
d.rectangle([cx - 104, top, cx + 104, top + 380], outline=ink, width=4)                  # upper column
d.rectangle([cx - 140, top + 380, cx + 140, top + 410], outline=ink, width=4)            # flange
d.rectangle([cx - 104, top + 410, cx + 104, top + 410 + 600], outline=ink, width=4)      # connecting piece 3 ft 4 1/2
d.rectangle([cx - 140, top + 1010, cx + 140, top + 1040], outline=ink, width=4)
d.rectangle([cx - 104, top + 1040, cx + 104, top + 1250], outline=ink, width=4)
# girder (elevation), lattice
gx0, gx1, gy0, gy1 = cx + 104 + 8, W - 160, top + 430, top + 430 + 520
d.rectangle([gx0, gy0, gx1, gy0 + 24], outline=ink, width=4); d.rectangle([gx0, gy1 - 24, gx1, gy1], outline=ink, width=4)
n = 6; step = (gx1 - gx0) / n
for k in range(n + 1):
    x = gx0 + k * step; d.line([x, gy0, x, gy1], fill=ink, width=4)
    if k < n: d.line([x, gy0 + 24, x + step, gy1 - 24], fill=ink, width=3); d.line([x + step, gy0 + 24, x, gy1 - 24], fill=ink, width=3)
# key and wedge detail
for (y, lab) in ((gy0 - 40, "key"), (gy1 + 10, "wedge")):
    d.polygon([(gx0 + 30, y), (gx0 + 46, y), (gx0 + 52, y + 34), (gx0 + 24, y + 34)], outline=red, width=3)
# dimension lines
def dim(x0, y0, x1, y1, t, off=(10, -40)):
    d.line([x0, y0, x1, y1], fill=red, width=2)
    for (x, y) in ((x0, y0), (x1, y1)): d.line([x - 12, y - 12, x + 12, y + 12], fill=red, width=2)
    d.text(((x0 + x1) / 2 + off[0], (y0 + y1) / 2 + off[1]), t, fill=red, font=f2)
dim(cx - 220, top + 410, cx - 220, top + 1010, "3' 4 1/2\"", (-200, 0))
dim(gx1 + 50, gy0, gx1 + 50, gy1, "3' 0\"", (-150, 0))
dim(gx0, gy1 + 90, gx1, gy1 + 90, "24' 0\" bay", (-60, 10))
dim(cx - 104, top - 50, cx + 104, top - 50, "8\"", (-10, -50))
d.text((120, 100), "CAST IRON COLUMN, CONNECTING PIECE AND 24 FT GIRDER  -  ELEVATION", fill=ink, font=F)
d.text((120, H - 150), "Interpretive sheet for the film (after Downes 1852, Plate VIII).  Not a facsimile.", fill=ink, font=f2)
d.text((W - 640, H - 150), "Scale: 1 1/2 in to 1 ft", fill=ink, font=f2)
os.makedirs("textures", exist_ok=True); im.save("textures/drawing_cp009.png"); print("OK")
