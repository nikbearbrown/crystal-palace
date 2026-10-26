#!/usr/bin/env python3
"""
Fixed neutral-grey studio rig for the garden fountain basin.
Opens the saved .blend (does not modify geometry), adds lights and
cameras, renders the standard views to renders/.

Views: front (from the gardens, -Y, low), side (from +X, low),
three-quarter (low oblique), elevated-three-quarter (the money view,
approximating the elevated 1886 photograph).
Cycles — EEVEE hangs in this VM.
"""
import bpy
import math
import os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BLEND = os.path.join(ROOT, "garden-fountain-basin.blend")
RENDERS = os.path.join(ROOT, "renders")
os.makedirs(RENDERS, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=BLEND)
scene = bpy.context.scene

# --- render settings -------------------------------------------------------
scene.render.engine = 'CYCLES'
scene.cycles.samples = 96
scene.cycles.use_denoise = True
scene.render.resolution_x = 1280
scene.render.resolution_y = 960
scene.render.film_transparent = False

# --- neutral grey world ----------------------------------------------------
world = bpy.data.worlds.new("StudioWorld") if not bpy.data.worlds else bpy.data.worlds[0]
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.36, 0.36, 0.36, 1.0)
bg.inputs[1].default_value = 0.85

# --- lights: one sun + one soft fill ---------------------------------------
def point_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()

sun_data = bpy.data.lights.new("Sun", 'SUN')
sun_data.energy = 3.2
sun_data.angle = math.radians(6)
sun = bpy.data.objects.new("Sun", sun_data)
sun.location = (55, -38, 80)
scene.collection.objects.link(sun)
point_at(sun, (0, 0, 0))

fill_data = bpy.data.lights.new("Fill", 'AREA')
fill_data.energy = 900
fill_data.shape = 'DISK'
fill_data.size = 60
fill = bpy.data.objects.new("Fill", fill_data)
fill.location = (-45, 30, 55)
scene.collection.objects.link(fill)
point_at(fill, (0, 0, 0))

# --- cameras ---------------------------------------------------------------
VIEWS = {
    "front": ((0, -60, 8), (0, 0, 1.5), 42),
    "side": ((54, 0, 8), (0, 0, 1.5), 42),
    "three-quarter": ((31, -39, 15), (0, 0, 1.0), 42),
    "elevated-three-quarter": ((25, -33, 34), (0, 0, 0), 46),
}

for name, (loc, target, lens) in VIEWS.items():
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = lens
    cam = bpy.data.objects.new(name, cam_data)
    cam.location = loc
    scene.collection.objects.link(cam)
    point_at(cam, target)
    scene.camera = cam
    scene.render.filepath = os.path.join(RENDERS, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("rendered", name)

print("rig done")
