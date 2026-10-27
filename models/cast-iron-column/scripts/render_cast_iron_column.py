#!/usr/bin/env python3
"""Render the complete cast-iron column on the fixed neutral-grey rig.
Front / side / three-quarter full-height views + a close-up of the
tier-1 connecting piece C (the Fig. 12 joint). Same rig each round."""
import bpy
import math
import os
from mathutils import Vector

OUT = os.path.expanduser("~/workspace/cp-models/cast-iron-column")
RENDERS = os.path.join(OUT, "renders")
os.makedirs(RENDERS, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT, "cast-iron-column.blend"))

# clean any previous rig
for ob in list(bpy.data.objects):
    if ob.name.startswith("RIG_"):
        bpy.data.objects.remove(ob, do_unlink=True)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.device = 'CPU'
scene.cycles.use_denoising = True
scene.render.film_transparent = False
world = bpy.data.worlds.new("RigWorld") if not bpy.data.worlds else bpy.data.worlds[0]
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.52, 0.52, 0.52, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

def add(name, obj):
    obj.name = name
    if obj.name not in scene.collection.objects:
        scene.collection.objects.link(obj)
    return obj

# ground plane at the bottom of the foundation foot
bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, -0.612))
ground = add("RIG_Ground", bpy.context.active_object)
gm = bpy.data.materials.new("RigGrey")
gm.use_nodes = True
gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.56, 0.56, 0.56, 1)
gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
ground.data.materials.append(gm)

bpy.ops.object.light_add(type='SUN', location=(12, -14, 30))
sun = add("RIG_Sun", bpy.context.active_object)
sun.data.energy = 3.8
sun.rotation_euler = (math.radians(52), math.radians(12), math.radians(38))
bpy.ops.object.light_add(type='AREA', location=(-16, 10, 22))
fill = add("RIG_Fill", bpy.context.active_object)
fill.data.energy = 900
fill.data.shape = 'DISK'
fill.data.size = 14

def look_at(cam, target):
    cam.rotation_mode = 'QUATERNION'
    d = Vector(target) - cam.location
    cam.rotation_quaternion = d.to_track_quat('-Z', 'Y')

def shot(name, loc, target, lens, rx, ry):
    bpy.ops.object.camera_add(location=loc)
    cam = add("RIG_Cam_" + name, bpy.context.active_object)
    cam.data.lens = lens
    cam.data.clip_end = 300
    look_at(cam, target)
    scene.camera = cam
    scene.render.resolution_x = rx
    scene.render.resolution_y = ry
    scene.render.filepath = os.path.join(RENDERS, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("rendered", name)

MID = (0, 0, 9.2)
shot("front", (0, -36, 9.2), MID, 52, 1000, 1500)
shot("side", (36, 0, 9.2), MID, 52, 1000, 1500)
shot("three-quarter", (24, -25, 13.8), (0, 0, 9.0), 48, 1000, 1500)
shot("detail-tier1-joint", (3.2, -3.9, 7.6), (0, 0, 6.30), 55, 1200, 1000)
print("done")
