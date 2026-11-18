"""CP052 live hero recipe = survey dud-fix v4 (look/dud_fix/scripts/reframe_and_render.py, 2026-10-27): the blend as saved by the
reframe (camera already in place), look v1.1 apply_look(era_for_scene('CP052'), tod_for_scene('CP052')) = 1852 / exterior_afternoon
(-0.8 EV), 1280x720, 32 spp. r16 + this recipe = renders/r16/r16_CAM_CP052_scaffold_reglaze_35mm.png (max diff 0, 2026-11-18).
usage: blender -b <blend> -P scripts/render_cp052_look.py -- out.png [cam] [spp] [WxH]"""
import sys, bpy
sys.path.insert(0, "/workspace/crystal-palace-survey/look")
from crystal_palace_look import apply_look, era_for_scene, tod_for_scene
argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]; cam = argv[1] if len(argv) > 1 else "CAM_CP052_scaffold_reglaze_35mm"
spp = int(argv[2]) if len(argv) > 2 else 32
res = argv[3] if len(argv) > 3 else "1280x720"
sc = bpy.context.scene
sc.camera = bpy.data.objects[cam]
info = apply_look(era=era_for_scene("CP052"), time_of_day=tod_for_scene("CP052"), exposure=None, high_contrast=False)
print("LOOK", info)
w, h = map(int, res.split("x"))
sc.render.resolution_x, sc.render.resolution_y = w, h
sc.render.resolution_percentage = 100
sc.cycles.samples = spp
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("RENDERED", out)
