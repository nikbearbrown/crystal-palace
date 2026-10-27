# r14 G-STATION (CP036): Crystal Palace (Low Level) station of the West End of London & Crystal Palace Railway, opened
# with the palace in June 1854 (R), and the glazed covered way (the 720 ft 'colonnade', R: guide p.35) climbing from
# it to the south wing. Exec'd from eras.py (OPEN54) - shares the build.py namespace.
# The r01-r13 colonnade was a flat 720 ft tube at wing-basement level that ended ~70 ft above the park; here it is
# rebuilt bay by bay following the ground, stepping down the slope (I) to a terminus train shed (layout/form U:
# no plan of the 1854 station in the repo; the surviving Low Level building is Driver's 1870s rebuild - not used).
SC = coll('SY54_LowLevel_station_and_covered_way__1854')
kill('colonnade_roof', 'colonnade_frame')
CWX = -WING_CX - WING_W/2 - 12            # same line as before (route U)
CW_Y0 = WING_Y0 - WING_LEN + 60           # -614: joins the south wing (as r01)
CW_Y1 = CW_Y0 - COLONNADE_LEN             # -1334 (720 ft, R)
ZS = round(gzp(CWX, CW_Y1) - 2.0, 1)      # station rail/platform datum (I)
SH_X0, SH_X1, SH_Y0, SH_Y1 = -1130.0, -650.0, -1350.0, -1440.0
# --- flatten the park under the station + clear beds/paths/trees there ---
_ps = bpy.data.objects.get('park_slope')
if _ps:
    for v in _ps.data.vertices:
        x, y = v.co.x / FT, v.co.y / FT
        if SH_X0 - 40 < x < SH_X1 + 120 and SH_Y1 - 30 < y < SH_Y0 + 14: v.co.z = f(ZS - 0.5)
    _ps.data.update()
for nm in ('flower_beds', 'park_paths_gravel', 'parterre_grass'):
    clip(nm, lambda x, y, z: SH_X0 - 50 < x < SH_X1 + 130 and SH_Y1 - 40 < y < SH_Y0 + 20 or (abs(x - CWX) < 18 and CW_Y1 < y < CW_Y0))
for o in list(bpy.data.objects):
    if o.name.startswith('PLACEHOLDER_park_tree') and o.type == 'MESH':
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]; cxx = sum(v.x for v in bb)/8/FT; cyy = sum(v.y for v in bb)/8/FT
        if (SH_X0 - 60 < cxx < SH_X1 + 140 and SH_Y1 - 50 < cyy < SH_Y0 + 40) or (abs(cxx - CWX) < 40 and CW_Y1 - 10 < cyy < CW_Y0): kill_obj(o)
glass_r = M['glass_roof']; glass_w = M['glass_wall']; iron = M['iron']
brick = fmat('station_stock_brick', (0.3, 0.2, 0.13), 0.9); stone_ = fmat('station_platform_stone', (0.42, 0.4, 0.36), 0.85)
ballast = fmat('station_ballast', (0.18, 0.16, 0.14), 0.95); timber = fmat('station_floor_boards', (0.3, 0.22, 0.14), 0.8)
CR = MB('covered_way_roof_glass', SC, glass_r); CG = MB('covered_way_side_glass', SC, glass_w); CF = MB('covered_way_ironwork', SC, iron)
CFL = MB('covered_way_floor_steps', SC, timber); CW = MB('covered_way_dado', SC, brick)
y = CW_Y0; prevz = None; cw_floor = []
while y > CW_Y1 + 0.01:
    ya, yb = y - BAY, y
    zf = min(-BD - 10, gzp(CWX, (ya + yb)/2) + 0.5)
    if prevz is not None and zf < prevz - 6: zf = prevz - 6        # landings at most a flight apart (I)
    cw_floor.append(((ya + yb)/2, zf))
    CFL.box(CWX - 12, CWX + 12, ya, yb, zf - 1.5 if prevz is None else min(zf, prevz) - 1.5, zf)
    if prevz is not None and prevz - zf > 0.4:                      # flight of steps at the upper end of the bay
        n_ = int((prevz - zf) / 0.55) + 1
        for k in range(n_): CFL.box(CWX - 12, CWX + 12, yb - (k + 1)*1.1, yb, zf, prevz - (k + 1)*(prevz - zf)/n_ + 0.001)
    for xx in (CWX - 12, CWX + 12):
        CF.box(xx - 0.4, xx + 0.4, yb - 0.4, yb + 0.4, zf, zf + 16); CF.box(xx - 0.4, xx + 0.4, ya, yb, zf + 15.4, zf + 16)
        CW.box(xx - 0.5, xx + 0.5, ya, yb, zf, zf + 3)
        CG.poly([(xx, ya, zf + 3), (xx, yb, zf + 3), (xx, yb, zf + 15.4), (xx, ya, zf + 15.4)])
    CR.poly([(CWX - 12.5, ya, zf + 16), (CWX - 12.5, yb, zf + 16), (CWX, yb, zf + 22), (CWX, ya, zf + 22)])
    CR.poly([(CWX, ya, zf + 22), (CWX, yb, zf + 22), (CWX + 12.5, yb, zf + 16), (CWX + 12.5, ya, zf + 16)])
    CF.box(CWX - 12.5, CWX + 12.5, yb - 0.3, yb + 0.3, zf + 16, zf + 17)
    if prevz is not None and prevz > zf: CR.poly([(CWX - 12.5, yb, zf + 16), (CWX + 12.5, yb, zf + 16), (CWX + 12.5, yb, prevz + 16), (CWX - 12.5, yb, prevz + 16)])
    prevz = zf; y -= BAY
# --- train shed: brick side walls, two glazed pitched spans on iron columns (I) ---
SR = MB('station_shed_roof_glass', SC, glass_r); SF = MB('station_shed_ironwork', SC, iron); SB = MB('station_brickwork', SC, brick)
SP = MB('station_platforms', SC, stone_); BL = MB('station_track_ballast', SC, ballast); RLm = MB('station_rails', SC, iron)
EAVE, RIDGE = ZS + 24, ZS + 36
for yw in (SH_Y0, SH_Y1):
    for x0 in range(int(SH_X0), int(SH_X1), 24):
        if yw == SH_Y0 and x0 <= CWX + 12 and x0 + 24 >= CWX - 12: SB.box(x0, x0 + 24, yw - 1.5, yw + 1.5, ZS + 18, EAVE); continue   # covered-way doorway
        SB.box(x0, x0 + 24, yw - 1.5, yw + 1.5, ZS - 1, EAVE)
SB.box(SH_X0 - 2, SH_X0, SH_Y1, SH_Y0, ZS - 1, EAVE)   # buffer-end wall
yc = (SH_Y0 + SH_Y1) / 2
for (ya_, yb_) in ((SH_Y0, yc), (yc, SH_Y1)):
    ym = (ya_ + yb_) / 2
    SR.poly([(SH_X0, ya_, EAVE), (SH_X1, ya_, EAVE), (SH_X1, ym, RIDGE), (SH_X0, ym, RIDGE)])
    SR.poly([(SH_X0, ym, RIDGE), (SH_X1, ym, RIDGE), (SH_X1, yb_, EAVE), (SH_X0, yb_, EAVE)])
    for x0 in range(int(SH_X0), int(SH_X1) + 1, 24):
        SF.strut((x0, ya_, EAVE), (x0, ym, RIDGE), 0.6, 0.9); SF.strut((x0, ym, RIDGE), (x0, yb_, EAVE), 0.6, 0.9)
        SF.box(x0 - 0.3, x0 + 0.3, ya_, yb_, EAVE - 0.6, EAVE)
    SF.box(SH_X0, SH_X1, ym - 0.4, ym + 0.4, RIDGE - 0.6, RIDGE)
for x0 in range(int(SH_X0) + 24, int(SH_X1), 24): SF.cyl(x0, yc, ZS + 3, EAVE, 0.55, 0.45, 8)
# platforms (3 ft) and tracks (U layout: side platform under the covered way, island platform, two roads)
PLATS = [(SH_Y0 - 1.5, -1372.0), (-1386.0, -1404.0), (-1418.0, SH_Y1 + 1.5)]
TRACKS = [-1379.0, -1411.0]
for (pa, pb) in PLATS: SP.box(SH_X0 + 10, SH_X1, pb, pa, ZS, ZS + 3)
for yt in TRACKS:
    BL.box(SH_X0 + 4, -540, yt - 5, yt + 5, ZS - 0.6, ZS + 0.2)
    for d in (-2.35, 2.35): RLm.box(SH_X0 + 4, -540, yt + d - 0.12, yt + d + 0.12, ZS + 0.2, ZS + 0.75)
    SB.box(SH_X0 + 4, SH_X0 + 7, yt - 4, yt + 4, ZS, ZS + 3.5)     # buffer stop
# --- an arrived train on road 1: tank engine + 4-wheel carriages (forms I) ---
TB = MB('train_carriage_bodies', SC, fmat('train_carriage_brown', (0.2, 0.07, 0.04), 0.5)); TK = MB('train_black', SC, fmat('train_black_iron', (0.03, 0.03, 0.03), 0.45))
TG = MB('train_engine_green', SC, fmat('train_engine_green', (0.04, 0.14, 0.07), 0.4)); TRf = MB('train_roofs', SC, fmat('train_roof_grey', (0.3, 0.3, 0.29), 0.8))
def hcyl(mb, x0, x1, y, z, r, seg=12):
    ring = [(y + r*math.cos(2*math.pi*k/seg), z + r*math.sin(2*math.pi*k/seg)) for k in range(seg)]
    for k in range(seg):
        a, b = ring[k], ring[(k + 1) % seg]; mb.poly([(x0, a[0], a[1]), (x1, a[0], a[1]), (x1, b[0], b[1]), (x0, b[0], b[1])])
    mb.poly([(x0, a[0], a[1]) for a in reversed(ring)]); mb.poly([(x1, a[0], a[1]) for a in ring])
yt = TRACKS[0]; xe = SH_X0 + 12
TG.box(xe, xe + 5, yt - 4, yt + 4, ZS + 5, ZS + 13)                 # cab (open-backed, I)
hcyl(TG, xe + 5, xe + 22, yt, ZS + 8.2, 2.3); TK.cyl(xe + 20, yt, ZS + 10, ZS + 15.5, 0.9, 0.8, 10)   # boiler + chimney
TK.box(xe - 1, xe + 24, yt - 3.6, yt + 3.6, ZS + 3.2, ZS + 5.2)
for xw in (xe + 3, xe + 11, xe + 19): hcyl(TK, xw - 2.4, xw + 2.4, yt - 2.45, ZS + 3.0, 2.6, 10) if False else TK.box(xw - 2.5, xw + 2.5, yt - 2.6, yt + 2.6, ZS + 0.6, ZS + 5.6)
x = xe + 27
for c_ in range(9):
    TB.box(x, x + 23, yt - 3.9, yt + 3.9, ZS + 3.6, ZS + 10.6); TRf.poly([(x, yt - 4.1, ZS + 10.6), (x + 23, yt - 4.1, ZS + 10.6), (x + 23, yt, ZS + 11.6), (x, yt, ZS + 11.6)])
    TRf.poly([(x, yt, ZS + 11.6), (x + 23, yt, ZS + 11.6), (x + 23, yt + 4.1, ZS + 10.6), (x, yt + 4.1, ZS + 10.6)])
    for d in range(1, 3): TK.box(x + d*23/3 - 0.15, x + d*23/3 + 0.15, yt - 3.95, yt + 3.95, ZS + 3.6, ZS + 10.6)   # compartment divisions
    for xw in (x + 5, x + 18): TK.box(xw - 1.8, xw + 1.8, yt - 2.6, yt + 2.6, ZS + 0.6, ZS + 4.2)
    x += 25
for m_ in (CR, CG, CF, CFL, CW, SR, SF, SB, SP, BL, RLm, TB, TK, TG, TRf): m_.done()
# --- cameras, then arriving visitors ---
def cwz(yq):
    best = min(cw_floor, key=lambda t: abs(t[0] - yq)); return best[1]
cam('CAM_CP036_platform_arrival_28mm', (-700, -1395, ZS + 3 + EYE), (-1100, -1366, ZS + 9), 28)
cam('CAM_CP036_covered_way_28mm', (CWX + 4, -1318, cwz(-1318) + EYE), (CWX - 1, -1000, cwz(-1000) + 9), 28)
cam('CAM_CP036_station_exterior_35mm', (-560, -1580, gzp(-560, -1580) + EYE), (-930, -1080, ZS + 30), 35)
sp_ = []
for (pa, pb) in PLATS[:2]:
    for k in range(380 if pa > -1380 else 240):
        x_ = R_.uniform(SH_X0 + 40, SH_X1 - 20); y_ = R_.uniform(pb + 1.5, pa - 1.5)
        if pa > -1380 and R_.random() < 0.6: x_ = R_.uniform(CWX - 120, CWX + 60)        # heading for the covered way
        sp_.append((x_, y_, ZS + 3, public(R_), face_rot(CWX - x_, 1) + R_.uniform(-0.5, 0.5), R_.uniform(0.95, 1.04)))
for (ym, zf) in cw_floor:                                                                    # streaming up the covered way
    for k in range(12):
        sp_.append((CWX + R_.uniform(-10, 10), ym + R_.uniform(-11, 11), zf, public(R_), face_rot(R_.uniform(-0.2, 0.2), 1), R_.uniform(0.95, 1.04)))
PS = people('ppl54_station_visitors', SC, sp_)
print('STATION ZS', ZS, 'covered way bays', len(cw_floor), 'floor', cw_floor[0][1], '->', cw_floor[-1][1], 'visitors', PS['people_count'])
