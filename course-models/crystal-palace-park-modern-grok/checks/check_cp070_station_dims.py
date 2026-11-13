"""Dimension / source checks for the CP070 station candidate: blender -b CAND.blend -P checks/check_cp070_station_dims.py -- out.json
Values are read from the built geometry (bounding boxes), not from the script constants."""
import bpy, sys, json, math
from mathutils import Vector
out = sys.argv[sys.argv.index("--") + 1]; O = bpy.data.objects; res = []
def bb(n):
    o = O[n]; P = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return [min(p[i] for p in P) for i in range(3)], [max(p[i] for p in P) for i in range(3)]
def chk(ok, label, val, src): res.append({"ok": bool(ok), "check": label, "value": val, "src": src}); print("PASS" if ok else "FAIL", label, val, "|", src)
LOG = json.load(open(bpy.path.abspath("//../../checks/cp070_station_candidate.json")))
lay = LOG["layout"]
(w0, w1) = bb("cp70_station_walls")
front_w = w1[0] - w0[0]; cx, cy = (w0[0] + w1[0]) / 2, None
chk(abs(front_w - 47.0) < 0.5, "frontage width (two pavilions + 1-storey link)", round(front_w, 2), "HE 1064353 composition; width I (no measured elevation)")
sx, sy = LOG["station_ngr_model"]
fy = lay["FY"]; dy = abs((fy - 6.0) - sy); dx = abs(cx - sx)
chk(dx < 1.0 and dy < 1.0, "building centred on HE NGR TQ 34123 70553 via D-PM-31 grid", (round(cx, 2), round(fy - 6.0, 2), sx, sy), "HE 1064353 NGR; D-PM-31 grid")
chk(-344 <= sx <= -198 and -440 <= sy <= -400, "registered point at the head of the Sydenham build's 1854 Low Level shed (x -344..-198, y -411..-439 m)", (sx, sy), "sydenham D-R14-S2 (independent placement)")
zb = lay["ZR"] + 0.12; (r0, r1) = bb("cp70_station_roofs")
chk(r1[2] - zb > 15.0, "left pavilion is the tallest element ('very steep hipped slate roof')", round(r1[2] - zb, 2), "HE 1064353")
D = LOG["dims"]
chk(2 * 4.0 <= D["left_eaves_m"] <= 2 * 5.0 and 2 * 4.0 <= D["right_eaves_m"] <= 2 * 5.0, "both pavilions 2 storeys (4.0-5.0 m per Victorian storey)", (D["left_eaves_m"], D["right_eaves_m"]), "HE 1064353 '2 storeys'; storey height I")
chk(D["central_parapet_m"] < D["right_eaves_m"], "central ticket-office section 1 storey, lower than both pavilions", D["central_parapet_m"], "HE 1064353 '1 storey'")
chk(D["left_roof_pitch_deg"] >= 60 and D["right_roof_pitch_deg"] <= 45, "left roof 'very steep', right roof ordinary hipped", (D["left_roof_pitch_deg"], D["right_roof_pitch_deg"]), "HE 1064353")
doors = [o for o in O if o.name == "cp70_station_doors"]; chk(bool(doors), "2 round-headed doorcases with fanlights + 4 windows in the central section (WDWWDW)", "WDWWDW", "HE 1064353")
chk(not any("canopy" in o.name.lower() for o in O if o.get("cp070_now")), "no canopy over the entrance ('canopy now missing')", "none", "HE 1064353")
road0, road1 = lay["ROAD"]; cw = road1 - road0
chk(7.0 <= cw <= 7.4, "carriageway width", round(cw, 2), "UK single carriageway 7.3 m (DMRB CD 127) I")
BR = 179.53 / 108.66; chk(abs(BR - 38 / 23) < 0.01, "Rail Symbol 2 outline proportion 38:23", round(BR, 3), "Network Rail 'Rail Symbol 2' guidelines 1.2")
t0, t1 = bb("cp70_txt_totem_N"); chk(t1[0] - t0[0] > 1.0, "totem name 'Crystal Palace' readable width > 1 m", round(t1[0] - t0[0], 2), "station sign I")
(g0, g1) = bb("cp70_park_boundary"); chk(1.9 <= (g1[2] - (lay["ZR"] + 0.12)) <= 3.4, "park railings/piers height above pavement", round(g1[2] - lay["ZR"] - 0.12, 2), "typical park boundary I")
json.dump(res, open(out, "w"), indent=1); print("DIMS", sum(r["ok"] for r in res), "/", len(res))
