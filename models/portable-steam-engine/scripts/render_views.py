#!/usr/bin/env python3
"""Render rig for portable-steam-engine: ONE fixed neutral-grey rig,
consistent lighting (same recipe as the other Muse props).
Run after the build script:
  blender -b portable-steam-engine.blend -noaudio -P scripts/render_views.py
Side view is from -Y (the side opposite the flywheel), matching the
Garrett calotype aspect: firebox left, chimney right. photomatch.png
uses a long lens from the calotype's own angle (about 25 degrees
toward the smokebox end, which is what exposes the flywheel there).
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
scene.render.resolution_x = 1150
scene.render.resolution_y = 850
scene.render.film_transparent = False

world = bpy.data.worlds.new('GreyWorld')
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs[0].default_value = (0.42, 0.42, 0.42, 1.0)
bg.inputs[1].default_value = 0.35

bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, -0.002))
gnd = bpy.context.object
gnd.name = 'Ground'
gm = bpy.data.materials.new('GroundGrey')
gm.use_nodes = True
gm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.46, 0.46, 0.46, 1.0)
gm.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 1.0
gnd.data.materials.append(gm)

sun_data = bpy.data.lights.new('Key', 'SUN')
sun_data.energy = 2.4
sun_data.angle = 0.35
sun = bpy.data.objects.new('Key', sun_data)
sun.rotation_euler = (math.radians(52), math.radians(-18), math.radians(-38))
bpy.context.collection.objects.link(sun)

fill_data = bpy.data.lights.new('Fill', 'AREA')
fill_data.energy = 300
fill_data.shape = 'DISK'
fill_data.size = 7.0
fill = bpy.data.objects.new('Fill', fill_data)
fill.location = (-6.0, -5.0, 5.5)
bpy.context.collection.objects.link(fill)

cam_data = bpy.data.cameras.new('Cam')
cam_data.lens = 40
cam = bpy.data.objects.new('Cam', cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam

def aim(pos, target):
    cam.location = pos
    d = Vector(target) - Vector(pos)
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

VIEWS = [
    ('front.png', (15.5, -1.6, 2.6), (0.4, 0, 1.85), 40),
    ('side.png', (-0.2, -15.5, 2.2), (-0.2, 0, 1.95), 40),
    ('three-quarter.png', (10.8, -10.8, 5.4), (-0.1, 0, 1.65), 40),
    ('photomatch.png', (12.7, -27.2, 2.1), (-0.2, 0, 1.95), 85),
]
for fname, pos, tgt, lens in VIEWS:
    cam_data.lens = lens
    aim(pos, tgt)
    scene.render.filepath = os.path.join(OUT, fname)
    bpy.ops.render.render(write_still=True)
    print('RENDERED', fname)
print('RENDERS DONE')
