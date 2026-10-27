"""Hyde Park 1851 Crystal Palace: EXTERIOR completion -- east half, north strip, end walls, outer glazing (Grok Bot).

Complements course-models/crystal-palace-1851-claude (west frame, lines x <= -36 ft) and
course-models/crystal-palace-1851-transept-grok (transept core, |x| <= 132 ft). Same frame as Claude: metres, origin at
the nave/transept crossing at floor level, X east, Y north, Z up, 1 ft = 0.3048 m. Hyde Park only (never Sydenham).
Sources: Downes 1852 Plates I-V, VI, XXI; CONTROL-DIMENSIONS D01-D05, D10-D14.  Shared helper prelude copied verbatim
from build_transept.py (materials, column / girder meshes) so the two folders stay independent.

Run:  blender -b -P build_exterior.py -- --out ../rounds/x01.blend [--milestones DIR] [--colour neutral|owen]
"""
import bpy, bmesh, math, random, sys, os, json
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default
OUT = arg("--out", "/tmp/exterior.blend")
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
ROOT = coll("EXTERIOR_GROK")
C = {n: coll(n, ROOT) for n in ["COLUMNS", "GIRDERS", "TRUSSES", "ROOFS", "GALLERIES", "RAILINGS", "WALLS", "CRESTING", "FLOOR", "GROUND"]}
LIB = bpy.data.collections.new("LIB_GROK_EXT")   # unlinked library of shared meshes

# ---------------- materials ----------------
def mat_principled(name, rgb, rough=0.6, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    m.diffuse_color = (*rgb, 1)
    return m

def mat_glass(name, tint=(0.88, 0.95, 0.93), bars=True, milk=0.06, milk_rgb=(0.9, 0.93, 0.92)):
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
    df = n.new("ShaderNodeBsdfDiffuse"); df.inputs[0].default_value = (*milk_rgb, 1)
    mx2 = n.new("ShaderNodeMixShader"); mx2.inputs[0].default_value = milk; l.new(mx.outputs[0], mx2.inputs[1]); l.new(df.outputs[0], mx2.inputs[2])
    last = mx2.outputs[0]
    if bars:
        uv = n.new("ShaderNodeTexCoord"); sep = n.new("ShaderNodeSeparateXYZ"); l.new(uv.outputs["UV"], sep.inputs[0])
        add = n.new("ShaderNodeMath"); add.operation = 'ADD'; l.new(sep.outputs[0], add.inputs[0]); l.new(sep.outputs[1], add.inputs[1])
        mul = n.new("ShaderNodeMath"); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 1 / 0.85; l.new(add.outputs[0], mul.inputs[0])
        frc = n.new("ShaderNodeMath"); frc.operation = 'FRACT'; l.new(mul.outputs[0], frc.inputs[0])
        lt = n.new("ShaderNodeMath"); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.07; l.new(frc.outputs[0], lt.inputs[0])
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
FAN = mat_principled("GT_FanIron", (0.10, 0.11, 0.11), 0.5) if COLOUR != "owen" else oj_material("GT_Fan_OJ", "plain")
WOOD = mat_principled("GT_Timber", (0.72, 0.66, 0.56), 0.7)
WOODDARK = mat_principled("GT_Boarding", (0.62, 0.55, 0.45), 0.8)
LEAD = mat_principled("GT_Lead", (0.42, 0.44, 0.46), 0.5, 0.3)
GLASS = mat_glass("GT_Glass")
GLASS_PLAIN = mat_glass("GT_GlassPlain", tint=(0.62, 0.68, 0.68), bars=False)
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


parts = []
def place(meshkey, name, coll_, x, y, z, rot=0.0, **props):
    ob = new_obj(name, LIBM[meshkey], coll_, (ft(x), ft(y), ft(z)), rot, dict(props))
    parts.append(name); return ob

# =====================================================================================================================
# EXTERIOR COMPLETION (Grok Bot): east half (lines x = 36..924), the north strip (x -708..228, y 204..252), every
# outer wall, the end walls at x = +-924, cresting and finials.  Complementary to Claude's west frame (lines x <= -36)
# and to Grok's transept (x -132..132 core); this script never re-builds a column either of them builds.
# =====================================================================================================================
X_END = 924.0
STRIP_X0, STRIP_X1, STRIP_Y1 = -708.0, 228.0, 252.0      # D05: 936 x 48 ft, north chain 216 + 936 + 696
ROWS_Y = [-Y_HALF + GRID * j for j in range(18)]
LINES_E = [36.0 + GRID * k for k in range(38)]            # 36 .. 924

def claude_top_tier(y):
    ay = abs(y)
    return 3 if ay <= 60 else (2 if ay <= 132 else 1)

def transept_owns(x, y):
    """column positions built by course-models/crystal-palace-1851-transept-grok (mirrors its plan loop)."""
    ax, ay = abs(x), abs(y)
    if ax in (36, 60, 84, 108, 132) and ay <= Y_HALF:
        if ay < NAVE: return False
        if ax > X_LF and ay < 60: return False
        return True
    if ax == 12 and y in (-Y_HALF, Y_HALF, -180, VOID_S): return True
    return False

def transept_tier(x, y):
    ax = abs(x)
    if ax <= X_LF: return 3
    if ax <= X_ARM: return 3 if abs(y) <= 60 else 2
    return 1

cols = {}          # (x, y) -> top tier, for every column this build places
known = {}         # (x, y) -> top tier, incl. transept columns (for shared girders)
for x in (-132, -108, -84, -60, -36, 36, 60, 84, 108, 132):
    for y in ROWS_Y:
        if transept_owns(x, y): known[(x, y)] = transept_tier(x, y)
for x in LINES_E:
    for y in ROWS_Y:
        if abs(y) < NAVE: continue                 # clear 72 ft nave (Plate VI; DEPARTURES EX02)
        if transept_owns(x, y): continue
        t = claude_top_tier(y)
        place(f"col{t}", f"ECOL_X{x:+05.0f}_Y{y:+04.0f}", C["COLUMNS"], x, y, 0, part_kind="column", tier=t, half="east")
        cols[(x, y)] = t; known[(x, y)] = t
# north strip: two more rows (y 228, 252) on every line from -708 to 228, tier 1 only
for i in range(40):
    x = STRIP_X0 + GRID * i
    for y in (228.0, 252.0):
        place("col1", f"NCOL_X{x:+05.0f}_Y{y:+04.0f}", C["COLUMNS"], x, y, 0, part_kind="column", tier=1, half="north_strip")
        cols[(x, y)] = 1; known[(x, y)] = 1

def gird(a, b, along, tiers):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    for k in range(tiers):
        place("g24", f"EGIR_T{k+1}_{along}_{mx:+.0f}_{my:+.0f}", C["GIRDERS"], mx, my, GIRDER_TOP[k],
              math.pi / 2 if along == "Y" else 0.0, part_kind="girder", tier=k + 1, span_ft=24)
ngird = 0
for (x, y), t in list(cols.items()):
    for (dx, dy, al) in ((24, 0, "X"), (-24, 0, "X"), (0, 24, "Y"), (0, -24, "Y")):
        b = (x + dx, y + dy)
        if b not in known: continue
        if b in cols and (dx < 0 or dy < 0): continue          # mine-mine pairs once
        gird((x, y), b, al, min(t, known[b])); ngird += 1
# strip girders down to the main block's y = 204 row (Claude's / transept's / mine), tier 1
for i in range(40):
    x = STRIP_X0 + GRID * i
    if (x, 204.0) in known: continue                 # handled by the pair loop above
    gird((x, 204.0), (x, 228.0), "Y", 1)
# 72 ft trusses across the nave on every east line beyond the transept (Plate VI; transept owns 36 and 60)
for x in LINES_E:
    if x <= X_LF: continue
    place("t72g", f"ETRUSS72_X{x:+05.0f}", C["TRUSSES"], x, 0, GIRDER_TOP[2], math.pi / 2, part_kind="truss", span_ft=72)

# ---------------- ridge-and-furrow roofs (24 x 8 ft units, ridges along X like Claude's) ----------------
# EX19: exterior roof glass greyer and less milky than the transept glass, so 19 acres of roof read as glass, not white slabs
ROOFGLASS = mat_glass("GT_RoofGlassExt", tint=(0.58, 0.64, 0.64), milk=0.025, milk_rgb=(0.55, 0.58, 0.58))
def mesh_roof_unit():
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    L = ft(24); W = ft(8); rise = ft(1.6)
    v = [bm.verts.new(p) for p in [(-L/2, -W/2, 0), (L/2, -W/2, 0), (L/2, 0, rise), (-L/2, 0, rise),
                                   (-L/2, W/2, 0), (L/2, W/2, 0)]]
    for f in ([v[0], v[1], v[2], v[3]], [v[3], v[2], v[5], v[4]]):
        ff = bm.faces.new(f)
        for lp in ff.loops: lp[uvl].uv = (lp.vert.co.x / FT, lp.vert.co.y / FT * 1.3)
    # Paxton gutter on the furrow line
    bm_box(bm, -L/2, L/2, -W/2 - inch(3), -W/2 + inch(3), -inch(5), inch(1))
    return finish(bm, "roof_unit", ROOFGLASS, [ROOFGLASS, WOOD])
LIBM["roof"] = mesh_roof_unit()
def roof_band(x0, x1, y0, y1, tier, tag):
    n = 0
    for xb in range(int(x0), int(x1), 24):
        for k in range(int((y1 - y0) / 8)):
            yc = y0 + 4 + 8 * k
            place("roof", f"EROOF{tier}_{tag}_{xb + 12:+d}_{yc:+.0f}", C["ROOFS"], xb + 12, yc, GIRDER_TOP[tier - 1],
                  part_kind="roof", tier=tier); n += 1
    return n
roof_n = roof_band(60, 924, -60, 60, 3, "nave")
for s in (-1, 1):
    roof_n += roof_band(132, 924, *sorted((s * 60, s * 132)), 2, f"t2{s:+d}")
    roof_n += roof_band(132, 924, *sorted((s * 132, s * 204)), 1, f"t1{s:+d}")
roof_n += roof_band(STRIP_X0, STRIP_X1, 204, 252, 1, "strip")

# ---------------- east-half galleries (mirror of Claude's cells; Plate II) ----------------
AVENUE_VOID_BAYS = set(list(range(1, 8)) + list(range(9, 17)) + list(range(18, 26)) + list(range(27, 34)) + [35, 36])
STAIR_BAYS = {8, 17, 26, 34}
def mirror_bay(xc):           # east bay centre -> Claude's bay index of the mirrored bay
    return int(round((-xc - 12 + 924) / 24))
gbm = bmesh.new(); rbm = bmesh.new()
for xb in range(132, 924, 24):
    xc = xb + 12; b = mirror_bay(xc)
    for kc in range(11):
        y_lo = -132 + 24 * kc
        if kc in (4, 5, 6) and b >= 3: continue                     # nave void
        if kc in (1, 2, 8, 9) and (b in AVENUE_VOID_BAYS or b in STAIR_BAYS): continue
        bm_box(gbm, ft(xb), ft(xb + 24), ft(y_lo), ft(y_lo + 24), ft(GALLERY_TOP - GALLERY_T), ft(GALLERY_TOP))
for xb in range(132, 924, 24):
    xc = xb + 12; b = mirror_bay(xc)
    edges = [36, -36] if b >= 3 else []
    if b in AVENUE_VOID_BAYS or b in STAIR_BAYS: edges += [60, 108, -60, -108]
    for ye in edges:
        H = ft(3.06)
        bm_box(rbm, ft(xb), ft(xb + 24), ft(ye) - inch(1.5), ft(ye) + inch(1.5), ft(GALLERY_TOP), ft(GALLERY_TOP) + H)
        for k in range(5):
            x = xb + 6 * k
            bm_box(rbm, ft(x) - inch(1.2), ft(x) + inch(1.2), ft(ye) - inch(1.2), ft(ye) + inch(1.2), ft(GALLERY_TOP), ft(GALLERY_TOP) + H)
new_obj("EGAL_FLOORS", finish(gbm, "egal_floors", WOOD), C["GALLERIES"], props={"part_kind": "gallery_floor"})
new_obj("EGAL_RAILS", finish(rbm, "egal_rails", IRON), C["RAILINGS"], props={"part_kind": "balustrade"})
STAIR_RISE_LAND = 137.5 / 12
def mesh_flight(run_ft, rise_ft, width_ft, name):
    bm = bmesh.new(); n = max(2, round(rise_ft / (6.5 / 12))); g = run_ft / n; r = rise_ft / n; w = width_ft
    for k in range(n):
        bm_box(bm, ft(-w/2), ft(w/2), ft(k * g), ft((k + 1) * g + 0.1), ft((k + 1) * r - 0.12), ft((k + 1) * r))
    for sx in (-1, 1):
        bm_bar(bm, (ft(sx * w/2), 0, ft(0.4)), (ft(sx * w/2), ft(run_ft), ft(rise_ft + 0.4)), inch(2), inch(11))
    return finish(bm, name, WOOD)
LIBM["flight"] = mesh_flight(20, STAIR_RISE_LAND, 7.0, "stair_flight")
LIBM["flight2"] = mesh_flight(20, GALLERY_TOP - STAIR_RISE_LAND, 7.0, "stair_flight_upper")
def slab(name, x0, x1, y0, y1, z_top, t, mat, coll_, **props):
    bm = bmesh.new(); bm_box(bm, ft(x0), ft(x1), ft(y0), ft(y1), ft(z_top - t), ft(z_top))
    return new_obj(name, finish(bm, name, mat), coll_, props=props)
stairs = 0
for xb in range(132, 924, 24):
    xc = xb + 12
    if mirror_bay(xc) not in STAIR_BAYS: continue
    for sy in (-1, 1):
        xg0, xg1 = xc - 24, xc + 24          # 48 x 24 ft cross gallery straddling the stair bay (Claude's scheme)
        y0, y1 = sorted((sy * 60, sy * 108))
        for (xa, xbb) in ((xg0, xc - 4), (xc + 4, xg1)):
            slab(f"EXGAL_{xc:+.0f}{sy:+d}_{xa:+.0f}", xa, xbb, y0, y1, GALLERY_TOP, GALLERY_T, WOOD, C["GALLERIES"], part_kind="gallery_floor")
        ym0, ym1 = sorted((sy * 80, sy * 88))
        slab(f"ESTLAND_{xc:+.0f}{sy:+d}", xc - 12, xc + 12, ym0, ym1, STAIR_RISE_LAND, 0.5, WOOD, C["GALLERIES"], part_kind="stair_landing")
        rot_out = 0.0 if sy > 0 else math.pi
        for dx in (-7.75, 7.75):
            place("flight", f"ESTFL_{xc:+.0f}{sy:+d}_{dx:+.0f}", C["GALLERIES"], xc + dx, sy * 60, 0, rot_out, part_kind="stair_flight")
        place("flight2", f"ESTFU_{xc:+.0f}{sy:+d}_IN", C["GALLERIES"], xc, sy * 80, STAIR_RISE_LAND, rot_out + math.pi, part_kind="stair_flight")
        place("flight2", f"ESTFU_{xc:+.0f}{sy:+d}_OUT", C["GALLERIES"], xc, sy * 88, STAIR_RISE_LAND, rot_out, part_kind="stair_flight")
        stairs += 1

# ---------------- floor and ground ----------------
slab("EFLOOR_BOARDS", 132, 936, -Y_HALF, Y_HALF, 0.002 / FT, 0.5, FLOORM, C["FLOOR"], part_kind="floor_ground")
slab("EFLOOR_STRIP", STRIP_X0, STRIP_X1, Y_HALF, STRIP_Y1, 0.002 / FT, 0.5, FLOORM, C["FLOOR"], part_kind="floor_ground")
bm = bmesh.new(); bm_box(bm, ft(-9000), ft(9000), ft(-9000), ft(9000), -0.30, -0.02)
new_obj("EGROUND_PARK", finish(bm, "ground", GRASS), C["GROUND"], props={"part_kind": "ground"})
# gravel apron round the building (the drive / path seen in Plate IV and the Dickinson views)
bm = bmesh.new(); bm_box(bm, ft(-960), ft(960), ft(-240), ft(290), -0.02, -0.005)
GRAVEL = mat_principled("GT_Gravel", (0.50, 0.46, 0.38), 0.95)
new_obj("EGRAVEL_APRON", finish(bm, "gravel", GRAVEL), C["GROUND"], props={"part_kind": "ground"})

# ---------------- walls (Plate XXI ground tier; Plates IV, V upper tiers) ----------------
DOOR = mat_principled("GT_DoorPaint", (0.20, 0.17, 0.13), 0.7)
def mesh_wall_bay(width_ft, height_ft, boarded):
    """24 ft bay between iron columns, three 8 ft compartments split by timber posts (Plate XXI); round-headed sashes.
    Ground tier: vertical boarding with iron louvres top and bottom. Upper tiers: glazed arched panels."""
    bm = bmesh.new(); W = width_ft; H = height_ft; n = int(round(W / 8)); pw = W / n
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
            bm_bar(bm, (ft(xa), 0, ft(za)), (ft(xb), 0, ft(zb)), inch(2), inch(3.5))
        if not boarded:
            bm_box(bm, ft(xc) - inch(1), ft(xc) + inch(1), -inch(1), inch(1), ft(0.5), ft(head_c))
            for zz in (H * 0.33, H * 0.62):
                bm_box(bm, ft(xc - pw/2), ft(xc + pw/2), -inch(1), inch(1), ft(zz) - inch(1), ft(zz) + inch(1))
        else:   # boarding battens
            for j in range(1, 8):
                xx = xc - pw/2 + pw * j / 8
                bm_box(bm, ft(xx) - inch(0.6), ft(xx) + inch(0.6), -inch(1.2), inch(1.2), ft(0.5), ft(H) - inch(5))
    me = finish(bm, f"wall_{W}_{H:.2f}_{'b' if boarded else 'g'}", WOOD)
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    v = [bm.verts.new(p) for p in [(ft(-W/2), 0, ft(0.5)), (ft(W/2), 0, ft(0.5)), (ft(W/2), 0, ft(H)), (ft(-W/2), 0, ft(H))]]
    f = bm.faces.new(v)
    for lp in f.loops: lp[uvl].uv = (lp.vert.co.x / FT, lp.vert.co.z / FT)
    me2 = finish(bm, me.name + "_fill", WOODDARK if boarded else GLASS_PLAIN)
    return me, me2
def mesh_louvre():
    bm = bmesh.new()
    for k in range(4):
        z = 0.3 + 0.55 * k
        bm_bar(bm, (ft(-12), -inch(2), ft(z)), (ft(12), inch(2), ft(z) + inch(4)), inch(5), inch(0.5))
    return finish(bm, "wall_louvre", IRON)
LIBM["louv"] = mesh_louvre()
def mesh_doors():
    bm = bmesh.new()
    for k in range(3):
        xc = -8 + 8 * k
        bm_box(bm, ft(xc - 3.5), ft(xc + 3.5), -inch(4), inch(4), 0, ft(11.5))
    return finish(bm, "doors24", DOOR)
LIBM["doors"] = mesh_doors()
walls = []
def wall_run(x0, y0, x1, y1, z0, z1, boarded, tag, louvre=None, doors=()):
    """infill between column lines (x0,y0)->(x1,y1) in 24 ft bays from z0 to z1 ft. Ground-tier boarding has louvre
    bands at the bottom and top (Plate XXI); glazed tiers have a louvre band at the top."""
    louvre = boarded if louvre is None else louvre
    L = math.hypot(x1 - x0, y1 - y0); n = max(1, round(L / 24))
    lb = 2.5 if louvre else 0.0; lo = 2.5 if boarded else 0.0
    H = z1 - z0 - lb - lo
    key = f"w{H:.2f}{boarded}"
    if key not in LIBM: LIBM[key], LIBM[key + "f"] = mesh_wall_bay(24, H, boarded)
    rot = math.pi / 2 if abs(x1 - x0) < 1e-6 else 0.0
    for k in range(n):
        xa = x0 + (x1 - x0) * (k + 0.5) / n; ya = y0 + (y1 - y0) * (k + 0.5) / n
        place(key, f"EWALL_{tag}_{k}", C["WALLS"], xa, ya, z0 + lo, rot, part_kind="wall", tag=tag)
        is_door = k in doors
        if is_door:
            place("doors", f"EDOOR_{tag}_{k}", C["WALLS"], xa, ya, 0, rot, part_kind="door", tag=tag)
            place(f"w{H:.2f}False" if f"w{H:.2f}False" in LIBM else key + "f", f"EWALLF_{tag}_{k}", C["WALLS"], xa, ya, z0 + lo, rot, part_kind="wall_fill", tag=tag)
        else:
            place(key + "f", f"EWALLF_{tag}_{k}", C["WALLS"], xa, ya, z0 + lo, rot, part_kind="wall_fill", tag=tag)
        if boarded:
            place("louv", f"ELOUVB_{tag}_{k}", C["WALLS"], xa, ya, z0, rot, part_kind="louvre")
        if louvre:
            place("louv", f"ELOUV_{tag}_{k}", C["WALLS"], xa, ya, z0 + lo + H, rot, part_kind="louvre")
    walls.append({"tag": tag, "from": [x0, y0], "to": [x1, y1], "z": [z0, z1], "boarded": boarded, "bays": n})
T1 = (0.0, GIRDER_TOP[0] - GIRDER_D); T2 = (GIRDER_TOP[0], GIRDER_TOP[1] - GIRDER_D); T3 = (GIRDER_TOP[1], GIRDER_TOP[2] - GIRDER_D)
# ground-tier sides (boarded), both halves -- west-half runs are tagged as overlay on Claude's frame
for s, tag in ((-1, "S"), (1, "N")):
    Y = s * Y_HALF
    runs = [(-X_END, -X_ARM), (X_ARM, X_END)] if s < 0 else [(-X_END, STRIP_X0), (STRIP_X1, X_END)]
    for xa, xb in runs:
        wall_run(xa, Y, xb, Y, *T1, True, f"{tag}1_{xa:+.0f}")
    for xa, xb in ((-X_END, -X_ARM), (X_ARM, X_END)):
        wall_run(xa, s * 132, xb, s * 132, *T2, False, f"{tag}2_{xa:+.0f}", louvre=True)
    for xa, xb in ((-X_END, -X_LF), (X_LF, X_END)):
        wall_run(xa, s * 60, xb, s * 60, *T3, False, f"{tag}3_{xa:+.0f}", louvre=True)
# north strip outer walls
wall_run(STRIP_X0, STRIP_Y1, STRIP_X1, STRIP_Y1, *T1, True, "NS1")
wall_run(STRIP_X0, Y_HALF, STRIP_X0, STRIP_Y1, *T1, True, "NSW")
wall_run(STRIP_X1, Y_HALF, STRIP_X1, STRIP_Y1, *T1, True, "NSE")
# end walls (Plate V): glazed arched panels in all three tiers, doors in the central three bays and the outer bays
for sx, tag in ((-1, "W"), (1, "E")):
    X = sx * X_END
    n1 = int(408 / 24); mid = n1 // 2
    wall_run(X, -Y_HALF, X, Y_HALF, *T1, False, f"{tag}1", louvre=True, doors=(0, 3, mid - 1, mid, mid + 1, n1 - 4, n1 - 1))   # Plate V: 7 doorways
    wall_run(X, -132, X, 132, *T2, False, f"{tag}2", louvre=True)
    wall_run(X, -60, X, 60, *T3, False, f"{tag}3", louvre=True)

# ---------------- cresting and finials along every tier edge (Plates IV, V) ----------------
cbm = bmesh.new(); fin = 0
def crest(x0, y0, x1, y1, z):
    global fin
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L
    px, py = -uy, ux
    for k in range(int(L / 2)):
        a = (ft(x0 + ux * 2 * k), ft(y0 + uy * 2 * k)); b = (ft(x0 + ux * 2 * (k + 1)), ft(y0 + uy * 2 * (k + 1)))
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        bm_bar(cbm, (a[0], a[1], ft(z)), (m[0], m[1], ft(z + 1.6)), inch(1), inch(1))
        bm_bar(cbm, (m[0], m[1], ft(z + 1.6)), (b[0], b[1], ft(z)), inch(1), inch(1))
    bm_bar(cbm, (ft(x0), ft(y0), ft(z + 0.15)), (ft(x1), ft(y1), ft(z + 0.15)), inch(2), inch(3))
    for k in range(int(round(L / 24)) + 1):
        x = x0 + ux * 24 * k; y = y0 + uy * 24 * k
        bm_cyl(cbm, inch(2.5), ft(z), ft(z + 4.5), 8, ft(x), ft(y))
        bm_cyl(cbm, inch(5), ft(z + 4.5), ft(z + 5.3), 8, ft(x), ft(y)); fin += 1
for s in (-1, 1):
    for xa, xb in ((-X_END, -X_ARM), (X_ARM, X_END)):
        crest(xa, s * Y_HALF, xb, s * Y_HALF, GIRDER_TOP[0]) if not (s > 0) else None
        crest(xa, s * 132, xb, s * 132, GIRDER_TOP[1])
    for xa, xb in ((-X_END, -X_LF), (X_LF, X_END)):
        crest(xa, s * 60, xb, s * 60, GIRDER_TOP[2])
for xa, xb in ((-X_END, STRIP_X0), (STRIP_X1, X_END)):
    crest(xa, Y_HALF, xb, Y_HALF, GIRDER_TOP[0])
crest(STRIP_X0, STRIP_Y1, STRIP_X1, STRIP_Y1, GIRDER_TOP[0])
crest(STRIP_X0, Y_HALF, STRIP_X0, STRIP_Y1, GIRDER_TOP[0]); crest(STRIP_X1, Y_HALF, STRIP_X1, STRIP_Y1, GIRDER_TOP[0])
for sx in (-1, 1):
    X = sx * X_END
    crest(X, -Y_HALF, X, Y_HALF, GIRDER_TOP[0]); crest(X, -132, X, 132, GIRDER_TOP[1]); crest(X, -60, X, 60, GIRDER_TOP[2])
new_obj("ECRESTING", finish(cbm, "cresting", IRON), C["CRESTING"], props={"part_kind": "cresting", "finials": fin})
# eaves boarding: a plain fascia under the cresting, the "entablature" band of Plate V (girder depth, painted)
fbm = bmesh.new()
def fascia(x0, y0, x1, y1, z):
    if abs(x1 - x0) < 1e-6: bm_box(fbm, ft(x0) - inch(4), ft(x0) + inch(4), ft(min(y0, y1)), ft(max(y0, y1)), ft(z - GIRDER_D), ft(z))
    else: bm_box(fbm, ft(min(x0, x1)), ft(max(x0, x1)), ft(y0) - inch(4), ft(y0) + inch(4), ft(z - GIRDER_D), ft(z))
for s in (-1, 1):
    for xa, xb in ((-X_END, -X_ARM), (X_ARM, X_END)):
        fascia(xa, s * 132, xb, s * 132, GIRDER_TOP[1])
        if s < 0: fascia(xa, s * Y_HALF, xb, s * Y_HALF, GIRDER_TOP[0])
    for xa, xb in ((-X_END, -X_LF), (X_LF, X_END)): fascia(xa, s * 60, xb, s * 60, GIRDER_TOP[2])
for xa, xb in ((-X_END, STRIP_X0), (STRIP_X1, X_END)): fascia(xa, Y_HALF, xb, Y_HALF, GIRDER_TOP[0])
fascia(STRIP_X0, STRIP_Y1, STRIP_X1, STRIP_Y1, GIRDER_TOP[0]); fascia(STRIP_X0, Y_HALF, STRIP_X0, STRIP_Y1, GIRDER_TOP[0]); fascia(STRIP_X1, Y_HALF, STRIP_X1, STRIP_Y1, GIRDER_TOP[0])
for sx in (-1, 1):
    X = sx * X_END; fascia(X, -Y_HALF, X, Y_HALF, GIRDER_TOP[0]); fascia(X, -132, X, 132, GIRDER_TOP[1]); fascia(X, -60, X, 60, GIRDER_TOP[2])
new_obj("EFASCIA", finish(fbm, "fascia", WOOD), C["CRESTING"], props={"part_kind": "fascia"})
# tag every west-half (x < -36 ft) wall / cresting part as an overlay on Claude's frame
for ob in bpy.data.objects:
    if ob.get("part_kind") in ("wall", "wall_fill", "louvre", "door") and ob.location.x < ft(-36):
        ob["claude_overlay"] = True
if MILESTONES:
    os.makedirs(MILESTONES, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(MILESTONES, "m01_east_frame_walls.blend"), compress=True)

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
scene.view_settings.exposure = -0.6     # whole-building views: glass roofs over ~19 acres clip at the transept setting (EX10)

# ---------------- cameras (storyboard v001 grammar) ----------------
CAMS = bpy.data.collections.new("CAMERAS_GROK"); scene.collection.children.link(CAMS)
def cam(name, loc_ft, look_ft, lens, ortho=None, sensor=36.0, clip_end_ft=None):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.sensor_width = sensor; cd.clip_start = 0.1
    cd.clip_end = ft(clip_end_ft) if clip_end_ft else 3000   # elevation-drawing cut (EX18)
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
            cam(f"{shot['id']}_{key}", shot[key]["pos_ft"], shot[key]["look_ft"], shot["lens_mm"], shot.get("ortho_m"), clip_end_ft=shot.get("clip_end_ft"))
scene.camera = bpy.data.objects.get("EXT_SE_34_start")

scene["grok_exterior_build"] = json.dumps({"parts": len(parts), "columns": len(cols), "roof_units": roof_n, "walls": walls,
                                           "stairs": stairs, "finials": fin, "seed": SEED, "colour": COLOUR})
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True)
print("SAVED", OUT, "parts", len(parts), "columns", len(cols), "roofs", roof_n, "stairs", stairs)
