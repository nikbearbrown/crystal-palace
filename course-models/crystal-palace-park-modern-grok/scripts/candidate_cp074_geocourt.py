"""CP074 'The oldest-looking survivors' - PARK-NOW (present day) polish, CANDIDATE 2026-11-16 (Grok; no verdict).
blender -b rounds/parknow-r01.blend -P scripts/candidate_cp074_geocourt.py -- [--out rounds/candidates/parknow-r01_cp074geocourt.blend]
Never overwrites the opened (live) blend. PARK-NOW (present day) only.

Why r01: the live hero renders/r01_parknow_CAM_CP074_dinosaurs_35mm.png (look v1.1 keep-better, 2026-10-27) was
rendered from rounds/parknow-r01.blend (PNG 'File' metadata), and survey look/apply_render.py on r01 (CP074, present,
exterior_afternoon, 1280x720, 24 spp, --no-people) reproduces it at max pixel diff 0 (checked 2026-11-16). parknow-r02
(the manifest/COVERAGE blend) does NOT reproduce it (dud-fix v4 left a grey box in front of the lens there).

Defect (live hero, at a glance): the 'present-day' Geological Court is the appended 1854 state (DN54_*): a bare
billiard-table young-turf island, 1854 young lollipop planting casting big blob shadows, and the Hawkins sculptures
reading as cream/white blobs on open lawn - nothing of the conserved, painted, gravel-and-rock setting a visitor sees.

Candidate (DEPARTURES D-PM-50..D-PM-57), dated: present day, after the 2023-26 Geological Court conservation
(HTA Design lead consultant, appointed 2023 by Bromley; SSHC Conservators; Friends of Crystal Palace Dinosaurs):
 1. Present-day paint on the Secondary Island sculptures (D-PM-51): 'Paint analysis identified original 1850s colours
    ... 50 different colours, ... a striking display allowing visitors to recognise and navigate between species from
    afar' (HTA). Distinct per-species schemes, darker back / paler belly, lichen + weathering. Hues are I (no colour chart).
 2. Gravel swathes around the sculptures (D-PM-52): 'New gravel formations are introduced around the sculptures ...
    the Purbeck and Wealden formations - the specific geological contexts associated with the Iguanodon and
    Hylaeosaurus' (HTA); buff Wealden gravel round Iguanodons + Hylaeosaurus, pale oolite gravel round Megalosaurus.
 3. Rock blocks (D-PM-53): 'The sandstone blocks around the Iguanodon and Hylaeosaurus represent the geology of Sussex
    (Wealden Sandstones)'; 'The Megalosaurus is surrounded by limestone ... from the Cotswolds' (cpdinosaurs.org,
    Secondary Island page).
 4. Palaeo-planting (D-PM-54): 'Beyond these gravel margins, a low-growing planting zone ... ferns and conifers'
    (HTA); 'scattered ... cycad plants ... living Cycas revoluta' (cpdinosaurs.org); 'age-appropriate swamp cypresses
    and ferns' (Smithsonian 2023). Parametric ferns, cycads, swamp cypresses.
 5. Present-day sward (D-PM-55): the island turf material swapped for a mown/rough present-day sward with worn patches.
 6. 1854 young planting hidden (D-PM-56); mature present-day trees (MV20 v2 generator, park_trees_now.py) at the same
    trunk sites, except within 10 m of a Secondary Island sculpture ('Removal of unmanaged vegetation ... reinstates key
    views and vistas across the Geological Court', HTA).
World, look, exposure, sun, sculpture meshes, every camera: unchanged.
"""
import os, sys, json, math, random, argparse
import bpy, bmesh
from mathutils import Vector, Matrix, noise
from mathutils.bvhtree import BVHTree
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import park_trees_now as PT

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser(); ap.add_argument("--out", default="rounds/candidates/parknow-r01_cp074geocourt.blend")
ap.add_argument("--no-save", action="store_true")
A = ap.parse_args(argv)
SRC = bpy.data.filepath
OUT = A.out if os.path.isabs(A.out) else os.path.join(os.path.dirname(HERE), A.out)
assert os.path.abspath(OUT) != os.path.abspath(SRC), "refusing to overwrite the opened (live) blend"
assert not any("cp074_now" in o.keys() for o in bpy.data.objects), "source already carries the CP074 candidate"
TAG = "cp074_now_v1"
DATED = "present day (after the 2023-26 Geological Court conservation)"
R = random.Random(7474)
LOG = {"version": TAG, "src": SRC, "dated": DATED, "hidden": [], "objects": 0, "dims": {}, "trees": [], "skipped_trees": []}

coll = bpy.data.collections.new("PARKNOW_CP074_geological_court_now"); coll["dated"] = DATED
bpy.data.collections["PARK-NOW_present_day"].children.link(coll)
def link(ob):
    coll.objects.link(ob); ob["cp074_now"] = TAG; ob["dated"] = DATED; return ob

# ------------------------------------------------------------------ ground
TER = bpy.data.objects["terrain_lake_islands_1854"]
dg = bpy.context.evaluated_depsgraph_get()
BVH = BVHTree.FromObject(TER, dg); TINV = TER.matrix_world.inverted()
WATER_Z = bpy.data.objects["lake_water"].matrix_world.translation.z
def ground(x, y):
    loc, nrm, idx, d = BVH.ray_cast(TINV @ Vector((x, y, 200.0)), Vector((0, 0, -1)))
    if loc is None: return None, None
    z = (TER.matrix_world @ loc).z
    return z, TER.data.materials[TER.data.polygons[idx].material_index].name
def dry(x, y, margin=0.25):
    z, m = ground(x, y)
    return z is not None and z > WATER_Z + margin and m != "lake_bank_mud", z

# ------------------------------------------------------------------ material helpers
def mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; m["cp074_now"] = TAG
    nt = m.node_tree; b = next(x for x in nt.nodes if x.type == "BSDF_PRINCIPLED"); return m, nt.nodes, nt.links, b
def ramp(n, els):
    r = n.new("ShaderNodeValToRGB"); e = r.color_ramp.elements
    while len(e) < len(els): e.new(0.5)
    for el, (p, c) in zip(e, els): el.position = p; el.color = (*c, 1)
    return r
def tnoise(n, l, vec, scale, detail=4.0, rough=0.55):
    t = n.new("ShaderNodeTexNoise"); t.inputs["Scale"].default_value = scale; t.inputs["Detail"].default_value = detail
    t.inputs["Roughness"].default_value = rough
    if vec is not None: l.new(vec, t.inputs["Vector"])
    return t
def mix(n, l, fac, a, b_, blend="MIX"):
    m = n.new("ShaderNodeMix"); m.data_type = "RGBA"; m.blend_type = blend
    for s, i in ((fac, 0), (a, 6), (b_, 7)):
        if isinstance(s, (int, float)): m.inputs[i].default_value = s
        elif isinstance(s, tuple): m.inputs[i].default_value = (*s, 1)
        else: l.new(s, m.inputs[i])
    return m.outputs[2]
def smath(n, l, op, a, b_=None, clamp=False):
    m = n.new("ShaderNodeMath"); m.operation = op; m.use_clamp = clamp
    for i, s in enumerate((a, b_)):
        if s is None: continue
        if isinstance(s, (int, float)): m.inputs[i].default_value = s
        else: l.new(s, m.inputs[i])
    return m.outputs[0]

# ------------------------------------------------------------------ 1. present-day sculpture paint (D-PM-51)
# (back, flank, belly, mottle) linear albedo; I (hues), chosen so species read apart from afar (HTA brief)
PAINT = {
    "iguanodon":   ((0.050, 0.068, 0.036), (0.085, 0.100, 0.052), (0.150, 0.140, 0.092), (0.030, 0.040, 0.024)),
    "megalosaurus":((0.052, 0.040, 0.030), (0.090, 0.068, 0.046), (0.150, 0.122, 0.085), (0.030, 0.024, 0.018)),
    "hylaeosaurus":((0.040, 0.050, 0.030), (0.068, 0.074, 0.044), (0.120, 0.112, 0.074), (0.024, 0.030, 0.018)),
    "plesiosaur":  ((0.060, 0.056, 0.040), (0.095, 0.085, 0.060), (0.150, 0.135, 0.100), (0.036, 0.034, 0.026)),
    "ichthyosaur": ((0.046, 0.050, 0.050), (0.075, 0.080, 0.078), (0.135, 0.135, 0.125), (0.028, 0.030, 0.030)),
}
def paint_mat(sp):
    back, flank, belly, mott = PAINT[sp]
    m, n, l, b = mat(f"paint_now_{sp}")
    geo = n.new("ShaderNodeNewGeometry"); sep = n.new("ShaderNodeSeparateXYZ"); l.new(geo.outputs["Normal"], sep.inputs[0])
    tc = n.new("ShaderNodeTexCoord")
    # normal z -1..1 -> 0..1 (belly .. back)
    nz = n.new("ShaderNodeMapRange"); l.new(sep.outputs["Z"], nz.inputs["Value"]); nz.inputs["From Min"].default_value = -0.6; nz.inputs["From Max"].default_value = 0.9
    body = ramp(n, [(0.0, belly), (0.45, flank), (1.0, back)]); l.new(nz.outputs["Result"], body.inputs[0])
    mo = tnoise(n, l, tc.outputs["Object"], 0.9, 5.0, 0.6)
    mr = ramp(n, [(0.50, (0, 0, 0)), (0.62, (1, 1, 1))]); l.new(mo.outputs["Fac"], mr.inputs[0])
    c = mix(n, l, mr.outputs["Color"], body.outputs["Color"], mott)
    # lichen / lime bloom on upward faces (weathered concrete-and-brick sculptures)
    li = tnoise(n, l, tc.outputs["Object"], 3.5, 6.0, 0.7)
    lr = ramp(n, [(0.62, (0, 0, 0)), (0.70, (1, 1, 1))]); l.new(li.outputs["Fac"], lr.inputs[0])
    lf = smath(n, l, "MULTIPLY", lr.outputs["Color"], nz.outputs["Result"])
    c = mix(n, l, smath(n, l, "MULTIPLY", lf, 0.55), c, (0.16, 0.165, 0.13))
    l.new(c, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.78
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.35
    vo = n.new("ShaderNodeTexVoronoi"); l.new(tc.outputs["Object"], vo.inputs["Vector"]); vo.inputs["Scale"].default_value = 9.0
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.35; bp.inputs["Distance"].default_value = 0.02
    l.new(vo.outputs["Distance"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (*flank, 1); m["dated"] = DATED; m["source"] = "HTA Geological Court conservation: 50 colours, species legible from afar (hue I)"
    return m
SCULPT = [o for o in bpy.data.collections["DN54_secondary_island_sculptures__1854"].all_objects if o.type == "MESH" and not o.hide_render]
PM = {}
LOG["paint"] = {}
for o in SCULPT:
    sp = next(k for k in PAINT if o.name.startswith(k))
    if sp not in PM: PM[sp] = paint_mat(sp)
    for s in o.material_slots:
        s.link = "OBJECT"; s.material = PM[sp]       # object-level slot: the shared mesh/material data stay untouched
    o["cp074_now_paint"] = PM[sp].name; LOG["paint"][o.name] = PM[sp].name
    LOG["dims"][o.name] = [round(v, 2) for v in o.dimensions]

# ------------------------------------------------------------------ 5. present-day sward (D-PM-55)
m, n, l, b = mat("grass_now_island_sward")
tc = n.new("ShaderNodeTexCoord")
big = tnoise(n, l, tc.outputs["Object"], 0.045, 4.0, 0.55); fine = tnoise(n, l, tc.outputs["Object"], 0.9, 6.0, 0.6)
g = ramp(n, [(0.30, (0.040, 0.075, 0.022)), (0.55, (0.062, 0.100, 0.030)), (0.75, (0.095, 0.115, 0.040)), (0.92, (0.135, 0.125, 0.060))])
l.new(big.outputs["Fac"], g.inputs[0])
f2 = ramp(n, [(0.35, (0.80, 0.80, 0.80)), (0.65, (1.12, 1.10, 1.05))]); l.new(fine.outputs["Fac"], f2.inputs[0])
c = mix(n, l, 1.0, g.outputs["Color"], f2.outputs["Color"], "MULTIPLY")
wear = tnoise(n, l, tc.outputs["Object"], 0.12, 3.0, 0.5)
wr = ramp(n, [(0.68, (0, 0, 0)), (0.76, (1, 1, 1))]); l.new(wear.outputs["Fac"], wr.inputs[0])
c = mix(n, l, smath(n, l, "MULTIPLY", wr.outputs["Color"], 0.6), c, (0.12, 0.10, 0.065))
l.new(c, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.92
if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.25
bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.3; l.new(fine.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
m.diffuse_color = (0.062, 0.1, 0.03, 1); m["dated"] = DATED
for s in TER.material_slots:
    if s.material and s.material.name == "grass_1854_young_turf":
        s.link = "OBJECT"; s.material = m; LOG["sward"] = "object-slot swap grass_1854_young_turf -> grass_now_island_sward"

# ------------------------------------------------------------------ 2. gravel swathes (D-PM-52)
def gravel_mat(name, c0, c1):
    m, n, l, b = mat(name); tc = n.new("ShaderNodeTexCoord")
    vo = n.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 22.0; l.new(tc.outputs["Object"], vo.inputs["Vector"])
    nz = tnoise(n, l, tc.outputs["Object"], 0.6, 4.0, 0.6)
    r = ramp(n, [(0.0, c0), (1.0, c1)]); l.new(vo.outputs["Distance"], r.inputs[0])
    r2 = ramp(n, [(0.3, (0.78, 0.78, 0.78)), (0.7, (1.1, 1.08, 1.05))]); l.new(nz.outputs["Fac"], r2.inputs[0])
    l.new(mix(n, l, 1.0, r.outputs["Color"], r2.outputs["Color"], "MULTIPLY"), b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.95
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.6; bp.inputs["Distance"].default_value = 0.03
    l.new(vo.outputs["Distance"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (*c1, 1); m["dated"] = DATED; return m
G_WEALD = gravel_mat("gravel_now_wealden_buff", (0.105, 0.080, 0.050), (0.200, 0.160, 0.105))
G_OOL = gravel_mat("gravel_now_oolite_pale", (0.150, 0.140, 0.115), (0.250, 0.235, 0.195))
def sculpt_frame(o):
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
    cx = sum(v.x for v in bb) / 8; cy = sum(v.y for v in bb) / 8
    ang = o.matrix_world.to_euler().z
    return Vector((cx, cy)), ang, o.dimensions.x / 2, o.dimensions.y / 2
LAND = [o for o in SCULPT if o.name.split("_")[0] in ("iguanodon", "megalosaurus", "hylaeosaurus")]
def swathe(name, ctr, ang, ax, ay, gm, rings=10, segs=72):
    bm = bmesh.new(); cs, sn = math.cos(ang), math.sin(ang); rows = []
    wob = [1.0 + 0.10 * math.sin(3 * t * 2 * math.pi / segs + 1.3) + 0.06 * math.sin(7 * t * 2 * math.pi / segs) for t in range(segs)]
    centre = bm.verts.new((ctr.x, ctr.y, (ground(ctr.x, ctr.y)[0] or 0) + 0.04))
    for r in range(1, rings + 1):
        row = []
        for t in range(segs):
            th = 2 * math.pi * t / segs; k = r / rings * wob[t]
            lx, ly = math.cos(th) * ax * k, math.sin(th) * ay * k
            x, y = ctr.x + lx * cs - ly * sn, ctr.y + lx * sn + ly * cs
            z = ground(x, y)[0]; z = (z if z is not None else WATER_Z) + 0.04
            row.append(bm.verts.new((x, y, z)))
        rows.append(row)
    for t in range(segs): bm.faces.new((centre, rows[0][t], rows[0][(t + 1) % segs]))
    for a_, b_ in zip(rows, rows[1:]):
        for t in range(segs): bm.faces.new((a_[t], b_[t], b_[(t + 1) % segs], a_[(t + 1) % segs]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(gm)
    for p in me.polygons: p.use_smooth = True
    return link(bpy.data.objects.new(name, me))
SW = []
LOG["swathes"] = []
for o in LAND:
    ctr, ang, hx, hy = sculpt_frame(o)
    gm = G_OOL if o.name.startswith("megalosaurus") else G_WEALD
    ax, ay = hx + 3.2, hy + 3.0
    sw = swathe("cp74_gravel_" + o.name, ctr, ang, ax, ay, gm); SW.append((o, ctr, ang, ax, ay))
    LOG["swathes"].append((o.name, gm.name, round(2 * ax, 1), round(2 * ay, 1)))

# ------------------------------------------------------------------ 3. rock blocks (D-PM-53)
def stone_mat(name, c0, c1):
    m, n, l, b = mat(name); tc = n.new("ShaderNodeTexCoord")
    nz = tnoise(n, l, tc.outputs["Object"], 2.2, 6.0, 0.65); st = tnoise(n, l, tc.outputs["Object"], 0.5, 3.0, 0.5)
    r = ramp(n, [(0.25, c0), (0.75, c1)]); l.new(nz.outputs["Fac"], r.inputs[0])
    dk = ramp(n, [(0.4, (0.7, 0.72, 0.68)), (0.6, (1.0, 1.0, 1.0))]); l.new(st.outputs["Fac"], dk.inputs[0])
    l.new(mix(n, l, 1.0, r.outputs["Color"], dk.outputs["Color"], "MULTIPLY"), b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.9
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.5; l.new(nz.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (*c1, 1); m["dated"] = DATED; return m
S_WEALD = stone_mat("stone_now_wealden_sandstone", (0.085, 0.072, 0.048), (0.180, 0.150, 0.098))
S_OOL = stone_mat("stone_now_cotswold_oolite", (0.130, 0.118, 0.090), (0.240, 0.220, 0.170))
def rock(name, c, sx, sy, sz, yaw, sm, seed):
    """weathered boulder: subdivided icosphere, two-octave noise, flattened bed bedded ~25 % into the ground"""
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=3, radius=0.5)
    off = Vector((seed * 0.37, seed * 0.11, seed * 0.73))
    for v in bm.verts:
        p = v.co.copy(); k = 1.0 + 0.28 * noise.noise(p * 1.6 + off) + 0.08 * noise.noise(p * 6.0 + off)
        q = Vector((p.x * sx * k, p.y * sy * k, p.z * sz * k))
        q.z = max(q.z, -0.22 * sz)                                       # flat bed
        v.co = q
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(yaw, 3, "Z"))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(sm)
    for p_ in me.polygons: p_.use_smooth = True
    ob = link(bpy.data.objects.new(name, me)); ob.location = c; return ob
LOG["rocks"] = 0
for o, ctr, ang, ax, ay in SW:
    sm = S_OOL if o.name.startswith("megalosaurus") else S_WEALD
    cs, sn = math.cos(ang), math.sin(ang); nb = 9 if o.name.startswith("iguanodon") else 8
    for i in range(nb):
        th = 2 * math.pi * (i + R.uniform(-0.3, 0.3)) / nb; k = R.uniform(0.62, 0.92)
        lx, ly = math.cos(th) * ax * k, math.sin(th) * ay * k
        x, y = ctr.x + lx * cs - ly * sn, ctr.y + lx * sn + ly * cs
        z = ground(x, y)[0]
        if z is None: continue
        for j in range(R.randint(1, 3)):                                   # small clusters of 1-3 stones
            s = R.uniform(0.6, 1.4) * (0.65 if j else 1.0)
            xx, yy = x + R.uniform(-0.9, 0.9) * j, y + R.uniform(-0.9, 0.9) * j
            zz = ground(xx, yy)[0] or z
            rock(f"cp74_rock_{o.name}_{i:02d}{j}", Vector((xx, yy, zz)), s * R.uniform(1.0, 1.6), s * R.uniform(0.8, 1.2), s * R.uniform(0.5, 0.8), R.uniform(0, math.pi), sm, i * 7 + j + len(o.name) * 13)
            LOG["rocks"] += 1

# ------------------------------------------------------------------ 4. palaeo-planting: ferns, cycads, swamp cypresses (D-PM-54)
def plant_mat(name, c0, c1, trans=0.3):
    m, n, l, b = mat(name); oi = n.new("ShaderNodeObjectInfo"); at = n.new("ShaderNodeAttribute"); at.attribute_name = "t"
    r = ramp(n, [(0.0, c0), (1.0, c1)])
    l.new(smath(n, l, "ADD", smath(n, l, "MULTIPLY", oi.outputs["Random"], 0.5), smath(n, l, "MULTIPLY", at.outputs["Fac"], 0.5)), r.inputs[0])
    l.new(r.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.6
    tr = n.new("ShaderNodeBsdfTranslucent"); l.new(r.outputs["Color"], tr.inputs["Color"])
    mx = n.new("ShaderNodeMixShader"); mx.inputs[0].default_value = trans
    out = next(x for x in n if x.type == "OUTPUT_MATERIAL"); l.new(b.outputs[0], mx.inputs[1]); l.new(tr.outputs[0], mx.inputs[2]); l.new(mx.outputs[0], out.inputs[0])
    m.diffuse_color = (*c1, 1); m["dated"] = DATED; return m
M_FERN = plant_mat("plant_now_fern", (0.030, 0.070, 0.015), (0.085, 0.150, 0.035), 0.35)
M_CYCAD = plant_mat("plant_now_cycas", (0.018, 0.040, 0.012), (0.050, 0.085, 0.025), 0.15)
M_CYTRUNK = stone_mat("plant_now_cycas_trunk", (0.060, 0.042, 0.028), (0.110, 0.080, 0.050))
M_TAXO = plant_mat("plant_now_taxodium", (0.040, 0.065, 0.020), (0.100, 0.130, 0.045), 0.25)
def frond(bm, tl, base, yaw, pitch, L, w, n=9, droop=0.55, stiff=False):
    """pinnate frond: rachis arc + paired leaflets (triangles); 't' attr 0 at base .. 1 at tip"""
    d0 = Vector((math.cos(yaw) * math.cos(pitch), math.sin(yaw) * math.cos(pitch), math.sin(pitch)))
    side = Vector((-math.sin(yaw), math.cos(yaw), 0.0))
    pts = []
    for i in range(n + 1):
        t = i / n; p = base + d0 * (L * t); p.z -= droop * L * t * t * (0.4 if stiff else 1.0); pts.append((t, p))
    for (t0, p0), (t1, p1) in zip(pts, pts[1:]):
        ww = w * (1.0 - 0.75 * t0) if not stiff else w * (1.0 - 0.3 * t0)
        dirv = (p1 - p0).normalized()
        for sgn in (-1, 1):
            tip = p0 + side * (sgn * ww) + dirv * (ww * 0.6) + Vector((0, 0, -0.15 * ww if not stiff else 0.0))
            f = bm.faces.new((bm.verts.new(p0), bm.verts.new(p1), bm.verts.new(tip)))
            for lp in f.loops: lp[tl].uv = (t0, 0.0)
def plant_obj(name, build, loc, m_list):
    bm = bmesh.new(); tl = bm.loops.layers.uv.new("tuv"); build(bm, tl)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for mm in m_list: me.materials.append(mm)
    # copy uv.x into a float attribute 't' (face corner) for the shader ramp
    uv = me.uv_layers["tuv"]; at = me.attributes.new("t", "FLOAT", "CORNER")
    for i, d in enumerate(uv.data): at.data[i].value = d.uv.x
    ob = link(bpy.data.objects.new(name, me)); ob.location = loc; return ob
def fern(seed, H):
    rr = random.Random(seed)
    def b_(bm, tl):
        nf = rr.randint(9, 14)
        for k in range(nf):
            yaw = 2 * math.pi * k / nf + rr.uniform(-0.25, 0.25)
            frond(bm, tl, Vector((0, 0, 0.05)), yaw, math.radians(rr.uniform(40, 68)), H * rr.uniform(0.85, 1.2), H * 0.13, 16, 0.55)
    return b_
def cycad(seed, H):
    rr = random.Random(seed)
    def b_(bm, tl):
        th = H * 0.35
        res = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.20 * H, radius2=0.15 * H, depth=th)
        bmesh.ops.translate(bm, verts=res["verts"], vec=(0, 0, th / 2))
        for f in bm.faces: f.material_index = 1
        nf = rr.randint(16, 22)
        for k in range(nf):
            yaw = 2 * math.pi * k / nf + rr.uniform(-0.15, 0.15)
            frond(bm, tl, Vector((0, 0, th)), yaw, math.radians(rr.uniform(15, 45)), H * rr.uniform(0.9, 1.15), H * 0.09, 14, 0.25, stiff=True)
    return b_
def taxodium(seed, H):
    """swamp cypress: straight buttressed trunk + narrow conical crown of feathery clumps"""
    rr = random.Random(seed)
    def b_(bm, tl):
        res = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.035 * H, radius2=0.01 * H, depth=H * 0.92)
        bmesh.ops.translate(bm, verts=res["verts"], vec=(0, 0, H * 0.46))
        for f in bm.faces: f.material_index = 1
        nlev = 46
        for i in range(nlev):
            t = i / (nlev - 1); z = H * (0.18 + 0.80 * t); rad = H * 0.24 * (1.0 - t) ** 0.9 + 0.4
            for k in range(rr.randint(16, 22)):
                yaw = rr.uniform(0, 2 * math.pi); zz = z + rr.uniform(-0.25, 0.25)
                frond(bm, tl, Vector((0, 0, zz)), yaw, math.radians(rr.uniform(-5, 30)), rad * rr.uniform(0.55, 1.1), 0.55 + 0.55 * (1 - t), 7, 0.12)
    return b_
LOG["ferns"] = 0; LOG["cycads"] = 0; LOG["taxodium"] = []
def near_sculpt(x, y, pad):
    for o, ctr, ang, ax, ay in SW:
        cs, sn = math.cos(-ang), math.sin(-ang); dx, dy = x - ctr.x, y - ctr.y
        lx, ly = dx * cs - dy * sn, dx * sn + dy * cs
        if (lx / (ax + pad)) ** 2 + (ly / (ay + pad)) ** 2 < 1.0: return True
    return False
# planting zone: an annulus 0.5..6 m outside each gravel swathe
for o, ctr, ang, ax, ay in SW:
    cs, sn = math.cos(ang), math.sin(ang)
    nfern = 46 if o.name.startswith("iguanodon") else 30
    for i in range(nfern):
        th = R.uniform(0, 2 * math.pi); k = 1.0 + R.uniform(0.12, 0.75)
        lx, ly = math.cos(th) * ax * k, math.sin(th) * ay * k
        x, y = ctr.x + lx * cs - ly * sn, ctr.y + lx * sn + ly * cs
        if near_sculpt(x, y, 0.2): continue
        ok, z = dry(x, y)
        if not ok: continue
        H = R.uniform(0.9, 1.5)
        ob = plant_obj(f"cp74_fern_{o.name}_{i:02d}", fern(i * 31 + len(o.name), H), Vector((x, y, z - 0.02)), [M_FERN]); ob.rotation_euler.z = R.uniform(0, 6.28)
        LOG["ferns"] += 1
    for i in range(5):
        th = R.uniform(0, 2 * math.pi); k = 1.0 + R.uniform(0.1, 0.5)
        lx, ly = math.cos(th) * ax * k, math.sin(th) * ay * k
        x, y = ctr.x + lx * cs - ly * sn, ctr.y + lx * sn + ly * cs
        if near_sculpt(x, y, 0.3): continue
        ok, z = dry(x, y)
        if not ok: continue
        H = R.uniform(0.9, 1.4)          # Cycas revoluta: ~1-1.5 m fronds on a short trunk (I)
        plant_obj(f"cp74_cycas_{o.name}_{i:02d}", cycad(i * 17 + len(o.name) * 3, H), Vector((x, y, z - 0.05)), [M_CYCAD, M_CYTRUNK]).rotation_euler.z = R.uniform(0, 6.28)
        LOG["cycads"] += 1


# rough-sward tufts in the CP074 view (present-day long grass at the planting margins; I)
M_TUFT = plant_mat("plant_now_rough_grass", (0.040, 0.075, 0.022), (0.110, 0.125, 0.045), 0.3)
bm = bmesh.new(); tl = bm.loops.layers.uv.new("tuv"); ntuft = 0
camo = bpy.data.objects["CAM_CP074_dinosaurs_35mm"]; fwd = (camo.matrix_world.to_3x3() @ Vector((0, 0, -1))).xy.normalized()
for i in range(26000):
    dist = 4.0 + 46.0 * (R.random() ** 1.4); a = math.radians(R.uniform(-40, 40))
    d2 = Vector((fwd.x * math.cos(a) - fwd.y * math.sin(a), fwd.x * math.sin(a) + fwd.y * math.cos(a)))
    x, y = camo.location.x + d2.x * dist, camo.location.y + d2.y * dist
    if near_sculpt(x, y, -0.3): continue
    ok, z = dry(x, y, 0.15)
    if not ok: continue
    # clump density follows a low-frequency noise so the long grass gathers in drifts, not an even carpet
    nv = noise.noise(Vector((x * 0.09, y * 0.09, 0.5)))
    if nv > 0.12 or near_sculpt(x, y, 3.5): hh = R.uniform(0.22, 0.45)          # long-grass drift / planting margin
    elif R.random() < 0.55: continue
    else: hh = R.uniform(0.07, 0.16)                                            # mown sward texture
    for k in range(7):
        yaw = R.uniform(0, 2 * math.pi); lean = R.uniform(0.15, 0.55)
        b0 = Vector((x + R.uniform(-0.06, 0.06), y + R.uniform(-0.06, 0.06), z - 0.01))
        side = Vector((-math.sin(yaw), math.cos(yaw), 0)) * 0.012
        tip = b0 + Vector((math.cos(yaw) * lean * hh, math.sin(yaw) * lean * hh, hh))
        f = bm.faces.new((bm.verts.new(b0 - side), bm.verts.new(b0 + side), bm.verts.new(tip)))
        for j, lp in enumerate(f.loops): lp[tl].uv = (1.0 if j == 2 else 0.0, 0.0)
    ntuft += 1
me = bpy.data.meshes.new("cp74_rough_grass_tufts"); bm.to_mesh(me); bm.free(); me.materials.append(M_TUFT)
uv = me.uv_layers["tuv"]; at = me.attributes.new("t", "FLOAT", "CORNER")
for i, d in enumerate(uv.data): at.data[i].value = d.uv.x
link(bpy.data.objects.new("cp74_rough_grass_tufts", me)); LOG["tufts"] = ntuft

# ------------------------------------------------------------------ 6. young 1854 planting -> mature present-day trees (D-PM-56)
TREES = bpy.data.objects["trees_parkland_and_young_island_planting"]
tb = bmesh.new(); tb.from_mesh(TREES.data); tb.verts.ensure_lookup_table(); seen = set(); sites = []
for v in tb.verts:
    if v.index in seen: continue
    st = [v]; seen.add(v.index); comp = []
    while st:
        x = st.pop(); comp.append(x)
        for e in x.link_edges:
            y = e.other_vert(x)
            if y.index not in seen: seen.add(y.index); st.append(y)
    if len(comp) == 14:                                   # trunk cylinders (crown blobs are 42-vert parts)
        pts = [TREES.matrix_world @ q.co for q in comp]
        zmin = min(p.z for p in pts); zmax = max(p.z for p in pts)
        sites.append((sum(p.x for p in pts) / 14, sum(p.y for p in pts) / 14, zmin, zmax - zmin))
tb.free()
TREES.hide_render = True; LOG["hidden"].append((TREES.name, "1854 young planting; replaced by mature present-day trees at the same trunk sites"))
PT.LEAF_GAIN = 1.0
cam = bpy.data.objects["CAM_CP074_dinosaurs_35mm"].location
def blocks_view(x, y, half_deg=12.0):
    """True if a trunk at (x, y) stands nearer than the sculptures inside +-half_deg of the sight line from either CP074 camera."""
    for cn in ("CAM_CP074_dinosaurs_35mm", "CAM_CP074_iguanodon_50mm"):
        c = bpy.data.objects[cn].location.xy; v = Vector((x, y)) - c
        for o, ctr, ang, ax, ay in SW:
            w = ctr - c
            if v.length < w.length and v.length > 0.1 and abs(math.degrees(v.angle_signed(w))) < half_deg: return True
    return False
for i, (x, y, zmin, h) in enumerate(sites):
    if near_sculpt(x, y, 7.0):
        LOG["skipped_trees"].append((round(x, 1), round(y, 1), "within ~10 m of a Secondary Island sculpture (vistas reinstated)")); continue
    if (Vector((x, y)) - cam.xy).length < 6.0:
        LOG["skipped_trees"].append((round(x, 1), round(y, 1), "camera position")); continue
    if blocks_view(x, y):
        LOG["skipped_trees"].append((round(x, 1), round(y, 1), "would stand between a CP074 camera and the sculptures")); continue
    z, gm = ground(x, y)
    if z is None: z = zmin
    hab = "oak" if i % 3 else "elm"; H = R.uniform(17.0, 24.0)   # 170-year park trees (I); young 1854 sites were 7-12 m
    me, info = PT.build_tree(f"cp74_tree_{i:03d}", hab, H, 7400 + i * 29)
    ob = link(bpy.data.objects.new(f"cp74_tree_{i:03d}", me)); ob.location = (x, y, z - 0.05); ob.rotation_euler.z = R.uniform(0, 6.28)
    LOG["trees"].append((ob.name, hab, round(H, 1), round(x, 1), round(y, 1), round(h, 1)))
# swamp cypresses on the island rim behind the dinosaurs (Smithsonian 2023: 'surrounded by age-appropriate swamp cypresses')
for j, (x, y) in enumerate([(-74.0, -884.0), (-90.0, -879.0), (-102.0, -871.0), (-58.0, -887.0)]):
    ok, z = dry(x, y)
    if not ok or near_sculpt(x, y, 2.0):
        LOG["taxodium"].append((round(x, 1), round(y, 1), "skipped")); continue
    H = R.uniform(18.0, 24.0)
    plant_obj(f"cp74_taxodium_{j}", taxodium(900 + j, H), Vector((x, y, z - 0.1)), [M_TAXO, PT.tree_mats("oak")["bark"]])
    LOG["taxodium"].append((round(x, 1), round(y, 1), round(H, 1)))

bpy.context.scene["cp074_geocourt_candidate"] = TAG
LOG["objects"] = sum(1 for o in bpy.data.objects if "cp074_now" in o.keys())
os.makedirs(os.path.join(os.path.dirname(HERE), "checks"), exist_ok=True)
json.dump(LOG, open(os.path.join(os.path.dirname(HERE), "checks", "cp074_geocourt_candidate.json"), "w"), indent=1)
if not A.no_save:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True, copy=True)
print("CP074_CANDIDATE_SAVED", OUT, "objects", LOG["objects"], "trees", len(LOG["trees"]), "skipped", len(LOG["skipped_trees"]),
      "ferns", LOG["ferns"], "cycads", LOG["cycads"], "rocks", LOG["rocks"], flush=True)
