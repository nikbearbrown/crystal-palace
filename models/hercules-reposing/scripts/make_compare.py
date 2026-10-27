"""Side-by-side compare: photomatch render vs the stereograph.
Output: ../renders/compare.jpg"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

photo = Image.open(os.path.join(ROOT, "refs", "hercules-nave-stereograph.jpg")).convert("RGB")
w, h = photo.size
# right half of the stereo pair, statue region
photo = photo.crop((int(w * 0.615), int(h * 0.04), int(w * 0.885), int(h * 0.90)))

render = Image.open(os.path.join(ROOT, "renders", "photomatch.png")).convert("RGB")

H = 900
def fit(im):
    return im.resize((int(im.width * H / im.height), H), Image.LANCZOS)
photo, render = fit(photo), fit(render)
out = Image.new("RGB", (photo.width + render.width + 12, H), (40, 40, 40))
out.paste(photo, (0, 0))
out.paste(render, (photo.width + 12, 0))
out.save(os.path.join(ROOT, "renders", "compare.jpg"), quality=88)
print("[compare] saved", out.size)
