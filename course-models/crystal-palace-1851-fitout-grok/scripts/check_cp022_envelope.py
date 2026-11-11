"""Checks for the CP022 envelope CANDIDATE (2026-11-11, FT67-FT73): measures the new C22_* parts against the sources (same
checks as check_cp020_nave.py) plus N14/N15 for the FT71 gallery-figure fix.
blender -b rounds/candidates/o01_cp022envelope.blend -P scripts/check_cp022_envelope.py -- --out checks/cp022_envelope_checks.json"""
import bpy, sys, json
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]; OUT = argv[argv.index("--out") + 1]
FT = 0.3048; res = []
def rec(i, what, target, tol, meas, src):
    res.append({"id": i, "check": what, "target": target, "tol": tol, "measured": round(meas, 3), "pass": abs(meas - target) <= tol, "source": src})
new = [o for o in bpy.data.objects if o.name.startswith("C22_")]
cols = [o for o in new if o.get("part_kind") == "column"]
allcols = [o for o in bpy.data.objects if o.get("part_kind") == "column" and not o.hide_render]
xs = sorted({round(o.location.x / FT, 3) for o in cols}); ys = sorted({round(o.location.y / FT, 3) for o in allcols})
rec("N01", "west end column line x (ft); transept at the middle of 1,848 ft", -924.0, 0.01, min(xs), "SURVEY: length 1,848 ft (column centres)")
rec("N02", "length between end column centres if mirrored east (ft)", 1848.0, 0.01, -2 * min(xs), "SURVEY 1,848 ft")
wx = [x for x in xs if x <= -84]; ex = [x for x in xs if x >= 84]
steps = sorted({round(b - a, 3) for L in (wx, ex) for a, b in zip(L, L[1:])})
rec("N03", "largest new column-line step along the nave, west -924..-84 and east 84..132 runs (ft)", 24.0, 0.01, max(steps), "Downes 24 ft grid")
rec("N04", "smallest new column-line step along the nave, same runs (ft)", 24.0, 0.01, min(steps), "Downes 24 ft grid")
def tier_w(t):
    yy = [abs(o.location.y / FT) for o in cols if o.get("tier") >= t and o.location.x / FT < -132]
    return 2 * max(yy)
rec("N05", "tier-1 width west block (ft)", 408.0, 0.01, tier_w(1), "SURVEY tier widths 408/264/120")
rec("N06", "tier-2 width west block (ft)", 264.0, 0.01, tier_w(2), "SURVEY tier widths")
rec("N07", "tier-3 width west block (ft)", 120.0, 0.01, tier_w(3), "SURVEY tier widths")
navec = [abs(o.location.y / FT) for o in cols if abs(o.location.y / FT) < 40 and abs(o.location.y / FT) > 20]
rec("N08", "nave clear width between column centres (ft)", 72.0, 0.01, 2 * min(navec), "Downes: nave 72 ft")
for t, z in ((1, 22 + 2 / 12), (2, 42 + 2 / 12), (3, 62 + 2 / 12)):
    gz = sorted({round(o.location.z / FT, 3) for o in new if o.get("part_kind") == "girder" and o.get("tier") == t})
    rec(f"N09_{t}", f"tier-{t} girder top (ft)", z, 0.01, gz[0] if len(gz) == 1 else -1, "D11a-c (build_transept.py)")
tz = sorted({round(o.location.z / FT, 3) for o in new if o.get("part_kind") == "truss"})
rec("N10", "nave truss top (ft) = tier-3 girder top", 62 + 2 / 12, 0.01, tz[0] if len(tz) == 1 else -1, "D19 / transept trusses")
fl = bpy.data.objects["C22_FLOOR_W"]; fz = max((fl.matrix_world @ Vector(c)).z for c in fl.bound_box) / FT
fw = max((bpy.data.objects["FLOOR_BOARDS"].matrix_world @ Vector(c)).z for c in bpy.data.objects["FLOOR_BOARDS"].bound_box) / FT
rec("N11", "west floor top equals live floor top (ft difference)", 0.0, 0.001, fz - fw, "FT63")
figs = [o for o in bpy.data.objects if o.get("part_kind") == "figure" and not o.hide_render]
clash = sum(1 for o in figs for c in cols if (o.location.xy - c.location.xy).length < 1.6 * FT)
rec("N12", "figures inside a new column (count)", 0, 0, clash, "staging")
dup = len(cols) - len({(round(o.location.x / FT), round(o.location.y / FT)) for o in cols + [o for o in allcols if not o.name.startswith('C22_')]}) + len([o for o in allcols if not o.name.startswith('C22_')])
rec("N13", "new columns duplicating an existing column position (count)", 0, 0, dup, "no double columns")
decks = []
for o in bpy.data.objects:
    if o.type == 'MESH' and not o.hide_render and (o.name.startswith("GAL_") or o.name.startswith("C22_GAL_")):
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        decks.append((min(v.x for v in bb) / FT, max(v.x for v in bb) / FT, min(v.y for v in bb) / FT, max(v.y for v in bb) / FT))
up = [o for o in bpy.data.objects if o.name.startswith("CROWD") and not o.hide_render and o.location.z / FT > 10]
off = [o.name for o in up if not any(a <= o.location.x / FT <= b and c <= o.location.y / FT <= d for (a, b, c, d) in decks)]
rec("N14", "visible gallery-level crowd figures not over a gallery deck (count)", 0, 0, len(off), "FT71")
rec("N15", "visible gallery-level crowd figures kept (>= 300 of 380)", 1, 0, 1 if len(up) >= 300 else 0, "FT71 keeps the gallery crowd")
json.dump(res, open(OUT, "w"), indent=1)
print("CP022_ENVELOPE_CHECKS", "gallery figs", len(up), sum(r["pass"] for r in res), "/", len(res))
for r in res:
    if not r["pass"]: print("FAIL", r)
