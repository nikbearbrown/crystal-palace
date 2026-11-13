"""CP063 CANDIDATE (2026-11-13): SY-CLEARANCE 1937 — the scrap merchants break up the frame by hand.

usage: blender -b rounds/sydenham-clearance-r17.blend -P scripts/candidate_cp063_scrap_clearance.py [-- out.blend]
       (env CP063_NOSAVE=1: build in memory only)
Opens the live CLEARANCE round (never writes it), adds dated collection
SY37_clearance_scrap_sorting_remnant__1937 and hides (never deletes) the r15/r17 solid 'rust box' scrap
piles and the 28 cone stand-ins of the crane gang. Cameras are NOT moved.
Sources (DEPARTURES D-SY-CP063-01..):
  * Crystal Palace Foundation, 'Disaster strikes, 1936': by 1937 most of the ironwork removed by W. Ward & Co. Ltd, scrap merchants.
  * Getty/Hulton (Fox Photos, Becker) 886658878, 15 Jul 1937: Buckland helps workmen pull down the last of the ironwork
    in the central transept after a controlled explosion.
  * UMD World's Fair Treasury umd:1014 (13 amateur snapshots, Thos. W. Ward of Sheffield and London): frame still standing,
    workers haul rubble; 'removal process was mostly done by hand and not with machinery'.
  * Member sizes: survey SURVEY.md (Downes 1852): column 8 in dia, top at 18'11 3/4"; girders 3 ft deep, 23'3 1/4" long;
    Sydenham params BAY = 24 ft (guide p.35); central transept span 120 ft -> column line x = -60 ft.
Units: feet (F converts). Datum z=0 = palace main floor; ground = gz(y) from build.py (copied).
"""
import bpy, bmesh, math, sys, os, random
from mathutils import Vector, Matrix

F = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P
from cpl_people import person_mesh

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP063_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-clearance-r17_cp063scrap.blend')

BD = P.BASEMENT_DEPTH
def gz(y): return -BD if y <= -84 else -1.5 + (-BD + 1.5) * (156 - y) / (156 + 84)   # build.py l.702

COL_D = 8 / 12.0                 # R: column 8 in diameter (Downes via SURVEY.md)
COL_H = 18 + 11.75 / 12          # R: column top at 18'11 3/4"
GIR_L = 23 + 3.25 / 12           # R: girder 23'3 1/4"
GIR_D = 3.0                      # R: girder 3 ft deep
STATE = 'SY-CLEARANCE_1937'
RNG = random.Random(1937)

COLL = 'SY37_clearance_scrap_sorting_remnant__1937'
col = bpy.data.collections.get(COLL) or bpy.data.collections.new(COLL)
if col.name not in [c.name for c in bpy.context.scene.collection.children]:
    bpy.context.scene.collection.children.link(col)
col['cp_state'] = STATE
col['evidence'] = 'Ward & Co clearance 1937 R; hand pull-down of last transept ironwork 15 Jul 1937 R; member sizes R; pile layout/counts I/U'

def mat(name, rgb, rough=0.7, metal=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    return m

M = dict(
    iron=mat('cp063_fire_scaled_cast_iron', (0.075, 0.060, 0.050), 0.82, 0.35),   # fire-blackened, light rust bloom (I)
    rust=mat('cp063_rust_bloom', (0.17, 0.085, 0.045), 0.9, 0.15),
    paint=mat('cp063_scorched_paint', (0.30, 0.26, 0.20), 0.85, 0.0),            # blistered pale paint on unburnt faces (I)
    cullet=mat('cp063_cullet_glass', (0.36, 0.44, 0.42), 0.22, 0.0),
    ash=mat('cp063_ash_rubble', (0.24, 0.22, 0.20), 0.95, 0.0),
    timber=mat('cp063_bearer_timber', (0.26, 0.19, 0.11), 0.85, 0.0),
    rope=mat('cp063_manila_rope', (0.42, 0.34, 0.20), 0.9, 0.0),
)

class MB:
    def __init__(self, name, m):
        self.name, self.bm, self.m = name, bmesh.new(), m
    def box(self, x0, x1, y0, y1, z0, z1, rotz=0.0, piv=None):
        r = bmesh.ops.create_cube(self.bm, size=1.0)
        T = Matrix.Translation(Vector(((x0+x1)/2, (y0+y1)/2, (z0+z1)/2)) * F) @ Matrix.Diagonal(Vector((abs(x1-x0)*F, abs(y1-y0)*F, abs(z1-z0)*F, 1)))
        if rotz:
            p = Vector(piv if piv else ((x0+x1)/2, (y0+y1)/2, 0)) * F
            T = Matrix.Translation(p) @ Matrix.Rotation(rotz, 4, 'Z') @ Matrix.Translation(-p) @ T
        bmesh.ops.transform(self.bm, matrix=T, verts=r['verts'])
    def rod(self, a, b, r, seg=10):
        """round bar / column from a to b (radius r ft)"""
        a, b = Vector(a), Vector(b); d = b - a; L = d.length
        res = bmesh.ops.create_cone(self.bm, cap_ends=True, segments=seg, radius1=r*F, radius2=r*F, depth=L*F)
        q = d.to_track_quat('Z', 'Y')
        bmesh.ops.transform(self.bm, matrix=Matrix.Translation((a + b) / 2 * F) @ q.to_matrix().to_4x4(), verts=res['verts'])
    def strut(self, a, b, w, h=None):
        h = w if h is None else h
        a, b = Vector(a), Vector(b); d = b - a; L = d.length
        res = bmesh.ops.create_cube(self.bm, size=1.0)
        q = d.to_track_quat('Z', 'Y')
        bmesh.ops.transform(self.bm, matrix=Matrix.Translation((a + b) / 2 * F) @ q.to_matrix().to_4x4()
                            @ Matrix.Diagonal(Vector((w*F, h*F, L*F, 1))), verts=res['verts'])
    def mound(self, x, y, z, rx, ry, rz, sub=2, jit=0.25, rng=RNG):
        res = bmesh.ops.create_icosphere(self.bm, subdivisions=sub, radius=1.0)
        for v in res['verts']:
            k = 1 + rng.uniform(-jit, jit)
            v.co = Vector((v.co.x * rx * k, v.co.y * ry * k, max(v.co.z, -0.05) * rz * k))
            v.co = (v.co + Vector((x, y, z))) * F
    def done(self):
        me = bpy.data.meshes.new(self.name); self.bm.to_mesh(me); self.bm.free()
        me.materials.append(self.m)
        o = bpy.data.objects.new(self.name, me); col.objects.link(o); o['cp_state'] = STATE; return o

def girder(mb, a, b, up, depth=GIR_D, flange=0.35, web=0.12, nbay=6):
    """3 ft trellis girder between a and b in the plane spanned by (b-a) and `up` (Downes: open trellis web, I for the web pattern)."""
    a, b, up = Vector(a), Vector(b), Vector(up).normalized()
    t = (b - a)
    upn = (up - up.project(t)).normalized() * depth
    mb.strut(a, b, flange, flange); mb.strut(a + upn, b + upn, flange, flange)
    for k in range(nbay + 1):
        p = a + t * (k / nbay); mb.strut(p, p + upn, web, flange * 0.8)
        if k < nbay:
            q = a + t * ((k + 1) / nbay)
            mb.strut(p, q + upn, web, flange * 0.6); mb.strut(p + upn, q, web, flange * 0.6)

# ------------------------------------------------------------------ 0. hide the r15/r17 rust-box piles and cone gang (kept in file)
HIDDEN = []
def hide(o):
    o.hide_render = True; o.hide_viewport = True; o['cp063_hidden_by_candidate'] = True; HIDDEN.append(o.name)
box_centres = []
for nm in ('clearance_scrap_piles', 'clearance_crane_fg_scrap'):
    o = bpy.data.objects[nm]; mw = o.matrix_world
    vs = [mw @ v.co for v in o.data.vertices]
    for i in range(0, len(vs) - 7, 8):          # MB.box -> create_cube: 8 verts per pile
        ch = vs[i:i + 8]
        xs = [v.x / F for v in ch]; ys = [v.y / F for v in ch]; zs = [v.z / F for v in ch]
        box_centres.append((nm, (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, min(zs), max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)))
    hide(o)
gang = [o for o in bpy.data.objects if o.name.startswith('worker_crane_')]
for o in gang: hide(o)
print('CP063 hidden', len(HIDDEN), 'piles found', len(box_centres))

# ------------------------------------------------------------------ 1. the remnant: last standing bay of the central-transept frame
# Central transept span 120 ft -> south column line x = -60 (params CT_SPAN, I); bays on COL_Y 36 / 60 (R).
# Racked 9 deg toward the gang by the haul (the 15 Jul 1937 photo shows men pulling the last ironwork down by hand).
RX, Y0, Y1 = -60.0, 36.0, 60.0
LEAN = math.radians(9)
haul_dir = Vector((-0.82, 0.33, 0)).normalized()      # gang stands back-right of the bay, side-on to the lens (I)
REM = MB('cp063_remnant_transept_bay', M['iron'])
def leaned(y_base, h, lean=LEAN):
    zb = gz(y_base)
    return Vector((RX, y_base, zb)) + haul_dir * (h * math.sin(lean)) + Vector((0, 0, h * math.cos(lean)))
for yb in (Y0, Y1):
    zb = gz(yb)
    REM.rod((RX, yb, zb - 0.5), leaned(yb, COL_H), COL_D / 2, 12)
    REM.rod((RX, yb, zb - 0.5), (RX, yb, zb + 1.2), COL_D / 2 + 0.25, 12)           # base socket / collar (I)
    REM.box(RX - 1.0, RX + 1.0, yb - 1.0, yb + 1.0, zb - 0.6, zb + 0.15)                 # base plate on its pad (I)
ta, tb = leaned(Y0, COL_H), leaned(Y1, COL_H)
upv = (leaned(Y0, 1.0) - Vector((RX, Y0, gz(Y0)))).normalized()
girder(REM, ta - upv * GIR_D, tb - upv * GIR_D, upv, nbay=8)
# a second-tier stub column snapped off above the connection (fire/blast, I)
REM.rod(tb, tb + upv * 4.2 + Vector((0, 0.6, 0)), COL_D / 2, 12)
# the bay's other girder already down, lying across its own footing (U)
g0 = Vector((RX + 2.0, Y0 - 3.0, gz(Y0) + 0.35))
girder(REM, g0, g0 + Vector((-9.0, -21.4, gz(Y0 - 24) - gz(Y0))), (0.95, -0.3, 0.12), nbay=6)
remnant = REM.done()

# ropes: two falls from the girder head back to the gang
RP = MB('cp063_haul_ropes', M['rope'])
GANG = []
for k, (attach, s0, n_men) in enumerate([(tb - upv * 0.4, 9.0, 5), (ta.lerp(tb, 0.3) - upv * 0.4, 8.0, 4)]):
    base = Vector((RX, tb.y if k == 0 else ta.lerp(tb, 0.3).y, 0))
    side = Vector((-haul_dir.y, haul_dir.x, 0)) * (1.5 if k == 0 else -1.5)
    men = []
    for j in range(n_men):
        p = base + haul_dir * (s0 + j * 3.3) + side
        p.z = gz(p.y)
        men.append(p)
    hand = lambda p: Vector((p.x, p.y, p.z + 3.6))      # ~1.1 m hand height in the hauling pose (I)
    RP.rod(attach, hand(men[0]), 0.07, 6)
    for j in range(len(men) - 1): RP.rod(hand(men[j]), hand(men[j + 1]), 0.07, 6)
    tail = men[-1] + haul_dir * 4.0; tail.z = gz(tail.y) + 0.1
    RP.rod(hand(men[-1]), tail, 0.07, 6)
    GANG += [(p, 'hauling') for p in men]
RP.done()

# ------------------------------------------------------------------ 2. sorted scrap stacks (merchants sort by kind before carting) — I
# FG-left: cut column lengths stacked on timber bearers; FG-right: girders laid flat; mid: cullet + rib heaps.
CS = MB('cp063_stack_columns', M['iron']); TB = MB('cp063_stack_bearers', M['timber'])
def column_stack(cx, cy, yaw, rows=4, per=7, L=COL_H):
    d = Vector((math.cos(yaw), math.sin(yaw), 0)); n = Vector((-d.y, d.x, 0))
    z0 = gz(cy)
    for b in (-L * 0.32, L * 0.32):
        c = Vector((cx, cy, 0)) + d * b
        TB.strut(Vector((c.x, c.y, z0 + 0.25)) - n * (per * COL_D * 0.6), Vector((c.x, c.y, z0 + 0.25)) + n * (per * COL_D * 0.6), 0.5, 0.5)
    for r in range(rows):
        cnt = per - r
        for i in range(cnt):
            off = (i - (cnt - 1) / 2) * COL_D * 1.02
            z = z0 + 0.5 + COL_D / 2 + r * COL_D * 0.87
            c = Vector((cx, cy, z)) + n * off + d * RNG.uniform(-0.8, 0.8)
            LL = L * (1.0 if RNG.random() < 0.7 else RNG.uniform(0.45, 0.7))   # some snapped at the fire-cracked joints
            CS.rod(c - d * LL / 2, c + d * LL / 2, COL_D / 2, 10)
column_stack(-41.0, 63.0, math.radians(-25))
GS = MB('cp063_stack_girders', M['iron'])
def girder_stack(cx, cy, yaw, n=5):
    d = Vector((math.cos(yaw), math.sin(yaw), 0)); w = Vector((-d.y, d.x, 0))
    z0 = gz(cy) + 0.5
    for b in (-7, 7):
        c = Vector((cx, cy, 0)) + d * b
        TB.strut(Vector((c.x, c.y, z0 - 0.25)) - w * 2.0, Vector((c.x, c.y, z0 - 0.25)) + w * 4.5, 0.5, 0.5)
    for k in range(n):
        a = Vector((cx, cy, z0 + k * 0.4)) - d * GIR_L / 2 + w * RNG.uniform(-0.3, 0.3)
        girder(GS, a, a + d * GIR_L, w, nbay=6)
girder_stack(-47.0, 44.0, math.radians(70), n=6)
# broken girder halves thrown on a heap near the crane hook (cast iron snaps rather than bends, I)
for i in range(9):
    x, y = -76 + RNG.uniform(-7, 7), 52 + RNG.uniform(-6, 6)
    ang = RNG.uniform(0, math.pi); L = RNG.uniform(7, 12)
    a = Vector((x, y, gz(y) + 0.3 + RNG.uniform(0, 2.5))); b = a + Vector((L * math.cos(ang), L * math.sin(ang), RNG.uniform(-1.5, 2.5)))
    girder(GS, a, b, (RNG.uniform(-1, 1), RNG.uniform(-1, 1), 0.6), depth=GIR_D, nbay=3)
CS.done(); GS.done()

# heaps: cullet (molten/broken glass) and ash rubble; curved wrought-iron rib segments of the transept vault (I)
CU = MB('cp063_heaps_cullet', M['cullet']); AS = MB('cp063_heaps_ash_rubble', M['ash'])
for (x, y, rx, ry, rz) in [(-92, 30, 9, 7, 2.6), (-70, 20, 7, 6, 2.0), (-100, 55, 6, 5, 1.8)]:
    CU.mound(x, y, gz(y), rx, ry, rz)
for (x, y, rx, ry, rz) in [(-62, 30, 6, 5, 1.4), (-85, 64, 8, 6, 1.6), (-110, 38, 10, 8, 2.2), (-30, 45, 5, 4, 1.0)]:
    AS.mound(x, y, gz(y), rx, ry, rz)
RB = MB('cp063_heap_vault_ribs', M['iron'])
R_V = P.CT_SPAN / 2
for i in range(7):
    cx, cy = -84 + RNG.uniform(-5, 5), 72 + RNG.uniform(-4, 4); z0 = gz(cy) + 0.4 + i * 0.5
    yaw = RNG.uniform(0, math.pi); a0 = RNG.uniform(0.2, 0.5); seg = 6; arc = 0.32
    pts = []
    for s in range(seg + 1):
        t = a0 + arc * s / seg
        u = R_V * (math.cos(t) - math.cos(a0)); h = R_V * (math.sin(t) - math.sin(a0)) * 0.25
        pts.append(Vector((cx + u * math.cos(yaw), cy + u * math.sin(yaw), z0 + abs(h) * 0.3 + RNG.uniform(0, 0.2))))
    for p, q in zip(pts, pts[1:]): RB.strut(p, q, 0.3, 0.75)   # rib section ~9 in deep (I)
RB.done(); CU.done(); AS.done()

# plateau piles: each old rust box -> a low mixed pile (ash mound + 3-5 cut members), same seeded positions
PP = MB('cp063_plateau_piles_members', M['iron']); PA = MB('cp063_plateau_piles_ash', M['ash'])
n_pp = 0
for (nm, x, y, z0, w, d, h) in box_centres:
    if nm != 'clearance_scrap_piles': continue
    PA.mound(x, y, z0, w * 0.75, d * 0.75, max(0.8, h * 0.3), sub=1)
    for k in range(RNG.randint(3, 5)):
        ang = RNG.uniform(0, math.pi); L = RNG.choice((COL_H, COL_H * 0.5, GIR_L * 0.5, 8.0))
        c = Vector((x + RNG.uniform(-2, 2), y + RNG.uniform(-2, 2), z0 + 0.4 + k * 0.6))
        dd = Vector((math.cos(ang), math.sin(ang), RNG.uniform(-0.08, 0.08))) * L / 2
        PP.rod(c - dd, c + dd, COL_D / 2, 8)
    n_pp += 1
PP.done(); PA.done()
TB.done()

# ------------------------------------------------------------------ 3. the gang: people_lib v3.4 1930s men (baked meshes), replaces the cones
def put(name, pose, p, face, seed, lod='mid'):
    person_mesh(name, '1930s_man', style={'role': '1930s_man', 'pose': pose, 'lod': lod, 'era': '1930s'}, seed=seed)
    o = bpy.data.objects[name]
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o)
    o.location = (p.x * F, p.y * F, p.z * F)
    o.rotation_euler = (0, 0, math.atan2(face[0], -face[1]))   # base meshes face local -Y
    o['cp_state'] = STATE; o['cpl_people'] = 'cpl_people_v3'
    return o
for i, (p, pose) in enumerate(GANG):          # haulers face the remnant, leaning back on the rope
    put(f'cp063_hauler_{i:02d}', pose, p, (-haul_dir.x, -haul_dir.y), 6300 + i)
LOOK = (-0.8, -0.6)                            # camera look; men within ~45 ft keep their backs to the lens
# people_lib close-up gate: nobody nearer than ~44 ft (keeps figures < ~8 % of frame height, backs or profiles only)
others = [((-63.0, 69.0), 'working', (-0.9, -0.4)), ((-58.0, 27.0), 'working', (-0.5, -0.85)),   # column / girder sorting
          ((-41.0, 40.0), 'standing', (-0.7, 0.7)),
          ((-72.0, 47.0), 'working', (-0.7, 0.7)), ((-80.0, 57.0), 'standing', (0.8, -0.3)),  # under the hook
          ((-66.0, 33.0), 'working', (0.9, 0.4)), ((-95.0, 40.0), 'walking', (1, 0.1)),
          ((-88.0, 26.0), 'working', (0.2, 1))]
for j, ((x, y), pose, face) in enumerate(others):
    put(f'cp063_ward_man_{j:02d}', pose, Vector((x, y, gz(y))), face, 6350 + j)
print('CP063 BUILT remnant + stacks + piles', n_pp, 'gang', len(GANG), 'others', len(others))

if OUT != '--nosave':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP063 SAVED', OUT)
