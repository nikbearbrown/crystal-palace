"""2026-11-10 pairs for the CP026 environment-only polish (DEPARTURES FT56/FT56b, FT57, FT59; no FT55). Parent verdict KEEP.
before = live renders/h03/CP026_shilling_ext_start.png as it was before the KEEP (people v3.1, look v1.1 exterior_midday, exposure -0.7).
after  = renders/candidates/cp026_env_20261110/after/CP026_shilling_ext_start.png (same recipe, same exposure -0.7).
-> survey look/pairs_geo/KEEP_CP026_env_start_{before,after,pair,detail_pair}.png
   python3 scripts/cand_cp026_env_pairs.py [--before PATH]   (default before = live PNG; after the KEEP pass the pre-keep PNG)"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil, sys
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except Exception: FN = ImageFont.load_default()
LB = "BEFORE live h03 CP026_shilling_ext_start (exp -0.7)"
LA = "AFTER KEEP: gravel apron, vertical south boarding, Downes 4 ft 9 in pedestals; people v3.1 untouched (exp -0.7)"
a = sys.argv[sys.argv.index("--before") + 1] if "--before" in sys.argv else f"{H}/renders/h03/CP026_shilling_ext_start.png"
b = f"{H}/renders/candidates/cp026_env_20261110/after/CP026_shilling_ext_start.png"
P = f"{OUT}/KEEP_CP026_env_start"
shutil.copy(a, P + "_before.png"); shutil.copy(b, P + "_after.png")
A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
def luma(im): return ImageStat.Stat(im.convert("L")).mean[0]
def pair(A, B, la, lb, out):
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 36), (20, 20, 20)); S.paste(A, (0, 36)); S.paste(B, (A.width + 10, 36))
    d = ImageDraw.Draw(S); d.text((10, 7), la, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 7), lb, fill=(255, 255, 255), font=FN); S.save(out)
pair(A, B, LB, LA, P + "_pair.png")
box = (0, 330, 853, 720)   # lower 54 %: queue, pedestal, gravel at 1.5x
ca, cb = [im.crop(box).resize((int(853 * 1.5), int(390 * 1.5)), Image.LANCZOS) for im in (A, B)]
pair(ca, cb, "BEFORE detail 1.5x", "AFTER detail 1.5x", P + "_detail_pair.png")
print("PAIRS", P + "_{before,after,pair,detail_pair}.png", f"luma {luma(A):.2f} -> {luma(B):.2f}")
