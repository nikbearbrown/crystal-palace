"""CP074 geocourt CANDIDATE checks (2026-11-16). blender -b BLEND -P checks/cp074_geocourt_check.py -- OUT.json
Dumps camera transforms, world/look-relevant scene settings, sculpture dimensions vs sources, and candidate object datings."""
import bpy, sys, json, math
out = sys.argv[sys.argv.index("--") + 1]
sc = bpy.context.scene
D = {"blend": bpy.data.filepath, "cams": {}, "scene": {}, "dims": {}, "cand": {}}
for o in bpy.data.objects:
    if o.type == "CAMERA":
        D["cams"][o.name] = [round(v, 5) for v in (*o.location, *o.rotation_euler, o.data.lens, o.data.sensor_width)]
D["scene"] = {"exposure": sc.view_settings.exposure, "view": sc.view_settings.view_transform, "world": sc.world.name if sc.world else None,
              "samples": sc.cycles.samples, "res": [sc.render.resolution_x, sc.render.resolution_y],
              "sun": [[round(v, 5) for v in (*o.location, *o.rotation_euler, o.data.energy)] for o in bpy.data.objects if o.type == "LIGHT"]}
FT = 0.3048
SRC = {"iguanodon_standing": (10.0, 2.7, "cpdinosaurs.org: c.10 m long, 2.7 m high"),
       "iguanodon_recumbent": (10.0, 7.0 * FT, "length as standing; 7.0 ft high (dinosaurs-1854 DEPARTURES 4, I)"),
       "megalosaurus": (10.0, 3.5, "Historic England / cpdinosaurs: c.10 m x 3.5 m"),
       "hylaeosaurus": (7.4, None, "24.4 ft / 7.4 m by eye (dinosaurs-1854 DEPARTURES 6, I)")}
for n, (L, H, s) in SRC.items():
    o = bpy.data.objects[n]; d = o.dimensions
    okL = abs(d.x - L) / L <= 0.10 or abs(d.x - L) <= FT
    okH = True if H is None else (abs(d.z - H) / H <= 0.12 or abs(d.z - H) <= FT)
    D["dims"][n] = {"L_m": round(d.x, 2), "H_m": round(d.z, 2), "src_L": L, "src_H": H, "source": s, "pass": bool(okL and okH)}
c = [o for o in bpy.data.objects if "cp074_now" in o.keys()]
D["cand"] = {"n": len(c), "undated": [o.name for o in c if "dated" not in o.keys()],
             "not_parknow": [o.name for o in c if not any(cl.name.startswith("PARKNOW_CP074") for cl in o.users_collection)],
             "hyde_park_or_1851_objects_added": [o.name for o in c if any(k in o.name.lower() for k in ("hyde", "1851", "hp_"))],
             "tree_H_m": sorted(round(o.dimensions.z, 1) for o in c if o.name.startswith("cp74_tree_"))[:3] + ["..."] + sorted(round(o.dimensions.z, 1) for o in c if o.name.startswith("cp74_tree_"))[-3:],
             "taxodium_H_m": [round(o.dimensions.z, 1) for o in c if o.name.startswith("cp74_taxodium")],
             "cycas_H_m": [round(o.dimensions.z, 2) for o in c if o.name.startswith("cp74_cycas")][:6],
             "fern_spread_m": [round(max(o.dimensions.x, o.dimensions.y), 2) for o in c if o.name.startswith("cp74_fern")][:6],
             "gravel_LxW_m": {o.name: [round(o.dimensions.x, 1), round(o.dimensions.y, 1)] for o in c if o.name.startswith("cp74_gravel")},
             "rock_max_m": round(max([max(o.dimensions) for o in c if o.name.startswith("cp74_rock")] or [0]), 2)}
D["sculpture_slots"] = {o.name: [(s.link, s.material.name if s.material else None) for s in o.material_slots] for o in bpy.data.collections["DN54_secondary_island_sculptures__1854"].all_objects}
D["hidden_render"] = sorted(o.name for o in bpy.data.objects if o.hide_render)
json.dump(D, open(out, "w"), indent=1); print("CHECK_WROTE", out)
