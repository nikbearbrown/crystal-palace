"""CP074 Geological Court present-day CANDIDATE 2026-11-16: before/after pairs into the survey look/pairs_geo (python3 + PIL).
Before = rounds/parknow-r01.blend (fb640758; the blend the live CP074 hero was rendered from), after =
rounds/candidates/parknow-r01_cp074geocourt.blend; both rendered by scripts/render_cp074_candidate.sh with the live recipe
(survey look/apply_render.py, look v1.1 present/exterior_afternoon, exposure -0.8, --no-people), 1920x1080, 48 spp, one camera
per Blender session. No camera is moved."""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "renders/candidates/cp074_geocourt_20261116")
DST = "/workspace/crystal-palace-survey/look/pairs_geo"
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
def arr(im): return np.asarray(im.convert("RGB")).astype(float)
def luma(im): a = arr(im); return float((0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).mean())
def strip(w, lines):
    s = Image.new("RGB", (w, 50), (16, 16, 16)); d = ImageDraw.Draw(s)
    for i, t in enumerate(lines): d.text((6, 3 + 23 * i), t, font=F, fill=(235, 235, 235))
    return s
def pair(b, a, lb, la, scale=0.5, box=None):
    if box: b, a = b.crop(box), a.crop(box)
    w, h = int(b.width * scale), int(b.height * scale); b2, a2 = b.resize((w, h), Image.LANCZOS), a.resize((w, h), Image.LANCZOS)
    out = Image.new("RGB", (2 * w + 10, h + 50), (0, 0, 0))
    out.paste(strip(w, lb), (0, 0)); out.paste(b2, (0, 50)); out.paste(strip(w, la), (w + 10, 0)); out.paste(a2, (w + 10, 50))
    return out
SHOTS = [("CAM_CP074_dinosaurs_35mm", "CANDIDATE_CP074_geocourt_now_dinosaurs", "CP074 hero", "cam unchanged; painted sculptures, gravel, rocks, ferns/cycads, mature trees"),
         ("CAM_CP074_iguanodon_50mm", "CANDIDATE_CP074_sidefx_iguanodon_50mm", "side effect CP074 50 mm (no live hero)", "cam unchanged"),
         ("CAM_CP075_layered_nsc_35mm", "CANDIDATE_CP074_sidefx_CP075_layered_nsc_r01", "side effect CP075 on r01 (live hero is r02)", "cam unchanged: far tree line darker/mature"),
         ("CAM_CP066_nsc_wide_35mm", "CANDIDATE_CP074_sidefx_CP066_nsc_wide_r01", "side effect CP066 nsc_wide on r01 (no live hero)", "cam unchanged: far tree line darker/mature"),
         ("CAM_CP072_footprint_35mm", "CANDIDATE_CP074_sidefx_CP072_footprint", "side effect CP072 (live hero from r01)", "cam unchanged")]
res = {}
for cam, stem, what, note in SHOTS:
    b = Image.open(os.path.join(SRC, "before", cam + ".png")).convert("RGB"); a = Image.open(os.path.join(SRC, "after", cam + ".png")).convert("RGB")
    lb, la = luma(b), luma(a); d = np.abs(arr(b) - arr(a)); res[cam] = {"luma_before": round(lb, 2), "luma_after": round(la, 2),
        "max_diff": int(d.max()), "mean_diff": round(float(d.mean()), 3), "px_gt8": int((d.max(2) > 8).sum()), "size": list(b.size)}
    b.save(os.path.join(DST, stem + "_before.png")); a.save(os.path.join(DST, stem + "_after.png"))
    pair(b, a, [f"BEFORE live parknow-r01 {cam} (1920x1080 48 spp, luma {lb:.2f})", f"{what}: live recipe (look v1.1 present, exp -0.8)"],
         [f"AFTER CANDIDATE parknow-r01_cp074geocourt (luma {la:.2f})", f"D-PM-50..57; {note}"]).save(os.path.join(DST, stem + "_pair.png"))
    if cam == "CAM_CP074_dinosaurs_35mm":
        box = (240, 240, 1200, 780)
        pair(b, a, ["BEFORE detail: recumbent Iguanodon", "cream blob on 1854 young turf"],
             ["AFTER detail: present-day paint, Wealden gravel + sandstone", "ferns, Cycas, rough sward"], scale=1.0, box=box).save(os.path.join(DST, stem + "_detail_pair.png"))
json.dump(res, open(os.path.join(HERE, "checks", "cp074_geocourt_pairs.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
