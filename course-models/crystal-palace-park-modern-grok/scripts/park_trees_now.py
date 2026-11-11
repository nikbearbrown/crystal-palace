"""Present-day park trees for PARK-NOW (CP076 plateau CANDIDATE 2026-11-11, Grok).
Vendored copy of the parametric tree generator from our own move folder
(crystal-palace-move-1852-grok/scripts/candidate_cp076_now_v2.py, MV20 v2, KEPT 2026-11-03): node helpers,
leaf/bark materials and build_tree(), unchanged except:
  * material names are *_Now (present-day; never shared with the 1852 move set),
  * leaf ramps are brightened by LEAF_GAIN for the PARK-NOW look (exposure -0.8, present afternoon),
  * add_haze() is a no-op unless HAZE['on'] (the PARK-NOW world already carries aerosol haze, D-PM-20),
  * no hawthorn blossom (present-day leaf season only).
"""
import math, random
import bpy, bmesh
from mathutils import Vector, noise, kdtree
VERSION = "cp076_now_v1"
HAZE = dict(on=False, haze_L=600.0, haze_max=0.5, haze_rgb=(0.6, 0.65, 0.7))
LEAF_GAIN = 1.0
P = HAZE
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
    return m.outputs[0]
def _mixc(n, l, fac, ca, cb, blend="MIX"):
    m = n.new("ShaderNodeMix"); m.data_type = "RGBA"; m.blend_type = blend
    for s, i in ((fac, 0), (ca, 6), (cb, 7)):
        if isinstance(s, (int, float)): m.inputs[i].default_value = s
        elif isinstance(s, tuple): m.inputs[i].default_value = (*s, 1)
        else: l.new(s, m.inputs[i])
    return m.outputs[2]
def new_mat(name):
    old = bpy.data.materials.get(name)
    if old: return old, None, None
    m = bpy.data.materials.new(name); m.use_nodes = True; return m, m.node_tree.nodes, m.node_tree.links


def add_haze(m, k=1.0):
    if not HAZE["on"]:
        m["cp076_now"] = VERSION; return
    """Aerial perspective for camera rays: shader -> mix(shader, emission(haze radiance), hmax*(1-exp(-d/L)))."""
    nt = m.node_tree; n, l = nt.nodes, nt.links
    out = next(x for x in n if x.type == "OUTPUT_MATERIAL"); src = out.inputs[0].links[0].from_socket
    cd = n.new("ShaderNodeCameraData"); lp = n.new("ShaderNodeLightPath")
    e = _math(n, l, "EXPONENT", _math(n, l, "MULTIPLY", cd.outputs["View Distance"], -1.0 / P["haze_L"]))
    f = _math(n, l, "MULTIPLY", _math(n, l, "SUBTRACT", 1.0, e), P["haze_max"] * k)
    f = _math(n, l, "MULTIPLY", f, lp.outputs["Is Camera Ray"])
    em = n.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (*P["haze_rgb"], 1); em.inputs["Strength"].default_value = 1.0
    mx = n.new("ShaderNodeMixShader"); l.new(f, mx.inputs[0]); l.new(src, mx.inputs[1]); l.new(em.outputs[0], mx.inputs[2])
    l.new(mx.outputs[0], out.inputs[0])
    for tgt in (m, getattr(m, "cycles", None)):
        if tgt is not None and hasattr(tgt, "emission_sampling"):
            try: tgt.emission_sampling = "NONE"
            except Exception: pass
    m["cp076_now_v"] = VERSION; m["haze"] = "L=%g m, max %.2f, camera rays only" % (P["haze_L"], P["haze_max"])


# ---------------------------------------------------------------- materials
def leaf_mat(name, cols, tint_span, trans=0.25):
    """Leaf cards + clump cores: colour from attribute 'lv' (x card random, y clump random, z outerness)."""
    m, n, l = new_mat(name)
    if n is None: return m
    b = _p(m)
    at = n.new("ShaderNodeAttribute"); at.attribute_name = "lv"; at.attribute_type = "GEOMETRY"
    sep = n.new("ShaderNodeSeparateXYZ"); l.new(at.outputs["Vector"], sep.inputs[0]); oi = n.new("ShaderNodeObjectInfo")
    v = _math(n, l, "MULTIPLY", sep.outputs["Z"], 0.50)
    v = _math(n, l, "ADD", v, _math(n, l, "MULTIPLY", sep.outputs["Y"], 0.30))
    v = _math(n, l, "ADD", v, _math(n, l, "MULTIPLY", sep.outputs["X"], 0.08))
    v = _math(n, l, "ADD", v, _math(n, l, "MULTIPLY", _math(n, l, "SUBTRACT", oi.outputs["Random"], 0.5), 0.16), clamp=True)
    cols = [(pos, tuple(min(1.0, ch * LEAF_GAIN) for ch in c)) for pos, c in cols]
    r = _ramp(n, cols); l.new(v, r.inputs[0])
    tint = _ramp(n, [(0.0, tint_span[0]), (0.5, (1.0, 1.0, 1.0)), (1.0, tint_span[1])])
    rnd2 = _math(n, l, "FRACT", _math(n, l, "MULTIPLY", oi.outputs["Random"], 7.31))
    l.new(rnd2, tint.inputs[0])
    c = _mixc(n, l, 1.0, r.outputs["Color"], tint.outputs["Color"], "MULTIPLY")
    l.new(c, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.62
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.3
    tr = n.new("ShaderNodeBsdfTranslucent"); l.new(c, tr.inputs["Color"])
    mx = n.new("ShaderNodeMixShader"); mx.inputs[0].default_value = trans
    out = next(x for x in n if x.type == "OUTPUT_MATERIAL")
    l.new(b.outputs[0], mx.inputs[1]); l.new(tr.outputs[0], mx.inputs[2]); l.new(mx.outputs[0], out.inputs[0])
    m.diffuse_color = (*cols[1][1], 1); add_haze(m); return m


def bark_mat2():
    m, n, l = new_mat("GT_TreeBarkNow")
    if n is None: return m
    b = _p(m); tc = n.new("ShaderNodeTexCoord"); mp = n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (6.0, 6.0, 0.8)
    l.new(tc.outputs["Object"], mp.inputs["Vector"]); nz = _noise(n, l, mp.outputs["Vector"], 3.0, 6.0, 0.65)
    r = _ramp(n, [(0.3, (0.075, 0.066, 0.054)), (0.7, (0.160, 0.142, 0.118))]); l.new(nz.outputs["Fac"], r.inputs[0])
    l.new(r.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.95
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.4
    l.new(nz.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (0.11, 0.10, 0.085, 1); add_haze(m); return m


def blossom_mat():
    m, n, l = new_mat("GT_ThornBlossomNow")
    if n is None: return m
    b = _p(m); oi = n.new("ShaderNodeObjectInfo")
    r = _ramp(n, [(0.0, (0.26, 0.25, 0.20)), (1.0, (0.34, 0.32, 0.26))]); l.new(oi.outputs["Random"], r.inputs[0])
    l.new(r.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.7
    m.diffuse_color = (0.48, 0.46, 0.38, 1); add_haze(m); return m


LEAF = {}
def tree_mats(habit):
    if not LEAF:
        LEAF["oak"] = leaf_mat("GT_OakLeafNow", [(0.0, (0.036, 0.050, 0.020)), (0.45, (0.074, 0.096, 0.036)), (0.80, (0.122, 0.142, 0.056)), (1.0, (0.160, 0.170, 0.074))],
                               ((0.92, 1.0, 0.86), (1.12, 1.05, 0.82)))
        LEAF["elm"] = leaf_mat("GT_ElmLeafNow", [(0.0, (0.030, 0.044, 0.022)), (0.45, (0.060, 0.082, 0.040)), (0.80, (0.100, 0.124, 0.062)), (1.0, (0.135, 0.152, 0.080))],
                               ((0.90, 0.98, 0.95), (1.05, 1.03, 0.90)))
        LEAF["thorn"] = leaf_mat("GT_ThornLeafNow", [(0.0, (0.034, 0.052, 0.020)), (0.45, (0.070, 0.098, 0.034)), (0.80, (0.115, 0.145, 0.052)), (1.0, (0.150, 0.172, 0.068))],
                                 ((0.95, 1.0, 0.92), (1.06, 1.04, 0.90)))
        LEAF["far"] = leaf_mat("GT_FarWoodLeafNow", [(0.0, (0.036, 0.050, 0.024)), (0.5, (0.068, 0.088, 0.040)), (1.0, (0.120, 0.138, 0.066))],
                               ((0.90, 0.98, 0.94), (1.10, 1.05, 0.85)))
        LEAF["bark"] = bark_mat2(); LEAF["blossom"] = blossom_mat()
    return LEAF


def build_tree(name, habit, H, seed):
    rnd = random.Random(seed); segs = []; tips = []
    def branch(p, d, length, radius, depth, nkids=3):
        n = max(2, int(length / 1.2)); cur = Vector(p); dv = Vector(d).normalized(); pts = [cur.copy()]
        for i in range(n):
            dv = (dv + Vector((rnd.uniform(-.22, .22), rnd.uniform(-.22, .22), rnd.uniform(-.10, .14)))).normalized()
            cur = cur + dv * (length / n); cur.z = min(cur.z, H - 0.6); pts.append(cur.copy())
        for i, (q0, q1) in enumerate(zip(pts, pts[1:])):
            segs.append((q0, q1, radius * (1 - 0.55 * i / n), radius * (1 - 0.55 * (i + 1) / n), 7 if radius > 0.15 else 4, depth))
        if depth == 0:
            tips.extend(pts[1:]); return
        for k in range(nkids):
            t = rnd.uniform(0.35, 1.0); base = pts[max(1, min(n, int(round(t * n))))]
            ang = rnd.uniform(0, 2 * math.pi)
            nd = (dv * 0.8 + Vector((math.cos(ang), math.sin(ang), rnd.uniform(0.0, 0.7)))).normalized()
            branch(base, nd, length * rnd.uniform(0.45, 0.6), radius * 0.48, depth - 1, nkids)
    lobes = []                                   # (centre, rx, rz) ellipsoids: the crown envelope
    if habit == "oak":
        trunk_h = H * rnd.uniform(0.20, 0.25); D = H * 0.055; CR = H * rnd.uniform(0.36, 0.42); zc = trunk_h + (H - trunk_h) * 0.45
        segs.append((Vector((0, 0, -0.6)), Vector((0, 0, 0.5)), D * 0.85, D * 0.55, 10, 3)); segs.append((Vector((0, 0, 0.5)), Vector((0, 0, trunk_h + 0.3)), D * 0.55, D * 0.42, 10, 3))
        nl = rnd.randint(5, 7)
        for k in range(nl):
            ang = 2 * math.pi * k / nl + rnd.uniform(-.35, .35); low = k < 2
            elev = rnd.uniform(0.12, 0.35) if low else rnd.uniform(0.7, 1.7)
            zb = trunk_h * rnd.uniform(0.85, 1.05) + (0 if low else rnd.uniform(0, H * 0.08))
            branch(Vector((0, 0, zb)), Vector((math.cos(ang), math.sin(ang), elev)), CR * rnd.uniform(0.65, 0.85), D * rnd.uniform(0.20, 0.26), 2)
        branch(Vector((0, 0, trunk_h)), Vector((rnd.uniform(-.15, .15), rnd.uniform(-.15, .15), 1)), (H - trunk_h) * 0.75, D * 0.24, 2)
        lobes.append((Vector((0, 0, zc)), CR, (H - 1.2) - zc))
        for k in range(rnd.randint(3, 5)):                                  # irregular bulges, not a perfect dome
            ang = rnd.uniform(0, 2 * math.pi); rr = CR * rnd.uniform(0.45, 0.7)
            lobes.append((Vector((math.cos(ang) * CR * 0.55, math.sin(ang) * CR * 0.55, zc + rnd.uniform(-0.15, 0.35) * (H - zc))), rr, rr * 0.8))
        rclump = (1.1, 1.9); ncard = 46; cardsz = (0.16, 0.28); zmin = trunk_h * 0.95
    elif habit == "elm":
        trunk_h = H * rnd.uniform(0.80, 0.88); D = H * 0.040
        segs.append((Vector((0, 0, -0.6)), Vector((0, 0, 0.6)), D * 0.8, D * 0.55, 10, 3))
        segs.append((Vector((0, 0, 0.6)), Vector((0, 0, trunk_h)), D * 0.55, D * 0.22, 10, 3))
        nb = rnd.randint(7, 10)
        for k in range(nb):
            zb = H * rnd.uniform(0.22, 0.80); ang = rnd.uniform(0, 2 * math.pi)
            branch(Vector((0, 0, zb)), Vector((math.cos(ang), math.sin(ang), rnd.uniform(0.6, 1.8))), H * rnd.uniform(0.13, 0.22), D * 0.18, 1, 4)
        for k in range(rnd.randint(4, 6)):                                  # billowing stacked lobes
            t = k / 5.0; ang = rnd.uniform(0, 2 * math.pi); off = H * rnd.uniform(0.04, 0.14)
            rr = H * rnd.uniform(0.14, 0.20) * (1.0 - 0.25 * t)
            lobes.append((Vector((math.cos(ang) * off, math.sin(ang) * off, H * (0.33 + 0.52 * t))), rr, rr * 0.95))
        top = max(c.z + rz for c, rx, rz in lobes); s = (H - 0.8) / top
        lobes = [(Vector((c.x, c.y, c.z * s)), rx, rz * s) for c, rx, rz in lobes]
        rclump = (1.0, 1.6); ncard = 40; cardsz = (0.14, 0.24); zmin = H * 0.18
    elif habit == "thorn":
        trunk_h = H * 0.18; D = H * 0.05
        for k in range(rnd.randint(3, 4)):
            ang = rnd.uniform(0, 2 * math.pi)
            branch(Vector((0, 0, -0.2)), Vector((math.cos(ang) * 0.5, math.sin(ang) * 0.5, 1)), H * 0.55, D * 0.5, 1, 4)
        lobes.append((Vector((0, 0, H * 0.55)), H * 0.52, H * 0.42))
        for k in range(3):
            ang = rnd.uniform(0, 2 * math.pi); rr = H * rnd.uniform(0.25, 0.35)
            lobes.append((Vector((math.cos(ang) * H * 0.3, math.sin(ang) * H * 0.3, H * rnd.uniform(0.35, 0.65))), rr, rr * 0.85))
        rclump = (0.5, 0.85); ncard = 34; cardsz = (0.07, 0.12); zmin = H * 0.12
    else:  # far: low-LOD broadleaf for the distant belt
        trunk_h = H * rnd.uniform(0.25, 0.35); D = H * 0.05
        segs.append((Vector((0, 0, -0.6)), Vector((0, 0, trunk_h + 1.0)), D * 0.6, D * 0.35, 6, 3))
        CR = H * rnd.uniform(0.28, 0.40); zc = trunk_h + (H - trunk_h) * 0.5
        lobes.append((Vector((0, 0, zc)), CR, (H - 0.8) - zc))
        for k in range(rnd.randint(2, 4)):
            ang = rnd.uniform(0, 2 * math.pi); rr = CR * rnd.uniform(0.5, 0.75)
            lobes.append((Vector((math.cos(ang) * CR * 0.5, math.sin(ang) * CR * 0.5, zc + rnd.uniform(-0.2, 0.3) * (H - zc))), rr, rr * 0.85))
        rclump = (2.0, 3.0); ncard = 10; cardsz = (0.35, 0.55); zmin = trunk_h
    def inside(c, k=1.0):
        return any(((c.x - o.x) / rx) ** 2 + ((c.y - o.y) / rx) ** 2 + ((c.z - o.z) / rz) ** 2 < k for o, rx, rz in lobes)
    # clump centres: branch tips inside the envelope, then a shell over each lobe with sky gaps
    centres = []; rmin = rclump[0] * 0.8
    rnd.shuffle(tips)
    for tp in tips:
        c = Vector(tp) + Vector((rnd.uniform(-.6, .6), rnd.uniform(-.6, .6), rnd.uniform(0.0, 0.8)))
        if c.z < zmin or c.z > H - 0.6 or not inside(c, 1.1): continue
        if any((c - q).length < rmin for q in centres): continue
        centres.append(c)
    for o, rx, rz in lobes:
        area = 4 * math.pi * rx * max(rx, rz); nn = int(area / (rclump[1] ** 2) * 1.3) + 6
        for k in range(nn):
            th = rnd.uniform(0, 2 * math.pi); ph = math.acos(rnd.uniform(-0.45, 1.0)); rs = rnd.uniform(0.70, 0.98)
            c = o + Vector((math.cos(th) * math.sin(ph) * rx * rs, math.sin(th) * math.sin(ph) * rx * rs, math.cos(ph) * rz * rs))
            if rnd.random() < 0.16 or c.z < zmin or c.z > H - 0.6: continue
            if any((c - q).length < rclump[1] * 0.75 for q in centres): continue
            centres.append(c)
    kd = kdtree.KDTree(len(centres))
    for i, c in enumerate(centres): kd.insert(c, i)
    kd.balance()
    bm = bmesh.new(); lv = bm.faces.layers.float_vector.new("lv")
    # wood: cull finest twigs whose end is clear of the foliage (the 'antennae' at 1:1)
    culled = 0
    for (q0, q1, ra, rb, sg, dep) in segs:
        if dep <= 1 and kd.find(q1)[2] > rclump[1] + 0.25: culled += 1; continue
        d = q1 - q0
        if d.length < 1e-6: continue
        d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0))
        s = d.cross(up).normalized(); u = s.cross(d).normalized()
        A = [bm.verts.new(q0 + (s * math.cos(2 * math.pi * k / sg) + u * math.sin(2 * math.pi * k / sg)) * ra) for k in range(sg)]
        B = [bm.verts.new(q1 + (s * math.cos(2 * math.pi * k / sg) + u * math.sin(2 * math.pi * k / sg)) * rb) for k in range(sg)]
        for k in range(sg): bm.faces.new([A[k], A[(k + 1) % sg], B[(k + 1) % sg], B[k]])
    wood_faces = len(bm.faces); cards = 0; extent = max(max(rx for o, rx, rz in lobes), 1.0)
    for c in centres:
        r = rnd.uniform(*rclump); cv = rnd.random()
        outer = min(1.0, max(0.0, 0.5 * (math.hypot(c.x, c.y) / extent) + 0.5 * ((c.z - trunk_h) / max(H - trunk_h, 1.0))))
        # solid core: low icosphere, noise-displaced, interior value
        g = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r * 0.66); sd = Vector((rnd.uniform(0, 50), rnd.uniform(0, 50), 0))
        for v in g["verts"]:
            v.co = Vector((v.co.x, v.co.y, v.co.z * 0.8)) * (1.0 + 0.22 * noise.noise(v.co * 1.7 + sd)) + c
        for f in {f for v in g["verts"] for f in v.link_faces}:
            f.material_index = 1; f[lv] = (0.5, cv, outer * 0.55)
        nc = int(ncard * (r / sum(rclump) * 2) ** 2)
        for j in range(nc):
            dvec = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1))).normalized()
            q = c + Vector((dvec.x, dvec.y, dvec.z * 0.78)) * (r * rnd.uniform(0.62, 1.0))
            nrm = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.2, 1))).normalized()
            t1 = nrm.cross(Vector((0.3, 0.2, 1))).normalized(); t2 = nrm.cross(t1); sz = rnd.uniform(*cardsz)
            vs = [bm.verts.new(q + (t1 * sx + t2 * sy) * sz) for (sx, sy) in ((-1, -0.7), (1, -1), (0.8, 1), (-0.9, 0.8))]
            f = bm.faces.new(vs)
            bl = False  # present-day: no blossom
            f.material_index = 2 if bl else 1
            o2 = min(1.0, 0.5 * outer + 0.3 * (dvec.z * 0.5 + 0.5) + 0.2 * (Vector((q.x, q.y, 0)).normalized().dot(Vector((dvec.x, dvec.y, 0)).normalized()) * 0.5 + 0.5 if dvec.xy.length > 1e-3 and q.xy.length > 1e-3 else 0.5))
            f[lv] = (rnd.random(), cv, o2); cards += 1
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    M = tree_mats(habit)
    me.materials.append(M["bark"]); me.materials.append(M[habit]); me.materials.append(M["blossom"])
    for pg in me.polygons: pg.use_smooth = pg.material_index == 0
    me["cp076_now"] = VERSION; me["habit"] = habit; me["H_m"] = round(H, 2)
    return me, dict(habit=habit, H_m=round(H, 2), clumps=len(centres), cards=cards, wood_faces=wood_faces, twigs_culled=culled, faces=len(me.polygons))


