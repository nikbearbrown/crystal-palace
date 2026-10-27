"""D-checks for CP068 legacy-today. blender -b rounds/m03_legacy.blend -P scripts/check_legacy_today.py -- --out checks/m03_checks.json"""
import bpy, sys, os, json, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
out = argv[argv.index("--out") + 1] if "--out" in argv else "checks/m03_checks.json"
R = []; O = bpy.data.objects
def chk(name, ok, detail=""):
    R.append({"name": name, "pass": bool(ok), "detail": detail})
info = json.loads(bpy.context.scene.get("grok_move", "{}"))
chk("has_kjoint", "K_CONNECTING_PIECE" in O, "connecting piece present")
chk("has_bay", "BAY_FRAME" in O, "prefab bay present")
chk("has_park_ground", "TODAY_GRASS" in O)
# eye height ~5.25 ft on cams
for c in [o for o in O if o.type == 'CAMERA']:
    z_ft = c.location.z / 0.3048
    chk(f"eye_{c.name}", 5.0 <= z_ft <= 5.6, f"z_ft={z_ft:.2f}")
    # no roll: rotation roughly from track-to
    roll = abs(c.rotation_euler.y)
    chk(f"noroll_{c.name}", roll < 0.05, f"ry={roll:.4f}")
# clearance: kit cam not inside geometry (distance to origin > 1 ft)
cam = O.get("CP068_kit_start")
if cam:
    d = cam.location.length / 0.3048
    chk("kit_clearance", d >= 3.0, f"dist_ft={d:.2f}")
# bay span ~24 ft
chk("bay_span_note", info.get("bay", {}).get("span_ft") == 24, str(info.get("bay")))
res = {"set": "LEGACY_TODAY_CP068", "passed": sum(r["pass"] for r in R), "total": len(R), "checks": R}
os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
json.dump(res, open(out, "w"), indent=2)
print("CHECKS", res["passed"], "/", res["total"], flush=True)
