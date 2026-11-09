"""2026-11-09 pairs for the CP006 "winterpark" CANDIDATE (DEPARTURES SD35-SD42; NOT live, awaiting review).
before = live renders/s02_png/CP006_{k}.png (start: authored lighting, state exposure -0.25; end: look v1.1, -0.85).
after  = renders/candidates/cp006_winterpark_20261109/after/CP006_{k}.png (start 0.14 / end -0.50, luma-matched).
-> survey look/pairs_geo/CANDIDATE_CP006_winterpark_{start,end}_{before,after,pair}.png"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
LB = "BEFORE live s02 CP006"
LA = "AFTER CANDIDATE: bare winter crowns, winter turf + sward, survey party in 1850 dress at theodolite/chain/pole/staff"
EXP = {"start": (-0.25, 0.14), "end": (-0.85, -0.50)}
for k in ("start", "end"):
    a, b = f"{H}/renders/s02_png/CP006_{k}.png", f"{H}/renders/candidates/cp006_winterpark_20261109/after/CP006_{k}.png"
    shutil.copy(a, f"{OUT}/CANDIDATE_CP006_winterpark_{k}_before.png"); shutil.copy(b, f"{OUT}/CANDIDATE_CP006_winterpark_{k}_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    la = ImageStat.Stat(A.convert("L").resize((960, 540))).mean[0]; lb = ImageStat.Stat(B.convert("L").resize((960, 540))).mean[0]
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
    d = ImageDraw.Draw(S); d.text((10, 8), LB, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), LA, fill=(255, 255, 255), font=FN)
    out = f"{OUT}/CANDIDATE_CP006_winterpark_{k}_pair.png"; S.save(out)
    print("PAIR", out, f"luma {la:.2f} -> {lb:.2f} (exposure {EXP[k][0]} -> {EXP[k][1]})")
