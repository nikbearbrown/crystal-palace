"""State checks (fitout / hp51 / closing) on a BUILT round: camera grammar (eye 5.25 ft over its floor, no roll,
lens grammar, >= 1 ft clearance by raycast), state contents, file size.
blender -b rounds/X.blend -P check_state.py -- --out checks/X"""
import bpy, sys, os, json, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[argv.index("--out") + 1]
FT = 0.3048; GT = 22.92
info = json.loads(bpy.context.scene.get("grok_build", "{}")); STATE = info.get("state"); SI = info.get("state_info", {})
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
        abs(fl - base) < 0.6 or (STATE == "fitout" and 84 <= p.x <= 132 and -36 <= p.y <= 36), round(fl, 2), f"{base}")
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
if STATE == "fitout":
    rec("FT.fountain", "fountain absent (FT02)", not any(n.startswith("FOUNTAIN") or n.startswith("FTN") for n in names) and "removed" in SI.get("fountain", ""), SI.get("fountain"))
    pa = SI.get("paint", {}); rec("FT.paint", "painted, half-painted and primed members all present", pa.get("painted", 0) > 0 and pa.get("half", 0) >= 4 and pa.get("primer", 0) > 0, pa)
    rec("FT.painters", "painters on ladders and cradles", SI.get("painters", 0) >= 8 and SI.get("ladders", 0) >= 2 and SI.get("cradles", 0) >= 4, [SI.get("painters"), SI.get("ladders"), SI.get("cradles")])
    rec("FT.crates", "crates/cases arriving (dray, skids, trucks, stacks)", cnt("DRAY_") >= 2 and cnt("TRUCK_") >= 4 and cnt("STACK_") >= 4, [cnt("DRAY_"), cnt("TRUCK_"), cnt("STACK_")])
    rec("FT.floor", "unboarded patch: Muse floor tiles + loose boards", SI.get("floor_tiles", 0) >= 9 and SI.get("floor", {}).get("loose_boards", 0) > 0, [SI.get("floor_tiles"), SI.get("floor")])
    rec("FT.sweep", "sweeping machine + sprinkler hand-engine present", "SWEEPER" in names and "HAND_ENGINE" in names, ["SWEEPER" in names, "HAND_ENGINE" in names])
    rec("FT.exhibits", "no exhibits installed (FT01)", not any(n.startswith("MUSE_EX") or n.startswith("EXH_") for n in names), "")
if STATE == "hp51":
    rd = SI.get("crowd_redressed", [0, 1]); rec("H.dress", "shilling-day crowd: >= 60% in working dress", rd[0] / max(1, rd[1]) >= 0.6, rd)
    rec("H.turnstiles", "turnstiles + pay boxes + police at the south entrance", cnt("TURNSTILE_") >= 4 and cnt("PAYBOX_") == 2 and cnt("POLICE_") >= 2, [cnt("TURNSTILE_"), cnt("PAYBOX_"), cnt("POLICE_")])
    rec("H.queue", "exterior queue >= 100 figures", SI.get("queue_figures", 0) >= 100, SI.get("queue_figures"))
    rec("H.stair", "visitors on the gallery stair", SI.get("stair_figures", 0) >= 4, SI.get("stair_figures"))
    rec("H.louvre", "Muse louvre compartments + attendant + rope", SI.get("louvre_compartments", 0) == 3 and "ATTEND_LOUVRE" in names and "LOUVRE_ROPE" in names, SI.get("louvre_compartments"))
    rec("H.water", "watering attendants with cans", cnt("ATTEND_WATER_") >= 3 and cnt("CAN_") >= 3, cnt("ATTEND_WATER_"))
    rec("H.doors", "south doors open", "SOUTH_DOORS_OPEN" in names and "SOUTH_DOORS" not in names, "")
if STATE == "closing":
    rec("C.dais", "dais, canopy and chair of state", all(n in names for n in ("DAIS", "DAIS_CANOPY", "CHAIR_OF_STATE")), "")
    cc = SI.get("ceremony_crowd", [0, 0]); rec("C.crowd", "ceremony crowd >= 500 floor + 150 gallery (added to the hp51 dressing)", cc[0] >= 500 and cc[1] >= 150, cc)
    rec("C.leaf", "autumn leaf tint applied", SI.get("leaf") == "autumn tint", SI.get("leaf"))
    rec("C.dais_people", "commissioners on the dais", SI.get("dais_figures", 0) >= 20, SI.get("dais_figures"))
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
