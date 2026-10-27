"""render named cameras from a built .blend (never saves it).
  blender -b rounds/m01.blend -P scripts/render_shots.py -- --out renders/m01 --cams A,B --samples 64 --pct 100
Optional per-shot state hook: if the scene holds a text block 'grok_states' (json {cam_prefix: {"hide": [...], "show": [...]}}),
objects whose name starts with a listed prefix are hidden/shown for that camera."""
import bpy, sys, os, json
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
sc = bpy.context.scene; out = os.path.abspath(arg("--out", "renders/tmp")); os.makedirs(out, exist_ok=True)
sc.cycles.samples = int(arg("--samples", "64")); sc.render.resolution_percentage = int(arg("--pct", "100"))
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_depth = '8'
cams = arg("--cams", "").split(",") if arg("--cams") else [o.name for o in bpy.data.objects if o.type == 'CAMERA']
states = json.loads(bpy.data.texts["grok_states"].as_string()) if "grok_states" in bpy.data.texts else {}
base = {o.name: o.hide_render for o in bpy.data.objects}
exp0 = sc.view_settings.exposure
for cn in cams:
    cam = bpy.data.objects[cn]; sc.camera = cam
    for n, h in base.items(): bpy.data.objects[n].hide_render = h
    sc.view_settings.exposure = exp0
    for pre, st in states.items():
        if cn.startswith(pre):
            for o in bpy.data.objects:
                if any(o.name.startswith(p) for p in st.get("hide", [])): o.hide_render = True
                if any(o.name.startswith(p) for p in st.get("show", [])): o.hide_render = False
            if "exposure" in st: sc.view_settings.exposure = st["exposure"]
    sc.render.filepath = os.path.join(out, cn + ".png"); bpy.ops.render.render(write_still=True)
    print("RENDERED", cn, flush=True)
