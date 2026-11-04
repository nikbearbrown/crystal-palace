"""2026-11-04 pairs for the CP009 "contract" CANDIDATE (DEPARTURES SD28-SD31; NOT live, awaiting review).
before = live renders/s02_png/CP009_{k}.png (s02, authored lighting exposure -0.4, Oct 27 figures).
after  = renders/candidates/cp009_contract_20261104/after/CP009_{k}.png, exposure 0.68 / 0.22 (luma-matched).
-> survey look/pairs_geo/CANDIDATE_CP009_contract_{start,end}_{before,after,pair}.png"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
LB = "BEFORE live s02 CP009"
LA = "AFTER CANDIDATE SD28-31: planked deal, weathered hoarding, primed iron, trodden earth, people v3.4"
EXP = {"start": (-0.4, 0.68), "end": (-0.4, 0.22)}
for k in ("start", "end"):
    a, b = f"{H}/renders/s02_png/CP009_{k}.png", f"{H}/renders/candidates/cp009_contract_20261104/after/CP009_{k}.png"
    shutil.copy(a, f"{OUT}/CANDIDATE_CP009_contract_{k}_before.png"); shutil.copy(b, f"{OUT}/CANDIDATE_CP009_contract_{k}_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    la, lb = ImageStat.Stat(A.convert("L")).mean[0], ImageStat.Stat(B.convert("L")).mean[0]
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
    d = ImageDraw.Draw(S); d.text((10, 8), LB, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), LA, fill=(255, 255, 255), font=FN)
    out = f"{OUT}/CANDIDATE_CP009_contract_{k}_pair.png"; S.save(out)
    print("PAIR", out, f"luma {la:.2f} -> {lb:.2f} (exposure {EXP[k][0]} -> {EXP[k][1]})")
