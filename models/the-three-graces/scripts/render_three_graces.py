#!/usr/bin/env python3
"""Render the Three Graces prop on ONE fixed neutral-grey rig:
front, side, three-quarter. Run after build_three_graces.py:
  blender -b -noaudio --python render_three_graces.py
"""
import bpy, os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "renders")
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "the-three-graces.blend"))
scene = bpy.context.scene

# neutral grey world + ground (assign the world explicitly — a loaded
# factory file may have none, and an unassigned world renders black)
world = bpy.data.worlds.new("rig world")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.40, 0.40, 0.40, 1.0)
world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

def grey_mat(name, v):
    m = bpy.data.materials.new(name); m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (v, v, v, 1.0)
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
    return m

bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -0.001))
ground = bpy.context.active_object
ground.name = "rig ground"
ground.data.materials.append(grey_mat("rig ground grey", 0.52))

def look_at(obj, target):
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = (Vector(target) - obj.location).to_track_quat('-Z', 'Y')

def area_light(name, loc, energy, size, target=(0, 0, 1.85)):
    d = bpy.data.lights.new(name, 'AREA')
    d.energy = energy; d.shape = 'DISK'; d.size = size
    o = bpy.data.objects.new(name, d)
    bpy.context.collection.objects.link(o)
    o.location = loc
    look_at(o, target)
    return o

area_light("key",  (4.5, -3.5, 7.5), 650, 4.0)
area_light("fill", (-5.5, -1.0, 3.5), 220, 3.0)
area_light("rim",  (-1.0, 6.0, 6.5), 420, 3.0)

cam_data = bpy.data.cameras.new("rig camera")
cam_data.lens = 50
cam = bpy.data.objects.new("rig camera", cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam

scene.render.engine = 'BLENDER_WORKBENCH'
sh = scene.display.shading
sh.light = 'STUDIO'
sh.studiolight_rotate_z = 20.0
sh.show_cavity = True
sh.cavity_type = 'BOTH'
sh.curvature_ridge_factor = 1.2
sh.curvature_valley_factor = 0.8
sh.color_type = 'MATERIAL'
sh.background_type = 'WORLD'
scene.render.resolution_x = 1000
scene.render.resolution_y = 1150
scene.render.film_transparent = False

TARGET = Vector((0, 0, 1.85))
VIEWS = {
    "front":         Vector((0.0, 8.8, 2.0)),
    "side":          Vector((8.8, 0.0, 2.0)),
    "three-quarter": Vector((6.1, 6.1, 2.9)),
}
for name, loc in VIEWS.items():
    cam.location = loc
    look_at(cam, TARGET)
    scene.render.filepath = os.path.join(OUT, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED", name)
