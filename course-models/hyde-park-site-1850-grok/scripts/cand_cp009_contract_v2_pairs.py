"""2026-11-09 pairs for the CP009 "contract" CANDIDATE v2 (DEPARTURES SD28-SD30, SD32-SD34; NOT live, awaiting review).
before = live renders/s02_png/CP009_{k}.png (s02, authored lighting, exposure -0.4).
after  = renders/candidates/cp009_contract_v2_20261109/after/CP009_{k}.png, exposure 0.29 / 0.06 (luma-matched).
-> survey look/pairs_geo/CANDIDATE_CP009_contract_v2_{start,end}_{before,after,pair}.png"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
LB = "BEFORE live s02 CP009"
LA = "AFTER CANDIDATE v2: planked deal, weathered hoarding, trodden earth, 1850 dress figures (hats, coats, boots)"
EXP = {"start": (-0.4, 0.29), "end": (-0.4, 0.06)}
for k in ("start", "end"):
    a, b = f"{H}/renders/s02_png/CP009_{k}.png", f"{H}/renders/candidates/cp009_contract_v2_20261109/after/CP009_{k}.png"
    shutil.copy(a, f"{OUT}/CANDIDATE_CP009_contract_v2_{k}_before.png"); shutil.copy(b, f"{OUT}/CANDIDATE_CP009_contract_v2_{k}_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    la = ImageStat.Stat(A.convert("L").resize((960, 540))).mean[0]; lb = ImageStat.Stat(B.convert("L").resize((960, 540))).mean[0]
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
    d = ImageDraw.Draw(S); d.text((10, 8), LB, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), LA, fill=(255, 255, 255), font=FN)
    out = f"{OUT}/CANDIDATE_CP009_contract_v2_{k}_pair.png"; S.save(out)
    print("PAIR", out, f"luma {la:.2f} -> {lb:.2f} (exposure {EXP[k][0]} -> {EXP[k][1]})")
