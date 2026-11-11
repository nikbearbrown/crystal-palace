"""CP014 cams CANDIDATE 2026-11-11 (DEPARTURES KD14-KD17; no verdict, NOT live).
Carries the CP014_drain_whole "Downes plate" KEEP (KD07-KD13, the KD7_* objects) over to CP014_drain_roof / _gutter / _base
so all four CP014 shots show the same parts. Reads the LIVE k01 (rounds/k01.blend, md5 2c1e3235..., never written) and saves
rounds/candidates/k01_cp014cams.blend. Hyde Park 1851 only (Downes 1852, Pl. VIII, XII, XIII; pp. 4, 15-16).
  KD14  KD7_Column_DownesVIII (Pl. VIII Fig. 3 base piece, 2 x 3 ft concrete), KD7_Outlet_pipe_drain (7 in outlet),
        KD7_MainGutter_DownesXIII (p.15 main gutter + shoe) and KD7_Water_gutter_column_pipe now render in all four CP014
        shots; the old KD_Column_hollow / KD_BasePipe_and_drain / KD_BoxGutter / KD_Water_boxgutter / _column / _pipe_drain
        are hidden in all four. KD13 cut-face fix comes with them. CP014_drain_base keeps its trench ground (KD_Ground).
  KD15  CP014_drain_roof labels rebuilt in screen space (the live ones sit ~14 ft above their anchors, off the top of the
        frame: build_drain.labels_for read cam.matrix_world before the depsgraph update, so fwd/up/right were the identity);
        "Box gutter"/"Outlet" relabelled to the p.15 main gutter and the p.16 shoe; small paper tags; all checked in frame.
  KD16  Concrete cut face (whole + base) in a concrete-grey section colour instead of red, so the base plate (iron, red
        cut) no longer merges with the concrete into one red block. Only the concrete faces of KD7_Column_DownesVIII change.
  blender -b rounds/k01.blend -P scripts/cand_cp014_cams_20261111.py -- --out rounds/candidates/k01_cp014cams.blend [--no-kd16]"""
import bpy, sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grokkit as G
from grokkit import ft, Kit
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/k01_cp014cams.blend"
ROOTDIR = os.path.dirname(HERE); OUT = OUT if os.path.isabs(OUT) else os.path.join(ROOTDIR, OUT)
D = bpy.data
assert any(o.name.startswith("KD7_") for o in D.objects), "needs the live k01 with the CP014 plate KEEP (KD7_*)"
assert not any(o.name.startswith("KD14_") for o in D.objects), "candidate already applied"
WHOLE, ROOF, GUT, BASE = "CP014_drain_whole", "CP014_drain_roof", "CP014_drain_gutter", "CP014_drain_base"
ALL4 = ",".join((WHOLE, ROOF, GUT, BASE))
# ---- KD14: shared parts in all four shots ----
for n in ("KD7_Column_DownesVIII", "KD7_Outlet_pipe_drain", "KD7_MainGutter_DownesXIII", "KD7_Water_gutter_column_pipe"):
    o = D.objects[n]; assert o["only_cams"] == WHOLE, n; o["only_cams"] = ALL4
for n in ("KD_Column_hollow", "KD_BasePipe_and_drain", "KD_BoxGutter", "KD_Water_boxgutter", "KD_Water_column", "KD_Water_pipe_drain"):
    o = D.objects[n]; assert o.get("hide_cams") == WHOLE and not o.get("only_cams"), n; o["hide_cams"] = ALL4
# KD14b: in CP014_drain_base the flow arrow over the pipe keeps its live clearance (~0.45 ft) above the new, lower pipe
# (outlet centre 5 in above the plate, KD08): a copy of KD_Arrows with that one arrow lowered by the pipe drop at x 5.8 ft
ar = D.objects["KD_Arrows"]; assert not ar.get("only_cams") and not ar.get("hide_cams")
a2 = ar.copy(); a2.data = ar.data.copy(); a2.name = "KD14_Arrows_base"; a2.data.name = "KD14_Arrows_base"
D.collections["KDRAIN_K01"].objects.link(a2); a2["only_cams"] = BASE; ar["hide_cams"] = BASE
OLD_Z = -2.4 - 0.35 * (5.8 - 0.28) / (11.3 - 0.28); NEW_Z = (-3.15 + 0.40) - 0.40 * (5.8 - 0.31) / (11.3 - 0.31); DZ = NEW_Z - OLD_Z
nv = 0
for v in a2.data.vertices:
    c = (a2.matrix_world @ v.co) / ft(1)
    if 4.6 < c.x < 7.0 and -2.4 < c.z < -1.4 and abs(c.y) < 0.5: v.co.z += ft(DZ); nv += 1
print("KD14_ARROW_VERTS", nv, "dz_ft", round(DZ, 3)); assert nv > 10
# ---- KD16: concrete section colour (concrete cut faces of KD7_Column_DownesVIII only) ----
F = ft(1); GRAVEL_Z, PL_Z0 = -3.4 - 1.6, -3.4
if "--no-kd16" not in argv:
    col = D.objects["KD7_Column_DownesVIII"]; me = col.data
    cc = G.mat("ConcreteCut", (0.47, 0.45, 0.41), 0.95); cc.name = "KD14_ConcreteCut"
    me.materials.append(cc); ci = len(me.materials) - 1; cut_i = list(me.materials).index(D.materials["KD_CutFace"])
    nn = 0
    for p in me.polygons:
        c = p.center / F
        if p.material_index == cut_i and GRAVEL_Z - 0.01 < c.z < PL_Z0 + 0.01 and abs(c.x) <= 1.01 and c.y < 0.04:
            p.material_index = ci; nn += 1
    print("KD16_CONCRETE_FACES", nn); assert nn >= 1
# ---- KD15: roof labels in screen space ----
for o in D.objects:
    if o.get("only_cams") == ROOF and o.name.startswith(("KD_Label_", "KD_Leader_", "KD_Dot_")): o["only_cams"] = "NONE_KD15"
COLL = G.coll("KD14_CP014_CAMS", D.collections["KDRAIN_K01"]); LBL = G.coll("KD14_ROOF_LABELS", COLL)
cam = D.objects[ROOF + "_start"]; bpy.context.view_layer.update()
mw = cam.matrix_world.to_3x3(); R_ = mw @ Vector((1, 0, 0)); U_ = mw @ Vector((0, 1, 0)); f = mw @ Vector((0, 0, -1))
dist = 150.0; TGT = cam.matrix_world.translation + f * ft(dist)
S_W = cam.data.ortho_scale / ft(1); S_H = S_W * 720 / 1280
def scr(p): d = Vector([ft(v) for v in p]) - TGT; return d.dot(R_) / ft(1), d.dot(U_) / ft(1)
def world(sx, sy, toward=30.0): return TGT + R_ * ft(sx) + U_ * ft(sy) - f * ft(toward)
def pax_bot(y): return 23.78 + 0.22 * min(y, 12.0) / 12.0
def ridge_z(y): return pax_bot(y) + 0.5 + 1.6
BZ0, PLK = 23.0, 1.5 / 12
def fb_top(x): return BZ0 + PLK + 0.03 + 3 / 96 * abs(x) + 1 / 12
SZ = 0.30; LX, RX = -8.35, 1.2
ITEMS = [  # text, world anchor (ft), label first-baseline screen pos (ft)
    ("Rain runs down the outer glass", (-6.0, 7.0, ridge_z(7) - 0.8), (LX, 4.25)),
    ("Ridge: ridges and furrows 8 ft apart", (8.0, 5.0, ridge_z(5.0) + 0.05), (RX - 3.2, 4.25)),
    ("Sash bar, grooved underneath", (-6.2, 4.33, (ridge_z(4.3) + pax_bot(4.3) + 0.5) / 2 - 0.1), (LX, -1.15)),
    ("Paxton gutter, 5 x 6 in: rain channel\nand two condensation grooves", (-4.0, 6.0, pax_bot(6) + 0.3), (LX, -1.85)),
    ("Truss rod under the Paxton gutter", (4.0, 7.5, pax_bot(7.5) - 0.65), (RX + 2.4, 2.35)),
    ("Main gutter on the girder: 9 in plank,\n7 1/2 in sides; false bottom falls\n3 in in 8 ft to the column", (2.6, 0.12, fb_top(2.6)), (RX + 2.4, -2.15)),
    ("Cast-iron shoe drops the water\ninto the column head", (0.0, 0.2, BZ0 + PLK + 0.03), (LX, -3.15)),
    ("Connecting piece / girder lug", (0.56, 0.1, 21.0), (RX + 1.3, -4.45)),
]
PAPER = D.materials["KD_Paper"]; INK = D.materials["KD_Ink"]
def sbox(ob):
    pts = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    ss = [((p - TGT).dot(R_) / ft(1), (p - TGT).dot(U_) / ft(1)) for p in pts]
    return min(s[0] for s in ss), max(s[0] for s in ss), min(s[1] for s in ss), max(s[1] for s in ss)
made = []
for n, (txt, A, (sx, sy)) in enumerate(ITEMS):
    ob = G.label(LBL, f"KD14_RoofLabel_{n}", txt, 0, 0, 0, size_ft=SZ, rot=cam.rotation_euler.copy(), m=INK)
    ob.location = world(sx, sy); ob["only_cams"] = ROOF; made.append((ob, A))
bpy.context.view_layer.update()
bad = 0; MARG = 0.25
for ob, A in made:
    x0, x1, y0, y1 = sbox(ob); ax, ay = scr(A)
    ok = x0 >= -S_W / 2 + MARG and x1 <= S_W / 2 - MARG and y0 >= -S_H / 2 + MARG and y1 <= S_H / 2 - MARG
    ain = abs(ax) < S_W / 2 - 0.1 and abs(ay) < S_H / 2 - 0.1
    bad += (not ok) + (not ain)
    print("LABEL", ob.name, "OK" if ok else "OUT", [round(v, 2) for v in (x0, x1, y0, y1)], "anchor", round(ax, 2), round(ay, 2), "in" if ain else "OUTSIDE")
    # paper tag behind the text
    pd = 0.08; tk = Kit([PAPER]); c = [world(x, y, 29.9) / ft(1) for x, y in ((x0 - pd, y0 - pd), (x1 + pd, y0 - pd), (x1 + pd, y1 + pd), (x0 - pd, y1 + pd))]
    tk.quad(0, [tuple(v) for v in c]); to = tk.done(ob.name.replace("Label", "Tag"), LBL); to["only_cams"] = ROOF
    # leader from the nearest tag edge to the anchor; dot at the anchor
    ly = min(max(ay, y0), y1); lx = x1 + pd if ax > x1 else (x0 - pd if ax < x0 else ax)
    if x0 <= ax <= x1: ly = y0 - pd if ay < y0 else y1 + pd
    P = world(lx, ly, 29.8) / ft(1); Q = world(ax, ay, 29.8) / ft(1)
    lk = Kit([INK]); lk.bar(0, tuple(P), tuple(Q), SZ * 0.06); lo = lk.done(ob.name.replace("Label", "Leader"), LBL); lo["only_cams"] = ROOF
    fq = f / ft(1) * ft(1); dk = Kit([INK]); dk.cyl(0, tuple(Q - f * 0.05), tuple(Q + f * 0.05), SZ * 0.16, 12)
    do = dk.done(ob.name.replace("Label", "Dot"), LBL); do["only_cams"] = ROOF
print("LABELS_OUT", bad)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=False)
print("SAVED", OUT)
