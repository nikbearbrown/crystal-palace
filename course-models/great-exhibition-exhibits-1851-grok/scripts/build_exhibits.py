"""Great Exhibition 1851 hero exhibits as standalone, instance-ready assets (Grok Bot).
  blender -b -P scripts/build_exhibits.py -- --out rounds/e01.blend
Assets (each its own collection under EXH_ASSETS, origin = floor centre, Z up, metres; geometry written in feet):
  EXH_KOHINOOR            CP025  Koh-i-Noor (186 ct, pre-1852 cut) in the Chubb gilded 'birdcage' case  [I: case form from written
                                 accounts, ILN 17/31 May 1851, Illustrated Exhibitor 7 Jun 1851]
  EXH_OSLER_CANDELABRUM   CP025  one of F. & C. Osler's pair of cut crystal-glass candelabra, 8 ft high, 15 lights, prismatic shaft
                                 over 3 ft (Official Catalogue Class 24 no. 20, Central North Gallery; property of the Queen)
  EXH_NASMYTH_HAMMER      CP024  J. Nasmyth's steam hammer (Official Catalogue Class 6 no. 236), proportions after the Smithsonian
                                 Nasmyth hammer c.1851-56 (base 14 x 6 ft, ~19 ft high); ram animated, 4 blows over frames 1-96
The SHOWROOM collection is a neutral preview stand (boards, 24 ft column line, figures, cameras); it is not part of any asset.
place_exhibits.py instances these collections into any other scene (e.g. Claude's west nave) without editing that file."""
import bpy, bmesh, math, sys, os, json, importlib
from mathutils import Vector, Matrix
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as CM, figures as FG, parts1851 as P
for m in (CM, FG, P): importlib.reload(m)
from common import ft, FT, mat, noisy_mat, coll, obj, instance
from parts1851 import finish, mark, box, rod, beam, prism, lathe, I
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
OUT = os.path.abspath(arg("--out", "/tmp/exhibits.blend")); HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'; sc.frame_start = 1; sc.frame_end = 96; sc.render.fps = 24
ROOT = sc.collection

def glass(name, rgb=(1, 1, 1), ior=1.5, rough=0.0, frost=False):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Transmission Weight"].default_value = 1.0
    b.inputs["IOR"].default_value = ior; b.inputs["Roughness"].default_value = 0.35 if frost else rough
    m.diffuse_color = (*rgb, 0.3); return m
GILT = mat("EX_Gilt", (0.83, 0.60, 0.26), 0.28, 1.0)
BRASS = mat("EX_Brass", (0.78, 0.60, 0.33), 0.35, 1.0)
VELVET = mat("EX_Velvet_crimson", (0.30, 0.02, 0.03), 0.95)
CLOTH = mat("EX_Pedestal_cloth", (0.36, 0.05, 0.05), 0.9)
GOLD = mat("EX_Gold", (0.95, 0.72, 0.30), 0.2, 1.0)
DIAMOND = glass("EX_Diamond", ior=2.417)
DOME = glass("EX_Dome_glass", ior=1.5)
CRYSTAL = glass("EX_Crystal_glass", (0.98, 0.99, 1.0), ior=1.56)
FROST = glass("EX_Frosted_glass", ior=1.5, frost=True)
WAX = mat("EX_Candle_wax", (0.88, 0.85, 0.76), 0.5)
MACH = mat("EX_Machine_paint", (0.10, 0.13, 0.11), 0.55)      # dark green-grey: interpretive (EX07)
STEEL = mat("EX_Bright_steel", (0.62, 0.62, 0.60), 0.25, 1.0)
CAST = mat("EX_Cast_iron", (0.09, 0.09, 0.09), 0.7, 0.4)
RAIL = mat("EX_Rail_iron", (0.05, 0.05, 0.05), 0.5, 0.5)
MAHOG = mat("EX_Mahogany", (0.20, 0.07, 0.03), 0.45)

ASSETS = coll("EXH_ASSETS", ROOT)
def asset(name, **meta):
    C = coll(name, ASSETS); C.instance_offset = (0, 0, 0)
    for k, v in meta.items(): C[k] = v if not isinstance(v, (dict, list)) else json.dumps(v)
    return C
def part(name, C, bm, mats, loc=(0, 0, 0), **props):
    o = obj(name, finish(bm, "ME_" + name, mats), C, loc, 0.0, **props); return o
def ring(bm, r, z, t, seg=48):
    for k in range(seg):
        a0 = 2 * math.pi * k / seg; a1 = 2 * math.pi * (k + 1) / seg
        rod(bm, (r * math.cos(a0), r * math.sin(a0), z), (r * math.cos(a1), r * math.sin(a1), z), t, 6)
def poly_rod(bm, pts, r, seg=6):
    for a, b in zip(pts[:-1], pts[1:]): rod(bm, a, b, r, seg)

# ============ EXH_KOHINOOR (CP025) ============
KC = asset("EXH_KOHINOOR", shot="CP025", status="I", title="The Koh-i-Noor in its gilded cage (Chubb)",
           credit="Grok Bot; case form interpreted from written accounts - no measured drawing survives in our sources",
           sources="ILN 17 May 1851 p.426-428, 31 May 1851 p.491; Illustrated Exhibitor 7 Jun & 12 Jul 1851 ('a golden cage', 'great parrot-cage with gilded bars', small gilt crown; diamond on velvet under glass, the two armlet stones beside it; lowered into an iron safe at night)",
           placement="Main avenue, east of the transept (contemporary guides); 8 ft tall, rail R 6.5 ft", dims_ft={"rail_r": 6.5, "cage_r": 1.45, "height": 8.15})
R_RAIL = 6.5; CAGE_R = 1.45; PED_TOP = 3.1; CAGE_TOP = 6.2; DOME_APEX = 7.35
bm = bmesh.new()                                   # pedestal = Chubb safe housing, draped (I)
lathe(bm, [(0, 0), (2.05, 0), (2.05, 0.35), (1.75, 0.45), (1.6, 0.5), (1.6, 2.75), (1.85, 2.85), (1.85, PED_TOP), (0, PED_TOP)], 40)
part("KOH_pedestal", KC, bm, [CLOTH], part_kind="pedestal", note="houses the iron safe the stone descended into at night")
bm = bmesh.new(); NB = 32                          # gilded bars: vertical, then curving into a bell dome
for k in range(NB):
    a = 2 * math.pi * k / NB; c, s = math.cos(a), math.sin(a); pts = [(CAGE_R * c, CAGE_R * s, PED_TOP)]
    pts.append((CAGE_R * c, CAGE_R * s, CAGE_TOP))
    for j in range(1, 9):
        t = j / 8 * math.pi / 2; r = CAGE_R * math.cos(t); z = CAGE_TOP + (DOME_APEX - CAGE_TOP) * math.sin(t)
        pts.append((max(r, 0.12) * c, max(r, 0.12) * s, z))
    poly_rod(bm, pts, 0.032)
for z, t in ((PED_TOP + 0.06, 0.07), (PED_TOP + 0.95, 0.04), (4.95, 0.04), (CAGE_TOP, 0.06)): ring(bm, CAGE_R, z, t)
ring(bm, CAGE_R * math.cos(math.radians(45)), CAGE_TOP + (DOME_APEX - CAGE_TOP) * math.sin(math.radians(45)), 0.035, 32)
lathe(bm, [(0, DOME_APEX - 0.05), (0.26, DOME_APEX - 0.05), (0.26, DOME_APEX + 0.02), (0, DOME_APEX + 0.02)], 24)
part("KOH_cage", KC, bm, [GILT], part_kind="cage", bars=NB)
bm = bmesh.new()                                   # little crown on the apex (I)
lathe(bm, [(0, 0), (0.24, 0), (0.26, 0.2), (0, 0.2)], 24)
for k in range(8):
    a = 2 * math.pi * k / 8
    poly_rod(bm, [(0.25 * math.cos(a) * math.cos(t), 0.25 * math.sin(a) * math.cos(t), 0.2 + 0.38 * math.sin(t)) for t in [i / 6 * math.pi / 2 for i in range(7)]], 0.022)
lathe(bm, [(0, 0.55), (0.06, 0.58), (0.075, 0.64), (0.06, 0.7), (0, 0.72)], 16)
beam(bm, (0, 0, 0.7), (0, 0, 0.9), 0.03, 0.03); beam(bm, (-0.06, 0, 0.83), (0.06, 0, 0.83), 0.03, 0.03)
part("KOH_crown", KC, bm, [GILT], loc=(0, 0, DOME_APEX + 0.02), part_kind="crown")
bm = bmesh.new()                                   # velvet stand inside the cage
lathe(bm, [(0, PED_TOP), (0.55, PED_TOP), (0.55, PED_TOP + 0.12), (0.28, PED_TOP + 0.25), (0.22, 3.75), (0.5, 3.85), (0.5, 3.98), (0, 3.98)], 32)
part("KOH_stand", KC, bm, [VELVET], part_kind="stand")
bm = bmesh.new(); prof = []                        # glass dome (bell jar), real shell
for j in range(13):
    t = j / 12 * math.pi / 2; prof.append((0.42 * math.cos(t) if j < 12 else 0.0, 3.98 + 0.72 * math.sin(t)))
inner = [(max(r - 0.012, 0), z - 0.012) for r, z in reversed(prof)]
lathe(bm, prof + inner[:-1] + [(0.408, 3.98)], 40)
part("KOH_dome", KC, bm, [DOME], part_kind="glass_dome")
def gem(name, Lin, Win, Din, loc, tilt):
    """pre-1852 Mughal cut: a flattish, irregular oval with many shallow facets; Lin x Win x Din in INCHES"""
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
    for v in bm.verts:
        x, y, z = v.co; z = min(z, 0.55)                       # flat table on top
        v.co = Vector((x * Lin / 2 * I, y * Win / 2 * I, z * Din / 2 * I))
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.radians(tilt), 3, 'X'))
    me = finish(bm, "ME_" + name, [DIAMOND])
    for p in me.polygons: p.use_smooth = False
    return obj(name, me, KC, loc, 0.0, part_kind="gem", L_in=Lin, W_in=Win, D_in=Din)
GZ = 4.22
gem("KOH_diamond", 1.55, 1.3, 0.68, (0, 0, GZ), -65)           # ~186 ct by volume (EX02)
gem("KOH_armlet_L", 0.75, 0.6, 0.35, (-0.2, 0, 4.12), -65); gem("KOH_armlet_R", 0.75, 0.6, 0.35, (0.2, 0, 4.12), -65)
bm = bmesh.new()                                    # gold prongs holding the three stones
for (x, zt) in ((0, GZ - 0.04), (-0.2, 4.1), (0.2, 4.1)):
    rod(bm, (x, 0.02, 3.98), (x, 0.02, zt), 0.012, 6); rod(bm, (x, 0.02, zt), (x + 0.03, -0.02, zt + 0.05), 0.008, 6)
    rod(bm, (x, 0.02, zt), (x - 0.03, -0.02, zt + 0.05), 0.008, 6)
part("KOH_prongs", KC, bm, [GOLD], part_kind="prongs")
bm = bmesh.new(); NP = 12                          # barrier rail (I: keeps the crowd ~6 ft off, as the queue accounts imply)
for k in range(NP):
    a = 2 * math.pi * k / NP; x, y = R_RAIL * math.cos(a), R_RAIL * math.sin(a)
    rod(bm, (x, y, 0), (x, y, 3.0), 0.07, 10); lathe(bm, [(0, 0), (0.22, 0), (0.18, 0.12), (0, 0.12)], 12, Matrix.Translation((x, y, 0)))
    lathe(bm, [(0, 2.95), (0.12, 2.98), (0.12, 3.08), (0, 3.12)], 12, Matrix.Translation((x, y, 0)))
ring(bm, R_RAIL, 3.0, 0.06, 72); ring(bm, R_RAIL, 1.4, 0.035, 72)
part("KOH_rail", KC, bm, [BRASS], part_kind="rail", radius_ft=R_RAIL)

# ============ EXH_OSLER_CANDELABRUM ============
OC = asset("EXH_OSLER_CANDELABRUM", shot="CP025", status="C/I", title="F. & C. Osler cut crystal-glass candelabrum (one of the Queen's pair)",
           credit="Grok Bot; height, light count and prism shaft from the Official Catalogue; arm layout and cutting interpretive",
           sources="Official Catalogue 1851, Class 24 no. 20 (Central North Gallery I.27): 'A pair of richly cut crystal-glass candelabra, 8 feet high, carrying 15 lights each. The shaft composed of prisms upwards of 3 feet in length'; Official Descriptive & Illustrated Catalogue vol. II p.297",
           placement="historically in the Central North Gallery (upper level); asset stands on its own foot", dims_ft={"height": 8.0, "lights": 15, "shaft": 3.4})
bm = bmesh.new()
lathe(bm, [(0, 0), (1.25, 0), (1.25, 0.12), (1.05, 0.2), (1.05, 0.3), (0.75, 0.42), (0.55, 0.6), (0.62, 0.75), (0.4, 0.95), (0.24, 1.05), (0.3, 1.12), (0, 1.12)], 16)
lathe(bm, [(0, 4.5), (0.3, 4.5), (0.55, 4.62), (0.5, 4.85), (0.2, 4.95), (0, 4.95)], 16)
for z in (5.4, 6.0, 6.7):
    lathe(bm, [(0, z - 0.12), (0.12, z - 0.12), (0.2, z), (0.12, z + 0.12), (0, z + 0.12)], 12)
rod(bm, (0, 0, 4.9), (0, 0, 7.2), 0.07, 12)
part("OSL_body", OC, bm, [CRYSTAL], part_kind="glass_body")
bm = bmesh.new()                                    # the prismatic shaft: 6 long hexagonal prisms + core (C: 'prisms upwards of 3 ft')
SH0, SH1 = 1.12, 4.5
hexp = [(0.055 * math.cos(math.radians(60 * k)), 0.055 * math.sin(math.radians(60 * k))) for k in range(6)]
for k in range(6):
    a = math.radians(60 * k + 30); cx, cy = 0.15 * math.cos(a), 0.15 * math.sin(a)
    prism(bm, [(cx + x, cy + y) for x, y in hexp], SH0, SH1)
prism(bm, [(x * 1.4, y * 1.4) for x, y in hexp], SH0, SH1)
part("OSL_shaft_prisms", OC, bm, [CRYSTAL], part_kind="prism_shaft", length_ft=SH1 - SH0)
arms = bmesh.new(); pans = bmesh.new(); wax = bmesh.new(); drops = bmesh.new(); lights = []
def light(x, y, z, cand=0.75):
    lathe(pans, [(0, z - 0.03), (0.2, z - 0.01), (0.22, z + 0.02), (0.08, z + 0.03), (0.07, z + 0.12), (0, z + 0.12)], 16)
    lathe(wax, [(0, z + 0.1), (0.055, z + 0.1), (0.055, z + 0.1 + cand), (0.02, z + 0.12 + cand), (0, z + 0.12 + cand)], 10)
    for k in range(6):                                  # hanging prism drops off each pan
        a = 2 * math.pi * k / 6 + 0.3; dx, dy = x + 0.21 * math.cos(a), y + 0.21 * math.sin(a)
        bmesh.ops.create_cone(drops, cap_ends=True, segments=4, radius1=0.025, radius2=0.0, depth=0.28, matrix=Matrix.Translation((dx, dy, z - 0.18)) @ Matrix.Rotation(math.pi, 4, 'X'))
        rod(drops, (dx, dy, z - 0.02), (dx, dy, z - 0.04), 0.022, 4)
    lights.append((x, y, z + 0.1 + cand))
for k in range(8):                                   # lower tier: 8 S-arms
    a = 2 * math.pi * k / 8; c, s = math.cos(a), math.sin(a); pts = []
    for j in range(13):
        t = j / 12; r = 0.35 + 1.55 * t; z = 4.72 - 0.45 * math.sin(math.pi * t) + 0.95 * t * t; pts.append((r * c, r * s, z))
    poly_rod(arms, pts, 0.045, 8); light(1.9 * c, 1.9 * s, 5.67)
for k in range(6):                                   # upper tier: 6 arms
    a = 2 * math.pi * k / 6 + math.pi / 6; c, s = math.cos(a), math.sin(a); pts = []
    for j in range(11):
        t = j / 10; r = 0.12 + 0.98 * t; z = 6.0 - 0.25 * math.sin(math.pi * t) + 0.6 * t * t; pts.append((r * c, r * s, z))
    poly_rod(arms, pts, 0.035, 8); light(1.1 * c, 1.1 * s, 6.6)
light(0, 0, 7.18, 0.7)                               # central light -> top of candle = 8.0 ft
for k in range(8):                                   # festoons of prisms between the lower pans
    a0 = 2 * math.pi * k / 8; a1 = 2 * math.pi * (k + 1) / 8
    for j in range(1, 12):
        t = j / 12; a = a0 + (a1 - a0) * t; r = 1.9 * math.cos((a1 - a0) / 2) / math.cos(a - (a0 + a1) / 2) * 0.98
        z = 5.6 - 0.45 * math.sin(math.pi * t)
        bmesh.ops.create_icosphere(drops, subdivisions=1, radius=0.035, matrix=Matrix.Translation((r * math.cos(a), r * math.sin(a), z)))
part("OSL_arms", OC, arms, [CRYSTAL], part_kind="arms"); part("OSL_pans", OC, pans, [CRYSTAL], part_kind="drip_pans")
part("OSL_drops", OC, drops, [CRYSTAL], part_kind="drops"); part("OSL_candles", OC, wax, [WAX], part_kind="candles", lights=len(lights))
OC["lights_built"] = len(lights); OC["height_built_ft"] = round(max(l[2] for l in lights) + 0.02, 3)

# ============ EXH_NASMYTH_HAMMER (CP024) ============
HC = asset("EXH_NASMYTH_HAMMER", shot="CP024", status="C/B", title="Nasmyth's steam hammer (James Nasmyth & Co., Patricroft, Manchester)",
           credit="Grok Bot; general arrangement after the Smithsonian NMAH Nasmyth hammer (c.1851-56: base 6 x 14 ft, ~19 ft high, 14 tons); 1851 exhibit's own dimensions not found",
           sources="Official Catalogue 1851 Class 6 no. 236 'Nasmyth, J., Manchester. Steam hammer'; Machinery in Motion, north-west (British) side; NMAH object record (Nasmyth steam hammer); Nasmyth, Autobiography (1883) ch. 13",
           placement="Machinery in Motion, north-west area; footprint 14 x 6 ft, barrier 22 x 14 ft", dims_ft={"base_x": 14.0, "base_y": 6.0, "height": 19.0, "stroke": 3.5})
bm = bmesh.new()
for sx in (-1, 1):                                   # sole plates (I arrangement)
    box(bm, min(sx * 2.6, sx * 7.0), max(sx * 2.6, sx * 7.0), -3.0, 3.0, 0, 0.7)
    for (xa, xb) in ((6.2, 3.15), (2.75, 1.75)):         # two legs per standard, raking in, box section 0.9 x 2.2
        beam(bm, (sx * xa, 0, 0.7), (sx * xb, 0, 12.5), 0.9, 2.2)
    for z in (3.8, 7.6, 10.6):                          # ribs between the legs
        xo = 6.2 + (3.15 - 6.2) * (z - 0.7) / 11.8; xi = 2.75 + (1.75 - 2.75) * (z - 0.7) / 11.8
        box(bm, min(sx * xi, sx * xo), max(sx * xi, sx * xo), -0.9, 0.9, z - 0.3, z + 0.3)
    box(bm, min(sx * 1.45, sx * 1.65), max(sx * 1.45, sx * 1.65), -0.55, 0.55, 3.0, 12.5)      # guide strips (bright)
    for (yy) in (-1.2, 1.2):                            # holding-down bolts
        rod(bm, (sx * 6.2, yy * 2, 0.7), (sx * 6.2, yy * 2, 1.05), 0.12, 6); rod(bm, (sx * 3.2, yy * 2, 0.7), (sx * 3.2, yy * 2, 1.05), 0.12, 6)
box(bm, -3.6, 3.6, -1.3, 1.3, 12.5, 13.6)          # entablature / cylinder bed
part("HAM_frame", HC, bm, [MACH], part_kind="frame")
bm = bmesh.new()
for sx in (-1, 1): box(bm, min(sx * 1.43, sx * 1.47), max(sx * 1.43, sx * 1.47), -0.5, 0.5, 3.0, 12.4)
box(bm, -0.85, 0.85, -0.65, 0.65, 2.6, 2.95)         # lower die on the anvil
part("HAM_guides_dies", HC, bm, [STEEL], part_kind="guides")
bm = bmesh.new()                                     # anvil block on its own foundation (Nasmyth's practice; C)
box(bm, -2.1, 2.1, -2.1, 2.1, 0, 0.4); box(bm, -1.8, 1.8, -1.8, 1.8, 0.4, 1.9); box(bm, -1.3, 1.3, -1.1, 1.1, 1.9, 2.6)
part("HAM_anvil", HC, bm, [CAST], part_kind="anvil", independent_foundation=True)
bm = bmesh.new()                                     # steam cylinder, valve chest, pipes
lathe(bm, [(0, 13.6), (1.45, 13.6), (1.45, 13.85), (1.25, 13.85), (1.25, 18.0), (1.45, 18.0), (1.45, 18.25), (1.0, 18.55), (0.3, 18.7), (0, 18.7)], 32)
box(bm, 1.2, 1.95, -0.65, 0.65, 14.2, 16.8); box(bm, 1.9, 2.05, -0.75, 0.75, 14.1, 16.9)
poly_rod(bm, [(1.95, 0.2, 16.3), (3.2, 0.2, 16.3), (3.6, 0.2, 15.9), (3.6, 0.2, 0.0)], 0.2, 12)       # steam main from below floor (C: supplied from the boiler house)
poly_rod(bm, [(1.95, -0.3, 14.6), (2.6, -0.3, 14.6), (2.6, -0.3, 18.6), (2.6, -0.3, 19.0)], 0.17, 12)    # exhaust up
lathe(bm, [(0, 18.62), (0.25, 18.62), (0.25, 19.0), (0, 19.0)], 12, Matrix.Translation((2.6, -0.3, 0)))
part("HAM_cylinder", HC, bm, [MACH], part_kind="cylinder")
bm = bmesh.new()                                     # valve gear and the driver's hand lever (simplified; B)
rod(bm, (2.15, -0.8, 15.4), (2.15, -0.8, 4.4), 0.06, 8); rod(bm, (2.15, -0.8, 4.4), (4.0, -1.6, 3.6), 0.07, 8)
lathe(bm, [(0, -0.12), (0.09, -0.1), (0.09, 0.1), (0, 0.12)], 10, Matrix.Translation((4.0, -1.6, 3.6)))
rod(bm, (2.15, -0.8, 15.4), (1.95, -0.5, 15.6), 0.05, 8)
part("HAM_valve_gear", HC, bm, [STEEL], part_kind="valve_gear")
bm = bmesh.new()                                     # the ram (tup) with its piston rod; origin at the ram's striking face
box(bm, -1.2, 1.2, -0.9, 0.9, 0.35, 2.55); box(bm, -0.85, 0.85, -0.65, 0.65, 0.0, 0.35)
for sx in (-1, 1): box(bm, min(sx * 1.2, sx * 1.42), max(sx * 1.2, sx * 1.42), -0.45, 0.45, 0.6, 2.3)
rod(bm, (0, 0, 2.55), (0, 0, 2.55 + 8.9), 0.22, 16)
DIE_TOP = 2.95; STROKE = 3.5
tup = part("HAM_ram", HC, bm, [MACH], loc=(0, 0, DIE_TOP), part_kind="ram", stroke_ft=STROKE)
tup.data.materials.append(STEEL)
for p in tup.data.polygons:
    if p.center.z < ft(0.36) or p.center.z > ft(2.6): p.material_index = 1
for blow in range(4):                                # 4 blows in 96 frames: lift 14 frames, hold 4, fall 6 (gravity + top steam)
    f0 = 1 + 24 * blow
    for fr, dz, interp in ((f0, 0, 'BEZIER'), (f0 + 14, STROKE, 'BEZIER'), (f0 + 18, STROKE, 'QUAD'), (f0 + 24, 0, 'BEZIER')):
        tup.location.z = ft(DIE_TOP + dz); tup.keyframe_insert("location", index=2, frame=fr)
for fc in (tup.animation_data.action.fcurves if hasattr(tup.animation_data.action, "fcurves") else []):
    for kp in fc.keyframe_points:
        if abs(kp.co[1] - ft(DIE_TOP + STROKE)) < 1e-4 and kp.co[0] % 24 in (19,): kp.interpolation = 'QUAD'; kp.easing = 'EASE_IN'
bm = bmesh.new()                                     # barrier (I)
BX, BY = 11.0, 7.0; posts = []
for x in (-BX, -BX / 2, 0, BX / 2, BX):
    posts += [(x, -BY), (x, BY)]
for y in (-BY / 2 * 0, ): posts += [(-BX, 0), (BX, 0)]
for (x, y) in posts: rod(bm, (x, y, 0), (x, y, 3.0), 0.07, 8)
for (a, b) in (((-BX, -BY), (BX, -BY)), ((BX, -BY), (BX, BY)), ((BX, BY), (-BX, BY)), ((-BX, BY), (-BX, -BY))):
    rod(bm, (*a, 3.0), (*b, 3.0), 0.06, 8); rod(bm, (*a, 1.5), (*b, 1.5), 0.04, 8)
part("HAM_barrier", HC, bm, [RAIL], part_kind="rail", half_ft=[BX, BY])
bm = bmesh.new(); box(bm, -1.2, 1.2, -0.04, 0.04, 0, 1.6); box(bm, -1.3, 1.3, -0.06, 0.06, 1.6, 2.3)
part("HAM_label", HC, bm, [MAHOG], loc=(-4.5, -BY - 0.6, 0), part_kind="label", text="Nasmyth's Patent Steam Hammer - J. Nasmyth & Co., Patricroft")

for C in (KC, OC, HC):
    zs = [(o.matrix_world @ Vector(c)).z for o in C.objects for c in o.bound_box]; C["min_z_ft"] = round(min(zs) / FT, 3)
    try: C.asset_mark(); C.asset_data.description = C["title"] + " - " + C["status"]
    except Exception as e: print("asset_mark", e)

# ============ SHOWROOM (preview stand only) ============
CM.world(sun_elev=58, sun_rot=150, strength=0.5, sun_energy=3.0, exposure=-2.0)
SR = coll("SHOWROOM", ROOT); RES = coll("SHOWROOM_FIGURES", SR)
FLOOR = noisy_mat("EX_Floor_boards", (0.30, 0.22, 0.14), (0.38, 0.29, 0.19), scale=1.2, rough=0.8)
bm = bmesh.new(); box(bm, -60, 160, -60, 60, -0.5, 0.0); part("SR_floor", SR, bm, [FLOOR], part_kind="floor")
COLP = mat("EX_Column_blue", (0.32, 0.42, 0.62), 0.6)
bm = bmesh.new()
for k in range(-2, 8):
    x = 24 * k - 12
    for y in (-36, 36):
        P.add_column(bm, 22 + 2 / 12 - 3, M=Matrix.Translation((x, y, 0)))
    if k < 7:
        for y in (-36, 36): P.add_girder(bm, M=Matrix.Translation((x + 12, y, 22 + 2 / 12)))
part("SR_column_lines", SR, bm, [COLP], part_kind="context", note="24 ft column lines at the nave edges (y +-36 ft) for scale only")
bm = bmesh.new(); box(bm, 42.5, 53.5, -5.5, 5.5, 0, 0.5); part("SR_osler_dais", SR, bm, [MAHOG], part_kind="dais")
bm = bmesh.new(); box(bm, 40, 56, 7.5, 8.0, 0, 15); part("SR_osler_drape", SR, bm, [VELVET], part_kind="drape")   # EX09: crimson backdrop so cut glass reads (preview stand only)
POS = {"EXH_KOHINOOR": (0, 0, 0), "EXH_OSLER_CANDELABRUM": (48, 0, 0.5), "EXH_NASMYTH_HAMMER": (96, 0, 0)}
bpy.context.view_layer.layer_collection.children["EXH_ASSETS"].exclude = True   # assets render only through instances
for n, p in POS.items(): instance("EXI_" + n[4:], bpy.data.collections[n], SR, p, 0.0, part_kind="exhibit_instance", asset=n)
SK = [mat("GT_Skin_a", (0.72, 0.53, 0.42), 0.6), mat("GT_Skin_b", (0.60, 0.43, 0.33), 0.6)]
COAT = [mat("GT_Coat_blk", (0.03, 0.03, 0.035), 0.8), mat("GT_Coat_brn", (0.14, 0.10, 0.07), 0.85), mat("GT_Coat_bottle", (0.06, 0.12, 0.08), 0.85)]
DRESS = [mat("GT_Dress_plum", (0.26, 0.08, 0.16), 0.85), mat("GT_Dress_blue", (0.10, 0.16, 0.32), 0.85), mat("GT_Dress_fawn", (0.50, 0.40, 0.28), 0.85), mat("GT_Dress_grey", (0.34, 0.33, 0.36), 0.85)]
TROU = [mat("GT_Trou_fawn", (0.36, 0.31, 0.23), 0.85), mat("GT_Trou_dk", (0.10, 0.09, 0.08), 0.85)]
HAT = mat("GT_Hat", (0.02, 0.02, 0.02), 0.8); TRIM = mat("GT_Trim", (0.75, 0.74, 0.70), 0.8)
POLICE = mat("GT_Police_blue", (0.03, 0.04, 0.10), 0.8); FUST = mat("GT_Fustian", (0.30, 0.26, 0.18), 0.9)
def person(name, kind, mats, style, x, y, face_to, **props):
    me = FG.person_mesh("PM_" + name, kind, mats, style=style)
    fd = math.degrees(math.atan2(face_to[1] - y, face_to[0] - x))
    return obj(name, me, RES, (x, y, 0), math.radians(fd + 90), part_kind="figure", face_deg=fd, **props)
crowd = [  # (kind, x, y, look-at)
    ("woman", -2.6, -7.4, (0, 0)), ("man", -4.6, -6.2, (0, 0)), ("girl", -3.6, -6.9, (0, 0)), ("man", 5.8, -4.6, (0, 0)),
    ("woman", 7.5, 0.6, (0, 0)), ("man", 6.2, 4.2, (0, 0)), ("woman", -6.9, 0.6, (0, 0)), ("man", -1.0, 7.6, (0, 0)),
    ("man", 44.5, -7.5, (48, 0)), ("woman", 42.8, -6.4, (48, 0)),
    ("man", 101.0, -8.2, (96, 0)), ("woman", 103.2, -8.2, (96, 0)), ("man", 92.0, -8.1, (96, 0)), ("boy", 93.4, -7.9, (96, 0)), ("man", 108.0, -3.0, (96, 0))]
for j, (k, x, y, la) in enumerate(crowd):
    if k in ("woman", "girl"): m = [DRESS[j % 4], DRESS[(j + 1) % 4], SK[j % 2], HAT, TRIM]; st = {"skirt_w": 1.25, "shawl": j % 2 == 0}
    else: m = [COAT[j % 3], TROU[j % 2], SK[j % 2], HAT, TRIM]; st = {"hat": "top" if k == "man" else "cap", "frock": j % 2 == 1, "cravat": True}
    person(f"VIS_{j:02d}", k, m, st, x, y, la, role="visitor")
person("VIS_police", "man", [POLICE, POLICE, SK[0], HAT, TRIM], {"hat": "top", "frock": True}, 6.9, -2.8, (20, -8), role="policeman", note="Metropolitan police on duty at the Koh-i-Noor (ILN)")
person("VIS_hammer_driver", "man", [FUST, TROU[1], SK[1], HAT, TRIM], {"hat": "cap", "belt": True}, 96 + 4.6, -2.2, (96, 0), role="engine_man")
cams = CM.cameras(os.path.join(HERE, "route", "exhibit_route.json"), SR)
sc.camera = cams[0]
sc.frame_set(48)
info = {"assets": {C.name: {k: C[k] for k in C.keys() if k in ("status", "min_z_ft", "lights_built", "height_built_ft")} for C in (KC, OC, HC)},
        "figures": len(RES.objects), "cameras": [c.name for c in cams]}
t = bpy.data.texts.new("grok_info"); t.write(json.dumps(info, indent=1))
print("INFO", json.dumps(info))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True); print("SAVED", OUT)
