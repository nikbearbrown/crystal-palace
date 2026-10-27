#!/usr/bin/env python3
"""Render rig for iguanodon: ONE fixed neutral-grey rig, consistent
lighting, four views. Run after the build script:
  blender -b iguanodon.blend -noaudio -P scripts/render_views.py
The three-quarter view is the documented view (the reference is a
front 3/4); photomatch.png approximates the photograph's viewpoint
for renders/compare.png.
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

TARGET = Vector((0.1, 0, 1.15))

def aim(cam_ob, pos, target=TARGET):
    cam_ob.location = pos
    d = target - Vector(pos)
    cam_ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

VIEWS = {
    'front.png': ((14.5, 0.0, 2.4), Vector((0.8, 0, 1.2))),
    'side.png': ((0.1, 14.5, 1.9), TARGET),
    'three-quarter.png': ((9.8, 9.8, 4.6), TARGET),
    'photomatch.png': ((10.6, 8.2, 3.1), Vector((0.0, 0, 1.15))),
}
for fname, (pos, tgt) in VIEWS.items():
    aim(cam, pos, tgt)
    scene.render.filepath = os.path.join(OUT, fname)
    bpy.ops.render.render(write_still=True)
    print('RENDERED', fname)
print('RENDERS DONE')
