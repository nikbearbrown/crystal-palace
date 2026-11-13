"""2026-11-13 pairs for the CP026 turnstiles CANDIDATE (DEPARTURES FT95-FT100). NOT live, no verdict.
before = live rounds/h03.blend re-rendered, after = rounds/candidates/h03_cp026turnstiles.blend; same live camera, same per-camera
recipe both sides (FT100), 1920x1080 48 spp (scripts/render_cp026_turnstiles.sh).
-> survey look/pairs_geo/CANDIDATE_CP026_turnstiles_start_{before,after,pair,detail_pair}.png (hero)
   and CANDIDATE_CP026_sidefx_{shilling_ext,watering,louvre}_{before,after,pair}.png;
   small side-by-sides (960 px per side) in /workspace/tmp/cp026cand/.
   python3 scripts/cand_cp026_turnstiles_pairs.py"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os, shutil, json
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
SM = "/workspace/tmp/cp026cand"; os.makedirs(SM, exist_ok=True)
R = f"{H}/renders/candidates/cp026_turnstiles_20261113"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except Exception: FN = ImageFont.load_default()
def luma(im):
    a = np.asarray(im.convert("RGB")).astype(float); return float((0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).mean())
def pair(A, B, la, lb, out):
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 36), (20, 20, 20)); S.paste(A, (0, 36)); S.paste(B, (A.width + 10, 36))
    d = ImageDraw.Draw(S); d.text((10, 7), la, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 7), lb, fill=(255, 255, 255), font=FN); S.save(out)
res = {}
HERO = "CP026_turnstiles_start"
for cam, P in [(HERO, f"{OUT}/CANDIDATE_CP026_turnstiles_start"),
               ("CP026_shilling_ext_start", f"{OUT}/CANDIDATE_CP026_sidefx_shilling_ext"),
               ("CP028_watering_start", f"{OUT}/CANDIDATE_CP026_sidefx_watering"),
               ("CP028_louvre_start", f"{OUT}/CANDIDATE_CP026_sidefx_louvre")]:
    a, b = f"{R}/before/{cam}.png", f"{R}/after/{cam}.png"
    if not (os.path.exists(a) and os.path.exists(b)): print("MISSING", cam); continue
    shutil.copy(a, P + "_before.png"); shutil.copy(b, P + "_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    d = np.abs(np.asarray(A).astype(int) - np.asarray(B).astype(int)).max(2)
    la, lb = luma(A), luma(B)
    tag = "CANDIDATE" if cam == HERO else "CANDIDATE side effect"
    pair(A, B, f"BEFORE live h03 {cam} (same recipe/exposure, luma {la:.2f})",
         f"{tag}: south entrance frame + Kensington Rd elms (luma {lb:.2f}); not live", P + "_pair.png")
    sa, sb = A.resize((960, 540), Image.LANCZOS), B.resize((960, 540), Image.LANCZOS)
    pair(sa, sb, f"BEFORE {cam} (luma {la:.1f})", f"CANDIDATE {cam} (luma {lb:.1f}); not live", f"{SM}/{cam}_pair_small.png")
    if cam == HERO:
        box = (640, 0, 1920, 720)   # the central door bay: open sky/lawn hole -> framed doors + trees
        ca, cb = [im.crop(box) for im in (A, B)]
        pair(ca, cb, "BEFORE detail (door bay, 1:1)", "CANDIDATE detail (door bay, 1:1)", P + "_detail_pair.png")
    ys, xs = np.nonzero(d > 20)
    res[cam] = {"luma_before": round(la, 2), "luma_after": round(lb, 2), "max_diff": int(d.max()), "mean_diff": round(float(d.mean()), 3),
                "px_gt20": int((d > 20).sum()), "bbox_gt20": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None,
                "pair": P + "_pair.png", "small_pair": f"{SM}/{cam}_pair_small.png"}
    print("PAIR", cam, res[cam])
json.dump(res, open(f"{H}/checks/cp026_turnstiles_pairs.json", "w"), indent=1)
