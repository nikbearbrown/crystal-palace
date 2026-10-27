# r08 fine-arts courts for SY-EARLY (exec'd inside build.py namespace: MB, mat, coll, root, cam, EYE, f, M, math, bmesh...).
# Walkable *limited* sets per storyboard CP038 (Egyptian) and CP041 (Alhambra): ground floor only, entered from the nave.
# Plan sources: guide 1856 p.47 'Ground Plan of Egyptian Court' (gallery 0226) and p.67 'Ground Plan of the Alhambra'
# (0246), placed by the overall plan 0205. Evidence grades are logged in DEPARTURES.md (D-R08-*).

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
EG_SAND = (0.74, 0.60, 0.42); EG_BLUE = (0.07, 0.20, 0.52); EG_RED = (0.60, 0.12, 0.07); EG_YEL = (0.86, 0.66, 0.20); EG_GRN = (0.12, 0.40, 0.30)
m_eg_wall = ramp_mat('eg_wall_painted_OJ', 'z', 1.0, [(0.0, EG_RED), (f(2.8), EG_SAND), (f(15.0), EG_BLUE), (f(15.8), EG_YEL), (f(16.6), EG_RED), (f(17.2), EG_SAND)], mode='z')
m_eg_col = ramp_mat('eg_column_banded_OJ', 'z', 1.0, [(0.0, EG_SAND), (f(1.2), EG_RED), (f(1.8), EG_SAND), (f(9.5), EG_BLUE), (f(10.1), EG_YEL), (f(10.7), EG_RED), (f(11.3), EG_GRN), (f(11.9), EG_SAND)], mode='z')
m_eg_cap = ramp_mat('eg_capital_papyrus_OJ', 'xy', 1.6, [(0.0, EG_GRN), (0.33, EG_BLUE), (0.5, EG_GRN), (0.83, EG_RED)], mode='xy')
m_eg_corn = ramp_mat('eg_cornice_leaf_OJ', 'xy', 1.2, [(0.0, EG_BLUE), (0.25, EG_SAND), (0.33, EG_RED), (0.58, EG_SAND), (0.66, EG_GRN), (0.92, EG_SAND)], mode='xy')
m_eg_arch = ramp_mat('eg_architrave_OJ', 'z', 1.0, [(0.0, EG_BLUE), (f(17.6), EG_YEL), (f(18.1), EG_BLUE), (f(19.4), EG_YEL)], mode='z')
m_eg_floor = mat('eg_floor_flags', (0.62, 0.55, 0.45), 0.8)
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
    EARC.box(x-r*0.9, x+r*0.9, y-r*0.9, y+r*0.9, h+3.0, h+3.6)    # abacus
    return h + 3.6
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
    papyrus_col(xx, yLF, h=14.0, r=1.4)
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
        for xx in (d0 - 1.1, d1 + 1.1): papyrus_col(xx, 58.2, h=14.5, r=1.1)
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
AL_CREAM = (0.80, 0.72, 0.56); AL_RED = (0.58, 0.07, 0.05); AL_BLUE = (0.06, 0.14, 0.45); AL_GOLD = (0.80, 0.58, 0.18)
m_al_stucco = pattern_mat('al_stucco_diaper_OJ', [AL_CREAM, AL_GOLD, AL_RED, AL_BLUE], scale=4.5)
m_al_dado = pattern_mat('al_zellige_dado', [(0.85, 0.82, 0.74), (0.10, 0.32, 0.20), (0.10, 0.10, 0.12), (0.72, 0.52, 0.12)], scale=3.0, kind='checker')
m_al_marble = mat('al_marble_columns', (0.86, 0.84, 0.80), 0.3)
m_al_gold = mat('al_capitals_gilt', (0.78, 0.56, 0.20), 0.35, 0.6)
m_al_floor = pattern_mat('al_floor_marble', [(0.82, 0.80, 0.76), (0.62, 0.60, 0.58), (0.82, 0.80, 0.76), (0.70, 0.68, 0.64)], scale=0.9, kind='checker')
AST = MB('al_stucco', ALC, m_al_stucco); ADA = MB('al_dado', ALC, m_al_dado); AMA = MB('al_columns', ALC, m_al_marble)
AGO = MB('al_capitals', ALC, m_al_gold); AFL = MB('al_floor', ALC, m_al_floor); AWA = MB('al_fountain_water', ALC, M['water'])
APL = MB('al_beds_planting', ALC, M['foliage']); APA = MB('al_paths', ALC, m_al_floor); ALN = MB('al_lions', ALC, M['marble'])
AL_WALL = 24.0; DADO = 4.5; SPR = 11.0; CROWN = 14.5; ATOP = 17.5
def al_wall(x0, x1, y0, y1, top=AL_WALL, t=1.6):
    if abs(x1-x0) < 0.01: x0, x1 = x0-t/2, x0+t/2
    if abs(y1-y0) < 0.01: y0, y1 = y0-t/2, y0+t/2
    ADA.box(x0-0.05, x1+0.05, y0-0.05, y1+0.05, 0, DADO); AST.box(x0, x1, y0, y1, DADO, top)
    AGO.box(x0-0.3, x1+0.3, y0-0.3, y1+0.3, top, top+0.6)       # gilt eaves moulding (I)
def al_col(x, y, h=9.0):
    AMA.cyl(x, y, 0, 0.6, 0.75, 0.75, seg=12); AMA.cyl(x, y, 0.6, h, 0.42, 0.42, seg=12)
    for zr in (h*0.75, h*0.8): AGO.cyl(x, y, zr, zr+0.15, 0.5, 0.5, seg=12)   # shaft rings
    AGO.cyl(x, y, h, h+1.2, 0.48, 0.75, seg=12); AGO.box(x-0.85, x+0.85, y-0.85, y+0.85, h+1.2, h+1.6)  # capital + impost
def arch_profile(u0, u1, z_spr, z_crown, cusps=7, n=36):
    """stilted, cusped (lobed) arch intrados, returns [(u, z)] from u0 to u1"""
    R = (u1 - u0) / 2; uc = (u0 + u1) / 2; stilt = max(0.0, z_crown - z_spr - R)
    pts = [(u0, z_spr)]
    for i in range(n+1):
        t = math.pi * i / n
        lob = 1.0 - 0.10 * abs(math.sin(cusps * t))
        pts.append((uc - R*math.cos(t)*lob, z_spr + stilt + (z_crown - z_spr - stilt)*math.sin(t)*lob))
    pts.append((u1, z_spr)); return pts
def arch_screen(p0, p1, col_us, z_spr=SPR+1.6, z_crown=CROWN, top=ATOP, depth=1.4, mb=None):
    """arcade panel over columns between p0 and p1 (plan ft); col_us = column positions (distance along the line).
    Each bay = an ngon spandrel face (front/back) with a cusped stilted arch cut, plus soffit quads."""
    mb = mb or AST; (xa, ya), (xb, yb) = p0, p1; L = math.hypot(xb-xa, yb-ya); ux, uy = (xb-xa)/L, (yb-ya)/L; nx, ny = -uy, ux
    P = lambda u, z, s: (xa + ux*u + nx*s*depth/2, ya + uy*u + ny*s*depth/2, z)
    for u0, u1 in zip(col_us[:-1], col_us[1:]):
        a0, a1 = u0 + 0.55, u1 - 0.55
        prof = arch_profile(a0, a1, z_spr, z_crown)
        for s in (-1, 1):   # r08b: spandrel as vertical quad strips (no concave ngons -> no triangulation artefacts)
            strips = [((u0, z_spr), (a0, z_spr))] + list(zip(prof[:-1], prof[1:])) + [((a1, z_spr), (u1, z_spr))]
            for (ua, za), (ub, zb) in strips:
                q = [P(ua, za, s), P(ub, zb, s), P(ub, top, s), P(ua, top, s)]
                mb.poly(q if s > 0 else list(reversed(q)))
        for (ua, za), (ub, zb) in zip(prof[:-1], prof[1:]):
            mb.poly([P(ua, za, -1), P(ub, zb, -1), P(ub, zb, 1), P(ua, za, 1)])
    AGO.box(min(xa, xb) - abs(nx)*depth/2 - 0.2, max(xa, xb) + abs(nx)*depth/2 + 0.2, min(ya, yb) - abs(ny)*depth/2 - 0.2, max(ya, yb) + abs(ny)*depth/2 + 0.2, top, top+0.5)
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
arch_screen((ax(253), yA), (ax(308), yA), [0, ax(308)-ax(253)], z_spr=SPR+3, z_crown=CROWN+3, top=ATOP+3)
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
arch_screen((ax(253), yB), (ax(308), yB), [0, ax(308)-ax(253)], z_spr=SPR+3, z_crown=CROWN+3, top=ATOP+3)
# --- Court of the Lions: colonnade on the rectangle px 112-448 x py 518-694, arcades above, 4 beds, cross paths ---
cx0, cx1, cy0, cy1 = ax(112), ax(448), ay(694), ay(518)        # cy0 = nave side, cy1 = Hall of Justice side
NB = 12
xs_c = [cx0 + (cx1-cx0)*i/NB for i in range(NB+1)]; ys_c = [cy0 + (cy1-cy0)*i/7 for i in range(8)]
for xx in xs_c:
    for yy in (cy0, cy1): al_col(xx, yy)
for yy in ys_c[1:-1]:
    for xx in (cx0, cx1): al_col(xx, yy)
arch_screen((cx0, cy0), (cx1, cy0), [x_-cx0 for x_ in xs_c]); arch_screen((cx0, cy1), (cx1, cy1), [x_-cx0 for x_ in xs_c])
arch_screen((cx0, cy0), (cx0, cy1), [y_-cy0 for y_ in ys_c]); arch_screen((cx1, cy0), (cx1, cy1), [y_-cy0 for y_ in ys_c])
# corridor roofs over the colonnade walks (between arcade and outer walls; flat, I)
AST.box(ax(70), cx0, cy0-6, cy1, ATOP, ATOP+0.8); AST.box(cx1, ax(490), cy0-6, cy1, ATOP, ATOP+0.8)
AST.box(ax(70), ax(490), ay(745), cy0, ATOP, ATOP+0.8)
# beds (sunken, planted; cut corners towards the octagon) and cross paths with round ends
ocx, ocy = ax(282), ay(605)
for sx in (-1, 1):
    for sy in (-1, 1):
        xa_, xb_ = sorted((ocx + sx*(17.5/5.833 + 0.5), ocx + sx*((440-282)/5.833 - 0.5)))
        ya_, yb_ = sorted((ocy + sy*(7/5.833 + 0.6), ocy + sy*((605-520)/5.833 - 0.5)))
        APL.box(xa_, xb_, ya_, yb_, -0.6, 0.6)
        for k in range(14): APL.cyl(xa_ + (k*7.3) % (xb_-xa_), ya_ + (k*3.1) % (yb_-ya_), 0.6, 2.2 + (k % 3), 1.2, 0.3, seg=6)
APA.box(ocx - 7.5/5.833*1.0, ocx + 7.5/5.833*1.0, cy0, cy1, 0.12, 0.2); APA.box(ax(95), ax(465), ocy-1.2, ocy+1.2, 0.12, 0.2)
for px in (100, 460):
    AMA.cyl(ax(px), ocy, 0, 0.9, 1.6, 1.6, seg=16); AWA.cyl(ax(px), ocy, 0.9, 0.92, 1.3, 1.3, seg=16)
# Fountain of the Lions: octagonal surround, 12-sided basin, 12 lions carrying the bowl, upper bowl
APA.cyl(ocx, ocy, 0.12, 0.3, 45/5.833, 45/5.833, seg=8)
AMA.cyl(ocx, ocy, 0, 1.4, 28/5.833, 28/5.833, seg=12); AWA.cyl(ocx, ocy, 1.4, 1.42, 28/5.833-0.4, 28/5.833-0.4, seg=12)
for k in range(12):
    t = 2*math.pi*k/12; lx, ly = ocx + 2.6*math.cos(t), ocy + 2.6*math.sin(t)
    ALN.strut((lx - 0.55*math.cos(t), ly - 0.55*math.sin(t), 1.4+1.0), (lx + 0.55*math.cos(t), ly + 0.55*math.sin(t), 1.4+1.0), 0.75, 1.1)    # body
    ALN.cyl(lx + 0.75*math.cos(t), ly + 0.75*math.sin(t), 2.4, 3.6, 0.45, 0.4, seg=8)                                                  # head/mane
    ALN.cyl(lx, ly, 1.4, 1.9, 0.45, 0.45, seg=6)
AMA.cyl(ocx, ocy, 3.0, 3.6, 2.6, 3.4, seg=12); AMA.cyl(ocx, ocy, 3.6, 4.0, 3.5, 3.5, seg=12)                                     # main bowl (12-sided)
AWA.cyl(ocx, ocy, 3.95, 3.97, 3.2, 3.2, seg=12)
AMA.cyl(ocx, ocy, 4.0, 5.6, 0.4, 0.4, seg=8); AMA.cyl(ocx, ocy, 5.6, 6.0, 0.6, 1.3, seg=12); AMA.cyl(ocx, ocy, 6.0, 6.8, 0.3, 0.12, seg=8)
AJ = MB('al_lions_jet', ALC, M['jet']); AJ.cyl(ocx, ocy, 6.8, 9.5, 0.25, 0.05, seg=8); AJ.done()
# side wall segments flanking the court (px 70-82 py 565-645) and front corners/walls to the nave
al_wall(ax(76), ax(76), ay(645), ay(565)); al_wall(ax(484), ax(484), ay(645), ay(565))
for (pa_, pb_) in ((70, 118), (175, 255), (310, 390), (442, 490)): al_wall(ax(pa_), ax(pb_), ay(739), ay(739), top=ATOP)
al_wall(ax(76), ax(76), ay(745), ay(700), top=ATOP); al_wall(ax(484), ax(484), ay(745), ay(700), top=ATOP)
al_wall(ax(76), ax(76), ay(512), ay(380)); al_wall(ax(484), ax(484), ay(512), ay(380))
for px in (130, 158, 395, 425): al_col(ax(px), ay(739))
arch_screen((ax(118), ay(739)), (ax(175), ay(739)), [0, ax(130)-ax(118), ax(158)-ax(118), ax(175)-ax(118)])
arch_screen((ax(390), ay(739)), (ax(442), ay(739)), [0, ax(395)-ax(390), ax(425)-ax(390), ax(442)-ax(390)])
# central entrance (px 255-310): taller horseshoe-cusped arch screen
arch_screen((ax(255), ay(739)), (ax(310), ay(739)), [0, ax(310)-ax(255)], z_spr=SPR+2, z_crown=CROWN+3.5, top=ATOP+3, depth=1.8)
bmesh.ops.remove_doubles(AST.bm, verts=AST.bm.verts, dist=0.0005)   # r08b: weld spandrel strips (crack leaks showed as black seams)
for mb_ in (AST, ADA, AMA, AGO, AFL, AWA, APL, APA, ALN): mb_.done()

# ---------------- court cameras (36 mm sensor, 1.6 m eye, no roll) ----------------
def anim_cam(name, p0, p1, look, lens, f0=1, f1=120):
    o = cam(name, p1, look, lens)
    o.location = [f(v) for v in p0]; o.keyframe_insert('location', frame=f0)
    o.location = [f(v) for v in p1]; o.keyframe_insert('location', frame=f1); return o
DX = 6.0 / F   # 6 m move
xd = (DOORS[1][0] + DOORS[1][1]) / 2
anim_cam('CAM_CP038_egyptian_entry_28mm', (xd, 44.0, EYE), (xd, 44.0 + DX, EYE), (xd, 130, EYE + 5.5), 28)
cam('CAM_CP038_egyptian_hold_28mm', (xd, 49.0 + DX, EYE), (xd - 4, 130, EYE + 5.5), 28)
xa_ = (ax(255) + ax(310)) / 2
anim_cam('CAM_CP041_alhambra_entry_28mm', (xa_, 52.0, EYE), (xa_, 52.0 + DX, EYE), (xa_, 150, EYE + 3.0), 28)
cam('CAM_CP041_alhambra_hold_28mm', (xa_, 52.0 + DX, EYE), (xa_, 150, EYE + 3.0), 28)
cam('CAM_CP041_insert_spandrel_50mm', (xa_ - 6, cy0 + 22, EYE), (cx0 + (cx1-cx0)*0.25, cy0, 12.5), 50)
cam('CAM_compare_0108_alhambra', (ax(302), yB + 5.0, EYE), (ocx - 3.0, ocy, 6.5), 28)   # r08b: from the Hall of Justice through its central arch (row B), fountain left of centre (0108; I)
