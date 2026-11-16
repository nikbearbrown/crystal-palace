"""CP050 candidate checks (2026-11-16). blender -b rounds/candidates/fb02_1895_cp050cup.blend -P checks/check_cp050_cupfinal.py -- --live rounds/fb02_1895.blend"""
import bpy, sys, json, math, os
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]; LIVE = argv[argv.index("--live") + 1]
CX, CY, CZ, GX, PL = -158.0, -598.0, -47.5, 55.0, 70.0; YD = 0.9144
res = []
def rec(w, ok, m, t=""): res.append({"check": w, "target": t, "measured": m, "pass": bool(ok)})
O = bpy.data.objects
cams = {o.name: (tuple(round(v, 5) for v in o.location), tuple(round(v, 5) for v in o.rotation_euler), o.data.lens) for o in O if o.type == 'CAMERA'}
with bpy.data.libraries.load(os.path.abspath(LIVE), link=False) as (src, dst): dst.objects = [n for n in src.objects if n.startswith(("CP050", "CP055"))]
for lo in dst.objects:
    if lo.type == 'CAMERA':
        base = lo.name[:-4] if lo.name.endswith(".001") else lo.name; c = cams.get(base)
        live = (tuple(round(v, 5) for v in lo.location), tuple(round(v, 5) for v in lo.rotation_euler), lo.data.lens)
        rec(f"camera {base} not moved vs live", c == live, str(c), str(live))
info = json.loads(bpy.context.scene["grok_build"])["cp050_candidate"]
rec("people total = 1895 attendance", info["people_total"] == 42560, info["people_total"], 42560)
rec("players", len([o for o in O if o.name.startswith(("FB95_villa_", "FB95_wba_")) and o.type == 'MESH']) == 22, 22, 22)
rec("officials", len([o for o in O if o.name.startswith(("FB95_referee", "FB95_linesman_")) and o.type == 'MESH' and "_stick" not in o.name and "_flag" not in o.name]) == 3, 3, 3)
for n in ("FB_Crowd_1895", "FB_Halfway"): rec(f"{n} hidden not deleted", n in O and O[n].hide_render, n in O, "present + hide_render")
rec("pitch visitors hidden", all(o.hide_render for o in O if o.name.startswith("FB_Hero_pitch_")), sum(o.hide_render for o in O if o.name.startswith("FB_Hero_pitch_")), 8)
rec("old goals hidden", all(o.hide_render for o in O if o.name.startswith(("FB_Post_", "FB_Bar_"))), "", "")
posts = [o for o in O if o.name.startswith("FB95_post_W")]
ys = sorted(sum((o.matrix_world @ Vector(c)).y for c in o.bound_box) / 8 for o in posts)
rec("goal width 8 yd (centres)", abs((ys[1] - ys[0]) - 8 * YD) < 0.01, round(ys[1] - ys[0], 3), round(8 * YD, 3))
bar = O["FB95_bar_W"]; bz = max((bar.matrix_world @ Vector(c)).z for c in bar.bound_box) - CZ
rec("crossbar 8 ft", abs(bz - 8 * 0.3048) < 0.01, round(bz, 3), round(8 * 0.3048, 3))
gx = sum((posts[0].matrix_world @ Vector(c)).x for c in posts[0].bound_box) / 8
rec("goals on the 70 m lines (x = CX-55)", abs(gx - (CX - GX)) < 0.01, round(gx, 3), CX - GX)
l12 = O["FB95_12yd_W"]; lx = sum((l12.matrix_world @ Vector(c)).x for c in l12.bound_box) / 8
rec("12 yd line", abs(lx - (CX - GX + 12 * YD)) < 0.01, round(lx - (CX - GX), 3), round(12 * YD, 3))
length, breadth = 2 * GX / YD, PL / YD
rec("1891 law length 100-200 yd", 100 <= length <= 200, round(length, 1), "100-200")
rec("1891 law breadth 50-100 yd", 50 <= breadth <= 100, round(breadth, 1), "50-100")
cr = O["FB95_Crowd_1895_cupfinal"]; pts = [v.co.copy() for v in cr.data.vertices]
inside = sum(1 for p in pts if CX - GX - 1.5 < p.x < CX + GX + 1.5 and CY - PL / 2 - 1.5 < p.y < CY + PL / 2 + 1.5)
rec("no crowd on the pitch (+1.5 m)", inside == 0, inside, 0)
cam = Vector((-158.0, -680.0)); wedge = sum(1 for p in pts if (Vector((p.x, p.y)) - cam).length < 9 and (Vector((p.x, p.y)) - cam).angle(Vector((0, 1)), 0) < math.radians(50) or (Vector((p.x, p.y)) - cam).length < 1.5)
rec("CP050 lens wedge clear (9 m, +-50 deg)", wedge == 0, wedge, 0)
dg = bpy.context.evaluated_depsgraph_get(); sc = bpy.context.scene; bad = 0
for p in pts[::500]:
    q = Vector((p.x, p.y, p.z + 0.5)); hit = False
    for _ in range(6):
        h, l, nrm, i, o, m = sc.ray_cast(dg, q, Vector((0, 0, -1)), distance=3)
        if not h: break
        if o.name.startswith(("FB_NaturalBank", "FB_EndBank", "FB_Apron", "FB_Pavilion_floor", "FB_Stand", "FB_Turf", "FB_Pitch")):
            hit = abs(l.z - p.z) < 0.05; break
        q = l + Vector((0, 0, -0.02))
    bad += (not hit)
rec("crowd feet on ground (every 500th point)", bad == 0, bad, 0)
n = sum(r["pass"] for r in res); print(json.dumps(res, indent=1)); print(f"CP050_CHECKS {n}/{len(res)}")
json.dump(res, open("checks/cp050_cupfinal_checks.json", "w"), indent=1)
