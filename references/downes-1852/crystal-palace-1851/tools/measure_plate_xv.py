"""Plate XV (the staircases: general plan, and the section through the stairs): the figures the model's stair is built to.

Run:  python3 -I measure_plate_xv.py

Covers CONTROL-DIMENSIONS D27 (landing width), D31 (landing level), D32 (flight run) and the stair rows of
DEPARTURES-LEDGER.md. Read-only, no model.

Method
 1. Ruler: the plate's own "Scale for Plans and Section" bar, 0 to 20 ft: the 0, 10 and 20 ft ticks are found in
    windows seeded by looking at the plate (each reported with every candidate in its window).
 2. Vertical datum: the ground-floor line of the section. Heights are measured up from it.
 3. In the section: the top and underside of the landing beam, and the level of the main gallery floor line (a check:
    it should come out at the printed 22 ft 11 in).
 4. In the section: the three main columns (centre lines), 24 ft apart in life. They give a horizontal scale that
    differs from the bar by about 1 per cent (the sheet is stretched); both are printed.
 5. In the plan: the riser lines of the first flight, counted and spaced, in feet by the bar. The label "21" stands
    beyond the last line, on the landing, so the 21 steps are 20 treads and the landing.
What stays read by eye: the tread heights on the section (6.49 in mean, from six nosings), the handrail height above the
nosing line (2.7 ft), the string depth (about 1.15 ft square to the slope), and the well-hole and landing positions on
Plates I and II. They are in MEASUREMENTS.md.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I drops the script dir; common.py is ours
from common import centres, dark_cols, dark_rows, load_gray  # noqa: E402

a = load_gray("plate-015.jpg")
print(f"plate-015.jpg {a.shape[1]} x {a.shape[0]} px")


def strongest_col(x_seed, half, y0, y1):
    """The darkest vertical stroke within x_seed +- half over rows y0:y1: (x, dark fraction)."""
    b = a[y0:y1, x_seed - half:x_seed + half + 1]
    c = (b < np.median(a[y0:y1, x_seed - 60:x_seed + 60]) - 40).sum(axis=0) / b.shape[0]
    k = int(np.argmax(c))
    return x_seed - half + k, float(c[k])


# 1. ruler --------------------------------------------------------------------------------------------------
# 0 and 20 ft ticks stand above the bar's lines; the 10 ft tick is found lower, where the numerals do not reach.
t0 = strongest_col(1575, 14, 3385, 3445)
t10 = strongest_col(837, 14, 3455, 3480)
t20 = strongest_col(3047, 14, 3385, 3445)
print("scale bar ticks (x px, dark fraction): 0 ft", (t0[0], round(t0[1], 2)), "| 10 ft", (t10[0], round(t10[1], 2)),
      "| 20 ft", (t20[0], round(t20[1], 2)))
bar_10 = (t0[0] - t10[0]) / 10   # the left half of the bar runs 0 -> 10 to the left
bar_20 = (t20[0] - t0[0]) / 20
PX = (bar_10 + bar_20) / 2
print(f"scale bar: 0-10 ft = {bar_10:.2f} px/ft; 0-20 ft = {bar_20:.2f} px/ft; used below: {PX:.2f} px/ft "
      f"(the two baselines differ by {abs(bar_10 - bar_20) / PX:.1%})")

# 2. vertical datum: the ground-floor line, which tilts across the sheet (the scan is rotated about 0.2 degree) --------
gx, gy = [], []
for lo, hi in ((5000, 5500), (6500, 7000), (7200, 7700)):
    r = dark_rows(a, 2330, 2385, lo, hi, 25, 0.7)
    print(f"ground-floor line, x {lo}-{hi}: rows {[(round(v, 1), w) for v, w in r]}")
    if r:
        gx.append((lo + hi) / 2)
        gy.append(r[0][0])
gk, gb = np.polyfit(gx, gy, 1)
ground = lambda x: gk * x + gb
print(f"ground line: row = {gk:.5f} x + {gb:.1f} (tilt {np.degrees(np.arctan(gk)):.2f} deg); "
      f"row {ground(4375):.1f} at the first column, {ground(6162):.1f} at the landing, {ground(7945):.1f} at the third")

# 3. landing beam and main gallery floor line ----------------------------------------------------------------
beam = sorted({round(r, 1) for r, w in dark_rows(a, 1490, 1600, 5930, 6120, 25, 0.9) + dark_rows(a, 1490, 1600, 6200, 6420, 25, 0.9)})
zl = lambda row: (ground(6162) - row) / PX
print("landing beam lines at the landing (row, z above ground ft):", [(r, round(zl(r), 2)) for r in beam])
gal = [round(r, 1) for r, w in dark_rows(a, 560, 800, 4150, 4330, 25, 0.6)]
zg = lambda row: (ground(4200) - row) / PX
print("main gallery floor lines left of the first column (row, z ft):", [(r, round(zg(r), 2)) for r in gal])
if beam and gal:
    top_beam, top_gal = beam[0], gal[0]
    print(f"landing beam top {zl(top_beam):.2f} ft, gallery floor top {zg(top_gal):.2f} ft: "
          f"ratio {zl(top_beam) / zg(top_gal):.3f} (half = 0.500); printed gallery surface 22 ft 11 in = 22.92 ft")

# 4. the three main columns ----------------------------------------------------------------------------------
mid = []
for lo, hi in ((4300, 4450), (6100, 6230), (7900, 8010)):
    cs = dark_cols(a, 1880, 1960, lo, hi, 25, 0.7)
    xs = [x for x, w in cs]
    mid.append((min(xs) + max(xs)) / 2 if xs else float("nan"))
    print(f"  column window {lo}-{hi}: lines at {[round(x, 1) for x in xs]}  centre {mid[-1]:.1f}")
sp1, sp2 = mid[1] - mid[0], mid[2] - mid[1]
print(f"main column spacings: {sp1:.0f} and {sp2:.0f} px = {sp1 / PX:.2f} and {sp2 / PX:.2f} ft by the bar; "
      f"if 24 ft, {sp1 / 24:.1f} and {sp2 / 24:.1f} px/ft (horizontal stretch {np.mean([sp1, sp2]) / 24 / PX - 1:+.1%})")

# 5. plan: riser lines of the first flight -------------------------------------------------------------------
cs = dark_cols(a, 1700, 1950, 100, 1750, 22, 0.8)
xs = [x for x, w in cs]
print(f"plan riser lines found in rows 1700-1950, x 100-1750: {len(xs)}")
if len(xs) >= 2:
    d = np.diff(xs)
    print("  x:", [round(x) for x in xs])
    print(f"  spacing mean {d.mean():.1f} px (min {d.min():.0f}, max {d.max():.0f}) = {d.mean() / PX:.3f} ft; "
          f"first to last {xs[-1] - xs[0]:.0f} px = {(xs[-1] - xs[0]) / PX:.2f} ft over {len(xs) - 1} intervals")
    print("  (the 21st line, the landing edge, is dashed on the plate and is not found; with it the 21 lines span "
          f"{(xs[-1] - xs[0] + d.mean()) / PX:.2f} ft over 20 intervals)")
