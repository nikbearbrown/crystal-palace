"""CP044 CANDIDATE (2026-11-13): admission point at the ENTRANCE FROM RAILWAY STATION (plan 0205), SY-EARLY c.1856.

usage: blender -b rounds/sydenham-1856-r16.blend -P scripts/candidate_cp044_railway_entrance.py [-- out.blend]   (env CP044_NOSAVE=1: build in memory only)
Opens the live EARLY round, adds dated collection SY56_railway_entrance_admission__c1856 and moves
CAM_CP044_pay_desks_35mm from the nave palm garden to the railway entrance; adds CAM_CP044_maintenance_50mm.
Never writes the live round. Units: feet in this file (F converts), datum z=0 = palace main floor.
Departures: DEPARTURES.md D-SY-CP044-01..  (evidence grades B/R/I/U).
"""
import bpy, bmesh, math, sys, os, random
from mathutils import Vector, Matrix

F = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P
from cpl_people import person_mesh

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP044_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-1856-r16_cp044gate.blend')

BD = P.BASEMENT_DEPTH
ZF = -BD - 10                       # wing lower storey floor (build.py zb), -33.58 ft
XC = -P.WING_CX                     # south wing centre x = -860
XA, XB = XC - P.WING_W / 2, XC + P.WING_W / 2     # -878 / -842
YEND = P.WING_Y0 - P.WING_LEN       # -674 (wing end wall)
# Plan 0205 'ENTRANCE FROM RAILWAY STATION' cross, read off the plan at 2.887 px/ft (D-SY-CP044-01):
STEP_HW = 24.0                      # 48 ft wide neck/stub (138 px)
ARM_HW = 49.0                       # 98 ft cross arms (282 px)
Y_STEP0, Y_ARM0, Y_ARM1 = -578.0, -601.0, -649.0   # neck starts / arm north wall / arm south wall
H_ARM = 24.0                        # I: arm/stub wall height (one wing storey band 18 ft + clerestory)
Y_BAR = -598.0                      # admission barrier line, 3 ft inside the neck (I)

COLL = 'SY56_railway_entrance_admission__c1856'
col = bpy.data.collections.get(COLL) or bpy.data.collections.new(COLL)
if col.name not in [c.name for c in bpy.context.scene.collection.children]:
    bpy.context.scene.collection.children.link(col)
col['cp_state'] = 'SY-EARLY_c1856'
col['evidence'] = 'plan 0205 entrance label R; pay boxes/turnstiles/fittings I; family/staff U'

def mat(name, rgb, rough=0.7, metal=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    return m

M = dict(
    glass=bpy.data.materials['glass_wall'], groof=bpy.data.materials['glass_roof'],
    iron=bpy.data.materials['iron_painted_OJ'], ironp=bpy.data.materials['iron_exterior_pale'],
    boards=bpy.data.materials['boards_gapped'],
    oak=mat('cp044_grained_oak', (0.30, 0.17, 0.08), 0.55),
    paint=mat('cp044_board_green', (0.06, 0.16, 0.10), 0.6),
    gilt=mat('cp044_gilt_line', (0.62, 0.45, 0.16), 0.35, 0.8),
    castiron=mat('cp044_cast_iron_black', (0.03, 0.03, 0.035), 0.45, 0.6),
    brass=mat('cp044_brass', (0.62, 0.46, 0.20), 0.3, 1.0),
    tub=mat('cp044_tub_green', (0.10, 0.20, 0.12), 0.6),
    hoop=mat('cp044_tub_hoop', (0.08, 0.08, 0.08), 0.5, 0.7),
    soil=mat('cp044_soil', (0.10, 0.07, 0.05), 0.95),
    leaf=bpy.data.materials['foliage'], bark=bpy.data.materials['bark'],
    orange=mat('cp044_orange_fruit', (0.75, 0.30, 0.03), 0.5),
    ticket=mat('cp044_ticket_card', (0.85, 0.80, 0.62), 0.6),
    zinc=mat('cp044_zinc_can', (0.45, 0.47, 0.48), 0.4, 0.8),
    deal=mat('cp044_deal_ladder', (0.55, 0.42, 0.26), 0.8),
    pane=mat('cp044_pane', (0.75, 0.85, 0.88), 0.05),
    mat_coco=mat('cp044_coco_mat', (0.30, 0.22, 0.12), 0.95),
)
_pb = M['pane'].node_tree.nodes['Principled BSDF']
_pb.inputs['Transmission Weight'].default_value = 0.9; _pb.inputs['IOR'].default_value = 1.52

class MB:
    def __init__(self, name, m):
        self.name, self.bm = name, bmesh.new(); self.mats = [m]
    def box(self, x0, x1, y0, y1, z0, z1):
        r = bmesh.ops.create_cube(self.bm, size=1.0)
        bmesh.ops.transform(self.bm, matrix=Matrix.Translation(Vector(((x0+x1)/2, (y0+y1)/2, (z0+z1)/2)) * F)
                            @ Matrix.Diagonal(Vector((abs(x1-x0)*F, abs(y1-y0)*F, abs(z1-z0)*F, 1))), verts=r['verts'])
    def cyl(self, x, y, z0, z1, r0, r1=None, seg=16):
        r1 = r0 if r1 is None else r1
        res = bmesh.ops.create_cone(self.bm, cap_ends=True, segments=seg, radius1=r0*F, radius2=r1*F, depth=(z1-z0)*F)
        bmesh.ops.translate(self.bm, vec=Vector((x*F, y*F, (z0+z1)/2*F)), verts=res['verts'])
    def sphere(self, x, y, z, r, sub=2):
        res = bmesh.ops.create_icosphere(self.bm, subdivisions=sub, radius=r*F)
        bmesh.ops.translate(self.bm, vec=Vector((x*F, y*F, z*F)), verts=res['verts'])
    def strut(self, a, b, w):
        a, b = Vector(a), Vector(b); d = b - a; L = d.length
        res = bmesh.ops.create_cube(self.bm, size=1.0)
        q = d.to_track_quat('Z', 'Y')
        bmesh.ops.transform(self.bm, matrix=Matrix.Translation((a + b) / 2 * F) @ q.to_matrix().to_4x4()
                            @ Matrix.Diagonal(Vector((w*F, w*F, L*F, 1))), verts=res['verts'])
    def quad(self, pts):
        vs = [self.bm.verts.new(Vector(p) * F) for p in pts]; self.bm.faces.new(vs)
    def done(self):
        me = bpy.data.meshes.new(self.name); self.bm.to_mesh(me); self.bm.free()
        for m in self.mats: me.materials.append(m)
        o = bpy.data.objects.new(self.name, me); col.objects.link(o); return o

# ------------------------------------------------------------------ 1. open the wing walls into the cross
# The modelled wing is a plain glazed box to y=-674; plan 0205 shows the last ~96 ft as the cross-shaped entrance.
wg = bpy.data.objects['wings_glass']
bm = bmesh.new(); bm.from_mesh(wg.data); mw = wg.matrix_world
kill = []
for fc in bm.faces:
    c = mw @ fc.calc_center_median(); cx, cy = c.x / F, c.y / F
    if cx < -800 and (abs(cx - XA) < 1.0 or abs(cx - XB) < 1.0) and YEND - 1 < cy < Y_STEP0 + 1:
        kill.append(fc)
    elif cx < -800 and abs(cy - YEND) < 1.0 and XA - 1 < cx < XB + 1:
        kill.append(fc)        # wing end wall: replaced by the stub with the doorway
print('CP044 wing glass faces removed', len(kill))
# faces span the full wing length -> split them at the cross instead of deleting the whole wall
bm.free()
# robust approach: rebuild the two side walls of the south wing in pieces (glass is a single quad per wall)
bm = bmesh.new(); bm.from_mesh(wg.data)
side = []
for fc in bm.faces:
    c = mw @ fc.calc_center_median(); cx, cy = c.x / F, c.y / F
    if cx < -800 and ((abs(cx - XA) < 1.0 or abs(cx - XB) < 1.0) or abs(cy - YEND) < 1.0):
        side.append(fc)
zs = sorted({round((mw @ v.co).z / F, 3) for fc in side for v in fc.verts})
bmesh.ops.delete(bm, geom=side, context='FACES')
bm.to_mesh(wg.data); bm.free()
ZB_W, ZT_W = zs[0], zs[-1]
G = MB('cp044_wing_glass_rebuilt', M['glass'])
for xx in (XA, XB):                 # wing side walls kept north of the neck
    G.quad([(xx, Y_STEP0, ZB_W), (xx, P.WING_Y0, ZB_W), (xx, P.WING_Y0, ZT_W), (xx, Y_STEP0, ZT_W)])
    G.quad([(xx, YEND, ZF + H_ARM), (xx, Y_STEP0, ZF + H_ARM), (xx, Y_STEP0, ZT_W), (xx, YEND, ZT_W)])  # clerestory over the cross
# cross outline (plan 0205), walls glazed ZF..ZF+H_ARM, anticlockwise from the NW neck corner
O = [(XA, Y_STEP0), (XC - STEP_HW, Y_STEP0), (XC - STEP_HW, Y_ARM0), (XC - ARM_HW, Y_ARM0), (XC - ARM_HW, Y_ARM1),
     (XC - STEP_HW, Y_ARM1), (XC - STEP_HW, YEND), (XC + STEP_HW, YEND), (XC + STEP_HW, Y_ARM1), (XC + ARM_HW, Y_ARM1),
     (XC + ARM_HW, Y_ARM0), (XC + STEP_HW, Y_ARM0), (XC + STEP_HW, Y_STEP0), (XB, Y_STEP0)]
FR = MB('cp044_entrance_frame', M['ironp'])
DOORS = {(6, 7): (XC - 6, XC + 6), (3, 4): None}    # stub south wall: 12 ft doorway (I); west arm: colonnade
CX_COL = -P.WING_CX - P.WING_W / 2 - 12             # colonnade axis x (build.py)
for i in range(len(O) - 1):
    (x0, y0), (x1, y1) = O[i], O[i + 1]
    L = math.hypot(x1 - x0, y1 - y0); n = max(1, round(L / 8))
    openings = []
    if (i, i + 1) == (6, 7): openings = [(XC - 6, XC + 6)]
    if (i, i + 1) == (4, 5): openings = [(CX_COL - 12, CX_COL + 12)]   # colonnade arrives through the west arm's south wall
    for k in range(n):
        ax, ay = x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n
        bx, by = x0 + (x1 - x0) * (k + 1) / n, y0 + (y1 - y0) * (k + 1) / n
        mx_ = (ax + bx) / 2
        is_open = any(lo < mx_ < hi for lo, hi in openings) if y0 == y1 else False
        zlo = ZF + (10 if is_open else 0)
        G.quad([(ax, ay, zlo), (bx, by, zlo), (bx, by, ZF + H_ARM), (ax, ay, ZF + H_ARM)])
        FR.box(ax - 0.35, ax + 0.35, ay - 0.35, ay + 0.35, ZF, ZF + H_ARM)          # 8 ft mullion/column
    for t in (ZF + 3.0, ZF + 10.0, ZF + H_ARM - 1.2):                                  # sill, transom, plate
        if t == ZF + 3.0 and (i, i + 1) in ((6, 7), (4, 5)): continue
        FR.strut((x0, y0, t), (x1, y1, t), 0.7 if t < ZF + H_ARM - 2 else 1.4)
# flat glazed roofs over arms/stub/neck extensions (I)
R = MB('cp044_entrance_roof', M['groof'])
for (x0, x1, y0, y1) in ((XC - ARM_HW, XA, Y_ARM1, Y_ARM0), (XB, XC + ARM_HW, Y_ARM1, Y_ARM0),
                         (XC - STEP_HW, XA, Y_ARM0, Y_STEP0), (XB, XC + STEP_HW, Y_ARM0, Y_STEP0),
                         (XC - STEP_HW, XA, YEND, Y_ARM1), (XB, XC + STEP_HW, YEND, Y_ARM1)):
    R.quad([(x0, y0, ZF + H_ARM), (x1, y0, ZF + H_ARM), (x1, y1, ZF + H_ARM), (x0, y1, ZF + H_ARM)])
for xx in (XA, XB):
    FR.box(xx - 0.5, xx + 0.5, YEND, Y_STEP0, ZF + H_ARM - 1.4, ZF + H_ARM)
    for yy in (Y_ARM1, Y_ARM0, Y_STEP0):
        FR.box(xx - 0.4, xx + 0.4, yy - 0.4, yy + 0.4, ZF, ZF + H_ARM)
# boarded floor over the whole entrance (the wing floor slab reads as pale iron)
FL = MB('cp044_entrance_floor', M['boards'])
FL.box(XC - ARM_HW, XC + ARM_HW, Y_ARM1, Y_ARM0, ZF, ZF + 0.12)
FL.box(XC - STEP_HW, XC + STEP_HW, YEND, Y_ARM1, ZF, ZF + 0.12)
FL.box(XC - STEP_HW, XC + STEP_HW, Y_ARM0, Y_STEP0, ZF, ZF + 0.12)
FL.box(XA, XB, Y_STEP0, -300, ZF, ZF + 0.12)
G.done(); FR.done(); R.done(); FL.done()

# ------------------------------------------------------------------ 2. admission barrier, turnstiles, pay boxes
Z0 = ZF + 0.12
BAR = MB('cp044_barrier_oak', M['oak']); PNT = MB('cp044_boards_green', M['paint']); GIL = MB('cp044_gilt', M['gilt'])
CI = MB('cp044_turnstiles_iron', M['castiron']); BR = MB('cp044_brass_fittings', M['brass'])
TS = [XC - 12.5, XC - 9.5, XC - 6.5]                 # three turnstile passages (2 ft 6 in centres 3 ft) I
GATE = (XC - 2.5, XC + 2.5)                          # central exit/carriage-bath-chair gate, closed (I)
PB = [(XC - STEP_HW, XC - 16.0), (XC + 9.0, XC + 16.0)]  # two pay boxes (money-takers) I
segs = [(XC - 16.0, TS[0] - 1.25), (TS[0] + 1.25, TS[1] - 1.25), (TS[1] + 1.25, TS[2] - 1.25), (TS[2] + 1.25, GATE[0]),
        (GATE[1], XC + 9.0), (XC + 16.0, XC + STEP_HW)]
for (a, b) in segs:                                   # panelled dado barrier 3 ft 6 in (I)
    BAR.box(a, b, Y_BAR - 0.15, Y_BAR + 0.15, Z0, Z0 + 3.2)
    BAR.box(a - 0.1, b + 0.1, Y_BAR - 0.3, Y_BAR + 0.3, Z0 + 3.2, Z0 + 3.5)       # handrail
    for x in (a, b): BAR.box(x - 0.3, x + 0.3, Y_BAR - 0.3, Y_BAR + 0.3, Z0, Z0 + 3.9)  # newels
    BR.sphere(a, Y_BAR, Z0 + 4.0, 0.22); BR.sphere(b, Y_BAR, Z0 + 4.0, 0.22)
    n = max(1, round((b - a) / 2.0))
    for k in range(n):
        x0 = a + (b - a) * k / n + 0.25; x1 = a + (b - a) * (k + 1) / n - 0.25
        PNT.box(x0, x1, Y_BAR - 0.2, Y_BAR - 0.16, Z0 + 0.6, Z0 + 2.8)             # sunk panels
for i, x in enumerate(TS):                            # cast-iron turnstile: pedestal, drum, 4 arms (I)
    CI.cyl(x, Y_BAR, Z0, Z0 + 2.6, 0.35, 0.28, 12)
    CI.cyl(x, Y_BAR, Z0 + 2.6, Z0 + 3.1, 0.42, 0.42, 16)
    BR.cyl(x, Y_BAR, Z0 + 3.1, Z0 + 3.25, 0.25, 0.1, 12)
    for k in range(4):
        a = math.radians(45 + 90 * k + 20 * i)
        CI.strut((x, Y_BAR, Z0 + 2.85), (x + 1.15 * math.cos(a), Y_BAR + 1.15 * math.sin(a), Z0 + 2.85), 0.12)
    for side in (-1, 1):                              # guide rails each side of the passage
        CI.strut((x + side * 1.25, Y_BAR - 2.5, Z0 + 3.0), (x + side * 1.25, Y_BAR + 2.5, Z0 + 3.0), 0.1)
        for yy in (Y_BAR - 2.5, Y_BAR + 2.5):
            CI.strut((x + side * 1.25, yy, Z0), (x + side * 1.25, yy, Z0 + 3.0), 0.12)
BAR.box(GATE[0], GATE[1], Y_BAR - 0.12, Y_BAR + 0.12, Z0 + 0.4, Z0 + 3.4)              # closed gate leaf
for x in GATE: BAR.box(x - 0.3, x + 0.3, Y_BAR - 0.3, Y_BAR + 0.3, Z0, Z0 + 4.2)
# collector's desk on the station side, between turnstiles and gate (I)
BAR.box(XC - 4.6, XC - 3.0, Y_BAR - 3.0, Y_BAR - 0.4, Z0, Z0 + 3.4)
BAR.box(XC - 4.8, XC - 2.8, Y_BAR - 3.2, Y_BAR - 0.2, Z0 + 3.4, Z0 + 3.55)
BR.box(XC - 4.4, XC - 3.6, Y_BAR - 2.6, Y_BAR - 1.4, Z0 + 3.55, Z0 + 3.95)            # ticket box
for (a, b) in PB:                                     # pay boxes: panelled oak booth, glazed sash, pediment board
    y0, y1 = Y_BAR - 6.5, Y_BAR + 0.0
    BAR.box(a, b, y0, y1, Z0, Z0 + 3.4)                                                   # lower body
    for xx in (a, b):
        BAR.box(xx - 0.25, xx + 0.25, y0, y1, Z0 + 3.4, Z0 + 8.6)                         # corner posts
    BAR.box(a, b, y1 - 0.4, y1, Z0 + 3.4, Z0 + 8.6)                                      # back
    side_face = b if a < XC else a                                                       # aisle-side face
    BAR.box(side_face - 0.15, side_face + 0.15, y0, y1, Z0 + 3.4, Z0 + 8.6)
    BAR.box(a - 0.3, b + 0.3, y0 - 0.3, y1 + 0.3, Z0 + 8.6, Z0 + 9.2)                     # cornice
    PNT.box(a + 0.3, b - 0.3, y0 - 0.32, y0 - 0.28, Z0 + 9.3, Z0 + 10.8)                # blank fascia board (no tariff shown)
    BAR.box(a, b, y0 - 0.25, y0 + 0.1, Z0 + 9.2, Z0 + 11.1)
    GIL.box(a + 0.45, b - 0.45, y0 - 0.36, y0 - 0.33, Z0 + 9.45, Z0 + 9.55)
    GIL.box(a + 0.45, b - 0.45, y0 - 0.36, y0 - 0.33, Z0 + 10.55, Z0 + 10.65)
    BAR.box(a + 0.3, b - 0.3, y0 - 0.6, y0 + 0.2, Z0 + 3.4, Z0 + 3.6)                    # counter sill
    BR.box((a + b) / 2 - 0.6, (a + b) / 2 + 0.6, y0 - 0.12, y0 - 0.08, Z0 + 3.6, Z0 + 4.4)  # speaking grille
    for xx in (a + (b - a) / 3, a + 2 * (b - a) / 3):
        BAR.box(xx - 0.08, xx + 0.08, y0 - 0.05, y0 + 0.05, Z0 + 3.6, Z0 + 8.6)          # sash bars
    BAR.box(a, b, y0 - 0.05, y0 + 0.05, Z0 + 6.2, Z0 + 6.32)
    g = MB(f'cp044_paybox_glass_{int(a)}', M['glass'])
    g.quad([(a, y0, Z0 + 3.6), (b, y0, Z0 + 3.6), (b, y0, Z0 + 8.6), (a, y0, Z0 + 8.6)]); g.done()
    BAR.box(a + 0.5, b - 0.5, y0 + 1.5, y0 + 2.4, Z0, Z0 + 3.2)                          # inner desk
# coconut mats at the turnstiles (I)
MT = MB('cp044_mats', M['mat_coco'])
for x in TS: MT.box(x - 1.1, x + 1.1, Y_BAR - 4.0, Y_BAR - 0.4, Z0, Z0 + 0.06)
MT.done()
BAR.done(); PNT.done(); GIL.done(); CI.done(); BR.done()

# ------------------------------------------------------------------ 2b. the wing staircase drawn on plan 0205 just north of the entrance
# plan 0205 px (full res): side flights 23 px (8 ft) each, spine 20 px (7 ft), 63 px (21.8 ft) long; landing 22 px (7.6 ft) x 65 px
# (22.5 ft); central flight 25 px (8.7 ft) x 58 px (20 ft). Plan y shifted by the same -11 ft as the cross (D-SY-CP044-06).
# Rise I: side flights + central flight climb one wing storey (18 ft, the existing zb+18 frame band) to an upper floor (I).
ST = MB('cp044_wing_stair_oak', M['oak']); STR = MB('cp044_wing_stair_treads', M['boards'])
Y_SF0, Y_SF1, Y_LD1, Y_CF1 = -554.0, -532.2, -524.6, -504.6
Z_LD, Z_UP = Z0 + 9.0, ZF + 18.0
def flight(x0, x1, y0, y1, z0, z1, n):
    for k in range(n):
        ya = y0 + (y1 - y0) * k / n; yb = y0 + (y1 - y0) * (k + 1) / n
        STR.box(x0, x1, ya, yb, z0, z0 + (z1 - z0) * (k + 1) / n)
    for xx in (x0, x1):                                   # strings + handrail
        ST.strut((xx, y0, z0 + 0.6), (xx, y1, z1 + 0.6), 0.35)
        ST.strut((xx, y0, z0 + 3.3), (xx, y1, z1 + 3.3), 0.2)
        for k in range(0, n + 1, 3):
            t = k / n; ST.strut((xx, y0 + (y1 - y0) * t, z0 + (z1 - z0) * t), (xx, y0 + (y1 - y0) * t, z0 + (z1 - z0) * t + 3.3), 0.08)
flight(XC - 11.2, XC - 3.2, Y_SF0, Y_SF1, Z0, Z_LD, 18)
flight(XC + 3.2, XC + 11.2, Y_SF0, Y_SF1, Z0, Z_LD, 18)
ST.box(XC - 3.2, XC + 3.2, Y_SF0, Y_SF1, Z0, Z_LD - 0.3)                                  # spine wall between flights
STR.box(XC - 11.2, XC + 11.2, Y_SF1, Y_LD1, Z0, Z_LD)                                     # landing
flight(XC - 4.35, XC + 4.35, Y_LD1, Y_CF1, Z_LD, Z_UP, 18)
STR.box(XA, XB, Y_CF1, -100.0, Z_UP - 0.6, Z_UP)                                           # upper floor of the wing (I)
for xx in (XA + 0.5, XC - 4.35, XC + 4.35, XB - 0.5):
    ST.box(xx - 0.25, xx + 0.25, Y_CF1 - 0.25, Y_CF1 + 0.25, Z_UP, Z_UP + 3.6)
ST.strut((XA + 0.5, Y_CF1, Z_UP + 3.4), (XC - 4.35, Y_CF1, Z_UP + 3.4), 0.25)             # balustrade at the stair head
ST.strut((XC + 4.35, Y_CF1, Z_UP + 3.4), (XB - 0.5, Y_CF1, Z_UP + 3.4), 0.25)
for xx in [XA + 0.5 + k * 1.0 for k in range(14)] + [XC + 4.35 + k * 1.0 for k in range(14)]:
    ST.strut((xx, Y_CF1, Z_UP), (xx, Y_CF1, Z_UP + 3.4), 0.1)
for xx in (XC - 11.2, XC + 11.2):                                                          # landing posts carrying the upper floor edge
    ST.box(xx - 0.4, xx + 0.4, Y_LD1 - 0.4, Y_LD1 + 0.4, Z0, Z_UP - 0.6)
ST.done(); STR.done()

# ------------------------------------------------------------------ 3. plants in tubs (company plants; orange trees I)
TB = MB('cp044_tubs', M['tub']); HP = MB('cp044_tub_hoops', M['hoop']); SO = MB('cp044_soil', M['soil'])
LF = MB('cp044_orange_foliage', M['leaf']); BK = MB('cp044_orange_stems', M['bark']); OR = MB('cp044_oranges', M['orange'])
rnd = random.Random(1856044)
TUBS = [(XC - 40, Y_ARM0 - 4), (XC - 30, Y_ARM0 - 4), (XC + 30, Y_ARM0 - 4), (XC + 40, Y_ARM0 - 4),
        (XA + 3.5, -566), (XA + 3.5, -540), (XB - 3.5, -566), (XB - 3.5, -536), (XA + 3.5, -516), (XB - 3.5, -512)]
for (x, y) in TUBS:
    s = 2.4
    TB.box(x - s / 2, x + s / 2, y - s / 2, y + s / 2, Z0 + 0.3, Z0 + 2.6)               # square Versailles tub
    for (dx, dy) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        TB.box(x + dx * s / 2 - 0.15, x + dx * s / 2 + 0.15, y + dy * s / 2 - 0.15, y + dy * s / 2 + 0.15, Z0, Z0 + 3.0)
        HP.sphere(x + dx * s / 2, y + dy * s / 2, Z0 + 3.05, 0.18, 1)
    for z in (Z0 + 0.8, Z0 + 2.2): HP.box(x - s / 2 - 0.04, x + s / 2 + 0.04, y - s / 2 - 0.04, y + s / 2 + 0.04, z, z + 0.12)
    SO.box(x - s / 2 + 0.1, x + s / 2 - 0.1, y - s / 2 + 0.1, y + s / 2 - 0.1, Z0 + 2.6, Z0 + 2.7)
    BK.cyl(x, y, Z0 + 2.6, Z0 + 5.2, 0.16, 0.12, 8)
    cz = Z0 + 6.6
    for k in range(7):
        LF.sphere(x + rnd.uniform(-0.9, 0.9), y + rnd.uniform(-0.9, 0.9), cz + rnd.uniform(-0.6, 0.8), rnd.uniform(0.9, 1.3), 2)
    for k in range(9):
        a = rnd.uniform(0, 6.28); OR.sphere(x + 1.55 * math.cos(a), y + 1.55 * math.sin(a), cz + rnd.uniform(-0.8, 0.6), 0.14, 1)
TB.done(); HP.done(); SO.done(); LF.done(); BK.done(); OR.done()

# ------------------------------------------------------------------ 4. maintenance: glazier's ladder + pane, gardener's can
LD = MB('cp044_glazier_ladder', M['deal'])
LX, LY = XB - 1.6, -548.0                            # against the east wing glazing, north of the barrier
for dy in (-0.9, 0.9): LD.strut((LX - 2.2, LY + dy, Z0), (LX - 0.2, LY + dy, Z0 + 11.5), 0.22)
for k in range(1, 11):
    t = k / 11.5 * 11.5
    LD.strut((LX - 2.2 + 2.0 * t / 11.5, LY - 0.9, Z0 + t), (LX - 2.2 + 2.0 * t / 11.5, LY + 0.9, Z0 + t), 0.12)
LD.done()
PN = MB('cp044_new_pane', M['pane']); PN.box(XB - 0.9, XB - 0.84, LY - 1.0, LY + 1.0, Z0 + 8.2, Z0 + 12.2); PN.done()
PE = MB('cp044_new_pane_paper_edge', M['ticket'])           # paper-wrapped edges of the new sheet (I)
for (y0, y1, z0, z1) in ((LY - 1.0, LY + 1.0, Z0 + 8.2, Z0 + 8.4), (LY - 1.0, LY + 1.0, Z0 + 12.0, Z0 + 12.2),
                         (LY - 1.0, LY - 0.8, Z0 + 8.2, Z0 + 12.2), (LY + 0.8, LY + 1.0, Z0 + 8.2, Z0 + 12.2)):
    PE.box(XB - 0.92, XB - 0.82, y0, y1, z0, z1)
PE.done()  # pane offered up (49 in sheet, I)
WC = MB('cp044_watering_can', M['zinc'])
GX, GY = XB - 6.6, -568.5
WC.cyl(GX + 1.0, GY - 0.9, Z0 + 2.7, Z0 + 3.7, 0.42, 0.42, 14)
WC.strut((GX + 1.3, GY - 0.9, Z0 + 2.9), (GX + 2.7, GY - 1.6, Z0 + 3.8), 0.12)
WC.done()

# ------------------------------------------------------------------ 5. people (people_lib v3.4, hero/mid LOD, baked meshes)
def put(name, role, pose, x, y, face, lod='hero', seed=None, z=None, scale=1.0):
    me = person_mesh(name, role, style={'role': role, 'pose': pose, 'lod': lod}, seed=seed)
    o = bpy.data.objects[name]
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o)
    o.location = (x * F, y * F, (Z0 if z is None else z) * F)
    o.rotation_euler = (0, 0, math.atan2(face[0], -face[1]))   # base meshes face local -Y
    o.scale = (scale,) * 3
    o['cp_state'] = 'SY-EARLY_c1856'; o['cpl_people'] = 'cpl_people_v3'
    bpy.context.view_layer.update(); print('CP044 PERSON', name, role, round(o.dimensions.z / scale, 2), 'm')
    return o
N = (0, 1)
# the family at the left turnstile, backs to the lens (no close faces)
put('cp044_family_father', '1850s_gentleman', 'pointing', TS[0] + 0.2, Y_BAR - 2.6, (0.35, 1), seed=4401)
put('cp044_family_mother', '1850s_lady', 'standing', TS[0] - 2.4, Y_BAR - 5.0, (0.1, 1), seed=4402)
put('cp044_family_boy', '1850s_boy', 'walking', TS[0] - 0.4, Y_BAR - 5.6, (0.15, 1), seed=4403)
_g = put('cp044_family_girl', '1850s_girl', 'standing', TS[0] - 3.2, Y_BAR - 7.0, (0.3, 1), seed=4404)
print('CP044 GIRL MATS', [m.name for m in _g.data.materials])
_bon = mat('cp044_girl_bonnet_silk', (0.22, 0.08, 0.12), 0.55)
for i, m in enumerate(_g.data.materials):          # pale bonnet read as a bald head from behind: dark silk bonnet (I)
    if m and any(k in m.name.lower() for k in ('hat', 'bonnet', 'straw')):
        _g.data.materials[i] = _bon
# staff: ticket collector at his desk facing the passage, money-taker seated in the left pay box
put('cp044_staff_collector', '1850s_police', 'standing', XC - 4.0, Y_BAR - 1.4, (-1, -0.25), seed=4405)
put('cp044_staff_moneytaker', '1850s_gentleman', 'seated', (PB[0][0] + PB[0][1]) / 2, Y_BAR - 3.2, (0, -1), lod='mid', seed=4406)
# others: a queue at the right pay box, two through already, a couple further up the wing
put('cp044_vis_paybox_m', '1850s_gentleman', 'standing', PB[1][0] + 3.4, Y_BAR - 8.6, (0, 1), lod='mid', seed=4407)
put('cp044_vis_paybox_w', '1850s_lady', 'standing', PB[1][0] + 1.4, Y_BAR - 11.2, (0.2, 1), lod='mid', seed=4408)
put('cp044_vis_arm_w', '1850s_lady', 'walking', XC + 24, Y_ARM0 - 18, (-1, 0.4), lod='mid', seed=4409)
put('cp044_vis_through_m', '1850s_gentleman', 'walking', XC - 9.0, Y_BAR + 22.0, N, lod='mid', seed=4410)
put('cp044_vis_through_w', '1850s_lady', 'walking', XC - 6.6, Y_BAR + 24.0, N, lod='mid', seed=4411)
put('cp044_vis_arrive_w', '1850s_lady', 'walking', XC + 5.0, Y_BAR - 13.0, (0.45, 1), lod='mid', seed=4417)
put('cp044_vis_stair_w', '1850s_lady', 'walking', XC + 7.2, -543.0, N, lod='mid', seed=4412, z=Z0 + 9.0 * (11.0 / 21.8))
put('cp044_vis_stair_m', '1850s_gentleman', 'walking', XC + 0.5, -514.0, N, lod='mid', seed=4413, z=Z_LD + 9.0 * (10.6 / 20.0))
put('cp044_vis_upper_m', '1850s_gentleman', 'standing', XC - 8.0, -497.0, (0.3, -1), lod='crowd', seed=4418, z=Z_UP)
# maintenance: glazier on the ladder, gardener watering an orange tub
put('cp044_staff_glazier', '1850s_workman', 'working', LX - 1.3, LY, (1, 0), seed=4414, z=Z0 + 6.0)
put('cp044_staff_gardener', '1850s_workman', 'working', GX, GY, (1, -0.3), seed=4415)

# ------------------------------------------------------------------ 6. cameras
def cam(name, loc, tgt, lens):
    o = bpy.data.objects.get(name)
    if o is None:
        cd = bpy.data.cameras.new(name); o = bpy.data.objects.new(name, cd); bpy.context.scene.collection.objects.link(o)
    o.data.lens = lens; o.data.sensor_width = 36
    o.location = Vector(loc) * F
    o.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    o['cp044'] = 'candidate 2026-11-13'
EYE = 5.25                                            # 1.6 m
cam('CAM_CP044_pay_desks_35mm', (XC - 5.0, Y_ARM1 + 13.0, Z0 + EYE), (XC - 4.0, Y_BAR + 40.0, Z0 + 4.2), 35)
cam('CAM_CP044_maintenance_50mm', (XC - 6.0, Y_BAR + 6.0, Z0 + EYE), (XB - 4.0, -556.0, Z0 + 7.0), 50)

if OUT != '--nosave':
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True)
    print('CP044 SAVED', OUT)
