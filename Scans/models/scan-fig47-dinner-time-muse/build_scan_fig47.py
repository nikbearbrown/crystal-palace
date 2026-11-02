# Build script — scan-fig47-dinner-time (Muse version)
# Reference: fig-47_dinner-time-crystal-palace-punch-1851.png (Punch, 5 July 1851)
# Working families eating around the base of a standing Shakespeare statue whose
# plinth bears the motto "One touch of nature makes the whole world kin".
# Composition followed WITHOUT the cartoon's caricature exaggeration.
# Statue abstracted (blank detail); sculptor pass deferred. Inscription tablet left blank.
import bpy, math, os

OUT = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig47-dinner-time"

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

def mat(name, rgb, rough=0.9):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Roughness"].default_value = rough
    return m

STONE  = mat("Stone", (0.58, 0.56, 0.52))
PLINTH = mat("PlinthDark", (0.30, 0.29, 0.28))
TABLET = mat("Tablet", (0.78, 0.76, 0.70))
FLOOR  = mat("Floor", (0.60, 0.57, 0.52))
COATS = [mat("CoatA", (0.35, 0.29, 0.23)), mat("CoatB", (0.24, 0.21, 0.19)), mat("Smock", (0.60, 0.56, 0.48))]
DRESS = [mat("DressA", (0.40, 0.29, 0.27)), mat("DressB", (0.29, 0.33, 0.39)), mat("DressC", (0.46, 0.41, 0.33))]
SKIN   = mat("Skin", (0.80, 0.62, 0.50))
DARK   = mat("Dark", (0.16, 0.15, 0.14))
WOOD   = mat("Wood", (0.45, 0.34, 0.22))
CLOTH  = mat("ClothWhite", (0.82, 0.80, 0.74))

def box(name, loc, dims, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.dimensions = dims
    bpy.ops.object.transform_apply(scale=True)
    if material: o.data.materials.append(material)
    return o

def cyl(name, loc, r1, r2, depth, material, verts=10, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2,
                                    depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    if material: o.data.materials.append(material)
    return o

def sph(name, loc, scale, material, seg=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=max(6, seg // 2), location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    if material: o.data.materials.append(material)
    for p in o.data.polygons: p.use_smooth = True
    return o

# ----- figures -----
def head_hat(x, y, hz, s, kind):
    sph("head", (x, y, hz), (0.082 * s, 0.086 * s, 0.10 * s), SKIN)
    if kind == "top":
        cyl("brim", (x, y, hz + 0.085 * s), 0.115 * s, 0.115 * s, 0.014, DARK, 12)
        cyl("tophat", (x, y, hz + 0.17 * s), 0.080 * s, 0.087 * s, 0.16 * s, DARK, 12)
    elif kind == "cap":
        sph("cap", (x, y, hz + 0.075 * s), (0.092 * s, 0.092 * s, 0.055 * s), COATS[1])
    elif kind == "bonnet":
        sph("bonnet", (x, y - 0.015 * s, hz + 0.03 * s), (0.096 * s, 0.10 * s, 0.088 * s), DRESS[0])
        cyl("bbrim", (x, y + 0.015 * s, hz + 0.015 * s), 0.105 * s, 0.105 * s, 0.012, DRESS[0], 12)

def man_standing(x, y, ry=0.0, h=1.72, coat=None, hat="cap"):
    coat = coat or COATS[0]; s = h / 1.72
    for dx in (-0.075, 0.075):
        box("leg", (x + dx * s, y, 0.40 * s), (0.085 * s, 0.09 * s, 0.80 * s), DARK, (0, 0, -ry))
    box("coat", (x, y, 1.10 * s), (0.40 * s, 0.24 * s, 0.62 * s), coat, (0, 0, -ry))
    for dx in (-0.245, 0.245):
        box("arm", (x + dx * s, y, 1.12 * s), (0.075 * s, 0.075 * s, 0.55 * s), coat, (0.05, 0, -ry))
    head_hat(x, y, 1.58 * s, s, hat)

def woman_seated(x, y, ry=0.0, dress=None, baby=False):
    dress = dress or DRESS[0]; s = 1.0
    cyl("skirt", (x, y, 0.26), 0.34, 0.20, 0.52, dress, 12)            # spread skirt on floor
    box("bodice", (x, y - 0.02, 0.72), (0.30, 0.20, 0.42), dress, (math.radians(-6), 0, -ry))
    sph("head", (x, y - 0.03, 1.06), (0.078, 0.082, 0.095), SKIN)
    sph("bonnet", (x, y - 0.055, 1.10), (0.095, 0.10, 0.085), dress)
    if baby:  # bundle held at chest
        sph("baby", (x + 0.08, y + 0.17, 0.78), (0.075, 0.125, 0.065), CLOTH)
        box("armL", (x - 0.16, y + 0.10, 0.74), (0.06, 0.06, 0.34), dress, (math.radians(65), 0, 0))
        box("armR", (x + 0.17, y + 0.10, 0.74), (0.06, 0.06, 0.34), dress, (math.radians(65), 0, 0))
    else:
        for dx in (-0.20, 0.20):
            box("arm", (x + dx, y + 0.03, 0.68), (0.06, 0.06, 0.42), dress, (math.radians(28), 0, -ry))

def child_standing(x, y, h=1.0, dress=None):
    dress = dress or DRESS[2]; s = h / 1.0
    cyl("cskirt", (x, y, 0.30 * s), 0.20 * s, 0.13 * s, 0.60 * s, dress, 10)
    box("cbod", (x, y, 0.72 * s), (0.22 * s, 0.15 * s, 0.26 * s), dress)
    sph("chead", (x, y, 0.93 * s), (0.070 * s, 0.073 * s, 0.082 * s), SKIN)
    sph("cbonnet", (x, y - 0.01, 0.97 * s), (0.082 * s, 0.085 * s, 0.07 * s), dress)

def basket(x, y, z=0.0):
    cyl("basket", (x, y, z + 0.11), 0.17, 0.12, 0.22, WOOD, 10)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.15, minor_radius=0.016,
                                     major_segments=12, minor_segments=6,
                                     location=(x, y, z + 0.24), rotation=(0, 0, 0))
    o = bpy.context.object; o.name = "basketHandle"; o.scale = (1, 1, 0.9)
    o.data.materials.append(WOOD)

# ----- ground -----
box("Floor", (0, 0, -0.03), (7.6, 4.6, 0.06), FLOOR)

# ----- plinth (centre, tall, dark, stepped) -----
box("PlinthBase", (0, -0.55, 0.30), (2.0, 1.3, 0.60), PLINTH)
box("PlinthMid", (0, -0.55, 0.85), (1.7, 1.1, 0.50), PLINTH)
box("PlinthTop", (0, -0.55, 1.30), (1.45, 0.95, 0.40), PLINTH)
box("Tablet", (0, 0.03, 0.85), (1.15, 0.05, 0.42), TABLET)   # motto tablet — left BLANK

# ----- Shakespeare statue (abstracted standing figure, ~2.3 m) -----
SZ = 1.50; SX, SY = 0, -0.55
# legs: one crossed in front of the other, as drawn
box("SLegA", (SX - 0.13, SY, SZ + 0.42), (0.17, 0.19, 0.84), STONE)
box("SLegB", (SX + 0.10, SY + 0.10, SZ + 0.40), (0.17, 0.19, 0.82), STONE, (math.radians(-8), math.radians(10), 0))
box("STrunk", (SX, SY, SZ + 1.13), (0.46, 0.28, 0.62), STONE)      # doublet
box("SSkirt", (SX, SY, SZ + 0.86), (0.50, 0.30, 0.14), STONE)      # trunk-hose band
box("SArmL", (SX - 0.30, SY, SZ + 1.08), (0.10, 0.11, 0.62), STONE, (math.radians(-14), 0, 0))
box("SArmR", (SX + 0.31, SY + 0.02, SZ + 1.05), (0.10, 0.11, 0.55), STONE, (math.radians(10), 0, 0))
sph("SHead", (SX, SY, SZ + 1.60), (0.115, 0.12, 0.14), STONE)      # bald dome, no features
box("SCollar", (SX, SY, SZ + 1.45), (0.36, 0.27, 0.08), STONE)     # collar/ruff suggestion
box("SBookPost", (SX - 0.48, SY, SZ + 0.45), (0.22, 0.30, 0.90), STONE)  # support post at his left
box("SBook", (SX - 0.48, SY, SZ + 0.95), (0.30, 0.24, 0.09), STONE)      # book/scroll block on post
cyl("SLaurel", (SX - 0.42, SY - 0.18, SZ + 0.25), 0.03, 0.045, 0.5, STONE, 6)  # laurel spray hint

# ----- families around the base -----
# left: standing man pouring from a bottle (top hat), woman reclining on plinth step, girl seated
man_standing(-2.35, 0.15, 0.35, 1.78, COATS[1], "top")
box("BottleArm", (-2.02, 0.38, 1.28), (0.07, 0.07, 0.42), COATS[1], (math.radians(70), 0, 0))
cyl("Bottle", (-1.94, 0.55, 1.18), 0.035, 0.045, 0.24, DARK, 8, (math.radians(115), 0, 0))
cyl("ReclineSkirt", (-1.55, 0.28, 0.20), 0.42, 0.24, 0.40, DRESS[1], 12, (0, math.radians(18), 0))
box("ReclineBod", (-1.72, 0.05, 0.55), (0.30, 0.20, 0.40), DRESS[1], (math.radians(-32), 0, 0))
sph("ReclineHead", (-1.80, -0.02, 0.82), (0.078, 0.082, 0.095), SKIN)
sph("ReclineBonnet", (-1.83, -0.05, 0.86), (0.095, 0.10, 0.085), DRESS[1])
child_standing(-1.15, 0.55, 0.95, DRESS[2])
basket(-1.95, 0.85)
# centre: mother nursing baby, basket at her side
woman_seated(-0.55, 0.55, 0.0, DRESS[0], baby=True)
basket(-0.05, 0.95)
# centre-right: small boy standing with back three-quarter, older woman seated with basket
man_standing(0.55, 0.62, 3.0, 1.02, COATS[0], "cap")   # small boy (back view)
woman_seated(1.35, 0.45, -0.2, DRESS[1])
child_standing(1.95, 0.70, 1.12, DRESS[0])
basket(1.75, 1.05)
# right: woman seated on floor with cloth/bundle
woman_seated(2.60, 0.30, -0.3, DRESS[2])
sph("BundleCloth", (2.30, 0.80, 0.12), (0.22, 0.18, 0.12), CLOTH)

# ----- background crowd silhouettes (heads & shoulders masses) -----
for i, (bx, by) in enumerate([(-3.1, -0.9), (-2.6, -1.1), (-2.1, -0.95), (2.2, -1.0),
                              (2.7, -0.85), (3.15, -1.05), (-3.35, -0.55), (3.45, -0.6)]):
    h = 1.66 + (i % 3) * 0.06
    if i % 2 == 0:
        man_standing(bx, by, 0.0, h, COATS[i % 3], "top" if i % 4 == 0 else "cap")
    else:
        cyl("bgSkirt", (bx, by, 0.42), 0.30, 0.17, 0.84, DRESS[i % 3], 10)
        box("bgBod", (bx, by, 1.02), (0.30, 0.20, 0.36), DRESS[i % 3])
        sph("bgHead", (bx, by, 1.36), (0.078, 0.082, 0.095), SKIN)
        sph("bgBonnet", (bx, by - 0.015, 1.40), (0.095, 0.10, 0.085), DRESS[i % 3])

# ----- camera / light / render (portrait-ish, comparable to the print) -----
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.use_denoising = True
scene.render.resolution_x = 760; scene.render.resolution_y = 960
scene.render.filepath = os.path.join(OUT, "preview.png")
world = bpy.data.worlds.new("W"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.9
bpy.ops.object.light_add(type='SUN', location=(4, 6, 9))
sun = bpy.context.object; sun.data.energy = 3.0; sun.rotation_euler = (math.radians(50), 0, math.radians(35))
bpy.ops.object.camera_add(location=(0.2, 7.8, 2.7))
cam = bpy.context.object; scene.camera = cam
cam.rotation_euler = (math.radians(82), 0, math.radians(180))
cam.data.lens = 37

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, SLUG + ".blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, SLUG + ".glb"), export_format='GLB')
bpy.ops.render.render(write_still=True)

dg = bpy.context.evaluated_depsgraph_get()
tris = 0
for ob in scene.objects:
    if ob.type == 'MESH':
        ev = ob.evaluated_get(dg); me = ev.to_mesh()
        me.calc_loop_triangles(); tris += len(me.loop_triangles)
        ev.to_mesh_clear()
print("TOTAL_TRIS", tris)
