"""2026-11-02 CANDIDATE pairs for CP016_wheels (before = live c06, after = renders/candidates/cp016_wheels_20261102)."""
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
live = f"{H}/renders/c06/CP016_wheels_start.png"; cs = f"{H}/renders/candidates/cp016_wheels_20261102/CP016_wheels_start.png"
ce = f"{H}/renders/candidates/cp016_wheels_20261102/CP016_wheels_end.png"
pair(live, cs, "BEFORE live c06 CP016_wheels_start", "AFTER CANDIDATE 2026-11-02 (off scaffold standard, iron wheels)", f"{OUT}/CANDIDATE_CP016_wheels_reframe_pair.png")
pair(cs, ce, "CANDIDATE start", "CANDIDATE end (1.5 ft push-in; no live end exists)", f"{OUT}/CANDIDATE_CP016_wheels_reframe_startend.png")
