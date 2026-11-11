"""2026-11-11 pairs for the CP022 envelope CANDIDATE (DEPARTURES FT67-FT73). NOT live, no verdict.
before = live rounds/o01.blend re-rendered, after = rounds/candidates/o01_cp022envelope.blend; same live camera, 1280x720,
48 spp, --keep-lighting (exposure -0.7), people_lib 3.3 (scripts/render_cp022_envelope.sh).
-> survey look/pairs_geo/CANDIDATE_CP022_envelope_{before,after,pair,detail_pair}.png (hero CP022_fountain_start)
   and CANDIDATE_CP022_envelope_sidefx_<cam>_{before,after,pair}.png for the other o01 cameras.
   python3 scripts/cand_cp022_envelope_pairs.py"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os, shutil, json
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
R = f"{H}/renders/candidates/cp022_envelope_20261111"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except Exception: FN = ImageFont.load_default()
def luma(im):
    a = np.asarray(im.convert("RGB")).astype(float); return float((0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).mean())
def pair(A, B, la, lb, out):
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 36), (20, 20, 20)); S.paste(A, (0, 36)); S.paste(B, (A.width + 10, 36))
    d = ImageDraw.Draw(S); d.text((10, 7), la, fill=(255, 255, 255), font=FN); d.text((A.width + 20, 7), lb, fill=(255, 255, 255), font=FN); S.save(out)
res = {}
for cam, P in [("CP022_fountain_start", f"{OUT}/CANDIDATE_CP022_envelope"),
               ("CP021_doors_start", f"{OUT}/CANDIDATE_CP022_envelope_sidefx_CP021_doors"),
               ("CP021_dais_start", f"{OUT}/CANDIDATE_CP022_envelope_sidefx_CP021_dais"),
               ("CP022_crossing_start", f"{OUT}/CANDIDATE_CP022_envelope_sidefx_CP022_crossing")]:
    a, b = f"{R}/before/{cam}.png", f"{R}/after/{cam}.png"
    if not (os.path.exists(a) and os.path.exists(b)): print("MISSING", cam); continue
    shutil.copy(a, P + "_before.png"); shutil.copy(b, P + "_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    d = np.abs(np.asarray(A).astype(int) - np.asarray(B).astype(int)).max(2)
    la, lb = luma(A), luma(B)
    tag = "CANDIDATE" if cam == "CP022_fountain_start" else "CANDIDATE side effect"
    pair(A, B, f"BEFORE live o01 {cam} (exp -0.7, luma {la:.2f})",
         f"{tag}: west nave + floating gallery visitors hidden (exp -0.7, luma {lb:.2f}); not live", P + "_pair.png")
    if cam == "CP022_fountain_start":
        box = (0, 0, 640, 400)   # upper-left: west side gallery / sky -> nave, floating visitors
        ca, cb = [im.crop(box).resize((960, 600), Image.LANCZOS) for im in (A, B)]
        pair(ca, cb, "BEFORE detail 1.5x", "CANDIDATE detail 1.5x", P + "_detail_pair.png")
    res[cam] = {"luma_before": round(la, 2), "luma_after": round(lb, 2), "max_diff": int(d.max()), "mean_diff": round(float(d.mean()), 3),
                "px_gt20": int((d > 20).sum()), "pair": P + "_pair.png"}
    print("PAIR", cam, res[cam])
json.dump(res, open(f"{H}/checks/cp022_envelope_pairs.json", "w"), indent=1)
