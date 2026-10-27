#!/usr/bin/env python3
"""
Assyrian human-headed bull (lamassu) — Crystal Palace, Sydenham Nineveh Court cast.
Procedural build, Blender 4.2, headless.

Design basis: Delamotte album photograph "Assyrian Court. Facade Towards the Nave"
(MET DP323102, CC0) — top-left image of the album sheet.  See NOTES.md for the
measured vs inferred breakdown.

Local axes: +X = forward (head end), +Y = figure's left, +Z = up.
Origin at base centre; model sits on z=0 (plinth bottom).
"""
import bpy
import bmesh
import math
import os
import sys
from mathutils import Vector, Matrix

# ---------------------------------------------------------------- parameters
PLINTH_H = 0.15
PLINTH_L = 3.70
PLINTH_W = 1.25
SG = PLINTH_H                      # statue ground (top of plinth)

BODY_HALF_W = 0.40                 # slab-like body, per the facade photographs
BACK_Z = 2.12                      # statue coords (above SG)
BELLY_Z = 1.12
CHEST_X = 1.30
RUMP_X = -1.44

# ---------------------------------------------------------------- scene reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ---------------------------------------------------------------- materials
def make_mat(name, rgb, rough=0.85):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return m

MAT_STONE = make_mat("Stone", (0.545, 0.525, 0.485))
MAT_DARK = make_mat("StoneDark", (0.415, 0.395, 0.365))   # hair / beard / hooves articulation
MAT_PLINTH = make_mat("Plinth", (0.44, 0.425, 0.40))

MODEL_OBJS = []

def register(obj, mat=None):
    if mat:
        obj.data.materials.append(mat)
    MODEL_OBJS.append(obj)
    return obj

def finish(obj):
    """Apply rotation/scale (keep location), return obj."""
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return obj

# ---------------------------------------------------------------- helpers
def prism_from_profile(pts_xz, y0, y1, name, mat):
    """Extrude a 2D profile (list of (x,z)) between y0 and y1."""
    bm = bmesh.new()
    verts = [bm.verts.new((x, y0, z)) for (x, z) in pts_xz]
    face = bm.faces.new(verts)
    res = bmesh.ops.extrude_face_region(bm, geom=[face])
    new_verts = [g for g in res['geom'] if isinstance(g, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=new_verts, vec=(0, y1 - y0, 0))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    return register(obj, mat)

def box(name, loc, size, mat, rot=(0, 0, 0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.dimensions = size
    finish(obj)
    if bevel:
        bev = obj.modifiers.new("b", 'BEVEL')
        bev.width = bevel
        bev.segments = 2
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier="b")
    return register(obj, mat)

def sphere(name, loc, scale, mat, seg=20, rings=14):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    finish(obj)
    for p in obj.data.polygons:
        p.use_smooth = True
    return register(obj, mat)

def cylinder(name, loc, r, h, mat, verts=18, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h,
                                        location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    finish(obj)
    return register(obj, mat)

def cone(name, loc, r1, r2, h, mat, verts=14, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2,
                                    depth=h, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    finish(obj)
    return register(obj, mat)

def limb(name, p1, p2, r1, r2, mat, verts=14):
    """Tapered cylinder between two points (r1 at p1, r2 at p2)."""
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    L = d.length
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r2, radius2=r1,
                                    depth=L, location=(p1 + p2) / 2)
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    finish(obj)
    for p in obj.data.polygons:
        p.use_smooth = True
    return register(obj, mat)

def beam(name, p1, p2, w, t, mat):
    """Thin box from p1 to p2 (+X along the beam)."""
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    L = d.length
    bpy.ops.mesh.primitive_cube_add(location=(p1 + p2) / 2)
    obj = bpy.context.active_object
    obj.name = name
    obj.dimensions = (L, w, t)
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = Vector((1, 0, 0)).rotation_difference(d.normalized())
    finish(obj)
    return register(obj, mat)

def torus(name, loc, major, minor, mat, rot=(0, 0, 0), arc=2 * math.pi,
          major_seg=14, minor_seg=6):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
                                     major_segments=major_seg, minor_segments=minor_seg,
                                     location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    # primitive_torus_add in 4.2 ignores 'arc' style partial via abso; full ring used
    finish(obj)
    return register(obj, mat)

def z(v):
    """statue coords -> world (add plinth top)."""
    return v + SG

# ------------------------------------------------- merged low-poly instances
def _unit_sphere(seg=7, rings=4):
    """Unit UV sphere as (verts, faces); low-poly template for instancing."""
    verts = [(0.0, 0.0, 1.0)]
    for r in range(1, rings):
        phi = math.pi * r / rings
        for sgi in range(seg):
            th = 2 * math.pi * sgi / seg
            verts.append((math.sin(phi) * math.cos(th),
                          math.sin(phi) * math.sin(th),
                          math.cos(phi)))
    verts.append((0.0, 0.0, -1.0))
    faces = []
    for sgi in range(seg):
        faces.append((0, 1 + (sgi + 1) % seg, 1 + sgi))
    for r in range(rings - 2):
        row0 = 1 + r * seg
        row1 = row0 + seg
        for sgi in range(seg):
            a, b = row0 + sgi, row0 + (sgi + 1) % seg
            c, d = row1 + sgi, row1 + (sgi + 1) % seg
            faces.append((a, b, d))
            faces.append((a, d, c))
    last = len(verts) - 1
    rowb = 1 + (rings - 2) * seg
    for sgi in range(seg):
        faces.append((last, rowb + sgi, rowb + (sgi + 1) % seg))
    return verts, faces

_UNIT_VERTS, _UNIT_FACES = _unit_sphere()

def instances_mesh(name, items, mat):
    """One mesh from many axis-aligned scaled unit spheres.
    items: list of (loc, scale) tuples."""
    verts, faces = [], []
    for loc, sc in items:
        base = len(verts)
        for (x, y, zz) in _UNIT_VERTS:
            verts.append((loc[0] + x * sc[0], loc[1] + y * sc[1], loc[2] + zz * sc[2]))
        for f in _UNIT_FACES:
            faces.append(tuple(base + i for i in f))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    return register(obj, mat)

# ---------------------------------------------------------------- plinth
box("PlinthStep", (0, 0, 0.02), (PLINTH_L + 0.07, PLINTH_W + 0.07, 0.04), MAT_PLINTH)
box("Plinth", (0, 0, PLINTH_H / 2 + 0.02), (PLINTH_L, PLINTH_W, PLINTH_H - 0.04), MAT_PLINTH)

# ---------------------------------------------------------------- body core
profile = [
    (1.20, z(1.14)), (1.35, z(1.30)), (1.38, z(1.62)), (1.33, z(1.94)),
    (1.10, z(2.10)), (0.55, z(2.17)), (-0.30, z(2.19)), (-0.98, z(2.15)),
    (-1.36, z(2.05)), (-1.50, z(1.86)), (-1.53, z(1.55)), (-1.48, z(1.28)),
    (-1.24, z(1.15)), (-0.40, z(1.10)), (0.45, z(1.10)), (0.98, z(1.11)),
]
body = prism_from_profile(profile, -BODY_HALF_W, BODY_HALF_W, "Body", MAT_STONE)
# soften the slab edges
bev = body.modifiers.new("bev", 'BEVEL')
bev.width = 0.035
bev.segments = 2
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.modifier_apply(modifier="bev")

# brisket / chest mass (also drives the apron scale placement below)
BRISKET_C = (1.14, 0, 1.58)
BRISKET_R = (0.32, 0.415, 0.48)
sphere("Brisket", (BRISKET_C[0], BRISKET_C[1], z(BRISKET_C[2])), BRISKET_R, MAT_STONE, seg=16, rings=12)
# rump rounding
sphere("Rump", (-1.34, 0, z(1.60)), (0.30, 0.40, 0.50), MAT_STONE, seg=16, rings=12)

# ---------------------------------------------------------------- legs
def leg(x, y, hind, tag):
    sx = 1 if y > 0 else -1
    if not hind:
        # front leg: near-vertical, slight knee
        limb(f"Leg{tag}Upper", (x, y, z(1.35)), (x + 0.01, y, z(0.58)), 0.165, 0.118, MAT_STONE)
        limb(f"Leg{tag}Cannon", (x + 0.01, y, z(0.60)), (x + 0.015, y, z(0.16)), 0.108, 0.094, MAT_STONE)
        hoof_z = 0.0
        hoof_x = x + 0.02
    else:
        # hind leg: thigh angles back to hock, cannon vertical
        limb(f"Leg{tag}Thigh", (x + 0.10, y, z(1.42)), (x - 0.06, y, z(0.66)), 0.175, 0.120, MAT_STONE)
        limb(f"Leg{tag}Cannon", (x - 0.06, y, z(0.68)), (x - 0.05, y, z(0.16)), 0.104, 0.090, MAT_STONE)
        hoof_z = 0.0
        hoof_x = x - 0.045
    # fetlock ring
    torus(f"Leg{tag}Fetlock", (hoof_x, y, z(0.175)), 0.088, 0.016, MAT_STONE)
    # cloven hoof: two toe boxes
    for s in (-1, 1):
        toe = box(f"Leg{tag}Toe{s}", (hoof_x + 0.035, y + s * 0.049, z(0.06)),
                  (0.185, 0.088, 0.125), MAT_DARK)
        # round the toes a little
        bev = toe.modifiers.new("b", 'BEVEL')
        bev.width = 0.02
        bev.segments = 2
        bpy.ops.object.select_all(action='DESELECT')
        toe.select_set(True)
        bpy.context.view_layer.objects.active = toe
        bpy.ops.object.modifier_apply(modifier="b")

leg(1.08, 0.26, False, "FL")
leg(1.08, -0.26, False, "FR")
leg(-1.12, 0.26, True, "HL")
leg(-1.12, -0.26, True, "HR")

# ---------------------------------------------------------------- tail
limb("Tail1", (-1.52, 0, z(1.92)), (-1.58, 0, z(1.30)), 0.048, 0.040, MAT_STONE)
limb("Tail2", (-1.58, 0, z(1.32)), (-1.59, 0, z(0.78)), 0.040, 0.033, MAT_STONE)
sphere("TailTuft", (-1.59, 0, z(0.60)), (0.075, 0.070, 0.17), MAT_DARK)

# ---------------------------------------------------------------- neck + head
limb("Neck", (1.26, 0, z(1.78)), (1.50, 0, z(2.26)), 0.27, 0.235, MAT_STONE)

HEAD_X = 1.56
# cranium + face
sphere("Cranium", (HEAD_X - 0.04, 0, z(2.54)), (0.22, 0.185, 0.23), MAT_STONE, seg=20, rings=14)
sphere("Face", (HEAD_X + 0.11, 0, z(2.46)), (0.145, 0.165, 0.215), MAT_STONE, seg=20, rings=14)
# brow ridge
box("Brow", (HEAD_X + 0.225, 0, z(2.575)), (0.055, 0.29, 0.05), MAT_STONE, rot=(0, -0.15, 0), bevel=0.012)
# eyes (almond, nearly flush)
for s in (-1, 1):
    sphere(f"Eye{s}", (HEAD_X + 0.215, s * 0.09, z(2.535)), (0.020, 0.048, 0.016),
           MAT_DARK, seg=12, rings=8)
# nose: bridge + wider base
box("NoseBridge", (HEAD_X + 0.235, 0, z(2.465)), (0.07, 0.072, 0.165), MAT_STONE, rot=(0, 0.06, 0), bevel=0.014)
box("NoseBase", (HEAD_X + 0.225, 0, z(2.375)), (0.08, 0.11, 0.05), MAT_STONE, bevel=0.012)
# mouth + chin
box("Mouth", (HEAD_X + 0.21, 0, z(2.325)), (0.055, 0.115, 0.026), MAT_STONE, bevel=0.008)
sphere("Chin", (HEAD_X + 0.145, 0, z(2.275)), (0.09, 0.10, 0.06), MAT_STONE, seg=16, rings=12)
# ears (bovine, sideways, kept small as in the photographs)
for s in (-1, 1):
    cone(f"Ear{s}", (HEAD_X - 0.07, s * 0.207, z(2.51)), 0.045, 0.014, 0.11, MAT_STONE,
         rot=(s * 1.25, 0, 0))
# NOTE: a horn-like curve at the crown base on the middle bull of the row could
# not be resolved at the photograph's resolution — horns deliberately omitted
# (see NOTES.md).

# hair side locks with curl rows
HAIR_CURLS = []
for s in (-1, 1):
    box(f"HairLock{s}", (HEAD_X - 0.03, s * 0.207, z(2.16)), (0.25, 0.06, 0.62), MAT_DARK)
    for r in range(9):
        for c in range(4):
            HAIR_CURLS.append(((HEAD_X - 0.115 + c * 0.0575, s * 0.243, z(1.90 + r * 0.055)),
                               (0.023, 0.013, 0.023)))
instances_mesh("HairCurls", HAIR_CURLS, MAT_DARK)

# beard: deep block + grid of curls on the front face; chest-hair mass fills
# the junction between beard and chest so no bare neck shows
box("ChestHair", (1.44, 0, z(1.93)), (0.34, 0.36, 0.60), MAT_DARK, rot=(0, -0.10, 0), bevel=0.05)
beard = box("Beard", (HEAD_X + 0.10, 0, z(1.99)), (0.26, 0.30, 0.62), MAT_DARK, bevel=0.03)
BEARD_CURLS = []
for r in range(14):
    for c in range(7):
        BEARD_CURLS.append(((HEAD_X + 0.234, -0.126 + c * 0.042, z(1.715 + r * 0.0415)),
                            (0.0135, 0.0205, 0.0205)))
instances_mesh("BeardCurls", BEARD_CURLS, MAT_DARK)

# ---------------------------------------------------------------- crown (tiered mitre)
CX = HEAD_X - 0.04
CROWN_DOTS = []
# diadem band + rosette row
cylinder("CrownDiadem", (CX, 0, z(2.7175)), 0.215, 0.11, MAT_STONE, verts=28)
for i in range(18):
    a = 2 * math.pi * i / 18
    CROWN_DOTS.append(((CX + 0.210 * math.cos(a), 0.210 * math.sin(a), z(2.7175)),
                       (0.017, 0.017, 0.017)))
# main dotted band
cylinder("CrownBand", (CX, 0, z(2.8325)), 0.225, 0.155, MAT_STONE, verts=28)
for row, zz in enumerate((2.7925, 2.8725)):
    for i in range(20):
        a = 2 * math.pi * (i + row * 0.5) / 20
        CROWN_DOTS.append(((CX + 0.219 * math.cos(a), 0.219 * math.sin(a), z(zz)),
                           (0.0185, 0.0185, 0.0185)))
instances_mesh("CrownDots", CROWN_DOTS, MAT_DARK)
# ribbed top rim
cylinder("CrownRim", (CX, 0, z(2.9575)), 0.233, 0.095, MAT_STONE, verts=28)
for i in range(26):
    a = 2 * math.pi * i / 26
    box(f"CrownRib{i}", (CX + 0.229 * math.cos(a), 0.229 * math.sin(a), z(2.9575)),
        (0.016, 0.016, 0.10), MAT_STONE, rot=(0, 0, -a))
# cap
cylinder("CrownCap", (CX, 0, z(3.0155)), 0.205, 0.035, MAT_STONE, verts=28)
sphere("CrownDome", (CX, 0, z(3.0225)), (0.205, 0.205, 0.03), MAT_STONE, seg=20, rings=8)

# ---------------------------------------------------------------- wings
WING_PROFILE = [
    (0.88, 1.72), (0.84, 1.98), (0.68, 2.22), (0.42, 2.38),
    (0.10, 2.45), (-0.22, 2.44), (-0.55, 2.37), (-0.82, 2.24),
    (-1.00, 2.05), (-1.10, 1.90), (-1.03, 1.76), (-0.78, 1.665),
    (-0.33, 1.63), (0.17, 1.635), (0.58, 1.66), (0.80, 1.685),
]
WING_PROFILE = [(x, z(zz)) for (x, zz) in WING_PROFILE]

def point_in_poly(x, zz, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, z1 = poly[i]
        x2, z2 = poly[(i + 1) % n]
        if (z1 > zz) != (z2 > zz):
            xin = (x2 - x1) * (zz - z1) / (z2 - z1) + x1
            if x < xin:
                inside = not inside
    return inside

WING_SCALES = []
for s in (1, -1):
    y_in = s * 0.425
    y_out = s * 0.475
    wing = prism_from_profile(WING_PROFILE, min(y_in, y_out), max(y_in, y_out),
                              f"Wing{s}", MAT_STONE)
    # primary feather ridges: long near-parallel sweeps from the lower root
    # to the top/trailing edge, as drawn by the photograph's feather lines
    root_pts = [(0.74, 1.78), (0.42, 1.72), (0.05, 1.685), (-0.32, 1.67),
                (-0.66, 1.69), (-0.90, 1.78)]
    tip_pts = [(0.28, 2.40), (-0.08, 2.445), (-0.44, 2.415), (-0.74, 2.315),
               (-0.97, 2.13), (-1.06, 1.95)]
    for i, ((x1, z1), (x2, z2)) in enumerate(zip(root_pts, tip_pts)):
        beam(f"Feather{s}_{i}", (x1, s * 0.482, z(z1)), (x2, s * 0.482, z(z2)),
             0.030, 0.016, MAT_STONE)
    # covert band: two rows of scales along the wing's lower front
    for r in range(2):
        for c in range(10):
            xx = 0.74 - c * 0.113
            zz = 1.90 - r * 0.095 - (0.74 - xx) * 0.10
            WING_SCALES.append(((xx, s * 0.480, z(zz)), (0.044, 0.012, 0.036)))
instances_mesh("WingCovertScales", WING_SCALES, MAT_STONE)

# ---------------------------------------------------------------- scale panels
SIDE_SCALES = []
def scale_panel(s, x_from, x_to, z_from, z_to, dx=0.062, dz=0.055):
    cols = max(2, int((x_to - x_from) / dx) + 1)
    rows = max(2, int((z_to - z_from) / dz) + 1)
    for r in range(rows):
        zz = z_from + r * (z_to - z_from) / (rows - 1)
        off = (r % 2) * dx * 0.5
        for c in range(cols):
            xx = x_from + c * (x_to - x_from) / (cols - 1) + (off if c < cols - 1 else 0)
            if point_in_poly(xx, z(zz), WING_PROFILE):
                continue  # wing root covers this area
            SIDE_SCALES.append(((xx, s * 0.409, z(zz)), (0.052, 0.016, 0.054)))

for s in (1, -1):
    scale_panel(s, 0.60, 1.30, 1.30, 1.94)     # shoulder
    scale_panel(s, -1.42, -0.78, 1.32, 1.90)   # hindquarter
instances_mesh("SideScales", SIDE_SCALES, MAT_STONE)

# chest apron (front face, facing +X) — scales sit on the brisket surface
APRON_SCALES = []
for r in range(9):
    zz = 1.30 + r * 0.0775
    for c in range(8):
        yy = -0.272 + c * 0.0775 + ((r % 2) * 0.038)
        if abs(yy) > 0.30:
            continue
        k = 1.0 - ((zz - BRISKET_C[2]) / BRISKET_R[2]) ** 2 - (yy / BRISKET_R[1]) ** 2
        if k < 0.18:
            continue  # surface curves away at the apron's edges; scale would sink
        xx = BRISKET_C[0] + BRISKET_R[0] * math.sqrt(k) + 0.004
        APRON_SCALES.append(((xx, yy, z(zz)), (0.016, 0.050, 0.050)))
instances_mesh("ApronScales", APRON_SCALES, MAT_STONE)

# ---------------------------------------------------------------- inscription band (plain — no invented text)
for s in (1, -1):
    box(f"InscPanel{s}", (-0.02, s * 0.404, z(1.20)), (1.15, 0.014, 0.20), MAT_STONE)

# belly ribs (the ribbed skirt under the chest, seen in the photograph)
for i in range(5):
    xx = 0.52 + i * 0.115
    box(f"BellyRib{i}", (xx, 0, z(1.085)), (0.028, 0.60, 0.020), MAT_STONE)

# ---------------------------------------------------------------- report stats
bpy.context.view_layer.update()
total_tris = 0
for obj in MODEL_OBJS:
    me = obj.data
    me.calc_loop_triangles()
    total_tris += len(me.loop_triangles)
print(f"OBJECTS: {len(MODEL_OBJS)}")
print(f"TRIANGLES: {total_tris}")
# bbox
mins = Vector((1e9, 1e9, 1e9))
maxs = Vector((-1e9, -1e9, -1e9))
for obj in MODEL_OBJS:
    for c in obj.bound_box:
        w = obj.matrix_world @ Vector(c)
        mins = Vector(map(min, mins, w))
        maxs = Vector(map(max, maxs, w))
print(f"BBOX min {tuple(round(v,3) for v in mins)} max {tuple(round(v,3) for v in maxs)}")
print(f"DIMS: {maxs.x-mins.x:.3f} x {maxs.y-mins.y:.3f} x {maxs.z-mins.z:.3f} m")

# ---------------------------------------------------------------- save + export
out_dir = os.path.expanduser("~/workspace/cp-models/assyrian-lamassu")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out_dir, "assyrian-lamassu.blend"))
bpy.ops.object.select_all(action='DESELECT')
for obj in MODEL_OBJS:
    obj.select_set(True)
bpy.context.view_layer.objects.active = MODEL_OBJS[0]
bpy.ops.export_scene.gltf(filepath=os.path.join(out_dir, "assyrian-lamassu.glb"),
                          export_format='GLB', use_selection=True, export_apply=True)
print("SAVED blend + glb")
