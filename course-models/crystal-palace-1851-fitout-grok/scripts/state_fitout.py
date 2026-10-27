# HP-FITOUT (CP018-CP020): the building in the fit-out months, Jan-Apr 1851. Exec'd in build_transept.py (--state fitout).
# DEPARTURES FT01-FT14.
exec(open(os.path.join(HERE, "state_common.py")).read())
FIT = coll("FITOUT_F01", ROOT)
info = {}; info["doors_open"] = open_south_doors()

# ---- FT02: Osler's crystal fountain was erected only in April 1851 -> not yet here ----
for ob in list(C["FOUNTAIN"].objects) if "FOUNTAIN" in C else list(FC.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
info["fountain"] = "removed (FT02)"

# ---- FT03-FT05: paint progress (Owen Jones scheme going on top-down over a pale priming coat) ----
PRIMER = mat_principled("FT_PrimingCoat", (0.58, 0.55, 0.49), 0.75)
def half_material(src, axis):
    """copy of an OJ material: above the per-object cut ('paint_cut', metres, object space) the OJ colours, below primer."""
    m = src.copy(); m.name = src.name + "_HALF_" + axis
    nt = m.node_tree; n = nt.nodes; l = nt.links; b = n["Principled BSDF"]
    lk = b.inputs["Base Color"].links[0]; oj = lk.from_socket; nt.links.remove(lk)
    tc = n.new("ShaderNodeTexCoord"); sp = n.new("ShaderNodeSeparateXYZ"); l.new(tc.outputs["Object"], sp.inputs[0])
    at = n.new("ShaderNodeAttribute"); at.attribute_type = 'OBJECT'; at.attribute_name = "paint_cut"
    gt = n.new("ShaderNodeMath"); gt.operation = 'GREATER_THAN'
    l.new(sp.outputs["Z" if axis == "z" else "X"], gt.inputs[0]); l.new(at.outputs["Fac"], gt.inputs[1])
    mx = n.new("ShaderNodeMix"); mx.data_type = 'RGBA'; l.new(gt.outputs[0], mx.inputs["Factor"])
    mx.inputs["A"].default_value = (*PRIMER.diffuse_color[:3], 1); l.new(oj, mx.inputs["B"]); l.new(mx.outputs["Result"], b.inputs["Base Color"])
    # a wet sheen on the fresh coat
    return m
HALF_COL = half_material(IRON_COL, "z")
def set_mat(ob, m):
    for sl in ob.material_slots: sl.link = 'OBJECT'; sl.material = m
def col_xy(ob): return round(ob.location.x / FT), round(ob.location.y / FT)
FRAC = {-36: 0.14, -60: 0.40, -84: 0.66, -108: 0.86}   # painted fraction (from the top) of the transept-line columns
cuts = {}; work = []
for ob in C["COLUMNS"].objects:
    x, y = col_xy(ob); h = ob.dimensions.z / FT; ax = abs(x)
    if x > 61 or (ax <= 61 and y >= 30): cut = 0.0
    elif ax == 36 and y in FRAC: cut = round(h * (1 - FRAC[y]), 1)
    else: cut = None
    cuts[(x, y)] = cut if cut is not None else 999.0
    if cut is None: set_mat(ob, PRIMER); ob["paint_state"] = "primer"
    elif cut == 0: ob["paint_state"] = "painted"
    else:
        set_mat(ob, HALF_COL); ob["paint_cut"] = ft(cut); ob["paint_cut_ft"] = cut; ob["paint_state"] = "half"; work.append((x, y, cut, h))
for cname in ("GIRDERS",):
    for ob in C[cname].objects:
        x, y = col_xy(ob); top = ob.location.z / FT
        if x > 61 or y > -30: ob["paint_state"] = "painted"; continue
        ends = [(x, y - 12), (x, y + 12)] if abs(math.cos(ob.rotation_euler.z)) < 0.5 else [(x - 12, y), (x + 12, y)]
        c_ = max(cuts.get(e, 999.0) for e in ends)
        if top - 1.5 > c_: ob["paint_state"] = "painted"
        else: set_mat(ob, PRIMER); ob["paint_state"] = "primer"
for cname in ("TRUSSES", "GALLERY_TRUSSES"):
    if cname in C:
        for ob in C[cname].objects:
            if ob.location.y / FT < -132 or ob.location.x / FT < -61: set_mat(ob, PRIMER); ob["paint_state"] = "primer"
info["paint"] = {s: sum(1 for o in bpy.data.objects if o.get("paint_state") == s) for s in ("painted", "half", "primer")}

# ---- FT04: ladders, cradles and painters at the paint front ----
POTS = [M_("paint_blue", OJ_BLUE, 0.3), M_("paint_red", OJ_RED, 0.3), M_("paint_yellow", OJ_YELLOW, 0.3), M_("paint_white", OJ_WHITE, 0.3)]
def mesh_ladder(L):
    k = Kit([TIMBER]); w = 0.8
    for s in (-w, w): k.box(0, s - 0.1, s + 0.1, -0.08, 0.08, 0, L)
    z = 0.8
    while z < L - 0.3: k.cyl(0, (-w, 0, z), (w, 0, z), 0.07, 6); z += 0.9
    return k.done(f"ladder_{L:.0f}")
def mesh_pot(i):
    k = Kit([IRON_DK, POTS[i]]); k.cyl(0, (0, 0, 0), (0, 0, 0.55), 0.3, 12); k.cyl(1, (0, 0, 0.55), (0, 0, 0.57), 0.28, 12)
    k.bar(0, (-0.3, 0, 0.55), (0, 0, 0.9), 0.04); k.bar(0, (0, 0, 0.9), (0.3, 0, 0.55), 0.04)
    return k.done(f"paint_pot_{i}")
POT = [mesh_pot(i) for i in range(4)]
PAINTER = pmesh("man", [WK["smock"], WK["trou_dk"], SKIN2[0], WK["paper_cap"], WK["shirt"]], {"hat": "cap", "frock": True}, "painter")
PAINTER2 = pmesh("man", [WK["smock"], WK["moleskin"], SKIN2[1], WK["cap_dk"], WK["shirt"]], {"hat": "cap"}, "painter2")
def painter(nm, x, y, z, face_x, j):
    rz = heading_rz(face_x, 0)
    person(f"PAINTER_{nm}", (PAINTER, PAINTER2)[j % 2], x, y, z, rz, trade="painter")
    arm_reach(f"PAINTER_{nm}_ARM", x, y, z, rz, up=0.8 + 0.2 * (j % 2), side=(0.66, -0.66)[j % 2])
def mesh_cradle(Lr):
    """painter's cradle: 8 x 2 ft stage, 3 ft guard rail, ropes up Lr ft to the girder (local, y along the stage)"""
    k = Kit([TIMBER, ROPE])
    k.box(0, -1.0, 1.0, -4.0, 4.0, -0.15, 0)
    for sy in (-4.0, 4.0):
        k.box(0, -1.0, 1.0, sy - 0.1, sy + 0.1, 0, 3.2)
        k.bar(1, (0, sy * 0.95, 3.2), (0, sy * 0.95, Lr), 0.08)
    k.box(0, -1.05, -0.95, -4.0, 4.0, 3.0, 3.2); k.box(0, -1.05, -0.95, -4.0, 4.0, 1.5, 1.65)
    return k.done(f"cradle_{Lr:.0f}")
nlad = ncrad = npaint = 0
for (x, y, cut, h) in sorted(work):
    sx = 1 if x > 0 else -1; inside = x - sx * 1.6    # on the void side of the column line
    face = sx                                           # painter faces the column (+x for the east line)
    zf = max(0.0, cut - 4.6)
    if zf < 0.6:   # base: a painter standing on the floor, kettle at his feet
        painter(f"{x:+d}_{y:+d}", inside - sx * 0.4, y + 0.6, 0, face, npaint); npaint += 1
        prop(f"POT_{x:+d}_{y:+d}", POT[npaint % 4], inside - sx * 0.6, y - 1.6, 0)
    elif zf <= 15.0:   # ladder leaning on the column face
        L = zf + 7.0; base = L * 0.24
        lad = prop(f"LADDER_{x:+d}_{y:+d}", mesh_ladder(L), x - sx * (1.0 + base), y - 1.2, 0, 0, part_kind="ladder")
        lad.rotation_euler = (0, sx * math.atan2(base, L), 0); nlad += 1
        pz = zf; px = x - sx * (1.0 + base * (1 - pz / L)) - sx * 0.95
        painter(f"{x:+d}_{y:+d}", px, y - 1.2, pz, face, npaint); npaint += 1
        prop(f"POT_{x:+d}_{y:+d}", POT[npaint % 4], px + sx * 0.4, y - 0.4, pz + 0.9)   # hung on the ladder
        for jj in range(2): worker_ob = person(f"FOOT_{x:+d}_{y:+d}_{jj}", worker_mesh(jj + 2), x - sx * (3.5 + base + 2 * jj), y - 3.5 - jj, 0, heading_rz(sx, 0.3), trade="labourer")
    else:   # cradle slung from the girder above
        gt = min(g for g in GIRDER_TOP if g > zf + 7.0)
        cr = prop(f"CRADLE_{x:+d}_{y:+d}", mesh_cradle(gt - 3.0 - zf), inside - sx * 0.6, y, zf, 0, part_kind="cradle"); ncrad += 1
        for jj, dy in enumerate((-1.8, 1.9)):
            painter(f"{x:+d}_{y:+d}_{jj}", inside - sx * 0.2, y + dy, zf, face, npaint + jj)
            prop(f"POT_{x:+d}_{y:+d}_{jj}", POT[(npaint + jj) % 4], inside - sx * 1.1, y + dy * 1.6, zf)
        npaint += 2
info["painters"] = npaint; info["ladders"] = nlad; info["cradles"] = ncrad
# the paint shop on the floor: trestle table, kegs of colour, a man grinding and mixing
TABLE = Kit([TIMBER, TIMBER_DK])
TABLE.box(0, -1.5, 1.5, -5, 5, 2.6, 2.8)
for sy in (-4, 4):
    for sx in (-1.2, 1.2): TABLE.bar(1, (sx, sy - 0.8, 0), (sx * 0.8, sy, 2.6), 0.18)
prop("PAINT_TABLE", TABLE.done("paint_table"), 18, -128, 0, 0, part_kind="paint_shop")
for j in range(7): prop(f"PAINT_TABLE_POT_{j}", POT[j % 4], 18 + (j % 2 - 0.5) * 1.6, -132 + j * 1.3, 2.8)
KEG = Kit([TIMBER_DK, IRON_DK]); KEG.cyl(0, (0, 0, 0), (0, 0, 2.2), 0.95, 14)
for z in (0.3, 1.9): KEG.cyl(1, (0, 0, z), (0, 0, z + 0.12), 0.98, 14)
KEG = KEG.done("keg")
for j, (kx, ky) in enumerate(((22.5, -122), (22.8, -124.3), (21.0, -136.5), (23.0, -134.5), (14.0, -137))):
    prop(f"PAINT_KEG_{j}", KEG, kx, ky, 0, j)
painter("mixer", 15.6, -129.5, 0, 1, 1); person("PAINT_FOREMAN", worker_mesh(3), 21.5, -118, 0, heading_rz(-0.5, -1), trade="foreman")

# ---- FT06-FT08: cases and crates arriving through the south doors ----
GRAVEL = M_("gravel_apron", (0.50, 0.46, 0.40), 0.95)
slab("FT_APRON", -60, 60, -300, -204.3, 0.02, 0.3, GRAVEL, PROPS, part_kind="ground")
def mesh_dray():
    """brewer's / carrier's four-wheel dray: 13 x 6 ft deck 4 ft up, 3 ft fore and 4.5 ft hind wheels, shafts forward (+x)"""
    k = Kit([TIMBER_DK, IRON_DK, TIMBER])
    k.box(0, -7.0, 6.0, -3.0, 3.0, 3.7, 4.0)
    for sy in (-3.0, 3.0): k.box(0, -7.0, 6.0, sy - 0.12, sy + 0.12, 4.0, 4.6)
    for sy in (-2.9, 2.9):
        k.wheel(1, (-4.5, sy + 0.3 * (1 if sy > 0 else -1), 2.25), "y", 2.25, w=0.35, rim=0.22, spokes=12)
        k.wheel(1, (3.8, sy + 0.3 * (1 if sy > 0 else -1), 1.5), "y", 1.5, w=0.3, rim=0.2, spokes=10)
    k.bar(1, (-4.5, -3.3, 2.25), (-4.5, 3.3, 2.25), 0.25); k.bar(1, (3.8, -3.3, 1.5), (3.8, 3.3, 1.5), 0.22)
    for sy in (-1.3, 1.3): k.bar(2, (6.0, sy, 3.6), (14.5, sy * 0.8, 3.7), 0.25)
    return k.done("dray")
DRAY = mesh_dray()
HORSE_B = mat_principled("FT_DraughtBay", (0.14, 0.08, 0.05), 0.7); HORSE_G = mat_principled("FT_DraughtGrey", (0.42, 0.40, 0.37), 0.7)
HORSE = [FG.horse_group_mesh("ft_horse_bay", 2.35, HORSE_B, rearing=False, rider=False, base=False),
         FG.horse_group_mesh("ft_horse_grey", 2.35, HORSE_G, rearing=False, rider=False, base=False)]
def dray(nm, x, y, deg, loads, horse=0):
    a = math.radians(deg); ca, sa = math.cos(a), math.sin(a)
    prop(f"DRAY_{nm}", DRAY, x, y, 0, a, part_kind="dray")
    prop(f"DRAY_{nm}_HORSE", HORSE[horse], x + 11.5 * ca, y + 11.5 * sa, 0, a, part_kind="horse")
    for j, (lx, ly, lz, rr) in enumerate(loads):
        inst(CRATE, f"DRAY_{nm}_CRATE_{j}", x + lx * ca - ly * sa, y + lx * sa + ly * ca, 4.0 + lz, a + rr, SRND.uniform(0.95, 1.2), part_kind="crate")
if CRATE:
    dray("door", -2, -219, -90, [(-1, -1.5, 0, 0), (-1, 1.5, 0, 0), (2.5, 0, 0, 1.57), (-1, 0, 2.6, 0.1)], 0)  # tail to the door, horse south
    dray("wait", 30, -262, -120, [(-3, -1.4, 0, 0), (-3, 1.4, 0, 0), (0.8, 0, 0, 0), (-3, 0, 2.5, 0.05)], 1)
    person("CARTER_door", worker_mesh(4), 4.5, -232, 0, heading_rz(-1, 0.4), trade="carter")
    person("CARTER_wait", worker_mesh(0), 37, -270, 0, heading_rz(-0.6, 0.6), trade="carter")
    # unloading at the tail: two porters easing a crate down a skid onto a truck at the threshold
    SKID = Kit([TIMBER_DK]); [SKID.bar(0, (sx, 0, 4.0), (sx, 7.0, 0.1), 0.35, 0.3) for sx in (-1.0, 1.0)]
    prop("DRAY_door_SKIDS", SKID.done("skids"), -2, -213.5, 0, 0, part_kind="skids")
    inst(CRATE, "SKID_CRATE", -2, -209.8, 1.9, 1.57, 1.0, part_kind="crate"); bpy.data.objects["SKID_CRATE"].rotation_euler = (math.radians(-29), 0, 1.57)
    for j, sx in enumerate((-4.6, 2.6)): person(f"PORTER_skid_{j}", worker_mesh(j), sx, -208.5, 0, heading_rz(-sx, -1), trade="porter")
    # trucks coming up the transept with crates and an exhibitor's case
    trucks = [(-1, -192, 0, 1), (9, -168, 8, 2), (-12, -146, -25, 1), (6, -112, 4, "case")]
    for j, (tx, ty, deg, load) in enumerate(trucks):
        a = math.radians(deg)
        prop(f"TRUCK_{j}", TROLLEY, tx, ty, 0, a, part_kind="trolley")
        if load == "case":
            inst(CASE_M, f"TRUCK_{j}_CASE", tx, ty, 1.18, a + math.pi / 2, 1.0, part_kind="case_arriving")
        else:
            for m in range(load): inst(CRATE, f"TRUCK_{j}_CRATE_{m}", tx, ty, 1.18 + m * CRATE_H, a + math.pi / 2 + 0.08 * m, 1.0 + 0.1 * m, part_kind="crate")
        hx, hy = tx - 5.2 * math.sin(-a), ty - 5.2 * math.cos(a)
        person(f"PORTER_truck_{j}", worker_mesh(j + 1), hx, hy, 0, heading_rz(-math.sin(a), math.cos(a)), trade="porter")
        arm_reach(f"PORTER_truck_{j}_ARM", hx, hy, 0, heading_rz(-math.sin(a), math.cos(a)), up=-0.6, side=0.66, tool=None, mat=[WK["fustian"], WK["cord"], WK["moleskin"]][j % 3])
        if j % 2 == 0: person(f"PORTER_truck_{j}_b", worker_mesh(j + 3), tx + 2.4 * math.cos(a), ty + 2.4 * math.sin(a) + 2.0, 0, heading_rz(-math.sin(a), math.cos(a)), trade="porter")
    # stacks waiting under the east gallery and a case being unpacked
    stack = [(44, -196, 0, 0.0), (44, -196, 1, 0.05), (48.5, -196, 0, 0.0), (52.5, -195, 0, 0.1), (48.5, -196, 1, -0.05), (44, -196, 2, 0.0),
             (54.5, -186, 0, 1.57), (54.5, -186, 1, 1.6), (-46, -194, 0, 0), (-50.5, -194, 0, 0), (-46, -194, 1, 0.04), (-55, -186, 0, 1.57)]
    for j, (sx_, sy_, lev, rr) in enumerate(stack):
        inst(CRATE, f"STACK_{j}", sx_, sy_, lev * CRATE_H * 1.05, rr, 1.05, part_kind="crate")
    inst(CRATE_OPEN, "UNPACK_CRATE", 46, -150, 0, 1.57, 1.1, part_kind="crate_open")
    LID = Kit([TIMBER]); [LID.box(0, kk * 0.52, kk * 0.52 + 0.5, 0, 2.6, 0, 0.08) for kk in range(8)]
    lid = prop("UNPACK_LID", LID.done("lid"), 50.5, -153, 0.3, 0.2); lid.rotation_euler = (math.radians(75), 0, 0.2)
    STRAW = M_("straw", (0.70, 0.58, 0.30), 0.95); sbm = bmesh.new()
    for kk in range(9): bmesh.ops.create_icosphere(sbm, subdivisions=1, radius=ft(SRND.uniform(0.6, 1.1)), matrix=Matrix.Translation((ft(SRND.uniform(-3, 3)), ft(SRND.uniform(-3, 3)), 0)))
    for v in sbm.verts: v.co.z = max(0.0, v.co.z * 0.45)
    prop("UNPACK_STRAW", finish(sbm, "straw", STRAW), 41.5, -146, 0, 0, part_kind="straw")
    inst(CASE_M, "UNPACK_CASE", 42, -156, 0, 0.0, 1.0, part_kind="case_unpacked")
    for j, (px_, py_, hx_) in enumerate(((44.0, -152.5, 1), (40.0, -159.5, 0.3), (49.5, -147, -1))):
        person(f"UNPACK_{j}", worker_mesh(j + 5), px_, py_, 0, heading_rz(hx_, 0.4), trade="porter")
    person("EXHIBITOR_0", pmesh("man", [M_("coat_black", (0.03, 0.03, 0.035)), M_("trou_grey", (0.25, 0.24, 0.22)), SKIN2[0], M_("hat_black", (0.02, 0.02, 0.02)), WK["shirt"]], {"hat": "top", "frock": True, "cravat": True}, "exhibitor"), 39.0, -150.5, 0, heading_rz(1, -0.4), trade="exhibitor")

# ---- FT09-FT12: the floor: boards still going down in the east nave; sprinkling and the sweeping machine ----
RX0, RX1, RY0, RY1 = 84.0, 132.0, -36.0, 36.0          # unboarded patch (east nave, crossing side of the stair bays)
fb = bpy.data.objects["FLOOR_BOARDS"]; bpy.data.objects.remove(fb, do_unlink=True)
for nm, (x0, x1, y0, y1) in {"W": (-X_ARM - 12, RX0, -Y_HALF, Y_HALF), "E": (RX1, X_ARM + 12, -Y_HALF, Y_HALF),
                             "S": (RX0, RX1, -Y_HALF, RY0), "N": (RX0, RX1, RY1, Y_HALF)}.items():
    slab(f"FLOOR_BOARDS_{nm}", x0, x1, y0, y1, 0.002 / FT, 0.5, FLOORM, C["FLOOR"], part_kind="floor_ground")
gp = bpy.data.objects["GROUND_PARK"]; bpy.data.objects.remove(gp, do_unlink=True)
bm = bmesh.new()
for (x0, x1, y0, y1) in ((-9000, RX0, -9000, 9000), (RX1, 9000, -9000, 9000), (RX0, RX1, -9000, RY0), (RX0, RX1, RY1, 9000)):
    bm_box(bm, ft(x0), ft(x1), ft(y0), ft(y1), -0.30, -0.02)
new_obj("GROUND_PARK", finish(bm, "ground", GRASS), C["GROUND"], props={"part_kind": "ground"})
EARTH = M_("earth_levelled", (0.30, 0.24, 0.18), 0.95)
slab("FT_EARTH_UNDERFLOOR", RX0, RX1, RY0, RY1, -0.40 / FT, 0.4, EARTH, FIT, part_kind="ground_underfloor")
FB = muse_prop("hp-floor-boards", lambda n: n.startswith(("Board", "Joist", "Sleeper")), (0.0, 0.0, 0.0), "MUSE_FloorBoards_by_Muse")
FBJ = muse_prop("hp-floor-boards", lambda n: n.startswith(("Joist", "Sleeper")), (0.0, 0.0, 0.0), "MUSE_FloorJoists_by_Muse")
ZTILE = -0.546 / FT; tiles = 0
if FB:
    for i in range(3):            # 16 ft tiles along x: first boarded, the other two joists and sleepers only
        for j in range(6):        # 12 ft along y
            inst(FB if i == 0 else FBJ, f"FLOORTILE_{i}_{j}", RX0 + 8 + 16 * i, RY0 + 6 + 12 * j, ZTILE, 0.0, 1.0, part_kind="floor_tile"); tiles += 1
info["floor_tiles"] = tiles
# loose boards being laid on the next tile (9 x 1.5 in, 1/2 in gaps; Paxton 1850), and the stack on trestles
BRD = Kit([TIMBER]); n_b = 0; yb = RY0 + 0.1
while yb < -11.0:
    BRD.box(0, RX0 + 16, RX0 + 32, yb, yb + 0.75, -0.125, 0.0); yb += 0.75 + 0.5 / 12; n_b += 1
prop("BOARDS_LAID_LOOSE", BRD.done("boards_laid"), 0, 0, 0, 0, part_kind="floor_boards_new")
ST = Kit([TIMBER, TIMBER_DK])
for lev in range(9):
    for kk in range(6): ST.box(0, 0, 16, kk * 0.8, kk * 0.8 + 0.75, 2.6 + lev * 0.13, 2.6 + lev * 0.13 + 0.125)
for sx in (2, 14):
    for sy in (-0.3, 5.1): ST.bar(1, (sx - 0.7, sy, 0), (sx, sy, 2.6), 0.2)
    ST.box(1, sx - 0.15, sx + 0.15, -0.4, 5.2, 2.4, 2.6)
prop("BOARD_STACK", ST.done("board_stack"), RX0 + 22, 14, 0, 0, part_kind="board_stack")
for j, (kx, ky) in enumerate(((RX0 + 26, -14.2), (RX0 + 20, -15.2), (RX0 + 30.5, -13.6))):
    prop(f"LAYER_{j}", KNEEL, kx, ky, 0, heading_rz(0, -1), part_kind="figure", trade="carpenter")
person("CARRY_0", worker_mesh(6), RX0 + 24, -6, 0, heading_rz(0, -1), trade="carpenter")
BOARD1 = Kit([TIMBER]); BOARD1.box(0, -8, 8, -0.375, 0.375, 0, 0.125)
b1 = prop("BOARD_CARRIED", BOARD1.done("board_carried"), RX0 + 24.6, -6.2, 4.9, 0.3); b1.rotation_euler = (0, 0.05, 0.3)
# FT11: Paxton's water hand-engine and sweeping machine (Society of Arts lecture, 13 Nov 1850): a light
# wheeled frame of many brooms drawn by a shaft, following the sprinkler. Shown on trial on the boarded nave.
def mesh_sweeper():
    k = Kit([TIMBER_DK, IRON_DK, M_("bristle", (0.20, 0.15, 0.10), 0.95)])
    k.box(0, -2.0, 2.0, -4.2, 4.2, 1.5, 1.75)                         # frame (machine runs along +x)
    for sx in (-1.9, 1.9): k.box(0, sx - 0.1, sx + 0.1, -4.2, 4.2, 1.0, 1.75)
    for r_, sx in enumerate((-1.2, 0.0, 1.2)):                        # three staggered rows of brooms
        for kk in range(7):
            yy = -3.6 + kk * 1.2 + (0.6 if r_ == 1 else 0)
            if abs(yy) > 3.9: continue
            k.box(0, sx - 0.25, sx + 0.25, yy - 0.5, yy + 0.5, 0.55, 0.8); k.box(2, sx - 0.2, sx + 0.2, yy - 0.45, yy + 0.45, 0.0, 0.55)
            k.bar(0, (sx, yy, 0.8), (sx, yy, 1.5), 0.12)
    for sy in (-4.5, 4.5):
        for sx in (-1.6, 1.6): k.wheel(1, (sx, sy, 0.9), "y", 0.9, w=0.12, rim=0.1, spokes=6)
    for sy in (-0.8, 0.8): k.bar(0, (2.0, sy, 1.6), (8.5, sy * 0.6, 3.1), 0.18)    # the shaft
    k.bar(0, (8.5, -0.9, 3.1), (8.5, 0.9, 3.1), 0.16)
    return k.done("sweeper")
def mesh_engine():
    k = Kit([TIMBER_DK, IRON_DK, M_("copper", (0.55, 0.30, 0.15), 0.35, 1.0)])
    k.cyl(0, (-1.6, 0, 2.3), (1.6, 0, 2.3), 1.25, 16)                 # water cistern on wheels
    for sy in (-1.5, 1.5): k.wheel(1, (0, sy, 1.5), "y", 1.5, w=0.18, rim=0.14, spokes=8)
    k.bar(1, (0, -1.6, 1.5), (0, 1.6, 1.5), 0.15)
    k.cyl(2, (0, 0, 3.5), (0, 0, 4.5), 0.25, 10)                      # pump barrel
    k.bar(0, (-2.2, 0, 4.6), (2.2, 0, 4.0), 0.12)                     # pump brake
    for sy in (-0.7, 0.7): k.bar(0, (-1.6, sy, 1.6), (-5.0, sy * 0.6, 2.8), 0.15)   # handles to pull
    k.bar(2, (1.6, 0.6, 2.4), (5.0, 2.5, 0.8), 0.12); k.bar(2, (5.0, 2.5, 0.8), (6.2, 3.0, 2.9), 0.1)   # hose to the branch pipe
    k.cyl(2, (6.2, 3.0, 2.9), (6.6, 3.2, 3.3), 0.18, 8)
    return k.done("hand_engine")
WET = M_("floor_wet", (0.22, 0.17, 0.12), 0.18)
prop("WET_STRIP", finish((lambda b: (bm_box(b, ft(46), ft(80), ft(2.0), ft(14.0), ft(0.005), ft(0.012)), b)[1])(bmesh.new()), "wet", WET), 0, 0, 0, 0, part_kind="wet_floor")
prop("HAND_ENGINE", mesh_engine(), 74.5, 8.0, 0, math.pi, part_kind="hand_engine", source="Paxton, Society of Arts lecture Nov 1850")
person("ENGINE_PUMP", worker_mesh(7), 77.0, 9.6, 0, heading_rz(0, -1), trade="labourer")
arm_reach("ENGINE_PUMP_ARM", 77.0, 9.6, 0, heading_rz(0, -1), up=0.2, side=0.66, tool=None, mat=WK["moleskin"])
person("ENGINE_BRANCH", worker_mesh(8), 69.0, 12.8, 0, heading_rz(1, -0.6), trade="labourer")
person("ENGINE_PULL", worker_mesh(9), 80.5, 7.2, 0, heading_rz(1, 0), trade="labourer")
prop("SWEEPER", mesh_sweeper(), 55.0, 8.0, 0, 0.0, part_kind="sweeping_machine", source="Paxton, Society of Arts lecture Nov 1850 (planned)")
person("SWEEPER_PULL", worker_mesh(10), 64.2, 8.0, 0, heading_rz(1, 0), trade="labourer")
arm_reach("SWEEPER_PULL_ARM", 64.2, 8.0, 0, heading_rz(1, 0), up=-0.5, side=-0.66, tool=None, mat=WK["cord"])
DUST = M_("dust_line", (0.45, 0.40, 0.33), 0.95)
prop("DUST_WINDROW", finish((lambda b: (bm_box(b, ft(52.6), ft(53.0), ft(3.6), ft(12.4), 0, ft(0.06)), b)[1])(bmesh.new()), "dust", DUST), 0, 0, 0, 0)
info["floor"] = {"unboarded_patch_ft": [RX0, RX1, RY0, RY1], "loose_boards": n_b}
STATE_INFO = info
print("FITOUT", info, flush=True)
