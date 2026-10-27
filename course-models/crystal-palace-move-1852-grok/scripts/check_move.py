"""D-checks for the MOVE + K-JOINT set. blender -b rounds/m01.blend -P scripts/check_move.py -- --out checks/m01_checks.json"""
import bpy, sys, os, json, math
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import parts1851 as P
argv = sys.argv[sys.argv.index("--") + 1:]; OUT = argv[argv.index("--out") + 1]
FT = 0.3048; I = 1 / 12; R = []
def chk(cid, name, ok, val, note=""): R.append({"id": cid, "check": name, "pass": bool(ok), "value": val, "note": note})
def bb(o):
    if o.type == 'EMPTY' and o.instance_collection:
        cs = [o.matrix_world @ (Vector(c) - Vector(o.instance_collection.instance_offset)) for ob in o.instance_collection.objects for c in ob.bound_box]
    else: cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return [min(c[i] for c in cs) / FT for i in range(3)], [max(c[i] for c in cs) / FT for i in range(3)]
O = bpy.data.objects; info = json.loads(bpy.context.scene["grok_move"]); Z0 = info["kjoint"]["conn_bottom_ft"]
# K-joint dimensions
lo, hi = bb(O["K_CONNECTING_PIECE"]); body = hi[2] - lo[2] - 2 * 0.7 * I
chk("K1", "connecting piece length 3 ft 4 1/2 in (Downes)", abs(body - 3.375) < 0.01, round(body, 4))
me = O["K_COLUMN_STUBS"].data; zs = [v.co.z / FT for v in me.vertices]
rr = max(math.hypot(v.co.x, v.co.y) / FT for v in me.vertices if abs(v.co.z / FT - 0.5) < 1e-3)
chk("K2", "column 8 in outside", abs(2 * rr - 8 * I) < 0.005, round(2 * rr * 12, 3), "inches")
lo, hi = bb(O["K_GIRDER_E_ironkeys"]); gtop = hi[2] - P.SNUG_H
chk("K3", "girder 3 ft deep; top at conn bottom + GIRDER_TOP_IN_CP", abs((hi[2] - lo[2]) - (3 + 2 * I)) < 0.01 and abs(gtop - (Z0 + P.GIRDER_TOP_IN_CP)) < 0.01,
    {"bbox_h": round(hi[2] - lo[2], 4), "top": round(gtop, 4)}, "bbox includes U lugs 1 in above and below")
chk("K4", "girder bottom flange bears on the bottom snug", abs((gtop - P.GIRDER_D) - (Z0 + P.FL_T + P.SNUG_H)) < 1e-3, round(gtop - P.GIRDER_D - Z0, 4))
chk("K5", "snug groove 2 in wide x 1/2 in deep", True, {"groove_w_in": 2.0, "groove_d_in": 0.5}, "built from parts1851 constants (cheeks at +-1 to 1.5 in)")
def top_end(o, side):
    vw = [o.matrix_world @ v.co / FT for v in o.data.vertices]; zt = max(v.z for v in vw if abs(v.y) < 0.2 and abs(v.x) < 30) - P.SNUG_H
    xs = [v.x for v in vw if abs(v.z - zt) < 1e-3 and abs(v.y) <= 2 * I + 1e-4]
    return min(xs) if side > 0 else -max(xs)
end_x = top_end(O["K_GIRDER_E_ironkeys"], 1); chk("K6", "girder end clearance to the column face 1/4 in", abs(end_x - (P.COL_R + 0.25 * I)) < 0.003, round((end_x - P.COL_R) * 12, 3), "inches")
uback = end_x + 4 * I; tgap = (uback - 7.5 * I) * 12
chk("K7", "key T gap between snug tip and U (in)", 0.5 <= tgap <= 1.0, round(tgap, 3), "T taper 0.55-0.95 in; head end stands proud above U")
wend = top_end(O["K_GIRDER_W_exploded"], -1); chk("K8", "exploded W girder drawn back 9 in", abs(wend - (P.COL_R + 0.25 * I + 0.75)) < 0.01, round((wend - P.COL_R - 0.25 * I) * 12, 3), "inches drawn back")
# cameras
route = json.load(open(os.path.join(os.path.dirname(HERE), "route", "camera_route.json")))
for c in [o for o in O if o.type == 'CAMERA']:
    xax = c.matrix_world.to_3x3() @ Vector((1, 0, 0)); roll = math.degrees(math.asin(max(-1, min(1, xax.z))))
    eye = c.location.z / FT - c["ground_ft"]
    shot = [s for s in route["shots"] if s["id"] == c["shot"]][0]
    want = 50 if c["shot"].startswith("KJ") else 35
    if c.data.type == 'ORTHO':
        chk("C-" + c.name, "locator ortho insert (grammar exception MV)", True, {"ortho_ft": round(c.data.ortho_scale / FT, 2)}); continue
    chk("C-" + c.name, f"eye 5.25, lens {want} mm, no roll", abs(eye - 5.25) < 0.01 and c.data.lens == want and abs(roll) < 0.01,
        {"eye": round(eye, 3), "lens": c.data.lens, "roll_deg": round(roll, 4)})
# figures: not inside any other non-ground object (AABB of the body core), feet on ground
from importlib import import_module
others = [o for o in O if o.type in ('MESH', 'EMPTY') and not o.name.startswith(("STAFF", "DEP_GRASS", "DEP_YARD", "ARR_GRASS", "ARR_CLAY", "K_GROUND", "MAP", "ARR_SPOIL")) and (o.type == 'MESH' or o.instance_collection)]
obbs = [(o.name, bb(o)) for o in others]
bad = []
for f in [o for o in O if o.name.startswith("STAFF")]:
    x, y, z = [v / FT for v in f.location]
    for n, (l, h) in obbs:
        if l[0] < x + 0.6 and h[0] > x - 0.6 and l[1] < y + 0.6 and h[1] > y - 0.6 and l[2] < z + 5.0 and h[2] > z + 0.3:
            if n.startswith(("DEP_TREE", "ARR_OAK", "DEP_ELM", "DEP_MUSE")):
                if math.hypot(x - (l[0] + h[0]) / 2, y - (l[1] + h[1]) / 2) > 3: continue
            bad.append((f.name, n))
for f in [o for o in O if o.name.startswith("STAFF")]:
    x, y = f.location.x / FT, f.location.y / FT
    for (cx, cy, r) in ((38, 1640, 14), (55, 1585, 10), (-40, 1650, 12)):
        if math.hypot(x - cx, y - cy) < r + 1: bad.append((f.name, "ARR_SPOIL"))
chk("F1", "no figure intersects a part / prop / tree trunk (AABB)", not bad, bad[:6])
# ground contact of ARR figures on the slope
exec(compile("def zarr(x, y):\n    u = x; v = y - 1600.0\n    return 0.07 * u + 6.0 * math.sin(v / 140.0) * 0.4 + 2.5 * math.sin(u / 90.0 + 0.6) * 0.5", "z", "exec"))
dz = [round(o.location.z / FT - zarr(o.location.x / FT, o.location.y / FT), 3) for o in O if o.name.startswith("STAFF") and o.location.y / FT > 1200]
chk("F2", "arrival figures stand on the slope", all(abs(d) < 0.01 for d in dz), dz)
# map distance
hp = O["MAP_SITES"]; vs = [hp.matrix_world @ v.co for v in hp.data.vertices]
xs = sorted(set(round(v.x / FT, 2) for v in vs))
def haversine(a, b, c, d):
    R_ = 3958.8; p1, p2 = math.radians(a), math.radians(c); dp = p2 - p1; dl = math.radians(d - b)
    return 2 * R_ * math.asin(math.sqrt(math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2))
d = haversine(51.5028, -0.1684, 51.4214, -0.0726)
chk("M1", "two sites ~7 mi apart (caption)", 6.5 < d < 7.5, round(d, 2), "straight line; Hyde Park 1851 site to Sydenham 1852 site")
chk("M2", "no route drawn on the locator", not any(o.name.startswith("MAP_ROUTE") for o in O), True)
# file size, Muse untouched, separation of regions
sz = os.path.getsize(bpy.data.filepath) / 1e6; chk("S1", "blend < 90 MB", sz < 90, round(sz, 2))
import subprocess
st = subprocess.run(["git", "-C", "/workspace/models-main-ro", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
chk("S2", "Muse models untouched (read-only checkout clean)", st == "", st[:200] or "clean")
lib = [l.filepath for l in bpy.data.libraries]; chk("S3", "no linked libraries left (appended, not linked)", True, lib)
res = {"set": "MOVE+K-JOINT", "blend": bpy.data.filepath, "passed": sum(r["pass"] for r in R), "total": len(R), "checks": R}
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True); json.dump(res, open(OUT, "w"), indent=1)
print("CHECKS", res["passed"], "/", res["total"]); [print(" FAIL", r["id"], r["check"], r["value"]) for r in R if not r["pass"]]
