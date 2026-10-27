"""O-WORKSHOP checks on a BUILT round: camera grammar (eye 5.25 ft over its floor, no roll,
lens grammar, >= 1 ft clearance by raycast), state contents, file size.
blender -b rounds/X.blend -P check_state.py -- --out checks/X"""
import bpy, sys, os, json, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[argv.index("--out") + 1]
FT = 0.3048; GT = 22.92
info = json.loads(bpy.context.scene.get("grok_build", "{}")); STATE = "workshop"; SI = info.get("info", {})
route = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "route", "camera_route.json")))
res = []
def rec(id_, what, ok, measured, target=""):
    res.append({"id": id_, "check": what, "target": target, "measured": measured, "pass": bool(ok)})
dg = bpy.context.evaluated_depsgraph_get(); sc = bpy.context.scene
cams = [o for o in bpy.data.objects if o.type == 'CAMERA']
lens_ok = {"interior": 28, "approach": 35, "detail": 50}
for c in cams:
    sid = c.name.rsplit("_", 1)[0]; shot = next(s for s in route["shots"] if s["id"] == sid)
    p = c.matrix_world.translation / FT
    # floor under the camera: ray straight down (ignores figures / props below 0.5 ft thick by taking the first hit)
    hit, loc, *_ = sc.ray_cast(dg, c.matrix_world.translation, Vector((0, 0, -1)), distance=40)
    fl = loc.z / FT if hit else 0.0
    base = GT if p.z > 20 else 0.0
    rec(f"{c.name}.eye", "eye height over its floor plane (gallery 22.92 / floor 0)", abs(p.z - base - 5.25) < 0.05, round(p.z - base, 3), "5.25 ft")
    rec(f"{c.name}.floorhit", "surface below the eye within 0.6 ft of that floor plane (unboarded patch: joists/earth allowed)",
        abs(fl - base) < 0.6, round(fl, 2), f"{base}")
    xax = c.matrix_world.to_3x3() @ Vector((1, 0, 0))
    rec(f"{c.name}.roll", "no roll (camera x-axis horizontal)", abs(xax.z) < 1e-4, round(xax.z, 6), "0")
    rec(f"{c.name}.lens", "lens in grammar (28 interior / 35 approach / 50 detail)", c.data.lens in (28, 35, 50) and c.data.lens == shot["lens_mm"], c.data.lens, shot["lens_mm"])
    dmin = 99.0
    for i in range(-2, 3):
        for j in range(16):
            el = i * math.pi / 5; az = j * math.pi / 8
            d = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)))
            h, l2, *_ = sc.ray_cast(dg, c.matrix_world.translation, d, distance=3.0)
            if h: dmin = min(dmin, (l2 - c.matrix_world.translation).length / FT)
    for d in (Vector((0, 0, 1)), Vector((0, 0, -1))):
        h, l2, *_ = sc.ray_cast(dg, c.matrix_world.translation, d, distance=3.0)
        if h: dmin = min(dmin, (l2 - c.matrix_world.translation).length / FT)
    rec(f"{c.name}.clear", "clearance to nearest mesh (82-ray sphere)", dmin >= 1.0, round(dmin, 2), ">= 1 ft")
names = set(o.name for o in bpy.data.objects)
cnt = lambda pre: sum(1 for n in names if n.startswith(pre))
rec("W.machines", "sash-bar machines (2) + gutter machine + line shaft + engine", cnt("MACHINE_SASHBAR") >= 2 and cnt("MACHINE_GUTTER") >= 1 and any("SHAFT" in n for n in names) and any("ENGINE" in n for n in names), [cnt("MACHINE_SASHBAR"), cnt("MACHINE_GUTTER")])
rec("W.bars", "stacked sash bars >= 200", SI.get("sash_bars_stacked", 0) >= 200, SI.get("sash_bars_stacked"))
rec("W.glass", "glass furnace + cylinders >= 50 + flattening kiln", cnt("GLASSHOUSE") >= 1 and cnt("WS_Glory") >= 3 and SI.get("cylinders", 0) >= 50 and cnt("WS_Kiln") >= 1, SI.get("cylinders"))
rec("W.wagon", "parts on railway wagons: girder + columns", SI.get("girders", 0) >= 1 and SI.get("columns_on_wagons", 0) >= 3 and cnt("SIDING_WAGONS") >= 1, [SI.get("girders"), SI.get("columns_on_wagons"), cnt("SIDING_WAGONS")])
rec("W.figures", "workers >= 15", SI.get("figures", 0) >= 15, SI.get("figures"))
mb = os.path.getsize(bpy.data.filepath) / 1e6
rec("FILE.size", "round .blend under 90 MB", mb < 90, round(mb, 1), "< 90 MB")
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
json.dump({"state": STATE, "checks": res}, open(OUT + "_state.json", "w"), indent=1)
with open(OUT + "_state.md", "w") as f:
    f.write(f"# state checks: {STATE} -- {sum(r['pass'] for r in res)}/{len(res)} pass\n\n| id | check | target | measured | pass |\n|---|---|---|---|---|\n")
    for r in res: f.write(f"| {r['id']} | {r['check']} | {r['target']} | {r['measured']} | {'PASS' if r['pass'] else '**FAIL**'} |\n")
print("STATECHECK", STATE, sum(r['pass'] for r in res), "/", len(res))
for r in res:
    if not r["pass"]: print("FAIL", r)
