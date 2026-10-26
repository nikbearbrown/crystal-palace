"""Plate VI (transverse section): tier widths, bay pitch, heights, gutter pitch, concrete pads.

Run:  python3 -I measure_plate_vi.py

Covers CONTROL-DIMENSIONS D02, D03, D04, D06, D09, D10, D11, D12, D17. Read-only, no model.

Method
 1. Scale bar: tick marks of the 10-ft divisions -> px/ft, with the spread between divisions.
 2. Tier widths: outermost column lines of tiers 1, 2 and 3.
 3. Bay pitch: tier-3 column lines at one 24 ft step from each other.
 4. Heights: in a bay free of columns, horizontal lines are found; the floor line is the thickest line
    near the column feet; girder tops and the gallery floor are the thickest lines inside a +/-1 ft
    window around the stated height. Every candidate in each window is printed, so ambiguity shows.
 5. Gutter pitch: autocorrelation of the roof finials along the third-tier roof.
 6. Pads: below each tier-1 column, the dense speckled block (concrete) under the floor line.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I drops the script dir; common.py is ours
from common import (centres, dark_cols, dark_rows, fit_scale, groups, load_gray, pct, ticks)  # noqa: E402

a = load_gray("plate-006.jpg")

# 1. scale bar --------------------------------------------------------------------------------
tk = [t for t in ticks(a, 3219, 3228, 4000, 7800) if t > 4900]  # 10 ft, 20 ft, ...
PX, (lo, hi) = fit_scale(tk, 10, 10)
print(f"scale bar: {PX:.2f} px/ft from {len(tk)} ticks; per-10-ft spread {lo:.2f}-{hi:.2f} px/ft "
      f"(+/-{100*(hi-lo)/2/PX:.1f}%)")


def ft(px):
    return px / PX


# 2. tier widths ------------------------------------------------------------------------------
t1 = [c for c, _ in dark_cols(a, 2300, 2600, 0, 11630, 45, 0.85)]
t2 = [c for c, _ in dark_cols(a, 2000, 2250, 2200, 9400, 35, 0.7)]
t3 = [c for c, _ in dark_cols(a, 1150, 1950, 3800, 7800, 35, 0.5)]
for name, stated, lines in (("D02 tier 1 width", 408, t1), ("D03 tier 2 width", 264, t2),
                            ("D04 tier 3 width", 120, t3)):
    w = ft(lines[-1] - lines[0] if name != "D02 tier 1 width" else max(lines) - min(lines))
    print(f"{name}: stated {stated} ft, measured {w:.1f} ft ({pct(w, stated):+.2f}%)")

# 3. bay pitch (tier 3), stepping from the left edge by ~24 ft and snapping to the nearest line -
want = 24 * PX
col = [t3[0]]
for _ in range(5):
    nxt = min(t3, key=lambda x: abs(x - (col[-1] + want)))
    col.append(nxt)
gaps = np.diff(col)
print(f"D06 bay pitch (tier 3): gaps {[round(float(g), 1) for g in gaps]} px, mean {gaps.mean():.1f} px = "
      f"{ft(gaps.mean()):.2f} ft (stated 24)")

# 4. heights ----------------------------------------------------------------------------------
BAY = (5000, 5420)  # between two tier-3 columns
rows = dark_rows(a, 900, 2900, BAY[0], BAY[1], 30, 0.55)
floor_c = [(y, w) for y, w in rows if 2600 < y < 2800]
floor = max(floor_c, key=lambda r: r[1])[0]
print(f"floor line: y = {floor:.1f} (thickest of {[(round(y, 1), w) for y, w in floor_c]})")


def window(h_ft, tol=1.0):
    y0 = floor - h_ft * PX
    cand = [(y, w) for y, w in rows if abs(y - y0) < tol * PX]
    best = max(cand, key=lambda r: (r[1], -abs(r[0] - y0))) if cand else None
    return y0, cand, best


tops = {}
for label, stated, h in (("tier 3 girder top", "62 ft 2 in", 62 + 2 / 12),
                         ("tier 2 girder top", "42 ft 2 in", 42 + 2 / 12),
                         ("tier 1 girder top", "22 ft 2 in", 22 + 2 / 12),
                         ("gallery floor", "22 ft 11 in", 22 + 11 / 12)):
    y0, cand, best = window(h)
    note = ""
    if label == "tier 1 girder top" and tops.get("tier 2 girder top") and tops.get("tier 3 girder top"):
        # the tier-1 and gallery-floor windows overlap (9 in apart), so the thickest line would be the
        # gallery floor; instead take the candidate nearest to one tier-spacing below tier 2
        pred = tops["tier 2 girder top"][0] + (tops["tier 2 girder top"][0] - tops["tier 3 girder top"][0])
        best = min(cand, key=lambda r: abs(r[0] - pred))
        note = f" [nearest to the tier-2 + tier-spacing prediction y={pred:.1f}, so it assumes 20 ft spacing]"
    tops[label] = best
    if best:
        print(f"{label}: stated {stated}; chosen y={best[0]:.1f} (width {best[1]}) -> "
              f"{ft(floor - best[0]):.2f} ft{note}; candidates "
              f"{[(round(y, 1), w, round(ft(floor - y), 2)) for y, w in cand]}")
if tops["tier 3 girder top"] and tops["tier 2 girder top"]:
    sp = ft(tops["tier 2 girder top"][0] - tops["tier 3 girder top"][0])
    print(f"tier 3 -> tier 2 girder-top spacing: {sp:.2f} ft (20 ft expected)")
if tops["tier 3 girder top"]:
    # girder depth: bottom flange line is the next strong line within ~2.4-3.6 ft below the top flange
    y = tops["tier 3 girder top"][0]
    below = [(yy, w) for yy, w in rows if 2.4 * PX < yy - y < 3.6 * PX]
    print(f"D10 girder depth (tier 3): lines 2.4-3.6 ft below the top flange "
          f"{[(round(yy, 1), w, round(ft(yy - y), 2)) for yy, w in below]}  (3 ft stated; "
          f"lines are candidates, not a single reading)")

# 5. gutter pitch: autocorrelation of finials along the tier-3 roof ----------------------------
band = a[1065:1100, 4300:7320]
sig = (band < np.median(band) - 35).sum(axis=0).astype(float)
sig -= sig.mean()
ac = np.correlate(sig, sig, "full")[len(sig) - 1:]
lag = 150 + int(np.argmax(ac[150:250]))
print(f"D09 gutter pitch: autocorrelation peak at {lag} px = {ft(lag):.2f} ft (8 ft stated)")

# 6. concrete pads -----------------------------------------------------------------------------
pitch = (max(t1) - min(t1)) / 17
print(f"pads: tier-1 column pitch {pitch:.1f} px = {ft(pitch):.2f} ft (24 ft expected, 17 bays)")
readings = []
for k in range(18):
    xc = min(t1) + k * pitch
    x0, x1 = int(xc - 90), int(min(xc + 90, a.shape[1] - 1))
    b = a[2740:3060, x0:x1]
    dark = b < np.median(b) - 35
    ys = np.where(dark.sum(axis=1) > 14)[0]
    if not len(ys):
        continue
    grp = max([g for g in groups(ys, 6)], key=len)
    top, bot = 2740 + grp[0], 2740 + grp[-1]
    cols = np.where(dark[grp[0]:grp[-1] + 1].sum(axis=0) > len(grp) * 0.3)[0]
    width = (cols.max() - cols.min()) if len(cols) else 0
    readings.append((k, float(ft(top - floor)), float(ft(bot - floor)), float(ft(bot - top)), float(ft(width))))
print("pads, all columns (k, top below floor, bottom below floor, thickness, width), in ft:")
for r in readings:
    print("  ", r[0], [round(v, 2) for v in r[1:]])
clean = [r for r in readings if 1.2 <= r[1] <= 2.1 and 1.0 <= r[3] <= 3.5 and 1.4 <= r[4] <= 4.0]
print(f"D17 clean readings (top 1.2-2.1 ft below floor, thickness 1-3.5 ft, width 1.4-4 ft): "
      f"{len(clean)} columns; thickness {min(r[3] for r in clean):.2f}-{max(r[3] for r in clean):.2f} ft, "
      f"width {min(r[4] for r in clean):.2f}-{max(r[4] for r in clean):.2f} ft (text: depth 1 to 4 ft)")
