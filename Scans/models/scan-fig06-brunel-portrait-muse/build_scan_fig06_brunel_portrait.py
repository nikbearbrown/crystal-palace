# Build script: scan-fig06-brunel-portrait
# Stylised figure of Brunel (after Howlett 1857) before the Great Eastern
# launching chains. Mannequin-like figure, NO facial features / likeness.
# Re-runnable: blender -b --python build_scan_fig06_brunel_portrait.py
import bpy, math, os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig06-brunel-portrait"

# ---------- scene reset ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
model_col = bpy.data.collections.new("Model")
bpy.context.scene.collection.children.link(model_col)
setup_col = bpy.data.collections.new("RenderSetup")
bpy.context.scene.collection.children.link(setup_col)

def mat(name, rgb, rough=0.85, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m

COAT   = mat("CoatCharcoal", (0.055, 0.05, 0.048))
WAIST  = mat("Waistcoat", (0.16, 0.14, 0.125))
TROUS  = mat("Trousers", (0.09, 0.085, 0.08))
SHIRT  = mat("ShirtWhite", (0.82, 0.8, 0.76))
SKIN   = mat("SkinTone", (0.62, 0.45, 0.34))
HAIR   = mat("HairDark", (0.05, 0.04, 0.035))
HAT    = mat("HatBlack", (0.03, 0.03, 0.03), 0.6)
SHOE   = mat("ShoeBrown", (0.12, 0.08, 0.05), 0.6)
IRON   = mat("ChainIron", (0.13, 0.13, 0.135), 0.55, 0.65)
GOLD   = mat("WatchChain", (0.45, 0.32, 0.1), 0.35, 0.8)
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

def lathe(name, profile, material, segments=24, centre=(0, 0, 0)):
    """profile: list of (radius, z). Lathed around Z, then moved to centre."""
    verts, faces = [], []
    n = len(profile)
    for i, (r, z) in enumerate(profile):
        for j in range(segments):
            a = 2 * math.pi * j / segments
            verts.append((r * math.cos(a), r * math.sin(a), z))
    for i in range(n - 1):
        for j in range(segments):
            j2 = (j + 1) % segments
            faces.append((i * segments + j, i * segments + j2,
                          (i + 1) * segments + j2, (i + 1) * segments + j))
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

# ================= FIGURE (height ~1.70 m incl. hat) =================
# legs (trousers): slight stance, feet apart
tube("LegL", (-0.09, 0, 0.10), (-0.10, 0, 0.82), 0.062, TROUS)
tube("LegR", (0.11, 0.02, 0.10), (0.09, 0, 0.82), 0.062, TROUS)
# shoes
ball("ShoeL", (-0.10, 0.07, 0.045), (0.055, 0.14, 0.04), SHOE)
ball("ShoeR", (0.115, 0.09, 0.045), (0.055, 0.14, 0.04), SHOE)
# frock coat torso + skirt flare
lathe("Coat", [(0.001, 0.78), (0.155, 0.80), (0.165, 0.95), (0.150, 1.12),
               (0.158, 1.28), (0.175, 1.42), (0.150, 1.50), (0.001, 1.52)], COAT)
# coat tails behind
box("CoatTail", (0, -0.155, 1.02), (0.24, 0.05, 0.52), COAT, rot=(math.radians(6), 0, 0))
# waistcoat front (flattened proud panel) + shirt triangle
ball("Waistcoat", (0, 0.095, 1.215), (0.105, 0.058, 0.175), WAIST)
ball("Shirt", (0, 0.118, 1.435), (0.048, 0.034, 0.058), SHIRT)
# waistcoat buttons + watch chain (shallow V of fine tube) + fob
for i, z in enumerate((1.30, 1.20, 1.10)):
    ball(f"Button{i}", (0, 0.152, z), (0.011, 0.008, 0.011), HAT, seg=8)
tube("WatchChainL", (-0.075, 0.148, 1.19), (0.0, 0.158, 1.115), 0.0045, GOLD, seg=6)
tube("WatchChainR", (0.0, 0.158, 1.115), (0.075, 0.148, 1.19), 0.0045, GOLD, seg=6)
ball("WatchFob", (0, 0.16, 1.085), (0.013, 0.007, 0.018), GOLD, seg=8)
# cravat
ball("Cravat", (0, 0.10, 1.485), (0.055, 0.04, 0.03), HAT)
# arms: hands in pockets — upper arm down, forearm angled in to hips
ball("ShoulderL", (-0.163, 0, 1.435), (0.062, 0.058, 0.062), COAT)
ball("ShoulderR", (0.163, 0, 1.435), (0.062, 0.058, 0.062), COAT)
tube("ArmLU", (-0.175, 0, 1.42), (-0.205, 0.02, 1.13), 0.048, COAT)
tube("ArmLF", (-0.205, 0.02, 1.13), (-0.115, 0.06, 0.94), 0.040, COAT)
tube("ArmRU", (0.175, 0, 1.42), (0.21, 0.02, 1.13), 0.048, COAT)
tube("ArmRF", (0.21, 0.02, 1.13), (0.12, 0.06, 0.94), 0.040, COAT)
ball("CuffL", (-0.14, 0.05, 0.97), (0.035, 0.03, 0.045), SHIRT)
ball("CuffR", (0.145, 0.05, 0.97), (0.035, 0.03, 0.045), SHIRT)
# head (featureless) + hair mass at back/sides
ball("Head", (0, 0, 1.615), (0.088, 0.082, 0.105), SKIN)
ball("Hair", (0, -0.028, 1.63), (0.092, 0.082, 0.10), HAIR)
ball("FaceMask", (0, 0.018, 1.612), (0.086, 0.080, 0.103), SKIN)  # keeps front clean skin
# cigar (tiny, at mouth height, angled) — pose detail from the photograph
tube("Cigar", (0.028, 0.072, 1.575), (0.068, 0.112, 1.568), 0.0055, SHIRT, seg=6)
# stovepipe hat ON head
lathe("HatBrim", [(0.001, 1.685), (0.16, 1.685), (0.165, 1.695), (0.115, 1.70),
                  (0.112, 1.955), (0.118, 1.96), (0.001, 1.965)], HAT)

# ================= CHAIN WALL (backdrop) =================
# One stud-link built in LOCAL space: elongated oval ring in the XZ plane
# (vertical, facing +/-Y), ~0.30 m wide x 0.56 m long, cross stud along X.
def make_link(name):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.19, minor_radius=0.048,
                                     major_segments=16, minor_segments=8,
                                     location=(0, 0, 0))
    ob = bpy.context.active_object
    ob.name = name
    # torus ring starts in XY (local); oval it in local axes (x squash,
    # y stretch = the ring's length once stood up), then rotate X 90 so
    # the ring stands in the XZ plane. Bake BOTH rotation and scale.
    ob.scale = (0.75, 1.25, 1.0)
    ob.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    ob.data.materials.append(IRON)
    for p in ob.data.polygons:
        p.use_smooth = True
    link(ob)
    tube(name + "Stud", (-0.115, 0, 0), (0.115, 0, 0), 0.038, IRON, seg=8)
    return ob

proto = make_link("ChainLinkProto")
proto_stud = bpy.data.objects["ChainLinkProtoStud"]
# hanging chains: 9 columns x 8 links; alternate links twist 90 deg about Z
# (vertical axis) so the wall reads as interlocked stud-link chain.
for c in range(9):
    x = -1.45 + c * 0.36
    for r in range(8):
        z = 0.30 + r * 0.435
        twist = (r % 2 == 1)
        if c == 0 and r == 0:
            ob, so = proto, proto_stud
        else:
            ob = proto.copy(); ob.data = proto.data; link(ob)
            so = proto_stud.copy(); so.data = proto_stud.data; link(so)
        ob.location = (x, -0.55, z)
        ob.rotation_euler = (0, 0, math.radians(90) if twist else 0)
        so.location = (x, -0.55, z)
        so.rotation_euler = (0, 0, math.radians(90) if twist else 0)

# a couple of loose links lying at the base
for i, (x, rz) in enumerate(((-1.15, 15), (1.30, 70))):
    ob = proto.copy(); ob.data = proto.data; link(ob)
    ob.location = (x, -0.42, 0.055)
    ob.rotation_euler = (math.radians(90), 0, math.radians(rz))

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
cam.location = (0.55, 3.1, 1.35)
_target = Vector((0, -0.1, 1.05))
cam.rotation_quaternion = (_target - cam.location).to_track_quat('-Z', 'Y')
cam.rotation_mode = 'XYZ'
cam.rotation_euler = cam.rotation_quaternion.to_euler()
cam_data.lens = 55
bpy.context.scene.camera = cam

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 48
sc.cycles.device = 'CPU'
sc.render.resolution_x = 768
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
