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
M = {
 'iron': mat('iron_painted', (0.50,0.53,0.55), 0.45, 0.2),     # I: paint colour unresolved (U)
 'glass_roof': glass_mat('glass_roof', (0.80,0.86,0.85), 0.012, 8.0),
 'glass_wall': glass_mat('glass_wall', (0.78,0.85,0.84), 0.02, 8.0),
 'floor': mat('boards', (0.30,0.22,0.15), 0.8),
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
     'SY_terraces_terrain', 'CAMERAS']}
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
wall_y(156, 0, TIERS[0]); wall_y(132, TIERS[0], TIERS[1]); wall_y(60, TIERS[1], TIERS[2]); wall_y(36, TIERS[2], NAVE_SPRING)
wall_y(-156, 0, TIERS[0]); wall_y(-108, TIERS[0], TIERS[1]); wall_y(-60, TIERS[1], TIERS[2]); wall_y(-36, TIERS[2], NAVE_SPRING)
# end walls x = +-HALF: stepped profile
for xe in (-HALF, HALF):
    for hi, lo, h in BANDS:
        top = NAVE_SPRING if h == 'vault' else h
        gw.poly([(xe,lo,0),(xe,hi,0),(xe,hi,top),(xe,lo,top)])
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
vault('central_transept_vault', C['SY_central_transept'], 'y', 0, CT_SPAN, CT_SPRING, CT_Y0, CT_Y1, 24.0, nseg=48)
for nm, xc in (('south', -ST_X), ('north', ST_X)):
    key = 'SY_south_transept' if nm=='south' else 'SY_north_transept__lost1866'
    vault(nm+'_transept_vault', C[key], 'y', xc, ST_SPAN, NAVE_SPRING, -156, 156, 24.0)

# transept walls (clerestory/side screens) and end screens with 24 ft garden recesses
def transept(key, xc, span, spring, y0, y1, recess):
    c = C[key]; w = MB(key+'_walls', c, M['glass_wall']); fr = MB(key+'_frame', c, M['iron'])
    R = span/2
    for xs in (xc-R, xc+R):
        # side walls from floor to springing, only where above surrounding roofs (whole height for simplicity)
        w.poly([(xs,y0,0),(xs,y1,0),(xs,y1,spring),(xs,y0,spring)])
        y = y0
        while y <= y1+0.01:  # wall columns/stacks every 24 ft
            fr.box(xs-1.0, xs+1.0, y-1.0, y+1.0, 0, spring); y += BAY
        for t in TIERS + [spring]:
            fr.box(xs-0.5, xs+0.5, y0, y1, t-3, t)
    # end screens: west end at y1, garden end recessed
    for ye, flat in ((y1, False), (y0+recess, True)):
        w.poly([(xc-R,ye,0),(xc+R,ye,0),(xc+R,ye,spring),(xc-R,ye,spring)])
        n = 32
        for i in range(n):
            a0 = math.pi*i/n; a1 = math.pi*(i+1)/n
            w.poly([(xc,ye,spring),(xc+R*math.cos(a0),ye,spring+R*math.sin(a0)),(xc+R*math.cos(a1),ye,spring+R*math.sin(a1))])
        # radial bars of the lunette
        for i in range(0, n+1, 4):
            a = math.pi*i/n
            fr.box(xc+R*0.5*math.cos(a)-0.3, xc+R*0.5*math.cos(a)+0.3, ye-0.3, ye+0.3, spring, spring+0.5)
        for xx in [xc-R + k*8 for k in range(int(span/8)+1)]:
            fr.box(xx-0.25, xx+0.25, ye-0.4, ye+0.4, 0, spring + (math.sqrt(max(R*R-(xx-xc)**2,0))))
        for t in TIERS + [spring]:
            fr.box(xc-R, xc+R, ye-0.5, ye+0.5, t-1.5, t)
    # recess floor / open arch frame at garden face
    fr.box(xc-R-1, xc-R+1, y0-1, y0+1, 0, spring); fr.box(xc+R-1, xc+R+1, y0-1, y0+1, 0, spring)
    w.done(); fr.done()
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
bs.box(-HALF, HALF, -157, -156, -BD, 0)            # front wall (windows in glass layer below)
bs.box(-HALF, HALF, -108, -84, -BD, -BD+1)        # tunnel floor (24 ft wide)
bs.box(-HALF, HALF, -84, -83, -BD, 0)             # tunnel inner wall
bs.box(-HALF-1, -HALF, -157, -83, -BD, 0); bs.box(HALF, HALF+1, -157, -83, -BD, 0)
bs.box(-CT_SPAN/2-2, CT_SPAN/2+2, CT_Y0-1, -156, -BD, -1)  # central projection plinth
bs.done()
bw = MB('basement_windows', C['SY_basement_garden_front'], M['glass_wall'])
x = -HALF + 4
while x < HALF - 12:
    bw.poly([(x,-157.1,-BD+3),(x+16,-157.1,-BD+3),(x+16,-157.1,-3),(x,-157.1,-3)]); x += BAY
bw.done()

# ---------- wings (574 ft, toward the garden at both ends) ----------
wg = MB('wings_glass', C['SY_wings'], M['glass_wall']); wf = MB('wings_frame', C['SY_wings'], M['iron']); wr = MB('wings_roof', C['SY_wings'], M['glass_roof'])
for sx in (-1, 1):
    xc = sx*WING_CX; xa, xb = xc-WING_W/2, xc+WING_W/2
    ya, yb = WING_Y0 - WING_LEN, WING_Y0
    top = TIERS[1]   # I: wing roof level with 2nd tier of main building; base steps down with slope (U)
    zb = -BD - 10    # I: wing lower storey below basement level (guide p.29-30: 3 storeys in South Wing)
    for (p0, p1) in (((xa,ya),(xa,yb)), ((xb,ya),(xb,yb)), ((xa,ya),(xb,ya))):
        wg.poly([(p0[0],p0[1],zb),(p1[0],p1[1],zb),(p1[0],p1[1],top),(p0[0],p0[1],top)])
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

# ---------- terraces and terrain ----------
T = MB('terrain', C['SY_terraces_terrain'], M['grass']); S = MB('terraces_stone', C['SY_terraces_terrain'], M['stone']); G = MB('terrace_gravel', C['SY_terraces_terrain'], M['gravel'])
UT = -BD; LT = UT - LOWER_TERRACE_DROP
yU = -157 - UPPER_TERRACE_D; yL = yU - LOWER_TERRACE_D
TX = HALF - 20
G.box(-TX, TX, yU, -157, UT-2, UT)                            # upper terrace (gravel)
S.box(-TX, TX, yU-2, yU, LT, UT+3.5)                           # retaining wall + balustrade
for k in range(int(2*TX/6)):
    S.box(-TX+k*6, -TX+k*6+1.0, yU-1.6, yU-0.4, UT, UT+3.2)    # balusters (coarse)
G.box(-TX, TX, yL, yU-2, LT-2, LT)                            # lower terrace
# grand central flight
for i in range(10):
    S.box(-48, 48, yU-2-i*3, yU-2-(i+1)*3, LT, UT - i*(LOWER_TERRACE_DROP/10) + 0.01)
# grass parterres on lower terrace
for xa in (-700, -480, -260, 60, 280, 500):
    T.box(xa, xa+160, yL+40, yU-40, LT, LT+0.4)
# west (Parade) side ground at floor level, slope beyond terraces toward the garden
T.box(-1100, 1100, 156, 700, -3, -0.5)
T.box(-1100, 1100, -157, 156, -BD-1, -BD)  # ground under building/basement zone
T.box(-1100, -TX, yL, -157, LT-1, LT)
T.box(TX, 1100, yL, -157, LT-1, LT)
bm = bmesh.new()
pts = []
for i, (y, z) in enumerate(((yL, LT-1), (yL-1400, LT-140))):  # U: ~1:10 fall, Penge at foot of hill
    pts.append(((-1300, y, z), (1300, y, z)))
vs = [bm.verts.new((f(a),f(b),f(c))) for a,b,c in (pts[0][0], pts[0][1], pts[1][1], pts[1][0])]; bm.faces.new(vs)
me = bpy.data.meshes.new('lower_slope'); bm.to_mesh(me); me.materials.append(M['grass'])
o = bpy.data.objects.new('lower_slope', me); C['SY_terraces_terrain'].objects.link(o)
T.done(); S.done(); G.done()

# fountains on lower terrace (dated; U)
fo = MB('terrace_basins', C['SY56_fountains_basins__dated'], M['stone']); fw = MB('terrace_basin_water', C['SY56_fountains_basins__dated'], M['water'])
for xc in (-420, 420, -620, 620):
    yc = (yL + yU)/2; r = 34
    n = 32
    ring = [(xc + r*math.cos(2*math.pi*k/n), yc + r*math.sin(2*math.pi*k/n)) for k in range(n)]
    for k in range(n):
        a = ring[k]; b = ring[(k+1)%n]
        fo.box(min(a[0],b[0])-0.8, max(a[0],b[0])+0.8, min(a[1],b[1])-0.8, max(a[1],b[1])+0.8, LT, LT+2.2)
    fw.poly([(p[0], p[1], LT+1.6) for p in ring])
fo.done(); fw.done()


# r02: distant ground plane so elevated views do not show sky below horizon (U: Penge/Anerley lowland level)
T2 = MB('distant_ground', C['SY_terraces_terrain'], M['grass']); T2.box(-60000, 60000, -90000, 60000, LT-142, LT-141); T2.done()
# r02: nave planting/statuary placeholders (guide: nave laid out with trees, plants, sculpture; positions I)
ip = MB('nave_planting_tubs', C['SY_main_frame'], M['wood'])
xx = -HALF + 36
while xx < HALF - 36:
    if not in_span(xx, [(c, w+30) for c,w in TSPANS]):
        for yy in (-22, 22):
            ip.box(xx-3, xx+3, yy-3, yy+3, 0, 3.5)
            ip.box(xx-0.4, xx+0.4, yy-0.4, yy+0.4, 3.5, 10)
            tb = bmesh.new(); bmesh.ops.create_uvsphere(tb, u_segments=12, v_segments=8, radius=f(7))
            bmesh.ops.scale(tb, vec=(1,1,1.35), verts=tb.verts); bmesh.ops.translate(tb, vec=(f(xx),f(yy),f(17)), verts=tb.verts)
            tm = bpy.data.meshes.new('tree'); tb.to_mesh(tm); tm.materials.append(M['grass'])
            for pl in tm.polygons: pl.use_smooth = True
            to = bpy.data.objects.new(f'nave_tree_{int(xx)}_{yy}', tm); C['SY_main_frame'].objects.link(to)
    xx += 72
ip.done(); 
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
    if ortho: cd.type = 'ORTHO'; cd.ortho_scale = ortho
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
