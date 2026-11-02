"""2026-11-02 CANDIDATE v3 pairs for CP016_wheels. before = live (KEEP reframe, renders/candidates/cp016_wheels_20261102),
after = renders/candidates/cp016_wheels_v3_20261102 (v2 no-glaziers + far workmen in dark fustian, raised-arm man hidden)."""
from PIL import Image, ImageDraw, ImageFont
import os
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
LIVE = f"{H}/renders/candidates/cp016_wheels_20261102"; V3 = f"{H}/renders/candidates/cp016_wheels_v3_20261102"
for k in ("start", "end"):
    A, B = Image.open(f"{LIVE}/CP016_wheels_{k}.png").convert("RGB"), Image.open(f"{V3}/CP016_wheels_{k}.png").convert("RGB")
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
    d = ImageDraw.Draw(S); d.text((10, 8), f"BEFORE live CP016_wheels_{k} (KEEP reframe)", fill=(255, 255, 255), font=FN)
    d.text((A.width + 20, 8), "AFTER CANDIDATE v3: stub axles + 32 mm cam, far workmen in fustian", fill=(255, 255, 255), font=FN)
    out = f"{OUT}/KEEP_CP016_wheels_v3_{k}_pair.png"; S.save(out); print("PAIR", out)
