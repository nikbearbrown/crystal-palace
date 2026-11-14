"""CP051 CANDIDATE (2026-11-14): SY-LATE, 30 Jan - 7 Feb 1903 — the first SMMT motor show in the Sydenham nave.

usage: blender -b rounds/sydenham-late11-r16.blend -P scripts/candidate_cp051_motor_show.py [-- out.blend]
       (env CP051_NOSAVE=1: build in memory only)
Opens the live LATE11 round (never writes it), adds dated collection SY03_smmt_motor_show_nave__1903 and hides (never
deletes) the west-nave planting placeholders, the r16 gold 'tech cabinet' boxes (mesh copy, pendants kept), and the
1911 Festival / 1913 Plymouth flags that read through the glazing (later dates than this state). Removes only the stray
nave-interior points (x -360..-30, |y| < 40) from the three LATE11 GN crowds (copied meshes); those points were duplicated
across all three objects (overlapping figures = the 'double-face' noted in DEPARTURES people v3.1/v3.3) and include
points floating at z 57 ft inside the nave span. Cameras are NOT moved.
Sources (DEPARTURES D-SY-CP051-01..):
  * Grace's Guide, '1903 Motor Show (SMMT January)': Crystal Palace, 30 Jan - 7 Feb 1903; petrol cars, steam cars,
    electromobiles, chassis; e.g. Sunbeam 12 h.p. 4-cyl, Fiat 16/20/30 h.p. 4-cyl, Traveller two/three-seat voiturettes,
    Mabley 2 3/4 h.p. De Dion engined, Toledo steam cars; numbered stands, some in the courts (Stand 3a Greek Court).
  * Grace's Guide, 'Motor Show Early History' (1903): over 530 cars, about 440 complete and 68 chassis.
  * britainbycar.co.uk 'The Crystal Palace Motor Car Shows': shows held 'amid the courts and permanent attractions',
    1896, 1902-1906; 1903 = first SMMT show.
  * Storyboard CP051: 'approach one display ... hold old framing with newer technology in the same composition';
    'select and date one actual exhibit' -> stand dressing is generic (blank fascias, no invented makers/prices).
Car forms are generic 1903 types (I): rear-entrance tonneau (12-16 h.p. 4-cyl class), two-seat voiturette, bare chassis.
Units: feet (F converts).
"""
import bpy, bmesh, math, sys, os, random
from mathutils import Vector, Matrix

F = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P
from cpl_people import person_mesh

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP051_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-late11-r16_cp051motor.blend')
STATE = 'SY-LATE_1903-01-30..1903-02-07_SMMT_motor_show'
RNG = random.Random(1903)
BAY = P.BAY
NY = P.NAVE_SPAN / 2

COLL = 'SY03_smmt_motor_show_nave__1903'
col = bpy.data.collections.get(COLL) or bpy.data.collections.new(COLL)
if col.name not in [c.name for c in bpy.context.scene.collection.children]:
    bpy.context.scene.collection.children.link(col)
col['cp_state'] = STATE
col['evidence'] = "Grace's Guide 1903 Motor Show (SMMT January) + Motor Show Early History R (dates, 530 cars, 68 chassis, petrol/steam/electric, stands in courts); car forms, stand dressing, layout I"

def mat(name, rgb, rough=0.6, metal=0.0, coat=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if coat and 'Coat Weight' in b.inputs: b.inputs['Coat Weight'].default_value = coat
    m.diffuse_color = (*rgb, 1)
    return m

PAINTS = [mat('cp051_paint_green', (0.035, 0.11, 0.06), 0.35, 0, 0.6), mat('cp051_paint_maroon', (0.17, 0.025, 0.03), 0.35, 0, 0.6),
          mat('cp051_paint_blue', (0.03, 0.05, 0.14), 0.35, 0, 0.6), mat('cp051_paint_cream', (0.62, 0.55, 0.40), 0.4, 0, 0.5),
          mat('cp051_paint_red', (0.32, 0.03, 0.02), 0.35, 0, 0.6)]
M = dict(
    leather_b=mat('cp051_leather_black', (0.02, 0.018, 0.016), 0.5),
    leather_r=mat('cp051_leather_red', (0.20, 0.04, 0.03), 0.5),
    leather_g=mat('cp051_leather_green', (0.05, 0.09, 0.05), 0.5),
    brass=mat('cp051_brass', (0.62, 0.45, 0.16), 0.25, 1.0),
    steel=mat('cp051_steel_black', (0.025, 0.025, 0.027), 0.45, 0.6),
    iron=mat('cp051_engine_iron', (0.10, 0.10, 0.10), 0.55, 0.5),
    alu=mat('cp051_engine_alu', (0.45, 0.45, 0.43), 0.4, 0.9),
    wheel=mat('cp051_wheel_varnished_ash', (0.32, 0.17, 0.07), 0.4),
    tyre=mat('cp051_tyre_grey_rubber', (0.40, 0.39, 0.36), 0.8),     # pre-carbon-black grey rubber (I)
    wood=mat('cp051_dash_mahogany', (0.18, 0.07, 0.03), 0.35),
    core=mat('cp051_radiator_core', (0.04, 0.035, 0.03), 0.7, 0.4),
    deal=mat('cp051_stand_deal_stained', (0.24, 0.15, 0.08), 0.7),
    baize_r=mat('cp051_stand_baize_crimson', (0.30, 0.04, 0.04), 0.95),
    baize_g=mat('cp051_stand_baize_green', (0.06, 0.15, 0.08), 0.95),
    fascia=mat('cp051_fascia_dark_green', (0.03, 0.07, 0.045), 0.5),
    letter=mat('cp051_fascia_gilt_band', (0.55, 0.42, 0.18), 0.35, 0.7),
    rail=mat('cp051_stand_rail_white', (0.62, 0.60, 0.55), 0.5),
    rope=mat('cp051_stand_rope_crimson', (0.35, 0.05, 0.05), 0.8),
)

class MB:
    """bmesh builder with a placement matrix (feet in, metres out); one mesh per material."""
    def __init__(self, name, m):
        self.name, self.bm, self.m = name, bmesh.new(), m
    def _put(self, verts, T):
        bmesh.ops.transform(self.bm, matrix=T, verts=verts)
    def box(self, W, x0, x1, y0, y1, z0, z1):
        r = bmesh.ops.create_cube(self.bm, size=1.0)
        T = W @ Matrix.Translation(Vector(((x0+x1)/2, (y0+y1)/2, (z0+z1)/2)) * F) @ Matrix.Diagonal(Vector((abs(x1-x0)*F, abs(y1-y0)*F, abs(z1-z0)*F, 1)))
        self._put(r['verts'], T)
    def rod(self, W, a, b, r, seg=8):
        a, b = Vector(a), Vector(b); d = b - a; L = d.length
        res = bmesh.ops.create_cone(self.bm, cap_ends=True, segments=seg, radius1=r*F, radius2=r*F, depth=L*F)
        q = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_matrix().to_4x4()
        self._put(res['verts'], W @ Matrix.Translation(((a+b)/2) * F) @ q)
    def cyl_y(self, W, x, y, z, r, w, seg=16):            # axis along local y (wheels, axles)
        self.rod(W, (x, y - w/2, z), (x, y + w/2, z), r, seg)
    def torus_y(self, W, x, y, z, R, r, seg=28, sseg=8):  # ring in the local xz plane
        bm = self.bm; rings = []
        for i in range(seg):
            a = 2*math.pi*i/seg; ring = []
            for j in range(sseg):
                b = 2*math.pi*j/sseg
                rr = R + r*math.cos(b)
                ring.append(bm.verts.new(Vector((x + rr*math.cos(a), y + r*math.sin(b), z + rr*math.sin(a))) ))
            rings.append(ring)
        for i in range(seg):
            for j in range(sseg):
                a0, a1 = rings[i], rings[(i+1) % seg]
                bm.faces.new((a0[j], a1[j], a1[(j+1) % sseg], a0[(j+1) % sseg]))
        vs = [v for rg in rings for v in rg]
        self._put(vs, W @ Matrix.Diagonal(Vector((F, F, F, 1))))
    def arc_strip(self, W, cx, cz, R, a0, a1, y0, y1, t=0.06, seg=12):   # curved mudguard in local xz
        bm = self.bm; outer = []; inner = []
        for i in range(seg + 1):
            a = math.radians(a0 + (a1 - a0) * i / seg)
            for rr, lst in ((R, outer), (R + t, inner)):
                lst.append((bm.verts.new(Vector((cx + rr*math.cos(a), y0, cz + rr*math.sin(a)))),
                            bm.verts.new(Vector((cx + rr*math.cos(a), y1, cz + rr*math.sin(a))))))
        for i in range(seg):
            for L in (outer, inner):
                bm.faces.new((L[i][0], L[i+1][0], L[i+1][1], L[i][1]))
            bm.faces.new((outer[i][0], inner[i][0], inner[i+1][0], outer[i+1][0]))
            bm.faces.new((outer[i][1], outer[i+1][1], inner[i+1][1], inner[i][1]))
        vs = [v for L in (outer, inner) for p in L for v in p]
        self._put(vs, W @ Matrix.Diagonal(Vector((F, F, F, 1))))
    def ring_z(self, W, cx, cy, z0, z1, ro, ri, a0, a1, seg=16):  # vertical curved wall (tonneau back)
        bm = self.bm; pts = []
        for i in range(seg + 1):
            a = math.radians(a0 + (a1 - a0) * i / seg)
            pts.append([bm.verts.new(Vector((cx + rr*math.cos(a), cy + rr*math.sin(a), z))) for rr in (ro, ri) for z in (z0, z1)])
        for i in range(seg):
            p, q = pts[i], pts[i+1]
            for (u, v) in ((0, 1), (2, 3)): bm.faces.new((p[u], q[u], q[v], p[v]))
            bm.faces.new((p[1], q[1], q[3], p[3])); bm.faces.new((p[0], p[2], q[2], q[0]))
        for p in (pts[0], pts[-1]): bm.faces.new((p[0], p[1], p[3], p[2]))
        self._put([v for p in pts for v in p], W @ Matrix.Diagonal(Vector((F, F, F, 1))))
    def done(self):
        if not self.bm.verts: self.bm.free(); return None
        me = bpy.data.meshes.new(self.name); self.bm.to_mesh(me); self.bm.free()
        me.materials.append(self.m)
        for p in me.polygons: p.use_smooth = False
        o = bpy.data.objects.new(self.name, me); col.objects.link(o); o['cp_state'] = STATE; return o

_B = {}
def B(key, m):
    if key not in _B: _B[key] = MB('cp051_' + key, m)
    return _B[key]

def placement(x, y, yaw_deg):
    return Matrix.Translation(Vector((x, y, 0)) * F) @ Matrix.Rotation(math.radians(yaw_deg), 4, 'Z')

def steering_wheel(W, a, b, R):
    d = (Vector(b) - Vector(a)).normalized()
    q = Vector((0, 1, 0)).rotation_difference(d).to_matrix().to_4x4()
    B('wood', M['wood']).torus_y(W @ Matrix.Translation(Vector(b) * F) @ q, 0, 0, 0, R, 0.05, 24, 6)   # torus_y applies the ft->m scale

def wheel(W, x, y, z0, D, w=0.28, spokes=12):
    R = D / 2; zc = R
    B('tyre', M['tyre']).torus_y(W, x, y, zc, R - 0.13, 0.13, 30, 8)
    B('wheel', M['wheel']).torus_y(W, x, y, zc, R - 0.31, 0.06, 26, 6)                # felloe
    B('wheel', M['wheel']).cyl_y(W, x, y, zc, 0.26, w, 12)                            # hub shell
    B('brass', M['brass']).cyl_y(W, x, y + (w/2 + 0.04) * (1 if y > 0 else -1), zc, 0.13, 0.08, 10)   # hub cap
    for k in range(spokes):
        a = 2*math.pi*k/spokes
        B('wheel', M['wheel']).rod(W, (x + 0.22*math.cos(a), y, zc + 0.22*math.sin(a)), (x + (R-0.33)*math.cos(a), y, zc + (R-0.33)*math.sin(a)), 0.05, 6)
    return zc

def car_tonneau(x, y, yaw, paint, leather, seed=0, hood=False):
    """generic 1903 rear-entrance tonneau, 12-16 h.p. 4-cyl class (I): wheelbase 7 ft 6 in, track 4 ft 5 in, 33/34 in wheels"""
    W = placement(x, y, yaw); r = random.Random(seed)
    WB, TR = 7.5, 4.4
    for (wx, D) in ((WB/2, 2.75), (-WB/2, 2.83)):
        for s in (1, -1): wheel(W, wx, s*TR/2, 0, D)
    S = B('steel', M['steel'])
    for s in (1, -1): S.box(W, -4.7, 4.75, s*1.3 - 0.1, s*1.3 + 0.1, 1.55, 1.95)           # frame side members
    S.cyl_y(W, WB/2, 0, 1.375, 0.09, TR, 8); S.cyl_y(W, -WB/2, 0, 1.415, 0.11, TR, 8)        # axles
    for s in (1, -1):                                                                        # semi-elliptic springs
        for ax in (WB/2, -WB/2): S.box(W, ax - 1.5, ax + 1.5, s*1.3 - 0.12, s*1.3 + 0.12, 1.45, 1.6)
    Br = B('brass', M['brass'])
    Br.box(W, 4.55, 4.78, -1.0, 1.0, 1.85, 4.0)                                              # radiator shell (honeycomb)
    B('core', M['core']).box(W, 4.76, 4.80, -0.85, 0.85, 2.0, 3.85)
    Pn = B('paint_' + paint.name, paint)
    Pn.box(W, 2.0, 4.55, -0.95, 0.95, 2.0, 3.45)                                             # bonnet
    Pn.rod(W, (2.0, 0, 3.45), (4.55, 0, 3.45), 0.95, 16)                                     # rounded bonnet top
    S.box(W, 2.0, 4.55, -0.97, 0.97, 1.95, 2.05)
    B('wood', M['wood']).box(W, 1.85, 2.0, -1.55, 1.55, 1.95, 4.05)                          # dash
    Pn.box(W, -0.55, 1.85, -1.6, 1.6, 1.95, 3.15)                                            # front seat tub
    Lm = B('leather_' + leather.name, leather)
    Lm.box(W, -0.35, 1.1, -1.45, 1.45, 3.0, 3.4)                                             # cushion
    Lm.box(W, -0.6, -0.25, -1.5, 1.5, 3.1, 4.75)                                             # front squab
    Pn.box(W, -2.6, -0.55, -1.95, 1.95, 1.95, 3.3)                                           # tonneau body
    Pn.rod(W, (-2.6, 0, 1.95), (-2.6, 0, 3.3), 1.95, 24)                                     # rounded tonneau back
    Pn.ring_z(W, -2.6, 0, 3.3, 4.55, 1.95, 1.75, 90, 270, 18)                                # back rail
    Lm.rod(W, (-2.6, 0, 3.3), (-2.6, 0, 3.5), 1.7, 20); Lm.box(W, -2.6, -0.7, -1.75, 1.75, 3.3, 3.5)   # rear cushions
    S.box(W, -4.56, -4.5, -0.45, 0.45, 2.0, 3.6)                                              # rear door seam (dark)
    Br.box(W, -4.58, -4.53, 0.25, 0.35, 2.6, 2.8)                                             # door handle
    G = B('steel', M['steel'])
    for (wx, D) in ((WB/2, 2.75), (-WB/2, 2.83)):                                             # wings
        for s in (1, -1):
            G.arc_strip(W, wx, D/2, D/2 + 0.18, 15 if wx > 0 else 25, 165 if wx > 0 else 160, s*(TR/2 - 0.35), s*(TR/2 + 0.35), 0.05, 12)
    for s in (1, -1): G.box(W, -2.35, 2.35, s*1.65, s*2.55, 1.5, 1.56)                        # running boards
    Br.rod(W, (1.45, -0.55, 2.0), (0.45, -0.55, 4.25), 0.07, 8)                               # raked steering column (RHD)
    steering_wheel(W, (1.45, -0.55, 2.0), (0.42, -0.55, 4.3), 0.72)
    for s in (1, -1): Br.rod(W, (1.95, s*1.62, 3.45), (1.95, s*1.62, 3.95), 0.2, 10)          # oil side lamps
    Br.rod(W, (4.85, 0, 3.0), (5.35, 0, 3.0), 0.33, 14)                                        # acetylene head lamp
    Br.rod(W, (1.6, -1.65, 2.6), (1.6, -1.65, 4.1), 0.035, 6)                                 # brake/change lever
    Br.rod(W, (1.4, -1.68, 2.6), (1.35, -1.68, 3.9), 0.035, 6)
    if hood:                                                                                  # folded cape-cart hood on the back
        Lm.rod(W, (-4.0, -1.9, 4.6), (-4.0, 1.9, 4.6), 0.35, 12)

def car_voiturette(x, y, yaw, paint, leather, seed=0):
    """generic two-seat voiturette, single-cyl 6-9 h.p. class (I): wheelbase 5 ft 9 in, 28 in wheels"""
    W = placement(x, y, yaw)
    WB, TR = 5.75, 3.9
    for wx in (WB/2, -WB/2):
        for s in (1, -1): wheel(W, wx, s*TR/2, 0, 2.35, 0.24, 10)
    S = B('steel', M['steel'])
    for s in (1, -1): S.box(W, -3.3, 3.5, s*1.05 - 0.08, s*1.05 + 0.08, 1.35, 1.65)
    S.cyl_y(W, WB/2, 0, 1.175, 0.08, TR, 8); S.cyl_y(W, -WB/2, 0, 1.175, 0.09, TR, 8)
    Pn = B('paint_' + paint.name, paint); Lm = B('leather_' + leather.name, leather); Br = B('brass', M['brass'])
    Br.box(W, 3.3, 3.45, -0.75, 0.75, 1.6, 3.0)
    Pn.box(W, 1.9, 3.3, -0.75, 0.75, 1.65, 2.75); Pn.rod(W, (1.9, 0, 2.75), (3.3, 0, 2.75), 0.75, 14)
    B('wood', M['wood']).box(W, 1.75, 1.9, -1.25, 1.25, 1.65, 3.3)
    Pn.box(W, -2.9, 1.75, -1.35, 1.35, 1.65, 2.85)
    Lm.box(W, -1.6, 0.4, -1.25, 1.25, 2.75, 3.1); Lm.box(W, -2.0, -1.6, -1.3, 1.3, 2.8, 4.1)
    G = B('steel', M['steel'])
    for wx in (WB/2, -WB/2):
        for s in (1, -1): G.arc_strip(W, wx, 1.175, 1.35, 20, 160, s*(TR/2 - 0.3), s*(TR/2 + 0.3), 0.05, 10)
    Br.rod(W, (1.3, -0.45, 1.8), (0.55, -0.45, 3.7), 0.06, 8)
    steering_wheel(W, (1.3, -0.45, 1.8), (0.52, -0.45, 3.75), 0.6)
    for s in (1, -1): Br.rod(W, (1.8, s*1.3, 2.9), (1.8, s*1.3, 3.35), 0.17, 10)

def chassis(x, y, yaw, seed=0):
    """bare 4-cyl chassis on its wheels (68 chassis shown, Grace's Guide R; form I): engine, gearbox, chains exposed"""
    W = placement(x, y, yaw)
    WB, TR = 7.5, 4.4
    for (wx, D) in ((WB/2, 2.75), (-WB/2, 2.83)):
        for s in (1, -1): wheel(W, wx, s*TR/2, 0, D)
    S = B('steel', M['steel']); I = B('iron', M['iron']); A = B('alu', M['alu']); Br = B('brass', M['brass'])
    for s in (1, -1): S.box(W, -4.7, 4.75, s*1.3 - 0.1, s*1.3 + 0.1, 1.55, 1.95)
    for xx in (-4.2, -1.0, 1.8, 4.4): S.box(W, xx - 0.1, xx + 0.1, -1.3, 1.3, 1.6, 1.85)
    S.cyl_y(W, WB/2, 0, 1.375, 0.09, TR, 8); S.cyl_y(W, -WB/2, 0, 1.415, 0.11, TR, 8)
    A.box(W, 2.1, 4.2, -0.75, 0.75, 1.6, 2.1)                                                  # crankcase
    for k in range(4): I.rod(W, (2.35 + k*0.5, 0, 2.05), (2.35 + k*0.5, 0, 3.1), 0.24, 12)     # four cylinders
    Br.rod(W, (2.2, 0.35, 3.1), (4.1, 0.35, 3.1), 0.05, 6)                                     # induction pipe
    Br.box(W, 4.55, 4.78, -1.0, 1.0, 1.85, 4.0); B('core', M['core']).box(W, 4.76, 4.80, -0.85, 0.85, 2.0, 3.85)
    A.box(W, -0.6, 1.3, -0.5, 0.5, 1.5, 2.1)                                                   # gearbox
    S.cyl_y(W, -0.2, 0, 1.75, 0.08, 3.4, 8)                                                    # countershaft
    for s in (1, -1):
        I.cyl_y(W, -0.2, s*1.75, 1.75, 0.32, 0.06, 18); I.cyl_y(W, -WB/2, s*1.75, 1.415, 0.62, 0.06, 24)   # chain sprockets
        S.rod(W, (-0.2, s*1.75, 2.07), (-WB/2, s*1.75, 2.03), 0.035, 4); S.rod(W, (-0.2, s*1.75, 1.43), (-WB/2, s*1.75, 0.8), 0.035, 4)
    B('wood', M['wood']).box(W, 1.85, 2.0, -1.4, 1.4, 1.9, 3.6)
    Br.rod(W, (1.45, -0.55, 2.0), (0.45, -0.55, 4.25), 0.07, 8)
    steering_wheel(W, (1.45, -0.55, 2.0), (0.42, -0.55, 4.3), 0.72)

def stand(x0, x1, side, baize):
    """exhibitor stand: 6 in deal platform with baize, white front rail on turned posts + crimson rope, blank fascia board
    on two posts at the gangway edge (I; no invented maker names / prices)"""
    s = 1 if side > 0 else -1
    yi, yo = s*13.0, s*33.5                     # gangway edge / back (column line at 36)
    y0, y1 = min(yi, yo), max(yi, yo)
    D = B('deal', M['deal']); Bz = B('baize_' + baize.name, baize); R = B('rail', M['rail']); Rp = B('rope', M['rope'])
    D.box(Matrix(), x0, x1, y0, y1, 0, 0.42); Bz.box(Matrix(), x0 + 0.1, x1 - 0.1, y0 + 0.1, y1 - 0.1, 0.42, 0.5)
    np_ = int((x1 - x0) // 4.5)
    xs = [x0 + 0.5 + k * (x1 - x0 - 1.0) / np_ for k in range(np_ + 1)]
    for k, xp in enumerate(xs):
        if k in (np_ // 2,): continue           # way onto the stand
        R.rod(Matrix(), (xp, yi, 0.5), (xp, yi, 3.0), 0.09, 8); R.rod(Matrix(), (xp, yi, 3.0), (xp, yi, 3.15), 0.14, 8)
    for k in range(np_):
        if k in (np_ // 2 - 1, np_ // 2): continue
        Rp.rod(Matrix(), (xs[k], yi, 2.7), ((xs[k] + xs[k+1]) / 2, yi, 2.35), 0.05, 6); Rp.rod(Matrix(), ((xs[k] + xs[k+1]) / 2, yi, 2.35), (xs[k+1], yi, 2.7), 0.05, 6)
    Fs = B('fascia', M['fascia']); Lt = B('letter', M['letter'])
    xm = (x0 + x1) / 2; fw = min(18.0, x1 - x0 - 3); yb = yo - s*0.6        # name board at the back of the stand, facing the gangway
    for xp in (xm - fw/2 + 0.4, xm + fw/2 - 0.4): Fs.rod(Matrix(), (xp, yb, 0.5), (xp, yb, 11.6), 0.14, 8)
    Fs.box(Matrix(), xm - fw/2, xm + fw/2, yb - 0.15, yb + 0.15, 9.4, 11.6)
    yf = yb - s*0.17
    Lt.box(Matrix(), xm - fw/2 + 0.25, xm + fw/2 - 0.25, yf - 0.03, yf + 0.03, 9.65, 9.75)   # gilt lines, no lettering
    Lt.box(Matrix(), xm - fw/2 + 0.25, xm + fw/2 - 0.25, yf - 0.03, yf + 0.03, 11.25, 11.35)
    for xp in (xm - fw/2 + 0.25, xm + fw/2 - 0.35): Lt.box(Matrix(), xp, xp + 0.1, yf - 0.03, yf + 0.03, 9.65, 11.35)

# ------------------------------------------------------------------ 0. hide placeholders / later-dated pieces (kept in file)
HIDDEN = []
def hide(o, why):
    o.hide_render = True; o.hide_viewport = True; o['cp051_hidden_by_candidate'] = why; HIDDEN.append(o.name)
for o in list(bpy.data.objects):
    if o.name.startswith(('PLACEHOLDER_nave_tree_', 'PLACEHOLDER_nave_palm_')):
        try: xs = [(o.matrix_world @ Vector(c)).x / F for c in o.bound_box]
        except Exception: continue
        if max(xs) < -30 and min(xs) > -420: hide(o, 'west-nave planting placeholder (stand space)')
    if o.name in ('late11_flagpoles', 'late11_flags_red', 'late11_flags_white', 'late11_flags_blue',
                  'cov_plymouth_poles', 'cov_plymouth_flag_red', 'cov_plymouth_flag_white', 'cov_plymouth_flag_blue'):
        hide(o, 'later-dated (1911 / 1913) flags read through the glazing')
print('CP051 hidden', len(HIDDEN), HIDDEN)

# r16 'tech exhibit cabinets' (gold boxes, z < 9 ft) removed from a copy of cov_electric_fittings; pendants kept
ef = bpy.data.objects['cov_electric_fittings']
me = ef.data.copy(); me.name = 'cov_electric_fittings_cp051'; ef.data = me
bm = bmesh.new(); bm.from_mesh(me)
dead = [v for v in bm.verts if (ef.matrix_world @ v.co).z / F < 9.0]
bmesh.ops.delete(bm, geom=dead, context='VERTS'); bm.to_mesh(me); bm.free(); me.update()
ef['cp051_removed_cabinet_verts'] = len(dead)
print('CP051 cabinet verts removed', len(dead))

# stray nave-interior crowd points (duplicated across the three GN crowds)
for n in ('ppl11_festival_crowd', 'ppl11_reglazing_gang', 'ppl13_plymouth_rescue_crowd'):
    pp = bpy.data.objects[n]
    me = pp.data.copy(); me.name = n + '_cp051'; pp.data = me
    bm = bmesh.new(); bm.from_mesh(me); mw = pp.matrix_world
    dead = [v for v in bm.verts if -360 < (mw @ v.co).x / F < -30 and abs((mw @ v.co).y / F) < 40]
    bmesh.ops.delete(bm, geom=dead, context='VERTS'); bm.to_mesh(me); bm.free(); me.update()
    pp['cp051_removed_nave_points'] = len(dead)
    print('CP051 removed stray nave points', n, len(dead), 'left', len(me.vertices))

# ------------------------------------------------------------------ 1. stands + cars, west nave x -258..-42 (9 bays), both sides
LEATH = [M['leather_b'], M['leather_r'], M['leather_g']]
bays = [(-258 + i * BAY, -258 + (i + 1) * BAY) for i in range(9)]
NCARS = [0]
def put_car(kind, x, y, yaw, seed):
    p = PAINTS[seed % len(PAINTS)]; l = LEATH[(seed // 2) % 3]
    if kind == 'T': car_tonneau(x, y, yaw, p, l, seed, hood=False)
    elif kind == 'V': car_voiturette(x, y, yaw, p, l, seed)
    else: chassis(x, y, yaw, seed)
    NCARS[0] += 1
LAYOUT_L = ['TV', 'TC', 'VT', 'TT', 'CV', 'TV', 'VT', 'TC', 'TV']
LAYOUT_R = ['T', 'VT', 'TC', 'VV', 'TT', 'CT', 'TV', 'VT', 'TT']
for i, (x0, x1) in enumerate(bays):
    for side, lay in ((1, LAYOUT_L[i]), (-1, LAYOUT_R[i])):
        stand(x0 + 0.8, x1 - 0.8, side, M['baize_r'] if (i + (side > 0)) % 2 else M['baize_g'])
        n = len(lay)
        for k, kind in enumerate(lay):
            if n == 1: cx, cy, yaw = (x0 + x1) / 2 + 7.0, side * 23.0, (180 + side * 32)   # hero: nose angled toward the gangway
            else:
                cx = x0 + (k + 0.5) * (x1 - x0) / n
                cy = side * (20.5 if k % 2 == 0 else 26.5)
                yaw = side * (-90 + (25 if k % 2 == 0 else -18))
            put_car(kind, cx, cy, yaw, 100 * i + 10 * k + (side > 0))
for b in list(_B.values()): b.done()
print('CP051 stands', len(bays) * 2, 'cars', NCARS[0])

# ------------------------------------------------------------------ 2. visitors + stand attendants (people_lib 1890s roles as the 1900s stand-in, as CP054)
NPEOPLE = [0]
def person(name, role, pose, x, y, face, seed, z=0.0):
    person_mesh(name, role, style={'role': role, 'pose': pose, 'lod': 'mid', 'era': '1890s'}, seed=seed)
    o = bpy.data.objects[name]
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o)
    o.location = (x * F, y * F, z * F)
    o.rotation_euler = (0, 0, math.atan2(face[0], -face[1]))
    o['cp_state'] = STATE; o['cpl_people'] = 'cpl_people_v3'; NPEOPLE[0] += 1
    return o
# camera (-280, -20, 7.2): nearest figure ~70 ft; gangway |y| < 12
k = 0
for i in range(46):
    x = RNG.uniform(-212, -50); y = RNG.uniform(-10.5, 10.5)
    role = '1890s_lady' if RNG.random() < 0.42 else '1890s_gentleman'
    pose = 'walking' if RNG.random() < 0.55 else ('pointing' if RNG.random() < 0.15 else 'standing')
    a = RNG.uniform(0, 2 * math.pi)
    face = (math.cos(a), math.sin(a)) if pose != 'walking' else ((1, RNG.uniform(-0.3, 0.3)) if RNG.random() < 0.5 else (-1, RNG.uniform(-0.3, 0.3)))
    person(f'cp051_visitor_{i:02d}', role, pose, x, y, face, 51000 + i)
# attendants / buyers on the stands beside cars (z = 0.5 ft platform)
for i, (x0, x1) in enumerate(bays[2:], start=2):
    for side in (1, -1):
        if RNG.random() < 0.7:
            person(f'cp051_stand_{i}_{"L" if side > 0 else "R"}', '1890s_gentleman', 'standing', RNG.uniform(x0 + 3, x1 - 3), side * RNG.uniform(15.5, 17.5), (0, -side), 51500 + i * 2 + (side > 0), z=0.5)
# a few visitors walking the garden-side aisle outside the column line (nearest ~85 ft)
for i in range(8):
    person(f'cp051_aisle_{i}', '1890s_lady' if i % 3 == 0 else '1890s_gentleman', 'walking', RNG.uniform(-205, -110), RNG.uniform(-56, -41), (1 if i % 2 else -1, 0), 51700 + i)
print('CP051 BUILT people', NPEOPLE[0])

if OUT != '--nosave':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP051 SAVED', OUT)
