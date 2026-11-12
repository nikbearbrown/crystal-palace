"""2026-11-12 pairs for the CP018 east-nave CANDIDATE (DEPARTURES FT88-FT94). NOT live, no verdict.
before = live rounds/f03.blend re-rendered, after = rounds/candidates/f03_cp018east.blend; same live camera, same per-camera
recipe both sides (FT94), 1920x1080 48 spp (scripts/render_cp018_east.sh).
-> survey look/pairs_geo/CANDIDATE_CP018_paint_start_{before,after,pair,detail_pair}.png (hero)
   and CANDIDATE_CP018_sidefx_{paint_end,dray,floor}_{before,after,pair}.png;
   small side-by-sides (960 px per side) in /workspace/tmp/cp018/.
   python3 scripts/cand_cp018_east_pairs.py"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os, shutil, json
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
SM = "/workspace/tmp/cp018"; os.makedirs(SM, exist_ok=True)
R = f"{H}/renders/candidates/cp018_east_20261112"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except Exception: FN = ImageFont.load_default()
def luma(im):
    a = np.asarray(im.convert("RGB")).astype(float); return float((0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).mean())
def pair(A, B, la, lb, out):
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 36), (20, 20, 20)); S.paste(A, (0, 36)); S.paste(B, (A.width + 10, 36))
    d = ImageDraw.Draw(S); d.text((10, 7), la, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 7), lb, fill=(255, 255, 255), font=FN); S.save(out)
res = {}
HERO = "CP018_paint_start"
for cam, P, short in [(HERO, f"{OUT}/CANDIDATE_CP018_paint_start", "paint"),
                      ("CP018_paint_end", f"{OUT}/CANDIDATE_CP018_sidefx_paint_end", "paint_end"),
                      ("CP019_dray_start", f"{OUT}/CANDIDATE_CP018_sidefx_dray", "dray"),
                      ("CP020_floor_start", f"{OUT}/CANDIDATE_CP018_sidefx_floor", "floor")]:
    a, b = f"{R}/before/{cam}.png", f"{R}/after/{cam}.png"
    if not (os.path.exists(a) and os.path.exists(b)): print("MISSING", cam); continue
    shutil.copy(a, P + "_before.png"); shutil.copy(b, P + "_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    d = np.abs(np.asarray(A).astype(int) - np.asarray(B).astype(int)).max(2)
    la, lb = luma(A), luma(B)
    tag = "CANDIDATE" if cam == HERO else "CANDIDATE side effect"
    pair(A, B, f"BEFORE live f03 {cam} (same recipe/exposure, luma {la:.2f})",
         f"{tag}: east nave added beyond x = +132 ft (luma {lb:.2f}); not live", P + "_pair.png")
    sa, sb = A.resize((960, 540), Image.LANCZOS), B.resize((960, 540), Image.LANCZOS)
    pair(sa, sb, f"BEFORE {cam} (luma {la:.1f})", f"CANDIDATE {cam} (luma {lb:.1f}); not live", f"{SM}/{cam}_pair_small.png")
    if cam == HERO:
        box = (560, 300, 1520, 840)   # middle band: lawn + open sky under the galleries -> east nave
        ca, cb = [im.crop(box) for im in (A, B)]
        pair(ca, cb, "BEFORE detail (right, 1:1)", "CANDIDATE detail (right, 1:1)", P + "_detail_pair.png")
    ys, xs = np.nonzero(d > 20)
    res[cam] = {"luma_before": round(la, 2), "luma_after": round(lb, 2), "max_diff": int(d.max()), "mean_diff": round(float(d.mean()), 3),
                "px_gt20": int((d > 20).sum()), "bbox_gt20": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None,
                "px_gt20_middle_band": int((d[300:840, :] > 20).sum()), "pair": P + "_pair.png", "small_pair": f"{SM}/{cam}_pair_small.png"}
    print("PAIR", cam, res[cam])
json.dump(res, open(f"{H}/checks/cp018_east_pairs.json", "w"), indent=1)
