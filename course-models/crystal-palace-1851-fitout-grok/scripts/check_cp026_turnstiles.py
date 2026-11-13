"""Checks for the CP026 turnstiles CANDIDATE (2026-11-13, FT95-FT100): measures the new C26T_* entrance frame, louvre band and
tree row against the sources and the live h03 parts they must match, plus staging (no figure in a post, nothing hidden, nothing
outside the wall plane) and a live-vs-candidate object accounting (only C26T_* objects added, no existing object changed).
blender -b rounds/candidates/h03_cp026turnstiles.blend -P scripts/check_cp026_turnstiles.py -- --out checks/cp026_turnstiles_checks.json --live rounds/h03.blend"""
import bpy, sys, json, math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]; OUT = argv[argv.index("--out") + 1]; LIVE = argv[argv.index("--live") + 1]
FT = 0.3048; res = []
def rec(i, what, target, tol, meas, src):
    res.append({"id": i, "check": what, "target": target, "tol": tol, "measured": round(meas, 3), "pass": abs(meas - target) <= tol, "source": src})
O = bpy.data.objects
def bbz(o):
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]; return [min(v[i] for v in bb) / FT for i in range(3)], [max(v[i] for v in bb) / FT for i in range(3)]
fr = O["C26T_WALL_SE1_mid_frame"]
dg = bpy.context.evaluated_depsgraph_get()
bvh = BVHTree.FromObject(fr, dg)
def occupied(x, z):   # ray across the wall plane (y) at (x, z): does it hit the frame?
    h = bvh.ray_cast(Vector((x * FT, -205.5 * FT, z * FT)), Vector((0, 1, 0)), 3 * FT); return h[0] is not None
def intervals(z, step=0.01):
    out = []; cur = None; x = -11.7
    while x <= 11.7:
        o = occupied(x, z)
        if not o and cur is None: cur = x
        if o and cur is not None: out.append((cur, x)); cur = None
        x += step
    if cur is not None: out.append((cur, 11.7))
    return out
op = intervals(7.0)
rec("T01", "door openings in the central bay at 7 ft (count)", 3, 0, len(op), "FT06: three 6 ft door openings")
for k, (a, b) in enumerate(op):
    rec(f"T02_{k}", f"door opening {k} clear width at 7 ft (ft)", 6.0, 0.03, b - a, "FT06 (6 ft openings; leaves 2 x 3 ft)")
cen = [(a + b) / 2 for a, b in op]
rec("T03", "door opening pitch (ft) = 8 ft compartments between wood columns B", 8.0, 0.03, (cen[-1] - cen[0]) / 2 if len(cen) == 3 else -1, "Downes p.34, Plate XXI: 24 ft bays in three 8 ft compartments")
solid = intervals(15.0)
rec("T04", "no opening through the frame at 14.0-14.5 ft (door head) -> free intervals at 14.25 ft", 0, 0, len(intervals(14.25)), "Downes Plate XXII Fig 18: door head 6 in square")
mn, mx = bbz(fr)
leaf = O["SOUTH_DOORS_OPEN"]; lmn, lmx = bbz(leaf)
# door head underside: first hit downward from 14.25 ft at x = 0 over the centre door
h = bvh.ray_cast(Vector((0, -204 * FT, 13.0 * FT)), Vector((0, 0, 1)), 5 * FT)
rec("T05", "door head underside (ft) = FT06 leaf top", lmx[2], 0.01, (h[0].z / FT) if h[0] else -1, "FT06 leaves 14 ft")
h2 = bvh.ray_cast(Vector((0, -204 * FT, 14.3 * FT)), Vector((0, 0, 1)), 5 * FT)  # inside the head: next face up is the head top
w = O["WALL_SE1_12_0"]; wmn, wmx = bbz(w)
rec("T06", "frame top (ft) = flanking WALL_SE1 frame top (16.67)", wmx[2], 0.01, mx[2], "build_transept.py wall_run (19.17 - 2.5 louvre)")
rec("T07", "frame depth in y (ft) = wall-frame depth 6 in (+ 1 in sill nosing each side)", 0.6, 0.01, mx[1] - mn[1], "mesh_wall_bay +-3 in; sill 4.3 x 6.5 in (Plate XXII Fig 18)")
rec("T08", "frame stays on the wall line: centre y (ft)", -204.0, 0.01, (mx[1] + mn[1]) / 2, "south end column line y = -204")
lv = O["C26T_WLOUV_SE1_mid"]; lvm, lvx = bbz(lv); rf, rx = bbz(O["WLOUV_SE1_12_0"])
rec("T09a", "louvre band bottom (ft) = flanking WLOUV_SE1", rf[2], 0.001, lvm[2], "FT96")
rec("T09b", "louvre band top (ft) = flanking WLOUV_SE1", rx[2], 0.001, lvx[2], "FT96")
rec("T09c", "louvre band x span (ft) = central bay 24", 24.0, 0.01, lvx[0] - lvm[0], "FT96")
# door posts: measured on the 7 ft line between opening edges and the B columns / frame posts
posts = []
occ = []; x = -11.79; cur = None
while x <= 11.79:
    o = occupied(x, 7.0)
    if o and cur is None: cur = x
    if not o and cur is not None: occ.append((cur, x)); cur = None
    x += 0.005
if cur is not None: occ.append((cur, 11.79))
rec("T10", "solid runs at 7 ft between the frame posts at +-12 (2 end door posts + 2 post/column/post runs)", 4, 0, len(occ), "FT95")
ends = [b - a for a, b in occ if a < -11 or b > 11]
rec("T11", "end door post width (ft); Downes door posts 1 ft x 6 in, here 9.5 in (FT99)", 1.0, 0.25, min(ends) if ends else -1, "Downes Plate XXII Fig 17 (door posts 1 ft x 6 in)")
mids = [b - a for a, b in occ if a > -11 and b < 11]
rec("T12", "door post + wood column B + door post run (ft) = 2 ft between openings", 2.0, 0.03, max(mids) if mids else -1, "FT06 openings at 8 ft pitch")
# leaves clear of the posts
lc = 0
for xc in (-8, 0, 8):
    for sx in (-1, 1):
        if occupied(xc + 2.88 * sx, 7.0): lc += 1
rec("T13", "leaf hinge lines (xc +- 2.88 ft) inside the clear openings: blocked count", 0, 0, lc, "FT06 leaves swing inside the opening")
# staging
figs = [o for o in O if o.get("part_kind") == "figure" and not o.hide_render]
clash = [o.name for o in figs if abs(o.location.y / FT + 204) < 0.6 and occupied(o.location.x / FT, 4.0)] if figs else []
rec("T14", "figures standing inside the new frame (count)", 0, 0, len(clash), "staging")
trees = [o for o in O if o.name.startswith("C26T_TREE_") and o.type == 'EMPTY']
rec("T15a", "Kensington Road side trees (count, x -700..700)", 11, 0, len(trees), "FT97")
ys = [o.location.y / FT for o in trees]; xs = sorted(o.location.x / FT for o in trees)
rec("T15b", "tree row mean y (ft); exterior EX31 row y = -520", -520.0, 12.0, sum(ys) / len(ys), "exterior EX31")
rec("T15c", "max |y - (-520)| (ft) <= 12", 0.0, 12.0, max(abs(y + 520) for y in ys), "EX22 jitter +-12")
gaps = [b - a for a, b in zip(xs, xs[1:])]
rec("T15d", "min tree spacing (ft) >= 115", 132.5, 17.5, min(gaps), "EX31 115-150 ft")
rec("T15e", "max tree spacing (ft) <= 150", 132.5, 17.5, max(gaps), "EX31 115-150 ft")
hts = []
for t in trees:
    zs = [ (c.matrix_world @ Vector(v)).z for c in t.children for v in c.bound_box]; hts.append(max(zs) / FT)
rec("T15f", "lowest tree top (ft) within the exterior 62-86 ft range +-10 %", 74.0, 18.2, min(hts), "EX22 62/74/86 ft")
rec("T15g", "highest tree top (ft) within the exterior 62-86 ft range +-10 %", 74.0, 18.2, max(hts), "EX22 62/74/86 ft")
rec("T15h", "nearest tree to the south front (ft) > 300 (outside the apron, beyond the queue)", 316.0, 16.0, min(-204 - y for y in ys), "apron to y = -320")
cand = {o.name: (tuple(round(v, 5) for v in o.matrix_world.translation), o.hide_render, o.data.name if o.data else None) for o in O}
hid_c = sorted(n for n, v in cand.items() if v[1])
bpy.ops.wm.open_mainfile(filepath=LIVE)
live = {o.name: (tuple(round(v, 5) for v in o.matrix_world.translation), o.hide_render, o.data.name if o.data else None) for o in bpy.data.objects}
added = sorted(set(cand) - set(live)); removed = sorted(set(live) - set(cand))
changed = sorted(n for n in live if n in cand and live[n] != cand[n])
rec("T16a", "objects removed from live h03 (count)", 0, 0, len(removed), "FT98")
rec("T16b", "live h03 objects moved / hidden / re-meshed (count)", 0, 0, len(changed), "FT98")
rec("T16c", "objects added that are not C26T_* (count)", 0, 0, len([n for n in added if not n.startswith("C26T_")]), "FT98")
rec("T16d", "hidden objects: candidate minus live (count)", 0, 0, len(hid_c) - len([n for n, v in live.items() if v[1]]), "FT98: nothing hidden")
json.dump({"checks": res, "added": added, "changed": changed, "removed": removed}, open(OUT, "w"), indent=1)
print("CP026T_CHECKS", sum(r["pass"] for r in res), "/", len(res), "added", len(added))
for r in res:
    if not r["pass"]: print("FAIL", r)
