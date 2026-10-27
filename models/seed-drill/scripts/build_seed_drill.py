#!/usr/bin/env python3
"""Build the 1851 seed drill (candidate #30) for nikbearbrown/crystal-palace.

Type synthesised from the two Talbot calotypes of the Garrett (plate 1) and
Hornsby (plate 2) exhibits, Great Exhibition 1851. Built in metres.
Machine axes: X = across the machine, Y = direction of travel (drawbar +Y),
Z = up, ground at z=0. Origin ends at the centre of the ground footprint.
"""
import bpy
import math
from mathutils import Vector

# ---------------------------------------------------------------- materials
def make_mat(name, color, metallic=0.0, roughness=0.7):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return m

PAINT = make_mat("PaintedIronwood_DarkGreen", (0.045, 0.065, 0.045), 0.15, 0.62)
IRON = make_mat("Iron_Dark", (0.075, 0.075, 0.08), 0.65, 0.52)
STEEL = make_mat("Steel_Worn", (0.32, 0.33, 0.34), 0.85, 0.38)
WOOD = make_mat("Wood_Shafts", (0.045, 0.032, 0.020), 0.0, 0.78)
BRASS = make_mat("Brass_Boss", (0.20, 0.145, 0.05), 0.8, 0.55)

# ---------------------------------------------------------------- helpers
def finish(obj, mat):
    if mat:
        obj.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return obj

def box(name, loc, size, mat, bevel=0.006):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = name
    o.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel > 0:
        mod = o.modifiers.new("bev", 'BEVEL')
        mod.width = bevel
        mod.segments = 1
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.modifier_apply(modifier="bev")
    return finish(o, mat)

def cyl(name, loc, radius, depth, mat, verts=20, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth,
                                        location=loc, rotation=rotation)
    o = bpy.context.active_object
    o.name = name
    return finish(o, mat)

def tube_between(name, p1, p2, r1, r2=None, mat=None, verts=10):
    """Tapered cylinder (cone) spanning p1->p2."""
    p1, p2 = Vector(p1), Vector(p2)
    mid = (p1 + p2) / 2
    d = p2 - p1
    length = d.length
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1,
                                    radius2=r2 if r2 is not None else r1,
                                    depth=length, location=mid)
    o = bpy.context.active_object
    o.name = name
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return finish(o, mat)

def open_tube(name, loc, radius, depth, mat, verts=28, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth,
                                        location=loc, rotation=rotation, end_fill_type='NOTHING')
    o = bpy.context.active_object
    o.name = name
    return finish(o, mat)

def wheel(name, centre, R, tyre_w, n_spokes, hub_r, mat_main, mat_tyre):
    """Spoked wheel in the YZ plane (axle along X)."""
    cx, cy, cz = centre
    rot = (0, math.radians(90), 0)  # cylinder axis -> X
    # iron tyre band
    open_tube(name + "_Tyre", centre, R, tyre_w, mat_tyre, 36, rot)
    # wooden felloe ring just inside tyre
    open_tube(name + "_Felloe", centre, R - 0.028, tyre_w * 0.92, mat_main, 36, rot)
    # hub
    cyl(name + "_Hub", centre, hub_r, tyre_w * 2.1, mat_main, 18, rot)
    cyl(name + "_HubBand", centre, hub_r * 1.04, tyre_w * 0.7, mat_tyre, 18, rot)
    # spokes: tapered, hub -> felloe
    for i in range(n_spokes):
        a = 2 * math.pi * i / n_spokes
        y0 = cy + (hub_r * 0.55) * math.cos(a)
        z0 = cz + (hub_r * 0.55) * math.sin(a)
        y1 = cy + (R - 0.055) * math.cos(a)
        z1 = cz + (R - 0.055) * math.sin(a)
        tube_between(f"{name}_Spoke{i:02d}", (cx, y0, z0), (cx, y1, z1),
                     0.021, 0.016, mat_main, 8)

# ---------------------------------------------------------------- clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
    pass

# ---------------------------------------------------------------- dimensions
WHEEL_R = 0.70          # driving wheels, measured ratio anchor (see NOTES)
AXLE_Z = WHEEL_R
TRACK = 1.94            # wheel centre-to-centre across X
BOX_L = 1.84            # seed box length (X)
BOX_D = 0.52            # seed box depth (Y)
BOX_BOT = 0.88
BOX_TOP = 1.30
LID_RIDGE = 1.415
N_COULTER = 11
COULTER_PITCH = 0.16

# ---------------------------------------------------------------- seed box
box("SeedBox_Body", (0, -0.05, (BOX_BOT + BOX_TOP) / 2), (BOX_L, BOX_D, BOX_TOP - BOX_BOT), PAINT, 0.004)
# panel mouldings: front and rear long faces get a slightly proud panel frame
for sgn, nm in ((1, "Front"), (-1, "Rear")):
    y = -0.05 + sgn * (BOX_D / 2 + 0.006)
    box(f"SeedBox_{nm}Panel", (0, y, 1.09), (BOX_L * 0.94, 0.012, 0.26), PAINT, 0.003)
    # bottom batten strip along each long face (strong line in both plates)
    box(f"SeedBox_{nm}Batten", (0, y, 0.945), (BOX_L * 0.98, 0.014, 0.05), PAINT, 0.003)
# end boards + circular maker's medallion boss (blank: no lettering invented)
for sgn in (1, -1):
    box("SeedBox_End", (sgn * (BOX_L / 2 + 0.008), -0.05, 1.09), (0.016, BOX_D * 0.96, 0.40), PAINT, 0.003)
    cyl("MedallionBoss", (sgn * (BOX_L / 2 + 0.022), -0.05, 1.13), 0.075, 0.018, BRASS, 24,
        (0, math.radians(90), 0))
    cyl("MedallionBossInner", (sgn * (BOX_L / 2 + 0.026), -0.05, 1.13), 0.048, 0.02, BRASS, 24,
        (0, math.radians(90), 0))
# lid: two slabs sloping DOWN from a central ridge running along X
for sgn, nm in ((1, "Front"), (-1, "Rear")):
    lid = box(f"SeedBox_Lid{nm}", (0, -0.05 + sgn * BOX_D / 4, (BOX_TOP + LID_RIDGE) / 2 + 0.004),
              (BOX_L + 0.03, BOX_D / 2 + 0.045, 0.022), PAINT, 0.004)
    lid.rotation_euler = (-sgn * math.radians(13.5), 0, 0)
    bpy.context.view_layer.objects.active = lid
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
# ridge cap strip
box("SeedBox_Ridge", (0, -0.05, LID_RIDGE + 0.012), (BOX_L + 0.03, 0.05, 0.018), PAINT, 0.004)

# seed cups: row of small funnels along the rear face (photo 1) + drop tubes
for i in range(N_COULTER):
    x = (i - (N_COULTER - 1) / 2) * COULTER_PITCH
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.016, radius2=0.034, depth=0.07,
                                    location=(x, -0.05 - BOX_D / 2 - 0.012, 1.16))
    o = bpy.context.active_object
    o.name = "SeedCup"
    finish(o, IRON)

# ---------------------------------------------------------------- frame + axle
cyl("MainAxle", (0, 0, AXLE_Z), 0.038, TRACK + 0.10, IRON, 14, (0, math.radians(90), 0))
for sgn in (1, -1):
    # side rails running fore-aft
    box("FrameRail", (sgn * 0.80, 0.55, 0.80), (0.055, 2.20, 0.075), WOOD, 0.004)
    # axle bearing block
    box("AxleBearing", (sgn * 0.80, 0, 0.74), (0.09, 0.16, 0.14), IRON, 0.004)
    # diagonal brace axle->box rear
    tube_between("FrameBrace", (sgn * 0.80, -0.02, 0.72), (sgn * 0.80, -0.33, 0.92), 0.022, 0.022, IRON, 8)
# cross rails
box("CrossRail_Front", (0, 0.28, 0.82), (1.66, 0.06, 0.06), WOOD, 0.003)
box("CrossRail_Rear", (0, -0.36, 0.80), (1.66, 0.06, 0.06), WOOD, 0.003)

# ---------------------------------------------------------------- driving wheels
wheel("WheelL", (-TRACK / 2, 0, AXLE_Z), WHEEL_R, 0.082, 12, 0.105, WOOD, IRON)
wheel("WheelR", (TRACK / 2, 0, AXLE_Z), WHEEL_R, 0.082, 12, 0.105, WOOD, IRON)

# drive suggestion: gear ring inside right wheel + end gear on the metering
# shaft (the intermediate drive is not resolved in the photographs and is
# represented schematically only -- see NOTES.md)
cyl("DriveGearRing", (TRACK / 2 - 0.075, 0, AXLE_Z), 0.30, 0.03, IRON, 28, (0, math.radians(90), 0))
# metering shaft beneath the box with feed discs
cyl("MeteringShaft", (0, -0.30, 0.94), 0.02, BOX_L * 0.92, IRON, 12, (0, math.radians(90), 0))
cyl("DriveEndGear", (BOX_L * 0.46 + 0.01, -0.30, 0.94), 0.075, 0.025, IRON, 18, (0, math.radians(90), 0))
for i in range(N_COULTER):
    x = (i - (N_COULTER - 1) / 2) * COULTER_PITCH
    cyl("FeedDisc", (x, -0.30, 0.94), 0.045, 0.014, IRON, 14, (0, math.radians(90), 0))

# ---------------------------------------------------------------- coulter bar + coulters
BAR_Y, BAR_Z = -0.40, 0.47
box("CoulterBar", (0, BAR_Y, BAR_Z), (BOX_L * 0.94, 0.055, 0.055), IRON, 0.003)
# hangers from box bottom down to the bar
for xh in (-0.75, -0.25, 0.25, 0.75):
    tube_between("BarHanger", (xh, -0.33, BOX_BOT), (xh, BAR_Y, BAR_Z + 0.03), 0.016, 0.016, IRON, 8)

for i in range(N_COULTER):
    x = (i - (N_COULTER - 1) / 2) * COULTER_PITCH
    grp = f"Coulter{i:02d}"
    # lever shank: from bar pivot down and slightly back to the shoe
    tube_between(grp + "_Shank", (x, BAR_Y, BAR_Z), (x, -0.46, 0.10), 0.020, 0.015, IRON, 8)
    # shoe: flat triangular point (scaled, rotated box)
    shoe = box(grp + "_Shoe", (x, -0.475, 0.075), (0.020, 0.20, 0.09), STEEL, 0.002)
    shoe.rotation_euler = (math.radians(-18), 0, 0)
    bpy.context.view_layer.objects.active = shoe
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    # seed tube: box outlet down behind the shank
    tube_between(grp + "_Tube", (x, -0.325, 1.12), (x, -0.435, 0.16), 0.011, 0.011, IRON, 8)
    # lifting chain: box bottom -> mid shank, with a sag (two segments)
    top = Vector((x, -0.325, BOX_BOT))
    mid = Vector((x, -0.44, 0.42))
    low = Vector((x, -0.435, 0.30))
    tube_between(grp + "_ChainA", top, mid, 0.006, 0.006, IRON, 6)
    tube_between(grp + "_ChainB", mid, low, 0.006, 0.006, IRON, 6)

# ---------------------------------------------------------------- lift lever (photo 1, rear left)
tube_between("LiftLever", (-0.86, -0.30, 0.78), (-0.92, -0.62, 1.52), 0.020, 0.016, IRON, 8)
tube_between("LiftLeverGrip", (-0.92, -0.62, 1.52), (-0.92, -0.70, 1.60), 0.014, 0.014, WOOD, 8)
# quadrant arc suggestion
tube_between("LiftQuadrant", (-0.86, -0.30, 0.80), (-0.88, -0.52, 1.06), 0.010, 0.010, IRON, 6)

# ---------------------------------------------------------------- drawbar + fore-carriage
for sgn in (1, -1):
    tube_between("DrawbarShaft", (sgn * 0.80, 1.58, 0.80), (sgn * 0.26, 3.05, 0.60), 0.030, 0.024, WOOD, 10)
# cross piece at the draught end
box("DrawbarCross", (0, 3.05, 0.60), (0.62, 0.055, 0.055), WOOD, 0.003)
# draught hook hanging below (photo 2)
tube_between("DraughtHook", (0.12, 2.55, 0.62), (0.12, 2.55, 0.42), 0.011, 0.011, IRON, 8)
bpy.ops.mesh.primitive_torus_add(major_radius=0.045, minor_radius=0.011,
                                 major_segments=14, minor_segments=8,
                                 location=(0.12, 2.55, 0.375))
o = bpy.context.active_object
o.name = "DraughtHookRing"
finish(o, IRON)

# fore-carriage: axle + two small 6-spoke wheels + steering post with T handle
FORE_Y = 3.28
cyl("ForeAxle", (0, FORE_Y, 0.33), 0.026, 0.92, IRON, 12, (0, math.radians(90), 0))
wheel("ForeWheelL", (-0.46, FORE_Y, 0.33), 0.33, 0.035, 6, 0.055, IRON, IRON)
wheel("ForeWheelR", (0.46, FORE_Y, 0.33), 0.33, 0.035, 6, 0.055, IRON, IRON)
# fore frame connecting drawbar to fore axle
for sgn in (1, -1):
    tube_between("ForeFrame", (sgn * 0.26, 3.05, 0.60), (sgn * 0.40, FORE_Y, 0.36), 0.022, 0.022, IRON, 8)
# steering post + T handle (photo 2)
tube_between("SteerPost", (0, 3.12, 0.60), (0, 3.12, 1.06), 0.020, 0.020, IRON, 10)
tube_between("SteerHandle", (-0.29, 3.12, 1.06), (0.29, 3.12, 1.06), 0.016, 0.016, WOOD, 8)

# ---------------------------------------------------------------- recentre: origin at footprint centre, ground z=0
bpy.ops.object.select_all(action='SELECT')
objs = list(bpy.context.selected_objects)
min_y = min((o.matrix_world @ Vector(c)).y for o in objs if o.type == 'MESH'
            for c in o.bound_box)
max_y = max((o.matrix_world @ Vector(c)).y for o in objs if o.type == 'MESH'
            for c in o.bound_box)
cy = (min_y + max_y) / 2
for o in objs:
    o.location.y -= cy
bpy.ops.object.select_all(action='DESELECT')

# ---------------------------------------------------------------- report stats
dg = bpy.context.evaluated_depsgraph_get()
tris = 0
n_obj = 0
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        n_obj += 1
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        ev.to_mesh_clear()
xs, ys, zs = [], [], []
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            xs.append(w.x); ys.append(w.y); zs.append(w.z)
print(f"STATS objects={n_obj} tris={tris}")
print(f"STATS bbox X {min(xs):.3f}..{max(xs):.3f} ({max(xs)-min(xs):.3f} m)")
print(f"STATS bbox Y {min(ys):.3f}..{max(ys):.3f} ({max(ys)-min(ys):.3f} m)")
print(f"STATS bbox Z {min(zs):.3f}..{max(zs):.3f} ({max(zs)-min(zs):.3f} m)")

# ---------------------------------------------------------------- save + export
import os
OUT = os.path.expanduser("~/workspace/cp-models/seed-drill")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "seed-drill.blend"))
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "seed-drill.glb"),
                          export_format='GLB', export_apply=True)
print("SAVED", OUT)
