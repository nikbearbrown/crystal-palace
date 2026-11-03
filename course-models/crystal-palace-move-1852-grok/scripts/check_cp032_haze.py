"""CANDIDATE CP032 parkland depth / haze / meadow / ruts checks (2026-11-03, no verdict; DEPARTURES MV20).
  python3 scripts/check_cp032_haze.py      -> dumps live m02 + candidate via Blender, writes checks/m02_cp032haze_checks.json
Checks: object set = live + ARR_PK_* only (all in ARR_SYDENHAM_1852); nothing removed; transforms identical except
ARR_OAK_* whose change is a uniform scale only (location and rotation identical, scale 0.80-1.15); mesh data changes
only on ARR_OAK_* and ARR_YD_RUTS; material slots change only on ARR_GRASS / ARR_YD_RUTS / ARR_OAK_*; no instance
changes; every pre-existing material is unchanged (node/value hash); cameras (CP032 + all) and scene look/exposure
unchanged; no DEP_* (Hyde Park 1851) object touched; Muse's crate collection unchanged."""
import json, os, subprocess, tempfile
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "/workspace/blender5/blender"
LIVE = os.path.join(HERE, "rounds/m02.blend"); CAND = os.path.join(HERE, "rounds/candidates/m02_cp032haze.blend")
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
    d[o.name] = dict(mw=[round(x, 6) for r in o.matrix_world for x in r], loc=[round(x, 6) for x in o.location],
        rot=[round(x, 6) for x in o.rotation_euler], scl=[round(x, 6) for x in o.scale], mesh=h,
        polys=len(o.data.polygons) if o.type == "MESH" else 0,
        mats=[s.material.name if s.material else None for s in o.material_slots],
        colls=[c.name for c in o.users_collection], inst=o.instance_collection.name if o.instance_collection else None,
        cam=[o.data.lens, o.data.sensor_width, o.data.clip_start, o.data.clip_end] if o.type == "CAMERA" else None,
        bb=[min(v.x for v in bb), min(v.y for v in bb), min(v.z for v in bb), max(v.x for v in bb), max(v.y for v in bb), max(v.z for v in bb)])
def mhash(m):
    s = []
    if m.node_tree:
        for n in sorted(m.node_tree.nodes, key=lambda x: x.name):
            s.append(n.name + n.bl_idname)
            for i in n.inputs:
                v = getattr(i, "default_value", None)
                try: v = tuple(round(x, 5) for x in v)
                except TypeError: v = round(v, 5) if isinstance(v, float) else v
                s.append(str(v))
        for l in m.node_tree.links: s.append(l.from_node.name + l.from_socket.identifier + l.to_node.name + l.to_socket.identifier)
    return hashlib.md5("|".join(s).encode()).hexdigest()
d["__mats__"] = {m.name: mhash(m) for m in bpy.data.materials}
sc = bpy.context.scene; vs = sc.view_settings
d["__scene__"] = dict(exposure=vs.exposure, gamma=vs.gamma, view=vs.view_transform, look=vs.look, world=sc.world.name if sc.world else None,
                      world_hash=mhash(sc.world) if sc.world else None, res=[sc.render.resolution_x, sc.render.resolution_y],
                      states=bpy.data.texts["grok_states"].as_string() if "grok_states" in bpy.data.texts else None)
d["__muse__"] = sorted(o.name for o in bpy.data.collections["MUSE_Crate_by_Muse"].objects)
json.dump(d, open(out, "w"))
'''
def dump(blend):
    f = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False); f.write(DUMP); f.close()
    o = tempfile.mktemp(suffix=".json")
    subprocess.run([B, "-b", blend, "-P", f.name, "--", o], check=True, capture_output=True)
    return json.load(open(o))
L, C = dump(LIVE), dump(CAND)
LM, CM = L.pop("__mats__"), C.pop("__mats__"); LS, CS = L.pop("__scene__"), C.pop("__scene__")
muse_ok = L.pop("__muse__") == C.pop("__muse__")
new = sorted(set(C) - set(L)); gone = sorted(set(L) - set(C))
SLOTS_OK = {"ARR_GRASS", "ARR_YD_RUTS"}
slot_ch, tf_ch, mesh_ch, inst_ch, oaks, cam_ch = {}, [], [], {}, {}, []
for n in L:
    if n not in C: continue
    a, b = L[n], C[n]
    if a["mw"] != b["mw"]: tf_ch.append(n)
    if a["mesh"] != b["mesh"]: mesh_ch.append(n)
    if a["mats"] != b["mats"]: slot_ch[n] = [a["mats"], b["mats"]]
    if a["inst"] != b["inst"]: inst_ch[n] = [a["inst"], b["inst"]]
    if a["cam"] != b["cam"]: cam_ch.append(n)
    if n.startswith("ARR_OAK_"):
        s = b["scl"]
        oaks[n] = dict(loc_same=a["loc"] == b["loc"], rot_same=a["rot"] == b["rot"], scale=s[0], uniform=abs(s[0] - s[1]) < 1e-6 and abs(s[0] - s[2]) < 1e-6,
                       h_old=round(a["bb"][5] - a["bb"][2], 2), h_new=round(b["bb"][5] - b["bb"][2], 2), habit=b["mats"][1] if len(b["mats"]) > 1 else None)
tf_bad = [n for n in tf_ch if not n.startswith("ARR_OAK_")]
oak_tf_ok = all(v["loc_same"] and v["rot_same"] and v["uniform"] and 0.799 <= v["scale"] <= 1.151 for v in oaks.values())
mat_changed = sorted(m for m in LM if m in CM and LM[m] != CM[m]); mat_gone = sorted(set(LM) - set(CM)); mat_new = sorted(set(CM) - set(LM))
dep_touched = sorted(n for n in set(slot_ch) | set(tf_ch) | set(mesh_ch) | set(inst_ch) if n.startswith("DEP_") or "1851" in n)
newc = {}
for n in new:
    k = n.split("_")[2] if n.count("_") >= 2 else n; newc[k] = newc.get(k, 0) + 1
res = dict(date="2026-11-03", candidate="rounds/candidates/m02_cp032haze.blend", base="rounds/m02.blend (move 5b943fa, MV19 live)",
    new_objects=len(new), new_by_kind=newc, removed_objects=gone,
    new_only_ARR_PK=all(n.startswith("ARR_PK_") for n in new),
    new_in_ARR_SYDENHAM_1852=all(C[n]["colls"] == ["ARR_SYDENHAM_1852"] for n in new),
    no_hydepark_added=not any(("1851" in n) or n.upper().startswith(("HP_", "HYDE", "DEP_")) for n in new),
    muse_crate_collection_unchanged=muse_ok,
    transform_changed=len(tf_ch), transform_changed_not_oak=tf_bad, oak_transform_scale_only=oak_tf_ok,
    oak_scale_range=[min(v["scale"] for v in oaks.values()), max(v["scale"] for v in oaks.values())],
    oak_height_range_old=[min(v["h_old"] for v in oaks.values()), max(v["h_old"] for v in oaks.values())],
    oak_height_range_new=[min(v["h_new"] for v in oaks.values()), max(v["h_new"] for v in oaks.values())],
    elm_objects=sorted(n for n, v in oaks.items() if v["habit"] == "GT_ElmLeaf1852h"),
    mesh_changed=sorted(set(n if not n.startswith("ARR_OAK_") else "ARR_OAK_*" for n in mesh_ch)), mesh_changed_count=len(mesh_ch),
    mesh_changed_allowed=all(n.startswith("ARR_OAK_") or n == "ARR_YD_RUTS" for n in mesh_ch),
    ruts_polys=[L["ARR_YD_RUTS"]["polys"], C["ARR_YD_RUTS"]["polys"]],
    tree_polys_old=sum(L[n]["polys"] for n in oaks), tree_polys_new=sum(C[n]["polys"] for n in oaks) + sum(C[n]["polys"] for n in new if "_FAR_" in n or "_THORN_" in n),
    new_polys_total=sum(C[n]["polys"] for n in new),
    material_slot_changes={k: v for k, v in slot_ch.items() if not k.startswith("ARR_OAK_")}, oak_slot_changes=sum(k.startswith("ARR_OAK_") for k in slot_ch),
    slot_changes_allowed=all(n in SLOTS_OK or n.startswith("ARR_OAK_") for n in slot_ch),
    instance_changes=inst_ch, existing_materials_changed=mat_changed, materials_removed=mat_gone, materials_new=mat_new,
    camera_data_changed=cam_ch, scene_look_unchanged=LS == CS, scene=CS,
    dep_objects_touched=dep_touched,
    notes="MV19 GT_OakLeaf1852 / GT_OakBark1852 / GT_SydenhamMeadow1852 / GT_CartRutClay had no users left (ARR_* only) and are "
          "dropped on save, as are the orphaned MV19 oak meshes. Haze lives only in the new *_h materials and GT_SydenhamMeadow1852b.")
res["pass"] = bool(not gone and res["new_only_ARR_PK"] and res["new_in_ARR_SYDENHAM_1852"] and res["no_hydepark_added"] and muse_ok
    and not tf_bad and oak_tf_ok and res["mesh_changed_allowed"] and res["slot_changes_allowed"] and not inst_ch
    and not mat_changed and not cam_ch and res["scene_look_unchanged"] and not dep_touched)
os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
json.dump(res, open(os.path.join(HERE, "checks/m02_cp032haze_checks.json"), "w"), indent=1)
r2 = dict(res); r2.pop("scene")
print(json.dumps(r2, indent=1)); print("CP032_HAZE_CHECKS", "PASS" if res["pass"] else "FAIL")
