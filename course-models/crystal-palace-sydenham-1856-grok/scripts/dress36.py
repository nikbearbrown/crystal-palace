# r12 PPL-20C + 1936 dressing (exec'd from states.py; shares build.py's namespace: f, MB, coll, mat, cam, gz, UT, LT,
# yU, yL, STATE, EYE, HALF, BANK ...). Units feet unless noted. Everything here is a stand-in: grades in DEPARTURES r12.
#  * People: low-poly lathe figures in 1930s dress (overcoat + trilby / flat cap; mid-calf coat + cloche; Metropolitan
#    Police greatcoat + custodian helmet; LFB firemen in dark tunics, leggings, helmets). Lathe approach adapted from the
#    HP executor's figures.py `person_mesh` (read-only reference; no code imported). Crowds = "blocks" of ~36 people
#    merged once and placed as linked duplicates (shared mesh data) to keep the .blend small.
#  * Appliances: block-outs of a 1930s London Fire Brigade pump (Dennis/Leyland type, open cab, ladder on top) and a
#    Leyland-Metz 100 ft turntable ladder (TL). Proportions I (period photographs, no drawings in repo).
#  * Hoses, branch jets, police lines. Counts: 89 appliances and 438 firemen attended (LFB / Wikipedia, R) - only the
#    ones that the storyboard cameras see are modelled (I).
import bpy, bmesh, math, random
from mathutils import Vector, Matrix

D36 = random.Random(1936)
FTM = 0.3048

def _m(name, rgb, rough=0.6, metal=0.0):
    return bpy.data.materials.get(name) or mat(name, rgb, rough, metal)
PM = [_m('ppl36_coat_charcoal', (0.035, 0.035, 0.038), 0.85), _m('ppl36_coat_brown', (0.09, 0.06, 0.04), 0.85),
      _m('ppl36_coat_grey', (0.12, 0.12, 0.11), 0.85), _m('ppl36_coat_navy_police', (0.012, 0.014, 0.03), 0.8),
      _m('ppl36_trousers', (0.03, 0.03, 0.032), 0.85), _m('ppl36_skin', (0.55, 0.36, 0.27), 0.6),
      _m('ppl36_hat_dark', (0.025, 0.024, 0.024), 0.7), _m('ppl36_hat_felt_brown', (0.11, 0.08, 0.055), 0.75),
      _m('ppl36_lfb_tunic', (0.02, 0.02, 0.025), 0.75), _m('ppl36_lfb_helmet', (0.04, 0.035, 0.03), 0.35, 0.3),
      _m('ppl36_coat_camel', (0.32, 0.22, 0.12), 0.85), _m('ppl36_stockings', (0.25, 0.17, 0.12), 0.7),
      _m('ppl36_brass', (0.6, 0.42, 0.15), 0.35, 1.0)]
I_CHAR, I_BROWN, I_GREY, I_NAVY, I_TROU, I_SKIN, I_HATD, I_HATB, I_TUN, I_HELM, I_CAMEL, I_STOCK, I_BRASS = range(13)

def lathe(bm, prof, seg, mi, cx=0.0, cy=0.0):
    rings = [[bm.verts.new((FTM*(cx + r*math.cos(2*math.pi*k/seg)), FTM*(cy + r*math.sin(2*math.pi*k/seg)), FTM*z)) for k in range(seg)] for r, z in prof]
    for A, B in zip(rings, rings[1:]):
        for k in range(seg):
            if prof[rings.index(A)][0] == 0 and prof[rings.index(B)][0] == 0: continue
            fa = bm.faces.new([A[k], A[(k+1) % seg], B[(k+1) % seg], B[k]]); fa.material_index = mi
    if prof[-1][0] > 0: bm.faces.new(rings[-1]).material_index = mi
    if prof[0][0] > 0: bm.faces.new(list(reversed(rings[0]))).material_index = mi
def bbox(bm, x0, x1, y0, y1, z0, z1, mi, M_=None):
    vs = [Vector((x, y, z)) * FTM for x, y, z in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]]
    if M_ is not None: vs = [M_ @ v for v in vs]
    vs = [bm.verts.new(v) for v in vs]
    for q in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:
        bm.faces.new([vs[i] for i in q]).material_index = mi

def person(bm, kind, rng, ox=0.0, oy=0.0, rot=0.0, coat=None):
    """one 1930s figure into bm at (ox, oy) feet, facing -Y rotated by rot. kinds: man, woman, police, fireman."""
    v0 = len(bm.verts)
    k = rng.uniform(0.94, 1.05)
    if kind == 'woman':
        c = coat if coat is not None else rng.choice((I_CHAR, I_BROWN, I_GREY, I_CAMEL, I_NAVY))
        for s in (-0.22, 0.22): lathe(bm, [(0.13, 0.0), (0.14, 1.2), (0.0, 1.3)], 6, I_STOCK, cx=s)
        lathe(bm, [(0.0, 1.15), (0.62, 1.15), (0.55, 2.4), (0.5, 3.3), (0.6, 4.25), (0.38, 4.6), (0.0, 4.65)], 9, c)   # mid-calf coat
        for s in (-0.58, 0.58): lathe(bm, [(0.15, 2.9), (0.16, 4.3), (0.0, 4.4)], 5, c, cx=s)
        lathe(bm, [(0.0, 4.6), (0.27, 4.68), (0.32, 4.95), (0.26, 5.15), (0.0, 5.2)], 8, I_SKIN)
        lathe(bm, [(0.0, 4.88), (0.38, 4.88), (0.36, 5.0), (0.33, 5.3), (0.18, 5.42), (0.0, 5.44)], 8, rng.choice((I_HATD, I_HATB, I_NAVY)))  # cloche
        h = 5.4
    else:
        c = {'police': I_NAVY, 'fireman': I_TUN}.get(kind) if coat is None else coat
        if c is None: c = rng.choice((I_CHAR, I_CHAR, I_BROWN, I_GREY, I_GREY, I_CAMEL, I_NAVY))
        legm = I_TUN if kind == 'fireman' else I_TROU
        for s in (-0.26, 0.26): lathe(bm, [(0.2, 0.0), (0.2, 1.2), (0.23, 2.6), (0.0, 2.65)], 6, legm, cx=s)
        hem = {'police': 1.25, 'fireman': 2.3}.get(kind, rng.choice((1.6, 1.9, 2.4)))   # greatcoat / tunic / overcoat
        lathe(bm, [(0.0, hem), (0.7, hem), (0.62, 2.9), (0.6, 3.6), (0.7, 4.35), (0.42, 4.72), (0.0, 4.78)], 9, c)
        for s in (-0.7, 0.7): lathe(bm, [(0.17, 3.0), (0.18, 4.4), (0.0, 4.5)], 5, c, cx=s)
        lathe(bm, [(0.0, 4.72), (0.3, 4.82), (0.35, 5.12), (0.29, 5.4), (0.0, 5.48)], 8, I_SKIN)
        if kind == 'police':     # custodian helmet (tall dome + rose + small brim)
            lathe(bm, [(0.0, 5.2), (0.42, 5.2), (0.42, 5.26), (0.33, 5.3), (0.36, 5.75), (0.25, 6.15), (0.06, 6.25), (0.0, 6.3)], 9, I_NAVY)
            bbox(bm, -0.06, 0.06, -0.38, -0.3, 5.6, 5.75, I_BRASS)
        elif kind == 'fireman':  # LFB helmet with comb (black composite by 1936: brass mostly withdrawn, U) + belt
            lathe(bm, [(0.0, 5.18), (0.55, 5.18), (0.5, 5.25), (0.36, 5.3), (0.36, 5.6), (0.2, 5.8), (0.0, 5.85)], 9, I_HELM)
            bbox(bm, -0.05, 0.05, -0.38, 0.4, 5.6, 5.95, I_HELM)
            lathe(bm, [(0.0, 3.1), (0.64, 3.1), (0.63, 3.3), (0.0, 3.3)], 9, I_BRASS)
        elif rng.random() < 0.55:  # trilby / homburg
            lathe(bm, [(0.0, 5.25), (0.52, 5.25), (0.5, 5.32), (0.33, 5.36), (0.33, 5.7), (0.15, 5.74), (0.0, 5.7)], 8, rng.choice((I_HATD, I_HATB, I_HATD, I_GREY)))
        elif rng.random() < 0.8:   # flat cap
            lathe(bm, [(0.0, 5.25), (0.4, 5.25), (0.43, 5.42), (0.0, 5.5)], 8, rng.choice((I_GREY, I_BROWN, I_CHAR)))
            bbox(bm, -0.25, 0.25, -0.62, -0.3, 5.24, 5.3, I_GREY)
        h = 5.5
    vs = bm.verts[v0:] if hasattr(bm.verts, '__getitem__') else None
    bm.verts.ensure_lookup_table(); vs = [bm.verts[i] for i in range(v0, len(bm.verts))]
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector((ox, oy, 0)) * FTM) @ Matrix.Rotation(rot, 4, 'Z') @ Matrix.Scale(k, 4), verts=vs)

def mesh_from(name, build):
    bm = bmesh.new(); build(bm); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m_ in PM: me.materials.append(m_)
    return me

def place(name, me, col, x, y, z, rz=0.0):
    o = bpy.data.objects.new(name, me); col.objects.link(o); o.location = (f(x), f(y), f(z)); o.rotation_euler = (0, 0, rz); return o

# --- crowd blocks: 36 onlookers in a 28 x 20 ft patch, mostly facing -Y (toward whatever is in front) ---
def crowd_block_mesh(name, seed, n=36, w=28, d=20, mix=0.35, facing=0.0, spread=0.6):
    r = random.Random(seed)
    def b(bm):
        for i in range(n):
            person(bm, 'woman' if r.random() < mix else 'man', r, r.uniform(-w/2, w/2), r.uniform(-d/2, d/2), facing + r.uniform(-spread, spread))
    return mesh_from(name, b)

def line_mesh(name, kind, n, gap, facing, seed):
    r = random.Random(seed)
    def b(bm):
        for i in range(n): person(bm, kind, r, (i - (n-1)/2)*gap + r.uniform(-0.6, 0.6), r.uniform(-0.4, 0.4), facing + r.uniform(-0.15, 0.15))
    return mesh_from(name, b)

# --- appliances (local +X = forward, origin at ground centre of the wheelbase) ---
AM = [_m('lfb_red_1936', (0.42, 0.025, 0.02), 0.35), _m('lfb_black_chassis', (0.02, 0.02, 0.02), 0.6),
      _m('lfb_tyre', (0.015, 0.015, 0.015), 0.85), _m('lfb_brightwork', (0.75, 0.7, 0.6), 0.25, 1.0),
      _m('lfb_ladder_timber', (0.36, 0.22, 0.1), 0.6), _m('lfb_glass', (0.1, 0.12, 0.13), 0.05),
      _m('lfb_headlamp', (1.0, 0.95, 0.8), 0.3)]
A_RED, A_BLK, A_TYRE, A_BRIGHT, A_TIMB, A_GLASS, A_LAMP = range(7)
def wheel(bm, x, y, r=1.65, w=0.75, mi=A_TYRE, seg=14):
    rings = []
    for yy in (y - w/2, y + w/2):
        rings.append([bm.verts.new(Vector((x + r*math.cos(2*math.pi*k/seg), yy, r + r*math.sin(2*math.pi*k/seg))) * FTM) for k in range(seg)])
    A, B = rings
    for k in range(seg): bm.faces.new([A[k], A[(k+1) % seg], B[(k+1) % seg], B[k]]).material_index = mi
    bm.faces.new(list(reversed(A))).material_index = mi; bm.faces.new(B).material_index = mi
def ladder(bm, x0, x1, y0, z, w=1.6, mi=A_TIMB, rung=1.0):
    for s in (y0 - w/2, y0 + w/2): bbox(bm, x0, x1, s - 0.12, s + 0.12, z, z + 0.35, mi)
    x = x0 + 0.5
    while x < x1: bbox(bm, x - 0.06, x + 0.06, y0 - w/2, y0 + w/2, z + 0.1, z + 0.22, mi); x += rung
def pump_mesh(name):
    """1930s LFB pump/'pump escape' block-out: ~25 ft long, 7 ft wide, 7 ft to the ladder, open cab (I)."""
    def b(bm):
        bbox(bm, -11, 13, -2.6, 2.6, 1.2, 2.2, A_BLK)                       # chassis frame
        bbox(bm, 7.5, 12.6, -1.9, 1.9, 2.2, 5.0, A_RED)                     # bonnet
        bbox(bm, 12.6, 13.0, -1.6, 1.6, 2.4, 4.8, A_BRIGHT)                 # radiator
        for s in (-1.1, 1.1): bbox(bm, 12.9, 13.4, s - 0.35, s + 0.35, 4.1, 4.8, A_LAMP)
        bbox(bm, 7.3, 7.5, -3.2, 3.2, 4.0, 6.4, A_GLASS)                    # windscreen (open cab)
        bbox(bm, 3.5, 7.3, -3.4, 3.4, 2.2, 4.0, A_RED)                      # cab sides / seat box
        bbox(bm, 3.8, 6.6, -3.2, 3.2, 4.0, 4.8, A_BLK)                      # bench seat backs
        bbox(bm, -11, 3.5, -3.5, 3.5, 2.2, 5.6, A_RED)                      # body with lockers
        bbox(bm, -11.2, -9.2, -3.0, 3.0, 2.0, 5.2, A_BRIGHT)                # rear pump bay
        for s in (-1, 1): bbox(bm, -10, 11, s*3.5 - 0.1, s*3.5 + 0.1, 2.0, 2.3, A_BRIGHT)   # running boards
        for s in (-1, 1): bbox(bm, -8, 3, s*3.55 - 0.05, s*3.55 + 0.05, 4.3, 5.1, A_RED)
        ladder(bm, -12.5, 11.5, 0.0, 5.7, 1.8)                              # 35 ft extension ladder on top
        bbox(bm, -10.5, 1.5, -1.6, 1.6, 6.1, 6.6, A_TIMB)
        for xw in (9.2, -6.5):
            for s in (-1, 1): wheel(bm, xw, s*2.95)
        bbox(bm, -6.5, -6.0, -2.9, 2.9, 1.8, 2.0, A_BLK)
    return mesh_from_mats(name, b)
def ttl_base_mesh(name):
    """Leyland-Metz 100 ft turntable ladder chassis (~30 ft) with turntable at the rear (I)."""
    def b(bm):
        bbox(bm, -14, 15, -2.7, 2.7, 1.2, 2.3, A_BLK)
        bbox(bm, 9.5, 14.6, -1.9, 1.9, 2.3, 5.2, A_RED); bbox(bm, 14.6, 15.0, -1.6, 1.6, 2.5, 5.0, A_BRIGHT)
        for s in (-1.1, 1.1): bbox(bm, 14.9, 15.4, s - 0.35, s + 0.35, 4.3, 5.0, A_LAMP)
        bbox(bm, 5.5, 9.5, -3.4, 3.4, 2.3, 6.8, A_RED); bbox(bm, 9.3, 9.5, -3.2, 3.2, 4.8, 6.7, A_GLASS)
        bbox(bm, -14, 5.5, -3.5, 3.5, 2.3, 4.8, A_RED)
        for s in (-1, 1): bbox(bm, -13, 12, s*3.5 - 0.1, s*3.5 + 0.1, 2.0, 2.3, A_BRIGHT)
        for s in (-1, 1): bbox(bm, -12, -9, s*2.5, s*4.8, 0.0, 2.0, A_BLK)                # jacks
        tt = bm.verts.new
        lathe_ab(bm, -8.5, 0, 4.8, 5.6, 4.0, A_BLK)                           # turntable
        bbox(bm, -10.5, -6.5, -1.5, 1.5, 5.6, 8.0, A_RED)                    # ladder pivot housing
        for xw in (11.0, -4.0, -8.5):
            for s in (-1, 1): wheel(bm, xw, s*2.95)
    return mesh_from_mats(name, b)
def lathe_ab(bm, x, y, z0, z1, r, mi, seg=16):
    a = [bm.verts.new(Vector((x + r*math.cos(2*math.pi*k/seg), y + r*math.sin(2*math.pi*k/seg), z0)) * FTM) for k in range(seg)]
    b = [bm.verts.new(Vector((x + r*math.cos(2*math.pi*k/seg), y + r*math.sin(2*math.pi*k/seg), z1)) * FTM) for k in range(seg)]
    for k in range(seg): bm.faces.new([a[k], a[(k+1) % seg], b[(k+1) % seg], b[k]]).material_index = mi
    bm.faces.new(list(reversed(a))).material_index = mi; bm.faces.new(b).material_index = mi
def ttl_ladder_mesh(name, L=95.0):
    """4-section steel ladder extended to L ft along local +X from the pivot (I), truss sides + rungs."""
    def b(bm):
        secs = 4
        for i in range(secs):
            x0, x1 = i*L/secs - (1.5 if i else 0), (i+1)*L/secs; w = 2.4 - i*0.3; t = 0.35 - i*0.05
            for s in (-1, 1):
                bbox(bm, x0, x1, s*w/2 - 0.12, s*w/2 + 0.12, i*0.25, i*0.25 + 0.9, A_RED)
            x = x0 + 0.6
            while x < x1: bbox(bm, x - 0.05, x + 0.05, -w/2, w/2, i*0.25 + 0.4, i*0.25 + 0.5, A_BRIGHT); x += 1.0
        bbox(bm, L - 1.0, L + 0.6, -0.8, 0.8, 1.0, 1.4, A_BRIGHT)              # monitor / branch at the head
    return mesh_from_mats(name, b)
def mesh_from_mats(name, build):
    bm = bmesh.new(); build(bm); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m_ in AM: me.materials.append(m_)
    return me

# --- hoses and jets as bevelled curves ---
HOSE = _m('lfb_hose_canvas', (0.45, 0.4, 0.3), 0.85)
def jet_mat():
    m = bpy.data.materials.get('water_jet_spray')
    if m: return m
    m = bpy.data.materials.new('water_jet_spray'); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; n.clear()
    out = n.new('ShaderNodeOutputMaterial'); tr = n.new('ShaderNodeBsdfTransparent'); pb = n.new('ShaderNodeBsdfPrincipled')
    pb.inputs['Base Color'].default_value = (0.85, 0.88, 0.9, 1); pb.inputs['Roughness'].default_value = 0.3
    lw = n.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.35
    mx = n.new('ShaderNodeMixShader'); nt.links.new(lw.outputs['Facing'], mx.inputs[0])
    nt.links.new(pb.outputs[0], mx.inputs[1]); nt.links.new(tr.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    try: m.surface_render_method = 'BLENDED'
    except Exception: pass
    return m
def curves_obj(name, col, polylines, radius_ft, material):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = f(radius_ft); cu.bevel_resolution = 1
    cu.resolution_u = 6
    for pl in polylines:
        sp = cu.splines.new('POLY'); sp.points.add(len(pl) - 1)
        for p, q in zip(sp.points, pl): p.co = (f(q[0]), f(q[1]), f(q[2]), 1)
    cu.materials.append(material); o = bpy.data.objects.new(name, cu); col.objects.link(o); return o
def hose_path(a, b, z, rng, n=7, wig=4.0):
    pts = []
    for i in range(n + 1):
        t = i / n; w = math.sin(math.pi*t) * rng.uniform(-wig, wig)
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
        pts.append((a[0] + dx*t - dy/L*w, a[1] + dy*t + dx/L*w, (z(t) if callable(z) else z) + 0.12))
    return pts
def jet_arc(p, q, peak, n=14):
    return [(p[0] + (q[0]-p[0])*t, p[1] + (q[1]-p[1])*t, p[2] + (q[2]-p[2])*t + 4*peak*t*(1-t)) for t in [i/n for i in range(n + 1)]]

# =================== placement ===================
ZPAR = -0.5                     # Parade road surface (terrain box top, build.py)
FIRE_ = STATE == 'FIRE'; AFTER_ = STATE == 'AFTER'
if STATE == '1936':
    DC = coll('SY36_visitors__Nov1936')
    r = random.Random(36)
    def vb(bm):
        for i in range(70):
            x_ = r.uniform(-700, 700); y_ = r.uniform(yU + 6, -175)
            person(bm, 'woman' if r.random() < 0.45 else 'man', r, x_, y_, r.uniform(0, 2*math.pi))
    place('visitors_upper_terrace_1936', mesh_from('visitors_upper_terrace_1936', vb), DC, 0, 0, UT)
    def vb2(bm):
        for i in range(60):
            x_ = r.uniform(-900, 900); y_ = r.uniform(185, 300)
            person(bm, 'woman' if r.random() < 0.45 else 'man', r, x_, y_, r.uniform(0, 2*math.pi))
    place('visitors_parade_1936', mesh_from('visitors_parade_1936', vb2), DC, 0, 0, ZPAR)

if FIRE_ or AFTER_:
    DC = coll('SY36_fire_appliances_crowds__30Nov1936' if FIRE_ else 'SY36_fire_appliances_sightseers__1Dec1936')
    rr = random.Random(30111936)
    PUMP = pump_mesh('lfb_pump_1936'); TBASE = ttl_base_mesh('lfb_ttl_chassis_1936'); TLAD = ttl_ladder_mesh('lfb_ttl_ladder_100ft')
    hoses, jets = [], []
    def ttl(tag, x, y, z, heading, az, elev, L_target=None, jet_to=None):
        place('TL_' + tag, TBASE, DC, x, y, z, heading)
        px, py = x + math.cos(heading)*-8.5, y + math.sin(heading)*-8.5
        lad = place('TL_ladder_' + tag, TLAD, DC, px, py, z + 7.0)
        lad.rotation_euler = (0, -elev, az)
        if jet_to:
            L = 95.0; head = (px + math.cos(az)*math.cos(elev)*L, py + math.sin(az)*math.cos(elev)*L, z + 7.0 + math.sin(elev)*L + 1.2)
            jets.append(jet_arc(head, jet_to, 6))
        return (px, py)
    def pump(tag, x, y, z, heading):
        place('pump_' + tag, PUMP, DC, x, y, z, heading)
        return (x + math.cos(heading)*-11.5, y + math.sin(heading)*-11.5)
    n_pump = 0
    # ---- Parade side (+Y): pumps along the road, TLs at the transept front (I positions) ----
    # r17 AFTER: denser appliance line so CP058 reads outbreak/aftermath (was 2 pumps on empty olive plane)
    par_pumps = [(-620, 192, 0), (-470, 196, math.pi), (-330, 190, 0), (-200, 197, math.pi), (-120, 190, 0), (130, 192, math.pi),
                 (285, 197, 0), (360, 190, math.pi), (500, 196, 0), (650, 191, math.pi)] if FIRE_ else                 [(-360, 192, 0), (-280, 196, math.pi), (-200, 190, 0), (-120, 195, math.pi), (-40, 191, 0), (80, 196, math.pi), (180, 192, 0)]
    for i, (x_, y_, h_) in enumerate(par_pumps):
        rp = pump('parade_%02d' % i, x_, y_, ZPAR, h_); n_pump += 1
        for k in range(2 if FIRE_ else 1):     # lines of hose into the building / to the transept front
            tx = x_ + rr.uniform(-40, 40) if abs(x_) > 90 else rr.uniform(-60, 60)
            hoses.append(hose_path(rp, (tx, 160 if FIRE_ else 150), ZPAR, rr))
    if FIRE_:
        ttl('parade_S', -85, 185, ZPAR, 0.0, -math.pi/2 + 0.35, math.radians(68), jet_to=(-30, 40, 70))
        ttl('parade_N', 95, 186, ZPAR, math.pi, -math.pi/2 - 0.3, math.radians(66), jet_to=(35, 30, 60))
        for i in range(10):   # hydrant connections on the far kerb
            hoses.append(hose_path((rr.uniform(-650, 650), 214), (par_pumps[i][0] - 9, par_pumps[i][1] + 2), ZPAR, rr, 4, 1.5))
    # ---- garden side: upper terrace (UT) ----
    gt = [(-260, -205, 0.3), (-40, -230, math.pi + 0.2), (60, -215, -0.4), (240, -200, math.pi), (420, -212, 0.1)] if FIRE_ else \
         [(-60, -215, 0.3), (260, -205, math.pi)]
    for i, (x_, y_, h_) in enumerate(gt):
        rp = pump('terrace_%02d' % i, x_, y_, UT, h_); n_pump += 1
        for k in range(2):
            hoses.append(hose_path(rp, (x_ + rr.uniform(-50, 50), -158), UT, rr))
    if FIRE_:
        ttl('terrace_C', 20, -195, UT, math.pi/2 + 0.1, math.pi/2 - 0.1, math.radians(62), jet_to=(10, -100, 72))
        ttl('terrace_S', -140, -200, UT, math.pi/2, math.pi/2 + 0.25, math.radians(64), jet_to=(-60, -110, 66))
    else:
        ttl('terrace_C', 20, -195, UT, math.pi/2 + 0.1, math.pi/2 - 0.1, math.radians(30), jet_to=(15, -60, 4))
    curves_obj('hoses_canvas_2_75in', DC, hoses, 0.13, HOSE)
    # branch men at the facade with jets into the building (FIRE) / damping down (AFTER)
    br = []
    def fb(bm):
        for i in range(14 if FIRE_ else 8):
            side = 1 if i % 2 else -1
            x_ = rr.uniform(-400, 400); y_ = (186 if abs(x_) < 75 else 168) if side > 0 else -168
            z_ = ZPAR if side > 0 else UT
            for j in range(3):    # branch crew of three along the hose
                person(bm, 'fireman', rr, x_ + rr.uniform(-1, 1), y_ + side*(2 + j*2.5), (0 if side > 0 else math.pi) + rr.uniform(-0.3, 0.3))
            br.append((x_, y_, z_, side))
        for i in range(70 if FIRE_ else 20):     # crews at the appliances
            src = rr.choice(par_pumps + [(a, b_, c_) for a, b_, c_ in gt])
            person(bm, 'fireman', rr, src[0] + rr.uniform(-14, 14), src[1] + rr.choice((-5, 5)) + rr.uniform(-1, 1), rr.uniform(0, 2*math.pi))
    # firemen on the Parade and terrace have different ground levels: build two meshes
    def split_build(pred):
        def b(bm):
            r0 = rr.getstate(); fb(bm); rr.setstate(r0)
            bm.verts.ensure_lookup_table()
            kill = [v for v in bm.verts if not pred(v.co.y / FTM)]
            bmesh.ops.delete(bm, geom=kill, context='VERTS')
        return b
    place('lfb_firemen_parade', mesh_from('lfb_firemen_parade', split_build(lambda y: y > 0)), DC, 0, 0, ZPAR)
    place('lfb_firemen_terrace', mesh_from('lfb_firemen_terrace', split_build(lambda y: y <= 0)), DC, 0, 0, UT)
    for x_, y_, z_, side in br[:(14 if FIRE_ else 8)]:
        p = (x_, y_ + side*2.0, z_ + 4.0)
        q = (x_ + rr.uniform(-10, 10), y_ - side*rr.uniform(40, 70), (rr.uniform(25, 45) if FIRE_ else z_ + 1))
        jets.append(jet_arc(p, q, 8 if FIRE_ else 4))
    curves_obj('water_jets', DC, jets, 0.35, jet_mat())
    # ---- crowds + police lines ----
    blocks = [crowd_block_mesh('crowd36_block_%d' % k, 600 + k, mix=0.33) for k in range(4)]
    n_people = 0
    def crowd_band(tag, xa, xb, y0, y1, z, facing, density=1.0):
        global n_people
        x = xa
        while x < xb:
            y = y0
            while y < y1:
                if rr.random() < density:
                    place('crowd36_%s' % tag, rr.choice(blocks), DC, x + rr.uniform(-3, 3), y + rr.uniform(-2, 2), z, facing + rr.uniform(-0.25, 0.25))
                    n_people += 36
                y += 21
            x += 29
    # Parade: the crowd held back across the road (y > 222) facing the palace (-Y); police line at the kerb (I)
    if FIRE_:
        crowd_band('parade', -720, 720, 236, 300, ZPAR, 0.0, 0.85)
        PL = line_mesh('police_line_parade', 'police', 120, 11.0, 0.0, 77)
        place('police_line_parade', PL, DC, 0, 224, ZPAR)
        # garden side: onlookers on the lower terrace below the bank, police line along its foot (I)
        crowd_band('lower_terrace', -520, 520, yU - BANK - 52, yU - BANK - 10, LT, 0.0, 0.75)
        place('police_line_lower_terrace', line_mesh('police_line_lower_terrace', 'police', 70, 14.0, math.pi, 78), DC, 0, yU - BANK - 6, LT)
        # CP058/CP061 flank: a crowd on the south end of the upper terrace kept back by constables (I)
        crowd_band('upper_terrace_S', -560, -330, yU + 12, yU + 58, UT, math.pi/2 + 0.6, 0.8)
        place('police_line_upper_terrace', line_mesh('police_line_upper_terrace', 'police', 10, 9.0, -math.pi/2, 79), DC, -315, yU + 35, UT, math.pi/2)
    else:
        # AFTER TTL still damping down (I) + denser parade sightseers around appliances
        ttl('parade_after', -90, 188, ZPAR, 0.0, -math.pi/2 + 0.2, math.radians(28), jet_to=(-20, 80, 8))
        crowd_band('parade_after', -400, 200, 210, 250, ZPAR, math.pi, 0.7)
        crowd_band('lower_terrace_sightseers', -300, 300, yU - BANK - 40, yU - BANK - 10, LT, 0.0, 0.35)
        place('police_line_lower_terrace', line_mesh('police_line_lower_terrace_am', 'police', 24, 18.0, math.pi, 80), DC, 0, yU - BANK - 6, LT)
    print('DRESS36', STATE, 'pumps', n_pump, 'crowd', n_people, 'hoses', len(hoses), 'jets', len(jets))

# CP058 (appliances & firemen on the Parade) and CP060 (the crowd watching) - new storyboard cameras, positions I
# r17: stand among appliances looking along the pump line toward scorched nave + tower (was empty olive FG)
cam('CAM_CP058_parade_appliances_35mm', (-300, 215, ZPAR + EYE), (-80, 195, ZPAR + 5), 35)  # r17i along pump line (was lookat z=35 → empty sky)
cam('CAM_CP060_crowd_watching_35mm', (-420, 318, ZPAR + EYE + 1.0), (-40, 40, 70), 35)
