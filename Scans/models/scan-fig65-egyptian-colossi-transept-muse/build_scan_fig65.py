# scan-fig65-egyptian-colossi-transept — North transept, Sydenham: Egyptian colossi, sphinx avenue, palms
# Reference: fig-65_north-transept-egyptian-colossi-sydenham.png
# Colossi/sphinxes are LARGE STYLISED temple figures (abstracted monumental forms, not detailed sculpture).
import bpy, math, os
from mathutils import Vector

SLUG = "scan-fig65-egyptian-colossi-transept"
OUT = os.path.dirname(os.path.abspath(__file__))

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

def sphere(name, loc, r, material=None, sc=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=14, ring_count=10)
    o = bpy.context.object; o.name = name; o.scale = sc
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material: o.data.materials.append(material)
    return o

def figure(name, loc, female=True, coat=(0.16, 0.14, 0.13), s=1.0):
    x, y, z = loc
    mc = mat("Coat" + name, coat, 0.9); sk = mat("Skin", (0.76, 0.58, 0.46), 0.7)
    if female:
        cyl(name + "_skirt", (x, y, z + 0.48 * s), 0.40 * s, 0.96 * s, mc, verts=12, r2=0.15 * s)
        cyl(name + "_bodice", (x, y, z + 1.13 * s), 0.155 * s, 0.36 * s, mc, verts=12, r2=0.13 * s)
    else:
        box(name + "_legs", (x, y, z + 0.42 * s), (0.26 * s, 0.17 * s, 0.84 * s), mat("Trou", (0.23, 0.21, 0.19), 0.9))
        cyl(name + "_coat", (x, y, z + 1.12 * s), 0.20 * s, 0.62 * s, mc, verts=12, r2=0.165 * s)
    sphere(name + "_head", (x, y, z + 1.56 * s), 0.105 * s, sk)
    if female: cyl(name + "_bonnet", (x, y, z + 1.63 * s), 0.115 * s, 0.07 * s, mc, verts=12)
    else:
        cyl(name + "_hatbrim", (x, y, z + 1.635 * s), 0.16 * s, 0.02 * s, mc, verts=14)
        cyl(name + "_hat", (x, y, z + 1.74 * s), 0.105 * s, 0.19 * s, mc, verts=14)

clean()
STONE = mat("ColossusStone", (0.72, 0.62, 0.45), 0.95)
STONE2 = mat("SphinxStone", (0.60, 0.48, 0.33), 0.95)
STONED = mat("StoneDark", (0.50, 0.40, 0.27), 0.95)
WOODF = mat("FloorBoards", (0.52, 0.38, 0.22), 0.9)
IRON = mat("IronPainted", (0.34, 0.33, 0.29), 0.6, 0.2)
GLASS = mat("Glass", (0.78, 0.84, 0.86), 0.12, 0.0, alpha=0.32)
PALMG = mat("PalmGreen", (0.25, 0.38, 0.18), 0.9)
PALMT = mat("PalmTrunk", (0.40, 0.30, 0.18), 0.95)
WHITE = mat("CrownWhite", (0.85, 0.82, 0.75), 0.85)

# floor (boarded)
box("Floor", (0, 0, -0.09), (30, 22, 0.18), WOODF)
# raised platform for colossi
box("Platform", (0, 6.4, 0.35), (11.5, 3.4, 0.7), STONED)
box("PlatformStep", (0, 4.4, 0.17), (9.0, 0.9, 0.34), STONED)
# patterned front band of platform (simplified blocks)
for i in range(11):
    box("PlatBand", (-5.0 + i * 1.0, 4.72, 0.5), (0.55, 0.06, 0.4), STONE)

# ---------- seated colossus (stylised) ----------
def colossus(name, cx, cy, H=7.6):
    s = H / 7.6
    box(name + "_plinth", (cx, cy, 0.7 + 0.45 * s), (3.0 * s, 2.6 * s, 0.9 * s), STONED)
    bz = 0.7 + 0.9 * s  # base top
    # seat block
    box(name + "_seat", (cx, cy + 0.25 * s, bz + 0.8 * s), (2.5 * s, 2.0 * s, 1.6 * s), STONE)
    # lower legs (vertical, front)
    for sx in (-1, 1):
        box(name + "_shin", (cx + sx * 0.62 * s, cy - 0.95 * s, bz + 0.75 * s), (0.62 * s, 0.5 * s, 1.5 * s), STONE)
        box(name + "_foot", (cx + sx * 0.62 * s, cy - 1.35 * s, bz + 0.14 * s), (0.62 * s, 1.15 * s, 0.28 * s), STONE)
        # thighs (horizontal)
        box(name + "_thigh", (cx + sx * 0.62 * s, cy - 0.55 * s, bz + 1.62 * s), (0.62 * s, 1.6 * s, 0.55 * s), STONE)
    # torso (broad, slightly tapered block)
    cyl(name + "_torso", (cx, cy + 0.15 * s, bz + 2.85 * s), 1.18 * s, 2.5 * s, STONE, verts=4, rot=(0, 0, math.radians(45)), r2=1.42 * s)
    # arms along sides, close to torso
    for sx in (-1, 1):
        box(name + "_arm", (cx + sx * 1.30 * s, cy - 0.05 * s, bz + 2.65 * s), (0.40 * s, 0.55 * s, 2.0 * s), STONE, rot=(0.10, 0, 0))
    # nemes headdress: flared slab behind/beside head
    box(name + "_nemes", (cx, cy + 0.34 * s, bz + 4.75 * s), (1.95 * s, 0.95 * s, 1.55 * s), STONE2)
    # head
    sphere(name + "_head", (cx, cy - 0.16 * s, bz + 4.95 * s), 0.64 * s, STONE, sc=(0.82, 0.9, 1.12))
    box(name + "_brow", (cx, cy - 0.72 * s, bz + 5.12 * s), (0.98 * s, 0.18 * s, 0.22 * s), STONE2)
    # tall crown (hedjet-like) with disc, as shown — seated on the head
    cyl(name + "_crown", (cx, cy + 0.08 * s, bz + 5.95 * s), 0.28 * s, 1.25 * s, WHITE, verts=12, r2=0.44 * s)
    sphere(name + "_disc", (cx, cy + 0.08 * s, bz + 6.62 * s), 0.20 * s, STONE2)
    # small standing statue between the legs (as in the view) — plain stone figure
    box(name + "_attendant", (cx, cy - 1.12 * s, bz + 0.85 * s), (0.42 * s, 0.30 * s, 1.7 * s), STONE2)
    sphere(name + "_atthead", (cx, cy - 1.12 * s, bz + 1.85 * s), 0.17 * s, STONE2)

colossus("ColossusL", -2.35, 6.6)
colossus("ColossusR", 2.35, 6.6)

# ---------- sphinx (stylised) ----------
def sphinx(name, cx, cy, L=4.4, facing=-1):
    s = L / 4.4
    box(name + "_plinth", (cx, cy, 0.28 * s), (1.5 * s, L * 0.98, 0.56 * s), STONED)
    bz = 0.56 * s
    # lion body
    body = box(name + "_body", (cx, cy + 0.1 * s, bz + 0.75 * s), (1.25 * s, L * 0.78, 1.35 * s), STONE2)
    # haunch rise at rear
    box(name + "_haunch", (cx, cy + L * 0.30 * s, bz + 0.95 * s), (1.3 * s, L * 0.25, 1.6 * s), STONE2)
    # front paws extending forward
    fy = cy - facing * 0  # paws toward -Y (front)
    for sx in (-1, 1):
        box(name + "_paw", (cx + sx * 0.33 * s, cy - L * 0.44, bz + 0.22 * s), (0.42 * s, L * 0.30, 0.44 * s), STONE2)
    # chest
    box(name + "_chest", (cx, cy - L * 0.33, bz + 1.05 * s), (1.05 * s, 0.5 * s, 1.7 * s), STONE2)
    # nemes + head
    box(name + "_nemes", (cx, cy - L * 0.36, bz + 2.15 * s), (1.15 * s, 0.62 * s, 1.15 * s), STONED)
    sphere(name + "_head", (cx, cy - L * 0.47, bz + 2.30 * s), 0.42 * s, STONE2, sc=(0.85, 0.9, 1.1))

sphinx("SphinxL1", -6.5, -5.0, 4.6)
sphinx("SphinxL2", -6.9, -0.2, 4.2)
sphinx("SphinxL3", -7.2, 4.2, 3.9)
sphinx("SphinxR1", 6.6, -4.2, 4.4)
sphinx("SphinxR2", 7.0, 0.6, 4.0)

# ---------- palms ----------
def palm(name, cx, cy, H=6.8):
    seg = 5
    px, py = cx, cy
    for i in range(seg):
        z = H * (i + 0.5) / seg
        off = 0.35 * (i / seg) ** 2
        cyl(name + f"_trunk{i}", (px + off, py, z), 0.16 - 0.015 * i, H / seg + 0.1, PALMT, verts=9)
        px += 0.0
    tx, ty, tz = cx + 0.35, cy, H
    for k in range(9):
        a = 2 * math.pi * k / 9 + 0.3
        dx, dy = math.cos(a), math.sin(a)
        # frond: thin box whose long axis (+Y) tracks an outward, slightly rising direction
        from mathutils import Vector as _V
        dirv = _V((dx * 0.82, dy * 0.82, 0.42)).normalized()
        cen = _V((tx, ty, tz)) + dirv * 1.15
        o = box(name + f"_frond{k}", tuple(cen), (0.17, 2.4, 0.03), PALMG)
        o.rotation_euler = dirv.to_track_quat('Y', 'Z').to_euler()

palm("PalmL1", -5.6, 3.4, 7.2)
palm("PalmL2", -6.4, -0.8, 6.2)
palm("PalmR1", 5.8, 3.0, 7.0)
palm("PalmR2", 6.6, -1.4, 6.0)

# ---------- transept vault (partial section) + end fan ----------
CZ = 3.5; RW = 15.0
AMAX = math.asin(min(1.0, 12.8 / RW))
verts, faces = [], []
SEG_A, SEG_X = 16, 5
for i in range(SEG_A + 1):
    a = -AMAX + 2 * AMAX * i / SEG_A
    y = RW * math.sin(a); z = CZ + RW * math.cos(a)
    verts.append((-9.0, y, z)); verts.append((9.0, y, z))
for i in range(SEG_A):
    a0 = i * 2; faces.append((a0, a0 + 2, a0 + 3, a0 + 1))
me = bpy.data.meshes.new("VaultGlass"); me.from_pydata(verts, [], faces); me.update()
o = bpy.data.objects.new("VaultGlass", me); bpy.context.collection.objects.link(o); me.materials.append(GLASS)
for j, xx in enumerate((-9.0, -4.5, 0.0, 4.5, 9.0)):
    for i in range(SEG_A):
        a0 = -AMAX + 2 * AMAX * i / SEG_A; a1 = -AMAX + 2 * AMAX * (i + 1) / SEG_A
        y0, z0 = RW * math.sin(a0), CZ + RW * math.cos(a0)
        y1, z1 = RW * math.sin(a1), CZ + RW * math.cos(a1)
        ln = math.hypot(y1 - y0, z1 - z0); ang = math.atan2(z1 - z0, y1 - y0)
        box("VaultRib", (xx, (y0 + y1) / 2, (z0 + z1) / 2), (0.15, ln, 0.15), IRON, rot=(ang, 0, 0))
for i in range(0, SEG_A + 1, 2):
    a = -AMAX + 2 * AMAX * i / SEG_A
    y, z = RW * math.sin(a), CZ + RW * math.cos(a)
    box("Purlin", (0, y, z), (18.0, 0.08, 0.08), IRON)
# end fan window behind colossi (semicircle + radial bars), in the XZ end plane
fy = 9.4; FCZ = 13.2; FR = 5.2
bpy.ops.mesh.primitive_circle_add(vertices=28, radius=FR, fill_type='NGON', location=(0, fy, FCZ))
fan = bpy.context.object; fan.name = "FanGlass"; fan.rotation_euler = (math.pi / 2, 0, 0)
fan.data.materials.append(GLASS)
for k in range(7):
    a = math.pi * (k + 0.5) / 7
    cen = (FR * 0.5 * math.cos(a), fy - 0.02, FCZ + FR * 0.5 * math.sin(a))
    box("FanBar", cen, (FR * 0.96, 0.05, 0.09), IRON, rot=(0, -a, 0))
# chord bar across the fan diameter + rim segments along the semicircle
box("FanChord", (0, fy - 0.02, FCZ), (2 * FR, 0.06, 0.12), IRON)
for k in range(10):
    a0 = math.pi * k / 10; a1 = math.pi * (k + 1) / 10
    y0, z0 = FR * math.cos(a0), FCZ + FR * math.sin(a0)
    y1, z1 = FR * math.cos(a1), FCZ + FR * math.sin(a1)
    ln = math.hypot(y1 - y0, z1 - z0); ang = math.atan2(z1 - z0, y1 - y0)
    box("FanRimSeg", ((y0 + y1) / 2, fy - 0.02, (z0 + z1) / 2), (ln, 0.06, 0.12), IRON, rot=(0, -ang, 0))
# side gallery hint (right)
box("GallerySlab", (11.8, 0, 8.2), (3.4, 16, 0.3), IRON)
for i in range(3):
    cyl("GalCol", (11.8, -6 + i * 6, 4.1), 0.13, 8.2, IRON, verts=10)

# visitors
figure("V1", (-0.8, -4.6, 0), female=True, coat=(0.30, 0.22, 0.30))
figure("V2", (-1.9, -4.2, 0), female=False)
figure("V3", (1.4, -5.2, 0), female=False)
figure("V4", (2.5, -4.8, 0), female=True, coat=(0.16, 0.24, 0.34))
figure("V5", (-3.8, -2.6, 0), female=False)
figure("V6", (4.4, -3.0, 0), female=True, coat=(0.38, 0.28, 0.16))

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
bpy.ops.object.light_add(type='SUN', location=(6, -10, 16))
sun = bpy.context.object; sun.data.energy = 2.8; sun.rotation_euler = (math.radians(48), 0, math.radians(30))
bpy.ops.object.light_add(type='AREA', location=(0, -4, 14))
ar = bpy.context.object; ar.data.energy = 1000; ar.data.shape = 'DISK'; ar.data.size = 12
bpy.ops.object.camera_add(location=(0, -20.5, 4.2))
cam = bpy.context.object
cam.rotation_euler = (Vector((0, 3.0, 4.8)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 40
scene.camera = cam
scene.render.filepath = os.path.join(OUT, "preview.png")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, SLUG + ".blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, SLUG + ".glb"), export_format='GLB')
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
