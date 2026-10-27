"""CANDIDATE CP024 Nasmyth hammer polish — next hero (organ = CP045 Sydenham only;
Coalbrookdale gates not in storyboard). Enrich massing: cylinder flanges/bolts,
valve chest + linkage, crosshead guides, boltheads; reframe ram cam to show full
~19 ft machine.

  blender -b rounds/e02.blend -P scripts/polish_hammer_cand.py -- \
      --out rounds/candidates/e02_hammer.blend
"""
import bpy, bmesh, math, os, sys, importlib
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import common as CM, parts1851 as P
importlib.reload(CM); importlib.reload(P)
from common import ft, FT, mat
from parts1851 import box, rod, beam, lathe, finish, I

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/e02_hammer.blend"
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "rounds/e02.blend"))

HC = bpy.data.collections.get("EXH_NASMYTH_HAMMER")
if HC is None:
    raise SystemExit("EXH_NASMYTH_HAMMER missing")

for o in list(HC.objects):
    if o.name.startswith("HAM_cand"):
        bpy.data.objects.remove(o, do_unlink=True)

STEEL = mat("HAM_cand_Steel", (0.70, 0.72, 0.74), 0.22, metal=0.9)
BRASS = mat("HAM_cand_Brass", (0.70, 0.52, 0.20), 0.32, metal=0.75)
MACH = mat("HAM_cand_Mach", (0.20, 0.28, 0.30), 0.5)
CAST = mat("HAM_cand_Cast", (0.16, 0.16, 0.17), 0.65)

def add_part(name, bm, mats, loc=(0, 0, 0)):
    me = finish(bm, "ME_" + name, mats)
    o = bpy.data.objects.new(name, me)
    o.location = Vector([ft(v) for v in loc])
    HC.objects.link(o)
    o["candidate"] = "CP024_hammer"
    return o

# --- Cylinder top flanges + stuffing box + cover nuts ---
bm = bmesh.new()
# bottom flange under cylinder bed already there; add mid ring + top cover
lathe(bm, [(0, 13.55), (1.55, 13.55), (1.55, 13.72), (1.35, 13.72), (1.35, 13.55)], 28)
lathe(bm, [(0, 18.15), (1.55, 18.15), (1.55, 18.35), (1.15, 18.35), (1.15, 18.55), (0.55, 18.7), (0, 18.7)], 28)
# stuffing box collar at piston exit through entablature
lathe(bm, [(0, 13.35), (0.42, 13.35), (0.42, 13.55), (0.55, 13.55), (0.55, 13.7), (0.35, 13.7), (0.35, 13.35)], 20)
# bolt circle on top cover
for k in range(8):
    a = 2 * math.pi * k / 8
    x, y = 1.15 * math.cos(a), 1.15 * math.sin(a)
    rod(bm, (x, y, 18.35), (x, y, 18.55), 0.06, 8)
    lathe(bm, [(0, 18.55), (0.1, 18.55), (0.1, 18.62), (0, 18.62)], 8, Matrix.Translation((x, y, 0)))
add_part("HAM_cand_cyl_detail", bm, [STEEL, MACH])

# --- Valve chest enrichment + eccentric-ish linkage ---
bm = bmesh.new()
box(bm, 1.15, 2.15, -0.75, 0.75, 14.0, 17.0)          # larger chest body
box(bm, 2.05, 2.25, -0.85, 0.85, 13.9, 17.1)          # cover plate
# chest bolts
for z in (14.3, 15.5, 16.6):
    for y in (-0.7, 0.7):
        rod(bm, (2.25, y, z), (2.38, y, z), 0.05, 6)
# vertical valve spindle
rod(bm, (1.65, -0.95, 16.8), (1.65, -0.95, 4.2), 0.07, 10)
# bell-crank / lever
beam(bm, (1.65, -0.95, 4.2), (4.2, -1.8, 3.5), 0.12, 0.22)
lathe(bm, [(0, -0.15), (0.14, -0.12), (0.14, 0.12), (0, 0.15)], 12, Matrix.Translation((4.2, -1.8, 3.5)))
# horizontal reach rod to chest
rod(bm, (1.65, -0.95, 15.8), (1.9, -0.55, 15.9), 0.05, 8)
# small steam branch flanges
lathe(bm, [(0, 0), (0.28, 0), (0.28, 0.12), (0.22, 0.12), (0.22, 0.35), (0, 0.35)], 12,
      Matrix.Translation((2.15, 0.0, 16.2)) @ Matrix.Rotation(math.radians(90), 4, "Y"))
add_part("HAM_cand_valve", bm, [STEEL, BRASS])

# --- Crosshead / ram top detail + guide slippers ---
bm = bmesh.new()
box(bm, -1.35, 1.35, -1.0, 1.0, 2.4, 2.85)           # heavier tup body band
for sx in (-1, 1):
    box(bm, sx * 1.35, sx * 1.55, -0.55, 0.55, 0.7, 2.5)  # guide slippers
# piston rod collar
lathe(bm, [(0, 2.55), (0.32, 2.55), (0.32, 2.75), (0.22, 2.75), (0.22, 2.55)], 16)
add_part("HAM_cand_ram_detail", bm, [STEEL], loc=(0, 0, 2.95))  # same as DIE_TOP offset as live ram

# Parent ram detail to ram so it animates
ram = bpy.data.objects.get("HAM_ram")
det = bpy.data.objects.get("HAM_cand_ram_detail")
if ram and det:
    det.parent = ram
    # ram loc is already DIE_TOP in meters; child local should be relative
    # Live: tup loc=(0,0,DIE_TOP) with mesh origin at striking face.
    # Detail built with z in feet absolute from 0; we set loc DIE_TOP then parent —
    # after parenting, clear and set local so detail sits on tup.
    det.parent = None
    det.location = Vector((0, 0, 0))
    # rebuild detail in ram-local feet (mesh already includes z 0..2.85 band near tup)
    # Simpler: keep world-aligned by copying ram matrix each frame via constraint
    det.parent = ram
    det.matrix_parent_inverse = ram.matrix_world.inverted()
    # Place detail at ram world origin (striking face); mesh has geometry from z=0.7..2.85 ft
    det.location = (0, 0, 0)

# --- Frame boltheads + capital mouldings on standards ---
bm = bmesh.new()
for sx in (-1, 1):
    for z in (3.8, 7.6, 10.6, 12.3):
        xo = 6.2 + (3.15 - 6.2) * (z - 0.7) / 11.8
        for yy in (-0.95, 0.95):
            rod(bm, (sx * xo, yy, z), (sx * xo, yy, z + 0.18), 0.08, 6)
            lathe(bm, [(0, z + 0.18), (0.12, z + 0.18), (0.12, z + 0.26), (0, z + 0.26)], 8,
                  Matrix.Translation((sx * xo, yy, 0)))
    # capital under entablature
    box(bm, sx * 1.2, sx * 2.0, -1.15, 1.15, 12.2, 12.55)
add_part("HAM_cand_frame_bolts", bm, [STEEL, CAST])

# --- Anvil face / die polish (brighter steel top) ---
bm = bmesh.new()
box(bm, -0.95, 0.95, -0.75, 0.75, 2.55, 2.72)
for k in range(4):
    a = math.pi / 4 + k * math.pi / 2
    x, y = 0.7 * math.cos(a), 0.55 * math.sin(a)
    rod(bm, (x, y, 2.5), (x, y, 2.55), 0.05, 6)
add_part("HAM_cand_die", bm, [STEEL])

# Soften live flat paint slightly by not touching MACH materials — overlays carry steel.

# --- Reframe CP024_ram_start: show full ~19 ft machine ---
# Instance empty at ~29.26 ft in X (meters: 29.261 — wait that's already meters!)
# EXI at [29.261, 0, 0] meters = ~96 ft — matches POS. Cam at 29.566,-7.315,1.6 m
# looking at instance. Machine height 19 ft = 5.79 m. Pull back on -Y, look at mid height.
empty = bpy.data.objects["EXI_NASMYTH_HAMMER"]
anchor = empty.matrix_world.translation.copy()  # meters
cam = bpy.data.objects["CP024_ram_start"]
# eye 5.25 ft, ~38 ft back on -Y from machine, slight +X for 3/4
back = 38 * FT
cam.location = Vector((anchor.x + 2.5 * FT, anchor.y - back, 5.25 * FT))
target = Vector((anchor.x, anchor.y, 10.0 * FT))  # mid machine
look = (target - cam.location).normalized()
world_up = Vector((0, 0, 1))
right = look.cross(world_up).normalized()
up = right.cross(look).normalized()
M = Matrix([
    [right.x, up.x, (-look).x, cam.location.x],
    [right.y, up.y, (-look).y, cam.location.y],
    [right.z, up.z, (-look).z, cam.location.z],
    [0, 0, 0, 1],
])
cam.matrix_world = M
cam.data.lens = 35.0  # wider to take whole machine
cam["candidate"] = "CP024_hammer"
print("CAM", [round(v / FT, 2) for v in cam.location], "lens", cam.data.lens,
      "target_z_ft", 10.0, flush=True)

# Also nudge approach cam slightly for consistency
for cname in ("CP024_approach_start", "CP024_approach_end"):
    c = bpy.data.objects.get(cname)
    if not c:
        continue
    # keep lens; pull back a bit
    c.location.y = min(c.location.y, anchor.y - 22 * FT)
    c["candidate"] = "CP024_hammer"

txt = bpy.data.texts.get("CREDIT_HAM_CAND") or bpy.data.texts.new("CREDIT_HAM_CAND")
txt.clear()
txt.write(
    "CANDIDATE CP024 Nasmyth hammer polish\n"
    "Why this hero: Willis organ only needed CP045 (Sydenham 1857); Coalbrookdale gates\n"
    "not in storyboard. Next-crudest HP hero by screen time = Nasmyth steam hammer (CP024).\n"
    "Adds: cylinder flanges/bolts, valve chest+linkage, ram slippers, frame boltheads, die face.\n"
    "Reframe CP024_ram_start: 35 mm, eye 5.25 ft, full ~19 ft machine in frame.\n"
    "Live e02 untouched until KEEP.\n"
)

bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out, "objs", [o.name for o in HC.objects if o.name.startswith("HAM_cand")], flush=True)
