"""Render named cameras from a transept .blend.
blender -b rounds/rNN.blend -P render_views.py -- --cams A,B --outdir renders/rNN --res 960x540 --samples 48 [--portrait A] [--claude path.blend]"""
import bpy, sys, os
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
cams = arg("--cams").split(","); outdir = arg("--outdir"); W, H = map(int, arg("--res", "960x540").split("x"))
portrait = set((arg("--portrait", "") or "").split(","))
sc = bpy.context.scene; sc.cycles.samples = int(arg("--samples", "48"))
sc.render.threads_mode = 'FIXED'; sc.render.threads = int(arg("--threads", "8"))
claude = arg("--claude")
if claude:   # append Claude's model collection read-only (never saved)
    with bpy.data.libraries.load(claude, link=False) as (src, dst):
        dst.collections = [c for c in src.collections if c == "MODEL"]
    for c in dst.collections:
        if c: sc.collection.children.link(c)
    # hide our duplicates on Claude's line 37 (x = -36 ft)
    for ob in bpy.data.objects:
        if ob.get("claude_line37") or ob.get("claude_overlap"): ob.hide_render = True
        elif ob.get("part_kind") in ("column", "girder", "roof") and ob.location.x < -0.3048 * 36.5: ob.hide_render = True
os.makedirs(outdir, exist_ok=True)
for c in cams:
    cam = bpy.data.objects.get(c)
    if not cam: print("NO CAM", c); continue
    sc.camera = cam
    if c in portrait: sc.render.resolution_x, sc.render.resolution_y = H * 3 // 4, int(H * 1.0)
    else: sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.filepath = os.path.join(outdir, c + ".png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath, flush=True)
