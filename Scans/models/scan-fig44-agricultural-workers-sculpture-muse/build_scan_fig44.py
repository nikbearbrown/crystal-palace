# Build script — scan-fig44-agricultural-workers-sculpture (Muse version)
# Reference: fig-44_agricultural-workers-great-exhibition-1851.png (ILN, 19 July 1851)
# Rural visitors standing among sculpture exhibits; principal statue is the large
# standing DOG on its plinth (catalogue text says "a lion"; the image clearly shows
# a dog — the image governs). Stylised figures; abstracted statue; sculptor pass deferred.
import bpy, math, os
from mathutils import Vector

OUT = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig44-agricultural-workers-sculpture"

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ---------- materials ----------
def mat(name, rgb, rough=0.9):
    m = bpy.data.materials.new(name); m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return m

STONE  = mat("Stone",  (0.62, 0.60, 0.56))
STONE2 = mat("StoneDark", (0.45, 0.43, 0.40))
FLOOR  = mat("Floor",  (0.55, 0.52, 0.48))
COATS = [mat("CoatA", (0.36, 0.30, 0.24)), mat("CoatB", (0.25, 0.22, 0.20)),
         mat("Smock", (0.62, 0.58, 0.50)), mat("CoatC", (0.30, 0.26, 0.30))]
DRESS = [mat("DressA", (0.38, 0.28, 0.26)), mat("DressB", (0.28, 0.32, 0.38)),
         mat("DressC", (0.45, 0.40, 0.32))]
SKIN   = mat("Skin", (0.80, 0.62, 0.50))
DARK   = mat("Dark", (0.16, 0.15, 0.14))
WOOD   = mat("Wood", (0.42, 0.32, 0.22))

# ---------- primitives ----------
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

# ---------- stylised figures (interpretive; no likenesses) ----------
def hat_top(loc, s=1.0):
    cyl("brim", (loc[0], loc[1], loc[2]), 0.115 * s, 0.115 * s, 0.015, DARK, 12)
    cyl("tophat", (loc[0], loc[1], loc[2] + 0.085 * s), 0.082 * s, 0.088 * s, 0.16 * s, DARK, 12)

def hat_cap(loc, s=1.0, ry=0.0):
    sph("cap", (loc[0], loc[1], loc[2] + 0.01), (0.095 * s, 0.095 * s, 0.06 * s), COATS[1])
    box("peak", (loc[0] + math.sin(ry) * 0.1 * s, loc[1] + math.cos(ry) * 0.1 * s, loc[2]),
        (0.09 * s, 0.07 * s, 0.012), DARK, (0, 0, -ry))

def figure_man(x, y, ry=0.0, h=1.72, coat=None, hat="cap", smock=False):
    coat = coat or COATS[0]; s = h / 1.72
    fx, fy = math.sin(ry), math.cos(ry)  # facing direction (local +Y after rot -ry)
    # short boot hints at the base — no stick legs
    for dx in (-0.085, 0.085):
        box("boot", (x + dx * s * math.cos(ry) + fx * 0.05 * s,
                     y - dx * s * math.sin(ry) + fy * 0.05 * s, 0.05 * s),
            (0.10 * s, 0.22 * s, 0.10 * s), DARK, (0, 0, -ry))
    # tapered smock/coat body mass reaching near the ground (house style, cf. fig67 women/men)
    rbase = 0.29 if smock else 0.265
    cyl("body", (x, y, 0.555 * s), rbase * s, 0.20 * s, 0.95 * s, coat, 14)
    cyl("chest", (x, y, 1.28 * s), 0.20 * s, 0.115 * s, 0.50 * s, coat, 14)
    # arms hanging
    for dx in (-0.235, 0.235):
        box("arm", (x + dx * s * math.cos(ry), y - dx * s * math.sin(ry), 1.05 * s),
            (0.075 * s, 0.075 * s, 0.55 * s), coat, (0.06, 0, -ry))
    sph("head", (x, y, 1.60 * s), (0.092 * s, 0.096 * s, 0.112 * s), SKIN)
    if hat == "top": hat_top((x, y, 1.68 * s), s)
    elif hat == "cap": hat_cap((x, y, 1.685 * s), s, ry)
    elif hat == "bowler":
        sph("bowler", (x, y, 1.685 * s), (0.10 * s, 0.10 * s, 0.055 * s), DARK)
        cyl("bbrim", (x, y, 1.665 * s), 0.115 * s, 0.115 * s, 0.012, DARK, 12)

def figure_woman(x, y, ry=0.0, h=1.62, dress=None):
    dress = dress or DRESS[0]; s = h / 1.62
    cyl("skirt", (x, y, 0.42 * s), 0.30 * s, 0.16 * s, 0.84 * s, dress, 12)
    box("bodice", (x, y, 1.02 * s), (0.30 * s, 0.20 * s, 0.36 * s), dress, (0, 0, -ry))
    for dx in (-0.20, 0.20):
        box("arm", (x + dx * s * math.cos(ry), y - dx * s * math.sin(ry), 0.95 * s),
            (0.06 * s, 0.06 * s, 0.45 * s), dress, (0.15, 0, -ry))
    sph("head", (x, y, 1.36 * s), (0.078 * s, 0.082 * s, 0.095 * s), SKIN)
    # bonnet: half-dome + brim ring hint
    sph("bonnet", (x, y - 0.012 * s, 1.40 * s), (0.095 * s, 0.10 * s, 0.085 * s), dress)
    cyl("bonnetbrim", (x, y + 0.02 * s, 1.375 * s), 0.105 * s, 0.105 * s, 0.012, dress, 12)

def figure_child(x, y, ry=0.0, h=1.05, dress=None):
    figure_woman(x, y, ry, h, dress) if dress else figure_man(x, y, ry, h, COATS[2], "cap")

# ---------- ground ----------
box("Floor", (0, 0, -0.03), (9.0, 5.6, 0.06), FLOOR)

# ---------- dog plinth (right of centre) ----------
PX, PY = 1.85, -1.05
box("DogPlinth", (PX, PY, 0.70), (2.1, 1.0, 1.40), STONE)
box("DogPlinthBase", (PX, PY, 0.06), (2.3, 1.15, 0.12), STONE2)
box("DogPlinthCap", (PX, PY, 1.45), (2.25, 1.10, 0.10), STONE)
box("PlinthLabel", (PX, PY + 0.53, 0.95), (0.42, 0.03, 0.26), STONE2)  # blank label plate

# ---------- the dog statue (abstracted monumental mass; detail deferred) ----------
DZ = 1.50  # plinth top
DX, DY = PX, PY
sph("DogBody", (DX, DY, DZ + 0.78), (0.88, 0.30, 0.34), STONE)          # torso mass
sph("DogChest", (DX + 0.72, DY, DZ + 0.76), (0.30, 0.28, 0.33), STONE)  # deep chest, head end -X
for lx, ly in ((-0.62, -0.16), (-0.62, 0.16), (0.62, -0.16), (0.62, 0.16)):
    cyl("DogLeg", (DX + lx, DY + ly, DZ + 0.30), 0.075, 0.088, 0.62, STONE, 8)
    box("DogPaw", (DX + lx + 0.02, DY + ly, DZ + 0.025), (0.20, 0.11, 0.05), STONE)
cyl("DogNeck", (DX + 0.92, DY, DZ + 0.92), 0.16, 0.20, 0.35, STONE, 10, (0, 0, math.radians(-55)))
sph("DogHead", (DX + 1.08, DY, DZ + 1.06), (0.21, 0.17, 0.19), STONE)
box("DogMuzzle", (DX + 1.28, DY, DZ + 0.99), (0.22, 0.15, 0.13), STONE)
for ly in (-0.13, 0.13):  # long drop ears
    box("DogEar", (DX + 1.02, DY + ly, DZ + 0.94), (0.16, 0.045, 0.30), STONE)
cyl("DogTail", (DX - 0.92, DY, DZ + 0.62), 0.035, 0.05, 0.55, STONE, 8, (0, math.radians(38), 0))

# ---------- second plinth, left rear: lower legs of a standing statue ----------
LX, LY = -2.75, -1.35
box("LegsPlinth", (LX, LY, 0.55), (1.3, 0.9, 1.10), STONE)
for dx in (-0.18, 0.18):
    cyl("StatueLeg", (LX + dx, LY, 1.10 + 0.55), 0.11, 0.14, 1.10, STONE, 10)  # cut off by frame, as drawn
box("StatueDrape", (LX + 0.30, LY - 0.05, 1.55), (0.28, 0.5, 0.9), STONE)      # drapery edge

# ---------- ornate lamp / candelabrum silhouette, centre rear ----------
cyl("LampPost", (0.1, -1.9, 1.30), 0.045, 0.06, 2.60, DARK, 8)
sph("LampBowl", (0.1, -1.9, 2.72), (0.20, 0.20, 0.12), STONE2)
for a in range(5):
    ang = a * 2 * math.pi / 5
    cyl("LampArm", (0.1 + 0.17 * math.cos(ang), -1.9 + 0.17 * math.sin(ang), 2.72),
        0.014, 0.014, 0.22, DARK, 6)
    sph("LampGlobe", (0.1 + 0.19 * math.cos(ang), -1.9 + 0.19 * math.sin(ang), 2.86), (0.045, 0.045, 0.055), STONE2, 8)

# ---------- vague statue mass, far right rear ----------
box("FarPlinth", (3.85, -1.6, 0.5), (0.8, 0.7, 1.0), STONE2)
sph("FarStatue", (3.85, -1.6, 1.45), (0.30, 0.24, 0.55), STONE2)

# ---------- crowd (stylised, interpretive) ----------
figure_man(-3.55, -0.15, 0.15, 1.74, COATS[1], "none")
figure_woman(-3.05, 0.25, 0.1, dress=DRESS[0])
figure_child(-3.30, 0.75, 0.0, 1.02, DRESS[2])
figure_man(-2.45, 0.05, 0.2, 1.70, COATS[0], "top")
figure_man(-1.95, 0.35, 0.1, 1.76, COATS[2], "cap", smock=True)
figure_woman(-1.45, 0.15, -0.1, dress=DRESS[1])
figure_child(-1.80, 0.85, 0.2, 0.98, DRESS[0])
figure_man(-0.95, -0.05, 0.0, 1.78, COATS[1], "top")
figure_woman(-0.45, 0.30, 0.05, dress=DRESS[2])
figure_man(0.15, 0.10, -0.1, 1.70, COATS[0], "bowler", smock=True)   # old man w/ smock
figure_man(0.70, 0.25, 0.15, 1.73, COATS[1], "cap")
figure_woman(1.20, 0.05, 0.0, dress=DRESS[0])
figure_child(2.05, 0.80, 3.14, 1.0, None)                            # boy seen from back, right
figure_man(2.55, 0.20, -0.15, 1.68, COATS[2], "cap", smock=True)
figure_woman(3.05, 0.45, -0.05, dress=DRESS[1])
figure_man(3.55, 0.05, -0.2, 1.75, COATS[0], "bowler", smock=True)
figure_man(4.05, 0.30, -0.3, 1.72, COATS[1], "cap")
# walking sticks
cyl("Stick1", (0.42, 0.42, 0.45), 0.016, 0.016, 0.95, WOOD, 6, (math.radians(18), 0, 0))
cyl("Stick2", (4.28, 0.55, 0.45), 0.016, 0.016, 0.95, WOOD, 6, (math.radians(-14), 0, 0))
# a bundle / basket at feet
cyl("Bundle", (-1.55, 0.95, 0.14), 0.20, 0.15, 0.28, WOOD, 10)

# ---------- camera / light / render ----------
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.use_denoising = True
scene.render.resolution_x = 960; scene.render.resolution_y = 640
scene.render.filepath = os.path.join(OUT, "preview.png")
world = bpy.data.worlds.new("W"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.9
bpy.ops.object.light_add(type='SUN', location=(4, 6, 8))
sun = bpy.context.object; sun.data.energy = 3.0; sun.rotation_euler = (math.radians(50), 0, math.radians(35))
bpy.ops.object.camera_add(location=(0.3, 9.9, 2.8))
cam = bpy.context.object; scene.camera = cam
cam.rotation_euler = (math.radians(83), 0, math.radians(180))
cam.data.lens = 36

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
