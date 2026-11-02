"""Build the CP028 drive v2 review pairs (same layout as the v1 pairs) into the survey repo's pairs_geo.
   python3 scripts/make_cp028_drive_v2_pairs.py [--out /workspace/crystal-palace-survey/look/pairs_geo]"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "/workspace/crystal-palace-survey/look/pairs_geo"
SRC = os.path.join(ROOT, "renders/candidates/cp028_drive_v2_20261102")
bef = Image.open(os.path.join(SRC, "before/CP028_louvre_start.png")).convert("RGB")
aft = Image.open(os.path.join(SRC, "after/CP028_louvre_start.png")).convert("RGB")
P = "CANDIDATE_CP028_drive_v2_"
bef.save(os.path.join(OUT, P + "before.png")); aft.save(os.path.join(OUT, P + "after.png"))
BG = (16, 16, 16); GAP = 8; LAB = 28
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
W, H = bef.size
pair = Image.new("RGB", (2 * W + GAP, H + LAB), BG)
pair.paste(bef, (0, LAB)); pair.paste(aft, (W + GAP, LAB))
d = ImageDraw.Draw(pair)
d.text((6, 7), "CP028 LIVE h03 (before)", fill=(214, 214, 214), font=font)
d.text((W + GAP + 6, 7), "CP028 CANDIDATE v2: FT51-53 as v1 (one pulley Q + shafting T, intermediate cranks) + oiler restaged ON the steps (FT54 v2)",
       fill=(150, 220, 120), font=font)
pair.save(os.path.join(OUT, P + "pair.png"))
box = (80, 160, 1180, 600)
cb, ca = bef.crop(box), aft.crop(box)
det = Image.new("RGB", (cb.width, 2 * cb.height + GAP), BG)
det.paste(cb, (0, 0)); det.paste(ca, (0, cb.height + GAP))
det.save(os.path.join(OUT, P + "detail_pair.png"))
print("wrote", [P + n + ".png" for n in ("before", "after", "pair", "detail_pair")])
