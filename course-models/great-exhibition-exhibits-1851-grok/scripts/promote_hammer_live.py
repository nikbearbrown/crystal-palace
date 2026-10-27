"""KEEP hammer model: promote HAM_cand* enrich from e02_hammer into live e02.
Does NOT change the outdoor showroom setting (court is a separate candidate).
  blender -b rounds/e02.blend -P scripts/promote_hammer_live.py
"""
import bpy, os, shutil
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CAND = os.path.join(ROOT, "rounds/candidates/e02_hammer.blend")
LIVE = os.path.join(ROOT, "rounds/e02.blend")
if not os.path.isfile(CAND):
    raise SystemExit("missing " + CAND)

bak = LIVE + ".pre_hammer_keep"
if not os.path.isfile(bak):
    shutil.copy2(LIVE, bak)

# Open candidate (has enrich); strip court-unrelated candidate flags; save as live.
# Keep outdoor cams as in candidate for now (live outdoor); court cand will reframe.
bpy.ops.wm.open_mainfile(filepath=CAND)

# Remove any court objects if present (shouldn't be)
for o in list(bpy.data.objects):
    if o.name.startswith("MC_"):
        bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections):
    if c.name.startswith("MC_"):
        bpy.data.collections.remove(c)

for o in bpy.data.objects:
    if o.name.startswith("HAM_cand"):
        o["keep"] = "CP024_hammer_model"
        if "candidate" in o:
            del o["candidate"]
    if o.name.startswith("CP024_") and "candidate" in o:
        # live keeps candidate cam pull-back until court KEEP; strip flag, tag keep-model
        del o["candidate"]
        o["keep_model"] = "CP024_hammer"

txt = bpy.data.texts.get("CREDIT_HAM_KEEP") or bpy.data.texts.new("CREDIT_HAM_KEEP")
txt.clear()
txt.write(
    "KEEP CP024 Nasmyth hammer MODEL (2026-10-27)\n"
    "Promoted enrich from rounds/candidates/e02_hammer.blend into live e02:\n"
    "cylinder flanges/bolts, valve chest+linkage, ram slippers, frame boltheads, die face.\n"
    "Setting still outdoor showroom — court interior is a separate CANDIDATE.\n"
)

bpy.ops.wm.save_as_mainfile(filepath=LIVE)
print("PROMOTED_HAMMER_MODEL", LIVE, flush=True)
