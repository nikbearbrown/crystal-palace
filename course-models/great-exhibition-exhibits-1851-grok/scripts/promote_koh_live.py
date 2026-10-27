"""KEEP: promote e02_koh_v2 candidate into live rounds/e02.blend.
Applies the kept Koh changes in place on live e02 (or copies from candidate).
  blender -b rounds/e02.blend -P scripts/promote_koh_live.py
"""
import bpy, bmesh, math, os, sys, shutil
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
I = 0.0254; FT = 0.3048
CAND = os.path.join(ROOT, "rounds/candidates/e02_koh_v2.blend")
LIVE = os.path.join(ROOT, "rounds/e02.blend")

# Prefer copying the KEEP candidate over live (it already has all geometry/cam)
# then strip candidate flags and write CREDIT.
if not os.path.isfile(CAND):
    raise SystemExit("missing " + CAND)

# Backup live
bak = LIVE + ".pre_koh_keep"
if not os.path.isfile(bak):
    shutil.copy2(LIVE, bak)

bpy.ops.wm.open_mainfile(filepath=CAND)

# Strip candidate markers; tag keep
for o in bpy.data.objects:
    if "candidate" in o:
        del o["candidate"]
    if o.name.startswith("KOH_cand2") or o.name in ("KOH_diamond",) or o.name.startswith("KOH_cand"):
        o["keep"] = "CP025_koh_v2"
        o["credit"] = o.get("credit") or "Grok Bot; KEEP CP025 koh v2 (open south, reframe, sparkle)"

cam = bpy.data.objects.get("CP025_july_start")
if cam:
    cam["keep"] = "CP025_koh_v2"
    if "candidate" in cam:
        del cam["candidate"]

txt = bpy.data.texts.get("CREDIT_KOH_KEEP") or bpy.data.texts.new("CREDIT_KOH_KEEP")
txt.clear()
txt.write(
    "KEEP CP025 Koh-i-Noor v2 (2026-10-27)\n"
    "Promoted from rounds/candidates/e02_koh_v2.blend.\n"
    "Open-south July tent (three-wall crimson); OSL_shaft_prisms + KOH_gas_pipes hidden;\n"
    "CP025_july_start 50 mm / eye 5.25 ft / no roll; whole cage; rose-cut 3.5x + emission sparkle.\n"
    "Muse glass-topped-display-counter skipped (EX_KOH_COUNTER).\n"
)

bpy.ops.wm.save_as_mainfile(filepath=LIVE)
print("PROMOTED", LIVE, flush=True)
