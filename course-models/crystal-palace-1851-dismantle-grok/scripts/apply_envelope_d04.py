"""CANDIDATE: HP interior envelope east-nave seal + daylit for CP030 aisle/walk.

  blender -b rounds/d04_empty.blend -P scripts/apply_envelope_d04.py -- \
      --out rounds/candidates/d04_envelope.blend
"""
import bpy, os, sys, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, "/workspace/crystal-palace-survey/envelope")
import hp_interior_envelope as ENV
importlib.reload(ENV)

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/d04_envelope.blend"
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "rounds/d04_empty.blend"))

CAND = "HPE_envelope_d04"
ENV.hide_outdoor_leaks()
for o in bpy.data.objects:
    if "ground_park" in o.name.lower() or o.name == "GROUND_PARK":
        o.hide_render = True
        o.hide_viewport = True
        print("HIDE", o.name, flush=True)

ENV.extend_host_east_nave(
    x_start=156.0, x_end=252.0, y_min=-72.0, y_max=72.0, candidate=CAND,
)
ENV.brighten_host_glass()
ENV.apply_daylit(bpy.context.scene, exposure=-0.7, sun_energy=3.36)

for cname in ("CP030_empty_walk_start", "CP030_empty_walk_end", "CP030_empty_aisle_start"):
    c = bpy.data.objects.get(cname)
    if c:
        c["candidate"] = CAND

txt = bpy.data.texts.get("CREDIT_HPE_D04") or bpy.data.texts.new("CREDIT_HPE_D04")
txt.clear()
txt.write(
    "CANDIDATE HP interior envelope on d04_empty (2026-10-27)\n"
    "Shared kit seals open east nave; GROUND_PARK hidden; interior_daylit -0.7.\n"
    "Shots: CP030_empty_walk, CP030_empty_aisle. Claude west nave RO.\n"
)

bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out, flush=True)
