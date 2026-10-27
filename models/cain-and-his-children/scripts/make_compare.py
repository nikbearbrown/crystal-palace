"""Compose renders/compare.png: the stereograph's left-eye frontal
view beside the model's photomatch render, matched height, labelled."""
from PIL import Image, ImageDraw
import os

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

ref = Image.open(os.path.join(BASE, "refs", "cain-stereograph.jpg"))
w, h = ref.size
# left-eye view, statue area (fractions measured on the card)
photo = ref.crop((int(w * 0.5 * 0.27), int(h * 0.13),
                  int(w * 0.5 * 0.90), int(h * 0.84)))
render = Image.open(os.path.join(BASE, "renders", "photomatch.png")).convert("RGB")

H = 780
photo = photo.resize((int(photo.width * H / photo.height), H), Image.LANCZOS)
render = render.resize((int(render.width * H / render.height), H), Image.LANCZOS)

pad, label_h = 16, 44
out = Image.new("RGB", (photo.width + render.width + pad * 3,
                        H + label_h + pad), (24, 24, 24))
out.paste(photo, (pad, pad))
out.paste(photo, (pad, pad))
out.paste(render, (pad * 2 + photo.width, pad))
d = ImageDraw.Draw(out)
d.text((pad + 6, H + pad + 10),
       "REFERENCE: stereograph RP-F-2012-96-336 (CC0, Rijksmuseum) - Sydenham sculpture gallery, frontal",
       fill=(230, 230, 230))
d.text((pad * 2 + photo.width + 6, H + pad + 10),
       "MODEL: photomatch render, same viewpoint (approx.)",
       fill=(230, 230, 230))
out.save(os.path.join(BASE, "renders", "compare.png"))
print("compare.png written", out.size)
