"""CP076 hero render recipe (= survey look/dud_fix/scripts/reframe_and_render.py render_cam, dud-fix v4):
apply_look(era_for_scene('CP076'), tod_for_scene('CP076')), 1280x720, 32 spp, no camera re-aim.
blender -b ROUND.blend -P scripts/render_cp076_look.py -- OUT.png [CAM] [SCENE_ID] [EXPOSURE]
Each camera is rendered in its own Blender session (one cam per call) so regressions compare like with like."""
import sys, bpy
from pathlib import Path
sys.path.insert(0, "/workspace/crystal-palace-survey/look")
from crystal_palace_look import apply_look, era_for_scene, tod_for_scene
a = sys.argv[sys.argv.index("--") + 1:]
out = Path(a[0]); cam = a[1] if len(a) > 1 else "CAM_CP076_empty_plateau_35mm"; sid = a[2] if len(a) > 2 else "CP076"
exp = float(a[3]) if len(a) > 3 and a[3] != "none" else None
sc = bpy.context.scene; sc.camera = bpy.data.objects[cam]
info = apply_look(era=era_for_scene(sid), time_of_day=tod_for_scene(sid), exposure=exp, high_contrast=False)
print("LOOK", info, flush=True)
sc.render.resolution_x, sc.render.resolution_y = 1280, 720; sc.render.resolution_percentage = 100
sc.cycles.samples = 32; sc.render.filepath = str(out); out.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.render.render(write_still=True); print("RENDERED", cam, out, "exposure", sc.view_settings.exposure, flush=True)
