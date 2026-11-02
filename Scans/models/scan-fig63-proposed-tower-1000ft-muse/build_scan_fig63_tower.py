#!/usr/bin/env python3
"""Build scan-fig63-proposed-tower-1000ft: "Design for the conversion of the
Exhibition Building into a Tower 1000 Feet High" by Mr C. Burton (engraving,
1851). Modelled as an architect's presentation model at 1:100: the design is
1000 ft = 304.8 m, so the model stands 3.048 m on a landscaped baseboard with
two blank annotation boards. Blender 4.5.3, metres, origin at base centre.
Re-runnable:
  blender -b --python build_scan_fig63_tower.py
Outputs .blend, .glb, preview.png beside this script. No lettering anywhere."""
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

STONE  = mat("ModelStone", (0.82, 0.79, 0.72), 0.9)
STONE_D = mat("ModelStoneShade", (0.68, 0.64, 0.56), 0.9)
GLASSM = mat("PalaceGlass", (0.62, 0.72, 0.76), 0.35)
FRAME  = mat("PalaceFrame", (0.90, 0.88, 0.82), 0.8)
DARKIN = mat("DarkOpening", (0.14, 0.13, 0.11), 1.0)
WOOD_D = mat("BaseWood", (0.30, 0.19, 0.10), 0.7)
LAWN   = mat("ModelLawn", (0.45, 0.55, 0.32), 1.0)
PATH   = mat("GravelPath", (0.80, 0.76, 0.66), 1.0)
TREE   = mat("TreeGreen", (0.25, 0.38, 0.20), 1.0)
PAPER  = mat("PaperBlank", (0.92, 0.90, 0.84), 0.9)
RED    = mat("FlagRed", (0.55, 0.10, 0.10), 0.85)
FIGD   = mat("FigureDark", (0.10, 0.10, 0.11), 0.9)

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
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=16, ring_count=10, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _fin(o, material)

def torus(name, loc, R, r, material=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=24, minor_segments=8, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    return _fin(o, material)

def strut(name, a, b, r, material=None, vertices=8):
    a, b = Vector(a), Vector(b)
    d = b - a; L = d.length
    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=L, location=(a + b) / 2)
    o = bpy.context.object; o.name = name; o.rotation_euler = q.to_euler()
    return _fin(o, material)

def banded_block(name, z0, z1, w, d, ledge_every, mat_body=STONE, mullions=0):
    """A tower tier: core block + horizontal floor ledges proud of the front
    and sides + optional vertical mullion strips on the front face."""
    h = z1 - z0
    box(f"{name}_core", (0, 0, z0 + h / 2), (w, d, h), mat_body)
    n = max(1, int(h / ledge_every))
    for i in range(1, n + 1):
        z = z0 + i * ledge_every
        if z >= z1 - 0.005: continue
        box(f"{name}_ledge{i}", (0, -0.006, z), (w + 0.018, d + 0.012, 0.012), FRAME)
    if mullions:
        for i in range(mullions):
            x = -w / 2 + (i + 0.5) * (w / mullions)
            box(f"{name}_mull{i}", (x, -d / 2 - 0.004, z0 + h / 2), (0.010, 0.008, h * 0.96), FRAME)
    # top cornice
    box(f"{name}_cornice", (0, 0, z1 - 0.008), (w + 0.03, d + 0.03, 0.016), FRAME)

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
# SCENE — fig-63 Burton's 1000-ft conversion tower as a 1:100 model.
# Design height 1000 ft = 304.8 m -> model tower 3.048 m.
# ============================================================
OUT = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig63-proposed-tower-1000ft"

# ---- display baseboard + landscaped plinth ----
box("Baseboard", (0, 0, 0.025), (2.3, 1.8, 0.05), WOOD_D)
box("Plinth", (0, 0, 0.075), (2.0, 1.5, 0.05), LAWN)
# paths: main approach + cross path, as in the print
box("PathMain", (0, -0.45, 0.103), (0.22, 0.85, 0.008), PATH)
box("PathCross", (0, -0.10, 0.103), (1.7, 0.16, 0.008), PATH)
box("Terrace", (0, 0.02, 0.108), (1.15, 0.55, 0.012), PATH)
# model trees around the base
for i, (tx, ty, th) in enumerate(((-0.85, -0.35, 0.16), (-0.72, 0.28, 0.13), (0.85, -0.30, 0.15),
                                  (0.74, 0.30, 0.12), (-0.45, -0.55, 0.11), (0.5, -0.58, 0.12))):
    cyl(f"TreeTrunk_{i}", (tx, ty, 0.10 + th * 0.35), 0.008, th * 0.7, WOOD_D, 8)
    sphere(f"TreeTop_{i}", (tx, ty, 0.10 + th * 0.85), th * 0.42, TREE, scale=(1, 1, 1.25))
# two tiny visitors on the path (1:100 people, ~0.017 m)
for i, (fx, fy) in enumerate(((0.06, -0.42), (-0.05, -0.30))):
    cyl(f"Visitor{i}", (fx, fy, 0.108), 0.0035, 0.011, FIGD, 8)
    sphere(f"VisitorHead{i}", (fx, fy, 0.122), 0.0028, FIGD)

BASE_Z = 0.11  # top of terrace

# ---- Tier 0: the Crystal Palace base (as drawn: nave + transept arch) ----
banded_block("Palace", BASE_Z, BASE_Z + 0.30, 0.80, 0.30, 0.10, mat_body=GLASSM, mullions=7)
# side wings, lower
for sx in (-1, 1):
    banded_block(f"Wing{sx}", BASE_Z, BASE_Z + 0.18, 0.20, 0.26, 0.09, mat_body=GLASSM, mullions=0)
    # reposition wing core/ledges: banded_block builds at x=0; shift via last objects is messy,
    # so wings are rebuilt manually below instead.
# (wing blocks from banded_block sit at centre; remove and rebuild at sides)
# -- simpler: the two wing calls above created centred blocks; move them now
for o in list(bpy.data.objects):
    if o.name.startswith("Wing"):
        pass  # handled by name-based shift below
# shift wing parts sideways
for sx, tag in ((-1, "Wing-1"), (1, "Wing1")):
    for o in bpy.data.objects:
        if o.name.startswith(tag):
            o.location.x += sx * 0.50
# transept front: an arch-topped GLAZED panel flush in the facade (dark
# backing + pale glass rectangle and semicircle of the same glass, so the
# pair reads as one arch), frame ring, glazing bars, dark door. The barrel
# vault starts behind the facade so its end cap never shows as a disc.
cyl("TranseptVault", (0, 0.045, BASE_Z + 0.30), 0.14, 0.25, GLASSM, 20, rot=(math.radians(90), 0, 0))
box("TranseptBack", (0, -0.152, BASE_Z + 0.080), (0.29, 0.008, 0.16), DARKIN)
cyl("TranseptBackTop", (0, -0.152, BASE_Z + 0.16), 0.145, 0.008, DARKIN, 20, rot=(math.radians(90), 0, 0))
box("TranseptGlass", (0, -0.158, BASE_Z + 0.080), (0.27, 0.006, 0.16), GLASSM)
cyl("TranseptGlassTop", (0, -0.158, BASE_Z + 0.16), 0.135, 0.006, GLASSM, 20, rot=(math.radians(90), 0, 0))
torus("TranseptArch", (0, -0.160, BASE_Z + 0.16), 0.140, 0.012, FRAME)
for i, mx in enumerate((-0.07, 0.0, 0.07)):
    box(f"TranseptMull_{i}", (mx, -0.162, BASE_Z + 0.10), (0.011, 0.005, 0.20), FRAME)
box("TranseptTransom", (0, -0.162, BASE_Z + 0.16), (0.26, 0.005, 0.011), FRAME)
box("TranseptDoor", (0, -0.162, BASE_Z + 0.05), (0.09, 0.005, 0.10), DARKIN)
# nave ridge behind the transept
box("NaveRidge", (0, 0.02, BASE_Z + 0.335), (0.24, 0.36, 0.03), FRAME)

# ---- Tier 1: broad multi-storey block ----
banded_block("Tier1", BASE_Z + 0.30, 1.28, 0.56, 0.27, 0.115, mat_body=STONE, mullions=6)
# corner turrets on Tier 1's top, flanking Tier 2
for sx in (-1, 1):
    box(f"Turret_{sx}", (sx * 0.235, 0, 1.38), (0.095, 0.095, 0.20), STONE)
    frustum(f"TurretCap_{sx}", (sx * 0.235, 0, 1.525), 0.075, 0.006, 0.09, STONE_D, 4, rot=(0, 0, math.radians(45)))
    sphere(f"TurretFinial_{sx}", (sx * 0.235, 0, 1.575), 0.012, STONE_D)

# ---- Tier 2: mid tower with the great circular window ----
banded_block("Tier2", 1.28, 1.80, 0.37, 0.22, 0.105, mat_body=STONE, mullions=4)
torus("Oculus", (0, -0.118, 1.56), 0.072, 0.011, FRAME)
cyl("OculusGlass", (0, -0.112, 1.56), 0.066, 0.008, DARKIN, 22, rot=(math.radians(90), 0, 0))
box("OculusCrossV", (0, -0.120, 1.56), (0.010, 0.006, 0.125), FRAME)
box("OculusCrossH", (0, -0.120, 1.56), (0.125, 0.006, 0.010), FRAME)

# ---- Tier 3: the long slim shaft, six slightly stepping segments ----
z = 1.80
for i in range(6):
    seg_h = 0.175
    w = 0.26 - i * 0.011
    dpt = 0.185 - i * 0.007
    banded_block(f"Shaft{i}", z, z + seg_h, w, dpt, seg_h, mat_body=STONE, mullions=4)
    z += seg_h
SHAFT_TOP = z  # 2.85

# ---- crown: cap block, lantern, flag ----
banded_block("Cap", SHAFT_TOP, 2.96, 0.235, 0.165, 0.11, mat_body=STONE, mullions=3)
box("Lantern", (0, 0, 3.004), (0.125, 0.105, 0.088), STONE)
box("LanternRoof", (0, 0, 3.052), (0.15, 0.13, 0.012), STONE_D)
cyl("FlagPole", (0, 0, 3.10), 0.004, 0.11, FIGD, 8)
box("Flag", (0.035, 0, 3.135), (0.062, 0.004, 0.036), RED)

# ---- two blank annotation boards on easels, front corners of the base ----
def annotation_board(name, cx, ry):
    parts = []
    parts.append(box(f"{name}_back", (0, 0, 0), (0.36, 0.02, 0.28), WOOD_D))
    parts.append(box(f"{name}_paper", (0, -0.013, 0), (0.32, 0.006, 0.24), PAPER))
    parts.append(box(f"{name}_rule", (0, -0.017, 0.085), (0.26, 0.004, 0.012), STONE_D))
    for i in range(3):
        parts.append(box(f"{name}_line{i}", (0, -0.017, 0.03 - i * 0.045), (0.24, 0.004, 0.010), STONE_D))
    tilt = Matrix.Rotation(math.radians(-14), 4, 'X')  # board leans back on its easel
    M = Matrix.Translation(Vector((cx, -0.62, 0.30))) @ Matrix.Rotation(ry, 4, 'Z') @ tilt
    for o in parts:
        o.matrix_world = M @ o.matrix_world
    strut(f"{name}_legL", (cx - 0.13, -0.60, 0.44), (cx - 0.16, -0.52, 0.10), 0.011, WOOD_D)
    strut(f"{name}_legR", (cx + 0.13, -0.60, 0.44), (cx + 0.16, -0.52, 0.10), 0.011, WOOD_D)
    strut(f"{name}_legB", (cx, -0.60, 0.42), (cx, -0.72, 0.10), 0.011, WOOD_D)

annotation_board("BoardL", -0.78, math.radians(10))
annotation_board("BoardR", 0.78, math.radians(-10))

lights_and_camera((2.4, -4.6, 1.35), (0, 0, 1.42), lens=42, res=(760, 1024))
finish(SLUG, OUT)
