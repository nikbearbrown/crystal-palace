"""KEEP CP024 Machinery Court stand dressing (2026-11-02; parent viewed all three pairs:
approach_start, approach_end, ram_start). Promotes rounds/candidates/e02_machinery_dress.blend
(built by polish_machinery_dress.py, boiler placard nudged +1.0 ft east) to live rounds/e02.blend.
Backs up the old live once to rounds/e02.blend.pre_machinery_keep (untracked; == git 5c4b55d e02).
Only retags (candidate -> keep) and renames the credit text; no geometry, material or camera change.
  blender -b -P scripts/promote_machinery_live.py
"""
import bpy, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CAND = os.path.join(ROOT, "rounds/candidates/e02_machinery_dress.blend")
LIVE = os.path.join(ROOT, "rounds/e02.blend")
BAK = LIVE + ".pre_machinery_keep"
if not os.path.isfile(CAND): raise SystemExit("missing " + CAND)
if not os.path.isfile(BAK): shutil.copy2(LIVE, BAK)
bpy.ops.wm.open_mainfile(filepath=CAND)
n = 0
for o in bpy.data.objects:
    if o.get("candidate") == "e02_machinery_dress":
        del o["candidate"]; o["keep"] = "CP024_machinery_dress"; n += 1
c = bpy.data.collections.get("MCD_MACHINERY_DRESS_1851")
if c is not None and c.get("candidate") == "e02_machinery_dress":
    del c["candidate"]; c["keep"] = "CP024_machinery_dress"
t = bpy.data.texts.get("CREDIT_MCD_CAND")
if t is not None:
    body = t.as_string().replace("CANDIDATE e02_machinery_dress", "KEEP CP024 machinery dressing (e02_machinery_dress)")
    t.name = "CREDIT_MCD_KEEP"; t.clear(); t.write(body + "KEEP 2026-11-02: approach_start/end + ram_start; boiler CLASS V placard +1.0 ft east.\n")
bpy.ops.wm.save_as_mainfile(filepath=LIVE, compress=False)
print("PROMOTED_MACHINERY", n, LIVE, flush=True)
