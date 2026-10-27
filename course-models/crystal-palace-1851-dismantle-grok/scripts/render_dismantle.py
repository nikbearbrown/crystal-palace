"""Render HP-EMPTY / HP-DISMANTLE cameras. Opens the exterior x05 .blend (Grok), appends this folder's dNN_<state>.blend
(transept + dismantle dressing + cameras) and Claude's west frame read-only through the exterior's combine(), swaps
Muse's furrow bay in at render time, applies zones.py, renders. Nothing here is saved.
blender -b <exterior>/rounds/x05.blend -P render_dismantle.py -- --dismantle rounds/d01_dismantle.blend --state dismantle
        --cams A,B --outdir renders/d01 [--claude claude.blend] [--res 1280x720] [--samples 48]"""
import bpy, sys, os
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "..", "crystal-palace-1851-exterior-grok", "scripts")
sys.path.insert(0, EXT); sys.path.insert(0, HERE)
sys.path.insert(0, "/workspace/crystal-palace-survey/look")
from crystal_palace_look import apply_look
from combine import combine
import zones
state = arg("--state"); cams = arg("--cams").split(","); outdir = arg("--outdir"); W, H = map(int, arg("--res", "1280x720").split("x"))
sc = bpy.context.scene; sc.cycles.samples = int(arg("--samples", "48"))
sc.render.threads_mode = 'FIXED'; sc.render.threads = int(arg("--threads", "8"))
combine(arg("--claude"), arg("--dismantle"), roof_override=True, furrow=True)
for o in bpy.data.objects:          # flags struck after the closing (DM09)
    if o.get("part_kind") == "flag": o.hide_render = True; o.hide_viewport = True
zones.apply(state); zones.fix_floor_seam()
import json
ROUTE = {s["id"]: s for s in json.load(open(os.path.join(HERE, "..", "route", "camera_route.json")))["shots"]}
DUSK = "--dusk" in argv
if DUSK:
    zones.dusk()
    apply_look(era="1852", time_of_day="exterior_dusk", sky=False, clamp_mats=True)
else:
    tod = "interior_daylit" if state == "empty" else "exterior_afternoon"
    apply_look(era="1852", time_of_day=tod, clamp_mats=True)
BASE_EXP = sc.view_settings.exposure  # look sets exposure; route may refine
os.makedirs(outdir, exist_ok=True)
for c in cams:
    cam = bpy.data.objects.get(c)
    if not cam: print("NO CAM", c); continue
    sc.camera = cam; sc.render.resolution_x, sc.render.resolution_y = W, H
    shot = ROUTE.get(cam.get("shot", c.rsplit("_", 1)[0]), {})
    sc.view_settings.exposure = shot.get("dusk_exposure", BASE_EXP) if DUSK else BASE_EXP  # look v1 wins over day route
    print("EXPOSURE", c, sc.view_settings.exposure, flush=True)
    sc.render.filepath = os.path.join(outdir, c + ("_dusk" if DUSK else "") + ".png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath, flush=True)
