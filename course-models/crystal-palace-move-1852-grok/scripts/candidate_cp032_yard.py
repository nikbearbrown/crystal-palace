"""CP032 arrival yard dressing (2026-11-02, Grok; CANDIDATE, no verdict; DEPARTURES MV18).

blender -b rounds/m02.blend -P scripts/candidate_cp032_yard.py -- [--out rounds/candidates/m02_cp032yard.blend]
blender -b ROUND.blend -P scripts/candidate_cp032_yard.py -- --live     # apply in place (only after a KEEP call)
Idempotent; always prints `CP032_YARD_IN_PLACE True|False`. Needs MV17 (GT_SydenhamClayYard on ARR_CLAY) in place.

Sydenham (Penge Place) 1852 receiving yard only; nothing of Hyde Park 1851 and nothing of the Sydenham building.
 1. Yard surface: GT_SydenhamClayYard's node tree rebuilt (same name, so MV17's check still holds): the soft 2 m
    blotches are damped; mid-scale trodden/compacted patchiness, Voronoi clods and foot-dents, and fine grit added.
 2. Dressing (new objects ARR_YD_*, collection ARR_SYDENHAM_1852, all ray-dropped onto ARR_CLAY/ARR_SPOIL):
    cart ruts (the parked wagon's own track, 5 ft gauge, plus two older, softer delivery tracks), shallow puddles in
    rut low points and the yard, ~380 scattered flints/ironstone/pebbles, deal walking boards and loose timbers, a
    navvy's wooden barrow, a shovel and a pick.
 3. ARR_SPOIL -> GT_SydenhamSpoil1852 (fresh-dug London Clay: weathered brown with blue-grey unweathered lumps,
    lumpier; same palette as the yard), plus a subdivision + low displacement so the heaps read as dug spoil.
 4. ARR_BARS_GUTTERS slots 0/2 -> GT_SashBarWeathered / GT_GutterTimberWeathered (weathered, travel-dirty white-lead
    paint on deal). DEP_BARS_GUTTERS (Hyde Park departure) keeps GT_SashBarBundle / GT_GutterTimber.
All colours are by-eye interpretive (grade D). No existing object's transform, mesh, camera, figure or exposure changes.
Live rounds/m02.blend is never written without --live.
"""
import os, sys, json, math, random, argparse
import bpy, bmesh
from mathutils import Vector, Matrix, Euler, noise

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser(); ap.add_argument("--out", default="rounds/candidates/m02_cp032yard.blend")
ap.add_argument("--live", action="store_true")
a = ap.parse_args(argv)
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if a.live:
    out = os.path.abspath(bpy.data.filepath)
else:
    out = os.path.join(here, a.out) if not os.path.isabs(a.out) else a.out
    assert os.path.abspath(out) != os.path.abspath(bpy.data.filepath), "refusing to overwrite the opened blend without --live"

VERSION = 1
PFX = "ARR_YD_"
COLL = "ARR_SYDENHAM_1852"
GAUGE = 1.524           # 5 ft wheel track, by eye for a heavy timber/iron wagon (D)
# ---------------------------------------------------------------- parameters (all by eye, grade D)
P = dict(
    seed=1852,
    tracks=[  # (name, centreline control points xy, groove depth scale, berm scale, fade-in m, fade-out m)
        ("wagon", [(-3.2, 479.80), (1.0, 480.05), (5.5, 480.9), (10.0, 482.6), (14.5, 485.4), (19.0, 488.6)], 1.0, 1.0, 0.3, 2.0),
        ("old_a", [(13.0, 482.6), (8.0, 485.0), (3.5, 487.85), (-0.5, 488.05), (-4.5, 488.0), (-8.0, 487.55), (-12.0, 487.0)], 0.75, 0.7, 2.0, 2.5),
        ("old_b", [(9.5, 494.4), (5.0, 493.4), (1.0, 492.9), (-3.0, 492.6), (-7.5, 492.9), (-12.5, 494.0)], 0.5, 0.45, 2.0, 2.0),
    ],
    stones=320, stone_box=(-9.0, 7.5, 483.4, 494.6),
    puddles=[  # (x, y, rx, ry, rot)
        "rut:old_a:+1:4.0:0.9", "rut:old_a:+1:11.5:0.6", "rut:old_a:-1:16.0:1.1", "rut:old_a:-1:20.5:0.5",
        "rut:old_b:-1:13.0:0.7", "rut:wagon:+1:6.0:0.8",
        (-3.4, 491.75, 0.45, 0.28, 0.3), (5.6, 491.2, 0.35, 0.22, -0.6),
    ],
    boards=[  # (x0, y0, x1, y1, width, thick, material)  deal boards, 9 x 3 in, 12 ft
        (-9.2, 486.2, -5.55, 486.75, 0.229, 0.076, "deal"), (-5.6, 486.75, -1.95, 487.15, 0.229, 0.076, "deal"),
        (-7.4, 491.75, -6.15, 491.45, 0.18, 0.05, "deal"),                   # offcut
        (5.0, 492.9, 7.4, 493.2, 0.30, 0.30, "baulk"),                         # 8 ft baulk, 12 in sq
        (5.1, 493.35, 7.3, 493.55, 0.229, 0.076, "deal"),
    ],
    barrow=(-0.75, 491.45, math.radians(160.0)),                             # x, y, heading of wheel end
    shovel_lean=True,
    pick=(-3.9, 486.15, math.radians(-20.0)),
)
C_DRY0, C_DRY1 = (0.066, 0.056, 0.043), (0.160, 0.133, 0.095)
C_WET = (0.050, 0.042, 0.032)
C_RUT = (0.034, 0.028, 0.021)


# ---------------------------------------------------------------- ground
GROUND = [bpy.data.objects[n] for n in ("ARR_CLAY", "ARR_SPOIL")]


def ground(x, y):
    best = None
    for o in GROUND:
        mi = o.matrix_world.inverted()
        org = mi @ Vector((x, y, 60.0)); d = (mi.to_3x3() @ Vector((0, 0, -1))).normalized()
        ok, loc, nrm, _ = o.ray_cast(org, d)
        if ok:
            z = (o.matrix_world @ loc).z
            if best is None or z > best: best = z
    return best


# ---------------------------------------------------------------- materials
def _p(m):
    return next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")


def _ramp(n, a0, c0, a1, c1):
    r = n.new("ShaderNodeValToRGB"); e = r.color_ramp.elements
    e[0].position, e[0].color = a0, (*c0, 1); e[1].position, e[1].color = a1, (*c1, 1); return r


def _noise(n, l, vec, scale, detail=4.0, rough=0.5):
    t = n.new("ShaderNodeTexNoise"); t.inputs["Scale"].default_value = scale; t.inputs["Detail"].default_value = detail
    t.inputs["Roughness"].default_value = rough; l.new(vec, t.inputs["Vector"]); return t


def _mix(n, l, fac, c_a, c_b):
    m = n.new("ShaderNodeMix"); m.data_type = "RGBA"
    for s, v in ((fac, 0), (c_a, 6), (c_b, 7)):
        if isinstance(s, tuple): m.inputs[v].default_value = (*s, 1) if v else s
        else: l.new(s, m.inputs[v])
    return m


def _math(n, l, op, a_, b_):
    m = n.new("ShaderNodeMath"); m.operation = op
    for i, s in enumerate((a_, b_)):
        if isinstance(s, (int, float)): m.inputs[i].default_value = s
        else: l.new(s, m.inputs[i])
    return m


def yard_rebuild(m):
    """GT_SydenhamClayYard v2: trodden London Clay. Soft blotches damped; patch / clod / grit scales added."""
    nt = m.node_tree; nt.nodes.clear(); n = nt.nodes; l = nt.links
    o = n.new("ShaderNodeOutputMaterial"); b = n.new("ShaderNodeBsdfPrincipled"); l.new(b.outputs[0], o.inputs[0])
    tc = n.new("ShaderNodeTexCoord"); v = tc.outputs["Object"]
    big = _noise(n, l, v, 0.55, 3.0)                                     # wet low patches (few, broad)
    wet = _ramp(n, 0.40, (1, 1, 1), 0.47, (0, 0, 0))                     # 1 = wet
    l.new(big.outputs["Fac"], wet.inputs[0])
    mid = _noise(n, l, v, 2.6, 5.0, 0.62)                                # trodden / compacted patchiness ~0.4 m
    rm = _ramp(n, 0.36, C_DRY0, 0.64, C_DRY1); l.new(mid.outputs["Fac"], rm.inputs[0])
    vor = n.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 11.0; vor.inputs["Randomness"].default_value = 1.0
    l.new(v, vor.inputs["Vector"])                                       # clods / boot dents
    vr = _ramp(n, 0.0, (0, 0, 0), 0.55, (1, 1, 1)); l.new(vor.outputs["Distance"], vr.inputs[0])
    grit = _noise(n, l, v, 85.0, 2.0, 0.5)
    gr = _ramp(n, 0.3, (0.82, 0.82, 0.82), 0.7, (1.12, 1.10, 1.06)); l.new(grit.outputs["Fac"], gr.inputs[0])
    c1 = n.new("ShaderNodeMix"); c1.data_type = "RGBA"; c1.blend_type = "MULTIPLY"; c1.inputs[0].default_value = 1.0
    l.new(rm.outputs["Color"], c1.inputs[6]); l.new(gr.outputs["Color"], c1.inputs[7])
    dent = _ramp(n, 0.0, (0.80, 0.80, 0.80), 0.35, (1.0, 1.0, 1.0)); l.new(vor.outputs["Distance"], dent.inputs[0])
    c2 = n.new("ShaderNodeMix"); c2.data_type = "RGBA"; c2.blend_type = "MULTIPLY"; c2.inputs[0].default_value = 1.0
    l.new(c1.outputs[2], c2.inputs[6]); l.new(dent.outputs["Color"], c2.inputs[7])
    wf = _math(n, l, "MULTIPLY", wet.outputs["Color"], 0.85)
    c3 = n.new("ShaderNodeMix"); c3.data_type = "RGBA"; l.new(wf.outputs[0], c3.inputs[0])
    l.new(c2.outputs[2], c3.inputs[6]); c3.inputs[7].default_value = (*C_WET, 1)
    l.new(c3.outputs[2], b.inputs["Base Color"])
    rr = n.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = 0.93; rr.inputs["To Max"].default_value = 0.55
    l.new(wf.outputs[0], rr.inputs["Value"]); l.new(rr.outputs["Result"], b.inputs["Roughness"])
    # height: clods (voronoi, 1.5 cm) + grit (2 mm) + mid undulation
    h1 = _math(n, l, "MULTIPLY", vr.outputs["Color"], 0.6)
    h2 = _math(n, l, "MULTIPLY", grit.outputs["Fac"], 0.25)
    h3 = _math(n, l, "ADD", h1.outputs[0], h2.outputs[0])
    h4 = _math(n, l, "MULTIPLY", mid.outputs["Fac"], 0.3)
    h5 = _math(n, l, "ADD", h3.outputs[0], h4.outputs[0])
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.55; bp.inputs["Distance"].default_value = 0.025
    l.new(h5.outputs[0], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.3
    b.inputs["Base Color"].default_value = (*[(x + y) / 2 for x, y in zip(C_DRY0, C_DRY1)], 1)
    m.diffuse_color = b.inputs["Base Color"].default_value
    m["cp032_yard_v"] = VERSION
    return m


def spoil_mat():
    m = bpy.data.materials.get("GT_SydenhamSpoil1852")
    if m: return m
    m = bpy.data.materials.new("GT_SydenhamSpoil1852"); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    b = _p(m); tc = n.new("ShaderNodeTexCoord"); v = tc.outputs["Object"]
    vor = n.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 3.2; l.new(v, vor.inputs["Vector"])
    lump = _ramp(n, 0.55, (0, 0, 0), 0.75, (1, 1, 1)); l.new(vor.outputs["Color"], lump.inputs[0])   # blue-grey lumps
    nz = _noise(n, l, v, 1.8, 5.0, 0.6)
    brown = _ramp(n, 0.38, (0.150, 0.112, 0.072), 0.66, (0.235, 0.178, 0.108)); l.new(nz.outputs["Fac"], brown.inputs[0])
    lf = _math(n, l, "MULTIPLY", lump.outputs["Color"], 0.7)
    mx = n.new("ShaderNodeMix"); mx.data_type = "RGBA"; l.new(lf.outputs[0], mx.inputs[0])
    l.new(brown.outputs["Color"], mx.inputs[6]); mx.inputs[7].default_value = (0.120, 0.118, 0.110, 1)
    grit = _noise(n, l, v, 60.0, 2.0)
    gr = _ramp(n, 0.3, (0.8, 0.8, 0.8), 0.7, (1.12, 1.1, 1.05)); l.new(grit.outputs["Fac"], gr.inputs[0])
    mm = n.new("ShaderNodeMix"); mm.data_type = "RGBA"; mm.blend_type = "MULTIPLY"; mm.inputs[0].default_value = 1.0
    l.new(mx.outputs[2], mm.inputs[6]); l.new(gr.outputs["Color"], mm.inputs[7]); l.new(mm.outputs[2], b.inputs["Base Color"])
    vor2 = n.new("ShaderNodeTexVoronoi"); vor2.inputs["Scale"].default_value = 7.0; l.new(v, vor2.inputs["Vector"])
    h = _math(n, l, "ADD", vor2.outputs["Distance"], grit.outputs["Fac"])
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.7; bp.inputs["Distance"].default_value = 0.05
    l.new(h.outputs[0], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.9
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.3
    m.diffuse_color = (0.19, 0.145, 0.09, 1); return m


def flat_mat(name, c0, c1, scale=(1.0, 1.0, 1.0), nscale=6.0, rough=0.85, streak=True):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    b = _p(m); tc = n.new("ShaderNodeTexCoord")
    mp = n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = scale; l.new(tc.outputs["Object"], mp.inputs["Vector"])
    nz = _noise(n, l, mp.outputs["Vector"], nscale, 6.0, 0.6)
    r = _ramp(n, 0.3, c0, 0.7, c1); l.new(nz.outputs["Fac"], r.inputs[0]); l.new(r.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.35
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.2
    l.new(nz.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (*[(x + y) / 2 for x, y in zip(c0, c1)], 1); return m


def bars_mat():   # weathered white-lead paint on deal, a year out of doors + transport grime
    m = bpy.data.materials.get("GT_SashBarWeathered")
    if m: return m
    m = bpy.data.materials.new("GT_SashBarWeathered"); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    b = _p(m); tc = n.new("ShaderNodeTexCoord"); v = tc.outputs["Object"]
    st = n.new("ShaderNodeMapping"); st.inputs["Scale"].default_value = (0.6, 18.0, 18.0); l.new(v, st.inputs["Vector"])
    s = _noise(n, l, st.outputs["Vector"], 3.0, 4.0)               # long streaks (bars run along x)
    r = _ramp(n, 0.3, (0.190, 0.178, 0.152), 0.75, (0.275, 0.258, 0.222)); l.new(s.outputs["Fac"], r.inputs[0])
    sep = n.new("ShaderNodeSeparateXYZ"); l.new(v, sep.inputs[0])   # grime toward the bottom of the stack
    g = n.new("ShaderNodeMapRange"); g.inputs["From Min"].default_value = -0.2; g.inputs["From Max"].default_value = 0.35
    g.inputs["To Min"].default_value = 0.62; g.inputs["To Max"].default_value = 1.0
    l.new(sep.outputs["Z"], g.inputs["Value"])
    mm = n.new("ShaderNodeMix"); mm.data_type = "RGBA"; mm.blend_type = "MULTIPLY"; mm.inputs[0].default_value = 1.0
    l.new(r.outputs["Color"], mm.inputs[6]); l.new(g.outputs["Result"], mm.inputs[7])
    cmb = n.new("ShaderNodeCombineColor"); l.new(g.outputs["Result"], cmb.inputs[0]); l.new(g.outputs["Result"], cmb.inputs[1]); l.new(g.outputs["Result"], cmb.inputs[2])
    l.new(cmb.outputs[0], mm.inputs[7])
    sep2 = n.new("ShaderNodeSeparateXYZ"); l.new(v, sep2.inputs[0])
    cy = n.new("ShaderNodeCombineXYZ"); l.new(sep2.outputs["Y"], cy.inputs["X"]); l.new(sep2.outputs["Z"], cy.inputs["Y"])
    br = n.new("ShaderNodeTexBrick"); br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = 0.038; br.inputs["Row Height"].default_value = 0.026
    br.inputs["Mortar Size"].default_value = 0.004; br.inputs["Mortar Smooth"].default_value = 0.3
    br.offset = 0.0; br.squash = 1.0
    br.inputs["Color1"].default_value = (1, 1, 1, 1); br.inputs["Color2"].default_value = (0.86, 0.86, 0.86, 1)
    br.inputs["Mortar"].default_value = (0.35, 0.33, 0.30, 1); l.new(cy.outputs[0], br.inputs["Vector"])
    m2 = n.new("ShaderNodeMix"); m2.data_type = "RGBA"; m2.blend_type = "MULTIPLY"; m2.inputs[0].default_value = 1.0
    l.new(mm.outputs[2], m2.inputs[6]); l.new(br.outputs["Color"], m2.inputs[7])
    bpb = n.new("ShaderNodeBump"); bpb.inputs["Strength"].default_value = 0.5; bpb.inputs["Distance"].default_value = 0.004
    l.new(br.outputs["Fac"], bpb.inputs["Height"]); l.new(bpb.outputs["Normal"], b.inputs["Normal"])
    l.new(m2.outputs[2], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.88
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.3
    m.diffuse_color = (0.3, 0.285, 0.25, 1); return m


def water_mat():
    m = bpy.data.materials.get("GT_PuddleWater1852")
    if m: return m
    m = bpy.data.materials.new("GT_PuddleWater1852"); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    b = _p(m); tc = n.new("ShaderNodeTexCoord"); at = n.new("ShaderNodeAttribute"); at.attribute_name = "pd"
    nz = _noise(n, l, tc.outputs["Object"], 9.0, 4.0)
    e = _math(n, l, "ADD", at.outputs["Fac"], nz.outputs["Fac"])          # ragged shoreline
    sm = n.new("ShaderNodeMapRange"); sm.interpolation_type = "SMOOTHSTEP"
    sm.inputs["From Min"].default_value = 0.75; sm.inputs["From Max"].default_value = 1.05; l.new(e.outputs[0], sm.inputs["Value"])
    rr = n.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = 0.9; rr.inputs["To Max"].default_value = 0.07
    l.new(sm.outputs["Result"], rr.inputs["Value"]); l.new(rr.outputs["Result"], b.inputs["Roughness"])
    mx = n.new("ShaderNodeMix"); mx.data_type = "RGBA"; l.new(sm.outputs["Result"], mx.inputs[0])
    mx.inputs[6].default_value = (*C_WET, 1); mx.inputs[7].default_value = (0.040, 0.034, 0.026, 1)
    l.new(mx.outputs[2], b.inputs["Base Color"])
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.35
    m.diffuse_color = (0.045, 0.04, 0.03, 1); return m


def rut_mat():
    m = bpy.data.materials.get("GT_CartRutClay")
    if m: return m
    m = bpy.data.materials.new("GT_CartRutClay"); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    b = _p(m); at = n.new("ShaderNodeAttribute"); at.attribute_name = "groove"
    tc = n.new("ShaderNodeTexCoord"); nz = _noise(n, l, tc.outputs["Object"], 7.0, 5.0, 0.6)
    berm = _ramp(n, 0.35, (0.118, 0.098, 0.072), 0.7, (0.185, 0.152, 0.108)); l.new(nz.outputs["Fac"], berm.inputs[0])
    mx = n.new("ShaderNodeMix"); mx.data_type = "RGBA"; l.new(at.outputs["Fac"], mx.inputs[0])
    l.new(berm.outputs["Color"], mx.inputs[6]); mx.inputs[7].default_value = (*C_RUT, 1)
    l.new(mx.outputs[2], b.inputs["Base Color"])
    rr = n.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = 0.95; rr.inputs["To Max"].default_value = 0.82
    l.new(at.outputs["Fac"], rr.inputs["Value"]); l.new(rr.outputs["Result"], b.inputs["Roughness"])
    g = _noise(n, l, tc.outputs["Object"], 40.0, 3.0)
    vo = n.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 14.0; l.new(tc.outputs["Object"], vo.inputs["Vector"])
    hh = _math(n, l, "ADD", vo.outputs["Distance"], g.outputs["Fac"])
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.6; bp.inputs["Distance"].default_value = 0.02
    l.new(hh.outputs[0], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.3
    out = [x for x in n if x.type == "OUTPUT_MATERIAL"][0]
    aa = n.new("ShaderNodeAttribute"); aa.attribute_name = "ralpha"
    tr = n.new("ShaderNodeBsdfTransparent"); ms = n.new("ShaderNodeMixShader")
    l.new(aa.outputs["Fac"], ms.inputs[0]); l.new(tr.outputs[0], ms.inputs[1]); l.new(b.outputs[0], ms.inputs[2])
    l.new(ms.outputs[0], out.inputs["Surface"])
    m.diffuse_color = (*C_RUT, 1); return m


# ---------------------------------------------------------------- helpers
def new_obj(name, bm, mats, coll):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    ob["cp032_yard"] = VERSION; return ob


def catmull(pts, step):
    P_ = [Vector((x, y)) for x, y in pts]; P_ = [P_[0] * 2 - P_[1]] + P_ + [P_[-1] * 2 - P_[-2]]
    out = []
    for i in range(1, len(P_) - 2):
        p0, p1, p2, p3 = P_[i - 1:i + 3]; nseg = max(2, int((p2 - p1).length / step))
        for k in range(nseg):
            t = k / nseg; t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(P_[-2]); return out


TRACKS = {}


def track_point(name, side, dist):
    cl, L = TRACKS[name]
    i = min(range(len(L)), key=lambda k: abs(L[k] - dist))
    tng = (cl[min(i + 1, len(cl) - 1)] - cl[max(i - 1, 0)]).normalized(); nrm = Vector((-tng.y, tng.x))
    p = cl[i] + nrm * (side * GAUGE / 2)
    return p, math.atan2(tng.y, tng.x)


def ruts(coll, rng):
    PROF_S = [-0.22, -0.15, -0.10, -0.05, 0.0, 0.05, 0.10, 0.15, 0.22]
    PROF_H = [0.004, 0.022, 0.017, 0.013, 0.012, 0.013, 0.017, 0.022, 0.004]   # ribbon sits clear of clay quad-triangulation error; groove floor lower than berms
    PROF_G = [0.0, 0.5, 0.95, 1.0, 1.0, 1.0, 0.95, 0.5, 0.0]
    PROF_A = [0.0, 0.7, 1.0, 1.0, 1.0, 1.0, 1.0, 0.7, 0.0]   # outer edge fades into the clay (no cut line)
    bm = bmesh.new(); lay = bm.verts.layers.float.new("groove"); lay_a = bm.verts.layers.float.new("ralpha"); info = []
    for name, ctrl, gsc, bsc, fin, fout in P["tracks"]:
        cl = catmull(ctrl, 0.06); L = [0.0]
        for i in range(1, len(cl)): L.append(L[-1] + (cl[i] - cl[i - 1]).length)
        tot = L[-1]; TRACKS[name] = (cl, L)
        for side in (-1, 1):
            rows = []
            for i, c in enumerate(cl):
                tng = (cl[min(i + 1, len(cl) - 1)] - cl[max(i - 1, 0)]).normalized(); nrm = Vector((-tng.y, tng.x))
                w = min(1.0, L[i] / fin if fin else 1.0, (tot - L[i]) / fout if fout else 1.0)
                wob = 0.035 * noise.noise(Vector((L[i] * 0.7, side * 3.1, 0.5))) + 0.06 * noise.noise(Vector((L[i] * 0.12, 7.7, 0.5)))
                cc = c + nrm * (side * GAUGE / 2 + wob)
                row = []
                for s, h, gv, av in zip(PROF_S, PROF_H, PROF_G, PROF_A):
                    sc_ = bsc if h > 0.006 else gsc
                    jitter = 1.0 + 0.6 * noise.noise(Vector((L[i] * 2.3, s * 9.0, side)))
                    p = cc + nrm * s
                    z = ground(p.x, p.y)
                    if z is None: row.append(None); continue
                    v = bm.verts.new((p.x, p.y, z + 0.002 + h * sc_ * w * max(0.3, jitter)))
                    v[lay_a] = av * min(1.0, 0.2 + w)
                    v[lay] = gv * w * min(1.0, max(0.25, 0.75 + 0.6 * noise.noise(Vector((L[i] * 0.9, side * 5.0, 2.0))))); row.append(v)
                rows.append(row)
            for r0, r1 in zip(rows, rows[1:]):
                for j in range(len(PROF_S) - 1):
                    q = [r0[j], r0[j + 1], r1[j + 1], r1[j]]
                    if all(q): bm.faces.new(q)
        info.append((name, round(tot, 2)))
    bm.normal_update()
    for f in bm.faces:
        if f.normal.z < 0: f.normal_flip()
    ob = new_obj(PFX + "RUTS", bm, [rut_mat()], coll)
    ob.visible_shadow = True; return ob, info


def puddles(coll, rng):
    bm = bmesh.new(); lay = bm.verts.layers.float.new("pd")
    for i, spec in enumerate(P["puddles"]):
        if isinstance(spec, str):                       # puddle lying in a rut groove
            _, tn, sd, dist, ln = spec.split(":"); p, rot = track_point(tn, int(sd), float(dist))
            x, y, rx, ry = p.x, p.y, float(ln) / 2, 0.075
        else:
            x, y, rx, ry, rot = spec
        NR, NA = 6, 28; ctr = None; rings = []
        for r in range(NR + 1):
            ring = []
            for k in range(NA):
                th = 2 * math.pi * k / NA
                f = r / NR * (1.0 + 0.28 * noise.noise(Vector((math.cos(th) * 1.7, math.sin(th) * 1.7, i * 3.3))))
                lx, ly = rx * f * math.cos(th), ry * f * math.sin(th)
                px = x + lx * math.cos(rot) - ly * math.sin(rot); py = y + lx * math.sin(rot) + ly * math.cos(rot)
                z = ground(px, py)
                vv = bm.verts.new((px, py, (z if z is not None else 0) + 0.007)); vv[lay] = 1.0 - (r / NR) ** 1.6
                ring.append(vv)
                if r == 0: break
            rings.append(ring)
        c = rings[0][0]
        for k in range(NA): bm.faces.new([c, rings[1][k], rings[1][(k + 1) % NA]])
        for r in range(1, NR):
            for k in range(NA):
                bm.faces.new([rings[r][k], rings[r + 1][k], rings[r + 1][(k + 1) % NA], rings[r][(k + 1) % NA]])
    bm.normal_update()
    for f in bm.faces:
        if f.normal.z < 0: f.normal_flip()
    return new_obj(PFX + "PUDDLES", bm, [water_mat()], coll)


def obstacles():
    obs = []
    skip = ("ARR_CLAY", "ARR_SPOIL", "ARR_GRASS", "ARR_OAK", "ARR_PEGS", "ARR_HUT", PFX)
    for o in bpy.data.objects:
        if not o.name.startswith("ARR_") or o.name.startswith(skip) or o.type != "MESH": continue
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        obs.append((o.name, min(v.x for v in bb), max(v.x for v in bb), min(v.y for v in bb), max(v.y for v in bb)))
    return obs


def clear_of(x, y, obs, m):
    return all(not (x0 - m < x < x1 + m and y0 - m < y < y1 + m) for _, x0, x1, y0, y1 in obs)


def stones(coll, rng, obs):
    bm = bmesh.new(); x0, x1, y0, y1 = P["stone_box"]; placed = 0; tries = 0
    while placed < P["stones"] and tries < 20000:
        tries += 1
        if rng.random() < 0.45:                         # kicked up along the rut berms
            tn = rng.choice(list(TRACKS)); cl, L = TRACKS[tn]
            p, _ = track_point(tn, rng.choice((-1, 1)), rng.uniform(0, L[-1]))
            x, y = p.x + rng.gauss(0, 0.22), p.y + rng.gauss(0, 0.22)
            if not (x0 < x < x1 and y0 < y < y1): continue
        else:
            x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if not clear_of(x, y, obs, 0.12): continue
        z = ground(x, y)
        if z is None: continue
        sz = rng.choice([0.018] * 7 + [0.03] * 5 + [0.045] * 3 + [0.075]) * rng.uniform(0.7, 1.3)
        kind = rng.choices([0, 1, 2, 3], [0.45, 0.25, 0.22, 0.08])[0]   # flint, ironstone, pebble, clay clod
        g = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0)
        vs = g["verts"]; seed = Vector((rng.uniform(0, 99), rng.uniform(0, 99), 0))
        sx, sy, szz = sz * rng.uniform(0.8, 1.4), sz * rng.uniform(0.7, 1.1), sz * rng.uniform(0.45, 0.8)
        R = Euler((rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), rng.uniform(0, 6.28))).to_matrix()
        for v in vs:
            j = 1.0 + 0.28 * noise.noise(v.co * 1.3 + seed)
            co = Vector((v.co.x * sx, v.co.y * sy, v.co.z * szz)) * j
            v.co = R @ co + Vector((x, y, z + szz * 0.25))
        for f in {f for v in vs for f in v.link_faces}: f.material_index = kind
        placed += 1
    mats = [flat_mat("GT_Flint1852", (0.075, 0.072, 0.068), (0.150, 0.140, 0.125), nscale=30),
            flat_mat("GT_Ironstone1852", (0.110, 0.072, 0.042), (0.190, 0.125, 0.070), nscale=25),
            flat_mat("GT_Pebble1852", (0.120, 0.105, 0.085), (0.215, 0.190, 0.150), nscale=20, rough=0.7),
            bpy.data.materials["GT_SydenhamSpoil1852"]]
    ob = new_obj(PFX + "STONES", bm, mats, coll)
    for p in ob.data.polygons: p.use_smooth = False
    return ob, placed


def box(bm, L, W, H, M, mi=0):
    g = bmesh.ops.create_cube(bm, size=1.0)
    for v in g["verts"]: v.co = M @ Vector((v.co.x * L, v.co.y * W, v.co.z * H))
    for f in {f for v in g["verts"] for f in v.link_faces}: f.material_index = mi
    return g


def cyl(bm, r, depth, M, seg=10, mi=0):
    g = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=depth)
    for v in g["verts"]: v.co = M @ v.co
    for f in {f for v in g["verts"] for f in v.link_faces}: f.material_index = mi
    return g


def boards(coll, rng):
    bm = bmesh.new(); res = []
    for (xa, ya, xb, yb, w, t, kind) in P["boards"]:
        A, B = Vector((xa, ya)), Vector((xb, yb)); L = (B - A).length; d = (B - A).normalized(); nrm = Vector((-d.y, d.x))
        zs = [ground(*(A + (B - A) * (k / 8) + nrm * s)) for k in range(9) for s in (-w / 2, w / 2)]
        za, zb = ground(*A), ground(*B)
        # rigid board resting on the highest points; sinks 1 cm (soft clay)
        top_line = max(z - (za + (zb - za) * (k / 8)) for k, z in zip([k for k in range(9) for _ in (0, 1)], zs))
        zc = (za + zb) / 2 + top_line + t / 2 - 0.012
        yaw = math.atan2(d.y, d.x); pitch = -math.atan2(zb - za, L)
        roll = rng.uniform(-0.02, 0.02)
        M = Matrix.Translation(Vector(((xa + xb) / 2, (ya + yb) / 2, zc))) @ Euler((roll, pitch, yaw), "XYZ").to_matrix().to_4x4()
        # Euler XYZ applies yaw last; pitch about local y
        M = Matrix.Translation(Vector(((xa + xb) / 2, (ya + yb) / 2, zc))) @ Matrix.Rotation(yaw, 4, "Z") @ Matrix.Rotation(pitch, 4, "Y") @ Matrix.Rotation(roll, 4, "X")
        box(bm, L, w, t, M, 0 if kind == "deal" else 1)
        res.append((kind, round(L, 2)))
    mats = [flat_mat("GT_DealMuddy1852", (0.105, 0.085, 0.060), (0.190, 0.155, 0.110), scale=(0.25, 6.0, 6.0), nscale=4),
            flat_mat("GT_BaulkWeathered1852", (0.120, 0.100, 0.078), (0.205, 0.175, 0.135), scale=(0.3, 5.0, 5.0), nscale=4)]
    ob = new_obj(PFX + "BOARDS", bm, mats, coll)
    for p in ob.data.polygons: p.use_smooth = False
    return ob, res


def barrow(coll):
    """Navvy's wooden barrow (period type: flat tray with flared sides, two shafts, iron-tyred wooden wheel, two
    legs). Local +x = wheel end. Proportions by eye (D)."""
    x, y, hd = P["barrow"]; bm = bmesh.new()
    WR = 0.21; tray_z = 0.36
    # shafts: from axle (x=+0.55) back to grips (x=-1.05), rising from wheel hub to 0.55 m at grips when tipped up?
    # parked: legs on the ground, shafts slope down to the wheel hub.
    for s in (-1, 1):
        a = Vector((0.58, s * 0.16, WR)); b = Vector((-1.05, s * 0.30, 0.44)); d = b - a
        M = Matrix.Translation((a + b) / 2) @ d.to_track_quat("X", "Z").to_matrix().to_4x4()
        box(bm, d.length, 0.045, 0.055, M, 0)
        box(bm, 0.05, 0.05, 0.34, Matrix.Translation(Vector((-0.42, s * 0.25, 0.17))), 0)   # leg
    # tray: bottom + sides (flared)
    box(bm, 0.66, 0.46, 0.025, Matrix.Translation(Vector((-0.05, 0, tray_z))), 0)
    for s in (-1, 1):
        M = Matrix.Translation(Vector((-0.05, s * 0.29, tray_z + 0.13))) @ Matrix.Rotation(s * math.radians(-22), 4, "X")
        box(bm, 0.74, 0.022, 0.29, M, 0)
    Mf = Matrix.Translation(Vector((0.33, 0, tray_z + 0.15))) @ Matrix.Rotation(math.radians(30), 4, "Y")
    box(bm, 0.022, 0.62, 0.30, Mf, 0)                                                         # front board, raked
    Mb = Matrix.Translation(Vector((-0.40, 0, tray_z + 0.09))) @ Matrix.Rotation(math.radians(-12), 4, "Y")
    box(bm, 0.022, 0.52, 0.18, Mb, 0)
    # wheel: wooden disc, iron tyre, axle
    Mw = Matrix.Translation(Vector((0.62, 0, WR))) @ Matrix.Rotation(math.radians(90), 4, "X")
    cyl(bm, WR - 0.012, 0.055, Mw, 20, 0); cyl(bm, WR, 0.045, Mw, 20, 1); cyl(bm, 0.03, 0.40, Mw, 8, 1)
    # a little spoil in the tray
    g = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
    for v in g["verts"]:
        c = v.co.copy(); v.co = Vector((c.x * 0.27, c.y * 0.19, max(c.z, -0.2) * 0.09)) * (1 + 0.15 * noise.noise(c * 2.0)) + Vector((-0.04, 0, tray_z + 0.06))
    for f in {f for v in g["verts"] for f in v.link_faces}: f.material_index = 2
    mats = [flat_mat("GT_BarrowElm1852", (0.105, 0.085, 0.062), (0.185, 0.150, 0.108), scale=(0.3, 5, 5), nscale=5),
            flat_mat("GT_WroughtIron1852", (0.035, 0.034, 0.033), (0.065, 0.060, 0.056), nscale=20, rough=0.6),
            bpy.data.materials["GT_SydenhamSpoil1852"]]
    ob = new_obj(PFX + "BARROW", bm, mats, coll)
    for p in ob.data.polygons: p.use_smooth = False
    # place: wheel and both legs on the ground
    c, s_ = math.cos(hd), math.sin(hd)
    def w(lx, ly): return Vector((x + lx * c - ly * s_, y + lx * s_ + ly * c))
    zw = ground(*w(0.62, 0)); zl = max(ground(*w(-0.42, -0.25)), ground(*w(-0.42, 0.25)))
    pitch = math.atan2(zw - zl, 1.04)
    ob.matrix_world = Matrix.Translation(Vector((x, y, zl + 0.42 * math.tan(pitch) - 0.01))) @ Matrix.Rotation(hd, 4, "Z") @ Matrix.Rotation(-pitch, 4, "Y")
    return ob


def tools(coll, barrow_ob):
    bm = bmesh.new()
    # shovel: long ash handle, iron blade; leaning in the barrow
    if P["shovel_lean"]:
        M0 = barrow_ob.matrix_world
        base = M0 @ Vector((-0.10, 0.05, 0.40)); top = M0 @ Vector((-0.95, -0.10, 1.10))
        d = top - base; q = d.to_track_quat("Z", "Y").to_matrix().to_4x4()
        cyl(bm, 0.017, d.length, Matrix.Translation((base + top) / 2) @ q, 8, 0)
        Mb = Matrix.Translation(base - d.normalized() * 0.13) @ q
        box(bm, 0.24, 0.006, 0.28, Mb, 1)
    # pick: lying on the clay beside the walking boards
    px, py, ph = P["pick"]; z = ground(px, py)
    Mh = Matrix.Translation(Vector((px, py, z + 0.02))) @ Matrix.Rotation(ph, 4, "Z") @ Matrix.Rotation(math.radians(90), 4, "Y")
    cyl(bm, 0.02, 0.90, Mh, 8, 0)
    hx = Vector((px, py, z)) + Matrix.Rotation(ph, 3, "Z") @ Vector((0.45, 0, 0.035))
    Mp = Matrix.Translation(hx) @ Matrix.Rotation(ph + math.pi / 2, 4, "Z")
    box(bm, 0.60, 0.035, 0.04, Mp, 1)
    mats = [flat_mat("GT_AshHandle1852", (0.18, 0.14, 0.095), (0.27, 0.21, 0.14), scale=(1, 1, 0.2), nscale=6),
            bpy.data.materials["GT_WroughtIron1852"]]
    ob = new_obj(PFX + "TOOLS", bm, mats, coll)
    for p in ob.data.polygons: p.use_smooth = False
    return ob


def spoil_shape():
    o = bpy.data.objects["ARR_SPOIL"]
    if "CP032Y_Subsurf" not in o.modifiers:
        m = o.modifiers.new("CP032Y_Subsurf", "SUBSURF"); m.levels = m.render_levels = 3
    if "CP032Y_Displace" not in o.modifiers:
        t = bpy.data.textures.get("CP032Y_SpoilLumps") or bpy.data.textures.new("CP032Y_SpoilLumps", "CLOUDS")
        t.noise_scale = 0.8; t.noise_depth = 3
        m = o.modifiers.new("CP032Y_Displace", "DISPLACE"); m.texture = t; m.strength = 0.22; m.mid_level = 0.5
        m.texture_coords = "GLOBAL"


# ---------------------------------------------------------------- apply
def in_place():
    cl = bpy.data.objects.get("ARR_CLAY"); sp = bpy.data.objects.get("ARR_SPOIL"); bg = bpy.data.objects.get("ARR_BARS_GUTTERS")
    if not (cl and sp and bg): return False
    ym = cl.data.materials[0]
    return (ym is not None and ym.name == "GT_SydenhamClayYard" and ym.get("cp032_yard_v") == VERSION
            and sp.data.materials[0].name == "GT_SydenhamSpoil1852"
            and bg.data.materials[0].name == "GT_SashBarWeathered" and bg.data.materials[2].name == "GT_GutterTimberWeathered"
            and all(bpy.data.objects.get(PFX + n) for n in ("RUTS", "PUDDLES", "STONES", "BOARDS", "BARROW", "TOOLS")))


already = in_place(); info = {}
if already:
    print("CP032_YARD already applied; nothing changed")
else:
    cl = bpy.data.objects["ARR_CLAY"]
    assert cl.data.materials[0].name == "GT_SydenhamClayYard", "needs MV17 (candidate_cp032_foreground.py) first"
    assert not any(o.name.startswith(PFX) for o in bpy.data.objects), "partial ARR_YD_ state; rebuild from a clean round"
    rng = random.Random(P["seed"]); coll = bpy.data.collections[COLL]
    yard_rebuild(cl.data.materials[0])
    spm = spoil_mat(); sp = bpy.data.objects["ARR_SPOIL"]; old_sp = sp.data.materials[0].name; sp.data.materials[0] = spm
    obs = obstacles()
    r_ob, rinfo = ruts(coll, rng)
    p_ob = puddles(coll, rng)
    s_ob, ns = stones(coll, rng, obs)
    b_ob, binfo = boards(coll, rng)
    w_ob = barrow(coll)
    t_ob = tools(coll, w_ob)
    spoil_shape()
    bg = bpy.data.objects["ARR_BARS_GUTTERS"]; old_bg = [m.name for m in bg.data.materials]
    bg.data.materials[0] = bars_mat()
    bg.data.materials[2] = flat_mat("GT_GutterTimberWeathered", (0.135, 0.122, 0.100), (0.215, 0.195, 0.165), scale=(0.5, 8, 8), nscale=4)
    info = {"tracks": rinfo, "stones": ns, "boards": binfo, "spoil_material": [old_sp, spm.name],
            "bars_materials": [old_bg, [m.name for m in bg.data.materials]],
            "new_objects": sorted(o.name for o in bpy.data.objects if o.name.startswith(PFX))}
print("CP032_YARD_INFO " + json.dumps(info))
print("CP032_YARD_IN_PLACE", in_place())
if not already or not a.live:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True)
    print("CP032_YARD saved", out)
