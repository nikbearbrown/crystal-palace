"""CP039 CANDIDATE (2026-11-17, no verdict): 'Antiquity in colour' - the Pompeian Court peristyle (Digby Wyatt, painted
by Giuseppe Abbate; opened with the Palace 10 Jun 1854), dressed after Scharf's 1854 handbook.

usage: blender -b rounds/sydenham-1856-r13.blend -P scripts/candidate_cp039_pompeian.py [-- out.blend]
       (env CP039_NOSAVE=1: build in memory only)
Opens rounds/sydenham-1856-r13.blend (md5 74dc7aa3; never written) - the blend the live CP039 hero
renders/r13_1856_CAM_CP039_pompeian_peristyle_28mm.png was rendered from (r13 finals recipe: scripts/render.py, RES=1280x720,
100 %, 32 spp, no PEOPLE_ERA / KEEP_LIGHTING / EXPO; look v1.1 was REVERTED for CP039; re-render max diff 0)
-> rounds/candidates/sydenham-1856-r13_cp039pompeian.blend.
Live hero shows: low-poly pv57 cone crinolines / blocky top-hat gent filling the left foreground, plain faceted stucco
shafts with box capitals, a flat green garden box with green stump 'shrubs', the end wall as a blue field with green
rectangles, dark brown sloping tile soffit over the ambulatory, plain dark floor.
Sources: G. Scharf, The Pompeian Court in the Crystal Palace (1854; archive.org pompeiancourtinc00scha), peristyle Nos. 18-26
(see scripts/cp039_pompeian_paint.py docstring for the quotes): ambulatory ceiling 'panelled ... very thin lines of the
brightest colours upon white' (R); 'Ionic capitals ... from the Basilica. The shafts ... not fluted at the lower part ...
painted bright red' (R); end wall No. 23 'general colour is white. Dado red and yellow', three central compartments
(lyrist under a high canopy on thin columns, priestess, youth with wreath), dado recesses with a seated lyre girl (R content,
drawing I); lararium 'a niche raised on a pedestal, flanked by pilasters, and surmounted by a pediment', wall behind
'rich Pompeian red, with a yellow ornament' (R form, position I); peristyle 'laid out with plants like a garden, bordered
with columns' (R; planting I). Plan footprint and wall heights unchanged (D-R13-F1).
Adds dated collection SY54_pompeian_peristyle_painted__1854_1856 and:
  1. painted wall faces (textures from scripts/cp039_pompeian_paint.py, packed) 0.14 ft proud of the r13 end, west and
     tablinum-side peristyle walls (r13 paint boxes left in place behind them);
  2. white panelled ambulatory ceiling at 15.2 ft with cross beams on the column bays (hides the dark tile soffit);
  3. fluted Ionic shafts + capitals (volute bolsters, abacus) + red base torus on the 14 peristyle columns (the r13 faceted
     shafts/box capitals removed from a mesh COPY of pompeian_stucco, original hidden; red lower thirds kept);
  4. ambulatory mosaic pavement + meander border along the stylobate; low stone kerb round the garden;
  5. garden: r13 green bed + 10 stump shrubs removed from a mesh COPY of pompeian_grn (original hidden); new soil bed,
     clipped box edging in four compartments round the r13 marble basin, roses / lilies / acanthus, 4 bay-laurel
     standards, 1 marble krater on a pedestal at the far end, no jet (Scharf names none in the peristyle);
  6. lararium aedicula on the end wall (far west end);
  7. pv57 visitor points in the peristyle or within 7 m of the hero lens dropped from a mesh COPY of ppl57_pompeian_visitors
     (original hidden), re-dressed as people_lib 1850s visitors looking at the paintings, nearest >= 8 m from the lens.
Cameras NOT moved, sun/world/exposure NOT changed. Units metres in the blend; feet here.
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector

FT = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from cpl_people import person_mesh
TEX = os.path.join(HERE, '..', 'refs', 'cp039_pompeian_paint')

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP039_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-1856-r13_cp039pompeian.blend')
STATE = 'SY54_pompeian_peristyle_painted__1854_1856'
RNG = random.Random(1854039)
sc = bpy.context.scene
CAM = bpy.data.objects['CAM_CP039_pompeian_peristyle_28mm']
COLL = 'SY54_pompeian_peristyle_painted__1854_1856'
col = bpy.data.collections.get(COLL) or bpy.data.collections.new(COLL)
parent = bpy.data.collections['SY54_court_pompeian__dated']
if col.name not in [c.name for c in parent.children]: parent.children.link(col)
col['cp_state'] = STATE
col['evidence'] = ('Scharf 1854 Pompeian Court handbook Nos. 18-26: white thin-line panelled ambulatory ceiling R, Ionic capitals + '
                   'red unfluted lower shafts R, end wall white with red/yellow dado + three central compartments R (drawing I), '
                   'lararium aedicula R (position I), peristyle garden R (planting I); footprint D-R13-F1 unchanged')
INFO = {}; HIDDEN = []
def hide(o):
    o.hide_render = True; o.hide_viewport = True; o['cp039_hidden_by_candidate'] = True; HIDDEN.append(o.name)

# r13 court geometry (scripts/courts2.py, feet)
PX0, PX1, PY0, PY1, PH = -562.0, -494.0, 62.0, 154.0, 20.0
XC = (PX0 + PX1) / 2
TY1 = 118.0
PCX0, PCX1, PCY0, PCY1 = -552.0, -504.0, 126.0, 146.0
COLS = [(PCX0 + i * (PCX1 - PCX0) / 5, y) for i in range(6) for y in (PCY0, PCY1)] + [(x, (PCY0 + PCY1) / 2) for x in (PCX0, PCX1)]
WE, WW, WT = PY1 - 0.6, PX0 + 0.6, TY1 + 0.5        # wall faces: end (north, y), west (x), tablinum side (y)
OFF = 0.14

# ------------------------------------------------------------------ materials
def nmat(name, c0, c1, scale=6.0, rough=0.85, bump=0.1, metal=0.0, spec=0.3):
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    b = N['Principled BSDF']; tc = N.new('ShaderNodeTexCoord'); nz = N.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = 5.0; L.new(tc.outputs['Object'], nz.inputs['Vector'])
    rp = N.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = (*c0, 1); rp.color_ramp.elements[1].color = (*c1, 1)
    rp.color_ramp.elements[0].position = 0.3; rp.color_ramp.elements[1].position = 0.72
    L.new(nz.outputs['Fac'], rp.inputs[0]); L.new(rp.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    b.inputs['Specular IOR Level'].default_value = spec
    if bump:
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; L.new(nz.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs[0], b.inputs['Normal'])
    m.diffuse_color = (*c1, 1); return m
def imat(name, fname, rough=0.55, spec=0.35, repeat=False):
    p = os.path.abspath(os.path.join(TEX, fname))
    img = bpy.data.images.load(p, check_existing=False); img.name = 'cp039_' + fname; img.pack()
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    b = N['Principled BSDF']; tx = N.new('ShaderNodeTexImage'); tx.image = img; tx.interpolation = 'Linear'
    tx.extension = 'REPEAT' if repeat else 'EXTEND'
    uv = N.new('ShaderNodeTexCoord'); L.new(uv.outputs['UV'], tx.inputs['Vector']); L.new(tx.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough; b.inputs['Specular IOR Level'].default_value = spec
    m.diffuse_color = (0.7, 0.6, 0.5, 1); return m
def fluted(name, base_c):
    """stucco shaft: 20 flutes as a cosine bump around the object z axis"""
    m = nmat(name, base_c, tuple(min(1, c * 1.05) for c in base_c), 14.0, 0.6, 0.02)
    return m
MAT = bpy.data.materials
M = dict(
    end=imat('cp039_paint_end_wall_no23', 'cp039_end_wall_no23.png'),
    west=imat('cp039_paint_west_wall', 'cp039_west_wall.png'),
    tab=imat('cp039_paint_tablinum_wall', 'cp039_tablinum_wall.png'),
    ceil=imat('cp039_paint_ceiling', 'cp039_ceiling_tile.png', 0.7, 0.2, True),
    floor=imat('cp039_mosaic_floor', 'cp039_floor_tile.png', 0.45, 0.4, True),
    border=imat('cp039_mosaic_border', 'cp039_border_strip.png', 0.45, 0.4, True),
    stucco=fluted('cp039_stucco_shaft', (0.80, 0.76, 0.68)),
    red=MAT['pomp_red'], marble=MAT['pomp_marble'], water=MAT['pomp_water'],
    beam=nmat('cp039_ceiling_beam', (0.78, 0.74, 0.66), (0.84, 0.80, 0.72), 10.0, 0.7, 0.02),
    kerb=nmat('cp039_kerb_stone', (0.55, 0.52, 0.46), (0.66, 0.63, 0.56), 9.0, 0.8, 0.05),
    soil=nmat('cp039_soil', (0.07, 0.045, 0.03), (0.13, 0.085, 0.05), 30.0, 0.95, 0.3),
    box=nmat('cp039_box_hedge', (0.03, 0.09, 0.03), (0.07, 0.17, 0.05), 40.0, 0.7, 0.4, 0.0, 0.3),
    leaf=nmat('cp039_bay_leaf', (0.03, 0.10, 0.03), (0.08, 0.20, 0.05), 25.0, 0.5, 0.15, 0.0, 0.4),
    acanthus=nmat('cp039_acanthus', (0.10, 0.22, 0.07), (0.18, 0.32, 0.10), 12.0, 0.6, 0.05),
    stem=nmat('cp039_stem', (0.18, 0.13, 0.08), (0.26, 0.19, 0.12), 20.0, 0.9, 0.2),
    rose=nmat('cp039_rose', (0.62, 0.06, 0.10), (0.80, 0.18, 0.22), 20.0, 0.6, 0.0),
    pink=nmat('cp039_rose_pink', (0.78, 0.38, 0.45), (0.90, 0.52, 0.58), 20.0, 0.6, 0.0),
    lily=nmat('cp039_lily', (0.84, 0.82, 0.74), (0.94, 0.92, 0.86), 20.0, 0.6, 0.0),
    niche=nmat('cp039_lararium_niche', (0.30, 0.04, 0.03), (0.40, 0.07, 0.04), 8.0, 0.7, 0.02),
    yel=MAT['pomp_yel'], bronze=nmat('cp039_bronze', (0.18, 0.12, 0.05), (0.30, 0.20, 0.08), 12.0, 0.4, 0.02, 0.8),
    jet=MAT.get('water_spray_running') or nmat('cp039_jet', (0.8, 0.85, 0.9), (0.9, 0.95, 1.0), 4.0, 0.2, 0.0),
)
IX = {k: i for i, k in enumerate(M)}

class Kit:
    """bmesh builder, inputs in FEET (world), stored in metres; optional per-face UVs"""
    def __init__(s): s.bm = bmesh.new(); s.uvl = s.bm.loops.layers.uv.new('UVMap')
    def v(s, p): return s.bm.verts.new((p[0] * FT, p[1] * FT, p[2] * FT))
    def poly(s, k, pts, uvs=None):
        f = s.bm.faces.new([s.v(p) for p in pts]); f.material_index = IX[k]
        if uvs:
            for lp, uv in zip(f.loops, uvs): lp[s.uvl].uv = uv
        return f
    def box(s, k, x0, x1, y0, y1, z0, z1):
        x0, x1 = min(x0, x1), max(x0, x1); y0, y1 = min(y0, y1), max(y0, y1); z0, z1 = min(z0, z1), max(z0, z1)
        vs = [s.v(p) for p in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]]
        for fi in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:
            s.bm.faces.new([vs[j] for j in fi]).material_index = IX[k]
    def lathe(s, k, x, y, prof, seg=16):
        rings = [[s.v((x + r * math.cos(2 * math.pi * j / seg), y + r * math.sin(2 * math.pi * j / seg), z)) for j in range(seg)] for r, z in prof]
        for a, b in zip(rings, rings[1:]):
            for j in range(seg):
                j1 = (j + 1) % seg; s.bm.faces.new((a[j], a[j1], b[j1], b[j])).material_index = IX[k]
        s.bm.faces.new(list(reversed(rings[0]))).material_index = IX[k]; s.bm.faces.new(rings[-1]).material_index = IX[k]
    def shaft(s, k, x, y, z0, z1, r0, r1, flutes=20, depth=0.06, seg_per=3):
        n = flutes * seg_per
        def ring(z, r):
            return [s.v((x + (r - depth * 0.5 * (1 - math.cos(2 * math.pi * (j % seg_per) / seg_per))) * math.cos(2 * math.pi * j / n),
                         y + (r - depth * 0.5 * (1 - math.cos(2 * math.pi * (j % seg_per) / seg_per))) * math.sin(2 * math.pi * j / n), z)) for j in range(n)]
        a = ring(z0, r0); b = ring(z1, r1)
        for j in range(n):
            j1 = (j + 1) % n; s.bm.faces.new((a[j], a[j1], b[j1], b[j])).material_index = IX[k]
    def cylax(s, k, a, b, r, seg=14):
        A = Vector(a); B = Vector(b); d = (B - A).normalized(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0))
        u = d.cross(up).normalized(); w = u.cross(d).normalized()
        ra = [s.v(A + (u * math.cos(2 * math.pi * j / seg) + w * math.sin(2 * math.pi * j / seg)) * r) for j in range(seg)]
        rb = [s.v(B + (u * math.cos(2 * math.pi * j / seg) + w * math.sin(2 * math.pi * j / seg)) * r) for j in range(seg)]
        for j in range(seg):
            j1 = (j + 1) % seg; s.bm.faces.new((ra[j], ra[j1], rb[j1], rb[j])).material_index = IX[k]
        s.bm.faces.new(list(reversed(ra))).material_index = IX[k]; s.bm.faces.new(rb).material_index = IX[k]
    def blob(s, k, c, r, seed=0, sub=2, jit=0.18, smooth=False):
        rr = random.Random(seed); bm2 = bmesh.new(); bmesh.ops.create_icosphere(bm2, subdivisions=sub, radius=1.0)
        vm = {}
        for vv in bm2.verts:
            j = 1 + rr.uniform(-jit, jit); vm[vv] = s.v((c[0] + vv.co.x * r[0] * j, c[1] + vv.co.y * r[1] * j, c[2] + vv.co.z * r[2] * j))
        for f in bm2.faces:
            nf = s.bm.faces.new([vm[vv] for vv in f.verts]); nf.material_index = IX[k]; nf.smooth = smooth
        bm2.free()
    def done(s, name, smooth=False):
        me = bpy.data.meshes.new(name); s.bm.to_mesh(me); s.bm.free()
        for m in M.values(): me.materials.append(m)
        if smooth:
            for p in me.polygons: p.use_smooth = True
        o = bpy.data.objects.new(name, me); col.objects.link(o); o['cp_state'] = STATE; return o

def mesh_copy_drop(name, pred, tag):
    """mesh COPY of a r13 object with faces whose world centroid (ft) satisfies pred removed; original hidden"""
    o = bpy.data.objects[name]; me = o.data.copy(); me.name = o.data.name + '_cp039'
    bm = bmesh.new(); bm.from_mesh(me); mw = o.matrix_world
    kill = [f for f in bm.faces if pred((mw @ f.calc_center_median()) / FT)]
    n = len(kill); bmesh.ops.delete(bm, geom=kill, context='FACES'); bm.to_mesh(me); bm.free()
    nw = bpy.data.objects.new(o.name + '_cp039', me); nw.matrix_world = mw.copy()
    for c in o.users_collection: c.objects.link(nw)
    nw['cp039_mesh_copy_of'] = o.name; hide(o); INFO[tag] = n; return nw

# ------------------------------------------------------------------ 1. painted walls
P = Kit()
def wall_plane(k, ax, c, u_a, u_b, z0, z1, W_ft, u_of):
    """vertical textured plane; ax 'x': runs along x at y=c; 'y': along y at x=c. u_of(world coord) -> u ft in image"""
    zz0, zz1 = z0, z1
    if ax == 'x': pts = [(u_a, c, zz0), (u_b, c, zz0), (u_b, c, zz1), (u_a, c, zz1)]
    else: pts = [(c, u_a, zz0), (c, u_b, zz0), (c, u_b, zz1), (c, u_a, zz1)]
    uvs = [(u_of(u_a) / W_ft, zz0 / 19.4), (u_of(u_b) / W_ft, zz0 / 19.4), (u_of(u_b) / W_ft, zz1 / 19.4), (u_of(u_a) / W_ft, zz1 / 19.4)]
    P.poly(k, pts, uvs)
Z0 = 0.085
# end wall (face -y): image left = x -561.4
wall_plane('end', 'x', WE - OFF, PX1 - 0.6, PX0 + 0.6, Z0, 19.4, 66.8, lambda x: x - (PX0 + 0.6))
# west wall (face +x): image left = y 118.5
wall_plane('west', 'y', WW + OFF, PY1 - 0.6, WT, Z0, 19.4, 34.9, lambda y: y - WT)
# tablinum-side wall (face +y): image left = x -494.6; tablinum opening x XC-8..XC+8 below 15.5
uo = lambda x: (PX1 - 0.6) - x
wall_plane('tab', 'x', WT + OFF, PX0 + 0.6, XC - 8, Z0, 19.4, 66.8, uo)
wall_plane('tab', 'x', WT + OFF, XC + 8, PX1 - 0.6, Z0, 19.4, 66.8, uo)
wall_plane('tab', 'x', WT + OFF, XC - 8, XC + 8, 15.5, 19.4, 66.8, uo)
# fix winding so normals face the room (end wall faces -y, west +x, tab +y)
P.bm.normal_update()
for f in P.bm.faces:
    c = f.calc_center_median() / FT
    want = Vector((0, -1, 0)) if abs(c.y - (WE - OFF)) < 0.05 else (Vector((1, 0, 0)) if abs(c.x - (WW + OFF)) < 0.05 else Vector((0, 1, 0)))
    if f.normal.dot(want) < 0: f.normal_flip()
INFO['painted_wall_ft2'] = round(sum(f.calc_area() for f in P.bm.faces) / FT / FT, 1)
P.done('cp039_painted_walls')

# ------------------------------------------------------------------ 2. ambulatory ceiling + beams
Cc = Kit(); ZC = 15.2; T = 8.0
def ceil(x0, x1, y0, y1):
    pts = [(x0, y0, ZC), (x0, y1, ZC), (x1, y1, ZC), (x1, y0, ZC)]       # wound to face down
    Cc.poly('ceil', pts, [(p[0] / T, p[1] / T) for p in pts])
ceil(WW, PX1 - 0.6, WT, PCY0 - 0.7)                 # south (camera side)
ceil(WW, PX1 - 0.6, PCY1 + 0.7, WE)                 # north (end wall)
ceil(WW, PCX0 - 0.7, PCY0 - 0.7, PCY1 + 0.7)        # west
ceil(PCX1 + 0.7, PX1 - 0.6, PCY0 - 0.7, PCY1 + 0.7) # east
for x, y in COLS:                                   # cross beams from every column to the wall
    if y == PCY0: Cc.box('beam', x - 0.35, x + 0.35, WT, y, ZC - 0.55, ZC)
    elif y == PCY1: Cc.box('beam', x - 0.35, x + 0.35, y, WE, ZC - 0.55, ZC)
for y in (PCY0, (PCY0 + PCY1) / 2, PCY1):
    Cc.box('beam', WW, PCX0, y - 0.35, y + 0.35, ZC - 0.55, ZC); Cc.box('beam', PCX1, PX1 - 0.6, y - 0.35, y + 0.35, ZC - 0.55, ZC)
Cc.done('cp039_ambulatory_ceiling')

# ------------------------------------------------------------------ 3. Ionic columns
stc = mesh_copy_drop('pompeian_stucco', lambda c: 4.4 < c.z < 14.31 and any(math.hypot(c.x - x, c.y - y) < 1.05 for x, y in COLS), 'stucco_column_faces_removed')
K = Kit()
for x, y in COLS:
    along_x = y in (PCY0, PCY1)
    K.lathe('red', x, y, [(0.82, 0.0), (0.82, 0.12), (0.78, 0.22), (0.70, 0.30), (0.72, 0.38), (0.64, 0.46)], 20)   # Attic base, red
    K.shaft('stucco', x, y, 4.5, 13.0, 0.62, 0.52, 20, 0.07)
    K.lathe('stucco', x, y, [(0.55, 13.0), (0.58, 13.1), (0.58, 13.2), (0.52, 13.25)], 20)                                 # astragal
    K.lathe('stucco', x, y, [(0.52, 13.25), (0.70, 13.45), (0.68, 13.65), (0.50, 13.7)], 20)                               # echinus
    # volute bolsters: axis perpendicular to the architrave, at +-0.62 ft along it; disc ends read as volutes
    for sgn in (-1, 1):
        cx, cy = (x + sgn * 0.62, y) if along_x else (x, y + sgn * 0.62)
        a = (cx, cy - 0.55, 13.6) if along_x else (cx - 0.55, cy, 13.6); b = (cx, cy + 0.55, 13.6) if along_x else (cx + 0.55, cy, 13.6)
        K.cylax('stucco', a, b, 0.27, 16)
        for e in (a, b):
            o_ = Vector(e) + (Vector(e) - Vector((cx, cy, 13.6))).normalized() * 0.02
            K.cylax('yel', tuple(Vector(e)), tuple(o_), 0.16, 12)                                # gilt eye (the coloured volute centre, I)
    K.box('stucco', x - 0.92, x + 0.92, y - 0.92, y + 0.92, 13.85, 14.3) if False else K.box('stucco', x - 0.9, x + 0.9, y - 0.9, y + 0.9, 13.87, 14.3)
    K.box('stucco', (x - 0.95) if along_x else (x - 0.62), (x + 0.95) if along_x else (x + 0.62), (y - 0.62) if along_x else (y - 0.95), (y + 0.62) if along_x else (y + 0.95), 13.7, 13.87)
K.done('cp039_ionic_columns', smooth=False)

# ------------------------------------------------------------------ 4. pavement, border, kerb
F = Kit(); ZF = 0.09
def fpoly(k, x0, x1, y0, y1, t, rot=False):
    pts = [(x0, y0, ZF), (x1, y0, ZF), (x1, y1, ZF), (x0, y1, ZF)]
    F.poly(k, pts, [((p[1] if rot else p[0]) / t, (p[0] if rot else p[1]) / t) for p in pts])
KO = 1.6     # kerb half-width round the column line
fpoly('floor', WW, PX1 - 0.6, WT, PCY0 - KO - 2, 4.0)
fpoly('floor', WW, PX1 - 0.6, PCY1 + KO + 2, WE, 4.0)
fpoly('floor', WW, PCX0 - KO - 2, PCY0 - KO - 2, PCY1 + KO + 2, 4.0)
fpoly('floor', PCX1 + KO + 2, PX1 - 0.6, PCY0 - KO - 2, PCY1 + KO + 2, 4.0)
# meander border strips (2 ft) just outside the kerb; texture runs along the strip
for (x0, x1, y0, y1, rot) in ((PCX0 - KO - 2, PCX1 + KO + 2, PCY0 - KO - 2, PCY0 - KO, False), (PCX0 - KO - 2, PCX1 + KO + 2, PCY1 + KO, PCY1 + KO + 2, False),
                              (PCX0 - KO - 2, PCX0 - KO, PCY0 - KO, PCY1 + KO, True), (PCX1 + KO, PCX1 + KO + 2, PCY0 - KO, PCY1 + KO, True)):
    pts = [(x0, y0, ZF + 0.002), (x1, y0, ZF + 0.002), (x1, y1, ZF + 0.002), (x0, y1, ZF + 0.002)]
    if rot: uvs = [((p[1]) / 8.0, (p[0] - x0) / 2.0) for p in pts]
    else: uvs = [((p[0]) / 8.0, (p[1] - y0) / 2.0) for p in pts]
    F.poly('border', pts, uvs)
# stylobate kerb ring (stone, 0.35 ft) on the column line
for (x0, x1, y0, y1) in ((PCX0 - KO, PCX1 + KO, PCY0 - KO, PCY0 + KO), (PCX0 - KO, PCX1 + KO, PCY1 - KO, PCY1 + KO),
                         (PCX0 - KO, PCX0 + KO, PCY0 + KO, PCY1 - KO), (PCX1 - KO, PCX1 + KO, PCY0 + KO, PCY1 - KO)):
    F.box('kerb', x0, x1, y0, y1, 0.0, 0.35)
F.done('cp039_pavement_kerb')

# ------------------------------------------------------------------ 5. garden
grn = mesh_copy_drop('pompeian_grn', lambda c: PCX0 + 1.0 < c.x < PCX1 - 1.0 and PCY0 + 1.0 < c.y < PCY1 - 1.0 and c.z < 3.0, 'garden_faces_removed')
G = Kit()
GX0, GX1, GY0, GY1 = PCX0 + KO, PCX1 - KO, PCY0 + KO, PCY1 - KO
G.box('kerb', GX0, GX1, GY0, GY1, 0.0, 0.62)                          # raised bed with stone kerb (pluteus, I)
G.box('soil', GX0 + 0.5, GX1 - 0.5, GY0 + 0.5, GY1 - 0.5, 0.62, 0.9)
YC = (PCY0 + PCY1) / 2
BX = [(GX0 + 1.2, XC - 4.8), (XC + 4.8, GX1 - 1.2)]
BY = [(GY0 + 1.2, YC - 0.9), (YC + 0.9, GY1 - 1.2)]
nbox = 0
for (bx0, bx1) in BX:
    for (by0, by1) in BY:
        for (a0, a1, b0, b1) in ((bx0, bx1, by0, by0 + 0.8), (bx0, bx1, by1 - 0.8, by1), (bx0, bx0 + 0.8, by0, by1), (bx1 - 0.8, bx1, by0, by1)):
            G.box('box', a0, a1, b0, b1, 0.9, 1.75); nbox += 1
        cx_, cy_ = (bx0 + bx1) / 2, (by0 + by1) / 2
        # bay-laurel standard in the middle of each compartment
        G.cylax('stem', (cx_, cy_, 0.9), (cx_, cy_, 5.2), 0.12, 8)
        rr_ = random.Random(int(abs(cx_ * 10 + cy_)))
        for q in range(9):                                     # clipped head: a cluster of leafy lobes
            t = rr_.uniform(0, 6.28); e = rr_.uniform(-0.6, 0.9); rad = 1.0 if q else 0.0
            c3 = (cx_ + rad * 1.0 * math.cos(t) * math.cos(e), cy_ + rad * 1.0 * math.sin(t) * math.cos(e), 6.6 + rad * 1.0 * math.sin(e))
            G.blob('leaf', c3, (0.95, 0.95, 0.9) if q else (1.35, 1.35, 1.4), q * 31 + int(cx_), 3, 0.22, True)
        G.cylax('stem', (cx_, cy_, 5.0), (cx_ + 0.3, cy_ + 0.2, 6.0), 0.07, 6); G.cylax('stem', (cx_, cy_, 5.0), (cx_ - 0.3, cy_ - 0.1, 6.0), 0.07, 6)
        # roses and lilies round it, acanthus in the corners
        for q in range(14):
            rx = RNG.uniform(bx0 + 1.2, bx1 - 1.2); ry = RNG.uniform(by0 + 1.1, by1 - 1.1)
            if math.hypot(rx - cx_, ry - cy_) < 1.0: continue
            kind = RNG.choice(('rose', 'pink', 'lily', 'rose'))
            G.cylax('stem', (rx, ry, 0.9), (rx, ry, 1.9), 0.03, 5)
            G.blob('acanthus', (rx, ry, 1.8), (0.45, 0.45, 0.4), q, 1, 0.25)
            for b in range(5):
                t = RNG.uniform(0, 6.28); G.blob(kind, (rx + 0.38 * math.cos(t), ry + 0.38 * math.sin(t), 2.0 + RNG.uniform(-0.1, 0.25)), (0.12, 0.12, 0.1), b, 1, 0.2)
        for (ax_, ay_) in ((bx0 + 1.3, by0 + 1.3), (bx1 - 1.3, by1 - 1.3)):
            for leaf in range(7):
                t = 2 * math.pi * leaf / 7
                G.poly('acanthus', [(ax_, ay_, 0.95), (ax_ + 1.1 * math.cos(t - 0.25), ay_ + 1.1 * math.sin(t - 0.25), 1.6), (ax_ + 1.5 * math.cos(t), ay_ + 1.5 * math.sin(t), 1.2), (ax_ + 1.1 * math.cos(t + 0.25), ay_ + 1.1 * math.sin(t + 0.25), 1.6)])
# marble krater on a pedestal at the far (west) end of the bed axis (a near-end twin would block the lens, dropped)
for kx in (GX0 + 2.6,):
    G.box('marble', kx - 0.8, kx + 0.8, YC - 0.8, YC + 0.8, 0.9, 3.4)
    G.lathe('marble', kx, YC, [(0.35, 3.4), (0.28, 3.6), (0.22, 3.75), (0.45, 3.85), (0.75, 4.4), (0.95, 5.0), (1.0, 5.15), (0.9, 5.2)], 20)
    G.cylax('marble', (kx - 0.95, YC, 4.85), (kx - 1.15, YC, 4.6), 0.07, 6); G.cylax('marble', (kx + 0.95, YC, 4.85), (kx + 1.15, YC, 4.6), 0.07, 6)
INFO['box_edging_runs'] = nbox
G.done('cp039_peristyle_garden')

# ------------------------------------------------------------------ 6. lararium (No. 18) on the end wall, far west end (image u 10 -> x -551.4)
Lr = Kit(); LXc = WW + 10.0; Y = WE - OFF
Lr.box('kerb', LXc - 1.8, LXc + 1.8, Y - 1.6, Y, 0.09, 3.4)                         # pedestal
Lr.box('kerb', LXc - 2.0, LXc + 2.0, Y - 1.8, Y, 3.4, 3.7)
Lr.box('niche', LXc - 1.1, LXc + 1.1, Y - 0.25, Y, 3.7, 6.6)                         # niche back (red)
for s_ in (-1, 1): Lr.box('marble', LXc + s_ * 1.45 - 0.22, LXc + s_ * 1.45 + 0.22, Y - 1.0, Y, 3.7, 6.6)   # pilasters
Lr.box('marble', LXc - 1.0, LXc + 1.0, Y - 1.0, Y - 0.25, 3.7, 3.8)                  # niche floor
Lr.box('marble', LXc - 1.9, LXc + 1.9, Y - 1.2, Y, 6.6, 7.1)                         # entablature
pv = [(LXc - 1.9, 7.1), (LXc + 1.9, 7.1), (LXc, 8.1)]
Lr.poly('marble', [(u, Y - 1.2, z) for u, z in pv]); Lr.poly('marble', [(u, Y - 0.02, z) for u, z in reversed(pv)])
Lr.poly('marble', [(LXc - 1.9, Y - 1.2, 7.1), (LXc, Y - 1.2, 8.1), (LXc, Y, 8.1), (LXc - 1.9, Y, 7.1)])
Lr.poly('marble', [(LXc + 1.9, Y, 7.1), (LXc, Y, 8.1), (LXc, Y - 1.2, 8.1), (LXc + 1.9, Y - 1.2, 7.1)])
for s_ in (-0.45, 0.45):                                                              # two small bronze Lares (I)
    Lr.lathe('bronze', LXc + s_, Y - 0.6, [(0.16, 3.8), (0.12, 4.6), (0.09, 5.0), (0.07, 5.05), (0.08, 5.2), (0.0, 5.3)], 10)
Lr.done('cp039_lararium')

# ------------------------------------------------------------------ 7. visitors
pp = bpy.data.objects['ppl57_pompeian_visitors']; mw = pp.matrix_world; cl = CAM.location
drop = []
for vv in pp.data.vertices:
    p = mw @ vv.co; q = p / FT
    if (PX0 < q.x < PX1 and TY1 - 12.0 < q.y < PY1) or (p - cl).length < 7.0: drop.append(vv.index)   # peristyle + tablinum (seen through its opening)
pme = pp.data.copy(); pme.name = pp.data.name + '_cp039'
bq = bmesh.new(); bq.from_mesh(pme); bq.verts.ensure_lookup_table()
bmesh.ops.delete(bq, geom=[bq.verts[i] for i in drop], context='VERTS'); bq.to_mesh(pme); bq.free()
pn = bpy.data.objects.new(pp.name + '_cp039', pme); pn.matrix_world = mw.copy()
for c in pp.users_collection: c.objects.link(pn)
for m_ in pp.modifiers:
    nm_ = pn.modifiers.new(m_.name, m_.type)
    if m_.type == 'NODES': nm_.node_group = m_.node_group
for k_ in pp.keys():
    try: pn[k_] = pp[k_]
    except Exception: pass
pn['people_count'] = len(pme.vertices); pn['cp039_mesh_copy_of'] = pp.name; hide(pp)
INFO['pv57_points_dropped'] = len(drop); INFO['pv57_points_kept'] = len(pme.vertices)

def link(o):
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o['cp_state'] = STATE; return o
people = []
def put(name, role, pose, x, y, z, rz, seed, lod):
    person_mesh(name, role, style={'role': role, 'pose': pose, 'lod': lod, 'era': '1850s'}, seed=seed)
    o = bpy.data.objects[name]; link(o); o.location = (x * FT, y * FT, z * FT); o.rotation_euler = (0, 0, rz)
    o['cpl_people'] = 'cpl_people_v3'; people.append(o); return o
def face_to(x, y, tx, ty): return math.atan2(ty - y, tx - x) + math.pi / 2     # people_lib local -y faces forward
SPOTS = [  # (x, y, role, pose, look-at)  - north walk at the end-wall paintings, west walk, far end of the south walk
    (-522.0, 150.0, '1850s_lady', 'standing', (-522.0, 160.0)), (-524.2, 150.6, '1850s_gentleman', 'pointing', (-526.0, 160.0)),
    (-533.5, 149.8, '1850s_lady', 'standing', (-533.0, 160.0)), (-542.0, 149.5, '1850s_gentleman', 'walking', (-560.0, 149.5)),
    (-549.5, 150.2, '1850s_girl', 'standing', (-551.4, 160.0)), (-551.8, 149.7, '1850s_lady', 'standing', (-551.4, 160.0)),
    (-557.6, 131.0, '1850s_gentleman', 'standing', (-570.0, 131.0)), (-558.0, 139.5, '1850s_lady', 'walking', (-558.0, 120.0)),
    (-541.0, 121.8, '1850s_lady', 'walking', (-520.0, 121.8)), (-543.2, 122.6, '1850s_gentleman', 'walking', (-520.0, 122.6)),
    (-529.0, 112.0, '1850s_boy', 'standing', (-529.0, 130.0)),
]
camx, camy = cl.x / FT, cl.y / FT; nearest = 1e9
for n, (x, y, role, pose, tgt) in enumerate(SPOTS):
    d = math.hypot(x - camx, y - camy) * FT
    if d < 8.0: continue
    put(f'cp039_visitor_{n:03d}', role, pose, x, y, ZF, face_to(x, y, *tgt) + RNG.uniform(-0.15, 0.15), 1854390 + n * 13, 'hero' if d < 15 else 'mid')
    nearest = min(nearest, d)
INFO['people_lib_visitors'] = len(people); INFO['nearest_new_figure_m'] = round(nearest, 2)

for o in col.objects: o['cp_state'] = STATE
print('CP039 BUILT', INFO, 'hidden', HIDDEN)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP039 SAVED', OUT)
