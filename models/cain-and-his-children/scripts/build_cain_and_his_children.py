"""
Cain and his Children — Antoine Etex (Sydenham sculpture gallery),
procedural Blender 4.2 build.

Frontal-composition-first construction from the Rijksmuseum stereograph
RP-F-2012-96-336 (CC0): the ONLY view of the group in the collection.
Masses are chained ellipsoids/lofts posed to track the photograph's
frontal composition and silhouette, then joined and voxel-remeshed per
figure. Depth and backs are sculptural inference (see ../NOTES.md).

Outputs: ../cain-and-his-children.blend, ../cain-and-his-children.glb,
         ../renders/{front,side,three-quarter,photomatch}.png
Run: blender -b --python build_cain_and_his_children.py [-- final]
"""

import bpy
import math
import os
import random
import sys
from mathutils import Vector, Matrix, noise as mnoise

random.seed(23)

OUT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FINAL = "final" in sys.argv
RES = 1000 if FINAL else 640
VOXEL = 0.026

# ----------------------------------------------------------------- materials

def make_material(name, color, roughness):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat

MARBLE = None
ROCK_M = None
EBON = None
PELT_M = None
PLATE_M = None

# ----------------------------------------------------------------- helpers

def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

def loft(name, stations, segs=16, cap=True, smooth=True):
    """Loft elliptical rings along a spine (house helper, after the
    Una build). stations: (centre Vector, half_w, half_h)."""
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

def ball(name, loc, scale, mat=None, seg=20, rings=14, disp=0.0, freq=3.0,
         seed=0.0):
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
        me.update()
    if mat is not None:
        obj.data.materials.append(mat)
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj

def limb(name, a, b, r0, r1, mat=None, knee=None, knee_r=0.0):
    """Tapered limb between two points, optional joint ball."""
    a, b = Vector(a), Vector(b)
    mid = (a + b) * 0.5
    stations = [(a, r0, r0),
                (a.lerp(b, 0.35), r0 * 0.92 + r1 * 0.08, r0 * 0.92 + r1 * 0.08),
                (a.lerp(b, 0.7), r0 * 0.55 + r1 * 0.45, r0 * 0.55 + r1 * 0.45),
                (b, r1, r1)]
    parts = [loft(name, stations, segs=14)]
    if knee is not None:
        parts.append(ball(name + "Joint", tuple(knee),
                          (knee_r, knee_r, knee_r), mat=mat))
    if mat is not None:
        parts[0].data.materials.append(mat)
    return parts

def unify(objs, name, voxel=VOXEL):
    """Join part objects into one, voxel-remesh for a carved read."""
    objs = [o for o in objs if o is not None]
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active
    o.name = name
    o.data.remesh_voxel_size = voxel
    o.data.remesh_voxel_adaptivity = 0.0
    bpy.ops.object.voxel_remesh()
    for p in o.data.polygons:
        p.use_smooth = True
    return o

MODEL_OBJECTS = []
def reg(o):
    MODEL_OBJECTS.append(o)
    return o

# =================================================================
clear_scene()
MARBLE = make_material("CastMarble", (0.905, 0.885, 0.845), 0.52)
ROCK_M = make_material("RockBase", (0.375, 0.35, 0.315), 0.95)
EBON = make_material("EbonisedBase", (0.055, 0.05, 0.045), 0.55)
PELT_M = make_material("AnimalPelt", (0.36, 0.29, 0.215), 0.98)
PLATE_M = make_material("LabelPlate", (0.16, 0.15, 0.14), 0.6)

V = Vector

# ----------------------------------------------------------------- display base
# Low, wide ebonised group base (plinth-family variant documented in
# models/display-plinth/NOTES.md: group bases are lower and wider, with a
# sloped shoulder and a small label low on the front). Lofted rectangle
# profile: bottom slab, step-in, sloped shoulder, top.
def box_loft(name, profile, mat):
    """profile: list of (z, half_w, half_d) — rectangular loft."""
    verts, faces = [], []
    n = len(profile)
    for z, hw, hd in profile:
        for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            verts.append((sx * hw, sy * hd, z))
    for i in range(n - 1):
        for j in range(4):
            a = i * 4 + j
            b = i * 4 + (j + 1) % 4
            c2 = (i + 1) * 4 + (j + 1) % 4
            d = (i + 1) * 4 + j
            faces.append((a, b, c2, d))
    # top cap + bottom cap
    ci = len(verts); verts.append((0, 0, profile[-1][0]))
    base = (n - 1) * 4
    for j in range(4):
        faces.append((ci, base + j, base + (j + 1) % 4))
    ci = len(verts); verts.append((0, 0, profile[0][0]))
    for j in range(4):
        faces.append((ci, (j + 1) % 4, j))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj

reg(box_loft("DisplayBase", [
    (0.000, 1.060, 0.680),
    (0.035, 1.060, 0.680),
    (0.050, 1.015, 0.645),
    (0.120, 0.965, 0.600),   # sloped shoulder
    (0.160, 0.955, 0.590),
], EBON))
# small unlettered label plate, low on the front face
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.663, 0.082))
plate = bpy.context.view_layer.objects.active
plate.name = "LabelPlate"
plate.scale = (0.36, 0.016, 0.105)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
plate.data.materials.append(PLATE_M)
reg(plate)

# ----------------------------------------------------------------- rock mound
# The group's integral rocky base: a craggy mass of overlapping,
# noise-displaced forms joined and remeshed — sloped shoulders, a higher
# shelf at the back where Cain sits, feet shelves at the front.
rock_parts = []
for i, (loc, sc) in enumerate([
        ((0.00, 0.02, 0.335), (1.00, 0.62, 0.215)),
        ((-0.45, -0.28, 0.275), (0.54, 0.36, 0.155)),
        ((0.45, -0.28, 0.275), (0.54, 0.36, 0.155)),
        ((0.00, 0.30, 0.42), (0.82, 0.36, 0.22)),
        ((0.00, 0.06, 0.50), (0.72, 0.47, 0.125)),
        ((-0.68, 0.12, 0.33), (0.30, 0.34, 0.185)),
        ((0.68, 0.12, 0.33), (0.30, 0.34, 0.185)),
        ((-0.25, -0.45, 0.235), (0.34, 0.18, 0.095)),
        ((0.25, -0.45, 0.235), (0.34, 0.18, 0.095)),
        ((-0.66, -0.10, 0.395), (0.26, 0.30, 0.125))]):  # boy's standing shelf
    rock_parts.append(ball(f"RockMass{i}", loc, sc, mat=ROCK_M, seg=22,
                           rings=16, disp=0.034, freq=3.4, seed=i * 2.1))
rock = unify(rock_parts, "RockMound", voxel=0.030)
# second crag pass: displace along normals so the top breaks up too
rock.data.update()
for v in rock.data.vertices:
    n = mnoise.noise(Vector((v.co.x * 4.5 + 3.0, v.co.y * 4.5, v.co.z * 4.5)))
    n2 = mnoise.noise(Vector((v.co.x * 15.0, v.co.y * 15.0 + 5.0, v.co.z * 15.0)))
    v.co += v.normal * (n * 0.030 + n2 * 0.009)
rock.data.update()
reg(rock)

MOUND_TOP_REAR = 0.66   # Cain's seat shelf
MOUND_TOP_FRONT = 0.33  # where the feet rest

# =================================================================
# CAIN — seated centre-back, head bowed, both shins hanging in front.
cain = []
# pelvis + torso: loft hunched well forward
cain.append(loft("CainTorso", [
    (V((0.00, 0.17, 0.70)), 0.235, 0.175),
    (V((0.00, 0.155, 0.92)), 0.285, 0.195),
    (V((-0.01, 0.11, 1.14)), 0.315, 0.205),
    (V((-0.015, 0.05, 1.32)), 0.30, 0.185),
    (V((-0.02, -0.01, 1.42)), 0.225, 0.15),
], segs=20))
cain[-1].data.materials.append(MARBLE)
# chest/abdomen fill
cain.append(ball("CainBelly", (0.0, 0.10, 1.02), (0.26, 0.20, 0.26), mat=MARBLE))
cain.append(ball("CainPecL", (-0.14, 0.0, 1.235), (0.155, 0.13, 0.14), mat=MARBLE))
cain.append(ball("CainPecR", (0.13, 0.0, 1.235), (0.155, 0.13, 0.14), mat=MARBLE))
# hunched shoulder/back mass swallowing the neck
cain.append(ball("CainHunch", (-0.01, 0.085, 1.395), (0.295, 0.185, 0.135), mat=MARBLE))
# head bowed deep: skull sunk forward between the shoulders
cain.append(ball("CainHead", (-0.02, -0.10, 1.465), (0.105, 0.115, 0.125), mat=MARBLE))
cain.append(ball("CainBeard", (-0.02, -0.155, 1.375), (0.095, 0.08, 0.10),
                 mat=MARBLE, disp=0.012, freq=10.0, seed=4.0))
# neck/shoulder mass
cain.append(ball("CainTraps", (-0.01, 0.045, 1.375), (0.24, 0.16, 0.11), mat=MARBLE))
# --- Cain's right leg (viewer's left): thigh forward, shin vertical
cain += limb("CainRThigh", ( -0.15, 0.13, 0.74), (-0.24, -0.30, 0.96),
             0.105, 0.10, mat=MARBLE)
cain.append(ball("CainRKnee", (-0.24, -0.325, 0.965), (0.105, 0.105, 0.11), mat=MARBLE))
cain += limb("CainRShin", (-0.24, -0.335, 0.925), (-0.23, -0.45, 0.425),
             0.085, 0.052, mat=MARBLE)
cain.append(ball("CainRCalf", (-0.235, -0.365, 0.70), (0.075, 0.075, 0.14), mat=MARBLE))
cain.append(ball("CainRFoot", (-0.23, -0.485, 0.345), (0.075, 0.135, 0.045), mat=MARBLE))
cain.append(ball("CainRToes", (-0.23, -0.55, 0.315), (0.07, 0.05, 0.035), mat=MARBLE))
# --- Cain's left leg (viewer's right of centre)
cain += limb("CainLThigh", (0.15, 0.13, 0.74), (0.14, -0.26, 0.92),
             0.10, 0.095, mat=MARBLE)
cain.append(ball("CainLKnee", (0.14, -0.28, 0.925), (0.10, 0.10, 0.105), mat=MARBLE))
cain += limb("CainLShin", (0.14, -0.29, 0.885), (0.16, -0.42, 0.41),
             0.08, 0.05, mat=MARBLE)
cain.append(ball("CainLCalf", (0.15, -0.325, 0.67), (0.07, 0.07, 0.13), mat=MARBLE))
cain.append(ball("CainLFoot", (0.16, -0.455, 0.325), (0.072, 0.13, 0.043), mat=MARBLE))
cain.append(ball("CainLToes", (0.16, -0.515, 0.30), (0.067, 0.048, 0.033), mat=MARBLE))
# --- Cain's right arm: down behind the boy, hand to his own right knee
cain += limb("CainRUpperArm", (-0.285, 0.03, 1.30), (-0.375, -0.05, 1.02),
             0.088, 0.068, mat=MARBLE)
cain += limb("CainRForearm", (-0.375, -0.05, 1.02), (-0.26, -0.27, 0.945),
             0.06, 0.047, mat=MARBLE)
cain.append(ball("CainRHand", (-0.25, -0.295, 0.95), (0.055, 0.075, 0.04), mat=MARBLE))
# --- Cain's left arm: reaches down to clasp the right figure's hand
cain += limb("CainLUpperArm", (0.29, 0.03, 1.30), (0.45, -0.10, 1.02),
             0.09, 0.068, mat=MARBLE)
cain += limb("CainLForearm", (0.45, -0.10, 1.02), (0.515, -0.13, 0.875),
             0.058, 0.045, mat=MARBLE)
cain.append(ball("CainLHand", (0.52, -0.145, 0.865), (0.052, 0.07, 0.038), mat=MARBLE))
reg(unify(cain, "Cain"))
# Cain's shaggy hair, kept OUT of the remesh so its surface survives
reg(ball("CainHair", (-0.02, -0.085, 1.505), (0.128, 0.132, 0.118),
         mat=MARBLE, disp=0.020, freq=8.0, seed=2.0))

# --- the animal pelt hanging between Cain's knees
pelt = []
pelt.append(loft("PeltHang", [
    (V((-0.09, -0.10, 0.86)), 0.14, 0.082),
    (V((-0.08, -0.21, 0.64)), 0.155, 0.075),
    (V((-0.07, -0.265, 0.46)), 0.138, 0.062),
    (V((-0.06, -0.29, 0.385)), 0.105, 0.048),
], segs=14))
pelt[-1].data.materials.append(PELT_M)
for v in pelt[0].data.vertices:
    n = mnoise.noise(Vector((v.co.x * 14.0, v.co.y * 14.0, v.co.z * 14.0)))
    v.co.z += n * 0.012
    v.co.x += n * 0.008
pelt[0].data.update()
pelt.append(ball("PeltHead", (-0.12, -0.13, 0.865), (0.088, 0.10, 0.06),
                 mat=PELT_M, disp=0.014, freq=11.0, seed=7.0))
pelt.append(ball("PeltSpill", (-0.03, -0.38, 0.30), (0.115, 0.09, 0.035),
                 mat=PELT_M, disp=0.012, freq=11.0, seed=9.0))
reg(unify(pelt, "Pelt", voxel=0.020))

# =================================================================
# STANDING BOY — at Cain's right (viewer's left), head up toward Cain,
# near hand resting on Cain's right knee.
boy = []
boy.append(loft("BoyTorso", [
    (V((-0.615, -0.03, 0.94)), 0.105, 0.085),
    (V((-0.60, -0.015, 1.10)), 0.115, 0.09),
    (V((-0.575, 0.0, 1.25)), 0.105, 0.082),
    (V((-0.55, 0.005, 1.32)), 0.075, 0.06),
], segs=16))
boy[-1].data.materials.append(MARBLE)
boy.append(ball("BoyHead", (-0.52, -0.02, 1.44), (0.082, 0.088, 0.098), mat=MARBLE))
# standing leg (near): slight knee bend, contrapposto
boy += limb("BoyThighNear", (-0.64, -0.05, 0.94), (-0.665, -0.10, 0.72),
            0.058, 0.046, mat=MARBLE)
boy += limb("BoyShinNear", (-0.665, -0.10, 0.72), (-0.66, -0.12, 0.545),
            0.042, 0.032, mat=MARBLE)
boy.append(ball("BoyFootNear", (-0.665, -0.185, 0.52), (0.045, 0.085, 0.028), mat=MARBLE))
# trailing leg crossing behind toward the centre
boy += limb("BoyLegFar", (-0.565, 0.03, 0.94), (-0.475, -0.10, 0.70),
            0.055, 0.042, mat=MARBLE,
            knee=(-0.475, -0.10, 0.70), knee_r=0.05)
boy += limb("BoyShinFar", (-0.475, -0.10, 0.70), (-0.315, -0.28, 0.375),
            0.04, 0.028, mat=MARBLE)
boy.append(ball("BoyFootFar", (-0.30, -0.335, 0.355), (0.04, 0.075, 0.025), mat=MARBLE))
# near arm: bent, hand on Cain's knee
boy += limb("BoyArmNear", (-0.52, -0.03, 1.25), (-0.42, -0.16, 1.02),
            0.045, 0.036, mat=MARBLE)
boy += limb("BoyForearmNear", (-0.42, -0.16, 1.02), (-0.25, -0.295, 0.955),
            0.034, 0.027, mat=MARBLE)
boy.append(ball("BoyHandNear", (-0.24, -0.30, 0.95), (0.038, 0.055, 0.026), mat=MARBLE))
# far arm hanging at his side
boy += limb("BoyArmFar", (-0.665, 0.03, 1.25), (-0.70, 0.0, 0.95),
            0.042, 0.027, mat=MARBLE)
boy.append(ball("BoyHandFar", (-0.70, 0.0, 0.925), (0.032, 0.045, 0.024), mat=MARBLE))
reg(unify(boy, "StandingBoy"))
# the boy's shoulder-length wavy hair, un-remeshed so it keeps its surface
reg(ball("BoyHair", (-0.535, 0.0, 1.47), (0.096, 0.098, 0.095),
         mat=MARBLE, disp=0.013, freq=10.0, seed=3.0))
reg(ball("BoyHairFall", (-0.548, 0.045, 1.395), (0.086, 0.07, 0.09),
         mat=MARBLE, disp=0.011, freq=10.0, seed=3.7))

# =================================================================
# CENTRAL CHILD — crouched in front of Cain between his knees, head
# bowed, mostly behind the pelt and Cain's left shin.
child = []
child.append(ball("ChildBack", (0.0, -0.17, 0.66), (0.135, 0.12, 0.16), mat=MARBLE))
child.append(ball("ChildHip", (0.0, -0.13, 0.50), (0.115, 0.11, 0.09), mat=MARBLE))
child.append(ball("ChildFace", (0.03, -0.375, 0.79), (0.068, 0.06, 0.065), mat=MARBLE))
# one small leg folded, foot planted at the mound's front edge
child += limb("ChildLeg", (0.07, -0.22, 0.50), (0.105, -0.36, 0.315),
              0.045, 0.03, mat=MARBLE)
child.append(ball("ChildFoot", (0.11, -0.40, 0.30), (0.04, 0.07, 0.024), mat=MARBLE))
# small arm reaching down the mound front
child += limb("ChildArm", (0.10, -0.26, 0.66), (0.155, -0.375, 0.42),
              0.032, 0.022, mat=MARBLE)
reg(unify(child, "CentralChild"))
# the child's big curly head, un-remeshed so the curls survive
reg(ball("ChildHead", (0.03, -0.335, 0.875), (0.102, 0.102, 0.107),
         mat=MARBLE, disp=0.020, freq=11.0, seed=5.0))

# =================================================================
# RIGHT FIGURE — the largest child, crouched at Cain's left with its
# back to the viewer; one leg extended along the mound, one arm raised
# to Cain's clasping hand; the infant sheltered against its side.
wife = []
wife.append(ball("RightBack", (0.575, 0.05, 0.715), (0.185, 0.16, 0.205), mat=MARBLE))
wife.append(ball("RightHip", (0.62, -0.03, 0.52), (0.16, 0.145, 0.115), mat=MARBLE))
wife.append(ball("RightShoulder", (0.495, 0.0, 0.865), (0.115, 0.105, 0.10), mat=MARBLE))
wife.append(ball("RightHead", (0.45, -0.15, 0.785), (0.088, 0.09, 0.098),
                 mat=MARBLE, disp=0.010, freq=11.0, seed=6.0))  # bowed, hair
# extended leg along the mound to the right, foot at the edge
wife += limb("RightThighExt", (0.63, -0.06, 0.52), (0.775, -0.235, 0.435),
             0.082, 0.062, mat=MARBLE)
wife += limb("RightShinExt", (0.775, -0.235, 0.435), (0.86, -0.31, 0.355),
             0.052, 0.034, mat=MARBLE)
wife.append(ball("RightFootExt", (0.88, -0.355, 0.335), (0.045, 0.085, 0.028), mat=MARBLE))
# folded leg under the body
wife += limb("RightThighFold", (0.55, -0.10, 0.50), (0.44, -0.27, 0.40),
             0.08, 0.06, mat=MARBLE)
wife.append(ball("RightFootFold", (0.415, -0.315, 0.335), (0.042, 0.075, 0.026), mat=MARBLE))
# raised arm to Cain's hand
wife += limb("RightArmUp", (0.505, -0.02, 0.88), (0.52, -0.135, 0.875),
             0.042, 0.03, mat=MARBLE)
wife.append(ball("RightHandUp", (0.522, -0.148, 0.868), (0.036, 0.052, 0.026), mat=MARBLE))
# supporting arm down to the mound
wife += limb("RightArmDown", (0.63, -0.08, 0.72), (0.665, -0.30, 0.42),
             0.045, 0.03, mat=MARBLE)
wife.append(ball("RightHandDown", (0.67, -0.325, 0.395), (0.04, 0.055, 0.024), mat=MARBLE))
reg(unify(wife, "RightFigure"))

# =================================================================
# INFANT — tucked between the central child and the right figure,
# head resting against the right figure's side.
inf = []
inf.append(ball("InfantBody", (0.335, -0.22, 0.50), (0.095, 0.085, 0.075), mat=MARBLE))
inf.append(ball("InfantHead", (0.375, -0.265, 0.625), (0.068, 0.068, 0.072), mat=MARBLE))
inf += limb("InfantArm", (0.31, -0.25, 0.575), (0.235, -0.315, 0.45),
            0.024, 0.017, mat=MARBLE)
inf += limb("InfantLeg", (0.30, -0.16, 0.475), (0.225, -0.24, 0.365),
            0.028, 0.019, mat=MARBLE)
reg(unify(inf, "Infant"))

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
print(f"[cain] triangles: {tris}")
print(f"[cain] bbox X {min(xs):.3f}..{max(xs):.3f} ({max(xs)-min(xs):.3f} m)")
print(f"[cain] bbox Y {min(ys):.3f}..{max(ys):.3f} ({max(ys)-min(ys):.3f} m)")
print(f"[cain] bbox Z {min(zs):.3f}..{max(zs):.3f} ({max(zs)-min(zs):.3f} m)")

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, "cain-and-his-children.blend"))
bpy.ops.export_scene.gltf(
    filepath=os.path.join(OUT_DIR, "cain-and-his-children.glb"),
    export_format="GLB", use_selection=True, export_apply=True)
print("[cain] blend + glb saved")

# ----------------------------------------------------------------- render rig
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

TARGET = Vector((0, 0, 0.95))

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

add_area("Key", (4.2, -5.6, 6.6), (6.0, 4.2), 1000)
add_area("Fill", (-5.8, -3.0, 2.6), (5.0, 3.6), 340)
add_area("Rim", (-1.0, 5.4, 4.8), (5.0, 3.2), 680)

cam_data = bpy.data.cameras.new("Camera")
cam_data.lens = 50
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam

VIEWS = {
    "front": Vector((0.05, -5.6, 1.15)),
    "side": Vector((5.6, 0.05, 1.15)),
    "three-quarter": Vector((3.5, -4.4, 2.3)),
    "photomatch": Vector((0.5, -4.3, 1.45)),  # stereograph viewpoint, approx.
}
os.makedirs(os.path.join(OUT_DIR, "renders"), exist_ok=True)
for name, pos in VIEWS.items():
    cam.location = pos
    tgt = Vector((0.0, 0, 0.93)) if name == "photomatch" else TARGET
    cam.rotation_euler = (tgt - pos).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(OUT_DIR, "renders", f"{name}.png")
    bpy.ops.render.render(write_still=True)
    print(f"[cain] rendered {name}")

print("[cain] done")
