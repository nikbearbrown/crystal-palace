#!/usr/bin/env python3
"""
Park bench (Sydenham gardens) — procedural build, Blender 4.2.

Evidence basis (see NOTES.md): the benches are visible only as small
silhouettes in one CC0 photograph of the Sydenham fountain gardens
(Rijksmuseum RP-F-F01134-AL). The photo establishes existence, placement
along the walks, a backed bench with two horizontal back rails, and pale
seat surfaces with dark supports. Everything else — the scrolled
cast-iron end profile in particular — is period-typical inference and
is labelled as such in NOTES.md. Do not treat this model as measured.

Dimensions (metres, all inferred/typical for the period):
  overall length 1.90, seat height 0.45, overall height 0.86,
  seat slatted depth 0.46, overall depth 0.63.
"""
import bpy
import bmesh
import math
import os
from mathutils import Vector

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)                      # park-bench/
BLEND_OUT = os.path.join(ROOT, "park-bench.blend")
GLB_OUT = os.path.join(ROOT, "park-bench.glb")
RENDER_DIR = os.path.join(ROOT, "renders")

# ---------------------------------------------------------------- scene reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# ---------------------------------------------------------------- materials
def make_mat(name, color, roughness=0.8, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m

IRON = make_mat("IronPaint_DarkGreen", (0.045, 0.062, 0.052), roughness=0.52, metallic=0.35)
WOOD_A = make_mat("Wood_Slat", (0.200, 0.115, 0.055), roughness=0.80)
WOOD_B = make_mat("Wood_Slat_alt", (0.170, 0.095, 0.045), roughness=0.84)
GROUND_MAT = make_mat("Ground_Grey", (0.32, 0.32, 0.32), roughness=1.0)

# ---------------------------------------------------------------- helpers
def link_obj(obj, mat=None):
    bpy.context.collection.objects.link(obj)
    if mat:
        obj.data.materials.append(mat)
    return obj

def profile_mesh(name, pts_yz, thickness):
    """Flat plate: polygon profile in the YZ plane, solidified along X."""
    verts = [(0.0, y, z) for (y, z) in pts_yz]
    faces = [tuple(range(len(verts)))]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    link_obj(ob, IRON)
    mod = ob.modifiers.new("plate", 'SOLIDIFY')
    mod.thickness = thickness
    mod.offset = 0.0
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.modifier_apply(modifier=mod.name)
    ob.select_set(False)
    return ob

def spiral_tube(name, cx, cy, cz, r_start, r_end, turns, x, phase=0.0, tube=0.0115, flip=False):
    """Archimedean spiral in the YZ plane -> bevelled curve -> mesh (a volute)."""
    pts = []
    steps = 40
    for i in range(steps + 1):
        t = i / steps
        ang = phase + t * turns * 2.0 * math.pi * (1 if not flip else -1)
        r = r_start + (r_end - r_start) * t
        pts.append((x, cy + r * math.cos(ang), cz + r * math.sin(ang)))
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = tube
    cu.bevel_resolution = 2
    spl = cu.splines.new('POLY')
    spl.points.add(len(pts) - 1)
    for p, co in zip(spl.points, pts):
        p.co = (*co, 1.0)
    ob = bpy.data.objects.new(name, cu)
    link_obj(ob, IRON)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.convert(target='MESH')
    ob.select_set(False)
    return ob

def box(name, loc, dims, mat, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        ob.data.materials.append(mat)
    if bevel > 0:
        mod = ob.modifiers.new("soft", 'BEVEL')
        mod.width = bevel
        mod.segments = 2
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.modifier_apply(modifier=mod.name)
    return ob

def bolt(name, x, y, z):
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.0085, depth=0.006,
                                        location=(x, y, z), rotation=(0, math.pi / 2, 0))
    ob = bpy.context.active_object
    ob.name = name
    ob.data.materials.append(IRON)
    return ob

# ---------------------------------------------------------------- geometry
END_X = 0.86          # centre plane of each iron end
PLATE = 0.028         # iron plate thickness
SLAT_L = 1.90         # slat length (overall bench length)
SEAT_Z = 0.45         # top-of-frame seat height (slat centre 0.4375+... see below)

# One end frame: OPEN frame outline traced as a single inverted-U path
# (up the front leg, across the seat rail, down the rear leg, then back
# along the inner edges — the middle under the seat stays open).
BASE_PROFILE = [
    (-0.315, 0.000), (-0.315, 0.048), (-0.270, 0.052), (-0.254, 0.140),
    (-0.246, 0.452), (0.196, 0.452), (0.214, 0.300), (0.226, 0.140),
    (0.238, 0.052), (0.284, 0.052), (0.284, 0.000), (0.238, 0.000),
    (0.222, 0.120), (0.208, 0.300), (0.200, 0.398), (-0.176, 0.398),
    (-0.186, 0.300), (-0.196, 0.120), (-0.206, 0.000),
]
# Back post: raked bar from the seat rail up to just under the top rail
POST_PROFILE = [
    (0.168, 0.430), (0.224, 0.430), (0.304, 0.846), (0.250, 0.860),
]

for side, sx in (("R", END_X), ("L", -END_X)):
    base = profile_mesh(f"EndFrame_{side}", BASE_PROFILE, PLATE)
    base.location.x = sx
    post = profile_mesh(f"BackPost_{side}", POST_PROFILE, PLATE)
    post.location.x = sx
    # side stretcher between the legs, low
    box(f"SideStretcher_{side}", (sx, -0.002, 0.155), (0.020, 0.400, 0.032), IRON)
    # scrolls: volute under the front of the seat rail, finial volute at
    # the top of the back post, S-brace hint under the seat
    spiral_tube(f"SeatFrontScroll_{side}", sx, -0.198, 0.360, 0.046, 0.009, 1.6, sx, phase=2.4)
    spiral_tube(f"TopScroll_{side}", sx, 0.284, 0.812, 0.042, 0.008, 1.6, sx, phase=-0.6, flip=True)
    spiral_tube(f"SeatScroll_{side}", sx, -0.010, 0.332, 0.050, 0.012, 1.25, sx, phase=0.4)

# longitudinal stretcher bar between the two ends, under the seat
box("LongStretcher", (0.0, 0.0, 0.155), (END_X * 2, 0.026, 0.034), IRON)

# seat slats: 4 boards, y from -0.255 (front) to +0.206 (rear)
seat_ys = [-0.2075, -0.0855, 0.0365, 0.1585]
for i, y in enumerate(seat_ys):
    box(f"SeatSlat_{i}", (0.0, y, 0.4495), (SLAT_L, 0.095, 0.025),
        WOOD_A if i % 2 == 0 else WOOD_B, bevel=0.004)

# back slats: 2 broad rails following the post rake (12 deg from vertical)
RAKE = math.radians(12.0)
def back_slat(name, z_c, width, mat):
    # post front face line: y = 0.196 + (z - 0.452) * tan(rake); slat sits proud
    y_c = 0.196 + (z_c - 0.452) * math.tan(RAKE) - 0.020
    ob = box(name, (0.0, y_c, z_c), (SLAT_L, 0.024, width), mat, bevel=0.004)
    ob.rotation_euler = (RAKE, 0, 0)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    return ob

back_slat("BackSlat_lower", 0.655, 0.105, WOOD_A)
back_slat("BackSlat_upper", 0.815, 0.115, WOOD_B)

# bolt heads on the outer faces of the ends
for sx in (END_X, -END_X):
    xo = sx + math.copysign(PLATE / 2 + 0.002, sx)
    for y in seat_ys:
        bolt("Bolt", xo, y, 0.4495)
    for z_c in (0.655, 0.815):
        y_c = 0.196 + (z_c - 0.452) * math.tan(RAKE) - 0.006
        bolt("Bolt", xo, y_c, z_c)

# ---------------------------------------------------------------- ground + rig
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"
ground.data.materials.append(GROUND_MAT)

def add_sun(name, loc, energy, angle=0.6):
    ld = bpy.data.lights.new(name, 'SUN')
    ld.energy = energy
    ld.angle = angle
    ob = bpy.data.objects.new(name, ld)
    ob.location = loc
    ob.rotation_euler = (math.radians(52), math.radians(8), math.radians(-38))
    bpy.context.collection.objects.link(ob)
    return ob

add_sun("KeySun", (2.5, -2.0, 3.5), 2.8)
ld = bpy.data.lights.new("Fill", 'AREA')
ld.energy = 260
ld.shape = 'DISK'
ld.size = 3.0
fill = bpy.data.objects.new("Fill", ld)
fill.location = (-2.6, -1.6, 1.9)
bpy.context.collection.objects.link(fill)

world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.23, 0.23, 0.23, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.75

# cameras on ONE fixed rig
def add_cam(name, loc, target):
    cd = bpy.data.cameras.new(name)
    cd.lens = 42
    ob = bpy.data.objects.new(name, cd)
    ob.location = loc
    bpy.context.collection.objects.link(ob)
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob

CAMS = {
    "front": add_cam("CamFront", (0.0, -3.15, 0.74), (0, 0, 0.44)),
    "side": add_cam("CamSide", (3.15, -0.10, 0.68), (0, 0, 0.43)),
    "three-quarter": add_cam("CamTQ", (2.35, -2.45, 1.32), (0, 0, 0.40)),
}

# point the area light at the bench
fill.rotation_euler = (Vector((0, 0, 0.4)) - fill.location).to_track_quat('-Z', 'Y').to_euler()

# ---------------------------------------------------------------- report dims
bpy.context.view_layer.update()
meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.name != "Ground"]
tris = 0
for o in meshes:
    o.data.calc_loop_triangles()
    tris += len(o.data.loop_triangles)
xs = [o.matrix_world.translation.x for o in meshes]
print(f"MESH OBJECTS: {len(meshes)}  TRIANGLES (excl. ground): {tris}")
import mathutils
mn = Vector((1e9, 1e9, 1e9)); mx = Vector((-1e9, -1e9, -1e9))
for o in meshes:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
print(f"BBOX min {tuple(round(v,3) for v in mn)} max {tuple(round(v,3) for v in mx)}")
print(f"DIMS LxDxH: {mx.x-mn.x:.3f} x {mx.y-mn.y:.3f} x {mx.z-mn.z:.3f}")

# ---------------------------------------------------------------- save/export
bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
scene.camera = CAMS["three-quarter"]
bpy.ops.export_scene.gltf(filepath=GLB_OUT, export_format='GLB')

scene.render.engine = 'CYCLES'
scene.cycles.samples = 80
scene.cycles.use_denoising = True
scene.render.resolution_x = 1280
scene.render.resolution_y = 960
scene.render.film_transparent = False
for view, cam in CAMS.items():
    scene.camera = cam
    scene.render.filepath = os.path.join(RENDER_DIR, f"{view}.png")
    bpy.ops.render.render(write_still=True)
    print("rendered", view)
print("DONE")
