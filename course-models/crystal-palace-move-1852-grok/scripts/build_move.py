"""MOVE + K-JOINT (storyboard CP032, 1852). Grok Bot.
  blender -b --factory-startup -P scripts/build_move.py -- --out rounds/m01.blend
Regions (feet; X east, Y north, Z up), each with its own ground so no shot sees another:
  K   (0, 0)      K-JOINT hero kit: a trial assembly of one connecting piece with girders, keys and wedges (Downes VIII)
  DEP (0, 600)    departure stack, Hyde Park 1852 (park ground, elms, a stripped frame beyond); camera looks west
  ARR (0, 1600)   receiving stack, Sydenham (Penge Place) 1852: a generic sloping, wooded site; camera looks east
  MAP (0, -400)   two-site schematic locator plane (no route drawn), top-down ortho insert
Muse kits appended read-only: hp-crate-and-display-case (crates), hp-great-elm (distant elms), park-bench."""
import bpy, bmesh, math, random, sys, os, json
from mathutils import Vector, Matrix
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
OUT = arg("--out", "rounds/m01.blend")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOTDIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import parts1851 as P, trees as TR, figures as FG
from common import *
from parts1851 import box, rod, beam, prism, wedge, mark, finish, I
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
sc = bpy.context.scene; rnd = random.Random(1852)
ROOT = bpy.data.collections.new("MOVE1852_GROK"); sc.collection.children.link(ROOT)
info = {"credits": [], "regions": {"K": [0, 0], "DEP": [0, 600], "ARR": [0, 1600], "MAP": [0, -400]}}

# ---------------- materials ----------------
PAINT = mat("GT_IronPaint1851", (0.17, 0.25, 0.38), 0.6, 0.0)          # Owen Jones blue, weathered (1851 paint, stripped 1852)
PAINT_K = mat("GT_IronPaintKit", (0.19, 0.27, 0.40), 0.5, 0.0)
WI = mat("GT_WroughtIronKey", (0.055, 0.055, 0.06), 0.42, 0.7)
OAKK = mat("GT_OakKey", (0.40, 0.27, 0.15), 0.7)
BOLT = mat("GT_BoltNut", (0.07, 0.07, 0.075), 0.5, 0.6)
OAK = mat("GT_OakBearer", (0.30, 0.23, 0.16), 0.85)
DEAL = mat("GT_Deal", (0.52, 0.42, 0.30), 0.8)
BOARD = mat("GT_HoardingBoard", (0.20, 0.17, 0.13), 0.9)
CRATEW = mat("GT_PackingCase", (0.36, 0.28, 0.19), 0.85)
ROPE = mat("GT_Rope", (0.45, 0.40, 0.30), 0.9)
TIMBERP = mat("GT_SashBarBundle", (0.70, 0.66, 0.58), 0.8)
GUTTER = mat("GT_GutterTimber", (0.55, 0.52, 0.46), 0.8)
BARK = mat("GT_Bark", (0.075, 0.065, 0.055), 0.95)
LEAF = TR.leaf_material()
FOLIAGE = mat("GT_Foliage", (0.06, 0.10, 0.03), 0.85)
FOLIAGE_SY = mat("GT_FoliageOak", (0.07, 0.11, 0.035), 0.85)
GRASS = noisy_mat("GT_Grass1852", (0.10, 0.16, 0.05), (0.19, 0.25, 0.09), 0.08, 0.95, 0.15)
TROD = noisy_mat("GT_TroddenGround", (0.20, 0.17, 0.12), (0.30, 0.26, 0.18), 0.4, 0.95, 0.3)
GRAVEL = noisy_mat("GT_YardGravel", (0.33, 0.30, 0.25), (0.45, 0.41, 0.34), 1.5, 0.95, 0.4)
CLAY = noisy_mat("GT_SydenhamClay", (0.36, 0.22, 0.12), (0.50, 0.34, 0.19), 0.3, 0.95, 0.4)
SK = [mat("GT_Skin_a", (0.72, 0.53, 0.42), 0.6), mat("GT_Skin_b", (0.60, 0.43, 0.33), 0.6)]
WCOAT = [mat("GT_WorkCoat_dk", (0.05, 0.05, 0.06), 0.85), mat("GT_WorkCoat_brn", (0.14, 0.10, 0.07), 0.85),
         mat("GT_WorkSmock", (0.62, 0.60, 0.52), 0.9), mat("GT_WorkShirt", (0.74, 0.72, 0.66), 0.85)]
WTROU = [mat("GT_WorkTrou_fawn", (0.36, 0.31, 0.23), 0.85), mat("GT_WorkTrou_dk", (0.10, 0.09, 0.08), 0.85)]
HATS = [mat("GT_WorkCap", (0.08, 0.07, 0.06), 0.85), mat("GT_HatBlack", (0.02, 0.02, 0.02), 0.8)]
TRIM = mat("GT_TrimWhite", (0.75, 0.74, 0.70), 0.8)
HORSE = mat("GT_DraughtHorse", (0.13, 0.08, 0.05), 0.7)

# ---------------- shared part meshes ----------------
def m_column(L, name):
    bm = bmesh.new(); P.add_column(bm, L); return finish(bm, name, [PAINT])
def m_conn(name, matl=PAINT):
    bm = bmesh.new(); P.add_connecting_piece(bm); return finish(bm, name, [matl])
def m_girder(name, matl=PAINT):
    bm = bmesh.new(); P.add_girder(bm); return finish(bm, name, [matl])
COL18 = m_column(18 + 8 / 12, "column_18ft8")             # tier-1 column 'a' 18 ft 8 in (Downes p.4)
CONN = m_conn("connecting_piece")
GIRD = m_girder("girder_24")

# ---------------- people ----------------
PM = [FG.person_mesh(f"PERSON_workman_{j}", "man", [WCOAT[j % 4], WTROU[j % 2], SK[j % 2], HATS[j % 2], TRIM],
                     style={"hat": ("cap", "low", "cap", "top", "cap", "low")[j], "belt": j % 2 == 0}) for j in range(6)]
PM_CLERK = FG.person_mesh("PERSON_clerk", "man", [WCOAT[0], WTROU[1], SK[0], HATS[1], TRIM], style={"hat": "top", "frock": True, "cravat": True})
staff = []
def man(c, x, y, face_deg, z=0.0, k=None, role="workman"):
    me = PM_CLERK if role == "clerk" else PM[(len(staff) if k is None else k) % len(PM)]
    # figures.person_mesh faces -Y at rz 0, so a facing direction needs rz = face + 90 (DM18)
    o = obj(f"STAFF_{len(staff):02d}_{role}", me, c, (x, y, z), math.radians(face_deg + 90), part_kind="figure", role=role)
    staff.append(o); return o

# ---------------- Muse kits (read-only append) ----------------
MC = muse_collection(f"{MUSE_ROOT}/hp-crate-and-display-case/hp-crate-and-display-case.blend", "MUSE_Crate_by_Muse",
                     lambda n: n.startswith("Crate"), "Muse, models/hp-crate-and-display-case (origin/main), appended read-only",
                     (-1.4, 0.0, 0.0))
bm = bmesh.new()                       # closed sheathing over Muse's frame (Grok, construction c04 / dismantle recipe), metres
def mbox(x0, x1, y0, y1, z0, z1): box(bm, x0 / P.FT, x1 / P.FT, y0 / P.FT, y1 / P.FT, z0 / P.FT, z1 / P.FT)
for k in range(5):
    z0 = 0.03 + k * 0.152; z1 = z0 + 0.146
    mbox(-1.905, -0.895, -0.405, -0.395, z0, z1); mbox(-1.905, -0.895, 0.395, 0.405, z0, z1)
    mbox(-1.905, -1.895, -0.395, 0.395, z0, z1); mbox(-0.905, -0.895, -0.395, 0.395, z0, z1)
for k in range(6): mbox(-1.905 + k * 0.1683, -1.905 + k * 0.1683 + 0.162, -0.41, 0.41, 0.80, 0.82)
sh = bpy.data.objects.new("CRATE_closed_sheathing_Grok", finish(bm, "crate_sheathing", [CRATEW])); MC.objects.link(sh)
ME = muse_collection(f"{MUSE_ROOT}/hp-great-elm/hp-great-elm.blend", "MUSE_GreatElm_by_Muse",
                     lambda n: n.startswith(("Branch", "Crown", "Trunk", "Leaf")), "Muse, models/hp-great-elm (origin/main), appended read-only")
MB = muse_collection(f"{MUSE_ROOT}/park-bench/park-bench.blend", "MUSE_ParkBench_by_Muse",
                     lambda n: not n.startswith(("Cam", "Backdrop", "Ground", "Key", "Fill", "Rim", "Light", "Sun")), "Muse, models/park-bench (origin/main), appended read-only")
info["credits"] += ["Muse crate (hp-crate-and-display-case)", "Muse great elm (hp-great-elm), distant only", "Muse park bench"]
CRATE_H = 0.845 / P.FT
for c in (MC, ME, MB):
    if c.name not in [x.name for x in sc.collection.children]: pass   # kept unlinked: instancing only

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

# ======================= K: the K-JOINT hero kit =======================
KC = coll("K_JOINT", ROOT)
flat = lambda x, y: 0.0
ground_patch("K_GROUND", KC, -60, 60, -60, 60, flat, GRAVEL, 10.0)
bm = bmesh.new()
for k in range(30): box(bm, -27.2, -27.0, -30 + k * 2.0, -30 + k * 2.0 + 1.95, 0, 9.0)    # close-boarded hoarding beyond the girder ends
for z in (1.5, 7.5): box(bm, -27.0, -26.6, -30, 30, z, z + 0.6)
for k in range(-30, 31, 10): box(bm, -26.6, -26.1, k - 0.25, k + 0.25, 0, 9.2)
obj("K_HOARDING", finish(bm, "k_hoarding", [BOARD]), KC, part_kind="hoarding")
bm = bmesh.new()
for k in range(30): box(bm, -30 + k * 2.0, -30 + k * 2.0 + 1.95, 27.0, 27.2, 0, 9.0)
obj("K_HOARDING_N", finish(bm, "k_hoarding_n", [BOARD]), KC, part_kind="hoarding")
Z0 = 1.7                                                     # bottom of the connecting piece on the trial stand
bm = bmesh.new()
box(bm, -1.4, 1.4, -1.4, 1.4, 0.0, 0.5)                      # oak sole
for s in (-1, 1): box(bm, -2.6, 2.6, s * 0.9 - 0.3, s * 0.9 + 0.3, 0.0, 0.35)
obj("K_SOLE", finish(bm, "k_sole", [OAK]), KC, part_kind="stand")
bm = bmesh.new(); P.add_column(bm, Z0 - 0.5, bot_flange=False, M=Matrix.Translation((0, 0, 0.5)))
P.add_column(bm, 1.1, top_flange=False, M=Matrix.Translation((0, 0, Z0 + P.CONN_L)))
obj("K_COLUMN_STUBS", finish(bm, "k_col_stubs", [PAINT_K]), KC, part_kind="column", note="lower stub + upper column foot (trial stand)")
bm = bmesh.new(); P.add_connecting_piece(bm, M=Matrix.Translation((0, 0, Z0)))
obj("K_CONNECTING_PIECE", finish(bm, "k_conn", [PAINT_K]), KC, part_kind="connecting_piece", length_ft=P.CONN_L)
GZ = Z0 + P.GIRDER_TOP_IN_CP
def k_girder(face, pull=0.0, tag=""):
    a = math.radians(90 * face)
    d = P.COL_R + 0.25 * I + P.GIRDER_L / 2 + pull
    M = Matrix.Rotation(a, 4, 'Z') @ Matrix.Translation((d, 0, GZ))
    bm = bmesh.new(); P.add_girder(bm, M)
    o = obj(f"K_GIRDER_{tag}", finish(bm, f"k_girder_{tag}", [PAINT_K]), KC, part_kind="girder", face=face, pull_ft=pull)
    # far-end trestle at 20 ft
    far = Matrix.Rotation(a, 4, 'Z')
    bm = bmesh.new(); tz = GZ - P.GIRDER_D
    for dx in (19.0, 22.0):
        for s in (-1, 1):
            p0 = far @ Vector((dx, s * 1.3, 0)); p1 = far @ Vector((dx, s * 0.25, tz))
            rod(bm, p0, p1, 0.12, 6)
        q0 = far @ Vector((dx, 0, tz - 0.25)); box(bm, q0.x - 0.4, q0.x + 0.4, q0.y - 0.4, q0.y + 0.4, tz - 0.3, tz)
    obj(f"K_TRESTLE_{tag}", finish(bm, f"k_trestle_{tag}", [DEAL]), KC, part_kind="trestle")
    return o
k_girder(0, 0.0, "E_ironkeys"); k_girder(1, 0.0, "N_oakkeys"); k_girder(2, 0.75, "W_exploded")
bm = bmesh.new(); P.add_keys(bm, Matrix.Translation((0, 0, Z0)), driven=True)
obj("K_KEYS_IRON_E", finish(bm, "k_keys_iron", [WI]), KC, part_kind="key", material_note="wrought iron (within 200 ft of the ends/transept)")
bm = bmesh.new(); P.add_keys(bm, Matrix.Translation((0, 0, Z0)) @ Matrix.Rotation(math.radians(90), 4, 'Z'), driven=True)
obj("K_KEYS_OAK_N", finish(bm, "k_keys_oak", [OAKK]), KC, part_kind="key", material_note="oak (the two ~500 ft intermediate runs)")
# loose keys for the exploded W joint laid on a little trestle stool beside it, with a hand maul
bm = bmesh.new(); sx, sy, sz = -2.3, 1.6, 2.7
for (dx, dy) in ((-0.9, -0.5), (0.9, -0.5), (-0.9, 0.5), (0.9, 0.5)): rod(bm, (sx + dx, sy + dy, 0), (sx + dx * 0.8, sy + dy * 0.8, sz), 0.08, 6)
box(bm, sx - 1.1, sx + 1.1, sy - 0.65, sy + 0.65, sz, sz + 0.12)
obj("K_STOOL", finish(bm, "k_stool", [DEAL]), KC, part_kind="trestle")
bm = bmesh.new(); zt = sz + 0.12
for k, dy in enumerate((-0.45, -0.25, -0.05, 0.15)):          # four T keys lying flat (taper 0.95 -> 0.55 in, ~3.8 in long)
    wedge(bm, 0, 0, 0.0, 2.8 * I, 0.0, 3.8 * I, 0.95 * I, 0.55 * I,
          Matrix.Translation((sx - 0.1 + 0.03 * k, sy + dy, zt)) @ Matrix.Rotation(math.radians(-90), 4, 'Y'))
box(bm, sx + 0.2, sx + 0.45, sy - 0.4, sy - 0.24, zt, zt + 1.9 * I)                     # S key
obj("K_KEYS_LOOSE_W", finish(bm, "k_keys_loose", [WI]), KC, part_kind="key", state="knocked out")
bm = bmesh.new(); rod(bm, (sx + 0.1, sy + 0.35, zt + 0.06), (sx + 1.0, sy + 0.1, zt + 0.06), 0.035, 6)
rod(bm, (sx + 0.1, sy + 0.25, zt + 0.06), (sx + 0.1, sy + 0.45, zt + 0.06), 0.07, 8)
obj("K_HAND_MAUL", finish(bm, "k_maul", [BOLT]), KC, part_kind="tool")
info["kjoint"] = {"conn_bottom_ft": Z0, "girder_top_ft": round(GZ, 4), "girder_depth_ft": P.GIRDER_D, "conn_len_ft": P.CONN_L}

# ======================= stacks (shared builder) =======================
def stack(c, tag, ox, oy, zf, style):
    """component stack: bearers + columns (axis X, ends toward +X), girders on edge in a rack (axis Y), connecting
    pieces upright in a row, sash-bar bundles, gutters, crates. Positions are offsets from (ox, oy) in feet."""
    out = {}
    g = lambda x, y: zf(ox + x, oy + y)
    # bearers
    bm = bmesh.new()
    z00 = max(g(-19, -12), g(0, -12)) + 0.6                    # bearer tops level: stepped packing on a slope
    for x in (-17.0, -9.5, -2.0):
        box(bm, x - 0.4, x + 0.4, -16.5, -10.0, min(g(x, -16.5), g(x, -10)) - 0.3, z00)
    obj(f"{tag}_BEARERS_COL", finish(bm, f"{tag}_bear_c", [OAK]), c, (ox, oy, 0), part_kind="bearer")
    rows = [5, 4, 3] if style == "dep" else [4, 3]
    n = 0
    for li, nn in enumerate(rows):
        for k in range(nn):
            y = -16.0 + P.COL_R * 2 * 1.04 * (k + 0.5 * li) + 1.4 + (0.0 if style == "dep" else 0.4)
            z = z00 + P.COL_R + li * P.COL_R * 2 * 0.87
            o = obj(f"{tag}_COLUMN_{n:02d}", COL18, c, (ox - 19.0, oy + y, z), 0.0, part_kind="column", length_ft=18.667)
            o.rotation_euler = (0, math.radians(90), 0); n += 1
    out["columns"] = n
    # girders on edge in a rack: axis along Y, spaced 0.75 ft, top flange up
    gx0 = -30.0 if style == "dep" else 12.0          # arrival: rack set east of the crates (a different yard layout)
    ng = 7 if style == "dep" else 5
    bm = bmesh.new()
    zb = max(g(gx0 + ng * 0.8, yy) for yy in (-11, 0, 11)) + 0.5
    for yy in (-11.0, 0.0, 11.0):
        box(bm, gx0 - 0.8, gx0 + ng * 0.8 + 0.6, yy - 0.45, yy + 0.45, min(g(gx0 - 0.8, yy), g(gx0 + ng * 0.8, yy)) - 0.3, zb)
    obj(f"{tag}_BEARERS_GIR", finish(bm, f"{tag}_bear_g", [OAK]), c, (ox, oy, 0), part_kind="bearer")
    for k in range(ng):
        o = obj(f"{tag}_GIRDER_{k:02d}", GIRD, c, (ox + gx0 + k * 0.8, oy, zb + P.GIRDER_D + 0.05), math.radians(90), part_kind="girder")
    out["girders"] = ng
    # connecting pieces standing in a row (repeated joints)
    nc = 8 if style == "dep" else 5
    for k in range(nc):
        x, y = -4.0 - k * 1.25, 5.0
        obj(f"{tag}_CONN_{k:02d}", CONN, c, (ox + x, oy + y, g(x, y) + 0.02), math.radians(rnd.uniform(-8, 8)), part_kind="connecting_piece")
    out["conn"] = nc
    # sash-bar bundles and gutters (dep: many; arr: two)
    bm = bmesh.new(); nb = 4 if style == "dep" else 2
    for b in range(nb):
        bx, by = -18.0, 9.0 + b * 1.6; z = max(g(bx, by), g(bx + 8, by)) + 0.3
        n0 = len(bm.faces)
        for t in (0.6, 7.0): box(bm, bx + t, bx + t + 0.5, by - 0.6, by + 0.6, min(g(bx + t, by), g(bx + t + 0.5, by)) - 0.2, z)
        mark(bm, n0, 3)
        n0 = len(bm.faces); box(bm, bx, bx + 8.0, by - 0.55, by + 0.55, z, z + 1.0); mark(bm, n0, 0)
        n0 = len(bm.faces)
        for t in (0.8, 4.0, 7.2): box(bm, bx + t, bx + t + 0.12, by - 0.58, by + 0.58, z - 0.02, z + 1.03)
        mark(bm, n0, 1)
    if style == "dep":
        for k in range(3):
            z = g(-30, 17) + 0.6 + k * 0.6
            n0 = len(bm.faces); box(bm, -30.0, -6.0, 16.6, 17.4, z, z + 0.55); mark(bm, n0, 2)
        for x in (-28, -18, -8): z = g(x, 17); n0 = len(bm.faces); box(bm, x - 0.4, x + 0.4, 16.0, 18.0, z - 0.2, z + 0.6); mark(bm, n0, 3)
    obj(f"{tag}_BARS_GUTTERS", finish(bm, f"{tag}_bars", [TIMBERP, ROPE, GUTTER, OAK]), c, (ox, oy, 0), part_kind="component_stack")
    # crates (Muse)
    ncr = 0
    for k in range(5 if style == "dep" else 2):
        x, y = (4.0, 8.0 + k * 3.6) if style == "dep" else (4.0, -12.0 + k * 3.6)
        instance(f"{tag}_CRATE_{k}", MC, c, (ox + x, oy + y, g(x, y)), math.radians(90), part_kind="crate", credit="Muse"); ncr += 1
    if style == "dep":
        instance(f"{tag}_CRATE_top", MC, c, (ox + 4.0, oy + 9.5, g(4, 9.5) + CRATE_H), math.radians(92), part_kind="crate", credit="Muse"); ncr += 1
    out["crates"] = ncr
    return out

def wagon(c, tag, x, y, z, rzdeg, load="girders"):
    """four-wheeled timber wagon 16 ft with a draught horse (Grok dismantle trolley, re-used) - loaded"""
    hm = bpy.data.meshes.get("horse_draught") or FG.horse_group_mesh("horse_draught", 2.35, HORSE, rearing=False, rider=False, base=False)
    bm = bmesh.new()
    for sx in (-6.0, 6.0):
        for sy in (-2.6, 2.6): rod(bm, (sx, sy - 0.2, 1.8), (sx, sy + 0.2, 1.8), 1.8, 18)
    box(bm, -8, 8, -2.2, 2.2, 2.6, 3.0); beam(bm, (8, 0, 2.6), (14, 0, 3.2), 0.3, 0.3)
    for sx in (-7.6, 7.6):
        for sy in (-2.1, 2.1): box(bm, sx - 0.15, sx + 0.15, sy - 0.15, sy + 0.15, 3.0, 4.6)   # stakes
    o = obj(f"{tag}_WAGON", finish(bm, f"{tag}_wagon", [OAK]), c, (x, y, z), math.radians(rzdeg), part_kind="wagon", load=load)
    a = math.radians(rzdeg)
    for k in range(2 if load == "girders" else 0):
        g = obj(f"{tag}_WAGON_GIRDER_{k}", GIRD, c, (x + 0.0, y + 0.0, z + 3.0 + P.GIRDER_D + 0.05), a, part_kind="girder", on="wagon")
        g.location.x += P.FT * (-math.sin(a) * (k - 0.5) * 0.9); g.location.y += P.FT * (math.cos(a) * (k - 0.5) * 0.9)
    if load == "columns":
        for k in range(5):
            cc = obj(f"{tag}_WAGON_COL_{k}", COL18, c, (x, y, z + 3.4 + (k // 3) * 0.6), 0.0, part_kind="column", on="wagon")
            cc.rotation_euler = (0, math.radians(90), a)
            off = Vector((-9.3, (k % 3 - 1) * 0.75 + (0.37 if k >= 3 else 0), 0)); off.rotate(Matrix.Rotation(a, 3, 'Z'))
            cc.location.x += P.FT * off.x; cc.location.y += P.FT * off.y
    obj(f"{tag}_HORSE", hm, c, (x + 16.5 * math.cos(a), y + 16.5 * math.sin(a), z), a, part_kind="horse")
    return o

# ======================= DEP: Hyde Park 1852 =======================
DC = coll("DEP_HYDE_PARK_1852", ROOT)
DX, DY = 0.0, 600.0
ground_patch("DEP_GRASS", DC, -1100, 400, 300, 900, flat, GRASS, 25.0)
ground_patch("DEP_YARD", DC, -60, 30, 570, 632, flat, TROD, 3.0, z_off=0.03)
stats_dep = stack(DC, "DEP", DX, DY, flat, "dep")
wagon(DC, "DEP", -14.0, 575.0, 0.0, -2.0, load="columns")                    # wagon south of the stack, horse to the east
man(DC, -8.0, 579.5, 100, k=0); man(DC, -12.5, 581.0, 80, k=2); man(DC, -21.0, 590.0, 90, k=4)
man(DC, 2.5, 596.0, 180, role="clerk")                                         # checker with a tally book at the crate end
man(DC, -21.0, 606.0, 10, k=1); man(DC, -19.0, 601.0, 300, k=3)
man(DC, 7.5, 590.0, 120, k=5)
# the stripped frame beyond (1851 building, glass and floors gone): 4 x 3 bays of tier-1 columns + girders
bm = bmesh.new(); xs = [-150 - 24 * i for i in range(5)]; ys = [560 + 24 * j for j in range(4)]
for x in xs:
    for y in ys:
        P.add_column(bm, 18 + 11.75 / 12, M=Matrix.Translation((x, y, 0)))
        P.add_connecting_piece(bm, M=Matrix.Translation((x, y, 18 + 11.75 / 12)))
zg = 18 + 11.75 / 12 + P.GIRDER_TOP_IN_CP
for j, y in enumerate(ys):
    for i in range(len(xs) - 1):
        if (i, j) in ((3, 0), (2, 3)): continue                                       # two already lowered
        P.add_girder(bm, Matrix.Translation(((xs[i] + xs[i + 1]) / 2, y, zg)))
for i, x in enumerate(xs):
    for j in range(len(ys) - 1):
        if (i, j) in ((4, 1),): continue
        P.add_girder(bm, Matrix.Translation((x, (ys[j] + ys[j + 1]) / 2, zg)) @ Matrix.Rotation(math.radians(90), 4, 'Z'))
obj("DEP_STRIPPED_FRAME", finish(bm, "dep_frame", [PAINT]), DC, part_kind="stripped_frame", note="illustrative fragment of the 1851 frame being taken down")
# elms (the transept elms stayed in the park) + distant Muse elms + a row of round trees
TR.build_elm("DEP_ELM_A", -95, 655, 0, 78, 3.6, 30, 7, BARK, LEAF, DC, cards_per=90)
TR.build_elm("DEP_ELM_B", -120, 520, 0, 70, 3.2, 27, 8, BARK, LEAF, DC, cards_per=90)
for k, (x, y) in enumerate(((-420, 700), (-470, 560), (-520, 640), (-380, 480), (-610, 520), (-650, 720))):
    instance(f"DEP_MUSE_ELM_{k}", ME, DC, (x, y, 0), rnd.uniform(0, 6.28), scale=rnd.uniform(1.1, 1.4), part_kind="elm", credit="Muse")
TM = [TR.round_tree_mesh(f"round_tree_{s}", s, h, BARK, FOLIAGE) for s, h in ((11, 62), (23, 74), (37, 66))]
for k in range(26):
    x = -1050 + k * 40 + rnd.uniform(-10, 10); y = 860 + rnd.uniform(-20, 20)
    obj(f"DEP_TREE_N_{k:02d}", TM[k % 3], DC, (x, y, 0), rnd.uniform(0, 6.3), part_kind="park_tree")
for k in range(26):
    x = -1050 + k * 40 + rnd.uniform(-10, 10); y = 340 + rnd.uniform(-20, 20)
    obj(f"DEP_TREE_S_{k:02d}", TM[k % 3], DC, (x, y, 0), rnd.uniform(0, 6.3), part_kind="park_tree")
for k in range(10):
    obj(f"DEP_TREE_W_{k:02d}", TM[k % 3], DC, (-1080 + rnd.uniform(-20, 20), 360 + k * 55, 0), rnd.uniform(0, 6.3), part_kind="park_tree")
for k, (x, y, r) in enumerate(((40, 640, 200), (34, 556, 160))):
    instance(f"DEP_BENCH_{k}", MB, DC, (x, y, 0), math.radians(r), part_kind="bench", credit="Muse")

# ======================= ARR: Sydenham (Penge Place) 1852 =======================
AC = coll("ARR_SYDENHAM_1852", ROOT)
AX, AY = 0.0, 1600.0
def zarr(x, y):
    """generic slope rising to the east ~1 in 14 with a soft shoulder (the hill site; generic, not surveyed)"""
    u = x - AX; v = y - AY
    return 0.07 * u + 6.0 * math.sin(v / 140.0) * 0.4 + 2.5 * math.sin(u / 90.0 + 0.6) * 0.5
ground_patch("ARR_GRASS", AC, -500, 1400, 1250, 1950, zarr, GRASS, 20.0)
ground_patch("ARR_CLAY", AC, -45, 40, 1572, 1630, zarr, CLAY, 3.0, z_off=0.04)
stats_arr = stack(AC, "ARR", AX, AY, zarr, "arr")
# packing under the bearers on the slope is implicit in their depth; levelling pegs and a line
bm = bmesh.new()
for k in range(9):
    x = -40 + k * 10; y = 1568; z = zarr(x, y); box(bm, x - 0.08, x + 0.08, y - 0.08, y + 0.08, z - 0.3, z + 2.2)
for k in range(8):
    x0 = -40 + k * 10; z0 = zarr(x0, 1568) + 2.0; z1 = zarr(x0 + 10, 1568) + 2.0
    rod(bm, (x0, 1568, z0), (x0 + 10, 1568, z1), 0.012, 4)
obj("ARR_PEGS", finish(bm, "arr_pegs", [DEAL]), AC, part_kind="peg")
# spoil heaps and a contractor's hut
bm = bmesh.new()
for (x, y, r, h) in ((38, 1640, 14, 4.5), (55, 1585, 10, 3.0), (-40, 1650, 12, 3.5)):
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=r, radius2=r * 0.25, depth=h, matrix=Matrix.Translation((x, y, zarr(x, y) + h / 2 - 0.4)))
obj("ARR_SPOIL", finish(bm, "arr_spoil", [CLAY]), AC, part_kind="spoil")
hx, hy = 62.0, 1622.0; hz = zarr(hx, hy)
bm = bmesh.new(); box(bm, hx - 7, hx + 7, hy - 5, hy + 5, hz - 1.5, hz + 8.0)
prism(bm, [(hx - 7.6, hy - 5.6), (hx + 7.6, hy - 5.6), (hx + 7.6, hy + 5.6), (hx - 7.6, hy + 5.6)], hz + 8.0, hz + 8.4)
obj("ARR_HUT", finish(bm, "arr_hut", [BOARD]), AC, part_kind="hut")
wagon(AC, "ARR", -18.0, 1574.0, zarr(-18, 1574) - 0.2, 178.0, load="girders")       # arriving, horse to the west (uphill side away)
man(AC, -14.0, 1579.5, 270, z=zarr(-14, 1579.5), k=1); man(AC, -8.0, 1580.5, 200, z=zarr(-8, 1580.5), k=3)
man(AC, 1.0, 1607.0, 250, z=zarr(1, 1607), k=5); man(AC, -22.0, 1614.0, 330, z=zarr(-22, 1614), k=0)
man(AC, 6.5, 1597.0, 200, z=zarr(6.5, 1597), role="clerk")
TO = [TR.round_tree_mesh(f"oak_{s}", s, h, BARK, FOLIAGE_SY, crown=0.24) for s, h in ((5, 55), (17, 62), (29, 48), (41, 70))]
for k in range(70):
    a = rnd.uniform(-0.9, 0.9); d = rnd.uniform(260, 700)
    x = AX + d * math.cos(a) + 120; y = AY + d * math.sin(a) * 0.9
    if not (-500 < x < 1400 and 1250 < y < 1950): continue
    obj(f"ARR_OAK_{k:02d}", TO[k % 4], AC, (x, y, zarr(x, y) - 0.5), rnd.uniform(0, 6.3), part_kind="oak", note="generic wooded grounds (ILN 5 Jun 1852 sketch)")
for k in range(16):
    x = rnd.uniform(-300, 200); y = rnd.choice((1300, 1900)) + rnd.uniform(-40, 40)
    obj(f"ARR_OAK_EDGE_{k:02d}", TO[k % 4], AC, (x, y, zarr(x, y) - 0.5), rnd.uniform(0, 6.3), part_kind="oak")

# ======================= MAP: two-site schematic locator =======================
MPC = coll("MAP_LOCATOR", ROOT)
MX, MY = 0.0, -400.0; S = 1.2                          # 1.2 ft per mile on the plane
LAT0, LON0 = 51.468, -0.120
def ll(lat, lon): return (MX + (lon - LON0) * 43.1 * S, MY + (lat - LAT0) * 69.0 * S)
PAPER = mat("GT_MapPaper", (0.80, 0.74, 0.60), 0.9, emit=0.35)
INK = mat("GT_MapInk", (0.06, 0.05, 0.04), 0.9)
WATER = mat("GT_MapWater", (0.30, 0.42, 0.52), 0.8)
PARKG = mat("GT_MapPark", (0.40, 0.52, 0.30), 0.9)
RED = mat("GT_MapSite", (0.55, 0.08, 0.05), 0.7)
bm = bmesh.new(); box(bm, MX - 10.6, MX + 10.6, MY - 6.0, MY + 6.0, -0.05, 0.0)
obj("MAP_PAPER", finish(bm, "map_paper", [PAPER]), MPC, part_kind="map")
bm = bmesh.new()
for x0, x1, y0, y1 in ((-10.4, 10.4, 5.75, 5.8), (-10.4, 10.4, -5.8, -5.75), (-10.4, -10.35, -5.8, 5.8), (10.35, 10.4, -5.8, 5.8)):
    box(bm, MX + x0, MX + x1, MY + y0, MY + y1, 0.0, 0.01)
obj("MAP_BORDER", finish(bm, "map_border", [INK]), MPC, part_kind="map")
THAMES = [(51.470, -0.245), (51.488, -0.230), (51.466, -0.213), (51.461, -0.188), (51.482, -0.170), (51.485, -0.150),
          (51.488, -0.127), (51.495, -0.121), (51.501, -0.122), (51.509, -0.117), (51.509, -0.104), (51.508, -0.088),
          (51.505, -0.075), (51.502, -0.052), (51.509, -0.035), (51.495, -0.022), (51.484, -0.010), (51.493, 0.000),
          (51.505, 0.005), (51.505, 0.020)]
pts = [Vector((*ll(a, b), 0.012)) for a, b in THAMES]
bm = bmesh.new(); w = 0.11; L_, R_ = [], []
for i, p in enumerate(pts):                                     # mitred ribbon (no bead joints)
    d0 = (p - pts[i - 1]).normalized() if i else (pts[1] - p).normalized()
    d1 = (pts[i + 1] - p).normalized() if i < len(pts) - 1 else d0
    t = (d0 + d1).normalized(); nrm = Vector((-t.y, t.x, 0)); k = w / max(0.4, nrm.dot(Vector((-d0.y, d0.x, 0))))
    L_.append(bm.verts.new(p + nrm * k)); R_.append(bm.verts.new(p - nrm * k))
for i in range(len(pts) - 1): bm.faces.new([R_[i], R_[i + 1], L_[i + 1], L_[i]])
obj("MAP_THAMES", finish(bm, "map_thames", [WATER]), MPC, part_kind="map", note="schematic river line, approximate")
HP = ll(51.5028, -0.1684); SY = ll(51.4214, -0.0726)
bm = bmesh.new()
a0 = ll(51.5035, -0.188); a1 = ll(51.5125, -0.152); box(bm, a0[0], a1[0], a0[1], a1[1], 0.0, 0.008)       # Hyde Park (approx.)
b0 = ll(51.4170, -0.0800); b1 = ll(51.4250, -0.0640); box(bm, b0[0], b1[0], b0[1], b1[1], 0.0, 0.008)       # the Penge Place grounds (approx.)
obj("MAP_PARKS", finish(bm, "map_parks", [PARKG]), MPC, part_kind="map")
bm = bmesh.new()
for (x, y) in (HP, SY):
    bmesh.ops.create_circle(bm, cap_ends=True, segments=24, radius=0.22, matrix=Matrix.Translation((x, y, 0.02)))
obj("MAP_SITES", finish(bm, "map_sites", [RED]), MPC, part_kind="map")
def label(txt, x, y, size=0.38, align='LEFT', body_mat=INK, name=None):
    cu = bpy.data.curves.new(name or ("lbl_" + txt[:12]), 'FONT'); cu.body = txt; cu.size = size; cu.align_x = align
    o = bpy.data.objects.new(name or ("MAP_LABEL_" + txt[:16]), cu); o.location = (P.FT * x, P.FT * y, P.FT * 0.03)
    cu.materials.append(body_mat); o.scale = (P.FT, P.FT, P.FT); MPC.objects.link(o); o["part_kind"] = "map_label"; return o
label("HYDE PARK", HP[0] - 0.4, HP[1] + 0.5, 0.55, 'RIGHT')
label("1851 building, taken down 1852", HP[0] - 0.4, HP[1] - 0.05, 0.36, 'RIGHT')
label("SYDENHAM", SY[0] + 0.4, SY[1] + 0.15, 0.55)
label("Penge Place, re-erected 1852-54", SY[0] + 0.4, SY[1] - 0.42, 0.36)
label("Thames", ll(51.500, -0.060)[0], ll(51.500, -0.060)[1] + 0.3, 0.42)
label("TWO SITES  -  schematic locator, no route shown", MX - 10.0, MY + 5.0, 0.50)
label("about 7 miles apart in a straight line", MX - 10.0, MY + 4.4, 0.36)
bm = bmesh.new(); nx_, ny_ = MX + 9.0, MY + 3.4
prism(bm, [(nx_ - 0.25, ny_ - 0.6), (nx_, ny_ + 0.7), (nx_ + 0.25, ny_ - 0.6), (nx_, ny_ - 0.3)], 0.0, 0.015)
sx0 = MX + 6.0; box(bm, sx0, sx0 + 2 * S, MY - 5.2, MY - 5.1, 0.0, 0.015)
for t in (0, 1, 2): box(bm, sx0 + t * S - 0.03, sx0 + t * S + 0.03, MY - 5.25, MY - 4.95, 0.0, 0.015)
obj("MAP_NORTH_SCALE", finish(bm, "map_ns", [INK]), MPC, part_kind="map")
label("N", nx_, ny_ + 0.85, 0.36, 'CENTER'); label("0        1        2 miles", sx0 - 0.1, MY - 4.8, 0.24)

# ---------------- world + cameras ----------------
world(sun_elev=34, sun_rot=215, strength=0.35, sun_energy=3.0, exposure=-0.4)
cams = cameras(os.path.join(ROOTDIR, "route", "camera_route.json"), ROOT,
               zfun=lambda x, y: zarr(x, y) if 1250 < y < 1950 else 0.0)
info.update({"stack_dep": stats_dep, "stack_arr": stats_arr, "staff": len(staff), "cams": [c.name for c in cams],
             "objects": len(bpy.data.objects)})
t = bpy.data.texts.new("grok_states"); t.write(json.dumps({"KJ_exploded": {"hide": ["K_GIRDER_N_oakkeys", "K_KEYS_OAK_N"]}}))   # m02: declutter
sc["grok_move"] = json.dumps(info)
print("MOVE_INFO", json.dumps(info), flush=True)
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True)
print("SAVED", OUT)
