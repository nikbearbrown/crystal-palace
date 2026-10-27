#!/usr/bin/env python3
"""Lattice girder / truss bay — Hyde Park 1851, one 24 ft module.

Three parts (see NOTES.md for provenance):
  A. Cast-iron lattice girder, Downes PL.10 Fig.3 (24 ft span, ~3 ft 2 in deep)
  B. One 24 ft bay (3 panels) of the wrought-iron 48 ft roof truss, PL.11 Fig.I
     (5 ft 6 in deep plate-measured), shown above the girder with a gap —
     the two are alternative members, stacked for comparison, NOT an assembly.
  C. Short cruciform column stubs under the girder ends (end conditions only).
Units: metres. Origin at base centre (underside of stubs).
"""
import bpy, math
from mathutils import Vector

# ---------- clean scene ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ---------- materials ----------
def mat(name, rgb, rough=0.6, metal=0.35):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m

CAST_IRON = mat("CastIron_painted", (0.145, 0.165, 0.155), 0.62, 0.25)
WROUGHT   = mat("WroughtIron_painted", (0.185, 0.19, 0.185), 0.55, 0.35)
ENDPOST   = mat("EndPost_iron", (0.16, 0.165, 0.16), 0.6, 0.3)

FT = 0.3048
SPAN = 24 * FT            # 7.3152 m, printed on both plates
HX = SPAN / 2.0

def box(name, cx, cy, cz, sx, sy, sz, material, rotz=0.0, collection=None):
    bpy.ops.mesh.primitive_cube_add(location=(cx, cy, cz))
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = (sx, sy, sz)
    if rotz:
        ob.rotation_euler = (0, 0, rotz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if rotz:
        ob.rotation_euler = (0, 0, rotz)
    if material:
        ob.data.materials.append(material)
    if collection:
        for c in ob.users_collection:
            c.objects.unlink(ob)
        collection.objects.link(ob)
    return ob

def bar_between(name, p1, p2, width, thick, material, collection, y=0.0):
    """Flat bar in the X-Z plane between two (x,z) points, at offset y."""
    x1, z1 = p1; x2, z2 = p2
    length = math.hypot(x2 - x1, z2 - z1)
    ang = math.atan2(z2 - z1, x2 - x1)
    bpy.ops.mesh.primitive_cube_add(location=((x1 + x2) / 2, y, (z1 + z2) / 2))
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = (length, thick, width)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.rotation_euler = (0, -ang, 0)
    if material:
        ob.data.materials.append(material)
    if collection:
        for c in ob.users_collection:
            c.objects.unlink(ob)
        collection.objects.link(ob)
    return ob

def cruciform(name, cx, z_base, height, arm, web_t, material, collection):
    box(name + "_v", cx, 0, z_base + height / 2, web_t, arm, height, material, collection=collection)
    box(name + "_h", cx, 0, z_base + height / 2, arm, web_t, height, material, collection=collection)

def coll(name):
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    return c

# =====================================================================
# C. Column stubs (end conditions) — cruciform, PL.11 standard section
# =====================================================================
cC = coll("ColumnStubs")
STUB_H = 0.45
for sx in (-1, 1):
    cruciform(f"Stub_{'L' if sx<0 else 'R'}", sx * HX, 0.0, STUB_H, 0.28, 0.045, CAST_IRON, cC)
    box(f"StubBase_{'L' if sx<0 else 'R'}", sx * HX, 0, 0.03, 0.42, 0.42, 0.06, CAST_IRON, collection=cC)

# =====================================================================
# A. Cast-iron lattice girder — PL.10 Fig.3.  z: STUB_H .. STUB_H+0.965
# =====================================================================
cA = coll("Girder_PL10_Fig3")
GZ = STUB_H
GD = 0.965                      # overall depth ~3 ft 2 in (printed 3'1¼" in plate chain)
FL_T = 0.028                    # flange thickness (inferred)
WEB_T = 0.022                   # lattice web thickness (inferred)
# top chord: T — flange + web stub below
box("G_top_flange", 0, 0, GZ + GD - FL_T / 2, SPAN, 0.23, FL_T, CAST_IRON, collection=cA)
box("G_top_web",    0, 0, GZ + GD - FL_T - 0.075, SPAN, WEB_T, 0.15, CAST_IRON, collection=cA)
# bottom chord: inverted T — wide flange + web stub above
box("G_bot_flange", 0, 0, GZ + FL_T / 2, SPAN, 0.30, FL_T, CAST_IRON, collection=cA)
box("G_bot_web",    0, 0, GZ + FL_T + 0.075, SPAN, WEB_T, 0.15, CAST_IRON, collection=cA)
z_lo = GZ + FL_T + 0.10         # lattice field
z_hi = GZ + GD - FL_T - 0.10
BAR_W = 0.14
third = SPAN / 3.0
xs = [-HX, -HX + third, HX - third, HX]
# end posts C
for x in (xs[0], xs[-1]):
    box("G_endpost", x, 0, (z_lo + z_hi) / 2, 0.115, 0.05, z_hi - z_lo, CAST_IRON, collection=cA)
# verticals B at third points (cruciform per enlarged sections b.b)
for x in xs[1:-1]:
    cruciform("G_verticalB", x, z_lo, z_hi - z_lo, 0.14, 0.024, CAST_IRON, cA)
# X lattice in each of 3 panels
def inset(p, q, f=0.05):
    return (p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f)
for i in range(3):
    xa, xb = xs[i], xs[i + 1]
    a1, a2 = (xa, z_lo), (xb, z_hi)
    b1, b2 = (xa, z_hi), (xb, z_lo)
    bar_between(f"G_diag_{i}a", inset(a1, a2), inset(a2, a1), BAR_W, WEB_T, CAST_IRON, cA, y=+0.014)
    bar_between(f"G_diag_{i}b", inset(b1, b2), inset(b2, b1), BAR_W, WEB_T, CAST_IRON, cA, y=-0.014)

# =====================================================================
# B. Wrought-iron roof truss bay — PL.11 Fig.I (48 ft truss, one 24 ft bay)
#    z: TZ .. TZ+1.676  (5 ft 6 in plate-measured overall depth)
# =====================================================================
cB = coll("Truss_PL11_FigI")
TZ = GZ + GD + 0.30             # display gap — NOT an as-built connection
TD = 1.676
PANEL = 8 * FT                  # 2.4384 m
txs = [-HX + i * PANEL for i in range(4)]   # standards at 0/8/16/24 ft
CH_Y = 0.048                    # half-distance between paired chord members
# top chord: pair of angle irons 4" x 2" x 1/4" (printed)
for sy in (-1, 1):
    box("T_top_angle_legV", 0, sy * CH_Y, TZ + TD - 0.051, SPAN, 0.0064, 0.102, WROUGHT, collection=cB)
    box("T_top_angle_legH", 0, sy * (CH_Y - 0.0225), TZ + TD - 0.0032, SPAN, 0.051, 0.0064, WROUGHT, collection=cB)
# bottom chord: pair of flat bars 4½" x 1/4" (printed)
for sy in (-1, 1):
    box("T_bot_bar", 0, sy * CH_Y, TZ + 0.057, SPAN, 0.0064, 0.114, WROUGHT, collection=cB)
tz_lo = TZ + 0.114
tz_hi = TZ + TD - 0.102
# end standards: T-section posts (Fig.10)
for x in (txs[0], txs[-1]):
    box("T_endpost_flange", x, 0, (tz_lo + tz_hi) / 2, 0.111, 0.024, tz_hi - tz_lo, ENDPOST, collection=cB)
    box("T_endpost_web", x, 0, (tz_lo + tz_hi) / 2, 0.024, 0.10, tz_hi - tz_lo, ENDPOST, collection=cB)
# intermediate cast-iron standards d: cruciform (Figs.5/8)
for x in txs[1:-1]:
    cruciform("T_standard_d", x, tz_lo, tz_hi - tz_lo, 0.111, 0.024, CAST_IRON, cB)
# X diagonals per 8 ft panel: flat bars 4" x 7/8" (printed sizes; both modelled as iron bars)
for i in range(3):
    xa, xb = txs[i], txs[i + 1]
    bar_between(f"T_diag_{i}a", (xa, tz_lo), (xb, tz_hi), 0.102, 0.022, WROUGHT, cB, y=+0.013)
    bar_between(f"T_diag_{i}b", (xa, tz_hi), (xb, tz_lo), 0.102, 0.022, WROUGHT, cB, y=-0.013)
# joint pins at panel points (1⅛ in dia bolts printed, Fig.I end detail)
for x in txs:
    for z in (TZ + 0.057, TZ + TD - 0.051):
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.0143, depth=0.13,
                                            location=(x, 0, z), rotation=(math.radians(90), 0, 0))
        ob = bpy.context.active_object
        ob.name = "T_pin"
        ob.data.materials.append(WROUGHT)
        for c in ob.users_collection:
            c.objects.unlink(ob)
        cB.objects.link(ob)

# ---------- report + save ----------
bpy.ops.object.select_all(action='SELECT')
tris = 0
for ob in bpy.context.scene.objects:
    if ob.type == 'MESH':
        tris += sum(len(p.vertices) - 2 for p in ob.data.polygons)
print(f"OBJECTS: {len(bpy.context.scene.objects)}  TRIANGLES: {tris}")
for ob in bpy.context.scene.objects:
    ob.select_set(False)

import os
OUT = os.path.expanduser("~/workspace/cp-models/lattice-girder-truss-bay")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "lattice-girder-truss-bay.blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "lattice-girder-truss-bay.glb"),
                          export_format='GLB', export_apply=True)
print("SAVED blend + glb")
