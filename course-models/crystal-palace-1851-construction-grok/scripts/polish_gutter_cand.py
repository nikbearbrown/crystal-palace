"""CANDIDATE: adopt Muse paxton-gutter profile into K-DRAIN (k01).
Hide KD_PaxtonGutters (+ related); append Muse Paxton_Gutter_24ft + Main_Gutter_24ft with credit.

  blender -b rounds/k01.blend -P scripts/polish_gutter_cand.py -- \
      --out rounds/candidates/k01_gutter.blend
"""
import bpy, os, sys, math
from mathutils import Vector, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MUSE = "/workspace/models-main-ro/models/paxton-gutter/paxton-gutter.blend"
FT = 0.3048

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/k01_gutter.blend"
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)

if not bpy.data.filepath:
    bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "rounds/k01.blend"))

# Hide our simplified Paxton troughs
for o in list(bpy.data.objects):
    pk = o.get("part_kind", "")
    if pk == "paxton_gutter" or o.name.startswith("KD_Paxton"):
        o.hide_render = True
        o.hide_viewport = True
        try:
            o.hide_set(True)
        except Exception:
            pass
    # also hide our box gutter stand-in if Muse main gutter covers it — keep box for column connection
    # leave KD_BoxGutter visible

# Clear prior muse gutter append
for o in list(bpy.data.objects):
    if o.name.startswith("MUSE_GUTTER_"):
        bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections):
    if c.name.startswith("MUSE_GUTTER"):
        bpy.data.collections.remove(c)

before = set(bpy.data.objects.keys())
with bpy.data.libraries.load(MUSE, link=False) as (data_from, data_to):
    data_to.objects = list(data_from.objects)

muse_col = bpy.data.collections.new("MUSE_GUTTER_PAXTON")
bpy.context.scene.collection.children.link(muse_col)

# Place Muse gutters: Muse origin = underside centre, length along X (24 ft).
# Our K-DRAIN Paxton gutters run along Y at several gx in PAX_X. Match first visible gutter.
# Find a hidden KD paxton to read placement, else default.
ref = None
for o in bpy.data.objects:
    if o.get("part_kind") == "paxton_gutter":
        ref = o
        break

# Collect Muse mesh objects (skip cameras/lights/ground)
new_objs = [o for o in bpy.data.objects if o.name not in before]
keep = []
for o in new_objs:
    if o.type != "MESH":
        for col in list(o.users_collection):
            col.objects.unlink(o)
        continue
    if o.name.lower().startswith("ground") or "Cam" in o.name:
        for col in list(o.users_collection):
            col.objects.unlink(o)
        continue
    keep.append(o)

# Parent all keep under an empty at scene placement
empty = bpy.data.objects.new("MUSE_GUTTER_ROOT", None)
muse_col.objects.link(empty)
# Position: K-DRAIN set is near origin of the cutaway. Place Paxton body along Y
# (rotate Muse X-run → Y-run) at first furrow line. From build_drain: PAX_X typically ±4 etc.
# Use x=4 ft, y=6 ft mid, z = pax underside ~ BOX related. Read from a KD object bbox.
z_place = 23.0 * FT  # BOX_Z0 was 23 ft in build_drain — gutters sit on roof
x_place = -4.0 * FT
y_place = 6.0 * FT
if ref:
    bb = [ref.matrix_world @ Vector(c) for c in ref.bound_box]
    xs = [v.x for v in bb]; ys = [v.y for v in bb]; zs = [v.z for v in bb]
    x_place = sum(xs) / len(xs)
    y_place = min(ys) + 0.5 * FT  # start near south end
    z_place = min(zs)
    print("REF paxton at", x_place, y_place, z_place, flush=True)

empty.location = Vector((x_place, y_place, z_place))
# Muse length along +X; our gutters along +Y → rotate 90° about Z
empty.rotation_euler = Euler((0, 0, math.pi / 2), "XYZ")

n = 0
for o in keep:
    for col in list(o.users_collection):
        col.objects.unlink(o)
    muse_col.objects.link(o)
    o.parent = empty
    if not o.name.startswith("MUSE_GUTTER_"):
        o.name = "MUSE_GUTTER_" + o.name
    o["credit"] = "Muse — paxton-gutter (Downes XII/XIII printed profile)"
    o["source_blend"] = MUSE
    o["part_kind"] = "paxton_gutter_muse"
    o["candidate"] = "CP014_gutter_muse"
    o.hide_render = False
    o.hide_viewport = False
    n += 1

# Also instance a second Paxton gutter at +8 ft in X (next furrow) if space
# Skip for clarity on gutter detail cam.

txt = bpy.data.texts.get("CREDIT_MUSE_GUTTER") or bpy.data.texts.new("CREDIT_MUSE_GUTTER")
txt.clear()
txt.write(
    "CANDIDATE — adopt Muse paxton-gutter into K-DRAIN (k01)\n"
    "models/paxton-gutter/ (origin/main via models-main-ro). Credit: Muse.\n"
    "Downes Plate XII Fig.10 printed: depth 6 in, base 5 in, cheek ~5.7 in;\n"
    "bar notches 10.5 in centres. Plate XIII main gutter included.\n"
    "Our KD_PaxtonGutters (KD03 simplified trough) hidden, not deleted.\n"
)

bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out, "muse_objs", n, flush=True)
