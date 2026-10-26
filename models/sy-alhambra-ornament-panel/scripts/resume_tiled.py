#!/usr/bin/env python3
"""Build sy-alhambra-ornament-panel in Blender (headless, re-runnable).

Run scripts/make_textures.py first (system python3 + PIL), then:
  blender -b --python scripts/build_sy_alhambra_ornament_panel.py

One repeatable wall panel of the Sydenham Alhambra Court (1854) plus a
narrow quatrefoil-medallion strip, composed as one bay unit. All pattern
evidence and the measured/derived/inferred status of every dimension
are in ../NOTES.md. Sydenham 1854 only.
"""
import bpy, bmesh, math, os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
TEX = os.path.join(ROOT, "textures")

# ------------------------------------------------------------------ dims
# MEASURED on the 1856 guide p.66 woodcut (visual grounding, see NOTES):
#   dado zone = 24.7% of entrance-wall height; medallion strip width
#   = 0.154 x wall height; dado diamonds w:h = 2:1.
# DERIVED: zone heights below apply the measured dado fraction to the
#   adopted panel height; sebka diamond proportions from the woodcut's
#   upper-wall diaper.
# ADOPTED (no dimension printed anywhere): overall panel height 3.60 m
#   (a dressing height within the side-aisle courts; the court's Court
#   of Lions arches were full-size per guide p.69, but no wall-panel
#   dimension is attested) and width 3.60 m so the unit is square and
#   the sebka net divides exactly.
PANEL_W   = 3.60
PANEL_H   = 3.60
SLAB_T    = 0.12            # slab thickness (adopted)
SKIRT_T   = 0.12
DADO_T    = 0.86            # dado top  (0.86/3.60 = 23.9% ~ measured 24.7%)
ZIG_T     = 0.98
INSC_T    = 1.16
FIELD_T   = 3.10
FRIEZE_T  = 3.43
SEB_W     = 0.45            # sebka diamond width  (8 across)
SEB_H     = 0.485           # sebka diamond height (4 rows of centres x2)
STRIP_W   = 0.56            # medallion strip width (0.154 x 3.60 = 0.554)
STRIP_X   = -(PANEL_W / 2 + STRIP_W / 2)   # strip centre x (abuts panel)

# ------------------------------------------------------------------ setup
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

model = bpy.data.collections.new("Model")
scene.collection.children.link(model)
setup = bpy.data.collections.new("RenderSetup")
scene.collection.children.link(setup)

def mat_principled(name, color, rough=0.72):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return m

def mat_textured(name, color_png, bump_png, rough=0.62):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree.nodes
    lk = m.node_tree.links
    bsdf = nt["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = rough
    tex = nt.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(os.path.join(TEX, color_png))
    tex.image.colorspace_settings.name = 'sRGB'
    lk.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bmp = nt.new("ShaderNodeTexImage")
    bmp.image = bpy.data.images.load(os.path.join(TEX, bump_png))
    bmp.image.colorspace_settings.name = 'Non-Color'
    bump = nt.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.55
    bump.inputs["Distance"].default_value = 0.012
    lk.new(bmp.outputs["Color"], bump.inputs["Height"])
    lk.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return m

IVORY = (0.80, 0.68, 0.47)
BLUE_SRGB = (0.10, 0.19, 0.38)
mat_stucco = mat_principled("StuccoPlain", IVORY, 0.8)
mat_back = mat_principled("SlabBack", (0.55, 0.47, 0.35), 0.9)
mat_rib = mat_principled("SebkaRibBlue", BLUE_SRGB, 0.6)
mat_gold = mat_principled("GoldTrim", (0.62, 0.45, 0.18), 0.5)
mat_panel = mat_textured("PanelFront", "panel_front.png", "panel_bump.png")
mat_strip = mat_textured("StripFront", "strip_front.png", "strip_bump.png")

def box(name, sx, sy, sz, loc, mat, coll=model):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        ob.data.materials.append(mat)
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    coll.objects.link(ob)
    return ob

def front_plane(name, w, h, cx, y, mat):
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(cx, y, h / 2))
    ob = bpy.context.active_object
    ob.name = name
    ob.rotation_euler = (math.radians(90), 0, 0)   # face -Y
    ob.dimensions = (w, h, 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.data.materials.append(mat)
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    model.objects.link(ob)
    return ob

FRONT_Y = -SLAB_T / 2 - 0.001

# ------------------------------------------------------------------ panel
box("PanelSlab", PANEL_W, SLAB_T, PANEL_H, (0, 0, PANEL_H / 2), mat_stucco)
front_plane("PanelFront", PANEL_W, PANEL_H, 0, FRONT_Y, mat_panel)

# sebka ribs: thin blue bars along the net edges (same grid as texture).
# Each net edge is generated ONCE (two of the four diagonal directions per
# grid point) and all bars are built into a single bmesh with an identity
# object transform. (First build drew every edge twice as exactly
# coincident joined cubes; the coincident pairs self-shadowed in Cycles
# and rendered black -- see NOTES.md QC.)
import bmesh
from mathutils import Matrix
rows = int(round((FIELD_T - INSC_T) / (SEB_H / 2)))
seg_len = math.hypot(SEB_W / 2, SEB_H / 2)
ang = math.atan2(SEB_H / 2, SEB_W / 2)
bm = bmesh.new()
n_seg = 0
for j in range(rows + 1):
    cz = FIELD_T - j * (SEB_H / 2)
    off = (SEB_W / 2) if j % 2 else 0.0
    cx = -PANEL_W / 2 - SEB_W + off
    while cx < PANEL_W / 2 + SEB_W:
        for (dx, dz, a) in ((SEB_W / 4, SEB_H / 4, -ang), (SEB_W / 4, -SEB_H / 4, ang)):
            mx, mz = cx + dx, cz + dz
            if -PANEL_W / 2 - 0.05 <= mx <= PANEL_W / 2 + 0.05 and INSC_T - 0.02 <= mz <= FIELD_T + 0.02:
                ret = bmesh.ops.create_cube(bm, size=1.0)
                vs = ret["verts"]
                bmesh.ops.scale(bm, verts=vs, vec=(seg_len + 0.012, 0.016, 0.034))
                bmesh.ops.rotate(bm, verts=vs, cent=(0, 0, 0),
                                 matrix=Matrix.Rotation(a, 3, 'Y'))
                bmesh.ops.translate(bm, verts=vs, vec=(mx, FRONT_Y - 0.008, mz))
                n_seg += 1
        cx += SEB_W
rib_mesh = bpy.data.meshes.new("SebkaRibsMesh")
bm.to_mesh(rib_mesh)
bm.free()
ribs = bpy.data.objects.new("SebkaRibs", rib_mesh)
model.objects.link(ribs)
rib_mesh.materials.append(mat_rib)
print(f"sebka segments: {n_seg}")

# vertical frame battens closing the field's left/right edges
for sgn in (-1, 1):
    box("FieldFrame", 0.05, 0.032, FIELD_T - INSC_T,
        (sgn * (PANEL_W / 2 - 0.025), -SLAB_T / 2 - 0.008, (INSC_T + FIELD_T) / 2), mat_stucco)

# roundel rings (flat annuli over the painted roundels)
ring_objs = []
for k in range(8):
    cx = -PANEL_W / 2 + 0.225 + k * 0.45
    cz = (FIELD_T + FRIEZE_T) / 2
    bpy.ops.mesh.primitive_torus_add(major_radius=0.112, minor_radius=0.014,
                                     major_segments=24, minor_segments=6,
                                     location=(cx, FRONT_Y - 0.004, cz),
                                     rotation=(math.radians(90), 0, 0))
    ring_objs.append(bpy.context.active_object)
bpy.ops.object.select_all(action='DESELECT')
for ob in ring_objs:
    ob.select_set(True)
bpy.context.view_layer.objects.active = ring_objs[0]
bpy.ops.object.join()
rings = bpy.context.active_object
rings.name = "RoundelRings"
rings.data.materials.append(mat_rib)
for c in list(rings.users_collection):
    c.objects.unlink(rings)
model.objects.link(rings)

# horizontal ledges at zone boundaries + cornice steps
for (nm, zz, dep) in (("LedgeFieldBase", INSC_T, 0.030), ("LedgeFieldTop", FIELD_T, 0.030),
                      ("CorniceLow", FRIEZE_T, 0.036), ("CorniceHigh", 3.545, 0.030)):
    box(nm, PANEL_W, dep, 0.045, (0, -SLAB_T / 2 - dep / 2 + 0.012, zz), mat_stucco)

# ------------------------------------------------------------------ strip
box("StripSlab", STRIP_W, SLAB_T, PANEL_H, (STRIP_X, 0, PANEL_H / 2), mat_stucco)
front_plane("StripFront", STRIP_W, PANEL_H, STRIP_X, FRONT_Y, mat_strip)
for sgn in (-1, 1):
    box("StripRail", 0.045, 0.026, PANEL_H,
        (STRIP_X + sgn * (STRIP_W / 2 - 0.0225), -SLAB_T / 2 - 0.006, PANEL_H / 2), mat_stucco)

# ------------------------------------------------------------------ render setup
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"
ground.data.materials.append(mat_principled("GroundGrey", (0.42, 0.42, 0.42), 0.95))
for c in list(ground.users_collection):
    c.objects.unlink(ground)
setup.objects.link(ground)

world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.9

bpy.ops.object.light_add(type='SUN', location=(4, -6, 8))
sun = bpy.context.active_object
sun.data.energy = 3.2
sun.rotation_euler = (math.radians(48), math.radians(12), math.radians(-32))
for c in list(sun.users_collection):
    c.objects.unlink(sun)
setup.objects.link(sun)

bpy.ops.object.light_add(type='AREA', location=(-5, -7, 5))
fill = bpy.context.active_object
fill.data.energy = 900
fill.data.shape = 'RECTANGLE'
fill.data.size = 6
fill.data.size_y = 4
from mathutils import Vector as _V
def point_at(ob, target):
    ob.rotation_euler = (_V(target) - ob.location).to_track_quat('-Z', 'Y').to_euler()
point_at(fill, (-0.3, 0, 1.6))
for c in list(fill.users_collection):
    c.objects.unlink(fill)
setup.objects.link(fill)

UNIT_CX = STRIP_X - STRIP_W / 2 + (PANEL_W / 2 - (STRIP_X - STRIP_W / 2)) / 2  # ~ -0.28
UNIT_CX = (STRIP_X - STRIP_W / 2 + PANEL_W / 2) / 2

def make_cam(name, loc, target, lens=42):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.active_object
    cam.name = name
    cam.data.lens = lens
    point_at(cam, target)
    for c in list(cam.users_collection):
        c.objects.unlink(cam)
    setup.objects.link(cam)
    return cam

cam_front = make_cam("CamFront", (UNIT_CX, -8.2, 1.85), (UNIT_CX, 0, 1.78))
cam_side = make_cam("CamSide", (8.2, -0.6, 1.85), (0.4, 0, 1.75))
cam_tq = make_cam("CamThreeQuarter", (4.4, -5.8, 3.6), (-0.35, 0, 1.55))
cam_tiled = make_cam("CamTiled", (UNIT_CX, -13.5, 1.9), (UNIT_CX, 0, 1.75), lens=40)

# tiled arrangement: two extra bay units (render-only copies)
tiled = bpy.data.collections.new("TiledSetup")
scene.collection.children.link(tiled)
src_objs = list(model.objects)
for rep in (-1, 1):
    for ob in src_objs:
        cp = ob.copy()
        cp.data = ob.data
        cp.location = ob.location + _V((rep * (PANEL_W + STRIP_W), 0, 0))
        tiled.objects.link(cp)

scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'

REND = os.path.join(ROOT, "renders")
os.makedirs(REND, exist_ok=True)

def render(cam, path, rx, ry, colls_on):
    for coll in (model, tiled, setup):
        coll.hide_render = coll not in colls_on
    scene.camera = cam
    scene.render.resolution_x = rx
    scene.render.resolution_y = ry
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)

# RESUME VARIANT: front/side/three-quarter already rendered by the main
# build before a VM restart killed it during the tiled render; the scene
# construction above is byte-identical, so only the tiled render is redone.
render(cam_tiled, os.path.join(REND, "tiled-front.png"), 1600, 1000, (tiled, model, setup))
for coll in (model, tiled, setup):
    coll.hide_render = False

# ------------------------------------------------------------------ export
for img in bpy.data.images:
    try:
        img.pack()
    except Exception:
        pass
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "sy-alhambra-ornament-panel.blend"))

bpy.ops.object.select_all(action='DESELECT')
for ob in model.objects:
    ob.select_set(True)
bpy.context.view_layer.objects.active = list(model.objects)[0]
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT, "sy-alhambra-ornament-panel.glb"),
                          export_format='GLB', use_selection=True)

# ------------------------------------------------------------------ report
dg = bpy.context.evaluated_depsgraph_get()
tris = 0
for ob in model.objects:
    if ob.type == 'MESH':
        ev = ob.evaluated_get(dg)
        tris += sum(len(p.vertices) - 2 for p in ev.data.polygons)
print(f"ALHAMBRA-PANEL objects={len(model.objects)} tris={tris} "
      f"bbox_x={STRIP_X - STRIP_W/2:.2f}..{PANEL_W/2:.2f} h={PANEL_H}")
