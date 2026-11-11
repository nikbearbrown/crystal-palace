"""CP020 "Preparing for feet and crowds" nave CANDIDATE (2026-11-11, DEPARTURES FT60-FT66). NOT live, no verdict.
  blender -b -P scripts/cand_cp020_nave_20261111.py -- --src rounds/f03.blend --out rounds/candidates/f03_cp020nave.blend
Hyde Park 1851 fit-out state only (Jan-Apr 1851); nothing Sydenham.

Live CP020_floor_start looks west down the nave from the unboarded east-nave patch. Because f03 is the transept model
(|x| <= 132 ft; the nave tier-3 strip |y| < 60 beyond x = +-60 and everything beyond x = +-132 was left to a nave model),
the left third of the frame runs out past x = -144 onto open park with a flat horizon, and the nave over the camera
has no roof, so the top-left is open sky. This candidate continues the building with f03's OWN part library
(linked meshes col_22/42/62, girder24, truss72, roof_unit, wall_24_* bays + fills, wall_louvre, railing24), on Downes'
24 ft grid, using the same rules as the transept folder's KEEP envelope v2 (apply_envelope_v2.py, ENV2-02..10),
mirrored west and run to the true west end:
  FT60  nave tier-3 strip |y| <= 60 for x 60..132 and -60..-132 (columns on y = +-36, 72 ft light trusses, roof units,
        tier-3 clerestory at y = +-60, nave-front railings at y = +-36).
  FT61  the full three-tier section west of x = -132 to x = -924 (1,848 ft between end column centres, transept at the
        middle; SURVEY: length 1,848 ft, tier widths 408 / 264 / 120 ft), galleries over the aisles |y| 36..60, 108..132.
  FT62  a west end at x = -924: boarded ground tier, glazed tier-2/3 bays, end columns at (-924, +-12) (C02 pattern).
  FT63  floor boards continued x -924..-144 (GT_FloorBoards, object coords at the origin).
  FT64  the west arm's x = -132 tier-2 side walls for |y| < 132 hidden (interior once the west block exists).
  FT65  new ironwork uses the part meshes' own painted materials (GT_IronColumn_OJ / GT_IronGirder_OJ); no new paint.
Lighting, world, exposure, figures and every existing object are unchanged (people are swapped at render time exactly
as for the live frame)."""
import bpy, bmesh, math, os, sys
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
SRC, OUT = arg("--src"), arg("--out")
assert os.path.abspath(SRC) != os.path.abspath(OUT), "refusing to overwrite the source blend"
assert not os.path.abspath(OUT).endswith("rounds/f03.blend"), "refusing to overwrite live f03"
bpy.ops.wm.open_mainfile(filepath=SRC)
try: bpy.context.preferences.filepaths.save_version = 0
except Exception: pass
sc = bpy.context.scene
FT = 0.3048
def ft(v): return v * FT
TAG = "cp020_nave_20261111"
GIRDER_TOP = [22 + 2 / 12, 42 + 2 / 12, 62 + 2 / 12]   # D11a-c, as build_transept.py / apply_envelope_v2.py
X_WEST_END = -924                                     # 1,848 ft between end column centres, transept at the middle

LIB = {k: bpy.data.meshes[k] for k in ("col_22", "col_42", "col_62", "girder24", "truss72", "roof_unit", "wall_louvre", "railing24")}
def mesh_like(prefix):
    for me in bpy.data.meshes:
        if me.name.startswith(prefix): return me
    raise KeyError(prefix)
LIB["wall_g"] = mesh_like("wall_24_14.4"); LIB["wall_g_fill"] = bpy.data.meshes[LIB["wall_g"].name + "_fill"]
LIB["wall_b"] = mesh_like("wall_24_16.6"); LIB["wall_b_fill"] = bpy.data.meshes[LIB["wall_b"].name + "_fill"]
H_G = max(v.co.z for v in LIB["wall_g"].vertices) / FT
H_B = max(v.co.z for v in LIB["wall_b"].vertices) / FT

coll = bpy.data.collections.new("C20_NAVE"); sc.collection.children.link(coll)
coll["candidate"] = TAG
coll["credit"] = "Grok Bot: f03's own transept part library continued along the nave on Downes' 24 ft grid (CP020 candidate)"
count = {}
def put(key, name, x, y, z, rot=0.0, **props):
    o = bpy.data.objects.new("C20_" + name, LIB[key])
    o.location = (ft(x), ft(y), ft(z)); o.rotation_euler = (0, 0, rot)
    coll.objects.link(o); o[TAG] = "FT60-FT62"
    for k, v in props.items(): o[k] = v
    count[key] = count.get(key, 0) + 1
    return o

cols = {}
for o in bpy.data.objects:
    if o.name.startswith("COL_") and o.type == 'MESH' and "tier" in o:
        cols[(round(o.location.x / FT), round(o.location.y / FT))] = int(o["tier"])
existing = set(cols)
ROWS_Y = [-204 + 24 * j for j in range(18)]
X_EAST = [84, 108, 132]
X_WEST = list(range(-84, X_WEST_END - 1, -24))        # -84 .. -924
def tier_of(y):
    ay = abs(y); return 3 if ay <= 60 else (2 if ay <= 132 else 1)
new_cols = {}
for x in X_EAST + X_WEST:
    for y in ROWS_Y:
        if abs(y) < 36 or (x, y) in existing: continue
        if abs(x) <= 132 and abs(y) > 60: continue
        new_cols[(x, y)] = tier_of(y)
for y in (-12, 12): new_cols[(X_WEST_END, y)] = 3     # end-screen columns across the 72 ft nave (C02 pattern)
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
gird((X_WEST_END, -36), (X_WEST_END, -12), "Y"); gird((X_WEST_END, 12), (X_WEST_END, 36), "Y")
for x in X_EAST + X_WEST:
    put("truss72", f"TRUSS72_X{x:+04d}", x, 0, GIRDER_TOP[2], math.pi / 2, part_kind="truss", span_ft=72, strength="light")
XC3 = [72, 96, 120] + list(range(-72, X_WEST_END - 1, -24))          # bay centres of the tier-3 strip
XCW = list(range(-144, X_WEST_END - 1, -24))                         # bay centres west of x = -132
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
for yc in range(-192, 193, 24): wall_bay(f"W1_{yc}", X_WEST_END, yc, 0.0, False, math.pi / 2)
for yc in range(-120, 121, 24): wall_bay(f"W2_{yc}", X_WEST_END, yc, GIRDER_TOP[0], True, math.pi / 2)
for yc in range(-48, 49, 24): wall_bay(f"W3_{yc}", X_WEST_END, yc, GIRDER_TOP[1], True, math.pi / 2)
hidden = []
for o in bpy.data.objects:   # FT64
    if o.name.startswith(("WALL_A-1", "WALLF_A-1", "WLOUV_A-1")) and abs(o.location.y / FT) < 132:
        o.hide_render = True; o.hide_viewport = True; o[TAG] = "FT64 hidden: interior once the west block exists"; hidden.append(o.name)
timber = bpy.data.materials["GT_Timber"]
def slab(name, x0, x1, y0, y1, z_top, t, mat, kind):
    bm = bmesh.new()
    vs = [bm.verts.new((ft(a), ft(b), ft(c))) for (a, b, c) in
          [(x0, y0, z_top - t), (x1, y0, z_top - t), (x1, y1, z_top - t), (x0, y1, z_top - t),
           (x0, y0, z_top), (x1, y0, z_top), (x1, y1, z_top), (x0, y1, z_top)]]
    for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]: bm.faces.new([vs[i] for i in f])
    me = bpy.data.meshes.new("C20_" + name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
    o = bpy.data.objects.new("C20_" + name, me); coll.objects.link(o); o[TAG] = "FT61/FT63"; o["part_kind"] = kind
    return o
GAL_TOP = 22 + 11 / 12; GAL_T = 0.75
for sy in (-1, 1):
    for (a, b) in ((36, 60), (108, 132)):
        y0, y1 = sorted((sy * a, sy * b))
        slab(f"GAL_W_{sy:+d}_{a}", X_WEST_END, -132, y0, y1, GAL_TOP, GAL_T, timber, "gallery_floor")
    for xc in XC3: put("railing24", f"RAIL_NV_{sy:+d}_{xc}", xc, sy * 36, GAL_TOP, part_kind="balustrade")
    for xc in XCW:
        for yy in (60, 108): put("railing24", f"RAIL_AV_{sy:+d}_{yy}_{xc}", xc, sy * yy, GAL_TOP, part_kind="balustrade")
fb = bpy.data.objects["FLOOR_BOARDS_W"]
ztop = max((fb.matrix_world @ Vector(c)).z for c in fb.bound_box) / FT
slab("FLOOR_W", X_WEST_END - 0.5, -144, -204, 204, ztop, 0.5, fb.material_slots[0].material, "floor_ground")
# figures standing inside a new column: hide (none expected; checked)
fig_hidden = []
for o in bpy.data.objects:
    if o.get("part_kind") == "figure" or o.name.startswith(("CROWD", "KWORKER")):
        for (x, y) in new_cols:
            if abs(o.location.x / FT - x) < 1.6 and abs(o.location.y / FT - y) < 1.6:
                o.hide_render = True; fig_hidden.append(o.name); break
info = {"parts": dict(sorted(count.items())), "new_cols": len(new_cols), "hidden_walls": len(hidden), "fig_hidden": fig_hidden,
        "wall_h": (round(H_G, 2), round(H_B, 2)), "floor_ztop_ft": round(ztop, 3)}
sc["cp020_nave"] = TAG
print("CP020_NAVE", info, flush=True)
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
print("SAVED", OUT, flush=True)
