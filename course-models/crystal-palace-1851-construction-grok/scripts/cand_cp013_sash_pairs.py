"""2026-11-11 pairs for the CP013_sash "Downes roof" CANDIDATE (DEPARTURES CN54; no verdict, NOT live).
before = live rounds/c04.blend (md5 415e5100) re-rendered now, exposure -0.85 (look v1 exterior_midday)
after  = rounds/candidates/c04_cp013sash.blend, exposure re-matched to the before mean luma (start -0.78, end -0.95)
-> survey look/pairs_geo/CANDIDATE_CP013_sash_{start,end}_{before,after,pair}.png"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
R = f"{H}/renders/candidates/cp013_sash_20261111"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
EXP = {"start": (-0.85, -0.78), "end": (-0.85, -0.95)}
LB = "BEFORE live c04 (1.5x2.5 in bars, box gutters, no glass)"
LA = "AFTER CANDIDATE CN54: Downes bars/gutter/ridge, tie-rods, glazing order"
for fr, (eb, ea) in EXP.items():
    a, b = f"{R}/before/CP013_sash_{fr}.png", f"{R}/after/CP013_sash_{fr}.png"
    shutil.copy(a, f"{OUT}/CANDIDATE_CP013_sash_{fr}_before.png"); shutil.copy(b, f"{OUT}/CANDIDATE_CP013_sash_{fr}_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    la, lb = ImageStat.Stat(A.convert("L")).mean[0], ImageStat.Stat(B.convert("L")).mean[0]
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
    d = ImageDraw.Draw(S); d.text((10, 8), LB, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), LA, fill=(255, 255, 255), font=FN)
    out = f"{OUT}/CANDIDATE_CP013_sash_{fr}_pair.png"; S.save(out)
    print("PAIR", out, f"luma {la:.2f} -> {lb:.2f} (exposure {eb} -> {ea})")
