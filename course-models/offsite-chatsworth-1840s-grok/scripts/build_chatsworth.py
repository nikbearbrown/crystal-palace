"""O-CHATS (CP003, CP004): Paxton's Chatsworth Great Conservatory (Great Stove) interior and the 1849-50
Victoria regia lily house. Feet. Great Stove origin at (0,0); lily house centred at (0,0) in its own collection
offset to x=200 so both live in one .blend. DEPARTURES CH01-."""
import bpy, sys, os, math, json, random
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grokkit as G
from grokkit import ft, Kit
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "/tmp/ch01.blend"
SEED = 1849; R = random.Random(SEED); sc = G.reset("CH_")
ROOT = G.coll("CHATSWORTH_CH01"); STOVE = G.coll("GREAT_STOVE", ROOT); LILY = G.coll("LILY_HOUSE", ROOT)
info = {}
M = dict(
    timber=G.mat("Timber", (0.42, 0.32, 0.20), 0.75), deal=G.mat("Deal", (0.55, 0.46, 0.32), 0.7),
    iron=G.mat("Iron", (0.07, 0.065, 0.055), 0.45, 0.35), paint=G.mat("WhitePaint", (0.62, 0.55, 0.42), 0.7),
    glass=G.mat_thin_glass("Glass", (0.72, 0.82, 0.78), 0.14),
    leaf=G.mat("Leaf", (0.10, 0.42, 0.12), 0.65, 0.0, ((0.05, 0.18, 0.04), 0.15)), leafu=G.mat("LeafUnder", (0.40, 0.50, 0.22), 0.55),
    rib=G.mat("LeafRib", (0.50, 0.45, 0.25), 0.55), water=G.mat("Water", (0.04, 0.20, 0.32), 0.04, 0, ((0.08, 0.28, 0.45), 0.55)),
    stone=G.mat("Stone", (0.55, 0.52, 0.46), 0.9), soil=G.mat("Soil", (0.25, 0.18, 0.10), 0.95),
    brick=G.mat("Brick", (0.48, 0.28, 0.18), 0.85), path=G.mat("Path", (0.40, 0.38, 0.32), 0.9),
    pot=G.mat("Terracotta", (0.55, 0.28, 0.14), 0.8), trunk=G.mat("Trunk", (0.28, 0.18, 0.10), 0.9),
    flower=G.mat("Flower", (0.70, 0.15, 0.25), 0.5), hat=G.mat("Hat", (0.08, 0.07, 0.06), 0.8),
    coat=G.mat("Coat", (0.18, 0.16, 0.14), 0.85), skin=G.mat("Skin", (0.62, 0.45, 0.35), 0.6),
    shirt=G.mat("Shirt", (0.75, 0.72, 0.66), 0.8), skirt=G.mat("Skirt", (0.25, 0.30, 0.45), 0.8),
    gold=G.mat("Gold", (0.55, 0.42, 0.15), 0.35, 0.7))
ML = list(M.values()); IX = {k: i for i, k in enumerate(M)}
def K(): return Kit(ML)
def I(k): return IX[k]

# ========== GREAT STOVE (277 x 123 x 67 ft) — CH01 ==========
# Plan: elliptical-ish rectangle, long axis Y. Curved laminated timber ribs span the width (X).
L, W, H = 277.0, 123.0, 67.0   # length (Y), width (X), height
HALF_X, HALF_Y = W / 2, L / 2
# floor + dwarf brick wall
gk = K(); gk.box(I("path"), -HALF_X - 2, HALF_X + 2, -HALF_Y - 2, HALF_Y + 2, -0.3, 0.0)
gk.box(I("brick"), -HALF_X - 1.2, HALF_X + 1.2, -HALF_Y - 1.2, HALF_Y + 1.2, 0, 4.0)
gk.box(I("path"), -HALF_X + 0.5, HALF_X - 0.5, -HALF_Y + 0.5, HALF_Y - 0.5, 3.9, 4.05)  # walk ledge
gk.done("CH_Stove_floor", STOVE)
# laminated ribs: arched across X, spaced ~12 ft along Y. Profile: rise to H at centre.
N_RIBS = 23; info["stove_ribs"] = N_RIBS
rk = K()
def arch_pts(n=18):
    pts = []
    for i in range(n + 1):
        t = i / n; x = -HALF_X + t * W
        # semicircle-ish: z = H * sqrt(1 - ((x)/(HALF_X*1.02))^2) roughly, but flatter crown
        u = (x / (HALF_X * 1.05)); z = max(4.5, H * math.sqrt(max(0, 1 - u * u)) * 0.98)
        pts.append((x, z))
    return pts
AP = arch_pts()
for ri in range(N_RIBS):
    y = -HALF_Y + 6 + ri * (L - 12) / (N_RIBS - 1)
    for (x0, z0), (x1, z1) in zip(AP, AP[1:]):
        rk.bar(I("timber"), (x0, y, z0), (x1, y, z1), 0.55, 1.1)   # laminated rib section ~6x13 in
    # ridge-and-furrow purlins between ribs (every other bay has a ridge)
    if ri < N_RIBS - 1:
        y2 = -HALF_Y + 6 + (ri + 1) * (L - 12) / (N_RIBS - 1)
        for (x, z) in AP[::2]:
            rk.bar(I("deal"), (x, y, z + 0.4), (x, y2, z + 0.4), 0.22, 0.18)
rk.done("CH_Stove_ribs", STOVE, part="rib")
# glazing panes between ribs (thin glass sheets following the arch, every 2nd bay for speed)
gk = K()
for ri in range(0, N_RIBS - 1, 2):
    y0 = -HALF_Y + 6 + ri * (L - 12) / (N_RIBS - 1)
    y1 = -HALF_Y + 6 + (ri + 1) * (L - 12) / (N_RIBS - 1)
    for (x0, z0), (x1, z1) in zip(AP, AP[1:]):
        gk.quad(I("glass"), [(x0, y0, z0 + 0.55), (x0, y1, z0 + 0.55), (x1, y1, z1 + 0.55), (x1, y0, z1 + 0.55)])
gk.done("CH_Stove_glass", STOVE, part="glass")
# end screens (glazed gables)
eg = K()
for y in (-HALF_Y, HALF_Y):
    for (x0, z0), (x1, z1) in zip(AP, AP[1:]):
        eg.bar(I("timber"), (x0, y, z0), (x1, y, z1), 0.35, 0.7)
        eg.quad(I("glass"), [(x0, y - 0.1, 4.1), (x1, y - 0.1, 4.1), (x1, y - 0.1, z1), (x0, y - 0.1, z0)])
eg.done("CH_Stove_ends", STOVE)
# tropical planting: pots + palm-ish trunks along the centre beds
pk = K(); info["plants"] = 0
for j in range(18):
    y = -HALF_Y + 18 + j * 14; x = R.choice([-18, -8, 8, 18]) * R.uniform(0.8, 1.1)
    h = R.uniform(8, 22); r = R.uniform(0.4, 0.9)
    pk.cyl(I("pot"), (x, y, 4.1), (x, y, 5.0), r * 1.3, 10, True, r * 1.1)
    pk.cyl(I("trunk"), (x, y, 5.0), (x + R.uniform(-0.5, 0.5), y + R.uniform(-0.3, 0.3), 5 + h), r * 0.35, 8)
    # fronds as simple bars
    for k in range(6):
        a = k * math.pi / 3; pk.bar(I("leaf"), (x, y, 5 + h), (x + 4 * math.cos(a), y + 4 * math.sin(a), 5 + h - 1.5), 0.15, 0.4)
    info["plants"] += 1
# underplanting boxes
for j in range(24):
    y = -HALF_Y + 12 + j * 11; x = R.uniform(-40, 40)
    pk.box(I("soil"), x - 2, x + 2, y - 1.2, y + 1.2, 4.05, 4.35)
    for _ in range(3):
        px, py = x + R.uniform(-1.5, 1.5), y + R.uniform(-0.8, 0.8)
        pk.cyl(I("leaf"), (px, py, 4.35), (px, py, 4.35 + R.uniform(1.5, 4)), 0.4, 6)
    info["plants"] += 1
pk.done("CH_Stove_plants", STOVE, part="plant")
# central path gravel
ck = K(); ck.box(I("path"), -6, 6, -HALF_Y + 4, HALF_Y - 4, 4.05, 4.12); ck.done("CH_Stove_path", STOVE)

# ========== LILY HOUSE at x=200 (61 x 49 ft, tank ~33 ft) — CH02 ==========
LX = 200.0; LW, LL, LH = 61.0, 49.0, 22.0; TD = 33.0
# floor, walls, ridge-and-furrow on hollow iron columns
lk = K()
lk.box(I("stone"), LX - LW / 2 - 1, LX + LW / 2 + 1, -LL / 2 - 1, LL / 2 + 1, -0.4, 0)
# perimeter dwarf wall (not a solid fill — cameras stand on the floor)
WT=1.0; WH=3.5
lk.box(I("brick"), LX - LW / 2, LX + LW / 2, -LL / 2, -LL / 2 + WT, 0, WH)
lk.box(I("brick"), LX - LW / 2, LX + LW / 2, LL / 2 - WT, LL / 2, 0, WH)
lk.box(I("brick"), LX - LW / 2, LX - LW / 2 + WT, -LL / 2 + WT, LL / 2 - WT, 0, WH)
lk.box(I("brick"), LX + LW / 2 - WT, LX + LW / 2, -LL / 2 + WT, LL / 2 - WT, 0, WH)
lk.box(I("path"), LX - LW / 2 + WT, LX + LW / 2 - WT, -LL / 2 + WT, LL / 2 - WT, -0.02, 0.02)
# columns on a 12 ft grid around the tank
cols = []; info["lily_columns"] = 0
for xi in range(-2, 3):
    for yi in range(-2, 3):
        if xi * xi + yi * yi == 0: continue
        x, y = LX + xi * 12, yi * 12
        if abs(x - LX) > LW / 2 - 2 or abs(y) > LL / 2 - 2: continue
        lk.cyl(I("iron"), (x, y, 0), (x, y, 16), 0.25, 10); cols.append((x, y)); info["lily_columns"] += 1
lk.done("CH_Lily_shell", LILY)
# ridge-and-furrow roof: ridges every 8 ft along X, spanning Y
rf = K(); gl = K()
for i, x in enumerate([LX + k * 8 for k in range(-3, 4)]):
    # ridge beam
    z_r = 18.5 if i % 2 == 0 else 16.8   # alternate ridge / furrow heights
    rf.bar(I("deal"), (x, -LL / 2 + 1, z_r), (x, LL / 2 - 1, z_r), 0.2, 0.35)
for i in range(-3, 3):
    x0 = LX + i * 8; x1 = LX + (i + 1) * 8; zr0 = 18.5 if i % 2 == 0 else 16.8; zr1 = 18.5 if (i + 1) % 2 == 0 else 16.8
    # sash bars across
    for yi in range(-6, 7):
        y = yi * 3.5; rf.bar(I("deal"), (x0, y, zr0), (x1, y, zr1), 0.1, 0.12)
    gl.quad(I("glass"), [(x0, -LL / 2 + 1.5, zr0 + 0.1), (x0, LL / 2 - 1.5, zr0 + 0.1), (x1, LL / 2 - 1.5, zr1 + 0.1), (x1, -LL / 2 + 1.5, zr1 + 0.1)])
rf.done("CH_Lily_roof_bars", LILY); gl.done("CH_Lily_glass", LILY)
# circular tank
tk = K(); info["tank_d_ft"] = TD
# ring wall
seg = 32
for j in range(seg):
    a0 = 2 * math.pi * j / seg; a1 = 2 * math.pi * (j + 1) / seg
    x0, y0 = LX + (TD / 2) * math.cos(a0), (TD / 2) * math.sin(a0)
    x1, y1 = LX + (TD / 2) * math.cos(a1), (TD / 2) * math.sin(a1)
    tk.box(I("stone"), min(x0, x1) - 0.3, max(x0, x1) + 0.3, min(y0, y1) - 0.3, max(y0, y1) + 0.3, 0, 2.4)
tk.cyl(I("water"), (LX, 0, 0.3), (LX, 0, 2.0), TD / 2 - 0.4, 48, True)
tk.cyl(I("stone"), (LX, 0, -0.5), (LX, 0, 0.3), TD / 2 - 0.2, 32, True)
tk.done("CH_Lily_tank", LILY, part="tank")

# Victoria regia pads — CH03
def pad_mesh(name, coll, x, y, z, radius, rz=0, underside=False, flower=False):
    """giant lily pad: upturned rim, radial + cross ribs on underside"""
    k = K(); n = 24; n_rib = 12
    # top surface slightly domed, rim upturned
    for j in range(n):
        a0 = 2 * math.pi * j / n; a1 = 2 * math.pi * (j + 1) / n
        for ring in range(4):
            r0 = radius * ring / 4; r1 = radius * (ring + 1) / 4
            z0 = z + 0.08 * (1 - (r0 / radius) ** 2); z1 = z + 0.08 * (1 - (r1 / radius) ** 2)
            if ring == 3: z1 = z + 0.35   # upturned rim
            k.quad(I("leafu" if underside else "leaf"), [
                (x + r0 * math.cos(a0), y + r0 * math.sin(a0), z0),
                (x + r0 * math.cos(a1), y + r0 * math.sin(a1), z0),
                (x + r1 * math.cos(a1), y + r1 * math.sin(a1), z1),
                (x + r1 * math.cos(a0), y + r1 * math.sin(a0), z1)])
    # underside ribs (radial + concentric cross)
    if underside or True:
        for j in range(n_rib):
            a = 2 * math.pi * j / n_rib
            k.bar(I("rib"), (x, y, z - 0.05), (x + (radius - 0.3) * math.cos(a), y + (radius - 0.3) * math.sin(a), z - 0.05 + (0.25 if False else 0)), 0.12, 0.18)
        for rr in (radius * 0.35, radius * 0.65, radius * 0.88):
            for j in range(n):
                a0 = 2 * math.pi * j / n; a1 = 2 * math.pi * (j + 1) / n
                k.bar(I("rib"), (x + rr * math.cos(a0), y + rr * math.sin(a0), z - 0.06),
                      (x + rr * math.cos(a1), y + rr * math.sin(a1), z - 0.06), 0.08, 0.1)
    if flower:
        k.cyl(I("flower"), (x, y, z + 0.05), (x, y, z + 0.7), 0.5, 12, True, 0.15)
    return k.done(name, coll, x=0, y=0, z=0, rz=rz, part="pad")

info["pads"] = 0
PAD_POS = [(-8, -4, 2.8), (6, 5, 2.7), (-3, 9, 2.85), (10, -7, 2.75), (-11, 6, 2.7), (2, -10, 2.8), (8, 10, 2.75), (-6, -11, 2.7), (0, 2, 2.85), (4, -2, 2.8)]
for i, (dx, dy, zz) in enumerate(PAD_POS):
    pad_mesh(f"CH_Pad_{i}", LILY, LX + dx, dy, zz, R.uniform(3.8, 5.2), R.uniform(0, 6), flower=(i % 3 == 0))
    info["pads"] += 1
# turned-over leaf on a trestle for the underside + learning shot — CH04
tr = K(); TX, TY, TZ = LX + 5, 6.5, 0
tr.box(I("deal"), TX - 2, TX + 2, TY - 0.8, TY + 0.8, TZ + 2.8, TZ + 3.0)
tr.cyl(I("deal"), (TX - 1.6, TY - 0.5, 0), (TX - 1.6, TY - 0.5, 2.8), 0.12, 8)
tr.cyl(I("deal"), (TX + 1.6, TY - 0.5, 0), (TX + 1.6, TY - 0.5, 2.8), 0.12, 8)
tr.cyl(I("deal"), (TX - 1.6, TY + 0.5, 0), (TX - 1.6, TY + 0.5, 2.8), 0.12, 8)
tr.cyl(I("deal"), (TX + 1.6, TY + 0.5, 0), (TX + 1.6, TY + 0.5, 2.8), 0.12, 8)
tr.done("CH_Trestle", LILY)
# underside leaf: flipped (ribs up), slightly tilted
uk = K(); ur = 4.6; n = 24; n_rib = 14; ux, uy, uz = TX, TY, TZ + 3.15
for j in range(n):
    a0 = 2 * math.pi * j / n; a1 = 2 * math.pi * (j + 1) / n
    for ring in range(4):
        r0 = ur * ring / 4; r1 = ur * (ring + 1) / 4
        z0 = uz - 0.06 * (1 - (r0 / ur) ** 2); z1 = uz - 0.06 * (1 - (r1 / ur) ** 2)
        if ring == 3: z1 = uz - 0.3
        uk.quad(I("leafu"), [(ux + r0 * math.cos(a0), uy + r0 * math.sin(a0), z0), (ux + r0 * math.cos(a1), uy + r0 * math.sin(a1), z0),
                             (ux + r1 * math.cos(a1), uy + r1 * math.sin(a1), z1), (ux + r1 * math.cos(a0), uy + r1 * math.sin(a0), z1)])
for j in range(n_rib):
    a = 2 * math.pi * j / n_rib
    uk.bar(I("rib"), (ux, uy, uz + 0.08), (ux + (ur - 0.25) * math.cos(a), uy + (ur - 0.25) * math.sin(a), uz + 0.05), 0.14, 0.22)
for rr in (ur * 0.3, ur * 0.55, ur * 0.8):
    for j in range(n):
        a0 = 2 * math.pi * j / n; a1 = 2 * math.pi * (j + 1) / n
        uk.bar(I("rib"), (ux + rr * math.cos(a0), uy + rr * math.sin(a0), uz + 0.06),
               (ux + rr * math.cos(a1), uy + rr * math.sin(a1), uz + 0.06), 0.09, 0.12)
uk.done("CH_UndersideLeaf", LILY, part="underside"); info["underside_leaf"] = 1

# ========== figures ==========
FIG = G.coll("CH_FIGURES", ROOT)
fm_m = [M["coat"], M["coat"], M["skin"], M["hat"], M["shirt"]]
fm_w = [M["skirt"], M["skirt"], M["skin"], M["hat"], M["shirt"]]
me_m = G.pm("man", fm_m, {"hat": "top", "cravat": True}, "gent")
me_w = G.pm("woman", fm_w, {"hat": "low", "frock": True}, "lady")
me_lab = G.pm("man", [G.mat("LabCoat", (0.35, 0.32, 0.25), 0.9), G.mat("LabTr", (0.25, 0.22, 0.18), 0.9), M["skin"], G.mat("Cap", (0.15, 0.12, 0.08), 0.8), M["shirt"]], {"hat": "cap"}, "lab")
info["figures"] = 0
# stove: Paxton + visitors
for name, me, x, y, z, look in [
    ("CH_Paxton_stove", me_lab, -4, -40, 4.1, (0, 20)),
    ("CH_Visitor_m1", me_m, 8, -30, 4.1, (-5, 15)),
    ("CH_Visitor_w1", me_w, 10, -28, 4.1, (-5, 15)),
    ("CH_Gardener", me_lab, -22, 10, 4.1, (5, 0))]:
    G.person(FIG, name, me, x, y, z, G.heading(look[0] - x, look[1] - y), R); info["figures"] += 1
# lily house
for name, me, x, y, z, look in [
    ("CH_Paxton_lily", me_lab, LX - 8, -14, 0, (LX, 0)),
    ("CH_Visitor_lily_m", me_m, LX + 12, -10, 0, (LX, 2)),
    ("CH_Visitor_lily_w", me_w, LX + 14, -9, 0, (LX, 2)),
    ("CH_Boy_lily", G.pm("boy", fm_m, {"hat": "cap"}, "boy"), LX + 6, -16, 0, (LX + 5, 6))]:
    G.person(FIG, name, me, x, y, z, G.heading(look[0] - x, look[1] - y), R); info["figures"] += 1

# ========== cameras: stove at origin, lily cams offset ==========
# rewrite route positions for lily shots (add LX)
route_path = os.path.join(HERE, "..", "route", "camera_route.json")
route = json.load(open(route_path))
for s in route["shots"]:
    if s["id"].startswith("CP004"):
        for key in ("start", "end"):
            if key in s:
                s[key]["pos_ft"][0] += LX; s[key]["look_ft"][0] += LX
tmp = "/tmp/ch_route.json"; json.dump(route, open(tmp, "w"))
CAMS = G.coll("CAMERAS"); G.cameras(tmp, CAMS)
# CH03: warmer glasshouse light, less bleach; lily tank soft fill
G.world_sky(elev=38, rot=150, strength=0.28, sun_energy=2.2, sun_rot=(48, 0, 25), sun_col=(1.0, 0.88, 0.72), haze=(1.2, 0.45))
G.render_settings(exposure=-0.15)
fill = bpy.data.lights.new("CH_LilyFill", "AREA"); fill.energy = 180; fill.size = 18; fill.color = (1.0, 0.95, 0.85)
fo = bpy.data.objects.new("CH_LilyFill", fill); fo.location = (LX, 0, 14); LILY.objects.link(fo)
G.save(OUT, info, "O-CHATS ch01", SEED)
