"""2026-11-16 pairs for the CP019 cases CANDIDATE (DEPARTURES FT101-FT108). NOT live, no verdict.
before = live rounds/f03.blend re-rendered, after = rounds/candidates/f03_cp019cases.blend; same live camera, same per-camera
recipe both sides (FT107), 1920x1080 48 spp (scripts/render_cp019_cases.sh).
-> renders/candidates/cp019_cases_20261116/CANDIDATE_<cam>_pair.jpg (+ hero detail pairs) and
   survey look/pairs_geo/CANDIDATE_CP019_doors_start_{before,after,pair,detail_pair}.png, CANDIDATE_CP019_sidefx_dray_{before,after,pair}.png
   python3 scripts/cand_cp019_cases_pairs.py [--survey]   (2026-11-16 run: without --survey; nothing written outside this model folder)"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os, shutil, json, sys
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo" if "--survey" in sys.argv else "/nonexistent"   # survey copies only on request
R = f"{H}/renders/candidates/cp019_cases_20261116"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except Exception: FN = ImageFont.load_default()
def luma(im):
    a = np.asarray(im.convert("RGB")).astype(float); return float((0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).mean())
def pair(A, B, la, lb, out):
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 36), (20, 20, 20)); S.paste(A, (0, 36)); S.paste(B, (A.width + 10, 36))
    d = ImageDraw.Draw(S); d.text((10, 7), la, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 7), lb, fill=(255, 255, 255), font=FN)
    S.save(out, quality=90) if out.endswith(".jpg") else S.save(out)
res = {}
HERO = "CP019_doors_start"
for cam, P in [(HERO, f"{OUT}/CANDIDATE_CP019_doors_start"), ("CP019_dray_start", f"{OUT}/CANDIDATE_CP019_sidefx_dray")]:
    a, b = f"{R}/before/{cam}.png", f"{R}/after/{cam}.png"
    if not (os.path.exists(a) and os.path.exists(b)): print("MISSING", cam); continue
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    d = np.abs(np.asarray(A).astype(int) - np.asarray(B).astype(int)).max(2)
    la, lb = luma(A), luma(B)
    tag = "CANDIDATE" if cam == HERO else "CANDIDATE side effect"
    LA = f"BEFORE live f03 {cam} (same recipe/exposure, luma {la:.2f})"; LB = f"{tag}: cases, bales, sculpture, flywheel, bare elms (luma {lb:.2f}); not live"
    pair(A, B, LA, LB, f"{R}/CANDIDATE_{cam}_pair.jpg")
    if os.path.isdir(OUT):
        shutil.copy(a, P + "_before.png"); shutil.copy(b, P + "_after.png"); pair(A, B, LA, LB, P + "_pair.png")
    det = {}
    if cam == HERO:
        for nm, box in (("left_cases", (0, 380, 960, 920)), ("right_sculpture", (1100, 260, 1920, 900)), ("doors_trees", (560, 180, 1360, 720))):
            ca, cb = [im.crop(box) for im in (A, B)]
            pth = f"{R}/CANDIDATE_{cam}_detail_{nm}_pair.jpg"; pair(ca, cb, f"BEFORE detail {nm} (1:1)", f"CANDIDATE detail {nm} (1:1)", pth); det[nm] = pth
        if os.path.isdir(OUT): shutil.copy(det["right_sculpture"], P + "_detail_pair.jpg")
    ys, xs = np.nonzero(d > 20)
    res[cam] = {"before": a, "after": b, "luma_before": round(la, 2), "luma_after": round(lb, 2), "max_diff": int(d.max()), "mean_diff": round(float(d.mean()), 3),
                "px_gt20": int((d > 20).sum()), "bbox_gt20": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None,
                "pair": f"{R}/CANDIDATE_{cam}_pair.jpg", "details": det}
    print("PAIR", cam, json.dumps(res[cam]))
json.dump(res, open(f"{H}/checks/cp019_cases_pairs.json", "w"), indent=1)
json.dump(res, open(f"{R}/pairs.json", "w"), indent=1)
