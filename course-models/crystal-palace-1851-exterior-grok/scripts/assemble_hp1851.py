"""HP1851 complete: one self-contained film scene = Claude's west frame + Grok transept + Grok exterior (east half,
north strip, walls, ends, flags, park), with every camera of the route and a film-order marker track (EX25).
blender -b rounds/xNN.blend -P scripts/assemble_hp1851.py -- --claude CLAUDE.blend --transept TRANSEPT.blend --out assembly/HP1851_complete.blend
Sources are appended (copied) read-only; nothing is ever saved into Claude's or the transept's file. Claude's roof
units get GT_RoofGlassExt inside this assembly only (EX24)."""
import bpy, sys, os, json
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from combine import combine
claude, transept, out = os.path.abspath(arg("--claude")), os.path.abspath(arg("--transept")), os.path.abspath(arg("--out"))
sc = bpy.context.scene; sc.name = "HP1851_complete"
res = combine(claude, transept)
ext_cams = bpy.data.collections["CAMERAS_GROK"]; ext_cams.name = "CAMERAS_EXTERIOR"
# transept cameras (their own collection, outside TRANSEPT_GROK)
with bpy.data.libraries.load(transept, link=False) as (src, dst):
    dst.collections = [c for c in src.collections if c == "CAMERAS_GROK"]
tc = dst.collections[0]; tc.name = "CAMERAS_TRANSEPT"; sc.collection.children.link(tc)
# Claude's review cameras (objects only, not his lights)
with bpy.data.libraries.load(claude, link=False) as (src, dst):
    dst.objects = [o for o in src.objects if o.startswith("cam_")]
cc = bpy.data.collections.new("CAMERAS_CLAUDE"); sc.collection.children.link(cc)
for o in dst.objects:
    if o and o.type == 'CAMERA': cc.objects.link(o)
# merged route as a text block
tr = json.load(open(os.path.join(os.path.dirname(transept), "..", "route", "camera_route.json")))
er = json.load(open(os.path.join(HERE, "..", "route", "camera_route.json")))
txt = bpy.data.texts.new("HP1851_camera_route.json")
txt.write(json.dumps({"frame": er.get("frame"), "transept": tr["shots"], "exterior": er["shots"],
                      "claude_review_cams": [o.name for o in cc.objects]}, indent=1))
# film-order marker track: approach, ends, CP008 build-around, CP017 park inside, interior, fountain, Talbot, gallery, aerial
order = ["EXT_SE_34_start", "EXT_east_end_start", "EXT_NE_strip_start", "CP008_build_around_start", "CP008_build_around_end",
         "CP017_park_inside_start", "CP017_park_inside_end", "EXT_int_east_nave_start", "DET_fountain_start",
         "REF_talbot_start", "OPEN_gallery_start", "REF_aerial_SE_start"]
f = 1; placed = []
for name in order:
    cam = bpy.data.objects.get(name)
    if not cam: print("MISSING CAM", name); continue
    m = sc.timeline_markers.new(name, frame=f); m.camera = cam; placed.append((f, name)); f += 96
sc.frame_start, sc.frame_end = 1, f - 1; sc.render.fps = 24
sc.camera = bpy.data.objects.get(order[0])
sc["hp1851_assembly"] = json.dumps({"claude": os.path.basename(claude), "transept": os.path.basename(transept),
                                    "roof_override_slots": res.get("roof_slots"), "markers": placed})
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
print("ASSEMBLY", out, "markers", len(placed), "cams", len([o for o in bpy.data.objects if o.type == 'CAMERA']))
