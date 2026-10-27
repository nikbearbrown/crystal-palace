"""Render named cameras from an exterior .blend, optionally with Claude's west frame and Grok's transept appended
read-only (never saved). Claude's roof glass is overridden with ours at render time unless --no-roof-override (EX24).
blender -b rounds/xNN.blend -P render_views.py -- --cams A,B --outdir renders/xNN --res 1280x720 --samples 48
        [--claude claude.blend] [--transept transept.blend] [--no-roof-override] [--no-furrow]"""
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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from combine import combine
cams = arg("--cams").split(","); outdir = arg("--outdir"); W, H = map(int, arg("--res", "1280x720").split("x"))
sc = bpy.context.scene; sc.cycles.samples = int(arg("--samples", "48"))
sc.render.threads_mode = 'FIXED'; sc.render.threads = int(arg("--threads", "8"))
combine(arg("--claude"), arg("--transept"), roof_override="--no-roof-override" not in argv, furrow=bool(arg("--claude")) and "--no-furrow" not in argv)
# apply shared look once per blend (override with --era / --tod)
_era = arg("--era", "1851"); _tod = arg("--tod", "exterior_midday")
apply_look(era=_era, time_of_day=_tod)
if arg("--exposure"): sc.view_settings.exposure = float(arg("--exposure"))
os.makedirs(outdir, exist_ok=True)
base_exp = sc.view_settings.exposure
ortho_exp = sc.get("grok_ortho_exposure", base_exp - 0.55)
for c in cams:
    cam = bpy.data.objects.get(c)
    if not cam: print("NO CAM", c); continue
    sc.camera = cam; sc.render.resolution_x, sc.render.resolution_y = W, H
    # x07: ortho elevation contrast pass
    if cam.data.type == 'ORTHO':
        sc.view_settings.exposure = float(ortho_exp)
        try: sc.view_settings.look = 'AgX - High Contrast'
        except TypeError: pass
    else:
        sc.view_settings.exposure = base_exp
    sc.render.filepath = os.path.join(outdir, c + ".png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath, flush=True)
