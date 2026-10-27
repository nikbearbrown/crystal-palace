"""Compose renders/compare.png: the reference photograph (foreground
animal) beside the model's photomatch render, matched height, labelled."""
from PIL import Image, ImageDraw
import os

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

ref = Image.open(os.path.join(BASE, "refs", "Iguanodon_Crystal_Palace.jpg")).convert("RGB")
# window on the FOREGROUND animal (the reclining browser, lower part of
# the frame; the standing second Iguanodon is partly in frame at left)
photo = ref.crop((0, 205, 1024, 704))
render = Image.open(os.path.join(BASE, "renders", "photomatch.png")).convert("RGB")

H = 760
photo = photo.resize((int(photo.width * H / photo.height), H), Image.LANCZOS)
render = render.resize((int(render.width * H / render.height), H), Image.LANCZOS)

pad, label_h = 16, 44
out = Image.new("RGB", (photo.width + render.width + pad * 3,
                        H + label_h + pad), (24, 24, 24))
out.paste(photo, (pad, pad))
out.paste(render, (pad * 2 + photo.width, pad))
d = ImageDraw.Draw(out)
d.text((pad + 6, H + pad + 10),
       "REFERENCE: Iguanodon_Crystal_Palace.jpg (CC BY-SA 2.0) - foreground animal, front 3/4",
       fill=(230, 230, 230))
d.text((pad * 2 + photo.width + 6, H + pad + 10),
       "MODEL: photomatch render, same viewpoint (approx.)",
       fill=(230, 230, 230))
out.save(os.path.join(BASE, "renders", "compare.png"))
print("compare.png written", out.size)
