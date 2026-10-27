"""Hyde Park 1851 Crystal Palace: the central TRANSEPT (Grok Bot).

Scripted parametric build from Downes 1852 (Plates II, III, IV, VII, XVIII, XX, XXIV-XXVI and pages 15, 36-42, 50).
Same conventions as course-models/crystal-palace-1851-claude: metres, origin at the centre of the nave/transept
crossing at floor level, X east along the length, Y north across the width, Z up. Hyde Park only.

Run:  blender -b -P build_transept.py -- --out ../rounds/r01.blend [--milestones DIR] [--colour neutral|owen]
"""
import bpy, bmesh, math, random, sys, os, json
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default
OUT = arg("--out", "/tmp/transept.blend")
MILESTONES = arg("--milestones")
COLOUR = arg("--colour", "neutral")
SEED = int(arg("--seed", "1851"))

FT = 0.3048
def ft(f, i=0.0): return (f + i / 12.0) * FT
def inch(i): return i / 12.0 * FT

# ---------------- parameters (feet unless noted) ----------------
GRID = 24.0
Y_HALF = 204.0                    # 408 ft main block
GIRDER_TOP = [22 + 2/12, 42 + 2/12, 62 + 2/12]      # D11a-c
GIRDER_D = 3.0                    # D10a
COL_D_IN = 8.0                    # D13
COL_TOP1 = 18 + 11.75/12          # D14
CONN_L = 3.375                    # D15
GALLERY_TOP = 22 + 11/12          # D12
GALLERY_T = 0.75
SPRING = 65.0                     # vault springing axis (inferred, see DEPARTURES)
R_EXT = 74 + 4/12                 # D20 extrados diameter
R_EXT = R_EXT / 2.0               # 37.1667
RIB_A_D, RIB_A_W = 1.5, 8/12      # D20 section 1 ft 6 in x 8 in
RIB_B_D, RIB_B_W = 0.75, 8/12     # intermediate rib (OCR "4 in deep", read as 9 in; inferred)
RIB_B_PITCH = 8.0
RIDGE_RISE = 0.9                  # glazing ridge above the rib extrados (inferred)
TRUSS72_D = 6.0                   # D19b
TRUSS72_FACE = 71.2               # D19a, face to face
LEADFLAT_T = 0.75
VOID_S, VOID_N = -156.0, 180.0    # transept gallery void ends (Plate II "48.0" south; 24 ft north)
X_T = 36.0; X_LF = 60.0; X_ARM = 132.0
NAVE = 36.0

random.seed(SEED)

# ---------------- scene reset ----------------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'; scene.unit_settings.scale_length = 1.0

def coll(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or scene.collection).children.link(c)
    return c
ROOT = coll("TRANSEPT_GROK")
C = {n: coll(n, ROOT) for n in ["COLUMNS", "GIRDERS", "TRUSSES", "VAULT_RIBS", "VAULT_GLASS", "VAULT_BRACING",
                                "LEAD_FLATS", "ROOFS", "GALLERIES", "RAILINGS", "END_SCREENS", "WALLS", "FLOOR",
                                "ELMS", "GROUND"]}
LIB = bpy.data.collections.new("LIB_GROK")   # unlinked library of shared meshes

# ---------------- materials ----------------
def mat_principled(name, rgb, rough=0.6, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    m.diffuse_color = (*rgb, 1)
    return m

def mat_glass(name, tint=(0.88, 0.95, 0.93), bars=True, ridge=False):
    """Thin sheet glass: fresnel-weighted gloss over a tinted transparent, shadow rays pass (so sun reaches the
    floor), optional procedural diagonal sash-bar lines from the UVs (1 UV unit = 1 ft)."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; n = nt.nodes; l = nt.links
    for x in list(n): n.remove(x)
    out = n.new("ShaderNodeOutputMaterial")
    tr = n.new("ShaderNodeBsdfTransparent"); tr.inputs[0].default_value = (*tint, 1)
    gl = n.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.04
    fr = n.new("ShaderNodeFresnel"); fr.inputs["IOR"].default_value = 1.52
    mx = n.new("ShaderNodeMixShader"); l.new(fr.outputs[0], mx.inputs[0]); l.new(tr.outputs[0], mx.inputs[1]); l.new(gl.outputs[0], mx.inputs[2])
    # a faint milky scatter so the glass reads as a surface (period sheet glass was not optically clear)
    df = n.new("ShaderNodeBsdfDiffuse"); df.inputs[0].default_value = (0.9, 0.93, 0.92, 1)
    mx2 = n.new("ShaderNodeMixShader"); mx2.inputs[0].default_value = 0.06; l.new(mx.outputs[0], mx2.inputs[1]); l.new(df.outputs[0], mx2.inputs[2])
    last = mx2.outputs[0]
    if bars:
        uv = n.new("ShaderNodeTexCoord"); sep = n.new("ShaderNodeSeparateXYZ"); l.new(uv.outputs["UV"], sep.inputs[0])
        mul = n.new("ShaderNodeMath"); mul.operation = 'MULTIPLY'
        if ridge:   # EX27/RL05: Paxton sash bars run down the slope, square to the ridge (X), at 10.5 in (0.875 ft) centres
            mul.inputs[1].default_value = 1 / 0.875; l.new(sep.outputs[0], mul.inputs[0]); thr = 0.12   # ~1.25 in bar / 10.5 in
        else:       # legacy diagonal mask (vault / sash glazing)
            add = n.new("ShaderNodeMath"); add.operation = 'ADD'; l.new(sep.outputs[0], add.inputs[0]); l.new(sep.outputs[1], add.inputs[1])
            mul.inputs[1].default_value = 1 / 0.85; l.new(add.outputs[0], mul.inputs[0]); thr = 0.07
        frc = n.new("ShaderNodeMath"); frc.operation = 'FRACT'; l.new(mul.outputs[0], frc.inputs[0])
        lt = n.new("ShaderNodeMath"); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = thr; l.new(frc.outputs[0], lt.inputs[0])
        bar = n.new("ShaderNodeBsdfDiffuse"); bar.inputs[0].default_value = (0.82, 0.8, 0.74, 1)
        mx3 = n.new("ShaderNodeMixShader"); l.new(lt.outputs[0], mx3.inputs[0]); l.new(last, mx3.inputs[1]); l.new(bar.outputs[0], mx3.inputs[2])
        last = mx3.outputs[0]
    l.new(last, out.inputs[0])
    m.blend_method = 'BLEND' if hasattr(m, "blend_method") else None
    m.diffuse_color = (*tint, 0.3)
    return m

OJ_BLUE, OJ_RED, OJ_YELLOW, OJ_WHITE = (0.13, 0.25, 0.58), (0.58, 0.05, 0.04), (0.86, 0.62, 0.12), (0.86, 0.86, 0.82)
def oj_material(name, mode):
    """Owen Jones 1851 scheme (see DEPARTURES OJ rows): primaries separated by white; blue on the large and
    concave surfaces, yellow on the convex, red only on the undersides. mode: 'column' (vertical stripes round the
    shaft, by angle in object space), 'girder' (red underside by normal, yellow top chord, blue faces), 'plain' (blue)."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; n = nt.nodes; l = nt.links; b = n["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.5
    def rgb(c):
        r = n.new("ShaderNodeRGB"); r.outputs[0].default_value = (*c, 1); return r.outputs[0]
    def mix(fac, a, c):
        x = n.new("ShaderNodeMix"); x.data_type = 'RGBA'; l.new(fac, x.inputs["Factor"]); l.new(a, x.inputs["A"]); l.new(c, x.inputs["B"]); return x.outputs["Result"]
    def math_(op, a, v=None, a2=None):
        x = n.new("ShaderNodeMath"); x.operation = op
        l.new(a, x.inputs[0])
        if a2 is not None: l.new(a2, x.inputs[1])
        elif v is not None: x.inputs[1].default_value = v
        return x.outputs[0]
    tc = n.new("ShaderNodeTexCoord"); sep = n.new("ShaderNodeSeparateXYZ"); l.new(tc.outputs["Object"], sep.inputs[0])
    geo = n.new("ShaderNodeNewGeometry"); sn = n.new("ShaderNodeSeparateXYZ"); l.new(geo.outputs["Normal"], sn.inputs[0])
    if mode == "column":
        ang = math_('ARCTAN2', sep.outputs[1], a2=sep.outputs[0])
        k = math_('FRACT', math_('MULTIPLY', ang, 8 / (2 * math.pi)))      # 8 stripes round the shaft
        # stripe sequence per quarter: blue (wide), white, yellow, white
        is_white1 = math_('LESS_THAN', math_('ABSOLUTE', math_('SUBTRACT', k, 0.5)), 0.08)
        q = math_('FRACT', math_('MULTIPLY', ang, 4 / (2 * math.pi)))
        is_yel = math_('GREATER_THAN', q, 0.5)
        c = mix(is_yel, rgb(OJ_BLUE), rgb(OJ_YELLOW))
        c = mix(is_white1, c, rgb(OJ_WHITE))
        down = math_('LESS_THAN', sn.outputs[2], -0.5)
        c = mix(down, c, rgb(OJ_RED))
    elif mode == "girder":
        top = math_('GREATER_THAN', sep.outputs[2], -inch(3.2))
        down = math_('LESS_THAN', sn.outputs[2], -0.5)
        c = mix(top, rgb(OJ_BLUE), rgb(OJ_YELLOW))
        c = mix(down, c, rgb(OJ_RED))
    else:
        down = math_('LESS_THAN', sn.outputs[2], -0.5)
        c = mix(down, rgb(OJ_BLUE), rgb(OJ_RED))
    l.new(c, b.inputs["Base Color"]); m.diffuse_color = (*OJ_BLUE, 1)
    return m
if COLOUR == "owen":
    IRON = oj_material("GT_Iron_OJ", "plain")
    IRON_COL = oj_material("GT_IronColumn_OJ", "column")
    IRON_GIR = oj_material("GT_IronGirder_OJ", "girder")
else:                  # neutral, to sit beside Claude's preview frame
    IRON = mat_principled("GT_Iron", (0.80, 0.80, 0.77), 0.55)
    IRON_COL = IRON_GIR = IRON
FAN = mat_principled("GT_FanIron", (0.018, 0.02, 0.02), 0.65)   # r10 L03: near-black like Talbot (was 0.10) if COLOUR != "owen" else oj_material("GT_Fan_OJ", "plain")
WOOD = mat_principled("GT_Timber", (0.72, 0.66, 0.56), 0.7)
WOODDARK = mat_principled("GT_Boarding", (0.62, 0.55, 0.45), 0.8)
LEAD = mat_principled("GT_Lead", (0.42, 0.44, 0.46), 0.5, 0.3)
GLASS = mat_glass("GT_Glass")
GLASS_PLAIN = mat_glass("GT_GlassPlain", tint=(0.62, 0.68, 0.68), bars=False)
GLASS_END = mat_glass("GT_GlassEndScreen", tint=(0.30, 0.34, 0.34), bars=False)   # r09 L02 / r10 L03: darker so the fan reads
for _n in GLASS_END.node_tree.nodes:          # r10 L03: the sunlit milky veil turned the lunette pale; much less of it on the end screen
    if _n.type == 'BSDF_DIFFUSE': _n.inputs[0].default_value = (0.30, 0.31, 0.31, 1)
BARK = mat_principled("GT_Bark", (0.075, 0.065, 0.055), 0.95)
GRASS = mat_principled("GT_Grass", (0.16, 0.24, 0.08), 0.9)

def leaf_material():
    m = bpy.data.materials.new("GT_ElmLeaf"); m.use_nodes = True
    nt = m.node_tree; n = nt.nodes; l = nt.links
    b = n["Principled BSDF"]
    oi = n.new("ShaderNodeObjectInfo"); ramp = n.new("ShaderNodeValToRGB")
    noise = n.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 0.6
    ramp.color_ramp.elements[0].color = (0.035, 0.065, 0.015, 1); ramp.color_ramp.elements[1].color = (0.13, 0.19, 0.045, 1)
    l.new(noise.outputs["Fac"], ramp.inputs[0]); l.new(ramp.outputs[0], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.7
    try:
        b.inputs["Subsurface Weight"].default_value = 0.0
        b.inputs["Transmission Weight"].default_value = 0.0
    except KeyError:
        pass
    # leaf-card cutout: a rounded lozenge in UV space with a few notches, so cards read as small leaf sprays
    tc = n.new("ShaderNodeTexCoord"); sep = n.new("ShaderNodeSeparateXYZ"); l.new(tc.outputs["UV"], sep.inputs[0])
    vor = n.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 3.0; l.new(tc.outputs["UV"], vor.inputs["Vector"])
    lt = n.new("ShaderNodeMath"); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.42
    l.new(vor.outputs["Distance"], lt.inputs[0]); l.new(lt.outputs[0], b.inputs["Alpha"])
    m.diffuse_color = (0.08, 0.13, 0.03, 1)
    return m
LEAF = leaf_material()
FLOORM = mat_principled("GT_FloorBoards", (0.55, 0.46, 0.35), 0.85)
def floor_boards(m):
    nt = m.node_tree; n = nt.nodes; l = nt.links; b = n["Principled BSDF"]
    tc = n.new("ShaderNodeTexCoord"); sep = n.new("ShaderNodeSeparateXYZ"); l.new(tc.outputs["Object"], sep.inputs[0])
    mul = n.new("ShaderNodeMath"); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 1 / inch(9.5)   # 9 in boards + 1/2 in gap
    l.new(sep.outputs[0], mul.inputs[0])
    frc = n.new("ShaderNodeMath"); frc.operation = 'FRACT'; l.new(mul.outputs[0], frc.inputs[0])
    gt = n.new("ShaderNodeMath"); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 9.0 / 9.5; l.new(frc.outputs[0], gt.inputs[0])
    mix = n.new("ShaderNodeMix"); mix.data_type = 'RGBA'
    mix.inputs["A"].default_value = (0.58, 0.49, 0.37, 1); mix.inputs["B"].default_value = (0.05, 0.04, 0.03, 1)
    l.new(gt.outputs[0], mix.inputs["Factor"]); l.new(mix.outputs["Result"], b.inputs["Base Color"])
floor_boards(FLOORM)

# ---------------- mesh helpers ----------------
def new_obj(name, me, coll_, loc=(0, 0, 0), rot_z=0.0, props=None):
    ob = bpy.data.objects.new(name, me)
    ob.location = loc; ob.rotation_euler = (0, 0, rot_z)
    coll_.objects.link(ob)
    for k, v in (props or {}).items(): ob[k] = v
    return ob

def bm_box(bm, x0, x1, y0, y1, z0, z1):
    vs = [bm.verts.new(v) for v in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]]
    for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:
        bm.faces.new([vs[i] for i in f])

def bm_bar(bm, a, b, w, t):
    """square-ish bar from point a to b (metres), width w (horizontal-ish), thickness t."""
    a = Vector(a); b = Vector(b); d = (b - a)
    L = d.length
    if L < 1e-6: return
    d.normalize()
    up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0))
    s = d.cross(up).normalized(); u = s.cross(d).normalized()
    pts = []
    for p in (a, b):
        for (i, j) in [(-1,-1),(1,-1),(1,1),(-1,1)]:
            pts.append(bm.verts.new(p + s * (i * w / 2) + u * (j * t / 2)))
    for f in [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]:
        bm.faces.new([pts[i] for i in f])

def bm_cyl(bm, r, z0, z1, seg=16, cx=0, cy=0):
    bot = [bm.verts.new((cx + r*math.cos(2*math.pi*k/seg), cy + r*math.sin(2*math.pi*k/seg), z0)) for k in range(seg)]
    top = [bm.verts.new((cx + r*math.cos(2*math.pi*k/seg), cy + r*math.sin(2*math.pi*k/seg), z1)) for k in range(seg)]
    for k in range(seg):
        bm.faces.new([bot[k], bot[(k+1)%seg], top[(k+1)%seg], top[k]])
    bm.faces.new(list(reversed(bot))); bm.faces.new(top)

def finish(bm, name, mat, mats=None):
    me = bpy.data.meshes.new(name)
    bm.normal_update(); bm.to_mesh(me); bm.free()
    me.materials.append(mat)
    for m in (mats or []): me.materials.append(m)
    for p in me.polygons: p.use_smooth = False
    return me

# ---------------- part library ----------------
def mesh_column(top_ft, with_seat=False):
    """A full-height column (shafts + connecting pieces) from the floor to the top of the given tier."""
    bm = bmesh.new(); r = inch(COL_D_IN) / 2
    tiers = [t for t in GIRDER_TOP if t <= top_ft + 1e-6]
    z = 0.0
    # base flare
    bm_cyl(bm, r * 1.6, 0, ft(1.0), 16)
    for t in tiers:
        cp0 = t - GIRDER_D - 0.1875; cp1 = t + 0.1875          # connecting piece stands 2 1/4 in proud (D15/D18)
        bm_cyl(bm, r, ft(z), ft(cp0), 16)
        bm_box(bm, -inch(5.5), inch(5.5), -inch(5.5), inch(5.5), ft(cp0), ft(cp1))
        bm_cyl(bm, r * 1.25, ft(cp0 - 0.6), ft(cp0), 16)      # capital ring
        z = cp1
    if with_seat:     # transept columns carry the arched ribs to the springing (Plate VIII Figs. 9-10, p. 37)
        bm_cyl(bm, r, ft(z), ft(SPRING), 16)
        bm_box(bm, -inch(7), inch(7), -inch(7), inch(7), ft(SPRING - 0.8), ft(SPRING))
    return finish(bm, f"col_{int(top_ft)}{'_seat' if with_seat else ''}", IRON_COL)

def mesh_girder(span_ft, depth_ft, panel_ft, name):
    """Trellis girder along +X centred on 0, top at z=0 (place at the girder top)."""
    bm = bmesh.new(); L = span_ft; face = L - 0.729 if span_ft == 24 else L
    x0, x1 = ft(-face/2), ft(face/2); D = ft(depth_ft); t = inch(3.5); w = inch(4)
    bm_box(bm, x0, x1, -w/2, w/2, -inch(3), 0)              # top flange
    bm_box(bm, x0, x1, -w/2, w/2, -D, -D + inch(3))         # bottom flange
    n = max(1, round(L / panel_ft))
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        bm_box(bm, x - inch(1.5), x + inch(1.5), -inch(1), inch(1), -D, 0)
    for k in range(n):
        xa = x0 + (x1 - x0) * k / n; xb = x0 + (x1 - x0) * (k + 1) / n
        bm_bar(bm, (xa, 0, -D + inch(3)), (xb, 0, -inch(3)), inch(1.5), inch(1.0))
        bm_bar(bm, (xa, 0, -inch(3)), (xb, 0, -D + inch(3)), inch(1.5), inch(1.0))
    return finish(bm, name, IRON_GIR)

LIBM = {
    "col1": mesh_column(GIRDER_TOP[0]), "col2": mesh_column(GIRDER_TOP[1]),
    "col3": mesh_column(GIRDER_TOP[2]), "col3seat": mesh_column(GIRDER_TOP[2], True),
    "g24": mesh_girder(24, GIRDER_D, 8, "girder24"),
    "t72": mesh_girder(TRUSS72_FACE, TRUSS72_D, 8, "truss72"),
    "t72g": mesh_girder(72, 3.0, 8, "truss72_gallery"),
}

# ---------------- plan ----------------
ROWS_Y = [-Y_HALF + GRID * j for j in range(18)]
X_LINES = [-132, -108, -84, -60, -36, 36, 60, 84, 108, 132]
def top_tier(x, y):
    """Highest tier reached by the column at (x, y) in the transept block (Plate III: cross-shaped tier 3)."""
    ax = abs(x)
    if ax <= X_LF: return 3
    if ax <= X_ARM: return 3 if abs(y) <= 60 else 2
    return 1

parts = []  # (name, kind, props) for the signature/report
def place(meshkey, name, coll_, x, y, z, rot=0.0, **props):
    ob = new_obj(name, LIBM[meshkey], coll_, (ft(x), ft(y), ft(z)), rot, dict(props))
    parts.append(name); return ob

cols = {}
for x in X_LINES:
    for y in ROWS_Y:
        if abs(y) < NAVE and abs(x) <= X_ARM:     # nave void: no columns inside the 72 ft nave
            continue
        if abs(x) > X_LF and abs(y) < 60:         # nave tier-3 strip outside the transept: Claude's / east half
            continue
        t = top_tier(x, y)
        key = "col3seat" if abs(x) == X_T else f"col{t}"
        place(key, f"COL_X{x:+04d}_Y{int(y):+04d}", C["COLUMNS"], x, y, 0, part_kind="column", tier=t,
              claude_line37=(x == -36))
        cols[(x, y)] = t
# end-wall intermediate columns at x = +-12 (Plate VII: four columns across the 72 ft end; Plate II dots at the
# south void end y=-156) -- full height at the ends, tier 1 at y=-156 and y=-180
for x in (-12, 12):
    for y in (-Y_HALF, Y_HALF):
        place("col3", f"COL_END_X{x:+04d}_Y{int(y):+04d}", C["COLUMNS"], x, y, 0, part_kind="column", tier=3); cols[(x, y)] = 3
    for y in (-180, VOID_S):
        place("col1", f"COL_XGAL_X{x:+04d}_Y{int(y):+04d}", C["COLUMNS"], x, y, 0, part_kind="column", tier=1); cols[(x, y)] = 1

# girders between neighbouring columns that both reach a tier
def gird_between(a, b, along):
    ta, tb = cols.get(a), cols.get(b)
    if not ta or not tb: return
    for k in range(min(ta, tb)):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        place("g24", f"GIR_T{k+1}_{along}_{mx:+.0f}_{my:+.0f}", C["GIRDERS"], mx, my, GIRDER_TOP[k],
              math.pi / 2 if along == "Y" else 0.0, part_kind="girder", tier=k + 1, span_ft=24)
keys = set(cols)
for (x, y) in keys:
    if (x, y + 24) in keys: gird_between((x, y), (x, y + 24), "Y")
    for dx in (24,):
        if (x + dx, y) in keys: gird_between((x, y), (x + dx, y), "X")
# the transept void lines 36 -> 60 are 24 ft apart along X: handled by dx=24. 36 <-> -36 has no girder (open span).

# 72 ft trusses across the nave (Plate XX; p. 39): strong under the arched ribs at x=+-36, light under the outer
# edge of the lead flats at x=+-60. Top at the tier-3 girder top.
for x, kind in ((-36, "strong"), (36, "strong"), (-60, "light"), (60, "light")):
    place("t72", f"TRUSS72_{kind}_X{x:+04d}", C["TRUSSES"], x, 0, GIRDER_TOP[2], math.pi / 2,
          part_kind="truss", span_ft=72, strength=kind)
# 72 ft gallery-level trusses across the transept carrying the north cross gallery at y=180 (inferred: Plate II
# shows no intermediate columns there) and the end walls' tier girders across the 72 ft at both ends are 24 ft girders
# on the x=+-12 end columns (Plate VII).
place("t72g", "TRUSS72_GAL_N", C["TRUSSES"], 0, VOID_N, GIRDER_TOP[0], 0.0, part_kind="gallery_truss", span_ft=72)
for y in (-Y_HALF, Y_HALF):
    for x0, x1 in ((-36, -12), (-12, 12), (12, 36)):
        for k in range(3):
            place("g24", f"GIR_END_T{k+1}_{(x0+x1)//2:+d}_{int(y):+d}", C["GIRDERS"], (x0 + x1) / 2, y, GIRDER_TOP[k],
                  0.0, part_kind="girder", tier=k + 1, span_ft=24)
for y in (-180, VOID_S):
    for x0, x1 in ((-36, -12), (-12, 12), (12, 36)):
        place("g24", f"GIR_XGAL_{(x0+x1)//2:+d}_{int(y):+d}", C["GIRDERS"], (x0 + x1) / 2, y, GIRDER_TOP[0],
              0.0, part_kind="girder", tier=1, span_ft=24)
for x in (-12, 12):
    for y0, y1 in ((-204, -180), (-180, -156)):
        place("g24", f"GIR_XGALY_{x:+d}_{(y0+y1)//2:+d}", C["GIRDERS"], x, (y0 + y1) / 2, GIRDER_TOP[0],
              math.pi / 2, part_kind="girder", tier=1, span_ft=24)

if MILESTONES:
    os.makedirs(MILESTONES, exist_ok=True)

# ---------------- vault ----------------
SEG = 72
def arc_pts(r, n=SEG):
    return [(r * math.cos(math.pi * k / n), r * math.sin(math.pi * k / n)) for k in range(n + 1)]

def mesh_rib(depth, width, name, ext=R_EXT):
    """Arched rib in the XZ plane centred on x=0, springing axis at z=0; extrados radius ext."""
    bm = bmesh.new(); ri = ft(ext - depth); ro = ft(ext); hw = ft(width) / 2
    rings = []
    for k in range(SEG + 1):
        a = math.pi * k / SEG; c, s = math.cos(a), math.sin(a)
        rings.append([bm.verts.new((ri*c, -hw, ri*s)), bm.verts.new((ro*c, -hw, ro*s)),
                      bm.verts.new((ro*c, hw, ro*s)), bm.verts.new((ri*c, hw, ri*s))])
    for k in range(SEG):
        A, B = rings[k], rings[k + 1]
        for i in range(4):
            bm.faces.new([A[i], A[(i+1)%4], B[(i+1)%4], B[i]])
    bm.faces.new(rings[0]); bm.faces.new(list(reversed(rings[-1])))
    return finish(bm, name, WOOD)
LIBM["ribA"] = mesh_rib(RIB_A_D, RIB_A_W, "rib_A")
LIBM["ribB"] = mesh_rib(RIB_B_D, RIB_B_W, "rib_B")

def mesh_vault_glass(bay_ft):
    """Ridge-and-furrow glazing for one rib-to-rib bay along Y (0..bay), following the arc: gutters on the ribs,
    a ridge in the middle RIDGE_RISE above the extrados. UV in feet (u along the arc, v along Y)."""
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    r0 = ft(R_EXT); r1 = ft(R_EXT + RIDGE_RISE)
    ys = [0, bay_ft / 2, bay_ft]; rs = [r0, r1, r0]
    grid = []
    for k in range(SEG + 1):
        a = math.pi * k / SEG
        grid.append([bm.verts.new((rs[i]*math.cos(a), ft(ys[i]), rs[i]*math.sin(a))) for i in range(3)])
    for k in range(SEG):
        for i in range(2):
            f = bm.faces.new([grid[k][i], grid[k][i+1], grid[k+1][i+1], grid[k+1][i]])
            for lp in f.loops:
                kk = k if lp.vert in (grid[k][i], grid[k][i+1]) else k + 1
                ii = i if lp.vert in (grid[k][i], grid[k+1][i]) else i + 1
                lp[uvl].uv = (R_EXT * math.pi * kk / SEG, ys[ii] if i == 0 else bay_ft - ys[ii])
    me = finish(bm, f"vault_glass_{bay_ft}", GLASS)
    return me
LIBM["vglass"] = mesh_vault_glass(RIB_B_PITCH)

def mesh_ridge(bay_ft):
    bm = bmesh.new(); pts = arc_pts(ft(R_EXT + RIDGE_RISE))
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        bm_bar(bm, (x0, ft(bay_ft/2), z0), (x1, ft(bay_ft/2), z1), inch(3), inch(4))
    return finish(bm, "vault_ridge", WOOD)
LIBM["vridge"] = mesh_ridge(RIB_B_PITCH)

ys_rib = [-Y_HALF + RIB_B_PITCH * k for k in range(int(2 * Y_HALF / RIB_B_PITCH) + 1)]
for y in ys_rib:
    main = abs((y + Y_HALF) % GRID) < 1e-6
    place("ribA" if main else "ribB", f"RIB_{'A' if main else 'B'}_Y{y:+06.0f}", C["VAULT_RIBS"], 0, y, SPRING,
          part_kind="vault_rib" if main else "vault_rib_b", rib=("A" if main else "B"),
          on_truss=(main and abs(y) == 12))
for y in ys_rib[:-1]:
    place("vglass", f"VGLASS_Y{y:+06.0f}", C["VAULT_GLASS"], 0, y, SPRING, part_kind="vault_glass")
    place("vridge", f"VRIDGE_Y{y:+06.0f}", C["VAULT_GLASS"], 0, y, SPRING, part_kind="vault_ridge")

# purlins (c c) and diagonal bracing: six crosses in each bay (p. 36)
bm = bmesh.new()
NP = 7; rp = ft(R_EXT - RIB_A_D - 0.25)
angs = [math.pi * k / (NP + 1) for k in range(1, NP + 1)]
for a in angs:
    bm_box(bm, rp*math.cos(a) - inch(3), rp*math.cos(a) + inch(3), ft(-Y_HALF), ft(Y_HALF), rp*math.sin(a) - inch(4), rp*math.sin(a) + inch(4))
pur = finish(bm, "vault_purlins", WOOD)
new_obj("VAULT_PURLINS", pur, C["VAULT_BRACING"], (0, 0, ft(SPRING)), props={"part_kind": "vault_purlin"})
bm = bmesh.new(); rb = ft(R_EXT - RIB_A_D - 0.05)
allang = [0.0] + angs + [math.pi]
for j in range(17):
    y0, y1 = ft(-Y_HALF + 24 * j), ft(-Y_HALF + 24 * (j + 1))
    for a0, a1 in zip(angs, angs[1:]):
        p = lambda a, y: (rb*math.cos(a), y, rb*math.sin(a))
        bm_bar(bm, p(a0, y0), p(a1, y1), inch(1), inch(1)); bm_bar(bm, p(a1, y0), p(a0, y1), inch(1), inch(1))
brc = finish(bm, "vault_bracing", IRON)
new_obj("VAULT_BRACING", brc, C["VAULT_BRACING"], (0, 0, ft(SPRING)), props={"part_kind": "vault_bracing"})

# lead flats either side of the vault (Plates XVIII-XIX): 24 ft strips at the tier-3 girder top
for s in (-1, 1):
    bm = bmesh.new()
    xa, xb = sorted((s * (R_EXT + 0.1), s * X_LF))
    bm_box(bm, ft(xa), ft(xb), ft(-Y_HALF), ft(Y_HALF), 0, ft(LEADFLAT_T))
    new_obj(f"LEADFLAT_{'W' if s < 0 else 'E'}", finish(bm, "leadflat", LEAD), C["LEAD_FLATS"],
            (0, 0, ft(GIRDER_TOP[2])), props={"part_kind": "lead_flat"})
    # louvre band between the lead flat and the springing (space J, Plate XVIII)
    bm = bmesh.new(); x = s * (R_EXT - RIB_A_D / 2)
    z0, z1 = GIRDER_TOP[2] + LEADFLAT_T, SPRING
    nl = 4
    for k in range(nl):
        zz = z0 + (z1 - z0) * (k + 0.5) / nl
        bm_box(bm, ft(x) - inch(0.5), ft(x) + inch(0.5), ft(-Y_HALF), ft(Y_HALF), ft(zz) - inch(2.5), ft(zz) + inch(2.5))
    new_obj(f"LOUVRES_VAULT_{'W' if s < 0 else 'E'}", finish(bm, "louvres", IRON), C["LEAD_FLATS"], props={"part_kind": "louvre"})
    # timber sill (u, Plate XXVI) the ribs bear on along the side
    bm = bmesh.new(); bm_box(bm, ft(s*36) - inch(6), ft(s*36) + inch(6), ft(-Y_HALF), ft(Y_HALF), ft(SPRING - 1.0), ft(SPRING))
    new_obj(f"SILL_{'W' if s < 0 else 'E'}", finish(bm, "sill", WOOD), C["LEAD_FLATS"], props={"part_kind": "sill"})

# ---------------- flat ridge-and-furrow roofs of the tier-2 arms (60..132, |y| 60..204) ----------------
ROOFGLASS_T = mat_glass("GT_RoofGlass", ridge=True)   # RL05: ridge-normal bars at 10.5 in
def mesh_roof_unit():
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    L = ft(24); W = ft(8); rise = ft(1.6)
    v = [bm.verts.new(p) for p in [(-L/2, -W/2, 0), (L/2, -W/2, 0), (L/2, 0, rise), (-L/2, 0, rise),
                                   (-L/2, W/2, 0), (L/2, W/2, 0)]]
    for f in ([v[0], v[1], v[2], v[3]], [v[3], v[2], v[5], v[4]]):
        ff = bm.faces.new(f)
        for lp in ff.loops: lp[uvl].uv = (lp.vert.co.x / FT, lp.vert.co.y / FT * 1.3)
    return finish(bm, "roof_unit", ROOFGLASS_T)
LIBM["roof"] = mesh_roof_unit()
for sx in (-1, 1):
    for xb in (72, 96, 120):
        for y in [60 + 4 + 8 * k for k in range(18)]:
            for sy in (-1, 1):
                place("roof", f"ROOF2_{sx*xb:+d}_{sy*y:+d}", C["ROOFS"], sx * xb, sy * y, GIRDER_TOP[1], part_kind="roof", tier=2)

# ---------------- galleries ----------------
def slab(name, x0, x1, y0, y1, z_top, t, mat, coll_, **props):
    bm = bmesh.new(); bm_box(bm, ft(x0), ft(x1), ft(y0), ft(y1), ft(z_top - t), ft(z_top))
    return new_obj(name, finish(bm, name, mat), coll_, props=props)
for s in (-1, 1):
    xa, xb = sorted((s * X_T, s * X_LF))
    slab(f"GAL_SIDE_{s:+d}_N", xa, xb, NAVE, Y_HALF, GALLERY_TOP, GALLERY_T, WOOD, C["GALLERIES"], part_kind="gallery_floor")
    slab(f"GAL_SIDE_{s:+d}_S", xa, xb, -Y_HALF, -NAVE, GALLERY_TOP, GALLERY_T, WOOD, C["GALLERIES"], part_kind="gallery_floor")
slab("GAL_CROSS_N", -X_T, X_T, VOID_N, Y_HALF, GALLERY_TOP, GALLERY_T, WOOD, C["GALLERIES"], part_kind="gallery_floor", sample="cross_n")
slab("GAL_CROSS_S", -X_T, X_T, -Y_HALF, VOID_S, GALLERY_TOP, GALLERY_T, WOOD, C["GALLERIES"], part_kind="gallery_floor", sample="cross_s")

def mesh_railing(length_ft):
    bm = bmesh.new(); L = ft(length_ft); H = ft(3.06)
    bm_box(bm, -L/2, L/2, -inch(1.5), inch(1.5), 0, inch(5.7))
    bm_box(bm, -L/2, L/2, -inch(1.5), inch(1.5), H - inch(4), H)
    n = int(length_ft / 1.5)
    for k in range(n):
        xa = -L/2 + L * k / n; xb = -L/2 + L * (k + 1) / n
        bm_bar(bm, (xa, 0, inch(5.7)), (xb, 0, H - inch(4)), inch(0.8), inch(0.6))
        bm_bar(bm, (xb, 0, inch(5.7)), (xa, 0, H - inch(4)), inch(0.8), inch(0.6))
    for k in range(int(length_ft / 6) + 1):
        x = -L/2 + ft(6 * k)
        bm_box(bm, x - inch(1.2), x + inch(1.2), -inch(1.2), inch(1.2), 0, H + inch(2))
    return finish(bm, f"railing{length_ft}", IRON)
LIBM["rail24"] = mesh_railing(24)
def rail_run(x0, y0, x1, y1, tag):
    L = math.hypot(x1 - x0, y1 - y0); n = max(1, round(L / 24))
    for k in range(n):
        xa = x0 + (x1 - x0) * (k + 0.5) / n; ya = y0 + (y1 - y0) * (k + 0.5) / n
        place("rail24", f"RAIL_{tag}_{k}", C["RAILINGS"], xa, ya, GALLERY_TOP,
              math.pi / 2 if abs(x1 - x0) < 1e-6 else 0.0, part_kind="balustrade")
for s in (-1, 1):
    rail_run(s * X_T, NAVE, s * X_T, VOID_N, f"T{s:+d}N")
    rail_run(s * X_T, VOID_S, s * X_T, -NAVE, f"T{s:+d}S")
    for sy in (-1, 1):
        xa, xb = sorted((s * X_T, s * X_LF))
        rail_run(xa, sy * NAVE, xb, sy * NAVE, f"NV{s:+d}{sy:+d}")
rail_run(-X_T, VOID_N, X_T, VOID_N, "XN"); rail_run(-X_T, VOID_S, X_T, VOID_S, "XS")

# ---------------- floor and ground ----------------
slab("FLOOR_BOARDS", -X_ARM - 12, X_ARM + 12, -Y_HALF, Y_HALF, 0.002 / FT, 0.5, FLOORM, C["FLOOR"], part_kind="floor_ground")
bm = bmesh.new(); bm_box(bm, ft(-9000), ft(9000), ft(-9000), ft(9000), -0.30, -0.02)
new_obj("GROUND_PARK", finish(bm, "ground", GRASS), C["GROUND"], props={"part_kind": "ground"})

# ---------------- walls (ends of the transept block, and the arms' clerestory sides) ----------------
def mesh_wall_bay(width_ft, height_ft, boarded):
    """One 24 ft wall bay between columns: 3 panels 8 ft wide with round heads; ground tier boarded."""
    bm = bmesh.new(); W = width_ft; H = height_ft
    n = int(round(W / 8)); pw = W / n
    mats_idx = []
    for k in range(n + 1):
        x = -W/2 + pw * k
        bm_box(bm, ft(x) - inch(2.5), ft(x) + inch(2.5), -inch(3), inch(3), 0, ft(H))
    bm_box(bm, ft(-W/2), ft(W/2), -inch(3), inch(3), 0, ft(0.5))
    bm_box(bm, ft(-W/2), ft(W/2), -inch(3), inch(3), ft(H) - inch(5), ft(H))
    head_c = H - 1.5 - pw / 2
    for k in range(n):
        xc = -W/2 + pw * (k + 0.5)
        pts = [(xc + pw/2*math.cos(math.pi*j/12), head_c + pw/2*math.sin(math.pi*j/12)) for j in range(13)]
        for (xa, za), (xb, zb) in zip(pts, pts[1:]):
            bm_bar(bm, (ft(xa), 0, ft(za)), (ft(xb), 0, ft(zb)), inch(2), inch(3))
        bm_box(bm, ft(xc) - inch(1), ft(xc) + inch(1), -inch(1), inch(1), ft(0.5), ft(head_c))  # central sash bar
    me = finish(bm, f"wall_{W}_{H}_{'b' if boarded else 'g'}", WOOD)
    # infill: boarding or glass, as one plane
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    v = [bm.verts.new(p) for p in [(ft(-W/2), 0, ft(0.5)), (ft(W/2), 0, ft(0.5)), (ft(W/2), 0, ft(H)), (ft(-W/2), 0, ft(H))]]
    f = bm.faces.new(v)
    for lp in f.loops: lp[uvl].uv = (lp.vert.co.x / FT, lp.vert.co.z / FT)
    me2 = finish(bm, me.name + "_fill", WOODDARK if boarded else GLASS)
    return me, me2

def wall_run(x0, y0, x1, y1, z0, z1, boarded, tag, louvre=True):
    """infill wall between columns from (x0,y0) to (x1,y1) in 24 ft bays, z0..z1 ft."""
    L = math.hypot(x1 - x0, y1 - y0); n = max(1, round(L / 24)); H = z1 - z0 - (2.5 if louvre else 0)
    key = f"w{H:.2f}{boarded}"
    if key not in LIBM: LIBM[key], LIBM[key + "f"] = mesh_wall_bay(24, H, boarded)
    if louvre and "louv" not in LIBM:
        bm = bmesh.new()
        for k in range(4):
            z = 0.3 + 0.55 * k
            bm_bar(bm, (ft(-12), -inch(2), ft(z)), (ft(12), inch(2), ft(z) + inch(4)), inch(5), inch(0.5))
        LIBM["louv"] = finish(bm, "wall_louvre", IRON)
    rot = math.pi / 2 if abs(x1 - x0) < 1e-6 else 0.0
    for k in range(n):
        xa = x0 + (x1 - x0) * (k + 0.5) / n; ya = y0 + (y1 - y0) * (k + 0.5) / n
        place(key, f"WALL_{tag}_{k}", C["WALLS"], xa, ya, z0, rot, part_kind="wall")
        place(key + "f", f"WALLF_{tag}_{k}", C["WALLS"], xa, ya, z0, rot, part_kind="wall_fill")
        if louvre:
            place("louv", f"WLOUV_{tag}_{k}", C["WALLS"], xa, ya, z0 + H, rot, part_kind="louvre")

for sy in (-1, 1):
    Y = sy * Y_HALF; tag = "S" if sy < 0 else "N"
    # tier 1 (0 .. 19.17, under the girder) across the whole block, tier 2 across |x|<=132, tier 3 across |x|<=60
    for (xa, xb) in ((-X_ARM, -X_T), (X_T, X_ARM)):
        wall_run(xa, Y, xb, Y, 0.0, GIRDER_TOP[0] - GIRDER_D, True, f"{tag}1_{xa}")
        wall_run(xa, Y, xb, Y, GIRDER_TOP[0], GIRDER_TOP[1] - GIRDER_D, False, f"{tag}2_{xa}")
    for (xa, xb) in ((-X_LF, -X_T), (X_T, X_LF)):
        wall_run(xa, Y, xb, Y, GIRDER_TOP[1], GIRDER_TOP[2] - GIRDER_D, False, f"{tag}3_{xa}")
    # transept end proper (x -36..36): ground tier boarded with the entrance at the south (doorways left open)
    for (xa, xb) in ((-36, -12), (12, 36)):
        wall_run(xa, Y, xb, Y, 0.0, GIRDER_TOP[0] - GIRDER_D, True, f"{tag}E1_{xa}")
    if sy > 0:
        wall_run(-12, Y, 12, Y, 0.0, GIRDER_TOP[0] - GIRDER_D, True, f"{tag}E1_mid")
    wall_run(-36, Y, 36, Y, GIRDER_TOP[0], GIRDER_TOP[1] - GIRDER_D, False, f"{tag}E2")
    wall_run(-36, Y, 36, Y, GIRDER_TOP[1], GIRDER_TOP[2] - GIRDER_D, False, f"{tag}E3")
for sx in (-1, 1):   # clerestory sides of the tier-2 arms, and tier-3 sides of the lead-flat strips
    for sy in (-1, 1):
        ya, yb = sorted((sy * 60, sy * Y_HALF))
        wall_run(sx * X_ARM, ya, sx * X_ARM, yb, GIRDER_TOP[0], GIRDER_TOP[1] - GIRDER_D, False, f"A{sx:+d}{sy:+d}")
        wall_run(sx * X_LF, ya, sx * X_LF, yb, GIRDER_TOP[1], GIRDER_TOP[2] - GIRDER_D, False, f"L{sx:+d}{sy:+d}")

# ---------------- arm galleries and avenue stairs (Plate II, XV-XVII; mirrors Claude's scheme) ----------------
# Gallery cells in the tier-2 arms (|x| 60..132): strips |y| 36..60 and 108..132; avenue voids |y| 60..108 except the
# stair bay |x| 84..108, where a 48 x 24 ft cross gallery bridges the void (two 8 x 16 ft wells over the middle strip).
STAIR_RISE_LAND = 137.5 / 12          # landing height, ft (Claude parts.STAIR_RISE)
def mesh_flight(run_ft, rise_ft, width_ft, name):
    """straight flight along +Y from y=0 (foot) to y=run, rising rise; strings and treads; origin at the foot."""
    bm = bmesh.new(); n = max(2, round(rise_ft / (6.5 / 12))); g = run_ft / n; r = rise_ft / n; w = width_ft
    for k in range(n):
        bm_box(bm, ft(-w/2), ft(w/2), ft(k * g), ft((k + 1) * g + 0.1), ft((k + 1) * r - 0.12), ft((k + 1) * r))
    for sx in (-1, 1):
        bm_bar(bm, (ft(sx * w/2), 0, ft(0.4)), (ft(sx * w/2), ft(run_ft), ft(rise_ft + 0.4)), inch(2), inch(11))
        bm_bar(bm, (ft(sx * w/2), 0, ft(3.0)), (ft(sx * w/2), ft(run_ft), ft(rise_ft + 3.0)), inch(2.5), inch(2.5))
    return finish(bm, name, WOOD)
LIBM["flight"] = mesh_flight(20, STAIR_RISE_LAND, 7.0, "stair_flight")
LIBM["flight2"] = mesh_flight(20, GALLERY_TOP - STAIR_RISE_LAND, 7.0, "stair_flight_upper")
for sx in (-1, 1):
    ov = {"claude_overlap": sx < 0}
    for sy in (-1, 1):
        for (ya, yb) in ((36, 60), (108, 132)):
            y0, y1 = sorted((sy * ya, sy * yb)); x0, x1 = sorted((sx * X_LF, sx * X_ARM))
            slab(f"GAL_ARM_{sx:+d}{sy:+d}_{ya}", x0, x1, y0, y1, GALLERY_TOP, GALLERY_T, WOOD, C["GALLERIES"],
                 part_kind="gallery_floor", **ov)
        # cross gallery over the stair bay
        xc = sx * 96; y0, y1 = sorted((sy * 60, sy * 108))
        for (xa, xb) in ((-12, -4), (4, 12)):
            slab(f"XGAL_{sx:+d}{sy:+d}_{xa}", xc + xa, xc + xb, y0, y1, GALLERY_TOP, GALLERY_T, WOOD, C["GALLERIES"], part_kind="gallery_floor", **ov)
        ym0, ym1 = sorted((sy * 76, sy * 92))
        slab(f"XGAL_{sx:+d}{sy:+d}_mid", xc - 4, xc + 4, ym0, ym1, GALLERY_TOP, GALLERY_T, WOOD, C["GALLERIES"], part_kind="gallery_floor", **ov)
        # stair: landing at the void centre, two ground flights in the outer strips, two upper flights in the middle
        ym0, ym1 = sorted((sy * 80, sy * 88))
        slab(f"STLAND_{sx:+d}{sy:+d}", xc - 12, xc + 12, ym0, ym1, STAIR_RISE_LAND, 0.5, WOOD, C["GALLERIES"], part_kind="stair_landing", **ov)
        rot_out = 0.0 if sy > 0 else math.pi      # flight local +Y points away from the nave
        for dx in (-7.75, 7.75):
            place("flight", f"STFL_{sx:+d}{sy:+d}_{dx:+.0f}", C["GALLERIES"], xc + dx, sy * 60, 0, rot_out, part_kind="stair_flight", **ov)
        place("flight2", f"STFU_{sx:+d}{sy:+d}_IN", C["GALLERIES"], xc, sy * 80, STAIR_RISE_LAND, rot_out + math.pi, part_kind="stair_flight", **ov)
        place("flight2", f"STFU_{sx:+d}{sy:+d}_OUT", C["GALLERIES"], xc, sy * 88, STAIR_RISE_LAND, rot_out, part_kind="stair_flight", **ov)
        for k, (xa, xb) in enumerate(((60, 84), (108, 132))):
            for ye in (60, 108):
                rail_run(sx * xa, sy * ye, sx * xb, sy * ye, f"ARM{sx:+d}{sy:+d}{k}{ye}")
        rail_run(sx * X_LF, sy * 60, sx * X_LF, sy * 108, f"ARMX{sx:+d}{sy:+d}")
for ob in list(C["RAILINGS"].objects):
    if ob.name.startswith(("RAIL_ARM", "RAIL_ARMX")) and ob.location.x < 0: ob["claude_overlap"] = True

# ---------------- the Osler crystal fountain at the crossing (ILN 1851 engraving; 27 ft of cut glass) ----------------
def glass_solid(name, tint=(0.95, 0.97, 1.0), ior=1.5, rough=0.0):
    """cut glass read as thin shells: Fresnel mix of a tinted transparent and a sharp glossy, plus a faint
    refraction lobe for the cut-glass sparkle. A solid refractive BSDF on single-sided lathe shells read as
    chrome in r06 tests (total internal reflection), so the shells are treated as thin glass."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    for x in list(n):
        if x.type != 'OUTPUT_MATERIAL': n.remove(x)
    out = [x for x in n if x.type == 'OUTPUT_MATERIAL'][0]
    fr = n.new("ShaderNodeFresnel"); fr.inputs["IOR"].default_value = ior
    tr = n.new("ShaderNodeBsdfTransparent"); tr.inputs["Color"].default_value = (*tint, 1)
    gl = n.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = rough
    rf = n.new("ShaderNodeBsdfRefraction"); rf.inputs["IOR"].default_value = ior; rf.inputs["Color"].default_value = (*tint, 1)
    m1 = n.new("ShaderNodeMixShader"); m1.inputs[0].default_value = 0.15
    l.new(tr.outputs[0], m1.inputs[1]); l.new(rf.outputs[0], m1.inputs[2])
    m2 = n.new("ShaderNodeMixShader"); l.new(fr.outputs[0], m2.inputs[0]); l.new(m1.outputs[0], m2.inputs[1]); l.new(gl.outputs[0], m2.inputs[2])
    l.new(m2.outputs[0], out.inputs["Surface"])
    m.diffuse_color = (*tint, 0.4)
    return m
CRYSTAL = glass_solid("GT_OslerCrystal", (0.96, 0.97, 1.0), 1.55, 0.0)
WATER = glass_solid("GT_Water", (0.80, 0.88, 0.86), 1.33, 0.02)
STONE = mat_principled("GT_Stone", (0.62, 0.60, 0.56), 0.8)
def lathe(profile_ft, name, mat, seg=48, cx=0.0, cy=0.0):
    """revolve a (r, z) polyline in feet about the vertical axis"""
    bm = bmesh.new(); rings = []
    for (r, z) in profile_ft:
        rings.append([bm.verts.new((ft(cx) + ft(r) * math.cos(2*math.pi*k/seg), ft(cy) + ft(r) * math.sin(2*math.pi*k/seg), ft(z))) for k in range(seg)])
    for A, B in zip(rings, rings[1:]):
        for k in range(seg):
            bm.faces.new([A[k], A[(k+1)%seg], B[(k+1)%seg], B[k]])
    me = finish(bm, name, mat)
    for p in me.polygons: p.use_smooth = True
    return me
FC = coll("FOUNTAIN", ROOT)
# basin: a stone curb 30 ft across (inferred from the figures in the ILN engraving), water 0.9 ft below the curb
new_obj("FOUNTAIN_CURB", lathe([(13.6, 0), (15.0, 0), (15.0, 1.6), (14.4, 1.9), (13.6, 1.9), (13.6, 0)], "f_curb", STONE), FC, props={"part_kind": "fountain"})
new_obj("FOUNTAIN_WATER", lathe([(0, 1.0), (13.65, 1.0)], "f_water", WATER, 64), FC, props={"part_kind": "fountain"})
# glass body: stepped plinth, big lower bowl, crowned middle bowl, small upper bowl, knopped shaft, finial
prof = [(0, 1.0), (5.2, 1.0), (5.2, 2.4), (4.4, 2.6), (4.4, 3.6), (3.6, 3.8), (2.2, 4.4), (1.6, 6.0),
        (1.3, 7.2), (3.5, 7.6), (7.6, 8.4), (8.4, 9.4), (8.0, 9.9), (2.0, 9.6), (1.2, 10.4), (1.0, 12.4),
        (2.0, 12.6), (5.2, 13.5), (5.6, 14.3), (1.0, 14.0), (0.8, 15.2), (1.5, 15.6), (3.2, 16.6), (3.4, 17.2),
        (0.7, 17.0), (0.6, 18.4), (1.0, 18.9), (0.5, 19.5), (0.45, 21.0), (0.85, 21.5), (0.4, 22.0), (0.35, 23.6),
        (0.7, 24.1), (0.3, 24.6), (0.25, 26.2), (0.55, 26.6), (0.0, 27.0)]
prof = [(r * (1.45 if z > 10.0 else 1.15), z) for (r, z) in prof]   # r07 F03: Talbot/ILN read a much fuller body than r06
new_obj("FOUNTAIN_GLASS", lathe(prof, "f_glass", CRYSTAL, 48), FC, props={"part_kind": "fountain", "height_ft": 27.0})
# hanging prism fringes on the bowls and the spiked crown on the middle bowl
bm = bmesh.new()
for (rr, z0, n, L) in ((8.2 * 1.15, 9.4, 64, 1.6), (5.4 * 1.45, 13.6, 44, 1.1), (3.3 * 1.45, 16.7, 28, 0.8)):
    for k in range(n):
        a = 2 * math.pi * k / n
        bm_cyl(bm, inch(0.9), ft(z0 - L), ft(z0), 5, ft(rr) * math.cos(a), ft(rr) * math.sin(a))
for k in range(18):
    a = 2 * math.pi * k / 18
    bm_bar(bm, (ft(6.7) * math.cos(a), ft(6.7) * math.sin(a), ft(14.2)), (ft(7.1) * math.cos(a), ft(7.1) * math.sin(a), ft(16.2)), inch(2.5), inch(2.5))
new_obj("FOUNTAIN_PRISMS", finish(bm, "f_prisms", CRYSTAL), FC, props={"part_kind": "fountain"})
# the water: a jet from the finial and a sheet falling from each bowl (thin glassy shells)
new_obj("FOUNTAIN_JET", lathe([(0.05, 26.9), (0.12, 29.5), (0.6, 30.6), (1.6, 30.2), (2.6, 28.0)], "f_jet", WATER, 24), FC, props={"part_kind": "fountain_water"})
# (r06: falling water sheets dropped; they read as solid chrome cylinders. Logged F-row.)

# ---------------- r07: statue and railing stand-ins (Talbot foreground; grades in DEPARTURES ST02/RL01) ----------------
SC = coll("STATUES", ROOT)
MARBLE = mat_principled("GT_Marble", (0.86, 0.85, 0.81), 0.45)
def statue(name, x, y, h=7.0, plinth=4.5):
    """plinth + a lathe figure stand-in (robed standing figure); not a likeness of any exhibited work"""
    bm = bmesh.new(); bm_box(bm, ft(x - 2.2), ft(x + 2.2), ft(y - 2.2), ft(y + 2.2), 0, ft(plinth))
    me_p = finish(bm, name + "_plinth", STONE); new_obj(name + "_PLINTH", me_p, SC, props={"part_kind": "statue"})
    z = plinth; f = [(0.0, z), (1.3, z), (1.2, z + 0.25 * h), (0.85, z + 0.55 * h), (1.05, z + 0.72 * h), (0.45, z + 0.80 * h),
                     (0.38, z + 0.84 * h), (0.55, z + 0.92 * h), (0.0, z + h)]
    new_obj(name + "_FIGURE", lathe(f, name + "_fig", MARBLE, 16, x, y), SC, props={"part_kind": "statue"})
# r09: the r07 lathe stand-ins read as mannequins; replaced by scripts/dressing.py (figures.py classical stand-ins on moulded pedestals)
# curved iron railing round the fountain (the scrolled railing in the Talbot foreground), r = 22 ft, 4 gaps
bm = bmesh.new(); Rr = 22.0; nseg = 96
for k in range(nseg):
    a0 = 2 * math.pi * k / nseg; a1 = 2 * math.pi * (k + 1) / nseg
    if (k % 24) in (0, 1, 23): continue    # 4 openings on the axes
    for zr in (0.4, 3.2, 3.5):
        bm_bar(bm, (ft(Rr * math.cos(a0)), ft(Rr * math.sin(a0)), ft(zr)), (ft(Rr * math.cos(a1)), ft(Rr * math.sin(a1)), ft(zr)), inch(1.5), inch(1.5))
    for j in range(3):
        a = a0 + (a1 - a0) * j / 3
        bm_bar(bm, (ft(Rr * math.cos(a)), ft(Rr * math.sin(a)), 0), (ft(Rr * math.cos(a)), ft(Rr * math.sin(a)), ft(3.5)), inch(0.75), inch(0.75))
new_obj("FOUNTAIN_RAILING", finish(bm, "f_rail", FAN if COLOUR != "owen" else IRON), FC, props={"part_kind": "railing"})

# ---------------- semicircular end screens (Plates VII, XXIV-XXVI) ----------------
def build_end_screen(sy):
    Y = ft(sy * Y_HALF); tag = "S" if sy < 0 else "N"
    bm = bmesh.new()
    R = R_EXT; zc = SPRING
    # attic band 62'2" .. springing: lath-and-cement panel (Fig. 7, p. 50)
    bm_box(bm, ft(-36), ft(36), Y - inch(4), Y + inch(4), ft(GIRDER_TOP[2]), ft(SPRING))
    # outer arch band / zinc cornice and the semicircular rib T
    for (r0, r1, d) in ((R - 1.5, R + 0.4, 10), (R - 0.2, R + 1.0, 14)):
        pts_o = arc_pts(ft(r1), 96); pts_i = arc_pts(ft(r0), 96)
        for k in range(96):
            q = [bm.verts.new((pts_i[k][0], Y - inch(d/2), ft(zc) + pts_i[k][1])), bm.verts.new((pts_o[k][0], Y - inch(d/2), ft(zc) + pts_o[k][1])),
                 bm.verts.new((pts_o[k+1][0], Y - inch(d/2), ft(zc) + pts_o[k+1][1])), bm.verts.new((pts_i[k+1][0], Y - inch(d/2), ft(zc) + pts_i[k+1][1])),
                 bm.verts.new((pts_i[k][0], Y + inch(d/2), ft(zc) + pts_i[k][1])), bm.verts.new((pts_o[k][0], Y + inch(d/2), ft(zc) + pts_o[k][1])),
                 bm.verts.new((pts_o[k+1][0], Y + inch(d/2), ft(zc) + pts_o[k+1][1])), bm.verts.new((pts_i[k+1][0], Y + inch(d/2), ft(zc) + pts_i[k+1][1]))]
            for f in [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]:
                bm.faces.new([q[i] for i in f])
    # fan: hub, concentric rings and radial bars (read by eye from Plates VII and XXIV)
    rings = [4.0, 12.0, 21.0, 29.0]
    for r in rings:
        pts = arc_pts(ft(r), 64)
        for (xa, za), (xb, zb) in zip(pts, pts[1:]):
            bm_bar(bm, (xa, Y, ft(zc) + za), (xb, Y, ft(zc) + zb), inch(9), inch(6))   # r09 L02: heavier, they vanished against the sky
    spokes = [(rings[0], rings[1], 16), (rings[1], rings[2], 16), (rings[2], rings[3], 16), (rings[3], R - 1.5, 48)]   # r09: 48 outer spokes
    for (ra, rb, n) in spokes:
        for k in range(1, n):
            a = math.pi * k / n
            bm_bar(bm, (ft(ra)*math.cos(a), Y, ft(zc) + ft(ra)*math.sin(a)), (ft(rb)*math.cos(a), Y, ft(zc) + ft(rb)*math.sin(a)), inch(8), inch(6))   # r10 L03 radial bars 6->8 in
    # petal heads: small arcs between spokes on the outer rings
    for (ra, rb, n) in spokes[1:3] + [(spokes[3][0], spokes[3][1], 24)]:
        for k in range(n):
            a0, a1 = math.pi * k / n, math.pi * (k + 1) / n; am = (a0 + a1) / 2
            rr = rb - (rb - ra) * 0.12
            pr = (rb - ra) * 0.0 + rr * math.sin((a1 - a0) / 2)
            pts = []
            for j in range(9):
                t = math.pi * j / 8
                # small arch whose apex points outward, spanning the two spokes
                ca = a0 + (a1 - a0) * j / 8
                rad = rr - pr * 0.6 * (1 - math.sin(t))
                pts.append((ft(rad) * math.cos(ca), ft(zc) + ft(rad) * math.sin(ca)))
            for (xa, za), (xb, zb) in zip(pts, pts[1:]):
                bm_bar(bm, (xa, Y, za), (xb, Y, zb), inch(4), inch(4))
    # columns of the screen: the semi-elliptical wooden columns B rise with the arch (approximated as 2 mullions per 24 ft)
    new_obj(f"ENDSCREEN_FRAME_{tag}", finish(bm, f"endscreen_{tag}", FAN), C["END_SCREENS"], props={"part_kind": "end_screen"})
    # glass disc
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    pts = arc_pts(ft(R - 0.5), 96)
    c = bm.verts.new((0, Y + sy * inch(1), ft(zc)))
    vs = [bm.verts.new((x, Y + sy * inch(1), ft(zc) + z)) for (x, z) in pts]
    for a, b in zip(vs, vs[1:]):
        f = bm.faces.new([c, a, b])
        for lp in f.loops: lp[uvl].uv = (lp.vert.co.x / FT * 0.01, lp.vert.co.z / FT * 0.01)
    new_obj(f"ENDSCREEN_GLASS_{tag}", finish(bm, f"endglass_{tag}", GLASS_END), C["END_SCREENS"], props={"part_kind": "end_glass"})
for sy in (-1, 1): build_end_screen(sy)

# south entrance: doors and pedestals (Plate XXVI) -- simple timber door leaves in the central bay
bm = bmesh.new()
for xc in (-8, 0, 8):
    bm_box(bm, ft(xc - 3), ft(xc + 3), ft(-Y_HALF) - inch(2), ft(-Y_HALF) + inch(2), 0, ft(14))
new_obj("SOUTH_DOORS", finish(bm, "south_doors", WOODDARK), C["WALLS"], props={"part_kind": "door"})
bm = bmesh.new()
for xc in (-12, 12):
    bm_box(bm, ft(xc - 2.5), ft(xc + 2.5), ft(-Y_HALF - 6), ft(-Y_HALF - 1), 0, ft(7))
new_obj("SOUTH_PEDESTALS", finish(bm, "pedestals", WOODDARK), C["WALLS"], props={"part_kind": "pedestal"})

if MILESTONES:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(MILESTONES, "m01_frame_vault_glazing.blend"), compress=True)

# ---------------- elms ----------------
ELMS = [  # name, x ft, y ft, height ft, trunk dia ft, crown radius ft  (inferred; see DEPARTURES)
    ("ELM_SOUTH", 4.0, -128.0, 78.0, 3.6, 30.0),
    ("ELM_NORTH", -3.0, 142.0, 84.0, 4.0, 31.0),
    ("ELM_NORTH2", 12.0, 98.0, 64.0, 2.6, 22.0),
]
def vault_half_width(z_ft):
    h = z_ft - SPRING
    ri = R_EXT - RIB_A_D
    if h <= 0: return X_T - 1.0
    if h >= ri: return 0.0
    return math.sqrt(ri * ri - h * h)

def bm_tube(bm, a, b, ra, rb, seg=8):
    a = Vector(a); b = Vector(b); d = b - a
    if d.length < 1e-6: return
    d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0))
    s = d.cross(up).normalized(); u = s.cross(d).normalized()
    ra_ = [bm.verts.new(a + (s * math.cos(2*math.pi*k/seg) + u * math.sin(2*math.pi*k/seg)) * ra) for k in range(seg)]
    rb_ = [bm.verts.new(b + (s * math.cos(2*math.pi*k/seg) + u * math.sin(2*math.pi*k/seg)) * rb) for k in range(seg)]
    for k in range(seg):
        bm.faces.new([ra_[k], ra_[(k+1)%seg], rb_[(k+1)%seg], rb_[k]])

def build_elm(name, x, y, H, D, CR, seed):
    """English elm, stylised: a straight bole that forks low into ascending leaders, tapering limbs, and a
    foliage made of many small leaf cards gathered in billowing clusters (the 'cumulus' look of elms in
    the Talbot and empty-transept photographs). All in feet, converted at the end."""
    rnd = random.Random(seed)
    bm = bmesh.new(); tips = []
    F = lambda v: Vector((ft(v[0]), ft(v[1]), ft(v[2])))
    def branch(p, d, length, radius, depth, wig):
        n = max(2, int(length / 4))
        cur = Vector(p); dirv = Vector(d).normalized(); pts = [cur.copy()]
        for i in range(n):
            dirv = (dirv + Vector((rnd.uniform(-wig, wig), rnd.uniform(-wig, wig), rnd.uniform(-wig/3, wig/2)))).normalized()
            cur = cur + dirv * (length / n)
            cur.z = min(cur.z, H - 1.0)
            lim = min(vault_half_width(cur.z + 1.0) - 4.0, X_T - 3.0)
            while lim < 1.0 and cur.z > 0:      # too high near the crown: drop the point until it fits
                cur.z -= 1.0; lim = min(vault_half_width(cur.z + 1.0) - 4.0, X_T - 3.0)
            if abs(cur.x) > lim:
                cur.x = math.copysign(lim, cur.x); dirv = (dirv + Vector((-math.copysign(0.6, cur.x), 0, 0.2))).normalized()
            pts.append(cur.copy())
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            r0 = radius * (1 - 0.6 * i / n); r1 = radius * (1 - 0.6 * (i + 1) / n)
            bm_tube(bm, F(a), F(b), ft(r0), ft(r1), 8 if radius > 0.6 else 5)
        if depth == 0:
            tips.extend(pts[len(pts)//2:]); return
        nk = 4 if depth >= 2 else 3
        for k in range(nk):
            t = rnd.uniform(0.35, 0.95); base = pts[max(1, min(len(pts)-1, int(round(t * n))))]
            ang = rnd.uniform(0, 2*math.pi)
            nd = (dirv * 1.0 + Vector((math.cos(ang), math.sin(ang), rnd.uniform(0.1, 0.6)))).normalized()
            branch(base, nd, length * rnd.uniform(0.45, 0.62), radius * 0.5, depth - 1, wig * 1.3)
    trunk_h = H * 0.30
    branch((x, y, 0), (0, 0, 1), trunk_h, D / 2, 0, 0.03)
    tips.clear()
    top = Vector((x, y, trunk_h))
    nlead = 5
    for k in range(nlead):
        ang = 2 * math.pi * k / nlead + rnd.uniform(-.3, .3)
        spread = rnd.uniform(0.45, 0.8)
        nd = Vector((math.cos(ang) * spread, math.sin(ang) * spread, 1)).normalized()
        branch(top, nd, (H - trunk_h) * rnd.uniform(0.55, 0.7), D * 0.26, 3, 0.10)
    # English elm: lower side limbs off the bole and leaders give the tall, billowing, low-starting crown
    # (r05 fix: r04 read as an umbrella pine with a bare stem)
    for k in range(6):
        zb = trunk_h * rnd.uniform(0.75, 1.0) + (H - trunk_h) * rnd.uniform(0.0, 0.25)
        ang = rnd.uniform(0, 2 * math.pi)
        nd = Vector((math.cos(ang), math.sin(ang), rnd.uniform(0.35, 0.7))).normalized()
        branch(Vector((x, y, zb)), nd, CR * rnd.uniform(0.55, 0.8), D * 0.14, 2, 0.12)
    me = finish(bm, name + "_wood", BARK)
    for pg in me.polygons: pg.use_smooth = True
    new_obj(name + "_WOOD", me, C["ELMS"], props={"part_kind": "elm_wood"})
    # foliage: clusters of leaf cards
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    zc = trunk_h + (H - trunk_h) * 0.5; hz = (H - trunk_h) * 0.62
    clusters = 0; cards = 0
    for tp in tips:
        if rnd.random() < 0.05: continue
        c = Vector(tp) + Vector((rnd.uniform(-2, 2), rnd.uniform(-2, 2), rnd.uniform(0, 2.5)))
        r = rnd.uniform(3.0, 5.0)
        if c.z < H * 0.26: continue
        if math.hypot(c.x - x, c.y - y) + r * 0.6 > CR or (c.z - zc) / hz > 1.0 or c.z + r > H: continue
        if abs(c.x) + r + 1.6 > min(vault_half_width(c.z + r + 1.6) - 3.0, X_T - 2.0): continue
        clusters += 1
        for j in range(150):
            # points in a squashed sphere, denser at the outer, sunlit skin
            v = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1))).normalized() * (r * rnd.uniform(0.55, 1.0) ** 0.5)
            v.z *= 0.75
            q = c + v
            nrm = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.3, 1))).normalized()
            t1 = nrm.cross(Vector((0.3, 0.2, 1))).normalized(); t2 = nrm.cross(t1)
            sz = rnd.uniform(0.45, 0.8)
            vs = [bm.verts.new(F(q + (t1 * sx + t2 * sy) * sz)) for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            f = bm.faces.new(vs)
            for lp, uv in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))): lp[uvl].uv = uv
            cards += 1
    me = finish(bm, name + "_leaves", LEAF)
    new_obj(name + "_LEAVES", me, C["ELMS"], props={"part_kind": "elm_leaves", "clusters": clusters, "cards": cards})
    return {"clusters": clusters, "cards": cards}
elm_report = {}
for i, (n, x, y, H, D, CR) in enumerate(ELMS):
    elm_report[n] = build_elm(n, x, y, H, D, CR, SEED + i)

if MILESTONES:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(MILESTONES, "m02_elms.blend"), compress=True)

# ---------------- world, sun, render settings ----------------
world = bpy.data.worlds.new("GT_World"); scene.world = world; world.use_nodes = True
wn = world.node_tree.nodes; bg = wn["Background"]
sky = wn.new("ShaderNodeTexSky")
try:
    sky.sky_type = 'NISHITA'
except TypeError:
    pass
try:
    sky.sun_elevation = math.radians(38); sky.sun_rotation = math.radians(200)
except AttributeError:
    pass
world.node_tree.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 0.35
sun = bpy.data.lights.new("GT_Sun", 'SUN'); sun.energy = 3.2; sun.angle = math.radians(0.6)
sun.color = (1.0, 0.96, 0.9)
so = bpy.data.objects.new("GT_Sun", sun); scene.collection.objects.link(so)
so.rotation_euler = (math.radians(52), 0, math.radians(200 - 180 + 90))
cy = scene.cycles if hasattr(scene, "cycles") else None
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'; scene.cycles.samples = 96; scene.cycles.use_denoising = True
scene.cycles.max_bounces = 6; scene.cycles.transparent_max_bounces = 32; scene.cycles.glossy_bounces = 3
scene.cycles.transmission_bounces = 6
scene.render.resolution_x = 1920; scene.render.resolution_y = 1080; scene.render.resolution_percentage = 100
try:
    scene.view_settings.view_transform = 'AgX'
except TypeError:
    scene.view_settings.view_transform = 'Filmic'
try:
    scene.view_settings.look = 'AgX - Medium High Contrast'   # r07 V08: r06 read flat and washed out
except TypeError:
    pass
scene.view_settings.exposure = -0.7   # r10 G03: darker grade (was -0.25)

# ---------------- r08: exhibit proxies appended from Muse's models/ (read-only extract, origin/main adb0d2c; MC03) ----------------
MUSE_DIR = "/workspace/models-main-ro/models"
def muse_prop(fname, keep, offset, cname):
    path = os.path.join(MUSE_DIR, fname, fname + ".blend")
    if not os.path.exists(path): return None
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = [n for n in src.objects if keep(n)]
    mc = bpy.data.collections.new(cname); mc.instance_offset = offset
    mc["credit"] = f"Muse, models/{fname} (origin/main 549fd0c), appended read-only"
    for o in dst.objects:
        if o and o.type == 'MESH': mc.objects.link(o)
    return mc
EXC = coll("EXHIBITS", ROOT); exhibits = []
def put(mc, name, x, y, rz, kind):
    e = bpy.data.objects.new(name, None); e.instance_type = 'COLLECTION'; e.instance_collection = mc
    e.location = (ft(x), ft(y), 0); e.rotation_euler = (0, 0, rz); EXC.objects.link(e)
    e["part_kind"] = kind; e["credit"] = "Muse"; exhibits.append(e)
CASE = muse_prop("hp-crate-and-display-case", lambda n: n.startswith("Case"), (1.4, 0.0, 0.0), "MUSE_DisplayCase_by_Muse")
BENCH = muse_prop("park-bench", lambda n: n not in ("Ground", "Backdrop"), (0.0, 0.0, 0.0), "MUSE_Bench_by_Muse")
PLINTH = muse_prop("display-plinth", lambda n: n == "DisplayPlinth", (0.0, 0.0, 0.0), "MUSE_Plinth_by_Muse")
if CASE:   # paired vitrines down both transept aisles under the galleries (|x| 36-60), one pair per 24 ft bay
    for sx in (-1, 1):
        for sy in (-1, 1):
            for j in range(6):
                yc = sy * (48 + 24 * j)
                for dy in (-5.5, 5.5): put(CASE, f"EXH_CASE_{sx:+d}{sy:+d}_{j}_{dy:+.0f}", sx * 46.5, yc + dy, math.pi / 2, "exhibit_case")
if PLINTH:  # empty plinths along the aisle line facing the transept (sculpture to follow; plinths stand where Talbot shows statues)
    for sx in (-1, 1):
        for sy in (-1, 1):
            for j in range(3): put(PLINTH, f"EXH_PLINTH_{sx:+d}{sy:+d}_{j}", sx * 37.5, sy * (60 + 48 * j), -sx * math.pi / 2, "exhibit_plinth")
if BENCH:   # benches in the transept, east side near the fountain and west side to the north
    for (x, y, rz) in ((22, -46, -math.pi / 2), (22, 46, -math.pi / 2), (-22, 116, math.pi / 2), (-22, 158, math.pi / 2)):   # seat front (Muse -y) faces the axis
        put(BENCH, f"EXH_BENCH_{x:+d}_{y:+d}", x, y, rz, "bench")
print("MUSE_EXHIBITS", len(exhibits), flush=True)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dressing.py")).read())

# ---------------- cameras (storyboard v001 grammar) ----------------
CAMS = bpy.data.collections.new("CAMERAS_GROK"); scene.collection.children.link(CAMS)
def cam(name, loc_ft, look_ft, lens, ortho=None, sensor=36.0):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.sensor_width = sensor; cd.clip_start = 0.1; cd.clip_end = 3000
    if ortho: cd.type = 'ORTHO'; cd.ortho_scale = ortho
    ob = bpy.data.objects.new(name, cd); CAMS.objects.link(ob)
    ob.location = [ft(v) for v in loc_ft]
    d = Vector([ft(v) for v in look_ft]) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()   # no roll: Y-up track keeps the horizon level
    return ob
EYE = 1.6 / FT
route = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "route", "camera_route.json")))
for shot in route["shots"]:
    for key in ("start", "end"):
        if key in shot:
            cam(f"{shot['id']}_{key}", shot[key]["pos_ft"], shot[key]["look_ft"], shot["lens_mm"], shot.get("ortho_m"))
scene.camera = bpy.data.objects.get("REV_ext34_start")

# ---------------- report ----------------
scene["grok_build"] = json.dumps({"parts": len(parts), "elm_clumps": elm_report, "spring_ft": SPRING, "seed": SEED, "colour": COLOUR})
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True)
print("SAVED", OUT, "parts", len(parts), "elms", elm_report)
