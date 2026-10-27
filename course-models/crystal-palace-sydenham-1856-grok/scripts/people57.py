# r13 PPL-1850s: Victorian (c.1854-60) figure templates + Geometry-Nodes instancing (exec'd from build.py's namespace:
# f, mat, coll, root, sc ...). Units feet. Low-poly lathe figures in the manner of r12 dress36.py (itself adapted from the
# HP executor's figures.py person_mesh - read-only reference, no code imported), re-dressed for the 1850s:
#   men: frock coat to the knee, dark trousers, top hat (R: period photographs/prints, e.g. stereo 0057, print 0595);
#   women: dome-shaped crinoline skirt (fashion peak c.1856-60, R), mantle/shawl, close bonnet (R); colours U.
#   performers: chorus women in pale dress (U), chorus men in black with white shirt fronts (I), seated strings with
#   violin / cello, standing double basses, seated winds; conductor with raised baton (all I).
# Crowds are NOT merged meshes: a carrier mesh holds one vertex per person with attributes tmpl (template index),
# rot (euler) and scl, and a shared Geometry Nodes group instances the templates (Instance on Points, Pick Instance)
# -> thousands of people at a few MB. Template collection is excluded from the view layer (instances still render).
import bpy, bmesh, math, random
from mathutils import Vector, Matrix
FTM = 0.3048
def _pm(name, rgb, rough=0.7, metal=0.0):
    return bpy.data.materials.get(name) or mat(name, rgb, rough, metal)
PV = [_pm('pv57_black_cloth', (0.022, 0.021, 0.022), 0.8), _pm('pv57_dark_brown', (0.07, 0.045, 0.03), 0.85),
      _pm('pv57_dark_grey', (0.08, 0.08, 0.085), 0.85), _pm('pv57_navy', (0.02, 0.025, 0.06), 0.8),
      _pm('pv57_skin', (0.6, 0.42, 0.33), 0.6), _pm('pv57_white_linen', (0.78, 0.76, 0.7), 0.7),
      _pm('pv57_silk_green', (0.08, 0.17, 0.09), 0.45), _pm('pv57_silk_plum', (0.2, 0.05, 0.11), 0.45),
      _pm('pv57_silk_blue', (0.08, 0.12, 0.27), 0.45), _pm('pv57_silk_fawn', (0.38, 0.28, 0.17), 0.5),
      _pm('pv57_silk_grey', (0.26, 0.25, 0.25), 0.5), _pm('pv57_muslin_white', (0.85, 0.84, 0.8), 0.75),
      _pm('pv57_straw_bonnet', (0.55, 0.45, 0.28), 0.8), _pm('pv57_varnish_wood', (0.25, 0.1, 0.04), 0.35),
      _pm('pv57_paisley_shawl', (0.42, 0.12, 0.06), 0.8), _pm('pv57_brass', (0.62, 0.45, 0.16), 0.3, 1.0),
      # r14 additions (indices 16-23): scarlet, gold lace, moleskin, rust flannel, cream, boater straw, khaki-ish drab, pink silk
      _pm('pv57_scarlet', (0.42, 0.03, 0.025), 0.6), _pm('pv57_gold_lace', (0.7, 0.52, 0.18), 0.35, 1.0),
      _pm('pv57_moleskin', (0.2, 0.17, 0.12), 0.9), _pm('pv57_rust_flannel', (0.3, 0.1, 0.06), 0.9),
      _pm('pv57_cream', (0.7, 0.66, 0.55), 0.7), _pm('pv57_boater_straw', (0.66, 0.56, 0.36), 0.8),
      _pm('pv57_drab', (0.22, 0.2, 0.14), 0.85), _pm('pv57_pink_silk', (0.6, 0.38, 0.38), 0.45)]
(V_BLK, V_BRN, V_GRY, V_NAVY, V_SKIN, V_LIN, V_GRN, V_PLUM, V_BLUE, V_FAWN, V_SGRY, V_MUS, V_STRAW, V_WOOD, V_SHAWL,
 V_BRASS, V_SCAR, V_GOLD, V_MOLE, V_RUST, V_CREAM, V_BOAT, V_DRAB, V_PINK) = range(24)

def _lathe(bm, prof, seg, mi, cx=0.0, cy=0.0, sx=1.0, sy=1.0):
    rings = [[bm.verts.new((FTM*(cx + sx*r*math.cos(2*math.pi*k/seg)), FTM*(cy + sy*r*math.sin(2*math.pi*k/seg)), FTM*z)) for k in range(seg)] for r, z in prof]
    for i in range(len(rings)-1):
        A, B = rings[i], rings[i+1]
        if prof[i][0] == 0 and prof[i+1][0] == 0: continue
        for k in range(seg):
            bm.faces.new([A[k], A[(k+1) % seg], B[(k+1) % seg], B[k]]).material_index = mi
    if prof[-1][0] > 0: bm.faces.new(rings[-1]).material_index = mi
    if prof[0][0] > 0: bm.faces.new(list(reversed(rings[0]))).material_index = mi
def _box(bm, x0, x1, y0, y1, z0, z1, mi, R=None):
    vs = [Vector((x, y, z)) for x, y, z in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]]
    if R is not None: vs = [R @ v for v in vs]
    vs = [bm.verts.new(v * FTM) for v in vs]
    for q in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:
        bm.faces.new([vs[i] for i in q]).material_index = mi
def _head(bm, z0, hair=V_BRN):
    _lathe(bm, [(0.0, z0), (0.13, z0), (0.13, z0+0.12), (0.27, z0+0.2), (0.32, z0+0.45), (0.27, z0+0.7), (0.0, z0+0.77)], 8, V_SKIN)
def _tophat(bm, z0, mi=V_BLK):
    _lathe(bm, [(0.0, z0), (0.48, z0), (0.48, z0+0.06), (0.31, z0+0.08), (0.33, z0+0.75), (0.34, z0+0.8), (0.0, z0+0.8)], 10, mi)
def _bonnet(bm, z0, mi):
    # close 'spoon' bonnet of the later 1850s: crown on the back of the head + brim framing the face (front = -Y)
    _lathe(bm, [(0.0, z0+0.05), (0.3, z0+0.1), (0.36, z0+0.4), (0.3, z0+0.66), (0.0, z0+0.72)], 8, mi, cy=0.08)
    _lathe(bm, [(0.42, z0+0.08), (0.44, z0+0.45), (0.36, z0+0.78), (0.3, z0+0.8)], 10, mi, cy=-0.12, sy=0.6)
def _arm(bm, x, z0, z1, mi, r=0.17):
    _lathe(bm, [(r, z0), (r*1.05, z1), (0.0, z1+0.1)], 5, mi, cx=x)

def man_standing(bm, coat, hat=True, shirt=False):
    for s in (-0.26, 0.26): _lathe(bm, [(0.2, 0.0), (0.19, 1.3), (0.22, 2.7), (0.0, 2.75)], 6, V_BLK if coat == V_BLK else V_GRY, cx=s)
    _lathe(bm, [(0.0, 1.85), (0.72, 1.85), (0.6, 2.8), (0.5, 3.45), (0.62, 4.3), (0.66, 4.55), (0.4, 4.78), (0.0, 4.8)], 10, coat)  # frock coat to the knee
    if shirt: _box(bm, -0.18, 0.18, -0.6, -0.5, 3.9, 4.65, V_LIN)
    for s in (-0.7, 0.7): _arm(bm, s, 3.0, 4.45, coat)
    _head(bm, 4.72)
    if hat: _tophat(bm, 5.38)
def woman_standing(bm, dress, mantle, bonnet=True, crin=2.1):
    _lathe(bm, [(0.0, 0.0), (crin, 0.0), (crin*0.98, 0.35), (crin*0.86, 1.2), (crin*0.62, 2.2), (0.42, 3.3), (0.0, 3.32)], 14, dress)  # crinoline dome
    _lathe(bm, [(0.0, 3.2), (0.4, 3.2), (0.36, 3.5), (0.5, 4.1), (0.38, 4.45), (0.0, 4.5)], 9, dress)    # bodice
    _lathe(bm, [(0.0, 3.35), (0.95, 3.35), (0.75, 3.8), (0.46, 4.3), (0.2, 4.45), (0.0, 4.46)], 10, mantle)   # mantle / shawl
    _head(bm, 4.38)
    if bonnet: _bonnet(bm, 4.6, V_STRAW if mantle != V_BLK else V_BLK)
    else: _lathe(bm, [(0.0, 4.95), (0.31, 4.98), (0.3, 5.15), (0.0, 5.18)], 8, V_BRN)   # hair, centre parting
def man_seated(bm, coat, hat=False, shirt=False):
    for s in (-0.26, 0.26):
        _lathe(bm, [(0.2, 0.0), (0.2, 1.5), (0.0, 1.52)], 6, V_BLK, cx=s, cy=-1.4)          # shins
        _box(bm, s-0.21, s+0.21, -1.6, 0.0, 1.3, 1.75, V_BLK)                              # thighs
    _lathe(bm, [(0.0, 1.3), (0.7, 1.3), (0.55, 2.0), (0.6, 2.9), (0.64, 3.1), (0.4, 3.32), (0.0, 3.35)], 10, coat)
    if shirt: _box(bm, -0.18, 0.18, -0.6, -0.5, 2.45, 3.2, V_LIN)
    for s in (-0.68, 0.68): _box(bm, s-0.16, s+0.16, -1.0, 0.1, 1.9, 2.3, coat)            # forearms on lap
    _head(bm, 3.27)
    if hat: _tophat(bm, 3.93)
def woman_seated(bm, dress, mantle, bonnet=True):
    _lathe(bm, [(0.0, 0.0), (1.8, 0.0), (1.75, 0.5), (1.5, 1.4), (0.9, 1.85), (0.0, 1.9)], 12, dress, cy=-0.45)   # spread skirt
    _lathe(bm, [(0.0, 1.8), (0.4, 1.8), (0.36, 2.05), (0.5, 2.65), (0.38, 3.0), (0.0, 3.05)], 9, dress)
    _lathe(bm, [(0.0, 1.95), (0.9, 1.95), (0.72, 2.35), (0.46, 2.85), (0.0, 3.0)], 10, mantle)
    _head(bm, 2.93)
    if bonnet: _bonnet(bm, 3.15, V_STRAW if mantle != V_BLK else V_BLK)
    else: _lathe(bm, [(0.0, 3.5), (0.31, 3.53), (0.3, 3.7), (0.0, 3.73)], 8, V_BRN)
def strings_player(bm, kind):
    man_seated(bm, V_BLK, shirt=True)
    if kind == 'violin':
        _box(bm, 0.25, 0.6, -0.9, 0.15, 3.0, 3.18, V_WOOD)            # violin under the chin (block, I)
        _box(bm, -0.85, 0.1, -1.0, -0.94, 2.95, 3.05, V_BLK)           # bow
    elif kind == 'cello':
        _lathe(bm, [(0.0, 0.3), (0.55, 0.45), (0.45, 1.3), (0.55, 2.0), (0.3, 2.4), (0.06, 2.5), (0.05, 3.6), (0.0, 3.7)], 8, V_WOOD, cy=-1.3, sy=0.45)
    elif kind == 'wind':
        _box(bm, -0.05, 0.05, -1.25, -0.5, 2.5, 3.4, V_BLK)            # clarinet / oboe, I
    elif kind == 'brass':
        _lathe(bm, [(0.08, 2.3), (0.1, 2.9), (0.45, 3.3), (0.0, 3.31)], 8, V_BRASS, cy=-0.9)
def bass_player(bm):
    man_standing(bm, V_BLK, hat=False, shirt=True)
    _lathe(bm, [(0.0, 0.25), (0.75, 0.5), (0.6, 2.0), (0.75, 3.0), (0.42, 3.8), (0.08, 3.95), (0.07, 5.7), (0.0, 5.8)], 8, V_WOOD, cx=0.35, cy=-1.0, sy=0.45)
def conductor(bm):
    man_standing(bm, V_BLK, hat=False, shirt=True)
    _box(bm, 0.62, 0.8, -0.3, -0.1, 4.4, 5.5, V_BLK)                   # raised right forearm
    _box(bm, 0.69, 0.73, -0.5, -0.45, 5.3, 6.6, V_LIN)                 # baton

TEMPLATES = []   # (key, builder)
def _t(key, fn): TEMPLATES.append((key, fn))
for i, c in enumerate((V_BLK, V_BRN, V_GRY, V_NAVY)):
    _t(f'man_st_{i}', lambda bm, c=c: man_standing(bm, c))
for i, (d, m) in enumerate(((V_GRN, V_BLK), (V_PLUM, V_SHAWL), (V_BLUE, V_FAWN), (V_FAWN, V_BLK), (V_SGRY, V_SHAWL), (V_BLK, V_SGRY))):
    _t(f'woman_st_{i}', lambda bm, d=d, m=m: woman_standing(bm, d, m))
for i, c in enumerate((V_BLK, V_BRN, V_GRY)):
    _t(f'man_se_{i}', lambda bm, c=c: man_seated(bm, c))
for i, (d, m) in enumerate(((V_GRN, V_BLK), (V_PLUM, V_SHAWL), (V_BLUE, V_FAWN), (V_SGRY, V_BLK))):
    _t(f'woman_se_{i}', lambda bm, d=d, m=m: woman_seated(bm, d, m))
_t('chorus_w_0', lambda bm: woman_standing(bm, V_MUS, V_MUS, bonnet=False, crin=1.35))
_t('chorus_w_1', lambda bm: woman_standing(bm, V_MUS, V_LIN, bonnet=False, crin=1.35))
_t('chorus_m_0', lambda bm: man_standing(bm, V_BLK, hat=False, shirt=True))
for k in ('violin', 'cello', 'wind', 'brass'):
    _t(f'band_{k}', lambda bm, k=k: strings_player(bm, k))
_t('band_bass', bass_player)
_t('conductor', conductor)

# ---- r14 period templates (appended so r13 indices stay stable) ----
def navvy(bm, shirt, tool):
    for s_ in (-0.26, 0.26): _lathe(bm, [(0.22, 0.0), (0.21, 1.3), (0.24, 2.75), (0.0, 2.8)], 6, V_MOLE, cx=s_)   # moleskin trousers
    _lathe(bm, [(0.0, 2.7), (0.6, 2.7), (0.55, 3.4), (0.64, 4.3), (0.66, 4.5), (0.4, 4.75), (0.0, 4.78)], 10, shirt)  # flannel shirt
    _lathe(bm, [(0.0, 3.3), (0.6, 3.3), (0.62, 4.3), (0.0, 4.32)], 10, V_BRN)                                      # waistcoat
    _arm(bm, -0.7, 3.0, 4.45, shirt); _box(bm, 0.55, 0.85, -0.55, -0.25, 3.3, 4.45, shirt)                         # one arm forward
    _head(bm, 4.72)
    _lathe(bm, [(0.0, 5.3), (0.5, 5.32), (0.5, 5.38), (0.33, 5.42), (0.32, 5.75), (0.0, 5.78)], 10, V_DRAB)        # wideawake hat
    if tool == 'shovel':
        _box(bm, 0.66, 0.74, -0.9, -0.82, 1.2, 4.0, V_WOOD); _box(bm, 0.45, 0.95, -0.95, -0.88, 0.2, 1.3, V_GRY)
    elif tool == 'pick':
        _box(bm, 0.66, 0.74, -0.75, -0.67, 2.2, 5.6, V_WOOD); _box(bm, 0.2, 1.2, -0.76, -0.66, 5.4, 5.6, V_GRY)
def courtier(bm, coat, sash=None):
    man_standing(bm, coat, hat=False, shirt=True)
    if sash is not None: _box(bm, -0.5, 0.5, -0.66, -0.58, 3.8, 4.0, sash)
    for s_ in (-0.5, 0.5): _box(bm, s_-0.18, s_+0.18, -0.2, 0.2, 4.5, 4.62, V_GOLD)                                # epaulettes / lace
def queen(bm):
    woman_standing(bm, V_PINK, V_PINK, bonnet=False, crin=2.0)
    _box(bm, -0.55, 0.55, -0.48, -0.42, 3.6, 3.75, V_BLUE)                                                         # Garter riband
    _lathe(bm, [(0.0, 5.12), (0.24, 5.12), (0.24, 5.3), (0.0, 5.32)], 8, V_GOLD)                                   # diadem (form only)
def yeoman(bm):
    man_standing(bm, V_SCAR, hat=False)
    _box(bm, -0.45, 0.45, -0.68, -0.6, 3.2, 4.4, V_GOLD)
    _lathe(bm, [(0.0, 5.32), (0.55, 5.34), (0.4, 5.45), (0.36, 5.8), (0.0, 5.85)], 10, V_BLK)                      # Tudor bonnet
    _box(bm, 0.75, 0.82, -0.3, -0.23, 0.0, 7.2, V_WOOD); _box(bm, 0.6, 0.98, -0.31, -0.22, 7.0, 7.8, V_GRY)        # partisan
def ed_man(bm, coat, hat):
    for s_ in (-0.24, 0.24): _lathe(bm, [(0.19, 0.0), (0.18, 1.3), (0.21, 2.75), (0.0, 2.8)], 6, coat, cx=s_)
    _lathe(bm, [(0.0, 2.6), (0.6, 2.6), (0.56, 3.4), (0.62, 4.3), (0.64, 4.52), (0.38, 4.75), (0.0, 4.78)], 10, coat)   # lounge suit
    _box(bm, -0.12, 0.12, -0.62, -0.55, 4.2, 4.65, V_LIN)
    for s_ in (-0.68, 0.68): _arm(bm, s_, 3.0, 4.45, coat)
    _head(bm, 4.72)
    if hat == 'boater': _lathe(bm, [(0.0, 5.3), (0.55, 5.32), (0.55, 5.36), (0.34, 5.38), (0.34, 5.6), (0.0, 5.62)], 12, V_BOAT)
    else: _lathe(bm, [(0.0, 5.3), (0.45, 5.32), (0.42, 5.38), (0.33, 5.42), (0.36, 5.7), (0.2, 5.82), (0.0, 5.84)], 10, V_BLK)   # bowler
def ed_woman(bm, dress, hat):
    _lathe(bm, [(0.0, 0.0), (0.95, 0.0), (0.8, 0.6), (0.55, 2.0), (0.42, 3.0), (0.0, 3.05)], 12, dress)               # long gored skirt (c.1908-13)
    _lathe(bm, [(0.0, 2.95), (0.42, 2.95), (0.36, 3.3), (0.52, 4.0), (0.36, 4.42), (0.0, 4.48)], 9, V_CREAM if dress != V_CREAM else V_LIN)  # blouse
    for s_ in (-0.6, 0.6): _arm(bm, s_, 3.0, 4.3, V_CREAM, r=0.13)
    _head(bm, 4.38)
    _lathe(bm, [(0.0, 4.95), (1.1, 4.98), (1.1, 5.04), (0.4, 5.1), (0.38, 5.4), (0.0, 5.45)], 14, hat)                # picture hat
def rating(bm, white_top=False):
    for s_ in (-0.25, 0.25): _lathe(bm, [(0.24, 0.0), (0.22, 1.3), (0.22, 2.75), (0.0, 2.8)], 6, V_NAVY, cx=s_)      # bell-bottoms
    _lathe(bm, [(0.0, 2.6), (0.58, 2.6), (0.55, 3.4), (0.62, 4.35), (0.64, 4.5), (0.38, 4.75), (0.0, 4.78)], 10, V_LIN if white_top else V_NAVY)  # jumper
    _box(bm, -0.55, 0.55, -0.05, 0.6, 4.3, 4.72, V_NAVY if white_top else V_SGRY)                                 # square collar
    for s_ in (-0.68, 0.68): _arm(bm, s_, 3.0, 4.45, V_LIN if white_top else V_NAVY)
    _head(bm, 4.72)
    _lathe(bm, [(0.0, 5.3), (0.36, 5.32), (0.42, 5.5), (0.42, 5.56), (0.0, 5.58)], 10, V_LIN)                      # white-topped cap
    _box(bm, 0.72, 0.8, -0.12, -0.04, 1.5, 5.6, V_WOOD)                                                          # rifle at the slope/order (I)
for k_, fn_ in (('navvy_shovel', lambda bm: navvy(bm, V_RUST, 'shovel')), ('navvy_pick', lambda bm: navvy(bm, V_LIN, 'pick')),
                ('navvy_plain', lambda bm: navvy(bm, V_RUST, None)), ('courtier_blk', lambda bm: courtier(bm, V_BLK, V_BLUE)),
                ('courtier_scar', lambda bm: courtier(bm, V_SCAR, V_BLUE)), ('queen_1854', queen), ('yeoman', yeoman),
                ('ed_man_0', lambda bm: ed_man(bm, V_GRY, 'boater')), ('ed_man_1', lambda bm: ed_man(bm, V_NAVY, 'bowler')),
                ('ed_man_2', lambda bm: ed_man(bm, V_BRN, 'bowler')), ('ed_woman_0', lambda bm: ed_woman(bm, V_CREAM, V_BLK)),
                ('ed_woman_1', lambda bm: ed_woman(bm, V_NAVY, V_BOAT)), ('ed_woman_2', lambda bm: ed_woman(bm, V_SGRY, V_PLUM)),
                ('ed_woman_3', lambda bm: ed_woman(bm, V_GRN, V_CREAM)), ('rating_blue', lambda bm: rating(bm)),
                ('rating_white', lambda bm: rating(bm, True))):
    _t(k_, fn_)
TIDX = {k: i for i, (k, _) in enumerate(TEMPLATES)}
MEN_ST = [TIDX[f'man_st_{i}'] for i in range(4)]; WOM_ST = [TIDX[f'woman_st_{i}'] for i in range(6)]
MEN_SE = [TIDX[f'man_se_{i}'] for i in range(3)]; WOM_SE = [TIDX[f'woman_se_{i}'] for i in range(4)]
NAVVY = [TIDX[k] for k in ('navvy_shovel', 'navvy_pick', 'navvy_plain')]; ED_M = [TIDX[f'ed_man_{i}'] for i in range(3)]; ED_W = [TIDX[f'ed_woman_{i}'] for i in range(4)]
def public11(r, wfrac=0.5): return r.choice(ED_W) if r.random() < wfrac else r.choice(ED_M)

PPL_TC = bpy.data.collections.new('PPL57_templates__instanced_not_rendered'); sc.collection.children.link(PPL_TC)
for i, (k, fn) in enumerate(TEMPLATES):
    bm = bmesh.new(); fn(bm); me = bpy.data.meshes.new(f'pv57_{i:02d}_{k}'); bm.to_mesh(me); bm.free()
    for m_ in PV: me.materials.append(m_)
    PPL_TC.objects.link(bpy.data.objects.new(f'pv57_{i:02d}_{k}', me))
for lc in bpy.context.view_layer.layer_collection.children:
    if lc.collection == PPL_TC: lc.exclude = True

def _ppl_group():
    ng = bpy.data.node_groups.get('PPL57_instance_people')
    if ng: return ng
    ng = bpy.data.node_groups.new('PPL57_instance_people', 'GeometryNodeTree')
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    n, l = ng.nodes, ng.links
    gi = n.new('NodeGroupInput'); go = n.new('NodeGroupOutput')
    ci = n.new('GeometryNodeCollectionInfo'); ci.inputs['Collection'].default_value = PPL_TC
    ci.inputs['Separate Children'].default_value = True; ci.inputs['Reset Children'].default_value = True
    ci.transform_space = 'ORIGINAL'
    io = n.new('GeometryNodeInstanceOnPoints'); io.inputs['Pick Instance'].default_value = True
    a_t = n.new('GeometryNodeInputNamedAttribute'); a_t.data_type = 'INT'; a_t.inputs['Name'].default_value = 'tmpl'
    a_r = n.new('GeometryNodeInputNamedAttribute'); a_r.data_type = 'FLOAT_VECTOR'; a_r.inputs['Name'].default_value = 'rot'
    a_s = n.new('GeometryNodeInputNamedAttribute'); a_s.data_type = 'FLOAT'; a_s.inputs['Name'].default_value = 'scl'
    e2r = n.new('FunctionNodeEulerToRotation')
    l.new(gi.outputs[0], io.inputs['Points']); l.new(ci.outputs[0], io.inputs['Instance'])
    l.new(a_t.outputs['Attribute'], io.inputs['Instance Index']); l.new(a_r.outputs['Attribute'], e2r.inputs[0])
    l.new(e2r.outputs[0], io.inputs['Rotation']); l.new(a_s.outputs['Attribute'], io.inputs['Scale'])
    l.new(io.outputs[0], go.inputs[0])
    return ng
def face_rot(dx, dy):
    """templates face local -Y; rotation about Z so the figure faces (dx, dy)"""
    return math.atan2(dx, -dy)
F_ = 0.3048
def people(name, col, pts):
    """pts: (x, y, z, tmpl, rotz[, scl]) in feet -> carrier mesh (1 vertex / person) + GN instancing modifier"""
    # r13: keep a clear zone round every camera already in the file (no figure within 7 ft of a lens)
    cams = [(o.location.x/F_, o.location.y/F_, o.location.z/F_) for o in bpy.data.objects if o.type == 'CAMERA']
    pts = [p for p in pts if not any((p[0]-c[0])**2 + (p[1]-c[1])**2 < 49 and abs(p[2] + 5 - c[2]) < 8 for c in cams)]
    me = bpy.data.meshes.new(name); me.vertices.add(len(pts))
    me.vertices.foreach_set('co', [c for p in pts for c in (f(p[0]), f(p[1]), f(p[2]))])
    at = me.attributes.new('tmpl', 'INT', 'POINT'); at.data.foreach_set('value', [int(p[3]) for p in pts])
    ar = me.attributes.new('rot', 'FLOAT_VECTOR', 'POINT'); ar.data.foreach_set('vector', [c for p in pts for c in (0.0, 0.0, p[4])])
    asl = me.attributes.new('scl', 'FLOAT', 'POINT'); asl.data.foreach_set('value', [p[5] if len(p) > 5 else 1.0 for p in pts])
    o = bpy.data.objects.new(name, me); col.objects.link(o)
    md = o.modifiers.new('people', 'NODES'); md.node_group = _ppl_group()
    o['people_count'] = len(pts)
    return o
PRNG = random.Random(1857)
def public(r, seated=False, wfrac=0.5):
    if seated: return r.choice(WOM_SE) if r.random() < wfrac else r.choice(MEN_SE)
    return r.choice(WOM_ST) if r.random() < wfrac else r.choice(MEN_ST)
