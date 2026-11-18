"""CP040 CANDIDATE (2026-11-18, no verdict): 'Walking through arranged history' - the English Mediaeval Court (Digby Wyatt,
opened 10 Jun 1854) dressed after Phillips' 1854 Guide: the Rochester doorway coloured, the niches and canopies round the walls,
the upper tier of large statues beneath canopies, and two of the floor's sepulchral monuments.

usage: blender -b rounds/sydenham-1856-r14.blend -P scripts/candidate_cp040_mediaeval.py [-- out.blend]  (env CP040_NOSAVE=1: no save)
Base = rounds/sydenham-1856-r14.blend (md5 00df0959, unchanged since 1c96ad7) - the blend the live CP040 hero
  renders/r14_1856_CAM_CP040_mediaeval_court_28mm.png was rendered from (survey look v1.1, look/sydenham_logs/CP040.log:
  apply_render.py --scene-id CP040 --era 1851 --tod interior_daylit --spp 24 --res 1280x720 --no-people; re-render max diff 0).
  -> rounds/candidates/sydenham-1856-r14_cp040mediaeval.blend
Live hero shows: the Rochester doorway as plain grey stone (left edge), the court's back (garden) wall and the west wall below
  the stained glass as bare cream plaster (about a third of the frame), two plain white blocks on the floor (the r13 tomb-chest
  massing and the font), pv57 cone visitors in the foreground.
Sources (S. Phillips, Guide to the Crystal Palace and Park, 1854, 'The English Mediaeval Court', pp. 81-84; archive.org
  guidetocrystalpa00phil_0):
  'the magnificent door-way from Rochester Cathedral, coloured so as to give an idea of its appearance when first erected ...
   the practice of colouring and gilding was carried to an almost extravagant extent in the Gothic style' (R: coloured; scheme I)
  'The exquisite niches and canopies round the walls of the court are from Southwell Minster, Ely Cathedral, Beverley Minster'
   (R: niches + canopies round the walls; bay design generic Decorated I)
  'The upper tier, consisting principally of sculpture ... The large statues beneath the canopies are from the facade of Wells'
   (R: upper tier of large statues under canopies; figures generic U)
  'The floor presents a remarkable ... series of the best sepulchral monuments ... Queen Eleanor, from Westminster; Edward II.,
   from Gloucester; ... William of Wykeham ... and that of Edward the Black Prince, from Canterbury' (R: monuments on the floor;
   two of the four modelled, positions I, dimensions approximate I).
Adds dated collection SY54_english_mediaeval_court_dressed__1854_1856 (cp_state on every object). Camera NOT moved,
sun/world/exposure/look NOT changed, nothing hidden or deleted; additions only (paint is applied as thin overlay plates
0.012-0.03 ft proud of the r14 door faces, the r14 stone is untouched).
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector, Matrix

F = 0.3048
f = lambda v: v * F
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP040_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-1856-r14_cp040mediaeval.blend')
STATE = 'SY54_english_mediaeval_court_dressed__1854_1856'
RNG = random.Random(1854400)
CAM = bpy.data.objects['CAM_CP040_mediaeval_court_28mm']
MC = bpy.data.collections['SY54_court_mediaeval__dated']
parent = next(c for c in bpy.data.collections if MC.name in [k.name for k in c.children])
col = bpy.data.collections.get(STATE) or bpy.data.collections.new(STATE)
if col.name not in [c.name for c in parent.children]: parent.children.link(col)
col['cp_state'] = STATE
col['evidence'] = ('Phillips 1854 pp.81-84: Rochester doorway coloured as when first erected R (scheme I); niches and canopies round '
                   'the walls (Southwell, Ely, Beverley) R (bay design I); upper tier of large statues beneath canopies (Wells facade) R '
                   '(figures U); floor monuments Queen Eleanor + Black Prince R (2 of 4, positions I, dimensions approx. I)')
INFO = {}

# ---------------------------------------------------------------- r14 court geometry (scripts/courts2.py, ft)
MX0, MX1, MY0, MY1 = 392.0, 490.0, -116.0, -46.0
BACK = MY0 + 1.0          # back (garden) wall court face, y -115.0, normal +Y
WEST = MX0 + 1.0          # west wall court face, x 393.0, normal +X
RCX = 432.0; FYR = BACK; DEP = 0.9
Z0 = 0.05                 # tile floor top
WIN = (-81.6, -62.4)      # west lancet group incl. dark surrounds (-80.9..-63.1) + 0.7 ft margin; glass sill z 6.0 (surround 5.5)
HOOD_X0 = RCX - 9.5       # Rochester hood / outer order west edge, x 422.5

# ---------------------------------------------------------------- materials
def mat(name, base, rough=0.6, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*base, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal; return m
M = {k: mat('cp040_' + k, c, r, mt) for k, (c, r, mt) in {
    'cast':   ((0.78, 0.74, 0.64), 0.75, 0.0),    # plaster cast, stone-coloured (matches med_stone 0.74/0.70/0.60)
    'castd':  ((0.66, 0.62, 0.53), 0.80, 0.0),    # shaded mouldings
    'purbeck':((0.17, 0.17, 0.15), 0.35, 0.0),    # Purbeck marble shafts / tomb chests
    'red':    ((0.52, 0.09, 0.06), 0.60, 0.0),
    'blue':   ((0.07, 0.13, 0.36), 0.60, 0.0),
    'green':  ((0.10, 0.27, 0.15), 0.60, 0.0),
    'gilt':   ((0.80, 0.58, 0.22), 0.35, 0.75),
    'gilt_e': ((0.70, 0.52, 0.24), 0.45, 0.60),   # effigy gilt-bronze / latten
    'pbk2':   ((0.30, 0.29, 0.26), 0.45, 0.0),    # Purbeck panel mouldings
    'blk':    ((0.05, 0.05, 0.05), 0.55, 0.0),
    'wht':    ((0.85, 0.83, 0.78), 0.55, 0.0),
}.items()}
BM = {k: bmesh.new() for k in M}

# ---------------------------------------------------------------- helpers (ft in, metres out)
def box(k, x0, x1, y0, y1, z0, z1):
    bm = BM[k]; x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    r = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(f(x1 - x0), f(y1 - y0), f(z1 - z0)), verts=r['verts'])
    bmesh.ops.translate(bm, vec=(f((x0 + x1) / 2), f((y0 + y1) / 2), f((z0 + z1) / 2)), verts=r['verts'])
def poly(k, pts):
    bm = BM[k]; bm.faces.new([bm.verts.new((f(x), f(y), f(z))) for x, y, z in pts])
def cyl(k, x, y, z0, z1, r0, r1, seg=12):
    bm = BM[k]; r = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=f(r0), radius2=f(r1), depth=f(z1 - z0))
    bmesh.ops.translate(bm, vec=(f(x), f(y), f((z0 + z1) / 2)), verts=r['verts'])
def ell(k, c, r, seg=16, rings=10, Mx=None):
    bm = BM[k]; s = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0)
    for v in s['verts']:
        p = Vector((v.co.x * r[0], v.co.y * r[1], v.co.z * r[2]))
        if Mx is not None: p = Mx @ p
        v.co = Vector((f(c[0] + p.x), f(c[1] + p.y), f(c[2] + p.z)))
class Wall:
    """local wall frame: u along the wall, d out of the wall face (into the court), z up"""
    def __init__(s, which): s.w = which
    def P(s, u, d, z): return (u, BACK + d, z) if s.w == 'back' else (WEST + d, u, z)
    def box(s, k, u0, u1, d0, d1, z0, z1):
        a, b = s.P(u0, d0, z0), s.P(u1, d1, z1); box(k, a[0], b[0], a[1], b[1], a[2], b[2])
    def plate(s, k, d, pts):           # polygon (u, z) facing the court
        q = [s.P(u, d, z) for u, z in pts]
        if s.w == 'west': q = q[::-1]
        poly(k, q)
    def prism(s, k, d0, d1, pts):      # extruded polygon (u, z) between depths d0..d1
        bm = BM[k]
        A = [bm.verts.new(tuple(f(c) for c in s.P(u, d1, z))) for u, z in pts]
        B = [bm.verts.new(tuple(f(c) for c in s.P(u, d0, z))) for u, z in pts]
        fa, fb = (A, B[::-1]) if s.w == 'back' else (A[::-1], B)
        bm.faces.new(fa); bm.faces.new(fb)
        n = len(pts)
        for i in range(n):
            j = (i + 1) % n; q = (A[i], B[i], B[j], A[j]) if s.w == 'back' else (A[j], B[j], B[i], A[i])
            bm.faces.new(q)
    def cyl(s, k, u, d, z0, z1, r, seg=10):
        p = s.P(u, d, 0); cyl(k, p[0], p[1], z0, z1, r, r, seg)
def arch(u0, w, zs, n=8):
    """equilateral pointed arch outline over opening u0 +- w/2 springing at zs, left springer -> apex -> right springer"""
    L = [(u0 + w / 2 + w * math.cos(math.radians(180 - 60 * i / n)), zs + w * math.sin(math.radians(180 - 60 * i / n))) for i in range(n + 1)]
    R = [(u0 - w / 2 + w * math.cos(math.radians(60 - 60 * i / n)), zs + w * math.sin(math.radians(60 - 60 * i / n))) for i in range(1, n + 1)]
    return L + R
def niche_back(Wl, k, u0, w, z0, zs):
    Wl.plate(k, 0.04, [(u0 - w / 2, z0), (u0 + w / 2, z0)] + arch(u0, w, zs)[::-1])
def gable(Wl, kf, kc, u0, half, zb, h, d0, d1, crockets=True):
    Wl.prism(kf, d0, d1, [(u0 - half, zb), (u0 + half, zb), (u0, zb + h)])
    if crockets:
        n = 3
        for i in range(1, n + 1):
            t = i / (n + 1)
            for sgn in (-1, 1):
                uu = u0 + sgn * half * (1 - t); zz = zb + h * t
                Wl.box(kc, uu - 0.13, uu + 0.13, d1 - 0.05, d1 + 0.12, zz + 0.05, zz + 0.32)
    Wl.box(kc, u0 - 0.14, u0 + 0.14, d0, d1 + 0.05, zb + h, zb + h + 0.55)         # finial
    Wl.box(kc, u0 - 0.26, u0 + 0.26, d0, d1 + 0.1, zb + h + 0.30, zb + h + 0.46)
def pinnacle(Wl, k, u0, d0, d1, z0, z1):
    Wl.box(k, u0 - 0.24, u0 + 0.24, d0, d1, z0, z1)
    a = Wl.P(u0 - 0.30, (d0 + d1) / 2 - 0.30, z1); b = Wl.P(u0 + 0.30, (d0 + d1) / 2 + 0.30, z1)
    cx, cy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; cyl(k, cx, cy, z1, z1 + 1.3, 0.40, 0.02, seg=4)

def statue(Wl, u0, dbase, z0, H, kind, seed):
    """standing draped figure (Wells facade type, generic U): lathe-turned robe with vertical folds, mantle, head, crown/mitre;
    flattened front-to-back; stone colour (cast)"""
    R = random.Random(seed); bm = BM['cast']
    nseg, nr = 24, 14; prof = [(0.00, 0.58), (0.06, 0.62), (0.30, 0.56), (0.55, 0.47), (0.70, 0.45), (0.78, 0.43), (0.84, 0.30), (0.86, 0.14)]
    rows = []
    for i in range(nr + 1):
        t = i / nr * 0.86
        for j in range(len(prof) - 1):
            if prof[j][0] <= t <= prof[j + 1][0]:
                a = (t - prof[j][0]) / (prof[j + 1][0] - prof[j][0]); rr = prof[j][1] * (1 - a) + prof[j + 1][1] * a; break
        ring = []
        for j in range(nseg):
            th = 2 * math.pi * j / nseg
            fold = 1.0 + (0.07 * math.sin(6 * th + R.uniform(0, 0.4)) * (1 - t / 0.86) if t < 0.70 else 0.0)
            x = 1.45 * rr * fold * math.cos(th); y = 0.80 * rr * fold * math.sin(th)       # ~1.8 ft across the shoulders
            p = Wl.P(u0 + x * H / 6.3, dbase + 0.62 + y * H / 6.3, z0 + t * H)
            ring.append(bm.verts.new(tuple(f(c) for c in p)))
        rows.append(ring)
    for i in range(nr):
        for j in range(nseg):
            jj = (j + 1) % nseg; bm.faces.new((rows[i][j], rows[i][jj], rows[i + 1][jj], rows[i + 1][j]))
    bm.faces.new(rows[0][::-1]); bm.faces.new(rows[-1])
    s = H / 6.3
    c = Wl.P(u0, dbase + 0.66, z0 + 0.93 * H)
    ell('cast', c, (0.34 * s, 0.32 * s, 0.42 * s), 14, 10)                                   # head
    c2 = Wl.P(u0, dbase + 0.95, z0 + 0.62 * H)
    ell('cast', c2, (0.26 * s, 0.20 * s, 0.30 * s) if Wl.w == 'back' else (0.20 * s, 0.26 * s, 0.30 * s), 10, 8)   # hands / book on the breast
    if kind == 'king':
        p = Wl.P(u0, dbase + 0.66, z0 + 1.0 * H); cyl('cast', p[0], p[1], z0 + 0.985 * H, z0 + 1.05 * H, 0.30 * s, 0.33 * s, 12)
    elif kind == 'bishop':
        p = Wl.P(u0, dbase + 0.66, z0 + 0.99 * H); cyl('cast', p[0], p[1], z0 + 0.98 * H, z0 + 1.12 * H, 0.30 * s, 0.08 * s, 4)
    else:   # saint / queen: veil
        ell('cast', Wl.P(u0, dbase + 0.58, z0 + 0.90 * H), (0.36 * s, 0.34 * s, 0.42 * s), 12, 8)

# ---------------------------------------------------------------- 1. ground row: niches and canopies round the walls
def ground_row(Wl, u_a, u_b, pitch, name):
    n = int((u_b - u_a) // pitch); u_a = (u_a + u_b) / 2 - n * pitch / 2
    W_, ZS = pitch - 1.6, 6.9                     # opening, springing (apex ZS + W_*0.866)
    Wl.box('castd', u_a, u_a + n * pitch, 0.0, 1.35, Z0, 1.45)                     # bench / plinth
    Wl.box('cast', u_a - 0.1, u_a + n * pitch + 0.1, 0.0, 1.50, 1.45, 1.68)         # plinth moulding
    for i in range(n):
        u0 = u_a + (i + 0.5) * pitch
        niche_back(Wl, 'red' if i % 2 == 0 else 'blue', u0, W_, 1.68, ZS)
        # arch front (spandrels) between the shafts, 1.0..1.15 ft proud
        top = ZS + W_ * 0.866 + 1.0
        a = arch(u0, W_, ZS)
        Wl.prism('cast', 0.95, 1.12, [(u0 - pitch / 2, ZS), (u0 - W_ / 2, ZS)] + a[1:len(a) // 2 + 1] + [(u0, top), (u0 - pitch / 2, top)])
        Wl.prism('cast', 0.95, 1.12, [(u0, top)] + a[len(a) // 2:-1] + [(u0 + W_ / 2, ZS), (u0 + pitch / 2, ZS), (u0 + pitch / 2, top)])
        # roll moulding on the arch (thin ring 0.22 ft, gilt fillet)
        for m_ in range(len(a) - 1):
            (ua, za), (ub, zb) = a[m_], a[m_ + 1]
            Wl.prism('gilt', 1.12, 1.17, [(ua, za), (ub, zb), (ub + (0.18 if ub > u0 else -0.18) * 0, zb + 0.18), (ua, za + 0.18)])
        # crocketed gable canopy over the arch
        gable(Wl, 'cast', 'castd', u0, pitch / 2 - 0.35, top, 1.7, 0.90, 1.18)
        # small seated/standing figure? no - the niches show coloured grounds (I)
    for i in range(n + 1):                       # shafts between bays: stone pier + Purbeck colonnette + capital + pinnacle
        u = u_a + i * pitch
        Wl.box('cast', u - 0.42, u + 0.42, 0.0, 1.10, 1.68, ZS + W_ * 0.866 + 1.0)
        Wl.cyl('purbeck', u, 1.25, 1.68, ZS - 0.35, 0.16)
        Wl.box('gilt', u - 0.30, u + 0.30, 1.0, 1.50, ZS - 0.35, ZS)
        pinnacle(Wl, 'cast', u, 0.55, 1.15, ZS + W_ * 0.866 + 1.0, ZS + W_ * 0.866 + 1.9)
    Wl.box('cast', u_a - 0.1, u_a + n * pitch + 0.1, 0.0, 0.55, ZS + W_ * 0.866 + 1.0, ZS + W_ * 0.866 + 1.25)   # cornice line behind
    INFO[name] = dict(bays=n, pitch_ft=pitch, opening_ft=round(W_, 2), top_ft=round(max(ZS + W_ * 0.866 + 1.9 + 1.3, ZS + W_ * 0.866 + 1.0 + 1.7 + 0.55), 2), u=(round(u_a, 2), round(u_a + n * pitch, 2)))
    return n

def low_arcade(Wl, u_a, u_b, pitch, name):
    """under the stained glass: low blind arcade (sedilia-type) to 5.2 ft, clear of the lancet sills (5.5 / 6.0 ft)"""
    n = int((u_b - u_a) // pitch); u_a = (u_a + u_b) / 2 - n * pitch / 2
    W_, ZS = pitch - 0.7, 2.9
    Wl.box('castd', u_a, u_a + n * pitch, 0.0, 0.9, Z0, 1.15)
    for i in range(n):
        u0 = u_a + (i + 0.5) * pitch
        niche_back(Wl, 'blue' if i % 2 == 0 else 'red', u0, W_, 1.15, ZS)
        top = 5.0; a = arch(u0, W_, ZS)
        Wl.prism('cast', 0.55, 0.70, [(u0 - pitch / 2, ZS), (u0 - W_ / 2, ZS)] + a[1:len(a) // 2 + 1] + [(u0, top), (u0 - pitch / 2, top)])
        Wl.prism('cast', 0.55, 0.70, [(u0, top)] + a[len(a) // 2:-1] + [(u0 + W_ / 2, ZS), (u0 + pitch / 2, ZS), (u0 + pitch / 2, top)])
    for i in range(n + 1):
        u = u_a + i * pitch
        Wl.cyl('purbeck', u, 0.80, 1.15, ZS, 0.13); Wl.box('gilt', u - 0.22, u + 0.22, 0.55, 1.02, ZS - 0.22, ZS)
    Wl.box('cast', u_a - 0.1, u_a + n * pitch + 0.1, 0.0, 0.85, 5.0, 5.2)        # string course (below the 5.5 ft surround)
    INFO[name] = dict(bays=n, pitch_ft=pitch, top_ft=5.2, u=(round(u_a, 2), round(u_a + n * pitch, 2)))

def upper_tier(Wl, u_a, u_b, pitch, kinds, name):
    """upper tier: large statues beneath canopies (Wells facade casts, generic U) on a string course at 13.0 ft"""
    n = int((u_b - u_a) // pitch); u_a = (u_a + u_b) / 2 - n * pitch / 2
    Wl.box('cast', u_a - 0.3, u_a + n * pitch + 0.3, 0.0, 1.25, 12.75, 13.25)       # string course / statue shelf
    W_ = pitch - 1.5; ZS = 19.4
    for i in range(n):
        u0 = u_a + (i + 0.5) * pitch
        Wl.plate('blue', 0.04, [(u0 - W_ / 2, 13.25), (u0 + W_ / 2, 13.25), (u0 + W_ / 2, ZS + 0.55), (u0 - W_ / 2, ZS + 0.55)])   # painted ground behind the statue
        Wl.box('castd', u0 - 0.75, u0 + 0.75, 0.0, 1.30, 13.25, 13.75)              # statue base
        statue(Wl, u0, 0.05, 13.75, 6.3, kinds[i % len(kinds)], 1854400 + i * 7 + (0 if Wl.w == 'back' else 100))
        # canopy: projecting hood with cusped pointed front + gable, to z 21.9 (below the glazing line at ~22.3 ft)
        Wl.box('cast', u0 - W_ / 2 - 0.2, u0 + W_ / 2 + 0.2, 0.0, 1.45, ZS + 0.2, ZS + 0.55)
        a = arch(u0, W_ * 0.62, ZS - 0.4, 6)
        Wl.prism('cast', 1.30, 1.45, [(u0 - W_ / 2 - 0.2, ZS - 0.4), (u0 - W_ * 0.31, ZS - 0.4)] + a[1:len(a) // 2 + 1] + [(u0, ZS + 0.2), (u0 - W_ / 2 - 0.2, ZS + 0.2)])
        Wl.prism('cast', 1.30, 1.45, [(u0, ZS + 0.2)] + a[len(a) // 2:-1] + [(u0 + W_ * 0.31, ZS - 0.4), (u0 + W_ / 2 + 0.2, ZS - 0.4), (u0 + W_ / 2 + 0.2, ZS + 0.2)])
        gable(Wl, 'cast', 'castd', u0, W_ / 2, ZS + 0.55, 1.25, 1.10, 1.40, crockets=False)
    for i in range(n + 1):
        u = u_a + i * pitch
        Wl.box('cast', u - 0.32, u + 0.32, 0.0, 0.95, 13.25, ZS + 0.55)
        Wl.cyl('purbeck', u, 1.05, 13.25, ZS + 0.2, 0.12)
        pinnacle(Wl, 'cast', u, 0.35, 0.95, ZS + 0.55, ZS + 1.0)
    INFO[name] = dict(statues=n, pitch_ft=pitch, statue_h_ft=6.3, top_ft=round(ZS + 1.0 + 1.3, 2), u=(round(u_a, 2), round(u_a + n * pitch, 2)))

BW, WW = Wall('back'), Wall('west')
ground_row(BW, WEST + 1.6, HOOD_X0 - 0.6, 4.5, 'back_ground_row')               # back wall x 394.6 .. 421.9
ground_row(WW, MY0 + 2.6, WIN[0], 4.5, 'west_ground_row_south')                  # west wall y -113.4 .. -81.6
low_arcade(WW, WIN[0], WIN[1], 2.4, 'west_low_arcade_under_glass')
ground_row(WW, WIN[1], MY1 - 1.8, 4.5, 'west_ground_row_north')                  # y -62.4 .. -47.8
upper_tier(BW, WEST + 2.0, HOOD_X0 - 1.0, 6.5, ('king', 'bishop', 'queen', 'king'), 'back_upper_tier')
upper_tier(WW, MY0 + 3.0, WIN[0] - 0.4, 6.5, ('bishop', 'king', 'queen', 'king', 'bishop'), 'west_upper_tier')

# ---------------------------------------------------------------- 2. Rochester doorway coloured (overlay plates on the r14 faces)
ORD = ['red', 'blue', 'green', 'red', 'blue']          # order k = 0 (inner) .. 4 (outer); scheme I
for k in range(5):
    r0, r1 = 3.5 + k, 4.5 + k; yf = FYR + DEP * (k + 1)
    ky = 0.012 if k in (1, 3) else 0.02                # chevron orders: paint under the r14 chevron triangles (yfront + 0.02)
    for s_ in (-1, 1):
        xa, xb = sorted((RCX + s_ * r0, RCX + s_ * r1))
        poly(ORD[k], [(xa, yf + ky, Z0 + 0.6), (xb, yf + ky, Z0 + 0.6), (xb, yf + ky, 8.3), (xa, yf + ky, 8.3)])       # jamb face
        poly('gilt', [(xa, yf + ky + 0.004, 8.3), (xb, yf + ky + 0.004, 8.3), (xb, yf + ky + 0.004, 9.0), (xa, yf + ky + 0.004, 9.0)])   # capital band
        cx = RCX + s_ * (r0 + 0.45)
        cyl('red' if k % 2 else 'green', cx, yf + 0.3, 0.6, 8.3, 0.35, 0.35, seg=10)                                   # nook-shaft sleeve
        for zb in (0.9, 8.0): cyl('gilt', cx, yf + 0.3, zb, zb + 0.18, 0.40, 0.40, seg=10)                           # gilt bands
    n = 24
    for i in range(n):                                  # arch ring face
        ta, tb = math.pi * i / n, math.pi * (i + 1) / n
        P = [(RCX + r0 * math.cos(ta), 9.0 + r0 * math.sin(ta)), (RCX + r1 * math.cos(ta), 9.0 + r1 * math.sin(ta)),
             (RCX + r1 * math.cos(tb), 9.0 + r1 * math.sin(tb)), (RCX + r0 * math.cos(tb), 9.0 + r0 * math.sin(tb))]
        poly(ORD[k], [(u, yf + ky, z) for u, z in P][::-1])
    if k in (1, 3):                                     # gilt the chevrons: thin gilt copies just proud of the r14 triangles
        for i in range(18):
            ta, tb = math.pi * i / 18, math.pi * (i + 1) / 18; tm = (ta + tb) / 2
            rr_a, rr_b = (r0 + 0.1, r1 - 0.1) if i % 2 else (r1 - 0.1, r0 + 0.1)
            pa = (RCX + rr_a * math.cos(ta), 9.0 + rr_a * math.sin(ta)); pb = (RCX + rr_b * math.cos(tm), 9.0 + rr_b * math.sin(tm)); pc = (RCX + rr_a * math.cos(tb), 9.0 + rr_a * math.sin(tb))
            poly('gilt', [(pa[0], yf + 0.035, pa[1]), (pc[0], yf + 0.035, pc[1]), (pb[0], yf + 0.035, pb[1])])
poly('red', [(RCX - 9.5, FYR + DEP * 5 + 0.32, 14.2), (RCX + 9.5, FYR + DEP * 5 + 0.32, 14.2), (RCX + 9.5, FYR + DEP * 5 + 0.32, 15.0), (RCX - 9.5, FYR + DEP * 5 + 0.32, 15.0)])   # hood face
for i in range(19):                                    # gilt billet / pellets on the hood
    u = RCX - 9.0 + i * 1.0; box('gilt', u - 0.18, u + 0.18, FYR + DEP * 5 + 0.32, FYR + DEP * 5 + 0.42, 14.45, 14.75)
TY = [(RCX + 3.5 * math.cos(math.pi * i / 20), 9.0 + 3.5 * math.sin(math.pi * i / 20)) for i in range(21)]
poly('blue', [(u, FYR + 0.13, z) for u, z in TY][::-1])                               # tympanum ground (r14 plate at +0.10)
poly('red', [(RCX - 3.5, FYR + 0.42, 8.2), (RCX + 3.5, FYR + 0.42, 8.2), (RCX + 3.5, FYR + 0.42, 9.0), (RCX - 3.5, FYR + 0.42, 9.0)])   # lintel ground behind the apostles
box('gilt', RCX - 0.47, RCX + 0.47, FYR + 0.76, FYR + 0.79, 9.6, 11.6)               # seated Christ face gilt
for i in range(12):                                                                    # apostles: white-robed, gilt haloes
    u = RCX - 3.3 + i * 0.55
    box('wht', u, u + 0.4, FYR + 0.61, FYR + 0.63, 8.25, 8.80); box('gilt', u + 0.05, u + 0.35, FYR + 0.61, FYR + 0.64, 8.80, 8.95)
INFO['rochester_orders_painted'] = 5

# ---------------------------------------------------------------- 3. floor monuments: tomb chests with recumbent gilt effigies
#  Queen Eleanor of Castile (Westminster; Westminster Abbey: tomb L 3.02 x W 1.10 x H 1.65 m; V&A cast of the Torel effigy
#    213.5 x 77 cm; gilt bronze; two lions at her feet; left hand raised to the mantle cord; shields of England, Castile-Leon,
#    Ponthieu on the chest) - R dimensions.
#  Edward the Black Prince (Canterbury; will: 'twelve escutcheons ... each of the breadth of a foot, six of our arms entire, and
#    the other six of ostrich feathers'; gilt latten effigy in armour, head on the helm, feet on a leopard; Purbeck chest; the
#    tester above is NOT modelled) - escutcheons R, chest size I.
def effigy(cx, cy, zt, L, kind, wf=1.0):
    """recumbent effigy along +X (head to the west, -X): cushions / helm, head, hands, body with long folds, beasts at the feet.
    Gilt metal (both originals gilt copper alloy; R)."""
    k = 'gilt_e'; s = L / 6.2; q = s * wf
    box(k, cx - L / 2 - 0.05, cx - L / 2 + 1.05 * s, cy - 0.85 * q, cy + 0.85 * q, zt, zt + 0.30 * s)                  # pillow / helm base
    Rc = Matrix.Rotation(math.radians(-20), 3, 'Y')
    ell(k, (cx - L / 2 + 0.62 * s, cy, zt + 0.42 * s), (0.42 * s, 0.62 * q, 0.14 * s), 12, 6, Rc)                    # upper pillow / helm (tilted)
    ell(k, (cx - L / 2 + 0.95 * s, cy, zt + 0.55 * s), (0.36 * s, 0.30 * s, 0.30 * s), 14, 10)                      # head
    if kind == 'prince':
        ell(k, (cx - L / 2 + 0.95 * s, cy, zt + 0.62 * s), (0.40 * s, 0.33 * s, 0.30 * s), 14, 10)                  # bascinet
        ell(k, (cx - L / 2 + 1.40 * s, cy, zt + 0.40 * s), (0.30 * s, 0.50 * s, 0.22 * s), 12, 8)                   # aventail
    else:
        cyl(k, cx - L / 2 + 0.80 * s, cy, zt + 0.55 * s, zt + 0.80 * s, 0.30 * s, 0.33 * s, 12)                     # crown
        ell(k, (cx - L / 2 + 0.95 * s, cy, zt + 0.42 * s), (0.42 * s, 0.50 * s, 0.24 * s), 12, 8)                   # veil / hair
    bm = BM[k]; nseg, nr = 18, 16; rows = []
    for i in range(nr + 1):
        t = i / nr; x = cx - L / 2 + (1.30 + t * (L / s - 1.75)) * s
        w = (0.72 - 0.30 * t ** 1.4) * q; h = (0.46 - 0.16 * t) * s
        ring = []
        for j in range(nseg):
            th = 2 * math.pi * j / nseg
            fold = 1.0 + (0.06 * math.sin(7 * th) if kind != 'prince' else 0.03 * math.sin(4 * th))
            ring.append(bm.verts.new((f(x), f(cy + w * fold * math.cos(th)), f(zt + h + h * 0.9 * math.sin(th) * (1.0 if math.sin(th) > 0 else 0.25)))))
        rows.append(ring)
    for i in range(nr):
        for j in range(nseg):
            jj = (j + 1) % nseg; bm.faces.new((rows[i][j], rows[i][jj], rows[i + 1][jj], rows[i + 1][j]))
    bm.faces.new(rows[0][::-1]); bm.faces.new(rows[-1])
    hx = cx - L / 2 + 2.05 * s
    if kind == 'prince':
        ell(k, (hx, cy, zt + 0.80 * s), (0.12 * s, 0.10 * s, 0.24 * s), 8, 6)                                       # hands in prayer
        box(k, cx - L / 2 + 2.6 * s, cx - L / 2 + 2.78 * s, cy - 0.66 * s, cy + 0.66 * s, zt + 0.55 * s, zt + 0.82 * s)  # girdle
        ell(k, (cx + L / 2 - 0.55 * s, cy, zt + 0.36 * s), (0.42 * s, 0.36 * s, 0.26 * s), 12, 8)                    # leopard at the feet (massing)
    else:
        ell(k, (hx - 0.15 * s, cy + 0.12 * s, zt + 0.78 * s), (0.20 * s, 0.10 * s, 0.10 * s), 8, 6)                # left hand at the mantle cord
        ell(k, (cx + L / 2 - 0.45 * s, cy, zt + 0.25 * s), (0.30 * s, 0.50 * q, 0.22 * s), 12, 8)                    # gown hem over the feet
        for sy in (-1, 1):
            ell(k, (cx + L / 2 + 0.05 * s, cy + sy * 0.38 * q, zt + 0.22 * s), (0.32 * s, 0.22 * s, 0.20 * s), 10, 6)   # two small lions (massing)

def tomb(name, cx, cy, L, W, H, kind, n_side, n_end, arms, eff_L, wf=1.0):
    """Purbeck chest on a plinth step; escutcheons 1.0 ft broad in cusped quatrefoil panels on both long sides and both ends"""
    x0, x1, y0, y1 = cx - L / 2, cx + L / 2, cy - W / 2, cy + W / 2
    box('purbeck', x0 - 0.25, x1 + 0.25, y0 - 0.25, y1 + 0.25, Z0, Z0 + 0.5)                   # plinth step
    box('purbeck', x0, x1, y0, y1, Z0 + 0.5, H - 0.35)                                           # chest
    box('purbeck', x0 - 0.18, x1 + 0.18, y0 - 0.18, y1 + 0.18, H - 0.35, H)                      # top slab
    zc = Z0 + 0.5 + (H - 0.85 - Z0) / 2; r = 0.85; sw, sh = 0.50, 0.62                          # shield 1.0 ft broad
    faces = [('y', +1, y1, x0, x1, n_side), ('y', -1, y0, x0, x1, n_side), ('x', +1, x1, y0, y1, n_end), ('x', -1, x0, y0, y1, n_end)]
    ns = 0
    for ax, side, c, a0, a1, n in faces:
        for i in range(n):
            u0 = a0 + (i + 0.5) * (a1 - a0) / n
            def P(u, d, z): return (u, c + side * d, z) if ax == 'y' else (c + side * d, u, z)
            def put(kk, pts2, d):
                pts = [P(u, d, z) for u, z in pts2]
                flip = (ax == 'y') != (side > 0)
                poly(kk, pts[::-1] if flip else pts)
            q = []
            for m_ in range(32):
                th = 2 * math.pi * m_ / 32; rr = r * (0.78 + 0.22 * abs(math.cos(2 * th)))
                q.append((u0 + rr * math.cos(th), zc + rr * math.sin(th)))
            put('pbk2', q, 0.012)
            c1, c2 = arms[ns % len(arms)]
            put(c1, [(u0 - sw, zc + sh * 0.55), (u0 + sw, zc + sh * 0.55), (u0 + sw, zc - sh * 0.1), (u0, zc - sh), (u0 - sw, zc - sh * 0.1)], 0.022)
            put(c2, [(u0, zc + sh * 0.55), (u0 + sw, zc + sh * 0.55), (u0 + sw, zc - sh * 0.1), (u0, zc - sh)], 0.030)
            ns += 1
    effigy(cx, cy, H, eff_L, kind, wf)
    INFO[name] = dict(centre_ft=(cx, cy), chest_ft=(L, W, H), escutcheons=ns, escutcheon_w_ft=2 * sw, effigy_ft=round(eff_L, 2))

PEACE, WAR = ('blk', 'wht'), ('blue', 'red')        # ostrich feathers (white on black) / arms quartered (France blue, England red)
tomb('tomb_black_prince', 426.5, -93.0, 8.0, 3.5, 4.0, 'prince', 4, 2, [WAR, PEACE], 6.8)
# Eleanor: chest + slab 9.91 x 3.61 ft; overall height 5.41 ft = chest 4.30 ft + effigy; effigy 7.00 x 2.53 ft (body widened, wf)
tomb('tomb_queen_eleanor', 412.0, -68.0, 9.91 - 0.36, 3.61 - 0.36, 4.30, 'queen', 4, 2, [('red', 'gilt'), ('red', 'wht'), ('blue', 'gilt')], 7.00, wf=2.53 / (2 * 0.85 * 7.00 / 6.2))

# ---------------------------------------------------------------- emit objects
for k, bm in BM.items():
    if not bm.verts: bm.free(); continue
    me = bpy.data.meshes.new('cp040_' + k); bm.to_mesh(me); bm.free()
    if k == 'gilt_e':
        for p in me.polygons: p.use_smooth = True
    me.materials.append(M[k])
    o = bpy.data.objects.new('cp040_mediaeval_' + k, me); col.objects.link(o)
for o in col.objects: o['cp_state'] = STATE
INFO['objects'] = len(col.objects)
print('CP040 BUILT', INFO)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP040 SAVED', OUT)
