"""CANDIDATE: HP interior envelope east-nave seal + daylit for CP023 into_nave.

  blender -b rounds/r11.blend -P scripts/apply_envelope_r11.py -- \
      --out rounds/candidates/r11_envelope.blend
"""
import bpy, os, sys, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, "/workspace/crystal-palace-survey/envelope")
import hp_interior_envelope as ENV
importlib.reload(ENV)

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/r11_envelope.blend"
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "rounds/r11.blend"))

CAND = "HPE_envelope_r11"
# Hide park / outdoor leaks that show through open east
ENV.hide_outdoor_leaks()
for o in bpy.data.objects:
    n = o.name.lower()
    if "ground_park" in n or o.name == "GROUND_PARK":
        o.hide_render = True
        o.hide_viewport = True
        print("HIDE", o.name, flush=True)

# Extend nave +X on 24 ft grid with glazed end; reuse host west structure
ENV.extend_host_east_nave(
    x_start=156.0, x_end=252.0, y_min=-72.0, y_max=72.0, candidate=CAND,
)
ENV.brighten_host_glass()
ENV.apply_daylit(bpy.context.scene, exposure=-0.7, sun_energy=3.36)

for cname in ("CP023_into_nave_start", "CP023_into_nave_end"):
    c = bpy.data.objects.get(cname)
    if c:
        c["candidate"] = CAND

txt = bpy.data.texts.get("CREDIT_HPE_R11") or bpy.data.texts.new("CREDIT_HPE_R11")
txt.clear()
txt.write(
    "CANDIDATE HP interior envelope on r11 (2026-10-27)\n"
    "Shared kit seals open east nave (156..252 ft) with glazed walls + ridge-and-furrow;\n"
    "GROUND_PARK hidden; host glass brightened; interior_daylit -0.7.\n"
    "Host transept / Muse Osler / Claude west nave untouched on disk (RO at render).\n"
)

bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out, flush=True)
