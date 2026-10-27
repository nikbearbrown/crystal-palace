"""Generic set checks on a BUILT round: camera grammar (eye 5.25 ft over the surface it stands on, unless the shot is
flagged "diagram"; no roll; lens == route and in the 28/35/50 grammar; >= 1 ft clearance by 82-ray sphere), contents from
route["contents"] ([{"id","what","prefix"|"info","min"}]) and file size < 90 MB.
blender -b rounds/X.blend -P check_set.py -- --out checks/X"""
import bpy, sys, os, json, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]; OUT = argv[argv.index("--out") + 1]
FT = 0.3048; sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get()
info = json.loads(sc.get("grok_build", "{}")); SI = info.get("info", {})
RP = argv[argv.index("--route") + 1] if "--route" in argv else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "route", "camera_route.json")
route = json.load(open(RP))
units_m = route.get("units") == "m"; EYE = 1.6 if units_m else 5.25; CLR = 1.0 if not units_m else 1.0  # clearance still in ft via /FT below; for m use metres
EU = 1.0 if units_m else FT  # divide world metres by EU to get eye units
res = []
def rec(i, w, ok, m, t=""): res.append({"id": i, "check": w, "target": t, "measured": m, "pass": bool(ok)})
ppl = {o.name for o in bpy.data.objects if o.get("person")}
def cast(p, d, dist):
    q = p.copy()
    for _ in range(6):   # skip hits on figures (eye height is over the ground / deck, not over a head)
        h, l, n, i, o, m = sc.ray_cast(dg, q, d, distance=dist)
        if not h: return None, None
        if o.name not in ppl or d.z > -0.5: return l, o
        q = l + d * 0.01
    return None, None
for c in [o for o in bpy.data.objects if o.type == 'CAMERA']:
    sid = c.name.rsplit("_", 1)[0]; shot = next(s for s in route["shots"] if s["id"] == sid); P = c.matrix_world.translation
    diag = shot.get("diagram", False)
    if not diag:
        l, o = cast(P, Vector((0, 0, -1)), 400)
        eye = (P.z - l.z) / EU if l is not None else None
        rec(f"{c.name}.eye", f"eye {EYE} over the surface below ({o.name if o else '-'})", eye is not None and abs(eye - EYE) < (0.08 if units_m else 0.1), round(eye, 3) if eye else None, f"{EYE} m" if units_m else "5.25 ft")
        xax = c.matrix_world.to_3x3() @ Vector((1, 0, 0)); rec(f"{c.name}.roll", "no roll", abs(xax.z) < 1e-4, round(xax.z, 6), "0")
        rec(f"{c.name}.lens", "lens in grammar (28 interior / 35 approach / 50 detail) and = route", c.data.lens in (28, 35, 50) and c.data.lens == shot["lens_mm"], c.data.lens, shot["lens_mm"])
        dmin = 99.0
        for i in range(-2, 3):
            for j in range(16):
                el = i * math.pi / 5; az = j * math.pi / 8; d = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)))
                h, l2, *_ = sc.ray_cast(dg, P, d, distance=3.0)
                if h: dmin = min(dmin, (l2 - P).length / FT)
        for d in (Vector((0, 0, 1)), Vector((0, 0, -1))):
            h, l2, *_ = sc.ray_cast(dg, P, d, distance=3.0)
            if h: dmin = min(dmin, (l2 - P).length / FT)
        rec(f"{c.name}.clear", "clearance to nearest mesh (82-ray sphere)", dmin >= 1.0, round(dmin, 2), ">= 1 ft")
    else:
        rec(f"{c.name}.diagram", "diagram camera (labelled cutaway; eye grammar n/a), no roll", abs((c.matrix_world.to_3x3() @ Vector((1, 0, 0))).z) < 1e-4, c.data.type, "")
names = [o.name for o in bpy.data.objects]
for k in route.get("contents", []):
    if "prefix" in k: v = sum(1 for n in names if n.startswith(k["prefix"]))
    else:
        v = SI
        for part in k["info"].split("."): v = v.get(part, 0) if isinstance(v, dict) else 0
    rec(k["id"], k["what"], (v if isinstance(v, (int, float)) else 0) >= k["min"], v, f">= {k['min']}")
mb = os.path.getsize(bpy.data.filepath) / 1e6; rec("FILE.size", "round .blend under 90 MB", mb < 90, round(mb, 1), "< 90 MB")
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
json.dump({"set": info.get("set"), "checks": res}, open(OUT + "_checks.json", "w"), indent=1)
with open(OUT + "_checks.md", "w") as f:
    f.write(f"# checks: {info.get('set')} -- {sum(r['pass'] for r in res)}/{len(res)} pass\n\n| id | check | target | measured | pass |\n|---|---|---|---|---|\n")
    for r in res: f.write(f"| {r['id']} | {r['check']} | {r['target']} | {r['measured']} | {'PASS' if r['pass'] else '**FAIL**'} |\n")
print("SETCHECK", info.get("set"), sum(r['pass'] for r in res), "/", len(res))
for r in res:
    if not r["pass"]: print("FAIL", r)
