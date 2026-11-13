"""CANDIDATE r06 (2026-11-13): CP034b Dinner in the Iguanodon, 31 Dec 1853 -- one-scene polish on live r05.
Source: ILN 7 Jan 1854 woodcut (refs/ILN1854_dinner_in_the_iguanodon_PD.jpg) + accounts (21 diners in the mould, Owen at the head).
Changes ONLY inside collection DN53_iguanodon_dinner__31Dec1853 (off-site set at x = 3000 ft); new objects are prefixed DN53c_.
 1 marquee enclosed: boarded hoarding walls (back y=+22, ends x=+-34) up to 21 ft, striped red/cream valance 21-26 ft under the
   existing canopy, boarded marquee floor over the yard grass (print: boarded walls, striped tent, plank floor).
 2 diners re-seated INSIDE the mould: 10 a side + Owen at the head = 21 (R), bare-headed (print), seated so only chest/head show
   above the rim; the old standing top-hatted guests (legs visible under the belly, front row outside the mould wall) are hidden.
 3 old inner floor plank (poked out of the narrow neck as a floating bench), old table and legs removed from the combined deck mesh and
   rebuilt inside the measured mould interior (per-1-ft slice half-widths), tablecloth + plates + glasses.
 4 name boards BUCKLAND / CUVIER / OWEN / MANTELL (R, print) lettered, lowered from 22-24.5 ft (out of frame) to the wall top;
   chandelier rebuilt lower (16.5 ft) with gas globes; evergreen festoon on the back wall; folding screen behind Owen (print);
   three waiters with trays on the deck (print).
Nothing outside the dinner collection is touched. Refuses to overwrite r05 and refuses a source that already has DN53c_ objects.
usage: blender -b -P scripts/cand_cp034b_dinner_20261113.py
"""
import bpy, bmesh, math, os, random, collections
from mathutils import Vector, Matrix
BASE = '/workspace/crystal-palace-dinosaurs/course-models/crystal-palace-dinosaurs-1854-grok'
SRC = os.path.join(BASE, 'rounds/dinosaurs-1854-r05.blend')
OUT = os.path.join(BASE, 'rounds/dinosaurs-1854-r06-cand.blend')
assert os.path.abspath(OUT) != os.path.abspath(SRC)
bpy.ops.wm.open_mainfile(filepath=SRC)
assert not [o for o in bpy.data.objects if o.name.startswith('DN53c_')], 'source already has candidate objects'
F = 0.3048; DX = 3000.0
def f(v): return v * F
CD = bpy.data.collections['DN53_iguanodon_dinner__31Dec1853']
M = {k: bpy.data.materials[n] for k, n in dict(plaster='plaster_mould_white', timber='deal_boards_weathered', linen='table_linen',
     red='marquee_stripe_red', cream='marquee_stripe_cream', brass='brass_chandelier', coat='frock_coat_black', skin='skin',
     shirt='shirt_white', foliage='foliage').items()}
def newmat(name, rgb, rough=0.6, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough
    if emit: b.inputs['Emission Color'].default_value = (*rgb, 1); b.inputs['Emission Strength'].default_value = emit
    return m
M['hoard'] = newmat('DN53c_hoarding_deal_painted', (0.27, 0.21, 0.14), 0.85)
M['hoard2'] = newmat('DN53c_hoarding_deal_painted_b', (0.22, 0.17, 0.11), 0.85)
M['board'] = newmat('DN53c_nameboard_cream', (0.78, 0.72, 0.58), 0.7)
M['globe'] = newmat('DN53c_gas_globe', (1.0, 0.82, 0.55), 0.3, emit=6.0)
M['hair'] = newmat('DN53c_hair_dark', (0.05, 0.04, 0.03), 0.7)
M['glass'] = newmat('DN53c_wine_glass', (0.85, 0.85, 0.8), 0.1)

# ---------- helpers (feet) ----------
def box(bm, x0, x1, y0, y1, z0, z1, mi=0):
    r = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector(((x0+x1)/2, (y0+y1)/2, (z0+z1)/2))*F) @ Matrix.Diagonal(Vector((f(x1-x0), f(y1-y0), f(z1-z0), 1))), verts=r['verts'])
    for fc in {fc for v in r['verts'] for fc in v.link_faces}: fc.material_index = mi
def strut(bm, a, b, r, mi=0, seg=6):
    a, b = Vector(a), Vector(b); d = b - a
    res = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=f(r), radius2=f(r), depth=f(d.length))
    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
    bmesh.ops.transform(bm, matrix=Matrix.Translation((a + b) / 2 * F) @ q.to_matrix().to_4x4(), verts=res['verts'])
    for fc in {fc for v in res['verts'] for fc in v.link_faces}: fc.material_index = mi
def lathe(bm, prof, seg, mi, cx=0.0, cy=0.0, sx=1.0):
    rings = []
    for r, z in prof:
        if r <= 1e-4: rings.append([bm.verts.new((f(cx), f(cy), f(z)))])
        else: rings.append([bm.verts.new((f(cx + sx*r*math.cos(2*math.pi*i/seg)), f(cy + r*math.sin(2*math.pi*i/seg)), f(z))) for i in range(seg)])
    for a, b in zip(rings, rings[1:]):
        if len(a) == 1 and len(b) == 1: continue
        if len(a) == 1: fs = [bm.faces.new((a[0], b[i], b[(i+1) % seg])) for i in range(seg)]
        elif len(b) == 1: fs = [bm.faces.new((a[i], a[(i+1) % seg], b[0])) for i in range(seg)]
        else: fs = [bm.faces.new((a[i], a[(i+1) % seg], b[(i+1) % seg], b[i])) for i in range(seg)]
        for fc in fs: fc.material_index = mi; fc.smooth = True
def sub(bm, fn, mat):
    """build a part in its own bmesh, transform ALL its verts, append to bm (bmesh op vert order is not append-only)"""
    tb = bmesh.new(); fn(tb); bmesh.ops.transform(tb, matrix=mat, verts=tb.verts[:])
    me = bpy.data.meshes.new('_tmp'); tb.to_mesh(me); tb.free(); bm.from_mesh(me); bpy.data.meshes.remove(me)
def at(x, y, z, rot=0.0, k=1.0): return Matrix.Translation(Vector((f(x), f(y), f(z)))) @ Matrix.Rotation(rot, 4, 'Z') @ Matrix.Scale(k, 4)
def sphere(bm, x, y, z, r, mi=0, sd=1):
    def fn(tb):
        res = bmesh.ops.create_icosphere(tb, subdivisions=sd, radius=f(r))
        for fc in tb.faces: fc.material_index = mi; fc.smooth = True
    sub(bm, fn, at(x, y, z))
def mk(name, fn, mats):
    bm = bmesh.new(); fn(bm); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    o = bpy.data.objects.new(name, me); CD.objects.link(o); return o

LOG = []
# ---------- 0. measure the mould interior per 1-ft slice ----------
mo = bpy.data.objects['iguanodon_mould_open']
S = collections.defaultdict(list)
for v in mo.data.vertices:
    w = mo.matrix_world @ v.co; S[int(math.floor(w.x / F - DX))].append((w.y / F, w.z / F))
def inner(x, z0, z1):
    k = int(math.floor(x)); pts = S.get(k, [])
    if not pts: return 0.0, 0.0
    ys = [a for a, b in pts]; yc = (min(ys) + max(ys)) / 2
    m = [abs(a - yc) for a, b in pts if z0 <= b <= z1 and abs(a - yc) > 0.6]   # ignore interior leg/cap verts near the axis
    return yc, (min(m) if m else 0.0)
RIM = max(b for pts in S.values() for a, b in pts if True)
LOG.append(f'mould rim max z {RIM:.2f} ft')

# ---------- 1. remove old floor plank / table / legs / chandelier / name boards from the combined deck mesh ----------
dk = bpy.data.objects['dinner_deck_marquee_table']
bm = bmesh.new(); bm.from_mesh(dk.data); bm.verts.ensure_lookup_table()
seen = set(); removed = collections.Counter(); kill = []
for v in bm.verts:
    if v.index in seen: continue
    isl = []; st = [v]; seen.add(v.index)
    while st:
        a = st.pop(); isl.append(a)
        for e in a.link_edges:
            b = e.other_vert(a)
            if b.index not in seen: seen.add(b.index); st.append(b)
    xs = [p.co.x / F - DX for p in isl]; ys = [p.co.y / F for p in isl]; zs = [p.co.z / F for p in isl]
    x0, x1, y0, y1, z0, z1 = min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)
    tag = None
    if abs(z0 - 7.4) < 0.05 and abs(z1 - 7.9) < 0.05 and x0 < -12: tag = 'inner_floor_plank'
    elif abs(z0 - 10.1) < 0.05 and abs(z1 - 10.4) < 0.05: tag = 'table_top'
    elif z0 > 7.7 and z1 < 10.3 and abs(y0) < 1.6 and x1 - x0 < 0.6: tag = 'table_leg'
    elif z0 > 19.5 and abs((x0 + x1) / 2 + 1) < 3.5 and abs((y0 + y1) / 2) < 3.5 and z1 < 33: tag = 'chandelier'
    elif y0 > 21.4 and z0 > 21.9 and z1 < 24.6: tag = 'name_board_blank'
    if tag:
        removed[tag] += 1; kill.extend(isl)
bmesh.ops.delete(bm, geom=kill, context='VERTS')
bm.to_mesh(dk.data); bm.free()
LOG.append(f'removed from dinner_deck_marquee_table: {dict(removed)}')
# hide the old standing guests (kept in file for reversibility)
g = bpy.data.objects['dinner_guests_21']; g.hide_render = True; g.hide_viewport = True
LOG.append('hidden: dinner_guests_21 (old standing top-hatted figures)')

# ---------- 2. mould floor + table inside measured interior ----------
TX0, TX1 = -8.6, 5.6
def floor_table(bm):
    for k in range(-9, 6):
        yc, hw = inner(k + 0.5, 7.4, 8.2)
        if hw - 0.15 >= 0.8: box(bm, DX + k, DX + k + 1, yc - (hw - 0.15), yc + (hw - 0.15), 7.45, 7.75, 0)
    x = TX0
    while x < TX1 - 1e-6:
        x2 = min(TX1, x + 1.0); yc, _ = inner((x + x2) / 2, 8.5, 10)
        box(bm, DX + x, DX + x2, yc - 0.85, yc + 0.85, 10.05, 10.2, 1)              # table top + cloth
        for s in (-1, 1): box(bm, DX + x, DX + x2, yc + s*0.85 - 0.02, yc + s*0.85 + 0.02, 9.55, 10.2, 1)   # cloth drop
        x = x2
    for xx in (TX0, TX1): box(bm, DX + xx - 0.02, DX + xx + 0.02, -0.87, 0.87, 9.55, 10.2, 1)
mk('DN53c_mould_floor_and_table', floor_table, [M['timber'], M['linen']])

# ---------- 3. 21 seated diners (bare-headed, ILN print) ----------
rr = random.Random(18531231)
SEATS = []
xs = [TX0 + 0.75 + i * (TX1 - TX0 - 1.5) / 9 for i in range(10)]
for x in xs:
    yc, hw = inner(x, 8.5, 10)
    for s in (-1, 1):
        y = yc + s * min(1.75, hw - 0.6); SEATS.append((x, y, math.pi/2 if s < 0 else -math.pi/2, hw))
yc, hw = inner(TX1 + 0.9, 8.5, 10); SEATS.append((TX1 + 0.9, yc, math.pi, hw))   # Owen at the head (R), facing down the table
def seated(bm0, x, y, rot, rr):
  k = rr.uniform(0.94, 1.04); h = 8.6
  def fn(bm):
    lathe(bm, [(0, 0), (0.5, 0.02), (0.55, 0.6), (0.58, 1.45), (0.5, 1.8), (0.24, 1.95), (0, 1.98)], 10, 0, sx=0.75)   # frock coat torso
    lathe(bm, [(0, 1.2), (0.2, 1.25), (0.2, 1.85), (0, 1.9)], 6, 2, cx=0.36)                                       # shirt front
    lathe(bm, [(0, 1.86), (0.27, 1.92), (0.31, 2.2), (0.27, 2.5), (0, 2.58)], 8, 1)                               # head
    lathe(bm, [(0.29, 2.22), (0.33, 2.42), (0.22, 2.6), (0, 2.63)], 8, 3, cx=-0.05)                                # hair
    for s in (-1, 1):
        strut(bm, (0.05, s*0.52, 1.7), (0.55, s*0.5, 1.25), 0.14, 0, 5)                                           # upper arm
        strut(bm, (0.55, s*0.5, 1.25), (1.0, s*0.32, 1.55), 0.12, 0, 5)                                           # forearm to table
  sub(bm0, fn, at(DX + x, y, h, rot, k))
def diners(bm):
    for x, y, rot, hw in SEATS: seated(bm, x, y, rot, rr)
mk('DN53c_diners_21_seated', diners, [M['coat'], M['skin'], M['shirt'], M['hair']])
def tableware(bm):
    for x, y, rot, hw in SEATS:
        d = Vector((math.cos(rot), math.sin(rot), 0)); p = Vector((x, y, 0)) + d * 1.05
        p = p + Vector((DX, 0, 0)); lathe(bm, [(0, 10.2), (0.36, 10.21), (0.4, 10.25), (0, 10.24)], 10, 0, cx=p.x, cy=p.y)
        q = p + d * 0.25 + Vector((-d.y, d.x, 0)) * 0.35
        lathe(bm, [(0, 10.2), (0.1, 10.21), (0.02, 10.25), (0.02, 10.38), (0.08, 10.42), (0.09, 10.55), (0, 10.5)], 6, 1, cx=q.x, cy=q.y)
    for k in range(4):   # decanters + epergne down the table centre
        x = TX0 + 1.8 + k * 3.4; yc, _ = inner(x, 8.5, 10)
        lathe(bm, [(0, 10.2), (0.22, 10.25), (0.28, 10.5), (0.08, 10.8), (0.08, 11.0), (0, 11.02)], 8, 1, cx=DX + x, cy=yc)
mk('DN53c_tableware', tableware, [M['shirt'], M['glass']])
LOG.append(f'seated diners: {len(SEATS)} (min seat clearance to mould wall {min(hw - abs(y - inner(x, 8.5, 10)[0]) - 0.55 for x, y, r, hw in SEATS):.2f} ft)')

# ---------- 4. marquee enclosure: boarded hoarding + striped valance + plank floor ----------
WX, WY, WH = 34.0, 22.0, 21.0
def hoarding(bm):
    rb = random.Random(7)
    def wall(axis, c, a0, a1, face):
        a = a0
        while a < a1 - 1e-6:
            w = min(0.72, a1 - a); d = rb.uniform(0.18, 0.26); mi = rb.random() < 0.5
            if axis == 'y': box(bm, DX + a, DX + a + w - 0.04, c - face*d, c, 0.0, WH, mi)
            else: box(bm, DX + c - face*d, DX + c, a, a + w - 0.04, 0.0, WH, mi)
            a += w
        for zz in (3.0, 11.0, WH - 0.6):   # rails
            if axis == 'y': box(bm, DX + a0, DX + a1, c - face*0.45, c - face*0.2, zz, zz + 0.5, 0)
            else: box(bm, DX + c - face*0.45, DX + c - face*0.2, a0, a1, zz, zz + 0.5, 0)
    wall('y', WY, -WX, WX, 1)          # back wall, inner face toward -y
    wall('x', WX, -WY + 4, WY, 1)      # east end (frame right)
    wall('x', -WX, -WY + 4, WY, -1)    # west end
mk('DN53c_marquee_hoarding', hoarding, [M['hoard'], M['hoard2']])
def valance(bm):
    k = 0; a = -WX
    while a < WX - 1e-6:
        box(bm, DX + a, DX + a + 1.5, WY - 0.45, WY - 0.3, WH - (0.8 if k % 2 else 0.0), 26.0, 0 if k % 2 else 1); a += 1.5; k += 1
    for c in (WX, -WX):
        k = 0; a = -WY + 4
        while a < WY - 1e-6:
            sg = 1 if c > 0 else -1
            box(bm, DX + c - sg*0.45, DX + c - sg*0.3, a, a + 1.5, WH - (0.8 if k % 2 else 0.0), 26.0, 0 if k % 2 else 1); a += 1.5; k += 1
mk('DN53c_marquee_valance_striped', valance, [M['red'], M['cream']])
def mfloor(bm):
    a = -WY
    while a < WY - 1e-6:
        box(bm, DX - WX, DX + WX, a, a + 0.7, 0.0, 0.12 if int(a / 0.7) % 2 else 0.1, int(a / 0.7) % 2); a += 0.72
mk('DN53c_marquee_plank_floor', mfloor, [M['timber'], M['hoard2']])

# ---------- 5. name boards (lettered), festoon, chandelier, screen, waiters ----------
NAMES = [('BUCKLAND', -22.0), ('CUVIER', -6.0), ('OWEN', 10.0), ('MANTELL', 26.0)]
def boards(bm):
    for nm, x in NAMES:
        sub(bm, lambda tb: bmesh.ops.create_cone(tb, cap_ends=True, segments=24, radius1=1.0, radius2=1.0, depth=1.0),
            Matrix.Translation(Vector((f(DX + x), f(WY - 0.55), f(18.2)))) @ Matrix.Rotation(math.pi/2, 4, 'X') @ Matrix.Diagonal(Vector((f(4.6), f(1.4), f(0.12), 1))))
        strut(bm, (DX + x - 4.6, WY - 0.5, 18.2), (DX + x + 4.6, WY - 0.5, 18.2), 0.06, 1, 4)
mk('DN53c_name_boards', boards, [M['board'], M['brass']])
for nm, x in NAMES:
    cu = bpy.data.curves.new('DN53c_lettering_' + nm, 'FONT'); cu.body = nm; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
    cu.size = f(1.25); cu.extrude = f(0.03); cu.materials.append(M['coat'])
    o = bpy.data.objects.new('DN53c_lettering_' + nm, cu); CD.objects.link(o)
    o.location = (f(DX + x), f(WY - 0.75), f(18.2)); o.rotation_euler = (math.pi/2, 0, 0)
def festoon(bm):
    nails = [-30, -18, -6, 6, 18, 30]
    for a, b in zip(nails, nails[1:]):
        for i in range(24):
            t = i / 23; x = a + (b - a) * t; z = 15.6 - 1.6 * math.sin(math.pi * t)
            sphere(bm, DX + x, WY - 0.6, z, 0.32)
    for i in range(30):   # second festoon slung over the table (print)
        t = i / 29; x = -10 + 20 * t; z = 16.0 - 1.2 * math.sin(math.pi * t)
        sphere(bm, DX + x, 2.0, z, 0.25)
mk('DN53c_evergreen_festoons', festoon, [M['foliage']])
CH = (DX - 1, 0.0, 16.5)
def chandelier(bm):
    strut(bm, (CH[0], 0, 30), (CH[0], 0, CH[2] + 1.2), 0.06, 0, 4)
    lathe(bm, [(0, CH[2] + 1.2), (0.5, CH[2] + 0.9), (0.3, CH[2]), (0.6, CH[2] - 0.4), (0, CH[2] - 0.7)], 10, 0, cx=CH[0])
    for k in range(10):
        a = 2*math.pi*k/10; p = (CH[0] + 2.2*math.cos(a), 2.2*math.sin(a), CH[2] + 0.2)
        strut(bm, (CH[0], 0, CH[2] - 0.2), p, 0.06, 0, 4)
        sphere(bm, p[0], p[1], p[2] + 0.3, 0.28, 1, 2)
mk_ch = mk('DN53c_chandelier', chandelier, [M['brass'], M['globe']])
# globes = icospheres: assign globe material to faces of small spheres (all faces above arm ends)
lt = bpy.data.lights.new('DN53c_chandelier_gas', 'POINT'); lt.energy = 1500; lt.color = (1.0, 0.7, 0.4); lt.shadow_soft_size = f(2.0)
lo = bpy.data.objects.new('DN53c_chandelier_gas', lt); CD.objects.link(lo); lo.location = (f(CH[0]), 0, f(CH[2] + 0.4))
def screen(bm):
    x0 = DX + 16.0   # beyond the mould tail end (x +14), behind Owen's end (print)
    for i in range(5):
        y0 = -4.0 + i * 1.6; xx = x0 + (0.25 if i % 2 else 0.0)
        box(bm, xx, xx + 0.12, y0, y0 + 1.55, 4.0, 11.5, 0)
        box(bm, xx - 0.05, xx + 0.17, y0, y0 + 1.55, 11.3, 11.6, 1)
mk('DN53c_folding_screen', screen, [M['board'], M['timber']])
def waiter(bm0, x, y, rot):
  def fn(bm):
    for s in (-0.25, 0.25): lathe(bm, [(0.17, 0), (0.18, 1.3), (0.2, 2.7), (0, 2.75)], 6, 0, cy=s)
    lathe(bm, [(0, 2.4), (0.55, 2.4), (0.58, 3.3), (0.56, 4.3), (0.4, 4.7), (0, 4.76)], 9, 0)
    lathe(bm, [(0, 1.6), (0.5, 1.6), (0.6, 3.6), (0, 3.62)], 8, 2, cx=0.12)                 # white apron
    lathe(bm, [(0, 4.72), (0.3, 4.8), (0.34, 5.1), (0.28, 5.4), (0, 5.48)], 8, 1)
    lathe(bm, [(0.32, 5.05), (0.36, 5.3), (0.24, 5.5), (0, 5.53)], 8, 4, cx=-0.05)   # hair
    for s in (-1, 1): strut(bm, (0, s*0.62, 4.4), (0.75, s*0.4, 3.9), 0.15, 0, 5)
    lathe(bm, [(0, 4.05), (0.9, 4.05), (0.95, 4.12), (0, 4.12)], 12, 3, cx=0.9)               # tray
    lathe(bm, [(0, 4.12), (0.55, 4.12), (0.4, 4.6), (0, 4.75)], 10, 3, cx=0.9)                # dish cover
  sub(bm0, fn, at(x, y, 4.0, rot))
def waiters(bm):
    waiter(bm, DX - 9.0, -9.5, math.radians(60)); waiter(bm, DX - 1.0, -13.5, math.radians(90)); waiter(bm, DX + 13.0, -6.0, math.radians(150))
mk('DN53c_waiters_3', waiters, [M['coat'], M['skin'], M['shirt'], M['brass'], M['hair']])
for o in CD.objects:
    if o.name.startswith('DN53c_'): o['cand'] = 'r06 CP034b dinner 2026-11-13'
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
for l in LOG: print('LOG', l)
print('CAND_OK', OUT)
