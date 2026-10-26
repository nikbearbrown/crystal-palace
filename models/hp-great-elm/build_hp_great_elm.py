#!/usr/bin/env python3
"""
Build script — hp-great-elm  (v2)
A procedural mature English elm (Ulmus procera) in full summer leaf,
of the kind enclosed under the Hyde Park transept vault in 1851.

GENERIC PROP: this is not a portrait of any specific elm. The
transept views cannot capture an individual tree; the model is an
art-directed procedural elm whose overall proportions are estimated
from the views listed in refs/REFERENCES.md (chiefly H. F. Talbot's
1851 calotype "View of transept, looking south").

Height estimate: in the Talbot view the elm stands at the far end of
the transept, against the end wall whose arch crown is the transept
vault crown, 102 ft 2 in (31.16 m) above the floor (1856 guide table,
Hyde Park). Measured on the image (normalised plate coordinates):
arch crown y=135, elm canopy top y=218, floor at the tree y=424.
Elm height = (424-218)/(424-135) x 31.16 m = 22.2 m -> built 22.0 m.
Canopy/roof clearance is UNRESOLVED in the storyboard; this prop
must not be used to "prove" transept clearance (see NOTES.md).

Re-runnable:  blender -b --python build_hp_great_elm.py
Seeded (random.Random(1851)) so re-runs produce the same tree.
Produces hp-great-elm.blend, hp-great-elm.glb and renders/*.png in
this script's directory. Metres throughout. Origin at base centre.
"""
import bpy
import os
import math
import random
from mathutils import Vector, Matrix

FT = 0.3048

# ------------------------------------------------------------ dimensions
# All values are ESTIMATES for a generic mature elm (see header/NOTES).
TOTAL_H   = 22.0        # m, estimated from Talbot view proportions
CROWN_BOT = 8.8         # m, lowest hanging foliage (skirt)
SPREAD    = 18.5        # m, crown width (fits the 72 ft transept bay)
TRUNK_R0  = 0.98        # m, base radius
TRUNK_R1  = 0.52        # m, radius at top of bole

BASE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(1851)

def log(msg):
    print(msg, flush=True)

# ---------------------------------------------------------------- helpers
def look_at(obj, target):
    obj.rotation_mode = 'QUATERNION'
    direction = Vector(target) - obj.location
    obj.rotation_quaternion = direction.to_track_quat('-Z', 'Y')

def flat_material(name, rgb, rough=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return m

# ---------------------------------------------------------------- scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

model_col = bpy.data.collections.new("Model")
scene.collection.children.link(model_col)
setup_col = bpy.data.collections.new("RenderSetup")
scene.collection.children.link(setup_col)

# ------------------------------------------------------------- materials
bark_mat  = flat_material("BarkGreyBrown", (0.115, 0.092, 0.072), rough=1.0)
leaf_mid  = flat_material("LeafMid",  (0.098, 0.218, 0.052), rough=1.0)
leaf_sun  = flat_material("LeafSun",  (0.185, 0.325, 0.088), rough=1.0)
leaf_deep = flat_material("LeafDeep", (0.045, 0.102, 0.030), rough=1.0)

# ------------------------------------------------------- tube generation
bark_verts = []
bark_faces = []

def add_tube(nodes, radial_segs, flutes=None):
    """nodes: list of (Vector, radius); flutes: optional per-node
    fluting amplitude (vertical grooves, elm-trunk character)."""
    rings = []
    n = len(nodes)
    for i, (p, r) in enumerate(nodes):
        if i == 0:
            tan = nodes[1][0] - nodes[0][0]
        elif i == n - 1:
            tan = nodes[-1][0] - nodes[-2][0]
        else:
            tan = nodes[i + 1][0] - nodes[i - 1][0]
        tan.normalize()
        ref = Vector((0, 0, 1)) if abs(tan.z) < 0.9 else Vector((1, 0, 0))
        side = tan.cross(ref).normalized()
        up = side.cross(tan).normalized()
        fl = flutes[i] if flutes else 0.0
        ring = []
        for j in range(radial_segs):
            a = 2 * math.pi * j / radial_segs
            rr = r
            if fl:
                rr *= 1.0 + fl * math.cos(5 * a + 0.4)
            rr *= 1.0 + 0.045 * math.sin(9.0 * a + 1.7 * p.z + 3.1 * i)
            rr *= 1.0 + 0.038 * math.sin(3.0 * a + 2.0 * p.z + 1.1)
            v = p + (side * math.cos(a) + up * math.sin(a)) * rr
            ring.append(len(bark_verts))
            bark_verts.append(tuple(v))
        rings.append(ring)
    for i in range(n - 1):
        for j in range(radial_segs):
            j2 = (j + 1) % radial_segs
            bark_faces.append((rings[i][j], rings[i][j2],
                               rings[i + 1][j2], rings[i + 1][j]))

def dir_from_angles(azimuth, tilt_from_vertical):
    t = math.radians(tilt_from_vertical)
    return Vector((math.sin(t) * math.cos(azimuth),
                   math.sin(t) * math.sin(azimuth),
                   math.cos(t)))

branch_tips = []   # endpoints, for foliage anchoring
branch_pts = []    # (point, radius) along level>=2 branches

def grow_branch(start, direction, length, r0, r1, level, segs_radial):
    """Branch of 4 segments whose direction arches away from vertical;
    recurses to level 3 (twigs). Records points for foliage."""
    bend = {1: 15.0, 2: 19.0, 3: 22.0}[level]
    steps = 4
    pts = [start.copy()]
    p = start.copy()
    d = direction.copy()
    az = math.atan2(d.y, d.x)
    axis = Vector((-math.sin(az), math.cos(az), 0.0))
    seg_len = length / steps
    for s in range(steps):
        step_tilt = bend * ((s + 1) / steps) ** 2 - bend * (s / steps) ** 2
        d = (Matrix.Rotation(math.radians(step_tilt), 4, axis) @ d).normalized()
        p = p + d * seg_len
        pts.append(p.copy())
    nodes = []
    for i, pt in enumerate(pts):
        f = i / steps
        nodes.append((pt, r0 + (r1 - r0) * f))
    add_tube(nodes, segs_radial)
    branch_tips.append((pts[-1], level))
    if level >= 2:
        for pt, r in nodes[1:]:
            branch_pts.append((pt, r))
    if level >= 3:
        return
    az0 = math.atan2(direction.y, direction.x)
    tilt0 = math.degrees(math.acos(max(-1.0, min(1.0, direction.z))))
    if level == 1:
        plan = [(0.5, 1), (0.8, 1), (1.0, 2)]
    else:
        plan = [(0.45, 1), (0.75, 1), (1.0, 2)]
    for f, count in plan:
        base_pt = pts[min(steps, round(f * steps))]
        base_r = r0 + (r1 - r0) * f
        for s in range(count):
            az = az0 + rng.uniform(-0.85, 0.85) + (s - (count - 1) / 2) * 0.6
            if level == 2 and rng.random() < 0.10:
                tilt = rng.uniform(92, 100)      # drooping outer twig
            else:
                tilt = tilt0 + rng.uniform(8, 28)
            nd = dir_from_angles(az, tilt)
            nl = length * rng.uniform(0.56, 0.68)
            nr0 = base_r * 0.60
            grow_branch(base_pt, nd, nl, nr0, max(0.010, nr0 * 0.28),
                        level + 1, max(4, segs_radial - 1))

# ---------------------------------------------------------------- trunk
trunk_nodes = [(Vector((0, 0, -0.05)), TRUNK_R0 * 1.32),
               (Vector((0, 0, 0.6)), TRUNK_R0 * 1.04),
               (Vector((0.05, 0.02, 2.6)), TRUNK_R0 * 0.90),
               (Vector((0.12, 0.05, 5.2)), TRUNK_R0 * 0.74),
               (Vector((0.25, 0.10, 7.8)), TRUNK_R1)]
trunk_flutes = [0.12, 0.11, 0.08, 0.05, 0.03]
add_tube(trunk_nodes, 14, flutes=trunk_flutes)

# ------------------------------------------------------- scaffold limbs
for i in range(5):
    az = (2 * math.pi * i / 5) + rng.uniform(-0.25, 0.25)
    start_z = 5.9 + 1.5 * rng.random()
    start = Vector((0.20 * math.cos(az), 0.20 * math.sin(az), start_z))
    tilt = rng.uniform(18, 34)                 # vase form, opening out
    d = dir_from_angles(az, tilt)
    grow_branch(start, d, rng.uniform(8.2, 9.8),
                rng.uniform(0.36, 0.42), 0.11, 1, 6)
# central leader, steepest and longest
d = dir_from_angles(rng.uniform(0, 6.28), rng.uniform(4, 10))
grow_branch(Vector((0.10, 0.05, 7.4)), d, 10.4, 0.38, 0.10, 1, 6)

bark_mesh = bpy.data.meshes.new("BarkMesh")
bark_mesh.from_pydata(bark_verts, [], bark_faces)
bark_mesh.update()
for poly in bark_mesh.polygons:
    poly.use_smooth = True
bark_obj = bpy.data.objects.new("ElmBark", bark_mesh)
model_col.objects.link(bark_obj)
bark_mesh.materials.append(bark_mat)
log(f"HP-GREAT-ELM bark tubes done: tips={len(branch_tips)} "
    f"branch_pts={len(branch_pts)}")

# ---------------------------------------------------- foliage clusters
# A small set of reusable cluster meshes (instancing-friendly): an
# icosphere subdivided once (80 tris), displaced by smooth noise plus
# per-vertex hash jitter (leafy breakup), flattened and stretched.
# Instances share mesh data; transforms are location + rotation only
# (scale exactly 1.0 — size variety is baked into the variants).
def icosphere():
    t = (1.0 + math.sqrt(5.0)) / 2.0
    verts = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
             (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
             (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    verts = [Vector(v).normalized() for v in verts]
    faces = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
             (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
             (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
             (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    cache = {}
    def midpoint(a, b):
        key = (min(a, b), max(a, b))
        if key not in cache:
            cache[key] = len(verts)
            verts.append((verts[a] + verts[b]).normalized())
        return cache[key]
    new_faces = []
    for a, b, c in faces:
        ab, bc, ca = midpoint(a, b), midpoint(b, c), midpoint(c, a)
        new_faces += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
    return verts, new_faces

def hash_jitter(v):
    h = math.sin(v.x * 127.1 + v.y * 311.7 + v.z * 74.7) * 43758.5453
    return (h - math.floor(h)) - 0.5

def make_cluster_mesh(idx, radius, mat, stretch_x):
    verts, faces = icosphere()
    s1, s2, s3 = (rng.uniform(0, 6.28) for _ in range(3))
    out = []
    for v in verts:
        n = (1.0 + 0.20 * math.sin(3.1 * v.x + s1) * math.cos(2.7 * v.y + s2)
             + 0.15 * math.sin(4.3 * v.z + s3)
             + 0.46 * hash_jitter(v))
        p = v * (radius * n)
        out.append((p.x * stretch_x, p.y * rng.uniform(0.90, 1.10),
                    p.z * 0.60))
    mesh = bpy.data.meshes.new(f"LeafCluster{idx:02d}Mesh")
    mesh.from_pydata(out, [], faces)
    mesh.update()
    # flat shading: facets read as leafy breakup at film distance,
    # where smooth-shaded blobs read as balloons
    for poly in mesh.polygons:
        poly.use_smooth = False
    mesh.materials.append(mat)
    return mesh

outer_variants = []
for i in range(12):
    radius = (0.50, 0.70, 0.92)[i % 3]
    mat = leaf_sun if i % 2 else leaf_mid
    outer_variants.append(make_cluster_mesh(i, radius, mat,
                                            rng.uniform(1.15, 1.45)))
deep_variants = []
for i in range(4):
    deep_variants.append(make_cluster_mesh(30 + i, 0.78, leaf_deep, 1.25))

CLUSTER_CAP = 560          # keeps the instanced total under ~50k tris
_count = [0]

def place_cluster(pool, loc, name, slack=1.18):
    if _count[0] >= CLUSTER_CAP:
        return None
    # clamp to the crown volume: no strays floating outside the fan
    x, y, z = loc
    rr = math.hypot(x, y)
    if z > 21.9 or rr > crown_halfwidth(min(z, 22.0)) * slack + 0.6:
        return None
    obj = bpy.data.objects.new(name, pool[rng.randrange(len(pool))])
    model_col.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = (rng.uniform(0, 6.28), rng.uniform(0, 6.28),
                          rng.uniform(0, 6.28))
    _count[0] += 1
    return obj

def crown_halfwidth(z):
    pts = [(8.8, 3.0), (11.0, 5.4), (13.0, 7.0), (15.0, 8.2),
           (17.0, 9.0), (19.0, 9.3), (20.5, 8.6), (21.5, 7.0),
           (22.0, 4.8)]
    if z <= pts[0][0]:
        return pts[0][1]
    for (z0, w0), (z1, w1) in zip(pts, pts[1:]):
        if z <= z1:
            return w0 + (w1 - w0) * (z - z0) / (z1 - z0)
    return pts[-1][1]

def az_lobe(az):
    """Lobed crown outline — several sub-crowns, not a perfect fan."""
    return 1.0 + 0.09 * math.sin(3 * az + 1.3) + 0.06 * math.sin(7 * az + 4.1)

n_clusters = 0
# outer shell — the visible surface of the fan
for i in range(165):
    z = 9.6 + 12.2 * (rng.random() ** 0.72)
    az = rng.uniform(0, 2 * math.pi)
    r = crown_halfwidth(z) * az_lobe(az) * rng.uniform(0.80, 1.0)
    place_cluster(outer_variants,
                  (r * math.cos(az), r * math.sin(az), z),
                  f"Leaf_{n_clusters:03d}")
    n_clusters += 1
# mid layer — fills the gaps behind the shell so the crown reads solid
for i in range(70):
    z = 10.2 + 11.4 * (rng.random() ** 0.8)
    az = rng.uniform(0, 2 * math.pi)
    r = crown_halfwidth(z) * rng.uniform(0.52, 0.78)
    place_cluster(outer_variants,
                  (r * math.cos(az), r * math.sin(az), z),
                  f"Leaf_{n_clusters:03d}")
    n_clusters += 1
# top cap
for i in range(30):
    z = rng.uniform(19.4, 21.8)
    az = rng.uniform(0, 2 * math.pi)
    r = crown_halfwidth(z) * rng.uniform(0.1, 0.85)
    place_cluster(outer_variants,
                  (r * math.cos(az), r * math.sin(az), z),
                  f"Leaf_{n_clusters:03d}")
    n_clusters += 1
# hanging skirt at the crown's lower edge
for i in range(28):
    z = rng.uniform(8.6, 11.6)
    az = rng.uniform(0, 2 * math.pi)
    r = crown_halfwidth(z) * az_lobe(az) + rng.uniform(0.0, 0.4)
    place_cluster(outer_variants,
                  (r * math.cos(az), r * math.sin(az), z - 0.3),
                  f"Leaf_{n_clusters:03d}")
    n_clusters += 1
# dark interior fill (depth behind the shell)
for i in range(36):
    z = rng.uniform(11.5, 19.5)
    az = rng.uniform(0, 2 * math.pi)
    r = crown_halfwidth(z) * rng.uniform(0.22, 0.52)
    place_cluster(deep_variants,
                  (r * math.cos(az), r * math.sin(az), z),
                  f"Leaf_{n_clusters:03d}")
    n_clusters += 1
# foliage hung on the branches themselves (outer halves + tips), so
# the limb structure carries leaves instead of floating under a shell
for pt, r in branch_pts:
    if pt.z > 10.5 and rng.random() < 0.26:
        off = Vector((rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5),
                      rng.uniform(-0.2, 0.45)))
        place_cluster(outer_variants, tuple(pt + off),
                      f"Leaf_{n_clusters:03d}")
        n_clusters += 1
for pt, level in branch_tips:
    if pt.z > 9.5 and (level >= 2 or rng.random() < 0.5) \
            and rng.random() < 0.85:
        # looser clamp for tip clusters: they cap the twig ends, so a
        # twig is never left bare against the sky
        place_cluster(outer_variants, (pt.x, pt.y, pt.z + 0.2),
                      f"Leaf_{n_clusters:03d}", slack=1.35)
        n_clusters += 1
n_clusters = _count[0]
log(f"HP-GREAT-ELM clusters placed: {n_clusters}")

# ---------------------------------------------------------- render setup
def box(name, centre, size, material, collection):
    cx, cy, cz = centre
    sx, sy, sz = size[0] / 2, size[1] / 2, size[2] / 2
    verts = [(cx + dx, cy + dy, cz + dz)
             for dx in (-sx, sx) for dy in (-sy, sy) for dz in (-sz, sz)]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1),
             (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    if material:
        mesh.materials.append(material)
    return obj

bg_mat = flat_material("BackdropGrey", (0.52, 0.52, 0.52), rough=1.0)
box("Backdrop", (0, 0, -0.002), (170, 170, 0.002), bg_mat, setup_col)

world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)
bg.inputs[1].default_value = 0.85

sun_data = bpy.data.lights.new("Sun", 'SUN')
sun_data.energy = 3.0
sun_data.angle = 0.35
sun = bpy.data.objects.new("Sun", sun_data)
setup_col.objects.link(sun)
sun.location = (14, -10, 26)
look_at(sun, (0, 0, 0))

fill_data = bpy.data.lights.new("Fill", 'AREA')
fill_data.energy = 1400
fill_data.shape = 'DISK'
fill_data.size = 18
fill = bpy.data.objects.new("Fill", fill_data)
setup_col.objects.link(fill)
fill.location = (-16, 12, 16)
look_at(fill, (0, 0, 8))

def make_camera(name, loc, target, ortho=None, lens=55):
    data = bpy.data.cameras.new(name)
    if ortho:
        data.type = 'ORTHO'
        data.ortho_scale = ortho
    else:
        data.type = 'PERSP'
        data.lens = lens
    cam = bpy.data.objects.new(name, data)
    setup_col.objects.link(cam)
    cam.location = loc
    look_at(cam, target)
    return cam

mid = (0, 0, 10.8)
cam_front = make_camera("CamFront", (0, -80, 10.8), mid, ortho=33)
cam_side  = make_camera("CamSide", (80, 0, 10.8), mid, ortho=33)
cam_tq    = make_camera("CamThreeQuarter", (26, -35, 18),
                        (0, 0, 10.2), lens=40)

# ------------------------------------------------------------- rendering
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.cycles.use_denoising = True
try:
    scene.cycles.device = 'CPU'
except Exception:
    pass
scene.render.resolution_x = 960
scene.render.resolution_y = 720
scene.render.film_transparent = False

os.makedirs(os.path.join(BASE, "renders"), exist_ok=True)
_skip = set(filter(None, os.environ.get("HPGE_SKIP", "").split(",")))
for cam, fname in ((cam_front, "front.png"),
                   (cam_side, "side.png"),
                   (cam_tq, "three-quarter.png")):
    if fname in _skip:
        continue
    log(f"HP-GREAT-ELM rendering {fname} ...")
    scene.camera = cam
    scene.render.filepath = os.path.join(BASE, "renders", fname)
    bpy.ops.render.render(write_still=True)
    log(f"HP-GREAT-ELM rendered {fname}")

# ------------------------------------------------------ save + GLB export
blend_path = os.path.join(BASE, "hp-great-elm.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
log("HP-GREAT-ELM blend saved")

bpy.ops.object.select_all(action='DESELECT')
tris = 0
for obj in model_col.objects:
    obj.select_set(True)
    if obj.type == 'MESH':
        obj.data.calc_loop_triangles()
        tris += len(obj.data.loop_triangles)
bpy.context.view_layer.objects.active = bark_obj
glb_path = os.path.join(BASE, "hp-great-elm.glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB',
                          use_selection=True, export_yup=True)
log("HP-GREAT-ELM glb exported")

log(f"HP-GREAT-ELM objects={len(model_col.objects)} "
    f"clusters={n_clusters} branch_tips={len(branch_tips)}")
log(f"HP-GREAT-ELM triangles={tris} (instanced total)")
log(f"HP-GREAT-ELM height={TOTAL_H:.1f} m spread={SPREAD:.1f} m "
    f"— ESTIMATES, generic elm, see NOTES.md")
