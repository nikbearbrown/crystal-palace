"""2026-11-02 CANDIDATE v3 (Grok Bot executor, not a verdict): CP016_wheels, no-glaziers line only.
Base: rounds/candidates/c06_cp016wheels_v2_noglaziers.blend (stub axles + front32 cam, CN44). Saves
rounds/candidates/c06_cp016wheels_v3.blend (CP016_wheels only; never render other shots from it).
Parent verdict on v2 (2026-11-02): the pre-swapped far workmen (wagons 1-3, gutter men) read as pale bare-torso figures,
one with an odd raised arm. Fix, in this blend only (people_lib and its shared CPL3_* materials untouched):
  * each pre-swapped KWORKER_*_CP016 gets its CPL3_smock_* slot replaced by a local, dark period fustian
    (CP016V3_fustian_blue / _grey / _drab, matte, no sheen), so the torso no longer reads as skin;
  * --hide NAMES   comma list hidden (render + viewport) in this shot, e.g. the raised-arm 'pointing' gutter man;
  * --repose NAMES comma list rebuilt from people_lib 1850s_workman 'working' (same LOD/seed/transform) instead of 'pointing'.
blender -b rounds/candidates/c06_cp016wheels_v2_noglaziers.blend -P scripts/cand_cp016_wheels_v3_20261102.py -- --hide KWORKER_028_CP016,KPANE_SLIDING_1 --repose KWORKER_029_CP016,KWORKER_030_CP016"""
import bpy, os, sys, hashlib
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
def names(n): return [s for s in (arg(n, "") or "").split(",") if s]
# brown was tried (try2) and dropped: in back view on the muscular base mesh it read as a tanned bare back
# order matters (round-robin over sorted names): hero wagon_1 men 015/016 get blue/grey; drab olive on the back-view hero read a bit "green muscle" (try3)
FUSTIAN = {"blue": (0.030, 0.042, 0.075), "grey": (0.050, 0.050, 0.048), "drab": (0.040, 0.044, 0.034)}
mats = {}
for k, c in FUSTIAN.items():
    m = bpy.data.materials.get(f"CP016V3_fustian_{k}") or bpy.data.materials.new(f"CP016V3_fustian_{k}")
    m.use_nodes = True; b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*c, 1.0); b.inputs["Roughness"].default_value = 0.95
    for s in ("Specular IOR Level", "Specular"):
        if s in b.inputs: b.inputs[s].default_value = 0.2; break
    if "Sheen Weight" in b.inputs: b.inputs["Sheen Weight"].default_value = 0.0
    m.diffuse_color = (*c, 1.0); mats[k] = m
order = list(FUSTIAN)
workers = sorted(o.name for o in bpy.data.objects if o.name.startswith("KWORKER_") and o.name.endswith("_CP016") and o.get("cand_v2_20261102"))
if names("--repose"):
    sys.path.insert(0, "/workspace/crystal-palace-survey/people"); import people_lib as PL
    for n in names("--repose"):
        o = bpy.data.objects[n]; lod = "hero" if "hero" in o.data.name else "mid"
        seed = int(hashlib.md5(o.name.encode()).hexdigest()[:6], 16)
        tmp = PL._build_person("1850s_workman", "working", lod, seed); mw = o.matrix_world.copy()
        o.data = tmp.data; bpy.data.objects.remove(tmp, do_unlink=True); o.matrix_world = mw; o.scale = (1, 1, 1)
        o["cand_v3_20261102"] = f"repose working {lod}"; print("REPOSE", n, lod)
for i, n in enumerate(workers):
    o = bpy.data.objects[n]; me = o.data
    if me.users > 1: o.data = me = me.copy()   # never retint a mesh shared with other objects
    k = order[i % len(order)]
    for si, m in enumerate(me.materials):
        if m and (m.name.startswith("CPL3_smock") or m.name.startswith("CPL3_waist")): me.materials[si] = mats[k]
    o["cand_v3_20261102"] = (o.get("cand_v3_20261102", "") + f" fustian {k}").strip(); print("FUSTIAN", n, k)
for n in names("--hide"):
    o = bpy.data.objects[n]; o.hide_render = True; o.hide_viewport = True; o["cand_v3_20261102"] = "hidden in CP016_wheels v3"; print("HIDE", n)
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = arg("--out") or os.path.join(here, "rounds", "candidates", "c06_cp016wheels_v3.blend")
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True); print("SAVED", out)
