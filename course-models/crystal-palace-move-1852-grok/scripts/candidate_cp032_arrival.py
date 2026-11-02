"""CP032 arrival hands (2026-11-02, Grok): CANDIDATE, no verdict. Dressed 1852 receiving gang at the Sydenham
(Penge Place) arrival stack.

blender -b rounds/m02.blend -P scripts/candidate_cp032_arrival.py -- [--out rounds/candidates/m02_cp032arrival.blend]

Opens LIVE m02 read-only and replaces the five Sydenham arrival stand-ins STAFF_07..11 (r-era box/lathe mannequins:
two of the workmen wear silk top hats and the clerk renders as a pale robe; the shared people swap skips them as
close-ups) with survey people_lib v3.4 HBM hero figures, the same recipe as the KEEP departure hands (MV15):
three `1850s_workman`, one `1850s_navvy` (the 1852 site was being dug and levelled) and one `1850s_gentleman` for the
contractor's clerk who checks the delivery off. Each figure keeps its stand-in's floor position and heading; its
feet are dropped by a downward ray onto the ARR_GRASS / ARR_CLAY surface (the arrival yard slopes, so z=0 is wrong
here). Workmen's smocks and waistcoats take the CP032 departure dark matte fustian; the clerk takes the same black
frock coat and silk hat. Objects are named ARR_HAND_* so the render-time people swap leaves them alone.
Saves a SIBLING blend; live rounds/m02.blend is never written. Sydenham 1852 site only: nothing from the Hyde Park
building is added (figures are period dress only).
Prints `CP032_ARR_INFO {json}` and `CP032_ARR_HANDS_IN_PLACE True|False`.
"""
import os, sys, json, argparse
import bpy
from mathutils import Vector
sys.path.insert(0, "/workspace/crystal-palace-survey/people")
import people_lib as P

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser(); ap.add_argument("--out", default="rounds/candidates/m02_cp032arrival.blend")
a = ap.parse_args(argv)
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(here, a.out) if not os.path.isabs(a.out) else a.out
assert os.path.abspath(out) != os.path.abspath(bpy.data.filepath), "refusing to overwrite the opened blend"

# stand-in -> (role, pose). STAFF_07/08 stand at the wagon tail, 09 at the column stack, 10 by the spoil, 11 clerk.
CAST = {
    "STAFF_07_workman": ("1850s_workman", "working"),
    "STAFF_08_workman": ("1850s_workman", "standing"),
    "STAFF_09_workman": ("1850s_workman", "working"),
    "STAFF_10_workman": ("1850s_navvy", "standing"),
    "STAFF_11_clerk":   ("1850s_gentleman", "standing"),
}
FUSTIAN = {"blue": (0.030, 0.042, 0.075), "grey": (0.050, 0.050, 0.048), "drab": (0.040, 0.044, 0.034)}
CLERK = {"coat": (0.016, 0.015, 0.015), "hat": (0.010, 0.010, 0.011)}
GROUND = ("ARR_GRASS", "ARR_CLAY")


def _mat(name, rgb, rough=0.95):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True; b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*rgb, 1.0); b.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.2
    if "Sheen Weight" in b.inputs: b.inputs["Sheen Weight"].default_value = 0.0
    m.diffuse_color = (*rgb, 1.0); return m


FM = {k: _mat("CP032C_fustian_" + k, c) for k, c in FUSTIAN.items()}   # same datablocks/values as MV15
CM = {"coat": _mat("CP032C_clerk_coat", CLERK["coat"], 0.9), "hat": _mat("CP032C_clerk_hat", CLERK["hat"], 0.55)}


def ground_z(x, y):
    """highest ARR_GRASS/ARR_CLAY surface under (x, y), world metres"""
    best = None
    for gn in GROUND:
        g = bpy.data.objects[gn]; mi = g.matrix_world.inverted()
        o = mi @ Vector((x, y, 200.0)); d = (mi.to_3x3() @ Vector((0, 0, -1))).normalized()
        ok, loc, nor, idx = g.ray_cast(o, d)
        if ok:
            z = (g.matrix_world @ loc).z
            best = z if best is None else max(best, z)
    assert best is not None, (x, y)
    return best


def hands_in_place():
    hands = [o for o in bpy.data.objects if o.name.startswith("ARR_HAND_")]
    return len(hands) == len(CAST) and not any(n in bpy.data.objects for n in CAST)


info = {}
for i, (nm, (role, pose)) in enumerate(CAST.items()):
    old = bpy.data.objects[nm]
    coll = old.users_collection[0]
    loc = old.matrix_world.translation.copy(); yaw = old.matrix_world.to_euler().z
    tmpn = "CP032A_TMP_%02d" % i
    me = P.person_mesh(tmpn, role.split("_")[1], style={"role": role}, pose=pose, lod="hero", seed=1852132 + 7 * i)
    tmp = bpy.data.objects.get(tmpn)
    me = me.copy(); me.name = "cp032_arr_hand_%02d" % i
    if tmp is not None:
        bpy.data.objects.remove(tmp, do_unlink=True)
    for si, m in enumerate(me.materials):
        if not m: continue
        if role.split("_")[1] in ("workman", "navvy") and (m.name.startswith("CPL3_smock") or m.name.startswith("CPL3_waist")):
            me.materials[si] = FM[list(FUSTIAN)[i % 3]]
        elif role.endswith("gentleman") and m.name.startswith("CPL3_coat"):
            me.materials[si] = CM["coat"]
        elif role.endswith("gentleman") and m.name.startswith("CPL3_hat"):
            me.materials[si] = CM["hat"]
    names = [m.name if m else "" for m in me.materials]
    if pose == "standing" and any(n.startswith("CPL3_skin") for n in names):
        sk = next(k for k, n in enumerate(names) if n.startswith("CPL3_skin"))
        for poly in me.polygons:   # v3.4 hero hands carry the trouser slot (read as dark gloves); MV15 fix
            if abs(poly.center.x) > 0.40 and names[poly.material_index].startswith("CPL3_trou"):
                poly.material_index = sk
    zmin = min(v.co.z for v in me.vertices)
    old_z = loc.z
    bpy.data.objects.remove(old, do_unlink=True)
    gz = ground_z(loc.x, loc.y)
    ob = bpy.data.objects.new("ARR_HAND_%02d_%s" % (i, role.split("_")[1]), me)
    coll.objects.link(ob)
    ob.location = (loc.x, loc.y, gz - zmin)
    ob.rotation_euler = (0, 0, yaw)
    ob["cp032_role"] = role; ob["cp032_pose"] = pose; ob["part_kind"] = "figure_hero"
    hz = max(v.co.z for v in me.vertices) - zmin
    info[ob.name] = {"from": nm, "xy": [round(loc.x, 2), round(loc.y, 2)], "yaw_deg": round(yaw * 57.2958, 1),
                     "height_m": round(hz, 3), "ground_z": round(gz, 3), "standin_z": round(old_z, 3)}
print("CP032_ARR_INFO " + json.dumps(info))
print("CP032_ARR_HANDS_IN_PLACE", hands_in_place())
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True)
print("CP032_ARR saved", out)
