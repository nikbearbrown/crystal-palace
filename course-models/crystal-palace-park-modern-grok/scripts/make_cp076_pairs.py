"""CP076 plateau CANDIDATE 2026-11-11: before/after pairs into the survey look/pairs_geo (python3 + PIL).
Before = live rounds/parknow-r02.blend, after = rounds/candidates/parknow-r02_cp076plateau.blend; both rendered with
scripts/render_cp076_look.py (dud-fix v4 recipe: look v1.1 present/exterior_afternoon, exposure -0.8, 1280x720, 32 spp),
one camera per Blender session for both sides."""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "renders/candidates/cp076_plateau_20261111")
DST = "/workspace/crystal-palace-survey/look/pairs_geo"
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
def luma(im): a = np.asarray(im.convert("RGB")).astype(float); return float((0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).mean())
def strip(w, lines):
    s = Image.new("RGB", (w, 46), (16, 16, 16)); d = ImageDraw.Draw(s)
    for i, t in enumerate(lines): d.text((6, 4 + 20 * i), t, font=F, fill=(235, 235, 235))
    return s
def pair(b, a, lb, la, scale=720 / 1280.0, box=None):
    if box: b, a = b.crop(box), a.crop(box)
    w, h = int(b.width * scale), int(b.height * scale); b2, a2 = b.resize((w, h), Image.LANCZOS), a.resize((w, h), Image.LANCZOS)
    out = Image.new("RGB", (2 * w + 10, h + 46), (0, 0, 0))
    out.paste(strip(w, lb), (0, 0)); out.paste(b2, (0, 46)); out.paste(strip(w, la), (w + 10, 0)); out.paste(a2, (w + 10, 46))
    return out
SHOTS = [("CAM_CP076_empty_plateau_35mm", "CANDIDATE_CP076_plateau_start", "CP076 hero"),
         ("CAM_CP070_begin_walk_35mm", "CANDIDATE_CP076_plateau_sidefx_CP070", "side effect CP070"),
         ("CAM_CP072_footprint_35mm", "CANDIDATE_CP076_plateau_sidefx_CP072", "side effect CP072"),
         ("CAM_CP073_sphinx_steps_50mm", "CANDIDATE_CP076_plateau_sidefx_CP073", "side effect CP073"),
         ("CAM_CP075_layered_nsc_35mm", "CANDIDATE_CP076_plateau_sidefx_CP075", "side effect CP075")]
res = {}
for cam, stem, what in SHOTS:
    b = Image.open(os.path.join(SRC, f"before_{cam}.png")).convert("RGB"); a = Image.open(os.path.join(SRC, f"after_{cam}.png")).convert("RGB")
    lb, la = luma(b), luma(a); res[cam] = (round(lb, 2), round(la, 2))
    b.save(os.path.join(DST, stem + "_before.png")); a.save(os.path.join(DST, stem + "_after.png"))
    pair(b, a, [f"BEFORE live parknow-r02 {cam} (exp -0.8, luma {lb:.2f})", f"{what}: dud-fix v4 recipe, same session grouping"],
         [f"AFTER CANDIDATE parknow-r02_cp076plateau (exp -0.8, luma {la:.2f})", "D-PM-26..31: grounded, trees, terrace grass, mast"]).save(os.path.join(DST, stem + "_pair.png"))
    if cam == "CAM_CP076_empty_plateau_35mm":
        box = (0, 0, 1280, 500)   # wall line, trees, transmitter, floating-object zone
        pair(b, a, ["BEFORE detail: wall line + sky (floating trees / visitors)", f"luma {lb:.2f}"],
             ["AFTER detail: grounded trees on the upper terrace, scrub, 1956 mast", f"luma {la:.2f}"], scale=0.6, box=box).save(os.path.join(DST, stem + "_detail_pair.png"))
json.dump(res, open(os.path.join(HERE, "checks", "cp076_plateau_luma.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
