"""CP031 key-strike candidate (2026-11-02, Grok, no verdict).

blender -b rounds/d04_dismantle.blend -P scripts/candidate_cp031_strike.py -- [--out rounds/candidates/d04_cp031strike.blend]

Opens the LIVE d04 blend read-only, swaps the r09 stand-in striker + bolt-on arm rods for a people_lib v3.4
1850s workman in a scripted contact-strike pose with a re-hung maul, and saves a SIBLING blend.
The live d04_dismantle.blend is never written.
"""
import os, sys, json, argparse
import bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cp031_striker as S

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser(); ap.add_argument("--out", default="rounds/candidates/d04_cp031strike.blend")
ap.add_argument("--man", default="181.55,-153.0")  # centre of the live trestle deck (DM17)
a = ap.parse_args(argv)
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(here, a.out) if not os.path.isabs(a.out) else a.out
assert os.path.abspath(out) != os.path.abspath(bpy.data.filepath), "refusing to overwrite the live blend"

old_st = bpy.data.objects["D_STAFF_STRIKER"]; old_ma = bpy.data.objects["D_MAUL"]
coll_staff = old_st.users_collection[0]; coll_sup = old_ma.users_collection[0]
cast = old_ma.data.materials[0]
ash = None
for nm in ("D_SHORES", "D_TRESTLE_STAGE", "D_SCAFFOLD_JOINT"):
    o = bpy.data.objects.get(nm)
    if o:
        for m in o.data.materials:
            if m and any(k in m.name.lower() for k in ("oak", "plank", "timber", "wood")):
                ash = m; break
    if ash: break
ash = ash or old_ma.data.materials[-1]
print("CP031 mats", cast.name, ash.name, "colls", coll_staff.name, coll_sup.name)
for o in (old_st, old_ma):
    bpy.data.objects.remove(o, do_unlink=True)
jx, jy = 180.0, -156.0
key_box = (jx + 0.55, jx + 0.72, jy - 0.07, jy + 0.07, 20.9, 23.0)
mx, my = (float(v) for v in a.man.split(","))
st, ma, info = S.build(None, coll_staff, coll_sup, [cast, ash], (mx, my), 16.0, key_box)
print("CP031_INFO " + json.dumps(info))
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True)
print("CP031 saved", out)
