#!/usr/bin/env python3
"""Build the Crystal Palace cast-iron column, COMPLETE (candidate #18).

Source: Downes (1852), Plate VIII "Details of columns" (Figs. 1-13) and
Plate XIV Figs. 9-13 (ornamental bands on columns); cross-section diagram
The_Crystal_Palace_page_52b.jpg; dimension controls in
references/downes-1852/crystal-palace-1851/CONTROL-DIMENSIONS.md
(D10-D18), themselves read off the printed pages of Downes's text.

The model is the full three-storey outer column of Plate VIII Figs. 6-8:
foundation piece B, lower column A, connecting piece C, tier-2 column E,
connecting piece F, tier-3 column G, top connecting piece H. Short
truncated girder stubs sit in the bearings of C, F and H (H one side
only, per Fig. 6). Ornamental octagonal bands (Plate XIV) dress the two
gallery joints.

Real-world metres. Origin at the centre of the column at GROUND-FLOOR
level (z = 0); the foundation foot B extends 0.610 m below the origin.
Total height above floor 62 ft 4 1/4 in = 19.006 m (printed, D18).

PRINTED dimensions used (see NOTES.md for the full table):
  - external diameter 8 in in every case (printed text p.17; Plate VIII
    Fig. 13 prints 8" across the flats of the section)
  - wall 9/16 in on the shaft sections (plans at o.o / m.m / l.l),
    11/16 in on the connecting-piece drum (Fig. 13)
  - stack: B top 3 3/4 in above floor; A 18 ft 8 in; C 3 ft 4 1/2 in;
    E 16 ft 7 1/2 in; F 3 ft 4 1/2 in; G 16 ft 7 1/2 in; H 3 ft 4 1/2 in
  - girder depth 3 ft 0 in, seated in the connecting pieces with 2 1/4 in
    of the piece below and above it
  - base plate (foot plan) 3 ft 0 in x 1 ft 6 in (Figs. 6-8, D16)
  - bolt holes 1 1/4 in dia; bolt spacing 10 in (lower joints, Fig. 6 /
    Fig. 13) and 9 3/4 in (upper joints, Fig. 6)
"""
import bpy
import math
import os
from mathutils import Vector

OUT = os.path.expanduser("~/workspace/cp-models/cast-iron-column")
RENDERS = os.path.join(OUT, "renders")
os.makedirs(RENDERS, exist_ok=True)

IN = 0.0254

# ------------------------------------------------------------------ stack
B_BELOW = 0.610                    # foundation depth below floor (inferred)
B_TOP = 3.75 * IN                  # 0.0953  B top above floor (printed)
A_LEN = (18 * 12 + 8) * IN         # 5.6896
C_LEN = (3 * 12 + 4.5) * IN        # 1.0287
E_LEN = (16 * 12 + 7.5) * IN       # 5.0673
G_LEN = E_LEN
GIRDER = 3 * 12 * IN               # 0.9144
PROUD = 2.25 * IN                  # 0.0572 piece above/below girder

Z = {}
z = B_TOP
Z['A0'] = z;  z += A_LEN;  Z['A1'] = z          # 5.7849  18'11.75"
Z['C0'] = z;  z += C_LEN;  Z['C1'] = z          # 6.8136  22'4.25"
Z['E0'] = z;  z += E_LEN;  Z['E1'] = z          # 11.8809 38'11.75"
Z['F0'] = z;  z += C_LEN;  Z['F1'] = z          # 12.9096 42'4.25"
Z['G0'] = z;  z += G_LEN;  Z['G1'] = z          # 17.9769 58'11.75"
Z['H0'] = z;  z += C_LEN;  Z['H1'] = z          # 19.0056 62'4.25"
TOTAL = Z['H1']

R_OUT = 4 * IN                     # 0.1016  (8 in external, printed)
WALL_S = 9 / 16 * IN               # shaft wall
R_IN_S = R_OUT - WALL_S            # bore dia 6 7/8 in
R_DRUM = 0.127                     # connecting-piece drum (plate-measured est.)
WALL_C = 11 / 16 * IN
R_IN_C = R_DRUM - WALL_C
BOLT_R_LO = (10 * IN / 2) * math.sqrt(2) / 1.41421356  # holes 10 in apart on a side
BOLT_CIRC_LO = 10 * IN / math.sqrt(2)   # centre radius of the 4 diagonal holes
BOLT_CIRC_HI = 9.75 * IN / math.sqrt(2)
BOLT_R = 0.625 * IN                # 1 1/4 in dia holes -> bolt shank radius

# ------------------------------------------------------------------ scene
bpy.ops.wm.read_factory_settings(use_empty=True)
model_coll = bpy.data.collections.new("Model")
bpy.context.scene.collection.children.link(model_coll)
rig_coll = bpy.data.collections.new("RenderSetup")
bpy.context.scene.collection.children.link(rig_coll)

mat_iron = bpy.data.materials.new("PaintedIron")
mat_iron.use_nodes = True
mat_iron.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.50, 0.48, 0.45, 1)
mat_iron.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.62
mat_iron.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.15

mat_dark = bpy.data.materials.new("BoreDark")
mat_dark.use_nodes = True
mat_dark.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.13, 0.12, 0.11, 1)
mat_dark.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9


def link_model(obj):
    model_coll.objects.link(obj)
    return obj


def mesh_obj(name, verts, faces, mat=mat_iron):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    if mat:
        me.materials.append(mat)
    return link_model(ob)


def tube(name, z0, z1, r_out, r_in, seg=28):
    """Hollow tube, open ends show the bore (annulus caps top and bottom)."""
    verts, faces = [], []
    for z in (z0, z1):
        for r in (r_out, r_in):
            for i in range(seg):
                a = 2 * math.pi * i / seg
                verts.append((r * math.cos(a), r * math.sin(a), z))
    # ring index: ring0 outer bottom = 0, ring1 inner bottom = seg,
    # ring2 outer top = 2seg, ring3 inner top = 3seg
    for i in range(seg):
        j = (i + 1) % seg
        faces.append((i, j, 2 * seg + j, 2 * seg + i))                    # outer
        faces.append((seg + j, seg + i, 3 * seg + i, 3 * seg + j))        # inner
        faces.append((2 * seg + i, 2 * seg + j, 3 * seg + j, 3 * seg + i))  # top annulus
        faces.append((j, i, seg + i, seg + j))                            # bottom annulus
    return mesh_obj(name, verts, faces)


def solid_cyl(name, z0, z1, r, seg=28):
    verts, faces = [], []
    for z in (z0, z1):
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append((r * math.cos(a), r * math.sin(a), z))
    verts.append((0, 0, z0)); verts.append((0, 0, z1))
    cb, ct = 2 * seg, 2 * seg + 1
    for i in range(seg):
        j = (i + 1) % seg
        faces.append((i, j, seg + j, seg + i))
        faces.append((j, i, cb))
        faces.append((seg + i, seg + j, ct))
    return mesh_obj(name, verts, faces)


def ngon_plate(name, z0, z1, r, n=8, rot=math.pi / 8):
    return solid_cyl_ngon(name, z0, z1, r, n, rot)


def solid_cyl_ngon(name, z0, z1, r, n, rot=0.0):
    verts, faces = [], []
    for z in (z0, z1):
        for i in range(n):
            a = rot + 2 * math.pi * i / n
            verts.append((r * math.cos(a), r * math.sin(a), z))
    verts.append((0, 0, z0)); verts.append((0, 0, z1))
    cb, ct = 2 * n, 2 * n + 1
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        faces.append((j, i, cb))
        faces.append((n + i, n + j, ct))
    return mesh_obj(name, verts, faces)


def box(name, cx, cy, cz, sx, sy, sz):
    bpy.ops.mesh.primitive_cube_add(location=(cx, cy, cz))
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    ob.data.materials.append(mat_iron)
    bpy.context.scene.collection.objects.unlink(ob)
    return link_model(ob)


def hex_nut(name, cx, cy, cz, r=0.028, h=0.026):
    return solid_cyl_ngon(name, cz - h / 2, cz + h / 2, r, 6)


def frustum_box(name, z0, z1, sx0, sy0, sx1, sy1):
    v = [(-sx0 / 2, -sy0 / 2, z0), (sx0 / 2, -sy0 / 2, z0),
         (sx0 / 2, sy0 / 2, z0), (-sx0 / 2, sy0 / 2, z0),
         (-sx1 / 2, -sy1 / 2, z1), (sx1 / 2, -sy1 / 2, z1),
         (sx1 / 2, sy1 / 2, z1), (-sx1 / 2, sy1 / 2, z1)]
    f = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2),
         (2, 6, 7, 3), (3, 7, 4, 0)]
    return mesh_obj(name, v, f)


def revolve8(name, profile, z_base):
    """profile: list of (r, z_rel) outer then inner return; 8-sided revolve."""
    n = 8
    verts, faces = [], []
    for (r, zr) in profile:
        for i in range(n):
            a = math.pi / 8 + 2 * math.pi * i / n
            verts.append((r * math.cos(a), r * math.sin(a), z_base + zr))
    rings = len(profile)
    for k in range(rings - 1):
        for i in range(n):
            j = (i + 1) % n
            faces.append((k * n + i, k * n + j, (k + 1) * n + j, (k + 1) * n + i))
    # cap the loop ends to the axis-side: close bottom and top with fans to
    # the first/last ring centres is wrong for a collar; instead the profile
    # is a closed loop (last point returns near first radius at base), so add
    # the closing ring faces:
    k = rings - 1
    for i in range(n):
        j = (i + 1) % n
        faces.append((k * n + i, k * n + j, j, i))
    return mesh_obj(name, verts, faces)


def girder_stub(prefix, side, z_bot, z_top):
    """Truncated girder in the connecting-piece bearing, along +/-X.
    Flanges horizontal; web a tapered plate (simplification - the plate's
    triangular lightening is not cut). Cut at |x| = 0.85 m."""
    s = 1 if side > 0 else -1
    x0, x1 = 0.18, 0.85
    ft = 0.032
    box(f"{prefix}_GirderFlangeTop{'P' if s>0 else 'M'}",
        s * (x0 + x1) / 2, 0, z_top - ft / 2, x1 - x0, 0.22, ft)
    box(f"{prefix}_GirderFlangeBot{'P' if s>0 else 'M'}",
        s * (x0 + x1) / 2, 0, z_bot + ft / 2, x1 - x0, 0.22, ft)
    # tapered web prism
    zb0, zt0 = z_bot + ft, z_top - ft
    mid = (zb0 + zt0) / 2
    half1 = 0.26
    t = 0.026
    v = [(s * x0, -t / 2, zb0), (s * x0, t / 2, zb0), (s * x0, t / 2, zt0),
         (s * x0, -t / 2, zt0),
         (s * x1, -t / 2, mid - half1), (s * x1, t / 2, mid - half1),
         (s * x1, t / 2, mid + half1), (s * x1, -t / 2, mid + half1)]
    if s < 0:
        v = [(x, y, z) for (x, y, z) in v]
    f = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2),
         (2, 6, 7, 3), (3, 7, 4, 0)]
    if s < 0:
        f = [tuple(reversed(x)) for x in f]
    mesh_obj(f"{prefix}_GirderWeb{'P' if s>0 else 'M'}", v, f)
    box(f"{prefix}_GirderCut{'P' if s>0 else 'M'}",
        s * x1, 0, mid, 0.018, 0.22, half1 * 2 + ft)


def shaft(name, z0, z1, bolt_circ):
    """One column length with end flanges, 4 longitudinal ribs, bolts."""
    ft = 0.040
    ngon_plate(name + "_FlangeBot", z0, z0 + ft, 0.210)
    ngon_plate(name + "_FlangeTop", z1 - ft, z1, 0.210)
    tube(name + "_Shaft", z0 + ft, z1 - ft, R_OUT, R_IN_S)
    # four longitudinal ribs (page_52b section: ribs at cardinal points)
    for k, ang in enumerate((0, 90, 180, 270)):
        a = math.radians(ang)
        cx, cy = (R_OUT - 0.002) * math.cos(a), (R_OUT - 0.002) * math.sin(a)
        rib = box(f"{name}_Rib{k}", cx, cy, (z0 + z1) / 2,
                  0.070 if k % 2 == 0 else 0.014,
                  0.014 if k % 2 == 0 else 0.070,
                  z1 - z0 - 2 * ft)
    # bolt nuts at the top flange (diagonal holes, Fig. 13)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        hex_nut(f"{name}_Nut{k}",
                bolt_circ * math.cos(a), bolt_circ * math.sin(a), z1 - ft - 0.016)


def connecting(name, z0, top=False):
    """Connecting piece C/F/H: bottom plate P, drum, top plate P, lugs,
    girder bearings. Returns (girder_bottom_z, girder_top_z)."""
    pt = PROUD  # plate thickness = the 2 1/4 in the piece stands proud
    ngon_plate(name + "_PlateBot", z0, z0 + pt, 0.240)
    if top:
        # H: top is an open octagonal ring plate (Plan of Top, Fig. 6)
        tube(name + "_PlateTop", z0 + C_LEN - pt, z0 + C_LEN, 0.240, 0.115, seg=8)
    else:
        ngon_plate(name + "_PlateTop", z0 + C_LEN - pt, z0 + C_LEN, 0.240)
    tube(name + "_Drum", z0 + pt, z0 + C_LEN - pt, R_DRUM, R_IN_C)
    # girder-bearing lugs P on +/-X at both plate levels (Fig. 13 plan)
    for lvl, zz in (("Bot", z0 + pt / 2), ("Top", z0 + C_LEN - pt / 2)):
        for s, tag in ((1, "P"), (-1, "M")):
            box(f"{name}_Lug{lvl}{tag}", s * 0.285, 0, zz, 0.10, 0.17, 0.052)
    return z0 + pt, z0 + C_LEN - pt


# ------------------------------------------------------------------ build
# Foundation piece B (below floor, flared foot 3'0" x 1'6" printed)
box("B_BasePlate", 0, 0, -B_BELOW + 0.025, 3 * 12 * IN, 1.5 * 12 * IN, 0.05)
frustum_box("B_Flare", -B_BELOW + 0.05, 0.02, 0.86, 0.42, 0.30, 0.24)
solid_cyl("B_Neck", -0.20, B_TOP, 0.120)
ngon_plate("B_TopFlange", B_TOP - 0.040, B_TOP, 0.175)

# Lower column A + connecting piece C (+ stubs, band)
shaft("A", Z['A0'], Z['A1'], BOLT_CIRC_LO)
gb, gt = connecting("C", Z['C0'])
girder_stub("C", +1, gb, gt)
girder_stub("C", -1, gb, gt)

# Tier-2 column E + connecting piece F (+ stubs, band)
shaft("E", Z['E0'], Z['E1'], BOLT_CIRC_HI)
gb, gt = connecting("F", Z['F0'])
girder_stub("F", +1, gb, gt)
girder_stub("F", -1, gb, gt)

# Tier-3 column G + top connecting piece H (+ one stub, Fig. 6)
shaft("G", Z['G0'], Z['G1'], BOLT_CIRC_HI)
gb, gt = connecting("H", Z['H0'], top=True)
girder_stub("H", +1, gb, gt)
# small top lugs on +/-Y (Plan of Top, Fig. 6)
for s, tag in ((1, "P"), (-1, "M")):
    box(f"H_TopLug{tag}", 0, s * 0.265, Z['H1'] - PROUD / 2, 0.09, 0.06, 0.05)

# bracing strap on the front (+Y) face of G near its top (Fig. 6)
box("G_Strap", 0, R_OUT + 0.008, Z['G1'] - 0.55, 0.105, 0.018, 0.34)
hex_nut("G_StrapNut", 0, R_OUT + 0.022, Z['G1'] - 0.55, r=0.026, h=0.024)

# Ornamental bands (Plate XIV Figs. 9-13): octagonal ogee collars at the
# two gallery floors. Gallery floor = girder top + 9 in (D11/D12: gallery
# floor 22'11" vs girder top 22'2").
band_profile = [(0.235, 0.00), (0.252, 0.06), (0.266, 0.20), (0.252, 0.34),
                (0.216, 0.44), (0.206, 0.50),
                (0.181, 0.50), (0.191, 0.44), (0.227, 0.34), (0.241, 0.20),
                (0.227, 0.06), (0.210, 0.00)]
GAL1 = Z['C1'] - PROUD + 9 * IN   # 22 ft 11 in = 6.985 m
GAL2 = Z['F1'] - PROUD + 9 * IN   # 42 ft 11 in
revolve8("Band_Tier1", band_profile, GAL1)
revolve8("Band_Tier2", band_profile, GAL2)
for nm, zb in (("Band_Tier1", GAL1), ("Band_Tier2", GAL2)):
    for k in range(4):
        a = math.radians(45 + 90 * k)
        box(f"{nm}_Spacer{k}", 0.150 * math.cos(a), 0.150 * math.sin(a),
            zb + 0.03, 0.07, 0.07, 0.06)

# ------------------------------------------------------------------ counts
dg = bpy.context.evaluated_depsgraph_get()
tris = 0
objs = 0
for ob in model_coll.objects:
    if ob.type == 'MESH':
        objs += 1
        ev = ob.evaluated_get(dg)
        tris += sum(len(p.vertices) - 2 for p in ev.data.polygons)
print(f"MODEL objects={objs} triangles={tris} total_height={TOTAL + B_BELOW:.3f} m "
      f"above_floor={TOTAL:.4f} m")

# ------------------------------------------------------------------ save
blend_path = os.path.join(OUT, "cast-iron-column.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

# GLB: Model collection only
for ob in rig_coll.objects:
    ob.hide_viewport = True
    ob.hide_render = True
bpy.ops.object.select_all(action='DESELECT')
for ob in model_coll.objects:
    ob.select_set(True)
bpy.context.view_layer.objects.active = model_coll.objects[0]
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "cast-iron-column.glb"),
                          export_format='GLB', use_visible=True,
                          export_apply=True)
print("saved", blend_path)
