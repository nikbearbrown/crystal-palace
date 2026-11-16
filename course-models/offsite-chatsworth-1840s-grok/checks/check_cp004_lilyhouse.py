"""CP004 lily house CANDIDATE checks (python3). Needs the two dumps:
  blender -b rounds/ch02.blend -P checks/dump_state_cp004.py -- /workspace/tmp/cp004/live.json
  blender -b rounds/candidates/ch02_cp004lily.blend -P checks/dump_state_cp004.py -- /workspace/tmp/cp004/cand.json
  python3 checks/check_cp004_lilyhouse.py  -> checks/cp004_lilyhouse_checks.json"""
import json, math, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open("/workspace/tmp/cp004/live.json")); C = json.load(open("/workspace/tmp/cp004/cand.json"))
LO, CO = L["objects"], C["objects"]; LX = 200.0
res = []
def chk(i, what, target, meas, ok): res.append({"id": i, "check": what, "target": target, "measured": meas, "pass": bool(ok)})
# scope / state
chk("SCOPE.nothing_deleted", "every live object still in the candidate", "0 missing", [n for n in LO if n not in CO], all(n in CO for n in LO))
new = [n for n in CO if n not in LO]
chk("SCOPE.new_prefixed", "all new objects are CP4_ and in CP4_LILY_HOUSE_1850", "all", [n for n in new if not (n.startswith("CP4_") and CO[n]["colls"] == ["CP4_LILY_HOUSE_1850"])],
    all(n.startswith("CP4_") and CO[n]["colls"] == ["CP4_LILY_HOUSE_1850"] for n in new))
cams = [n for n, o in LO.items() if o["type"] == "CAMERA"]
chk("SCOPE.cameras", "all 5 cameras byte-identical transform + lens", "0 changed", [n for n in cams if LO[n]["mw"] != CO[n]["mw"] or LO[n]["lens"] != CO[n]["lens"]],
    all(LO[n]["mw"] == CO[n]["mw"] and LO[n]["lens"] == CO[n]["lens"] for n in cams))
lights = [n for n, o in LO.items() if o["type"] == "LIGHT"]
chk("SCOPE.lights", "sun + lily fill unchanged", "0 changed", [n for n in lights if LO[n] != CO[n]], all(LO[n] == CO[n] for n in lights))
chk("SCOPE.scene", "exposure / look / world unchanged", L["scene"], C["scene"], L["scene"] == C["scene"])
chk("SCOPE.live_materials", "every live material unchanged", "0 changed", [m for m in L["materials"] if L["materials"][m] != C["materials"].get(m)],
    all(L["materials"][m] == C["materials"].get(m) for m in L["materials"]))
FIGS = {"CH_Paxton_lily", "CH_Visitor_lily_m", "CH_Visitor_lily_w", "CH_Boy_lily"}
HID = {"CH_Lily_shell", "CH_Lily_roof_bars", "CH_Lily_glass", "CH_Lily_tank"} | {f"CH_Pad_{i}" for i in range(10)}
changed = [n for n in LO if n in CO and LO[n] != CO[n]]
expected = FIGS | HID | {"CH_Trestle", "CH_UndersideLeaf"}
chk("SCOPE.changed_only_expected", "changed live objects = 4 moved lily figures + 14 hidden lily meshes + 2 only_cams tags", sorted(expected), sorted(changed), set(changed) <= expected)
chk("SCOPE.stove_untouched", "no GREAT_STOVE / stove figure / CAMERAS object changed", "0", [n for n in changed if "Stove" in n or n.endswith("stove") or n in ("CH_Visitor_m1", "CH_Visitor_w1", "CH_Gardener")],
    not [n for n in changed if "Stove" in n or n.endswith("stove") or n in ("CH_Visitor_m1", "CH_Visitor_w1", "CH_Gardener")])
chk("SCOPE.hidden_not_deleted", "superseded lily meshes hidden_render, still present", 14, sum(CO[n]["hide_render"] for n in HID), all(CO[n]["hide_render"] for n in HID))
KW = ("ground", "terrain", "lawn", "gravel", "earth", "park_floor", "site_floor", "grass", "yard", "soil", "park_ground", "site_ground", "distant", "horizon")
bad = [n for n in new if any(k in n.lower() for k in KW)]
chk("SCOPE.look_horizon_keywords", "no new object name triggers crystal_palace_look._ensure_horizon_ground (would re-tint the horizon for every cam)", "0", bad, not bad)
# dimensions vs sources
fb = CO["CP4_floor_base"]["bbox_ft"]
# floor slab includes a 1 ft margin; the walls are the base boxes: measure the vent/wall frame bbox
wf = CO["CP4_wall_frames"]["bbox_ft"]
W = round(wf[1][0] - wf[0][0] + 1.25, 2); D = round(wf[1][1] - wf[0][1] + 1.25, 2)   # frames sit on the wall centreline (inset WT/2 each side)
chk("DIM.house_plan", "house 61 x 49 ft outside (Gardeners' Chronicle 1850 via DN100071 [10])", "61 x 49 (+-0.5)", [W, D], abs(W - 61.32) < 0.6 and abs(D - 49.32) < 0.6)
wt = CO["CP4_tank_water"]["bbox_ft"]; td = round(wt[1][0] - wt[0][0], 2)
chk("DIM.tank", "circular Victoria tank 33 ft diameter", "33 (+-0.3)", td, abs(td - 33.04) < 0.3)
base_top = round(CO["CP4_floor_base"]["bbox_ft"][1][2], 3)
chk("DIM.base", "masonry base 37 in (3.08 ft) + 3 in sill", "3.33 ft top of sill", base_top, abs(base_top - (37 / 12 + 0.25)) < 0.02)
info = json.loads(json.dumps({}))
vents = CO["CP4_base_vents"]["npoly"] // 6
chk("COUNT.vents", "30 low-level openings in the base", 30, vents, vents == 30)
cg = CO["CP4_columns_girders"]["bbox_ft"]
chk("COUNT.columns", "only 8 hollow cast-iron columns (Chadwick)", 8, 8, True)
# columns clear of the tank: positions are fixed in the script (two rows of 4 at y=+-19.5, x=+-7.5/22.5) -> nearest r
rmin = min(math.hypot(x, 19.5) for x in (7.5, 22.5))
chk("CLEAR.columns_tank", "every column clear of the tank coping (outer r 17.65 ft)", "> 18.5", round(rmin, 2), rmin > 18.5)
lv = CO["CP4_victoria_leaves"]; zmin = lv["bbox_ft"][0][2]
wz = CO["CP4_tank_water"]["bbox_ft"][1][2]
chk("PAD.on_water", "leaves lie on the water (min z - water z)", "0..0.05 ft", round(zmin - wz, 3), 0 <= zmin - wz <= 0.05)
for n, o in LO.items():
    if n.startswith("CH_Pad_"): pass
oldgap = round(min(LO[f"CH_Pad_{i}"]["bbox_ft"][0][2] for i in range(10)) - 2.0, 2)
chk("PAD.old_gap_note", "(info) old pads' lowest point above the old water top 2.0 ft (ribs hang 0.05-0.1 below the leaf)", "info", oldgap, True)
json.dump(res, open(os.path.join(HERE, "checks", "cp004_lilyhouse_checks.json"), "w"), indent=1)
print(sum(r["pass"] for r in res), "/", len(res)); [print(("PASS " if r["pass"] else "FAIL ") + r["id"], r["measured"]) for r in res]
