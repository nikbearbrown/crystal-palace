# Build script: scan-fig43-mary-callinack
# Stylised seated figure of Mary Callinack (ILN, 25 Oct 1851): elderly woman
# in bonnet, checked shawl and apron, seated, hands clasped. NO facial
# features / likeness. The scan's repaired left-edge strip is NON-evidence;
# the dress outline there uses the plainest period interpretation.
# Re-runnable: blender -b --python build_scan_fig43_mary_callinack.py
import bpy, math, os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig43-mary-callinack"

bpy.ops.wm.read_factory_settings(use_empty=True)
model_col = bpy.data.collections.new("Model")
bpy.context.scene.collection.children.link(model_col)
setup_col = bpy.data.collections.new("RenderSetup")
bpy.context.scene.collection.children.link(setup_col)

def mat(name, rgb, rough=0.9, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m

DRESS  = mat("DressMidtone", (0.235, 0.215, 0.20))
APRON  = mat("ApronPale", (0.66, 0.63, 0.57))
SHAWL  = mat("ShawlCheckBase", (0.295, 0.235, 0.195))
SHAWLD = mat("ShawlCheckDark", (0.16, 0.14, 0.13))
BONNET = mat("BonnetDark", (0.07, 0.06, 0.055))
SKIN   = mat("SkinTone", (0.62, 0.45, 0.34))
HAIR   = mat("HairGrey", (0.55, 0.53, 0.5))
WOOD   = mat("ChairWood", (0.23, 0.15, 0.09), 0.7)
SHOE   = mat("ShoeDark", (0.08, 0.07, 0.06), 0.6)
GROUND = mat("GroundGrey", (0.32, 0.32, 0.32))

def link(obj, col=model_col):
    col.objects.link(obj)
    return obj

def finish(obj, material=None):
    if material:
        obj.data.materials.append(material)
    for p in obj.data.polygons:
        p.use_smooth = True
    return link(obj)

def lathe(name, profile, material, segments=26, centre=(0, 0, 0), squash_y=1.0,
          a0=0.0, a1=None):
    if a1 is None:
        a1 = 2 * math.pi
    closed = abs((a1 - a0) - 2 * math.pi) < 1e-6
    steps = segments if closed else segments
    verts, faces = [], []
    n = len(profile)
    for i, (r, z) in enumerate(profile):
        for j in range(steps + (0 if closed else 1)):
            a = a0 + (a1 - a0) * j / steps
            verts.append((r * math.cos(a), r * math.sin(a) * squash_y, z))
    cols = steps + (0 if closed else 1)
    for i in range(n - 1):
        for j in range(steps):
            j2 = (j + 1) % cols if closed else j + 1
            faces.append((i * cols + j, i * cols + j2,
                          (i + 1) * cols + j2, (i + 1) * cols + j))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.location = centre
    return finish(ob, material)

def ball(name, pos, scale, material, seg=20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2,
                                         location=pos)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(ob, material)

def tube(name, p1, p2, r, material, seg=12):
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    bpy.ops.mesh.primitive_cylinder_add(vertices=seg, radius=r, depth=d.length,
                                        location=(p1 + p2) / 2)
    ob = bpy.context.active_object
    ob.name = name
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return finish(ob, material)

def box(name, pos, size, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=pos)
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = size
    ob.rotation_euler = rot
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        ob.data.materials.append(material)
    return link(ob)

# ================= CHAIR (simple wooden side chair) =================
box("ChairSeat", (0, -0.03, 0.45), (0.46, 0.44, 0.04), WOOD)
for sx in (-1, 1):
    for sy in (-1, 1):
        tube(f"ChairLeg{sx}{sy}", (sx * 0.20, -0.03 + sy * 0.19, 0.0),
             (sx * 0.21, -0.03 + sy * 0.20, 0.45), 0.021, WOOD, seg=10)
# back posts + two rails (visible behind her right shoulder in the engraving)
tube("BackPostL", (-0.20, -0.235, 0.45), (-0.21, -0.25, 1.06), 0.022, WOOD, seg=10)
tube("BackPostR", (0.20, -0.235, 0.45), (0.21, -0.25, 1.06), 0.022, WOOD, seg=10)
box("BackRailTop", (0, -0.252, 1.02), (0.46, 0.03, 0.09), WOOD)
box("BackRailMid", (0, -0.247, 0.86), (0.44, 0.025, 0.06), WOOD)

# ================= FIGURE (seated, leaning forward) =================
# Skirt: broad bell from seat to floor, front-weighted (apron over dress)
lathe("Skirt", [(0.44, 0.01), (0.435, 0.10), (0.40, 0.28), (0.335, 0.46),
                (0.27, 0.60), (0.21, 0.70), (0.001, 0.74)], DRESS,
      centre=(0, 0.05, 0))
# apron: pale PARTIAL shell (front arc only), uniformly proud of the skirt
# so its edge is one clean curve, not a z-fighting patchwork
lathe("Apron", [(0.468, 0.03), (0.455, 0.16), (0.415, 0.36), (0.325, 0.55),
                (0.235, 0.66), (0.001, 0.70)], APRON,
      centre=(0, 0.05, 0), segments=30,
      a0=math.pi / 2 + 0.35 - 1.15, a1=math.pi / 2 + 0.35 + 1.15)
# torso leaning forward: bodice + shawl mass
lathe("Torso", [(0.001, 0.66), (0.20, 0.68), (0.215, 0.82), (0.185, 0.98),
                (0.150, 1.10), (0.105, 1.18), (0.001, 1.21)], SHAWL,
      centre=(0, 0.10, 0))
# shawl suggestion: ONE diagonal wrap band across the torso (the shawl's
# crossing edge), instead of hoop-like rings
bpy.ops.mesh.primitive_torus_add(major_radius=0.20, minor_radius=0.016,
                                 major_segments=26, minor_segments=8,
                                 location=(0, 0.10, 0.99),
                                 rotation=(math.radians(24), 0, math.radians(-14)))
tb = bpy.context.active_object
tb.name = "ShawlBand"
tb.scale = (1.0, 1.0, 1.35)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
finish(tb, SHAWLD)
# arms: sleeves down-forward, forearms crossed/clasped in the lap
tube("ArmLU", (-0.185, 0.12, 1.10), (-0.225, 0.16, 0.88), 0.055, SHAWL)
tube("ArmLF", (-0.225, 0.16, 0.88), (-0.03, 0.30, 0.74), 0.045, SHAWL)
tube("ArmRU", (0.185, 0.12, 1.10), (0.225, 0.16, 0.88), 0.055, SHAWL)
tube("ArmRF", (0.225, 0.16, 0.88), (0.045, 0.31, 0.755), 0.045, SHAWL)
ball("Hands", (0.005, 0.315, 0.745), (0.075, 0.05, 0.035), SKIN)
# neck + bowed head (featureless), tilted down/forward
tube("Neck", (0, 0.115, 1.16), (0, 0.215, 1.26), 0.048, SKIN, seg=10)
ball("Head", (0, 0.305, 1.26), (0.088, 0.084, 0.104), SKIN)
# white hair mass filling the bonnet opening around the face
ball("Hair", (0, 0.25, 1.272), (0.125, 0.105, 0.118), HAIR)
# bonnet: large dark shape — deep crown as a PARTIAL lathe (open at the
# front so the bowed face sits in the bonnet's opening, as in the
# engraving) + a wide saucer brim (lathe ring) framing the face
lathe("Bonnet", [(0.125, 1.215), (0.155, 1.30), (0.148, 1.39),
                 (0.10, 1.455), (0.001, 1.475)], BONNET,
      centre=(0, 0.19, 0), segments=30,
      a0=math.pi / 2 + 1.05, a1=math.pi / 2 - 1.05 + 2 * math.pi)
ball("BonnetCap", (0, 0.19, 1.398), (0.152, 0.152, 0.088), BONNET)
# interior plug: fills the crown shell behind the face/hair so no
# sightline reaches the shell's unlit inside
ball("BonnetPlug", (0, 0.16, 1.33), (0.145, 0.145, 0.135), BONNET)
lathe("BonnetBrim", [(0.120, 0.01), (0.165, -0.005), (0.215, -0.045),
                     (0.250, -0.115), (0.238, -0.128), (0.165, -0.070),
                     (0.122, -0.020)], BONNET,
      centre=(0, 0.20, 1.315))
# shoes peeking below the skirt front
ball("ShoeL", (-0.09, 0.465, 0.028), (0.042, 0.115, 0.028), SHOE)
ball("ShoeR", (0.07, 0.475, 0.028), (0.042, 0.115, 0.028), SHOE)

# ================= RENDER SETUP =================
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
g = bpy.context.active_object
g.name = "Ground"
g.data.materials.append(GROUND)
setup_col.objects.link(g)
bpy.context.scene.collection.objects.unlink(g)

world = bpy.data.worlds.new("W")
bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

def light(name, typ, loc, energy, size=4):
    ld = bpy.data.lights.new(name, typ)
    ld.energy = energy
    if typ == 'AREA':
        ld.shape = 'DISK'; ld.size = size
    ob = bpy.data.objects.new(name, ld)
    ob.location = loc
    setup_col.objects.link(ob)
    return ob

sun = light("Sun", 'SUN', (2.5, 3.5, 5), 3.0)
sun.rotation_euler = (math.radians(55), 0, math.radians(35))
light("Fill", 'AREA', (3.5, 4.5, 2.5), 500)

cam_data = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_data)
setup_col.objects.link(cam)
# three-quarter from her front-left, comparable to the engraving
cam.location = (1.45, 2.30, 1.12)
_target = Vector((0, 0.02, 0.66))
cam.rotation_quaternion = (_target - cam.location).to_track_quat('-Z', 'Y')
cam.rotation_mode = 'XYZ'
cam.rotation_euler = cam.rotation_quaternion.to_euler()
cam_data.lens = 50
bpy.context.scene.camera = cam

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 48
sc.cycles.device = 'CPU'
sc.render.resolution_x = 800
sc.render.resolution_y = 960
sc.render.filepath = os.path.join(HERE, "renders", "preview.png")
sc.view_settings.view_transform = 'Filmic'

# ================= EXPORT =================
tris = 0
for ob in model_col.objects:
    if ob.type == 'MESH':
        tris += sum(len(p.vertices) - 2 for p in ob.data.polygons)
print("TRIANGLES:", tris, "OBJECTS:", len(model_col.objects))

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, SLUG + ".blend"))
bpy.ops.object.select_all(action='DESELECT')
for ob in model_col.objects:
    ob.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, SLUG + ".glb"),
                          use_selection=True, export_apply=True)
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
