"""2026-11-12 pairs for the CP027 east-nave CANDIDATE (DEPARTURES FT74-FT80). NOT live, no verdict.
before = live rounds/h01.blend re-rendered, after = rounds/candidates/h01_cp027east.blend; same live camera, same recipe
(people_lib v3.1, look --era 1851, identical exposure both sides): hero 1920x1080 48 spp, side-effect cam 1280x720 24 spp
(scripts/render_cp027_east.sh).
-> survey look/pairs_geo/CANDIDATE_CP027_{before,after,pair,detail_pair}.png (hero CP027_stair_foot_start)
   and CANDIDATE_CP027_sidefx_gallery_rail_{before,after,pair}.png.
   python3 scripts/cand_cp027_east_pairs.py"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os, shutil, json
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
R = f"{H}/renders/candidates/cp027_east_20261112"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except Exception: FN = ImageFont.load_default()
def luma(im):
    a = np.asarray(im.convert("RGB")).astype(float); return float((0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).mean())
def pair(A, B, la, lb, out):
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 36), (20, 20, 20)); S.paste(A, (0, 36)); S.paste(B, (A.width + 10, 36))
    d = ImageDraw.Draw(S); d.text((10, 7), la, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 7), lb, fill=(255, 255, 255), font=FN); S.save(out)
res = {}
for cam, P in [("CP027_stair_foot_start", f"{OUT}/CANDIDATE_CP027"),
               ("CP027_gallery_rail_start", f"{OUT}/CANDIDATE_CP027_sidefx_gallery_rail")]:
    a, b = f"{R}/before/{cam}.png", f"{R}/after/{cam}.png"
    if not (os.path.exists(a) and os.path.exists(b)): print("MISSING", cam); continue
    shutil.copy(a, P + "_before.png"); shutil.copy(b, P + "_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    d = np.abs(np.asarray(A).astype(int) - np.asarray(B).astype(int)).max(2)
    la, lb = luma(A), luma(B)
    tag = "CANDIDATE" if cam == "CP027_stair_foot_start" else "CANDIDATE side effect"
    pair(A, B, f"BEFORE live h01 {cam} (same look/exposure, luma {la:.2f})",
         f"{tag}: east nave added, lawn/sky gone (same look/exposure, luma {lb:.2f}); not live", P + "_pair.png")
    if cam == "CP027_stair_foot_start":
        box = (0, 300, 800, 1080)   # left: open lawn + sky under the side gallery -> east nave
        ca, cb = [im.crop(box).resize((800, 780), Image.LANCZOS) for im in (A, B)]
        pair(ca, cb, "BEFORE detail (left, 1:1)", "CANDIDATE detail (left, 1:1)", P + "_detail_pair.png")
    res[cam] = {"luma_before": round(la, 2), "luma_after": round(lb, 2), "max_diff": int(d.max()), "mean_diff": round(float(d.mean()), 3),
                "px_gt20": int((d > 20).sum()), "pair": P + "_pair.png"}
    print("PAIR", cam, res[cam])
json.dump(res, open(f"{H}/checks/cp027_east_pairs.json", "w"), indent=1)
