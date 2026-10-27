#!/usr/bin/env python3
"""Build Garrett & Sons' portable steam engine as photographed by
H. F. Talbot at the Great Exhibition, 1851 (calotype, PD).

Run headless:
  blender -b -noaudio -P scripts/build_portable_steam_engine.py

Layout as photographed (side aspect, firebox at -X, smokebox/chimney
at +X): horizontal locomotive-type boiler on a four-wheeled carriage.
The cylinder sits on top of the boiler at the FIREBOX end and a long
connecting rod runs along the boiler top to a crankshaft carried over
the SMOKEBOX end; the flywheel (6 spokes) is on the far side (+Y).
Road wheels: LARGE pair (1.45 m) under the smokebox end, SMALL pair
(1.12 m) under the firebox end -- the reverse of later practice, but
that is what the calotype shows (see NOTES.md for the measurement
chain; the Hornsby engine in the companion calotype has the big pair
at the firebox end instead).

Scale chain: proportions measured on the calotype against a grid
(vertical extents used throughout; the plate is yawed ~25 deg so
horizontal extents were corrected x1.10). Absolute scale anchored on
the large road wheel at 1.45 m (4 ft 9 in, a standard period size),
giving a boiler barrel of 0.92 m diameter. Origin at base centre:
ground level under the middle of the engine body.
"""
import bpy
import math
import os
from mathutils import Vector, Matrix

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'portable-steam-engine'

# ---------------------------------------------------------------- clean
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ---------------------------------------------------------------- mats
def mat(name, rgb, rough=0.5, metal=0.6):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*rgb, 1.0)
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Metallic'].default_value = metal
    return m

MAT_BOILER = mat('BoilerBlack', (0.018, 0.018, 0.020), 0.38, 0.85)
MAT_FRAME  = mat('FrameBlack',  (0.028, 0.028, 0.032), 0.52, 0.6)
MAT_WHEEL  = mat('WheelBlack',  (0.022, 0.024, 0.022), 0.50, 0.6)
MAT_TYRE   = mat('TyreSteel',   (0.16, 0.16, 0.17),    0.35, 0.9)
MAT_BRASS  = mat('PolishedBrass', (0.46, 0.31, 0.10), 0.27, 1.0)
MAT_STEEL  = mat('PolishedSteel', (0.56, 0.58, 0.61), 0.20, 1.0)
MAT_COPPER = mat('CopperPipe',  (0.32, 0.11, 0.05),    0.35, 1.0)
MAT_BRONZE = mat('DomeBronze',  (0.145, 0.098, 0.038), 0.42, 1.0)
MAT_DARK   = mat('ShadowIron',  (0.012, 0.012, 0.013), 0.70, 0.4)

# ---------------------------------------------------------------- helpers
def finish(obj, material):
    if material:
        obj.data.materials.append(material)
    return obj

def box(name, x, y, z, dx, dy, dz, material, rot=None):
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
    o = bpy.context.object
    o.name = name
    o.dimensions = (dx, dy, dz)
    if rot:
        o.rotation_euler = rot
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(o, material)

def cyl(name, x, y, z, r, depth, material, rot=None, verts=28):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth,
                                        location=(x, y, z))
    o = bpy.context.object
    o.name = name
    if rot:
        o.rotation_euler = rot
    return finish(o, material)

def lathe(name, profile, material, segments=40):
    """Spin a (r, z) profile around the Z axis into a mesh."""
    n = len(profile)
    verts, faces = [], []
    for i in range(segments):
        a = 2.0 * math.pi * i / segments
        ca, sa = math.cos(a), math.sin(a)
        for (r, z) in profile:
            verts.append((r * ca, r * sa, z))
    for i in range(segments):
        j = (i + 1) % segments
        for k in range(n - 1):
            faces.append((i * n + k, j * n + k, j * n + k + 1, i * n + k + 1))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    return finish(o, material)

def beam(name, p1, p2, w, h, material):
    """Rectangular-section beam between two points (section w x h,
    length along the line p1->p2)."""
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    L = d.length
    bpy.ops.mesh.primitive_cube_add(location=(p1 + p2) / 2.0)
    o = bpy.context.object
    o.name = name
    o.dimensions = (L, w, h)
    x_axis = d.normalized()
    up = Vector((0, 0, 1)) if abs(x_axis.z) < 0.9 else Vector((0, 1, 0))
    z_axis = x_axis.cross(up).normalized()
    y_axis = z_axis.cross(x_axis).normalized()
    m = Matrix((x_axis, y_axis, z_axis)).transposed()
    o.rotation_euler = m.to_euler()
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(o, material)

def rod(name, p1, p2, r, material, verts=12):
    """Round rod between two points."""
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d.length,
                                        location=(p1 + p2) / 2.0)
    o = bpy.context.object
    o.name = name
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return finish(o, material)

# ================================================================ dimensions
BC = 1.47            # boiler centreline height
BR = 0.46            # boiler barrel radius (0.92 m dia)

# ================================================================ boiler
# barrel: firebox tube plate x=-1.55 to smokebox back x=+1.22
cyl('BoilerBarrel', -0.165, 0, BC, BR, 2.77, MAT_BOILER, rot=(0, math.pi / 2, 0), verts=44)
# smokebox (slightly larger dia), front face x=+1.66
cyl('Smokebox', 1.44, 0, BC, 0.48, 0.44, MAT_BOILER, rot=(0, math.pi / 2, 0), verts=44)
# smokebox door: dished disc + rim + centre boss
door = lathe('SmokeboxDoor', [(0.0, 0.0), (0.30, 0.015), (0.44, 0.045),
                              (0.475, 0.075), (0.48, 0.10), (0.46, 0.105),
                              (0.30, 0.075), (0.0, 0.055)], MAT_BOILER, segments=44)
door.rotation_euler = (0, math.pi / 2, 0)
door.location = (1.665, 0, BC)
cyl('DoorBoss', 1.79, 0, BC, 0.055, 0.07, MAT_FRAME, rot=(0, math.pi / 2, 0))
beam('DoorHandleH', (1.83, -0.16, BC), (1.83, 0.16, BC), 0.028, 0.028, MAT_FRAME)
beam('DoorHandleV', (1.83, 0, BC - 0.16), (1.83, 0, BC + 0.16), 0.028, 0.028, MAT_FRAME)
# barrel bands (brass) and one dark strap
for bx, bm in [( -0.55, MAT_BRASS), (0.30, MAT_BRASS), (0.95, MAT_DARK)]:
    t = bpy.ops.mesh.primitive_torus_add(major_radius=BR + 0.006, minor_radius=0.016,
                                         location=(bx, 0, BC))
    ring = bpy.context.object
    ring.name = 'BarrelBand'
    ring.rotation_euler = (0, math.pi / 2, 0)
    ring.scale = (1.0, 1.0, 1.6)
    finish(ring, bm)

# firebox wrapper: rectangular casing below/around the barrel at -X
box('FireboxWrapper', -1.10, 0, 1.16, 0.96, 1.04, 1.10, MAT_BOILER)
box('FireboxSaddle', -1.10, 0, 1.66, 1.00, 1.08, 0.10, MAT_FRAME)
box('Ashpan', -1.10, 0, 0.50, 0.70, 0.80, 0.24, MAT_DARK)
# backhead plate at x=-1.63
plate = lathe('Backhead', [(0.0, 0.0), (0.40, 0.01), (0.465, 0.035), (0.47, 0.06),
                           (0.40, 0.05), (0.0, 0.03)], MAT_BOILER, segments=44)
plate.rotation_euler = (0, -math.pi / 2, 0)
plate.location = (-1.635, 0, BC)
# backhead fittings cluster (as photographed: fire door, cocks, wheel, lever)
box('FireDoor', -1.70, 0.0, 1.22, 0.05, 0.36, 0.34, MAT_FRAME)
cyl('FireDoorHinge', -1.70, -0.19, 1.22, 0.022, 0.30, MAT_STEEL, rot=(0, 0, 0), verts=10)
cyl('GaugeCockL', -1.70, -0.22, 1.78, 0.020, 0.10, MAT_BRASS, rot=(0, math.pi / 2, 0), verts=10)
cyl('GaugeCockR', -1.70, 0.22, 1.78, 0.020, 0.10, MAT_BRASS, rot=(0, math.pi / 2, 0), verts=10)
cyl('BlowdownPipe', -1.68, 0.30, 1.05, 0.024, 0.55, MAT_COPPER, verts=10)
wheel_h = bpy.ops.mesh.primitive_torus_add(major_radius=0.085, minor_radius=0.014,
                                           location=(-1.74, 0.28, 1.86))
wh = bpy.context.object; wh.name = 'BackheadWheel'
wh.rotation_euler = (0, math.pi / 2, 0); finish(wh, MAT_FRAME)
beam('HangingLever', (-1.72, -0.30, 1.62), (-1.78, -0.34, 1.18), 0.03, 0.02, MAT_STEEL)
rod('BackheadPipeRun', (-1.67, -0.33, 1.80), (-1.67, -0.33, 0.95), 0.016, MAT_COPPER)

# ================================================================ chimney
chim = lathe('Chimney', [(0.335, 0.0), (0.30, 0.05), (0.20, 0.17), (0.158, 0.34),
                         (0.150, 1.55), (0.146, 2.02), (0.155, 2.14), (0.185, 2.26),
                         (0.208, 2.34), (0.212, 2.385), (0.196, 2.385), (0.180, 2.30),
                         (0.150, 2.16), (0.142, 2.05)], MAT_BOILER, segments=36)
chim.location = (1.16, 0, 1.875)
for bz in (2.78, 3.38):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.152, minor_radius=0.011,
                                     location=(1.16, 0, bz))
    b = bpy.context.object; b.name = 'ChimneyBand'; finish(b, MAT_BRASS)

# ================================================================ dome + whistle
dome = lathe('SteamDome', [(0.30, 0.0), (0.29, 0.05), (0.275, 0.16), (0.24, 0.27),
                           (0.17, 0.36), (0.085, 0.415), (0.078, 0.47),
                           (0.10, 0.55), (0.125, 0.615), (0.128, 0.65),
                           (0.105, 0.65), (0.080, 0.575), (0.062, 0.49),
                           (0.0, 0.47)], MAT_BRONZE, segments=36)
dome.location = (-1.16, 0, 1.86)
rod('Whistle', (-1.22, -0.18, 1.95), (-1.22, -0.18, 2.44), 0.016, MAT_BRASS)
beam('WhistleCross', (-1.22, -0.25, 2.40), (-1.22, -0.11, 2.40), 0.018, 0.018, MAT_BRASS)
beam('RegulatorLever', (-1.05, -0.10, 2.02), (-1.30, -0.16, 2.42), 0.026, 0.018, MAT_STEEL)

# ================================================================ cylinder + motion (top, firebox end)
cyl('Cylinder', -0.85, 0, 2.04, 0.17, 0.86, MAT_BOILER, rot=(0, math.pi / 2, 0), verts=32)
cyl('CylinderCoverF', -0.395, 0, 2.04, 0.185, 0.045, MAT_FRAME, rot=(0, math.pi / 2, 0), verts=32)
cyl('CylinderCoverB', -1.295, 0, 2.04, 0.185, 0.045, MAT_FRAME, rot=(0, math.pi / 2, 0), verts=32)
cyl('SteamChest', -0.85, 0, 2.245, 0.085, 0.66, MAT_BOILER, rot=(0, math.pi / 2, 0), verts=20)
box('CylinderSaddle', -0.85, 0, 1.90, 0.74, 0.30, 0.10, MAT_FRAME)
rod('SteamPipe', (-1.10, 0.12, 1.95), (-1.00, 0.05, 2.20), 0.032, MAT_COPPER)
# crosshead guides + block
box('GuideBarTop', -0.23, 0, 2.135, 0.46, 0.05, 0.028, MAT_STEEL)
box('GuideBarBottom', -0.23, 0, 1.945, 0.46, 0.05, 0.028, MAT_STEEL)
box('Crosshead', -0.28, 0, 2.04, 0.13, 0.09, 0.17, MAT_FRAME)
box('MotionBracket', -0.01, 0, 1.99, 0.05, 0.06, 0.20, MAT_FRAME)
rod('PistonRod', (-0.40, 0, 2.04), (-0.28, 0, 2.04), 0.023, MAT_STEEL)
# crankshaft over the smokebox end; crank pin posed down-forward
CRANK = Vector((1.22, 0, 1.98))
PIN = Vector((1.22 + 0.155, 0, 1.98 - 0.109))
rod('ConnectingRod', (-0.25, -0.10, 2.04), (PIN.x, -0.60, PIN.z), 0.030, MAT_STEEL)
beam('ConnectingRodFlat', (-0.23, -0.585, 2.03), (PIN.x - 0.05, -0.585, PIN.z + 0.01),
     0.055, 0.030, MAT_STEEL)
rod('ValveRod', (-0.53, 0.0, 2.26), (0.92, 0.0, 2.20), 0.011, MAT_STEEL)
rod('EccentricRod', (0.92, 0.0, 2.20), (1.13, -0.30, 2.02), 0.010, MAT_STEEL)
for sy in (-1, 1):
    box('CrankBracket', 1.22, sy * 0.50, 1.80, 0.10, 0.07, 0.50, MAT_FRAME,
        rot=(0.35 * sy * 0, 0, 0))
    cyl('CrankBearing', 1.22, sy * 0.545, 1.98, 0.075, 0.07, MAT_FRAME,
        rot=(math.pi / 2, 0, 0), verts=16)
rod('Crankshaft', (1.22, -0.62, 1.98), (1.22, 0.62, 1.98), 0.042, MAT_STEEL)
disc = lathe('CrankDisc', [(0.0, -0.03), (0.13, -0.03), (0.13, 0.03), (0.0, 0.03)],
             MAT_FRAME, segments=28)
disc.rotation_euler = (math.pi / 2, 0, 0)
disc.location = (1.22, -0.60, 1.98)
rod('CrankPin', (PIN.x, -0.66, PIN.z), (PIN.x, -0.54, PIN.z), 0.026, MAT_STEEL)

# ================================================================ flywheel (far side, +Y)
FW = Vector((1.20, 0.665, 1.98))
rim = lathe('FlywheelRim', [(0.775, -0.065), (0.875, -0.065), (0.875, 0.065),
                            (0.775, 0.065)], MAT_WHEEL, segments=48)
rim.rotation_euler = (math.pi / 2, 0, 0)
rim.location = FW
cyl('FlywheelHub', FW.x, FW.y, FW.z, 0.115, 0.17, MAT_WHEEL, rot=(math.pi / 2, 0, 0), verts=20)
for i in range(6):
    a = math.radians(60 * i + 15)
    p1 = (FW.x + 0.10 * math.cos(a), FW.y, FW.z + 0.10 * math.sin(a))
    p2 = (FW.x + 0.80 * math.cos(a), FW.y, FW.z + 0.80 * math.sin(a))
    rod('FlywheelSpoke', p1, p2, 0.030, MAT_WHEEL, verts=10)

# ================================================================ governor + fittings
rod('GovernorSpindle', (-0.03, 0, 1.93), (-0.03, 0, 2.56), 0.016, MAT_STEEL)
cyl('GovernorPulley', -0.03, 0, 1.99, 0.055, 0.05, MAT_FRAME, verts=16)
for sy in (-1, 1):
    beam('GovernorArm', (-0.03, 0, 2.47), (-0.03 + 0.0, sy * 0.105, 2.235),
         0.014, 0.014, MAT_BRASS)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.056, location=(-0.03, sy * 0.115, 2.205))
    ball = bpy.context.object; ball.name = 'GovernorBall'; finish(ball, MAT_BRASS)
cyl('GovernorTop', -0.03, 0, 2.585, 0.020, 0.05, MAT_BRASS, verts=10)
rod('GovernorBelt', (-0.03, 0.055, 1.99), (1.13, 0.30, 1.94), 0.007, MAT_DARK)
# tall safety-valve / gauge column, firebox side of the governor
rod('SafetyColumn', (-0.35, 0.10, 1.93), (-0.35, 0.10, 2.33), 0.024, MAT_BRASS)
cyl('SafetyCup', -0.35, 0.10, 2.375, 0.045, 0.09, MAT_BRASS, verts=14)
# feed-pump rod down the smokebox front face (near side), from the crank
rod('PumpRod', (1.60, -0.33, 1.92), (1.60, -0.33, 1.02), 0.013, MAT_STEEL)
cyl('PumpBarrel', 1.60, -0.33, 0.94, 0.048, 0.26, MAT_FRAME, verts=14)
rod('PumpPipe', (1.60, -0.33, 0.82), (1.35, -0.20, 0.80), 0.014, MAT_COPPER)

# ================================================================ underframe + axles
for sy in (-1, 1):
    box('FrameRail', 0.05, sy * 0.44, 0.98, 2.90, 0.07, 0.15, MAT_FRAME)
    rod('TieRod', (-1.48, sy * 0.80, 0.60), (0.85, sy * 0.82, 0.66), 0.011, MAT_STEEL)
rod('RearAxle', (-1.48, -0.88, 0.58), (-1.48, 0.88, 0.58), 0.055, MAT_FRAME)
rod('FrontAxle', (0.85, -0.90, 0.725), (0.85, 0.90, 0.725), 0.060, MAT_FRAME)
box('RearAxleBed', -1.48, 0, 0.68, 0.22, 0.80, 0.10, MAT_FRAME)
box('FrontAxleBed', 0.85, 0, 0.84, 0.24, 0.84, 0.10, MAT_FRAME)
# turntable under the firebox end + drawbar toward -X (as photographed)
cyl('Turntable', -1.48, 0, 0.635, 0.30, 0.055, MAT_FRAME, verts=24)
beam('Drawbar', (-1.70, 0, 0.60), (-2.48, 0, 0.52), 0.055, 0.045, MAT_FRAME)
cyl('DrawbarEye', -2.52, 0, 0.515, 0.05, 0.03, MAT_FRAME, rot=(math.pi / 2, 0, 0), verts=12)

# ================================================================ road wheels
def road_wheel(name, cx, cz, R, tyre_w, n_spokes, y_side):
    """Spoked road wheel in the X-Z plane at y = y_side (outer face)."""
    yc = y_side - math.copysign(tyre_w / 2.0 + 0.055, y_side)  # hub centre plane
    tire = lathe(name + 'Tyre', [(R - 0.028, -tyre_w / 2), (R + 0.012, -tyre_w / 2),
                                 (R + 0.012, tyre_w / 2), (R - 0.028, tyre_w / 2)],
                 MAT_TYRE, segments=40)
    tire.rotation_euler = (math.pi / 2, 0, 0)
    tire.location = (cx, y_side, cz)
    rimw = lathe(name + 'Rim', [(R - 0.105, -tyre_w * 0.36), (R - 0.028, -tyre_w * 0.36),
                                (R - 0.028, tyre_w * 0.36), (R - 0.105, tyre_w * 0.36)],
                 MAT_WHEEL, segments=40)
    rimw.rotation_euler = (math.pi / 2, 0, 0)
    rimw.location = (cx, y_side, cz)
    hub = lathe(name + 'Hub', [(0.001, -0.085), (0.105, -0.085), (0.125, -0.03),
                               (0.125, 0.05), (0.10, 0.085), (0.001, 0.085)],
                MAT_WHEEL, segments=24)
    hub.rotation_euler = (math.pi / 2, 0, 0)
    hub.location = (cx, yc + math.copysign(0.02, y_side), cz)
    cap = cyl(name + 'HubCap', cx, y_side + math.copysign(tyre_w / 2 + 0.075, y_side),
              cz, 0.052, 0.045, MAT_BRASS, rot=(math.pi / 2, 0, 0), verts=14)
    for i in range(n_spokes):
        a = 2 * math.pi * i / n_spokes + 0.13
        p1 = (cx + 0.09 * math.cos(a), yc, cz + 0.09 * math.sin(a))
        p2 = (cx + (R - 0.085) * math.cos(a), y_side, cz + (R - 0.085) * math.sin(a))
        beam(name + 'Spoke', p1, p2, 0.030, 0.052, MAT_WHEEL)

road_wheel('WheelFL', 0.85, 0.725, 0.725, 0.13, 14, -0.90)
road_wheel('WheelFR', 0.85, 0.725, 0.725, 0.13, 14, 0.90)
road_wheel('WheelRL', -1.48, 0.58, 0.56, 0.11, 12, -0.88)
road_wheel('WheelRR', -1.48, 0.58, 0.56, 0.11, 12, 0.88)

# ================================================================ apply + save
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.ops.object.select_all(action='DESELECT')

dg = bpy.context.evaluated_depsgraph_get()
tris = 0
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        ev = o.evaluated_get(dg)
        tris += sum(len(p.vertices) - 2 for p in ev.data.polygons)
print('TRIANGLES:', tris)
print('OBJECTS:', len(bpy.context.scene.objects))

blend_path = os.path.join(ROOT, SLUG + '.blend')
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
glb_path = os.path.join(ROOT, SLUG + '.glb')
bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB', export_apply=True)
print('SAVED', blend_path)
print('SAVED', glb_path)
