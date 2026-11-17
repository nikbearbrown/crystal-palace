"""CP038 CANDIDATE (2026-11-17, no verdict): 'Egypt, interpreted in South London' - the outer court of the Egyptian Court as
the 1854 visitor met it: the avenue of Prudhoe-lion casts up to the Ptolemaic portico, coloured sunk reliefs on the portico
screen walls, the winged globe over the central entrance, and a few Victorian visitors.

usage: blender -b rounds/sydenham-1856-r08.blend -P scripts/candidate_cp038_lions.py [-- out.blend]   (env CP038_NOSAVE=1: no save)
Base = rounds/sydenham-1856-r08.blend (md5 0aa6e9ce, unchanged since 968c1d5) - the blend the live CP038 hero
  renders/r08final_CAM_CP038_egyptian_hold_28mm.png was rendered from (survey look v1.1 batch, look/sydenham_logs/CP038.log:
  apply_render.py --scene-id CP038 --era 1851 --tod interior_daylit --spp 24 --res 1280x720 --no-people; re-render max diff 0).
  -> rounds/candidates/sydenham-1856-r08_cp038lions.blend
Live hero shows: the Ptolemaic screen (lower facade of the Hall of Columns, y 111.6 ft) as plain sandstone boxes, a plain
yellow architrave, and the lower ~30 % of the frame an empty grey floor - no sculpture, no visitors.
Sources:
  M. D. Wyatt, Views of the Crystal Palace and Park, Sydenham (1854), Plate V 'The Egyptian Court, as seen from the Nave'
    (victorianweb transcription): portico of the Ptolemaic period (Edfu arrangement); 'The lions which guard the approach on
    either side have been taken from those ... presented to the British Museum by ... Lord Prudhoe'; 'The winged globe, with
    serpents beneath it, in the centre of the frieze over the main entrances'.
  Phillips, Guide to the Crystal Palace (1854), 'A walk through the nave' (sydenham.org.uk transcription): 'Advancing up the
    avenue of lions, cast from a pair brought from Egypt by Lord Prudhoe ... we have before us the outer walls and columns of a
    temple ... On the walls are coloured sunk-reliefs showing a king making offerings or receiving gifts from the gods.'
  British Museum EA2 (Prudhoe lion): red granite, H 115 cm, L 216 cm, W 99 cm; recumbent on its side, forepaws crossed,
    circular mane, head turned, tail curled round the rump onto the base; 'a mirror image to its companion piece'.
  Spectator 24 Jun 1854: the older lions 'at the entrance from the nave'.
  Guide 1856 p.47 plan 0226 (outer court between the nave front and the Facade of the Hall of Columns, nothing drawn in it).
  Storyboard CP038: 'Painted columns and reproduced sculpture frame visitors in Victorian clothing'.
Interpretation (I): the model (r08, D-R08) puts the Ptolemaic portico at the lower facade of the Hall of Columns, inside the
  court; the avenue is therefore laid in the model's outer court on the axis of the portico's open centre bay, from the nave
  doorway to the portico. Count (3 pairs), plinths, colours of the casts and relief drawing are I/U.
Adds dated collection SY54_egyptian_outer_court_lion_avenue__1854_1856 (cp_state on every object). Camera NOT moved,
sun/world/exposure/look NOT changed, nothing hidden or deleted.
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector, Matrix

F = 0.3048
f = lambda v: v * F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP038_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-1856-r08_cp038lions.blend')
STATE = 'SY54_egyptian_outer_court_lion_avenue__1854_1856'
RNG = random.Random(1854038)
CAM = bpy.data.objects['CAM_CP038_egyptian_hold_28mm']
EGC = bpy.data.collections['SY56_court_egyptian_0226__dated']
parent = next(c for c in bpy.data.collections if EGC.name in [k.name for k in c.children])
col = bpy.data.collections.get(STATE) or bpy.data.collections.new(STATE)
if col.name not in [c.name for c in parent.children]: parent.children.link(col)
col['cp_state'] = STATE
col['evidence'] = ('Wyatt 1854 Plate V + Phillips 1854: avenue of Prudhoe-lion casts guarding the approach to the Ptolemaic '
                   'portico R; coloured sunk reliefs (king offering / receiving gifts) on the portico walls R (drawing I/U); winged '
                   'globe with serpents over the main entrance R (form I); BM EA2 dimensions R; placement in the model outer court I; '
                   'count 3 pairs, plinths, cast colour I; 1850s visitors I')
INFO = {}

# ---------------------------------------------------------------- helpers (copied from build.py so ornament.NG works)
def mat(name, base, rough=0.5, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*base, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal; return m
def socket(node, ident, out=False):
    return [x for x in (node.outputs if out else node.inputs) if x.identifier == ident][0]
exec(open(os.path.join(HERE, 'ornament.py')).read())      # NG node helper (defs only)

def new_obj(name, bm, m, origin=(0, 0, 0), smooth=False):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    if smooth:
        for p in me.polygons: p.use_smooth = True
    me.materials.append(m)
    o = bpy.data.objects.new(name, me); o.location = origin; col.objects.link(o); o['cp_state'] = STATE; return o
def box(bm, x0, x1, y0, y1, z0, z1):   # ft
    r = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(f(x1 - x0), f(y1 - y0), f(z1 - z0)), verts=r['verts'])
    bmesh.ops.translate(bm, vec=(f((x0 + x1) / 2), f((y0 + y1) / 2), f((z0 + z1) / 2)), verts=r['verts'])
def ell(bm, M, c, r, seg=20, rings=12):
    """ellipsoid at local c (ft) radii r (ft), transformed by M (local ft -> world m)"""
    s = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0)
    for v in s['verts']:
        p = Vector((c[0] + v.co.x * r[0], c[1] + v.co.y * r[1], c[2] + v.co.z * r[2])); v.co = M @ p

# ---------------------------------------------------------------- materials
def granite():
    m = mat('cp038_lion_cast_red_granite', (0.44, 0.20, 0.15), 0.42); g = NG(m)
    nz = g.noise(60.0, 2.0); sp = g.noise(240.0, 1.0)
    c = g.mix(nz, (0.36, 0.15, 0.11), (0.52, 0.25, 0.18)); c = g.mix(g.op('GREATER_THAN', sp, 0.66), c, (0.16, 0.10, 0.09))
    g.finish(c, g.noise(90.0, 3.0), 0.25, 0.004); return m
M_LION = granite()
M_PL = mat('cp038_plinth_sandstone', (0.80, 0.64, 0.44), 0.8)
_g = NG(M_PL); _g.finish(_g.mix(_g.noise(3.0, 4.0), (0.70, 0.54, 0.36), (0.85, 0.70, 0.49)), _g.noise(18.0, 3.0), 0.5, 0.01)
M_BAND = mat('cp038_plinth_cavetto_painted', (0.16, 0.27, 0.45), 0.6)
_g = NG(M_BAND); _st = _g.op('FRACT', _g.op('DIVIDE', _g.add(_g.sp.outputs['X'], _g.sp.outputs['Y']), f(0.9)))
_rp = _g.n.new('ShaderNodeValToRGB'); _cr = _rp.color_ramp; _cr.interpolation = 'CONSTANT'
_cr.elements[0].position, _cr.elements[0].color = 0.0, (0.16, 0.27, 0.45, 1); _cr.elements[1].position, _cr.elements[1].color = 0.25, (0.80, 0.64, 0.44, 1)
for _p, _c in ((0.33, (0.55, 0.20, 0.12)), (0.58, (0.80, 0.64, 0.44)), (0.66, (0.22, 0.40, 0.30)), (0.92, (0.80, 0.64, 0.44))):
    _e = _cr.elements.new(_p); _e.color = (*_c, 1)
_g.l.new(_st, _rp.inputs[0]); _g.l.new(_rp.outputs[0], _g.b.inputs['Base Color'])
def walk_mat():
    m = mat('cp038_walk_flags_sandstone', (0.74, 0.62, 0.46), 0.85); g = NG(m)
    X = g.op('DIVIDE', g.sp.outputs['X'], F); Y = g.op('DIVIDE', g.sp.outputs['Y'], F)
    row = g.op('FLOOR', g.op('DIVIDE', Y, 2.5)); xo = g.add(X, g.mul(g.op('FRACT', g.mul(row, 0.5)), 3.5))
    jx = g.op('LESS_THAN', g.op('FRACT', g.op('DIVIDE', xo, 3.5)), 0.018); jy = g.op('LESS_THAN', g.op('FRACT', g.op('DIVIDE', Y, 2.5)), 0.025)
    j = g.op('MAXIMUM', jx, jy)
    tone = g.white(g.op('FLOOR', g.op('DIVIDE', xo, 3.5)), row)
    c = g.mix(tone, (0.66, 0.54, 0.39), (0.80, 0.68, 0.51)); c = g.mix(g.mul(g.noise(4.0, 3.0), 0.5), c, (0.60, 0.50, 0.37))
    c = g.mix(j, c, (0.30, 0.25, 0.19))
    g.finish(c, g.op('SUBTRACT', g.mul(g.noise(20.0, 2.0), 0.2), j), 0.5, 0.008); return m
M_WALK = walk_mat()

def relief_mat(W, H):
    """coloured sunk relief panel (local object coords: X 0..W ft along the wall, Z 0..H ft): king offering a bowl (left,
    facing right) to a standing god with was-sceptre and plumed crown (right, facing left), glyph column between, blue/yellow
    frame, star-strewn sky band. Drawing generic (U), subject per Phillips 1854 (R)."""
    m = mat('cp038_portico_sunk_relief_%d' % int(W * 10), (0.80, 0.64, 0.44), 0.75); g = NG(m)
    s = g.op('DIVIDE', g.sp.outputs['X'], F); t = g.op('DIVIDE', g.sp.outputs['Z'], F)   # ft
    BLUE, RED, GRN, YEL, BLK, WHT = (0.13, 0.24, 0.47), (0.58, 0.19, 0.10), (0.18, 0.40, 0.28), (0.86, 0.64, 0.22), (0.10, 0.09, 0.09), (0.88, 0.85, 0.74)
    base = g.mix(g.noise(2.0, 3.0), (0.74, 0.58, 0.39), (0.86, 0.71, 0.50))
    def E(a, b, cx, cy, rx, ry):
        u = g.op('DIVIDE', g.op('SUBTRACT', a, cx), rx); v = g.op('DIVIDE', g.op('SUBTRACT', b, cy), ry)
        return g.op('LESS_THAN', g.add(g.mul(u, u), g.mul(v, v)), 1.0)
    def R(a, b, x0, x1, y0, y1): return g.mul(g.band(a, x0, x1), g.band(b, y0, y1))
    def U(*ms):
        r = ms[0]
        for k in ms[1:]: r = g.op('MAXIMUM', r, k)
        return r
    def figure(cx, d, god):
        a = g.mul(g.op('SUBTRACT', s, cx), d)          # a > 0 = the way the figure faces
        b = g.op('SUBTRACT', t, 0.55)                    # standing line 0.55 ft above panel foot
        legs = U(R(a, b, 0.14, 0.30, 0.0, 1.25), R(a, b, -0.36, -0.20, 0.0, 1.25), R(a, b, 0.14, 0.42, 0.0, 0.08), R(a, b, -0.36, -0.12, 0.0, 0.08))
        kilt = g.mul(g.band(b, 1.15, 1.85), g.op('LESS_THAN', g.op('ABSOLUTE', g.op('SUBTRACT', a, 0.02)), g.add(0.26, g.mul(g.op('SUBTRACT', 1.85, b), 0.28))))
        torso = U(E(a, b, 0.0, 2.35, 0.27, 0.55), R(a, b, -0.24, 0.24, 1.8, 2.3))
        neck = R(a, b, -0.07, 0.09, 2.85, 3.05)
        head = U(E(a, b, 0.05, 3.22, 0.20, 0.22), E(a, b, 0.24, 3.13, 0.07, 0.06))
        wig = E(a, b, -0.05, 3.30, 0.22, 0.22)
        if god:
            arm = U(R(a, b, 0.0, 0.42, 2.48, 2.60))
            staff = U(R(a, b, 0.40, 0.48, 0.0, 3.25), R(a, b, 0.40, 0.60, 3.18, 3.30))
            crown = U(R(a, b, -0.20, -0.02, 3.45, 4.15), R(a, b, 0.0, 0.18, 3.45, 4.15))
            skin = (0.20, 0.34, 0.58)        # Amun blue (I)
            prop = staff; propc = YEL
        else:
            arm = U(R(a, b, 0.0, 0.62, 2.50, 2.62), R(a, b, 0.0, 0.58, 2.20, 2.32))
            prop = U(E(a, b, 0.72, 2.70, 0.20, 0.09), E(a, b, 0.70, 2.86, 0.10, 0.10))     # offering bowl with a loaf
            crown = R(a, b, -0.20, 0.16, 3.42, 3.62)
            skin = (0.62, 0.30, 0.16); propc = YEL
        body = U(legs, torso, neck, head, arm)
        shape = U(body, kilt, wig, crown, prop)
        c = g.mix(body, base, skin); c = g.mix(kilt, c, WHT); c = g.mix(wig, c, BLK); c = g.mix(crown, c, BLUE if not god else RED)
        c = g.mix(prop, c, propc); return shape, c
    sh1, c1 = figure(W * 0.28, 1.0, False); sh2, c2 = figure(W * 0.76, -1.0, True)
    # glyph column between the figures
    gc = g.op('DIVIDE', g.op('SUBTRACT', t, 1.0), 0.42); gq = g.op('FRACT', gc); gr = g.white(g.op('FLOOR', gc), 3.1)
    glyph = g.mul(g.mul(g.band(t, 1.0, H - 1.25), g.op('LESS_THAN', g.op('ABSOLUTE', g.op('SUBTRACT', s, W * 0.52)), 0.17)), g.band(gq, 0.18, 0.82))
    glc = g.mix(g.op('LESS_THAN', gr, 0.33), g.mix(g.op('LESS_THAN', gr, 0.66), GRN, RED), BLUE)
    # frame + sky band
    inner = g.mul(g.band(s, 0.32, W - 0.32), g.band(t, 0.35, H - 0.35))
    frame_y = g.mul(g.band(s, 0.14, W - 0.14), g.band(t, 0.17, H - 0.17))
    sky = g.mul(inner, g.op('GREATER_THAN', t, H - 0.95))
    star = g.mul(sky, g.op('LESS_THAN', g.op('ABSOLUTE', g.op('SUBTRACT', g.op('FRACT', g.op('DIVIDE', s, 0.5)), 0.5)), 0.12))
    c = g.mix(g.op('SUBTRACT', 1.0, frame_y), base, BLUE)
    c = g.mix(g.mul(frame_y, g.op('SUBTRACT', 1.0, inner)), c, YEL)
    c = g.mix(sky, c, BLUE); c = g.mix(g.mul(star, g.band(g.op('FRACT', g.op('DIVIDE', t, 0.3)), 0.3, 0.7)), c, YEL)
    c = g.mix(g.mul(inner, sh1), c, c1); c = g.mix(g.mul(inner, sh2), c, c2); c = g.mix(glyph, c, glc)
    sunk = g.mul(inner, U(sh1, sh2, glyph))
    h = g.op('SUBTRACT', 1.0, g.add(g.mul(sunk, 0.8), g.mul(g.op('SUBTRACT', 1.0, inner), 0.25)))
    g.finish(c, h, 0.9, 0.010); return m

M_DISC = mat('cp038_winged_globe_red', (0.62, 0.17, 0.08), 0.5)
M_WB = mat('cp038_winged_globe_wing_blue', (0.13, 0.24, 0.47), 0.6)
M_WR = mat('cp038_winged_globe_wing_red', (0.58, 0.19, 0.10), 0.6)
M_WG = mat('cp038_winged_globe_wing_green', (0.18, 0.40, 0.28), 0.6)
M_WY = mat('cp038_winged_globe_gilt_yellow', (0.86, 0.64, 0.22), 0.45)

# ---------------------------------------------------------------- model geometry (ft, from courts.py r08 / raycast)
ex = lambda px: 180 + (px - 118) / 3.875
ey = lambda py: 60 + (800 - py) / 3.875
KX = [ex(px) for px in (248, 278, 310, 342, 373, 405, 436, 466)]
yLF = ey(600)                              # portico (lower facade of the Hall of Columns) line, 111.61 ft
FACE = yLF - 0.9                           # screen-wall face toward the nave, 110.71 ft
ARCH = yLF - 1.5                           # architrave face, 110.11 ft (z 17.6-19.4)
AX = (KX[3] + KX[4]) / 2                   # axis of the open centre bay, 241.81 ft
Z0 = 0.12                                  # court floor top (eg_floor 0..0.12 ft)
INFO['axis_ft'] = round(AX, 2); INFO['portico_face_ft'] = round(FACE, 2)

# 1. flagged walk, 10 ft, nave doorway -> portico centre bay
bm = bmesh.new(); box(bm, AX - 5.0, AX + 5.0, 61.2, FACE - 0.05, Z0, Z0 + 0.08)
new_obj('cp038_avenue_walk_flags', bm, M_WALK)
INFO['walk_ft'] = (10.0, round(FACE - 0.05 - 61.2, 2))

# 2. plinths + 6 lions (3 pairs, mirror images), heads toward the nave
LL, LW, LH = 7.09, 3.25, 3.77              # BM EA2: L 216 cm, W 99 cm, H 115 cm (incl. its base)
PL_L, PL_W, PL_H = 8.0, 3.8, 1.35          # low pedestal (I): lion crown ~5.1 ft, just under the 5.25 ft eye
YS = [82.0, 91.5, 101.0]                   # 3 pairs (I); the nave-side pair would sit beside the lens
bmp = bmesh.new(); bmb = bmesh.new(); bml = bmesh.new(); bmd_ = bmesh.new()
lion_boxes = []
for side in (-1, 1):
    xc = AX + side * (6.0 + PL_W / 2)
    for yc in YS:
        box(bmp, xc - PL_W / 2 - 0.25, xc + PL_W / 2 + 0.25, yc - PL_L / 2 - 0.25, yc + PL_L / 2 + 0.25, Z0, Z0 + 0.35)   # foot
        box(bmp, xc - PL_W / 2, xc + PL_W / 2, yc - PL_L / 2, yc + PL_L / 2, Z0 + 0.35, Z0 + PL_H - 0.45)
        box(bmb, xc - PL_W / 2 - 0.12, xc + PL_W / 2 + 0.12, yc - PL_L / 2 - 0.12, yc + PL_L / 2 + 0.12, Z0 + PL_H - 0.45, Z0 + PL_H - 0.15)
        box(bmp, xc - PL_W / 2 - 0.3, xc + PL_W / 2 + 0.3, yc - PL_L / 2 - 0.3, yc + PL_L / 2 + 0.3, Z0 + PL_H - 0.15, Z0 + PL_H)
        zt = Z0 + PL_H
        # local lion frame: +x = head direction (world -y, toward the nave and the approaching visitor), +y = flank toward the walk axis
        # (pair mirrored, BM: 'a mirror image to its companion piece'); head frontal, NOT turned as on EA1/EA2 (I, readability); ft -> m
        tw = -side                          # world x direction of the walk axis from this plinth
        Mx = Matrix(((0, tw * 1, 0), (-1, 0, 0), (0, 0, 1)))       # columns: local x -> (0,-1,0), local y -> (tw,0,0)
        Mx = Matrix(((0, tw, 0, 0), (-1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
        SZ = Matrix.Diagonal((1.0, 1.0, LH / 3.24, 1.0))     # sculpted at 3.24 ft crown -> scaled to the BM 3.77 ft height
        M = Matrix.Translation((f(xc), f(yc), f(zt))) @ Matrix.Scale(F, 4) @ SZ @ Mx
        b0 = 0.42
        # base slab (part of the cast)
        r = bmesh.ops.create_cube(bml, size=1.0)
        for v in r['verts']: v.co = M @ Vector((v.co.x * LL, v.co.y * LW, b0 / 2 + v.co.z * b0))
        ell(bml, M, (-0.55, 0.0, b0 + 0.80), (2.35, 0.88, 0.78))          # long low body
        ell(bml, M, (-0.30, 0.0, b0 + 1.38), (1.90, 0.40, 0.22), 16, 8)   # spine / back ridge
        ell(bml, M, (-2.05, 0.08, b0 + 0.88), (0.95, 0.92, 0.88))         # haunch
        ell(bml, M, (1.05, 0.0, b0 + 0.98), (0.90, 0.88, 0.95))           # chest / shoulders
        ell(bml, M, (1.55, 0.0, b0 + 1.72), (0.55, 0.92, 0.98), 24, 12)   # mane mass behind the face
        for k in range(28):                                                # circular mane ruff framing the face (BM: 'stylized circular mane')
            t_ = 2 * math.pi * k / 28
            ell(bml, M, (1.98, 0.74 * math.cos(t_), b0 + 1.78 + 0.80 * math.sin(t_)), (0.20, 0.24, 0.24), 10, 6)
        ell(bml, M, (2.05, 0.0, b0 + 1.80), (0.42, 0.52, 0.56))           # face
        ell(bml, M, (2.48, 0.0, b0 + 1.55), (0.34, 0.32, 0.27))           # projecting muzzle
        ell(bml, M, (2.36, 0.0, b0 + 1.95), (0.18, 0.40, 0.10), 12, 6)    # brow
        for ez in (-0.48, 0.48): ell(bml, M, (1.92, ez, b0 + 2.55), (0.12, 0.13, 0.16), 10, 6)   # ears on the ruff
        for ez in (-0.20, 0.20): ell(bmd_, M, (2.40, ez, b0 + 1.82), (0.06, 0.09, 0.05), 8, 6)  # eye hollows (dark)
        ell(bmd_, M, (2.80, 0.0, b0 + 1.62), (0.06, 0.13, 0.07), 8, 6)  # nose
        for py_, dz in ((0.30, 0.0), (-0.30, 0.0)): ell(bml, M, (2.70, py_, b0 + 0.22 + dz), (0.90, 0.26, 0.22))   # forepaws forward
        ell(bml, M, (-1.60, 0.88, b0 + 0.44), (0.95, 0.22, 0.40))         # near hind leg on the flank
        ell(bml, M, (-0.55, 1.02, b0 + 0.17), (0.48, 0.22, 0.17))         # hind paw forward
        for k in range(9):                                                 # tail curled round the rump onto the base
            a_ = math.pi * (0.95 - 0.55 * k / 8)
            ell(bml, M, (-2.55 + 1.05 * math.cos(a_) + 0.9, 1.05 * math.sin(a_) * 1.1, b0 + 0.11), (0.13, 0.13, 0.11), 10, 6)
        lion_boxes.append((xc, yc, zt))
new_obj('cp038_lion_plinths_sandstone', bmp, M_PL); new_obj('cp038_lion_plinth_cornice_band', bmb, M_BAND)
L = new_obj('cp038_prudhoe_lion_casts_x6', bml, M_LION, smooth=True)
new_obj('cp038_lion_eyes_nose_dark', bmd_, mat('cp038_lion_cast_dark_hollows', (0.08, 0.05, 0.045), 0.7), smooth=True)
INFO['lions'] = len(lion_boxes); INFO['lion_dims_ft'] = (LL, LW, LH); INFO['plinth_ft'] = (PL_L, PL_W, PL_H)

# 3. coloured sunk-relief panels on the six portico screen walls (face y 110.71 ft, wall 0..7.5 ft)
np_ = 0
for i in range(len(KX) - 1):
    if i == 3: continue
    x0, x1 = KX[i] + 1.4, KX[i + 1] - 1.4; W, H = x1 - x0, 7.5 - 0.9
    bm = bmesh.new()
    vs = [bm.verts.new((f(a), 0.0, f(c))) for a, c in ((0, 0), (W, 0), (W, H), (0, H))]
    bm.faces.new(vs)
    o = new_obj('cp038_portico_relief_panel_%d' % i, bm, relief_mat(W, H), origin=(f(x0), f(FACE - 0.03), f(0.9)))
    np_ += 1
INFO['relief_panels'] = np_

# 4. winged globe with two uraei on the architrave over the open centre bay
bmd = bmesh.new(); bmw = {k: bmesh.new() for k in 'BRGY'}
yD = ARCH - 0.06; zc = 18.65
Mw = Matrix.Translation((f(AX), f(yD), f(zc))) @ Matrix.Scale(F, 4)
ell(bmd, Mw, (0, -0.10, 0), (0.62, 0.18, 0.62), 24, 10)                # sun disc
for sd in (-1, 1):
    # wing: three feather tiers sweeping out and down, each a thin slab
    for tier, (key, z0_, z1_, x1_) in enumerate((('Y', 0.38, 0.62, 4.6), ('B', 0.05, 0.38, 4.9), ('R', -0.28, 0.05, 4.4), ('G', -0.62, -0.28, 3.6))):
        bmx = bmw[key]
        x0_ = 0.7
        quad = [(x0_, z0_), (x1_, z0_ - 0.25), (x1_, z1_ - 0.22), (x0_, z1_)]
        vs = [bmx.verts.new(Mw @ Vector((sd * xq, -0.05 - 0.02 * tier, zq))) for xq, zq in quad]
        bmx.faces.new(vs if sd > 0 else vs[::-1])
    # uraeus hanging from the disc
    ell(bmw['Y'], Mw, (sd * 0.48, -0.16, -0.58), (0.12, 0.10, 0.25), 10, 8)
    ell(bmw['Y'], Mw, (sd * 0.48, -0.18, -0.30), (0.15, 0.10, 0.11), 10, 6)
new_obj('cp038_winged_globe_disc', bmd, M_DISC, smooth=True)
for key, mm in (('B', M_WB), ('R', M_WR), ('G', M_WG), ('Y', M_WY)):
    new_obj('cp038_winged_globe_wings_' + key, bmw[key], mm, smooth=(key == 'Y'))
INFO['winged_globe_span_ft'] = 2 * 4.9

# 5. Victorian visitors (people_lib v3.4, 1850s), well clear of the lens and of the centre bay
from cpl_people import person_mesh
camx, camy = CAM.location.x / F, CAM.location.y / F
people = []
def put(name, role, pose, x, y, face, seed, lod):
    person_mesh(name, role, style={'role': role, 'pose': pose, 'lod': lod, 'era': '1850s'}, seed=seed)
    o = bpy.data.objects[name]
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o.location = (f(x), f(y), f(Z0 + 0.08))
    o.rotation_euler = (0, 0, math.atan2(face[0], -face[1]) + RNG.uniform(-0.15, 0.15))   # base meshes face local -Y
    o['cp_state'] = STATE; o['cpl_people'] = 'cpl_people_v3'; people.append(o); return o
N_, S_, E_, W_ = (0, 1), (0, -1), (1, 0), (-1, 0)
G = [(237.6, 103.5, '1850s_gentleman', 'walking', N_), (238.5, 104.2, '1850s_lady', 'walking', N_),
     (246.0, 94.0, '1850s_lady', 'standing', E_), (245.4, 95.4, '1850s_girl', 'standing', E_),
     (236.9, 99.5, '1850s_gentleman', 'pointing', W_)]
nearest = 1e9
for n, (x, y, role, pose, face) in enumerate(G):
    d = math.hypot(x - camx, y - camy) * F
    put('cp038_visitor_%02d' % n, role, pose, x, y, face, 1854380 + n * 11, 'hero' if d < 12 else 'mid')
    nearest = min(nearest, d)
INFO['people_lib_visitors'] = len(people); INFO['nearest_new_figure_m'] = round(nearest, 2)

for o in col.objects: o['cp_state'] = STATE
print('CP038 BUILT', INFO)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP038 SAVED', OUT)
