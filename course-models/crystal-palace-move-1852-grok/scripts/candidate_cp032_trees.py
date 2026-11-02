"""CP032 arrival parkland trees + meadow (+ timber tone, workmen's hats) (2026-11-02, Grok; CANDIDATE, no verdict;
DEPARTURES MV19).

blender -b rounds/m02.blend -P scripts/candidate_cp032_trees.py -- [--out rounds/candidates/m02_cp032trees.blend]
blender -b ROUND.blend -P scripts/candidate_cp032_trees.py -- --live     # apply in place (only after a KEEP call)
Idempotent; always prints `CP032_TREES_IN_PLACE True|False`. Needs MV17 + MV18 in place.

Sydenham (Penge Place) 1852 only; nothing of Hyde Park 1851 and nothing of the Sydenham building.
 1. Trees: the 86 ARR_OAK_* / ARR_OAK_EDGE_* objects keep their transforms; their shared low-poly 'round_tree'
    meshes (a cone trunk under nine icospheres) are swapped for parametric open-grown parkland oaks (ARR_TR_oak_*,
    8 variants, same four heights 48/55/62/70 ft as before): tapered trunk with root flare, 5-7 spreading limbs and
    two orders of branches, foliage as clumped leaf-card clusters (irregular silhouette, sky gaps, sun-tipped outer
    clumps, darker interior) in GT_OakLeaf1852 and GT_OakBark1852. Per-card / per-clump / per-tree colour variation.
 2. Field: ARR_GRASS only -> GT_SydenhamMeadow1852 (rough pasture / mown meadow: muted summer greens, large drier
    and lusher patches, tussock-scale value variation, straw flecks, bump). DEP_GRASS keeps GT_Grass1852.
 3. Timber (ARR only): ARR_BEARERS_COL / ARR_BEARERS_GIR and ARR_BARS_GUTTERS slot 3 -> GT_OakBearerWeathered1852
    (grey-brown weathered oak, grain); ARR_CRATE_0/1 instance a copy of the Muse crate collection
    (ARR_CrateSY1852_from_Muse, Muse meshes shared read-only) with GT_PackingCaseWeathered1852 / GT_CrateDealWeathered1852.
    DEP keeps GT_OakBearer / GT_PackingCase / Timber.
 4. Workmen/navvy (ARR_HAND_00..03): an ARR_HD_HAT_NN soft felt 'wideawake' hat (round crown + brim) and an
    ARR_HD_HAIR_NN short-hair band under the brim, fitted to each head from its skin vertices (the people_lib cap
    is a small flat disc on a bald-looking skull). Figure meshes untouched; clerk keeps his silk hat.
All colours by eye (grade D). Existing cameras, exposure, figures and yard dressing unchanged.
"""
import os, sys, json, math, random, argparse
import bpy, bmesh
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser(); ap.add_argument("--out", default="rounds/candidates/m02_cp032trees.blend")
ap.add_argument("--live", action="store_true")
a = ap.parse_args(argv)
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if a.live:
    out = os.path.abspath(bpy.data.filepath)
else:
    out = os.path.join(here, a.out) if not os.path.isabs(a.out) else a.out
    assert os.path.abspath(out) != os.path.abspath(bpy.data.filepath), "refusing to overwrite the opened blend without --live"

VERSION = 2
FT = 0.3048
COLL = "ARR_SYDENHAM_1852"
P = dict(seed=18520605, variants_per_height=2, crown_w_over_h=0.85)   # old trees: height taken from each old mesh


# ---------------------------------------------------------------- node helpers
def _p(m): return next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
def _ramp(n, els):
    r = n.new("ShaderNodeValToRGB"); e = r.color_ramp.elements
    while len(e) < len(els): e.new(0.5)
    for el, (pos, c) in zip(e, els): el.position = pos; el.color = (*c, 1)
    return r
def _noise(n, l, vec, scale, detail=4.0, rough=0.5):
    t = n.new("ShaderNodeTexNoise"); t.inputs["Scale"].default_value = scale; t.inputs["Detail"].default_value = detail
    t.inputs["Roughness"].default_value = rough
    if vec is not None: l.new(vec, t.inputs["Vector"])
    return t
def _math(n, l, op, a_, b_=None, clamp=False):
    m = n.new("ShaderNodeMath"); m.operation = op; m.use_clamp = clamp
    for i, s in enumerate((a_, b_)):
        if s is None: continue
        if isinstance(s, (int, float)): m.inputs[i].default_value = s
        else: l.new(s, m.inputs[i])
    return m
def _mixc(n, l, fac, ca, cb, blend="MIX"):
    m = n.new("ShaderNodeMix"); m.data_type = "RGBA"; m.blend_type = blend
    for s, i in ((fac, 0), (ca, 6), (cb, 7)):
        if isinstance(s, (int, float)): m.inputs[i].default_value = s
        elif isinstance(s, tuple): m.inputs[i].default_value = (*s, 1)
        else: l.new(s, m.inputs[i])
    return m.outputs[2]
def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; return m, m.node_tree.nodes, m.node_tree.links


# ---------------------------------------------------------------- materials
def leaf_mat():
    """Oak leaf cards: colour from per-card attribute 'lv' (x: card random, y: clump random, z: outerness/sun)."""
    m = bpy.data.materials.get("GT_OakLeaf1852")
    if m: return m
    m, n, l = new_mat("GT_OakLeaf1852"); b = _p(m)
    at = n.new("ShaderNodeAttribute"); at.attribute_name = "lv"; at.attribute_type = "GEOMETRY"
    sep = n.new("ShaderNodeSeparateXYZ"); l.new(at.outputs["Vector"], sep.inputs[0])
    oi = n.new("ShaderNodeObjectInfo")
    # value driver: outerness (sun-tipped outside of the clumps) + clump + card + per-tree
    v = _math(n, l, "MULTIPLY", sep.outputs["Z"], 0.55)
    v = _math(n, l, "ADD", v.outputs[0], _math(n, l, "MULTIPLY", sep.outputs["Y"], 0.25).outputs[0])
    v = _math(n, l, "ADD", v.outputs[0], _math(n, l, "MULTIPLY", sep.outputs["X"], 0.20).outputs[0], clamp=True)
    r = _ramp(n, [(0.0, (0.032, 0.046, 0.018)), (0.45, (0.070, 0.092, 0.034)), (0.80, (0.120, 0.140, 0.055)), (1.0, (0.165, 0.175, 0.075))])
    l.new(v.outputs[0], r.inputs[0])
    # per-tree hue drift: some trees yellower/olive, some bluer-green
    tint = _ramp(n, [(0.0, (0.92, 1.0, 0.86)), (0.5, (1.0, 1.0, 1.0)), (1.0, (1.12, 1.04, 0.80))])
    l.new(oi.outputs["Random"], tint.inputs[0])
    c = _mixc(n, l, 1.0, r.outputs["Color"], tint.outputs["Color"], "MULTIPLY")
    l.new(c, b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.62
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.35
    # a little translucency so backlit clumps are not dead
    tr = n.new("ShaderNodeBsdfTranslucent"); l.new(c, tr.inputs["Color"])
    mx = n.new("ShaderNodeMixShader"); mx.inputs[0].default_value = 0.25
    out = next(x for x in n if x.type == "OUTPUT_MATERIAL")
    l.new(b.outputs[0], mx.inputs[1]); l.new(tr.outputs[0], mx.inputs[2]); l.new(mx.outputs[0], out.inputs[0])
    m.diffuse_color = (0.055, 0.07, 0.027, 1); m["cp032_trees_v"] = VERSION
    return m


def bark_mat():
    m = bpy.data.materials.get("GT_OakBark1852")
    if m: return m
    m, n, l = new_mat("GT_OakBark1852"); b = _p(m)
    tc = n.new("ShaderNodeTexCoord"); mp = n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (6.0, 6.0, 0.8)
    l.new(tc.outputs["Object"], mp.inputs["Vector"])
    nz = _noise(n, l, mp.outputs["Vector"], 3.0, 6.0, 0.65)
    r = _ramp(n, [(0.3, (0.060, 0.050, 0.040)), (0.7, (0.135, 0.118, 0.098))]); l.new(nz.outputs["Fac"], r.inputs[0])
    l.new(r.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.95
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.4
    l.new(nz.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (0.075, 0.07, 0.062, 1); return m


def meadow_mat():
    """Penge Place rough pasture / mown meadow, early June 1852 (ILN 5 Jun 1852: wooded, deer). By eye (D)."""
    m = bpy.data.materials.get("GT_SydenhamMeadow1852")
    if m: return m
    m, n, l = new_mat("GT_SydenhamMeadow1852"); b = _p(m)
    tc = n.new("ShaderNodeTexCoord"); v = tc.outputs["Object"]             # ARR_GRASS sits at the origin: metres
    macro = _noise(n, l, v, 0.012, 3.0, 0.55)                             # ~80 m pasture patches
    meso = _noise(n, l, v, 0.09, 4.0, 0.6)                                # ~10 m swathes
    tus = _noise(n, l, v, 1.1, 5.0, 0.7)                                  # tussocks
    fine = _noise(n, l, v, 9.0, 3.0, 0.6)                                 # blades / grain
    lush = (0.026, 0.044, 0.014); mid = (0.052, 0.070, 0.024); dry = (0.118, 0.110, 0.050); straw = (0.150, 0.135, 0.075)
    base = _ramp(n, [(0.40, lush), (0.50, mid), (0.60, dry)]); l.new(macro.outputs["Fac"], base.inputs[0])
    swath = _ramp(n, [(0.40, (0.62, 0.66, 0.60)), (0.60, (1.25, 1.20, 1.10))]); l.new(meso.outputs["Fac"], swath.inputs[0])
    c = _mixc(n, l, 1.0, base.outputs["Color"], swath.outputs["Color"], "MULTIPLY")
    tsr = _ramp(n, [(0.32, (0.72, 0.76, 0.72)), (0.68, (1.15, 1.12, 1.05))]); l.new(tus.outputs["Fac"], tsr.inputs[0])
    c = _mixc(n, l, 1.0, c, tsr.outputs["Color"], "MULTIPLY")
    fl = _math(n, l, "GREATER_THAN", fine.outputs["Fac"], 0.66)            # straw / seed-head flecks
    fl = _math(n, l, "MULTIPLY", fl.outputs[0], 0.45)
    c = _mixc(n, l, fl.outputs[0], c, straw)
    l.new(c, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.92
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.25
    h = _math(n, l, "ADD", tus.outputs["Fac"], _math(n, l, "MULTIPLY", fine.outputs["Fac"], 0.6).outputs[0])
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.35; bp.inputs["Distance"].default_value = 0.05
    l.new(h.outputs[0], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (*mid, 1); m["cp032_trees_v"] = VERSION
    return m


def wood_mat(name, c0, c1, scale, nscale=5.0, grain=True):
    m = bpy.data.materials.get(name)
    if m: return m
    m, n, l = new_mat(name); b = _p(m)
    tc = n.new("ShaderNodeTexCoord"); mp = n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = scale
    l.new(tc.outputs["Object"], mp.inputs["Vector"])
    g = _noise(n, l, mp.outputs["Vector"], nscale, 6.0, 0.6)               # stretched grain / weathering streaks
    bl = _noise(n, l, tc.outputs["Object"], 1.3, 3.0, 0.5)                 # blotches (damp, dirt)
    r = _ramp(n, [(0.3, c0), (0.7, c1)]); l.new(g.outputs["Fac"], r.inputs[0])
    br = _ramp(n, [(0.35, (0.78, 0.78, 0.80)), (0.7, (1.05, 1.03, 1.0))]); l.new(bl.outputs["Fac"], br.inputs[0])
    c = _mixc(n, l, 1.0, r.outputs["Color"], br.outputs["Color"], "MULTIPLY")
    l.new(c, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.88
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.3
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.25
    l.new(g.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (*[(x + y) / 2 for x, y in zip(c0, c1)], 1); m["cp032_trees_v"] = VERSION
    return m


def plain_mat(name, c, rough=0.9):
    m = bpy.data.materials.get(name)
    if m: return m
    m, n, l = new_mat(name); b = _p(m); b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.3
    m.diffuse_color = (*c, 1); return m


# ---------------------------------------------------------------- oak generator (metres, origin at trunk foot)
def _tube(bm, a, b, ra, rb, seg):
    d = b - a
    if d.length < 1e-6: return
    d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0))
    s = d.cross(up).normalized(); u = s.cross(d).normalized()
    A = [bm.verts.new(a + (s * math.cos(2 * math.pi * k / seg) + u * math.sin(2 * math.pi * k / seg)) * ra) for k in range(seg)]
    B = [bm.verts.new(b + (s * math.cos(2 * math.pi * k / seg) + u * math.sin(2 * math.pi * k / seg)) * rb) for k in range(seg)]
    for k in range(seg): bm.faces.new([A[k], A[(k + 1) % seg], B[(k + 1) % seg], B[k]])


def build_oak(name, H, seed):
    """Open-grown English oak (Quercus robur), parkland form: short stout bole, broad domed crown about as wide as
    0.7-0.8 x the height, heavy near-horizontal lower limbs. H in metres. Proportions by eye (D)."""
    rnd = random.Random(seed); bm = bmesh.new(); tips = []
    trunk_h = H * rnd.uniform(0.20, 0.25); D = H * 0.055                   # bole diameter ~0.8-1.15 m
    CR = H * rnd.uniform(0.36, 0.42); zc = trunk_h + (H - trunk_h) * 0.45
    def branch(p, d, length, radius, depth):
        n = max(2, int(length / 1.2)); cur = Vector(p); dv = Vector(d).normalized(); pts = [cur.copy()]
        for i in range(n):
            dv = (dv + Vector((rnd.uniform(-.22, .22), rnd.uniform(-.22, .22), rnd.uniform(-.10, .14)))).normalized()
            cur = cur + dv * (length / n); cur.z = min(cur.z, H - 0.6); pts.append(cur.copy())
        for i, (q0, q1) in enumerate(zip(pts, pts[1:])):
            _tube(bm, q0, q1, radius * (1 - 0.55 * i / n), radius * (1 - 0.55 * (i + 1) / n), 7 if radius > 0.15 else 4)
        if depth == 0:
            tips.extend(pts[1:]); return
        for k in range(3 if depth == 2 else 3):
            t = rnd.uniform(0.35, 1.0); base = pts[max(1, min(n, int(round(t * n))))]
            ang = rnd.uniform(0, 2 * math.pi)
            nd = (dv * 0.8 + Vector((math.cos(ang), math.sin(ang), rnd.uniform(0.0, 0.7)))).normalized()
            branch(base, nd, length * rnd.uniform(0.45, 0.6), radius * 0.48, depth - 1)
    # bole with flare
    _tube(bm, Vector((0, 0, -0.6)), Vector((0, 0, 0.5)), D * 0.85, D * 0.55, 10)
    _tube(bm, Vector((0, 0, 0.5)), Vector((0, 0, trunk_h + 0.3)), D * 0.55, D * 0.42, 10)
    nl = rnd.randint(5, 7)
    for k in range(nl):
        ang = 2 * math.pi * k / nl + rnd.uniform(-.35, .35); low = k < 2
        elev = rnd.uniform(0.12, 0.35) if low else rnd.uniform(0.7, 1.7)
        zb = trunk_h * rnd.uniform(0.85, 1.05) + (0 if low else rnd.uniform(0, H * 0.08))
        d = Vector((math.cos(ang), math.sin(ang), elev)).normalized()
        branch(Vector((0, 0, zb)), d, CR * rnd.uniform(0.65, 0.85), D * rnd.uniform(0.20, 0.26), 2)
    branch(Vector((0, 0, trunk_h)), Vector((rnd.uniform(-.15, .15), rnd.uniform(-.15, .15), 1)), (H - trunk_h) * 0.75, D * 0.24, 2)
    wood_faces = len(bm.faces)
    # foliage clumps
    lv = bm.faces.layers.float_vector.new("lv") if hasattr(bm.faces.layers, "float_vector") else None
    hz = (H - trunk_h) * 0.55; cards = clumps = 0
    rnd.shuffle(tips)
    centres = []
    for tp in tips:
        c = Vector(tp) + Vector((rnd.uniform(-.8, .8), rnd.uniform(-.8, .8), rnd.uniform(0.0, 1.0)))
        rr = math.hypot(c.x, c.y) / CR; zz = (c.z - zc) / hz
        if c.z < trunk_h * 0.95 or rr * rr + max(zz, -0.6 * 1) ** 2 > 1.15 or c.z > H - 0.8: continue
        if any((c - q).length < 0.9 for q in centres): continue
        centres.append(c)
    ztop = H - 1.2; hz2 = ztop - zc
    for k in range(int(2.2 * CR * CR / 1.0) + 20):
        th = rnd.uniform(0, 2 * math.pi); ph = math.acos(rnd.uniform(-0.35, 1.0)); rs = rnd.uniform(0.72, 1.0)
        c = Vector((math.cos(th) * math.sin(ph) * CR * rs, math.sin(th) * math.sin(ph) * CR * rs, zc + math.cos(ph) * hz2 * rs))
        if rnd.random() < 0.18 or c.z < trunk_h + 1.0: continue                       # gaps / sky holes
        if any((c - q).length < 1.3 for q in centres): continue
        centres.append(c)
    for c in centres:
        r = rnd.uniform(1.1, 1.9); cv = rnd.random()
        outer = min(1.0, max(0.0, 0.5 * (math.hypot(c.x, c.y) / CR) + 0.5 * ((c.z - trunk_h) / (H - trunk_h))))
        clumps += 1; ncard = int(70 * (r / 1.5) ** 2)
        for j in range(ncard):
            v = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1))).normalized() * (r * rnd.uniform(0.35, 1.0) ** 0.5)
            v.z *= 0.7; q = c + v
            nrm = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.2, 1))).normalized()
            t1 = nrm.cross(Vector((0.3, 0.2, 1))).normalized(); t2 = nrm.cross(t1); sz = rnd.uniform(0.17, 0.30)
            vs = [bm.verts.new(q + (t1 * sx + t2 * sy) * sz) for (sx, sy) in ((-1, -0.7), (1, -1), (0.8, 1), (-0.9, 0.8))]
            f = bm.faces.new(vs); f.material_index = 1
            # outerness of this card: top/outside of its clump faces the sun and sky
            loc = (v.z / r) * 0.5 + 0.5; rad = Vector((q.x, q.y, 0)).normalized().dot(Vector((v.x, v.y, 0)).normalized()) * 0.5 + 0.5 if v.xy.length > 1e-3 else 0.5
            o = min(1.0, 0.45 * outer + 0.35 * loc + 0.2 * rad)
            if lv is not None: f[lv] = (rnd.random(), cv, o)
            cards += 1
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(bark_mat()); me.materials.append(leaf_mat())
    for pg in me.polygons: pg.use_smooth = pg.material_index == 0
    me["cp032_trees"] = True; me["H_m"] = round(H, 2); me["clumps"] = clumps; me["cards"] = cards
    return me, dict(H_m=round(H, 2), crown_w_m=round(2 * CR, 1), bole_d_m=round(D, 2), clumps=clumps, cards=cards, wood_faces=wood_faces)


# ---------------------------------------------------------------- hats / hair for the arrival workmen
def fit_head(o):
    """Skull from the figure's skin vertices: centre/radius from the slice 2-7 cm below the top of the head (above
    ears and nose); facing from the nose (the skin vertex furthest from the skull axis 8-14 cm down)."""
    me = o.data; mw = o.matrix_world
    skin = [i for i, s in enumerate(o.material_slots) if s.material and "skin" in s.material.name.lower()]
    hat = [i for i, s in enumerate(o.material_slots) if s.material and "hat" in s.material.name.lower()]
    vs_skin, vs_hat = set(), set()
    for p in me.polygons:
        if p.material_index in skin: vs_skin.update(p.vertices)
        elif p.material_index in hat: vs_hat.update(p.vertices)
    S = [mw @ me.vertices[i].co for i in vs_skin]; top = max(v.z for v in S)
    sl = [v for v in S if top - 0.07 < v.z < top - 0.02]
    cx = (min(v.x for v in sl) + max(v.x for v in sl)) / 2; cy = (min(v.y for v in sl) + max(v.y for v in sl)) / 2
    rad = max(max(v.x for v in sl) - min(v.x for v in sl), max(v.y for v in sl) - min(v.y for v in sl)) / 2
    face = [v for v in S if top - 0.14 < v.z < top - 0.08]
    nose = max(face, key=lambda v: math.hypot(v.x - cx, v.y - cy))
    fwd = Vector((nose.x - cx, nose.y - cy, 0)).normalized()
    H = [mw @ me.vertices[i].co for i in vs_hat]
    hz = max(v.z for v in H) if H else top
    hr = max(math.hypot(v.x - cx, v.y - cy) for v in H) if H else 0.0      # old people_lib cap disc, to be enclosed
    return Vector((cx, cy, top)), rad, hz, fwd, hr


def hat_and_hair(o, k, coll, mats, CAP_OFF):
    c, rad, hz, fwd, hr = fit_head(o); rnd = random.Random(1852 + k)
    R = rad + 0.014                                          # crown inner radius over the skull
    bm = bmesh.new(); seg = 24
    z0 = c.z - 0.065; z1 = c.z + 0.05                            # crown sits down on the brow
    tilt = Matrix.Rotation(rnd.uniform(-0.08, 0.08), 4, "X") @ Matrix.Rotation(rnd.uniform(-0.08, 0.08), 4, "Y")
    def ring(z, r, sq=1.0):
        return [bm.verts.new(Vector((math.cos(2 * math.pi * i / seg) * r, math.sin(2 * math.pi * i / seg) * r * sq, z))) for i in range(seg)]
    brim_r = R + rnd.uniform(0.045, 0.06)
    rings = [ring(-0.012 - 0.01, brim_r - 0.004), ring(-0.006, brim_r), ring(0.0, R + 0.004), ring((z1 - z0) * 0.6, R * 0.98),
             ring((z1 - z0) * 0.92, R * 0.86), ring(z1 - z0, R * 0.55)]
    for A, B in zip(rings, rings[1:]):
        for i in range(seg): bm.faces.new([A[i], A[(i + 1) % seg], B[(i + 1) % seg], B[i]])
    bm.faces.new(list(reversed(rings[-1])))
    inner = ring(-0.016, R + 0.002)
    for i in range(seg): bm.faces.new([inner[(i + 1) % seg], inner[i], rings[0][i], rings[0][(i + 1) % seg]])
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector((c.x, c.y, z0))) @ tilt, verts=bm.verts)
    me = bpy.data.meshes.new(f"ARR_HD_HAT_{k:02d}"); bm.to_mesh(me); bm.free(); me.materials.append(mats[0])
    for pg in me.polygons: pg.use_smooth = True
    h = bpy.data.objects.new(f"ARR_HD_HAT_{k:02d}", me); coll.objects.link(h)
    # hair: a short band from under the brim down the back and sides of the skull (front open for the face)
    bm = bmesh.new(); seg2 = 18
    pts_top, pts_bot = [], []
    for i in range(seg2 + 1):
        ang = math.radians(-125 + 250 * i / seg2)                          # around the back (front = 0 excluded)
        d = Vector((-fwd.x, -fwd.y, 0)); d.rotate(Matrix.Rotation(ang, 3, "Z"))
        drop = 0.075 if abs(ang) < math.radians(70) else 0.045             # lower at the nape, shorter over the ears
        pts_top.append(bm.verts.new(Vector((c.x, c.y, z0 - 0.005)) + d * (R + 0.002)))
        pts_bot.append(bm.verts.new(Vector((c.x, c.y, z0 - drop)) + d * (R - 0.006)))
    for i in range(seg2): bm.faces.new([pts_top[i], pts_top[i + 1], pts_bot[i + 1], pts_bot[i]])
    me = bpy.data.meshes.new(f"ARR_HD_HAIR_{k:02d}"); bm.to_mesh(me); bm.free(); me.materials.append(mats[1])
    for pg in me.polygons: pg.use_smooth = True
    hob = bpy.data.objects.new(f"ARR_HD_HAIR_{k:02d}", me); coll.objects.link(hob)
    for x in (h, hob): x["cp032_trees"] = True; x["figure"] = o.name
    for sl in o.material_slots:
        if sl.material and "hat" in sl.material.name.lower():
            sl.link = "OBJECT"; sl.material = CAP_OFF
    o["cp032_trees_cap_off"] = True
    return dict(figure=o.name, head_top_z=round(c.z, 3), skull_r=round(rad, 3), old_cap_r=round(hr, 3), hat_crown_r=round(R, 3), brim_r=round(brim_r, 3))


# ---------------------------------------------------------------- apply
def oak_objs(): return [o for o in bpy.data.objects if o.name.startswith("ARR_OAK_") and o.type == "MESH"]


def in_place():
    g = bpy.data.objects.get("ARR_GRASS")
    if not g or g.data.materials[0] is None or g.data.materials[0].name != "GT_SydenhamMeadow1852": return False
    if bpy.data.materials["GT_SydenhamMeadow1852"].get("cp032_trees_v") != VERSION: return False
    oo = oak_objs()
    return (len(oo) > 0 and all(o.data.get("cp032_trees") for o in oo)
            and bpy.data.objects["ARR_BEARERS_COL"].data.materials[0].name == "GT_OakBearerWeathered1852"
            and all(bpy.data.objects[f"ARR_CRATE_{i}"].instance_collection.name == "ARR_CrateSY1852_from_Muse" for i in (0, 1))
            and all(bpy.data.objects.get(f"ARR_HD_HAT_{k:02d}") for k in range(4)))


already = in_place(); info = {}
if already:
    print("CP032_TREES already applied; nothing changed")
else:
    assert bpy.data.objects.get("ARR_YD_RUTS") is not None, "needs MV18 (candidate_cp032_yard.py) first"
    assert not any(o.name.startswith("ARR_HD_") for o in bpy.data.objects), "partial state; rebuild from a clean round"
    coll = bpy.data.collections[COLL]; rnd = random.Random(P["seed"])
    # 1 trees
    old = sorted({o.data.name for o in oak_objs()})
    variants = {}
    for mn in old:
        om = bpy.data.meshes[mn]; Hm = max(v.co.z for v in om.vertices); variants[mn] = []    # keep each old tree's height
        for j in range(P["variants_per_height"]):
            me, st = build_oak(f"ARR_TR_{mn}_{j}", Hm, P["seed"] + 97 * len(variants) + 13 * j)
            zs = [v.co.z for v in me.vertices]; xs = [v.co.x for v in me.vertices]; ys = [v.co.y for v in me.vertices]
            w = max(max(xs) - min(xs), max(ys) - min(ys)); sz = Hm / max(zs); sxy = P["crown_w_over_h"] * Hm / w
            me.transform(Matrix.Diagonal((sxy, sxy, sz, 1.0)))
            st.update(H_m=round(Hm, 2), crown_w_m=round(w * sxy, 1), fit_scale_xy=round(sxy, 3), fit_scale_z=round(sz, 3))
            variants[mn].append(me); info.setdefault("oaks", {})[me.name] = st
    for i, o in enumerate(sorted(oak_objs(), key=lambda x: x.name)):
        mn = o.data.name; o.data = variants[mn][i % P["variants_per_height"]]
    for mn in old:
        me = bpy.data.meshes.get(mn)
        if me and me.users == 0: bpy.data.meshes.remove(me)
    # 2 meadow
    g = bpy.data.objects["ARR_GRASS"]; info["grass"] = [g.data.materials[0].name, "GT_SydenhamMeadow1852"]
    g.data.materials[0] = meadow_mat()
    # 3 timber
    oakw = wood_mat("GT_OakBearerWeathered1852", (0.135, 0.112, 0.086), (0.225, 0.190, 0.148), (0.35, 0.35, 6.0), 4.0)
    for on in ("ARR_BEARERS_COL", "ARR_BEARERS_GIR"): bpy.data.objects[on].data.materials[0] = oakw
    bg = bpy.data.objects["ARR_BARS_GUTTERS"]; bg.data.materials[3] = oakw
    src = bpy.data.collections["MUSE_Crate_by_Muse"]; cc = bpy.data.collections.new("ARR_CrateSY1852_from_Muse")
    cc.instance_offset = src.instance_offset
    case_w = wood_mat("GT_PackingCaseWeathered1852", (0.165, 0.132, 0.096), (0.255, 0.210, 0.158), (6.0, 0.4, 0.4), 4.0)
    deal_w = wood_mat("GT_CrateDealWeathered1852", (0.180, 0.145, 0.104), (0.275, 0.225, 0.165), (6.0, 0.4, 0.4), 4.0)
    remap = {"GT_PackingCase": case_w, "Timber": deal_w}
    for so in src.objects:
        no = so.copy(); no.name = "ARR_SY_" + so.name; cc.objects.link(no)
        for s in no.material_slots:
            mn0 = s.material.name if s.material else None
            if mn0 in remap:
                s.link = "OBJECT"; s.material = remap[mn0]
    for i in (0, 1): bpy.data.objects[f"ARR_CRATE_{i}"].instance_collection = cc
    cc["credit"] = "Muse, models/hp-crate-and-display-case (appended read-only); copy with ARR-only weathered materials (Grok)"
    # 4 hats + hair
    felt = [plain_mat("GT_FeltHat1852_a", (0.030, 0.027, 0.024), 0.85), plain_mat("GT_FeltHat1852_b", (0.055, 0.045, 0.035), 0.85)]
    hair = [plain_mat("GT_Hair1852_dk", (0.022, 0.016, 0.011), 0.6), plain_mat("GT_Hair1852_br", (0.055, 0.035, 0.020), 0.6)]
    CAP_OFF = bpy.data.materials.new("GT_CapRetired_CP032"); CAP_OFF.use_nodes = True
    nt = CAP_OFF.node_tree; nt.nodes.clear(); tb = nt.nodes.new("ShaderNodeBsdfTransparent")
    nt.links.new(tb.outputs[0], nt.nodes.new("ShaderNodeOutputMaterial").inputs[0])
    CAP_OFF["note"] = "hides the people_lib flat cap disc on ARR_HAND workmen only; replaced by ARR_HD_HAT felt hats"
    figs = [o for o in bpy.data.objects if o.name.startswith("ARR_HAND_") and "gentleman" not in o.name]
    figs = sorted(figs, key=lambda x: x.name)
    info["hats"] = [hat_and_hair(o, k, coll, (felt[k % 2], hair[k % 2]), CAP_OFF) for k, o in enumerate(figs)]
print("CP032_TREES_INFO " + json.dumps(info))
print("CP032_TREES_IN_PLACE", in_place())
if not already or not a.live:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True)
    print("CP032_TREES saved", out)
