# r08 fine-arts courts for SY-EARLY (exec'd inside build.py namespace: MB, mat, coll, root, cam, EYE, f, M, math, bmesh...).
# Walkable *limited* sets per storyboard CP038 (Egyptian) and CP041 (Alhambra): ground floor only, entered from the nave.
# Plan sources: guide 1856 p.47 'Ground Plan of Egyptian Court' (gallery 0226) and p.67 'Ground Plan of the Alhambra'
# (0246), placed by the overall plan 0205. Evidence grades are logged in DEPARTURES.md (D-R08-*).

from mathutils.geometry import tessellate_polygon
# ---------------- shared helpers ----------------
def ramp_mat(name, coord_axis, scale_ft, stops, rough=0.6, mode='z', interp='CONSTANT'):
    """procedural painted banding: colour = ramp(world-ish coordinate / scale). mode 'z' = horizontal bands by height;
    'xy' = vertical stripes along x+y (for cornice leaf stripes); stops = [(pos, rgb)]"""
    m = mat(name, stops[0][1], rough); nt = m.node_tree; n = nt.nodes; l = nt.links; b = n['Principled BSDF']
    tc = n.new('ShaderNodeTexCoord'); sep = n.new('ShaderNodeSeparateXYZ'); l.new(tc.outputs['Object'], sep.inputs[0])
    if mode == 'z':
        val = sep.outputs['Z']
    else:
        add = n.new('ShaderNodeMath'); add.operation = 'ADD'; l.new(sep.outputs['X'], add.inputs[0]); l.new(sep.outputs['Y'], add.inputs[1]); val = add.outputs[0]
    dv = n.new('ShaderNodeMath'); dv.operation = 'DIVIDE'; dv.inputs[1].default_value = f(scale_ft); l.new(val, dv.inputs[0])
    if mode != 'z':
        fr = n.new('ShaderNodeMath'); fr.operation = 'FRACT'; l.new(dv.outputs[0], fr.inputs[0]); src = fr.outputs[0]
    else:
        src = dv.outputs[0]
    ramp = n.new('ShaderNodeValToRGB'); cr = ramp.color_ramp; cr.interpolation = interp
    cr.elements[0].position = stops[0][0]; cr.elements[0].color = (*stops[0][1], 1)
    cr.elements[1].position = stops[1][0]; cr.elements[1].color = (*stops[1][1], 1)
    for pos, col in stops[2:]:
        e = cr.elements.new(pos); e.color = (*col, 1)
    l.new(src, ramp.inputs[0]); l.new(ramp.outputs[0], b.inputs['Base Color']); return m

def pattern_mat(name, cols, scale=1.0, kind='diaper', rough=0.55):
    """two crossed wave-band masks (diagonal diaper / lozenge) mixing 3 colours on a ground (Owen Jones Alhambra scheme)"""
    m = mat(name, cols[0], rough); nt = m.node_tree; n = nt.nodes; l = nt.links; b = n['Principled BSDF']
    tc = n.new('ShaderNodeTexCoord'); mp = n.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale, scale, scale)
    l.new(tc.outputs['Object'], mp.inputs[0])
    if kind == 'checker':
        ch = n.new('ShaderNodeTexChecker'); ch.inputs['Scale'].default_value = 1.0
        ch.inputs['Color1'].default_value = (*cols[1], 1); ch.inputs['Color2'].default_value = (*cols[2], 1); l.new(mp.outputs[0], ch.inputs['Vector'])
        ch2 = n.new('ShaderNodeTexChecker'); ch2.inputs['Scale'].default_value = 0.5
        ch2.inputs['Color1'].default_value = (*cols[3], 1); ch2.inputs['Color2'].default_value = (*cols[0], 1); l.new(mp.outputs[0], ch2.inputs['Vector'])
        mx = n.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs['Factor'].default_value = 0.5
        l.new(ch.outputs['Color'], mx.inputs[6]); l.new(ch2.outputs['Color'], mx.inputs[7]); l.new(mx.outputs[2], b.inputs['Base Color']); return m
    w1 = n.new('ShaderNodeTexWave'); w1.bands_direction = 'DIAGONAL'; w1.inputs['Scale'].default_value = 1.0
    w2 = n.new('ShaderNodeTexWave'); w2.bands_direction = 'DIAGONAL'; w2.inputs['Scale'].default_value = 1.0
    rot = n.new('ShaderNodeMapping'); rot.inputs['Scale'].default_value = (scale, scale, -scale)   # x+y-z vs x+y+z -> lozenges on every wall
    l.new(tc.outputs['Object'], rot.inputs[0]); l.new(mp.outputs[0], w1.inputs['Vector']); l.new(rot.outputs[0], w2.inputs['Vector'])
    mul = n.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; l.new(w1.outputs['Fac'], mul.inputs[0]); l.new(w2.outputs['Fac'], mul.inputs[1])
    ramp = n.new('ShaderNodeValToRGB'); cr = ramp.color_ramp; cr.interpolation = 'CONSTANT'
    cr.elements[0].position = 0.0; cr.elements[0].color = (*cols[0], 1)
    cr.elements[1].position = 0.18; cr.elements[1].color = (*cols[1], 1)
    e = cr.elements.new(0.40); e.color = (*cols[2], 1)
    e = cr.elements.new(0.62); e.color = (*cols[3], 1)
    l.new(mul.outputs[0], ramp.inputs[0]); l.new(ramp.outputs[0], b.inputs['Base Color']); return m

# =====================================================================================================================
# EGYPTIAN COURT  (plan 0226; placed x 180-276 (CT side -> north), y 60 (nave front) -> 184 (Museum annex beyond the
# Parade wall at 156). Plan px of the 679-wide guide page: x = 180 + (px-118)/3.875, y = 60 + (800-py)/3.875.)
# Heights: guide plan gives none; elements held under the 22.17 ft first-tier roof/girders of the outer aisle band (I).
# =====================================================================================================================
EGC = coll('SY56_court_egyptian_0226__dated')
ex = lambda px: 180 + (px - 118) / 3.875
ey = lambda py: 60 + (800 - py) / 3.875
# Owen Jones / Bonomi Egyptian palette: blue, red, yellow, green on sandstone (colour layout I, exact hues U)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ornament.py')).read())
# r10: warmer sandstone, softer (less saturated) paint, relief by bump (ornament.py)
EG_SAND = (0.80, 0.64, 0.44); EG_BLUE = (0.16, 0.27, 0.45); EG_RED = (0.55, 0.20, 0.12); EG_YEL = (0.80, 0.62, 0.28); EG_GRN = (0.22, 0.40, 0.30)
def add_bump(m, scale=14.0, strength=0.35):
    g = NG(m); bp = g.n.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = strength; bp.inputs['Distance'].default_value = 0.01
    g.l.new(g.noise(scale, 4.0), bp.inputs['Height']); g.l.new(bp.outputs['Normal'], g.b.inputs['Normal']); return m
m_eg_wall = eg_relief_mat('eg_wall_relief_hieroglyph_r10', EG_SAND)
m_eg_col = ramp_mat('eg_column_banded_OJ', 'z', 1.0, [(0.0, EG_SAND), (f(1.2), EG_RED), (f(1.8), EG_SAND), (f(9.5), EG_BLUE), (f(10.1), EG_YEL), (f(10.7), EG_RED), (f(11.3), EG_GRN), (f(11.9), EG_SAND)], mode='z'); add_bump(m_eg_col)
m_eg_cap = ramp_mat('eg_capital_papyrus_OJ', 'xy', 1.6, [(0.0, EG_GRN), (0.33, EG_BLUE), (0.5, EG_GRN), (0.83, EG_RED)], mode='xy')
m_eg_corn = ramp_mat('eg_cornice_leaf_OJ', 'xy', 1.2, [(0.0, EG_BLUE), (0.25, EG_SAND), (0.33, EG_RED), (0.58, EG_SAND), (0.66, EG_GRN), (0.92, EG_SAND)], mode='xy')
m_eg_arch = ramp_mat('eg_architrave_OJ', 'z', 1.0, [(0.0, EG_BLUE), (f(17.6), EG_YEL), (f(18.1), EG_BLUE), (f(19.4), EG_YEL)], mode='z')
m_eg_floor = eg_stone_mat('eg_floor_flags_r10', (0.66, 0.56, 0.42))
m_eg_stat = mat('eg_statue_granite', (0.32, 0.27, 0.24), 0.6)
EW = MB('eg_walls', EGC, m_eg_wall); ECOL = MB('eg_columns', EGC, m_eg_col); ECAP = MB('eg_capitals', EGC, m_eg_cap)
ECOR = MB('eg_cornices', EGC, m_eg_corn); EARC = MB('eg_architraves', EGC, m_eg_arch); EFL = MB('eg_floor', EGC, m_eg_floor)
EST = MB('eg_statues', EGC, m_eg_stat); EROOF = MB('eg_annex_roof', EGC, M['stone'])
EG_TOP = 20.0      # wall top below cornice (I)
def eg_wall(x0, x1, y0, y1, top=EG_TOP, t=2.0):
    if abs(x1-x0) < 0.01: x0, x1 = x0-t/2, x0+t/2
    if abs(y1-y0) < 0.01: y0, y1 = y0-t/2, y0+t/2
    EW.box(x0, x1, y0, y1, 0, top)
    # cavetto cornice: roll moulding + flared gorge (stepped boxes), leaf-striped
    xa, xb, ya, yb = min(x0,x1), max(x0,x1), min(y0,y1), max(y0,y1)
    ECOR.box(xa-0.2, xb+0.2, ya-0.2, yb+0.2, top, top+0.4)
    ECOR.box(xa-0.6, xb+0.6, ya-0.6, yb+0.6, top+0.4, top+1.0)
    ECOR.box(xa-1.0, xb+1.0, ya-1.0, yb+1.0, top+1.0, top+1.4)
def papyrus_col(x, y, h=15.5, r=1.7):
    ECOL.cyl(x, y, 0, 0.8, r+0.6, r+0.6, seg=20)                  # round base disc
    ECOL.cyl(x, y, 0.8, h, r, r*0.86, seg=20)                     # shaft (slight taper)
    ECAP.cyl(x, y, h, h+2.6, r*0.9, r*1.55, seg=20)               # open papyrus bell
    ECAP.cyl(x, y, h+2.6, h+3.0, r*1.55, r*1.55, seg=20)
    for k in range(16):   # r10: petal ribs on the open bell + sepal leaves at its foot (I)
        t = 2*math.pi*k/16; c_, s_ = math.cos(t), math.sin(t)
        ECOR.strut((x + c_*r*0.92, y + s_*r*0.92, h + 0.1), (x + c_*r*1.58, y + s_*r*1.58, h + 2.6), 0.16, 0.12)
        if k % 2 == 0:
            t2 = t + 2*math.pi/32
            ECOR.poly([(x + c_*r*0.9, y + s_*r*0.9, h - 0.05), (x + math.cos(t+2*math.pi/16)*r*0.9, y + math.sin(t+2*math.pi/16)*r*0.9, h - 0.05),
                       (x + math.cos(t2)*r*1.2, y + math.sin(t2)*r*1.2, h + 1.1)])
    EARC.box(x-r*0.9, x+r*0.9, y-r*0.9, y+r*0.9, h+3.0, h+3.6)    # abacus
    return h + 3.6
def lotus_col(x, y, h=14.0, r=1.2):
    """r10: lotus-bud (closed) column: bundled shaft of 8 stems, 5 binding bands, 8-lobed bud capital, abacus (I)"""
    ECOL.cyl(x, y, 0, 0.7, r+0.5, r+0.5, seg=20)
    ECOL.cyl(x, y, 0.7, h, r*0.72, r*0.66, seg=16)
    for k in range(8):
        t = 2*math.pi*(k+0.5)/8; ox, oy = math.cos(t), math.sin(t)
        ECOL.cyl(x + ox*r*0.62, y + oy*r*0.62, 0.7, 1.6, r*0.22, r*0.36, seg=8)          # stem foot (tapered in)
        ECOL.cyl(x + ox*r*0.62, y + oy*r*0.62, 1.6, h, r*0.36, r*0.31, seg=8)            # stem
        ECAP.cyl(x + ox*r*0.66, y + oy*r*0.66, h, h+1.3, r*0.32, r*0.46, seg=8)          # bud lobe swelling
        ECAP.cyl(x + ox*r*0.62, y + oy*r*0.62, h+1.3, h+2.4, r*0.46, r*0.14, seg=8)      # bud lobe closing
    for k in range(5): EARC.cyl(x, y, h-1.6+k*0.28, h-1.6+k*0.28+0.16, r*1.02, r*1.02, seg=20)   # binding bands
    ECAP.cyl(x, y, h, h+2.2, r*0.9, r*0.55, seg=16)
    EARC.box(x-r*0.75, x+r*0.75, y-r*0.75, y+r*0.75, h+2.4, h+3.0)
    return h + 3.0
def sq_pillar(x, y, s=4.0, h=17.6):
    ECOL.box(x-s/2, x+s/2, y-s/2, y+s/2, 0, h); EARC.box(x-s/2-0.3, x+s/2+0.3, y-s/2-0.3, y+s/2+0.3, h, h+0.5)
def seated_colossus(x, y, h, face=-1, mb=None):
    """seated figure massing (throne, legs, torso, nemes head); face = -1 faces -y, +1 faces +y, 'x-' faces -x"""
    mb = mb or EST; s = h / 20.0
    if face == 'x-':
        mb.box(x, x+6*s, y-3*s, y+3*s, 0, 9*s); mb.box(x-4*s, x, y-2.6*s, y+2.6*s, 0, 7.5*s)
        mb.box(x+0.5*s, x+4.5*s, y-2.4*s, y+2.4*s, 9*s, 15.5*s); mb.box(x+1*s, x+4*s, y-1.6*s, y+1.6*s, 15.5*s, 19*s); mb.box(x+1.6*s, x+3.6*s, y-1.0*s, y+1.0*s, 19*s, h); return
    d = face
    y_back = y - d*3*s
    mb.box(x-3*s, x+3*s, min(y_back, y_back+d*6*s), max(y_back, y_back+d*6*s), 0, 9*s)              # throne block
    mb.box(x-2.6*s, x+2.6*s, min(y+d*3*s, y+d*7*s), max(y+d*3*s, y+d*7*s), 0, 7.5*s)               # legs/knees
    mb.box(x-2.4*s, x+2.4*s, y-d*2.5*s - 2*s, y-d*2.5*s + 2*s, 9*s, 15.5*s)                        # torso
    mb.box(x-1.6*s, x+1.6*s, y-d*2.5*s - 1.5*s, y-d*2.5*s + 1.5*s, 15.5*s, 19*s)                   # nemes head
    mb.box(x-1.0*s, x+1.0*s, y-d*2.5*s - 1.0*s, y-d*2.5*s + 1.0*s, 19*s, h)                        # crown
EFL.box(180, 276, 60, 155, 0, 0.12); EFL.box(180, 248.4, 155, 184, 0, 0.12)
# --- Egyptian Museum (projects beyond the Parade wall) ---
eg_wall(180, 180, 60, 184)                                              # left (CT-side) wall along x=180, full depth
eg_wall(180, 248.4, 184, 184)                                           # annex back wall (Parade side)
eg_wall(248.4, 248.4, 155, 184)                                         # annex right wall
eg_wall(222.3, 222.3, 158, 184)                                         # Museum / Abu Simbel partition
eg_wall(180, ex(135), 154.5, 154.5); eg_wall(ex(270), 222.3, 154.5, 154.5)
for px in (147, 170, 193, 216, 239, 262): sq_pillar(ex(px), 154.5, 3.6)
EROOF.box(179, 249.4, 155.5, 185, EG_TOP+1.4, EG_TOP+2.2)               # annex roof (outside the glazed shell; I)
# --- Model of the Temple of Abu Simbel: 4 seated colossi against the back wall, low rail in front (U scale) ---
for k in range(4): seated_colossus(225.5 + k*6.6, 178.5, 9.0, face=-1)
EW.box(222.3, 248.4, 154.6, 155.4, 0, 3.0)
# --- inner court back + right walls ---
eg_wall(248.4, 276, 155, 155); eg_wall(276, 276, 60, 155)
# --- facade of the Hall of Columns (upper; 6 square pillars + T at px 237, wall stub to the right wall) ---
yHC = ey(515)
for px in (282, 315, 348, 380, 412, 445): sq_pillar(ex(px), yHC, 3.6)
eg_wall(ex(222), ex(255), yHC, yHC); eg_wall(ex(237), ex(237), ey(535), yHC)
eg_wall(ex(450), 276, yHC, yHC)
EARC.box(ex(282)-2.2, ex(445)+2.2, yHC-1.8, yHC+1.8, 17.6, 19.4); ECOR.box(ex(282)-2.6, ex(445)+2.6, yHC-2.2, yHC+2.2, 19.4, 20.6)
# --- Hall of Karnak columns: two rows of 8 papyrus columns + architraves ---
KX = [ex(px) for px in (248, 278, 310, 342, 373, 405, 436, 466)]
for py in (545, 575):
    yy = ey(py)
    for xx in KX: papyrus_col(xx, yy)
    EARC.box(KX[0]-1.6, KX[-1]+1.6, yy-1.4, yy+1.4, 19.1, 20.6)
for xx in KX: EARC.box(xx-1.2, xx+1.2, ey(575), ey(545), 19.1, 20.6)    # cross architraves (I)
# --- Tomb of Beni Hassan (rock-cut tomb front: side + back walls, 2 proto-Doric pillars inside, 2 at the front, roof) ---
tx0, tx1, ty0, ty1 = ex(150), ex(232), ey(585), ey(520)
eg_wall(tx0, tx0, ty0, ty1, top=14); eg_wall(tx1, tx1, ty0, ty1, top=14); eg_wall(tx0, tx1, ty1, ty1, top=14)
for px, py in ((160, 545), (218, 545), (160, 575), (218, 575)):
    ECOL.cyl(ex(px), ey(py), 0, 12.6, 1.3, 1.2, seg=16)                 # 16-sided 'proto-Doric' shafts (Beni Hassan type; I)
    EARC.box(ex(px)-1.4, ex(px)+1.4, ey(py)-1.4, ey(py)+1.4, 12.6, 13.2)
EROOF.box(tx0-1, tx1+1, ty0, ty1+1, 14, 15)
# --- statues of Amenoph (two seated colossi at the CT edge, facing the transept; scale U) ---
for py in (520, 560): seated_colossus(ex(105), ey(py), 16.0, face='x-')
# --- lower facade of the Hall of Columns: 8 columns with Ptolemaic screen walls, centre bay open (screen ht I) ---
yLF = ey(600)
eg_wall(180, ex(237), yLF, yLF)
for i, xx in enumerate(KX):
    lotus_col(xx, yLF, h=14.6, r=1.4)
    if i < len(KX)-1 and i != 3:
        EW.box(xx+1.4, KX[i+1]-1.4, yLF-0.9, yLF+0.9, 0, 7.5); ECOR.box(xx+1.4, KX[i+1]-1.4, yLF-1.4, yLF+1.4, 7.5, 8.3)
EARC.box(KX[0]-1.8, KX[-1]+1.8, yLF-1.5, yLF+1.5, 17.6, 19.4); ECOR.box(KX[0]-2.2, KX[-1]+2.2, yLF-2.0, yLF+2.0, 19.4, 20.6)
eg_wall(KX[-1]+1.8, 276, yLF, yLF)
for px in (160, 200): sq_pillar(ex(px), ey(620), 3.4, 15.0)
# --- Court of Amunothph (Amunsthph on the plan): 4 Osiride pillars on the left edge + left wall ---
for py in (665, 700, 728, 757):
    sq_pillar(183.6, ey(py), 5.6, 16.0)
    seated_colossus(183.6, ey(py)-3.2, 9.0, face=-1)   # standing Osiride figures read as massing only (U)
eg_wall(ex(237), ex(237), ey(720), ey(660))
# --- nave front (y=60): screen-wall segments, 3 narrow doorways (x 219.7-223.5, 238.6-242.4, 257.5-261.5 from 0226) ---
DOORS = [(219.7, 223.5), (238.6, 242.4), (257.5, 261.5)]
xa = 180.0
for d0, d1 in DOORS + [(276.0, 276.0)]:
    if d0 > xa: eg_wall(xa, d0, 60, 60, top=14.0)
    if d1 > d0:
        for xx in (d0 - 1.1, d1 + 1.1): lotus_col(xx, 58.2, h=15.1, r=1.1)
        EARC.box(d0-2.4, d1+2.4, 56.8, 59.6, 18.1, 19.4); ECOR.box(d0-2.8, d1+2.8, 56.4, 60.0, 19.4, 20.4)
    xa = d1
eg_wall(ex(237), ex(237), 60, ey(755), top=14.0)
for px in (165, 195): sq_pillar(ex(px), 62.6, 3.4, 12.0)
for mb_ in (EW, ECOL, ECAP, ECOR, EARC, EFL, EST, EROOF): mb_.done()

# =====================================================================================================================
# ALHAMBRA COURT  (plan 0246; court 25 on plan 0205 lies at x~486-560: placed x 492-564 so the end walls take the
# north-transept span columns (3 ft shift, I). Plan px of the 674-wide page: X = 492 + (px-70)/5.833, Y = 60 + (745-py)/5.833.)
# Heights: Sydenham court was a reduced-scale reproduction; columns 9 ft, arches to 14.5 ft, walls 24 ft (I).
# Colour: Owen Jones' Alhambra scheme of blue, red and gold on the upper stucco, tile mosaic dado (Jones, *Plans,
# Elevations ... of the Alhambra* / Grammar of Ornament - external to muse-drive, not checked here: I).
# =====================================================================================================================
ALC = coll('SY56_court_alhambra_0246__dated')
ax = lambda px: 492 + (px - 70) / 5.833
ay = lambda py: 60 + (745 - py) / 5.833
# r10: muted palette + relief materials (ornament.py). Engraving 0108 reads near-monochrome ivory stucco with darker
# recesses; OJ blue/red/gold kept as faded grounds only (I).
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ornament.py')).read())
m_al_stucco = al_relief_mat('al_stucco_relief_sebka_r10')
m_al_frame = mat('al_mouldings_ivory_r10', (0.76, 0.68, 0.54), 0.6); add_bump(m_al_frame, 30.0, 0.25)   # r10b: projected relief on thin side faces went black -> plain moulding
m_al_dado = zellige_mat('al_zellige_dado_r10')
m_al_marble = mat('al_marble_columns', (0.84, 0.82, 0.77), 0.28)
m_al_gold = mat('al_capitals_gilt_muted_r10', (0.62, 0.52, 0.34), 0.45, 0.25)
m_al_mq = al_relief_mat('al_muqarnas_r10', S=0.20, tint=0.45, ground=(0.72, 0.63, 0.48))
m_al_floor = pattern_mat('al_floor_marble', [(0.82, 0.80, 0.76), (0.62, 0.60, 0.58), (0.82, 0.80, 0.76), (0.70, 0.68, 0.64)], scale=0.9, kind='checker')
m_al_leaf = foliage_mat('al_foliage_r10'); m_al_vine = foliage_mat('al_vine_r10', (0.06, 0.15, 0.05), (0.22, 0.30, 0.10))
m_al_pot = mat('al_pots_terracotta', (0.50, 0.28, 0.17), 0.8)
AST = MB('al_stucco', ALC, m_al_stucco); ADA = MB('al_dado', ALC, m_al_dado); AMA = MB('al_columns', ALC, m_al_marble)
AGO = MB('al_capitals', ALC, m_al_gold); AFL = MB('al_floor', ALC, m_al_floor); AWA = MB('al_fountain_water', ALC, M['water'])
APL = MB('al_beds_planting', ALC, m_al_leaf); APA = MB('al_paths', ALC, m_al_floor); ALN = MB('al_lions', ALC, M['marble'])
AFR = MB('al_alfiz_frames_bands', ALC, m_al_frame); AMQ = MB('al_muqarnas', ALC, m_al_mq); AVN = MB('al_hanging_planting', ALC, m_al_vine)
APT = MB('al_pots', ALC, m_al_pot); ABED = MB('al_bed_soil', ALC, M['grass'])
RNG = random.Random(1856)
AL_WALL = 21.4 if POST66 else 24.0; DADO = 4.5; SPR = 10.4; CROWN = 16.2; ATOP = 19.5     # r10: stilted arches -> arcade top raised 17.5 -> 19.5 (I)
COL_H = 9.0; IMP = COL_H + 1.65                                           # impost top over the Nasrid capital
def al_wall(x0, x1, y0, y1, top=AL_WALL, t=1.6):
    if abs(x1-x0) < 0.01: x0, x1 = x0-t/2, x0+t/2
    if abs(y1-y0) < 0.01: y0, y1 = y0-t/2, y0+t/2
    ADA.box(x0-0.05, x1+0.05, y0-0.05, y1+0.05, 0, DADO); AST.box(x0, x1, y0, y1, DADO, top)
    AFR.box(x0-0.12, x1+0.12, y0-0.12, y1+0.12, DADO, DADO+0.25)              # dado cap moulding
    AFR.box(x0-0.08, x1+0.08, y0-0.08, y1+0.08, top-1.4, top-0.4)             # upper inscription band, proud
    AGO.box(x0-0.3, x1+0.3, y0-0.3, y1+0.3, top, top+0.6)                     # eaves moulding (I)
def al_col(x, y, h=COL_H, pair_axis=None, gap=0.38):
    """r10: slender marble shaft (dia 0.6 ft, ~1:15), small moulded base, astragal rings, Nasrid capital (cylindrical
    lower drum + cubic upper block) and impost (cimacio). pair_axis 'x'/'y' -> two shafts sharing one impost."""
    pts = [(x, y)] if pair_axis is None else ([(x-gap, y), (x+gap, y)] if pair_axis == 'x' else [(x, y-gap), (x, y+gap)])
    for (px_, py_) in pts:
        AMA.cyl(px_, py_, 0, 0.18, 0.42, 0.42, seg=16); AMA.cyl(px_, py_, 0.18, 0.38, 0.38, 0.31, seg=16)
        AMA.cyl(px_, py_, 0.38, h, 0.30, 0.27, seg=16)
        for zr in (h-0.55, h-0.35): AGO.cyl(px_, py_, zr, zr+0.09, 0.31, 0.31, seg=16)
        AGO.cyl(px_, py_, h, h+0.55, 0.29, 0.34, seg=16)                       # drum with leaf band
        AGO.box(px_-0.42, px_+0.42, py_-0.42, py_+0.42, h+0.55, h+1.2)         # cubic block
    hx = 0.55 + (gap if pair_axis == 'x' else 0); hy = 0.55 + (gap if pair_axis == 'y' else 0)
    AFR.box(x-hx, x+hx, y-hy, y+hy, h+1.2, IMP)                                 # impost block
def arch_profile(u0, u1, z_spr, z_crown, cusps=9, n=72, A=0.17):
    """r10: stilted cusped (lobed) arch intrados: round lobes separated by sharp inward cusps
    (r = R*(1 - A*(1-|sin(k t)|))); the r08 profile had the kink reversed and read as plain scallops"""
    R = (u1 - u0) / 2; uc = (u0 + u1) / 2; stilt = max(0.0, z_crown - z_spr - R)
    pts = []
    for i in range(n+1):
        t = math.pi * i / n
        lob = 1.0 - A * (1.0 - abs(math.sin(cusps * t)))
        pts.append((uc - R*math.cos(t)*lob, z_spr + stilt + (z_crown - z_spr - stilt)*math.sin(t)*lob))
    pts[0] = (u0, z_spr + stilt); pts[-1] = (u1, z_spr + stilt)
    return [(u0, IMP)] + pts + [(u1, IMP)], (uc, z_spr + stilt), R
def arch_screen(p0, p1, col_us, z_spr=SPR+1.6, z_crown=CROWN, top=ATOP, depth=2.0, mb=None, hw=None, muq=False, alfiz=False):
    """arcade panel over columns between p0 and p1 (plan ft); col_us = column positions along the line; hw = per-column
    half-width of the pier/impost (paired columns wider). Spandrels as vertical quad strips, soffit quads, optional
    muqarnas fringe (radial stalactite cells in 2 staggered tiers x 3 rows) and alfiz frame (rectangular moulding)."""
    mb = mb or AST; (xa, ya), (xb, yb) = p0, p1; L = math.hypot(xb-xa, yb-ya); ux, uy = (xb-xa)/L, (yb-ya)/L; nx, ny = -uy, ux
    hw = hw or [0.55]*len(col_us)
    P = lambda u, z, s: (xa + ux*u + nx*s*depth/2, ya + uy*u + ny*s*depth/2, z)
    Q = lambda u, z, sd: Vector((xa + ux*u + nx*sd, ya + uy*u + ny*sd, z))
    for i, (u0, u1) in enumerate(zip(col_us[:-1], col_us[1:])):
        a0, a1 = u0 + hw[i], u1 - hw[i+1]
        prof, (ucc, zc), R = arch_profile(a0, a1, z_spr, z_crown)
        # r10b: spandrel faces as one tessellated outline per side. The cusped profile backtracks in u, so the r08 vertical
        # strips overlapped coplanar with flipped winding -> black shadow-acne slits in the CP041 insert.
        outl = [(u0, top), (u0, IMP)] + prof + [(u1, IMP), (u1, top)]
        ol = []
        for pt in outl:
            if not ol or abs(pt[0]-ol[-1][0]) + abs(pt[1]-ol[-1][1]) > 1e-4: ol.append(pt)
        tris = tessellate_polygon([[Vector((u_, z_, 0.0)) for u_, z_ in ol]])
        for s in (-1, 1):
            for tri in tris:
                q = [P(ol[k][0], ol[k][1], s) for k in tri]
                nrm = (Vector(q[1]) - Vector(q[0])).cross(Vector(q[2]) - Vector(q[0]))
                if nrm.length < 1e-9: continue
                if nrm.dot(Vector((nx*s, ny*s, 0))) < 0: q = q[::-1]
                mb.poly(q)
        for (ua, za), (ub, zb) in zip(prof[:-1], prof[1:]):
            mb.poly([P(ua, za, -1), P(ub, zb, -1), P(ub, zb, 1), P(ua, za, 1)])
        if muq:
            curve = prof[1:-1]; n_ = len(curve)
            for tier, (step, hfac, wfac) in enumerate(((3, 1.0, 1.25), (3, 0.6, 0.9))):
                for j in range(1 + tier, n_ - 1, step):
                    (ua, za) = curve[j]
                    if za < z_spr + 0.4: continue
                    cvec = Vector((ucc - ua, zc - za)); 
                    if cvec.length < 1e-3: continue
                    rd = cvec.normalized(); tg = Vector((rd.y, -rd.x))
                    ds = math.hypot(curve[j+1][0]-curve[j-1][0], curve[j+1][1]-curve[j-1][1]) * 1.5 * wfac
                    hcell = (0.55 + 0.30 * ((j * 7) % 3) / 2) * hfac * (R / 4.5 + 0.4)
                    for row, sd in enumerate((-depth/3, 0.0, depth/3)):
                        sh = 0.5 * ds * ((row + tier) % 2) * 0.5
                        top_u, top_z = ua + tg.x*sh - rd.x*0.05, za + tg.y*sh - rd.y*0.05
                        bot_u, bot_z = top_u + rd.x*hcell, top_z + rd.y*hcell
                        T = Vector((ux*tg.x, uy*tg.x, tg.y)); N = Vector((nx, ny, 0))
                        frustum(AMQ, Q(top_u, top_z, sd), Q(bot_u, bot_z, sd), T, N, ds, depth/3*0.98, ds*0.28, depth/3*0.3)
        if alfiz:
            for s in (-1, 1):
                sd = s*(depth/2 + 0.08)
                for (ua_, ub_, za_, zb_) in ((a0-0.6, a0-0.35, IMP, z_crown+0.7), (a1+0.35, a1+0.6, IMP, z_crown+0.7), (a0-0.6, a1+0.6, z_crown+0.45, z_crown+0.7)):
                    p_a, p_b = Q(ua_, za_, sd - s*0.08), Q(ub_, zb_, sd + s*0.08)
                    AFR.box(min(p_a.x, p_b.x)/1, max(p_a.x, p_b.x), min(p_a.y, p_b.y), max(p_a.y, p_b.y), za_, zb_)
    x0_, x1_ = min(xa, xb) - abs(nx)*depth/2, max(xa, xb) + abs(nx)*depth/2; y0_, y1_ = min(ya, yb) - abs(ny)*depth/2, max(ya, yb) + abs(ny)*depth/2
    AFR.box(x0_-0.08, x1_+0.08, y0_-0.08, y1_+0.08, top-1.3, top-0.5)          # inscription band (proud)
    AGO.box(x0_-0.2, x1_+0.2, y0_-0.2, y1_+0.2, top, top+0.5)
def hang(x0, x1, y0, y1, z, dens=0.55, drop=3.0):
    """r10 planting overhang: foliage clumps along an arcade top with trailing strands (0108 shows creepers over the
    arcade and potted plants; species U)"""
    L = max(abs(x1-x0), abs(y1-y0)); n = max(2, int(L * dens))
    for k in range(n):
        t = (k + RNG.uniform(0.1, 0.9)) / n; x = x0 + (x1-x0)*t; y = y0 + (y1-y0)*t
        blob(AVN, x, y, z + 0.4, RNG.uniform(0.6, 1.0), RNG, n=4, sub=2)
        if RNG.random() < 0.45:     # trailing tress: tapering leafy clumps, not a bead chain
            zz = z; dz = RNG.uniform(0.5, 1.0) * drop; rr = 0.55
            while zz > z - dz and rr > 0.12:   # r10 guard: geometric series alone cannot reach dz
                zz -= max(rr, 0.3) * 0.8; blob(AVN, x + RNG.uniform(-0.2, 0.2), y + RNG.uniform(-0.2, 0.2), zz, rr, RNG, n=2, spread=0.5, sub=2); rr *= 0.85
def vine(x, y, z0, z1, r=0.38):
    n = int((z1 - z0) / 0.35)
    for k in range(n):
        t = k * 1.7; ico(AVN, x + r*math.cos(t), y + r*math.sin(t), z0 + k*0.35, RNG.uniform(0.14, 0.24), 1)
def pot_plant(x, y, h=4.0, palm=False):
    APT.cyl(x, y, 0.12, 1.6, 0.7, 0.95, seg=12)
    if palm:
        AMA.cyl(x, y, 1.6, h, 0.12, 0.1, seg=6)
        for k in range(9):
            t = 2*math.pi*k/9; AVN.strut((x, y, h), (x + 2.2*math.cos(t), y + 2.2*math.sin(t), h - 0.9), 0.5, 0.05)
    else:
        blob(APL, x, y, 1.6 + h*0.35, h*0.32, RNG, n=6, spread=0.6)
AFL.box(492, 564, 60, 153.5, 0, 0.12)
# --- outer walls (Cast Room / Abencerrages / Divans block at the back, side walls) ---
al_wall(ax(70), ax(487), ay(203), ay(203))                                         # back wall
al_wall(ax(75), ax(75), ay(380), ay(203)); al_wall(ax(484), ax(484), ay(380), ay(203))
al_wall(ax(186), ax(186), ay(255), ay(207)); al_wall(ax(186), ax(186), ay(333), ay(300))   # Cast Room partition + door
al_wall(ax(375), ax(375), ay(330), ay(207))                                        # Divans partition (doorway I below)
ADA.box(ax(375)-0.8, ax(375)+0.8, ay(300), ay(240), 0, 0.1)
# Hall of the Abencerrages fountain (12-sided basin) and Divans dome-ring on piers (dome itself not modelled: miss)
fx, fy = ax(280), ay(275)
AMA.cyl(fx, fy, 0, 1.6, 4.3, 4.3, seg=12); AWA.cyl(fx, fy, 1.6, 1.62, 3.9, 3.9, seg=12); AMA.cyl(fx, fy, 1.6, 3.6, 0.5, 0.5, seg=8); AMA.cyl(fx, fy, 3.6, 4.1, 1.6, 1.0, seg=12)
for px in (213, 347): al_col(ax(px), ay(275))
dcx, dcy, dr = ax(415), ay(272), 35 / 5.833
for k in range(8):
    t = 2*math.pi*k/8; al_col(dcx + dr*math.cos(t), dcy + dr*math.sin(t))
for k in range(32):
    t0, t1 = 2*math.pi*k/32, 2*math.pi*(k+1)/32
    AST.poly([(dcx+dr*1.1*math.cos(t0), dcy+dr*1.1*math.sin(t0), SPR+1.6), (dcx+dr*1.1*math.cos(t1), dcy+dr*1.1*math.sin(t1), SPR+1.6),
              (dcx+dr*1.1*math.cos(t1), dcy+dr*1.1*math.sin(t1), ATOP+2), (dcx+dr*1.1*math.cos(t0), dcy+dr*1.1*math.sin(t0), ATOP+2)])
# --- pier row A (py ~339): L ends, cross piers, slender columns; arch screens between ---
def pier(px0, px1, py0, py1):
    x0, x1, y0, y1 = ax(px0), ax(px1), ay(py1), ay(py0); ADA.box(x0, x1, y0, y1, 0, DADO); AST.box(x0, x1, y0, y1, DADO, AL_WALL)
yA, yB = ay(339), ay(471)
pier(70, 118, 333, 345); pier(70, 82, 333, 380); pier(175, 253, 333, 345); pier(207, 220, 320, 380)
pier(308, 388, 333, 345); pier(341, 354, 320, 380); pier(440, 490, 333, 345); pier(478, 490, 333, 380)
for px in (130, 158, 395, 425): al_col(ax(px), yA)
arch_screen((ax(118), yA), (ax(175), yA), [0, ax(130)-ax(118), ax(158)-ax(118), ax(175)-ax(118)])
arch_screen((ax(388), yA), (ax(440), yA), [0, ax(395)-ax(388), ax(425)-ax(388), ax(440)-ax(388)])
arch_screen((ax(253), yA), (ax(308), yA), [0, ax(308)-ax(253)], z_spr=SPR+3, z_crown=CROWN+3, top=ATOP+3, muq=True, alfiz=True)
# --- Hall of Justice ceiling (flat, coffered stalactite vaults not modelled: miss) ---
AST.box(ax(70), ax(490), yB, yA, AL_WALL, AL_WALL+1.2)
AST.box(ax(70), ax(490), yA, ay(203), AL_WALL, AL_WALL+1.2)
AST.box(ax(70), ax(490), ay(518), yB, ATOP, ATOP+0.8)          # r08b: arcade-walk ceiling between Lions colonnade and pier row B (I)
# --- pier row B (py ~471): T piers + columns ---
pier(70, 118, 465, 478); pier(70, 82, 432, 512); pier(175, 253, 465, 478); pier(207, 220, 432, 465)
pier(308, 388, 465, 478); pier(343, 356, 432, 465); pier(440, 490, 465, 478); pier(478, 490, 432, 512)
for px in (130, 158, 395, 425): al_col(ax(px), yB)
arch_screen((ax(118), yB), (ax(175), yB), [0, ax(130)-ax(118), ax(158)-ax(118), ax(175)-ax(118)])
arch_screen((ax(388), yB), (ax(440), yB), [0, ax(395)-ax(388), ax(425)-ax(388), ax(440)-ax(388)])
arch_screen((ax(253), yB), (ax(308), yB), [0, ax(308)-ax(253)], z_spr=SPR+3, z_crown=CROWN+3, top=ATOP+3, muq=True, alfiz=True)
# --- Court of the Lions: colonnade on the rectangle px 112-448 x py 518-694, arcades above, 4 beds, cross paths ---
cx0, cx1, cy0, cy1 = ax(112), ax(448), ay(694), ay(518)        # cy0 = nave side, cy1 = Hall of Justice side
NB = 12
xs_c = [cx0 + (cx1-cx0)*i/NB for i in range(NB+1)]; ys_c = [cy0 + (cy1-cy0)*i/7 for i in range(8)]
# r10: single and paired slender shafts (0108 shows coupled columns; rhythm I): pairs at corners and every 3rd column
PX = [i % 3 == 0 for i in range(NB+1)]; PY = [i in (0, 3, 4, 7) for i in range(8)]
for i, xx in enumerate(xs_c):
    for yy in (cy0, cy1): al_col(xx, yy, pair_axis='x' if PX[i] else None)
for j, yy in enumerate(ys_c):
    for xx in (cx0, cx1):
        if 0 < j < 7: al_col(xx, yy, pair_axis='y' if PY[j] else None)
        else: al_col(xx, yy + (0.76 if j == 0 else -0.76), pair_axis=None)     # corner cluster: third shaft on the short side
HWX = [0.55 + (0.38 if p_ else 0) for p_ in PX]; HWY = [0.55 + (0.38 if p_ else 0) for p_ in PY]; HWY[0] = HWY[-1] = 1.3
arch_screen((cx0, cy0), (cx1, cy0), [x_-cx0 for x_ in xs_c], hw=HWX); arch_screen((cx0, cy1), (cx1, cy1), [x_-cx0 for x_ in xs_c], hw=HWX)
arch_screen((cx0, cy0), (cx0, cy1), [y_-cy0 for y_ in ys_c], hw=HWY); arch_screen((cx1, cy0), (cx1, cy1), [y_-cy0 for y_ in ys_c], hw=HWY)
# r10 planting overhang over the inner arcade tops + creepers on some shafts
for (p_a, p_b) in (((cx0, cy0+1.3), (cx1, cy0+1.3)), ((cx0, cy1-1.3), (cx1, cy1-1.3)), ((cx0+1.2, cy0), (cx0+1.2, cy1)), ((cx1-1.2, cy0), (cx1-1.2, cy1))):
    hang(p_a[0], p_b[0], p_a[1], p_b[1], ATOP + 0.5)
for i in (1, 4, 8, 11):
    vine(xs_c[i], cy0, 0.4, COL_H + 1.0); vine(xs_c[i], cy1, 0.4, COL_H + 1.0)
# corridor roofs over the colonnade walks (between arcade and outer walls; flat, I)
AST.box(ax(70), cx0, cy0-6, cy1, ATOP, ATOP+0.8); AST.box(cx1, ax(490), cy0-6, cy1, ATOP, ATOP+0.8)
AST.box(ax(70), ax(490), ay(745), cy0, ATOP, ATOP+0.8)
# beds (sunken, planted; cut corners towards the octagon) and cross paths with round ends
ocx, ocy = ax(282), ay(605)
for sx in (-1, 1):
    for sy in (-1, 1):
        xa_, xb_ = sorted((ocx + sx*(17.5/5.833 + 0.5), ocx + sx*((440-282)/5.833 - 0.5)))
        ya_, yb_ = sorted((ocy + sy*(7/5.833 + 0.6), ocy + sy*((605-520)/5.833 - 0.5)))
        ABED.box(xa_, xb_, ya_, yb_, -0.6, 0.5)
        for k in range(22): blob(APL, xa_ + 0.6 + (k*7.3) % (xb_-xa_-1.2), ya_ + 0.6 + (k*3.1) % (yb_-ya_-1.2), 1.0 + 0.5*(k % 4), 0.6 + 0.25*(k % 4), RNG, n=6, spread=0.9, sub=2)
        pot_plant(ocx + sx*((440-282)/5.833 - 3.0), ocy + sy*((605-520)/5.833 - 3.0), 9.0, palm=True)
APA.box(ocx - 7.5/5.833*1.0, ocx + 7.5/5.833*1.0, cy0, cy1, 0.12, 0.2); APA.box(ax(95), ax(465), ocy-1.2, ocy+1.2, 0.12, 0.2)
for px in (100, 460):
    AMA.cyl(ax(px), ocy, 0, 0.9, 1.6, 1.6, seg=16); AWA.cyl(ax(px), ocy, 0.9, 0.92, 1.3, 1.3, seg=16)
AJ = MB('al_lions_jet', ALC, M['jet'])
# Fountain of the Lions: octagonal surround, 12-sided basin, 12 lions carrying the bowl, upper bowl
APA.cyl(ocx, ocy, 0.12, 0.3, 45/5.833, 45/5.833, seg=8)
AMA.cyl(ocx, ocy, 0, 1.4, 28/5.833, 28/5.833, seg=12); AWA.cyl(ocx, ocy, 1.4, 1.42, 28/5.833-0.4, 28/5.833-0.4, seg=12)
for k in range(12):   # r10: 12 lions facing outward, legs/haunches/maned head/muzzle; water from the mouths (B: 12 lions; form I)
    t = 2*math.pi*k/12; c_, s_ = math.cos(t), math.sin(t); lx, ly = ocx + 2.5*c_, ocy + 2.5*s_; z0 = 1.4
    P_ = lambda a, b, z: (lx + a*c_ - b*s_, ly + a*s_ + b*c_, z)     # a = outward, b = sideways (local lion frame)
    ALN.strut(P_(-0.75, 0, z0+1.05), P_(0.45, 0, z0+1.15), 0.62, 0.8)                     # body
    ALN.strut(P_(-0.80, 0, z0+0.85), P_(-0.55, 0, z0+1.30), 0.75, 0.9)                    # haunches
    for a_ in (-0.62, 0.35):
        for b_ in (-0.24, 0.24): ALN.strut(P_(a_, b_, z0), P_(a_ + 0.05, b_, z0+0.95), 0.2, 0.22)   # legs
    for a_, b_ in ((0.45, -0.25), (0.45, 0.25)): ALN.strut(P_(a_, b_, z0), P_(a_ + 0.18, b_, z0 + 0.12), 0.24, 0.26)  # paws
    ALN.strut(P_(0.35, 0, z0+1.05), P_(0.62, 0, z0+1.85), 0.78, 0.95)                     # mane block
    ALN.strut(P_(0.60, 0, z0+1.45), P_(0.98, 0, z0+1.38), 0.42, 0.40)                     # muzzle
    ALN.strut(P_(0.55, -0.22, z0+1.85), P_(0.55, -0.22, z0+2.0), 0.1, 0.12); ALN.strut(P_(0.55, 0.22, z0+1.85), P_(0.55, 0.22, z0+2.0), 0.1, 0.12)  # ears
    ALN.strut(P_(-0.85, 0, z0+0.95), P_(-0.95, 0.35, z0+0.25), 0.1, 0.1)                  # tail
    ALN.cyl(lx, ly, z0, z0+0.12, 1.0, 1.0, seg=8)                                          # plinth
    sp = [P_(1.0, 0, z0+1.36), P_(1.45, 0, z0+1.2), P_(1.8, 0, z0+0.7), P_(2.0, 0, z0+0.05)]
    for p_a, p_b in zip(sp[:-1], sp[1:]): AJ.strut(p_a, p_b, 0.07, 0.07)
ALN.cyl(ocx, ocy, 1.4, 3.0, 1.1, 0.9, seg=12)                                              # central drum the lions surround
AMA.cyl(ocx, ocy, 3.0, 3.6, 1.8, 2.7, seg=12); AMA.cyl(ocx, ocy, 3.6, 4.0, 2.75, 2.75, seg=12)                                     # main bowl (12-sided)
AWA.cyl(ocx, ocy, 3.95, 3.97, 2.45, 2.45, seg=12)
AMA.cyl(ocx, ocy, 4.0, 5.6, 0.4, 0.4, seg=8); AMA.cyl(ocx, ocy, 5.6, 6.0, 0.6, 1.3, seg=12); AMA.cyl(ocx, ocy, 6.0, 6.8, 0.3, 0.12, seg=8)
AJ.cyl(ocx, ocy, 6.8, 9.5, 0.25, 0.05, seg=8); AJ.done()
# side wall segments flanking the court (px 70-82 py 565-645) and front corners/walls to the nave
al_wall(ax(76), ax(76), ay(645), ay(565)); al_wall(ax(484), ax(484), ay(645), ay(565))
for (pa_, pb_) in ((70, 118), (175, 255), (310, 390), (442, 490)): al_wall(ax(pa_), ax(pb_), ay(739), ay(739), top=ATOP)
al_wall(ax(76), ax(76), ay(745), ay(700), top=ATOP); al_wall(ax(484), ax(484), ay(745), ay(700), top=ATOP)
al_wall(ax(76), ax(76), ay(512), ay(380)); al_wall(ax(484), ax(484), ay(512), ay(380))
for px in (130, 158, 395, 425): al_col(ax(px), ay(739))
arch_screen((ax(118), ay(739)), (ax(175), ay(739)), [0, ax(130)-ax(118), ax(158)-ax(118), ax(175)-ax(118)])
arch_screen((ax(390), ay(739)), (ax(442), ay(739)), [0, ax(395)-ax(390), ax(425)-ax(390), ax(442)-ax(390)])
# central entrance (px 255-310): taller horseshoe-cusped arch screen
arch_screen((ax(255), ay(739)), (ax(310), ay(739)), [0, ax(310)-ax(255)], z_spr=SPR+2, z_crown=CROWN+3.5, top=ATOP+3, depth=2.2, muq=True, alfiz=True)
bmesh.ops.remove_doubles(AST.bm, verts=AST.bm.verts, dist=0.0005)   # r08b: weld spandrel strips (crack leaks showed as black seams)
for px_, py_ in ((96, 560), (464, 560), (96, 650), (464, 650)): pot_plant(ax(px_), ay(py_), 4.5)
for mb_ in (AST, ADA, AMA, AGO, AFL, AWA, APL, APA, ALN, AFR, AMQ, AVN, APT, ABED):
    o_ = mb_.done()
    if mb_ in (APL, AVN, AMA, ALN, APT):   # smooth-shade organic + turned pieces
        for pg in o_.data.polygons: pg.use_smooth = True

# ---------------- court cameras (36 mm sensor, 1.6 m eye, no roll) ----------------
def anim_cam(name, p0, p1, look, lens, f0=1, f1=120):
    o = cam(name, p1, look, lens)
    o.location = [f(v) for v in p0]; o.keyframe_insert('location', frame=f0)
    o.location = [f(v) for v in p1]; o.keyframe_insert('location', frame=f1); return o
DX = 6.0 / F   # 6 m move
xd = (DOORS[1][0] + DOORS[1][1]) / 2
# r10: frame 1 moved back 4 ft (y 44 -> 40, 20 ft off the screen wall) so it opens on the whole lotus portal + relief walls,
# not on the jambs; the 6 m push ends on the threshold (y 59.7) looking into the Hall of Columns (I)
anim_cam('CAM_CP038_egyptian_entry_28mm', (xd, 40.0, EYE), (xd, 40.0 + DX, EYE), (xd, 130, EYE + 6.5), 28)
cam('CAM_CP038_egyptian_hold_28mm', (xd, 49.0 + DX, EYE), (xd - 4, 130, EYE + 5.5), 28)
xa_ = (ax(255) + ax(310)) / 2
anim_cam('CAM_CP041_alhambra_entry_28mm', (xa_, 52.0, EYE), (xa_, 52.0 + DX, EYE), (xa_, 150, EYE + 3.0), 28)
cam('CAM_CP041_alhambra_hold_28mm', (xa_, 52.0 + DX, EYE), (xa_, 150, EYE + 3.0), 28)
cam('CAM_CP041_insert_spandrel_50mm', (xa_ - 6, cy0 + 22, EYE), (cx0 + (cx1-cx0)*0.25, cy0, 12.5), 50)
cam('CAM_compare_0108_alhambra', (ax(302), yB + 17.0, EYE), (ocx - 3.0, ocy, 9.6), 28)   # r10: 17 ft back inside the Hall of Justice so the row-B muqarnas arch frames the top, as in 0108; render portrait RES=1080x1350 (I)   # r08b: from the Hall of Justice through its central arch (row B), fountain left of centre (0108; I)

# =====================================================================================================================
# r09: Abu Simbel colossi pair (Muse, models/egyptian-court-colossi @ origin/main 90e62cc), appended unmodified.
# Guide 1856 p.50: "the gigantic figures in the northern transept" -> placed in the north transept (lost 1866 fire), at its
# garden (-Y) end, backs 2 ft off the recessed end wall, facing +Y up the transept toward the nave (end chosen: I;
# the Parade half of the transept bay is occupied by the plan-0205-traced Alhambra Court, x 492-564).
# =====================================================================================================================
_cpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vendor', 'muse-egyptian-court-colossi', 'egyptian-court-colossi.blend')
if os.path.exists(_cpath) and not POST66:   # POST66: transept gone; colossi no longer displayed (B/R: fire accounts; their later fate U)
    CLC = coll('SY56_north_transept_colossi_muse__lost1866', parent=C['SY_north_transept__lost1866'])
    with bpy.data.libraries.load(_cpath, link=False) as (src, dst):
        dst.objects = list(src.objects)
    croot = bpy.data.objects.new('colossi_root_muse', None); CLC.objects.link(croot)
    croot.location = (f(ST_X), f(-156 + RECESS + 2) + 5.85, 0.0); croot.rotation_euler = (0, 0, math.pi)
    for o in dst.objects:
        if o is None: continue
        CLC.objects.link(o)
        if o.parent is None: o.parent = croot
    # r10: headroom fix - camera back to y 58 (Alhambra front at 60), pitch 12.8 deg: crowns (86.5 ft) sit ~3 deg below frame top
    cam('CAM_north_transept_colossi_35mm', (ST_X - 6, 58, EYE), (ST_X, -140, 50.2), 35)
