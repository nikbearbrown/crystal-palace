#!/usr/bin/env python3
"""Side-by-side compare sheets: render vs Talbot photograph crops."""
from PIL import Image
import os

D = os.path.expanduser("~/workspace/cp-models/seed-drill")

def sheet(render_path, photo_path, crop, out_name, label_r, label_p):
    r = Image.open(render_path).convert("RGB")
    p = Image.open(photo_path).convert("RGB")
    x0, y0, x1, y1 = crop
    p = p.crop((int(x0 * p.width), int(y0 * p.height), int(x1 * p.width), int(y1 * p.height)))
    H = 560
    def fit(im):
        return im.resize((int(im.width * H / im.height), H), Image.LANCZOS)
    r, p = fit(r), fit(p)
    from PIL import ImageDraw
    sheet = Image.new("RGB", (r.width + p.width + 12, H + 26), (40, 40, 40))
    sheet.paste(r, (0, 26))
    sheet.paste(p, (r.width + 12, 26))
    d = ImageDraw.Draw(sheet)
    d.text((8, 7), label_r, fill=(255, 255, 255))
    d.text((r.width + 20, 7), label_p, fill=(255, 255, 255))
    out = os.path.join(D, "renders", out_name)
    sheet.save(out)
    print("SAVED", out, sheet.size)

# plate 1 angle: rear-left three-quarter vs Garrett plate crop
sheet(os.path.join(D, "renders", "rear-three-quarter.png"),
      os.path.join(D, "refs", "talbot-agricultural-implements-1.jpg"),
      (0.03, 0.50, 0.37, 0.83), "compare-plate1.jpg",
      "MODEL rear-left 3/4", "PHOTO Talbot plate 1 (Garrett), 1851")
# plate 2 angle: front-right vs Hornsby plate crop
sheet(os.path.join(D, "renders", "plate2-angle.png"),
      os.path.join(D, "refs", "talbot-agricultural-implements-2.jpg"),
      (0.565, 0.545, 0.905, 0.765), "compare-plate2.jpg",
      "MODEL front-right", "PHOTO Talbot plate 2 (Hornsby), 1851")
