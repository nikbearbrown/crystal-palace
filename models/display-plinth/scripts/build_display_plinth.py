"""
Standard display plinth — Sydenham Crystal Palace courts (film prop, candidate #35).

Modelled from the Rijksmuseum stereographs of the Sydenham courts
(CC0, via Wikimedia Commons; copies in refs/):
  * Greek & Roman sculpture court (RP-F-2012-96-327) — the Aristides plinth,
    measured in the photograph; the tall Minerva bust pedestal beside it.
  * Cain and his Children, sculpture gallery (RP-F-2012-96-336).
  * Hercules in the nave (RP-F-2012-96-329).

Dimensions are photo-derived ratios, not survey measurements — see NOTES.md.
Height 0.90 m assumes the Aristides/Aeschines cast in frame is the full-size
~2.0 m Naples figure (in-photo plinth:statue ratio 0.454, measured).

Blender 4.2, headless:  blender -b --python build_display_plinth.py
Outputs (next to this script's folder): ../display-plinth.blend,
../display-plinth.glb, ../renders/{front,side,three-quarter}.png
"""

import bpy
import math
import os
from mathutils import Vector

# ---------------------------------------------------------------- parameters
# All dimensions in metres. Origin at base centre; plinth stands on z = 0.
TOTAL_H = 0.90

# Loft profile: (z, half_width_x, half_depth_y), bottom to top.
# Base moulding (stepped foot + chamfer) / straight shaft / stepped cap.
PROFILE = [
    (0.000, 0.450, 0.325),   # foot, bottom slab
    (0.080, 0.450, 0.325),   # foot, bottom slab top
    (0.095, 0.428, 0.303),   # small step in
    (0.165, 0.400, 0.275),   # chamfer rise (steeper)
    (0.185, 0.392, 0.267),   # shaft
    (0.825, 0.392, 0.267),   # shaft top
    (0.850, 0.408, 0.283),   # cap step out
    (0.870, 0.408, 0.283),   # cap step top
    (0.900, 0.420, 0.295),   # top slab
]

# Label plate on the FRONT face (-Y), upper shaft. Photos show painted white
# lettering here (catalogue number / title / origin, 3 lines); modelled as a
# shallow unlettered recess — no invented text.
PANEL_W = 0.42
PANEL_H = 0.17
PANEL_Z_TOP = 0.785          # just below the cap
PANEL_RECESS = 0.0035        # front surface sits this far behind the shaft face

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ------------------------------------------------------------------ helpers

def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
        pass  # orphaned data is harmless for a one-shot build


def make_material(name, color, roughness):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def loft_mesh(profile):
    """Rectangular loft through the profile rings, capped top and bottom."""
    verts, faces = [], []
    rings = []
    for z, hx, hy in profile:
        ring = []
        for x, y in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)):
            ring.append(len(verts))
            verts.append((x, y, z))
        rings.append(ring)
    for a, b in zip(rings[:-1], rings[1:]):
        for i in range(4):
            j = (i + 1) % 4
            faces.append((a[i], a[j], b[j], b[i]))
    faces.append(tuple(reversed(rings[0])))   # bottom
    faces.append(tuple(rings[-1]))           # top
    mesh = bpy.data.meshes.new("DisplayPlinthMesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    return mesh


def box_mesh(w, d, h):
    mesh = bpy.data.meshes.new("LabelPanelMesh")
    x, y, z = w / 2, d / 2, h / 2
    verts = [(-x, -y, -z), (x, -y, -z), (x, y, -z), (-x, y, -z),
             (-x, -y, z), (x, -y, z), (x, y, z), (-x, y, z)]
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
             (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    return mesh

# --------------------------------------------------------------------- build

clear_scene()

body_mat = make_material("EbonisedWood", (0.007, 0.006, 0.005), 0.38)
panel_mat = make_material("LabelPlate", (0.011, 0.010, 0.009), 0.58)

body = bpy.data.objects.new("DisplayPlinth", loft_mesh(PROFILE))
bpy.context.collection.objects.link(body)
body.data.materials.append(body_mat)

shaft_hy = 0.267
# Recess: boolean-cut a shallow pocket into the front face, then set the
# unlettered plate at the back of the pocket.
POCKET_W = PANEL_W + 0.004
POCKET_H = PANEL_H + 0.004
POCKET_DEPTH = 0.008
cutter = bpy.data.objects.new(
    "LabelCutter", box_mesh(POCKET_W, 0.03, POCKET_H))
bpy.context.collection.objects.link(cutter)
# Cutter back face at the pocket floor (POCKET_DEPTH behind the front face);
# the rest of the cutter pokes out through the face so the cut is clean.
cutter.location = (
    0.0,
    -shaft_hy + POCKET_DEPTH - 0.015,
    PANEL_Z_TOP - PANEL_H / 2,
)

bpy.context.view_layer.objects.active = body
mod = body.modifiers.new("LabelRecess", "BOOLEAN")
mod.operation = "DIFFERENCE"
mod.solver = "EXACT"
mod.object = cutter
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(cutter, do_unlink=True)

# Plate at the back of the pocket, front face flush with the pocket floor.
plate_depth = 0.014
panel = bpy.data.objects.new("LabelPanel", box_mesh(PANEL_W, plate_depth, PANEL_H))
bpy.context.collection.objects.link(panel)
panel.data.materials.append(panel_mat)
panel.location = (
    0.0,
    -shaft_hy + POCKET_DEPTH + plate_depth / 2 - 0.002,
    PANEL_Z_TOP - PANEL_H / 2,
)

# Join panel into the body as a second material slot.
bpy.ops.object.select_all(action="DESELECT")
body.select_set(True)
panel.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.join()
plinth = bpy.context.view_layer.objects.active
plinth.name = "DisplayPlinth"

# Real-world scale is built in; apply transforms per spec regardless.
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

tri_count = sum(len(p.vertices) - 2 for p in plinth.data.polygons)
print(f"[plinth] triangles: {tri_count}")
bb = [plinth.matrix_world @ Vector(c) for c in plinth.bound_box]
zs = [v.z for v in bb]
print(f"[plinth] height: {max(zs) - min(zs):.3f} m")

# Save the clean model first (rig is added afterwards, not saved).
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, "display-plinth.blend"))

# ---------------------------------------------------------------- render rig
# One fixed neutral-grey rig for all three views.
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.render.resolution_x = 1000
scene.render.resolution_y = 1000
scene.render.film_transparent = False
scene.view_settings.view_transform = "Filmic"
scene.view_settings.look = "Medium Contrast"
scene.view_settings.exposure = 0.0

world = bpy.data.worlds.new("GreyWorld")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.22, 0.22, 0.22, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.4

ground_mat = make_material("BackdropGrey", (0.30, 0.30, 0.30), 0.95)
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
ground = bpy.context.view_layer.objects.active
ground.name = "Backdrop"
ground.data.materials.append(ground_mat)


def add_area(name, loc, size, energy, rot=(0, 0, 0)):
    data = bpy.data.lights.new(name, "AREA")
    data.shape = "RECTANGLE"
    data.size = size[0]
    data.size_y = size[1]
    data.energy = energy
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = rot
    # aim at plinth centre
    direction = Vector((0, 0, 0.45)) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return obj


add_area("Key", (2.4, -3.0, 3.4), (3.0, 2.0), 300)
add_area("Fill", (-3.2, -1.2, 1.6), (2.5, 1.8), 80)
add_area("Rim", (0.4, 3.2, 2.6), (2.5, 1.5), 150)

cam_data = bpy.data.cameras.new("Camera")
cam_data.lens = 50
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam

TARGET = Vector((0, 0, 0.46))
VIEWS = {
    "front": Vector((0.0, -2.7, 0.78)),
    "side": Vector((2.7, 0.0, 0.78)),
    "three-quarter": Vector((-1.95, -1.95, 1.2)),
}
for name, pos in VIEWS.items():
    cam.location = pos
    cam.rotation_euler = (TARGET - pos).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(OUT_DIR, "renders", f"{name}.png")
    bpy.ops.render.render(write_still=True)
    print(f"[plinth] rendered {name}")

# ------------------------------------------------------------------ GLB out
bpy.ops.object.select_all(action="DESELECT")
plinth.select_set(True)
bpy.context.view_layer.objects.active = plinth
bpy.ops.export_scene.gltf(
    filepath=os.path.join(OUT_DIR, "display-plinth.glb"),
    export_format="GLB",
    use_selection=True,
    export_apply=True,
)
print("[plinth] done")
