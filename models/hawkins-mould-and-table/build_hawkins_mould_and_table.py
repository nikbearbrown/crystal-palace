#!/usr/bin/env python3
"""
Build script — hawkins-mould-and-table (SCENE-BUILD-PLAN Wave 5, item 22).

The Iguanodon MOULD of B. Waterhouse Hawkins, Sydenham model-room,
winter 1853-54, as dressed for the New Year's Eve dinner of
31 December 1853 (ILN, 7 Jan 1854, p.22) — plus the staging platform
and the dinner table set inside it, kept abstract.

This is the WORKSHOP ARTEFACT (the hollow piece-mould from which the
standing Iguanodon was built up), NOT a finished dinosaur. No people,
no food, no finished creature.

Run:  blender -b --factory-startup -noaudio --python build_hawkins_mould_and_table.py

Units: metres. Origin at base centre of the set. Collections:
  Mould  — body + tail mould sections, iron hoops, joint flange, cradle
  Table  — staging platform, stairs, dinner table, benches, candlesticks
  RenderSetup — ground, lights, cameras (NOT exported to .glb)

Evidence summary (see NOTES.md / refs/REFERENCES.md for the full audit):
  - Animal size (hence mould size): ILN 5 Nov 1853 — the Iguanodon
    "in clay, thirty feet long and eleven feet high" (9.14 m x 3.35 m).
  - The dinner: ILN 7 Jan 1854 p.22 — 21 guests, Owen at the head,
    in the head of the animal; table inside the body mould; staging
    platform + steps around it (the woodcut on the same page).
  - Mould case form: ILN 31 Dec 1853 model-room engraving — plain
    panelled case ~1.9 m to the rim, body rising out of it, timber
    cradle blocks and trestles in the workshop.
  - This prop models the VENTRAL (lower) half mould, open side up:
    rim 1.86-1.94 m, cavity floor 0.60 m. The upper half mould and the
    head mould section are not evidenced as separate workshop objects
    and are not modelled.
"""

import bpy
import math
import os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "hawkins-mould-and-table"

# ----------------------------------------------------------------------------
# clean scene
# ----------------------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

coll_mould = bpy.data.collections.new("Mould")
coll_table = bpy.data.collections.new("Table")
coll_rs = bpy.data.collections.new("RenderSetup")
for c in (coll_mould, coll_table, coll_rs):
    scene.collection.children.link(c)

# ----------------------------------------------------------------------------
# materials (procedural only — no photo textures)
# ----------------------------------------------------------------------------

def make_mat(name, color, rough=0.9, metal=0.0, noise_bump=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if noise_bump > 0:
        nt = m.node_tree.nodes.new("ShaderNodeTexNoise")
        nt.inputs["Scale"].default_value = 14.0
        nt.inputs["Detail"].default_value = 3.0
        nt.inputs["Roughness"].default_value = 0.8
        bump = m.node_tree.nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = noise_bump
        bump.inputs["Distance"].default_value = 0.12
        m.node_tree.links.new(nt.outputs["Fac"], bump.inputs["Height"])
        m.node_tree.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return m

MAT_PLASTER = make_mat("MouldPlasterCompo", (0.66, 0.60, 0.50), 0.95, 0.0, 0.07)
MAT_PLASTER_DARK = make_mat("MouldPlasterShadow", (0.52, 0.47, 0.39), 0.97, 0.0, 0.07)
MAT_IRON = make_mat("IronHooping", (0.16, 0.15, 0.14), 0.55, 0.85)
MAT_TIMBER = make_mat("WorkshopTimber", (0.40, 0.28, 0.16), 0.85, 0.0, 0.12)
MAT_TIMBER_DARK = make_mat("WorkshopTimberDark", (0.30, 0.20, 0.11), 0.9, 0.0, 0.12)
MAT_CLOTH = make_mat("TableCloth", (0.88, 0.85, 0.78), 0.95)
MAT_BRASS = make_mat("Brass", (0.55, 0.38, 0.14), 0.35, 1.0)

# ----------------------------------------------------------------------------
# mesh helpers
# ----------------------------------------------------------------------------

def new_obj(name, coll, verts, faces, mat=None, smooth_edges=None):
    """faces: list of index tuples. smooth_edges: optional set of face
    indices to shade smooth (all others flat)."""
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    if mat:
        me.materials.append(mat)
    if smooth_edges is not None:
        for i, poly in enumerate(me.polygons):
            poly.use_smooth = i in smooth_edges
    return ob


class BoxBatch:
    """Accumulate axis-aligned (or Z-rotated) boxes into one mesh."""

    def __init__(self):
        self.verts = []
        self.faces = []

    def add(self, cx, cy, cz, sx, sy, sz, rotz=0.0, rotx=0.0, roty=0.0):
        hx, hy, hz = sx / 2, sy / 2, sz / 2
        corners = [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
                   (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz)]
        R = (Vector((math.cos(rotz), -math.sin(rotz), 0)),
             Vector((math.sin(rotz), math.cos(rotz), 0)),
             Vector((0, 0, 1)))
        out = []
        for (x, y, z) in corners:
            # apply rotx then roty then rotz (good enough for dressing parts)
            y1 = y * math.cos(rotx) - z * math.sin(rotx)
            z1 = y * math.sin(rotx) + z * math.cos(rotx)
            x2 = x * math.cos(roty) + z1 * math.sin(roty)
            z2 = -x * math.sin(roty) + z1 * math.cos(roty)
            xr = x2 * R[0][0] + y1 * R[0][1]
            yr = x2 * R[1][0] + y1 * R[1][1]
            out.append((cx + xr, cy + yr, cz + z2))
        base = len(self.verts)
        self.verts.extend(out)
        quads = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
                 (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
        for q in quads:
            self.faces.append(tuple(base + i for i in q))

    def build(self, name, coll, mat):
        return new_obj(name, coll, self.verts, self.faces, mat)


def cyl_batch(name, coll, mat, items, seg=10):
    """items: (cx, cy, cz, r, h, axis) axis in {'z','x'} vertical or along X."""
    verts, faces = [], []
    for (cx, cy, cz, r, h, axis) in items:
        base = len(verts)
        for e in (-h / 2, h / 2):
            for i in range(seg):
                a = 2 * math.pi * i / seg
                if axis == 'z':
                    verts.append((cx + r * math.cos(a), cy + r * math.sin(a), cz + e))
                else:
                    verts.append((cx + e, cy + r * math.cos(a), cz + r * math.sin(a)))
        for i in range(seg):
            j = (i + 1) % seg
            faces.append((base + i, base + j, base + seg + j, base + seg + i))
        faces.append(tuple(base + seg + i for i in range(seg)))
        faces.append(tuple(base + (seg - 1 - i) for i in range(seg)))
    return new_obj(name, coll, verts, faces, mat)

# ----------------------------------------------------------------------------
# the mould shell — lofted open trough (ventral half-mould)
# ----------------------------------------------------------------------------

def wall_y(st, z):
    """Half width of the straight outer wall at height z (linear
    between bottom and rim)."""
    x, wb, wr, zb, zr, zcf = st
    if zr == zb:
        return wb
    t = (z - zb) / (zr - zb)
    return wb + (wr - wb) * t


def ring_points(st):
    """Closed cross-section ring (y,z) for one station — the boundary
    of the material cross-section: up the outer wall, out and back
    along the reinforcing flange rib (root points exactly ON the wall
    line, so the loop never self-intersects — v1 crossed itself at
    the flange step and shaded black), over the rim, down the inner
    wall, across the cavity floor, and back. 21 points.
    st = (x, wb, wr, zb, zr, zcf)."""
    x, wb, wr, zb, zr, zcf = st
    wi = wr - 0.14          # inner (cavity) half width
    f = 0.09                # flange rib outreach
    fz1 = zr - 0.16         # flange rib bottom
    fz2 = zr - 0.10         # flange rib top
    return [
        (0.0, zb - 0.04),                    # 0 bottom centre
        (-wb, zb),                           # 1 bottom L
        (-(wb + wr) / 2, (zb + zr) / 2),     # 2 outer wall mid L
        (-wall_y(st, fz1), fz1),             # 3 flange root bottom L
        (-wr - f, fz1),                      # 4 flange tip bottom L
        (-wr - f, fz2),                      # 5 flange tip top L
        (-wall_y(st, fz2), fz2),             # 6 flange root top L
        (-wr, zr),                           # 7 outer rim L
        (-wi, zr),                           # 8 inner rim L
        (-wi, zcf + 0.30),                   # 9 inner wall low L
        (-wi * 0.75, zcf),                   # 10 cavity floor L
        (wi * 0.75, zcf),                    # 11 cavity floor R
        (wi, zcf + 0.30),                    # 12 inner wall low R
        (wi, zr),                            # 13 inner rim R
        (wr, zr),                            # 14 outer rim R
        (wall_y(st, fz2), fz2),              # 15 flange root top R
        (wr + f, fz2),                       # 16 flange tip top R
        (wr + f, fz1),                       # 17 flange tip bottom R
        (wall_y(st, fz1), fz1),              # 18 flange root bottom R
        ((wb + wr) / 2, (zb + zr) / 2),      # 19 outer wall mid R
        (wb, zb),                            # 20 bottom R
    ]

# ring edges shaded flat: underside, flange rib faces, rim faces, floor
FLAT_EDGES = {0, 3, 4, 5, 7, 10, 13, 15, 16, 17, 20}


def loft_section(name, stations, mat):
    rings = [ring_points(st) for st in stations]
    n = len(rings[0])
    verts = []
    for st, ring in zip(stations, rings):
        for (y, z) in ring:
            verts.append((st[0], y, z))
    faces = []
    smooth = set()
    for s in range(len(stations) - 1):
        for e in range(n):
            e2 = (e + 1) % n
            a = s * n + e
            b = s * n + e2
            c = (s + 1) * n + e2
            d = (s + 1) * n + e
            # (a, d, c, b): this winding puts the normals OUT of the
            # material for this ring's traversal direction (v1's
            # (a, b, c, d) pointed every wall normal inward).
            faces.append((a, d, c, b))
            if e not in FLAT_EDGES:
                smooth.add(len(faces) - 1)
    # end caps (flat ngons) — ring winds clockwise seen from +X, so the
    # start cap keeps ring order (normal -X, outward) and the end cap
    # is reversed (normal +X, outward). Getting this wrong renders the
    # cap black from outside (v1 defect, caught in the side render).
    faces.append(tuple(range(n)))
    faces.append(tuple(reversed([(len(stations) - 1) * n + i for i in range(n)])))
    return new_obj(name, coll_mould, verts, faces, mat, smooth)


def outer_path(st, lift=0.0):
    """Outer U path (y,z) of a station, optionally pushed outward."""
    x, wb, wr, zb, zr, zcf = st
    pts = [(-wr, zr), (-(wb + wr) / 2, (zb + zr) / 2), (-wb, zb),
           (0.0, zb - 0.04), (wb, zb),
           ((wb + wr) / 2, (zb + zr) / 2), (wr, zr)]
    if lift:
        cz = (zb + zr) / 2
        out = []
        for (y, z) in pts:
            v = Vector((y, z - cz))
            if v.length > 1e-6:
                v.normalize()
            out.append((y + v.x * lift, z + v.y * lift))
        return out
    return pts


def band(name, st, x0, x1, lift_in, lift_out, mat):
    """Thickened hoop following the outer U path between x0..x1."""
    pin = outer_path(st, lift_in)
    pout = outer_path(st, lift_out)
    verts = []
    for xx in (x0, x1):
        for (y, z) in pin:
            verts.append((xx, y, z))
        for (y, z) in pout:
            verts.append((xx, y, z))
    m = len(pin)
    faces = []
    # outer surface
    for i in range(m - 1):
        faces.append((m + i, m + i + 1, 3 * m + i + 1, 3 * m + i))
        # inner surface
        faces.append((i, 2 * m + i, 2 * m + i + 1, i + 1))
    # end cheeks
    for i in range(m - 1):
        faces.append((i, i + 1, m + i + 1, m + i))
        faces.append((2 * m + i, 3 * m + i, 3 * m + i + 1, 2 * m + i + 1))
    return new_obj(name, coll_mould, verts, faces, mat)


# stations: (x, wb=outer bottom halfW, wr=rim halfW, zb=bottom z,
#            zr=rim z, zcf=cavity floor z)   head/neck at -X, tail at +X
BODY = [
    (-4.35, 0.66, 0.72, 0.45, 1.72, 0.60),
    (-3.65, 0.83, 0.92, 0.45, 1.86, 0.60),
    (-2.45, 0.94, 1.02, 0.45, 1.92, 0.60),
    (-1.05, 0.97, 1.05, 0.45, 1.94, 0.60),
    ( 0.35, 0.95, 1.03, 0.45, 1.92, 0.60),
    ( 1.55, 0.86, 0.94, 0.45, 1.86, 0.60),
]
TAIL = [
    ( 1.55, 0.86, 0.94, 0.45, 1.86, 0.62),
    ( 2.55, 0.72, 0.80, 0.50, 1.74, 0.72),
    ( 3.55, 0.54, 0.60, 0.62, 1.58, 0.86),
    ( 4.35, 0.33, 0.38, 0.80, 1.42, 1.02),
]

loft_section("Mould_BodySection", BODY, MAT_PLASTER)
loft_section("Mould_TailSection", TAIL, MAT_PLASTER)

# neck-end section flange (full ring band at the head end) and tail tip cap band
band("Mould_NeckFlange", BODY[0], -4.44, -4.30, 0.005, 0.05, MAT_PLASTER_DARK)
band("Mould_TailFlange", TAIL[-1], 4.24, 4.36, 0.005, 0.045, MAT_PLASTER_DARK)

# joint flange between body and tail sections (piece-mould joint)
band("Mould_JointFlange", BODY[-1], 1.46, 1.64, 0.005, 0.065, MAT_PLASTER_DARK)
# bolt bosses around the joint flange
_joint_path = outer_path(BODY[-1], 0.085)
bolts = []
for (y, z) in _joint_path:
    bolts.append((1.55, y, z, 0.030, 0.20, 'x'))
cyl_batch("Mould_JointBolts", coll_mould, MAT_IRON, bolts, seg=8)

# iron hoops around the body section
for i, sx in enumerate((-3.3, -1.9, -0.4, 1.0)):
    st = min(BODY, key=lambda s: abs(s[0] - sx))
    band("Mould_IronHoop_%d" % (i + 1), st, sx - 0.045, sx + 0.045,
         0.004, 0.032, MAT_IRON)

# ----------------------------------------------------------------------------
# timber cradle under the mould
# ----------------------------------------------------------------------------
cradle = BoxBatch()
# cross sills on the floor
for sx in (-3.9, -2.3, -0.7, 0.9):
    cradle.add(sx, 0, 0.09, 0.24, 1.80, 0.18)
# longitudinal baulks under the body
for sy in (-0.55, 0.55):
    cradle.add(-1.40, sy, 0.30, 3.60, 0.24, 0.24)
# packing blocks under the shoulders of the case
for sx in (-3.65, -1.05, 0.9):
    cradle.add(sx, 0, 0.36, 0.30, 1.30, 0.12)
# stepped blocks following the rising tail
cradle.add(2.55, 0, 0.22, 0.34, 1.00, 0.44)
cradle.add(3.55, 0, 0.28, 0.34, 0.80, 0.56)
cradle.add(4.20, 0, 0.37, 0.30, 0.55, 0.74)
cradle.build("Mould_Cradle", coll_mould, MAT_TIMBER_DARK)

# spare planks stored under the staging (workshop dressing)
planks = BoxBatch()
planks.add(-0.55, -1.42, 0.85, 2.30, 0.045, 0.28, roty=0.22)
planks.add(-0.30, -1.50, 0.80, 2.10, 0.045, 0.24, roty=0.26)
planks.build("Mould_SparePlanks", coll_mould, MAT_TIMBER)

# ----------------------------------------------------------------------------
# staging platform + stairs (the dinner staging in the woodcut)
# ----------------------------------------------------------------------------
plat = BoxBatch()
# side decks: planks running along X, top at z = 0.95
for side in (-1, 1):
    for i in range(4):
        cy = side * (1.30 + i * 0.215)
        plat.add(-0.80, cy, 0.925, 7.60, 0.195, 0.05)
    # deck edge joists
    plat.add(-0.80, side * 1.20, 0.86, 7.60, 0.10, 0.10)
    plat.add(-0.80, side * 2.00, 0.86, 7.60, 0.10, 0.10)
    # posts
    for px in (-4.45, -2.5, -0.5, 1.5, 2.85):
        plat.add(px, side * 1.97, 0.45, 0.13, 0.13, 0.90)
        plat.add(px, side * 1.24, 0.45, 0.13, 0.13, 0.90)
plat.build("Table_Platform", coll_table, MAT_TIMBER)

# stairs at the head end, descending towards -X (5 steps to the deck)
stairs = BoxBatch()
for i in range(5):
    top = 0.95 - i * 0.19
    stairs.add(-4.83 - i * 0.25, 0, top - 0.025, 0.26, 1.10, 0.05)
    stairs.add(-4.83 - i * 0.25, 0, (top - 0.05) / 2, 0.26, 1.10, top - 0.05)
# stringers (sized to stay above the floor: v2's longer stringers
# dipped 0.09 m under z=0 at their lower corners)
stairs.add(-5.32, -0.52, 0.56, 1.42, 0.05, 0.24, roty=-0.65)
stairs.add(-5.32, 0.52, 0.56, 1.42, 0.05, 0.24, roty=-0.65)
# handrail posts + rails, both sides
for side in (-1, 1):
    for i in range(4):
        px = -4.75 - i * 0.36
        pz = 0.95 - i * 0.19
        stairs.add(px, side * 0.58, pz + 0.40, 0.06, 0.06, 0.85)
    stairs.add(-5.30, side * 0.58, 1.15, 1.70, 0.05, 0.07, roty=-0.50)
    # deck edge rail along the outer side
    for px in (-4.3, -2.4, -0.5, 1.4, 2.8):
        stairs.add(px, side * 2.06, 1.38, 0.06, 0.06, 0.86)
    stairs.add(-0.80, side * 2.06, 1.80, 7.50, 0.055, 0.06)
    stairs.add(-0.80, side * 2.06, 1.42, 7.50, 0.05, 0.05)
stairs.build("Table_StairsRails", coll_table, MAT_TIMBER)

# ----------------------------------------------------------------------------
# the dinner table set inside the mould (ABSTRACT: no food, no settings)
# ----------------------------------------------------------------------------
tt = BoxBatch()
tt.add(-1.10, 0, 1.355, 4.40, 1.02, 0.05)                    # table top
for lx in (-3.15, 0.95):
    for ly in (-0.40, 0.40):
        tt.add(lx, ly, 0.98, 0.10, 0.10, 0.72)               # legs (stand in mould)
tt.build("Table_DinnerTable", coll_table, MAT_TIMBER_DARK)

cloth = BoxBatch()
cloth.add(-1.10, 0, 1.395, 4.52, 1.12, 0.035)
cloth.build("Table_Cloth", coll_table, MAT_CLOTH)

benches = BoxBatch()
for side in (-1, 1):
    benches.add(-1.10, side * 0.685, 1.045, 4.20, 0.30, 0.045)   # seat in mould
    for lx in (-3.0, 0.8):
        benches.add(lx, side * 0.685, 0.83, 0.09, 0.26, 0.40)
    # benches on the side decks (overflow seating, per Owen/Rudwick)
    benches.add(-1.10, side * 1.62, 1.16, 3.60, 0.32, 0.05)
    for lx in (-2.7, 0.5):
        benches.add(lx, side * 1.62, 0.975, 0.10, 0.28, 0.34)
benches.build("Table_Benches", coll_table, MAT_TIMBER)

# candlesticks on the table — plain turned suggestion, no flames
csticks = []
for cx in (-2.9, -1.1, 0.7):
    csticks.append((cx, 0.0, 1.42, 0.055, 0.025, 'z'))
    csticks.append((cx, 0.0, 1.50, 0.013, 0.15, 'z'))
    csticks.append((cx, 0.0, 1.585, 0.024, 0.03, 'z'))
cyl_batch("Table_Candlesticks", coll_table, MAT_BRASS, csticks, seg=10)

# trestle stool beside the platform (workshop dressing, from the model-room image)
stool = BoxBatch()
stool.add(3.30, -1.75, 0.52, 0.60, 0.32, 0.05)
for dx in (-0.22, 0.22):
    stool.add(3.30 + dx, -1.75, 0.26, 0.05, 0.30, 0.50, rotx=0.0, roty=dx * 0.6)
stool.build("Table_TrestleStool", coll_table, MAT_TIMBER)

# ----------------------------------------------------------------------------
# render setup: ground, lights, cameras (RenderSetup — not exported)
# ----------------------------------------------------------------------------
def add_to_rs(ob):
    for c in ob.users_collection:
        c.objects.unlink(ob)
    coll_rs.objects.link(ob)
    return ob

bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, 0))
ground = add_to_rs(bpy.context.active_object)
ground.name = "RS_Ground"
gm = bpy.data.materials.new("GroundGrey")
gm.use_nodes = True
gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.42, 0.42, 0.42, 1)
gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
ground.data.materials.append(gm)

world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.5, 0.5, 0.5, 1)
bg.inputs[1].default_value = 1.15

bpy.ops.object.light_add(type='SUN', location=(6, -7, 10))
sun = add_to_rs(bpy.context.active_object)
sun.name = "RS_Sun"
sun.data.energy = 3.2
sun.data.angle = 0.35
sun.rotation_euler = (math.radians(52), math.radians(8), math.radians(38))

bpy.ops.object.light_add(type='AREA', location=(-7, -6, 7))
fill = add_to_rs(bpy.context.active_object)
fill.name = "RS_Fill"
fill.data.energy = 450
fill.data.size = 9
# aim the fill at the set (front-left, so the head end is not starved)
_d = Vector((0, 0, 1)) - fill.location
fill.rotation_euler = _d.to_track_quat('-Z', 'Y').to_euler()


def look_at(ob, target):
    d = Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def make_cam(name, loc, target, lens=40):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    ob = bpy.data.objects.new(name, cd)
    coll_rs.objects.link(ob)
    ob.location = loc
    look_at(ob, target)
    return ob

CAM_FRONT = make_cam("Cam_Front", (0.2, -14.5, 2.6), (-0.2, 0, 1.0), 40)
CAM_SIDE = make_cam("Cam_Side", (-13.5, 0.4, 2.0), (-0.2, 0, 1.0), 40)
CAM_TQ = make_cam("Cam_ThreeQuarter", (-9.5, -10.5, 5.2), (-0.2, 0, 0.9), 40)
CAM_INT = make_cam("Cam_Interior", (-4.6, -3.4, 3.6), (0.4, 0.1, 0.9), 34)

# ----------------------------------------------------------------------------
# render settings + renders
# ----------------------------------------------------------------------------
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.use_denoising = True
scene.cycles.device = 'CPU'
scene.render.resolution_x = 960
scene.render.resolution_y = 720
if os.environ.get("HAWK_TEST"):
    scene.cycles.samples = 8
    scene.render.resolution_x = 480
    scene.render.resolution_y = 360
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Medium Contrast'

os.makedirs(os.path.join(HERE, "renders"), exist_ok=True)
for cam, fname in ((CAM_FRONT, "front.png"), (CAM_SIDE, "side.png"),
                   (CAM_TQ, "three-quarter.png"), (CAM_INT, "mould-interior.png")):
    scene.camera = cam
    scene.render.filepath = os.path.join(HERE, "renders", fname)
    bpy.ops.render.render(write_still=True)
    print("RENDERED", fname)

# ----------------------------------------------------------------------------
# stats, GLB export (Mould + Table only), save .blend
# ----------------------------------------------------------------------------
tris = 0
model_objs = []
for coll in (coll_mould, coll_table):
    for ob in coll.objects:
        model_objs.append(ob)
        if ob.type == 'MESH':
            me = ob.data
            tris += sum(len(p.vertices) - 2 for p in me.polygons)
print("MODEL OBJECTS:", len(model_objs))
print("TRIANGLES:", tris)

bpy.ops.object.select_all(action='DESELECT')
for ob in model_objs:
    ob.select_set(True)
bpy.context.view_layer.objects.active = model_objs[0]
bpy.ops.export_scene.gltf(
    filepath=os.path.join(HERE, SLUG + ".glb"),
    use_selection=True, export_apply=True, export_yup=True)
print("GLB EXPORTED")

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, SLUG + ".blend"))
print("BLEND SAVED")
print("DONE")
