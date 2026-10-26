"""Render named cameras from an exterior .blend, optionally with Claude's west frame and Grok's transept appended
read-only (never saved). Claude's roof glass is overridden with ours at render time unless --no-roof-override (EX24).
blender -b rounds/xNN.blend -P render_views.py -- --cams A,B --outdir renders/xNN --res 1280x720 --samples 48
        [--claude claude.blend] [--transept transept.blend] [--no-roof-override]"""
import bpy, sys, os
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from combine import combine
cams = arg("--cams").split(","); outdir = arg("--outdir"); W, H = map(int, arg("--res", "1280x720").split("x"))
sc = bpy.context.scene; sc.cycles.samples = int(arg("--samples", "48"))
sc.render.threads_mode = 'FIXED'; sc.render.threads = int(arg("--threads", "8"))
combine(arg("--claude"), arg("--transept"), roof_override="--no-roof-override" not in argv)
os.makedirs(outdir, exist_ok=True)
for c in cams:
    cam = bpy.data.objects.get(c)
    if not cam: print("NO CAM", c); continue
    sc.camera = cam; sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.filepath = os.path.join(outdir, c + ".png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath, flush=True)
