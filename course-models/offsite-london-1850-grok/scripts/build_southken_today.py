"""CP069 — A second legacy elsewhere in London. Present-day South Kensington block-out:
Exhibition Road, Royal Albert Hall, museum fronts (bought with 1851 profits). OPTIONAL —
real footage may replace. Lean geometry only.
  blender -b --factory-startup -P scripts/build_southken_today.py -- --out rounds/ln03_southken.blend
"""
import bpy, sys, os, math, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grokkit as G
from grokkit import Kit
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/ln03_southken.blend"
SEED = 2026; R = random.Random(SEED); sc = G.reset("SK_")
ROOT = G.coll("SOUTHKEN_TODAY"); STREET = G.coll("EXHIBITION_ROAD", ROOT)
RAH = G.coll("ROYAL_ALBERT_HALL", ROOT); MUS = G.coll("MUSEUMS", ROOT)
info = {"scene": "CP069", "state": "today", "optional": True,
        "note": "w02: RAH frieze/windows/iron balcony/lantern; museum frames; street iron dressing; real footage may still replace"}

M = dict(
    asphalt=G.mat("Asphalt", (0.18, 0.18, 0.17), 0.92),
    pavement=G.mat("Pavement", (0.55, 0.52, 0.48), 0.88),
    brick=G.mat("BrickRed", (0.42, 0.22, 0.14), 0.9),
    terracotta=G.mat("Terracotta", (0.48, 0.28, 0.16), 0.85),
    stone=G.mat("StonePale", (0.62, 0.58, 0.52), 0.82),
    stone_d=G.mat("StoneDark", (0.35, 0.33, 0.30), 0.85),
    dome=G.mat("DomeLead", (0.22, 0.24, 0.22), 0.55, 0.3),
    glass=G.mat_thin_glass("Glass", (0.70, 0.78, 0.82), 0.12),
    grass=G.mat("Grass", (0.14, 0.28, 0.10), 0.95),
    iron=G.mat("IronRail", (0.08, 0.08, 0.09), 0.5, 0.5),
    slate=G.mat("Slate", (0.16, 0.17, 0.18), 0.75),
)
ML = list(M.values()); IX = {k: i for i, k in enumerate(M)}
def K(): return Kit(ML)
def I(k): return IX[k]

# Units: feet (same as rest of london set). Origin at Exhibition Road / Prince Consort Rd approx.
# +Y = north along Exhibition Road; +X = east toward Albert Hall / Hyde Park.

# ---- Exhibition Road ----
gk = K()
gk.box(I("asphalt"), -18, 18, -200, 220, -0.4, 0.0)          # carriageway
gk.box(I("pavement"), -32, -18, -200, 220, -0.05, 0.08)      # W pavement (museums)
gk.box(I("pavement"), 18, 36, -200, 220, -0.05, 0.08)        # E pavement
gk.done("SK_Road", STREET)

# street trees — multi-lobe canopy + iron tree guards (w02 polish)
for i, y in enumerate(range(-180, 200, 40)):
    for x in (-26, 28):
        tk = K()
        tk.cyl(I("stone_d"), (x, y, 0.1), (x, y, 14), 0.55, 10)
        # layered canopy lobes (not a single cone)
        for j, (dx, dy, h0, h1, r0, r1) in enumerate((
            (0, 0, 12, 22, 4.2, 1.2), (2.2, 1.0, 14, 20, 3.0, 0.8),
            (-2.0, -1.2, 13, 19, 2.8, 0.7), (0.5, -2.0, 15, 21, 2.5, 0.6),
        )):
            tk.cyl(I("grass"), (x + dx, y + dy, h0), (x + dx, y + dy, h1), r0, 12, True, r1)
        # iron tree-guard cage
        for a in range(0, 360, 45):
            import math as _m
            rr = 1.6; ax = x + rr * _m.cos(_m.radians(a)); ay = y + rr * _m.sin(_m.radians(a))
            tk.cyl(I("iron"), (ax, ay, 0.05), (ax, ay, 3.2), 0.06, 6)
        tk.cyl(I("iron"), (x, y, 3.1), (x, y, 3.25), 1.65, 16, True, 1.55)
        tk.done(f"SK_Tree_{i}_{x}", STREET)

# ---- Royal Albert Hall — w02: frieze band, window ring, iron balcony, glazed lantern ----
CX, CY = 95.0, 90.0
rk = K()
rk.box(I("stone"), CX - 130, CX + 130, CY - 150, CY + 150, 0.0, 3.5)   # podium
# amphitheatre body with slight entasis feel via two stacked rings
rk.cyl(I("terracotta"), (CX, CY, 3.5), (CX, CY, 28), 110, 36, True, 110)
rk.cyl(I("terracotta"), (CX, CY, 28), (CX, CY, 48), 110, 36, True, 108)
# mosaic frieze band (darker stone strip)
rk.cyl(I("stone_d"), (CX, CY, 40), (CX, CY, 46), 111.2, 36, True, 111.2)
# cornice + attic
rk.cyl(I("stone"), (CX, CY, 48), (CX, CY, 52), 112, 36, True, 108)
rk.cyl(I("stone"), (CX, CY, 52), (CX, CY, 58), 108, 32, True, 100)
# arched window recesses around the drum (shallow glass + iron mullions)
import math as _m
for i in range(36):
    a = _m.radians(i * 10 + 5)
    wx = CX + 109.2 * _m.cos(a); wy = CY + 109.2 * _m.sin(a)
    # outward normal box for glass
    nx, ny = _m.cos(a), _m.sin(a)
    for floor_z in (8.0, 18.0, 30.0):
        xa, xb = sorted([wx - 1.8 * ny - 0.3 * nx, wx + 1.8 * ny + 0.15 * nx])
        ya, yb = sorted([wy + 1.8 * nx - 0.3 * ny, wy - 1.8 * nx + 0.15 * ny])
        # thin radial thickness along normal
        xa2, xb2 = sorted([wx - 0.2 * nx, wx + 0.35 * nx])
        ya2, yb2 = sorted([wy - 0.2 * ny, wy + 0.35 * ny])
        # glass as small radial slab
        rk.box(I("glass"),
               min(wx - 1.6 * abs(ny) - 0.15 * abs(nx), wx + 1.6 * abs(ny) + 0.15 * abs(nx)),
               max(wx - 1.6 * abs(ny) - 0.15 * abs(nx), wx + 1.6 * abs(ny) + 0.15 * abs(nx)),
               min(wy - 1.6 * abs(nx) - 0.15 * abs(ny), wy + 1.6 * abs(nx) + 0.15 * abs(ny)),
               max(wy - 1.6 * abs(nx) - 0.15 * abs(ny), wy + 1.6 * abs(nx) + 0.15 * abs(ny)),
               floor_z, floor_z + 6.5)
        rk.cyl(I("iron"), (wx + 0.25 * nx, wy + 0.25 * ny, floor_z),
               (wx + 0.25 * nx, wy + 0.25 * ny, floor_z + 6.5), 0.08, 6)
# iron balcony rail at podium edge (camera-facing SW arc)
for i in range(20):
    a0 = _m.radians(200 + i * 4); a1 = _m.radians(200 + (i + 1) * 4)
    for a in (a0, a1):
        px = CX + 118 * _m.cos(a); py = CY + 118 * _m.sin(a)
        rk.cyl(I("iron"), (px, py, 3.5), (px, py, 6.0), 0.07, 6)
    # rail top
    x0, y0 = CX + 118 * _m.cos(a0), CY + 118 * _m.sin(a0)
    x1, y1 = CX + 118 * _m.cos(a1), CY + 118 * _m.sin(a1)
    rk.cyl(I("iron"), (x0, y0, 5.9), (x1, y1, 5.9), 0.06, 6)
# dome tiers + glazed lantern
rk.cyl(I("dome"), (CX, CY, 58), (CX, CY, 95), 95, 28, True, 70)
rk.cyl(I("dome"), (CX, CY, 95), (CX, CY, 125), 70, 24, True, 28)
rk.cyl(I("glass"), (CX, CY, 125), (CX, CY, 136), 28, 20, True, 10)  # glazed lantern ring
rk.cyl(I("iron"), (CX, CY, 136), (CX, CY, 148), 10, 14, True, 4)
# radial iron ribs on lower dome (visible silhouette)
for i in range(16):
    a = _m.radians(i * 22.5)
    x0 = CX + 92 * _m.cos(a); y0 = CY + 92 * _m.sin(a)
    x1 = CX + 68 * _m.cos(a); y1 = CY + 68 * _m.sin(a)
    rk.cyl(I("iron"), (x0, y0, 60), (x1, y1, 92), 0.35, 6)
rk.done("SK_RAH", RAH)
info["rah"] = {"cx_ft": CX, "cy_ft": CY, "note": "w02 frieze+windows+iron balcony+glazed lantern"}


# Albert Memorial suggestion (further NE, lean obelisk/canopy stub) — skip to keep lean

# ---- Museum fronts along west of Exhibition Road ----
# V&A / Science / NHM style: long stone/brick facades with central porticos
def museum_block(tag, x0, x1, y0, y1, h, mat_wall, portico=True):
    mk = K()
    mk.box(I(mat_wall), x0, x1, y0, y1, 0.0, h)
    mk.box(I("slate"), x0 - 1, x1 + 1, y0 - 1, y1 + 1, h, h + 4)
    # window rhythm (shallow recesses)
    span = x1 - x0; depth = abs(y1 - y0)
    face_y = y1 if y1 > y0 else y0
    nwin = max(4, int(span / 18))
    for i in range(nwin):
        wx = x0 + 8 + i * (span - 16) / max(1, nwin - 1)
        for floor in (8, 18, 28):
            if floor + 6 < h:
                mk.box(I("glass"), wx - 2.5, wx + 2.5, face_y - 0.4, face_y + 0.4, floor, floor + 5.5)
                # iron window frame + mullion
                mk.box(I("iron"), wx - 2.6, wx + 2.6, face_y - 0.55, face_y - 0.35, floor - 0.15, floor + 0.1)
                mk.box(I("iron"), wx - 2.6, wx + 2.6, face_y - 0.55, face_y - 0.35, floor + 5.4, floor + 5.65)
                mk.box(I("iron"), wx - 0.08, wx + 0.08, face_y - 0.55, face_y - 0.3, floor, floor + 5.5)
    if portico:
        mid = (y0 + y1) / 2
        # columned portico toward the road (east face at x1)
        for colx in (x1 - 2,):
            for cy in (mid - 18, mid - 6, mid + 6, mid + 18):
                mk.cyl(I("stone"), (colx, cy, 0.5), (colx, cy, h * 0.55), 1.4, 10)
        mk.box(I("stone"), x1 - 4, x1 + 6, mid - 24, mid + 24, h * 0.55, h * 0.55 + 3)
        # pediment
        mk.box(I("stone"), x1 - 2, x1 + 8, mid - 20, mid + 20, h * 0.55 + 3, h * 0.55 + 10)
    mk.done(f"SK_{tag}", MUS)

# West side: three museum fronts facing Exhibition Road (x negative)
museum_block("VA", -160, -34, -40, 80, 42, "stone", portico=True)          # V&A-ish
museum_block("SCIENCE", -150, -34, 100, 180, 38, "stone_d", portico=True)   # Science Museum-ish
museum_block("NHM", -170, -36, -180, -60, 48, "terracotta", portico=True)  # NHM-ish terracotta
info["museums"] = ["VA_block", "Science_block", "NHM_block"]

# Iron area railings along museum forecourts + Exhibition Rd lamps / bollards (set dressing)
dk = K()
import math as _m
for y in range(-170, 190, 12):
    # west railing (museum side)
    dk.cyl(I("iron"), (-33.5, y, 0.05), (-33.5, y, 3.4), 0.05, 6)
    if y % 24 == 0:
        dk.box(I("iron"), -34.0, -33.0, y - 0.15, y + 0.15, 3.2, 3.5)
for y in range(-170, 190, 24):
    dk.cyl(I("iron"), (-33.5, y, 3.35), (-33.5, y + 12, 3.35), 0.04, 6)
# east plaza railing toward RAH
for y in range(-40, 160, 10):
    dk.cyl(I("iron"), (34.5, y, 0.05), (34.5, y, 3.2), 0.05, 6)
for y in range(-160, 200, 50):
    # lamp posts
    for x in (-22, 24):
        dk.cyl(I("iron"), (x, y, 0.05), (x, y, 14), 0.22, 8)
        dk.cyl(I("iron"), (x, y, 14), (x, y, 15.2), 0.55, 8, True, 0.15)
        dk.box(I("glass"), x - 0.45, x + 0.45, y - 0.45, y + 0.45, 13.2, 14.6)
# bollards at road edge near RAH approach
for y in (40, 55, 70, 85):
    dk.cyl(I("iron"), (17.2, y, 0.0), (17.2, y, 2.8), 0.35, 10, True, 0.28)
dk.done("SK_StreetDress", STREET)
info["dressing"] = "iron rails, lamps, bollards, tree guards"

# Imperial College / Albert Hall plaza grass strip between road and RAH
gk2 = K()
gk2.box(I("grass"), 36, CX - 120, CY - 150, CY + 150, 0.0, 0.15)
gk2.done("SK_PlazaGrass", STREET)

# ---- present-day daylight ----
G.world_sky(elev=42, rot=185, strength=0.38, sun_energy=3.6,
            sun_rot=(48, 0, -20), sun_col=(1.0, 0.97, 0.92), haze=(1.2, 0.55))
sc.cycles.samples = 28
sc.render.resolution_x = 1280; sc.render.resolution_y = 720
G.render_settings(exposure=-0.15)

# ---- cameras: street approach + RAH hold ----
route = {
 "set": "SOUTH KEN TODAY (CP069) optional",
 "units": "feet",
 "grammar": "eye 5.25 ft, 35 mm, no roll",
 "shots": [
  {"id": "CP069_street", "storyboard": "CP069", "lens_mm": 35,
   "start": {"pos_ft": [0.0, -140.0, 5.25], "look_ft": [60.0, 50.0, 70.0]},
   "end":   {"pos_ft": [0.0, -110.0, 5.25], "look_ft": [70.0, 80.0, 80.0]},
   "note": "Exhibition Road looking NNE toward RAH dome"},
  {"id": "CP069_rah", "storyboard": "CP069", "lens_mm": 35,
   "start": {"pos_ft": [20.0, -160.0, 5.25], "look_ft": [95.0, 90.0, 90.0]},
   "note": "RAH full dome from further SW"},
  {"id": "CP069_museums", "storyboard": "CP069", "lens_mm": 35,
   "start": {"pos_ft": [5.0, 20.0, 5.25], "look_ft": [-120.0, 20.0, 22.0]},
   "note": "museum fronts from road centre looking west"}
 ]
}
rp = os.path.join(HERE, "..", "route", "camera_route_cp069.json")
json.dump(route, open(rp, "w"), indent=1)
# append into main route for coverage
main_rp = os.path.join(HERE, "..", "route", "camera_route.json")
main = json.load(open(main_rp))
ids = {s["id"] for s in main["shots"]}
for s in route["shots"]:
    if s["id"] not in ids: main["shots"].append(s)
json.dump(main, open(main_rp, "w"), indent=1)

CAMS = G.coll("CAMERAS")
G.cameras(rp, CAMS)
info["cams"] = [s["id"] for s in route["shots"]]
G.save(OUT, info, "O-LONDON southken today CP069", SEED)
print("SK_INFO", json.dumps(info), flush=True)
