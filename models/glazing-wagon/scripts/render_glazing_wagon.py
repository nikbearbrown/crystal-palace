#!/usr/bin/env python3
"""Render the glazing wagon on the standard neutral-grey rig:
front / side / three-quarter + an engraving-matched 3/4 for the compare."""
import bpy
import math
from mathutils import Vector

OUT = '/home/hatch/workspace/cp-models/glazing-wagon/renders'

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1000
scene.render.resolution_y = 750
scene.eevee.taa_render_samples = 32

# world: flat mid grey
world = bpy.data.worlds.new('Rig') if not bpy.data.worlds else bpy.data.worlds[0]
scene.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0.32, 0.32, 0.32, 1)
world.node_tree.nodes['Background'].inputs[1].default_value = 1.0

# ground plane
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
gnd = bpy.context.active_object
gnd.name = 'Ground'
m = bpy.data.materials.new('GroundGrey')
m.use_nodes = True
m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.36, 0.36, 0.36, 1)
m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 1.0
gnd.data.materials.append(m)

# sun + fill
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

TARGET = Vector((0, 0, 0.95))

def aim(cam_ob, pos):
    cam_ob.location = pos
    d = TARGET - Vector(pos)
    cam_ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

VIEWS = {
    'front':         (6.6, 0.0, 1.7),
    'side':          (0.0, 7.2, 1.6),
    'three-quarter': (4.8, -4.8, 3.3),
    'compare':       (4.8, -4.8, 3.3),
}
for name, pos in VIEWS.items():
    aim(cam, pos)
    scene.render.filepath = f'{OUT}/{name}.png'
    bpy.ops.render.render(write_still=True)
    print('RENDERED', name)
