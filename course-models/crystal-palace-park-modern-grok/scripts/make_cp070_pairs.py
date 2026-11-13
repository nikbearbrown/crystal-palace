"""CP070 station CANDIDATE 2026-11-13: before/after pairs into the survey look/pairs_geo (python3 + PIL).
Before = live rounds/parknow-r02.blend (48fc01ec), after = rounds/candidates/parknow-r02_cp070station.blend; both rendered by
scripts/render_cp070_candidate.sh with each camera's live recipe (render_cp076_look.py, look v1.1 present/exterior_afternoon,
exposure -0.8; CP070/CP067 with pk_grass_plateau shown as in their live heroes, CP075 hidden), 1920x1080, 48 spp, one camera
per Blender session. NB the two CP070 cameras are MOVED in the candidate (reframe to the surviving Low Level station)."""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "renders/candidates/cp070_station_20261113")
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
SHOTS = [("CAM_CP070_begin_walk_35mm", "CANDIDATE_CP070_station_begin_walk", "CP070 hero", "cam MOVED: Parade/HL site -> Low Level station (sign, visitor in doorway)"),
         ("CAM_CP070_park_entry_35mm", "CANDIDATE_CP070_station_park_entry", "CP070 2nd cam", "cam MOVED: 8 m along the walk, into the park gate"),
         ("CAM_CP075_layered_nsc_35mm", "CANDIDATE_CP070_sidefx_CP075_layered_nsc", "side effect CP075", "cam unchanged: station roof on far right horizon, trees replaced"),
         ("CAM_CP067_dino_conservation_35mm", "CANDIDATE_CP070_sidefx_CP067_dino_conservation", "side effect CP067", "cam unchanged")]
res = {}
for cam, stem, what, note in SHOTS:
    b = Image.open(os.path.join(SRC, "before", cam + ".png")).convert("RGB"); a = Image.open(os.path.join(SRC, "after", cam + ".png")).convert("RGB")
    lb, la = luma(b), luma(a); d = np.abs(arr(b) - arr(a)); res[cam] = {"luma_before": round(lb, 2), "luma_after": round(la, 2),
        "max_diff": int(d.max()), "mean_diff": round(float(d.mean()), 3), "px_gt8": int((d.max(2) > 8).sum()), "size": list(b.size)}
    b.save(os.path.join(DST, stem + "_before.png")); a.save(os.path.join(DST, stem + "_after.png"))
    pair(b, a, [f"BEFORE live parknow-r02 {cam} (1920x1080 48 spp, luma {lb:.2f})", f"{what}: live recipe (look v1.1 present, exp -0.8)"],
         [f"AFTER CANDIDATE parknow-r02_cp070station (luma {la:.2f})", f"D-PM-33..41; {note}"]).save(os.path.join(DST, stem + "_pair.png"))
    if cam == "CAM_CP070_begin_walk_35mm":
        box = (960, 380, 1920, 1080)
        pair(b, a, ["BEFORE detail (right half, lower)", "parade road slab / footprint overlay"],
             ["AFTER detail: open doorcase + visitor, Rail Symbol 2 totem", "'CRYSTAL PALACE STATION' parapet board"], scale=1.0, box=box).save(os.path.join(DST, stem + "_detail_pair.png"))
json.dump(res, open(os.path.join(HERE, "checks", "cp070_station_pairs.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
