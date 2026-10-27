#!/usr/bin/env python3
"""Fixed neutral-grey render rig for minerva-bust.
Views: front = the bust's front (-Y); side = its anatomical left
(+X, the profile the stereograph nearly shows); three-quarter from
(+X,-Y), the photograph's own quadrant; photomatch approximates the
stereograph's viewpoint for the compare image. Same world, lights
and backdrop for every view; Cycles CPU (no EGL in this VM)."""
import bpy
import os
from mathutils import Vector

OUT = os.path.expanduser("~/workspace/cp-models/minerva-bust/renders")
os.makedirs(OUT, exist_ok=True)
scene = bpy.context.scene

w = bpy.data.worlds.new("RigWorld") if not bpy.data.worlds else bpy.data.worlds[0]
scene.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.36, 0.36, 0.36, 1.0)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.55

bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
floor = bpy.context.active_object; floor.name = "RigFloor"
m = bpy.data.materials.new("RigGrey"); m.use_nodes = True
m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.30, 0.30, 0.30, 1.0)
m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
floor.data.materials.append(m)

def sun(name, loc, energy, angle=0.35):
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
    ld = bpy.data.lights.new(name, 'SUN'); ld.energy = energy; ld.angle = angle
    ob = bpy.data.objects.new(name, ld); bpy.context.collection.objects.link(ob)
    ob.location = loc
    d = Vector((0, 0, 1.4)) - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob

sun("KeySun", (-6, -5, 9), 3.2)
sun("FillSun", (6, 2, 5), 0.85)
sun("RimSun", (4, 6, 7), 1.1)

def cam(name, loc, target, ortho=None, lens=58):
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
    cd = bpy.data.cameras.new(name)
    ob = bpy.data.objects.new(name, cd); bpy.context.collection.objects.link(ob)
    ob.location = loc
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    if ortho:
        cd.type = 'ORTHO'; cd.ortho_scale = ortho
    else:
        cd.type = 'PERSP'; cd.lens = lens
    return ob

scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.cycles.device = 'CPU'
scene.render.resolution_percentage = 100
scene.render.film_transparent = False

import sys
ONLY = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ALL = [
    ("front",         (0.0, -7.6, 1.50), (0, 0, 1.42), 2.75, (760, 980)),
    ("side",          (7.6, 0.0, 1.50), (0, 0, 1.42), 2.75, (760, 980)),
    ("three-quarter", (3.05, -4.45, 2.75), (0, 0, 1.30), None, (900, 900)),
    ("photomatch",    (1.30, -2.45, 1.80), (-0.03, 0, 1.66), None, (760, 980)),
]
VIEWS = [v for v in ALL if not ONLY or v[0] in ONLY]
for name, loc, tgt, ortho, res in VIEWS:
    c = cam("Cam", loc, tgt, ortho=ortho)
    scene.camera = c
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.filepath = os.path.join(OUT, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("rendered", name)
