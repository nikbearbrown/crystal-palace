"""Overlay a section render of the model on Plate VI (the transverse section) and write a stacked comparison.

  python3 -I model/compare_plate_vi.py --render model/previews/slice01_v003_section.png --tag slice01_v003

The render must come from render_preview.py's `section` view (3000 x 800, orthographic, 440 ft wide, centre of
the width in the middle, camera height centred on z = 32 ft). The plate is registered with its own scale bar
(24.74 px/ft, tools/measure_plate_vi.py), its ground-floor line (y = 2697) and the mid-point of its outer
columns. That registration uses the plate's figures, which the model was also built from, so a close match is a
consistency check, not independent evidence; what it does show is where the model is missing parts the plate has.
Writes <tag>_overlay_plateVI.png (model in red on the plate) and <tag>_vs_plateVI.png (plate above, render below)
into the render's folder.
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser()
ap.add_argument("--render", required=True)
ap.add_argument("--tag", required=True)
ap.add_argument("--plate", default=str(Path(__file__).resolve().parents[2] / "source-scans" / "plates" / "plate-006.jpg"))
args = ap.parse_args()

PX = 24.74                    # plate px per ft (tools/measure_plate_vi.py)
FLOOR_Y = 2697.0              # ground-floor line on the plate
CX = (782.0 + 10821.2) / 2    # mid-point of the plate's outer column lines
W, H, FT_ACROSS, Z_CENTRE = 3000, 800, 440.0, 32.0
R = W / FT_ACROSS             # render px per ft

plate = Image.open(args.plate).convert("RGB")
render = Image.open(args.render).convert("RGB")
floor_row = H / 2 + Z_CENTRE * R
x0, x1 = CX - FT_ACROSS / 2 * PX, CX + FT_ACROSS / 2 * PX
y0 = FLOOR_Y - floor_row / R * PX
y1 = y0 + H / R * PX
crop = plate.crop((int(x0), int(y0), int(x1), int(y1))).resize((W, H), Image.LANCZOS)

mask = np.asarray(render.convert("L"), dtype=float) > 60
pc = np.asarray(crop).astype(float)
ov = pc.copy()
ov[mask] = 0.35 * pc[mask] + 0.65 * np.array([230, 40, 40])
out = Path(args.render).parent
Image.fromarray(ov.astype("uint8")).save(out / f"{args.tag}_overlay_plateVI.png")
both = Image.new("RGB", (W, 2 * H + 20), "white")
both.paste(crop, (0, 0))
both.paste(render, (0, H + 20))
both.save(out / f"{args.tag}_vs_plateVI.png")
print("wrote", out / f"{args.tag}_overlay_plateVI.png", "and", out / f"{args.tag}_vs_plateVI.png")
