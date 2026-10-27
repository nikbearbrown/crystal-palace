#!/usr/bin/env python3
"""
Render rig for alhambra-lion-fountain: ONE fixed neutral-grey studio rig.
Opens the model .blend, adds backdrop + lights + cameras, renders
front / side / three-quarter. Does NOT save the .blend.
Args: 'quick' for low-res iteration; a view name to render only that view.
"""
import bpy
import math
import os
import sys
from mathutils import Vector

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLEND = os.path.join(BASE, "alhambra-lion-fountain.blend")
OUT = os.path.join(BASE, "renders")
os.makedirs(OUT, exist_ok=True)

ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
QUICK = 'quick' in ARGS
ONLY = [a for a in ARGS if a in ('front', 'side', 'three-quarter')]

bpy.ops.wm.open_mainfile(filepath=BLEND)
scene = bpy.context.scene

scene.render.engine = 'CYCLES'
scene.cycles.samples = 24 if QUICK else 64
scene.cycles.use_denoising = not QUICK
scene.cycles.device = 'CPU'
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.02
scene.render.resolution_x = 500 if QUICK else 1000
scene.render.resolution_y = 625 if QUICK else 1250
scene.render.film_transparent = False
scene.world = bpy.data.worlds.new("RigWorld")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.40, 0.40, 0.40, 1.0)
bg.inputs[1].default_value = 1.0
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Base Contrast'

grey = bpy.data.materials.new("BackdropGrey")
grey.use_nodes = True
gbsdf = grey.node_tree.nodes["Principled BSDF"]
gbsdf.inputs["Base Color"].default_value = (0.46, 0.46, 0.46, 1.0)
gbsdf.inputs["Roughness"].default_value = 0.95

bpy.ops.mesh.primitive_circle_add(radius=16.0, vertices=64, fill_type='NGON',
                                  location=(0, 0, -0.002))
floor = bpy.context.active_object
floor.name = "RigFloor"
floor.data.materials.append(grey)

def softbox(name, loc, rot, size, energy):
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = (size[0], size[1], 1.0)
    o.rotation_euler = rot
    m = bpy.data.materials.new(name + "Mat")
    m.use_nodes = True
    em = m.node_tree.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
    em.inputs[1].default_value = energy
    m.node_tree.links.new(em.outputs[0], m.node_tree.nodes["Material Output"].inputs[0])
    o.data.materials.append(m)
    o.visible_camera = False
    return o

D = math.radians
softbox("SoftL", (-6, -2, 4.5), (D(90), 0, D(65)), (5, 9), 5.0)
softbox("SoftR", (6, -1.5, 5), (D(90), 0, D(-115)), (4, 8), 4.0)
softbox("SoftTop", (0, 2, 10), (D(15), 0, 0), (8, 4), 5.0)
softbox("SoftBack", (0, 9, 5), (D(90), 0, D(180)), (9, 7), 3.0)

def area(name, loc, energy, size, look=(0, 0, 1.3)):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.energy = energy
    ld.shape = 'DISK'
    ld.size = size
    o = bpy.data.objects.new(name, ld)
    bpy.context.collection.objects.link(o)
    o.location = loc
    d = Vector(look) - Vector(loc)
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return o

area("Key", (-5, -6.5, 9), 900, 5)
area("Fill", (5.5, -4, 5), 350, 4)
area("Rim", (2, 7.5, 7.5), 700, 4)

def cam(name, loc, look=(0, 0, 1.30), lens=50):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.clip_end = 200
    o = bpy.data.objects.new(name, cd)
    bpy.context.collection.objects.link(o)
    o.location = loc
    d = Vector(look) - Vector(loc)
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return o

cams = {
    'front': cam("CamFront", (0, -8.4, 1.75)),
    'side': cam("CamSide", (8.4, 0, 1.75)),
    'three-quarter': cam("CamTQ", (5.9, -5.9, 3.4), look=(0, 0, 1.25)),
}

for name, c in cams.items():
    if ONLY and name not in ONLY:
        continue
    scene.camera = c
    scene.render.filepath = os.path.join(OUT, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED", name)

print("RIG DONE")
