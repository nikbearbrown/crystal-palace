"""K-DRAIN (CP014 detail): labelled cutaway of the rain path ridge -> glass -> Paxton gutter -> box gutter -> hollow
cast-iron column -> base-piece outlet -> drain (after Downes 1852, pls XII-XIII). Feet; column axis at x=0,y=0, ground z=0.
The cut plane is y=0: column, connecting piece, box gutter, base pipe and soil are shown as their back half (cut faces red).
blender -b -P scripts/build_drain.py -- --out rounds/k01.blend   (DEPARTURES KD01-)"""
import bpy, sys, os, math, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grokkit as G
from grokkit import ft, Kit
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "/tmp/k01.blend"
R = random.Random(14); sc = G.reset("KD_")
ROOT = G.coll("KDRAIN_K01"); info = {}
M = dict(
    iron=G.mat("Iron", (0.18, 0.20, 0.22), 0.55, 0.25), cut=G.mat("CutFace", (0.62, 0.10, 0.06), 0.6),
    wood=G.mat("Deal", (0.50, 0.40, 0.28), 0.75), sash=G.mat("SashBar", (0.62, 0.58, 0.50), 0.7),
    glass=G.mat_thin_glass("RoofGlass", (0.80, 0.88, 0.88), 0.12),
    water=G.mat("Water", (0.03, 0.22, 0.85), 0.15, 0, ((0.05, 0.35, 1.0), 1.6)),
    cond=G.mat("Condensation", (0.10, 0.70, 0.75), 0.2, 0, ((0.15, 0.85, 0.9), 1.4)),
    arrow=G.mat("Arrow", (0.02, 0.10, 0.55), 0.4, 0, ((0.02, 0.16, 0.7), 0.6)),
    ink=G.mat("Ink", (0.02, 0.02, 0.025), 0.9), soil=G.mat("Soil", (0.30, 0.22, 0.15), 0.95),
    soilcut=G.mat("SoilCut", (0.42, 0.30, 0.19), 0.95), conc=G.mat("Concrete", (0.55, 0.53, 0.49), 0.9),
    brick=G.mat("Brick", (0.45, 0.20, 0.13), 0.9), grass=G.mat("Ground", (0.30, 0.31, 0.20), 0.95),
    paper=G.mat("Paper", (0.92, 0.90, 0.84), 1.0), lead=G.mat("Lead", (0.36, 0.38, 0.40), 0.5, 0.4),
    plank=G.mat("Plank", (0.46, 0.37, 0.26), 0.85))
ML = list(M.values()); IX = {k: i for i, k in enumerate(M)}
def K(): return Kit(ML)
def I(k): return IX[k]
# ---- dimensions (ft) ----
COL_R, COL_RI = 4 / 12, 3 / 12            # 8 in o.d. lower-tier column, ~1 in metal (KD02)
COL_TOP = 19.5; GIR_Z0, GIR_Z1 = 20.0, 23.0  # 3 ft cast girder on the connecting piece
BOX_Z0, BOX_IN = 23.0, 23.12              # box (main) gutter on the girder top
PAX_X = (-4.0, 4.0); RIDGE_X = (-8.0, 0.0, 8.0); RISE = 1.6; PAX_W = 5 / 12; PAX_D = 0.5   # 8 ft ridge-and-furrow (KD03)
Y_END = 13.0                               # roof cut back at 13 ft (half the 24 ft span = gutter mid-camber)
CAMBER = 0.22                              # Paxton gutter camber over 12 ft (falls to the box gutter)
def pax_bot(y): return 23.78 + CAMBER * min(y, 12.0) / 12.0
# ---- half tube (cut at y=0, back half kept) ----
def half_tube(k, a, b, ro, ri, u, w, seg=16, cuti=None):
    A = Vector([ft(v) for v in a]); B = Vector([ft(v) for v in b]); u = Vector(u); w = Vector(w)
    bm = k.bm; n0 = len(bm.faces)
    def ring(C, r): return [bm.verts.new(C + (u * math.cos(math.pi * j / seg) + w * math.sin(math.pi * j / seg)) * ft(r)) for j in range(seg + 1)]
    oa, ob_, ia, ib = ring(A, ro), ring(B, ro), ring(A, ri), ring(B, ri)
    for j in range(seg):
        bm.faces.new([oa[j], oa[j + 1], ob_[j + 1], ob_[j]]); bm.faces.new([ia[j], ib[j], ib[j + 1], ia[j + 1]])
        bm.faces.new([oa[j], ia[j], ia[j + 1], oa[j + 1]]); bm.faces.new([ob_[j], ob_[j + 1], ib[j + 1], ib[j]])
    k._t(I("iron"), n0); n1 = len(bm.faces)
    bm.faces.new([oa[0], ob_[0], ib[0], ia[0]]); bm.faces.new([oa[seg], ia[seg], ib[seg], ob_[seg]])
    k._t(cuti if cuti is not None else I("cut"), n1)
def prism_y(k, i, prof, y0, y1, zf, x0=0.0):
    """extrude an (x,z) profile along y from y0 to y1; zf(y) = base z offset (camber)"""
    bm = k.bm; n0 = len(bm.faces)
    ra = [bm.verts.new((ft(x0 + px), ft(y0), ft(zf(y0) + pz))) for px, pz in prof]
    rb = [bm.verts.new((ft(x0 + px), ft(y1), ft(zf(y1) + pz))) for px, pz in prof]
    n = len(prof)
    for j in range(n): bm.faces.new([ra[j], ra[(j + 1) % n], rb[(j + 1) % n], rb[j]])
    k._t(i, n0); n1 = len(bm.faces); bm.faces.new(list(reversed(ra))); bm.faces.new(rb); k._t(I("cut"), n1)
# ---- ground with an open inspection trench in front of the column foot ----
gk = K(); TX0, TX1, TY0, TY1, TZ = -4.0, 14.0, -5.0, 0.55, -5.0
for (x0, x1, y0, y1) in [(-45, TX0, -45, 45), (TX1, 45, -45, 45), (TX0, TX1, -45, TY0), (TX0, TX1, TY1, 45)]:
    gk.box(I("grass"), x0, x1, y0, y1, -0.4, 0)
gk.box(I("soil"), TX0, TX1, TY1, 8, TZ, -0.4)                  # soil behind the cut, its face is the trench back wall
gk.box(I("soilcut"), TX0, TX1, TY1 - 0.02, TY1, TZ, -0.4)      # section face
gk.box(I("soil"), TX0 - 3, TX0, TY0, TY1, TZ, -0.4); gk.box(I("soil"), TX1, TX1 + 3, TY0, TY1, TZ, -0.4)
gk.box(I("soil"), TX0, TX1, TY0 - 3, TY0, TZ, -0.4); gk.box(I("soil"), TX0 - 3, TX1 + 3, TY0 - 3, 8, TZ - 0.5, TZ)
gk.done("KD_Ground", ROOT)
# ---- footing, base piece, column (cut), connecting piece ----
ck = K()
ck.box(I("conc"), -2.0, 2.0, 0.0, 2.0, -5.0, -3.4); ck.box(I("cut"), -2.0, 2.0, 0.0, 0.03, -5.0, -3.4)   # concrete pad, cut
ck.box(I("iron"), -1.2, 1.2, 0.0, 1.2, -3.4, -3.15); ck.box(I("cut"), -1.2, 1.2, 0.0, 0.03, -3.4, -3.15)  # base plate
half_tube(ck, (0, 0, -3.15), (0, 0, COL_TOP), COL_R, COL_RI, (1, 0, 0), (0, 1, 0))
half_tube(ck, (0, 0, -3.15), (0, 0, -1.4), COL_R + 0.12, COL_R, (1, 0, 0), (0, 1, 0))   # base-piece socket thickening
ck.box(I("iron"), -0.03, 0.03, 0.0, 0.03, -3.15, -2.9)
for s in (-1, 1):   # base flange ribs (back half only)
    ck.box(I("iron"), s * 0.35 - 0.04, s * 0.35 + 0.04, 0.0, 0.9, -3.15, -2.0)
    ck.box(I("iron"), -0.04, 0.04, 0.3, 1.1, -3.15, -2.0) if s > 0 else None
# connecting piece: square hollow block, back half, bolted lugs for the girders
CP = 0.5
ck.box(I("iron"), -CP, CP, CP - 0.08, CP, COL_TOP, GIR_Z1)
for s in (-1, 1):
    ck.box(I("iron"), min(s * CP, s * (CP - 0.08)), max(s * CP, s * (CP - 0.08)), 0.0, CP, COL_TOP, GIR_Z1)
    ck.box(I("cut"), min(s * CP, s * (CP - 0.08)), max(s * CP, s * (CP - 0.08)), 0.0, 0.03, COL_TOP, GIR_Z1)
    ck.box(I("iron"), s * CP, s * (CP + 0.12), -0.0, 0.35, GIR_Z0, GIR_Z1)     # lug
ck.box(I("iron"), -CP, CP, 0.0, CP, COL_TOP - 0.1, COL_TOP)
ck.done("KD_Column_hollow", ROOT, part="column", note="8 in hollow cast-iron column used as the downpipe")
# outlet pipe from the base piece to the drain (half pipe, cut at y=0), brick drain end-on at x 12
pk = K(); PZ = -2.4
half_tube(pk, (COL_R - 0.05, 0, PZ), (11.3, 0, PZ - 0.35), 0.27, 0.22, (0, 0, 1), (0, 1, 0))
pk.box(I("brick"), 11.3, 13.6, 0.0, 4.0, -4.6, -4.4); pk.box(I("brick"), 11.3, 11.75, 0.0, 4.0, -4.4, -1.6)
pk.box(I("brick"), 13.15, 13.6, 0.0, 4.0, -4.4, -1.6); pk.box(I("brick"), 11.3, 13.6, 0.0, 4.0, -1.6, -1.15)
pk.box(I("cut"), 11.3, 13.6, 0.0, 0.03, -4.6, -4.4); pk.box(I("cut"), 11.3, 11.75, 0.0, 0.03, -4.4, -1.6)
pk.box(I("cut"), 13.15, 13.6, 0.0, 0.03, -4.4, -1.6); pk.box(I("cut"), 11.3, 13.6, 0.0, 0.03, -1.6, -1.15)
pk.done("KD_BasePipe_and_drain", ROOT, part="drain")
# ---- girders (3 ft cast girders each side of the connecting piece) ----
gr = K()
for s in (-1, 1):
    x0, x1 = s * (CP + 0.12), s * 12.0
    gr.box(I("iron"), min(x0, x1), max(x0, x1), -0.22, 0.22, GIR_Z1 - 0.18, GIR_Z1)
    gr.box(I("iron"), min(x0, x1), max(x0, x1), -0.22, 0.22, GIR_Z0, GIR_Z0 + 0.18)
    n = 6
    for j in range(n):
        xa = x0 + (x1 - x0) * j / n; xb = x0 + (x1 - x0) * (j + 1) / n
        gr.bar(I("iron"), (xa, 0, GIR_Z0 + 0.15), (xb, 0, GIR_Z1 - 0.15), 0.12, 0.1); gr.bar(I("iron"), (xb, 0, GIR_Z0 + 0.15), (xa, 0, GIR_Z1 - 0.15), 0.12, 0.1)
        gr.box(I("iron"), xa - 0.05, xa + 0.05, -0.08, 0.08, GIR_Z0, GIR_Z1)
gr.done("KD_Girders", ROOT, part="girder")
# ---- box gutter on the girder (timber trough, front half cut away over the column) ----
bx = K(); BW = 0.5
bx.box(I("wood"), -10, 10, 0.0, BW + 0.1, BOX_Z0, BOX_IN)              # bottom (back half)
bx.box(I("wood"), -10, 10, BW, BW + 0.1, BOX_IN, BOX_Z0 + 0.72)          # back wall
bx.box(I("cut"), -10, 10, 0.0, 0.02, BOX_Z0, BOX_IN)
bx.box(I("lead"), -0.45, 0.45, 0.02, BW, BOX_IN, BOX_IN + 0.01)          # lead cesspool/outlet plate over the column
bx.done("KD_BoxGutter", ROOT, part="box_gutter")
# ---- Paxton gutters: rain channel + two condensation grooves, cambered, trussed underneath ----
# MK03b (2026-10-27): adopt Muse paxton-gutter printed profile on next full rebuild.
# Printed (Downes XII Fig.10): depth 6 in, base 5 in, channel top 3 in, cheek ~5.7 in;
# bar notches 10.5 in. Until then candidate k01_gutter appends Muse mesh.
# Half-widths in feet (base half = 2.5 in = 0.2083 ft; cheek half ~2.85 in = 0.2375 ft; depth 0.5 ft):
PROF = [(-0.2375, 0), (0.2375, 0), (0.2375, 0.5), (0.2083, 0.5), (0.2083, 0.25),
        (0.125, 0.25), (0.125, 0.5), (0.0625, 0.5), (0.0625, 0.25),
        (-0.0625, 0.25), (-0.0625, 0.5), (-0.125, 0.5), (-0.125, 0.25),
        (-0.2083, 0.25), (-0.2083, 0.5), (-0.2375, 0.5)]  # Muse/Downes XII Fig.10 half-widths (ft)
pxk = K(); info["paxton_gutters"] = 0
for gx in PAX_X:
    prism_y(pxk, I("wood"), PROF, 0.0, 12.0, pax_bot, gx); prism_y(pxk, I("wood"), PROF, 12.0, Y_END, pax_bot, gx)
    pxk.bar(I("iron"), (gx, 0.6, pax_bot(0.6)), (gx, 8.0, pax_bot(8) - 0.75), 0.05)      # truss rod and strut
    pxk.bar(I("iron"), (gx, 8.0, pax_bot(8) - 0.75), (gx, Y_END, pax_bot(Y_END) - 0.75), 0.05)
    pxk.bar(I("iron"), (gx, 8.0, pax_bot(8)), (gx, 8.0, pax_bot(8) - 0.75), 0.07)
    info["paxton_gutters"] += 1
pxk.done("KD_PaxtonGutters", ROOT, part="paxton_gutter")
# ---- ridges, sash bars, glass ----
rk = K(); gl = K(); info["sash_bars"] = 0; SP = 10 / 12
def ridge_z(y): return pax_bot(y) + PAX_D + RISE
def slope_pts(gx, rx):
    e = gx + (0.21 if rx > gx else -0.21); return e
for rx in RIDGE_X:
    rk.bar(I("wood"), (rx, 0.05, ridge_z(0.05) + 0.05), (rx, Y_END, ridge_z(Y_END) + 0.05), 0.14, 0.28)
for gx in PAX_X:
    for rx in (gx - 4, gx + 4):
        e = slope_pts(gx, rx); y = 0.1
        while y < Y_END - 0.05:
            rk.bar(I("sash"), (e, y, pax_bot(y) + PAX_D), (rx, y, ridge_z(y)), 0.11, 0.13); info["sash_bars"] += 1; y += SP
        gl.quad(0, [(e, 0.1, pax_bot(0.1) + PAX_D + 0.03), (e, Y_END, pax_bot(Y_END) + PAX_D + 0.03), (rx, Y_END, ridge_z(Y_END) + 0.03), (rx, 0.1, ridge_z(0.1) + 0.03)])
rk.done("KD_RidgesSashBars", ROOT, part="sash")
gl.mats = [M["glass"]]; gl.done("KD_Glass", ROOT, part="glass")
# ---- water: rain on glass, Paxton channel, condensation grooves, falls, box gutter, column, pipe, drain ----
def strip(k, i, a, b, w, t=0.025): k.bar(i, a, b, w, t)
wk = K(); path = []
for gx in PAX_X:
    for rx in (gx - 4, gx + 4):
        e = slope_pts(gx, rx)
        for yy in (2.2, 4.7, 7.5, 10.3):     # rain runs down the outer glass to the gutter
            yj = yy + R.uniform(-0.25, 0.25); strip(wk, I("water"), (rx + (e - rx) * 0.12, yj, ridge_z(yj) - RISE * 0.12 + 0.07), (e, yj, pax_bot(yj) + PAX_D + 0.06), 0.09)
    strip(wk, I("water"), (gx, Y_END - 0.02, pax_bot(Y_END) + 0.3), (gx, 0.0, pax_bot(0) + 0.3), 0.14, 0.06)   # main rain channel
    # the fall from the gutter end into the box gutter
    strip(wk, I("water"), (gx, -0.02, pax_bot(0) + 0.3), (gx, 0.18, BOX_IN + 0.03), 0.13, 0.04)
wk.done("KD_Water_roof", ROOT, part="water")
ck2 = K()
for gx in PAX_X:
    for s in (-1, 1):
        ck2.bar(I("cond"), (gx + s * 0.1475, Y_END, pax_bot(Y_END) + 0.43), (gx + s * 0.1475, 0.0, pax_bot(0) + 0.43), 0.035, 0.02)
        rx = gx + s * 4; e = slope_pts(gx, rx)
        for yy in (1.77, 3.43, 6.77, 9.27):   # condensation down the grooves on the underside of the sash bars
            ck2.bar(I("cond"), (rx + (e - rx) * 0.1, yy, ridge_z(yy) - RISE * 0.1 - 0.1), (e, yy, pax_bot(yy) + PAX_D - 0.09), 0.05, 0.03)
ck2.done("KD_Water_condensation", ROOT, part="condensation")
bw = K()
strip(bw, I("water"), (-9.8, 0.25, BOX_IN + 0.03), (9.8, 0.25, BOX_IN + 0.03), 0.42, 0.05)
strip(bw, I("water"), (0, 0.18, BOX_IN), (0, 0.2, COL_TOP - 0.1), 0.2, 0.05)
bw.done("KD_Water_boxgutter", ROOT, part="water")
cw = K()
strip(cw, I("water"), (0, COL_RI - 0.03, COL_TOP), (0, COL_RI - 0.03, PZ + 0.1), 0.24, 0.04)     # film down the bore
strip(cw, I("water"), (0, 0.06, COL_TOP), (0, 0.06, PZ + 0.2), 0.05, 0.05)                     # falling core
cw.done("KD_Water_column", ROOT, part="water")
pw = K()
strip(pw, I("water"), (COL_R - 0.05, 0.12, PZ - 0.16), (11.3, 0.12, PZ - 0.51), 0.24, 0.05)
strip(pw, I("water"), (11.5, 0.15, -4.36), (13.0, 0.15, -4.36), 0.5, 0.05)
strip(pw, I("water"), (12.2, 0.02, -4.36), (12.2, 4.0, -4.36), 0.9, 0.05)
pw.done("KD_Water_pipe_drain", ROOT, part="water")
# the path polyline (for the monotone check and the arrows)
PATH = [(-1.0, 6.0, ridge_z(6) - 0.4), (-3.75, 6.0, pax_bot(6) + PAX_D + 0.08), (-4.0, 6.0, pax_bot(6) + 0.3), (-4.0, 0.0, pax_bot(0) + 0.3),
        (-4.0, 0.18, BOX_IN + 0.05), (0.0, 0.25, BOX_IN + 0.05), (0.0, 0.15, COL_TOP), (0.0, 0.15, PZ), (11.3, 0.12, PZ - 0.35), (12.2, 1.0, -4.3)]
info["path_monotone"] = int(all(b[2] <= a[2] + 1e-6 for a, b in zip(PATH, PATH[1:])))
info["path_drop_ft"] = round(PATH[0][2] - PATH[-1][2], 2)
# ---- arrows ----
ak = K(); info["arrows"] = 0
def arrow(p, d, L=1.2, r=0.13, off=(0, 0, 0)):
    p = Vector(p) + Vector(off); d = Vector(d).normalized(); a = p - d * L / 2; b = p + d * (L / 2 - 0.35)
    ak.cyl(I("arrow"), tuple(a), tuple(b), r * 0.38, 10); ak.cyl(I("arrow"), tuple(b), tuple(p + d * L / 2), r, 12, True, 0.005)
    info["arrows"] += 1
for gx in PAX_X:
    for s in (-1, 1):
        rx = gx + s * 4; e = slope_pts(gx, rx); yy = 8.9
        a = Vector((rx, yy, ridge_z(yy))); b = Vector((e, yy, pax_bot(yy) + PAX_D)); arrow(tuple((a + b) / 2), tuple(b - a), 1.3, off=(0, 0, 0.32))
    arrow((gx, 4.0, pax_bot(4) + 0.95), (0, -1, -0.02), 1.6)
for sx in (-1, 1): arrow((sx * 2.2, 0.25, BOX_IN + 0.85), (-sx, 0, 0), 1.4)
arrow((0, 0.05, 16.5), (0, 0, -1), 2.0, 0.17); arrow((0, 0.05, 8.0), (0, 0, -1), 2.0, 0.17); arrow((0, 0.05, 1.5), (0, 0, -1), 2.0, 0.17)
arrow((5.8, 0.0, PZ + 0.55), (1, 0, -0.03), 1.8, 0.16); arrow((12.4, 0.5, -3.4), (0.3, 0.2, -1), 1.0, 0.14)
ak.done("KD_Arrows", ROOT, part="arrow")
# rain falling onto the roof (short dashes, whole diagram)
rn = K()
for j in range(46):
    x = R.uniform(-8, 8); y = R.uniform(0.5, Y_END - 0.5); z = ridge_z(y) + R.uniform(0.8, 4.0)
    rn.bar(I("water"), (x, y, z), (x - 0.06, y, z - 0.55), 0.035)
rn.done("KD_Water_rainfall", ROOT, part="rain")
# ---- scale figure ----
FIG = G.coll("KD_FIGURES", ROOT); fm = [G.mat("Coat", (0.16, 0.14, 0.12), 0.9), G.mat("Trouser", (0.30, 0.27, 0.22), 0.9), G.mat("Skin", (0.62, 0.45, 0.35), 0.6), G.mat("Hat", (0.08, 0.07, 0.06), 0.8), G.mat("Shirt", (0.75, 0.72, 0.66), 0.8)]
me = G.pm("man", fm, {"hat": "low"}, "lab")
G.person(FIG, "KD_FIG_labourer", me, -5.6, -2.6, 0.0, G.heading(1, 0.6), R); info["figures"] = 1
# glazier's scaffold board for the gutter detail camera (CP014_drain_gutter only)
sk = K(); BX, BY, BZ = -5.0, -7.5, 21.35
sk.box(I("plank"), BX - 1.6, BX + 1.6, BY - 1.6, BY + 1.6, BZ - 0.17, BZ)
for dx in (-1.5, 1.5):
    for dy in (-1.5, 1.5): sk.cyl(I("plank"), (BX + dx, BY + dy, -0.4), (BX + dx, BY + dy, BZ + 3.6), 0.16, 8)
sk.box(I("plank"), BX - 1.6, BX + 1.6, BY + 1.45, BY + 1.6, BZ + 3.0, BZ + 3.25)
ob = sk.done("KD_Scaffold_board", ROOT, part="scaffold"); ob["only_cams"] = "CP014_drain_gutter"
# ---- cameras, labels, backdrop ----
CAMS = G.coll("CAMERAS")
route = G.cameras(os.path.join(HERE, "..", "route", "drain_route.json"), CAMS)
LBL = G.coll("KD_LABELS", ROOT); info["labels"] = 0
def labels_for(cam_id, items, size, title=None):
    cam = bpy.data.objects[cam_id + "_start"]; rot = cam.rotation_euler.copy(); mw = cam.matrix_world.to_3x3()
    right = mw @ Vector((1, 0, 0)); up = mw @ Vector((0, 1, 0)); fwd = mw @ Vector((0, 0, -1))
    for n, (txt, anchor, dx, dy) in enumerate(items):
        A = Vector(anchor); T = A + right * dx + up * dy - fwd * 14     # 30 ft toward the camera so text is never hidden
        ob = G.label(LBL, f"KD_Label_{cam_id}_{n}", txt, *T, size_ft=size, rot=rot, m=M["ink"], align='RIGHT' if dx < 0 else 'LEFT')
        ob["only_cams"] = cam_id; info["labels"] += 1
        tip = T - (right * (0.25 * size) if dx < 0 else -right * (0.25 * size)) + up * (size * 0.3)
        lk = Kit([M["ink"]]); lk.bar(0, tuple(tip), tuple(A - fwd * 0.6), size * 0.05); lo = lk.done(f"KD_Leader_{cam_id}_{n}", LBL); lo["only_cams"] = cam_id
        dk = Kit([M["ink"]]); dk.cyl(0, tuple(A - fwd * 0.7), tuple(A - fwd * 0.6), size * 0.16, 12); do = dk.done(f"KD_Dot_{cam_id}_{n}", LBL); do["only_cams"] = cam_id
    if title:
        T = Vector(title[1]); ob = G.label(LBL, f"KD_Title_{cam_id}", title[0], *T, size_ft=size * 1.15, rot=rot, m=M["ink"]); ob["only_cams"] = cam_id; info["labels"] += 1
    # paper backdrop behind the model, square to the view
    bk = Kit([M["paper"]]); C = Vector(route_target[cam_id]) + fwd * 42; S = 55
    # winding so the normal faces the camera (-fwd)
    bk.quad(0, [tuple(C + (-right - up) * S), tuple(C + (-right + up) * S), tuple(C + (right + up) * S), tuple(C + (right - up) * S)])
    bo = bk.done(f"KD_Backdrop_{cam_id}", LBL); bo["only_cams"] = cam_id
    return right, up, fwd
route_target = {s["id"]: s["start"]["look_ft"] for s in route["shots"]}
W_ITEMS = [
    ("1  Rain runs down the sloping glass", (-6.0, 5.5, ridge_z(5.5) - 0.8), -5.5, 3.0),
    ("2  Ridge-and-furrow: ridges and furrows 8 ft apart", (-8.0, 9.0, ridge_z(9)), -4.0, 6.0),
    ("3  Paxton gutter: rain channel in the middle,\n    condensation grooves either side", (-4.0, 9.0, pax_bot(9) + 0.3), -6.5, 0.6),
    ("4  Sash-bar grooves carry the inside condensation", (4.5, 10.0, ridge_z(10) - 0.6), 4.5, 3.4),
    ("5  Gutter ends spill into the box gutter on the girder", (4.0, 0.15, BOX_IN + 0.3), 6.5, 0.4),
    ("6  Cast-iron girder, 3 ft deep", (7.5, 0.0, 21.5), 4.5, -0.6),
    ("7  Hollow cast-iron column (8 in) is the downpipe", (0.0, 0.2, 12.0), 3.0, 0.0),
    ("8  Base piece: side outlet below ground", (0.4, 0.2, PZ), 2.0, 4.6),
    ("9  Pipe falls to the brick drain", (7.0, 0.1, PZ - 0.25), 3.0, -3.0),
    ("10 Concrete footing", (-1.5, 1.0, -4.5), -3.0, -1.0),
    ("cut faces in red", (-0.5, 0.0, 6.0), -3.0, 0.0)]
r_, u_, f_ = labels_for("CP014_drain_whole", W_ITEMS, 0.85, None)
tt = Vector(route_target["CP014_drain_whole"]) + u_ * 16.6 - r_ * 9.6 - f_ * 30
ob = G.label(LBL, "KD_Title_whole", "K-DRAIN  CP014  How rain leaves the roof\nafter Downes 1852, pls XII-XIII (cutaway, not to a single scale)", *tt, size_ft=0.95, rot=bpy.data.objects["CP014_drain_whole_start"].rotation_euler.copy(), m=M["ink"]); ob["only_cams"] = "CP014_drain_whole"; info["labels"] += 1
R_ITEMS = [
    ("Rain on the outer glass", (-6.0, 7.0, ridge_z(7) - 0.8), -2.0, 2.4),
    ("Ridge", (-8.0, 11.5, ridge_z(11.5) + 0.1), -1.2, 1.4),
    ("Sash bar, grooved underneath", (-6.2, 4.33, (ridge_z(4.3) + pax_bot(4.3) + PAX_D) / 2 - 0.1), -3.4, -1.0),
    ("Condensation grooves", (-4.15, 3.0, pax_bot(3) + 0.43), -3.5, -2.6),
    ("Paxton gutter (rain channel)", (-4.0, 6.0, pax_bot(6) + 0.3), -3.0, -3.8),
    ("Box gutter", (2.0, 0.3, BOX_IN + 0.05), 1.0, -2.6),
    ("Outlet into the column head", (0.0, 0.2, BOX_IN), 3.6, -3.3),
    ("Connecting piece / girder lug", (CP + 0.06, 0.1, 21.0), 3.0, -4.6),
    ("Truss rod under the gutter", (4.0, 7.5, pax_bot(7.5) - 0.65), 2.8, -1.4)]
labels_for("CP014_drain_roof", R_ITEMS, 0.48)
# ---- world, light, render ----
# flat studio world (KD04): the labelled cutaway is a diagram, not a sunlit site view
w = bpy.data.worlds.new("KD_Studio"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.78, 0.76, 0.70, 1); bg.inputs[1].default_value = 1.0
L = bpy.data.lights.new("KD_Key", "AREA"); L.energy = 180; L.size = 8; L.color = (1.0, 0.97, 0.92)
ko = bpy.data.objects.new("KD_Key", L); sc.collection.objects.link(ko); ko.location = (ft(18), ft(-22), ft(28)); ko.rotation_euler = (math.radians(55), 0, math.radians(35))
L2 = bpy.data.lights.new("KD_Fill", "AREA"); L2.energy = 60; L2.size = 10; L2.color = (0.85, 0.90, 1.0)
fo = bpy.data.objects.new("KD_Fill", L2); sc.collection.objects.link(fo); fo.location = (ft(-16), ft(18), ft(22)); fo.rotation_euler = (math.radians(40), 0, math.radians(-140))
G.render_settings(exposure=0.15, look="AgX - Medium High Contrast")
bpy.data.objects["CP014_drain_whole_start"]["exposure"] = 0.3; bpy.data.objects["CP014_drain_roof_start"]["exposure"] = 0.3
G.save(OUT, info, "K-DRAIN k01", 14)
