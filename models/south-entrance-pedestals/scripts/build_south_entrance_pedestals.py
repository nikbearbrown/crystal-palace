#!/usr/bin/env python3
"""
South-entrance pedestals (candidate #26) — Crystal Palace, Hyde Park 1851.

Source: Downes (1852), Plate XXVI — "Details of ditto, and pedestals at
south entrance" (references/downes-1852/source-scans/plates/plate-026.jpg),
described in Downes' text pp. 38-39:

  Fig. 26  elevation of the pedestal of one of the DETACHED columns at the
           entrance at the south end of the Transept.
  Fig. 27  sectional plan of the same at line z.z.  a3 = cast-iron column;
           a5 = pedestal of cast iron, made in two pieces, united by
           countersunk screws.
  Figs. 28-29  parts of a side elevation of the pedestal (B3) of one of the
           semi-elliptical WOODEN columns B.
  Fig. 30  sectional plan of the same.  A = cast-iron column, A5 its
           pedestal; B = semi-elliptical wooden column, B3 its pedestal.

Calibration (pixel metrology on the scan, see NOTES.md):
  Figs. 26/27: printed dimension 4'9" spans the pedestal from its top line
  (y=329) to floor (y=3153) = 2824 px  ->  49.54 px/in.
  Figs. 28-30: printed 3-3/4" = 157 px and 4-1/4" = 184 px -> ~42.5 px/in.

Pedestal A total height is therefore exactly 4 ft 9 in = 1.4478 m.
Pedestal B adopts the same overall height (shared floor datum and cap
levels on the plate; its undrawn shaft middle is reconstructed).

Blender 4.2, procedural bpy, real-world metres, origin at base centre
(of pedestal A; B stands offset at (+1.05, +0.62) m for comparison,
staggered so both pedestals read in front and side views, as documented).
"""
import bpy
import math
import os
from mathutils import Vector

IN = 0.0254
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(OUT_DIR)

# ----------------------------------------------------------------------------
# scene reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ----------------------------------------------------------------------------
# materials
def make_mat(name, color, metallic=0.0, rough=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    return m

IRON = make_mat("PaintedCastIron", (0.335, 0.32, 0.295), 0.15, 0.52)
DARK = make_mat("DarkIron", (0.07, 0.07, 0.075), 0.4, 0.6)
TIMBER = make_mat("TimberColumn", (0.235, 0.125, 0.055), 0.0, 0.78)
GREY = make_mat("BackdropGrey", (0.5, 0.5, 0.5), 0.0, 1.0)
MATS = [IRON, DARK, TIMBER, GREY]


def assign(obj, mat):
    obj.data.materials.append(mat)


# ----------------------------------------------------------------------------
# generic loft: rings = list of (z, [ (x,y), ... ]) all rings same point count
def loft(name, rings, mat, collection):
    verts = []
    for z, pts in rings:
        for (x, y) in pts:
            verts.append((x, y, z))
    n = len(rings[0][1])
    faces = []
    for i in range(len(rings) - 1):
        for j in range(n):
            a = i * n + j
            b = i * n + (j + 1) % n
            c = (i + 1) * n + (j + 1) % n
            d = (i + 1) * n + j
            faces.append((a, b, c, d))
    # bottom fan (centre vertex at first ring z) and top fan
    z0 = rings[0][0]
    z1 = rings[-1][0]
    cb = len(verts); verts.append((0.0, 0.0, z0))
    ct = len(verts); verts.append((0.0, 0.0, z1))
    for j in range(n):
        faces.append((cb, (j + 1) % n, j))
        faces.append((ct, (len(rings) - 1) * n + j, (len(rings) - 1) * n + (j + 1) % n))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    assign(ob, mat)
    return ob


def oct_ring(apothem):
    """Regular octagon ring points, flats normal to +-X / +-Y (front flat -Y)."""
    R = apothem / math.cos(math.radians(22.5))
    return [(R * math.cos(math.radians(22.5 + 45 * k)),
             R * math.sin(math.radians(22.5 + 45 * k))) for k in range(8)]


def rect_ring(hx, hy):
    return [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]


def box(name, loc, dims, mat, collection, rotz=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc,
                                    rotation=(0, 0, rotz))
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    # move from default collection into ours
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    collection.objects.link(ob)
    assign(ob, mat)
    return ob


def collection(name):
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    return c


colA = collection("Pedestal_A_A5_octagonal")
colB = collection("Pedestal_B_B3_rectangular")
BX = 1.05  # pedestal B centre offset in X (documented in NOTES.md)
BY = 0.62   # ... and staggered +Y so both read in the side view

# ----------------------------------------------------------------------------
# PEDESTAL A — octagonal cast-iron pedestal (a5), Figs. 26-27.
# Profile: (z_in, apothem_in).  Heights from code-measured plate lines at
# 49.54 px/in; the printed 4'9" runs floor (y3153) -> pedestal top (y329).
A_prof = [
    (0.00, 10.10),   # plinth bottom
    (5.41, 10.10),   # plinth top
    (5.41, 7.00),    # ledge in to base-flare foot
    (6.56, 6.99),    # base flare (cyma trumpet), sampled
    (7.71, 6.95),
    (8.86, 6.84),
    (10.01, 6.60),
    (10.86, 6.25),
    (11.41, 5.945),  # flare top = shaft
    (52.32, 5.945),  # shaft top
    (52.90, 6.30),   # torus (cushion moulding), sampled
    (53.60, 6.72),
    (54.30, 6.98),
    (55.00, 7.05),   # torus max
    (55.70, 6.94),
    (56.24, 6.75),   # torus top
    (57.00, 6.75),   # band top = PEDESTAL TOP (4'9")
    (57.45, 6.72),   # bell (column socket flare), sampled
    (58.20, 6.50),
    (59.10, 6.24),
    (60.00, 6.05),
    (60.75, 5.945),  # bell top
]
ringsA = [(z * IN, oct_ring(r * IN)) for (z, r) in A_prof]
pedA = loft("PedestalA", ringsA, IRON, colA)

# column stub a3 (round cast-iron column, OD 9.3 in from Fig. 27 plan),
# rising from the bell; stub height 9 in is ADOPTED (plate is cut at top).
stub_prof = [(60.75, 5.10), (61.20, 5.10), (61.20, 4.65), (69.75, 4.65)]
rings_stub = []
for (z, r) in stub_prof:
    rings_stub.append((z * IN, [(r * IN * math.cos(2 * math.pi * k / 32),
                                 r * IN * math.sin(2 * math.pi * k / 32))
                                for k in range(32)]))
stubA = loft("ColumnA3_stub", rings_stub, IRON, colA)

# countersunk screws on the front (-Y) facet, as drawn in Fig. 26:
# (z_in, apothem_in at that height) — bell 1, torus 1, shaft 3, plinth 1.
screws = [(59.80, 6.10), (54.30, 6.98), (45.70, 5.945),
          (31.80, 5.945), (18.40, 5.945), (3.10, 10.10)]
for i, (z, ap) in enumerate(screws):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16, radius=0.55 * IN, depth=0.10 * IN,
        location=(0, -(ap + 0.02) * IN, z * IN),
        rotation=(math.radians(90), 0, 0))
    ob = bpy.context.active_object
    ob.name = f"ScrewHead_{i}"
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    colA.objects.link(ob)
    assign(ob, DARK)
    slot = box(f"ScrewSlot_{i}", (0, -(ap + 0.075) * IN, z * IN),
               (0.80 * IN, 0.02 * IN, 0.15 * IN), DARK, colA,
               rotz=math.radians(35))

# ----------------------------------------------------------------------------
# PEDESTAL B — rectangular pedestal (B3) of the semi-elliptical wooden
# column B, Figs. 28-30.  Plan from Fig. 30 at ~42.5 px/in: 23.0 in wide
# (along wall) x 21.3 in deep.  Plinth 6.4 in from Fig. 29.  Overall height
# adopted equal to A (4'9"); cap profile follows A (Figs. 28-29 share A's
# levels).  Built in local coords, then offset +X.
B_prof = [  # (z_in, hx_in, hy_in)
    (0.00, 11.50, 10.65),   # plinth
    (6.40, 11.50, 10.65),   # plinth top
    (6.40, 10.60, 9.60),    # ledge in to flare foot
    (7.80, 10.59, 9.59),    # base flare, sampled
    (9.20, 10.54, 9.54),
    (10.60, 10.40, 9.40),
    (11.90, 10.25, 9.25),   # flare top = shaft
    (52.32, 10.25, 9.25),   # shaft top
    (52.90, 10.60, 9.60),   # torus, sampled (A profile + plan offset)
    (53.60, 11.02, 10.02),
    (54.30, 11.28, 10.28),
    (55.00, 11.35, 10.35),
    (55.70, 11.24, 10.24),
    (56.24, 11.05, 10.05),  # torus top
    (57.00, 11.05, 10.05),  # band top = pedestal top (adopted 4'9")
    (57.45, 11.02, 10.02),  # bell, sampled
    (58.20, 10.80, 9.80),
    (59.10, 10.54, 9.54),
    (60.00, 10.35, 9.35),
    (60.75, 10.25, 9.25),   # bell top
]
ringsB = [(z * IN, rect_ring(hx * IN, hy * IN)) for (z, hx, hy) in B_prof]
pedB = loft("PedestalB", ringsB, IRON, colB)
pedB.location = (BX, BY, 0)

# recessed front panel on B's shaft (framed panel read from Fig. 30's
# section; projection shallow — see NOTES). Front = -Y face.
panel_cz = 32.0 * IN
frame_w, frame_h, rail = 15.0 * IN, 30.0 * IN, 1.6 * IN
fy = BY - (9.25 + 0.10) * IN
for nm, loc, dims in [
    ("PanelStile_L", (BX - frame_w / 2 + rail / 2, fy, panel_cz), (rail, 0.20 * IN, frame_h)),
    ("PanelStile_R", (BX + frame_w / 2 - rail / 2, fy, panel_cz), (rail, 0.20 * IN, frame_h)),
    ("PanelRail_T", (BX, fy, panel_cz + frame_h / 2 - rail / 2), (frame_w - 2 * rail, 0.20 * IN, rail)),
    ("PanelRail_B", (BX, fy, panel_cz - frame_h / 2 + rail / 2), (frame_w - 2 * rail, 0.20 * IN, rail)),
    ("PanelField", (BX, BY - (9.25 + 0.03) * IN, panel_cz),
     (frame_w - 2 * rail, 0.06 * IN, frame_h - 2 * rail)),
]:
    box(nm, loc, dims, IRON, colB)

# semi-elliptical wooden column stub B: flat back on the +Y (wall) side,
# half-ellipse bulging to -Y.  Width 19.5 in, projection 13.5 in from the
# shaft back face (Fig. 30).  Stub height 12 in ADOPTED.
ell_pts = []
SEG = 24
cx_e, cy_e = 0.0, 9.25  # centre of ellipse (local, inches), back line y=+9.25
for k in range(SEG + 1):
    phi = math.pi + math.pi * k / SEG  # 180..360 deg: bulge to -Y
    ell_pts.append(((cx_e + 9.75 * math.cos(phi)) * IN,
                    (cy_e + 13.5 * math.sin(phi)) * IN))
ringsE = [(60.75 * IN, ell_pts), (72.75 * IN, ell_pts)]
stubB = loft("WoodColumnB_stub", ringsE, TIMBER, colB)
stubB.location = (BX, BY, 0)

# ----------------------------------------------------------------------------
# backdrop + lights + cameras (fixed neutral-grey rig)
bpy.ops.mesh.primitive_plane_add(size=40, location=(0.5, 0.3, -0.001))
bd = bpy.context.active_object
bd.name = "Backdrop"
assign(bd, GREY)

def light(name, loc, energy, size=4.0):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.energy = energy
    ld.shape = 'DISK'
    ld.size = size
    o = bpy.data.objects.new(name, ld)
    o.location = loc
    scene.collection.objects.link(o)
    d = Vector((0.5, 0.25, 0.85)) - o.location
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return o

light("Key", (-3.5, -4.5, 5.0), 900)
light("Fill", (5.0, -1.5, 2.5), 350)
light("Rim", (0.5, 5.0, 5.5), 500, 3.0)

scene.world = bpy.data.worlds.new("W")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.32, 0.32, 0.32, 1)
scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.6

TARGET = (0.5, 0.25, 0.82)

def shot(name, loc, lens=55):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    o = bpy.data.objects.new(name, cd)
    o.location = loc
    scene.collection.objects.link(o)
    d = Vector(TARGET) - o.location
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return o

CAMS = {
    "front": shot("CamFront", (0.5, -4.9, 0.95)),
    "side": shot("CamSide", (5.4, -0.3, 0.95)),
    "three-quarter": shot("CamTQ", (3.7, -3.7, 2.1)),
}

# ----------------------------------------------------------------------------
# stats
def tri_count():
    total = 0
    for ob in scene.objects:
        if ob.type == 'MESH' and ob.name != 'Backdrop':
            me = ob.data
            me.calc_loop_triangles()
            total += len(me.loop_triangles)
    return total

TRIS = tri_count()
print(f"TRIANGLES: {TRIS}")
for ob in scene.objects:
    if ob.type == 'MESH' and ob.name != 'Backdrop':
        bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
        xs = [v.x for v in bb]; ys = [v.y for v in bb]; zs = [v.z for v in bb]
        print(f"  {ob.name}: X {min(xs):.3f}..{max(xs):.3f}  Y {min(ys):.3f}..{max(ys):.3f}  Z {min(zs):.3f}..{max(zs):.3f}")

# save .blend
blend_path = os.path.join(ROOT, "south-entrance-pedestals.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("saved", blend_path)

# export .glb (model objects only)
bpy.ops.object.select_all(action='DESELECT')
for ob in scene.objects:
    if ob.type == 'MESH' and ob.name != 'Backdrop':
        ob.select_set(True)
glb_path = os.path.join(ROOT, "south-entrance-pedestals.glb")
bpy.ops.export_scene.gltf(filepath=glb_path, use_selection=True,
                          export_apply=True)
print("exported", glb_path)

print("BUILD+EXPORT DONE")
