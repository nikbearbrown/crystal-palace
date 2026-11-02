#!/usr/bin/env python3
"""Build scan-fig46-pound-and-a-shilling: Punch cartoon "The Pound and the Shilling", 1851.
Two family groups meet in the exhibition: a portly gentleman (the Pound) greets a rustic
labourer family (the Shilling). Blender 4.5.3, metres, origin at base centre. Re-runnable:
  blender -b --python build_scan_fig46_pound_and_a_shilling.py
Outputs .blend, .glb, preview.png beside this script. No text/lettering anywhere."""
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

GLASS = mat("Glass", (0.80, 0.88, 0.90), 0.08, 0.0, alpha=0.18)
SKIN  = mat("SkinTone", (0.90, 0.68, 0.53), 0.65)
HAIR_D = mat("HairDark", (0.16, 0.11, 0.08), 0.8)
HAIR_W = mat("HairWhite", (0.88, 0.86, 0.80), 0.85)
BLACK = mat("CoatBlack", (0.045, 0.045, 0.055), 0.8)
CHARC = mat("Charcoal", (0.13, 0.13, 0.14), 0.85)
BROWN = mat("BrownCoat", (0.30, 0.20, 0.12), 0.85)
TAN   = mat("SmockTan", (0.66, 0.55, 0.38), 0.9)
CREAM = mat("WaistcoatCream", (0.90, 0.84, 0.68), 0.8)
WHITE = mat("WhiteCloth", (0.93, 0.92, 0.88), 0.85)
GREY  = mat("GreyDress", (0.45, 0.46, 0.48), 0.9)
PALE  = mat("PaleDress", (0.84, 0.80, 0.72), 0.9)
BLUE  = mat("DressBlue", (0.10, 0.20, 0.38), 0.85)
BURG  = mat("DressBurgundy", (0.32, 0.07, 0.11), 0.85)
GREEN = mat("DressGreen", (0.13, 0.28, 0.16), 0.85)
RUST  = mat("ShawlRust", (0.48, 0.22, 0.12), 0.9)
RED   = mat("AccentRed", (0.55, 0.10, 0.10), 0.8)
GOLD  = mat("Gilt", (0.85, 0.62, 0.20), 0.35, 0.85)
BRASS = mat("Brass", (0.70, 0.50, 0.22), 0.4, 0.8)
IRON  = mat("IronPale", (0.55, 0.58, 0.53), 0.6, 0.4)
STONE = mat("Stone", (0.74, 0.70, 0.62), 0.9)
WOOD_D = mat("WoodDark", (0.28, 0.18, 0.10), 0.85)
WOOD_M = mat("WoodMid", (0.45, 0.30, 0.17), 0.85)
WOOD_L = mat("WoodLight", (0.62, 0.46, 0.28), 0.85)
LEATH = mat("Leather", (0.36, 0.22, 0.12), 0.7)
PAPER = mat("PaperBlank", (0.92, 0.90, 0.84), 0.9)
DARKIN = mat("DarkInterior", (0.10, 0.09, 0.08), 0.95)

# ---------- primitive helpers (scale applied at creation) ----------
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

def arch_panel(name, w, h_straight, t, material=None):
    """Panel in XZ plane (x across, z up), base at z=0, semicircular top radius w/2, thickness t along Y."""
    import bmesh
    r = w / 2.0
    pts = [(-r, 0.0), (r, 0.0), (r, h_straight)]
    for i in range(1, 13):
        a = (i / 12.0) * math.pi
        pts.append((r * math.cos(a), h_straight + r * math.sin(a)))
    pts.append((-r, h_straight))
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new((x, 0, z)) for x, z in pts]
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    tv = [e for e in ext['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=tv, vec=(0, t, 0))
    bm.to_mesh(mesh); bm.free()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(o)
    if material: mesh.materials.append(material)
    return o

def tri_panel(name, w, h, t, material=None):
    """Right-triangle panel in XZ plane, vertical edge at x=0, thickness t along Y."""
    import bmesh
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new(p) for p in ((0, 0, 0), (w, 0, 0), (0, 0, h))]
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    tv = [e for e in ext['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=tv, vec=(0, t, 0))
    bm.to_mesh(mesh); bm.free()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(o)
    if material: mesh.materials.append(material)
    return o

def xform(objs, matrix):
    for o in objs:
        o.matrix_world = matrix @ o.matrix_world

def place(objs, loc, ry=0.0, lean=0.0):
    M = Matrix.Translation(Vector(loc)) @ Matrix.Rotation(ry, 4, 'Z') @ Matrix.Rotation(lean, 4, 'X')
    xform(objs, M)

def wheel(name, r, material, hub_mat=None, width=0.05):
    """Wheel in XY plane, axle along Z. Returns list of objects."""
    parts = [torus(name + "_rim", (0, 0, 0), r - 0.02, 0.028, material),
             cyl(name + "_hub", (0, 0, 0), 0.05, width + 0.03, hub_mat or material, rot=(0, 0, 0))]
    for i in range(3):
        a = i * math.pi / 3
        parts.append(box(name + f"_sp{i}", (0, 0, 0), (0.03, 2 * r - 0.05, 0.03), material, rot=(0, 0, a)))
    return parts

# ---------- hats ----------
def hat_top(name, z, s=1.0, material=None):
    material = material or BLACK
    return [cyl(name + "_brim", (0, 0, z), 0.118 * s, 0.014, material, 20),
            cyl(name + "_crown", (0, 0, z + 0.085 * s), 0.083 * s, 0.16 * s, material, 20)]

def hat_wide(name, z, s=1.0, material=None):
    material = material or BROWN
    return [cyl(name + "_brim", (0, 0, z), 0.165 * s, 0.012, material, 20),
            sphere(name + "_crown", (0, 0, z + 0.028 * s), 0.098 * s, material, scale=(1, 1, 0.62))]

def hat_cap(name, z, s=1.0, material=None):
    material = material or CHARC
    return [sphere(name + "_cap", (0, 0.01, z), 0.10 * s, material, scale=(1, 1, 0.62)),
            box(name + "_peak", (0, -0.115 * s, z - 0.005), (0.11 * s, 0.07 * s, 0.012), material)]

def hat_nightcap(name, z, s=1.0):
    return [frustum(name + "_nightcap", (0.02, 0.01, z + 0.11 * s), 0.10 * s, 0.015, 0.30 * s, WHITE, 14,
                    rot=(0, math.radians(14), 0))]

def bonnet(name, z, s=1.0, material=None):
    material = material or BURG
    return [sphere(name + "_bonnet", (0, 0.032 * s, z + 0.015 * s), 0.112 * s, material, scale=(1, 1.02, 1.05)),
            torus(name + "_brim", (0, -0.012 * s, z + 0.01 * s), 0.104 * s, 0.02 * s, material,
                  rot=(math.radians(78), 0, 0))]

# ---------- figures (local coords, facing -Y, base at origin) ----------
def figure_man(name, suit=BLACK, hat='top', h=1.75, portly=1.0, waist=None,
               armL=None, armR=None, bend=0.0, trouser=None, apron=None, hair=HAIR_D):
    """armL/armR: (elbow, hand) points in torso-group coords (origin at hip, z up).
    Default arms hang at sides. bend: forward bow of torso group about the hip."""
    s = h / 1.75; p = portly
    trouser = trouser or CHARC
    parts = []
    for sd, sgn in (("L", -1), ("R", 1)):
        parts.append(box(f"{name}_shoe{sd}", (sgn * 0.10 * s, -0.045, 0.03), (0.09 * s, 0.25 * s, 0.06), BLACK))
        parts.append(strut(f"{name}_leg{sd}", (sgn * 0.095 * s, 0, 0.95 * s), (sgn * 0.10 * s, -0.01, 0.07), 0.057 * s, trouser))
    if True:  # coat skirt
        parts.append(frustum(f"{name}_coatskirt", (0, 0.01, 0.80 * s), 0.212 * s * p, 0.163 * s * p, 0.42 * s, suit))
        parts.append(box(f"{name}_tails", (0, 0.155 * s * p, 0.76 * s), (0.19 * s, 0.035, 0.44 * s), suit, rot=(math.radians(6), 0, 0)))
    upper = []
    upper.append(frustum(f"{name}_torso", (0, 0, 0.24 * s), 0.163 * s * p, 0.140 * s * p, 0.46 * s, suit))
    upper.append(sphere(f"{name}_shoulders", (0, 0, 0.455 * s), 0.20 * s * p, suit, scale=(1, 0.60, 0.52)))
    if waist:
        upper.append(box(f"{name}_waistcoat", (0, -0.148 * s * p, 0.22 * s), (0.205 * s, 0.025, 0.36 * s), waist))
    if apron:
        upper.append(box(f"{name}_apron", (0, -0.155 * s * p, 0.10 * s), (0.24 * s, 0.02, 0.55 * s), apron))
    upper.append(cyl(f"{name}_neck", (0, 0, 0.52 * s), 0.045 * s, 0.08 * s, SKIN, 12))
    upper.append(sphere(f"{name}_head", (0, -0.005, 0.665 * s), 0.105 * s, SKIN))
    if hair == HAIR_W:
        upper.append(sphere(f"{name}_hair", (0, 0.028, 0.685 * s), 0.107 * s, HAIR_W, scale=(1, 1, 0.92)))
    hz = 0.745 * s
    if hat == 'top': upper += hat_top(name, hz, s)
    elif hat == 'wide': upper += hat_wide(name, hz, s)
    elif hat == 'cap': upper += hat_cap(name, hz, s)
    elif hat == 'nightcap': upper += hat_nightcap(name, hz, s)
    defs = {"L": ((-0.30 * s * p, -0.03, 0.20 * s), (-0.26 * s * p, -0.05, -0.18 * s)),
            "R": ((0.30 * s * p, -0.03, 0.20 * s), (0.26 * s * p, -0.05, -0.18 * s))}
    for sd, arm in (("L", armL), ("R", armR)):
        sgn = -1 if sd == "L" else 1
        elbow, hand = arm if arm else defs[sd]
        sh = (sgn * 0.215 * s * p, 0, 0.43 * s)
        upper.append(strut(f"{name}_arm{sd}u", sh, elbow, 0.047 * s, suit))
        upper.append(strut(f"{name}_arm{sd}f", elbow, hand, 0.040 * s, suit))
        upper.append(sphere(f"{name}_hand{sd}", hand, 0.040 * s, SKIN))
    if bend:
        xform(upper, Matrix.Rotation(bend, 4, 'X'))
    xform(upper, Matrix.Translation(Vector((0, 0, 0.98 * s))))
    parts += upper
    return parts

def figure_woman(name, dress=PALE, hat='bonnet', h=1.62, armL=None, armR=None,
                 shawl=None, sash=None, hair=HAIR_D):
    s = h / 1.62
    parts = []
    parts.append(frustum(f"{name}_skirt1", (0, 0, 0.175), 0.365 * s, 0.315 * s, 0.35, dress))
    parts.append(frustum(f"{name}_skirt2", (0, 0, 0.47), 0.305 * s, 0.245 * s, 0.30, dress))
    parts.append(frustum(f"{name}_skirt3", (0, 0, 0.74), 0.235 * s, 0.172 * s, 0.28, dress))
    parts.append(frustum(f"{name}_bodice", (0, 0, 1.09 * s), 0.138 * s, 0.096 * s, 0.44 * s, dress))
    parts.append(sphere(f"{name}_shoulders", (0, 0, 1.315 * s), 0.155 * s, dress, scale=(1, 0.62, 0.55)))
    if shawl:
        parts.append(frustum(f"{name}_shawl", (0, 0, 1.20 * s), 0.205 * s, 0.125 * s, 0.34 * s, shawl))
    if sash:
        parts.append(box(f"{name}_sash", (0, -0.105 * s, 1.13 * s), (0.075 * s, 0.02, 0.42 * s), sash, rot=(0, 0, math.radians(38))))
    parts.append(cyl(f"{name}_neck", (0, 0, 1.375 * s), 0.04 * s, 0.07 * s, SKIN, 12))
    parts.append(sphere(f"{name}_head", (0, -0.005, 1.475 * s), 0.10 * s, SKIN))
    parts.append(sphere(f"{name}_bun", (0, 0.065 * s, 1.53 * s), 0.055 * s, hair))
    if hat == 'bonnet': parts += bonnet(name, 1.475 * s, s, dress)
    elif hat == 'crown':
        parts.append(cyl(f"{name}_crown", (0, 0, 1.585 * s), 0.068 * s, 0.05 * s, GOLD, 14))
        for i in range(4):
            a = i * math.pi / 2 + math.pi / 4
            parts.append(frustum(f"{name}_crownpt{i}", (0.055 * s * math.cos(a), 0.055 * s * math.sin(a), 1.635 * s), 0.012, 0.001, 0.05 * s, GOLD, 6))
    defs = {"L": ((-0.235 * s, -0.04, 1.02 * s), (-0.17 * s, -0.16, 0.86 * s)),
            "R": ((0.235 * s, -0.04, 1.02 * s), (0.17 * s, -0.16, 0.86 * s))}
    for sd, arm in (("L", armL), ("R", armR)):
        sgn = -1 if sd == "L" else 1
        elbow, hand = arm if arm else defs[sd]
        sh = (sgn * 0.16 * s, 0, 1.30 * s)
        parts.append(strut(f"{name}_arm{sd}u", sh, elbow, 0.042 * s, dress))
        parts.append(strut(f"{name}_arm{sd}f", elbow, hand, 0.036 * s, dress))
        parts.append(sphere(f"{name}_hand{sd}", hand, 0.036 * s, SKIN))
    return parts

def bust(name, dress=PALE, hat='bonnet', h=1.62):
    """Head + shoulders only, for crowds behind rails/galleries. Base at origin."""
    s = h / 1.62
    parts = [frustum(f"{name}_shoulders", (0, 0, 0.10), 0.20 * s, 0.10 * s, 0.24, dress),
             sphere(f"{name}_head", (0, -0.005, 0.335 * s), 0.10 * s, SKIN)]
    if hat == 'bonnet': parts += bonnet(name, 0.335 * s, s, dress)
    elif hat == 'top': parts += hat_top(name, 0.405 * s, s)
    elif hat == 'cap': parts += hat_cap(name, 0.405 * s, s)
    elif hat == 'wide': parts += hat_wide(name, 0.405 * s, s)
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
# SCENE — fig-46 "The Pound and the Shilling" (Punch, 14 June 1851)
# ============================================================
OUT = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig46-pound-and-a-shilling"

LILAC = mat("DressLilac", (0.74, 0.68, 0.80), 0.9)
BACKBOARD = mat("BackdropBoard", (0.23, 0.20, 0.17), 0.95)

# ---- floor: boarded exhibition floor ----
box("Floor", (0, 0, -0.04), (6.4, 3.6, 0.08), WOOD_M)
for i in range(7):
    box(f"FloorGroove{i}", (0, -1.5 + i * 0.5, 0.002), (6.4, 0.018, 0.004), WOOD_D)

# ---- background: hoarding board + barrier rail + crowd busts behind ----
box("Hoarding", (0, 1.58, 0.575), (6.4, 0.07, 1.15), BACKBOARD)
for i, x in enumerate((-3.0, -1.5, 0.0, 1.5, 3.0)):
    box(f"RailPost{i}", (x, 1.22, 0.5), (0.07, 0.07, 1.0), WOOD_D)
box("RailTop", (0, 1.22, 1.02), (6.4, 0.06, 0.07), WOOD_D)
box("RailMid", (0, 1.22, 0.55), (6.4, 0.05, 0.05), WOOD_D)
crowd_specs = [(-2.6, PALE, 'bonnet'), (-1.35, GREY, 'top'), (0.05, BURG, 'bonnet'),
               (1.45, CHARC, 'cap'), (2.65, BLUE, 'bonnet')]
for i, (x, dm, ht) in enumerate(crowd_specs):
    b = bust(f"Crowd{i}", dress=dm, hat=ht)
    place(b, (x, 1.66, 1.13), ry=math.radians(180 + (i - 2) * 6))

# ---- column (right) and statue stand (right-mid, background) ----
box("ColumnBase", (2.78, 0.72, 0.13), (0.52, 0.52, 0.26), IRON)
cyl("ColumnShaft", (2.78, 0.72, 1.85), 0.15, 3.2, IRON, 14)
box("ColumnCapital", (2.78, 0.72, 3.5), (0.46, 0.46, 0.14), IRON)
box("Pedestal", (1.82, 1.08, 0.5), (0.54, 0.54, 1.0), STONE)
statue = [frustum("StatueRobe", (0, 0, 0.31), 0.165, 0.10, 0.62, STONE),
          frustum("StatueTorso", (0, 0, 0.76), 0.10, 0.075, 0.30, STONE),
          sphere("StatueHead", (0, -0.01, 1.0), 0.075, STONE),
          strut("StatueArm", (0.09, 0, 0.82), (0.16, -0.10, 0.55), 0.032, STONE)]
place(statue, (1.82, 1.08, 1.0), ry=math.radians(-18))

# ---- THE POUND: tall portly gentleman, arm extended in greeting ----
sG = 1.86 / 1.75
gent = figure_man("Gent", suit=BLACK, hat='top', h=1.86, portly=1.38, waist=CREAM,
                  armL=((-0.36, -0.30, 0.33 * sG), (-0.22, -0.68, 0.17 * sG)),
                  armR=((0.38, -0.04, 0.14 * sG), (0.35, -0.24, -0.26 * sG)))
# umbrella in his right hand (figure-local coords)
gent.append(strut("UmbrellaShaft", (0.35, -0.26, 0.80), (0.44, -0.40, 0.05), 0.014, WOOD_D))
gent.append(frustum("UmbrellaFold", (0.415, -0.365, 0.30), 0.016, 0.055, 0.42, CHARC))
# carpet bag at his feet
gent.append(box("CarpetBag", (0.02, -0.55, 0.15), (0.36, 0.21, 0.30), LEATH))
gent.append(box("CarpetBagTop", (0.02, -0.55, 0.315), (0.30, 0.17, 0.04), BROWN))
gent.append(torus("CarpetBagHandle", (0.02, -0.55, 0.36), 0.085, 0.014, BRASS, rot=(math.radians(90), 0, 0)))
place(gent, (-0.88, -0.18, 0), ry=math.radians(80))

# ---- his wife: bonneted lady in pale crinoline with parasol ----
wife = figure_woman("GentsWife", dress=LILAC, hat='bonnet', h=1.60,
                    armL=((-0.24, -0.05, 1.0), (-0.15, -0.20, 0.88)),
                    armR=((0.26, -0.14, 1.04), (0.19, -0.30, 1.10)))
wife.append(strut("ParasolStick", (0.19, -0.31, 1.06), (0.38, -0.58, 1.80), 0.013, WOOD_D))
wife.append(frustum("ParasolCanopy", (0.40, -0.61, 1.82), 0.41, 0.03, 0.18, CREAM, 16, rot=(math.radians(-22), 0, 0)))
place(wife, (-1.68, 0.32, 0), ry=math.radians(58))

# ---- THE SHILLING: rustic labourer leaning back in surprise, staff in hand ----
sL = 1.72 / 1.75
lab = figure_man("Labourer", suit=TAN, hat='wide', h=1.72, portly=0.95, trouser=BROWN,
                 armL=((-0.35, -0.14, 0.30 * sL), (-0.31, -0.42, 0.44 * sL)),
                 armR=((0.33, -0.02, 0.10 * sL), (0.31, -0.13, -0.28 * sL)))
lab.append(torus("Neckerchief", (0, 0, 1.40 * sL), 0.088, 0.030, RUST))
lab.append(cyl("Staff", (0.335, -0.15, 0.98), 0.018, 1.96, WOOD_M, 10))
lab.append(box("StaffHead", (0.335, -0.15, 1.93), (0.34, 0.045, 0.045), WOOD_D))
place(lab, (0.82, -0.12, 0), ry=math.radians(-76), lean=math.radians(-5))

# ---- his wife: bonnet, shawl, baby in arms ----
sW = 1.58 / 1.62
labwife = figure_woman("LabWife", dress=GREY, hat='bonnet', h=1.58, shawl=RUST,
                       armL=((-0.235 * sW, -0.15, 1.04 * sW), (-0.06, -0.25, 1.03 * sW)),
                       armR=((0.235 * sW, -0.15, 1.04 * sW), (0.06, -0.25, 1.03 * sW)))
labwife.append(cyl("BabyBundle", (0, -0.27, 1.10 * sW), 0.066, 0.34, CREAM, 12, rot=(0, 0, math.radians(90))))
labwife.append(sphere("BabyHead", (0.155, -0.27, 1.13 * sW), 0.05, SKIN))
labwife.append(box("Apron", (0, -0.235, 0.52), (0.27, 0.02, 0.52), WHITE, rot=(math.radians(-10), 0, 0)))
place(labwife, (1.62, 0.30, 0), ry=math.radians(-62))

# ---- their small daughter, holding toward her mother ----
girl = figure_woman("Girl", dress=PALE, hat='bonnet', h=1.02,
                    armL=((-0.17, -0.03, 0.64), (-0.15, -0.06, 0.60)),
                    armR=((0.15, -0.05, 0.62), (0.11, -0.16, 0.52)))
place(girl, (2.08, -0.34, 0), ry=math.radians(-48))

lights_and_camera((0.2, -6.5, 2.0), (0.0, 0.15, 0.92), lens=40, res=(800, 1024))
finish(SLUG, OUT)
