"""2026-11-02 CANDIDATE pairs for CP012_bay sheer legs re-pitched (CN46; no verdict, NOT live).
before = LIVE KEEP renders renders/candidates/cp012_bay_20261102/CP012_bay_{start,end}.png (render_cp012_bay.sh);
after  = renders/candidates/cp012_shears_20261102 (render_cp012_shears.sh). Same cameras, 1280x720, 48 spp, look exposure, --no-people."""
from PIL import Image, ImageDraw, ImageFont
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
LIVE, CAND = f"{H}/renders/candidates/cp012_bay_20261102", f"{H}/renders/candidates/cp012_shears_20261102"
LAB = {"start": ("BEFORE live KEEP: shears plumb, a post in the middle", "AFTER CANDIDATE: shears raked 12.5 deg, back guy"),
       "end": ("BEFORE live KEEP end", "AFTER CANDIDATE: raked shears, girder seated")}
for k in ("start", "end"):
    a, b = f"{LIVE}/CP012_bay_{k}.png", f"{CAND}/CP012_bay_{k}.png"
    shutil.copy(a, f"{OUT}/CANDIDATE_CP012_shears_{k}_before.png"); shutil.copy(b, f"{OUT}/CANDIDATE_CP012_shears_{k}_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
    d = ImageDraw.Draw(S); d.text((10, 8), LAB[k][0], fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), LAB[k][1], fill=(255, 255, 255), font=FN)
    out = f"{OUT}/CANDIDATE_CP012_shears_{k}_pair.png"; S.save(out); print("PAIR", out)
