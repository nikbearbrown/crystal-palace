"""Render named cameras of a built round.
blender -b rounds/X.blend -P render_views.py -- --cams A,B --outdir renders/X --res 1280x720 --samples 48 [--exposure E] [--keep-lighting]"""
import bpy, sys, os
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
cams = arg("--cams").split(","); outdir = arg("--outdir"); W, H = map(int, arg("--res", "1280x720").split("x"))
sc = bpy.context.scene; sc.cycles.samples = int(arg("--samples", "48"))
sc.render.threads_mode = 'FIXED'; sc.render.threads = int(arg("--threads", "8")); base_exp = sc.view_settings.exposure
# --keep-lighting: preserve blend world/sun/exposure (geometry/material passes)
if "--keep-lighting" in argv:
    print("KEEP_LIGHTING exposure", sc.view_settings.exposure, flush=True)
    base_exp = sc.view_settings.exposure
else:
    try:
        from cpl_look import apply_look, era_for_scene, tod_for_scene
        _era = arg("--era") or era_for_scene(sc); _tod = arg("--tod") or tod_for_scene(sc)
        _look = apply_look(era=_era, time_of_day=_tod); base_exp = _look["exposure"]
    except Exception as e:
        print("LOOK_FALLBACK", e, flush=True)
if arg("--exposure"): sc.view_settings.exposure = float(arg("--exposure"))
os.makedirs(outdir, exist_ok=True)
for c in cams:
    cam = bpy.data.objects.get(c)
    if not cam:
        # try _start suffix
        cam = bpy.data.objects.get(c if c.endswith("_start") or c.endswith("_end") else c + "_start")
    if not cam: print("NO CAM", c); continue
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.view_settings.exposure = float(arg("--exposure")) if arg("--exposure") else base_exp
    sc.render.filepath = os.path.join(outdir, (c if c.endswith(".png") else cam.name) + ("" if cam.name.endswith(".png") else ""))
    # normalize filename to camera object name
    sc.render.filepath = os.path.join(outdir, cam.name + ".png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath, flush=True)
