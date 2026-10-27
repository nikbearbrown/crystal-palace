#!/usr/bin/env python3
"""Build the Crystal Palace glazing wagon (candidate #31) procedurally.

Source: references/muse-drive/images/commons/Glazing_waggon.png (PD engraving,
3/4 view of Charles Fox's glazing waggon on the Hyde Park roof, crew omitted).

Dimensions are INFERRED - see NOTES.md for the full provenance chain:
  deck 3.66 x 2.44 m (12 x 8 ft; width = one ridge-and-furrow slope module),
  hoop rise 1.50 m scaled from the crew figures, wheels 0.30 m dia, gauge 1.98 m.
"""
import bpy
import math
from mathutils import Vector

# ---------------------------------------------------------------- clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras,
                   bpy.data.lights, bpy.data.materials):
    pass  # leave datablocks; new ones created fresh below

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ---------------------------------------------------------------- materials
def make_mat(name, rgb, rough=0.8, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*rgb, 1.0)
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Metallic'].default_value = metal
    return m

TIMBER_DARK = make_mat('TimberDark', (0.235, 0.155, 0.09), 0.85)
TIMBER_DECK = make_mat('TimberDeck', (0.345, 0.25, 0.145), 0.9)
IRON        = make_mat('IronDark', (0.145, 0.145, 0.155), 0.5, 0.85)
IRON_RUST   = make_mat('IronWheel', (0.225, 0.175, 0.14), 0.62, 0.7)

# ---------------------------------------------------------------- helpers
def box(name, dims, loc, mat, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        ob.data.materials.append(mat)
    if bevel > 0:
        mod = ob.modifiers.new('soft', 'BEVEL')
        mod.width = bevel
        mod.segments = 2
    return ob

def cyl(name, radius, depth, loc, mat, rot=(0, 0, 0), verts=24):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth,
                                        vertices=verts, location=loc,
                                        rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        ob.data.materials.append(mat)
    return ob

def tube_along_points(name, pts, radius, mat, verts=10):
    """Tube mesh swept along a polyline of Vectors (square-ish segments)."""
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = radius
    cu.bevel_resolution = 2
    cu.resolution_u = 1
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for p, co in zip(sp.points, pts):
        p.co = (*co, 1.0)
    ob = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.convert(target='MESH')
    ob = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        ob.data.materials.append(mat)
    ob.select_set(False)
    return ob

# ---------------------------------------------------------------- dimensions
L, W = 3.66, 2.44          # deck length (x, direction of travel), width (y)
DECK_Z = 0.60              # deck top height
BEAM_D = 0.22              # side beam depth
HOOP_RISE = 1.50
WHEEL_R = 0.15
GAUGE_Y = 0.99             # wheel centre |y|  (gauge 1.98 m)
AXLE_X = 1.40              # wheel centre |x|  (wheelbase 2.80 m)

# ---------------------------------------------------------------- deck frame
beam_y = W / 2 - 0.045
for s in (-1, 1):
    box(f'SideBeam_{"L" if s<0 else "R"}', (L, 0.09, BEAM_D),
        (0, s * beam_y, DECK_Z - BEAM_D / 2), TIMBER_DARK, bevel=0.005)
for s in (-1, 1):
    box(f'EndBeam_{"F" if s>0 else "B"}', (0.09, W - 0.18, BEAM_D),
        (s * (L / 2 - 0.045), 0, DECK_Z - BEAM_D / 2), TIMBER_DARK, bevel=0.005)
# cross bearers under planks
for i, fx in enumerate((-0.75, -0.25, 0.25, 0.75)):
    box(f'CrossBearer_{i}', (0.09, W - 0.18, 0.10),
        (fx * L / 1.6, 0, DECK_Z - 0.09), TIMBER_DARK)
# deck planks, lengthwise, small gaps
n_planks, gap = 7, 0.015
pw = (W - 0.18 - gap * (n_planks - 1)) / n_planks
for i in range(n_planks):
    y = -(W - 0.18) / 2 + pw / 2 + i * (pw + gap)
    box(f'Plank_{i:02d}', (L - 0.06, pw, 0.04), (0, y, DECK_Z - 0.02),
        TIMBER_DECK, bevel=0.003)

# ---------------------------------------------------------------- underframe
for s in (-1, 1):
    box(f'LongBearer_{"L" if s<0 else "R"}', (3.30, 0.12, 0.14),
        (0, s * GAUGE_Y, 0.31), TIMBER_DARK, bevel=0.005)
# axles + axle boxes + wheels
for sx in (-1, 1):
    cyl(f'Axle_{sx}', 0.035, 2 * GAUGE_Y + 0.10, (sx * AXLE_X, 0, WHEEL_R),
        IRON, rot=(math.radians(90), 0, 0))
    for sy in (-1, 1):
        box('AxleBox', (0.20, 0.16, 0.16), (sx * AXLE_X, sy * GAUGE_Y, 0.30),
            TIMBER_DARK, bevel=0.005)
        # wheel: plain dished disc read - tyre disc + hub + inner flange ring
        cyl('Wheel', WHEEL_R, 0.05, (sx * AXLE_X, sy * GAUGE_Y, WHEEL_R),
            IRON_RUST, rot=(math.radians(90), 0, 0), verts=28)
        cyl('WheelHub', 0.055, 0.09, (sx * AXLE_X, sy * GAUGE_Y, WHEEL_R),
            IRON, rot=(math.radians(90), 0, 0), verts=16)
        # flange on the inner face
        fdir = -sy
        cyl('WheelFlange', WHEEL_R + 0.018, 0.016,
            (sx * AXLE_X, sy * GAUGE_Y + fdir * 0.033, WHEEL_R),
            IRON_RUST, rot=(math.radians(90), 0, 0), verts=28)

# ---------------------------------------------------------------- hoops
def hoop_points(rise=HOOP_RISE, half=W / 2, z0=DECK_Z, n=25):
    pts = []
    for i in range(n + 1):
        th = -math.pi / 2 + math.pi * i / n
        y = half * math.sin(th)
        z = z0 + rise * math.cos(th)
        pts.append(Vector((0, y, z)))
    return pts

for i, hx in enumerate((-1.50, -0.50, 0.50, 1.50)):
    pts = [Vector((hx, p.y, p.z)) for p in hoop_points()]
    tube_along_points(f'Hoop_{i}', pts, 0.016, IRON)
    # hoop feet: short straps down the deck edge + foot plates
    for s in (-1, 1):
        box('HoopFoot', (0.07, 0.03, 0.12), (hx, s * (W / 2 - 0.02),
            DECK_Z - 0.04), IRON)
# crown bar along the hoop tops
cyl('CrownBar', 0.013, 3.10, (0, 0, DECK_Z + HOOP_RISE), IRON,
    rot=(0, math.radians(90), 0))

# ------------------------------------------------------- end upstand (drawn end)
box('EndUpstand', (0.04, W - 0.10, 0.26), (L / 2 - 0.02, 0, DECK_Z + 0.13),
    TIMBER_DARK, bevel=0.004)
box('EndUpstandLedge', (0.09, W - 0.10, 0.035),
    (L / 2 - 0.02, 0, DECK_Z + 0.275), TIMBER_DECK, bevel=0.004)
for yy in (-0.8, 0.0, 0.8):
    cyl('UpstandBolt', 0.014, 0.055, (L / 2 - 0.02, yy, DECK_Z + 0.13),
        IRON, rot=(0, math.radians(90), 0), verts=10)

# ------------------------------------------------------- side-beam bolt heads (engraving shows a bolted row)
for s in (-1, 1):
    for i, fx in enumerate((-0.83, -0.5, -0.17, 0.17, 0.5, 0.83)):
        cyl('BeamBolt', 0.016, 0.02,
            (fx * 1.95, s * (W / 2 + 0.004), DECK_Z - BEAM_D / 2),
            IRON, rot=(math.radians(90), 0, 0), verts=10)

# ---------------------------------------------------------------- finish
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.ops.object.select_all(action='DESELECT')

# triangle count (evaluated, i.e. modifiers applied, as exported)
dg = bpy.context.evaluated_depsgraph_get()
total_tris = 0
for ob in bpy.context.scene.objects:
    if ob.type == 'MESH':
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        total_tris += len(me.loop_triangles)
        ev.to_mesh_clear()
print(f'TRIANGLES: {total_tris}')
print(f'OBJECTS: {len(bpy.context.scene.objects)}')

bpy.ops.wm.save_as_mainfile(
    filepath='/home/hatch/workspace/cp-models/glazing-wagon/glazing-wagon.blend')

bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(
    filepath='/home/hatch/workspace/cp-models/glazing-wagon/glazing-wagon.glb',
    export_format='GLB', export_apply=True)
print('EXPORTED GLB')
