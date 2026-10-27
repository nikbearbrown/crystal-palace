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

# RAH reads: deep red brick, buff terracotta, dark mosaic frieze, darker iron/glass dome
M = dict(
    asphalt=G.mat("Asphalt", (0.16, 0.16, 0.15), 0.92),
    pavement=G.mat("Pavement", (0.48, 0.46, 0.42), 0.88),
    brick=G.mat("BrickDeep", (0.16, 0.045, 0.028), 0.92),            # deeper red — fight AgX mid lift
    terracotta=G.mat("TerracottaBuff", (0.48, 0.32, 0.16), 0.85),  # buff terracotta band
    mosaic=G.mat("MosaicFrieze", (0.06, 0.05, 0.045), 0.70),       # dark mosaic under cornice
    stone=G.mat("StonePale", (0.55, 0.52, 0.46), 0.82),
    stone_d=G.mat("StoneDark", (0.32, 0.30, 0.27), 0.85),
    dome=G.mat("DomeIronGlass", (0.08, 0.085, 0.08), 0.38, 0.7),  # darker grey wrought-iron/glass
    glass=G.mat_thin_glass("Glass", (0.45, 0.52, 0.55), 0.18),     # tinted, less sky wash
    glass_win=G.mat("GlassWinDark", (0.08, 0.10, 0.12), 0.25, 0.35),  # dark exterior glazing
    grass=G.mat("Grass", (0.12, 0.24, 0.08), 0.95),
    leaf=G.mat("LeafPlane", (0.10, 0.22, 0.06), 0.95),
    leaf_d=G.mat("LeafDeep", (0.045, 0.12, 0.03), 0.95),
    bark=G.mat("Bark", (0.28, 0.18, 0.10), 0.9),
    iron=G.mat("IronRail", (0.07, 0.07, 0.08), 0.45, 0.65),
    slate=G.mat("Slate", (0.14, 0.15, 0.16), 0.75),
)
ML = list(M.values()); IX = {k: i for i, k in enumerate(M)}
def K(): return Kit(ML)

def I(k): return IX[k]

def leaf_noise_mat(base_mat, scale=18.0):
    """Multiply leaf albedo by noise so canopy reads leafy, not plastic."""
    if base_mat.get("leaf_noise"): return base_mat
    nt = base_mat.node_tree; b = nt.nodes.get("Principled BSDF")
    if not b: return base_mat
    tex = nt.nodes.new("ShaderNodeTexNoise"); tex.inputs["Scale"].default_value = scale
    tex.inputs["Detail"].default_value = 12; tex.inputs["Roughness"].default_value = 0.65
    tex.location = (-600, 200)
    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.location = (-380, 200)
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[0].color = (0.45, 0.55, 0.35, 1)
    ramp.color_ramp.elements[1].position = 0.72
    ramp.color_ramp.elements[1].color = (1.15, 1.15, 1.05, 1)
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"
    mix.inputs["Factor"].default_value = 1.0; mix.location = (-160, 120)
    col = tuple(b.inputs["Base Color"].default_value[:3]) + (1.0,)
    mix.inputs["A"].default_value = col
    nt.links.new(tex.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], mix.inputs["B"])
    nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
    base_mat["leaf_noise"] = 1
    return base_mat

# Units: feet (same as rest of london set). Origin at Exhibition Road / Prince Consort Rd approx.
# +Y = north along Exhibition Road; +X = east toward Albert Hall / Hyde Park.

# ---- Exhibition Road ----
gk = K()
gk.box(I("asphalt"), -18, 18, -200, 220, -0.4, 0.0)          # carriageway
gk.box(I("pavement"), -32, -18, -200, 220, -0.05, 0.08)      # W pavement (museums)
gk.box(I("pavement"), 18, 36, -200, 220, -0.05, 0.08)        # E pavement
gk.done("SK_Road", STREET)

# street trees — rounded broadleaf London planes (icosphere lobes + leaf noise; exterior park-tree grammar)

def albedo_noise(mat, scale=40.0, lo=(0.7,0.7,0.7), hi=(1.15,1.1,1.05), strength=0.55):
    if mat.get("albedo_noise"): return mat
    nt = mat.node_tree; b = nt.nodes.get("Principled BSDF")
    if not b: return mat
    tex = nt.nodes.new("ShaderNodeTexNoise"); tex.inputs["Scale"].default_value = scale
    tex.inputs["Detail"].default_value = 14; tex.inputs["Roughness"].default_value = 0.55
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.35; ramp.color_ramp.elements[0].color = (*lo, 1)
    ramp.color_ramp.elements[1].position = 0.7; ramp.color_ramp.elements[1].color = (*hi, 1)
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"
    mix.inputs["Factor"].default_value = strength
    col = tuple(b.inputs["Base Color"].default_value[:3]) + (1.0,)
    mix.inputs["A"].default_value = col
    nt.links.new(tex.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], mix.inputs["B"])
    nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
    mat["albedo_noise"] = 1
    return mat

leaf_noise_mat(M["leaf"], 22.0)
leaf_noise_mat(M["leaf_d"], 16.0)
albedo_noise(M["brick"], scale=55.0, lo=(0.65,0.55,0.50), hi=(1.05,0.95,0.88), strength=0.45)
albedo_noise(M["terracotta"], scale=30.0, lo=(0.75,0.7,0.6), hi=(1.1,1.05,0.95), strength=0.4)
albedo_noise(M["mosaic"], scale=80.0, lo=(0.4,0.4,0.4), hi=(1.3,1.2,1.1), strength=0.8)

def london_plane(name, x, y, H=28.0, seed=1):
    """Rounded broadleaf London plane: bark trunk + icosphere canopy lobes (exterior park-tree grammar) + leaf noise."""
    import bmesh
    from mathutils import Matrix
    rr = random.Random(seed)
    FT = 0.3048
    bm = bmesh.new()
    # trunk as cone
    bmesh.ops.create_cone(bm, cap_ends=True, segments=10,
                          radius1=0.7*FT, radius2=0.5*FT, depth=H*0.42*FT,
                          matrix=Matrix.Translation((x*FT, y*FT, H*0.21*FT)))
    trunk_faces = set(bm.faces)
    # canopy lobes — icospheres (reads rounded, not cone)
    for j in range(14):
        a = rr.uniform(0, 2*math.pi)
        d = rr.uniform(0, H*0.16)
        z = rr.uniform(H*0.42, H*0.82)
        r = rr.uniform(H*0.09, H*0.16)
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=r*FT,
            matrix=Matrix.Translation(((x + d*math.cos(a))*FT, (y + d*math.sin(a))*FT, z*FT)))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    me.materials.append(M["bark"]); me.materials.append(M["leaf"]); me.materials.append(M["leaf_d"])
    trunk_z = H * 0.40 * FT
    for poly in me.polygons:
        c = poly.center
        # trunk: near axis and below canopy springing
        if c.z < trunk_z and (c.x - x*FT)**2 + (c.y - y*FT)**2 < (1.2*FT)**2:
            poly.material_index = 0
        else:
            poly.material_index = 1 if (poly.index % 2) else 2
    ob = bpy.data.objects.new(name, me)
    STREET.objects.link(ob)
    # iron tree-guard as separate Kit
    gk = K()
    for a in range(0, 360, 45):
        rr2 = 1.7; ax = x + rr2 * math.cos(math.radians(a)); ay = y + rr2 * math.sin(math.radians(a))
        gk.cyl(I("iron"), (ax, ay, 0.05), (ax, ay, 3.4), 0.06, 6)
    gk.cyl(I("iron"), (x, y, 3.3), (x, y, 3.45), 1.75, 16, True, 1.65)
    gk.done(name + "_guard", STREET)

for i, y in enumerate(range(-180, 200, 40)):
    for xi, x in enumerate((-26, 28)):
        london_plane(f"SK_Plane_{i}_{x}", x, y, H=26 + (i + xi) % 5, seed=100 + i * 3 + xi)


# ---- Royal Albert Hall — deep red brick, buff band, dark mosaic, arched bays, darker ribbed dome ----
CX, CY = 95.0, 90.0
rk = K()
rk.box(I("stone"), CX - 130, CX + 130, CY - 150, CY + 150, 0.0, 3.5)   # podium
# deep red brick amphitheatre body (two stacked rings, slight entasis)
rk.cyl(I("brick"), (CX, CY, 3.5), (CX, CY, 28), 110, 48, True, 110)
rk.cyl(I("brick"), (CX, CY, 28), (CX, CY, 38), 110, 48, True, 109.5)
# buff terracotta band (taller so it reads from Exhibition Road)
rk.cyl(I("terracotta"), (CX, CY, 38), (CX, CY, 45), 111.2, 48, True, 111.2)
# dark mosaic frieze under the cornice
rk.cyl(I("mosaic"), (CX, CY, 45), (CX, CY, 51), 111.6, 48, True, 111.6)
# stone cornice + attic
rk.cyl(I("stone"), (CX, CY, 51), (CX, CY, 54.5), 113.0, 40, True, 108)
rk.cyl(I("stone"), (CX, CY, 54.5), (CX, CY, 58), 108, 36, True, 100)
# regular arched window bays — 36 × 2 storeys; dark glazing + iron arch frames (no AABB dashes / spikes)
N_BAY = 36
for i in range(N_BAY):
    a = math.radians(i * (360.0 / N_BAY) + 5)
    nx, ny = math.cos(a), math.sin(a)
    tx, ty = -ny, nx
    R = 110.35
    half_w = 3.6
    for floor_z, arch_h in ((7.0, 16.0), (24.0, 14.0)):
        z0 = floor_z
        z_spring = floor_z + arch_h * 0.62   # springing of arch
        z1 = floor_z + arch_h                # crown
        # rectangular dark glazing up to springing
        g = [
            (CX + R*nx + half_w*tx, CY + R*ny + half_w*ty, z0),
            (CX + R*nx - half_w*tx, CY + R*ny - half_w*ty, z0),
            (CX + R*nx - half_w*tx, CY + R*ny - half_w*ty, z_spring),
            (CX + R*nx + half_w*tx, CY + R*ny + half_w*ty, z_spring),
        ]
        rk.quad(I("glass_win"), g)
        # arched head: fan of dark quads under semicircle
        for k in range(6):
            t0 = -1.0 + k * (2.0/6); t1 = -1.0 + (k+1) * (2.0/6)
            # height of semicircle at t
            def arch_z(tt):
                return z_spring + (z1 - z_spring) * math.sqrt(max(0.0, 1.0 - tt*tt))
            q = [
                (CX + R*nx + half_w*t0*tx, CY + R*ny + half_w*t0*ty, z_spring),
                (CX + R*nx + half_w*t1*tx, CY + R*ny + half_w*t1*ty, z_spring),
                (CX + R*nx + half_w*t1*tx, CY + R*ny + half_w*t1*ty, arch_z(t1)),
                (CX + R*nx + half_w*t0*tx, CY + R*ny + half_w*t0*ty, arch_z(t0)),
            ]
            rk.quad(I("glass_win"), q)
        # iron frame: jambs + arch polyline + sill + centre mullion
        wx, wy = CX + (R+0.15)*nx, CY + (R+0.15)*ny
        # left/right jambs
        for s in (-1.0, 1.0):
            rk.cyl(I("iron"),
                   (CX + R*nx + half_w*s*tx, CY + R*ny + half_w*s*ty, z0),
                   (CX + R*nx + half_w*s*tx, CY + R*ny + half_w*s*ty, z_spring),
                   0.14, 6)
        # arch iron: segments along semicircle
        prev = None
        for k in range(9):
            tt = -1.0 + k * (2.0/8)
            zz = z_spring + (z1 - z_spring) * math.sqrt(max(0.0, 1.0 - tt*tt))
            pt = (CX + R*nx + half_w*tt*tx, CY + R*ny + half_w*tt*ty, zz)
            if prev is not None:
                rk.cyl(I("iron"), prev, pt, 0.12, 5)
            prev = pt
        # sill + centre mullion
        rk.cyl(I("iron"),
               (CX + R*nx + half_w*tx, CY + R*ny + half_w*ty, z0),
               (CX + R*nx - half_w*tx, CY + R*ny - half_w*ty, z0), 0.12, 5)
        rk.cyl(I("iron"), (wx, wy, z0), (wx, wy, z_spring), 0.10, 6)
# iron balcony rail at podium (camera-facing SW arc)
for i in range(24):
    a0 = math.radians(200 + i * 3.5); a1 = math.radians(200 + (i + 1) * 3.5)
    for a in (a0, a1):
        px = CX + 118 * math.cos(a); py = CY + 118 * math.sin(a)
        rk.cyl(I("iron"), (px, py, 3.5), (px, py, 6.0), 0.07, 6)
    x0, y0 = CX + 118 * math.cos(a0), CY + 118 * math.sin(a0)
    x1, y1 = CX + 118 * math.cos(a1), CY + 118 * math.sin(a1)
    rk.cyl(I("iron"), (x0, y0, 5.9), (x1, y1, 5.9), 0.06, 6)

# darker wrought-iron / glass dome with ribs (no bright washed lantern)
rk.cyl(I("dome"), (CX, CY, 58), (CX, CY, 95), 95, 36, True, 70)
rk.cyl(I("dome"), (CX, CY, 95), (CX, CY, 125), 70, 32, True, 28)
# lantern: iron frame + dark glass (not bright sky-hole)
rk.cyl(I("iron"), (CX, CY, 125), (CX, CY, 136), 28, 20, True, 12)
rk.cyl(I("glass_win"), (CX, CY, 126), (CX, CY, 134), 26, 16, True, 11)
rk.cyl(I("iron"), (CX, CY, 136), (CX, CY, 148), 10, 14, True, 4)
# radial iron ribs on lower + upper dome
for i in range(24):
    a = math.radians(i * 15)
    x0 = CX + 92 * math.cos(a); y0 = CY + 92 * math.sin(a)
    x1 = CX + 68 * math.cos(a); y1 = CY + 68 * math.sin(a)
    rk.cyl(I("iron"), (x0, y0, 60), (x1, y1, 94), 1.35, 6)
    x2 = CX + 66 * math.cos(a); y2 = CY + 66 * math.sin(a)
    x3 = CX + 26 * math.cos(a); y3 = CY + 26 * math.sin(a)
    rk.cyl(I("iron"), (x2, y2, 96), (x3, y3, 124), 1.05, 6)
rk.done("SK_RAH", RAH)
info["rah"] = {"cx_ft": CX, "cy_ft": CY, "note": "w03: deep brick, buff band, mosaic frieze, arched bays, dark ribbed dome"}
info["note"] = "w03: RAH readable as itself; London-plane trees; exposure matched to before luminance; real footage may still replace"

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
# authored daylight but held back so brick/dome don't wash (match before mean luminance ~0.73)
G.world_sky(elev=36, rot=185, strength=0.18, sun_energy=1.8,
            sun_rot=(52, 0, -25), sun_col=(1.0, 0.94, 0.86), haze=(0.8, 0.35))
sc.cycles.samples = 28
sc.render.resolution_x = 1280; sc.render.resolution_y = 720
# authored exposure held for brick saturation; mean-luminance matched in w03 review
G.render_settings(exposure=-0.18)

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
