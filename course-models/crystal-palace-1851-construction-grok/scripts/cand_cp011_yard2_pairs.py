"""2026-11-03 pairs for the CP011_yard "yard2" CANDIDATE (DEPARTURES CN51; KEEP 2026-11-03, now LIVE).
before = pre-yard2 live CP011 = survey KEEP_CP011_pile_{k}_after.png (was renders/c07/CP011_yard_{k}.png until the CN51 KEEP
         promotion 2026-11-03; renders/c07 now carries yard2) (CN47 + CN49 + CN50 KEEP, c07 md5 6920b1e9), exposure 1.09 / 1.16.
after  = renders/candidates/cp011_yard2_20261103/after/CP011_yard_{k}.png, exposure 0.83 / 0.88 (shed bounce light lifts the frame).
-> survey look/pairs_geo/CANDIDATE_CP011_yard2_{start,end}_{before,after,pair}.png (historical: renamed KEEP_CP011_yard2_* and
   relabelled KEEP after the parent's verdict 2026-11-03; re-running writes fresh CANDIDATE_* files)"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
LB = "BEFORE live c07 (KEEP CN47 + CN49 + CN50)"
LA = "AFTER CANDIDATE CN51: chimney smoke, board fence, coursed brick, shed ceiling"
EXP = {"start": (1.09, 0.83), "end": (1.16, 0.88)}
for k in ("start", "end"):
    a, b = f"{OUT}/KEEP_CP011_pile_{k}_after.png", f"{H}/renders/candidates/cp011_yard2_20261103/after/CP011_yard_{k}.png"
    shutil.copy(a, f"{OUT}/CANDIDATE_CP011_yard2_{k}_before.png"); shutil.copy(b, f"{OUT}/CANDIDATE_CP011_yard2_{k}_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    la, lb = ImageStat.Stat(A.convert("L")).mean[0], ImageStat.Stat(B.convert("L")).mean[0]
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
    d = ImageDraw.Draw(S); d.text((10, 8), LB, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), LA, fill=(255, 255, 255), font=FN)
    out = f"{OUT}/CANDIDATE_CP011_yard2_{k}_pair.png"; S.save(out)
    print("PAIR", out, f"luma {la:.2f} -> {lb:.2f} (exposure {EXP[k][0]} -> {EXP[k][1]})")
