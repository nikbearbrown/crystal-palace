"""Measure the exterior D-checks on the BUILT model (and its fit to Claude's frame and Grok's transept).
blender -b rounds/xNN.blend -P check_dims.py -- --out checks/xNN [--claude claude.blend] [--transept transept.blend]
Writes checks/xNN/checks.json and checks.md"""
import bpy, sys, os, json, math
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
OUT = arg("--out"); FT = 0.3048
objs = bpy.data.objects
def wverts(ob): return [ob.matrix_world @ v.co for v in ob.data.vertices]
def bbox(obs):
    vs = [v for o in obs for v in wverts(o)]
    return [min(v[i] for v in vs) / FT for i in range(3)], [max(v[i] for v in vs) / FT for i in range(3)]
res = []
def rec(id_, what, target, tol, measured, unit="ft", src=""):
    res.append({"id": id_, "check": what, "target": round(target, 4), "tolerance": tol, "measured": round(measured, 4),
                "unit": unit, "pass": abs(measured - target) <= tol, "source": src})
walls = [o for o in objs if o.get("part_kind") == "wall"]
def wall_tag(prefix): return [o for o in walls if str(o.get("tag", "")).startswith(prefix)]
lo, hi = bbox(wall_tag("E1") + wall_tag("W1"))
rec("D01", "building length, end wall to end wall (column centrelines)", 1848.0, 1.0, (hi[0] + lo[0] * -1) - 0.5, src="Downes D01, Plate I/IV: 1848 ft")
for k, tgt, did in ((1, 408, "D02a"), (2, 264, "D02b"), (3, 120, "D02c")):
    ws = wall_tag(f"S{k}_") + wall_tag(f"N{k}_")
    ys = sorted(set(round(o.location.y / FT, 2) for o in ws))
    rec(did, f"tier-{k} width between its outer side walls", tgt, 0.5, ys[-1] - ys[0], src="Downes D02 / Plate III: 408 / 264 / 120 ft")
    xs = [o.location.x / FT for o in ws]
    rec(did + "L", f"tier-{k} side walls reach the end walls (x extent of wall-bay centres + 24)", 1848.0, 1.0, max(xs) - min(xs) + 24, src="tiers all 1848 ft long")
lo, hi = bbox(wall_tag("NS1"))
rec("D05a", "north strip length (x extent of its north wall)", 936.0, 1.0, hi[0] - lo[0], src="CONTROL-DIMENSIONS D05")
ns = [o for o in walls if str(o.get("tag")) in ("NSW", "NSE")]
lo2, hi2 = bbox(ns)
rec("D05b", "north strip depth beyond the 408 ft block", 48.0, 0.6, hi2[1] - 204.0, src="D05: 48 ft")
rec("D05c", "north strip start x (216 ft west of the transept centre-line chain)", -708.0, 0.6, lo[0], src="north chain 216 + 936 + 696")
# frame
cols = [o for o in objs if o.get("part_kind") == "column"]
off = max(max(abs((o.location.x / FT + 924) / 24 - round((o.location.x / FT + 924) / 24)),
              abs((o.location.y / FT + 204) / 24 - round((o.location.y / FT + 204) / 24))) for o in cols) * 24
rec("G01", "every column on Claude's 24 ft grid (max off-grid, ft)", 0.0, 0.01, off, src="x=-924+24i, y=-204+24j")
rec("G02", "no exterior column west of line 40 except the north strip", 0, 0, sum(1 for o in cols if o.location.x / FT < 35 and o.get("half") != "north_strip"), unit="count", src="complementary to Claude (x <= -36)")
pos = {(round(o.location.x / FT), round(o.location.y / FT)) for o in cols}
rec("G03", "no duplicate column positions", len(cols), 0, len(pos), unit="count", src="")
rec("G04", "no column inside the 72 ft nave (|y| < 36)", 0, 0, sum(1 for o in cols if abs(o.location.y / FT) < 35), unit="count", src="Plate VI; EX02")
for k, tgt, did in ((1, 22 + 2/12, "D11a"), (2, 42 + 2/12, "D11b"), (3, 62 + 2/12, "D11c")):
    g = [o for o in objs if o.get("part_kind") == "girder" and o.get("tier") == k][:30]
    rec(did, f"tier-{k} girder top", tgt, 0.05, max(max(v.z for v in wverts(o)) for o in g) / FT, src="controls D11")
g = [o for o in objs if o.name == "EGAL_FLOORS"][0]
rec("D12", "east gallery floor top", 22 + 11/12, 0.05, max(v.z for v in wverts(g)) / FT, src="controls D12")
fill = [o for o in objs if o.get("part_kind") == "wall" and abs(o.rotation_euler.z) < 0.1][0]
lv = [((v.x - fill.location.x) / FT, (v.z - fill.location.z) / FT) for v in wverts(fill)]
top = max(z for _, z in lv)
bot = {round(x, 2) for x, z in lv if abs(z) < 1e-3 and abs(abs(x) - 12) > 0.01}
tp = {round(x, 2) for x, z in lv if abs(z - top) < 1e-3 and abs(abs(x) - 12) > 0.01}
rec("W01", "full-height posts per 24 ft wall bay (iron-column ends + 2 timber posts at 8 ft, Plate XXI)", 4, 0, len(bot & tp) // 2, unit="posts", src="Plate XXI")
ends = wall_tag("E1") + wall_tag("E2") + wall_tag("E3")
lv3 = [o for o in objs if o.name.startswith("ELOUV_E3_")]
rec("E01", "east end wall incl. top louvre band reaches the tier-3 girder underside", 62 + 2/12 - 3, 0.6, max(max(v.z for v in wverts(o)) for o in ends + lv3) / FT + 0.0, src="Plate V")
rec("E02", "east end doorways (centre 3, the bays at y=+-120, the outer 2; Plate V)", 7, 0, sum(1 for o in objs if o.get("part_kind") == "door" and o.location.x > 0), unit="count", src="Plate V")
st = sum(1 for o in objs if o.name.startswith("ESTLAND_"))
rec("S01", "east-half avenue staircases (mirrors of Claude's stair bays 8/17/26, N and S)", 6, 0, st, unit="count", src="Plate II; Claude STAIR_BAYS")
# cameras: no roll, eye height on storyboard (non-REF / non-ortho) shots
for c in [o for o in objs if o.type == 'CAMERA']:
    rec("C_" + c.name, "camera: no roll (deg) + eye-height error (cm) unless review/ortho", 0.0, 0.5,
        abs(math.degrees(c.matrix_world.to_euler('XYZ').y)) + (0 if c.name.startswith(("REF_", "PLATE_")) else abs(c.location.z - 1.6) * 100), unit="deg+cm", src="storyboard v001")
os.makedirs(OUT, exist_ok=True)
json.dump(res, open(os.path.join(OUT, "checks.json"), "w"), indent=1)
with open(os.path.join(OUT, "checks.md"), "w") as f:
    n = sum(r["pass"] for r in res); f.write(f"# Exterior checks {os.path.basename(OUT)}: {n}/{len(res)} pass\n\n| id | check | target | measured | tol | pass | source |\n|---|---|---|---|---|---|---|\n")
    for r in res: f.write(f"| {r['id']} | {r['check']} | {r['target']} | {r['measured']} | {r['tolerance']} | {'PASS' if r['pass'] else 'FAIL'} | {r['source']} |\n")
print("CHECKS", sum(r["pass"] for r in res), "/", len(res))
for r in res:
    if not r["pass"]: print("FAIL", r)
