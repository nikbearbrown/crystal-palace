"""CP019 "The world arrives in cases" CANDIDATE (2026-11-16, DEPARTURES FT101-FT108): consignment marks for the packing cases and bales.
Painted-stencil marks in lamp black on transparent RGBA, one PNG per consignment -> textures/cp019_mark_<key>.png.
The marks are the period pattern (exhibitor's mark in a diamond, case number, port/town of origin, destination); the names and
numbers are staging (FT104), not catalogue entries.   python3 scripts/make_cp019_stencils.py"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, os, random
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = f"{H}/textures"; os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/truetype/sand-box/google/Barlow Condensed/BarlowCondensed-Bold.ttf"
MARKS = {   # key: (diamond initials, line 1 big, case no., line 3)
    "france":   ("C&F", "FRANCE", "No 287", "EXHIBITION  LONDON"),
    "zoll":     ("GH", "ZOLLVEREIN", "No 64", "HYDE PARK  LONDON"),
    "usa":      ("JW", "UNITED STATES", "No 412", "EXHIBITION  LONDON"),
    "india":    ("EIC", "INDIA", "No 33", "FROM CALCUTTA"),
    "belgique": ("VM", "BELGIQUE", "No 158", "EXHIBITION  LONDON"),
    "care":     ("", "WITH CARE", "No 1146", "THIS SIDE UP"),
    "bale":     ("T&S", "MANCHESTER", "No 9", "HYDE PARK"),
}
def mark(key, a, l1, no, l3, W=1024, Hh=640, seed=0):
    rnd = random.Random(seed); im = Image.new("L", (W, Hh), 0); d = ImageDraw.Draw(im)
    big = ImageFont.truetype(FONT, 150 if len(l1) <= 10 else 118); mid = ImageFont.truetype(FONT, 104); sm = ImageFont.truetype(FONT, 78)
    y = 30
    if a:
        cx, cy, r = W // 2, 120, 95
        d.polygon([(cx, cy - r), (cx + r * 1.45, cy), (cx, cy + r), (cx - r * 1.45, cy)], outline=255, width=14)
        f = ImageFont.truetype(FONT, 82); tw = d.textlength(a, font=f); d.text((cx - tw / 2, cy - 50), a, font=f, fill=255)
        y = 230
    for txt, f, dy in ((l1, big, 0), (no, mid, 0), (l3, sm, 0)):
        tw = d.textlength(txt, font=f); d.text(((W - tw) / 2, y), txt, font=f, fill=255); y += int(f.size * 1.02)
    a_ = np.asarray(im).astype(float) / 255.0
    noise = np.asarray(Image.effect_noise((W, Hh), 60).filter(ImageFilter.GaussianBlur(2))).astype(float) / 255.0
    a_ = np.clip(a_ * (0.55 + 0.6 * noise), 0, 1) * 0.92           # dry-brush stencil: patchy paint
    rgba = np.zeros((Hh, W, 4), np.uint8); rgba[..., 0] = 22; rgba[..., 1] = 18; rgba[..., 2] = 14; rgba[..., 3] = (a_ * 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(f"{OUT}/cp019_mark_{key}.png"); print("WROTE", key)
for i, (k, v) in enumerate(MARKS.items()): mark(k, *v, seed=i)
