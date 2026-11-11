"""CP076 hero render recipe (= survey look/dud_fix/scripts/reframe_and_render.py render_cam, dud-fix v4):
apply_look(era_for_scene('CP076'), tod_for_scene('CP076')), 1280x720, 32 spp, no camera re-aim.
blender -b ROUND.blend -P scripts/render_cp076_look.py -- OUT.png [CAM] [SCENE_ID] [EXPOSURE] [WxH] [SAMPLES]
Optional WxH / SAMPLES override the 1280x720 / 32 spp defaults (defaults unchanged for CP076). CP073 live hero passes
1920x1080 24: the film's 1080p delivery size and the sample count the pre-KEEP r17k CP073 hero was rendered with
(PNG metadata cycles.ViewLayer.samples = 24; the r17 blend's own scene setting is 48 but was overridden at render time).
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
rx, ry = map(int, a[4].split("x")) if len(a) > 4 and a[4] != "default" else (1280, 720)
spp = int(a[5]) if len(a) > 5 else 32
sc.render.resolution_x, sc.render.resolution_y = rx, ry; sc.render.resolution_percentage = 100
sc.cycles.samples = spp; sc.render.filepath = str(out); out.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.render.render(write_still=True); print("RENDERED", cam, out, "exposure", sc.view_settings.exposure, "res", rx, ry, "spp", spp, flush=True)
