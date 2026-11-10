"""2026-11-10 pair for the CP007 "committee" CANDIDATE (DEPARTURES SD43-SD49; NOT live, awaiting review).
before = live renders/s02_png/CP007_start.png (authored lighting, keep-lighting, exposure -0.4).
after  = renders/candidates/cp007_committee_20261110/after/CP007_start.png (exposure 0.85, luma-matched).
-> survey look/pairs_geo/CANDIDATE_CP007_committee_start_{before,after,pair}.png
CP007_end is unchanged by eye (W7_ objects sit below its frame; 25 % regression max 9/255 on 59 px, sampling noise)."""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
LB = "BEFORE live s02 CP007_start"
LA = "AFTER CANDIDATE: Building Committee design 1:600 true heights (ribbed dome on drum, sheds, arched entrances), deal table, plan sheet, sward, f/8"
EXP = (-0.4, 0.85)
a, b = f"{H}/renders/s02_png/CP007_start.png", f"{H}/renders/candidates/cp007_committee_20261110/after/CP007_start.png"
shutil.copy(a, f"{OUT}/CANDIDATE_CP007_committee_start_before.png"); shutil.copy(b, f"{OUT}/CANDIDATE_CP007_committee_start_after.png")
A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
la = ImageStat.Stat(A.convert("L").resize((960, 540))).mean[0]; lb = ImageStat.Stat(B.convert("L").resize((960, 540))).mean[0]
S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
d = ImageDraw.Draw(S); d.text((10, 8), LB, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), LA, fill=(255, 255, 255), font=FN)
out = f"{OUT}/CANDIDATE_CP007_committee_start_pair.png"; S.save(out)
print("PAIR", out, f"luma {la:.2f} -> {lb:.2f} (exposure {EXP[0]} -> {EXP[1]})")
