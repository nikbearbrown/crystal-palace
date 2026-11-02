"""
Build script: scan-fig54-elkington-jewel-cabinet
Jewel cabinet designed by Louis (Ludwig) Gruner for Elkington & Co., 1851
(Royal Collection). Reference: fig-54 colour photograph, front view.
NOTE: the scan's repaired area is the upper-left BACKGROUND only; the cabinet
itself is original. No repaired pixels were used as evidence.
Re-runnable: blender -b --python build_scan_fig54_elkington_jewel_cabinet.py
Scale: furniture scale, ESTIMATED (overall width 1.80 m) from the image.
"""
import bpy
import math
import os
from mathutils import Vector

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig54-elkington-jewel-cabinet"

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
model_coll = bpy.data.collections.new("Model")
bpy.context.scene.collection.children.link(model_coll)
setup_coll = bpy.data.collections.new("RenderSetup")
bpy.context.scene.collection.children.link(setup_coll)

# ---------------------------------------------------------------- materials
def make_mat(name, color, roughness=0.5, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m

GOLD = make_mat("GiltBronze", (0.72, 0.47, 0.16), roughness=0.36, metallic=1.0)
GOLD_DARK = make_mat("GiltBronzeDark", (0.44, 0.28, 0.10), roughness=0.44, metallic=1.0)
SILVER = make_mat("SilveredMetal", (0.72, 0.73, 0.76), roughness=0.30, metallic=1.0)
ENAMEL_BLUE = make_mat("EnamelBlue", (0.05, 0.12, 0.46), roughness=0.2, metallic=0.1)
ENAMEL_LIGHT = make_mat("EnamelPatternPale", (0.45, 0.52, 0.66), roughness=0.38, metallic=0.4)
MEDAL_BLUE = make_mat("MedallionBlue", (0.07, 0.17, 0.55), roughness=0.25, metallic=0.1)
WOOD = make_mat("CabinetWood", (0.15, 0.085, 0.04), roughness=0.55)
PANEL = make_mat("PortraitPanelDark", (0.035, 0.028, 0.024), roughness=0.45)
PANEL_FIG = make_mat("PortraitSilhouette", (0.14, 0.105, 0.075), roughness=0.5)

# Scallop (fish-scale) enamel texture, generated in-Blender.
def scale_texture():
    import numpy as np
    W = H = 256
    img = bpy.data.images.new("ScaleEnamelTex", W, H)
    px = np.zeros((H, W, 4), dtype=np.float32)
    cell = 32
    for y in range(H):
        row = y // (cell // 2)
        off = (cell // 2) if row % 2 else 0
        for x in range(W):
            cx = ((x + off) % cell) - cell / 2
            cy = (y % (cell // 2)) - cell / 2
            d = math.sqrt(cx * cx + cy * cy) / (cell / 2)
            shade = 0.75 + 0.45 * max(0.0, 1.0 - d)
            edge = 0.55 if d > 0.92 else 1.0
            px[y, x] = (0.10 * shade * edge, 0.20 * shade * edge,
                        0.72 * shade * edge, 1.0)
    img.pixels.foreach_set(px.ravel())
    img.pack()
    return img

def mat_with_image(name, img, color=(1, 1, 1)):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    tex = m.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = img
    m.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.22
    return m

SCALE_MAT = mat_with_image("ScaleEnamel", scale_texture())

# ---------------------------------------------------------------- helpers
def link(ob, coll=model_coll):
    for c in ob.users_collection:
        c.objects.unlink(ob)
    coll.objects.link(ob)
    return ob

def box(name, loc, dims, mat, rot=(0, 0, 0), coll=model_coll):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = dims
    bpy.ops.object.transform_apply(scale=True)
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def ball(name, loc, scale, mat, coll=model_coll):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    for p in ob.data.polygons:
        p.use_smooth = True
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def cyl(name, loc, r, h, mat, vertices=28, rot=(0, 0, 0), coll=model_coll):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=h,
                                        location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def cone(name, loc, r1, r2, depth, mat, rot=(0, 0, 0), coll=model_coll):
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=r1, radius2=r2,
                                    depth=depth, location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    for p in ob.data.polygons:
        p.use_smooth = True
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def lathe(name, profile, mat, segments=40, location=(0, 0, 0), coll=model_coll):
    verts, faces = [], []
    n = len(profile)
    for (r, z) in profile:
        for j in range(segments):
            a = 2.0 * math.pi * j / segments
            verts.append((r * math.cos(a), r * math.sin(a), z))
    for i in range(n - 1):
        for j in range(segments):
            j2 = (j + 1) % segments
            faces.append((i * segments + j, (i + 1) * segments + j,
                          (i + 1) * segments + j2, i * segments + j2))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    ob.location = location
    if mat:
        ob.data.materials.append(mat)
    return ob

def tube(name, points, radius, mat, coll=model_coll):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = radius
    cu.bevel_resolution = 2
    cu.resolution_u = 3
    spl = cu.splines.new('BEZIER')
    spl.bezier_points.add(len(points) - 1)
    for bp, co in zip(spl.bezier_points, points):
        bp.co = co
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'
    ob = bpy.data.objects.new(name, cu)
    coll.objects.link(ob)
    if mat:
        ob.data.materials.append(mat)
    return ob

def prism(name, outline, z0, z1, mat, coll=model_coll):
    """Extrude a 2D (x,y) outline between two heights."""
    n = len(outline)
    verts = [(x, y, z0) for (x, y) in outline] + [(x, y, z1) for (x, y) in outline]
    faces = []
    faces.append(tuple(reversed(range(n))))
    faces.append(tuple(range(n, 2 * n)))
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    if mat:
        ob.data.materials.append(mat)
    return ob

def chamfer_outline(hw, hd, cut):
    return [(-hw + cut, -hd), (hw - cut, -hd), (hw, -hd + cut), (hw, hd - cut),
            (hw - cut, hd), (-hw + cut, hd), (-hw, hd - cut), (-hw, -hd + cut)]

def capsule_between(name, p1, p2, r, mat, coll=model_coll):
    p1, p2 = Vector(p1), Vector(p2)
    mid = (p1 + p2) / 2
    length = (p2 - p1).length
    bpy.ops.mesh.primitive_cylinder_add(vertices=14, radius=r, depth=length,
                                        location=mid)
    ob = bpy.context.active_object
    ob.name = name
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = (p2 - p1).to_track_quat('Z', 'Y')
    if mat:
        ob.data.materials.append(mat)
    ball(name + "_J1", tuple(p1), (r, r, r), mat, coll)
    ball(name + "_J2", tuple(p2), (r, r, r), mat, coll)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll)

def silver_figure(name, base_loc, height, mat=SILVER, facing=0.0):
    """Simplified classical draped female figure (stylised, no facial detail).
    Proportions: skirt 0-0.55h, torso ~0.68h, neck 0.78-0.86h, head ~0.90h,
    all parts overlapping so the figure reads as one form."""
    x, y, z0 = base_loc
    h = height
    s = h / 0.72
    prof = [(0.001, 0.0), (0.100 * s, 0.0), (0.094 * s, 0.05 * h),
            (0.070 * s, 0.28 * h), (0.055 * s, 0.46 * h),
            (0.049 * s, 0.56 * h)]
    lathe(name + "_Skirt", prof, mat, segments=28, location=(x, y, z0))
    ball(name + "_Torso", (x, y, z0 + 0.665 * h),
         (0.050 * s, 0.038 * s, 0.088 * h / 0.72 * 0.72), mat)
    cyl(name + "_Neck", (x, y, z0 + 0.815 * h), 0.021 * s, 0.09 * h, mat)
    ball(name + "_Head", (x, y, z0 + 0.905 * h),
         (0.034 * s, 0.032 * s, 0.044 * s), mat)
    ball(name + "_HairBun", (x, y - 0.030 * s, z0 + 0.925 * h),
         (0.020 * s, 0.018 * s, 0.022 * s), mat)
    capsule_between(name + "_ArmL",
                    (x - 0.048 * s, y + 0.010, z0 + 0.74 * h),
                    (x - 0.080 * s, y + 0.034, z0 + 0.50 * h), 0.019 * s, mat)
    capsule_between(name + "_ArmR",
                    (x + 0.048 * s, y + 0.010, z0 + 0.74 * h),
                    (x + 0.070 * s, y - 0.024, z0 + 0.53 * h), 0.019 * s, mat)

# ---------------------------------------------------------------- carcass
OUTLINE = chamfer_outline(0.90, 0.29, 0.17)
prism("Plinth_Foot", OUTLINE, 0.0, 0.055, GOLD_DARK)
prism("Plinth_Body", chamfer_outline(0.885, 0.28, 0.16), 0.055, 0.235, WOOD)
# gilt frieze band on plinth front with scroll curls and portrait medallions
box("Plinth_Frieze", (0, 0.272, 0.155), (1.46, 0.018, 0.115), GOLD)
for sx in (-0.80, 0.80):
    box(f"Plinth_FriezeSide_{sx:+.0f}", (sx * 0.94, 0.155, 0.155),
        (0.20, 0.30, 0.115), GOLD)
for i in range(9):
    cx = -0.60 + i * 0.15
    pts = []
    for k in range(11):
        t = k / 10 * 4.6
        r = 0.030 * (1 - t / 6.2)
        pts.append((cx + r * math.cos(t + i), 0.284, 0.155 + r * math.sin(t + i)))
    tube(f"FriezeScroll_{i}", pts, 0.0055, GOLD_DARK)
for i, mx in enumerate((-0.475, -0.158, 0.158, 0.475)):
    cyl(f"PortraitMedallion_{i}", (mx, 0.283, 0.155), 0.047, 0.012, MEDAL_BLUE,
        rot=(math.pi / 2, 0, 0))
    ball(f"MedallionBust_{i}", (mx, 0.292, 0.163), (0.016, 0.008, 0.020), ENAMEL_LIGHT)
    cone(f"MedallionBustBase_{i}", (mx, 0.292, 0.138), 0.020, 0.010, 0.022,
         ENAMEL_LIGHT, rot=(-math.pi / 2, 0, 0))

prism("Body_Carcass", chamfer_outline(0.86, 0.26, 0.15), 0.235, 0.93, WOOD)
box("Body_FrontGround", (0, 0.245, 0.585), (1.47, 0.02, 0.66), GOLD_DARK)

# ---------------------------------------------------------------- portrait panels
def portrait_panel(name, cx, figures):
    cz = 0.585
    box(name + "_FrameOuter", (cx, 0.252, cz), (0.66, 0.022, 0.70), GOLD)
    # pale patterned enamel border: instanced small diamonds
    src = box(name + "_BorderSrc", (0, -5, -5), (0.030, 0.010, 0.030), ENAMEL_LIGHT)
    positions = []
    for k in range(15):
        positions.append((cx - 0.285 + k * 0.0407, cz + 0.315))
        positions.append((cx - 0.285 + k * 0.0407, cz - 0.315))
    for k in range(13):
        positions.append((cx - 0.305, cz - 0.262 + k * 0.0407))
        positions.append((cx + 0.305, cz - 0.262 + k * 0.0407))
    for i, (px, pz) in enumerate(positions):
        d = src.copy()
        d.name = f"{name}_Border_{i}"
        d.location = (px, 0.274, pz)
        d.scale = (1.35, 1.35, 1.35)
        d.rotation_euler = (0, 0, math.pi / 4)
        model_coll.objects.link(d)
    bpy.data.objects.remove(src, do_unlink=True)
    box(name + "_Panel", (cx, 0.258, cz), (0.545, 0.014, 0.585), PANEL)
    for j, (fx, fs) in enumerate(figures):
        ball(f"{name}_Figure{j}", (cx + fx, 0.268, cz - 0.045), (0.072 * fs, 0.012, 0.115 * fs), PANEL_FIG)
        ball(f"{name}_Figure{j}Head", (cx + fx, 0.270, cz + 0.075 * fs), (0.032 * fs, 0.012, 0.040 * fs), PANEL_FIG)

# Screen-left panel (+X in this scene's camera convention): Queen Victoria
# with a child (abstract silhouettes, no faces).
portrait_panel("PanelVictoria", 0.435, [(-0.09, 1.15), (0.13, 0.72)])
# Screen-right panel: Prince Albert (single taller silhouette).
portrait_panel("PanelAlbert", -0.435, [(0.0, 1.3)])

# ---------------------------------------------------------------- central niche + figure
prof_niche = [(-0.16, 0.30), (0.16, 0.30), (0.16, 0.78)]
# niche back panel with arch: built from a box + half-cylinder top, recessed dark
box("Niche_Back", (0, 0.238, 0.60), (0.30, 0.012, 0.52), PANEL)
cyl("Niche_Arch", (0, 0.238, 0.86), 0.15, 0.012, PANEL, vertices=28,
    rot=(math.pi / 2, 0, 0))
box("Niche_Frame", (-0.175, 0.252, 0.585), (0.05, 0.02, 0.63), GOLD)
box("Niche_FrameR", (0.175, 0.252, 0.585), (0.05, 0.02, 0.63), GOLD)
cyl("Niche_FrameArch", (0, 0.252, 0.90), 0.175, 0.02, GOLD, vertices=28,
    rot=(math.pi / 2, 0, 0))
cyl("Niche_Pedestal", (0, 0.252, 0.315), 0.055, 0.09, GOLD_DARK, vertices=8)
silver_figure("NicheFigure", (0, 0.252, 0.36), 0.52)

# ---------------------------------------------------------------- corner figures
for sx, nm in ((-1, "CornerFigure_L"), (1, "CornerFigure_R")):
    box(nm + "_Plinth", (sx * 0.795, 0.185, 0.245), (0.20, 0.24, 0.03), GOLD_DARK)
    silver_figure(nm, (sx * 0.795, 0.195, 0.26), 0.66)

# ---------------------------------------------------------------- cornice + dentils
prism("Cornice_Lower", chamfer_outline(0.90, 0.295, 0.17), 0.93, 0.965, GOLD)
for i in range(37):
    box(f"Dentil_{i}", (-0.80 + i * 0.0445, 0.288, 0.978), (0.024, 0.014, 0.026), GOLD_DARK)
prism("Cornice_Upper", chamfer_outline(0.92, 0.305, 0.18), 0.99, 1.025, GOLD)

# ---------------------------------------------------------------- roof
# hipped cap: frustum built as a prism pair (lower gilt slope + blue front panel)
def frustum(name, hw0, hd0, hw1, hd1, z0, z1, mat):
    ob = prism(name, chamfer_outline(hw0, hd0, 0.001), z0, z0 + 0.001, mat)
    # rebuild manually: simpler - two stacked thin prisms read as slope steps
    return ob

# stepped gilt roof slopes (front/back/ends suggested by stacked chamfered slabs)
prism("Roof_Step1", chamfer_outline(0.93, 0.31, 0.18), 1.025, 1.075, GOLD_DARK)
prism("Roof_Step2", chamfer_outline(0.82, 0.26, 0.14), 1.075, 1.125, GOLD)
prism("Roof_Step3", chamfer_outline(0.68, 0.205, 0.10), 1.125, 1.175, GOLD_DARK)
# blue scale-enamel front slope panel, mounted proud of the roof steps.
# NOTE: this file's box() bakes world coordinates into the mesh (object
# origin stays at 0,0,0), so setting object rotation would swing the panel
# about the world origin. Build the tilted panel directly in world space.
def tilted_panel(name, centre, width, height, thick, tilt, mat):
    import math as _m
    cx, cy, cz = centre
    c, s = _m.cos(tilt), _m.sin(tilt)
    corn = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                lx, ly, lz = sx * width / 2, sy * thick / 2, sz * height / 2
                corn.append((cx + lx, cy + ly * c - lz * s, cz + ly * s + lz * c))
    # corner index = 4*(sx>0) + 2*(sy>0) + (sz>0), matching the loop order
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1),
             (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(corn, [], faces)
    me.update()
    # simple planar UVs from the un-tilted local coords (texture needs them)
    uvs = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                uvs.append((sx * 0.5 + 0.5, sz * 0.5 + 0.5))
    uv_layer = me.uv_layers.new(name="UVMap")
    for loop in me.loops:
        uv_layer.data[loop.index].uv = uvs[loop.vertex_index]
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    return link(ob, model_coll)

tilted_panel("Roof_BlueScalePanel", (0, 0.272, 1.124), 1.10, 0.21, 0.012,
             0.545, SCALE_MAT)
box("Roof_TopPlateau", (0, 0, 1.185), (1.06, 0.30, 0.03), GOLD)

# ---------------------------------------------------------------- crest: putti + lion
cyl("Crest_Pedestal", (0, 0, 1.245), 0.075, 0.09, GOLD_DARK, vertices=8)
box("Crest_PedestalTop", (0, 0, 1.30), (0.13, 0.13, 0.025), GOLD)
# lion (stylised heraldic, standing)
lx, lz = 0, 1.312
ball("Lion_Body", (lx, 0, lz + 0.075), (0.085, 0.038, 0.045), GOLD)
ball("Lion_Head", (lx - 0.088, 0, lz + 0.105), (0.034, 0.032, 0.036), GOLD)
cone("Lion_Muzzle", (lx - 0.118, 0, lz + 0.098), 0.016, 0.008, 0.03, GOLD,
     rot=(0, -math.pi / 2, 0))
for dx, dy in ((-0.055, 0.02), (-0.055, -0.02), (0.055, 0.02), (0.055, -0.02)):
    cyl(f"Lion_Leg_{dx}_{dy}", (lx + dx, dy, lz + 0.032), 0.010, 0.065, GOLD)
tube("Lion_Tail", [(lx + 0.088, 0, lz + 0.10), (lx + 0.115, 0, lz + 0.14),
                   (lx + 0.10, 0, lz + 0.175)], 0.007, GOLD)
# putti flanking (stylised kneeling cherubs, silver)
for sx, nm in ((-1, "Putto_L"), (1, "Putto_R")):
    px = sx * 0.185
    ball(nm + "_Body", (px, 0, 1.245), (0.038, 0.034, 0.052), SILVER)
    ball(nm + "_Head", (px + sx * 0.008, 0, 1.315), (0.026, 0.025, 0.028), SILVER)
    ball(nm + "_Knee", (px + sx * 0.045, 0.01, 1.205), (0.030, 0.028, 0.020), SILVER)
    capsule_between(nm + "_Arm", (px + sx * 0.02, 0.01, 1.27),
                    (px - sx * 0.055, 0.01, 1.30), 0.011, SILVER)
    ball(nm + "_Wing", (px + sx * 0.045, -0.028, 1.285), (0.014, 0.008, 0.034), SILVER)

# ---------------------------------------------------------------- render setup
def look_at(ob, target):
    ob.rotation_euler = (Vector(target) - ob.location).to_track_quat('-Z', 'Y').to_euler()

bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -0.001))
ground = bpy.context.active_object
ground.name = "GroundPlane"
gm = make_mat("BackdropGrey", (0.45, 0.44, 0.43), roughness=1.0)
ground.data.materials.append(gm)
link(ground, setup_coll)

bpy.ops.object.camera_add(location=(0.45, 3.35, 1.06))
cam = bpy.context.active_object
cam.name = "PreviewCamera"
cam.data.lens = 50
look_at(cam, (0, 0, 0.64))
link(cam, setup_coll)
bpy.context.scene.camera = cam

def add_light(name, loc, energy, size):
    bpy.ops.object.light_add(type='AREA', location=loc)
    li = bpy.context.active_object
    li.name = name
    li.data.energy = energy
    li.data.shape = 'DISK'
    li.data.size = size
    look_at(li, (0, 0, 0.6))
    return link(li, setup_coll)

add_light("KeyLight", (1.6, 2.2, 2.4), 95, 1.2)
add_light("FillLight", (-1.8, 1.6, 1.0), 32, 1.6)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.03
scene.render.resolution_percentage = 85
scene.cycles.use_denoising = True
scene.render.resolution_x = 960
scene.render.resolution_y = 720
scene.world = bpy.data.worlds.new("GreyWorld")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.45, 0.44, 0.43, 1)
scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.5

def tri_count(coll):
    total = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for ob in coll.objects:
        ev = ob.evaluated_get(dg)
        try:
            me = ev.to_mesh()
            total += sum(len(p.vertices) - 2 for p in me.polygons)
            ev.to_mesh_clear()
        except Exception:
            pass
    return total

print(f"TRIANGLES: {tri_count(model_coll)}")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, SLUG + ".blend"))
bpy.ops.object.select_all(action='DESELECT')
for ob in model_coll.objects:
    ob.select_set(True)
bpy.context.view_layer.objects.active = model_coll.objects[0]
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT_DIR, SLUG + ".glb"),
                          export_format='GLB', use_selection=True, export_apply=True)
bpy.ops.object.select_all(action='DESELECT')
scene.render.filepath = os.path.join(OUT_DIR, "preview.png")
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
