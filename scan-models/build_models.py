"""Blender headless: turn each generated GLB into an organised .blend, a scaled GLB export and a preview render.

    /Applications/Blender.app/Contents/MacOS/Blender -b -P scan-models/build_models.py -- scan-models [slug ...]

Per model: one collection CP_<slug> with applied transforms, base centred on the origin at Z=0, scaled to the target
in objects.json (basis recorded as a custom property), mesh objects renamed <slug>_NN. Outputs:
blend/<slug>.blend, glb/<slug>.glb, previews/<slug>.png (camera 2.6x the largest dimension away, front view).
"""
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
ROOT = Path(argv[0]).resolve()
AZ_SCAN = "--az-scan" in argv  # render four azimuths to previews_scan/ instead of building, to choose objects.json azimuth
only = set(a for a in argv[1:] if not a.startswith("--"))
CHAIN = ["tripo_h31", "trellis2", "rodin_v25", "hunyuan_pro", "meshy_71"]
RES = 800


def winners():
    state = {}
    for line in (ROOT / "ledger.jsonl").read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            state.setdefault((r["model"], r["image_id"]), {}).update(r)
    out = {}
    for (m, i), r in state.items():
        if r.get("status") == "completed" and (ROOT / r["output_path"]).exists():
            if i not in out or CHAIN.index(m) < CHAIN.index(out[i][0]):
                out[i] = (m, ROOT / r["output_path"])
    return out


def bounds(meshes):
    lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
    for o in meshes:
        for c in o.bound_box:
            p = o.matrix_world @ Vector(c)
            lo = Vector(map(min, lo, p)); hi = Vector(map(max, hi, p))
    return lo, hi


def import_and_normalise(glb, obj):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=str(glb))
    imported = [o for o in bpy.context.scene.objects if o not in before]
    meshes = [o for o in imported if o.type == "MESH"]
    lo, hi = bounds(meshes)
    size = hi - lo
    target = obj["scale"]["metres"]
    ref = size.z if obj["scale"]["dim"] == "height" else max(size)
    s = target / ref
    ctr = (lo + hi) / 2
    tri = 0
    for o in meshes:
        mw = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = mw
    for o in imported:
        if o.type != "MESH":
            bpy.data.objects.remove(o, do_unlink=True)
    coll = bpy.data.collections.new(f"CP_{obj['slug']}")
    bpy.context.scene.collection.children.link(coll)
    for n, o in enumerate(sorted(meshes, key=lambda x: x.name), 1):
        o.name = f"{obj['slug']}_{n:02d}"
        o.data.name = o.name
        for c in list(o.users_collection):
            c.objects.unlink(o)
        coll.objects.link(o)
        o.scale = o.scale * s
        o.location = (o.location - Vector((ctr.x, ctr.y, lo.z))) * s
        bpy.context.view_layer.objects.active = o
        o.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        # location was moved by the same factor; bake it into the vertices so the origin sits at the base centre
        o.data.transform(__import__("mathutils").Matrix.Translation(o.location))
        o.location = (0, 0, 0)
        tri += sum(len(p.vertices) - 2 for p in o.data.polygons)
        o.select_set(False)
    lo2, hi2 = bounds(meshes)
    return meshes, coll, tri, (hi2 - lo2)


def render_preview(meshes, dest, az):
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            sc.render.engine = eng
            break
        except TypeError:
            continue
    sc.render.resolution_x = sc.render.resolution_y = RES
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("w"); w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.42, 0.43, 0.46, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.7
    sc.world = w
    lo, hi = bounds(meshes)
    D = max(hi - lo)
    rig = bpy.data.collections.new("preview_rig"); sc.collection.children.link(rig)
    def put(o):
        rig.objects.link(o)
    for name, rot, e in (("key", (math.radians(50), 0, math.radians(35)), 2.2),
                         ("fill", (math.radians(65), 0, math.radians(-120)), 0.8)):
        d = bpy.data.lights.new(name, "SUN"); d.energy = e
        o = bpy.data.objects.new(name, d); o.rotation_euler = rot; put(o)
    a = bpy.data.lights.new("top", "AREA"); a.energy = 120 * (D / 2) ** 2; a.size = 3 * D
    o = bpy.data.objects.new("top", a); o.location = (0, 0, 3 * D); put(o)
    bpy.ops.mesh.primitive_plane_add(size=6 * D, location=(0, 0, 0))
    g = bpy.context.active_object
    for c in list(g.users_collection):
        c.objects.unlink(g)
    put(g)
    m = bpy.data.materials.new("g"); m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.22, 0.22, 0.23, 1)
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    g.data.materials.append(m)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); put(cam)
    cam.data.lens = 60; cam.data.clip_end = 100 * D
    sc.camera = cam
    r = 2.6 * D
    cam.location = (r * math.sin(math.radians(az)), -r * math.cos(math.radians(az)), 0.95 * D)
    cam.rotation_euler = (Vector((0, 0, 0.5 * D)) - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = str(dest)
    bpy.ops.render.render(write_still=True)
    return rig


objects = {o["slug"]: o for o in json.loads((ROOT / "objects.json").read_text())}
for d in ("blend", "glb", "previews"):
    (ROOT / d).mkdir(exist_ok=True)
for slug, (model, glb) in sorted(winners().items()):
    if only and slug not in only:
        continue
    obj = objects[slug]
    try:
        meshes, coll, tri, dims = import_and_normalise(glb, obj)
    except Exception as e:
        print("BUILD FAIL", slug, e, flush=True)
        continue
    if AZ_SCAN:
        (ROOT / "previews_scan").mkdir(exist_ok=True)
        for az in (0, 90, 180, 270):
            rig = render_preview(meshes, ROOT / "previews_scan" / f"{slug}_{az}.png", az)
            bpy.data.collections.remove(rig)
        print("SCANNED", slug, flush=True)
        continue
    coll["source_image"] = obj["source"]
    coll["source_crop"] = json.dumps(obj["crop"])
    coll["generator"] = model
    coll["scale_basis"] = obj["scale"]["basis"]
    coll["scale_target_m"] = f"{obj['scale']['dim']} = {obj['scale']['metres']}"
    coll["assumptions"] = " | ".join(obj["assumptions"])
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes:
        o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(ROOT / "glb" / f"{slug}.glb"), export_format="GLB", use_selection=True)
    rig = render_preview(meshes, ROOT / "previews" / f"{slug}.png", obj["azimuth"])
    bpy.data.collections.remove(rig)  # keep the .blend asset-only; the preview rig is not part of the model
    for o in list(bpy.data.objects):
        if o.users == 0:
            bpy.data.objects.remove(o)
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "blend" / f"{slug}.blend"))
    print("BUILT", slug, model, f"{tri} tris", tuple(round(v, 2) for v in dims), flush=True)
