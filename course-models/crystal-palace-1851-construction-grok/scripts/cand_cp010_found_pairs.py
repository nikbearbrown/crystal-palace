"""2026-11-10 pairs for the CP010_foundations "setting out + gravel" CANDIDATE (DEPARTURES CN53; no verdict, NOT live).
before = live rounds/c06.blend (md5 e461f024) re-rendered now, live pipeline (look -0.85, people swap): renders/candidates/cp010_found_20261110/before/
after  = rounds/candidates/c06_cp010found.blend, --no-people, exposure -0.42 start / -0.31 end: renders/candidates/cp010_found_20261110/after/
-> survey look/pairs_geo/CANDIDATE_CP010_found_{start,end}_{before,after,pair}.png"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
R = f"{H}/renders/candidates/cp010_found_20261110"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
EXP = {"start": (-0.85, -0.42), "end": (-0.85, -0.31)}
LB = "BEFORE live c06 (flat clay, smooth domes, block stand-ins)"
LA = "AFTER CANDIDATE CN53: Downes setting-out stakes, gravel stratum, rough spoil"
for fr in ("start", "end"):
    a, b = f"{R}/before/CP010_foundations_{fr}.png", f"{R}/after/CP010_foundations_{fr}.png"
    shutil.copy(a, f"{OUT}/CANDIDATE_CP010_found_{fr}_before.png"); shutil.copy(b, f"{OUT}/CANDIDATE_CP010_found_{fr}_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    la, lb = ImageStat.Stat(A.convert("L")).mean[0], ImageStat.Stat(B.convert("L")).mean[0]
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
    d = ImageDraw.Draw(S); d.text((10, 8), LB, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), LA, fill=(255, 255, 255), font=FN)
    out = f"{OUT}/CANDIDATE_CP010_found_{fr}_pair.png"; S.save(out)
    print("PAIR", out, f"luma {la:.2f} -> {lb:.2f} (exposure {EXP[fr][0]} -> {EXP[fr][1]})")
