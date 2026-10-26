"""Overlay a stair section render on Plate XV (the section along the flights) and write a stacked comparison.

  python3 -I model/compare_plate_xv.py --render model/previews/west02_v001_stairsec.png --tag west02_v001

The render must come from render_preview.py's `stairsec` view with --flat (2800 x 1500, orthographic, 56 ft across
centred on the avenue's middle line, 30 ft high centred on z = 14 ft, 50 px/ft). The plate is registered on its ground
line (row 2355.8) and the middle main column (x 6167), with the vertical scale from its scale bar (73.65 px/ft,
tools-style reading, +-0.2%). The horizontal scale is taken from the plate's three main columns, which stand 1,792 and
1,780 px apart: 74.4 px/ft if they are 24 ft apart, 1% more than the bar (paper stretch). Both are printed with the
result so the reader sees what was assumed. The model was built from the same plate's figures, so this is a consistency
check, not independent evidence: it shows where the model's flights and landing leave the plate's.
Writes <tag>_overlay_plateXV.png (model in red on the plate) and <tag>_vs_plateXV.png (plate above, render below).
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser()
ap.add_argument("--render", required=True)
ap.add_argument("--tag", required=True)
ap.add_argument("--plate", default=str(Path(__file__).resolve().parents[2] / "source-scans" / "plates" / "plate-015.jpg"))
ap.add_argument("--px-h", type=float, default=74.4, help="plate px per ft along the width (columns)")
ap.add_argument("--px-v", type=float, default=73.65, help="plate px per ft up the height (scale bar)")
args = ap.parse_args()

W, H, RPX = 2800, 1500, 50.0          # render size and px per ft
FT_W, FT_H, Z_CENTRE = W / RPX, H / RPX, 14.0
GROUND_Y, CENTRE_X = 2355.8, 6167.0   # plate pixel of the ground line and of the middle main column
plate = Image.open(args.plate).convert("RGB")
render = Image.open(args.render).convert("RGB")
x0, x1 = CENTRE_X - FT_W / 2 * args.px_h, CENTRE_X + FT_W / 2 * args.px_h
y_top = GROUND_Y - (Z_CENTRE + FT_H / 2) * args.px_v
y_bot = GROUND_Y - (Z_CENTRE - FT_H / 2) * args.px_v
crop = plate.crop((int(x0), int(y_top), int(x1), int(y_bot))).resize((W, H), Image.LANCZOS)
mask = np.asarray(render.convert("L"), dtype=float) > 60
pc = np.asarray(crop).astype(float)
ov = pc.copy()
ov[mask] = 0.35 * pc[mask] + 0.65 * np.array([230, 40, 40])
out = Path(args.render).parent
Image.fromarray(ov.astype("uint8")).save(out / f"{args.tag}_overlay_plateXV.png")
both = Image.new("RGB", (W, 2 * H + 20), "white")
both.paste(crop, (0, 0))
both.paste(render, (0, H + 20))
both.save(out / f"{args.tag}_vs_plateXV.png")
print(f"plate scale {args.px_h} px/ft across, {args.px_v} px/ft up; wrote {out / (args.tag + '_overlay_plateXV.png')}")
