#!/usr/bin/env python3
"""Render the exhibition carriage on the standard neutral-grey rig:
front / side / three-quarter. Forward = +X."""
import bpy
import math
from mathutils import Vector

OUT = '/home/hatch/workspace/cp-models/exhibition-carriage/renders'

scene = bpy.context.scene
# NOTE: EEVEE hangs on this VM (EGL); Cycles CPU used instead — same rig,
# world, lights and cameras as the standard EEVEE rig (sibling precedent:
# glass-topped-display-counter). Disclosed in NOTES.md.
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.device = 'CPU'
scene.render.resolution_x = 1000
scene.render.resolution_y = 750

world = bpy.data.worlds[0] if bpy.data.worlds else bpy.data.worlds.new('Rig')
scene.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0.32, 0.32, 0.32, 1)
world.node_tree.nodes['Background'].inputs[1].default_value = 1.0

bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -0.001))
gnd = bpy.context.active_object
gnd.name = 'Ground'
m = bpy.data.materials.new('GroundGrey')
m.use_nodes = True
m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.36, 0.36, 0.36, 1)
m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 1.0
gnd.data.materials.append(m)

bpy.ops.object.light_add(type='SUN', location=(4, -3, 7))
sun = bpy.context.active_object
sun.data.energy = 3.2
sun.rotation_euler = (math.radians(52), math.radians(12), math.radians(-32))
bpy.ops.object.light_add(type='AREA', location=(-5, 4, 5))
fill = bpy.context.active_object
fill.data.energy = 350
fill.data.size = 6
fill.rotation_euler = (math.radians(60), 0, math.radians(140))

cam_data = bpy.data.cameras.new('RigCam')
cam = bpy.data.objects.new('RigCam', cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
cam_data.clip_end = 100
cam_data.lens = 42

TARGET = Vector((0.15, 0, 1.05))

def aim(pos):
    cam.location = pos
    d = TARGET - Vector(pos)
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

VIEWS = {
    'front':         (7.4, 0.0, 1.8),
    'side':          (0.15, 7.8, 1.7),
    'three-quarter': (5.4, -5.4, 3.4),
}
for name, pos in VIEWS.items():
    aim(pos)
    scene.render.filepath = f'{OUT}/{name}.png'
    bpy.ops.render.render(write_still=True)
    print('rendered', name)
