"""Render named cameras from an exterior .blend, optionally with Claude's west frame and Grok's transept appended
read-only (never saved).
blender -b rounds/xNN.blend -P render_views.py -- --cams A,B --outdir renders/xNN --res 1280x720 --samples 48
        [--claude claude.blend] [--transept transept.blend]"""
import bpy, sys, os
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
FT = 0.3048
cams = arg("--cams").split(","); outdir = arg("--outdir"); W, H = map(int, arg("--res", "1280x720").split("x"))
sc = bpy.context.scene; sc.cycles.samples = int(arg("--samples", "48"))
sc.render.threads_mode = 'FIXED'; sc.render.threads = int(arg("--threads", "8"))
def append(path, name):
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.collections = [c for c in src.collections if c == name]
    for c in dst.collections:
        if c: sc.collection.children.link(c); return c
claude, transept = arg("--claude"), arg("--transept")
if claude: append(claude, "MODEL")
if transept:
    T = append(transept, "TRANSEPT_GROK")
    for ob in [o for o in T.all_objects if o is not None]:
        x, y, z = ob.location / FT; pk = ob.get("part_kind")
        if claude and (ob.get("claude_line37") or ob.get("claude_overlap") or (pk in ("column", "girder", "roof") and x < -36.5)):
            ob.hide_render = True
        if ob.name.startswith(("WALL_N1_", "WALLF_N1_", "WLOUV_N1_", "WALL_NE1", "WALLF_NE1", "WLOUV_NE1")):
            ob.hide_render = True                                        # opens into the north strip (EX06)
        if pk in ("wall", "wall_fill", "louvre") and abs(abs(x) - 132) < 0.2 and abs(y) < 132:
            ob.hide_render = True                                        # arm clerestory is interior once tier 2 runs on (EX07)
if transept:      # one park plane only: keep the transept's (r06 ground fix), drop ours
    for ob in bpy.data.objects:
        if ob.name.startswith("EGROUND_PARK"): ob.hide_render = True
os.makedirs(outdir, exist_ok=True)
for c in cams:
    cam = bpy.data.objects.get(c)
    if not cam: print("NO CAM", c); continue
    sc.camera = cam; sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.filepath = os.path.join(outdir, c + ".png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath, flush=True)
