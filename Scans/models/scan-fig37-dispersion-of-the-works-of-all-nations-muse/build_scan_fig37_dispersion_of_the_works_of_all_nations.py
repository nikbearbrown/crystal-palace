#!/usr/bin/env python3
"""Build scan-fig37-dispersion-of-the-works-of-all-nations: Cruikshank's "The Dispersion of the Works of All Nations from the Great Exhibition of 1851" - the exhibits scatter from the Crystal Palace.
Blender 4.5.3, metres, origin at base centre. Re-runnable:
  blender -b --python build_scan_fig37_dispersion_of_the_works_of_all_nations.py
Outputs .blend, .glb, preview.png beside this script. Roof banner blank - no lettering anywhere."""
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
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=14, ring_count=10, location=loc)
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
# SCENE — fig-37 "The Dispersion of the Works of All Nations" (Cruikshank, 1851)
# The exhibits scatter in every direction from the Crystal Palace.
# Elevated pieces rest on slim dark struts: a staging device to suggest the
# drawn flight (flagged in NOTES). Blank roof banner — no lettering.
# ============================================================
OUT = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig37-dispersion-of-the-works-of-all-nations"

import bmesh
def vault_shell(name, r, length, material, seg=16):
    """Half-cylinder shell, axis along Y, base rim at z=0, opening downward."""
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rows = []
    for y in (0.0, length):
        row = [bm.verts.new((r * math.cos(math.pi * i / seg), y, r * math.sin(math.pi * i / seg))) for i in range(seg + 1)]
        rows.append(row)
    for i in range(seg):
        bm.faces.new((rows[0][i], rows[0][i + 1], rows[1][i + 1], rows[1][i]))
    bm.to_mesh(mesh); bm.free()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(o)
    if material: mesh.materials.append(material)
    return o

def vault_shell_x(name, span_r, rise, length, material, seg=16):
    """Barrel vault with ridge along X: arc in the YZ plane (y across, z up), length along X."""
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rows = []
    for x in (-length / 2, length / 2):
        row = [bm.verts.new((x, span_r * math.cos(math.pi * i / seg), rise * math.sin(math.pi * i / seg))) for i in range(seg + 1)]
        rows.append(row)
    for i in range(seg):
        bm.faces.new((rows[0][i], rows[1][i], rows[1][i + 1], rows[0][i + 1]))
    bm.to_mesh(mesh); bm.free()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(o)
    if material: mesh.materials.append(material)
    return o

SAIL = mat("SailCanvas", (0.90, 0.87, 0.78), 0.9)
HULL = mat("HullDark", (0.20, 0.13, 0.09), 0.8)
BEAR = mat("BearWhite", (0.92, 0.90, 0.85), 0.9)
OCEAN = mat("GlobeOcean", (0.25, 0.45, 0.55), 0.6)
LAND = mat("GlobeLand", (0.55, 0.48, 0.30), 0.8)
STRUTD = mat("DisplayStrut", (0.08, 0.08, 0.09), 0.7, 0.4)

# ---- floor ----
box("Floor", (0, 0, -0.04), (13.0, 7.0, 0.08), WOOD_L)
for i in range(11):
    box(f"FloorGroove{i}", (0, -3.0 + i * 0.6, 0.002), (13.0, 0.02, 0.004), WOOD_M)

# ---- the Crystal Palace hint, centre-back ----
pal = []
pal.append(box("PalacePlinth", (0, 0.9, 0.075), (8.8, 1.9, 0.15), STONE))
pal.append(box("PalaceWall", (0, 0, 1.25), (8.8, 0.12, 2.2), IRON))
for i in range(7):
    ap = arch_panel(f"NaveWindow{i}", 0.92, 1.15, 0.03, GLASS)
    place([ap], (-3.3 + i * 1.1, -0.10, 0.30)); pal.append(ap)
    if i < 6:
        pal.append(box(f"NaveMullion{i}", (-2.75 + i * 1.1, -0.06, 1.25), (0.09, 0.06, 2.2), IRON))
pal.append(box("PalaceWallBack", (0, 1.78, 1.25), (8.8, 0.12, 2.2), IRON))
nv = vault_shell_x("NaveVault", 0.95, 2.0, 8.8, GLASS); place([nv], (0, 0.9, 2.35)); pal.append(nv)
# transept: taller centre block with great arch, vault running front-to-back
pal.append(box("TranseptWallL", (-1.55, 0, 1.575), (0.35, 0.12, 2.85), IRON))
pal.append(box("TranseptWallR", (1.55, 0, 1.575), (0.35, 0.12, 2.85), IRON))
pal.append(box("TranseptWallTop", (0, 0, 2.92), (3.45, 0.12, 0.30), IRON))
tap = arch_panel("TranseptArch", 2.6, 1.35, 0.03, GLASS); place([tap], (0, -0.10, 0.25)); pal.append(tap)
tv = vault_shell("TranseptVault", 1.3, 2.1, GLASS); place([tv], (0, -0.15, 3.0)); pal.append(tv)
# blank banner board across the roof front (the print lettered it; left blank here)
pal.append(box("RoofBanner", (0, 0.55, 4.12), (3.8, 0.05, 0.55), PAPER, rot=(math.radians(-30), 0, 0)))
pal.append(cyl("BannerPoleL", (-1.8, 0.5, 3.9), 0.025, 0.85, WOOD_D, 8))
pal.append(cyl("BannerPoleR", (1.8, 0.5, 3.9), 0.025, 0.85, WOOD_D, 8))
place(pal, (0, 1.55, 0))
# tower + chimney behind the roof
box("Tower", (0.2, 2.75, 3.15), (0.85, 0.85, 6.3), mat("TowerStone", (0.60, 0.56, 0.50), 0.9))
frustum("TowerCap", (0.2, 2.75, 6.55), 0.62, 0.05, 0.55, WOOD_D, 4)
sphere("TowerFinial", (0.2, 2.75, 6.9), 0.09, GOLD)
box("Chimney", (-2.7, 2.45, 2.2), (0.5, 0.5, 4.4), mat("ChimneyStone", (0.60, 0.56, 0.50), 0.9))
cyl("ChimneyPot", (-2.7, 2.45, 4.55), 0.13, 0.35, BROWN, 12)

# ---- locomotive (left foreground, steaming away) ----
loco = []
loco.append(box("LocoFrame", (0, 0, 0.52), (2.7, 0.78, 0.30), BLACK))
loco.append(cyl("LocoBoiler", (-0.25, 0, 1.02), 0.335, 1.95, CHARC, 20, rot=(0, math.radians(90), 0)))
loco.append(frustum("LocoChimney", (0.62, 0, 1.52), 0.075, 0.13, 0.42, BLACK, 14))
loco.append(sphere("LocoDome", (-0.05, 0, 1.33), 0.15, BRASS, scale=(1, 1, 0.8)))
loco.append(box("LocoCab", (-1.05, 0, 1.06), (0.62, 0.84, 1.38), BROWN))
loco.append(box("LocoCabRoof", (-1.05, 0, 1.80), (0.74, 0.94, 0.07), BLACK))
loco.append(box("LocoBuffer", (1.38, 0, 0.55), (0.10, 0.7, 0.22), WOOD_D))
for wx, wr in ((-0.95, 0.30), (-0.25, 0.30), (0.62, 0.40)):
    for sd in (-1, 1):
        w = wheel(f"LocoWheel{wx}_{sd}", wr, IRON, BLACK, 0.06)
        xform(w, Matrix.Rotation(math.radians(90), 4, 'X'))
        place(w, (wx, sd * 0.42, wr)); loco += w
loco.append(box("Tender", (-2.15, 0, 0.78), (1.05, 0.82, 0.85), GREEN))
loco.append(box("TenderCoal", (-2.15, 0, 1.24), (0.9, 0.68, 0.10), BLACK))
for wx in (-2.45, -1.85):
    for sd in (-1, 1):
        w = wheel(f"TenderWheel{wx}_{sd}", 0.26, IRON, BLACK, 0.05)
        xform(w, Matrix.Rotation(math.radians(90), 4, 'X'))
        place(w, (wx, sd * 0.42, 0.26)); loco += w
place(loco, (-4.12, -1.38, 0), ry=math.radians(26))

# ---- horse-drawn carriage (right foreground) ----
car = []
car.append(box("CarriageBody", (0, 0, 1.02), (1.55, 0.95, 1.05), BURG))
car.append(box("CarriageRoof", (0, 0, 1.62), (1.65, 1.0, 0.10), BLACK))
car.append(box("CarriageDoor", (-0.1, -0.49, 1.05), (0.62, 0.02, 0.85), BROWN))
car.append(box("DriverBox", (1.05, 0, 1.28), (0.4, 0.8, 0.18), WOOD_D))
for wx, wr in ((-0.62, 0.52), (0.62, 0.38)):
    for sd in (-1, 1):
        w = wheel(f"CarWheel{wx}_{sd}", wr, WOOD_D, BRASS, 0.05)
        xform(w, Matrix.Rotation(math.radians(90), 4, 'X'))
        place(w, (wx, sd * 0.55, wr)); car += w
car.append(strut("ShaftL", (0.85, -0.30, 0.85), (1.95, -0.28, 0.92), 0.03, WOOD_D))
car.append(strut("ShaftR", (0.85, 0.30, 0.85), (1.95, 0.28, 0.92), 0.03, WOOD_D))
horse = []
horse.append(sphere("HorseBody", (0, 0, 1.08), 0.36, BROWN, scale=(1.65, 0.66, 0.78)))
horse.append(box("HorseNeck", (0.62, 0, 1.30), (0.42, 0.20, 0.30), BROWN, rot=(0, math.radians(-38), 0)))
horse.append(box("HorseHead", (0.88, 0, 1.52), (0.44, 0.17, 0.20), BROWN, rot=(0, math.radians(24), 0)))
horse.append(frustum("HorseEarL", (0.72, -0.07, 1.66), 0.03, 0.005, 0.10, BROWN, 8))
horse.append(frustum("HorseEarR", (0.72, 0.07, 1.66), 0.03, 0.005, 0.10, BROWN, 8))
horse.append(frustum("HorseTail", (-0.62, 0, 1.05), 0.09, 0.02, 0.55, HAIR_D, 10, rot=(0, math.radians(24), 0)))
for lx, lz in ((-0.42, 0), (0.42, 0)):
    for sd in (-1, 1):
        horse.append(strut(f"HorseLeg{lx}_{sd}", (lx, sd * 0.16, 0.85), (lx + 0.05, sd * 0.17, 0.04), 0.045, BROWN))
place(horse, (2.45, 0, 0))
car += horse
place(car, (4.75, -0.85, 0), ry=math.radians(180 + 15))

# ---- boat under sail (left, elevated on struts as if flying) ----
boat = []
boat.append(sphere("BoatHull", (0, 0, 0), 0.55, HULL, scale=(2.3, 0.52, 0.42)))
boat.append(box("BoatDeck", (0, 0, 0.16), (1.85, 0.5, 0.07), WOOD_M))
boat.append(cyl("BoatMast", (-0.1, 0, 1.05), 0.028, 1.95, WOOD_D, 10))
sail = tri_panel("BoatSail", 1.05, 1.55, 0.015, SAIL); place([sail], (-0.06, 0.02, 0.28)); boat.append(sail)
boat.append(box("BoatStrutA", (-0.6, 0, -0.72), (0.05, 0.05, 1.05), STRUTD))
boat.append(box("BoatStrutB", (0.6, 0, -0.72), (0.05, 0.05, 1.05), STRUTD))
place(boat, (-5.05, 0.95, 1.25), ry=math.radians(-18), lean=math.radians(6))

# ---- two-masted ship (right, elevated) ----
ship = []
ship.append(sphere("ShipHull", (0, 0, 0), 0.5, HULL, scale=(2.1, 0.5, 0.45)))
ship.append(box("ShipDeck", (0, 0, 0.15), (1.6, 0.45, 0.06), WOOD_M))
for mx in (-0.35, 0.35):
    ship.append(cyl(f"ShipMast{mx}", (mx, 0, 0.95), 0.024, 1.7, WOOD_D, 10))
    s1 = tri_panel(f"ShipSail{mx}", 0.62, 1.15, 0.015, SAIL); place([s1], (mx + 0.03, 0.02, 0.35)); ship.append(s1)
ship.append(box("ShipStrutA", (-0.5, 0, -0.85), (0.05, 0.05, 1.2), STRUTD))
ship.append(box("ShipStrutB", (0.5, 0, -0.85), (0.05, 0.05, 1.2), STRUTD))
place(ship, (5.15, 1.05, 1.45), ry=math.radians(16), lean=math.radians(-5))

# ---- great fish (upper left, on a slim strut) ----
fish = []
fish.append(sphere("FishBody", (0, 0, 0), 0.42, OCEAN, scale=(2.4, 0.55, 0.72)))
tail = tri_panel("FishTail", 0.5, 0.62, 0.03, OCEAN); place([tail], (0.98, 0, -0.28), ry=math.radians(-90)); fish.append(tail)
fish.append(frustum("FishFin", (0.1, 0, 0.32), 0.16, 0.02, 0.26, OCEAN, 4))
fish.append(box("FishStrut", (0, 0, -1.60), (0.045, 0.045, 2.9), STRUTD))
place(fish, (-3.35, 1.35, 3.05), ry=math.radians(-14))

# ---- polar bear (left mid) ----
bear = []
bear.append(sphere("BearBody", (0, 0, 0.62), 0.44, BEAR, scale=(1.55, 0.72, 0.80)))
bear.append(sphere("BearHead", (0.72, 0, 0.66), 0.21, BEAR, scale=(1.1, 0.85, 0.85)))
bear.append(box("BearSnout", (0.92, 0, 0.58), (0.18, 0.14, 0.13), BEAR))
bear.append(sphere("BearEarL", (0.62, -0.12, 0.84), 0.055, BEAR))
bear.append(sphere("BearEarR", (0.62, 0.12, 0.84), 0.055, BEAR))
for lx in (-0.45, 0.45):
    for sd in (-1, 1):
        bear.append(strut(f"BearLeg{lx}_{sd}", (lx, sd * 0.20, 0.45), (lx, sd * 0.21, 0.03), 0.075, BEAR))
place(bear, (-3.75, -0.55, 0), ry=math.radians(-32))

# ---- globe on stand (left foreground) ----
globe = []
globe.append(cyl("GlobeBase", (0, 0, 0.05), 0.26, 0.10, WOOD_D, 18))
globe.append(cyl("GlobePost", (0, 0, 0.32), 0.045, 0.45, WOOD_D, 12))
globe.append(torus("GlobeRing", (0, 0, 0.78), 0.475, 0.022, BRASS, rot=(0, math.radians(23), 0)))
globe.append(sphere("GlobeSphere", (0, 0, 0.78), 0.44, OCEAN))
for i, (gx, gy, gz, gs) in enumerate(((0.18, -0.30, 0.95, 0.16), (-0.28, -0.24, 0.68, 0.13), (0.05, -0.40, 0.60, 0.11), (-0.12, -0.28, 1.05, 0.10))):
    globe.append(sphere(f"GlobeLand{i}", (gx, gy, gz), gs, LAND, scale=(1, 0.45, 0.8)))
place(globe, (-2.55, -2.35, 0))

# ---- furniture cluster scattering (centre foreground) ----
sofa = []
sofa.append(box("SofaBase", (0, 0, 0.32), (1.75, 0.78, 0.5), GREEN))
sofa.append(box("SofaBack", (0, 0.34, 0.72), (1.75, 0.18, 0.62), GREEN))
sofa.append(box("SofaArmL", (-0.80, 0, 0.58), (0.16, 0.78, 0.42), GREEN))
sofa.append(box("SofaArmR", (0.80, 0, 0.58), (0.16, 0.78, 0.42), GREEN))
sofa.append(box("SofaCushL", (-0.42, -0.04, 0.60), (0.72, 0.62, 0.10), BURG))
sofa.append(box("SofaCushR", (0.42, -0.04, 0.60), (0.72, 0.62, 0.10), BURG))
place(sofa, (-0.95, -2.55, 0), ry=math.radians(14))
chair = []
chair.append(box("ChairSeat", (0, 0, 0.46), (0.48, 0.46, 0.06), BURG))
chair.append(box("ChairBack", (0, 0.22, 0.82), (0.48, 0.06, 0.72), BURG))
for sx in (-0.20, 0.20):
    for sy in (-0.19, 0.19):
        chair.append(cyl(f"ChairLeg{sx}_{sy}", (sx, sy, 0.23), 0.025, 0.46, WOOD_D, 10))
place(chair, (-2.35, -1.55, 0), ry=math.radians(48))
table = []
table.append(box("TableTop", (0, 0, 0.74), (1.15, 0.7, 0.05), WOOD_M))
for sx in (-0.50, 0.50):
    for sy in (-0.28, 0.28):
        table.append(cyl(f"TableLeg{sx}_{sy}", (sx, sy, 0.37), 0.03, 0.74, WOOD_D, 10))
table.append(frustum("TableVase", (0, 0, 0.90), 0.05, 0.10, 0.26, BLUE, 14))
place(table, (-1.55, -3.05, 0), ry=math.radians(-12))
chest = []
chest.append(box("ChestBody", (0, 0, 0.55), (1.3, 0.52, 1.1), WOOD_M))
for i in range(3):
    chest.append(box(f"ChestDrawer{i}", (0, -0.27, 0.28 + i * 0.30), (1.14, 0.015, 0.24), WOOD_L))
    chest.append(sphere(f"ChestKnob{i}a", (-0.3, -0.29, 0.28 + i * 0.30), 0.028, BRASS))
    chest.append(sphere(f"ChestKnob{i}b", (0.3, -0.29, 0.28 + i * 0.30), 0.028, BRASS))
place(chest, (0.55, -2.75, 0), ry=math.radians(-8))

# ---- cannon (centre right) ----
cannon = []
cannon.append(cyl("CannonBarrel", (0.1, 0, 0.58), 0.105, 1.55, IRON, 16, rot=(0, math.radians(90), 0)))
cannon.append(torus("CannonMuzzle", (0.88, 0, 0.58), 0.115, 0.025, IRON, rot=(0, math.radians(90), 0)))
cannon.append(frustum("CannonBreech", (-0.72, 0, 0.58), 0.13, 0.10, 0.25, IRON, 14, rot=(0, math.radians(90), 0)))
cannon.append(box("CannonTrail", (-0.55, 0, 0.28), (1.0, 0.30, 0.14), WOOD_D, rot=(0, math.radians(-14), 0)))
for sd in (-1, 1):
    w = wheel(f"CannonWheel{sd}", 0.44, WOOD_D, IRON, 0.06)
    xform(w, Matrix.Rotation(math.radians(90), 4, 'X'))
    place(w, (0.05, sd * 0.30, 0.44)); cannon += w
place(cannon, (1.40, -2.40, 0), ry=math.radians(-38))

# ---- striped lighthouse (right mid) ----
lh = []
bands = [(0.34, 0.30, RED), (0.30, 0.265, WHITE), (0.265, 0.235, RED), (0.235, 0.21, WHITE)]
z = 0.0
for i, (rb, rt, cm) in enumerate(bands):
    lh.append(frustum(f"LHBand{i}", (0, 0, z + 0.30), rb, rt, 0.60, cm, 18)); z += 0.60
lh.append(torus("LHGallery", (0, 0, z + 0.02), 0.27, 0.03, IRON))
lh.append(cyl("LHLamp", (0, 0, z + 0.22), 0.16, 0.36, GLASS, 12))
lh.append(frustum("LHCap", (0, 0, z + 0.52), 0.24, 0.02, 0.26, BLACK, 14))
place(lh, (3.55, 0.55, 0))

# ---- statue on pedestal (right mid) + great urn (elevated) ----
ped = [box("StatuePed", (0, 0, 0.5), (0.56, 0.56, 1.0), STONE),
       frustum("StatueRobe", (0, 0, 1.32), 0.17, 0.105, 0.64, STONE),
       frustum("StatueTorso", (0, 0, 1.79), 0.105, 0.08, 0.32, STONE),
       sphere("StatueHead", (0, -0.01, 2.03), 0.078, STONE),
       strut("StatueArm", (-0.09, 0, 1.85), (-0.17, -0.10, 1.58), 0.033, STONE)]
place(ped, (2.65, -0.95, 0), ry=math.radians(15))
urn = []
urn.append(cyl("UrnFoot", (0, 0, 0.05), 0.16, 0.10, BRASS, 16))
urn.append(frustum("UrnStem", (0, 0, 0.20), 0.07, 0.13, 0.22, BRASS, 16))
urn.append(sphere("UrnBelly", (0, 0, 0.52), 0.30, BRASS, scale=(1, 1, 1.15)))
urn.append(cyl("UrnNeck", (0, 0, 0.88), 0.13, 0.18, BRASS, 16))
urn.append(torus("UrnRim", (0, 0, 0.98), 0.17, 0.028, BRASS))
urn.append(box("UrnStrut", (0, 0, -0.30), (0.05, 0.05, 0.55), STRUTD))
place(urn, (1.25, 0.75, 0.62), ry=math.radians(0))

# ---- barrels and crates (right foreground) ----
for i, (bx, by) in enumerate(((3.35, -2.75), (3.95, -2.60), (3.62, -2.72))):
    bg = []
    bg.append(frustum(f"Barrel{i}Lo", (0, 0, 0.19), 0.26, 0.315, 0.38, WOOD_M, 14))
    bg.append(frustum(f"Barrel{i}Hi", (0, 0, 0.57), 0.315, 0.26, 0.38, WOOD_M, 14))
    bg.append(torus(f"Barrel{i}BandA", (0, 0, 0.16), 0.285, 0.018, IRON))
    bg.append(torus(f"Barrel{i}BandB", (0, 0, 0.60), 0.285, 0.018, IRON))
    place(bg, (bx, by, 0.38 if i == 2 else 0))
for i, (cx, cy, cr) in enumerate(((4.35, -2.95, 12), (4.90, -2.70, -8))):
    cg = [box(f"Crate{i}", (0, 0, 0.31), (0.62, 0.62, 0.62), WOOD_L),
          box(f"Crate{i}BattenT", (0, 0, 0.60), (0.66, 0.66, 0.05), WOOD_M),
          box(f"Crate{i}BattenB", (0, 0, 0.03), (0.66, 0.66, 0.05), WOOD_M)]
    place(cg, (cx, cy, 0), ry=math.radians(cr))

# ---- dispersing visitors, streaming both ways with bundles ----
def visitor(x, y, ry, kind, bundle=None, lean_deg=4):
    if kind == 'woman':
        f = figure_woman(f"Vis_{x}_{y}", dress=[PALE, BURG, BLUE, GREY][abs(int(x * 10)) % 4], hat='bonnet', h=1.60)
    else:
        f = figure_man(f"Vis_{x}_{y}", suit=[BLACK, BROWN, CHARC][abs(int(y * 10)) % 3],
                       hat='top' if int(abs(x)) % 2 == 0 else 'cap', h=1.74)
    if bundle == 'box':
        f.append(box(f"Bundle_{x}_{y}", (0, -0.38, 0.78), (0.34, 0.22, 0.26), LEATH))
    elif bundle == 'case':
        f.append(box(f"Portmanteau_{x}_{y}", (0.34, -0.05, 0.42), (0.16, 0.42, 0.55), LEATH))
    place(f, (x, y, 0), ry=math.radians(ry), lean=math.radians(lean_deg))
    return f

visitor(-3.15, -1.85, -52, 'man', 'box')
visitor(-2.55, -2.70, -38, 'woman')
visitor(-3.95, -2.80, -64, 'man', 'case')
visitor(-1.85, -1.15, -30, 'man')
visitor(-4.45, -0.75, -70, 'woman')
visitor(3.05, -2.25, 48, 'man', 'box')
visitor(2.15, -2.95, 34, 'woman')
visitor(4.05, -2.60, 58, 'man', 'case')
visitor(1.75, -1.30, 28, 'woman')
visitor(-0.35, -1.55, -14, 'man', None, 9)
visitor(0.85, -1.05, 18, 'woman', None, 8)
visitor(5.35, -0.45, 66, 'man')

lights_and_camera((0.6, -12.2, 5.0), (0, 0.3, 1.15), lens=36, res=(960, 690))
finish(SLUG, OUT)
