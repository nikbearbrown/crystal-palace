"""Render named cameras of a built round. Per-camera custom props: res 'WxH' (scaled to --res width class), exposure.
blender -b rounds/X.blend -P render_views.py -- --cams A,B --outdir renders/X --res 1280x720 --samples 48 [--exposure E] [--threads 8]"""
import bpy, sys, os

# crystal-palace-look v1 (shared grade)
try:
    from cpl_look import apply_look, era_for_scene, tod_for_scene
except ImportError:
    import sys as _s
    _s.path.insert(0, "/workspace/crystal-palace-survey/look")
    from crystal_palace_look import apply_look, era_for_scene, tod_for_scene

# crystal-palace-people v2 (swap lathe crowds → articulated; skip with --no-people)
try:
    from cpl_people import swap_scene_people, PEOPLE_VERSION as _PPL_VER
except ImportError:
    import sys as _s
    from pathlib import Path as _P
    _s.path.insert(0, "/workspace/crystal-palace-survey/people")
    try:
        from people_lib import swap_scene_people, PEOPLE_VERSION as _PPL_VER
    except ImportError:
        swap_scene_people = None; _PPL_VER = None

argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
sc = bpy.context.scene; W, H = map(int, arg("--res", "1280x720").split("x")); sc.cycles.samples = int(arg("--samples", "48"))
sc.render.threads_mode = 'FIXED'; sc.render.threads = int(arg("--threads", "8")); base_exp = sc.view_settings.exposure
_era = arg("--era", "1850"); _tod = arg("--tod", "exterior_midday")
_look = apply_look(era=_era, time_of_day=_tod)
base_exp = _look["exposure"]
if arg("--exposure"): sc.view_settings.exposure = float(arg("--exposure"))
os.makedirs(arg("--outdir"), exist_ok=True)
cams = arg("--cams").split(",") if arg("--cams") != "ALL" else sorted(o.name for o in bpy.data.objects if o.type == 'CAMERA')
for c in cams:
    ob = bpy.data.objects[c]; sc.camera = ob
    if swap_scene_people is not None and "--no-people" not in argv:
        _pst = swap_scene_people(era=_era, camera=sc.camera)
        print("PEOPLE", _PPL_VER, _pst, flush=True)

    sid = c.rsplit("_", 1)[0]
    for o in bpy.data.objects:   # objects tagged only_cams="ID,ID" render only for those shots (diagram backdrops, labels)
        if o.get("only_cams"): o.hide_render = sid not in o["only_cams"].split(",")
    if ob.get("res"):   # per-shot frame (e.g. portrait diagram), scaled by --res width / 1280
        w, h = map(int, ob["res"].split("x")); k = W / 1280; sc.render.resolution_x, sc.render.resolution_y = int(w * k), int(h * k)
    else: sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.view_settings.exposure = float(arg("--exposure")) if arg("--exposure") else (ob.get("exposure", base_exp) if "--cam-exposure" in argv else base_exp)
    sc.render.filepath = os.path.join(arg("--outdir"), c + ".png"); bpy.ops.render.render(write_still=True); print("WROTE", sc.render.filepath)
