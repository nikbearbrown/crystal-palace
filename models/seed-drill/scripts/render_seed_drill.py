#!/usr/bin/env python3
"""Fixed neutral-grey render rig for the seed drill.

Renders front / side / three-quarter on one rig, plus the two photograph
angles (rear-left for Talbot plate 1, front-right for plate 2) used for the
compare sheets. Run after build_seed_drill.py has saved seed-drill.blend.
"""
import bpy
import os
from mathutils import Vector

OUT = os.path.expanduser("~/workspace/cp-models/seed-drill")
bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT, "seed-drill.blend"))
scene = bpy.context.scene

# ---- neutral grey world + ground
world = bpy.data.worlds.new("GreyWorld")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.60, 0.60, 0.60, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -0.002))
gnd = bpy.context.active_object
gnd.name = "Ground"
m = bpy.data.materials.new("GroundGrey")
m.use_nodes = True
m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.52, 0.52, 0.52, 1)
m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
gnd.data.materials.append(m)

# ---- lights: one sun, one fill
bpy.ops.object.light_add(type='SUN', location=(5, -4, 8))
sun = bpy.context.active_object
sun.data.energy = 3.2
sun.rotation_euler = (0.9, 0.2, 0.7)
bpy.ops.object.light_add(type='AREA', location=(-6, 5, 4))
fill = bpy.context.active_object
fill.data.energy = 350
fill.data.shape = 'DISK'
fill.data.size = 6
fill.rotation_euler = (1.1, 0.3, -2.2)

# ---- camera + target
bpy.ops.object.camera_add()
cam = bpy.context.active_object
scene.camera = cam
cam.data.lens = 55
TARGET = Vector((0, 0, 0.60))

def aim(pos):
    cam.location = pos
    d = TARGET - Vector(pos)
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 720
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 32

VIEWS = {
    "front": (0, 6.6, 1.15),
    "side": (6.6, 0, 1.15),
    "three-quarter": (4.5, 4.5, 2.8),
    "rear-three-quarter": (-4.5, -4.5, 2.8),
    "plate2-angle": (5.0, 5.4, 1.95),
}
for name, pos in VIEWS.items():
    aim(pos)
    scene.render.filepath = os.path.join(OUT, "renders", name + ".png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED", name)
