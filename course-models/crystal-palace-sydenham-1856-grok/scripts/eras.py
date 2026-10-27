# r14: further dated Sydenham states (exec'd at the end of build.py, after people57; shares its namespace).
#   BUILD53  SY-BUILD   CP033  c. autumn 1853: frame rising, terraces being cut, park earthworks (pre-1866 fabric, stripped)
#   OPEN54   SY54       CP035  10 June 1854 opening: royal procession, dais, choir, crowds, flags (no water towers / great
#                              fountains); also G-STATION CP036 (scripts/station.py)
#   LATE11   SY-LATE    CP049-54  1911 Festival of Empire dressing on the worn post-1866 fabric
#   WAR      SY-WAR     CP056  1914-18 Royal Naval Division depot 'HMS Crystal Palace': ratings drilling
# Every guess is graded in DEPARTURES r14 (D-R14-*).
import bmesh, random
from mathutils import Vector
FT = 0.3048
def kill_obj(o): bpy.data.objects.remove(o, do_unlink=True)
def kill_coll(name):
    c = bpy.data.collections.get(name)
    if not c: return
    for o in list(c.all_objects): kill_obj(o)
    for ch in list(c.children_recursive): bpy.data.collections.remove(ch)
    bpy.data.collections.remove(c)
def kill(*names):
    for n in names:
        o = bpy.data.objects.get(n)
        if o: kill_obj(o)
def clip(name, pred):
    """delete faces of object `name` whose centre (feet) satisfies pred(x, y, z)"""
    o = bpy.data.objects.get(name)
    if not o or o.type != 'MESH': return 0
    bm = bmesh.new(); bm.from_mesh(o.data); mw = o.matrix_world
    d = [fc for fc in bm.faces if pred(*((mw @ fc.calc_center_median()) / FT))]
    bmesh.ops.delete(bm, geom=d, context='FACES'); bm.to_mesh(o.data); bm.free(); o.data.update(); return len(d)
def remat(name, m, m2=None, pred2=None):
    o = bpy.data.objects.get(name)
    if not o: return
    o.data.materials.clear(); o.data.materials.append(m)
    if m2 is not None: o.data.materials.append(m2)
    mw = o.matrix_world
    for p in o.data.polygons:
        p.material_index = 1 if (m2 is not None and pred2(*((mw @ p.center) / FT))) else 0
def gz_ray(x, y, top=400.0, skip=()):
    dg = bpy.context.evaluated_depsgraph_get()
    o0 = Vector((f(x), f(y), f(top)))
    for _ in range(12):
        h, loc, n_, i_, ob, m_ = sc.ray_cast(dg, o0, Vector((0, 0, -1)))
        if not h: return None
        if ob.name.startswith(skip) if skip else False:
            o0 = loc - Vector((0, 0, 0.01)); continue
        return loc.z / FT
    return None
GROUNDS = ('park_slope', 'terrain', 'terrace_gravel', 'central_walk', 'park_paths_gravel', 'parterre_grass', 'flower_beds',
           'ground_under_palace', 'terraces_stone', 'distant_ground', 'earth_')
def gzg(x, y):
    """ground height (ft) at x,y: first hit on a ground object"""
    dg = bpy.context.evaluated_depsgraph_get(); o0 = Vector((f(x), f(y), f(500)))
    for _ in range(40):
        h, loc, n_, i_, ob, m_ = sc.ray_cast(dg, o0, Vector((0, 0, -1)))
        if not h: return gzp(x, y)
        if ob.name.startswith(GROUNDS): return loc.z / FT
        o0 = loc - Vector((0, 0, 0.02))
    return gzp(x, y)
def flag(mb_pole, mats_bands, x, y, z0, pole_h, w=12.0, h=8.0, wave=1.2, axis='x', vertical=False, seed=0):
    """pole + waving flag (flag built as vertical bands of materials, list of MB). Flag flies toward +axis."""
    if mb_pole is not None: mb_pole.cyl(x, y, z0, z0 + pole_h, 0.35, 0.18, 6)
    n = len(mats_bands); zt = z0 + pole_h - 0.5
    for k, mb in enumerate(mats_bands):
        segs = 4
        for s_ in range(segs):
            u0 = (k + s_/segs) / n; u1 = (k + (s_+1)/segs) / n
            d0 = wave * math.sin(u0 * 5.0 + seed); d1 = wave * math.sin(u1 * 5.0 + seed)
            if axis == 'x': p = [(x + u0*w, y + d0, zt - h), (x + u1*w, y + d1, zt - h), (x + u1*w, y + d1, zt), (x + u0*w, y + d0, zt)]
            else: p = [(x + d0, y + u0*w, zt - h), (x + d1, y + u1*w, zt - h), (x + d1, y + u1*w, zt), (x + d0, y + u0*w, zt)]
            mb.poly(p)
def banner(mb, x, y, z_top, w, h, axis='x'):
    """hanging banner (flat, hangs down from z_top), faces +-y if axis 'x'"""
    if axis == 'x': mb.poly([(x - w/2, y, z_top - h), (x + w/2, y, z_top - h), (x + w/2, y, z_top), (x - w/2, y, z_top)])
    else: mb.poly([(x, y - w/2, z_top - h), (x, y + w/2, z_top - h), (x, y + w/2, z_top), (x, y - w/2, z_top)])
def fmat(name, rgb, rough=0.75, two=True):
    m = bpy.data.materials.get(name) or mat(name, rgb, rough)
    m.use_backface_culling = False; return m
def grime():
    """1900s wear: glass greyed/darkened, some panes boarded (CP049-054 / CP056). I"""
    for m in bpy.data.materials:
        if not m.node_tree: continue
        for n_ in m.node_tree.nodes:
            if n_.type == 'BSDF_TRANSPARENT':
                c = n_.inputs[0].default_value; n_.inputs[0].default_value = (c[0]*0.62, c[1]*0.62, c[2]*0.6, 1)
    board = fmat('late_boarded_panes_zinc', (0.16, 0.16, 0.15), 0.8)
    rr = random.Random(1911)
    for nm in ('ridge_furrow_roofs', 'glazed_walls', 'nave_vault_glass', 'central_transept_vault_glass', 'south_transept_vault_glass', 'wings_glass'):
        o = bpy.data.objects.get(nm)
        if not o: continue
        o.data.materials.append(board); bi = len(o.data.materials) - 1
        for p in o.data.polygons:
            if rr.random() < 0.035: p.material_index = bi
def crowd_pts(r, region, n, z_of, tfun, face=None):
    x0, x1, y0, y1 = region; pts = []
    for _ in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); z = z_of(x, y)
        if z is None: continue
        rz = face(x, y) if face else r.uniform(-math.pi, math.pi)
        pts.append((x, y, z, tfun(r), rz, r.uniform(0.94, 1.05)))
    return pts

R_ = random.Random(1400 + len(STATE))
_sd14 = os.path.dirname(os.path.abspath(__file__))

# =====================================================================================================================
if STATE == 'BUILD53':
    # ---- what was not there yet (towers 1855-56, fountains 1856, courts/statuary/planting 1854, colonnade 1854) ----
    for cn in ('SY56_water_towers__dated', 'SY56_fountains_basins__dated', 'SY56_park_fountains_cascades__dated',
               'SY_nave_planting_statuary__placeholders', 'SY56_park_paths_beds__dated', 'SY56_court_egyptian_0226__dated',
               'SY56_court_alhambra_0246__dated', 'SY54_terrace_sphinxes_and_side_flights__1854_extant', 'SY54_railway_colonnade',
               'SY56_north_transept_colossi_muse__lost1866', 'MUSE_props_lib__instanced_not_rendered'):
        kill_coll(cn)
    # ---- erection front (D-R14-B1, U): south end first (complete + glazed to x=-350), centre to tier 3 with the
    #      transept ribs half up, x 150..450 columns to tier 1 only, north of x 450 basement piers only ----
    XG, XT3, XT1 = -350.0, 150.0, 450.0
    def zlim(x):
        if x < XG: return 1e9
        if x < XT3: return TIERS[2] + 2.5
        if x < XT1: return TIERS[0] + 1.5
        return 0.5
    for nm in ('frame_SY_main_frame', 'transverse_bracing_72ft', 'roof_gutters', 'facade_ironwork', 'frame_SY_central_transept',
               'SY_central_transept_frame', 'frame_SY_south_transept', 'SY_south_transept_frame', 'frame_SY_north_transept__lost1866',
               'SY_north_transept__lost1866_frame', 'crossing_towers', 'west_front_timber_dado'):
        if 'central' in nm: continue          # the central transept frame was pushed up first (I)
        clip(nm, lambda x, y, z: z > zlim(x))
    for nm in ('gallery_floors', 'main_floor', 'central_transept_projection_floor'):
        clip(nm, lambda x, y, z: x > XT3)
    for nm in ('ridge_furrow_roofs', 'glazed_walls', 'SY_south_transept_walls', 'SY_south_transept_front_roofs', 'basement_windows'):
        clip(nm, lambda x, y, z: x > XG)
    kill('nave_vault_glass', 'central_transept_vault_glass', 'north_transept_vault_glass', 'crossing_towers_glass',
         'SY_central_transept_walls', 'SY_central_transept_front_roofs', 'SY_north_transept__lost1866_walls',
         'SY_north_transept__lost1866_front_roofs', 'north_transept_vault_ribs', 'garden_stairs_to_main_floor')
    clip('nave_vault_ribs', lambda x, y, z: x > XG)
    clip('central_transept_vault_ribs', lambda x, y, z: y < -40)          # ribs going up from the Parade side (U)
    clip('basement_brick', lambda x, y, z: x > XT1)
    for nm in ('wings_glass', 'wings_frame', 'wings_roof'):
        clip(nm, lambda x, y, z: x > 0 or (nm != 'wings_frame' and y < -300))
    # ---- ground: raw clay where the terraces are being cut; park beyond y=-1300 still meadow (D-R14-B2, I) ----
    clay = fmat('build53_raw_clay_spoil', (0.26, 0.17, 0.1), 0.95); meadow = fmat('build53_rough_meadow', (0.09, 0.13, 0.05), 0.95)
    gravel = fmat('build53_trodden_ground', (0.2, 0.17, 0.13), 0.95)
    for nm in ('terrace_gravel', 'terrain', 'ground_under_palace') + tuple(n for n in ('central_walk', 'central_walk.001', 'central_walk.002', 'central_walk.003', 'central_walk.004')):
        remat(nm, clay)
    remat('park_slope', clay, meadow, lambda x, y, z: y < -1300 or abs(x) > 1000)
    clip('terraces_stone', lambda x, y, z: x > 40)   # retaining walls only built on the south half so far (U)
    B = coll('SY-BUILD_construction_1853__dated')
    E = MB('earth_spoil_heaps_cuttings', B, clay)
    # uncut ground still standing on the north half of the lower terrace: wedge from UT down to LT with a raw cut face
    for xa, xb in ((60, 380), (380, 760)):
        y_face = yU - BANK - (70 if xa < 300 else 160)
        E.poly([(xa, y_face, LT), (xb, y_face, LT), (xb, yU - BANK, UT), (xa, yU - BANK, UT)])
        E.poly([(xa, y_face, LT), (xa, yU - BANK, UT), (xa, yU - BANK, LT)]); E.poly([(xb, yU - BANK, LT), (xb, yU - BANK, UT), (xb, y_face, LT)])
    heaps = []
    for i in range(22):
        x = R_.uniform(-900, 900); y = R_.uniform(-1250, yL - 40)
        if abs(x) < 70: continue
        r = R_.uniform(30, 70); hh = r * R_.uniform(0.28, 0.42); z = gzp(x, y) - 1
        E.cyl(x, y, z, z + hh, r, r * 0.25, 12); heaps.append((x, y, z + hh, r))
    E.done()
    # ---- contractor tramways down the slope with tip wagons (D-R14-B3, I) ----
    T = MB('build53_tramway_rails', B, M.get('iron', fmat('build53_iron', (0.1, 0.1, 0.1), 0.5)))
    S = MB('build53_timber', B, fmat('build53_scaffold_timber', (0.33, 0.24, 0.15), 0.85))
    W = MB('build53_tip_wagons', B, fmat('build53_wagon_wood', (0.22, 0.15, 0.09), 0.8))
    HS = MB('build53_horses', B, fmat('build53_horse_bay', (0.13, 0.07, 0.035), 0.8))
    lines = [(-300, -230), (300, 230), (-620, -560)]
    for xa_, xb_ in lines:
        prev = None
        for k in range(0, 44):
            y = -170 - k * 24.0; x = xa_ + (xb_ - xa_) * k / 43.0; z = gzp(x, y) + 0.3
            S.box(x - 3.5, x + 3.5, y - 0.4, y + 0.4, z - 0.3, z)
            if prev:
                for d in (-1.8, 1.8): T.strut((prev[0] + d, prev[1], prev[2] + 0.3), (x + d, y, z + 0.3), 0.25, 0.3)
            prev = (x, y, z)
            if k in (6, 7, 8, 19, 20, 31) :
                W.box(x - 2.6, x + 2.6, y - 4, y + 4, z + 1.2, z + 4.5); W.box(x - 2.0, x + 2.0, y - 3.5, y + 3.5, z + 0.3, z + 1.2)
    def horse(mb, x, y, z, heading):
        c, s_ = math.cos(heading), math.sin(heading)
        def P(u, v, w_): return (x + u*c - v*s_, y + u*s_ + v*c, z + w_)
        def bx(u0, u1, v0, v1, w0, w1):
            mb.poly([P(u0, v0, w0), P(u1, v0, w0), P(u1, v1, w0), P(u0, v1, w0)]); mb.poly([P(u0, v0, w1), P(u0, v1, w1), P(u1, v1, w1), P(u1, v0, w1)])
            mb.poly([P(u0, v0, w0), P(u0, v0, w1), P(u1, v0, w1), P(u1, v0, w0)]); mb.poly([P(u0, v1, w0), P(u1, v1, w0), P(u1, v1, w1), P(u0, v1, w1)])
            mb.poly([P(u0, v0, w0), P(u0, v1, w0), P(u0, v1, w1), P(u0, v0, w1)]); mb.poly([P(u1, v0, w0), P(u1, v0, w1), P(u1, v1, w1), P(u1, v1, w0)])
        bx(-3.2, 3.2, -1.1, 1.1, 3.0, 5.6)
        for u in (-2.6, 2.4):
            for v in (-0.7, 0.7): bx(u - 0.3, u + 0.3, v - 0.3, v + 0.3, 0, 3.1)
        bx(2.6, 4.2, -0.5, 0.5, 4.6, 7.2); bx(3.6, 5.6, -0.45, 0.45, 6.6, 7.6)
    for i, (x, y) in enumerate(((-160, -420), (210, -470), (-420, -720), (520, -820), (90, -930), (-700, -560), (620, -260))):
        z = gzp(x, y); hd = R_.uniform(-3, 3); horse(HS, x, y, z, hd)
        c, s_ = math.cos(hd), math.sin(hd); cx_, cy_ = x - 9*c, y - 9*s_
        W.box(cx_ - 3, cx_ + 3, cy_ - 3, cy_ + 3, z + 2.2, z + 5.2)   # tip cart (axis-aligned box, I)
    # ---- scaffolding round the central transept + shear-legs at the erection front (D-R14-B4, I) ----
    for xx in (-96, -72, 72, 96):
        for yy in range(-168, 193, 24):
            S.box(xx - 0.5, xx + 0.5, yy - 0.5, yy + 0.5, 0, 168 if abs(xx) == 72 else 120)
    for xx in (-96, -72, 72, 96):
        for zz in range(20, 170, 20):
            if abs(xx) == 96 and zz > 120: continue
            S.box(xx - 0.4, xx + 0.4, -168, 192, zz - 0.4, zz + 0.4)
    for yy in range(-168, 193, 48):
        for zz in range(40, 170, 40): S.box(-96, 96, yy - 0.4, yy + 0.4, zz - 0.4, zz + 0.4) if zz <= 120 else None
    def shear_legs(x, y, z0, h, heading):
        c, s_ = math.cos(heading), math.sin(heading); top = (x + 4*c, y + 4*s_, z0 + h)
        for d in (-9, 9): S.strut((x - d*s_, y + d*c, z0), top, 1.0, 1.0)
        S.strut((x - 22*c, y - 22*s_, z0), top, 0.9, 0.9)
        T.strut(top, (top[0] + 2*c, top[1] + 2*s_, z0 + 8), 0.12, 0.12)    # fall rope
    for (x, y) in ((XT3 + 24, 140), (XT3 + 24, -140), (XT3 + 120, 0), (XT1 - 40, 120), (XT1 - 40, -120), (-20, 205)):
        shear_legs(x, y, 0 if y > -150 else gz(y), 70 if x < XT1 - 100 else 40, 0.0)
    # stacks of columns and girders on the Parade side (north)
    for i in range(10):
        x0 = 520 + (i % 5) * 40; y0 = 200 + (i // 5) * 40
        for k in range(5):
            S.box(x0, x0 + 24, y0 + k * 3, y0 + k * 3 + 1.5, 0.2 + (k % 2) * 1.5, 1.7 + (k % 2) * 1.5) if i % 2 else T.box(x0, x0 + 24, y0 + k * 2.4, y0 + k * 2.4 + 1.2, 0.2, 2.6)
    # contractor's huts on the Parade
    for (x, y) in ((-200, 260), (-140, 260), (260, 250), (700, 330)):
        S.box(x - 18, x + 18, y - 9, y + 9, 0, 10); S.poly([(x - 19, y - 10, 10), (x + 19, y - 10, 10), (x + 19, y, 14), (x - 19, y, 14)]); S.poly([(x - 19, y, 14), (x + 19, y, 14), (x + 19, y + 10, 10), (x - 19, y + 10, 10)])
    T.done(); S.done(); W.done(); HS.done()
    # ---- cameras then navvies (people() keeps the lens clear) ----
    cam('CAM_CP033_slope_up_35mm', (260, -1080, gzp(260, -1080) + EYE + 4), (40, -200, 55), 35)
    cam('CAM_CP033_terrace_cut_35mm', (-160, yL + 30, LT + EYE), (460, yU - 120, LT + 22), 35)
    cam('CAM_CP033_frame_rising_35mm', (760, 520, EYE), (200, 40, 45), 35)
    cam('CAM_CP033_transept_ribs_28mm', (-150, -14, EYE), (10, 10, 110), 28)
    pts = []
    for (x, y, zt, r) in heaps:
        for k in range(R_.randint(6, 14)):
            a = R_.uniform(0, 6.283); d = r * R_.uniform(1.0, 1.4)
            px, py = x + d*math.cos(a), y + d*math.sin(a); pts.append((px, py, gzp(px, py), R_.choice(NAVVY), face_rot(x - px, y - py), R_.uniform(0.95, 1.04)))
    for xa, xb in ((60, 380), (380, 760)):     # gangs at the cut faces
        y_face = yU - BANK - (70 if xa < 300 else 160)
        for k in range(55):
            px = R_.uniform(xa + 5, xb - 5); py = y_face - R_.uniform(2, 30)
            pts.append((px, py, LT, R_.choice(NAVVY), face_rot(0, 1) + R_.uniform(-0.6, 0.6), R_.uniform(0.95, 1.04)))
    for xa_, xb_ in lines:
        for k in range(0, 44, 2):
            y = -170 - k*24.0; x = xa_ + (xb_ - xa_)*k/43.0 + R_.choice((-6, 6))
            if R_.random() < 0.6: pts.append((x, y, gzp(x, y), R_.choice(NAVVY), R_.uniform(-3, 3), 1.0))
    for k in range(260):      # erectors on the frame (gallery level girders, tier 1 front) and ground gangs in the building
        x = R_.uniform(XG, XT1); y = R_.choice(COL_Y) + R_.uniform(-1, 1)
        z = 0 if (R_.random() < 0.55 or x > XT1) else (TIERS[0] if x < XT1 else 0)
        if x > XT3 and z == 0: z = 0 if R_.random() < 0.5 else TIERS[0]
        pts.append((x, y, z, R_.choice(NAVVY), R_.uniform(-3, 3), 1.0))
    for k in range(120):
        x = R_.uniform(-900, 900); y = R_.uniform(-1250, -200); pts.append((x, y, gzp(x, y), R_.choice(NAVVY), R_.uniform(-3, 3), 1.0))
    NV = people('ppl53_navvies_erectors', B, pts)
    print('BUILD53 navvies', NV['people_count'])

# =====================================================================================================================
if STATE == 'OPEN54':
    kill_coll('SY56_water_towers__dated'); kill_coll('SY56_park_fountains_cascades__dated')   # towers 1855-56, park fountains 1856 (R)
    kill('fountain_jets')                                                                    # terrace fountains not playing (U)
    O = coll('SY54_opening_day_10Jun1854__dated')
    red = fmat('open54_crimson_cloth', (0.32, 0.02, 0.03), 0.7); gold = fmat('open54_gold_fringe', (0.62, 0.45, 0.14), 0.35)
    wht = fmat('open54_white_bunting', (0.8, 0.8, 0.76)); blu = fmat('open54_blue_bunting', (0.03, 0.06, 0.25)); scar = fmat('open54_red_bunting', (0.45, 0.03, 0.03))
    grn = fmat('open54_green_bunting', (0.03, 0.2, 0.06)); yel = fmat('open54_yellow_bunting', (0.65, 0.5, 0.05))
    MBS = {k: MB('open54_flags_' + k, O, m) for k, m in (('red', scar), ('white', wht), ('blue', blu), ('green', grn), ('yellow', yel), ('gold', gold), ('crimson', red))}
    POLE = MB('open54_flagpoles', O, fmat('open54_pole_white', (0.7, 0.7, 0.66), 0.6))
    combos = [('red', 'white', 'blue'), ('blue', 'white', 'red'), ('green', 'white', 'red'), ('yellow', 'red'), ('red', 'white'), ('blue', 'yellow'), ('red',), ('white', 'green')]
    # roof flags (D-R14-O3, I: engravings show a line of flags of many nations along the roof)
    for i, x in enumerate(range(-768, 769, 96)):
        if abs(x) < 72: continue
        flag(POLE, [MBS[c] for c in combos[i % len(combos)]], x, 0, NAVE_CROWN, 26, 14, 9, seed=i)
    for xc_ in (0, -ST_X, ST_X):
        crown = CT_CROWN if xc_ == 0 else ST_CROWN
        for yy in (-140, 0, 150):
            flag(POLE, [MBS['gold'], MBS['crimson'], MBS['blue'], MBS['gold']] if (xc_ == 0 and yy == 0) else [MBS[c] for c in combos[int(yy // 10 + xc_) % len(combos)]],
                 xc_, yy, crown, 34 if xc_ == 0 else 26, 18 if xc_ == 0 else 13, 12 if xc_ == 0 else 8, seed=yy)
    # banners from the gallery fronts down the nave and round the transept (I)
    for i, x in enumerate(range(-780, 781, 48)):
        if abs(x) < 64: continue
        for sy in (-1, 1):
            banner(MBS[combos[(i + (sy > 0)) % len(combos)][0]], x, sy * 35.5, GALLERY_FLOOR + 3, 7, 14)
    # ---- dais + throne + canopy at the transept centre, facing north to the choir (D-R14-O1, U) ----
    D = MB('open54_dais', O, red); G = MB('open54_dais_gilt', O, gold)
    D.box(-46, -14, -22, 22, 0, 3.0); D.box(-50, -46, -22, 22, 0, 1.5); G.box(-46.2, -13.8, -22.2, 22.2, 2.6, 3.05)
    D.box(-42, -38, -3, 3, 3, 9.5); G.box(-42.2, -37.8, -3.2, 3.2, 9.3, 10)                                  # throne (block)
    for yy in (-12, 12):
        for xx in (-44, -24): G.cyl(xx, yy, 3, 22, 0.35, 0.35, 8)
    D.box(-46, -22, -14, 14, 22, 24); G.box(-46.4, -21.6, -14.4, 14.4, 21.6, 22.2)
    # choir/orchestra stand (I: 1,600 performers per press, form U)
    CH = MB('open54_choir_stand', O, fmat('open54_stand_timber', (0.32, 0.22, 0.13), 0.8))
    for k in range(14): CH.box(70 + k*6.5, 172, -104, 104, 0, 2 + k*2.6)
    # seating stands in the transept arms (Parade + garden sides)
    for sy in (-1, 1):
        for k in range(10): CH.box(-56, 56, sy*(40 + k*7) - (7 if sy < 0 else 0), sy*(40 + k*7) + (0 if sy < 0 else 7), 0, 1.2 + k*2.0)
    for m_ in list(MBS.values()) + [POLE, D, G, CH]: m_.done()
    # ---- cameras before crowds ----
    cam('CAM_CP035_transept_gallery_28mm', (-98, 40, GALLERY_FLOOR + EYE), (40, -6, 6), 28)
    cam('CAM_CP035_procession_nave_28mm', (-56, 16, EYE + 3), (-260, -3, 7), 28)
    cam('CAM_CP035_dais_50mm', (-8, 26, EYE + 3), (-38, 0, 8), 50)
    cam('CAM_CP035_garden_front_flags_35mm', (-220, yL + 30, LT + EYE), (40, -157, 125), 35)
    pts = []; perf = []
    # royal party on the dais (Queen, Prince Albert, children, King of Portugal, court) - figure forms only (I)
    roy = [(-40, 0, 'queen_1854'), (-40, 4.5, 'courtier_scar'), (-37, -4.5, 'woman_st_5'), (-34, 6, 'man_st_0'), (-34, -7, 'courtier_scar'),
           (-28, 9, 'courtier_blk'), (-28, -9, 'courtier_blk'), (-31, 11, 'woman_st_1'), (-31, -11, 'woman_st_4'), (-25, 0, 'courtier_blk')]
    for x, y, t in roy: pts.append((x, y, 3.0, TIDX[t], face_rot(1, 0), 1.0 if t != 'man_st_0' else 0.8))
    for k in range(10):       # yeomen of the guard lining the dais steps
        pts.append((-52 + (k % 5) * 8, -26 if k < 5 else 26, 0, TIDX['yeoman'], face_rot(0, 1 if k < 5 else -1), 1.0))
    # procession in the nave heading to the dais: yeomen pairs, heralds/officers, the royal party walking (I/U)
    for k in range(18):
        x = -120 - k*6; pts.append((x, -5, 0, TIDX['yeoman'] if k % 3 else TIDX['courtier_blk'], face_rot(1, 0), 1.0)); pts.append((x, 5, 0, TIDX['yeoman'] if k % 3 else TIDX['courtier_scar'], face_rot(1, 0), 1.0))
    for k, t in enumerate(('courtier_blk', 'courtier_scar', 'courtier_blk', 'courtier_blk', 'courtier_scar', 'woman_st_1', 'woman_st_5', 'man_st_3')):
        pts.append((-232 - (k // 2)*7, -3 + (k % 2)*6, 0, TIDX[t], face_rot(1, 0), 1.0))
    # crowds lining the nave behind barriers, in the transept stands, the galleries
    # r16 quality: densify via people() instancing toward ~40,000 present (R); prior ~8.8k
    for x0 in range(-780, -40, 1):
        for sy in (-1, 1):
            for j in range(9):
                y = sy * (12 + j * 2.2 + R_.uniform(-0.5, 0.5)); x = x0 + R_.uniform(-0.4, 0.4)
                if R_.random() < 0.92: pts.append((x, y, 0, public(R_), face_rot(0, -sy) + R_.uniform(-0.5, 0.5), R_.uniform(0.95, 1.04)))
    for sy in (-1, 1):
        for k in range(12):
            yy = sy*(38 + k*6.5) + (sy*3.2 if sy > 0 else -3.2); zz = 1.0 + k*1.85
            for xx in [a for a in [i_ * 2.0 - 56 for i_ in range(58)]]:
                if R_.random() < 0.93: pts.append((xx + R_.uniform(-0.35, 0.35), yy, zz, public(R_, seated=True), face_rot(0, -sy), 1.0))
    for k in range(14):
        zz = 2 + k*2.6; xx = 70 + k*6.5 + 3
        for yy in [i_ * 2.4 - 102 for i_ in range(86)]:
            tt = TIDX['chorus_w_0' if (yy < 0) else 'chorus_m_0'] if k > 3 else R_.choice((TIDX['band_violin'], TIDX['band_cello'], TIDX['band_wind'], TIDX['band_brass']))
            pts.append((xx, yy, zz, tt, face_rot(-1, 0), 1.0))
    pts.append((64, 0, 1.5, TIDX['conductor'], face_rot(1, 0), 1.0))
    for x0 in range(-790, 790, 2):          # denser gallery fronts
        if abs(x0) < 100: continue
        for sy in (-1, 1):
            for j in range(3): pts.append((x0 + R_.uniform(-0.8, 0.8), sy*(36 + j*2.4), GALLERY_FLOOR, public(R_), face_rot(0, -sy), 1.0))
    for x0 in range(-96, 97, 2):            # denser transept galleries
        for sy in (-1, 1):
            for j in range(3): pts.append((x0, sy*(158 - j*2.4), GALLERY_FLOOR, public(R_), face_rot(0, -sy), 1.0))
    # nave aisle fill (standing behind first rows)
    for x0 in range(-760, -80, 2):
        for sy in (-1, 1):
            for j in range(3):
                if R_.random() < 0.7:
                    pts.append((x0 + R_.uniform(-0.5, 0.5), sy*(4.5 + j*2.0), 0, public(R_), face_rot(0, -sy), R_.uniform(0.95, 1.03)))
    PP = people('ppl54_opening_day', O, pts)
    # terrace + park lawn densify (opening-day grounds packed R)
    ext = crowd_pts(R_, (-700, 700, yU + 6, -175), 8000, lambda x, y: UT, lambda r: public(r), lambda x, y: face_rot(0, 1))
    PE = people('ppl54_terrace_crowd', O, ext)
    park = crowd_pts(R_, (-650, 650, yU - BANK - 80, yU - BANK - 8), 9000, lambda x, y: LT, lambda r: public(r), lambda x, y: face_rot(0, 1))
    PK = people('ppl54_park_lawn_crowd', O, park)
    print('OPEN54 people', PP['people_count'], 'terrace', PE['people_count'], 'park', PK['people_count'])
    exec(open(os.path.join(_sd14, 'station.py')).read())

# =====================================================================================================================
if STATE in ('LATE11', 'WAR'):
    grime()
if STATE == 'LATE11':
    L = coll('SY-LATE_FestivalOfEmpire_1911__dated')
    wht = fmat('late11_render_white', (0.72, 0.7, 0.64), 0.8); stone = fmat('late11_stone_grey', (0.42, 0.4, 0.36), 0.85)
    roof = fmat('late11_slate_copper', (0.12, 0.2, 0.17), 0.6); rust = fmat('late11_red_brick', (0.32, 0.12, 0.07), 0.9)
    WH = MB('late11_pavilions_render', L, wht); ST_ = MB('late11_pavilions_stone', L, stone); RF = MB('late11_pavilions_roofs', L, roof)
    RL = MB('late11_all_red_route_rails', L, M.get('iron', rust)); TR = MB('late11_all_red_route_cars', L, rust)
    def pav_classical(cx, cy, w, d, h, dome=False):
        z = gzg(cx, cy) - 1
        WH.box(cx - w/2, cx + w/2, cy - d/2, cy + d/2, z, z + h)
        for k in range(8): ST_.cyl(cx - w*0.3 + k*w*0.6/7, cy + d/2 + 8, z + 4, z + h - 4, 1.4, 1.4, 10)     # portico columns
        ST_.box(cx - w*0.34, cx + w*0.34, cy + d/2, cy + d/2 + 10, z, z + 4); ST_.box(cx - w*0.34, cx + w*0.34, cy + d/2, cy + d/2 + 10, z + h - 4, z + h)
        RF.poly([(cx - w*0.34, cy + d/2 + 10, z + h), (cx + w*0.34, cy + d/2 + 10, z + h), (cx, cy + d/2 + 10, z + h + 10)])
        if dome: RF.cyl(cx, cy, z + h, z + h + w*0.22, w*0.16, 2, 16)
        return z
    def pav_gothic(cx, cy, w, d, h):
        z = gzg(cx, cy) - 1
        ST_.box(cx - w/2, cx + w/2, cy - d/2, cy + d/2, z, z + h)
        RF.poly([(cx - w/2, cy - d/2, z + h), (cx + w/2, cy - d/2, z + h), (cx + w/2, cy, z + h + 16), (cx - w/2, cy, z + h + 16)])
        RF.poly([(cx - w/2, cy, z + h + 16), (cx + w/2, cy, z + h + 16), (cx + w/2, cy + d/2, z + h), (cx - w/2, cy + d/2, z + h)])
        ST_.box(cx - 11, cx + 11, cy + d/2 - 4, cy + d/2 + 18, z, z + h*2.3)                                  # central tower
        RF.cyl(cx, cy + d/2 + 7, z + h*2.3, z + h*2.3 + 28, 10, 0.5, 4)
        return z
    # three-quarter-scale replicas of Dominion parliament buildings in the grounds (R: festival accounts; forms, sites I/U)
    pavs = [('Canada', pav_gothic(-520, -1300, 180, 70, 40)), ('Australia', pav_classical(520, -1300, 160, 70, 42, True)),
            ('South Africa', pav_classical(-300, -1560, 150, 64, 38, True)), ('New Zealand', pav_classical(300, -1560, 110, 54, 32))]
    # 'All-Red Route' railway loop round the replicas (R that it existed; route I)
    loop = []
    for k in range(120):
        a = 2*math.pi*k/120; x = 760*math.cos(a); y = -1420 + 300*math.sin(a); loop.append((x, y, gzg(x, y) + 0.4))
    for i in range(len(loop)):
        p0, p1 = loop[i], loop[(i + 1) % len(loop)]
        for d in (-1.2, 1.2): RL.strut((p0[0], p0[1] + d, p0[2]), (p1[0], p1[1] + d, p1[2]), 0.25, 0.3)
    for j in range(6):
        p = loop[30 + j*2]; TR.box(p[0] - 4, p[0] + 4, p[1] - 3, p[1] + 3, p[2] + 1, p[2] + 6)
    FL = {k: MB('late11_flags_' + k, L, fmat('late11_flag_' + k, c)) for k, c in (('red', (0.45, 0.03, 0.03)), ('white', (0.8, 0.8, 0.76)), ('blue', (0.03, 0.06, 0.25)))}
    POLE = MB('late11_flagpoles', L, fmat('late11_pole_white', (0.7, 0.7, 0.66), 0.6))
    for i, x in enumerate(range(-768, 769, 96)):
        if abs(x) < 72: continue
        flag(POLE, [FL['red'], FL['white'], FL['blue']] if i % 2 else [FL['blue'], FL['red']], x, 0, NAVE_CROWN, 26, 14, 9, seed=i)
    for i, x in enumerate(range(-640, 641, 64)):   # flag line along the upper terrace balustrade
        flag(POLE, [FL['red'], FL['white'], FL['blue']] if i % 3 == 0 else [FL['red']] if i % 3 == 1 else [FL['blue']], x, yU + 3, UT, 30, 9, 6, seed=i*0.7)
    for p in pavs: pass
    for m_ in (WH, ST_, RF, RL, TR, POLE, *FL.values()): m_.done()
    cam('CAM_CP049_worn_garden_front_35mm', (-300, yU + 20, UT + EYE), (120, -157, 70), 35)
    cam('CAM_CP053_festival_of_empire_35mm', (0, -1040, gzp(0, -1040) + EYE), (-420, -1330, gzg(-420, -1330) + 45), 35)
    cam('CAM_CP053_empire_pavilions_wide_35mm', (60, -1900, gzg(60, -1900) + EYE + 20), (0, -900, 30), 35)
    pts = crowd_pts(R_, (-700, 700, yU + 6, -175), 1200, lambda x, y: UT, lambda r: public11(r), None)
    pts += crowd_pts(R_, (-800, 800, -1750, -1080), 3000, lambda x, y: gzg(x, y), lambda r: public11(r), None)
    pts += crowd_pts(R_, (-600, 600, yL + 6, yU - BANK - 4), 900, lambda x, y: LT, lambda r: public11(r), None)
    PL = people('ppl11_festival_crowd', L, pts)
    print('LATE11 people', PL['people_count'])

# =====================================================================================================================
if STATE == 'WAR':
    Wc = coll('SY-WAR_HMS_CrystalPalace_1914-18__dated')
    FL = {k: MB('war_flags_' + k, Wc, fmat('war_flag_' + k, c)) for k, c in (('red', (0.45, 0.03, 0.03)), ('white', (0.82, 0.82, 0.78)), ('blue', (0.03, 0.06, 0.25)))}
    POLE = MB('war_masts', Wc, fmat('war_mast_white', (0.72, 0.72, 0.68), 0.6))
    # White Ensign (white field, red St George cross: approximated as white/red/white bands, I) on the transept and a
    # dressed 'ship's' mast with yard on the upper terrace (depot ritual: I)
    flag(POLE, [FL['white'], FL['red'], FL['white']], 0, 0, CT_CROWN, 34, 18, 12)
    flag(POLE, [FL['white'], FL['red'], FL['white']], 0, -250, UT, 80, 14, 9)
    POLE.box(-30, 30, -250.5, -249.5, UT + 64, UT + 65.2)
    for m_ in (POLE, *FL.values()): m_.done()
    cam('CAM_CP056_terrace_drill_35mm', (-440, -300, UT + EYE), (40, -235, UT + 14), 35)
    cam('CAM_CP056_nave_drill_gallery_28mm', (-340, 38, GALLERY_FLOOR + EYE), (-130, -6, 0), 28)
    cam('CAM_CP056_ranks_50mm', (-150, -216, UT + EYE), (-60, -250, UT + 5), 50)
    pts = []
    # companies on the upper terrace: 8 blocks of 6 ranks x 16 files (D-R14-W1, I: numbers/formation U)
    for b in range(8):
        bx0 = -330 + (b % 4) * 170; by0 = -205 - (b // 4) * 75
        for r_ in range(6):
            for c_ in range(16):
                pts.append((bx0 + c_*3.0 + R_.uniform(-0.15, 0.15), by0 - r_*4.0, UT, TIDX['rating_blue'] if b % 3 else TIDX['rating_white'], face_rot(0, 1), R_.uniform(0.96, 1.03)))
        pts.append((bx0 + 22, by0 + 12, UT, TIDX['courtier_blk'], face_rot(0, -1), 1.0))        # instructor (officer, I)
    # squads in the nave (wet-weather drill, I)
    for b in range(4):
        bx0 = -300 + b*60
        for r_ in range(4):
            for c_ in range(10): pts.append((bx0 + c_*3.2, -12 + r_*5, 0, TIDX['rating_blue'], face_rot(1, 0) if b % 2 else face_rot(0, 1), 1.0))
    for k in range(240):
        x = R_.uniform(-700, 700); y = R_.uniform(yL + 10, yU - BANK - 6); pts.append((x, y, LT, TIDX['rating_blue'] if R_.random() < 0.8 else R_.choice(ED_M), R_.uniform(-3, 3), 1.0))
    PW = people('ppl15_rnd_ratings', Wc, pts)
    print('WAR people', PW['people_count'])
