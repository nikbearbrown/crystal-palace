"""CP032 departure hands (2026-11-02, Grok; KEEP 2026-11-02, live in m02): dressed 1852 dismantling gang.

blender -b rounds/m02.blend -P scripts/candidate_cp032_people.py -- [--out rounds/candidates/m02_cp032people.blend]
blender -b ROUND.blend -P scripts/candidate_cp032_people.py -- --live      # apply in place to a move round (KEEP)
Idempotent: if the round already carries the seven DEP_HAND_* figures and no STAFF_00..06 stand-ins it changes
nothing. Always ends by printing `CP032_HANDS_IN_PLACE True|False` (build_m02.sh asserts True).

Opens LIVE m02 read-only and replaces the seven Hyde Park departure stand-ins STAFF_00..06 (r-era box/lathe
mannequins; the shared people swap skips them as close-ups, so they still render as toys) with people_lib v3.4
HBM figures: six `1850s_workman` (cap, smock, trousers, boots) and one `1850s_gentleman` (frock coat + top hat)
for the clerk / contractor's agent who checks stock off. Each new figure keeps its stand-in's floor position and
heading; feet are dropped onto the ground plane (z=0). HBM A-pose arms are left as built (a scripted
arm-lowering pass was tried and dropped: it tore the sleeve shells). Workmen's smocks and
waistcoats take the same dark matte fustian as CP012/CP016 v3 (pale smocks read as bare torsos); the clerk takes a
black wool frock coat and black silk hat. Objects are named DEP_HAND_* so the render-time people
swap leaves them alone. Saves a SIBLING blend; live rounds/m02.blend is never written.
people_lib is imported read-only from the survey repo (the vendored copy in this folder carries someone else's
uncommitted edits and is not touched).
"""
import os, sys, json, argparse, math
import bpy
from mathutils import Vector, Matrix
sys.path.insert(0, "/workspace/crystal-palace-survey/people")
import people_lib as P

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser(); ap.add_argument("--out", default="rounds/candidates/m02_cp032people.blend")
ap.add_argument("--live", action="store_true", help="KEEP mode: write back into the opened blend (in place)")
a = ap.parse_args(argv)
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if a.live:
    out = os.path.abspath(bpy.data.filepath)
else:
    out = os.path.join(here, a.out) if not os.path.isabs(a.out) else a.out
    assert os.path.abspath(out) != os.path.abspath(bpy.data.filepath), "refusing to overwrite the opened blend without --live"

# stand-in -> (role, pose, extra yaw rad). Poses kept to standing/working: no load in hand, so no hauling mime.
CAST = {
    "STAFF_00_workman": ("1850s_workman", "standing", 0.0),
    "STAFF_01_workman": ("1850s_workman", "working", 0.0),
    "STAFF_02_workman": ("1850s_workman", "standing", 0.0),
    "STAFF_03_clerk":   ("1850s_gentleman", "standing", 0.0),
    "STAFF_04_workman": ("1850s_workman", "standing", 0.0),
    "STAFF_05_workman": ("1850s_workman", "working", 0.0),
    "STAFF_06_workman": ("1850s_workman", "standing", 0.0),
}
FUSTIAN = {"blue": (0.030, 0.042, 0.075), "grey": (0.050, 0.050, 0.048), "drab": (0.040, 0.044, 0.034)}
CLERK = {"coat": (0.016, 0.015, 0.015), "hat": (0.010, 0.010, 0.011)}


def _mat(name, rgb, rough=0.95):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True; b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*rgb, 1.0); b.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.2
    if "Sheen Weight" in b.inputs: b.inputs["Sheen Weight"].default_value = 0.0
    m.diffuse_color = (*rgb, 1.0); return m


FM = {k: _mat("CP032C_fustian_" + k, c) for k, c in FUSTIAN.items()}
CM = {"coat": _mat("CP032C_clerk_coat", CLERK["coat"], 0.9), "hat": _mat("CP032C_clerk_hat", CLERK["hat"], 0.55)}


def lower_arms(me, deg=17.0, radius=0.15):
    """Rotate each arm (incl. sleeve shells) about its shoulder toward the body. Weight ramps 0->1 over the first
    0.12 m of the arm axis, and only verts within `radius` of the shoulder->hand axis move (torso stays put)."""
    vs = me.vertices; zs = [v.co.z for v in vs]; z0 = min(zs); h = max(zs) - z0
    moved = 0
    for side in (1, -1):
        cand = [v.co for v in vs if side * v.co.x > 0.30 and v.co.z < z0 + 0.6 * h]
        hand = max(cand, key=lambda c: side * c.x).copy()
        S = Vector((side * 0.19, 0.0, z0 + 0.823 * h))
        ax = hand - S; L = ax.length; ax.normalize()
        R = Matrix.Rotation(math.radians(deg) * side, 3, 'Y')   # +x arm swings down/in about +Y
        for v in vs:
            d = v.co - S; t = d.dot(ax)
            if t < -0.02 or t > L + 0.30: continue
            if (d - ax * t).length > radius: continue
            if side * v.co.x < 0.15: continue
            w = max(0.0, min(1.0, t / 0.12)); w = w * w * (3 - 2 * w)
            v.co = S + (Matrix.Rotation(math.radians(deg) * side * w, 3, 'Y') @ d); moved += 1
    me.update(); return moved


def hands_in_place():
    hands = [o for o in bpy.data.objects if o.name.startswith("DEP_HAND_")]
    staff = [n for n in CAST if n in bpy.data.objects]
    return len(hands) == len(CAST) and not staff and all(abs(o.matrix_world.translation.z - o.location.z) < 1e-6 for o in hands)


already = hands_in_place()
if already:
    print("CP032 already applied: %d DEP_HAND_* present, no STAFF stand-ins; nothing changed" % len(CAST))
info = {}
for i, (nm, (role, pose, dyaw)) in enumerate([] if already else CAST.items()):
    old = bpy.data.objects[nm]
    coll = old.users_collection[0]
    loc = old.matrix_world.translation.copy(); yaw = old.matrix_world.to_euler().z + dyaw
    tmpn = "CP032_TMP_%02d" % i
    me = P.person_mesh(tmpn, role.split("_")[1], style={"role": role}, pose=pose, lod="hero", seed=1852032 + 7 * i)
    tmp = bpy.data.objects.get(tmpn)
    me = me.copy(); me.name = "cp032_hand_%02d" % i
    if tmp is not None:
        bpy.data.objects.remove(tmp, do_unlink=True)
    moved = 0   # arm lowering tried and dropped: tore sleeve shells and mangled hands (see DEPARTURES MV15)
    for si, m in enumerate(me.materials):
        if not m: continue
        if role.endswith("workman") and (m.name.startswith("CPL3_smock") or m.name.startswith("CPL3_waist")):
            me.materials[si] = FM[list(FUSTIAN)[i % 3]]
        elif role.endswith("gentleman") and m.name.startswith("CPL3_coat"):
            me.materials[si] = CM["coat"]
        elif role.endswith("gentleman") and m.name.startswith("CPL3_hat"):
            me.materials[si] = CM["hat"]
    # people_lib v3.4 hero hands carry the trouser slot (read as dark gloves); give standing hands the skin slot
    names = [m.name if m else "" for m in me.materials]
    if pose == "standing" and any(n.startswith("CPL3_skin") for n in names):
        sk = next(k for k, n in enumerate(names) if n.startswith("CPL3_skin"))
        for poly in me.polygons:
            if abs(poly.center.x) > 0.40 and names[poly.material_index].startswith("CPL3_trou"):
                poly.material_index = sk
    zmin = min(v.co.z for v in me.vertices)
    bpy.data.objects.remove(old, do_unlink=True)
    ob = bpy.data.objects.new("DEP_HAND_%02d_%s" % (i, role.split("_")[1]), me)
    coll.objects.link(ob)
    ob.location = (loc.x, loc.y, 0.0 - zmin)
    ob.rotation_euler = (0, 0, yaw)
    ob["cp032_role"] = role; ob["cp032_pose"] = pose
    hz = max(v.co.z for v in me.vertices) - zmin
    info[ob.name] = {"from": nm, "xy": [round(loc.x, 2), round(loc.y, 2)], "yaw_deg": round(yaw * 57.2958, 1),
                     "height_m": round(hz, 3), "feet_z": 0.0, "arm_verts_lowered": moved}
print("CP032_INFO " + json.dumps(info))
print("CP032_HANDS_IN_PLACE", hands_in_place())
if not already or not a.live:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True)
    print("CP032 saved", out)
