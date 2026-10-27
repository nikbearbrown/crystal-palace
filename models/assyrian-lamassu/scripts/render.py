#!/usr/bin/env python3
"""
Render rig for the Assyrian lamassu — ONE fixed neutral-grey setup for all views.
Usage: blender -b assyrian-lamassu.blend -P render.py
Outputs renders/front.png, renders/side.png, renders/three-quarter.png,
renders/photo-match.png (angle approximating the Delamotte facade photograph).
"""
import bpy
import math
import os
from mathutils import Vector

OUT = os.path.expanduser("~/workspace/cp-models/assyrian-lamassu/renders")
os.makedirs(OUT, exist_ok=True)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.use_denoising = False
scene.render.resolution_x = 760
scene.render.resolution_y = 760
scene.render.film_transparent = False

# neutral grey world
world = bpy.data.worlds.new("GreyWorld")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.52, 0.52, 0.52, 1.0)
bg.inputs[1].default_value = 1.0

# ground plane (render-only dressing, part of the rig, not the model)
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "RIG_Ground"
gm = bpy.data.materials.new("RigGrey")
gm.use_nodes = True
gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.56, 0.56, 0.56, 1.0)
gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
ground.data.materials.append(gm)

def add_light(name, type_, loc, energy, size=None, rot=(0, 0, 0)):
    ld = bpy.data.lights.new(name, type_)
    ld.energy = energy
    if type_ == 'AREA':
        ld.shape = 'DISK'
        ld.size = size
    if type_ == 'SUN':
        ld.angle = 0.35
    lo = bpy.data.objects.new(name, ld)
    bpy.context.collection.objects.link(lo)
    lo.location = loc
    lo.rotation_euler = rot
    return lo

# key sun from upper front-left, soft fill, top rim
add_light("RIG_Sun", 'SUN', (4, 5, 8), 3.2, rot=(math.radians(38), math.radians(8), math.radians(28)))
add_light("RIG_Fill", 'AREA', (-6, -4, 3.5), 450, size=6)
add_light("RIG_Rim", 'AREA', (-3, -6, 7), 500, size=5)

# aim area lights at the model centre
for lname in ("RIG_Fill", "RIG_Rim"):
    lo = bpy.data.objects[lname]
    d = Vector((0, 0, 1.5)) - lo.location
    lo.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

cam_data = bpy.data.cameras.new("Cam")
cam_data.clip_end = 200
cam = bpy.data.objects.new("Cam", cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam

TARGET = Vector((0.05, 0, 1.5))

import sys
ONLY = None
if "--" in sys.argv:
    args = sys.argv[sys.argv.index("--") + 1:]
    if args:
        ONLY = args[0]

def shoot(name, loc, lens=52):
    if ONLY and ONLY not in name:
        return
    cam.location = loc
    cam_data.lens = lens
    d = TARGET - cam.location
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    scene.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
    print("RENDERED", name)

# front: head-on to the face (+X)
shoot("front.png", Vector((8.6, 0.0, 1.75)))
# side: figure's left flank (+Y) — the side the photograph shows
shoot("side.png", Vector((0.05, 8.8, 1.75)))
# three-quarter: front-left, slightly above
shoot("three-quarter.png", Vector((5.6, 6.0, 3.3)))
# photo-match: approximates Delamotte's viewpoint down the facade row —
# front-left, near shoulder height, longer lens
shoot("photo-match.png", Vector((4.6, 5.4, 2.15)), lens=62)
print("ALL RENDERS DONE")
