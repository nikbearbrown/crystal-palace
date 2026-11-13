"""CP070 station CANDIDATE checks (2026-11-13).
 1) blender -b rounds/parknow-r02.blend -P checks/check_cp070_station.py -- dump /tmp/live.json
 2) blender -b rounds/candidates/parknow-r02_cp070station.blend -P checks/check_cp070_station.py -- dump /tmp/cand.json
 3) python3 checks/check_cp070_station.py compare /tmp/live.json /tmp/cand.json checks/cp070_station_checks.json
Scope vs live (nothing deleted; only listed hide_render flips + the two CP070 cams changed; every new object tagged
cp070_now and inside the dated PARKNOW_CP070 collection), state/dating rules, and dimensions vs sources."""
import sys, json, math
try:
    import bpy
    from mathutils import Vector
except ImportError:
    bpy = None
a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
if a[0] == "dump":
    sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get(); D = {"objects": {}, "colls": {}}
    for o in bpy.data.objects:
        D["objects"][o.name] = {"type": o.type, "hide_render": o.hide_render, "data": o.data.name if o.data else None,
                                "mw": [round(v, 4) for r in o.matrix_world for v in r], "tag": o.get("cp070_now"),
                                "colls": [c.name for c in o.users_collection], "H_m": o.get("H_m"),
                                "lens": o.data.lens if o.type == "CAMERA" else None,
                                "nverts": len(o.data.vertices) if o.type == "MESH" else None}
    def walk(c, path):
        D["colls"][c.name] = path
        for ch in c.children: walk(ch, path + [c.name])
    walk(sc.collection, [])
    # grounding: feet of new visitors / trees vs the highest visible surface under them (excluding themselves)
    D["ground"] = {}
    for o in bpy.data.objects:
        if o.get("cp070_now") and (o.name.startswith("cp70_ppl_") or o.name.startswith("cp70_tree") or o.name.startswith("cp70_PLACEHOLDER")):
            hr = o.hide_render; o.hide_viewport = True; dg.update()
            p = o.location; best = None
            for dx, dy in ((0, 0), (0.06, 0.06), (-0.06, -0.06)):
                ok, loc, n, i, ob, m = sc.ray_cast(dg, Vector((p.x + dx, p.y + dy, p.z + 3.0)), Vector((0, 0, -1)))
                while ok and (ob.hide_render or ob.name.startswith("cp70_ppl_")):
                    ok, loc, n, i, ob, m = sc.ray_cast(dg, loc + Vector((0, 0, -0.001)), Vector((0, 0, -1)))
                if ok and (best is None or loc.z > best[0]): best = (loc.z, ob.name)
            o.hide_viewport = False; dg.update()
            D["ground"][o.name] = [round(p.z, 3), round(best[0], 3) if best else None, best[1] if best else None]
    json.dump(D, open(a[1], "w"), indent=0); print("DUMPED", a[1], len(D["objects"])); sys.exit(0) if not bpy else None
if a[0] == "compare":
    L = json.load(open(a[1])); C = json.load(open(a[2])); res = []
    def chk(ok, label, src=""): res.append({"ok": bool(ok), "check": label, "src": src}); print("PASS" if ok else "FAIL", label, src)
    lo, co = L["objects"], C["objects"]
    chk(set(lo) <= set(co), "nothing deleted (every live object still present)", "scope")
    new = sorted(set(co) - set(lo)); chk(all(co[n]["tag"] for n in new if co[n]["type"] in ("MESH", "FONT")), f"all {len(new)} new objects tagged cp070_now", "scope")
    chk(all(any("PARKNOW_CP070" in c or "PARKNOW_CP070" in "/".join(C["colls"].get(c, [])) for c in co[n]["colls"]) for n in new if co[n]["type"] in ("MESH", "FONT")), "new objects inside PARKNOW_CP070_lowlevel_station__present", "scope")
    chk(all("PARK-NOW_present_day" in C["colls"].get(c, []) for n in new for c in co[n]["colls"] if co[n]["type"] in ("MESH", "FONT")), "new collection nested under the dated PARK-NOW_present_day root", "dating")
    changed = [n for n in lo if n in co and (lo[n]["mw"] != co[n]["mw"] or lo[n]["data"] != co[n]["data"] or lo[n]["lens"] != co[n]["lens"])]
    chk(sorted(changed) == ["CAM_CP070_begin_walk_35mm", "CAM_CP070_park_entry_35mm"], f"only the two CP070 cameras moved/changed: {sorted(changed)}", "scope")
    flips = [n for n in lo if n in co and lo[n]["hide_render"] != co[n]["hide_render"]]
    chk(all(not lo[n]["hide_render"] and co[n]["hide_render"] for n in flips), f"{len(flips)} live objects hidden (render only), none un-hidden", "scope")
    chk(all(n.startswith(("PLACEHOLDER_park_tree", "colonnade_", "pk_tree_", "ppl_now")) for n in flips), "hidden set = placeholder trees + 1854 colonnade only", "scope")
    chk(not any(k in n.lower() for n in new for k in ("hyde", "1851", "hp_", "transept")), "no Hyde Park / 1851 objects added", "rule: never blend HP and Sydenham")
    chk(all("present" in c or "PARKNOW" in c or "1875_as_today" in c for n in new for c in co[n]["colls"] if co[n]["type"] in ("MESH", "FONT")), "every new collection is dated (present / 1875 building as today)", "dating")
    # cameras
    import math as m_
    def loc(mw): return (mw[3], mw[7], mw[11])
    b, e = loc(co["CAM_CP070_begin_walk_35mm"]["mw"]), loc(co["CAM_CP070_park_entry_35mm"]["mw"])
    walk = m_.dist(b, e); chk(abs(walk - 8.0) < 0.05, f"walk between CP070 cams = {walk:.2f} m (storyboard 8 m)", "storyboard CP070")
    chk(co["CAM_CP070_begin_walk_35mm"]["lens"] == 35 and co["CAM_CP070_park_entry_35mm"]["lens"] == 35, "35 mm both CP070 cams", "storyboard CP070")
    G = C["ground"]; bad = [k for k, v in G.items() if v[1] is None or v[0] - v[1] > 0.03 or (k.startswith("cp70_ppl_") and v[1] - v[0] > 0.03) or v[1] - v[0] > 0.30]
    chk(not bad, f"{len(G)} new visitors/trees grounded: none floating (>3 cm), visitors' soles within 3 cm, tree bases sunk <= 0.30 m {bad}", "no floating")
    hs = [co[n]["H_m"] for n in new if n.startswith("cp70_ppl_")]
    chk(hs and all(1.55 <= h <= 1.90 for h in hs), f"visitor heights {min(hs)}-{max(hs)} m in adult range 1.55-1.90", "PPL-NOW")
    json.dump(res, open(a[3], "w"), indent=1); print("CHECKS", sum(r["ok"] for r in res), "/", len(res))
