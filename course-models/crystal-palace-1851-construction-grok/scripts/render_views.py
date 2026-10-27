"""Render named cameras from a construction .blend.
blender -b rounds/cNN.blend -P render_views.py -- --cams A,B --outdir renders/cNN --res 1280x720 --samples 48 [--frame N]"""
import bpy, sys, os
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
cams = arg("--cams").split(","); outdir = arg("--outdir"); W, H = map(int, arg("--res", "1280x720").split("x"))
sc = bpy.context.scene; sc.cycles.samples = int(arg("--samples", "48"))
sc.render.threads_mode = 'FIXED'; sc.render.threads = int(arg("--threads", "8"))
fr = arg("--frame"); suffix = arg("--suffix", "")
if fr: sc.frame_set(int(fr))
os.makedirs(outdir, exist_ok=True)
for c in cams:
    cam = bpy.data.objects.get(c)
    if not cam: print("NO CAM", c); continue
    sc.camera = cam; sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.filepath = os.path.join(outdir, c + suffix + ".png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath, flush=True)
