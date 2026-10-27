#!/usr/bin/env python3
"""Render the vacuum sugar apparatus on the fixed neutral-grey studio rig:
front (the documented Talbot view), side, three-quarter, plus a portrait
'compare' frame echoing the photograph. Opens the .blend, adds rig only."""
import bpy, math, os, sys
from mathutils import Vector

BASE = os.path.expanduser("~/workspace/cp-models/vacuum-sugar-apparatus")
bpy.ops.wm.open_mainfile(filepath=os.path.join(BASE, "vacuum-sugar-apparatus.blend"))
sc = bpy.context.scene

# ---- studio: grey floor + background, three area lights
def area(name, loc, energy, size):
    d = bpy.data.lights.new(name, 'AREA')
    d.energy, d.shape, d.size = energy, 'DISK', size
    o = bpy.data.objects.new(name, d)
    o.location = loc
    sc.collection.objects.link(o)
    return o

def point_at(ob, target):
    ob.rotation_euler = (Vector(target) - ob.location).to_track_quat('-Z', 'Y').to_euler()

key = area("Key", (4.5, -4.5, 7.5), 1600, 4.0)
fill = area("Fill", (-5.5, -1.5, 3.5), 550, 3.0)
rim = area("Rim", (0.5, 5.5, 6.5), 1000, 3.0)

fm = bpy.data.materials.new("StudioFloor")
fm.use_nodes = True
fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.40, 0.40, 0.40, 1)
fm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
floor = bpy.context.object
floor.name = "StudioFloor"
floor.data.materials.append(fm)

w = bpy.data.worlds.new("StudioWorld") if not bpy.data.worlds else bpy.data.worlds[0]
sc.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.46, 0.46, 0.46, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0

sc.render.engine = 'CYCLES'
sc.cycles.samples = 128
sc.cycles.use_denoising = True
sc.render.resolution_percentage = 100
sc.view_settings.view_transform = 'Filmic'
sc.view_settings.look = 'Medium Contrast'

cam_data = bpy.data.cameras.new("Rig")
cam = bpy.data.objects.new("Rig", cam_data)
sc.collection.objects.link(cam)
sc.camera = cam

VIEWS = [
    ("front",         (0.20, -8.4, 2.20), (0.20, 0, 1.95), 50, (1100, 1100)),
    ("side",          (8.4, -0.4, 2.10),  (0.1, 0, 1.95),  50, (1100, 1100)),
    ("three-quarter", (5.4, -5.8, 3.6),   (0.10, 0, 1.85), 46, (1100, 1100)),
    ("compare",       (0.25, -7.6, 2.45), (0.25, 0, 2.00), 55, (950, 1180)),
]
only = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
for name, loc, tgt, lens, res in VIEWS:
    if only and name not in only:
        continue
    cam.location = loc
    cam_data.lens = lens
    point_at(cam, tgt)
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.filepath = os.path.join(BASE, "renders", name + ".png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED", name)
print("ALL RENDERS DONE")
