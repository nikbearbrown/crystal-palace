"""2026-11-11 pairs for the CP020 nave CANDIDATE (DEPARTURES FT60-FT66). NOT live, no verdict.
before = live renders/f03/CP020_floor_start.png (people v3.3, --keep-lighting, exposure -1.768, 24 spp; re-render max diff 1).
after  = renders/candidates/cp020_nave_20261111/after/CP020_floor_start.png (same recipe, same exposure -1.768).
-> survey look/pairs_geo/CANDIDATE_CP020_nave_start_{before,after,pair,detail_pair}.png
   python3 scripts/cand_cp020_nave_pairs.py"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except Exception: FN = ImageFont.load_default()
LB = "BEFORE live f03 CP020_floor_start (exp -1.768)"
LA = "CANDIDATE: nave continued west to the 1,848 ft end + nave roof, f03 part library; people untouched (exp -1.768)"
a = f"{H}/renders/f03/CP020_floor_start.png"
b = f"{H}/renders/candidates/cp020_nave_20261111/after/CP020_floor_start.png"
P = f"{OUT}/CANDIDATE_CP020_nave_start"
shutil.copy(a, P + "_before.png"); shutil.copy(b, P + "_after.png")
A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
def luma(im): return ImageStat.Stat(im.convert("L")).mean[0]
def pair(A, B, la, lb, out):
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 36), (20, 20, 20)); S.paste(A, (0, 36)); S.paste(B, (A.width + 10, 36))
    d = ImageDraw.Draw(S); d.text((10, 7), la, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 7), lb, fill=(255, 255, 255), font=FN); S.save(out)
pair(A, B, LB, LA, P + "_pair.png")
box = (0, 0, 853, 420)   # upper-left: the view down the nave (horizon / roof) at 1.5x
ca, cb = [im.crop(box).resize((int(853 * 1.5), int(420 * 1.5)), Image.LANCZOS) for im in (A, B)]
pair(ca, cb, "BEFORE detail 1.5x", "CANDIDATE detail 1.5x", P + "_detail_pair.png")
print("PAIRS", P + "_{before,after,pair,detail_pair}.png", f"luma(L) {luma(A):.2f} -> {luma(B):.2f}")
