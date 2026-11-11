"""2026-11-11 pairs for the CP014_drain_whole "Downes plate" CANDIDATE (DEPARTURES KD07-KD13; no verdict, NOT live).
before = live rounds/k01.blend (md5 6f647743) re-rendered now with the live hero recipe (look v1 studio, exposure 0.40)
after  = rounds/candidates/k01_cp014plate.blend, exposure -0.13 (re-matched to the before mean luma)
-> survey look/pairs_geo/CANDIDATE_CP014_plate_whole_start_{before,after,pair}.png + _detail_pair.png (same pixel crop, x2)"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
R = f"{H}/renders/candidates/cp014_plate_20261111"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
except Exception: FN = ImageFont.load_default()
EB, EA = 0.40, -0.13
a, b = f"{R}/before/CP014_drain_whole_start.png", f"{R}/after/CP014_drain_whole_start.png"
P = f"{OUT}/CANDIDATE_CP014_plate_whole_start"
shutil.copy(a, P + "_before.png"); shutil.copy(b, P + "_after.png")
A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
la, lb = ImageStat.Stat(A.convert("L")).mean[0], ImageStat.Stat(B.convert("L")).mean[0]
def pair(A, B, LB, LA, out):
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 56), (20, 20, 20)); S.paste(A, (0, 56)); S.paste(B, (A.width + 10, 56))
    d = ImageDraw.Draw(S)
    for i, t in enumerate(LB.split("\n")): d.text((8, 6 + 22 * i), t, fill=(255, 255, 255), font=FN)
    for i, t in enumerate(LA.split("\n")): d.text((A.width + 18, 6 + 22 * i), t, fill=(255, 255, 255), font=FN)
    S.save(out); return out
print("PAIR", pair(A, B, f"BEFORE live k01 (exp {EB}, luma {la:.2f})\nlabels cut off, buried drain hidden by turf",
                   f"AFTER CANDIDATE KD07-13 (exp {EA}, luma {lb:.2f})\nground in section, Downes VIII/XIII sizes", P + "_pair.png"), f"luma {la:.2f} -> {lb:.2f}")
box = (150, 860, 720, 1240)   # underground run: column foot, base piece, outlet, pipe, drain
print("PAIR", pair(A.crop(box).resize(((box[2] - box[0]) * 2, (box[3] - box[1]) * 2)), B.crop(box).resize(((box[2] - box[0]) * 2, (box[3] - box[1]) * 2)),
                   "BEFORE detail (same crop, x2)", "AFTER detail (same crop, x2)", P + "_detail_pair.png"))
