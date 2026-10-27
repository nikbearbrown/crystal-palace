"""Compose renders/compare.png: the model's three-quarter render beside
a crop of Talbot's View of Eastern Nave showing the counter runs along
the left (south) side of the nave, matched height, labelled."""
from PIL import Image, ImageDraw
import os

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

ref = Image.open(os.path.join(BASE, "refs", "talbot-eastern-nave.jpg")).convert("RGB")
w, h = ref.size
# left-side counter runs with goods on top, mid-distance
photo = ref.crop((int(w * 0.05), int(h * 0.48), int(w * 0.36), int(h * 0.78)))
render = Image.open(os.path.join(BASE, "renders", "three-quarter.png")).convert("RGB")

H = 700
photo = photo.resize((int(photo.width * H / photo.height), H), Image.LANCZOS)
render = render.resize((int(render.width * H / render.height), H), Image.LANCZOS)

pad, label_h = 16, 44
out = Image.new("RGB", (photo.width + render.width + pad * 3,
                        H + label_h + pad), (24, 24, 24))
out.paste(photo, (pad, pad))
out.paste(render, (pad * 2 + photo.width, pad))
d = ImageDraw.Draw(out)
d.text((pad + 6, H + pad + 10),
       "REFERENCE: Talbot, View of Eastern Nave (1851) - counter runs, left side (PD)",
       fill=(230, 230, 230))
d.text((pad * 2 + photo.width + 6, H + pad + 10),
       "MODEL: one 12 ft run unit, three-quarter render",
       fill=(230, 230, 230))
out.save(os.path.join(BASE, "renders", "compare.png"))
print("compare.png written", out.size)
