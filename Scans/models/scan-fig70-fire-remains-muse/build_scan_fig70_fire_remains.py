# Build script: scan-fig70-fire-remains (Muse version)
# Reference: fig-70_crystal-palace-remains-after-fire.png
# Daylight photograph across the wreckage: rubble field and twisted girders
# in the foreground, charred standing columns, a leaning girder ramp at
# centre, skeletal framework at mid-right, the surviving transept barrel
# vault skeleton at back-left, and Brunel's north water tower standing
# intact in the centre background (it IS visible in this photograph).
# Conventions: metres, origin at base centre, camera from +Y (screen-left=+X).
# Somber grey palette. Scale: estimated excerpt of a much larger site.
import bpy, math, os, random

# clear the default startup scene (cube/camera/light)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
from mathutils import Vector

PKG = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig70-fire-remains"
random.seed(70)

def srgb2lin(c):
    return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c)

def mat(name, srgb, rough=0.95, metal=0.1):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*srgb2lin(srgb), 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m

def box(name, loc, dims, material=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    ob = bpy.context.active_object; ob.name = name; ob.dimensions = dims
    if material: ob.data.materials.append(material)
    return ob

def cyl(name, loc, r_top, r_bot, depth, material=None, rot=(0, 0, 0), verts=16):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r_bot, radius2=r_top,
                                    depth=depth, location=loc, rotation=rot)
    ob = bpy.context.active_object; ob.name = name
    if material: ob.data.materials.append(material)
    return ob

def sphere(name, loc, r, material=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=16, ring_count=10)
    ob = bpy.context.active_object; ob.name = name; ob.scale = scale
    if material: ob.data.materials.append(material)
    return ob

def beam(name, p1, p2, w, material, w2=None):
    p1, p2 = Vector(p1), Vector(p2); mid = (p1 + p2) / 2; d = p2 - p1
    bpy.ops.mesh.primitive_cube_add(location=mid)
    ob = bpy.context.active_object; ob.name = name
    ob.dimensions = (w, w2 if w2 else w, d.length)
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    if material: ob.data.materials.append(material)
    return ob

CHAR  = mat("charred_iron", (0.09, 0.085, 0.09), 0.85, 0.35)
RUST  = mat("rusted_iron", (0.23, 0.16, 0.12), 0.9, 0.2)
PALE  = mat("pale_burnt_metal", (0.52, 0.50, 0.48), 0.85, 0.15)
RUB1  = mat("rubble_dark", (0.16, 0.15, 0.15), 1.0, 0.0)
RUB2  = mat("rubble_mid", (0.30, 0.28, 0.27), 1.0, 0.0)
RUB3  = mat("rubble_light", (0.44, 0.42, 0.40), 1.0, 0.0)
GROUND= mat("ash_ground", (0.35, 0.33, 0.32), 1.0, 0.0)
TOWER = mat("tower_stone_pale", (0.62, 0.60, 0.57), 0.95, 0.0)
DARK  = mat("void_dark", (0.05, 0.05, 0.05), 1.0, 0.0)

box("ground", (0, -6, -0.06), (76, 46, 0.12), GROUND)

# ---------- rubble field ----------
for i in range(52):
    x = random.uniform(-11, 11); y = random.uniform(3.2, -4.5)
    m = random.choice((RUB1, RUB2, RUB3))
    r = random.uniform(0.28, 0.8)
    sphere("rubble_%d" % i, (x, y, r * 0.10), r, m, scale=(1.35, 1.0, 0.34))
for i in range(24):  # angular chunks among the mounds
    x = random.uniform(-10.5, 10.5); y = random.uniform(3.0, -4.2)
    box("rubble_chunk_%d" % i, (x, y, random.uniform(0.05, 0.22)),
        (random.uniform(0.4, 1.3), random.uniform(0.3, 0.9), random.uniform(0.15, 0.45)),
        random.choice((RUB1, RUB2, RUB3)),
        rot=(random.uniform(-0.35, 0.35), random.uniform(-0.3, 0.3), random.uniform(0, 3.1)))
for i in range(26):  # scattered twisted beams in the debris
    x = random.uniform(-10, 10); y = random.uniform(2.8, -4.0)
    a = random.uniform(0, math.pi); ln = random.uniform(0.8, 2.6)
    dz = random.uniform(-0.25, 0.35)
    beam("debris_beam_%d" % i, (x, y, 0.15),
         (x + ln * math.cos(a), y + ln * math.sin(a) * 0.4, 0.15 + dz),
         random.uniform(0.05, 0.12), random.choice((CHAR, RUST)))
for i in range(8):  # bent sheet plates
    x = random.uniform(-9, 9); y = random.uniform(2.5, -3.5)
    box("debris_plate_%d" % i, (x, y, 0.28), (random.uniform(0.7, 1.6), random.uniform(0.5, 1.0), 0.05),
        random.choice((CHAR, RUST, PALE)),
        rot=(random.uniform(-0.4, 0.4), random.uniform(-0.3, 0.3), random.uniform(0, 3)))

# ---------- charred standing columns (foreground rank) ----------
def column(name, x, y, h, material, lean=0.0, capital=True):
    top = (x + lean, y, h)
    beam(name, (x, y, 0), top, 0.20, material)
    if capital:
        box(name + "_cap", (top[0], top[1], h + 0.12), (0.42, 0.42, 0.24), material)
    box(name + "_base", (x, y, 0.18), (0.4, 0.4, 0.36), material)

column("col_fg_L", 7.6, 1.6, 6.4, PALE, lean=-0.15)          # tall pale column, left foreground
column("col_fg_L2", 6.2, -0.6, 4.4, CHAR, lean=0.1, capital=False)
column("col_mid_1", 2.8, -1.8, 5.2, CHAR, lean=0.35)
column("col_mid_2", 0.6, -2.2, 6.8, CHAR, lean=-0.2, capital=False)
column("col_mid_3", -2.4, -2.0, 5.6, RUST, lean=0.15)
# rank of shorter white-painted-looking columns at screen-right
for i in range(4):
    column("col_R_%d" % i, -6.4 - i * 1.15, -1.4 - i * 0.35, 3.1 - i * 0.15, PALE, capital=False)
# two very tall thin masts at centre-right (as in photo)
beam("mast_1", (-3.9, -3.4, 0), (-3.7, -3.4, 10.5), 0.14, CHAR)
beam("mast_2", (-5.6, -3.6, 0), (-5.9, -3.6, 9.0), 0.13, CHAR)
beam("mast_cross", (-5.8, -3.55, 8.2), (-2.2, -3.3, 8.2), 0.08, CHAR)

# ---------- leaning girder ramp at centre ----------
beam("ramp_girder", (5.4, 0.4, 3.1), (-1.8, -0.8, 0.35), 0.34, RUST, w2=0.16)
beam("ramp_girder2", (5.0, -0.9, 2.7), (-2.2, -1.9, 0.3), 0.26, CHAR, w2=0.13)
for i in range(7):  # wreckage ribs sticking off the ramp
    t = i / 6
    bx = 5.4 + (-1.8 - 5.4) * t; by = 0.4 + (-0.8 - 0.4) * t; bz = 3.1 + (0.35 - 3.1) * t
    beam("ramp_rib_%d" % i, (bx, by, bz), (bx + random.uniform(-0.3, 0.3), by - 0.5, bz - 0.8), 0.06, CHAR)

# ---------- skeletal framework, mid-right ----------
FX, FY = -4.6, -4.6
for dx in (-1.8, 1.8):
    for dy in (-1.2, 1.2):
        beam("frame_post", (FX + dx, FY + dy, 0), (FX + dx, FY + dy, 4.6), 0.15, CHAR)
for zz in (2.3, 4.6):
    beam("frame_beam_a", (FX - 1.8, FY - 1.2, zz), (FX + 1.8, FY - 1.2, zz), 0.12, CHAR)
    beam("frame_beam_b", (FX - 1.8, FY + 1.2, zz), (FX + 1.8, FY + 1.2, zz), 0.12, CHAR)
    beam("frame_beam_c", (FX - 1.8, FY - 1.2, zz), (FX - 1.8, FY + 1.2, zz), 0.12, RUST)
    beam("frame_beam_d", (FX + 1.8, FY - 1.2, zz), (FX + 1.8, FY + 1.2, zz), 0.12, RUST)
beam("frame_diag", (FX - 1.8, FY - 1.2, 0.2), (FX + 1.8, FY - 1.2, 4.4), 0.08, CHAR)
# bent arch stubs at right (collapsed nave ribs)
for i in range(3):
    x = -8.6 - i * 0.9
    pts = [(x, -3.2, 0), (x - 0.3, -3.6, 1.8), (x - 1.3, -4.0, 2.9), (x - 2.6, -4.3, 2.4)]
    for j in range(3):
        beam("bent_rib_%d_%d" % (i, j), pts[j], pts[j + 1], 0.10, RUST)

# ---------- surviving transept vault skeleton, back-left ----------
VX, VY = 7.8, -7.6
def arch_xz(name, cx, cy, R, zbase, material, w=0.13, n=12, squash=1.0):
    pts = []
    for i in range(n + 1):
        a = math.pi * i / n
        pts.append((cx - R * math.cos(a), cy, zbase + R * math.sin(a) * squash))
    for i in range(n):
        beam("%s_%d" % (name, i), pts[i], pts[i + 1], w, material)
for k in range(5):  # repeated barrel ribs receding
    arch_xz("vault_rib_%d" % k, VX, VY - k * 0.0, 4.4, 4.6, CHAR if k % 2 else PALE, 0.12)
    VX -= 1.9
beam("vault_ridge", (9.6, -7.6, 9.0), (1.5, -7.6, 9.0), 0.14, CHAR)
for sx in (-1, 1):
    for k in range(4):
        box("vault_col", (7.8 - k * 1.9 + sx * 4.4, -7.6, 2.3), (0.16, 0.16, 4.6), CHAR)
box("vault_end_dark", (8.4, -8.7, 4.2), (7.6, 0.15, 7.8), mat("void_mid", (0.13, 0.13, 0.13), 1.0, 0.0))  # dark hollow of the far end

# ---------- Brunel north water tower, standing intact, centre background ----------
TX, TY = -1.4, -9.3
cyl("tower_shaft", (TX, TY, 5.2), 1.6, 1.85, 10.4, TOWER, verts=24)
for lvl in range(4):
    for i in range(8):
        a = 2 * math.pi * i / 8
        box("tower_win", (TX + 1.72 * math.sin(a), TY + 1.72 * math.cos(a), 2.4 + lvl * 2.15),
            (0.48, 0.08, 1.05), DARK, rot=(0, 0, -a))
cyl("tower_belt", (TX, TY, 10.6), 2.0, 1.85, 0.5, TOWER, verts=24)
cyl("tower_cap", (TX, TY, 12.3), 0.3, 1.95, 2.9, mat("tower_cap", (0.45, 0.43, 0.42), 0.95), verts=24)
sphere("tower_finial", (TX, TY, 13.95), 0.2, TOWER)

# ---------- scene / lights / camera ----------
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 48
sc.cycles.use_denoising = True
sc.render.resolution_x = 960; sc.render.resolution_y = 720
w = sc.world; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (*srgb2lin((0.80, 0.80, 0.79)), 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0

d = bpy.data.lights.new("overcast", 'SUN'); d.energy = 2.7; d.color = (0.95, 0.95, 0.97)
o = bpy.data.objects.new("overcast", d); sc.collection.objects.link(o)
o.rotation_euler = (math.radians(55), math.radians(8), math.radians(-35))
d2 = bpy.data.lights.new("sky_fill", 'SUN'); d2.energy = 0.5; d2.color = (0.85, 0.88, 1.0)
o2 = bpy.data.objects.new("sky_fill", d2); sc.collection.objects.link(o2)
o2.rotation_euler = (math.radians(120), 0, math.radians(40))

cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 33; cam_d.clip_end = 200
cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam)
cam.location = (1.5, 26.0, 6.2)
cam.rotation_mode = 'QUATERNION'
cam.rotation_quaternion = (Vector((0.2, -3.0, 2.8)) - cam.location).to_track_quat('-Z', 'Y')
sc.camera = cam

for ob in bpy.data.objects:
    if ob.type == 'MESH':
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        ob.select_set(False)

tris = 0
for ob in bpy.data.objects:
    if ob.type == 'MESH':
        ob.data.calc_loop_triangles()
        tris += len(ob.data.loop_triangles)
print("TRIANGLES:", tris)

sc.render.filepath = os.path.join(PKG, "preview.png")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(PKG, SLUG + ".blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(PKG, SLUG + ".glb"), export_format='GLB')
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
