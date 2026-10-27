#!/usr/bin/env python3
"""Build the Minerva bust (candidate #7) for the Crystal Palace film.

Sydenham Greek & Roman Court (CP036): the helmeted bust labelled
"328 / MINERVA / FROM MUNICH" in Rijksmuseum stereograph RP-F-2012-96-327,
on its tall dark court pedestal (the CastBase_Bust of
models/sy-classical-cast-base/, reproduced at its published dimensions
so the two props agree: pedestal 1.30 m, die 0.46 m square).

Scale chain (see NOTES.md): pedestal 1.30 m adopted from the cast-base
build; bust + socle = pedestal / 1.48 (ratio measured on this same
photograph by that build) = 0.88 m. Internal proportions are measured
fractions of that height from the left half of the stereograph.

Front of the bust faces -Y. The head turns to its anatomical left
(+X) and bows, as photographed. Blender 4.2, metres, origin at the
base centre, floor z = 0.
"""
import bpy
import math
import random
from mathutils import Vector

random.seed(328)

# ---------------------------------------------------------------- helpers

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.materials):
        pass

def superellipse(t, a, b, e):
    c, s = math.cos(t), math.sin(t)
    x = a * math.copysign(abs(c) ** e, c)
    y = b * math.copysign(abs(s) ** e, s)
    return x, y

def loft(name, rings, seg=72, expo=0.9, cap_bottom=False, cap_top=False,
         displace=None):
    """rings: list of (z, cx, cy, rx, ry). displace: fn(x,y,z,theta)->radial scale."""
    verts, faces = [], []
    for (z, cx, cy, rx, ry) in rings:
        for i in range(seg):
            t = 2 * math.pi * i / seg
            x, y = superellipse(t, rx, ry, expo)
            if displace:
                s = displace(cx + x, cy + y, z, t)
                x, y = x * s, y * s
            verts.append((cx + x, cy + y, z))
    for r in range(len(rings) - 1):
        for i in range(seg):
            a = r * seg + i
            b = r * seg + (i + 1) % seg
            c = (r + 1) * seg + (i + 1) % seg
            d = (r + 1) * seg + i
            faces.append((a, b, c, d))
    if cap_bottom:
        z, cx, cy = rings[0][0], rings[0][1], rings[0][2]
        ci = len(verts); verts.append((cx, cy, z))
        for i in range(seg):
            faces.append((ci, (i + 1) % seg, i))
    if cap_top:
        z, cx, cy = rings[-1][0], rings[-1][1], rings[-1][2]
        base = (len(rings) - 1) * seg
        ci = len(verts); verts.append((cx, cy, z))
        for i in range(seg):
            faces.append((ci, base + i, base + (i + 1) % seg))
    return make_mesh(name, verts, faces)

def lathe(name, profile, seg=64):
    """profile: list of (r, z), bottom to top."""
    verts, faces = [], []
    for (r, z) in profile:
        for i in range(seg):
            t = 2 * math.pi * i / seg
            verts.append((r * math.cos(t), r * math.sin(t), z))
    for r in range(len(profile) - 1):
        for i in range(seg):
            a = r * seg + i
            b = r * seg + (i + 1) % seg
            c = (r + 1) * seg + (i + 1) % seg
            d = (r + 1) * seg + i
            faces.append((a, b, c, d))
    # bottom cap fan
    ci = len(verts); verts.append((0, 0, profile[0][1]))
    for i in range(seg):
        faces.append((ci, (i + 1) % seg, i))
    return make_mesh(name, verts, faces)

def partial_loft(name, rings, seg=24, t0=0.0, t1=math.pi):
    """Loft over an angular span (for the helmet neck guard).
    rings: (z, cx, cy, rx, ry)."""
    verts, faces = [], []
    for (z, cx, cy, rx, ry) in rings:
        for i in range(seg + 1):
            t = t0 + (t1 - t0) * i / seg
            verts.append((cx + rx * math.cos(t), cy + ry * math.sin(t), z))
    w = seg + 1
    for r in range(len(rings) - 1):
        for i in range(seg):
            a = r * w + i; b = a + 1; c = a + w + 1; d = a + w
            faces.append((a, b, c, d))
    return make_mesh(name, verts, faces)

def loft_points(name, rings_pts, cap_bottom=False, cap_top=False):
    """Loft through explicit per-ring (x, y) point lists.
    rings_pts: list of (z, [(x, y), ...]) with equal counts per ring."""
    verts, faces = [], []
    seg = len(rings_pts[0][1])
    for (z, pts) in rings_pts:
        for (x, y) in pts:
            verts.append((x, y, z))
    for r in range(len(rings_pts) - 1):
        for i in range(seg):
            a = r * seg + i
            b = r * seg + (i + 1) % seg
            c = (r + 1) * seg + (i + 1) % seg
            d = (r + 1) * seg + i
            faces.append((a, b, c, d))
    if cap_bottom:
        z, pts = rings_pts[0]
        ci = len(verts); verts.append((0, 0, z))
        for i in range(seg):
            faces.append((ci, (i + 1) % seg, i))
    if cap_top:
        z, pts = rings_pts[-1]
        base = (len(rings_pts) - 1) * seg
        ci = len(verts); verts.append((0, 0, z))
        for i in range(seg):
            faces.append((ci, base + i, base + (i + 1) % seg))
    return make_mesh(name, verts, faces)

def rounded_rect_outline(a, b, r, straight=12, arc=6):
    """CCW outline of a rectangle of half-widths (a, b) with corner
    radius r, in the XY plane. 4*(straight+arc) = 72 points.
    Walk: +X face up, corner, +Y face left, corner, -X face down,
    corner, -Y face right, corner -- CCW seen from +Z."""
    pts = []
    for i in range(straight):  # +X face, -Y -> +Y
        f = (i + 1) / (straight + 1)
        pts.append((a, -(b - r) + 2 * (b - r) * f))
    for j in range(arc):       # corner centre (a-r, b-r), angles 0..90
        t = math.radians(90 * (j + 1) / arc)
        pts.append(((a - r) + r * math.cos(t), (b - r) + r * math.sin(t)))
    for i in range(straight):  # +Y face, +X -> -X
        f = (i + 1) / (straight + 1)
        pts.append(((a - r) - 2 * (a - r) * f, b))
    for j in range(arc):       # corner centre (-(a-r), b-r), 90..180
        t = math.radians(90 + 90 * (j + 1) / arc)
        pts.append((-(a - r) + r * math.cos(t), (b - r) + r * math.sin(t)))
    for i in range(straight):  # -X face, +Y -> -Y
        f = (i + 1) / (straight + 1)
        pts.append((-a, (b - r) - 2 * (b - r) * f))
    for j in range(arc):       # corner centre (-(a-r), -(b-r)), 180..270
        t = math.radians(180 + 90 * (j + 1) / arc)
        pts.append((-(a - r) + r * math.cos(t), -(b - r) + r * math.sin(t)))
    for i in range(straight):  # -Y face, -X -> +X
        f = (i + 1) / (straight + 1)
        pts.append((-(a - r) + 2 * (a - r) * f, -b))
    for j in range(arc):       # corner centre (a-r, -(b-r)), 270..360
        t = math.radians(270 + 90 * (j + 1) / arc)
        pts.append(((a - r) + r * math.cos(t), -(b - r) + r * math.sin(t)))
    return pts

def tube(name, points, radii, sides=10):
    """Round tube along a polyline with per-point radii."""
    pts = [Vector(p) for p in points]
    verts, faces = [], []
    up = Vector((0, 0, 1))
    for i, p in enumerate(pts):
        if i == 0:
            tan = (pts[1] - pts[0]).normalized()
        elif i == len(pts) - 1:
            tan = (pts[-1] - pts[-2]).normalized()
        else:
            tan = (pts[i + 1] - pts[i - 1]).normalized()
        n1 = tan.cross(up)
        if n1.length < 1e-4:
            n1 = Vector((1, 0, 0))
        n1.normalize()
        n2 = tan.cross(n1).normalized()
        for j in range(sides):
            t = 2 * math.pi * j / sides
            off = radii[i] * (math.cos(t) * n1 + math.sin(t) * n2)
            verts.append(tuple(p + off))
    for r in range(len(pts) - 1):
        for j in range(sides):
            a = r * sides + j
            b = r * sides + (j + 1) % sides
            c = (r + 1) * sides + (j + 1) % sides
            d = (r + 1) * sides + j
            faces.append((a, b, c, d))
    # end caps
    ci = len(verts); verts.append(tuple(pts[0]))
    for j in range(sides):
        faces.append((ci, (j + 1) % sides, j))
    ci = len(verts); verts.append(tuple(pts[-1]))
    base = (len(pts) - 1) * sides
    for j in range(sides):
        faces.append((ci, base + j, base + (j + 1) % sides))
    return make_mesh(name, verts, faces)

def ellipsoid(name, loc, scale, wseg=24, hseg=16, noise=0.0):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=wseg, ring_count=hseg,
                                         location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    if noise:
        for v in ob.data.vertices:
            n = math.sin(v.co.x * 91.7) * math.sin(v.co.y * 77.3) * math.sin(v.co.z * 83.9)
            v.co += v.co.normalized() * noise * n if v.co.length else v.co
    return ob

def box(name, loc, size):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = size
    bpy.ops.object.transform_apply(scale=True)
    return ob

def make_mesh(name, verts, faces):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    return ob

def join_objects(name, obs):
    bpy.ops.object.select_all(action='DESELECT')
    for o in obs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    bpy.ops.object.join()
    ob = bpy.context.active_object
    ob.name = name
    return ob

def assign(ob, mat):
    ob.data.materials.append(mat)

# ---------------------------------------------------------------- materials

def make_mat(name, rgb, rough=0.6):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return m

clean_scene()
PLASTER = make_mat("PlasterCast", (0.80, 0.78, 0.74), 0.62)
DARK = make_mat("PedestalDark", (0.052, 0.043, 0.038), 0.55)
PLATE = make_mat("LabelPlate", (0.105, 0.095, 0.085), 0.5)

# ---------------------------------------------------------------- pedestal
# Reproduces models/sy-classical-cast-base/ CastBase_Bust at its published
# dimensions: total height 1.30 m; foot step 0.055 high projecting 38 mm;
# cove 0.095; die 0.46 m square; plain flat top (no cap moulding).

ped_profile = [  # (z, half-width)
    (0.000, 0.268), (0.055, 0.268),   # foot step
    (0.075, 0.261), (0.100, 0.249),   # cove sweep
    (0.125, 0.238), (0.150, 0.230),   # die begins
    (1.295, 0.230), (1.300, 0.230),
]
ped_rings = [(z, rounded_rect_outline(hw, hw, 0.028 * hw / 0.268))
             for (z, hw) in ped_profile]
pedestal = loft_points("Pedestal", ped_rings, cap_bottom=True, cap_top=True)
assign(pedestal, DARK)

# recessed unlettered label plate, high on the front (-Y) die face,
# as in the display-plinth build (project practice: no fabricated text)
plate = box("LabelPlate", (0, -0.2315, 1.175), (0.24, 0.006, 0.125))
assign(plate, PLATE)

# ---------------------------------------------------------------- socle
# Turned round socle of the bust itself, read from the socle crop:
# flared trumpet neck under the bust, a projecting roll at ~60% height,
# concave waist, stepped wide foot. Height 0.15 m (0.175 of bust+socle).

socle_profile = [
    (0.115, 1.300), (0.115, 1.314), (0.104, 1.324), (0.096, 1.342),
    (0.093, 1.358), (0.100, 1.372), (0.111, 1.384), (0.108, 1.396),
    (0.099, 1.406), (0.103, 1.418), (0.118, 1.432), (0.138, 1.444),
    (0.148, 1.450),
]
socle = lathe("Socle", socle_profile, seg=56)
assign(socle, PLASTER)

bpy.context.view_layer.objects.active = socle
print("pedestal + socle done")

# ---------------------------------------------------------------- bust body
# Lofted torso: truncation at z 1.45 (on the socle), chest, shoulders,
# neck base. Max width 0.50 m at the chest (photo fractions applied to
# the 0.88 m bust+socle: truncation ~0.44 wide, shoulders ~0.50).

BODY_RINGS = [
    (1.450, 0, 0.002, 0.215, 0.150),
    (1.470, 0, 0.002, 0.228, 0.158),
    (1.520, 0, 0.000, 0.240, 0.165),
    (1.580, 0, -0.002, 0.250, 0.172),
    (1.640, 0, -0.002, 0.248, 0.170),
    (1.700, 0, 0.000, 0.240, 0.163),
    (1.755, 0, 0.002, 0.216, 0.146),
    (1.795, 0, 0.004, 0.180, 0.126),
    (1.835, 0, 0.004, 0.138, 0.106),
    (1.865, 0, 0.002, 0.086, 0.080),
    (1.878, 0, 0.000, 0.052, 0.048),
]

def ring_ry_rx(z):
    """Interpolate (rx, ry) of BODY_RINGS at height z."""
    if z <= BODY_RINGS[0][0]:
        return BODY_RINGS[0][3], BODY_RINGS[0][4]
    for a, b in zip(BODY_RINGS, BODY_RINGS[1:]):
        if a[0] <= z <= b[0]:
            f = (z - a[0]) / (b[0] - a[0])
            return (a[3] + (b[3] - a[3]) * f, a[4] + (b[4] - a[4]) * f)
    return BODY_RINGS[-1][3], BODY_RINGS[-1][4]

def surf_y(x, z, proud=0.0):
    """Front (-Y) surface ordinate of the bust body at (x, z)."""
    rx, ry = ring_ry_rx(z)
    k = min(abs(x) / rx, 0.999)
    return -ry * (1 - k ** 2.35) ** (1 / 2.35) + proud

def body_folds(x, y, z, theta):
    """Radial scale for carved drapery: fine vertical folds low on the
    truncation, a diagonal swirl across the chest front."""
    r = max(math.hypot(x, y), 1e-5)
    d = 0.0
    if y < 0.03:  # front and sides
        low = max(0.0, 1 - (z - 1.45) / 0.18)          # fades by z 1.63
        d += 0.0042 * math.sin(theta * 9 + 1.2) * low
        mid = max(0.0, 1 - abs(z - 1.63) / 0.17)       # chest band
        phase = x * 0.9 - (z - 1.45) * 1.35
        d += 0.0032 * math.sin(phase * 40.0) * mid * (1 if y < -0.02 else 0.3)
    return 1 + d / r

bust = loft("BustBody", BODY_RINGS, seg=96, expo=0.85, cap_bottom=True,
            cap_top=True, displace=body_folds)
assign(bust, PLASTER)

# Bold diagonal pleats: five fold tubes sweeping from the anatomical
# left shoulder (+X) down across the chest to the lower right, as the
# photograph's heavy himation folds read.
pleats = []
base_path = [(0.185, 1.827), (0.150, 1.757), (0.095, 1.687),
             (0.020, 1.622), (-0.060, 1.567), (-0.125, 1.520)]
for k in range(5):
    ox, oz = k * 0.030, -k * 0.020
    pts = []
    for (x, z) in base_path:
        xx, zz = x + ox * 0.4, z + oz
        if zz < 1.470:
            continue
        pts.append((xx, surf_y(xx, zz, proud=-0.0045), zz))
    rads = [0.0125 - 0.0009 * i for i in range(len(pts))]
    pleats.append(tube(f"Pleat{k}", pts, rads, sides=10))
# three shorter pleats over the left shoulder
for k in range(3):
    ox = k * 0.026
    pts = []
    for (x, z) in [(0.085 + ox, 1.862), (0.140 + ox, 1.852), (0.185 + ox, 1.800),
                   (0.200 + ox, 1.735)]:
        pts.append((x, surf_y(x, z, proud=-0.004), z))
    pleats.append(tube(f"ShPleat{k}", pts, [0.010, 0.011, 0.010, 0.008], sides=10))
pleats_ob = join_objects("Pleats", pleats)
assign(pleats_ob, PLASTER)

# ---------------------------------------------------------------- aegis
# Scaly aegis patch high on the chest with the gorgoneion at its
# centre, offset toward the anatomical right (-X), as photographed.
aegis_parts = []
patch = ellipsoid("AegisPatch", (-0.055, -0.143, 1.665), (0.088, 0.034, 0.108),
                  noise=0.005)
aegis_parts.append(patch)
# gorgoneion disc
bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=0.034, depth=0.015,
                                    location=(-0.055, -0.181, 1.672),
                                    rotation=(math.radians(96), 0, 0))
disc = bpy.context.active_object; disc.name = "Gorgoneion"
aegis_parts.append(disc)
# schematic face on the disc: two eye bumps, brow bar, nose wedge
for sx in (-1, 1):
    aegis_parts.append(ellipsoid(f"GorgEye{sx}", (-0.055 + sx * 0.0125, -0.190, 1.680),
                                 (0.0062, 0.004, 0.005)))
aegis_parts.append(box("GorgBrow", (-0.055, -0.1885, 1.686), (0.036, 0.006, 0.007)))
bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.0075, radius2=0.002,
                                depth=0.020, location=(-0.055, -0.190, 1.664),
                                rotation=(math.radians(-96), 0, 0))
nose_g = bpy.context.active_object; nose_g.name = "GorgNose"
aegis_parts.append(nose_g)
# snake fringe: small bumps around the patch's lower rim
for i in range(7):
    a = math.pi * (0.15 + 0.70 * i / 6)
    sx = -0.055 + 0.082 * math.cos(a)
    sz = 1.665 - 0.100 * math.sin(a)
    aegis_parts.append(ellipsoid(f"Snake{i}", (sx, surf_y(sx, sz, proud=-0.002), sz),
                                 (0.006, 0.006, 0.006)))
aegis = join_objects("Aegis", aegis_parts)
assign(aegis, PLASTER)

# aegis strap / trim cord descending from the neck to the patch
strap = tube("AegisStrap",
             [(0.052, surf_y(0.052, 1.858, proud=-0.002), 1.858),
              (0.028, surf_y(0.028, 1.790, proud=-0.002), 1.790),
              (-0.005, surf_y(-0.005, 1.738, proud=-0.002), 1.738),
              (-0.036, surf_y(-0.036, 1.712, proud=-0.002), 1.712)],
             [0.005, 0.005, 0.005, 0.0045], sides=8)
assign(strap, PLASTER)

print("bust body + aegis done")

# ---------------------------------------------------------------- head group
# Built in local coordinates (front -Y, origin at the neck-top pivot),
# then placed with the photographed pose: yaw +45 deg about Z (turned
# to its anatomical left, +X) and pitch +19 deg about X (bowed down).
# The yaw is the single-view estimate that makes the face read as the
# photograph's three-quarter from the photograph's own quadrant.
# Pivot world (0, -0.012, 1.917) sets the helmet crown at 2.18 m and
# the chin at 1.84 m, matching the stereograph's fractions of the
# 0.88 m bust + socle.

PIVOT = Vector((0, -0.012, 1.932))
from mathutils import Matrix
HEAD_M = (Matrix.Translation(PIVOT)
          @ Matrix.Rotation(math.radians(45), 4, 'Z')
          @ Matrix.Rotation(math.radians(19), 4, 'X'))

def place_head(ob):
    ob.matrix_world = HEAD_M
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return ob

neck = loft("Neck", [
    (-0.145, 0, 0.024, 0.084, 0.079),
    (-0.105, 0, 0.020, 0.082, 0.077),
    (-0.060, 0, 0.012, 0.075, 0.070),
    (-0.020, 0, 0.006, 0.071, 0.066),
    (0.005, 0, 0.003, 0.069, 0.064),
], seg=64, expo=0.9, cap_bottom=True)
place_head(neck); assign(neck, PLASTER)

def face_sculpt(x, y, z, theta):
    r = max(math.hypot(x, y), 1e-5)
    d = 0.0
    if y < -0.02:  # face front only
        d += 0.0035 * math.exp(-((z - 0.098) / 0.013) ** 2) * max(0.0, 1 - abs(x) / 0.075)
        d -= 0.0032 * math.exp(-(((abs(x) - 0.030) / 0.012) ** 2 + ((z - 0.034) / 0.010) ** 2))
        d -= 0.0020 * math.exp(-((z + 0.022) / 0.0045) ** 2) * math.exp(-(x / 0.020) ** 2)
    return 1 + d / r

head_parts = []
head = loft("Head", [
    (-0.062, 0, 0.002, 0.052, 0.058),
    (-0.025, 0, -0.004, 0.066, 0.072),
    (0.030, 0, -0.006, 0.073, 0.080),
    (0.095, 0, -0.002, 0.070, 0.079),
    (0.130, 0, 0.004, 0.072, 0.084),
    (0.160, 0, 0.008, 0.068, 0.082),
    (0.185, 0, 0.010, 0.052, 0.066),
    (0.200, 0, 0.012, 0.028, 0.038),
], seg=72, expo=0.9, cap_bottom=True, cap_top=True, displace=face_sculpt)
head_parts.append(head)
head_parts.append(tube("Nose",
                       [(0, -0.080, 0.088), (0, -0.100, 0.062), (0, -0.108, 0.038),
                        (0, -0.100, 0.018), (0, -0.090, 0.006)],
                       [0.0125, 0.0105, 0.0090, 0.0105, 0.008], sides=10))
for sx in (-1, 1):
    head_parts.append(ellipsoid(f"NostrilWing{sx}", (sx * 0.0125, -0.094, 0.010),
                                (0.007, 0.009, 0.005)))
head_ob = join_objects("Head", head_parts)
place_head(head_ob); assign(head_ob, PLASTER)

hair_parts = []
for sx in (-1, 1):
    hair_parts.append(ellipsoid(f"HairSide{sx}", (sx * 0.070, 0.014, 0.005),
                                (0.023, 0.030, 0.044), noise=0.004))
    hair_parts.append(ellipsoid(f"HairLow{sx}", (sx * 0.068, 0.028, -0.045),
                                (0.022, 0.027, 0.036), noise=0.004))
    hair_parts.append(ellipsoid(f"HairBack{sx}", (sx * 0.060, 0.052, -0.055),
                                (0.022, 0.026, 0.032), noise=0.004))
hair_parts.append(ellipsoid("HairNape", (0, 0.082, -0.010), (0.052, 0.026, 0.044),
                            noise=0.004))
hair = join_objects("Hair", hair_parts)
place_head(hair); assign(hair, PLASTER)

helmet_parts = []
helmet_parts.append(loft("HelmetBowl", [
    (0.098, 0, 0.002, 0.089, 0.101),
    (0.128, 0, 0.004, 0.091, 0.104),
    (0.165, 0, 0.006, 0.087, 0.100),
    (0.205, 0, 0.008, 0.077, 0.091),
    (0.238, 0, 0.010, 0.061, 0.074),
    (0.258, 0, 0.011, 0.040, 0.050),
    (0.268, 0, 0.012, 0.018, 0.024),
], seg=72, expo=0.9, cap_top=True))
helmet_parts.append(loft("HelmetBand", [
    (0.098, 0, 0.002, 0.0925, 0.1045),
    (0.116, 0, 0.003, 0.0935, 0.1055),
], seg=72, expo=0.9))
for sx in (-1, 1):
    helmet_parts.append(ellipsoid(f"CheekPiece{sx}", (sx * 0.079, -0.034, 0.040),
                                  (0.013, 0.040, 0.052)))
guard = partial_loft("NeckGuard", [
    (0.095, 0, 0.004, 0.097, 0.106),
    (0.045, 0, 0.005, 0.102, 0.112),
    (-0.010, 0, 0.007, 0.110, 0.119),
], seg=26, t0=math.radians(26), t1=math.radians(154))
mod = guard.modifiers.new("solid", 'SOLIDIFY'); mod.thickness = 0.0045
bpy.context.view_layer.objects.active = guard
bpy.ops.object.modifier_apply(modifier=mod.name)
helmet_parts.append(guard)
# NOTE: no crest or crest ridge is modelled -- the dome reads smooth
# in the stereograph; see NOTES.md.
helmet = join_objects("Helmet", helmet_parts)
place_head(helmet); assign(helmet, PLASTER)

# ---------------------------------------------------------------- report/save
tris = 0
for ob in bpy.context.scene.objects:
    if ob.type == 'MESH':
        tris += sum(max(len(p.vertices) - 2, 0) for p in ob.data.polygons)
print("OBJECTS:", [(o.name, o.dimensions[:]) for o in bpy.context.scene.objects if o.type == 'MESH'])
print("TRIANGLES:", tris)
import os
OUT = os.path.expanduser("~/workspace/cp-models/minerva-bust")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "minerva-bust.blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "minerva-bust.glb"),
                          export_format='GLB')
print("saved blend + glb")
