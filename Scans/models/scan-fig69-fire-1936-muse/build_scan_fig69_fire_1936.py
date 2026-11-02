# Build script: scan-fig69-fire-1936 (Muse version)
# Reference: fig-69_crystal-palace-fire-1936.png
# Night photograph of the Crystal Palace fire (caption prints "20 November
# 1936" - unverified; the fire was 30 November 1936). Burning transept arch
# at screen-left, nave receding, Brunel's south water tower standing lit at
# centre-right, turntable ladder with water jet at screen-right, railings
# and a bare tree in the foreground.
# Conventions: metres, origin at base centre, camera from +Y (screen-left=+X).
# Scale is an estimated excerpt of a far larger building.
import bpy, math, os, random

# clear the default startup scene (cube/camera/light)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
from mathutils import Vector

PKG = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig69-fire-1936"
random.seed(69)

def srgb2lin(c):
    return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c)

def mat(name, srgb, rough=0.9, metal=0.0, emit=None, emit_strength=0.0, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*srgb2lin(srgb), 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit is not None:
        b.inputs["Emission Color"].default_value = (*srgb2lin(emit), 1.0)
        b.inputs["Emission Strength"].default_value = emit_strength
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        m.surface_render_method = 'DITHERED'
    return m

def box(name, loc, dims, material=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    ob = bpy.context.active_object; ob.name = name; ob.dimensions = dims
    if material: ob.data.materials.append(material)
    return ob

def cyl(name, loc, r_top, r_bot, depth, material=None, rot=(0, 0, 0), verts=18):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r_bot, radius2=r_top,
                                    depth=depth, location=loc, rotation=rot)
    ob = bpy.context.active_object; ob.name = name
    if material: ob.data.materials.append(material)
    return ob

def sphere(name, loc, r, material=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=20, ring_count=12)
    ob = bpy.context.active_object; ob.name = name; ob.scale = scale
    if material: ob.data.materials.append(material)
    return ob

def beam(name, p1, p2, w, material):
    p1, p2 = Vector(p1), Vector(p2); mid = (p1 + p2) / 2; d = p2 - p1
    bpy.ops.mesh.primitive_cube_add(location=mid)
    ob = bpy.context.active_object; ob.name = name
    ob.dimensions = (w, w, d.length)
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    if material: ob.data.materials.append(material)
    return ob

# materials
IRON   = mat("iron_dark", (0.10, 0.10, 0.11), 0.7, 0.4)
IRON_L = mat("iron_lit", (0.30, 0.28, 0.27), 0.8, 0.2)
GLASS  = mat("glass_glow", (0.45, 0.38, 0.30), 0.4, 0.0, emit=(1.0, 0.50, 0.14), emit_strength=0.30)
FLAME1 = mat("flame_core", (1.0, 0.34, 0.02), 1.0, 0.0, emit=(1.0, 0.29, 0.01), emit_strength=2.6)
FLAME2 = mat("flame_mid", (1.0, 0.47, 0.05), 1.0, 0.0, emit=(1.0, 0.40, 0.03), emit_strength=1.7)
FLAME3 = mat("flame_tip", (1.0, 0.60, 0.12), 1.0, 0.0, emit=(1.0, 0.52, 0.07), emit_strength=1.15)
SMOKE  = mat("smoke", (0.16, 0.15, 0.15), 1.0, 0.0, alpha=0.28)
WATER  = mat("water_jet", (0.85, 0.90, 0.95), 0.3, 0.0, alpha=0.32)
TOWER_M = mat("tower_masonry_lit", (0.42, 0.40, 0.38), 0.9)
DARKM  = mat("near_black", (0.03, 0.03, 0.035), 1.0)
GROUND = mat("ground_night", (0.095, 0.09, 0.085), 1.0)
BACKDROP = mat("backdrop_night", (0.085, 0.085, 0.098), 1.0)

# ---------- ground & backdrop ----------
box("ground", (0, -2, -0.05), (30, 16, 0.1), GROUND)
box("backdrop", (0, -7.5, 7), (34, 0.2, 16), BACKDROP)

# ---------- the burning building ----------
# Excerpt ~20 m wide: transept arch front at x=+4..+10 (screen-left),
# nave barrel receding toward -X behind it.
BX = 5.5            # transept front plane x-centre offset
# transept arched end: series of arch ribs (half-torus segments approximated
# by beams along an arc) + lattice columns
def arch_rib(name, cx, cy, cz0, R, zbase, material, w=0.14):
    n = 11
    prev = None
    for i in range(n + 1):
        a = math.pi * i / n
        p = (cx, cy, zbase + R * math.sin(a))
        xx = cx + 0  # arch spans in ZY? -> arch in the Y-Z plane is wrong;
        # arch spans across Y (width) rising in Z: point:
        p = (cx, cy - R * math.cos(a) * 0 + (R * math.cos(a)) * 0, 0)
        prev = p
    # simpler: build in X-Z plane at fixed y
    pts = []
    for i in range(n + 1):
        a = math.pi * i / n
        pts.append((cx - R * math.cos(a), cy, zbase + R * math.sin(a)))
    for i in range(n):
        beam(name + "_%d" % i, pts[i], pts[i + 1], w, material)

# NOTE: transept end wall faces the camera (+Y): its arch spans X, rises in Z.
def arch_rib_xz(name, cx, cy, R, zbase, material, w=0.14):
    n = 12; pts = []
    for i in range(n + 1):
        a = math.pi * i / n
        pts.append((cx - R * math.cos(a), cy, zbase + R * math.sin(a)))
    for i in range(n):
        beam("%s_%d" % (name, i), pts[i], pts[i + 1], w, material)

# Transept end at x ~ +6.5 (screen-left), width 9, arch crown ~11.5
arch_rib_xz("transept_arch_outer", 6.5, -1.5, 4.5, 7.0, IRON_L, 0.18)
arch_rib_xz("transept_arch_inner", 6.5, -1.5, 4.0, 7.0, IRON, 0.12)
for sx in (-1, 1):
    box("transept_col", (6.5 + sx * 4.5, -1.5, 3.5), (0.22, 0.22, 7.0), IRON_L)
    box("transept_col2", (6.5 + sx * 3.0, -1.5, 3.0), (0.16, 0.16, 6.0), IRON)
# vertical mullions of the transept end
for i in range(-3, 4):
    box("transept_mull", (6.5 + i * 1.25, -1.5, 3.4), (0.07, 0.07, 6.8), IRON)
# glowing glazing behind the arch (the fire inside)
box("transept_glow", (6.5, -1.75, 5.2), (8.6, 0.1, 10.0), GLASS)

# Nave barrel receding to -X: ribs every 2.2 m, partial (roof partly gone)
for k in range(6):
    x = 1.5 - k * 2.3
    arch_rib_xz("nave_rib_%d" % k, x, -4.5, 4.6, 6.4, IRON if k % 2 else IRON_L, 0.13)
# ridge + purlins
beam("ridge", (2.2, -4.5, 11.05), (-10.5, -4.5, 11.05), 0.16, IRON_L)
for zz, yy in ((8.6, -2.6), (8.6, -6.4)):
    beam("purlin", (2.2, yy, zz), (-10.5, yy, zz), 0.09, IRON)
# lower side wall of nave (arcaded)
for k in range(7):
    box("nave_col", (1.8 - k * 2.0, -0.6, 1.9), (0.18, 0.18, 3.8), IRON_L)
box("nave_wall_glow", (-3.5, -0.75, 1.9), (12.5, 0.08, 3.6), GLASS)

# ---------- flames (stylised layered cones, emissive) ----------
def flame(name, x, y, z, h, r, tilt=(0.0, 0.0)):
    cyl(name + "_a", (x, y, z + h * 0.30), r * 0.52, r, h * 0.6, FLAME1, rot=(tilt[0], tilt[1], 0), verts=10)
    cyl(name + "_b", (x + r * 0.2, y, z + h * 0.55), r * 0.26, r * 0.52, h * 0.55, FLAME2, rot=(tilt[0], tilt[1], 0), verts=10)
    cyl(name + "_c", (x - r * 0.15, y, z + h * 0.82), 0.02, r * 0.24, h * 0.38, FLAME3, rot=(tilt[0], tilt[1], 0), verts=8)

# interior fire inside the transept, just behind the mullions, silhouetted
# against the glowing end wall
for i, (fx, fh, fr) in enumerate(((4.6, 6.5, 0.75), (5.9, 8.0, 0.9), (7.2, 7.0, 0.8),
                                   (8.4, 5.5, 0.65), (6.5, 9.0, 0.7))):
    flame("fl_transept_%d" % i, fx, -1.62, 0.3, fh, fr, tilt=(0.03 * i, 0.02 * i))
# small flames licking along the top of the nave side wall (a visible base)
for i, (fx, fh, fr) in enumerate(((0.8, 1.7, 0.4), (-2.2, 2.1, 0.45), (-5.4, 1.6, 0.38))):
    flame("fl_wall_%d" % i, fx, -0.95, 3.7, fh, fr, tilt=(0.04 * i, -0.03 * i))
# ground fires in front of the nave wall
for i, (fx, fh, fr) in enumerate(((3.0, 3.0, 0.7), (0.8, 2.3, 0.55), (-1.8, 2.7, 0.6),
                                   (8.8, 2.5, 0.6))):
    flame("fl_ground_%d" % i, fx, -1.1, 0.0, fh, fr, tilt=(-0.03 * i, 0.04 * i))

# smoke: soft flattened translucent blobs above the roofline
for i, (sx, sy, sz, sr) in enumerate(((6.5, -3.5, 13.5, 3.2), (2.0, -4.5, 13.0, 2.6),
                                      (-3.0, -5.0, 12.6, 2.8), (8.5, -4.0, 12.2, 2.2),
                                      (4.5, -2.5, 12.8, 2.0))):
    sphere("smoke_%d" % i, (sx, sy, sz), sr, SMOKE, scale=(1.5, 0.8, 0.55))

# ---------- Brunel water tower (standing, centre-right of frame) ----------
TX, TY = -4.2, -6.2
cyl("tower_shaft", (TX, TY, 5.0), 1.55, 1.75, 10.0, TOWER_M, verts=24)
for lvl in range(4):
    for i in range(8):
        a = 2 * math.pi * i / 8
        box("tower_window", (TX + 1.62 * math.sin(a), TY + 1.62 * math.cos(a), 2.2 + lvl * 2.1),
            (0.5, 0.08, 1.1), DARKM, rot=(0, 0, -a))
cyl("tower_belt", (TX, TY, 10.1), 1.95, 1.8, 0.5, TOWER_M, verts=24)
for i in range(10):  # arcaded top stage: small columns
    a = 2 * math.pi * i / 10
    box("tower_top_col", (TX + 1.78 * math.sin(a), TY + 1.78 * math.cos(a), 11.3),
        (0.16, 0.16, 1.9), TOWER_M)
cyl("tower_top_ring", (TX, TY, 12.35), 1.95, 1.95, 0.3, TOWER_M, verts=24)
cyl("tower_cap", (TX, TY, 13.6), 0.25, 1.9, 2.2, mat("tower_cap_dark", (0.16, 0.15, 0.16), 0.9), verts=24)
sphere("tower_finial", (TX, TY, 14.85), 0.22, TOWER_M)

# ---------- firefighting at screen-right ----------
# turntable ladder raised against the building, at x ~ -8.5 (screen-right)
LX, LY = -8.6, 1.2
box("ladder_base", (LX, LY, 0.55), (1.5, 0.9, 1.1), IRON)
for s in (-1, 1):
    beam("ladder_rail", (LX + s * 0.22, LY, 1.0), (LX - 2.6 + s * 0.22, LY - 0.6, 10.6), 0.09, IRON_L)
for i in range(9):
    t = i / 8
    beam("ladder_rung", (LX - 2.6 * t - 0.22, LY - 0.6 * t, 1.0 + 9.6 * t),
         (LX - 2.6 * t + 0.22, LY - 0.6 * t, 1.0 + 9.6 * t), 0.05, IRON_L)
# water jet: tapering translucent cone from ladder head toward the nave wall
beam("water_jet", (LX - 2.6, LY - 0.6, 10.6), (-1.0, -1.0, 8.2), 0.10, WATER)
# two firemen silhouettes at the ladder base + one with a hose line
def fireman(name, x, y, h=1.75):
    cyl(name + "_legs", (x, y, 0.42 * h / 1.75 * 1.75 / 2), 0.09, 0.11, 0.8, DARKM)
    cyl(name + "_body", (x, y, 1.15), 0.13, 0.16, 0.65, DARKM)
    sphere(name + "_head", (x, y, 1.62), 0.11, DARKM)
    cyl(name + "_helmet", (x, y, 1.70), 0.13, 0.15, 0.07, IRON_L)
fireman("fireman1", -7.6, 1.7)
fireman("fireman2", -9.4, 0.6)
fireman("fireman3", -6.4, -0.6)

# lamp post (seen in photo, right of centre foreground)
cyl("lamp_post", (-5.6, 2.6, 2.2), 0.05, 0.07, 4.4, IRON)
sphere("lamp_head", (-5.6, 2.6, 4.55), 0.16, mat("lamp_glow", (0.95, 0.92, 0.85), 0.4, 0.0,
                                                 emit=(1.0, 0.95, 0.85), emit_strength=2.5))

# ---------- foreground: railings, gate, bare tree ----------
for i in range(26):
    x = -3.4 + i * 0.34
    if 1.2 < x < 2.6:   # gate opening
        continue
    box("rail_bar", (x, 3.4, 0.55), (0.035, 0.035, 1.1), IRON)
box("rail_top", (0.9, 3.4, 1.12), (9.6, 0.05, 0.05), IRON)
for gx in (1.2, 2.6):
    box("gate_post", (gx, 3.4, 0.6), (0.09, 0.09, 1.2), IRON)
box("gate_frame", (1.9, 3.4, 0.58), (1.35, 0.04, 1.05), IRON)
# bare winter tree at screen-left foreground
TX2, TY2 = 9.6, 2.2
beam("tree_trunk", (TX2, TY2, 0), (TX2 - 0.15, TY2, 3.4), 0.30, DARKM)
for i, (dx, dy, dz, ln) in enumerate((( -1.6, 0.2, 5.6, 2.6), (1.4, -0.2, 5.9, 2.4),
                                      (-0.5, 0.4, 6.4, 2.2), (0.9, 0.3, 6.8, 1.9),
                                      (-2.2, -0.3, 4.6, 2.0))):
    base = (TX2 - 0.15, TY2, 3.4)
    beam("tree_branch_%d" % i, base, (base[0] + dx, base[1] + dy, dz), 0.09, DARKM)
    beam("tree_twig_%d" % i, (base[0] + dx, base[1] + dy, dz),
         (base[0] + dx * 1.5, base[1] + dy * 1.6, dz + ln * 0.45), 0.045, DARKM)

# ---------- scene / lights / camera ----------
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 48
sc.cycles.use_denoising = True
sc.render.resolution_x = 960; sc.render.resolution_y = 700
w = sc.world; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (*srgb2lin((0.05, 0.05, 0.062)), 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
sc.view_settings.exposure = 0.3

def point(name, loc, energy, color, radius=0.4):
    d = bpy.data.lights.new(name, 'POINT'); d.energy = energy; d.color = color
    d.shadow_soft_size = radius
    o = bpy.data.objects.new(name, d); sc.collection.objects.link(o); o.location = loc
    return o
point("fire_glow_main", (6.0, 0.5, 6.0), 2400, (1.0, 0.52, 0.20), 2.5)
point("fire_glow_nave", (-3.0, -0.5, 5.0), 1300, (1.0, 0.48, 0.18), 2.0)
point("lamp_light", (-5.6, 2.6, 4.5), 450, (1.0, 0.95, 0.85), 0.5)
point("tower_glow", (-3.5, 5.0, 8.0), 1100, (1.0, 0.60, 0.25), 1.5)
d = bpy.data.lights.new("moon_fill", 'SUN'); d.energy = 0.55; d.color = (0.7, 0.78, 1.0)
o = bpy.data.objects.new("moon_fill", d); sc.collection.objects.link(o)
o.rotation_euler = (math.radians(50), 0, math.radians(-30))

cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 35; cam_d.clip_end = 200
cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam)
cam.location = (1.8, 25.5, 9.3)
cam.rotation_mode = 'QUATERNION'
cam.rotation_quaternion = (Vector((-0.2, -1.8, 4.9)) - cam.location).to_track_quat('-Z', 'Y')
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
