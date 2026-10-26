#!/usr/bin/env python3
"""
Render rig for fountain-basin-railing: ONE fixed neutral-grey studio rig.
Opens the model .blend, adds backdrop + lights + cameras, renders
front / side (along the arc) / three-quarter. Does NOT save the .blend.
"""
import bpy
import math
import os
from mathutils import Vector

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLEND = os.path.join(BASE, "fountain-basin-railing.blend")
OUT = os.path.join(BASE, "renders")
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=BLEND)
scene = bpy.context.scene

# ---- render settings -------------------------------------------------------
import sys
ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
QUICK = 'quick' in ARGS
scene.render.engine = 'CYCLES'
scene.cycles.samples = 16 if QUICK else 32
scene.cycles.use_denoising = not QUICK
scene.cycles.device = 'CPU'
scene.render.resolution_x = 1024 if QUICK else 1280
scene.render.resolution_y = 768 if QUICK else 960
scene.render.film_transparent = False
scene.world = bpy.data.worlds.new("RigWorld")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.42, 0.42, 0.42, 1.0)
bg.inputs[1].default_value = 1.0
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Base Contrast'

# ---- backdrop: floor disc + big soft cyclorama plane -----------------------
grey = bpy.data.materials.new("BackdropGrey")
grey.use_nodes = True
gbsdf = grey.node_tree.nodes["Principled BSDF"]
gbsdf.inputs["Base Color"].default_value = (0.46, 0.46, 0.46, 1.0)
gbsdf.inputs["Roughness"].default_value = 0.95

bpy.ops.mesh.primitive_circle_add(radius=9.0, vertices=48, fill_type='NGON',
                                  location=(0, 0, -0.001))
floor = bpy.context.active_object
floor.name = "RigFloor"
floor.data.materials.append(grey)

bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 11.5, 8))
back = bpy.context.active_object
back.name = "RigBack"
back.rotation_euler = (math.radians(90), 0, 0)
back.data.materials.append(grey)

# ---- lights (fixed for all views) ------------------------------------------
def area(name, loc, energy, size, look_at=(0, 1.6, 0.55)):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.energy = energy
    ld.shape = 'DISK'
    ld.size = size
    ob = bpy.data.objects.new(name, ld)
    bpy.context.collection.objects.link(ob)
    ob.location = loc
    d = Vector(look_at) - Vector(loc)
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob

area("KeyLight", (5.5, -4.5, 7.5), 900, 4.0)
area("FillLight", (-6.5, 3.5, 4.0), 350, 5.0)
area("RimLight", (0.5, 7.5, 6.5), 600, 3.0)

# ---- camera ----------------------------------------------------------------
cam_data = bpy.data.cameras.new("RigCam")
cam_data.lens = 42
cam = bpy.data.objects.new("RigCam", cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam

BIS = math.radians(45)  # quadrant bisector

def aim(cam, loc, target):
    cam.location = loc
    d = Vector(target) - Vector(loc)
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def shot(name, loc, target):
    aim(cam, loc, target)
    scene.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
    print("rendered", name)

# target: middle of the quadrant at mid height
T = (2.0 * math.cos(BIS), 2.0 * math.sin(BIS), 0.55)

# FRONT — outside the arc on the bisector, looking in
d = 6.4
if not ARGS or 'front' in ARGS or QUICK:
    shot("front.png",
         (T[0] + d * math.cos(BIS), T[1] + d * math.sin(BIS), 1.35), T)
# SIDE — along the arc: from just outside the 90-degree end, looking back
# along the curve toward the 0-degree end
end = (3.5 * math.cos(math.radians(90)), 3.5 * math.sin(math.radians(90)), 0)
if not ARGS or 'side' in ARGS:
    shot("side.png",
         (end[0] - 1.1, end[1] + 2.6, 1.15),
         (3.5 * math.cos(math.radians(18)), 3.5 * math.sin(math.radians(18)), 0.55))
# THREE-QUARTER — elevated oblique from outside the 0-degree end
if not ARGS or 'three-quarter' in ARGS or QUICK:
    shot("three-quarter.png",
         (T[0] + 5.2 * math.cos(math.radians(8)), T[1] + 5.2 * math.sin(math.radians(8)), 3.4),
         (1.55, 1.55, 0.45))
print("ALL RENDERS DONE")
