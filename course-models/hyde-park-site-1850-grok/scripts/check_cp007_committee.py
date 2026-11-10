"""Dimension checks for the CP007 committee CANDIDATE (run on rounds/candidates/s02_cp007committee.blend).
Measures W7_MODEL_BUILDING in plan feet (local coords; object scale = 1:600) against the 1851 text values."""
import bpy, json, math, os, sys
o = bpy.data.objects["W7_MODEL_BUILDING"]; me = o.data; K = o.scale[0]
V = [v.co for v in me.vertices]
def rng(f, axis):
    s = [v[axis] for v in V if f(v)]; return (min(s), max(s)) if s else (None, None)
res = []
def chk(name, val, lo, hi, src):
    ok = val is not None and lo <= val <= hi; res.append({"check": name, "value": round(val, 2) if val is not None else None, "range": [lo, hi], "pass": ok, "source": src}); print("CHECK", "PASS" if ok else "FAIL", name, round(val, 2) if val is not None else None, [lo, hi])
body = lambda v: -0.1 < v.z < 31 and -0.5 <= v.y <= 420 and -0.1 <= v.x <= 2200.1      # walls/sheds only (no pavilion/pent projections)
u0, u1 = rng(body, 0); chk("length between end walls (ft)", u1 - u0, 2150, 2250, "about 2,200 ft (Bogue 1851)")
v0, v1 = rng(lambda v: -0.1 < v.z < 33 and -0.1 <= v.y, 1); chk("body width incl. north pavilion (ft)", v1 - v0, 400, 450, "greatest width nearly 450 ft incl. projections")
w0, w1 = rng(lambda v: v.z < 100, 1); chk("greatest width incl. pavilions/pent roof (ft)", w1 - w0, 420, 470, "nearly 450 ft")
top = max(v.z for v in V); chk("dome top incl. lantern (ft)", top, 160, 175, "cupola more than 160 ft")
drum = [v for v in V if abs(math.hypot(v.x - 1000, v.y - 144) - 100) < 2.5 and v.z <= 60.5]
chk("drum height (ft)", max(v.z for v in drum), 57, 61, "drum about 60 ft")
ring = [math.hypot(v.x - 1000, v.y - 144) for v in V if 59 < v.z < 61]
chk("rotunda diameter at drum top (ft)", 2 * max(r for r in ring if r < 101), 196, 204, "200 ft")
main = [v.z for v in V if 118 <= v.y <= 170 and (100 < v.x < 880 or 1120 < v.x < 2100) and v.z < 60]
chk("main avenue crown incl. 0.9 ft rib bands (ft)", max(main), 51, 54, "52 ft")
side = [v.z for v in V if 15 < v.y < 119 and 100 < v.x < 880 and 31 < v.z < 45]
chk("side avenue ridge incl. skylight (ft)", max(side), 35, 38, "36 ft")
li = [m.name for m in me.materials].index("W7_ModelDomeIron")
gap = min(V[i].z for p in me.polygons if p.material_index == li for i in p.vertices) - max(v.z for v in drum)
chk("dome shell spring minus drum top (ft) [live model: dome floated above its drum]", gap, -1.0, 0.5, "dome rests on the drum")
chk("model scale denominator", 0.3048 / K, 599.5, 600.5, "SD43 1:600")
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "checks", "cp007_committee_checks.json")
json.dump({"date": "2026-11-10", "state": "Hyde Park spring 1850 (Building Committee design, June 1850)", "checks": res,
           "passed": sum(r["pass"] for r in res), "total": len(res)}, open(out, "w"), indent=1)
print("CHECKS", sum(r["pass"] for r in res), "/", len(res))
