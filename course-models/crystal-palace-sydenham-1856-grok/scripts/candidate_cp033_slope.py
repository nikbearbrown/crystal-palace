"""CP033 CANDIDATE (2026-11-16): 'A new building on a slope' — Sydenham park slope below the terraces, c. autumn 1853.

usage: blender -b rounds/sydenham-build53-r18b.blend -P scripts/candidate_cp033_slope.py [-- out.blend]
       (env CP033_NOSAVE=1: build in memory only)
Opens the live CP033 round (never writes it) -> rounds/candidates/sydenham-build53-r18b_cp033slope.blend.
The live hero (renders/r18_build53_CAM_CP033_slope_up_35mm.png) shows the rising palace above a flat, uniform beige plane:
the slope does not read, the one big spoil heap in the centre is a low 24-sided cone with a floating rim, the 'navvies'
are pv57 instance posts with white heads that read as signposts, and a placeholder tree blob floats at the right edge.
Adds dated collection SY53_slope_works__autumn1853 (cp_state SY-BUILD_c1853_slope_works) and:
  1. park-slope works ground in the CAM_CP033 frustum (overlay 2-4 cm above park_slope): worked London-clay surface with
     micro-relief, two wheel-rutted cart tracks up the slope, wet trodden bands, remnant rough pasture patches (old Penge
     Place park, I) — park_slope itself is unchanged;
  2. the centre cone heap (earth_spoil_heaps_cuttings island at x 55, y -219 m) dropped from a mesh COPY (original hidden,
     not deleted) and replaced by an irregular grounded tip heap with plank barrow runs (Delamotte 1852-53 'Workmen in the
     grounds' / 'Commencement of the terraces', R for barrow-and-plank earthworks; shapes I);
  3. pv57 navvy instance points inside the CAM_CP033 frustum (<= 430 m) dropped from a mesh COPY of ppl53_navvies_erectors
     and re-placed at the same spots as people_lib v3.4 1850s_navvy / 1850s_workman figures; plus a foreground navvy gang
     cutting the bank with shovels/picks and barrows, three horse-drawn tip carts with carters, a surveyor's level and staff,
     ranging poles along the slope;
  4. lower-terrace garden-front wall (x 40..238 m, y -195.5 m) under construction where BUILD53 had nothing (terraces_stone
     is clipped for x > 40): brick piers + part-built alcove arches, pole scaffolds, brick stacks, two shear-legs (I/U);
  5. placeholder tree 38 (52 m from the lens, right edge) hidden and replaced by an elm (trees.py build_elm recipe, CP032).
Cameras NOT moved, sun/world/exposure NOT changed (Filmic -1.0 EV). Units metres in the blend; feet in DEPARTURES.
Sources: guide 1854 'The Terraces' (upper terrace 1576 x 48 ft; central steps and Grand Central Walk 96 ft; lower terrace
1664 x 512 ft); Gardeners' Chronicle/Journal of Horticulture 1853 ('about 1000 labourers ... levelling the ground, forming
basins'); Delamotte, Photographic Views of the Progress of the Crystal Palace, Sydenham (1855): 'Commencement of terraces
Aug. 1852', 'Workmen in the grounds', 'The Terrace Front, with Mortar Machine', 'Scaffolding for the erection of the great
ribs'; CPF history (1,608 ft long, three transepts, barrel-vaulted nave).
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector, Matrix, noise
from bpy_extras.object_utils import world_to_camera_view as w2c

FT = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from cpl_people import person_mesh

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP033_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-build53-r18b_cp033slope.blend')
STATE = 'SY-BUILD_c1853_slope_works'
RNG = random.Random(1853033)
sc = bpy.context.scene
CAM = bpy.data.objects['CAM_CP033_slope_up_35mm']
COLL = 'SY53_slope_works__autumn1853'
col = bpy.data.collections.get(COLL) or bpy.data.collections.new(COLL)
if col.name not in [c.name for c in sc.collection.children]: sc.collection.children.link(col)
col['cp_state'] = STATE
col['evidence'] = ('terrace/walk dims R (1854 guide); ~1000 labourers on ground works R (1853 press); barrow runs/carts/levels R-typical '
                   '(Delamotte 1852-54); positions, counts, colours I; lower-terrace wall progress autumn 1853 U')
INFO = {}

def link(o):
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o['cp_state'] = STATE; return o

HIDDEN = []
def hide(o):
    o.hide_render = True; o.hide_viewport = True; o['cp033_hidden_by_candidate'] = True; HIDDEN.append(o.name)

# ------------------------------------------------------------------ camera frame helpers
cl = CAM.location.copy()
fwd = CAM.matrix_world.to_quaternion() @ Vector((0, 0, -1)); fwd.z = 0; fwd.normalize()
right = Vector((fwd.y, -fwd.x, 0))
def at(d, lat): p = cl + fwd * d + right * lat; return p.x, p.y
def inview(p, m=0.0):
    v = w2c(sc, CAM, Vector(p)); return v.z > 0 and -m < v.x < 1 + m and -m < v.y < 1 + m
GROUND = [bpy.data.objects[n] for n in ('park_slope', 'terrain', 'terrace_gravel')] + \
         [o for o in bpy.data.objects if o.name.startswith('central_walk')]
def ground(x, y, objs=None):
    best = None
    for g in (objs or GROUND):
        if g.hide_render: continue
        mi = g.matrix_world.inverted(); o_ = mi @ Vector((x, y, 300.0)); d_ = (mi.to_3x3() @ Vector((0, 0, -1))).normalized()
        hit, loc, nrm, idx = g.ray_cast(o_, d_)
        if hit:
            z = (g.matrix_world @ loc).z; best = z if best is None else max(best, z)
    return best
SLOPE = [bpy.data.objects['park_slope']]

# ------------------------------------------------------------------ materials
def nmat(name, c0, c1, scale=6.0, rough=0.9, bump=0.15, detail=6.0, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    b = N['Principled BSDF']; tc = N.new('ShaderNodeTexCoord'); nz = N.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = detail; L.new(tc.outputs['Object'], nz.inputs['Vector'])
    rp = N.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = (*c0, 1); rp.color_ramp.elements[1].color = (*c1, 1)
    rp.color_ramp.elements[0].position = 0.3; rp.color_ramp.elements[1].position = 0.72
    L.new(nz.outputs['Fac'], rp.inputs[0]); L.new(rp.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if rough >= 0.9: b.inputs['Specular IOR Level'].default_value = 0.15
    if bump:
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; L.new(nz.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs[0], b.inputs['Normal'])
    m.diffuse_color = (*c1, 1); return m

def ground_mat():
    """worked London clay + rough pasture + wet trodden track, masks from float attributes grass/track/wet"""
    m = bpy.data.materials.new('cp033_slope_ground_1853'); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    b = N['Principled BSDF']; tc = N.new('ShaderNodeTexCoord')
    def noi(scale, det=6.0, rough=0.55):
        n = N.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = scale; n.inputs['Detail'].default_value = det
        n.inputs['Roughness'].default_value = rough; L.new(tc.outputs['Object'], n.inputs['Vector']); return n
    def ramp(fac, pts):
        r = N.new('ShaderNodeValToRGB'); E = r.color_ramp.elements
        E[0].position, E[0].color = pts[0][0], (*pts[0][1], 1); E[1].position, E[1].color = pts[-1][0], (*pts[-1][1], 1)
        for p, c in pts[1:-1]: e = E.new(p); e.color = (*c, 1)
        L.new(fac, r.inputs[0]); return r
    def attr(nm):
        a = N.new('ShaderNodeAttribute'); a.attribute_name = nm; a.attribute_type = 'GEOMETRY'; return a.outputs['Fac']
    def mix(fac, a, bb):
        x = N.new('ShaderNodeMix'); x.data_type = 'RGBA'; L.new(fac, x.inputs['Factor'])
        L.new(a, x.inputs[6]); L.new(bb, x.inputs[7]); return x.outputs[2]
    n1 = noi(0.18, 4.0); n2 = noi(1.6, 8.0, 0.62); n3 = noi(9.0, 4.0)
    clay = ramp(n1.outputs['Fac'], [(0.30, (0.072, 0.047, 0.026)), (0.52, (0.108, 0.072, 0.040)), (0.72, (0.150, 0.106, 0.060))])
    clay2 = ramp(n2.outputs['Fac'], [(0.35, (0.60, 0.60, 0.60)), (0.65, (1.0, 1.0, 1.0))])
    cm = N.new('ShaderNodeMix'); cm.data_type = 'RGBA'; cm.blend_type = 'MULTIPLY'; cm.inputs['Factor'].default_value = 0.4
    L.new(clay.outputs[0], cm.inputs[6]); L.new(clay2.outputs[0], cm.inputs[7])
    grass = ramp(n2.outputs['Fac'], [(0.30, (0.042, 0.055, 0.018)), (0.55, (0.085, 0.098, 0.034)), (0.75, (0.135, 0.125, 0.055))])
    track = ramp(n3.outputs['Fac'], [(0.35, (0.042, 0.030, 0.019)), (0.70, (0.068, 0.048, 0.030))])
    wet = ramp(n3.outputs['Fac'], [(0.4, (0.040, 0.031, 0.022)), (0.7, (0.058, 0.044, 0.030))])
    # grass mask sharpened with fine noise so the sward edge breaks up
    gm = N.new('ShaderNodeMath'); gm.operation = 'MULTIPLY_ADD'; L.new(attr('grass'), gm.inputs[0]); gm.inputs[1].default_value = 1.6
    gn = N.new('ShaderNodeMath'); gn.operation = 'SUBTRACT'; L.new(n2.outputs['Fac'], gn.inputs[0]); gn.inputs[1].default_value = 0.5
    L.new(gn.outputs[0], gm.inputs[2])
    gc = N.new('ShaderNodeClamp'); L.new(gm.outputs[0], gc.inputs[0])
    gs = N.new('ShaderNodeMapRange'); gs.inputs['From Min'].default_value = 0.35; gs.inputs['From Max'].default_value = 0.65; L.new(gc.outputs[0], gs.inputs['Value'])
    c = mix(gs.outputs['Result'], cm.outputs[2], grass.outputs[0])
    c = mix(attr('track'), c, track.outputs[0])
    c = mix(attr('wet'), c, wet.outputs[0])
    L.new(c, b.inputs['Base Color'])
    rr = N.new('ShaderNodeMath'); rr.operation = 'MULTIPLY_ADD'; L.new(attr('wet'), rr.inputs[0]); rr.inputs[1].default_value = -0.35; rr.inputs[2].default_value = 0.93
    L.new(rr.outputs[0], b.inputs['Roughness'])
    # grazing-angle sky sheen made the dry clay read lavender-grey: dry earth has little specular (wet patches keep theirs)
    sp = N.new('ShaderNodeMath'); sp.operation = 'MULTIPLY_ADD'; L.new(attr('wet'), sp.inputs[0]); sp.inputs[1].default_value = 0.4; sp.inputs[2].default_value = 0.12
    L.new(sp.outputs[0], b.inputs['Specular IOR Level'])
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.35; bp.inputs['Distance'].default_value = 0.05
    hb = N.new('ShaderNodeMath'); hb.operation = 'ADD'; L.new(n3.outputs['Fac'], hb.inputs[0]); L.new(n2.outputs['Fac'], hb.inputs[1])
    L.new(hb.outputs[0], bp.inputs['Height']); L.new(bp.outputs[0], b.inputs['Normal'])
    m.diffuse_color = (0.28, 0.19, 0.10, 1); return m

M = dict(
    ground=ground_mat(),
    spoil=nmat('cp033_spoil_1853', (0.15, 0.10, 0.055), (0.31, 0.225, 0.125), 1.2, 0.95, 0.4),
    plank=nmat('cp033_planks', (0.20, 0.15, 0.10), (0.34, 0.27, 0.19), 3.0, 0.85, 0.1),
    deal=nmat('cp033_deal_poles', (0.30, 0.22, 0.14), (0.46, 0.36, 0.24), 4.0, 0.8, 0.05),
    iron=nmat('cp033_iron', (0.03, 0.03, 0.03), (0.07, 0.065, 0.06), 6.0, 0.55, 0.05, metal=0.6),
    brick=nmat('cp033_stock_brick', (0.17, 0.095, 0.055), (0.29, 0.18, 0.105), 14.0, 0.9, 0.2),
    mortar=nmat('cp033_mortar', (0.50, 0.48, 0.43), (0.62, 0.60, 0.55), 8.0, 0.95, 0.1),
    bathstone=nmat('cp033_bath_stone', (0.55, 0.48, 0.36), (0.68, 0.61, 0.47), 3.0, 0.85, 0.1),
    horse=nmat('cp033_horse_bay', (0.06, 0.03, 0.017), (0.11, 0.06, 0.03), 2.0, 0.5, 0.05),
    horsedk=nmat('cp033_horse_dark', (0.02, 0.016, 0.014), (0.035, 0.028, 0.022), 2.0, 0.6, 0.0),
    harness=nmat('cp033_harness', (0.025, 0.018, 0.012), (0.05, 0.035, 0.022), 4.0, 0.45, 0.0),
    cart=nmat('cp033_cart_red', (0.16, 0.05, 0.03), (0.26, 0.09, 0.05), 3.0, 0.75, 0.05),
    paintR=nmat('cp033_pole_red', (0.35, 0.03, 0.02), (0.45, 0.05, 0.03), 3.0, 0.6, 0.0),
    paintW=nmat('cp033_pole_white', (0.62, 0.60, 0.55), (0.75, 0.73, 0.68), 3.0, 0.6, 0.0),
    brass=nmat('cp033_brass', (0.35, 0.24, 0.08), (0.5, 0.36, 0.12), 3.0, 0.35, 0.0, metal=0.9),
    tar=nmat('cp033_tarred_board', (0.035, 0.03, 0.025), (0.07, 0.06, 0.05), 3.0, 0.8, 0.1),
)
ML = list(M.values()); IX = {k: i for i, k in enumerate(M)}

class Kit:
    """bmesh builder, inputs in METRES (local coords); +x forward for vehicles/animals"""
    def __init__(s): s.bm = bmesh.new()
    def _t(s, k, n0):
        s.bm.faces.ensure_lookup_table()
        for j in range(n0, len(s.bm.faces)): s.bm.faces[j].material_index = IX[k]
    def box(s, k, x0, x1, y0, y1, z0, z1):
        n0 = len(s.bm.faces); vs = [s.bm.verts.new(p) for p in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]]
        for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]: s.bm.faces.new([vs[j] for j in f])
        s._t(k, n0)
    def bar(s, k, a, b, w, t=None):
        t = t or w; A = Vector(a); B = Vector(b); d = B - A
        if d.length < 1e-6: return
        d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0)); sd = d.cross(up).normalized(); u = sd.cross(d).normalized()
        n0 = len(s.bm.faces); pts = [s.bm.verts.new(p + sd * (i * w / 2) + u * (j * t / 2)) for p in (A, B) for (i, j) in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        for f in [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]: s.bm.faces.new([pts[j] for j in f])
        s._t(k, n0)
    def cyl(s, k, a, b, r, seg=10, cap=True, r2=None):
        A = Vector(a); B = Vector(b); d = B - A
        if d.length < 1e-6: return
        d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0)); u = d.cross(up).normalized(); w = u.cross(d).normalized()
        n0 = len(s.bm.faces); r2 = r if r2 is None else r2
        ra = [s.bm.verts.new(A + (u * math.cos(2 * math.pi * j / seg) + w * math.sin(2 * math.pi * j / seg)) * r) for j in range(seg)]
        rb = [s.bm.verts.new(B + (u * math.cos(2 * math.pi * j / seg) + w * math.sin(2 * math.pi * j / seg)) * r2) for j in range(seg)]
        for j in range(seg): s.bm.faces.new([ra[j], ra[(j + 1) % seg], rb[(j + 1) % seg], rb[j]])
        if cap: s.bm.faces.new(list(reversed(ra))); s.bm.faces.new(rb)
        s._t(k, n0)
    def ell(s, k, c, radii, rot=(0, 0, 0), seg=12, rings=8):
        n0 = len(s.bm.faces)
        mat = Matrix.Translation(Vector(c)) @ Matrix.Rotation(rot[2], 4, 'Z') @ Matrix.Rotation(rot[1], 4, 'Y') @ Matrix.Rotation(rot[0], 4, 'X') @ Matrix.Diagonal((*radii, 1))
        bmesh.ops.create_uvsphere(s.bm, u_segments=seg, v_segments=rings, radius=1.0, matrix=mat); s._t(k, n0)
    def wheel(s, k, c, r, w=0.09, rim=0.07, spokes=12):
        C_ = Vector(c); u = Vector((0, 0, 1)); v = Vector((1, 0, 0)); n = 24
        pts = [C_ + (u * math.cos(2 * math.pi * j / n) + v * math.sin(2 * math.pi * j / n)) * (r - rim / 2) for j in range(n + 1)]
        for p, q in zip(pts, pts[1:]): s.bar(k, tuple(p), tuple(q), rim, w)
        for j in range(spokes):
            a = 2 * math.pi * j / spokes; s.bar(k, tuple(C_), tuple(C_ + (u * math.cos(a) + v * math.sin(a)) * (r - rim)), 0.035)
        s.cyl(k, tuple(C_ - Vector((0, w * 1.6, 0))), tuple(C_ + Vector((0, w * 1.6, 0))), r * 0.16, 10)
    def done(s, name, loc=(0, 0, 0), rz=0.0, smooth=False):
        me = bpy.data.meshes.new(name); s.bm.normal_update(); s.bm.to_mesh(me); s.bm.free()
        for m in ML: me.materials.append(m)
        if smooth:
            for p in me.polygons: p.use_smooth = True
        ob = bpy.data.objects.new(name, me); ob.location = loc; ob.rotation_euler = (0, 0, rz); col.objects.link(ob); ob['cp_state'] = STATE
        return ob

# ------------------------------------------------------------------ 1. works ground overlay (polar grid in the CP033 frustum)
TRACKS = []   # polylines (x, y) of cart tracks, wheel gauge 1.5 m (~5 ft, I)
TRACKS.append([at(9, -3.0), at(30, -1.0), at(60, 2.5), at(95, 3.0), at(128, 0.5)])        # T1 up the slope to the tip heap
TRACKS.append([at(14, 22.0), at(40, 18.0), at(80, 12.0), at(118, 6.0)])                   # T2 from the right, joining T1
WETS = [(at(33, 0.2), 2.2), (at(52, 1.8), 1.6), (at(44, 16.5), 1.5), (at(76, 11.5), 1.8)]
GANG = (at(24, -9.0), 7.5)            # foreground bank cutting (centre, radius)
CUTC = at(20.5, -9.0)                   # centre of the fresh cut strip (gang stands either side)
HEAP_C = Vector((55.2, -219.4))
def seg_dist(p, a, b):
    ab = (b - a); t = max(0.0, min(1.0, (p - a).dot(ab) / max(ab.length_squared, 1e-9))); return (p - (a + ab * t)).length, t
def track_info(x, y):
    p = Vector((x, y)); best = (1e9, None)
    for tr in TRACKS:
        for a, b in zip(tr, tr[1:]):
            a = Vector(a); b = Vector(b); d, t = seg_dist(p, a, b)
            if d < best[0]:
                n = (b - a).normalized(); side = (p - a).cross(n) if hasattr(p, 'cross') else 0
                best = (d, ((p - a).x * n.y - (p - a).y * n.x))
    return best
# existing r18 dress pieces (sleepers, baulks, puddles, benches...) keep their look: the overlay dips under their OBB footprints
DRESS = []
for o in bpy.data.collections['SY_BUILD53_dress_r18'].objects:
    if o.type != 'MESH' or o.hide_render: continue
    mi = o.matrix_world.inverted(); bb = o.bound_box
    lo = Vector((min(c[0] for c in bb), min(c[1] for c in bb))); hi = Vector((max(c[0] for c in bb), max(c[1] for c in bb)))
    DRESS.append((o.matrix_world.translation.xy.copy(), max(o.dimensions.x, o.dimensions.y) + 1.0, mi, lo, hi))
def under_dress(x, y):
    p = Vector((x, y))
    for (c, r, mi, lo, hi) in DRESS:
        if (p - c).length > r: continue
        q = mi @ Vector((x, y, (mi.inverted()).translation.z))
        if lo.x - 0.05 <= q.x <= hi.x + 0.05 and lo.y - 0.05 <= q.y <= hi.y + 0.05: return True
    return False
bm = bmesh.new(); la_g = bm.verts.layers.float.new('grass'); la_t = bm.verts.layers.float.new('track'); la_w = bm.verts.layers.float.new('wet')
DS = []; d = 7.0
while d < 150: DS.append(d); d *= 1.011
NA = 240; A0 = math.radians(-33); A1 = math.radians(33)
rows = []
for d in DS:
    row = []
    for j in range(NA + 1):
        a = A0 + (A1 - A0) * j / NA
        dirv = fwd * math.cos(a) + right * math.sin(a)
        p = cl + dirv * d; x, y = p.x, p.y
        if y > -196.2: row.append(None); continue
        z = ground(x, y, SLOPE)
        if z is None: row.append(None); continue
        # micro relief: broad swells + fine clods
        h = 0.06 * noise.noise(Vector((x * 0.05, y * 0.05, 0.3))) + 0.025 * noise.noise(Vector((x * 0.6, y * 0.6, 1.7)))
        td, side = track_info(x, y)
        tr = max(0.0, 1.0 - td / 2.6)
        for g in (-0.75, 0.75):                                    # wheel ruts
            r_ = abs(side - g); h -= 0.07 * max(0.0, 1.0 - r_ / 0.16)
        h -= 0.02 * tr
        wet = 0.0
        for (wc, wr) in WETS:
            dd = (Vector((x, y)) - Vector(wc)).length; wet = max(wet, max(0.0, min(1.0, (wr - dd) / 0.6)))
        h -= 0.03 * wet
        gd = (Vector((x, y)) - Vector(GANG[0])).length
        cv = Vector((x, y)) - Vector(CUTC); cu = abs(cv.dot(right.xy)); cf = cv.dot(fwd.xy)
        if cu < 7.5 and -0.9 < cf < 0.9:                            # the fresh cut the gang is digging (0.3 m, I)
            k_ = min(1.0, (7.5 - cu) / 0.6) * min(1.0, (0.9 - abs(cf)) / 0.3); h -= 0.1 * k_; tr = max(tr, 0.85 * k_)
        dh = (Vector((x, y)) - HEAP_C).length
        # remnant pasture: away from tracks, heap, gang cut and the central works lane; denser to the sides (I)
        lat = abs(math.degrees(a))
        g = 0.5 + 0.5 * noise.noise(Vector((x * 0.035, y * 0.035, 5.0)))
        g = g * (0.55 + 0.6 * min(1.0, max(0.0, (lat - 6) / 18.0)))
        g *= min(1.0, td / 7.0) * min(1.0, max(0.0, (gd - 9) / 6.0)) * min(1.0, max(0.0, (dh - 26) / 10.0))
        if d > 120: g *= max(0.0, (140 - d) / 20.0)
        h = max(h, -0.10)                                          # never cut below park_slope (+0.12 base)
        if under_dress(x, y): h = -0.16                          # 4 cm below park_slope under existing dress
        v = bm.verts.new((x, y, z + 0.12 + h)); v[la_g] = max(0.0, min(1.0, g)); v[la_t] = min(1.0, tr * 1.2); v[la_w] = wet
        row.append(v)
    rows.append(row)
for r0, r1 in zip(rows, rows[1:]):
    for j in range(NA):
        q = (r0[j], r0[j + 1], r1[j + 1], r1[j])
        if all(q): bm.faces.new(q)
for v in [v for v in bm.verts if not v.link_faces]: bm.verts.remove(v)
me = bpy.data.meshes.new('cp033_slope_works_ground'); bm.to_mesh(me); bm.free(); me.materials.append(M['ground'])
for p in me.polygons: p.use_smooth = True
og = bpy.data.objects.new('cp033_slope_works_ground', me); col.objects.link(og); og['cp_state'] = STATE
INFO['ground_faces'] = len(me.polygons)

# ------------------------------------------------------------------ 2. centre cone heap -> irregular tip heap
def mesh_copy_drop_island(name, centre, radius):
    o = bpy.data.objects[name]; me_ = o.data.copy(); me_.name = name + '_cp033'
    b = bmesh.new(); b.from_mesh(me_); mw = o.matrix_world
    kill = [f for f in b.faces if ((mw @ f.calc_center_median()).xy - centre).length < radius]; n = len(kill)
    bmesh.ops.delete(b, geom=kill, context='FACES'); b.to_mesh(me_); b.free()
    no = bpy.data.objects.new(name + '_cp033', me_); no.matrix_world = mw.copy()
    for c in o.users_collection: c.objects.link(no)
    no['cp_state'] = o.get('cp_state', ''); no['cp033_mesh_copy_of'] = name
    hide(o); return n
INFO['heap_faces_dropped'] = mesh_copy_drop_island('earth_spoil_heaps_cuttings', HEAP_C, 21.0)

def tip_heap(name, cx, cy, L_, W_, H_, rz, seed):
    """elongated spoil tip: flat-ish top, steep tipping face at the +x end, base sunk 0.5 m into the slope"""
    r = random.Random(seed); b = bmesh.new(); NU, NV = 64, 26; grid = []
    ca, sa = math.cos(rz), math.sin(rz)
    for i in range(NV + 1):
        rr_ = i / NV; ring = []
        for j in range(NU):
            t = 2 * math.pi * j / NU
            ex = math.cos(t); ey = math.sin(t)
            sq = (abs(ex) ** 0.6) * (1 if ex >= 0 else -1), (abs(ey) ** 0.8) * (1 if ey >= 0 else -1)
            lx = sq[0] * L_ / 2 * rr_; ly = sq[1] * W_ / 2 * rr_
            wob = 1.0 + 0.12 * noise.noise(Vector((ex * 2.1 + seed, ey * 2.1, 0.5)))
            lx *= wob; ly *= wob
            x = cx + lx * ca - ly * sa; y = cy + lx * sa + ly * ca
            gz = ground(x, y, SLOPE) or -15.0
            prof = 1.0 - rr_ ** 3.2 if ex < 0.4 else 1.0 - rr_ ** 6.0      # tipping face (+x end) steeper
            z = gz - 0.5 + (H_ + 0.5) * prof + 0.35 * noise.noise(Vector((x * 0.4, y * 0.4, 2.0))) * (1 - rr_ ** 4)
            ring.append(b.verts.new((x, y, z)))
        grid.append(ring)
    top = b.verts.new((cx, cy, (ground(cx, cy, SLOPE) or -15.0) + H_))
    for j in range(NU): b.faces.new((top, grid[0][(j + 1) % NU], grid[0][j])) if False else None
    for i in range(NV):
        for j in range(NU): b.faces.new((grid[i][j], grid[i][(j + 1) % NU], grid[i + 1][(j + 1) % NU], grid[i + 1][j]))
    bmesh.ops.remove_doubles(b, verts=grid[0], dist=0.05); b.verts.remove(top)
    me_ = bpy.data.meshes.new(name); b.to_mesh(me_); b.free(); me_.materials.append(M['spoil'])
    for p in me_.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me_); col.objects.link(o); o['cp_state'] = STATE; return o
# the replaced island was 40.6 m across, 6.4 m high (a squat cone); the new tip is 34 x 20 m, 4.2 m high, tipping toward the lens (I)
hrz = math.atan2(-fwd.y, -fwd.x)
tip_heap('cp033_tip_heap_centre', HEAP_C.x, HEAP_C.y, 34.0, 20.0, 4.2, hrz + 0.25, 7)
tip_heap('cp033_tip_heap_small', HEAP_C.x + 26, HEAP_C.y - 6, 14.0, 9.0, 2.2, hrz - 0.4, 11)
# plank barrow runs: lens side of the heap up to its top (Delamotte: barrow and plank, R-typical)
kp = Kit()
def plank_run(p0, p1, z0, z1, w=0.3):
    a = Vector((*p0, z0)); bb = Vector((*p1, z1)); kp.bar('plank', a, bb, w, 0.06)
    n = int((bb - a).length / 3.2)
    for i in range(1, n):                                           # trestles under the run
        q = a.lerp(bb, i / n); gz = ground(q.x, q.y) or q.z
        if q.z - gz > 0.25: kp.bar('deal', (q.x, q.y, gz), (q.x, q.y, q.z - 0.03), 0.09)
for (u0, u1) in ((-15.0, -4.0), (14.0, 5.0)):                          # two runs climbing the lens-side flank diagonally
    e_ = HEAP_C - fwd.xy * 12.5 + right.xy * u0; s_ = HEAP_C - fwd.xy * 4.5 + right.xy * u1
    ze = (ground(e_.x, e_.y, SLOPE) or -16) + 0.14; zt = (ground(s_.x, s_.y, SLOPE) or -15) + 3.4
    kp.bar('plank', (e_.x, e_.y, ze), (s_.x, s_.y, zt), 0.3, 0.06)
    for i in range(1, 5):
        q = e_.lerp(s_, i / 5); gz = ground(q.x, q.y, SLOPE) or -16
        kp.bar('deal', (q.x, q.y, gz - 0.2), (q.x, q.y, ze + (zt - ze) * i / 5 - 0.04), 0.1)
kp.done('cp033_barrow_plank_runs')

# ------------------------------------------------------------------ 3a. tools, barrows, carts, horses (local metres)
def barrow(name, x, y, rz, load=True):
    k = Kit(); z = ground(x, y) or 0
    k.box('plank', -0.15, 0.75, -0.30, 0.30, 0.30, 0.34); k.box('plank', -0.15, 0.75, -0.32, -0.28, 0.34, 0.62)
    k.box('plank', -0.15, 0.75, 0.28, 0.32, 0.34, 0.62); k.box('plank', 0.72, 0.78, -0.32, 0.32, 0.30, 0.62)
    for sgn in (-1, 1): k.bar('deal', (-1.05, sgn * 0.27, 0.55), (0.95, sgn * 0.22, 0.22), 0.05)
    k.wheel('iron', (1.0, 0, 0.22), 0.22, 0.04, 0.04, 8)
    for sgn in (-1, 1): k.bar('deal', (-0.05, sgn * 0.25, 0.30), (-0.05, sgn * 0.25, 0.0), 0.05)
    if load: k.ell('spoil', (0.30, 0, 0.6), (0.42, 0.27, 0.14))
    return k.done(name, (x, y, z), rz)
def shovel_for(fig_xy, z, rz, kind, seed):
    """a shovel or pick held in front of a 'working' figure (figure faces local -y)"""
    r = random.Random(seed); k = Kit()
    if kind == 'shovel':
        k.bar('deal', (0.18, -0.35, 0.95), (0.22, -0.95, 0.12), 0.035); k.box('iron', 0.1, 0.34, -1.12, -0.92, 0.0, 0.03)
    else:
        k.bar('deal', (0.12, -0.25, 1.15), (0.15, -0.85, 1.55), 0.04); k.bar('iron', (-0.15, -0.88, 1.6), (0.45, -0.82, 1.45), 0.04)
    return k.done(f'cp033_tool_{seed}', (fig_xy[0], fig_xy[1], z), rz)
def horse(name, x, y, heading, stride=0.0, dark=False):
    """~16 hands draught horse (port of the CP002 LN2 horse, feet -> metres), local +x forward"""
    k = Kit(); F = FT; mb = 'horsedk' if dark else 'horse'
    def e(c, r, rot=(0, 0, 0)): k.ell(mb, tuple(v * F for v in c), tuple(v * F for v in r), rot)
    def tube(mat, pts, seg=10):
        for a, b in zip(pts, pts[1:]): k.cyl(mat, tuple(v * F for v in a[:3]), tuple(v * F for v in b[:3]), a[3] * F, seg, True, b[3] * F)
    e((0, 0, 4.25), (3.3, 1.35, 1.45)); e((2.3, 0, 4.55), (1.5, 1.3, 1.5)); e((-2.4, 0, 4.6), (1.4, 1.35, 1.35))
    tube(mb, [(2.4, 0, 4.9, 1.1), (3.2, 0, 5.9, 0.9), (3.85, 0, 6.75, 0.64), (4.2, 0, 7.15, 0.5)], 12)
    tube(mb, [(4.22, 0, 7.22, 0.47), (4.75, 0, 6.6, 0.42), (5.3, 0, 5.95, 0.33), (5.58, 0, 5.62, 0.29)], 10)
    e((4.45, 0, 6.72), (0.62, 0.46, 0.55), (0, math.radians(-40), 0)); e((5.5, 0, 5.66), (0.36, 0.33, 0.33))
    tube('horsedk', [(2.5, 0, 6.05, 0.16), (3.35, 0, 6.85, 0.2), (4.1, 0, 7.6, 0.16)], 6)
    for ex in (-0.24, 0.24): k.cyl(mb, (4.18 * F, ex * F, 7.5 * F), (4.02 * F, ex * 1.25 * F, 8.12 * F), 0.13 * F, 6, True, 0.02 * F)
    cc_ = Vector((2.95, 0, 5.55)); Nn = Vector((-0.78, 0, 0.62)); Yy = Vector((0, 1, 0)); ring = []
    for j in range(17):
        a_ = 2 * math.pi * j / 16; ring.append(cc_ + Yy * (math.cos(a_) * 1.18) + Nn * (math.sin(a_) * 1.42))
    for p0, p1 in zip(ring, ring[1:]): k.cyl('harness', tuple(p0 * F), tuple(p1 * F), 0.3 * F, 8)
    for ex in (-0.45, 0.45): k.cyl('brass', (2.5 * F, ex * F, 6.6 * F), (2.35 * F, ex * 1.1 * F, 7.25 * F), 0.09 * F, 6, True, 0.12 * F)
    tube('horsedk', [(-3.6, 0, 5.0, 0.28), (-4.1, 0, 3.6, 0.32), (-4.0, 0, 2.2, 0.2)], 8)
    for (lx, ly, front, ph) in ((2.3, 0.65, True, 0.0), (2.0, -0.65, True, 1.0), (-2.5, 0.65, False, 1.0), (-2.8, -0.65, False, 0.0)):
        sw = stride * (1 if ph else -1)
        if front: pts = [(lx, ly, 3.6, 0.42), (lx + 0.05 + sw * 0.3, ly, 2.2, 0.26), (lx + sw * 0.6, ly, 0.9, 0.2), (lx + sw * 0.7, ly, 0.35, 0.28)]
        else: pts = [(lx, ly, 3.7, 0.5), (lx - 0.45 + sw * 0.2, ly, 2.4, 0.3), (lx - 0.1 + sw * 0.5, ly, 1.0, 0.2), (lx + sw * 0.6, ly, 0.35, 0.28)]
        tube(mb, pts, 8); k.cyl('horsedk', (pts[-1][0] * F, ly * F, 0.0), (pts[-1][0] * F, ly * F, 0.55 * F), 0.38 * F, 8, True, 0.33 * F)
    k.box('harness', -0.6 * F, 0.4 * F, -1.42 * F, 1.42 * F, 5.45 * F, 5.75 * F)
    for sg in (-1, 1):
        k.bar('harness', (-3.4 * F, sg * 1.36 * F, 4.4 * F), (0.0, sg * 1.42 * F, 4.3 * F), 0.2 * F, 0.06 * F)
        k.bar('harness', (2.2 * F, sg * 1.25 * F, 4.6 * F), (-1.0 * F, sg * 1.42 * F, 4.6 * F), 0.18 * F, 0.05 * F)
    z = ground(x, y) or 0
    return k.done(name, (x, y, z), heading, smooth=True)
def tip_cart(name, x, y, heading, tipped=0.0):
    """two-wheeled earth (tip) cart ~6 ft x 4 ft 6 in body, 5 ft wheels, shafts forward (+x), clay load (I)"""
    k = Kit(); F = FT
    body = Kit()
    k.box('cart', -6.2 * F, 0.0, -2.3 * F, 2.3 * F, 2.4 * F, 2.6 * F)
    for sg in (-1, 1): k.box('cart', -6.2 * F, 0.0, sg * 2.3 * F - 0.04, sg * 2.3 * F + 0.04, 2.6 * F, 4.2 * F)
    k.box('cart', -6.25 * F, -6.15 * F, -2.3 * F, 2.3 * F, 2.6 * F, 4.1 * F); k.box('cart', -0.05, 0.05, -2.3 * F, 2.3 * F, 2.6 * F, 4.6 * F)
    k.ell('spoil', (-3.1 * F, 0, 4.0 * F), (2.9 * F, 2.1 * F, 0.9 * F))
    for sg in (-1, 1): k.wheel('cart', (-3.0 * F, sg * 2.75 * F, 2.5 * F), 2.5 * F, 0.1, 0.08, 12)
    k.cyl('iron', (-3.0 * F, -2.9 * F, 2.5 * F), (-3.0 * F, 2.9 * F, 2.5 * F), 0.06, 8)
    for sg in (-1, 1): k.bar('deal', (0.0, sg * 1.45 * F, 3.0 * F), (8.0 * F, sg * 1.45 * F, 4.2 * F), 0.09, 0.09)
    z = ground(x, y) or 0
    return k.done(name, (x, y, z), heading)

people = []
def put_person(name, role, pose, x, y, rz, seed, lod='mid', zfix=None):
    z = ground(x, y) if zfix is None else zfix
    if z is None: return None
    z2 = ground(x, y, [og])
    if z2 is not None: z = max(z, z2)
    person_mesh(name, role, style={'role': role, 'pose': pose, 'lod': lod, 'era': '1850s'}, seed=seed)
    o = bpy.data.objects[name]; link(o); o.location = (x, y, z); o.rotation_euler = (0, 0, rz)
    o['cpl_people'] = 'cpl_people_v3'; people.append(o); return o
def face(x, y, tx, ty): return math.atan2(tx - x, -(ty - y)) + math.pi      # local -y toward (tx, ty)

# foreground gang cutting the bank (centre-left, 18-31 m): 7 navvies, shovels/picks, 2 barrows on a plank
gx, gy = GANG[0]
gang = [(-3.0, -4.0, 'working', 'shovel'), (-1.2, -2.6, 'working', 'pick'), (0.8, -3.4, 'working', 'shovel'), (2.6, -2.0, 'working', 'shovel'),
        (-2.0, 1.0, 'working', 'pick'), (3.8, 1.5, 'standing', None), (1.0, 3.6, 'hauling', None)]
for i, (dx, dy, pose, tool) in enumerate(gang):
    x = gx + right.x * dx + fwd.x * dy; y = gy + right.y * dx + fwd.y * dy
    rz = face(x, y, gx + right.x * dx * 0.3 - fwd.x * 6, gy + right.y * dx * 0.3 - fwd.y * 6) + RNG.uniform(-0.5, 0.5)
    o = put_person(f'cp033_gang_navvy_{i}', '1850s_navvy', pose, x, y, rz, 1853100 + i * 7)
    if o and tool: link(shovel_for((x, y), o.location.z, rz, tool, 1853100 + i * 7))
# the cut itself: a shallow trench strip with a clay ridge (spoil cast up-slope)
bb_ = bmesh.new(); rowsb = []; c0 = Vector(CUTC) + fwd.xy * 1.9       # thrown-up clay berm on the up-slope lip of the cut
for i in range(41):
    u = -7.8 + 15.6 * i / 40; ring = []
    for j in range(9):
        w = -1.3 + 2.6 * j / 8; q = c0 + right.xy * u + fwd.xy * w; z = ground(q.x, q.y, SLOPE) or 0
        hh = 0.55 * max(0.0, 1 - (w / 1.3) ** 2) * min(1.0, (7.8 - abs(u)) / 1.2) * (0.8 + 0.4 * noise.noise(Vector((q.x * 0.7, q.y * 0.7, 3.3))))
        ring.append(bb_.verts.new((q.x, q.y, z - 0.05 + hh + 0.06 * noise.noise(Vector((q.x * 3, q.y * 3, 1.0))))))
    rowsb.append(ring)
for r0, r1 in zip(rowsb, rowsb[1:]):
    for j in range(8): bb_.faces.new((r0[j], r0[j + 1], r1[j + 1], r1[j]))
meb = bpy.data.meshes.new('cp033_gang_cut_berm'); bb_.to_mesh(meb); bb_.free(); meb.materials.append(M['spoil'])
for p_ in meb.polygons: p_.use_smooth = True
ob_ = bpy.data.objects.new('cp033_gang_cut_berm', meb); col.objects.link(ob_)
barrow('cp033_barrow_gang_0', *at(28.5, -6.0), hrz + math.pi + 0.15)
barrow('cp033_barrow_gang_1', *at(21.0, -13.0), hrz + 0.8, load=False)
bxy = at(29.2, -6.0)
put_person('cp033_barrow_man_0', '1850s_navvy', 'hauling', bxy[0] - fwd.x * 1.3, bxy[1] - fwd.y * 1.3, face(bxy[0], bxy[1], bxy[0] + fwd.x * 5, bxy[1] + fwd.y * 5), 1853171)

# carts: one loading close right (28 m), one climbing T2 (64 m); carters at the horse's head
def cart_team(tag, d, lat, along, stride, dark, seed):
    x, y = at(d, lat); hd = math.atan2(along.y, along.x)
    hx, hy = x + along.x * 1.75, y + along.y * 1.75
    horse(f'cp033_horse_{tag}', hx, hy, hd, stride, dark)
    tip_cart(f'cp033_tipcart_{tag}', x, y, hd)
    cxp = hx + along.x * 1.4 + Vector((-along.y, along.x)).x * 1.2; cyp = hy + along.y * 1.4 + Vector((-along.y, along.x)).y * 1.2
    put_person(f'cp033_carter_{tag}', '1850s_workman', 'walking' if stride else 'standing', cxp, cyp, face(cxp, cyp, cxp + along.x, cyp + along.y), seed)
up_ = (Vector(at(60, 2.5)) - Vector(at(30, -1.0))).normalized()
cart_team('near', 27.0, 7.5, Vector((-right.x, -right.y)) * 0.6 + up_ * 0.4, 0.0, False, 1853201)
up2 = (Vector(at(80, 12.0)) - Vector(at(40, 18.0))).normalized()
cart_team('climb', 61.0, 15.2, up2, 0.35, True, 1853202)
cart_team('heap', 112.0, 3.2, (Vector(at(128, 0.5)) - Vector(at(95, 3.0))).normalized(), 0.3, False, 1853203)
# navvies filling the near cart
nx, ny = at(26.0, 10.5)
for i, (dx, dy) in enumerate(((0.0, 0.0), (1.6, 1.2), (-1.4, 1.8))):
    x = nx + right.x * dx + fwd.x * dy; y = ny + right.y * dx + fwd.y * dy
    tx, ty = at(27.0, 7.5); rz = face(x, y, tx, ty)
    o = put_person(f'cp033_cart_navvy_{i}', '1850s_navvy', 'working', x, y, rz, 1853210 + i)
    if o: link(shovel_for((x, y), o.location.z, rz, 'shovel', 1853210 + i))

# surveyor's level + staff and ranging poles / batter-board profiles stepping up the design gradient (slope cue)
ks = Kit()
sx, sy = at(19.0, 4.0); sz = ground(sx, sy) or 0
for a in (0, 2.1, 4.2):
    ks.bar('deal', (sx, sy, sz + 1.35), (sx + 0.45 * math.cos(a), sy + 0.45 * math.sin(a), sz), 0.035)
ks.cyl('brass', (sx - 0.22, sy, sz + 1.45), (sx + 0.22, sy, sz + 1.45), 0.045, 10); ks.box('deal', sx - 0.08, sx + 0.08, sy - 0.08, sy + 0.08, sz + 1.32, sz + 1.40)
put_person('cp033_surveyor', '1850s_gentleman', 'standing', sx - fwd.x * 0.7 + right.x * 0.15, sy - fwd.y * 0.7 + right.y * 0.15, face(sx, sy, sx + fwd.x, sy + fwd.y), 1853301)
stx, sty = at(47.0, 6.0); stz = ground(stx, sty) or 0
for i in range(14):
    ks.box('paintW' if i % 2 == 0 else 'paintR', stx - 0.05, stx + 0.05, sty - 0.02, sty + 0.02, stz + i * 0.3, stz + (i + 1) * 0.3)
put_person('cp033_staffman', '1850s_workman', 'standing', stx + right.x * 0.45, sty + right.y * 0.45, face(stx, sty, sx, sy), 1853302)
# ranging poles along the line of the future lower-terrace wall and down the central works lane (6 ft 6 in, red/white feet)
for (d, lat) in ((70, -26), (88, -24), (104, -22), (126, -20), (140, 24), (122, 30), (98, 34), (62, -30)):
    x, y = at(d, lat); z = ground(x, y) or 0
    for i in range(4): ks.box('paintR' if i % 2 else 'paintW', x - 0.03, x + 0.03, y - 0.03, y + 0.03, z + i * 0.61, z + (i + 1) * 0.61)
ks.done('cp033_survey_level_staff_poles')

# timber stack + tarred tool hut (mid-left, ~95 m)
kh = Kit(); hx, hy = at(95.0, -28.0); hz_ = ground(hx, hy) or 0
kh.box('tar', -2.4, 2.4, -1.6, 1.6, -0.2, 2.3)
for sg in (-1, 1): kh.bar('tar', (-2.6, sg * 1.75, 2.15), (2.6, sg * 0.0, 2.95), 0.03, 3.3) if False else None
kh.box('tar', -2.6, 2.6, -1.8, 1.8, 2.3, 2.42); kh.box('plank', -0.45, 0.45, -1.62, -1.58, 0.0, 1.9)
kh.done('cp033_tool_hut', (hx, hy, hz_), hrz + math.pi / 2)
kt = Kit(); tx_, ty_ = at(88.0, -18.0); tz_ = ground(tx_, ty_) or 0
for lay in range(5):
    for j in range(6 - lay // 2):
        kt.box('plank', -3.0, 3.0, -1.0 + j * 0.34, -0.72 + j * 0.34, lay * 0.24, lay * 0.24 + 0.22)
kt.done('cp033_timber_stack', (tx_, ty_, tz_), hrz + 0.3)

# ------------------------------------------------------------------ 3b. pv57 navvy points in the frustum -> people_lib figures
pp = bpy.data.objects['ppl53_navvies_erectors']; pme = pp.data.copy(); pme.name = 'ppl53_navvies_erectors_cp033'
mw = pp.matrix_world; drop = []; spots = []
for v in pme.vertices:
    p = mw @ v.co
    if inview(p, 0.03) and (p.xy - cl.xy).length < 430:
        drop.append(v.index)
        if all((p.xy - q.xy).length > 0.9 for q in spots): spots.append(p.copy())
bq = bmesh.new(); bq.from_mesh(pme); bq.verts.ensure_lookup_table()
bmesh.ops.delete(bq, geom=[bq.verts[i] for i in drop], context='VERTS'); bq.to_mesh(pme); bq.free()
pn = bpy.data.objects.new('ppl53_navvies_erectors_cp033', pme); pn.matrix_world = mw.copy()
for c in pp.users_collection: c.objects.link(pn)
for m_ in pp.modifiers:
    nm_ = pn.modifiers.new(m_.name, m_.type)
    if m_.type == 'NODES': nm_.node_group = m_.node_group
    for k_ in m_.keys():
        try: nm_[k_] = m_[k_]
        except Exception: pass
pn['cp033_mesh_copy_of'] = pp.name; hide(pp)
INFO['pv57_points_dropped'] = len(drop); INFO['pv57_spots'] = len(spots)
ns = 0
for i, s in enumerate(spots):
    dd = (s.xy - cl.xy).length
    role = '1850s_workman' if s.y > -112 else ('1850s_navvy' if RNG.random() < 0.8 else '1850s_workman')
    pose = RNG.choice(('working', 'working', 'hauling', 'standing', 'walking'))
    o = put_person(f'cp033_works_{i:03d}', role, pose, s.x, s.y, RNG.uniform(0, 2 * math.pi), 1853400 + i, 'mid' if dd < 140 else 'crowd', zfix=s.z)
    if o: ns += 1
INFO['pv57_replaced'] = ns

# ------------------------------------------------------------------ 4. lower-terrace garden-front wall under construction (x 40..238)
kw = Kit(); YW = -195.6; PIER = 7.3      # alcove bay ~24 ft (I); wall 3 ft thick
x = 41.0; ib = 0
while x < 238.0:
    z = ground(x, YW - 1.0) or -13.6
    prog = 1.0 if x < 80 else max(0.0, 1.0 - (x - 80.0) / 120.0)   # work proceeds north from the finished stone section (I)
    hgt = max(0.4, 3.0 * min(1.0, prog * 1.1 + 0.12 * RNG.random()))
    kw.box('brick', x - 0.45, x + 0.45, YW - 0.5, YW + 0.45, z - 0.3, z + hgt)
    if hgt > 2.6 and x + PIER < 238:                 # alcove arch turned between piers
        for k_ in range(9):
            a0 = math.pi * k_ / 9; a1 = math.pi * (k_ + 1) / 9; r_ = (PIER - 0.9) / 2; cxw = x + PIER / 2
            kw.bar('brick', (cxw - r_ * math.cos(a0), YW, z + 1.9 + r_ * 0.3 * math.sin(a0)), (cxw - r_ * math.cos(a1), YW, z + 1.9 + r_ * 0.3 * math.sin(a1)), 0.5, 0.9)
        kw.box('brick', x + 0.45, x + PIER - 0.45, YW + 0.15, YW + 0.45, z - 0.3, z + 1.9)    # alcove back wall
    elif hgt > 1.2 and x + PIER < 238:
        kw.box('brick', x + 0.45, x + PIER - 0.45, YW + 0.15, YW + 0.45, z - 0.3, z + hgt * 0.6)
    if 1.0 < hgt < 3.3 and ib % 2 == 0:              # pole scaffold on the park face
        for dx in (-0.2, PIER / 2, PIER - 0.6):
            zz = ground(x + dx, YW - 1.8) or z
            kw.bar('deal', (x + dx, YW - 1.8, zz - 0.2), (x + dx, YW - 1.8, z + hgt + 1.4), 0.12)
        kw.bar('deal', (x - 0.4, YW - 1.8, z + hgt - 0.2), (x + PIER, YW - 1.8, z + hgt - 0.2), 0.08)
        kw.box('plank', x - 0.4, x + PIER, YW - 2.2, YW - 1.0, z + hgt - 0.12, z + hgt - 0.06)
    if ib % 3 == 1:                                   # brick stacks and mortar boards on the park side
        zz = ground(x + 2.5, YW - 4.0) or z
        kw.box('brick', x + 1.6, x + 3.4, YW - 4.6, YW - 3.6, zz - 0.05, zz + 1.1)
        kw.box('mortar', x + 4.0, x + 4.9, YW - 3.4, YW - 2.5, zz, zz + 0.12)
    x += PIER; ib += 1
# Bath-stone coping blocks and two shear-legs (derricks) lifting them (Delamotte 'The Terrace Front', R-typical)
for (sx_, h_) in ((62.0, 11.0), (118.0, 10.0)):
    z = ground(sx_, YW - 3.0) or -13.8
    top = Vector((sx_, YW - 0.8, z + h_))
    for (dx, dy) in ((-2.4, -4.5), (2.4, -4.5)):
        kw.cyl('deal', (sx_ + dx, YW + dy, z - 0.3), tuple(top), 0.16, 8, True, 0.11)
    kw.cyl('deal', (sx_, YW + 6.0, z - 0.2), tuple(top), 0.12, 8, True, 0.1)        # back guy/leg
    kw.bar('iron', tuple(top), (sx_, YW - 1.6, z + 2.4), 0.025)                         # fall
    kw.box('bathstone', sx_ - 0.7, sx_ + 0.7, YW - 2.0, YW - 1.2, z + 1.6, z + 2.3)
    for j in range(4):
        zz = ground(sx_ + 4 + j * 1.6, YW - 5.0) or z
        kw.box('bathstone', sx_ + 3.4 + j * 1.6, sx_ + 4.8 + j * 1.6, YW - 5.4, YW - 4.6, zz - 0.05, zz + 0.6)
kw.done('cp033_lower_terrace_wall_works')
for i, (xx, dd) in enumerate(((50.0, 0), (58.0, 1), (66.0, 0), (64.0, 1), (115.0, 0), (121.0, 1), (90.0, 0), (150.0, 1))):
    yy = YW - 2.5 - 1.5 * dd
    put_person(f'cp033_mason_{i}', '1850s_workman', 'working' if i % 3 else 'hauling', xx, yy, face(xx, yy, xx, YW), 1853500 + i)

# ------------------------------------------------------------------ 5. placeholder tree 38 -> elm (CP032 trees.py recipe)
def _tube(b, a, c, ra, rb, seg=8):
    d = (c - a)
    if d.length < 1e-6: return
    d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0))
    s = d.cross(up).normalized(); u = s.cross(d).normalized()
    A = [b.verts.new(a + (s * math.cos(2 * math.pi * k / seg) + u * math.sin(2 * math.pi * k / seg)) * ra) for k in range(seg)]
    B = [b.verts.new(c + (s * math.cos(2 * math.pi * k / seg) + u * math.sin(2 * math.pi * k / seg)) * rb) for k in range(seg)]
    for k in range(seg): b.faces.new([A[k], A[(k + 1) % seg], B[(k + 1) % seg], B[k]])
def leaf_mat():
    m = bpy.data.materials.new('cp033_elm_leaf_autumn1853'); m.use_nodes = True; t = m.node_tree; n = t.nodes; l = t.links; b = n['Principled BSDF']
    ramp = n.new('ShaderNodeValToRGB'); nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.6
    ramp.color_ramp.elements[0].color = (0.040, 0.060, 0.014, 1); ramp.color_ramp.elements[1].color = (0.150, 0.170, 0.040, 1)
    e = ramp.color_ramp.elements.new(0.8); e.color = (0.20, 0.16, 0.04, 1)                 # first autumn yellowing (I)
    l.new(nz.outputs['Fac'], ramp.inputs[0]); l.new(ramp.outputs[0], b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.7
    tc = n.new('ShaderNodeTexCoord'); vor = n.new('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = 3.0; l.new(tc.outputs['UV'], vor.inputs['Vector'])
    lt = n.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.42; l.new(vor.outputs['Distance'], lt.inputs[0]); l.new(lt.outputs[0], b.inputs['Alpha'])
    m.diffuse_color = (0.12, 0.15, 0.04, 1); return m
def build_elm(name, x, y, z0, H, D, CR, seed, bark, leaf, cards_per=150):
    rnd = random.Random(seed); b = bmesh.new(); tips = []
    def branch(p, d, length, radius, depth, wig):
        n = max(2, int(length / 4)); cur = Vector(p); dirv = Vector(d).normalized(); pts = [cur.copy()]
        for i in range(n):
            dirv = (dirv + Vector((rnd.uniform(-wig, wig), rnd.uniform(-wig, wig), rnd.uniform(-wig / 3, wig / 2)))).normalized()
            cur = cur + dirv * (length / n); cur.z = min(cur.z, H - 1.0); pts.append(cur.copy())
        for i, (a, c) in enumerate(zip(pts, pts[1:])):
            _tube(b, a, c, radius * (1 - 0.6 * i / n), radius * (1 - 0.6 * (i + 1) / n), 8 if radius > 0.6 else 5)
        if depth == 0: tips.extend(pts[len(pts) // 2:]); return
        for k in range(4 if depth >= 2 else 3):
            t = rnd.uniform(0.35, 0.95); base = pts[max(1, min(len(pts) - 1, int(round(t * n))))]; ang = rnd.uniform(0, 2 * math.pi)
            nd = (dirv + Vector((math.cos(ang), math.sin(ang), rnd.uniform(0.1, 0.6)))).normalized()
            branch(base, nd, length * rnd.uniform(0.45, 0.62), radius * 0.5, depth - 1, wig * 1.3)
    trunk_h = H * 0.30
    branch((0, 0, -0.5), (0, 0, 1), trunk_h + 0.5, D / 2, 0, 0.03); tips.clear(); top = Vector((0, 0, trunk_h))
    for k in range(5):
        ang = 2 * math.pi * k / 5 + rnd.uniform(-.3, .3); spread = rnd.uniform(0.45, 0.8)
        branch(top, Vector((math.cos(ang) * spread, math.sin(ang) * spread, 1)).normalized(), (H - trunk_h) * rnd.uniform(0.55, 0.7), D * 0.26, 3, 0.10)
    for k in range(6):
        zb = trunk_h * rnd.uniform(0.75, 1.0) + (H - trunk_h) * rnd.uniform(0.0, 0.25); ang = rnd.uniform(0, 2 * math.pi)
        branch(Vector((0, 0, zb)), Vector((math.cos(ang), math.sin(ang), rnd.uniform(0.35, 0.7))).normalized(), CR * rnd.uniform(0.55, 0.8), D * 0.14, 2, 0.12)
    bmesh.ops.scale(b, vec=(FT, FT, FT), verts=b.verts)
    me_ = bpy.data.meshes.new(name + '_wood'); b.to_mesh(me_); b.free(); me_.materials.append(bark)
    for pg in me_.polygons: pg.use_smooth = True
    W = bpy.data.objects.new(name + '_WOOD', me_); W.location = (x, y, z0); col.objects.link(W)
    b = bmesh.new(); uvl = b.loops.layers.uv.new(); zc = trunk_h + (H - trunk_h) * 0.5; hz = (H - trunk_h) * 0.62; cards = 0
    for tp in tips:
        if rnd.random() < 0.05: continue
        c = Vector(tp) + Vector((rnd.uniform(-2, 2), rnd.uniform(-2, 2), rnd.uniform(0, 2.5))); r = rnd.uniform(3.0, 5.0)
        if c.z < H * 0.26: continue
        if math.hypot(c.x, c.y) + r * 0.6 > CR or (c.z - zc) / hz > 1.0 or c.z + r > H: continue
        for j in range(cards_per):
            v = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1))).normalized() * (r * rnd.uniform(0.55, 1.0) ** 0.5); v.z *= 0.75
            q = c + v; nrm = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.3, 1))).normalized()
            t1 = nrm.cross(Vector((0.3, 0.2, 1))).normalized(); t2 = nrm.cross(t1); sz = rnd.uniform(0.45, 0.8) * (150 / cards_per) ** 0.5
            vs = [b.verts.new((q + (t1 * sx + t2 * sy) * sz) * FT) for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            f = b.faces.new(vs)
            for lp, uv in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))): lp[uvl].uv = uv
            cards += 1
    me_ = bpy.data.meshes.new(name + '_leaves'); b.to_mesh(me_); b.free(); me_.materials.append(leaf)
    Lf = bpy.data.objects.new(name + '_LEAVES', me_); Lf.location = W.location; col.objects.link(Lf)
    for o in (W, Lf): o['cp_state'] = STATE
    return W, Lf, cards
for nm in ('PLACEHOLDER_park_tree_38_trunk', 'PLACEHOLDER_park_tree_38_crown'):
    o = bpy.data.objects.get(nm)
    if o: hide(o)
ex, ey = 94.2, -273.8
bark = bpy.data.materials.get('bark') or nmat('cp033_bark', (0.05, 0.04, 0.03), (0.10, 0.08, 0.06), 6.0, 0.9, 0.3)
_, _, INFO['elm_cards'] = build_elm('cp033_elm_38', ex, ey, ground(ex, ey) or -17.2, 62.0, 3.2, 24.0, 3833, bark, leaf_mat())

# navvy dress: people_lib smocks (albedo 0.35-0.48) read as white mannequins in the BUILD53 sun; navvies wore canvas/flannel
# shirts, moleskin/fustian and velveteen (Coleman, The Railway Navvies, R-typical) -> darker worn drab/blue/brown (I)
NAVVY_SHIRT = [(0.20, 0.17, 0.12), (0.10, 0.115, 0.15), (0.16, 0.13, 0.09), (0.22, 0.20, 0.16), (0.17, 0.08, 0.055), (0.13, 0.12, 0.10)]
recol = {}; nre = 0
for o in people:
    for i_, m_ in enumerate(o.data.materials):
        if m_ and m_.name.startswith('CPL3_smock'):
            key = (m_.name, o.data.name)
            if key not in recol:
                nm = m_.copy(); nm.name = 'cp033_navvy_shirt_%d' % (len(recol) % 99)
                c_ = NAVVY_SHIRT[len(recol) % len(NAVVY_SHIRT)]
                b_ = nm.node_tree.nodes.get('Principled BSDF') if nm.use_nodes else None
                if b_: b_.inputs['Base Color'].default_value = (*c_, 1)
                nm.diffuse_color = (*c_, 1); recol[key] = nm
            o.data.materials[i_] = recol[key]; nre += 1
INFO['smock_slots_recoloured'] = nre
for o in col.objects:
    o['cp_state'] = STATE
print('CP033 BUILT', INFO, 'people', len(people), 'hidden', HIDDEN)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP033 SAVED', OUT)
