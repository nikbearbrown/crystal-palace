"""CP032 arrival parkland depth + aerial haze, meadow variation, cut cart ruts (2026-11-03, Grok; CANDIDATE, no
verdict; DEPARTURES MV20).

blender -b rounds/m02.blend -P scripts/candidate_cp032_haze.py -- [--out rounds/candidates/m02_cp032haze.blend]
blender -b ROUND.blend -P scripts/candidate_cp032_haze.py -- --live     # apply in place (only after a KEEP call)
Idempotent; always prints `CP032_HAZE_IN_PLACE True|False`. Needs MV17, MV18 and MV19 in place.

Sydenham (Penge Place) 1852 only; nothing of Hyde Park 1851 and nothing of the Sydenham building.
 1. Trees (ARR_OAK_* keep their locations and rotations): the 8 MV19 oak meshes are rebuilt (ARR_TR2_oak_*) with a
    solid displaced core inside every leaf clump (so the crown edge reads as massed foliage, not confetti), lower
    card-to-card value contrast, and bare twig tips that poke out of the foliage culled. A third of the interior
    trees become English elms (ARR_TR2_elm_*, tall lobed 'billowing' crowns, 23-30 m); every ARR_OAK_* gets a
    per-object scale 0.80-1.15 (about its trunk foot). New ARR_PK_* objects: a loose second belt of hazy woodland
    on the rising ground 260-420 m out (ARR_PK_FAR_*, low-LOD broadleaf), and three hawthorns at 50-70 m
    (ARR_PK_THORN_*, late 'may' blossom fading, early June). All tree leaf/bark materials are new (*_h) and carry
    an aerial-perspective term: camera rays only, mix toward the horizon haze radiance by 1 - exp(-d / L).
 2. Meadow: ARR_GRASS -> GT_SydenhamMeadow1852b (stronger pasture patches, hay-mown swathes, a trodden worn margin
    round the yard, buttercup / sorrel flecks, same haze term), plus ARR_PK_TUSSOCKS (grass-blade tussocks on the
    near meadow, 13-75 m) and ARR_PK_TRACK (a worn two-wheel cart track crossing the meadow from the yard ruts).
 3. Ruts: ARR_YD_RUTS mesh rebuilt on the MV18 centrelines with a cut-groove profile (floor at the clay, pushed-up
    lumpy clay lips 3-6 cm), material -> GT_CartRutClay2 (damp clay floor, not a flat dark band).
All by eye (grade D). Cameras, exposure, figures, ironwork, yard dressing other than the ruts: unchanged.
"""
import os, sys, json, math, random, argparse
import bpy, bmesh
from mathutils import Vector, Matrix, noise, kdtree

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser(); ap.add_argument("--out", default="rounds/candidates/m02_cp032haze.blend")
ap.add_argument("--live", action="store_true")
a = ap.parse_args(argv)
if a.live:
    out = os.path.abspath(bpy.data.filepath)
else:
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(here, a.out) if not os.path.isabs(a.out) else a.out
    assert os.path.abspath(out) != os.path.abspath(bpy.data.filepath), "refusing to overwrite the opened blend without --live"

VERSION = 1
COLL = "ARR_SYDENHAM_1852"
P = dict(
    seed=18520603,
    haze_L=315.0, haze_max=0.92, haze_rgb=(0.150, 0.158, 0.172),     # horizon radiance (calibrated against the look sky)
    elm_frac=0.28, elm_H=(20.0, 25.5), scale=(0.80, 1.15),
    far_n=46, far_box=(265.0, 418.0, 372.0, 600.0), far_H=(13.0, 22.0),
    thorns=[(54.0, 447.5, 5.6), (58.5, 452.5, 4.6), (69.0, 506.0, 6.2)],
    tussocks=9000, tuss_box=(13.0, 75.0), track=[(16.5, 488.4), (24.0, 487.6), (34.0, 485.2), (48.0, 480.0), (66.0, 472.5), (88.0, 462.0), (112.0, 449.0)],
    gauge=1.524,
)
# MV18 rut centrelines (copied from candidate_cp032_yard.py so the grooves sit where the old ribbons were)
TRACKS_DEF = [
    ("wagon", [(-3.2, 479.80), (1.0, 480.05), (5.5, 480.9), (10.0, 482.6), (14.5, 485.4), (19.0, 488.6)], 1.0, 1.0, 0.3, 2.0),
    ("old_a", [(13.0, 482.6), (8.0, 485.0), (3.5, 487.85), (-0.5, 488.05), (-4.5, 488.0), (-8.0, 487.55), (-12.0, 487.0)], 0.75, 0.7, 2.0, 2.5),
    ("old_b", [(9.5, 494.4), (5.0, 493.4), (1.0, 492.9), (-3.0, 492.6), (-7.5, 492.9), (-12.5, 494.0)], 0.5, 0.45, 2.0, 2.0),
]


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
    m["cp032_haze_v"] = VERSION; m["haze"] = "L=%g m, max %.2f, camera rays only" % (P["haze_L"], P["haze_max"])


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
    m, n, l = new_mat("GT_TreeBark1852h")
    if n is None: return m
    b = _p(m); tc = n.new("ShaderNodeTexCoord"); mp = n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (6.0, 6.0, 0.8)
    l.new(tc.outputs["Object"], mp.inputs["Vector"]); nz = _noise(n, l, mp.outputs["Vector"], 3.0, 6.0, 0.65)
    r = _ramp(n, [(0.3, (0.075, 0.066, 0.054)), (0.7, (0.160, 0.142, 0.118))]); l.new(nz.outputs["Fac"], r.inputs[0])
    l.new(r.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.95
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.4
    l.new(nz.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (0.11, 0.10, 0.085, 1); add_haze(m); return m


def blossom_mat():
    m, n, l = new_mat("GT_ThornBlossom1852h")
    if n is None: return m
    b = _p(m); oi = n.new("ShaderNodeObjectInfo")
    r = _ramp(n, [(0.0, (0.26, 0.25, 0.20)), (1.0, (0.34, 0.32, 0.26))]); l.new(oi.outputs["Random"], r.inputs[0])
    l.new(r.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.7
    m.diffuse_color = (0.48, 0.46, 0.38, 1); add_haze(m); return m


def meadow_mat2():
    """Penge Place pasture, early June 1852, v2: stronger patches, hay-mown swathes, trodden margin round the yard."""
    m, n, l = new_mat("GT_SydenhamMeadow1852b")
    if n is None: return m
    b = _p(m); tc = n.new("ShaderNodeTexCoord"); v = tc.outputs["Object"]             # ARR_GRASS at the origin: metres
    sep = n.new("ShaderNodeSeparateXYZ"); l.new(v, sep.inputs[0])
    macro = _noise(n, l, v, 0.010, 3.0, 0.55)                     # ~100 m pasture patches
    meso = _noise(n, l, v, 0.07, 4.0, 0.6)                        # ~14 m swathes / soft patches
    tus = _noise(n, l, v, 0.9, 5.0, 0.7)                          # tussock scale
    fine = _noise(n, l, v, 9.0, 3.0, 0.6)
    lush = (0.018, 0.034, 0.010); mid = (0.048, 0.066, 0.022); dry = (0.150, 0.134, 0.060)
    base = _ramp(n, [(0.36, lush), (0.50, mid), (0.64, dry)]); l.new(macro.outputs["Fac"], base.inputs[0])
    sw = _ramp(n, [(0.36, (0.48, 0.56, 0.50)), (0.64, (1.40, 1.32, 1.15))]); l.new(meso.outputs["Fac"], sw.inputs[0])
    c = _mixc(n, l, 1.0, base.outputs["Color"], sw.outputs["Color"], "MULTIPLY")
    # hay-mown swathes: 1.8 m strips at 32 deg, only in some fields (mask from a second macro noise)
    rot = _math(n, l, "ADD", _math(n, l, "MULTIPLY", sep.outputs["X"], math.cos(0.56)), _math(n, l, "MULTIPLY", sep.outputs["Y"], math.sin(0.56)))
    wob = _noise(n, l, v, 0.05, 2.0)
    rot = _math(n, l, "ADD", rot, _math(n, l, "MULTIPLY", wob.outputs["Fac"], 3.0))
    st = _math(n, l, "SINE", _math(n, l, "MULTIPLY", rot, 2 * math.pi / 3.6))
    stripe = _math(n, l, "GREATER_THAN", st, 0.0)
    fm = _noise(n, l, _mixc(n, l, 1.0, v, (0.37, 0.71, 0.0), "ADD"), 0.006, 2.0)
    fmask = _math(n, l, "GREATER_THAN", fm.outputs["Fac"], 0.53)
    mown = _mixc(n, l, 1.0, c, (1.55, 1.42, 1.15), "MULTIPLY")          # pale stubble / turned hay
    uncut = _mixc(n, l, 1.0, c, (0.80, 0.86, 0.80), "MULTIPLY")
    cm = _mixc(n, l, stripe, uncut, mown)
    c = _mixc(n, l, fmask, c, cm)
    # trodden margin round the receiving yard (box x -15..22, y 476..506): worn, paler, bare clay showing
    dx = _math(n, l, "SUBTRACT", _math(n, l, "ABSOLUTE", _math(n, l, "SUBTRACT", sep.outputs["X"], 3.5)), 18.5)
    dy = _math(n, l, "SUBTRACT", _math(n, l, "ABSOLUTE", _math(n, l, "SUBTRACT", sep.outputs["Y"], 491.0)), 15.0)
    dd = _math(n, l, "MAXIMUM", dx, dy)
    wn = _noise(n, l, v, 0.35, 4.0, 0.6)
    dd = _math(n, l, "ADD", dd, _math(n, l, "MULTIPLY", wn.outputs["Fac"], 10.0))
    worn = n.new("ShaderNodeMapRange"); worn.inputs["From Min"].default_value = 10.0; worn.inputs["From Max"].default_value = 1.0
    l.new(dd, worn.inputs["Value"])
    bare = _ramp(n, [(0.42, (0.070, 0.074, 0.038)), (0.62, (0.118, 0.100, 0.066))]); l.new(_noise(n, l, v, 1.6, 4.0).outputs["Fac"], bare.inputs[0])
    c = _mixc(n, l, _math(n, l, "MULTIPLY", worn.outputs["Result"], 0.65), c, bare.outputs["Color"])
    tsr = _ramp(n, [(0.30, (0.66, 0.72, 0.66)), (0.70, (1.18, 1.14, 1.06))]); l.new(tus.outputs["Fac"], tsr.inputs[0])
    c = _mixc(n, l, 1.0, c, tsr.outputs["Color"], "MULTIPLY")
    fl = _math(n, l, "GREATER_THAN", fine.outputs["Fac"], 0.67)
    c = _mixc(n, l, _math(n, l, "MULTIPLY", fl, 0.40), c, (0.150, 0.135, 0.075))             # straw / seed heads
    vor = n.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 2.2; l.new(v, vor.inputs["Vector"])
    bc = _math(n, l, "GREATER_THAN", vor.outputs["Color"], 0.93)                               # buttercup flecks
    bf = _math(n, l, "MULTIPLY", _math(n, l, "LESS_THAN", vor.outputs["Distance"], 0.18), bc)
    c = _mixc(n, l, _math(n, l, "MULTIPLY", bf, 0.8), c, (0.30, 0.24, 0.025))
    sor = _math(n, l, "MULTIPLY", _math(n, l, "LESS_THAN", vor.outputs["Distance"], 0.14), _math(n, l, "LESS_THAN", vor.outputs["Color"], 0.05))
    c = _mixc(n, l, _math(n, l, "MULTIPLY", sor, 0.7), c, (0.11, 0.045, 0.025))                 # sorrel
    l.new(c, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.92
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.25
    h = _math(n, l, "ADD", tus.outputs["Fac"], _math(n, l, "MULTIPLY", fine.outputs["Fac"], 0.6))
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.4; bp.inputs["Distance"].default_value = 0.06
    l.new(h, bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (*mid, 1); add_haze(m); return m


def tussock_mat():
    m, n, l = new_mat("GT_MeadowTussock1852h")
    if n is None: return m
    b = _p(m); at = n.new("ShaderNodeAttribute"); at.attribute_name = "tv"
    sep = n.new("ShaderNodeSeparateXYZ"); l.new(at.outputs["Vector"], sep.inputs[0])   # x clump random, y height along blade, z kind
    base = _ramp(n, [(0.0, (0.040, 0.058, 0.020)), (0.5, (0.068, 0.084, 0.032)), (1.0, (0.120, 0.114, 0.056))]); l.new(sep.outputs["X"], base.inputs[0])
    tip = _ramp(n, [(0.0, (0.70, 0.74, 0.70)), (1.0, (1.05, 1.03, 0.98))]); l.new(sep.outputs["Y"], tip.inputs[0])
    c = _mixc(n, l, 1.0, base.outputs["Color"], tip.outputs["Color"], "MULTIPLY")
    k = _math(n, l, "GREATER_THAN", sep.outputs["Z"], 0.5)
    c = _mixc(n, l, k, c, (0.105, 0.092, 0.052))                                         # seeding / dry bents
    l.new(c, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.8
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.3
    tr = n.new("ShaderNodeBsdfTranslucent"); l.new(c, tr.inputs["Color"])
    mx = n.new("ShaderNodeMixShader"); mx.inputs[0].default_value = 0.2
    out = next(x for x in n if x.type == "OUTPUT_MATERIAL")
    l.new(b.outputs[0], mx.inputs[1]); l.new(tr.outputs[0], mx.inputs[2]); l.new(mx.outputs[0], out.inputs[0])
    m.diffuse_color = (0.06, 0.075, 0.03, 1); add_haze(m); return m


def track_mat():
    m, n, l = new_mat("GT_MeadowCartTrack1852h")
    if n is None: return m
    b = _p(m); tc = n.new("ShaderNodeTexCoord"); v = tc.outputs["Object"]
    at = n.new("ShaderNodeAttribute"); at.attribute_name = "wear"
    nz = _noise(n, l, v, 1.8, 5.0, 0.6)
    soil = _ramp(n, [(0.35, (0.088, 0.074, 0.052)), (0.65, (0.150, 0.124, 0.088))]); l.new(nz.outputs["Fac"], soil.inputs[0])
    flat = _ramp(n, [(0.35, (0.070, 0.074, 0.034)), (0.65, (0.125, 0.118, 0.060))]); l.new(nz.outputs["Fac"], flat.inputs[0])
    wn = _noise(n, l, v, 3.5, 3.0); w = _math(n, l, "MULTIPLY", at.outputs["Fac"], _math(n, l, "ADD", 0.55, _math(n, l, "MULTIPLY", wn.outputs["Fac"], 0.9)), clamp=True)
    c = _mixc(n, l, w, flat.outputs["Color"], soil.outputs["Color"])
    l.new(c, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.9
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.25
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.5; bp.inputs["Distance"].default_value = 0.03
    l.new(_noise(n, l, v, 12.0, 3.0).outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    out = next(x for x in n if x.type == "OUTPUT_MATERIAL")
    aa = n.new("ShaderNodeAttribute"); aa.attribute_name = "talpha"
    an = _noise(n, l, v, 4.0, 3.0)
    al = _math(n, l, "MULTIPLY", aa.outputs["Fac"], _math(n, l, "ADD", 0.45, an.outputs["Fac"]), clamp=True)
    tr = n.new("ShaderNodeBsdfTransparent"); ms = n.new("ShaderNodeMixShader")
    l.new(al, ms.inputs[0]); l.new(tr.outputs[0], ms.inputs[1]); l.new(b.outputs[0], ms.inputs[2]); l.new(ms.outputs[0], out.inputs[0])
    m.diffuse_color = (0.1, 0.09, 0.06, 1); add_haze(m); return m


C_RUT_FLOOR = (0.058, 0.048, 0.036)
def rut_mat2():
    m, n, l = new_mat("GT_CartRutClay2")
    if n is None: return m
    b = _p(m); at = n.new("ShaderNodeAttribute"); at.attribute_name = "groove"
    tc = n.new("ShaderNodeTexCoord"); nz = _noise(n, l, tc.outputs["Object"], 7.0, 5.0, 0.6)
    lip = _ramp(n, [(0.30, (0.090, 0.075, 0.056)), (0.72, (0.148, 0.124, 0.089))]); l.new(nz.outputs["Fac"], lip.inputs[0])
    fl = _ramp(n, [(0.30, C_RUT_FLOOR), (0.72, (0.085, 0.070, 0.052))]); l.new(nz.outputs["Fac"], fl.inputs[0])
    c = _mixc(n, l, at.outputs["Fac"], lip.outputs["Color"], fl.outputs["Color"])
    l.new(c, b.inputs["Base Color"])
    rr = n.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = 0.94; rr.inputs["To Max"].default_value = 0.70
    l.new(at.outputs["Fac"], rr.inputs["Value"]); l.new(rr.outputs["Result"], b.inputs["Roughness"])
    g = _noise(n, l, tc.outputs["Object"], 40.0, 3.0)
    vo = n.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 16.0; l.new(tc.outputs["Object"], vo.inputs["Vector"])
    hh = _math(n, l, "ADD", vo.outputs["Distance"], g.outputs["Fac"])
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.7; bp.inputs["Distance"].default_value = 0.02
    l.new(hh, bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.3
    out = next(x for x in n if x.type == "OUTPUT_MATERIAL")
    aa = n.new("ShaderNodeAttribute"); aa.attribute_name = "ralpha"
    tr = n.new("ShaderNodeBsdfTransparent"); ms = n.new("ShaderNodeMixShader")
    l.new(aa.outputs["Fac"], ms.inputs[0]); l.new(tr.outputs[0], ms.inputs[1]); l.new(b.outputs[0], ms.inputs[2])
    l.new(ms.outputs[0], out.inputs["Surface"])
    m.diffuse_color = (*C_RUT_FLOOR, 1); m["cp032_haze_v"] = VERSION; return m


# ---------------------------------------------------------------- tree generator v2 (metres, origin at trunk foot)
LEAF = {}
def tree_mats(habit):
    if not LEAF:
        LEAF["oak"] = leaf_mat("GT_OakLeaf1852h", [(0.0, (0.036, 0.050, 0.020)), (0.45, (0.074, 0.096, 0.036)), (0.80, (0.122, 0.142, 0.056)), (1.0, (0.160, 0.170, 0.074))],
                               ((0.92, 1.0, 0.86), (1.12, 1.05, 0.82)))
        LEAF["elm"] = leaf_mat("GT_ElmLeaf1852h", [(0.0, (0.030, 0.044, 0.022)), (0.45, (0.060, 0.082, 0.040)), (0.80, (0.100, 0.124, 0.062)), (1.0, (0.135, 0.152, 0.080))],
                               ((0.90, 0.98, 0.95), (1.05, 1.03, 0.90)))
        LEAF["thorn"] = leaf_mat("GT_ThornLeaf1852h", [(0.0, (0.034, 0.052, 0.020)), (0.45, (0.070, 0.098, 0.034)), (0.80, (0.115, 0.145, 0.052)), (1.0, (0.150, 0.172, 0.068))],
                                 ((0.95, 1.0, 0.92), (1.06, 1.04, 0.90)))
        LEAF["far"] = leaf_mat("GT_FarWoodLeaf1852h", [(0.0, (0.036, 0.050, 0.024)), (0.5, (0.068, 0.088, 0.040)), (1.0, (0.120, 0.138, 0.066))],
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
            bl = habit == "thorn" and rnd.random() < 0.05 and dvec.z > 0.1
            f.material_index = 2 if bl else 1
            o2 = min(1.0, 0.5 * outer + 0.3 * (dvec.z * 0.5 + 0.5) + 0.2 * (Vector((q.x, q.y, 0)).normalized().dot(Vector((dvec.x, dvec.y, 0)).normalized()) * 0.5 + 0.5 if dvec.xy.length > 1e-3 and q.xy.length > 1e-3 else 0.5))
            f[lv] = (rnd.random(), cv, o2); cards += 1
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    M = tree_mats(habit)
    me.materials.append(M["bark"]); me.materials.append(M[habit]); me.materials.append(M["blossom"])
    for pg in me.polygons: pg.use_smooth = pg.material_index == 0
    me["cp032_haze"] = VERSION; me["habit"] = habit; me["H_m"] = round(H, 2)
    return me, dict(habit=habit, H_m=round(H, 2), clumps=len(centres), cards=cards, wood_faces=wood_faces, twigs_culled=culled, faces=len(me.polygons))


# ---------------------------------------------------------------- ground helpers
def ray_z(objs, x, y):
    best = None
    for o in objs:
        mi = o.matrix_world.inverted(); org = mi @ Vector((x, y, 300.0)); d = (mi.to_3x3() @ Vector((0, 0, -1))).normalized()
        ok, loc, nrm, _ = o.ray_cast(org, d)
        if ok:
            z = (o.matrix_world @ loc).z
            if best is None or z > best: best = z
    return best


def catmull(pts, step):
    P_ = [Vector(p) for p in pts]; P_ = [P_[0] * 2 - P_[1]] + P_ + [P_[-1] * 2 - P_[-2]]
    out_ = []
    for i in range(1, len(P_) - 2):
        p0, p1, p2, p3 = P_[i - 1:i + 3]; nseg = max(2, int((p2 - p1).length / step))
        for k in range(nseg):
            t = k / nseg; t2, t3 = t * t, t * t * t
            out_.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out_.append(P_[-2]); return out_


def ruts_v2():
    """Cut-groove profile on the MV18 centrelines: floor down at the clay (3 mm clear), lumpy pushed-up lips."""
    GROUND = [bpy.data.objects[n] for n in ("ARR_CLAY", "ARR_SPOIL")]; G = P["gauge"]
    PROF_S = [-0.40, -0.30, -0.22, -0.16, -0.11, -0.07, -0.03, 0.0, 0.03, 0.07, 0.11, 0.16, 0.22, 0.30, 0.40]
    PROF_H = [0.000, 0.012, 0.034, 0.046, 0.030, 0.006, 0.000, 0.000, 0.000, 0.006, 0.030, 0.046, 0.034, 0.012, 0.000]
    PROF_G = [0.0, 0.0, 0.0, 0.05, 0.35, 0.85, 1.0, 1.0, 1.0, 0.85, 0.35, 0.05, 0.0, 0.0, 0.0]
    PROF_A = [0.0, 0.55, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.55, 0.0]
    bm = bmesh.new(); lay = bm.verts.layers.float.new("groove"); lay_a = bm.verts.layers.float.new("ralpha"); info = []
    for name, ctrl, gsc, bsc, fin, fout in TRACKS_DEF:
        cl = catmull(ctrl, 0.05); L = [0.0]
        for i in range(1, len(cl)): L.append(L[-1] + (cl[i] - cl[i - 1]).length)
        tot = L[-1]
        for side in (-1, 1):
            rows = []
            for i, c in enumerate(cl):
                tng = (cl[min(i + 1, len(cl) - 1)] - cl[max(i - 1, 0)]).normalized(); nrm = Vector((-tng.y, tng.x))
                w = min(1.0, L[i] / fin if fin else 1.0, (tot - L[i]) / fout if fout else 1.0)
                wob = 0.035 * noise.noise(Vector((L[i] * 0.7, side * 3.1, 0.5))) + 0.06 * noise.noise(Vector((L[i] * 0.12, 7.7, 0.5)))
                cc = c + nrm * (side * G / 2 + wob); row = []
                for s, h, gv, av in zip(PROF_S, PROF_H, PROF_G, PROF_A):
                    lump = 1.0 + 0.45 * noise.noise(Vector((L[i] * 1.3, s * 5.0, side * 2.0))) + 0.15 * noise.noise(Vector((L[i] * 4.0, s * 9.0, side)))
                    p = cc + nrm * (s * (1.0 + 0.15 * noise.noise(Vector((L[i] * 0.8, s, 4.0)))))
                    z = ray_z(GROUND, p.x, p.y)
                    if z is None: row.append(None); continue
                    v = bm.verts.new((p.x, p.y, z + 0.003 + h * bsc * w * max(0.15, lump)))
                    v[lay_a] = av * min(1.0, 0.2 + w); v[lay] = gv * w * gsc ** 0.5
                    row.append(v)
                rows.append(row)
            for r0, r1 in zip(rows, rows[1:]):
                for j in range(len(PROF_S) - 1):
                    q = [r0[j], r0[j + 1], r1[j + 1], r1[j]]
                    if all(q): bm.faces.new(q)
        info.append((name, round(tot, 2)))
    bm.normal_update()
    for f in bm.faces:
        if f.normal.z < 0: f.normal_flip()
    me = bpy.data.meshes.new("ARR_YD_RUTS_v2"); bm.to_mesh(me); bm.free(); me.materials.append(rut_mat2())
    for pg in me.polygons: pg.use_smooth = True
    me["cp032_haze"] = VERSION; return me, info


def cart_track(coll):
    """Worn two-wheel cart track across the pasture from the yard ruts (flattened grass, bare clay in the wheel lines)."""
    g = [bpy.data.objects["ARR_GRASS"]]; G = P["gauge"]
    cl = catmull(P["track"], 0.25); L = [0.0]
    for i in range(1, len(cl)): L.append(L[-1] + (cl[i] - cl[i - 1]).length)
    tot = L[-1]
    bm = bmesh.new(); lw = bm.verts.layers.float.new("wear"); la = bm.verts.layers.float.new("talpha")
    for side, half, wear in ((-1, 0.32, 1.0), (1, 0.32, 1.0), (0, 0.45, 0.55)):       # two wheel lines + the horse path
        prof = [(-half, 0.0), (-half * 0.5, 1.0), (0.0, 1.0), (half * 0.5, 1.0), (half, 0.0)]
        rows = []
        for i, c in enumerate(cl):
            tng = (cl[min(i + 1, len(cl) - 1)] - cl[max(i - 1, 0)]).normalized(); nrm = Vector((-tng.y, tng.x))
            fade = min(1.0, L[i] / 3.0, (tot - L[i]) / 12.0)
            wob = 0.05 * noise.noise(Vector((L[i] * 0.4, side * 2.0, 9.0)))
            cc = c + nrm * (side * G / 2 + wob); row = []
            for s, av in prof:
                p = cc + nrm * s; z = ray_z(g, p.x, p.y)
                v = bm.verts.new((p.x, p.y, (z or 0.0) + 0.012 + 0.0004 * L[i]))
                v[la] = av * fade; v[lw] = wear; row.append(v)
            rows.append(row)
        for r0, r1 in zip(rows, rows[1:]):
            for j in range(len(prof) - 1): bm.faces.new([r0[j], r0[j + 1], r1[j + 1], r1[j]])
    bm.normal_update()
    for f in bm.faces:
        if f.normal.z < 0: f.normal_flip()
    me = bpy.data.meshes.new("ARR_PK_TRACK"); bm.to_mesh(me); bm.free(); me.materials.append(track_mat())
    ob = bpy.data.objects.new("ARR_PK_TRACK", me); coll.objects.link(ob); ob["cp032_haze"] = VERSION
    return ob, cl, round(tot, 1)


def tussocks(coll, rnd, track_cl, cams):
    """Grass-blade tussocks on the near meadow (x 13-75 m), only inside the two CP032 arrival frusta."""
    from bpy_extras.object_utils import world_to_camera_view as w2c
    sc = bpy.context.scene; g = [bpy.data.objects["ARR_GRASS"]]
    avoid = []
    for n in ("ARR_HUT", "ARR_SPOIL", "ARR_CLAY", "ARR_PEGS"):
        o = bpy.data.objects[n]; bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        avoid.append((min(v.x for v in bb) - 0.6, max(v.x for v in bb) + 0.6, min(v.y for v in bb) - 0.6, max(v.y for v in bb) + 0.6))
    tkd = kdtree.KDTree(len(track_cl))
    for i, c in enumerate(track_cl): tkd.insert(Vector((c.x, c.y, 0)), i)
    tkd.balance()
    bm = bmesh.new(); tv = bm.faces.layers.float_vector.new("tv"); n = 0; tries = 0
    x0, x1 = P["tuss_box"]
    while n < P["tussocks"] and tries < 200000:
        tries += 1
        x = x0 + (x1 - x0) * rnd.random() ** 1.6; y = rnd.uniform(430.0, 530.0)       # denser near the camera
        if any(a0 < x < a1 and b0 < y < b1 for a0, a1, b0, b1 in avoid): continue
        if tkd.find(Vector((x, y, 0)))[2] < 1.25: continue
        z = ray_z(g, x, y)
        if z is None: continue
        p = Vector((x, y, z))
        if not any(0.0 <= w2c(sc, c, p).x <= 1.0 and 0.0 <= w2c(sc, c, p).y <= 1.0 for c in cams): continue
        ck = rnd.random(); kind = 1.0 if rnd.random() < 0.18 else 0.0
        hh = rnd.uniform(0.05, 0.16) * (1.35 if kind else 1.0); nb = rnd.randint(5, 8)
        for b in range(nb):
            ang = rnd.uniform(0, 2 * math.pi); lean = rnd.uniform(0.1, 0.6)
            base = p + Vector((math.cos(ang), math.sin(ang), 0)) * rnd.uniform(0, 0.09) + Vector((0, 0, -0.02))
            tip = base + Vector((math.cos(ang) * lean, math.sin(ang) * lean, 1.0)).normalized() * hh * rnd.uniform(0.7, 1.15)
            side = Vector((-math.sin(ang), math.cos(ang), 0)) * rnd.uniform(0.012, 0.022)
            v0 = bm.verts.new(base - side); v1 = bm.verts.new(base + side); v2 = bm.verts.new(tip)
            f = bm.faces.new([v0, v1, v2]); f[tv] = (ck, 0.6, kind)
        n += 1
    me = bpy.data.meshes.new("ARR_PK_TUSSOCKS"); bm.to_mesh(me); bm.free(); me.materials.append(tussock_mat())
    # blade value: darker at the base -> lighter tips via a per-corner attribute is overkill; use per-face y
    ob = bpy.data.objects.new("ARR_PK_TUSSOCKS", me); coll.objects.link(ob); ob["cp032_haze"] = VERSION
    return ob, n


# ---------------------------------------------------------------- apply
def oak_objs(): return sorted([o for o in bpy.data.objects if o.name.startswith("ARR_OAK_") and o.type == "MESH"], key=lambda x: x.name)


def in_place():
    g = bpy.data.objects.get("ARR_GRASS"); r = bpy.data.objects.get("ARR_YD_RUTS")
    if not g or g.data.materials[0] is None or g.data.materials[0].name != "GT_SydenhamMeadow1852b": return False
    if bpy.data.materials["GT_SydenhamMeadow1852b"].get("cp032_haze_v") != VERSION: return False
    oo = oak_objs()
    return (len(oo) > 0 and all(o.data.get("cp032_haze") == VERSION for o in oo) and r is not None and r.data.get("cp032_haze") == VERSION
            and all(bpy.data.objects.get(n) for n in ("ARR_PK_TRACK", "ARR_PK_TUSSOCKS", "ARR_PK_THORN_00", "ARR_PK_FAR_00")))


already = in_place(); info = {}
if already:
    print("CP032_HAZE already applied; nothing changed")
else:
    assert bpy.data.materials.get("GT_SydenhamMeadow1852") and bpy.data.objects.get("ARR_HD_HAT_00"), "needs MV19 (candidate_cp032_trees.py) first"
    assert not any(o.name.startswith("ARR_PK_") for o in bpy.data.objects), "partial state; rebuild from a clean round"
    coll = bpy.data.collections[COLL]; rnd = random.Random(P["seed"])
    cams = [bpy.data.objects["CP032_arrival_start"], bpy.data.objects["CP032_arrival_end"]]
    # 1a oaks rebuilt (same heights as MV19) + elms
    oo = oak_objs(); old = sorted({o.data.name for o in oo}); new = {}
    for k, mn in enumerate(old):
        Hm = bpy.data.meshes[mn].get("H_m") or max(v.co.z for v in bpy.data.meshes[mn].vertices)
        me, st = build_tree(mn.replace("ARR_TR_", "ARR_TR2_"), "oak", Hm, P["seed"] + 101 * k)
        xs = [v.co.x for v in me.vertices]; ys = [v.co.y for v in me.vertices]; zs = [v.co.z for v in me.vertices]
        w = max(max(xs) - min(xs), max(ys) - min(ys)); sz = Hm / max(zs); sxy = 0.85 * Hm / w
        me.transform(Matrix.Diagonal((sxy, sxy, sz, 1.0))); st.update(fit_xy=round(sxy, 3), fit_z=round(sz, 3), crown_w_m=round(w * sxy, 1))
        new[mn] = me; info.setdefault("trees", {})[me.name] = st
    elms = []
    for k in range(4):
        H = rnd.uniform(*P["elm_H"]); me, st = build_tree("ARR_TR2_elm_%d" % k, "elm", H, P["seed"] + 7000 + 31 * k)
        elms.append(me); info["trees"][me.name] = st
    interior = [o for o in oo if not o.name.startswith("ARR_OAK_EDGE")]
    elm_set = set(o.name for o in rnd.sample(interior, int(len(interior) * P["elm_frac"])))
    info["elm_objects"] = sorted(elm_set); info["scales"] = {}
    for i, o in enumerate(oo):
        o.data = elms[i % len(elms)] if o.name in elm_set else new[o.data.name]
        s = rnd.uniform(*P["scale"]); o.scale = (s, s, s); info["scales"][o.name] = round(s, 3)
    for mn in old:
        me = bpy.data.meshes.get(mn)
        if me and me.users == 0: bpy.data.meshes.remove(me)
    # 1b far woodland belt + hawthorns
    far = []
    for k in range(4):
        me, st = build_tree("ARR_TR2_far_%d" % k, "far", 18.0, P["seed"] + 9000 + 17 * k); far.append(me); info["trees"][me.name] = st
    g = [bpy.data.objects["ARR_GRASS"]]; fx0, fx1, fy0, fy1 = P["far_box"]
    groups = [(rnd.uniform(fx0, fx1), rnd.uniform(fy0, fy1), rnd.uniform(12, 30)) for _ in range(11)]   # loose copses + gaps
    placed = []; k = 0; tries = 0
    while k < P["far_n"] and tries < 5000:
        tries += 1; gx, gy, gr = rnd.choice(groups)
        x, y = gx + rnd.gauss(0, gr * 0.6), gy + rnd.gauss(0, gr * 0.6)
        if not (fx0 < x < fx1 and fy0 < y < fy1) or any((x - px) ** 2 + (y - py) ** 2 < 8.0 ** 2 for px, py in placed): continue
        z = ray_z(g, x, y)
        if z is None: continue
        ob = bpy.data.objects.new("ARR_PK_FAR_%02d" % k, far[k % 4]); coll.objects.link(ob)
        s = rnd.uniform(*P["far_H"]) / 18.0; ob.location = (x, y, z); ob.scale = (s, s, s); ob.rotation_euler.z = rnd.uniform(0, 6.283)
        ob["cp032_haze"] = VERSION; placed.append((x, y)); k += 1
    info["far_trees"] = k
    for j, (x, y, H) in enumerate(P["thorns"]):
        me, st = build_tree("ARR_TR2_thorn_%d" % j, "thorn", H, P["seed"] + 500 + j); info["trees"][me.name] = st
        ob = bpy.data.objects.new("ARR_PK_THORN_%02d" % j, me); coll.objects.link(ob)
        ob.location = (x, y, ray_z(g, x, y)); ob.rotation_euler.z = rnd.uniform(0, 6.283); ob["cp032_haze"] = VERSION
    # 2 meadow + track + tussocks
    gr = bpy.data.objects["ARR_GRASS"]; info["grass"] = [gr.data.materials[0].name, "GT_SydenhamMeadow1852b"]
    gr.data.materials[0] = meadow_mat2()
    t_ob, tcl, tlen = cart_track(coll); info["track_len_m"] = tlen
    tu_ob, ntu = tussocks(coll, rnd, tcl, cams); info["tussocks"] = ntu; info["tussock_faces"] = len(tu_ob.data.polygons)
    # 3 ruts
    r = bpy.data.objects["ARR_YD_RUTS"]; oldme = r.data; me, rinfo = ruts_v2(); r.data = me; info["ruts"] = rinfo
    if oldme.users == 0: bpy.data.meshes.remove(oldme)
print("CP032_HAZE_INFO " + json.dumps(info))
print("CP032_HAZE_IN_PLACE", in_place())
if not already or not a.live:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True)
    print("CP032_HAZE saved", out)
