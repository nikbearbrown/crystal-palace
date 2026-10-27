#!/usr/bin/env python3
"""
Build alhambra-lion-fountain: the Fountain of the Lions in Owen Jones's
Alhambra Court, Sydenham (film scene CP041).

Evidence (all in-repo — see NOTES.md):
- Coloured print "Entrance to the Alhambra Court" (PD): the fountain
  centre-left — standing lions with ribbed manes spouting from their
  mouths, polygonal basin carried on their backs, upper basin + jet.
- 1856 guide p.66 woodcut of the same view: clearer structure —
  upper bowl with falling arcs, basin fascia, lions in a row.
- 1856 guide p.67 plan: dodecagonal fountain at the centre of the
  Court of the Lions; p.68: court 75 ft long, "the fountain supported
  by the lions"; p.69: Arabic poem round the basin (band here is
  abstract knot-blocks, NO letterforms — the print resolves none).

Dimensions adopted (chain in NOTES.md): basin 2.70 m across vertices
from the plan ratio against the guide's 75 ft court; heights as
fractions of basin diameter read off the two views.

Run: blender -b --python scripts/build_alhambra_lion_fountain.py
"""
import bpy
import math
import os
from mathutils import Vector

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = "alhambra-lion-fountain"
D = math.radians

# ---------------------------------------------------------------- clean
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'

WATER = bpy.data.collections.new("Water")
scene.collection.children.link(WATER)

# ---------------------------------------------------------------- mats
def mat(name, rgb, rough=0.9, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Roughness"].default_value = rough
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        m.surface_render_method = 'DITHERED'
    return m

STONE = mat("StonePale", (0.78, 0.72, 0.62), 0.85)        # lions, column
STONE_WHITE = mat("StoneBasin", (0.85, 0.81, 0.72), 0.8)  # basins
PLINTH_M = mat("StonePlinth", (0.52, 0.48, 0.41), 0.95)
DARK = mat("DetailDark", (0.13, 0.11, 0.09), 0.7)
WATER_M = mat("Water", (0.72, 0.83, 0.88), 0.12, alpha=0.5)

# fascia band: image texture (abstract knot blocks), colour + bump
FASCIA = bpy.data.materials.new("FasciaBand")
FASCIA.use_nodes = True
nt = FASCIA.node_tree
fb = nt.nodes["Principled BSDF"]
fb.inputs["Roughness"].default_value = 0.85
tex = nt.nodes.new("ShaderNodeTexImage")
tex.image = bpy.data.images.load(os.path.join(BASE, "textures", "fascia_band.png"))
tex.extension = 'REPEAT'
bump = nt.nodes.new("ShaderNodeBump")
bump.inputs["Strength"].default_value = 0.3
bump.inputs["Distance"].default_value = 0.012
nt.links.new(tex.outputs["Color"], fb.inputs["Base Color"])
nt.links.new(tex.outputs["Color"], bump.inputs["Height"])
nt.links.new(bump.outputs["Normal"], fb.inputs["Normal"])

# ---------------------------------------------------------------- helpers
def lathe(name, profile, steps=48, material=None, flute=0.0, flute_n=12,
          uv_repeat_u=1.0, band=None):
    """Surface of revolution from (r, z) profile points (bottom -> top).
    band=(z0, z1, material_index_material): faces whose midpoint z lies in
    [z0, z1] get material slot 1 (material passed as `band_mat`)."""
    band_mat = band[2] if band else None
    verts, faces, uvs, fmat = [], [], [], []
    # cumulative v along profile
    vs = [0.0]
    for i in range(1, len(profile)):
        dr = profile[i][0] - profile[i - 1][0]
        dz = profile[i][1] - profile[i - 1][1]
        vs.append(vs[-1] + math.hypot(dr, dz))
    total = vs[-1] or 1.0
    for j, (r, z) in enumerate(profile):
        vj = vs[j] / total
        if band:
            # rows inside the band get v remapped to 0..1 across the band,
            # so the band texture is sampled over its full height
            if band[0] - 1e-9 <= z <= band[1] + 1e-9:
                vj = (z - band[0]) / (band[1] - band[0])
        for i in range(steps):
            th = 2 * math.pi * i / steps
            rr = r * (1.0 + flute * math.cos(flute_n * th)) if flute else r
            verts.append((rr * math.cos(th), rr * math.sin(th), z))
            uvs.append((i / steps * uv_repeat_u, vj))
    for j in range(len(profile) - 1):
        zmid = 0.5 * (profile[j][1] + profile[j + 1][1])
        mi = 0
        if band and band[0] <= zmid <= band[1]:
            mi = 1
        for i in range(steps):
            a = j * steps + i
            b = j * steps + (i + 1) % steps
            c = (j + 1) * steps + (i + 1) % steps
            d2 = (j + 1) * steps + i
            faces.append((a, b, c, d2))
            fmat.append(mi)
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    for p, mi in zip(me.polygons, fmat):
        p.material_index = mi
    uv = me.uv_layers.new(name="UVMap")
    idx = 0
    for f in faces:
        for vi in f:
            uv.data[idx].uv = uvs[vi]
            idx += 1
    ob = bpy.data.objects.new(name, me)
    scene.collection.objects.link(ob)
    if material:
        me.materials.append(material)
    if band_mat:
        me.materials.append(band_mat)
    for p in me.polygons:
        p.use_smooth = True
    return ob

def shade(ob, smooth=True):
    for p in ob.data.polygons:
        p.use_smooth = smooth
    return ob

def sph(name, loc, scale, material, seg=10, rings=7):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings,
                                         location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    if material:
        o.data.materials.append(material)
    return shade(o)

def cyl(name, loc, r1, r2, depth, material, verts=8):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2,
                                    depth=depth, location=loc)
    o = bpy.context.active_object
    o.name = name
    if material:
        o.data.materials.append(material)
    return shade(o)

def tube(name, points, radius, material, collection=None):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = radius
    cu.bevel_resolution = 1
    cu.resolution_u = 5
    sp = cu.splines.new('BEZIER')
    sp.bezier_points.add(len(points) - 1)
    for bp, co in zip(sp.bezier_points, points):
        bp.co = co
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'
    ob = bpy.data.objects.new(name, cu)
    (collection or scene.collection).objects.link(ob)
    if material:
        cu.materials.append(material)
    return ob

def to_water(ob):
    """Move an object from the scene collection into the Water collection."""
    for coll in list(ob.users_collection):
        coll.objects.unlink(ob)
    WATER.objects.link(ob)
    return ob

# ---------------------------------------------------------------- plinth
# step ring + plinth, dodecagonal (same 12-fold rhythm as the basin)
lathe("StepRing", [(0.0, 0.0), (1.80, 0.0), (1.80, 0.07), (1.72, 0.07),
                   (1.72, 0.09), (0.0, 0.09)], steps=12, material=PLINTH_M)
lathe("Plinth", [(0.0, 0.07), (1.65, 0.07), (1.65, 0.19), (1.58, 0.21),
                 (0.0, 0.21)], steps=12, material=PLINTH_M)

# ---------------------------------------------------------------- basin
# dodecagonal: vertex radius 1.35 -> 2.70 m across vertices, 2.61 across flats.
# Underside z=1.03 rests on the lions' backs (0.21 plinth + 0.82 lion).
basin_profile = [
    (0.00, 1.06), (0.70, 1.045), (1.10, 1.035), (1.26, 1.03),   # underside
    (1.335, 1.055), (1.35, 1.10),                                # cove to wall
    (1.362, 1.115), (1.362, 1.235),                              # fascia band (proud)
    (1.35, 1.25), (1.368, 1.285), (1.352, 1.315),                # rim roll, top 1.315
    (1.27, 1.30), (1.245, 1.24), (1.24, 1.14),                   # inner lip + wall
    (0.00, 1.13),                                                # basin floor
]
lathe("MainBasin", basin_profile, steps=12, material=STONE_WHITE,
      band=(1.11, 1.24, FASCIA), uv_repeat_u=12.0)

# basin water (hideable)
wb = lathe("Water_Basin", [(0.0, 1.238), (1.20, 1.238), (1.238, 1.232)],
           steps=12, material=WATER_M)
to_water(wb)

# ---------------------------------------------------------------- column
lathe("CentralColumn", [
    (0.0, 1.12), (0.30, 1.12), (0.30, 1.17), (0.17, 1.24), (0.135, 1.34),
    (0.125, 1.50), (0.185, 1.565), (0.19, 1.60), (0.125, 1.66),
    (0.125, 1.86), (0.17, 1.93), (0.0, 1.95),
], steps=36, material=STONE)

# ---------------------------------------------------------------- upper basin
# fluted drum (the coloured print's reading) under a shallow bowl
lathe("UpperBasin", [
    (0.0, 1.93), (0.40, 1.93), (0.50, 1.96), (0.52, 2.00),
    (0.525, 2.06),                       # fluted drum band
    (0.55, 2.10), (0.575, 2.145), (0.565, 2.165),   # rim
    (0.50, 2.13), (0.44, 2.05), (0.0, 2.03),
], steps=72, material=STONE_WHITE, flute=0.028, flute_n=12)
uw = lathe("Water_Upper", [(0.0, 2.095), (0.46, 2.095), (0.495, 2.09)],
           steps=36, material=WATER_M)
to_water(uw)

# nozzle + jet
lathe("Nozzle", [(0.0, 2.10), (0.055, 2.10), (0.05, 2.17), (0.028, 2.22),
                 (0.0, 2.23)], steps=16, material=STONE)
jet = cyl("Water_Jet", (0, 0, 2.50), 0.016, 0.034, 0.56, WATER_M, verts=10)
to_water(jet)

# ---------------------------------------------------------------- the lion
# Stylised standing lion, built facing +X, feet at z=0 (stands on plinth
# top z=0.21 in the scene). Back top at 0.82 -> meets basin underside.
# The prints' most legible traits: blocky body, columnar legs, a mane of
# strong horizontal ribs, head up, mouth open spouting. No other detail
# is resolved at the prints' scale, so none is invented.
def build_lion():
    parts = []
    # body masses
    parts.append(sph("haunch", (-0.17, 0, 0.53), (0.20, 0.155, 0.185), STONE))
    parts.append(sph("barrel", (0.0, 0, 0.565), (0.26, 0.15, 0.175), STONE))
    parts.append(sph("chest", (0.185, 0, 0.56), (0.185, 0.15, 0.20), STONE))
    # legs + paws
    for sx, lx in ((1, 0.235), (-1, -0.255)):
        for sy in (1, -1):
            parts.append(cyl("leg", (lx, sy * 0.125, 0.21), 0.060, 0.050,
                             0.42, STONE, verts=8))
            parts.append(sph("paw", (lx + 0.025, sy * 0.125, 0.032),
                             (0.062, 0.048, 0.032), STONE, seg=8, rings=6))
    # ribbed mane: stack of tori on the neck axis (axis along X)
    for i, (mx, mr) in enumerate(((0.24, 0.152), (0.295, 0.160),
                                  (0.35, 0.156), (0.405, 0.144),
                                  (0.455, 0.128))):
        bpy.ops.mesh.primitive_torus_add(major_radius=mr, minor_radius=0.034,
                                         major_segments=12, minor_segments=5,
                                         location=(mx, 0, 0.63))
        t = bpy.context.active_object
        t.name = "mane"
        t.rotation_euler = (0, D(90), 0)
        t.scale = (1.0, 0.94, 1.04)
        bpy.ops.object.transform_apply(scale=True)
        t.data.materials.append(STONE)
        parts.append(shade(t))
    # head
    parts.append(sph("head", (0.555, 0, 0.70), (0.105, 0.098, 0.104), STONE))
    parts.append(sph("muzzle", (0.655, 0, 0.645), (0.070, 0.064, 0.056), STONE))
    parts.append(sph("jaw", (0.64, 0, 0.575), (0.060, 0.054, 0.040), STONE))
    for sy in (1, -1):
        parts.append(sph("ear", (0.47, sy * 0.078, 0.752),
                         (0.024, 0.015, 0.026), STONE, seg=7, rings=5))
        parts.append(sph("eye", (0.625, sy * 0.066, 0.735),
                         (0.016, 0.014, 0.016), DARK, seg=7, rings=5))
    parts.append(sph("nose", (0.715, 0, 0.675), (0.022, 0.028, 0.018), DARK,
                     seg=7, rings=5))
    # open mouth: dark slot under the muzzle
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.69, 0, 0.61))
    mo = bpy.context.active_object
    mo.name = "mouth"
    mo.scale = (0.020, 0.034, 0.011)
    bpy.ops.object.transform_apply(scale=True)
    mo.data.materials.append(DARK)
    parts.append(mo)
    # tail: rises along the rear flank, tuft at the top (as drawn at Granada
    # and hinted in the print's left-most lion)
    parts.append(tube("tail", [(-0.345, -0.10, 0.42), (-0.40, -0.155, 0.55),
                               (-0.375, -0.165, 0.72)], 0.020, STONE))
    parts.append(sph("tuft", (-0.37, -0.165, 0.76), (0.034, 0.034, 0.048),
                     STONE, seg=8, rings=6))
    # join into one mesh
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    lion = bpy.context.active_object
    lion.name = "LionMaster"
    return lion

lion = build_lion()
# ring of twelve, one centred under each basin side, heads outward
R_LION = 0.98
for k in range(12):
    th = D(30 * k)
    if k == 0:
        ob = lion
    else:
        ob = lion.copy()  # shares mesh data
        scene.collection.objects.link(ob)
    ob.name = f"Lion_{k + 1:02d}"
    ob.location = (R_LION * math.cos(th), R_LION * math.sin(th), 0.21)
    ob.rotation_euler = (0, 0, th)

# ---------------------------------------------------------------- water arcs
# upper bowl overflow: 8 arcs falling into the main basin
for k in range(8):
    th = D(45 * k + 22.5)
    c, s = math.cos(th), math.sin(th)
    pts = [(0.56 * c, 0.56 * s, 2.10), (0.72 * c, 0.72 * s, 1.94),
           (0.90 * c, 0.90 * s, 1.62), (1.02 * c, 1.02 * s, 1.26)]
    to_water(tube(f"Water_Overflow_{k + 1}", pts, 0.016, WATER_M))
# lion mouth spouts: from each mouth arcing out to the step ring
for k in range(12):
    th = D(30 * k)
    c, s = math.cos(th), math.sin(th)
    r0 = R_LION + 0.70
    pts = [(r0 * c, r0 * s, 0.21 + 0.595), ((r0 + 0.10) * c, (r0 + 0.10) * s, 0.71),
           ((r0 + 0.155) * c, (r0 + 0.155) * s, 0.42),
           ((r0 + 0.175) * c, (r0 + 0.175) * s, 0.10)]
    to_water(tube(f"Water_Spout_{k + 1:02d}", pts, 0.013, WATER_M))

# ---------------------------------------------------------------- save
for ob in bpy.data.objects:
    ob.select_set(False)

blend_path = os.path.join(BASE, SLUG + ".blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
glb_path = os.path.join(BASE, SLUG + ".glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB',
                          export_apply=True)

# stats from the evaluated scene
dg = bpy.context.evaluated_depsgraph_get()
tris = 0
for ob in bpy.data.objects:
    if ob.type in ('MESH', 'CURVE'):
        ev = ob.evaluated_get(dg)
        me = bpy.data.meshes.new_from_object(ev, depsgraph=dg)
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        bpy.data.meshes.remove(me)
import itertools
corners = []
for ob in bpy.data.objects:
    if ob.type in ('MESH', 'CURVE'):
        for c in ob.bound_box:
            corners.append(ob.matrix_world @ Vector(c))
mn = Vector((min(c.x for c in corners), min(c.y for c in corners),
             min(c.z for c in corners)))
mx = Vector((max(c.x for c in corners), max(c.y for c in corners),
             max(c.z for c in corners)))
print(f"OBJECTS {len(bpy.data.objects)}")
print(f"TRIANGLES {tris}")
print(f"BBOX {mx.x - mn.x:.3f} x {mx.y - mn.y:.3f} x {mx.z - mn.z:.3f} m")
print(f"BLEND {blend_path} {os.path.getsize(blend_path)} bytes")
print(f"GLB {glb_path} {os.path.getsize(glb_path)} bytes")
print("BUILD DONE")
