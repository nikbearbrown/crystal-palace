"""CP057 CANDIDATE (2026-11-18, no verdict): 'Trying to recover an audience' (1920s-1930s) - the lower terrace in front of the
garden front on a summer afternoon in 1936, the last summer before the fire: a modest interwar public strolling the terrace
walks and sitting in hired deck chairs on the lawns. Not a packed crowd: the narration says the palace 'remained a landmark,
without commanding the same place in public life'.

usage: blender -b rounds/sydenham-1936-r11.blend -P scripts/candidate_cp057_visitors.py [-- out.blend]   (env CP057_NOSAVE=1: no save)
Base = rounds/sydenham-1936-r11.blend (md5 40140697, unchanged since 1b3c92d) - the blend the live CP057 hero
  renders/r11_1936_CAM_CP057_1936_lower_terrace_35mm.png was rendered from (survey look v1.1, look/sydenham_logs/CP057.log:
  apply_render.py --scene-id CP057 --era 1852 --tod exterior_afternoon --spp 24 --res 1280x720 --no-people; re-render max diff 0).
  -> rounds/candidates/sydenham-1936-r11_cp057visitors.blend
Live hero shows: an empty lower terrace - flat lawns, a dry basin and empty walks in front of the whole garden front; nothing in
  the frame says 'exhibitions and entertainment returned' or that anyone still came.
Adds ONE dated collection SY36_lower_terrace_interwar_visitors__summer1936:
  * people_lib 1930s_man / 1930s_woman figures (role set PPL-20C) re-dressed per object for summer: women in mid-calf day
    frocks (muted rose, powder blue, sage, oatmeal, navy, lilac), men in grey/fawn/navy lounge suits; hats from the library
    (trilbies / cloche-type, never white). Walking couples and family groups on the basin walk, the lawn beyond the basin,
    the central flight and the upper terrace; nearest figure >= 22 m from the lens.
  * striped canvas deck chairs (folding, beech frame, ~0.6 m wide) in small clusters on the lawn beyond the basin, most
    occupied (seated people_lib pose), on the lawns left and right of the basin: two small clusters of empty
    chairs on the front lawns at 22-28 m (no figure nearer than 28 m), the rest 40-95 m from the lens.
Sources: storyboard CP057 (1920s-1930s, 'after the war, exhibitions and entertainment returned', PPL-20C); BUILD-PLAN PPL-20C
  (people of 1911-1940s); Historic England / Inside Croydon (fountains out of use long before 1936, basins dry - left dry, as
  in r11). Deck-chair hire in London parks between the wars R in general; at the Crystal Palace terraces I. Dress: 1930s summer
  day dress (mid-calf, natural waist), lounge suits + trilbies R in general; colours I. Numbers and placement I.
Cameras NOT moved, sun/world/exposure/look NOT changed. Nothing deleted or hidden; architecture untouched.
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP057_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-1936-r11_cp057visitors.blend')
STATE = 'SY36_lower_terrace_interwar_visitors__summer1936'
assert bpy.data.collections.get(STATE) is None, 'base already dressed'
n_before = len(bpy.data.objects)
hidden_before = sorted(o.name for o in bpy.data.objects if o.hide_render)
sc = bpy.context.scene
col = bpy.data.collections.new(STATE); sc.collection.children.link(col)
CAM = bpy.data.objects['CAM_CP057_1936_lower_terrace_35mm']
C = CAM.location.copy()
FWD = (CAM.matrix_world.to_3x3() @ Vector((0, 0, -1))).to_2d().normalized()
RNG = random.Random(1936057)
INFO = {}

# ------------------------------------------------------------------ ground probe (base scene only, render-visible objects)
_vis = {}
for o in bpy.data.objects:
    _vis[o.name] = o.hide_viewport; o.hide_viewport = o.hide_render
dg = bpy.context.evaluated_depsgraph_get()
OK_GROUND = ('terrain', 'park_paths_gravel', 'terrace_gravel')
def ground(x, y):
    hit, loc, nor, idx, ob, _ = sc.ray_cast(dg, Vector((x, y, 60.0)), Vector((0, 0, -1)))
    if not hit: return None
    return (loc.z, ob.name, nor.z)
def polar(d, deg):   # deg > 0 = left of the optical axis
    a = math.radians(deg); f = FWD
    v = Vector((f.x * math.cos(a) - f.y * math.sin(a), f.x * math.sin(a) + f.y * math.cos(a)))
    return C.x + d * v.x, C.y + d * v.y
def seen(x, y, z, h=1.6):   # head visible from the lens (base scene)
    tgt = Vector((x, y, z + h)); d = tgt - C; L = d.length
    hit, loc, *_ = sc.ray_cast(dg, C, d.normalized(), distance=L - 0.3)
    return not hit
# ------------------------------------------------------------------ materials
def pmat(name, rgb, rough=0.75):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name); m.use_nodes = True
        b = m.node_tree.nodes.get('Principled BSDF'); b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough
        m['cp_state'] = STATE
    return m
# albedos kept mid-dark: the frame is high-key (live luma ~181), pale cloth blows out to pink/white at this exposure
FROCKS = [(0.20, 0.09, 0.10), (0.09, 0.13, 0.22), (0.12, 0.16, 0.10), (0.22, 0.18, 0.12), (0.03, 0.04, 0.08),
          (0.14, 0.10, 0.18), (0.20, 0.11, 0.06), (0.09, 0.09, 0.10)]
SUITS = [(0.07, 0.07, 0.075), (0.11, 0.11, 0.115), (0.03, 0.035, 0.06), (0.10, 0.095, 0.09), (0.15, 0.15, 0.15), (0.07, 0.055, 0.045)]   # charcoal, grey, navy, mid grey, grey flannel, dark brown (no fawn/khaki: reads military)
def stripe_mat(name, ca, cb):
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    b = N.get('Principled BSDF'); b.inputs['Roughness'].default_value = 0.9
    tc = N.new('ShaderNodeTexCoord'); sep = N.new('ShaderNodeSeparateXYZ'); mul = N.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
    mul.inputs[1].default_value = 7.5 / 2.0         # 7-8 stripes across the 0.6 m sling (generated coords 0..1 over width)
    fr = N.new('ShaderNodeMath'); fr.operation = 'FRACT'; gt = N.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.5
    mix = N.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs[6].default_value = (*ca, 1); mix.inputs[7].default_value = (*cb, 1)
    L.new(tc.outputs['UV'], sep.inputs[0]); L.new(sep.outputs['X'], mul.inputs[0]); L.new(mul.outputs[0], fr.inputs[0])
    L.new(fr.outputs[0], gt.inputs[0]); L.new(gt.outputs[0], mix.inputs[0]); L.new(mix.outputs[2], b.inputs['Base Color'])
    m['cp_state'] = STATE; return m
CANVAS = [stripe_mat('cp057_deckchair_canvas_green', (0.20, 0.32, 0.20), (0.62, 0.58, 0.48)),
          stripe_mat('cp057_deckchair_canvas_red', (0.45, 0.14, 0.12), (0.62, 0.58, 0.48)),
          stripe_mat('cp057_deckchair_canvas_blue', (0.16, 0.22, 0.38), (0.62, 0.58, 0.48)),
          stripe_mat('cp057_deckchair_canvas_orange', (0.52, 0.30, 0.12), (0.60, 0.56, 0.46))]
BEECH = pmat('cp057_deckchair_beech', (0.42, 0.30, 0.18), 0.6)

# ------------------------------------------------------------------ deck chair (classic folding pattern, metres)
W, RAIL = 0.60, 0.028
def box(bm, p0, p1, w):   # square rail from p0 to p1
    p0, p1 = Vector(p0), Vector(p1); ax = (p1 - p0); L = ax.length; ax.normalize()
    up = Vector((0, 0, 1)) if abs(ax.z) < 0.95 else Vector((0, 1, 0))
    s1 = ax.cross(up).normalized() * w / 2; s2 = ax.cross(s1).normalized() * w / 2
    vs = [bm.verts.new(p + a + b) for p in (p0, p1) for a, b in ((s1, s2), (-s1, s2), (-s1, -s2), (s1, -s2))]
    for f in ((0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)): bm.faces.new([vs[i] for i in f])
def deckchair_mesh(name):
    bm = bmesh.new()
    for sx in (-W / 2, W / 2):
        box(bm, (sx, 0.55, 0.0), (sx, -0.30, 0.95), RAIL)       # back rails (feet behind, top forward-up)  local -Y = front
        box(bm, (sx, -0.45, 0.0), (sx, 0.05, 0.42), RAIL)       # front legs / seat frame
        box(bm, (sx, -0.55, 0.38), (sx, 0.25, 0.38), RAIL)      # seat rails (arm level)
    box(bm, (-W / 2, -0.30, 0.95), (W / 2, -0.30, 0.95), RAIL)  # top bar
    box(bm, (-W / 2, -0.55, 0.38), (W / 2, -0.55, 0.38), RAIL)  # front bar
    box(bm, (-W / 2, 0.40, 0.12), (W / 2, 0.40, 0.12), RAIL)    # back stretcher
    me_w = bpy.data.meshes.new(name + '_frame'); bm.to_mesh(me_w); bm.free()
    # canvas sling: from top bar sagging down to the front bar
    bm = bmesh.new(); uv = bm.loops.layers.uv.new('UV')
    P0, P1 = Vector((0, -0.30, 0.93)), Vector((0, -0.55, 0.36)); n = 10; rows = []
    for k in range(n + 1):
        t = k / n; p = P0.lerp(P1, t); p.z -= 0.16 * math.sin(math.pi * t); p.y += 0.10 * math.sin(math.pi * t)
        rows.append([bm.verts.new((sx * (W / 2 - 0.02), p.y, p.z)) for sx in (-1, 1)])
    for k in range(n):
        f = bm.faces.new((rows[k][0], rows[k][1], rows[k + 1][1], rows[k + 1][0]))
        for l in f.loops: l[uv].uv = (0.0 if l.vert.co.x < 0 else 1.0, 0.0)
    me_c = bpy.data.meshes.new(name + '_canvas'); bm.to_mesh(me_c); bm.free()
    me_w.materials.append(BEECH); me_c.materials.append(CANVAS[0])
    return me_w, me_c
ME_FRAME, ME_CANVAS = deckchair_mesh('cp057_deckchair')
def deckchair(i, x, y, z, yaw):
    canvas = CANVAS[RNG.randrange(len(CANVAS))]
    fo = bpy.data.objects.new(f'cp057_deckchair_{i:02d}_frame', ME_FRAME); co = bpy.data.objects.new(f'cp057_deckchair_{i:02d}_canvas', ME_CANVAS)
    for o in (fo, co):
        col.objects.link(o); o.location = (x, y, z); o.rotation_euler = (0, 0, yaw); o['cp_state'] = STATE
    co.material_slots[0].link = 'OBJECT'; co.material_slots[0].material = canvas
    return fo

# ------------------------------------------------------------------ people
from cpl_people import person_mesh
people = []
def redress(o, role, k):
    for s in o.material_slots:
        m = s.material
        if m is None: continue
        if m.name.startswith('CPL3_coat1930') or m.name.startswith('CPL3_bodice1930'):
            s.link = 'OBJECT'
            if role == '1930s_woman':
                c = FROCKS[(k + (0 if 'coat' in m.name else 3)) % len(FROCKS)]
                s.material = pmat(f'cp057_frock_{FROCKS.index(c)}', c, 0.8)
            else:
                c = SUITS[k % len(SUITS)]; s.material = pmat(f'cp057_suit_{SUITS.index(c)}', c, 0.72)
def skirt(o, k):
    """A-line mid-calf day-dress skirt over the library's leg-following 'skirt' shell (which reads as trousers): an
    elliptical frustum from just below the waist to mid-calf, in the figure's frock colour, parented to the figure."""
    h = o.dimensions.z; z0, z1 = 0.19 * h, 0.555 * h; seg = 18
    bm = bmesh.new(); ring = []
    for (z, rx, ry) in ((z1, 0.165, 0.125), (0.5 * (z0 + z1), 0.20, 0.165), (z0, 0.235, 0.205)):
        ring.append([bm.verts.new((rx * math.cos(2 * math.pi * i / seg), ry * math.sin(2 * math.pi * i / seg), z)) for i in range(seg)])
    for a, b in ((0, 1), (1, 2)):
        for i in range(seg):
            j = (i + 1) % seg; bm.faces.new((ring[a][i], ring[a][j], ring[b][j], ring[b][i]))
    bm.faces.new(list(reversed(ring[0]))); bm.faces.new(ring[2])
    me = bpy.data.meshes.new(o.name + '_skirt'); bm.to_mesh(me); bm.free()
    c = FROCKS[k % len(FROCKS)]; me.materials.append(pmat(f'cp057_frock_{FROCKS.index(c)}', c, 0.8))
    for f in me.polygons: f.use_smooth = True
    so = bpy.data.objects.new(o.name + '_skirt', me); col.objects.link(so); so.parent = o; so['cp_state'] = STATE
    return so
def put(name, role, pose, x, y, z, yaw, seed, lod):
    person_mesh(name, role, style={'role': role, 'pose': pose, 'lod': lod, 'era': '1930s'}, seed=seed)
    o = bpy.data.objects[name]
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o.location = (x, y, z + 0.012); o.rotation_euler = (0, 0, yaw)
    o['cpl_people'] = 'cpl_people_v3'; o['cp_state'] = STATE
    redress(o, role, seed); people.append(o)
    if role == '1930s_woman' and pose != 'seated':
        bpy.context.view_layer.update(); skirt(o, seed)
    return o
def yaw_to(dx, dy): return math.atan2(dx, -dy)       # base meshes face local -Y
def lod_for(d): return 'hero' if d < 30 else ('mid' if d < 70 else 'crowd')

placed = []
def free(x, y, r=0.5): return all((x - a) ** 2 + (y - b) ** 2 > r * r for a, b in placed)
nearest = 1e9; skipped = {'ground': 0, 'hidden': 0, 'near': 0, 'crowded': 0}
def try_person(n, role, pose, x, y, yaw, dmin=28.0):
    global nearest
    d = math.hypot(x - C.x, y - C.y)
    if d < dmin: skipped['near'] += 1; return None
    g = ground(x, y)
    okg = g is not None and (g[1] in OK_GROUND or (g[1] == 'terraces_stone' and -25 < x < 20 and -116 < y < -100))
    if not okg or g[2] < 0.9: skipped['ground'] += 1; return None
    if not free(x, y): skipped['crowded'] += 1; return None
    if not seen(x, y, g[0]): skipped['hidden'] += 1; return None
    placed.append((x, y)); nearest = min(nearest, d)
    return put(f'cp057_visitor_{n:03d}', role, pose, x, y, g[0], yaw + RNG.uniform(-0.25, 0.25), 1936570 + n * 23, lod_for(d))

# ------------------------------------------------------------------ where the lens actually sees open ground
# cast a grid of rays through the frame; keep ground hits on lawn / walks (flat enough to stand on). Placing on these points
# guarantees the new figures stand on visible ground (the basin parapet hides most of the lower lawn behind it).
mw = CAM.matrix_world; fr = CAM.data.view_frame(scene=sc)
xs = [v.x for v in fr]; ys = [v.y for v in fr]; zf = fr[0].z
VIS = []
for j in range(0, 160):
    for i in range(0, 284):
        u = (i + 0.5) / 284; v = 0.55 + 0.45 * (j + 0.5) / 160
        p = Vector((min(xs) + u * (max(xs) - min(xs)), max(ys) - v * (max(ys) - min(ys)), zf))
        dvec = (mw.to_3x3() @ p).normalized()
        hit, loc, nor, idx, ob, _ = sc.ray_cast(dg, C, dvec)
        if hit and ob.name in OK_GROUND and nor.z > 0.9 and 0.03 < u < 0.97:
            VIS.append((loc.x, loc.y, loc.z, (loc - C).to_2d().length, u, v))
INFO['visible_ground_samples'] = len(VIS)
def pick(dlo, dhi, ulo=0.0, uhi=1.0):
    pool = [q for q in VIS if dlo <= q[3] < dhi and ulo <= q[4] <= uhi]
    return RNG.choice(pool) if pool else None

n = 0
def couple(q, dirx, diry, pose='walking', third=None, women_pose=None):
    global n
    x, y = q[0], q[1]; yaw = yaw_to(dirx, diry); px, py = -diry * 0.62, dirx * 0.62
    try_person(n, '1930s_woman', women_pose or pose, x, y, yaw); n += 1
    try_person(n, '1930s_man', pose, x + px, y + py, yaw); n += 1
    if third: try_person(n, third, women_pose or pose if third == '1930s_woman' else pose, x - px, y - py, yaw); n += 1
DIRS = ((1, 0.25), (-1, 0.2), (0.25, 1), (-0.3, -1), (0.8, 0.6), (-0.7, 0.7))
# A. the basin walk in front of the basin and the lawn either side (28-42 m), spread across the frame: a few groups,
#    women mostly standing (the library's walking pose splits the legs; the added skirt covers it)
for k, (ulo, uhi) in enumerate(((0.05, 0.25), (0.25, 0.45), (0.45, 0.62), (0.62, 0.8), (0.8, 0.97))):
    q = pick(28, 42, ulo, uhi)
    if q: couple(q, *RNG.choice(DIRS), pose=RNG.choice(('walking', 'standing')), women_pose=RNG.choice(('standing', 'walking')), third='1930s_woman' if k == 2 else None)
# B. the lawns left and right of the basin (40-95 m): deck-chair clusters, mostly occupied, plus strolling couples
chairs = 0
SIDES = ((0.0, 0.2), (0.72, 1.0))
# two near clusters of EMPTY hired chairs on the front lawns either side of the basin walk (22-28 m: gives the empty
# foreground lawn a period detail with no figure in the near foreground - library figures read doll-like that close),
# then eight occupied clusters on the far lawns
NEAR_CL = [pick(22, 28, 0.03, 0.22), pick(22, 28, 0.78, 0.97)]
for k in range(10):
    q = NEAR_CL[k] if k < 2 else pick(40, 95, *SIDES[k % 2])
    if q is None: continue
    cx, cy, cz = q[0], q[1], q[2]
    if not free(cx, cy, 3.0): continue
    face = Vector((C.x - cx, C.y - cy)).normalized()
    base_yaw = yaw_to(face.x, face.y) + RNG.uniform(-0.6, 0.6)
    kk = RNG.choice((2, 2, 3))
    for j in range(kk):
        off = (j - (kk - 1) / 2) * 0.95
        x = cx + math.cos(base_yaw) * off; y = cy + math.sin(base_yaw) * off
        g = ground(x, y)
        if g is None or g[1] not in OK_GROUND or g[2] < 0.9: continue
        yaw = base_yaw + RNG.uniform(-0.25, 0.25)
        deckchair(chairs, x, y, g[0], yaw); chairs += 1
        if k >= 2 and RNG.random() < 0.8:   # far clusters occupied (near clusters left empty: hired chairs waiting): seated figure, hips at the sling's low point, feet forward (local -Y)
            sx, sy = x + math.sin(yaw) * 0.33, y - math.cos(yaw) * 0.33
            role = '1930s_woman' if RNG.random() < 0.55 else '1930s_man'
            put(f'cp057_visitor_{n:03d}', role, 'seated', sx, sy, g[0] - 0.02, yaw, 1936570 + n * 23, lod_for(math.hypot(sx - C.x, sy - C.y)))
            n += 1
        placed.append((x, y))
    if k >= 2 and RNG.random() < 0.5:
        try_person(n, RNG.choice(('1930s_man', '1930s_woman')), 'standing', cx + RNG.uniform(-1.6, 1.6), cy + RNG.uniform(1.0, 1.8), base_yaw); n += 1
INFO['deckchairs'] = chairs
for k in range(8):
    q = pick(40, 95, *SIDES[k % 2])
    if q: couple(q, *RNG.choice(DIRS), women_pose='standing' if q[3] < 45 else None, third=RNG.choice((None, None, '1930s_man', '1930s_woman')))
# C. the grass bank below the upper-terrace wall (the green band above the basin, ~80-110 m): visitors sitting on the slope
#    facing down it (seated pose, legs down the slope; hips lifted 0.15 m so they sit on, not in, the 30-degree turf),
#    a few standing. Sitting out on the terrace slopes R in general for Crystal Palace crowds; here I.
BANK = []
for j in range(70):
    for i in range(280):
        u = 0.03 + 0.94 * (i + 0.5) / 280; v = 0.70 + 0.16 * (j + 0.5) / 70
        p = Vector((min(xs) + u * (max(xs) - min(xs)), max(ys) - v * (max(ys) - min(ys)), zf))
        hit, loc, nor, idx, ob, _ = sc.ray_cast(dg, C, (mw.to_3x3() @ p).normalized())
        if hit and ob.name == 'terrain' and 0.6 < nor.z <= 0.9 and -118 < loc.y < -100:
            BANK.append((loc.x, loc.y, loc.z, nor.x, nor.y, u))
INFO['bank_samples'] = len(BANK); bank_n = 0
for k in range(60):
    if not BANK or bank_n >= 26: break
    b8 = k % 8; pool = [q for q in BANK if b8 / 8 <= (q[5] - 0.03) / 0.94 < (b8 + 1) / 8] or BANK   # spread across the width
    x, y, z, nx, ny, _u = RNG.choice(pool)
    if not free(x, y, 1.2): continue
    d = math.hypot(x - C.x, y - C.y)
    if RNG.random() < 0.75:
        yaw = yaw_to(nx, ny) + RNG.uniform(-0.4, 0.4)
        put(f'cp057_visitor_{n:03d}', RNG.choice(('1930s_woman', '1930s_man')), 'seated', x, y, z + 0.15, yaw, 1936570 + n * 23, lod_for(d))
    else:
        put(f'cp057_visitor_{n:03d}', RNG.choice(('1930s_woman', '1930s_man')), 'standing', x, y, z - 0.05, yaw_to(*RNG.choice(DIRS)), 1936570 + n * 23, lod_for(d))
    placed.append((x, y)); n += 1; bank_n += 1
INFO['bank_figures'] = bank_n
# D. far lawn / bank foot / terrace walks (95-170 m): small figures
for k in range(40):
    q = pick(95, 170)
    if q: try_person(n, RNG.choice(('1930s_man', '1930s_woman', '1930s_woman')), RNG.choice(('walking', 'walking', 'standing')), q[0], q[1], yaw_to(*RNG.choice(DIRS))); n += 1

for o in bpy.data.objects:
    if o.name in _vis: o.hide_viewport = _vis[o.name]
col['cp_state'] = STATE
col['evidence'] = ('storyboard CP057 1920s-1930s, exhibitions and entertainment returned (R); PPL-20C 1930s dress (R in general, colours I); '
                   'deck-chair hire in interwar London parks (R in general; at Sydenham I); basins dry 1936 (Historic England via Inside Croydon, as r11); '
                   'numbers, groups and placement I')
INFO['visitors'] = len(people); INFO['nearest_figure_m'] = round(nearest, 2); INFO['skipped'] = dict(skipped)
INFO['objects'] = len(col.objects); INFO['new_objects_total'] = len(bpy.data.objects) - n_before
assert sorted(o.name for o in bpy.data.objects if o.hide_render) == hidden_before
assert len(bpy.data.objects) - n_before == len(col.objects), 'every new object must be in the one dated collection'
print('CP057 BUILT', INFO)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP057 SAVED', OUT)
