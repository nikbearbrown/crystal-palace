"""CANDIDATE CP032 parkland oaks / meadow / timber / hats checks (2026-11-02, no verdict; DEPARTURES MV19).
  python3 scripts/check_cp032_trees.py      -> dumps live m02 + candidate via Blender, writes checks/m02_cp032trees_checks.json
Checks: object set = live + ARR_HD_* + ARR_SY_* (crate copies, in their own collection) only; every pre-existing object
keeps its transform; mesh data changes only on ARR_OAK_* (new parametric oaks: crown top within 5 cm of the old top, bole sunk <1 m below the old foot) and
material slots change only on ARR_GRASS / ARR_BEARERS_* / ARR_BARS_GUTTERS / the 4 ARR_HAND workmen (cap slot);
ARR_CRATE_0/1 instance the ARR-only copy; no DEP_* (Hyde Park 1851) object or MUSE_Crate_by_Muse member changed;
each new hat sits on its figure's skull (hat crown centre within 3 cm of the skull axis, crown base below the head top)."""
import json, os, subprocess, tempfile
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "/workspace/blender5/blender"
LIVE = os.path.join(HERE, "rounds/m02.blend"); CAND = os.path.join(HERE, "rounds/candidates/m02_cp032trees.blend")
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
    d[o.name] = dict(mw=[round(x, 6) for r in o.matrix_world for x in r], mesh=h, polys=len(o.data.polygons) if o.type == "MESH" else 0,
        mats=[s.material.name if s.material else None for s in o.material_slots],
        colls=[c.name for c in o.users_collection], tag=bool(o.get("cp032_trees")), fig=o.get("figure"),
        inst=o.instance_collection.name if o.instance_collection else None,
        bb=[min(v.x for v in bb), min(v.y for v in bb), min(v.z for v in bb), max(v.x for v in bb), max(v.y for v in bb), max(v.z for v in bb)])
heads = {}
for o in bpy.data.objects:
    if o.name.startswith("ARR_HAND_") and o.type == "MESH":
        me = o.data; mw = o.matrix_world
        sk = [i for i, s in enumerate(o.material_slots) if s.material and "skin" in s.material.name.lower()]
        V = [mw @ me.vertices[j].co for p in me.polygons if p.material_index in sk for j in p.vertices]
        top = max(v.z for v in V); sl = [v for v in V if top - 0.07 < v.z < top - 0.02]
        heads[o.name] = [(min(v.x for v in sl) + max(v.x for v in sl)) / 2, (min(v.y for v in sl) + max(v.y for v in sl)) / 2, top]
d["__heads__"] = heads
d["__muse__"] = sorted(o.name for o in bpy.data.collections["MUSE_Crate_by_Muse"].objects)
json.dump(d, open(out, "w"))
'''
def dump(blend):
    f = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False); f.write(DUMP); f.close()
    o = tempfile.mktemp(suffix=".json")
    subprocess.run([B, "-b", blend, "-P", f.name, "--", o], check=True, capture_output=True)
    return json.load(open(o))
L, C = dump(LIVE), dump(CAND)
L.pop("__heads__"); HEADS = C.pop("__heads__"); muse_ok = L.pop("__muse__") == C.pop("__muse__")
new = sorted(set(C) - set(L)); gone = sorted(set(L) - set(C))
SLOTS_OK = {"ARR_GRASS", "ARR_BEARERS_COL", "ARR_BEARERS_GIR", "ARR_BARS_GUTTERS",
            "ARR_HAND_00_workman", "ARR_HAND_01_workman", "ARR_HAND_02_workman", "ARR_HAND_03_navvy"}
slot_ch, tf_bad, mesh_ch, inst_ch, oak_h = {}, [], [], {}, {}
for n in L:
    if n not in C: continue
    a, b = L[n], C[n]
    if a["mw"] != b["mw"]: tf_bad.append(n)
    if a["mesh"] != b["mesh"]: mesh_ch.append(n)
    if a["mats"] != b["mats"]: slot_ch[n] = [a["mats"], b["mats"]]
    if a["inst"] != b["inst"]: inst_ch[n] = [a["inst"], b["inst"]]
    if n.startswith("ARR_OAK_") and a["mesh"] != b["mesh"]:
        ha = a["bb"][5] - a["bb"][2]; hb = b["bb"][5] - b["bb"][2]
        oak_h[n] = dict(h_old=round(ha, 2), h_new=round(hb, 2), top_dz=round(b["bb"][5] - a["bb"][5], 3), base_dz=round(b["bb"][2] - a["bb"][2], 2),
                        w_old=round(max(a["bb"][3] - a["bb"][0], a["bb"][4] - a["bb"][1]), 1),
                        w_new=round(max(b["bb"][3] - b["bb"][0], b["bb"][4] - b["bb"][1]), 1))
oaks_all = sorted(n for n in L if n.startswith("ARR_OAK_") and L[n]["mesh"])
oak_ok = set(oak_h) == set(oaks_all) and all(abs(v["top_dz"]) < 0.05 and -1.0 < v["base_dz"] <= 0.0 for v in oak_h.values())
hats = {}
for n in new:
    if n.startswith("ARR_HD_HAT_"):
        f = C[n]["fig"]; hx, hy, ht = HEADS[f]; bb = C[n]["bb"]
        cx, cy = (bb[0] + bb[3]) / 2, (bb[1] + bb[4]) / 2
        hats[n] = dict(figure=f, axis_off_m=round(((cx - hx) ** 2 + (cy - hy) ** 2) ** 0.5, 3),
                       base_below_top_m=round(ht - bb[2], 3), top_above_head_m=round(bb[5] - ht, 3))
hats_ok = len(hats) == 4 and all(v["axis_off_m"] < 0.03 and 0.03 < v["base_below_top_m"] < 0.12 and 0.02 < v["top_above_head_m"] < 0.09 for v in hats.values())
dep_touched = sorted(n for n in set(slot_ch) | set(tf_bad) | set(mesh_ch) | set(inst_ch) if n.startswith("DEP_") or "1851" in n)
res = dict(date="2026-11-02", candidate="rounds/candidates/m02_cp032trees.blend", base="rounds/m02.blend (move d1711db, MV18 live)",
    new_objects=len(new), removed_objects=gone,
    new_only_ARR_HD_or_ARR_SY=all(n.startswith(("ARR_HD_", "ARR_SY_")) for n in new),
    hats_hair_in_ARR_SYDENHAM_1852=all("ARR_SYDENHAM_1852" in C[n]["colls"] for n in new if n.startswith("ARR_HD_")),
    crate_copies_in_ARR_CrateSY1852=all(C[n]["colls"] == ["ARR_CrateSY1852_from_Muse"] for n in new if n.startswith("ARR_SY_")),
    muse_crate_collection_unchanged=muse_ok,
    no_hydepark_added=not any(("1851" in n) or n.upper().startswith(("HP_", "HYDE", "DEP_")) for n in new),
    transforms_identical=not tf_bad, transform_changed=tf_bad,
    mesh_changed_only_oaks=all(n.startswith("ARR_OAK_") for n in mesh_ch), mesh_changed_count=len(mesh_ch),
    oaks=oak_h, oak_heights_kept=oak_ok,
    oak_polys_old=sum(L[n]["polys"] for n in oaks_all), oak_polys_new=sum(C[n]["polys"] for n in oaks_all),
    material_slot_changes=slot_ch, slot_changes_allowed=all(n in SLOTS_OK or n.startswith("ARR_OAK_") for n in slot_ch),
    instance_changes=inst_ch, instance_changes_allowed=set(inst_ch) <= {"ARR_CRATE_0", "ARR_CRATE_1"},
    dep_objects_touched=dep_touched, hats=hats, hats_on_heads=hats_ok,
    notes="Gentleman (ARR_HAND_04) keeps his CP032C top hat. Workmen cap slot is object-linked to GT_CapRetired_CP032 "
          "(transparent) so shared CPL3_hat_* (also on DEP figures) are untouched. Wagon keeps GT_OakBearer.")
res["pass"] = bool(not gone and res["new_only_ARR_HD_or_ARR_SY"] and res["hats_hair_in_ARR_SYDENHAM_1852"]
    and res["crate_copies_in_ARR_CrateSY1852"] and muse_ok and res["no_hydepark_added"] and not tf_bad
    and res["mesh_changed_only_oaks"] and oak_ok and res["slot_changes_allowed"] and res["instance_changes_allowed"]
    and not dep_touched and hats_ok)
os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
json.dump(res, open(os.path.join(HERE, "checks/m02_cp032trees_checks.json"), "w"), indent=1)
r2 = dict(res); r2["oaks"] = "%d oaks" % len(oak_h); r2["material_slot_changes"] = sorted(n for n in slot_ch if not n.startswith("ARR_OAK_")) + ["ARR_OAK_* x%d" % sum(n.startswith("ARR_OAK_") for n in slot_ch)]; r2["hats"] = "see json"
print(json.dumps(r2, indent=1)); print("CP032_TREES_CHECKS", "PASS" if res["pass"] else "FAIL")
