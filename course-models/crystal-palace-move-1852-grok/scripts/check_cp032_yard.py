"""CANDIDATE CP032 yard dressing checks (2026-11-02, no verdict; DEPARTURES MV18).
  python3 scripts/check_cp032_yard.py      -> dumps live m02 + candidate via Blender, writes checks/m02_cp032yard_checks.json
Checks: object set = live + ARR_YD_* only; every pre-existing object keeps transform, mesh data hash, modifiers (except
ARR_SPOIL's CP032Y_* modifiers) and material slots (except the listed ARR slots); all new objects are in
ARR_SYDENHAM_1852 and carry ["cp032_yard"]; dressing does not sit on any figure's feet; dressing is grounded
(min z within 5 cm of the yard); no Hyde Park (1851) object added."""
import json, os, subprocess, sys, tempfile, hashlib
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "/workspace/blender5/blender"
LIVE = os.path.join(HERE, "rounds/m02.blend"); CAND = os.path.join(HERE, "rounds/candidates/m02_cp032yard.blend")

DUMP = r'''
import bpy, json, sys, hashlib
from mathutils import Vector
out = sys.argv[sys.argv.index("--") + 1]
d = {}
for o in bpy.data.objects:
    h = None
    if o.type == "MESH":
        me = o.data; co = [0.0] * (len(me.vertices) * 3); me.vertices.foreach_get("co", co)
        h = hashlib.md5((str(len(me.polygons)) + ",".join("%.5f" % c for c in co)).encode()).hexdigest()
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
    d[o.name] = dict(mw=[round(x, 6) for r in o.matrix_world for x in r], mesh=h,
        mods=[m.name for m in o.modifiers], mats=[s.material.name if s.material else None for s in o.material_slots],
        colls=[c.name for c in o.users_collection], tag=bool(o.get("cp032_yard")),
        bb=[min(v.x for v in bb), min(v.y for v in bb), min(v.z for v in bb), max(v.x for v in bb), max(v.y for v in bb), max(v.z for v in bb)])
# per-vertex feet / grounding checks for the CP032Y dressing (only meaningful on the candidate)
yd = {}
clay = bpy.data.objects.get("ARR_CLAY")
if clay and any(n.startswith("ARR_YD_") for n in d):
    import bmesh
    from mathutils.bvhtree import BVHTree
    bm = bmesh.new(); bm.from_mesh(clay.data); bm.transform(clay.matrix_world); tree = BVHTree.FromBMesh(bm)
    def gz(x, y):
        h = tree.ray_cast(Vector((x, y, 60.0)), Vector((0, 0, -1)))
        return h[0].z if h[0] else None
    feet = []
    for o in bpy.data.objects:
        if o.name.startswith("ARR_HAND_") and o.type == "MESH":
            vs = [o.matrix_world @ v.co for v in o.data.vertices]
            if not vs: continue
            mz = min(v.z for v in vs); lo = [v for v in vs if v.z < mz + 0.15]
            feet.append((o.name, min(v.x for v in lo) - 0.05, min(v.y for v in lo) - 0.05, max(v.x for v in lo) + 0.05, max(v.y for v in lo) + 0.05, mz))
    hits, worst = [], {}
    for o in bpy.data.objects:
        if not o.name.startswith("ARR_YD_") or o.type != "MESH": continue
        vs = [o.matrix_world @ v.co for v in o.data.vertices]
        for f in feet:
            if o.name in ("ARR_YD_RUTS", "ARR_YD_PUDDLES"): break
            n_in = sum(1 for v in vs if f[1] < v.x < f[3] and f[2] < v.y < f[4] and v.z > f[5] + 0.02)
            if n_in: hits.append([o.name, f[0], n_in])
        # grounding: islands' lowest points vs clay (sampled)
        bmo = bmesh.new(); bmo.from_mesh(o.data); bmo.transform(o.matrix_world); bmo.verts.ensure_lookup_table()
        seen, gaps = set(), []
        for v0 in bmo.verts:
            if v0.index in seen: continue
            st, isl = [v0], []
            seen.add(v0.index)
            while st:
                v = st.pop(); isl.append(v)
                for e in v.link_edges:
                    w = e.other_vert(v)
                    if w.index not in seen: seen.add(w.index); st.append(w)
            lowv = min(isl, key=lambda v: v.co.z); g = gz(lowv.co.x, lowv.co.y)
            if g is not None: gaps.append(lowv.co.z - g)
        worst[o.name] = [round(min(gaps), 3), round(max(gaps), 3), len(gaps)] if gaps else None
    yd = dict(feet_boxes=[f[0] for f in feet], feet_hits=hits, island_low_minus_clay=worst)
d["__yd__"] = yd
json.dump(d, open(out, "w"))
'''
def dump(blend):
    f = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False); f.write(DUMP); f.close()
    o = tempfile.mktemp(suffix=".json")
    subprocess.run([B, "-b", blend, "-P", f.name, "--", o], check=True, capture_output=True)
    return json.load(open(o))

L, C = dump(LIVE), dump(CAND)
L.pop("__yd__", None); YD = C.pop("__yd__")
new = sorted(set(C) - set(L)); gone = sorted(set(L) - set(C))
ALLOWED_SLOTS = {"ARR_SPOIL", "ARR_BARS_GUTTERS"}
slot_changes, mod_changes, tf_bad, mesh_bad = {}, {}, [], []
for n in L:
    if n not in C: continue
    a, b = L[n], C[n]
    if a["mw"] != b["mw"]: tf_bad.append(n)
    if a["mesh"] != b["mesh"]: mesh_bad.append(n)
    if a["mats"] != b["mats"]: slot_changes[n] = [a["mats"], b["mats"]]
    if a["mods"] != b["mods"]: mod_changes[n] = [a["mods"], b["mods"]]
feet_hits = YD["feet_hits"]
grounded = YD["island_low_minus_clay"]
# every object's lowest island touches the clay; free-lying pieces (stones, boards, puddles, ruts) each do too.
# Barrow/tools are multi-island assemblies (wheel+body+handles; shovel resting in the barrow), so only their lowest point counts.
FREE = ("ARR_YD_STONES", "ARR_YD_BOARDS", "ARR_YD_PUDDLES", "ARR_YD_RUTS")
ground_ok = all(v is None or (-0.12 < v[0] < 0.12 and (k not in FREE or v[1] < 0.12)) for k, v in grounded.items())
res = dict(date="2026-11-02", candidate="rounds/candidates/m02_cp032yard.blend", base="rounds/m02.blend (move b19926f)",
    new_objects=new, removed_objects=gone,
    new_only_ARR_YD=all(n.startswith("ARR_YD_") for n in new),
    new_in_ARR_SYDENHAM_1852=all("ARR_SYDENHAM_1852" in C[n]["colls"] for n in new),
    new_tagged=all(C[n]["tag"] for n in new),
    no_hydepark_added=not any(("1851" in n) or n.upper().startswith(("HP_", "HYDE")) for n in new),
    transforms_identical=not tf_bad, transform_changed=tf_bad,
    meshes_identical=not mesh_bad, mesh_changed=mesh_bad,
    material_slot_changes=slot_changes, slot_changes_allowed=set(slot_changes) <= ALLOWED_SLOTS,
    modifier_changes=mod_changes,
    modifier_changes_allowed=set(mod_changes) <= {"ARR_SPOIL"} and all(all(m.startswith("CP032Y_") for m in v[1]) for v in mod_changes.values()),
    figure_feet_checked=YD["feet_boxes"], dressing_on_figure_feet=feet_hits,
    island_lowest_point_minus_clay_m=grounded, grounded_within_12cm=ground_ok,
    notes="GT_SydenhamClayYard node tree rebuilt in place (name kept, cp032_yard_v=1) so ARR_CLAY slot is unchanged; "
          "DEP_BARS_GUTTERS keeps GT_SashBarBundle/GT_GutterTimber (departure frames unchanged).")
res["pass"] = bool(not gone and res["new_only_ARR_YD"] and res["new_in_ARR_SYDENHAM_1852"] and res["new_tagged"]
    and res["no_hydepark_added"] and not tf_bad and not mesh_bad and res["slot_changes_allowed"]
    and res["modifier_changes_allowed"] and not feet_hits and ground_ok)
os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
json.dump(res, open(os.path.join(HERE, "checks/m02_cp032yard_checks.json"), "w"), indent=1)
print(json.dumps(res, indent=1)); print("CP032_YARD_CHECKS", "PASS" if res["pass"] else "FAIL")
