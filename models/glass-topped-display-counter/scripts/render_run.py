"""Render renders/run-three-quarter.png from the saved single-unit .blend:
duplicates the Model collection twice along X (in memory only, the file
is not re-saved) to show three units tiled into a counter run."""
import bpy, os
from mathutils import Vector

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
bpy.ops.wm.open_mainfile(filepath=os.path.join(BASE, "glass-topped-display-counter.blend"))
model = bpy.data.collections["Model"]
for k in (-1, 1):
    for o in list(model.objects):
        n = o.copy()
        n.data = o.data
        n.location = o.location + Vector((k * (3.658 + 0.03), 0, 0))
        model.objects.link(n)
scene = bpy.context.scene
# Cycles CPU: EEVEE's EGL stack is unavailable in this VM session
# (libEGL unresolved after a runtime restart); Cycles needs no EGL.
scene.render.engine = "CYCLES"
scene.cycles.samples = 64
scene.cycles.use_denoising = False
scene.cycles.device = "CPU"
scene.camera = bpy.data.objects["CamRun"]
scene.render.resolution_x = 1600
scene.render.resolution_y = 1000
scene.render.filepath = os.path.join(BASE, "renders", "run-three-quarter.png")
bpy.ops.render.render(write_still=True)
print("DONE")
