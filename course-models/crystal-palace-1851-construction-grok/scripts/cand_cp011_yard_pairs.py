"""2026-11-03 pairs for CP011_yard (CN47): KEEP start+end 2026-11-03 (parent verdict; was CANDIDATE, files renamed
CANDIDATE_CP011_yard_* -> KEEP_CP011_yard_*, after labels relabelled KEEP, pixels otherwise unchanged; live = rounds/c07.blend
via scripts/render_cp011_yard_live.sh -> renders/c07/CP011_yard_{start,end}.png, pixel-identical to the afters).
before = rounds/c07.blend re-rendered 2026-11-03 with the current pipeline (render_views default look + people swap);
the COVERAGE file renders/c07/CP011_yard_start.png is stale/pre-look (luma ~104) and is not used.
after = rounds/candidates/c07_cp011yard.blend (scripts/cand_cp011_yard_20261103.py), --no-people, exposure start 0.95 / end 1.06
to match before mean luma within 1 (scripts/render_cp011_yard.sh)."""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
C = f"{H}/renders/candidates/cp011_yard_20261103"
LB = "BEFORE c07 (re-rendered 2026-11-03): open shed, white CP014 backdrop leaking"
PFX = "KEEP"
LA = {"start": "AFTER KEEP: brick works, cinder yard, stacked girders + columns",
      "end": "AFTER KEEP: timber bay, benches, trolley, tally clerk"}
for k in ("start", "end"):
    a, b = f"{C}/before/CP011_yard_{k}.png", f"{C}/after/CP011_yard_{k}.png"
    shutil.copy(a, f"{OUT}/{PFX}_CP011_yard_{k}_before.png"); shutil.copy(b, f"{OUT}/{PFX}_CP011_yard_{k}_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    la, lb = ImageStat.Stat(A.convert("L")).mean[0], ImageStat.Stat(B.convert("L")).mean[0]
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
    d = ImageDraw.Draw(S); d.text((10, 8), LB, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), LA[k], fill=(255, 255, 255), font=FN)
    out = f"{OUT}/{PFX}_CP011_yard_{k}_pair.png"; S.save(out); print("PAIR", out, f"luma {la:.1f} -> {lb:.1f}")
