#!/usr/bin/env python3
"""
Build: Andromeda — John Bell (candidate #2), nikbearbrown/crystal-palace.

Frontal-first procedural build from the single MET photograph
(DP323119, CC0). Figure proportions are photo-measured ratios hung on
a life-size anchor; depths, side and back are sculptural inference.
See NOTES.md for the full evidence table.

Run: blender -b --python scripts/build_andromeda.py
Outputs (in the staging folder, i.e. the parent of scripts/):
    andromeda.blend, andromeda.glb
"""
import bpy
import math
import os
import random
from mathutils import Vector, Matrix

random.seed(1851)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ----------------------------------------------------------------------
# Dimensions (metres). Groups: MEASURED = photo ratios on the stated
# anchor; ADOPTED = taken from a sibling build's documented estimate;
# INFERRED = sculptural judgement, no direct evidence.
# ----------------------------------------------------------------------
# MEASURED (photo pixel ratios; anchor = figure 1.63 m life-size,
# crown->standing sole as posed). See NOTES.md for the landmark table.
FIG_H        = 1.63     # figure vertical extent, crown to standing sole
SHOULDER_W   = 0.30     # silhouette width at shoulder line (photo ratio)
WAIST_W      = 0.215    # silhouette width at waist (photo ratio + remesh-erosion allowance)
HIP_W        = 0.315    # silhouette width at hips
Z_SHOULDER   = 1.346    # shoulder line above standing sole
Z_WAIST      = 1.075
Z_HIP        = 0.915    # pelvis centre
Z_KNEE       = 0.470    # both knees ~ level
RAISED_TOE_Z = 0.080    # raised-foot toe contact above standing sole
# ADOPTED
PED_H        = 0.55     # pedestal height (sy-classical-cast-base NOTES: ~0.5-0.6 m)
# INFERRED
PED_TOP      = 0.86    # pedestal top slab plan
PED_PLAN     = 0.82     # pedestal die plan
ROCK_TOP     = 0.100   # rock height at standing-foot contact

SLAB_H = 0.025
FIG_Z = PED_H + SLAB_H + ROCK_TOP   # world z of the standing sole = 0.675

# ----------------------------------------------------------------------
# Scene reset
# ----------------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

model_coll = bpy.data.collections.new('Model')
scene.collection.children.link(model_coll)


def to_model(obj):
    model_coll.objects.link(obj)
    if obj.name in scene.collection.objects:
        scene.collection.objects.unlink(obj)
    return obj


# ----------------------------------------------------------------------
# Loft helper: rings of (centre, rx, ry) -> mesh with elliptical rings
# in planes perpendicular to the local path direction.
# ----------------------------------------------------------------------
def loft(name, rings, segments=28, cap_start=True, cap_end=True):
    n = len(rings)
    verts = []
    frames = []
    for i, (c, rx, ry) in enumerate(rings):
        if i == 0:
            t = (rings[1][0] - rings[0][0]).normalized()
        elif i == n - 1:
            t = (rings[-1][0] - rings[-2][0]).normalized()
        else:
            t = (rings[i + 1][0] - rings[i - 1][0]).normalized()
        up = Vector((0, 0, 1))
        if abs(t.dot(up)) > 0.95:
            up = Vector((0, 1, 0))
        u = t.cross(up).normalized()
        v = t.cross(u).normalized()
        frames.append((u, v))
        for j in range(segments):
            a = 2 * math.pi * j / segments
            p = c + u * (rx * math.cos(a)) + v * (ry * math.sin(a))
            verts.append(tuple(p))
    faces = []
    for i in range(n - 1):
        for j in range(segments):
            j2 = (j + 1) % segments
            a = i * segments + j
            b = i * segments + j2
            c2 = (i + 1) * segments + j2
            d = (i + 1) * segments + j
            faces.append((a, b, c2, d))
    if cap_start:
        ci = len(verts)
        verts.append(tuple(rings[0][0]))
        for j in range(segments):
            faces.append((ci, (j + 1) % segments, j))
    if cap_end:
        ci = len(verts)
        base = (n - 1) * segments
        verts.append(tuple(rings[-1][0]))
        for j in range(segments):
            faces.append((ci, base + j, base + (j + 1) % segments))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    return to_model(ob)


def ball(name, centre, scale, segments=24, rings=16, rot=None):
    """Ellipsoid built entirely in data space (object at origin).

    No object transform_apply anywhere in this build: every part's
    vertices are baked to world coordinates, so joins and remeshes
    cannot silently move a part (the round-1 raised foot was rotated
    about the world origin by an ops-based apply — data space only).
    """
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings,
                                         radius=1.0, location=(0, 0, 0))
    ob = bpy.context.active_object
    ob.name = name
    m = Matrix.Translation(centre)
    if rot:
        m = m @ Matrix.Rotation(rot[0], 4, 'X') @ Matrix.Rotation(rot[1], 4, 'Y') @ Matrix.Rotation(rot[2], 4, 'Z')
    m = m @ Matrix.Diagonal(V((scale.x, scale.y, scale.z, 1.0)))
    ob.data.transform(m)
    return to_model(ob)


def box(name, dims, centre):
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    ob = bpy.context.active_object
    ob.name = name
    ob.data.transform(Matrix.Translation(centre) @
                      Matrix.Diagonal(V((dims.x / 2, dims.y / 2, dims.z / 2, 1.0))))
    return to_model(ob)


V = Vector

# ----------------------------------------------------------------------
# FIGURE — all z below are world (figure-local + FIG_Z)
# ----------------------------------------------------------------------
def fz(z):
    return z + FIG_Z


figure_parts = []

# Torso loft: rings (z, cx, rx, ry) — widths from the photo landmarks,
# depths inferred (classical proportions, flagged in NOTES). The two
# lowest rings round the pelvis down into the thigh merge.
torso_rings_spec = [
    (0.700, 0.004, 0.096, 0.058),
    (0.740, 0.004, 0.118, 0.074),
    (0.780, 0.004, 0.134, 0.086),
    (0.860, 0.004, 0.146, 0.092),
    (0.915, 0.003, HIP_W / 2, 0.098),
    (0.970, 0.001, 0.143, 0.088),
    (1.030, -0.002, 0.122, 0.078),
    (Z_WAIST, -0.003, WAIST_W / 2, 0.076),
    (1.130, -0.002, 0.112, 0.072),
    (1.190, -0.001, 0.120, 0.076),
    (1.250, 0.000, 0.126, 0.082),
    (1.300, 0.000, 0.120, 0.072),
    (Z_SHOULDER, 0.000, 0.128, 0.064),
    (1.375, 0.000, 0.064, 0.052),
]
torso_rings = [(V((cx, 0.0, fz(z))), rx, ry) for (z, cx, rx, ry) in torso_rings_spec]
figure_parts.append(loft('Torso', torso_rings, segments=32))

# Breasts (seen, frontal) — soft, wide, low-profile against the chest.
for s in (-1, 1):
    figure_parts.append(ball('Breast', V((s * 0.064, -0.046, fz(1.200))),
                             V((0.054, 0.042, 0.044))))
# Buttocks (inferred — back never photographed).
for s in (-1, 1):
    figure_parts.append(ball('Buttock', V((s * 0.074, 0.058, fz(0.895))),
                             V((0.082, 0.055, 0.080))))
# Deltoid caps — tucked close to the shoulder line.
for s in (-1, 1):
    figure_parts.append(ball('Deltoid', V((s * 0.124, 0.0, fz(1.328))),
                             V((0.046, 0.048, 0.052))))

# Legs — path lofts. Standing leg = figure's LEFT (+X, viewer's right).
standing_leg = [
    (V((0.084, 0.000, fz(1.000))), 0.076, 0.074),
    (V((0.082, -0.001, fz(0.900))), 0.082, 0.080),
    (V((0.076, -0.003, fz(0.800))), 0.080, 0.078),
    (V((0.066, -0.004, fz(0.660))), 0.070, 0.067),
    (V((0.048, -0.005, fz(0.530))), 0.058, 0.055),
    (V((0.042, -0.006, fz(Z_KNEE))), 0.050, 0.047),
    (V((0.033, 0.010, fz(0.310))), 0.050, 0.047),
    (V((0.024, -0.001, fz(0.160))), 0.034, 0.032),
    (V((0.017, -0.008, fz(0.052))), 0.028, 0.026),
]
figure_parts.append(loft('LegStanding', standing_leg, segments=24))
# Raised leg = figure's RIGHT (-X): knee forward, shin near-vertical,
# foot pointed onto the raised rock lump.
raised_leg = [
    (V((-0.086, 0.000, fz(1.005))), 0.076, 0.074),
    (V((-0.092, -0.004, fz(0.905))), 0.080, 0.078),
    (V((-0.098, -0.012, fz(0.805))), 0.078, 0.076),
    (V((-0.105, -0.020, fz(0.640))), 0.068, 0.065),
    (V((-0.113, -0.028, fz(Z_KNEE + 0.003))), 0.050, 0.047),
    (V((-0.114, -0.016, fz(0.330))), 0.046, 0.043),
    (V((-0.113, -0.020, fz(0.224))), 0.028, 0.026),
]
figure_parts.append(loft('LegRaised', raised_leg, segments=24))

# Feet.
figure_parts.append(ball('FootStanding', V((0.017, -0.062, fz(0.014))),
                         V((0.047, 0.125, 0.020))))
figure_parts.append(ball('ToesStanding', V((0.017, -0.148, fz(0.009))),
                         V((0.034, 0.036, 0.011))))
figure_parts.append(ball('AnkleBlend', V((0.017, -0.010, fz(0.045))),
                         V((0.036, 0.050, 0.035))))
figure_parts.append(ball('FootRaised', V((-0.130, -0.028, fz(0.158))),
                         V((0.036, 0.046, 0.080)),
                         rot=(math.radians(-16), 0, math.radians(11))))
figure_parts.append(ball('ToesRaised', V((-0.146, -0.034, fz(0.092))),
                         V((0.030, 0.036, 0.026))))

# Arms — both pass behind the back; wrists meet at the shackle point.
def arm(side):
    s = side  # -1 = figure's right, +1 = figure's left
    pts = [
        (V((s * 0.130, 0.008, fz(1.334))), 0.054, 0.052),
        (V((s * 0.140, 0.020, fz(1.200))), 0.043, 0.041),
        (V((s * 0.148, 0.055, fz(1.078))), 0.036, 0.034),   # elbow, behind hip line
        (V((s * 0.120, 0.115, fz(0.985))), 0.031, 0.029),
        (V((s * 0.038, 0.152, fz(0.945))), 0.027, 0.025),   # wrist, behind back
    ]
    return loft('Arm', pts, segments=20)

figure_parts.append(arm(-1))
figure_parts.append(arm(1))
# Hands (merged pair at the shackle, hidden behind the back).
for s in (-1, 1):
    figure_parts.append(ball('Hand', V((s * 0.028, 0.158, fz(0.940))),
                             V((0.030, 0.026, 0.052))))

# Neck + head, in a head frame: pitched forward 27 deg, yawed -10 deg
# (face turned slightly to her right, gaze down — as photographed).
neck_rings = [
    (V((0.000, -0.004, fz(1.360))), 0.058, 0.052),
    (V((0.000, -0.016, fz(1.400))), 0.047, 0.044),
    (V((-0.002, -0.026, fz(1.435))), 0.044, 0.042),
]
figure_parts.append(loft('Neck', neck_rings, segments=24))

head_origin = V((-0.002, -0.032, fz(1.440)))
M_head = (Matrix.Translation(head_origin) @
          Matrix.Rotation(math.radians(-10), 4, 'Z') @
          Matrix.Rotation(math.radians(34), 4, 'X'))


def head_part(name, centre_local, scale, segments=28, rings=20):
    ob = ball(name, V((0, 0, 0)), V((1, 1, 1)), segments=segments, rings=rings)
    m = M_head @ Matrix.Translation(centre_local) @ Matrix.Diagonal(V((scale.x, scale.y, scale.z, 1.0)))
    ob.data.transform(m)
    return ob


figure_parts.append(head_part('Cranium', V((0, 0.004, 0.118)), V((0.083, 0.089, 0.092))))
figure_parts.append(head_part('Face', V((0, -0.016, 0.048)), V((0.070, 0.074, 0.077))))
figure_parts.append(head_part('Jaw', V((0, -0.014, 0.012)), V((0.046, 0.052, 0.034))))
# Nose — schematic wedge on the face front.
figure_parts.append(head_part('Nose', V((0, -0.080, 0.048)), V((0.012, 0.017, 0.024)), segments=16, rings=12))

# ----------------------------------------------------------------------
# Join figure parts and voxel-remesh into one skin
# ----------------------------------------------------------------------
bpy.ops.object.select_all(action='DESELECT')
for ob in figure_parts:
    ob.select_set(True)
bpy.context.view_layer.objects.active = figure_parts[0]
bpy.ops.object.join()
figure = bpy.context.view_layer.objects.active
figure.name = 'Figure'
figure.data.remesh_mode = 'VOXEL'
figure.data.remesh_voxel_size = 0.011
figure.data.use_remesh_fix_poles = True
bpy.ops.object.voxel_remesh()
# Smooth shading + a gentle Laplacian pass: the raw remesh grid read
# as long flat facets down the legs in rounds 1-2.
for p in figure.data.polygons:
    p.use_smooth = True
_soft = figure.modifiers.new('Soften', 'SMOOTH')
_soft.factor = 0.32
_soft.iterations = 3
bpy.context.view_layer.objects.active = figure
bpy.ops.object.modifier_apply(modifier=_soft.name)

# If the remesh overshoots the triangle budget, decimate the figure.
def tri_count(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)

ft = tri_count(figure)
print('Figure triangles after remesh:', ft)
if ft > 38000:
    ratio = 38000 / ft
    mod = figure.modifiers.new('Budget', 'DECIMATE')
    mod.ratio = ratio
    bpy.context.view_layer.objects.active = figure
    bpy.ops.object.modifier_apply(modifier=mod.name)
    print('Figure triangles after decimate:', tri_count(figure))

# ----------------------------------------------------------------------
# Smooth low-frequency value noise (hair curls + rock crag)
# ----------------------------------------------------------------------
def _hash(ix, iy, iz):
    h = (ix * 374761393 + iy * 668265263 + iz * 2147483629) & 0xffffffff
    h = (h ^ (h >> 13)) * 1274126177 & 0xffffffff
    return ((h ^ (h >> 16)) & 0xffff) / 0xffff


def value_noise(p, cell):
    gx, gy, gz = p.x / cell, p.y / cell, p.z / cell
    ix, iy, iz = math.floor(gx), math.floor(gy), math.floor(gz)
    fx, fy, fz = gx - ix, gy - iy, gz - iz
    sx, sy, sz = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy), fz * fz * (3 - 2 * fz)

    def L(a, b, t):
        return a + (b - a) * t

    return L(
        L(L(_hash(ix, iy, iz), _hash(ix + 1, iy, iz), sx),
          L(_hash(ix, iy + 1, iz), _hash(ix + 1, iy + 1, iz), sx), sy),
        L(L(_hash(ix, iy, iz + 1), _hash(ix + 1, iy, iz + 1), sx),
          L(_hash(ix, iy + 1, iz + 1), _hash(ix + 1, iy + 1, iz + 1), sx), sy), sz)


# ----------------------------------------------------------------------
# HAIR — curly cap + back bun, same stone, noise-displaced shell
# ----------------------------------------------------------------------
hair = head_part('Hair', V((0, 0.010, 0.120)), V((0.088, 0.094, 0.097)), segments=36, rings=24)
# Tuck the lower-front of the shell in to form the hairline (graded,
# so no hard shelf); displace the rest for the carved-curl read.
M_inv = M_head.inverted()
for vtx in hair.data.vertices:
    local = M_inv @ vtx.co
    if local.z < 0.055 and local.y < 0.020:
        t = max(0.0, min(1.0, (0.055 - local.z) / 0.075))
        f = 1.0 - 0.07 * t
        vtx.co = head_origin + (vtx.co - head_origin) * f
for vtx in hair.data.vertices:
    n = vtx.normal
    d = (value_noise(vtx.co, 0.020) - 0.5) * 0.012
    d += (value_noise(vtx.co + V((3.1, 8.4, 1.7)), 0.045) - 0.5) * 0.006
    vtx.co += n * d
hair.data.update()
bun = head_part('HairBun', V((0, 0.082, 0.052)), V((0.050, 0.042, 0.050)), segments=20, rings=14)
for vtx in bun.data.vertices:
    vtx.co += vtx.normal * random.uniform(-0.003, 0.003)
bun.data.update()
for _ob in (hair, bun):
    for _p in _ob.data.polygons:
        _p.use_smooth = True

# Shackle ring at the wrists (behind the back).
bpy.ops.mesh.primitive_torus_add(major_radius=0.030, minor_radius=0.007,
                                 major_segments=20, minor_segments=8,
                                 location=V((0, 0.168, fz(0.945))))
shackle = to_model(bpy.context.active_object)
shackle.name = 'Shackle'
shackle.rotation_euler = (math.radians(90), 0, 0)
bpy.context.view_layer.objects.active = shackle
bpy.ops.object.transform_apply(rotation=True)

# ----------------------------------------------------------------------
# CHAIN — instanced torus links along a Catmull-Rom path
# (photo: wrists -> around right hip -> hangs at thigh -> diagonal
# across the fronts of the thighs -> down the standing shin -> rock)
# ----------------------------------------------------------------------
def catmull_rom(points, samples_per_seg=14):
    pts = [points[0]] + list(points) + [points[-1]]
    out = []
    for i in range(len(pts) - 3):
        p0, p1, p2, p3 = pts[i], pts[i + 1], pts[i + 2], pts[i + 3]
        for j in range(samples_per_seg):
            t = j / samples_per_seg
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t +
                              (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
                              (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(points[-1])
    return out


chain_ctrl = [
    V((0.000, 0.168, fz(0.945))),     # at the shackle, behind the back
    V((-0.150, 0.118, fz(0.885))),
    V((-0.190, 0.010, fz(0.872))),    # around the right hip
    V((-0.194, -0.052, fz(0.660))),   # hanging free beside the thigh
    V((-0.150, -0.100, fz(0.540))),
    V((-0.055, -0.092, fz(0.470))),   # diagonal across the thighs
    V((0.006, -0.082, fz(0.428))),
    V((0.044, -0.048, fz(0.300))),    # down the front of the standing shin
    V((0.048, -0.046, fz(0.150))),
    V((0.095, -0.052, fz(0.045))),    # onto the rock
    V((0.150, -0.040, fz(0.012))),    # pooled at the anchor
]
path = catmull_rom(chain_ctrl, samples_per_seg=16)
# Resample the path at ~link pitch.
LINK_PITCH = 0.033
samples = [path[0]]
acc = 0.0
for a, b in zip(path, path[1:]):
    acc += (b - a).length
    if acc >= LINK_PITCH:
        samples.append(b)
        acc = 0.0
if (samples[-1] - path[-1]).length > 0.012:
    samples.append(path[-1])

bpy.ops.mesh.primitive_torus_add(major_radius=0.0140, minor_radius=0.0040,
                                 major_segments=12, minor_segments=6,
                                 location=(0, 0, -10))
link_proto = to_model(bpy.context.active_object)
link_proto.name = 'LinkProto'

chain_links = []
for i, p in enumerate(samples):
    if i == 0:
        tangent = (samples[1] - samples[0]).normalized()
    elif i == len(samples) - 1:
        tangent = (samples[-1] - samples[-2]).normalized()
    else:
        tangent = (samples[i + 1] - samples[i - 1]).normalized()
    ob = link_proto.copy()
    ob.data = link_proto.data
    ob.location = p
    # Torus lies in XY plane, axis = Z. Lay the link along the tangent,
    # twisting alternate links 90 degrees about the tangent.
    z_axis = tangent
    ref = Vector((0, 0, 1)) if abs(tangent.z) < 0.9 else Vector((1, 0, 0))
    x_axis = z_axis.cross(ref).normalized()
    y_axis = z_axis.cross(x_axis).normalized()
    m = Matrix((x_axis, y_axis, z_axis)).to_4x4()
    twist = Matrix.Rotation(math.radians(90) * (i % 2), 4, 'Z')
    roll = Matrix.Rotation(math.radians(90), 4, 'X')  # link plane contains tangent
    ob.matrix_world = Matrix.Translation(p) @ m @ twist @ roll
    model_coll.objects.link(ob)
    chain_links.append(ob)
bpy.data.objects.remove(link_proto, do_unlink=True)

# Two pooled links lying flat at the anchor.
for k, (px, py, ang) in enumerate(((0.168, -0.018, 25), (0.150, 0.018, 100))):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.0140, minor_radius=0.0040,
                                     major_segments=12, minor_segments=6,
                                     location=V((px, py, fz(0.006))))
    ob = to_model(bpy.context.active_object)
    ob.name = 'ChainPool'
    ob.rotation_euler = (0, 0, math.radians(ang))
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.transform_apply(rotation=True)
    chain_links.append(ob)

# Join the chain into one object.
bpy.ops.object.select_all(action='DESELECT')
for ob in chain_links:
    ob.select_set(True)
bpy.context.view_layer.objects.active = chain_links[0]
bpy.ops.object.join()
chain = bpy.context.view_layer.objects.active
chain.name = 'Chain'

# ----------------------------------------------------------------------
# ROCK — craggy mound: displaced merged lumps, remeshed
# ----------------------------------------------------------------------
rock_parts = []
rock_base = ball('RockBase', V((0.000, 0.000, PED_H + SLAB_H + 0.052)),
                 V((0.40, 0.27, 0.068)), segments=28, rings=18)
rock_parts.append(rock_base)
rock_parts.append(ball('RockLumpRaised', V((-0.150, -0.010, PED_H + SLAB_H + 0.108)),
                       V((0.135, 0.115, 0.086)), segments=20, rings=14))
rock_parts.append(ball('RockToeKnob', V((-0.148, -0.022, PED_H + SLAB_H + 0.062)),
                       V((0.075, 0.070, 0.052)), segments=16, rings=12))
rock_parts.append(ball('RockCragFront', V((0.185, -0.115, PED_H + SLAB_H + 0.045)),
                       V((0.115, 0.095, 0.058)), segments=20, rings=14))
rock_parts.append(ball('RockKnobLeft', V((-0.315, 0.030, PED_H + SLAB_H + 0.052)),
                       V((0.055, 0.050, 0.052)), segments=16, rings=12))
rock_parts.append(ball('RockBack', V((0.030, 0.130, PED_H + SLAB_H + 0.058)),
                       V((0.20, 0.10, 0.062)), segments=20, rings=14))
bpy.ops.object.select_all(action='DESELECT')
for ob in rock_parts:
    ob.select_set(True)
bpy.context.view_layer.objects.active = rock_parts[0]
bpy.ops.object.join()
rock = bpy.context.view_layer.objects.active
rock.name = 'Rock'
rock.data.remesh_mode = 'VOXEL'
rock.data.remesh_voxel_size = 0.016
bpy.ops.object.voxel_remesh()


# Crag displacement uses the value-noise helpers defined above.
for v in rock.data.vertices:
    n = value_noise(v.co, 0.055) - 0.5
    n += 0.5 * (value_noise(v.co + V((7.3, 2.9, 5.1)), 0.16) - 0.5)
    if v.co.z > PED_H + SLAB_H + 0.01:   # keep the underside seated
        v.co += v.normal * n * 0.055
rock.data.update()
print('Rock triangles:', tri_count(rock))

# ----------------------------------------------------------------------
# PEDESTAL — plain dark box + top slab + inscribed front face
# ----------------------------------------------------------------------
ped = box('Pedestal', V((PED_PLAN, PED_PLAN, PED_H)), V((0, 0, PED_H / 2)))
slab = box('PedestalSlab', V((PED_TOP, PED_TOP, SLAB_H)), V((0, 0, PED_H + SLAB_H / 2)))
base_shadow = box('PedestalBase', V((0.78, 0.78, 0.03)), V((0, 0, 0.015)))

tex_path = os.path.join(HERE, 'inscription_texture.png')
img = bpy.data.images.load(tex_path)
img.pack()   # keep the .blend self-contained
# Inscribed front face as an explicit mesh (world-space verts + UVs);
# the round-1 ops-built plane landed under the pedestal.
fx, fy = PED_PLAN / 2, -PED_PLAN / 2 - 0.0012
me_face = bpy.data.meshes.new('PedestalFace')
me_face.from_pydata(
    [(-fx, fy, 0.0), (fx, fy, 0.0), (fx, fy, PED_H), (-fx, fy, PED_H)],
    [], [(0, 1, 2, 3)])
me_face.update()
uv_layer = me_face.uv_layers.new(name='UVMap')
for loop in me_face.loops:
    vi = loop.vertex_index
    uv_layer.data[loop.index].uv = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))[vi]
face = bpy.data.objects.new('PedestalFace', me_face)
to_model(face)

# ----------------------------------------------------------------------
# MATERIALS
# ----------------------------------------------------------------------
def principled(name, colour, roughness, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*colour, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    return m

mat_stone = principled('PlasterStone', (0.845, 0.825, 0.775), 0.62)
mat_rock = principled('RockStone', (0.565, 0.545, 0.50), 0.95)
mat_ebonised = principled('EbonisedWood', (0.030, 0.027, 0.023), 0.72)
mat_iron = principled('DarkIron', (0.055, 0.055, 0.058), 0.48, metallic=0.85)

figure.data.materials.append(mat_stone)
hair.data.materials.append(mat_stone)
bun.data.materials.append(mat_stone)
rock.data.materials.append(mat_rock)
for ob in (ped, slab, base_shadow):
    ob.data.materials.append(mat_ebonised)
chain.data.materials.append(mat_iron)
shackle.data.materials.append(mat_iron)

mat_face = bpy.data.materials.new('Inscription')
mat_face.use_nodes = True
nt = mat_face.node_tree
bsdf = nt.nodes['Principled BSDF']
tex = nt.nodes.new('ShaderNodeTexImage')
tex.image = img
nt.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
bsdf.inputs['Roughness'].default_value = 0.72
face.data.materials.append(mat_face)

# ----------------------------------------------------------------------
# Save + export
# ----------------------------------------------------------------------
for ob in model_coll.objects:
    ob.select_set(True)
bpy.context.view_layer.objects.active = figure
total = sum(tri_count(ob) for ob in model_coll.objects if ob.type == 'MESH')
print('TOTAL triangles:', total)
with open(os.path.join(ROOT, 'build_stats.txt'), 'w') as fh:
    for ob in sorted(model_coll.objects, key=lambda o: o.name):
        if ob.type == 'MESH':
            fh.write(f'{ob.name}: {tri_count(ob)} tris, dims '
                     f'{ob.dimensions.x:.3f} x {ob.dimensions.y:.3f} x {ob.dimensions.z:.3f}\n')
    fh.write(f'TOTAL: {total}\n')

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, 'andromeda.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT, 'andromeda.glb'),
                          export_format='GLB', use_selection=True,
                          export_apply=True)
print('BUILD DONE')
