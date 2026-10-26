"""Plate XX (Fig. 1, half of the strong deep truss): panel length, half length, depth.

Run:  python3 -I measure_plate_xx.py

Covers CONTROL-DIMENSIONS D19 (72 ft truss, 6 ft deep; the plate prints "36'. 0"" for half the truss
and "6'. 0"" for its depth). Read-only, no model.

Method
 1. Ruler: the vertical posts of the truss are a panel apart; the plate labels each panel "8'. 0"" (the
    diagonals carry it), so the mean post spacing / 8 ft gives px/ft. The scale bar for elevations
    (0-20 ft) was read by eye on a preview at about 148 px/ft, in agreement; automatic tick detection
    was not attempted.
 2. Half length: from the dashed centre line of the column (at the left edge of the sheet) to the
    dashed centre line of the truss at the right. Candidates for the column line are printed, since the
    left edge carries the column body, its centre line, and the paper edge.
 3. Depth: from the top edge of the top rail to the bottom edge of the bottom rail, with the
    candidate lines printed.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I drops the script dir; common.py is ours
from common import dark_cols, dark_rows, load_gray, pct  # noqa: E402

a = load_gray("plate-020.jpg")

# 1. ruler: the posts -----------------------------------------------------------------------------
cols = dark_cols(a, 800, 1500, 0, 5779, 35, 0.5, gap=70)  # each post is drawn as three close lines
posts = [x for x, w in cols if 1100 < x < 5000]
gaps = np.diff(posts)
PX = float(np.mean(gaps)) / 8
print(f"posts at x = {[round(p) for p in posts]}; gaps {[round(float(g)) for g in gaps]} px; "
      f"8 ft per panel -> {PX:.1f} px/ft (spread {gaps.min() / 8:.1f}-{gaps.max() / 8:.1f})")

# 2. half length --------------------------------------------------------------------------------
cl_truss = next(x for x, w in dark_cols(a, 700, 1700, 5300, 5450, 30, 0.2))
print(f"centre line of the truss: x = {cl_truss:.0f}; last post to the centre line "
      f"{(cl_truss - posts[-1]) / PX:.2f} ft; first post to the centre line {(cl_truss - posts[0]) / PX:.2f} ft "
      f"(28 ft if the first post stands 8 ft from the column centre line)")
left = [x for x, w in dark_cols(a, 700, 1700, 0, 400, 30, 0.3) if 80 < x < 220]
for x in left:
    L = (cl_truss - x) / PX
    print(f"  from the left-edge line at x={x:.0f}: {L:.2f} ft ({pct(L, 36):+.1f}% vs 36 ft printed)")

# 3. depth --------------------------------------------------------------------------------------
rows = dark_rows(a, 600, 1800, 1300, 5200, 25, 0.08)
top = [(y, w) for y, w in rows if 700 < y < 830]       # the top rail is a thick band; width = its height
bot = [(y, w) for y, w in rows if y > 1500]
print(f"top rail band {[(round(y), w) for y, w in top]}; bottom rail lines {[(round(y), w) for y, w in bot]}")
top_edge = top[0][0] - top[0][1] / 2
bot_edge = bot[-1][0] + bot[-1][1] / 2
d_out = (bot_edge - top_edge) / PX
d_cen = (bot[-2][0] - top[0][0]) / PX
print(f"D19 depth: outer edge of top rail ({top_edge:.0f}) to outer edge of bottom rail ({bot_edge:.0f}) = "
      f"{d_out:.2f} ft ({pct(d_out, 6):+.1f}% vs 6 ft printed); rail centre to rail centre about {d_cen:.2f} ft")
