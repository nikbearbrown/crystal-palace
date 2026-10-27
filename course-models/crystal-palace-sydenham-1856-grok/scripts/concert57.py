# r13 C-CONCERT (CP045): the Great Handel Festival, 15/17/19 June 1857, central transept (exec'd from build.py when
# SY_STATE=CONCERT57; shares its namespace). Units feet. Sources + grades: DEPARTURES r13 (D-R13-C*).
#  R  Grove 'Handel Festival' (Wikisource) / Wikipedia 'Handel Festival 1857': choir 2000, band 396, conductor
#     Michael Costa, grand organ built by Gray & Davison expressly for the occasion; screens + awning only from 1859.
#  B  orchestra breadth 216 ft (common figure for the Handel orchestra) -> nave + both inner aisles, y -108..108.
#  I  orchestra on the NORTH side of the crossing rising into the first nave bays, facing south (Trove 1857 puts the
#     royal box 'in the north corner of the transept immediately facing the orchestra' - orientation conflict, see D-R13-C02);
#     tier radii/rises, organ case design (four pipe towers after the later Negretti & Zambra photo 0595), rostrum.
#  U  dress colours, seating plan of the audience (~9,600 modelled), voice/instrument layout.
import math, random
CON = coll('SY57_HandelFestival_15-19Jun1857__dated')
HW = mat('handel_orchestra_stained_deal', (0.30, 0.19, 0.10), 0.7)   # U colour
CW_ = MB('handel_orchestra_tiers', CON, HW)
RISERS = mat('handel_orchestra_riser_red_baize', (0.28, 0.035, 0.03), 0.9)
RF_ = MB('handel_orchestra_riser_fronts', CON, RISERS)
PX, PY = 30.0, 0.0                    # amphitheatre focus (just behind the conductor), I
R0, DR, NROW = 40.0, 3.4, 28          # first row radius, row depth, rows (I: sized to seat 2,000 + 396)
Z0, DZ = 4.5, 1.5                     # stage height and rise per row (top row ~46 ft, I)
XMIN, YMAX = 60.0, 108.0
ORGAN_HALF, ORGAN_FRONT = 27.0, 158.0
def theta_max(r):
    c = (XMIN - PX)/r
    return min(math.acos(max(-1, min(1, c))), math.asin(min(1.0, YMAX/r)))
def sector(mb, r0, r1, z0, z1, n=48):
    """annular sector about (PX, PY) clipped to x>=XMIN, |y|<=YMAX, extruded z0..z1 (feet)"""
    t0, t1 = theta_max(r0), theta_max(r1)
    inner = [(PX + r0*math.cos(t), PY + r0*math.sin(t)) for t in [-t0 + 2*t0*i/n for i in range(n+1)]]
    outer = [(PX + r1*math.cos(t), PY + r1*math.sin(t)) for t in [t1 - 2*t1*i/n for i in range(n+1)]]
    ring = inner + outer
    bm = mb.bm
    B = [bm.verts.new((f(x), f(y), f(z0))) for x, y in ring]; T = [bm.verts.new((f(x), f(y), f(z1))) for x, y in ring]
    bm.faces.new(list(reversed(B))); bm.faces.new(T)
    for k in range(len(ring)):
        k1 = (k+1) % len(ring); bm.faces.new((B[k], B[k1], T[k1], T[k]))
    return inner, outer
ROWS = []
for k in range(NROW):
    r = R0 + DR*k; z = Z0 + DZ*k
    sector(CW_, r - DR/2, r + DR/2, 0.0, z)
    ROWS.append((r, z))
# stage apron in front of the first row (conductor's level), I
sector(CW_, 26.5, R0 - DR/2, 0.0, Z0 - 0.5)
# front rail + riser baize along the orchestra front
rail = MB('handel_orchestra_front_rail', CON, M['iron'])
tf = theta_max(26.5)
for i in range(40):
    t0_ = -tf + 2*tf*i/40; t1_ = -tf + 2*tf*(i+1)/40
    a_ = (PX + 26.5*math.cos(t0_), PY + 26.5*math.sin(t0_)); b_ = (PX + 26.5*math.cos(t1_), PY + 26.5*math.sin(t1_))
    RF_.poly([(a_[0]-0.05, a_[1], 0), (b_[0]-0.05, b_[1], 0), (b_[0]-0.05, b_[1], Z0-0.5), (a_[0]-0.05, a_[1], Z0-0.5)])
    rail.strut((a_[0], a_[1], Z0+2.9), (b_[0], b_[1], Z0+2.9), 0.15)
    rail.strut((a_[0], a_[1], Z0-0.5), (a_[0], a_[1], Z0+2.9), 0.1)
# side screens of the tiers are open framing in 1857 (no 1859 screens, R): plain timber cheeks only
for s in (-1, 1):
    CW_.box(XMIN, 172, s*YMAX - 0.4, s*YMAX + 0.4, 0, 3.0)
CW_.done(); RF_.done(); rail.done()

# --- Gray & Davison organ, 1857 (case design I/U; 4 pipe towers after 0595, which shows the later, rebuilt organ) ---
ORG = coll('SY57_GrayDavison_organ_1857__dated', parent=CON)
GILT = mat('organ_pipes_gilt', (0.75, 0.55, 0.22), 0.28, 1.0)
CASE = mat('organ_case_oak_dark', (0.12, 0.07, 0.035), 0.55)
oc = MB('organ_case_1857', ORG, CASE); op = MB('organ_front_pipes_1857', ORG, GILT)
zb = Z0 + DZ*(NROW-1) - 6                                # organ gallery floor (top tiers run to its foot), I
oc.box(ORGAN_FRONT, ORGAN_FRONT + 22, -ORGAN_HALF, ORGAN_HALF, 0, zb + 12)                    # impost / console stage
oc.box(ORGAN_FRONT - 0.6, ORGAN_FRONT + 22, -ORGAN_HALF - 0.6, ORGAN_HALF + 0.6, zb + 12, zb + 13.2)   # impost cornice
TOWERS = [-21.0, -8.0, 8.0, 21.0]
for ty in TOWERS:                                         # four round-fronted towers
    oc.box(ORGAN_FRONT + 0.5, ORGAN_FRONT + 8, ty - 4.2, ty + 4.2, zb + 13.2, zb + 50)
    oc.cyl(ORGAN_FRONT + 1.5, ty, zb + 50, zb + 52.5, 4.8, 4.8, seg=16)                          # tower cornice
    for c_ in range(4):                                                                        # battlement cresting
        oc.box(ORGAN_FRONT - 1.5 + 2.2*c_, ORGAN_FRONT - 0.3 + 2.2*c_, ty - 1.2, ty + 1.2, zb + 52.5, zb + 54)
    for p in range(7):                                                                         # tower pipes in a half-round
        a = math.pi*(p/6 - 0.5); px_, py_ = ORGAN_FRONT + 1.3 - 3.4*math.cos(a), ty + 3.4*math.sin(a)
        L = 30 - 1.5*abs(p - 3)
        op.cyl(px_, py_, zb + 14, zb + 16.5, 0.05, 0.42, seg=8)                                  # foot
        op.cyl(px_, py_, zb + 16.5, zb + 16.5 + L, 0.42, 0.42, seg=8)
for (ya, yb, hmax) in ((-16.5, -12.4, 22), (-3.6, 3.6, 30), (12.4, 16.5, 22)):                  # flats between the towers
    oc.box(ORGAN_FRONT + 2.5, ORGAN_FRONT + 9, ya, yb, zb + 13.2, zb + 18 + hmax + 4)
    oc.box(ORGAN_FRONT + 1.6, ORGAN_FRONT + 9, ya - 0.3, yb + 0.3, zb + 18 + hmax + 4, zb + 18 + hmax + 5.2)
    n = max(3, int((yb - ya)/0.95)); 
    for p in range(n):
        py_ = ya + (p + 0.5)*(yb - ya)/n; L = hmax - 6*abs((p + 0.5)/n - 0.5)
        op.cyl(ORGAN_FRONT + 2.2, py_, zb + 14, zb + 15.5, 0.05, 0.36, seg=8)
        op.cyl(ORGAN_FRONT + 2.2, py_, zb + 15.5, zb + 15.5 + L, 0.36, 0.36, seg=8)
oc.box(ORGAN_FRONT + 8, ORGAN_FRONT + 22, -ORGAN_HALF, ORGAN_HALF, zb + 13.2, zb + 46)            # swell box / body behind
oc.box(ORGAN_FRONT - 4, ORGAN_FRONT + 0.5, -3.0, 3.0, zb + 4, zb + 8)                          # console (organist faces it)
oc.done(); op.done()

# --- conductor's rostrum (Costa), royal box opposite, audience benches ---
RO = MB('costa_rostrum', CON, HW)
RO.box(PX + 18, PX + 23, -3, 3, 0, Z0 + 0.5); RO.box(PX + 22.5, PX + 23, -2.5, 2.5, Z0 + 0.5, Z0 + 3.6)   # desk front
RO.box(PX + 21.5, PX + 23, -1.4, 1.4, Z0 + 3.0, Z0 + 3.4); RO.done()
VEL = mat('royal_box_crimson_velvet', (0.32, 0.015, 0.03), 0.9)
GOLD = mat('royal_box_gilt_fringe', (0.7, 0.5, 0.15), 0.35, 1.0)
rb = MB('royal_box_1857', CON, VEL); rg = MB('royal_box_gilding', CON, GOLD); rw = MB('royal_box_structure', CON, HW)
RBX, RBZ = -60.0, GALLERY_FLOOR
rw.box(RBX - 14, RBX, -20, 20, RBZ - 1.2, RBZ)                                   # box floor projecting into the crossing
for yy in (-19, 19): rw.box(RBX - 0.6, RBX, yy - 0.6, yy + 0.6, 0, RBZ)          # posts down to the floor
rb.box(RBX - 0.5, RBX, -20, 20, RBZ, RBZ + 3.4)                                   # draped parapet
rg.box(RBX - 0.7, RBX + 0.1, -20.2, 20.2, RBZ + 3.3, RBZ + 3.7)
for yy in (-19, -6, 6, 19): rw.box(RBX - 0.9, RBX - 0.3, yy - 0.3, yy + 0.3, RBZ, RBZ + 13)
rb.box(RBX - 14, RBX + 0.4, -21, 21, RBZ + 13, RBZ + 14.2)                        # canopy
for i in range(28):                                                               # swagged valance
    y0_ = -21 + 42*i/28; y1_ = -21 + 42*(i+1)/28
    rb.poly([(RBX + 0.4, y0_, RBZ + 13), (RBX + 0.4, y1_, RBZ + 13), (RBX + 0.4, (y0_+y1_)/2, RBZ + 11.2)])
rg.box(RBX + 0.3, RBX + 0.6, -21, 21, RBZ + 12.8, RBZ + 13.1)
rb.poly([(RBX - 14, -21, RBZ + 14.2), (RBX + 0.4, -21, RBZ + 14.2), (RBX - 7, 0, RBZ + 18)])
rb.poly([(RBX - 14, 21, RBZ + 14.2), (RBX + 0.4, 21, RBZ + 14.2), (RBX - 7, 0, RBZ + 18)])
rb.poly([(RBX + 0.4, -21, RBZ + 14.2), (RBX + 0.4, 21, RBZ + 14.2), (RBX - 7, 0, RBZ + 18)])
rb.done(); rg.done(); rw.done()

def near_col(x, y, d=1.6):
    return any(abs(x - xc) < d for xc in xs_grid) and any(abs(y - yc) < d for yc in COL_Y)
# --- performers (GN instanced) ---
rng = random.Random(1857615)
pts = []
for k, (r, z) in enumerate(ROWS):
    band = k < 8
    pitch = 2.7 if band else 2.05
    tmx = theta_max(r) - 0.6/r
    n = int(2*tmx*r/pitch)
    for i in range(n):
        t = -tmx + 2*tmx*(i + 0.5)/n; x = PX + r*math.cos(t) + rng.uniform(-0.2, 0.2); y = PY + r*math.sin(t)
        if near_col(x, y) or (abs(y) < ORGAN_HALF + 1 and x > ORGAN_FRONT - 4.5): continue
        rot = face_rot(PX + 22 - x, -y) + rng.uniform(-0.12, 0.12)          # all face the conductor
        if band:
            if abs(y) > 0.62*r*math.sin(tmx) and k < 6: tk = 'band_cello' if rng.random() < 0.6 else 'band_bass'
            elif k >= 6 and abs(y) < 30: tk = 'band_brass' if k == 7 else 'band_wind'
            else: tk = 'band_violin'
        else:
            # voices: sopranos/altos (women) on the lower chorus rows and the sides, men above + in the centre (U)
            woman = (k < 17 and abs(y) > 18) or (k < 13) or (abs(y) > 0.8*r*math.sin(tmx) and k < 22)
            tk = rng.choice(('chorus_w_0', 'chorus_w_1')) if woman else 'chorus_m_0'
        pts.append((x, y, z, TIDX[tk], rot, rng.uniform(0.95, 1.04)))
pts.append((PX + 20.5, 0, Z0 + 0.5, TIDX['conductor'], face_rot(1, 0)))       # Michael Costa (form only; no likeness)
N_PERF = len(pts) - 1
# --- cameras (CP045), defined before the crowds so people() keeps a clear zone round each lens ---
cam('CAM_CP045_gallery_wide_28mm', (-63, 46, GALLERY_FLOOR + EYE), (110, -10, 30), 28)
cam('CAM_CP045_gallery_wide_b_28mm', (-72, -38, GALLERY_FLOOR + EYE), (110, 8, 30), 28)   # r13b: mid-bay at the gallery front, clear of the bracing
cam('CAM_CP045_floor_aisle_28mm', (-48, 0, EYE), (120, 0, 30), 28)
cam('CAM_CP045_from_organ_gallery_28mm', (140, 0, 70 + EYE), (-120, 0, 0), 28)   # r13b: on axis above the top tiers in front of the organ (Negretti reverse view, I)
cam('CAM_CP045_conductor_detail_50mm', (36, -30, Z0 + EYE), (62, 4, Z0 + 5), 50)
PERF = people('ppl57_performers_choir_band', CON, pts)
PERF['note'] = 'choir 2000 + band 396 (R); modelled count is what the tiers seat at the chosen pitch (I)'
# --- audience: transept floor + south nave/aisles on benches facing +X; gallery fronts standing; royal box ---
bench = MB('concert_benches', CON, HW)
apts = []
def seat_block(x0, x1, y0, y1, aisles, pitch_x=2.9, pitch_y=1.9, fill=0.96):
    x = x1
    while x > x0:
        segs = []; ya = y0
        for a0, a1 in sorted(aisles) + [(y1, y1)]:
            if a0 > ya: segs.append((ya, min(a0, y1)))
            ya = max(ya, a1)
        for s0, s1 in segs:
            if s1 - s0 < 2: continue
            bench.box(x - 0.7, x + 0.5, s0, s1, 0, 1.45)
            n = int((s1 - s0)/pitch_y)
            for i in range(n):
                y = s0 + (i + 0.5)*(s1 - s0)/n
                if rng.random() > fill or near_col(x, y, 1.4): continue
                apts.append((x - 0.2, y, 0.0, public(rng, seated=True), face_rot(1, 0) + rng.uniform(-0.25, 0.25), rng.uniform(0.95, 1.04)))
        x -= pitch_x
seat_block(-57, PX + 14, -150, 150, [(-4, 4), (-74, -70), (70, 74), (-110, -106), (106, 110)])
seat_block(-200, -64, -104, 104, [(-4, 4), (-37.5, -34.5), (34.5, 37.5), (-61, -59), (59, 61)])
bench.done()
# standing promenaders at the gallery fronts (nave edge, y = +-36 and +-60) south of the crossing, facing the orchestra
for s in (-1, 1):
    x = -66
    while x > -300:
        if not near_col(x, s*37, 1.0):
            apts.append((x, s*37.6, GALLERY_FLOOR, public(rng), face_rot(1, -s*0.6) + rng.uniform(-0.3, 0.3)))
        if rng.random() < 0.85 and not near_col(x, s*39.5, 1.0):
            apts.append((x + 0.9, s*39.6, GALLERY_FLOOR, public(rng), face_rot(1, -s*0.5) + rng.uniform(-0.3, 0.3)))
        x -= 2.2
# standing crowd along the transept sides (garden/Parade ends of the crossing), facing the orchestra
for (y0_, y1_) in ((-185, -155), (155, 185)):
    for i in range(700):
        x = rng.uniform(-56, 50); y = rng.uniform(y0_, y1_)
        apts.append((x, y, 0.0, public(rng), face_rot(PX + 60 - x, -y) + rng.uniform(-0.4, 0.4)))
# royal box party (anonymous; no likenesses)
for i, y in enumerate((-10, -5, 0, 5, 10)):
    apts.append((RBX - 3, y, RBZ, public(rng, seated=True, wfrac=0.5 if i != 2 else 1.0), face_rot(1, 0)))
    if i % 2 == 0: apts.append((RBX - 7, y + 1.5, RBZ, public(rng), face_rot(1, 0)))
N_AUD = len(apts)
AUD = people('ppl57_audience', CON, apts)
print('CONCERT57 performers', PERF['people_count'] - 1, 'audience', AUD['people_count'])

# --- cameras (CP045) ---
