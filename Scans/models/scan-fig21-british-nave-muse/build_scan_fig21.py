# scan-fig21-british-nave — Western (British) nave vignette, Crystal Palace, Hyde Park 1851
# Reference: fig-21_western-british-nave-crystal-palace.png (colour view along the nave)
# Documented module basis: 24 ft (7.315 m) bay; nave 72 ft (21.95 m) wide; gallery level ~24 ft.
import bpy, math, os
from mathutils import Vector

SLUG = "scan-fig21-british-nave"
OUT = os.path.dirname(os.path.abspath(__file__))

def clean():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()

def mat(name, color, rough=0.85, metal=0.0, alpha=None):
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

def sphere(name, loc, r, material=None, sy=1.0):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=14, ring_count=10)
    o = bpy.context.object; o.name = name; o.scale = (1, 1, sy)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
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

clean()
IRON = mat("IronPainted", (0.55, 0.52, 0.45), 0.6, 0.2)
IRONR = mat("IronRed", (0.38, 0.18, 0.13), 0.65, 0.1)
GLASS = mat("Glass", (0.75, 0.82, 0.85), 0.12, 0.0, alpha=0.35)
WOODF = mat("FloorWood", (0.55, 0.40, 0.24), 0.9)
RED = mat("DisplayRed", (0.55, 0.13, 0.10), 0.8)
GOLD = mat("GoldPaint", (0.62, 0.45, 0.18), 0.55, 0.25)
BRONZE = mat("Bronze", (0.22, 0.18, 0.13), 0.5, 0.5)
DARK = mat("DarkExhibit", (0.13, 0.11, 0.10), 0.7)
CREAM = mat("Cream", (0.78, 0.72, 0.60), 0.8)

BAY = 7.315; LEN = 1.5 * BAY          # 10.97 m along X
NAVE_HW = 10.97                        # half width of nave (72 ft)
SPRING = 8.6; R = 10.97; CROWN = SPRING + 8.4   # vault: shallow segment, crown ~17 m (interpretation)
GAL = 7.3                              # gallery level

# floor
box("Floor", (0, 0, -0.09), (LEN + 4, 29, 0.18), WOODF)

# columns (both sides, 4 along length) + transverse positions
for sx in (-LEN / 2, -LEN / 6, LEN / 6, LEN / 2):
    for sy in (-1, 1):
        cyl("Column", (sx, sy * 9.4, SPRING / 2), 0.14, SPRING, IRON, verts=12)
        cyl("ColBase", (sx, sy * 9.4, 0.35), 0.24, 0.7, IRONR, verts=12)
        cyl("ColCap", (sx, sy * 9.4, SPRING - 0.25), 0.22, 0.5, IRON, verts=12)
        # gallery columns continue above gallery
        cyl("ColumnUp", (sx, sy * 11.8, GAL + 1.8), 0.10, 3.6, IRON, verts=10)

# galleries both sides
for sy in (-1, 1):
    box("GallerySlab", (0, sy * 11.4, GAL), (LEN, 4.6, 0.28), IRONR)
    box("GalleryRail", (0, sy * 9.45, GAL + 0.95), (LEN, 0.06, 0.08), IRON)
    box("GalleryFascia", (0, sy * 9.42, GAL - 0.28), (LEN, 0.08, 0.42), GOLD)
    for i in range(26):
        x = -LEN / 2 + 0.3 + i * (LEN - 0.6) / 25
        box("Baluster", (x, sy * 9.45, GAL + 0.5), (0.035, 0.035, 0.85), IRON)
    # banners hanging below gallery edge
    cols = [(0.45, 0.15, 0.12), (0.15, 0.25, 0.45), (0.55, 0.45, 0.15), (0.30, 0.12, 0.35), (0.12, 0.35, 0.25)]
    for i in range(5):
        bx = -LEN / 2 + 1.2 + i * (LEN - 2.4) / 4
        bm = mat(f"Banner{i}{sy}", cols[i], 0.9)
        box("Banner", (bx, sy * 9.38, GAL - 1.35), (1.3, 0.05, 1.9), bm)

# ---------- barrel vault (partial, over the vignette length) ----------
import math
def arc_point(a):  # a in radians from vertical
    return (R * math.sin(a), SPRING + R - R * math.cos(a) - (R - 8.4))
# simpler parametric: centre at (y=0, z=SPRING + (R-8.4)) so crown = SPRING+8.4
CZ = SPRING - 2.57  # circle centre height; R chosen so springing at y=+-10.97 -> z=SPRING
R2 = math.hypot(NAVE_HW, SPRING - CZ)
AMAX = math.atan2(NAVE_HW, SPRING - CZ)
# glass surface (grid mesh)
verts, faces = [], []
SEG_A, SEG_X = 14, 5
for i in range(SEG_A + 1):
    a = -AMAX + 2 * AMAX * i / SEG_A
    y = R2 * math.sin(a); z = CZ + R2 * math.cos(a)
    for j in range(SEG_X + 1):
        x = -LEN / 2 + LEN * j / SEG_X
        verts.append((x, y, z))
for i in range(SEG_A):
    for j in range(SEG_X):
        a = i * (SEG_X + 1) + j; b = a + SEG_X + 1
        faces.append((a, b, b + 1, a + 1))
me = bpy.data.meshes.new("VaultGlass"); me.from_pydata(verts, [], faces); me.update()
o = bpy.data.objects.new("VaultGlass", me); bpy.context.collection.objects.link(o); me.materials.append(GLASS)
# ribs along length
for j in range(SEG_X + 1):
    x = -LEN / 2 + LEN * j / SEG_X
    for i in range(SEG_A):
        a0 = -AMAX + 2 * AMAX * i / SEG_A; a1 = -AMAX + 2 * AMAX * (i + 1) / SEG_A
        y0, z0 = R2 * math.sin(a0), CZ + R2 * math.cos(a0)
        y1, z1 = R2 * math.sin(a1), CZ + R2 * math.cos(a1)
        ln = math.hypot(y1 - y0, z1 - z0)
        ang = math.atan2(z1 - z0, y1 - y0)
        box("VaultRib", (x, (y0 + y1) / 2, (z0 + z1) / 2), (0.09, ln, 0.09), IRON, rot=(ang, 0, 0))
# longitudinal purlins
for i in range(0, SEG_A + 1, 2):
    a = -AMAX + 2 * AMAX * i / SEG_A
    y, z = R2 * math.sin(a), CZ + R2 * math.cos(a)
    box("Purlin", (0, y, z), (LEN, 0.07, 0.07), IRON)
# transverse lattice trusses at the two ends
for ex in (-LEN / 2, LEN / 2):
    box("TieBeam", (ex, 0, SPRING + 0.4), (0.18, 2 * NAVE_HW, 0.3), IRON)
    for k in range(9):
        yy = -NAVE_HW + 1.2 + k * (2 * NAVE_HW - 2.4) / 8
        box("TrussDiag", (ex, yy, SPRING + 1.1), (0.07, 1.9, 0.07), IRON, rot=(0.6, 0, 0))
        box("TrussDiag2", (ex, yy, SPRING + 1.1), (0.07, 1.9, 0.07), IRON, rot=(-0.6, 0, 0))

# ---------- exhibits ----------
# lighthouse lens apparatus (left foreground in reference)
lx, ly = -3.6, -5.2
box("LensStand", (lx, ly, 0.9), (1.5, 1.5, 1.8), DARK)
cyl("LensBase", (lx, ly, 2.0), 0.75, 0.4, BRONZE, verts=16)
cyl("LensDrum", (lx, ly, 3.3), 0.85, 2.2, GLASS, verts=18)
for k in range(3):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.86, minor_radius=0.045, location=(lx, ly, 2.5 + k * 0.8))
    t = bpy.context.object; t.name = "LensRing"; t.data.materials.append(BRONZE)
sphere("LensDome", (lx, ly, 4.42), 0.85, GLASS, sy=0.75)
cyl("LensFinial", (lx, ly, 5.25), 0.06, 0.5, BRONZE, verts=8)
box("LensPlinth", (lx, ly, 0.28), (2.0, 2.0, 0.56), RED)

# central ornamental fountain (simplified, gold-painted iron)
fx, fy = 3.4, 1.6
cyl("FountainBasin", (fx, fy, 0.4), 2.1, 0.8, GOLD, verts=20)
cyl("FountainWater", (fx, fy, 0.82), 1.95, 0.05, mat("Water", (0.55, 0.65, 0.70), 0.15), verts=20)
cyl("FountainStem", (fx, fy, 1.7), 0.5, 1.7, GOLD, verts=14)
cyl("FountainTier1", (fx, fy, 2.75), 1.25, 0.35, GOLD, verts=18)
cyl("FountainStem2", (fx, fy, 3.4), 0.30, 1.0, GOLD, verts=12)
cyl("FountainTier2", (fx, fy, 4.05), 0.75, 0.28, GOLD, verts=16)
cyl("FountainCrown", (fx, fy, 4.65), 0.12, 0.9, GOLD, verts=10)
sphere("FountainBall", (fx, fy, 5.25), 0.20, GOLD)

# red plinths with busts
for i, (px, py) in enumerate([(-4.6, -1.2), (-4.6, 0.6), (-1.2, -5.6)]):
    box("Plinth", (px, py, 0.62), (0.62, 0.62, 1.24), RED)
    cyl("BustBase", (px, py, 1.38), 0.16, 0.28, BRONZE, verts=10)
    sphere("BustHead", (px, py, 1.78), 0.17, BRONZE)
    box("BustShoulders", (px, py, 1.55), (0.42, 0.26, 0.22), BRONZE)

# long red display table
box("DisplayTable", (-0.6, -3.2, 0.55), (3.4, 1.2, 1.1), RED)
box("DisplayTableTop", (-0.6, -3.2, 1.14), (3.6, 1.4, 0.08), CREAM)

# dark domed pavilion exhibit (right distance in reference)
gx, gy = 4.9, 5.4
cyl("PavBase", (gx, gy, 0.5), 1.5, 1.0, DARK, verts=16)
for k in range(8):
    a = 2 * math.pi * k / 8
    cyl("PavCol", (gx + 1.35 * math.cos(a), gy + 1.35 * math.sin(a), 1.9), 0.06, 1.9, DARK, verts=8)
sphere("PavDome", (gx, gy, 2.95), 1.55, DARK, sy=0.85)
cyl("PavSpire", (gx, gy, 4.6), 0.03, 1.1, DARK, verts=6, r2=0.09)

# a glass display case
box("Case", (1.8, -5.8, 0.75), (1.9, 0.8, 1.5), WOODF if False else mat("CaseWood", (0.35, 0.22, 0.12), 0.8))
box("CaseGlass", (1.8, -5.8, 1.75), (1.7, 0.65, 0.55), GLASS)

# visitors (stylised, interpretive)
figure("V1", (0.4, -1.4, 0), female=False)
figure("V2", (1.1, -1.7, 0), female=True, coat=(0.30, 0.20, 0.30))
figure("V3", (-1.8, -0.6, 0), female=True, coat=(0.14, 0.22, 0.30))
figure("V4", (3.9, -2.6, 0), female=False)
figure("V5", (-3.9, 2.4, 0), female=True, coat=(0.35, 0.25, 0.15))
figure("V6", (5.6, -0.8, 0), female=False)

# gallery visitors (tiny silhouettes)
for i, gx2 in enumerate((-4.2, -1.0, 2.4)):
    figure(f"G{i}", (gx2, -11.2, GAL + 0.15), female=(i % 2 == 0))

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.ops.object.select_all(action='DESELECT')
tris = sum(len(p.vertices) - 2 for o in bpy.data.objects if o.type == 'MESH' for p in o.data.polygons)
print("TRIANGLES:", tris)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'; scene.cycles.samples = 48; scene.cycles.device = 'CPU'
scene.render.resolution_x = 960; scene.render.resolution_y = 720
scene.world = bpy.data.worlds.new("W"); scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.50, 0.50, 0.50, 1)
bpy.ops.object.light_add(type='SUN', location=(6, -8, 14))
sun = bpy.context.object; sun.data.energy = 2.3; sun.rotation_euler = (math.radians(50), 0, math.radians(35))
bpy.ops.object.light_add(type='AREA', location=(0, 0, 15))
ar = bpy.context.object; ar.data.energy = 900; ar.data.shape = 'DISK'; ar.data.size = 12
bpy.ops.object.camera_add(location=(-17.5, -7.5, 6.8))
cam = bpy.context.object
cam.rotation_euler = (Vector((2.0, 0.5, 4.6)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 40
scene.camera = cam
scene.render.filepath = os.path.join(OUT, "preview.png")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, SLUG + ".blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, SLUG + ".glb"), export_format='GLB')
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
