#!/usr/bin/env python3
"""Build the iguanodon prop for the Crystal Palace film.

Benjamin Waterhouse Hawkins's 1854 concrete Iguanodon AS IT SURVIVES in
Crystal Palace Park -- the FOREGROUND animal of the reference photograph:
a sprawled, low browsing quadruped, head raised, near foreleg raised
gripping the reddish conifer trunk it is pulling at, tail dragging on
the ground behind. Deliberately Hawkins's anatomy -- rhinoceros-like
barrel body, columnar legs, and the thumb spike misplaced on the nose --
NOT a modern palaeontological reconstruction.

Source: one modern colour photograph, front 3/4 only
(refs/Iguanodon_Crystal_Palace.jpg, CC BY-SA 2.0).

Blender 4.2, headless, procedural. Units: metres. Z up.
Animal faces +X (head at +X, tail at -X). Animal's left side = +Y.
Origin at base centre (ground level under the body's midpoint).
"""
import bpy
import math
import os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ----------------------------------------------------------------------------
# scene reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ----------------------------------------------------------------------------
# materials
def skin_material():
    """Sage green-grey hide: noise mottle + voronoi scale bump.

    Procedural nodes live in the .blend; the .glb carries the base
    colour / roughness approximation only (see NOTES.md).
    """
    mat = bpy.data.materials.new('IguanodonHide')
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes['Principled BSDF']
    bsdf.inputs['Roughness'].default_value = 0.82
    tex = nt.nodes.new('ShaderNodeTexCoord')
    # large mottling
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 2.6
    noise.inputs['Detail'].default_value = 4.0
    noise.inputs['Roughness'].default_value = 0.75
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.28
    ramp.color_ramp.elements[0].color = (0.235, 0.275, 0.190, 1.0)
    ramp.color_ramp.elements[1].position = 0.72
    ramp.color_ramp.elements[1].color = (0.470, 0.510, 0.395, 1.0)
    nt.links.new(tex.outputs['Generated'], noise.inputs['Vector'])
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    # scale pattern: voronoi cells -> bump + a whisper of colour variation
    vor = nt.nodes.new('ShaderNodeTexVoronoi')
    vor.feature = 'F1'
    vor.inputs['Scale'].default_value = 5.0
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.55
    bump.inputs['Distance'].default_value = 0.012
    nt.links.new(tex.outputs['Generated'], vor.inputs['Vector'])
    nt.links.new(vor.outputs['Distance'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat

def plain_material(name, color, roughness=0.9):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    b = mat.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1.0)
    b.inputs['Roughness'].default_value = roughness
    return mat

def earth_material():
    mat = bpy.data.materials.new('ParkEarth')
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes['Principled BSDF']
    bsdf.inputs['Roughness'].default_value = 1.0
    tex = nt.nodes.new('ShaderNodeTexCoord')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 5.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[0].color = (0.185, 0.145, 0.100, 1.0)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (0.360, 0.295, 0.205, 1.0)
    nt.links.new(tex.outputs['Generated'], noise.inputs['Vector'])
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    return mat

def trunk_material():
    mat = bpy.data.materials.new('CycadTrunk')
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes['Principled BSDF']
    bsdf.inputs['Roughness'].default_value = 0.95
    tex = nt.nodes.new('ShaderNodeTexCoord')
    vor = nt.nodes.new('ShaderNodeTexVoronoi')
    vor.feature = 'F1'
    vor.inputs['Scale'].default_value = 7.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[0].color = (0.300, 0.105, 0.045, 1.0)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (0.520, 0.230, 0.110, 1.0)
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.7
    bump.inputs['Distance'].default_value = 0.015
    nt.links.new(tex.outputs['Generated'], vor.inputs['Vector'])
    nt.links.new(vor.outputs['Distance'], ramp.inputs['Fac'])
    nt.links.new(vor.outputs['Distance'], bump.inputs['Height'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat

MAT_SKIN = skin_material()
MAT_BONE = plain_material('BoneClawTeeth', (0.72, 0.68, 0.57), 0.55)
MAT_EYE = plain_material('EyeDark', (0.015, 0.015, 0.012), 0.22)
MAT_EARTH = earth_material()
MAT_TRUNK = trunk_material()

# ----------------------------------------------------------------------------
# mesh helpers
def make_mesh(name, verts, faces, mat, smooth_shade=False):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    if mat:
        me.materials.append(mat)
    if smooth_shade:
        for p in me.polygons:
            p.use_smooth = True
    return ob

def catmull_rom(pts, radii, samples_per_seg=6):
    """Sample a Catmull-Rom spline through pts (Vectors) with radii.
    Returns (centers, tangents, radii) lists."""
    P = [pts[0] * 2 - pts[1]] + list(pts) + [pts[-1] * 2 - pts[-2]]
    R = [radii[0]] + list(radii) + [radii[-1]]
    centers, tans, rads = [], [], []
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = P[i], P[i + 1], P[i + 2], P[i + 3]
        r0, r1, r2, r3 = R[i], R[i + 1], R[i + 2], R[i + 3]
        for j in range(samples_per_seg):
            t = j / samples_per_seg
            t2, t3 = t * t, t * t * t
            c = 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                       + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)
            d = 0.5 * ((-p0 + p2) + 2 * (2 * p0 - 5 * p1 + 4 * p2 - p3) * t
                       + 3 * (-p0 + 3 * p1 - 3 * p2 + p3) * t2)
            r = 0.5 * ((2 * r1) + (-r0 + r2) * t + (2 * r0 - 5 * r1 + 4 * r2 - r3) * t2
                       + (-r0 + 3 * r1 - 3 * r2 + r3) * t3)
            centers.append(c)
            tans.append(d.normalized())
            rads.append(r)
    centers.append(pts[-1])
    tans.append((pts[-1] - pts[-2]).normalized())
    rads.append(radii[-1])
    return centers, tans, rads

def loft(name, stations, mat, nseg=20, cap_start=True, cap_end=True):
    """Loft elliptical rings. stations = list of dicts:
    c=Vector centre, t=Vector tangent, ry=lateral radius, rz=vertical
    radius, flat=belly flattening 0..1 applied to the lower half."""
    # parallel-transport frames
    t0 = stations[0]['t'].normalized()
    ref = Vector((0, 0, 1)) if abs(t0.z) < 0.9 else Vector((0, 1, 0))
    lat = (ref - t0 * ref.dot(t0)).normalized()
    frames = []
    for st in stations:
        t = st['t'].normalized()
        lat = (lat - t * lat.dot(t)).normalized()
        vert = t.cross(lat).normalized()
        # ensure vert points generally +Z for body-like lofts
        frames.append((lat.copy(), vert))
    verts, faces = [], []
    ns = len(stations)
    for si, st in enumerate(stations):
        lat, vert = frames[si]
        for i in range(nseg):
            th = 2 * math.pi * i / nseg
            s, c = math.sin(th), math.cos(th)
            rz = st['rz'] * (1.0 - st.get('flat', 0.0)) if c < 0 else st['rz']
            p = st['c'] + lat * (s * st['ry']) + vert * (c * rz)
            verts.append(tuple(p))
    for s in range(ns - 1):
        for i in range(nseg):
            a = s * nseg + i
            b = s * nseg + (i + 1) % nseg
            cc = (s + 1) * nseg + (i + 1) % nseg
            d = (s + 1) * nseg + i
            faces.append((a, b, cc, d))
    if cap_start:
        c = stations[0]['c'] - stations[0]['t'].normalized() * stations[0]['rz'] * 0.5
        ci = len(verts)
        verts.append(tuple(c))
        for i in range(nseg):
            faces.append((ci, (i + 1) % nseg, i))
    if cap_end:
        c = stations[-1]['c'] + stations[-1]['t'].normalized() * stations[-1]['rz'] * 0.5
        ci = len(verts)
        verts.append(tuple(c))
        base = (ns - 1) * nseg
        for i in range(nseg):
            faces.append((ci, base + i, base + (i + 1) % nseg))
    return make_mesh(name, verts, faces, mat, smooth_shade=True)

def tube(name, pts, radii, mat, nseg=14, samples_per_seg=6):
    centers, tans, rads = catmull_rom([Vector(p) for p in pts], radii, samples_per_seg)
    stations = [{'c': c, 't': t, 'ry': r, 'rz': r} for c, t, r in zip(centers, tans, rads)]
    return loft(name, stations, mat, nseg=nseg)

def cone_verts_faces(base, tip, r, nseg=9):
    """One cone (base centre -> tip) as (verts, faces) for merging."""
    d = (tip - base)
    axis = d.normalized()
    ref = Vector((0, 0, 1)) if abs(axis.z) < 0.9 else Vector((1, 0, 0))
    u = (ref - axis * ref.dot(axis)).normalized()
    v = axis.cross(u).normalized()
    verts, faces = [], []
    for i in range(nseg):
        th = 2 * math.pi * i / nseg
        p = base + u * (math.cos(th) * r) + v * (math.sin(th) * r)
        verts.append(tuple(p))
    ti = len(verts)
    verts.append(tuple(tip))
    bc = len(verts)
    verts.append(tuple(base))
    for i in range(nseg):
        a, b = i, (i + 1) % nseg
        faces.append((a, b, ti))
        faces.append((bc, b, a))
    return verts, faces

def merged_cones(name, cones, mat, smooth_shade=False):
    verts, faces = [], []
    for base, tip, r in cones:
        v, f = cone_verts_faces(Vector(base), Vector(tip), r)
        off = len(verts)
        verts += v
        faces += [tuple(i + off for i in fc) for fc in f]
    return make_mesh(name, verts, faces, mat, smooth_shade=smooth_shade)

def box(name, sx, sy, sz, loc, mat, bevel=0.02, rot_z=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.dimensions = (sx, sy, sz)
    ob.rotation_euler = (0, 0, rot_z)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = ob.modifiers.new('bev', 'BEVEL')
        mod.width = bevel
        mod.segments = 2
        bpy.ops.object.modifier_apply(modifier='bev')
    ob.data.materials.append(mat)
    return ob

def sphere(name, loc, scale, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=18, ring_count=12, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for p in ob.data.polygons:
        p.use_smooth = True
    ob.data.materials.append(mat)
    return ob

# ----------------------------------------------------------------------------
# body + tail + neck: one loft. Stations (x, cz, ry, rz, belly-flat).
BODY = [
    (-4.70, 0.17, 0.05, 0.07, 0.05),
    (-4.45, 0.18, 0.09, 0.12, 0.05),
    (-4.10, 0.21, 0.14, 0.19, 0.06),
    (-3.70, 0.27, 0.20, 0.27, 0.07),
    (-3.25, 0.35, 0.27, 0.36, 0.08),
    (-2.80, 0.45, 0.35, 0.46, 0.09),
    (-2.35, 0.57, 0.44, 0.57, 0.10),
    (-1.95, 0.73, 0.55, 0.70, 0.12),
    (-1.60, 0.89, 0.68, 0.85, 0.14),
    (-1.25, 0.99, 0.80, 0.98, 0.15),
    (-0.85, 1.04, 0.90, 1.08, 0.15),
    (-0.40, 1.07, 0.95, 1.14, 0.15),
    ( 0.05, 1.07, 0.95, 1.14, 0.15),
    ( 0.50, 1.05, 0.92, 1.11, 0.15),
    ( 0.95, 1.03, 0.88, 1.07, 0.15),
    ( 1.35, 1.04, 0.82, 1.02, 0.14),
    ( 1.70, 1.09, 0.74, 0.95, 0.13),
    ( 2.00, 1.19, 0.63, 0.86, 0.12),
    ( 2.30, 1.35, 0.53, 0.76, 0.11),
    ( 2.58, 1.55, 0.45, 0.66, 0.10),
    ( 2.82, 1.75, 0.39, 0.57, 0.09),
    ( 3.05, 1.95, 0.345, 0.49, 0.08),
    ( 3.22, 2.09, 0.315, 0.44, 0.08),
]
def build_body():
    stations = []
    for i, (x, cz, ry, rz, fl) in enumerate(BODY):
        if i == 0:
            t = Vector((BODY[1][0] - x, 0, BODY[1][1] - cz))
        elif i == len(BODY) - 1:
            t = Vector((x - BODY[-2][0], 0, cz - BODY[-2][1]))
        else:
            t = Vector((BODY[i + 1][0] - BODY[i - 1][0], 0, BODY[i + 1][1] - BODY[i - 1][1]))
        stations.append({'c': Vector((x, 0, cz)), 't': t, 'ry': ry, 'rz': rz, 'flat': fl})
    return loft('Body', stations, MAT_SKIN, nseg=24)

# head: its own loft along a rising axis. Stations (x, cz, ry, rz).
HEAD = [
    (3.00, 2.05, 0.325, 0.415),
    (3.30, 2.22, 0.30, 0.39),
    (3.58, 2.32, 0.29, 0.37),
    (3.85, 2.42, 0.245, 0.315),
    (4.12, 2.43, 0.20, 0.255),
    (4.34, 2.36, 0.14, 0.185),
    (4.50, 2.30, 0.07, 0.10),
]
def head_at(x):
    """Interpolate (cz, ry, rz) of the head loft at plan position x."""
    for i in range(len(HEAD) - 1):
        x0, cz0, ry0, rz0 = HEAD[i]
        x1, cz1, ry1, rz1 = HEAD[i + 1]
        if x0 <= x <= x1:
            f = (x - x0) / (x1 - x0)
            return (cz0 + f * (cz1 - cz0), ry0 + f * (ry1 - ry0), rz0 + f * (rz1 - rz0))
    return HEAD[-1][1], HEAD[-1][2], HEAD[-1][3]

def build_head():
    stations = []
    for i, (x, cz, ry, rz) in enumerate(HEAD):
        if i == 0:
            t = Vector((HEAD[1][0] - x, 0, HEAD[1][1] - cz))
        elif i == len(HEAD) - 1:
            t = Vector((x - HEAD[-2][0], 0, cz - HEAD[-2][1]))
        else:
            t = Vector((HEAD[i + 1][0] - HEAD[i - 1][0], 0, HEAD[i + 1][1] - HEAD[i - 1][1]))
        stations.append({'c': Vector((x, 0, cz)), 't': t, 'ry': ry, 'rz': rz, 'flat': 0.05})
    loft('Head', stations, MAT_SKIN, nseg=20)
    # lower jaw / chin mass, tucked under the skull so the mouth reads
    # as a near-closed jaw with the tooth fringe along its seam
    JAW = [
        (3.12, 1.83, 0.265, 0.145),
        (3.50, 1.90, 0.25, 0.135),
        (3.90, 1.99, 0.21, 0.115),
        (4.24, 2.05, 0.145, 0.09),
        (4.46, 2.10, 0.06, 0.05),
    ]
    stations = []
    for i, (x, cz, ry, rz) in enumerate(JAW):
        if i == 0:
            t = Vector((JAW[1][0] - x, 0, JAW[1][1] - cz))
        elif i == len(JAW) - 1:
            t = Vector((x - JAW[-2][0], 0, cz - JAW[-2][1]))
        else:
            t = Vector((JAW[i + 1][0] - JAW[i - 1][0], 0, JAW[i + 1][1] - JAW[i - 1][1]))
        stations.append({'c': Vector((x, 0, cz)), 't': t, 'ry': ry, 'rz': rz, 'flat': 0.0})
    loft('Jaw', stations, MAT_SKIN, nseg=16)
    # THE thumb spike, misplaced on the nose (Hawkins, 1854)
    merged_cones('NoseHorn', [((4.08, 0, 2.62), (4.17, 0, 2.80), 0.05)], MAT_SKIN,
                 smooth_shade=True)
    # eyes: small, high on the skull sides
    sphere('EyeL', (3.58, 0.292, 2.45), (0.048, 0.033, 0.048), MAT_EYE)
    sphere('EyeR', (3.58, -0.292, 2.45), (0.048, 0.033, 0.048), MAT_EYE)
    # nostrils: small dark pits on the snout
    sphere('NostrilL', (4.28, 0.075, 2.50), (0.04, 0.026, 0.016), MAT_EYE)
    sphere('NostrilR', (4.28, -0.075, 2.50), (0.04, 0.026, 0.016), MAT_EYE)
    # upper tooth fringe: small pale teeth hanging along the mouth seam
    teeth = []
    x = 3.38
    while x <= 4.36:
        cz, ry, rz = head_at(x)
        z = cz - rz * 0.94
        taper = 0.7 + 0.3 * math.sin((x - 3.38) / 0.98 * math.pi)
        for sgn in (1, -1):
            y = sgn * ry * 0.94
            teeth.append(((x, y, z + 0.024), (x + 0.010, y + sgn * 0.005, z - 0.024 * taper - 0.010), 0.015))
        x += 0.082
    merged_cones('Teeth', teeth, MAT_BONE)

# ----------------------------------------------------------------------------
# legs, feet, claws
def build_legs():
    # near hind leg (+Y, the hero leg of the photograph): crouched fold
    tube('HindLegL', [(-1.45, 0.70, 1.32), (-1.30, 0.95, 0.85), (-1.02, 1.03, 0.48),
                      (-1.22, 1.00, 0.24), (-1.16, 0.99, 0.13)],
         [0.42, 0.335, 0.235, 0.165, 0.14], MAT_SKIN)
    box('HindFootL', 0.56, 0.30, 0.15, (-0.98, 1.00, 0.085), MAT_SKIN, bevel=0.045)
    # far hind leg (-Y): same fold, mostly behind the body
    tube('HindLegR', [(-1.50, -0.70, 1.30), (-1.38, -0.92, 0.82), (-1.12, -0.99, 0.46),
                      (-1.30, -0.96, 0.22), (-1.24, -0.95, 0.12)],
         [0.42, 0.33, 0.23, 0.16, 0.135], MAT_SKIN)
    box('HindFootR', 0.54, 0.29, 0.15, (-1.06, -0.95, 0.08), MAT_SKIN, bevel=0.045)
    # far foreleg (-Y): planted column under the shoulder
    tube('ForeLegR', [(1.55, -0.55, 1.27), (1.68, -0.72, 0.80), (1.80, -0.80, 0.42),
                      (1.86, -0.84, 0.15)],
         [0.31, 0.225, 0.165, 0.13], MAT_SKIN)
    box('ForeFootR', 0.44, 0.27, 0.13, (1.95, -0.85, 0.065), MAT_SKIN, bevel=0.04)
    # near foreleg (+Y): raised, forearm up to the gripping hand
    tube('ForeLegL', [(1.50, 0.58, 1.30), (1.94, 1.02, 0.82), (2.22, 1.01, 1.04),
                      (2.40, 0.93, 1.33)],
         [0.33, 0.25, 0.19, 0.15], MAT_SKIN)
    sphere('HandL', (2.47, 0.90, 1.44), (0.20, 0.16, 0.24), MAT_SKIN)
    # claws: hind toes point forward, fore toes shorter, the raised hand
    # carries four long claws curled around the trunk (aimed down/in)
    claws = []
    for dy in (-0.095, 0.0, 0.095):   # hind toes, both feet
        claws.append(((-0.72, 1.00 + dy, 0.075), (-0.52, 1.00 + dy, 0.015), 0.048))
        claws.append(((-0.80, -0.95 + dy, 0.07), (-0.61, -0.95 + dy, 0.012), 0.046))
    for dy in (-0.085, -0.028, 0.028, 0.085):   # planted forefoot toes
        claws.append(((2.15, -0.85 + dy, 0.055), (2.29, -0.85 + dy, 0.012), 0.034))
    grip = [((2.52, 1.02, 1.52), (2.62, 1.10, 1.28), 0.036),
            ((2.56, 0.92, 1.56), (2.68, 0.94, 1.30), 0.038),
            ((2.52, 0.80, 1.52), (2.62, 0.72, 1.28), 0.036),
            ((2.42, 0.88, 1.62), (2.48, 0.88, 1.40), 0.032)]
    claws += grip
    merged_cones('Claws', claws, MAT_BONE)

# ----------------------------------------------------------------------------
# the reddish conifer trunk the animal is pulling at
def build_trunk():
    tube('Trunk', [(3.32, 0.68, -0.06), (3.06, 0.77, 0.45), (2.74, 0.84, 0.95),
                   (2.50, 0.88, 1.32), (2.40, 0.87, 1.52)],
         [0.175, 0.155, 0.14, 0.125, 0.10], MAT_TRUNK, nseg=12)

# ----------------------------------------------------------------------------
# simple ground / rock base: a low displaced earth mound
def build_base():
    import random
    random.seed(1854)
    nx, ny = 46, 26
    sx, sy = 12.6, 7.2
    verts, faces = [], []
    for j in range(ny):
        for i in range(nx):
            x = -sx / 2 + sx * i / (nx - 1)
            y = -sy / 2 + sy * j / (ny - 1)
            dx, dy = (x - 0.1) / 5.9, y / 3.15
            f = max(0.0, 1.0 - dx * dx - dy * dy)
            z = 0.02 + 0.11 * f ** 1.4
            z += f * (0.022 * math.sin(x * 2.1 + 0.7) * math.cos(y * 1.8)
                      + 0.013 * math.sin(x * 5.1 + 1.9) * math.sin(y * 4.3))
            verts.append((x, y, z))
    for j in range(ny - 1):
        for i in range(nx - 1):
            a = j * nx + i
            faces.append((a, a + 1, a + 1 + nx, a + nx))
    make_mesh('GroundBase', verts, faces, MAT_EARTH, smooth_shade=True)

# ----------------------------------------------------------------------------
def main():
    build_body()
    build_head()
    build_legs()
    build_trunk()
    build_base()

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    dg = bpy.context.evaluated_depsgraph_get()
    tris = 0
    nobjs = 0
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH':
            nobjs += 1
            ev = ob.evaluated_get(dg)
            me = ev.to_mesh()
            me.calc_loop_triangles()
            tris += len(me.loop_triangles)
            ev.to_mesh_clear()
    xs = [v.co.x for ob in bpy.context.scene.objects if ob.type == 'MESH' for v in ob.data.vertices]
    ys = [v.co.y for ob in bpy.context.scene.objects if ob.type == 'MESH' for v in ob.data.vertices]
    zs = [v.co.z for ob in bpy.context.scene.objects if ob.type == 'MESH' for v in ob.data.vertices]
    print(f'STATS objects={nobjs} tris={tris}')
    print(f'STATS bbox x {min(xs):.3f}..{max(xs):.3f}  y {min(ys):.3f}..{max(ys):.3f}  z {min(zs):.3f}..{max(zs):.3f}')
    print(f'STATS dims x={max(xs)-min(xs):.3f} y={max(ys)-min(ys):.3f} z={max(zs)-min(zs):.3f}')

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, 'iguanodon.blend'))
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT, 'iguanodon.glb'),
                              export_format='GLB', export_apply=True)
    print('BUILD DONE')

if __name__ == '__main__':
    main()
