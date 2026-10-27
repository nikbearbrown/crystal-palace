#!/usr/bin/env python3
"""Build the terrace-statue-survivor prop for the Crystal Palace film.

The surviving headless draped statue on the Sydenham Upper Terrace,
AS IT STANDS TODAY (present-day park state; CP072/CP076 family).
Source: one modern photograph, rear three-quarter only
(refs/headless-statue-geograph-2436241.jpg, CC BY-SA 2.0).
The head and arms are lost in reality; nothing is restored.

Blender 4.2, headless, procedural. Units: metres. Z up.
Figure front = -Y. Figure's left = +X. Origin at base centre
(bottom of pedestal, z = 0).
"""
import bpy
import math
import os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

FIGURE_H = 3.00          # adopted, see NOTES.md scale chain
PED_H = 1.02             # pedestal height, photo-proportioned

# ----------------------------------------------------------------------------
# scene reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ----------------------------------------------------------------------------
# materials
def stone_material(name, dark, light, blotch_scale=1.6, grain_scale=7.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes['Principled BSDF']
    bsdf.inputs['Roughness'].default_value = 0.95
    tex = nt.nodes.new('ShaderNodeTexCoord')
    noise_big = nt.nodes.new('ShaderNodeTexNoise')
    noise_big.inputs['Scale'].default_value = blotch_scale
    noise_big.inputs['Detail'].default_value = 3.0
    noise_big.inputs['Roughness'].default_value = 0.8
    noise_grain = nt.nodes.new('ShaderNodeTexNoise')
    noise_grain.inputs['Scale'].default_value = grain_scale
    noise_grain.inputs['Detail'].default_value = 4.0
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'FLOAT'
    mix.inputs[0].default_value = 0.35
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.25
    ramp.color_ramp.elements[0].color = (*dark, 1.0)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (*light, 1.0)
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.45
    bump.inputs['Distance'].default_value = 0.03
    nt.links.new(tex.outputs['Generated'], noise_big.inputs['Vector'])
    nt.links.new(tex.outputs['Generated'], noise_grain.inputs['Vector'])
    nt.links.new(noise_big.outputs['Fac'], mix.inputs[1])
    nt.links.new(noise_grain.outputs['Fac'], mix.inputs[2])
    nt.links.new(mix.outputs[0], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    nt.links.new(mix.outputs[0], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat

MAT_FIGURE = stone_material('WeatheredStoneFigure',
                            (0.135, 0.140, 0.125), (0.340, 0.350, 0.325))
MAT_PEDESTAL = stone_material('WeatheredStonePedestal',
                              (0.225, 0.218, 0.195), (0.420, 0.410, 0.380),
                              blotch_scale=2.2, grain_scale=5.0)
MAT_DARK = bpy.data.materials.new('CavityDark')
MAT_DARK.use_nodes = True
MAT_DARK.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.030, 0.030, 0.028, 1.0)
MAT_DARK.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 1.0

# ----------------------------------------------------------------------------
# helpers
def make_mesh(name, verts, faces, mat):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    if mat:
        me.materials.append(mat)
    return ob

def smooth(ob):
    for p in ob.data.polygons:
        p.use_smooth = True

# ----------------------------------------------------------------------------
# the figure: lofted drapery mass
# profile(z) -> (rx half-width, ry half-depth), z local 0..FIGURE_H
PROFILE = [
    (0.00, 0.575, 0.435),
    (0.06, 0.565, 0.425),
    (0.15, 0.535, 0.405),
    (0.30, 0.505, 0.385),
    (0.55, 0.470, 0.360),
    (0.85, 0.440, 0.340),
    (1.15, 0.435, 0.335),
    (1.45, 0.458, 0.352),
    (1.62, 0.478, 0.368),   # fold roll at skirt top
    (1.74, 0.452, 0.350),
    (2.00, 0.442, 0.350),
    (2.25, 0.458, 0.368),
    (2.50, 0.478, 0.382),   # shoulder mass
    (2.66, 0.452, 0.360),
    (2.80, 0.385, 0.312),
    (2.90, 0.300, 0.255),
    (2.97, 0.215, 0.190),
    (3.00, 0.120, 0.110),
]

def profile_at(z):
    if z <= PROFILE[0][0]:
        return PROFILE[0][1], PROFILE[0][2]
    for i in range(len(PROFILE) - 1):
        z0, rx0, ry0 = PROFILE[i]
        z1, rx1, ry1 = PROFILE[i + 1]
        if z <= z1:
            t = (z - z0) / (z1 - z0)
            t = t * t * (3 - 2 * t)
            return rx0 + (rx1 - rx0) * t, ry0 + (ry1 - ry0) * t
    return PROFILE[-1][1], PROFILE[-1][2]

def gauss(x, mu, sig):
    return math.exp(-((x - mu) ** 2) / (2 * sig * sig))

def build_figure():
    SEG = 128
    RINGS = []
    z = 0.0
    while z < FIGURE_H - 1e-6:
        RINGS.append(z)
        # denser rings near hem and shoulders
        z += 0.055 if (z < 0.35 or z > 2.3) else 0.085
    RINGS.append(FIGURE_H)
    verts = []
    faces = []
    for zi, zl in enumerate(RINGS):
        rx, ry = profile_at(zl)
        # flute amplitude by height: strong at hem, weak mid, streaks on dome
        if zl < 1.5:
            amp = 0.078 - 0.042 * (zl / 1.5)
        elif zl < 2.6:
            amp = 0.020
        else:
            amp = 0.048
        phase = 0.55 * math.sin(zl * 1.15) + 0.25 * zl
        for si in range(SEG):
            th = 2 * math.pi * si / SEG
            ct, st = math.cos(th), math.sin(th)
            c13 = math.cos(13 * th + phase)
            c13 = math.copysign(abs(c13) ** 0.7, c13)   # crisper ridges
            flute = (amp * c13
                     + 0.45 * amp * math.cos(27 * th - phase * 0.7)
                     + 0.020 * math.cos(5 * th + 1.3) * (1.0 if zl < 1.7 else 0.4))
            r_scale = 1.0 + flute
            x = rx * ct * r_scale
            y = ry * st * r_scale
            # slight lopsided lean of the dome toward the figure's right (-X)
            x -= 0.022 * gauss(zl, 2.95, 0.22)
            # subtle diagonal groove across the front (inferred himation line)
            # front centre is th = 3*pi/2 in this parametrisation
            if st < 0:
                u = th - 1.5 * math.pi
                if abs(u) < 0.65:
                    zline = 2.20 - 0.58 * u
                    y += 0.010 * gauss(zl, zline, 0.10)  # front is -Y: +y = inward
            # back mass: broad bulge on +Y (the back) at hip height
            if st > 0:
                y += 0.030 * st * gauss(zl, 1.45, 0.55)
            # chest suggestion on the front (-Y), inferred
            if st < 0:
                y -= 0.022 * (-st) * gauss(zl, 2.32, 0.30)
            # the cavity: deep dent on the figure's left flank (+X)
            ang2 = math.atan2(x, y)   # angle from +Y axis; +X flank = +pi/2
            dent = (0.23 * gauss(zl, 2.08, 0.24)
                    * math.exp(-((ang2 - math.pi / 2) ** 2) / (2 * 0.60 ** 2)))
            if dent > 0.001 and x > 0:
                # pull the point in along X (into the flank)
                x -= dent * max(ct, 0.0)
            verts.append((x, y, zl + PED_H))
        if zi > 0:
            base = (zi - 1) * SEG
            cur = zi * SEG
            for si in range(SEG):
                sj = (si + 1) % SEG
                faces.append((base + si, base + sj, cur + sj, cur + si))
    # cap the dome top with a fan to a centre point
    cx, cy = 0.0, 0.0
    top_idx = len(verts)
    verts.append((cx, cy, FIGURE_H + 0.055 + PED_H))
    last = (len(RINGS) - 1) * SEG
    for si in range(SEG):
        sj = (si + 1) % SEG
        faces.append((last + si, last + sj, top_idx))
    # bottom cap (sits on plinth, unseen) fan downward
    bot_idx = len(verts)
    verts.append((0.0, 0.0, PED_H - 0.01))
    for si in range(SEG):
        sj = (si + 1) % SEG
        faces.append((sj, si, bot_idx))
    ob = make_mesh('Figure', verts, faces, MAT_FIGURE)
    smooth(ob)
    return ob

def build_cavity_cup():
    # two overlapping dark shells sunk into the dent, for an irregular
    # broken-hollow outline rather than one clean oval
    made = []
    for name, sc, loc, rz in [
        ('CavityInterior', (0.125, 0.150, 0.235), (0.300, 0.03, 2.06 + PED_H), 0.30),
        ('CavityInterior2', (0.095, 0.115, 0.150), (0.315, -0.055, 1.86 + PED_H), -0.25),
    ]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16,
                                             location=(0.0, 0.0, 0.0))
        ob = bpy.context.object
        ob.name = name
        ob.scale = sc
        ob.rotation_euler = (0, 0, rz)
        ob.location = loc
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        ob.data.materials.append(MAT_DARK)
        smooth(ob)
        made.append(ob)
    return made

def ribbon(name, path_pts, width, thick, fold_period=0.17, fold_amp=0.010):
    """Sweep a shallow-arc ribbon along path_pts (list of Vector on/near the
    body). Cross-section: 5 points, arc bulging along the local outward
    normal (path point direction from the body axis)."""
    verts = []
    faces = []
    up = Vector((0, 0, 1))
    for i, p in enumerate(path_pts):
        outward = Vector((p.x, p.y, 0.0))
        if outward.length < 1e-6:
            outward = Vector((0, 1, 0))
        outward.normalize()
        tangent = Vector((0, 0, 1))
        side = tangent.cross(outward).normalized()
        bulge = fold_amp * math.sin(i * 0.9)
        for j, s in enumerate((-1.0, -0.5, 0.0, 0.5, 1.0)):
            arc = thick * (1.0 - (s ** 2)) + bulge * (1.0 - abs(s))
            v = p + side * (s * width / 2) + outward * arc
            verts.append(tuple(v))
        if i > 0:
            b0 = (i - 1) * 5
            b1 = i * 5
            for j in range(4):
                faces.append((b0 + j, b0 + j + 1, b1 + j + 1, b1 + j))
    ob = make_mesh(name, verts, faces, MAT_FIGURE)
    smooth(ob)
    return ob

def body_point(theta_deg, z, out=0.012):
    """Point on the figure surface at angle theta (deg, 0=+Y back,
    90=+X left flank, 180=-Y front, 270=-X right flank)."""
    rx, ry = profile_at(z)
    th = math.radians(theta_deg)
    x = rx * math.sin(th)
    y = ry * math.cos(th)
    r = math.hypot(x / rx, y / ry)
    x *= (1 + out)
    y *= (1 + out)
    return Vector((x, y, z + PED_H))

def build_swag_back():
    pts = []
    n = 26
    for i in range(n + 1):
        t = i / n
        theta = -52 + t * 118          # from back-right over the back to left
        z = 2.62 - t * 0.95             # descending diagonal
        pts.append(body_point(theta, z, out=0.015))
    main = ribbon('SwagBack', pts, width=0.30, thick=0.034, fold_amp=0.006)
    # a thinner companion roll just above it: the bundle reads as folded cloth
    pts2 = []
    for i in range(n + 1):
        t = i / n
        theta = -50 + t * 116
        z = 2.76 - t * 0.95
        pts2.append(body_point(theta, z, out=0.012))
    comp = ribbon('SwagBackRoll', pts2, width=0.13, thick=0.026, fold_amp=0.004)
    return [main, comp]

def build_flap():
    # hanging pointed flap of drapery on the back-right, from photo
    verts = []
    faces = []
    rows, cols = 9, 7
    for i in range(rows):
        t = i / (rows - 1)              # 0 top -> 1 bottom
        z = 2.52 - t * 0.62
        theta_c = -38 + 6 * math.sin(t * 2.2)
        width = 0.30 * (1 - 0.45 * t) * (1 - 0.35 * max(0.0, t - 0.75) * 4)
        for j in range(cols):
            s = j / (cols - 1) - 0.5
            theta = theta_c + s * 34
            p = body_point(theta, z, out=0.018 + 0.03 * t)
            p.z -= 0.05 * (s ** 2) * t  # edges curl down slightly
            verts.append(tuple(p))
        if i > 0:
            b0 = (i - 1) * cols
            b1 = i * cols
            for j in range(cols - 1):
                faces.append((b0 + j, b0 + j + 1, b1 + j + 1, b1 + j))
    ob = make_mesh('HimationFlap', verts, faces, MAT_FIGURE)
    smooth(ob)
    return ob

def simple_foot(name, cx, cy, ang_deg, scale=1.0):
    """Schematic bare foot: squashed loft + toe bumps, pointing -Y rotated."""
    parts = []
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=10,
                                         location=(cx, cy, PED_H + 0.055))
    ob = bpy.context.object
    ob.name = name
    ob.scale = (0.075 * scale, 0.16 * scale, 0.052 * scale)
    ob.rotation_euler = (0, 0, math.radians(ang_deg))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=False)
    ob.rotation_euler = (0, 0, 0)
    # toes: 4 small spheres at the front end
    toe_base = Vector((cx, cy, PED_H + 0.045))
    fwd = Vector((math.sin(math.radians(ang_deg)), -math.cos(math.radians(ang_deg)), 0))
    sidev = Vector((fwd.y, -fwd.x, 0))
    toes = []
    for k, (off, r) in enumerate([(-0.036, 0.020), (-0.012, 0.023), (0.012, 0.021), (0.034, 0.017)]):
        loc = toe_base + fwd * (0.145 * scale) + sidev * (off * scale)
        loc.z = PED_H + 0.030
        bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, location=tuple(loc))
        t = bpy.context.object
        t.name = name + '_toe'
        t.scale = (r * scale, r * 1.35 * scale, r * 0.8 * scale)
        toes.append(t)
    for o in [ob] + toes:
        o.data.materials.append(MAT_FIGURE)
        smooth(o)
    return [ob] + toes

def build_pedestal():
    def box(name, sx, sy, sz, zc, mat=MAT_PEDESTAL, bevel=0.012):
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, zc))
        ob = bpy.context.object
        ob.name = name
        ob.dimensions = (sx, sy, sz)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if bevel:
            mod = ob.modifiers.new('bev', 'BEVEL')
            mod.width = bevel
            mod.segments = 2
            bpy.ops.object.modifier_apply(modifier='bev')
        ob.data.materials.append(mat)
        return ob
    made = []
    made.append(box('PedestalCorbel1', 2.02, 1.48, 0.10, 0.05))
    made.append(box('PedestalCorbel2', 1.95, 1.42, 0.09, 0.145))
    made.append(box('PedestalCorbel3', 1.89, 1.37, 0.09, 0.235))
    made.append(box('PedestalBlock',   1.86, 1.34, 0.44, 0.50))
    made.append(box('PedestalNeck',    1.68, 1.18, 0.14, 0.79))
    made.append(box('PedestalSlab',    1.82, 1.32, 0.16, 0.94))
    return made

def main():
    build_pedestal()
    build_figure()
    build_cavity_cup()
    build_swag_back()
    build_flap()
    simple_foot('FootLeft', 0.20, -0.375, -8, scale=1.15)
    # right foot: only a toe-tip hint at the hem
    simple_foot('FootRightHint', -0.20, -0.315, 6, scale=0.55)

    # apply all transforms
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # stats
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
    print(f'STATS objects={nobjs} tris={tris}')
    print(f'STATS bbox x {min(xs):.3f}..{max(xs):.3f}  y {min(ys):.3f}..{max(ys):.3f}')

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, 'terrace-statue-survivor.blend'))
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT, 'terrace-statue-survivor.glb'),
                              export_format='GLB', export_apply=True)
    print('BUILD DONE')

if __name__ == '__main__':
    main()
