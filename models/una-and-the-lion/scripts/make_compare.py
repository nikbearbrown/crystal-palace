"""Compose renders/compare.png: reference stereograph (right-eye view)
beside the model's photomatch render, matched height, with labels."""
from PIL import Image, ImageDraw
import os

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

ref = Image.open(os.path.join(BASE, "refs", "stereograph-una-and-the-lion-DP700246.jpg"))
# right-eye view window of the stereograph card
photo = ref.crop((1790, 520, 2680, 1560))
render = Image.open(os.path.join(BASE, "renders", "photomatch.png")).convert("RGB")

H = 1000
photo = photo.resize((int(photo.width * H / photo.height), H), Image.LANCZOS)
render = render.resize((int(render.width * H / render.height), H), Image.LANCZOS)

pad, label_h = 16, 44
out = Image.new("RGB", (photo.width + render.width + pad * 3,
                        H + label_h + pad), (24, 24, 24))
out.paste(photo, (pad, pad))
out.paste(render, (pad * 2 + photo.width, pad))
d = ImageDraw.Draw(out)
d.text((pad + 6, H + pad + 10),
       "REFERENCE: stereograph DP700246 (CC0, MET) - Sydenham display, 3/4 view",
       fill=(230, 230, 230))
d.text((pad * 2 + photo.width + 6, H + pad + 10),
       "MODEL: photomatch render, same viewpoint (approx.)",
       fill=(230, 230, 230))
out.save(os.path.join(BASE, "renders", "compare.png"))
print("compare.png written", out.size)
