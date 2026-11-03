"""2026-11-03 CANDIDATE pairs for CP011_yard lattice pass (DEPARTURES CN48, no verdict, NOT live).
before = live KEEP renders (survey look/pairs_geo/KEEP_CP011_yard_{k}_after.png = renders/c07/CP011_yard_{k}.png);
after = rounds/candidates/c07_cp011lattice.blend via scripts/render_cp011_lattice.sh (same live settings + exposure)."""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
C = f"{H}/renders/candidates/cp011_lattice_20261103/after"
LB = "BEFORE live c07 (KEEP CN47): girders flat, read as plank stacks"
LA = "AFTER CANDIDATE CN48: girders on edge (lattice web), bay sightline, smoke"
for k in ("start", "end"):
    a, b = f"{OUT}/KEEP_CP011_yard_{k}_after.png", f"{C}/CP011_yard_{k}.png"
    shutil.copy(a, f"{OUT}/CANDIDATE_CP011_lattice_{k}_before.png"); shutil.copy(b, f"{OUT}/CANDIDATE_CP011_lattice_{k}_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    la, lb = ImageStat.Stat(A.convert("L")).mean[0], ImageStat.Stat(B.convert("L")).mean[0]
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
    d = ImageDraw.Draw(S); d.text((10, 8), LB, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), LA, fill=(255, 255, 255), font=FN)
    out = f"{OUT}/CANDIDATE_CP011_lattice_{k}_pair.png"; S.save(out); print("PAIR", out, f"luma {la:.1f} -> {lb:.1f}")
