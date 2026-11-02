"""2026-11-02 CANDIDATE pairs for CP012_bay (not promoted). before start = live renders/c07/CP012_bay_start.png;
before end = there is no live c07 end, so c07.blend re-rendered 2026-11-02 with the current pipeline
(renders/candidates/cp012_bay_20261102/BEFORE_c07_rerender_CP012_bay_end.png; render_views default people swap).
after = renders/candidates/cp012_bay_20261102 (scripts/render_cp012_bay.sh, CN45)."""
from PIL import Image, ImageDraw, ImageFont
import os
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
C = f"{H}/renders/candidates/cp012_bay_20261102"
BEFORE = {"start": (f"{H}/renders/c07/CP012_bay_start.png", "BEFORE live CP012_bay_start (c07)"),
          "end": (f"{C}/BEFORE_c07_rerender_CP012_bay_end.png", "BEFORE c07 end (no live end; re-rendered 2026-11-02)")}
AFTER = {"start": "AFTER CANDIDATE: square-on bay, girder hanging 3 ft below seat",
         "end": "AFTER CANDIDATE: walked out of lifting zone, girder seated"}
for k in ("start", "end"):
    A, B = Image.open(BEFORE[k][0]).convert("RGB"), Image.open(f"{C}/CP012_bay_{k}.png").convert("RGB")
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
    d = ImageDraw.Draw(S); d.text((10, 8), BEFORE[k][1], fill=(255, 255, 255), font=FN)
    d.text((A.width + 20, 8), AFTER[k], fill=(255, 255, 255), font=FN)
    out = f"{OUT}/CANDIDATE_CP012_bay_{k}_pair.png"; S.save(out); print("PAIR", out)
