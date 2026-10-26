"""Plate XVIII (transept roof, Fig. 1): radius of the transept vault from its scale bar.

Run:  python3 -I measure_plate_xviii.py

Covers CONTROL-DIMENSIONS D20 (extrados diameter 74 ft 4 in; rib depth 1 ft 6 in) and, through it,
D21 (37-ft radius). Read-only, no model.

Method
 1. Scale bar ("Scale for Transverse and Longitudinal Sections", 0-30 ft): 1-ft ticks of the sub-scale
    and the long ticks at 0, 10, 20 and 30 ft -> px/ft and its spread.
 2. The vault is a quarter circle springing from the dashed horizontal axis. The radius is the distance
    from that axis to the top of the extrados at the centre line of the vault.
 3. The rib depth is looked for as lines 1.3-1.7 ft below the top of the extrados at the crown.

An automatic circle fit (RANSAC on edge pixels, and a radial search for the outer edge) was tried and
abandoned: the sheet carries other drawings (Figs. 4, 6, 7, 9-14) and the rib is hatched, so those fits
returned radii from 2,070 to 2,215 px. The springing axis and the crown are therefore found as lines in
narrow windows chosen by looking at the plate, and every candidate line is printed.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I drops the script dir; common.py is ours
from common import centres, dark_rows, fit_scale, load_gray, pct  # noqa: E402

a = load_gray("plate-018.jpg")

# 1. scale bar ----------------------------------------------------------------------------------
band = a[3320:3338, 2300:4900]
c = (band < np.median(band) - 30).sum(axis=0)
cand = [m for m, _ in centres(np.where(c >= 0.6 * band.shape[0])[0] + 2300, 3)]
sub = [x for x in cand if 2350 < x < 3000]  # the 1-ft ticks of the sub-scale, 10 ft ... 0 ft
zero = max(sub)  # the right-hand end of the sub-scale is 0 ft
sub_gaps = np.diff(sorted(sub))
approx = 58.5
longs = [zero]
for n in (1, 2, 3):
    target = zero + n * 10 * approx
    longs.append(min(cand, key=lambda x: abs(x - target)))
PX, (lo, hi) = fit_scale(longs, 10, 0)
print(f"scale bar: 0/10/20/30 ft ticks at x = {[round(x) for x in longs]} -> {PX:.2f} px/ft; "
      f"per-10-ft spread {lo:.2f}-{hi:.2f} px/ft (+/-{100*(hi-lo)/2/PX:.1f}%); "
      f"sub-scale 1-ft ticks give {np.median(sub_gaps):.1f} px/ft")

# 2. springing axis and crown -------------------------------------------------------------------
axis_c = dark_rows(a, 2550, 2800, 3000, 3900, 35, 0.25)
axis = max(axis_c, key=lambda r: r[1])[0]
print(f"springing axis (dashed line): y = {axis:.0f} (candidates {[(round(y), w) for y, w in axis_c]})")
crown_c = [(y, w) for y, w in dark_rows(a, 250, 800, 3980, 4080, 45, 0.5) if y > 350]
print(f"crown: horizontal lines at the centre line, below the sheet border: "
      f"{[(round(y), w) for y, w in crown_c]}")
crown = crown_c[0][0]  # the topmost line is the extrados
R = (axis - crown) / PX
print(f"D20 extrados radius: ({axis:.0f} - {crown:.0f}) = {axis - crown:.0f} px = {R:.2f} ft "
      f"-> diameter {2 * R:.2f} ft (stated 74 ft 4 in = 74.33 ft; {pct(2 * R, 74 + 4 / 12):+.2f}%); "
      f"37-ft radius (D21): {pct(R, 37):+.2f}%")
print("  sensitivity: using the next candidate lines as the crown gives "
      f"{[round(2 * (axis - y) / PX, 2) for y, _ in crown_c[:4]]} ft diameter")

# 3. rib depth ----------------------------------------------------------------------------------
below = [(y, w) for y, w in crown_c if 1.3 * PX < y - crown < 1.7 * PX]
print(f"rib depth (1 ft 6 in stated): lines 1.3-1.7 ft below the extrados: "
      f"{[(round(y), w, round((y - crown) / PX, 2)) for y, w in below]} (candidates, not a single reading)")
