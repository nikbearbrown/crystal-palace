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
        "note": "simple present-day block-out; real footage may replace (DEPARTURES)"}

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

# street trees as simple cylinders (lean)
for i, y in enumerate(range(-180, 200, 40)):
    for x in (-26, 28):
        tk = K()
        tk.cyl(I("stone_d"), (x, y, 0.1), (x, y, 12), 0.6, 8)
        tk.cyl(I("grass"), (x, y, 12), (x, y, 22), 5.0, 10, True, 0.5)
        tk.done(f"SK_Tree_{i}_{x}", STREET)

# ---- Royal Albert Hall (east of Exhibition Rd) — simple cylinder + dome block-out ----
# Centre ~X=95, Y=90. Camera-safe: solid massing without thick wall ring that swallowed cams.
CX, CY = 95.0, 90.0
rk = K()
rk.box(I("stone"), CX - 130, CX + 130, CY - 150, CY + 150, 0.0, 3.5)   # podium
rk.cyl(I("terracotta"), (CX, CY, 3.5), (CX, CY, 48), 110, 28, True, 110)  # amphitheatre body
rk.cyl(I("stone"), (CX, CY, 48), (CX, CY, 52), 112, 28, True, 108)        # cornice
rk.cyl(I("dome"), (CX, CY, 52), (CX, CY, 95), 95, 24, True, 70)
rk.cyl(I("dome"), (CX, CY, 95), (CX, CY, 125), 70, 20, True, 28)
rk.cyl(I("dome"), (CX, CY, 125), (CX, CY, 138), 28, 16, True, 6)
rk.cyl(I("iron"), (CX, CY, 138), (CX, CY, 148), 8, 12, True, 4)
rk.done("SK_RAH", RAH)
info["rah"] = {"cx_ft": CX, "cy_ft": CY, "note": "block-out cylinder amphitheatre + dome"}


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
