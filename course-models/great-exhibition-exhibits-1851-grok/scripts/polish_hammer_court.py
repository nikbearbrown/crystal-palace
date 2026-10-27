"""CANDIDATE CP024 Machinery Court setting around KEEP Nasmyth hammer.
Builds cast-iron columns, gallery + girders, glazed ridge-and-furrow roof,
boarded floor, neighbouring machine block-outs; removes sea-horizon showroom;
interior_machinery lighting; raises/backs CP024_ram_start so hammer top reads
against gallery/roof, not empty sky.

  blender -b rounds/e02.blend -P scripts/polish_hammer_court.py -- \
      --out rounds/candidates/e02_hammer_court.blend
"""
import bpy, bmesh, math, os, sys, importlib
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import common as CM, parts1851 as P
importlib.reload(CM); importlib.reload(P)
from common import ft, FT, mat
from parts1851 import box, rod, beam, lathe, finish, add_column, add_girder, GIRDER_D

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/e02_hammer_court.blend"
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "rounds/e02.blend"))

# --- Hide outdoor showroom context that reads as empty plaza ---
for name in ("SR_floor", "SR_column_lines", "SR_osler_dais", "SR_osler_drape"):
    o = bpy.data.objects.get(name)
    if o:
        o.hide_render = True
        o.hide_viewport = True

# Hide Koh/Osler preview assets for this shot (machinery court only)
for cname in ("EXH_KOHINOOR", "EXH_OSLER_CANDELABRUM", "CP025_KOH_CAND2"):
    c = bpy.data.collections.get(cname)
    if c:
        for o in c.objects:
            o.hide_render = True
# Also hide EXI instances for koh/osler
for n in list(bpy.data.objects.keys()):
    if n.startswith("EXI_KOH") or n.startswith("EXI_OSLER") or n.startswith("KOH_") or n.startswith("OSL_"):
        o = bpy.data.objects.get(n)
        if o:
            o.hide_render = True

# Clear prior MC
for o in list(bpy.data.objects):
    if o.name.startswith("MC_"):
        bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections):
    if c.name.startswith("MC_"):
        bpy.data.collections.remove(c)

root = bpy.context.scene.collection
MC = bpy.data.collections.new("MC_MACHINERY_COURT")
root.children.link(MC)
MC["credit"] = "Grok Bot Machinery Court block-out for CP024; HP 1851 proportions (24 ft bay)"
MC["candidate"] = "CP024_court"

IRON = mat("MC_Iron", (0.55, 0.56, 0.58), 0.35, metal=0.85)
PAINT = mat("MC_Paint", (0.72, 0.74, 0.76), 0.45, metal=0.15)  # white-iron
WOOD = mat("MC_Board", (0.42, 0.34, 0.24), 0.75)
GLASS = mat("MC_Glass", (0.78, 0.86, 0.90), 0.05, metal=0.0)
# make glass transmission-ish
if GLASS.use_nodes:
    b = GLASS.node_tree.nodes["Principled BSDF"]
    if "Transmission Weight" in b.inputs:
        b.inputs["Transmission Weight"].default_value = 0.92
    elif "Transmission" in b.inputs:
        b.inputs["Transmission"].default_value = 0.92
    b.inputs["Roughness"].default_value = 0.05
    b.inputs["Alpha"].default_value = 0.15
    GLASS.blend_method = 'HASHED' if hasattr(GLASS, 'blend_method') else GLASS.blend_method
MACH = mat("MC_MachBlock", (0.22, 0.26, 0.28), 0.55, metal=0.4)
DARK = mat("MC_Gallery", (0.28, 0.28, 0.30), 0.65)

def add_mesh(name, bm, mats, loc=(0, 0, 0)):
    me = finish(bm, "ME_" + name, mats)
    o = bpy.data.objects.new(name, me)
    o.location = Vector([ft(v) for v in loc])
    MC.objects.link(o)
    o["candidate"] = "CP024_court"
    o["part_kind"] = "court"
    return o

# Hammer sits at EXI_NASMYTH_HAMMER (~96, 0, 0) ft via instance; court in world feet around that.
empty = bpy.data.objects.get("EXI_NASMYTH_HAMMER")
ax = empty.matrix_world.translation.x / FT if empty else 96.0
ay = empty.matrix_world.translation.y / FT if empty else 0.0
print("HAMMER_ANCHOR_FT", round(ax, 2), round(ay, 2), flush=True)

# Grid: 24 ft bays; cover 5 x 4 bays around hammer
BAY = 24.0
xs = [ax + BAY * i for i in range(-2, 3)]   # -48 .. +48 relative
ys = [ay + BAY * j for j in (-1, 0, 1, 2)]  # -24 .. +48
COL_H1 = 22.0   # ground tier to gallery
COL_H2 = 20.0   # gallery to roof spring
GAL_Z = COL_H1
ROOF_Z = COL_H1 + COL_H2  # ~42 ft spring / gutter line
RIDGE_RISE = 1.6  # Paxton furrow rise over 4 ft half

# --- Boarded floor ---
bm = bmesh.new()
# main deck
box(bm, ax - 60, ax + 60, ay - 48, ay + 60, -0.15, 0.0)
# board grooves (visual strips)
for i in range(-20, 21):
    x0 = ax - 60 + i * 3.0
    box(bm, x0, x0 + 0.04, ay - 48, ay + 60, 0.0, 0.02)
add_mesh("MC_floor", bm, [WOOD])

# --- Cast-iron columns (ground + gallery tiers) ---
bm = bmesh.new()
for x in xs:
    for y in ys:
        add_column(bm, COL_H1, M=Matrix.Translation((x, y, 0)))
        add_column(bm, COL_H2, M=Matrix.Translation((x, y, GAL_Z)))
add_mesh("MC_columns", bm, [IRON, PAINT])

# --- Girders at gallery top (along X between columns) and cross girders along Y ---
bm = bmesh.new()
for y in ys:
    for i in range(len(xs) - 1):
        cx = 0.5 * (xs[i] + xs[i + 1])
        # girder top at GAL_Z, depth down
        add_girder(bm, M=Matrix.Translation((cx, y, GAL_Z)))
for x in xs:
    for j in range(len(ys) - 1):
        cy = 0.5 * (ys[j] + ys[j + 1])
        # rotate girder 90 deg about Z for Y-span
        M = Matrix.Translation((x, cy, GAL_Z)) @ Matrix.Rotation(math.radians(90), 4, "Z")
        add_girder(bm, M=M)
# roof-level girders
for y in ys:
    for i in range(len(xs) - 1):
        cx = 0.5 * (xs[i] + xs[i + 1])
        add_girder(bm, M=Matrix.Translation((cx, y, ROOF_Z)))
for x in xs:
    for j in range(len(ys) - 1):
        cy = 0.5 * (ys[j] + ys[j + 1])
        M = Matrix.Translation((x, cy, ROOF_Z)) @ Matrix.Rotation(math.radians(90), 4, "Z")
        add_girder(bm, M=M)
add_mesh("MC_girders", bm, [IRON, PAINT])

# --- Gallery floor slab + lattice rail (north, east, west of hammer aisle) ---
bm = bmesh.new()
# side galleries: leave central aisle open over hammer (y -12..12)
box(bm, ax - 60, ax + 60, ay + 12, ay + 60, GAL_Z - 0.35, GAL_Z)  # north gallery
box(bm, ax - 60, ax - 12, ay - 48, ay + 12, GAL_Z - 0.35, GAL_Z)  # west
box(bm, ax + 12, ax + 60, ay - 48, ay + 12, GAL_Z - 0.35, GAL_Z)  # east
# simple rail posts + rails on gallery edge
for x in [ax + t for t in range(-48, 49, 6)]:
    for yedge, ysign in ((ay + 12, 1),):
        rod(bm, (x, yedge, GAL_Z), (x, yedge, GAL_Z + 3.5), 0.06, 6)
    beam(bm, (ax - 48, ay + 12, GAL_Z + 3.2), (ax + 48, ay + 12, GAL_Z + 3.2), 0.08, 0.12)
    beam(bm, (ax - 48, ay + 12, GAL_Z + 1.8), (ax + 48, ay + 12, GAL_Z + 1.8), 0.06, 0.08)
add_mesh("MC_gallery", bm, [DARK, IRON])

# --- Ridge-and-furrow glazed roof over the court ---
# Furrows run along X; ridges every 8 ft in Y (Paxton)
bm = bmesh.new()
glass_bm = bmesh.new()
y0, y1 = ay - 48, ay + 60
x0, x1 = ax - 60, ax + 60
furrow_pitch = 8.0
yy = y0
while yy < y1 - 0.1:
    yb = min(yy + furrow_pitch, y1)
    mid = 0.5 * (yy + yb)
    # two slopes meeting at ridge mid
    # left slope yy -> mid, right mid -> yb; rise RIDGE_RISE
    # build as thin glass slabs (quads via boxes with small thickness)
    # approximate with prism strips
    for (ya, yb_, za, zb_) in (
        (yy, mid, ROOF_Z, ROOF_Z + RIDGE_RISE),
        (mid, yb, ROOF_Z + RIDGE_RISE, ROOF_Z),
    ):
        # roof plane as thin box following slope - use prism
        # simpler: stepped flat glass + iron sash bars
        z_lo = min(za, zb_)
        z_hi = max(za, zb_)
        # iron valley / ridge bars
        rod(bm, (x0, ya, za), (x1, ya, za), 0.08, 6)
        # glass pane (flat approx at average z)
        zavg = 0.5 * (za + zb_)
        box(glass_bm, x0, x1, ya, yb_, zavg, zavg + 0.08)
    # sash bars across
    for xi in range(int(x0), int(x1) + 1, 4):
        rod(bm, (xi, yy, ROOF_Z), (xi, yb, ROOF_Z + RIDGE_RISE * 0.5), 0.04, 5)
    yy = yb
# perimeter eaves beam
box(bm, x0, x1, y0 - 0.3, y0, ROOF_Z - 0.4, ROOF_Z + 0.2)
box(bm, x0, x1, y1, y1 + 0.3, ROOF_Z - 0.4, ROOF_Z + 0.2)
box(bm, x0 - 0.3, x0, y0, y1, ROOF_Z - 0.4, ROOF_Z + 0.2)
box(bm, x1, x1 + 0.3, y0, y1, ROOF_Z - 0.4, ROOF_Z + 0.2)
add_mesh("MC_roof_iron", bm, [IRON, PAINT])
add_mesh("MC_roof_glass", glass_bm, [GLASS])

# --- Side / end glazing walls so sky doesn't read as sea beyond the floor ---
bm = bmesh.new()
# south wall (behind camera-ish / far side from hammer look) — actually camera looks +Y-ish from -Y
# put glazed walls on north far end and partial sides
box(bm, x0, x1, y1, y1 + 0.25, 0, ROOF_Z)  # north end wall (iron mullion massing)
# west/east aisle walls beyond galleries (solid-ish to kill horizon)
box(bm, x0 - 0.25, x0, y0, y1, 0, ROOF_Z)
box(bm, x1, x1 + 0.25, y0, y1, 0, ROOF_Z)
# south low screen behind camera so we don't see infinite floor->sky
box(bm, x0, x1, y0 - 0.25, y0, 0, 12.0)
add_mesh("MC_walls", bm, [PAINT, IRON])

# Glass infill on north wall (above 8 ft)
gb = bmesh.new()
box(gb, x0 + 1, x1 - 1, y1 - 0.05, y1 + 0.05, 8.0, ROOF_Z - 0.5)
add_mesh("MC_wall_glass", gb, [GLASS])

# --- Neighbouring machine block-outs ---
def machine_block(name, loc, sx=8, sy=5, sz=11):
    bm = bmesh.new()
    box(bm, -sx / 2, sx / 2, -sy / 2, sy / 2, 0, sz * 0.55)
    # uprights / flywheel stand-in
    lathe(bm, [(0, sz * 0.4), (sx * 0.22, sz * 0.4), (sx * 0.22, sz * 0.95), (0, sz * 0.95)], 16,
          Matrix.Translation((0, 0, 0)))
    box(bm, -sx * 0.15, sx * 0.15, -sy * 0.15, sy * 0.15, sz * 0.55, sz)
    add_mesh(name, bm, [MACH, IRON], loc=loc)

machine_block("MC_nbr_press", (ax - 28, ay + 18, 0), 10, 6, 12)
machine_block("MC_nbr_lathe", (ax + 30, ay + 10, 0), 7, 4, 8)
machine_block("MC_nbr_boiler", (ax - 32, ay - 8, 0), 9, 5, 10)
machine_block("MC_nbr_engine", (ax + 26, ay - 14, 0), 8, 5, 9)
# low cases / barriers between
bm = bmesh.new()
box(bm, ax - 50, ax - 40, ay + 2, ay + 8, 0, 3.5)
box(bm, ax + 40, ax + 50, ay + 2, ay + 8, 0, 3.5)
add_mesh("MC_nbr_cases", bm, [WOOD, MACH])

# --- Kill any CPL/GT horizon ground disks if present ---
for o in list(bpy.data.objects):
    n = o.name.lower()
    if "horizon" in n or o.name.startswith("CPL_Horizon") or o.name.startswith("CPL_Ground"):
        o.hide_render = True
        print("HIDE_HORIZON", o.name, flush=True)

# --- interior_machinery world (no outdoor sea band) ---
sc = bpy.context.scene
# Soft high sky through glass: low-strength pale world, not Nishita sea rim
w = bpy.data.worlds.get("MC_World") or bpy.data.worlds.new("MC_World")
sc.world = w
w.use_nodes = True
nt = w.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
out_n = nt.nodes.new("ShaderNodeOutputWorld")
bg = nt.nodes.new("ShaderNodeBackground")
bg.inputs["Color"].default_value = (0.62, 0.68, 0.74, 1)  # pale daylit glass
bg.inputs["Strength"].default_value = 0.35
nt.links.new(bg.outputs[0], out_n.inputs[0])
# Sun-ish area through roof
for lamp_name in ("GT_Sun", "CPL_Sun", "Sun"):
    o = bpy.data.objects.get(lamp_name)
    if o and o.type == "LIGHT":
        o.hide_render = True
sun = bpy.data.lights.new("MC_Sun", "SUN")
sun.energy = 2.4
sun.angle = math.radians(5)
sun.color = (1.0, 0.97, 0.92)
so = bpy.data.objects.new("MC_Sun", sun)
sc.collection.objects.link(so)
so.rotation_euler = (math.radians(50), 0, math.radians(35))
# soft fill from gallery
fill = bpy.data.lights.new("MC_Fill", "AREA")
fill.energy = 250
fill.size = ft(40)
fill.color = (0.85, 0.90, 0.95)
fo = bpy.data.objects.new("MC_Fill", fill)
sc.collection.objects.link(fo)
fo.location = Vector((ft(ax), ft(ay - 10), ft(GAL_Z + 8)))
fo.rotation_euler = (math.radians(90), 0, 0)
sc.view_settings.exposure = -1.65  # interior_machinery
try:
    sc.view_settings.view_transform = "AgX"
except TypeError:
    pass
print("LIGHTING interior_machinery exposure", sc.view_settings.exposure, flush=True)

# --- Reframe CP024_ram_start: back + raise so top reads against gallery/roof ---
cam = bpy.data.objects["CP024_ram_start"]
anchor = empty.matrix_world.translation.copy()
# eye ~7.0 ft, ~48 ft back, slight side
cam.location = Vector((anchor.x + 4.0 * FT, anchor.y - 48.0 * FT, 7.0 * FT))
target = Vector((anchor.x, anchor.y, 14.0 * FT))  # aim mid-upper machine / gallery line
look = (target - cam.location).normalized()
world_up = Vector((0, 0, 1))
right = look.cross(world_up).normalized()
up = right.cross(look).normalized()
cam.matrix_world = Matrix([
    [right.x, up.x, (-look).x, cam.location.x],
    [right.y, up.y, (-look).y, cam.location.y],
    [right.z, up.z, (-look).z, cam.location.z],
    [0, 0, 0, 1],
])
cam.data.lens = 35.0
cam["candidate"] = "CP024_court"
print("CAM_FT", [round(v / FT, 2) for v in cam.location], "look_z", 14.0, flush=True)

# Hide outdoor approach cams' empty sky by not rendering them this pass
for cname in ("CP024_approach_start", "CP024_approach_end"):
    c = bpy.data.objects.get(cname)
    if c:
        c["candidate"] = "CP024_court"

txt = bpy.data.texts.get("CREDIT_HAM_COURT") or bpy.data.texts.new("CREDIT_HAM_COURT")
txt.clear()
txt.write(
    "CANDIDATE CP024 Machinery Court setting (2026-10-27)\n"
    "KEEP hammer model already in live e02. This candidate wraps it in an HP 1851\n"
    "Machinery Court block-out: 24 ft cast-iron columns, gallery + girders, glazed\n"
    "ridge-and-furrow roof, boarded floor, neighbouring machine block-outs.\n"
    "World = pale daylit glass (no Nishita sea horizon). Lighting case: interior_machinery.\n"
    "CP024_ram_start: 35 mm, eye 7 ft, ~48 ft back; look mid-upper so top reads against\n"
    "gallery/roof. Claude west nave not appended this pass (local court is self-contained);\n"
    "may append read-only with credit on a later pass if needed.\n"
)

bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out, "MC objs", len(MC.objects), flush=True)
