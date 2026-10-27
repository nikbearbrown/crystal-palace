# Build script — sy36-ruin-fragment-bay
# A composed wreckage fragment of the Sydenham Crystal Palace after the
# fire of 30 November 1936: one 24 ft bay's worth of fallen structure on
# an ash slab. All structural members are the DOCUMENTED members of the
# palace (Downes 1852 plates / CONTROL-DIMENSIONS), heat-damaged:
#   - cast-iron columns, OD 10 in, bore 8 in (Plate VIII; D13/D14)
#   - plate girder, 3 ft deep (Plate VIII Fig. 12; D10)
#   - ridge-and-furrow roof: 8 ft furrow pitch, sash bars 1 x 1 3/8 in,
#     strong bars 2 1/2 in, panes 49 in long, ridge piece 3 in,
#     Paxton timber gutter 5 in base / 6 in deep (Plate XII; D09)
#   - floor boards 9 in x 1 1/2 in (1851 Catalogue pp.62-63)
# Failure behaviour is read from the photographs listed in
# refs/REFERENCES.md: the 1936 aerial (total collapse into a low,
# interlaced mat) and the ILN 1867 ground view of the same structure
# after the 1866 fire (heat-bent members in smooth arcs, drooping thin
# rods, stripped standing stubs, flat interlaced lengths).
# Re-runnable: blender -b -P build_sy36_ruin_fragment_bay.py
import bpy, math, random, os
from mathutils import Vector

random.seed(1936)
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------- documented dimensions (metres) ----------
BAY        = 7.315    # 24 ft primary unit (D06)
COL_R      = 0.127    # column outer radius (10 in OD)
COL_BORE_R = 0.1015   # column bore radius (8 in)
COLLAR_R   = 0.19     # floor collar radius (Plate VIII fig. 3, ~6 in high)
GIRDER_D   = 0.914    # girder depth 3 ft (D10)
FLANGE_W   = 0.30     # girder flange width (interpreted, Plate VIII fig.12)
FLANGE_T   = 0.045
WEB_T      = 0.025
FURROW_HALF = 1.219   # ridge CL to gutter CL, 4 ft (Plate XII fig. 1)
ROOF_RISE  = FURROW_HALF / 2.5   # slopes at 2.5 : 1  -> 0.488 m
BAR_W, BAR_D = 0.025, 0.035      # sash bar 1 in x 1 3/8 in
STRONG_W   = 0.0635              # strong bar 2 1/2 in
RIDGE_W, RIDGE_D = 0.076, 0.09   # ridge piece 3 in wide
GUT_BASE, GUT_D = 0.127, 0.152   # Paxton gutter 5 in base, 6 in deep
BOARD_W, BOARD_T = 0.229, 0.038  # floor board 9 in x 1 1/2 in

# ---------- scene reset ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
model_coll = bpy.data.collections.new("Model")
bpy.context.scene.collection.children.link(model_coll)
setup_coll = bpy.data.collections.new("RenderSetup")
bpy.context.scene.collection.children.link(setup_coll)

def mat(name, rgb, rough=0.9, metal=0.0, alpha=1.0, transmission=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if transmission > 0:
        bsdf.inputs["Transmission Weight"].default_value = transmission
        bsdf.inputs["IOR"].default_value = 1.5
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        m.surface_render_method = 'DITHERED'
    return m

M_IRON   = mat("IronBlackened", (0.078, 0.070, 0.065), 0.82, 0.55)  # heat-blackened iron
M_IRONG  = mat("IronAshGrey",   (0.23, 0.215, 0.20),  0.95, 0.15)   # ash-dusted iron
M_CHAR   = mat("CharredTimber", (0.016, 0.014, 0.013), 1.0, 0.0)   # charcoal
M_TIMBER = mat("BurntTimber",   (0.10, 0.065, 0.04),  0.95, 0.0)   # scorched, unburnt core tone
M_GLASS  = mat("GlassShard",    (0.62, 0.74, 0.70), 0.12, 0.0, transmission=0.92)
M_ASH    = mat("AshSlab",       (0.185, 0.178, 0.170), 1.0, 0.0)
M_DARK   = mat("BoreDark",      (0.008, 0.008, 0.008), 1.0, 0.0)

def link_model(obj):
    model_coll.objects.link(obj)
    return obj

def box(name, size, loc, rot=(0, 0, 0), material=None):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material: o.data.materials.append(material)
    link_model(o)
    return o

def cyl(name, r, depth, loc, rot=(0, 0, 0), material=None, verts=20):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth,
                                        location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    if material: o.data.materials.append(material)
    link_model(o)
    return o

def beam_between(name, p1, p2, w, h, material=None):
    """Box whose length runs p1->p2, cross-section w (local y) x h (local z-ish)."""
    p1, p2 = Vector(p1), Vector(p2)
    mid = (p1 + p2) / 2
    d = p2 - p1
    length = d.length
    bpy.ops.mesh.primitive_cube_add(location=mid)
    o = bpy.context.object
    o.name = name
    o.dimensions = (length, w, h)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((1, 0, 0)).rotation_difference(d.normalized())
    if material: o.data.materials.append(material)
    link_model(o)
    return o

def tube_along(name, pts, radius, material=None, verts=14):
    """Chain of cylinders following a polyline; joined into one object."""
    objs = []
    for i in range(len(pts) - 1):
        p1, p2 = Vector(pts[i]), Vector(pts[i + 1])
        d = p2 - p1
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius,
                                            depth=d.length * 1.06,
                                            location=(p1 + p2) / 2)
        o = bpy.context.object
        o.rotation_mode = 'QUATERNION'
        o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
        objs.append(o)
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    o = bpy.context.object
    o.name = name
    if material: o.data.materials.append(material)
    link_model(o)
    return o

def mound(name, loc, scale, material=None):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for p in o.data.polygons: p.use_smooth = True
    if material: o.data.materials.append(material)
    link_model(o)
    return o

# ---------- ground slab (ash field) ----------
box("Slab", (8.6, 6.6, 0.15), (0, 0, 0.075), material=M_ASH)
# ash drifts / debris mounds
mound("AshMound1", (-2.6,  2.5, 0.10), (1.5, 0.8, 0.22), M_ASH)
mound("AshMound2", ( 3.4, -2.4, 0.10), (1.1, 0.7, 0.30), M_ASH)
mound("AshMound3", ( 3.3,  2.55, 0.08), (1.3, 0.6, 0.16), M_ASH)
mound("AshMound4", (-3.3,  1.2, 0.08), (0.9, 0.7, 0.18), M_ASH)

# ---------- 1. standing column stump, kinked, broken ----------
SX, SY = -3.15, -1.55
box("StumpBasePlate", (0.61, 0.305, 0.05), (SX, SY, 0.175), material=M_IRON)
cyl("StumpCollar", COLLAR_R, 0.152, (SX, SY, 0.276), material=M_IRON)
# lower shaft, vertical to 1.55 m
cyl("StumpShaftLow", COL_R, 1.35, (SX, SY, 0.35 + 0.675), material=M_IRON)
# upper shaft kinked 11 degrees toward +x, from 1.70 m to 2.60 m
kink = math.radians(11)
top_c = (SX + math.sin(kink) * 0.45, SY, 1.70 + math.cos(kink) * 0.45)
tube_along("StumpShaftUpper", [(SX, SY, 1.62), (SX, SY, 1.72), top_c,
                              (SX + math.sin(kink) * 0.92, SY, 1.70 + math.cos(kink) * 0.92)],
           COL_R, M_IRON, verts=20)
# fracture cap: darker rough disc at the break + short bore tube
tip = (SX + math.sin(kink) * 0.92, SY, 1.70 + math.cos(kink) * 0.92)
cyl("StumpBore", COL_BORE_R, 0.06, (tip[0], tip[1], tip[2] + 0.01),
    rot=(0, kink, 0), material=M_DARK)
# fallen chunks of the same column beside the stump
cyl("ColumnChunk1", COL_R, 0.85, (SX + 0.75, SY + 0.55, 0.28),
    rot=(math.radians(90), 0, math.radians(25)), material=M_IRONG)
cyl("ColumnChunk2", COL_R, 0.55, (SX + 1.35, SY - 0.35, 0.28),
    rot=(math.radians(90), 0, math.radians(-40)), material=M_IRON)

# ---------- 2. fallen column, heat-sagged smooth curve ----------
sag_pts = [(-2.75, 1.15, 0.52), (-1.6, 0.90, 0.30), (-0.4, 0.62, 0.155),
           (0.8, 0.35, 0.155), (2.0, 0.12, 0.30), (3.05, -0.15, 0.55)]
tube_along("FallenColumn", sag_pts, COL_R, M_IRON, verts=20)
# its floor collar, still on the shaft near the low end
cyl("FallenCollar", COLLAR_R, 0.152, (-2.35, 1.03, 0.42),
    rot=(math.radians(78), 0, math.radians(-72)), material=M_IRONG)
# broken far end: dark bore disc
cyl("FallenBore", COL_BORE_R, 0.05, (3.08, -0.16, 0.57),
    rot=(math.radians(96), 0, math.radians(-72)), material=M_DARK)

# ---------- 3. fallen plate girder, sagging + twisted ----------
# Built as three long plates (web + 2 flanges) subdivided along their
# length, then bent per-vertex: a smooth heat sag (ends propped on
# debris, middle down) with a progressive twist about the long axis.
import bmesh
GY = 2.72
def girder_part(name, cy, cz, sy, sz):
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    o = bpy.context.object
    o.dimensions = (BAY, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bm = bmesh.new()
    bm.from_mesh(o.data)
    long_edges = [e for e in bm.edges if e.calc_length() > 1.0]
    bmesh.ops.subdivide_edges(bm, edges=long_edges, cuts=28)
    bm.to_mesh(o.data)
    bm.free()
    for v in o.data.vertices:
        x, y, z = v.co
        t = min(1.0, max(0.0, x / BAY + 0.5))
        za = 0.52 - 0.36 * max(0.0, math.sin(math.pi * t)) ** 1.5   # axis height (sag)
        a = math.radians(-4 + 13 * t)                     # twist
        yy, zz = y + cy, z + cz
        v.co = (x, GY + yy * math.cos(a) - zz * math.sin(a),
                za + yy * math.sin(a) + zz * math.cos(a))
    o.name = name
    return o
gparts = [girder_part("GirderWeb", 0, 0, WEB_T, GIRDER_D - 2 * FLANGE_T),
          girder_part("GirderFlangeT", 0,  (GIRDER_D - FLANGE_T) / 2, FLANGE_W, FLANGE_T),
          girder_part("GirderFlangeB", 0, -(GIRDER_D - FLANGE_T) / 2, FLANGE_W, FLANGE_T)]
bpy.ops.object.select_all(action='DESELECT')
for o in gparts: o.select_set(True)
bpy.context.view_layer.objects.active = gparts[0]
bpy.ops.object.join()
g = bpy.context.object
g.name = "FallenGirder"
g.data.materials.append(M_IRONG)
link_model(g)

# ---------- 4. collapsed ridge-and-furrow roof section ----------
# Local frame: panel centred at (1.35, 1.45), rotated -18 deg about z.
# Local x = along the bay (bars spaced along it), local y = across the
# furrow (gutter - ridge - gutter), local z up. The section has slumped:
# the ridge sits at ~55% of its true rise above the near gutter, the far
# gutter is tipped up on fallen debris; every sash bar droops.
PANEL_C = Vector((1.15, 0.85, 0.0))
PANEL_ROT = math.radians(-18)
def L2W(lx, ly, lz):
    """local panel coords -> world"""
    c, s = math.cos(PANEL_ROT), math.sin(PANEL_ROT)
    return (PANEL_C.x + lx * c - ly * s, PANEL_C.y + lx * s + ly * c, lz)

PANEL_LEN = 3.6
GUT_NEAR_Z = 0.30          # near gutter lies on the slab (top ~0.30)
RIDGE_Z = GUT_NEAR_Z + ROOF_RISE * 0.55   # slumped ridge ~0.57
GUT_FAR_Z = 0.46           # far gutter propped on debris
# Paxton gutters: base + two cheeks, in 3 chained lengths each
def gutter(name, ly, zbase, mat, breaks=()):
    xs = [-PANEL_LEN / 2, -0.6, 0.7, PANEL_LEN / 2]
    for i in range(3):
        if i in breaks: continue
        zoff = 0.03 * math.sin(i * 2.1)
        for nm, dyy, dzz, sy, sz in [("base", 0.0, GUT_D / 2, GUT_BASE, 0.03),
                                     ("ch1", -GUT_BASE / 2 + 0.012, GUT_D / 2, 0.024, GUT_D),
                                     ("ch2",  GUT_BASE / 2 - 0.012, GUT_D / 2, 0.024, GUT_D)]:
            p1 = L2W(xs[i], ly + dyy, zbase + dzz + zoff)
            p2 = L2W(xs[i + 1], ly + dyy, zbase + dzz + zoff * 0.4)
            beam_between(f"{name}_{i}_{nm}", p1, p2, sy, sz, mat)
gutter("GutterNear", -FURROW_HALF, 0.15, M_CHAR)
gutter("GutterFar",   FURROW_HALF, GUT_FAR_Z - GUT_D, M_CHAR, breaks=(1,))
# ridge piece, sagging in 3 lengths
rx = [-PANEL_LEN / 2, -0.6, 0.7, PANEL_LEN / 2]
for i in range(3):
    zm = RIDGE_Z - 0.05 * (1 if i == 1 else 0)
    beam_between(f"Ridge_{i}", L2W(rx[i], 0, RIDGE_Z), L2W(rx[i + 1], 0, zm),
                 RIDGE_W, RIDGE_D, M_CHAR)
# sash bars: gutter -> ridge on both slopes, drooping mid-point
bar_xs = [x for x in [ -PANEL_LEN/2 + 0.13 + 0.267 * k for k in range(14)]]
strong_at = {3, 7, 11}
for side, (ly0, z0) in [("N", (-FURROW_HALF, GUT_NEAR_Z)), ("F", (FURROW_HALF, GUT_FAR_Z))]:
    for k, bx in enumerate(bar_xs):
        wdt = STRONG_W if k in strong_at else BAR_W
        p_start = L2W(bx, ly0, z0)
        p_ridge = L2W(bx, 0, RIDGE_Z)
        mid = ((p_start[0] + p_ridge[0]) / 2, (p_start[1] + p_ridge[1]) / 2,
               (p_start[2] + p_ridge[2]) / 2 - 0.055)   # heat droop
        m = M_TIMBER if k % 4 else M_CHAR
        beam_between(f"Bar{side}{k}a", p_start, mid, wdt, BAR_D, m)
        beam_between(f"Bar{side}{k}b", mid, p_ridge, wdt, BAR_D, m)
# glass shards still held in the near slope, close to the ridge
for i, (bx, ly, tilt) in enumerate([(-0.9, -0.35, 0.10), (-0.35, -0.55, 0.06),
                                    (0.55, -0.30, 0.16), (1.15, -0.62, 0.05)]):
    p = L2W(bx, ly, GUT_NEAR_Z + (RIDGE_Z - GUT_NEAR_Z) * (1 - abs(ly) / FURROW_HALF) + 0.03)
    o = box(f"HeldShard{i}", (0.24, 1.05, 0.004), p,
            rot=(tilt, 0.1, PANEL_ROT + math.radians(90) * 0 + 0.30), material=M_GLASS)

# ---------- 5. charred floor boards ----------
board_specs = [
    ((-1.9, 0.3, 0.19), 0.5, 2.5), ((-1.7, 0.62, 0.19), 0.44, 2.3),
    ((-1.85, 0.45, 0.235), 0.47, 1.6),   # one stacked, shorter (snapped)
    ((0.2, -0.9, 0.18), -0.9, 2.4), ((2.7, -2.2, 0.18), 2.6, 2.1),
    ((-0.6, -1.5, 0.18), 0.15, 1.9),
]
for i, (loc, ang, ln) in enumerate(board_specs):
    box(f"Board{i}", (ln, BOARD_W, BOARD_T), loc, rot=(0, 0, ang),
        material=M_CHAR if i != 4 else M_TIMBER)
# snapped-off board end, tilted against a mound
box("BoardSnap", (0.7, BOARD_W, BOARD_T), (2.55, -1.95, 0.26),
    rot=(0.18, 0.1, 2.75), material=M_CHAR)

# ---------- 6. drooping thin rods (tie/louvre rods, heat-bent) ----------
rod_specs = [
    ((3.55, -1.7, 0.3), 1.55, 0.55), ((-3.75, 0.6, 0.2), 1.15, -0.4),
    ((-2.2, 2.75, 0.25), 0.95, 2.8), ((-0.9, -2.9, 0.35), 1.3, 1.9),
]
for i, (base, h, lean_ang) in enumerate(rod_specs):
    bx, by, bz = base
    tipx = bx + math.cos(lean_ang) * 0.45
    tipy = by + math.sin(lean_ang) * 0.45
    pts = [(bx, by, bz), (bx + math.cos(lean_ang) * 0.06, by + math.sin(lean_ang) * 0.06, bz + h * 0.55),
           (bx + math.cos(lean_ang) * 0.20, by + math.sin(lean_ang) * 0.20, bz + h * 0.88),
           (tipx, tipy, bz + h * 0.92)]   # tip wilts over
    tube_along(f"Rod{i}", pts, 0.016, M_IRON, verts=8)

# ---------- 7. scattered glass shards on the slab ----------
for i in range(24):
    cx = random.uniform(-3.9, 4.0)
    cy = random.uniform(-3.0, 3.0)
    # concentrate near the roof panel
    if i < 14:
        cx = 1.15 + random.uniform(-2.0, 2.0)
        cy = 0.85 + random.uniform(-1.7, 1.7)
    s = random.uniform(0.08, 0.30)
    box(f"Shard{i}", (s, s * random.uniform(0.5, 0.9), 0.004),
        (cx, cy, 0.155), rot=(0, 0, random.uniform(0, 3.14)), material=M_GLASS)
# a small stack of unbroken panes, slid off the fallen panel
for i in range(3):
    box(f"PaneStack{i}", (0.25, 1.20, 0.004), (3.30, 0.30 + i * 0.02, 0.16 + i * 0.006),
        rot=(0.02 * i, 0, math.radians(-32)), material=M_GLASS)

# ---------- render setup ----------
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.cycles.use_denoising = True
scene.render.resolution_x = 960
scene.render.resolution_y = 720
scene.render.film_transparent = False
world = bpy.data.worlds.new("W")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.52, 0.52, 0.52, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

def setup_obj(o):
    setup_coll.objects.link(o)
    return o

bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -0.001))
gp = bpy.context.object; gp.name = "Ground"
gm = mat("GroundGrey", (0.46, 0.46, 0.46), 1.0)
gp.data.materials.append(gm); setup_obj(gp)

bpy.ops.object.light_add(type='SUN', location=(6, -4, 10))
sun = bpy.context.object; sun.name = "Sun"
sun.data.energy = 3.6; sun.data.angle = math.radians(8)
sun.rotation_euler = (math.radians(52), math.radians(12), math.radians(38))
setup_obj(sun)
bpy.ops.object.light_add(type='AREA', location=(-7, 6, 7))
fill = bpy.context.object; fill.name = "Fill"
fill.data.energy = 450; fill.data.shape = 'DISK'; fill.data.size = 6
fill.rotation_euler = (math.radians(55), math.radians(-18), math.radians(-128))
setup_obj(fill)

def camera(name, loc, target, lens=42):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object; c.name = name
    c.data.lens = lens
    d = Vector(target) - Vector(loc)
    c.rotation_mode = 'QUATERNION'
    c.rotation_quaternion = d.to_track_quat('-Z', 'Y')
    setup_obj(c)
    return c

cams = {
    "front":        camera("CamFront", (0, -11.5, 2.0), (0, 0, 0.7)),
    "side":         camera("CamSide", (11.5, 0, 2.0), (0, 0, 0.7)),
    "three-quarter": camera("CamTQ", (7.6, -7.8, 4.6), (0, 0, 0.55)),
}

# ---------- save, export, render ----------
def tri_count():
    dg = bpy.context.evaluated_depsgraph_get()
    total = 0
    for o in model_coll.objects:
        if o.type != 'MESH': continue
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        total += len(me.loop_triangles)
        ev.to_mesh_clear()
    return total

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "sy36-ruin-fragment-bay.blend"))
print("TRIANGLES:", tri_count())

bpy.ops.object.select_all(action='DESELECT')
for o in model_coll.objects: o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "sy36-ruin-fragment-bay.glb"),
                          export_format='GLB', use_selection=True, export_apply=True)
bpy.ops.object.select_all(action='DESELECT')

if os.environ.get("SKIP_RENDER") != "1":
    for key, cam in cams.items():
        scene.camera = cam
        scene.render.filepath = os.path.join(OUT, "renders", key + ".png")
        bpy.ops.render.render(write_still=True)
        print("RENDERED", key)
print("DONE")
