"""
Hercules Reposing — the Farnese Hercules cast, Sydenham nave,
procedural Blender 4.2 build.

Frontal-first construction from the Rijksmuseum stereograph
RP-F-2012-96-329 (CC0): the ONLY view of this cast in the collection.
Masses are chained ellipsoids/lofts posed to track the photograph's
frontal silhouette (weary slump, crossed legs, lion skin sheeted over
the club at his left), then joined and voxel-remeshed. Depth, side
and back are inferred from the Farnese type (see ../NOTES.md).

Outputs: ../hercules-reposing.blend, ../hercules-reposing.glb,
         ../renders/{front,side,three-quarter,photomatch}.png
Run: blender -b --python build_hercules_reposing.py [-- final]
"""

import bpy
import math
import os
import random
import sys
from mathutils import Vector, noise as mnoise

random.seed(41)

OUT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FINAL = "final" in sys.argv
RES = 1000 if FINAL else 640
VOXEL = 0.021

# Pose constants (metres). Figure front faces -Y; his left is +X.
PED_H = 0.90          # pedestal, adopted from the documented court family
SLAB_H = 0.24         # pale integral base slab, photo ratio 0.122 x figure
FZ = PED_H + SLAB_H   # figure feet plane = 1.14

# ----------------------------------------------------------------- materials

def make_material(name, color, roughness):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat

MARBLE = None
SLAB_M = None
EBON = None
PLATE_M = None

# ----------------------------------------------------------------- helpers

def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

def loft(name, stations, segs=16, cap=True, smooth=True):
    """Loft elliptical rings along a spine. stations: (centre Vector,
    half_w, half_h)."""
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

def box_loft(name, profile, mat):
    """profile: list of (z, half_w, half_d) — rectangular loft."""
    n = len(profile)
    verts, faces = [], []
    for (z, hw, hd) in profile:
        for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            verts.append((sx * hw, sy * hd, z))
    for i in range(n - 1):
        for j in range(4):
            a = i * 4 + j
            b = i * 4 + (j + 1) % 4
            c2 = (i + 1) * 4 + (j + 1) % 4
            d = (i + 1) * 4 + j
            faces.append((a, b, c2, d))
    # caps
    ci = len(verts); verts.append((0, 0, profile[0][0]))
    for j in range(4):
        faces.append((ci, (j + 1) % 4, j))
    ci = len(verts); verts.append((0, 0, profile[-1][0]))
    base = (n - 1) * 4
    for j in range(4):
        faces.append((ci, base + j, base + (j + 1) % 4))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if mat is not None:
        obj.data.materials.append(mat)
    return obj

MODEL_OBJECTS = []
def reg(o):
    MODEL_OBJECTS.append(o)
    return o

V = Vector

# =================================================================
clear_scene()
MARBLE = make_material("CastPlaster", (0.905, 0.885, 0.845), 0.52)
SLAB_M = make_material("BaseSlab", (0.925, 0.915, 0.885), 0.6)
EBON = make_material("EbonisedBase", (0.055, 0.05, 0.045), 0.55)
PLATE_M = make_material("LabelPlate", (0.16, 0.15, 0.14), 0.6)

def L(x, y, z):
    """Figure-local point -> world (feet plane at FZ)."""
    return (x, y, z + FZ)

# ----------------------------------------------------------------- pedestal
# Widened variant of the documented Sydenham standing-statue pedestal
# (cf. display-plinth / sy-classical-cast-base: 0.90 m high, moulded
# foot and cap). Width/depth scaled up to carry the 1.45 m slab.
reg(box_loft("Pedestal", [
    (0.00, 0.820, 0.470),
    (0.02, 0.820, 0.470),
    (0.05, 0.770, 0.435),
    (0.16, 0.755, 0.425),
    (0.20, 0.740, 0.415),
    (0.70, 0.740, 0.415),
    (0.74, 0.755, 0.425),
    (0.85, 0.770, 0.435),
    (0.88, 0.800, 0.455),
    (0.90, 0.800, 0.455),
], EBON))

# unlettered label plate on the front face (photo lettering illegible)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.4235, 0.58))
plate = bpy.context.view_layer.objects.active
plate.name = "LabelPlate"
plate.scale = (0.36, 0.012, 0.075)
plate.data.materials.append(PLATE_M)
reg(plate)

# ----------------------------------------------------------------- slab
reg(box_loft("BaseSlab", [
    (PED_H, 0.700, 0.380),
    (PED_H + 0.03, 0.715, 0.392),
    (PED_H + SLAB_H - 0.03, 0.725, 0.400),
    (PED_H + SLAB_H, 0.705, 0.388),
], SLAB_M))

# ----------------------------------------------------------------- figure
fig = []

# torso: slumped heroic mass, belly forward, shoulders rolled
fig.append(loft("Torso", [
    (V(L(0.000, 0.020, 0.94)), 0.200, 0.145),
    (V(L(0.000, 0.025, 1.06)), 0.220, 0.160),
    (V(L(0.004, 0.045, 1.20)), 0.242, 0.184),
    (V(L(0.006, 0.058, 1.33)), 0.250, 0.205),
    (V(L(0.004, 0.038, 1.46)), 0.275, 0.192),
    (V(L(0.000, 0.012, 1.59)), 0.283, 0.183),
    (V(L(-0.004, -0.008, 1.70)), 0.262, 0.168),
    (V(L(-0.010, -0.032, 1.79)), 0.205, 0.142),
    (V(L(-0.014, -0.048, 1.86)), 0.128, 0.108),
], segs=20))
# pecs and belly
fig.append(ball("PecL", L(0.120, -0.130, 1.575), (0.124, 0.045, 0.086), mat=MARBLE))
fig.append(ball("PecR", L(-0.120, -0.130, 1.575), (0.124, 0.045, 0.086), mat=MARBLE))
fig.append(ball("Belly", L(0.005, -0.082, 1.345), (0.198, 0.098, 0.165), mat=MARBLE))
# deltoids + trapezius
fig.append(ball("DeltL", L(0.283, -0.005, 1.735), (0.098, 0.095, 0.105), mat=MARBLE))
fig.append(ball("DeltR", L(-0.283, -0.005, 1.735), (0.098, 0.095, 0.105), mat=MARBLE))
fig.append(ball("Trap", L(-0.008, -0.022, 1.830), (0.140, 0.110, 0.080), mat=MARBLE))

# head: bowed, bearded — crown at local 2.00
fig.append(ball("Skull", L(-0.018, -0.088, 1.895), (0.094, 0.099, 0.080), mat=MARBLE))
fig.append(ball("Hair", L(-0.016, -0.060, 1.928), (0.100, 0.104, 0.068),
                mat=MARBLE, disp=0.010, freq=26.0, seed=3.1))
fig.append(ball("Face", L(-0.018, -0.155, 1.836), (0.072, 0.062, 0.066), mat=MARBLE))
fig.append(ball("Beard", L(-0.018, -0.142, 1.780), (0.086, 0.076, 0.066),
                mat=MARBLE, disp=0.012, freq=22.0, seed=7.7))

# right arm hangs at his side, hand low against the thigh
fig += limb("ArmRup", L(-0.295, -0.002, 1.720), L(-0.338, -0.012, 1.385),
            0.096, 0.079, mat=MARBLE, knee=V(L(-0.338, -0.012, 1.385)), knee_r=0.082)
fig += limb("ArmRfo", L(-0.338, -0.012, 1.385), L(-0.302, -0.052, 1.075),
            0.074, 0.054, mat=MARBLE)
fig.append(ball("HandR", L(-0.308, -0.058, 1.005), (0.050, 0.036, 0.078), mat=MARBLE))

# left arm bends onto the club head
fig += limb("ArmLup", L(0.295, -0.008, 1.715), L(0.398, -0.058, 1.472),
            0.096, 0.079, mat=MARBLE, knee=V(L(0.398, -0.058, 1.472)), knee_r=0.080)
fig += limb("ArmLfo", L(0.398, -0.058, 1.472), L(0.440, -0.050, 1.348),
            0.072, 0.055, mat=MARBLE)
fig.append(ball("HandL", L(0.443, -0.055, 1.312), (0.056, 0.040, 0.068), mat=MARBLE))

# legs: right planted; left crosses in FRONT (photo's shin X)
fig += limb("LegRth", L(-0.165, 0.005, 1.03), L(-0.188, -0.008, 0.545),
            0.150, 0.112, mat=MARBLE, knee=V(L(-0.188, -0.012, 0.545)), knee_r=0.105)
fig += limb("LegRsh", L(-0.188, -0.012, 0.545), L(-0.162, -0.002, 0.095),
            0.104, 0.066, mat=MARBLE)
fig += limb("LegLth", L(0.160, 0.002, 1.03), L(-0.005, -0.088, 0.565),
            0.148, 0.110, mat=MARBLE, knee=V(L(-0.009, -0.093, 0.565)), knee_r=0.107)
fig += limb("LegLsh", L(-0.009, -0.093, 0.565), L(0.075, -0.055, 0.095),
            0.104, 0.064, mat=MARBLE)
fig.append(ball("FootR", L(-0.160, -0.076, 0.038), (0.057, 0.128, 0.036), mat=MARBLE))
fig.append(ball("FootL", L(0.078, -0.086, 0.036), (0.054, 0.125, 0.034), mat=MARBLE))

# club: near-vertical, knotty, mostly behind the skin sheet
club = loft("Club", [
    (V(L(0.462, 0.005, 0.015)), 0.046, 0.046),
    (V(L(0.458, 0.005, 0.35)), 0.052, 0.052),
    (V(L(0.455, 0.005, 0.70)), 0.058, 0.058),
    (V(L(0.452, 0.005, 1.02)), 0.066, 0.066),
    (V(L(0.450, 0.005, 1.24)), 0.074, 0.074),
    (V(L(0.448, 0.002, 1.345)), 0.078, 0.078),
], segs=14)
club.data.materials.append(MARBLE)
fig.append(club)
fig.append(ball("ClubKnot1", L(0.470, -0.010, 0.82), (0.062, 0.060, 0.070),
                mat=MARBLE, disp=0.006, freq=18.0, seed=5.2))
fig.append(ball("ClubKnot2", L(0.442, -0.008, 1.13), (0.068, 0.064, 0.062),
                mat=MARBLE, disp=0.006, freq=18.0, seed=9.4))

reg(unify(fig, "HerculesFigure", voxel=VOXEL))

# ----------------------------------------------------------------- lion skin
# Sheet draped over the club: narrow at the hand, flaring to the
# ground (photo). Fold-displaced before remesh.
skin = []
sheet = loft("SkinSheet", [
    (V(L(0.455, -0.005, 1.345)), 0.105, 0.048),
    (V(L(0.492, -0.030, 1.10)), 0.172, 0.052),
    (V(L(0.528, -0.012, 0.80)), 0.218, 0.056),
    (V(L(0.555, 0.002, 0.50)), 0.258, 0.060),
    (V(L(0.575, 0.012, 0.22)), 0.288, 0.066),
    (V(L(0.585, 0.018, 0.035)), 0.300, 0.072),
], segs=18)
me = sheet.data
for v in me.vertices:
    lx, ly, lz = v.co.x, v.co.y, v.co.z - FZ
    fold = math.sin(lx * 21.0) * 0.007 + math.sin(lx * 47.0 + 1.3) * 0.003
    n = mnoise.noise(Vector((lx * 6.0, ly * 6.0, lz * 3.0))) * 0.010
    v.co.y += (fold + n) * (1.15 - lz * 0.35)
me.update()
sheet.data.materials.append(MARBLE)
skin.append(sheet)
# lion's head mass over the club top, paws hanging in front
skin.append(ball("LionHead", L(0.450, -0.035, 1.338), (0.092, 0.082, 0.072),
                 mat=MARBLE, disp=0.009, freq=20.0, seed=2.9))
skin += limb("Paw1", L(0.415, -0.100, 1.285), L(0.400, -0.122, 1.050),
             0.027, 0.023, mat=MARBLE)
skin.append(ball("Paw1End", L(0.398, -0.125, 1.022), (0.034, 0.030, 0.042), mat=MARBLE))
skin += limb("Paw2", L(0.478, -0.102, 1.280), L(0.472, -0.124, 1.098),
             0.025, 0.021, mat=MARBLE)
skin.append(ball("Paw2End", L(0.470, -0.127, 1.072), (0.031, 0.028, 0.038), mat=MARBLE))
reg(unify(skin, "LionSkin", voxel=0.018))

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
print(f"[hercules] triangles: {tris}")
print(f"[hercules] bbox X {min(xs):.3f}..{max(xs):.3f} ({max(xs)-min(xs):.3f} m)")
print(f"[hercules] bbox Y {min(ys):.3f}..{max(ys):.3f} ({max(ys)-min(ys):.3f} m)")
print(f"[hercules] bbox Z {min(zs):.3f}..{max(zs):.3f} ({max(zs)-min(zs):.3f} m)")

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, "hercules-reposing.blend"))
bpy.ops.export_scene.gltf(
    filepath=os.path.join(OUT_DIR, "hercules-reposing.glb"),
    export_format="GLB", use_selection=True, export_apply=True)
print("[hercules] blend + glb saved")

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
scene.view_settings.exposure = -0.2

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

TARGET = Vector((0.05, 0, 1.28))

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
    "front": Vector((0.05, -6.3, 1.40)),
    "side": Vector((6.3, 0.05, 1.40)),
    "three-quarter": Vector((4.0, -5.0, 2.6)),
    "photomatch": Vector((0.60, -5.7, 1.70)),  # stereograph viewpoint, approx.
}
os.makedirs(os.path.join(OUT_DIR, "renders"), exist_ok=True)
for name, pos in VIEWS.items():
    cam.location = pos
    tgt = Vector((0.05, 0, 1.32)) if name == "photomatch" else TARGET
    cam.rotation_euler = (tgt - pos).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(OUT_DIR, "renders", f"{name}.png")
    bpy.ops.render.render(write_still=True)
    print(f"[hercules] rendered {name}")

print("[hercules] done")
