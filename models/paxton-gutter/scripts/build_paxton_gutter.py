#!/usr/bin/env python3
"""Build the Paxton gutter + main gutter prop (Crystal Palace, Hyde Park 1851).

Sources: Downes (1852) Plate XII Fig. 10 (Paxton gutter section, printed dims)
and Fig. 3 (elevation / bar-notch chain); Plate XIII Figs. 2, 4, 5, 7
(main gutter sections + 24 ft span elevation).

Two pieces in one scene, in separate collections:
  Paxton_Gutter_24ft - one 24 ft bay length of the timber Paxton gutter
  Main_Gutter_24ft   - one 24 ft span length of the Plate XIII main gutter
Length along X, width along Y, Z up. Origin at base centre of the pair.
Units: metres. Blender 4.2.
"""
import bpy
import bmesh
from mathutils import Vector

IN = 0.0254
BAY = 24 * 12 * IN          # 7.3152 m
PAXTON_Y = -0.46            # centreline offsets so the pair sits side by side
MAIN_Y = 0.46

# ---------------------------------------------------------------- materials
def make_mat(name, color, rough=0.85, metal=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m

MAT_PAXTON = make_mat("PaintedTimber_Pale", (0.80, 0.77, 0.70), 0.8)
MAT_MAIN = make_mat("Timber_Mid", (0.46, 0.385, 0.30), 0.9)
MAT_IRON = make_mat("Iron_Dark", (0.09, 0.09, 0.095), 0.55, 0.85)

# ---------------------------------------------------------------- helpers
def extrude_profile(name, profile_yz, length, mat, collection, y_off):
    """Prism from a closed (y,z) profile loop, extruded along X, centred."""
    n = len(profile_yz)
    x0, x1 = -length / 2, length / 2
    verts = [(x0, y + y_off, z) for (y, z) in profile_yz] + \
            [(x1, y + y_off, z) for (y, z) in profile_yz]
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    faces.append(tuple(reversed(range(n))))            # cap at x0
    faces.append(tuple(n + i for i in range(n)))       # cap at x1
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    if mat:
        mesh.materials.append(mat)
    return obj

def add_box(name, loc, dims, mat, collection):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collection.objects.link(obj)
    if mat:
        obj.data.materials.append(mat)
    return obj

def add_cyl(name, loc, radius, depth, mat, collection, verts=20):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius,
                                        depth=depth, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collection.objects.link(obj)
    if mat:
        obj.data.materials.append(mat)
    return obj

def new_collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col

# ---------------------------------------------------------------- clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for col in list(bpy.context.scene.collection.children):
    bpy.context.scene.collection.children.unlink(col)

# ================================================================ PAXTON GUTTER
col_px = new_collection("Paxton_Gutter_24ft")

# Profile from Plate XII Fig. 10 (inches). Overall 6 deep, base 5 wide,
# cheeks ~5.7 wide at top, channel 3 wide x 3 deep (printed segments
# 1.25 + 1.75 in), solid 3 below the channel, condensation groove each side
# with its lip 3.25 above the base.
# Extrusion stops at z=5.625; the top 3/8 in of cheek is built as notch strips.
prof_in = [
    (-2.50, 0.00), (2.50, 0.00),
    (2.50, 3.25), (2.05, 3.60), (2.02, 4.05), (2.55, 4.45), (2.82, 4.90),
    (2.85, 5.625),
    (1.50, 5.625),
    (1.49, 4.75), (1.46, 4.35), (1.36, 3.95), (1.16, 3.55), (0.88, 3.25),
    (0.45, 3.05), (0.00, 3.00),
    (-0.45, 3.05), (-0.88, 3.25), (-1.16, 3.55), (-1.36, 3.95),
    (-1.46, 4.35), (-1.49, 4.75), (-1.50, 5.625),
    (-2.85, 5.625), (-2.82, 4.90), (-2.55, 4.45), (-2.02, 4.05),
    (-2.05, 3.60), (-2.50, 3.25),
]
profile = [(y * IN, z * IN) for (y, z) in prof_in]
extrude_profile("PaxtonGutter_Body", profile, BAY, MAT_PAXTON, col_px, PAXTON_Y)

# Bar-notch chain (Plate XII Fig. 3, printed): 5.25 in end margins, 10.5 in
# typical centres, 11.25 in flanking the strong bars at 4 / 12 / 20 ft.
# 27 bars; chain closes exactly (last margin 5.25 in).
strong = {48.0, 144.0, 240.0}
positions = [5.25, 15.75, 26.25, 36.75, 48.0, 59.25, 69.75, 80.25, 90.75,
             101.25, 111.75, 122.25, 132.75, 144.0, 155.25, 165.75, 176.25,
             186.75, 197.25, 207.75, 218.25, 228.75, 240.0, 251.25, 261.75,
             272.25, 282.75]
notches = []           # (centre_in, width_in)
for p in positions:
    notches.append((p, 2.5 if p in strong else 1.0))
edges = [0.0]
for c, w in notches:
    edges += [c - w / 2, c + w / 2]
edges.append(288.0)
segments = [(edges[i], edges[i + 1]) for i in range(0, len(edges) - 1, 2)]

strip_objs = []
for side in (+1, -1):
    yc = side * (1.5 + 2.87) / 2 * IN + PAXTON_Y
    for (a, b) in segments:
        if b - a < 0.05:
            continue
        o = add_box("notch_strip",
                    ((a + b) / 2 * IN - BAY / 2, yc, (5.60 + 6.02) / 2 * IN),
                    ((b - a) * IN, (2.87 - 1.45) * IN, 0.42 * IN),
                    MAT_PAXTON, col_px)
        strip_objs.append(o)
# join strips into one object
bpy.ops.object.select_all(action='DESELECT')
for o in strip_objs:
    o.select_set(True)
bpy.context.view_layer.objects.active = strip_objs[0]
bpy.ops.object.join()
strip_objs[0].name = "PaxtonGutter_NotchStrips"

# ================================================================ MAIN GUTTER
col_mg = new_collection("Main_Gutter_24ft")
# Plate XIII Fig. 2: bottom board E 14 in wide x 2.5 thick; side boards C/D
# 1.375 thick standing 6 in above E (8.5 overall); clear channel 5.25 in;
# outside top width 8 in.
add_box("MainGutter_BottomBoard",
        (0, MAIN_Y, 1.25 * IN),
        (BAY, 14 * IN, 2.5 * IN), MAT_MAIN, col_mg)
for side in (+1, -1):
    yc = MAIN_Y + side * (4.0 - 1.375 / 2) * IN
    add_box("MainGutter_SideBoard",
            (0, yc, 5.5 * IN),
            (BAY, 1.375 * IN, 6.0 * IN), MAT_MAIN, col_mg)
# Fig. 4 cross-tie between the boards at the b.b section (one, at mid-length)
add_box("MainGutter_CrossTie",
        (0, MAIN_Y, 6.1 * IN),
        (2.0 * IN, 5.25 * IN, 1.5 * IN), MAT_MAIN, col_mg)
# Bolt pairs (Fig. 2 pattern): vertical bolt through each side board and the
# bottom board, washer + square nut below. Placed at both ends and at the
# 4 / 12 / 20 ft module centres (spacing inferred - see NOTES).
# Bolt spans z -0.5 in (nut) to 8.7 in (just above the board top at 8.5 in).
bolt_x = [-BAY / 2 + 0.15, -4 * 12 * IN, 0.0, 4 * 12 * IN, BAY / 2 - 0.15]
for bx in bolt_x:
    for side in (+1, -1):
        yc = MAIN_Y + side * (4.0 - 1.375 / 2) * IN
        add_cyl("bolt", (bx, yc, 4.1 * IN), 0.25 * IN, 9.2 * IN,
                MAT_IRON, col_mg, verts=12)
        add_box("bolt_nut", (bx, yc, -0.55 * IN),
                (0.95 * IN, 0.95 * IN, 0.6 * IN), MAT_IRON, col_mg)

# ---------------------------------------------------------------- save
bpy.ops.wm.save_as_mainfile(
    filepath="/home/hatch/workspace/cp-models/paxton-gutter/paxton-gutter.blend")

# ---------------------------------------------------------------- stats
total_tris = 0
report = []
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH' and obj.name != 'Ground':
        n = sum(len(p.vertices) - 2 for p in obj.data.polygons)
        total_tris += n
        report.append(f"{obj.name}: {n} tris, dims {tuple(round(d,4) for d in obj.dimensions)}")
print("\n".join(sorted(report)))
print("TOTAL TRIS (excl. ground):", total_tris)
