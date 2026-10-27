import bpy, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "south-entrance-pedestals.blend"))
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 96
scene.cycles.use_denoising = False
scene.cycles.device = 'CPU'
scene.render.resolution_x = 1200
scene.render.resolution_y = 1050
for name, camname in [("front", "CamFront"), ("side", "CamSide"), ("three-quarter", "CamTQ")]:
    scene.camera = bpy.data.objects[camname]
    scene.render.filepath = os.path.join(ROOT, "renders", name + ".png")
    bpy.ops.render.render(write_still=True)
    print("rendered", name)
print("RENDERS DONE")
