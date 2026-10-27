#!/usr/bin/env python3
"""Fixed neutral-grey render rig: front / side / three-quarter + plate crops for compare."""
import bpy, math, os
from mathutils import Vector

OUT = os.path.expanduser("~/workspace/cp-models/lattice-girder-truss-bay/renders")
os.makedirs(OUT, exist_ok=True)
scene = bpy.context.scene

# world: uniform neutral grey
world = bpy.data.worlds.new("RigWorld")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.55, 0.55, 0.55, 1.0)
bg.inputs[1].default_value = 1.0

# lights: key sun + soft fill
def add_sun(name, loc, energy, angle_deg):
    d = bpy.data.lights.new(name, 'SUN')
    d.energy = energy
    d.angle = math.radians(angle_deg)
    o = bpy.data.objects.new(name, d)
    o.location = loc
    o.rotation_euler = (math.radians(55), 0, math.radians(-35))
    scene.collection.objects.link(o)
add_sun("KeySun", (4, -6, 9), 3.2, 25)
add_sun("FillSun", (-6, 5, 4), 1.1, 40)

# ground shadow-catcher plane
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -0.001))
gp = bpy.context.active_object
gm = bpy.data.materials.new("GroundGrey")
gm.use_nodes = True
gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1.0)
gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
gp.data.materials.append(gm)

scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.cycles.use_denoising = True
scene.render.resolution_x = 1600
scene.render.resolution_y = 1000
scene.render.film_transparent = False

cam_data = bpy.data.cameras.new("RigCam")
cam = bpy.data.objects.new("RigCam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam

TARGET = Vector((0, 0, 1.55))

def look(cam, loc):
    cam.location = loc
    d = TARGET - Vector(loc)
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def shot(name, loc, ortho=None, lens=50):
    if ortho:
        cam_data.type = 'ORTHO'
        cam_data.ortho_scale = ortho
    else:
        cam_data.type = 'PERSP'
        cam_data.lens = lens
    look(cam, loc)
    scene.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
    print("RENDERED", name)

shot("front.png", (0, -13, 1.55), ortho=8.6)
shot("side.png", (13, 0, 1.62), ortho=6.6)
shot("three-quarter.png", (7.5, -8.5, 4.6), lens=42)
print("ALL RENDERS DONE")
