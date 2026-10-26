#!/usr/bin/env python3
"""
Build script — hp-floor-boards
A short section of the Hyde Park 1851 open-boarded ground floor
(boards with the 1/2-inch cleaning gaps), on joists, on sleepers.

Evidence: Official Descriptive and Illustrated Catalogue of the Great
Exhibition (1851), Introduction p.62, quoting Paxton's own account:
"The boards for the floor are 1-1/2 inch thick, laid half an inch
apart, upon joists 7 inches by 2-1/2 inches, which rest upon large
timbers or sleepers, 13 inches by 3-1/4 inches, at intervals of
8 feet apart."

Re-runnable:  blender -b --python build_hp_floor_boards.py
Produces hp-floor-boards.blend, hp-floor-boards.glb and renders/*.png
in this script's directory. Metres throughout. Origin at base centre.
"""
import bpy
import os
import math
import random
from mathutils import Vector

IN = 0.0254          # one inch in metres
FT = 12 * IN

# ---------------------------------------------------------------- evidence
BOARD_T   = 1.5 * IN     # printed, Catalogue p.62
GAP       = 0.5 * IN     # printed, Catalogue p.62 (and Berlyn p.37)
JOIST_D   = 7.0 * IN     # printed, depth (vertical), p.62
JOIST_W   = 2.5 * IN     # printed, width, p.62
SLEEP_D   = 13.0 * IN    # printed, read as depth (vertical) — see NOTES
SLEEP_W   = 3.25 * IN    # printed, width, p.62
SLEEP_PITCH = 8 * FT     # printed, "at intervals of 8 feet apart"

# ---------------------------------------------------------------- inferred
BOARD_W   = 9.0 * IN     # INFERRED — no width is printed; see NOTES.md
JOIST_PITCH = 2 * FT     # INFERRED — no joist spacing is printed; see NOTES.md

# ------------------------------------------------------------- the section
SEC_LEN = 16 * FT        # along X: two full 8 ft sleeper intervals
SEC_WID = 12 * FT        # along Y: joist span across both sleepers + bearing

BASE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- helpers
def box(name, centre, size, material, collection):
    """Axis-aligned box with world-space verts; object transform = identity."""
    cx, cy, cz = centre
    sx, sy, sz = size[0] / 2, size[1] / 2, size[2] / 2
    verts = [(cx + dx, cy + dy, cz + dz)
             for dx in (-sx, sx) for dy in (-sy, sy) for dz in (-sz, sz)]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1),
             (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    if material:
        mesh.materials.append(material)
    return obj

def timber(name, rgb, rough=0.85):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return m

def look_at(obj, target):
    """Point an object's -Z (camera) / +Y (light) at target, safely."""
    obj.rotation_mode = 'QUATERNION'          # set BEFORE assigning quaternion
    direction = Vector(target) - obj.location
    obj.rotation_quaternion = direction.to_track_quat('-Z', 'Y')

# ---------------------------------------------------------------- scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

model_col = bpy.data.collections.new("Model")
scene.collection.children.link(model_col)
setup_col = bpy.data.collections.new("RenderSetup")
scene.collection.children.link(setup_col)

rng = random.Random(1851)

# ------------------------------------------------------------- materials
sleeper_mat = timber("TimberSleeper", (0.30, 0.21, 0.12))
joist_mat   = timber("TimberJoist",   (0.36, 0.25, 0.14))
board_mats  = []
for i in range(5):  # subtle per-board variation, cycled deterministically
    j = rng.uniform(-0.035, 0.035)
    board_mats.append(timber(f"TimberBoard{i+1}",
                             (0.46 + j, 0.335 + j * 0.8, 0.20 + j * 0.5)))

# ------------------------------------------------------------- structure
z0 = 0.0                       # underside of sleepers = prop base (origin)
z_sleeper_top = z0 + SLEEP_D
z_joist_top   = z_sleeper_top + JOIST_D
z_board_top   = z_joist_top + BOARD_T

# Sleepers: run along X, spaced SLEEP_PITCH apart across Y.
for i, y in enumerate((-SLEEP_PITCH / 2, SLEEP_PITCH / 2)):
    box(f"Sleeper_{i+1:02d}", (0, y, z0 + SLEEP_D / 2),
        (SEC_LEN, SLEEP_W, SLEEP_D), sleeper_mat, model_col)

# Joists: run along Y, rest on the sleepers, inferred 2 ft centres along X.
# End joists sit one full pitch in from the cut ends, so the section reads
# as cut from a continuous floor rather than terminated.
joist_xs = [(-SEC_LEN / 2 + JOIST_PITCH) + i * JOIST_PITCH
            for i in range(int(SEC_LEN / JOIST_PITCH) - 1)]
# -> 7 joists at X = -6, -4, -2, 0, +2, +4, +6 ft relative to centre
for i, x in enumerate(joist_xs):
    box(f"Joist_{i+1:02d}", (x, 0, z_sleeper_top + JOIST_D / 2),
        (JOIST_W, SEC_WID, JOIST_D), joist_mat, model_col)

# Boards: run along X on top of the joists, printed 1/2 in gaps between.
pitch = BOARD_W + GAP
n_boards = int((SEC_WID + GAP) / pitch)            # 15 across 12 ft
span = n_boards * BOARD_W + (n_boards - 1) * GAP
y_start = -span / 2 + BOARD_W / 2
for i in range(n_boards):
    y = y_start + i * pitch
    box(f"Board_{i+1:02d}", (0, y, z_joist_top + BOARD_T / 2),
        (SEC_LEN, BOARD_W, BOARD_T), board_mats[i % len(board_mats)],
        model_col)

# ---------------------------------------------------------- render setup
# Backdrop: one large neutral-grey plane under the prop (z just below base).
bg_mat = timber("BackdropGrey", (0.52, 0.52, 0.52), rough=1.0)
box("Backdrop", (0, 0, -0.002), (40, 40, 0.002), bg_mat, setup_col)

world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)
bg.inputs[1].default_value = 0.85

sun_data = bpy.data.lights.new("Sun", 'SUN')
sun_data.energy = 3.0
sun_data.angle = 0.35
sun = bpy.data.objects.new("Sun", sun_data)
setup_col.objects.link(sun)
sun.location = (4, -3, 7)
look_at(sun, (0, 0, 0))

fill_data = bpy.data.lights.new("Fill", 'AREA')
fill_data.energy = 350
fill_data.shape = 'DISK'
fill_data.size = 6
fill = bpy.data.objects.new("Fill", fill_data)
setup_col.objects.link(fill)
fill.location = (-5, 4, 5)
look_at(fill, (0, 0, 0.1))

def make_camera(name, loc, target, ortho=None, lens=55):
    data = bpy.data.cameras.new(name)
    if ortho:
        data.type = 'ORTHO'
        data.ortho_scale = ortho
    else:
        data.type = 'PERSP'
        data.lens = lens
    cam = bpy.data.objects.new(name, data)
    setup_col.objects.link(cam)
    cam.location = loc
    look_at(cam, target)
    return cam

mid_z = z_board_top / 2
cam_front = make_camera("CamFront", (-9, 0, mid_z), (0, 0, mid_z),
                        ortho=4.3)                       # section across Y
cam_side  = make_camera("CamSide", (0, -10, mid_z), (0, 0, mid_z),
                        ortho=5.5)                       # elevation along X
cam_tq    = make_camera("CamThreeQuarter", (4.6, -5.4, 3.3),
                        (0, 0, 0.15), lens=55)

# ------------------------------------------------------------- rendering
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.cycles.use_denoising = True
try:
    scene.cycles.device = 'CPU'
except Exception:
    pass
scene.render.resolution_x = 960
scene.render.resolution_y = 720
scene.render.film_transparent = False

os.makedirs(os.path.join(BASE, "renders"), exist_ok=True)
_skip = set(filter(None, os.environ.get("HPFB_SKIP", "").split(",")))
for cam, fname in ((cam_front, "front.png"),
                   (cam_side, "side.png"),
                   (cam_tq, "three-quarter.png")):
    if fname in _skip:
        continue
    scene.camera = cam
    scene.render.filepath = os.path.join(BASE, "renders", fname)
    bpy.ops.render.render(write_still=True)

# ------------------------------------------------------ save + GLB export
blend_path = os.path.join(BASE, "hp-floor-boards.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.ops.object.select_all(action='DESELECT')
tris = 0
for obj in model_col.objects:
    obj.select_set(True)
    if obj.type == 'MESH':
        obj.data.calc_loop_triangles()
        tris += len(obj.data.loop_triangles)
bpy.context.view_layer.objects.active = model_col.objects[0]
glb_path = os.path.join(BASE, "hp-floor-boards.glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB',
                          use_selection=True, export_yup=True)

print(f"HP-FLOOR-BOARDS objects={len(model_col.objects)} triangles={tris}")
print(f"HP-FLOOR-BOARDS section={SEC_LEN:.4f} x {SEC_WID:.4f} m, "
      f"floor top z={z_board_top:.4f} m "
      f"({z_board_top / IN:.2f} in above base)")
print(f"HP-FLOOR-BOARDS boards={n_boards} joists={len(joist_xs)} sleepers=2")
