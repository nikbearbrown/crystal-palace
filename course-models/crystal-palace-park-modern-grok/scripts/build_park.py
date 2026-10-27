"""PARK54 / PARK60 / PARK-NOW (CP065–CP076): Crystal Palace Park after the palace.
Appends Sydenham ruins41 shell READ-ONLY (terraces, sphinxes, footing pads, empty footprint)
and dinosaurs-1854 READ-ONLY. Builds High Level closed state, NSC block-outs, restored subway,
footprint overlay, PPL-NOW. Units: metres in Blender (Sydenham file is metres); local props in feet via grokkit.
DEPARTURES D-PM-*. No LiDAR/OS open data found in workspace — levels inferred from Sydenham terrain (logged).
usage: blender -b -P scripts/build_park.py -- --out rounds/X.blend --state PARK54|PARK60|PARKNOW
"""
import bpy, sys, os, math, json, random
from mathutils import Vector, Matrix
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grokkit as G
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(k, d): return argv[argv.index(k) + 1] if k in argv else d
OUT = arg("--out", "/tmp/park.blend")
STATE = arg("--state", "PARKNOW").upper()   # PARK54 | PARK60 | PARKNOW
SY = arg("--sydenham",
    "/workspace/crystal-palace-sydenham/course-models/crystal-palace-sydenham-1856-grok/rounds/sydenham-ruins41-r11.blend")
DINO = arg("--dinos",
    "/workspace/crystal-palace-dinosaurs/course-models/crystal-palace-dinosaurs-1854-grok/rounds/dinosaurs-1854-r02.blend")
SEED = {"PARK54": 1954, "PARK60": 1964, "PARKNOW": 2024}.get(STATE, 2024)
R = random.Random(SEED)
assert STATE in ("PARK54", "PARK60", "PARKNOW"), STATE
sc = G.reset("PK_")
ROOT = G.coll({"PARK54": "PARK54_HighLevel_closed_1954",
               "PARK60": "PARK60_NationalSportsCentre_1960s",
               "PARKNOW": "PARK-NOW_present_day"}[STATE])
info = {"state": STATE, "inferences": []}

# ---- append Sydenham ruins41 shell (read-only; never edit sydenham folder) ----
DROP = {"CAMERAS", "PPL57_templates__instanced_not_rendered", "REF_plan_0205",
        "MUSE_the-three-graces", "MUSE_farnese-bull", "MUSE_krater-vase", "MUSE_display-plinth",
        "MUSE_sy-classical-cast-base", "MUSE_sy-gothic-arch-fragment",
        "SY56_waterworks_running__18Jun1856", "SY_north_transept__lost1866",
        "SY56_north_transept_colossi_muse__lost1866"}
with bpy.data.libraries.load(SY, link=False) as (src, dst):
    keep = [c for c in src.collections if c not in DROP]
    dst.collections = keep
SY_ROOT = G.coll("SYDENHAM_RUINS41_APPENDED", ROOT)
for c in dst.collections:
    if c: SY_ROOT.children.link(c)
info["sydenham_appended"] = len(dst.collections)
# Drop any cameras that rode in on non-CAMERAS collections (avoid name collisions / bad lookats)
for _o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
    bpy.data.objects.remove(_o, do_unlink=True)
info["inferences"].append("D-PM-01 I: park levels reuse Sydenham ruins41 terrain (no OS/LiDAR open data in workspace; searched 2026-10-27)")

# r17d: mid warm stone on sphinx (was too dark vs olive; was washed white before)
for _m in bpy.data.materials:
    if "sphinx" in _m.name.lower():
        if _m.use_nodes:
            for _n in _m.node_tree.nodes:
                if _n.type == "BSDF_PRINCIPLED":
                    _n.inputs["Base Color"].default_value = (0.52, 0.46, 0.36, 1.0)
                    try: _n.inputs["Roughness"].default_value = 0.88
                    except Exception: pass
        else:
            _m.diffuse_color = (0.52, 0.46, 0.36, 1.0)

# ---- materials ----
# r02: richer present-day materials — noise grass, worn stone, NSC formwork concrete
M_brick = G.mat("Brick", (0.30, 0.18, 0.12), 0.9)
M_brick_w = G.mat("BrickWeathered", (0.35, 0.28, 0.22), 0.95)
M_stone = G.mat_noise("StoneWorn", (0.42, 0.40, 0.36), (0.58, 0.55, 0.48), rough=0.9, scale=8.0, bump=0.12)
M_concrete = G.mat_noise("ConcreteNSC", (0.48, 0.47, 0.44), (0.62, 0.60, 0.55), rough=0.88, scale=4.5, bump=0.15)
M_concrete_d = G.mat_noise("ConcreteDark", (0.32, 0.32, 0.30), (0.42, 0.41, 0.38), rough=0.85, scale=3.5, bump=0.12)
M_iron = G.mat("Iron", (0.10, 0.10, 0.11), 0.5, 0.3)
M_rust = G.mat("Rust", (0.30, 0.14, 0.06), 0.9, 0.2)
M_glass = G.mat_thin_glass("Glass", (0.78, 0.84, 0.86), 0.12)
M_road = G.mat("Road", (0.22, 0.22, 0.20), 0.95)
M_grass = G.mat_noise("Grass", (0.14, 0.28, 0.10), (0.28, 0.42, 0.16), rough=0.95, scale=40.0, bump=0.06)
M_bark = G.mat_noise("Bark", (0.18, 0.12, 0.08), (0.28, 0.20, 0.12), rough=0.9, scale=18.0, bump=0.2)
M_leaf = G.mat_noise("Leaf", (0.10, 0.28, 0.08), (0.22, 0.40, 0.14), rough=0.85, scale=25.0, bump=0.05)
M_tile = G.mat("Tile", (0.55, 0.30, 0.14), 0.6)
M_cream = G.mat("VaultCream", (0.78, 0.72, 0.58), 0.85)
M_red = G.mat("VaultRed", (0.42, 0.12, 0.08), 0.85)
M_asphalt = G.mat("Asphalt", (0.12, 0.12, 0.12), 0.95)
M_track_red = G.mat("TrackRed", (0.85, 0.10, 0.04), 0.8, 0.0, emit=((1.0, 0.18, 0.05), 0.55))  # r17h emit so AgX keeps red
M_infield = G.mat("NSCInfield", (0.22, 0.38, 0.16), 0.9)
M_seat = G.mat("Seat", (0.62, 0.16, 0.12), 0.65)  # r17 slightly brighter seat face
M_skin = G.mat("Skin", (0.55, 0.40, 0.32), 0.6)
M_coat = G.mat("Coat", (0.15, 0.18, 0.22), 0.85)
M_jeans = G.mat("Jeans", (0.12, 0.18, 0.32), 0.85)
M_overlay = G.mat("FootprintOverlay", (0.85, 0.55, 0.10), 0.4, emit=((0.9, 0.55, 0.05), 0.6))

FT = 0.3048
def ft(v): return v * FT

# High Level placement (same as SY60, metres)
ZS = ft(-2); ROAD_Z = ft(4); SUB_Z = ft(-14); SUB_CROWN = ft(-2); SUB_W = ft(18)
ST_X0, ST_X1 = ft(-220), ft(220); ST_Y0, ST_Y1 = ft(300), ft(400)
BOOK_Y0, BOOK_Y1 = ft(260), ft(300); SUB_Y0, SUB_Y1 = ft(190), ft(268)
PARADE_Y0, PARADE_Y1 = ft(200), ft(260)
EYE = 1.6

def box(name, coll, x0, x1, y0, y1, z0, z1, mat_):
    vs = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    fs = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update()
    if mat_: me.materials.append(mat_)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob); return ob

def poly(name, coll, pts, mat_):
    me = bpy.data.meshes.new(name); me.from_pydata(pts, [], [tuple(range(len(pts)))]); me.update()
    if mat_: me.materials.append(mat_)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob); return ob

def cam(name, loc, look, lens):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.sensor_width = 36; cd.clip_end = 3000
    o = bpy.data.objects.new(name, cd); CAM.objects.link(o)
    o.location = loc
    d = Vector(look) - o.location
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return o

CAM = G.coll("CAMERAS", ROOT)

# =====================================================================
# High Level station + subway (all park states; condition varies)
# =====================================================================
HL = G.coll("G_STATION_HighLevel", ROOT)
closed = STATE in ("PARK54", "PARK60", "PARKNOW")
restored_sub = STATE == "PARKNOW"
brick_m = M_brick_w if closed else M_brick

# Parade road
box("pk_parade_road", HL, ST_X0 - ft(30), ST_X1 + ft(30), PARADE_Y0, PARADE_Y1, ROAD_Z - 0.3, ROAD_Z, M_road)

# Station shed — derelict / closed in PARK54+
EAVE, RIDGE = ZS + ft(22), ZS + ft(34)
box("pk_hl_wall_S", HL, ST_X0, ST_X1, ST_Y0 - 0.4, ST_Y0 + 0.4, ZS, EAVE, brick_m)
box("pk_hl_wall_N", HL, ST_X0, ST_X1, ST_Y1 - 0.4, ST_Y1 + 0.4, ZS, EAVE, brick_m)
box("pk_hl_wall_W", HL, ST_X0 - 0.4, ST_X0, ST_Y0, ST_Y1, ZS, EAVE, brick_m)
box("pk_hl_wall_E", HL, ST_X1, ST_X1 + 0.4, ST_Y0, ST_Y1, ZS, EAVE, brick_m)
# roof: intact glass for 1865 would be elsewhere; here boarded/partial for closed states
yc = (ST_Y0 + ST_Y1) / 2
if STATE == "PARK54":
    # boarded / missing panes, rusting trusses
    for (ya, yb) in ((ST_Y0, yc), (yc, ST_Y1)):
        ym = (ya + yb) / 2
        poly(f"pk_hl_roof_{ya:.0f}", HL,
             [(ST_X0, ya, EAVE), (ST_X1, ya, EAVE), (ST_X1, ym, RIDGE), (ST_X0, ym, RIDGE)], M_rust)
    # boarded openings
    box("pk_hl_boarding", HL, ST_X0 + 2, ST_X1 - 2, ST_Y0 + 0.5, ST_Y0 + 1.0, ZS + ft(3), ZS + ft(12), G.mat("Board", (0.25, 0.18, 0.10), 0.9))
elif STATE in ("PARK60", "PARKNOW"):
    # demolished / cleared station — only platform stubs and subway head remain (R: closed 1954, later demolished)
    box("pk_hl_platform_stub", HL, ST_X0 + ft(20), ST_X1 - ft(20), ST_Y0 + ft(5), ST_Y0 + ft(18), ZS, ZS + ft(1.5), M_concrete_d)
    info["inferences"].append("D-PM-02 I: HL shed demolished by 1960s; platform stubs only (exact demolition date U)")
else:
    pass
# platforms (PARK54 keeps them)
if STATE == "PARK54":
    box("pk_hl_platform_1", HL, ST_X0 + ft(8), ST_X1 - ft(8), ST_Y0 + ft(2), ST_Y0 + ft(20), ZS, ZS + ft(3), M_stone)
    box("pk_hl_platform_2", HL, ST_X0 + ft(8), ST_X1 - ft(8), yc - ft(8), yc + ft(8), ZS, ZS + ft(3), M_stone)

# Booking hall / subway head
box("pk_booking_floor", HL, ft(-40), ft(40), BOOK_Y0, BOOK_Y1, ZS, ZS + 0.15, M_stone if restored_sub else M_brick_w)
box("pk_booking_wall_L", HL, ft(-42), ft(-40), BOOK_Y0, BOOK_Y1, ZS, ZS + ft(16), brick_m)
box("pk_booking_wall_R", HL, ft(40), ft(42), BOOK_Y0, BOOK_Y1, ZS, ZS + ft(16), brick_m)
if STATE == "PARK54":
    box("pk_booking_closed_gate", HL, ft(-9), ft(9), BOOK_Y0, BOOK_Y0 + 0.3, ZS, ZS + ft(10), M_iron)  # quieter closed entrance
    # r17 WEAK CP065: approach-side boarding, notices, chain, threshold lamps (story: closed 1954)
    board_m = G.mat("BoardGate", (0.22, 0.15, 0.08), 0.9)
    chalk_m = G.mat("NoticeBoard", (0.75, 0.72, 0.62), 0.85)
    for bx in (ft(-28), ft(-16), ft(8), ft(20)):
        box(f"pk_book_board_{bx:.0f}", HL, bx, bx + ft(8), BOOK_Y0 - 0.5, BOOK_Y0 - 0.15, ZS + ft(2), ZS + ft(9), board_m)
    for bx in (ft(-20), ft(12)):
        box(f"pk_book_notice_{bx:.0f}", HL, bx, bx + ft(5), BOOK_Y0 - 0.7, BOOK_Y0 - 0.4, ZS + ft(4), ZS + ft(7), chalk_m)
    for i, bx in enumerate(range(int(ft(-9)), int(ft(9)), 2)):
        zc = ZS + ft(4.5) + (0.25 if i % 2 else -0.2)
        box(f"pk_book_chain_{i}", HL, bx, bx + 1.6, BOOK_Y0 - 0.9, BOOK_Y0 - 0.7, zc, zc + 0.3, M_iron)
    # warm threshold lamps so closed gate reads at dusk
    for i, lx in enumerate((ft(-14), 0.0, ft(14))):
        ld = bpy.data.lights.new(f"pk_book_lamp_{i}", "POINT"); ld.energy = 320; ld.color = (1.0, 0.78, 0.45)
        lo = bpy.data.objects.new(ld.name, ld); HL.objects.link(lo)
        lo.location = (lx, BOOK_Y0 + 4, ZS + ft(12))
    # approach paving on parade side of gate
    box("pk_booking_approach", HL, ft(-40), ft(40), PARADE_Y1 - ft(8), BOOK_Y0, ROAD_Z - 0.05, ROAD_Z + 0.05, M_stone)

# Subway vault
def build_subway(restored=False):
    SUB = G.coll("G_STATION_subway", HL)
    vm = M_cream if restored else M_brick_w
    fm = M_tile if restored else M_stone
    box("pk_subway_floor", SUB, -SUB_W/2, SUB_W/2, SUB_Y0, SUB_Y1, SUB_Z - 0.15, SUB_Z, fm)
    box("pk_subway_wall_L", SUB, -SUB_W/2 - 0.25, -SUB_W/2, SUB_Y0, SUB_Y1, SUB_Z, SUB_Z + ft(8), vm)
    box("pk_subway_wall_R", SUB, SUB_W/2, SUB_W/2 + 0.25, SUB_Y0, SUB_Y1, SUB_Z, SUB_Z + ft(8), vm)
    # faceted barrel vault
    segs, bays = 10, 12
    bay = (SUB_Y1 - SUB_Y0) / bays
    SPRING = SUB_Z + ft(8)
    for i in range(bays):
        ya = SUB_Y0 + i * bay; yb = ya + bay
        pts = []
        for k in range(segs + 1):
            a = math.pi * k / segs
            x = (-SUB_W/2) * math.cos(a)
            z = SPRING + (SUB_CROWN - SPRING) * math.sin(a)
            pts.append((x, ya, z))
        for k in range(segs + 1):
            a = math.pi * (segs - k) / segs
            x = (-SUB_W/2) * math.cos(a)
            z = SPRING + (SUB_CROWN - SPRING) * math.sin(a)
            pts.append((x, yb, z))
        # build as strip quads
        vs = []; fs = []
        for k in range(segs + 1):
            a = math.pi * k / segs
            x = (-SUB_W/2) * math.cos(a)
            z = SPRING + (SUB_CROWN - SPRING) * math.sin(a)
            vs.append((x, ya, z)); vs.append((x, yb, z))
        for k in range(segs):
            a = k * 2; fs.append((a, a+1, a+3, a+2))
        me = bpy.data.meshes.new(f"pk_vault_bay_{i}"); me.from_pydata(vs, [], fs); me.update()
        me.materials.append(vm if restored else M_brick_w)
        ob = bpy.data.objects.new(f"pk_vault_bay_{i}", me); SUB.objects.link(ob)
        # columns
        for s in (-1, 1):
            cx = s * (SUB_W/2 - ft(1.2))
            box(f"pk_col_{i}_{s}", SUB, cx - 0.15, cx + 0.15, ya + 0.05, ya + 0.25, SUB_Z, SPRING, M_red if restored else M_brick_w)
    # exit pavilion (south / park side)
    box("pk_subway_exit", SUB, -SUB_W/2 - ft(4), SUB_W/2 + ft(4), SUB_Y0 - ft(8), SUB_Y0, SUB_Z, SUB_Z + ft(12), M_stone)
    # r17k: sealed bulkhead at north end (1954 closure) — fills CP065 lookat at subway Z
    if not restored:
        box("pk_subway_seal_N", SUB, -SUB_W/2 - 0.1, SUB_W/2 + 0.1, SUB_Y1 - 0.35, SUB_Y1, SUB_Z, SUB_CROWN + 0.2, M_iron)
        box("pk_subway_seal_bar_1", SUB, -SUB_W/2 + 0.3, SUB_W/2 - 0.3, SUB_Y1 - 0.55, SUB_Y1 - 0.4, SUB_Z + ft(3), SUB_Z + ft(3.4), M_iron)
        box("pk_subway_seal_bar_2", SUB, -SUB_W/2 + 0.3, SUB_W/2 - 0.3, SUB_Y1 - 0.55, SUB_Y1 - 0.4, SUB_Z + ft(6), SUB_Z + ft(6.4), M_iron)
    if restored:
        info["inferences"].append("D-PM-03 I: subway shown in restored Open-House condition (cream/red patterned brick); exact 2020s finish U")
    else:
        info["inferences"].append("D-PM-04 I: subway sealed/quiet after 1954 closure; interior still patterned but dim")
    return SUB

build_subway(restored=restored_sub)

# =====================================================================
# NSC block-outs (PARK60 + PARKNOW) — athletics stadium + sports hall
# =====================================================================
# Location I: lower park / former Italian-garden / football area, ~ (-50, -550) m
# Real NSC opened 1964 (R). Plans not in repo -> block-outs U/I.
if STATE in ("PARK60", "PARKNOW"):
    NSC = G.coll("G_NSC_NationalSportsCentre", ROOT)
    CX, CY, CZ = -50.0, -550.0, -40.0   # r17g: above park_slope (~-45.5) so red track is not buried
    info["inferences"].append(f"D-PM-05 I: NSC placed at ({CX},{CY},{CZ}) m near former south-basin/football ground; no NSC plan in repo")
    # athletics stadium: oval bowl ~180 x 120 m, banked seating
    RW, RH = 90.0, 60.0
    box("nsc_infield", NSC, CX - 50, CX + 50, CY - 35, CY + 35, CZ, CZ + 0.2, M_infield)
    # r17: red cinder track ring so CP066 reads as athletics stadium
    box("nsc_track_N", NSC, CX - 75, CX + 75, CY + 32, CY + 52, CZ, CZ + 0.45, M_track_red)
    box("nsc_track_S", NSC, CX - 75, CX + 75, CY - 52, CY - 32, CZ, CZ + 0.45, M_track_red)
    box("nsc_track_W", NSC, CX - 75, CX - 45, CY - 32, CY + 32, CZ, CZ + 0.45, M_track_red)
    box("nsc_track_E", NSC, CX + 45, CX + 75, CY - 32, CY + 32, CZ, CZ + 0.45, M_track_red)
    # concrete seating banks — tiered risers
    for (name, x0, x1, y0, y1, z1) in (
        ("nsc_bank_N", CX - 80, CX + 80, CY + 48, CY + 72, CZ + 12),
        ("nsc_bank_S", CX - 80, CX + 80, CY - 72, CY - 48, CZ + 12),
        ("nsc_bank_W", CX - 95, CX - 70, CY - 55, CY + 55, CZ + 14),
        ("nsc_bank_E", CX + 70, CX + 95, CY - 55, CY + 55, CZ + 14),
    ):
        box(name, NSC, x0, x1, y0, y1, CZ, z1, M_concrete)
        box(name + "_seats", NSC, x0 + 1, x1 - 1, y0 + 1, y1 - 1, z1 - 0.4, z1, M_seat)
        # mid tier for depth
        box(name + "_mid", NSC, x0 + 2, x1 - 2, y0 + 2, y1 - 2, CZ + 4, z1 - 2, M_concrete)
    # concrete sports hall (block) east of stadium
    HX, HY = CX + 130, CY
    box("nsc_sports_hall", NSC, HX - 35, HX + 35, HY - 25, HY + 25, CZ, CZ + 14, M_concrete_d)
    box("nsc_sports_hall_roof", NSC, HX - 36, HX + 36, HY - 26, HY + 26, CZ + 14, CZ + 15.5, M_concrete)
    box("nsc_sports_hall_glazing", NSC, HX - 34, HX + 34, HY - 24.7, HY - 24.5, CZ + 3, CZ + 12, M_glass)
    # access road
    box("nsc_access_road", NSC, CX - 20, CX + 160, CY + 80, CY + 88, CZ - 0.5, CZ, M_road)
    # r17 floodlight poles + warm fills so bowl isn't a dark mass (CP066)
    for i, (px, py) in enumerate(((CX - 85, CY - 55), (CX + 85, CY - 55), (CX - 85, CY + 55), (CX + 85, CY + 55))):
        box(f"nsc_flood_pole_{i}", NSC, px - 0.5, px + 0.5, py - 0.5, py + 0.5, CZ, CZ + 28, M_iron)
        fl = bpy.data.lights.new(f"nsc_flood_{i}", "AREA"); fl.energy = 2400; fl.color = (1.0, 0.92, 0.75); fl.size = 7
        fo = bpy.data.objects.new(fl.name, fl); NSC.objects.link(fo)
        fo.location = (px, py, CZ + 26)
        direction = Vector((CX - px, CY - py, (CZ + 2) - (CZ + 26)))
        fo.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    info["nsc"] = 1
    # r17d: south basins sit on same footprint as NSC — hide so red track/infield read
    for _o in list(bpy.data.objects):
        if _o.name.startswith("park_basins"):
            _o.hide_render = True
            _o.hide_viewport = True

# =====================================================================
# PARK-NOW extras: footprint overlay, dinosaurs append, PPL-NOW
# =====================================================================
if STATE == "PARKNOW":
    # Footprint overlay — glowing outline of Sydenham palace on empty plateau (interpretive, CP072)
    OV = G.coll("PARKNOW_footprint_overlay", ROOT)
    # palace footprint: x -804..+804, y -156..+156 (feet) = metres
    hx, hy = ft(804), ft(156)
    z_ov = 0.15  # slightly above footing pads
    # outline strips
    tw = 0.6
    box("ov_N", OV, -hx, hx, hy - tw, hy, z_ov, z_ov + 0.08, M_overlay)
    box("ov_S", OV, -hx, hx, -hy, -hy + tw, z_ov, z_ov + 0.08, M_overlay)
    box("ov_W", OV, -hx, -hx + tw, -hy, hy, z_ov, z_ov + 0.08, M_overlay)
    box("ov_E", OV, hx - tw, hx, -hy, hy, z_ov, z_ov + 0.08, M_overlay)
    # central transept stub
    ctx, cty = ft(60), ft(192)
    box("ov_CT", OV, -ctx, ctx, -cty, cty, z_ov, z_ov + 0.08, M_overlay)
    info["inferences"].append("D-PM-06 I: footprint overlay registered to Sydenham model axes (not independently georeferenced OS); label approximate")

    # Append dinosaurs READ-ONLY (lake-island sculptures)
    DN = G.coll("G_DINO_appended_readonly", ROOT)
    DINO_KEEP = {"DN54_lake_islands__1854", "DN54_secondary_island_sculptures__1854",
                 "DN54_tertiary_island_mammals__1854", "DN54_geological_strata__1854"}
    try:
        with bpy.data.libraries.load(DINO, link=False) as (src, dst):
            dst.collections = [c for c in src.collections if c in DINO_KEEP]
        for c in dst.collections:
            if c: DN.children.link(c)
        info["dinos_appended"] = len(dst.collections)
        # Native dinosaurs blend is local-origin; translate to south-park lake islands (I; no OS/LiDAR).
        DINO_OFF = Vector((-50.0, -880.0, -48.0))
        for _c in dst.collections:
            if not _c: continue
            for _o in _c.all_objects:
                _o.location = Vector(_o.location) + DINO_OFF
        info["inferences"].append("D-PM-07 R: dinosaurs appended read-only from dinosaurs-1854-r02.blend (conserved survivors)")
        info["inferences"].append("D-PM-08 I: dinosaur cluster translated by (-50,-880,-48) m to south-park lake; native blend local origin")
        # CP067 interpretive board (conservation / "earlier understanding")
        board_m = G.mat("InterpBoard", (0.15, 0.18, 0.12), 0.7)
        box("pk_dino_interp_board", DN, -25, -23.5, -868, -866, -47.5, -45.5, board_m)
    except Exception as e:
        info["dinos_appended"] = 0
        info["inferences"].append(f"D-PM-07 U: dino append failed: {e}")

    # PPL-NOW: present-day visitors (simple lathe stand-ins)
    PPL = G.coll("PPL_NOW_visitors", ROOT)
    def visitor(name, x, y, z, rot=0):
        bm = __import__("bmesh").new()
        import bmesh
        from mathutils import Matrix as Mx
        # r02: clearer silhouette — legs, wider torso, arms, head
        for s in (-0.10, 0.10):
            bmesh.ops.create_cone(bm, cap_ends=True, segments=5, radius1=0.07, radius2=0.055, depth=0.85,
                                  matrix=Mx.Translation(Vector((x + s, y, z + 0.42))))
        bmesh.ops.create_cone(bm, cap_ends=True, segments=7, radius1=0.26, radius2=0.18, depth=0.75,
                              matrix=Mx.Translation(Vector((x, y, z + 1.2))))
        for s in (-0.32, 0.32):
            bmesh.ops.create_cone(bm, cap_ends=True, segments=4, radius1=0.05, radius2=0.04, depth=0.55,
                                  matrix=Mx.Translation(Vector((x + s, y, z + 1.25))) @ Mx.Rotation(math.radians(18 if s > 0 else -18), 4, 'Y'))
        bmesh.ops.create_uvsphere(bm, u_segments=7, v_segments=5, radius=0.13,
                                  matrix=Mx.Translation(Vector((x, y, z + 1.72))))
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
        me.materials.append(M_coat if R.random() < 0.5 else M_jeans); me.materials.append(M_skin)
        o = bpy.data.objects.new(name, me); o.rotation_euler[2] = rot; PPL.objects.link(o)
        return o
    # visitors on terrace / plateau / subway / dino path / NSC
    spots = []
    for i in range(30):  # plateau / footprint
        spots.append((R.uniform(-200, 200)*FT, R.uniform(-100, 100)*FT, 0.1))
    for i in range(20):  # upper terrace (yU ~ -337 ft)
        spots.append((R.uniform(-200, 200)*FT, ft(-337) + R.uniform(0, 10), ft(-23.58) + 0.1))
    for i in range(15):  # subway
        spots.append((R.uniform(-SUB_W/2+0.5, SUB_W/2-0.5), R.uniform(SUB_Y0+2, SUB_Y1-2), SUB_Z))
    for i in range(25):  # NSC
        spots.append((-50 + R.uniform(-40, 40), -550 + R.uniform(-40, 40), -47 + 0.2))
    for i in range(12):  # dinosaur islands area (approx - south park)
        spots.append((-80 + R.uniform(-60, 60), -900 + R.uniform(-80, 80), -50))
    # clear 7 ft around cameras (added below — so place people after cams? do cams first)
    info["ppl_spots_planned"] = len(spots)

    # r02: present-day grass carpets + park trees (richer PARK-NOW materials)
    GR = G.coll("PARKNOW_grass_trees", ROOT)
    box("pk_grass_plateau", GR, -hx - 40, hx + 40, -hy - 80, hy + 40, -0.05, 0.02, M_grass)
    box("pk_grass_terrace_band", GR, -hx, hx, ft(-337) - 5, ft(-337) + 25, ft(-23.58) - 0.05, ft(-23.58) + 0.02, M_grass)
    box("pk_grass_nsc_surround", GR, CX - 120, CX + 120, CY - 100, CY + 100, CZ - 0.3, CZ - 0.05, M_grass)
    def _tree(name, x, y, z, h):
        bm = __import__("bmesh").new(); import bmesh
        from mathutils import Matrix as Mx
        bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=h*0.04, radius2=h*0.02, depth=h*0.55,
                              matrix=Mx.Translation(Vector((x, y, z + h*0.28))))
        for k in range(4):
            ox, oy = R.uniform(-h*0.12, h*0.12), R.uniform(-h*0.12, h*0.12)
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=h*0.22*R.uniform(0.7, 1.1),
                                       matrix=Mx.Translation(Vector((x+ox, y+oy, z + h*0.55 + R.uniform(0, h*0.15)))))
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
        me.materials.append(M_bark); me.materials.append(M_leaf)
        for i, p in enumerate(me.polygons):
            p.material_index = 0 if i < 6 else 1
        o = bpy.data.objects.new(name, me); GR.objects.link(o); return o
    for i in range(28):
        _tree(f"pk_tree_{i}", R.uniform(-220, 220), R.uniform(-180, 120), 0.0, R.uniform(8, 16))
    for i in range(18):
        _tree(f"pk_tree_nsc_{i}", CX + R.uniform(-90, 90), CY + R.uniform(-70, 90), CZ, R.uniform(7, 14))
    info["inferences"].append("D-PM-12 I: PARK-NOW grass carpets + park trees (no OS tree survey; placement U)")

# Subway interior lights (underground; needed for CP071 / CP065 threshold)
SUB_LIGHTS = G.coll("G_STATION_subway_lights", ROOT)
def _sub_light(name, y, energy=500):
    ld = bpy.data.lights.new(name, "AREA"); ld.energy = energy; ld.size = 1.2; ld.size_y = 0.6
    ld.shape = "RECTANGLE"; ld.color = (1.0, 0.95, 0.85)
    o = bpy.data.objects.new(name, ld); SUB_LIGHTS.objects.link(o)
    o.location = (0, y, SUB_CROWN - 0.4); return o
_y = SUB_Y0 + 4
_i = 0
while _y < SUB_Y1 - 3:
    _sub_light(f"pk_subway_light_{_i}", _y, 600 if restored_sub else 180); _i += 1; _y += 5.5
_sub_light("pk_subway_exit_fill", SUB_Y0 - 1.5, 350 if restored_sub else 120)

# =====================================================================
# Cameras (storyboard CP065–CP076)
# =====================================================================
# CP065 PARK54: r17 — approach from parade facing closed gate (was cam pressed into gate → blank FOV)
cam("CAM_CP065_hl_closed_35mm", (ft(18), PARADE_Y1 - ft(6), ROAD_Z + EYE), (0, BOOK_Y0 + 1, ZS + ft(6)), 35)
# hero r17k: inside vault looking north at sealed bulkhead (street booking is above SUB_Z)
_c65 = cam("CAM_CP065_subway_threshold_35mm", (0, SUB_Y0 + ft(28), SUB_Z + EYE), (0, SUB_Y1 - 0.2, SUB_Z + ft(5)), 35)
_c65.location = Vector((0, SUB_Y0 + ft(28), SUB_Z + EYE)); _c65.keyframe_insert("location", frame=1)
_c65.location = Vector((0, SUB_Y0 + ft(40), SUB_Z + EYE)); _c65.keyframe_insert("location", frame=120)

# CP066 PARK60: r17 elevated looking into lit bowl with red track
if STATE in ("PARK60", "PARKNOW"):
    # r17f: high SW 3/4 over bowl — red track oval + green infield must read as sports
    cam("CAM_CP066_nsc_stadium_35mm", (-180, -680, 18), (-50, -550, -38), 28)
    cam("CAM_CP066_nsc_hall_35mm", (40, -520, -40), (80, -550, -33), 35)
    cam("CAM_CP066_nsc_wide_35mm", (-50, -380, -12), (-50, -560, -40), 35)

if STATE == "PARKNOW":
    # CP070 begin walk — lower station area (distinct from HL)
    cam("CAM_CP070_park_entry_35mm", (ft(-800), ft(-1200), -40), (0, ft(-400), 10), 35)  # CP070 begin the walk today
    # alias name for coverage audit
    cam("CAM_CP070_begin_walk_35mm", (ft(-800), ft(-1200), -40), (0, ft(-400), 10), 35)
    # CP071 restored subway interior
    cam("CAM_CP071_subway_interior_28mm", (0, (SUB_Y0+SUB_Y1)/2, SUB_Z + EYE), (0, SUB_Y0, SUB_Z + 1.5), 28)
    cam("CAM_CP071_subway_vault_50mm", (SUB_W/4, SUB_Y1 - 5, SUB_Z + EYE), (0, SUB_Y0 + 10, SUB_Z + 3), 50)
    # CP072 empty footprint + overlay
    cam("CAM_CP072_footprint_35mm", (ft(-420), ft(-280), 28), (0, 0, 1), 35)
    # r17j: from SE along terrace — sphinx + steps + arches; sky not plateau fill
    cam("CAM_CP073_sphinx_steps_50mm", (ft(20), ft(-370), ft(-23.58) + EYE),
        (ft(-54.5), ft(-337), ft(-23.58) + 1.2), 35)
    cam("CAM_CP073_steps_35mm", (ft(-100), ft(-380), ft(-43.58) + EYE),
        (ft(-40), ft(-337) + 2, ft(-23.58) + 1.5), 35)
    # r17d warm fill so sphinx stone reads against sky
    _sl = bpy.data.lights.new("sphinx_fill", "AREA"); _sl.energy = 900; _sl.color = (1.0, 0.95, 0.85); _sl.size = 8
    _so = bpy.data.objects.new("sphinx_fill", _sl); ROOT.objects.link(_so)
    _so.location = (ft(-40), ft(-320), ft(-10))
    # CP067 — dinosaur conservation today (preserving Hawkins' earlier understanding)
    cam("CAM_CP067_dino_conservation_35mm", (5, -855, -43), (-35, -878, -46.5), 35)
    # CP074 dinosaurs (after D-PM-08 translate; aim at iguanodon/megalosaurus cluster)
    cam("CAM_CP074_dinosaurs_35mm", (-10, -860, -44), (-40, -875, -46.5), 35)
    cam("CAM_CP074_iguanodon_50mm", (20, -870, -45), (-5, -878, -46.5), 50)
    # CP075 layered landscape NSC + park
    cam("CAM_CP075_layered_nsc_35mm", (-50, -300, -10), (-50, -550, -40), 35)
    # CP076 turn back toward empty site
    cam("CAM_CP076_empty_plateau_35mm", (ft(200), ft(-400), 15), (0, 0, 5), 35)
    cam("CAM_CP076_hold_35mm", (ft(200), ft(-400), 15), (0, ft(-50), 2), 35)

    # place PPL-NOW with 7 ft camera clear zone + hero silhouettes just outside
    cams_xy = [(o.location.x, o.location.y, o.location.z) for o in bpy.data.objects if o.type == "CAMERA"]
    n_placed = 0
    for i, (x, y, z) in enumerate(spots):
        if any((x - cx)**2 + (y - cy)**2 < (7 * FT)**2 for cx, cy, _ in cams_xy): continue
        visitor(f"ppl_now_{n_placed:03d}", x, y, z, R.uniform(0, 6.28)); n_placed += 1
    for cx, cy, cz in cams_xy:
        for k in range(3):
            ang = k * 2.1 + 0.4; d = 3.2 + (k % 2) * 0.6
            visitor(f"ppl_now_hero_{n_placed:03d}", cx + d*math.cos(ang), cy + d*math.sin(ang), cz - 1.55, ang + math.pi)
            n_placed += 1
    info["ppl_now"] = n_placed

# =====================================================================
# World / render settings
# =====================================================================
w = bpy.data.worlds.new("sky"); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes["Background"]
sky = nt.nodes.new("ShaderNodeTexSky")
try: sky.sky_type = "NISHITA"
except Exception: pass
try:
    # r17: state-tuned sky — PARKNOW cooler/lower so sphinx not blown; PARK54 dusk; PARK60 evening floods
    if STATE == "PARKNOW":
        sky.sun_elevation = math.radians(28); sky.sun_rotation = math.radians(220)
    elif STATE == "PARK54":
        sky.sun_elevation = math.radians(12); sky.sun_rotation = math.radians(200)
    else:
        sky.sun_elevation = math.radians(10); sky.sun_rotation = math.radians(215)
except Exception: pass
nt.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 1.0 if STATE == "PARKNOW" else 0.55
sun = bpy.data.lights.new("sun", "SUN"); sun.energy = 2.0 if STATE != "PARK60" else 1.4; sun.angle = math.radians(0.5)
so = bpy.data.objects.new("sun", sun); ROOT.objects.link(so)
so.rotation_euler = (math.radians(40 if STATE == "PARKNOW" else 28), 0, math.radians(210))
if STATE == "PARK54": sun.color = (1.0, 0.75, 0.5)
elif STATE == "PARK60": sun.color = (1.0, 0.7, 0.48)
else: sun.color = (1.0, 0.9, 0.78)
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 48
sc.cycles.use_denoising = True; sc.cycles.max_bounces = 6
sc.render.resolution_x = 1920; sc.render.resolution_y = 1080
try: sc.view_settings.view_transform = "AgX"
except Exception: sc.view_settings.view_transform = "Filmic"
sc.unit_settings.system = "METRIC"
sc.view_settings.exposure = {"PARKNOW": 0.15, "PARK54": -0.2, "PARK60": 0.05}.get(STATE, -0.15)
if CAM.objects: sc.camera = list(CAM.objects)[0]

# save + write info
# r17i: horizon berm + Nishita aerosol — kill hard blue band where ground ends
try:
    for a_, v_ in (("dust_density", 5.0), ("aerosol_density", 6.5), ("air_density", 1.5)):
        try: setattr(sky, a_, v_)
        except Exception: pass
except Exception: pass
_berm = G.coll("G_HORIZON_FILL", ROOT)
# r17k: tall stepped berms — subway seal handles CP065; berms kill CP066/073 plane-edge band
box("horizon_berm_N", _berm, -1600, 1600, 400, 4000, -5, 40, M_grass)
box("horizon_berm_S", _berm, -1600, 1600, -4000, -1100, -55, -25, M_grass)
box("horizon_berm_S2", _berm, -2000, 2000, -5500, -3800, -30, 35, M_grass)
box("horizon_berm_E", _berm, 900, 3500, -3500, 3500, -50, 30, M_grass)
box("horizon_berm_W", _berm, -3500, -900, -3500, 3500, -50, 30, M_grass)
box("horizon_berm_far", _berm, -4500, 4500, -6500, 6500, -70, -55, M_grass)

bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
tri = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == "MESH")
info["objects"] = len(bpy.data.objects); info["faces"] = tri
info_path = os.path.splitext(OUT)[0] + "_info.json"
json.dump(info, open(info_path, "w"), indent=2)
print("BUILD_OK", OUT, "state", STATE, "objects", info["objects"], "faces", tri)
print("INFERENCES", *info["inferences"], sep="\n  ")
