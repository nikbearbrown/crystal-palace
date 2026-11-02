"""CANDIDATE CP031 stale-view pairs (2026-11-02, no verdict): pre-CP031 d04 (7b7171a, r09 stand-in) vs live d04
(dressed striker DM24 + maul nudge DM25). Both rendered by scripts/render_cp031_stale.sh with identical settings
(x05 host, 1280x720, 24 spp, look exposure) — no post exposure adjustment.
python3 scripts/make_cp031_stale_pairs.py BEFORE_DIR"""
import os, sys, shutil
from PIL import Image, ImageDraw, ImageFont, ImageStat
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PG = "/workspace/crystal-palace-survey/look/pairs_geo"
BEF = sys.argv[1]
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
except OSError:
    FONT = ImageFont.load_default()
def label(im, text):
    d = ImageDraw.Draw(im); w = int(d.textlength(text, font=FONT)) + 12
    d.rectangle((0, 0, w, 21), fill=(0, 0, 0)); d.text((6, 2), text, fill=(255, 255, 255), font=FONT); return im
def pair(a, b, la, lb, out):
    w, h = a.size; o = Image.new("RGB", (w * 2 + 12, h), (255, 255, 255))
    o.paste(label(a.copy(), la), (0, 0)); o.paste(label(b.copy(), lb), (w + 12, 0)); o.save(out)
VIEWS = {"joint_detail": "CP031_joint_detail_start", "lateral_end": "CP031_lateral_end",
         "lateral_end_dusk": "CP031_lateral_end_dusk", "aerial": "REV_dismantle_aerial_start"}
for v, f in VIEWS.items():
    bp = os.path.join(PG, "CANDIDATE_CP031_stale_%s_before.png" % v); ap = os.path.join(PG, "CANDIDATE_CP031_stale_%s_after.png" % v)
    shutil.copyfile(os.path.join(BEF, f + ".png"), bp); shutil.copyfile(os.path.join(HERE, "renders/d04", f + ".png"), ap)
    a = Image.open(bp).convert("RGB"); b = Image.open(ap).convert("RGB")
    print(v, "mean luma before %.2f after %.2f" % (ImageStat.Stat(a.convert("L")).mean[0], ImageStat.Stat(b.convert("L")).mean[0]))
    pair(a, b, "BEFORE d04 pre-CP031 (r09 stand-in)", "AFTER live d04 (dressed striker) — CANDIDATE", os.path.join(PG, "CANDIDATE_CP031_stale_%s_pair.png" % v))
# detail: joint_detail upper-right (striker head, hands, maul head on the key), box (500,0,1280,500) at 1x
a = Image.open(os.path.join(PG, "CANDIDATE_CP031_stale_joint_detail_before.png")).convert("RGB").crop((500, 0, 1280, 500))
b = Image.open(os.path.join(PG, "CANDIDATE_CP031_stale_joint_detail_after.png")).convert("RGB").crop((500, 0, 1280, 500))
pair(a, b, "BEFORE joint_detail crop", "AFTER joint_detail crop — CANDIDATE", os.path.join(PG, "CANDIDATE_CP031_stale_joint_detail_detail_pair.png"))
