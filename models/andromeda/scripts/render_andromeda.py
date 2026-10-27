#!/usr/bin/env python3
"""
Render rig for Andromeda: ONE fixed neutral-grey studio setup
(same for every build round) — front / side / three-quarter.

Run: blender -b andromeda.blend --python scripts/render_andromeda.py
"""
import bpy
import math
import os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'renders')
os.makedirs(OUT, exist_ok=True)

scene = bpy.context.scene

# Remove any previous rig objects.
for name in ('RigCam', 'RigSun', 'RigFill', 'RigBackdrop'):
    ob = bpy.data.objects.get(name)
    if ob:
        bpy.data.objects.remove(ob, do_unlink=True)

# Neutral grey world.
world = bpy.data.worlds.new('RigWorld') if not bpy.data.worlds else bpy.data.worlds[0]
scene.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0.30, 0.30, 0.30, 1.0)
world.node_tree.nodes['Background'].inputs[1].default_value = 0.45

# Backdrop: large soft-grey ground disc to catch the base shadow.
bpy.ops.mesh.primitive_circle_add(vertices=48, radius=9.0, fill_type='NGON',
                                  location=(0, 0, -0.001))
disc = bpy.context.active_object
disc.name = 'RigBackdrop'
mat = bpy.data.materials.new('BackdropGrey')
mat.use_nodes = True
mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.32, 0.32, 0.32, 1.0)
mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 1.0
disc.data.materials.append(mat)

# Key sun + camera-side fill.
bpy.ops.object.light_add(type='SUN', location=(2.5, -3.0, 5.0))
sun = bpy.context.active_object
sun.name = 'RigSun'
sun.data.energy = 2.3
sun.rotation_euler = (math.radians(52), math.radians(8), math.radians(38))
bpy.ops.object.light_add(type='AREA', location=(-2.6, -2.4, 2.2))
fill = bpy.context.active_object
fill.name = 'RigFill'
fill.data.energy = 120
fill.data.shape = 'DISK'
fill.data.size = 3.0
fill.rotation_euler = (math.radians(66), 0, math.radians(-42))

# Camera.
cam_data = bpy.data.cameras.new('RigCam')
cam_data.lens = 52
cam = bpy.data.objects.new('RigCam', cam_data)
scene.collection.objects.link(cam)
scene.camera = cam

TARGET = Vector((0.0, 0.0, 1.12))
DIST = 3.55

VIEWS = {
    'front.png':         Vector((0.0, -DIST, 1.30)),
    'side.png':          Vector((DIST, 0.0, 1.30)),
    'three-quarter.png': Vector((2.20, -2.60, 1.66)),
    'rear-quarter.png':  Vector((-2.20, 2.60, 1.66)),
}

scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 16
scene.cycles.use_denoising = False
scene.render.resolution_x = 1000
scene.render.resolution_y = 1250
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False

import sys
only = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
for fname, pos in VIEWS.items():
    if only and fname not in only:
        continue
    cam.location = pos
    direction = TARGET - pos
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    scene.render.filepath = os.path.join(OUT, fname)
    bpy.ops.render.render(write_still=True)
    print('rendered', fname)
print('RENDERS DONE')
