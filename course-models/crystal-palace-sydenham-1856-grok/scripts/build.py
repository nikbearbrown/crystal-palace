"""Scripted build of the Sydenham Crystal Palace, c.1856 state (SY-EARLY). Blender 5.1 headless.
usage: blender -b -P scripts/build.py -- <out.blend>
"""
import bpy, bmesh, math, sys, os
from mathutils import Matrix, Vector
sys.path.insert(0, os.path.dirname(__file__))
from params import *
OUT = sys.argv[sys.argv.index('--')+1]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
f = lambda v: v*F

# ---------- materials ----------
def mat(name, base, rough=0.5, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*base, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal; return m
def glass_mat(name, tint=(0.82,0.88,0.86), mull=0.0, spacing=8.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    n.clear(); out = n.new('ShaderNodeOutputMaterial')
    tr = n.new('ShaderNodeBsdfTransparent'); tr.inputs[0].default_value = (*tint,1)
    gl = n.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.04
    fr = n.new('ShaderNodeFresnel'); fr.inputs['IOR'].default_value = 1.52
    mx = n.new('ShaderNodeMixShader'); l.new(fr.outputs[0], mx.inputs[0]); l.new(tr.outputs[0], mx.inputs[1]); l.new(gl.outputs[0], mx.inputs[2])
    last = mx
    if mull > 0:  # sash-bar grid as shader (world-space, every `spacing` ft)
        tc = n.new('ShaderNodeTexCoord'); sep = n.new('ShaderNodeSeparateXYZ'); l.new(tc.outputs['Object'], sep.inputs[0])
        def stripe(comp):
            mth = n.new('ShaderNodeMath'); mth.operation='PINGPONG'; mth.inputs[1].default_value = f(spacing)/2
            l.new(sep.outputs[comp], mth.inputs[0])
            cmp = n.new('ShaderNodeMath'); cmp.operation='LESS_THAN'; cmp.inputs[1].default_value = mull
            l.new(mth.outputs[0], cmp.inputs[0]); return cmp
        sx, sz = stripe('X'), stripe('Z'); sy = stripe('Y')
        mx2 = n.new('ShaderNodeMath'); mx2.operation='MAXIMUM'; l.new(sx.outputs[0], mx2.inputs[0]); l.new(sz.outputs[0], mx2.inputs[1])
        mx3 = n.new('ShaderNodeMath'); mx3.operation='MAXIMUM'; l.new(mx2.outputs[0], mx3.inputs[0]); l.new(sy.outputs[0], mx3.inputs[1])
        ir = n.new('ShaderNodeBsdfPrincipled'); ir.inputs['Base Color'].default_value=(0.42,0.44,0.46,1); ir.inputs['Roughness'].default_value=0.5
        mm = n.new('ShaderNodeMixShader'); l.new(mx3.outputs[0], mm.inputs[0]); l.new(mx.outputs[0], mm.inputs[1]); l.new(ir.outputs[0], mm.inputs[2]); last = mm
    l.new(last.outputs[0], out.inputs[0])
    m.blend_method = 'BLEND' if hasattr(m,'blend_method') else None
    return m
def socket(node, ident, out=False):
    return [x for x in (node.outputs if out else node.inputs) if x.identifier == ident][0]
def iron_oj(name):
    """Iron with toggleable Owen Jones-style polychromy (U): Value node 'OJ_TOGGLE' 0=grey,1=OJ.
    OJ approximation: blue ground, yellow bands on vertical faces, red undersides (after 1851 scheme; Sydenham scheme U)."""
    m = mat(name, (0.50,0.53,0.55), 0.45, 0.2); nt = m.node_tree; n = nt.nodes; l = nt.links
    b = n['Principled BSDF']
    tog = n.new('ShaderNodeValue'); tog.name = tog.label = 'OJ_TOGGLE'; tog.outputs[0].default_value = 1.0
    geo = n.new('ShaderNodeNewGeometry'); sep = n.new('ShaderNodeSeparateXYZ'); l.new(geo.outputs['Normal'], sep.inputs[0])
    sepP = n.new('ShaderNodeSeparateXYZ'); l.new(geo.outputs['Position'], sepP.inputs[0])
    pp = n.new('ShaderNodeMath'); pp.operation = 'PINGPONG'; pp.inputs[1].default_value = f(3.0); l.new(sepP.outputs['Z'], pp.inputs[0])
    yb = n.new('ShaderNodeMath'); yb.operation = 'LESS_THAN'; yb.inputs[1].default_value = f(0.7); l.new(pp.outputs[0], yb.inputs[0])
    vz = n.new('ShaderNodeMath'); vz.operation = 'ABSOLUTE'; l.new(sep.outputs['Z'], vz.inputs[0])
    vert = n.new('ShaderNodeMath'); vert.operation = 'LESS_THAN'; vert.inputs[1].default_value = 0.5; l.new(vz.outputs[0], vert.inputs[0])
    ystripe = n.new('ShaderNodeMath'); ystripe.operation = 'MULTIPLY'; l.new(yb.outputs[0], ystripe.inputs[0]); l.new(vert.outputs[0], ystripe.inputs[1])
    under = n.new('ShaderNodeMath'); under.operation = 'LESS_THAN'; under.inputs[1].default_value = -0.5; l.new(sep.outputs['Z'], under.inputs[0])
    def mix(fac_out, a, bcol):
        mx = n.new('ShaderNodeMix'); mx.data_type = 'RGBA'; l.new(fac_out, socket(mx,'Factor_Float'))
        for ident, v in (('A_Color', a), ('B_Color', bcol)):
            if isinstance(v, tuple): socket(mx, ident).default_value = (*v, 1)
            else: l.new(v, socket(mx, ident))
        return socket(mx, 'Result_Color', True)
    c1 = mix(ystripe.outputs[0], (0.10,0.17,0.42), (0.80,0.62,0.12))   # blue ground / yellow bands
    c2 = mix(under.outputs[0], c1, (0.55,0.07,0.05))                     # red undersides
    c3 = mix(tog.outputs[0], (0.50,0.53,0.55), c2)
    l.new(c3, b.inputs['Base Color']); return m
def boards(name):
    """guide p.35: 1.5 in boards, 0.5 in gaps (B); board run direction along X (I)"""
    m = mat(name, (0.30,0.22,0.15), 0.8); nt = m.node_tree; n = nt.nodes; l = nt.links; b = n['Principled BSDF']
    tc = n.new('ShaderNodeTexCoord'); sp = n.new('ShaderNodeSeparateXYZ'); l.new(tc.outputs['Object'], sp.inputs[0])
    pp = n.new('ShaderNodeMath'); pp.operation = 'PINGPONG'; pp.inputs[1].default_value = f(1/12); l.new(sp.outputs['Y'], pp.inputs[0])
    g = n.new('ShaderNodeMath'); g.operation = 'LESS_THAN'; g.inputs[1].default_value = f(0.25/12); l.new(pp.outputs[0], g.inputs[0])
    nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.6; l.new(tc.outputs['Object'], nz.inputs['Vector'])
    ramp = n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color = (0.26,0.18,0.11,1); ramp.color_ramp.elements[1].color = (0.40,0.29,0.18,1)
    l.new(nz.outputs['Fac'], ramp.inputs[0])
    mx = n.new('ShaderNodeMix'); mx.data_type = 'RGBA'; l.new(g.outputs[0], socket(mx,'Factor_Float'))
    l.new(ramp.outputs[0], socket(mx,'A_Color')); socket(mx,'B_Color').default_value = (0.03,0.025,0.02,1)
    l.new(socket(mx,'Result_Color',True), b.inputs['Base Color']); return m
M = {
 'iron': iron_oj('iron_painted_OJ'),
 'iron_ext': mat('iron_exterior_pale', (0.74,0.74,0.70), 0.5, 0.1),   # r05 I: period photos 0074/0007 read pale outside; OJ kept inside     # U: Sydenham paint scheme unresolved; toggle via scripts/set_palette.py
 'marble': mat('statuary_placeholder', (0.78,0.76,0.72), 0.5),
 'foliage': mat('foliage', (0.07,0.16,0.05), 0.8),
 'palm': mat('palm_frond', (0.10,0.20,0.06), 0.7),
 'bark': mat('bark', (0.20,0.15,0.10), 0.9),
 'glass_roof': glass_mat('glass_roof', (0.80,0.86,0.85), 0.012, 8.0),
 'glass_wall': glass_mat('glass_wall', (0.58,0.66,0.68), 0.02, 8.0),
 'floor': boards('boards_gapped'),
 'brick': mat('brick_basement', (0.55,0.36,0.27), 0.85),
 'stone': mat('terrace_stone', (0.52,0.49,0.43), 0.8),
 'gravel': mat('gravel', (0.40,0.37,0.31), 0.95),
 'grass': mat('grass', (0.16,0.27,0.09), 0.9),
 'water': mat('water', (0.05,0.10,0.12), 0.05),
 'wood': mat('wood_panel', (0.55,0.50,0.42), 0.7),
}
# r07 materials: fountain jets (spray as translucent cones, I) and flower-bed planting (colour mix U)
M['jet'] = mat('fountain_jet_spray', (0.86,0.89,0.92), 0.35)
_jb = M['jet'].node_tree.nodes['Principled BSDF']; _jb.inputs['Alpha'].default_value = 0.4; _jb.inputs['Transmission Weight'].default_value = 0.85; _jb.inputs['Roughness'].default_value = 0.6
def flowers_mat(name):
    m = mat(name, (0.3,0.2,0.1), 0.85); nt = m.node_tree; n = nt.nodes; l = nt.links; b = n['Principled BSDF']
    tc = n.new('ShaderNodeTexCoord'); nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3.0
    l.new(tc.outputs['Object'], nz.inputs['Vector'])
    ramp = n.new('ShaderNodeValToRGB'); cr = ramp.color_ramp; cr.interpolation = 'CONSTANT'
    cr.elements[0].position = 0.0; cr.elements[0].color = (0.10,0.22,0.06,1)
    cr.elements[1].position = 0.45; cr.elements[1].color = (0.55,0.05,0.04,1)
    for pos, col in ((0.55, (0.75,0.62,0.10,1)), (0.62, (0.80,0.78,0.72,1)), (0.70, (0.45,0.04,0.20,1)), (0.78, (0.10,0.22,0.06,1))):
        e = cr.elements.new(pos); e.color = col
    l.new(nz.outputs['Fac'], ramp.inputs[0]); l.new(ramp.outputs[0], b.inputs['Base Color']); return m
M['flowers'] = flowers_mat('flower_beds_bedding')

# ---------- collections ----------
# r10: SY-POST66 state toggle (env SY_STATE=POST66). Fire of 30 Dec 1866: north transept never rebuilt (Park Trust
# chronology; Norwood Soc.), north nave rebuilt over ~2 years (Park Trust), north wing only partly rebuilt (Black's guide
# via History Hunters; crystal.dircon: 'except part of a low narrow wing'); 1928 aerial EPW021373 shows no north transept
# and a continuous nave to an arched north end gable. See DEPARTURES D-R10-P*.
# r11: further states share this script: 1936 (Nov 1936 pre-fire), FIRE (night of 30 Nov 1936), AFTER (morning after,
# Dec 1936), RUINS (cleared site c.1937-40, both towers), RUINS41 (after the tower demolitions of 1940-41). All later
# states inherit the POST66 fabric (the north transept stays missing). See scripts/states.py and DEPARTURES r11.
STATE = os.environ.get('SY_STATE', 'EARLY').upper() or 'EARLY'
ROOTS = {'EARLY': 'SY-EARLY_c1856', 'POST66': 'SY-POST66_c1868', '1936': 'SY-1936_Nov1936_preFire',
         'FIRE': 'SY-1936FIRE_30Nov1936_night', 'AFTER': 'SY-1936AFTER_Dec1936_morning',
         'RUINS': 'SY-RUINS_c1937-40', 'RUINS41': 'SY-RUINS_post1941'}
assert STATE in ROOTS, STATE
POST66 = STATE != 'EARLY'
root = bpy.data.collections.new(ROOTS[STATE]); sc.collection.children.link(root)
def coll(name, parent=root):
    c = bpy.data.collections.new(name); parent.children.link(c); return c
C = {k: coll(k) for k in ['SY_main_frame', 'SY_main_roofs_glazing', 'SY_nave_vault', 'SY_central_transept',
     'SY_south_transept', 'SY_north_transept__lost1866', 'SY_crossing_towers', 'SY_basement_garden_front',
     'SY_wings', 'SY54_railway_colonnade', 'SY56_water_towers__dated', 'SY56_fountains_basins__dated',
     'SY_terraces_terrain', 'SY_facade_ironwork', 'SY_nave_planting_statuary__placeholders', 'SY56_park_fountains_cascades__dated', 'CAMERAS']}
refc = bpy.data.collections.new('REF_plan_0205'); sc.collection.children.link(refc)

class MB:
    """mesh builder: accumulate boxes/quads in one bmesh per (collection, material)"""
    def __init__(s, name, col, m):
        s.bm = bmesh.new(); s.name = name; s.col = col; s.m = m
    def box(s, x0,x1,y0,y1,z0,z1):  # feet
        if x1<x0: x0,x1=x1,x0
        if y1<y0: y0,y1=y1,y0
        if z1<z0: z0,z1=z1,z0
        r = bmesh.ops.create_cube(s.bm, size=1.0)
        mtx = Matrix.Translation(Vector((f((x0+x1)/2), f((y0+y1)/2), f((z0+z1)/2)))) @ Matrix.Diagonal((f(x1-x0), f(y1-y0), f(z1-z0), 1))
        bmesh.ops.transform(s.bm, matrix=mtx, verts=r['verts'])
    def poly(s, pts):  # list of (x,y,z) feet
        vs = [s.bm.verts.new((f(a),f(b),f(c))) for a,b,c in pts]; s.bm.faces.new(vs)
    def strut(s, p0, p1, w=0.5, d=None):  # r07: oriented square bar between two points (feet)
        d = d or w; a = Vector(p0); b = Vector(p1); v = b - a; L = v.length
        if L < 1e-3: return
        r = bmesh.ops.create_cube(s.bm, size=1.0)
        q = v.normalized().to_track_quat('Z', 'Y')
        mtx = Matrix.Translation(Vector([f(c) for c in (a+b)/2])) @ q.to_matrix().to_4x4() @ Matrix.Diagonal((f(w), f(d), f(L), 1))
        bmesh.ops.transform(s.bm, matrix=mtx, verts=r['verts'])
    def cyl(s, x, y, z0, z1, r0, r1=None, seg=12):  # r07: (tapered) cylinder / cone frustum, feet
        r1 = r0 if r1 is None else r1
        bmesh.ops.create_cone(s.bm, cap_ends=True, segments=seg, radius1=f(r0), radius2=f(max(r1, 0.001)), depth=f(z1-z0),
                              matrix=Matrix.Translation(Vector((f(x), f(y), f((z0+z1)/2)))))
    def done(s):
        me = bpy.data.meshes.new(s.name); s.bm.to_mesh(me); s.bm.free()
        me.materials.append(s.m); o = bpy.data.objects.new(s.name, me); s.col.objects.link(o); return o

HALF = LENGTH/2
def in_span(x, xs):  # inside a transept span (open interior)
    return any(abs(x-c) < w/2 - 0.1 for c,w in xs)
TSPANS = [(0, CT_SPAN), (-ST_X, ST_SPAN)] + ([] if POST66 else [(ST_X, ST_SPAN)])   # POST66: north transept bay rebuilt as plain nave bays (R/I)
def tcol(x):
    if abs(x) < CT_SPAN/2+0.1: return 'SY_central_transept'
    if abs(x-ST_X) < ST_SPAN/2+0.1: return 'SY_north_transept__lost1866'
    if abs(x+ST_X) < ST_SPAN/2+0.1: return 'SY_south_transept'
    return None

def band_h(y):  # roof height of band containing y
    for hi,lo,h in BANDS:
        if lo <= y <= hi: return h
def col_h(y):
    hs = []
    for hi,lo,h in BANDS:
        if lo-0.1 <= y <= hi+0.1: hs.append(NAVE_SPRING if h=='vault' else h)
    return max(hs)

# r08 courts: main-frame voids where a fine-arts court occupies the ground floor (columns/girders/gallery floor omitted
# inside the court rectangle; Egyptian court x180-276 y60-156 per plans 0205/0226; I - the real columns' treatment is U)
COURT_VOIDS = [] if os.environ.get('SY_NO_COURTS') else [(180, 276, 60, 156)] + ([(492, 564, 60, 156)] if POST66 else [])   # POST66: restored Alhambra keeps its void in the infilled bay (I)
def in_court(x, y): return any(x0 < x < x1 and y0 < y < y1 for x0, x1, y0, y1 in COURT_VOIDS)
# ---------- main frame: columns + girders on the 24 ft grid ----------
frame = {}
def fb(key):
    if key not in frame: frame[key] = MB('frame_'+key, C[key], M['iron'])
    return frame[key]
xs_grid = [-HALF + i*BAY for i in range(int(LENGTH/BAY)+1)]
CW = 0.67  # 8 in column (HP precedent, I)
for x in xs_grid:
    for y in COL_Y:
        if in_span(x, TSPANS) and abs(y) < 156-0.1: continue  # transept interiors open full height (I)
        if in_court(x, y): continue
        h = col_h(y)
        key = tcol(x) if (tcol(x) and abs(y)<156-0.1) else 'SY_main_frame'
        fb(key).box(x-CW/2, x+CW/2, y-CW/2, y+CW/2, 0, h)
        # 8 ft-advanced paired columns into the nave every 72 ft (guide p.35) -> at nave edge lines
        if abs(y) == 36 and (round((x+HALF)/BAY) % 3 == 0) and not in_span(x,TSPANS):
            yy = y - math.copysign(8, y)
            fb('SY_main_frame').box(x-CW/2, x+CW/2, yy-CW/2, yy+CW/2, 0, NAVE_SPRING)
            fb('SY_main_frame').box(x-0.4, x+0.4, min(y,yy), max(y,yy), NAVE_SPRING-3, NAVE_SPRING)
# girders: along X on every column line at each tier up to its height; along Y between lines
for y in COL_Y:
    h = col_h(y)
    for t in TIERS + ([NAVE_SPRING] if abs(y)==36 else []):
        if t > h+0.1: continue
        x = -HALF
        segs = []
        for i in range(len(xs_grid)-1):
            xa, xb = xs_grid[i], xs_grid[i+1]
            if in_span((xa+xb)/2, TSPANS) and abs(y)<156-0.1: continue
            if in_court((xa+xb)/2, y): continue
            fb('SY_main_frame').box(xa, xb, y-0.35, y+0.35, t-3, t)
for x in xs_grid:
    if in_span(x, TSPANS): continue
    for (ya, yb) in zip(COL_Y[:-1], COL_Y[1:]):
        if abs(ya)==36 and abs(yb)==36: continue  # nave: vault ribs instead
        if in_court(x, (ya+yb)/2): continue
        hmin = min(col_h(ya), col_h(yb))
        for t in TIERS:
            if t <= hmin+0.1:
                fb('SY_main_frame').box(x-0.35, x+0.35, yb, ya, t-3, t)
# gallery floors at tier 1 in the inner bands (I: HP practice; Sydenham gallery area 261,568 sq ft, guide p.35)
gal = MB('gallery_floors', C['SY_main_frame'], M['floor'])
def galbox(xa, xb, yl, yh, z0, z1):  # r08: gallery floor strip with court voids cut out
    cuts = sorted((x0, x1) for x0, x1, y0, y1 in COURT_VOIDS if y0 < (yl+yh)/2 < y1 and x0 < xb and x1 > xa)
    for x0, x1 in cuts:
        if x0 > xa: gal.box(xa, x0, yl, yh, z0, z1)
        xa = max(xa, x1)
    if xb > xa: gal.box(xa, xb, yl, yh, z0, z1)
for (yh, yl) in [(108,60),(60,36),(-36,-60),(-60,-108)]:
    xa = -HALF
    for c,w in sorted(TSPANS):
        galbox(xa, c-w/2, yl, yh, GALLERY_FLOOR-0.6, GALLERY_FLOOR); xa = c+w/2
    galbox(xa, HALF, yl, yh, GALLERY_FLOOR-0.6, GALLERY_FLOOR)
for (yh, yl) in [(60,36),(-36,-60)]:  # second gallery in the tower stacks
    xa = -HALF
    for c,w in sorted(TSPANS):
        gal.box(xa, c-w/2, yl, yh, TIERS[1]+0.2, TIERS[1]+0.8); xa = c+w/2
    gal.box(xa, HALF, yl, yh, TIERS[1]+0.2, TIERS[1]+0.8)
gal.done()
for _mb in list(frame.values()): _mb.done()  # r04 BUGFIX: r01-r03 never finalised the column/girder meshes
# ground floor (boarded, 1.5 in boards with gaps: shader-free, U)
fl = MB('main_floor', C['SY_main_frame'], M['floor'])
for xa_, xb_ in zip(xs_grid[:-1], xs_grid[1:]): fl.box(xa_, xb_, -156, 156, -1.5, 0)   # r07: per-bay so section slices show a cut floor (joist depth I)
fl.done()

# ---------- flat ridge-and-furrow roofs ----------
rf = MB('ridge_furrow_roofs', C['SY_main_roofs_glazing'], M['glass_roof'])
gut = MB('roof_gutters', C['SY_main_roofs_glazing'], M['iron'])
RF = 8.0; RISE = 2.0
for hi, lo, h in BANDS:
    if h == 'vault': continue
    x = -HALF
    while x < HALF - 0.01:
        xm = x + RF/2
        if not in_span(xm, TSPANS):
            rf.poly([(x,lo,h),(xm,lo,h+RISE),(xm,hi,h+RISE),(x,hi,h)])
            rf.poly([(xm,lo,h+RISE),(x+RF,lo,h),(x+RF,hi,h),(xm,hi,h+RISE)])
            gut.box(x-0.25, x+0.25, lo, hi, h-0.6, h)
        x += RF
# transept zones: flat roofs of the low outer bands still run through side transepts? -> no, transept vault covers full width (I)
rf.done(); gut.done()

# ---------- vertical glazed walls (step faces between bands, ends, fronts) ----------
gw = MB('glazed_walls', C['SY_main_roofs_glazing'], M['glass_wall'])
FI = MB('facade_ironwork', C['SY_facade_ironwork'], M['iron_ext'])
def facade(p0, p1, z0, z1, bands=(), mull=8.0, out=0.0):
    """iron sash-bars every `mull` ft, 24 ft stanchions, horizontal fascia bands (I: HP-type glazing rhythm; Sydenham detail U)"""
    (xa, ya), (xb, yb) = p0, p1; L = math.hypot(xb-xa, yb-ya)
    if L < 0.5 or z1 - z0 < 0.5: return
    ux, uy = (xb-xa)/L, (yb-ya)/L
    k = 0; t = 0.0
    while t <= L + 0.01:
        x, y = xa + ux*t, ya + uy*t; w = 0.9 if (k % 3 == 0) else 0.3
        FI.box(x-w/2, x+w/2, y-w/2, y+w/2, z0, z1); t += mull; k += 1
    for z in (z0,) + tuple(bands) + (z1,):
        if z0 - 0.1 <= z <= z1 + 0.1:
            zz0 = max(z0, z-2.5); FI.box(min(xa,xb)-abs(uy)*0.5, max(xa,xb)+abs(uy)*0.5, min(ya,yb)-abs(ux)*0.5, max(ya,yb)+abs(ux)*0.5, zz0, max(zz0+0.6, z))
def wall_y(y, z0, z1, xa=-HALF, xb=HALF, skip=True):
    segs = [(xa, xb)]
    if skip:
        segs = []; a = xa
        for c,w in sorted(TSPANS):
            if c-w/2 > a: segs.append((a, c-w/2))
            a = max(a, c+w/2)
        if a < xb: segs.append((a, xb))
    for a,b in segs:
        gw.poly([(a,y,z0),(b,y,z0),(b,y,z1),(a,y,z1)])
        facade((a,y),(b,y), z0, z1, bands=[t for t in TIERS if z0 < t < z1] + [z0 + (z1-z0)/2] * (z1-z0 > 18))
if COURT_VOIDS: wall_y(156, 0, TIERS[0], xb=180); wall_y(156, 0, TIERS[0], xa=248.4)
else: wall_y(156, 0, TIERS[0])   # r08: Egyptian Museum/Abu Simbel annex breaks the Parade wall (plan 0226; I)
wall_y(132, TIERS[0], TIERS[1]); wall_y(60, TIERS[1], TIERS[2]); wall_y(36, TIERS[2], NAVE_SPRING)
wall_y(-156, 0, TIERS[0]); wall_y(-108, TIERS[0], TIERS[1]); wall_y(-60, TIERS[1], TIERS[2]); wall_y(-36, TIERS[2], NAVE_SPRING)
# end walls x = +-HALF: stepped profile
for xe in (-HALF, HALF):
    for hi, lo, h in BANDS:
        top = NAVE_SPRING if h == 'vault' else h
        gw.poly([(xe,lo,0),(xe,hi,0),(xe,hi,top),(xe,lo,top)])
        facade((xe,lo),(xe,hi), 0, top, bands=[t for t in TIERS if t < top])
    # nave end lunette
    n = 24
    for i in range(n):
        a0 = math.pi*i/n; a1 = math.pi*(i+1)/n
        gw.poly([(xe,0,NAVE_SPRING),(xe,36*math.cos(a0),NAVE_SPRING+36*math.sin(a0)),(xe,36*math.cos(a1),NAVE_SPRING+36*math.sin(a1))])
gw.done()
# west front timber panelling at ground tier (guide p.35 "portion at the west front panelled with wood"; extent U)
wp = MB('west_front_timber_dado', C['SY_main_roofs_glazing'], M['wood']); wp.box(-HALF, HALF, 156, 156.4, 0, 6); wp.done()

# ---------- barrel vaults ----------
def vault(name, col, axis, c, span, spring, a_lo, a_hi, rib_every=24.0, skip=None, nseg=32):
    """axis 'x': vault runs along X between a_lo..a_hi, centred y=c. axis 'y': runs along Y, centred x=c"""
    g = MB(name+'_glass', col, M['glass_roof']); r = MB(name+'_ribs', col, M['iron'])
    R = span/2
    def P(t, u, rr=R):  # t along axis, u angle
        if axis=='x': return (t, c + rr*math.cos(u), spring + rr*math.sin(u))
        return (c + rr*math.cos(u), t, spring + rr*math.sin(u))
    # skin in 8 ft strips
    t = a_lo
    while t < a_hi - 0.01:
        t1 = min(t+8.0, a_hi)
        if not (skip and skip((t+t1)/2)):
            for i in range(nseg):
                u0 = math.pi*i/nseg; u1 = math.pi*(i+1)/nseg
                g.poly([P(t,u0),P(t1,u0),P(t1,u1),P(t,u1)])
        t = t1
    # r07: ribs re-sized after photo 0074 (deep, closely spaced arched rib bands; I for sizes):
    #  main lattice ribs every 24 ft: two chords (outer flange 1.2 x 0.5, inner chord 1.2 x 0.6) 3.5 ft apart with zigzag web;
    #  secondary ribs every 8 ft: solid band 0.5 wide x 1.2 deep; purlins every 2nd facet; ridge cresting.
    DEP = 3.5
    def rib_band(t, w, dep, rr):
        for i in range(nseg):
            u0 = math.pi*i/nseg; u1 = math.pi*(i+1)/nseg; ta, tb = t-w/2, t+w/2
            pa, pb = P(ta,u0,rr), P(ta,u1,rr); pc, pd = P(tb,u1,rr), P(tb,u0,rr)
            qa, qb = P(ta,u0,rr-dep), P(ta,u1,rr-dep); qc, qd = P(tb,u1,rr-dep), P(tb,u0,rr-dep)
            r.poly([pa,pb,qb,qa]); r.poly([pd,pc,qc,qd]); r.poly([qa,qb,qc,qd]); r.poly([pa,pb,pc,pd])
    t = a_lo; k = 0
    while t <= a_hi + 0.01:
        if not (skip and skip(t)):
            if k % 3 == 0:
                rib_band(t, 1.2, 0.5, R); rib_band(t, 1.2, 0.6, R-DEP+0.6)
                for i in range(nseg):   # zigzag lattice web between the chords
                    u0 = math.pi*i/nseg; u1 = math.pi*(i+1)/nseg
                    r.strut(P(t, u0, R-0.5), P(t, u1, R-DEP+0.6), 0.35, 0.35)
            else:
                rib_band(t, 0.5, 1.2, R)
        t += 8.0; k += 1
    for i in range(0, nseg+1, 2):
        u = math.pi*i/nseg; a = P(a_lo,u)
        if axis=='x': r.box(a_lo, a_hi, a[1]-0.25, a[1]+0.25, a[2]-0.7, a[2])
        else: r.box(a[0]-0.25, a[0]+0.25, a_lo, a_hi, a[2]-0.7, a[2])
    top = P(a_lo, math.pi/2)
    if axis=='x': r.box(a_lo, a_hi, top[1]-0.6, top[1]+0.6, top[2], top[2]+1.6)          # ridge cresting band (photo 0074 ridge ornament; I)
    else: r.box(top[0]-0.6, top[0]+0.6, a_lo, a_hi, top[2], top[2]+1.6)
    return g.done(), r.done()
vault('nave_vault', C['SY_nave_vault'], 'x', 0, NAVE_SPAN, NAVE_SPRING, -HALF, HALF, 24.0, skip=lambda t: in_span(t, TSPANS))
CT_Y0, CT_Y1 = -156-CT_GARDEN_PROJ, 156+CT_WEST_PROJ
vault('central_transept_vault', C['SY_central_transept'], 'y', 0, CT_SPAN, CT_SPRING, CT_Y0+RECESS, CT_Y1, 24.0, nseg=48)
for nm, xc in (('south', -ST_X),) + (() if POST66 else (('north', ST_X),)):
    key = 'SY_south_transept' if nm=='south' else 'SY_north_transept__lost1866'
    vault(nm+'_transept_vault', C[key], 'y', xc, ST_SPAN, NAVE_SPRING, -156+RECESS, 156, 24.0)

# transept walls (clerestory/side screens) and end screens with 24 ft garden recesses
def transept(key, xc, span, spring, y0, y1, recess):
    """r04: garden front = three stacked glazed storeys stepping back 8 ft each (photos 0074/0007; step depths I),
    great arched end screen set at y0+recess (guide p.31 24 ft recesses), side walls only above the adjoining roofs."""
    c = C[key]; w = MB(key+'_walls', c, M['glass_wall']); fr = MB(key+'_frame', c, M['iron_ext']); rr = MB(key+'_front_roofs', c, M['glass_roof'])
    R_ = span/2; yE = y0 + recess
    def lower_at(y):  # height of the roof adjoining the transept side at y
        if y < -156 or y > 156: return 0.0
        h = band_h(y); return NAVE_CROWN if h == 'vault' else h
    for xs in (xc-R_, xc+R_):
        # side walls in strips along Y from yE..y1, bottom = adjoining roof
        ys = sorted(set([yE, y1] + [v for hi, lo, _ in BANDS for v in (hi, lo) if yE < v < y1]))
        for ya, yb in zip(ys[:-1], ys[1:]):
            lo = lower_at((ya+yb)/2)
            if lo < spring - 0.5:
                w.poly([(xs,ya,lo),(xs,yb,lo),(xs,yb,spring),(xs,ya,spring)])
                facade((xs,ya),(xs,yb), lo, spring, bands=[t for t in TIERS if lo < t < spring])
        fr.box(xs-0.5, xs+0.5, yE, y1, spring-3, spring)
    # stepped front storeys in the recess zone y0..yE
    zs_ = [0.0] + list(TIERS)
    for k in range(3):
        yf = y0 + k*(recess/3); z0_, z1_ = 0.0, TIERS[k]
        w.poly([(xc-R_,yf,zs_[k]),(xc+R_,yf,zs_[k]),(xc+R_,yf,z1_),(xc-R_,yf,z1_)])
        facade((xc-R_,yf),(xc+R_,yf), zs_[k], z1_, bands=[z1_-0.01])
        for xs in (xc-R_, xc+R_):
            w.poly([(xs,yf,zs_[k]),(xs,yE,zs_[k]),(xs,yE,z1_),(xs,yf,z1_)])
        # ridge-and-furrow on the step top, ridges running front-to-back (I)
        yb_ = yf + recess/3; x = xc - R_
        while x < xc + R_ - 0.01:
            xm = x + 4
            rr.poly([(x,yf,z1_),(xm,yf,z1_+2),(xm,yb_,z1_+2),(x,yb_,z1_)]); rr.poly([(xm,yf,z1_+2),(x+8,yf,z1_),(x+8,yb_,z1_),(xm,yb_,z1_+2)])
            x += 8
        fr.box(xc-R_, xc+R_, yf-0.6, yf+0.6, z1_-3, z1_)
    # r07: great end screen set back HOOD ft behind a heavy double lattice arch band at yE, so the vault reads as a deep
    #  projecting hood (photo 0074; HOOD/ring depths I). Outer band: chords R and R-5 with radial+diagonal web, 1.6 ft thick.
    HOOD = 8.0; yS = yE + HOOD
    rr.box(xc-R_, xc+R_, yE, yS, TIERS[2]-0.5, TIERS[2]+0.4)                     # lead flat over the hood floor
    w.poly([(xc-R_,yS,TIERS[2]),(xc+R_,yS,TIERS[2]),(xc+R_,yS,spring),(xc-R_,yS,spring)])
    n = 32
    for i in range(n):
        a0 = math.pi*i/n; a1 = math.pi*(i+1)/n
        w.poly([(xc,yS,spring),(xc+R_*math.cos(a0),yS,spring+R_*math.sin(a0)),(xc+R_*math.cos(a1),yS,spring+R_*math.sin(a1))])
    def arcpt(rad, a_, y_): return (xc + rad*math.cos(a_), y_, spring + rad*math.sin(a_))
    for (yy, ro, ri, th) in ((yE, R_, R_-5.0, 1.6), (yE+HOOD/2, R_-0.3, R_-2.0, 0.8), (yS, R_-0.6, R_-3.0, 1.0)):
        for i in range(n):
            a0 = math.pi*i/n; a1 = math.pi*(i+1)/n
            for rad, wd in ((ro, 1.4), (ri, 1.0)):
                fr.strut(arcpt(rad-wd/2, a0, yy), arcpt(rad-wd/2, a1, yy), wd, th)
            fr.strut(arcpt(ro, a0, yy), arcpt(ri, a0, yy), 0.5, th)              # radial web
            fr.strut(arcpt(ro, a0, yy), arcpt(ri, a1, yy), 0.35, th*0.8)          # diagonal web
    # inner arch and concentric ring on the screen (0074 shows a second arch inside the lunette; radius I)
    for i in range(n):
        a0 = math.pi*i/n; a1 = math.pi*(i+1)/n
        fr.strut(arcpt(R_*0.62, a0, yS-0.3), arcpt(R_*0.62, a1, yS-0.3), 1.0, 0.8)
    for xx in [xc-R_ + k*8 for k in range(int(span/8)+1)]:
        fr.box(xx-0.3, xx+0.3, yS-0.5, yS+0.3, TIERS[2], spring + math.sqrt(max(R_*R_-(xx-xc)**2, 0)))
    for t in [spring, spring - (spring-TIERS[2])/2, spring + R_*0.35]:
        hw = R_ if t <= spring else math.sqrt(max(R_*R_-(t-spring)**2, 0))
        fr.box(xc-hw, xc+hw, yS-0.7, yS+0.3, t-1.6, t)
    for xs in (xc-R_, xc+R_):                                                    # hood side cheeks: stanchions to spring
        fr.box(xs-1.0, xs+1.0, yE-0.8, yS+0.8, TIERS[2], spring)
    # west end screen full height
    w.poly([(xc-R_,y1,0),(xc+R_,y1,0),(xc+R_,y1,spring),(xc-R_,y1,spring)])
    facade((xc-R_,y1),(xc+R_,y1), 0, spring, bands=list(TIERS))
    for i in range(n):
        a0 = math.pi*i/n; a1 = math.pi*(i+1)/n
        w.poly([(xc,y1,spring),(xc+R_*math.cos(a0),y1,spring+R_*math.sin(a0)),(xc+R_*math.cos(a1),y1,spring+R_*math.sin(a1))])
    w.done(); fr.done(); rr.done()
transept('SY_central_transept', 0, CT_SPAN, CT_SPRING, CT_Y0, CT_Y1, RECESS)
transept('SY_south_transept', -ST_X, ST_SPAN, NAVE_SPRING, -156, 156, RECESS)
if not POST66: transept('SY_north_transept__lost1866', ST_X, ST_SPAN, NAVE_SPRING, -156, 156, RECESS)
# central transept floor projections beyond general walls
ctf = MB('central_transept_projection_floor', C['SY_central_transept'], M['floor'])
ctf.box(-CT_SPAN/2, CT_SPAN/2, CT_Y0, -156, -1, 0); ctf.box(-CT_SPAN/2, CT_SPAN/2, 156, CT_Y1, -1, 0); ctf.done()

# ---------- low square towers at nave/transept junctions (guide p.33; size/height I) ----------
tw = MB('crossing_towers', C['SY_crossing_towers'], M['iron']); twg = MB('crossing_towers_glass', C['SY_crossing_towers'], M['glass_wall'])
for xc, sp in TSPANS:
    for sx in (-1, 1):
        for sy in (-1, 1):
            x0 = xc + sx*sp/2; x1 = x0 + sx*BAY; y0 = sy*36; y1 = y0 + sy*BAY
            top = NAVE_SPRING + 12
            for (xx, yy) in ((x0,y0),(x1,y0),(x0,y1),(x1,y1)):
                tw.box(xx-0.8, xx+0.8, yy-0.8, yy+0.8, TIERS[2], top)
            tw.box(min(x0,x1), max(x0,x1), min(y0,y1), max(y0,y1), top-1.5, top)
            for yy in (y0, y1):
                twg.poly([(x0,yy,TIERS[2]),(x1,yy,TIERS[2]),(x1,yy,top),(x0,yy,top)])
            for xx in (x0, x1):
                twg.poly([(xx,y0,TIERS[2]),(xx,y1,TIERS[2]),(xx,y1,top),(xx,y0,top)])
# r07: diagonal X-bracing (section 0212 shows braced stacks flanking the vault; photo 0074 braced tower faces; member sizes I)
def xbrace(mb, p0, p1, z0, z1, w=0.45):
    (xa, ya), (xb, yb) = p0, p1
    mb.strut((xa, ya, z0), (xb, yb, z1), w, w); mb.strut((xb, yb, z0), (xa, ya, z1), w, w)
for xc, sp in TSPANS:
    for sx in (-1, 1):
        for sy in (-1, 1):
            x0 = xc + sx*sp/2; x1 = x0 + sx*BAY; y0 = sy*36; y1 = y0 + sy*BAY
            levels = [0.0] + list(TIERS) + [NAVE_SPRING + 12]
            for za, zb in zip(levels[:-1], levels[1:]):
                for (pa, pb) in (((x0,y0),(x1,y0)), ((x0,y1),(x1,y1)), ((x0,y0),(x0,y1)), ((x1,y0),(x1,y1))):
                    xbrace(tw, pa, pb, za+0.5, zb-3)
# transverse braced frames in the 36-60 ft tower stacks every 72 ft (k%3==0, with the paired nave columns; spacing I).
# Own object so it can be hidden for walkthrough shots (braces cross the side aisles/galleries at those frames).
tb = MB('transverse_bracing_72ft', C['SY_main_frame'], M['iron'])
for x in xs_grid:
    k_ = round((x+HALF)/BAY)
    if k_ % 3 or in_span(x, [(c_, w_+0.2) for c_, w_ in TSPANS]): continue
    for sy in (-1, 1):
        levels = [0.0] + list(TIERS)
        for za, zb in zip(levels[:-1], levels[1:]):
            xbrace(tb, (x, sy*36), (x, sy*60), za+0.5, zb-3, 0.35)
tb.done(); tw.done(); twg.done()

# ---------- basement storey along the garden front (guide p.34: lower storey + Paxton's tunnel 24 ft) ----------
BD = BASEMENT_DEPTH
bs = MB('basement_brick', C['SY_basement_garden_front'], M['brick'])
# r04: front = brick piers + round-arched glazed openings each 24 ft bay (arch form I; photos show glazed basement storey)
bs.box(-HALF, HALF, -108, -84, -BD, -BD+1)        # tunnel floor (24 ft wide)
bs.box(-HALF, HALF, -84, -83, -BD, 0)             # tunnel inner wall
bs.box(-HALF-1, -HALF, -157, -83, -BD, 0); bs.box(HALF, HALF+1, -157, -83, -BD, 0)
bs.box(-CT_SPAN/2-2, CT_SPAN/2+2, CT_Y0, -156, -BD, -1)  # central projection basement mass (I)
bw = MB('basement_windows', C['SY_basement_garden_front'], M['glass_wall'])
def arcade(xa, xb, y, z0, z1):
    x = xa
    while x < xb - 0.01:
        x2 = min(x + BAY, xb); pw = 1.5
        bs.box(x-pw, x+pw, y-1.2, y+0.2, z0, z1)                       # pier
        l, r = x + pw, x2 - pw; rad = (r - l)/2; cxa = (l + r)/2; spr = z1 - 2.0 - rad
        if rad > 2 and spr > z0 + 4:
            arc = [(cxa + rad*math.cos(math.pi - math.pi*i/12), spr + rad*math.sin(math.pi - math.pi*i/12)) for i in range(13)]
            bw.poly([(l,y,z0+1.5),(r,y,z0+1.5)] + [(px,y,pz) for px,pz in reversed(arc)])
            bs.poly([(l,y-0.6,z1),(l,y-0.6,spr)] + [(px,y-0.6,pz) for px,pz in arc] + [(r,y-0.6,spr),(r,y-0.6,z1)])
            bs.box(l, r, y-0.8, y+0.2, z0, z0+1.5)
        x = x2
    bs.box(xa-1.5, xb+1.5, y-1.4, y+0.2, z1-1.5, z1)                   # string course
for xa_, xb_ in ((-HALF, -CT_SPAN/2), (CT_SPAN/2, HALF)):
    arcade(xa_, xb_, -157.0, -BD, 0)
arcade(-CT_SPAN/2, CT_SPAN/2, CT_Y0, -BD, 0)
# garden stairs from the upper terrace to the main floor at each transept front (I: positions; 0007 shows central flight)
stt = MB('garden_stairs_to_main_floor', C['SY_basement_garden_front'], M['stone'])
for xc_, wdt, yf in ((0, 72, CT_Y0), (-ST_X, 48, -157)) + (() if POST66 else ((ST_X, 48, -157),)):   # POST66: no transept door to serve (I)
    nst = 32; rise = BD/nst
    for i in range(nst):
        stt.box(xc_-wdt/2, xc_+wdt/2, yf-(nst-i)*1.25, yf-(nst-i-1)*1.25, -BD, -BD + (i+1)*rise)
    for sx in (-1, 1):
        stt.box(xc_+sx*wdt/2-1.2, xc_+sx*wdt/2+1.2, yf-nst*1.25, yf, -BD, 3)
bw.done(); stt.done(); bs.done()

# ---------- wings (574 ft, toward the garden at both ends) ----------
WING_LEN_POST66 = 240.0   # U: 'part of a low narrow wing' survived / partly rebuilt; 10 bays kept, length not evidenced
wg = MB('wings_glass', C['SY_wings'], M['glass_wall']); wf = MB('wings_frame', C['SY_wings'], M['iron_ext']); wr = MB('wings_roof', C['SY_wings'], M['glass_roof'])
for sx in (-1, 1):
    xc = sx*WING_CX; xa, xb = xc-WING_W/2, xc+WING_W/2
    ya, yb = WING_Y0 - (WING_LEN_POST66 if (POST66 and sx > 0) else WING_LEN), WING_Y0
    top = TIERS[1]   # I: wing roof level with 2nd tier of main building; base steps down with slope (U)
    zb = -BD - 10    # I: wing lower storey below basement level (guide p.29-30: 3 storeys in South Wing)
    for (p0, p1) in (((xa,ya),(xa,yb)), ((xb,ya),(xb,yb)), ((xa,ya),(xb,ya))):
        wg.poly([(p0[0],p0[1],zb),(p1[0],p1[1],zb),(p1[0],p1[1],top),(p0[0],p0[1],top)])
        facade(p0, p1, zb, top, bands=[zb+18, 0, TIERS[0]])
    y = ya
    while y <= yb + 0.01:
        for xx in (xa, xb): wf.box(xx-0.4, xx+0.4, y-0.4, y+0.4, zb, top)
        y += BAY
    for t in (zb+18, 0, TIERS[0], top):
        for xx in (xa, xb): wf.box(xx-0.4, xx+0.4, ya, yb, t-2, t)
    # connecting block between end wall and wing
    wf.box(min(sx*HALF, xa if sx>0 else xb), max(sx*HALF, xa if sx>0 else xb), -156, WING_Y0, -1, 0)
    wg.poly([(sx*HALF, -156, 0), (xc, -156, 0), (xc, -156, top), (sx*HALF, -156, top)])
    # arched roof on wing (I)
    n = 12; R = WING_W/2
    for i in range(n):
        a0 = math.pi*i/n; a1 = math.pi*(i+1)/n
        wr.poly([(xc+R*math.cos(a0), ya, top+R*0.5*math.sin(a0)), (xc+R*math.cos(a0), WING_Y0+60, top+R*0.5*math.sin(a0)),
                 (xc+R*math.cos(a1), WING_Y0+60, top+R*0.5*math.sin(a1)), (xc+R*math.cos(a1), ya, top+R*0.5*math.sin(a1))])
    wf.box(xa, xb, ya, yb, zb-1, zb)
wg.done(); wf.done(); wr.done()

# ---------- railway colonnade (from south wing toward the station; route U) ----------
cg = MB('colonnade_roof', C['SY54_railway_colonnade'], M['glass_roof']); cf = MB('colonnade_frame', C['SY54_railway_colonnade'], M['iron'])
cx = -WING_CX - WING_W/2 - 12; cy0 = WING_Y0 - WING_LEN + 60
zc = -BD - 10
y = cy0
while y > cy0 - COLONNADE_LEN:
    for xx in (cx-12, cx+12): cf.box(xx-0.4, xx+0.4, y-0.4, y+0.4, zc, zc+20)
    y -= BAY
cf.box(cx-12, cx+12, cy0-COLONNADE_LEN, cy0, zc+19, zc+20)
cg.poly([(cx-12, cy0-COLONNADE_LEN, zc+20), (cx-12, cy0, zc+20), (cx, cy0, zc+26), (cx, cy0-COLONNADE_LEN, zc+26)])
cg.poly([(cx, cy0-COLONNADE_LEN, zc+26), (cx, cy0, zc+26), (cx+12, cy0, zc+20), (cx+12, cy0-COLONNADE_LEN, zc+20)])
cg.done(); cf.done()

# ---------- Brunel water towers (dated 1856; positions U) ----------
# r07: octagonal, tiered, tapering shaft with storey bands and paired windows per face, projecting gallery under the
# tank storey, tank storey, octagonal pyramid roof and an OPEN lantern (posts + cap + finial), after photo 0074 (distant
# tower) and the brief. Side count 8 per brief (photo 0074 reads many-sided: I); storey height 18 ft, radii, tank and
# lantern sizes I; overall height TOWER_H U.
for nm, sx in (('south', -1), ('north', 1)):
    o = MB('water_tower_'+nm, C['SY56_water_towers__dated'], M['iron_ext']); g = MB('water_tower_glass_'+nm, C['SY56_water_towers__dated'], M['glass_wall'])
    bk = MB('water_tower_base_'+nm, C['SY56_water_towers__dated'], M['brick'])
    xc = sx*(HALF+120); yc = 60; H = TOWER_H; sides = 8
    def ring(r, z, rot=math.pi/8): return [(xc + r*math.cos(rot+2*math.pi*k/sides), yc + r*math.sin(rot+2*math.pi*k/sides), z) for k in range(sides)]
    def prism(mb, r0, z0, r1, z1, cap=False):
        a_, b_ = ring(r0, z0), ring(r1, z1)
        for k in range(sides):
            k1 = (k+1) % sides; mb.poly([a_[k], a_[k1], b_[k1], b_[k]])
        if cap: mb.poly(list(reversed(a_))); mb.poly(b_)
    zg = 0.0; ZT = H - 62; R0, R1 = 24.0, 19.0
    rad = lambda z: R0 + (R1-R0)*(z-zg)/(ZT-zg)
    prism(bk, R0+3, zg-12, R0+3, zg+8, cap=True)                                   # brick base (I)
    prism(g, R0, zg+8, R1, ZT)                                                      # glazed/infill skin
    st = 18.0; z = zg + 8
    while z < ZT - 0.1:
        z2 = min(z + st, ZT); r_a, r_b = rad(z), rad(z2)
        prism(o, r_a+0.6, z, r_a+0.6, z+1.6, cap=False)                             # storey band
        A, B = ring(r_a+0.3, z), ring(r_b+0.3, z2)
        for k in range(sides):
            k1 = (k+1) % sides
            o.strut(A[k], B[k], 1.4, 1.4)                                           # angle posts
            for tt in (0.33, 0.67):                                                 # paired windows: mullions
                pa = tuple(A[k][i] + (A[k1][i]-A[k][i])*tt for i in range(2)) + (z,)
                pb = tuple(B[k][i] + (B[k1][i]-B[k][i])*tt for i in range(2)) + (z2,)
                o.strut(pa, pb, 0.6, 0.6)
        z = z2
    prism(o, R1+4.5, ZT-1.5, R1+4.5, ZT, cap=True)                                  # projecting gallery floor
    GR = ring(R1+4.3, ZT)
    for k in range(sides):                                                          # gallery rail + brackets
        k1 = (k+1) % sides
        o.strut((GR[k][0], GR[k][1], ZT+3.5), (GR[k1][0], GR[k1][1], ZT+3.5), 0.4, 0.4)
        for tt in (0.0, 0.25, 0.5, 0.75):
            px_, py_ = GR[k][0] + (GR[k1][0]-GR[k][0])*tt, GR[k][1] + (GR[k1][1]-GR[k][1])*tt
            o.strut((px_, py_, ZT), (px_, py_, ZT+3.5), 0.25, 0.25)
        o.strut(ring(R1, ZT-8)[k], GR[k], 0.8, 0.8)
    prism(g, R1+1.5, ZT, R1+1.5, ZT+22)                                             # tank storey (glazed screen; I)
    TS = ring(R1+1.8, ZT)
    for k in range(sides):
        o.strut(TS[k], (TS[k][0], TS[k][1], ZT+22), 1.2, 1.2)
    prism(o, R1+3.5, ZT+22, R1+3.5, ZT+24.5, cap=True)                              # cornice
    zr0, zr1 = ZT+24.5, H-16                                                        # octagonal pyramid roof
    a_, b_ = ring(R1+3.0, zr0), ring(5.0, zr1)
    for k in range(sides):
        k1 = (k+1) % sides; o.poly([a_[k], a_[k1], b_[k1], b_[k]])
        o.strut(a_[k], b_[k], 0.7, 0.7)                                             # hip ribs
    o.poly(b_)
    LP = ring(4.2, zr1)                                                             # open lantern: posts, no glazing
    for k in range(sides):
        o.strut(LP[k], (LP[k][0], LP[k][1], H-8), 0.45, 0.45)
    prism(o, 5.2, H-8, 5.2, H-7, cap=True)
    c_ = ring(5.2, H-7); tip = (xc, yc, H-2.5)
    for k in range(sides):
        o.poly([c_[k], c_[(k+1) % sides], tip])
    o.cyl(xc, yc, H-2.5, H, 0.35, 0.1, seg=8)                                      # finial
    o.done(); g.done(); bk.done()

# ---------- terraces and terrain (r04) ----------
T = MB('terrain', C['SY_terraces_terrain'], M['grass']); S = MB('terraces_stone', C['SY_terraces_terrain'], M['stone']); G = MB('terrace_gravel', C['SY_terraces_terrain'], M['gravel'])
UT = -BD; LT = UT - LOWER_TERRACE_DROP
yU = -157 - UPPER_TERRACE_D; yL = yU - LOWER_TERRACE_D
TX = HALF - 20
def mdx(dx): return (dx - 541) * MAP_FT_PER_DPX            # 1857 map 0591 (display px) -> model ft (R)
def mdy(dy): return -100 - (dy - 265) * MAP_FT_PER_DPX
# park profile (y, z): U levels; platforms for H and the M basins read from the map layout
PROF = [(yL, LT-1), (-1000, LT-40), (-1200, LT-44), (-1700, LT-105), (-2350, LT-110), (-3200, LT-140)]
def zs(y):
    if y >= PROF[0][0]: return PROF[0][1]
    for (ya, za), (yb, zb) in zip(PROF[:-1], PROF[1:]):
        if yb <= y <= ya: return za + (zb-za)*(ya-y)/(ya-yb)
    return PROF[-1][1]
G.box(-TX, TX, yU, -157, UT-2, UT)                              # upper terrace (gravel)
# r07: grass bank between the terraces instead of r04-r06's vertical retaining wall (photos 0074/0007 read sloping turf;
# bank run BANK ft I). Stone kerb at the top under the balustrade; bank interrupted by the central flight (|x|<50).
BANK = 40.0
S.box(-TX, TX, yU-2.5, yU, UT-3, UT)
for xa_, xb_ in ((-TX, -50), (50, TX)):
    T.poly([(xa_, yU-BANK, LT+0.05), (xb_, yU-BANK, LT+0.05), (xb_, yU-2.5, UT-0.6), (xa_, yU-2.5, UT-0.6)])
    for xe_ in (xa_, xb_):
        S.poly([(xe_, yU-BANK, LT), (xe_, yU-2.5, LT), (xe_, yU-2.5, UT-0.6)])
def balustrade(xa, xb, y, z, statues_every=None, gap=None):
    """plinth 0.8, balusters 0.55 wide @1.4 ft, coping 0.6 -> 3.3 ft high (I: typical Italianate terrace scale)"""
    if not gap: segs = [(xa, xb)]
    else:   # r11: gap may be one (a, b) or a list of them
        gl = sorted(gap if isinstance(gap[0], (tuple, list)) else [gap]); segs = []; xc0 = xa
        for g0, g1 in gl: segs.append((xc0, g0)); xc0 = g1
        segs.append((xc0, xb))
    for a_, b_ in segs:
        S.box(a_, b_, y-1.0, y+1.0, z, z+0.8); S.box(a_, b_, y-1.1, y+1.1, z+2.7, z+3.3)
        x = a_ + 0.7
        while x < b_ - 0.5:
            S.box(x-0.27, x+0.27, y-0.35, y+0.35, z+0.8, z+2.7); x += 1.4
        if statues_every:
            x = a_ + 12
            while x < b_ - 6:
                statue(x, y, z+3.3, S); x += statues_every
def statue(x, y, z, mb, scale=1.0):
    """placeholder statue: pedestal 3.5x3.5x5 ft + 7 ft figure (life-and-a-bit; I). PLACEHOLDER"""
    mb.box(x-1.75, x+1.75, y-1.75, y+1.75, z, z+5*scale)
    mb.box(x-0.8, x+0.8, y-0.6, y+0.6, z+5*scale, z+(5+4.6)*scale)            # draped body
    mb.box(x-1.1, x+1.1, y-0.5, y+0.5, z+(5+4.0)*scale, z+(5+5.6)*scale)      # shoulders
    mb.box(x-0.45, x+0.45, y-0.45, y+0.45, z+(5+5.6)*scale, z+(5+6.6)*scale)  # head
balustrade(-TX, TX, yU-1.5, UT, statues_every=96, gap=[(-48, 48), (-ST_X-18, -ST_X+18), (ST_X-18, ST_X+18)])   # r11: side flights (sphinx steps)
G.box(-TX, TX, yL, yU-BANK, LT-2, LT)                           # lower terrace
balustrade(-TX, TX, yL+1, LT, statues_every=144, gap=(-30, 30))
RUN = (BANK-2.5)/10
for i in range(10):                                              # grand central flight upper->lower terrace
    S.box(-48, 48, yU-2.5-(i+1)*RUN, yU-2.5-i*RUN, LT, UT - i*(LOWER_TERRACE_DROP/10) + 0.01)
# r07: stepped cheek walls with moulded coping and terminal pedestals + urns (r06 miss: plain cheeks; forms I)
def cheek(xc_, ytop, ybot, ztop, zbot, nst):
    for i in range(nst):
        y0_, y1_ = ytop - (i+1)*(ytop-ybot)/nst, ytop - i*(ytop-ybot)/nst; zt = ztop - i*(ztop-zbot)/nst
        S.box(xc_-1.5, xc_+1.5, y0_, y1_, zbot, zt+3.0); S.box(xc_-1.9, xc_+1.9, y0_, y1_, zt+3.0, zt+3.6)
    for yy_, zz_ in ((ytop, ztop), (ybot, zbot)):
        S.box(xc_-2.4, xc_+2.4, yy_-2.4, yy_+2.4, zz_, zz_+4.2); S.box(xc_-2.8, xc_+2.8, yy_-2.8, yy_+2.8, zz_+4.2, zz_+4.8)
        S.cyl(xc_, yy_, zz_+4.8, zz_+5.6, 0.9, 1.4, seg=12); S.cyl(xc_, yy_, zz_+5.6, zz_+7.6, 1.9, 1.5, seg=12); S.cyl(xc_, yy_, zz_+7.6, zz_+8.2, 0.5, 0.2, seg=8)
for sx in (-1, 1): cheek(sx*49.5, yU, yU-BANK, UT, LT, 10)
for i in range(14):                                              # central flight lower terrace -> park (I)
    S.box(-30, 30, yL-(i+1)*2.6, yL-i*2.6, zs(yL-i*2.6)-3, LT - i*(LT-zs(yL-40))/14)
for sx in (-1, 1): cheek(sx*31.5, yL, yL-14*2.6, LT, zs(yL-14*2.6), 14)
# parterres on the lower terrace: 6 beds with S fountains (map 0591 S, R)
YP0, YP1 = yL+22, yU-BANK-18; YPC = (YP0+YP1)/2     # r07: parterre panels (beds/paths added in the park-paths block)
for xs_ in (-720, -515, -231, 231, 515, 720):
    T.box(xs_-85, xs_+85, YP0, YP1, LT, LT+0.25)
T.box(-1100, 1100, 156, 700, -3, -0.5)
# r07: ground under the palace slopes from the Parade (just below the floor) to the garden basement level, as drawn in
# section 0212 (linear profile I). Built as a prism split on the 24 ft grid so a section slice shows a filled cut face.
# garden side y<-84 (Paxton's tunnel + basement storey, guide p.34) held at full basement depth (I).
def gz(y): return -BD if y <= -84 else -1.5 + (-BD + 1.5) * (156 - y) / (156 + 84)
GP = [(156, gz(156)), (36, gz(36)), (-36, gz(-36)), (-84, -BD), (-157, -BD), (-157, -BD-12), (156, -BD-12)]
gb = bmesh.new(); xs_cut = [-1100] + [x for x in xs_grid] + [1100]
for xa_, xb_ in zip(xs_cut[:-1], xs_cut[1:]):
    A_ = [gb.verts.new((f(xa_), f(y_), f(z_))) for y_, z_ in GP]; B_ = [gb.verts.new((f(xb_), f(y_), f(z_))) for y_, z_ in GP]
    gb.faces.new(A_); gb.faces.new(list(reversed(B_)))
    for k_ in range(len(GP)):
        k1_ = (k_+1) % len(GP); gb.faces.new((A_[k_], B_[k_], B_[k1_], A_[k1_]))
gme = bpy.data.meshes.new('ground_under_palace'); gb.to_mesh(gme); gme.materials.append(M['grass'])
C['SY_terraces_terrain'].objects.link(bpy.data.objects.new('ground_under_palace', gme))
# basement piers under every column line where the ground falls away (section 0212 piers + 'A' basement; sizes I)
bp = MB('basement_piers', C['SY_basement_garden_front'], M['brick'])
for x in xs_grid:
    for y in COL_Y:
        zg_ = gz(y)
        if zg_ < -2.5 and abs(y) < 156.5: bp.box(x-1.0, x+1.0, y-1.0, y+1.0, zg_, -1.0)
bp.done()
T.box(-1100, -TX, yL, -157, LT-1, LT); T.box(TX, 1100, yL, -157, LT-1, LT)
bm = bmesh.new(); vv = []
for y, z in PROF:
    vv.append((bm.verts.new((f(-1600), f(y), f(z))), bm.verts.new((f(1600), f(y), f(z)))))
for (a0, a1), (b0, b1) in zip(vv[:-1], vv[1:]): bm.faces.new((a0, a1, b1, b0))
me = bpy.data.meshes.new('park_slope'); bm.to_mesh(me); me.materials.append(M['grass'])
o = bpy.data.objects.new('park_slope', me); C['SY_terraces_terrain'].objects.link(o)
for (ya, za), (yb, zb) in zip(PROF[:-1], PROF[1:]):
    bmw = bmesh.new(); q = [bmw.verts.new((f(x_), f(y_), f(z_+0.3))) for x_, y_, z_ in ((-40, ya, za), (40, ya, za), (40, yb, zb), (-40, yb, zb))]
    bmw.faces.new(q); mw = bpy.data.meshes.new('central_walk'); bmw.to_mesh(mw); mw.materials.append(M['gravel'])
    ow = bpy.data.objects.new('central_walk', mw); C['SY_terraces_terrain'].objects.link(ow)
T.done(); S.done(); G.done()
T2 = MB('distant_ground', C['SY_terraces_terrain'], M['grass']); T2.box(-60000, 60000, -90000, 60000, LT-142, LT-141); T2.done()

# ---------- terrace fountains (S) : SY56_fountains_basins__dated ----------
fo = MB('terrace_basins', C['SY56_fountains_basins__dated'], M['stone']); fw = MB('terrace_basin_water', C['SY56_fountains_basins__dated'], M['water'])
def basin(mbs, mbw, xc, yc, z, r, n=40, rim=1.2, h=2.2, jet=None, shape=None):
    ring = shape if shape else [(xc + r*math.cos(2*math.pi*k/n), yc + r*math.sin(2*math.pi*k/n)) for k in range(n)]
    for k in range(len(ring)):
        a_, b_ = ring[k], ring[(k+1) % len(ring)]
        L = math.hypot(b_[0]-a_[0], b_[1]-a_[1]); ang = math.atan2(b_[1]-a_[1], b_[0]-a_[0])
        bmr = mbs.bm; rr_ = bmesh.ops.create_cube(bmr, size=1.0)
        mtx = Matrix.Translation(Vector((f((a_[0]+b_[0])/2), f((a_[1]+b_[1])/2), f(z+h/2)))) @ Matrix.Rotation(ang, 4, 'Z') @ Matrix.Diagonal((f(L+rim), f(rim), f(h), 1))
        bmesh.ops.transform(bmr, matrix=mtx, verts=rr_['verts'])
    mbw.poly([(p_[0], p_[1], z+h-0.6) for p_ in ring])
    if jet:  # central pedestal/jet placeholder (water jets not simulated)
        mbs.box(xc-jet*0.15, xc+jet*0.15, yc-jet*0.15, yc+jet*0.15, z, z+jet*0.3)
def ring_wall(mbs, ring, z0, z1, wd):
    for k in range(len(ring)):
        a_, b_ = ring[k], ring[(k+1) % len(ring)]
        L = math.hypot(b_[0]-a_[0], b_[1]-a_[1]); ang = math.atan2(b_[1]-a_[1], b_[0]-a_[0])
        rr_ = bmesh.ops.create_cube(mbs.bm, size=1.0)
        mtx = Matrix.Translation(Vector((f((a_[0]+b_[0])/2), f((a_[1]+b_[1])/2), f((z0+z1)/2)))) @ Matrix.Rotation(ang, 4, 'Z') @ Matrix.Diagonal((f(L+wd*0.6), f(wd), f(z1-z0), 1))
        bmesh.ops.transform(mbs.bm, matrix=mtx, verts=rr_['verts'])
JETS = MB('fountain_jets', C['SY56_fountains_basins__dated'], M['jet'])
def ornate_basin(mbs, mbw, xc, yc, z, r, jet_h=30, lobes=8, shape=None, urns=True):
    """r07: lobed outline, stepped kerb, moulded rim + coping + bead, central two-tier fountain with jet and rim jets,
    urns on pedestals on the kerb. All ornament forms I (period photos too distant); outline lobing I."""
    def outline(dr):
        if shape:
            return [(xc + (px_-xc)*(1+dr/max(r, 1)), yc + (py_-yc)*(1+dr/max(r, 1))) for px_, py_ in shape]
        return [(xc + (r+dr)*(1+0.06*math.cos(lobes*t))*math.cos(t), yc + (r+dr)*(1+0.06*math.cos(lobes*t))*math.sin(t))
                for t in [2*math.pi*k/96 for k in range(96)]]
    ring_wall(mbs, outline(5.0), z, z+0.7, 4.0)           # outer step
    ring_wall(mbs, outline(2.5), z, z+1.3, 2.0)           # second step
    ring_wall(mbs, outline(0), z, z+2.4, 1.8)             # rim wall
    ring_wall(mbs, outline(0), z+2.4, z+2.9, 2.8)         # coping
    ring_wall(mbs, outline(0), z+2.9, z+3.2, 1.6)         # bead
    mbw.poly([(p_[0], p_[1], z+1.8) for p_ in outline(-0.8)])
    s_ = max(0.45, min(r/45.0, 1.4))
    mbs.cyl(xc, yc, z, z+4*s_, 5*s_, 4.2*s_, seg=8)                          # pedestal
    mbs.cyl(xc, yc, z+4*s_, z+6.5*s_, 3*s_, 11*s_, seg=24)                    # lower bowl
    mbs.cyl(xc, yc, z+6.5*s_, z+7.1*s_, 11.6*s_, 11.6*s_, seg=24)             # bowl lip
    mbs.cyl(xc, yc, z+7.1*s_, z+13*s_, 1.6*s_, 1.2*s_, seg=12)                # shaft
    mbs.cyl(xc, yc, z+10*s_, z+11*s_, 2.4*s_, 2.4*s_, seg=12)                 # knop
    mbs.cyl(xc, yc, z+13*s_, z+15*s_, 1.5*s_, 5.5*s_, seg=16)                 # upper bowl
    mbs.cyl(xc, yc, z+15*s_, z+18*s_, 0.8*s_, 0.3*s_, seg=8)                  # finial
    JETS.cyl(xc, yc, z+18*s_, z+18*s_+jet_h, 2.2*s_, 0.4, seg=12)             # main jet (spray column, I)
    for k in range(8):                                                        # rim jets arching inward (as straight cones)
        t = 2*math.pi*k/8 + math.pi/8; px_, py_ = xc + (r-3)*math.cos(t), yc + (r-3)*math.sin(t)
        JETS.cyl(px_, py_, z+2.9, z+2.9+min(8, jet_h*0.2), 0.9, 0.15, seg=8)
    if urns:
        for k in range(4):
            t = math.pi/2*k; px_, py_ = xc + (r+6.5)*math.cos(t), yc + (r+6.5)*math.sin(t)
            mbs.box(px_-1.8, px_+1.8, py_-1.8, py_+1.8, z, z+3.8); mbs.box(px_-2.1, px_+2.1, py_-2.1, py_+2.1, z+3.8, z+4.3)
            mbs.cyl(px_, py_, z+4.3, z+5.1, 0.8, 1.3, seg=12); mbs.cyl(px_, py_, z+5.1, z+7.0, 1.8, 1.4, seg=12)
for xs_ in (-720, -515, -231, 231, 515, 720):
    ornate_basin(fo, fw, xs_, YPC, LT, 45, jet_h=26)   # r05: map S ~25 dpx dia ≈ 107 ft (R); r07 ornate (forms I)
fo.done(); fw.done()

# ---------- park fountains & cascades (map 0591: R, H, J, L, M) : SY56_park_fountains_cascades__dated ----------
PF = C['SY56_park_fountains_cascades__dated']
po = MB('park_basins_stone', PF, M['stone']); pw = MB('park_basins_water', PF, M['water'])
for dx in (447, 632):                                            # R fountains
    x_, y_ = mdx(dx), mdy(445); po.box(x_-30, x_+30, y_-30, y_+30, zs(y_)-2, zs(y_)); ornate_basin(po, pw, x_, y_, zs(y_), 20, jet_h=25)
yH = mdy(500); zH = zs(yH)                                       # H large circular fountain (map ~36 dpx dia ≈ 154 ft; R)
po.box(-100, 100, yH-100, yH+100, zH-3, zH); ornate_basin(po, pw, 0, yH, zH, 77, jet_h=60, lobes=12)
yM = mdy(700); zM = zs(yM)
def super_ellipse(xc, yc, a, b, e=4, n=72):
    return [(xc + a*math.copysign(abs(math.cos(t))**(2/e), math.cos(t)), yc + b*math.copysign(abs(math.sin(t))**(2/e), math.sin(t))) for t in [2*math.pi*k/n for k in range(n)]]
for dx in (420, 662):                                            # M great basins (~190x110 dpx ≈ 800x470 ft; shape simplified, R/I)
    x_ = mdx(dx); shp = super_ellipse(x_, yM, 380, 210)
    po.box(x_-400, x_+400, yM-230, yM+230, zM-4, zM); basin(po, pw, x_, yM, zM, 0, rim=3, h=3.5, shape=shp)
for dx in (500, 582):                                            # L cascades: stepped channels from J temples down to M (I: steps)
    x_ = mdx(dx); ya_, yb_ = mdy(560), mdy(690); nstep = 16
    for i in range(nstep):
        y0_ = ya_ + (yb_-ya_)*i/nstep; y1_ = ya_ + (yb_-ya_)*(i+1)/nstep; z_ = zs((y0_+y1_)/2)
        po.box(x_-14, x_+14, y1_, y0_, z_-1, z_+1.5); pw.poly([(x_-11, y1_, z_+1.2), (x_+11, y1_, z_+1.2), (x_+11, y0_, z_+1.2), (x_-11, y0_, z_+1.2)])
    yJ = mdy(560); zJ = zs(yJ)                                    # J temples (placeholder pavilions)
    po.box(x_-20, x_+20, yJ-6, yJ+34, zJ, zJ+4)
    for cx_ in (-16, 16):
        for cy_ in (-2, 30): po.box(x_+cx_-1.2, x_+cx_+1.2, yJ+cy_-1.2, yJ+cy_+1.2, zJ+4, zJ+30)
    po.box(x_-20, x_+20, yJ-6, yJ+34, zJ+30, zJ+36)
po.done(); pw.done(); JETS.done()

# ---------- r07: park paths and flower beds digitised from the 1857 map 0591 (display px -> ft via mdx/mdy; R for
# alignment of the main walks/rings, I for widths, curvature between control points and bed shapes) ----------
PB = coll('SY56_park_paths_beds__dated')
PG = MB('park_paths_gravel', PB, M['gravel']); FB = MB('flower_beds', PB, M['flowers']); GPN = MB('parterre_grass', PB, M['grass'])
def gzp(x, y):  # ground height at a park/terrace point
    if y > -157: return UT
    if y > yU - 2.5: return UT
    if y > yU - BANK: return LT + (UT-LT)*(y-(yU-BANK))/(BANK-2.5)
    if y > yL: return LT
    return zs(y)
def catmull(pts, step=12.0):
    out = []
    P_ = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P_)-2):
        p0, p1, p2, p3 = P_[i-1], P_[i], P_[i+1], P_[i+2]
        n_ = max(2, int(math.hypot(p2[0]-p1[0], p2[1]-p1[1]) / step))
        for j in range(n_):
            t = j/n_; t2, t3 = t*t, t*t*t
            out.append(tuple(0.5*((2*p1[c]) + (-p0[c]+p2[c])*t + (2*p0[c]-5*p1[c]+4*p2[c]-p3[c])*t2 + (-p0[c]+3*p1[c]-3*p2[c]+p3[c])*t3) for c in range(2)))
    out.append(pts[-1]); return out
def ribbon(mb, pts, w, dz=0.35, closed=False):
    if closed: pts = pts + [pts[0]]
    for (xa_, ya_), (xb_, yb_) in zip(pts[:-1], pts[1:]):
        L = math.hypot(xb_-xa_, yb_-ya_)
        if L < 0.1: continue
        nx_, ny_ = -(yb_-ya_)/L*w/2, (xb_-xa_)/L*w/2
        mb.poly([(xa_-nx_, ya_-ny_, gzp(xa_, ya_)+dz), (xb_-nx_, yb_-ny_, gzp(xb_, yb_)+dz), (xb_+nx_, yb_+ny_, gzp(xb_, yb_)+dz), (xa_+nx_, ya_+ny_, gzp(xa_, ya_)+dz)])
def circle_pts(cx, cy, r, n=64): return [(cx + r*math.cos(2*math.pi*k/n), cy + r*math.sin(2*math.pi*k/n)) for k in range(n)]
def sector(mb, cx, cy, r0, r1, a0, a1, twist=0.0, dz=0.45, nr=5, na=8):
    """annular sector bed draped on the ground; twist = extra rotation (rad) at r1 (whirling rosette beds, map I)"""
    for i in range(nr):
        for j in range(na):
            q = []
            for (ii, jj) in ((i, j), (i, j+1), (i+1, j+1), (i+1, j)):
                rr_ = r0 + (r1-r0)*ii/nr; aa = a0 + (a1-a0)*jj/na + twist*ii/nr
                x_, y_ = cx + rr_*math.cos(aa), cy + rr_*math.sin(aa); q.append((x_, y_, gzp(x_, y_)+dz))
            mb.poly(q)
D = lambda dx, dy: (mdx(dx), mdy(dy))
# side walks from the lower terrace (D) down to the R fountains, and their surrounding rings
for dx in (447, 632):
    ribbon(PG, catmull([D(dx, 380), D(dx, 412), D(dx, 432)]), 16)
    ribbon(PG, circle_pts(mdx(dx), mdy(445), 44), 12, closed=True)
# H basin ring walk and 8 round beds around it
ribbon(PG, circle_pts(0, yH, 118, 96), 16, closed=True)
for k in range(8):
    t = 2*math.pi*k/8 + math.pi/8
    if abs(math.cos(t)) < 0.3: continue
    sector(FB, 140*math.cos(t), yH + 140*math.sin(t), 0, 11, 0, 2*math.pi, na=12, nr=2)
# I gardens: whirling rosettes with central disc, inner ring, 6 radiating walks and 6 whirl beds, outer ring walk
for dx in (370, 698):
    cx, cy = mdx(dx), mdy(555)
    ribbon(PG, circle_pts(cx, cy, 290, 120), 14, closed=True)
    ribbon(PG, circle_pts(cx, cy, 185, 96), 10, closed=True)
    ribbon(PG, circle_pts(cx, cy, 48, 48), 10, closed=True)
    sector(FB, cx, cy, 0, 40, 0, 2*math.pi, na=16, nr=3)
    for k in range(6):
        a = 2*math.pi*k/6
        sp = [(cx + rr_*math.cos(a + 0.55*rr_/290), cy + rr_*math.sin(a + 0.55*rr_/290)) for rr_ in range(53, 291, 12)]
        ribbon(PG, sp, 9)
        sector(FB, cx, cy, 62, 175, a + 0.16, a + 0.75, twist=0.38)
        sector(FB, cx, cy, 195, 280, a + 0.40, a + 0.95, twist=0.20)
    # link walks from the R rings and the H ring to the I outer ring
    sgn = -1 if dx < 541 else 1
    ribbon(PG, catmull([(mdx(447 if sgn < 0 else 632) + sgn*30, mdy(445) - 34), (cx - sgn*120, cy + 300), (cx - sgn*150, cy + 250)]), 12)
    ribbon(PG, catmull([(sgn*110, yH - 40), (sgn*220, yH - 120), (cx - sgn*280, cy + 40)]), 12)
# walks around the M basins (offset outline of the simplified basin shape) and the cross walk between the J heads
for dx in (420, 662):
    ribbon(PG, super_ellipse(mdx(dx), yM, 430, 262, n=120), 18, closed=True)
ribbon(PG, [D(330, 560), D(495, 560)], 14); ribbon(PG, [D(587, 560), D(752, 560)], 14)
# perimeter serpentine walks (west mirrored to east; east side kept short of lake K; I)
west = [D(318, 395), D(308, 440), D(322, 480), D(308, 530), D(300, 600), D(325, 650), D(360, 672)]
ribbon(PG, catmull(west), 12)
ribbon(PG, catmull([(-x_, y_) for x_, y_ in west[:5]]), 12)
# lower-terrace parterres: grass panels with gravel border walks and four lobed bedding beds round each basin (map S; I)
for xs_ in (-720, -515, -231, 231, 515, 720):
    ribbon(PG, [(xs_-80, YP0+5), (xs_+80, YP0+5), (xs_+80, YP1-5), (xs_-80, YP1-5)], 7, dz=0.4, closed=True)
    ribbon(PG, circle_pts(xs_, YPC, 56, 64), 7, dz=0.4, closed=True)
    for k in range(4):
        a = math.pi/2*k + math.pi/4
        sector(FB, xs_, YPC, 63, 74, a-0.55, a+0.55, dz=0.5)
    for (bx, by) in ((xs_-68, YP0+16), (xs_+68, YP0+16), (xs_-68, YP1-16), (xs_+68, YP1-16)):
        sector(FB, bx, by, 0, 7, 0, 2*math.pi, na=12, nr=2, dz=0.5)
PG.done(); FB.done(); GPN.done()

# ---------- nave planting & statuary (PLACEHOLDERS; bed x-positions detected on plan 0205: checks/plan_nave_beds.json) ----------
NP = C['SY_nave_planting_statuary__placeholders']
import json, random
random.seed(1856)
beds = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'checks', 'plan_nave_beds.json')))
tub = MB('PLACEHOLDER_nave_tubs', NP, M['wood']); st = MB('PLACEHOLDER_nave_statues', NP, M['marble'])
def tree_broadleaf(x, y, z, h=30, name='tree'):
    bmt = bmesh.new()
    bmesh.ops.create_cone(bmt, cap_ends=True, segments=8, radius1=f(0.9), radius2=f(0.5), depth=f(h*0.55), matrix=Matrix.Translation(Vector((f(x), f(y), f(z+h*0.275)))))
    me1 = bpy.data.meshes.new(name+'_trunk'); bmt.to_mesh(me1); me1.materials.append(M['bark']); o1 = bpy.data.objects.new(name+'_trunk', me1); NP.objects.link(o1)
    bmc = bmesh.new()
    for k in range(9):
        sc_ = h/30.0; r = random.uniform(4.5, 7.5)*sc_; dx_, dy_ = random.uniform(-6, 6)*sc_, random.uniform(-6, 6)*sc_; dz_ = random.uniform(h*0.55, h*0.95)
        res = bmesh.ops.create_icosphere(bmc, subdivisions=2, radius=f(r), matrix=Matrix.Translation(Vector((f(x+dx_), f(y+dy_), f(z+dz_)))))
        for v in res['verts']: v.co += Vector([random.uniform(-0.25, 0.25) for _ in range(3)]) * f(r*0.5)
    me2 = bpy.data.meshes.new(name+'_crown'); bmc.to_mesh(me2); me2.materials.append(M['foliage'])
    for pl in me2.polygons: pl.use_smooth = True
    o2 = bpy.data.objects.new(name+'_crown', me2); NP.objects.link(o2)
def palm(x, y, z, h=26, name='palm'):
    bmt = bmesh.new()
    bmesh.ops.create_cone(bmt, cap_ends=True, segments=8, radius1=f(1.0), radius2=f(0.6), depth=f(h), matrix=Matrix.Translation(Vector((f(x), f(y), f(z+h/2)))))
    me1 = bpy.data.meshes.new(name+'_trunk'); bmt.to_mesh(me1); me1.materials.append(M['bark']); o1 = bpy.data.objects.new(name+'_trunk', me1); NP.objects.link(o1)
    bmf = bmesh.new()
    for k in range(14):
        th = 2*math.pi*k/14 + random.uniform(-0.15, 0.15); L = random.uniform(11, 15); prev = None
        for i in range(7):
            t = i/6; d = L*t; zz = z + h + 3*math.sin(math.pi*t*0.8) - 7*t*t; wdt = 2.2*math.sin(math.pi*min(t*1.1, 1)) + 0.2
            cx_, cy_ = x + d*math.cos(th), y + d*math.sin(th); px, py = -math.sin(th)*wdt/2, math.cos(th)*wdt/2
            cur = (bmf.verts.new((f(cx_-px), f(cy_-py), f(zz))), bmf.verts.new((f(cx_+px), f(cy_+py), f(zz))))
            if prev: bmf.faces.new((prev[0], prev[1], cur[1], cur[0]))
            prev = cur
    me2 = bpy.data.meshes.new(name+'_fronds'); bmf.to_mesh(me2); me2.materials.append(M['palm']); o2 = bpy.data.objects.new(name+'_fronds', me2); NP.objects.link(o2)
k = 0
for side, yy in (('west', 26), ('garden', -26)):
    for xx in beds[side]:
        if in_span(xx, [(c_, w_+20) for c_, w_ in TSPANS]) or abs(xx) > HALF-20: continue
        tub.box(xx-4, xx+4, yy-4, yy+4, 0, 3.5)
        (palm if k % 2 else tree_broadleaf)(xx, yy, 3.5, name=f'PLACEHOLDER_nave_{"palm" if k%2 else "tree"}_{side}_{int(xx)}'); k += 1
# r05: statue / group / basin placeholders at marks DETECTED on plan 0205 (scripts/plan_nave_objects.py ->
# checks/plan_nave_objects_filtered.json; R for position, I for form). r04's regular 72 ft statue rhythm (I) and the
# crossing Crystal Fountain (no mark on 0205 at the crossing) are withdrawn.
objs = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'checks', 'plan_nave_objects_filtered.json')))
cf_s = MB('PLACEHOLDER_nave_basins_groups', NP, M['stone']); cf_w = MB('PLACEHOLDER_nave_basins_water', NP, M['water'])
for o_ in objs:
    x_, y_, w_, d_ = o_['x'], o_['y'], o_['w'], o_['d']
    if o_['kind'] == 'statue':
        statue(x_, y_, 0, st, scale=1.0)
    else:   # ~10 ft mark: low basin with a sculpture group on a central pedestal (placeholder)
        r_ = max(w_, d_)/2
        basin(cf_s, cf_w, x_, y_, 0, r_, n=28, rim=0.9, h=2.0)
        st.box(x_-1.6, x_+1.6, y_-1.6, y_+1.6, 0, 4.5); st.box(x_-1.2, x_+1.2, y_-1.0, y_+1.0, 4.5, 11)
cf_s.done(); cf_w.done()
tub.done(); st.done()
# r05: park trees (PLACEHOLDERS, density/species I) so the 1857 park reads as wooded, as on map 0591 and photo 0007
PT = coll('SY_park_trees__placeholders')
_NP_saved = NP; NP = PT
random.seed(1857); placed = []
yHc = mdy(500); yMc = mdy(700)
while len(placed) < 70:
    x_ = random.uniform(-1250, 1250); y_ = random.uniform(-2300, -720)
    if abs(x_) < 140: continue                                                   # central axis, cascades
    if math.hypot(x_, y_-yHc) < 130: continue
    if any(abs(x_-mdx(dx)) < 430 and abs(y_-yMc) < 260 for dx in (420, 662)): continue
    if any(math.hypot(x_-mdx(dx), y_-mdy(445)) < 50 for dx in (447, 632)): continue
    if any(math.hypot(x_-a, y_-b) < 45 for a, b in placed): continue
    placed.append((x_, y_)); h_ = random.uniform(38, 60)
    tree_broadleaf(x_, y_, zs(y_), h=h_, name=f'PLACEHOLDER_park_tree_{len(placed):02d}')
NP = _NP_saved

FI.done()

# ---------- reference plan plane (registered 0205), hidden in renders ----------
PLAN = '/workspace/crystal-palace/references/muse-drive/images/commons/Guide_to_the_Crystal_Palace_and_Park_1856_(147900384).jpg'
if os.path.exists(PLAN):
    img = bpy.data.images.load(PLAN); W, H = img.size
    pm = bpy.data.materials.new('plan_0205'); pm.use_nodes = True
    tex = pm.node_tree.nodes.new('ShaderNodeTexImage'); tex.image = img
    pm.node_tree.links.new(tex.outputs[0], pm.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
    bm = bmesh.new(); s = PLAN_PX_PER_FT
    corners = [(0, H), (W, H), (W, 0), (0, 0)]
    vs = [bm.verts.new((f((px-PLAN_X0)/s), f(-(py-PLAN_Y0)/s), f(-BD-3))) for px, py in corners]
    face = bm.faces.new(vs); uv = bm.loops.layers.uv.new()
    for lp, (u, v) in zip(face.loops, ((0,0),(1,0),(1,1),(0,1))): lp[uv].uv = (u, v)
    me = bpy.data.meshes.new('plan_0205'); bm.to_mesh(me); me.materials.append(pm)
    o = bpy.data.objects.new('REF_plan_0205_registered', me); refc.objects.link(o); o.hide_render = True
    refc.hide_render = True

# ---------- cameras (36 mm sensor; storyboard camera grammar) ----------
def cam(name, loc_ft, look_ft, lens, ortho=None):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.sensor_width = 36; cd.clip_end = 3000
    if ortho: cd.type = 'ORTHO'; cd.ortho_scale = f(ortho)
    o = bpy.data.objects.new(name, cd); C['CAMERAS'].objects.link(o)
    o.location = [f(v) for v in loc_ft]
    d = Vector([f(v) for v in look_ft]) - o.location
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return o
EYE = 1.6/F
cam('CAM_ext_garden_34_terrace', (640, yL+30, LT+EYE), (-80, -120, 95), 35)
cam('CAM_central_transept_straight', (0, yL+10, LT+EYE), (0, 0, 120), 35)
cam('CAM_nave_interior_28mm', (-330, 0, EYE), (0, 0, EYE+6), 28)
cam('CAM_ext_elevated_overview', (900, -1300, 420), (-50, -60, 40), 35)
cam('CAM_plan_overlay_top', (0, 0, 2000), (0, 0, 0), 50)
cam('CAM_compare_0074', (-340, yL+60, LT+EYE+6), (160, -157, 62), 35)       # r05: photo 0074 from lower terrace S of CT looking N along garden front (I)
cam('CAM_compare_0007', (60, -1500, LT+30), (-194, -157, -98), 35)  # r07: re-solved from tower/transept bearings (-21°/+8°) and H basin in the foreground; raised, looking down (I)
cs = cam('CAM_section_cut_x-300', (-330, -20, 62), (0, -20, 62), 50, ortho=400)  # r07: true section on braced grid line x=-300 (k=21)
cs.data.clip_start = f(24); cs.data.clip_end = f(36)  # slice x=-306..-294
# r10 CP047/CP048 (storyboard: north end from the upper garden terrace; terrace walk). Same cameras in both states so the
# SY-EARLY / SY-POST66 renders are a matched before/after pair (positions I).
cam('CAM_CP047_north_end_35mm', (280, yU + 10, UT + EYE), (620, -156, 50), 35)
_c48 = cam('CAM_CP048_terrace_walk_35mm', (380 + 7.0/F, yU + 24, UT + EYE), (760, -150, 40), 35)
_c48.location = [f(v) for v in (380, yU + 24, UT + EYE)]; _c48.keyframe_insert('location', frame=1)
_c48.location = [f(v) for v in (380 + 7.0/F, yU + 24, UT + EYE)]; _c48.keyframe_insert('location', frame=120)   # 7 m walk north
cam('CAM_CP048_terrace_hold_35mm', (380 + 7.0/F, yU + 24, UT + EYE), (760, -150, 40), 35)
sc.camera = bpy.data.objects['CAM_ext_garden_34_terrace']

# ---------- r08: fine-arts courts (separate collections inside the shell) ----------
if not os.environ.get('SY_NO_COURTS'):   # r07 shell-only round was built with SY_NO_COURTS=1
    exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'courts.py')).read())

# ---------- world / render ----------
w = bpy.data.worlds.new('sky'); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes['Background']
sky = nt.nodes.new('ShaderNodeTexSky')
try: sky.sky_type = 'NISHITA'
except Exception: pass
try:
    sky.sun_elevation = math.radians(28); sky.sun_rotation = math.radians(200)
except Exception: pass
nt.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 0.35
sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 2.2; sun.angle = math.radians(0.6)
so = bpy.data.objects.new('sun', sun); root.objects.link(so); so.rotation_euler = (math.radians(58), 0, math.radians(200))
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 48
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6; sc.cycles.transparent_max_bounces = 24
sc.render.resolution_x = 1920; sc.render.resolution_y = 1080
sc.view_settings.view_transform = 'AgX' if 'AgX' in [i.identifier for i in sc.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
sc.unit_settings.system = 'METRIC'
sc.view_settings.exposure = -1.0
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'states.py')).read())   # r11 later states + sphinxes
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
tri = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
print('BUILD_OK', OUT, 'objects', len(bpy.data.objects), 'faces', tri)
