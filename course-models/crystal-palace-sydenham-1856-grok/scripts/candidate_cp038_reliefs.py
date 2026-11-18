"""CP038 CANDIDATE v2 (2026-11-17, no verdict): Egyptian Court outer court - coloured sunk reliefs on the Ptolemaic portico
screen walls (large, one register filling each screen), the winged sun disc with uraei over the open centre bay, a flagged walk
from the nave doorway and a few 1850s visitors. NO lion casts (v1 dd0e644 candidate_cp038_lions.py was rejected at review:
foreground lions read cartoonish/toy-like and dominated the frame; luma dropped 80 -> 71).

usage: blender -b rounds/sydenham-1856-r08.blend -P scripts/candidate_cp038_reliefs.py [-- out.blend]   (env CP038_NOSAVE=1: no save)
Base = rounds/sydenham-1856-r08.blend (md5 0aa6e9ce, unchanged since 968c1d5) - the blend the live CP038 hero
  renders/r08final_CAM_CP038_egyptian_hold_28mm.png was rendered from (survey look v1.1, look/sydenham_logs/CP038.log:
  apply_render.py --scene-id CP038 --era 1851 --tod interior_daylit --spp 24 --res 1280x720 --no-people; re-render max diff 0).
  -> rounds/candidates/sydenham-1856-r08_cp038reliefs.blend
Sources:
  Phillips, Guide to the Crystal Palace (1854), 'A walk through the nave': '... the outer walls and columns of a temple ... On
    the walls are coloured sunk-reliefs showing a king making offerings or receiving gifts from the gods.'
  M. D. Wyatt, Views of the Crystal Palace and Park, Sydenham (1854), Plate V: portico of the Ptolemaic period; 'The winged
    globe, with serpents beneath it, in the centre of the frieze over the main entrances'.
  Guide 1856 p.47 plan 0226 (outer court between the nave front and the Facade of the Hall of Columns).
  Storyboard CP038: 'Painted columns and reproduced sculpture frame visitors in Victorian clothing'.
Interpretation: relief drawing generic (U); subject R; one register per screen, figures scaled to fill the screen (I); disc span
  and colours I; walk I; visitors I. The Prudhoe-lion avenue (R, Wyatt/Phillips) is deliberately NOT modelled (departure).
Adds dated collection SY54_egyptian_outer_court_portico_reliefs__1854_1856 (cp_state on every object). Camera NOT moved,
sun/world/exposure/look NOT changed, nothing hidden or deleted.
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector, Matrix

F = 0.3048
f = lambda v: v * F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP038_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-1856-r08_cp038reliefs.blend')
STATE = 'SY54_egyptian_outer_court_portico_reliefs__1854_1856'
RNG = random.Random(1854382)
CAM = bpy.data.objects['CAM_CP038_egyptian_hold_28mm']
EGC = bpy.data.collections['SY56_court_egyptian_0226__dated']
parent = next(c for c in bpy.data.collections if EGC.name in [k.name for k in c.children])
col = bpy.data.collections.get(STATE) or bpy.data.collections.new(STATE)
if col.name not in [c.name for c in parent.children]: parent.children.link(col)
col['cp_state'] = STATE
col['evidence'] = ('Phillips 1854: coloured sunk reliefs (king offering / receiving gifts from the gods) on the portico walls R '
                   '(drawing U, one large register per screen I); Wyatt 1854 Plate V: winged globe with serpents over the main entrance R '
                   '(form/span/colour I); flagged walk I; 1850s visitors I; Prudhoe-lion avenue R but deliberately omitted (departure)')
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
def walk_mat():
    m = mat('cp038v2_walk_flags_sandstone', (0.80, 0.69, 0.53), 0.85); g = NG(m)
    X = g.op('DIVIDE', g.sp.outputs['X'], F); Y = g.op('DIVIDE', g.sp.outputs['Y'], F)
    row = g.op('FLOOR', g.op('DIVIDE', Y, 2.5)); xo = g.add(X, g.mul(g.op('FRACT', g.mul(row, 0.5)), 3.5))
    jx = g.op('LESS_THAN', g.op('FRACT', g.op('DIVIDE', xo, 3.5)), 0.018); jy = g.op('LESS_THAN', g.op('FRACT', g.op('DIVIDE', Y, 2.5)), 0.025)
    j = g.op('MAXIMUM', jx, jy)
    tone = g.white(g.op('FLOOR', g.op('DIVIDE', xo, 3.5)), row)
    c = g.mix(tone, (0.74, 0.63, 0.47), (0.88, 0.77, 0.60)); c = g.mix(g.mul(g.noise(4.0, 3.0), 0.5), c, (0.60, 0.50, 0.37))
    c = g.mix(j, c, (0.30, 0.25, 0.19))
    g.finish(c, g.op('SUBTRACT', g.mul(g.noise(20.0, 2.0), 0.2), j), 0.5, 0.008); return m
M_WALK = walk_mat()

K = 1.30                                   # figure scale: v1 figures were ~4.15 ft tall; v2 fill the screen register (I)
def relief_mat(W, H, idx):
    """coloured sunk relief panel (local object coords: X 0..W ft along the wall, Z 0..H ft): king offering a bowl to a standing
    god with was-sceptre and plumed crown, figures filling one register, cast-shadow edge on the sunk outline (lit from upper
    left), caption glyph column between the heads, cartouche, blue/yellow frame, star band. Alternate panels mirror the pair
    and swap the god's skin (Amun blue / Ra-Horakhty green) so the six screens do not repeat exactly. Drawing generic (U)."""
    m = mat('cp038v2_portico_sunk_relief_%d' % idx, (0.80, 0.64, 0.44), 0.75); g = NG(m)
    s = g.op('DIVIDE', g.sp.outputs['X'], F); t = g.op('DIVIDE', g.sp.outputs['Z'], F)   # ft
    BLUE, RED, GRN, YEL, BLK, WHT = (0.10, 0.22, 0.52), (0.66, 0.17, 0.08), (0.14, 0.44, 0.26), (0.92, 0.68, 0.18), (0.07, 0.06, 0.06), (0.93, 0.90, 0.80)
    base = g.mix(g.noise(2.0, 3.0), (0.86, 0.73, 0.53), (0.95, 0.84, 0.64))
    def E(a, b, cx, cy, rx, ry):
        u = g.op('DIVIDE', g.op('SUBTRACT', a, cx), rx); v = g.op('DIVIDE', g.op('SUBTRACT', b, cy), ry)
        return g.op('LESS_THAN', g.add(g.mul(u, u), g.mul(v, v)), 1.0)
    def R(a, b, x0, x1, y0, y1): return g.mul(g.band(a, x0, x1), g.band(b, y0, y1))
    def U(*ms):
        r = ms[0]
        for k in ms[1:]: r = g.op('MAXIMUM', r, k)
        return r
    def figure(ss, tt, cx, d, god, godskin):
        a = g.op('DIVIDE', g.mul(g.op('SUBTRACT', ss, cx), d), K)      # a > 0 = the way the figure faces (figure units)
        b = g.op('DIVIDE', g.op('SUBTRACT', tt, 0.50), K)                # standing line 0.50 ft above panel foot
        legs = U(R(a, b, 0.14, 0.30, 0.0, 1.25), R(a, b, -0.36, -0.20, 0.0, 1.25), R(a, b, 0.14, 0.42, 0.0, 0.08), R(a, b, -0.36, -0.12, 0.0, 0.08))
        kilt = g.mul(g.band(b, 1.15, 1.85), g.op('LESS_THAN', g.op('ABSOLUTE', g.op('SUBTRACT', a, 0.02)), g.add(0.26, g.mul(g.op('SUBTRACT', 1.85, b), 0.28))))
        torso = U(E(a, b, 0.0, 2.35, 0.27, 0.55), R(a, b, -0.24, 0.24, 1.8, 2.3))
        collar = g.mul(E(a, b, 0.0, 2.80, 0.30, 0.16), g.op('LESS_THAN', b, 2.85))
        neck = R(a, b, -0.07, 0.09, 2.85, 3.05)
        head = U(E(a, b, 0.05, 3.22, 0.20, 0.22), E(a, b, 0.24, 3.13, 0.07, 0.06))
        wig = E(a, b, -0.05, 3.30, 0.22, 0.22)
        if god:
            arm = U(R(a, b, 0.0, 0.42, 2.48, 2.60), R(a, b, -0.10, 0.30, 2.05, 2.16))
            staff = U(R(a, b, 0.40, 0.48, 0.0, 3.25), R(a, b, 0.40, 0.60, 3.18, 3.30))
            ankh = U(E(a, b, 0.36, 2.00, 0.06, 0.08), R(a, b, 0.34, 0.38, 1.70, 1.94), R(a, b, 0.28, 0.44, 1.90, 1.94))
            crown = U(R(a, b, -0.20, -0.02, 3.45, 4.15), R(a, b, 0.0, 0.18, 3.45, 4.15))
            skin = godskin; prop = U(staff, ankh); propc = YEL; crc = RED
        else:
            arm = U(R(a, b, 0.0, 0.62, 2.50, 2.62), R(a, b, 0.0, 0.58, 2.20, 2.32))
            prop = U(E(a, b, 0.72, 2.70, 0.20, 0.09), E(a, b, 0.70, 2.86, 0.10, 0.10))     # offering bowl with a loaf
            crown = U(R(a, b, -0.20, 0.16, 3.42, 3.62), E(a, b, 0.20, 3.50, 0.05, 0.08))   # khepresh band + uraeus
            skin = (0.66, 0.30, 0.14); propc = YEL; crc = BLUE
        body = U(legs, torso, neck, head, arm)
        shape = U(body, kilt, wig, crown, prop, collar)
        c = g.mix(body, base, skin); c = g.mix(kilt, c, WHT); c = g.mix(collar, c, GRN if not god else BLUE)
        c = g.mix(wig, c, BLK); c = g.mix(crown, c, crc); c = g.mix(prop, c, propc); return shape, c
    flip = (idx % 2 == 1)
    gskin = (0.16, 0.32, 0.66) if idx % 3 != 2 else (0.18, 0.50, 0.30)
    kx, gx, kd = (W * 0.27, W * 0.75, 1.0) if not flip else (W * 0.73, W * 0.25, -1.0)
    sh1, c1 = figure(s, t, kx, kd, False, gskin); sh2, c2 = figure(s, t, gx, -kd, True, gskin)
    # cast-shadow edge of the sunk cut (light from upper left): mask offset down-right minus the mask
    so, to = g.add(s, -0.05), g.add(t, 0.05)
    e1, _ = figure(so, to, kx, kd, False, gskin); e2, _ = figure(so, to, gx, -kd, True, gskin)
    sunkall = U(sh1, sh2); edge = g.mul(U(e1, e2), g.op('SUBTRACT', 1.0, sunkall))
    # caption glyph column between the heads + a cartouche above the king (yellow ring, red fill)
    gx0 = W * 0.50
    gc = g.op('DIVIDE', g.op('SUBTRACT', t, 4.45), 0.36); gq = g.op('FRACT', gc); gr = g.white(g.op('FLOOR', gc), 3.1 + idx)
    glyph = g.mul(g.mul(g.band(t, 4.45, H - 0.95), g.op('LESS_THAN', g.op('ABSOLUTE', g.op('SUBTRACT', s, gx0)), 0.17)), g.band(gq, 0.16, 0.84))
    glc = g.mix(g.op('LESS_THAN', gr, 0.33), g.mix(g.op('LESS_THAN', gr, 0.66), GRN, RED), BLUE)
    cart_o = E(s, t, kx + kd * 0.55, H - 1.55, 0.17, 0.42); cart_i = E(s, t, kx + kd * 0.55, H - 1.55, 0.11, 0.35)
    # frame + sky band
    inner = g.mul(g.band(s, 0.30, W - 0.30), g.band(t, 0.30, H - 0.30))
    frame_y = g.mul(g.band(s, 0.08, W - 0.08), g.band(t, 0.10, H - 0.10))
    sky = g.mul(inner, g.op('GREATER_THAN', t, H - 0.70))
    star = g.mul(sky, g.op('LESS_THAN', g.op('ABSOLUTE', g.op('SUBTRACT', g.op('FRACT', g.op('DIVIDE', s, 0.5)), 0.5)), 0.12))
    ground = g.mul(inner, g.band(t, 0.30, 0.48))
    c = g.mix(g.op('SUBTRACT', 1.0, frame_y), base, BLUE)
    c = g.mix(g.mul(frame_y, g.op('SUBTRACT', 1.0, inner)), c, YEL)
    c = g.mix(sky, c, BLUE); c = g.mix(g.mul(star, g.band(g.op('FRACT', g.op('DIVIDE', t, 0.3)), 0.3, 0.7)), c, YEL)
    c = g.mix(ground, c, RED)
    c = g.mix(g.mul(inner, edge), c, (0.36, 0.27, 0.17))
    c = g.mix(g.mul(inner, sh1), c, c1); c = g.mix(g.mul(inner, sh2), c, c2); c = g.mix(glyph, c, glc)
    c = g.mix(cart_o, c, YEL); c = g.mix(cart_i, c, RED)
    sunk = g.mul(inner, U(sh1, sh2, glyph, cart_o))
    h = g.op('SUBTRACT', 1.0, g.add(g.mul(sunk, 0.8), g.mul(g.op('SUBTRACT', 1.0, inner), 0.25)))
    g.finish(c, h, 1.0, 0.012); return m

M_DISC = mat('cp038v2_winged_globe_red', (0.72, 0.16, 0.06), 0.45)
M_WB = mat('cp038v2_winged_globe_wing_blue', (0.22, 0.40, 0.70), 0.6)
M_WR = mat('cp038v2_winged_globe_wing_red', (0.72, 0.26, 0.12), 0.6)
M_WG = mat('cp038v2_winged_globe_wing_green', (0.24, 0.54, 0.36), 0.6)
M_WY = mat('cp038v2_winged_globe_gilt_yellow', (0.95, 0.74, 0.28), 0.45)

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
new_obj('cp038v2_axial_walk_flags', bm, M_WALK)
INFO['walk_ft'] = (10.0, round(FACE - 0.05 - 61.2, 2))

# 2. coloured sunk-relief panels on the six portico screen walls (face y 110.71 ft, wall 0..7.5 ft): larger than v1
#    (v1: 1.4 ft side inset, z 0.9..7.5, figures 4.15 ft; v2: 1.25 ft inset, z 0.45..7.40, figures ~5.4 ft)
np_ = 0; PZ0, PZ1, PIN = 0.45, 7.40, 1.25
for i in range(len(KX) - 1):
    if i == 3: continue
    x0, x1 = KX[i] + PIN, KX[i + 1] - PIN; W, H = x1 - x0, PZ1 - PZ0
    bm = bmesh.new()
    vs = [bm.verts.new((f(a), 0.0, f(c))) for a, c in ((0, 0), (W, 0), (W, H), (0, H))]
    bm.faces.new(vs)
    o = new_obj('cp038v2_portico_relief_panel_%d' % i, bm, relief_mat(W, H, i), origin=(f(x0), f(FACE - 0.03), f(PZ0)))
    np_ += 1
INFO['relief_panels'] = np_; INFO['relief_panel_ft'] = (round(W, 2), round(H, 2)); INFO['figure_h_ft'] = round(4.15 * K, 2)

# 3. winged sun disc with two uraei on the architrave over the open centre bay (z 17.6..19.4): v1 span 9.8 ft -> v2 ~14 ft
bmd = bmesh.new(); bmw = {k: bmesh.new() for k in 'BRGY'}
yD = ARCH - 0.06; zc = 18.56; S = 1.30
Mw = Matrix.Translation((f(AX), f(yD), f(zc))) @ Matrix.Scale(F, 4)
ell(bmd, Mw, (0, -0.10, 0), (0.62 * S, 0.18, 0.62 * S), 28, 12)          # sun disc
for sd in (-1, 1):
    for tier, (key, z0_, z1_, x1_) in enumerate((('Y', 0.40, 0.62, 5.6), ('B', 0.10, 0.40, 6.9), ('R', -0.22, 0.10, 6.3), ('G', -0.62, -0.22, 5.0))):
        bmx = bmw[key]; x0_ = 0.62 * S - 0.05
        quad = [(x0_, z0_ * S), (x1_, z0_ * S - 0.12), (x1_, z1_ * S - 0.11), (x0_, z1_ * S)]
        vs = [bmx.verts.new(Mw @ Vector((sd * xq, -0.05 - 0.02 * tier, zq))) for xq, zq in quad]
        bmx.faces.new(vs if sd > 0 else vs[::-1])
        for k in range(1, int(x1_ / 0.55)):                                 # feather divisions (thin dark-gilt strips)
            xk = x0_ + k * 0.55
            if xk > x1_ - 0.1: break
            r = (xk - x0_) / (x1_ - x0_)
            zb = z0_ * S - 0.12 * r; zt = z1_ * S - 0.11 * r
            vs = [bmw['Y'].verts.new(Mw @ Vector((sd * xq, -0.13 - 0.02 * tier, zq))) for xq, zq in ((xk, zb), (xk + 0.05, zb), (xk + 0.05, zt), (xk, zt))]
            bmw['Y'].faces.new(vs if sd > 0 else vs[::-1])
    ell(bmw['Y'], Mw, (sd * 0.60 * S, -0.16, -0.55 * S), (0.14 * S, 0.10, 0.18 * S), 10, 8)   # uraeus body
    ell(bmw['Y'], Mw, (sd * 0.60 * S, -0.18, -0.30 * S), (0.17 * S, 0.10, 0.12 * S), 10, 6)   # hood
new_obj('cp038v2_winged_disc', bmd, M_DISC, smooth=True)
for key, mm in (('B', M_WB), ('R', M_WR), ('G', M_WG), ('Y', M_WY)):
    new_obj('cp038v2_winged_disc_wings_' + key, bmw[key], mm, smooth=False)
INFO['winged_disc_span_ft'] = 2 * 6.9; INFO['disc_d_ft'] = round(2 * 0.62 * S, 2)

# 4. a few 1850s visitors (people_lib v3.4), off the panels, not in the foreground
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
NE_ = (0.6, 0.8); NW_ = (-0.6, 0.8)
G = [(239.2, 105.0, '1850s_gentleman', 'walking', N_), (240.7, 105.6, '1850s_lady', 'walking', N_),   # couple walking into the centre bay
     (252.3, 104.5, '1850s_gentleman', 'pointing', NW_),                                               # in line with column 5 (projected), pointing at panel 4
     (231.0, 104.5, '1850s_lady', 'standing', NE_)]                                                    # in line with column 2 (projected), looking at panel 2
nearest = 1e9
for n, (x, y, role, pose, face) in enumerate(G):
    d = math.hypot(x - camx, y - camy) * F
    put('cp038v2_visitor_%02d' % n, role, pose, x, y, face, 1854390 + n * 13, 'hero' if d < 12 else 'mid')
    nearest = min(nearest, d)
INFO['people_lib_visitors'] = len(people); INFO['nearest_new_figure_m'] = round(nearest, 2)

for o in col.objects: o['cp_state'] = STATE
print('CP038 BUILT', INFO)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP038 SAVED', OUT)
