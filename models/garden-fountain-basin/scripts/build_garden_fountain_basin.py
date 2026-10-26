#!/usr/bin/env python3
"""
Sydenham garden fountain basin — Crystal Palace lower gardens.

Procedural build, Blender 4.2, headless.
Sources (repo references, see NOTES.md):
  - Delamotte photograph RP-F-F01134-AL (CC0): the great basins before the
    Palace, the lower basin in the foreground with its scalloped rim,
    urns on the rim and one tall central jet.
  - "Crystal Palace Park - fountains in 1886" (public domain): elevated
    view; the lower basin's lobed plan-form and jet pattern read from above.

The model is the BASIN ALONE (stone rim/walls/floor, water surface and the
jets as static display forms). The rim urns and the statues around the
basin are separate candidates and are NOT built here.

Plan-form: an ellipse ringed with semicircular lobes, as read from the
1886 elevated photograph. All absolute dimensions are INFERRED from the
photographs (see NOTES.md for the method); rim profile detail is beyond
the resolution of both photographs and is kept deliberately simple.

Origin at the basin centre, ground at z = 0, real-world metres.
"""
import bpy
import math
import os
from mathutils import Vector

# ----------------------------------------------------------------------------
# Parameters (metres) — all INFERRED, see NOTES.md
# ----------------------------------------------------------------------------
A = 20.0            # outline half-length (E-W, parallel to Palace front)
B = 13.5            # outline half-width  (N-S)  -> overall 40.0 x 27.0 m
LOBES = 14          # scallops around the perimeter (photos resolve ~12-16)
LOBE_AMP = 0.9      # radial amplitude of the scallops
SEG = 224           # outline samples

COPING_TOP = 0.56   # rim crown height above ground
WATER_Z = 0.40      # water surface (0.16 below the crown)
FLOOR_Z = -0.55     # basin floor

CENTRAL_JET_H = 20.0
RING1_N, RING1_FRAC, RING1_H = 8, 0.17, 7.5
RING2_N, RING2_FRAC, RING2_H = 16, 0.40, 3.4
RING3_FRAC, RING3_H = 0.78, 2.1     # one small jet per lobe
# per-jet base radii (m) — a playing jet is a near-uniform column, not a spike
JET_BASE_R = {"centre": 1.7, "ring1": 0.62, "ring2": 0.34, "ring3": 0.16}

OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = "garden-fountain-basin"

# ----------------------------------------------------------------------------
# Scene reset
# ----------------------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ----------------------------------------------------------------------------
# Materials
# ----------------------------------------------------------------------------
def principled(name, color, roughness, alpha=1.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        mat.surface_render_method = 'DITHERED'
    return mat

MAT_COPING = principled("CopingStone", (0.62, 0.58, 0.50), 0.85)   # pale stone
MAT_APRON = principled("ApronStone", (0.48, 0.45, 0.40), 0.95)    # gravel margin
MAT_INNER = principled("InnerStoneWet", (0.30, 0.31, 0.28), 0.7)  # dark, wet
MAT_FLOOR = principled("BasinFloor", (0.16, 0.19, 0.17), 0.9)     # dark floor
MAT_WATER = principled("BasinWater", (0.62, 0.70, 0.72), 0.12, alpha=0.94)
MAT_JET = principled("JetWater", (0.94, 0.97, 1.0), 0.3, alpha=0.5)
MAT_FOAM = principled("JetFoam", (0.96, 0.97, 0.97), 0.9, alpha=0.8)
MAT_GROUND = principled("StudioGround", (0.32, 0.32, 0.32), 1.0)

# ----------------------------------------------------------------------------
# Outline: ellipse + scallop modulation, sampled in polar angle
# ----------------------------------------------------------------------------
def outline_point(theta, a=A, b=B, amp=LOBE_AMP):
    re = a * b / math.sqrt((b * math.cos(theta)) ** 2 + (a * math.sin(theta)) ** 2)
    r = re + amp * math.cos(LOBES * theta)
    return Vector((r * math.cos(theta), r * math.sin(theta), 0.0))

OUTLINE = [outline_point(2 * math.pi * i / SEG) for i in range(SEG)]

def outline_normal(i):
    p_prev = OUTLINE[(i - 1) % SEG]
    p_next = OUTLINE[(i + 1) % SEG]
    t = p_next - p_prev
    n = Vector((t.y, -t.x, 0.0))
    n.normalize()
    # ensure outward: normal should point away from centre
    if n.dot(OUTLINE[i]) < 0:
        n = -n
    return n

# ----------------------------------------------------------------------------
# Stone: rim, walls and floor as one swept profile along the outline.
# Profile = (radial offset from outline along its normal, z). Negative
# offsets lie OUTSIDE the outline (apron / outer wall).
# ----------------------------------------------------------------------------
PROFILE = [
    (-1.18, -0.05),   # skirt, sunk below ground
    (-1.12,  0.04),   # apron outer edge
    (-0.60,  0.10),   # apron top
    (-0.42,  0.30),   # outer wall
    (-0.30,  0.44),   # shoulder
    (-0.13,  0.53),   # coping outer roll
    ( 0.05,  COPING_TOP),  # coping crown
    ( 0.22,  0.50),   # coping inner roll
    ( 0.30,  0.42),   # inner shoulder
    ( 0.34,  0.20),   # inner wall, waterline zone
    ( 0.34,  FLOOR_Z),     # inner wall at floor
]
# material per profile band (row between profile[i] and profile[i+1]) + floor
BAND_MATS = [1, 1, 0, 0, 0, 0, 0, 2, 2, 2]   # 0 coping, 1 apron, 2 inner
FLOOR_MAT = 3

def build_stone():
    verts = []
    for i in range(SEG):
        n = outline_normal(i)
        p = OUTLINE[i]
        for (u, z) in PROFILE:
            q = p + n * u
            verts.append((q.x, q.y, z))
    np_ = len(PROFILE)
    faces = []
    face_mat = []
    for i in range(SEG):
        j = (i + 1) % SEG
        for k in range(np_ - 1):
            a0 = i * np_ + k
            b0 = j * np_ + k
            faces.append((a0, b0, b0 + 1, a0 + 1))
            face_mat.append(BAND_MATS[k])
    # floor: fan from the last profile ring to a centre vertex
    centre_idx = len(verts)
    verts.append((0.0, 0.0, FLOOR_Z - 0.07))
    ring0 = (np_ - 1)
    for i in range(SEG):
        j = (i + 1) % SEG
        faces.append((i * np_ + ring0, j * np_ + ring0, centre_idx))
        face_mat.append(FLOOR_MAT)
    mesh = bpy.data.meshes.new("BasinStoneMesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    for m in (MAT_COPING, MAT_APRON, MAT_INNER, MAT_FLOOR):
        mesh.materials.append(m)
    for poly, mi in zip(mesh.polygons, face_mat):
        poly.material_index = mi
        poly.use_smooth = False
    obj = bpy.data.objects.new("GardenFountainBasin", mesh)
    bpy.context.collection.objects.link(obj)
    return obj

# ----------------------------------------------------------------------------
# Water: same outline inset to the inner wall, flat at WATER_Z
# ----------------------------------------------------------------------------
def build_water():
    inset = 0.28
    verts = []
    for i in range(SEG):
        th = 2 * math.pi * i / SEG
        p = outline_point(th)
        r = p.length
        q = p * ((r - inset) / r)
        verts.append((q.x, q.y, WATER_Z))
    centre_idx = len(verts)
    verts.append((0.0, 0.0, WATER_Z))
    faces = [(i, (i + 1) % SEG, centre_idx) for i in range(SEG)]
    mesh = bpy.data.meshes.new("WaterMesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    mesh.materials.append(MAT_WATER)
    obj = bpy.data.objects.new("BasinWater", mesh)
    bpy.context.collection.objects.link(obj)
    return obj

# ----------------------------------------------------------------------------
# Jets: lathed display forms + foam discs, merged into one mesh
# ----------------------------------------------------------------------------
JET_PROFILE = [  # (height fraction, radius factor) — columnar, spray-broken top
    (0.00, 1.00), (0.05, 0.78), (0.20, 0.66), (0.50, 0.60),
    (0.75, 0.60), (0.88, 0.68), (0.96, 0.55), (1.00, 0.05),
]
JET_SEG = 12

def jet_geometry(cx, cy, h, base_r, verts, faces, mat_ids, mat_id, skirt=False):
    start = len(verts)
    rings = len(JET_PROFILE)
    for (tf, rf) in JET_PROFILE:
        z = WATER_Z + tf * h
        r = base_r * rf
        for s in range(JET_SEG):
            a = 2 * math.pi * s / JET_SEG
            verts.append((cx + r * math.cos(a), cy + r * math.sin(a), z))
    for k in range(rings - 1):
        for s in range(JET_SEG):
            s2 = (s + 1) % JET_SEG
            a0 = start + k * JET_SEG + s
            b0 = start + k * JET_SEG + s2
            faces.append((a0, b0, b0 + JET_SEG, a0 + JET_SEG))
            mat_ids.append(mat_id)
    # falling-water skirt: a squat foam frustum where the jet lands
    if skirt:
        s0 = len(verts)
        for (z, r) in ((WATER_Z + 0.02, base_r * 2.6), (WATER_Z + 0.12 * h, base_r * 1.1)):
            for s in range(JET_SEG):
                a = 2 * math.pi * s / JET_SEG
                verts.append((cx + r * math.cos(a), cy + r * math.sin(a), z))
        for s in range(JET_SEG):
            s2 = (s + 1) % JET_SEG
            faces.append((s0 + s, s0 + s2, s0 + JET_SEG + s2, s0 + JET_SEG + s))
            mat_ids.append(1)
    # foam patch at water level: a low dome, not a flat plate
    foam_r = base_r * 1.6
    c_idx = len(verts)
    verts.append((cx, cy, WATER_Z + 0.09))
    ring_start = len(verts)
    for s in range(JET_SEG * 2):
        a = 2 * math.pi * s / (JET_SEG * 2)
        verts.append((cx + foam_r * math.cos(a), cy + foam_r * math.sin(a), WATER_Z + 0.02))
    for s in range(JET_SEG * 2):
        faces.append((c_idx, ring_start + s, ring_start + (s + 1) % (JET_SEG * 2)))
        mat_ids.append(1)  # foam material index in the jets mesh

def build_jets():
    verts, faces, mat_ids = [], [], []
    def add(cx, cy, h, base_r, skirt=False):
        jet_geometry(cx, cy, h, base_r, verts, faces, mat_ids, 0, skirt=skirt)
    add(0.0, 0.0, CENTRAL_JET_H, JET_BASE_R["centre"], skirt=True)
    for k in range(RING1_N):
        th = 2 * math.pi * k / RING1_N
        add(RING1_FRAC * A * math.cos(th), RING1_FRAC * B * math.sin(th),
            RING1_H, JET_BASE_R["ring1"], skirt=True)
    for k in range(RING2_N):
        th = 2 * math.pi * (k + 0.5) / RING2_N
        add(RING2_FRAC * A * math.cos(th), RING2_FRAC * B * math.sin(th),
            RING2_H, JET_BASE_R["ring2"])
    for k in range(LOBES):
        th = 2 * math.pi * k / LOBES
        p = outline_point(th)
        add(RING3_FRAC * p.x, RING3_FRAC * p.y, RING3_H, JET_BASE_R["ring3"])
    mesh = bpy.data.meshes.new("JetsMesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    mesh.materials.append(MAT_JET)
    mesh.materials.append(MAT_FOAM)
    for poly, mi in zip(mesh.polygons, mat_ids):
        poly.material_index = mi
    obj = bpy.data.objects.new("FountainJets", mesh)
    bpy.context.collection.objects.link(obj)
    return obj

stone = build_stone()
water = build_water()
jets = build_jets()
# Playing water must not cast hard shadows: in the photographs the jet
# cluster and its foam read bright, lit by sky and spray.
jets.visible_shadow = False
water.visible_shadow = False

# ----------------------------------------------------------------------------
# Studio ground (rig only — excluded from the .glb by selection)
# ----------------------------------------------------------------------------
bpy.ops.mesh.primitive_circle_add(vertices=48, radius=130.0, fill_type='NGON',
                                  location=(0, 0, -0.02))
ground = bpy.context.active_object
ground.name = "STUDIO_GROUND"
ground.data.materials.append(MAT_GROUND)

# ----------------------------------------------------------------------------
# Report, save, export
# ----------------------------------------------------------------------------
def tri_count(obj):
    return sum(len(p.vertices) - 2 for p in obj.data.polygons)

total = 0
for obj in (stone, water, jets):
    n = tri_count(obj)
    total += n
    print(f"TRIS {obj.name}: {n}  dims {tuple(round(d,2) for d in obj.dimensions)}")
print(f"TRIS TOTAL (prop): {total}")

blend_path = os.path.join(OUT_DIR, SLUG + ".blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("saved", blend_path)

bpy.ops.object.select_all(action='DESELECT')
for obj in (stone, water, jets):
    obj.select_set(True)
bpy.context.view_layer.objects.active = stone
glb_path = os.path.join(OUT_DIR, SLUG + ".glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB',
                          use_selection=True, export_apply=True)
print("exported", glb_path)
