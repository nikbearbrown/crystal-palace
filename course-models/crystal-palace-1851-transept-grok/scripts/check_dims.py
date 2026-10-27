"""Measure the D-checks (Downes controls.json) and transept checks on the BUILT model. Writes checks/<round>.json and .md
blender -b rounds/rNN.blend -P check_dims.py -- --out checks/rNN"""
import bpy, sys, os, json, math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[argv.index("--out") + 1]
FT = 0.3048
dg = bpy.context.evaluated_depsgraph_get()
def wverts(ob): return [ob.matrix_world @ v.co for v in ob.data.vertices]
def ext(ob):
    vs = wverts(ob); return [ (max(v[i] for v in vs) - min(v[i] for v in vs)) / FT for i in range(3)], vs
res = []
def rec(id_, what, target, tol, measured, unit="ft", src="", rel=False):
    lim = target * tol if rel else tol
    ok = abs(measured - target) <= lim
    res.append({"id": id_, "check": what, "target": round(target, 4), "tolerance": (f"{tol*100:.2f}%" if rel else tol),
                "measured": round(measured, 4), "unit": unit, "pass": ok, "source": src})
objs = bpy.data.objects
# D19 72 ft truss
t = objs["TRUSS72_strong_X-036"]; e, _ = ext(t)
rec("D19a", "72 ft truss, face-to-face extent across the nave (Y)", 71.2, 0.4, e[1], src="controls.json D19a, Plate XX")
rec("D19b", "72 ft truss depth (Z)", 6.0, 0.1, e[2], src="controls.json D19b, Plate XX")
# D20/D21 rib
rib = objs["RIB_A_Y+00012"]; e, vs = ext(rib)
rec("D20", "main rib A extrados diameter (X extent)", 74 + 4/12, 0.007, e[0], src="controls.json D20, p. 50", rel=True)
zc = rib.location.z
rs = [math.hypot(v.x - rib.location.x, v.z - zc) / FT for v in vs]
rec("D21", "main rib A radius (extrados, the 37 ft the ribs are 'cut to')", 37.0, 0.007, max(rs), src="p. 50, D21", rel=True)
rec("D21i", "main rib A depth (extrados - intrados)", 1.5, 0.02, max(rs) - min(rs), src="p. 50: 1 ft 6 in")
rec("T01", "vault crown (rib extrados top) above floor", 102 + 2/12, 1.0, max(v.z for v in vs) / FT, src="1856 guide: transept height 102 ft 2 in")
ribs = [o for o in objs if o.get("part_kind") in ("vault_rib", "vault_rib_b")]
ys = sorted(o.location.y / FT for o in ribs)
rec("T02", "transept (vault) length, end rib to end rib", 408.0, 0.5, ys[-1] - ys[0], src="Plate II/III, 408 ft main block")
A = sorted(o.location.y / FT for o in ribs if o["rib"] == "A")
rec("T05", "main rib A pitch (on the 24 ft columns)", 24.0, 0.01, max(b - a for a, b in zip(A, A[1:])), src="p. 36")
rec("T06", "main ribs carried on the strong 72 ft trusses at y = +-12 ft", 2, 0, sum(1 for o in ribs if o.get("on_truss")), unit="count", src="p. 36")
# grid
cols = [o for o in objs if o.get("part_kind") == "column"]
xs = sorted(set(round(o.location.x / FT, 3) for o in cols if not o.name.startswith(("COL_END", "COL_XGAL"))))
yy = sorted(set(round(o.location.y / FT, 3) for o in cols if not o.name.startswith(("COL_END", "COL_XGAL"))))
off = max(max(abs((x + 924) / 24 - round((x + 924) / 24)) for x in xs), max(abs((y + 204) / 24 - round((y + 204) / 24)) for y in yy)) * 24
rec("G01", "columns on Claude's 24 ft grid (max off-grid error)", 0.0, 0.01, off, src="Claude frame: x=-924+24i, y=-204+24j")
rec("G02", "transept clear width between column lines", 72.0, 0.01, min(x for x in xs if x > 0) - max(x for x in xs if x < 0), src="Plate II")
# girder tops by tier
for k, tgt, did in ((1, 22 + 2/12, "D11a"), (2, 42 + 2/12, "D11b"), (3, 62 + 2/12, "D11c")):
    g = [o for o in objs if o.get("part_kind") == "girder" and o.get("tier") == k]
    tops = [max(v.z for v in wverts(o)) / FT for o in g[:20]]
    rec(did, f"tier-{k} girder top", tgt, 0.05, max(tops), src="controls.json " + did)
gal = objs["GAL_CROSS_S"]; gv = wverts(gal)
rec("D12", "gallery floor top", 22 + 11/12, 0.05, max(v.z for v in gv) / FT, src="controls.json D12")
rec("T03", "south cross gallery depth (Plate II '48.0')", 48.0, 0.1, (max(v.y for v in gv) - min(v.y for v in gv)) / FT, src="Plate II")
gn = wverts(objs["GAL_CROSS_N"])
rec("T04", "north cross gallery depth", 24.0, 0.1, (max(v.y for v in gn) - min(v.y for v in gn)) / FT, src="Plate II")
c = objs["COL_X-036_Y-060"]; cv = wverts(c)
rad = [math.hypot(v.x - c.location.x, v.y - c.location.y) for v in cv if 2 * FT < v.z < 22 * FT]
rec("D13", "column outside diameter (shaft)", 8.0, 0.1, 2 * min(rad) / FT * 12, unit="in", src="controls.json D13")
cp = [v for v in cv if abs(abs(v.x - c.location.x) - 5.5 / 12 * FT) < 1e-4]
rec("D14", "column shaft top (bottom of the first connecting piece)", 18 + 11.75/12, 0.05, min(v.z for v in cp) / FT, src="controls.json D14")
# elm clearances
SPRING = 65.0; RI = 37 + 2/12 - 1.5
def clear_vault(v):
    x, z = v.x / FT, v.z / FT
    if z <= SPRING: return 36.0 - abs(x)
    return RI - math.hypot(x, z - SPRING)
worst = {}
for o in objs:
    if o.get("part_kind") in ("elm_leaves", "elm_wood"):
        vs = wverts(o)
        worst[o.name] = min(min(clear_vault(v) for v in vs), min(GT for GT in [22.9167] ) if False else 1e9)
        ht = max(v.z for v in vs) / FT
        worst[o.name] = (min(clear_vault(v) for v in vs), ht)
for n, (cl, ht) in worst.items():
    rec("E01_" + n, f"{n}: min clearance to vault intrados / 72 ft column lines (>= 3 ft)", 3.0, 0, min(cl, 3.0) if cl >= 3 else cl, src="CP017: canopy and roof clearance established")
    res[-1]["measured_clearance_ft"] = round(cl, 2); res[-1]["top_ft"] = round(ht, 1); res[-1]["pass"] = cl >= 3.0
# cameras: eye height, no roll, branch clearance
trees = []
for o in objs:
    if o.get("part_kind") in ("elm_leaves", "elm_wood"):
        me = o.evaluated_get(dg).to_mesh()
        trees.append(BVHTree.FromPolygons([o.matrix_world @ v.co for v in me.vertices], [p.vertices[:] for p in me.polygons]))
route = json.load(open(os.path.join(os.path.dirname(bpy.data.filepath), "..", "route", "camera_route.json")))
for cam in [o for o in objs if o.type == 'CAMERA']:
    p = cam.matrix_world.translation
    d = min((t.find_nearest(p)[3] for t in trees if t.find_nearest(p)[0] is not None), default=1e9) / FT
    xa = cam.matrix_world.to_3x3().col[0]; roll = abs(math.asin(max(-1, min(1, xa.z))))
    walk = cam.name.startswith(("CP0", "REV_int", "REF_elm"))
    ok = d >= 1.0 and roll < 1e-3 and (not walk or abs(p.z - 1.6) < 0.01)
    res.append({"id": "CAM_" + cam.name, "check": "camera: >=1 ft from any branch/leaf, no roll, eye 1.6 m on walks",
                "measured": {"branch_clearance_ft": round(d, 2), "roll_rad": round(roll, 5), "z_m": round(p.z, 3)}, "pass": ok})
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(res, open(OUT + ".json", "w"), indent=1)
with open(OUT + ".md", "w") as f:
    f.write("| id | check | target | tol | measured | pass |\n|---|---|---|---|---|---|\n")
    for r in res:
        f.write(f"| {r['id']} | {r['check']} | {r.get('target','')} | {r.get('tolerance','')} | {r['measured']} | {'PASS' if r['pass'] else 'FAIL'} |\n")
print("CHECKS", sum(r["pass"] for r in res), "/", len(res))
for r in res:
    if not r["pass"]: print("FAIL", r)
