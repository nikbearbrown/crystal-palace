# Shared kit for the fit-out / HP51 / closing states (exec'd inside build_transept.py after dressing.py; uses its
# globals: Kit, new_obj, finish, bm_box, ft, inch, mat_principled, coll, ROOT, C, FG, MUSE_DIR, muse_prop ...).
# Feet throughout; person meshes face local -y (rz = heading + pi/2).
import random as _random
SRND = _random.Random(SEED + 1850)
def heading_rz(dx, dy): return math.atan2(dy, dx) + math.pi / 2
M_ = lambda n, c, r=0.8, m=0.0: mat_principled("FT_" + n, c, r, m)
SKIN2 = [M_("skin_a", (0.72, 0.53, 0.42), 0.6), M_("skin_b", (0.60, 0.43, 0.33), 0.6)]
WK = {"smock": M_("smock_white", (0.78, 0.76, 0.70)), "fustian": M_("fustian", (0.30, 0.24, 0.16)),
      "cord": M_("corduroy", (0.36, 0.30, 0.20)), "moleskin": M_("moleskin", (0.33, 0.31, 0.27)),
      "blue": M_("jacket_blue", (0.08, 0.10, 0.18)), "shirt": M_("shirt", (0.70, 0.68, 0.62)),
      "trou_dk": M_("trou_dark", (0.10, 0.09, 0.08)), "trou_fawn": M_("trou_fawn", (0.38, 0.32, 0.22)),
      "cap_dk": M_("cap_dark", (0.06, 0.06, 0.06)), "paper_cap": M_("paper_cap", (0.86, 0.85, 0.80)),
      "apron": M_("apron", (0.62, 0.58, 0.50)), "green": M_("livery_green", (0.06, 0.14, 0.08)), "brass": M_("brass", (0.70, 0.52, 0.22), 0.3, 1.0)}
TIMBER = M_("timber_new", (0.66, 0.55, 0.40), 0.75)
TIMBER_DK = M_("timber_dark", (0.32, 0.24, 0.16), 0.8)
IRON_DK = M_("iron_dark", (0.06, 0.06, 0.065), 0.5, 0.6)
ROPE = M_("rope", (0.55, 0.47, 0.33), 0.9)
FIGS = coll("FIGURES_" + STATE.upper(), ROOT)
_PM = {}
def pmesh(kind, mats, style, key):
    if key not in _PM: _PM[key] = FG.person_mesh("P_" + key, kind, mats, style=style)
    return _PM[key]
def person(name, me, x, y, z, rz, coll_=None, **props):
    ob = new_obj(name, me, coll_ or FIGS, (ft(x), ft(y), ft(z)), rz, dict(props, part_kind=props.get("part_kind", "figure")))
    k = SRND.uniform(0.95, 1.04); ob.scale = (k, k, k * SRND.uniform(0.97, 1.03)); return ob
def worker_mesh(j):
    """working men 1851: fustian / corduroy / moleskin jackets, caps, a few smocks and aprons"""
    coats = [WK["fustian"], WK["cord"], WK["moleskin"], WK["blue"], WK["smock"]]
    tr = [WK["trou_dk"], WK["trou_fawn"], WK["cord"]]
    st = {"hat": ("cap", "cap", "low", "cap")[j % 4], "frock": j % 5 == 4}
    return pmesh("man", [coats[j % 5], tr[j % 3], SKIN2[j % 2], WK["cap_dk"], WK["shirt"]], st, f"worker_{j}")
def arm_reach(name, x, y, z, rz, up=1.0, side=0.66, tool="brush", mat=None, coll_=None):
    """a raised working arm (+ tool) added to a standing figure: shoulder (side, 0, 4.4) to hand forward/up (local -y)."""
    k = Kit([mat or WK["smock"], SKIN2[0], TIMBER_DK, WK["paper_cap"]])
    hand = (side * 0.7, -1.55, 4.4 + 1.1 * up)
    k.bar(0, (side, -0.1, 4.35), hand, 0.3)
    k.box(1, hand[0] - 0.12, hand[0] + 0.12, hand[1] - 0.12, hand[1] + 0.12, hand[2] - 0.12, hand[2] + 0.12)
    if tool == "brush":
        k.bar(2, hand, (hand[0], hand[1] - 0.55, hand[2] + 0.35), 0.08)
        k.box(3, hand[0] - 0.12, hand[0] + 0.12, hand[1] - 0.75, hand[1] - 0.5, hand[2] + 0.35, hand[2] + 0.65)
    elif tool == "crank":
        k.bar(2, hand, (hand[0], hand[1] - 0.2, hand[2] + 0.6), 0.1)
    return new_obj(name, k.done(name.lower()), coll_ or FIGS, (ft(x), ft(y), ft(z)), rz, {"part_kind": "figure_arm"})
def kneeler_mesh(mats):
    """kneeling man (laying boards / nailing): built from the person proportions, legs folded under."""
    k = Kit(mats)
    for s in (-0.3, 0.3):
        k.bar(1, (s, 0.0, 0.25), (s, 1.6, 0.25), 0.5)        # shins on the floor behind
        k.bar(1, (s, 0.0, 0.3), (s, 0.1, 1.9), 0.55)         # thighs up
    k.cyl(0, (0, 0.2, 1.8), (0, -0.4, 3.6), 0.62, 10)        # torso leaning forward
    for s in (-0.6, 0.6): k.bar(0, (s, -0.3, 3.4), (s * 0.6, -1.5, 1.2), 0.3)
    k.cyl(2, (0, -0.55, 3.75), (0, -0.62, 4.35), 0.32, 10)  # head
    k.cyl(3, (0, -0.6, 4.3), (0, -0.62, 4.5), 0.42, 10)     # cap
    return k.done("kneeler")
KNEEL = kneeler_mesh([WK["fustian"], WK["trou_dk"], SKIN2[0], WK["cap_dk"]])

# ---- Muse crate (closed with Grok sheathing) and Muse display case ----
def muse_crate_closed():
    mc = muse_prop("hp-crate-and-display-case", lambda n: n.startswith("Crate"), (1.70, 0.0, 0.0), "MUSE_Crate_by_Muse")
    if not mc: return None
    bm = bmesh.new()   # sheathing boards 5 in, 1/4 in gaps, and a lid over Muse's battened frame (crate local coords, metres)
    for kk in range(5):
        z0 = 0.004 + kk * 0.136; z1 = z0 + 0.13
        bm_box(bm, 1.15, 2.25, -0.352, -0.342, z0, z1); bm_box(bm, 1.15, 2.25, 0.342, 0.352, z0, z1)
        bm_box(bm, 1.148, 1.158, -0.342, 0.342, z0, z1); bm_box(bm, 2.242, 2.252, -0.342, 0.342, z0, z1)
    for kk in range(7): bm_box(bm, 1.15 + kk * 0.157, 1.15 + kk * 0.157 + 0.152, -0.36, 0.36, 0.68, 0.70)
    for sx in (1.35, 2.05): bm_box(bm, sx - 0.04, sx + 0.04, -0.36, 0.36, 0.70, 0.725)
    o = bpy.data.objects.new("CRATE_sheathing_Grok", finish(bm, "crate_sheathing", TIMBER)); o["credit"] = "Grok"
    mc.objects.link(o); mc["credit"] += " + Grok sheathing and lid"
    return mc
CRATE = muse_crate_closed()
CRATE_OPEN = muse_prop("hp-crate-and-display-case", lambda n: n.startswith("Crate"), (1.70, 0.0, 0.0), "MUSE_CrateOpen_by_Muse")
CASE_M = muse_prop("hp-crate-and-display-case", lambda n: n.startswith("Case"), (0.0, 0.0, 0.0), "MUSE_Case_by_Muse")
CRATE_L, CRATE_W, CRATE_H = 1.17 / FT, 0.77 / FT, 0.725 / FT     # ft
PROPS = coll("PROPS_" + STATE.upper(), ROOT)
def inst(mc, name, x, y, z, rz, s=1.0, sz=None, **props):
    e = bpy.data.objects.new(name, None); e.instance_type = 'COLLECTION'; e.instance_collection = mc
    e.location = (ft(x), ft(y), ft(z)); e.rotation_euler = (0, 0, rz); e.scale = (s, s, sz or s); PROPS.objects.link(e)
    for kk, v in dict(props, credit=props.get("credit", "Muse")).items(): e[kk] = v
    return e
def prop(name, me, x, y, z=0.0, rz=0.0, **props):
    return new_obj(name, me, PROPS, (ft(x), ft(y), ft(z)), rz, dict(props, credit=props.get("credit", "Grok")))

def mesh_trolley(handle=True):
    """porter's four-wheel truck: 6 x 3 ft deck 14 in up, 12 in cast wheels, T handle (local +y forward... handle at -y)"""
    k = Kit([TIMBER_DK, IRON_DK])
    k.box(0, -1.5, 1.5, -3.0, 3.0, 0.95, 1.18)
    for sx in (-1.35, 1.35): k.box(0, sx - 0.15, sx + 0.15, -3.0, 3.0, 0.8, 0.95)
    for sx in (-1.2, 1.2):
        for sy in (-2.2, 2.2): k.wheel(1, (sx * 1.18, sy, 0.5), "x", 0.5, w=0.18, rim=0.12, spokes=6)
    if handle:
        for sx in (-0.9, 0.9): k.bar(1, (sx, -3.0, 1.1), (sx * 0.5, -4.6, 3.1), 0.1)
        k.bar(1, (-0.8, -4.6, 3.1), (0.8, -4.6, 3.1), 0.1)
    return k.done("trolley")
TROLLEY = mesh_trolley()

def open_south_doors():
    """FT: the three central door openings of the south entrance stand open -- each 6 ft opening as two 3 ft leaves
    swung 90 deg inward against the jambs (leaf division inferred; the build had them as closed slabs)."""
    od = bpy.data.objects.get("SOUTH_DOORS")
    if not od: return 0
    mat = od.data.materials[0] if od.data.materials else WOOD
    bpy.data.objects.remove(od, do_unlink=True)
    k = Kit([mat])
    for xc in (-8, 0, 8):
        for sx in (-1, 1):
            xh = xc + 3 * sx - 0.12 * sx
            k.box(0, xh - 0.08, xh + 0.08, -204.0 + 0.2, -204.0 + 3.0, 0.1, 14.0)
    ob = new_obj("SOUTH_DOORS_OPEN", k.done("south_doors_open"), C["WALLS"], props={"part_kind": "door", "state": "open"})
    return 6

# FT39 (f02/h02/c02): the boarded end walls blew out white in sunlit exteriors -> tone the timber down ~25 %
# (state rounds only; the base transept build is unchanged). Weathered painted deal, not new white board.
for _mn, _rgb in (("GT_Timber", (0.54, 0.495, 0.42)), ("GT_Boarding", (0.45, 0.40, 0.325))):
    _m = bpy.data.materials.get(_mn)
    if _m and _m.use_nodes:
        _b = _m.node_tree.nodes.get("Principled BSDF")
        if _b and not _b.inputs["Base Color"].is_linked: _b.inputs["Base Color"].default_value = (*_rgb, 1)
        _m.diffuse_color = (*_rgb, 1)
