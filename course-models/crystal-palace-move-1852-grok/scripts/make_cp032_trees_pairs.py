"""CANDIDATE CP032 parkland trees + meadow (+ timber, hats) pairs (2026-11-02, no verdict; MV19): live m02 vs candidate m02_cp032trees.
Same cameras and render settings, no post exposure adjustment.
python3 scripts/make_cp032_trees_pairs.py DIR   (DIR/before, DIR/after)"""
import os, sys, shutil
from PIL import Image, ImageDraw, ImageFont, ImageStat
PG = "/workspace/crystal-palace-survey/look/pairs_geo"; D = sys.argv[1]
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except OSError:
    FONT = ImageFont.load_default()
def label(im, t):
    d = ImageDraw.Draw(im); w = int(d.textlength(t, font=FONT)) + 12
    d.rectangle((0, 0, w, 30), fill=(0, 0, 0)); d.text((6, 3), t, fill=(255, 255, 255), font=FONT); return im
def pair(a, b, la, lb, out):
    w, h = a.size; o = Image.new("RGB", (w * 2 + 12, h), (255, 255, 255))
    o.paste(label(a.copy(), la), (0, 0)); o.paste(label(b.copy(), lb), (w + 12, 0)); o.save(out)
for shot, tag in (("CP032_arrival_start", "start"), ("CP032_arrival_end", "end")):
    stem = os.path.join(PG, "CANDIDATE_CP032_trees_%s" % tag)
    shutil.copyfile(os.path.join(D, "before", shot + ".png"), stem + "_before.png")
    shutil.copyfile(os.path.join(D, "after", shot + ".png"), stem + "_after.png")
    a = Image.open(stem + "_before.png").convert("RGB"); b = Image.open(stem + "_after.png").convert("RGB")
    h = a.size[1]; lo = (0, int(h * 0.6), a.size[0], h)
    print("%s mean luma before %.2f after %.2f | lower 40%% before %.2f after %.2f" % (shot,
          ImageStat.Stat(a.convert("L")).mean[0], ImageStat.Stat(b.convert("L")).mean[0],
          ImageStat.Stat(a.crop(lo).convert("L")).mean[0], ImageStat.Stat(b.crop(lo).convert("L")).mean[0]))
    pair(a, b, "BEFORE live m02", "AFTER candidate (parkland oaks, meadow, timber, hats) - CANDIDATE", stem + "_pair.png")
print("PAIRS_DONE")
