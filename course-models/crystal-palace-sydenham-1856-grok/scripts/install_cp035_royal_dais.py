"""CP035 CANDIDATE (2026-11-17, no verdict): 'The second opening' - royal dais in the central transept, 10 June 1854.

usage: blender -b rounds/sydenham-open54-r16.blend -P scripts/install_cp035_royal_dais.py [-- out.blend]
       (env CP035_NOSAVE=1: build in memory only)
Opens the live CP035 round rounds/sydenham-open54-r16.blend (md5 683b1bc9; never written) ->
rounds/candidates/sydenham-open54-r16_cp035dais.blend.
Live hero renders/r16/r16_CAM_CP035_transept_gallery_28mm.png (1280x720, 28 spp, NO_PEOPLE, blend lighting Filmic -1.0 EV)
shows: a crude 32 x 44 ft red box dais with a flat red 'roof' canopy over its west half and a red block 'throne' at the
WEST end facing the orchestra (D-R14-O1, U); the royal party as a handful of pv57 cone figures mixed with nave-lining
crowd points that stand ON the dais; the gallery front the camera stands on has no railing at all, and a pv57 crinoline
point 2.7 m from the lens is a huge pale blob at the left edge.
Adds dated collection SY54_royal_dais__10Jun1854 (cp_state SY54_opening_royal_dais__10Jun1854) and:
  1. dais rebuilt on the same 32 x 44 ft footprint (x -46..-14 ft, y +-22 ft, 3 ft high, crimson cloth, gilt fringe band):
     carpeted three-step central flight on the WEST front, raised haut-pas at the EAST end with the chair of state facing
     WEST - Queen Victoria's journal (10 Jun 1854): 'Immediately behind us rose the enormous Orchestra' (R; the choir stand
     is x 70..172 ft, east of the dais) - so the r14 throne orientation (facing the orchestra) is reversed; small crimson
     canopy with scalloped gilt-fringed valance and dossal over the throne only (U: canopy not in the texts found);
     low gilt rails along the dais sides; crimson carpet runner from the steps westward (I);
     flower vases on pedestals at the dais corners, flanking the steps and the throne (R: 'a dais was erected for her
     Majesty and the royal party, with vases full of the choicest flowers', e-rara vol. III p.[216]; forms I);
  2. pv57 points standing on / crowding the dais (old royal-party + yeomen points and the east ends of the nave-lining
     rows) dropped from a mesh COPY of ppl54_opening_day (original hidden, not deleted), re-dressed as people_lib v3.4
     figures: Queen, Prince Albert (uniform), Prince of Wales, Prince Alfred, Princess Royal, Princess Alice, King of
     Portugal, Duke of Oporto (R: party named in the e-rara vol. III p.[217]), ladies of the household, ministers
     on one side and foreign ambassadors in coloured uniforms on the other (R: 'members of the government were arranged on
     one side, and the foreign ambassadors, in their rich costumes, on the other'), Laing with the address on the steps (R:
     'advanced to the foot of the throne'), yeomen of the guard in scarlet lining the flight and the dais sides (I);
  3. gallery-front railings (3 ft 6 in, cast-iron dog-bars, timber cap; I/R-typical) on every free nave/transept edge of
     the existing gallery floors (both tiers) - the galleries had nothing between the crowds and a 23 ft drop;
  4. pv57 gallery points within 9 m of the hero lens dropped (same mesh copy) - the 2.7 m pale crinoline blob is gone;
     3 people_lib spectators at the rail 8-11 m from the lens.
Cameras NOT moved, sun/world/exposure NOT changed (Filmic -1.0 EV). Units metres in the blend; feet in DEPARTURES.
"""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view as w2c

FT = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from cpl_people import person_mesh

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP035_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-open54-r16_cp035dais.blend')
STATE = 'SY54_opening_royal_dais__10Jun1854'
RNG = random.Random(1854035)
sc = bpy.context.scene
CAM = bpy.data.objects['CAM_CP035_transept_gallery_28mm']
COLL = 'SY54_royal_dais__10Jun1854'
col = bpy.data.collections.get(COLL) or bpy.data.collections.new(COLL)
if col.name not in [c.name for c in sc.collection.children]: sc.collection.children.link(col)
col['cp_state'] = STATE
col['evidence'] = ('dais in the centre of the building with vases of flowers R (e-rara vol. III [216]); royal party, government one side, '
                   'ambassadors other side R (e-rara vol. III [217]); orchestra behind the Queen R (QV journal 10 Jun 1854); footprint/heights U (r14); '
                   'canopy U; forms, colours, positions I; gallery railing form I')
INFO = {}
HIDDEN = []
def link(o):
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o['cp_state'] = STATE; return o
def hide(o):
    o.hide_render = True; o.hide_viewport = True; o['cp035_hidden_by_candidate'] = True; HIDDEN.append(o.name)

# ------------------------------------------------------------------ materials
def nmat(name, c0, c1, scale=6.0, rough=0.9, bump=0.1, metal=0.0, spec=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; t = m.node_tree; N = t.nodes; L = t.links
    b = N['Principled BSDF']; tc = N.new('ShaderNodeTexCoord'); nz = N.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = 6.0; L.new(tc.outputs['Object'], nz.inputs['Vector'])
    rp = N.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = (*c0, 1); rp.color_ramp.elements[1].color = (*c1, 1)
    rp.color_ramp.elements[0].position = 0.3; rp.color_ramp.elements[1].position = 0.72
    L.new(nz.outputs['Fac'], rp.inputs[0]); L.new(rp.outputs[0], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    b.inputs['Specular IOR Level'].default_value = 0.15 if spec is None else spec
    if bump:
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; L.new(nz.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs[0], b.inputs['Normal'])
    m.diffuse_color = (*c1, 1); return m

def velvet(name, c0, c1):
    """crimson cloth: noise colour + sheen (velvet/baize) so it does not read as plastic"""
    m = nmat(name, c0, c1, 9.0, 0.85, 0.08)
    b = m.node_tree.nodes['Principled BSDF']
    if 'Sheen Weight' in b.inputs:
        b.inputs['Sheen Weight'].default_value = 0.25; b.inputs['Sheen Tint'].default_value = (0.6, 0.08, 0.08, 1)
    b.inputs['Specular IOR Level'].default_value = 0.05
    return m

M = dict(
    crimson=velvet('cp035_crimson_cloth', (0.22, 0.012, 0.02), (0.33, 0.03, 0.04)),
    carpet=velvet('cp035_crimson_carpet', (0.17, 0.015, 0.02), (0.27, 0.035, 0.035)),
    gilt=nmat('cp035_gilt', (0.42, 0.29, 0.08), (0.62, 0.46, 0.16), 14.0, 0.32, 0.05, metal=0.85, spec=0.5),
    fringe=nmat('cp035_gold_fringe', (0.40, 0.28, 0.08), (0.58, 0.43, 0.14), 40.0, 0.5, 0.3, metal=0.5),
    stone=nmat('cp035_vase_pedestal', (0.55, 0.52, 0.47), (0.66, 0.63, 0.57), 4.0, 0.6, 0.05),
    leaf=nmat('cp035_foliage', (0.03, 0.07, 0.02), (0.07, 0.14, 0.04), 30.0, 0.7, 0.2),
    bloomW=nmat('cp035_bloom_white', (0.62, 0.60, 0.55), (0.72, 0.70, 0.64), 30.0, 0.6, 0.1),
    bloomP=nmat('cp035_bloom_pink', (0.55, 0.22, 0.30), (0.68, 0.32, 0.40), 30.0, 0.6, 0.1),
    bloomR=nmat('cp035_bloom_red', (0.40, 0.03, 0.04), (0.52, 0.06, 0.06), 30.0, 0.6, 0.1),
    bloomY=nmat('cp035_bloom_yellow', (0.60, 0.45, 0.06), (0.70, 0.56, 0.12), 30.0, 0.6, 0.1),
    bloomV=nmat('cp035_bloom_violet', (0.22, 0.12, 0.38), (0.32, 0.20, 0.48), 30.0, 0.6, 0.1),
    iron=nmat('cp035_rail_iron_OJ_blue', (0.085, 0.145, 0.36), (0.10, 0.17, 0.42), 8.0, 0.45, 0.0, metal=0.2, spec=0.5),   # = iron_painted_OJ blue
    cap=nmat('cp035_rail_mahogany_cap', (0.10, 0.04, 0.02), (0.17, 0.07, 0.035), 6.0, 0.4, 0.0),
    paper=nmat('cp035_address_vellum', (0.62, 0.58, 0.48), (0.70, 0.66, 0.56), 4.0, 0.7, 0.0),
)
ML = list(M.values()); IX = {k: i for i, k in enumerate(M)}

class Kit:
    """bmesh builder, metres, world coords"""
    def __init__(s): s.bm = bmesh.new()
    def _t(s, k, n0):
        s.bm.faces.ensure_lookup_table()
        for j in range(n0, len(s.bm.faces)): s.bm.faces[j].material_index = IX[k]
    def box(s, k, x0, x1, y0, y1, z0, z1):
        n0 = len(s.bm.faces); vs = [s.bm.verts.new(p) for p in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]]
        for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]: s.bm.faces.new([vs[j] for j in f])
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
    def bar(s, k, a, b, w, t=None):
        t = t or w; A = Vector(a); B = Vector(b); d = B - A
        if d.length < 1e-6: return
        d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0)); sd = d.cross(up).normalized(); u = sd.cross(d).normalized()
        n0 = len(s.bm.faces); pts = [s.bm.verts.new(p + sd * (i * w / 2) + u * (j * t / 2)) for p in (A, B) for (i, j) in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        for f in [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]: s.bm.faces.new([pts[j] for j in f])
        s._t(k, n0)
    def lathe(s, k, cx, cy, prof, seg=16):
        """profile [(r, z)] revolved about the vertical through (cx, cy)"""
        n0 = len(s.bm.faces); rings = []
        for r, z in prof:
            rings.append([s.bm.verts.new((cx + max(r, 1e-4) * math.cos(2 * math.pi * j / seg), cy + max(r, 1e-4) * math.sin(2 * math.pi * j / seg), z)) for j in range(seg)])
        for a, b in zip(rings, rings[1:]):
            for j in range(seg): s.bm.faces.new([a[j], a[(j + 1) % seg], b[(j + 1) % seg], b[j]])
        s.bm.faces.new(list(reversed(rings[0]))); s.bm.faces.new(rings[-1]); s._t(k, n0)
    def ell(s, k, c, radii, seg=10, rings=6):
        n0 = len(s.bm.faces)
        mat = Matrix.Translation(Vector(c)) @ Matrix.Diagonal((*radii, 1))
        bmesh.ops.create_uvsphere(s.bm, u_segments=seg, v_segments=rings, radius=1.0, matrix=mat); s._t(k, n0)
    def done(s, name, smooth=False):
        me = bpy.data.meshes.new(name); s.bm.normal_update(); s.bm.to_mesh(me); s.bm.free()
        for m in ML: me.materials.append(m)
        if smooth:
            for p in me.polygons: p.use_smooth = True
        ob = bpy.data.objects.new(name, me); col.objects.link(ob); ob['cp_state'] = STATE
        return ob

# ------------------------------------------------------------------ 1. dais (same footprint as r14 open54_dais)
X0, X1, YH, ZD = -46 * FT, -14 * FT, 22 * FT, 3 * FT          # platform x -14.02..-4.27 m, y +-6.71 m, top 0.914 m
for n in ('open54_dais', 'open54_dais_gilt'): hide(bpy.data.objects[n])
k = Kit()
k.box('crimson', X0, X1, -YH, YH, 0.0, ZD - 0.02)
k.box('carpet', X0 + 0.02, X1 - 0.02, -YH + 0.02, YH - 0.02, ZD - 0.02, ZD)
# gilt fascia band + bullion fringe on all four faces (6 in band at the top of the 3 ft fascia)
for (xa, xb, ya, yb) in ((X0 - 0.03, X1 + 0.03, -YH - 0.03, -YH + 0.01), (X0 - 0.03, X1 + 0.03, YH - 0.01, YH + 0.03),
                         (X0 - 0.03, X0 + 0.01, -YH - 0.03, YH + 0.03), (X1 - 0.01, X1 + 0.03, -YH - 0.03, YH + 0.03)):
    k.box('gilt', xa, xb, ya, yb, ZD - 0.07, ZD + 0.01)
    k.box('fringe', xa - 0.005, xb + 0.005, ya - 0.005, yb + 0.005, ZD - 0.20, ZD - 0.07)
# west flight: three 1 ft risers, 20 ft wide (I), carpeted, gilt nosings
SW = 10 * FT
for i in range(3):
    xa = X0 - (3 - i) * 0.30; z1 = (i + 1) * ZD / 3
    k.box('crimson', xa, X0, -SW, SW, 0.0, z1 - 0.015); k.box('carpet', xa, X0, -SW + 0.5, SW - 0.5, z1 - 0.015, z1)
    k.box('gilt', xa - 0.012, xa + 0.02, -SW, SW, z1 - 0.03, z1 + 0.004)
# carpet runner from the flight westward along the nave (12 ft wide, 30 ft long; I)
k.box('carpet', X0 - 0.9 - 30 * FT, X0 - 0.9, -6 * FT, 6 * FT, 0.0, 0.012)
k.box('gilt', X0 - 0.9 - 30 * FT, X0 - 0.9, -6 * FT - 0.06, -6 * FT, 0.0, 0.014); k.box('gilt', X0 - 0.9 - 30 * FT, X0 - 0.9, 6 * FT, 6 * FT + 0.06, 0.0, 0.014)
# haut-pas at the east end (8 x 16 ft, +1 ft) for the chair of state
HX0, HY, ZH = X1 - 8 * FT, 8 * FT, ZD + 1 * FT
k.box('crimson', HX0, X1 - 0.05, -HY, HY, ZD, ZH - 0.015); k.box('carpet', HX0, X1 - 0.05, -HY, HY, ZH - 0.015, ZH)
k.box('gilt', HX0 - 0.015, HX0 + 0.02, -HY, HY, ZH - 0.04, ZH + 0.004)
k.box('fringe', HX0 - 0.02, HX0, -HY, HY, ZH - 0.16, ZH - 0.04)
# chair of state facing WEST (-x): seat 18 in above the haut-pas, back 5 ft 6 in, gilt frame, crimson upholstery (forms I)
TX = X1 - 0.95
k.box('gilt', TX - 0.36, TX + 0.36, -0.42, 0.42, ZH, ZH + 0.40)                     # seat rail / base
k.box('crimson', TX - 0.34, TX + 0.34, -0.38, 0.38, ZH + 0.40, ZH + 0.50)          # cushion
k.box('gilt', TX + 0.30, TX + 0.42, -0.44, 0.44, ZH, ZH + 1.68)                     # back frame
k.box('crimson', TX + 0.27, TX + 0.31, -0.36, 0.36, ZH + 0.52, ZH + 1.58)          # back panel
for sy in (-1, 1):
    k.box('gilt', TX - 0.38, TX + 0.36, sy * 0.40 - 0.05, sy * 0.40 + 0.05, ZH + 0.40, ZH + 0.72)   # arm
    k.cyl('gilt', (TX - 0.36, sy * 0.40, ZH), (TX - 0.36, sy * 0.40, ZH + 0.74), 0.045, 8)
k.ell('gilt', (TX + 0.36, 0, ZH + 1.78), (0.07, 0.30, 0.16))                        # crown cresting
k.ell('gilt', (TX + 0.36, 0, ZH + 1.96), (0.06, 0.06, 0.07))
k.box('crimson', TX - 0.85, TX - 0.45, -0.28, 0.28, ZH, ZH + 0.16)                  # footstool
k.box('gilt', TX - 0.86, TX - 0.44, -0.29, 0.29, ZH + 0.14, ZH + 0.17)
# canopy over the throne only (U): 4 gilt posts, tester 9 x 16 ft at 15 ft above the dais, scalloped valance, dossal
CX0, CX1, CY, CZ = HX0 - 0.15, X1 - 0.1, HY - 0.1, ZD + 15 * FT
for xx in (CX0, CX1):
    for sy in (-1, 1):
        k.cyl('gilt', (xx, sy * CY, ZH if xx > HX0 else ZD), (xx, sy * CY, CZ), 0.07, 12)
        k.cyl('gilt', (xx, sy * CY, ZD if xx <= HX0 else ZH), (xx, sy * CY, (ZD if xx <= HX0 else ZH) + 0.25), 0.13, 12, r2=0.09)
        k.ell('gilt', (xx, sy * CY, CZ + 0.55), (0.12, 0.12, 0.16))
k.box('crimson', CX0 - 0.12, CX1 + 0.12, -CY - 0.12, CY + 0.12, CZ, CZ + 0.42)
k.box('gilt', CX0 - 0.15, CX1 + 0.15, -CY - 0.15, CY + 0.15, CZ + 0.40, CZ + 0.48)
k.box('gilt', CX0 - 0.15, CX1 + 0.15, -CY - 0.15, CY + 0.15, CZ - 0.03, CZ + 0.02)
def valance(p0, p1, z, n, drop=0.38):
    P0 = Vector(p0); P1 = Vector(p1)
    for i in range(n):
        a = P0 + (P1 - P0) * (i / n); b = P0 + (P1 - P0) * ((i + 1) / n); m_ = (a + b) / 2
        d = (b - a); nrm = Vector((-d.y, d.x, 0)).normalized() * 0.02
        bm = k.bm; n0 = len(bm.faces)
        vs = [bm.verts.new((a.x, a.y, z)), bm.verts.new((b.x, b.y, z)), bm.verts.new((b.x, b.y, z - drop * 0.55)),
              bm.verts.new((m_.x, m_.y, z - drop)), bm.verts.new((a.x, a.y, z - drop * 0.55))]
        bm.faces.new(vs); k._t('crimson', n0)
        n0 = len(bm.faces)
        for q0, q1 in ((vs[2], vs[3]), (vs[3], vs[4])):
            e0 = bm.verts.new(q0.co + nrm); e1 = bm.verts.new(q1.co + nrm); e2 = bm.verts.new(q1.co + nrm + Vector((0, 0, -0.08))); e3 = bm.verts.new(q0.co + nrm + Vector((0, 0, -0.08)))
            bm.faces.new((e0, e1, e2, e3))
        k._t('fringe', n0)
E = 0.13
valance((CX0 - E, -CY - E), (CX0 - E, CY + E), CZ, 9)
valance((CX0 - E, CY + E), (CX1 + E, CY + E), CZ, 5)
valance((CX1 + E, CY + E), (CX1 + E, -CY - E), CZ, 9)
valance((CX1 + E, -CY - E), (CX0 - E, -CY - E), CZ, 5)
k.box('crimson', CX1 - 0.06, CX1 - 0.01, -CY + 0.05, CY - 0.05, ZH, CZ)          # dossal behind the chair
k.box('gilt', CX1 - 0.07, CX1 - 0.05, -0.9, 0.9, ZH + 2.6, ZH + 2.66)
k.ell('gilt', ((CX0 + CX1) / 2, 0, CZ + 0.72), (0.32, 0.32, 0.26), 12, 8)       # crown on the tester
k.ell('crimson', ((CX0 + CX1) / 2, 0, CZ + 0.80), (0.24, 0.24, 0.2), 12, 8)
k.ell('gilt', ((CX0 + CX1) / 2, 0, CZ + 1.08), (0.07, 0.07, 0.09))
# low gilt rails along the north/south dais edges and the west front (gap for the flight)
RH = 2.5 * FT
def rail(p0, p1):
    P0 = Vector(p0); P1 = Vector(p1); L_ = (P1 - P0).length; n = max(2, int(L_ / 0.9))
    k.cyl('gilt', (P0.x, P0.y, ZD + RH), (P1.x, P1.y, ZD + RH), 0.035, 8)
    k.cyl('gilt', (P0.x, P0.y, ZD + 0.12), (P1.x, P1.y, ZD + 0.12), 0.02, 6)
    for i in range(n + 1):
        q = P0 + (P1 - P0) * (i / n)
        k.lathe('gilt', q.x, q.y, [(0.06, ZD), (0.05, ZD + 0.08), (0.025, ZD + 0.14), (0.03, ZD + 0.4), (0.022, ZD + RH - 0.05), (0.045, ZD + RH + 0.04), (0.001, ZD + RH + 0.10)], 8)
ri = 0.12
rail((X0 + ri, -YH + ri), (X1 - ri, -YH + ri)); rail((X0 + ri, YH - ri), (X1 - ri, YH - ri))
rail((X0 + ri, -YH + ri), (X0 + ri, -SW - 0.3)); rail((X0 + ri, SW + 0.3), (X0 + ri, YH - ri))
# flower vases on pedestals (R: 'vases full of the choicest flowers'; forms, colours I)
BLOOMS = ['bloomW', 'bloomW', 'bloomP', 'bloomP', 'bloomR', 'bloomY', 'bloomV']
def vase(x, y, z0, s=1.0, seed=0):
    r = random.Random(seed)
    k.lathe('stone', x, y, [(0.30*s, z0), (0.30*s, z0+0.10*s), (0.20*s, z0+0.14*s), (0.17*s, z0+0.75*s), (0.24*s, z0+0.80*s), (0.24*s, z0+0.86*s)], 16)
    zz = z0 + 0.86 * s
    k.lathe('gilt', x, y, [(0.10*s, zz), (0.07*s, zz+0.10*s), (0.10*s, zz+0.16*s), (0.32*s, zz+0.36*s), (0.36*s, zz+0.44*s), (0.30*s, zz+0.46*s)], 16)
    zt = zz + 0.44 * s
    k.ell('leaf', (x, y, zt + 0.10 * s), (0.42 * s, 0.42 * s, 0.30 * s), 12, 7)
    for i in range(150):
        a = r.uniform(0, 2 * math.pi); e = r.uniform(0.05, 1.25); rr = 0.40 * s
        px = x + rr * math.cos(a) * math.cos(e) * 1.02; py = y + rr * math.sin(a) * math.cos(e) * 1.02; pz = zt + 0.10 * s + 0.30 * s * math.sin(e) * 1.05
        k.ell(r.choice(BLOOMS), (px, py, pz), (0.036 * s, 0.036 * s, 0.03 * s), 6, 4)
    for i in range(10):       # trailing fronds over the rim
        a = r.uniform(0, 2 * math.pi)
        k.ell('leaf', (x + 0.40 * s * math.cos(a), y + 0.40 * s * math.sin(a), zt - 0.04 * s), (0.10 * s, 0.10 * s, 0.14 * s), 6, 4)
vs_ = [(X0 + 0.45, -YH + 0.45, ZD), (X0 + 0.45, YH - 0.45, ZD),
       (X0 - 1.15, -SW - 0.55, 0.0), (X0 - 1.15, SW + 0.55, 0.0), (HX0 + 0.35, -HY + 0.35, ZH), (HX0 + 0.35, HY - 0.35, ZH)]
for i, (x, y, z) in enumerate(vs_): vase(x, y, z, 0.85 if z >= ZH else 1.0, 18540 + i)
# the address (vellum roll) in Laing's hand is placed with the figures below
dais = k.done('cp035_royal_dais', smooth=False)
INFO['dais_faces'] = len(dais.data.polygons)

# ------------------------------------------------------------------ 3. gallery-front railings on free gallery edges
# 3 ft 6 in, mahogany cap on an iron top rail, bottom rail, stanchions every 8 ft, open diamond lattice of flat bars (form I)
gf = bpy.data.objects['gallery_floors']; gw = gf.matrix_world
tops = []
for p in gf.data.polygons:
    if p.normal.z > 0.9:
        vs = [gw @ gf.data.vertices[i].co for i in p.vertices]
        tops.append((min(v.x for v in vs), max(v.x for v in vs), min(v.y for v in vs), max(v.y for v in vs), round(vs[0].z, 2)))
def covered(x, y, z):
    return any(a - 1e-3 <= x <= b + 1e-3 and c - 1e-3 <= y <= d + 1e-3 and abs(z - zz) < 0.05 for a, b, c, d, zz in tops)
kr = Kit(); RL = 3.5 * FT; RAILS = []; length = 0.0
for (a, b, c, d, z) in tops:
    for (p0, p1, out) in (((a, c), (b, c), (0, -1)), ((b, c), (b, d), (1, 0)), ((b, d), (a, d), (0, 1)), ((a, d), (a, c), (-1, 0))):
        if out[1] != 0 and abs(p0[1]) > 32.9: continue                                  # outer walls
        if out[0] != 0 and abs(p0[0]) > 245.0: continue                                 # building ends
        if out[1] != 0 and z > 10 and abs(abs(p0[1]) - 18.29) < 0.05: continue          # upper-tier back edge
        P0 = Vector((*p0, z)); P1 = Vector((*p1, z)); L_ = (P1 - P0).length
        nS = max(1, int(L_ / 0.5)); run = None; last = None
        for i in range(nS + 1):
            q = P0 + (P1 - P0) * (i / nS)
            free = not covered(q.x + out[0] * 0.3, q.y + out[1] * 0.3, z)
            if free:
                if run is None: run = q.copy()
                last = q.copy()
            if (not free or i == nS) and run is not None:
                if (last - run).length > 0.4: RAILS.append((run, last, Vector((out[0], out[1], 0)), z))
                run = None
for (A0, B0, out, z) in RAILS:
    off = out * -0.05; A = A0 + off; B = B0 + off; Lr = (B - A).length; dd = (B - A).normalized(); length += Lr
    zc = z + RL
    kr.bar('cap', (A.x, A.y, zc - 0.035), (B.x, B.y, zc - 0.035), 0.09, 0.07)
    kr.bar('iron', (A.x, A.y, zc - 0.10), (B.x, B.y, zc - 0.10), 0.03, 0.06)
    kr.bar('iron', (A.x, A.y, z + 0.10), (B.x, B.y, z + 0.10), 0.03, 0.06)
    nb = max(1, int(round(Lr / (8 * FT))))
    for j in range(nb + 1):
        q = A + (B - A) * (j / nb); kr.bar('iron', (q.x, q.y, z), (q.x, q.y, zc - 0.07), 0.05, 0.05)
    nm = max(1, int(round(Lr / 0.6)))                 # diamond lattice modules ~2 ft
    for j in range(nm):
        q0 = A + (B - A) * (j / nm); q1 = A + (B - A) * ((j + 1) / nm)
        kr.bar('iron', (q0.x, q0.y, z + 0.13), (q1.x, q1.y, zc - 0.13), 0.016, 0.008)
        kr.bar('iron', (q1.x, q1.y, z + 0.13), (q0.x, q0.y, zc - 0.13), 0.016, 0.008)
rails = kr.done('cp035_gallery_front_railings')
INFO['rail_runs'] = len(RAILS); INFO['rail_m'] = round(length, 1)

# ------------------------------------------------------------------ 2+4. pv57 point edits (mesh COPIES of every PPL57 crowd carrier)
# r16 people() also adds 4 'hero silhouettes' 9.5 ft round EVERY camera to EVERY crowd carrier, so six figures are stacked
# 2.9 m from the hero lens (the pale blob, left edge). Per carrier: drop points on/at the dais and the approach, drop gallery
# points within 9 m of the hero lens, and push gallery-front points that would stand in the new railing 0.45 m back.
cl = CAM.location.copy()
def rail_push(p):
    for (A0, B0, out, z) in RAILS:
        if abs(p.z - z) > 0.2: continue
        ab = (B0 - A0); t = (p - A0).dot(ab) / ab.length_squared
        if not (-0.02 <= t <= 1.02): continue
        dout = (p - A0).dot(out)                       # > 0 = over the void, < 0 = on the floor
        if -0.45 < dout <= 0.05: return p - out * (dout + 0.45)
    return None
carriers = [o for o in bpy.data.objects if o.type == 'MESH' and not o.hide_render and
            any(m.type == 'NODES' and m.node_group and m.node_group.name.startswith('PPL57_instance_people') for m in o.modifiers)]
ND = NG = NP = 0; COPIES = []
for pp in carriers:
    mw = pp.matrix_world; mi = mw.inverted(); drop = []; moves = {}
    for v in pp.data.vertices:
        p = mw @ v.co
        on_dais = (X0 - 1.9) <= p.x <= X1 + 0.6 and abs(p.y) <= YH + 1.3 and p.z < 3.0
        approach = (X0 - 0.9 - 30 * FT) <= p.x < X0 - 1.9 and abs(p.y) <= 6 * FT + 0.4 and p.z < 1.0
        near_lens = p.z > 6.5 and (p - cl).length < 9.0
        if on_dais or approach: drop.append(v.index); ND += 1
        elif near_lens: drop.append(v.index); NG += 1
        elif p.z > 6.5:
            q = rail_push(p)
            if q is not None: moves[v.index] = mi @ q
    if not drop and not moves: continue
    pme = pp.data.copy(); pme.name = pp.data.name + '_cp035'
    for i, co in moves.items(): pme.vertices[i].co = co
    NP += len(moves)
    bq = bmesh.new(); bq.from_mesh(pme); bq.verts.ensure_lookup_table()
    bmesh.ops.delete(bq, geom=[bq.verts[i] for i in drop], context='VERTS'); bq.to_mesh(pme); bq.free()
    pn = bpy.data.objects.new(pp.name + '_cp035', pme); pn.matrix_world = mw.copy()
    for c in pp.users_collection: c.objects.link(pn)
    for m_ in pp.modifiers:
        nm_ = pn.modifiers.new(m_.name, m_.type)
        if m_.type == 'NODES': nm_.node_group = m_.node_group
        for k_ in m_.keys():
            try: nm_[k_] = m_[k_]
            except Exception: pass
    for k_ in pp.keys():
        try: pn[k_] = pp[k_]
        except Exception: pass
    pn['people_count'] = len(pme.vertices); pn['cp035_mesh_copy_of'] = pp.name; pn['cp_state'] = pp.get('cp_state', ''); hide(pp)
    COPIES.append(pn.name)
INFO['pv57_dais_points_dropped'] = ND; INFO['pv57_gallery_points_dropped'] = NG; INFO['pv57_rail_points_pushed'] = NP; INFO['carrier_copies'] = len(COPIES)

# ------------------------------------------------------------------ people_lib figures + costumes
people = []
def face(x, y, tx, ty): return math.atan2(tx - x, -(ty - y)) + math.pi      # local -y toward (tx, ty)
def put_person(name, role, pose, x, y, z, rz, seed, lod='mid', costume=None):
    person_mesh(name, role, style={'role': role, 'pose': pose, 'lod': lod, 'era': '1850s'}, seed=seed)
    o = bpy.data.objects[name]; link(o); o.location = (x, y, z); o.rotation_euler = (0, 0, rz)
    o['cpl_people'] = 'cpl_people_v3'
    if costume:
        o.data = o.data.copy(); o.data.name = name + '_dress'
        for i_, m_ in enumerate(o.data.materials):
            if not m_: continue
            for pre, rgb in costume.items():
                if m_.name.startswith(pre):
                    nm = bpy.data.materials.get(f'cp035_{name}_{pre}')
                    if nm is None:
                        nm = m_.copy(); nm.name = f'cp035_{name}_{pre}'
                        b_ = nm.node_tree.nodes.get('Principled BSDF') if nm.use_nodes else None
                        if b_: b_.inputs['Base Color'].default_value = (*rgb, 1)
                        nm.diffuse_color = (*rgb, 1)
                    o.data.materials[i_] = nm; break
    people.append(o); return o
SCARLET = (0.42, 0.035, 0.03); GOLD = (0.55, 0.40, 0.12); NAVYU = (0.04, 0.06, 0.16); BLACK = (0.03, 0.03, 0.035)
QUEEN = {'CPL3_skirt_': (0.40, 0.32, 0.45), 'CPL3_bodice_': (0.36, 0.29, 0.41), 'CPL3_bonnet_': (0.50, 0.48, 0.45), 'CPL3_waist_': (0.52, 0.50, 0.46)}
ALBERT = {'CPL3_coat_': SCARLET, 'CPL3_trou_': NAVYU, 'CPL3_waist_': GOLD, 'CPL3_hat_': BLACK}
KING = {'CPL3_coat_': NAVYU, 'CPL3_trou_': (0.55, 0.53, 0.50), 'CPL3_waist_': GOLD, 'CPL3_hat_': BLACK}
COURT = {'CPL3_coat_': (0.035, 0.03, 0.04), 'CPL3_trou_': (0.035, 0.03, 0.04), 'CPL3_waist_': (0.50, 0.48, 0.44), 'CPL3_hat_': BLACK}
AMB = [{'CPL3_coat_': (0.05, 0.14, 0.07), 'CPL3_waist_': GOLD, 'CPL3_trou_': (0.55, 0.53, 0.50)},
       {'CPL3_coat_': (0.55, 0.53, 0.49), 'CPL3_waist_': GOLD, 'CPL3_trou_': (0.30, 0.04, 0.04)},
       {'CPL3_coat_': (0.05, 0.07, 0.22), 'CPL3_waist_': GOLD, 'CPL3_trou_': (0.05, 0.05, 0.06)},
       {'CPL3_coat_': (0.30, 0.04, 0.10), 'CPL3_waist_': GOLD, 'CPL3_trou_': (0.55, 0.53, 0.49)},
       {'CPL3_coat_': (0.08, 0.05, 0.03), 'CPL3_waist_': GOLD, 'CPL3_trou_': (0.55, 0.53, 0.50)}]
YEOMAN = {'CPL3_coat_': SCARLET, 'CPL3_trou_': SCARLET, 'CPL3_waist_': GOLD, 'CPL3_hat_': BLACK}
LADIES = [{'CPL3_skirt_': c, 'CPL3_bonnet_': (0.55, 0.52, 0.48)} for c in ((0.45, 0.48, 0.55), (0.55, 0.50, 0.40), (0.50, 0.42, 0.46), (0.42, 0.47, 0.44))]
GIRL = {'CPL3_skirt_': (0.46, 0.36, 0.40), 'CPL3_bodice_': (0.40, 0.33, 0.36), 'CPL3_bonnet_': (0.42, 0.38, 0.34)}
BOY = {'CPL3_coat_': (0.05, 0.06, 0.12), 'CPL3_trou_': (0.55, 0.53, 0.50), 'CPL3_hat_': BLACK}
W = -1.0e3   # face west: toward (W, y)
qx = TX - 0.75
fig = [  # name, role, pose, x, y, z, costume
    ('cp035_queen_victoria', '1850s_lady', 'standing', qx - 0.05, 0.0, ZH, QUEEN),
    ('cp035_prince_albert', '1850s_gentleman', 'standing', qx + 0.05, -0.85, ZH, ALBERT),
    ('cp035_king_of_portugal', '1850s_gentleman', 'standing', qx + 0.10, 0.95, ZH, KING),
    ('cp035_duke_of_oporto', '1850s_gentleman', 'standing', HX0 - 0.55, 1.55, ZD, KING),
    ('cp035_prince_of_wales', '1850s_boy', 'standing', HX0 - 0.55, -1.25, ZD, BOY),
    ('cp035_prince_alfred', '1850s_boy', 'standing', HX0 - 0.45, -1.85, ZD, BOY),
    ('cp035_princess_royal', '1850s_girl', 'standing', HX0 - 0.50, 2.35, ZD, GIRL),
    ('cp035_princess_alice', '1850s_girl', 'standing', HX0 - 0.40, 2.95, ZD, GIRL),
]
for i, (nm, role, pose, x, y, z, cos) in enumerate(fig):
    put_person(nm, role, pose, x, y, z, face(x, y, W, y), 1854100 + i * 11, 'hero', cos)
for i, (x, y) in enumerate(((X1 - 0.55, -2.0), (X1 - 0.55, 2.1), (X1 - 0.6, -2.8), (X1 - 0.6, 2.9))):
    put_person(f'cp035_household_lady_{i}', '1850s_lady', 'standing', x, y, ZH if abs(y) < HY else ZD, face(x, y, W, y), 1854200 + i * 7, 'mid', LADIES[i % 4])
# government (north side, +y) and foreign ambassadors (south side, -y), two ranks each, facing the centre line
n = 0
for side, cos_fn in ((1, lambda j: COURT), (-1, lambda j: AMB[j % len(AMB)])):
    for rank in range(2):
        for j in range(6):
            x = X0 + 1.6 + j * 1.25 + rank * 0.55; y = side * (YH - 0.65 - rank * 0.8)
            put_person(f'cp035_{"minister" if side > 0 else "ambassador"}_{rank}{j}', '1850s_gentleman', RNG.choice(('standing', 'standing', 'pointing')),
                       x, y, ZD, face(x, y, x + 0.6, 0.0) + RNG.uniform(-0.25, 0.25), 1854300 + n * 5, 'mid', cos_fn(j)); n += 1
# directors in court dress at the west front of the dais; Laing on the flight with the address
for j in range(4):
    x = X0 + 0.7 + (j % 2) * 0.6; y = (-1) ** j * (SW * 0.55 + 0.4 * (j // 2))
    put_person(f'cp035_director_{j}', '1850s_gentleman', 'standing', x, y, ZD, face(x, y, qx, 0.0), 1854400 + j * 9, 'mid', COURT)
lx = X0 - 0.45
put_person('cp035_samuel_laing', '1850s_gentleman', 'standing', lx, 0.35, ZD * 2 / 3, face(lx, 0.35, qx, 0.0), 1854450, 'hero', COURT)
ka = Kit(); ka.cyl('paper', (lx + 0.30, 0.20, ZD * 2 / 3 + 1.05), (lx + 0.30, 0.52, ZD * 2 / 3 + 1.05), 0.03, 8); ka.done('cp035_laing_address')
# yeomen of the guard: either side of the flight and along the dais sides on the floor, facing outward
yeo = [(X0 - 1.25, -SW - 1.25), (X0 - 1.25, SW + 1.25), (X0 - 2.35, -SW - 1.0), (X0 - 2.35, SW + 1.0)]
for j in range(5):
    x = X0 + 1.2 + j * 2.1; yeo += [(x, -YH - 0.75), (x, YH + 0.75)]
for j, (x, y) in enumerate(yeo):
    tx, ty = (x - 5.0, y) if x < X0 else (x, y + (1 if y > 0 else -1) * 5.0)
    put_person(f'cp035_yeoman_{j:02d}', '1850s_soldier', 'standing', x, y, 0.0, face(x, y, tx, ty), 1854500 + j * 3, 'mid', YEOMAN)
# gallery spectators at the new rail, 8-11 m from the hero lens, looking down into the transept
for j, (x, y) in enumerate(((-22.0, 11.5), (-20.5, 11.55), (-19.0, 12.5))):
    role = '1850s_lady' if j != 1 else '1850s_gentleman'
    put_person(f'cp035_gallery_spectator_{j}', role, 'standing', x, y, 6.99, face(x, y, -12.0, 0.0) + RNG.uniform(-0.3, 0.3), 1854600 + j * 13, 'mid')
INFO['people_lib_figures'] = len(people)

for o in col.objects: o['cp_state'] = STATE
print('CP035 BUILT', INFO, 'hidden', HIDDEN)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP035 SAVED', OUT)
