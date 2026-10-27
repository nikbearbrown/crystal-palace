# HP51 daily life (CP026-CP028): a shilling day, summer 1851. Exec'd in build_transept.py (--state hp51) after dressing.py.
# DEPARTURES FT20-FT29.
exec(open(os.path.join(HERE, "state_common.py")).read())
info = {}; info["doors_open"] = open_south_doors()
POLICE = pmesh("man", [M_("police_blue", (0.03, 0.04, 0.10)), M_("police_trou", (0.04, 0.04, 0.06)), SKIN2[0], M_("police_hat", (0.02, 0.02, 0.02)), WK["brass"]],
               {"hat": "top", "frock": True, "belt": True}, "policeman")
ATTEND = pmesh("man", [WK["green"], WK["trou_dk"], SKIN2[1], WK["cap_dk"], WK["brass"]], {"hat": "low", "frock": True}, "attendant")

# ---- FT21: the shilling-day crowd: re-dress most of the dressing.py crowd as working people ----
wc = {"man": [], "woman": [], "girl": [], "boy": []}
smock = M_("smock_frock", (0.62, 0.60, 0.50)); fust = [WK["fustian"], WK["cord"], WK["moleskin"], WK["blue"], smock, M_("velveteen", (0.18, 0.13, 0.08))]
shawls = [M_("shawl_red", (0.40, 0.08, 0.06)), M_("shawl_brown", (0.28, 0.18, 0.10)), M_("shawl_check", (0.30, 0.30, 0.22)), M_("shawl_blue", (0.12, 0.14, 0.24))]
cotton = [M_("print_lilac", (0.42, 0.36, 0.44)), M_("print_blue", (0.25, 0.30, 0.42)), M_("print_brown", (0.36, 0.26, 0.18)),
          M_("print_grey", (0.40, 0.39, 0.36)), M_("print_pink", (0.55, 0.38, 0.36)), M_("stuff_black", (0.06, 0.05, 0.05))]
bonnet = [M_("bonnet_straw2", (0.62, 0.52, 0.32)), M_("bonnet_black", (0.05, 0.05, 0.05)), M_("cap_white", (0.80, 0.78, 0.72))]
for j in range(12):
    st = {"hat": ("cap", "low", "cap", "low", "top", "cap")[j % 6], "frock": j % 6 == 4 or j % 4 == 1}
    wc["man"].append(pmesh("man", [fust[j % 6], [WK["trou_dk"], WK["trou_fawn"], WK["cord"]][j % 3], SKIN2[j % 2], [WK["cap_dk"], M_("hat_brown", (0.12, 0.09, 0.06))][j % 2], WK["shirt"]], st, f"wc_man_{j}"))
for j in range(10):
    st = {"skirt_w": (0.62, 0.7, 0.66, 0.78, 0.72)[j % 5], "shawl": j % 3 != 2}
    wc["woman"].append(pmesh("woman", [cotton[j % 6], cotton[(j + 3) % 6], SKIN2[j % 2], bonnet[j % 3], shawls[j % 4]], st, f"wc_woman_{j}"))
for j in range(3):
    wc["girl"].append(pmesh("girl", [cotton[(j * 2) % 6], cotton[j + 1], SKIN2[0], bonnet[0], shawls[j]], {"skirt_w": 0.7, "shawl": j == 1}, f"wc_girl_{j}"))
    wc["boy"].append(pmesh("boy", [fust[j], WK["cord"], SKIN2[j % 2], WK["cap_dk"], WK["shirt"]], {"hat": "cap"}, f"wc_boy_{j}"))
swapped = 0; total = 0
for ob in list(bpy.data.objects):
    if ob.get("part_kind") == "figure" and ob.name.startswith("CROWD_"):
        total += 1; kd = ob.get("person", "man")
        if kd in wc and SRND.random() < 0.78:
            ob.data = SRND.choice(wc[kd]); ob["dress"] = "working"; swapped += 1
            if kd == "woman": ob.scale.x *= 0.95
info["crowd_redressed"] = [swapped, total]

# ---- FT22-FT24: turnstiles and money-takers at the south entrance ----
TS = Kit([IRON_DK, M_("brass_ts", (0.70, 0.52, 0.22), 0.3, 1.0)])
TS.cyl(0, (0, 0, 0), (0, 0, 3.2), 0.28, 12); TS.cyl(1, (0, 0, 3.2), (0, 0, 3.5), 0.32, 12)
for kk in range(4):
    a = math.pi / 2 * kk + math.pi / 4; TS.bar(0, (0, 0, 3.0), (1.35 * math.cos(a), 1.35 * math.sin(a), 3.0), 0.12)
TS = TS.done("turnstile")
LANE = Kit([TIMBER_DK, IRON_DK]); LANE.box(0, -0.15, 0.15, -6, 6, 0, 3.4)
for sy in (-6, 0, 6): LANE.box(0, -0.25, 0.25, sy - 0.25, sy + 0.25, 0, 3.6)
LANE = LANE.done("lane_barrier")
def mesh_paybox():
    """money-taker's pay box: 5 x 4 ft boarded box, counter and window to the lane, little roof (interpretive)"""
    k = Kit([TIMBER, TIMBER_DK, M_("baize", (0.12, 0.22, 0.12), 0.9)])
    k.box(0, -2.5, 2.5, -2.0, -1.85, 0, 7.0); k.box(0, -2.5, 2.5, 1.85, 2.0, 0, 7.0); k.box(0, -2.5, -2.35, -2.0, 2.0, 0, 7.0)
    k.box(0, 2.35, 2.5, -2.0, 2.0, 0, 3.4); k.box(0, 2.35, 2.5, -2.0, 2.0, 6.0, 7.0)          # lane side: counter + window
    k.box(2, 2.2, 3.2, -2.0, 2.0, 3.4, 3.55); k.box(1, -2.7, 2.9, -2.2, 2.2, 7.0, 7.4)
    for sy in (-1.95, 1.95): k.box(1, 2.35, 2.5, sy - 0.08, sy + 0.08, 3.4, 6.0)
    return k.done("paybox")
PAYBOX = mesh_paybox()
TSY = -193.0
lanes_x = [-9.0, -4.5, 0.0, 4.5, 9.0]
for j, lx in enumerate(lanes_x):
    if j < len(lanes_x) - 1: prop(f"LANE_{j}", LANE, (lx + lanes_x[j + 1]) / 2, TSY, 0, 0, part_kind="lane_barrier")
for j, lx in enumerate(lanes_x[:-1]):
    cx = (lx + lanes_x[j + 1]) / 2
    prop(f"TURNSTILE_{j}", TS, cx + 0.9, TSY + 2.5, 0, 0.3 * j, part_kind="turnstile")
for j, (bx, ry) in enumerate(((-12.6, 0.0), (12.6, math.pi))):
    prop(f"PAYBOX_{j}", PAYBOX, bx, TSY - 2.0, 0, ry, part_kind="paybox")
    person(f"MONEYTAKER_{j}", pmesh("man", [M_("coat_black2", (0.03, 0.03, 0.035)), WK["trou_dk"], SKIN2[0], M_("hat_blk2", (0.02, 0.02, 0.02)), WK["shirt"]], {"hat": "low", "cravat": True}, "moneytaker"),
           bx - 0.6 * (1 if bx < 0 else -1), TSY - 2.0, 0, heading_rz(-bx, 0), trade="money_taker")
for j, (px_, py_, hx, hy) in enumerate(((-15.5, -186, 1, -0.4), (14.8, -182, -1, -0.6), (3, -214, 0.2, 1))):
    person(f"POLICE_{j}", POLICE, px_, py_, 0, heading_rz(hx, hy), trade="police")
# the queue on the apron and in the lanes (working dress, 4 abreast), plus people coming through
GRAVEL = M_("gravel_apron", (0.50, 0.46, 0.40), 0.95)
slab("HP_APRON", -60, 60, -320, -204.3, 0.02, 0.3, GRAVEL, PROPS, part_kind="ground")
allwc = [("man", m) for m in wc["man"]] * 2 + [("woman", m) for m in wc["woman"]] * 2 + [("girl", m) for m in wc["girl"]] + [("boy", m) for m in wc["boy"]]
q = 0
for j, lx in enumerate(lanes_x[:-1]):
    cx = (lx + lanes_x[j + 1]) / 2
    for kk in range(3):
        kd, me = SRND.choice(allwc); person(f"QUEUE_LANE_{j}_{kk}", me, cx + SRND.uniform(-0.5, 0.5), TSY - 3.0 - 2.4 * kk, 0, heading_rz(0, 1) + SRND.uniform(-0.2, 0.2), person=kd, dress="working"); q += 1
yq = -209.0
while yq > -300:
    w = 4 if yq > -250 else 3
    for kk in range(w):
        if SRND.random() < 0.1: continue
        kd, me = SRND.choice(allwc)
        xq = -6.0 + 12.0 * (kk + 0.5) / w + SRND.uniform(-0.6, 0.6) - (0 if yq > -250 else (yq + 250) * 0.35)
        person(f"QUEUE_{q:03d}", me, xq, yq + SRND.uniform(-0.5, 0.5), 0, heading_rz(0, 1) + SRND.uniform(-0.3, 0.3), person=kd, dress="working"); q += 1
    yq -= 2.3
for kk in range(14):   # through the stiles and spreading into the transept
    kd, me = SRND.choice(allwc); xx = SRND.uniform(-12, 12); yy = SRND.uniform(-186, -168)
    if cam_conflict(xx, yy, 1.0, 0.0) or occupied(xx, yy, 1.1): continue
    OCC.append((xx, yy, 0.9, "person"))
    person(f"ENTERING_{kk}", me, xx, yy, 0, heading_rz(SRND.uniform(-0.4, 0.4), 1), person=kd, dress="working")
info["queue_figures"] = q

# ---- FT25: K-STAIR -- visitors on the south-east gallery stair (flights STFL_+1-1 at x 96 +- 7.75, y -60 -> -80, rise 11.46 ft) ----
ns = 0
for dx in (-7.75, 7.75):
    for kk, t in enumerate((0.12, 0.38, 0.62, 0.86)):
        if dx > 0 and kk in (0, 1): continue   # the camera's own flight stays clear at the foot
        y = -60 - 20 * t; z = 11.46 * t
        kd, me = SRND.choice(allwc)
        person(f"STAIR_{dx:+.0f}_{kk}", me, 96 + dx + SRND.uniform(-1.2, 1.2), y, z, heading_rz(0, -1) if kk % 3 else heading_rz(0, 1), person=kd, dress="working"); ns += 1
info["stair_figures"] = ns

# ---- FT26-FT27: attendants working the louvres (Muse hp-louvre-and-blind, north end wall, tier 1) ----
LV = muse_prop("hp-louvre-and-blind", lambda n: True, (0.0, 0.0, 0.0), "MUSE_Louvre_by_Muse")
nlv = 0
if LV:
    # keep only the open state (Model_Open, x ~ 0); drop the closed copy at +3.90 m
    for o in list(LV.objects):
        cx = sum((o.matrix_world @ Vector(v)).x for v in o.bound_box) / 8.0
        if cx > 2.4 or o.name.startswith("Backdrop") or o.name.endswith(".001"): LV.objects.unlink(o)
    hid = []
    for o in C["WALLS"].objects:
        if o.name.startswith("WLOUV_NE1") and abs(o.location.y / FT - 204) < 2 and 12 < o.location.x / FT < 36: hid.append(o.name); o.hide_render = True; o.hide_viewport = True
    for kk in range(3):
        xc = 16 + 8 * kk
        inst(LV, f"LOUVRE_MUSE_{kk}", xc, 204.0 - 0.35, 16.67, 0.0, 1.0, part_kind="louvre_gear"); nlv += 1
    ROPEK = Kit([ROPE])
    for sx in (-0.217 / FT, 0.217 / FT): ROPEK.bar(0, (sx, 0, 16.67 - 2.45), (sx * 0.6, 1.2, 4.0), 0.06)
    prop("LOUVRE_ROPE", ROPEK.done("louvre_rope"), 24, 204.0 - 0.35 - 0.32 / FT * 0.0 - 1.05, 0, 0, part_kind="louvre_rope")
    person("ATTEND_LOUVRE", ATTEND, 24.3, 198.0, 0, heading_rz(0, 1), trade="attendant")
    arm_reach("ATTEND_LOUVRE_ARM", 24.3, 198.0, 0, heading_rz(0, 1), up=0.6, side=0.66, tool=None, mat=WK["green"])
    info["louvres_hidden"] = hid
info["louvre_compartments"] = nlv
# FT28: watering the elms and the planters with cans
def mesh_can():
    k = Kit([M_("zinc", (0.50, 0.52, 0.52), 0.35, 0.9)]); k.cyl(0, (0, 0, 0), (0, 0, 1.0), 0.45, 14)
    k.bar(0, (0.35, 0, 0.2), (1.4, 0, 1.0), 0.1); k.cyl(0, (1.4, 0, 1.0), (1.55, 0, 1.08), 0.16, 8); k.bar(0, (-0.3, 0, 1.0), (0.3, 0, 1.0), 0.06)
    return k.done("watering_can")
CAN = mesh_can()
for j, (wx, wy, tx, ty) in enumerate(((7.5, 92.5, 12, 98), (17.5, 95.5, 12, 98), (2.0, 134.5, -3, 142))):
    rz = heading_rz(tx - wx, ty - wy)
    person(f"ATTEND_WATER_{j}", ATTEND, wx, wy, 0, rz, trade="attendant")
    arm_reach(f"ATTEND_WATER_{j}_ARM", wx, wy, 0, rz, up=-0.3, side=0.66, tool=None, mat=WK["green"])
    can = prop(f"CAN_{j}", CAN, wx + 1.4 * math.cos(rz - math.pi / 2) , wy + 1.4 * math.sin(rz - math.pi / 2), 3.0, rz - math.pi / 2, part_kind="watering_can")
    can.rotation_euler = (0, math.radians(28), rz - math.pi / 2)
    prop(f"CAN_SPARE_{j}", CAN, wx - 1.2, wy - 1.0, 0, j)
WATERM = M_("water_puddle", (0.18, 0.15, 0.11), 0.1)
for j, (px_, py_) in enumerate(((10.5, 95.5), (13.5, 96.0))):
    bmw = bmesh.new(); bm_box(bmw, ft(-1.5), ft(1.5), ft(-1.0), ft(1.0), ft(0.004), ft(0.008)); prop(f"WET_{j}", finish(bmw, f"wet_{j}", WATERM), px_, py_, 0)
STATE_INFO = info
print("HP51", info, flush=True)
