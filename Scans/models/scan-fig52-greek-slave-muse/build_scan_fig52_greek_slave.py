"""
Build script: scan-fig52-greek-slave
Hiram Powers, The Greek Slave (1843) — marble statue as photographed (fig-52).
The figure is a SIMPLIFIED, smooth mannequin-like marble form recording the
statue's pose (contrapposto, head bowed and turned, chained wrists, drapery
over a post at her side). No anatomical detail, no likeness beyond the pose.
Re-runnable: blender -b --python build_scan_fig52_greek_slave.py
Scale: statue 1.65 m (estimated, life-size class) on a low round plinth.
"""
import bpy
import math
import os
from mathutils import Vector

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "scan-fig52-greek-slave"

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
model_coll = bpy.data.collections.new("Model")
bpy.context.scene.collection.children.link(model_coll)
setup_coll = bpy.data.collections.new("RenderSetup")
bpy.context.scene.collection.children.link(setup_coll)

def make_mat(name, color, roughness=0.5, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m

MARBLE = make_mat("Marble", (0.93, 0.92, 0.90), roughness=0.38)
MARBLE_BASE = make_mat("MarbleBase", (0.88, 0.87, 0.85), roughness=0.45)
IRON = make_mat("ChainIron", (0.25, 0.24, 0.24), roughness=0.45, metallic=0.85)

def link(ob, coll=model_coll):
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    coll.objects.link(ob)
    return ob

def ball(name, loc, scale, mat=None, coll=None, seg=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2 + 4,
                                         location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    for p in ob.data.polygons:
        p.use_smooth = True
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll) if coll else ob

def cyl(name, loc, r, h, mat=None, vertices=24, rot=(0, 0, 0), coll=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=h,
                                        location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    if mat:
        ob.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    return link(ob, coll) if coll else ob

def capsule(name, p1, p2, r, mat=None, coll=None):
    p1, p2 = Vector(p1), Vector(p2)
    mid = (p1 + p2) / 2
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=r,
                                        depth=(p2 - p1).length, location=mid)
    ob = bpy.context.active_object
    ob.name = name
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = (p2 - p1).to_track_quat('Z', 'Y')
    if mat:
        ob.data.materials.append(mat)
    # Return the cylinder AND its end spheres as separate clean manifold
    # objects for the boolean union. (Joining them into one self-intersecting
    # mesh made the EXACT boolean drop geometry; leaving them out entirely
    # left stray unmaterialised balls in the scene.)
    ea = ball(name + "_A", tuple(p1), (r, r, r), mat)
    eb = ball(name + "_B", tuple(p2), (r, r, r), mat)
    bpy.ops.object.select_all(action='DESELECT')
    return [ob, ea, eb]

def union_mesh(name, parts, mat, voxel=0.015):
    """Boolean-union a list of objects into one smooth mesh, then voxel remesh."""
    base = parts[0]
    base.name = name
    bpy.context.view_layer.objects.active = base
    for other in parts[1:]:
        mod = base.modifiers.new("u", 'BOOLEAN')
        mod.operation = 'UNION'
        mod.solver = 'EXACT'
        mod.object = other
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.data.objects.remove(other, do_unlink=True)
    rem = base.modifiers.new("remesh", 'REMESH')
    rem.mode = 'VOXEL'
    rem.voxel_size = voxel
    rem.use_smooth_shade = True
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.modifier_apply(modifier=rem.name)
    if mat:
        base.data.materials.clear()
        base.data.materials.append(mat)
    return base

# ================================================================= plinth
cyl("Plinth_Socle", (0, 0, 0.022), 0.335, 0.045, MARBLE_BASE, vertices=48,
    coll=model_coll)
cyl("Plinth_Top", (0, 0, 0.072), 0.295, 0.055, MARBLE, vertices=48, coll=model_coll)
# decorative rim bead on plinth edge (seen in the photograph)
bpy.ops.mesh.primitive_torus_add(major_radius=0.295, minor_radius=0.008,
                                 major_segments=48, minor_segments=8,
                                 location=(0, 0, 0.098))
rim = bpy.context.active_object
rim.name = "Plinth_RimBead"
rim.data.materials.append(MARBLE)
link(rim, model_coll)
bpy.ops.object.select_all(action='DESELECT')

BASE = 0.10  # figure feet stand on plinth top

# ================================================================= figure
# Stylised figure built in world space (feet at z = BASE), contrapposto:
# weight on the statue's LEFT leg (viewer's right), right leg relaxed forward.
parts = []
def P(ob):
    if isinstance(ob, list):
        parts.extend(ob)
    else:
        parts.append(ob)
    return ob

P(ball("Pelvis", (-0.005, 0, BASE + 0.875), (0.150, 0.102, 0.112)))
P(ball("Waist", (0.0, 0.002, BASE + 0.985), (0.108, 0.080, 0.095)))
P(ball("Chest", (0.006, 0.004, BASE + 1.115), (0.128, 0.090, 0.108)))
P(ball("ShoulderBar", (0.008, 0.004, BASE + 1.205), (0.148, 0.082, 0.062)))
P(cyl("Neck", (0.010, 0.006, BASE + 1.265), 0.034, 0.10))
# NOTE on sides: with the preview camera at +Y, screen-right is world -X,
# so the statue's anatomical LEFT is world -X and her RIGHT is world +X.
# left leg (weight-bearing, near straight)
P(capsule("LegL_Thigh", (-0.072, 0.002, BASE + 0.845), (-0.066, 0.006, BASE + 0.46), 0.066))
P(capsule("LegL_Calf", (-0.066, 0.006, BASE + 0.46), (-0.060, 0.010, BASE + 0.075), 0.040))
P(ball("FootL", (-0.058, 0.052, BASE + 0.022), (0.038, 0.092, 0.026)))
# right leg (relaxed, knee soft, foot a little forward)
P(capsule("LegR_Thigh", (0.074, 0.004, BASE + 0.84), (0.086, 0.030, BASE + 0.465), 0.064))
P(capsule("LegR_Calf", (0.086, 0.030, BASE + 0.465), (0.078, 0.052, BASE + 0.075), 0.039))
P(ball("FootR", (0.076, 0.092, BASE + 0.022), (0.037, 0.090, 0.025)))
# right arm hangs at her side, hand reaching the drapery post
P(capsule("ArmR_Upper", (0.138, 0.004, BASE + 1.20), (0.155, 0.010, BASE + 0.975), 0.036))
P(capsule("ArmR_Fore", (0.155, 0.010, BASE + 0.975), (0.142, 0.034, BASE + 0.755), 0.029))
P(ball("HandR", (0.146, 0.045, BASE + 0.715), (0.026, 0.052, 0.020)))
# left arm crosses the front of the pelvis, wrist meeting the chain
P(capsule("ArmL_Upper", (-0.132, 0.006, BASE + 1.20), (-0.122, 0.028, BASE + 0.985), 0.036))
P(capsule("ArmL_Fore", (-0.122, 0.028, BASE + 0.985), (-0.028, 0.082, BASE + 0.745), 0.029))
P(ball("HandL", (-0.012, 0.095, BASE + 0.715), (0.026, 0.052, 0.020)))

figure = union_mesh("Figure_GreekSlave", parts, MARBLE, voxel=0.0145)
link(figure, model_coll)

# Head: separate object so the bowed/turned pose reads; merged in local space.
hparts = []
hparts.append(ball("Skull", (0, 0, 0.085), (0.070, 0.076, 0.092)))
hparts.append(ball("Face", (-0.004, 0.018, 0.062), (0.058, 0.062, 0.070)))
hparts.append(ball("HairCap", (0.006, -0.020, 0.098), (0.072, 0.072, 0.088)))
hparts.append(ball("HairBun", (0.030, -0.082, 0.088), (0.034, 0.030, 0.034)))
hparts.append(ball("NeckStub", (0, 0, 0.0), (0.034, 0.034, 0.045)))
head = union_mesh("Head", hparts, MARBLE, voxel=0.010)
head.location = (0.012, 0.008, BASE + 1.285)
head.rotation_euler = (0.38, -0.10, -0.42)  # bowed down, turned to her left
link(head, model_coll)

# ================================================================= chains + cuffs
def chain(name, p0, p1, sag, links_n=13):
    p0, p1 = Vector(p0), Vector(p1)
    src = None
    for i in range(links_n):
        t = i / (links_n - 1)
        pos = (1 - t) * p0 + t * p1
        pos.z -= sag * 4 * t * (1 - t)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.0145, minor_radius=0.0044,
                                         major_segments=10, minor_segments=5,
                                         location=tuple(pos))
        ob = bpy.context.active_object
        if src is None:
            src = ob
            ob.name = name
            ob.data.materials.append(IRON)
            link(ob, model_coll)
        else:
            ob.data = src.data
            ob.name = f"{name}_{i}"
            link(ob, model_coll)
        ob.rotation_euler = (math.pi / 2.4, (i % 2) * math.pi / 2, 0.5)
    bpy.ops.object.select_all(action='DESELECT')

for nm, loc in (("CuffR", (0.148, 0.036, BASE + 0.745)),
                ("CuffL", (-0.030, 0.084, BASE + 0.742))):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.031, minor_radius=0.006,
                                     major_segments=20, minor_segments=6,
                                     location=loc, rotation=(0.3, 0.2, 0))
    cu = bpy.context.active_object
    cu.name = nm
    cu.data.materials.append(IRON)
    link(cu, model_coll)
chain("WristChain", (0.148, 0.045, BASE + 0.735), (-0.026, 0.092, BASE + 0.730),
      sag=0.055, links_n=13)
bpy.ops.object.select_all(action='DESELECT')

# ================================================================= drapery post (her right side)
cyl("DrapePost", (0.21, -0.015, BASE + 0.375), 0.048, 0.75, MARBLE,
    vertices=20, coll=model_coll)
cyl("DrapePost_Cap", (0.21, -0.015, BASE + 0.765), 0.062, 0.035, MARBLE,
    vertices=20, coll=model_coll)
# cloth thrown over the post, hanging to the plinth (simplified folds)
prof = [(0.0, 0.79), (0.058, 0.785), (0.068, 0.72), (0.076, 0.55),
        (0.084, 0.35), (0.092, 0.15), (0.098, 0.03)]
verts, faces = [], []
n = len(prof)
seg = 30
for (r, z) in prof:
    for j in range(seg):
        a = 2 * math.pi * j / seg
        wob = 1 + 0.05 * math.sin(5 * a + z * 4)
        verts.append((r * wob * math.cos(a), r * wob * math.sin(a), z))
for i in range(n - 1):
    for j in range(seg):
        j2 = (j + 1) % seg
        faces.append((i * seg + j, (i + 1) * seg + j, (i + 1) * seg + j2, i * seg + j2))
me = bpy.data.meshes.new("Drapery")
me.from_pydata(verts, [], faces)
me.update()
for p in me.polygons:
    p.use_smooth = True
cloth = bpy.data.objects.new("Drapery_Cloth", me)
cloth.data.materials.append(MARBLE)
cloth.location = (0.20, -0.01, BASE)
model_coll.objects.link(cloth)
# fringe tassels along the cloth's top edge, by her hand
for k in range(7):
    a = -0.5 + k * 0.17
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.007, radius2=0.002,
                                    depth=0.045,
                                    location=(0.20 + 0.068 * math.cos(a + 1.2),
                                              -0.01 + 0.068 * math.sin(a + 1.2),
                                              BASE + 0.745))
    ts = bpy.context.active_object
    ts.name = f"Drapery_Fringe_{k}"
    ts.data.materials.append(MARBLE)
    link(ts, model_coll)
bpy.ops.object.select_all(action='DESELECT')

# ================================================================= render setup
def look_at(ob, target):
    ob.rotation_euler = (Vector(target) - ob.location).to_track_quat('-Z', 'Y').to_euler()

bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -0.001))
ground = bpy.context.active_object
ground.name = "GroundPlane"
gm = make_mat("BackdropGrey", (0.44, 0.44, 0.44), roughness=1.0)
ground.data.materials.append(gm)
link(ground, setup_coll)

bpy.ops.object.camera_add(location=(0.55, 2.85, 1.30))
cam = bpy.context.active_object
cam.name = "PreviewCamera"
cam.data.lens = 50
look_at(cam, (0, 0, 0.80))
link(cam, setup_coll)
bpy.context.scene.camera = cam

def add_light(name, loc, energy, size):
    bpy.ops.object.light_add(type='AREA', location=loc)
    li = bpy.context.active_object
    li.name = name
    li.data.energy = energy
    li.data.shape = 'DISK'
    li.data.size = size
    look_at(li, (0, 0, 0.9))
    return link(li, setup_coll)

add_light("KeyLight", (1.4, 1.8, 2.4), 110, 1.0)
add_light("FillLight", (-1.6, 1.2, 1.2), 35, 1.4)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.03
scene.render.resolution_percentage = 85
scene.cycles.use_denoising = True
scene.render.resolution_x = 720
scene.render.resolution_y = 1080
scene.world = bpy.data.worlds.new("GreyWorld")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.44, 0.44, 0.44, 1)
scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.55

def tri_count(coll):
    total = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for ob in coll.all_objects:
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
for ob in model_coll.all_objects:
    ob.select_set(True)
bpy.context.view_layer.objects.active = model_coll.all_objects[0]
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT_DIR, SLUG + ".glb"),
                          export_format='GLB', use_selection=True, export_apply=True)
bpy.ops.object.select_all(action='DESELECT')
scene.render.filepath = os.path.join(OUT_DIR, "preview.png")
bpy.ops.render.render(write_still=True)
print("DONE", SLUG)
