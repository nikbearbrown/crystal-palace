#!/usr/bin/env python3
"""Build scan-fig61-at-the-opera: "The Opera" cartoon (Punch, 1851) —
'crossing boundaries: dressing and undressing'. A grand salon/reception room:
chandelier, arched opening, a long table down the middle, and a receiving line
of visitors in hugely varied national and evening dress. As drawn it is a
standing reception, NOT an opera box; the model follows the image.
Blender 4.5.3, metres, origin at base centre. Re-runnable:
  blender -b --python build_scan_fig61_opera.py
Outputs .blend, .glb, preview.png beside this script. No lettering; figures
stylised, no caricature exaggeration, no facial features."""
import bpy, math, os
from mathutils import Vector, Matrix

# ---------- scene reset ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# ---------- materials (sRGB -> linear conversion applied) ----------
def _lin(v):
    return ((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92

def mat(name, srgb, rough=0.75, metal=0.0, alpha=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    r, g, bl = (_lin(c) for c in srgb)
    b.inputs["Base Color"].default_value = (r, g, bl, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if alpha is not None:
        b.inputs["Alpha"].default_value = alpha
        m.surface_render_method = 'DITHERED'
    return m

SKIN  = mat("SkinTone", (0.90, 0.68, 0.53), 0.65)
HAIR_D = mat("HairDark", (0.16, 0.11, 0.08), 0.8)
BLACK = mat("CoatBlack", (0.045, 0.045, 0.055), 0.8)
CHARC = mat("Charcoal", (0.13, 0.13, 0.14), 0.85)
CREAM = mat("WaistcoatCream", (0.90, 0.84, 0.68), 0.8)
WHITE = mat("WhiteCloth", (0.93, 0.92, 0.88), 0.85)
PALE  = mat("PaleDress", (0.84, 0.80, 0.72), 0.9)
PINK  = mat("DressPink", (0.82, 0.62, 0.60), 0.9)
BLUE  = mat("DressBlue", (0.16, 0.26, 0.48), 0.85)
BURG  = mat("DressBurgundy", (0.32, 0.07, 0.11), 0.85)
GREEN = mat("DressGreen", (0.13, 0.28, 0.16), 0.85)
RED   = mat("GuardRed", (0.50, 0.08, 0.08), 0.8)
GOLD  = mat("Gilt", (0.85, 0.62, 0.20), 0.35, 0.85)
BRASS = mat("Brass", (0.70, 0.50, 0.22), 0.4, 0.8)
FUR   = mat("FurCream", (0.88, 0.83, 0.72), 1.0)
CLOAK = mat("CloakPattern", (0.78, 0.66, 0.42), 0.95)
CLOAK_D = mat("CloakPatternDark", (0.45, 0.25, 0.16), 0.95)
WALL  = mat("WallCream", (0.86, 0.82, 0.74), 0.95)
WALL_D = mat("WallPanel", (0.78, 0.73, 0.64), 0.95)
DARKIN = mat("DarkInterior", (0.12, 0.10, 0.09), 1.0)
WOOD_M = mat("WoodMid", (0.45, 0.30, 0.17), 0.6)
WOOD_D = mat("WoodDark", (0.28, 0.18, 0.10), 0.7)
GLASSM = mat("CrystalDrop", (0.72, 0.76, 0.78), 0.25)
CLOTH = mat("TableCloth", (0.82, 0.75, 0.60), 0.9)
CANDLE = mat("CandleWax", (0.94, 0.92, 0.84), 0.6)

# ---------- primitive helpers ----------
def _fin(o, material):
    if material: o.data.materials.append(material)
    return o

def box(name, loc, dims, material=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _fin(o, material)

def cyl(name, loc, r, depth, material=None, vertices=20, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    return _fin(o, material)

def frustum(name, loc, r_bot, r_top, depth, material=None, vertices=20, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r_bot, radius2=r_top, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    return _fin(o, material)

def sphere(name, loc, r, material=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=18, ring_count=12, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _fin(o, material)

def torus(name, loc, R, r, material=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=22, minor_segments=8, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    return _fin(o, material)

def strut(name, a, b, r, material=None, vertices=10):
    a, b = Vector(a), Vector(b)
    d = b - a; L = d.length
    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=L, location=(a + b) / 2)
    o = bpy.context.object; o.name = name; o.rotation_euler = q.to_euler()
    return _fin(o, material)

def xform(objs, matrix):
    for o in objs:
        o.matrix_world = matrix @ o.matrix_world

def place(objs, loc, ry=0.0):
    M = Matrix.Translation(Vector(loc)) @ Matrix.Rotation(ry, 4, 'Z')
    xform(objs, M)

# ---------- hats / headgear ----------
def hat_top(name, hz, s, m=BLACK):
    return [cyl(f"{name}_brim", (0, 0, hz), 0.145 * s, 0.014, m, 22),
            cyl(f"{name}_crown", (0, 0, hz + 0.095 * s), 0.098 * s, 0.185 * s, m, 20)]

def hat_conical(name, hz, s):
    return [frustum(f"{name}_conical", (0, 0, hz + 0.16 * s), 0.115 * s, 0.018 * s, 0.34 * s, BLACK, 18),
            cyl(f"{name}_cband", (0, 0, hz + 0.012), 0.118 * s, 0.024, FUR, 18)]

def hat_bearskin(name, hz, s):
    return [cyl(f"{name}_bearskin", (0, 0.01, hz + 0.13 * s), 0.108 * s, 0.28 * s, BLACK, 18)]

def hat_turban(name, hz, s):
    return [sphere(f"{name}_turban", (0, 0, hz + 0.045 * s), 0.115 * s, WHITE, scale=(1, 1, 0.72)),
            torus(f"{name}_twrap", (0, 0, hz + 0.02 * s), 0.105 * s, 0.020 * s, CREAM, rot=(math.radians(90), 0, 0)),
            sphere(f"{name}_jewel", (0, -0.105 * s, hz + 0.05 * s), 0.018 * s, GOLD)]

def hat_feathers(name, hz, s):
    parts = [cyl(f"{name}_band", (0, 0, hz + 0.01), 0.108 * s, 0.03, CLOAK_D, 16)]
    for i, (dx, tilt) in enumerate(((-0.055, -0.35), (0.0, 0.0), (0.055, 0.35))):
        tip = (dx * s, 0.045 * s, hz + 0.30 * s)
        parts.append(strut(f"{name}_feather{i}", (dx * 0.4 * s, 0.01, hz + 0.02), tip, 0.008 * s, CLOAK_D, 6))
        parts.append(sphere(f"{name}_plume{i}", tip, 0.035 * s, WHITE, scale=(0.55, 0.3, 1.5)))
    return parts

# ---------- figures ----------
def figure_man(name, suit=BLACK, hat='top', h=1.75, portly=1.0, waist=None,
               armL=None, armR=None, trouser=None, belt=False, epaulettes=False):
    s = h / 1.75; p = portly
    trouser = trouser or CHARC
    parts = []
    for sd, sgn in (("L", -1), ("R", 1)):
        parts.append(box(f"{name}_shoe{sd}", (sgn * 0.10 * s, -0.045, 0.03), (0.09 * s, 0.25 * s, 0.06), BLACK))
        parts.append(strut(f"{name}_leg{sd}", (sgn * 0.095 * s, 0, 0.95 * s), (sgn * 0.10 * s, -0.01, 0.07), 0.057 * s, trouser))
    parts.append(frustum(f"{name}_coatskirt", (0, 0.01, 0.80 * s), 0.212 * s * p, 0.163 * s * p, 0.42 * s, suit))
    upper = []
    upper.append(frustum(f"{name}_torso", (0, 0, 0.24 * s), 0.163 * s * p, 0.140 * s * p, 0.46 * s, suit))
    upper.append(sphere(f"{name}_shoulders", (0, 0, 0.455 * s), 0.20 * s * p, suit, scale=(1, 0.60, 0.52)))
    if waist:
        upper.append(box(f"{name}_waistcoat", (0, -0.148 * s * p, 0.22 * s), (0.205 * s, 0.025, 0.36 * s), waist))
    if belt:
        upper.append(box(f"{name}_xbelt", (0, -0.155 * s * p, 0.24 * s), (0.055 * s, 0.02, 0.42 * s), WHITE, rot=(math.radians(0), 0, math.radians(38))))
    if epaulettes:
        for sgn in (-1, 1):
            upper.append(box(f"{name}_epau{sgn}", (sgn * 0.20 * s, 0, 0.47 * s), (0.10 * s, 0.12 * s, 0.025), GOLD))
    upper.append(cyl(f"{name}_neck", (0, 0, 0.52 * s), 0.045 * s, 0.08 * s, SKIN, 12))
    upper.append(sphere(f"{name}_head", (0, -0.005, 0.665 * s), 0.105 * s, SKIN))
    hz = 0.745 * s
    if hat == 'top': upper += hat_top(name, hz, s)
    elif hat == 'conical': upper += hat_conical(name, hz, s)
    elif hat == 'bearskin': upper += hat_bearskin(name, hz, s)
    elif hat == 'turban': upper += hat_turban(name, hz, s)
    elif hat == 'feathers': upper += hat_feathers(name, hz, s)
    elif hat == 'cap':
        upper.append(sphere(f"{name}_cap", (0, 0.01, hz + 0.01), 0.108 * s, CHARC, scale=(1, 1, 0.62)))
    defs = {"L": ((-0.30 * s * p, -0.03, 0.20 * s), (-0.26 * s * p, -0.05, -0.18 * s)),
            "R": ((0.30 * s * p, -0.03, 0.20 * s), (0.26 * s * p, -0.05, -0.18 * s))}
    for sd, arm in (("L", armL), ("R", armR)):
        sgn = -1 if sd == "L" else 1
        elbow, hand = arm if arm else defs[sd]
        sh = (sgn * 0.215 * s * p, 0, 0.43 * s)
        upper.append(strut(f"{name}_arm{sd}u", sh, elbow, 0.047 * s, suit))
        upper.append(strut(f"{name}_arm{sd}f", elbow, hand, 0.040 * s, suit))
        upper.append(sphere(f"{name}_hand{sd}", hand, 0.040 * s, SKIN))
    xform(upper, Matrix.Translation(Vector((0, 0, 0.98 * s))))
    parts += upper
    return parts

def figure_woman(name, dress=PALE, bodice=None, h=1.62, veil=False, girl=False):
    s = h / 1.62
    bodice = bodice or dress
    parts = []
    skirt_r = 0.30 if girl else 0.36
    parts.append(frustum(f"{name}_skirt", (0, 0, 0.47 * s), skirt_r * s, 0.125 * s, 0.94 * s, dress, 22))
    parts.append(torus(f"{name}_hem", (0, 0, 0.035), skirt_r * s * 0.97, 0.016 * s, dress))
    parts.append(frustum(f"{name}_bodice", (0, 0, 1.13 * s), 0.125 * s, 0.105 * s, 0.38 * s, bodice, 16))
    parts.append(sphere(f"{name}_shoulders", (0, 0, 1.30 * s), 0.155 * s, bodice, scale=(1, 0.62, 0.55)))
    for sd, sgn in (("L", -1), ("R", 1)):
        parts.append(strut(f"{name}_arm{sd}", (sgn * 0.16 * s, 0, 1.30 * s), (sgn * 0.24 * s, -0.06, 0.92 * s), 0.036 * s, bodice))
        parts.append(sphere(f"{name}_hand{sd}", (sgn * 0.24 * s, -0.06, 0.90 * s), 0.034 * s, SKIN))
    parts.append(cyl(f"{name}_neck", (0, 0, 1.40 * s), 0.04 * s, 0.07 * s, SKIN, 12))
    if veil:
        parts.append(sphere(f"{name}_veilhead", (0, 0, 1.52 * s), 0.108 * s, WHITE))
        parts.append(frustum(f"{name}_veil", (0, 0.01, 1.28 * s), 0.10 * s, 0.20 * s, 0.42 * s, WHITE, 16))
    else:
        parts.append(sphere(f"{name}_head", (0, -0.005, 1.52 * s), 0.098 * s, SKIN))
        parts.append(sphere(f"{name}_hair", (0, 0.03, 1.545 * s), 0.10 * s, HAIR_D, scale=(1, 0.95, 0.9)))
        parts.append(sphere(f"{name}_bun", (0, 0.085 * s, 1.56 * s), 0.045 * s, HAIR_D))
    parts.append(box(f"{name}_shoeL", (-0.09 * s, -0.10, 0.025), (0.07 * s, 0.19 * s, 0.05), BLACK))
    parts.append(box(f"{name}_shoeR", (0.09 * s, -0.10, 0.025), (0.07 * s, 0.19 * s, 0.05), BLACK))
    return parts

def bust(name, suit, hat=None):
    """Background half-figure: torso + head, for crowd depth behind the table."""
    parts = [frustum(f"{name}_torso", (0, 0, 0.22), 0.17, 0.145, 0.44, suit, 14),
             sphere(f"{name}_shoulders", (0, 0, 0.42), 0.20, suit, scale=(1, 0.6, 0.52)),
             sphere(f"{name}_head", (0, -0.005, 0.63), 0.105, SKIN)]
    if hat == 'top': parts += hat_top(name, 0.715, 1.0)
    return parts

def lights_and_camera(cam_loc, target, lens=38, res=(960, 720), samples=48):
    bpy.ops.object.light_add(type='AREA', location=(3.5, -4.5, 5.5))
    key = bpy.context.object; key.name = "KeyLight"; key.data.energy = 550; key.data.shape = 'DISK'; key.data.size = 3.2
    key.rotation_euler = (math.radians(55), 0, math.radians(35))
    bpy.ops.object.light_add(type='AREA', location=(-4.5, -2.5, 3.5))
    fill = bpy.context.object; fill.name = "FillLight"; fill.data.energy = 220; fill.data.size = 2.6
    fill.rotation_euler = (math.radians(65), 0, math.radians(-50))
    bpy.ops.object.light_add(type='AREA', location=(0, 4.5, 4.0))
    back = bpy.context.object; back.name = "BackLight"; back.data.energy = 260; back.data.size = 3.0
    back.rotation_euler = (math.radians(120), 0, 0)
    world = bpy.data.worlds.new("World"); scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.55
    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.object; cam.name = "PreviewCamera"
    direction = Vector(target) - Vector(cam_loc)
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = lens
    scene.camera = cam
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.cycles.device = 'CPU'
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.film_transparent = False
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'Medium Contrast'

def finish(slug, outdir):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.select_all(action='DESELECT')
    tris = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for o in bpy.data.objects:
        if o.type == 'MESH':
            ev = o.evaluated_get(dg); m = ev.to_mesh(); m.calc_loop_triangles()
            tris += len(m.loop_triangles); ev.to_mesh_clear()
    print(f"TRIANGLE_COUNT {tris}")
    print(f"OBJECT_COUNT {len(bpy.data.objects)}")
    blend_path = os.path.join(outdir, slug + ".blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    glb_path = os.path.join(outdir, slug + ".glb")
    bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB')
    scene.render.filepath = os.path.join(outdir, "preview.png")
    bpy.ops.render.render(write_still=True)
    print("DONE", blend_path, glb_path)

# ============================================================
# SCENE — fig-61 "The Opera" (Punch, 1851). Salon vignette ~7.4 m wide.
# Long table centre; receiving line on both sides; chandelier above.
# ============================================================
OUT = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig61-at-the-opera"

# ---- floor + room shell (back wall built as segments around the arch) ----
box("Floor", (0, 0, -0.03), (7.6, 4.4, 0.06), WOOD_M)
box("BackWallL", (-2.21, 1.85, 1.65), (3.18, 0.15, 3.3), WALL)
box("BackWallR", (2.21, 1.85, 1.65), (3.18, 0.15, 3.3), WALL)
box("BackWallTopC", (0, 1.85, 3.01), (1.24, 0.15, 0.58), WALL)
for sx in (-1, 1):  # fill pieces between the rectangular opening and the arch curve
    box(f"ArchSpandrel_{sx}", (sx * 0.47, 1.85, 2.41), (0.32, 0.15, 0.62), WALL)
# wall panelling: three framed panels either side of the arch
for i, px in enumerate((-3.05, -2.15, 2.15, 3.05)):
    box(f"Panel_{i}", (px, 1.755, 1.75), (0.78, 0.03, 1.9), WALL_D)
    box(f"PanelIn_{i}", (px, 1.745, 1.75), (0.64, 0.03, 1.72), WALL)
for sx in (-1, 1):  # pilasters
    box(f"Pilaster_{sx}", (sx * 3.62, 1.76, 1.65), (0.22, 0.10, 3.3), WALL_D)
box("Cornice", (0, 1.78, 3.22), (7.6, 0.24, 0.16), WALL_D)
box("Skirting", (0, 1.76, 0.14), (7.6, 0.22, 0.28), WALL_D)

# ---- arched opening, centre-back (arch trim + dark room beyond) ----
torus("ArchTrim", (0, 1.755, 2.10), 0.62, 0.045, WALL_D, rot=(0, 0, 0))
box("ArchDark", (0, 2.02, 1.42), (1.5, 0.06, 2.84), DARKIN)
# a dim figure standing in the room beyond the arch
place(figure_man("BeyondFigure", suit=CHARC, hat='none', h=1.70, waist=CREAM), (0.08, 1.90, 0), ry=math.radians(180))

# ---- long table with cloth, centre ----
box("TableTop", (0, 0, 0.76), (3.7, 0.92, 0.05), WOOD_D)
box("TableClothTop", (0, 0, 0.795), (3.85, 1.02, 0.035), CLOTH)
box("TableClothFront", (0, -0.50, 0.42), (3.85, 0.03, 0.72), CLOTH)
box("TableClothBack", (0, 0.50, 0.42), (3.85, 0.03, 0.72), CLOTH)
box("TableClothTrim", (0, -0.517, 0.755), (3.85, 0.012, 0.045), GOLD)
for sx in (-1, 1):
    box(f"TableClothEnd_{sx}", (sx * 1.915, 0, 0.42), (0.03, 1.02, 0.72), CLOTH)
# centrepiece: low bowl + two candlesticks
sphere("CentreBowl", (0, 0, 0.86), 0.16, BRASS, scale=(1, 1, 0.45))
for sx in (-1, 1):
    cyl(f"Candlestick_{sx}", (sx * 1.15, 0, 0.90), 0.016, 0.17, BRASS, 10)
    cyl(f"Candle_{sx}", (sx * 1.15, 0, 1.015), 0.011, 0.07, CANDLE, 8)
    sphere(f"Flame_{sx}", (sx * 1.15, 0, 1.065), 0.011, GOLD, scale=(1, 1, 1.6))

# ---- chandelier above the table ----
CH = (0, 0, 0)
cyl("ChStem", (0, 0, 2.95), 0.016, 0.7, BRASS, 10)
sphere("ChHub", (0, 0, 2.62), 0.055, BRASS)
torus("ChRing", (0, 0, 2.42), 0.34, 0.016, BRASS)
for i in range(6):
    a = i * math.pi / 3.0
    ex, ey = 0.34 * math.cos(a), 0.34 * math.sin(a)
    strut(f"ChArm_{i}", (0, 0, 2.60), (ex, ey, 2.44), 0.009, BRASS, 6)
    cyl(f"ChCandle_{i}", (ex, ey, 2.50), 0.012, 0.11, CANDLE, 8)
    sphere(f"ChFlame_{i}", (ex, ey, 2.575), 0.010, GOLD, scale=(1, 1, 1.6))
    sphere(f"ChDrop_{i}", (ex * 0.96, ey * 0.96, 2.28), 0.011, GLASSM, scale=(1, 1, 1.5))
for i in range(3):
    sphere(f"ChDropC_{i}", (0, 0, 2.38 - i * 0.09), 0.010, GLASSM, scale=(1, 1, 1.5))

# ---- the receiving line ----
# far side (facing the camera, -Y default)
place(figure_man("FarMan1", suit=BLACK, hat='top', h=1.76, waist=CREAM), (-1.60, 0.82, 0), ry=math.radians(-6))
place(figure_man("FarMan2", suit=CHARC, hat='none', h=1.72), (-0.78, 0.86, 0), ry=math.radians(4))
place(figure_woman("FarWoman", dress=PINK, bodice=BURG), (0.98, 0.84, 0), ry=math.radians(-4))
place(figure_man("FarMan3", suit=CHARC, hat='top', h=1.74), (1.78, 0.86, 0), ry=math.radians(6))
# background busts for crowd depth, far back
place(bust("Crowd1", BLACK, 'top'), (-2.55, 1.15, 0.62))
place(bust("Crowd2", CHARC, None), (2.55, 1.15, 0.62))

# left end: fur-trimmed cloak + tall conical hat, facing the table
cloak = figure_man("CloakMan", suit=CLOAK_D, hat='conical', h=1.78, portly=1.12)
# fur collar + front trim
cloak.append(torus("CloakMan_furcollar", (0, 0, 1.44), 0.155, 0.038, FUR))
cloak.append(box("CloakMan_furfront", (0, -0.175, 0.95), (0.07, 0.03, 0.85), FUR))
place(cloak, (-2.35, -0.30, 0), ry=math.radians(52))
place(figure_woman("LeftWoman", dress=PALE, bodice=BLACK), (-2.95, 0.32, 0), ry=math.radians(128))

# centre near side: principal figure — feather headdress, patterned cloak, long staff
prin = figure_man("Principal", suit=CLOAK, hat='feathers', h=1.80, portly=1.0,
                  armR=((0.34, -0.05, 0.22), (0.34, -0.16, -0.30)))
prin.append(box("Principal_cloakpanel", (0, -0.165, 1.22), (0.24, 0.025, 0.42), CLOAK_D))
place(prin, (0.12, -0.62, 0), ry=math.radians(-8))
# the long staff, grounded beside him, passing through his lowered right hand
strut("Staff", (0.50, -0.85, 0.0), (0.465, -0.81, 1.55), 0.016, WOOD_D, 8)
sphere("StaffKnob", (0.465, -0.81, 1.58), 0.028, GOLD)

# right of centre, near side: turbaned man with a round hand-fan + woman + girl
turb = figure_man("TurbanMan", suit=GREEN, hat='turban', h=1.74,
                  armL=((-0.28, -0.14, 0.18), (-0.22, -0.30, -0.05)))
place(turb, (1.18, -0.52, 0), ry=math.radians(162))
cyl("HandFan", (1.44, -0.33, 0.95), 0.085, 0.012, CREAM, 20, rot=(math.radians(75), 0, math.radians(-15)))
place(figure_woman("RightWoman", dress=WHITE, bodice=BLUE), (1.78, -0.44, 0), ry=math.radians(176))
place(figure_woman("Girl", dress=PINK, h=1.18, girl=True), (2.32, -0.34, 0), ry=math.radians(168))

# far right: guardsman (bearskin, red coat, cross-belt) + veiled woman in white
place(figure_man("Guardsman", suit=RED, hat='bearskin', h=1.82, belt=True, epaulettes=True,
                 trouser=BLACK), (2.88, -0.12, 0), ry=math.radians(215))
place(figure_woman("VeiledWoman", dress=WHITE, veil=True), (3.38, 0.22, 0), ry=math.radians(205))

lights_and_camera((0.15, -7.6, 2.7), (0.1, 0.15, 1.10), lens=38, res=(1024, 720))
finish(SLUG, OUT)
