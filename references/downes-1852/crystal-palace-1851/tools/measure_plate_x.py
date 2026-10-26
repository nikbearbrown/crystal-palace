"""Plate X (Fig. 3, cast-iron girder under the roof): length, face-to-face length, depth.

Run:  python3 -I measure_plate_x.py

Covers CONTROL-DIMENSIONS D06 (24 ft) and D10 (girder depth 3 ft). Read-only, no model.

Method
 1. Ruler: the dimension printed on the plate, "24'. 0"", between the dashed centre lines of the two
    columns. The sheet's own scale bar (0-8 ft) was read by eye as a cross-check (not automated).
 2. Length face to face of the girder, against the printed "23'. 3 1/4"".
 3. Depth: the girder's top and bottom flange lines, reported as candidates. The stated 3 ft is the
    depth between the bearing surfaces; the outer lines include the flange thickness, so the overall
    figure should come out a little above 3 ft and the inner-line figure at or just under it.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I drops the script dir; common.py is ours
from common import dark_cols, dark_rows, load_gray, pct  # noqa: E402

a = load_gray("plate-010.jpg")

# 1. ruler --------------------------------------------------------------------------------------
cols = dark_cols(a, 1850, 2400, 100, 5600, 30, 0.55)
cl_left = next(x for x, w in cols if 100 <= x <= 180)
cl_right = next(x for x, w in cols if 5400 <= x <= 5470)
face_left = next(x for x, w in cols if 200 <= x <= 240)
face_right = next(x for x, w in cols if 5320 <= x <= 5370)
PX = (cl_right - cl_left) / 24
print(f"dashed centre lines x = {cl_left:.0f} and {cl_right:.0f}; printed 24 ft between them -> {PX:.1f} px/ft")

# The sheet's own scale bar for plans and elevations (0-8 ft) was read by eye on a preview at about 221
# px/ft, agreeing with this ruler; automatic tick detection was tried and dropped (the numerals above
# the bar and the 1-inch sub-scale produce 23 false candidates).

# 2. length -------------------------------------------------------------------------------------
L = (face_right - face_left) / PX
print(f"girder face to face: x {face_left:.0f}..{face_right:.0f} = {L:.2f} ft = {int(L)} ft {(L % 1) * 12:.1f} in "
      f"(printed 23 ft 3 1/4 in = 23.27 ft; {pct(L, 23 + 3.25 / 12):+.2f}%)")

# 3. depth --------------------------------------------------------------------------------------
rows = dark_rows(a, 1650, 2600, 300, 5300, 30, 0.12)
top = [(y, w) for y, w in rows if 1770 < y < 1792]    # outer line and flange underside of the top flange
bot = [(y, w) for y, w in rows if 2438 < y < 2480]    # upper face and outer line of the bottom flange
print(f"top flange lines: {[(round(y), w) for y, w in top]}")
print(f"bottom flange lines: {[(round(y), w) for y, w in bot]}  (lines between 2410 and 2425 belong to the web)")
pairs = sorted(((b_[0] - t[0]) / PX, t[0], b_[0]) for t in top for b_ in bot)
print("depth for each top/bottom pair (ft):", [(round(d, 2), round(t), round(b_)) for d, t, b_ in pairs])
inner = (bot[0][0] - top[-1][0]) / PX
outer = (bot[-1][0] - top[0][0]) / PX
print(f"D10 depth: between the inner flange lines {inner:.2f} ft ({pct(inner, 3):+.1f}% vs 3 ft, the stated "
      f"bearing-surface depth); overall between the outer lines {outer:.2f} ft (flanges included)")
print(f"ratio girder face-to-face length / inner depth = {(face_right - face_left) / (bot[0][0] - top[-1][0]):.2f} "
      f"(23.27 / 3 = 7.76 expected)")
