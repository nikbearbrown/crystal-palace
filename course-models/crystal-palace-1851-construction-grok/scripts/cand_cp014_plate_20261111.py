"""CP014_drain_whole "Downes plate" CANDIDATE 2026-11-11 (DEPARTURES KD07-KD13; no verdict, NOT live).
Reads the LIVE k01 (rounds/k01.blend, md5 6f647743..., never written) and saves rounds/candidates/k01_cp014plate.blend.
Hyde Park 1851 only (Downes 1852, Plates VIII, XII, XIII + text pp. 4-5, 14-16). Camera-scoped: every new object carries
only_cams=CP014_drain_whole; the live objects it replaces carry hide_cams=CP014_drain_whole, so CP014_drain_roof/gutter/base
render exactly as live. The old whole-shot labels are retagged only_cams=NONE_KD07 (never render).
  blender -b rounds/k01.blend -P scripts/cand_cp014_plate_20261111.py -- --out rounds/candidates/k01_cp014plate.blend"""
import bpy, bmesh, sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grokkit as G
from grokkit import ft, Kit
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/k01_cp014plate.blend"
ROOTDIR = os.path.dirname(HERE); OUT = OUT if os.path.isabs(OUT) else os.path.join(ROOTDIR, OUT)
SID = "CP014_drain_whole"; TAG = "KD07"
assert not any(o.name.startswith("KD7_") for o in bpy.data.objects), "candidate already applied"
D = bpy.data
def M(n): return D.materials["KD_" + n]
# live materials (same names as build_drain.py). KD13: red cut-face boxes sit 0.006 ft proud of the y=0 face they cover
# (the live coplanar boxes shade black: the concrete, base plate and brick drain cut faces in the live base/whole renders)
MAT = dict(iron=M("Iron"), cut=M("CutFace"), wood=M("Deal"), water=M("Water"), ink=M("Ink"), soil=M("Soil"),
           soilcut=M("SoilCut"), conc=M("Concrete"), brick=M("Brick"), grass=M("Ground"), lead=M("Lead"), arrow=M("Arrow"))
MAT["gravel"] = G.mat("KD7_GravelCut", (0.50, 0.44, 0.33), 0.95)
MAT["loamcut"] = G.mat("KD7_LoamCut", (0.40, 0.29, 0.19), 0.95)
ML = list(MAT.values()); IX = {k: i for i, k in enumerate(MAT)}
def K(): return Kit(ML)
def I(k): return IX[k]
COLL = G.coll("KD7_CP014_PLATE", D.collections["KDRAIN_K01"])
def done(kit, name, **pr):
    ob = kit.done(name, COLL, **pr); ob["only_cams"] = SID; return ob
def hide(name):
    assert not D.objects[name].get("only_cams"), name   # render_views applies hide_cams after only_cams: never mix them
    D.objects[name]["hide_cams"] = SID
# ---- live dimensions (build_drain.py), kept ----
COL_R, COL_RI = 4 / 12, 3 / 12; COL_TOP = 19.5; GIR_Z0, GIR_Z1 = 20.0, 23.0; CP = 0.5
# ---- KD08 base piece after Downes Pl. VIII Fig. 3 (inner column, first tier) ----
PL_X, PL_Y, PL_T = 1.5, 2.0, 0.25          # base plate 2 ft 0 in x 1 ft 6 in (p.4 Fig.4/5 + Fig.3 plan), outlet along the short side
PL_Z1 = -3.15; PL_Z0 = PL_Z1 - PL_T          # plate top kept at the live datum
D_RO, D_RI = 3.5 / 12, 2.5 / 12              # outlet D: 7 in outside (p.4), ~1 in metal at the column
PZ = PL_Z1 + 0.40                            # outlet centre ~5 in above the plate top (read off Fig. 3)
CONC = (2.0, 3.0, 1.6)                       # concrete "about 2 ft. by 3 ft." (p.4), depth within the printed 1-4 ft; live depth kept
FL_Z = 0.5                                   # A/B bolted flange ~6 in above the floor (Fig. 3 dimension)
GRAVEL_Z = PL_Z0 - CONC[2]                   # concrete rests on the gravel stratum (p.4)
def half_tube(k, a, b, ro, ri, u, w, seg=16, cuti=None, mati=None):
    A = Vector([ft(v) for v in a]); B = Vector([ft(v) for v in b]); u = Vector(u); w = Vector(w)
    bm = k.bm; n0 = len(bm.faces)
    def ring(C, r): return [bm.verts.new(C + (u * math.cos(math.pi * j / seg) + w * math.sin(math.pi * j / seg)) * ft(r)) for j in range(seg + 1)]
    oa, ob_, ia, ib = ring(A, ro), ring(B, ro), ring(A, ri), ring(B, ri)
    for j in range(seg):
        bm.faces.new([oa[j], oa[j + 1], ob_[j + 1], ob_[j]]); bm.faces.new([ia[j], ib[j], ib[j + 1], ia[j + 1]])
        bm.faces.new([oa[j], ia[j], ia[j + 1], oa[j + 1]]); bm.faces.new([ob_[j], ob_[j + 1], ib[j + 1], ib[j]])
    k._t(mati if mati is not None else I("iron"), n0); n1 = len(bm.faces)
    bm.faces.new([oa[0], ob_[0], ib[0], ia[0]]); bm.faces.new([oa[seg], ia[seg], ib[seg], ob_[seg]])
    k._t(cuti if cuti is not None else I("cut"), n1)
ck = K()
ck.box(I("conc"), -CONC[0] / 2, CONC[0] / 2, 0.0, CONC[1] / 2, GRAVEL_Z, PL_Z0)
ck.box(I("cut"), -CONC[0] / 2, CONC[0] / 2, -0.006, 0.03, GRAVEL_Z, PL_Z0)
ck.box(I("iron"), -PL_X / 2, PL_X / 2, 0.0, PL_Y / 2, PL_Z0, PL_Z1); ck.box(I("cut"), -PL_X / 2, PL_X / 2, -0.006, 0.03, PL_Z0, PL_Z1)
# shaft A+B (one hollow tube, bore = downpipe), with the B outlet window cut where D leaves (+x side)
half_tube(ck, (0, 0, PL_Z1), (0, 0, PZ - D_RO), COL_R, COL_RI, (1, 0, 0), (0, 1, 0))
half_tube(ck, (0, 0, PZ + D_RO), (0, 0, COL_TOP), COL_R, COL_RI, (1, 0, 0), (0, 1, 0))
half_tube(ck, (0, 0, PZ - D_RO), (0, 0, PZ + D_RO), COL_R, COL_RI, (-1, 0, 0), (0, 1, 0), seg=8)   # -x half only at the outlet
ck.box(I("iron"), -COL_RI, COL_RI, 0.0, COL_RI, PL_Z1, PL_Z1 + 0.08)                                    # closed foot of B
# flared brackets of B (Fig. 3 elevation / plan e.e): webs to the plate's long edges and corners, concave profile
def web(dirx, diry, reach):
    d = Vector((dirx, diry, 0)).normalized(); n = Vector((-d.y, d.x, 0)) * 0.035
    H = 1.35; pts = []
    for j in range(9):
        t = j / 8; r = COL_R + (reach - COL_R) * t; z = PL_Z1 + H * (1 - t) ** 2.2
        pts.append((r, z))
    bm = ck.bm; n0 = len(bm.faces); base = [Vector((0, 0, 0))]
    L = [bm.verts.new(tuple(ft(v) for v in (d * r - n + Vector((0, 0, z))))) for r, z in pts]
    R_ = [bm.verts.new(tuple(ft(v) for v in (d * r + n + Vector((0, 0, z))))) for r, z in pts]
    L0 = bm.verts.new(tuple(ft(v) for v in (d * pts[-1][0] - n + Vector((0, 0, PL_Z1))))); R0 = bm.verts.new(tuple(ft(v) for v in (d * pts[-1][0] + n + Vector((0, 0, PL_Z1)))))
    Lc = bm.verts.new(tuple(ft(v) for v in (d * COL_R - n + Vector((0, 0, PL_Z1))))); Rc = bm.verts.new(tuple(ft(v) for v in (d * COL_R + n + Vector((0, 0, PL_Z1)))))
    bm.faces.new(L + [L0, Lc][::-1][::-1] if False else [Lc] + L + [L0]); bm.faces.new(list(reversed([Rc] + R_ + [R0])))
    for a, b, c, e in zip(L, L[1:], R_[1:], R_): bm.faces.new([a, b, c, e])
    bm.faces.new([L[-1], L0, R0, R_[-1]]); bm.faces.new([L0, Lc, Rc, R0]); bm.faces.new([Lc, L[0], R_[0], Rc])
    ck._t(I("iron"), n0)
web(0, 1, PL_Y / 2); web(0.75, 1.0, math.hypot(PL_X / 2, PL_Y / 2) * 0.97); web(-0.75, 1.0, math.hypot(PL_X / 2, PL_Y / 2) * 0.97); web(-1, 0, PL_X / 2)
# A/B bolted joint just above the floor (Fig. 3: four lugs, four 1 in bolts)
half_tube(ck, (0, 0, FL_Z - 0.09), (0, 0, FL_Z + 0.09), COL_R + 0.16, COL_R, (1, 0, 0), (0, 1, 0))
for a in (45, 135):
    x, y = math.cos(math.radians(a)) * (COL_R + 0.2), math.sin(math.radians(a)) * (COL_R + 0.2)
    ck.cyl(I("iron"), (x, y, FL_Z - 0.28), (x, y, FL_Z + 0.28), 0.045, 8)
# connecting piece (live geometry, 3 ft 4 1/2 in per p.4 is close to the live 3.5 ft)
ck.box(I("iron"), -CP, CP, CP - 0.08, CP, COL_TOP, GIR_Z1)
for s in (-1, 1):
    ck.box(I("iron"), min(s * CP, s * (CP - 0.08)), max(s * CP, s * (CP - 0.08)), 0.0, CP, COL_TOP, GIR_Z1)
    ck.box(I("cut"), min(s * CP, s * (CP - 0.08)), max(s * CP, s * (CP - 0.08)), -0.006, 0.03, COL_TOP, GIR_Z1)
    ck.box(I("iron"), s * CP, s * (CP + 0.12), -0.0, 0.35, GIR_Z0, GIR_Z1)
ck.box(I("iron"), -CP, CP, 0.0, CP, COL_TOP - 0.1, COL_TOP)
done(ck, "KD7_Column_DownesVIII", part="column"); hide("KD_Column_hollow")
# outlet D + falling pipe to the live brick drain (drain itself rebuilt identically so it can be hidden as one object)
pk = K(); PX1 = 11.3; PZ1 = PZ - 0.40
half_tube(pk, (COL_R - 0.02, 0, PZ), (PX1, 0, PZ1), D_RO, D_RI, (0, 0, 1), (0, 1, 0))
half_tube(pk, (COL_R - 0.02, 0, PZ), (COL_R + 0.10, 0, PZ - 0.004), D_RO + 0.06, D_RO, (0, 0, 1), (0, 1, 0))   # spigot bead at the column
pk.box(I("brick"), 11.3, 13.6, 0.0, 4.0, -4.6, -4.4); pk.box(I("brick"), 11.3, 11.75, 0.0, 4.0, -4.4, -1.6)
pk.box(I("brick"), 13.15, 13.6, 0.0, 4.0, -4.4, -1.6); pk.box(I("brick"), 11.3, 13.6, 0.0, 4.0, -1.6, -1.15)
pk.box(I("cut"), 11.3, 13.6, -0.006, 0.03, -4.6, -4.4); pk.box(I("cut"), 11.3, 11.75, -0.006, 0.03, -4.4, -1.6)
pk.box(I("cut"), 13.15, 13.6, -0.006, 0.03, -4.4, -1.6); pk.box(I("cut"), 11.3, 13.6, -0.006, 0.03, -1.6, -1.15)
done(pk, "KD7_Outlet_pipe_drain", part="drain"); hide("KD_BasePipe_and_drain")
# ---- KD09 main gutter on the 24 ft girder (Downes p.15, Pl. XIII Fig. 5) ----
BZ0 = GIR_Z1; PLK = 1.5 / 12; SIDE_T, SIDE_D = 1.5 / 12, 7.5 / 12; HALF = 4.5 / 12   # plank 1 1/2 x 9 in, sides 1 1/2 x 7 1/2 in
FB_T = 1 / 12; FALL = 3 / 96                                                             # false bottom falls 3 in in 8 ft
def fb_z(x): return BZ0 + PLK + 0.03 + FALL * abs(x)
bx = K()
bx.box(I("wood"), -10, 10, 0.0, HALF, BZ0, BZ0 + PLK); bx.box(I("cut"), -10, 10, -0.006, 0.02, BZ0, BZ0 + PLK)
bx.box(I("wood"), -10, 10, HALF - SIDE_T, HALF, BZ0 + PLK, BZ0 + PLK + SIDE_D)
for s in (-1, 1):   # false bottom, two tilted boards falling to the column, cut at y=0
    x0, x1 = s * 0.45, s * 10.0
    bm = bx.bm; n0 = len(bm.faces)
    v = [bm.verts.new((ft(x), ft(y), ft(fb_z(x) + dz))) for (x, y, dz) in
         [(x0, 0, 0), (x1, 0, 0), (x1, HALF - SIDE_T, 0), (x0, HALF - SIDE_T, 0), (x0, 0, FB_T), (x1, 0, FB_T), (x1, HALF - SIDE_T, FB_T), (x0, HALF - SIDE_T, FB_T)]]
    for f in [(0, 3, 2, 1), (4, 5, 6, 7), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]: bm.faces.new([v[k] for k in f])
    bx._t(I("wood"), n0); n1 = len(bm.faces); bm.faces.new([v[0], v[1], v[5], v[4]]); bx._t(I("cut"), n1)
bx.box(I("iron"), -0.45, 0.45, 0.02, HALF - SIDE_T, BZ0 + PLK, BZ0 + PLK + 0.03)   # cast-iron shoe over the column head (Pl. XIII Figs 9-11)
done(bx, "KD7_MainGutter_DownesXIII", part="box_gutter"); hide("KD_BoxGutter")
def strip(k, i, a, b, w, t=0.025): k.bar(i, a, b, w, t)
wk = K()
for s in (-1, 1): strip(wk, I("water"), (s * 9.8, 0.14, fb_z(9.8) + FB_T + 0.02), (s * 0.5, 0.14, fb_z(0.5) + FB_T + 0.02), 0.22, 0.04)
strip(wk, I("water"), (0, 0.14, BZ0 + PLK + 0.03), (0, 0.18, COL_TOP - 0.1), 0.2, 0.05)
strip(wk, I("water"), (0, COL_RI - 0.03, COL_TOP), (0, COL_RI - 0.03, PZ + 0.05), 0.24, 0.04)
strip(wk, I("water"), (0, 0.06, COL_TOP), (0, 0.06, PZ), 0.05, 0.05)
strip(wk, I("water"), (COL_R - 0.05, 0.12, PZ - D_RI + 0.06), (PX1, 0.12, PZ1 - D_RI + 0.06), 0.24, 0.05)
strip(wk, I("water"), (11.5, 0.15, -4.36), (13.0, 0.15, -4.36), 0.5, 0.05)
strip(wk, I("water"), (12.2, 0.02, -4.36), (12.2, 4.0, -4.36), 0.9, 0.05)
done(wk, "KD7_Water_gutter_column_pipe", part="water")
for n in ("KD_Water_boxgutter", "KD_Water_column", "KD_Water_pipe_drain"): hide(n)
# ---- KD10 ground in section: soil cut on the y=0 plane, loam over the gravel stratum (p.4), cut-outs for the iron ----
SX0, SX1, SY1 = -9.0, 15.5, 7.0; SZ0 = GRAVEL_Z - 1.4
sk = K()
sk.box(I("loamcut"), SX0, SX1, 0.0, SY1, SZ0, 0.0)          # one closed solid (stacked coplanar boxes break the boolean)
for zc in (-0.25, GRAVEL_Z):                                   # split the faces at the turf and gravel lines before the boolean
    geom = sk.bm.verts[:] + sk.bm.edges[:] + sk.bm.faces[:]
    bmesh.ops.bisect_plane(sk.bm, geom=geom, plane_co=(0, 0, ft(zc)), plane_no=(0, 0, 1))
bmesh.ops.recalc_face_normals(sk.bm, faces=sk.bm.faces[:])
soil = done(sk, "KD7_Ground_section", part="ground")
# boolean out the buried iron, concrete, pipe and drain so their cut faces and bores read in front of the soil face
CUTS = [("box", (-CONC[0] / 2 - 0.01, CONC[0] / 2 + 0.01, -0.5, CONC[1] / 2 + 0.01, GRAVEL_Z - 0.01, PL_Z0 + 0.005)),
        ("box", (-PL_X / 2 - 0.01, PL_X / 2 + 0.01, -0.5, PL_Y / 2 + 0.01, PL_Z0 - 0.005, PL_Z1 + 1.4)),   # plate + bracket zone, open like Downes Fig. 3
        ("cyl", ((0, -0.0, PL_Z1 - 0.05), (0, 0, 0.3), COL_R + 0.01)),
        ("cyl", ((COL_R - 0.1, 0, PZ), (PX1 + 0.1, 0, PZ1), D_RO + 0.01)),
        ("box", (11.29, 13.61, -0.5, 4.01, -4.61, -1.14))]
bpy.context.view_layer.objects.active = soil
for kind, a_ in CUTS:   # one closed primitive per boolean (a self-overlapping cutter makes the MANIFOLD solver keep stray shells)
    cut = Kit([MAT["iron"]])
    if kind == "box": cut.box(0, *a_)
    else: cut.cyl(0, a_[0], a_[1], a_[2], 32)
    bmesh.ops.recalc_face_normals(cut.bm, faces=cut.bm.faces[:])
    cutter = cut.done("KD7_tmp_cutter", COLL)
    mod = soil.modifiers.new("cut", "BOOLEAN"); mod.operation = "DIFFERENCE"; mod.solver = "MANIFOLD"; mod.object = cutter
    with bpy.context.temp_override(object=soil, active_object=soil): bpy.ops.object.modifier_apply(modifier="cut")
    D.objects.remove(cutter, do_unlink=True)
print("SOIL_POLYS", len(soil.data.polygons)); assert len(soil.data.polygons) > 20, "boolean emptied the soil"
# materials by position: turf on top, loam / gravel on the section face and sides, dark soil on the cavity walls
F = ft(1)
for p in soil.data.polygons:
    c = p.center / F; n = p.normal
    if n.z > 0.9 and c.z > -0.01: p.material_index = I("grass")
    elif c.z > -0.25: p.material_index = I("grass")
    elif c.z < GRAVEL_Z: p.material_index = I("gravel")
    else: p.material_index = I("loamcut")
    inner = (SX0 + 0.01 < c.x < SX1 - 0.01) and (0.01 < c.y < SY1 - 0.01) and (SZ0 + 0.01 < c.z < -0.01)
    if inner: p.material_index = I("soil")
hide("KD_Ground")
# scale figure: same man, standing on the uncut ground behind the section (he stood on ground that is now cut away)
fig = D.objects["KD_FIG_labourer"]; f2 = fig.copy(); COLL.objects.link(f2); f2.name = "KD7_FIG_labourer"
f2.location = (ft(-6.6), ft(2.6), 0.0); f2["only_cams"] = SID; hide("KD_FIG_labourer")
# ---- KD11 camera: whole path ridge -> gravel and every label inside the portrait frame; view direction unchanged ----
cam = D.objects[SID + "_start"]; f = cam.matrix_world.to_3x3() @ Vector((0, 0, -1)); dist = 150.0
TGT = Vector((ft(2.4), ft(1.5), ft(11.2)))
cam.location = TGT - f * ft(dist); cam.data.ortho_scale = ft(48.0)
bpy.context.view_layer.update()
S_H = 48.0; S_W = S_H * 720 / 1280
mw = cam.matrix_world.to_3x3(); R_ = mw @ Vector((1, 0, 0)); U_ = mw @ Vector((0, 1, 0))
def scr(p_ft): d = Vector([ft(v) for v in p_ft]) - TGT; return (d.dot(R_) / ft(1), d.dot(U_) / ft(1))
def world(sx, sy, depth=dist - 40): return TGT + R_ * ft(sx) + U_ * ft(sy) - f * ft(dist - depth)
# ---- KD12 labels: Downes-printed sizes, laid out in screen space, checked inside the frame ----
for o in D.objects:
    if o.get("only_cams") == SID and (o.name.startswith("KD_Label_") or o.name.startswith("KD_Leader_") or o.name.startswith("KD_Dot_") or o.name.startswith("KD_Title_")):
        o["only_cams"] = "NONE_" + TAG
LBL = G.coll("KD7_LABELS", COLL)
def pax_bot(y): return 23.78 + 0.22 * min(y, 12.0) / 12.0
def ridge_z(y): return pax_bot(y) + 0.5 + 1.6
SZ = 0.74
L, RX = -12.7, 2.2      # left and right label columns (screen ft)
ITEMS = [  # text, anchor (ft, world), label screen position (sx, sy) of the first baseline, side
    ("Glass roof, ridge-and-furrow,\nridges 8 ft apart: rain runs\ndown the glass to the gutters", (6.0, 6.0, ridge_z(6.0) - 0.8), (RX + 1.0, 22.6), "R"),
    ("Connecting piece, 3 ft 4 1/2 in", (-CP, 0.0, 21.0), (L, 6.6), "L"),
    ("Hollow cast-iron column,\n8 in outside: the downpipe", (0.0, 0.2, 12.0), (L, 2.4), "L"),
    ("Bolted joint, 6 in above\nthe ground floor", (-COL_R - 0.2, 0.2, FL_Z), (L, -4.2), "L"),
    ("Cast-iron girder, 3 ft deep", (8.0, 0.0, 21.0), (RX + 1.0, 6.6), "R"),
    ("Main gutter on the girder:\n9 in plank, 7 1/2 in sides;\nfalse bottom falls 3 in in\n8 ft to the column", (6.5, 0.1, BZ0 + PLK + 0.45), (RX + 1.0, 4.6), "R"),
    ("Cast-iron shoe drops the water\ninto the column head", (0.0, 0.2, BZ0 + PLK + 0.03), (RX + 1.0, 0.4), "R"),
    ("Paxton gutter, 5 x 6 in:\nrain channel and two\ncondensation grooves", (4.0, 3.0, pax_bot(3) + 0.3), (5.0, 19.3), "R"),
    ("cut faces in red", (0.0, 0.0, 6.0), (RX + 1.0, -2.6), "R"),
    ("Base piece: 7 in outlet\nat the foot", (COL_R + 0.25, 0.0, PZ), (L, -17.0), "L"),
    ("Base plate 2 ft x 1 ft 6 in", (-PL_X / 2 + 0.1, 0.0, PL_Z0 + 0.12), (L, -19.6), "L"),
    ("Concrete, about 2 x 3 ft,\non the gravel stratum", (-0.6, 0.0, GRAVEL_Z + 0.5), (L, -21.4), "L"),
    ("Pipe falls to the brick drain", (7.0, 0.0, (PZ + PZ1) / 2 - 0.1), (RX - 1.0, -19.6), "R"),
]
TITLE = ("CP014  How rain leaves the roof\nHyde Park, 1851. After Downes 1852,\nPlates VIII, XII and XIII (cutaway)", (L, 22.6))
info = []
def put(name, txt, sx, sy, size, align="LEFT"):
    ob = G.label(LBL, name, txt, 0, 0, 0, size_ft=size, rot=cam.rotation_euler.copy(), m=MAT["ink"], align=align)
    ob.location = world(sx, sy); ob["only_cams"] = SID; return ob
made = []
for n, (txt, A, (sx, sy), side) in enumerate(ITEMS):
    ob = put(f"KD7_Label_{n}", txt, sx, sy, SZ); made.append((ob, A, sx, sy))
tob = put("KD7_Title", TITLE[0], *TITLE[1], SZ * 1.12)
bpy.context.view_layer.update()
def sbox(ob):
    pts = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    ss = [((p - TGT).dot(R_) / ft(1), (p - TGT).dot(U_) / ft(1)) for p in pts]
    return min(s[0] for s in ss), max(s[0] for s in ss), min(s[1] for s in ss), max(s[1] for s in ss)
bad = 0; MARG = 0.5
for ob in [m[0] for m in made] + [tob]:
    x0, x1, y0, y1 = sbox(ob)
    ok = x0 >= -S_W / 2 + MARG and x1 <= S_W / 2 - MARG and y0 >= -S_H / 2 + MARG and y1 <= S_H / 2 - MARG
    bad += not ok; print("LABEL", ob.name, "OK" if ok else "OUT", round(x0, 2), round(x1, 2), round(y0, 2), round(y1, 2), "frame +-", round(S_W / 2, 2), round(S_H / 2, 2))
for ob, A, sx, sy in made:
    x0, x1, y0, y1 = sbox(ob)
    ax, ay = scr(A)
    # leader from the label edge nearest the anchor (first line baseline height) to the anchor dot
    ly = sy + SZ * 0.3
    lx = x1 + 0.25 if ax > x1 else x0 - 0.25
    if x0 <= ax <= x1: lx = ax; ly = y0 - 0.2 if ay < y0 else y1 + 0.2
    P = world(lx, ly, dist - 39.5); Q = world(ax, ay, dist - 39.5)
    lk = Kit([MAT["ink"]]); lk.bar(0, tuple(v / ft(1) for v in P), tuple(v / ft(1) for v in Q), SZ * 0.045)
    lo = lk.done(ob.name.replace("Label", "Leader"), LBL); lo["only_cams"] = SID
    dk = Kit([MAT["ink"]]); Qf = Q / ft(1); dk.cyl(0, tuple(Qf - f / ft(1) * 0.05 * ft(1)), tuple(Qf + f / ft(1) * 0.05 * ft(1)), SZ * 0.14, 12)
    do = dk.done(ob.name.replace("Label", "Dot"), LBL); do["only_cams"] = SID
    print("ANCHOR", ob.name, "screen", round(ax, 2), round(ay, 2), "inside" if abs(ax) < S_W / 2 and abs(ay) < S_H / 2 else "OUTSIDE")
# paper backdrop behind the model, square to the new view (live one is centred on the old target)
D.objects["KD_Backdrop_CP014_drain_whole"]["only_cams"] = "NONE_" + TAG   # retag (it already has only_cams; hide_cams would override it and show it in other shots)
bk = Kit([D.materials["KD_Paper"]]); C = TGT + f * ft(42); Sb = ft(60)
bk.bm.faces.new([bk.bm.verts.new(tuple(C + (a * R_ + b * U_) * Sb)) for a, b in ((-1, -1), (-1, 1), (1, 1), (1, -1))]); bk._t(0, 0)
bo = bk.done("KD7_Backdrop", LBL); bo["only_cams"] = SID
print("LABELS_OUT", bad)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=False)
print("SAVED", OUT)
