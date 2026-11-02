"""CANDIDATE CP032 departure-hands pairs (2026-11-02, no verdict): live m02 (7 boxy STAFF_* stand-ins) vs candidate
m02_cp032people (people_lib v3.4 hero figures, dark fustian / black frock coat). Same render settings, no post
exposure adjustment.  python3 scripts/make_cp032_people_pairs.py DIR   (DIR/before, DIR/after)"""
import os, sys, shutil
from PIL import Image, ImageDraw, ImageFont, ImageStat
PG = "/workspace/crystal-palace-survey/look/pairs_geo"; D = sys.argv[1]; F = "CP032_departure_start.png"
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
except OSError:
    FONT = ImageFont.load_default()
def label(im, t):
    d = ImageDraw.Draw(im); w = int(d.textlength(t, font=FONT)) + 12
    d.rectangle((0, 0, w, 25), fill=(0, 0, 0)); d.text((6, 2), t, fill=(255, 255, 255), font=FONT); return im
def pair(a, b, la, lb, out):
    w, h = a.size; o = Image.new("RGB", (w * 2 + 12, h), (255, 255, 255))
    o.paste(label(a.copy(), la), (0, 0)); o.paste(label(b.copy(), lb), (w + 12, 0)); o.save(out)
bp = os.path.join(PG, "CANDIDATE_CP032_people_before.png"); ap = os.path.join(PG, "CANDIDATE_CP032_people_after.png")
shutil.copyfile(os.path.join(D, "before", F), bp); shutil.copyfile(os.path.join(D, "after", F), ap)
a = Image.open(bp).convert("RGB"); b = Image.open(ap).convert("RGB")
print("mean luma before %.2f after %.2f" % (ImageStat.Stat(a.convert("L")).mean[0], ImageStat.Stat(b.convert("L")).mean[0]))
pair(a, b, "BEFORE live m02 (STAFF stand-ins)", "AFTER candidate (v3.4 hero hands) - CANDIDATE", os.path.join(PG, "CANDIDATE_CP032_people_pair.png"))
box = (0, 300, 1100, 650)   # the seven departure hands, 1x
pair(a.crop(box), b.crop(box), "BEFORE detail", "AFTER detail - CANDIDATE", os.path.join(PG, "CANDIDATE_CP032_people_detail_pair.png"))
print("PAIRS_DONE")
