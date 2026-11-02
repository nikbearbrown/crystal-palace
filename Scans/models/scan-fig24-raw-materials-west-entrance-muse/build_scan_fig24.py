# scan-fig24-raw-materials-west-entrance — Raw materials display outside the west entrance, 1851
# Reference: fig-24_raw-materials-west-entrance-crystal-palace.png (colour view)
import bpy, math, random, os
from mathutils import Vector

SLUG = "scan-fig24-raw-materials-west-entrance"
OUT = os.path.dirname(os.path.abspath(__file__))
random.seed(24)

def clean():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()

def mat(name, color, rough=0.9, metal=0.0, alpha=None):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if alpha is not None:
        bsdf.inputs["Alpha"].default_value = alpha
        try: m.surface_render_method = 'DITHERED'
        except Exception: pass
    return m

def box(name, loc, dims, material=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material: o.data.materials.append(material)
    return o

def cyl(name, loc, r, h, material=None, verts=14, rot=(0, 0, 0), r2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r if r2 is None else r2,
                                    depth=h, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material: o.data.materials.append(material)
    return o

def sphere(name, loc, r, material=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=12, ring_count=8)
    o = bpy.context.object; o.name = name
    if material: o.data.materials.append(material)
    return o

def figure(name, loc, female=True, coat=(0.16, 0.14, 0.13)):
    x, y, z = loc
    mc = mat("Coat" + name, coat, 0.9); sk = mat("Skin", (0.76, 0.58, 0.46), 0.7)
    if female:
        cyl(name + "_skirt", (x, y, z + 0.48), 0.40, 0.96, mc, verts=12, r2=0.15)
        cyl(name + "_bodice", (x, y, z + 1.13), 0.155, 0.36, mc, verts=12, r2=0.13)
    else:
        box(name + "_legs", (x, y, z + 0.42), (0.26, 0.17, 0.84), mat("Trou", (0.23, 0.21, 0.19), 0.9))
        cyl(name + "_coat", (x, y, z + 1.12), 0.20, 0.62, mc, verts=12, r2=0.165)
    sphere(name + "_head", (x, y, z + 1.56), 0.105, sk)
    if female: cyl(name + "_bonnet", (x, y, z + 1.63), 0.115, 0.07, mc, verts=12)
    else:
        cyl(name + "_hatbrim", (x, y, z + 1.635), 0.16, 0.02, mc, verts=14)
        cyl(name + "_hat", (x, y, z + 1.74), 0.105, 0.19, mc, verts=14)

def boulder(name, loc, s, material):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=s, location=loc)
    o = bpy.context.object; o.name = name
    for v in o.data.vertices:
        v.co.x *= random.uniform(0.85, 1.2); v.co.y *= random.uniform(0.8, 1.1); v.co.z *= random.uniform(0.55, 0.75)
    for p in o.data.polygons: p.use_smooth = False
    o.data.materials.append(material)
    return o

clean()
SAND = mat("Sandstone", (0.55, 0.42, 0.26), 0.95)
SLATE = mat("SlateBlue", (0.30, 0.34, 0.38), 0.85)
PALE = mat("PaleStone", (0.66, 0.56, 0.38), 0.95)
BLACK = mat("BlackSlate", (0.08, 0.08, 0.09), 0.9)
WOOD = mat("Timber", (0.55, 0.38, 0.20), 0.9)
WOODD = mat("TimberDark", (0.38, 0.26, 0.14), 0.9)
MARBLE = mat("MarbleShaft", (0.78, 0.76, 0.70), 0.6)
IRON = mat("IronPalace", (0.52, 0.50, 0.44), 0.6, 0.2)
GLASS = mat("Glass", (0.75, 0.82, 0.85), 0.12, 0.0, alpha=0.35)
GROUND = mat("Earth", (0.50, 0.38, 0.25), 1.0)

box("Ground", (0, 0, -0.07), (34, 24, 0.14), GROUND)

# central stone obelisk (tapered, square section, rough top)
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.95, radius2=0.62, depth=8.6,
                                location=(0.6, 1.0, 4.3), rotation=(0, 0, math.radians(45)))
ob = bpy.context.object; ob.name = "Obelisk"; ob.data.materials.append(SAND)
box("ObeliskBase", (0.6, 1.0, 0.25), (1.9, 1.9, 0.5), SAND)

# leaning slate slabs (left)
for i, (lx, lz, ang) in enumerate([(-3.4, 1.7, 0.42), (-4.6, 1.5, 0.5), (-2.2, 1.9, 0.35)]):
    box(f"SlateSlab{i}", (lx, 1.2, lz), (2.6, 0.16, 3.4), SLATE, rot=(ang, 0, 0.06 * i))
box("SlateUpright", (-2.6, 3.4, 2.2), (0.18, 2.2, 4.4), SLATE, rot=(0, 0, 0.1))

# foreground boulders
boulder("Boulder1", (-1.6, -1.8, 0.55), 1.15, SAND)
boulder("Boulder2", (-0.1, -2.2, 0.42), 0.9, SAND)
boulder("Boulder3", (1.9, -1.7, 0.5), 1.0, PALE)
boulder("Boulder4", (-2.9, -1.2, 0.35), 0.7, PALE)

# stacked pale slabs (right of obelisk)
for i in range(4):
    box(f"SlabStack{i}", (3.4, 0.6, 0.22 + i * 0.24), (2.2, 1.5, 0.2), PALE, rot=(0, 0, 0.03 * i))
for i in range(3):
    box(f"SlabLean{i}", (4.6, 1.0, 1.0), (1.7, 0.14, 2.0), PALE, rot=(0.5, 0, -0.15 * i))

# timber baulks leaning
for i in range(4):
    box(f"Baulk{i}", (5.9 + i * 0.28, 1.3, 1.15), (0.24, 0.24, 3.1), WOOD, rot=(0.62, 0, 0))

# black slate slabs stack (back right)
for i in range(5):
    box(f"BlackSlab{i}", (7.6, 3.6, 0.3 + i * 0.42), (2.6, 1.7, 0.38), BLACK, rot=(0, 0, 0.02 * i))

# wooden hoist tower with pyramidal cap (back right)
tx, ty = 9.6, 4.6
for dx in (-0.8, 0.8):
    for dy in (-0.8, 0.8):
        box("TowerPost", (tx + dx, ty + dy, 3.1), (0.18, 0.18, 6.2), WOODD)
for z in (1.6, 3.4, 5.2):
    box("TowerRail", (tx, ty - 0.8, z), (1.8, 0.1, 0.12), WOODD)
    box("TowerRail2", (tx, ty + 0.8, z), (1.8, 0.1, 0.12), WOODD)
for s in (-1, 1):
    box("TowerBrace", (tx, ty + s * 0.8, 3.1), (0.1, 0.1, 4.6), WOODD, rot=(s * 0.62, 0, 0))
    box("TowerBrace2", (tx + s * 0.8, ty, 3.1), (0.1, 0.1, 4.6), WOODD, rot=(0, -s * 0.62, 0))
cyl("TowerCap", (tx, ty, 6.9), 1.55, 1.6, WOODD, verts=4, rot=(0, 0, math.radians(45)), r2=0.05)

# fluted column shaft behind tower
col = cyl("ColumnShaft", (11.6, 4.2, 2.2), 0.42, 4.4, MARBLE, verts=24)
box("ColumnBase", (11.6, 4.2, 0.3), (1.1, 1.1, 0.6), MARBLE)

# small distant building with round-window frieze (centre background, simplified)
box("DistantBldg", (2.2, 9.5, 1.5), (5.5, 1.6, 3.0), mat("DistantWall", (0.66, 0.62, 0.55), 0.95))
box("DistantRoof", (2.2, 9.5, 3.25), (5.9, 2.0, 0.5), SLATE)
for i in range(6):
    cyl("Roundel", (-0.05 + i * 0.95, 8.62, 2.45), 0.20, 0.06, mat("RoundelW", (0.85, 0.83, 0.78), 0.8), verts=14, rot=(math.pi / 2, 0, 0))

# ---- palace west front backdrop: 3 bays along the right side (24 ft module, flagged) ----
BAY = 7.315; PX = 14.5
for i in range(4):
    py = -6.5 + i * BAY * 0.62
    cyl("FrontCol", (PX, py, 5.0), 0.16, 10.0, IRON, verts=12)
for lvl, zz in ((0.12, 5.0), (0.12, 10.0)):
    pass
box("FrontTier1", (PX, -0.02, 5.0), (0.25, 3 * BAY * 0.62 + 1.0, 9.6), GLASS)
box("FrontBand", (PX - 0.1, -0.02, 5.05), (0.18, 3 * BAY * 0.62 + 1.0, 0.5), IRON)
box("FrontBandTop", (PX - 0.1, -0.02, 9.95), (0.18, 3 * BAY * 0.62 + 1.0, 0.4), IRON)
box("FrontBandBase", (PX - 0.1, -0.02, 0.35), (0.18, 3 * BAY * 0.62 + 1.0, 0.7), IRON)
for i in range(9):
    py = -6.5 + i * (3 * BAY * 0.62) / 8
    box("FrontMullion", (PX - 0.08, py, 5.0), (0.07, 0.09, 9.6), IRON)

# visitors
figure("F1", (-5.6, -1.4, 0), female=False)
figure("F2", (7.3, -1.6, 0), female=True, coat=(0.55, 0.40, 0.15))
figure("F3", (6.4, -2.1, 0), female=False)
figure("F4", (-4.4, -0.6, 0), female=False)
box("Paper", (-5.35, -1.62, 1.05), (0.3, 0.02, 0.4), mat("Paper", (0.9, 0.88, 0.82), 0.9), rot=(0.4, 0, 0))

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.ops.object.select_all(action='DESELECT')
tris = sum(len(p.vertices) - 2 for o in bpy.data.objects if o.type == 'MESH' for p in o.data.polygons)
print("TRIANGLES:", tris)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'; scene.cycles.samples = 48; scene.cycles.device = 'CPU'
scene.render.resolution_x = 960; scene.render.resolution_y = 720
scene.world = bpy.data.worlds.new("W"); scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1)
bpy.ops.object.light_add(type='SUN', location=(-6, -8, 14))
sun = bpy.context.object; sun.data.energy = 3.0; sun.rotation_euler = (math.radians(55), 0, math.radians(-30))
bpy.ops.object.camera_add(location=(-15.5, -17.5, 4.4))
cam = bpy.context.object
cam.rotation_euler = (Vector((1.5, 1.5, 2.9)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 44
scene.camera = cam
scene.render.filepath = os.path.join(OUT, "preview.png")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, SLUG + ".blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, SLUG + ".glb"), export_format='GLB')
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
