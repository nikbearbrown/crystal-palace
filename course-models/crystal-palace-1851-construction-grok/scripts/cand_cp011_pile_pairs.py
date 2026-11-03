"""2026-11-03 pairs for the CP011_yard near pile + timber bay CANDIDATE (DEPARTURES CN50; no verdict, NOT live).
before = live renders/c07/CP011_yard_{k}.png (= survey KEEP_CP011_lattice_v2_{k}_after.png), exposure 0.97 / 1.00.
after  = renders/candidates/cp011_pile_20261103/after/CP011_yard_{k}.png, exposure 1.09 / 1.16.
-> survey look/pairs_geo/CANDIDATE_CP011_pile_{start,end}_{before,after,pair}.png"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
LB = "BEFORE live c07 (KEEP CN47 + CN49)"
LA = "AFTER CANDIDATE CN50: flanged as-cast girders, deal stacks + floor"
EXP = {"start": (0.97, 1.09), "end": (1.00, 1.16)}
for k in ("start", "end"):
    a, b = f"{H}/renders/c07/CP011_yard_{k}.png", f"{H}/renders/candidates/cp011_pile_20261103/after/CP011_yard_{k}.png"
    shutil.copy(a, f"{OUT}/CANDIDATE_CP011_pile_{k}_before.png"); shutil.copy(b, f"{OUT}/CANDIDATE_CP011_pile_{k}_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    la, lb = ImageStat.Stat(A.convert("L")).mean[0], ImageStat.Stat(B.convert("L")).mean[0]
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
    d = ImageDraw.Draw(S); d.text((10, 8), LB, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), LA, fill=(255, 255, 255), font=FN)
    out = f"{OUT}/CANDIDATE_CP011_pile_{k}_pair.png"; S.save(out)
    print("PAIR", out, f"luma {la:.1f} -> {lb:.1f} (exposure {EXP[k][0]} -> {EXP[k][1]})")
