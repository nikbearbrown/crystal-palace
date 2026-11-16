"""CP004 lily house CANDIDATE 2026-11-16: before/after pairs into the survey look/pairs_geo (python3 + PIL).
Before = live rounds/ch02.blend (59eca5d7), after = rounds/candidates/ch02_cp004lily.blend; both rendered by
scripts/render_cp004_candidate.sh with the live CP004 recipe (render_views.py, look v1 1840s / exterior_midday,
exposure from the look), 1920x1080, 48 spp, one camera per Blender session. Cameras not moved."""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "renders/candidates/cp004_lilyhouse_20261116")
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
HERO = "CP004_lily_tank_start"
SHOTS = [(HERO, "CANDIDATE_CP004_lily_house_tank", "CP004 hero (live cam)", "cam not moved"),
         ("CP004_learning_start", "CANDIDATE_CP004_sidefx_learning", "side effect: CP004_learning (not a live hero)", "cam unchanged"),
         ("CP004_lily_underside_start", "CANDIDATE_CP004_sidefx_lily_underside", "side effect: CP004_lily_underside (not a live hero)", "cam unchanged"),
         ("CP003_stove_nave_start", "CANDIDATE_CP004_sidefx_CP003_stove_nave", "side effect: CP003 stove_nave (LIVE hero of CP003)", "cam unchanged"),
         ("CP003_stove_rib_start", "CANDIDATE_CP004_sidefx_CP003_stove_rib", "side effect: CP003 stove_rib (not a live hero)", "cam unchanged")]
res = {}
for cam, stem, what, note in SHOTS:
    b = Image.open(os.path.join(SRC, "before", cam + ".png")).convert("RGB"); a = Image.open(os.path.join(SRC, "after", cam + ".png")).convert("RGB")
    lb, la = luma(b), luma(a); d = np.abs(arr(b) - arr(a)); px = int((d.max(2) > 8).sum())
    res[cam] = {"luma_before": round(lb, 2), "luma_after": round(la, 2), "max_diff": int(d.max()), "mean_diff": round(float(d.mean()), 3), "px_gt8": px, "size": list(b.size)}
    if cam != HERO and px == 0:
        res[cam]["pair"] = "none (no visible change: 0 px > 8)"; continue
    b.save(os.path.join(DST, stem + "_before.png")); a.save(os.path.join(DST, stem + "_after.png"))
    pair(b, a, [f"BEFORE live ch02 {cam} (1920x1080 48 spp, luma {lb:.2f})", f"{what}: live recipe (look v1 1840s, exterior_midday)"],
         [f"AFTER CANDIDATE ch02_cp004lily (luma {la:.2f})", f"CH07-CH16 lily house spring 1850; {note}"]).save(os.path.join(DST, stem + "_pair.png"))
    res[cam]["pair"] = stem + "_pair.png"
    if cam == HERO:
        box = (0, 380, 1920, 1080)
        pair(b, a, ["BEFORE detail: pads hover 0.6-0.85 ft above bright water,", "trestle legs + 4 iron columns stand in the tank"],
             ["AFTER detail: one Victoria plant, 19 leaves 3.6-5.1 ft on dark water,", "drainage notch, low red rims, 2 flowers; corner tanks"], scale=0.6, box=box).save(os.path.join(DST, stem + "_detail_pair.png"))
json.dump(res, open(os.path.join(HERE, "checks", "cp004_lilyhouse_pairs.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
