"""2026-11-09 pairs for the CP015_blinds "canvas" CANDIDATE (DEPARTURES CN52; no verdict, NOT live).
before = live rounds/c04.blend (md5 7810ed1f) re-rendered now: renders/candidates/cp015_canvas_20261109/before/CP015_blinds_start.png, exposure -0.85
after  = rounds/candidates/c04_cp015canvas.blend, frame 36: renders/candidates/cp015_canvas_20261109/after/CP015_blinds_start.png, exposure -1.73
-> survey look/pairs_geo/CANDIDATE_CP015_canvas_start_{before,after,pair}.png"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
R = f"{H}/renders/candidates/cp015_canvas_20261109"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
LB = "BEFORE live c04 (CN09 canvas tent, louvres shut)"
LA = "AFTER CANDIDATE CN52: Downes drape, calico, louvres open together"
a, b = f"{R}/before/CP015_blinds_start.png", f"{R}/after/CP015_blinds_start.png"
shutil.copy(a, f"{OUT}/CANDIDATE_CP015_canvas_start_before.png"); shutil.copy(b, f"{OUT}/CANDIDATE_CP015_canvas_start_after.png")
A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
la, lb = ImageStat.Stat(A.convert("L")).mean[0], ImageStat.Stat(B.convert("L")).mean[0]
S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
d = ImageDraw.Draw(S); d.text((10, 8), LB, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), LA, fill=(255, 255, 255), font=FN)
out = f"{OUT}/CANDIDATE_CP015_canvas_start_pair.png"; S.save(out)
print("PAIR", out, f"luma {la:.2f} -> {lb:.2f} (exposure -0.85 -> -1.73)")
