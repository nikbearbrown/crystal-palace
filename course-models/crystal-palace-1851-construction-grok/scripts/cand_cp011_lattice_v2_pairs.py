"""2026-11-03 v2 pairs for CP011_yard lattice (DEPARTURES CN49). Verdict 2026-11-03 (parent viewed the pairs):
one-tier KEEP (live c07; after = renders/c07/CP011_yard_{k}.png) -> KEEP_CP011_lattice_v2_*;
two-tier REJECTED ("reads as a wall") -> REJECTED_CP011_lattice_v2_2tier_*. Labels relabelled; pixels unchanged.
before = CN47 yard KEEP (survey look/pairs_geo/KEEP_CP011_yard_{k}_after.png = the pre-lattice live renders/c07/CP011_yard_{k}.png).
after  = renders/candidates/cp011_lattice_v2_20261103/after (1-tier, recommended) -> KEEP_CP011_lattice_v2_* (was CANDIDATE_);
         .../after_2tier (two-tier comparison)                                    -> REJECTED_CP011_lattice_v2_2tier_* (was CANDIDATE_)."""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
except Exception: FN = ImageFont.load_default()
R = f"{H}/renders/candidates/cp011_lattice_v2_20261103"
LB = "BEFORE live c07 (KEEP CN47)"
SETS = (("KEEP", "v2", "after", "AFTER KEEP CN49 v2: girders on edge, 1 tier ~3.5 ft, live smoke", {"start": 0.97, "end": 1.00}),
        ("REJECTED", "v2_2tier", "after_2tier", "AFTER REJECTED CN49 v2 alt: 2 tiers ~7 ft (reads as a wall)", {"start": 1.08, "end": 1.30}))
for PFX, tag, sub, LA, EXP in SETS:
    for k in ("start", "end"):
        a, b = f"{OUT}/KEEP_CP011_yard_{k}_after.png", f"{R}/{sub}/CP011_yard_{k}.png"
        shutil.copy(a, f"{OUT}/{PFX}_CP011_lattice_{tag}_{k}_before.png"); shutil.copy(b, f"{OUT}/{PFX}_CP011_lattice_{tag}_{k}_after.png")
        A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
        la, lb = ImageStat.Stat(A.convert("L")).mean[0], ImageStat.Stat(B.convert("L")).mean[0]
        S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 40), (20, 20, 20)); S.paste(A, (0, 40)); S.paste(B, (A.width + 10, 40))
        d = ImageDraw.Draw(S); d.text((10, 8), LB, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 8), LA, fill=(255, 255, 255), font=FN)
        out = f"{OUT}/{PFX}_CP011_lattice_{tag}_{k}_pair.png"; S.save(out)
        print("PAIR", out, f"luma {la:.1f} -> {lb:.1f} (exposure {EXP[k]})")
