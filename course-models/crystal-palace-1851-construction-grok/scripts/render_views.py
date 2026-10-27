"""Render named cameras of a built round. Per-camera custom props: res 'WxH' (scaled to --res width class), exposure.
blender -b rounds/X.blend -P render_views.py -- --cams A,B --outdir renders/X --res 1280x720 --samples 48 [--exposure E] [--threads 8]"""
import bpy, sys, os
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
sc = bpy.context.scene; W, H = map(int, arg("--res", "1280x720").split("x")); sc.cycles.samples = int(arg("--samples", "48"))
sc.render.threads_mode = 'FIXED'; sc.render.threads = int(arg("--threads", "8")); base_exp = sc.view_settings.exposure
os.makedirs(arg("--outdir"), exist_ok=True)
cams = arg("--cams").split(",") if arg("--cams") != "ALL" else sorted(o.name for o in bpy.data.objects if o.type == 'CAMERA')
for c in cams:
    ob = bpy.data.objects[c]; sc.camera = ob
    sid = c.rsplit("_", 1)[0]
    for o in bpy.data.objects:   # objects tagged only_cams="ID,ID" render only for those shots (diagram backdrops, labels)
        if o.get("only_cams"): o.hide_render = sid not in o["only_cams"].split(",")
    if ob.get("res"):   # per-shot frame (e.g. portrait diagram), scaled by --res width / 1280
        w, h = map(int, ob["res"].split("x")); k = W / 1280; sc.render.resolution_x, sc.render.resolution_y = int(w * k), int(h * k)
    else: sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.view_settings.exposure = float(arg("--exposure")) if arg("--exposure") else ob.get("exposure", base_exp)
    sc.render.filepath = os.path.join(arg("--outdir"), c + ".png"); bpy.ops.render.render(write_still=True); print("WROTE", sc.render.filepath)
