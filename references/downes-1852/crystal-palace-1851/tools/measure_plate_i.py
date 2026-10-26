"""Plate I (plan of the ground floor): column grid pitch, overall length, north addition, avenues.

Run:  python3 -I measure_plate_i.py

Covers CONTROL-DIMENSIONS D01, D05, D07, D08. Read-only, no model.

Why the plan's own grid is the ruler: the sheet is warped (long lines run at -0.8 deg in the middle
and -1.4 to -2.1 deg on the left), so a single px/ft from the slanted scale bar is not trustworthy,
and rotating the image does not fix a warp. The column dots sit on a 24 ft grid, so the local dot
pitch gives a local scale. Lengths are integrated along x, bin by bin, using each bin's own pitch.

Method
 1. Find the column dots (small dark discs) and measure their horizontal pitch in 1,000 px bins.
 2. D01: distance between the east and west end walls, divided into bays with the local pitch.
 3. D05: the north addition: corner-to-corner length with the local pitch, and its depth by counting
    the 8 ft wall posts down its west end.
 4. D07, D08: pair spacings of dots on the same row in the crossing area, as multiples of 24 ft.
Seeds (where to look for walls) were chosen by looking at the plate; the wall positions themselves
are found by the script.
"""
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I drops the script dir; common.py is ours
from common import PLATES, groups, load_gray, pct  # noqa: E402

img = cv2.imread(str(PLATES / "plate-001.jpg"), cv2.IMREAD_GRAYSCALE)
a = img.astype(float)

# 1. dots --------------------------------------------------------------------------------------
s = 0.5
sm = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
diff = cv2.subtract(cv2.medianBlur(sm, 41), sm)
_, bw = cv2.threshold(diff, 40, 255, cv2.THRESH_BINARY)
n, lab, st, cen = cv2.connectedComponentsWithStats(bw)
pts = np.array([(cen[i][0] / s, cen[i][1] / s) for i in range(1, n)
                if 25 <= st[i][4] <= 120 and 5 <= st[i][2] <= 14 and 5 <= st[i][3] <= 14
                and abs(st[i][2] - st[i][3]) <= 3])
print(f"column dots found: {len(pts)}")


def pair_gaps(xlo, xhi, lo=100, hi=140):
    sel = pts[(pts[:, 0] >= xlo) & (pts[:, 0] < xhi)]
    g = []
    for p in sel:
        for q in sel:
            dx = q[0] - p[0]
            if lo < dx < hi and abs(q[1] - p[1]) < (0.03 * dx + 6):
                g.append(dx)
    return np.array(g)


BIN = 1000
edges = list(range(500, 10000, BIN))
pitch_bin = {}
for x0 in edges:
    g = pair_gaps(x0, x0 + BIN)
    pitch_bin[x0] = float(np.median(g)) if len(g) >= 15 else None
allg = pair_gaps(500, 9600)
GLOBAL = float(np.mean(allg))
print(f"dot pitch (24 ft): global mean {GLOBAL:.1f} px from {len(allg)} pairs; "
      f"by {BIN}-px bin {[(x, round(p, 1) if p else None) for x, p in pitch_bin.items()]}")


def feet(x_from, x_to):
    """Integrate x_from..x_to into feet with each bin's local pitch (24 ft per pitch)."""
    total, x = 0.0, x_from
    while x < x_to:
        b = x - ((x - 500) % BIN)
        nxt = min(x_to, b + BIN)
        p = pitch_bin.get(b) or GLOBAL
        total += (nxt - x) / p * 24
        x = nxt
    return total


# 2. D01: overall length -------------------------------------------------------------------------
def wall_x(y0, y1, x0, x1):
    b = a[y0:y1, x0:x1]
    c = (b < np.median(b) - 50).sum(axis=0) / b.shape[0]
    i = int(np.argmax(c))
    return x0 + i, float(c[i])


west = [wall_x(y, y + 300, 430, 620) for y in (1300, 2300)]
east = [wall_x(y, y + 300, 9450, 9640) for y in (1300, 2300)]
print(f"end walls: west x {[w[0] for w in west]} (strength {[round(w[1], 2) for w in west]}), "
      f"east x {[e[0] for e in east]} (strength {[round(e[1], 2) for e in east]})")
for (xw, _), (xe, _), tag in zip(west, east, ("y 1300-1600", "y 2300-2600")):
    L = feet(xw, xe)
    print(f"D01 length at {tag}: {xe - xw} px = {L:.0f} ft with local pitch "
          f"({pct(L, 1848):+.2f}% vs 1848); with the global mean pitch {(xe - xw) / GLOBAL * 24:.0f} ft")

# 3. D05: north addition -------------------------------------------------------------------------
def wall_near(seed, y0, y1, half=60):
    return wall_x(y0, y1, seed - half, seed + half)


wa, wc = wall_near(1562, 850, 1030), wall_near(6147, 790, 960)
print(f"north addition end walls: west x={wa[0]} (strength {wa[1]:.2f}), east x={wc[0]} (strength {wc[1]:.2f})")
La = feet(wa[0], wc[0])
print(f"D05 addition length: {wc[0] - wa[0]} px = {La:.0f} ft with local pitch ({pct(La, 936):+.2f}% vs 936); "
      f"with the global mean pitch {(wc[0] - wa[0]) / GLOBAL * 24:.0f} ft")
# depth: wall posts down the west end wall of the addition. A post is a disc about 10-14 px wide on a
# 5-6 px line, so the dark width across the wall peaks at each post. Peaks closer than 30 px are merged.
xw = wa[0]
ys = list(range(810, 1062))
width = np.array([(a[y, xw - 14:xw + 15] < a[y, xw - 60:xw - 30].mean() - 50).sum() for y in ys])
cand = [ys[i] for i in range(1, len(ys) - 1)
        if width[i] >= 9 and width[i] >= width[i - 1] and width[i] > width[i + 1]]
pk = []
for y in cand:
    if pk and y - pk[-1] < 30:
        if width[y - ys[0]] > width[pk[-1] - ys[0]]:
            pk[-1] = y
    else:
        pk.append(y)
iv = np.diff(pk)
print(f"posts down the addition's west end: y = {pk} -> {len(pk) - 1} intervals, spacing {iv.tolist()} px; "
      f"depth {(len(pk) - 1) * 8} ft at 8 ft per interval (48 ft stated)")

# 4. D07 / D08: dot pairs in the crossing -------------------------------------------------------
reg = pts[(pts[:, 0] > 4000) & (pts[:, 0] < 5800) & (pts[:, 1] > 1250) & (pts[:, 1] < 1900)]
pxft = GLOBAL / 24
ds = []
for p in reg:
    for q in reg:
        dx = q[0] - p[0]
        if dx > 60 and abs(q[1] - p[1]) < 8:
            ds.append(dx / pxft)
ds = np.array(ds)
for target in (24, 48, 72):
    sel = ds[np.abs(ds - target) < 0.06 * target]
    if len(sel):
        print(f"dot pairs on one row near {target} ft: {len(sel)} pairs, median {np.median(sel):.1f} ft "
              f"({pct(np.median(sel), target):+.1f}%), range {sel.min():.1f}-{sel.max():.1f}")
    else:
        print(f"dot pairs on one row near {target} ft: none found")
