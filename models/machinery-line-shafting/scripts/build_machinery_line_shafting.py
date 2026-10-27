#!/usr/bin/env python3
"""
Machinery line shafting — Crystal Palace film prop (candidate #34 core).

A 4-bay overhead line-shaft run of the kind that drove the 1851 machinery
court (Dickinson plate XXI): floor standards with plummer-block bearings,
a main shaft with graduated pulleys, one countershaft, and wide leather
belts dropping to plain floor machine bases. No individual machine from
the plate is modelled — see NOTES.md for the interpretation statement.

Units: metres. X = along the run, Y = depth, Z = up. Floor at z=0,
origin at base centre. Blender 4.2, headless.
"""
import bpy
import math
import json
import os
import sys
from mathutils import Vector

# ---------------------------------------------------------------- parameters
BAY = 7.315            # 24 ft building module (documented) — bay spacing
BAYS = 4
RUN_LEN = BAY * BAYS   # 29.26 m overall
SHAFT_Z = 4.00         # main shaft centre height (inferred)
SHAFT_R = 0.045        # main shaft radius, Ø90 mm ~ 3.5 in (inferred)
COUNTER_Z = 2.60       # countershaft centre height (inferred)
COUNTER_Y = 1.15       # countershaft lateral offset (inferred)
COUNTER_R = 0.040

OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if "--out" in sys.argv:
    OUT_DIR = sys.argv[sys.argv.index("--out") + 1]
RENDERS = os.path.join(OUT_DIR, "renders")
WORK = os.path.join(OUT_DIR, "work")
os.makedirs(RENDERS, exist_ok=True)
os.makedirs(WORK, exist_ok=True)

# ---------------------------------------------------------------- scene reset
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()
for coll in list(bpy.data.collections):
    if coll.name != "Collection":
        bpy.data.collections.remove(coll)
for block in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
    pass  # leftovers are unlinked; harmless

MODEL = bpy.data.collections.new("MODEL")
bpy.context.scene.collection.children.link(MODEL)
RIG = bpy.data.collections.new("RIG")
bpy.context.scene.collection.children.link(RIG)

# ---------------------------------------------------------------- materials
def make_mat(name, color, roughness, metallic):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m

IRON = make_mat("CastIronPainted", (0.055, 0.068, 0.062), 0.62, 0.55)   # near-black green-grey painted iron
IRON_DARK = make_mat("CastIronDark", (0.035, 0.038, 0.038), 0.7, 0.5)
STEEL = make_mat("MachinedSteel", (0.42, 0.45, 0.48), 0.34, 1.0)
LEATHER = make_mat("BeltLeather", (0.205, 0.118, 0.058), 0.92, 0.0)
BRASS = make_mat("BrassOilCup", (0.38, 0.26, 0.09), 0.35, 1.0)
GROUND_M = make_mat("RigGround", (0.52, 0.52, 0.52), 1.0, 0.0)

# ---------------------------------------------------------------- helpers
def _link(obj, coll):
    for c in obj.users_collection:
        c.objects.unlink(obj)
    coll.objects.link(obj)
    if obj.data and hasattr(obj.data, "materials"):
        pass
    return obj

def box(name, size, loc, mat, coll=MODEL, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.dimensions = size
    if mat:
        o.data.materials.append(mat)
    return _link(o, coll)

def cyl(name, radius, depth, loc, mat, coll=MODEL, rot=(0.0, 0.0, 0.0), verts=28):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth,
                                        location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    if mat:
        o.data.materials.append(mat)
    return _link(o, coll)

X_AXIS = (0.0, math.pi / 2, 0.0)   # rotate a Z-cylinder onto the X axis

def pulley(name, x, y, z, r, w):
    """Solid-web pulley: disc + hub + collars, axis along X."""
    g = []
    g.append(cyl(name + "_web", r, w, (x, y, z), IRON, rot=X_AXIS, verts=40))
    g.append(cyl(name + "_hub", 0.088, w + 0.05, (x, y, z), IRON_DARK, rot=X_AXIS, verts=24))
    g.append(cyl(name + "_rimface", r - 0.012, w + 0.006, (x, y, z), IRON_DARK, rot=X_AXIS, verts=40))
    return g

def plummer_top(name, x, y, z_shaft):
    """Bearing housing straddling the shaft at centre height z_shaft."""
    g = []
    g.append(box(name + "_block", (0.30, 0.30, 0.20), (x, y, z_shaft - 0.03), IRON))
    g.append(cyl(name + "_cap", 0.105, 0.30, (x, y, z_shaft + 0.015), IRON_DARK, rot=X_AXIS, verts=24))
    for s in (-1, 1):
        g.append(cyl(name + f"_bolt{s}", 0.016, 0.06, (x, y + s * 0.115, z_shaft + 0.10), STEEL, verts=12))
    g.append(cyl(name + "_oilcup", 0.020, 0.055, (x, y, z_shaft + 0.135), BRASS, verts=12))
    return g

def standard(name, x):
    """Floor standard (A-frame in the YZ plane) carrying the main shaft."""
    g = []
    g.append(box(name + "_foot", (1.10, 0.70, 0.09), (x, 0, 0.045), IRON))
    leg_top_z = SHAFT_Z - 0.16
    leg_dy = 0.24 - 0.055          # foot spread y=+-0.24 -> top y=+-0.055
    leg_dz = leg_top_z - 0.09
    leg_len = math.hypot(leg_dy, leg_dz)
    ang = math.atan2(leg_dy, leg_dz)
    for s in (-1, 1):
        g.append(box(name + f"_leg{s}", (0.16, 0.13, leg_len),
                     (x, s * (0.24 + 0.055) / 2, (0.09 + leg_top_z) / 2),
                     IRON, rot=(s * ang, 0.0, 0.0)))
    g.append(box(name + "_tie", (0.09, 0.40, 0.09), (x, 0, 1.85), IRON_DARK))
    g.append(box(name + "_neck", (0.24, 0.20, 0.22), (x, 0, leg_top_z + 0.06), IRON))
    g += plummer_top(name + "_brg", x, 0, SHAFT_Z)
    return g

def counter_standard(name, x):
    """Shorter single-post standard for the countershaft."""
    g = []
    g.append(box(name + "_foot", (0.80, 0.50, 0.08), (x, COUNTER_Y, 0.04), IRON))
    g.append(box(name + "_post", (0.18, 0.18, COUNTER_Z - 0.20), (x, COUNTER_Y, (COUNTER_Z - 0.12) / 2 + 0.04), IRON))
    g.append(box(name + "_neck", (0.22, 0.20, 0.20), (x, COUNTER_Y, COUNTER_Z - 0.10), IRON))
    g += plummer_top(name + "_brg", x, COUNTER_Y, COUNTER_Z)
    return g

def machine_base(name, x, y, pulley_r, pulley_w):
    """Plain floor machine base: plinth, two bearing pedestals, short shaft
    and one pulley. Deliberately NO machine silhouette above it."""
    g = []
    g.append(box(name + "_plinth", (1.15, 0.72, 0.22), (x, y, 0.11), IRON_DARK))
    g.append(box(name + "_bed", (0.95, 0.56, 0.07), (x, y, 0.255), IRON))
    shaft_z = 0.55
    for s in (-1, 1):
        g.append(box(name + f"_ped{s}", (0.15, 0.15, shaft_z - 0.29 + 0.10), (x + s * 0.30, y, (0.29 + shaft_z) / 2 - 0.02), IRON))
        g.append(box(name + f"_brg{s}", (0.17, 0.19, 0.13), (x + s * 0.30, y, shaft_z), IRON_DARK))
    g.append(cyl(name + "_shaft", 0.035, 0.80, (x, y, shaft_z), STEEL, rot=X_AXIS, verts=20))
    g += pulley(name + "_pulley", x, y, shaft_z, pulley_r, pulley_w)
    return g

# ---------------------------------------------------------------- belt builder
def _arc_samples(c, r, a0, a1, other, step=math.radians(5)):
    """Sample the wrap arc on circle c from angle a0 to a1, choosing the
    sweep direction whose arc bulges away from the other pulley centre."""
    def pt(a):
        return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))
    # ccw sweep
    ccw = (a1 - a0) % (2 * math.pi)
    mid_ccw = pt(a0 + ccw / 2)
    cw = (a0 - a1) % (2 * math.pi)
    mid_cw = pt(a0 - cw / 2)
    d_ccw = math.hypot(mid_ccw[0] - other[0], mid_ccw[1] - other[1])
    d_cw = math.hypot(mid_cw[0] - other[0], mid_cw[1] - other[1])
    if d_ccw >= d_cw:
        sweep, total = 1, ccw
    else:
        sweep, total = -1, cw
    n = max(2, int(total / step) + 1)
    out = []
    for i in range(n + 1):
        a = a0 + sweep * total * i / n
        p = pt(a)
        out.append((p, (math.cos(a), math.sin(a))))
    return out

def belt(name, A, rA, B, rB, x, width, thick=0.006, sag_a=0.0, sag_b=0.0):
    """Open flat belt between two pulleys whose axes run along X.
    A, B are (y, z) centres; the belt loop lies in the YZ plane at fixed x.
    sag_a / sag_b displace the two strands inward (negative = outward bow)."""
    dy, dz = B[0] - A[0], B[1] - A[1]
    L = math.hypot(dy, dz)
    phi = math.atan2(dz, dy)
    cos_a = max(-1.0, min(1.0, (rA - rB) / L))
    alpha = math.acos(cos_a)
    n1 = (math.cos(phi + alpha), math.sin(phi + alpha))
    n2 = (math.cos(phi - alpha), math.sin(phi - alpha))
    A1 = (A[0] + rA * n1[0], A[1] + rA * n1[1]); B1 = (B[0] + rB * n1[0], B[1] + rB * n1[1])
    A2 = (A[0] + rA * n2[0], A[1] + rA * n2[1]); B2 = (B[0] + rB * n2[0], B[1] + rB * n2[1])

    def strand(p, q, nrm, sag):
        pts = []
        steps = 7
        for i in range(steps + 1):
            t = i / steps
            px = p[0] + (q[0] - p[0]) * t
            pz = p[1] + (q[1] - p[1]) * t
            off = -sag * math.sin(math.pi * t)
            pts.append(((px + nrm[0] * off, pz + nrm[1] * off), nrm))
        return pts

    loop = []
    loop += strand(A1, B1, n1, sag_a)
    loop += _arc_samples(B, rB, math.atan2(n1[1], n1[0]), math.atan2(n2[1], n2[0]), A)[1:]
    loop += strand(B2, A2, n2, sag_b)
    loop += _arc_samples(A, rA, math.atan2(n2[1], n2[0]), math.atan2(n1[1], n1[0]), B)[1:]

    verts, faces = [], []
    N = len(loop)
    for (py, pz), (ny, nz) in loop:
        oy, oz = ny * thick / 2, nz * thick / 2
        verts += [(x - width / 2, py + oy, pz + oz), (x + width / 2, py + oy, pz + oz),
                  (x - width / 2, py - oy, pz - oz), (x + width / 2, py - oy, pz - oz)]
    for i in range(N):
        j = (i + 1) % N
        a, b = i * 4, j * 4
        faces += [(a, b, b + 1, a + 1),          # outer
                  (a + 2, a + 3, b + 3, b + 2),  # inner
                  (a, a + 2, b + 2, b),          # left edge
                  (a + 1, b + 1, b + 3, a + 3)]  # right edge
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    o = bpy.data.objects.new(name, mesh)
    MODEL.objects.link(o)
    o.data.materials.append(LEATHER)
    return o

# ---------------------------------------------------------------- assembly
std_xs = [(-BAYS / 2 + i) * BAY for i in range(BAYS + 1)]   # -14.63 .. +14.63
for i, sx in enumerate(std_xs):
    standard(f"Standard{i+1}", sx)

# main shaft + couplings
cyl("MainShaft", SHAFT_R, RUN_LEN + 0.6, (0, 0, SHAFT_Z), STEEL, rot=X_AXIS, verts=24)
for i in range(BAYS):
    cx = std_xs[i] + BAY / 2
    cyl(f"Coupling{i+1}", 0.085, 0.07, (cx, 0, SHAFT_Z), IRON_DARK, rot=X_AXIS, verts=20)

# main-shaft pulleys: (x, radius, width)
main_pulleys = [(-12.2, 0.45, 0.28), (-8.9, 0.30, 0.22), (-4.4, 0.375, 0.25),
                (-1.2, 0.25, 0.20), (2.8, 0.425, 0.28), (6.1, 0.275, 0.20),
                (9.6, 0.35, 0.24), (12.8, 0.225, 0.18)]
for i, (px, pr, pw) in enumerate(main_pulleys):
    pulley(f"MainPulley{i+1}", px, 0, SHAFT_Z, pr, pw)

# countershaft: standards, shaft, pulleys
counter_standard("CounterStd1", -6.9)
counter_standard("CounterStd2", -1.9)
cyl("CounterShaft", COUNTER_R, 5.6, (-4.4, COUNTER_Y, COUNTER_Z), STEEL, rot=X_AXIS, verts=20)
pulley("CounterPulleyDrive", -4.4, COUNTER_Y, COUNTER_Z, 0.30, 0.26)
pulley("CounterPulleyDrop", -5.6, COUNTER_Y, COUNTER_Z, 0.25, 0.22)

# floor machine bases (plinth + bearings + pulley only)
machine_base("Base1", -12.2, 0.0, 0.30, 0.28)
machine_base("Base2", 2.8, 0.0, 0.32, 0.28)
machine_base("Base3", 9.6, 0.0, 0.26, 0.24)
machine_base("Base4", -5.6, COUNTER_Y, 0.28, 0.22)

# belts — all loops lie in YZ planes (u=y, v=z)
belt("Belt1_drop", (0.0, SHAFT_Z), 0.45, (0.0, 0.55), 0.30, -12.2, 0.26, sag_a=-0.012, sag_b=0.0)
belt("Belt2_counter_drive", (0.0, SHAFT_Z), 0.375, (COUNTER_Y, COUNTER_Z), 0.30, -4.4, 0.24, sag_a=0.035, sag_b=0.0)
belt("Belt3_counter_drop", (COUNTER_Y, COUNTER_Z), 0.25, (COUNTER_Y, 0.55), 0.28, -5.6, 0.20, sag_a=-0.010, sag_b=0.0)
belt("Belt4_drop", (0.0, SHAFT_Z), 0.425, (0.0, 0.55), 0.32, 2.8, 0.26, sag_a=-0.012, sag_b=0.0)
belt("Belt5_drop", (0.0, SHAFT_Z), 0.35, (0.0, 0.55), 0.26, 9.6, 0.22, sag_a=-0.012, sag_b=0.0)

# ---------------------------------------------------------------- rig
bpy.context.scene.world = bpy.data.worlds.new("RigWorld") if not bpy.context.scene.world else bpy.context.scene.world
bpy.context.scene.world.use_nodes = True
bg = bpy.context.scene.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)
bg.inputs[1].default_value = 1.0

gnd = box("Ground", (110, 60, 0.1), (0, 0, -0.051), GROUND_M, coll=RIG)
bdt = box("Backdrop", (110, 0.1, 30), (0, 22, 15), GROUND_M, coll=RIG)

sun_data = bpy.data.lights.new("Sun", "SUN")
sun_data.energy = 3.2
sun_data.angle = 0.25
sun = bpy.data.objects.new("Sun", sun_data)
RIG.objects.link(sun)
sun.location = (-14, -18, 26)
sun.rotation_euler = (math.radians(52), math.radians(-8), math.radians(-32))

fill_data = bpy.data.lights.new("Fill", "AREA")
fill_data.energy = 900
fill_data.shape = "RECTANGLE"
fill_data.size = 24
fill_data.size_y = 10
fill = bpy.data.objects.new("Fill", fill_data)
RIG.objects.link(fill)
fill.location = (10, -20, 14)

def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()

def camera(name, loc, target, lens):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.clip_end = 500
    o = bpy.data.objects.new(name, cd)
    RIG.objects.link(o)
    o.location = loc
    look_at(o, target)
    return o

CAM_FRONT = camera("CamFront", (0, -34, 3.0), (0, 0, 2.15), 40)
CAM_SIDE = camera("CamSide", (-24, 3.0, 3.0), (0.5, 0, 2.0), 42)
CAM_34 = camera("Cam34", (16.5, -16.0, 7.5), (0, 0, 1.8), 42)

# ---------------------------------------------------------------- transforms + stats
bpy.context.view_layer.objects.active = None
for o in list(MODEL.objects):
    if o.type == "MESH":
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.select_all(action="DESELECT")

dg = bpy.context.evaluated_depsgraph_get()
tris = 0
meshes = 0
for o in MODEL.objects:
    if o.type == "MESH":
        meshes += 1
        ev = o.evaluated_get(dg)
        tris += sum(len(p.vertices) - 2 for p in ev.data.polygons)
stats = {"objects": meshes, "triangles": tris, "run_length_m": RUN_LEN,
         "bay_m": BAY, "shaft_height_m": SHAFT_Z}
print("STATS", json.dumps(stats))
with open(os.path.join(WORK, "stats.json"), "w") as f:
    json.dump(stats, f, indent=1)

# ---------------------------------------------------------------- save + export
blend_path = os.path.join(OUT_DIR, "machinery-line-shafting.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.ops.object.select_all(action="DESELECT")
for o in MODEL.objects:
    o.select_set(True)
glb_path = os.path.join(OUT_DIR, "machinery-line-shafting.glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format="GLB",
                          use_selection=True, export_apply=True)
bpy.ops.object.select_all(action="DESELECT")

# ---------------------------------------------------------------- renders
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.eevee.taa_render_samples = 64
scene.render.film_transparent = False
for cam, fname, rx, ry in ((CAM_FRONT, "front.png", 1600, 1000),
                           (CAM_SIDE, "side.png", 1400, 1000),
                           (CAM_34, "three-quarter.png", 1400, 1000)):
    scene.camera = cam
    scene.render.resolution_x = rx
    scene.render.resolution_y = ry
    scene.render.filepath = os.path.join(RENDERS, fname)
    bpy.ops.render.render(write_still=True)
    print("RENDERED", fname)
print("DONE")
