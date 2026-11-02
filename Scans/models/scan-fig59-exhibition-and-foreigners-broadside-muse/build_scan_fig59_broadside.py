#!/usr/bin/env python3
"""Build scan-fig59-exhibition-and-foreigners-broadside: the song broadside
"The Exhibition and Foreigners" (E. Hodges, 1851) as a physical sheet pasted
on a wooden hoarding. Blender 4.5.3, metres, origin at base centre. Re-runnable:
  blender -b --python build_scan_fig59_broadside.py
Outputs .blend, .glb, preview.png beside this script. No lettering anywhere:
the print is suggested by blank tonal layout blocks only."""
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

PAPER  = mat("PaperAged", (0.88, 0.83, 0.70), 0.95)
PAPER_D = mat("PaperShadow", (0.78, 0.72, 0.58), 0.95)
INK    = mat("PrintInk", (0.16, 0.13, 0.10), 0.9)
INK_SOFT = mat("PrintInkSoft", (0.45, 0.40, 0.33), 0.9)
LINE   = mat("TextLine", (0.52, 0.47, 0.38), 0.95)
STAMP  = mat("LibraryStamp", (0.35, 0.42, 0.55), 0.9)
WOOD_D = mat("WoodDark", (0.26, 0.17, 0.09), 0.9)
WOOD_M = mat("WoodMid", (0.42, 0.28, 0.15), 0.9)
WOOD_W = mat("WoodWeathered", (0.52, 0.42, 0.30), 0.95)
GROUND = mat("Ground", (0.55, 0.52, 0.47), 1.0)
IRON   = mat("IronDark", (0.10, 0.10, 0.11), 0.6, 0.5)

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
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=26, minor_segments=8, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    return _fin(o, material)

def sheet_mesh(name, w, h, material):
    """Slightly irregular paper sheet in XZ plane (base z=0), gentle bottom curl
    and softened torn corners, thin solid. Front faces -Y (mounted on board at y>0)."""
    import bmesh
    nx, ny = 14, 18
    verts = []
    for j in range(ny + 1):
        v = j / ny
        for i in range(nx + 1):
            u = i / nx
            x = (u - 0.5) * w
            z = v * h
            # torn-corner softening: pull extreme corners inward slightly
            cx = abs(u - 0.5) * 2.0
            cz_top = v
            if cz_top > 0.96 and cx > 0.9:
                z -= 0.012 * (cx - 0.9) * 10 * 0.3
            # curl: bottom edge lifts toward viewer (-Y), stronger at corners
            lift = 0.0
            if v < 0.16:
                t = (0.16 - v) / 0.16
                lift = 0.028 * t * t * (0.45 + 0.55 * cx)
            # slight overall billow
            y = -lift + 0.004 * math.sin(u * math.pi) * math.sin(v * math.pi)
            verts.append((x, y, z))
    faces = []
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i; b = a + 1; c = a + nx + 1; d = c + 1
            faces.append((a, c, d, b))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    sol = o.modifiers.new("sol", 'SOLIDIFY'); sol.thickness = 0.006; sol.offset = 1.0
    bpy.ops.object.modifier_apply(modifier=sol.name)
    o.select_set(False)
    if material: mesh.materials.append(material)
    return o

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
# SCENE — fig-59 "The Exhibition and Foreigners" broadside (Hodges, 1851)
# The image IS the sheet itself: model the sheet pasted on a hoarding.
# Sheet 1.55 x 2.00 m, portrait, on a weathered board fence panel.
# ============================================================
OUT = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig59-exhibition-and-foreigners-broadside"

# ---- ground ----
box("Ground", (0, 0.55, -0.03), (4.6, 3.4, 0.06), GROUND)

# ---- hoarding: two posts, horizontal rails, vertical weathered boards ----
for sx in (-1, 1):
    box(f"Post_{sx}", (sx * 1.05, 0.16, 1.15), (0.14, 0.10, 2.3), WOOD_D)
    # post feet
    box(f"PostFoot_{sx}", (sx * 1.05, 0.02, 0.06), (0.34, 0.5, 0.12), WOOD_D)
for rz in (0.45, 2.15):
    box(f"Rail_{rz}", (0, 0.145, rz), (2.3, 0.05, 0.12), WOOD_D)
for i in range(9):
    x = -1.04 + i * 0.26
    tone = WOOD_W if i % 2 == 0 else WOOD_M
    box(f"Board_{i}", (x, 0.10, 1.17), (0.245, 0.06, 2.34), tone)

# ---- the sheet (front face toward -Y) ----
SHEET_W, SHEET_H, SHEET_Z = 1.55, 2.00, 0.14
sh = sheet_mesh("Sheet", SHEET_W, SHEET_H, PAPER)
sh.location = (0, 0.062, SHEET_Z)
# paste wrinkles: two soft horizontal shadow bands on the paper
for wz in (0.52, 1.30):
    box(f"Wrinkle_{wz}", (0, 0.052, SHEET_Z + wz), (SHEET_W * 0.96, 0.004, 0.012), PAPER_D)

FY = 0.052  # front layout plane (just off the paper face)

# headline band (the big title block) — plain dark ink band, no letters
box("HeadlineBand", (0, FY - 0.004, SHEET_Z + 1.86), (1.38, 0.006, 0.15), INK)
box("RuleTop", (0, FY - 0.004, SHEET_Z + 1.755), (1.42, 0.006, 0.016), INK)
box("RuleTop2", (0, FY - 0.004, SHEET_Z + 1.735), (1.42, 0.006, 0.008), INK_SOFT)

# three caricature head vignettes — abstract ink silhouettes, no faces
def head_vignette(name, cx, kind):
    z0 = SHEET_Z + 1.36
    # vignette block (slightly darker paper patch) + frame rules
    box(f"{name}_block", (cx, FY - 0.003, z0 + 0.14), (0.44, 0.005, 0.30), PAPER_D)
    box(f"{name}_ruleT", (cx, FY - 0.005, z0 + 0.295), (0.46, 0.006, 0.010), INK)
    box(f"{name}_ruleB", (cx, FY - 0.005, z0 + 0.0), (0.46, 0.006, 0.010), INK)
    hz = z0 + 0.115
    if kind == 'turban':
        sphere(f"{name}_head", (cx, FY - 0.012, hz), 0.085, INK_SOFT, scale=(0.85, 0.45, 1.0))
        sphere(f"{name}_turban", (cx, FY - 0.012, hz + 0.075), 0.095, INK, scale=(1.05, 0.5, 0.62))
        cyl(f"{name}_plume", (cx + 0.02, FY - 0.012, hz + 0.145), 0.010, 0.06, INK, 8)
    elif kind == 'tallhat':
        sphere(f"{name}_head", (cx, FY - 0.012, hz), 0.082, INK_SOFT, scale=(0.85, 0.45, 1.0))
        cyl(f"{name}_brim", (cx, FY - 0.012, hz + 0.062), 0.115, 0.012, INK, 22)
        cyl(f"{name}_crown", (cx, FY - 0.012, hz + 0.125), 0.072, 0.115, INK, 18)
    else:  # feathered bonnet/hat in profile-ish mass
        sphere(f"{name}_head", (cx, FY - 0.012, hz), 0.082, INK_SOFT, scale=(0.85, 0.45, 1.0))
        cyl(f"{name}_brim", (cx, FY - 0.012, hz + 0.055), 0.125, 0.010, INK, 22, rot=(math.radians(10), 0, 0))
        sphere(f"{name}_crown", (cx - 0.01, FY - 0.012, hz + 0.095), 0.062, INK, scale=(1, 0.5, 0.8))
        cyl(f"{name}_feather", (cx + 0.07, FY - 0.012, hz + 0.15), 0.010, 0.11, INK, 8, rot=(0, math.radians(-18), 0))

head_vignette("VigL", -0.50, 'turban')
head_vignette("VigC", 0.0, 'tallhat')
head_vignette("VigR", 0.50, 'bonnet')

# publisher's imprint strip (blank)
box("ImprintStrip", (0, FY - 0.004, SHEET_Z + 1.315), (1.30, 0.006, 0.045), INK_SOFT)

# two verse columns: rows of thin print-line strips (no lettering)
def verse_column(name, cx, wdt, z_top, n_lines):
    for i in range(n_lines):
        z = z_top - i * 0.0375
        # vary line lengths slightly like justified verse with ragged ends
        lw = wdt * (0.86 + 0.14 * ((i * 7) % 5) / 4.0)
        box(f"{name}_ln{i:02d}", (cx - (wdt - lw) / 2, FY - 0.002, z), (lw, 0.002, 0.010), LINE)
    # stanza gaps are implicit in the spacing rhythm (every 8 lines reads as a block)

verse_column("ColL", -0.345, 0.63, SHEET_Z + 1.22, 30)
verse_column("ColR", 0.345, 0.63, SHEET_Z + 1.22, 30)
# column divider rule
box("ColRule", (0, FY - 0.003, SHEET_Z + 0.68), (0.006, 0.004, 1.06), INK_SOFT)

# library stamp: plain ring, bottom right (blank centre) — ring lies in the sheet plane
torus("Stamp", (0.56, FY - 0.004, SHEET_Z + 0.245), 0.085, 0.009, STAMP, rot=(math.radians(90), 0, 0))
cyl("StampDot", (0.56, FY - 0.004, SHEET_Z + 0.245), 0.030, 0.004, STAMP, 18, rot=(math.radians(90), 0, 0))

# paste brush + bucket at the foot of the hoarding (bill-sticker's kit, as context)
cyl("PasteBucket", (-0.95, -0.28, 0.14), 0.13, 0.28, WOOD_M, 16)
torus("BucketRim", (-0.95, -0.28, 0.285), 0.128, 0.012, IRON)
box("Brush", (-0.70, -0.33, 0.045), (0.20, 0.05, 0.03), WOOD_D, rot=(0, 0, math.radians(12)))
box("BrushBristle", (-0.795, -0.345, 0.045), (0.055, 0.055, 0.035), PAPER_D, rot=(0, 0, math.radians(12)))

lights_and_camera((-0.55, -3.1, 1.55), (0, 0, 1.12), lens=42, res=(800, 1024))
finish(SLUG, OUT)
