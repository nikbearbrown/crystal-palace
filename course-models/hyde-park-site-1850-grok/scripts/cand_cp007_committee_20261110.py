"""CP007 'The answer that would not work' -- polish CANDIDATE 'committee' 2026-11-10 (DEPARTURES SD43-SD49; NOT live).
Run on the live rounds/s02.blend (never written; saves rounds/candidates/s02_cp007committee.blend):
  blender -b rounds/s02.blend -P scripts/cand_cp007_committee_20261110.py -- [--out PATH] [--fstop 8.0 (0 = no DOF)]
Hyde Park, spring 1850 only. Scoped to CP007: every new object is W7_-prefixed and base-hidden; grok_states CP007 shows
W7_ and hides CM_ (the objects it replaces). CP006/CP008/CP009 states already hide CM_ and never show W7_.
  * SD43-SD45 study model of the Building Committee's published design (layout: scripts/cp007_committee_layout.py),
    1:600 with TRUE heights (retires SD15's doubled heights for CP007); the live dome floated above its drum -- fixed.
  * SD46 baseboard with painted park, the drive, Kensington Road, Rotten Row and model trees.
  * SD47 planked deal worktable (CM_TABLE footprint/height), our own ground-plan sheet (scripts/cp007_plan_sheet.py,
    'not a facsimile'), paper rolls, scale, dividers, weights, inkstand; reworded label card fully in frame.
  * SD48 CP007-only spring sward (particle hair) on the ground seen behind the table.
  * SD49 CP007_start camera depth of field (f/8 on the model); position/rotation/lens unchanged.
"""
import bpy, bmesh, sys, os, math, random, json
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view as w2c

def arg(k, d=None):
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return a[a.index(k) + 1] if k in a else d
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
import cp007_committee_layout as Lo
TAG = "cp007_committee_20261110"; FT = 0.3048
sc = bpy.context.scene; rnd = random.Random(1850)
coll = bpy.data.collections.new("CP007W"); sc.collection.children.link(coll)
def link(o):
    coll.objects.link(o); o.hide_render = True; o[TAG] = True; return o

# ---------------- materials ----------------
def newmat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(b.outputs[0], out.inputs[0]); return m, nt, b, out
def tex(nt, scale, detail=4.0, rough=0.55, coord="Object"):
    tc = nt.nodes.new("ShaderNodeTexCoord"); n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = detail; n.inputs["Roughness"].default_value = rough
    nt.links.new(tc.outputs[coord], n.inputs["Vector"]); return n
def ramp(nt, fac, cols):
    r = nt.nodes.new("ShaderNodeValToRGB"); e = r.color_ramp
    e.elements[0].position, e.elements[0].color = cols[0][0], (*cols[0][1], 1)
    e.elements[1].position, e.elements[1].color = cols[-1][0], (*cols[-1][1], 1)
    for p, c in cols[1:-1]: el = e.elements.new(p); el.color = (*c, 1)
    nt.links.new(fac, r.inputs[0]); return r.outputs[0]
def mottled(name, c0, c1, scale, rough=0.8, metal=0.0, bump=0.0, coord="Object", spec=0.5):
    m, nt, b, out = newmat(name); n = tex(nt, scale, coord=coord); b.inputs["Specular IOR Level"].default_value = spec
    nt.links.new(ramp(nt, n.outputs["Fac"], [(0.3, c0), (0.7, c1)]), b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if bump:
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump; bp.inputs["Distance"].default_value = 0.0005
        nt.links.new(n.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs[0], b.inputs["Normal"])
    m.diffuse_color = (*c0, 1); return m
BRICK = mottled("W7_ModelBrickRed", (0.30, 0.13, 0.08), (0.38, 0.18, 0.11), 900, spec=0.1)      # painted card, brick red
PANEL = mottled("W7_ModelPanelBuff", (0.40, 0.30, 0.18), (0.46, 0.35, 0.22), 900, spec=0.1)     # second colour of the panels
STONE = mottled("W7_ModelDressing", (0.46, 0.42, 0.33), (0.52, 0.48, 0.38), 900, spec=0.1)      # cornices, pilasters, arches
SLATE = mottled("W7_ModelSlate", (0.042, 0.039, 0.037), (0.058, 0.054, 0.05), 600, rough=0.92, spec=0.0)
SKY = mottled("W7_ModelSkylight", (0.07, 0.074, 0.078), (0.09, 0.094, 0.098), 400, rough=0.4, spec=0.15)
LEAD = mottled("W7_ModelDomeIron", (0.065, 0.066, 0.068), (0.085, 0.086, 0.088), 300, rough=0.7, metal=0.0, spec=0.05)
RIB = mottled("W7_ModelDomeRib", (0.13, 0.13, 0.13), (0.16, 0.16, 0.155), 300, rough=0.6, metal=0.0, spec=0.08)
DARK = mottled("W7_ModelOpening", (0.025, 0.025, 0.03), (0.04, 0.04, 0.045), 500, rough=0.35)
GLASSEYE = mottled("W7_ModelEye", (0.55, 0.60, 0.64), (0.66, 0.70, 0.72), 200, rough=0.15, metal=0.5)
PARKB = mottled("W7_ModelParkBaize", (0.085, 0.125, 0.045), (0.12, 0.165, 0.065), 140, rough=0.95, bump=0.25, spec=0.05)
ROAD = mottled("W7_ModelRoadSand", (0.19, 0.155, 0.10), (0.23, 0.19, 0.125), 220, rough=0.95, spec=0.05)
FLOOR = mottled("W7_ModelCourtGravel", (0.22, 0.19, 0.14), (0.26, 0.23, 0.17), 300, rough=0.95, spec=0.2)
TREE = mottled("W7_ModelTreeLichen", (0.045, 0.085, 0.03), (0.10, 0.15, 0.055), 2600, rough=0.95, bump=0.6, spec=0.05)
TRUNK = mottled("W7_ModelTreeTrunk", (0.10, 0.07, 0.05), (0.14, 0.10, 0.07), 300)
BOARD = mottled("W7_BaseboardStained", (0.16, 0.09, 0.05), (0.23, 0.14, 0.08), 40, rough=0.5)
WATER = mottled("W7_ModelFountain", (0.30, 0.36, 0.40), (0.38, 0.44, 0.48), 200, rough=0.1, metal=0.4)
def deal_mat(name, lo, hi):
    m, nt, b, _ = newmat(name)
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1.0, 18.0, 1.0)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    w = nt.nodes.new("ShaderNodeTexWave"); w.wave_type = "BANDS"; w.bands_direction = "Y"; w.inputs["Scale"].default_value = 14.0
    w.inputs["Distortion"].default_value = 3.0; w.inputs["Detail"].default_value = 3.0; w.inputs["Detail Scale"].default_value = 2.0
    nt.links.new(mp.outputs[0], w.inputs["Vector"])
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 6.0; nt.links.new(mp.outputs[0], n.inputs["Vector"])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "FLOAT"; mx.inputs[0].default_value = 0.22
    nt.links.new(w.outputs["Fac"], mx.inputs[2]); nt.links.new(n.outputs["Fac"], mx.inputs[3])
    nt.links.new(ramp(nt, mx.outputs[0], [(0.25, lo), (0.55, hi), (0.85, tuple(c * 0.92 for c in hi))]), b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.62; b.inputs["Specular IOR Level"].default_value = 0.22
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.08; nt.links.new(w.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs[0], b.inputs["Normal"]); m.diffuse_color = (*hi, 1); return m
DEAL = deal_mat("W7_DealPlanks", (0.23, 0.115, 0.035), (0.34, 0.19, 0.07))
DEALDK = deal_mat("W7_DealTrestle", (0.15, 0.085, 0.04), (0.23, 0.14, 0.065))
PAPER = mottled("W7_Paper", (0.33, 0.28, 0.18), (0.38, 0.32, 0.21), 30, rough=0.85, spec=0.3)
TAPE = mottled("W7_TapeRed", (0.38, 0.06, 0.04), (0.44, 0.09, 0.06), 80)
BOX = mottled("W7_Boxwood", (0.60, 0.46, 0.22), (0.66, 0.52, 0.27), 60, rough=0.4)
BRASS = mottled("W7_Brass", (0.55, 0.40, 0.15), (0.62, 0.47, 0.20), 50, rough=0.3, metal=1.0)
STEEL = mottled("W7_Steel", (0.45, 0.45, 0.45), (0.52, 0.52, 0.52), 50, rough=0.3, metal=1.0)
LEADW = mottled("W7_LeadWeight", (0.16, 0.16, 0.17), (0.22, 0.22, 0.23), 50, rough=0.5, metal=0.6)
INK = mottled("W7_InkGlass", (0.015, 0.02, 0.03), (0.03, 0.035, 0.05), 50, rough=0.08)
CARD = mottled("W7_LabelCard", (0.37, 0.33, 0.24), (0.40, 0.36, 0.26), 40, rough=0.8, spec=0.3)
INKT = mottled("W7_LabelInk", (0.03, 0.025, 0.02), (0.04, 0.03, 0.025), 40, rough=0.6)
def sheet_mat():
    m, nt, b, _ = newmat("W7_PlanSheet"); t = nt.nodes.new("ShaderNodeTexImage")
    t.image = bpy.data.images.load(os.path.join(ROOT, "textures", "cp007_committee_plan_sheet.png")); t.image.pack()
    g = nt.nodes.new("ShaderNodeMix"); g.data_type = "RGBA"; g.blend_type = "MULTIPLY"; g.inputs[0].default_value = 1.0
    g.inputs[7].default_value = (0.52, 0.47, 0.38, 1); nt.links.new(t.outputs[0], g.inputs[6]); nt.links.new(g.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.85; b.inputs["Specular IOR Level"].default_value = 0.2; return m
SHEET = sheet_mat()

# ---------------- mesh helpers (bmesh with per-face material index) ----------------
class MB:
    def __init__(s, mats): s.bm = bmesh.new(); s.mats = mats
    def mi(s, m): return s.mats.index(m)
    def poly(s, pts, m):
        vs = [s.bm.verts.new(p) for p in pts]; f = s.bm.faces.new(vs); f.material_index = s.mi(m); return f
    def box(s, x0, x1, y0, y1, z0, z1, m, M=None):
        if x1 < x0: x0, x1 = x1, x0
        if y1 < y0: y0, y1 = y1, y0
        r = bmesh.ops.create_cube(s.bm, size=1.0, matrix=Matrix.Translation(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)) @ Matrix.Diagonal((x1 - x0, y1 - y0, z1 - z0, 1)))
        if M is not None: bmesh.ops.transform(s.bm, matrix=M, verts=r["verts"])
        for f in {f for v in r["verts"] for f in v.link_faces}: f.material_index = s.mi(m)
    def prism(s, prof, y0, y1, m, axis="y"):
        """extrude a closed (x,z) profile along y (or along x for axis='x', profile given as (y,z))."""
        def P(a, z, t): return (a, t, z) if axis == "y" else (t, a, z)
        A = [s.bm.verts.new(P(a, z, y0)) for a, z in prof]; B = [s.bm.verts.new(P(a, z, y1)) for a, z in prof]
        n = len(prof); fs = [s.bm.faces.new(A[::-1]), s.bm.faces.new(B)]
        for i in range(n): fs.append(s.bm.faces.new([A[i], A[(i + 1) % n], B[(i + 1) % n], B[i]]))
        for f in fs: f.material_index = s.mi(m)
    def lathe(s, prof, seg, m, cx, cy, z0=0.0, a0=0.0, a1=2 * math.pi):
        full = abs(a1 - a0 - 2 * math.pi) < 1e-6; nseg = seg if full else seg + 1
        rings = [[s.bm.verts.new((cx + r * math.cos(a0 + (a1 - a0) * k / seg), cy + r * math.sin(a0 + (a1 - a0) * k / seg), z0 + z)) for (r, z) in prof] for k in range(nseg)]
        for k in range(seg):
            R0, R1 = rings[k], rings[(k + 1) % nseg]
            for i in range(len(prof) - 1):
                f = s.bm.faces.new([R0[i], R1[i], R1[i + 1], R0[i + 1]]); f.material_index = s.mi(m)
    def obj(s, name, loc=(0, 0, 0), scale=1.0, smooth=False):
        bmesh.ops.remove_doubles(s.bm, verts=s.bm.verts, dist=1e-6)
        me = bpy.data.meshes.new(name); s.bm.normal_update(); s.bm.to_mesh(me); s.bm.free()
        for m in s.mats: me.materials.append(m)
        if smooth:
            for p in me.polygons: p.use_smooth = True
        o = bpy.data.objects.new(name, me); o.location = loc; o.scale = (scale, scale, scale); return link(o)

# ---------------- table placement (same footprint/height as CM_TABLE) ----------------
T = bpy.data.objects["CM_TABLE"]; tv = [T.matrix_world @ v.co for v in T.data.vertices]
TX0, TX1 = min(v.x for v in tv), max(v.x for v in tv); TY0, TY1 = min(v.y for v in tv), max(v.y for v in tv)
TZ = max(v.z for v in tv); TZB = min(v.z for v in tv); TCX, TCY = (TX0 + TX1) / 2, (TY0 + TY1) / 2
print("W7 table", round(TX0, 3), round(TX1, 3), round(TY0, 3), round(TY1, 3), round(TZ, 3))
cam = bpy.data.objects["CP007_start"]

# SD45 planked deal table: 4 boards along the length on two cleats, two splayed trestles
mb = MB([DEAL, DEALDK]); TH = 0.032; nb = 4; bw = (TY1 - TY0) / nb
for k in range(nb):
    y0 = TY0 + k * bw + 0.0015; y1 = TY0 + (k + 1) * bw - 0.0015; dz = rnd.uniform(-0.0012, 0.0008)
    mb.box(TX0, TX1, y0, y1, TZ - TH + dz, TZ + dz, DEAL)
for xs in (TX0 + 0.28, TX1 - 0.28):
    mb.box(xs - 0.035, xs + 0.035, TY0 + 0.05, TY1 - 0.05, TZ - TH - 0.045, TZ - TH, DEALDK)          # cleat / trestle head
    for sy in (-1, 1):
        for sx in (-1, 1):
            top = Vector((xs, TCY + sy * 0.36, TZ - TH - 0.045)); foot = Vector((xs + sx * 0.16, TCY + sy * 0.40, TZB + 0.06))
            d = foot - top; L = d.length; R = d.to_track_quat("Z", "Y").to_matrix().to_4x4()
            mb.box(-0.025, 0.025, -0.03, 0.03, 0, L, DEALDK, M=Matrix.Translation(top) @ R)
    mb.box(xs - 0.02, xs + 0.02, TCY - 0.38, TCY + 0.38, TZB + 0.25, TZB + 0.31, DEALDK)                  # stretcher
mb.obj("W7_TABLE")

# ---------------- model placement: centre it in frame at mid-model depth ----------------
K = FT / 600.0                         # 1:600, true heights (SD43)
BASE_T = 0.014                         # baseboard thickness (m)
BU0, BU1, BV0, BV1 = -70.0, Lo.L + 70.0, -200.0, 560.0
MY = TCY + 0.02                        # model v-centre (building centre v=209) a little behind the table centre line
def mx_for_centre():
    lo, hi = TX0, TX1
    for _ in range(40):
        mid = (lo + hi) / 2; p = w2c(sc, cam, Vector((mid, MY, TZ + 0.03)))
        if p.x < 0.5: lo = mid
        else: hi = mid
    return (lo + hi) / 2
MX = mx_for_centre()
U0, V0 = Lo.L / 2, 209.0               # model origin in plan feet
ORG = Vector((MX - U0 * K, MY - V0 * K, TZ + BASE_T))     # world position of plan (0,0) at base top
print("W7 model origin", tuple(round(c, 4) for c in ORG), "centre x", round(MX, 4))

# SD44 baseboard: stained board edge + painted park top, roads, Rotten Row
mb = MB([BOARD, PARKB, ROAD])
mb.box(BU0, BU1, BV0, BV1, -BASE_T / K, -0.6, BOARD)
mb.box(BU0 + 4, BU1 - 4, BV0 + 4, BV1 - 4, -0.6, 0.0, PARKB)
mb.box(BU0 + 6, BU1 - 6, Lo.ROAD_DRIVE_V - 20, Lo.ROAD_DRIVE_V + 20, 0.0, 0.25, ROAD)
mb.box(BU0 + 6, BU1 - 6, Lo.ROAD_KENS_V - 26, Lo.ROAD_KENS_V + 26, 0.0, 0.25, ROAD)
mb.box(BU0 + 6, BU1 - 6, Lo.ROTTEN_ROW_V + 20, Lo.ROTTEN_ROW_V + 80, 0.0, 0.25, ROAD)          # Rotten Row, 60 ft sand ride
mb.box(Lo.ROT_U - 40, Lo.ROT_U + 40, Lo.ROAD_DRIVE_V + 20, -15.0, 0.0, 0.25, ROAD)               # carriage sweep to the principal entrance
mb.obj("W7_MODEL_BASE", loc=ORG, scale=K)

# SD43 building
mb = MB([BRICK, PANEL, STONE, SLATE, SKY, LEAD, RIB, DARK, GLASSEYE, FLOOR, WATER])
# avenue strips: brick-filled shed body to the eaves + slate pitched roof + glazed apex skylight
for (u0, u1, v0, v1) in Lo.strips():
    uc = (u0 + u1) / 2; hw = (u1 - u0) / 2
    mb.box(u0, u1, v0, v1, 0.0, Lo.EAVE, BRICK)
    mb.prism([(u0, Lo.EAVE), (u1, Lo.EAVE), (uc, Lo.RIDGE)], v0, v1, SLATE)
    mb.prism([(uc - 3.0, Lo.RIDGE - 0.75 * 3.0 / hw * 6), (uc + 3.0, Lo.RIDGE - 0.75 * 3.0 / hw * 6), (uc + 3.0, Lo.RIDGE + 0.9), (uc - 3.0, Lo.RIDGE + 0.9)], v0 + 2, v1 - 2, SKY)
# main avenue: semicircular ribbed roof, 52 ft crown, glazed crown band, 24 ft rib bands
def barrel(ua, ub):
    v0, v1 = Lo.MAIN_V; vc = (v0 + v1) / 2; r = (v1 - v0) / 2
    mb.box(ua, ub, v0, v1, 0.0, Lo.MAIN_SPRING, BRICK)
    prof = [(vc + r * math.cos(t), Lo.MAIN_SPRING + r * math.sin(t)) for t in [math.pi * k / 16 for k in range(17)]]
    mb.prism(prof, ua, ub, SLATE, axis="x")
    band = [(vc + (r + 0.4) * math.cos(t), Lo.MAIN_SPRING + (r + 0.4) * math.sin(t)) for t in [math.pi * (0.38 + 0.24 * k / 6) for k in range(7)]]
    band = band + [(vc + (r - 0.2) * math.cos(t), Lo.MAIN_SPRING + (r - 0.2) * math.sin(t)) for t in [math.pi * (0.62 - 0.24 * k / 6) for k in range(7)]]
    mb.prism(band, ua + 2, ub - 2, SKY, axis="x")
    u = ua + 24.0
    while u < ub - 1:
        rib = [(vc + (r + 0.9) * math.cos(t), Lo.MAIN_SPRING + (r + 0.9) * math.sin(t)) for t in [math.pi * k / 16 for k in range(17)]]
        rib += [(vc + (r - 0.1) * math.cos(t), Lo.MAIN_SPRING + (r - 0.1) * math.sin(t)) for t in [math.pi * (16 - k) / 16 for k in range(17)]]
        mb.prism(rib, u - 0.8, u + 0.8, RIB, axis="x"); u += 24.0
    for uu in (ua, ub):  # gable end walls where the vault meets the drum / end pavilions
        pass
hc = (Lo.ROT_R ** 2 - 24.0 ** 2) ** 0.5
barrel(20.0, Lo.ROT_U - hc + 4.0); barrel(Lo.ROT_U + hc - 4.0, Lo.L - 20.0)
# perimeter: 15 ft corridor + enclosing brick wall band (20 ft deep) with two-colour panels, cornice, windows
def wall_run(axis, a0, a1, c, outward, h=Lo.WALL_H):
    """axis 'u': wall along u at v=c, outward +1 (north) / -1 (south). axis 'v': wall along v at u=c, outward +-1."""
    d0, d1 = (c, c - 20.0 * outward) if True else (0, 0)
    if axis == "u": mb.box(a0, a1, d0, d1, 0.0, h, BRICK); mb.box(a0, a1, d0, d1, h - 0.3, h + 1.2, STONE)
    else: mb.box(d0, d1, a0, a1, 0.0, h, BRICK); mb.box(d0, d1, a0, a1, h - 0.3, h + 1.2, STONE)
    f = c + 0.35 * outward                                           # outer face plane
    n = int((a1 - a0) // 24.0)
    for k in range(n):
        s0 = a0 + k * 24.0
        if axis == "u":
            mb.box(s0 + 3.0, s0 + 21.0, f, f + 0.25 * outward, 4.0, h - 4.0, PANEL)          # buff panel (second colour)
            mb.box(s0 + 8.0, s0 + 16.0, f + 0.25 * outward, f + 0.5 * outward, 7.0, h - 8.0, DARK)  # tall window
            mb.box(s0 - 1.0, s0 + 1.0, f, f + 0.6 * outward, 0.0, h, STONE)                  # pilaster at the column line
        else:
            mb.box(f, f + 0.25 * outward, s0 + 3.0, s0 + 21.0, 4.0, h - 4.0, PANEL)
            mb.box(f + 0.25 * outward, f + 0.5 * outward, s0 + 8.0, s0 + 16.0, 7.0, h - 8.0, DARK)
            mb.box(f, f + 0.6 * outward, s0 - 1.0, s0 + 1.0, 0.0, h, STONE)
wall_run("u", 0.0, Lo.ROT_U - 60.0, 0.0, -1); wall_run("u", Lo.ROT_U + 60.0, Lo.L, 0.0, -1)
for (a, b, v) in Lo.NORTH:
    segs = [(a, b)]
    for (ca, cb, cv0, cv1, k) in Lo.COURTS:
        if cv1 >= v - 1: segs = [s for s0 in segs for s in ((s0[0], min(s0[1], ca)), (max(s0[0], cb), s0[1])) if s[1] - s[0] > 2]
    for (s0, s1) in segs: wall_run("u", s0, s1, v, +1)
for (a, b, v), (a2, b2, v2) in zip(Lo.NORTH, Lo.NORTH[1:]):       # short return walls at the north steps
    lo, hi = sorted((v, v2)); wall_run("v", lo - 20.0, hi, b, +1 if v2 < v else -1)
wall_run("v", 0.0, Lo.NORTH[0][2], 0.0, -1); wall_run("v", 0.0, Lo.NORTH[-1][2], Lo.L, +1)
# north filler between strip ends and the north wall (corridor roof, flat lead)
for (u0, u1, v0, v1) in Lo.strips():
    pass
# courts: gravel floor, low covered way round the octagon, fountain in the small court
for (a, b, c, e, k) in Lo.COURTS:
    mb.box(a, b, c, e, 0.0, 0.4, FLOOR)
    for (x0, x1, y0, y1) in ((a, b, c, c + 12), (a, a + 12, c, e), (b - 12, b, c, e)):   # covered way (15 ft high, slate)
        mb.box(x0, x1, y0, y1, 0.0, 14.0, BRICK); mb.box(x0, x1, y0, y1, 14.0, 16.0, SLATE)
    if k == "octagon":
        cu, cv = (a + b) / 2, (c + e) / 2 - 6; R = 80.0
        oct_ = [(R * math.cos(math.pi / 8 + i * math.pi / 4), R * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
        for i in range(8):
            (x0, y0), (x1, y1) = oct_[i], oct_[(i + 1) % 8]
            d = Vector((x1 - x0, y1 - y0, 0)); L = d.length; ang = math.atan2(d.y, d.x)
            M = Matrix.Translation((cu + x0, cv + y0, 0)) @ Matrix.Rotation(ang, 4, "Z")
            mb.box(0, L, -6, 0, 0.0, 15.0, BRICK, M=M); mb.box(0, L, -6.5, 0.5, 15.0, 16.5, SLATE, M=M)
    if k == "small":
        cu, cv = (a + b) / 2, (c + e) / 2
        mb.lathe([(0, 0.4), (14, 0.4), (14, 2.0), (12.5, 2.0), (12.5, 1.0), (0, 1.0)], 24, STONE, cu, cv)
        mb.lathe([(0, 1.05), (12.4, 1.05)], 24, WATER, cu, cv)
        mb.lathe([(2.0, 1.0), (1.2, 9.0), (3.5, 9.5), (0, 10.5)], 12, STONE, cu, cv)
# rotunda: brick drum with clerestory band + cornice, ribbed iron dome, glazed eye with a lantern ring
R = Lo.ROT_R
mb.lathe([(R - 6, 0.0), (R, 0.0), (R, Lo.DRUM_H - 3.0), (R + 2.0, Lo.DRUM_H - 3.0), (R + 2.0, Lo.DRUM_H), (R - 6, Lo.DRUM_H)], 96, BRICK, Lo.ROT_U, Lo.ROT_V)
mb.lathe([(R + 0.3, Lo.RIDGE + 2.0), (R + 0.3, Lo.RIDGE + 3.0)], 96, STONE, Lo.ROT_U, Lo.ROT_V)
mb.lathe([(R + 2.2, Lo.DRUM_H - 3.0), (R + 2.2, Lo.DRUM_H + 0.2)], 96, STONE, Lo.ROT_U, Lo.ROT_V)
NW = 48
for i in range(NW):                                                        # clerestory windows
    a = 2 * math.pi * (i + 0.5) / NW
    M = Matrix.Translation((Lo.ROT_U + (R + 0.15) * math.cos(a), Lo.ROT_V + (R + 0.15) * math.sin(a), 0)) @ Matrix.Rotation(a, 4, "Z")
    mb.box(-0.3, 0.3, -3.6, 3.6, Lo.DRUM_H - 15.0, Lo.DRUM_H - 5.0, DARK, M=M)
    mb.box(-0.1, 0.5, -0.9, 0.9, Lo.RIDGE + 3.0, Lo.DRUM_H - 3.0, STONE, M=Matrix.Translation((Lo.ROT_U + R * math.cos(a + math.pi / NW), Lo.ROT_V + R * math.sin(a + math.pi / NW), 0)) @ Matrix.Rotation(a + math.pi / NW, 4, "Z"))
EYE = 24.0; RISE = Lo.DOME_TOP - Lo.DRUM_H - 4.0
def dome_r(t):   # t 0..1 from spring to eye; slightly stilted ellipse, like the p.24 view
    th = t * math.acos(EYE / R); return R * math.cos(th), Lo.DRUM_H + RISE * math.sin(th) / math.sin(math.acos(EYE / R))
prof = [dome_r(k / 24) for k in range(25)]
mb.lathe([(r, z) for r, z in prof] + [(EYE - 2.0, prof[-1][1])], 96, LEAD, Lo.ROT_U, Lo.ROT_V)
NR = 64
for i in range(NR):                                                         # wrought-iron ribs (raised strips)
    a = 2 * math.pi * i / NR; ca, sa = math.cos(a), math.sin(a); ta = Vector((-sa, ca, 0)) * 0.9
    pts = [dome_r(k / 16) for k in range(17)]
    for (r0, z0), (r1, z1) in zip(pts, pts[1:]):
        o0 = Vector((Lo.ROT_U + (r0 + 0.6) * ca, Lo.ROT_V + (r0 + 0.6) * sa, z0)); o1 = Vector((Lo.ROT_U + (r1 + 0.6) * ca, Lo.ROT_V + (r1 + 0.6) * sa, z1))
        q = [o0 - ta, o0 + ta, o1 + ta, o1 - ta]; n = Vector((ca, sa, 0)) * 0.7
        vs = [mb.bm.verts.new(p) for p in q] + [mb.bm.verts.new(p + n) for p in q]
        for f in ([4, 5, 6, 7], [0, 4, 7, 3], [1, 2, 6, 5]):
            ff = mb.bm.faces.new([vs[j] for j in f]); ff.material_index = mb.mi(RIB)
ztop = prof[-1][1]
mb.lathe([(EYE - 2.0, ztop), (EYE - 2.0, ztop + 2.5), (EYE - 4.0, ztop + 2.5)], 48, RIB, Lo.ROT_U, Lo.ROT_V)
mb.lathe([(0, ztop + 2.0), (EYE - 4.0, ztop + 2.0)], 48, GLASSEYE, Lo.ROT_U, Lo.ROT_V)
mb.lathe([(EYE * 0.45, ztop + 2.0), (EYE * 0.45, ztop + 6.5), (EYE * 0.48, ztop + 7.0), (0, ztop + 7.5)], 24, RIB, Lo.ROT_U, Lo.ROT_V)
# arched entrance pavilions (gabled block, buff dressings, dark arched recess with radial glazing bars)
def pavilion(u, v, face, w, eave, gtop, ar, asp, dep):
    if face in "SN":
        s = -1 if face == "S" else 1
        M = Matrix.Translation((u, v, 0)) @ (Matrix.Identity(4) if face == "S" else Matrix.Rotation(math.pi, 4, "Z"))
    else:
        M = Matrix.Translation((u, v, 0)) @ Matrix.Rotation(-math.pi / 2 if face == "W" else math.pi / 2, 4, "Z")
    # local frame: x along the face, -y outward, block from y=-dep (outer face) to y=+40 (into the building)
    def B(x0, x1, y0, y1, z0, z1, m): mb.box(x0, x1, y0, y1, z0, z1, m, M=M)
    hw = w / 2
    B(-hw, hw, -dep, 40.0, 0.0, eave, BRICK)
    B(-hw - 1, hw + 1, -dep - 1, 40.0, eave - 1.0, eave + 1.0, STONE)
    for sx in (-1, 1): B(sx * hw - (4 if sx > 0 else -4), sx * hw, -dep - 1.2, -dep, 0.0, eave, STONE)
    # gable (triangular prism, slate roof) with buff verge
    gm = MB([]); pr = [(-hw - 1.5, eave + 1.0), (hw + 1.5, eave + 1.0), (0.0, gtop)]
    vs0 = [mb.bm.verts.new(M @ Vector((x, -dep - 0.6, z))) for x, z in pr]; vs1 = [mb.bm.verts.new(M @ Vector((x, 40.0, z))) for x, z in pr]
    for f, m in (([vs0[2], vs0[1], vs0[0]], PANEL), ([vs1[0], vs1[1], vs1[2]], BRICK), ([vs0[0], vs0[1], vs1[1], vs1[0]], SLATE),
                 ([vs0[1], vs0[2], vs1[2], vs1[1]], SLATE), ([vs0[2], vs0[0], vs1[0], vs1[2]], SLATE)):
        ff = mb.bm.faces.new(f); ff.material_index = mb.mi(m)
    # arched recess: dark fan + buff archivolt + radial bars + transom
    cz = asp; segs = 20; yy = -dep - 0.15
    pts = [Vector((ar * math.cos(math.pi * k / segs), yy, cz + ar * math.sin(math.pi * k / segs))) for k in range(segs + 1)]
    q = [Vector((ar, yy, 0.0))] + pts + [Vector((-ar, yy, 0.0))]
    vs = [mb.bm.verts.new(M @ p) for p in q]; ff = mb.bm.faces.new(vs[::-1]); ff.material_index = mb.mi(DARK)
    for k in range(segs):                                                     # archivolt
        a0, a1 = math.pi * k / segs, math.pi * (k + 1) / segs; y2 = yy - 0.35
        p = [Vector((r * math.cos(a), y2, cz + r * math.sin(a))) for r, a in ((ar, a0), (ar + 3.5, a0), (ar + 3.5, a1), (ar, a1))]
        vv = [mb.bm.verts.new(M @ x) for x in p]; ff = mb.bm.faces.new(vv[::-1]); ff.material_index = mb.mi(STONE)
    for sx in (-1, 1): B(sx * ar - 1.6, sx * ar + 1.6, yy - 0.5, yy, 0.0, cz, STONE)
    for k in range(1, 8):                                                     # radial glazing bars
        a = math.pi * k / 8
        p0 = Vector((ar * 0.25 * math.cos(a), yy - 0.2, cz + ar * 0.25 * math.sin(a))); p1 = Vector((ar * math.cos(a), yy - 0.2, cz + ar * math.sin(a)))
        d = p1 - p0; Rm = d.to_track_quat("Z", "Y").to_matrix().to_4x4()
        mb.box(-0.35, 0.35, -0.2, 0.2, 0, d.length, STONE, M=M @ Matrix.Translation(p0) @ Rm)
    B(-ar, ar, yy - 0.4, yy, cz - 0.6, cz + 0.6, STONE)
    for k in range(-2, 3): B(k * ar / 3 - 0.35, k * ar / 3 + 0.35, yy - 0.4, yy, 0.0, cz, STONE)
for p in Lo.PAVILIONS: pavilion(*p)
# executive offices flanking the principal entrance (to 40 ft, hipped slate)
for (a, b) in Lo.OFFICES:
    mb.box(a, b, -4.0, 44.0, 0.0, 40.0, BRICK); mb.box(a - 1, b + 1, -5.0, 45.0, 39.0, 41.0, STONE)
    mb.prism([(-5.0, 41.0), (45.0, 41.0), (20.0, 49.0)], a, b, SLATE, axis="x")
    for z in (8.0, 24.0):
        for k in range(2): mb.box(a + 6 + k * 18, a + 14 + k * 18, -4.4, -4.0, z, z + 10, DARK)
# pent roof (15 ft) along the principal front and both ends, on iron posts
def pent(axis, a0, a1, c, s):
    for (x0, x1) in ((a0, a1),):
        if axis == "u":
            M = Matrix.Identity(4)
            vs = [mb.bm.verts.new(p) for p in ((x0, c, 19.0), (x1, c, 19.0), (x1, c + 15.0 * s, 15.0), (x0, c + 15.0 * s, 15.0))]
        else:
            vs = [mb.bm.verts.new(p) for p in ((c, x0, 19.0), (c, x1, 19.0), (c + 15.0 * s, x1, 15.0), (c + 15.0 * s, x0, 15.0))]
        ff = mb.bm.faces.new(vs if s < 0 else vs[::-1]); ff.material_index = mb.mi(SLATE)
        k = a0 + 12.0
        while k < a1:
            if axis == "u": mb.box(k - 0.5, k + 0.5, c + 14.0 * s - 0.5, c + 14.0 * s + 0.5, 0.0, 15.3, STONE)
            else: mb.box(c + 14.0 * s - 0.5, c + 14.0 * s + 0.5, k - 0.5, k + 0.5, 0.0, 15.3, STONE)
            k += 24.0
pent("u", 4.0, Lo.ROT_U - 64.0, -0.6, -1); pent("u", Lo.ROT_U + 64.0, Lo.L - 4.0, -0.6, -1)
pent("v", 4.0, Lo.AXIS_V - 52.0, -0.6, -1); pent("v", Lo.AXIS_V + 52.0, Lo.NORTH[0][2] - 4.0, -0.6, -1)
pent("v", 4.0, Lo.AXIS_V - 52.0, Lo.L + 0.6, 1); pent("v", Lo.AXIS_V + 52.0, Lo.NORTH[-1][2] - 4.0, Lo.L + 0.6, 1)
# exit-door porches on the south front
for u in Lo.PORCHES_S:
    mb.box(u - 10, u + 10, -14.0, -0.5, 0.0, 14.0, STONE)
    mb.prism([(u - 11, 14.0), (u + 11, 14.0), (u, 22.0)], -14.5, -0.5, SLATE, axis="y") if False else None
    vs0 = [mb.bm.verts.new(p) for p in ((u - 11, -14.6, 14.0), (u + 11, -14.6, 14.0), (u, -14.6, 22.0))]
    vs1 = [mb.bm.verts.new(p) for p in ((u - 11, -0.5, 14.0), (u + 11, -0.5, 14.0), (u, -0.5, 22.0))]
    for f, m in (([vs0[2], vs0[1], vs0[0]], PANEL), ([vs0[0], vs0[1], vs1[1], vs1[0]], SLATE), ([vs0[1], vs0[2], vs1[2], vs1[1]], SLATE), ([vs0[2], vs0[0], vs1[0], vs1[2]], SLATE)):
        ff = mb.bm.faces.new(f); ff.material_index = mb.mi(m)
    mb.box(u - 5, u + 5, -14.8, -14.4, 0.0, 10.0, DARK)
# fill: flat lead corridor roof between strip ends and the enclosing walls (no visible gaps from above)
for (u0, u1, v0, v1) in Lo.strips():
    if v0 <= 21.0: mb.box(u0, u1, 0.0, v0, 0.0, Lo.WALL_H - 1.0, SLATE)
    nv = Lo.north_v((u0 + u1) / 2)
    if v1 >= nv - 21.0: mb.box(u0, u1, v1, nv, 0.0, Lo.WALL_H - 1.0, SLATE)
mb.box(0.0, 20.0, 0.0, Lo.NORTH[0][2], 0.0, Lo.WALL_H - 1.0, SLATE); mb.box(Lo.L - 20.0, Lo.L, 0.0, Lo.NORTH[-1][2], 0.0, Lo.WALL_H - 1.0, SLATE)
mb.box(930.0, 1070.0, 0.0, Lo.ROT_V - 96.0, 0.0, Lo.WALL_H + 2.0, BRICK)                    # vestibule between entrance and drum
B_OBJ = mb.obj("W7_MODEL_BUILDING", loc=ORG, scale=K)

# model trees: lichen-sponge tufts on wire trunks (as a model-maker would make them)
mb = MB([TREE, TRUNK])
for (u, v, cr, h) in Lo.TREES:
    mb.box(u - 1.5, u + 1.5, v - 1.5, v + 1.5, 0.0, h * 0.45, TRUNK)
    for j in range(14):
        a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(0.0, cr * 0.6); r = cr * rnd.uniform(0.38, 0.58)
        c = Vector((u + rr * math.cos(a), v + rr * math.sin(a), h * rnd.uniform(0.42, 0.80) - 0.15 * rr))
        res = bmesh.ops.create_icosphere(mb.bm, subdivisions=2, radius=1.0, matrix=Matrix.Translation(c) @ Matrix.Diagonal((r, r, r * 0.8, 1)))
        for vv in res["verts"]:
            vv.co += (vv.co - c).normalized() * r * rnd.uniform(-0.16, 0.16)
        for f in {f for vv in res["verts"] for f in vv.link_faces}: f.material_index = 0
mb.obj("W7_MODEL_TREES", loc=ORG, scale=K, smooth=True)

# ---------------- SD46 table dressing ----------------
def place(name, build, mats, smooth=False):
    m = MB(mats); build(m); return m.obj(name, smooth=smooth)
fy = TY0 + 0.035                                    # front strip of the table (in front of the baseboard)
by0 = ORG.y + BV0 * K                               # baseboard front edge (world y)
print("W7 baseboard front y", round(by0, 4), "table front", round(TY0, 4))
# plan sheet lying at the front left, slightly skewed, held by two lead weights
SW, SH = 0.34, 0.225
def frontx(px, y):  # world x at projected frame x 'px' for depth y on the table
    lo, hi = TX0 - 1, TX1 + 1
    for _ in range(40):
        mid = (lo + hi) / 2; p = w2c(sc, cam, Vector((mid, y, TZ)))
        if p.x < px: lo = mid
        else: hi = mid
    return (lo + hi) / 2
def sheet_y():
    lo, hi = TY0, by0
    for _ in range(40):
        mid = (lo + hi) / 2; p = w2c(sc, cam, Vector((frontx(0.22, mid), mid, TZ)))
        if p.y < 0.075: lo = mid
        else: hi = mid
    return (lo + hi) / 2
y_near = sheet_y(); scy = y_near + SH / 2; scx = frontx(0.215, scy)
def b_sheet(m):
    vs = [m.bm.verts.new((scx + x * math.cos(0.05) - y * math.sin(0.05), scy + x * math.sin(0.05) + y * math.cos(0.05), TZ + 0.0012)) for x, y in ((-SW / 2, -SH / 2), (SW / 2, -SH / 2), (SW / 2, SH / 2), (-SW / 2, SH / 2))]
    f = m.bm.faces.new(vs); f.material_index = 0
    uv = m.bm.loops.layers.uv.new("UVMap")
    for l, c in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))): l[uv].uv = c
place("W7_PLAN_SHEET", b_sheet, [SHEET])
def b_tools(m):
    for (dx, dy) in ((-SW / 2 + 0.02, SH / 2 - 0.03), (SW / 2 - 0.03, -SH / 2 + 0.03)):
        m.box(scx + dx - 0.022, scx + dx + 0.022, scy + dy - 0.016, scy + dy + 0.016, TZ + 0.001, TZ + 0.016, LEADW)
    # boxwood scale rule across the sheet's lower edge
    M = Matrix.Translation((scx + 0.03, scy - SH / 2 + 0.045, TZ + 0.0015)) @ Matrix.Rotation(0.05, 4, "Z")
    m.box(-0.155, 0.155, -0.011, 0.011, 0, 0.004, BOX, M=M)
    # dividers: two steel legs from a brass head, lying open on the sheet
    h = Vector((scx + 0.11, scy + 0.05, TZ + 0.006))
    for a in (-0.25, 0.18):
        d = Vector((math.cos(-0.9 + a) * 0.11, math.sin(-0.9 + a) * 0.11, -0.004)); R = d.to_track_quat("Z", "Y").to_matrix().to_4x4()
        m.box(-0.0025, 0.0025, -0.0025, 0.0025, 0, d.length, STEEL, M=Matrix.Translation(h) @ R)
    m.box(h.x - 0.007, h.x + 0.007, h.y - 0.007, h.y + 0.007, h.z - 0.004, h.z + 0.004, BRASS)
place("W7_TOOLS", b_tools, [LEADW, BOX, STEEL, BRASS])
# inkstand (deal tray, square glass pot, pen) to the right of the sheet
ix, iy = scx + SW / 2 + 0.07, scy + 0.04
def b_ink(m):
    m.box(ix - 0.06, ix + 0.06, iy - 0.035, iy + 0.035, TZ, TZ + 0.012, DEALDK)
    res = bmesh.ops.create_cone(m.bm, cap_ends=True, segments=16, radius1=0.022, radius2=0.017, depth=0.036, matrix=Matrix.Translation((ix - 0.025, iy, TZ + 0.03)))
    for f in {f for v in res["verts"] for f in v.link_faces}: f.material_index = m.mi(INK)
    m.box(ix - 0.03, ix - 0.02, iy - 0.005, iy + 0.005, TZ + 0.05, TZ + 0.057, BRASS)
    p0 = Vector((ix + 0.012, iy - 0.03, TZ + 0.016)); d = Vector((0.0, 0.075, 0.0)); R = d.to_track_quat("Z", "Y").to_matrix().to_4x4()
    m.box(-0.003, 0.003, -0.003, 0.003, 0, d.length, BOX, M=Matrix.Translation(p0) @ R)        # pen laid in the tray groove
place("W7_INKSTAND", b_ink, [DEALDK, INK, BRASS, BOX])
# label card: tent card at the front right, fully in frame (replaces CM_LABEL_*)
lx = frontx(0.79, fy + 0.07); ly = fy + 0.07; LW, LH = 0.27, 0.07; tilt = math.radians(18)
def b_card(m):
    M = Matrix.Translation((lx, ly, TZ)) @ Matrix.Rotation(tilt, 4, "X")
    m.box(-LW / 2, LW / 2, -0.0015, 0.0015, 0, LH, CARD, M=M)
    M2 = Matrix.Translation((lx, ly + 0.03, TZ)) @ Matrix.Rotation(-math.radians(38), 4, "X")
    m.box(-LW / 2, LW / 2, -0.0015, 0.0015, 0, LH * 0.9, CARD, M=M2)
place("W7_LABEL_CARD", b_card, [CARD])
cu = bpy.data.curves.new("W7_LABEL_TEXT", "FONT")
cu.body = "UNBUILT PROPOSAL\nBuilding Committee's design, June 1850\nstudy model 1:600 (interpretive)"
cu.size = 0.0118; cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.space_line = 1.25
try: cu.font = bpy.data.fonts.load("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
except Exception: pass
cu.materials.append(INKT)
to = bpy.data.objects.new("W7_LABEL_TEXT", cu); link(to)
to.matrix_world = Matrix.Translation((lx, ly - 0.0019 * math.cos(tilt), TZ + LH * 0.5 * math.cos(tilt) - 0.0)) @ Matrix.Rotation(tilt, 4, "X") @ Matrix.Translation((0, -0.0005, 0)) @ Matrix.Rotation(math.radians(90), 4, "X")
to.location = (lx, ly - 0.0025, TZ + LH * 0.5 * math.cos(tilt)); to.location.y -= LH * 0.5 * math.sin(tilt) * 1.0
# rolled drawings with red tapes at the back of the table, and a loose roll on the right
def b_rolls(m):
    for k, (x, y, L, r, a) in enumerate(((TCX - 0.62, TY1 - 0.08, 0.56, 0.022, 0.05), (TCX + 0.42, TY1 - 0.09, 0.60, 0.024, 0.10))):
        M = Matrix.Translation((x, y, TZ + r)) @ Matrix.Rotation(a, 4, "Z") @ Matrix.Rotation(math.pi / 2, 4, "Y")
        res = bmesh.ops.create_cone(m.bm, cap_ends=True, segments=20, radius1=r, radius2=r, depth=L, matrix=M)
        for f in {f for v in res["verts"] for f in v.link_faces}: f.material_index = 0
        for t in (-0.3, 0.3):
            res = bmesh.ops.create_cone(m.bm, cap_ends=True, segments=20, radius1=r + 0.0012, radius2=r + 0.0012, depth=0.012, matrix=M @ Matrix.Translation((0, 0, t * L)))
            for f in {f for v in res["verts"] for f in v.link_faces}: f.material_index = 1
place("W7_ROLLS", b_rolls, [PAPER, TAPE], smooth=True)

# ---------------- SD47 spring sward behind the table (CP007 only) ----------------
BV = []
for n in ("G_PARK_NEAR", "G_PARK"):
    o = bpy.data.objects[n]; bm = bmesh.new(); bm.from_mesh(o.data); bm.transform(o.matrix_world); BV.append(BVHTree.FromBMesh(bm)); bm.free()
def gz(x, y):
    for t in BV:
        hit = t.ray_cast(Vector((x, y, 50.0)), Vector((0, 0, -1)))
        if hit[0] is not None: return hit[0].z
    return 0.0
def sward():
    x0, x1, y0, y1, res = 7.5, 20.5, -72.6, -61.0, 0.25
    bm = bmesh.new(); nx = int((x1 - x0) / res) + 1; ny = int((y1 - y0) / res) + 1
    vs = [[bm.verts.new((x0 + i * res, y0 + j * res, gz(x0 + i * res, y0 + j * res) + 0.003)) for j in range(ny)] for i in range(nx)]
    for i in range(nx - 1):
        for j in range(ny - 1): bm.faces.new([vs[i][j], vs[i + 1][j], vs[i + 1][j + 1], vs[i][j + 1]])
    me = bpy.data.meshes.new("W7_SWARD"); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new("W7_SWARD", me); link(o)
    turf, nt, b, _ = newmat("W7_SpringTurf1850")
    n = tex(nt, 1.2, coord="Object"); n2 = tex(nt, 9.0, coord="Object")
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "FLOAT"; mx.inputs[0].default_value = 0.4
    nt.links.new(n.outputs["Fac"], mx.inputs[2]); nt.links.new(n2.outputs["Fac"], mx.inputs[3])
    nt.links.new(ramp(nt, mx.outputs[0], [(0.3, (0.13, 0.18, 0.06)), (0.55, (0.19, 0.26, 0.09)), (0.75, (0.26, 0.28, 0.13))]), b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.95; me.materials.append(turf)
    hm, nt, b, _ = newmat("W7_SpringBlades1850"); hi = nt.nodes.new("ShaderNodeHairInfo")
    c = ramp(nt, hi.outputs["Random"], [(0.0, (0.14, 0.22, 0.07)), (0.5, (0.22, 0.32, 0.10)), (0.85, (0.30, 0.37, 0.14)), (1.0, (0.40, 0.39, 0.22))])
    tipm = ramp(nt, hi.outputs["Intercept"], [(0.0, (0.45, 0.45, 0.45)), (1.0, (1.0, 1.0, 0.95))])
    mm = nt.nodes.new("ShaderNodeMix"); mm.data_type = "RGBA"; mm.blend_type = "MULTIPLY"; mm.inputs[0].default_value = 1.0
    nt.links.new(c, mm.inputs[6]); nt.links.new(tipm, mm.inputs[7]); nt.links.new(mm.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.7; me.materials.append(hm)
    mod = o.modifiers.new("sward", "PARTICLE_SYSTEM"); ps = mod.particle_system; st = ps.settings
    st.type = "HAIR"; st.count = 90000; st.use_advanced_hair = True; st.hair_length = 0.07
    st.emit_from = "FACE"; st.use_emit_random = True; st.distribution = "RAND"
    st.material = 2; st.hair_step = 4; st.display_step = 2; st.render_step = 3
    st.child_type = "INTERPOLATED"; st.child_percent = 2; st.rendered_child_count = 10
    st.child_length = 1.0; st.child_length_threshold = 0.0
    st.roughness_1 = 0.025; st.roughness_1_size = 1.0; st.roughness_endpoint = 0.015; st.roughness_2 = 0.02
    if hasattr(st, "length_random"): st.length_random = 0.6
    st.normal_factor = 0.018; st.factor_random = 0.007
    st.root_radius = 1.0; st.tip_radius = 0.0; st.radius_scale = 0.0022; st.use_close_tip = True; st.child_radius = 0.5
    ps.seed = 1850
    return st.count * st.rendered_child_count
print("W7 sward strands ~", sward())

# ---------------- SD48 depth of field on CP007_start only ----------------
fstop = float(arg("--fstop", "8.0"))
if fstop > 0:
    cd = cam.data; assert cd.users == 1
    cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop
    cd.dof.focus_distance = (Vector((MX, MY + 0.02, TZ + 0.03)) - cam.matrix_world.translation).length
    print("W7 DOF f/", fstop, "focus", round(cd.dof.focus_distance, 3))

# ---------------- grok_states: CP007 shows W7_, hides the CM_ objects it replaces ----------------
st = json.loads(bpy.data.texts["grok_states"].as_string()); c7 = st["CP007"]
c7.setdefault("show", [])
for h in ("CM_",):
    if h not in c7["hide"]: c7["hide"].append(h)
if "W7_" not in c7["show"]: c7["show"].append("W7_")
for k, v in st.items():
    if k != "CP007": assert "W7_" not in v.get("show", [])
t = bpy.data.texts["grok_states"]; t.clear(); t.write(json.dumps(st, indent=1)); print("W7 states CP007", c7)
# report frame coverage
for n in ("W7_MODEL_BASE", "W7_LABEL_CARD", "W7_PLAN_SHEET"):
    o = bpy.data.objects[n]; bpy.context.view_layer.update()
    ps = [w2c(sc, cam, o.matrix_world @ v.co) for v in o.data.vertices]
    print("W7 frame", n, round(min(p.x for p in ps), 3), round(max(p.x for p in ps), 3), round(min(p.y for p in ps), 3), round(max(p.y for p in ps), 3))
out = arg("--out") or os.path.join(ROOT, "rounds", "candidates", "s02_cp007committee.blend")
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True); print("W7 SAVED", out)
