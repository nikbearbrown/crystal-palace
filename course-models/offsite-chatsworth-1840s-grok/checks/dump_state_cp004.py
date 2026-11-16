"""Dump scene state for the CP004 candidate checks: blender -b X.blend -P checks/dump_state_cp004.py -- out.json"""
import bpy, sys, json
out = sys.argv[sys.argv.index("--") + 1]; F = 0.3048; sc = bpy.context.scene
def r(v, n=5): return [round(x, n) for x in v]
d = {"objects": {}, "materials": {}, "scene": {"exposure": sc.view_settings.exposure, "look": sc.view_settings.look, "world": sc.world.name}}
for o in bpy.data.objects:
    e = {"type": o.type, "mw": [r(row) for row in o.matrix_world], "hide_render": o.hide_render,
         "colls": [c.name for c in o.users_collection], "props": {k: str(o[k]) for k in o.keys()}}
    if o.type == "MESH":
        bb = [o.matrix_world @ __import__("mathutils").Vector(c) for c in o.bound_box]
        e["bbox_ft"] = [r([min(v[i] for v in bb) / F for i in range(3)], 3), r([max(v[i] for v in bb) / F for i in range(3)], 3)]
        e["npoly"] = len(o.data.polygons)
    if o.type == "LIGHT": e["light"] = [o.data.type, o.data.energy, r(o.data.color)]
    if o.type == "CAMERA": e["lens"] = o.data.lens
    d["objects"][o.name] = e
for m in bpy.data.materials:
    vals = {}
    if m.use_nodes:
        for n in m.node_tree.nodes:
            for i in n.inputs:
                if hasattr(i, "default_value"):
                    try: vals[n.name + "." + i.name] = r(i.default_value, 4) if hasattr(i.default_value, "__len__") else round(float(i.default_value), 4)
                    except Exception: pass
    d["materials"][m.name] = vals
json.dump(d, open(out, "w"), indent=0)
print("DUMPED", out, len(d["objects"]))
