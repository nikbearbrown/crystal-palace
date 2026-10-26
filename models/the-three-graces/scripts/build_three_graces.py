#!/usr/bin/env python3
"""Build the Three Graces prop for the Crystal Palace film (Sydenham Greek &
Roman Sculpture Court), from MET album sheet DP323102 (CC0).

STYLISED group at the limit of the evidence. The pedestal follows the
enlarged photograph closely (meander band, carved cartouche panel, low
base block). The figures are DRAPED, as the photograph shows, in a linked
arrangement read from the photograph (front pair + one behind); fine pose
detail remains convention. See NOTES.md for observed vs inferred.
Run: blender -b -noaudio --python build_three_graces.py
Outputs into ../ (the model folder): .blend, .glb, renders via render script.
"""
import bpy, math, os
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---------------------------------------------------------------- clean scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

MODEL = []

# ---------------------------------------------------------------- materials
def mat(name, color, rough=0.5, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    return m

MARBLE = mat("Cast plaster / marble (figures)", (0.93, 0.91, 0.87), 0.38)
STONE  = mat("Pedestal stone",                  (0.52, 0.49, 0.44), 0.62)
STONE_D= mat("Pedestal stone, shadowed",        (0.37, 0.35, 0.32), 0.7)
BASE_M = mat("Low base block",                  (0.25, 0.24, 0.22), 0.75)

# ---------------------------------------------------------------- helpers
def finish(obj, material=None, bevel=0.0, smooth=True):
    if material:
        obj.data.materials.append(material)
    if bevel > 0:
        mod = obj.modifiers.new("soft edges", 'BEVEL')
        mod.width = bevel
        mod.segments = 2
    if smooth:
        for p in obj.data.polygons:
            p.use_smooth = True
    MODEL.append(obj)
    return obj

def box(name, loc, dims, material, bevel=0.004):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = name
    o.dimensions = dims
    # In Blender 4.2 this ops call applies the whole transform; bake
    # deliberately (origin -> world origin, verts in world coords).
    # Never set rotation_euler on the result.
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return finish(o, material, bevel=bevel, smooth=False)

def ellipsoid(name, loc, radii, material, rot=(0,0,0), seg=24, ring=18):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=ring, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = radii
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return finish(o, material, smooth=True)

def limb(name, p1, p2, r1, r2, material, joint_r=None):
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    length = d.length
    bpy.ops.mesh.primitive_cone_add(vertices=20, radius1=r1, radius2=r2,
                                    depth=length, location=(p1 + p2) / 2)
    o = bpy.context.active_object
    o.name = name
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = d.to_track_quat('Z', 'Y')
    out = finish(o, material, smooth=True)
    if joint_r:
        s = ellipsoid(name + " joint", tuple(p2), (joint_r, joint_r, joint_r), material)
        out = [out, s]
    return out

def face_place(side):
    """Return (place_fn, dims_fn) mapping local face coords (x along face,
    y outward, z up) to world for face `side` (0:+Y 1:+X 2:-Y 3:-X)."""
    a = math.radians(90 * side)
    rot = Matrix.Rotation(a, 4, 'Z')
    def place(local):
        v = rot @ Vector(local)
        return (v.x, v.y, v.z)
    def dims(d):
        return (d[1], d[0], d[2]) if side % 2 == 1 else d
    return place, dims

# ================================================================ PEDESTAL
# Heights (m) read from the enlarged photograph; pedestal total 2.15 m
# against assumed life-size figures of 1.65 m. See NOTES.md.
PED_TOP = 2.15
box("base step",  (0, 0, 0.03), (1.46, 1.46, 0.06), BASE_M, 0.006)
box("base block", (0, 0, 0.29), (1.32, 1.32, 0.46), BASE_M, 0.008)
box("base bead",  (0, 0, 0.535), (1.37, 1.37, 0.03), STONE_D, 0.006)
BODY_W = 0.94
box("body core", (0, 0, (0.55 + 1.93) / 2), (BODY_W, BODY_W, 1.93 - 0.55), STONE, 0.006)

# --- meander (Greek key) band at the bottom of the body, all four faces ---
# Bold squared-spiral units between two rails, as in the photograph;
# corner squares close the band at each corner.
for side in range(4):
    place, dims = face_place(side)
    for rail_z in (0.578, 0.702):
        box("key rail", place((0, BODY_W/2 + 0.008, rail_z)), dims((0.84, 0.018, 0.024)), STONE_D, 0.0)
    for i in range(8):
        x0 = -0.40 + i * 0.10
        box("key top",  place((x0 + 0.043, BODY_W/2 + 0.010, 0.678)), dims((0.088, 0.020, 0.026)), STONE_D, 0.0)
        box("key drop", place((x0 + 0.074, BODY_W/2 + 0.010, 0.640)), dims((0.026, 0.020, 0.076)), STONE_D, 0.0)
        box("key mid",  place((x0 + 0.043, BODY_W/2 + 0.010, 0.604)), dims((0.062, 0.020, 0.026)), STONE_D, 0.0)
    for sx in (-1, 1):  # corner squares of the band
        box("key corner", place((sx * 0.415, BODY_W/2 + 0.010, 0.640)),
            dims((0.075, 0.022, 0.115)), STONE_D, 0.0)

def ring(name, loc, R, tube, material, rot):
    bpy.ops.mesh.primitive_torus_add(major_segments=14, minor_segments=6,
                                     major_radius=R, minor_radius=tube,
                                     location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return finish(o, material, smooth=True)

# --- carved panel: frame, cartouche with central plaque, corner scrolls ---
for side in range(4):
    place, dims = face_place(side)
    a = math.radians(90 * side)
    cz = 1.32
    box("panel", place((0, BODY_W/2 + 0.004, cz)), dims((0.64, 0.016, 0.80)), STONE_D, 0.003)
    for sgn in (-1, 1):
        box("panel rail v", place((sgn * 0.345, BODY_W/2 + 0.006, cz)), dims((0.03, 0.02, 0.86)), STONE_D, 0.003)
        box("panel rail h", place((0, BODY_W/2 + 0.006, cz + sgn * 0.415)), dims((0.66, 0.02, 0.03)), STONE_D, 0.003)
    # cartouche: oval shield (flat axis pointing OUT of the face) + plaque
    ellipsoid("cartouche", place((0, BODY_W/2 + 0.022, cz + 0.02)), (0.155, 0.030, 0.205),
              STONE, rot=(0, 0, a), seg=16, ring=12)
    box("plaque", place((0, BODY_W/2 + 0.034, cz + 0.02)), dims((0.15, 0.018, 0.21)), STONE_D, 0.002)
    # corner scrolls: small rings lying in the face plane
    ring_rot = (math.pi / 2, 0, 0) if side % 2 == 0 else (0, math.pi / 2, 0)
    for sx in (-1, 1):
        for sy in (-1, 1):
            ring("scroll ring", place((sx * 0.255, BODY_W/2 + 0.016, cz + sy * 0.305)),
                 0.034, 0.012, STONE, ring_rot)
    # swag above the panel, under the cap
    for i in range(9):
        t = i / 8.0
        x = -0.26 + t * 0.52
        z = 1.845 - math.sin(t * math.pi) * 0.07
        r = 0.022 + 0.011 * math.sin(t * math.pi)
        ellipsoid("swag bead", place((x, BODY_W/2 + 0.018, z)), (r, r * 0.7, r), STONE, seg=10, ring=8)
    for sgn in (-1, 1):
        ellipsoid("rosette", place((sgn * 0.28, BODY_W/2 + 0.02, 1.845)), (0.040, 0.022, 0.040), STONE, seg=12, ring=9)

# corner pilasters
for sx in (-1, 1):
    for sy in (-1, 1):
        box("corner pilaster", (sx * (BODY_W/2 - 0.005), sy * (BODY_W/2 - 0.005), 1.24),
            (0.105, 0.105, 1.38), STONE, 0.005)
        box("pilaster cap", (sx * (BODY_W/2 - 0.005), sy * (BODY_W/2 - 0.005), 1.905),
            (0.135, 0.135, 0.05), STONE_D, 0.004)

# cap / cornice
box("necking", (0, 0, 1.955), (1.00, 1.00, 0.05), STONE_D, 0.004)
box("cornice low", (0, 0, 2.02), (1.10, 1.10, 0.08), STONE, 0.008)
box("cornice high", (0, 0, 2.105), (1.24, 1.24, 0.09), STONE, 0.010)
# group plinth slab
box("group plinth", (0, 0, PED_TOP + 0.03), (1.24, 0.78, 0.06), STONE, 0.008)
PLINTH_TOP = PED_TOP + 0.06

# ================================================================ FIGURES
FIG_H = 1.65

def build_body(prefix):
    """Stylised female figure facing +Y in local space, feet at z=0.
    No arms (posed later in world space)."""
    parts = []
    def E(name, loc, radii, rot=(0,0,0)):
        parts.append(ellipsoid(prefix + " " + name, loc, radii, MARBLE, rot))
    def L(name, p1, p2, r1, r2, jr=None):
        r = limb(prefix + " " + name, p1, p2, r1, r2, MARBLE, jr)
        parts.extend(r if isinstance(r, list) else [r])
    for s in (-1, 1):
        L("thigh", (s*0.088, 0.005, 0.88), (s*0.078, 0.012, 0.48), 0.082, 0.056, 0.055)
        L("calf",  (s*0.078, 0.012, 0.48), (s*0.072, -0.012, 0.105), 0.052, 0.030, 0.030)
        E("foot", (s*0.072, 0.055, 0.038), (0.034, 0.105, 0.034))
    E("pelvis", (0, 0, 0.955), (0.152, 0.104, 0.098))
    E("waist",  (0, 0, 1.075), (0.118, 0.082, 0.085))
    E("chest",  (0, 0.004, 1.225), (0.146, 0.094, 0.105))
    for s in (-1, 1):
        E("breast", (s*0.062, 0.074, 1.225), (0.047, 0.042, 0.047))
    L("neck", (0, 0.002, 1.33), (0, 0.004, 1.42), 0.042, 0.038)
    E("head", (0, 0.006, 1.535), (0.082, 0.088, 0.105))
    E("hair cap", (0, -0.014, 1.562), (0.087, 0.090, 0.102))
    E("hair bun", (0, -0.082, 1.60), (0.044, 0.042, 0.044))
    return parts

def add_arm(parts, prefix, side_name, shoulder, elbow, hand, upper_r=0.045, fore_r=0.036):
    r = limb(prefix + " " + side_name + " upper", shoulder, elbow, upper_r, fore_r, MARBLE, 0.040)
    parts.extend(r if isinstance(r, list) else [r])
    r = limb(prefix + " " + side_name + " fore", elbow, hand, fore_r, 0.027, MARBLE, 0.030)
    parts.extend(r if isinstance(r, list) else [r])
    parts.append(ellipsoid(prefix + " " + side_name + " hand", hand, (0.027, 0.036, 0.027), MARBLE))

def lathe_mesh(prefix, rings, matrix, hem_raise_side=0.0, phase=0.0):
    """Folded lathe garment. rings: list of (z, radius). The hem (last ring)
    can be raised on one side (hem_raise_side: -1 raises at local -X)."""
    seg = 40
    verts, faces = [], []
    nr = len(rings)
    for ri, (z, r0) in enumerate(rings):
        amp = 0.02 + (1.32 - z) * 0.045
        for i in range(seg):
            th = 2 * math.pi * i / seg
            fold = 1.0 + amp * math.sin(th * 9 + phase + ri * 0.6)
            zz = z
            if hem_raise_side and ri >= nr - 2:
                s = math.sin(th) * hem_raise_side   # >0 on the raised side
                zz += 0.11 * max(0.0, s) ** 2 * (1.0 if ri == nr - 1 else 0.45)
            r = r0 * fold
            verts.append((r * math.sin(th), r * math.cos(th) * 0.84, zz))
    for ri in range(nr - 1):
        for i in range(seg):
            a = ri * seg + i; b = ri * seg + (i + 1) % seg
            c = (ri + 1) * seg + i; d = (ri + 1) * seg + (i + 1) % seg
            faces.append((a, c, d, b))
    me = bpy.data.meshes.new(prefix)
    me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new(prefix, me)
    bpy.context.collection.objects.link(o)
    o.matrix_world = matrix
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    o.select_set(False)
    return finish(o, MARBLE, smooth=True)

def cloth_fall(prefix, top):
    """Drapery hanging from a hand: narrow flared, folded fall (world coords)."""
    rings = [(0.0, 0.020), (-0.12, 0.034), (-0.24, 0.052), (-0.34, 0.070)]
    seg = 20
    verts, faces = [], []
    for ri, (dz, r0) in enumerate(rings):
        for i in range(seg):
            th = 2 * math.pi * i / seg
            fold = 1.0 + 0.07 * math.sin(th * 6 + ri)
            r = r0 * fold
            verts.append((top[0] + r * math.sin(th), top[1] + r * math.cos(th) * 0.7, top[2] + dz))
    for ri in range(len(rings) - 1):
        for i in range(seg):
            a = ri * seg + i; b = ri * seg + (i + 1) % seg
            c = (ri + 1) * seg + i; d = (ri + 1) * seg + (i + 1) % seg
            faces.append((a, c, d, b))
    me = bpy.data.meshes.new(prefix + " cloth")
    me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new(prefix + " cloth", me)
    bpy.context.collection.objects.link(o)
    return finish(o, MARBLE, smooth=True)

# Arrangement read from the photograph: a front pair (left figure in strong
# profile facing the group; front figure facing front-left, fully draped,
# sash across the torso) and a third figure behind, head and shoulders
# showing. NOT the Canova arrangement — see NOTES.md.
PLACEMENTS = [
    ("grace left",  -0.315,  0.030, -68.0, -1.0),   # name, x, y, facing, hem_raise_side
    ("grace front",  0.085,  0.115,  28.0,  0.0),
    ("grace rear",   0.300, -0.155,   8.0,  0.0),
]
def place_matrix(x, y, deg):
    m = Matrix.Rotation(math.radians(deg), 4, 'Z')
    m.translation = Vector((x, y, PLINTH_TOP))
    return m

GOWN_RINGS = [(1.360, 0.150), (1.315, 0.158), (1.24, 0.140), (1.10, 0.146),
              (0.95, 0.156), (0.75, 0.168), (0.55, 0.182), (0.35, 0.196),
              (0.16, 0.207), (0.075, 0.215)]

world_shoulders = {}
figure_parts = {}
for name, x, y, deg, hem in PLACEMENTS:
    m = place_matrix(x, y, deg)
    parts = build_body(name)
    for o in parts:
        o.matrix_world = m @ o.matrix_world
    for s, key in ((-1, 'L'), (1, 'R')):
        world_shoulders[(name, key)] = m @ Vector((s * 0.168, 0.0, 1.385))
    figure_parts[name] = parts
    # the gown: full-length drapery, as the photograph shows
    figure_parts[name].append(lathe_mesh(name + " gown", GOWN_RINGS, m,
                                         hem_raise_side=hem, phase=deg))

def S(fig, side):
    return world_shoulders[(fig, side)]

def link_arm(fig, side, hand, bow=0.04):
    sh = S(fig, side)
    elbow = (sh + hand) / 2 + Vector((math.copysign(bow, (hand - sh).x if abs((hand - sh).x) > 0.02 else sh.x), -0.02, -0.02))
    add_arm(figure_parts[fig], fig, side, tuple(sh), tuple(elbow), tuple(hand))

def hang_arm(fig, side, drop=(0.0, 0.0), cloth=False):
    sh = S(fig, side)
    hand = sh + Vector((drop[0], drop[1], -0.52))
    elbow = (sh + hand) / 2 + Vector((math.copysign(0.035, sh.x if sh.x else 1), 0.01, 0.0))
    add_arm(figure_parts[fig], fig, side, tuple(sh), tuple(elbow), tuple(hand))
    if cloth:
        figure_parts[fig].append(cloth_fall(fig, tuple(hand + Vector((0, 0, 0.01)))))
    return hand

# linked arms across shoulders (hands rest on top of the neighbour's shoulder)
link_arm("grace left",  'R', S("grace front", 'L') + Vector((0, 0, 0.045)))
link_arm("grace front", 'L', S("grace left",  'R') + Vector((0, 0, 0.045)))
link_arm("grace rear",  'L', S("grace front", 'R') + Vector((0, 0, 0.045)), bow=0.06)
# outer arms hang; the left and front figures hold drapery, as in the photo
hang_arm("grace left",  'L', drop=(-0.08, 0.02), cloth=True)
hang_arm("grace front", 'R', drop=(0.10, 0.05), cloth=True)
hang_arm("grace rear",  'R', drop=(0.09, -0.04), cloth=False)
# NOTE: no torso sashes — the photograph hints at diagonal drapery on the
# front figure, but at this evidence level a sash read as an artefact in
# test renders; the gown's chest overfold carries the drapery emphasis.

# join each figure's body parts into ONE voxel-unified mesh (gown and
# cloth falls stay separate marble pieces of the same figure)
for name, x, y, deg, hem in PLACEMENTS:
    parts = figure_parts[name]
    remesh_parts = [o for o in parts if not any(k in o.name for k in ("gown", "cloth"))]
    bpy.ops.object.select_all(action='DESELECT')
    for o in remesh_parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = remesh_parts[0]
    bpy.ops.object.join()
    body = bpy.context.view_layer.objects.active
    body.name = name + " body"
    mod = body.modifiers.new("unify", 'REMESH')
    mod.mode = 'VOXEL'
    mod.voxel_size = 0.023
    mod.use_smooth_shade = True
    bpy.ops.object.modifier_apply(modifier="unify")

# joined parts no longer exist separately: rebuild the model list
MODEL = [o for o in bpy.data.objects if o.type == 'MESH']

# bake every model object's transform (origin at base centre, scale applied)
bpy.ops.object.select_all(action='DESELECT')
for o in MODEL:
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    o.select_set(False)

# apply remaining modifiers (edge bevels) so counts match the delivered mesh
for o in MODEL:
    bpy.context.view_layer.objects.active = o
    for mod in list(o.modifiers):
        bpy.ops.object.modifier_apply(modifier=mod.name)

# ---------------------------------------------------------------- tri count
def tri_count(objs):
    total = 0
    for o in objs:
        if o.type == 'MESH':
            o.data.calc_loop_triangles()
            total += len(o.data.loop_triangles)
    return total

TRIS = tri_count(MODEL)
print("MODEL OBJECTS:", len(MODEL))
print("TRIANGLES:", TRIS)
print("DIMENSIONS: total height %.2f m (pedestal %.2f + plinth 0.06 + figures %.2f)"
      % (PLINTH_TOP + FIG_H, PED_TOP, FIG_H))

# ---------------------------------------------------------------- save/export
for o in MODEL:
    o.select_set(True)
bpy.context.view_layer.objects.active = MODEL[0]
blend_path = os.path.join(ROOT, "the-three-graces.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
glb_path = os.path.join(ROOT, "the-three-graces.glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB', use_selection=True)
print("SAVED", blend_path, "and", glb_path)
with open(os.path.join(HERE, "build_stats.txt"), "w") as f:
    f.write("triangles=%d\nobjects=%d\ntotal_height=%.2f\n" % (TRIS, len(MODEL), PLINTH_TOP + FIG_H))
