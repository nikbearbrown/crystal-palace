# r15 SY60 High Level station + vaulted tiled subway under Crystal Palace Parade, c.1865 (CP046).
# Exec'd from build.py when STATE=='SY60'. Shares build namespace (MB, mat, f, coll, cam, people, EYE, ...).
# Units: feet. Evidence thin: no measured HL plans in repo -> forms I/U, graded in DEPARTURES r15.
# Do NOT confuse with Low Level (CP036 / station.py). Subway is 1860s, not 1854.
import math, random
from mathutils import Vector

R60 = random.Random(1865)
HL = coll('SY60_HighLevel_station_and_subway__1865')

# ---- materials ----
def fmat(n, c, r=0.7, m=0.0):
    return mat(n, c, r, m) if n not in bpy.data.materials else bpy.data.materials[n]

brick = fmat('hl_stock_brick', (0.32, 0.20, 0.13), 0.9)
stone = fmat('hl_platform_stone', (0.45, 0.42, 0.38), 0.85)
iron = M.get('iron') or fmat('hl_iron', (0.12, 0.12, 0.13), 0.5, 0.3)
glass_r = M.get('glass_roof') or fmat('hl_glass_roof', (0.78, 0.84, 0.82), 0.05)
ballast = fmat('hl_ballast', (0.18, 0.16, 0.14), 0.95)
timber = fmat('hl_timber', (0.28, 0.20, 0.12), 0.8)
road = fmat('hl_parade_macadam', (0.22, 0.22, 0.20), 0.95)
cream = fmat('hl_vault_cream', (0.78, 0.72, 0.58), 0.85)
redb = fmat('hl_vault_red', (0.42, 0.12, 0.08), 0.85)
blackb = fmat('hl_vault_black', (0.08, 0.07, 0.07), 0.7)
tile_floor = fmat('hl_encaustic_floor', (0.55, 0.28, 0.12), 0.6)

# Patterned vault material: cream ground with red/black geometric bands (Byzantine subway look; period photos R existence; exact motif U)
def vault_mat(name):
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    b = n['Principled BSDF']
    tc = n.new('ShaderNodeTexCoord'); sep = n.new('ShaderNodeSeparateXYZ'); l.new(tc.outputs['Object'], sep.inputs[0])
    # stripes along X (length) every 2 ft cream/red; black bands every 8 ft; vertical rings along Y every 3 ft
    def band(comp, period, width):
        pp = n.new('ShaderNodeMath'); pp.operation = 'PINGPONG'; pp.inputs[1].default_value = f(period)/2
        l.new(sep.outputs[comp], pp.inputs[0])
        cmp = n.new('ShaderNodeMath'); cmp.operation = 'LESS_THAN'; cmp.inputs[1].default_value = f(width)
        l.new(pp.outputs[0], cmp.inputs[0]); return cmp
    red = band('X', 4.0, 0.55)
    blk = band('X', 16.0, 0.35)
    ring = band('Y', 6.0, 0.4)
    # mix cream -> red -> black
    mx1 = n.new('ShaderNodeMix'); mx1.data_type = 'RGBA'
    l.new(red.outputs[0], [x for x in mx1.inputs if x.identifier == 'Factor_Float'][0])
    [x for x in mx1.inputs if x.identifier == 'A_Color'][0].default_value = (0.78, 0.72, 0.58, 1)
    [x for x in mx1.inputs if x.identifier == 'B_Color'][0].default_value = (0.42, 0.12, 0.08, 1)
    mx2 = n.new('ShaderNodeMix'); mx2.data_type = 'RGBA'
    l.new(blk.outputs[0], [x for x in mx2.inputs if x.identifier == 'Factor_Float'][0])
    l.new([x for x in mx1.outputs if x.identifier == 'Result_Color'][0], [x for x in mx2.inputs if x.identifier == 'A_Color'][0])
    [x for x in mx2.inputs if x.identifier == 'B_Color'][0].default_value = (0.08, 0.07, 0.07, 1)
    mx3 = n.new('ShaderNodeMix'); mx3.data_type = 'RGBA'
    l.new(ring.outputs[0], [x for x in mx3.inputs if x.identifier == 'Factor_Float'][0])
    l.new([x for x in mx2.outputs if x.identifier == 'Result_Color'][0], [x for x in mx3.inputs if x.identifier == 'A_Color'][0])
    [x for x in mx3.inputs if x.identifier == 'B_Color'][0].default_value = (0.10, 0.09, 0.08, 1)
    l.new([x for x in mx3.outputs if x.identifier == 'Result_Color'][0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.82
    return m
vmat = vault_mat('hl_vault_patterned_brick')

# ---- placement (Parade / +Y side). Palace west facade ~ y=+156; CT west proj to ~180. ----
# Station beyond Parade road. Layout U (no HL plan in repo). Subway under Parade: R existence.
ZS = -2.0                    # rail / platform datum (I: near palace GF)
ROAD_Z = 4.0                 # Parade road deck (I)
SUB_Z = -14.0                # subway floor (I: under road)
SUB_CROWN = -2.0             # vault crown under road (I)
SUB_W = 18.0                 # clear width (I; surviving subway ~5-6 m)
ST_X0, ST_X1 = -220.0, 220.0
ST_Y0, ST_Y1 = 300.0, 400.0  # train shed
BOOK_Y0, BOOK_Y1 = 260.0, 300.0  # booking hall / subway head
# subway tunnel: from booking hall south toward palace, under Parade, to palace exit ~ y=190
SUB_Y0, SUB_Y1 = 190.0, 268.0
PARADE_Y0, PARADE_Y1 = 200.0, 260.0

# flatten park under station + clear trees
_ps = bpy.data.objects.get('park_slope')
if _ps:
    for v in _ps.data.vertices:
        x, y = v.co.x / F, v.co.y / F
        if ST_X0 - 40 < x < ST_X1 + 40 and ST_Y1 + 20 > y > PARADE_Y0 - 10:
            v.co.z = f(ZS - 0.5)
    _ps.data.update()
for o in list(bpy.data.objects):
    if o.name.startswith('PLACEHOLDER_park_tree') and o.type == 'MESH':
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        cxx = sum(v.x for v in bb)/8/F; cyy = sum(v.y for v in bb)/8/F
        if ST_X0 - 50 < cxx < ST_X1 + 50 and PARADE_Y0 - 20 < cyy < ST_Y1 + 40:
            bpy.data.objects.remove(o, do_unlink=True)

# ---- Parade road deck ----
RD = MB('hl_parade_road', HL, road)
RD.box(ST_X0 - 30, ST_X1 + 30, PARADE_Y0, PARADE_Y1, ROAD_Z - 1.0, ROAD_Z)
# keep a slot over the subway (no fill in the tunnel corridor) — road is a deck above
RD.done()

# ---- High Level train shed (two-span, brick sides; form I/U) ----
SR = MB('hl_shed_roof_glass', HL, glass_r)
SF = MB('hl_shed_ironwork', HL, iron)
SB = MB('hl_shed_brick', HL, brick)
SP = MB('hl_platforms', HL, stone)
BL = MB('hl_ballast', HL, ballast)
RL = MB('hl_rails', HL, iron)
EAVE, RIDGE = ZS + 22, ZS + 34
for yw in (ST_Y0, ST_Y1):
    SB.box(ST_X0 - 2, ST_X1 + 2, yw - 1.5, yw + 1.5, ZS - 1, EAVE)
SB.box(ST_X0 - 2, ST_X0, ST_Y0, ST_Y1, ZS - 1, EAVE)
SB.box(ST_X1, ST_X1 + 2, ST_Y0, ST_Y1, ZS - 1, EAVE)
yc = (ST_Y0 + ST_Y1) / 2
for (ya, yb) in ((ST_Y0, yc), (yc, ST_Y1)):
    ym = (ya + yb) / 2
    SR.poly([(ST_X0, ya, EAVE), (ST_X1, ya, EAVE), (ST_X1, ym, RIDGE), (ST_X0, ym, RIDGE)])
    SR.poly([(ST_X0, ym, RIDGE), (ST_X1, ym, RIDGE), (ST_X1, yb, EAVE), (ST_X0, yb, EAVE)])
    for x0 in range(int(ST_X0), int(ST_X1) + 1, 24):
        SF.strut((x0, ya, EAVE), (x0, ym, RIDGE), 0.55, 0.8)
        SF.strut((x0, ym, RIDGE), (x0, yb, EAVE), 0.55, 0.8)
        SF.box(x0 - 0.3, x0 + 0.3, ya, yb, EAVE - 0.5, EAVE)
    SF.box(ST_X0, ST_X1, ym - 0.35, ym + 0.35, RIDGE - 0.5, RIDGE)
for x0 in range(int(ST_X0) + 24, int(ST_X1), 24):
    SF.cyl(x0, yc, ZS + 2, EAVE, 0.5, 0.4, 8)
# platforms + tracks (U layout: side + island)
plats = [(ST_Y0 + 1.5, ST_Y0 + 22), (yc - 10, yc + 10), (ST_Y1 - 22, ST_Y1 - 1.5)]
tracks = [ST_Y0 + 30, ST_Y1 - 30]
for (pa, pb) in plats:
    SP.box(ST_X0 + 8, ST_X1 - 8, pa, pb, ZS, ZS + 3)
for yt in tracks:
    BL.box(ST_X0 + 4, ST_X1 - 4, yt - 5, yt + 5, ZS - 0.5, ZS + 0.2)
    for d in (-2.35, 2.35):
        RL.box(ST_X0 + 4, ST_X1 - 4, yt + d - 0.12, yt + d + 0.12, ZS + 0.2, ZS + 0.7)

# ---- Booking hall (head of subway) ----
BH = MB('hl_booking_hall', HL, brick)
BF = MB('hl_booking_floor', HL, timber)
BR = MB('hl_booking_roof', HL, stone)
BF.box(-40, 40, BOOK_Y0, BOOK_Y1, ZS, ZS + 0.4)
BH.box(-42, -40, BOOK_Y0, BOOK_Y1, ZS, ZS + 18)
BH.box(40, 42, BOOK_Y0, BOOK_Y1, ZS, ZS + 18)
BH.box(-42, 42, BOOK_Y1 - 1.5, BOOK_Y1, ZS, ZS + 18)
# open doorway into subway at BOOK_Y0
BH.box(-42, -SUB_W/2 - 1, BOOK_Y0, BOOK_Y0 + 1.5, ZS, ZS + 18)
BH.box(SUB_W/2 + 1, 42, BOOK_Y0, BOOK_Y0 + 1.5, ZS, ZS + 18)
BH.box(-SUB_W/2 - 1, SUB_W/2 + 1, BOOK_Y0, BOOK_Y0 + 1.5, ZS + 12, ZS + 18)  # lintel
BR.box(-44, 44, BOOK_Y0 - 2, BOOK_Y1 + 2, ZS + 18, ZS + 20)

# ---- Vaulted tiled subway under the Parade (the CP046 hero) ----
# Barrel vault of patterned brick; octagonal piers with cream/red rings; tiled floor.
SV = MB('hl_subway_vault_patterned', HL, vmat)
SW = MB('hl_subway_walls', HL, cream)
SC_ = MB('hl_subway_columns', HL, redb)
SFLOOR = MB('hl_subway_floor_tiles', HL, tile_floor)
# floor
SFLOOR.box(-SUB_W/2, SUB_W/2, SUB_Y0, SUB_Y1, SUB_Z - 0.4, SUB_Z)
# side walls up to springing
SPRING = SUB_Z + 8.0
for s in (-1, 1):
    SW.box(s * SUB_W/2 - (0.8 if s < 0 else 0), s * SUB_W/2 + (0 if s < 0 else 0.8),
           SUB_Y0, SUB_Y1, SUB_Z, SPRING)
# barrel vault as faceted half-cylinder polys along Y (I form; surviving subway is a series of groin/barrel bays)
BAYS = 12
bay_len = (SUB_Y1 - SUB_Y0) / BAYS
for i in range(BAYS):
    ya = SUB_Y0 + i * bay_len; yb = ya + bay_len
    # 8-segment semicircle from left spring to right
    segs = 10
    pts_a, pts_b = [], []
    for k in range(segs + 1):
        a = math.pi * k / segs  # 0..pi
        x = -SUB_W/2 * math.cos(a)
        z = SPRING + (SUB_CROWN - SPRING) * math.sin(a)  # wait: cos from -1 to 1 gives x; for vault we want x from -W/2 to W/2, z from SPRING up to CROWN
        # redo: a from 0 (left) to pi (right)
        x = (-SUB_W/2) * math.cos(a)   # -W/2 .. +W/2
        z = SPRING + (SUB_CROWN - SPRING) * math.sin(a)
        # sin(0)=0, sin(pi/2)=1, sin(pi)=0 -> good for semicircle rise
        pts_a.append((x, ya, z)); pts_b.append((x, yb, z))
    for k in range(segs):
        SV.poly([pts_a[k], pts_a[k+1], pts_b[k+1], pts_b[k]])
    # pier / column every bay on centreline sides
    for s in (-1, 1):
        cx = s * (SUB_W/2 - 1.2)
        SC_.cyl(cx, ya + 0.4, SUB_Z, SPRING, 0.55, 0.5, 8)
        # cream ring capitals
        SC_.box(cx - 0.7, cx + 0.7, ya + 0.1, ya + 0.7, SPRING - 0.3, SPRING + 0.15)

# palace-side exit pavilion (emergence toward the huge palace — the scale change)
EX = MB('hl_subway_exit_pavilion', HL, stone)
EX.box(-SUB_W/2 - 4, SUB_W/2 + 4, SUB_Y0 - 8, SUB_Y0, SUB_Z, SUB_Z + 14)
EX.box(-SUB_W/2 - 4, -SUB_W/2, SUB_Y0 - 8, SUB_Y0, SUB_Z, ROAD_Z + 2)
EX.box(SUB_W/2, SUB_W/2 + 4, SUB_Y0 - 8, SUB_Y0, SUB_Z, ROAD_Z + 2)
# steps up from subway floor toward palace GF (z=0)
nstep = 8
for k in range(nstep):
    t0 = k / nstep; t1 = (k + 1) / nstep
    z0 = SUB_Z + t0 * (0 - SUB_Z); z1 = SUB_Z + t1 * (0 - SUB_Z)
    yb = SUB_Y0 - 8 - k * 1.4; ya = yb - 1.4
    SFLOOR.box(-SUB_W/2 + 1, SUB_W/2 - 1, ya, yb, z0 - 0.3, z1)

for m_ in (SR, SF, SB, SP, BL, RL, BH, BF, BR, SV, SW, SC_, SFLOOR, EX):
    m_.done()

# ---- Victorian passengers (PPL-VIC via people57 templates) ----
# people() available only after people57 exec — build.py runs people57 before high_level for SY60
pts = []
# platform crowd
for i in range(80):
    x = R60.uniform(ST_X0 + 20, ST_X1 - 20)
    y = R60.choice([R60.uniform(plats[0][0]+1, plats[0][1]-1),
                    R60.uniform(plats[1][0]+1, plats[1][1]-1),
                    R60.uniform(plats[2][0]+1, plats[2][1]-1)])
    pts.append((x, y, ZS + 3, public(R60), face_rot(0, -1 if y > yc else 1), R60.uniform(0.96, 1.03)))
# booking hall
for i in range(40):
    pts.append((R60.uniform(-35, 35), R60.uniform(BOOK_Y0 + 4, BOOK_Y1 - 4), ZS + 0.4,
                public(R60), face_rot(0, -1), R60.uniform(0.97, 1.02)))
# subway passengers walking toward palace (face -Y)
for i in range(55):
    x = R60.uniform(-SUB_W/2 + 2, SUB_W/2 - 2)
    y = R60.uniform(SUB_Y0 + 6, SUB_Y1 - 6)
    pts.append((x, y, SUB_Z, public(R60), face_rot(0, -1), R60.uniform(0.97, 1.02)))
# emerging at exit toward palace
for i in range(25):
    pts.append((R60.uniform(-10, 10), R60.uniform(SUB_Y0 - 18, SUB_Y0 - 6), 0.2,
                public(R60), face_rot(0, -1), 1.0))
if 'people' in dir():
    PL = people('ppl60_hl_passengers', HL, pts)
    print('SY60 people', PL["people_count"])
else:
    print('SY60 WARNING: people() not available')


# ---- subway lighting (vault is underground; sun alone leaves CP046 black) ----
def _sub_light(name, y_ft, energy=400):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.size = f(4); ld.shape = 'RECTANGLE'
    ld.size_y = f(2); ld.color = (1.0, 0.92, 0.78)
    o = bpy.data.objects.new(name, ld); HL.objects.link(o)
    o.location = (0, f(y_ft), f(SUB_CROWN - 1.5))
    o.rotation_euler = (0, 0, 0); return o
for _i, _y in enumerate(range(int(SUB_Y0) + 12, int(SUB_Y1) - 4, 18)):
    _sub_light(f'hl_subway_light_{_i}', _y, 550)
# soft fill at exit pavilion
_sub_light('hl_subway_exit_fill', SUB_Y0 - 4, 300)

# ---- cameras CP046 (28 mm; establish station approach, walk under vaults, exit) ----
# eye height 1.6 m; 36 mm sensor via cam(); no roll
cam('CAM_CP046_hl_approach_28mm', (0, PARADE_Y0 + 10, ROAD_Z + EYE), (0, BOOK_Y1 + 20, ZS + 18), 28)
# start of vault walk (station side of subway)
_c = cam('CAM_CP046_subway_walk_28mm', (0, SUB_Y1 - 8, SUB_Z + EYE), (0, SUB_Y0 + 10, SUB_Z + 5), 28)
_c.location = [f(v) for v in (0, SUB_Y1 - 8, SUB_Z + EYE)]; _c.keyframe_insert('location', frame=1)
_c.location = [f(v) for v in (0, SUB_Y1 - 8 - 10.0/F, SUB_Z + EYE)]; _c.keyframe_insert('location', frame=120)  # 10 m walk
cam('CAM_CP046_subway_mid_28mm', (0, (SUB_Y0 + SUB_Y1)/2, SUB_Z + EYE), (0, SUB_Y0, SUB_Z + 4), 28)
cam('CAM_CP046_subway_exit_28mm', (0, SUB_Y0 - 6, SUB_Z + EYE + 1), (0, SUB_Y0 - 40, 8), 28)  # emerge toward palace
cam('CAM_CP046_palace_emergence_35mm', (0, SUB_Y0 - 30, EYE + 2), (0, 0, 80), 35)

print('SY60 High Level + subway OK', 'subway', SUB_Y0, '..', SUB_Y1, 'station', ST_Y0, '..', ST_Y1)
