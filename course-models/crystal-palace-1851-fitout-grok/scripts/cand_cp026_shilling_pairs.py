"""2026-11-10 pairs for the CP026 "shilling" CANDIDATE (DEPARTURES FT55-FT57, FT59; NOT live, awaiting review).
before = live renders/h03/CP026_shilling_ext_start.png (people v3.1, look v1.1 exterior_midday, exposure -0.7).
after  = renders/candidates/cp026_shilling_20261110/after/CP026_shilling_ext_start.png (same recipe, exposure -0.76, luma-matched).
-> survey look/pairs_geo/CANDIDATE_CP026_shilling_start_{before,after,pair,detail_pair}.png"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except Exception: FN = ImageFont.load_default()
LB = "BEFORE live h03 CP026_shilling_ext_start (exp -0.7)"
LA = "AFTER CANDIDATE: 1851 working dress queue (shawls, bonnets, smocks), Downes 4 ft 9 in pedestals, gravel, vertical boarding (exp -0.76)"
a = f"{H}/renders/h03/CP026_shilling_ext_start.png"; b = f"{H}/renders/candidates/cp026_shilling_20261110/after/CP026_shilling_ext_start.png"
P = f"{OUT}/CANDIDATE_CP026_shilling_start"
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
