"""mean luma (Rec.709, 8-bit sRGB values) before/after + max abs diff, and labelled side-by-side pairs.
  python3 scripts/pair_luma.py renders/candidates/scanprops_20261109 /workspace/crystal-palace-survey/look/pairs_geo"""
import sys, os
from PIL import Image, ImageChops, ImageDraw
import numpy as np
O, PAIRS = sys.argv[1], sys.argv[2]
def luma(im):
    a = np.asarray(im.convert("RGB")).astype(np.float64); return float((0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).mean())
for shot in ["CP025_visitors_start", "CP025_visitors_end", "EX_lineup_start", "CP025_july_start", "CP025_case_start"]:
    b = Image.open(os.path.join(O, "before", shot + ".png")).convert("RGB"); a = Image.open(os.path.join(O, "after", shot + ".png")).convert("RGB")
    lb, la = luma(b), luma(a); mx = int(np.asarray(ImageChops.difference(a, b)).max())
    # exposure check: luma outside the changed (prop) pixels, mask = |diff| > 12 dilated by 9 px
    from PIL import ImageFilter
    m = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > 12 else 0).filter(ImageFilter.MaxFilter(19))
    keep = np.asarray(m) == 0
    def lm(im): x = np.asarray(im).astype(np.float64); y = 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]; return float(y[keep].mean())
    ob, oa = lm(b), lm(a)
    print(f"{shot}: luma before {lb:.2f} after {la:.2f} ({100*(la-lb)/lb:+.2f}%) max_diff {mx} | outside prop mask ({100*keep.mean():.1f}% of frame) {ob:.2f} -> {oa:.2f} ({100*(oa-ob)/ob:+.2f}%)")
    if shot.startswith("CP025_july") or shot.startswith("CP025_case"): continue
    w, h = b.size; pair = Image.new("RGB", (w * 2 + 16, h + 64), (20, 20, 20)); pair.paste(b, (0, 64)); pair.paste(a, (w + 16, 64))
    d = ImageDraw.Draw(pair)
    d.text((16, 20), f"BEFORE live e02  {shot}  luma {lb:.1f}", fill=(230, 230, 230))
    d.text((w + 32, 20), f"AFTER CANDIDATE e02_scanprops (Greek Slave, Elkington cabinet, W&B vase)  luma {la:.1f}  - not live", fill=(230, 230, 230))
    pair.save(os.path.join(PAIRS, f"CANDIDATE_{shot}_scanprops_pair.png"))
