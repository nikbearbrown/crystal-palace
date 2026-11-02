"""KEEP CP031 strike pairs (2026-11-02): pre-KEEP live d04 (before) vs live d04 after promotion + maul-face nudge.
python3 scripts/make_cp031_keep_pairs.py   (run after scripts/render_cp031_live.sh)
Same layouts as the candidate pairs: side-by-side 1280+12+1280, and a 2x lateral crop of box (100,0,420,240)."""
import os, shutil
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PG = "/workspace/crystal-palace-survey/look/pairs_geo"
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
except OSError:
    FONT = ImageFont.load_default()


def label(im, text):
    d = ImageDraw.Draw(im); w = int(d.textlength(text, font=FONT)) + 12
    d.rectangle((0, 0, w, 21), fill=(0, 0, 0)); d.text((6, 2), text, fill=(255, 255, 255), font=FONT)
    return im


def pair(a, b, la, lb, out):
    w, h = a.size; o = Image.new("RGB", (w * 2 + 12, h), (255, 255, 255))
    o.paste(label(a.copy(), la), (0, 0)); o.paste(label(b.copy(), lb), (w + 12, 0)); o.save(out)


LA, LB = "BEFORE pre-KEEP live d04", "AFTER live d04 (KEEP 2026-11-02, maul face on key)"
for s in ("key_strike_start", "lateral_start"):
    live = os.path.join(HERE, "renders/d04/CP031_%s.png" % s)
    shutil.copyfile(live, os.path.join(PG, "KEEP_CP031_strike_%s_after.png" % s))
    a = Image.open(os.path.join(PG, "KEEP_CP031_strike_%s_before.png" % s)).convert("RGB")
    b = Image.open(live).convert("RGB")
    pair(a, b, LA, LB, os.path.join(PG, "KEEP_CP031_strike_%s_pair.png" % s))
    if s == "lateral_start":
        box = (100, 0, 420, 240)
        ca = a.crop(box).resize((640, 480), Image.LANCZOS); cb = b.crop(box).resize((640, 480), Image.LANCZOS)
        pair(ca, cb, "BEFORE lateral crop 2x", "AFTER (KEEP) lateral crop 2x", os.path.join(PG, "KEEP_CP031_strike_lateral_detail_pair.png"))
print("pairs written to", PG)
