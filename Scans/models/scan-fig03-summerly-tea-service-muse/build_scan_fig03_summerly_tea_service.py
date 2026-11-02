"""
Build script: scan-fig03-summerly-tea-service
Felix Summerly's Tea Service, designed by Henry Cole, Minton bone china, 1846.
Reference: fig-03 photograph (two-level display arrangement).
Re-runnable: blender -b --python build_scan_fig03_summerly_tea_service.py
All dimensions in metres. Scale: real tableware scale, estimated from the
photograph's internal proportions (teapot overall height ~0.15 m).
"""
import bpy
import math
import os
from mathutils import Vector

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig03-summerly-tea-service"

# ---------------------------------------------------------------- scene reset
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for coll in list(bpy.data.collections):
    if coll.name != 'Collection':
        bpy.data.collections.remove(coll)

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

PORCELAIN = make_mat("BoneChina", (0.90, 0.885, 0.855), roughness=0.16)
PORCELAIN_IN = make_mat("BoneChinaInside", (0.93, 0.92, 0.885), roughness=0.2)
STEP_MAT = make_mat("DisplayStepDark", (0.145, 0.135, 0.125), roughness=0.92)

# ---------------------------------------------------------------- helpers
def lathe(name, profile, mat, segments=56, location=(0, 0, 0), collection=model_coll):
    """Spin a profile of (radius, z) points around the Z axis."""
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
    collection.objects.link(ob)
    ob.location = location
    if mat:
        ob.data.materials.append(mat)
    return ob

def tube(name, points, radius, mat, collection=model_coll, bevel_segments=3):
    """Tube along a 3D polyline path (list of Vector-like tuples)."""
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = radius
    cu.bevel_resolution = bevel_segments
    cu.resolution_u = 4
    spl = cu.splines.new('BEZIER')
    spl.bezier_points.add(len(points) - 1)
    for bp, co in zip(spl.bezier_points, points):
        bp.co = co
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'
    ob = bpy.data.objects.new(name, cu)
    collection.objects.link(ob)
    if mat:
        ob.data.materials.append(mat)
    return ob

def ball(name, loc, scale, mat, collection=model_coll):
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
    return ob

def cone(name, loc, r1, r2, depth, mat, rot=(0, 0, 0), collection=model_coll):
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=r1, radius2=r2,
                                    depth=depth, location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    for p in ob.data.polygons:
        p.use_smooth = True
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return ob

def box(name, loc, dims, mat, collection=model_coll):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = dims
    bpy.ops.object.transform_apply(scale=True)
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return ob

def bird_finial(name, loc, s=1.0, mat=PORCELAIN):
    """Simplified crouching bird used as teapot-lid finial (stylised).
    The bird faces the spout (+X in this scene's screen convention)."""
    parts = []
    body = ball(name + "_Body", (loc[0], loc[1], loc[2] + 0.006 * s),
                (0.015 * s, 0.010 * s, 0.009 * s), mat)
    head = ball(name + "_Head", (loc[0] + 0.013 * s, loc[1], loc[2] + 0.012 * s),
                (0.0075 * s, 0.0068 * s, 0.0068 * s), mat)
    cone(name + "_Beak", (loc[0] + 0.021 * s, loc[1], loc[2] + 0.011 * s),
         0.0032 * s, 0.0, 0.008 * s, mat, rot=(0, math.pi / 2, 0))
    cone(name + "_Tail", (loc[0] - 0.015 * s, loc[1], loc[2] + 0.010 * s),
         0.0045 * s, 0.0012 * s, 0.012 * s, mat, rot=(0, -math.pi / 3.2, 0))
    return parts

def serpent_head(name, loc, s=1.0, mat=PORCELAIN, flip=1):
    """Small stylised animal/serpent head used at handle tops and spout tip."""
    ball(name + "_Head", loc, (0.0085 * s * flip, 0.0068 * s, 0.0072 * s), mat)
    cone(name + "_Snout", (loc[0] + 0.010 * s * flip, loc[1], loc[2] - 0.001 * s),
         0.0042 * s, 0.0008 * s, 0.010 * s, mat, rot=(0, flip * math.pi / 2.25, 0))

# ---------------------------------------------------------------- display steps
# Lower platform (top z = 0.02) and rear riser (top z = 0.17), as photographed.
box("DisplayStep_Lower", (0, 0.028, 0.010), (0.72, 0.36, 0.02), STEP_MAT)
box("DisplayStep_Riser", (0, -0.128, 0.085), (0.72, 0.15, 0.17), STEP_MAT)

LOW = 0.02    # lower shelf top height
HIGH = 0.17   # upper shelf top height

# ---------------------------------------------------------------- teapot (centre, lower level)
teapot_profile = [
    (0.0, 0.000), (0.028, 0.000), (0.046, 0.004), (0.0555, 0.014),
    (0.0585, 0.028), (0.0575, 0.042), (0.052, 0.054), (0.043, 0.062),
    (0.036, 0.066), (0.0345, 0.074), (0.0345, 0.100), (0.036, 0.106),
    (0.039, 0.108),
]
lathe("Teapot_Body", teapot_profile, PORCELAIN, location=(0, 0.015, LOW))
lathe("Teapot_Lid", [
    (0.0, 0.000), (0.030, 0.000), (0.0365, 0.003), (0.0360, 0.007),
    (0.026, 0.011), (0.012, 0.014), (0.0, 0.0145),
], PORCELAIN, location=(0, 0.015, LOW + 0.106))
bird_finial("Teapot_BirdFinial", (0, 0.015, LOW + 0.118), s=1.0)

# Spout: segmented tube rising on the +X side (screen-left from the preview
# camera), bird-head tip — as photographed.
tube("Teapot_Spout", [
    (0.046, 0.015, LOW + 0.030), (0.062, 0.015, LOW + 0.050),
    (0.072, 0.015, LOW + 0.070), (0.078, 0.015, LOW + 0.086),
], 0.0115, PORCELAIN)
cone("Teapot_SpoutTip", (0.081, 0.015, LOW + 0.090), 0.0110, 0.0088, 0.016,
     PORCELAIN, rot=(0, 0.5, 0))
serpent_head("Teapot_SpoutHead", (0.087, 0.015, LOW + 0.100), s=0.95, flip=1)

# Handle: C-curve on the -X side (screen-right), serpent head at top terminal.
tube("Teapot_Handle", [
    (-0.040, 0.015, LOW + 0.098), (-0.072, 0.015, LOW + 0.096),
    (-0.088, 0.015, LOW + 0.072), (-0.084, 0.015, LOW + 0.046),
    (-0.058, 0.015, LOW + 0.026),
], 0.0062, PORCELAIN)
serpent_head("Teapot_HandleHead", (-0.048, 0.015, LOW + 0.100), s=0.9, flip=-1)

# ---------------------------------------------------------------- tea cup + saucer (left, lower)
lathe("TeaCup", [
    (0.0, 0.001), (0.020, 0.001), (0.024, 0.005), (0.036, 0.014),
    (0.0455, 0.030), (0.048, 0.046), (0.0485, 0.055),
    (0.0455, 0.055), (0.041, 0.032), (0.026, 0.015), (0.0, 0.012),
], PORCELAIN, location=(0.205, 0.045, LOW))
tube("TeaCup_Handle", [
    (0.160, 0.045, LOW + 0.044), (0.143, 0.045, LOW + 0.038),
    (0.143, 0.045, LOW + 0.024), (0.158, 0.045, LOW + 0.016),
], 0.0038, PORCELAIN)
saucer_profile = [
    (0.0, 0.0012), (0.028, 0.0012), (0.052, 0.004), (0.068, 0.010),
    (0.0725, 0.0155), (0.0705, 0.0165), (0.052, 0.0085), (0.028, 0.0042),
    (0.0, 0.0042),
]
sc = lathe("TeaSaucer_Propped", saucer_profile, PORCELAIN,
           location=(0.212, -0.028, LOW + 0.066))
sc.rotation_euler = (-1.18, 0, 0)

# ---------------------------------------------------------------- coffee cup + saucer (right, lower)
lathe("CoffeeCup", [
    (0.0, 0.001), (0.019, 0.001), (0.023, 0.005), (0.028, 0.020),
    (0.0325, 0.045), (0.0365, 0.070), (0.0375, 0.080),
    (0.0348, 0.080), (0.031, 0.048), (0.022, 0.018), (0.0, 0.013),
], PORCELAIN, location=(-0.205, 0.045, LOW))
tube("CoffeeCup_Handle", [
    (-0.240, 0.045, LOW + 0.066), (-0.256, 0.045, LOW + 0.058),
    (-0.256, 0.045, LOW + 0.038), (-0.242, 0.045, LOW + 0.028),
], 0.0038, PORCELAIN)
sc2 = lathe("CoffeeSaucer_Propped", saucer_profile, PORCELAIN,
            location=(-0.212, -0.028, LOW + 0.066))
sc2.rotation_euler = (-1.18, 0, 0)

# ---------------------------------------------------------------- slop bowl (left, upper level)
lathe("SlopBowl", [
    (0.0, 0.0015), (0.034, 0.0015), (0.040, 0.005), (0.062, 0.016),
    (0.0755, 0.036), (0.080, 0.060), (0.0805, 0.082),
    (0.0775, 0.082), (0.072, 0.048), (0.052, 0.024), (0.024, 0.014),
    (0.0, 0.013),
], PORCELAIN, location=(0.165, -0.128, HIGH))

# ---------------------------------------------------------------- ewer (right, upper level)
ewer = lathe("Ewer", [
    (0.0, 0.0015), (0.030, 0.0015), (0.042, 0.006), (0.0505, 0.022),
    (0.0525, 0.045), (0.049, 0.072), (0.038, 0.094), (0.026, 0.106),
    (0.0235, 0.122), (0.024, 0.140), (0.029, 0.152), (0.034, 0.160),
], PORCELAIN, location=(-0.165, -0.128, HIGH))
# Wavy flower-like lip: displace the top ring vertices sinusoidally.
for v in ewer.data.vertices:
    wz = v.co.z
    if wz > 0.152:
        ang = math.atan2(v.co.y, v.co.x)
        v.co.z += 0.0042 * math.cos(4 * ang) + 0.0020
tube("Ewer_Handle", [
    (-0.191, -0.128, HIGH + 0.148), (-0.227, -0.128, HIGH + 0.168),
    (-0.247, -0.128, HIGH + 0.140), (-0.243, -0.128, HIGH + 0.100),
    (-0.217, -0.128, HIGH + 0.070),
], 0.0054, PORCELAIN)
serpent_head("Ewer_HandleHead", (-0.195, -0.128, HIGH + 0.152), s=0.9, flip=-1)

# ---------------------------------------------------------------- render setup
def look_at(ob, target):
    direction = Vector(target) - ob.location
    ob.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, -0.0005))
ground = bpy.context.active_object
ground.name = "GroundPlane"
gm = make_mat("BackdropGrey", (0.42, 0.42, 0.42), roughness=1.0)
ground.data.materials.append(gm)
bpy.ops.object.select_all(action='DESELECT')
setup_coll.objects.link(ground)
model_coll.objects.unlink(ground) if ground.name in model_coll.objects else None

for ob in list(bpy.context.scene.collection.objects):
    pass
# move ground out of default collection into RenderSetup if needed
if ground in bpy.context.scene.collection.objects.values():
    bpy.context.scene.collection.objects.unlink(ground)
    setup_coll.objects.link(ground)

bpy.ops.object.camera_add(location=(0.10, 0.98, 0.40))
cam = bpy.context.active_object
cam.name = "PreviewCamera"
cam.data.lens = 50
look_at(cam, (0, -0.02, 0.13))
setup_coll.objects.link(cam)
if cam in bpy.context.scene.collection.objects.values():
    bpy.context.scene.collection.objects.unlink(cam)
    setup_coll.objects.link(cam)
bpy.context.scene.camera = cam

def add_light(name, loc, energy, size):
    bpy.ops.object.light_add(type='AREA', location=loc)
    li = bpy.context.active_object
    li.name = name
    li.data.energy = energy
    li.data.shape = 'DISK'
    li.data.size = size
    look_at(li, (0, 0, 0.08))
    if li in bpy.context.scene.collection.objects.values():
        bpy.context.scene.collection.objects.unlink(li)
        setup_coll.objects.link(li)
    return li

add_light("KeyLight", (0.55, 0.65, 0.85), 30, 0.6)
add_light("FillLight", (-0.65, 0.45, 0.35), 12, 0.8)

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
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.42, 0.42, 0.42, 1)
scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.5

# ---------------------------------------------------------------- counts, save, export
def tri_count(coll):
    total = 0
    for ob in coll.objects:
        if ob.type == 'MESH':
            total += sum(len(p.vertices) - 2 for p in ob.data.polygons)
        elif ob.type == 'CURVE':
            dg = bpy.context.evaluated_depsgraph_get()
            ev = ob.evaluated_get(dg)
            total += sum(len(p.vertices) - 2 for p in ev.to_mesh().polygons)
    return total

tris = tri_count(model_coll)
print(f"TRIANGLES: {tris}")

blend_path = os.path.join(OUT_DIR, SLUG + ".blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.ops.object.select_all(action='DESELECT')
for ob in model_coll.objects:
    ob.select_set(True)
bpy.context.view_layer.objects.active = model_coll.objects[0]
glb_path = os.path.join(OUT_DIR, SLUG + ".glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB',
                          use_selection=True, export_apply=True)
bpy.ops.object.select_all(action='DESELECT')

scene.render.filepath = os.path.join(OUT_DIR, "preview.png")
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
