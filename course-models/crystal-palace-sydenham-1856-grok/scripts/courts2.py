# r13 Fine Arts Courts II (CP039 / CP040): Pompeian Court, Greek + Roman courts (nave fronts + sculpture interior),
# Mediaeval Court (English + German, Rochester doorway, stained glass). Exec'd from build.py for the pre-1866 states.
# Positions traced from the 1854 ground plan 0205 (R for placement, ±6 ft); forms after the 1854/1856 guides (Digby Wyatt,
# Owen Jones, Scharf) and the Delamotte / Rijksmuseum stereos 0040 (Greek & Roman sculpture court) and 0042 (French &
# Italian Mediaeval vestibule). Muse props appended unmodified (vendor/CREDIT.md). Grades in DEPARTURES r13 (D-R13-F*).
import bpy, math, os, random
from mathutils import Vector
_VD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vendor')
def _lc_find(lc, col):
    if lc.collection == col: return lc
    for c in lc.children:
        r = _lc_find(c, col)
        if r: return r
LIBC = coll('MUSE_props_lib__instanced_not_rendered')
_l = _lc_find(bpy.context.view_layer.layer_collection, LIBC)
if _l: _l.exclude = True
_MUSE = {}
def muse(name, want=None):
    """append a Muse prop once into its own (excluded) library collection; return that collection for instancing.
    want: collection name in the source file to take (others - ground, cameras, lights, backdrops - are left behind)."""
    if name in _MUSE: return _MUSE[name]
    path = os.path.join(_VD, 'muse-' + name, name + '.blend')
    if not os.path.exists(path): print('MUSE missing', path); _MUSE[name] = None; return None
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        if want: dst.collections = [want]
        else: dst.objects = list(src.objects)
    lc = bpy.data.collections.new('MUSE_' + name); LIBC.children.link(lc)
    objs = list(dst.collections[0].all_objects) if want else [o for o in dst.objects if o is not None]
    objs = [o for o in objs if o.type in ('MESH', 'CURVE', 'EMPTY')]
    keep = set(objs)
    for o in objs:
        if o.parent is not None and o.parent not in keep:
            mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
        lc.objects.link(o)
    if want:   # drop the appended source collection wrapper (objects now live in lc)
        for c in dst.collections:
            if c and c.users == 0: bpy.data.collections.remove(c)
    _MUSE[name] = lc; return lc
def place(name, col, x, y, z=0.0, rotz=0.0, want=None, scale=1.0):
    lc = muse(name, want)
    if lc is None: return None
    e = bpy.data.objects.new('muse_' + name + '_inst', None); e.instance_type = 'COLLECTION'; e.instance_collection = lc
    e.location = (f(x), f(y), f(z)); e.rotation_euler = (0, 0, rotz); e.scale = (scale,)*3; col.objects.link(e)
    e['credit'] = 'Muse / models/%s @ origin/main fab3531 (see vendor/CREDIT.md)' % name; return e

def MBx(name, col, m): return MB(name, col, m)
def bx(mb, x0, x1, y0, y1, z0, z1): mb.box(min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), min(z0, z1), max(z0, z1))
def fbox(mb, ax, c, side, a0, a1, z0, z1, d0, d1):
    """box on a wall face: ax 'x' -> face runs along x at y=c (normal side*Y); 'y' -> along y at x=c"""
    if ax == 'x': bx(mb, a0, a1, c + side*d0, c + side*d1, z0, z1)
    else: bx(mb, c + side*d0, c + side*d1, a0, a1, z0, z1)
def wall_run(mb, ax, c, t, a0, a1, z0, z1, gaps=()):
    """solid wall of thickness t centred on line c, from a0 to a1, with door gaps (g0, g1, head)"""
    a = a0
    for g0, g1, gh in sorted(gaps) + [(a1, a1, 0)]:
        if g0 > a: fbox(mb, ax, c, 1, a, g0, z0, z1, -t/2, t/2)
        if g1 > g0 and gh < z1: fbox(mb, ax, c, 1, g0, g1, gh, z1, -t/2, t/2)
        a = max(a, g1)
def ring_xz(mb, cx, cz, r0, r1, y0, y1, a0=0.0, a1=math.pi, n=20, ax='x'):
    """semicircular (or partial) ring in a vertical plane: ax 'x' -> plane XZ thickness along Y (y0..y1); 'y' -> plane YZ"""
    bm = mb.bm
    def V(u, z, d): return bm.verts.new((f(cx + u), f(d), f(z)) if ax == 'x' else (f(d), f(cx + u), f(z)))
    for i in range(n):
        ta, tb = a0 + (a1 - a0)*i/n, a0 + (a1 - a0)*(i + 1)/n
        P = [(r0*math.cos(ta), cz + r0*math.sin(ta)), (r1*math.cos(ta), cz + r1*math.sin(ta)),
             (r1*math.cos(tb), cz + r1*math.sin(tb)), (r0*math.cos(tb), cz + r0*math.sin(tb))]
        F = [V(u, z, y0) for u, z in P]; B = [V(u, z, y1) for u, z in P]
        bm.faces.new(F); bm.faces.new(list(reversed(B)))
        for k in range(4):
            k1 = (k + 1) % 4; bm.faces.new((F[k], B[k], B[k1], F[k1]))
def plate(mb, ax, c, pts):
    """flat polygon on a wall plane: pts (u, z); ax 'x' -> plane y=c, 'y' -> plane x=c"""
    mb.poly([(u, c, z) if ax == 'x' else (c, u, z) for u, z in pts])
def lancet(u0, w, z0, zs, n=10):
    """equilateral pointed-arch outline (u, z), sill z0, springing zs"""
    pts = [(u0 - w/2, z0), (u0 + w/2, z0), (u0 + w/2, zs)]
    for i in range(1, n + 1):
        t = math.radians(60)*i/n; pts.append((u0 - w/2 + w*math.cos(t), zs + w*math.sin(t)))
    for i in range(1, n):
        t = math.radians(120) + math.radians(60)*i/n; pts.append((u0 + w/2 + w*math.cos(t), zs + w*math.sin(t)))
    return pts

def stained_mat(name, scale=7.0, strength=4.0, hue=0):
    """leaded coloured glass, backlit: emission through a Voronoi cell mosaic with dark leading (I/U)"""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; L = nt.links
    n.clear(); out = n.new('ShaderNodeOutputMaterial')
    tc = n.new('ShaderNodeTexCoord')
    vo = n.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = scale; L.new(tc.outputs['Object'], vo.inputs['Vector'])
    ve = n.new('ShaderNodeTexVoronoi'); ve.feature = 'DISTANCE_TO_EDGE'; ve.inputs['Scale'].default_value = scale; L.new(tc.outputs['Object'], ve.inputs['Vector'])
    bw = n.new('ShaderNodeRGBToBW'); L.new(vo.outputs['Color'], bw.inputs[0])
    cr = n.new('ShaderNodeValToRGB'); cr.color_ramp.interpolation = 'CONSTANT'; L.new(bw.outputs[0], cr.inputs[0])
    pal = [(0.55, 0.02, 0.03), (0.04, 0.10, 0.55), (0.80, 0.55, 0.06), (0.05, 0.35, 0.08), (0.85, 0.82, 0.70), (0.10, 0.18, 0.75), (0.60, 0.05, 0.10)]
    pal = pal[hue:] + pal[:hue]
    els = cr.color_ramp.elements; els[0].position = 0.0; els[0].color = (*pal[0], 1); els[1].position = 1.0 / len(pal); els[1].color = (*pal[1], 1)
    for i in range(2, len(pal)):
        e = els.new(i / len(pal)); e.color = (*pal[i], 1)
    em = n.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = strength; L.new(cr.outputs['Color'], em.inputs['Color'])
    lt = n.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.05; L.new(ve.outputs['Distance'], lt.inputs[0])
    dk = n.new('ShaderNodeBsdfDiffuse'); dk.inputs['Color'].default_value = (0.02, 0.02, 0.02, 1)
    mx = n.new('ShaderNodeMixShader'); L.new(lt.outputs[0], mx.inputs[0]); L.new(em.outputs[0], mx.inputs[1]); L.new(dk.outputs[0], mx.inputs[2])
    L.new(mx.outputs[0], out.inputs[0]); return m
def checker_mat(name, c1, c2, sc=1.2):
    m = mat(name, c1, 0.45); nt = m.node_tree; n = nt.nodes; L = nt.links
    tc = n.new('ShaderNodeTexCoord'); ck = n.new('ShaderNodeTexChecker'); ck.inputs['Scale'].default_value = sc
    ck.inputs['Color1'].default_value = (*c1, 1); ck.inputs['Color2'].default_value = (*c2, 1)
    L.new(tc.outputs['Object'], ck.inputs['Vector']); L.new(ck.outputs['Color'], n['Principled BSDF'].inputs['Base Color']); return m

PRNG2 = random.Random(1854)
def near_col(x, y, d=1.6):
    return any(abs(x - xc) < d for xc in xs_grid) and any(abs(y - yc) < d for yc in COL_Y)
CTS = coll('SY54_fine_arts_courts_II_r13__dated')
# ---------------------------------------------------------------------------------------------------------------------
# 1. POMPEIAN COURT (Digby Wyatt, painted by Abbate; 1854) - plan 0205 x -564..-492, y 60..156, Parade half of the south
#    transept bay. A house after the 'House of Sallust/Pansa' type: fauces, atrium with compluvium + impluvium, side
#    cubicula, tablinum, peristyle garden. Wall decoration in the 'Fourth Style' zones: black dado, red (and yellow) main
#    zone with framed panels and black architectural strips, yellow frieze, white upper zone (Guide 1854 'Pompeian Court').
#    House plan R-type / dimensions I; painting schemes I/U (no colour photograph).
# ---------------------------------------------------------------------------------------------------------------------
PC = coll('SY54_court_pompeian__dated', parent=CTS)
PR = {k: mat('pomp_' + k, c, r) for k, c, r in (('red', (0.47, 0.055, 0.035), 0.6), ('yel', (0.78, 0.52, 0.12), 0.6),
      ('blk', (0.025, 0.022, 0.02), 0.5), ('wht', (0.84, 0.80, 0.70), 0.6), ('grn', (0.10, 0.24, 0.10), 0.7),
      ('sky', (0.30, 0.48, 0.62), 0.7), ('ochre', (0.55, 0.33, 0.10), 0.6), ('tile', (0.50, 0.19, 0.09), 0.75),
      ('stucco', (0.86, 0.83, 0.76), 0.55), ('floor', (0.33, 0.13, 0.08), 0.6), ('marble', (0.88, 0.87, 0.84), 0.3),
      ('water', (0.05, 0.10, 0.12), 0.05))}
PB = {k: MB('pompeian_' + k, PC, m) for k, m in PR.items()}
PX0, PX1, PY0, PY1, PH = -562.0, -494.0, 62.0, 154.0, 20.0
XC = (PX0 + PX1) / 2                      # -528
AX0, AX1, AY0, AY1 = -546.0, -510.0, 70.0, 106.0      # atrium
TY0, TY1 = 106.0, 118.0                    # tablinum zone
W = PB['stucco']
wall_run(W, 'x', PY0, 1.2, PX0, PX1, 0, PH, gaps=[(XC - 3, XC + 3, 11), (-556, -548, 10), (-508, -500, 10)])   # street front: fauces + 2 shops
wall_run(W, 'x', PY1, 1.2, PX0, PX1, 0, PH)
wall_run(W, 'y', PX0, 1.2, PY0, PY1, 0, PH); wall_run(W, 'y', PX1, 1.2, PY0, PY1, 0, PH)
wall_run(W, 'x', AY0, 1.0, PX0, PX1, 0, PH, gaps=[(XC - 4, XC + 4, 12)])
wall_run(W, 'y', AX0, 1.0, AY0, TY1, 0, PH, gaps=[(73, 78, 9), (84, 89, 9), (95, 100, 9), (108, 116, 13)])
wall_run(W, 'y', AX1, 1.0, AY0, TY1, 0, PH, gaps=[(73, 78, 9), (84, 89, 9), (95, 100, 9), (108, 116, 13)])
for yy in (81.0, 92.0, 103.0): wall_run(W, 'x', yy, 0.8, PX0, AX0, 0, PH); wall_run(W, 'x', yy, 0.8, AX1, PX1, 0, PH)
wall_run(W, 'x', TY0, 1.0, AX0, AX1, 0, PH, gaps=[(XC - 8, XC + 8, 15.5)])       # tablinum: wide openings both ends
wall_run(W, 'x', TY1, 1.0, PX0, PX1, 0, PH, gaps=[(XC - 8, XC + 8, 15.5)])
wall_run(W, 'y', XC - 8.5, 0.8, TY0, TY1, 0, PH); wall_run(W, 'y', XC + 8.5, 0.8, TY0, TY1, 0, PH)
bx(PB['floor'], PX0, PX1, PY0, PY1, 0, 0.08)                                   # opus signinum floor
# impluvium + compluvium
IX0, IX1, IY0, IY1 = XC - 8, XC + 8, 82.0, 94.0
bx(PB['marble'], IX0 - 1, IX1 + 1, IY0 - 1, IY1 + 1, 0.08, 0.7)
bx(PB['water'], IX0, IX1, IY0, IY1, 0.71, 0.75)
bx(PB['marble'], XC - 2.5, XC + 2.5, IY1 + 3, IY1 + 5.5, 0, 2.9)               # cartibulum table
for (x0, x1, y0, y1, ix0, ix1, iy0, iy1) in ((AX0, AX1, AY0, AY0, IX0, IX1, IY0, IY0), (AX0, AX1, AY1, AY1, IX0, IX1, IY1, IY1)):
    PB['tile'].poly([(x0, y0, PH), (x1, y0, PH), (ix1, iy0, PH - 3), (ix0, iy0, PH - 3)])
PB['tile'].poly([(AX0, AY0, PH), (IX0, IY0, PH - 3), (IX0, IY1, PH - 3), (AX0, AY1, PH)])
PB['tile'].poly([(AX1, AY0, PH), (AX1, AY1, PH), (IX1, IY1, PH - 3), (IX1, IY0, PH - 3)])
for (x0, x1, y0, y1) in ((PX0, AX0, PY0, TY1), (AX1, PX1, PY0, TY1), (AX0, AX1, PY0, AY0), (AX0, AX1, TY0, TY1)):
    bx(PB['tile'], x0 - 0.6, x1 + 0.6, y0 - 0.6, y1 + 0.6, PH, PH + 0.6)       # room roofs (low pitch read as flat, I)
# peristyle: colonnade 6 x 4, portico roof sloping in
PCX0, PCX1, PCY0, PCY1 = -552.0, -504.0, 126.0, 146.0
cols_ = [(PCX0 + i*(PCX1 - PCX0)/5, y) for i in range(6) for y in (PCY0, PCY1)] + [(x, PCY0 + (PCY1 - PCY0)*j/2) for x in (PCX0, PCX1) for j in (1,)]
for (x, y) in cols_:
    PB['red'].cyl(x, y, 0, 4.5, 0.62, 0.62, seg=16)                              # red lower third, plain
    PB['stucco'].cyl(x, y, 4.5, 13.2, 0.62, 0.52, seg=20)                       # fluted stucco above (facets)
    PB['stucco'].cyl(x, y, 13.2, 13.8, 0.55, 0.85, seg=16); bx(PB['stucco'], x - 0.95, x + 0.95, y - 0.95, y + 0.95, 13.8, 14.3)
for (x0, x1, y0, y1) in ((PCX0, PCX1, PCY0, PCY0), (PCX0, PCX1, PCY1, PCY1)):
    bx(PB['stucco'], x0 - 1, x1 + 1, y0 - 0.7, y0 + 0.7, 14.3, 15.6)
for x in (PCX0, PCX1): bx(PB['stucco'], x - 0.7, x + 0.7, PCY0 - 1, PCY1 + 1, 14.3, 15.6)
PB['tile'].poly([(PX0 + 0.6, TY1 + 0.5, 18.5), (PX1 - 0.6, TY1 + 0.5, 18.5), (PCX1 + 1, PCY0 - 1, 15.6), (PCX0 - 1, PCY0 - 1, 15.6)])
PB['tile'].poly([(PX0 + 0.6, PY1 - 0.6, 18.5), (PCX0 - 1, PCY1 + 1, 15.6), (PCX1 + 1, PCY1 + 1, 15.6), (PX1 - 0.6, PY1 - 0.6, 18.5)])
PB['tile'].poly([(PX0 + 0.6, TY1 + 0.5, 18.5), (PCX0 - 1, PCY0 - 1, 15.6), (PCX0 - 1, PCY1 + 1, 15.6), (PX0 + 0.6, PY1 - 0.6, 18.5)])
PB['tile'].poly([(PX1 - 0.6, TY1 + 0.5, 18.5), (PX1 - 0.6, PY1 - 0.6, 18.5), (PCX1 + 1, PCY1 + 1, 15.6), (PCX1 + 1, PCY0 - 1, 15.6)])
bx(PB['grn'], PCX0 + 1.5, PCX1 - 1.5, PCY0 + 1.5, PCY1 - 1.5, 0.08, 0.9)      # garden bed
bx(PB['marble'], XC - 3, XC + 3, (PCY0 + PCY1)/2 - 3, (PCY0 + PCY1)/2 + 3, 0.9, 1.8); bx(PB['water'], XC - 2.4, XC + 2.4, (PCY0 + PCY1)/2 - 2.4, (PCY0 + PCY1)/2 + 2.4, 1.8, 1.84)
for k in range(10):                                                            # box shrubs (I)
    PB['grn'].cyl(PCX0 + 4 + k*4.4, PCY0 + 3.2 if k % 2 else PCY1 - 3.2, 0.9, 2.6, 0.9, 0.6, seg=8)

def paint(ax, c, side, a0, a1, gaps=(), main='red', garden=False):
    """Fourth-Style painted wall face on the room side (side = +-1 normal) of a wall face at c"""
    d0, d1, d2 = 0.0, 0.04, 0.08
    spans = []; a = a0
    for g0, g1, gh in sorted(gaps) + [(a1, a1, 0)]:
        if g0 > a: spans.append((a, g0))
        a = max(a, g1)
    for s0, s1 in spans:
        fbox(PB['blk'], ax, c, side, s0, s1, 0.08, 3.2, d0, d1)                                   # dado
        if garden:
            fbox(PB['sky'], ax, c, side, s0, s1, 3.2, 16, d0, d1)
            for k in range(int((s1 - s0)/1.6)):
                u = s0 + 0.8 + 1.6*k + PRNG2.uniform(-0.4, 0.4); hh = PRNG2.uniform(7, 13)
                fbox(PB['grn'], ax, c, side, u - PRNG2.uniform(0.6, 1.4), u + PRNG2.uniform(0.6, 1.4), 3.2, hh, d1, d2)
            fbox(PB['marble'], ax, c, side, s0, s1, 3.2, 4.4, d1, d2 + 0.02)                      # painted fence
        else:
            fbox(PB[main], ax, c, side, s0, s1, 3.2, 13.0, d0, d1)
            n = max(1, int(round((s1 - s0)/8.5))); u = (s1 - s0)/n
            for i in range(n + 1):
                uc = s0 + i*u; sw = min(1.0, u*0.1)
                fbox(PB['blk'], ax, c, side, max(s0, uc - sw), min(s1, uc + sw), 3.2, 13.0, d1, d2)   # black strips
                if s0 < uc < s1: fbox(PB['wht'], ax, c, side, uc - 0.05, uc + 0.05, 4.0, 12.3, d2, d2 + 0.02)   # candelabrum line
            for i in range(n):
                q0, q1 = s0 + i*u + 1.4, s0 + (i + 1)*u - 1.4
                if q1 - q0 < 1.5: continue
                for (zz0, zz1) in ((4.0, 4.15), (12.05, 12.2)): fbox(PB['yel'], ax, c, side, q0, q1, zz0, zz1, d1, d2)
                for uu in (q0, q1 - 0.15): fbox(PB['yel'], ax, c, side, uu, uu + 0.15, 4.0, 12.2, d1, d2)
                um = (q0 + q1)/2; fbox(PB['wht' if main == 'red' else 'red'], ax, c, side, um - 0.6, um + 0.6, 7.2, 9.0, d1, d2)   # vignette
        fbox(PB['yel'], ax, c, side, s0, s1, 13.0, 15.6, d0, d1)                                 # frieze
        fbox(PB['blk'], ax, c, side, s0, s1, 13.0, 13.2, d1, d2); fbox(PB['blk'], ax, c, side, s0, s1, 15.4, 15.6, d1, d2)
        for k in range(int((s1 - s0)/2.2)):                                                       # frieze vignettes
            u = s0 + 1.1 + 2.2*k; fbox(PB['red' if k % 2 else 'grn'], ax, c, side, u - 0.4, u + 0.4, 13.8, 14.8, d1, d2)
        fbox(PB['wht'], ax, c, side, s0, s1, 15.6, PH - 0.6, d0, d1)                             # upper zone
        for k in range(int((s1 - s0)/4.5)):
            u = s0 + 2.2 + 4.5*k; fbox(PB['ochre'], ax, c, side, u - 0.07, u + 0.07, 15.9, 19.0, d1, d2)   # painted aediculae lines
        fbox(PB['stucco'], ax, c, side, s0, s1, PH - 0.6, PH, d0, 0.45)                          # cornice
    for g0, g1, gh in gaps:                                                                       # over-door zones
        if gh < 13: fbox(PB[main if not garden else 'sky'], ax, c, side, g0, g1, gh, 13.0, d0, d1)
        fbox(PB['yel'], ax, c, side, g0, g1, max(gh, 13.0), 15.6, d0, d1); fbox(PB['wht'], ax, c, side, g0, g1, 15.6, PH - 0.6, d0, d1)
        fbox(PB['stucco'], ax, c, side, g0, g1, PH - 0.6, PH, d0, 0.45)
        fbox(PB['blk'], ax, c, side, g0 - 0.3, g1 + 0.3, gh, gh + 0.4, d0, d2)                   # lintel band
dg = [(73, 78, 9), (84, 89, 9), (95, 100, 9), (108, 116, 13)]
paint('y', AX0 + 0.5, 1, AY0 + 0.5, TY1 - 0.5, dg, 'red'); paint('y', AX1 - 0.5, -1, AY0 + 0.5, TY1 - 0.5, dg, 'red')
paint('x', AY0 + 0.5, 1, AX0 + 0.5, AX1 - 0.5, [(XC - 4, XC + 4, 12)], 'red')
paint('x', TY0 - 0.5, -1, AX0 + 0.5, AX1 - 0.5, [(XC - 8, XC + 8, 15.5)], 'red')
paint('y', XC - 8.1, 1, TY0 + 0.5, TY1 - 0.5, (), 'yel'); paint('y', XC + 8.1, -1, TY0 + 0.5, TY1 - 0.5, (), 'yel')
paint('x', PY1 - 0.6, -1, PX0 + 0.6, PX1 - 0.6, (), garden=True)                                 # peristyle garden painting
paint('y', PX0 + 0.6, 1, TY1 + 0.5, PY1 - 0.6, (), 'yel'); paint('y', PX1 - 0.6, -1, TY1 + 0.5, PY1 - 0.6, (), 'yel')
paint('x', TY1 + 0.5, 1, PX0 + 0.6, PX1 - 0.6, [(XC - 8, XC + 8, 15.5)], 'red')
paint('x', PY0 - 0.6, -1, PX0, PX1, [(XC - 3, XC + 3, 11), (-556, -548, 10), (-508, -500, 10)], 'red')   # street face (towards the nave)
for k, m in PB.items(): m.done()
pp = []
for i in range(14):
    x = PRNG2.uniform(AX0 + 2, AX1 - 2); y = PRNG2.uniform(AY0 + 2, TY1 - 2)
    if IX0 - 1.5 < x < IX1 + 1.5 and IY0 - 1.5 < y < IY1 + 7: continue
    pp.append((x, y, 0.08, public(PRNG2), PRNG2.uniform(-math.pi, math.pi)))
for i in range(10):
    x = PRNG2.uniform(PX0 + 3, PX1 - 3); y = PRNG2.uniform(TY1 + 2, PCY0 - 2) if i % 2 else PRNG2.uniform(PCY1 + 2, PY1 - 3)
    pp.append((x, y, 0.08, public(PRNG2), PRNG2.uniform(-math.pi, math.pi)))
for i in range(16):
    x = PRNG2.uniform(PX0, PX1); y = PRNG2.uniform(30, 58)
    pp.append((x, y, 0.0, public(PRNG2), PRNG2.uniform(-math.pi, math.pi)))
cam('CAM_CP039_pompeian_atrium_28mm', (XC + 2, AY0 + 1.5, EYE), (XC - 1, 150, 8.0), 28)
cam('CAM_CP039_pompeian_wall_50mm', (XC + 9, 90, EYE), (AX0, 86.5, 8.5), 50)
cam('CAM_CP039_pompeian_peristyle_28mm', (PX1 - 3, TY1 + 3, EYE), (PX0 + 6, PCY1 + 2, 6), 28)
people('ppl57_pompeian_visitors', PC, pp)

# ---------------------------------------------------------------------------------------------------------------------
# 2. GREEK COURT (Owen Jones) x 277-374 and ROMAN COURT (Digby Wyatt) x 374-490, y 60..156, Parade side.
#    Nave fronts: Greek Doric order with painted triglyph frieze / meander (Owen Jones's polychromy - I/U colours);
#    Roman Corinthian order. Interiors: boarded floor, casts on dark plinths under the open palace frame, Greek frieze
#    band round the walls (stereo 0040, R for that arrangement; which court it shows is I). Muse casts placed here.
# ---------------------------------------------------------------------------------------------------------------------
GC = coll('SY54_court_greek_roman__dated', parent=CTS)
GR = {k: mat('gr_' + k, c, r) for k, c, r in (('stone', (0.80, 0.76, 0.66), 0.55), ('red', (0.42, 0.07, 0.05), 0.65),
      ('blue', (0.06, 0.12, 0.32), 0.6), ('gold', (0.72, 0.52, 0.16), 0.45), ('plinth', (0.06, 0.055, 0.05), 0.5),
      ('frieze', (0.86, 0.84, 0.78), 0.7), ('yel', (0.66, 0.50, 0.24), 0.6), ('giallo', (0.80, 0.68, 0.42), 0.35))}
GB = {k: MB('greekroman_' + k, GC, m) for k, m in GR.items()}
GX0, GX1, RX1, FY = 278.0, 374.0, 489.0, 60.0   # fronts on the y=60 column line: orders encase the iron columns (I)
# walls
for (xa, xb) in ((GX0, GX1), (GX1, RX1)):
    wall_run(GB['red'] if xa == GX0 else GB['yel'], 'x', 154.0, 1.2, xa, xb, 0, 21.5)
wall_run(GB['red'], 'y', GX0, 1.0, FY, 154, 0, 21.5); wall_run(GB['yel'], 'y', RX1, 1.0, FY, 154, 0, 21.5)
wall_run(GB['stone'], 'y', GX1, 1.2, 100, 154, 0, 21.5)                         # party wall, open at the front half (I)
for (xa, xb, main) in ((GX0 + 0.5, GX1 - 0.6, 'red'), (GX1 + 0.6, RX1 - 0.5, 'yel')):
    fbox(GB['frieze'], 'x', 153.4, -1, xa, xb, 13.0, 15.6, 0, 0.12)           # cast frieze band (Parthenon / Phigaleia, R type)
    for k in range(int((xb - xa)/1.3)):
        u = xa + 0.4 + 1.3*k + PRNG2.uniform(-0.2, 0.2)
        fbox(GB['frieze'], 'x', 153.4, -1, u, u + 0.55, 13.3, 15.3 - PRNG2.uniform(0, 0.4), 0.12, 0.32)   # relief figures (massing)
    fbox(GB['gold'], 'x', 153.4, -1, xa, xb, 15.6, 16.0, 0, 0.2); fbox(GB['plinth'], 'x', 153.4, -1, xa, xb, 0, 2.5, 0, 0.08)
for (xc_, s_) in ((GX0 + 0.5, 1), (RX1 - 0.5, -1)):
    fbox(GB['frieze'], 'y', xc_, s_, FY + 3, 153, 13.0, 15.6, 0, 0.12); fbox(GB['gold'], 'y', xc_, s_, FY + 3, 153, 15.6, 16.0, 0, 0.2)
# Greek Doric front: 3 steps, 10 columns, painted entablature
bx(GB['stone'], GX0, GX1, FY - 3.0, FY + 3.0, 0, 0.6); bx(GB['stone'], GX0, GX1, FY - 2.2, FY + 3.0, 0.6, 1.2); bx(GB['stone'], GX0, GX1, FY - 1.4, FY + 3.0, 1.2, 1.8)
xs_ = [288.0 + 12*i for i in range(7)]                                            # 12 ft intercolumns on the 24 ft palace grid (I)
for (a0, a1) in ((GX0, 282.0), (366.0, GX1)): bx(GB['stone'], a0, a1, FY - 1.3, FY + 1.3, 1.8, 16.0)   # antae
for x in xs_:
    GB['stone'].cyl(x, FY, 1.8, 14.6, 1.25, 0.98, seg=20)
    GB['stone'].cyl(x, FY, 14.6, 15.4, 1.0, 1.45, seg=20); bx(GB['stone'], x - 1.55, x + 1.55, FY - 1.55, FY + 1.55, 15.4, 16.0)
bx(GB['stone'], GX0, GX1, FY - 1.3, FY + 1.3, 16.0, 18.0)                          # architrave
bx(GB['red'], GX0, GX1, FY - 1.25, FY + 1.3, 18.0, 20.0)                            # metope ground (red)
for x in xs_ + [(a + b)/2 for a, b in zip(xs_, xs_[1:])]:
    bx(GB['blue'], x - 0.75, x + 0.75, FY - 1.4, FY - 1.25, 18.0, 20.0)                 # triglyphs (blue)
    bx(GB['gold'], x - 0.5, x + 0.5, FY - 1.32, FY - 1.25, 16.6, 16.8)                  # guttae band
bx(GB['blue'], GX0, GX1, FY - 1.32, FY - 1.25, 17.8, 18.0)                          # taenia
bx(GB['stone'], GX0 - 0.5, GX1 + 0.5, FY - 2.2, FY + 1.5, 20.0, 21.2)             # geison
bx(GB['gold'], GX0 - 0.5, GX1 + 0.5, FY - 2.25, FY - 2.2, 20.15, 21.05)
for k in range(int((GX1 - GX0)/0.9)):                                              # meander suggested by alternating blocks
    u = GX0 + 0.45*(2*k) ; bx(GB['blue'], u, u + 0.45, FY - 2.29, FY - 2.25, 20.3 if k % 2 else 20.55, 20.9 if k % 2 else 20.65)
for x in xs_: bx(GB['gold'], x - 0.45, x + 0.45, FY - 2.3, FY - 1.9, 21.2, 22.0)   # antefixes
# Roman Corinthian front
bx(GB['giallo'], GX1, RX1, FY - 2.0, FY + 3.0, 0, 1.2)
xr_ = [384.0 + 12*i for i in range(9)]
for (a0, a1) in ((GX1, 379.0), (485.0, RX1)): bx(GB['giallo'], a0, a1, FY - 1.3, FY + 1.3, 1.2, 17.9)   # antae
for x in xr_:
    GB['giallo'].cyl(x, FY, 1.2, 2.2, 1.35, 1.2, seg=16); GB['giallo'].cyl(x, FY, 2.2, 15.4, 1.0, 0.88, seg=18)
    GB['stone'].cyl(x, FY, 15.4, 17.4, 0.9, 1.3, seg=16)                                # bell
    for k in range(8):                                                                  # acanthus leaves (massing)
        a = 2*math.pi*k/8; GB['stone'].strut((x + 0.95*math.cos(a), FY + 0.95*math.sin(a), 15.4), (x + 1.35*math.cos(a), FY + 1.35*math.sin(a), 16.8), 0.35)
    bx(GB['stone'], x - 1.5, x + 1.5, FY - 1.5, FY + 1.5, 17.4, 17.9)
bx(GB['stone'], GX1, RX1, FY - 1.3, FY + 1.3, 17.9, 19.3); bx(GB['red'], GX1, RX1, FY - 1.25, FY + 1.3, 19.3, 20.6)
bx(GB['gold'], GX1, RX1, FY - 1.32, FY - 1.25, 19.6, 20.3)
bx(GB['stone'], GX1 - 0.3, RX1 + 0.5, FY - 2.0, FY + 1.5, 20.6, 21.6)
for k in range(int((RX1 - GX1)/0.8)): bx(GB['stone'], GX1 + 0.8*k, GX1 + 0.8*k + 0.4, FY - 2.25, FY - 2.0, 20.6, 21.0)   # dentils
# interior plinths (dark, tall - 0040)
PL = [(312, 96, 3.6), (360, 96, 3.6), (312, 144, 3.6), (360, 144, 3.6), (408, 144, 3.2), (456, 144, 3.2), (408, 96, 3.2), (456, 96, 3.2)]   # between the palace columns
for (x, y, h) in PL: bx(GB['plinth'], x - 1.6, x + 1.6, y - 1.6, y + 1.6, 0, h); bx(GB['plinth'], x - 1.9, x + 1.9, y - 1.9, y + 1.9, h - 0.3, h)
for k, m in GB.items(): m.done()
# Muse casts (unmodified, appended):
place('the-three-graces', GC, 336, 120, 0, 0)                                       # Canova's Graces (stylised)
place('farnese-bull', GC, 432, 120, 0, 0)                                          # Farnese Bull: centre of the Roman court
for (x, y, h) in PL[:4]:
    place('display-plinth', GC, x, y, h); place('krater-vase', GC, x, y, h + 0.9/0.3048, want='MODEL')
for (x, y, h) in PL[4:]:
    place('sy-classical-cast-base', GC, x, y, h, want='Model')
gp = []
for i in range(30):
    x = PRNG2.uniform(GX0 + 4, RX1 - 4); y = PRNG2.uniform(FY + 6, 150)
    if near_col(x, y) or any(abs(x - px) < 3.5 and abs(y - py) < 3.5 for px, py, _ in PL) or (abs(x - 336) < 5 and abs(y - 120) < 5) or (abs(x - 432) < 8 and abs(y - 120) < 7): continue
    gp.append((x, y, 0, public(PRNG2), PRNG2.uniform(-math.pi, math.pi)))
for i in range(24):
    x = PRNG2.uniform(GX0, RX1); y = PRNG2.uniform(28, FY - 5)
    gp.append((x, y, 0, public(PRNG2), PRNG2.uniform(-math.pi, math.pi)))
cam('CAM_CP040_greek_roman_fronts_28mm', (300, 12, EYE), (400, 80, 13), 28)
cam('CAM_CP040_greek_interior_28mm', (284, 70, EYE), (360, 140, 7), 28)
cam('CAM_CP040_doric_detail_50mm', (316, 40, EYE), (326, FY, 17.5), 50)
cam('CAM_CP040_three_graces_50mm', (336, 94, EYE), (336, 120, 4.8), 50)                     # r14
cam('CAM_CP040_farnese_bull_50mm', (424, 86, EYE), (432, 120, 6.5), 50)                      # r14
people('ppl57_greekroman_visitors', GC, gp)
# r14: fill light under the gallery floor (the real courts took light from the nave and the glazed roof above the
# galleries; our gallery deck blocks it). Presentation lighting, I.
for _lx in ((GX0 + GX1)/2, (GX1 + RX1)/2):
    _ld = bpy.data.lights.new('court_fill_greekroman', 'AREA'); _ld.shape = 'RECTANGLE'; _ld.size = f(90); _ld.size_y = f(86); _ld.energy = 9000
    _ld.color = (1.0, 0.96, 0.9); _lo = bpy.data.objects.new('court_fill_greekroman', _ld); GC.objects.link(_lo); _lo.location = (f(_lx), f(107), f(21.0))

# ---------------------------------------------------------------------------------------------------------------------
# 3. MEDIAEVAL COURT (Digby Wyatt) - plan 0205 x 392-490, y -116..-44, garden side. English section (west) with the
#    Guisborough cloister arcade (Muse bay, tiled) on the nave front and as the screen to the German section; Rochester
#    Cathedral west doorway (Norman, 5 orders, tympanum with Christ in Majesty) in the back wall; stained-glass lancets
#    (the court displayed modern glass by Hardman and others - 'nineteenth-century mediaeval', R type, designs U).
# ---------------------------------------------------------------------------------------------------------------------
MC = coll('SY54_court_mediaeval__dated', parent=CTS)
MR = {k: mat('med_' + k, c, r) for k, c, r in (('stone', (0.74, 0.70, 0.60), 0.7), ('dark', (0.20, 0.18, 0.16), 0.35),
      ('blue', (0.08, 0.13, 0.36), 0.7), ('gold', (0.70, 0.50, 0.15), 0.45), ('red', (0.40, 0.06, 0.05), 0.7),
      ('oak', (0.18, 0.10, 0.05), 0.6))}
MBm = {k: MB('mediaeval_' + k, MC, m) for k, m in MR.items()}
TILE = checker_mat('med_encaustic_tiles', (0.36, 0.09, 0.05), (0.62, 0.50, 0.30), 2.4)
fl = MB('mediaeval_tile_floor', MC, TILE); fl.box(393, 489, -115.5, -46, 0, 0.05); fl.done()
MX0, MX1, MY0, MY1, MH = 392.0, 490.0, -116.0, -46.0, 30.0
S = MBm['stone']
wall_run(S, 'y', MX0, 2.0, MY0, MY1, 0, MH); wall_run(S, 'y', MX1, 2.0, MY0, MY1, 0, MH)
RCX = 432.0                                                                          # Rochester doorway centre (I, plan 0205 ±6)
wall_run(S, 'x', MY0, 2.0, MX0, MX1, 0, MH, gaps=[(RCX - 3.5, RCX + 3.5, 9.0)])
# nave front: wall above the arcade (Muse bays 14.2 ft high) with quatrefoil frieze and pinnacles
BAYW = 2.40/0.3048; NB = 11; FX0 = (MX0 + MX1)/2 - NB*BAYW/2
bx(S, MX0 - 1, MX1 + 1, MY1 - 1.2, MY1 + 0.6, 14.17, MH - 3)
for k in range(NB):
    u = FX0 + (k + 0.5)*BAYW
    bx(MBm['blue'], u - 2.6, u + 2.6, MY1 + 0.6, MY1 + 0.7, 16.5, 23.5)               # painted panel (blue + gold, Owen Jones)
    ring_xz(MBm['gold'], u, 20.0, 1.5, 1.9, MY1 + 0.7, MY1 + 0.85, 0, 2*math.pi, 16)    # quatrefoil roundel (massing)
    bx(MBm['stone'], u - BAYW/2 - 0.4, u - BAYW/2 + 0.4, MY1 + 0.6, MY1 + 1.4, 14.17, MH)   # buttress strips
for k in range(NB + 1):
    u = FX0 + k*BAYW; S.box(u - 0.6, u + 0.6, MY1 - 0.6, MY1 + 0.6, MH - 3, MH + 1.5); S.cyl(u, MY1, MH + 1.5, MH + 6, 0.8, 0.02, seg=4)   # pinnacles
bx(S, MX0 - 1, MX1 + 1, MY1 - 1.4, MY1 + 0.9, MH - 3, MH - 2.2)                    # string course / cresting base
for k in range(int((MX1 - MX0)/2.0)):
    u = MX0 + 2.0*k; S.box(u, u + 1.0, MY1 - 0.4, MY1 + 0.4, MH - 3, MH - 1.6)        # battlement cresting
for k in range(NB):
    place('sy-gothic-arch-fragment', MC, FX0 + (k + 0.5)*BAYW, MY1 + 0.0, 0, math.pi, want='Model')   # faces the nave (+Y)
# screen between English and German sections (x 446), bays along Y, open arcade
SXS = 456.0; NB2 = 7; SY0 = (MY0 + MY1)/2 - NB2*BAYW/2
for k in range(NB2):
    place('sy-gothic-arch-fragment', MC, SXS, SY0 + (k + 0.5)*BAYW, 0, math.pi/2, want='Model')
bx(S, SXS - 1.2, SXS + 1.2, SY0, SY0 + NB2*BAYW, 14.17, 18.5)
# --- Rochester doorway (court face, +Y) ---
FYR = MY0 + 1.0                                                                     # wall face
DEP = 0.9
for k in range(5):
    r0, r1 = 3.5 + k, 4.5 + k; yfront = FYR + DEP*(k + 1)
    for s in (-1, 1):
        bx(S, RCX + s*r0, RCX + s*r1, FYR, yfront, 0, 9.0)                           # jamb order
        MBm['dark'].cyl(RCX + s*(r0 + 0.45), yfront + 0.3, 0.6, 8.3, 0.33, 0.33, seg=10)   # nook shaft
        bx(S, RCX + s*(r0 + 0.05) - 0.45, RCX + s*(r0 + 0.05) + 0.85, yfront - 0.2, yfront + 0.75, 8.3, 9.0)   # cushion capital
    ring_xz(S, RCX, 9.0, r0, r1, FYR, yfront, 0, math.pi, 24)
    if k in (1, 3):                                                                 # chevron orders
        for i in range(18):
            ta, tb = math.pi*i/18, math.pi*(i + 1)/18; tm = (ta + tb)/2
            rr_a, rr_b = (r0 + 0.1, r1 - 0.1) if i % 2 else (r1 - 0.1, r0 + 0.1)
            S.poly([(RCX + rr_a*math.cos(ta), yfront + 0.02, 9.0 + rr_a*math.sin(ta)), (RCX + rr_b*math.cos(tm), yfront + 0.02, 9.0 + rr_b*math.sin(tm)),
                    (RCX + rr_a*math.cos(tb), yfront + 0.25, 9.0 + rr_a*math.sin(tb))])
bx(S, RCX - 9.5, RCX + 9.5, FYR, FYR + DEP*5 + 0.3, 14.2, 15.0)                     # hood / string over the outer order
bx(S, RCX - 3.5, RCX + 3.5, FYR - 0.2, FYR + 0.4, 8.2, 9.0)                         # lintel
for i in range(12): bx(MBm['stone'], RCX - 3.3 + i*0.55, RCX - 3.3 + i*0.55 + 0.4, FYR + 0.4, FYR + 0.6, 8.25, 8.95)   # apostles (massing)
_ty = MBm['stone']; bm = _ty.bm
plate(_ty, 'x', FYR + 0.1, [(RCX + 3.5*math.cos(math.pi*i/20), 9.0 + 3.5*math.sin(math.pi*i/20)) for i in range(21)])   # tympanum
plate(MBm['gold'], 'x', FYR + 0.35, [(RCX + 1.0*math.cos(2*math.pi*i/24), 10.6 + 1.7*math.sin(2*math.pi*i/24)) for i in range(24)])   # mandorla
bx(MBm['stone'], RCX - 0.45, RCX + 0.45, FYR + 0.35, FYR + 0.75, 9.6, 11.6)         # seated Christ (massing)
for s in (-1, 1):                                                                   # evangelist symbols (massing)
    bx(MBm['stone'], RCX + s*2.1 - 0.4, RCX + s*2.1 + 0.4, FYR + 0.15, FYR + 0.45, 9.4, 10.5)
bx(MBm['oak'], RCX - 3.5, RCX + 3.5, FYR - 1.2, FYR - 0.9, 0, 8.2)                   # door leaves
for i in range(6): bx(MBm['dark'], RCX - 3.4, RCX + 3.4, FYR - 0.9, FYR - 0.8, 1 + i*1.3, 1.15 + i*1.3)   # iron straps
# --- stained glass ---
SG = [stained_mat('med_stained_glass_A', 7.0, 4.5, 0), stained_mat('med_stained_glass_B', 9.0, 4.5, 3), stained_mat('med_stained_glass_C', 6.0, 4.5, 5)]
sgm = [MB('mediaeval_stained_glass_%d' % i, MC, m) for i, m in enumerate(SG)]
# English section west wall (x 392, inner face +X): three lancets + roundel; German east wall: rose over two lancets
WFX = MX0 + 1.0
for j, (yc, w) in enumerate(((-78.5, 3.8), (-72.0, 4.4), (-65.5, 3.8))):
    zs_ = 19.0 if j == 1 else 17.5
    plate(sgm[j % 3], 'y', WFX + 0.06, lancet(yc, w, 6.0, zs_))
    plate(MBm['dark'], 'y', WFX + 0.03, lancet(yc, w + 1.0, 5.5, zs_))
    for z in range(8, int(zs_), 3): bx(MBm['dark'], WFX + 0.06, WFX + 0.14, yc - w/2, yc + w/2, z, z + 0.12)   # saddle bars
plate(sgm[1], 'y', WFX + 0.06, [(-72 + 2.4*math.cos(2*math.pi*i/24), 25.0 + 2.4*math.sin(2*math.pi*i/24)) for i in range(24)])
ring_xz(MBm['stone'], -72.0, 25.0, 2.4, 3.0, WFX, WFX + 0.4, 0, 2*math.pi, 24, ax='y')
EFX = MX1 - 1.0
plate(sgm[2], 'y', EFX - 0.06, [(-80 + 5.5*math.cos(2*math.pi*i/40), 19.5 + 5.5*math.sin(2*math.pi*i/40)) for i in range(40)])
ring_xz(MBm['stone'], -80.0, 19.5, 5.5, 6.4, EFX - 0.5, EFX, 0, 2*math.pi, 40, ax='y')
for i in range(8):                                                                  # rose spokes
    a = math.pi*i/8; MBm['stone'].strut((EFX - 0.2, -80 + 5.5*math.cos(a), 19.5 + 5.5*math.sin(a)), (EFX - 0.2, -80 - 5.5*math.cos(a), 19.5 - 5.5*math.sin(a)), 0.28)
for yc in (-86.0, -74.0):
    plate(sgm[0], 'y', EFX - 0.06, lancet(yc, 3.6, 3.5, 11.0)); plate(MBm['dark'], 'y', EFX - 0.03, lancet(yc, 4.6, 3.0, 11.0))
for xc_ in (462.0, 476.0):                                                          # German back-wall lancets
    plate(sgm[1], 'x', FYR + 0.06, lancet(xc_, 4.0, 6.0, 18.0)); plate(MBm['dark'], 'x', FYR + 0.03, lancet(xc_, 5.0, 5.5, 18.0))
# English monuments: tomb chest with effigy, font (I - the court held casts of tombs/effigies, which ones U)
bx(MBm['stone'], 404, 413, -78, -74, 0, 3.0); bx(MBm['dark'], 404.5, 412.5, -77.5, -74.5, 3.0, 3.25)
bx(MBm['stone'], 405.5, 411.5, -76.6, -75.4, 3.25, 4.0); MBm['stone'].cyl(405.6, -76.0, 3.25, 4.2, 0.55, 0.5, seg=10)
for k in range(5): bx(MBm['blue'], 404.6 + k*1.7, 405.6 + k*1.7, -78.05, -77.95, 0.6, 2.4)
MBm['stone'].cyl(432, -72, 0, 0.6, 2.2, 2.2, seg=8); MBm['stone'].cyl(432, -72, 0.6, 2.6, 0.8, 0.8, seg=8); MBm['stone'].cyl(432, -72, 2.6, 4.0, 1.7, 2.0, seg=8)
for k, m in MBm.items(): m.done()
for m in sgm: m.done()
mp = []
for i in range(36):
    x = PRNG2.uniform(MX0 + 3, MX1 - 3); y = PRNG2.uniform(MY0 + 7, MY1 - 3)
    if abs(x - SXS) < 2.5 or (402 < x < 415 and -80 < y < -72) or (abs(x - 432) < 3 and abs(y + 72) < 3) or near_col(x, y, 1.6): continue
    mp.append((x, y, 0.05, public(PRNG2), PRNG2.uniform(-math.pi, math.pi)))
for i in range(16):
    mp.append((PRNG2.uniform(MX0, MX1), PRNG2.uniform(-34, -14), 0, public(PRNG2), PRNG2.uniform(-math.pi, math.pi)))
cam('CAM_CP040_mediaeval_court_28mm', (452, -50, EYE), (398, -96, 13), 28)   # r14: out of the north-transept braced stack (x 468-492)
cam('CAM_CP040_rochester_door_50mm', (RCX + 3, -84, EYE), (RCX, MY0, 9.5), 50)
cam('CAM_CP040_mediaeval_front_28mm', (446, -6, EYE), (410, -46, 14), 28)   # r13b: moved off a nave pier
people('ppl57_mediaeval_visitors', MC, mp)
print('COURTS2 ok; muse props', [k for k, v in _MUSE.items() if v])
