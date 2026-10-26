"""Count what is in a Crystal Palace .blend: placed parts by kind, library meshes, evaluated triangles with instances, materials, extent.
  blender --background model.blend --python stats.py -- OUT.json     (never saves the .blend)"""
import json, sys, collections
import bpy
from mathutils import Vector
out = sys.argv[sys.argv.index("--") + 1]
dg = bpy.context.evaluated_depsgraph_get()
FT = 0.3048
kinds = collections.Counter(); per_coll = collections.Counter(); insts = []
for o in bpy.data.objects:
    if o.get("part_kind"):
        kinds[o["part_kind"]] += 1
        if o.instance_type == "COLLECTION" and o.instance_collection:
            per_coll[o.instance_collection.name] += 1; insts.append(o)
        else:
            per_coll["(mesh object)"] += 1
lib_tris, lib_bbox = {}, {}
for name in per_coll:
    c = bpy.data.collections.get(name)
    if not c: continue
    t = 0; pts = []
    for ob in c.all_objects:
        if ob.type != "MESH": continue
        ev = ob.evaluated_get(dg); me = ev.to_mesh()
        t += sum(len(p.vertices) - 2 for p in me.polygons)
        mw = ob.matrix_world
        pts += [mw @ Vector(v) for v in ob.bound_box]
        ev.to_mesh_clear()
    lib_tris[name] = t; lib_bbox[name] = pts
tot = sum(lib_tris.get(n, 0) * k for n, k in per_coll.items() if n in lib_tris)
mesh_objs_loose = [o for o in bpy.data.objects if o.type == "MESH" and o.get("part_kind")]
for o in mesh_objs_loose:
    ev = o.evaluated_get(dg); me = ev.to_mesh(); tot += sum(len(p.vertices) - 2 for p in me.polygons); ev.to_mesh_clear()
mn = Vector((1e9,) * 3); mx = Vector((-1e9,) * 3)
for o in insts:
    for v in lib_bbox.get(o.instance_collection.name, []):
        w = o.matrix_world @ v
        mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
for o in mesh_objs_loose:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c); mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
lib_meshes = sum(1 for n in lib_tris for ob in bpy.data.collections[n].all_objects if ob.type == "MESH")
d = dict(blender=bpy.app.version_string, parts=sum(kinds.values()), kinds=dict(kinds), library_collections=len(lib_tris),
         library_mesh_objects=lib_meshes, library_triangles={k: v for k, v in lib_tris.items()},
         instances_per_collection=dict(per_coll), triangles_instanced_total=tot,
         materials=len(bpy.data.materials), material_names=[m.name for m in bpy.data.materials],
         extent_ft=dict(x=[mn.x / FT, mx.x / FT], y=[mn.y / FT, mx.y / FT], z=[mn.z / FT, mx.z / FT],
                        length=(mx.x - mn.x) / FT, width=(mx.y - mn.y) / FT, height=(mx.z - mn.z) / FT),
         unit_scale=bpy.context.scene.unit_settings.scale_length, objects_total=len(bpy.data.objects))
json.dump(d, open(out, "w"), indent=1)
print("STATS", d["parts"], d["triangles_instanced_total"], d["extent_ft"]["length"], d["extent_ft"]["width"], d["extent_ft"]["height"])
