"""Place hero-exhibit assets into ANY open scene as collection instances, without editing that scene's source file.
Run inside another .blend, before its own render script (the host file is never saved by this script):
  blender -b HOST.blend -P place_exhibits.py -P HOST_render.py -- --lib rounds/e01.blend \
      --place "EXH_KOHINOOR:120,0,0,0;EXH_NASMYTH_HAMMER:-456,4,0,0" --pcam "PL_koh:128,-22,5.25:120,0,5:35"
  --place  NAME:x,y,z,rot_deg (feet; host floor assumed z=0 unless given)   --pcam NAME:pos:look:lens (eye ft, no roll)
  --hide-clash : hide (render only) host crowd/props standing inside a footprint.
  --clear-sightlines : hide (render only) loose crowd figures within 2.5 ft of a camera->asset sightline.
  --check-only : report what in the host intersects each asset's footprint and exit without rendering or saving.
Assets are APPENDED (local copy in memory) from the library file; the library itself is only read."""
import bpy, sys, os, math, json
from mathutils import Vector
FT = 0.3048
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
lib = os.path.abspath(arg("--lib")); sc = bpy.context.scene
places = [p.split(":") for p in arg("--place", "").split(";") if p]
def foot(name):   # footprint half-extents (ft) from the asset's dims
    return {"EXH_KOHINOOR": (7.0, 7.0), "EXH_OSLER_CANDELABRUM": (2.2, 2.2), "EXH_NASMYTH_HAMMER": (11.2, 7.2)}.get(name, (5, 5))
def clashes(name, x, y, rz):
    hx, hy = foot(name)
    if abs(math.sin(math.radians(rz))) > 0.7: hx, hy = hy, hx
    out = []
    for o in sc.objects:
        if o.type != 'MESH' or o.get("placed_exhibit") or "floor" in o.name.lower() or "ground" in o.name.lower(): continue
        cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
        lo = [min(c[i] for c in cs) / FT for i in range(3)]; hi = [max(c[i] for c in cs) / FT for i in range(3)]
        if hi[2] < 0.05 or lo[2] > 20: continue
        if lo[0] < x + hx and hi[0] > x - hx and lo[1] < y + hy and hi[1] > y - hy:
            # big objects (roofs, whole-floor meshes) only clash if their mesh actually has vertices in the footprint
            if (hi[0] - lo[0]) * (hi[1] - lo[1]) > 4 * hx * hy * 6:
                M = o.matrix_world; n = 0
                for v in o.data.vertices:
                    w = M @ v.co
                    if abs(w.x / FT - x) < hx and abs(w.y / FT - y) < hy and 0.05 < w.z / FT < 20: n += 1; break
                if not n: continue
            out.append(o.name)
    return out
report = {}
for nm, xyz in places:
    x, y, z, rz = (list(map(float, xyz.split(","))) + [0, 0])[:4]
    report[nm] = clashes(nm, x, y, rz)
    if "--hide-clash" in argv:
        for n in report[nm]:   # render-time only (host never saved); only loose crowd figures, never props/statues/machines
            if n.upper().startswith(("CROWD", "VIS", "FIG")): sc.objects[n].hide_render = True
        print("PLACE_HIDDEN", nm, [n for n in report[nm] if n.upper().startswith(("CROWD", "VIS", "FIG"))], flush=True)
print("PLACE_CLASHES", json.dumps(report), flush=True)
if "--check-only" in argv:
    print("PLACE_CHECK_ONLY: nothing placed, nothing saved", flush=True)
else:
    need = sorted({p[0] for p in places})
    with bpy.data.libraries.load(lib, link=False) as (src, dst):
        dst.collections = [c for c in src.collections if c in need]
    holder = bpy.data.collections.new("PLACED_EXHIBITS_grok"); sc.collection.children.link(holder)
    store = bpy.data.collections.new("PLACED_EXHIBIT_SOURCES_grok"); sc.collection.children.link(store)
    for c in dst.collections: store.children.link(c)
    bpy.context.view_layer.layer_collection.children[store.name].exclude = True
    for nm, xyz in places:
        x, y, z, rz = (list(map(float, xyz.split(","))) + [0, 0])[:4]
        e = bpy.data.objects.new("PLACED_" + nm, None); e.instance_type = 'COLLECTION'; e.instance_collection = bpy.data.collections[nm]
        e.location = (x * FT, y * FT, z * FT); e.rotation_euler = (0, 0, math.radians(rz)); e["placed_exhibit"] = True; e["credit"] = "Grok Bot exhibits"
        holder.objects.link(e)
    for spec in [s for s in arg("--pcam", "").split(";") if s]:
        n, p, l, lens = spec.split(":"); p = Vector(tuple(float(v) * FT for v in p.split(","))); l = Vector(tuple(float(v) * FT for v in l.split(",")))
        cd = bpy.data.cameras.new(n); cd.lens = float(lens); cd.sensor_width = 36; cd.clip_start = 0.05; cd.clip_end = 4000
        co = bpy.data.objects.new(n, cd); co.location = p; co.rotation_euler = (l - p).to_track_quat('-Z', 'Y').to_euler(); holder.objects.link(co)
    if "--clear-sightlines" in argv:   # render-time only: loose crowd figures standing on a camera->asset sightline (2.5 ft corridor)
        cams = [(spec.split(":")[0], Vector(tuple(float(v) for v in spec.split(":")[1].split(",")))) for spec in arg("--pcam", "").split(";") if spec]
        hid = []
        for o in sc.objects:
            if o.type != 'MESH' or not o.name.upper().startswith(("CROWD", "VIS", "FIG")): continue
            q = Vector((o.matrix_world.translation.x / FT, o.matrix_world.translation.y / FT))
            for cn, cp in cams:
                a = Vector((cp.x, cp.y))
                for nm, xyz in places:
                    x, y = map(float, xyz.split(",")[:2]); b = Vector((x, y)); d = b - a
                    t = max(0.0, min(1.0, (q - a).dot(d) / d.length_squared))
                    if (a + d * t - q).length < 2.5 and (b - a).length < 80: o.hide_render = True; hid.append(o.name)
        print("PLACE_SIGHTLINE_HIDDEN", sorted(set(hid)), flush=True)
    if arg("--frame"): sc.frame_set(int(arg("--frame")))
    print("PLACED", [p[0] for p in places], flush=True)
