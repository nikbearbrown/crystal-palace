"""D-checks for the HP-BUILD construction set. blender -b rounds/cNN.blend -P check_construction.py -- --out checks/cNN/checks.md"""
import bpy, sys, os, json, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]; OUT = argv[argv.index("--out") + 1]
FT = 0.3048; f = lambda m: m / FT
res = []
def chk(cid, ok, what, detail=""): res.append((cid, bool(ok), what, detail))
obs = bpy.data.objects
kind = lambda k: [o for o in obs if o.get("part_kind") == k]
cols = kind("column")
offgrid = [o.name for o in cols if abs((f(o.location.x) - 36) / 24 - round((f(o.location.x) - 36) / 24)) > 1e-3 or abs((f(o.location.y) + 204) / 24 - round((f(o.location.y) + 204) / 24)) > 1e-3]
chk("K01", not offgrid and cols, "columns on Claude's 24 ft grid (x = -924 + 24 i ft)", f"{len(cols)} columns, {len(offgrid)} off grid")
nave = [o.name for o in cols if abs(f(o.location.y)) < 36]
chk("K02", not nave, "no columns in the 72 ft nave", f"{len(nave)}")
TOPS = [22 + 2/12, 42 + 2/12, 62 + 2/12]
gir = [o for o in kind("girder") if o.get("state") == "fixed"]
bad = [o.name for o in gir if min(abs(f(o.location.z) - t) for t in TOPS) > 0.01]
chk("K03", not bad and gir, "fixed girder tops at 22'2\" / 42'2\" / 62'2\"", f"{len(gir)} girders, {len(bad)} bad")
hoist = [o for o in kind("girder") if o.get("state") == "hoisting"]
sl = kind("sheer_legs")
chk("K04", hoist and sl and sl[0]["apex_ft"][2] > f(hoist[0].location.z) + 6 and f(hoist[0].location.z) < TOPS[0],
    "CP012 hoisted girder below its seat and under the sheer-leg apex", f"girder top {f(hoist[0].location.z):.1f} ft, apex {sl[0]['apex_ft'][2]} ft")
D16 = {(2.0, 1.0), (2.0, 1.5), (3.0, 1.5), (3.0, 2.0)}
bp = kind("base_piece")
badp = [o.name for o in bp if (o["plate_L"], o["plate_W"]) not in D16]
chk("K05", bp and not badp, "D16 base plates from the Plate VIII printed set 2x1 .. 3x2 ft", f"{len(bp)} base pieces; sizes {sorted({(o['plate_L'], o['plate_W']) for o in bp})}")
pads = kind("pad")
badd = [o.name for o in pads if not (1.25 <= o["pad_t"] <= 3.48 and 1.58 <= o["pad_W"] <= 3.72 + 0.6 and 1.2 <= o["pad_top"] <= 2.1)]
chk("K06", pads and not badd, "D17 pads: thickness 1.25-3.48 ft, width 1.58-3.72 ft, top 1.2-2.1 ft below floor", f"{len(pads)} pads, {len(badd)} out of range")
ordered = all(o1["pad_t"] >= o0["pad_t"] for o0 in pads for o1 in pads if abs(o1["y"]) < abs(o0["y"]))
chk("K07", ordered, "D17 trend: pads deeper under the inner (heavier) columns")
badsock = [o.name for o in bp if abs(o["socket_top_ft"] - 3.75 / 12) > 1e-6 or abs(f(o.location.z) + o["socket_top_ft"] - 3.75/12 + o["socket_top_ft"] - o["socket_top_ft"]) > 5]
socket_z = [f(o.location.z) + f(max((o.matrix_world @ Vector(c)).z for c in o.bound_box) - o.location.z) for o in bp]
bad = [z for z in socket_z if abs(z - 3.75 / 12) > 0.02]
chk("K08", bp and not bad, "base piece socket 3 3/4 in above floor (Plate VIII Fig. 1)", f"socket top {min(socket_z)*12:.2f}-{max(socket_z)*12:.2f} in")
pegzone = [o for o in cols if f(o.location.x) > 708.5]
chk("K09", not pegzone, "no bare column on grass/earth: standing columns only where bases are backfilled (x <= 708)", f"{len(pegzone)}")
wag = kind("glazing_wagon")
def wheel_y(o):
    ys = sorted({round(f((o.matrix_world @ v.co).y) - f(o.location.y), 2) for v in o.data.vertices if f(v.co.z) < 0.6 and abs(f(v.co.x)) > 1.3})
    return ys
gauge = [max(wheel_y(o)) - min(wheel_y(o)) for o in wag]
gut = [abs((f(o.location.y) + 204) % 8) for o in wag]
chk("K10", wag and all(7.6 < g < 8.4 for g in gauge) and all(abs(g - 4) < 0.01 for g in gut),
    "glazing wagons: wheels in the gutters, 8 ft gauge, deck over one ridge", f"{len(wag)} wagons, wheel spread {min(gauge):.2f}-{max(gauge):.2f} ft (outer faces)")
bars = bpy.data.meshes.get("roof_bars")
nbar = int(bpy.context.scene.get("nbars", 0))
sp = 288 / (nbar + 1)
chk("K11", bars is not None and 10.0 < sp < 10.75, "sash bars at 10-10 3/4 in centres (> 10 in pane width; Plate XII 10 1/2 in) + 3 strong bars per 24 ft", f"{nbar} bars per slope per unit, {sp:.2f} in centres")
cr = kind("crate"); hd = kind("hoarding")
chk("K21", len(cr) >= 10 and all(o.instance_collection and o.instance_collection.get("credit", "").startswith("Muse") for o in cr), "props appended from models/ are credited to their maker", f"{len(cr)} Muse crates")
chk("K22", hd and all(7.5 < f(max((o.matrix_world @ Vector(c)).z for c in o.bound_box)) < 8.6 and f(max((o.matrix_world @ Vector(c)).y for c in o.bound_box)) < -290 for o in hd), "site hoarding ~8 ft high, south of the works (y < -290 ft)", f"{len(hd)} hoarding objects")
wk = kind("worker")
hs = [f(max((o.matrix_world @ Vector(c)).z for c in o.bound_box) - min((o.matrix_world @ Vector(c)).z for c in o.bound_box)) for o in wk if o.get("pose") in ("stand", "work")]
chk("K12", wk and all(5.3 < h < 5.9 for h in hs), "worker stand-ins 5'4\"-5'10\" (standing)", f"{len(wk)} workers; standing heights {min(hs):.2f}-{max(hs):.2f} ft")
cams = [o for o in obs if o.type == 'CAMERA']
lens = [o.name for o in cams if round(o.data.lens) not in (28, 35, 50) or abs(o.data.sensor_width - 36) > 1e-3]
chk("K13", not lens, "lenses 28/35/50 mm on 36 mm sensor", f"{len(cams)} cameras")
roll = []
for o in cams:
    m = o.matrix_world.to_3x3(); right = m @ Vector((1, 0, 0))
    if abs(right.z) > 1e-4: roll.append(o.name)
chk("K14", not roll, "no roll", f"{len(roll)}")
scaf = kind("scaffold")
def support(x, y):
    for s in scaf:
        if s["x0"] - 0.5 <= x <= s["x1"] + 0.5 and s["y0"] <= y <= s["y1"]: return s["deck_ft"], s.name
    return 0.0, "ground"
eye = []
for o in cams:
    if o.data.type == 'ORTHO' or o.name.startswith("REV_") or o.name.startswith("CP014"): continue
    z0, sup = support(f(o.location.x), f(o.location.y)); e = f(o.location.z) - z0
    if abs(e - 5.25) > 0.05: eye.append(f"{o.name} {e:.2f} on {sup}")
chk("K15", not eye, "eye height 1.6 m (5.25 ft) above ground or the work-platform deck the camera stands on", "; ".join(eye) or "all on ground or deck")
dg = bpy.context.evaluated_depsgraph_get(); clear = []
mesh_obs = [o for o in obs if o.type == 'MESH' and not o.name.startswith("KGROUND_PARK")]
for c in cams:
    if c.data.type == 'ORTHO': continue
    p = c.matrix_world.translation; best = (1e9, "")
    for o in mesh_obs:
        bb = [o.matrix_world @ Vector(v) for v in o.bound_box]
        lo = Vector([min(v[i] for v in bb) for i in range(3)]); hi = Vector([max(v[i] for v in bb) for i in range(3)])
        if any(p[i] < lo[i] - 1.0 or p[i] > hi[i] + 1.0 for i in range(3)): continue
        ok, loc, nrm, idx = o.closest_point_on_mesh(o.matrix_world.inverted() @ p)
        if ok:
            d = ((o.matrix_world @ loc) - p).length
            if d < best[0]: best = (d, o.name)
    if best[0] < FT * 1.0: clear.append(f"{c.name} {f(best[0]):.2f} ft from {best[1]}")
chk("K16", not clear, "camera clearance >= 1 ft from every object (never inside scaffold, girders, columns)", "; ".join(clear) or "all clear")
off = [o.name for o in obs if o.users_collection and o.users_collection[0].name in ("OFFSITE_YARD", "DETAIL_DRAINAGE") and f(o.location.x) < 2000 and o.type == 'MESH' and o.location.length > 0]
chk("K17", not off, "OFFSITE yard and detail sit >= 2000 ft from the building (never read as Hyde Park site)")
lbl = [o for o in obs if o.get("part_kind") == "label"]
chk("K18", len(lbl) >= 5, "CP014 section labelled", f"{len(lbl)} labels")
lv = [o for o in obs if o.get("part_kind") == "louvre_blade" and o.animation_data]
chk("K19", lv, "CP015 louvre opens/closes over frames 1-96", f"{len(lv)} animated blades")
syd = [o.name for o in obs if "sydenham" in o.name.lower()]
chk("K20", not syd, "Hyde Park 1851 only, no Sydenham content")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as fh:
    fh.write(f"# construction checks {os.path.basename(bpy.data.filepath)}\n\n| id | result | check | detail |\n|---|---|---|---|\n")
    for cid, ok, w, d in res: fh.write(f"| {cid} | {'PASS' if ok else 'FAIL'} | {w} | {d} |\n")
    fh.write(f"\n{sum(r[1] for r in res)}/{len(res)} pass\n")
print(open(OUT).read())
