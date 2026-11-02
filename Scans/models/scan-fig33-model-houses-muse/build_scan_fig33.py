# scan-fig33-model-houses — Prince Albert's Model Houses for Four Families (Henry Roberts, 1851)
# Reference: fig-33_prince-albert-model-working-class-home-1851.png (ILN engraving, 14 June 1851)
import bpy, math, os
from mathutils import Vector

SLUG = "scan-fig33-model-houses"
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------- helpers ----------
def clean():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
    for coll in (bpy.data.meshes, bpy.data.curves):
        pass

def mat(name, color, rough=0.85, metal=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m

def brick_mat():
    m = bpy.data.materials.get("Brick") or bpy.data.materials.new("Brick")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 0.9
    tex = nt.nodes.new("ShaderNodeTexCoord")
    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.inputs["Color1"].default_value = (0.42, 0.20, 0.13, 1)
    brick.inputs["Color2"].default_value = (0.50, 0.26, 0.16, 1)
    brick.inputs["Mortar"].default_value = (0.62, 0.58, 0.52, 1)
    brick.inputs["Scale"].default_value = 3.0
    brick.inputs["Mortar Size"].default_value = 0.012
    brick.inputs["Row Height"].default_value = 0.25
    brick.inputs["Brick Width"].default_value = 0.5
    nt.links.new(tex.outputs["Generated"], brick.inputs["Vector"])
    nt.links.new(brick.outputs["Color"], bsdf.inputs["Base Color"])
    return m

def box(name, loc, dims, material=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material: o.data.materials.append(material)
    return o

def cyl(name, loc, r, h, material=None, verts=16, rot=(0, 0, 0), r2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r if r2 is None else r2,
                                    depth=h, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material: o.data.materials.append(material)
    return o

def profile_prism(name, pts_xz, y0, y1, material):
    """Extrude a 2D profile (x,z) between y0 and y1."""
    n = len(pts_xz)
    verts = [(x, y0, z) for x, z in pts_xz] + [(x, y1, z) for x, z in pts_xz]
    faces = []
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    me = bpy.data.meshes.new(name + "Mesh")
    me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    if material: me.materials.append(material)
    return o

def figure(name, loc, female=True, coat=(0.16, 0.14, 0.13)):
    g = []
    x, y, z = loc
    mc = mat("Coat" + name, coat, 0.9)
    sk = mat("Skin", (0.76, 0.58, 0.46), 0.7)
    if female:
        g.append(cyl(name + "_skirt", (x, y, z + 0.48), 0.40, 0.96, mc, verts=14, r2=0.15))
        g.append(cyl(name + "_bodice", (x, y, z + 1.13), 0.155, 0.36, mc, verts=12, r2=0.13))
    else:
        g.append(box(name + "_legs", (x, y, z + 0.42), (0.26, 0.17, 0.84), mat("Trou", (0.23, 0.21, 0.19), 0.9)))
        g.append(cyl(name + "_coat", (x, y, z + 1.12), 0.20, 0.62, mc, verts=12, r2=0.165))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.105, location=(x, y, z + 1.56), segments=12, ring_count=8)
    h = bpy.context.object; h.name = name + "_head"; h.data.materials.append(sk); g.append(h)
    if female:
        g.append(cyl(name + "_bonnet", (x, y, z + 1.63), 0.115, 0.07, mc, verts=12))
    else:
        g.append(cyl(name + "_hatbrim", (x, y, z + 1.635), 0.16, 0.02, mc, verts=16))
        g.append(cyl(name + "_hat", (x, y, z + 1.74), 0.105, 0.19, mc, verts=16))
    return g

# ---------- materials ----------
clean()
STUCCO = mat("Stucco", (0.74, 0.69, 0.60), 0.95)
BRICK = mat("BrickTrim", (0.47, 0.25, 0.16), 0.9)
BRICKP = mat("BrickPlain", (0.45, 0.23, 0.15), 0.9)
SLATE = mat("Slate", (0.23, 0.25, 0.28), 0.8)
GLASS = mat("GlassDark", (0.10, 0.13, 0.15), 0.25, 0.1)
WOOD = mat("WoodDark", (0.30, 0.21, 0.13), 0.85)
IRON = mat("Iron", (0.12, 0.12, 0.13), 0.6, 0.4)
STONE = mat("Stone", (0.68, 0.64, 0.57), 0.9)
DARK = mat("Recess", (0.07, 0.06, 0.05), 1.0)
GROUND = mat("Ground", (0.52, 0.48, 0.42), 1.0)

W = 13.2; D = 7.6; GF = 3.1; FF = 6.2  # width, depth, floor heights

# ---------- main block ----------
box("Walls", (0, 0, FF / 2), (W, D, FF), STUCCO)
# brick quoins / vertical trim strips (front)
for sx in (-1, 1):
    box("Quoin", (sx * (W / 2 - 0.14), -D / 2 - 0.015, FF / 2), (0.28, 0.09, FF), BRICK)
    box("QuoinC", (sx * 2.55, -D / 2 - 0.015, FF / 2), (0.24, 0.09, FF), BRICK)
    box("QuoinS", (sx * (W / 2 - 0.14), 0, FF / 2), (0.10, D, FF), BRICK)  # side corners
# horizontal string courses (slightly prouder than quoins to avoid coplanar faces)
for z in (GF, FF - 0.12):
    box("String", (0, -D / 2 - 0.04, z), (W, 0.12, 0.22), BRICK)
box("Plinth", (0, -D / 2 - 0.01, 0.28), (W, 0.08, 0.56), BRICK)

# ---------- roof (pitched, behind gables) ----------
import mathutils
roof_pts = [(-W / 2 - 0.3, 6.0), (0, 8.05), (W / 2 + 0.3, 6.0)]
# build as two sloped boxes
for s in (-1, 1):
    ln = math.hypot(W / 2 + 0.3, 2.05)
    ang = math.atan2(2.05, W / 2 + 0.3)
    box("RoofSlope", (s * (W / 4 + 0.07), 0, 7.02), (ln, D + 0.5, 0.14), SLATE, rot=(0, s * ang, 0))
# side gable triangles (stucco) closing roof ends
for s in (-1, 1):
    profile_prism("GableEnd", [(0, 6.0), (0, 8.05)], 0, 0, STUCCO)  # placeholder removed below
    bpy.ops.object.select_all(action='DESELECT')
# (gable ends made properly:)
for o in list(bpy.data.objects):
    if o.name.startswith("GableEnd"):
        bpy.data.objects.remove(o, do_unlink=True)
for s in (-1, 1):
    me_pts = [(-D / 2, 6.0), (D / 2, 6.0), (0, 8.05)]
    verts = [(s * (W / 2), y, z) for y, z in me_pts]
    me = bpy.data.meshes.new("GE"); me.from_pydata(verts, [], [(0, 1, 2)]); me.update()
    o = bpy.data.objects.new("GableEnd", me); bpy.context.collection.objects.link(o); me.materials.append(STUCCO)

# ---------- shaped front gables ----------
def shaped_gable(name, cx, w, top, base=FF):
    hw = w / 2
    pts = [(-hw, base), (-hw, top - 0.55), (-hw + 0.28, top - 0.42), (-hw + 0.55, top - 0.14),
           (-0.30, top - 0.06), (0, top), (0.30, top - 0.06), (hw - 0.55, top - 0.14),
           (hw - 0.28, top - 0.42), (hw, top - 0.55), (hw, base)]
    pts = [(cx + px, pz) for px, pz in pts]
    profile_prism(name, pts, -D / 2 - 0.16, -D / 2 + 0.10, STUCCO)
    # roundel
    bpy.ops.mesh.primitive_torus_add(major_radius=0.30, minor_radius=0.07,
                                     location=(cx, -D / 2 - 0.18, top - 0.62), rotation=(0, 0, 0))
    t = bpy.context.object; t.name = name + "_roundel"; t.data.materials.append(BRICKP)
    cyl(name + "_disc", (cx, -D / 2 - 0.17, top - 0.62), 0.26, 0.06, STONE, verts=20, rot=(math.pi / 2, 0, 0))
    # finial: small obelisk
    cyl(name + "_finial", (cx, -D / 2 - 0.05, top + 0.28), 0.02, 0.55, STONE, verts=4, r2=0.11)
    box(name + "_finbase", (cx, -D / 2 - 0.05, top + 0.02), (0.24, 0.24, 0.10), STONE)

shaped_gable("GableL", -4.35, 3.9, 7.35)
shaped_gable("GableR", 4.35, 3.9, 7.35)
shaped_gable("GableC", 0, 4.7, 7.75)

# ---------- chimneys ----------
box("ChimneyL", (-5.6, 0.8, 8.0), (1.0, 1.4, 4.4), BRICKP)      # tall left stack
box("ChimneyLcap", (-5.6, 0.8, 10.25), (1.2, 1.6, 0.18), STONE)
box("ChimneyC", (1.9, 0.6, 7.9), (1.5, 1.1, 3.4), STUCCO)
box("ChimneyCtrim", (1.9, 0.6, 9.35), (1.62, 1.22, 0.5), BRICK)
box("ChimneyR", (5.5, 0.8, 7.9), (1.0, 1.3, 3.6), BRICKP)
box("ChimneyRcap", (5.5, 0.8, 9.75), (1.2, 1.5, 0.18), STONE)

# ---------- windows ----------
def window(name, cx, cz, w=1.8, h=2.0):
    box(name + "_surround", (cx, -D / 2 - 0.03, cz), (w + 0.36, 0.12, h + 0.36), BRICK)
    box(name + "_glass", (cx, -D / 2 - 0.06, cz), (w, 0.06, h), GLASS)
    box(name + "_mullV", (cx, -D / 2 - 0.09, cz), (0.06, 0.04, h), WOOD)
    box(name + "_mullH", (cx, -D / 2 - 0.09, cz), (w, 0.04, 0.06), WOOD)
    box(name + "_sill", (cx, -D / 2 - 0.06, cz - h / 2 - 0.24), (w + 0.44, 0.16, 0.10), STONE)

window("WinGL", -4.35, 1.65); window("WinGR", 4.35, 1.65)
window("WinFL", -4.35, 4.72); window("WinFR", 4.35, 4.72)

# ---------- central open gallery / porch ----------
RW = 3.3  # recess width
# dark recess panels applied on the facade (the main block is solid; the panels,
# columns and railing in front of them give the engraved recessed-gallery read)
box("PorchBack", (0, -D / 2 - 0.06, GF / 2), (RW, 0.10, GF), DARK)
box("GalleryBack", (0, -D / 2 - 0.06, GF + (FF - GF) / 2), (RW, 0.10, FF - GF), DARK)
box("GalleryDoor", (0.55, -D / 2 - 0.13, GF + 1.05), (0.95, 0.06, 2.1), WOOD)
# porch side walls + columns
for s in (-1, 1):
    box("PorchSide", (s * (RW / 2 - 0.08), -D / 2 + 0.5, GF / 2), (0.16, 1.0, GF), STUCCO)
    cyl("PorchCol", (s * (RW / 2 - 0.28), -D / 2 + 0.18, GF / 2), 0.07, GF, WOOD, verts=10)
# gallery floor slab + railing
box("GalleryFloor", (0, -D / 2 + 0.38, GF + 0.03), (RW + 0.2, 1.15, 0.10), STONE)
for i in range(15):
    x = -RW / 2 + 0.15 + i * (RW - 0.3) / 14
    box("RailBar", (x, -D / 2 - 0.18, GF + 0.55), (0.035, 0.035, 1.0), IRON)
box("RailTop", (0, -D / 2 - 0.18, GF + 1.06), (RW + 0.05, 0.05, 0.06), WOOD)
# stair glimpse inside porch (interpretation)
for i in range(6):
    box("StairStep", (-1.05, -D / 2 + 0.55, 0.25 + i * 0.001), (0.9, 0.5, 0.5), DARK)

# ---------- front wall, piers, gate ----------
WY = -D / 2 - 2.3
box("FrontWallL", (-3.9, WY, 0.45), (5.3, 0.25, 0.9), STUCCO)
box("FrontWallR", (3.9, WY, 0.45), (5.3, 0.25, 0.9), STUCCO)
box("WallCopL", (-3.9, WY, 0.95), (5.3, 0.34, 0.10), STONE)
box("WallCopR", (3.9, WY, 0.95), (5.3, 0.34, 0.10), STONE)
for s in (-1, 1):
    box("GatePier", (s * 1.35, WY, 0.65), (0.45, 0.45, 1.3), STUCCO)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17, location=(s * 1.35, WY, 1.42), segments=12, ring_count=8)
    b = bpy.context.object; b.name = "PierBall"; b.scale = (1, 1, 0.8); b.data.materials.append(STONE)
# iron gate (two leaves, simplified scroll = frame + bars)
for s in (-1, 1):
    for i in range(5):
        box("GateBar", (s * (0.18 + i * 0.24), WY, 0.55), (0.03, 0.03, 1.0), IRON)
    box("GateRail", (s * 0.62, WY, 1.02), (1.2, 0.03, 0.05), IRON)
    box("GateRail2", (s * 0.62, WY, 0.18), (1.2, 0.03, 0.05), IRON)

# ground
box("Ground", (0, -0.8, -0.06), (22, 13, 0.12), GROUND)

# figures (stylised, for scale — interpretive)
figure("Fig1", (-3.4, -6.6, 0), female=False)
figure("Fig2", (2.2, -6.9, 0), female=True, coat=(0.20, 0.16, 0.22))
figure("Fig3", (3.1, -6.7, 0), female=True, coat=(0.25, 0.18, 0.14))

# ---------- finish ----------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.ops.object.select_all(action='DESELECT')
tris = 0
for o in bpy.data.objects:
    if o.type == 'MESH':
        tris += sum(len(p.vertices) - 2 for p in o.data.polygons)
print("TRIANGLES:", tris)

# camera + render
scene = bpy.context.scene
scene.render.engine = 'CYCLES'; scene.cycles.samples = 48; scene.cycles.device = 'CPU'
scene.render.resolution_x = 960; scene.render.resolution_y = 720
scene.world = bpy.data.worlds.new("W"); scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1)
scene.world.node_tree.nodes["Background"].inputs[1].default_value = 1.0
bpy.ops.object.light_add(type='SUN', location=(6, -8, 14))
sun = bpy.context.object; sun.data.energy = 2.4; sun.rotation_euler = (math.radians(50), 0, math.radians(35))
bpy.ops.object.camera_add(location=(-14.5, -21.0, 6.0))
cam = bpy.context.object
cam.rotation_euler = (Vector((0, 0, 2.9)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 44
scene.camera = cam
scene.render.filepath = os.path.join(OUT, "preview.png")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, SLUG + ".blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, SLUG + ".glb"), export_format='GLB')
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
