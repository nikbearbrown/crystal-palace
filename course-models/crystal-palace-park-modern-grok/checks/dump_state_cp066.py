"""dump object state (name, type, matrix, hide_render, light energy, cam lens) of the opened blend to json: -- OUT.json"""
import bpy, json, sys
out = sys.argv[sys.argv.index("--") + 1]
d = {}
for o in bpy.data.objects:
    e = {"type": o.type, "m": [round(v, 5) for r in o.matrix_world for v in r], "hide_render": o.hide_render, "tag": "cp066_nsc" in o.keys()}
    if o.type == "LIGHT": e["energy"] = o.data.energy; e["color"] = list(o.data.color)
    if o.type == "CAMERA": e["lens"] = o.data.lens
    d[o.name] = e
sc = bpy.context.scene
d["__scene__"] = {"exposure": sc.view_settings.exposure, "vt": sc.view_settings.view_transform, "world": sc.world.name, "res": [sc.render.resolution_x, sc.render.resolution_y], "spp": sc.cycles.samples}
json.dump(d, open(out, "w"))
