"""HP-SITE: Hyde Park 1850 before work (storyboard CP006-CP009). Grok Bot.
  blender -b --factory-startup -P scripts/build_site.py -- --out rounds/s01.blend
Frame = Claude/Grok HP1851 frame: feet, origin at the transept crossing, X east, Y north; building lines x +-924, y -204..252.
The 1850 site drawing (Muse 0318 / round-2 S13 competition site drawing) is mapped by X = (px-425)*3.6, Y = (110-py)*3.6 (SD01).
One site, four states driven per camera by the 'grok_states' text block (render_shots.py):
  CP006 early 1850 bare trees + survey party; CP007 spring, committee study model on a table; CP008 summer, transept
  wireframe DESIGN STUDY over the elms; CP009 summer, hoarding, drawing table and first component stacks."""
import bpy, bmesh, math, random, sys, os, json
from mathutils import Vector, Matrix
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
OUT = arg("--out", "rounds/s01.blend")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOTDIR = os.path.dirname(HERE); sys.path.insert(0, HERE)
import parts1851 as P, trees as TR, figures as FG
from common import *
from parts1851 import box, rod, prism, mark, finish, I
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
sc = bpy.context.scene; rnd = random.Random(1850)
ROOT = bpy.data.collections.new("HPSITE1850_GROK"); sc.collection.children.link(ROOT)
info = {"credits": [], "counts": {}}
def px2ft(px, py): return ((px - 425) * 3.6, (110 - py) * 3.6)

# ---------------- materials ----------------
GRASS = noisy_mat("GT_ParkGrass1850", (0.10, 0.15, 0.05), (0.20, 0.25, 0.09), 0.06, 0.95, 0.15)
SAND = noisy_mat("GT_RottenRowSand", (0.42, 0.36, 0.26), (0.55, 0.48, 0.36), 0.5, 0.95, 0.3)
GRAVEL = noisy_mat("GT_PathGravel", (0.40, 0.36, 0.29), (0.52, 0.47, 0.38), 1.2, 0.95, 0.3)
ROADM = noisy_mat("GT_RoadMetal", (0.30, 0.28, 0.24), (0.40, 0.37, 0.31), 0.8, 0.95, 0.3)
BARK = mat("GT_Bark", (0.075, 0.065, 0.055), 0.95)
LEAF = TR.leaf_material()
FOL_S = mat("GT_FoliageSummer", (0.055, 0.095, 0.03), 0.85)
FOL_W = mat("GT_TwigsWinter", (0.13, 0.11, 0.09), 0.95)
OAK = mat("GT_OakPeg", (0.33, 0.25, 0.17), 0.85); WHITE = mat("GT_PegWhite", (0.78, 0.77, 0.72), 0.7)
REDP = mat("GT_PoleRed", (0.50, 0.08, 0.05), 0.6); BRASS = mat("GT_Brass", (0.55, 0.42, 0.18), 0.35, 0.9)
IRON = mat("GT_ChainIron", (0.10, 0.10, 0.10), 0.45, 0.8); DEAL = mat("GT_Deal", (0.52, 0.42, 0.30), 0.8)
BOARD = mat("GT_HoardingBoard", (0.22, 0.19, 0.15), 0.9); RAIL = mat("GT_RowRail", (0.28, 0.24, 0.19), 0.85)
PAINT = mat("GT_IronNew1850", (0.20, 0.19, 0.18), 0.55, 0.2)       # new castings, primed grey-black (SD13)
TIMBERP = mat("GT_SashBarBundle", (0.70, 0.66, 0.58), 0.8); ROPE = mat("GT_Rope", (0.45, 0.40, 0.30), 0.9)
GUTTER = mat("GT_GutterTimber", (0.55, 0.52, 0.46), 0.8); BAIZE = mat("GT_Baize", (0.10, 0.20, 0.10), 0.95)
CARD = mat("GT_ModelCard", (0.62, 0.50, 0.40), 0.8); DOMEM = mat("GT_ModelDome", (0.50, 0.50, 0.50), 0.6)
BRICKM = mat("GT_ModelBrick", (0.50, 0.30, 0.22), 0.85); INK = mat("GT_Ink", (0.03, 0.03, 0.04), 0.6)
LABEL = mat("GT_LabelCard", (0.82, 0.80, 0.72), 0.8, 0.0, 0.25)
WIRE = mat("GT_WireStudy", (1.0, 0.55, 0.12), 0.5, 0.0, 1.6); WIRE2 = mat("GT_WireStudyLabel", (1.0, 0.72, 0.3), 0.5, 0.0, 2.2)
HOUSE = mat("GT_DistantBrick", (0.42, 0.36, 0.30), 0.9); SLATE = mat("GT_Slate", (0.20, 0.21, 0.23), 0.8)
HORSE = mat("GT_Horse", (0.14, 0.09, 0.06), 0.7)
PAPER = bpy.data.materials.new("GT_DrawingSheet"); PAPER.use_nodes = True
_n = PAPER.node_tree.nodes; _t = _n.new("ShaderNodeTexImage")
_t.image = bpy.data.images.load(os.path.join(ROOTDIR, "textures", "drawing_cp009.png")); _t.image.pack()
PAPER.node_tree.links.new(_t.outputs[0], _n["Principled BSDF"].inputs["Base Color"]); _n["Principled BSDF"].inputs["Roughness"].default_value = 0.85
SK = [mat("GT_Skin_a", (0.72, 0.53, 0.42), 0.6), mat("GT_Skin_b", (0.60, 0.43, 0.33), 0.6)]
COAT = [mat("GT_Coat_blk", (0.03, 0.03, 0.035), 0.8), mat("GT_Coat_brn", (0.14, 0.10, 0.07), 0.85), mat("GT_Smock", (0.62, 0.60, 0.52), 0.9),
        mat("GT_Shirt", (0.74, 0.72, 0.66), 0.85), mat("GT_Coat_blue", (0.08, 0.10, 0.16), 0.8)]
TROU = [mat("GT_Trou_fawn", (0.36, 0.31, 0.23), 0.85), mat("GT_Trou_dk", (0.10, 0.09, 0.08), 0.85), mat("GT_Trou_grey", (0.30, 0.30, 0.30), 0.85)]
HAT = mat("GT_Hat", (0.02, 0.02, 0.02), 0.8); TRIM = mat("GT_Trim", (0.75, 0.74, 0.70), 0.8)
DRESS = [mat("GT_Dress_plum", (0.25, 0.10, 0.14), 0.8), mat("GT_Dress_grey", (0.40, 0.40, 0.42), 0.8)]

# ---------------- terrain (SD03) ----------------
def zg(x, y):
    return 1.1 * math.sin(x / 330.0 + 0.4) * math.cos(y / 270.0) + 0.5 * math.sin(x / 120.0 + y / 170.0) - 0.0004 * x
def ground_patch(name, c, x0, x1, y0, y1, zf, matl, res=6.0, z_off=0.0):
    bm = bmesh.new(); nx = int((x1 - x0) / res) + 1; ny = int((y1 - y0) / res) + 1
    vs = [[bm.verts.new((x0 + i * (x1 - x0) / (nx - 1), y0 + j * (y1 - y0) / (ny - 1), 0)) for j in range(ny)] for i in range(nx)]
    for row in vs:
        for v in row: v.co.z = zf(v.co.x, v.co.y) + z_off
    for i in range(nx - 1):
        for j in range(ny - 1): bm.faces.new([vs[i][j], vs[i + 1][j], vs[i + 1][j + 1], vs[i][j + 1]])
    o = obj(name, finish(bm, name, [matl]), c, part_kind="ground")
    for p in o.data.polygons: p.use_smooth = True
    return o
def strip(name, c, pts, w, matl, z_off, res=8.0):
    """a path ribbon draped on zg along a polyline (feet)"""
    bm = bmesh.new(); prev = None
    dense = []
    for a, b in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / res))
        for k in range(n): dense.append((a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n))
    dense.append(pts[-1])
    for i, p in enumerate(dense):
        q = dense[min(i + 1, len(dense) - 1)]; r = dense[max(i - 1, 0)]
        dx, dy = q[0] - r[0], q[1] - r[1]; L = math.hypot(dx, dy) or 1; nx_, ny_ = -dy / L * w / 2, dx / L * w / 2
        v1 = bm.verts.new((p[0] + nx_, p[1] + ny_, zg(p[0] + nx_, p[1] + ny_) + z_off)); v2 = bm.verts.new((p[0] - nx_, p[1] - ny_, zg(p[0] - nx_, p[1] - ny_) + z_off))
        if prev: bm.faces.new([prev[0], prev[1], v2, v1])
        prev = (v1, v2)
    o = obj(name, finish(bm, name, [matl]), c, part_kind="path")
    for p in o.data.polygons: p.use_smooth = True
    return o
GC = coll("GROUND", ROOT)
ground_patch("G_PARK", GC, -1500, 1500, -620, 900, zg, GRASS, 20.0)
ground_patch("G_PARK_NEAR", GC, -260, 260, -300, -120, zg, GRASS, 4.0, 0.02)       # finer facets where the cameras stand
bm = bmesh.new(); box(bm, -9000, 9000, -9000, 9000, -4.0, -2.5); obj("G_FAR", finish(bm, "g_far", [GRASS]), GC, part_kind="ground")
# north footpath (0318 'weg voor voetgangers'), kept clear of the 1851 north strip (SD02)
north = [px2ft(px, py) for (px, py) in ((0, 100), (45, 92), (100, 75), (200, 52), (300, 38), (425, 28), (550, 32), (650, 40), (775, 58), (940, 70))]
north = [(x, max(y + 40.0, 285.0)) for (x, y) in north]
def north_y(x):
    for a, b in zip(north, north[1:]):
        if a[0] <= x <= b[0]: return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])
    return north[-1][1]
strip("PATH_NORTH_FOOT", GC, north, 12.0, GRAVEL, 0.06)
rr_pts = [(x, y + 62.0) for (x, y) in north]
strip("ROTTEN_ROW", GC, rr_pts, 90.0, SAND, 0.05)                                  # 90 ft sand ride (SD04)
bm = bmesh.new()
for side in (-46.0, 46.0):
    for a, b in zip(rr_pts, rr_pts[1:]):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 9.0))
        for k in range(n):
            x = a[0] + (b[0] - a[0]) * k / n; y = a[1] + (b[1] - a[1]) * k / n + side; z = zg(x, y)
            box(bm, x - 0.25, x + 0.25, y - 0.25, y + 0.25, z - 0.3, z + 3.4)
        z = zg(a[0], a[1] + side)
        L = math.hypot(b[0] - a[0], b[1] - a[1]); ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for zz in (1.8, 3.2):
            M = Matrix.Translation((a[0], a[1] + side, z + zz)) @ Matrix.Rotation(ang, 4, 'Z')
            box(bm, 0, L, -0.12, 0.12, -0.14, 0.14, M=M)
obj("ROTTEN_ROW_RAILS", finish(bm, "rr_rails", [RAIL]), GC, part_kind="rail")
south = [(-1500, -262), (-600, -266), (0, -268), (600, -266), (1500, -262)]
strip("PATH_SOUTH_FOOT", GC, [(x, y + 8) for x, y in south], 10.0, GRAVEL, 0.06)
strip("DRIVE_FROM_KENSINGTON", GC, [(x, y - 14) for x, y in south], 28.0, ROADM, 0.05)
strip("KENSINGTON_ROAD", GC, [(-1500, -520), (0, -530), (1500, -520)], 50.0, ROADM, 0.05)
info["paths"] = {"north_footpath_y_at_x0": round(north_y(0), 1), "rotten_row_centre_y_at_x0": round(north_y(0) + 62, 1),
                 "south_drive_y": -282, "kensington_road_y": -530}

# ---------------- trees (SD05-SD08) ----------------
TC = coll("TREES", ROOT)
ELMS = [("ELM_SOUTH", 4.0, -128.0, 78.0, 3.6, 30.0), ("ELM_NORTH", -3.0, 142.0, 84.0, 4.0, 31.0), ("ELM_NORTH2", 12.0, 98.0, 64.0, 2.6, 22.0)]
BELT = [("ELM_BELT_1", -8.0, 196.0, 72.0, 3.0, 26.0), ("ELM_BELT_2", 9.0, 238.0, 76.0, 3.3, 27.0), ("ELM_BELT_3", -5.0, 283.0, 70.0, 2.9, 25.0)]
elm_rep = {}
for i, (n, x, y, H, D, CR) in enumerate(ELMS + BELT):
    W, L = TR.build_elm(n, x, y, zg(x, y), H, D, CR, 1851 + i if i < 3 else 1900 + i, BARK, LEAF, TC,
                        props={"source": "transept r10 ELMS (exact)" if i < 3 else "0318 belt, inferred"})
    L.name = "LV_" + n; elm_rep[n] = {"x": x, "y": y, "H": H, "cards": L["cards"]}
TMS = [TR.round_tree_mesh(f"TR_S_mesh_{k}", 30 + k, H, BARK, FOL_S, 0.2) for k, H in enumerate((58, 68, 78))]
TMW = [TR.round_tree_mesh(f"TR_W_mesh_{k}", 30 + k, H, BARK, FOL_W, 0.13) for k, H in enumerate((58, 68, 78))]
ntree = [0]
def park_tree(x, y, src):
    k = rnd.randrange(3); rz = rnd.uniform(0, 6.28); z = zg(x, y)
    obj(f"TR_S_{ntree[0]:03d}", TMS[k], TC, (x, y, z), rz, part_kind="park_tree", source=src)
    w = obj(f"TR_W_{ntree[0]:03d}", TMW[k], TC, (x, y, z), rz, part_kind="park_tree_winter", source=src); w.hide_render = True
    ntree[0] += 1
def clump(cx, cy, r, n, src):
    for k in range(n):
        a = rnd.uniform(0, 6.28); d = r * math.sqrt(rnd.random()); park_tree(cx + d * math.cos(a), cy + d * math.sin(a), src)
clump(*px2ft(235, 80), 70, 8, "0318 west clump")
for (px, py) in ((620, 40), (650, 50), (680, 42), (705, 38), (640, 66), (670, 70), (700, 60), (690, 76)):
    x, y = px2ft(px, py); park_tree(x + rnd.uniform(-10, 10), y + 30 + rnd.uniform(-10, 10), "0318 east clump")
for (px, py) in ((290, 18), (515, 38), (555, 38), (850, 65)):
    x, _ = px2ft(px, py); park_tree(x, north_y(x) - 16, "0318 trees on the north footpath")
for (px, py) in ((790, 110), (795, 155), (905, 100), (915, 125), (900, 150)):
    park_tree(*px2ft(px, py), "0318 beyond the east boundary")
for x in range(-1460, 1460, 64):                   # tree belts between the drive and Kensington Road (0318 hatched)
    for yy in (-350, -420):
        if abs(x) < 120 and yy == -350: continue      # keep the CP006 back view open (camera faces north anyway)
        park_tree(x + rnd.uniform(-14, 14), yy + rnd.uniform(-16, 16), "0318 south belts, generic")
for k in range(70):                                 # Hyde Park beyond Rotten Row: scattered (generic)
    x = rnd.uniform(-1400, 1400); park_tree(x, north_y(x) + 140 + rnd.uniform(0, 600), "generic park, north of Rotten Row")
info["counts"]["park_trees"] = ntree[0]; info["elms"] = elm_rep
bm = bmesh.new()                                    # Knightsbridge / Kensington Road frontage, distant (SD09)
for k in range(26):
    x0 = -1300 + k * 100 + rnd.uniform(0, 20); h = rnd.uniform(28, 46)
    box(bm, x0, x0 + rnd.uniform(60, 90), -600, -560, zg(x0, -580) - 1, zg(x0, -580) + h)
obj("DISTANT_HOUSES", finish(bm, "houses", [HOUSE]), GC, part_kind="distant")

# ---------------- people ----------------
def person(name, c, kind, mats, style, x, y, face_deg, z_extra=0.0, **props):
    me = FG.person_mesh("PM_" + name, kind, mats, style=style)
    return obj(name, me, c, (x, y, zg(x, y) + z_extra), math.radians(face_deg + 90), part_kind="figure", **props)
GENT = lambda j: [COAT[0 if j % 2 == 0 else 4], TROU[1 + j % 2], SK[j % 2], HAT, TRIM]
WORK = lambda j: [COAT[1 + j % 3], TROU[j % 2], SK[(j + 1) % 2], HAT, TRIM]

# ---------------- survey line and kit (SD10-SD12) ----------------
SV = coll("SURVEY", ROOT)
LINE_Y = -204.0
bm = bmesh.new(); npeg = 0
for k in range(-7, 8):                              # 24 ft pegs along a limited stretch of the south building line
    x = 24.0 * k; z = zg(x, LINE_Y)
    n0 = len(bm.faces); box(bm, x - 1.25 * I, x + 1.25 * I, LINE_Y - 1.25 * I, LINE_Y + 1.25 * I, z - 0.8, z + 0.95); mark(bm, n0, 0)
    n0 = len(bm.faces); box(bm, x - 1.3 * I, x + 1.3 * I, LINE_Y - 1.3 * I, LINE_Y + 1.3 * I, z + 0.75, z + 0.97); mark(bm, n0, 1); npeg += 1
for (x, y) in ((-924, -204), (924, -204), (-924, 252), (924, 252)):     # corner pegs, taller, white-headed
    z = zg(x, y); n0 = len(bm.faces); box(bm, x - 0.15, x + 0.15, y - 0.15, y + 0.15, z - 1, z + 2.2); mark(bm, n0, 0)
    n0 = len(bm.faces); box(bm, x - 0.16, x + 0.16, y - 0.16, y + 0.16, z + 1.8, z + 2.25); mark(bm, n0, 1)
obj("SV_PEGS", finish(bm, "pegs", [OAK, WHITE]), SV, part_kind="survey_peg", spacing_ft=24, count=npeg)
bm = bmesh.new()                                    # line cord between pegs (SD11)
for k in range(-7, 7):
    x0 = 24.0 * k; x1 = x0 + 24
    n = 6
    for j in range(n):
        a = x0 + 24 * j / n; b = x0 + 24 * (j + 1) / n
        rod(bm, (a, LINE_Y, zg(a, LINE_Y) + 0.85 - 0.25 * math.sin(math.pi * j / n)), (b, LINE_Y, zg(b, LINE_Y) + 0.85 - 0.25 * math.sin(math.pi * (j + 1) / n)), 0.012, 4)
obj("SV_LINE_CORD", finish(bm, "cord", [TRIM]), SV, part_kind="survey_line")
bm = bmesh.new()                                    # ranging poles, 8 ft, 1 ft red/white bands
for (x, y) in ((-168, LINE_Y), (168, LINE_Y), (-96, LINE_Y + 0.4), (-924, -204), (924, -204)):
    z = zg(x, y)
    for b in range(8):
        n0 = len(bm.faces); rod(bm, (x, y, z + b), (x, y, z + b + 1), 0.06, 8); mark(bm, n0, b % 2)
    n0 = len(bm.faces); rod(bm, (x, y, z - 0.6), (x, y, z), 0.04, 6); mark(bm, n0, 2)
obj("SV_TOOL_POLES", finish(bm, "poles", [REDP, WHITE, IRON]), SV, part_kind="ranging_pole", length_ft=8)
# Gunter's chain: 100 links of 7.92 in, brass tallies every 10 links, laid out east from x=-40 (SD12)
bm = bmesh.new(); x = -40.0; L_LINK = 7.92 * I; y0 = LINE_Y + 0.6
for k in range(100):
    xa, xb = x + k * L_LINK, x + (k + 1) * L_LINK; ya = y0 + 0.25 * math.sin(k / 9.0); yb = y0 + 0.25 * math.sin((k + 1) / 9.0)
    lift_a = max(0.0, (k - 96) / 4.0) * 2.0; lift_b = max(0.0, (k + 1 - 96) / 4.0) * 2.0
    n0 = len(bm.faces); rod(bm, (xa, ya, zg(xa, ya) + 0.03 + lift_a), (xb, yb, zg(xb, yb) + 0.03 + lift_b), 0.012, 4); mark(bm, n0, 0)
    if k % 10 == 9:
        n0 = len(bm.faces); box(bm, xb - 0.03, xb + 0.03, yb - 0.04, yb + 0.04, zg(xb, yb) + 0.01 + lift_b, zg(xb, yb) + 0.05 + lift_b); mark(bm, n0, 1)
for k in range(4):                                  # arrows (chaining pins) stuck at chain lengths
    xa = -40.0 - 66 * (k % 2) - 2; ya = y0 + 0.6 * k
    n0 = len(bm.faces); rod(bm, (xa, ya, zg(xa, ya) - 0.3), (xa, ya, zg(xa, ya) + 1.1), 0.012, 4); mark(bm, n0, 0)
obj("SV_TOOL_CHAIN", finish(bm, "chain", [IRON, BRASS]), SV, part_kind="gunters_chain", links=100, length_ft=66)
# theodolite on a tripod; levelling staff
TX, TY = -62.0, -208.0; tz = zg(TX, TY)
bm = bmesh.new()
for a in (0, 120, 240):
    r = math.radians(a + 30); n0 = len(bm.faces)
    rod(bm, (TX + 1.3 * math.cos(r), TY + 1.3 * math.sin(r), tz), (TX, TY, tz + 4.3), 0.05, 5); mark(bm, n0, 0)
n0 = len(bm.faces); P.lathe(bm, [(0, 0), (0.22, 0), (0.22, 0.12), (0.12, 0.2), (0.12, 0.45), (0.0, 0.45)], 16, M=Matrix.Translation((TX, TY, tz + 4.3))); mark(bm, n0, 1)
n0 = len(bm.faces); rod(bm, (TX - 0.55, TY, tz + 4.95), (TX + 0.65, TY, tz + 4.95), 0.07, 12); mark(bm, n0, 1)
n0 = len(bm.faces); rod(bm, (TX + 0.65, TY, tz + 4.95), (TX + 0.72, TY, tz + 4.95), 0.085, 12); mark(bm, n0, 2)
obj("SV_TOOL_THEODOLITE", finish(bm, "theodolite", [DEAL, BRASS, INK]), SV, part_kind="theodolite")
SX, SY_ = 62.0, -204.6; sz = zg(SX, SY_)
bm = bmesh.new()
for b in range(20):
    n0 = len(bm.faces); box(bm, SX - 0.18, SX + 0.18, SY_ - 0.05, SY_ + 0.05, sz + b * 0.5, sz + b * 0.5 + 0.5); mark(bm, n0, b % 2)
obj("SV_TOOL_STAFF", finish(bm, "staff", [WHITE, INK]), SV, part_kind="levelling_staff", length_ft=10)
SVP = coll("SURVEY_PARTY", ROOT); npp = 0
for (n, kind, mats, st, x, y, face) in (
        ("SVP_surveyor_theodolite", "man", GENT(0), {"hat": "top", "frock": True, "cravat": True}, TX - 2.1, TY, 0),
        ("SVP_surveyor_fieldbook", "man", GENT(1), {"hat": "top", "frock": True, "cravat": True}, TX + 3.0, TY - 5.0, 70),
        ("SVP_chainman_follower", "man", WORK(0), {"hat": "low", "belt": True}, -41.0, LINE_Y - 1.2, 0),
        ("SVP_chainman_leader", "man", WORK(1), {"hat": "cap"}, 26.5, LINE_Y - 0.6, 180),
        ("SVP_staffman", "man", WORK(2), {"hat": "cap"}, SX + 0.6, SY_ - 1.0, 170),
        ("SVP_boy_pole", "boy", WORK(0), {"hat": "cap"}, -96.0, LINE_Y - 1.3, 20)):
    person(n, SVP, kind, mats, st, x, y, face, role=n[4:]); npp += 1
for (n, kind, x, y, face, j) in (("SVP_visitor_woman", "woman", 48.0, -257.0, 180, 0), ("SVP_visitor_man", "man", 50.5, -256.0, 180, 1)):
    mats = [DRESS[j], DRESS[1 - j], SK[0], HAT, TRIM] if kind == "woman" else GENT(1)
    person(n, SVP, kind, mats, {"hat": "top", "cane": True} if kind == "man" else {"shawl": True}, x, y, face, role="park visitor")
hm = FG.horse_group_mesh("PM_rider", 2.4, HORSE, rearing=False, rider=True, base=False)
for k, (x, ang) in enumerate(((-260.0, 0), (210.0, 180), (420.0, 0))):
    obj(f"RIDER_{k}", hm, SVP, (x, north_y(x) + 62 + (k - 1) * 14, zg(x, north_y(x) + 62)), math.radians(ang), part_kind="rider_rotten_row")
info["counts"]["survey_party"] = npp

# ---------------- CP007: committee study model on a worktable (SD14-SD16) ----------------
CM = coll("COMMITTEE_TABLE", ROOT)
TXc, TYc = 40.0, -232.0; tzc = zg(TXc, TYc); TOP = 2.6
bm = bmesh.new()
n0 = len(bm.faces); box(bm, TXc - 3.5, TXc + 3.5, TYc - 1.6, TYc + 1.6, tzc + TOP - 0.12, tzc + TOP); mark(bm, n0, 0)
for sx in (-2.8, 2.8):                                # trestles
    for sy in (-1.3, 1.3):
        n0 = len(bm.faces); rod(bm, (TXc + sx + (0.25 if sy > 0 else -0.25) * 0, TYc + sy, tzc - 0.2), (TXc + sx, TYc + sy * 0.4, tzc + TOP - 0.12), 0.07, 5); mark(bm, n0, 0)
    n0 = len(bm.faces); box(bm, TXc + sx - 0.12, TXc + sx + 0.12, TYc - 0.9, TYc + 0.9, tzc + TOP - 0.32, tzc + TOP - 0.12); mark(bm, n0, 0)
obj("CM_TABLE", finish(bm, "cm_table", [DEAL]), CM, part_kind="worktable")
# model: 1:600 after the Berlyn 1851 ground plan of the Building Committee's design (S13 leaf 36)
SCL = 1 / 600.0; Lb = 2300 * SCL; Wb = Lb / 5.6; mz = tzc + TOP
bm = bmesh.new()
n0 = len(bm.faces); box(bm, TXc - Lb / 2 - 0.15, TXc + Lb / 2 + 0.15, TYc - Wb / 2 - 0.2, TYc + Wb / 2 + 0.2, mz, mz + 0.05); mark(bm, n0, 0)
B0 = mz + 0.05; HW = 30 * SCL * 2.0                    # walls ~30 ft, model height doubled for legibility (SD15)
n0 = len(bm.faces)
for (x0, x1, y0, y1) in ((-0.5, 0.5, -0.5, -0.42), (-0.5, 0.5, 0.42, 0.5), (-0.5, -0.49, -0.5, 0.5), (0.49, 0.5, -0.5, 0.5)):
    box(bm, TXc + x0 * Lb, TXc + x1 * Lb, TYc + y0 * Wb, TYc + y1 * Wb, B0, B0 + HW)
for k in range(1, 12):                                # long ranges of roofed halls (low ridges)
    if k in (5, 6): continue
    xx = -0.5 + k / 12.0; box(bm, TXc + xx * Lb - 0.03, TXc + xx * Lb + 0.03, TYc - 0.42 * Wb, TYc + 0.42 * Wb, B0, B0 + HW * 0.8)
box(bm, TXc - 0.5 * Lb, TXc + 0.5 * Lb, TYc - 0.42 * Wb, TYc + 0.42 * Wb, B0, B0 + HW * 0.55)
mark(bm, n0, 1)
RX = TXc - 0.04 * Lb; Rr = 100 * SCL
n0 = len(bm.faces); P.lathe(bm, [(0, 0), (Rr * 1.05, 0), (Rr * 1.05, 60 * SCL * 2), (0, 60 * SCL * 2)], 32, M=Matrix.Translation((RX, TYc, B0))); mark(bm, n0, 1)
prof = [(Rr * math.cos(t), 120 * SCL * 2 + Rr * 0.75 * math.sin(t)) for t in [i * math.pi / 2 / 10 for i in range(11)]]
n0 = len(bm.faces); P.lathe(bm, [(0, 120 * SCL * 2)] + prof, 32, M=Matrix.Translation((RX, TYc, B0))); mark(bm, n0, 2)
for (fx, fy) in ((0.28, 0.0), (-0.32, 0.0)):          # two enclosed courts with tree tufts (as the plan)
    for j in range(5):
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.035, matrix=Matrix.Translation((TXc + fx * Lb + rnd.uniform(-0.12, 0.12), TYc + fy + rnd.uniform(-0.12, 0.12), B0 + HW * 0.55 + 0.03)))
    for f in bm.faces:
        if f.material_index == 0 and not f.tag and len(f.verts) == 3: f.material_index = 3; f.tag = True
obj("CM_MODEL_COMMITTEE", finish(bm, "cm_model", [BAIZE, BRICKM, DOMEM, FOL_S]), CM, part_kind="study_model", scale="1:600",
    source="Berlyn & Fowler 1851, ground plan of the Building Committee's design (Muse round-2 S13)", evidence="B plan / C massing")
def text3d(name, c, txt, loc, rot, size, matl, align='CENTER', extrude=0.0):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = txt; cu.size = size; cu.align_x = align; cu.align_y = 'CENTER'; cu.extrude = extrude
    o = bpy.data.objects.new(name, cu); o.location = [ft(v) for v in loc]; o.rotation_euler = rot; o.scale = (FT, FT, FT)
    cu.materials.append(matl); c.objects.link(o); return o
bm = bmesh.new(); cxl, cyl = TXc + 1.6, TYc - 1.05
box(bm, cxl - 0.75, cxl + 0.75, cyl - 0.02, cyl + 0.02, mz, mz + 0.42)            # standing label card
obj("CM_LABEL_CARD", finish(bm, "cm_card", [LABEL]), CM, part_kind="label")
text3d("CM_LABEL_TEXT", CM, "UNBUILT COMMITTEE PROPOSAL\nstudy model, 1850 (interpretive)", (cxl, cyl - 0.03, mz + 0.22), (math.radians(90), 0, 0), 0.085, INK)
bm = bmesh.new()                                      # rolled drawings and an open sheet
for k in range(3): rod(bm, (TXc - 3.2, TYc + 0.6 + k * 0.28, mz + 0.12), (TXc - 0.9, TYc + 0.7 + k * 0.28, mz + 0.12), 0.12, 10)
box(bm, TXc + 2.2, TXc + 3.3, TYc - 0.2, TYc + 1.2, mz, mz + 0.01)
obj("CM_DRAWINGS", finish(bm, "cm_rolls", [LABEL]), CM, part_kind="drawings")

# ---------------- CP008: transept wireframe DESIGN STUDY (SD17-SD19) ----------------
OV = coll("OVERLAY_STUDY", ROOT)
SPRING, RV, XT, YH = 65.0, 37.1667, 36.0, 204.0
bm = bmesh.new(); rw = 0.13
def arc(y, r):
    pts = [(r * math.cos(t), y, SPRING + r * math.sin(t)) for t in [i * math.pi / 24 for i in range(25)]]
    for a, b in zip(pts, pts[1:]): rod(bm, a, b, rw, 5)
for k in range(18):
    arc(-YH + 24 * k, RV)
arc(YH - 0.01, RV)
for t in [i * math.pi / 6 for i in range(7)]:          # longitudinal purlin lines
    x, z = RV * math.cos(t), SPRING + RV * math.sin(t); rod(bm, (x, -YH, z), (x, YH, z), rw, 5)
for k in range(18):                                    # column lines and three tier lines on both transept walls
    y = -YH + 24 * k
    for s in (-1, 1): rod(bm, (s * XT, y, 0.3), (s * XT, y, SPRING), rw, 5)
for s in (-1, 1):
    for z in (24.2, 44.2, 64.2): rod(bm, (s * XT, -YH, z), (s * XT, YH, z), rw, 5)
for s in (-1, 1): rod(bm, (s * XT, YH, 0.3), (s * XT, YH, SPRING), rw, 5)
obj("OVL_TRANSEPT_WIRE", finish(bm, "ovl_wire", [WIRE]), OV, part_kind="design_study_overlay",
    source="Downes 1852 Plates XVIII/XX via Grok transept r10 (springing 65 ft, extrados 74 ft 4 in, 72 ft span, 408 ft)")
text3d("OVL_LABEL", OV, "DESIGN STUDY  -  not built\ntransept vault over the elms, developed June-July 1850", (-12.0, -196.0, 30.0),
       (math.radians(90), 0, math.radians(-12)), 1.5, WIRE2, 'CENTER')

# ---------------- CP009: hoarding, drawing table, first stacks (SD20-SD24) ----------------
ST = coll("FIRST_STACKS", ROOT)
HY = -247.0
bm = bmesh.new()
for x0 in range(-480, 480, 2):
    if 96 <= x0 < 120: continue                        # gate opening
    z = zg(x0 + 1, HY); box(bm, x0, x0 + 1.95, HY - 0.1, HY + 0.1, z - 0.3, z + 8.0)
for xp in range(-480, 481, 8):
    if 96 < xp < 120: continue
    z = zg(xp, HY); box(bm, xp - 0.22, xp + 0.22, HY + 0.1, HY + 0.55, z - 0.5, z + 8.2)
for zz in (1.4, 6.6): box(bm, -480, 96, HY + 0.1, HY + 0.4, zg(0, HY) + zz - 1.2, zg(0, HY) + zz - 0.7); box(bm, 120, 480, HY + 0.1, HY + 0.4, zg(300, HY) + zz - 1.2, zg(300, HY) + zz - 0.7)
obj("ST_HOARDING", finish(bm, "hoarding", [BOARD]), ST, part_kind="hoarding", note="contractor's close-boarded hoarding, 8 ft (SD21)")
COL18 = finish((lambda b: (P.add_column(b, 18 + 8 / 12), b)[1])(bmesh.new()), "column_18ft8", [PAINT])
CONN = finish((lambda b: (P.add_connecting_piece(b), b)[1])(bmesh.new()), "connecting_piece", [PAINT])
GIRD = finish((lambda b: (P.add_girder(b), b)[1])(bmesh.new()), "girder_24", [PAINT])
def stack(c, tag, ox, oy, zf):
    """first component stack (copy of the Grok move-1852 stack recipe, no crates): bearers + columns, girder rack, a row of
    connecting pieces (the repeated joint), sash-bar bundles"""
    out = {}; g = lambda x, y: zf(ox + x, oy + y)
    bm = bmesh.new(); z00 = max(g(-19, -12), g(0, -12)) + 0.6
    for x in (-17.0, -9.5, -2.0): box(bm, x - 0.4, x + 0.4, -16.5, -10.0, min(g(x, -16.5), g(x, -10)) - 0.3, z00)
    obj(f"{tag}_BEARERS_COL", finish(bm, f"{tag}_bear_c", [OAK]), c, (ox, oy, 0), part_kind="bearer")
    n = 0
    for li, nn in enumerate([4, 3]):
        for k in range(nn):
            y = -16.0 + P.COL_R * 2 * 1.04 * (k + 0.5 * li) + 1.4; z = z00 + P.COL_R + li * P.COL_R * 2 * 0.87
            o = obj(f"{tag}_COLUMN_{n:02d}", COL18, c, (ox - 19.0, oy + y, z), 0.0, part_kind="column", length_ft=18.667)
            o.rotation_euler = (0, math.radians(90), 0); n += 1
    out["columns"] = n
    gx0, ng = -30.0, 5; bm = bmesh.new(); zb = max(g(gx0 + ng * 0.8, yy) for yy in (-11, 0, 11)) + 0.5
    for yy in (-11.0, 0.0, 11.0): box(bm, gx0 - 0.8, gx0 + ng * 0.8 + 0.6, yy - 0.45, yy + 0.45, min(g(gx0 - 0.8, yy), g(gx0 + ng * 0.8, yy)) - 0.3, zb)
    obj(f"{tag}_BEARERS_GIR", finish(bm, f"{tag}_bear_g", [OAK]), c, (ox, oy, 0), part_kind="bearer")
    for k in range(ng): obj(f"{tag}_GIRDER_{k:02d}", GIRD, c, (ox + gx0 + k * 0.8, oy, zb + P.GIRDER_D + 0.05), math.radians(90), part_kind="girder")
    out["girders"] = ng
    nc = 8
    for k in range(nc):
        x, y = -4.0 - k * 1.25, 5.0
        obj(f"{tag}_CONN_{k:02d}", CONN, c, (ox + x, oy + y, g(x, y) + 0.02), math.radians(rnd.uniform(-6, 6)), part_kind="connecting_piece")
    out["conn"] = nc
    bm = bmesh.new()
    for b in range(2):
        bx, by = -18.0, 9.0 + b * 1.6; z = max(g(bx, by), g(bx + 8, by)) + 0.3
        n0 = len(bm.faces)
        for t in (0.6, 7.0): box(bm, bx + t, bx + t + 0.5, by - 0.6, by + 0.6, min(g(bx + t, by), g(bx + t + 0.5, by)) - 0.2, z)
        mark(bm, n0, 3); n0 = len(bm.faces); box(bm, bx, bx + 8.0, by - 0.55, by + 0.55, z, z + 1.0); mark(bm, n0, 0)
        n0 = len(bm.faces)
        for t in (0.8, 4.0, 7.2): box(bm, bx + t, bx + t + 0.12, by - 0.58, by + 0.58, z - 0.02, z + 1.03)
        mark(bm, n0, 1)
    obj(f"{tag}_BARS", finish(bm, f"{tag}_bars", [TIMBERP, ROPE, GUTTER, OAK]), c, (ox, oy, 0), part_kind="component_stack")
    return out
SOX, SOY = 185.0, -222.0
stats = stack(ST, "ST", SOX, SOY, zg)
# timber-wheeled dray bringing one more 18 ft 8 in column to the stack (fix s02; SD26)
CX, CY = 197.0, -228.0; cz = zg(CX, CY); WR = 2.4
bm = bmesh.new()
for sy in (-1, 1):                                    # two spoked wheels (rim, hub, 12 spokes)
    yw = CY + sy * 2.75
    for k in range(24):
        a0, a1 = 2 * math.pi * k / 24, 2 * math.pi * (k + 1) / 24
        rod(bm, (CX + WR * math.cos(a0), yw, cz + WR + WR * math.sin(a0)), (CX + WR * math.cos(a1), yw, cz + WR + WR * math.sin(a1)), 0.12, 6)
    for k in range(12):
        a = 2 * math.pi * k / 12; rod(bm, (CX, yw, cz + WR), (CX + (WR - 0.1) * math.cos(a), yw, cz + WR + (WR - 0.1) * math.sin(a)), 0.05, 5)
    rod(bm, (CX, yw - 0.35, cz + WR), (CX, yw + 0.35, cz + WR), 0.3, 10)
rod(bm, (CX, CY - 3.1, cz + WR), (CX, CY + 3.1, cz + WR), 0.14, 8)          # axle
box(bm, CX - 6.0, CX + 6.0, CY - 2.2, CY + 2.2, cz + WR + 0.25, cz + WR + 0.6)   # bed
for sy in (-1, 1):
    box(bm, CX - 6.0, CX + 6.0, CY + sy * 2.2 - 0.2, CY + sy * 2.2 + 0.2, cz + WR + 0.6, cz + WR + 1.1)  # side rails
    rod(bm, (CX + 5.5, CY + sy * 1.5, cz + WR + 0.4), (CX + 16.0, CY + sy * 1.25, cz + 3.4), 0.18, 6)   # shafts
box(bm, CX - 5.6, CX - 5.0, CY - 1.0, CY - 0.4, zg(CX - 5.3, CY) , cz + WR + 0.25)      # prop leg
obj("ST_CART", finish(bm, "st_cart", [DEAL]), ST, part_kind="cart", note="two-wheeled timber dray, interpretive (SD26)")
o = obj("ST_CART_COLUMN", COL18, ST, (CX - 9.0, CY, cz + WR + 0.6 + P.COL_R), 0.0, part_kind="column", length_ft=18.667); o.rotation_euler = (0, math.radians(90), 0)
hm = FG.horse_group_mesh("PM_carthorse", 2.5, HORSE, rearing=False, rider=False, base=False)
obj("ST_CARTHORSE", hm, ST, (CX + 14.5, CY, zg(CX + 14.5, CY)), 0.0, part_kind="horse")
person("ST_FIG_carter", ST, "man", WORK(2), {"hat": "low", "belt": True}, CX + 13.5, CY - 4.3, 150, role="carter")
DTX, DTY = 158.0, -243.0; dz = zg(DTX, DTY)
bm = bmesh.new()
n0 = len(bm.faces); box(bm, DTX - 2.5, DTX + 2.5, DTY - 1.4, DTY + 1.4, dz + 2.85, dz + 2.95); mark(bm, n0, 0)
for sx in (-2.2, 2.2):
    for sy in (-1.1, 1.1): n0 = len(bm.faces); box(bm, DTX + sx - 0.1, DTX + sx + 0.1, DTY + sy - 0.1, DTY + sy + 0.1, dz - 0.2, dz + 2.85); mark(bm, n0, 0)
obj("ST_DRAWING_TABLE", finish(bm, "dtable", [DEAL]), ST, part_kind="drawing_table")
def sheet(name, c, cx, cy, cz, w, h, rot):
    me = bpy.data.meshes.new(name); me.from_pydata([(-w / 2 * FT, -h / 2 * FT, 0), (w / 2 * FT, -h / 2 * FT, 0), (w / 2 * FT, h / 2 * FT, 0), (-w / 2 * FT, h / 2 * FT, 0)], [], [(0, 1, 2, 3)])
    me.uv_layers.new(); uv = me.uv_layers[0].data
    for i, (u, v) in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv[i].uv = (u, v)
    me.materials.append(PAPER); o = obj(name, me, c, (cx, cy, cz)); o.rotation_euler = rot; o["part_kind"] = "drawing"; return o
sheet("ST_DRAWING_ON_TABLE", ST, DTX - 0.4, DTY + 0.1, dz + 2.955, 3.0, 2.0, (0, 0, math.radians(180 + 4)))
sheet("ST_DRAWING_HANDED", ST, DTX + 2.05, DTY - 0.1, dz + 3.75, 1.5, 1.0, (math.radians(70), 0, math.radians(90)))
person("ST_FIG_engineer", ST, "man", GENT(0), {"hat": "top", "frock": True, "cravat": True}, DTX + 3.25, DTY - 0.1, 180, role="engineer (Fox, Henderson)")
person("ST_FIG_foreman", ST, "man", WORK(1), {"hat": "low", "belt": True}, DTX + 0.35, DTY - 2.6, 60, role="foreman")
for k, (x, y, f) in enumerate(((178.0, -207.0, 250), (179.0, -230.6, 200), (150.0, -214.0, 300))):
    person(f"ST_FIG_workman_{k}", ST, "man", WORK(k), {"hat": ("cap", "low", "cap")[k]}, x, y, f, role="workman")
info["stack"] = stats

# ---------------- world, states, cameras ----------------
world(sun_elev=36, sun_rot=160, strength=0.35, sun_energy=3.0, exposure=-0.4)
states = {"CP006": {"hide": ["LV_", "TR_S_", "CM_", "ST_", "OVL_"], "show": ["TR_W_"], "exposure": -0.25},
          "CP007": {"hide": ["ST_", "OVL_", "SVP_", "SV_TOOL"]},
          "CP008": {"hide": ["CM_", "ST_", "SVP_", "SV_TOOL"], "show": ["OVL_"]},
          "CP009": {"hide": ["CM_", "OVL_", "SVP_", "SV_TOOL"], "show": ["ST_"]}}
for o in bpy.data.objects:
    if o.name.startswith(("OVL_", "ST_")): o.hide_render = True
t = bpy.data.texts.new("grok_states"); t.write(json.dumps(states, indent=1))
cams = cameras(os.path.join(ROOTDIR, "route", "camera_route.json"), ROOT, zfun=zg)
info.update({"cams": [c.name for c in cams], "objects": len(bpy.data.objects), "states": states,
             "credits": ["Grok transept r10 elm positions and recipe (own work)", "Grok move-1852 stack recipe (own work)"]})
sc["grok_site"] = json.dumps(info)
print("SITE_INFO", json.dumps({k: v for k, v in info.items() if k != "states"}), flush=True)
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True)
print("SAVED", OUT)
