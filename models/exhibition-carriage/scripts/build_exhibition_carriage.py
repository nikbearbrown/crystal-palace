#!/usr/bin/env python3
"""Build the exhibition carriage (candidate #33) — a period enclosed carriage
(brougham type) read loosely from the one carriage visible, small and
occluded, through the curtained opening in Dickinson plate XXIV.
All dimensions INFERRED from period practice; see NOTES.md.
Forward = +X, ground z=0, origin at base centre."""
import bpy
import math
from mathutils import Vector

# ---------- clean ----------
bpy.ops.wm.read_factory_settings(use_empty=True)

# ---------- materials ----------
def mat(name, rgb, rough=0.6, metallic=0.0, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*rgb, 1)
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Metallic'].default_value = metallic
    if alpha < 1.0:
        bsdf.inputs['Alpha'].default_value = alpha
        m.surface_render_method = 'DITHERED'
    return m

BODY   = mat('JapanBlackGreen', (0.012, 0.020, 0.016), 0.32)   # japanned body, near-black green
BODY2  = mat('BodyPanel',       (0.020, 0.030, 0.024), 0.28)
ROOFM  = mat('RoofBlack',       (0.008, 0.008, 0.010), 0.55)
IRON   = mat('IronBlack',       (0.015, 0.015, 0.017), 0.45, 0.8)
STEEL  = mat('SteelPolished',   (0.30, 0.31, 0.32), 0.30, 0.9)
WOOD   = mat('WheelWood',       (0.05, 0.035, 0.022), 0.55)    # painted wheel timber, dark
SHAFTM = mat('ShaftWood',       (0.10, 0.065, 0.035), 0.5)
GLASS  = mat('Glass',           (0.62, 0.72, 0.74), 0.06, 0.0, 0.35)
TRIM   = mat('TrimRed',         (0.16, 0.02, 0.015), 0.5)      # lining / cushion hint
FABRIC = mat('SeatFabric',      (0.05, 0.05, 0.09), 0.9)
BRASS  = mat('Brass',           (0.35, 0.22, 0.06), 0.35, 0.9)
DARKIN = mat('InteriorDark',    (0.010, 0.010, 0.012), 0.95)

# ---------- helpers ----------
def box(name, loc, scale, material, bevel=0.0, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = (scale[0] / 2, scale[1] / 2, scale[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    if material: o.data.materials.append(material)
    if bevel > 0:
        mod = o.modifiers.new('bev', 'BEVEL')
        mod.width = bevel
        mod.segments = 2
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.modifier_apply(modifier='bev')
    return o

def cyl(name, loc, radius, depth, material, rot=(0, 0, 0), verts=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth,
                                        location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    if material: o.data.materials.append(material)
    return o

def beam(name, p1, p2, radius, material, verts=10):
    """Cylinder between two points (shafts, spokes, stays)."""
    p1, p2 = Vector(p1), Vector(p2)
    mid = (p1 + p2) / 2
    d = p2 - p1
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=d.length,
                                        location=mid)
    o = bpy.context.active_object
    o.name = name
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = d.to_track_quat('Z', 'Y')
    if material: o.data.materials.append(material)
    return o

def torus(name, loc, major, minor, material, rot=(0, 0, 0), seg=28, ring=10, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
                                     major_segments=seg, minor_segments=ring,
                                     location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    if material: o.data.materials.append(material)
    return o

# ============================================================
# WHEELS — spoked, iron tyre; rear larger than front (period)
# ============================================================
def build_wheel(name, R, spokes, hub_r, y):
    parts = []
    # iron tyre
    parts.append(torus(name + '_tyre', (0, y, R), R - 0.012, 0.016, IRON, rot=(math.radians(90), 0, 0), seg=36, ring=8))
    # wooden felloe rim just inside the tyre
    parts.append(torus(name + '_felloe', (0, y, R), R - 0.045, 0.028, WOOD, rot=(math.radians(90), 0, 0), seg=36, ring=8))
    # hub barrel + caps
    parts.append(cyl(name + '_hub', (0, y, R), hub_r, 0.13, WOOD, rot=(math.radians(90), 0, 0)))
    parts.append(cyl(name + '_hubband', (0, y, R), hub_r + 0.006, 0.05, IRON, rot=(math.radians(90), 0, 0)))
    # spokes, slightly dished in two rows
    for i in range(spokes):
        a = 2 * math.pi * i / spokes
        dish = 0.022 if i % 2 == 0 else -0.022
        p1 = (math.cos(a) * hub_r * 0.6, y + dish, R + math.sin(a) * hub_r * 0.6)
        p2 = (math.cos(a) * (R - 0.06), y, R + math.sin(a) * (R - 0.06))
        parts.append(beam(f'{name}_sp{i}', p1, p2, 0.015, WOOD, verts=8))
    return parts

REAR_X, FRONT_X = -1.08, 1.18
REAR_R, FRONT_R = 0.70, 0.46
for side, y in (('L', 0.79), ('R', -0.79)):
    build_wheel('WheelRear' + side, REAR_R, 14, 0.095, y)
for side, y in (('L', 0.73), ('R', -0.73)):
    build_wheel('WheelFront' + side, FRONT_R, 12, 0.080, y)

# ============================================================
# UNDER-CARRIAGE — perch, axles, elliptic springs, forecarriage
# ============================================================
# perch (central longitudinal bar)
box('Perch', (0.05, 0, 0.80), (2.70, 0.10, 0.12), IRON, bevel=0.01)
# rear axle
cyl('RearAxle', (REAR_X, 0, REAR_R), 0.035, 1.62, IRON, rot=(math.radians(90), 0, 0))
# front axle + forecarriage (fifth wheel + swivel)
cyl('FrontAxle', (FRONT_X, 0, FRONT_R), 0.032, 1.50, IRON, rot=(math.radians(90), 0, 0))
cyl('FifthWheel', (FRONT_X, 0, 0.62), 0.30, 0.035, IRON, verts=24)
cyl('ForeCarriageBar', (FRONT_X, 0, 0.70), 0.045, 0.55, IRON, rot=(0, 0, math.radians(90)))
beam('ReachBar', (0.30, 0, 0.80), (FRONT_X, 0, 0.66), 0.030, IRON)
# rear spring hangers / bed
box('RearBed', (REAR_X, 0, 0.92), (0.45, 1.16, 0.07), IRON, bevel=0.01)
box('FrontBed', (FRONT_X, 0, 0.80), (0.45, 1.15, 0.06), IRON, bevel=0.01)

def leaf_arc(name, x, zc, half_len, rise, y, up=True):
    """One leaf-spring arc from chord boxes in the XZ plane."""
    n = 7
    pts = []
    for i in range(n + 1):
        t = -1 + 2 * i / n
        zz = zc + (rise if up else -rise) * (1 - t * t)
        pts.append((x + t * half_len, zz))
    for i in range(n):
        (x1, z1), (x2, z2) = pts[i], pts[i + 1]
        L = math.hypot(x2 - x1, z2 - z1)
        ang = math.atan2(z2 - z1, x2 - x1)
        box(f'{name}_{i}', ((x1 + x2) / 2, y, (z1 + z2) / 2), (L + 0.012, 0.046, 0.009),
            STEEL, rot=(0, -ang, 0))

def elliptic_spring(name, x, z, half_len, y):
    """Full-elliptic spring: two leaf arcs facing off, centre bolt, end eyes."""
    leaf_arc(name + '_top', x, z + 0.012, half_len, 0.075, y, up=True)
    leaf_arc(name + '_bot', x, z - 0.012, half_len, 0.075, y, up=False)
    cyl(name + '_bolt', (x, y, z), 0.014, 0.10, IRON)
    for sx in (x - half_len, x + half_len):
        cyl(name + '_eye', (sx, y, z), 0.020, 0.05, IRON, rot=(math.radians(90), 0, 0), verts=10)

# rear full-elliptics on both sides
for y in (0.62, -0.62):
    elliptic_spring('RearSpring', REAR_X, 1.00, 0.30, y)
    beam('RearSpringLinkF', (REAR_X + 0.30, y, 1.00), (REAR_X + 0.18, y, 0.93), 0.010, IRON)
    beam('RearSpringLinkB', (REAR_X - 0.30, y, 1.00), (REAR_X - 0.18, y, 0.93), 0.010, IRON)
# front springs (smaller)
for y in (0.58, -0.58):
    elliptic_spring('FrontSpring', FRONT_X, 0.86, 0.24, y)

# ============================================================
# BODY — enclosed cabin (brougham type), floor z=1.12
# ============================================================
FLOOR = 1.12
BODY_X0, BODY_X1 = -1.62, 0.72       # body spans x
BODY_W = 1.44
CX = (BODY_X0 + BODY_X1) / 2

# lower body shell: three stacked, slightly tapering boxes read as the
# curved boat-bottom of a panelled carriage body
box('BodyLower', (CX, 0, FLOOR + 0.10), (2.26, BODY_W - 0.16, 0.22), BODY, bevel=0.07)
box('BodyMid',   (CX, 0, FLOOR + 0.30), (2.34, BODY_W - 0.06, 0.26), BODY, bevel=0.05)
box('BodyWaist', (CX, 0, FLOOR + 0.48), (2.38, BODY_W, 0.14), BODY, bevel=0.03)
# waist rail (moulding)
box('WaistRail', (CX, 0, FLOOR + 0.57), (2.42, BODY_W + 0.03, 0.045), BODY2, bevel=0.015)
# interior block (seen dark through glass)
box('Interior', (CX, 0, FLOOR + 0.78), (2.10, BODY_W - 0.22, 0.52), DARKIN)
# seat hint inside
box('InsideSeat', (CX - 0.45, 0, FLOOR + 0.62), (0.55, 1.05, 0.14), FABRIC, bevel=0.03)
box('InsideSeatBack', (CX - 0.78, 0, FLOOR + 0.86), (0.12, 1.05, 0.42), FABRIC, bevel=0.03)

# door panels and mouldings, both sides
for sgn, y in ((1, BODY_W / 2 + 0.005), (-1, -BODY_W / 2 - 0.005)):
    box(f'DoorPanel{sgn}', (CX + 0.18, y, FLOOR + 0.30), (0.95, 0.02, 0.52), BODY2, bevel=0.02)
    box(f'DoorPanelLow{sgn}', (CX + 0.18, y, FLOOR + 0.10), (0.90, 0.02, 0.16), BODY2, bevel=0.015)
    # door handle
    cyl(f'DoorHandle{sgn}', (CX + 0.58, y + (0.03 if sgn > 0 else -0.03), FLOOR + 0.38),
        0.014, 0.05, BRASS, rot=(math.radians(90), 0, 0))

# upperworks: corner pillars + window frames + glass
TOP = FLOOR + 1.10          # roof underside height (2.22)
PIL = [(BODY_X0 + 0.06, BODY_W / 2 - 0.05), (BODY_X0 + 0.06, -BODY_W / 2 + 0.05),
       (BODY_X1 - 0.06, BODY_W / 2 - 0.05), (BODY_X1 - 0.06, -BODY_W / 2 + 0.05),
       (CX + 0.45, BODY_W / 2 - 0.05), (CX + 0.45, -BODY_W / 2 + 0.05)]
for i, (px, py) in enumerate(PIL):
    box(f'Pillar{i}', (px, py, FLOOR + 0.83), (0.075, 0.075, 0.56), BODY)
# side glass: door window + rear quarter window, both sides
for sgn, y in ((1, BODY_W / 2 - 0.012), (-1, -BODY_W / 2 + 0.012)):
    box(f'GlassDoor{sgn}', (CX + 0.20, y, FLOOR + 0.84), (0.80, 0.015, 0.46), GLASS)
    box(f'GlassQuarter{sgn}', (CX - 0.62, y, FLOOR + 0.84), (0.62, 0.015, 0.46), GLASS)
    box(f'SillTop{sgn}', (CX - 0.19, y, FLOOR + 1.085), (2.20, 0.05, 0.05), BODY)
# front + back glass
box('GlassFront', (BODY_X1 - 0.055, 0, FLOOR + 0.84), (0.015, 1.05, 0.46), GLASS)
box('GlassBack', (BODY_X0 + 0.055, 0, FLOOR + 0.84), (0.015, 0.85, 0.42), GLASS)
box('FrontFrameTop', (BODY_X1 - 0.05, 0, FLOOR + 1.085), (0.05, 1.30, 0.05), BODY)
box('BackFrameTop', (BODY_X0 + 0.05, 0, FLOOR + 1.085), (0.05, 1.20, 0.05), BODY)
# roof: bevelled cushion slab + shallow crown step (the squashed-sphere
# dome of rounds 1–2 read as an inset oval tray; this reads as a roof)
box('Roof', (CX, 0, TOP + 0.045), (2.46, BODY_W + 0.08, 0.09), ROOFM, bevel=0.045)
box('RoofCrown', (CX, 0, TOP + 0.105), (2.00, 1.10, 0.05), ROOFM, bevel=0.024)

# rear boot / platform behind body
box('RearBoot', (BODY_X0 - 0.16, 0, FLOOR - 0.02), (0.30, 1.05, 0.10), IRON, bevel=0.01)

# ============================================================
# DRIVER'S BOX — seat ahead of the cabin on the forecarriage
# ============================================================
BX = 1.02
box('BoxFrame', (BX, 0, 1.16), (0.56, 1.10, 0.10), BODY, bevel=0.02)
box('BoxSeat', (BX - 0.02, 0, 1.30), (0.52, 1.12, 0.13), FABRIC, bevel=0.04)
# seat cheeks so the box reads as joinery, not a floating cushion
for sgn, y in ((1, 0.53), (-1, -0.53)):
    box(f'BoxCheek{sgn}', (BX - 0.05, y, 1.38), (0.46, 0.05, 0.30), BODY, bevel=0.015)
box('BoxBack', (BX - 0.30, 0, 1.52), (0.10, 1.12, 0.42), FABRIC, bevel=0.04)
box('BoxBackTop', (BX - 0.30, 0, 1.74), (0.12, 1.16, 0.06), BODY, bevel=0.02)
# iron stays from perch head to the box
for y in (0.48, -0.48):
    beam('BoxStay', (0.66, y, 0.86), (BX + 0.10, y, 1.14), 0.018, IRON)
# footboard: sloped board ahead of the box
box('Footboard', (1.48, 0, 0.98), (0.55, 1.02, 0.045), WOOD, bevel=0.01,
    rot=(0, math.radians(-32), 0))
beam('FootboardStayL', (1.30, 0.48, 0.80), (1.62, 0.48, 1.10), 0.014, IRON)
beam('FootboardStayR', (1.30, -0.48, 0.80), (1.62, -0.48, 1.10), 0.014, IRON)
# dashboard (leather apron board rising ahead of driver's feet)
box('Dashboard', (1.62, 0, 1.17), (0.05, 1.06, 0.34), BODY, bevel=0.02, rot=(0, math.radians(-14), 0))

# ============================================================
# LAMPS — square carriage lamps on the front corners of the body
# ============================================================
for sgn, y in ((1, 0.80), (-1, -0.80)):
    beam(f'LampBracket{sgn}', (0.62, y * 0.90, 1.86), (0.66, y, 1.94), 0.012, IRON)
    box(f'LampBody{sgn}', (0.66, y, 2.02), (0.13, 0.13, 0.20), IRON, bevel=0.01)
    box(f'LampGlass{sgn}', (0.735, y, 2.02), (0.012, 0.09, 0.13), GLASS)
    box(f'LampCap{sgn}', (0.66, y, 2.15), (0.16, 0.16, 0.035), IRON, bevel=0.01)
    cyl(f'LampChimney{sgn}', (0.66, y, 2.21), 0.022, 0.06, IRON)

# ============================================================
# SHAFTS — a pair, from body front sides angling forward/down
# ============================================================
for sgn, y in ((1, 0.66), (-1, -0.66)):
    beam(f'ShaftA{sgn}', (0.55, y, 1.02), (1.55, y + 0.02 * sgn, 0.90), 0.026, SHAFTM)
    beam(f'ShaftB{sgn}', (1.55, y + 0.02 * sgn, 0.90), (2.42, y + 0.04 * sgn, 0.80), 0.021, SHAFTM)
    cyl(f'ShaftTip{sgn}', (2.44, y + 0.04 * sgn, 0.80), 0.024, 0.07, IRON,
        rot=(math.radians(90), 0, math.radians(80)))

# steps at the door, both sides
for sgn, y in ((1, 0.86), (-1, -0.86)):
    box(f'StepLow{sgn}', (CX + 0.18, y, 0.60), (0.42, 0.20, 0.03), IRON)
    box(f'StepHigh{sgn}', (CX + 0.18, y * 0.94, 0.88), (0.40, 0.16, 0.03), IRON)
    beam(f'StepStay{sgn}', (CX + 0.05, y * 0.82, 1.10), (CX + 0.05, y, 0.62), 0.011, IRON)

# ---------- apply scale, join nothing; report ----------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

dg = bpy.context.evaluated_depsgraph_get()
tris = 0
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        ev = o.evaluated_get(dg)
        tris += sum(len(p.vertices) - 2 for p in ev.data.polygons)
print('OBJECTS:', len([o for o in bpy.context.scene.objects if o.type == 'MESH']))
print('TRIANGLES:', tris)

bpy.ops.wm.save_as_mainfile(filepath='/home/hatch/workspace/cp-models/exhibition-carriage/exhibition-carriage.blend')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath='/home/hatch/workspace/cp-models/exhibition-carriage/exhibition-carriage.glb',
                          export_apply=True)
print('SAVED blend + glb')
