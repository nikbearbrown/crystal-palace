#!/usr/bin/env python3
"""Render rig for terrace-statue-survivor: ONE fixed neutral-grey rig,
consistent lighting, five views. Run after the build script:
  blender -b terrace-statue-survivor.blend -noaudio -P scripts/render_views.py
"""
import bpy
import math
import os
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'renders')
os.makedirs(OUT, exist_ok=True)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 96
scene.cycles.use_denoising = True
scene.render.resolution_x = 900
scene.render.resolution_y = 1100
scene.render.film_transparent = False

# neutral grey world
world = bpy.data.worlds.new('GreyWorld')
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs[0].default_value = (0.42, 0.42, 0.42, 1.0)
bg.inputs[1].default_value = 0.35

# ground plane
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -0.001))
gnd = bpy.context.object
gnd.name = 'Ground'
gm = bpy.data.materials.new('GroundGrey')
gm.use_nodes = True
gm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.46, 0.46, 0.46, 1.0)
gm.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 1.0
gnd.data.materials.append(gm)

# lights: key sun + cool fill
sun_data = bpy.data.lights.new('Key', 'SUN')
sun_data.energy = 2.4
sun_data.angle = 0.35
sun = bpy.data.objects.new('Key', sun_data)
sun.rotation_euler = (math.radians(52), math.radians(-18), math.radians(-38))
bpy.context.collection.objects.link(sun)

fill_data = bpy.data.lights.new('Fill', 'AREA')
fill_data.energy = 260
fill_data.shape = 'DISK'
fill_data.size = 6.0
fill = bpy.data.objects.new('Fill', fill_data)
fill.location = (-5.5, -4.0, 5.0)
bpy.context.collection.objects.link(fill)

cam_data = bpy.data.cameras.new('Cam')
cam_data.lens = 42
cam = bpy.data.objects.new('Cam', cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam

TARGET = Vector((0, 0, 2.05))

def aim(cam_ob, pos):
    cam_ob.location = pos
    d = TARGET - Vector(pos)
    cam_ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

VIEWS = {
    'front.png': (0, -8.2, 2.3),
    'side.png': (8.2, 0.4, 2.3),                    # figure's left flank: the cavity
    'three-quarter.png': (-5.6, -5.9, 2.9),         # front-right 3/4
    'rear-three-quarter.png': (5.4, 5.9, 2.9),      # THE documented view (photo)
    'rear.png': (0, 8.2, 2.3),
}
for fname, pos in VIEWS.items():
    aim(cam, pos)
    scene.render.filepath = os.path.join(OUT, fname)
    bpy.ops.render.render(write_still=True)
    print('RENDERED', fname)
print('RENDERS DONE')
