"""G-DINO: Benjamin Waterhouse Hawkins' Crystal Palace Park geological illustration, as unveiled 1854 (Victorian, wrong).
usage: blender -b -P scripts/build.py -- <out.blend>
Collections (dated): DN54_lake_islands__1854 (terrain, water, rocks, planting), DN54_secondary_island_sculptures__1854,
DN54_tertiary_island_mammals__1854, DN54_geological_strata__1854, DN53_hawkins_studio__1853 (CP034 workshop, ILN print),
DN53_iguanodon_dinner__31Dec1853 (CP034b). Units: feet in code, metres in the file. +X east, +Y north; viewers on the S bank."""
import bpy, bmesh, math, random, sys, os
from mathutils import Vector, Matrix
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hawkins as HK
from mb import FT, mb_mesh, append_mesh
OUT = sys.argv[sys.argv.index('--') + 1]
F = FT
def f(v): return v * F
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
sc = bpy.context.scene
root = bpy.data.collections.new('DN-1854_crystal_palace_park_geological_illustration'); sc.collection.children.link(root)
def coll(name, parent=root):
    c = bpy.data.collections.new(name); parent.children.link(c); return c
C = {k: coll(k) for k in ['DN54_lake_islands__1854', 'DN54_secondary_island_sculptures__1854', 'DN54_tertiary_island_mammals__1854',
                          'DN54_geological_strata__1854', 'DN53_hawkins_studio__1853', 'DN53_iguanodon_dinner__31Dec1853', 'CAMERAS']}

# ---------------- materials ----------------
def mat(name, base, rough=0.6, metal=0.0, bump=None, var=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*base, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if var:   # colour variation (noise between base and var)
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = var[1]
        cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (*base, 1); cr.color_ramp.elements[1].color = (*var[0], 1)
        nt.links.new(nz.outputs[0], cr.inputs[0]); nt.links.new(cr.outputs[0], b.inputs['Base Color'])
    if bump:  # (kind, scale, strength)
        tx = nt.nodes.new('ShaderNodeTexVoronoi' if bump[0] == 'scales' else 'ShaderNodeTexNoise'); tx.inputs['Scale'].default_value = bump[1]
        bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump[2]
        nt.links.new(tx.outputs[0], bp.inputs['Height']); nt.links.new(bp.outputs[0], b.inputs['Normal'])
    return m
# Hawkins painted the statues (brick/iron cores, cement render); 1854 colours are not recorded well -> greens/greys/browns
# after contemporary coloured prints and the 2002 restoration palette (U).
M = dict(
    ig=mat('paint_iguanodon_green_grey', (0.16, 0.19, 0.12), 0.65, bump=('scales', 18, 0.35), var=((0.22, 0.22, 0.15), 3)),
    meg=mat('paint_megalosaurus_brown', (0.2, 0.13, 0.08), 0.65, bump=('scales', 18, 0.35), var=((0.26, 0.19, 0.12), 3)),
    hyl=mat('paint_hylaeosaurus_olive', (0.18, 0.17, 0.1), 0.65, bump=('scales', 20, 0.35), var=((0.25, 0.22, 0.14), 3)),
    ich=mat('paint_ichthyosaur_slate', (0.17, 0.18, 0.17), 0.5, bump=('noise', 30, 0.15), var=((0.24, 0.24, 0.2), 2)),
    ple=mat('paint_plesiosaur_dun', (0.21, 0.18, 0.13), 0.55, bump=('noise', 30, 0.15), var=((0.27, 0.24, 0.18), 2)),
    mgt=mat('paint_megatherium_brown_fur', (0.16, 0.11, 0.07), 0.8, bump=('noise', 60, 0.4), var=((0.22, 0.16, 0.1), 4)),
    elk=mat('paint_irish_elk_fawn', (0.3, 0.2, 0.11), 0.7, bump=('noise', 50, 0.2), var=((0.36, 0.26, 0.16), 4)),
    clay=mat('modelling_clay_wet_grey', (0.33, 0.31, 0.28), 0.85, bump=('noise', 25, 0.25)),
    plaster=mat('plaster_mould_white', (0.72, 0.7, 0.65), 0.9, bump=('noise', 12, 0.15)),
    grass=mat('grass_1854_young_turf', (0.07, 0.13, 0.035), 0.9, bump=('noise', 80, 0.3), var=((0.12, 0.15, 0.05), 0.08)),
    gravel=mat('path_hoggin_gravel', (0.42, 0.36, 0.27), 0.95, bump=('noise', 60, 0.3)),
    mud=mat('lake_bank_mud', (0.09, 0.075, 0.05), 0.7),
    rock=mat('sandstone_rocks', (0.32, 0.27, 0.2), 0.9, bump=('noise', 6, 0.6), var=((0.24, 0.2, 0.16), 1.5)),
    bark=mat('bark', (0.08, 0.06, 0.045), 0.9, bump=('noise', 40, 0.5)),
    leaf=mat('foliage', (0.025, 0.05, 0.015), 0.8, bump=('noise', 4, 0.8), var=((0.05, 0.08, 0.02), 1.2)),
    timber=mat('deal_boards_weathered', (0.36, 0.27, 0.17), 0.8, bump=('noise', 3, 0.2), var=((0.28, 0.2, 0.12), 0.6)),
    iron=mat('wrought_iron_fence', (0.03, 0.03, 0.03), 0.5, 0.6),
    cloth_r=mat('marquee_stripe_red', (0.35, 0.04, 0.03), 0.8), cloth_w=mat('marquee_stripe_cream', (0.7, 0.62, 0.48), 0.8),
    linen=mat('table_linen', (0.85, 0.83, 0.78), 0.7), coat=mat('frock_coat_black', (0.02, 0.02, 0.022), 0.6),
    skin=mat('skin', (0.55, 0.38, 0.28), 0.5), shirt=mat('shirt_white', (0.8, 0.78, 0.72), 0.7), smock=mat('workman_smock', (0.45, 0.42, 0.34), 0.85),
    brass=mat('brass_chandelier', (0.6, 0.45, 0.2), 0.3, 1.0),
    strata=[mat('strata_' + n, c, 0.9, bump=('noise', 4, 0.5)) for n, c in [('chalk', (0.7, 0.68, 0.6)), ('greensand', (0.23, 0.26, 0.15)), ('wealden_clay', (0.35, 0.25, 0.16)),
            ('oolite', (0.6, 0.48, 0.28)), ('lias', (0.25, 0.25, 0.24)), ('new_red_sandstone', (0.42, 0.16, 0.09)), ('coal_measures', (0.05, 0.05, 0.05)), ('mountain_limestone', (0.5, 0.5, 0.47))]])
def water_mat():
    m = bpy.data.materials.new('lake_water_still'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.015, 0.025, 0.02, 1); b.inputs['Roughness'].default_value = 0.12; b.inputs['IOR'].default_value = 1.33
    nt = m.node_tree; nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3.0
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.12; nt.links.new(nz.outputs[0], bp.inputs['Height']); nt.links.new(bp.outputs[0], b.inputs['Normal'])
    return m

def obj(name, me, col, loc=(0, 0, 0), rz=0.0, mats=()):
    for m in mats: me.materials.append(m)
    o = bpy.data.objects.new(name, me); col.objects.link(o); o.location = [f(v) for v in loc]; o.rotation_euler = (0, 0, rz); return o
def bm_obj(name, col, fn, mats):
    bm = bmesh.new(); fn(bm); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); return obj(name, me, col, mats=mats)
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

# ---------------- terrain: lake + Secondary / Tertiary islands (layout I after the 1854 park plan & modern survey) ----------------
WL = 0.0   # water level
LB = 118.0   # lake half-width N-S (I)
def lake_d(x, y): return ((x - 60) / 440) ** 2 + ((y + 5) / LB) ** 2
ISL = [(-15, 12, 190, 82, 'secondary'), (318, 40, 100, 66, 'tertiary')]
def isl_d(x, y): return min(((x - cx) / a) ** 2 + ((y - cy) / b) ** 2 for cx, cy, a, b, _ in ISL)
def ground(x, y):
    d = lake_d(x, y); h = 3.0 if d > 1.12 else (-4.0 if d < 0.9 else -4.0 + 7.0 * (d - 0.9) / 0.22)
    di = isl_d(x, y)
    if di < 1.12:
        hi = 2.2 + 3.2 * max(0.0, 1 - di) ** 1.5 if di < 0.88 else -4.0 + 6.2 * (1.12 - di) / 0.24
        h = max(h, hi)
    if d > 1.12: h += 0.012 * max(0, y - 140) + 1.5 * math.sin(x / 120) * min(1, max(0, (abs(y) - 160) / 60))   # rising parkland
    return h
def terrain(bm):
    X0, X1, Y0, Y1, S = -480, 600, -260, 260, 4.0
    nx, ny = int((X1 - X0) / S) + 1, int((Y1 - Y0) / S) + 1
    vs = [[bm.verts.new((f(X0 + i*S), f(Y0 + j*S), f(ground(X0 + i*S, Y0 + j*S)))) for j in range(ny)] for i in range(nx)]
    for i in range(nx - 1):
        for j in range(ny - 1):
            fc = bm.faces.new((vs[i][j], vs[i+1][j], vs[i+1][j+1], vs[i][j+1])); fc.smooth = True
            x, y = X0 + (i + .5)*S, Y0 + (j + .5)*S; z = ground(x, y)
            on_path = abs(lake_d(x, y) - 1.32) < 0.06 and y < 0                       # S bank walk
            fc.material_index = 2 if z < 1.2 else (1 if on_path else 0)
TER = bm_obj('terrain_lake_islands_1854', C['DN54_lake_islands__1854'], terrain, [M['grass'], M['gravel'], M['mud']])
def water(bm):
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector((f(60), f(-5), f(WL)))) @ Matrix.Diagonal(Vector((f(460), f(160), 1, 1))), verts=bm.verts)
bm_obj('lake_water', C['DN54_lake_islands__1854'], water, [water_mat()])
rng = random.Random(1854)
def rocks(bm, pts):
    for x, y, r in pts:
        res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=f(r))
        for v in res['verts']: v.co *= rng.uniform(0.75, 1.2)
        bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector((f(x), f(y), f(ground(x, y) - r * 0.3)))) @ Matrix.Diagonal(Vector((1, rng.uniform(0.7, 1.1), 0.6, 1))), verts=res['verts'])
# fence along the S bank walk (iron hurdle, I) and young 1854 planting
def fence(bm):
    xs = list(range(-330, 450, 8)); prev = None
    for x in xs:
        # path centre where lake_d == 1.32 on the S side; fence on its lake edge (1.24)
        y = -5 - LB * math.sqrt(max(0, 1.24 - ((x - 60) / 440) ** 2)); z = ground(x, y)
        strut(bm, (x, y, z), (x, y, z + 3.4), 0.06, 0, 4)
        if prev:
            for hz in (1.2, 2.3, 3.3): strut(bm, (prev[0], prev[1], prev[2] + hz), (x, y, z + hz), 0.03, 0, 4)
        prev = (x, y, z)
bm_obj('iron_hurdle_fence_south_walk', C['DN54_lake_islands__1854'], fence, [M['iron']])
def tree(bm, x, y, h, kind, rr):
    z = ground(x, y)
    strut(bm, (x, y, z - 1), (x + rr.uniform(-1, 1), y + rr.uniform(-1, 1), z + h * 0.55), max(0.25, h * 0.022), 0, 7)
    crowns = 1 if kind == 'young' else 4
    for k in range(crowns):
        cr = h * (0.28 if kind == 'young' else 0.24) * rr.uniform(0.8, 1.15)
        res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=f(cr))
        for v in res['verts']: v.co *= rr.uniform(0.85, 1.1)
        cx, cy = x + rr.uniform(-0.25, 0.25) * h * (k > 0), y + rr.uniform(-0.25, 0.25) * h * (k > 0)
        bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector((f(cx), f(cy), f(z + h * 0.62 + rr.uniform(-0.1, 0.12) * h)))) @ Matrix.Diagonal(Vector((1, 1, 0.85, 1))), verts=res['verts'])
        for fc in {fc for v in res['verts'] for fc in v.link_faces}: fc.material_index = 1; fc.smooth = True
def planting(bm):
    rr = random.Random(7)
    for i in range(42):    # mature parkland (Penge Place estate trees) beyond the lake, N side
        x, y = rr.uniform(-470, 590), rr.uniform(150, 255)
        if lake_d(x, y) > 1.25: tree(bm, x, y, rr.uniform(40, 75), 'mature', rr)
    for i in range(22):    # S side behind the viewers
        x, y = rr.uniform(-470, 590), rr.uniform(-258, -215)
        if lake_d(x, y) > 1.5: tree(bm, x, y, rr.uniform(40, 60), 'mature', rr)
    for cx, cy, a, b, nm in ISL:    # young 1854 planting on the islands (Paxton's planting just in, U)
        for i in range(14 if nm == 'secondary' else 8):
            t = rr.uniform(0, 2 * math.pi); r = rr.uniform(0.55, 0.85)
            x, y = cx + a * r * math.cos(t), cy + b * r * math.sin(t)
            if y < cy - 0.2 * b and nm == 'secondary': continue      # keep the viewing face (S shore) open
            tree(bm, x, y, rr.uniform(12, 22), 'young', rr)
bm_obj('trees_parkland_and_young_island_planting', C['DN54_lake_islands__1854'], planting, [M['bark'], M['leaf']])

# ---------------- sculptures (positions I; grouping after Hawkins' layout: reptiles on the Secondary island,
# mammals on the Tertiary, marine reptiles at the water's edge) ----------------
CS, CT = C['DN54_secondary_island_sculptures__1854'], C['DN54_tertiary_island_mammals__1854']
SCUL = []
def put(name, me, col, x, y, heading_deg, m, z=None, sink=0.4):
    zz = (ground(x, y) if z is None else z) - sink
    o = obj(name, me, col, (x, y, zz), math.radians(heading_deg), (m,)); SCUL.append(o); return o
IG_S = HK.iguanodon(False); IG_R = HK.iguanodon(True)
put('iguanodon_standing', IG_S, CS, 20, 6, -150, M['ig'])
put('iguanodon_recumbent', IG_R, CS, 62, 22, -25, M['ig'])
put('megalosaurus', HK.megalosaurus(), CS, -42, 18, -20, M['meg'])        # faces the Iguanodons (R per park guides)
put('hylaeosaurus', HK.hylaeosaurus(), CS, -95, 42, 95, M['hyl'])       # armoured back to the S bank (R)
ICH = HK.ichthyosaur()
put('ichthyosaur_1', ICH, CS, -150, -50, -60, M['ich'], z=WL - 0.6, sink=0)
put('ichthyosaur_2', ICH, CS, -112, -58, -10, M['ich'], z=WL - 0.9, sink=0)
put('ichthyosaur_3', HK.ichthyosaur(18), CS, -185, -30, -120, M['ich'], z=WL - 0.4, sink=0)
put('plesiosaur_1', HK.plesiosaur(1.0), CS, -40, -72, -40, M['ple'], z=WL - 0.6, sink=0)
put('plesiosaur_2', HK.plesiosaur(-1.0), CS, 5, -68, -110, M['ple'], z=WL - 0.9, sink=0)
put('plesiosaur_3', HK.plesiosaur(0.6), CS, 120, -55, 200, M['ple'], z=WL - 1.2, sink=0)
def base_rocks(bm):
    pts = []
    for o in SCUL:
        if o.location.z < 0: pts += [(o.location.x / F + rng.uniform(-9, 9), o.location.y / F + rng.uniform(-6, 6), rng.uniform(2.5, 5)) for _ in range(5)]
    pts += [(rng.uniform(-200, 160), rng.uniform(-75, -60), rng.uniform(2, 4)) for _ in range(30)]   # rocky shore
    rocks(bm, pts)
bm_obj('shore_rocks_and_bases', C['DN54_lake_islands__1854'], base_rocks, [M['rock']])
# Tertiary island: Megatherium at its tree (R that it clasps a tree), Irish elk group (1854: four built, two stags + two does, one doe reclining; R Wikipedia/cpdinosaurs)
def mg_tree(bm):
    x, y = 300 + 6.2, 55
    z = ground(x, y); strut(bm, (x, y, z - 1), (x - 0.5, y, z + 26), 1.0, 0, 9)
    for k in range(5):
        a = k * 1.3; strut(bm, (x, y, z + 15 + k*2.5), (x + 9*math.cos(a), y + 9*math.sin(a), z + 22 + k*2), 0.35, 0, 6)
    for k in range(5):
        res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=f(6.5))
        bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector((f(x + 7*math.cos(k*1.3)), f(y + 7*math.sin(k*1.3)), f(z + 27 + rng.uniform(-2, 3))))), verts=res['verts'])
        for fc in {fc for v in res['verts'] for fc in v.link_faces}: fc.material_index = 1; fc.smooth = True
bm_obj('megatherium_tree', CT, mg_tree, [M['bark'], M['leaf']])
put('megatherium', HK.megatherium(), CT, 300, 55, 0, M['mgt'])
put('irish_elk_stag', HK.elk(True), CT, 272, 10, -60, M['elk'])
put('irish_elk_stag_2', HK.elk(True, 0.95), CT, 258, 22, -20, M['elk'])
put('irish_elk_doe', HK.elk(False, 0.9), CT, 290, 0, -95, M['elk'])
put('irish_elk_doe_reclining', HK.elk(False, 0.9, lying=True), CT, 300, 8, -130, M['elk'])

# ---------------- geological strata cliff (E end of the lake; sequence after Ansted's design, layer thicknesses I) ----------------
def strata(bm):
    x0, y0 = 455, -10; zb = -2
    for i, th in enumerate([3, 3.5, 4, 3, 4, 3.5, 2.5, 5][::-1]):
        mi = 7 - i
        w = 60 - i * 5; dd = 18 - i * 1.5
        box(bm, x0 - w/2 + i*2, x0 + w/2 + i*2, y0 - dd/2, y0 + dd/2, zb, zb + th, mi)
        zb += th
    for k in range(4):   # dipping blocks (strata shown tilted)
        box(bm, x0 + 28 + k*6, x0 + 34 + k*6, y0 - 8, y0 + 8, -2, 18 - k*4, k)
bm_obj('geological_strata_illustration', C['DN54_geological_strata__1854'], strata, M['strata'])

# ---------------- people (1850s; HP-style lathe stand-ins) ----------------
def lathe(bm, prof, seg, mi, cx=0.0, cy=0.0):
    rings = []
    for r, z in prof:
        if r <= 1e-4: rings.append([bm.verts.new((f(cx), f(cy), f(z)))])
        else: rings.append([bm.verts.new((f(cx + r*math.cos(2*math.pi*k/seg)), f(cy + r*math.sin(2*math.pi*k/seg)), f(z))) for k in range(seg)])
    for a, b in zip(rings, rings[1:]):
        if len(a) == 1 and len(b) == 1: continue
        for k in range(seg):
            if len(a) == 1: q = (a[0], b[k], b[(k+1) % seg])
            elif len(b) == 1: q = (a[k], a[(k+1) % seg], b[0])
            else: q = (a[k], a[(k+1) % seg], b[(k+1) % seg], b[k])
            try: fc = bm.faces.new(q); fc.material_index = mi; fc.smooth = True
            except ValueError: pass
def man(bm, x, y, rot, kind, rr, z=0.0):
    v0 = len(bm.verts); c = 3 if kind == 'smock' else 0
    for s in (-0.25, 0.25): lathe(bm, [(0.19, 0), (0.2, 1.3), (0.23, 2.7), (0, 2.75)], 6, 0, cx=s)
    hem = 2.3 if kind == 'smock' else 2.4
    lathe(bm, [(0, hem), (0.75 if kind == 'smock' else 0.6, hem), (0.6, 3.3), (0.6, 4.3), (0.42, 4.7), (0, 4.76)], 9, c)
    for s in (-0.68, 0.68): lathe(bm, [(0.16, 3.0), (0.17, 4.35), (0, 4.45)], 5, c, cx=s)
    if kind != 'smock': lathe(bm, [(0.0, 4.2), (0.22, 4.25), (0.2, 4.7), (0, 4.72)], 6, 2, cy=-0.42)   # shirt front
    lathe(bm, [(0, 4.72), (0.3, 4.8), (0.34, 5.1), (0.28, 5.4), (0, 5.48)], 8, 1)
    if kind == 'top': lathe(bm, [(0, 5.3), (0.5, 5.3), (0.48, 5.36), (0.32, 5.38), (0.34, 6.25), (0, 6.27)], 9, 0)      # top hat
    elif kind == 'smock': lathe(bm, [(0, 5.3), (0.42, 5.3), (0.36, 5.55), (0, 5.6)], 8, 3)                          # soft cap
    bm.verts.ensure_lookup_table(); vs = [bm.verts[i] for i in range(v0, len(bm.verts))]
    k = rr.uniform(0.95, 1.04)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector((f(x), f(y), f(z)))) @ Matrix.Rotation(rot, 4, 'Z') @ Matrix.Scale(k, 4), verts=vs)
PEOPLE_M = [M['coat'], M['skin'], M['shirt'], M['smock']]

# ---------------- CP034: Hawkins' studio (ILN 1853 print, PD; shed dims I) at x 2000 ----------------
SX = 2000.0; SW_, SL_, SH_ = 60, 110, 26      # interior width (y), length (x), eaves height
def studio(bm):
    x0, x1, y0, y1 = SX - SL_/2, SX + SL_/2, -SW_/2, SW_/2
    box(bm, x0, x1, y0, y1, -0.5, 0, 1)                                        # boarded floor (mi 1 = timber)
    for xx in range(int(x0), int(x1) + 1, 4):                                  # studs + boarding as strips
        for yy in (y0, y1): box(bm, xx - 0.25, xx + 0.25, yy - 0.5, yy, 0, SH_, 1)
    for yy in range(int(y0), int(y1) + 1, 4):
        for xx in (x0, x1): box(bm, xx, xx + (0.5 if xx == x0 else -0.5), yy - 0.25, yy + 0.25, 0, SH_ + (SW_/2 - abs(yy)) * 0.5, 1)
    for yy in (y0 - 0.6, y1):                                                  # sheathing with a high clerestory gap (light)
        box(bm, x0, x1, yy, yy + 0.6, 0, SH_ - 6, 1)
    for xx in (x0 - 0.6, x1):
        box(bm, xx, xx + 0.6, y0, y1, 0, SH_ - 4, 1)
    for xx in range(int(x0) + 10, int(x1), 20):                                # king-post trusses (print R; spacing I)
        ridge = SH_ + SW_/2 * 0.5
        strut(bm, (xx, y0, SH_), (xx, y1, SH_), 0.4, 1, 4)
        strut(bm, (xx, y0, SH_), (xx, 0, ridge), 0.4, 1, 4); strut(bm, (xx, y1, SH_), (xx, 0, ridge), 0.4, 1, 4)
        strut(bm, (xx, 0, SH_), (xx, 0, ridge), 0.3, 1, 4)
        strut(bm, (xx, 0, SH_ + 1), (xx, -SW_/4, SH_ + SW_/8), 0.22, 1, 4); strut(bm, (xx, 0, SH_ + 1), (xx, SW_/4, SH_ + SW_/8), 0.22, 1, 4)
    for side in (-1, 1):                                                       # roof boarding with a glazed strip each side (I)
        for k in range(0, int(SL_), 1):
            pass
        ys = [0, side * SW_/2 * 0.35, side * SW_/2 * 0.62, side * SW_/2]
        for a, b in ((0, 1), (2, 3)):
            ya, yb = ys[a], ys[b]; za, zb = SH_ + (SW_/2 - abs(ya)) * 0.5 + 0.4, SH_ + (SW_/2 - abs(yb)) * 0.5 + 0.4
            v = [bm.verts.new((f(xx), f(yy), f(zz))) for xx, yy, zz in ((x0, ya, za), (x1, ya, za), (x1, yb, zb), (x0, yb, zb))]
            fc = bm.faces.new(v); fc.material_index = 1
    rr = random.Random(3)
    for k in range(9):                                                         # scaffold poles + ledgers round the big Iguanodon
        a = 2 * math.pi * k / 9; px, py = SX + 2 + 21 * math.cos(a), 7 * math.sin(a) * 1.6
        strut(bm, (px, py, 0), (px + rr.uniform(-0.4, 0.4), py, 21), 0.22, 2, 6)
    for hz in (7, 13):
        for k in range(9):
            a, b = 2*math.pi*k/9, 2*math.pi*(k+1)/9
            strut(bm, (SX + 2 + 21*math.cos(a), 11.2*math.sin(a), hz), (SX + 2 + 21*math.cos(b), 11.2*math.sin(b), hz), 0.15, 2, 4)
        box(bm, SX - 8, SX + 12, 9.5, 12, hz - 0.2, hz, 1)                    # plank stage
    for k in range(2):                                                         # ladders
        lx = SX - 22 + k * 40; ly = 12 if k == 0 else -12
        for s in (-0.8, 0.8): strut(bm, (lx + s, ly, 0), (lx + s, ly - 3.5 * (1 if k == 0 else -1), 14), 0.12, 1, 4)
        for r_ in range(1, 14):
            t = r_ / 14; strut(bm, (lx - 0.8, ly - 3.5*t*(1 if k == 0 else -1), 14*t), (lx + 0.8, ly - 3.5*t*(1 if k == 0 else -1), 14*t), 0.06, 1, 4)
    box(bm, SX - 18, SX + 20, -6.5, 6.5, 0, 1.2, 1)                           # low plank base under the figure
    for k in range(6):                                                         # trestle table with tools / small models
        box(bm, SX + 34 + k*0.0, SX + 46, -24, -18, 2.8, 3.1, 1)
    for x_, y_ in ((SX + 35, -23.5), (SX + 45, -23.5), (SX + 35, -18.5), (SX + 45, -18.5)): strut(bm, (x_, y_, 0), (x_, y_, 2.8), 0.12, 1, 4)
    box(bm, SX - 50, SX - 40, 14, 22, 0, 3, 3)                                # plaster mould sections stacked
    box(bm, SX - 50, SX - 46, 12, 24, 3, 7, 3)
bm_obj('hawkins_studio_shed_and_scaffold', C['DN53_hawkins_studio__1853'], studio, [M['plaster'], M['timber'], M['bark'], M['plaster']])
CSTU = C['DN53_hawkins_studio__1853']
obj('studio_iguanodon_in_clay', IG_S.copy(), CSTU, (SX + 2, 0, 1.2), math.radians(180), (M['clay'],))
obj('studio_hylaeosaurus_in_clay', HK.hylaeosaurus(), CSTU, (SX + 34, 16, 0), math.radians(-160), (M['clay'],))
_mg = HK.megalosaurus(); _mg.transform(Matrix.Scale(0.55, 4))       # working maquette head-and-body, reduced (ILN print shows several part-built beasts; I)
obj('studio_megalosaurus_part_built', _mg, CSTU, (SX - 30, 17, 0), math.radians(-20), (M['clay'],))
_elk = HK.elk(False, 0.9); obj('studio_small_mammal', _elk, CSTU, (SX + 30, -18, 0), math.radians(-60), (M['clay'],))
def studio_men(bm):
    rr = random.Random(53)
    for x, y, z, r, k in [(SX + 3, 11, 7.2, math.pi, 'smock'), (SX - 6, 11, 13.2, math.pi + 0.4, 'smock'), (SX + 14, -9, 0, 2.2, 'smock'),
                          (SX - 14, -10, 0, 0.6, 'smock'), (SX + 36, -21, 0, -1.4, 'top'), (SX + 24, 12, 0, 2.6, 'top'), (SX - 30, -4, 0, 1.0, 'smock')]:
        man(bm, x, y, r, k, rr, z)
bm_obj('studio_workmen_and_hawkins', CSTU, studio_men, PEOPLE_M)

# ---------------- CP034b: dinner in the Iguanodon mould, 31 Dec 1853 (ILN print, PD) at x 3000 ----------------
DX = 3000.0
CD = C['DN53_iguanodon_dinner__31Dec1853']
mould = IG_S.copy(); mould.name = 'iguanodon_mould_open'
bm = bmesh.new(); bm.from_mesh(mould)
cut = f(6.0)   # open the top: delete everything above the cut (the mould's upper half was left off for the dinner)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z > cut], context='VERTS')
bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=f(0.4)) if hasattr(bmesh.ops, 'solidify') else None
bm.to_mesh(mould); bm.free()
obj('iguanodon_mould_open', mould, CD, (DX, 0, 4.0), 0, (M['plaster'],))
def dinner(bm):
    box(bm, DX - 30, DX + 30, -16, 16, 0, 4.0, 1)                                  # raised plank deck
    for s in (-1, 1):                                                              # railings
        for xx in range(int(DX - 30), int(DX + 31), 5): strut(bm, (xx, s*16, 4), (xx, s*16, 7), 0.12, 1, 4)
        strut(bm, (DX - 30, s*16, 7), (DX + 30, s*16, 7), 0.12, 1, 4)
    for k in range(5): box(bm, DX - 3 + 0, DX + 3, -16 - 1.6*(k+1), -16 - 1.6*k, 0, 4.0 - 0.8*(k+1), 1)   # central stairs
    box(bm, DX - 13, DX + 11, -2.6, 2.6, 7.4, 7.9, 1)                             # boarded floor laid inside the mould (I)
    box(bm, DX - 11, DX + 9, -1.6, 1.6, 10.1, 10.4, 2)                               # table (linen) inside the beast
    for x_ in (DX - 10, DX + 8):
        for y_ in (-1.3, 1.3): strut(bm, (x_, y_, 7.9), (x_, y_, 10.1), 0.15, 1, 4)
    for k in range(13):                                                            # marquee: striped canopy on poles
        a0, a1 = -math.pi/2 + math.pi*k/13, -math.pi/2 + math.pi*(k+1)/13
        v = [bm.verts.new((f(xx), f(yy), f(zz))) for xx, yy, zz in
             ((DX - 34, 22*math.sin(a0), 26 + 8*math.cos(a0)), (DX + 34, 22*math.sin(a0), 26 + 8*math.cos(a0)),
              (DX + 34, 22*math.sin(a1), 26 + 8*math.cos(a1)), (DX - 34, 22*math.sin(a1), 26 + 8*math.cos(a1)))]
        fc = bm.faces.new(v); fc.material_index = 3 + (k % 2); fc.smooth = True
    for xx in (DX - 34, DX, DX + 34):
        for s in (-1, 1): strut(bm, (xx, s*22, 0), (xx, s*22, 26), 0.35, 1, 6)
    for xx in (DX - 34, DX + 34):                                                  # gable curtains (drawn back)
        for s in (-1, 1): box(bm, xx - 0.2, xx + 0.2, s*22 - s*6, s*22, 0, 26, 3 + (s > 0))
    for k, nm in enumerate(range(4)):                                              # name boards (BUCKLAND / CUVIER / OWEN / MANTELL)
        box(bm, DX - 24 + k*16, DX - 14 + k*16, 21.5, 21.8, 22, 24.5, 2)
    strut(bm, (DX - 1, 0, 32), (DX - 1, 0, 20), 0.08, 5, 4)                       # chandelier
    for k in range(8):
        a = 2*math.pi*k/8; strut(bm, (DX - 1, 0, 20), (DX - 1 + 2.5*math.cos(a), 2.5*math.sin(a), 20.6), 0.1, 5, 4)
    box(bm, DX - 25, DX - 17, -25, -17.5, 0, 12.0, 1)                              # press/spectators' gallery (I; ILN print is a raised view)
    for k in range(8): box(bm, DX - 25 - 1.2*(k+1), DX - 25 - 1.2*k, -25, -21.5, 0, 12.0 - 1.5*(k+1), 1)   # gallery steps
bm_obj('dinner_deck_marquee_table', CD, dinner, [M['plaster'], M['timber'], M['linen'], M['cloth_r'], M['cloth_w'], M['brass']])
def guests(bm):
    rr = random.Random(1853)
    for k in range(10):
        for s in (-1, 1): man(bm, DX - 9.5 + k*1.9, s*2.3, 0.0 if s > 0 else math.pi, 'plain', rr, 7.9 - 1.6)
    man(bm, DX + 10.6, 0, -math.pi/2, 'plain', rr, 7.9 - 1.6)                 # Owen at the head (R that he sat in the head; pose I)
bm_obj('dinner_guests_21', CD, guests, PEOPLE_M)
def yard(bm):   # grass yard under the off-site studio / dinner sets (I): hides the empty sky-ground horizon
    box(bm, 1000, 7000, -3000, 3000, -0.3, -0.05, 0)
bm_obj('sets_yard_grass', C['DN53_hawkins_studio__1853'], yard, [M['grass']])

# ---------------- cameras (36 mm sensor, 1.6 m eye, no roll) ----------------
EYE = 1.6 / F
def cam(name, loc, look, lens):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.sensor_width = 36; cd.clip_end = 3000; cd.clip_start = 0.1
    o = bpy.data.objects.new(name, cd); C['CAMERAS'].objects.link(o); o.location = [f(v) for v in loc]
    o.rotation_euler = (Vector([f(v) for v in look]) - o.location).to_track_quat('-Z', 'Y').to_euler(); return o
def walk_y(x): return -5 - LB * math.sqrt(max(0, 1.32 - ((x - 60) / 440) ** 2))
cam('CAM_CP043_lake_islands_35mm', (-60, walk_y(-60), ground(-60, walk_y(-60)) + EYE), (5, 10, 4), 35)
cam('CAM_CP043b_iguanodons_detail_50mm', (48, -84, WL + EYE), (36, 14, 4.5), 50)   # standing in a boat on the lake (I)
cam('CAM_CP043c_tertiary_megatherium_elk_50mm', (318, -60, WL + EYE), (289, 24, 8), 50)   # from a boat (I)
cam('CAM_CP034_hawkins_studio_28mm', (SX - 48, -22, EYE), (SX + 4, 0, 8), 28)
cam('CAM_CP034b_iguanodon_dinner_28mm', (DX - 21, -21, 12.0 + EYE), (DX - 1, 0, 9.5), 28)   # standing on the press gallery (I), print-like raised view
sc.camera = bpy.data.objects['CAM_CP043_lake_islands_35mm']

# ---------------- world / render ----------------
w = bpy.data.worlds.new('sky'); sc.world = w; w.use_nodes = True; nt = w.node_tree; bg = nt.nodes['Background']
sky = nt.nodes.new('ShaderNodeTexSky')
for t in ('NISHITA', 'MULTIPLE_SCATTERING', 'SINGLE_SCATTERING'):
    try: sky.sky_type = t; break
    except Exception: pass
try: sky.sun_elevation = math.radians(34); sky.sun_rotation = math.radians(150)
except Exception: pass
nt.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 0.25
sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 2.0; sun.angle = math.radians(1.0)
so = bpy.data.objects.new('sun', sun); root.objects.link(so); so.rotation_euler = (math.radians(56), 0, math.radians(150))
for nm, loc, e, sz in [('studio_clerestory_light_S', (SX, -26, 22), 9000, 90), ('studio_clerestory_light_N', (SX, 26, 22), 6000, 90), ('marquee_glow', (DX, 0, 24), 9000, 60)]:
    ld = bpy.data.lights.new(nm, 'AREA'); ld.energy = e; ld.shape = 'RECTANGLE'; ld.size = f(sz); ld.size_y = f(8)
    lo = bpy.data.objects.new(nm, ld); (CSTU if 'studio' in nm else CD).objects.link(lo); lo.location = [f(v) for v in loc]
    lo.rotation_euler = (math.radians(90 if loc[1] < 0 else -90) if 'studio' in nm else 0, 0, 0)
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 48; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 6
sc.render.resolution_x = 1920; sc.render.resolution_y = 1080
sc.view_settings.view_transform = 'AgX'; sc.view_settings.exposure = -1.4; sc.unit_settings.system = 'METRIC'
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
print('BUILD_OK', OUT, 'objects', len(bpy.data.objects), 'faces', sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH'))
