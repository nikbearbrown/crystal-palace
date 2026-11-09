"""CP006 'A temporary claim on a park' -- polish CANDIDATE 'winterpark' 2026-11-09 (DEPARTURES SD35-SD41; NOT live).
Run on the live rounds/s02.blend (never written; saves rounds/candidates/s02_cp006park.blend):
  blender -b rounds/s02.blend -P scripts/cand_cp006_winterpark_20261109.py -- [--out PATH]
Scoped to CP006 only: every new object is W6_-prefixed and base-hidden; grok_states CP006 shows W6_ and hides the
objects it replaces (G_PARK*, PATH_SOUTH_FOOT, SVP_, SV_TOOL, CPL_HorizonGround) -- CP007-CP009 states/objects untouched.
The TR_W_ winter park trees (already CP006-only: base-hidden, shown only by the CP006 state) get new bare-crown meshes.
  * SD35 winter park trees: lollipop icosphere clumps -> bare branching broadleaf crowns (trunk 30% H, ascending
    scaffold limbs, 3 orders of branches) + a feathered translucent twig-haze crown; heights 58/68/78 ft unchanged.
  * SD36 winter turf: CP006-only copy of the park ground with a dull olive/straw winter turf shader (multi-scale
    patches, tussock tone, fine bump).
  * SD37 near sward: particle-hair grass (5-11 cm blades, olive to straw) over both frusta out to ~55 m, thinning with distance.
  * SD38 footpath: CP006-only copy of the south footpath re-surfaced as trodden winter gravel (darker, damp, pebbles).
  * SD39 survey party in frame: 1850-dress figures (c9_figures_v2, the KEEP'd CP009 builder) at the theodolite, the
    field book, a ranging pole and the chain, on the limited survey line y = -204 ft; old lathe party hidden for CP006.
  * SD40 survey kit rebuilt in metres (theodolite on tripod, 8 ft ranging poles, Gunter's chain, chaining arrows,
    10 ft levelling staff) at the in-frame pegs.
  * SD41 CPL_HorizonGround hidden for CP006 cameras only (pale disk showing where the terrain dips below it).
"""
import bpy, bmesh, sys, os, math, random, json
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

def arg(k, d=None):
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return a[a.index(k) + 1] if k in a else d

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import c9_figures_v2 as F
FT = 0.3048; TAG = "cp006_winterpark_20261109"
sc = bpy.context.scene
coll = bpy.data.collections.new("CP006W"); sc.collection.children.link(coll)
def link(o):
    coll.objects.link(o); o.hide_render = True; o[TAG] = True; return o

# ---------------- ground height (BVH on the near park patch, fallback far patch) ----------------
def bvh_of(name):
    o = bpy.data.objects[name]; bm = bmesh.new(); bm.from_mesh(o.data); bm.transform(o.matrix_world)
    t = BVHTree.FromBMesh(bm); bm.free(); return t
BV = [bvh_of("G_PARK_NEAR"), bvh_of("G_PARK")]
def gz(x, y):
    for t in BV:
        hit = t.ray_cast(Vector((x, y, 50.0)), Vector((0, 0, -1)))
        if hit[0] is not None: return hit[0].z
    return 0.0

# ---------------- material helpers ----------------
def newmat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(b.outputs[0], out.inputs[0]); return m, nt, b, out
def flat(name, c, rough=0.8, metal=0.0):
    m, nt, b, _ = newmat(name); b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal; m.diffuse_color = (*c, 1); return m
def ramp(nt, fac, cols):
    r = nt.nodes.new("ShaderNodeValToRGB"); e = r.color_ramp
    e.elements[0].position, e.elements[0].color = cols[0][0], (*cols[0][1], 1)
    e.elements[1].position, e.elements[1].color = cols[-1][0], (*cols[-1][1], 1)
    for p, c in cols[1:-1]: el = e.elements.new(p); el.color = (*c, 1)
    nt.links.new(fac, r.inputs[0]); return r.outputs[0]
def wpos(nt):
    g = nt.nodes.new("ShaderNodeNewGeometry"); return g.outputs["Position"]
def noise(nt, vec, scale, detail=4, rough=0.55, out="Fac"):
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail; n.inputs["Roughness"].default_value = rough
    nt.links.new(vec, n.inputs["Vector"]); return n.outputs[out]
def mixc(nt, a, b, fac):
    m = nt.nodes.new("ShaderNodeMix"); m.data_type = "RGBA"
    nt.links.new(a, m.inputs[6]); nt.links.new(b, m.inputs[7])
    if isinstance(fac, float): m.inputs[0].default_value = fac
    else: nt.links.new(fac, m.inputs[0])
    return m.outputs[2]
def math_(nt, op, a, b=None, clamp=False):
    m = nt.nodes.new("ShaderNodeMath"); m.operation = op; m.use_clamp = clamp
    for i, v in enumerate((a, b)):
        if v is None: continue
        if isinstance(v, (int, float)): m.inputs[i].default_value = v
        else: nt.links.new(v, m.inputs[i])
    return m.outputs[0]

# SD36 winter turf (albedo kept close to GT_ParkGrass1850's 0.10-0.25 range so exposure barely moves)
def turf_mat():
    m, nt, b, _ = newmat("W6_WinterTurf1850")
    p = wpos(nt)
    big = noise(nt, p, 0.035, 3, 0.5); mid = noise(nt, p, 0.45, 5, 0.6); fine = noise(nt, p, 9.0, 3, 0.7)
    base = ramp(nt, big, [(0.30, (0.050, 0.075, 0.024)), (0.55, (0.085, 0.100, 0.036)), (0.75, (0.15, 0.135, 0.065))])
    tus = ramp(nt, mid, [(0.35, (0.040, 0.060, 0.020)), (0.65, (0.17, 0.15, 0.075))])
    c = mixc(nt, base, tus, 0.42)
    straw = ramp(nt, fine, [(0.45, (0.0, 0.0, 0.0)), (0.62, (1.0, 1.0, 1.0))])
    c = mixc(nt, c, ramp(nt, fine, [(0.0, (0.26, 0.22, 0.12)), (1.0, (0.30, 0.26, 0.15))]), math_(nt, "MULTIPLY", nt.nodes[-2].outputs[0] if False else straw, 0.35))
    nt.links.new(c, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.95
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.35; bp.inputs["Distance"].default_value = 0.02
    nt.links.new(math_(nt, "ADD", noise(nt, p, 30.0, 2), math_(nt, "MULTIPLY", noise(nt, p, 140.0, 1), 0.5)), bp.inputs["Height"])
    nt.links.new(bp.outputs[0], b.inputs["Normal"]); m.diffuse_color = (0.11, 0.12, 0.05, 1); return m

# SD38 trodden winter gravel
def gravel_mat():
    m, nt, b, _ = newmat("W6_WinterGravel1850")
    p = wpos(nt)
    v = nt.nodes.new("ShaderNodeTexVoronoi"); v.inputs["Scale"].default_value = 55.0; nt.links.new(p, v.inputs["Vector"])
    stones = ramp(nt, v.outputs["Distance"], [(0.05, (0.36, 0.32, 0.26)), (0.45, (0.17, 0.15, 0.12))])
    damp = noise(nt, p, 0.6, 4, 0.6)
    wet = ramp(nt, damp, [(0.40, (1.0, 1.0, 1.0)), (0.70, (0.62, 0.60, 0.58))])
    mm = nt.nodes.new("ShaderNodeMix"); mm.data_type = "RGBA"; mm.blend_type = "MULTIPLY"; mm.inputs[0].default_value = 1.0
    nt.links.new(stones, mm.inputs[6]); nt.links.new(wet, mm.inputs[7])
    tone = ramp(nt, noise(nt, p, 0.08, 3), [(0.3, (0.92, 0.95, 1.0)), (0.7, (1.05, 1.0, 0.92))])
    m2 = nt.nodes.new("ShaderNodeMix"); m2.data_type = "RGBA"; m2.blend_type = "MULTIPLY"; m2.inputs[0].default_value = 1.0
    nt.links.new(mm.outputs[2], m2.inputs[6]); nt.links.new(tone, m2.inputs[7])
    nt.links.new(m2.outputs[2], b.inputs["Base Color"])
    nt.links.new(ramp(nt, damp, [(0.40, (0.92, 0.92, 0.92)), (0.70, (0.55, 0.55, 0.55))]), b.inputs["Roughness"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.6; bp.inputs["Distance"].default_value = 0.01
    nt.links.new(v.outputs["Distance"], bp.inputs["Height"]); nt.links.new(bp.outputs[0], b.inputs["Normal"])
    m.diffuse_color = (0.24, 0.21, 0.17, 1); return m

# SD35 twig haze: translucent, thicker toward the crown centre (facing), broken by noise
def haze_mat():
    m = bpy.data.materials.new("W6_TwigHaze1850"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); d = nt.nodes.new("ShaderNodeBsdfPrincipled")
    d.inputs["Base Color"].default_value = (0.085, 0.072, 0.064, 1); d.inputs["Roughness"].default_value = 0.95
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader")
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.5
    face = math_(nt, "SUBTRACT", 1.0, lw.outputs["Facing"], clamp=True)
    face = math_(nt, "POWER", face, 1.6)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    n = noise(nt, tc.outputs["Object"], 0.9, 5, 0.7)
    nn = math_(nt, "MULTIPLY_ADD", n, 1.2) if False else math_(nt, "ADD", math_(nt, "MULTIPLY", n, 1.1), -0.15)
    a = math_(nt, "MULTIPLY", math_(nt, "MULTIPLY", face, nn), 0.62, clamp=True)
    nt.links.new(a, mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(d.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs[0]); m.diffuse_color = (0.085, 0.072, 0.064, 1)
    m.blend_method = "BLEND" if hasattr(m, "blend_method") else None
    return m

TURF = turf_mat(); GRAVEL = gravel_mat(); HAZE = haze_mat()
BARK = bpy.data.materials["GT_Bark"]

# ---------------- SD35 bare winter park trees ----------------
def tube(bm, a, b, ra, rb, seg):
    d = b - a
    if d.length < 1e-6: return
    d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0))
    s = d.cross(up).normalized(); u = s.cross(d).normalized()
    A = [bm.verts.new(a + (s * math.cos(2 * math.pi * k / seg) + u * math.sin(2 * math.pi * k / seg)) * ra) for k in range(seg)]
    B = [bm.verts.new(b + (s * math.cos(2 * math.pi * k / seg) + u * math.sin(2 * math.pi * k / seg)) * rb) for k in range(seg)]
    for k in range(seg): bm.faces.new([A[k], A[(k + 1) % seg], B[(k + 1) % seg], B[k]])

def bare_tree_mesh(name, seed, H_ft):
    rnd = random.Random(seed); H = H_ft * FT; bm = bmesh.new(); tips = []
    trunk_h = H * rnd.uniform(0.28, 0.34); R0 = H * 0.022
    crown_r = H * 0.36
    def branch(p, d, length, radius, depth, wig):
        n = max(2, int(length / 0.9)); cur = Vector(p); dv = Vector(d).normalized(); pts = [cur.copy()]
        for i in range(n):
            dv = (dv + Vector((rnd.uniform(-wig, wig), rnd.uniform(-wig, wig), rnd.uniform(-wig * 0.3, wig * 0.6)))).normalized()
            cur = cur + dv * (length / n)
            # keep the crown an ellipsoidal dome (elm/ broadleaf winter silhouette)
            cur.z = min(cur.z, H - 0.3)
            pts.append(cur.copy())
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            r0 = max(0.008, radius * (1 - 0.55 * i / n)); r1 = max(0.008, radius * (1 - 0.55 * (i + 1) / n))
            tube(bm, a, b, r0, r1, 7 if radius > 0.12 else 5 if radius > 0.04 else 3)
        if depth == 0: tips.append(pts[-1].copy()); return
        nk = 3 if depth >= 2 else 4
        for k in range(nk):
            t = rnd.uniform(0.35, 0.95); base = pts[max(1, min(len(pts) - 1, int(round(t * n))))]
            ang = rnd.uniform(0, 2 * math.pi)
            nd = (dv * 1.1 + Vector((math.cos(ang), math.sin(ang), rnd.uniform(0.0, 0.7)))).normalized()
            branch(base, nd, length * rnd.uniform(0.48, 0.62), radius * 0.52, depth - 1, wig * 1.25)
    branch((0, 0, -0.3), (0, 0, 1), trunk_h + 0.3, R0, 0, 0.02); tips.clear()
    top = Vector((0, 0, trunk_h))
    for k in range(5):
        ang = 2 * math.pi * k / 5 + rnd.uniform(-.35, .35); sp = rnd.uniform(0.35, 0.75)
        branch(top + Vector((0, 0, rnd.uniform(-0.6, 0.6))), Vector((math.cos(ang) * sp, math.sin(ang) * sp, 1)).normalized(),
               (H - trunk_h) * rnd.uniform(0.55, 0.72), R0 * 0.55, 3, 0.10)
    for k in range(4):
        ang = rnd.uniform(0, 2 * math.pi); zb = trunk_h * rnd.uniform(0.7, 1.0)
        branch(Vector((0, 0, zb)), Vector((math.cos(ang), math.sin(ang), rnd.uniform(0.3, 0.6))).normalized(), crown_r * rnd.uniform(0.6, 0.85), R0 * 0.30, 2, 0.12)
    nb = len(bm.faces)
    # twig haze: soft crown shells around clusters of branch tips (the fine twigs a bare broadleaf shows at distance)
    rnd.shuffle(tips); cents = []
    for tp in tips:
        if all((tp - c).length > H * 0.13 for c in cents): cents.append(tp)
        if len(cents) >= 9: break
    for c in cents:
        r = H * rnd.uniform(0.11, 0.16); cc = c * 0.92 + Vector((0, 0, H * 0.02))
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=Matrix.Translation(cc) @ Matrix.Diagonal((r, r, r * 0.82, 1)))
    bm.faces.ensure_lookup_table()
    for f in bm.faces[nb:]: f.material_index = 1
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(BARK); me.materials.append(HAZE)
    for p in me.polygons: p.use_smooth = True
    return me

NEW_TW = [bare_tree_mesh(f"W6_TR_W_bare_{k}", 600 + k, H) for k, H in enumerate((58, 68, 78))]
ntw = 0
for o in bpy.data.objects:
    if o.name.startswith("TR_W_") and o.type == "MESH":
        k = int(o.data.name.rsplit("_", 1)[-1]) if o.data.name.startswith("TR_W_mesh_") else 0
        o["w6_old_mesh"] = o.data.name; o.data = NEW_TW[k]; ntw += 1
print("W6 bare trees", ntw, [len(m.polygons) for m in NEW_TW])

# ---------------- SD36 winter turf / SD38 footpath copies ----------------
for src, dst, m in (("G_PARK", "W6_TURF_PARK", TURF), ("G_PARK_NEAR", "W6_TURF_NEAR", TURF), ("PATH_SOUTH_FOOT", "W6_PATH_SOUTH", GRAVEL)):
    s = bpy.data.objects[src]; o = bpy.data.objects.new(dst, s.data); o.matrix_world = s.matrix_world.copy(); link(o)
    o.material_slots[0].link = "OBJECT"; o.material_slots[0].material = m

# ---------------- SD37 near sward (particle hair) ----------------
def sward():
    # covers both CP006 frusta out to ~55 m; blade density 1.0 up to y -56 m, fading to 0.3 at the far edge (y -22 m) so
    # the far edge of the hair is not a visible line (blades are sub-pixel there anyway)
    x0, x1, y0, y1, res = -50.0, 36.0, -76.9, -22.0, 0.5
    bm = bmesh.new(); nx = int((x1 - x0) / res) + 1; ny = int((y1 - y0) / res) + 1
    vs = [[bm.verts.new((x0 + i * res, y0 + j * res, gz(x0 + i * res, y0 + j * res) + 0.004)) for j in range(ny)] for i in range(nx)]
    for i in range(nx - 1):
        for j in range(ny - 1): bm.faces.new([vs[i][j], vs[i + 1][j], vs[i + 1][j + 1], vs[i][j + 1]])
    me = bpy.data.meshes.new("W6_SWARD"); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new("W6_SWARD", me); link(o)
    vg = o.vertex_groups.new(name="density")
    for v in me.vertices:
        y = v.co.y; xe = min(v.co.x - x0, x1 - v.co.x)
        w = 1.0 if y < -56.0 else max(0.3, 1.0 - 0.7 * (y + 56.0) / 34.0)
        w *= min(1.0, 0.4 + xe / 12.0)
        vg.add([v.index], w, "REPLACE")
    o.data.materials.append(TURF)
    hm, nt, b, _ = newmat("W6_SwardBlades1850")
    hi = nt.nodes.new("ShaderNodeHairInfo")
    c = ramp(nt, hi.outputs["Random"], [(0.0, (0.032, 0.055, 0.013)), (0.50, (0.070, 0.092, 0.022)), (0.80, (0.15, 0.13, 0.050)), (1.0, (0.22, 0.18, 0.080))])
    tipm = ramp(nt, hi.outputs["Intercept"], [(0.0, (0.45, 0.45, 0.45)), (1.0, (0.95, 0.92, 0.85))])
    mm = nt.nodes.new("ShaderNodeMix"); mm.data_type = "RGBA"; mm.blend_type = "MULTIPLY"; mm.inputs[0].default_value = 1.0
    nt.links.new(c, mm.inputs[6]); nt.links.new(tipm, mm.inputs[7]); nt.links.new(mm.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.75; o.data.materials.append(hm)
    mod = o.modifiers.new("sward", "PARTICLE_SYSTEM"); ps = mod.particle_system; st = ps.settings
    st.type = "HAIR"; st.count = 190000; st.use_advanced_hair = True; st.hair_length = 0.085
    st.emit_from = "FACE"; st.use_emit_random = True; st.distribution = "RAND"
    st.material = 2; st.hair_step = 4; st.display_step = 2; st.render_step = 3
    st.child_type = "INTERPOLATED"; st.child_percent = 2; st.rendered_child_count = 9
    st.child_length = 1.0; st.child_length_threshold = 0.0
    st.clump_factor = 0.0; st.roughness_1 = 0.03; st.roughness_1_size = 1.0; st.roughness_endpoint = 0.02; st.roughness_2 = 0.02
    st.length_random = 0.6 if hasattr(st, "length_random") else 0.0
    st.normal_factor = 0.021; st.factor_random = 0.008; st.tangent_factor = 0.0
    st.root_radius = 1.0; st.tip_radius = 0.0; st.radius_scale = 0.0025; st.use_close_tip = True
    st.child_radius = 0.6; st.kink = "NO"
    ps.seed = 1850; ps.vertex_group_density = "density"
    return st.count * st.rendered_child_count
print("W6 sward strands ~", sward())

# ---------------- SD40 survey kit (metres) ----------------
LINE_Y = -204.0 * FT                       # south building line, survey stretch (SD10)
PEG = 24.0 * FT
OAK = bpy.data.materials["GT_OakPeg"]
RED = flat("W6_PoleRed", (0.42, 0.06, 0.04), 0.6); WHT = flat("W6_PoleWhite", (0.70, 0.69, 0.64), 0.6)
IRN = flat("W6_Iron", (0.06, 0.06, 0.06), 0.45, 0.7); BRS = flat("W6_Brass", (0.50, 0.36, 0.14), 0.32, 0.9)
MAH = flat("W6_Mahogany", (0.16, 0.07, 0.04), 0.5); BLK = flat("W6_BlackLacquer", (0.02, 0.02, 0.022), 0.35)
STF = flat("W6_StaffWhite", (0.66, 0.64, 0.58), 0.7); BOOK = flat("W6_FieldBook", (0.18, 0.10, 0.06), 0.6)
def mk(name, build, mats):
    bm = bmesh.new(); build(bm); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    for p in me.polygons: p.use_smooth = True
    return link(bpy.data.objects.new(name, me))
def rodm(bm, a, b, r, seg, mi):
    n0 = len(bm.faces); tube(bm, Vector(a), Vector(b), r, r, seg)
    bm.faces.ensure_lookup_table()
    for f in bm.faces[n0:]: f.material_index = mi

def ranging_pole(bm, x, y, tilt=(0.0, 0.0)):
    z = gz(x, y); top = Vector((x + tilt[0], y + tilt[1], z + 8 * FT))
    base = Vector((x, y, z)); d = (top - base) / 8.0
    for k in range(8): rodm(bm, base + d * k, base + d * (k + 1), 0.016, 8, k % 2)
    rodm(bm, base - Vector((0, 0, 0.18)), base, 0.012, 6, 2)

TX = -PEG; TYL = LINE_Y                      # theodolite over the peg at -24 ft
def kit(bm):
    # ranging poles at the 0 ft peg (held by the boy) and the +48 ft peg; chaining arrows by the follower
    ranging_pole(bm, 0.12, LINE_Y + 0.05, (0.03, 0.0))
    ranging_pole(bm, 2 * PEG, LINE_Y)
    for k in range(3):
        x, y = -2.6 + 0.12 * k, LINE_Y + 0.55 + 0.05 * k; z = gz(x, y)
        rodm(bm, (x, y, z - 0.1), (x + 0.02, y, z + 0.32), 0.004, 4, 2)
        n0 = len(bm.faces); bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.03, radius2=0.03, depth=0.008,
                                                 matrix=Matrix.Translation((x + 0.02, y, z + 0.33)) @ Matrix.Rotation(math.pi / 2, 4, "X"))
        bm.faces.ensure_lookup_table()
        for f in bm.faces[n0:]: f.material_index = 2
mk("W6_SV_POLES", kit, [RED, WHT, IRN])

def theodolite(bm):
    z = gz(TX, TYL); head = Vector((TX, TYL, z + 1.36))
    for a in (90, 210, 330):
        r = math.radians(a); foot = Vector((TX + 0.52 * math.cos(r), TYL + 0.52 * math.sin(r), gz(TX + 0.52 * math.cos(r), TYL + 0.52 * math.sin(r)) - 0.03))
        rodm(bm, foot, head - Vector((0, 0, 0.03)), 0.017, 6, 0)
        rodm(bm, foot - Vector((0, 0, 0.06)), foot + (head - foot) * 0.06, 0.009, 5, 2)
    # tripod head, levelling plates, vertical axis, standards, horizontal circle, telescope (sighting east, +x)
    n0 = len(bm.faces); bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.075, radius2=0.075, depth=0.035, matrix=Matrix.Translation(head))
    bm.faces.ensure_lookup_table(); [setattr(f, "material_index", 0) for f in bm.faces[n0:]]
    for (zz, r, h, mi) in ((0.04, 0.06, 0.012, 1), (0.075, 0.075, 0.018, 1), (0.10, 0.035, 0.06, 1)):
        n0 = len(bm.faces); bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=r, radius2=r, depth=h, matrix=Matrix.Translation(head + Vector((0, 0, zz))))
        bm.faces.ensure_lookup_table(); [setattr(f, "material_index", mi) for f in bm.faces[n0:]]
    for s in (-1, 1):
        rodm(bm, head + Vector((0, s * 0.05, 0.11)), head + Vector((0, s * 0.05, 0.21)), 0.008, 6, 1)
    tz = head + Vector((0, 0, 0.215))
    rodm(bm, tz - Vector((0.17, 0, 0)), tz + Vector((0.20, 0, 0)), 0.021, 14, 3)
    rodm(bm, tz + Vector((0.20, 0, 0)), tz + Vector((0.23, 0, 0)), 0.026, 14, 1)
    rodm(bm, tz - Vector((0.20, 0, 0)), tz - Vector((0.17, 0, 0)), 0.014, 12, 1)
    rodm(bm, tz + Vector((-0.02, 0, -0.03)), tz + Vector((0.08, 0, -0.03)), 0.007, 8, 1)     # level tube under the telescope
mk("W6_SV_THEODOLITE", theodolite, [MAH, BRS, IRN, BLK])

def chain(bm):
    L_LINK = 7.92 * 0.0254; x0 = -3.05; y0 = LINE_Y + 0.42
    for k in range(100):
        xa, xb = x0 + k * L_LINK, x0 + (k + 1) * L_LINK
        ya = y0 + 0.10 * math.sin(k / 7.0); yb = y0 + 0.10 * math.sin((k + 1) / 7.0)
        rodm(bm, (xa, ya, gz(xa, ya) + 0.012), (xb, yb, gz(xb, yb) + 0.012), 0.0045, 4, 0)
        if k % 10 == 9:
            n0 = len(bm.faces); bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((xb, yb, gz(xb, yb) + 0.015)) @ Matrix.Diagonal((0.035, 0.03, 0.012, 1)))
            bm.faces.ensure_lookup_table(); [setattr(f, "material_index", 1) for f in bm.faces[n0:]]
    # handle at the follower's end, lifted to his hand
    rodm(bm, (x0, y0, gz(x0, y0) + 0.012), (x0 - 0.15, y0 - 0.05, gz(x0, y0) + 0.35), 0.006, 4, 0)
mk("W6_SV_CHAIN", chain, [IRN, BRS])

SX, SY = 2.35, LINE_Y + 0.65
def staff(bm):
    z = gz(SX, SY)
    for k in range(20):
        n0 = len(bm.faces); bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((SX, SY, z + 0.02 + (k + 0.5) * 0.1524)) @ Matrix.Diagonal((0.055, 0.03, 0.1524, 1)))
        bm.faces.ensure_lookup_table(); [setattr(f, "material_index", 0) for f in bm.faces[n0:]]
        for j in range(3):   # black graduations (tenths of a foot), alternating sides
            if (k + j) % 2: continue
            n0 = len(bm.faces); bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((SX + (0.012 if j % 2 else -0.012), SY - 0.0155, z + 0.02 + k * 0.1524 + 0.03 + j * 0.0457)) @ Matrix.Diagonal((0.026, 0.002, 0.03, 1)))
            bm.faces.ensure_lookup_table(); [setattr(f, "material_index", 1) for f in bm.faces[n0:]]
mk("W6_SV_STAFF", staff, [STF, BLK])

# ---------------- SD39 survey party: c9_figures_v2 1850 dress ----------------
def face_rz(dx, dy): return math.atan2(dx, -dy)       # figures face local -y
CAST = [  # name, role, palette, pose, H, hat, x, y, facing (dx, dy)
    ("W6_SVP_surveyor_theodolite", "engineer", "engineer", "working", 1.78, "top", TX - 0.62, TYL - 0.05, (1, 0.05)),
    ("W6_SVP_surveyor_fieldbook", "engineer", "foreman", "table", 1.74, "top", TX + 0.75, TYL + 1.35, (-0.55, -1.0)),
    ("W6_SVP_boy_pole", "workman", "workman_a", "hauling", 1.48, "cap", 0.38, LINE_Y + 0.25, (-1, -0.15)),
    ("W6_SVP_chainman_follower", "workman", "workman_b", "working", 1.73, "wide", -3.42, LINE_Y + 0.30, (1, 0.2)),
    ("W6_SVP_staffman", "workman", "workman_a", "standing", 1.75, "wide", SX + 0.24, SY + 0.10, (-1, -0.35)),
]
for i, (n, role, pal, pose, H, hat, x, y, fd) in enumerate(CAST):
    o = F.build_figure(n, role, H, pose, seed=40 + i, mats=F.palette(f"w6_{i}", pal), hat=hat); link(o)
    o.location = (x, y, gz(x, y)); o.rotation_euler = (0, 0, face_rz(*fd)); o["part_kind"] = "cp006_survey_figure"
    o[TAG] = f"c9_figures_v2 {role}/{pal} {pose} {hat} {H}"
    print("PERSON", n, role, pal, pose, hat, H, round(x, 2), round(y, 2))
# field book in the left hand of the field-book surveyor ('table' pose wrist at local (-0.17k, -0.27k, 0.565H))
fb = bpy.data.objects["W6_SVP_surveyor_fieldbook"]; k = 1.74 / 1.75
wl = fb.matrix_world @ Vector((-0.17 * k, -0.33 * k, 0.575 * 1.74))
def book(bm):
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(wl) @ fb.matrix_world.to_3x3().to_4x4() @ Matrix.Rotation(math.radians(-25), 4, "X") @ Matrix.Diagonal((0.10, 0.16, 0.018, 1)))
mk("W6_SV_FIELDBOOK", book, [BOOK])

# ---------------- grok_states: CP006 shows W6_, hides what it replaces ----------------
st = json.loads(bpy.data.texts["grok_states"].as_string())
c6 = st["CP006"]
for h in ("G_PARK", "PATH_SOUTH_FOOT", "SVP_", "SV_TOOL", "CPL_HorizonGround"):
    if h not in c6["hide"]: c6["hide"].append(h)
if "W6_" not in c6["show"]: c6["show"].append("W6_")
t = bpy.data.texts["grok_states"]; t.clear(); t.write(json.dumps(st, indent=1))
print("W6 states CP006", c6)

out = arg("--out") or os.path.join(ROOT, "rounds", "candidates", "s02_cp006park.blend")
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True); print("W6 SAVED", out)
