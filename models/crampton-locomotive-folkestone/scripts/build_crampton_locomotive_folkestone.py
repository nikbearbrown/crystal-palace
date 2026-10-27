#!/usr/bin/env python3
"""Build the Crampton locomotive "Folkestone" (SER No. 136, Stephenson
works no. 787, 1851) from Talbot's Great Exhibition calotype.

Run headless:
  blender -b -noaudio -P scripts/build_crampton_locomotive_folkestone.py

Geometry is built in "photo metres": u = distance from the front
buffer-beam face, z = height above rail level. At the end every object
is shifted by -L/2 in X so the origin sits at base centre (rail level,
mid-length), front of engine toward -X.

Dimensions: driving wheels 6 ft (1.8288 m) and bogie wheels 3 ft 6 in
(1.0668 m) are published for this engine; all other proportions were
measured on the calotype at 4.303 mm/px (driver = 425 px). See NOTES.md.
"""
import bpy
import math
import os
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'crampton-locomotive-folkestone'

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
MAT_FRAME = mat('FrameBlack', (0.028, 0.028, 0.032), 0.52, 0.6)
MAT_WHEEL = mat('WheelBlack', (0.022, 0.024, 0.022), 0.5, 0.6)
MAT_TYRE = mat('TyreSteel', (0.16, 0.16, 0.17), 0.35, 0.9)
MAT_BRASS = mat('PolishedBrass', (0.46, 0.31, 0.10), 0.27, 1.0)
MAT_STEEL = mat('PolishedSteel', (0.56, 0.58, 0.61), 0.2, 1.0)
MAT_WOOD = mat('BeamWood', (0.05, 0.034, 0.02), 0.85, 0.0)
MAT_PANEL = mat('PanelGreenBlack', (0.008, 0.02, 0.014), 0.42, 0.5)
MAT_DARK = mat('ShadowIron', (0.012, 0.012, 0.013), 0.7, 0.4)

def mat_texture(name, filename):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    tex = m.node_tree.nodes.new('ShaderNodeTexImage')
    img = bpy.data.images.load(os.path.join(ROOT, 'textures', filename))
    img.pack()
    tex.image = img
    m.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    m.node_tree.links.new(tex.outputs['Alpha'], bsdf.inputs['Alpha'])
    bsdf.inputs['Roughness'].default_value = 0.42
    bsdf.inputs['Metallic'].default_value = 0.35
    return m

MAT_NAMEPLATE = mat_texture('Nameplate', 'nameplate.png')
MAT_MAKER = mat_texture('MakersPlate', 'makersplate.png')
MAT_LINING = mat_texture('PanelLining', 'panel_lining.png')

# ---------------------------------------------------------------- helpers
L = 7.62
XOFF = -L / 2.0

def box(name, u, y, z, du, dy, dz, material, rot_y=0.0):
    bpy.ops.mesh.primitive_cube_add(location=(u, y, z))
    o = bpy.context.object
    o.name = name
    o.dimensions = (du, dy, dz)
    if rot_y:
        o.rotation_euler = (0.0, rot_y, 0.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        o.data.materials.append(material)
    return o

def cyl_x(name, u, y, z, r, length, material, verts=28):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=length,
                                        location=(u, y, z), rotation=(0, math.radians(90), 0))
    o = bpy.context.object
    o.name = name
    if material:
        o.data.materials.append(material)
    return o

def cyl_y(name, u, y, z, r, length, material, verts=20):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=length,
                                        location=(u, y, z), rotation=(math.radians(90), 0, 0))
    o = bpy.context.object
    o.name = name
    if material:
        o.data.materials.append(material)
    return o

def cyl_z(name, u, y, z, r, length, material, verts=20):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=length,
                                        location=(u, y, z))
    o = bpy.context.object
    o.name = name
    if material:
        o.data.materials.append(material)
    return o

def rod(name, p1, p2, r, material, verts=12):
    a, b = Vector(p1), Vector(p2)
    mid = (a + b) / 2
    d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d.length,
                                        location=tuple(mid))
    o = bpy.context.object
    o.name = name
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    if material:
        o.data.materials.append(material)
    return o

def lathe_z(name, profile, material, u=0.0, y=0.0, z0=0.0, segments=44):
    """Surface of revolution about a vertical (Z) axis at (u, y).
    profile: list of (radius, height) bottom to top."""
    verts, faces = [], []
    rings = []
    for r, h in profile:
        r = max(r, 0.0012)
        ring = []
        for i in range(segments):
            a = 2 * math.pi * i / segments
            ring.append(len(verts))
            verts.append((u + r * math.cos(a), y + r * math.sin(a), z0 + h))
        rings.append(ring)
    for k in range(len(rings) - 1):
        for i in range(segments):
            j = (i + 1) % segments
            faces.append((rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    if material:
        me.materials.append(material)
    return o

def lathe_y(name, profile, material, segments=44):
    """Surface of revolution about a Y axis through the origin.
    profile: list of (radius, axial offset)."""
    verts, faces = [], []
    rings = []
    for r, off in profile:
        r = max(r, 0.0012)
        ring = []
        for i in range(segments):
            a = 2 * math.pi * i / segments
            ring.append(len(verts))
            verts.append((r * math.cos(a), off, r * math.sin(a)))
        rings.append(ring)
    for k in range(len(rings) - 1):
        for i in range(segments):
            j = (i + 1) % segments
            faces.append((rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    if material:
        me.materials.append(material)
    return o

def join_objects(objs, name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    o = bpy.context.object
    o.name = name
    return o

def flat_plate(name, cx, cy, cz, rx, ry, side, material):
    """Oval textured plate standing in the YZ plane, facing +/-Y.
    Texture reads correctly and upright from the facing side."""
    bpy.ops.mesh.primitive_circle_add(vertices=44, radius=rx, fill_type='NGON',
                                      location=(cx, cy, cz))
    p = bpy.context.object
    p.name = name
    p.scale = (1.0, ry / rx, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if side > 0:
        p.rotation_mode = 'YXZ'
        p.rotation_euler = (math.radians(-90), math.radians(180), 0)
    else:
        p.rotation_mode = 'XYZ'
        p.rotation_euler = (math.radians(90), 0, 0)
    p.data.materials.append(material)
    return p

# ---------------------------------------------------------------- wheels
A1, A2, DR = 1.205, 2.560, 6.385
Z_LEAD, Z_DRV = 0.5335, 0.9144
R_LEAD, R_DRV = 0.5335, 0.9144
WY = 0.78

def make_wheel(name, R, n_spokes, hub_r, tyre_w, side, crank=None):
    parts = []
    tw = tyre_w
    prof = [(R - 0.055, -tw / 2), (R - 0.012, -tw / 2), (R, -tw * 0.30),
            (R, tw * 0.30), (R - 0.012, tw / 2), (R - 0.055, tw / 2),
            (R - 0.16, tw * 0.34), (R - 0.16, -tw * 0.34), (R - 0.055, -tw / 2)]
    parts.append(lathe_y(name + '_tyre', prof, MAT_TYRE))
    parts.append(cyl_y(name + '_hub', 0, 0, 0, hub_r, tw + 0.10, MAT_WHEEL, 24))
    parts.append(cyl_y(name + '_boss', 0, side * (tw / 2 + 0.035), 0, hub_r * 0.55, 0.07, MAT_WHEEL, 20))
    spoke_len = R - 0.16 - hub_r + 0.10
    for i in range(n_spokes):
        a = 2 * math.pi * i / n_spokes
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        s = bpy.context.object
        s.name = name + '_spoke'
        s.dimensions = (0.052, tw * 0.42, spoke_len)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        for v in s.data.vertices:      # taper the rim end
            if v.co.z > 0:
                v.co.x *= 0.62
        rc = hub_r - 0.05 + spoke_len / 2
        s.location = (rc * math.cos(a), 0, rc * math.sin(a))
        s.rotation_mode = 'QUATERNION'
        s.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(
            Vector((math.cos(a), 0, math.sin(a))))
        s.data.materials.append(MAT_WHEEL)
        parts.append(s)
    if crank:
        du, dz, pin_len = crank
        parts.append(cyl_y(name + '_pinboss', du, side * (tw / 2 + 0.01), dz, 0.115, 0.05, MAT_WHEEL, 20))
        parts.append(cyl_y(name + '_pin', du, side * (tw / 2 + pin_len / 2), dz, 0.058, pin_len, MAT_STEEL, 16))
    return join_objects(parts, name)

for side in (1, -1):
    for (ax, zz, nm) in ((A1, Z_LEAD, 'LeadWheel1'), (A2, Z_LEAD, 'LeadWheel2')):
        w = make_wheel(nm, R_LEAD, 12, 0.105, 0.125, side)
        w.location = (ax, side * WY, zz)
    w = make_wheel('Driver', R_DRV, 20, 0.165, 0.135, side,
                   crank=(-0.275, -0.054, 0.30))
    w.location = (DR, side * WY, Z_DRV)
cyl_y('Axle', A1, 0, Z_LEAD, 0.075, 1.62, MAT_DARK)
cyl_y('Axle', A2, 0, Z_LEAD, 0.075, 1.62, MAT_DARK)
cyl_y('Axle', DR, 0, Z_DRV, 0.10, 1.66, MAT_DARK)

# axleboxes (outside the frames, both sides)
for side in (1, -1):
    for (ax, zz) in ((A1, Z_LEAD), (A2, Z_LEAD), (DR, Z_DRV)):
        box('Axlebox', ax, side * 1.005, zz + 0.05, 0.38, 0.10, 0.46, MAT_FRAME)
        box('AxleboxKeep', ax, side * 1.005, zz - 0.25, 0.30, 0.09, 0.10, MAT_FRAME)
    rod('BogieRod', (A1, side * 1.03, 0.62), (A2, side * 1.03, 0.62), 0.018, MAT_FRAME)

# bogie side frames (inside; mostly hidden)
for side in (1, -1):
    box('BogieFrame', 1.88, side * 0.60, 0.52, 2.55, 0.035, 0.42, MAT_DARK)
box('BogieBeam', 1.88, 0, 0.55, 0.25, 1.24, 0.18, MAT_DARK)

# ---------------------------------------------------------------- frames
def frame_outline():
    pts = [(0.05, 1.25), (7.57, 1.25), (7.57, 0.55), (5.60, 0.55),
           (4.40, 0.58), (3.35, 0.62)]
    for i in range(1, 8):   # arch over axle 2
        ang = math.pi * i / 8.0
        pts.append((2.560 + 0.60 * math.cos(ang), 0.62 + 0.41 * math.sin(ang)))
    pts.append((1.70, 0.60))
    for i in range(1, 8):   # arch over axle 1
        ang = math.pi * i / 8.0
        pts.append((1.205 + 0.585 * math.cos(ang), 0.60 + 0.41 * math.sin(ang)))
    pts.append((0.45, 0.62))
    pts.append((0.10, 0.62))
    return pts

import bmesh
def make_frame(side):
    pts = frame_outline()
    me = bpy.data.meshes.new('Frame')
    bm = bmesh.new()
    vs = [bm.verts.new((u, 0, z)) for (u, z) in pts]
    f = bm.faces.new(vs)
    res = bmesh.ops.extrude_face_region(bm, geom=[f])
    verts = [e for e in res['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=verts, vec=(0, 0.035, 0))
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new('Frame', me)
    bpy.context.collection.objects.link(o)
    o.location = (0, 0.9375 if side > 0 else -0.9725, 0)
    o.data.materials.append(MAT_FRAME)
    return o

for side in (1, -1):
    make_frame(side)

# footplate + valance
box('Footplate', 3.85, 0, 1.245, 7.70, 2.44, 0.07, MAT_FRAME)
for side in (1, -1):
    box('Valance', 3.85, side * 1.205, 1.16, 7.70, 0.03, 0.10, MAT_FRAME)

# buffer beams + buffers (rear set inferred - hidden in shadow in the photo)
for bu in (0.0, 7.62):
    box('BufferBeam', bu, 0, 0.92, 0.14, 2.44, 0.30, MAT_WOOD)
    out = -1 if bu == 0.0 else 1
    for side in (1, -1):
        cyl_x('BufferHousing', bu + out * 0.10, side * 0.78, 0.95, 0.095, 0.20, MAT_FRAME)
        cyl_x('BufferShank', bu + out * 0.24, side * 0.78, 0.95, 0.05, 0.12, MAT_STEEL)
        cyl_x('BufferHead', bu + out * 0.315, side * 0.78, 0.95, 0.16, 0.05, MAT_FRAME)

# ---------------------------------------------------------------- boiler
cyl_x('Smokebox', 0.94, 0, 2.02, 0.575, 0.88, MAT_BOILER, 48)
cyl_x('BoilerBarrel', 3.185, 0, 2.02, 0.56, 3.61, MAT_BOILER, 48)
for bu in (1.95, 2.90, 3.85, 4.70):
    cyl_x('BoilerBand', bu, 0, 2.02, 0.566, 0.035, MAT_FRAME, 48)
box('BoilerSaddle', 1.55, 0, 1.36, 0.5, 0.95, 0.24, MAT_DARK)
box('BoilerSaddle', 3.55, 0, 1.36, 0.5, 0.95, 0.24, MAT_DARK)

# smokebox door: convex lathe disc, axis swung to -X
door_prof = [(0.0012, 0.062), (0.30, 0.057), (0.48, 0.044), (0.56, 0.022), (0.575, 0.0)]
door = lathe_z('SmokeboxDoor', door_prof, MAT_BOILER, segments=44)
door.rotation_euler = (0, math.radians(-90), 0)
door.location = (0.50, 0, 2.02)
cyl_x('DoorRim', 0.535, 0, 2.02, 0.578, 0.03, MAT_FRAME, 48)
cyl_x('DoorDart', 0.44, 0, 2.02, 0.048, 0.12, MAT_STEEL, 16)
cyl_z('DoorHandleV', 0.40, 0, 2.02, 0.016, 0.30, MAT_STEEL, 10)
cyl_y('DoorHandleH', 0.40, 0, 2.02, 0.016, 0.30, MAT_STEEL, 10)

# chimney (tall, flared cap)
chim_prof = [(0.0012, 0.0), (0.30, 0.0), (0.335, 0.12), (0.30, 0.22), (0.252, 0.30),
             (0.245, 0.45), (0.245, 1.15), (0.262, 1.22), (0.268, 1.30), (0.246, 1.36),
             (0.268, 1.44), (0.332, 1.58), (0.364, 1.68), (0.368, 1.74), (0.30, 1.74),
             (0.285, 1.60), (0.26, 1.45), (0.0012, 1.45)]
lathe_z('Chimney', chim_prof, MAT_BOILER, u=1.162, z0=2.30, segments=44)

# handrails + stanchions + knobs
for side in (1, -1):
    rod('Handrail', (0.78, side * 0.548, 2.44), (4.85, side * 0.548, 2.44), 0.013, MAT_STEEL, 8)
    for bu in (0.85, 1.85, 2.85, 3.85, 4.75):
        y0 = math.sqrt(max(0.56 ** 2 - 0.42 ** 2, 0.01))
        rod('RailStanchion', (bu, side * y0 * 0.985, 2.44), (bu, side * 0.548, 2.44), 0.011, MAT_STEEL, 8)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.021,
                                             location=(bu, side * 0.548, 2.44))
        bpy.context.object.name = 'RailKnob'
        bpy.context.object.data.materials.append(MAT_STEEL)

# nameplates: curved patches wrapped on the barrel (barrel axis z=2.02)
def curved_plate(name, u_c, z_c, half_len, half_ang, side, material):
    R = 0.5685
    a0 = math.asin((z_c - 2.02) / R)
    NC, NR = 10, 5
    verts, faces, uvs = [], [], []
    for j in range(NR + 1):
        a = a0 - half_ang + 2 * half_ang * j / NR
        for i in range(NC + 1):
            u = u_c - half_len + 2 * half_len * i / NC
            verts.append((u, side * R * math.cos(a), 2.02 + R * math.sin(a)))
            uvs.append((i / NC, j / NR))
    for j in range(NR):
        for i in range(NC):
            a = j * (NC + 1) + i
            b = a + 1
            c = a + NC + 1
            faces.append((a, b, c))
            faces.append((b, c + 1, c))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    uv = me.uv_layers.new(name='UVMap')
    for loop in me.loops:
        uv.data[loop.index].uv = uvs[loop.vertex_index]
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    me.materials.append(material)
    return o

for side in (1, -1):
    curved_plate('Nameplate', 3.076, 2.09, 0.465, math.radians(24), side, MAT_NAMEPLATE)

# feed clacks + pipes (far side mirrored = inferred)
for side in (1, -1):
    cyl_z('FeedClack', 2.84, side * 0.46, 1.62, 0.055, 0.34, MAT_BRASS, 16)
    cyl_z('FeedClackCap', 2.84, side * 0.46, 1.81, 0.068, 0.035, MAT_BRASS, 16)
    rod('FeedPipe', (2.84, side * 0.46, 1.45), (2.90, side * 0.40, 1.02), 0.030, MAT_BRASS)
    rod('SidePipe', (3.02, side * 0.545, 1.55), (3.02, side * 0.545, 1.95), 0.011, MAT_STEEL, 8)

# ---------------------------------------------------------------- firebox
box('Firebox', 5.39, 0, 1.68, 1.18, 1.50, 1.26, MAT_BOILER)
bpy.ops.mesh.primitive_uv_sphere_add(segments=36, ring_count=18, location=(5.39, 0, 2.31))
fb = bpy.context.object
fb.name = 'FireboxTop'
fb.dimensions = (1.18, 1.50, 0.63)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
fb.data.materials.append(MAT_BOILER)
box('Ashpan', 5.39, 0, 0.52, 1.0, 0.92, 0.42, MAT_DARK)

# rear stack / dome casing (polished brass, bell base, flared lip)
stack_prof = [(0.0012, 0.0), (0.50, 0.0), (0.50, 0.12), (0.46, 0.28), (0.36, 0.42),
              (0.26, 0.55), (0.205, 0.68), (0.195, 0.98), (0.225, 1.03), (0.225, 1.10),
              (0.20, 1.14), (0.24, 1.20), (0.285, 1.24), (0.29, 1.28), (0.235, 1.28),
              (0.225, 1.16), (0.0012, 1.14)]
lathe_z('RearStack', stack_prof, MAT_BRASS, u=5.29, z0=2.30, segments=44)

# whistle (turned finial on the backhead top)
whistle_prof = [(0.0012, 0.0), (0.045, 0.0), (0.030, 0.10), (0.030, 0.38),
                (0.052, 0.44), (0.056, 0.52), (0.030, 0.62), (0.046, 0.70),
                (0.048, 0.76), (0.012, 0.85), (0.0012, 0.86)]
lathe_z('Whistle', whistle_prof, MAT_BRASS, u=5.90, y=0.20, z0=2.55, segments=24)

# backhead fittings (partly visible in the calotype; arrangement inferred)
cyl_z('BackheadColumn', 6.12, -0.30, 1.86, 0.045, 1.16, MAT_STEEL, 14)
rod('ColumnLever', (6.12, -0.30, 2.44), (6.12, -0.30, 2.72), 0.016, MAT_STEEL, 8)
rod('RegulatorLever', (6.02, 0.18, 2.20), (6.38, 0.18, 2.52), 0.020, MAT_STEEL, 8)
bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.032,
                                     location=(6.40, 0.18, 2.54))
bpy.context.object.name = 'LeverKnob'
bpy.context.object.data.materials.append(MAT_WOOD)
for side in (1, -1):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.075, minor_radius=0.013,
                                     major_segments=18, minor_segments=8,
                                     location=(6.03, side * 0.36, 2.12),
                                     rotation=(0, math.radians(90), 0))
    bpy.context.object.name = 'Handwheel'
    bpy.context.object.data.materials.append(MAT_BRASS)
bpy.ops.mesh.primitive_torus_add(major_radius=0.09, minor_radius=0.014,
                                 major_segments=20, minor_segments=8,
                                 location=(6.04, 0, 1.82), rotation=(0, math.radians(90), 0))
bpy.context.object.name = 'BackheadRing'
bpy.context.object.data.materials.append(MAT_STEEL)

# ---------------------------------------------------------------- splasher panels
for side in (1, -1):
    box('SplasherPanel', 6.23, side * 1.00, 1.775, 2.66, 0.045, 0.99, MAT_PANEL)
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(6.23, side * 1.0245, 1.775))
    pl = bpy.context.object
    pl.name = 'PanelLining'
    pl.dimensions = (2.66, 0.99, 0)
    if side > 0:
        pl.rotation_mode = 'YXZ'
        pl.rotation_euler = (math.radians(-90), math.radians(180), 0)
    else:
        pl.rotation_mode = 'XYZ'
        pl.rotation_euler = (math.radians(90), 0, 0)
    pl.data.materials.append(MAT_LINING)
    flat_plate('MakersPlate', 6.26, side * 1.028, 1.74, 0.43, 0.275, side, MAT_MAKER)
    rod('PanelPost', (4.94, side * 1.0, 1.28), (4.94, side * 1.0, 2.46), 0.018, MAT_STEEL, 8)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.028,
                                         location=(4.94, side * 1.0, 2.48))
    bpy.context.object.name = 'PostKnob'
    bpy.context.object.data.materials.append(MAT_BRASS)
box('SplasherTop', 6.23, 0, 2.295, 2.66, 2.05, 0.05, MAT_PANEL)

# ---------------------------------------------------------------- motion
CS = 3.895   # intermediate crankshaft position
cyl_y('Crankshaft', CS, 0, 1.03, 0.075, 2.10, MAT_STEEL)
for side in (1, -1):
    cyl_y('CrankWeb', CS, side * 1.035, 1.03, 0.30, 0.05, MAT_WHEEL, 28)
    cyl_y('CrankPin', CS - 0.27, side * 1.06, 0.955, 0.055, 0.10, MAT_STEEL, 14)
    cyl_y('CrankWebIn', CS, side * 0.32, 1.03, 0.27, 0.045, MAT_DARK, 24)
    p1 = Vector((CS - 0.27, side * 1.09, 0.955))
    p2 = Vector((DR - 0.275, side * 1.09, Z_DRV - 0.054))
    mid = (p1 + p2) / 2
    ln = (p2 - p1).length
    bpy.ops.mesh.primitive_cube_add(location=tuple(mid))
    r = bpy.context.object
    r.name = 'CouplingRod'
    r.dimensions = (ln + 0.34, 0.032, 0.105)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    r.rotation_euler = (0, math.atan2(p1.z - p2.z, p2.x - p1.x), 0)
    r.data.materials.append(MAT_STEEL)
    cyl_y('RodBigEnd', p2.x, side * 1.09, p2.z, 0.105, 0.055, MAT_STEEL, 20)
    cyl_y('RodSmallEnd', p1.x, side * 1.09, p1.z, 0.088, 0.055, MAT_STEEL, 20)

# inside cylinders + slide bars + crossheads (inferred; hidden between frames)
for side in (1, -1):
    cyl_x('Cylinder', 4.47, side * 0.38, 0.80, 0.235, 0.66, MAT_DARK, 24)
    box('SlideBarTop', 4.08, side * 0.38, 0.99, 0.42, 0.05, 0.03, MAT_STEEL)
    box('SlideBarBot', 4.08, side * 0.38, 0.63, 0.42, 0.05, 0.03, MAT_STEEL)
    box('Crosshead', 4.02, side * 0.38, 0.81, 0.16, 0.09, 0.30, MAT_STEEL)
    rod('MainRod', (3.95, side * 0.38, 0.86), (CS - 0.24, side * 0.34, 0.97), 0.026, MAT_STEEL, 10)

# diagonal rod low under the frames (visible in the calotype; likely brake rigging)
rod('LowRod', (3.6, 0, 0.30), (6.9, 0, 0.72), 0.016, MAT_FRAME)
# front-bottom drain pipes (as photographed)
rod('DrainPipe', (0.42, -0.30, 0.62), (0.30, -0.30, 0.22), 0.026, MAT_FRAME)
rod('DrainPipe', (0.42, 0.30, 0.62), (0.30, 0.30, 0.22), 0.026, MAT_FRAME)

# steps
for side in (1, -1):
    box('RearStep1', 7.38, side * 1.16, 0.97, 0.30, 0.24, 0.03, MAT_FRAME)
    box('RearStep2', 7.38, side * 1.20, 0.64, 0.30, 0.24, 0.03, MAT_FRAME)
    box('FrontStep', 0.62, side * 1.14, 0.72, 0.28, 0.22, 0.03, MAT_FRAME)

# ---------------------------------------------------------------- rivets
rivet_pts = []   # (x, y, z, axis) axis 'Y' = dome along Y, 'X' = dome along -X
for side in (1, -1):
    y = side * 0.978
    u = 0.25
    while u < 7.45:
        rivet_pts.append((u, y, 1.16, 'Y'))
        u += 0.26
    u = 0.25
    while u < 3.3:
        rivet_pts.append((u, y, 0.72, 'Y'))
        u += 0.26
    u = 3.5
    while u < 7.45:
        rivet_pts.append((u, y, 0.66, 'Y'))
        u += 0.26
    for (ax, zz) in ((A1, Z_LEAD), (A2, Z_LEAD), (DR, Z_DRV)):
        for (du, dz) in ((-0.13, 0.16), (0.13, 0.16), (-0.13, -0.16), (0.13, -0.16)):
            rivet_pts.append((ax + du, side * 1.06, zz + 0.05 + dz, 'Y'))
for i in range(26):
    a = 2 * math.pi * i / 26
    rivet_pts.append((0.545, 0.578 * math.cos(a), 2.02 + 0.578 * math.sin(a), 'X'))

def rivet_mesh(pts, r=0.016, segs=6):
    verts, faces = [], []
    for (px, py, pz, axis) in pts:
        base = len(verts)
        if axis == 'X':
            verts.append((px + 0.004, py, pz))
            for i in range(segs):
                a = 2 * math.pi * i / segs
                verts.append((px + 0.004, py + r * math.cos(a), pz + r * math.sin(a)))
            verts.append((px - r * 0.8, py, pz))
        else:
            sgn = 1 if py >= 0 else -1
            verts.append((px, py - sgn * 0.004, pz))
            for i in range(segs):
                a = 2 * math.pi * i / segs
                verts.append((px + r * math.cos(a), py - sgn * 0.004, pz + r * math.sin(a)))
            verts.append((px, py + sgn * (r * 0.8 - 0.004), pz))
        for i in range(segs):
            j = (i + 1) % segs
            faces.append((base + 1 + i, base + 1 + j, base + segs + 1))
    me = bpy.data.meshes.new('Rivets')
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new('Rivets', me)
    bpy.context.collection.objects.link(o)
    me.materials.append(MAT_FRAME)
    return o

rivet_mesh(rivet_pts)

# ---------------------------------------------------------------- leaf spring
# The big laminated spring over the leading bogie (signature feature of
# the calotype view): nested leaves on one curvature, centre bracket
# with a bolt, hanger links at the eyes. One is visible in the photo,
# outboard of the frame; a mirrored pair is modelled.
def arc_leaf(name, xc, yc, length, width, thk, z_centre, curve_c):
    NS = 13
    verts, faces = [], []
    for i in range(NS + 1):
        t = -1 + 2 * i / NS
        x = xc + t * length / 2
        z = z_centre - curve_c * (t * length / 2) ** 2
        verts.append((x, yc - width / 2, z + thk / 2))   # top L
        verts.append((x, yc + width / 2, z + thk / 2))   # top R
        verts.append((x, yc - width / 2, z - thk / 2))   # bot L
        verts.append((x, yc + width / 2, z - thk / 2))   # bot R
    for i in range(NS):
        a = i * 4
        b = a + 4
        faces.append((a, b, b + 1, a + 1))        # top
        faces.append((a + 2, a + 3, b + 3, b + 2))  # bottom
        faces.append((a, a + 2, b + 2, b))       # left side
        faces.append((a + 1, b + 1, b + 3, a + 3))  # right side
    n = NS * 4
    faces.append((0, 1, 3, 2))
    faces.append((n - 4, n - 2, n - 1, n - 3))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    me.materials.append(MAT_FRAME)
    return o

for side in (1, -1):
    yc = side * 0.99
    for k in range(9):
        arc_leaf('SpringLeaf', 1.65, yc, 1.14 - 0.05 * k, 0.105, 0.013,
                 1.7835 - 0.0155 * k, 1.45)
    box('SpringBracket', 1.65, yc, 1.47, 0.10, 0.05, 0.36, MAT_FRAME)
    cyl_y('SpringBolt', 1.65, yc, 1.38, 0.036, 0.10, MAT_STEEL, 12)
    for sgn in (1, -1):
        box('SpringHanger', 1.65 + sgn * 0.545, yc, 1.36, 0.035, 0.02, 0.24, MAT_FRAME)

# ---------------------------------------------------------------- recentre + save
bpy.ops.object.select_all(action='SELECT')
for o in bpy.context.selected_objects:
    o.location.x += XOFF
bpy.ops.object.select_all(action='DESELECT')

tris = 0
dg = bpy.context.evaluated_depsgraph_get()
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        ev = o.evaluated_get(dg)
        tris += sum(len(p.vertices) - 2 for p in ev.data.polygons)
print('TRIANGLES:', tris)
print('OBJECTS:', len(bpy.context.scene.objects))
xs, ys, zs = [], [], []
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            xs.append(w.x); ys.append(w.y); zs.append(w.z)
print('BBOX X %.2f..%.2f  Y %.2f..%.2f  Z %.2f..%.2f' %
      (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))

blend_path = os.path.join(ROOT, SLUG + '.blend')
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT, SLUG + '.glb'),
                          export_format='GLB', use_selection=True)
print('SAVED', blend_path)
