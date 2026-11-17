"""CP036 CANDIDATE (2026-11-17, no verdict): 'Arrival becomes part of the attraction' - the Railway Colonnade
(glazed covered way from the Crystal Palace (Low Level) station up to the south wing), c.1854-1856.

usage: blender -b rounds/sydenham-open54-r14.blend -P scripts/candidate_cp036_colonnade.py [-- out.blend]
       (env CP036_NOSAVE=1: build in memory only)
Opens rounds/sydenham-open54-r14.blend (md5 104ee46d; never written) - the blend the live CP036 hero
renders/r14_open54_CAM_CP036_covered_way_28mm.png was rendered from (look v1.1 apply_render.py, era 1851,
tod interior_daylit, 24 spp, 1280x720, --no-people; re-render max diff 0) -> rounds/candidates/sydenham-open54-r14_cp036colonnade.blend.
Live hero shows: a 24 ft wide glass tube with a 22 ft ridge, beige box floor + stepped beige landings, 16 ft side posts,
no planting at all, and pv57 low-poly cone crinolines / blocky gents filling the walk right up to the lens.
Sources (Guide to the Crystal Palace and Park, 1856; Muse OCR):
  0216: 'From the end of the south wing to the Crystal Palace Railway-station ... is a colonnade 720 feet long, 17 feet
         wide, and 18 feet high ... the quantity of iron employed in this covered passage is 60 tons; of glass 30,000
         superficial feet.'
  0208: 'The visitor, having reached the Crystal Palace terminus, quits the train, and ascends the broad flight of steps
         before him, leading to a covered way called the Railway Colonnade, in which is placed a collection of plants
         forming an avenue of choice exotics. At the end of this colonnade is the south wing of the Palace.'
Adds dated collection SY54_railway_colonnade_avenue__1854_1856 and:
  1. old covered way (roof glass, side glass, ironwork, floor+steps, dado) hidden (not deleted) and rebuilt on the SAME
     route and the SAME 30 x 24 ft bay floor levels (r14 stepping, I) at the 1856 Guide section: 17 ft clear between the
     glass lines, 18 ft floor-to-ridge; 3 ft brick dwarf walls, round cast-iron columns at 8 ft centres (Paxton module,
     I), glazed sides with sash bars + transom, eaves gutter, an arched rib (truss) at every column, pitched glass roof
     with glazing bars + ridge, glazed steps where the bays step; floor = r14 floor+steps narrowed to 17 ft, boarded;
     shed-wall doorway infilled to the narrower 17 ft colonnade (brick piers);
  2. 'an avenue of choice exotics': symmetrical pairs of tubbed / potted plants along both dwarf walls every 8 ft
     (feather palms, tree ferns, clipped orange trees, camellias, yuccas in green Versailles tubs; red pelargoniums in
     terracotta pots at the columns), from 8.5 m in front of the hero lens up to the south wing (species/forms I);
  3. pv57 station-visitor points inside the colonnade or within 6 m of the hero lens dropped from a mesh COPY of
     ppl54_station_visitors (original hidden, not deleted), re-dressed as people_lib v3.4 1850s visitors walking up
     toward the palace, a few pausing at the plants; nearest new figure >= 9 m from the hero lens, the camera line kept
     clear for the first 25 m so the avenue reads.
Cameras NOT moved, sun/world/exposure NOT changed. Units metres in the blend; feet in DEPARTURES.
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector, Matrix

FT = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from cpl_people import person_mesh

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP036_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-open54-r14_cp036colonnade.blend')
STATE = 'SY54-56_railway_colonnade_avenue__1854_1856'
RNG = random.Random(1856036)
sc = bpy.context.scene
CAM = bpy.data.objects['CAM_CP036_covered_way_28mm']
COLL = 'SY54_railway_colonnade_avenue__1854_1856'
col = bpy.data.collections.get(COLL) or bpy.data.collections.new(COLL)
if col.name not in [c.name for c in sc.collection.children]: sc.collection.children.link(col)
col['cp_state'] = STATE
col['evidence'] = ('colonnade 720 x 17 x 18 ft, 60 t iron, 30,000 sq ft glass R (1856 Guide, Muse 0216); avenue of choice exotics, '
                   'broad flight of steps from the terminus R (1856 Guide, Muse 0208); route + bay levels I (r14); column module, '
                   'truss form, plant species, tubs, visitors I')
INFO = {}; HIDDEN = []
def hide(o):
    o.hide_render = True; o.hide_viewport = True; o['cp036_hidden_by_candidate'] = True; HIDDEN.append(o.name)

# ------------------------------------------------------------------ materials
def nmat(name, c0, c1, scale=6.0, rough=0.85, bump=0.1, metal=0.0, spec=0.2, coord='Object'):
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    b = N['Principled BSDF']; tc = N.new('ShaderNodeTexCoord'); nz = N.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = 5.0; L.new(tc.outputs[coord], nz.inputs['Vector'])
    rp = N.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = (*c0, 1); rp.color_ramp.elements[1].color = (*c1, 1)
    rp.color_ramp.elements[0].position = 0.3; rp.color_ramp.elements[1].position = 0.72
    L.new(nz.outputs['Fac'], rp.inputs[0]); L.new(rp.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    b.inputs['Specular IOR Level'].default_value = spec
    if bump:
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; L.new(nz.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs[0], b.inputs['Normal'])
    m.diffuse_color = (*c1, 1); return m

def boards(name):
    """boarded floor: 6 in boards running along the walk (y), per-board tone, dark joints"""
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    b = N['Principled BSDF']; tc = N.new('ShaderNodeTexCoord')
    mp = N.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / (0.5 * FT), 1 / (12 * FT), 1.0)
    L.new(tc.outputs['Generated' if False else 'Object'], mp.inputs['Vector'])
    br = N.new('ShaderNodeTexBrick'); br.inputs['Scale'].default_value = 1.0; br.inputs['Mortar Size'].default_value = 0.04
    br.offset = 0.37; br.inputs['Color1'].default_value = (0.36, 0.25, 0.15, 1); br.inputs['Color2'].default_value = (0.27, 0.18, 0.10, 1)
    br.inputs['Mortar'].default_value = (0.08, 0.055, 0.035, 1); br.inputs['Brick Width'].default_value = 1.0; br.inputs['Row Height'].default_value = 1.0
    L.new(mp.outputs[0], br.inputs['Vector']); L.new(br.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.72; b.inputs['Specular IOR Level'].default_value = 0.25
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.15; L.new(br.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs[0], b.inputs['Normal'])
    m.diffuse_color = (0.33, 0.23, 0.14, 1); return m

def brickmat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    b = N['Principled BSDF']; tc = N.new('ShaderNodeTexCoord'); br = N.new('ShaderNodeTexBrick')
    br.inputs['Scale'].default_value = 1 / (0.75 * FT); br.inputs['Mortar Size'].default_value = 0.012
    br.inputs['Color1'].default_value = (0.42, 0.30, 0.18, 1); br.inputs['Color2'].default_value = (0.34, 0.22, 0.13, 1)
    br.inputs['Mortar'].default_value = (0.55, 0.52, 0.46, 1); br.inputs['Brick Width'].default_value = 0.5; br.inputs['Row Height'].default_value = 0.25
    sx_ = N.new('ShaderNodeSeparateXYZ'); cb = N.new('ShaderNodeCombineXYZ'); L.new(tc.outputs['Object'], sx_.inputs[0])
    L.new(sx_.outputs['Y'], cb.inputs['X']); L.new(sx_.outputs['Z'], cb.inputs['Y']); L.new(sx_.outputs['X'], cb.inputs['Z'])   # walls run along y
    L.new(cb.outputs[0], br.inputs['Vector']); L.new(br.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.9; m.diffuse_color = (0.4, 0.28, 0.17, 1); return m

IRON = bpy.data.materials.get('iron_painted_OJ') or nmat('cp036_iron', (0.1, 0.16, 0.35), (0.12, 0.2, 0.42))
GLASS_R = bpy.data.materials.get('glass_roof'); GLASS_W = bpy.data.materials.get('glass_wall')
M = dict(
    iron=IRON, glass_r=GLASS_R, glass_w=GLASS_W,
    floor=boards('cp036_floor_boards'), brick=brickmat('cp036_dwarf_wall_brick'),
    coping=nmat('cp036_stone_coping', (0.52, 0.49, 0.43), (0.62, 0.59, 0.52), 9.0, 0.8, 0.05),
    gutter=nmat('cp036_gutter_iron', (0.07, 0.07, 0.08), (0.12, 0.12, 0.13), 12.0, 0.5, 0.02, 0.6),
    tub=nmat('cp036_tub_green', (0.05, 0.13, 0.07), (0.08, 0.19, 0.10), 10.0, 0.55, 0.03, 0.0, 0.35),
    band=nmat('cp036_tub_band', (0.04, 0.04, 0.04), (0.08, 0.08, 0.07), 10.0, 0.45, 0.0, 0.7),
    soil=nmat('cp036_soil', (0.07, 0.045, 0.03), (0.12, 0.08, 0.05), 30.0, 0.95, 0.3),
    terracotta=nmat('cp036_terracotta', (0.42, 0.17, 0.08), (0.52, 0.24, 0.12), 14.0, 0.85, 0.05),
    palm_trunk=nmat('cp036_palm_trunk', (0.20, 0.15, 0.10), (0.33, 0.27, 0.19), 22.0, 0.95, 0.6),
    fern_trunk=nmat('cp036_fern_trunk', (0.07, 0.045, 0.025), (0.16, 0.10, 0.05), 40.0, 1.0, 0.8),
    frond=nmat('cp036_palm_frond', (0.06, 0.15, 0.04), (0.14, 0.28, 0.07), 8.0, 0.6, 0.05, 0.0, 0.35),
    fern=nmat('cp036_fern_frond', (0.10, 0.25, 0.05), (0.20, 0.40, 0.08), 8.0, 0.65, 0.05, 0.0, 0.3),
    leaf=nmat('cp036_leaf_dark', (0.03, 0.10, 0.03), (0.08, 0.20, 0.05), 25.0, 0.5, 0.15, 0.0, 0.4),
    yucca=nmat('cp036_yucca', (0.18, 0.28, 0.14), (0.30, 0.40, 0.20), 6.0, 0.55, 0.0, 0.0, 0.3),
    orange=nmat('cp036_orange_fruit', (0.70, 0.30, 0.02), (0.85, 0.42, 0.05), 20.0, 0.45, 0.0),
    bloom_pink=nmat('cp036_bloom_pink', (0.75, 0.30, 0.42), (0.88, 0.45, 0.55), 20.0, 0.6, 0.0),
    bloom_white=nmat('cp036_bloom_white', (0.80, 0.78, 0.72), (0.92, 0.90, 0.85), 20.0, 0.6, 0.0),
    bloom_red=nmat('cp036_bloom_red', (0.60, 0.04, 0.03), (0.78, 0.08, 0.05), 20.0, 0.6, 0.0),
    stem=nmat('cp036_stem', (0.18, 0.13, 0.08), (0.26, 0.19, 0.12), 20.0, 0.9, 0.2),
)
ML = list(M.values()); IX = {k: i for i, k in enumerate(M)}

class Kit:
    """bmesh builder, inputs in FEET (world), stored in metres"""
    def __init__(s): s.bm = bmesh.new()
    def _t(s, k, n0):
        s.bm.faces.ensure_lookup_table()
        for j in range(n0, len(s.bm.faces)): s.bm.faces[j].material_index = IX[k]
    def v(s, p): return s.bm.verts.new((p[0] * FT, p[1] * FT, p[2] * FT))
    def poly(s, k, pts):
        n0 = len(s.bm.faces); s.bm.faces.new([s.v(p) for p in pts]); s._t(k, n0)
    def box(s, k, x0, x1, y0, y1, z0, z1):
        n0 = len(s.bm.faces); vs = [s.v(p) for p in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]]
        for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]: s.bm.faces.new([vs[j] for j in f])
        s._t(k, n0)
    def cyl(s, k, a, b, r, seg=10, cap=True, r2=None):
        A = Vector(a); B = Vector(b); d = B - A
        if d.length < 1e-6: return
        d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0)); u = d.cross(up).normalized(); w = u.cross(d).normalized()
        n0 = len(s.bm.faces); r2 = r if r2 is None else r2
        ra = [s.v(A + (u * math.cos(2 * math.pi * j / seg) + w * math.sin(2 * math.pi * j / seg)) * r) for j in range(seg)]
        rb = [s.v(B + (u * math.cos(2 * math.pi * j / seg) + w * math.sin(2 * math.pi * j / seg)) * r2) for j in range(seg)]
        for j in range(seg): s.bm.faces.new([ra[j], ra[(j + 1) % seg], rb[(j + 1) % seg], rb[j]])
        if cap: s.bm.faces.new(list(reversed(ra))); s.bm.faces.new(rb)
        s._t(k, n0)
    def bar(s, k, a, b, w, t=None):
        t = t or w; A = Vector(a); B = Vector(b); d = B - A
        if d.length < 1e-6: return
        d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0)); sd = d.cross(up).normalized(); u = sd.cross(d).normalized()
        n0 = len(s.bm.faces); pts = [s.v(p + sd * (i * w / 2) + u * (j * t / 2)) for p in (A, B) for (i, j) in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        for f in [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]: s.bm.faces.new([pts[j] for j in f])
        s._t(k, n0)
    def lathe(s, k, cx, cy, prof, seg=14):
        n0 = len(s.bm.faces); rings = []
        for r, z in prof:
            rings.append([s.v((cx + max(r, 1e-3) * math.cos(2 * math.pi * j / seg), cy + max(r, 1e-3) * math.sin(2 * math.pi * j / seg), z)) for j in range(seg)])
        for a, b in zip(rings, rings[1:]):
            for j in range(seg): s.bm.faces.new([a[j], a[(j + 1) % seg], b[(j + 1) % seg], b[j]])
        s.bm.faces.new(list(reversed(rings[0]))); s.bm.faces.new(rings[-1]); s._t(k, n0)
    def blob(s, k, c, radii, rough=0.18, sub=2, seed=0):
        """displaced icosphere (foliage mass)"""
        n0 = len(s.bm.faces); r_ = random.Random(seed)
        tmp = bmesh.new(); bmesh.ops.create_icosphere(tmp, subdivisions=sub, radius=1.0)
        ph = [r_.uniform(0, 6.28) for _ in range(6)]
        mp = {}
        for vv in tmp.verts:
            d = vv.co.normalized()
            f = 1 + rough * (math.sin(3.1 * d.x + ph[0]) * math.sin(2.7 * d.y + ph[1]) + 0.6 * math.sin(5.3 * d.z + ph[2]) + r_.uniform(-0.5, 0.5))
            mp[vv] = s.v((c[0] + d.x * radii[0] * f, c[1] + d.y * radii[1] * f, c[2] + d.z * radii[2] * f))
        for fc in tmp.faces: s.bm.faces.new([mp[vv] for vv in fc.verts])
        tmp.free(); s._t(k, n0)
    def ico(s, k, c, r, sub=1):
        n0 = len(s.bm.faces)
        bmesh.ops.create_icosphere(s.bm, subdivisions=sub, radius=r * FT, matrix=Matrix.Translation(Vector(c) * FT)); s._t(k, n0)
    def done(s, name, smooth=False):
        me = bpy.data.meshes.new(name); s.bm.normal_update(); s.bm.to_mesh(me); s.bm.free()
        for m in ML: me.materials.append(m)
        if smooth:
            for p in me.polygons: p.use_smooth = True
        ob = bpy.data.objects.new(name, me); col.objects.link(ob); ob['cp_state'] = STATE
        return ob

# ------------------------------------------------------------------ route + bay levels from the r14 covered way
OLD = ['covered_way_roof_glass', 'covered_way_side_glass', 'covered_way_ironwork', 'covered_way_floor_steps', 'covered_way_dado']
fl = bpy.data.objects['covered_way_floor_steps']; dado = bpy.data.objects['covered_way_dado']
bbx = [(fl.matrix_world @ Vector(c)) / FT for c in fl.bound_box]
CWX = round((min(v.x for v in bbx) + max(v.x for v in bbx)) / 2, 2)          # -890 ft
Y1, Y0 = round(min(v.y for v in bbx), 2), round(max(v.y for v in bbx), 2)      # -1334 .. -614 ft (720 ft, R)
BAY = 24.0
NB = int(round((Y0 - Y1) / BAY))
bnd = {}                                                                     # boundary y -> set of dado z values there
for vv in dado.data.vertices:
    p = (dado.matrix_world @ vv.co) / FT
    bnd.setdefault(round(p.y, 1), set()).add(round(p.z, 2))
zmin = {}
for i in range(NB):
    a_, b_ = bnd[round(Y1 + i * BAY, 1)], bnd[round(Y1 + (i + 1) * BAY, 1)]
    zmin[i] = min(a_ & b_)                                                   # the bay's own dado (bottom = floor level zf)
bays = [(Y1 + i * BAY, Y1 + (i + 1) * BAY, round(zmin[i], 3)) for i in range(NB)]   # (ya, yb, zf) bottom (station) -> top (wing)
INFO['route'] = dict(CWX=CWX, Y1=Y1, Y0=Y0, length_ft=Y0 - Y1, bays=NB, rise_ft=round(bays[-1][2] - bays[0][2], 2))
HW = 17.0 / 2          # R 17 ft wide (clear between glass lines)
EAVE, RIDGE = 13.0, 18.0   # R 18 ft high (floor to ridge); eave I
for n in OLD: hide(bpy.data.objects[n])

# floor + steps: r14 mesh copy, narrowed 24 -> 17 ft about the axis (levels and step flights unchanged)
fm = fl.data.copy(); fm.name = 'cp036_colonnade_floor_steps'
for vv in fm.vertices:
    p = fl.matrix_world @ vv.co; p.x = CWX * FT + (p.x - CWX * FT) * (2 * HW / 24.0); vv.co = fl.matrix_world.inverted() @ p
fm.materials.clear(); fm.materials.append(M['floor'])
fo = bpy.data.objects.new('cp036_colonnade_floor_steps', fm); fo.matrix_world = fl.matrix_world.copy(); col.objects.link(fo); fo['cp_state'] = STATE

# park_slope (a 12-vertex plane here) stands up to ~1.2 ft ABOVE the r14 boards in many bays (the green strip at the foot of
# the second flight in the live hero). On a mesh COPY (r14 mesh kept with a fake user): bisect along the inner faces of the
# dwarf walls and the two ends, then delete the terrain faces inside that rectangle (under the boards it is never seen).
ps_ = bpy.data.objects.get('park_slope')
if ps_:
    nm = ps_.data.copy(); nm.name = ps_.data.name + '_cp036cut'
    pm_ = ps_.matrix_world; pmi = pm_.inverted()
    bt = bmesh.new(); bt.from_mesh(nm); nf0 = len(bt.faces)
    xa_, xb_ = (CWX - HW + 0.5) * FT, (CWX + HW - 0.5) * FT
    for (co_, no_) in (((xa_, 0, 0), (1, 0, 0)), ((xb_, 0, 0), (1, 0, 0)), ((0, Y1 * FT, 0), (0, 1, 0)), ((0, Y0 * FT, 0), (0, 1, 0))):
        co_l = pmi @ Vector(co_); no_l = (pmi.to_3x3().transposed().inverted() @ Vector(no_)).normalized() if False else (pm_.to_3x3().transposed() @ Vector(no_)).normalized()
        g = bt.verts[:] + bt.edges[:] + bt.faces[:]
        bmesh.ops.bisect_plane(bt, geom=g, plane_co=co_l, plane_no=no_l)
    dele = []
    for fc in bt.faces:
        c = pm_ @ fc.calc_center_median()
        if xa_ < c.x < xb_ and Y1 * FT < c.y < Y0 * FT: dele.append(fc)
    bmesh.ops.delete(bt, geom=dele, context='FACES'); bt.to_mesh(nm); bt.free()
    old_me = ps_.data; old_me.use_fake_user = True; ps_.data = nm
    INFO['park_slope_cut'] = f'{len(dele)} faces deleted inside the colonnade (r14 mesh {old_me.name} kept, fake user)'
k = Kit()
def step_len(i):
    if i + 1 >= NB: return 0.0
    rise = bays[i + 1][2] - bays[i][2]
    return (int(rise / 0.55) + 1) * 1.1 if rise > 0.4 else 0.0
NCOL = 0
for i, (ya, yb, zf) in enumerate(bays):
    for sx in (-1, 1):
        xo = CWX + sx * HW
        # brick dwarf wall 3 ft (1 ft thick, centred on the glass line) + stone coping
        k.box('brick', xo - 0.5, xo + 0.5, ya, yb, zf - 0.5, zf + 2.75); k.box('coping', xo - 0.6, xo + 0.6, ya, yb, zf + 2.75, zf + 3.0)
        for j in range(3):
            yc = ya + j * 8.0
            # cast-iron column (6 in shaft), base + cushion capital; 8 ft centres (I)
            k.box('iron', xo - 0.32, xo + 0.32, yc - 0.32, yc + 0.32, zf, zf + 0.6)
            k.cyl('iron', (xo, yc, zf + 0.6), (xo, yc, zf + EAVE - 0.6), 0.25, 10, cap=False, r2=0.21)
            k.cyl('iron', (xo, yc, zf + EAVE - 0.6), (xo, yc, zf + EAVE - 0.25), 0.21, 10, r2=0.34)
            k.box('iron', xo - 0.36, xo + 0.36, yc - 0.36, yc + 0.36, zf + EAVE - 0.25, zf + EAVE); NCOL += 1
            # glazing: two sashes per 8 ft, bars every 2 ft, transom at 8 ft
            k.poly('glass_w', [(xo, yc, zf + 3.0), (xo, yc + 8, zf + 3.0), (xo, yc + 8, zf + EAVE), (xo, yc, zf + EAVE)])
            for q in (2, 4, 6): k.box('iron', xo - 0.06, xo + 0.06, yc + q - 0.05, yc + q + 0.05, zf + 3.0, zf + EAVE)
            k.box('iron', xo - 0.08, xo + 0.08, yc, yc + 8, zf + 8.2, zf + 8.4)
            # arched rib at each column: rafters to the ridge + segmental arch brace + spandrel ring (I)
            if sx == 1:
                k.bar('iron', (CWX - HW, yc, zf + EAVE), (CWX, yc, zf + RIDGE), 0.25, 0.45)
                k.bar('iron', (CWX, yc, zf + RIDGE), (CWX + HW, yc, zf + EAVE), 0.25, 0.45)
                pts = []
                for a in range(13):
                    t = a / 12; ang = math.pi * (1 - t)
                    pts.append((CWX + HW * math.cos(ang), yc, zf + EAVE - 2.4 + 3.6 * math.sin(ang)))
                for p0, p1 in zip(pts, pts[1:]): k.bar('iron', p0, p1, 0.16, 0.22)
                for xr in (-0.55, 0.55):
                    k.cyl('iron', (CWX + xr * HW - 0.0, yc - 0.08, zf + EAVE + 0.15), (CWX + xr * HW, yc + 0.08, zf + EAVE + 0.15), 0.55, 12, cap=False)
        # eaves gutter + plate
        k.box('gutter', xo - 0.1 + sx * 0.35, xo + 0.1 + sx * 0.75, ya, yb, zf + EAVE - 0.1, zf + EAVE + 0.35)
        k.box('iron', xo - 0.35, xo + 0.35, ya, yb, zf + EAVE - 0.35, zf + EAVE)
    # roof glass + bars every 2 ft + ridge
    k.poly('glass_r', [(CWX - HW - 0.2, ya, zf + EAVE + 0.05), (CWX - HW - 0.2, yb, zf + EAVE + 0.05), (CWX, yb, zf + RIDGE + 0.05), (CWX, ya, zf + RIDGE + 0.05)])
    k.poly('glass_r', [(CWX, ya, zf + RIDGE + 0.05), (CWX, yb, zf + RIDGE + 0.05), (CWX + HW + 0.2, yb, zf + EAVE + 0.05), (CWX + HW + 0.2, ya, zf + EAVE + 0.05)])
    for q in range(1, 12):
        yq = ya + q * 2.0
        if q % 4 == 0: continue
        k.bar('iron', (CWX - HW, yq, zf + EAVE + 0.1), (CWX, yq, zf + RIDGE + 0.1), 0.08, 0.14)
        k.bar('iron', (CWX, yq, zf + RIDGE + 0.1), (CWX + HW, yq, zf + EAVE + 0.1), 0.08, 0.14)
    k.box('iron', CWX - 0.25, CWX + 0.25, ya, yb, zf + RIDGE - 0.2, zf + RIDGE + 0.35)
    # glazed step in the roof/sides where the next bay up is higher
    if i + 1 < NB:
        zh = bays[i + 1][2]
        if zh > zf + 0.05:
            for sx in (-1, 1):
                k.poly('glass_r', [(CWX + sx * HW, yb, zf + EAVE), (CWX, yb, zf + RIDGE), (CWX, yb, zh + RIDGE), (CWX + sx * HW, yb, zh + EAVE)])
            k.bar('iron', (CWX - HW, yb, zh + EAVE), (CWX, yb, zh + RIDGE), 0.25, 0.45); k.bar('iron', (CWX, yb, zh + RIDGE), (CWX + HW, yb, zh + EAVE), 0.25, 0.45)
# end columns at the wing end
for sx in (-1, 1):
    xo = CWX + sx * HW; zf = bays[-1][2]
    k.cyl('iron', (xo, Y0, zf), (xo, Y0, zf + EAVE), 0.25, 10)
# shed-wall doorway: infill the 24 ft opening to the 17 ft colonnade (brick piers); station datum from the platforms
sp = bpy.data.objects.get('station_platforms')
if sp:
    zs = min((sp.matrix_world @ Vector(c)).z for c in sp.bound_box) / FT
    ys = max((sp.matrix_world @ Vector(c)).y for c in sp.bound_box) / FT + 1.5   # shed wall line (SH_Y0)
    for sx in (-1, 1):
        k.box('brick', CWX + sx * HW + (0 if sx > 0 else -3.6), CWX + sx * HW + (3.6 if sx > 0 else 0), ys - 1.5, ys + 1.5, zs - 1, zs + 18.5)
    INFO['doorway_infill_y'] = round(ys, 1)
k.done('cp036_colonnade_structure')
INFO['columns'] = NCOL

# ------------------------------------------------------------------ 2. avenue of choice exotics
P = Kit()
def tub(x, y, z, w=2.4, h=2.0):
    a = w / 2
    P.box('tub', x - a + 0.12, x + a - 0.12, y - a + 0.12, y + a - 0.12, z, z + h)
    for sx in (-1, 1):
        for sy in (-1, 1):
            P.box('tub', x + sx * a - 0.14, x + sx * a + 0.14, y + sy * a - 0.14, y + sy * a + 0.14, z, z + h + 0.25)
            P.ico('tub', (x + sx * a, y + sy * a, z + h + 0.38), 0.15, 1)
    for zz in (z + 0.35, z + h - 0.35): P.box('band', x - a + 0.08, x + a - 0.08, y - a + 0.08, y + a - 0.08, zz, zz + 0.12)
    P.box('soil', x - a + 0.18, x + a - 0.18, y - a + 0.18, y + a - 0.18, z + h - 0.15, z + h - 0.1)
    return z + h - 0.1
def pot(x, y, z, r=0.55, h=1.0):
    P.lathe('terracotta', x, y, [(r * 0.7, z), (r, z + h - 0.12), (r * 1.1, z + h - 0.1), (r * 1.1, z + h), (r * 0.95, z + h)], 12)
    P.lathe('soil', x, y, [(r * 0.95, z + h - 0.12), (r * 0.95, z + h - 0.08)], 12)
    return z + h - 0.08
def pinnate(kind, base, az, length, elev, droop, leaf, n=16, wid=0.05):
    """frond: curved rachis + leaflet triangles both sides (feet)"""
    ca, sa = math.cos(az), math.sin(az)
    def at(t):
        hdist = length * t * math.cos(elev); vz = length * t * math.sin(elev) - droop * length * t * t
        return Vector((base[0] + ca * hdist, base[1] + sa * hdist, base[2] + vz))
    pts = [at(t / n) for t in range(n + 1)]
    # keep every frond (rachis + leaflet reach) inside the glass lines and under the roof: shorten until it fits
    for _ in range(12):
        if all(abs(q.x - CWX) + leaf * 0.95 < HW - 0.3 for q in pts) and all(q.z < base_zf + EAVE - 0.4 + (HW - abs(q.x - CWX)) * (RIDGE - EAVE) / HW for q in pts): break
        length *= 0.85; leaf *= 0.92; pts = [at(t / n) for t in range(n + 1)]
    for p0, p1 in zip(pts, pts[1:]): P.bar(kind, p0, p1, wid, wid)
    side = Vector((-sa, ca, 0))
    for j in range(1, n):
        p = pts[j]; d = (pts[j + 1] - pts[j - 1]).normalized(); t = j / n
        ll = leaf * math.sin(math.pi * min(1.0, t * 1.15)) + 0.05
        for sgn in (-1, 1):
            tip = p + side * sgn * ll * 0.92 + d * ll * 0.35 + Vector((0, 0, -0.25 * ll))
            P.poly(kind, [tuple(p), tuple(p + d * 0.22 * length / n * 2), tuple(tip)])
def palm(x, y, z, s=1.0, seed=0):
    r_ = random.Random(seed); th = 6.8 * s + r_.uniform(-0.4, 0.4)
    P.cyl('palm_trunk', (x, y, z - 0.2), (x, y, z + th), 0.42 * s, 10, r2=0.30 * s)
    for q in range(5): P.cyl('palm_trunk', (x, y, z + 0.6 + q * th / 5.5), (x, y, z + 0.9 + q * th / 5.5), 0.46 * s, 10, r2=0.40 * s)
    top = (x, y, z + th)
    nf = 13
    for f in range(nf):
        az = 2 * math.pi * f / nf + r_.uniform(-0.15, 0.15); el = r_.uniform(0.55, 1.05) if f % 2 else r_.uniform(0.25, 0.6)
        pinnate('frond', top, az, 5.4 * s * r_.uniform(0.85, 1.05), el, 0.55, 1.35 * s, 16, 0.07)
def treefern(x, y, z, s=1.0, seed=0):
    r_ = random.Random(seed); th = 4.8 * s + r_.uniform(-0.3, 0.3)
    P.cyl('fern_trunk', (x, y, z - 0.2), (x, y, z + th), 0.48 * s, 9, r2=0.55 * s)
    top = (x, y, z + th + 0.2); nf = 11
    for f in range(nf):
        az = 2 * math.pi * f / nf + r_.uniform(-0.2, 0.2)
        pinnate('fern', top, az, 5.0 * s * r_.uniform(0.85, 1.05), r_.uniform(0.5, 0.9), 0.75, 1.2 * s, 16, 0.06)
    for f in range(4): pinnate('fern', top, r_.uniform(0, 6.28), 1.3 * s, 1.35, 0.2, 0.4 * s, 6, 0.04)     # crozier flush
def orange(x, y, z, s=1.0, seed=0):
    r_ = random.Random(seed)
    P.cyl('stem', (x, y, z - 0.1), (x, y, z + 3.0 * s), 0.14, 8)
    c = (x, y, z + 3.0 * s + 1.6 * s)
    P.blob('leaf', c, (1.5 * s, 1.5 * s, 1.6 * s), 0.12, 2, seed)
    for q in range(26):
        th_ = r_.uniform(0, 6.28); ph = r_.uniform(-1.0, 1.1)
        d = Vector((math.cos(th_) * math.cos(ph), math.sin(th_) * math.cos(ph), math.sin(ph)))
        P.ico('orange', (c[0] + d.x * 1.54 * s, c[1] + d.y * 1.54 * s, c[2] + d.z * 1.62 * s), 0.15, 1)
def camellia(x, y, z, s=1.0, seed=0, bloom='bloom_pink'):
    r_ = random.Random(seed); c = (x, y, z + 2.3 * s)
    P.cyl('stem', (x, y, z - 0.1), (x, y, z + 1.0 * s), 0.1, 7)
    P.blob('leaf', c, (1.3 * s, 1.3 * s, 2.1 * s), 0.2, 2, seed)
    for q in range(60):
        th_ = r_.uniform(0, 6.28); ph = r_.uniform(-0.6, 1.2)
        d = Vector((math.cos(th_) * math.cos(ph), math.sin(th_) * math.cos(ph), math.sin(ph)))
        P.ico(bloom if q % 5 else 'bloom_white', (c[0] + d.x * 1.35 * s, c[1] + d.y * 1.35 * s, c[2] + d.z * 2.15 * s), 0.17, 1)
def yucca(x, y, z, s=1.0, seed=0):
    r_ = random.Random(seed)
    P.cyl('palm_trunk', (x, y, z - 0.1), (x, y, z + 2.2 * s), 0.25, 8, r2=0.22)
    top = Vector((x, y, z + 2.2 * s))
    for q in range(34):
        az = r_.uniform(0, 6.28); el = r_.uniform(0.2, 1.45); L = 2.6 * s * r_.uniform(0.8, 1.1)
        d = Vector((math.cos(az) * math.cos(el), math.sin(az) * math.cos(el), math.sin(el)))
        sd = Vector((-math.sin(az), math.cos(az), 0)) * 0.11
        while abs((top + d * L).x - CWX) > HW - 0.4 and L > 0.4: L *= 0.85
        P.poly('yucca', [tuple(top + sd), tuple(top - sd), tuple(top + d * L)])
def pelargonium(x, y, z, seed=0):
    r_ = random.Random(seed); c = (x, y, z + 0.45)
    P.blob('leaf', c, (0.6, 0.6, 0.45), 0.25, 1, seed)
    for q in range(14):
        th_ = r_.uniform(0, 6.28); ph = r_.uniform(0.0, 1.3)
        d = Vector((math.cos(th_) * math.cos(ph), math.sin(th_) * math.cos(ph), math.sin(ph)))
        P.ico('bloom_red', (c[0] + d.x * 0.62, c[1] + d.y * 0.62, c[2] + d.z * 0.5), 0.12, 1)

camy = CAM.location.y / FT
PLANT_FROM = camy + 28.0                     # first planting 28 ft (8.5 m) in front of the hero lens
base_zf = 0.0
SEQ = ['camellia', 'palm', 'orange', 'treefern', 'palm', 'yucca', 'orange', 'treefern', 'camellia', 'palm', 'orange', 'yucca']
PLANTS = {}; nseq = 0; NPOT = 0
for i, (ya, yb, zf) in enumerate(bays):
    lim = yb - step_len(i) - 1.4
    for j in range(3):
        yc = ya + 4.0 + j * 8.0
        if yc < PLANT_FROM or yc > lim: continue
        sp_ = SEQ[nseq % len(SEQ)]; nseq += 1
        for sx in (-1, 1):
            x = CWX + sx * (HW - 1.95); seed = int(abs(yc) * 10) + (sx > 0); base_zf = zf
            if sp_ in ('palm', 'treefern'): zt = tub(x, yc, zf, 2.8, 2.2)
            elif sp_ == 'yucca': zt = pot(x, yc, zf, 0.95, 1.6)
            else: zt = tub(x, yc, zf, 2.3, 1.9)
            # the first pair (nearest the lens) kept low
            sc_ = 0.8 if yc < PLANT_FROM + 10 else 1.0
            {'palm': palm, 'treefern': treefern, 'orange': orange, 'yucca': yucca}.get(sp_, camellia)(x, yc, zt, sc_, seed)
            PLANTS[sp_] = PLANTS.get(sp_, 0) + 1
        # pelargonium pots against the dwarf wall at the column (between tubs)
        yp = ya + 8.0 * (j + 1)
        if PLANT_FROM <= yp <= lim:
            for sx in (-1, 1):
                x = CWX + sx * (HW - 1.0); zt = pot(x, yp, zf, 0.45, 0.85); pelargonium(x, yp, zt, int(abs(yp) * 7) + (sx > 0)); NPOT += 1
P.done('cp036_avenue_of_exotics')
INFO['plants'] = PLANTS; INFO['pelargonium_pots'] = NPOT; INFO['plant_from_ft_ahead_of_lens'] = round(PLANT_FROM - camy, 1)

# ------------------------------------------------------------------ 3. visitors: drop pv57 points in the colonnade / near the lens, add people_lib
pp = bpy.data.objects['ppl54_station_visitors']; mw = pp.matrix_world; cl = CAM.location
drop = []
for vv in pp.data.vertices:
    p = mw @ vv.co
    in_way = abs(p.x / FT - CWX) < 13.0 and p.y / FT > Y1 - 1.0
    if in_way or (p - cl).length < 6.0: drop.append(vv.index)
pme = pp.data.copy(); pme.name = pp.data.name + '_cp036'
bq = bmesh.new(); bq.from_mesh(pme); bq.verts.ensure_lookup_table()
bmesh.ops.delete(bq, geom=[bq.verts[i] for i in drop], context='VERTS'); bq.to_mesh(pme); bq.free()
pn = bpy.data.objects.new(pp.name + '_cp036', pme); pn.matrix_world = mw.copy()
for c in pp.users_collection: c.objects.link(pn)
for m_ in pp.modifiers:
    nm_ = pn.modifiers.new(m_.name, m_.type)
    if m_.type == 'NODES': nm_.node_group = m_.node_group
for k_ in pp.keys():
    try: pn[k_] = pp[k_]
    except Exception: pass
pn['people_count'] = len(pme.vertices); pn['cp036_mesh_copy_of'] = pp.name; hide(pp)
INFO['pv57_points_dropped'] = len(drop); INFO['pv57_points_kept'] = len(pme.vertices)

def link(o):
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o['cp_state'] = STATE; return o
people = []
def put(name, role, pose, x, y, z, rz, seed, lod):
    person_mesh(name, role, style={'role': role, 'pose': pose, 'lod': lod, 'era': '1850s'}, seed=seed)
    o = bpy.data.objects[name]; link(o); o.location = (x * FT, y * FT, z * FT); o.rotation_euler = (0, 0, rz)
    o['cpl_people'] = 'cpl_people_v3'; people.append(o); return o
UP = math.pi          # people_lib local -y faces forward; rz = pi -> facing +y (up the colonnade toward the wing)
def flat_z(i, y):
    ya, yb, zf = bays[i]
    return zf if y < yb - step_len(i) - 0.3 else None
camx = cl.x / FT
n = 0; nearest = 1e9
for i, (ya, yb, zf) in enumerate(bays):
    for j in range(6):
        y = ya + RNG.uniform(1.0, BAY - 1.0)
        d_m = (y - camy) * FT
        if d_m < 9.0: continue
        z = flat_z(i, y)
        if z is None: continue
        dens = 2 if d_m < 18 else (3 if d_m < 35 else (4 if d_m < 80 else 5))
        if j >= dens: continue
        # walkway between the tubs: |x - CWX| <= 4.6 ft; first 25 m keep the camera line (camx +- 2.5 ft) clear
        for _ in range(12):
            x = CWX + RNG.uniform(-4.4, 4.4)
            if d_m < 25 and abs(x - camx) < 3.0: continue
            break
        roleset = ('1850s_lady', '1850s_lady', '1850s_gentleman', '1850s_gentleman', '1850s_lady', '1850s_gentleman', '1850s_girl', '1850s_boy')
        role = roleset[RNG.randrange(len(roleset))]
        pose = 'walking' if RNG.random() < 0.7 else ('pointing' if RNG.random() < 0.4 else 'standing')
        rz = UP + RNG.uniform(-0.35, 0.35)
        if pose != 'walking' and RNG.random() < 0.6: rz = UP + (math.pi / 2 if x < CWX else -math.pi / 2) * 0.8   # turned to the plants
        lod = 'hero' if d_m < 15 else ('mid' if d_m < 45 else 'crowd')
        put(f'cp036_visitor_{n:03d}', role, pose, x, y, z, rz, 1856000 + n * 7, lod); n += 1
        nearest = min(nearest, math.hypot((x - camx) * FT, d_m))
        # couples: a companion beside some walkers
        if pose == 'walking' and RNG.random() < 0.35 and abs(x - CWX) < 3.2:
            x2 = x + (1.7 if x < CWX else -1.7)
            if not (d_m < 25 and abs(x2 - camx) < 3.0):
                r2 = '1850s_gentleman' if 'lady' in role else '1850s_lady'
                put(f'cp036_visitor_{n:03d}', r2, 'walking', x2, y + RNG.uniform(-0.6, 0.6), z, rz + RNG.uniform(-0.1, 0.1), 1856000 + n * 7, lod); n += 1
INFO['people_lib_visitors'] = len(people); INFO['nearest_new_figure_m'] = round(nearest, 2)

for o in col.objects: o['cp_state'] = STATE
print('CP036 BUILT', INFO, 'hidden', HIDDEN)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP036 SAVED', OUT)
