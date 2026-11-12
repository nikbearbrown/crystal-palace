"""CP029 "The exhibition ends" east-nave CANDIDATE (2026-11-12, DEPARTURES FT81-FT87). NOT live, no verdict.
  blender -b -P scripts/cand_cp029_east_20261112.py -- --src rounds/c02.blend --out rounds/candidates/c02_cp029east.blend
Hyde Park 1851 CLOSING state (c02, 15 Oct 1851 closing ceremony) only; nothing Sydenham.

Live CP029_dais_start (28 mm) stands at (-27, -6) ft, eye 5.3 ft, looking 60 deg north of due east (dir 0.50, 0.87), so the
right third of the frame looks east-north-east along the line of the nave. c02 is the transept model (|x| <= 132 ft); east of
x = 132 there is only the ground plane, so the right edge shows a flat green lawn at floor level and the top-right shows open
sky where the east nave roof and galleries should be.
This candidate applies the CP027 east-nave rules (FT74-FT78, scripts/cand_cp027_east_20261112.py; themselves the KEPT CP020
nave rules FT60-FT65 mirrored east) unchanged to c02, using c02's own part library:
  FT81  (= FT74) nave tier-3 strip |y| <= 60 for x 60..132.
  FT82  (= FT75) full three-tier east nave x 132..924 with galleries; east end at x = +924.
  FT83  (= FT76) floor boards continued x 144..924.5.
  FT84  (= FT77) the x = +132 tier-2 side walls for |y| < 132 hidden.
  FT85  (= FT71, CP022 KEEP) gallery-level crowd figures (z ~ 22.9 ft) whose feet are over no gallery deck are hidden, not deleted:
        in c02 the closing-day gallery spawn ran over the nave/transept crossing (x ~ +-42 ft, |y| < 36 ft, no deck there), so
        one of them stands on air against the sky top-right of CP029. people_lib v3.1 seeds each figure by its NAME and ranks
        LOD over all figures incl. hidden ones, so hiding does not reshuffle anyone else. Figures inside a new column are also
        hidden (none expected).
  FT86  (= FT79) the east block is empty of exhibits, visitors and banners (judgement call).
Lighting, world, exposure, cameras and every existing object other than FT84 and FT85 are unchanged."""
import bpy, bmesh, math, os, sys
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
SRC, OUT = arg("--src"), arg("--out")
assert os.path.abspath(SRC) != os.path.abspath(OUT), "refusing to overwrite the source blend"
for live in ("rounds/c01.blend", "rounds/c02.blend", "rounds/h01.blend", "rounds/h02.blend", "rounds/h03.blend", "rounds/h04.blend"):
    assert not os.path.abspath(OUT).endswith(live), "refusing to overwrite a live blend"
bpy.ops.wm.open_mainfile(filepath=SRC)
assert not any(o.name.startswith(("C20_", "C22_", "C27_", "C29_")) for o in bpy.data.objects), "source already has a nave extension (C20_/C22_/C27_/C29_*)"
try: bpy.context.preferences.filepaths.save_version = 0
except Exception: pass
sc = bpy.context.scene
FT = 0.3048
def ft(v): return v * FT
TAG = "cp029_east_20261112"
GIRDER_TOP = [22 + 2 / 12, 42 + 2 / 12, 62 + 2 / 12]   # D11a-c, as build_transept.py / apply_envelope_v2.py
X_EAST_END = 924                                      # 1,848 ft between end column centres, transept at the middle (FT62 convention)

LIB = {k: bpy.data.meshes[k] for k in ("col_22", "col_42", "col_62", "girder24", "truss72", "roof_unit", "wall_louvre", "railing24")}
def mesh_like(prefix):
    for me in bpy.data.meshes:
        if me.name.startswith(prefix): return me
    raise KeyError(prefix)
LIB["wall_g"] = mesh_like("wall_24_14.4"); LIB["wall_g_fill"] = bpy.data.meshes[LIB["wall_g"].name + "_fill"]
LIB["wall_b"] = mesh_like("wall_24_16.6"); LIB["wall_b_fill"] = bpy.data.meshes[LIB["wall_b"].name + "_fill"]
H_G = max(v.co.z for v in LIB["wall_g"].vertices) / FT
H_B = max(v.co.z for v in LIB["wall_b"].vertices) / FT

coll = bpy.data.collections.new("C29_EAST_NAVE"); sc.collection.children.link(coll)
coll["candidate"] = TAG
coll["credit"] = "Grok Bot: c02's own transept part library continued along the nave on Downes' 24 ft grid (CP029 candidate; CP027 east-nave rules on c02)"
count = {}
def put(key, name, x, y, z, rot=0.0, **props):
    o = bpy.data.objects.new("C29_" + name, LIB[key])
    o.location = (ft(x), ft(y), ft(z)); o.rotation_euler = (0, 0, rot)
    coll.objects.link(o); o[TAG] = "FT81-FT82"
    for k, v in props.items(): o[k] = v
    count[key] = count.get(key, 0) + 1
    return o

cols = {}
for o in bpy.data.objects:
    if o.name.startswith("COL_") and o.type == 'MESH' and "tier" in o:
        cols[(round(o.location.x / FT), round(o.location.y / FT))] = int(o["tier"])
existing = set(cols)
ROWS_Y = [-204 + 24 * j for j in range(18)]
X_EAST = list(range(84, X_EAST_END + 1, 24))          # 84 .. 924
def tier_of(y):
    ay = abs(y); return 3 if ay <= 60 else (2 if ay <= 132 else 1)
new_cols = {}
for x in X_EAST:
    for y in ROWS_Y:
        if abs(y) < 36 or (x, y) in existing: continue
        if abs(x) <= 132 and abs(y) > 60: continue
        new_cols[(x, y)] = tier_of(y)
for y in (-12, 12): new_cols[(X_EAST_END, y)] = 3     # end-screen columns across the 72 ft nave (C02 pattern)
cols.update(new_cols)
COLKEY = {1: "col_22", 2: "col_42", 3: "col_62"}
for (x, y), t in sorted(new_cols.items()):
    put(COLKEY[t], f"COL_X{x:+04d}_Y{y:+04d}", x, y, 0, part_kind="column", tier=t, paint_state="painted")
def gird(a, b, along):
    ta, tb = cols.get(a), cols.get(b)
    if not ta or not tb or (a in existing and b in existing): return
    for k in range(min(ta, tb)):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        put("girder24", f"GIR_T{k+1}_{along}_{mx:+.0f}_{my:+.0f}", mx, my, GIRDER_TOP[k], math.pi / 2 if along == "Y" else 0.0,
            part_kind="girder", tier=k + 1, paint_state="painted")
for (x, y) in list(cols):
    if (x, y + 24) in cols: gird((x, y), (x, y + 24), "Y")
    if (x + 24, y) in cols: gird((x, y), (x + 24, y), "X")
gird((X_EAST_END, -36), (X_EAST_END, -12), "Y"); gird((X_EAST_END, 12), (X_EAST_END, 36), "Y")
for x in X_EAST:
    put("truss72", f"TRUSS72_X{x:+04d}", x, 0, GIRDER_TOP[2], math.pi / 2, part_kind="truss", span_ft=72, strength="light")
XC3 = list(range(72, X_EAST_END, 24))                                # bay centres of the tier-3 strip, 72 .. 912
XCW = list(range(144, X_EAST_END, 24))                               # bay centres east of x = +132, 144 .. 912
for xc in XC3:
    for yc in range(-56, 57, 8):
        put("roof_unit", f"ROOF3_{xc:+d}_{yc:+d}", xc, yc, GIRDER_TOP[2], part_kind="roof", tier=3)
for xc in XCW:
    for sy in (-1, 1):
        for yc in range(64, 129, 8): put("roof_unit", f"ROOF2_{xc:+d}_{sy*yc:+d}", xc, sy * yc, GIRDER_TOP[1], part_kind="roof", tier=2)
        for yc in range(136, 201, 8): put("roof_unit", f"ROOF1_{xc:+d}_{sy*yc:+d}", xc, sy * yc, GIRDER_TOP[0], part_kind="roof", tier=1)
def wall_bay(tag, x, y, z0, glazed, rot):
    k = "wall_g" if glazed else "wall_b"; H = H_G if glazed else H_B
    put(k, f"WALL_{tag}", x, y, z0, rot, part_kind="wall")
    put(k + "_fill", f"WALLF_{tag}", x, y, z0, rot, part_kind="wall_fill")
    put("wall_louvre", f"WLOUV_{tag}", x, y, z0 + H, rot, part_kind="louvre")
for sy in (-1, 1):
    s = "N" if sy > 0 else "S"
    for xc in XC3: wall_bay(f"T3{s}_{xc}", xc, sy * 60, GIRDER_TOP[1], True, 0.0)
    for xc in XCW:
        wall_bay(f"T2{s}_{xc}", xc, sy * 132, GIRDER_TOP[0], True, 0.0)
        wall_bay(f"T1{s}_{xc}", xc, sy * 204, 0.0, False, 0.0)
for yc in range(-192, 193, 24): wall_bay(f"E1_{yc}", X_EAST_END, yc, 0.0, False, math.pi / 2)
for yc in range(-120, 121, 24): wall_bay(f"E2_{yc}", X_EAST_END, yc, GIRDER_TOP[0], True, math.pi / 2)
for yc in range(-48, 49, 24): wall_bay(f"E3_{yc}", X_EAST_END, yc, GIRDER_TOP[1], True, math.pi / 2)
hidden = []
for o in bpy.data.objects:   # FT84 (= FT77)
    if o.name.startswith(("WALL_A+1", "WALLF_A+1", "WLOUV_A+1")) and abs(o.location.y / FT) < 132:
        o.hide_render = True; o.hide_viewport = True; o[TAG] = "FT84 hidden: interior once the east block exists"; hidden.append(o.name)
timber = bpy.data.materials["GT_Timber"]
def slab(name, x0, x1, y0, y1, z_top, t, mat, kind):
    bm = bmesh.new()
    vs = [bm.verts.new((ft(a), ft(b), ft(c))) for (a, b, c) in
          [(x0, y0, z_top - t), (x1, y0, z_top - t), (x1, y1, z_top - t), (x0, y1, z_top - t),
           (x0, y0, z_top), (x1, y0, z_top), (x1, y1, z_top), (x0, y1, z_top)]]
    for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]: bm.faces.new([vs[i] for i in f])
    me = bpy.data.meshes.new("C29_" + name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
    o = bpy.data.objects.new("C29_" + name, me); coll.objects.link(o); o[TAG] = "FT82/FT83"; o["part_kind"] = kind
    return o
GAL_TOP = 22 + 11 / 12; GAL_T = 0.75
for sy in (-1, 1):
    for (a, b) in ((36, 60), (108, 132)):
        y0, y1 = sorted((sy * a, sy * b))
        slab(f"GAL_E_{sy:+d}_{a}", 132, X_EAST_END, y0, y1, GAL_TOP, GAL_T, timber, "gallery_floor")
    for xc in XC3: put("railing24", f"RAIL_NV_{sy:+d}_{xc}", xc, sy * 36, GAL_TOP, part_kind="balustrade")
    for xc in XCW:
        for yy in (60, 108): put("railing24", f"RAIL_AV_{sy:+d}_{yy}_{xc}", xc, sy * yy, GAL_TOP, part_kind="balustrade")
fb = bpy.data.objects["FLOOR_BOARDS"]
ztop = max((fb.matrix_world @ Vector(c)).z for c in fb.bound_box) / FT
slab("FLOOR_E", 144, X_EAST_END + 0.5, -204, 204, ztop, 0.5, fb.material_slots[0].material, "floor_ground")
# figures standing inside a new column: hide (none expected; checked)
fig_hidden = []
for o in bpy.data.objects:
    if o.get("part_kind") == "figure" or o.name.startswith(("CROWD", "KWORKER")):
        for (x, y) in new_cols:
            if abs(o.location.x / FT - x) < 1.6 and abs(o.location.y / FT - y) < 1.6:
                o.hide_render = True; fig_hidden.append(o.name); break
# FT85 (= FT71): gallery-level figures not over any gallery deck are hidden
decks = []
for o in bpy.data.objects:
    if o.type == 'MESH' and not o.hide_render and (o.name.startswith("GAL_") or o.name.startswith("C29_GAL_")):
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        decks.append((min(v.x for v in bb) / FT, max(v.x for v in bb) / FT, min(v.y for v in bb) / FT, max(v.y for v in bb) / FT,
                      max(v.z for v in bb) / FT))
float_report = []
for o in bpy.data.objects:
    if not o.name.startswith("CROWD") or o.hide_render: continue
    z = o.location.z / FT
    if z < 10: continue
    x, y = o.location.x / FT, o.location.y / FT
    on = any(x0 + 0.5 <= x <= x1 - 0.5 and y0 + 0.5 <= y <= y1 - 0.5 and abs(zt - z) < 1.0 for (x0, x1, y0, y1, zt) in decks)
    if not on:
        float_report.append((o.name, round(x), round(y), round(z, 1)))
        o.hide_render = True; o.hide_viewport = True; o[TAG] = "FT85 hidden: floating gallery figure, no deck under feet"
info = {"parts": dict(sorted(count.items())), "new_cols": len(new_cols), "hidden_walls": len(hidden), "fig_hidden": fig_hidden,
        "float_hidden": float_report, "n_decks": len(decks),
        "wall_h": (round(H_G, 2), round(H_B, 2)), "floor_ztop_ft": round(ztop, 3)}
sc["cp029_east"] = TAG
print("CP029_EAST", info, flush=True)
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
print("SAVED", OUT, flush=True)
