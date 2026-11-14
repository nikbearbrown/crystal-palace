"""CP066 NSC 1964-67 CANDIDATE 2026-11-14: before/after pairs into the survey look/pairs_geo (python3 + PIL).
Before = live rounds/park60-r17.blend (9ea1c796), after = rounds/candidates/park60-r17_cp066nsc64.blend; both rendered by
scripts/render_cp066_candidate.sh with the live CP066 recipe (render_cp076_look.py CP066, look v1.1 present /
exterior_afternoon, exposure -0.8), 1920x1080, 48 spp, one camera per Blender session. Cameras not moved."""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "renders/candidates/cp066_nsc64_20261114")
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
SHOTS = [("CAM_CP066_nsc_stadium_35mm", "CANDIDATE_CP066_nsc1964_stadium", "CP066 hero (live cam)", "cam not moved"),
         ("CAM_CP066_nsc_wide_35mm", "CANDIDATE_CP066_sidefx_nsc_wide", "side effect: CP066 nsc_wide (not a live hero)", "cam unchanged"),
         ("CAM_CP066_nsc_hall_35mm", "CANDIDATE_CP066_sidefx_nsc_hall", "side effect: CP066 nsc_hall (not a live hero)", "cam unchanged"),
         ("CAM_CP065_hl_closed_35mm", "CANDIDATE_CP066_sidefx_CP065_hl_closed_park60", "side effect: park60 CP065 hl_closed (not live; CP065 is on park54)", "cam unchanged"),
         ("CAM_CP065_subway_threshold_35mm", "CANDIDATE_CP066_sidefx_CP065_subway_threshold_park60", "side effect: park60 CP065 subway (not live; CP065 is on park54)", "cam unchanged")]
res = {}
for cam, stem, what, note in SHOTS:
    b = Image.open(os.path.join(SRC, "before", cam + ".png")).convert("RGB"); a = Image.open(os.path.join(SRC, "after", cam + ".png")).convert("RGB")
    lb, la = luma(b), luma(a); d = np.abs(arr(b) - arr(a)); px = int((d.max(2) > 8).sum())
    res[cam] = {"luma_before": round(lb, 2), "luma_after": round(la, 2), "max_diff": int(d.max()), "mean_diff": round(float(d.mean()), 3), "px_gt8": px, "size": list(b.size)}
    if cam != "CAM_CP066_nsc_stadium_35mm" and px == 0:
        res[cam]["pair"] = "none (no visible change: 0 px > 8)"; continue
    b.save(os.path.join(DST, stem + "_before.png")); a.save(os.path.join(DST, stem + "_after.png"))
    pair(b, a, [f"BEFORE live park60-r17 {cam} (1920x1080 48 spp, luma {lb:.2f})", f"{what}: live recipe (look v1.1 present, exp -0.8)"],
         [f"AFTER CANDIDATE park60-r17_cp066nsc64 (luma {la:.2f})", f"D-PM-42..49 NSC 1964-67; {note}"]).save(os.path.join(DST, stem + "_pair.png"))
    res[cam]["pair"] = stem + "_pair.png"
    if cam == "CAM_CP066_nsc_stadium_35mm":
        box = (180, 260, 1500, 1000)
        pair(b, a, ["BEFORE detail", "white boxes, black tops, square red ring"],
             ["AFTER detail: 440 yd cinder oval, 1964 West Stand + canopy,", "open east terracing/banks, athletes + spectators"], scale=0.75, box=box).save(os.path.join(DST, stem + "_detail_pair.png"))
json.dump(res, open(os.path.join(HERE, "checks", "cp066_nsc64_pairs.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
