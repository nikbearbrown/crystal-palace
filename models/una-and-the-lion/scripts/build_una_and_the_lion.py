"""
Una and the Lion — John Bell (Sydenham display), procedural Blender 4.2 build.

Profile-first construction from the MET stereograph DP700246 (CC0):
lofted masses whose side silhouettes follow the photograph, with rounded
cross-sections. Dimensions photo-derived (see ../NOTES.md).

Outputs: ../una-and-the-lion.blend, ../una-and-the-lion.glb,
         ../renders/{front,side,three-quarter,photomatch}.png
Run: blender -b --python build_una_and_the_lion.py [-- final]
"""

import bpy
import math
import os
import random
import sys
from mathutils import Vector, Matrix, noise as mnoise

random.seed(11)

OUT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FINAL = "final" in sys.argv
RES = 1000 if FINAL else 640

# ----------------------------------------------------------------- materials

def make_material(name, color, roughness):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat

MARBLE = None  # set after scene clear
ROCK_M = None
EBON = None
PLATE_M = None

# ----------------------------------------------------------------- helpers

def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
        pass

def loft(name, stations, segs=18, cap=True, smooth=True):
    """Loft elliptical rings along a spine.
    stations: list of (centre Vector, half_w, half_h). Ring frame derived
    from the local tangent; half_w lies along the horizontal-ish side axis,
    half_h along the perpendicular 'up' axis of the ring plane."""
    n = len(stations)
    verts, faces = [], []
    world_up = Vector((0, 0, 1))
    for i, (c, hw, hh) in enumerate(stations):
        if i == 0:
            t = stations[1][0] - c
        elif i == n - 1:
            t = c - stations[i - 1][0]
        else:
            t = stations[i + 1][0] - stations[i - 1][0]
        t.normalize()
        if abs(t.dot(world_up)) > 0.9:
            side = Vector((1, 0, 0))
        else:
            side = t.cross(world_up).normalized()
        vert = side.cross(t).normalized()
        for j in range(segs):
            a = 2 * math.pi * j / segs
            v = c + side * (math.cos(a) * hw) + vert * (math.sin(a) * hh)
            verts.append(tuple(v))
    for i in range(n - 1):
        for j in range(segs):
            a = i * segs + j
            b = i * segs + (j + 1) % segs
            c2 = (i + 1) * segs + (j + 1) % segs
            d = (i + 1) * segs + j
            faces.append((a, b, c2, d))
    if cap:
        for idx, flip in ((0, True), (n - 1, False)):
            c = stations[idx][0]
            ci = len(verts)
            verts.append(tuple(c))
            base = idx * segs
            for j in range(segs):
                if flip:
                    faces.append((ci, base + (j + 1) % segs, base + j))
                else:
                    faces.append((ci, base + j, base + (j + 1) % segs))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    if smooth:
        for p in mesh.polygons:
            p.use_smooth = True
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

def ball(name, loc, scale, mat=None, seg=32, rings=24, disp=0.0, freq=3.0, seed=0.0,
         disp2=0.0):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=seg, ring_count=rings, location=loc)
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if disp > 0:
        me = obj.data
        for v in me.vertices:
            n = v.co.normalized()
            d = mnoise.noise(Vector((v.co.x * freq + seed,
                                     v.co.y * freq + seed * 1.7,
                                     v.co.z * freq - seed)))
            v.co += n * d * disp
        if disp2 > 0:
            for v in me.vertices:
                n = v.co.normalized()
                d = mnoise.noise(Vector((v.co.x * 5.5 + seed,
                                         v.co.y * 5.5 + seed,
                                         v.co.z * 2.1 - seed)))
                v.co += n * d * disp2
        me.update()
    for p in obj.data.polygons:
        p.use_smooth = True
    if mat:
        obj.data.materials.append(mat)
    return obj

def tube(name, points, r0, r1, mat=None, segs=10):
    stations = []
    n = len(points)
    for i, p in enumerate(points):
        r = r0 + (r1 - r0) * (i / max(n - 1, 1))
        stations.append((Vector(p), r, r))
    obj = loft(name, stations, segs=segs)
    if mat:
        obj.data.materials.append(mat)
    return obj

def ribbon(name, path, widths, folds=4, amp=0.018, thick=0.012, mat=None,
           pool_dir=None):
    """A hanging cloth sheet: rows follow `path` (top->bottom), columns run
    across the width (local X-ish), with sine folds across the width whose
    offset acts along the sheet normal (+Y side). pool_dir: if given, the
    last rows tilt forward onto a surface (normal rotates to +Z)."""
    rows = len(path)
    cols = 13
    verts, faces = [], []
    for i, p in enumerate(path):
        w = widths[i]
        tilt = 0.0
        if pool_dir is not None:
            tilt = pool_dir[i]
        for j in range(cols):
            f = j / (cols - 1)          # 0..1 across
            x = p[0] + (f - 0.5) * w
            fold = math.sin(f * folds * 2 * math.pi) * amp * (0.4 + 0.6 * i / max(rows - 1, 1))
            # sheet normal starts as +Y; when pooling, rotate towards +Z
            ny = math.cos(tilt)
            nz = math.sin(tilt)
            y = p[1] + fold * ny
            z = p[2] + fold * nz
            verts.append((x, y, z))
    for i in range(rows - 1):
        for j in range(cols - 1):
            a = i * cols + j
            faces.append((a, a + 1, a + cols + 1, a + cols))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    for p in mesh.polygons:
        p.use_smooth = True
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if mat:
        obj.data.materials.append(mat)
    if thick:
        mod = obj.modifiers.new("ClothThickness", "SOLIDIFY")
        mod.thickness = thick
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    return obj

def rect_loft(name, profile, chamfer=0.03, mat=None):
    """Vertical loft of rounded-corner rectangles.
    profile: list of (z, half_x, half_y)."""
    def ring(hx, hy, z):
        pts = []
        c = min(chamfer, hx * 0.4, hy * 0.4)
        corners = [(hx - c, hy - c), (-(hx - c), hy - c),
                   (-(hx - c), -(hy - c)), (hx - c, -(hy - c))]
        steps = 3
        for (cx, cy) in corners:
            for k in range(steps + 1):
                a = math.atan2(cy, cx) - math.pi / 4 + (k / steps) * (math.pi / 2)
                pts.append((cx + math.cos(a) * c, cy + math.sin(a) * c, z))
        return pts
    verts, faces = [], []
    rows = len(profile)
    per = None
    for (z, hx, hy) in profile:
        r = ring(hx, hy, z)
        per = len(r)
        verts.extend(r)
    for i in range(rows - 1):
        for j in range(per):
            a = i * per + j
            b = i * per + (j + 1) % per
            faces.append((a, b, b + per, a + per))
    # top and bottom fans
    for idx, flip in ((0, True), (rows - 1, False)):
        z, hx, hy = profile[idx]
        ci = len(verts)
        verts.append((0, 0, z))
        base = idx * per
        for j in range(per):
            if flip:
                faces.append((ci, base + (j + 1) % per, base + j))
            else:
                faces.append((ci, base + j, base + (j + 1) % per))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if mat:
        obj.data.materials.append(mat)
    return obj

def box(name, loc, size, mat=None, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel > 0:
        mod = obj.modifiers.new("bev", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    if mat:
        obj.data.materials.append(mat)
    return obj

MODEL_OBJECTS = []

def reg(obj):
    MODEL_OBJECTS.append(obj)
    return obj

# ----------------------------------------------------------------- scene

clear_scene()

MARBLE = make_material("Marble", (0.905, 0.890, 0.862), 0.38)
ROCK_M = make_material("RockBase", (0.44, 0.42, 0.40), 0.95)
EBON = make_material("EbonisedWood", (0.010, 0.009, 0.008), 0.42)
PLATE_M = make_material("LabelPlate", (0.016, 0.015, 0.014), 0.60)

V = Vector

# ----------------------------------------------------------------- plinth
# Ebonised group plinth of the standard court family: stepped foot, straight
# shaft, thin cap. Photo-measured height 1.10 m (see NOTES.md).
plinth_profile = [
    (0.00, 1.225, 0.490),
    (0.03, 1.225, 0.490),
    (0.10, 1.200, 0.472),
    (0.15, 1.183, 0.452),
    (0.19, 1.180, 0.450),
    (1.01, 1.180, 0.450),
    (1.05, 1.205, 0.470),
    (1.10, 1.220, 0.485),
]
plinth = reg(rect_loft("Plinth", plinth_profile, chamfer=0.025, mat=EBON))

# Label zone: shallow UNLETTERED plate on the display front (-Y face),
# following the display-plinth family convention (photos show painted
# lettering; no text invented).
plate = reg(box("LabelPlate", (0.0, -0.447, 0.74), (0.66, 0.012, 0.30),
                mat=PLATE_M))

# ----------------------------------------------------------------- rock slab
# The sculpture's own rough rock base, sitting on the plinth.
rock = reg(ball("RockSlab", (0, 0, 1.172), (1.14, 0.455, 0.145),
                mat=ROCK_M, seg=48, rings=24, disp=0.036, freq=2.4, seed=3.1, disp2=0.018))
# flatten its underside/top a touch by scaling done above; add edge rocks
for i, (rx, ry, rz, s) in enumerate([
        (-1.02, 0.30, 1.12, 0.125), (0.95, -0.28, 1.11, 0.145),
        (0.55, 0.36, 1.10, 0.10), (-0.55, -0.37, 1.11, 0.115),
        (1.05, 0.22, 1.13, 0.09)]):
    reg(ball(f"RockEdge{i}", (rx, ry, rz), (s, s * 0.8, s * 0.55),
             mat=ROCK_M, seg=20, rings=12, disp=0.02, freq=4.0, seed=i * 1.3))

ROCK_TOP = 1.30

# ----------------------------------------------------------------- lion body
body_stations = [
    (V((-1.00, 0, 1.98)), 0.10, 0.16),
    (V((-0.92, 0, 2.01)), 0.17, 0.24),
    (V((-0.78, 0, 2.04)), 0.215, 0.28),
    (V((-0.60, 0, 2.05)), 0.225, 0.285),
    (V((-0.40, 0, 2.04)), 0.215, 0.27),
    (V((-0.20, 0, 2.03)), 0.210, 0.26),
    (V((0.00, 0, 2.045)), 0.215, 0.255),
    (V((0.20, 0, 2.04)), 0.225, 0.28),
    (V((0.38, 0, 2.035)), 0.235, 0.315),
    (V((0.52, 0, 2.035)), 0.235, 0.320),
    (V((0.64, 0, 2.03)), 0.220, 0.29),
    (V((0.74, 0, 2.00)), 0.190, 0.25),
]
reg(loft("LionBody", body_stations, segs=20)).data.materials.append(MARBLE)

# haunches (blend body into hind legs)
for side, sgn in (("Near", 1), ("Far", -1)):
    reg(ball(f"Haunch{side}", (-0.70, sgn * 0.14, 1.90),
             (0.24, 0.105, 0.25), mat=MARBLE, seg=28, rings=18))
# shoulder masses
for side, sgn in (("Near", 1), ("Far", -1)):
    reg(ball(f"Shoulder{side}", (0.47, sgn * 0.14, 1.90),
             (0.22, 0.10, 0.30), mat=MARBLE, seg=28, rings=18))

# ----------------------------------------------------------------- lion legs
def leg(name, path, radii, mat=MARBLE):
    stations = [(V(p), r, r * 1.08) for p, r in zip(path, radii)]
    o = loft(name, stations, segs=14)
    o.data.materials.append(mat)
    return reg(o)

def paw(name, loc, yaw=0.0):
    p = ball(name, loc, (0.105, 0.062, 0.042), mat=MARBLE, seg=22, rings=14)
    # toe bumps at the front edge
    lx, ly, lz = loc
    for k, dy in enumerate((-0.036, 0.0, 0.036)):
        reg(ball(f"{name}Toe{k}", (lx + 0.085, ly + dy, lz - 0.012),
                 (0.038, 0.026, 0.028), mat=MARBLE, seg=12, rings=8))
    return p

# near foreleg: strides forward (pace gait)
leg("ForelegNear", [(0.52, -0.145, 1.98), (0.615, -0.155, 1.78),
                    (0.70, -0.165, 1.60), (0.84, -0.175, 1.42)],
    [0.088, 0.068, 0.050, 0.046])
paw("PawForeNear", (0.93, -0.18, 1.335))
# far foreleg: planted, more vertical, set back
leg("ForelegFar", [(0.50, 0.145, 1.97), (0.56, 0.16, 1.76),
                   (0.60, 0.165, 1.58), (0.63, 0.17, 1.42)],
    [0.085, 0.065, 0.049, 0.045])
paw("PawForeFar", (0.67, 0.17, 1.335))
# near hind leg
leg("HindlegNear", [(-0.70, -0.16, 1.99), (-0.79, -0.185, 1.74),
                    (-0.88, -0.19, 1.54), (-0.83, -0.19, 1.40)],
    [0.125, 0.085, 0.052, 0.047])
paw("PawHindNear", (-0.79, -0.195, 1.345))
# far hind leg: extended slightly further back
leg("HindlegFar", [(-0.73, 0.155, 1.98), (-0.85, 0.17, 1.72),
                   (-0.95, 0.175, 1.53), (-0.91, 0.175, 1.40)],
    [0.12, 0.082, 0.05, 0.046])
paw("PawHindFar", (-0.88, 0.18, 1.345))

# tail: hangs at the rear, tuft curving forward on the rock
reg(tube("Tail", [(-0.99, -0.01, 2.08), (-1.04, -0.02, 1.82),
                  (-1.03, -0.03, 1.56), (-0.97, -0.04, 1.38),
                  (-0.86, -0.045, 1.345)],
         0.030, 0.020, mat=MARBLE, segs=10))
reg(ball("TailTuft", (-0.79, -0.05, 1.35), (0.085, 0.048, 0.045),
         mat=MARBLE, seg=18, rings=12, disp=0.012, freq=6.0, seed=2.2))

# ----------------------------------------------------------------- mane + head
reg(ball("Mane", (0.67, 0, 2.00), (0.330, 0.340, 0.51),
         mat=MARBLE, seg=48, rings=32, disp=0.072, freq=2.6, seed=5.0, disp2=0.046))
reg(ball("ManeChest", (0.60, 0, 1.66), (0.20, 0.26, 0.225),
         mat=MARBLE, seg=40, rings=26, disp=0.060, freq=3.0, seed=8.4, disp2=0.036))
reg(ball("ManeTop", (0.76, 0, 2.36), (0.22, 0.27, 0.16),
         mat=MARBLE, seg=36, rings=22, disp=0.058, freq=3.4, seed=1.9, disp2=0.034))

# head: bowed low, muzzle forward-down; schematic (mane covers the ears)
reg(ball("FaceMask", (0.905, 0, 1.925), (0.130, 0.130, 0.130),
         mat=MARBLE, seg=26, rings=18))
reg(ball("Skull", (0.900, 0, 1.970), (0.150, 0.138, 0.140),
         mat=MARBLE, seg=30, rings=20))
for sgn in (1, -1):
    reg(ball(f"Cheek{sgn}", (0.875, sgn * 0.078, 1.895),
             (0.095, 0.062, 0.085), mat=MARBLE, seg=22, rings=14))
    reg(ball(f"Ear{sgn}", (0.83, sgn * 0.095, 2.10),
             (0.036, 0.026, 0.042), mat=MARBLE, seg=14, rings=10))
muzzle = reg(box("Muzzle", (1.030, 0, 1.780), (0.18, 0.155, 0.15),
                 mat=MARBLE, bevel=0.045))
muzzle.rotation_euler = (0, math.radians(-14), 0)
bpy.context.view_layer.objects.active = muzzle
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
reg(ball("ChinMane", (0.94, 0, 1.585), (0.105, 0.135, 0.115),
         mat=MARBLE, seg=24, rings=16, disp=0.03, freq=3.4, seed=6.3, disp2=0.02))
reg(ball("Nose", (1.085, 0, 1.838), (0.045, 0.062, 0.032),
         mat=MARBLE, seg=16, rings=10))
jaw = reg(box("Jaw", (1.000, 0, 1.655), (0.15, 0.12, 0.07),
              mat=MARBLE, bevel=0.028))
jaw.rotation_euler = (0, math.radians(-10), 0)
bpy.context.view_layer.objects.active = jaw
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

# ----------------------------------------------------------------- saddle cloth
cloth_stations = [
    (V((-0.66, 0, 2.335)), 0.27, 0.020),
    (V((-0.50, 0, 2.338)), 0.30, 0.022),
    (V((-0.34, 0, 2.313)), 0.305, 0.022),
    (V((-0.16, 0, 2.298)), 0.29, 0.020),
    (V((0.02, 0, 2.303)), 0.26, 0.020),
    (V((0.16, 0, 2.328)), 0.20, 0.018),
]
reg(loft("SaddleCloth", cloth_stations, segs=16)).data.materials.append(MARBLE)

# ----------------------------------------------------------------- Una torso
# spine near-vertical: ring half_w lies along X (front-back depth),
# half_h along Y (body width) — see loft() frame convention.
# Una faces -Y (the display front): her left-right axis is X,
# front-back is Y. For the
# near-vertical spine, loft() puts half_w along X (body width) and
# half_h along Y (body depth).
torso_stations = [
    (V((-0.365, -0.020, 2.315)), 0.175, 0.132),
    (V((-0.360, -0.020, 2.385)), 0.180, 0.138),
    (V((-0.352, -0.018, 2.480)), 0.168, 0.130),
    (V((-0.342, -0.016, 2.595)), 0.127, 0.103),
    (V((-0.336, -0.014, 2.720)), 0.144, 0.110),
    (V((-0.332, -0.012, 2.830)), 0.154, 0.126),
    (V((-0.328, -0.010, 2.930)), 0.150, 0.110),
    (V((-0.324, -0.008, 2.985)), 0.160, 0.094),
    (V((-0.320, -0.006, 3.030)), 0.075, 0.058),
]
reg(loft("UnaTorso", torso_stations, segs=20)).data.materials.append(MARBLE)
for sgn in (1, -1):
    reg(ball(f"Breast{sgn}", (-0.332 + sgn * 0.055, -0.108, 2.822),
             (0.042, 0.034, 0.042), mat=MARBLE, seg=18, rings=12))

# neck
reg(tube("Neck", [(-0.318, -0.008, 3.00), (-0.312, -0.020, 3.06),
                  (-0.306, -0.034, 3.105)],
         0.047, 0.042, mat=MARBLE, segs=12))

# head — built facing -Y, bowed ~10 deg and turned ~10 deg toward +X
# (the direction of the lion's travel),
# rotated about the neck pivot.
PIVOT = V((-0.306, -0.030, 3.045))
HEAD_ROT = Matrix.Rotation(math.radians(10), 4, 'X') @ \
           Matrix.Rotation(math.radians(10), 4, 'Z')

def hp(p):
    return tuple(PIVOT + HEAD_ROT @ (V(p) - PIVOT))

skull = reg(ball("UnaHead", hp((-0.300, -0.052, 3.135)), (0.082, 0.076, 0.102),
                 mat=MARBLE, seg=28, rings=20))
reg(ball("UnaJaw", hp((-0.298, -0.088, 3.062)), (0.058, 0.048, 0.046),
         mat=MARBLE, seg=20, rings=14))
reg(tube("UnaNose", [hp((-0.299, -0.118, 3.128)), hp((-0.298, -0.138, 3.105)),
                     hp((-0.298, -0.128, 3.088))],
         0.013, 0.009, mat=MARBLE, segs=8))
# hair: smooth cap swept back to a low knot, centre parting (schematic mass)
reg(ball("UnaHair", hp((-0.302, -0.030, 3.152)), (0.087, 0.081, 0.106),
         mat=MARBLE, seg=28, rings=20))
reg(ball("UnaBun", hp((-0.300, 0.062, 3.085)), (0.046, 0.040, 0.046),
         mat=MARBLE, seg=16, rings=12))

# ----------------------------------------------------------------- Una arms
# her left arm (on the +X side of her body): reaches forward,
# hand resting on the mane
leg("ArmLeft", [(-0.185, -0.012, 2.955), (-0.04, -0.032, 2.845),
                (0.10, -0.050, 2.720), (0.32, -0.062, 2.565)],
    [0.047, 0.040, 0.033, 0.028])
hand_l = reg(ball("HandLeft", (0.50, -0.068, 2.485), (0.062, 0.034, 0.020),
                  mat=MARBLE, seg=16, rings=10))
hand_l.rotation_euler = (math.radians(18), math.radians(-24), math.radians(10))
bpy.context.view_layer.objects.active = hand_l
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
# right arm: bent across the waist, hand cradling the lily stems
leg("ArmRight", [(-0.465, -0.012, 2.955), (-0.435, -0.085, 2.80),
                 (-0.375, -0.140, 2.665), (-0.245, -0.158, 2.545)],
    [0.047, 0.040, 0.033, 0.028])
reg(ball("HandRight", (-0.185, -0.162, 2.515), (0.055, 0.032, 0.020),
         mat=MARBLE, seg=16, rings=10))

# lilies: stems fan up from her right hand across her lap; schematic trumpets
lily_tips = [(-0.255, -0.178, 2.620), (-0.315, -0.185, 2.660),
             (-0.375, -0.180, 2.610), (-0.225, -0.172, 2.570)]
for i, tip in enumerate(lily_tips):
    reg(tube(f"LilyStem{i}", [(-0.185, -0.162, 2.515),
                              (-0.21, -0.17, 2.55), tip],
             0.006, 0.005, mat=MARBLE, segs=6))
    fl = reg(ball(f"LilyFlower{i}", (tip[0], tip[1], tip[2] + 0.028),
                  (0.026, 0.026, 0.042), mat=MARBLE, seg=12, rings=8))
    fl.rotation_euler = (math.radians(24), math.radians(-12), 0)
    bpy.context.view_layer.objects.active = fl
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
for i, lp in enumerate([(-0.27, -0.175, 2.60), (-0.33, -0.178, 2.63)]):
    leaf = reg(ball(f"LilyLeaf{i}", lp, (0.030, 0.008, 0.012),
                    mat=MARBLE, seg=10, rings=6))
    leaf.rotation_euler = (0, math.radians(30 + i * 20), math.radians(15))
    bpy.context.view_layer.objects.active = leaf
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

# ----------------------------------------------------------------- Una legs
# sidesaddle: both legs together on the lion's left (+Y) flank
leg("LegNear", [(-0.295, -0.120, 2.350), (-0.225, -0.225, 2.285),
                (-0.165, -0.295, 2.235), (-0.205, -0.325, 1.95),
                (-0.235, -0.335, 1.70)],
    [0.078, 0.072, 0.056, 0.045, 0.034])
foot_n = reg(ball("FootNear", (-0.243, -0.338, 1.615), (0.030, 0.026, 0.075),
                  mat=MARBLE, seg=16, rings=10))
foot_n.rotation_euler = (0, math.radians(38), 0)
bpy.context.view_layer.objects.active = foot_n
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
leg("LegFar", [(-0.420, -0.095, 2.335), (-0.355, -0.180, 2.255),
               (-0.300, -0.232, 2.155), (-0.322, -0.262, 1.90),
               (-0.338, -0.270, 1.645)],
    [0.074, 0.068, 0.053, 0.043, 0.032])
foot_f = reg(ball("FootFar", (-0.343, -0.272, 1.565), (0.029, 0.025, 0.072),
                  mat=MARBLE, seg=16, rings=10))
foot_f.rotation_euler = (0, math.radians(40), 0)
bpy.context.view_layer.objects.active = foot_f
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

# ----------------------------------------------------------------- drapery
# great sweep: from her seat down the near flank, pooling on the rock
sweep_path = [(-0.27, -0.205, 2.33), (-0.245, -0.245, 2.05),
              (-0.205, -0.262, 1.76), (-0.15, -0.265, 1.50),
              (-0.06, -0.270, 1.345), (0.05, -0.300, 1.322),
              (0.17, -0.320, 1.315)]
sweep_w = [0.27, 0.30, 0.29, 0.29, 0.34, 0.42, 0.48]
sweep_pool = [0, 0, 0, 0, 0.5, 1.25, 1.45]
reg(ribbon("DrapeSweep", sweep_path, sweep_w, folds=4, amp=0.026,
           mat=MARBLE, pool_dir=sweep_pool))
# shoulder panel: hangs on the near flank in front of her legs, by the mane
panel_path = [(0.335, -0.225, 2.315), (0.345, -0.248, 2.10),
              (0.350, -0.255, 1.90), (0.348, -0.250, 1.735)]
panel_w = [0.22, 0.245, 0.255, 0.245]
reg(ribbon("DrapePanel", panel_path, panel_w, folds=5, amp=0.016,
           mat=MARBLE))
# small fall behind her seat on the far side (partly inferred — see NOTES)
back_path = [(-0.47, 0.175, 2.33), (-0.50, 0.215, 2.05),
             (-0.52, 0.225, 1.80)]
reg(ribbon("DrapeBack", back_path, [0.22, 0.23, 0.22], folds=4, amp=0.014,
           mat=MARBLE))

# ----------------------------------------------------------------- garland
garland_pts = [(-0.80, -0.085, 2.375), (-0.90, -0.150, 2.20),
               (-0.945, -0.185, 1.98), (-0.90, -0.195, 1.79),
               (-0.78, -0.175, 1.685), (-0.685, -0.150, 1.76)]
reg(tube("Garland", garland_pts, 0.016, 0.016, mat=MARBLE, segs=8))
import random as _r
_r.seed(4)
for i in range(16):
    t = i / 15
    # sample along the garland polyline roughly
    seg = min(int(t * (len(garland_pts) - 1)), len(garland_pts) - 2)
    f = t * (len(garland_pts) - 1) - seg
    a, b = V(garland_pts[seg]), V(garland_pts[seg + 1])
    p = a + (b - a) * f
    r = 0.020 + 0.010 * _r.random()
    reg(ball(f"GarlandFlower{i}", tuple(p), (r, r, r * 0.85),
             mat=MARBLE, seg=10, rings=8))
# small cluster at the garland's top — reads as a bird-like form in the
# photograph; modelled schematically (see NOTES)
reg(ball("RumpClusterBody", (-0.815, -0.055, 2.415), (0.052, 0.030, 0.034),
         mat=MARBLE, seg=14, rings=10))
reg(ball("RumpClusterHead", (-0.775, -0.045, 2.455), (0.019, 0.017, 0.019),
         mat=MARBLE, seg=10, rings=8))

# ----------------------------------------------------------------- stats + save
bpy.ops.object.select_all(action="DESELECT")
for o in MODEL_OBJECTS:
    o.select_set(True)
bpy.context.view_layer.objects.active = MODEL_OBJECTS[0]
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

tris = 0
xs, ys, zs = [], [], []
for o in MODEL_OBJECTS:
    tris += sum(len(p.vertices) - 2 for p in o.data.polygons)
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        xs.append(w.x); ys.append(w.y); zs.append(w.z)
print(f"[una] triangles: {tris}")
print(f"[una] bbox X {min(xs):.3f}..{max(xs):.3f} ({max(xs)-min(xs):.3f} m)")
print(f"[una] bbox Y {min(ys):.3f}..{max(ys):.3f} ({max(ys)-min(ys):.3f} m)")
print(f"[una] bbox Z {min(zs):.3f}..{max(zs):.3f} ({max(zs)-min(zs):.3f} m)")

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, "una-and-the-lion.blend"))
bpy.ops.export_scene.gltf(
    filepath=os.path.join(OUT_DIR, "una-and-the-lion.glb"),
    export_format="GLB", use_selection=True, export_apply=True)
print("[una] blend + glb saved")

# ----------------------------------------------------------------- render rig
# One fixed neutral-grey rig (house convention, scaled to the monument).
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 64 if FINAL else 32
scene.cycles.use_denoising = True
scene.render.resolution_x = RES
scene.render.resolution_y = RES
scene.render.film_transparent = False
scene.view_settings.view_transform = "Filmic"
scene.view_settings.look = "Medium Contrast"
scene.view_settings.exposure = 0.0

world = bpy.data.worlds.new("GreyWorld")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.22, 0.22, 0.22, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.4

ground_mat = make_material("BackdropGrey", (0.30, 0.30, 0.30), 0.95)
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
ground = bpy.context.view_layer.objects.active
ground.name = "Backdrop"
ground.data.materials.append(ground_mat)

TARGET = Vector((0, 0, 1.62))

def add_area(name, loc, size, energy):
    data = bpy.data.lights.new(name, "AREA")
    data.shape = "RECTANGLE"
    data.size = size[0]
    data.size_y = size[1]
    data.energy = energy
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    direction = TARGET - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return obj

add_area("Key", (4.6, -6.2, 7.4), (6.5, 4.5), 1150)
add_area("Fill", (-6.4, -3.4, 2.8), (5.5, 4.0), 380)
add_area("Rim", (-1.2, 6.0, 5.4), (5.5, 3.5), 750)

cam_data = bpy.data.cameras.new("Camera")
cam_data.lens = 50
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam

VIEWS = {
    "front": Vector((0.10, -8.8, 1.95)),        # display front: lion profile + Una front
    "side": Vector((8.8, 0.15, 1.95)),         # down the lion's axis: bowed head/mane
    "three-quarter": Vector((5.4, -6.9, 3.6)),
    "photomatch": Vector((2.60, -6.4, 2.70)),   # stereograph's viewpoint, approx.
}
os.makedirs(os.path.join(OUT_DIR, "renders"), exist_ok=True)
for name, pos in VIEWS.items():
    cam.location = pos
    tgt = Vector((0.0, 0, 1.66)) if name == "photomatch" else TARGET
    cam.rotation_euler = (tgt - pos).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(OUT_DIR, "renders", f"{name}.png")
    bpy.ops.render.render(write_still=True)
    print(f"[una] rendered {name}")

print("[una] done")
