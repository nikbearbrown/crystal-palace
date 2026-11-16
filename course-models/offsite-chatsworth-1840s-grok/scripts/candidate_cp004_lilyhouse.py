"""CP004 'Learning to repeat' — Victoria regia lily house, Chatsworth, spring 1850 (completed state).
CANDIDATE 2026-11-16 (Grok; not live, no verdict). DEPARTURES CH07-CH16.

blender -b rounds/ch02.blend -P scripts/candidate_cp004_lilyhouse.py -- --out rounds/candidates/ch02_cp004lily.blend

Runs on the LIVE round rounds/ch02.blend (md5 59eca5d7, never written) and saves a sibling candidate.
Hero camera CP004_lily_tank_start is NOT moved; no camera, world, sun, fill light, exposure or existing
material is edited. Changes, all inside LILY_HOUSE (x = 200 ft offset):
  * old lily shell (dwarf wall + 14 iron columns on a 12 ft grid, 4 of them standing in the tank water), old
    part-width roof (ridges stop 6.5 ft short of the side walls), old box-segment tank ring and the 10 old pads
    (radius 3.8-5.2 ft = 7.6-10.4 ft leaves, floating 0.7-0.85 ft above the water) are hidden, not deleted;
  * rebuilt per the sources: 61 x 49 ft house on a 37 in masonry base with 30 low-level vent openings; walls
    are one repeated iron-and-glass module (4 ft bays, 1 ft panes, transom); flat ridge-and-furrow roof over
    the full plan (8 bays, trussed timber Paxton gutters on two lines of girders); only 8 hollow cast-iron
    columns (drainpipes, two rows of 4 clear of the tank); 33 ft circular tank with stone coping and dark still
    water; one Victoria plant: ~23 leaves 3.6-5.2 ft across with low upturned red rims and drainage notch, young
    leaves, 2 flowers (white first night, pink second night); 8 small corner tanks (Nymphaea, Nelumbium,
    Pontederia); a lawn + gravel apron outside so the glass shows ground instead of a void;
  * the turned-over leaf on its trestle stands in the tank water; it is kept for the two detail cameras via the
    existing render_views only_cams tag (CP004_lily_underside, CP004_learning) and so not drawn in the hero;
  * the 4 lily-house figures (Paxton, 2 visitors, boy) stood in/on the tank: moved onto the far walk.
"""
import bpy, sys, os, math, json, random, hashlib
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grokkit as G
from grokkit import ft, Kit
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = os.path.abspath(argv[argv.index("--out") + 1]) if "--out" in argv else "/tmp/ch02_cp004lily.blend"
SRC = os.path.abspath(bpy.data.filepath)
LIVE = os.path.abspath(os.path.join(HERE, "..", "rounds", "ch02.blend"))
assert OUT != LIVE and not OUT.endswith("/rounds/ch02.blend"), "refusing to overwrite the live round"
assert "CP4_LILY_HOUSE_1850" not in bpy.data.collections, "source already has the CP004 candidate"
G.PFX = "CP4_"
R = random.Random(18500)
info = {"src": SRC, "src_md5": hashlib.md5(open(SRC, "rb").read()).hexdigest()}
LX = 200.0; LW, LL = 61.0, 49.0; HX, HY = LW / 2, LL / 2

# ---------- materials: reuse the live CH_ materials, add a few new CP4_ ones ----------
Mm = bpy.data.materials
def mnew(n, c, r=0.7, m=0.0, spec=None):
    M = G.mat(n, c, r, m)
    if spec is not None: M.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = spec
    return M
def water_mat():
    M = bpy.data.materials.new("CP4_TankWater"); M.use_nodes = True; b = M.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.020, 0.032, 0.026, 1); b.inputs["Roughness"].default_value = 0.035
    b.inputs["IOR"].default_value = 1.333; M.diffuse_color = (0.02, 0.03, 0.03, 1); return M
MAT = dict(
    paint=Mm["CH_WhitePaint"], iron=Mm["CH_Iron"], glass=Mm["CH_Glass"], stone=Mm["CH_Stone"], brick=Mm["CH_Brick"],
    path=Mm["CH_Path"], deal=Mm["CH_Deal"], leaf=mnew("VictoriaTop", (0.075, 0.20, 0.05), 0.5), flower=Mm["CH_Flower"], soil=Mm["CH_Soil"],
    water=water_mat(), rim=mnew("LeafRim", (0.30, 0.07, 0.08), 0.6), vein=mnew("LeafVein", (0.10, 0.25, 0.07), 0.55), rimin=mnew("LeafRimInner", (0.12, 0.16, 0.05), 0.55),
    white=mnew("FlowerWhite", (0.85, 0.83, 0.76), 0.5), young=mnew("LeafYoung", (0.32, 0.12, 0.10), 0.55),
    nym=mnew("NymphaeaLeaf", (0.07, 0.24, 0.07), 0.45), lotus=mnew("LotusLeaf", (0.20, 0.34, 0.20), 0.8),
    reed=mnew("PontederiaLeaf", (0.09, 0.30, 0.08), 0.6), blue=mnew("PontederiaFlower", (0.25, 0.25, 0.65), 0.6),
    lawn=mnew("Lawn", (0.10, 0.20, 0.06), 0.95), grille=mnew("VentGrille", (0.03, 0.03, 0.03), 0.6))
ML = list(MAT.values()); IX = {k: i for i, k in enumerate(MAT)}
def K(): return Kit(ML)
def I(k): return IX[k]

LILY = bpy.data.collections["LILY_HOUSE"]
C = bpy.data.collections.new("CP4_LILY_HOUSE_1850"); LILY.children.link(C)
C["state_date"] = "spring 1850 (house completed; Victoria regia moved in from the 1849 tank)"
C["sources"] = "Gardeners' Chronicle 1850 description via thegardenhistory.blog 2018-07-14; WIT Trans. DN100071 (Victoria regia's bequest); Chadwick 1961 (8 hollow columns)"

# ---------- hide superseded live geometry (not deleted) ----------
hidden = []
for n in ["CH_Lily_shell", "CH_Lily_roof_bars", "CH_Lily_glass", "CH_Lily_tank"] + [f"CH_Pad_{i}" for i in range(10)]:
    o = bpy.data.objects[n]; o.hide_render = True; o.hide_viewport = True; o["cp4_superseded"] = 1; hidden.append(n)
info["hidden"] = hidden
for n in ("CH_Trestle", "CH_UndersideLeaf"):
    bpy.data.objects[n]["only_cams"] = "CP004_lily_underside,CP004_learning"
info["only_cams"] = {"CH_Trestle": "CP004_lily_underside,CP004_learning", "CH_UndersideLeaf": "CP004_lily_underside,CP004_learning"}

# ---------- floor, 37 in masonry base, vents, lawn ----------
BASE_H = 37 / 12.0; WT = 1.25
k = K()
k.box(I("stone"), LX - HX - 1, LX + HX + 1, -HY - 1, HY + 1, -0.4, 0)
k.box(I("path"), LX - HX + WT, LX + HX - WT, -HY + WT, HY - WT, -0.02, 0.02)
k.box(I("brick"), LX - HX, LX + HX, -HY, -HY + WT, 0, BASE_H); k.box(I("brick"), LX - HX, LX + HX, HY - WT, HY, 0, BASE_H)
k.box(I("brick"), LX - HX, LX - HX + WT, -HY + WT, HY - WT, 0, BASE_H); k.box(I("brick"), LX + HX - WT, LX + HX, -HY + WT, HY - WT, 0, BASE_H)
# stone sill on the base
k.box(I("stone"), LX - HX - 0.15, LX + HX + 0.15, -HY - 0.15, -HY + WT + 0.1, BASE_H, BASE_H + 0.25)
k.box(I("stone"), LX - HX - 0.15, LX + HX + 0.15, HY - WT - 0.1, HY + 0.15, BASE_H, BASE_H + 0.25)
k.box(I("stone"), LX - HX - 0.15, LX - HX + WT + 0.1, -HY + WT, HY - WT, BASE_H, BASE_H + 0.25)
k.box(I("stone"), LX + HX - WT - 0.1, LX + HX + 0.15, -HY + WT, HY - WT, BASE_H, BASE_H + 0.25)
k.done("CP4_floor_base", C)
SILL = BASE_H + 0.25
# 30 low-level openings in the base (source count): 9 per long wall, 6 per short wall, inner face grilles
v = K(); nv = 0
for side in (-1, 1):
    for i in range(9):
        x = LX - HX + (i + 0.5) * LW / 9; y = side * (HY - WT) - side * 0.02
        v.box(I("grille"), x - 0.55, x + 0.55, min(y, y - side * 0.06), max(y, y - side * 0.06), 0.7, 1.3); nv += 1
    for i in range(6):
        y = -HY + (i + 0.5) * LL / 6; x = LX + side * (HX - WT) - side * 0.02
        v.box(I("grille"), min(x, x - side * 0.06), max(x, x - side * 0.06), y - 0.55, y + 0.55, 0.7, 1.3); nv += 1
v.done("CP4_base_vents", C); info["base_vents"] = nv
g = K()
g.box(I("lawn"), LX - 100, LX + 100, -100, 100, -0.12, -0.06)
g.box(I("path"), LX - HX - 7, LX + HX + 7, -HY - 7, HY + 7, -0.06, -0.01)
# named "turf", not lawn/grass/gravel: crystal_palace_look._ensure_horizon_ground() samples any object whose name has
# ground/lawn/grass/gravel/soil/... to re-tint and re-height its CPL_HorizonGround for EVERY camera (it took this mesh's
# first material, cream paint, and lit up the CP003 stove horizon). The live horizon disk must stay as it is.
lawn = g.done("CP4_outside_turf_apron", C)
lawn["only_cams"] = "CP004_lily_tank,CP004_learning,CP004_lily_underside"   # keeps the CP003 stove views free of it (seen on the horizon)

# ---------- walls: one repeated iron-and-glass module ----------
EAVE = 16.0; TRANSOM = 9.5
w = K(); gl = K(); nb = 0
def wall(p0, p1, nbays):
    global nb
    P0, P1 = Vector(p0), Vector(p1); d = (P1 - P0) / nbays
    for b in range(nbays + 1):
        p = P0 + d * b; w.bar(I("paint"), (p.x, p.y, SILL), (p.x, p.y, EAVE), 0.32, 0.42)    # module mullion
    for b in range(nbays):
        a = P0 + d * b; e = a + d
        for s in (1, 2, 3):   # 3 sash bars per 4 ft bay (1 ft panes)
            q = a + d * (s / 4); w.bar(I("paint"), (q.x, q.y, SILL), (q.x, q.y, EAVE), 0.09, 0.14)
        gl.quad(I("glass"), [(a.x, a.y, SILL), (e.x, e.y, SILL), (e.x, e.y, EAVE), (a.x, a.y, EAVE)]); nb += 1
    for z, s_ in ((SILL + 0.1, 0.25), (TRANSOM, 0.28), (EAVE - 0.2, 0.4)):
        w.bar(I("paint"), (P0.x, P0.y, z), (P1.x, P1.y, z), s_, 0.36)
inset = WT / 2
wall((LX - HX + inset, -HY + inset), (LX + HX - inset, -HY + inset), 15)
wall((LX - HX + inset, HY - inset), (LX + HX - inset, HY - inset), 15)
wall((LX - HX + inset, -HY + inset), (LX - HX + inset, HY - inset), 12)
wall((LX + HX - inset, -HY + inset), (LX + HX - inset, HY - inset), 12)
w.done("CP4_wall_frames", C); gl.done("CP4_wall_glass", C, part="glass"); info["wall_bays"] = nb

# ---------- 8 hollow cast-iron columns + 2 girder lines ----------
COLS = [(LX + x, y) for y in (-19.5, 19.5) for x in (-22.5, -7.5, 7.5, 22.5)]
c = K()
for (x, y) in COLS:
    c.box(I("stone"), x - 0.6, x + 0.6, y - 0.6, y + 0.6, 0, 0.5)
    c.cyl(I("paint"), (x, y, 0.5), (x, y, 1.2), 0.42, 16, True, 0.32)
    c.cyl(I("paint"), (x, y, 1.2), (x, y, 14.3), 0.30, 16)
    c.cyl(I("paint"), (x, y, 14.3), (x, y, 14.8), 0.30, 16, True, 0.48)
GT, GB = EAVE - 0.15, 14.8
for y in (-19.5, 19.5):
    x0, x1 = LX - HX + inset, LX + HX - inset
    c.box(I("paint"), x0, x1, y - 0.35, y + 0.35, GT - 0.12, GT)        # top flange
    c.box(I("paint"), x0, x1, y - 0.35, y + 0.35, GB, GB + 0.12)        # bottom flange
    nlat = 30
    for i in range(nlat):                                               # lattice web
        xa = x0 + (x1 - x0) * i / nlat; xb = x0 + (x1 - x0) * (i + 1) / nlat
        za, zb = (GB + 0.12, GT - 0.12) if i % 2 == 0 else (GT - 0.12, GB + 0.12)
        c.bar(I("paint"), (xa, y, za), (xb, y, zb), 0.1, 0.12)
c.done("CP4_columns_girders", C); info["columns"] = len(COLS)

# ---------- flat ridge-and-furrow roof over the whole plan ----------
NB = 8; BW = LW / NB; RISE = 1.55
rf = K(); rg = K(); ng = 0
GX = [LX - HX + i * BW for i in range(NB + 1)]
for i, x in enumerate(GX):   # Paxton gutters (furrows) along Y
    xs = min(max(x, LX - HX + 0.3), LX + HX - 0.3)
    rf.box(I("deal"), xs - 0.28, xs + 0.28, -HY + inset, HY - inset, EAVE - 0.05, EAVE + 0.35); ng += 1
    if 0 < i < NB:   # trussed gutter: rod under each span + struts (Crystal Palace pattern)
        for (ya, yb) in ((-HY + inset, -19.5), (-19.5, 19.5), (19.5, HY - inset)):
            span = yb - ya
            if span < 8: continue
            sag = min(1.4, span / 26); y1, y2 = ya + span / 3, ya + 2 * span / 3
            pts = [(xs, ya, EAVE), (xs, y1, EAVE - sag), (xs, y2, EAVE - sag), (xs, yb, EAVE)]
            for p, q in zip(pts, pts[1:]): rf.bar(I("iron"), p, q, 0.06)
            for yy in (y1, y2): rf.bar(I("paint"), (xs, yy, EAVE - sag), (xs, yy, EAVE - 0.05), 0.12)
for i in range(NB):
    xa, xb = GX[i], GX[i + 1]; xm = (xa + xb) / 2; zt = EAVE + 0.35 + RISE
    rf.bar(I("deal"), (xm, -HY + inset, zt), (xm, HY - inset, zt), 0.22, 0.25)   # ridge
    ny = int(round((LL - WT) / 1.0))
    for j in range(ny + 1):   # sash bars every ~1 ft, gutter -> ridge -> gutter
        y = -HY + inset + j * (LL - WT) / ny
        rf.bar(I("paint"), (xa, y, EAVE + 0.35), (xm, y, zt), 0.08, 0.12); rf.bar(I("paint"), (xm, y, zt), (xb, y, EAVE + 0.35), 0.08, 0.12)
    for (p0, p1) in ((xa, xm), (xm, xb)):
        z0 = EAVE + 0.35 if p0 == xa else zt; z1 = zt if p0 == xa else EAVE + 0.35
        rg.quad(I("glass"), [(p0, -HY + inset, z0 + 0.05), (p1, -HY + inset, z1 + 0.05), (p1, HY - inset, z1 + 0.05), (p0, HY - inset, z0 + 0.05)])
# gable infill at the two long-wall ends of each ridge (glass triangles above the wall head)
for y in (-HY + inset, HY - inset):
    for i in range(NB):
        xa, xb = GX[i], GX[i + 1]; xm = (xa + xb) / 2
        rg.poly(I("glass"), [(xa, y, EAVE + 0.35), (xb, y, EAVE + 0.35), (xm, y, EAVE + 0.35 + RISE)])
rf.done("CP4_roof_frame", C); rg.done("CP4_roof_glass", C, part="glass"); info["roof_bays"] = NB; info["gutters"] = ng

# ---------- 33 ft tank ----------
TR = 33.0 / 2; COPE_H = 2.55; WATER_Z = 2.05
t = K()
t.lathe(I("stone"), (LX, 0), [(TR + 1.0, 0.0), (TR + 1.0, COPE_H - 0.15), (TR + 1.15, COPE_H - 0.15), (TR + 1.15, COPE_H), (TR - 0.1, COPE_H), (TR - 0.1, COPE_H - 0.12), (TR, COPE_H - 0.12), (TR, WATER_Z - 0.6)], seg=96)
t.done("CP4_tank_wall", C, smooth=True)
wt = K(); wt.lathe(I("water"), (LX, 0), [(TR + 0.02, WATER_Z), (0.0, WATER_Z)], seg=96); wt.done("CP4_tank_water", C)
info["tank_d_ft"] = 2 * TR

# ---------- Victoria regia leaves ----------
def victoria_leaf(k, x, y, r, rot, rim=0.13, notch=True, young=False):
    n = 40; z = WATER_Z + 0.015
    na = 0.10 if notch else 0.0   # drainage notch half-angle (rad) in the rim
    for j in range(n):
        a0 = rot + 2 * math.pi * j / n; a1 = rot + 2 * math.pi * (j + 1) / n
        for ring in range(3):
            r0, r1 = r * ring / 3, r * (ring + 1) / 3
            dz0, dz1 = 0.04 * (1 - (r0 / r) ** 2), 0.04 * (1 - (r1 / r) ** 2)
            k.quad(I("young" if young else "leaf"), [(x + r0 * math.cos(a0), y + r0 * math.sin(a0), z + dz0), (x + r0 * math.cos(a1), y + r0 * math.sin(a1), z + dz0),
                                                     (x + r1 * math.cos(a1), y + r1 * math.sin(a1), z + dz1), (x + r1 * math.cos(a0), y + r1 * math.sin(a0), z + dz1)])
        am = (a0 + a1) / 2 - rot
        if notch and (abs(am) < na or abs(am - 2 * math.pi) < na): continue
        h = rim
        k.quad(I("rim"), [(x + r * math.cos(a0), y + r * math.sin(a0), z), (x + r * math.cos(a1), y + r * math.sin(a1), z),
                          (x + (r + 0.05) * math.cos(a1), y + (r + 0.05) * math.sin(a1), z + h), (x + (r + 0.05) * math.cos(a0), y + (r + 0.05) * math.sin(a0), z + h)])
        ri = r - 0.035   # inner (green) face of the rim, offset so the two faces never coincide
        k.quad(I("rimin"), [(x + (ri + 0.05) * math.cos(a0), y + (ri + 0.05) * math.sin(a0), z + h), (x + (ri + 0.05) * math.cos(a1), y + (ri + 0.05) * math.sin(a1), z + h),
                            (x + ri * math.cos(a1), y + ri * math.sin(a1), z + 0.03), (x + ri * math.cos(a0), y + ri * math.sin(a0), z + 0.03)])
        k.quad(I("rim"), [(x + (r + 0.05) * math.cos(a0), y + (r + 0.05) * math.sin(a0), z + h), (x + (r + 0.05) * math.cos(a1), y + (r + 0.05) * math.sin(a1), z + h),
                          (x + (ri + 0.05) * math.cos(a1), y + (ri + 0.05) * math.sin(a1), z + h), (x + (ri + 0.05) * math.cos(a0), y + (ri + 0.05) * math.sin(a0), z + h)])
    if not young:   # quilted top: raised radial + ring veins (the underside rib net shows through)
        for j in range(16):
            a = rot + 2 * math.pi * (j + 0.5) / 16
            k.bar(I("vein"), (x + 0.15 * math.cos(a), y + 0.15 * math.sin(a), z + 0.05), (x + (r - 0.1) * math.cos(a), y + (r - 0.1) * math.sin(a), z + 0.012), 0.025, 0.012)
        for rr in (0.55,):
            for j in range(24):
                a0 = rot + 2 * math.pi * j / 24; a1 = rot + 2 * math.pi * (j + 1) / 24; R0 = r * rr; zz = z + 0.04 * (1 - rr * rr) + 0.012
                k.bar(I("vein"), (x + R0 * math.cos(a0), y + R0 * math.sin(a0), zz), (x + R0 * math.cos(a1), y + R0 * math.sin(a1), zz), 0.022, 0.01)
TRESTLE = (5.0, 6.5, 5.6)   # live trestle leaf (x, y offsets, keep-out radius) — still drawn in the two detail cams
pads = []
def free(x, y, r):
    if math.hypot(x, y) + r > TR - 0.6: return False
    if math.hypot(x - TRESTLE[0], y - TRESTLE[1]) < r + TRESTLE[2]: return False
    return all(math.hypot(x - px, y - py) > r + pr + 0.25 for px, py, pr in pads)
for ring_r, n_try, (rmin, rmax) in ((4.6, 7, (1.8, 2.15)), (9.6, 12, (2.1, 2.6)), (13.6, 14, (1.8, 2.3))):
    off = R.uniform(0, 2 * math.pi)
    for i in range(n_try):
        a = off + 2 * math.pi * i / n_try
        for _ in range(12):
            r = R.uniform(rmin, rmax); rr = ring_r + R.uniform(-0.6, 0.6); aa = a + R.uniform(-0.12, 0.12)
            x, y = rr * math.cos(aa), rr * math.sin(aa)
            if free(x, y, r): pads.append((x, y, r)); break
lk = K()
for (x, y, r) in pads:
    victoria_leaf(lk, LX + x, y, r, math.atan2(y, x) + math.pi)   # notch points at the crown (petiole side)
young = []
for a in (1.5, 3.0):   # young red leaves just opening, clear of the 2 flowers
    x, y, r = 1.6 * math.cos(a), 1.6 * math.sin(a), 0.7
    if free(x, y, r): young.append((x, y, r)); victoria_leaf(lk, LX + x, y, r, a + math.pi, rim=0.08, notch=False, young=True)
lk.done("CP4_victoria_leaves", C, part="pad")
info["victoria_leaves"] = len(pads); info["young_leaves"] = len(young)
info["leaf_diam_ft"] = [round(min(p[2] for p in pads) * 2, 2), round(max(p[2] for p in pads) * 2, 2)]
# flowers: first night white, second night pink (lathe cups on short stalks just clear of the water)
fk = K()
for (x, y, mat) in ((-0.9, -1.2, "white"), (1.3, 0.6, "flower")):
    X = LX + x
    fk.cyl(I("leaf"), (X, y, WATER_Z), (X, y, WATER_Z + 0.25), 0.12, 8)
    fk.lathe(I(mat), (X, y), [(0.15, WATER_Z + 0.25), (0.45, WATER_Z + 0.35), (0.62, WATER_Z + 0.55), (0.55, WATER_Z + 0.75), (0.35, WATER_Z + 0.82), (0.0, WATER_Z + 0.9)], seg=20)
    for p in range(12):   # outer petals
        a = 2 * math.pi * p / 12
        fk.bar(I(mat), (X + 0.3 * math.cos(a), y + 0.3 * math.sin(a), WATER_Z + 0.32), (X + 0.78 * math.cos(a), y + 0.78 * math.sin(a), WATER_Z + 0.62), 0.22, 0.04)
fk.done("CP4_victoria_flowers", C); info["flowers"] = 2

# ---------- 8 small corner tanks (other aquatics) ----------
ct = K(); cw = K(); cp = K(); ntank = 0
def corner_tank(x0, x1, y0, y1):
    global ntank
    ct.box(I("brick"), x0, x1, y0, y1, 0, COPE_H - 0.15)
    ct.box(I("stone"), x0 - 0.1, x1 + 0.1, y0 - 0.1, y0 + 0.35, COPE_H - 0.15, COPE_H); ct.box(I("stone"), x0 - 0.1, x1 + 0.1, y1 - 0.35, y1 + 0.1, COPE_H - 0.15, COPE_H)
    ct.box(I("stone"), x0 - 0.1, x0 + 0.35, y0, y1, COPE_H - 0.15, COPE_H); ct.box(I("stone"), x1 - 0.35, x1 + 0.1, y0, y1, COPE_H - 0.15, COPE_H)
    cw.box(I("water"), x0 + 0.35, x1 - 0.35, y0 + 0.35, y1 - 0.35, WATER_Z - 0.4, WATER_Z + 0.21)
    zt = WATER_Z + 0.22
    for _ in range(int((x1 - x0) * (y1 - y0) / 3.2)):   # Nymphaea pads + a few flowers
        r = R.uniform(0.35, 0.65); x = R.uniform(x0 + 0.4 + r, x1 - 0.4 - r); y = R.uniform(y0 + 0.4 + r, y1 - 0.4 - r)
        cp.cyl(I("nym"), (x, y, zt), (x, y, zt + 0.02), r, 14)
        if R.random() < 0.18: cp.cyl(I(R.choice(["white", "flower"])), (x, y, zt + 0.02), (x, y, zt + 0.25), 0.18, 8, True, 0.05)
    for _ in range(2):   # Nelumbium: cupped leaves held above the water
        x = R.uniform(x0 + 1, x1 - 1); y = R.uniform(y0 + 1, y1 - 1); h = R.uniform(1.5, 2.6)
        cp.cyl(I("lotus"), (x, y, zt), (x, y, zt + h), 0.03, 6)
        cp.lathe(I("lotus"), (x, y), [(0.0, zt + h), (0.5, zt + h + 0.08), (0.95, zt + h + 0.22)], seg=16)
    x = (x0 + x1) / 2 + R.uniform(-0.6, 0.6); y = (y0 + y1) / 2 + R.uniform(-0.4, 0.4)   # Pontederia clump
    for s in range(7):
        a = 2 * math.pi * s / 7; h = R.uniform(1.4, 2.2); tx, ty = x + 0.35 * math.cos(a), y + 0.35 * math.sin(a)
        cp.cyl(I("reed"), (x, y, zt), (tx, ty, zt + h), 0.03, 6)
        cp.cyl(I("reed"), (tx, ty, zt + h - 0.1), (tx + 0.25 * math.cos(a), ty + 0.25 * math.sin(a), zt + h + 0.45), 0.2, 8, True, 0.02)
    cp.cyl(I("blue"), (x, y, zt + 1.6), (x, y, zt + 2.5), 0.12, 8, True, 0.04)
    ntank += 1
for sx in (-1, 1):
    for sy in (-1, 1):
        xa, xb = sorted((LX + sx * 24.0, LX + sx * (HX - WT - 0.4))); corner_tank(xa, xb, *sorted((sy * 19.9, sy * (HY - WT - 0.4))))
        xa, xb = sorted((LX + sx * 25.3, LX + sx * (HX - WT - 0.4))); corner_tank(xa, xb, *sorted((sy * 10.5, sy * 17.2)))
ct.done("CP4_corner_tanks", C); cw.done("CP4_corner_tank_water", C); cp.done("CP4_corner_aquatics", C, part="plant"); info["corner_tanks"] = ntank

# ---------- figures off the tank, onto the far walk ----------
moves = {"CH_Paxton_lily": (LX - 5.5, 18.6, (LX - 3, 8)), "CH_Visitor_lily_m": (LX + 10.5, 18.0, (LX + 6, 6)),
         "CH_Visitor_lily_w": (LX + 12.2, 18.6, (LX + 6, 6)), "CH_Boy_lily": (LX + 2.0, 18.2, (LX + 1, 8))}
for n, (x, y, look) in moves.items():
    o = bpy.data.objects[n]; old = tuple(round(v / 0.3048, 2) for v in o.location)
    o.location = (ft(x), ft(y), 0.0); o.rotation_euler = (0, 0, G.heading(look[0] - x, look[1] - y)); info.setdefault("figures_moved", {})[n] = [old, [x, y, 0.0]]

for o in C.objects: o["cp4_candidate"] = 1
bpy.context.scene["grok_cp004_candidate"] = json.dumps(info)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True, copy=True)
print("CP004_CANDIDATE_SAVED", OUT, json.dumps(info))
