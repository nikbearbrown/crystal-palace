"""CP041 CANDIDATE (2026-11-18, no verdict): the Alhambra Court as Owen Jones coloured it, 1854-1856 - painted-stucco sebka
diaper in blue, red and gold over the court's arcades and walls, three inscription-style bands, and the stilted imposts that
carry the arcade screens down onto the column capitals.

usage: blender -b rounds/sydenham-1856-r08b.blend -P scripts/candidate_cp041_polychromy.py [-- out.blend]   (env CP041_NOSAVE=1: no save)
Base = rounds/sydenham-1856-r08b.blend (md5 60c76d85, unchanged since 702eddf, 2026-10-27) - the blend the live hero
  renders/r08bfinal_CAM_CP041_insert_spandrel_50mm.png (md5 33f7133c; COVERAGE.md CP041 hero) was rendered from:
  scripts/render.py -- <dir> r08bfinal 100 48 <cams> (blend's own 1920x1080, Filmic -1.0 EV, 48 spp, no people). The survey
  look v1.1 pass on it was REVERTED (look/sydenham_verdicts.json 'spandrel underexposed; polka valance lost', kept_from
  'before'), so the live hero is that plain render.py frame; re-rendered 2026-11-18 max diff 0.
  -> rounds/candidates/sydenham-1856-r08b_cp041polychromy.blend
Live hero shows: the arcade spandrels, soffits and the court walls behind in a cream ground with regular blue-purple dots
  (the r08 'al_stucco_diaper_OJ' wave-mask diaper renders as polka dots), the welded spandrel strips ending in mid-air
  0.6-0.8 m above the gilt capitals (no impost/stilt between capital and arch), dark crack lines at the strip seams. The
  beat - 'Geometric ornament and coloured surfaces emerge ... Pattern and colour were central to its effect' - does not read.
Adds ONE dated collection SY54_alhambra_court_OJ_polychromy_stilts__1854_1856:
  * cp041_oj_stucco_skin: a painted-stucco skin over every face of the r08b 'al_stucco' mesh (each face copied 6 mm proud on
    BOTH sides along its normal and grown 4 mm in its own plane so the copies close the strip-seam cracks). Material
    cp041_oj_sebka_polychrome: generated (numpy, in this script) tile textures, box-projected in world space:
      - sebka field: lobed (5-cusp) diamond net in deep blue with ivory fillets, red eight-lobed rosette with blue core
        and gold star in each diamond, ivory relief filigree on the gold ground; diamonds 0.45 m wide x 0.485 m high
        (the proportion read from the 1856 guide p.66 woodcut by the workshop prop sy-alhambra-ornament-panel, NOTES.md);
      - three inscription-style bands by height: dado cap 1.37-1.61 m, arcade frieze 5.04-5.33 m (under the r08b gilt
        eaves of the screens), wall frieze 6.98-7.32 m; dark blue ground, gold and red fillets, ivory eight-point star
        roundels alternating with interlace cartouches - ABSTRACT knotwork, no letterforms (no text invented);
      - relief by bump from the pattern height (alpha channel).
  * cp041_oj_stilt_imposts: one stilt block per column (abacus footprint, from the abacus top 3.23 m up into the arcade
    pier above), found by ray-casting up from every r08b capital; same skin material.
Sources: storyboard CP041 (c.1856 SY-EARLY Alhambra Court: 'Geometric ornament and coloured surfaces emerge'; verify
  colours; do not fill from an unrelated Islamic building); 1856 guide pp.66-70 (coloured stucco, 'diaper work ... flowing
  decoration', patterns from other parts of the Alhambra, Jones's casts); coloured print 0108 (gold-dominant with dark
  accents) - R for 'coloured diaper + inscription bands', I for the exact motifs and hues; Owen Jones's blue/red/gold
  primary scheme for the court: R in general (DEPARTURES r08 row 'Alhambra colour'), placement I. Stilted imposts over the
  capitals: R for the Court of the Lions arcades (0108 shows the arches springing from tall blocks over the capitals), I here.
Cameras NOT moved, sun/world/exposure/look NOT changed. Nothing deleted or hidden; r08b geometry and materials untouched.
"""
import bpy, bmesh, math, os, sys
import numpy as np
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP041_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-1856-r08b_cp041polychromy.blend')
STATE = 'SY54_alhambra_court_OJ_polychromy_stilts__1854_1856'
assert bpy.data.collections.get(STATE) is None, 'base already dressed'
FT = 0.3048
n_before = len(bpy.data.objects)
hidden_before = sorted(o.name for o in bpy.data.objects if o.hide_render)
sc = bpy.context.scene
col = bpy.data.collections.new(STATE); sc.collection.children.link(col)
INFO = {}

# ------------------------------------------------------------------ parameters
SKIN_D = 0.006            # m proud of the r08b stucco faces (both sides)
SKIN_GROW = 0.004         # m in-plane growth per face (closes the strip-seam cracks)
DIAMOND_W, DIAMOND_H = 0.45, 0.485     # sebka diamond (workshop sy-alhambra-ornament-panel: proportioned from guide p.66)
BANDS = [('dado_cap', 1.372, 1.61), ('arcade_frieze', 5.04, 5.33), ('wall_frieze', 6.98, 7.32)]   # z0, z1 m (I)
# linear RGB (painted stucco, muted; Owen Jones blue / red / gold scheme, hues I)
GOLD = (0.70, 0.55, 0.30); IVORY = (0.84, 0.77, 0.60); BLUE = (0.075, 0.13, 0.34); RED = (0.48, 0.12, 0.07)

# ------------------------------------------------------------------ generated textures (deterministic, no RNG)
def _put(img, h, m, c, hv): img[m] = c; h[m] = hv
def tex_sebka(N=1024):
    y, x = np.mgrid[0:N, 0:N] / N
    img = np.zeros((N, N, 3)); img[:] = GOLD; h = np.full((N, N), 0.45)
    p = x + y; q = x - y
    def line(a, b, A=0.045, k=5): return np.abs((np.mod(a + 0.5, 1.0) - 0.5) - A * (np.abs(np.sin(np.pi * k * b)) - 0.64))
    d = np.minimum(line(p, q), line(q, p))
    dp = np.mod(p, 1) - 0.5; dq = np.mod(q, 1) - 0.5; r = np.hypot(dp, dq); th = np.arctan2(dq, dp)
    f1 = np.sin(2 * np.pi * 9 * r + 2.2 * np.sin(6 * th))
    f2 = np.sin(2 * np.pi * 14 * (dp * math.cos(.6) + dq * math.sin(.6)) + 3 * np.sin(2 * np.pi * 3 * r))
    fil = ((np.abs(f1) < 0.16) | (np.abs(f2) < 0.10)) & (r < 0.45)
    _put(img, h, fil, np.array(IVORY), 0.62)
    _put(img, h, (np.abs(f1 - 0.35) < 0.08) & (r < 0.45) & ~fil, np.array(GOLD) * 0.72, 0.38)
    rr = 0.17 * (0.70 + 0.30 * np.abs(np.cos(4 * th)))
    _put(img, h, r < rr + 0.012, np.array(IVORY), 0.6); _put(img, h, r < rr, np.array(RED), 0.4)
    _put(img, h, r < 0.085, np.array(BLUE), 0.3)
    _put(img, h, r < 0.055 * (0.7 + 0.3 * np.cos(8 * th)), np.array(GOLD) * 1.1, 0.7)
    leaf = (np.abs(np.abs(dp) - np.abs(dq)) < 0.03 * (1 - np.clip((r - 0.22) / 0.12, 0, 1))) & (r > 0.21) & (r < 0.34)
    _put(img, h, leaf, np.array(BLUE), 0.35)
    _put(img, h, d < 0.034, np.array(IVORY), 0.85); _put(img, h, d < 0.021, np.array(BLUE) * 1.15, 1.0)
    kx = np.minimum(np.mod(p, 1), 1 - np.mod(p, 1)); ky = np.minimum(np.mod(q, 1), 1 - np.mod(q, 1)); kn = np.hypot(kx, ky)
    _put(img, h, kn < 0.042, np.array(RED), 0.9); _put(img, h, kn < 0.022, np.array(GOLD), 1.0)
    return img, h
def tex_band(W=2048, H=512):
    y, x = np.mgrid[0:H, 0:W]; u = x / H; v = y / H
    img = np.zeros((H, W, 3)); img[:] = BLUE; h = np.full((H, W), 0.3)
    _put(img, h, (v < 0.08) | (v > 0.92), np.array(GOLD), 0.95)
    _put(img, h, ((v > 0.08) & (v < 0.12)) | ((v > 0.88) & (v < 0.92)), np.array(RED), 0.6)
    a = np.mod(u, 1.0) - 0.5; cv = v - 0.5; r = np.hypot(a, cv); th = np.arctan2(cv, a)
    odd = (np.floor(u).astype(int) % 2) == 0
    st = 0.29 * (0.82 + 0.18 * np.cos(8 * th))
    _put(img, h, odd & (r < st) & (r > st - 0.04), np.array(IVORY), 1.0)
    _put(img, h, odd & (r < 0.13), np.array(RED), 0.7); _put(img, h, odd & (r < 0.05), np.array(GOLD), 0.9)
    e = np.maximum(np.abs(a) / 0.46, np.abs(cv) / 0.30)
    _put(img, h, (~odd) & (e < 1) & (e > 0.88), np.array(IVORY), 1.0)
    kn = (~odd) & (e < 0.80) & ((np.abs(np.mod((a + cv) * 7, 1) - 0.5) < 0.10) | (np.abs(np.mod((a - cv) * 7, 1) - 0.5) < 0.10))
    _put(img, h, kn, np.array(IVORY) * 0.85, 0.8)
    return img, h
def to_srgb(c):
    c = np.clip(c, 0, 1); return np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(c, 1 / 2.4) - 0.055)
def make_image(name, rgb, hgt):
    H, W = hgt.shape
    im = bpy.data.images.new(name, W, H, alpha=True)
    px = np.concatenate([to_srgb(rgb), hgt[..., None]], axis=2)[::-1].astype(np.float32)   # Blender rows bottom-up
    im.pixels.foreach_set(px.ravel()); im.alpha_mode = 'CHANNEL_PACKED'; im.pack(); im['cp_state'] = STATE
    return im
IM_SEBKA = make_image('cp041_oj_sebka_tile', *tex_sebka())
IM_BAND = make_image('cp041_oj_inscription_band_tile', *tex_band())

# ------------------------------------------------------------------ material: world box-projected sebka + z bands + bump
def oj_material():
    m = bpy.data.materials.new('cp041_oj_sebka_polychrome'); m.use_nodes = True; m['cp_state'] = STATE
    nt = m.node_tree; n = nt.nodes; l = nt.links; b = n['Principled BSDF']
    b.inputs['Roughness'].default_value = 0.62; m.diffuse_color = (*GOLD, 1)
    tc = n.new('ShaderNodeTexCoord'); sep = n.new('ShaderNodeSeparateXYZ'); l.new(tc.outputs['Object'], sep.inputs[0])
    def tex(img, scale, loc):
        mp = n.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = scale; mp.inputs['Location'].default_value = loc
        l.new(tc.outputs['Object'], mp.inputs[0])
        t = n.new('ShaderNodeTexImage'); t.image = img; t.projection = 'BOX'; t.projection_blend = 0.2; t.interpolation = 'Cubic'
        l.new(mp.outputs[0], t.inputs[0]); return t
    t0 = tex(IM_SEBKA, (1 / DIAMOND_W, 1 / DIAMOND_W, 1 / DIAMOND_H), (0, 0, 0))
    col_out, h_out = t0.outputs['Color'], t0.outputs['Alpha']
    for _, z0, z1 in BANDS:
        hh = z1 - z0
        tb = tex(IM_BAND, (1 / (4 * hh), 1 / (4 * hh), 1 / hh), (0, 0, -z0 / hh))
        gt = n.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = z0; l.new(sep.outputs['Z'], gt.inputs[0])
        lt = n.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = z1; l.new(sep.outputs['Z'], lt.inputs[0])
        mk = n.new('ShaderNodeMath'); mk.operation = 'MULTIPLY'; l.new(gt.outputs[0], mk.inputs[0]); l.new(lt.outputs[0], mk.inputs[1])
        mc = n.new('ShaderNodeMix'); mc.data_type = 'RGBA'; l.new(mk.outputs[0], mc.inputs['Factor']); l.new(col_out, mc.inputs[6]); l.new(tb.outputs['Color'], mc.inputs[7])
        mh = n.new('ShaderNodeMix'); mh.data_type = 'FLOAT'; l.new(mk.outputs[0], mh.inputs['Factor']); l.new(h_out, mh.inputs[2]); l.new(tb.outputs['Alpha'], mh.inputs[3])
        col_out, h_out = mc.outputs[2], mh.outputs[0]
    l.new(col_out, b.inputs['Base Color'])
    bp = n.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.45; bp.inputs['Distance'].default_value = 0.004
    l.new(h_out, bp.inputs['Height']); l.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m
OJ = oj_material()

def new_obj(name, bm, mat):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
    o = bpy.data.objects.new(name, me); col.objects.link(o); o['cp_state'] = STATE; return o

# ------------------------------------------------------------------ A. painted-stucco skin over the r08b stucco
src = bpy.data.objects['al_stucco']; Mw = src.matrix_world
assert all(abs(Mw[i][j] - (1.0 if i == j else 0.0)) < 1e-9 for i in range(4) for j in range(4)), 'al_stucco not at identity'
bm = bmesh.new(); nf = 0; area = 0.0
for poly in src.data.polygons:
    nrm = poly.normal
    if nrm.length < 0.5: continue
    vs = [src.data.vertices[k].co.copy() for k in poly.vertices]; c = poly.center
    grown = [v + (v - c).normalized() * SKIN_GROW if (v - c).length > 1e-6 else v for v in vs]
    for s in (1, -1):
        bv = [bm.verts.new(v + nrm * (SKIN_D * s)) for v in grown]
        f = bm.faces.new(bv if s == 1 else list(reversed(bv)))
        nf += 1
    area += poly.area
skin = new_obj('cp041_oj_stucco_skin', bm, OJ)
INFO['skin_faces'] = nf; INFO['stucco_faces_covered'] = len(src.data.polygons); INFO['stucco_area_m2'] = round(area, 1)

# ------------------------------------------------------------------ B. stilted imposts over the capitals
caps = bpy.data.objects['al_capitals']
cb = bmesh.new(); cb.from_mesh(caps.data); cb.verts.ensure_lookup_table()
seen = set(); abaci = []
for v in cb.verts:
    if v.index in seen: continue
    st = [v]; seen.add(v.index); vs = []
    while st:
        a = st.pop(); vs.append(caps.matrix_world @ a.co)
        for e in a.link_edges:
            o2 = e.other_vert(a)
            if o2.index not in seen: seen.add(o2.index); st.append(o2)
    mn = Vector([min(p[i] for p in vs) for i in range(3)]); mx = Vector([max(p[i] for p in vs) for i in range(3)])
    if abs(mx.z - 3.23) < 0.02 and abs(mn.z - 3.11) < 0.02: abaci.append((mn, mx))   # r08b impost/abacus block 3.11-3.23 m
cb.free()
dg = bpy.context.evaluated_depsgraph_get()
def up_hits(mn, mx):
    hs = []
    for i in range(5):
        for j in range(3):
            x = mn.x + (mx.x - mn.x) * (0.1 + 0.8 * i / 4); y = mn.y + (mx.y - mn.y) * (0.2 + 0.6 * j / 2)
            o = Vector((x, y, mx.z + 0.002))
            for _ in range(6):
                ok, loc, nor, idx, ob, _m = sc.ray_cast(dg, o, Vector((0, 0, 1)))
                if not ok or loc.z > 5.0: break
                if ob.name == 'al_stucco': hs.append(loc.z); break
                o = loc + Vector((0, 0, 0.001))
    return hs
bm = bmesh.new(); stilts = []
for mn, mx in abaci:
    hs = sorted(up_hits(mn, mx))
    if len(hs) < 5: continue
    ztop = hs[len(hs) // 2] + 0.04                 # median pier underside, 4 cm into the pier
    x0, x1, y0, y1, z0 = mn.x + 0.01, mx.x - 0.01, mn.y + 0.01, mx.y - 0.01, mx.z
    vs = [bm.verts.new((x, y, z)) for x in (x0, x1) for y in (y0, y1) for z in (z0, ztop)]
    for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)): bm.faces.new([vs[k] for k in f])
    stilts.append((round((x0 + x1) / 2, 2), round((y0 + y1) / 2, 2), round(z0, 3), round(ztop, 3), len(hs)))
bm.normal_update()
for f in bm.faces: f.normal_update()
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
stilt = new_obj('cp041_oj_stilt_imposts', bm, OJ)
INFO['abaci'] = len(abaci); INFO['stilts'] = len(stilts)
INFO['stilt_height_m'] = (round(min(s[3] - s[2] for s in stilts), 3), round(max(s[3] - s[2] for s in stilts), 3)) if stilts else None
stilt['stilts'] = str(stilts)

col['cp_state'] = STATE
col['evidence'] = ('storyboard CP041 c.1856 SY-EARLY Alhambra Court, geometric ornament and coloured surfaces (R as brief); 1856 guide pp.66-70 coloured '
                   'stucco diaper work, patterns from other parts of the Alhambra, Jones casts (R as text); print 0108 gold-dominant with dark accents '
                   '(R); sebka diamond proportion from guide p.66 woodcut via workshop sy-alhambra-ornament-panel (R ratio, I size); Owen Jones '
                   'blue/red/gold scheme (R in general, I placement); bands abstract knotwork, no text (I); stilted imposts over capitals (R type, I here)')
bpy.context.view_layer.update()
INFO['objects'] = len(col.objects); INFO['new_objects_total'] = len(bpy.data.objects) - n_before
assert sorted(o.name for o in bpy.data.objects if o.hide_render) == hidden_before
assert len(bpy.data.objects) - n_before == len(col.objects), 'every new object must be in the one dated collection'
print('CP041 BUILT', INFO)
print('CP041 STILTS', stilts)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP041 SAVED', OUT)
