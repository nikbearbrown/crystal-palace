"""CANDIDATE v2: envelope e02 with CP024_ram_start camera restored to the live
close-up (the v1 envelope pulled it back to a wide that duplicated CP024_approach).
  blender -b rounds/candidates/e02_envelope.blend -P scripts/envelope_restore_ramcam.py
"""
import bpy, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = os.path.join(ROOT, "rounds/e02.blend")
OUT = os.path.join(ROOT, "rounds/candidates/e02_envelope_v2.blend")
cam = bpy.data.objects["CP024_ram_start"]
with bpy.data.libraries.load(LIVE, link=False) as (src, dst):
    dst.objects = ["CP024_ram_start"]
live = [o for o in dst.objects if o][0]
cam.animation_data_clear()
if live.animation_data and live.animation_data.action:
    cam.animation_data_create(); cam.animation_data.action = live.animation_data.action
cam.parent = live.parent if live.parent and live.parent.name in bpy.data.objects else cam.parent
cam.matrix_world = live.matrix_world.copy()
cam.location = live.location.copy(); cam.rotation_mode = live.rotation_mode
cam.rotation_euler = live.rotation_euler.copy(); cam.rotation_quaternion = live.rotation_quaternion.copy()
cam.data.lens = live.data.lens
cons = [c.type for c in live.constraints]
print("LIVE_CAM", tuple(round(v,2) for v in live.location), live.data.lens, "anim", bool(live.animation_data), "cons", cons, flush=True)
bpy.data.objects.remove(live, do_unlink=True)
cam["candidate"] = "hp_interior_envelope_v2_ramcam_restored"
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT, flush=True)
