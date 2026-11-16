"""Checks for the CP019 cases CANDIDATE (2026-11-16, FT101-FT108): measures the new C19_* props against the sources/guesses they
follow, staging (on the floor or stacked, clear of the door lanes and cameras, inside the wall, statue inside its case, trees bare)
and a live-vs-candidate object accounting (only C19_* objects added, no existing object moved, hidden or removed).
blender -b rounds/candidates/f03_cp019cases.blend -P scripts/check_cp019_cases.py -- --out checks/cp019_cases_checks.json --live rounds/f03.blend"""
import bpy, sys, json, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]; OUT = argv[argv.index("--out") + 1]; LIVE = argv[argv.index("--live") + 1]
FT = 0.3048; res = []
def rec(i, what, ok, meas, target="", src=""):
    res.append({"id": i, "check": what, "target": target, "measured": meas, "pass": bool(ok), "source": src})
O = bpy.data.objects
def bb(o):
    if o.type == 'MESH' and o.data and len(o.data.vertices):
        vs = [o.matrix_world @ v.co for v in o.data.vertices]
    else:
        vs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return [min(v[i] for v in vs) / FT for i in range(3)], [max(v[i] for v in vs) / FT for i in range(3)]
C19 = [o for o in O if o.name.startswith("C19_")]
props = [o for o in C19 if o.type == 'MESH' and not o.name.startswith("C19_TREE")]
inside = [o for o in props if bb(o)[1][1] > -204.0 and not o.name.startswith("C19_DRAY_Q")]
# sizes
for nm in ("C19_CASE_E1", "C19_CASE_E2", "C19_CASE_E3", "C19_CASE_E4"):
    lo, hi = bb(O[nm]); s = O[nm]["size_ft"]
    rec(f"S_{nm}", f"{nm} footprint/height within a two-man to crane-lift case range (2.4-5.5 ft, h 2.4-3.8 ft)", 2.4 <= min(s[0], s[1]) and max(s[0], s[1]) <= 5.5 and 2.4 <= s[2] <= 3.8, list(s), "2.4-5.5 / 2.4-3.8", "Muse crate NOTES 3.7x2.4x2.4 ft (guessed, two-man lift); larger cases guessed for crane")
lo, hi = bb(O["C19_FLYWHEEL"]); rec("M01", "flywheel overall height (9 ft wheel + 1 ft cradle)", abs((hi[2] - lo[2]) - 10.0) <= 0.1, round(hi[2] - lo[2], 3), "10.0 +-0.1", "FT102: 9 ft wheel, cradle 1 ft")
rec("M02", "flywheel fits a 6 ft x 14 ft south door edgewise (thickness <= 6 ft incl. hub, height <= 14 ft)", (hi[1] - lo[1]) <= 6 and (hi[2] - lo[2]) <= 14, [round(hi[1] - lo[1], 2), round(hi[2] - lo[2], 2)], "<=6, <=14", "FT06 door 6 ft wide, 14 ft high")
fl, fh = bb(O["C19_SCULPT_FIGURE"]); cl, ch = bb(O["C19_SCULPT_CASE"])
rec("SC01", "statue height (6 ft 6 in figure, metaball surface)", abs((fh[2] - fl[2]) - 6.5) <= 0.5, round(fh[2] - fl[2], 3), "6.5 +-0.5", "FT102")
rec("SC02", "statue inside its case (x/z bbox inside case bbox, top below the lid)", fl[0] >= cl[0] and fh[0] <= ch[0] and fh[2] < ch[2] - 0.07, [round(v, 2) for v in fl + fh], f"case {[round(v, 2) for v in cl + ch]}", "")
# staging
stack_on = {"C19_CASE_E2": "C19_CASE_E1", "C19_BALE_2": "C19_BALE_1"}
for o in props:
    lo, hi = bb(o)
    if o.name in stack_on:
        base = bb(O[stack_on[o.name]])[1][2]; ok = abs(lo[2] - base) <= 0.1; tgt = f"on {stack_on[o.name]} top {base:.2f}"
    elif o.name == "C19_DRAY_Q_CASE_3": ok = abs(lo[2] - 6.5) <= 0.15; tgt = "on the 2.5 ft cases on the deck, 6.5"
    elif o.name.startswith("C19_DRAY_Q_CASE"): ok = abs(lo[2] - 4.0) <= 0.15; tgt = "dray deck 4.0"
    elif o.name == "C19_SCULPT_FIGURE": ok = abs(lo[2] - 0.25) <= 0.1; tgt = "case bottom 0.25"
    elif o.name == "C19_SCULPT_STRAW": ok = abs(lo[2] - 0.25) <= 0.3; tgt = "case bottom 0.25"
    else: ok = abs(lo[2]) <= 0.12; tgt = "floor 0 +-0.12"
    rec(f"Z_{o.name}", f"{o.name} rests on its support", ok, round(lo[2], 3), tgt, "")
lane = [o.name for o in inside if bb(o)[0][0] < 12.5 and bb(o)[1][0] > -12.5]
rec("L01", "no interior C19 prop in the door lanes / truck route (|x| < 12.5 ft)", not lane, lane, "[]", "FT06 doors x -12..12; FT07 truck lane")
wall = [o.name for o in inside if bb(o)[0][1] < -203.6]
rec("L02", "interior props inside the south wall face (y >= -203.6)", not wall, wall, "[]", "")
cams = [o for o in O if o.type == 'CAMERA']
mind = min(((Vector(c.matrix_world.translation) / FT - Vector([(a + b) / 2 for a, b in zip(*bb(o))])).length - max(bb(o)[1][0] - bb(o)[0][0], bb(o)[1][1] - bb(o)[0][1]) / 2, c.name, o.name) for c in cams for o in props)
rec("L03", "every camera >= 3 ft from the nearest C19 prop (centre distance minus half extent)", mind[0] >= 3.0, [round(mind[0], 2), mind[1], mind[2]], ">= 3", "check_state 1 ft clearance, with margin")
trees = [o for o in C19 if o.name.startswith("C19_TREE_") and o.type == 'EMPTY']
ys = [o.location.y / FT for o in trees]; xs = sorted(o.location.x / FT for o in trees); gaps = [b - a for a, b in zip(xs, xs[1:])]
rec("T01", "tree row y = -520 +- 12 ft", all(-532 <= y <= -508 for y in ys), [round(min(ys), 1), round(max(ys), 1)], "-532..-508", "exterior EX31 rule (as FT97)")
rec("T02", "tree spacing 115-150 ft", all(115 <= g <= 150 for g in gaps), [round(min(gaps), 1), round(max(gaps), 1)], "115-150", "EX31")
leaves = [o.name for o in C19 if "LEAVES" in o.name or (o.data and "leaves" in o.data.name.lower())]
rec("T03", "trees are bare (no leaf cards), Feb-Mar 1851", not leaves, leaves, "[]", "FT105")
marks = sum(1 for m in bpy.data.materials if m.name.startswith("C19_Mark_") and m.users)
packed = all(i.packed_file is not None for i in bpy.data.images if i.name.startswith("cp019_mark_"))
rec("K01", "consignment mark materials in use, images packed in the blend", marks >= 7 and packed, [marks, packed], ">= 7, packed", "FT104")
cand = {o.name: ([round(v, 5) for v in o.matrix_world.translation], o.hide_render, o.data.name if o.data else None) for o in O}
info = json.loads(bpy.context.scene["grok_build"]); st = info.get("state")
bpy.ops.wm.open_mainfile(filepath=LIVE)
live = {o.name: ([round(v, 5) for v in o.matrix_world.translation], o.hide_render, o.data.name if o.data else None) for o in bpy.data.objects}
added = sorted(set(cand) - set(live)); removed = sorted(set(live) - set(cand))
changed = [n for n in live if n in cand and cand[n] != live[n]]
rec("A01", "only C19_* objects added", all(n.startswith("C19_") for n in added), len(added), "all C19_*", "FT106")
rec("A02", "no live object removed", not removed, removed[:10], "[]", "FT106")
rec("A03", "no live object moved, re-meshed or hidden", not changed, changed[:10], "[]", "FT106")
rec("A04", "state stays fitout (Hyde Park, early 1851)", st == "fitout", st, "fitout", "Hyde Park and Sydenham never blended")
n_ok = sum(r["pass"] for r in res)
json.dump({"candidate": "rounds/candidates/f03_cp019cases.blend", "live": LIVE, "passed": n_ok, "total": len(res), "checks": res}, open(OUT, "w"), indent=1)
print(f"CP019_CHECKS {n_ok}/{len(res)}")
for r in res:
    if not r["pass"]: print("FAIL", r)
