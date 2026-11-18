"""CP052 CANDIDATE (2026-11-18, no verdict): 'Repair never finishes' (turn of the twentieth century, SY-LATE maintenance
state) - the projecting front of the central transept on the garden side, c. 1900: glaziers on a timber pole scaffold
re-glazing the ground storey, painters on a suspended cradle and a ladder repainting the ironwork, and the bays they have
not reached yet showing weathered paint with a few rust runs - weathered, not derelict.

usage: blender -b rounds/sydenham-late11-r16.blend -P scripts/candidate_cp052_repair.py [-- out.blend]   (env CP052_NOSAVE=1: no save)
Base = rounds/sydenham-late11-r16.blend (md5 3ce48caf, unchanged since the dud-fix v4 reframe of 2026-10-27) - the blend the live
  hero renders/r16/r16_CAM_CP052_scaffold_reglaze_35mm.png (md5 9d128c5b) was rendered from by the survey dud-fix v4 script
  (look/dud_fix/scripts/reframe_and_render.py: camera saved into the blend, then look v1.1 apply_look(era/tod for CP052),
  1280x720, 32 spp; re-rendered with scripts/render_cp052_look.py: max diff 0).
  -> rounds/candidates/sydenham-late11-r16_cp052repair.blend
Live hero shows: a clean, intact two-storey glass front, no person, no tool, no scaffold outside the glass (the r16
  cov_repair_scaffold stands inside, behind the transept glazing, and reads as interior frames); nothing says 'glass needed
  replacement ... paint failed ... the palace still needed people to care for it'.
Adds ONE dated collection SY00_transept_front_glaziers_painters__c1900 (24 objects):
  * a timber pole (putlog-type independent) scaffold across three 8 ft bays of the ground storey (x -11.0..-3.7 m):
    5 in fir standards in two rows on sole boards on the garden-stair treads (one on the stair cheek), 4 in ledgers at
    4 ft 6 in lifts, 3 in putlogs, a 4-board (9 in boards) working platform at the 3rd lift with guard rail and toe board,
    a part-boarded 2nd lift carrying a glazier's crate of panes, two parallel sway braces, a lashed ladder; 2 glaziers on
    the platform (one at the glass, one carrying a new 49 x 10 in pane), a putty pail.
  * a suspended painters' cradle (13 ft x 18 in stage, rope falls to hooks over the upper band) across the upper storey
    (x -11.0..-7.0 m) with two painters and paint pots, working west; a ladder against the ground storey (x 2.35 m) with a
    third painter.
  * 'not yet reached' weathered paint west of the painters (x < -11.1 m, both storeys and both bands): thin overlay plates
    on the mullions, piers and bands in a dulled, dirtied version of the live pale paint, short rust runs below the bands,
    and two broken panes boarded with deal boards.
Sources: storyboard CP052 (turn of the twentieth century, SY-LATE maintenance: 'A glazier repairs a pane while painters work
  elsewhere; weathered fabric is shown without exaggerated dereliction'; needed: glazier and painter assets); crystal.md ch. 7
  ('glass was constantly vulnerable ... Ironwork needed protection from corrosion ... Painting alone was an enormous
  undertaking ... Neglected metal rusted ... There was always more palace'). Pole scaffolds (standards / ledgers / putlogs,
  lifts 4-5 ft, standards 6-10 ft apart, 9 in boards), suspended painters' stages and wooden ladders c. 1900: R in general
  (building-trade manuals of the period), I for this facade. Workmen in cloth caps, glaziers in dark waistcoats, painters in
  pale overalls: R in general, colours I. Placement, numbers, which bays are weathered: I.
Cameras NOT moved, sun/world/exposure/look NOT changed. Nothing deleted or hidden; architecture untouched (overlays only).
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP052_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-late11-r16_cp052repair.blend')
STATE = 'SY00_transept_front_glaziers_painters__c1900'
assert bpy.data.collections.get(STATE) is None, 'base already dressed'
FT, IN = 0.3048, 0.0254
n_before = len(bpy.data.objects)
hidden_before = sorted(o.name for o in bpy.data.objects if o.hide_render)
sc = bpy.context.scene
col = bpy.data.collections.new(STATE); sc.collection.children.link(col)
CAM = bpy.data.objects['CAM_CP052_scaffold_reglaze_35mm']
C = CAM.location.copy()
RNG = random.Random(1900052)
INFO = {}

# ------------------------------------------------------------------ base geometry (read from r16, 2026-11-18 ray sweeps)
Y_GF = -62.225          # ground-storey glass/mullion front (piers at -62.316)
Y_PIER_GF = -62.316
Y_UF = -59.787          # upper-storey mullion front (piers -59.878)
Y_PIER_UF = -59.878
Y_BAND1 = -62.36        # band between storeys, z 5.85..6.76 (SY_central_transept_frame front)
Y_BAND2 = -59.92        # band above upper storey, z 11.94..12.86
Z_GF0, Z_GF1, Z_B1_0, Z_B1_1, Z_UF0, Z_UF1, Z_B2_1 = 0.19, 5.85, 5.85, 6.76, 6.95, 11.94, 12.86
MULLS = [(-18.42, 0.27), (-15.89, 0.09), (-13.45, 0.09), (-11.10, 0.27), (-8.58, 0.10), (-6.14, 0.09), (-3.79, 0.27), (-1.26, 0.09), (1.18, 0.09),
         (3.53, 0.27), (6.06, 0.09), (8.49, 0.10), (10.84, 0.27), (13.37, 0.09), (15.81, 0.09), (18.16, 0.27)]   # (x start, width) m

_vis = {}
for o in bpy.data.objects:
    _vis[o.name] = o.hide_viewport; o.hide_viewport = o.hide_render
dg = bpy.context.evaluated_depsgraph_get()
def ground(x, y):   # base-scene surface only (rays pass through anything this script adds)
    o = Vector((x, y, 30.0))
    for _ in range(20):
        hit, loc, nor, idx, ob, _m = sc.ray_cast(dg, o, Vector((0, 0, -1)))
        if not hit: return (None, None)
        if ob.get('cp_state') != STATE: return (loc.z, ob.name)
        o = loc - Vector((0, 0, 0.001))
    return (None, None)

# ------------------------------------------------------------------ materials
def pmat(name, rgb, rough=0.8, metal=0.0):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name); m.use_nodes = True
        b = m.node_tree.nodes.get('Principled BSDF'); b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough
        b.inputs['Metallic'].default_value = metal
        m.diffuse_color = (*rgb, 1); m['cp_state'] = STATE
    return m
POLE = pmat('cp052_fir_pole_weathered', (0.15, 0.12, 0.085), 0.85)
BOARD = pmat('cp052_scaffold_board_deal', (0.22, 0.175, 0.12), 0.85)
DEAL = pmat('cp052_boarded_pane_deal', (0.17, 0.135, 0.095), 0.85)
ROPE = pmat('cp052_hemp_rope', (0.30, 0.26, 0.19), 0.9)
IRON = pmat('cp052_wrought_hook', (0.05, 0.05, 0.05), 0.6, 0.6)
CRATE = pmat('cp052_glass_crate_deal', (0.24, 0.19, 0.13), 0.85)
PAIL = pmat('cp052_pail_tin', (0.20, 0.20, 0.21), 0.5, 0.5)
PAINT_LIVE = pmat('cp052_paint_pot_pale', (0.70, 0.70, 0.66), 0.5)
WEATHER = pmat('cp052_weathered_paint', (0.34, 0.315, 0.26), 0.75)      # the live 'iron_exterior_pale' is 0.74/0.74/0.70
WEATHER_B = pmat('cp052_weathered_paint_band', (0.37, 0.345, 0.285), 0.75)
RUST = pmat('cp052_rust_run', (0.28, 0.13, 0.06), 0.8)
def glass_mat():
    m = bpy.data.materials.get('cp052_new_pane_glass')
    if m: return m
    m = bpy.data.materials.new('cp052_new_pane_glass'); m.use_nodes = True
    b = m.node_tree.nodes.get('Principled BSDF'); b.inputs['Base Color'].default_value = (0.80, 0.88, 0.86, 1)
    b.inputs['Roughness'].default_value = 0.08; b.inputs['Transmission Weight'].default_value = 0.6; b.inputs['IOR'].default_value = 1.52
    m.diffuse_color = (0.6, 0.7, 0.7, 1); m['cp_state'] = STATE; return m
GLASS = glass_mat()

# ------------------------------------------------------------------ mesh helpers
def new_obj(name, bm, mat):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
    o = bpy.data.objects.new(name, me); col.objects.link(o); o['cp_state'] = STATE; return o
def cyl(bm, p0, p1, r, seg=8):
    p0, p1 = Vector(p0), Vector(p1); ax = p1 - p0; L = ax.length; axn = ax.normalized()
    up = Vector((0, 0, 1)) if abs(axn.z) < 0.95 else Vector((1, 0, 0))
    u = axn.cross(up).normalized(); v = axn.cross(u).normalized()
    ra = [bm.verts.new(p0 + (u * math.cos(2 * math.pi * k / seg) + v * math.sin(2 * math.pi * k / seg)) * r) for k in range(seg)]
    rb = [bm.verts.new(p1 + (u * math.cos(2 * math.pi * k / seg) + v * math.sin(2 * math.pi * k / seg)) * r) for k in range(seg)]
    for k in range(seg):
        j = (k + 1) % seg; bm.faces.new((ra[k], ra[j], rb[j], rb[k]))
    bm.faces.new(list(reversed(ra))); bm.faces.new(rb)
def box(bm, c, s):
    (cx, cy, cz), (sx, sy, sz) = c, s
    vs = [bm.verts.new((cx + dx * sx / 2, cy + dy * sy / 2, cz + dz * sz / 2)) for dx in (-1, 1) for dy in (-1, 1) for dz in (-1, 1)]
    for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)): bm.faces.new([vs[i] for i in f])
def beam(bm, p0, p1, w, h):   # rectangular timber from p0 to p1 (w horizontal, h vertical-ish)
    p0, p1 = Vector(p0), Vector(p1); ax = (p1 - p0).normalized()
    up = Vector((0, 0, 1)) if abs(ax.z) < 0.95 else Vector((0, 1, 0))
    s1 = ax.cross(up).normalized() * w / 2; s2 = s1.cross(ax).normalized() * h / 2
    vs = [bm.verts.new(p + a + b) for p in (p0, p1) for a, b in ((s1, s2), (-s1, s2), (-s1, -s2), (s1, -s2))]
    for f in ((0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)): bm.faces.new([vs[i] for i in f])
def plate_y(bm, x0, x1, z0, z1, y):   # vertical plate facing -Y at y
    vs = [bm.verts.new((x, y, z)) for x, z in ((x0, z0), (x1, z0), (x1, z1), (x0, z1))]; bm.faces.new(vs)

# ------------------------------------------------------------------ A. glaziers' pole scaffold, ground storey x -11.0..-3.7
SX = [-10.97, -8.53, -6.10, -3.66]                 # standards on the mullion lines (8 ft bays)
Y_IN, Y_OUT = Y_PIER_GF - 0.30, Y_PIER_GF - 0.30 - 1.12   # inner / outer standard rows (3 ft 8 in apart: 4 x 9 in boards + gaps)
R_STD, R_LED = 2.5 * IN, 2.0 * IN                  # 5 in standards, 4 in ledgers
LIFT = 4.5 * FT
Z_LIFTS = [LIFT * k for k in (1, 2, 3)]            # 1.37, 2.74, 4.11 m above the main-floor line (z 0)
Z_PLAT = Z_LIFTS[2] + R_LED + 3 * IN               # board top: ledger + putlog (3 in) ... boards 2 in below this
Z_TOP = Z_PLAT + 3.5 * FT                          # standards run 3 ft 6 in above the platform (guard rail)
bm = bmesh.new(); feet = []
for x in SX:
    for y in (Y_IN, Y_OUT):
        gz, gname = ground(x, y); feet.append((x, y, gz, gname))
        cyl(bm, (x, y, gz + 2 * IN), (x, y, Z_TOP), R_STD)
std = new_obj('cp052_scaffold_standards', bm, POLE)
FOOT = {(x, y): gz for x, y, gz, _ in feet}   # stair-tread heights measured before anything was added
bm = bmesh.new()
for x, y, gz, _ in feet:                           # sole boards on the stair treads (9 x 2 in deal, 3 ft)
    box(bm, (x, y, gz + IN), (9 * IN, 3 * FT, 2 * IN))
sole = new_obj('cp052_scaffold_sole_boards', bm, BOARD)
bm = bmesh.new()
for z in Z_LIFTS + [Z_PLAT + 3.0 * FT]:            # ledgers both rows (+ guard rail on the outer row only)
    for y in ((Y_IN, Y_OUT) if z in Z_LIFTS else (Y_OUT,)):
        cyl(bm, (SX[0] - 0.35, y - R_STD - R_LED, z), (SX[-1] + 0.35, y - R_STD - R_LED, z), R_LED)
# lower ledger pair at the first lift also sits below frame; keep for structure. Sway braces on the outer face
for a, b in ((0, 1), (2, 3)):   # two parallel sway braces, foot to 3rd lift
    cyl(bm, (SX[a], Y_OUT - R_STD - 2 * R_LED - 0.02, FOOT[(SX[a], Y_OUT)] + 0.3), (SX[b], Y_OUT - R_STD - 2 * R_LED - 0.02, Z_LIFTS[2] + 0.1), R_LED)
led = new_obj('cp052_scaffold_ledgers_braces', bm, POLE)
bm = bmesh.new()                                    # putlogs: 3 x 3 in, across both rows, one per standard pair + mid-bay
for z in Z_LIFTS[1:]:
    for x in SX + [(SX[k] + SX[k + 1]) / 2 for k in range(3)]:
        beam(bm, (x, Y_OUT - 0.25, z + R_LED + 1.5 * IN), (x, Y_PIER_GF - 0.05, z + R_LED + 1.5 * IN), 3 * IN, 3 * IN)
put_o = new_obj('cp052_scaffold_putlogs', bm, POLE)
bm = bmesh.new()                                    # boards: 9 x 2 in; 4 across at the platform, 2 at the 2nd lift (part-boarded)
BW, BT = 9 * IN, 2 * IN
def boards(z, n, y0):
    for k in range(n):
        y = y0 - BW / 2 - k * (BW + 0.6 * IN)
        box(bm, ((SX[0] + SX[-1]) / 2, y, z + BT / 2), (SX[-1] - SX[0] + 0.30, BW, BT))
boards(Z_PLAT, 4, Y_PIER_GF - 0.08)
box(bm, ((SX[0] + SX[-1]) / 2, Y_OUT - 0.08, Z_PLAT + BT + 4.5 * IN), (SX[-1] - SX[0] + 0.30, 1.5 * IN, 9 * IN))   # toe board
bm2 = bm; boards(Z_LIFTS[1] + R_LED + 3 * IN, 2, Y_PIER_GF - 0.08)
brd = new_obj('cp052_scaffold_boards', bm2, BOARD)
# ladder lashed to the outer row at the east end, foot on the stairs, through the platform guard
def ladder(name, foot, top, width=16 * IN, rung=10 * IN):
    foot, top = Vector(foot), Vector(top); ax = (top - foot); L = ax.length; axn = ax.normalized()
    side = Vector((1, 0, 0)) if abs(axn.x) < 0.9 else Vector((0, 1, 0))
    side = (side - axn * side.dot(axn)).normalized() * width / 2
    b = bmesh.new()
    for s in (-1, 1): beam(b, foot + side * s, top + side * s, 2 * IN, 3.5 * IN)
    n = int(L / rung)
    for k in range(1, n + 1):
        p = foot + axn * (k * rung)
        cyl(b, p - side, p + side, 0.6 * IN, 6)
    return new_obj(name, b, POLE), n
gz_l = ground(SX[-1] + 0.55, Y_OUT - 0.9)[0]
lad1, lad1_n = ladder('cp052_scaffold_ladder', (SX[-1] + 0.55, Y_OUT - 0.95, gz_l), (SX[-1] + 0.55, Y_OUT - 0.12, Z_PLAT + 3.2 * FT))
INFO['scaffold_feet_z'] = sorted({round(f[2], 2) for f in feet}); INFO['scaffold_feet_on'] = sorted({f[3] for f in feet})
INFO['platform_board_top_m'] = round(Z_PLAT + BT, 3)

# glazier's crate (deal frame, panes on edge) on the 2nd lift, putty pail on the platform
bm = bmesh.new(); cx, cy, cz = -9.75, Y_PIER_GF - 0.30, Z_LIFTS[1] + R_LED + 3 * IN + BT
for dx in (-0.62, 0.62):
    for dy in (-0.13, 0.13): beam(bm, (cx + dx, cy + dy, cz), (cx + dx, cy + dy, cz + 0.75), 2 * IN, 2 * IN)
for dz in (0.03, 0.72):
    for dy in (-0.13, 0.13): beam(bm, (cx - 0.64, cy + dy, cz + dz), (cx + 0.64, cy + dy, cz + dz), 1 * IN, 3 * IN)
crate = new_obj('cp052_glass_crate', bm, CRATE)
bm = bmesh.new()
for k in range(5): box(bm, (cx, cy - 0.08 + k * 0.04, cz + 0.36), (1.245, 0.006, 0.66))
crate_g = new_obj('cp052_glass_crate_panes', bm, GLASS)
bm = bmesh.new(); px, py = -5.2, Y_PIER_GF - 0.55
cyl(bm, (px, py, Z_PLAT + BT), (px, py, Z_PLAT + BT + 0.22), 0.13, 12)
pail = new_obj('cp052_putty_pail', bm, PAIL)

# ------------------------------------------------------------------ B. painters' suspended cradle, upper storey x -11.0..-7.0
Z_STAGE = 8.05; CX0, CX1 = -10.98, -10.98 + 13 * FT; CY = Y_PIER_UF - 0.55
bm = bmesh.new()
box(bm, ((CX0 + CX1) / 2, CY, Z_STAGE - 1 * IN), (CX1 - CX0, 18 * IN, 2 * IN))           # stage plank 18 in wide
for x in (CX0 + 0.15, CX1 - 0.15):                                                      # stirrups (end frames) + guard rail
    beam(bm, (x, CY - 0.26, Z_STAGE - 0.05), (x, CY - 0.26, Z_STAGE + 1.0), 2 * IN, 2 * IN)
    beam(bm, (x, CY + 0.26, Z_STAGE - 0.05), (x, CY + 0.26, Z_STAGE + 1.0), 2 * IN, 2 * IN)
    beam(bm, (x, CY - 0.26, Z_STAGE + 1.0), (x, CY + 0.26, Z_STAGE + 1.0), 2 * IN, 2 * IN)
beam(bm, (CX0 + 0.15, CY - 0.26, Z_STAGE + 0.95), (CX1 - 0.15, CY - 0.26, Z_STAGE + 0.95), 2 * IN, 2 * IN)
stage = new_obj('cp052_painters_cradle', bm, BOARD)
bm = bmesh.new()
for x in (CX0 + 0.15, CX1 - 0.15):                                                      # rope falls to hooks over the upper band
    cyl(bm, (x, CY, Z_STAGE + 1.0), (x, Y_BAND2 - 0.10, Z_B2_1 + 0.05), 0.75 * IN, 6)
    cyl(bm, (x + 0.06, CY, Z_STAGE + 1.0), (x + 0.06, Y_BAND2 - 0.10, Z_B2_1 + 0.05), 0.75 * IN, 6)
ropes = new_obj('cp052_cradle_rope_falls', bm, ROPE)
bm = bmesh.new()
for x in (CX0 + 0.15, CX1 - 0.15):
    beam(bm, (x, Y_BAND2 - 0.12, Z_B2_1 + 0.06), (x, Y_BAND2 + 0.6, Z_B2_1 + 0.06), 1.5 * IN, 0.75 * IN)
    beam(bm, (x, Y_BAND2 - 0.12, Z_B2_1 + 0.06), (x, Y_BAND2 - 0.12, Z_B2_1 - 0.20), 1.5 * IN, 0.75 * IN)
hooks = new_obj('cp052_cradle_hooks', bm, IRON)
bm = bmesh.new()
for x in (CX0 + 1.15, CX1 - 1.55):
    cyl(bm, (x, CY + 0.05, Z_STAGE), (x, CY + 0.05, Z_STAGE + 0.20), 0.09, 12)
pots = new_obj('cp052_cradle_paint_pots', bm, PAINT_LIVE)
# painter's ladder against the ground storey, east half of the front
LX = 2.35; gz_p = ground(LX, Y_GF - 1.45)[0]
lad2, lad2_n = ladder('cp052_painters_ladder', (LX, Y_GF - 1.45, gz_p), (LX, Y_GF - 0.10, 5.55))
INFO['painter_ladder_foot'] = (round(gz_p, 2), ground(LX, Y_GF - 1.45)[1])

# ------------------------------------------------------------------ C. weathered (not yet repainted) bays west of the painters
bm = bmesh.new(); nw = 0
for x0, w in MULLS:
    yf = Y_PIER_GF if w > 0.2 else Y_GF; yu = Y_PIER_UF if w > 0.2 else Y_UF
    if x0 < -11.05:   # west end bays (+ the west pier) not yet reached, both storeys; the cradle works its way west
        plate_y(bm, x0 - 0.005, x0 + w + 0.005, Z_GF0, Z_GF1, yf - 0.006); nw += 1
        plate_y(bm, x0 - 0.005, x0 + w + 0.005, Z_UF0, Z_UF1, yu - 0.006); nw += 1
wea = new_obj('cp052_weathered_paint_mullions', bm, WEATHER)
bm = bmesh.new()
plate_y(bm, -18.43, -11.10, Z_B1_0, Z_B1_1, Y_BAND1 - 0.006)                           # band between storeys, west part
plate_y(bm, -18.43, -11.10, Z_UF1, Z_B2_1, Y_BAND2 - 0.006)                             # upper band, west part
weab = new_obj('cp052_weathered_paint_bands', bm, WEATHER_B)
bm = bmesh.new(); runs = 0
for x0, w in MULLS:
    if x0 > -11.05: continue
    for (zt, yb) in ((Z_B1_0, Y_BAND1), (Z_UF1, Y_BAND2)):                              # runs from the band soffits down the mullion face
        L = RNG.uniform(0.5, 1.3); xc = x0 + w / 2 + RNG.uniform(-0.01, 0.01); hw = min(0.035, w / 2 - 0.005)
        yf = (Y_PIER_GF if w > 0.2 else Y_GF) if zt == Z_B1_0 else (Y_PIER_UF if w > 0.2 else Y_UF)
        plate_y(bm, xc - hw, xc + hw, zt - L, zt - 0.01, yf - 0.009); runs += 1
        plate_y(bm, xc - hw * 0.6, xc + hw * 0.6, zt - L - RNG.uniform(0.3, 0.8), zt - L, yf - 0.009); runs += 1   # thinning tail
rust = new_obj('cp052_rust_runs', bm, RUST)
INFO['weathered_plates'] = nw; INFO['rust_runs'] = runs
# two broken panes boarded with deal (3 boards, 9 in, with gaps)
bm = bmesh.new()
for (xc, zc, yf) in ((-14.65, 3.05, Y_GF), (-12.30, 9.55, Y_UF)):
    for k in (-1, 0, 1):
        plate_y(bm, xc + k * 0.245 - 0.11, xc + k * 0.245 + 0.11, zc - 0.48, zc + 0.48, yf - 0.03)
bpan = new_obj('cp052_boarded_panes', bm, DEAL)

# ------------------------------------------------------------------ D. the workmen (people_lib v3.4 1850s_workman: cloth cap, smock slot re-coloured)
from cpl_people import person_mesh
people = []
GLAZIER = (0.075, 0.065, 0.055)    # dark waistcoat / shirt
PAINTER = (0.46, 0.44, 0.39)       # pale painters' overalls (mid, not chalk: the frame is bright)
def put(name, pose, x, y, z, yaw, seed, coat):
    person_mesh(name, '1850s_workman', style={'role': '1850s_workman', 'pose': pose, 'lod': 'hero', 'era': '1850s'}, seed=seed)
    o = bpy.data.objects[name]
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o.location = (x, y, z + 0.005); o.rotation_euler = (0, 0, yaw)
    o['cpl_people'] = 'cpl_people_v3'; o['cp_state'] = STATE
    for s in o.material_slots:
        if s.material and s.material.name.startswith('CPL3_smock'):
            s.link = 'OBJECT'; s.material = pmat('cp052_workdress_%s' % ('painter' if coat == PAINTER else 'glazier'), coat, 0.85)
    people.append(o); return o
TO_GLASS = math.pi                         # meshes face local -Y; yaw pi = facing +Y (the facade)
zb = Z_PLAT + BT
g1 = put('cp052_glazier_at_glass', 'working', -7.35, Y_PIER_GF - 0.42, zb, TO_GLASS, 1900521, GLAZIER)
g2 = put('cp052_glazier_with_pane', 'standing', -9.55, Y_PIER_GF - 0.62, zb, TO_GLASS + 0.9, 1900526, GLAZIER)
bpy.context.view_layer.update()
# the new pane he carries: 49 x 10 in, held flat-faced across his body at chest height
bm = bmesh.new(); box(bm, (0, 0, 0), (1.245, 0.006, 0.254)); pane = new_obj('cp052_new_pane_carried', bm, GLASS)
pane.parent = g2; pane.location = (0.0, -0.30, 1.15); pane.rotation_euler = (0, 0, 0)
p1 = put('cp052_painter_cradle_w', 'working', CX0 + 0.60, CY + 0.02, Z_STAGE, TO_GLASS, 1900531, PAINTER)
p2 = put('cp052_painter_cradle_e', 'working', CX1 - 0.95, CY + 0.02, Z_STAGE, TO_GLASS, 1900534, PAINTER)
# ladder painter: feet on a round ~2.3 m up the ladder
t = (2.30 - gz_p) / (5.55 - gz_p); ly = (Y_GF - 1.45) + t * 1.35
p3 = put('cp052_painter_on_ladder', 'working', LX, ly - 0.22, 2.30, TO_GLASS, 1900537, PAINTER)

for o in bpy.data.objects:
    if o.name in _vis: o.hide_viewport = _vis[o.name]
col['cp_state'] = STATE
col['evidence'] = ('storyboard CP052 turn of the 20th century, glazier repairs a pane while painters work elsewhere, weathered not derelict (R as brief); '
                   'crystal.md ch.7 glass constantly vulnerable / ironwork protection / painting an enormous undertaking / neglected metal rusted (R as text); '
                   'pole scaffold, painters cradle and ladders c.1900 (R in general, I here); dress colours, placement, weathered bays I')
bpy.context.view_layer.update()
d = [((o.matrix_world.translation - C).length) for o in people]
INFO['workmen'] = len(people); INFO['nearest_figure_m'] = round(min(d), 2); INFO['farthest_figure_m'] = round(max(d), 2)
INFO['objects'] = len(col.objects); INFO['new_objects_total'] = len(bpy.data.objects) - n_before
assert sorted(o.name for o in bpy.data.objects if o.hide_render) == hidden_before
assert len(bpy.data.objects) - n_before == len(col.objects), 'every new object must be in the one dated collection'
print('CP052 BUILT', INFO)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP052 SAVED', OUT)
