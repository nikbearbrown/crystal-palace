#!/usr/bin/env python3
"""Render rig for paxton-gutter: ONE fixed neutral-grey studio setup.

Grey world, large ground plane, sun + fill. The prop objects are lifted
0.055 m in this render copy only (so the main gutter's under-board nuts,
which sit below the z=0 datum in reality, clear the studio floor); the
saved prop file is NOT modified.
Cameras: front (long elevation), side (END SECTION - the money shot),
three-quarter, plus close end-section shots of each gutter.
Cycles CPU (libEGL is absent on this VM, so Eevee cannot run).
"""
import bpy
import math
import os
from mathutils import Vector

BLEND = "/home/hatch/workspace/cp-models/paxton-gutter/paxton-gutter.blend"
OUT = "/home/hatch/workspace/cp-models/paxton-gutter/renders/"
bpy.ops.wm.open_mainfile(filepath=BLEND)
scene = bpy.context.scene

# lift props in the render copy so the under-board nuts clear the floor
for obj in scene.objects:
    obj.location.z += 0.055
LIFT = 0.055

# grey world
world = bpy.data.worlds["World"]
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.45, 0.45, 0.45, 1.0)
bg.inputs[1].default_value = 1.0

# ground
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -0.001))
gnd = bpy.context.active_object
gnd.name = "Ground"
m = bpy.data.materials.new("GroundGrey")
m.use_nodes = True
m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.38, 0.38, 0.38, 1)
m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
gnd.data.materials.append(m)

# lights: key sun + soft fill
def add_sun(name, loc, energy, angle_deg):
    d = bpy.data.lights.new(name, 'SUN')
    d.energy = energy
    d.angle = math.radians(angle_deg)
    o = bpy.data.objects.new(name, d)
    o.location = loc
    o.rotation_euler = (math.radians(55), math.radians(8), math.radians(-38))
    scene.collection.objects.link(o)

add_sun("KeySun", (4, -3, 7), 3.4, 12)
add_sun("FillSun", (-5, 4, 4), 0.9, 25)

def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()

def add_cam(name, loc, target, lens=50):
    d = bpy.data.cameras.new(name)
    d.lens = lens
    d.clip_end = 200
    o = bpy.data.objects.new(name, d)
    o.location = loc
    scene.collection.objects.link(o)
    look_at(o, target)
    return o

# name: (camera, res_x, res_y)
cams = {
    "front": (add_cam("front", (0, -9.8, 0.38),
                      (0, 0, 0.10 + LIFT), 58), 1800, 470),
    "side": (add_cam("side", (8.3, 0.03, 0.33),
                     (3.60, 0.03, 0.10 + LIFT), 80), 1700, 560),
    "three-quarter": (add_cam("three-quarter", (5.4, -4.9, 2.7),
                              (0, 0, 0.08 + LIFT), 50), 1800, 1050),
    "end-section-paxton": (add_cam("endpx", (4.85, -0.46, 0.18),
                                   (3.658, -0.46, 0.085 + LIFT), 85), 1300, 1000),
    "end-section-main": (add_cam("endmg", (5.0, 0.46, 0.22),
                                 (3.658, 0.46, 0.115 + LIFT), 85), 1300, 1000),
}

scene.render.engine = 'CYCLES'
scene.cycles.samples = int(os.environ.get("SAMPLES", "32"))
scene.cycles.device = 'CPU'
scene.render.film_transparent = False

ONLY = os.environ.get("VIEWS", "").split(",") if os.environ.get("VIEWS") else None
col_px = bpy.data.collections.get("Paxton_Gutter_24ft")
col_mg = bpy.data.collections.get("Main_Gutter_24ft")
for name, (cam, rx, ry) in cams.items():
    if ONLY and name not in ONLY:
        continue
    # isolate the subject in the two end-section close-ups
    if col_px and col_mg:
        col_px.hide_render = (name == "end-section-main")
        col_mg.hide_render = (name == "end-section-paxton")
    scene.camera = cam
    scene.render.resolution_x = rx
    scene.render.resolution_y = ry
    scene.render.filepath = OUT + name + ".png"
    bpy.ops.render.render(write_still=True)
    print("rendered", name)
