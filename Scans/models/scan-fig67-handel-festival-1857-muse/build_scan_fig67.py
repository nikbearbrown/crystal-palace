# Build script — scan-fig67-handel-festival-1857 (Muse version)
# Reference: fig-67_handel-festival-sydenham-crystal-palace-1857.png (ILN, 27 June 1857)
# The Great Handel Festival in the Sydenham transept: organ front centre-rear,
# massed choir on raked tiers, orchestra + conductor on the front platform,
# audience blocks in the foreground, iron galleries and draped swags above.
# Performers/audience are instanced stylised silhouettes — no likenesses.
import bpy, math, os, random

OUT = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig67-handel-festival-1857"
random.seed(67)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

def mat(name, rgb, rough=0.85, metallic=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    return m

FLOOR  = mat("Floor", (0.60, 0.56, 0.51))
STAGE  = mat("StageWood", (0.45, 0.36, 0.26))
DRAPE  = mat("Drape", (0.42, 0.38, 0.34))
GOLD   = mat("GiltPipe", (0.74, 0.58, 0.26), 0.4, 0.6)
CASE   = mat("OrganCase", (0.35, 0.26, 0.18))
IRON   = mat("IronFrame", (0.30, 0.32, 0.34))
CHOIRW = mat("ChoirWhite", (0.80, 0.78, 0.74))
DARK   = mat("Dark", (0.17, 0.16, 0.15))
SKIN   = mat("Skin", (0.80, 0.62, 0.50))
COATS = [mat("CoatA", (0.30, 0.25, 0.21)), mat("CoatB", (0.23, 0.21, 0.22)), mat("CoatC", (0.38, 0.31, 0.23))]
DRESS = [mat("DressA", (0.48, 0.36, 0.38)), mat("DressB", (0.34, 0.38, 0.48)), mat("DressC", (0.52, 0.45, 0.33))]
LEAF   = mat("Leaf", (0.32, 0.42, 0.26))
BARK   = mat("Bark", (0.36, 0.29, 0.21))

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

def sph(name, loc, scale, material, seg=10):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=max(5, seg // 2), location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    if material: o.data.materials.append(material)
    for p in o.data.polygons: p.use_smooth = True
    return o

# ----- figure prototypes (joined meshes, placed as linked duplicates) -----
def _join_parts(parts, name, material):
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts: p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.join()
    o = bpy.context.object; o.name = name; o.hide_render = True
    o.data.materials.append(material)
    return o

def _cube(parts, loc, dims):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object; o.dimensions = dims; parts.append(o)

def _sph(parts, loc, scale):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=5, location=loc)
    o = bpy.context.object; o.scale = scale; parts.append(o)

def _cone(parts, loc, r1, r2, d, verts=10):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=d, location=loc)
    parts.append(bpy.context.object)

def proto_standing(material, name):
    p = []
    _cube(p, (-0.075, 0, 0.40), (0.085, 0.09, 0.80)); _cube(p, (0.075, 0, 0.40), (0.085, 0.09, 0.80))
    _cube(p, (0, 0, 1.10), (0.40, 0.24, 0.62))
    _cube(p, (-0.245, 0, 1.12), (0.075, 0.075, 0.55)); _cube(p, (0.245, 0, 1.12), (0.075, 0.075, 0.55))
    _sph(p, (0, 0, 1.585), (0.082, 0.086, 0.10))
    return _join_parts(p, name, material)

def proto_woman(material, name):
    p = []
    _cone(p, (0, 0, 0.43), 0.33, 0.15, 0.86, 10)
    _cube(p, (0, 0, 1.04), (0.30, 0.20, 0.36))
    _sph(p, (0, 0, 1.345), (0.078, 0.082, 0.095))
    return _join_parts(p, name, material)

def proto_seated(material, name):
    p = []
    _cube(p, (0, 0.06, 0.26), (0.38, 0.30, 0.52))      # seated lower mass
    _cube(p, (0, -0.03, 0.72), (0.36, 0.22, 0.48))     # torso
    _sph(p, (0, -0.03, 1.10), (0.080, 0.084, 0.098))   # head
    _cube(p, (-0.24, 0.05, 0.68), (0.07, 0.07, 0.42)); _cube(p, (0.24, 0.05, 0.68), (0.07, 0.07, 0.42))
    return _join_parts(p, name, material)

PM = proto_standing(COATS[0], "ProtoMan")
PW = proto_woman(DRESS[0], "ProtoWoman")
PS = proto_seated(COATS[1], "ProtoSeated")
PSW = proto_seated(DRESS[1], "ProtoSeatedWoman")

def place(proto, x, y, z=0.0, ry=0.0, hs=1.0):
    o = proto.copy(); o.data = proto.data
    o.location = (x, y, z); o.rotation_euler = (0, 0, ry); o.scale = (hs, hs, hs)
    o.hide_render = False
    bpy.context.collection.objects.link(o)
    return o

# ----- floor -----
box("Floor", (0, 0, -0.03), (20.0, 15.0, 0.06), FLOOR)

# ----- organ front (centre rear) -----
OY = -6.2
box("OrganCase", (0, OY, 3.1), (6.4, 0.7, 6.2), CASE)
# three pipe towers: tall-centre arrangement as drawn (towers + flats of gilt pipes)
tower_x = [-2.35, 0.0, 2.35]
for tx in tower_x:
    cyl("TowerBase", (tx, OY + 0.45, 1.05), 0.62, 0.68, 2.1, CASE, 12)
    n = 5
    for i in range(n):
        px = tx - 0.36 + i * 0.18
        ph = 3.6 - abs(i - 2) * 0.35
        cyl("Pipe", (px, OY + 0.48, 2.1 + ph / 2), 0.062, 0.062, ph, GOLD, 8)
    sph("TowerCap", (tx, OY + 0.45, 6.05), (0.55, 0.30, 0.22), CASE)
for fx in (-1.18, 1.18):  # flats between towers
    for i in range(4):
        px = fx - 0.27 + i * 0.18
        cyl("FlatPipe", (px, OY + 0.48, 2.1 + 1.35), 0.058, 0.058, 2.7, GOLD, 8)
box("OrganGallery", (0, OY + 0.75, 0.55), (7.4, 1.4, 1.1), CASE)
# scallop shell motif over centre tower
sph("ShellMotif", (0, OY + 0.55, 6.45), (0.55, 0.18, 0.30), GOLD)

# ----- choir tiers (raked, both sides + centre below organ) -----
def tier_bank(x0, x1, rows=5):
    for r in range(rows):
        y = -4.9 + r * 0.78
        z = 0.35 + r * 0.42
        box("Tier", ( (x0 + x1) / 2, y, z - 0.21), (x1 - x0, 0.80, 0.42), STAGE)
        n = int((x1 - x0) / 0.52)
        for i in range(n):
            x = x0 + 0.3 + i * 0.52 + random.uniform(-0.05, 0.05)
            proto = PW if (i + r) % 3 else PM
            place(proto, x, y + 0.1, z, math.pi + random.uniform(-0.12, 0.12), random.uniform(0.95, 1.02))
tier_bank(-8.6, -1.6)
tier_bank(1.6, 8.6)
tier_bank(-1.5, 1.5, rows=3)   # centre block below organ

# ----- orchestra platform (front centre) -----
box("OrchPlatform", (0, -0.9, 0.30), (10.5, 3.4, 0.60), STAGE)
box("OrchFront", (0, 0.86, 0.45), (10.5, 0.08, 0.90), DRAPE)   # draped front
# seated orchestra with music desks, two arcs
for row, (ry_, n, rad) in enumerate([(0, 13, 0.0), (1, 15, 0.0)]):
    y = -1.9 + row * 1.05
    for i in range(n):
        x = -4.4 + i * (8.8 / max(1, n - 1))
        place(PS if i % 2 else PSW, x, y, 0.60, math.pi, 0.98)
        box("Desk", (x, y + 0.42, 1.05), (0.42, 0.03, 0.30), DARK, (math.radians(-32), 0, 0))
# conductor on podium, centre, arms raised
box("Podium", (0, -0.55, 0.78), (0.55, 0.55, 0.36), STAGE)
place(PM, 0, -0.55, 0.96, math.pi, 1.03)
box("CondArmL", (-0.30, -0.42, 2.30), (0.07, 0.07, 0.55), COATS[0], (0, math.radians(48), 0))
box("CondArmR", (0.30, -0.42, 2.30), (0.07, 0.07, 0.55), COATS[0], (0, math.radians(-48), 0))
cyl("Baton", (0.48, -0.30, 2.62), 0.008, 0.008, 0.35, CHOIRW, 6, (math.radians(70), 0, 0))
# soloists standing front of platform
for sx in (-1.6, -0.8, 0.9, 1.7):
    place(PW if sx < 0 else PM, sx, 0.35, 0.60, math.pi, 1.0)

# ----- side galleries (iron frame hints, left & right) -----
for side in (-1, 1):
    gx = side * 9.3
    for gz in (0, 1):
        pass
    for i in range(4):
        cyl("GalCol", (gx, -5.5 + i * 3.4, 3.4), 0.07, 0.09, 6.8, IRON, 8)
    box("GalDeck", (gx, -0.4, 5.1), (1.4, 13.6, 0.18), IRON)
    box("GalRail", (gx - side * 0.65, -0.4, 5.85), (0.05, 13.6, 0.09), IRON)

# ----- draped swags overhead -----
for sx in (-4.4, 4.4):
    bpy.ops.mesh.primitive_torus_add(major_radius=3.4, minor_radius=0.16, major_segments=20,
                                     minor_segments=6, location=(sx, -3.4, 10.6),
                                     rotation=(math.radians(90), 0, 0))
    sw = bpy.context.object; sw.name = "Swag"
    import bmesh
    bm = bmesh.new(); bm.from_mesh(sw.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > 0], context='VERTS')
    bm.to_mesh(sw.data); bm.free()
    sw.scale = (1, 1, 0.5); bpy.ops.object.transform_apply(scale=True)
    sw.data.materials.append(DRAPE)

# ----- potted trees at the sides (as in the engraving) -----
for tx in (-8.3, -6.9, 7.0, 8.4):
    cyl("Pot", (tx, 1.6, 0.25), 0.26, 0.20, 0.5, CASE, 10)
    cyl("Trunk", (tx, 1.6, 0.85), 0.05, 0.07, 0.8, BARK, 8)
    sph("TreeTop", (tx, 1.6, 1.75), (0.55, 0.55, 0.65), LEAF)

# ----- audience blocks (foreground, seated, with aisles) -----
for block, (ax0, ax1) in enumerate([(-8.8, -2.2), (-1.7, 1.7), (2.2, 8.8)]):
    for row in range(6):
        y = 2.6 + row * 0.85
        n = int((ax1 - ax0) / 0.58)
        for i in range(n):
            x = ax0 + 0.35 + i * 0.58 + random.uniform(-0.05, 0.05)
            proto = PSW if (i + row + block) % 2 else PS
            place(proto, x, y, 0.0, math.pi + random.uniform(-0.1, 0.1), random.uniform(0.94, 1.02))
# aisle standees at back
for i in range(7):
    place(PM, -6.5 + i * 2.1, 8.3, 0.0, math.pi, 1.05)

# ----- camera / light / render -----
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.use_denoising = True
scene.render.resolution_x = 960; scene.render.resolution_y = 680
scene.render.filepath = os.path.join(OUT, "preview.png")
world = bpy.data.worlds.new("W"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.9
bpy.ops.object.light_add(type='SUN', location=(6, 8, 12))
sun = bpy.context.object; sun.data.energy = 3.0; sun.rotation_euler = (math.radians(46), 0, math.radians(28))
bpy.ops.object.camera_add(location=(0.0, 14.6, 5.8))
cam = bpy.context.object; scene.camera = cam
cam.rotation_euler = (math.radians(74), 0, math.radians(180))
cam.data.lens = 31

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
