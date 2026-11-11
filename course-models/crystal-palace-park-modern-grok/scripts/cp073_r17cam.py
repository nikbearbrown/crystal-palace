"""CP073 live camera on r21 (CP073 KEEP 2026-11-11, D-PM-32): copy the exact live r17 CAM_CP073_sphinx_steps_50mm transform
and lens (along-terrace cam, 35 mm lens despite the object name; D-PM-19) from rounds/parknow-r17.blend onto the same-named
camera in the open blend (rounds/parknow-r21_cp076.blend, which still carries the r02 50 mm transform). In-session only;
the blend is not saved, so parknow-r21_cp076.blend stays byte-identical (md5 bc62d275) and --rebuild still reproduces it.
blender -b rounds/parknow-r21_cp076.blend -P scripts/cp073_r17cam.py -P scripts/render_cp076_look.py -- OUT.png CAM_CP073_sphinx_steps_50mm CP073 -0.8"""
import bpy
from pathlib import Path
lib = str(Path(bpy.data.filepath).resolve().parent / "parknow-r17.blend")
with bpy.data.libraries.load(lib) as (src, dst):
    dst.objects = ["CAM_CP073_sphinx_steps_50mm"]
o = dst.objects[0]; c = bpy.data.objects["CAM_CP073_sphinx_steps_50mm"]
c.location = o.location.copy(); c.rotation_mode = o.rotation_mode; c.rotation_euler = o.rotation_euler.copy(); c.scale = o.scale.copy()
c.data.lens = o.data.lens; c.data.sensor_width = o.data.sensor_width; c.data.clip_end = max(c.data.clip_end, o.data.clip_end)
print("R17CAM", tuple(c.location), c.data.lens, flush=True)
