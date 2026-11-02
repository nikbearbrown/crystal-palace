"""D-checks for the CP032 arrival-hands candidate (MV16).
blender -b rounds/candidates/m02_cp032arrival.blend -P scripts/check_cp032_arrival.py -- --out checks/m02_cp032arrival_checks.json
A1 five ARR_HAND_* present, no STAFF_07..11 left; A2 lowest vertex of each figure on ARR_GRASS/ARR_CLAY under it
(|dz| < 1 cm); A3 heights 1.60-1.85 m; A4 body core (0.36 x 0.36 m column, knee to shoulder) does not intersect any
non-ground mesh AABB; A5 departure DEP_HAND_* untouched (7); A6 nothing from Hyde Park in ARR_SYDENHAM_1852."""
import bpy, sys, json
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]; OUT = argv[argv.index("--out") + 1]
O = bpy.data.objects; R = []
def chk(cid, name, ok, val): R.append({"id": cid, "check": name, "pass": bool(ok), "value": val})
def gz(x, y):
    best = None
    for gn in ("ARR_GRASS", "ARR_CLAY"):
        g = O[gn]; mi = g.matrix_world.inverted()
        ok, loc, n, i = g.ray_cast(mi @ Vector((x, y, 200.0)), (mi.to_3x3() @ Vector((0, 0, -1))).normalized())
        if ok: z = (g.matrix_world @ loc).z; best = z if best is None else max(best, z)
    return best
H = [o for o in O if o.name.startswith("ARR_HAND_")]
chk("A1", "5 ARR_HAND_* and no STAFF_07..11", len(H) == 5 and not any(o.name.startswith(("STAFF_07", "STAFF_08", "STAFF_09", "STAFF_10", "STAFF_11")) for o in O), [o.name for o in H])
dz = {}; hs = {}
for o in H:
    zs = [(o.matrix_world @ v.co).z for v in o.data.vertices]; t = o.matrix_world.translation
    dz[o.name] = round(min(zs) - gz(t.x, t.y), 4); hs[o.name] = round(max(zs) - min(zs), 3)
chk("A2", "feet on the arrival ground (|dz|<0.01 m)", all(abs(v) < 0.01 for v in dz.values()), dz)
chk("A3", "heights 1.60-1.85 m", all(1.60 <= v <= 1.85 for v in hs.values()), hs)
skip = ("ARR_GRASS", "ARR_CLAY", "ARR_SPOIL", "ARR_HAND_", "DEP_", "K_", "MAP", "STAFF")
others = [o for o in O if o.type == 'MESH' and o.visible_get() is not None and not o.name.startswith(skip) and o.name.startswith("ARR")]
bad = []
for f in H:
    t = f.matrix_world.translation; z0 = min((f.matrix_world @ v.co).z for v in f.data.vertices)
    lo = (t.x - 0.18, t.y - 0.18, z0 + 0.5); hi = (t.x + 0.18, t.y + 0.18, z0 + 1.45)
    for o in others:
        cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
        mn = [min(c[i] for c in cs) for i in range(3)]; mx = [max(c[i] for c in cs) for i in range(3)]
        if all(lo[i] < mx[i] and hi[i] > mn[i] for i in range(3)): bad.append((f.name, o.name))
chk("A4", "figure core clear of every ARR part/prop AABB", not bad, bad[:8])
chk("A5", "departure DEP_HAND_* unchanged count 7", len([o for o in O if o.name.startswith("DEP_HAND_")]) == 7, None)
arr = bpy.data.collections["ARR_SYDENHAM_1852"].all_objects
chk("A6", "ARR collection holds no DEP_/Hyde Park objects", not [o.name for o in arr if o.name.startswith(("DEP_", "HP_"))], None)
json.dump(R, open(OUT, "w"), indent=1)
print("CHECKS %d/%d" % (sum(r["pass"] for r in R), len(R)))
for r in R: print(r["id"], r["pass"], r["value"])
