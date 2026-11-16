"""CP050 Cup Final 20 Apr 1895 CANDIDATE 2026-11-16: before/after pairs into the survey look/pairs_geo (python3 + PIL).
Before = live rounds/fb02_1895.blend (d8b263c0), after = rounds/candidates/fb02_1895_cp050cup.blend; both rendered by
scripts/render_cp050_candidate.sh with the live CP050 recipe (render_views.py, no people swap, file exposure 0.0),
1920x1080, 48 spp, one camera per Blender session. Cameras not moved."""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "renders/candidates/cp050_cupfinal_20261116")
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
HERO = "CP050_bank_1895_start"
SHOTS = [(HERO, "CANDIDATE_CP050_cup_final_1895_bank", "CP050 hero (live cam)", "cam not moved"),
         ("CP050_pavilion_1895_start", "CANDIDATE_CP050_sidefx_pavilion", "side effect: CP050_pavilion (not a live hero)", "cam unchanged")]
res = {}
for cam, stem, what, note in SHOTS:
    b = Image.open(os.path.join(SRC, "before", cam + ".png")).convert("RGB"); a = Image.open(os.path.join(SRC, "after", cam + ".png")).convert("RGB")
    lb, la = luma(b), luma(a); d = np.abs(arr(b) - arr(a)); px = int((d.max(2) > 8).sum())
    res[cam] = {"luma_before": round(lb, 2), "luma_after": round(la, 2), "max_diff": int(d.max()), "mean_diff": round(float(d.mean()), 3), "px_gt8": px, "size": list(b.size)}
    if cam != HERO and px == 0:
        res[cam]["pair"] = "none (no visible change: 0 px > 8)"; continue
    b.save(os.path.join(DST, stem + "_before.png")); a.save(os.path.join(DST, stem + "_after.png"))
    pair(b, a, [f"BEFORE live fb02_1895 {cam} (1920x1080 48 spp, luma {lb:.2f})", f"{what}: live recipe (render_views, exposure 0.0)"],
         [f"AFTER CANDIDATE fb02_1895_cp050cup (luma {la:.2f})", f"D-FB-CP050-01..10 FA Cup Final 20 Apr 1895; {note}"]).save(os.path.join(DST, stem + "_pair.png"))
    res[cam]["pair"] = stem + "_pair.png"
    if cam == HERO:
        box = (0, 560, 1920, 1080)
        pair(b, a, ["BEFORE detail: 3-box pastel 'variant' blocks on the bank,", "1851 lathe figures facing the lens, visitors on the pitch"],
             ["AFTER detail: people_lib 1890s caps/boaters/top hats facing the play,", "Villa claret/light-blue v WBA blue/white stripes, referee"], scale=0.6, box=box).save(os.path.join(DST, stem + "_detail_pair.png"))
json.dump(res, open(os.path.join(HERE, "checks", "cp050_cupfinal_pairs.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
