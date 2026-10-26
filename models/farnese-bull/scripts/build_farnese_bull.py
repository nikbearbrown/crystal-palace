"""
Farnese Bull group — Sydenham Greek & Roman Court centrepiece (cast).
Procedural Blender 4.2 build. MASSING-LEVEL, LOOSE INTERPRETATION.

The only view in the collection (Delamotte album page, MET DP323102, CC0)
shows the group small, elevated, from the rear-left. Overall size, the
rocky mount, the dark low platform and the rearing silhouette are read
from that photograph. The figure arrangement follows the canonical
composition of the famous antique type (the Naples Farnese Bull) and is
CONVENTION, not observation — see ../NOTES.md. Never cite this model as
a documented reconstruction.

Outputs: ../farnese-bull.blend, ../farnese-bull.glb,
         ../renders/{front,side,three-quarter,photomatch}.png
Run: blender -b --python build_farnese_bull.py [-- final]
"""

import bpy
import math
import os
import random
import sys
from mathutils import Vector
from mathutils import noise as mnoise

random.seed(23)

OUT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FINAL = "final" in sys.argv
RES = 1000 if FINAL else 640

MODEL_OBJECTS = []

# ----------------------------------------------------------------- materials

def make_material(name, color, roughness):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat

MARBLE = None   # pale cast material (figures + bull)
ROCK_M = None   # rocky mount, slightly darker/warmer
EBON = None     # ebonised timber platform

# ----------------------------------------------------------------- helpers

def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

def register(obj, mat=None):
    if mat is not None:
        obj.data.materials.append(mat)
    MODEL_OBJECTS.append(obj)
    return obj

def loft(name, stations, segs=12, cap=True, mat=None):
    """Loft elliptical rings along a spine.
    stations: list of (centre Vector, half_width, half_height)."""
    n = len(stations)
    verts = []
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
            verts.append(v)
    faces = []
    for i in range(n - 1):
        for j in range(segs):
            a = i * segs + j
            b = i * segs + (j + 1) % segs
            c2 = (i + 1) * segs + (j + 1) % segs
            d = (i + 1) * segs + j
            faces.append((a, b, c2, d))
    if cap:
        c0 = stations[0][0]
        c1 = stations[-1][0]
        i0 = len(verts); verts.append(c0)
        i1 = len(verts); verts.append(c1)
        for j in range(segs):
            faces.append((i0, (j + 1) % segs, j))
            faces.append((i1, (n - 1) * segs + j, (n - 1) * segs + (j + 1) % segs))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([tuple(v) for v in verts], [], faces)
    mesh.update()
    for p in mesh.polygons:
        p.use_smooth = True
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return register(obj, mat)

def ball(name, centre, radii, detail=2, mat=None, noise_amt=0.0, noise_scale=2.0, smooth=True):
    """Ellipsoid built directly in world coordinates via bmesh."""
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=detail, radius=1.0)
    cx, cy, cz = centre
    rx, ry, rz = radii
    for v in bm.verts:
        p = Vector((v.co.x * rx, v.co.y * ry, v.co.z * rz))
        if noise_amt:
            n = mnoise.noise(Vector((p.x * noise_scale + cx, p.y * noise_scale + cy, p.z * noise_scale))) * 0.7 \
                + mnoise.noise(Vector((p.x * noise_scale * 2.7 + cx + 9.0, p.y * noise_scale * 2.7 + cy, p.z * noise_scale * 2.7))) * 0.3
            p += p.normalized() * n * noise_amt if p.length > 0 else p
        v.co = Vector((p.x + cx, p.y + cy, p.z + cz))
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    if smooth:
        for p in mesh.polygons:
            p.use_smooth = True
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return register(obj, mat)

def box(name, centre, size, mat=None, bevel=0.0):
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    sx, sy, sz = size
    for v in bm.verts:
        v.co = Vector((v.co.x * sx + centre[0], v.co.y * sy + centre[1], v.co.z * sz + centre[2]))
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if bevel:
        mod = obj.modifiers.new("bev", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    return register(obj, mat)

def limb(name, p1, p2, r1, r2, mat=None, segs=10):
    """Tapered segment between two points, joint sphere at p2 end optional."""
    p1 = Vector(p1); p2 = Vector(p2)
    mid = (p1 + p2) / 2
    stations = [(p1, r1, r1), (mid, (r1 + r2) / 2 * 1.05, (r1 + r2) / 2 * 1.05), (p2, r2, r2)]
    return loft(name, stations, segs=segs, mat=mat)

def joint(name, p, r, mat=None):
    return ball(name, p, (r, r, r), detail=1, mat=mat)

def join_objects(name, objs):
    """Join several registered objects into one; keeps it in MODEL_OBJECTS."""
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
        MODEL_OBJECTS.remove(o)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = name
    MODEL_OBJECTS.append(joined)
    return joined

V = Vector

# ----------------------------------------------------------------- scene setup

clear_scene()
MARBLE = make_material("CastMarble", (0.80, 0.78, 0.74), 0.85)
ROCK_M = make_material("RockCast", (0.60, 0.56, 0.50), 1.0)
EBON = make_material("EbonisedTimber", (0.07, 0.06, 0.055), 0.6)
DARK = make_material("HoofHorn", (0.42, 0.39, 0.35), 0.9)

# ----------------------------------------------------------------- platform
# Observed in the photograph: a dark, low, rectangular display platform
# with a stepped/moulded top edge; group bases in these courts were low
# and wide (see display-plinth NOTES). Benches and a protective railing
# visible around it in the photo are court furniture, NOT modelled.

plat = []
plat.append(box("PlatformBase", (0, 0, 0.17), (3.60, 3.10, 0.34), mat=EBON, bevel=0.015))
plat.append(box("PlatformCap", (0, 0, 0.385), (3.44, 2.94, 0.09), mat=EBON, bevel=0.012))
join_objects("Platform", plat)
PLAT_TOP = 0.43

# ----------------------------------------------------------------- rocky mount
# Observed: an irregular rocky mound fills most of the platform top; the
# bull stands on its crest. Blobs displaced with noise, merged.

rock = []
rock.append(ball("RockApron", (0, 0, PLAT_TOP + 0.02), (1.50, 1.24, 0.16), detail=2, mat=ROCK_M, noise_amt=0.09, noise_scale=2.6))
rock.append(ball("RockChest", (-0.25, -0.35, PLAT_TOP + 0.80), (0.50, 0.45, 0.50), detail=2, mat=ROCK_M, noise_amt=0.07, noise_scale=2.4))
# angular crag shards embedded at the mount's edges to break the smoothness
for i, (cx, cy, cz, s) in enumerate([
        (0.30, -0.95, 0.72, 0.30), (-0.95, -0.30, 0.82, 0.26), (1.05, 0.15, 0.78, 0.28),
        (-0.35, 0.85, 0.92, 0.24), (0.55, 0.88, 0.98, 0.26), (-1.05, 0.35, 0.80, 0.22)]):
    rock.append(ball(f"RockCrag{i}", (cx, cy, cz), (s, s * 0.8, s * 0.66), detail=0, mat=ROCK_M, smooth=False))
rock.append(ball("RockMain", (0.15, 0.15, PLAT_TOP + 0.30), (1.15, 0.95, 0.42), detail=2, mat=ROCK_M, noise_amt=0.06, noise_scale=2.2))
rock.append(ball("RockCrest", (0.72, 0.52, PLAT_TOP + 0.62), (0.80, 0.64, 0.46), detail=2, mat=ROCK_M, noise_amt=0.075, noise_scale=2.4))
rock.append(ball("RockSaddle", (-0.10, -0.02, PLAT_TOP + 0.95), (0.62, 0.55, 0.55), detail=2, mat=ROCK_M, noise_amt=0.07, noise_scale=2.4))
rock.append(ball("RockFrontL", (-0.62, -0.55, PLAT_TOP + 0.22), (0.82, 0.66, 0.34), detail=2, mat=ROCK_M, noise_amt=0.06, noise_scale=2.4))
rock.append(ball("RockFrontR", (0.82, -0.50, PLAT_TOP + 0.18), (0.72, 0.60, 0.32), detail=2, mat=ROCK_M, noise_amt=0.06, noise_scale=2.4))
rock.append(ball("RockRearL", (-0.72, 0.50, PLAT_TOP + 0.36), (0.72, 0.56, 0.38), detail=2, mat=ROCK_M, noise_amt=0.05, noise_scale=2.4))
join_objects("RockyMount", rock)

# ----------------------------------------------------------------- the bull
# Rearing on the crest: hind hooves planted rear-right, body rising
# diagonally to the front-left, head high, forelegs raised. Arrangement
# from the canonical type; the photograph confirms the rearing diagonal
# and the raised forelegs.
bull = []
spine = [
    (V((0.62, 0.42, 2.02)), 0.27, 0.36),   # pelvis
    (V((0.30, 0.22, 2.28)), 0.30, 0.40),   # mid-back
    (V((-0.05, 0.00, 2.52)), 0.31, 0.46),  # shoulder hump
    (V((-0.32, -0.18, 2.64)), 0.22, 0.30), # neck base
    (V((-0.47, -0.29, 2.88)), 0.165, 0.20),# head joint
]
bull.append(loft("BullBody", spine, segs=14, mat=MARBLE))
# rump and hanging chest/belly masses so the body sits onto the rock
bull.append(ball("BullRump", (0.60, 0.40, 2.04), (0.28, 0.30, 0.34), detail=2, mat=MARBLE))
bull.append(ball("BullBelly", (-0.12, -0.04, 2.08), (0.27, 0.25, 0.31), detail=2, mat=MARBLE))
bull.append(ball("HaunchA", (0.72, 0.26, 1.88), (0.16, 0.15, 0.20), detail=1, mat=MARBLE))
bull.append(ball("HaunchB", (0.52, 0.60, 1.88), (0.16, 0.15, 0.20), detail=1, mat=MARBLE))
# head: short loft thrusting forward and down, muzzle blunt
bull.append(loft("BullHead", [
    (V((-0.47, -0.29, 2.88)), 0.155, 0.19),
    (V((-0.58, -0.40, 2.94)), 0.135, 0.15),
    (V((-0.68, -0.50, 2.90)), 0.105, 0.11),
], segs=12, mat=MARBLE))
# horns: curved tapered lofts sweeping up and wide from the head
for sgn, nm in ((1, "HornR"), (-1, "HornL")):
    lat = V((0.83, -0.55, 0)) * sgn  # lateral unit in plan
    base = V((-0.53, -0.36, 2.97)) + lat * 0.14
    bull.append(loft(nm, [
        (base, 0.040, 0.040),
        (base + lat * 0.17 + V((0, 0, 0.17)), 0.029, 0.029),
        (base + lat * 0.30 + V((-0.03, -0.08, 0.36)), 0.010, 0.010),
    ], segs=8, mat=DARK))
# ears
for sgn in (1, -1):
    lat = V((0.55, -0.84, 0)) * 0.20 * sgn
    p = V((-0.46, -0.28, 2.82)) + lat
    bull.append(ball(f"Ear{sgn}", tuple(p), (0.075, 0.045, 0.05), detail=1, mat=MARBLE))
# hind legs: braced on the crest, hip -> hock -> hoof
bull.append(limb("HindLegA1", (0.72, 0.26, 1.92), (0.94, 0.18, 1.56), 0.115, 0.075, mat=MARBLE))
bull.append(limb("HindLegA2", (0.94, 0.18, 1.56), (0.88, 0.22, 1.44), 0.070, 0.055, mat=MARBLE))
bull.append(box("HoofA", (0.88, 0.22, 1.42), (0.11, 0.11, 0.07), mat=DARK))
bull.append(limb("HindLegB1", (0.52, 0.60, 1.92), (0.66, 0.84, 1.58), 0.115, 0.075, mat=MARBLE))
bull.append(limb("HindLegB2", (0.66, 0.84, 1.58), (0.72, 0.74, 1.46), 0.070, 0.055, mat=MARBLE))
bull.append(box("HoofB", (0.72, 0.74, 1.44), (0.11, 0.11, 0.07), mat=DARK))
# forelegs: raised. A reaches down-forward (gripped by Zethus); B folds high.
bull.append(limb("ForeLegA1", (-0.28, -0.20, 2.38), (-0.56, -0.44, 2.52), 0.095, 0.065, mat=MARBLE))
bull.append(limb("ForeLegA2", (-0.56, -0.44, 2.52), (-0.79, -0.56, 2.16), 0.060, 0.048, mat=MARBLE))
bull.append(box("HoofFA", (-0.80, -0.57, 2.12), (0.10, 0.10, 0.09), mat=DARK))
bull.append(limb("ForeLegB1", (-0.14, 0.16, 2.36), (-0.36, 0.30, 2.66), 0.095, 0.065, mat=MARBLE))
bull.append(limb("ForeLegB2", (-0.36, 0.30, 2.66), (-0.54, 0.10, 3.00), 0.060, 0.048, mat=MARBLE))
bull.append(box("HoofFB", (-0.55, 0.08, 3.04), (0.10, 0.10, 0.09), mat=DARK))
# tail: thin curve down the rear with a tuft
bull.append(loft("Tail", [
    (V((0.80, 0.50, 2.06)), 0.045, 0.045),
    (V((0.98, 0.64, 1.66)), 0.032, 0.032),
    (V((0.94, 0.62, 1.30)), 0.026, 0.026),
], segs=8, mat=MARBLE))
bull.append(ball("TailTuft", (0.94, 0.62, 1.18), (0.055, 0.055, 0.10), detail=1, mat=DARK))
join_objects("Bull", bull)

# ----------------------------------------------------------------- figure kit
# Stylised standing/kneeling figure masses. All poses and arrangements
# follow the canonical composition of the antique type (convention).

def figure(name, pelvis, chest, head, arms, legs, skirt=None, sash=None, bun=False):
    """arms/legs: lists of (p_shoulder_or_hip, p_mid, p_end, r1, r2)."""
    parts = []
    parts.append(loft(name + "Torso", [
        (V(pelvis), 0.155, 0.115),
        (V(((pelvis[0] + chest[0]) / 2, (pelvis[1] + chest[1]) / 2, (pelvis[2] + chest[2]) / 2)), 0.165, 0.125),
        (V(chest), 0.19, 0.13),
    ], segs=12, mat=MARBLE))
    neck = V(((chest[0] + head[0]) / 2, (chest[1] + head[1]) / 2, (chest[2] + head[2]) / 2 - 0.03))
    parts.append(limb(name + "Neck", tuple(V(chest) + V((0, 0, 0.02))), tuple(neck), 0.055, 0.05, mat=MARBLE))
    parts.append(ball(name + "Head", head, (0.095, 0.105, 0.125), detail=2, mat=MARBLE))
    if bun:
        back = V(head) + V((0, 0.10, 0.03))
        parts.append(ball(name + "Hair", tuple(back), (0.085, 0.09, 0.10), detail=1, mat=MARBLE))
    for i, (a, b, c, r1, r2) in enumerate(arms):
        parts.append(limb(f"{name}Arm{i}a", a, b, r1, (r1 + r2) / 2, mat=MARBLE))
        parts.append(limb(f"{name}Arm{i}b", b, c, (r1 + r2) / 2, r2, mat=MARBLE))
        parts.append(joint(f"{name}Elb{i}", b, r1 * 0.92, mat=MARBLE))
    for i, (a, b, c, r1, r2) in enumerate(legs):
        parts.append(limb(f"{name}Leg{i}a", a, b, r1, (r1 + r2) / 2, mat=MARBLE))
        parts.append(limb(f"{name}Leg{i}b", b, c, (r1 + r2) / 2, r2, mat=MARBLE))
        parts.append(joint(f"{name}Knee{i}", b, r1 * 0.9, mat=MARBLE))
    if skirt is not None:
        top, hem, r_top, r_hem, z_hem = skirt
        parts.append(loft(name + "Skirt", [
            (V((top[0], top[1], z_hem)), r_hem, r_hem * 0.88),
            (V((top[0], top[1], (top[2] + z_hem) / 2)), (r_top + r_hem) / 2, (r_top + r_hem) / 2 * 0.9),
            (V(top), r_top, r_top * 0.9),
        ], segs=12, mat=MARBLE))
    if sash is not None:
        p1, p2 = sash
        parts.append(ball(name + "Sash", tuple((V(p1) + V(p2)) / 2), (0.20, 0.10, 0.30), detail=1, mat=MARBLE))
    return join_objects(name, parts)

# Zethus — front-left, leaning back, both hands up gripping the bull's
# lowered foreleg (canonical position for the hunter brother).
figure("Zethus",
       pelvis=(-0.98, -0.50, 1.55), chest=(-1.02, -0.44, 2.00), head=(-1.07, -0.42, 2.29),
       arms=[
           ((-1.13, -0.53, 1.97), (-0.96, -0.63, 2.14), (-0.81, -0.57, 2.15), 0.055, 0.042),
           ((-0.91, -0.35, 1.97), (-0.83, -0.45, 2.10), (-0.77, -0.53, 2.13), 0.055, 0.042),
       ],
       legs=[
           ((-1.07, -0.57, 1.52), (-1.19, -0.73, 1.10), (-1.13, -0.81, 0.76), 0.075, 0.05),
           ((-0.89, -0.43, 1.52), (-0.81, -0.37, 1.08), (-0.87, -0.29, 0.82), 0.075, 0.05),
       ])

# Amphion — front-right, lunging in; one arm up to the bull's jaw, the
# other pulling Dirce by the hair (canonical).
figure("Amphion",
       pelvis=(0.78, -0.52, 1.52), chest=(0.72, -0.47, 1.99), head=(0.68, -0.44, 2.27),
       arms=[
           ((0.62, -0.40, 1.98), (0.24, -0.38, 2.30), (-0.28, -0.35, 2.56), 0.055, 0.042),
           ((0.88, -0.55, 1.97), (0.62, -0.73, 1.90), (0.35, -0.85, 1.79), 0.052, 0.040),
       ],
       legs=[
           ((0.69, -0.60, 1.50), (0.54, -0.79, 1.05), (0.61, -0.89, 0.72), 0.075, 0.05),
           ((0.88, -0.43, 1.52), (1.06, -0.29, 1.10), (1.13, -0.21, 0.80), 0.075, 0.05),
       ])

# Dirce — front-centre foreground, kneeling on the rock slope, torso
# twisted up, one arm raised pleading; hair swept toward Amphion's hand.
figure("Dirce",
       pelvis=(0.08, -0.95, 1.06), chest=(0.02, -0.90, 1.50), head=(0.00, -0.87, 1.79),
       arms=[
           ((-0.09, -0.99, 1.47), (-0.21, -1.06, 1.74), (-0.27, -1.00, 2.01), 0.047, 0.037),
           ((0.13, -0.83, 1.47), (0.22, -0.80, 1.30), (0.26, -0.88, 1.14), 0.047, 0.037),
       ],
       legs=[],
       skirt=((0.08, -0.95, 1.10), None, 0.17, 0.27, 0.60),
       bun=True)
# hair-pull mass from Dirce's head toward Amphion's gripping hand
hair = loft("DirceHair", [
    (V((0.05, -0.80, 1.82)), 0.055, 0.06),
    (V((0.20, -0.83, 1.82)), 0.038, 0.042),
    (V((0.34, -0.85, 1.80)), 0.024, 0.026),
], segs=8, mat=MARBLE)

# Antiope — rear-left, standing tall in heavy drapery on the high rock,
# holding a thyrsus staff. Her draped back is one of the few forms the
# photograph actually resolves.
figure("Antiope",
       pelvis=(-1.04, 0.60, 2.00), chest=(-1.02, 0.58, 2.36), head=(-1.01, 0.57, 2.65),
       arms=[
           ((-0.92, 0.52, 2.35), (-0.82, 0.44, 2.14), (-0.70, 0.38, 2.06), 0.048, 0.038),
           ((-1.16, 0.64, 2.35), (-1.10, 0.56, 2.14), (-0.96, 0.54, 2.02), 0.048, 0.038),
       ],
       legs=[],
       skirt=((-1.04, 0.60, 2.04), None, 0.185, 0.315, 1.08),
       sash=((-1.16, 0.50, 2.22), (-0.90, 0.68, 1.96)),
       bun=True)
# thyrsus staff in Antiope's right hand
staff = []
staff.append(limb("ThyrsusShaft", (-0.70, 0.38, 1.14), (-0.67, 0.37, 2.66), 0.016, 0.013, mat=DARK))
staff.append(ball("ThyrsusTop", (-0.67, 0.37, 2.74), (0.05, 0.05, 0.09), detail=1, mat=DARK))
join_objects("Thyrsus", staff)

# ------------------------------------------------------- base small figures
small = []
# Child A — crouching at the front-right base with a small goat
small.append(ball("ChildABody", (1.02, -0.74, 0.86), (0.13, 0.11, 0.17), detail=1, mat=MARBLE))
small.append(ball("ChildAHead", (0.97, -0.70, 1.16), (0.075, 0.08, 0.095), detail=1, mat=MARBLE))
small.append(limb("ChildAArm", (0.95, -0.80, 0.95), (1.14, -0.86, 0.72), 0.035, 0.028, mat=MARBLE))
small.append(ball("GoatBody", (1.30, -0.88, 0.66), (0.17, 0.11, 0.115), detail=1, mat=MARBLE))
small.append(ball("GoatHead", (1.44, -0.93, 0.76), (0.07, 0.055, 0.07), detail=1, mat=MARBLE))
# Child B — seated at the rear-right base, arm raised
small.append(ball("ChildBBody", (1.06, 0.32, 0.80), (0.12, 0.105, 0.16), detail=1, mat=MARBLE))
small.append(ball("ChildBHead", (1.04, 0.30, 1.10), (0.072, 0.078, 0.092), detail=1, mat=MARBLE))
small.append(limb("ChildBArm", (1.12, 0.26, 0.92), (1.24, 0.18, 1.14), 0.033, 0.026, mat=MARBLE))
# Dog — seated front-left base, head up toward the bull (Zethus's dog)
small.append(ball("DogHaunch", (-1.20, -0.08, 0.62), (0.15, 0.13, 0.15), detail=1, mat=MARBLE))
small.append(limb("DogChest", (-1.20, -0.14, 0.66), (-1.22, -0.20, 0.92), 0.085, 0.07, mat=MARBLE))
small.append(ball("DogHead", (-1.23, -0.22, 1.04), (0.075, 0.095, 0.08), detail=1, mat=MARBLE))
small.append(loft("DogTail", [
    (V((-1.10, 0.04, 0.52)), 0.026, 0.026),
    (V((-0.98, 0.10, 0.50)), 0.02, 0.02),
    (V((-0.94, 0.06, 0.58)), 0.014, 0.014),
], segs=8, mat=MARBLE))
# Cista (sacrificial basket) — front-centre at the rock's foot
small.append(loft("Cista", [
    (V((0.42, -1.10, 0.52)), 0.125, 0.125),
    (V((0.42, -1.10, 0.68)), 0.15, 0.15),
    (V((0.42, -1.10, 0.80)), 0.155, 0.155),
], segs=12, mat=MARBLE))
small.append(ball("CistaLid", (0.50, -1.04, 0.86), (0.14, 0.14, 0.03), detail=1, mat=MARBLE))
join_objects("BaseFigures", small)

# ----------------------------------------------------------------- finish
# origin at base centre, floor at z=0, scale applied (all geometry was
# built in world coordinates; transforms are identity).
bpy.ops.object.select_all(action="DESELECT")
for o in MODEL_OBJECTS:
    o.select_set(True)
bpy.context.view_layer.objects.active = MODEL_OBJECTS[0]
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

tris = 0
xs, ys, zs = [], [], []
for o in MODEL_OBJECTS:
    if o.type != "MESH":
        continue
    tris += sum(len(p.vertices) - 2 for p in o.data.polygons)
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        xs.append(w.x); ys.append(w.y); zs.append(w.z)
print(f"[bull] objects: {[o.name for o in MODEL_OBJECTS]}")
print(f"[bull] triangles: {tris}")
print(f"[bull] bbox X {min(xs):.3f}..{max(xs):.3f} ({max(xs)-min(xs):.3f} m)")
print(f"[bull] bbox Y {min(ys):.3f}..{max(ys):.3f} ({max(ys)-min(ys):.3f} m)")
print(f"[bull] bbox Z {min(zs):.3f}..{max(zs):.3f} ({max(zs)-min(zs):.3f} m)")

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, "farnese-bull.blend"))
bpy.ops.export_scene.gltf(
    filepath=os.path.join(OUT_DIR, "farnese-bull.glb"),
    export_format="GLB", use_selection=True, export_apply=True)
print("[bull] blend + glb saved")

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

TARGET = Vector((0, 0, 1.78))

def add_area(name, loc, size, energy):
    data = bpy.data.lights.new(name, "AREA")
    data.shape = "RECTANGLE"
    data.size = size[0]
    data.size_y = size[1]
    data.energy = energy
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = (TARGET - Vector(loc)).to_track_quat("-Z", "Y").to_euler()

add_area("Key", (4.6, -6.2, 7.4), (6.5, 4.5), 1150)
add_area("Fill", (-6.4, -3.4, 2.8), (5.5, 4.0), 380)
add_area("Rim", (-1.2, 6.0, 5.4), (5.5, 3.5), 750)

cam_data = bpy.data.cameras.new("Camera")
cam_data.lens = 50
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam

VIEWS = {
    "front": Vector((0.10, -9.8, 2.15)),          # canonical display front
    "side": Vector((9.8, 0.15, 2.15)),            # down the group's long axis
    "three-quarter": Vector((6.0, -7.5, 4.1)),
    "photomatch": Vector((-5.4, 6.6, 5.6)),      # approx. the album photo's rear-left elevated viewpoint
}
os.makedirs(os.path.join(OUT_DIR, "renders"), exist_ok=True)
for name, pos in VIEWS.items():
    cam.location = pos
    tgt = Vector((0.0, 0, 1.45)) if name == "photomatch" else TARGET
    cam.rotation_euler = (tgt - pos).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(OUT_DIR, "renders", f"{name}.png")
    bpy.ops.render.render(write_still=True)
    print(f"[bull] rendered {name}")

print("[bull] done")
