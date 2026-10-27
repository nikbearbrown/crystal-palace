#!/usr/bin/env python3
"""
Render rig for cut-glass-chandelier: ONE fixed neutral-grey studio rig
(house pattern). Opens the model .blend, adds backdrop + lights + cameras,
renders front / side / three-quarter. Does NOT save the .blend.

The chandelier is radially symmetric; "front" is the +X view, chosen so a
lower spear and shell face the camera dead-centre, as in the engraving.
Usage: blender -b -noaudio --python render_rig.py -- [front|side|three-quarter|quick]
"""
import bpy
import math
import os
import sys
from mathutils import Vector

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLEND = os.path.join(BASE, "cut-glass-chandelier.blend")
OUT = os.path.join(BASE, "renders")
os.makedirs(OUT, exist_ok=True)

ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
QUICK = 'quick' in ARGS

bpy.ops.wm.open_mainfile(filepath=BLEND)
scene = bpy.context.scene

scene.render.engine = 'CYCLES'
scene.cycles.samples = 24 if QUICK else 64
scene.cycles.use_denoising = True
scene.cycles.device = 'CPU'
scene.render.resolution_x = 640 if QUICK else 1024
scene.render.resolution_y = 800 if QUICK else 1280
scene.render.film_transparent = False
scene.world = bpy.data.worlds.new("RigWorld")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.42, 0.42, 0.42, 1.0)
bg.inputs[1].default_value = 1.0
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Base Contrast'

grey = bpy.data.materials.new("BackdropGrey")
grey.use_nodes = True
gbsdf = grey.node_tree.nodes["Principled BSDF"]
gbsdf.inputs["Base Color"].default_value = (0.46, 0.46, 0.46, 1.0)
gbsdf.inputs["Roughness"].default_value = 0.95

bpy.ops.mesh.primitive_circle_add(radius=16.0, vertices=48, fill_type='NGON',
                                  location=(0, 0, -0.002))
floor = bpy.context.active_object
floor.name = "RigFloor"
floor.data.materials.append(grey)

def area(name, loc, energy, size, look_at=(0, 0, 2.6)):
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

area("KeyLight", (7.0, -5.5, 9.0), 1600, 5.0)
area("FillLight", (-8.0, 4.5, 5.0), 600, 6.0)
area("RimLight", (0.5, 9.0, 8.0), 1100, 4.0)
# low frontal fill so the flared cone and bottom finial do not go dead
area("LowFill", (0.0, -7.5, 1.0), 550, 4.0, look_at=(0, 0, 1.7))

cam_data = bpy.data.cameras.new("RigCam")
cam_data.lens = 42
cam = bpy.data.objects.new("RigCam", cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam

T = (0, 0, 2.70)

def shot(name, loc, target=T):
    cam.location = loc
    d = Vector(target) - Vector(loc)
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    scene.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
    print("rendered", name)

if not ARGS or 'front' in ARGS or QUICK:
    shot("front.png", (10.9, 0, 2.85))
if not ARGS or 'side' in ARGS:
    shot("side.png", (0, 10.9, 2.85))
if not ARGS or 'three-quarter' in ARGS or QUICK:
    shot("three-quarter.png", (7.3, -7.3, 4.7), (0, 0, 2.50))
print("ALL RENDERS DONE")
