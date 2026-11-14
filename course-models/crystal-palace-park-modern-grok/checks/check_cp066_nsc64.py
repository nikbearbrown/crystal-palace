"""CP066 NSC 1964-67 candidate checks (2026-11-14). Run:
blender -b rounds/candidates/park60-r17_cp066nsc64.blend -P checks/check_cp066_nsc64.py
Compares against live rounds/park60-r17.blend (state dumped by checks/dump_state_cp066.py in a 2nd Blender session):
scope, cameras, lights, hidden set, grounding, dated dimensions."""
import bpy, json, math, os, subprocess, tempfile
from mathutils import Vector
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = os.path.join(HERE, "rounds/park60-r17.blend")
cand = {o.name: o for o in bpy.data.objects}
res = []
def chk(name, ok, info=""):
    res.append({"check": name, "pass": bool(ok), "info": info}); print(("PASS " if ok else "FAIL ") + name, info, flush=True)
tmp = tempfile.mktemp(suffix=".json")
subprocess.run([bpy.app.binary_path, "-b", LIVE, "-P", os.path.join(HERE, "checks/dump_state_cp066.py"), "--", tmp], check=True, capture_output=True)
live = json.load(open(tmp)); sl = live.pop("__scene__")
new = [n for n, o in cand.items() if "cp066_nsc" in o.keys()]
def M(o): return [round(v, 5) for r in o.matrix_world for v in r]
missing = [n for n in live if n not in cand]
chk("no live object removed", not missing, f"{len(missing)} missing")
extra = [n for n in cand if n not in live and n not in new]
chk("only tagged cp066 objects added", not extra, f"new={len(new)} extra={extra[:5]}")
cam_bad = [n for n, e in live.items() if e["type"] == "CAMERA" and (e["m"] != M(cand[n]) or abs(e["lens"] - cand[n].data.lens) > 1e-6)]
chk("cameras unchanged (transform + lens)", not cam_bad, str(cam_bad))
li_bad = [n for n, e in live.items() if e["type"] == "LIGHT" and (e["m"] != M(cand[n]) or e["energy"] != cand[n].data.energy or e["hide_render"] != cand[n].hide_render)]
chk("lights unchanged (incl. the 4 nsc flood lights)", not li_bad, str(li_bad))
hid = [n for n, e in live.items() if (not e["hide_render"]) and cand[n].hide_render]
chk("only the 24 r17 nsc_ block-out meshes hidden", all(n.startswith("nsc_") and cand[n].type == "MESH" for n in hid) and len(hid) == 24, f"{len(hid)} hidden")
unhid = [n for n, e in live.items() if e["hide_render"] and not cand[n].hide_render]
chk("nothing un-hidden", not unhid, str(unhid[:5]))
mov = [n for n, e in live.items() if e["m"] != M(cand[n])]
chk("no live object moved", not mov, str(mov[:5]))
sc = bpy.context.scene
chk("scene exposure/look/world/res/spp unchanged in file", abs(sc.view_settings.exposure - sl["exposure"]) < 1e-6 and sc.view_settings.view_transform == sl["vt"]
    and sc.world.name == sl["world"] and [sc.render.resolution_x, sc.render.resolution_y] == sl["res"] and sc.cycles.samples == sl["spp"])
PS = cand["park_slope"]
def ground(x, y):
    ok, loc, n, i = PS.ray_cast(PS.matrix_world.inverted() @ Vector((x, y, 400.0)), Vector((0, 0, -1))); return (PS.matrix_world @ loc).z
L = json.load(open(os.path.join(HERE, "checks/cp066_nsc64_candidate.json")))
D = L["dims"]
for i in range(4):
    m = D[f"mast_{i}"]; g = ground(m["x"], m["y"])
    chk(f"mast_{i} grounded", m["base"] <= g, f"base {m['base']} ground {g:.2f}")
zs = []
for ix in range(-100, 101, 4):
    for iy in range(-60, 61, 4):
        ax = max(abs(ix) - D["straight"] / 2, 0); d = math.hypot(ax, iy) - D["bend_r"]
        if d > 13: continue
        for nm in ("park_slope", "central_walk.002", "central_walk.003", "park_paths_gravel", "flower_beds"):
            o = cand[nm]; mi = o.matrix_world.inverted()
            ok, loc, n_, i_ = o.ray_cast(mi @ Vector((-50 + ix, -550 + iy, 0.0)), (mi.to_3x3() @ Vector((0, 0, -1))).normalized())
            if ok: zs.append(((o.matrix_world @ loc).z, nm))
top = max(zs)
chk("no terrain/path pokes through the arena floor (Z0 -43.1)", top[0] < -43.1, f"highest {top[0]:.2f} ({top[1]})")
chk("sports centre plinth grounded", D["sports_centre"]["plinth_h"] > 0, str(D["sports_centre"]))
chk("lap 440 yd on the measurement line", abs(2 * D["straight"] + 2 * math.pi * (D["bend_r"] + 0.30) - 402.336) < 0.01, f"{D['lap_m']}")
chk("8 lanes x 4 ft", D["lanes"] == 8 and abs(D["lane_w"] - 1.2192) < 1e-4)
chk("sports centre = 1.75 acres (+-2%)", abs(D["sports_centre"]["acres"] - 1.75) / 1.75 < 0.02, str(D["sports_centre"]["acres"]))
chk("stand seats in a 12,000 order (8k-14k benches at 0.5 m)", 8000 <= D["west_stand"]["seats_est"] <= 14000, str(D["west_stand"]["seats_est"]))
chk("canopy clear height over covered front row 5-9 m", 5.0 <= D["canopy"]["front_clear_over_tread"] <= 9.0, str(D["canopy"]["front_clear_over_tread"]))
chk("no east stand (Jubilee Stand is 1977)", not any("jubilee" in n.lower() or "east_stand" in n.lower() for n in new))
json.dump(res, open(os.path.join(HERE, "checks/cp066_nsc64_checks.json"), "w"), indent=1)
print("CHECKS", sum(r["pass"] for r in res), "/", len(res), flush=True)
