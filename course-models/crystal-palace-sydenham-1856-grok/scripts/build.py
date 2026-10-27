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

# ---------- collections ----------
root = bpy.data.collections.new('SY-EARLY_c1856'); sc.collection.children.link(root)
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
    def done(s):
        me = bpy.data.meshes.new(s.name); s.bm.to_mesh(me); s.bm.free()
        me.materials.append(s.m); o = bpy.data.objects.new(s.name, me); s.col.objects.link(o); return o

HALF = LENGTH/2
def in_span(x, xs):  # inside a transept span (open interior)
    return any(abs(x-c) < w/2 - 0.1 for c,w in xs)
TSPANS = [(0, CT_SPAN), (-ST_X, ST_SPAN), (ST_X, ST_SPAN)]
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
            fb('SY_main_frame').box(xa, xb, y-0.35, y+0.35, t-3, t)
for x in xs_grid:
    if in_span(x, TSPANS): continue
    for (ya, yb) in zip(COL_Y[:-1], COL_Y[1:]):
        if abs(ya)==36 and abs(yb)==36: continue  # nave: vault ribs instead
        hmin = min(col_h(ya), col_h(yb))
        for t in TIERS:
            if t <= hmin+0.1:
                fb('SY_main_frame').box(x-0.35, x+0.35, yb, ya, t-3, t)
# gallery floors at tier 1 in the inner bands (I: HP practice; Sydenham gallery area 261,568 sq ft, guide p.35)
gal = MB('gallery_floors', C['SY_main_frame'], M['floor'])
for (yh, yl) in [(108,60),(60,36),(-36,-60),(-60,-108)]:
    xa = -HALF
    for c,w in sorted(TSPANS):
        gal.box(xa, c-w/2, yl, yh, GALLERY_FLOOR-0.6, GALLERY_FLOOR); xa = c+w/2
    gal.box(xa, HALF, yl, yh, GALLERY_FLOOR-0.6, GALLERY_FLOOR)
for (yh, yl) in [(60,36),(-36,-60)]:  # second gallery in the tower stacks
    xa = -HALF
    for c,w in sorted(TSPANS):
        gal.box(xa, c-w/2, yl, yh, TIERS[1]+0.2, TIERS[1]+0.8); xa = c+w/2
    gal.box(xa, HALF, yl, yh, TIERS[1]+0.2, TIERS[1]+0.8)
gal.done()
for _mb in list(frame.values()): _mb.done()  # r04 BUGFIX: r01-r03 never finalised the column/girder meshes
# ground floor (boarded, 1.5 in boards with gaps: shader-free, U)
fl = MB('main_floor', C['SY_main_frame'], M['floor']); fl.box(-HALF, HALF, -156, 156, -1.0, 0); fl.done()

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
wall_y(156, 0, TIERS[0]); wall_y(132, TIERS[0], TIERS[1]); wall_y(60, TIERS[1], TIERS[2]); wall_y(36, TIERS[2], NAVE_SPRING)
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
    # ribs: lattice arch ribs (rendered as a band 1.5 ft deep, 0.67 wide), and purlins
    t = a_lo
    while t <= a_hi + 0.01:
        if not (skip and skip(t)):
            for i in range(nseg):
                u0 = math.pi*i/nseg; u1 = math.pi*(i+1)/nseg
                for (ta, tb) in [(t-0.33, t+0.33)]:
                    pa, pb = P(ta,u0), P(ta,u1); pc, pd = P(tb,u1), P(tb,u0)
                    qa, qb = P(ta,u0,R-1.5), P(ta,u1,R-1.5); qc, qd = P(tb,u1,R-1.5), P(tb,u0,R-1.5)
                    r.poly([pa,pb,qb,qa]); r.poly([pd,pc,qc,qd]); r.poly([qa,qb,qc,qd])
        t += rib_every
    for i in range(0, nseg+1, 4):
        u = math.pi*i/nseg
        if axis=='x': a,b = P(a_lo,u), P(a_hi,u)
        else: a,b = P(a_lo,u), P(a_hi,u)
        # purlin as thin quad pair
        if axis=='x': r.box(a_lo, a_hi, a[1]-0.2, a[1]+0.2, a[2]-0.5, a[2])
        else: r.box(a[0]-0.2, a[0]+0.2, a_lo, a_hi, a[2]-0.5, a[2])
    return g.done(), r.done()
vault('nave_vault', C['SY_nave_vault'], 'x', 0, NAVE_SPAN, NAVE_SPRING, -HALF, HALF, 24.0, skip=lambda t: in_span(t, TSPANS))
CT_Y0, CT_Y1 = -156-CT_GARDEN_PROJ, 156+CT_WEST_PROJ
vault('central_transept_vault', C['SY_central_transept'], 'y', 0, CT_SPAN, CT_SPRING, CT_Y0+RECESS, CT_Y1, 24.0, nseg=48)
for nm, xc in (('south', -ST_X), ('north', ST_X)):
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
    # great end screen at yE: glazed from top step to springing, lunette above
    w.poly([(xc-R_,yE,TIERS[2]),(xc+R_,yE,TIERS[2]),(xc+R_,yE,spring),(xc-R_,yE,spring)])
    n = 32
    for i in range(n):
        a0 = math.pi*i/n; a1 = math.pi*(i+1)/n
        w.poly([(xc,yE,spring),(xc+R_*math.cos(a0),yE,spring+R_*math.sin(a0)),(xc+R_*math.cos(a1),yE,spring+R_*math.sin(a1))])
    for i in range(n):  # arch ring (main rib on the face)
        a0 = math.pi*i/n; a1 = math.pi*(i+1)/n
        p0 = (xc+R_*math.cos(a0), spring+R_*math.sin(a0)); p1 = (xc+R_*math.cos(a1), spring+R_*math.sin(a1))
        fr.box(min(p0[0],p1[0])-0.8, max(p0[0],p1[0])+0.8, yE-0.9, yE+0.9, min(p0[1],p1[1])-0.8, max(p0[1],p1[1])+0.8)
    for xx in [xc-R_ + k*8 for k in range(int(span/8)+1)]:
        fr.box(xx-0.25, xx+0.25, yE-0.4, yE+0.4, TIERS[2], spring + math.sqrt(max(R_*R_-(xx-xc)**2, 0)))
    for t in [spring, spring - (spring-TIERS[2])/2]:
        fr.box(xc-R_, xc+R_, yE-0.6, yE+0.6, t-2.5, t)
    # west end screen full height
    w.poly([(xc-R_,y1,0),(xc+R_,y1,0),(xc+R_,y1,spring),(xc-R_,y1,spring)])
    facade((xc-R_,y1),(xc+R_,y1), 0, spring, bands=list(TIERS))
    for i in range(n):
        a0 = math.pi*i/n; a1 = math.pi*(i+1)/n
        w.poly([(xc,y1,spring),(xc+R_*math.cos(a0),y1,spring+R_*math.sin(a0)),(xc+R_*math.cos(a1),y1,spring+R_*math.sin(a1))])
    w.done(); fr.done(); rr.done()
transept('SY_central_transept', 0, CT_SPAN, CT_SPRING, CT_Y0, CT_Y1, RECESS)
transept('SY_south_transept', -ST_X, ST_SPAN, NAVE_SPRING, -156, 156, RECESS)
transept('SY_north_transept__lost1866', ST_X, ST_SPAN, NAVE_SPRING, -156, 156, RECESS)
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
tw.done(); twg.done()

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
for xc_, wdt, yf in ((0, 72, CT_Y0), (-ST_X, 48, -157), (ST_X, 48, -157)):
    nst = 32; rise = BD/nst
    for i in range(nst):
        stt.box(xc_-wdt/2, xc_+wdt/2, yf-(nst-i)*1.25, yf-(nst-i-1)*1.25, -BD, -BD + (i+1)*rise)
    for sx in (-1, 1):
        stt.box(xc_+sx*wdt/2-1.2, xc_+sx*wdt/2+1.2, yf-nst*1.25, yf, -BD, 3)
bw.done(); stt.done(); bs.done()

# ---------- wings (574 ft, toward the garden at both ends) ----------
wg = MB('wings_glass', C['SY_wings'], M['glass_wall']); wf = MB('wings_frame', C['SY_wings'], M['iron_ext']); wr = MB('wings_roof', C['SY_wings'], M['glass_roof'])
for sx in (-1, 1):
    xc = sx*WING_CX; xa, xb = xc-WING_W/2, xc+WING_W/2
    ya, yb = WING_Y0 - WING_LEN, WING_Y0
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
for nm, sx in (('south', -1), ('north', 1)):
    o = MB('water_tower_'+nm, C['SY56_water_towers__dated'], M['iron']); g = MB('water_tower_glass_'+nm, C['SY56_water_towers__dated'], M['glass_wall'])
    xc = sx*(HALF+120); yc = 60
    sides = 12
    def ring(r, z): return [(xc + r*math.cos(2*math.pi*k/sides), yc + r*math.sin(2*math.pi*k/sides), z) for k in range(sides)]
    for (r0, z0, r1, z1) in ((24, 0, 20, TOWER_H-40),):
        a = ring(r0, z0); b = ring(r1, z1)
        for k in range(sides):
            k1 = (k+1) % sides
            g.poly([a[k], a[k1], b[k1], b[k]])
            o.box(a[k][0]-1, a[k][0]+1, a[k][1]-1, a[k][1]+1, 0, z1)
        for z in range(0, int(TOWER_H-40), 12):
            rr = r0 + (r1-r0)*z/(TOWER_H-40); q = ring(rr, z)
            for k in range(sides):
                k1 = (k+1)%sides; o.poly([q[k], q[k1], (q[k1][0], q[k1][1], z+1.2), (q[k][0], q[k][1], z+1.2)])
    tk = ring(24, TOWER_H-40); tt = ring(24, TOWER_H-8)
    for k in range(sides):
        k1 = (k+1) % sides; o.poly([tk[k], tk[k1], tt[k1], tt[k]])
    o.poly(list(reversed(tt))); o.poly(tk)
    o.done(); g.done()

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
S.box(-TX, TX, yU-3, yU, LT, UT)                                # retaining wall
def balustrade(xa, xb, y, z, statues_every=None, gap=None):
    """plinth 0.8, balusters 0.55 wide @1.4 ft, coping 0.6 -> 3.3 ft high (I: typical Italianate terrace scale)"""
    segs = [(xa, xb)] if not gap else [(xa, gap[0]), (gap[1], xb)]
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
balustrade(-TX, TX, yU-1.5, UT, statues_every=96, gap=(-48, 48))
G.box(-TX, TX, yL, yU-3, LT-2, LT)                              # lower terrace
balustrade(-TX, TX, yL+1, LT, statues_every=144, gap=(-30, 30))
for i in range(10):                                              # grand central flight upper->lower terrace
    S.box(-48, 48, yU-3-(i+1)*3, yU-3-i*3, LT, UT - i*(LOWER_TERRACE_DROP/10) + 0.01)
for sx in (-1, 1): S.box(sx*48-1.5, sx*48+1.5, yU-33, yU, LT, UT+3.3)
for i in range(14):                                              # central flight lower terrace -> park (I)
    S.box(-30, 30, yL-(i+1)*2.6, yL-i*2.6, zs(yL-i*2.6)-3, LT - i*(LT-zs(yL-40))/14)
# parterres on the lower terrace: 6 beds with S fountains (map 0591 S, R)
for xs_ in (-720, -515, -231, 231, 515, 720):
    T.box(xs_-85, xs_+85, yL+30, yU-30, LT, LT+0.4)
T.box(-1100, 1100, 156, 700, -3, -0.5)
T.box(-1100, 1100, -157, 156, -BD-1, -BD)
T.box(-1100, -TX, yL, -157, LT-1, LT); T.box(TX, 1100, yL, -157, LT-1, LT)
bm = bmesh.new(); vv = []
for y, z in PROF:
    vv.append((bm.verts.new((f(-1600), f(y), f(z))), bm.verts.new((f(1600), f(y), f(z)))))
for (a0, a1), (b0, b1) in zip(vv[:-1], vv[1:]): bm.faces.new((a0, a1, b1, b0))
me = bpy.data.meshes.new('park_slope'); bm.to_mesh(me); me.materials.append(M['grass'])
o = bpy.data.objects.new('park_slope', me); C['SY_terraces_terrain'].objects.link(o)
for (ya, za), (yb, zb) in zip(PROF[:-1], PROF[1:]):
    bmw = bmesh.new(); q = [bmw.verts.new((f(x_), f(y_), f(z_+0.3))) for x_, y_, z_ in ((-20, ya, za), (20, ya, za), (20, yb, zb), (-20, yb, zb))]
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
for xs_ in (-720, -515, -231, 231, 515, 720):
    basin(fo, fw, xs_, (yL+yU)/2, LT, 45, n=56, rim=1.6, h=2.4, jet=14)   # r05: map S ~25 dpx dia ≈ 107 ft (R); r04 r=22 too small
fo.done(); fw.done()

# ---------- park fountains & cascades (map 0591: R, H, J, L, M) : SY56_park_fountains_cascades__dated ----------
PF = C['SY56_park_fountains_cascades__dated']
po = MB('park_basins_stone', PF, M['stone']); pw = MB('park_basins_water', PF, M['water'])
for dx in (447, 632):                                            # R fountains
    x_, y_ = mdx(dx), mdy(445); po.box(x_-30, x_+30, y_-30, y_+30, zs(y_)-2, zs(y_)); basin(po, pw, x_, y_, zs(y_), 20, jet=10)
yH = mdy(500); zH = zs(yH)                                       # H large circular fountain (map ~36 dpx dia ≈ 154 ft; R)
po.box(-100, 100, yH-100, yH+100, zH-3, zH); basin(po, pw, 0, yH, zH, 77, n=64, rim=2.5, h=3, jet=24)
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
po.done(); pw.done()

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
cam('CAM_compare_0007', (-260, -1500, LT+30), (-302, -157, LT-12), 35)  # r05b: photo 0007 is elevated over the terraces; tower@5%/CT@~70% for 35 mm (I)
cs = cam('CAM_section_cut_x-276', (-300, -20, 80), (0, -20, 80), 50, ortho=430)  # true section: clip slice x=-276..-252 (between grid lines, ortho)
cs.data.clip_start = f(18); cs.data.clip_end = f(30)  # slice x=-282..-270 through column line -276
sc.camera = bpy.data.objects['CAM_ext_garden_34_terrace']

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
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
tri = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
print('BUILD_OK', OUT, 'objects', len(bpy.data.objects), 'faces', tri)
