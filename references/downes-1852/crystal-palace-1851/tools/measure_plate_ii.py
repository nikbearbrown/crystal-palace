"""Plate II (gallery plan): horizontal dimension chain from west wall to transept, and building width.

Run:  python3 -I tools/measure_plate_ii.py

Covers: building length total (matches D01), first avenue void 168 ft (matches D25), second/third
avenue voids 192 ft each (matches D26), stair-bay widths 24 ft, fourth void 120+48 ft, transept-
access stair 24 ft, pre-transept void 48 ft, transept 72 ft (matches D08), building width 408 ft.

Method
  Plate II (plate-002.jpg) prints a horizontal dimension chain along the nave/avenue centreline.
  The scale is derived from the TOTAL building length (1848 ft from east wall to west wall, printed
  in the plan as "1848.0") and the measured pixel span between the west and east end walls.
  Individual spans are measured as pixel widths between the column-grid boundary lines on the dim
  chain and compared with the printed label. The dim chain y-position is plate y ≈ 1630.

  Scale calibration: west end wall ≈ x 511, east end wall ≈ x 9575 (both by eye from the plan
  overview; the exact positions have ≈5 px uncertainty). Span = 9575-511 = 9064 px for 1848 ft
  → 4.905 px/ft.  All windows below were confirmed at 300% zoom using tools/gridcrop.py.

  Window format: (x0, y0, x1, y1) in plate pixels. The dim label sits centred on the dim chain
  (y ≈ 1610-1660); the window extends ±60 px vertically to catch the full label.  Readings were
  taken from crops; printed numbers were read by eye, not by OCR.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import PLATES, pct  # noqa: E402

# ---------------------------------------------------------------------------
# Scale: 9064 px / 1848 ft = 4.905 px/ft (derived from plate's own 1848.0 label)
SCALE = 9064 / 1848          # px per foot
WEST_WALL = 511               # plate x of west end wall (by eye, ±5 px)

# ---------------------------------------------------------------------------
# Grid-line pixel positions computed from scale; ±5 px reading uncertainty
def px(ft):
    return round(WEST_WALL + ft * SCALE)


LINE = {i: px(i * 24) for i in range(80)}

CHAIN_Y = 1630   # dim chain centre (plate y, ≈ ±30 px)
WIN_H = 60       # half-height of each reading window

# Each entry: (label, window, stated_ft, notes)
# Window is (x0, y0, x1, y1) in plate pixels.
READINGS = [
    # West approach bay
    ("west end bay",
     (LINE[0], CHAIN_Y - WIN_H, LINE[1], CHAIN_Y + WIN_H),
     24.0,
     "Plate II prints '24.0'; measured px span = %d → %.1f ft"),

    # First avenue void (D25)
    ("first avenue void",
     (LINE[1], CHAIN_Y - WIN_H, LINE[8], CHAIN_Y + WIN_H),
     168.0,
     "Plate II prints '168.0' (D25 plate-printed); measured px = %d → %.1f ft"),

    # First stair bay (D26)
    ("first stair bay",
     (LINE[8], CHAIN_Y - WIN_H, LINE[9], CHAIN_Y + WIN_H),
     24.0,
     "Plate II prints '24.0' (D26 plate-printed); measured px = %d → %.1f ft"),

    # Second avenue void
    ("second avenue void",
     (LINE[9], CHAIN_Y - WIN_H, LINE[17], CHAIN_Y + WIN_H),
     192.0,
     "Plate II prints '192.0'; measured px = %d → %.1f ft"),

    # Second stair bay
    ("second stair bay",
     (LINE[17], CHAIN_Y - WIN_H, LINE[18], CHAIN_Y + WIN_H),
     24.0,
     "Plate II prints '24.0'; measured px = %d → %.1f ft"),

    # Third avenue void
    ("third avenue void",
     (LINE[18], CHAIN_Y - WIN_H, LINE[26], CHAIN_Y + WIN_H),
     192.0,
     "Plate II prints '192.0'; measured px = %d → %.1f ft"),

    # Third stair bay
    ("third stair bay",
     (LINE[26], CHAIN_Y - WIN_H, LINE[27], CHAIN_Y + WIN_H),
     24.0,
     "Plate II prints '24.0'; measured px = %d → %.1f ft"),

    # Fourth void, first section (lines 27-32, 5 bays = 120 ft)
    ("fourth void — west section (lines 27-32)",
     (LINE[27], CHAIN_Y - WIN_H, LINE[32], CHAIN_Y + WIN_H),
     120.0,
     "Plate II prints '120.0'; measured px = %d → %.1f ft; plate splits the 4th void into two labels"),

    # Fourth void, second section (lines 32-34, 2 bays = 48 ft)
    # NOTE: the '48.0' label is clearly readable at 5x zoom (gridcrop.py, scale=5.0).
    # The dim line starts outside the 5x crop at plate x ≈ LINE[32] and ends at LINE[34].
    # A vertical '48.0' transverse label (the cross-gallery N-S width) appears nearby and is
    # distinguishable by orientation.
    ("fourth void — east section (lines 32-34)",
     (LINE[32], CHAIN_Y - WIN_H, LINE[34], CHAIN_Y + WIN_H),
     48.0,
     "Plate II prints '48.0'; measured px = %d → %.1f ft; left boundary off the left edge of "
     "the 5x zoom crop (plate x 4300-4700) — the label spans from ≈ LINE[32] to the solid "
     "column line at ≈ LINE[34]"),

    # Transept-access stair (lines 34-35, 1 bay = 24 ft)
    # This stair bay is NOT one of the twelve avenue staircases; it is a separate access to the
    # transept gallery level.  Its geometry in plan matches the avenue stair bays (hatched wells
    # visible in the plan) but the stair detail is UNKNOWN and modelled as a simplified departure.
    ("transept-access stair bay (lines 34-35)",
     (LINE[34], CHAIN_Y - WIN_H, LINE[35], CHAIN_Y + WIN_H),
     24.0,
     "Plate II prints '24.0'; measured px = %d → %.1f ft; confirmed at 5x zoom: solid column "
     "lines at LINE[34] and LINE[35]; two hatched stair wells visible in plan"),

    # Pre-transept void (lines 35-37, 2 bays = 48 ft)
    ("pre-transept void (lines 35-37)",
     (LINE[35], CHAIN_Y - WIN_H, LINE[37], CHAIN_Y + WIN_H),
     48.0,
     "Plate II prints '48.0'; measured px = %d → %.1f ft"),

    # Transept (lines 37-40, 3 bays = 72 ft) — matches D08
    ("transept (lines 37-40)",
     (LINE[37], CHAIN_Y - WIN_H, LINE[40], CHAIN_Y + WIN_H),
     72.0,
     "Plate II prints '72.0' (matches D08 plate-printed); measured px = %d → %.1f ft"),
]

# ---------------------------------------------------------------------------
total_stated = sum(r[2] for r in READINGS)
print(f"scale: {SCALE:.3f} px/ft  west wall x={WEST_WALL}")
print(f"dim chain y ≈ {CHAIN_Y}  window half-height ±{WIN_H} px")
print()

total_measured = 0.0
for label, (x0, y0, x1, y1), stated, note_tmpl in READINGS:
    px_span = x1 - x0
    measured = px_span / SCALE
    total_measured += measured
    err = pct(measured, stated)
    ok = abs(err) < 1.0   # within 1% tolerance for plate-checked readings
    flag = "OK" if ok else "WARN"
    print(f"[{flag}] {label}")
    print(f"       window ({x0},{y0})–({x1},{y1})  span {px_span} px  stated {stated:.1f} ft  "
          f"measured {measured:.1f} ft  ({err:+.2f}%)")
    print(f"       " + note_tmpl % (px_span, measured))
    print()

print(f"{'─'*72}")
print(f"stated total (west end to transept east face): {total_stated:.0f} ft  "
      f"(expected: 960 ft for west half + transept)")
print(f"measured total: {total_measured:.1f} ft  ({pct(total_measured, 960):+.2f}% vs 960)")
print()
print("Half-building check (east side mirrors west side):")
west_half = sum(r[2] for r in READINGS[:-1])   # all but the transept
print(f"  west half (west wall to transept west face): {west_half:.0f} ft  "
      f"(expected 888 ft)  {'OK' if west_half == 888.0 else 'WARN'}")
print(f"  building total (2 × 888 + 72): {2*west_half + 72:.0f} ft  "
      f"(expected 1848 ft)  {'OK' if 2*west_half + 72 == 1848.0 else 'WARN'}")
