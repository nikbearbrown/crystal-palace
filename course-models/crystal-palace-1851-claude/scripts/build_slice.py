"""Build part of the Crystal Palace along its length, from grid line FIRST to grid line LAST (counted from the west end).

  blender --background --python-exit-code 1 --python model/build_slice.py -- \
      --out model/crystal-palace-west-01_v001.blend --lines 0:6

Default `--lines 4:5` is slice 01 (the one-bay transverse section at line A-B of Plate VI); `0:6` is the first six
bays from the west end; `0:12` adds the first staircases and the next voids, to 288 ft; `0:37` builds the full west
half to 888 ft (the transept west face). Bays are 24 ft; line i stands 24 i ft from the west end.

What it builds: the 408 ft width of the lowest tier; a column on every grid line in every row, in 1, 2 or 3 storeys, with
connecting pieces; 24 ft girders at every tier in both directions; the ground floor slab; the gallery floor and railings
(Plate II); the staircases (Plates XV to XVII); and the ridge-and-valley roof of each tier. What it does not build yet
is listed in DEPARTURES-LEDGER.md.

Plan data from Plates I and II, valid for bays 0 to 36 (to 888 ft, the transept west face at 924 ft; the transept
itself is not yet modelled), so the script refuses a longer range:
  - the avenue voids (48 ft wide, either side of the nave) start 24 ft from the west end and run to 192 ft (printed
    "168.0"); each 24 ft avenue stair bay (printed "24.0") is followed by another void: 216-408 ft ("192.0"), 432-624 ft
    ("192.0"), 648-816 ft ("120.0"+"48.0"); a transept-access stair follows at 816-840 ft (printed "24.0", NOT one of
    the twelve avenue staircases), then a pre-transept void 840-888 ft (printed "48.0");
  - the nave void (72 ft wide) starts 72 ft from the west end (printed "72.0") and runs to 888 ft; no stairs;
  - in each AVENUE stair bay a cross gallery 48 x 24 ft covers the avenue and carries two well-holes (8 x 16 ft); under
    it a staircase of two ground flights, a landing and two upper flights, the ground flights starting on the nave side;
  - the gallery floor is solid everywhere else in the 264 ft width; railings run round every void, ends included.

Coordinates: metres, origin at the centre of the nave and transept crossing at floor level, X along the length (east),
Y across the width (north), Z up (controls.json model_conventions). Never saves anything except --out. Rebuilds from
scratch each run, so running it twice gives the same file.
"""
import argparse
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))  # the library sits beside this script
import parts  # noqa: E402
from parts import ft  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--lines", default="4:5", help="FIRST:LAST grid lines from the west end, inclusive (default 4:5)")
ap.add_argument("--diagnostic-cross-railing", action="store_true",
                help="DIAGNOSTIC ONLY, not part of the model: three railing runs across the nave void at the first "
                     "line, so the railing can be compared face-on with Plate VI's lattice band")
args = ap.parse_args(argv)
FIRST, LAST = (int(v) for v in args.lines.split(":"))
PLAN_DATA_LAST_LINE = 37      # Plates I and II have been read to 888 ft (line 37, transept west face)
if not (0 <= FIRST < LAST <= PLAN_DATA_LAST_LINE):
    sys.exit(f"--lines {args.lines}: need 0 <= FIRST < LAST <= {PLAN_DATA_LAST_LINE} "
             f"(the plan has been read from Plates I and II to 888 ft, line 37 only)")
LINES = list(range(FIRST, LAST + 1))
BAYS = LINES[:-1]

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 1.0

lib = parts.build_all()  # unlinked instance sources

model = bpy.data.collections.new("MODEL")
scene.collection.children.link(model)
kinds = {}
for k in ("COLUMNS", "GIRDERS", "ROOF", "FLOORS"):
    c = bpy.data.collections.new(k)  # grouping for the Outliner only; selectors never use collections
    model.children.link(c)
    kinds[k] = c

GRID = 24                      # ft
X_WEST = -924                  # ft, west end of the 1848 ft length, centre of the crossing at 0
Y_SOUTH = -204                 # ft, south edge of the 408 ft main block
ROWS = 18                      # column lines across the width (17 bays)
Z_PIECE1 = parts.SHAFT_H       # foot of the first connecting piece, metres
AVENUE_VOID_BAYS = (            # Plate II: avenue voids, west end to transept west face
    set(range(1, 8))            # 24-192 ft ("168.0")
    | set(range(9, 17))         # 216-408 ft ("192.0")
    | set(range(18, 26))        # 432-624 ft ("192.0")
    | set(range(27, 34))        # 648-816 ft ("120.0"+"48.0", one continuous void)
    | set(range(35, 37))        # 840-888 ft ("48.0", pre-transept)
)
STAIR_BAYS = {8, 17, 26, 34}   # avenue stair bays; bay 34 is the transept-access stair (not one of the twelve)
NAVE_VOID_FIRST_BAY = 3         # Plate II: from 72 ft


def x_of(i):
    return X_WEST + GRID * i


def top_tier(y):
    return 3 if abs(y) <= 60 else 2 if abs(y) <= 132 else 1


def place(coll, name, src, x_ft, y_ft, z_m, kind, rot_z=0.0, **props):
    e = bpy.data.objects.new(name, None)
    e.instance_type = "COLLECTION"
    e.instance_collection = src
    e.location = (ft(x_ft), ft(y_ft), z_m)
    e.rotation_euler = (0, 0, rot_z)
    e["part_id"] = name  # the unique ID is the object name (BLENDER.md section 4)
    e["part_kind"] = kind
    for k, v in props.items():
        e[k] = v
    coll.objects.link(e)
    return e


def girder_z(t):
    return Z_PIECE1 + (t - 1) * parts.TIER_RISE + parts.PIECE_BELOW_GIRDER


rows = [(j, Y_SOUTH + GRID * j) for j in range(ROWS)]
row_of = {y: j for j, y in rows}
tt = {j: top_tier(y) for j, y in rows}
row_tags = {}
for j, y in rows:
    t = []
    if y in (-36, 36):
        t.append("nave_edge")
    if y in (36, 84):
        t.append("avenue_A1")
    row_tags[j] = t

# columns --------------------------------------------------------------------------------------------
for i in LINES:
    x = x_of(i)
    line_tags = (["west_end"] if i == 0 else []) + (["avenue_void_end"] if i == 1 else []) + \
                (["nave_void_end"] if i == NAVE_VOID_FIRST_BAY else []) + \
                (["stair_gap_west"] if i in STAIR_BAYS else []) + (["stair_gap_east"] if i - 1 in STAIR_BAYS else [])
    for j, y in rows:
        tags = row_tags[j] + line_tags
        extra = {"tags": " ".join(tags)} if tags else {}
        if (i, j) == (LINES[0], 9):
            extra["sample"] = "shaft_a"
        place(kinds["COLUMNS"], f"COLS_X{i:02d}_Y{j:02d}", lib["column_shaft"], x, y, 0.0, "column_shaft",
              block="main", top_tier=tt[j], **extra)
        for t in range(1, tt[j] + 1):
            z0 = Z_PIECE1 + (t - 1) * parts.TIER_RISE
            place(kinds["COLUMNS"], f"COLC_T{t}_X{i:02d}_Y{j:02d}", lib["connecting_piece"], x, y, z0,
                  "connecting_piece", tier=t)
            if t < tt[j]:  # the upper column stands on this piece
                place(kinds["COLUMNS"], f"COLU_T{t + 1}_X{i:02d}_Y{j:02d}", lib["column_upper"], x, y,
                      z0 + parts.PIECE_H, "column_upper", tier=t + 1)

# girders: the girder's bottom is 2 1/4 in above the foot of its connecting piece ------------------------
for t in (1, 2, 3):
    for b in BAYS:                                      # along X, one per row, in each bay
        for j, y in rows:
            if tt[j] >= t:
                extra = {"sample": "girder_24_x"} if (t, j, b) == (1, 9, BAYS[0]) else {}
                place(kinds["GIRDERS"], f"GIRX_T{t}_X{b:02d}_Y{j:02d}", lib["girder24"], x_of(b) + GRID / 2, y,
                      girder_z(t), "girder", tier=t, span_ft=24, **extra)
    for i in LINES:                                     # along Y, between neighbouring rows, on each line
        for (j, y), (j2, y2) in zip(rows, rows[1:]):
            if tt[j] >= t and tt[j2] >= t:
                place(kinds["GIRDERS"], f"GIRY_T{t}_X{i:02d}_Y{j:02d}", lib["girder24"], x_of(i), (y + y2) / 2,
                      girder_z(t), "girder", rot_z=math.pi / 2, tier=t, span_ft=24)

# gallery floor and railings, from Plate II -----------------------------------------------------------------
# Cells are 24 x 24 ft; k counts the cells of the 264 ft gallery zone from the south (y = -132 + 24 k).
# Void cells: avenue voids k = 1, 2 (south) and 8, 9 (north); nave void k = 4, 5, 6.
AVENUE_K, NAVE_K = {1, 2, 8, 9}, {4, 5, 6}
floor_z = girder_z(1) + parts.GIRDER_D                      # girder top = foot of the floor structure


def void_cells(b):
    v = set()
    if b in AVENUE_VOID_BAYS or b in STAIR_BAYS:   # a stair bay's avenue cells belong to the cross gallery
        v |= AVENUE_K
    if b >= NAVE_VOID_FIRST_BAY:
        v |= NAVE_K
    return v


for b in BAYS:
    for k in range(11):
        if k in void_cells(b):
            continue
        y_lo = -132 + GRID * k
        place(kinds["FLOORS"], f"GFLR_L1_X{b:02d}_Y{row_of[y_lo]:02d}", lib["gallery_panel"], x_of(b) + GRID / 2,
              y_lo + GRID / 2, floor_z, "gallery_floor", level=1)
    # long railings: a run along X on every void edge, where the void is present in this bay
    edges = set()
    if b in AVENUE_VOID_BAYS:
        edges |= {-108, -60, 60, 108}
    if b >= NAVE_VOID_FIRST_BAY:
        edges |= {-36, 36}
    for y_edge in sorted(edges):
        place(kinds["FLOORS"], f"BAL_L1_X{b:02d}_Y{row_of[y_edge]:02d}", lib["balustrade24"], x_of(b) + GRID / 2,
              y_edge, floor_z + parts.GALLERY_T, "balustrade", level=1)

# cross railings across the void ends: runs along Y, 24 ft each, at the line where a void starts
for line, ks in (
    (1,                   sorted(AVENUE_K)),
    (NAVE_VOID_FIRST_BAY, sorted(NAVE_K)),
    (8,                   sorted(AVENUE_K)), (9,  sorted(AVENUE_K)),
    (17,                  sorted(AVENUE_K)), (18, sorted(AVENUE_K)),
    (26,                  sorted(AVENUE_K)), (27, sorted(AVENUE_K)),
    (34,                  sorted(AVENUE_K)), (35, sorted(AVENUE_K)),
    (37,                  sorted(AVENUE_K | NAVE_K)),  # transept west face: all voids close here
):
    if line in LINES:
        for k in ks:
            y_lo = -132 + GRID * k
            place(kinds["FLOORS"], f"BALY_L1_X{line:02d}_Y{row_of[y_lo]:02d}", lib["balustrade24"], x_of(line),
                  y_lo + GRID / 2, floor_z + parts.GALLERY_T, "balustrade", rot_z=math.pi / 2, level=1)

# staircases and cross galleries, Plates I, II, XV to XVII ------------------------------------------------------
# One staircase in each avenue void of a stair bay: the cross gallery (48 x 24 ft, two 8 x 16 ft well-holes at its ends,
# over the middle 8 ft strip), a landing 24 x 8 ft at the centre of the void at 137.5 in, two ground flights in the outer
# strips from the nave-side edge of the void, and two upper flights in the middle strip, one back toward the nave-side
# gallery and one out to the far gallery. Flights run along Y, 20 ft each, so 20 + 8 + 20 = the 48 ft of the void.
S_LAND_H = parts.STAIR_RISE
for b in BAYS:
    if b not in STAIR_BAYS:
        continue
    xc = x_of(b) + GRID / 2
    for sgn, av in ((1, "N"), (-1, "S")):
        first = (sgn == 1)
        yc = sgn * 84                                              # centre of the avenue void
        place(kinds["FLOORS"], f"XGAL_{av}_X{b:02d}", lib["cross_gallery"], xc, yc, floor_z, "gallery_floor",
              level=1, avenue=av, **({"sample": "cross_gallery"} if first else {}))
        place(kinds["FLOORS"], f"STLD_{av}_X{b:02d}", lib["stair_landing"], xc, yc, 0.0, "stair_landing", avenue=av,
              **({"sample": "stair_landing"} if first else {}))
        for ix, dx in enumerate(parts.LANDING_COL_X):
            for iy, dy in enumerate((-4, 4)):
                place(kinds["COLUMNS"], f"STCL_{av}_X{b:02d}_{ix}{iy}", lib["stair_column"], xc + dx / parts.FT, yc + dy,
                      0.0, "stair_column", avenue=av,
                      **({"sample": "stair_column"} if (first and ix == 0 and iy == 0) else {}))
        # ground flights: strings 7 ft 1 in apart, columns on the string lines (7 ft 1 in, 8 ft 5 in, 7 ft 1 in)
        for tag, dx in (("W", -7.75), ("E", 7.75)):
            place(kinds["FLOORS"], f"STFL_{av}_X{b:02d}_{tag}", lib["stair_flight"], xc + dx, sgn * 60, 0.0,
                  "stair_flight", rot_z=sgn * math.pi / 2, stage="lower", avenue=av,
                  **({"sample": "stair_flight"} if (first and tag == "W") else {}))
        # upper flights, from the landing surface: "IN" back toward the nave, "OUT" away from it
        place(kinds["FLOORS"], f"STFU_{av}_X{b:02d}_IN", lib["stair_flight"], xc, sgn * 80, S_LAND_H, "stair_flight",
              rot_z=-sgn * math.pi / 2, stage="upper", avenue=av)
        place(kinds["FLOORS"], f"STFU_{av}_X{b:02d}_OUT", lib["stair_flight"], xc, sgn * 88, S_LAND_H, "stair_flight",
              rot_z=sgn * math.pi / 2, stage="upper", avenue=av)
        # landing railings: the two ends of the landing, and the far edge beside the upper flight
        for k, x in enumerate((xc - 12, xc + 12)):
            place(kinds["FLOORS"], f"STRL_{av}_X{b:02d}_E{k}", lib["balustrade8"], x, yc, S_LAND_H, "balustrade",
                  rot_z=math.pi / 2, level="landing", avenue=av)
        for k, x in enumerate((xc - 8, xc + 8)):
            place(kinds["FLOORS"], f"STRL_{av}_X{b:02d}_F{k}", lib["balustrade8"], x, sgn * 88, S_LAND_H, "balustrade",
                  level="landing", avenue=av)

if args.diagnostic_cross_railing:
    for k, y in enumerate((-24, 0, 24)):
        place(kinds["FLOORS"], f"DIAG_BAL_Y{k}", lib["balustrade24"], x_of(LINES[0]), y,
              floor_z + parts.GALLERY_T, "diagnostic", rot_z=math.pi / 2)


# roof: units 8 ft gutter to gutter, valley at the girder top of the tier (INFERRED, see the ledger) ---------
def roof_row(t, y_centres):
    for b in BAYS:
        for y in y_centres:
            place(kinds["ROOF"], f"ROOF_T{t}_X{b:02d}_{'N' if y > 0 else 'S'}{abs(int(y)):03d}",
                  lib["roof_unit"], x_of(b) + GRID / 2, y, girder_z(t) + parts.GIRDER_D, "ridge", tier=t)


roof_row(3, [-56 + 8 * k for k in range(15)])                                      # |y| <= 60
roof_row(2, [64 + 8 * k for k in range(9)] + [-(64 + 8 * k) for k in range(9)])    # 60 < |y| <= 132
roof_row(1, [136 + 8 * k for k in range(9)] + [-(136 + 8 * k) for k in range(9)])  # 132 < |y| <= 204

# ground floor: a plain slab, top face at z = 0 (INFERRED: the real floor is boards on joists) --------------
x_lo = x_of(FIRST) - (0 if FIRST == 0 else GRID / 2)   # the slab starts at the west end, not beyond it
x_hi = x_of(LAST) + GRID / 2
fl = parts.box(kinds["FLOORS"], "FLOOR_ground", ft(x_lo), ft(x_hi), ft(Y_SOUTH), ft(Y_SOUTH + 408), -ft(0, 6), 0.0,
               "MAT_Floor")
fl["part_id"] = "FLOOR_ground"
fl["part_kind"] = "floor_ground"

bpy.ops.wm.save_as_mainfile(filepath=args.out)
n = {}
for o in bpy.data.objects:
    if o.get("part_kind"):
        n[o["part_kind"]] = n.get(o["part_kind"], 0) + 1
print(f"built lines {FIRST}:{LAST} ({len(BAYS)} bays):", args.out, n)
