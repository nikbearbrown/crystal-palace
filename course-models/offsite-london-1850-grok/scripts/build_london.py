"""O-INDUSTRY (CP002) + O-ROOM (CP005): c.1850 railway lane with factory/chimneys/terraces, and a London
planning room for 1849-50 with plans, samples and the commission table. Industry at origin; room at x=300.
DEPARTURES LN01-."""
import bpy, sys, os, math, json, random
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grokkit as G
from grokkit import ft, Kit
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "/tmp/ln01.blend"
SEED = 1850; R = random.Random(SEED); sc = G.reset("LN_")
ROOT = G.coll("LONDON_LN01"); IND = G.coll("INDUSTRY", ROOT); ROOM = G.coll("PLANNING_ROOM", ROOT)
info = {}; TEX = os.path.join(HERE, "..", "textures")
M = dict(
    brick=G.mat("Brick", (0.34, 0.16, 0.10), 0.92), brickd=G.mat("BrickDark", (0.18, 0.09, 0.06), 0.93),
    stone=G.mat("Stone", (0.38, 0.36, 0.32), 0.88), iron=G.mat("Iron", (0.06, 0.06, 0.07), 0.45, 0.5),
    soot=G.mat("Soot", (0.035, 0.035, 0.035), 0.97), slate=G.mat("Slate", (0.12, 0.13, 0.15), 0.75),
    cobble=G.mat("Cobble", (0.35, 0.33, 0.30), 0.95), mud=G.mat("Mud", (0.28, 0.22, 0.14), 0.95),
    wood=G.mat("Wood", (0.40, 0.28, 0.16), 0.8), paint=G.mat("Paint", (0.70, 0.68, 0.60), 0.7),
    glass=G.mat_thin_glass("Glass", (0.75, 0.82, 0.85), 0.15),
    smoke=G.mat("Smoke", (0.42, 0.42, 0.40), 0.95, 0, ((0.55, 0.55, 0.52), 0.45), alpha=0.42),
    plaster=G.mat("Plaster", (0.78, 0.74, 0.66), 0.9), carpet=G.mat("Carpet", (0.35, 0.12, 0.10), 0.95),
    oak=G.mat("Oak", (0.38, 0.26, 0.14), 0.65), paper=G.mat("Paper", (0.85, 0.82, 0.72), 0.9),
    brass=G.mat("Brass", (0.55, 0.42, 0.18), 0.35, 0.7), cloth=G.mat("Cloth", (0.20, 0.22, 0.35), 0.9),
    coat=G.mat("Coat", (0.14, 0.12, 0.12), 0.85), skin=G.mat("Skin", (0.62, 0.45, 0.35), 0.6),
    hat=G.mat("Hat", (0.06, 0.05, 0.05), 0.8), shirt=G.mat("Shirt", (0.78, 0.75, 0.68), 0.8),
    skirt=G.mat("Skirt", (0.30, 0.18, 0.22), 0.85), water=G.mat("Water", (0.15, 0.20, 0.22), 0.2))
# plan textures
for nm in ("plan_nave", "elev_south", "detail_gutter", "colour_oj"):
    M[nm] = G.mat_image(nm, os.path.join(TEX, nm + ".png"), 0.85)
ML = list(M.values()); IX = {k: i for i, k in enumerate(M)}
def K(): return Kit(ML)
def I(k): return IX[k]

# ========== INDUSTRY ==========
# ground
gk = K(); gk.box(I("mud"), -60, 160, -60, 80, -0.5, 0); gk.box(I("cobble"), -20, 140, -8, 18, -0.05, 0.05)
gk.done("LN_Ground", IND)
# viaduct along Y~0, arches spanning X, deck at z=28
vk = K(); info["viaduct_arches"] = 0; ARCH_W, ARCH_H, DECK = 16.0, 22.0, 28.0
for i in range(8):
    x0 = -10 + i * ARCH_W
    # piers
    vk.box(I("brick"), x0 - 1.5, x0 + 1.5, -6, 6, 0, DECK)
    vk.box(I("brick"), x0 + ARCH_W - 1.5, x0 + ARCH_W + 1.5, -6, 6, 0, DECK)
    # arch ring (approx with bars)
    for j in range(10):
        a0 = math.pi * j / 10; a1 = math.pi * (j + 1) / 10
        cx = x0 + ARCH_W / 2
        p0 = (cx + (ARCH_W / 2 - 1) * math.cos(a0), 0, 4 + (ARCH_H - 4) * math.sin(a0))
        p1 = (cx + (ARCH_W / 2 - 1) * math.cos(a1), 0, 4 + (ARCH_H - 4) * math.sin(a1))
        vk.bar(I("brick"), (p0[0], -5, p0[2]), (p1[0], -5, p1[2]), 1.2, 1.5)
        vk.bar(I("brick"), (p0[0], 5, p0[2]), (p1[0], 5, p1[2]), 1.2, 1.5)
    # spandrel fill
    vk.box(I("brick"), x0 + 1.5, x0 + ARCH_W - 1.5, -6, 6, ARCH_H, DECK)
    # LN02: fill black arch voids — soot rear wall + brick wing walls so arches read as tunnels, not holes
    cx = x0 + ARCH_W / 2
    vk.box(I("soot"), x0 + 2.0, x0 + ARCH_W - 2.0, -5.2, -4.6, 0.2, ARCH_H - 0.5)
    vk.box(I("brickd"), x0 + 1.6, x0 + 2.4, -5.5, 5.5, 0.0, ARCH_H - 0.2)
    vk.box(I("brickd"), x0 + ARCH_W - 2.4, x0 + ARCH_W - 1.6, -5.5, 5.5, 0.0, ARCH_H - 0.2)
    info["viaduct_arches"] += 1
vk.box(I("stone"), -12, -10 + 8 * ARCH_W + 2, -7, 7, DECK, DECK + 1.5)  # parapet deck
vk.box(I("iron"), -12, -10 + 8 * ARCH_W + 2, -1.5, 1.5, DECK + 1.5, DECK + 1.7)  # rails
vk.done("LN_Viaduct", IND)
# train on the deck
tk = K()
for i, dx in enumerate(range(0, 70, 14)):
    x = 20 + dx
    tk.box(I("soot" if i else "iron"), x, x + 12, -3.5, 3.5, DECK + 1.7, DECK + 1.7 + (5.5 if i else 7))
    if i == 0:  # loco chimney
        tk.cyl(I("soot"), (x + 3, 0, DECK + 8.7), (x + 3, 0, DECK + 14), 0.6, 10)
        tk.box(I("iron"), x + 8, x + 11, -2, 2, DECK + 7, DECK + 10)  # cab
        for s in range(7):  # LN03: denser train smoke plume downwind
            tk.cyl(I("smoke"), (x + 3 + s * 2.2, s * 0.4, DECK + 14 + s * 2.8),
                   (x + 4 + s * 2.2, s * 0.4, DECK + 17 + s * 2.8), 1.4 + s * 0.55, 8, True, 2.0 + s * 0.7)
    for wy in (-2.2, 2.2):
        for wx in (x + 2, x + 10):
            tk.cyl(I("iron"), (wx, wy - 0.3, DECK + 1.7), (wx, wy + 0.3, DECK + 1.7), 1.1, 12)
tk.done("LN_Train", IND); info["train"] = 1
# factory block + chimneys
fk = K(); info["chimneys"] = 0
fk.box(I("brickd"), 70, 130, 10, 55, 0, 32)
fk.box(I("slate"), 68, 132, 8, 57, 32, 34)
for (cx, cy, h) in [(85, 20, 55), (105, 40, 70), (120, 25, 48)]:
    fk.cyl(I("brickd"), (cx, cy, 32), (cx, cy, h), 3.5, 14)
    fk.cyl(I("brick"), (cx, cy, h), (cx, cy, h + 4), 3.8, 14, True, 3.2)
    # smoke plume (stacked translucent spheres via cyls)
    for s in range(5):
        fk.cyl(I("smoke"), (cx + s * 1.5, cy + s * 0.8, h + 4 + s * 4), (cx + s * 1.5 + 1, cy + s * 0.8, h + 8 + s * 4), 2.5 + s * 0.8, 8, True, 3.5 + s)
    info["chimneys"] += 1
# factory windows
for yi in range(3):
    for xi in range(6):
        fk.box(I("glass"), 72 + xi * 9, 72 + xi * 9 + 5, 10.05, 10.15, 6 + yi * 8, 6 + yi * 8 + 5)
fk.done("LN_Factory", IND)
# terraced housing under/beside the viaduct
hk = K(); info["terraces"] = 0
for i in range(12):
    x = -5 + i * 14; depth = 18; h = 22 + (i % 3) * 2
    hk.box(I("brick"), x, x + 12, 22, 22 + depth, 0, h)
    hk.box(I("slate"), x - 0.5, x + 12.5, 21.5, 22 + depth + 0.5, h, h + 3)
    # windows + door
    hk.box(I("wood"), x + 4.5, x + 7.5, 21.95, 22.05, 0, 7)
    for wy in (9, 15):
        hk.box(I("glass"), x + 2, x + 5, 21.95, 22.05, wy, wy + 4)
        hk.box(I("glass"), x + 7, x + 10, 21.95, 22.05, wy, wy + 4)
    info["terraces"] += 1
hk.done("LN_Terraces", IND)
# street figures + carts
FIG = G.coll("LN_FIGURES", ROOT)
fm = [M["coat"], M["coat"], M["skin"], M["hat"], M["shirt"]]
fw = [M["skirt"], M["skirt"], M["skin"], M["hat"], M["shirt"]]
me_m = G.pm("man", fm, {"hat": "top"}, "m"); me_w = G.pm("woman", fw, {"hat": "low", "frock": True}, "w")
me_lab = G.pm("man", [G.mat("Lab", (0.35, 0.30, 0.22), 0.9), G.mat("Lab2", (0.25, 0.22, 0.18), 0.9), M["skin"], G.mat("Cap", (0.12, 0.10, 0.08), 0.8), M["shirt"]], {"hat": "cap"}, "lab")
info["figures"] = 0
for i, (x, y, me) in enumerate([(5, 5, me_lab), (15, 10, me_m), (25, 6, me_w), (35, 12, me_m), (45, 4, me_lab), (8, -15, me_m), (60, 0, me_w), (70, -5, me_lab)]):
    G.person(FIG, f"LN_Street_{i}", me, x, y, 0, G.heading(1, 0.2), R); info["figures"] += 1
# cart
ck = K(); ck.box(I("wood"), 40, 50, -18, -12, 2.5, 6); ck.box(I("wood"), 41, 49, -17.5, -12.5, 6, 9)
for wx, wy in [(42, -13), (48, -13), (42, -17), (48, -17)]:
    ck.cyl(I("iron"), (wx, wy - 0.3, 1.5), (wx, wy + 0.3, 1.5), 1.5, 12)
ck.done("LN_Cart", IND)

# ========== PLANNING ROOM at x=300 ==========
RX = 300.0
rk = K()
# Georgian room 28 x 22 x 12 ft
rk.box(I("oak"), RX - 14, RX + 14, -11, 11, -0.2, 0)          # floor
rk.box(I("carpet"), RX - 10, RX + 10, -7, 7, 0, 0.05)
rk.box(I("plaster"), RX - 14, RX + 14, -11.15, -11, 0, 12)     # walls
rk.box(I("plaster"), RX - 14, RX + 14, 11, 11.15, 0, 12)
rk.box(I("plaster"), RX - 14.15, RX - 14, -11, 11, 0, 12)
rk.box(I("plaster"), RX + 14, RX + 14.15, -11, 11, 0, 12)
rk.box(I("plaster"), RX - 14, RX + 14, -11, 11, 12, 12.3)      # ceiling
# skirting + cornice
rk.box(I("oak"), RX - 14, RX + 14, -11.05, -10.85, 0, 0.7)
rk.box(I("oak"), RX - 14, RX + 14, 10.85, 11.05, 0, 0.7)
# windows on +y wall
for wx in (-8, 0, 8):
    rk.box(I("glass"), RX + wx - 2.5, RX + wx + 2.5, 11.0, 11.2, 3.5, 9.5)
    rk.box(I("oak"), RX + wx - 2.7, RX + wx + 2.7, 10.9, 11.05, 3.3, 9.7)
rk.done("LN_Room_shell", ROOM)
# commission table
tk = K(); tk.box(I("oak"), RX - 5, RX + 5, -3, 3, 2.55, 2.75)
for lx, ly in [(-4.5, -2.5), (4.5, -2.5), (-4.5, 2.5), (4.5, 2.5)]:
    tk.cyl(I("oak"), (RX + lx, ly, 0), (RX + lx, ly, 2.55), 0.2, 8)
tk.done("LN_CommissionTable", ROOM); info["table"] = 1
# chairs
for i, (dx, dy, rz) in enumerate([(-3, -4.5, 0), (0, -4.5, 0), (3, -4.5, 0), (-3, 4.5, math.pi), (0, 4.5, math.pi), (3, 4.5, math.pi), (-6.5, 0, math.pi / 2), (6.5, 0, -math.pi / 2)]):
    ck = K(); ck.box(I("oak"), -0.9, 0.9, -0.9, 0.9, 1.4, 1.55); ck.box(I("cloth"), -0.85, 0.85, -0.85, 0.85, 1.55, 1.65)
    ck.box(I("oak"), -0.9, 0.9, 0.7, 0.9, 1.55, 3.2)
    for a, b in [(-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)]: ck.cyl(I("oak"), (a, b, 0), (a, b, 1.4), 0.1, 6)
    ck.done(f"LN_Chair_{i}", ROOM, RX + dx, dy, 0, rz)
# plan sheets on table + walls
info["plans"] = 0
for i, (nm, dx, dy, dz, sx, sy) in enumerate([
    ("plan_nave", -2.5, -0.5, 2.78, 3.2, 2.4), ("elev_south", 1.5, 0.8, 2.78, 3.0, 2.2),
    ("detail_gutter", -1.0, 1.5, 2.78, 2.2, 1.6), ("colour_oj", 3.0, -1.2, 2.78, 2.4, 1.8)]):
    pk = Kit([M[nm]]); pk.quad(0, [(RX + dx - sx / 2, dy - sy / 2, dz), (RX + dx + sx / 2, dy - sy / 2, dz), (RX + dx + sx / 2, dy + sy / 2, dz), (RX + dx - sx / 2, dy + sy / 2, dz)])
    pk.done(f"LN_Plan_{i}", ROOM); info["plans"] += 1
# wall-hung plans
for i, (nm, x, z) in enumerate([("plan_nave", RX - 13.9, 5), ("elev_south", RX + 13.9, 5)]):
    pk = Kit([M[nm]])
    if i == 0: pk.quad(0, [(x, -4, z), (x, 4, z), (x, 4, z + 5), (x, -4, z + 5)])
    else: pk.quad(0, [(x, 4, z), (x, -4, z), (x, -4, z + 5), (x, 4, z + 5)])
    pk.done(f"LN_WallPlan_{i}", ROOM); info["plans"] += 1
# samples: glass pane, sash bar length, column section
info["samples"] = 0
sk = K()
sk.box(I("glass"), RX + 0.5, RX + 3.5, 1.5, 1.55, 2.78, 4.5); info["samples"] += 1   # glass sample standing
sk.bar(I("wood"), (RX - 3.5, 2.0, 2.9), (RX - 0.5, 2.0, 2.9), 0.15, 0.2); info["samples"] += 1  # sash bar
# column sample (short hollow cylinder with OJ paint suggestion)
sk.cyl(I("iron"), (RX + 4.5, -1.5, 2.78), (RX + 4.5, -1.5, 5.0), 0.35, 12, True, 0.28); info["samples"] += 1
sk.box(I("brass"), RX + 4.2, RX + 4.8, -1.8, -1.2, 2.75, 2.78)  # base plate
sk.done("LN_Samples", ROOM)
# fireplace
fk = K(); fk.box(I("stone"), RX - 3, RX + 3, -11.0, -10.3, 0, 5.5); fk.box(I("soot"), RX - 1.5, RX + 1.5, -10.5, -10.3, 0.5, 3.5)
fk.box(I("brass"), RX - 3.2, RX + 3.2, -10.4, -10.2, 5.3, 5.7); fk.done("LN_Fireplace", ROOM)
# bookshelf
bk = K(); bk.box(I("oak"), RX - 13.8, RX - 11.5, -8, 2, 0, 9)
for sh in range(5): bk.box(I("oak"), RX - 13.7, RX - 11.6, -7.9, 1.9, 1.5 + sh * 1.5, 1.6 + sh * 1.5)
bk.done("LN_Bookshelf", ROOM)
# room figures: commissioners
for i, (dx, dy, me, hx, hy) in enumerate([
    (-2, -5.5, me_m, 0, 1), (1, -5.5, me_m, 0, 1), (4, 5.2, me_m, 0, -1),
    (-5, 1, me_m, 1, 0), (8, -2, me_lab, -1, 0.3)]):
    G.person(FIG, f"LN_Comm_{i}", me, RX + dx, dy, 0, G.heading(hx, hy), R); info["figures"] += 1

# cameras with room offset
route_path = os.path.join(HERE, "..", "route", "camera_route.json")
route = json.load(open(route_path))
for s in route["shots"]:
    if s["id"].startswith("CP005"):
        for key in ("start", "end"):
            if key in s:
                s[key]["pos_ft"][0] += RX; s[key]["look_ft"][0] += RX
tmp = "/tmp/ln_route.json"; json.dump(route, open(tmp, "w"))
CAMS = G.coll("CAMERAS"); G.cameras(tmp, CAMS)
G.world_sky(elev=26, rot=200, strength=0.18, sun_energy=1.6, sun_rot=(58, 0, -40), sun_col=(1.0, 0.82, 0.62), haze=(1.8, 0.75))
# room needs interior light
G.point("LN_RoomLamp", (RX, 0, 10), 400, (1.0, 0.92, 0.8), 1.5, 'AREA')
G.render_settings(exposure=-0.1)
G.save(OUT, info, "O-LONDON ln01", SEED)
