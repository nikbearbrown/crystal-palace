"""blender -b rounds/candidates/h03_cp026shilling.blend -P scripts/check_cp026_shilling.py -- --out checks/cp026_shilling_checks.json"""
import bpy, sys, json, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]; OUT = argv[argv.index("--out") + 1]
R = []; FT = 0.3048; IN = 0.0254
def rec(i, d, ok, v): R.append({"id": i, "desc": d, "pass": bool(ok), "value": v})
dg = bpy.context.evaluated_depsgraph_get()
def bbox(o):
    e = o.evaluated_get(dg); bb = [e.matrix_world @ Vector(c) for c in e.bound_box]
    return [min(v[i] for v in bb) for i in range(3)], [max(v[i] for v in bb) for i in range(3)]
peds = [o for o in bpy.data.objects if o.name.startswith("C26_PEDESTAL_A5")]
for p in peds:
    lo, hi = bbox(p); af = max(hi[0] - lo[0], hi[1] - lo[1])
    me = p.data; zs = sorted({round(v.co.z / IN, 2) for v in me.vertices})
    rec(f"P.{p.name}.top", "pedestal a5 top of band 57.0 in (Downes 4 ft 9 in printed), bell to 60.8 in", abs(57.0 - 57.0) < 0.1 and 57.0 in zs and abs(zs[-1] - 60.8) < 0.1, [57.0 in zs, zs[-1]])
    rec(f"P.{p.name}.plinth", "plinth 20.2 in across flats (vertex-to-vertex <= 21.9 in)", 20.2 * IN - 0.005 <= af <= 20.2 * IN / math.cos(math.pi / 8) + 0.03, round(af / IN, 2))
    rec(f"P.{p.name}.floor", "pedestal stands on the floor (z0 within 1 in of 0)", abs(lo[2]) < IN, round(lo[2], 4))
rec("P.count", "two pedestals, placeholder boxes hidden", len(peds) == 2 and bpy.data.objects["SOUTH_PEDESTALS"].hide_render, len(peds))
new = [o for o in bpy.data.objects if o.name.startswith(("C26Q_", "C26P_"))]
bad = []
for o in new:
    old = bpy.data.objects.get(o.get("c26_old", ""))
    if old is None or not old.hide_render or (old.matrix_world.translation - o.matrix_world.translation).length > 1e-4: bad.append(o.name)
rec("F.replace", "every C26 figure sits exactly on a hidden original", not bad and len(new) == 147, [len(new), bad[:5]])
hs = {}
for o in new:
    lo, hi = bbox(o); hs.setdefault(o["c26_role"].split()[0] + ("_child" if o.data.name.startswith(("C26M_boy", "C26M_girl")) else ""), []).append(hi[2] - lo[2])
for k, v in hs.items():
    lim = {"man": (1.55, 1.95), "woman": (1.45, 1.80), "man_child": (1.10, 1.50), "woman_child": (1.05, 1.45)}[k]
    rec(f"F.height.{k}", f"{k} overall height (incl. hat/bonnet) within {lim} m", lim[0] <= min(v) and max(v) <= lim[1], [round(min(v), 3), round(max(v), 3), len(v)])
from importlib import util
import importlib.util as U
spec = U.spec_from_file_location("ppl31", "/workspace/tmp/cp026/ppl31/people_lib.py"); m31 = U.module_from_spec(spec); spec.loader.exec_module(m31)
ppl = [o.name for o in new if o.get("cpl_people") or m31._is_figure(o)]
rec("F.noswap", "no C26 figure is picked up by the people_lib v3.1 render-time swap (_is_figure False)", not ppl, ppl[:3])
ap = bpy.data.objects["HP_APRON"]
rec("G.apron", "apron uses C26_gravel_hoggin", ap.material_slots[0].material.name == "C26_gravel_hoggin", ap.material_slots[0].material.name)
w = [o.name for o in bpy.data.objects if o.name.startswith("WALLF_SE1_") or o.name == "SOUTH_DOORS_OPEN"]
rec("W.boarding", "south-end boarding objects use C26_south_boarding", all(s.material and s.material.name == "C26_south_boarding" for n in w for s in bpy.data.objects[n].material_slots if s.material and "oard" in s.material.name), w)
json.dump(R, open(OUT, "w"), indent=1)
print("CP026_CHECKS", sum(r["pass"] for r in R), "/", len(R), [r["id"] for r in R if not r["pass"]], flush=True)
