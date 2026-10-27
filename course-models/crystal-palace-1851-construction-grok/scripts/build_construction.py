"""Hyde Park 1851 Crystal Palace: HP-BUILD construction states for storyboard CP010-CP016 (Grok Bot).

One site, one scene: the east half of the building read as a construction front moving east (summer-late 1850):
  zone C  x  36..420  frame complete; tier-1 south roof glazed / being glazed (wagons) / sash bars only / gutters only;
                      canvas-shaded bays and a louvre wall bay (CP015, 1851 system insert); floor boards and bare joists
  zone B  x 444..636  erection: full columns to x 492, first-lift columns beyond, scaffolding, sheer legs lifting
                      a 24 ft girder into bay 540-564 (CP012)
  zone A  x 660..900  foundations (CP010): backfilled bases with first columns, base pieces set, pads poured, pits
                      dug, pegged positions (Downes Plate VIII base plates D16; Plate VI concrete pads D17)
  OFFSITE x ~3000     illustrative workshop yard (CP011) and the hollow-column drainage cutaway (CP014), well away
                      from the building so they are never mistaken for the Hyde Park site
Claude's frame: metres, origin at the crossing, X east, Y north, line i at x = -924 + 24 i, ft = 0.3048.
The material / column / girder prelude is executed from ../crystal-palace-1851-exterior-grok/scripts/build_exterior.py
(same parametric parts as the transept and exterior). Hyde Park only, never Sydenham.

Run:  blender -b -P scripts/build_construction.py -- --out rounds/cNN.blend
"""
import bpy, bmesh, math, random, sys, os, json
from mathutils import Vector, Matrix
HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "..", "crystal-palace-1851-exterior-grok", "scripts", "build_exterior.py")
SRC = open(EXT).read()
_pre = SRC[:SRC.index("\n# =====")]
exec(compile(_pre, EXT + "[prelude]", "exec"), globals())
_w0 = SRC.index("# ---------------- world, sun, render settings"); _w1 = SRC.index("\n# ---------------- ", _w0 + 10)
exec(compile(SRC[_w0:_w1], EXT + "[world]", "exec"), globals())
OUT = os.path.abspath(arg("--out", "/tmp/construction.blend"))
for c in list(C.values()): bpy.data.collections.remove(c)
ROOT.name = "CONSTRUCTION_GROK"
K = {n: coll(n, ROOT) for n in ["FRAME", "ROOF_STATES", "FOUNDATIONS", "GROUND", "SCAFFOLD", "LIFTING", "WAGONS",
                                "WORKERS", "FLOOR", "LOUVRE_CANVAS", "OFFSITE_YARD", "DETAIL_DRAINAGE"]}
rnd = random.Random(1850)
scene.view_settings.exposure = -2.4      # bare frame + earth reflect far more than the finished interior (CN13; c02 -1.9 -> -2.4)
# 1850 site ironwork: delivered in a dark oxide priming coat; Owen Jones' colours were applied winter 1850-51 (CN12)
PRIMER = mat_principled("GT_IronPrimer_1850", (0.11, 0.085, 0.07), 0.6)   # c02: darker (CN12)
for _me in bpy.data.meshes:
    for _i, _m in enumerate(_me.materials):
        if _m and _m.name.startswith("GT_Iron"): _me.materials[_i] = PRIMER
IRON = PRIMER
for _m, _c in ((WOOD, (0.40, 0.33, 0.24)), (WOODDARK, (0.32, 0.26, 0.19))):
    _m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*_c, 1); _m.diffuse_color = (*_c, 1)
try: scene.view_settings.look = 'AgX - Medium High Contrast'
except TypeError: pass

# ---------------- materials ----------------
EARTH = mat_principled("GT_Earth", (0.17, 0.13, 0.09), 0.95)
SPOIL = mat_principled("GT_Spoil", (0.22, 0.17, 0.12), 0.95)
CONCRETE = mat_principled("GT_Concrete", (0.40, 0.39, 0.36), 0.9)
CASTIRON = mat_principled("GT_CastIronBase", (0.20, 0.20, 0.21), 0.6, 0.4)
POLE = mat_principled("GT_ScaffoldPole", (0.32, 0.27, 0.20), 0.85)
PLANK = mat_principled("GT_ScaffoldPlank", (0.40, 0.34, 0.26), 0.85)
ROPE = mat_principled("GT_Rope", (0.45, 0.40, 0.30), 0.9)
COAT = mat_principled("GT_WorkerCoat", (0.07, 0.07, 0.08), 0.8)
TROUS = mat_principled("GT_WorkerTrousers", (0.20, 0.17, 0.13), 0.85)
SKIN = mat_principled("GT_WorkerSkin", (0.62, 0.46, 0.36), 0.6)
SHIRT = mat_principled("GT_WorkerShirt", (0.78, 0.76, 0.70), 0.8)
ROOFG = mat_glass("GT_RoofGlassBuild", tint=(0.58, 0.64, 0.64), bars=False, milk=0.025, milk_rgb=(0.55, 0.58, 0.58))
LABEL = mat_principled("GT_Label", (0.02, 0.02, 0.02), 0.9)
WAGONT = mat_principled("GT_WagonTimber", (0.22, 0.17, 0.12), 0.85)   # weathered wagon timber (c02)
def canvas_mat():
    m = bpy.data.materials.new("GT_Canvas"); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    for x in list(n): n.remove(x)
    o = n.new("ShaderNodeOutputMaterial"); d = n.new("ShaderNodeBsdfDiffuse"); d.inputs[0].default_value = (0.86, 0.83, 0.75, 1)
    t = n.new("ShaderNodeBsdfTranslucent"); t.inputs[0].default_value = (0.95, 0.88, 0.72, 1)
    mx = n.new("ShaderNodeMixShader"); mx.inputs[0].default_value = 0.45
    l.new(d.outputs[0], mx.inputs[1]); l.new(t.outputs[0], mx.inputs[2]); l.new(mx.outputs[0], o.inputs[0])
    m.diffuse_color = (0.86, 0.83, 0.75, 1); return m
CANVAS = canvas_mat()
def water_mat():
    m = mat_principled("GT_Water", (0.10, 0.35, 0.70), 0.05)
    b = m.node_tree.nodes["Principled BSDF"]
    try:
        b.inputs["Emission Color"].default_value = (0.15, 0.45, 0.9, 1); b.inputs["Emission Strength"].default_value = 0.6
    except KeyError: pass
    return m
WATER = water_mat()

def faces_since(bm, n0, idx):
    bm.faces.ensure_lookup_table()
    for f in bm.faces[n0:]: f.material_index = idx
def cyl_axis(bm, a, b, r, seg=10):
    """cylinder between points a, b (metres)."""
    a = Vector(a); b = Vector(b); d = b - a; L = d.length
    q = d.to_track_quat('Z', 'Y')
    M = Matrix.Translation((a + b) / 2) @ q.to_matrix().to_4x4()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=L, matrix=M)
def sphere(bm, c, r, sub=2):
    bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r, matrix=Matrix.Translation(c))

# ---------------- site plan ----------------
ROWS = [y for y in (-204.0 + 24 * j for j in range(18)) if abs(y) >= 36]
def tier_of(y): ay = abs(y); return 3 if ay <= 60 else (2 if ay <= 132 else 1)
LINES = [36.0 + 24 * k for k in range(37)]          # 36 .. 900
def zone(x):
    if x <= 420: return "C"
    if x <= 636: return "B"
    return "A"
FOUND_STATE = {900: "pegged", 876: "pegged", 852: "dug", 828: "dug", 804: "poured", 780: "poured",
               756: "base", 732: "base", 708: "backfilled", 684: "backfilled", 660: "backfilled"}

# D17 pads (Plate VI section, loose): deeper and wider under the inner columns that carry more.
PAD = {1: dict(w=1.6, t=1.25, top=1.2), 2: dict(w=2.6, t=2.3, top=1.6), 3: dict(w=3.6, t=3.0, top=2.1)}
# D16 base plates (Plate VIII printed): 2'0"x1'0" outer ground-floor column ... 3'0"x2'0"; assignment by load inferred (CN03)
def base_plate(x, y):
    t = tier_of(y)
    if abs(y) == 204: return (2.0, 1.0)
    return {1: (2.0, 1.5), 2: (3.0, 1.5), 3: (3.0, 2.0)}[t]
SOCKET_ABOVE_FLOOR = 3.75 / 12          # Plate VIII Fig. 1 / D14: base piece B stands 3 3/4 in above the floor line

# ---------------- frame (zones C and B; first lifts in zone A) ----------------
cols = {}
def put_col(x, y, top_tier, state):
    key = {1: "col1", 2: "col2", 3: "col3"}[top_tier]
    place(key, f"KCOL_X{x:+05.0f}_Y{y:+04.0f}", K["FRAME"], x, y, 0, part_kind="column", tier=top_tier, state=state)
    cols[(x, y)] = top_tier
for x in LINES:
    for y in ROWS:
        z = zone(x); t = tier_of(y)
        if z == "C" or (z == "B" and x <= 492): put_col(x, y, t, "complete")
        elif z == "B": put_col(x, y, 1, "first_lift")
        elif FOUND_STATE.get(int(x)) == "backfilled": put_col(x, y, 1, "first_lift")
def girder_tiers(xa, xb):
    """girder tiers allowed in the bay between lines xa < xb."""
    if xb <= 492: return 3
    if xb <= 540: return 1
    return 0
ngir = 0
for (x, y), t in list(cols.items()):
    for dx, dy, al in ((24, 0, "X"), (0, 24, "Y")):
        b = (x + dx, y + dy)
        if b not in cols: continue
        if al == "Y" and abs(y + 12) < 36: continue          # nave is spanned by trusses, not 24 ft girders
        n = min(t, cols[b], girder_tiers(min(x, b[0]), max(x, b[0])))
        for k in range(n):
            place("g24", f"KGIR_T{k+1}_{al}_{x + dx/2:+.0f}_{y + dy/2:+.0f}", K["FRAME"], x + dx / 2, y + dy / 2, GIRDER_TOP[k],
                  math.pi / 2 if al == "Y" else 0.0, part_kind="girder", tier=k + 1, state="fixed"); ngir += 1
for x in LINES:
    if x <= 420: place("t72g", f"KTRUSS72_X{x:+05.0f}", K["FRAME"], x, 0, GIRDER_TOP[2], math.pi / 2, part_kind="truss")

# ---------------- ridge-and-furrow roof states (24 x 8 ft Paxton units; panes 49 x 10 in -> bars at ~10 in) ----------------
RISE = 1.6; NBARS = 27            # CN23 (c03): 27 bars / 28 panes per slope per 24 ft (Plate XII; agrees with Muse hp-roof-furrow-bay)
STRONG_FT = (4.0, 12.0, 20.0)     # three 2 1/2 in strong bars in every 24 ft (Downes text; Plate XII Fig. 3)
def mesh_roof(kind):
    bm = bmesh.new(); L = ft(24); W = ft(8); rise = ft(RISE); off = inch(1.3)
    if kind in ("glazed", "canvas", "half"):
        x1 = L / 2 if kind != "half" else -L / 2 + ft(6)
        v = [bm.verts.new(p) for p in [(-L/2, -W/2, off), (x1, -W/2, off), (x1, 0, rise + off), (-L/2, 0, rise + off), (-L/2, W/2, off), (x1, W/2, off)]]
        bm.faces.new([v[0], v[1], v[2], v[3]]); bm.faces.new([v[3], v[2], v[5], v[4]])
    n0 = len(bm.faces)
    bm_box(bm, -L/2, L/2, -W/2 - inch(3), -W/2 + inch(3), -inch(5), inch(1))          # Paxton gutter (timber)
    if kind != "gutter":
        bm_box(bm, -L/2, L/2, -inch(1), inch(1), rise - inch(1.5), rise + inch(1.5))  # ridge
        for s in (-1, 1):
            xs = [-L/2 + (k + 1) * L / (NBARS + 1) for k in range(NBARS)]
            strong = {min(range(NBARS), key=lambda k: abs(xs[k] - (ft(sf) - L/2))) for sf in STRONG_FT}
            for k, x in enumerate(xs):
                bm_bar(bm, (x, s * (W/2 - inch(2)), inch(0.5)), (x, 0, rise), inch(2.5) if k in strong else inch(1.5), inch(2.5))
    faces_since(bm, n0, 1)
    if kind == "canvas":            # canvas laid over the outside of the ridges (Downes p. 24; CN09)
        n1 = len(bm.faces); co = inch(5)
        pts = [(-W/2, co), (-W/4, rise / 2 + co * 1.2), (0, rise + co), (W/4, rise / 2 + co * 1.2), (W/2, co)]
        vs = [[bm.verts.new((sx * L / 2, yy, zz)) for (yy, zz) in pts] for sx in (-1, 1)]
        for i in range(4): bm.faces.new([vs[0][i], vs[1][i], vs[1][i + 1], vs[0][i + 1]])
        faces_since(bm, n1, 2)
    me = finish(bm, f"roof_{kind}", ROOFG, [WOOD, CANVAS])
    return me
for kind in ("glazed", "bars", "gutter", "half", "canvas"): LIBM["roof_" + kind] = mesh_roof(kind)
WAGON_RIDGES = [-192.0, -176.0, -160.0, -144.0]
WAGON_X = 330.0
def roof_kind_t1_south(xb, yc):
    if 228 <= xb < 300: return "canvas"
    if xb < 324: return "glazed"
    if xb == 324: return "half" if yc in WAGON_RIDGES else "glazed"
    if xb < 396: return "bars"
    return "gutter"
def roof_kind_other(xb, tier):
    lim = {3: (300, 372), 2: (228, 348), 1: (324, 396)}[tier]
    return "glazed" if xb < lim[0] else ("bars" if xb < lim[1] else "gutter")
nroof = 0; roof_states = {}
for xb in range(36, 420, 24):
    for tier, bands in ((3, [(-60, 60)]), (2, [(-132, -60), (60, 132)]), (1, [(-204, -132), (132, 204)])):
        for (y0, y1) in bands:
            for k in range(int((y1 - y0) / 8)):
                yc = y0 + 4 + 8 * k
                kind = roof_kind_t1_south(xb, yc) if (tier == 1 and y1 < 0) else roof_kind_other(xb, tier)
                place("roof_" + kind, f"KROOF{tier}_{kind}_{xb + 12:+d}_{yc:+.0f}", K["ROOF_STATES"], xb + 12, yc,
                      GIRDER_TOP[tier - 1], part_kind="roof", tier=tier, state=kind); nroof += 1
                roof_states[kind] = roof_states.get(kind, 0) + 1

# ---------------- workers (simple stand-ins, 5 ft 8 in) ----------------
def mesh_worker(pose):
    bm = bmesh.new(); h = 0.0 if pose != "kneel" else 1.4
    legs_top = 2.8 if pose != "kneel" else 1.4
    n0 = len(bm.faces)
    for sx in (-0.3, 0.3): bm_cyl(bm, ft(0.27), 0, ft(legs_top), 8, cx=ft(sx))
    if pose == "kneel":
        for sx in (-0.3, 0.3): bm_bar(bm, (ft(sx), 0, ft(0.25)), (ft(sx), ft(-1.4), ft(0.25)), ft(0.45), ft(0.45))
    faces_since(bm, n0, 1); n0 = len(bm.faces)
    t0 = legs_top; t1 = t0 + 1.95
    bm_cyl(bm, ft(0.55), ft(t0), ft(t1), 10)
    sh = t1 - 0.15
    if pose in ("stand", "kneel"):
        arms = [((-0.75, 0, sh), (-0.8, 0.1, sh - 1.7)), ((0.75, 0, sh), (0.8, 0.1, sh - 1.7))]
    elif pose == "reach":
        arms = [((-0.7, 0, sh), (-0.55, 0.35, sh + 2.0)), ((0.7, 0, sh), (0.55, 0.35, sh + 2.0))]
    else:   # haul / work forward
        arms = [((-0.7, 0, sh), (-0.35, 1.7, sh - 0.6)), ((0.7, 0, sh), (0.35, 1.7, sh - 0.6))]
    for a, b in arms: bm_bar(bm, [ft(v) for v in a], [ft(v) for v in b], ft(0.32), ft(0.32))
    faces_since(bm, n0, 0); n0 = len(bm.faces)
    sphere(bm, (0, 0, ft(t1 + 0.42)), ft(0.36)); faces_since(bm, n0, 2); n0 = len(bm.faces)
    bm_cyl(bm, ft(0.38), ft(t1 + 0.65), ft(t1 + 0.92), 10); faces_since(bm, n0, 0)
    return finish(bm, f"worker_{pose}", COAT, [TROUS, SKIN])
WM = {p: mesh_worker(p) for p in ("stand", "reach", "work", "kneel")}
workers = []
def worker(x, y, z, pose, face_deg, scene_tag):
    ob = new_obj(f"KWORKER_{len(workers):03d}_{scene_tag}", WM[pose], K["WORKERS"], (ft(x), ft(y), ft(z)), math.radians(face_deg),
                 {"part_kind": "worker", "pose": pose, "height_ft": 5.67, "shot": scene_tag})
    workers.append(ob); return ob

# ---------------- ground ----------------
AX0, AX1, AY0, AY1 = 644.0, 916.0, -220.0, 220.0
def slab_xyz(name, x0, x1, y0, y1, z0, z1, mat, coll_, **props):
    bm = bmesh.new(); bm_box(bm, ft(x0), ft(x1), ft(y0), ft(y1), ft(z0), ft(z1))
    return new_obj(name, finish(bm, name, mat), coll_, props=props)
bm = bmesh.new()       # park grass with the site (x 0..1000, y -300..300) left open for the earth and the pits
for (x0, x1, y0, y1) in ((-9000, 0, -9000, 9000), (1000, 9000, -9000, 9000), (0, 1000, -9000, -300), (0, 1000, 300, 9000)):
    bm_box(bm, ft(x0), ft(x1), ft(y0), ft(y1), ft(-1.0), ft(-0.06))
new_obj("KGROUND_PARK", finish(bm, "park", GRASS), K["GROUND"], props={"part_kind": "ground"})
for nm, (x0, x1, y0, y1) in {"W": (0, AX0, -300, 300), "E": (AX1, 1000, -300, 300), "S": (AX0, AX1, -300, AY0), "N": (AX0, AX1, AY1, 300)}.items():
    slab_xyz(f"KGROUND_SITE_{nm}", x0, x1, y0, y1, -0.6, -0.02, EARTH, K["GROUND"], part_kind="ground")
pits = {}
for x, st in FOUND_STATE.items():
    if st in ("dug", "poured", "base"):
        for y in ROWS:
            p = PAD[tier_of(y)]; pits[(float(x), y)] = (st, p["top"] + p["t"])
bm = bmesh.new(); nx, ny = int((AX1 - AX0) / 4), int((AY1 - AY0) / 4)
def in_pit(cx, cy):
    for (px, py) in pits:
        if abs(cx - px) < 4 and abs(cy - py) < 4: return True
    return False
for i in range(nx):
    for j in range(ny):
        x0, y0 = AX0 + 4 * i, AY0 + 4 * j
        if in_pit(x0 + 2, y0 + 2): continue
        vs = [bm.verts.new((ft(a), ft(b), ft(-0.02))) for a, b in ((x0, y0), (x0 + 4, y0), (x0 + 4, y0 + 4), (x0, y0 + 4))]
        bm.faces.new(vs)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
for (px, py), (st, d) in pits.items():         # pit walls and floor (8 x 8 ft working pit, CN05)
    c = [(px - 4, py - 4), (px + 4, py - 4), (px + 4, py + 4), (px - 4, py + 4)]
    for k in range(4):
        (xa, ya), (xb, yb) = c[k], c[(k + 1) % 4]
        bm.faces.new([bm.verts.new((ft(xa), ft(ya), ft(-0.02))), bm.verts.new((ft(xa), ft(ya), ft(-d))),
                      bm.verts.new((ft(xb), ft(yb), ft(-d))), bm.verts.new((ft(xb), ft(yb), ft(-0.02)))])
    bm.faces.new([bm.verts.new((ft(a), ft(b), ft(-d))) for a, b in reversed(c)])
new_obj("KGROUND_FOUNDATIONS", finish(bm, "ground_foundations", EARTH), K["GROUND"], props={"part_kind": "ground"})

# ---------------- foundations: pads, base plates, base pieces, pegs (CP010) ----------------
def mesh_base_piece(pl, top_ft, name):
    """base plate (pl = L x W ft) + flared foot + 8 in pipe + socket, from the pad top (z=0) to top_ft."""
    bm = bmesh.new(); L, W = pl; r = inch(4)
    bm_box(bm, ft(-L/2), ft(L/2), ft(-W/2), ft(W/2), 0, inch(1.5))
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=ft(min(W, L) / 2 * 0.9), radius2=r * 1.15, depth=ft(0.9),
                          matrix=Matrix.Translation((0, 0, inch(1.5) + ft(0.45))))
    bm_cyl(bm, r, inch(1.5), ft(top_ft) - inch(4), 16)
    bm_cyl(bm, inch(6), ft(top_ft) - inch(4), ft(top_ft), 16)
    return finish(bm, name, CASTIRON)
BASEM = {}
found = []
for x, st in FOUND_STATE.items():
    x = float(x)
    for y in ROWS:
        t = tier_of(y); p = PAD[t]; pl = base_plate(x, y)
        padL, padW = pl[0] + 0.6, max(p["w"], pl[1] + 0.6)
        rec = dict(x=x, y=y, tier=t, state=st, pad_t=p["t"], pad_top=p["top"], pad_L=padL, pad_W=padW, plate=pl)
        if st == "pegged":
            slab_xyz(f"KPEG_{x:+.0f}_{y:+.0f}", x - 0.08, x + 0.08, y - 0.08, y + 0.08, -0.02, 1.4, WOOD, K["FOUNDATIONS"], part_kind="peg")
        if st in ("poured", "base"):
            ob = slab_xyz(f"KPAD_{x:+.0f}_{y:+.0f}", x - padL / 2, x + padL / 2, y - padW / 2, y + padW / 2,
                          -(p["top"] + p["t"]), -p["top"], CONCRETE, K["FOUNDATIONS"], part_kind="pad", **{k: v for k, v in rec.items() if k not in ("plate",)})
            ob["plate_L"], ob["plate_W"] = pl
        if st == "base":
            key = (pl, t)
            if key not in BASEM: BASEM[key] = mesh_base_piece(pl, p["top"] + SOCKET_ABOVE_FLOOR, f"base_piece_{pl[0]}x{pl[1]}_t{t}")
            ob = new_obj(f"KBASE_{x:+.0f}_{y:+.0f}", BASEM[key], K["FOUNDATIONS"], (ft(x), ft(y), ft(-p["top"])), 0,
                         {"part_kind": "base_piece", "plate_L": pl[0], "plate_W": pl[1], "tier": t, "socket_top_ft": SOCKET_ABOVE_FLOOR})
        found.append(rec)
# string lines along the rows in the pegged zone
bm = bmesh.new()
for y in ROWS: bm_bar(bm, (ft(866), ft(y), ft(1.2)), (ft(910), ft(y), ft(1.2)), inch(0.4), inch(0.4))
for x in (876, 900): bm_bar(bm, (ft(x), ft(-210), ft(1.2)), (ft(x), ft(210), ft(1.2)), inch(0.4), inch(0.4))
new_obj("KSTRINGLINES", finish(bm, "stringlines", ROPE), K["FOUNDATIONS"], props={"part_kind": "string_line"})

# ---------------- c04: spoil heaps sized to the pits (CN27) ----------------
# Every excavated pit not yet backfilled (dug / poured / base) keeps its spoil beside it: pit 8 x 8 ft x depth, bulked x1.25.
# Heap = cone frustum, base radius <= 7.5 ft (fits the 16 ft clear square between four pits), side slope 34 deg (loose earth).
# What will not fit is taken off by tip cart (one cart is loading at the 828 line); the carted share is recorded per heap.
_route0 = json.load(open(os.path.join(HERE, "..", "route", "camera_route.json")))
_campts = []
for _s in _route0["shots"]:
    _p = [_s[k]["pos_ft"] for k in ("start", "end") if k in _s]
    _campts.append((_p[0][:2], _p[-1][:2]))
def _segd(p, a, b):
    ax, ay = a; bx, by = b; dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)
CART_KEEP = [(814, 832, -196, -188)]          # the spoil cart's stand (below), kept clear of heaps
def _rect_hit(x, y, r):
    return any(x0 - r < x < x1 + r and y0 - r < y < y1 + r for (x0, x1, y0, y1) in CART_KEEP)
TAN = math.tan(math.radians(34)); RB = 7.5
def frustum_h(V, R=RB):
    lo, hi = 0.0, R * TAN
    if math.pi * R * R * hi / 3 <= V: return hi, 0.0
    for _ in range(50):
        h = (lo + hi) / 2; r = R - h / TAN
        if math.pi * h / 3 * (R * R + R * r + r * r) < V: lo = h
        else: hi = h
    return h, R - h / TAN
used = set(); heaps = []; heap_skipped = []
for (px, py), (st, d) in sorted(pits.items()):
    V = 1.25 * 64.0 * d
    h, rt = frustum_h(V)
    Vh = math.pi * h / 3 * (RB * RB + RB * rt + rt * rt)
    spot = None
    for (ox, oy) in ((12, 12), (12, -12), (-12, 12), (-12, -12)):
        cx, cy = px + ox, py + oy
        if (cx, cy) in used or abs(cy) > 210: continue
        if any(_segd((cx, cy), a, b) < RB + 4 for a, b in _campts): continue
        if _rect_hit(cx, cy, RB + 1): continue
        spot = (cx, cy); break
    if not spot: heap_skipped.append((px, py)); continue
    used.add(spot)
    bm = bmesh.new(); seg = 18; rng = random.Random(int(px * 1000 + py))
    ring0 = [bm.verts.new((ft(RB * (1 + rng.uniform(-0.06, 0.06)) * math.cos(2 * math.pi * k / seg)),
                           ft(RB * (1 + rng.uniform(-0.06, 0.06)) * math.sin(2 * math.pi * k / seg)), 0.0)) for k in range(seg)]
    rm = (RB + rt) / 2; hm = h * 0.55
    ringm = [bm.verts.new((ft((rm + 0.4 * (RB - rm)) * (1 + rng.uniform(-0.08, 0.08)) * math.cos(2 * math.pi * k / seg)),
                           ft((rm + 0.4 * (RB - rm)) * (1 + rng.uniform(-0.08, 0.08)) * math.sin(2 * math.pi * k / seg)), ft(hm))) for k in range(seg)]
    top = bm.verts.new((0, 0, ft(h)))
    ring1 = [bm.verts.new((ft(max(rt, 0.6) * math.cos(2 * math.pi * k / seg)), ft(max(rt, 0.6) * math.sin(2 * math.pi * k / seg)), ft(h * 0.97))) for k in range(seg)]
    for k in range(seg):
        k2 = (k + 1) % seg
        bm.faces.new([ring0[k], ring0[k2], ringm[k2], ringm[k]]); bm.faces.new([ringm[k], ringm[k2], ring1[k2], ring1[k]])
        bm.faces.new([ring1[k], ring1[k2], top])
    ob = new_obj(f"KSPOIL_{px:+.0f}_{py:+.0f}", finish(bm, f"spoil_{px:+.0f}_{py:+.0f}", SPOIL), K["FOUNDATIONS"], (ft(spot[0]), ft(spot[1]), ft(-0.05)), 0,
                 {"part_kind": "spoil", "pit": f"{px:+.0f},{py:+.0f}", "pit_depth_ft": round(d, 2), "pit_vol_ft3": round(64 * d, 1),
                  "bulked_ft3": round(V, 1), "heap_ft3": round(Vh, 1), "carted_ft3": round(max(0, V - Vh), 1), "heap_h_ft": round(h, 2)})
    for sl in []: pass
    for f_ in ob.data.polygons: f_.use_smooth = True
    heaps.append(ob)
print("SPOIL heaps", len(heaps), "skipped", heap_skipped, flush=True)
# CP010 crew: in and beside the dug pits on the far side of the walk
worker(828, -186, -PAD[1]["top"] - PAD[1]["t"], "work", 0, "CP010")
worker(852, -192, 0, "work", 20, "CP010"); worker(855, -195, 0, "stand", 200, "CP010")
worker(804, -186, 0, "stand", 70, "CP010"); worker(780, -150, 0, "work", 180, "CP010")
for k in range(3):     # wheelbarrows of concrete (crude)
    bm = bmesh.new(); bm_box(bm, ft(-1.2), ft(1.2), ft(-0.9), ft(0.9), ft(0.8), ft(2.0)); cyl_axis(bm, (ft(1.4), ft(-0.4), ft(0.6)), (ft(1.4), ft(0.4), ft(0.6)), ft(0.6))
    new_obj(f"KBARROW_{k}", finish(bm, "barrow", PLANK), K["FOUNDATIONS"], (ft(810 + 6 * k), ft(-196 - 2 * k), 0), 0.4 * k, {"part_kind": "barrow"})

# ---------------- scaffolding (timber standards, ledgers, putlogs, plank deck) ----------------
def scaffold(name, x0, x1, ya, yb, lifts, deck_z, rail=None, step=8.0):
    bm = bmesh.new(); n0 = 0
    xs = [x0 + step * i for i in range(int(round((x1 - x0) / step)) + 1)]
    top = deck_z + (3.5 if rail else 0.5)
    for x in xs:
        for y in (ya, yb): bm_cyl(bm, inch(3), ft(-0.5), ft(top), 8, cx=ft(x), cy=ft(y))
        for z in lifts: bm_bar(bm, (ft(x), ft(ya - 0.6), ft(z)), (ft(x), ft(yb + 0.6), ft(z)), inch(4), inch(4))        # putlogs
    for y in (ya, yb):
        for z in lifts: bm_bar(bm, (ft(x0 - 0.6), ft(y), ft(z + 0.35)), (ft(x1 + 0.6), ft(y), ft(z + 0.35)), inch(4), inch(4))  # ledgers
    for i in range(0, len(xs) - 1, 2):              # diagonal braces on the outer face
        bm_bar(bm, (ft(xs[i]), ft(ya - 0.3), ft(0.3)), (ft(xs[i + 1]), ft(ya - 0.3), ft(deck_z)), inch(3), inch(3))
    if rail:
        bm_bar(bm, (ft(x0), ft(rail), ft(deck_z + 3.5)), (ft(x1), ft(rail), ft(deck_z + 3.5)), inch(3), inch(3))
        bm_bar(bm, (ft(x0), ft(rail), ft(deck_z + 1.8)), (ft(x1), ft(rail), ft(deck_z + 1.8)), inch(3), inch(3))
    faces_since(bm, 0, 0); n0 = len(bm.faces)
    bm_box(bm, ft(x0 - 0.5), ft(x1 + 0.5), ft(min(ya, yb)), ft(max(ya, yb)), ft(deck_z - inch(2.5) / FT), ft(deck_z))
    faces_since(bm, n0, 1)
    return new_obj(name, finish(bm, name, POLE, [PLANK]), K["SCAFFOLD"], props={"part_kind": "scaffold", "deck_ft": deck_z,
                   "x0": x0, "x1": x1, "y0": min(ya, yb), "y1": max(ya, yb)})
DECK_ROOF = 24.0
scaffold("KSCAF_ROOFEDGE", 288, 432, -216, -208, [6.0, 12.5, 18.0], DECK_ROOF, rail=-216)
scaffold("KSCAF_JOINT", 502, 514, -192, -184, [6.0, 12.5], 18.25, step=6.0)
scaffold("KSCAF_HEAD540", 536, 544, -190, -184, [6.0, 11.0], 16.0, step=4.0)
scaffold("KSCAF_HEAD564", 560, 568, -190, -184, [6.0, 11.0], 16.0, step=4.0)
for s in (-1, 1):
    scaffold(f"KSCAF_TIER2_{s:+d}", 472, 584, s * 66, s * 54, [6.0, 12.5, 17.5, 25.0, 31.0], 37.0, step=8.0)

# ---------------- CP012: sheer legs lifting a 24 ft girder into bay 540-564, row y -180 ----------------
LIFT_Z = 15.0
g = place("g24", "KGIR_HOIST_X552_Y-180", K["LIFTING"], 552, -180, LIFT_Z, 0.0, part_kind="girder", tier=1, state="hoisting")
APEX = (552.0, -180.0, 36.0)
bm = bmesh.new()
for fy in (-196.0, -164.0): cyl_axis(bm, (ft(552), ft(fy), 0), [ft(v) for v in APEX], inch(5), 10)
new_obj("KSHEERLEGS", finish(bm, "sheerlegs", POLE), K["LIFTING"], props={"part_kind": "sheer_legs", "apex_ft": list(APEX)})
bm = bmesh.new(); r = inch(0.6)
cyl_axis(bm, [ft(v) for v in APEX], (ft(552), ft(-180), ft(LIFT_Z + 0.1)), r, 6)            # fall to the girder sling
for a, b in (((546, -180, LIFT_Z + 0.05), (552, -180, LIFT_Z + 2.0)), ((558, -180, LIFT_Z + 0.05), (552, -180, LIFT_Z + 2.0))):
    cyl_axis(bm, [ft(v) for v in a], [ft(v) for v in b], r, 6)                               # sling
cyl_axis(bm, [ft(v) for v in APEX], (ft(558), ft(-204), ft(2.0)), r, 6)                      # lead to the crab winch
for gx, gy in ((530, -236), (576, -126)): cyl_axis(bm, [ft(v) for v in APEX], (ft(gx), ft(gy), 0), r, 6)   # guys
cyl_axis(bm, (ft(541), ft(-180), ft(LIFT_Z - 3)), (ft(536), ft(-196), ft(3.6)), r, 6)       # tag line
new_obj("KROPES", finish(bm, "ropes", ROPE), K["LIFTING"], props={"part_kind": "rope"})
bm = bmesh.new(); bm_box(bm, ft(-1.5), ft(1.5), ft(-1.2), ft(1.2), 0, ft(2.4)); cyl_axis(bm, (ft(-1.6), 0, ft(2.0)), (ft(1.6), 0, ft(2.0)), ft(0.6))
new_obj("KCRAB_WINCH", finish(bm, "crab", PLANK), K["LIFTING"], (ft(558), ft(-206), 0), 0, {"part_kind": "winch"})
worker(556, -208, 0, "work", 0, "CP012"); worker(560, -209, 0, "work", 0, "CP012")
worker(536, -197, 0, "work", 160, "CP012")
worker(540, -187, 16.0, "reach", 0, "CP012"); worker(564, -187, 16.0, "reach", 0, "CP012")
worker(470, -196, 0, "stand", 60, "CP012"); worker(500, -120, 0, "stand", 270, "CP012")
worker(520, -62, 37.0, "reach", 180, "CP012")

# ---------------- CP016: glazing wagons on the gutters (Muse 0174; Downes roof detail) ----------------
def mesh_wagon():
    bm = bmesh.new(); n0 = 0
    for sx in (-1.9, 1.9):
        for sy in (-4.0, 4.0):
            cyl_axis(bm, (ft(sx), ft(sy - 0.1), inch(2)), (ft(sx), ft(sy + 0.1), inch(2)), ft(0.5), 12)
    for sy in (-4.0, 4.0):                                                                    # open side frames (0174), c02
        bm_box(bm, ft(-2.5), ft(2.5), ft(sy) - inch(2), ft(sy) + inch(2), ft(1.55), ft(1.9))      # sole beam under the deck
        bm_box(bm, ft(-2.5), ft(2.5), ft(sy) - inch(1.5), ft(sy) + inch(1.5), inch(1), inch(5))   # axle bearer
        for px in (-2.2, -0.0, 2.2): bm_box(bm, ft(px) - inch(1.5), ft(px) + inch(1.5), ft(sy) - inch(1.5), ft(sy) + inch(1.5), inch(4), ft(1.6))
    bm_box(bm, ft(-2.5), ft(2.5), ft(-4.25), ft(4.25), ft(1.9), ft(2.05))                    # deck
    for hx in (-2.2, 0.0, 2.2):                                                                 # hoops for the canvas cover
        pts = [(4.0 * math.cos(math.pi * j / 10), 2.05 + 3.6 * math.sin(math.pi * j / 10)) for j in range(11)]
        for (ya, za), (yb, zb) in zip(pts, pts[1:]): bm_bar(bm, (ft(hx), ft(ya), ft(za)), (ft(hx), ft(yb), ft(zb)), inch(1.5), inch(1.5))
    bm_bar(bm, (ft(-2.2), 0, ft(5.65)), (ft(2.2), 0, ft(5.65)), inch(1.5), inch(1.5))
    faces_since(bm, 0, 1); n0 = len(bm.faces)
    bm_box(bm, ft(1.2), ft(2.3), ft(-1.2), ft(1.2), ft(2.05), ft(3.0)); faces_since(bm, n0, 1); n0 = len(bm.faces)   # pane crate
    for k in range(6):
        bm_box(bm, ft(1.3) + inch(1.6 * k), ft(1.3) + inch(1.6 * k) + inch(0.15), ft(-1.0), ft(1.0), ft(2.1), ft(3.4))
    faces_since(bm, n0, 0); n0 = len(bm.faces)
    bm_cyl(bm, ft(0.6), ft(2.05), ft(3.3), 12, cx=ft(-1.7), cy=ft(2.6)); faces_since(bm, n0, 1)   # putty barrel
    return finish(bm, "glazing_wagon", ROOFG, [WAGONT])
WAGON = mesh_wagon()
for i, yc in enumerate(WAGON_RIDGES):
    x = WAGON_X + (0 if i % 2 == 0 else 1.5)
    new_obj(f"KWAGON_{i}", WAGON, K["WAGONS"], (ft(x), ft(yc), ft(GIRDER_TOP[0])), 0,
            {"part_kind": "glazing_wagon", "gauge_ft": 8.0, "ridge_y": yc})
    worker(x - 0.8, yc - 1.6, GIRDER_TOP[0] + 2.05, "kneel", 270, "CP016")
    worker(x - 0.8, yc + 1.6, GIRDER_TOP[0] + 2.05, "work", 270, "CP016")
# CP014 on site (c02): rain water standing in the Paxton gutters of the glazed bay 300-324, tier-1 south
bm = bmesh.new()
for gy in (-196.0, -188.0, -180.0, -172.0):
    bm_box(bm, ft(300.3), ft(323.7), ft(gy) - inch(2), ft(gy) + inch(2), ft(GIRDER_TOP[0]) + inch(1.0), ft(GIRDER_TOP[0]) + inch(1.4))
new_obj("KSITE_GUTTER_WATER", finish(bm, "site_gutter_water", WATER), K["DETAIL_DRAINAGE"], (0, 0, 0), 0, {"part_kind": "site_water"})
# CP013: gutter walkers and a man on the roof-edge platform, clear of the cameras
worker(372, -168, GIRDER_TOP[0] - 0.3, "stand", 90, "CP013"); worker(386, -152, GIRDER_TOP[0] - 0.3, "work", 270, "CP013")
worker(300, -212, DECK_ROOF, "work", 90, "CP013")

# ---------------- floor: boards to x 300, bare joists 300-420 (CP013 timber) ----------------
slab_xyz("KFLOOR_BOARDS", 36, 300, -204, 204, -0.02, 0.04, FLOORM, K["FLOOR"], part_kind="floor")
bm = bmesh.new()
for k in range(int(408 / 2) + 1):          # CN22 (c03): joists 7 x 2 1/2 in (Catalogue p.62, printed) at 2 ft centres (inferred, as Muse hp-floor-boards)
    y = -204 + 2 * k
    bm_box(bm, ft(300), ft(420), ft(y) - inch(1.25), ft(y) + inch(1.25), -inch(7), ft(0.0))
new_obj("KFLOOR_JOISTS", finish(bm, "joists", WOOD), K["FLOOR"], props={"part_kind": "joist"})

# ---------------- CP015: louvre wall bays (Plate XXI ground tier; Plate XXVII machinery) under canvas ----------------
louvres = []
def louvre_bay(xc, animate):
    bm = bmesh.new()
    for k in range(4):
        x = xc - 12 + 8 * k; bm_box(bm, ft(x) - inch(2.5), ft(x) + inch(2.5), ft(-204) - inch(3), ft(-204) + inch(3), 0, ft(GIRDER_TOP[0] - 3))
    for (z0, z1) in ((0.5, 3.5), (5.0, 14.0)):                                   # boarding below and between the louvre bands
        bm_box(bm, ft(xc - 12), ft(xc + 12), ft(-204) - inch(1), ft(-204) + inch(1), ft(z0), ft(z1))
    bm_box(bm, ft(xc - 12), ft(xc + 12), ft(-204) - inch(3), ft(-204) + inch(3), ft(18.6), ft(19.17))
    new_obj(f"KWALL_{xc:+.0f}", finish(bm, f"wall_{xc}", WOODDARK), K["LOUVRE_CANVAS"], props={"part_kind": "wall"})
    for band, (z0, z1) in (("low", (3.5, 5.0)), ("high", (14.0, 18.6))):
        nbl = 3 if band == "low" else 8
        for k in range(nbl):
            z = z0 + (z1 - z0) * (k + 0.5) / nbl
            bm = bmesh.new(); bm_box(bm, ft(-12) + inch(3), ft(12) - inch(3), -inch(0.3), inch(0.3), -ft((z1 - z0) / nbl * 0.55), ft((z1 - z0) / nbl * 0.55))
            ob = new_obj(f"KLOUVRE_{xc:+.0f}_{band}_{k}", finish(bm, "blade", IRON), K["LOUVRE_CANVAS"], (ft(xc), ft(-204), ft(z)), 0,
                         {"part_kind": "louvre_blade"})
            if animate:
                for fr, ang in ((1, 0), (36, 62), (60, 62), (96, 0)):
                    ob.rotation_euler.x = math.radians(ang); ob.keyframe_insert("rotation_euler", index=0, frame=fr)
            louvres.append(ob)
for xc in (240, 264, 288): louvre_bay(xc, xc == 240)

# ---------------- OFFSITE: CP011 workshop yard (illustrative, x ~ 3000) ----------------
OY = K["OFFSITE_YARD"]
slab_xyz("KYARD_GROUND", 2950, 3050, -120, 140, -0.3, -0.01, SPOIL, OY, part_kind="ground")
bm = bmesh.new()
for x in (2984, 3016):
    for y in range(-80, 129, 16): bm_box(bm, ft(x) - inch(5), ft(x) + inch(5), ft(y) - inch(5), ft(y) + inch(5), 0, ft(18))
    bm_box(bm, ft(x) - inch(5), ft(x) + inch(5), ft(-80), ft(128), ft(17), ft(18))
for y in range(-80, 129, 16): bm_box(bm, ft(2984), ft(3016), ft(y) - inch(4), ft(y) + inch(4), ft(17.2), ft(18))
bm_box(bm, ft(2982), ft(3018), ft(-82), ft(130), ft(18.6), ft(18.9))
new_obj("KYARD_SHED", finish(bm, "shed", PLANK), OY, props={"part_kind": "shed"})
for pile, y0 in enumerate((-10.0, 22.0)):          # girders lying flat, 6 high
    for k in range(6):
        ob = new_obj(f"KYARD_GIR_{pile}_{k}", LIBM["g24"], OY, (ft(3008.0), ft(y0 + 12), ft(0.2 + k * 0.42)), 0, {"part_kind": "stock_girder"})
        ob.rotation_euler = (math.pi / 2, 0, math.pi / 2)
bm = bmesh.new()
for pile, yc in enumerate((0.0, 32.0)):            # columns lying in pyramids
    for row, n in enumerate((5, 4, 3)):
        for i in range(n):
            x = 2988.6 + (i + row * 0.5) * 0.72; z = 0.36 + row * 0.62
            cyl_axis(bm, (ft(x), ft(yc - 9.5), ft(z)), (ft(x), ft(yc + 9.5), ft(z)), inch(4), 12)
new_obj("KYARD_COLUMNS", finish(bm, "stock_columns", IRON), OY, props={"part_kind": "stock_column"})
bm = bmesh.new()                                    # timber: sash-bar bundles and Paxton gutters, a separate bay (CN11)
for i in range(4):
    for j in range(5):
        for k in range(3): bm_box(bm, ft(2988 + i * 1.6), ft(2989.3 + i * 1.6), ft(70 + j * 5), ft(74.3 + j * 5), ft(k * 1.0), ft(k * 1.0 + 0.9))
for k in range(6): bm_box(bm, ft(3005), ft(3007), ft(68), ft(92), ft(k * 0.55), ft(k * 0.55 + 0.5))
new_obj("KYARD_TIMBER", finish(bm, "stock_timber", WOOD), OY, props={"part_kind": "stock_timber"})
for (x, y, pose, d) in ((2992, 44, "work", 90), (3010, 10, "stand", 250), (2991, 82, "work", 90)):
    worker(x, y, 0, pose, d, "CP011")

# ---------------- OFFSITE: CP014 explanatory drainage cutaway (labelled, x ~ 3124, cut plane y = 200) ----------------
DD = K["DETAIL_DRAINAGE"]; CX, CY = 3124.0, 200.0
def half_tube(bm, cx, cy, ro, ri, z0, z1, seg=14, axis="z", x0=None, x1=None):
    """half of a hollow tube on the +y side of the cut plane y = cy."""
    def P(a, r, s):
        if axis == "z": return (ft(cx + r * math.cos(a)), ft(cy + r * math.sin(a)), ft(s))
        return (ft(s), ft(cy + r * math.sin(a)), ft(cx + r * math.cos(a)))     # axis x: cx is the pipe-centre z
    angs = [math.pi * k / seg for k in range(seg + 1)]
    lo, hi = (z0, z1) if axis == "z" else (x0, x1)
    for r in (ro, ri):
        for a, b in zip(angs, angs[1:]): bm.faces.new([bm.verts.new(P(a, r, lo)), bm.verts.new(P(b, r, lo)), bm.verts.new(P(b, r, hi)), bm.verts.new(P(a, r, hi))])
    for a in (0, math.pi): bm.faces.new([bm.verts.new(P(a, ri, lo)), bm.verts.new(P(a, ro, lo)), bm.verts.new(P(a, ro, hi)), bm.verts.new(P(a, ri, hi))])
    for s in (lo, hi):
        for a, b in zip(angs, angs[1:]): bm.faces.new([bm.verts.new(P(a, ri, s)), bm.verts.new(P(b, ri, s)), bm.verts.new(P(b, ro, s)), bm.verts.new(P(a, ro, s))])
R_O, R_I = 4 / 12, 3 / 12                     # 8 in external (D13); wall ~1 in (printed range 3/8-1 1/4 in)
COLTOP = GIRDER_TOP[0] + 0.19; DRAIN_Z = -1.9
bm = bmesh.new()
half_tube(bm, CX, CY, R_O, R_I, DRAIN_Z - 0.4, COLTOP)
half_tube(bm, DRAIN_Z, CY, R_O, R_I, 0, 0, axis="x", x0=CX + R_O, x1=CX + 26)
new_obj("KDET_COLUMN_CUT", finish(bm, "column_cut", CASTIRON), DD, props={"part_kind": "detail_column"})
bm = bmesh.new()
bm_box(bm, ft(CX - 24), ft(CX + R_O), ft(CY), ft(CY + 0.55), ft(COLTOP), ft(COLTOP + 0.12))        # gutter floor
bm_box(bm, ft(CX - 24), ft(CX + R_O), ft(CY + 0.45), ft(CY + 0.55), ft(COLTOP), ft(COLTOP + 0.6))  # gutter back wall
new_obj("KDET_GUTTER", finish(bm, "gutter_cut", WOOD), DD, props={"part_kind": "detail_gutter"})
place("g24", "KDET_GIRDER", DD, CX - 12, CY + 0.9, GIRDER_TOP[0], 0.0, part_kind="detail_girder")
bm = bmesh.new()
bm_box(bm, ft(CX - 24), ft(CX - R_I), ft(CY), ft(CY + 0.4), ft(COLTOP + 0.12), ft(COLTOP + 0.18))   # water in the gutter
half_tube(bm, CX, CY, R_I * 0.75, 0.001, DRAIN_Z, COLTOP + 0.15, seg=10)                            # water falling inside
half_tube(bm, DRAIN_Z, CY, R_I * 0.6, 0.001, 0, 0, seg=10, axis="x", x0=CX, x1=CX + 26)            # water in the drain
new_obj("KDET_WATER", finish(bm, "water", WATER), DD, props={"part_kind": "detail_water"})
slab_xyz("KDET_PAD", CX - 1.8, CX + 1.8, CY, CY + 0.9, DRAIN_Z - 2.9, DRAIN_Z - 0.4, CONCRETE, DD, part_kind="detail_pad")
slab_xyz("KDET_EARTH", CX - 30, CX + 30, CY + 1.0, CY + 30, -6, -0.02, EARTH, DD, part_kind="detail_earth")
slab_xyz("KDET_FLOORLINE", CX - 30, CX + 30, CY - 4, CY + 1.0, -0.1, 0.0, FLOORM, DD, part_kind="detail_floor")
def label(text, x, z, size=1.25):
    cu = bpy.data.curves.new(f"lbl_{text[:12]}", 'FONT'); cu.body = text; cu.size = ft(size); cu.extrude = 0.002
    ob = bpy.data.objects.new(f"KLABEL_{text[:18]}", cu); DD.objects.link(ob)
    ob.location = (ft(x), ft(CY - 0.6), ft(z)); ob.rotation_euler = (math.pi / 2, 0, 0); cu.materials.append(LABEL)
    ob["part_kind"] = "label"; return ob
label("Paxton gutter, rain water ->", CX - 9.5, COLTOP + 0.9, 0.7)
label("hollow cast-iron column", CX - 9.5, 14.0, 0.7); label("= rain-water pipe", CX - 9.5, 13.1, 0.7)
label("floor level", CX + 1.2, 0.4, 0.7)
label("drain", CX + 1.2, DRAIN_Z - 1.2, 0.7)
LABEL_LT = mat_principled("GT_LabelLight", (0.85, 0.83, 0.78), 0.9)
label("concrete pad", CX - 9.5, DRAIN_Z - 2.2, 0.7).data.materials[0] = LABEL_LT
label("explanatory cutaway, off site", CX - 9.5, -5.6, 0.55).data.materials[0] = LABEL_LT
slab_xyz("KDET_BACKDROP", CX - 40, CX + 40, CY + 30, CY + 30.5, -0.02, 40, mat_principled("GT_Backdrop", (0.30, 0.31, 0.32), 0.9), DD, part_kind="detail_backdrop")
_al = bpy.data.lights.new("KDET_FILL", 'AREA'); _al.energy = 6000; _al.size = ft(40)
_alo = bpy.data.objects.new("KDET_FILL", _al); DD.objects.link(_alo)
_alo.location = (ft(CX), ft(CY - 40), ft(12)); _alo.rotation_euler = (math.radians(90), 0, 0)

# ---------------- c03: site hoarding (south side, gate gap for carts) ----------------
bm = bmesh.new()
for (xa, xb) in ((0, 596), (634, 1000)):
    for k in range(int((xb - xa) / 0.75)):
        x = xa + k * 0.75
        bm_box(bm, ft(x), ft(x + 0.71), ft(-296.1), ft(-296.0), ft(0), ft(8.0 + 0.15 * ((k * 7) % 3)))
    for x in range(int(xa), int(xb), 8): bm_box(bm, ft(x), ft(x + 0.33), ft(-295.95), ft(-295.6), ft(0), ft(7.6))   # posts
    for z in (1.2, 6.4): bm_box(bm, ft(xa), ft(xb), ft(-295.95), ft(-295.75), ft(z), ft(z + 0.6))                    # rails
new_obj("KHOARDING_S", finish(bm, "hoarding", WOODDARK), K["GROUND"], props={"part_kind": "hoarding"})

# ---------------- c03: packing crates appended from Muse's models/hp-crate-and-display-case (read-only extract; CN24) ----------------
MUSE = "/workspace/models-main-ro/models/hp-crate-and-display-case/hp-crate-and-display-case.blend"
crates = []
if os.path.exists(MUSE):
    with bpy.data.libraries.load(MUSE, link=False) as (src, dst):
        dst.objects = [n for n in src.objects if n.startswith("Crate")]
    MC = bpy.data.collections.new("MUSE_Crate_by_Muse")      # not linked to the scene: instanced only
    MC["credit"] = "Muse, models/hp-crate-and-display-case (origin/main adb0d2c), appended read-only"
    MC.instance_offset = (-1.4, 0.0, 0.0)
    for o in dst.objects:
        if o: MC.objects.link(o)
    KC = coll("CRATES", ROOT)
    spots = []
    for i in range(4):                       # glass crates by the glazing bays, outside the south wall (x 300-420)
        for j in range(2):
            for lv in range(2 if (i + j) % 2 == 0 else 1): spots.append((356 + i * 3.6, -214 - j * 3.0, lv * 0.8 / 0.3048, 0.1 * i))
    for i in range(5): spots.append((544 + i * 3.8, -214.5 - (i % 2) * 2.5, 0, 0.3 * i))     # unloaded at the gate road (CP012 foreground)
    for i in range(3): spots.append((258 + i * 3.6, -186, 0, 0.0))                            # inside, by the louvre bays
    for n, (x, y, z, rz) in enumerate(spots):
        e = bpy.data.objects.new(f"KCRATE_{n:02d}", None); e.instance_type = 'COLLECTION'; e.instance_collection = MC
        e.location = (ft(x), ft(y), ft(z)); e.rotation_euler = (0, 0, rz); KC.objects.link(e)
        e["part_kind"] = "crate"; e["credit"] = "Muse"; crates.append(e)


# ---------------- c04: glaziers with panes (CN28) ----------------
# Glass at Hyde Park: 49 x 10 in sheets, 1/16 in (Chance), slid up the grooved sash bars from the wagon. Each "work" glazier
# holds a pane tipped ~30 deg toward the slope; a second pane lies half-slid into the bars ahead of the wagon.
PANE = mat_glass("GT_PaneLoose", tint=(0.52, 0.60, 0.58), bars=False, milk=0.10, milk_rgb=(0.62, 0.68, 0.66))
def mesh_pane():
    bm = bmesh.new(); bm_box(bm, -inch(5), inch(5), -inch(24.5), inch(24.5), -inch(0.06), inch(0.06))
    return finish(bm, "pane_49x10", PANE)
PANEM = mesh_pane(); panes = []
SLOPE = math.atan2(1.6, 4.0)
for i, yc in enumerate(WAGON_RIDGES):
    x = WAGON_X + (0 if i % 2 == 0 else 1.5)
    zt = GIRDER_TOP[0]
    ob = new_obj(f"KPANE_HELD_{i}", PANEM, K["WAGONS"], (ft(x + 0.95), ft(yc + 1.45), ft(zt + 2.05 + 3.85)), 0, {"part_kind": "pane", "state": "held", "tilt_deg": 30})
    ob.rotation_euler = (math.radians(-30), 0, 0); panes.append(ob)
    dy = 2.6          # pane centre 2.6 ft down the south slope from the ridge: about 70 % slid in
    ob = new_obj(f"KPANE_SLIDING_{i}", PANEM, K["WAGONS"], (ft(x + 3.4), ft(yc - dy * math.cos(SLOPE) * 0.93), ft(zt + 1.6 - dy * math.sin(SLOPE) * 0.93 + 0.12)), 0,
                 {"part_kind": "pane", "state": "sliding", "tilt_deg": round(math.degrees(SLOPE), 1)})
    ob.rotation_euler = (SLOPE, 0, 0); panes.append(ob)
    worker(x + 3.4, yc - 4.6, zt + 0.15, "reach", 0, "CP016")   # man in the gutter pushing the pane up the bars

# ---------------- c04: carts and horses at the gate (CN29) ----------------
sys.path.insert(0, HERE)
import figures
HORSE_MAT = mat_principled("GT_DraughtHorse", (0.13, 0.08, 0.05), 0.7)
HORSE_GREY = mat_principled("GT_DraughtHorseGrey", (0.42, 0.40, 0.37), 0.7)
HORSES = [figures.horse_group_mesh("horse_draught_bay", 2.35, HORSE_MAT, rearing=False, rider=False, base=False),
          figures.horse_group_mesh("horse_draught_grey", 2.35, HORSE_GREY, rearing=False, rider=False, base=False)]
IRONTYRE = mat_principled("GT_CartTyre", (0.06, 0.06, 0.06), 0.5, 0.6)
def mesh_cart(load):
    """two-wheeled tip cart (tumbril): 5 ft wheels, body 7 x 4.5 x 2 ft, floor 3 ft up, shafts forward (+x)."""
    bm = bmesh.new()
    for sy in (-2.55, 2.55):
        n0 = len(bm.faces)
        cyl_axis(bm, (ft(-3.5), ft(sy - 0.17), ft(2.5)), (ft(-3.5), ft(sy + 0.17), ft(2.5)), ft(2.5), 20); faces_since(bm, n0, 2)
        n0 = len(bm.faces); cyl_axis(bm, (ft(-3.5), ft(sy - 0.25), ft(2.5)), (ft(-3.5), ft(sy + 0.25), ft(2.5)), ft(0.45), 10); faces_since(bm, n0, 0)
        for k in range(6):
            a = math.pi * k / 6
            bm_bar(bm, (ft(-3.5 - 2.3 * math.cos(a)), ft(sy), ft(2.5 - 2.3 * math.sin(a))), (ft(-3.5 + 2.3 * math.cos(a)), ft(sy), ft(2.5 + 2.3 * math.sin(a))), inch(2.2), inch(2.2))
    cyl_axis(bm, (ft(-3.5), ft(-2.4), ft(2.5)), (ft(-3.5), ft(2.4), ft(2.5)), inch(2.5), 8)      # axle
    bm_box(bm, ft(-7), ft(0), ft(-2.25), ft(2.25), ft(2.9), ft(3.1))                            # floor
    for sy in (-2.25, 2.15): bm_box(bm, ft(-7), ft(0), ft(sy), ft(sy + 0.1), ft(3.1), ft(5.0))     # sides
    for sx in (-7, -0.1): bm_box(bm, ft(sx), ft(sx + 0.1), ft(-2.25), ft(2.25), ft(3.1), ft(5.0)) # ends
    for sy in (-1.45, 1.45):                                                                        # shafts to the collar
        bm_bar(bm, (ft(0), ft(sy), ft(3.0)), (ft(8.5), ft(sy * 0.75), ft(3.6)), inch(3), inch(3))
    bm_bar(bm, (ft(-1.0), ft(0), ft(0.0)), (ft(-1.0), ft(0), ft(2.9)), inch(3), inch(3))           # prop / tipping stop
    if load == "spoil":
        n0 = len(bm.faces); sphere(bm, (ft(-3.5), 0, ft(4.6)), 1.0, 2)
        for v in bm.verts[-len(bm.verts):]: pass
        faces_since(bm, n0, 3)
    elif load == "columns":
        n0 = len(bm.faces)
        for sy in (-1.2, -0.4, 0.4, 1.2): cyl_axis(bm, (ft(-9.5), ft(sy), ft(3.5)), (ft(3.0), ft(sy), ft(3.5)), inch(4), 12)
        faces_since(bm, n0, 4)
    me = finish(bm, f"tip_cart_{load}", WAGONT, [WOODDARK, IRONTYRE, SPOIL, PRIMER])
    if load == "spoil":      # flatten the sphere into a heaped load inside the body
        for v in me.vertices:
            if v.co.z > ft(4.0) and abs(v.co.x - ft(-3.5)) < ft(1.05) and abs(v.co.y) < ft(1.05):
                v.co.x = ft(-3.5) + (v.co.x - ft(-3.5)) * 3.2; v.co.y *= 2.0; v.co.z = ft(4.6) + (v.co.z - ft(4.6)) * 0.8
    return me
CARTM = {k: mesh_cart(k) for k in ("spoil", "columns", "empty")}
KCART = coll("CARTS", ROOT); carts = []
def cart(name, x, y, rz_deg, load, horse=0, carter=True):
    a = math.radians(rz_deg); ca, sa = math.cos(a), math.sin(a)
    ob = new_obj(f"KCART_{name}", CARTM[load], KCART, (ft(x), ft(y), 0), a, {"part_kind": "cart", "load": load, "credit": "Grok"})
    hx, hy = x + 5.0 * ca, y + 5.0 * sa
    h = new_obj(f"KHORSE_{name}", HORSES[horse], KCART, (ft(hx), ft(hy), 0), a, {"part_kind": "horse", "height_withers_ft": 5.6})
    carts.append(ob)
    if carter:
        wx, wy = x + 8.6 * ca + 2.4 * sa, y + 8.6 * sa - 2.4 * ca
        worker(wx, wy, 0, "stand", rz_deg - 90, "CARTS")
    return ob
cart("gate_in", 615, -303, 90, "columns", 0)                # entering by the gate in the south hoarding with columns
cart("gate_crates", 549, -224, 0, "empty", 1)               # unloaded beside the Muse crates (CP012 foreground left)
cart("spoil_828", 829, -192, 180, "spoil", 0)               # tip cart taking off surplus spoil (CN27)
worker(832.5, -189.0, 0, "work", 90, "CP010")               # shovelling into it
cart("road", 690, -318, 180, "empty", 1)                    # outside the hoarding on the site road

# ---------------- c04: closed glass crates and darker crate timber (CN30) ----------------
if crates:
    for m in {sl.material for o in MC.objects for sl in o.material_slots if sl.material}:
        if not m.name.endswith("_dk"):
            bsdf = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None) if m.node_tree else None
            if bsdf:
                c = bsdf.inputs["Base Color"].default_value; bsdf.inputs["Base Color"].default_value = (c[0] * 0.55, c[1] * 0.55, c[2] * 0.55, 1)
            m.diffuse_color = (m.diffuse_color[0] * 0.55, m.diffuse_color[1] * 0.55, m.diffuse_color[2] * 0.55, 1)
            m.name = m.name + "_by_Muse_dk"
    tim = next((sl.material for o in MC.objects for sl in o.material_slots if sl.material and sl.material.name.startswith("Timber_")), WOOD)
    bm = bmesh.new()                       # our sheathing boards over Muse's frame: 6 x 5 in boards, 1/4 in gaps, lid with 2 battens
    for k in range(5):
        z0 = 0.03 + k * 0.152; z1 = z0 + 0.146
        bm_box(bm, -1.905, -0.895, -0.405, -0.395, z0, z1); bm_box(bm, -1.905, -0.895, 0.395, 0.405, z0, z1)
        bm_box(bm, -1.905, -1.895, -0.395, 0.395, z0, z1); bm_box(bm, -0.905, -0.895, -0.395, 0.395, z0, z1)
    for k in range(6): bm_box(bm, -1.905 + k * 0.1683, -1.905 + k * 0.1683 + 0.162, -0.41, 0.41, 0.80, 0.82)
    for sx in (-1.75, -1.05): bm_box(bm, sx - 0.04, sx + 0.04, -0.41, 0.41, 0.82, 0.845)
    sheath = bpy.data.objects.new("CRATE_closed_sheathing_Grok", finish(bm, "crate_closed_sheathing", tim)); sheath["credit"] = "Grok"
    MCC = bpy.data.collections.new("CRATE_closed_on_Muse_frame")
    MCC["credit"] = "Muse crate frame (models/hp-crate-and-display-case, appended read-only) + Grok sheathing and lid"
    MCC.instance_offset = (-1.4, 0.0, 0.0)
    for o in MC.objects: MCC.objects.link(o)
    MCC.objects.link(sheath)
    for e in crates:
        if e.location.x < ft(420) and e.location.y < ft(-210):     # the glass crates by the glazing bays
            e.instance_collection = MCC; e["variant"] = "closed"

# ---------------- cameras ----------------
CAMS = bpy.data.collections.new("CAMERAS_CONSTRUCTION"); scene.collection.children.link(CAMS)
def cam(name, loc_ft, look_ft, lens, ortho=None):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.sensor_width = 36.0; cd.clip_start = 0.05; cd.clip_end = 3000
    if ortho: cd.type = 'ORTHO'; cd.ortho_scale = ortho
    ob = bpy.data.objects.new(name, cd); CAMS.objects.link(ob)
    ob.location = [ft(v) for v in loc_ft]
    d = Vector([ft(v) for v in look_ft]) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob
route = json.load(open(os.path.join(HERE, "..", "route", "camera_route.json")))
for shot in route["shots"]:
    for key in ("start", "end"):
        if key in shot:
            ob = cam(f"{shot['id']}_{key}", shot[key]["pos_ft"], shot[key]["look_ft"], shot["lens_mm"], shot.get("ortho_m"))
            ob["shot"] = shot["id"]
scene.camera = bpy.data.objects.get("CP012_bay_start")
scene.frame_start, scene.frame_end = 1, 96; scene.render.fps = 24

info = {"columns": len(cols), "girders": ngir, "roof_units": nroof, "roof_states": roof_states, "workers": len(workers),
        "foundations": len(found), "louvre_blades": len(louvres), "parts": len(parts), "muse_crates": len(crates), "spoil_heaps": len(heaps), "panes": len(panes), "carts": len(carts),
        "closed_crates": sum(1 for e in crates if e.get("variant") == "closed")}
scene["grok_construction_build"] = json.dumps(info)
scene["foundations"] = json.dumps(found); scene["nbars"] = NBARS
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
print("SAVED", OUT, json.dumps(info))
