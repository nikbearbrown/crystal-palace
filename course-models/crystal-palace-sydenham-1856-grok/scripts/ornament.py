# r10 ornament: procedural relief materials (shader displacement = bump from a procedural height field) and small
# geometry helpers for the Alhambra and Egyptian courts. exec'd inside build.py namespace (mat, socket, f, F, MB, bmesh,
# Matrix, Vector, math). Patterns are generic Nasrid / Egyptian vocabulary, NOT traced from a specific panel (grade I/U,
# see DEPARTURES r10).
import random

class NG:
    """tiny node-graph helper: op() for Math nodes, ss() smoothstep 0..1, mix() for colours"""
    def __init__(s, m):
        s.nt = m.node_tree; s.n = s.nt.nodes; s.l = s.nt.links; s.b = s.n['Principled BSDF']
        tc = s.n.new('ShaderNodeTexCoord'); s.tc = tc
        sp = s.n.new('ShaderNodeSeparateXYZ'); s.l.new(tc.outputs['Object'], sp.inputs[0]); s.sp = sp
    def _in(s, sock, v):
        if isinstance(v, (int, float)): sock.default_value = v
        else: s.l.new(v, sock)
    def op(s, o, a, b=None):
        m = s.n.new('ShaderNodeMath'); m.operation = o; s._in(m.inputs[0], a)
        if b is not None: s._in(m.inputs[1], b)
        return m.outputs[0]
    def ss(s, x, e0, e1):
        r = s.n.new('ShaderNodeMapRange'); r.interpolation_type = 'SMOOTHSTEP'; s._in(r.inputs[0], x)
        r.inputs[1].default_value = e0; r.inputs[2].default_value = e1; r.inputs[3].default_value = 0.0; r.inputs[4].default_value = 1.0
        return r.outputs[0]
    def inv(s, x): return s.op('SUBTRACT', 1.0, x)
    def mul(s, a, b): return s.op('MULTIPLY', a, b)
    def add(s, a, b): return s.op('ADD', a, b)
    def band(s, x, lo, hi): return s.mul(s.op('GREATER_THAN', x, lo), s.op('LESS_THAN', x, hi))
    def mix(s, fac, a, b):
        mx = s.n.new('ShaderNodeMix'); mx.data_type = 'RGBA'; s._in(socket(mx, 'Factor_Float'), fac)
        for ident, v in (('A_Color', a), ('B_Color', b)):
            if isinstance(v, tuple): socket(mx, ident).default_value = (*v, 1)
            else: s.l.new(v, socket(mx, ident))
        return socket(mx, 'Result_Color', True)
    def vec(s, x, y, z=0.0):
        c = s.n.new('ShaderNodeCombineXYZ'); s._in(c.inputs[0], x); s._in(c.inputs[1], y); s._in(c.inputs[2], z); return c.outputs[0]
    def white(s, x, y):
        w = s.n.new('ShaderNodeTexWhiteNoise'); w.noise_dimensions = '3D'; s.l.new(s.vec(x, y, 0.37), w.inputs['Vector']); return w.outputs['Value']
    def noise(s, scale, detail=2.0):
        nz = s.n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = detail
        s.l.new(s.tc.outputs['Object'], nz.inputs['Vector']); return nz.outputs['Fac']
    def finish(s, col, height, strength=0.8, dist_m=0.012):
        s.l.new(col, s.b.inputs['Base Color'])
        bp = s.n.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = strength; bp.inputs['Distance'].default_value = dist_m
        s.l.new(height, bp.inputs['Height']); s.l.new(bp.outputs['Normal'], s.b.inputs['Normal'])
    def uv(s):   # walls are axis-aligned: u = x + y runs along either wall direction, v = z
        return s.add(s.sp.outputs['X'], s.sp.outputs['Y']), s.sp.outputs['Z']
    def star(s, pu, pv, off, r):
        """8-point star (union of square + 45deg square) distance-ish field in a unit cell; returns (field, |qu|, |qv|)"""
        qu = s.op('SUBTRACT', s.op('FRACT', s.add(pu, off)), 0.5); qv = s.op('SUBTRACT', s.op('FRACT', s.add(pv, off)), 0.5)
        au, av = s.op('ABSOLUTE', qu), s.op('ABSOLUTE', qv)
        st = s.op('MINIMUM', s.op('MAXIMUM', au, av), s.mul(s.add(au, av), 0.7071))
        return st, au, av
    def ring(s, field, r, w):   # 1 on a band |field-r|<w
        return s.inv(s.ss(s.op('ABSOLUTE', s.op('SUBTRACT', field, r)), w*0.45, w))

# ---------------- Alhambra ----------------
def al_relief_mat(name, S=0.42, tint=0.32, ground=(0.70, 0.60, 0.45)):
    """carved & painted stucco (yeseria): interlaced 8-point star lattice (sebka/taraceа vocabulary) with a fine
    ataurique-like ridge fill, relief by bump; paint muted (engraving 0108 reads near-monochrome, OJ colour kept faint)"""
    m = mat(name, ground, 0.7); g = NG(m); u, v = g.uv()
    pu, pv = g.op('DIVIDE', u, S), g.op('DIVIDE', v, S)
    st1, au, av = g.star(pu, pv, 0.0, 0.30); st2, _, _ = g.star(pu, pv, 0.5, 0.16)
    l1 = g.ring(st1, 0.30, 0.045); l2 = g.ring(st2, 0.16, 0.035)
    diag = g.ring(g.op('ABSOLUTE', g.op('SUBTRACT', au, av)), 0.0, 0.03)     # straight interlace strands between stars
    diag = g.mul(diag, g.op('GREATER_THAN', st1, 0.31))
    lines = g.op('MAXIMUM', g.op('MAXIMUM', l1, l2), diag)
    i1 = g.op('LESS_THAN', st1, 0.285); i2 = g.op('LESS_THAN', st2, 0.145)
    # fine fill: nested small stars (1/3 scale) + swirling scroll ridges (wave rings, distorted) = dense carved ground
    fu3, fv3 = g.mul(pu, 3.0), g.mul(pv, 3.0); st3, _, _ = g.star(fu3, fv3, 0.0, 0.3)
    wv = g.n.new('ShaderNodeTexWave'); wv.wave_type = 'RINGS'; wv.inputs['Scale'].default_value = 1.0/(S*0.9)
    wv.inputs['Distortion'].default_value = 6.0; wv.inputs['Detail'].default_value = 2.0
    g.l.new(g.tc.outputs['Object'], wv.inputs['Vector'])
    scroll = g.ss(wv.outputs['Fac'], 0.55, 0.8)
    fine = g.op('MAXIMUM', g.mul(g.ring(st3, 0.3, 0.07), 0.8), g.mul(scroll, 0.7))
    h = g.add(lines, g.mul(fine, 0.35))
    # inscription band just above the dado (z 4.6-5.5 ft): fine scroll only, gold-ochre ground
    bandm = g.band(v, f(4.6), f(5.5)); bline = g.op('MAXIMUM', g.ring(v, f(4.62), 0.012), g.ring(v, f(5.48), 0.012))
    hb = g.add(g.mul(fine, 0.9), bline)
    h = g.add(g.mul(h, g.inv(bandm)), g.mul(hb, bandm))
    c = g.mix(g.mul(i1, tint), ground, (0.33, 0.38, 0.47))       # faded blue grounds
    c = g.mix(g.mul(i2, tint), c, (0.55, 0.32, 0.25))            # faded red grounds
    c = g.mix(g.mul(fine, 0.25), c, (0.80, 0.72, 0.56))
    c = g.mix(lines, c, (0.86, 0.80, 0.66))                      # raised strands: ivory stucco
    c = g.mix(bandm, c, g.mix(fine, (0.58, 0.47, 0.30), (0.82, 0.72, 0.52)))
    grime = g.noise(1.5, 3.0); c = g.mix(g.mul(g.ss(grime, 0.4, 0.75), 0.25), c, (0.45, 0.40, 0.33))
    g.finish(c, h, 0.9, 0.014); return m

def zellige_mat(name, S=0.30, dado_top_ft=4.5):
    """alicatado tile dado: star tiles in cells, cell colour from a per-cell hash, white ground, grout relief,
    black/white chequer border under the dado cap (I: generic Alhambra dado vocabulary)"""
    m = mat(name, (0.84, 0.82, 0.75), 0.22); g = NG(m); u, v = g.uv()
    pu, pv = g.op('DIVIDE', u, S), g.op('DIVIDE', v, S)
    st, au, av = g.star(pu, pv, 0.0, 0.32)
    tile = g.op('LESS_THAN', st, 0.31)
    grout = g.op('MAXIMUM', g.ring(st, 0.315, 0.018), g.inv(g.ss(g.op('SUBTRACT', 0.5, g.op('MAXIMUM', au, av)), 0.006, 0.014)))
    r = g.white(g.op('FLOOR', pu), g.op('FLOOR', pv))
    rp = g.n.new('ShaderNodeValToRGB'); cr = rp.color_ramp; cr.interpolation = 'CONSTANT'
    pal = [(0.0, (0.17, 0.32, 0.22)), (0.3, (0.07, 0.07, 0.08)), (0.5, (0.60, 0.45, 0.20)), (0.75, (0.16, 0.25, 0.40))]
    cr.elements[0].position, cr.elements[0].color = pal[0][0], (*pal[0][1], 1); cr.elements[1].position, cr.elements[1].color = pal[1][0], (*pal[1][1], 1)
    for p_, c_ in pal[2:]: e = cr.elements.new(p_); e.color = (*c_, 1)
    g.l.new(r, rp.inputs[0])
    c = g.mix(tile, (0.84, 0.82, 0.75), rp.outputs[0])
    c = g.mix(grout, c, (0.36, 0.34, 0.31))
    bd = g.band(v, f(dado_top_ft - 0.55), f(dado_top_ft - 0.08))
    ck = g.n.new('ShaderNodeTexChecker'); ck.inputs['Scale'].default_value = 1.0
    g.l.new(g.vec(g.op('DIVIDE', u, 0.045), g.op('DIVIDE', v, 0.045), 0.0), ck.inputs['Vector'])
    ck.inputs['Color1'].default_value = (0.08, 0.08, 0.09, 1); ck.inputs['Color2'].default_value = (0.85, 0.83, 0.76, 1)
    c = g.mix(bd, c, ck.outputs['Color'])
    g.finish(c, g.inv(grout), 0.5, 0.004); return m

def foliage_mat(name, c1=(0.05, 0.13, 0.04), c2=(0.16, 0.26, 0.08)):
    m = mat(name, c1, 0.7); g = NG(m)
    rp = g.n.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = (*c1, 1); rp.color_ramp.elements[1].color = (*c2, 1)
    g.l.new(g.noise(9.0, 4.0), rp.inputs[0])
    g.finish(rp.outputs[0], g.noise(40.0, 2.0), 0.9, 0.02); return m

# ---------------- Egypt ----------------
def eg_relief_mat(name, warm=(0.80, 0.64, 0.44)):
    """painted sunk relief: dado / figure register / hieroglyph columns / horizontal text line / banded frieze.
    Zones by height (ft) on any wall; figures and glyph shapes are generic stand-ins, not readable texts (U)."""
    m = mat(name, warm, 0.75); g = NG(m); u, v = g.uv()
    nz = g.noise(2.0, 3.0)
    base = g.mix(nz, (0.70, 0.54, 0.36), (0.84, 0.69, 0.48))
    BLUE, RED, GRN, YEL, BLK = (0.16, 0.27, 0.45), (0.55, 0.20, 0.12), (0.22, 0.40, 0.30), (0.80, 0.62, 0.26), (0.12, 0.10, 0.09)
    def glyphs(z0, Wc, Hc):
        cu = g.op('DIVIDE', u, Wc); cv = g.op('DIVIDE', g.op('SUBTRACT', v, z0), Hc)
        qu = g.op('SUBTRACT', g.op('FRACT', cu), 0.5); qv = g.op('SUBTRACT', g.op('FRACT', cv), 0.5)
        r = g.white(g.op('FLOOR', cu), g.op('FLOOR', cv))
        rad = g.op('SQRT', g.add(g.mul(qu, qu), g.mul(qv, qv)))
        circ = g.op('LESS_THAN', rad, 0.26)
        hbar = g.mul(g.op('LESS_THAN', g.op('ABSOLUTE', qv), 0.09), g.op('LESS_THAN', g.op('ABSOLUTE', qu), 0.36))
        e = g.add(g.mul(g.op('DIVIDE', qu, 0.20), g.op('DIVIDE', qu, 0.20)), g.mul(g.op('DIVIDE', g.op('SUBTRACT', qv, -0.05), 0.33), g.op('DIVIDE', g.op('SUBTRACT', qv, -0.05), 0.33)))
        hd = g.op('SQRT', g.add(g.mul(g.op('SUBTRACT', qu, 0.12), g.op('SUBTRACT', qu, 0.12)), g.mul(g.op('SUBTRACT', qv, 0.30), g.op('SUBTRACT', qv, 0.30))))
        bird = g.op('MAXIMUM', g.op('LESS_THAN', e, 1.0), g.op('LESS_THAN', hd, 0.11))
        wave = g.op('SUBTRACT', qv, g.mul(g.op('SINE', g.mul(qu, 28.0)), 0.07))
        zig = g.mul(g.op('LESS_THAN', g.op('ABSOLUTE', wave), 0.05), g.op('LESS_THAN', g.op('ABSOLUTE', qu), 0.38))
        s1 = g.op('LESS_THAN', r, 0.28); s2 = g.mul(g.op('GREATER_THAN', r, 0.28), g.op('LESS_THAN', r, 0.55))
        s3 = g.mul(g.op('GREATER_THAN', r, 0.55), g.op('LESS_THAN', r, 0.80)); s4 = g.op('GREATER_THAN', r, 0.80)
        mk = g.add(g.add(g.mul(circ, s1), g.mul(hbar, s2)), g.add(g.mul(bird, s3), g.mul(zig, s4)))
        div = g.op('GREATER_THAN', g.op('ABSOLUTE', qu), 0.46)
        colr = g.mix(g.op('LESS_THAN', g.op('FRACT', g.mul(r, 3.7)), 0.5), g.mix(g.op('LESS_THAN', g.op('FRACT', g.mul(r, 7.3)), 0.5), GRN, RED), BLUE)
        return mk, div, colr
    # zone masks
    z_dado = g.op('LESS_THAN', v, f(2.6)); z_fig = g.band(v, f(2.6), f(9.2)); z_b1 = g.band(v, f(9.2), f(9.55))
    z_col = g.band(v, f(9.55), f(13.0)); z_b2 = g.band(v, f(13.0), f(13.35)); z_line = g.band(v, f(13.35), f(14.9)); z_fr = g.band(v, f(14.9), f(17.2))
    # figures (sunk relief): cells 2.4 ft wide
    W = f(2.4); fu = g.op('DIVIDE', u, W); qu = g.op('SUBTRACT', g.op('FRACT', fu), 0.5)
    t = g.op('DIVIDE', g.op('SUBTRACT', v, f(2.6)), f(6.6))
    def ell(cx, cy, rx, ry):
        a = g.op('DIVIDE', g.op('SUBTRACT', qu, cx), rx); b = g.op('DIVIDE', g.op('SUBTRACT', t, cy), ry)
        return g.op('LESS_THAN', g.add(g.mul(a, a), g.mul(b, b)), 1.0)
    torso = ell(0.0, 0.58, 0.13, 0.20); kilt = g.mul(g.band(t, 0.26, 0.42), g.op('LESS_THAN', g.op('ABSOLUTE', qu), g.add(0.10, g.mul(g.op('SUBTRACT', 0.42, t), 0.35))))
    legs = g.mul(g.band(t, 0.04, 0.27), g.op('LESS_THAN', g.op('ABSOLUTE', g.op('SUBTRACT', g.op('ABSOLUTE', qu), 0.045)), 0.03))
    head = ell(0.0, 0.85, 0.075, 0.07); wig = ell(-0.02, 0.86, 0.09, 0.085)
    staff = g.mul(g.band(t, 0.04, 0.97), g.op('LESS_THAN', g.op('ABSOLUTE', g.op('SUBTRACT', qu, 0.21)), 0.012))
    arm = g.mul(g.band(t, 0.66, 0.70), g.band(qu, 0.0, 0.21))
    fig = g.op('MINIMUM', g.add(g.add(g.add(torso, kilt), g.add(legs, head)), g.add(g.add(staff, arm), wig)), 1.0)
    figc = g.mix(kilt, g.mix(torso, (0.66, 0.34, 0.20), (0.62, 0.30, 0.17)), (0.86, 0.82, 0.70))
    figc = g.mix(wig, figc, (0.12, 0.13, 0.20)); figc = g.mix(head, figc, (0.62, 0.30, 0.17)); figc = g.mix(staff, figc, YEL)
    gm1, gd1, gc1 = glyphs(f(9.55), f(0.62), f(0.55)); gm2, gd2, gc2 = glyphs(f(13.35), f(0.78), f(0.78))
    st = g.op('FRACT', g.op('DIVIDE', u, f(0.9)))
    frp = g.n.new('ShaderNodeValToRGB'); cr = frp.color_ramp; cr.interpolation = 'CONSTANT'
    cr.elements[0].position, cr.elements[0].color = 0.0, (*BLUE, 1); cr.elements[1].position, cr.elements[1].color = 0.22, (*warm, 1)
    for p_, c_ in ((0.33, RED), (0.55, warm), (0.66, GRN), (0.88, warm)): e = cr.elements.new(p_); e.color = (*c_, 1)
    g.l.new(st, frp.inputs[0])
    frg = g.ring(g.op('FRACT', g.mul(st, 3.0)), 0.0, 0.08)
    c = g.mix(z_dado, base, g.mix(g.band(v, f(2.35), f(2.6)), (0.42, 0.17, 0.10), BLK))
    c = g.mix(g.mul(z_fig, fig), c, figc)
    c = g.mix(z_b1, c, g.mix(g.band(v, f(9.3), f(9.45)), BLUE, YEL))
    c = g.mix(g.mul(z_col, gm1), c, gc1); c = g.mix(g.mul(z_col, gd1), c, BLUE)
    c = g.mix(z_b2, c, YEL)
    c = g.mix(g.mul(z_line, gm2), c, gc2)
    c = g.mix(z_fr, c, frp.outputs[0])
    # height: sunk relief (figure/glyph surfaces 0.6 below wall face, carved outline groove via the step), frieze grooves
    h = g.inv(g.add(g.mul(g.mul(z_fig, fig), 0.7), g.add(g.mul(g.mul(z_col, g.op('MAXIMUM', gm1, gd1)), 0.6), g.mul(g.mul(z_line, gm2), 0.6))))
    h = g.op('SUBTRACT', h, g.add(g.mul(z_fr, frg), g.mul(g.add(z_b1, z_b2), 0.25)))
    h = g.add(h, g.mul(nz, 0.15))
    g.finish(c, h, 0.8, 0.010); return m

def eg_stone_mat(name, warm=(0.80, 0.64, 0.44)):
    m = mat(name, warm, 0.8); g = NG(m); nz = g.noise(3.0, 4.0)
    g.finish(g.mix(nz, (0.70, 0.54, 0.36), (0.85, 0.70, 0.49)), g.noise(18.0, 3.0), 0.5, 0.01); return m

# ---------------- geometry helpers ----------------
def ico(mb, x, y, z, r, sub=1):
    bmesh.ops.create_icosphere(mb.bm, subdivisions=sub, radius=f(r), matrix=Matrix.Translation(Vector((f(x), f(y), f(z)))))
def blob(mb, x, y, z, r, rng, n=5, spread=0.8, sub=1):
    for _ in range(n):
        ico(mb, x + rng.uniform(-spread, spread)*r, y + rng.uniform(-spread, spread)*r, z + rng.uniform(-0.5, 0.5)*r, r*rng.uniform(0.55, 0.95), sub)
def frustum(mb, top_c, bot_c, t, n, w_top, d_top, w_bot, d_bot):
    """generic oriented frustum: top/bottom centres (feet Vectors), t/n unit vectors spanning the faces"""
    def qd(c, w, d): return [c + t*(sx*w/2) + n*(sy*d/2) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    A = qd(top_c, w_top, d_top); B = qd(bot_c, w_bot, d_bot)
    for k in range(4):
        mb.poly([tuple(A[k]), tuple(A[(k+1) % 4]), tuple(B[(k+1) % 4]), tuple(B[k])])
    mb.poly([tuple(p) for p in reversed(B)])
