"""CANDIDATE: apply shared HP interior envelope to live e02 for
CP024 ram + approach, CP025_visitors, EX_lineup.

  blender -b rounds/e02.blend -P scripts/apply_envelope_e02.py -- \
      --out rounds/candidates/e02_envelope.blend
"""
import bpy, bmesh, math, os, sys, importlib
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, "/workspace/crystal-palace-survey/envelope")
import parts1851 as P
import hp_interior_envelope as ENV
importlib.reload(P); importlib.reload(ENV)
from common import FT, ft
from parts1851 import box, rod, beam, lathe, finish

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/e02_envelope.blend"
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "rounds/e02.blend"))

# Clear prior court + envelope
for o in list(bpy.data.objects):
    if o.name.startswith("MC_") or o.name.startswith("HPE_") or o.get("kit") == "hp_interior_envelope":
        bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections):
    if c.name.startswith("MC_") or c.name.startswith("HPE_"):
        bpy.data.collections.remove(c)

# Hide outdoor showroom
for name in ("SR_floor", "SR_column_lines", "SR_osler_dais", "SR_osler_drape"):
    o = bpy.data.objects.get(name)
    if o:
        o.hide_render = True
        o.hide_viewport = True

CAND = "HPE_envelope_e02"

# Mid-bay envelope centred on Osler (48,0) covering Koh (0) → Hammer (96)
# Columns at … −12,12,36,60,84,108,132,156… — assets sit mid-bay.
ENV.build_envelope(
    origin_ft=(48.0, 0.0),
    nx=8,
    ny=5,
    mid_bay=True,
    aisle_clear_y=14.0,
    canvas_shade=False,
    candidate=CAND,
    wall_sides=("n", "s", "e", "w"),
    gallery=True,
    roof=True,
    floor=True,
)

# Neighbouring machine block-outs around hammer (Machinery Court denseness)
IRON = ENV._mat("HPE_MachIron", (0.55, 0.56, 0.58), 0.35, 0.85)
MACH = ENV._mat("HPE_MachBlock", (0.22, 0.26, 0.28), 0.55, 0.4)
WOOD = ENV._mat("HPE_MachWood", (0.42, 0.34, 0.24), 0.75)
ax, ay = 96.0, 0.0
coll = bpy.data.collections.get("HPE_ENVELOPE") or bpy.context.scene.collection

def add_mesh(name, bm, mats, loc=(0, 0, 0)):
    me = finish(bm, "ME_" + name, mats)
    o = bpy.data.objects.new(name, me)
    o.location = Vector([ft(v) for v in loc])
    coll.objects.link(o)
    o["candidate"] = CAND
    o["kit"] = "hp_interior_envelope"
    o["part_kind"] = "court_fitout"
    return o

def machine_block(name, loc, sx=8, sy=5, sz=11):
    bm = bmesh.new()
    box(bm, -sx / 2, sx / 2, -sy / 2, sy / 2, 0, sz * 0.55)
    lathe(bm, [(0, sz * 0.4), (sx * 0.22, sz * 0.4), (sx * 0.22, sz * 0.95), (0, sz * 0.95)], 16,
          Matrix.Translation((0, 0, 0)))
    box(bm, -sx * 0.15, sx * 0.15, -sy * 0.15, sy * 0.15, sz * 0.55, sz)
    add_mesh(name, bm, [MACH, IRON], loc=loc)

machine_block("HPE_nbr_press", (ax - 28, ay + 18, 0), 10, 6, 12)
machine_block("HPE_nbr_lathe", (ax + 30, ay + 10, 0), 7, 4, 8)
machine_block("HPE_nbr_boiler", (ax - 32, ay - 8, 0), 9, 5, 10)
machine_block("HPE_nbr_engine", (ax + 26, ay - 14, 0), 8, 5, 9)
bm = bmesh.new()
box(bm, ax - 50, ax - 40, ay + 2, ay + 8, 0, 3.5)
box(bm, ax + 40, ax + 50, ay + 2, ay + 8, 0, 3.5)
add_mesh("HPE_nbr_cases", bm, [WOOD, MACH])

# Bright interior_daylit (CP021-matched)
ENV.apply_daylit(bpy.context.scene, exposure=-0.7, sun_energy=3.36)

# CP024: move camera so no column blocks the hammer (mid-bay sightline)
# mid-bay columns at x=…84,108…; hammer at 96. Eye at x=102 (mid), y=-45 (mid between -36/-60).
empty = bpy.data.objects.get("EXI_NASMYTH_HAMMER")
anchor = empty.matrix_world.translation.copy() if empty else Vector((ft(96), 0, 0))
cam = bpy.data.objects["CP024_ram_start"]
ENV.aim_camera(cam, (102.0, -45.0, 6.5), (96.0, 0.0, 13.0), lens=35.0)
cam["candidate"] = CAND
print("CP024_ram_FT", [round(v / FT, 2) for v in cam.location], flush=True)

# Approach: mid-bay, clear of columns, looking toward hammer
for cname, eye in (
    ("CP024_approach_start", (78.0, -52.0, 6.0)),
    ("CP024_approach_end", (88.0, -36.0, 6.0)),
):
    c = bpy.data.objects.get(cname)
    if c:
        ENV.aim_camera(c, eye, (96.0, 0.0, 10.0), lens=35.0)
        c["candidate"] = CAND

for cname in ("CP025_visitors_start", "CP025_visitors_end", "EX_lineup_start"):
    c = bpy.data.objects.get(cname)
    if c:
        c["candidate"] = CAND

txt = bpy.data.texts.get("CREDIT_HPE_E02") or bpy.data.texts.new("CREDIT_HPE_E02")
txt.clear()
txt.write(
    "CANDIDATE HP interior envelope on e02 (2026-10-27)\n"
    "Shared kit: crystal-palace-survey/envelope/hp_interior_envelope.py\n"
    "8 in OJ columns on 24 ft mid-bay grid; gallery girders+rail; fully glazed\n"
    "ridge-and-furrow + Paxton gutters; glazed outer walls; boarded floor.\n"
    "interior_daylit: exposure -0.7 / sun 3.36 (CP021 match); no black walls;\n"
    "no Nishita sea horizon. CP024_ram_start moved to mid-bay (102,-45,6.5)\n"
    "so no column blocks the KEEP hammer. Claude west nave not written.\n"
    "Shots: CP024_ram, CP024_approach, CP025_visitors, EX_lineup.\n"
)

bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out, flush=True)
