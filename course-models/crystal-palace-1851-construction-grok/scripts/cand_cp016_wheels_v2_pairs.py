"""2026-11-02 CANDIDATE v2 pairs for CP016_wheels. before = live (KEEP reframe, renders/candidates/cp016_wheels_20261102),
after = renders/candidates/cp016_wheels_v2_20261102 (stub axles + front32 camera + 2 glaziers) and
renders/candidates/cp016_wheels_v2_noglaziers_20261102 (stub axles + front32 camera only)."""
from PIL import Image, ImageDraw, ImageFont
import os
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
def pair(a, b, la, lb, out):
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
    d = ImageDraw.Draw(S); d.text((10, 8), la, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), lb, fill=(255, 255, 255), font=FN)
    S.save(out); print("PAIR", out)
LIVE = f"{H}/renders/candidates/cp016_wheels_20261102"; V2 = f"{H}/renders/candidates/cp016_wheels_v2_20261102"; NG = f"{H}/renders/candidates/cp016_wheels_v2_noglaziers_20261102"
for k in ("start", "end"):
    pair(f"{LIVE}/CP016_wheels_{k}.png", f"{V2}/CP016_wheels_{k}.png", f"BEFORE live CP016_wheels_{k} (KEEP reframe)",
         "AFTER CANDIDATE v2: stub axles, 32 mm deck-lip cam, 2 glaziers", f"{OUT}/REJECTED_CP016_wheels_v2_{k}_pair.png")
    pair(f"{LIVE}/CP016_wheels_{k}.png", f"{NG}/CP016_wheels_{k}.png", f"BEFORE live CP016_wheels_{k} (KEEP reframe)",
         "AFTER CANDIDATE v2 no glaziers: stub axles + 32 mm cam only", f"{OUT}/SUPERSEDED_CP016_wheels_v2_noglaziers_{k}_pair.png")
