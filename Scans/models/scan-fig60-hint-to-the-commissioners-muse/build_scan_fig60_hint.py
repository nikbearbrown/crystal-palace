#!/usr/bin/env python3
"""Build scan-fig60-hint-to-the-commissioners: John Leech, "A Hint to the
Commissioners", Punch, 26 April 1851. Three French visitors puzzle over a
washstand exhibit outdoors; an attendant in a top hat gestures at it.
Blender 4.5.3, metres, origin at base centre. Re-runnable:
  blender -b --python build_scan_fig60_hint.py
Outputs .blend, .glb, preview.png beside this script. No lettering anywhere;
figures are stylised, without caricature exaggeration."""
import bpy, math, os
from mathutils import Vector, Matrix

# ---------- scene reset ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ---------- materials (sRGB -> linear conversion applied) ----------
def _lin(v):
    return ((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92

def mat(name, srgb, rough=0.75, metal=0.0, alpha=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    r, g, bl = (_lin(c) for c in srgb)
    b.inputs["Base Color"].default_value = (r, g, bl, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if alpha is not None:
        b.inputs["Alpha"].default_value = alpha
        m.surface_render_method = 'DITHERED'
    return m

SKIN  = mat("SkinTone", (0.90, 0.68, 0.53), 0.65)
HAIR_D = mat("HairDark", (0.16, 0.11, 0.08), 0.8)
BLACK = mat("CoatBlack", (0.045, 0.045, 0.055), 0.8)
CHARC = mat("Charcoal", (0.13, 0.13, 0.14), 0.85)
CHECK = mat("CheckSuit", (0.36, 0.30, 0.26), 0.9)
CHECK_D = mat("CheckSuitDark", (0.24, 0.19, 0.16), 0.9)
ROBE  = mat("RobePattern", (0.42, 0.20, 0.13), 0.9)
ROBE_D = mat("RobeTrim", (0.25, 0.12, 0.08), 0.9)
CREAM = mat("WaistcoatCream", (0.90, 0.84, 0.68), 0.8)
WHITE = mat("WhiteCeramic", (0.93, 0.92, 0.88), 0.35)
CERAM = mat("CeramicBlue", (0.55, 0.65, 0.75), 0.35)
BROWN = mat("BrownCoat", (0.30, 0.20, 0.12), 0.85)
TAN   = mat("TrouserTan", (0.66, 0.55, 0.38), 0.9)
WOOD_D = mat("WoodDark", (0.28, 0.18, 0.10), 0.85)
WOOD_M = mat("WoodMid", (0.45, 0.30, 0.17), 0.85)
WOOD_L = mat("WoodLight", (0.62, 0.46, 0.28), 0.85)
STONE = mat("Stone", (0.74, 0.70, 0.62), 0.9)
GROUND = mat("Ground", (0.58, 0.55, 0.49), 1.0)
LEAF  = mat("LeafMuted", (0.32, 0.42, 0.24), 0.95)
BARK  = mat("Bark", (0.30, 0.22, 0.15), 1.0)
IRON  = mat("IronDark", (0.10, 0.10, 0.11), 0.6, 0.5)
PAPER = mat("PaperBlank", (0.92, 0.90, 0.84), 0.9)

# ---------- primitive helpers ----------
def _fin(o, material):
    if material: o.data.materials.append(material)
    return o

def box(name, loc, dims, material=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _fin(o, material)

def cyl(name, loc, r, depth, material=None, vertices=20, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    return _fin(o, material)

def frustum(name, loc, r_bot, r_top, depth, material=None, vertices=20, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r_bot, radius2=r_top, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    return _fin(o, material)

def sphere(name, loc, r, material=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=18, ring_count=12, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _fin(o, material)

def torus(name, loc, R, r, material=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=22, minor_segments=8, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    return _fin(o, material)

def strut(name, a, b, r, material=None, vertices=10):
    a, b = Vector(a), Vector(b)
    d = b - a; L = d.length
    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=L, location=(a + b) / 2)
    o = bpy.context.object; o.name = name; o.rotation_euler = q.to_euler()
    return _fin(o, material)

def xform(objs, matrix):
    for o in objs:
        o.matrix_world = matrix @ o.matrix_world

def place(objs, loc, ry=0.0):
    M = Matrix.Translation(Vector(loc)) @ Matrix.Rotation(ry, 4, 'Z')
    xform(objs, M)

def lathe(name, profile, material, segments=24):
    """profile: list of (r, z) from bottom to top; surface of revolution about Z at origin."""
    import bmesh
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    ring_vs = []
    for r, z in profile:
        rv = []
        for i in range(segments):
            a = 2 * math.pi * i / segments
            rv.append(bm.verts.new((r * math.cos(a), r * math.sin(a), z)))
        ring_vs.append(rv)
    for j in range(len(profile) - 1):
        for i in range(segments):
            i2 = (i + 1) % segments
            bm.faces.new((ring_vs[j][i], ring_vs[j][i2], ring_vs[j + 1][i2], ring_vs[j + 1][i]))
    # cap bottom and top centres if radius > 0
    for j in (0, len(profile) - 1):
        r, z = profile[j]
        if r > 0.001:
            c = bm.verts.new((0, 0, z))
            for i in range(segments):
                i2 = (i + 1) % segments
                if j == 0: bm.faces.new((c, ring_vs[j][i2], ring_vs[j][i]))
                else: bm.faces.new((c, ring_vs[j][i], ring_vs[j][i2]))
    bm.normal_update()
    bm.to_mesh(mesh); bm.free()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(o)
    if material: mesh.materials.append(material)
    return o

# ---------- hats ----------
def hat_top(name, hz, s, m=BLACK):
    return [cyl(f"{name}_brim", (0, 0, hz), 0.145 * s, 0.014, m, 22),
            cyl(f"{name}_crown", (0, 0, hz + 0.095 * s), 0.098 * s, 0.185 * s, m, 20)]

def hat_wide(name, hz, s, m=BROWN):
    return [cyl(f"{name}_brim", (0, 0, hz), 0.185 * s, 0.012, m, 22),
            sphere(f"{name}_crown", (0, 0, hz + 0.045 * s), 0.105 * s, m, scale=(1, 1, 0.62))]

def hat_cap(name, hz, s, m=CHARC):
    parts = [sphere(f"{name}_cap", (0, 0.01, hz + 0.01), 0.108 * s, m, scale=(1, 1, 0.62))]
    parts.append(box(f"{name}_peak", (0, -0.115 * s, hz), (0.11 * s, 0.085 * s, 0.012), m))
    return parts

# ---------- figures (batch house style: tapered masses, simple heads) ----------
def figure_man(name, suit=BLACK, hat='top', h=1.75, portly=1.0, waist=None,
               armL=None, armR=None, trouser=None, hair=HAIR_D, beard=False):
    s = h / 1.75; p = portly
    trouser = trouser or CHARC
    parts = []
    for sd, sgn in (("L", -1), ("R", 1)):
        parts.append(box(f"{name}_shoe{sd}", (sgn * 0.10 * s, -0.045, 0.03), (0.09 * s, 0.25 * s, 0.06), BLACK))
        parts.append(strut(f"{name}_leg{sd}", (sgn * 0.095 * s, 0, 0.95 * s), (sgn * 0.10 * s, -0.01, 0.07), 0.057 * s, trouser))
    parts.append(frustum(f"{name}_coatskirt", (0, 0.01, 0.80 * s), 0.212 * s * p, 0.163 * s * p, 0.42 * s, suit))
    parts.append(box(f"{name}_tails", (0, 0.155 * s * p, 0.76 * s), (0.19 * s, 0.035, 0.44 * s), suit, rot=(math.radians(6), 0, 0)))
    upper = []
    upper.append(frustum(f"{name}_torso", (0, 0, 0.24 * s), 0.163 * s * p, 0.140 * s * p, 0.46 * s, suit))
    upper.append(sphere(f"{name}_shoulders", (0, 0, 0.455 * s), 0.20 * s * p, suit, scale=(1, 0.60, 0.52)))
    if waist:
        upper.append(box(f"{name}_waistcoat", (0, -0.148 * s * p, 0.22 * s), (0.205 * s, 0.025, 0.36 * s), waist))
    upper.append(cyl(f"{name}_neck", (0, 0, 0.52 * s), 0.045 * s, 0.08 * s, SKIN, 12))
    upper.append(sphere(f"{name}_head", (0, -0.005, 0.665 * s), 0.105 * s, SKIN))
    if beard:
        upper.append(sphere(f"{name}_beard", (0, -0.055 * s, 0.585 * s), 0.095 * s, HAIR_D, scale=(0.92, 0.72, 1.15)))
    hz = 0.745 * s
    if hat == 'top': upper += hat_top(name, hz, s)
    elif hat == 'wide': upper += hat_wide(name, hz, s)
    elif hat == 'cap': upper += hat_cap(name, hz, s)
    defs = {"L": ((-0.30 * s * p, -0.03, 0.20 * s), (-0.26 * s * p, -0.05, -0.18 * s)),
            "R": ((0.30 * s * p, -0.03, 0.20 * s), (0.26 * s * p, -0.05, -0.18 * s))}
    for sd, arm in (("L", armL), ("R", armR)):
        sgn = -1 if sd == "L" else 1
        elbow, hand = arm if arm else defs[sd]
        sh = (sgn * 0.215 * s * p, 0, 0.43 * s)
        upper.append(strut(f"{name}_arm{sd}u", sh, elbow, 0.047 * s, suit))
        upper.append(strut(f"{name}_arm{sd}f", elbow, hand, 0.040 * s, suit))
        upper.append(sphere(f"{name}_hand{sd}", hand, 0.040 * s, SKIN))
    xform(upper, Matrix.Translation(Vector((0, 0, 0.98 * s))))
    parts += upper
    return parts

def lights_and_camera(cam_loc, target, lens=38, res=(960, 720), samples=48):
    bpy.ops.object.light_add(type='AREA', location=(3.5, -4.5, 5.5))
    key = bpy.context.object; key.name = "KeyLight"; key.data.energy = 550; key.data.shape = 'DISK'; key.data.size = 3.2
    key.rotation_euler = (math.radians(55), 0, math.radians(35))
    bpy.ops.object.light_add(type='AREA', location=(-4.5, -2.5, 3.5))
    fill = bpy.context.object; fill.name = "FillLight"; fill.data.energy = 220; fill.data.size = 2.6
    fill.rotation_euler = (math.radians(65), 0, math.radians(-50))
    bpy.ops.object.light_add(type='AREA', location=(0, 4.5, 4.0))
    back = bpy.context.object; back.name = "BackLight"; back.data.energy = 260; back.data.size = 3.0
    back.rotation_euler = (math.radians(120), 0, 0)
    world = bpy.data.worlds.new("World"); scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.55
    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.object; cam.name = "PreviewCamera"
    direction = Vector(target) - Vector(cam_loc)
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = lens
    scene.camera = cam
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.cycles.device = 'CPU'
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.film_transparent = False
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'Medium Contrast'

def finish(slug, outdir):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.select_all(action='DESELECT')
    tris = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for o in bpy.data.objects:
        if o.type == 'MESH':
            ev = o.evaluated_get(dg); m = ev.to_mesh(); m.calc_loop_triangles()
            tris += len(m.loop_triangles); ev.to_mesh_clear()
    print(f"TRIANGLE_COUNT {tris}")
    print(f"OBJECT_COUNT {len(bpy.data.objects)}")
    blend_path = os.path.join(outdir, slug + ".blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    glb_path = os.path.join(outdir, slug + ".glb")
    bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB')
    scene.render.filepath = os.path.join(outdir, "preview.png")
    bpy.ops.render.render(write_still=True)
    print("DONE", blend_path, glb_path)

# ============================================================
# SCENE — fig-60 "A Hint to the Commissioners" (Leech, Punch 1851)
# Vignette ~6 m: three visitors (left) study a washstand (centre-right);
# attendant (right) gestures at it. Tree + exhibition arcade behind.
# ============================================================
OUT = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig60-hint-to-the-commissioners"

# ---- ground ----
box("Ground", (0, 0.3, -0.03), (6.6, 3.6, 0.06), GROUND)

# ---- tree: trunk centre-back, two branches, sparse canopy masses ----
frustum("TreeTrunk", (0.55, 0.85, 1.35), 0.21, 0.13, 2.7, BARK, 12)
strut("BranchL", (0.55, 0.85, 2.45), (-0.75, 0.95, 3.05), 0.055, BARK)
strut("BranchR", (0.55, 0.85, 2.55), (1.75, 0.95, 3.15), 0.05, BARK)
for i, (cx, cy, cz, sx, sy, sz) in enumerate((
        (-0.6, 0.95, 3.25, 1.15, 0.55, 0.42), (0.75, 0.95, 3.45, 1.25, 0.6, 0.45),
        (1.7, 0.95, 3.3, 0.95, 0.5, 0.4), (-1.35, 0.9, 3.0, 0.8, 0.45, 0.38))):
    sphere(f"Canopy_{i}", (cx, cy, cz), 0.62, LEAF, scale=(sx, sy, sz))

# ---- exhibition arcade wall hint, back right (behind attendant) ----
box("ArcadeWall", (2.35, 1.05, 1.25), (2.1, 0.14, 2.5), STONE)
for i, ax in enumerate((1.75, 2.35, 2.95)):
    # arch opening suggested by dark inset + arch top
    box(f"ArchDark_{i}", (ax, 0.96, 0.95), (0.42, 0.03, 1.55), mat("ArchShade", (0.30, 0.28, 0.24), 1.0))
    torus(f"ArchTop_{i}", (ax, 0.945, 1.72), 0.21, 0.028, STONE, rot=(0, 0, 0))
box("ArcadeCornice", (2.35, 1.05, 2.56), (2.2, 0.2, 0.12), STONE)

# ---- THE WASHSTAND (key prop), centre-right ----
WS = (1.15, 0, 0)  # front-left corner reference: centre of stand
# legs
for sx in (-1, 1):
    for sy in (-1, 1):
        box(f"WS_leg_{sx}_{sy}", (WS[0] + sx * 0.52, sy * 0.20, 0.40), (0.055, 0.055, 0.80), WOOD_D)
# top slab + apron with two drawers
box("WS_top", (WS[0], 0, 0.845), (1.16, 0.52, 0.05), WOOD_M)
box("WS_apron", (WS[0], -0.225, 0.72), (1.10, 0.05, 0.20), WOOD_M)
for i, dx in enumerate((-0.28, 0.28)):
    box(f"WS_drawer_{i}", (WS[0] + dx, -0.255, 0.72), (0.46, 0.02, 0.15), WOOD_L)
    sphere(f"WS_knob_{i}", (WS[0] + dx, -0.27, 0.72), 0.018, IRON)
# raised back splash board with two blank card panels
box("WS_back", (WS[0], 0.245, 1.02), (1.16, 0.04, 0.40), WOOD_D)
for i, dx in enumerate((-0.29, 0.29)):
    box(f"WS_card_{i}", (WS[0] + dx, 0.218, 1.04), (0.40, 0.012, 0.26), PAPER)
box("WS_backrail", (WS[0], 0.245, 1.235), (1.16, 0.05, 0.035), WOOD_D)
# lower shelf
box("WS_shelf", (WS[0], 0, 0.16), (1.08, 0.44, 0.035), WOOD_M)

def ewer_and_basin(name, cx, cy, ceramic):
    parts = []
    # basin: wide shallow lathe bowl on the table top (z=0.87)
    b = lathe(f"{name}_basin", [(0.001, 0.0), (0.13, 0.005), (0.20, 0.03), (0.235, 0.075), (0.245, 0.10)], ceramic)
    b.location = (cx, cy, 0.87); parts.append(b)
    # ewer standing in/behind the basin
    e = lathe(f"{name}_ewer", [(0.001, 0.0), (0.075, 0.005), (0.095, 0.05), (0.105, 0.11),
                              (0.075, 0.19), (0.048, 0.235), (0.062, 0.265), (0.085, 0.27)], ceramic)
    e.location = (cx + 0.02, cy + 0.01, 0.90); parts.append(e)
    # handle: half-torus at the ewer's back
    parts.append(torus(f"{name}_handle", (cx + 0.115, cy + 0.01, 1.075), 0.052, 0.011, ceramic, rot=(0, math.radians(90), 0)))
    # spout hint
    parts.append(frustum(f"{name}_spout", (cx - 0.075, cy + 0.01, 1.10), 0.016, 0.026, 0.07, ceramic, 10, rot=(0, math.radians(115), 0)))
    return parts

ewer_and_basin("SetL", WS[0] - 0.30, -0.02, WHITE)
ewer_and_basin("SetR", WS[0] + 0.30, 0.0, CERAM)

# big slop basin + jug on the lower shelf
sb = lathe("SlopBasin", [(0.001, 0.0), (0.16, 0.005), (0.26, 0.04), (0.315, 0.10), (0.325, 0.13)], WHITE)
sb.location = (WS[0] + 0.05, 0, 0.18)
jug = lathe("ShelfJug", [(0.001, 0.0), (0.09, 0.005), (0.115, 0.07), (0.10, 0.15), (0.06, 0.19), (0.075, 0.21)], CERAM)
jug.location = (WS[0] + 0.05, 0, 0.20)

# stave bucket with lidded jug, at the stand's right foot
BK = (2.05, -0.30)
bk = lathe("Bucket", [(0.20, 0.0), (0.225, 0.06), (0.235, 0.16), (0.225, 0.26), (0.215, 0.30)], WOOD_L)
bk.location = (BK[0], BK[1], 0.0)
for bz in (0.07, 0.23):
    torus(f"BucketBand_{bz}", (BK[0], BK[1], bz), 0.232 if bz < 0.1 else 0.222, 0.010, IRON)
torus("BucketHandle", (BK[0], BK[1], 0.36), 0.19, 0.011, IRON, rot=(0, 0, 0))
kj = lathe("KettleJug", [(0.001, 0.0), (0.075, 0.005), (0.095, 0.05), (0.07, 0.11), (0.078, 0.125)], WOOD_D)
kj.location = (BK[0] - 0.02, BK[1], 0.26)
cyl("KettleLid", (BK[0] - 0.02, BK[1], 0.395), 0.05, 0.018, IRON, 14)

# ---- figures ----
# 1) robed visitor (left): long robe to the ground, wide collar, wide-brim hat
robe = []
robe.append(frustum("Robe_body", (0, 0, 0.78), 0.30, 0.185, 1.56, ROBE, 18))
robe.append(frustum("Robe_collar", (0, 0.02, 1.50), 0.13, 0.215, 0.16, ROBE_D, 18))
robe.append(cyl("Robe_neck", (0, 0, 1.585), 0.045, 0.06, SKIN, 12))
robe.append(sphere("Robe_head", (0, -0.005, 1.695), 0.105, SKIN))
robe += [h for h in hat_wide("Robe", 1.775, 1.12, ROBE_D)]
robe.append(box("Robe_shoeL", (-0.10, -0.05, 0.03), (0.09, 0.25, 0.06), BLACK))
robe.append(box("Robe_shoeR", (0.10, -0.05, 0.03), (0.09, 0.25, 0.06), BLACK))
# vertical pattern stripes on the robe (flat thin strips, front)
for i, sx in enumerate((-0.16, -0.06, 0.05, 0.15)):
    robe.append(box(f"Robe_stripe_{i}", (sx, -0.245 + abs(sx) * 0.55, 0.75), (0.028, 0.012, 1.30), ROBE_D))
place(robe, (-1.95, -0.15, 0), ry=math.radians(20))

# 2) tall bearded visitor in top hat and checked suit, hand to chest
fig2 = figure_man("Check", suit=CHECK, hat='top', h=1.80, portly=0.95, trouser=CHECK_D,
                  beard=True, armR=((-0.02, -0.10, 0.30), (-0.10, -0.185, 0.06)))
place(fig2, (-1.15, -0.05, 0), ry=math.radians(12))

# 3) capped visitor, high collar, cream waistcoat, baggy trousers, arms hanging
fig3 = figure_man("Cap", suit=BROWN, hat='cap', h=1.72, portly=0.9, waist=CREAM, trouser=TAN)
place(fig3, (-0.35, 0.0, 0), ry=math.radians(7))

# 4) attendant (right of the stand): top hat, cream waistcoat, near arm
# extended in an open gesture toward the washstand
fig4 = figure_man("Attendant", suit=CHARC, hat='top', h=1.76, portly=0.92, waist=CREAM,
                  armL=((0.02, -0.26, 0.20), (-0.34, -0.46, 0.08)))
place(fig4, (2.30, -0.05, 0), ry=math.radians(-22))

lights_and_camera((0.35, -5.6, 2.1), (0.15, 0.1, 1.0), lens=40, res=(960, 800))
finish(SLUG, OUT)
