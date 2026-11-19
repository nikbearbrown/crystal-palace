"""CP059 CANDIDATE (2026-11-18, no verdict): 'Why the image of fireproofness failed' - the night of 30 November 1936 inside
the south nave: the nave planting (the iron-and-glass palace's living, combustible contents) burning.

usage: blender -b rounds/sydenham-1936fire-r11b.blend -P scripts/candidate_cp059_burning_planting.py [-- out.blend]
       (env CP059_NOSAVE=1: build in memory only)
Base = rounds/sydenham-1936fire-r11b.blend (md5 62396fca, unchanged since 9aff52a, 2026-10-27) - the blend the live hero
  renders/r11b_1936fire_CAM_CP059_nave_fire_28mm.png (md5 77640c3a; COVERAGE.md CP059 hero) was rendered from:
  RES=960x540 scripts/render.py -- <dir> <tag> 100 32 CAM_CP059_nave_fire_28mm (blend's own Filmic -0.5 EV, no people,
  no look pass); re-rendered 2026-11-18 max diff 0.
  -> rounds/candidates/sydenham-1936fire-r11b_cp059planting.blend
Live hero shows: a corridor of flame at the far end and down both aisles, but the two biggest things mid-frame are the
  r03 broadleaf PLACEHOLDER crowns (nine smooth grey icospheres each) hanging in front of the flames like grey boulders on
  sticks; nothing in the frame is visibly the fuel the narration names ('fittings and accumulated displays could feed a
  fire'), and the trees, the most obviously combustible contents of the nave, do not burn.
Adds ONE dated collection SY36_nave_planting_burning__30Nov1936 (cp_state SY36-FIRE_30Nov1936_night), for every
  PLACEHOLDER_nave_tree_*_crown in the round (12 crowns; the r03 placeholders are kept, untouched, underneath):
  * cp059_leaf_canopy: broadleaf foliage - leaf blades (pointed-ellipse 6-gons, 0.14-0.30 m long) in twig clusters on and
    up to 0.75 m outside the visible surface of each placeholder crown (points inside a neighbouring sphere of the same
    crown are skipped; nothing beyond y = +-35 ft, inside the nave column lines, so no leaf passes through a gallery), so each crown gets a ragged, open leaf silhouette instead of a smooth sphere; material
    cp059_scorched_foliage: dark green -> scorched brown per leaf (attribute 'leafvar'), thin-leaf translucency so the
    blades glow amber where the fire is behind them;
  * cp059_smouldering_leaves: blades within 1.3 m of a crown flame tongue's base smoulder with probability 0.3
    (cp059_leaf_ember: blackbody 1000-1250 K, low emission);
  * cp059_charred_limbs: 7 primary limbs + forks per tree from the r03 trunk top out through the crown (charred bark);
  * cp059_crown_flames: flame tongues licking up out of the crowns, built exactly like the r11b nave tongues (cone +
    per-vertex 'hfac' 0 base -> 1 tip) and using the round's own fire_flames_surface material, so they match the
    existing flames; tongue count per crown follows the r11b nave flame density (states.py: w = exp(-((x_ft+120)/520)^2)).
Sources: storyboard CP059 (30 Nov 1936 SY36; 'Timber floors, glazing members, fittings and accumulated displays could
  feed a fire'; no forensic fire simulation); 1856 guide (OCR 0198/0200/0208: 'a magnificent collection of plants of
  every land', the Loddiges palms, 'an avenue of choice exotics') - R that the nave was planted, I that trees stood in
  these tubs in 1936; r03 placeholder positions from plan 0205 beds (R position, I form); LFB / Wikipedia (fire spread by
  wind through the building's timber and contents, R in general). Species, leaf size, scorch and which crowns burn: I.
Cameras NOT moved, world/sun/exposure/look NOT changed. Nothing deleted or hidden; every existing object/material untouched
(fire_flames_surface is reused, not edited).
"""
import bpy, bmesh, math, os, sys, random
import numpy as np
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP059_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-1936fire-r11b_cp059planting.blend')
STATE = 'SY36-FIRE_30Nov1936_night'
CNAME = 'SY36_nave_planting_burning__30Nov1936'
assert bpy.data.collections.get(CNAME) is None, 'base already dressed'
FT = 0.3048
RNG = random.Random(301136)
NPR = np.random.default_rng(301136)
sc = bpy.context.scene
n_before = len(bpy.data.objects); nmat_before = len(bpy.data.materials)
hidden_before = sorted(o.name for o in bpy.data.objects if o.hide_render)
col = bpy.data.collections.new(CNAME); sc.collection.children.link(col); col['cp_state'] = STATE
INFO = {}

# ------------------------------------------------------------------ parameters (m unless stated)
LEAF_L = (0.14, 0.30)        # leaf blade length (broadleaf ornamental tree, I)
LEAF_W = 0.42                # width / length
CLUSTER_PER_M2 = 15.0        # twig clusters per m2 of exposed crown surface
LEAVES_PER_CLUSTER = (5, 9)
CLUSTER_R = 0.32             # leaves within this radius of the twig cluster centre
OUT_OFF = (0.02, 0.75)       # cluster centre offset outside the placeholder sphere surface
EMBER_R = 1.3                # blades within this distance of a crown flame tongue's base may smoulder
EMBER_P = 0.30               # ... with this probability
TONGUES_MAX = 11             # flame tongues per crown at full burn weight
Y_CLEAR = 35.0 * FT          # foliage/limbs kept inside the nave column lines (y = +-36 ft, params.py) - no leaves through the galleries
def burn_w(x_m): return math.exp(-(((x_m / FT) + 120) / 520) ** 2)   # r11b nave flame density (states.py)

# ------------------------------------------------------------------ materials (new, tagged)
def tag(m): m['cp_state'] = STATE; return m
def foliage_mat():
    m = tag(bpy.data.materials.new('cp059_scorched_foliage')); nt = m.node_tree; n = nt.nodes; l = nt.links
    for x in list(n): n.remove(x)
    out = n.new('ShaderNodeOutputMaterial'); pb = n.new('ShaderNodeBsdfPrincipled'); tl = n.new('ShaderNodeBsdfTranslucent')
    mix = n.new('ShaderNodeMixShader'); at = n.new('ShaderNodeAttribute'); at.attribute_name = 'leafvar'; at.attribute_type = 'GEOMETRY'
    ramp = n.new('ShaderNodeValToRGB'); el = ramp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (0.030, 0.052, 0.018, 1)          # dark leaf green
    el[1].position = 0.62; el[1].color = (0.060, 0.062, 0.020, 1)         # olive, drying
    e2 = el.new(0.85); e2.color = (0.105, 0.055, 0.020, 1)                # scorched brown
    e3 = el.new(1.0); e3.color = (0.020, 0.016, 0.013, 1)                 # charred
    l.new(at.outputs['Fac'], ramp.inputs[0])
    l.new(ramp.outputs['Color'], pb.inputs['Base Color']); pb.inputs['Roughness'].default_value = 0.62
    hue = n.new('ShaderNodeMix'); hue.data_type = 'RGBA'; hue.inputs['Factor'].default_value = 0.0
    l.new(ramp.outputs['Color'], tl.inputs['Color'])
    mix.inputs[0].default_value = 0.38
    l.new(pb.outputs[0], mix.inputs[1]); l.new(tl.outputs[0], mix.inputs[2]); l.new(mix.outputs[0], out.inputs['Surface'])
    n.remove(hue)
    return m
def ember_mat():
    m = tag(bpy.data.materials.new('cp059_leaf_ember')); nt = m.node_tree; n = nt.nodes; l = nt.links
    for x in list(n): n.remove(x)
    out = n.new('ShaderNodeOutputMaterial'); em = n.new('ShaderNodeEmission'); df = n.new('ShaderNodeBsdfDiffuse'); add = n.new('ShaderNodeAddShader')
    at = n.new('ShaderNodeAttribute'); at.attribute_name = 'leafvar'; at.attribute_type = 'GEOMETRY'
    mr = n.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 1000; mr.inputs['To Max'].default_value = 1250
    l.new(at.outputs['Fac'], mr.inputs['Value']); bb = n.new('ShaderNodeBlackbody'); l.new(mr.outputs['Result'], bb.inputs['Temperature'])
    l.new(bb.outputs['Color'], em.inputs['Color']); em.inputs['Strength'].default_value = 1.6
    df.inputs['Color'].default_value = (0.03, 0.02, 0.015, 1)
    l.new(em.outputs[0], add.inputs[0]); l.new(df.outputs[0], add.inputs[1]); l.new(add.outputs[0], out.inputs['Surface'])
    return m
def limb_mat():
    m = tag(bpy.data.materials.new('cp059_charred_limb')); nt = m.node_tree; n = nt.nodes
    pb = n.get('Principled BSDF'); pb.inputs['Base Color'].default_value = (0.028, 0.022, 0.018, 1); pb.inputs['Roughness'].default_value = 0.92
    return m
M_LEAF, M_EMBER, M_LIMB = foliage_mat(), ember_mat(), limb_mat()
M_FLAME = bpy.data.materials['fire_flames_surface']       # the round's own r11b flame material, reused unedited

# ------------------------------------------------------------------ crown analysis: the r03 crowns are 9 icospheres x 80 faces (build.py tree_broadleaf)
crowns = sorted((o for o in bpy.data.objects if o.name.startswith('PLACEHOLDER_nave_tree_') and o.name.endswith('_crown')), key=lambda o: o.name)
def spheres_of(o):
    me = o.data; mw = o.matrix_world
    V = np.array([tuple(mw @ v.co) for v in me.vertices])
    polys = list(me.polygons); assert len(polys) % 80 == 0, (o.name, len(polys))
    out = []
    for k in range(len(polys) // 80):
        fs = polys[k*80:(k+1)*80]; vi = sorted({i for p in fs for i in p.vertices}); P = V[vi]
        c = P.mean(0); r = float(np.linalg.norm(P - c, axis=1).mean())
        out.append((c, r, fs))
    return V, out

leafV, leafF, leafVar = [], [], []      # canopy blades
embV, embF, embVar = [], [], []         # smouldering blades
limbBM = bmesh.new(); flameBM = bmesh.new(); HL = flameBM.verts.layers.float.new('hfac')
def blade(VL, FL, VarL, c, nrm, L, var):
    # pointed-ellipse leaf: 6 verts in a random plane roughly facing nrm
    a = Vector(NPR.normal(size=3)).normalized()
    d = (a - a.dot(nrm) * nrm * 0.6).normalized()            # leaf axis, mostly tangent-ish
    s = d.cross(nrm).normalized(); w = L * LEAF_W * 0.5
    tw = Vector(NPR.normal(size=3)) * 0.25; s = (s + tw).normalized()
    base = c - d * (L * 0.5)
    pts = [base, base + d * (L*0.3) + s * w, base + d * (L*0.7) + s * (w*0.8), base + d * L, base + d * (L*0.7) - s * (w*0.8), base + d * (L*0.3) - s * w]
    pts[3] = pts[3] + nrm * (L * NPR.uniform(-0.15, 0.25))   # slight curl
    i0 = len(VL); VL.extend(tuple(p) for p in pts); FL.append(tuple(range(i0, i0 + 6))); VarL.append(var)
def limb(p0, p1, r0, r1, seg=6):
    d = Vector(p1) - Vector(p0); Ln = d.length
    if Ln < 1e-4: return
    q = d.normalized().to_track_quat('Z', 'Y').to_matrix().to_4x4()
    res = bmesh.ops.create_cone(limbBM, cap_ends=False, segments=seg, radius1=r0, radius2=r1, depth=Ln)
    from mathutils import Matrix
    M = Matrix.Translation((Vector(p0) + Vector(p1)) / 2) @ q
    bmesh.ops.transform(limbBM, matrix=M, verts=res['verts'])
def tongue(x, y, z, r, h):
    from mathutils import Matrix
    n0 = len(flameBM.verts)
    res = bmesh.ops.create_cone(flameBM, cap_ends=True, segments=10, radius1=r, radius2=r * 0.12, depth=h)
    bmesh.ops.transform(flameBM, matrix=Matrix.Translation((x, y, z + h / 2)), verts=res['verts'])
    flameBM.verts.ensure_lookup_table()
    for v in flameBM.verts[n0:]: v[HL] = min(1.0, max(0.0, (v.co.z - z) / h))

per_crown = []
for o in crowns:
    V, sph = spheres_of(o)
    trunk = bpy.data.objects[o.name.replace('_crown', '_trunk')]
    tb = [trunk.matrix_world @ Vector(c) for c in trunk.bound_box]
    tx, ty = sum(v.x for v in tb) / 8, sum(v.y for v in tb) / 8; ttop = max(v.z for v in tb)
    cz = float(np.mean([s[0][2] for s in sph])); ctop = max(float(s[0][2]) + s[1] for s in sph)
    bw = burn_w(tx); nl = ne = 0
    # flame tongues out of the upper crown (positions first: smouldering blades gather round their bases)
    nt = int(round(TONGUES_MAX * bw))
    ups = [s for s in sph if s[0][2] >= cz - 0.2] or sph
    TB = []
    for j in range(nt):
        c, r, _ = ups[j % len(ups)]
        th = RNG.uniform(0, 2 * math.pi); el = RNG.uniform(0.25, 1.1)
        p = Vector(c) + Vector((math.cos(th) * math.cos(el), math.sin(th) * math.cos(el), math.sin(el))) * (r * 0.85)
        p.y = max(-Y_CLEAR + 1.0, min(Y_CLEAR - 1.0, p.y))
        h = RNG.uniform(1.8, 4.2) * (0.6 + 0.6 * bw); rr = RNG.uniform(0.45, 0.95)
        tongue(p.x, p.y, p.z - 0.3, rr, h); TB.append(np.array(tuple(p)))
    for k, (c, r, fs) in enumerate(sph):
        for p in fs:
            a = p.area
            if a <= 0: continue
            ncl = NPR.poisson(a * CLUSTER_PER_M2)
            vv = [V[i] for i in p.vertices]
            for _ in range(ncl):
                u, v_ = NPR.random(2)
                if u + v_ > 1: u, v_ = 1 - u, 1 - v_
                pt = vv[0] + u * (vv[1] - vv[0]) + v_ * (vv[2] - vv[0])
                nrm = pt - c; nrm = nrm / np.linalg.norm(nrm)
                off = NPR.uniform(*OUT_OFF) ** 1.0
                q = pt + nrm * off
                if abs(q[1]) > Y_CLEAR - CLUSTER_R: continue
                if any(j != k and np.linalg.norm(q - s2[0]) < s2[1] * 0.97 for j, s2 in enumerate(sph)): continue
                qn = Vector(nrm)
                upper = (q[2] - cz) > 0
                for _ in range(NPR.integers(*LEAVES_PER_CLUSTER, endpoint=True)):
                    lc = Vector(q) + Vector(NPR.normal(size=3)) * (CLUSTER_R * 0.5)
                    if abs(lc.y) > Y_CLEAR - 0.2: continue
                    L = NPR.uniform(*LEAF_L)
                    var = float(np.clip(NPR.beta(2.2, 2.0) * (0.75 + 0.35 * bw) + (0.12 if upper else 0.0) * bw, 0, 1))
                    near = TB and min(np.linalg.norm(np.array(tuple(lc)) - t) for t in TB) < EMBER_R
                    if near and NPR.random() < EMBER_P:
                        blade(embV, embF, embVar, lc, qn, L * 0.85, float(NPR.random())); ne += 1
                    else:
                        blade(leafV, leafF, leafVar, lc, qn, L, var); nl += 1
    # limbs: trunk top -> crown surface, with one fork each
    base = Vector((tx, ty, ttop - 0.4))
    for j in range(7):
        c, r, _ = sph[(j * 4 + RNG.randrange(9)) % len(sph)]
        dirn = (Vector(c) - base); dirn.z = abs(dirn.z) + 0.6; dirn.normalize()
        tip = Vector(c) + dirn * (r * RNG.uniform(0.85, 1.12)); tip.y = max(-Y_CLEAR, min(Y_CLEAR, tip.y))
        mid = base + (tip - base) * 0.5 + Vector((RNG.uniform(-.4, .4), RNG.uniform(-.4, .4), RNG.uniform(0, .5)))
        limb(base, mid, 0.13, 0.085); limb(mid, tip, 0.085, 0.03)
        fd = Vector((RNG.uniform(-1, 1), RNG.uniform(-1, 1), RNG.uniform(0.2, 1))).normalized()
        ft_ = mid + fd * RNG.uniform(1.4, 2.6); ft_.y = max(-Y_CLEAR, min(Y_CLEAR, ft_.y)); limb(mid, ft_, 0.06, 0.02, seg=5)
    per_crown.append((o.name, round(tx / FT), round(bw, 3), nl, ne, nt, round(ctop, 2)))

def mesh_obj(name, Vs, Fs, mat, var=None):
    me = bpy.data.meshes.new(name); me.from_pydata(Vs, [], Fs); me.materials.append(mat)
    if var is not None:
        at = me.attributes.new('leafvar', 'FLOAT', 'FACE'); at.data.foreach_set('value', np.array(var, dtype=np.float32))
    me.update(); o = bpy.data.objects.new(name, me); col.objects.link(o); o['cp_state'] = STATE; return o
canopy = mesh_obj('cp059_leaf_canopy', leafV, leafF, M_LEAF, leafVar)
ember = mesh_obj('cp059_smouldering_leaves', embV, embF, M_EMBER, embVar)
me = bpy.data.meshes.new('cp059_charred_limbs'); limbBM.to_mesh(me); limbBM.free(); me.materials.append(M_LIMB)
limbs = bpy.data.objects.new('cp059_charred_limbs', me); col.objects.link(limbs); limbs['cp_state'] = STATE
me = bpy.data.meshes.new('cp059_crown_flames'); flameBM.to_mesh(me); flameBM.free(); me.materials.append(M_FLAME)
fl = bpy.data.objects.new('cp059_crown_flames', me); col.objects.link(fl); fl['cp_state'] = STATE
fl.visible_shadow = False                                   # as the r11b fire_flames object
for o in (canopy, ember): pass
INFO['crowns'] = len(crowns); INFO['blades'] = len(leafF); INFO['ember_blades'] = len(embF); INFO['tongues'] = sum(p[5] for p in per_crown)
col['evidence'] = ('storyboard CP059 30 Nov 1936 SY36 fittings/displays feed the fire (R as brief); 1856 guide OCR 0198/0200/0208 nave planted '
                   '(plants of every land, Loddiges palms, avenue of choice exotics) R; trees in these tubs in 1936 I; r03 placeholder positions from '
                   'plan 0205 beds R/I; species, leaf size, scorch, burning crowns I; flame tongues = r11b recipe and material')
col['per_crown'] = str(per_crown)
bpy.context.view_layer.update()
INFO['objects'] = len(col.objects); INFO['new_objects_total'] = len(bpy.data.objects) - n_before
INFO['new_materials'] = len(bpy.data.materials) - nmat_before
assert sorted(o.name for o in bpy.data.objects if o.hide_render) == hidden_before
assert len(bpy.data.objects) - n_before == len(col.objects), 'every new object must be in the one dated collection'
print('CP059 BUILT', INFO)
for p in per_crown: print('CP059 CROWN', p)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP059 SAVED', OUT)
