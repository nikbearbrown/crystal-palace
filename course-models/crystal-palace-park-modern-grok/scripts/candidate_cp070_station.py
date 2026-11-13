"""CP070 'Begin the walk that remains' - PARK-NOW (present day) polish, CANDIDATE 2026-11-13 (Grok; no verdict).
blender -b rounds/parknow-r02.blend -P scripts/candidate_cp070_station.py -- [--out rounds/candidates/parknow-r02_cp070station.blend]
Never overwrites the opened (live) blend. PARK-NOW (present day) only; nothing of Hyde Park and no Victorian state.

Storyboard CP070 (survey crystal-palace-storyboard-v001.md): 'A visitor emerges from the surviving station into the park
approach'; '35 mm; establish station sign then walk 8 m toward park entrance'; transition to CP071 is an explicit
relocation ('do not imply next-door subway access'). The live CP070 cams (dud-fix v4) stand on Crystal Palace Parade at
the former HIGH LEVEL station (demolished 1961, right beside the subway) looking at the abstract footprint overlay: a third
of the frame is a blank light-grey road slab and there is no station at all.

Candidate (DEPARTURES D-PM-33..D-PM-41):
 1. The surviving LOW LEVEL station frontage (Crystal Palace station, 1875 rebuild; Historic England list entry 1064353,
    Grade II, NGR TQ 34123 70553) as a parametric stock-brick building following the list description: left pavilion
    'French Chateau style, 2 storeys stock brick, very steep hipped slate roof with decorative ironwork along ridge, stone
    moulded eaves cornice, 2 double round headed windows'; central 1-storey ticket-office section 'having 2 round-headed
    doorcases with fanlights and 4 windows; canopy now missing'; right pavilion '2 storeys stock brick with hipped slate
    roof, modillion cornice, 3 sashes, round headed on the ground floor'; booking hall with 'a fine celestory roof'
    (Historic England / Heritage Gateway 500640). Position registered with the D-PM-31 grid (subway TQ 33791 70972 =
    model (0, 60), palace axis bearing 22.5 deg) -> model (-260.0, -407.1). Sizes are inferred (no measured elevation).
 2. Station road with kerbs, paving, double yellow lines, a zebra crossing with Belisha beacons, street lamps; the park
    boundary opposite: dwarf brick wall, cast-iron railings, gate piers with open gates, a tarmac path climbing into the
    park, a park name board, parametric park trees (MV20 v2 generator via park_trees_now.py).
 3. Station sign: National Rail 'Rail Symbol 2' totem (double arrow, top arrow pointing right, 38:23, outline from the
    Commons 'British Rail - black logo.svg' path) with the name 'Crystal Palace', and a name board on the parapet.
 4. Present-day visitors (parametric, jeans/jackets/trainers, some backpacks; no period dress): one emerging from the
    east doorcase, others on the pavements and walking through the gate.
 5. Both CP070 cameras moved to the station (35 mm, eye 1.6 m): CAM_CP070_begin_walk_35mm on the park-side pavement
    establishing the station and the sign; CAM_CP070_park_entry_35mm 8.0 m further along the walk toward the park gate.
 6. Hidden (not deleted): the appended 1854 glazed covered way 'SY54_railway_colonnade' (an 1850s structure that does
    not stand today; it floated up to 20 m above the PARK-NOW ground here), and placeholder park trees whose trunks stand
    inside the new road/building footprint.
World, look, exposure, sun, every other object and every other camera: unchanged.
"""
import os, sys, json, math, random, argparse
import bpy, bmesh
from mathutils import Vector, Matrix
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import park_trees_now as PT

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser(); ap.add_argument("--out", default="rounds/candidates/parknow-r02_cp070station.blend")
ap.add_argument("--no-save", action="store_true")
A = ap.parse_args(argv)
SRC = bpy.data.filepath
OUT = A.out if os.path.isabs(A.out) else os.path.join(os.path.dirname(HERE), A.out)
assert os.path.abspath(OUT) != os.path.abspath(SRC), "refusing to overwrite the opened (live) blend"
assert not any("cp070_now" in o.keys() for o in bpy.data.objects), "source already carries the CP070 candidate"
TAG = "cp070_now_v1"
R = random.Random(7070)
LOG = {"version": TAG, "src": SRC, "hidden": [], "objects": 0, "dims": {}, "cams": {}}

# ------------------------------------------------------------------ registration (D-PM-31 grid)
BEAR = math.radians(22.5)
def ngr_to_model(E, N):
    dE, dN = E - 33791.0, N - 70972.0
    x = dE * math.sin(BEAR) + dN * math.cos(BEAR)
    y = 60.0 + (dE * -math.cos(BEAR) + dN * math.sin(BEAR))
    return x, y
SX, SY = ngr_to_model(34123.0, 70553.0)            # Historic England 1064353 NGR -> (-260.0, -407.1)
LOG["station_ngr_model"] = (round(SX, 2), round(SY, 2))

PS = bpy.data.objects["park_slope"]
def ground(x, y):
    ok, loc, n, i = PS.ray_cast(PS.matrix_world.inverted() @ Vector((x, y, 400.0)), Vector((0, 0, -1)))
    assert ok, (x, y); return (PS.matrix_world @ loc).z

# layout (metres; station front faces +y = up-slope, toward the park)
FY = round(SY + 6.0, 2)            # front wall plane (building centred on the NGR point, 12 m deep)
BX0, BX1 = SX - 23.5, SX + 23.5    # 47 m frontage: right pavilion (-x) 12 m | central 22 m | left chateau pavilion (+x) 13 m
XR1 = BX0 + 12.0; XL0 = BX1 - 13.0
FPV = FY + 4.0                     # forecourt pavement 4 m
KERB_S = FPV; ROAD_N = KERB_S + 7.4  # 7.4 m carriageway
NPV = ROAD_N + 3.0                 # park-side pavement 3 m
WALL_Y = NPV
ZR = round(ground(SX, WALL_Y + 0.4) + 0.06, 3)   # road / pavement datum just above the slope at the park wall
ZP = ZR + 0.12                     # pavement top (kerb upstand 120 mm)
DOOR_X = (XR1 + (XL0 - XR1) * (1.5 / 6.0))      # west doorcase (the one nearer the walk), leaf open
CB_X = SX - 21.0                  # begin_walk camera x (park-side pavement, west of the frontage centre)
WALK = 8.0                         # storyboard: walk 8 m toward the park entrance
GATE_X = CB_X + WALK + 0.6         # park gate opposite the end of the walk; zebra crossing on the same line
LOG["layout"] = dict(FY=FY, BX0=BX0, BX1=BX1, ZR=ZR, ROAD=(KERB_S, ROAD_N), WALL_Y=WALL_Y, DOOR_X=round(DOOR_X, 2))

ROOT = bpy.data.collections.new("PARKNOW_CP070_lowlevel_station__present"); bpy.data.collections["PARK-NOW_present_day"].children.link(ROOT)
def sub(n):
    c = bpy.data.collections.new(n); ROOT.children.link(c); return c
C_BLD = sub("CP070_station_building_1875_as_today"); C_ST = sub("CP070_station_road_present")
C_PK = sub("CP070_park_gate_present"); C_SIGN = sub("CP070_signs_present"); C_PPL = sub("CP070_visitors_present")
C_TR = sub("CP070_park_trees_present")

# ------------------------------------------------------------------ materials
def _bsdf(m): return next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
def mat_plain(name, col, rough=0.8, metal=0.0, emit=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = _bsdf(m)
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal; m.diffuse_color = (*col, 1)
    if emit: b.inputs["Emission Color"].default_value = (*emit[0], 1); b.inputs["Emission Strength"].default_value = emit[1]
    return m
def mat_brickish(name, c1, c2, mortar, bw, rh, rough=0.9, plane="xz", soot=None, bump=0.25, mortar_size=0.012, noise_scale=3.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; L = nt.links; b = _bsdf(m)
    tc = N.new("ShaderNodeTexCoord"); sep = N.new("ShaderNodeSeparateXYZ"); L.new(tc.outputs["Object"], sep.inputs[0])
    comb = N.new("ShaderNodeCombineXYZ")
    if plane == "xz":      # vertical walls: u = x + y (works on faces normal to x or y), v = z
        add = N.new("ShaderNodeMath"); add.operation = "ADD"; L.new(sep.outputs[0], add.inputs[0]); L.new(sep.outputs[1], add.inputs[1])
        L.new(add.outputs[0], comb.inputs[0]); L.new(sep.outputs[2], comb.inputs[1])
    else:                  # horizontal: u = x, v = y
        L.new(sep.outputs[0], comb.inputs[0]); L.new(sep.outputs[1], comb.inputs[1])
    br = N.new("ShaderNodeTexBrick"); L.new(comb.outputs[0], br.inputs["Vector"])
    br.inputs["Scale"].default_value = 1.0; br.inputs["Mortar Size"].default_value = mortar_size
    br.inputs["Brick Width"].default_value = bw; br.inputs["Row Height"].default_value = rh
    br.inputs["Color1"].default_value = (*c1, 1); br.inputs["Color2"].default_value = (*c2, 1); br.inputs["Mortar"].default_value = (*mortar, 1)
    br.inputs["Bias"].default_value = 0.0
    col_out = br.outputs["Color"]
    if soot:
        nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = noise_scale; nz.inputs["Detail"].default_value = 6
        L.new(tc.outputs["Object"], nz.inputs["Vector"])
        mx = N.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "MULTIPLY"
        L.new(nz.outputs["Fac"], mx.inputs[0]); L.new(col_out, mx.inputs[6]); mx.inputs[7].default_value = (*soot, 1)
        col_out = mx.outputs[2]
    L.new(col_out, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = rough
    bp = N.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump; bp.invert = True
    L.new(br.outputs["Fac"], bp.inputs["Height"]); L.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (*c1, 1); return m
def mat_noise(name, c0, c1, rough=0.85, scale=6.0, bump=0.05):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; L = nt.links; b = _bsdf(m)
    tc = N.new("ShaderNodeTexCoord"); nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = scale; nz.inputs["Detail"].default_value = 8
    L.new(tc.outputs["Object"], nz.inputs["Vector"]); rp = N.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (*c0, 1); rp.color_ramp.elements[1].color = (*c1, 1)
    L.new(nz.outputs["Fac"], rp.inputs[0]); L.new(rp.outputs[0], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = rough
    bp = N.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump; L.new(nz.outputs["Fac"], bp.inputs["Height"]); L.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (*c0, 1); return m

M = {}
M["stock"] = mat_brickish("CP70_LondonStockBrick", (0.42, 0.33, 0.20), (0.34, 0.26, 0.16), (0.50, 0.48, 0.43), 0.225, 0.075, soot=(0.62, 0.60, 0.58))
M["redbrick"] = mat_brickish("CP70_RedBrickDressing", (0.36, 0.13, 0.07), (0.30, 0.11, 0.06), (0.50, 0.48, 0.43), 0.225, 0.075)
M["stone"] = mat_noise("CP70_StoneDressing", (0.44, 0.41, 0.34), (0.55, 0.52, 0.44), 0.85, 9.0, 0.08)
M["slate"] = mat_brickish("CP70_WelshSlate", (0.035, 0.04, 0.05), (0.05, 0.055, 0.067), (0.025, 0.025, 0.03), 0.25, 0.14, rough=0.75, bump=0.15, mortar_size=0.006)
M["iron"] = mat_plain("CP70_CastIronBlack", (0.025, 0.027, 0.03), 0.45, 0.4)
M["glass"] = mat_plain("CP70_WindowPaneDark", (0.03, 0.038, 0.045), 0.12, 0.0)   # name avoids the look clamp (it turns "Glass" materials transmissive)
M["sash"] = mat_plain("CP70_SashWhite", (0.72, 0.71, 0.66), 0.5)
M["door"] = mat_plain("CP70_DoorGreen", (0.04, 0.10, 0.07), 0.45)
M["asphalt"] = mat_noise("CP70_Asphalt", (0.055, 0.055, 0.058), (0.10, 0.10, 0.10), 0.92, 40.0, 0.08)
M["paving"] = mat_brickish("CP70_ConcretePaving", (0.42, 0.41, 0.38), (0.38, 0.37, 0.35), (0.25, 0.25, 0.24), 0.6, 0.6, rough=0.9, plane="xy", bump=0.1, mortar_size=0.006)
M["kerb"] = mat_noise("CP70_GraniteKerb", (0.33, 0.33, 0.33), (0.46, 0.46, 0.45), 0.85, 30.0, 0.05)
M["yellow"] = mat_plain("CP70_LineYellow", (0.75, 0.55, 0.05), 0.6)
M["white"] = mat_plain("CP70_LineWhite", (0.80, 0.80, 0.78), 0.6)
M["tarmac_path"] = mat_noise("CP70_ParkPathTarmac", (0.075, 0.072, 0.068), (0.12, 0.115, 0.105), 0.92, 25.0, 0.06)
M["grey_steel"] = mat_plain("CP70_LampGrey", (0.18, 0.19, 0.20), 0.5, 0.6)
M["sign_white"] = mat_plain("CP70_SignWhite", (0.82, 0.82, 0.80), 0.45)
M["rail_red"] = mat_plain("CP70_RailRed", (0.60, 0.03, 0.03), 0.45)
M["text_dark"] = mat_plain("CP70_SignText", (0.02, 0.02, 0.025), 0.5)
M["park_green"] = mat_plain("CP70_ParkBoardGreen", (0.02, 0.10, 0.05), 0.5)
M["cream"] = mat_plain("CP70_EnamelCream", (0.78, 0.74, 0.62), 0.45)
M["amber"] = mat_plain("CP70_BelishaAmber", (0.9, 0.45, 0.05), 0.3, 0.0, emit=((1.0, 0.55, 0.1), 2.0))
M["bstripe_w"] = M["white"]; M["bstripe_k"] = M["text_dark"]
M["lamp_glow"] = mat_plain("CP70_LampLens", (0.85, 0.85, 0.8), 0.3)
for _k in ("slate", "asphalt"):
    _b = _bsdf(M[_k]); _b.inputs["Specular IOR Level"].default_value = 0.25

# ------------------------------------------------------------------ mesh builder
class MB:
    def __init__(self, name, coll, mats):
        self.name, self.coll, self.mats = name, coll, list(mats); self.bm = bmesh.new()
    def mi(self, m):
        if m not in self.mats: self.mats.append(m)
        return self.mats.index(m)
    def _faces(self, fs, m):
        i = self.mi(m)
        for f in fs: f.material_index = i
    def box(self, x0, x1, y0, y1, z0, z1, m):
        x0, x1 = min(x0, x1), max(x0, x1); y0, y1 = min(y0, y1), max(y0, y1); z0, z1 = min(z0, z1), max(z0, z1)
        r = bmesh.ops.create_cube(self.bm, size=1.0, matrix=Matrix.Translation(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)) @ Matrix.Diagonal((x1 - x0, y1 - y0, z1 - z0, 1)))
        self._faces({f for v in r["verts"] for f in v.link_faces}, m)
    def prism_y(self, pts, y0, y1, m):
        """extrude a 2D outline pts [(x, z)] between y0 and y1 (outline in the facade plane)."""
        vs0 = [self.bm.verts.new((x, y0, z)) for x, z in pts]; vs1 = [self.bm.verts.new((x, y1, z)) for x, z in pts]
        fs = [self.bm.faces.new(vs1), self.bm.faces.new(list(reversed(vs0)))]
        n = len(pts)
        for k in range(n):
            fs.append(self.bm.faces.new((vs0[k], vs0[(k + 1) % n], vs1[(k + 1) % n], vs1[k])))
        self._faces(fs, m)
    def poly(self, pts3, m):
        vs = [self.bm.verts.new(p) for p in pts3]; self._faces([self.bm.faces.new(vs)], m)
    def quadstrip(self, rows, m):
        vv = [[self.bm.verts.new(p) for p in r] for r in rows]; fs = []
        for a, b in zip(vv, vv[1:]):
            for k in range(len(a) - 1): fs.append(self.bm.faces.new((a[k], a[k + 1], b[k + 1], b[k])))
        self._faces(fs, m)
    def limb(self, p0, p1, r0, r1, m, segs=8):
        p0, p1 = Vector(p0), Vector(p1); d = p1 - p0; L = d.length
        q = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_matrix().to_4x4()
        r = bmesh.ops.create_cone(self.bm, cap_ends=True, segments=segs, radius1=r0, radius2=r1, depth=L, matrix=Matrix.Translation((p0 + p1) / 2) @ q)
        self._faces({f for v in r["verts"] for f in v.link_faces}, m)
    def sphere(self, c, rad, m, sc=(1, 1, 1), u=12, v=8):
        r = bmesh.ops.create_uvsphere(self.bm, u_segments=u, v_segments=v, radius=rad, matrix=Matrix.Translation(c) @ Matrix.Diagonal((*sc, 1)))
        self._faces({f for v_ in r["verts"] for f in v_.link_faces}, m)
    def done(self, smooth=False):
        bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)
        me = bpy.data.meshes.new(self.name); self.bm.to_mesh(me); self.bm.free()
        for m in self.mats: me.materials.append(m)
        if smooth:
            for p in me.polygons: p.use_smooth = True
        ob = bpy.data.objects.new(self.name, me); self.coll.objects.link(ob); ob["cp070_now"] = TAG; return ob

def arch_pts(x0, x1, z0, zs, n=12):
    """rectangle x0..x1 from z0 up to springing zs, semicircular head."""
    xc, r = (x0 + x1) / 2, (x1 - x0) / 2
    pts = [(x0, z0), (x1, z0), (x1, zs)]
    for k in range(1, n):
        a = math.pi * k / n; pts.append((xc + r * math.cos(a), zs + r * math.sin(a)))
    pts.append((x0, zs)); return pts

def window(mb, xc, z0, w, h, y, arched=True, frame=0.16, bars=True, glass=None):
    """surround (stone), dark glass, white sash bars; front at y (+y outward)."""
    glass = glass or M["glass"]
    zs = z0 + h - (w / 2 if arched else 0)
    out = arch_pts(xc - w / 2 - frame, xc + w / 2 + frame, z0 - frame, zs) if arched else [(xc - w/2 - frame, z0 - frame), (xc + w/2 + frame, z0 - frame), (xc + w/2 + frame, z0 + h + frame), (xc - w/2 - frame, z0 + h + frame)]
    mb.prism_y(out, y - 0.02, y + 0.06, M["stone"])
    inn = arch_pts(xc - w / 2, xc + w / 2, z0, zs) if arched else [(xc - w/2, z0), (xc + w/2, z0), (xc + w/2, z0 + h), (xc - w/2, z0 + h)]
    mb.prism_y(inn, y + 0.06, y + 0.075, glass)
    if bars:
        t = 0.05
        mb.box(xc - t / 2, xc + t / 2, y + 0.075, y + 0.095, z0, z0 + h - 0.05, M["sash"])
        for zz in (z0 + 0.0, z0 + h * 0.48, zs):
            mb.box(xc - w / 2, xc + w / 2, y + 0.075, y + 0.095, zz - t / 2, zz + t / 2, M["sash"])
        for xx in (xc - w / 2 + t / 2, xc + w / 2 - t / 2):
            mb.box(xx - t / 2, xx + t / 2, y + 0.075, y + 0.095, z0, zs, M["sash"])
    mb.box(xc - w / 2 - frame - 0.08, xc + w / 2 + frame + 0.08, y - 0.02, y + 0.16, z0 - frame - 0.12, z0 - frame, M["stone"])   # sill

# ------------------------------------------------------------------ station building (1875 frontage as it stands)
B = MB("cp70_station_walls", C_BLD, [M["stock"]]); D = MB("cp70_station_dressings", C_BLD, [M["stone"]])
RF = MB("cp70_station_roofs", C_BLD, [M["slate"]]); IR = MB("cp70_station_ironwork", C_BLD, [M["iron"]])
ZB = ZR + 0.12                   # ground-floor / forecourt level
FOUND = ground(SX, FY - 14.0) - 1.0
DEPTH_L, DEPTH_C, DEPTH_R = 12.0, 10.0, 11.0
H_L, H_C, H_R = 9.2, 6.0, 8.6    # eaves heights (2 storeys @ 4.6 / 1 storey / 2 storeys @ 4.3) - inferred
LOG["dims"] = {"frontage_m": 47.0, "left_pavilion_w_m": 13.0, "central_w_m": 22.0, "right_pavilion_w_m": 12.0,
               "left_eaves_m": H_L, "central_parapet_m": H_C + 0.8, "right_eaves_m": H_R}
# walls
B.box(XL0, BX1, FY - DEPTH_L, FY, FOUND, ZB + H_L, M["stock"])
B.box(XR1, XL0, FY - DEPTH_C, FY, FOUND, ZB + H_C, M["stock"])
B.box(BX0, XR1, FY - DEPTH_R, FY, FOUND, ZB + H_R, M["stock"])
# plinth + string courses + quoins
for (x0, x1, dep) in ((XL0, BX1, DEPTH_L), (XR1, XL0, DEPTH_C), (BX0, XR1, DEPTH_R)):
    D.box(x0 - 0.06, x1 + 0.06, FY - dep - 0.06, FY + 0.06, FOUND, ZB + 0.75, M["stone"])
for (x0, x1, dep, z) in ((XL0, BX1, DEPTH_L, 4.6), (BX0, XR1, DEPTH_R, 4.3)):
    D.box(x0 - 0.05, x1 + 0.05, FY - dep - 0.05, FY + 0.10, ZB + z - 0.15, ZB + z + 0.15, M["stone"])
for (x0, x1, h) in ((XL0, BX1, H_L), (BX0, XR1, H_R)):
    for xq in (x0, x1 - 0.7):
        for k in range(int(h / 0.6)):
            ww = 0.7 if k % 2 == 0 else 0.5
            xa = xq if xq == x0 else x1 - ww
            D.box(xa, xa + ww, FY - 0.02, FY + 0.05, ZB + 0.75 + k * 0.6, ZB + 0.75 + k * 0.6 + 0.52, M["redbrick"])
# left (chateau) pavilion: stone moulded eaves cornice, 2 double round-headed windows per floor, steep pavilion roof + cresting
W = MB("cp70_station_windows", C_BLD, [M["glass"]])
D.box(XL0 - 0.45, BX1 + 0.45, FY - DEPTH_L - 0.45, FY + 0.45, ZB + H_L - 0.15, ZB + H_L + 0.45, M["stone"])
D.box(XL0 - 0.25, BX1 + 0.25, FY - DEPTH_L - 0.25, FY + 0.25, ZB + H_L - 0.45, ZB + H_L - 0.15, M["stone"])
for xc in (XL0 + 13.0 * 0.27, XL0 + 13.0 * 0.73):
    for (z0, h) in ((ZB + 1.05, 2.9), (ZB + 5.45, 2.7)):
        for dx in (-0.62, 0.62):
            window(W, xc + dx, z0, 1.0, h, FY, arched=True, frame=0.14)
        D.box(xc - 0.09, xc + 0.09, FY, FY + 0.14, z0, z0 + h - 0.5, M["stone"])   # colonnette between the paired lights
RL_RISE = 6.6; RL_PITCH = math.radians(68.0); run = RL_RISE / math.tan(RL_PITCH)
ex0, ex1, ey0, ey1, ez = XL0 - 0.35, BX1 + 0.35, FY - DEPTH_L - 0.35, FY + 0.35, ZB + H_L + 0.45
tx0, tx1, ty0, ty1, tz = ex0 + run, ex1 - run, ey0 + run, ey1 - run, ez + RL_RISE
RF.quadstrip([[(ex0, ey1, ez), (ex1, ey1, ez)], [(tx0, ty1, tz), (tx1, ty1, tz)]], M["slate"])
RF.quadstrip([[(ex1, ey0, ez), (ex0, ey0, ez)], [(tx1, ty0, tz), (tx0, ty0, tz)]], M["slate"])
RF.quadstrip([[(ex0, ey0, ez), (ex0, ey1, ez)], [(tx0, ty0, tz), (tx0, ty1, tz)]], M["slate"])
RF.quadstrip([[(ex1, ey1, ez), (ex1, ey0, ez)], [(tx1, ty1, tz), (tx1, ty0, tz)]], M["slate"])
RF.poly([(tx0, ty0, tz), (tx1, ty0, tz), (tx1, ty1, tz), (tx0, ty1, tz)], M["slate"])
LOG["dims"]["left_roof_rise_m"] = RL_RISE; LOG["dims"]["left_roof_pitch_deg"] = 68.0
# cresting: decorative ironwork along the ridge / top platform edge
for (a, b) in (((tx0, ty1), (tx1, ty1)), ((tx0, ty0), (tx1, ty0)), ((tx0, ty0), (tx0, ty1)), ((tx1, ty0), (tx1, ty1))):
    a, b = Vector((*a, tz)), Vector((*b, tz)); L_ = (b - a).length; n = int(L_ / 0.22)
    for k in range(n + 1):
        p = a + (b - a) * (k / max(1, n)); hh = 0.75 if k % 4 == 0 else 0.48
        IR.box(p.x - 0.018, p.x + 0.018, p.y - 0.018, p.y + 0.018, tz, tz + hh, M["iron"])
        if k % 4 == 0: IR.sphere((p.x, p.y, tz + hh + 0.05), 0.06, M["iron"], u=6, v=4)
    IR.box(min(a.x, b.x) - 0.02, max(a.x, b.x) + 0.02, min(a.y, b.y) - 0.02, max(a.y, b.y) + 0.02, tz + 0.40, tz + 0.44, M["iron"])
# chimney stacks (brick, stone caps)
for (cx, cy) in ((XL0 + 1.6, FY - DEPTH_L * 0.55), (BX1 - 1.6, FY - DEPTH_L * 0.55), (BX0 + 2.0, FY - DEPTH_R * 0.5)):
    top = tz + 1.6 if cx > XR1 else ZB + H_R + 5.4
    B.box(cx - 0.55, cx + 0.55, cy - 0.4, cy + 0.4, ZB + 4.0, top, M["stock"])
    D.box(cx - 0.68, cx + 0.68, cy - 0.52, cy + 0.52, top, top + 0.22, M["stone"])
    for dx in (-0.25, 0.25): D.box(cx + dx - 0.11, cx + dx + 0.11, cy - 0.11, cy + 0.11, top + 0.22, top + 0.62, M["redbrick"])
# right pavilion: modillion cornice, 3 sashes (round-headed on the ground floor), hipped slate roof
D.box(BX0 - 0.40, XR1 + 0.40, FY - DEPTH_R - 0.40, FY + 0.40, ZB + H_R, ZB + H_R + 0.30, M["stone"])
for k in range(int((XR1 - BX0 + 0.6) / 0.42) + 1):
    xm = BX0 - 0.3 + k * 0.42
    D.box(xm - 0.07, xm + 0.07, FY, FY + 0.36, ZB + H_R - 0.22, ZB + H_R, M["stone"])
D.box(BX0 - 0.05, XR1 + 0.05, FY - 0.02, FY + 0.12, ZB + H_R - 0.42, ZB + H_R - 0.22, M["stone"])
for i in range(3):
    xc = BX0 + 12.0 * (i + 0.5) / 3
    window(W, xc, ZB + 1.0, 1.25, 2.9, FY, arched=True)
    window(W, xc, ZB + 5.2, 1.15, 2.2, FY, arched=False)
rr = 0.40; hx0, hx1, hy0, hy1, hz = BX0 - rr, XR1 + rr, FY - DEPTH_R - rr, FY + rr, ZB + H_R + 0.30
RR_P = math.radians(35.0); half = (hy1 - hy0) / 2; rise = half * math.tan(RR_P); ym = (hy0 + hy1) / 2
RF.quadstrip([[(hx0, hy1, hz), (hx1, hy1, hz)], [(hx0 + half, ym, hz + rise), (hx1 - half, ym, hz + rise)]], M["slate"])
RF.quadstrip([[(hx1, hy0, hz), (hx0, hy0, hz)], [(hx1 - half, ym, hz + rise), (hx0 + half, ym, hz + rise)]], M["slate"])
RF.poly([(hx0, hy0, hz), (hx0, hy1, hz), (hx0 + half, ym, hz + rise)], M["slate"])
RF.poly([(hx1, hy1, hz), (hx1, hy0, hz), (hx1 - half, ym, hz + rise)], M["slate"])
LOG["dims"]["right_roof_pitch_deg"] = 35.0
# central ticket-office section: 1 storey, W D W W D W, stone cornice + parapet, booking-hall clerestory roof behind; canopy missing
D.box(XR1, XL0, FY - 0.05, FY + 0.30, ZB + H_C - 0.35, ZB + H_C, M["stone"])
B.box(XR1, XL0, FY - 0.35, FY, ZB + H_C, ZB + H_C + 0.8, M["stock"])
D.box(XR1 - 0.05, XL0 + 0.05, FY - 0.42, FY + 0.08, ZB + H_C + 0.8, ZB + H_C + 0.95, M["stone"])
DR = MB("cp70_station_doors", C_BLD, [M["door"]])
slot = (XL0 - XR1) / 6.0
for i, kind in enumerate("WDWWDW"):
    xc = XR1 + slot * (i + 0.5)
    if kind == "W":
        window(W, xc, ZB + 1.0, 1.45, 3.2, FY, arched=True)
    else:   # round-headed doorcase with fanlight: rusticated stone surround, glazed fanlight, panelled double doors
        w, h = 1.9, 4.1; zs = ZB + h - w / 2
        for sx in (-1, 1):   # rusticated jambs
            for k in range(int((zs - ZB) / 0.45) + 1):
                za = ZB + k * 0.45; zb_ = min(zs, za + 0.40); ext = 0.42 if k % 2 == 0 else 0.30
                if zb_ > za: D.box(xc + sx * w / 2, xc + sx * (w / 2 + ext), FY - 0.02, FY + 0.12, za, zb_, M["stone"])
        for k in range(9):    # voussoirs
            a0, a1 = math.pi * k / 9, math.pi * (k + 1) / 9; r0, r1 = w / 2, w / 2 + 0.38
            pts = [(xc + r0 * math.cos(a0), zs + r0 * math.sin(a0)), (xc + r1 * math.cos(a0), zs + r1 * math.sin(a0)),
                   (xc + r1 * math.cos(a1), zs + r1 * math.sin(a1)), (xc + r0 * math.cos(a1), zs + r0 * math.sin(a1))]
            D.prism_y(pts, FY - 0.02, FY + 0.12 + (0.02 if k % 2 else 0.0), M["stone"])
        D.box(xc - 0.18, xc + 0.18, FY + 0.10, FY + 0.20, zs + w / 2 + 0.05, zs + w / 2 + 0.55, M["stone"])   # keystone
        W.prism_y(arch_pts(xc - w / 2, xc + w / 2, zs - 0.12, zs), FY + 0.12, FY + 0.13, M["glass"])
        for k in range(1, 6):   # fanlight radial bars
            a = math.pi * k / 6; W.limb((xc, FY + 0.14, zs), (xc + (w / 2) * math.cos(a), FY + 0.14, zs + (w / 2) * math.sin(a)), 0.02, 0.02, M["sash"], 4)
        W.prism_y([(xc - w / 2, zs), (xc + w / 2, zs), (xc + w / 2, zs + w / 2), (xc - w / 2, zs + w / 2)], FY + 0.12, FY + 0.125, M["glass"])
        W.prism_y(arch_pts(xc - w / 2, xc + w / 2, zs, zs, 12)[2:] + [(xc - w / 2, zs)], FY + 0.12, FY + 0.13, M["glass"])
        DR.box(xc - w / 2, xc + w / 2, FY - 0.20, FY + 0.05, ZB, zs - 0.12, M["door"])      # opening reveal
        for s in (-1, 1):  # door leaves, the east one open (visitor emerging)
            if i == 1 and s == 1:
                DR.box(xc + w / 2 - 0.05, xc + w / 2 + 0.0, FY + 0.05, FY + 0.95, ZB + 0.02, zs - 0.15, M["door"])
                W.box(xc, xc + w / 2, FY + 0.05, FY + 0.06, ZB, zs - 0.12, M["glass"])   # dark interior through the open leaf
            else:
                xa, xb = (xc - w / 2, xc - 0.01) if s < 0 else (xc + 0.01, xc + w / 2)
                DR.box(xa, xb, FY + 0.05, FY + 0.10, ZB, zs - 0.15, M["door"])
                W.box(xa + 0.12, xb - 0.12, FY + 0.10, FY + 0.11, ZB + 1.1, zs - 0.4, M["glass"])
# booking hall with clerestory roof (behind the parapet)
cx0, cx1, cy0, cy1 = XR1 + 0.6, XL0 - 0.6, FY - DEPTH_C + 0.6, FY - 0.8
ce = ZB + H_C + 0.2; cl = 1.8; crise = 2.4; cmy = (cy0 + cy1) / 2; cw = 2.2
RF.quadstrip([[(cx0, cy1, ce), (cx1, cy1, ce)], [(cx0, cmy + cw, ce + 1.3), (cx1, cmy + cw, ce + 1.3)]], M["slate"])
RF.quadstrip([[(cx1, cy0, ce), (cx0, cy0, ce)], [(cx1, cmy - cw, ce + 1.3), (cx0, cmy - cw, ce + 1.3)]], M["slate"])
W.box(cx0, cx1, cmy - cw, cmy + cw, ce + 1.3, ce + 1.3 + cl, M["glass"])
for k in range(int((cx1 - cx0) / 0.9) + 1):
    xx = cx0 + k * 0.9; IR.box(xx - 0.04, xx + 0.04, cmy + cw - 0.02, cmy + cw + 0.04, ce + 1.3, ce + 1.3 + cl, M["iron"])
RF.quadstrip([[(cx0 - 0.3, cmy + cw + 0.3, ce + 1.3 + cl), (cx1 + 0.3, cmy + cw + 0.3, ce + 1.3 + cl)], [(cx0 - 0.3, cmy, ce + 1.3 + cl + 0.9), (cx1 + 0.3, cmy, ce + 1.3 + cl + 0.9)]], M["slate"])
RF.quadstrip([[(cx1 + 0.3, cmy - cw - 0.3, ce + 1.3 + cl), (cx0 - 0.3, cmy - cw - 0.3, ce + 1.3 + cl)], [(cx1 + 0.3, cmy, ce + 1.3 + cl + 0.9), (cx0 - 0.3, cmy, ce + 1.3 + cl + 0.9)]], M["slate"])
for mb in (B, D, RF, IR, W, DR): mb.done()

# ------------------------------------------------------------------ road, pavements, markings
S = MB("cp70_station_road", C_ST, [M["asphalt"]])
RX0, RX1 = SX - 170.0, SX + 170.0
S.box(RX0, RX1, KERB_S, ROAD_N, ZR - 2.5, ZR, M["asphalt"])
S.box(RX0, RX1, FY - 0.05, KERB_S - 0.15, ZR - 2.5, ZP, M["paving"])                    # forecourt pavement
S.box(RX0, RX1, ROAD_N + 0.15, WALL_Y, ZR - 2.5, ZP, M["paving"])                       # park-side pavement
for yk in (KERB_S - 0.15, ROAD_N):
    S.box(RX0, RX1, yk, yk + 0.15, ZR - 0.3, ZP, M["kerb"])
S.box(BX0 - 8, BX1 + 8, FY - 14.5, FY - 0.05, FOUND, ZP, M["paving"])                     # station plinth / side yards
for yl in (KERB_S + 0.25, KERB_S + 0.45, ROAD_N - 0.35, ROAD_N - 0.55):               # double yellow lines
    S.box(RX0, RX1, yl - 0.05, yl + 0.05, ZR, ZR + 0.004, M["yellow"])
ZEBRA = False                      # D-PM-38: no evidence for a zebra crossing at the gate; none modelled
ZEB0, ZEB1 = GATE_X - 1.6, GATE_X + 1.6
ymid = (KERB_S + ROAD_N) / 2
for k in range(int((RX1 - RX0) / 9.0)):                                               # centre line dashes (not on the zebra)
    xa = RX0 + k * 9.0
    if ZEBRA and xa + 4.0 > ZEB0 - 8 and xa < ZEB1 + 8: continue
    S.box(xa, xa + 4.0, ymid - 0.05, ymid + 0.05, ZR, ZR + 0.004, M["white"])
yy = KERB_S + 0.2
while ZEBRA and yy + 0.5 < ROAD_N - 0.1:                                                         # zebra stripes, 0.5 m on / 0.5 m off
    S.box(ZEB0, ZEB1, yy, yy + 0.5, ZR, ZR + 0.005, M["white"]); yy += 1.0
for side in ((-1, 1) if ZEBRA else ()):                                               # zig-zag approach lines (white)
    for yzz in (KERB_S + 0.35, ROAD_N - 0.35):
        x = ZEB0 - 1.5 if side < 0 else ZEB1 + 1.5
        for k in range(8):
            xa = x + side * k * 1.5; xb = xa + side * 1.5
            ya, yb = (yzz - 0.12, yzz + 0.12) if k % 2 == 0 else (yzz + 0.12, yzz - 0.12)
            S.limb((xa, ya, ZR + 0.003), (xb, yb, ZR + 0.003), 0.05, 0.05, M["white"], 4)
if ZEBRA: S.box(ZEB0 - 0.1, ZEB1 + 0.1, KERB_S + 0.05, KERB_S + 0.15, ZR, ZR + 0.004, M["white"]); S.box(ZEB0 - 0.1, ZEB1 + 0.1, ROAD_N - 0.15, ROAD_N - 0.05, ZR, ZR + 0.004, M["white"])
road = S.done()
# Belisha beacons + street lamps + bollards
F = MB("cp70_street_furniture", C_ST, [M["grey_steel"]])
for yb in ((KERB_S - 0.6, ROAD_N + 0.6) if ZEBRA else ()):
    for xb in (ZEB0 - 0.5, ZEB1 + 0.5):
        for k in range(8):
            F.limb((xb, yb, ZP + k * 0.33), (xb, yb, ZP + (k + 1) * 0.33), 0.045, 0.045, M["text_dark"] if k % 2 == 0 else M["white"], 10)
        F.sphere((xb, yb, ZP + 2.64 + 0.16), 0.16, M["amber"], u=14, v=10)
for xl in (SX - 31, SX + 4, SX + 40, SX + 76):
    F.limb((xl, WALL_Y - 0.6, ZP), (xl, WALL_Y - 0.6, ZP + 8.0), 0.09, 0.06, M["grey_steel"], 10)
    F.limb((xl, WALL_Y - 0.6, ZP + 8.0), (xl, WALL_Y - 1.9, ZP + 8.1), 0.05, 0.05, M["grey_steel"], 8)
    F.box(xl - 0.18, xl + 0.18, WALL_Y - 2.4, WALL_Y - 1.6, ZP + 7.95, ZP + 8.12, M["grey_steel"])
    F.box(xl - 0.15, xl + 0.15, WALL_Y - 2.35, WALL_Y - 1.65, ZP + 7.93, ZP + 7.95, M["lamp_glow"])
for k in range(7):
    xb = DOOR_X - 13 + k * 3.2
    if abs(xb - DOOR_X) < 3.6: continue
    F.limb((xb, KERB_S - 0.55, ZP), (xb, KERB_S - 0.55, ZP + 0.95), 0.08, 0.08, M["iron"], 10)
F.done()

# ------------------------------------------------------------------ park boundary + gate + path
PK = MB("cp70_park_boundary", C_PK, [M["stock"]])
GW = 4.2; G0, G1 = GATE_X - GW / 2, GATE_X + GW / 2
for (xa, xb) in ((RX0, G0 - 0.7), (G1 + 0.7, RX1)):
    PK.box(xa, xb, WALL_Y, WALL_Y + 0.35, ZR - 1.0, ZP + 0.6, M["stock"])
    PK.box(xa, xb, WALL_Y - 0.04, WALL_Y + 0.39, ZP + 0.6, ZP + 0.68, M["stone"])
    PK.box(xa, xb, WALL_Y + 0.15, WALL_Y + 0.2, ZP + 0.68 + 1.25, ZP + 0.68 + 1.3, M["iron"])
    PK.box(xa, xb, WALL_Y + 0.15, WALL_Y + 0.2, ZP + 0.68 + 0.10, ZP + 0.68 + 0.14, M["iron"])
    x = xa + 0.08
    while x < xb - 0.05:
        if abs(x - SX) < 90:
            PK.box(x - 0.012, x + 0.012, WALL_Y + 0.165, WALL_Y + 0.185, ZP + 0.68, ZP + 0.68 + 1.42, M["iron"])
        x += 0.14
for xp in (G0 - 0.35, G1 + 0.35):           # gate piers: stock brick, red-brick bands, stone cap + ball
    PK.box(xp - 0.36, xp + 0.36, WALL_Y - 0.18, WALL_Y + 0.54, ZR - 1.0, ZP + 2.5, M["stock"])
    for zb in (ZP + 0.8, ZP + 1.6): PK.box(xp - 0.37, xp + 0.37, WALL_Y - 0.19, WALL_Y + 0.55, zb, zb + 0.23, M["redbrick"])
    PK.box(xp - 0.46, xp + 0.46, WALL_Y - 0.28, WALL_Y + 0.64, ZP + 2.5, ZP + 2.68, M["stone"])
    PK.sphere((xp, WALL_Y + 0.18, ZP + 2.9), 0.22, M["stone"], u=12, v=8)
for s in (-1, 1):                            # open gates, swung into the park ~75 deg
    hx = G0 if s < 0 else G1; ang = math.radians(75); L_ = GW / 2 - 0.05
    dx, dy = -s * math.cos(ang) * L_, math.sin(ang) * L_
    p0 = Vector((hx, WALL_Y + 0.2, 0)); p1 = Vector((hx + dx, WALL_Y + 0.2 + dy, 0))
    for zz in (ZP + 0.1, ZP + 1.0, ZP + 1.85):
        PK.limb((p0.x, p0.y, zz), (p1.x, p1.y, zz), 0.025, 0.025, M["iron"], 6)
    for k in range(int(L_ / 0.13) + 1):
        q = p0.lerp(p1, k / (L_ / 0.13)); PK.limb((q.x, q.y, ZP + 0.1), (q.x, q.y, ZP + 2.0), 0.011, 0.011, M["iron"], 4)
PK.box(G0, G1, WALL_Y - 0.05, WALL_Y + 0.6, ZR - 1.0, ZP + 0.01, M["paving"])
pk = PK.done()
# local present-day lawn over the dated 1856 parterre beds/paths (they stand 0.14-0.26 m proud of the slope with dark edges)
M["lawn"] = mat_noise("CP70_ParkLawn", (0.065, 0.14, 0.04), (0.13, 0.24, 0.065), 0.95, 1.6, 0.04)
LW_X0, LW_X1, LW_Y0, LW_Y1, LW_F, LW_UP = GATE_X - 75.0, GATE_X + 75.0, WALL_Y + 0.36, WALL_Y + 110.0, 14.0, 0.34
def lawn_z(x, y):
    e = min(x - LW_X0, LW_X1 - x, LW_Y1 - y, 1e9) / LW_F
    return ground(x, y) + (LW_UP if e >= 1 else -0.05 + (LW_UP + 0.05) * max(0.0, e) ** 0.7)
LN = MB("cp70_park_lawn", C_PK, [M["lawn"]]); rows = []
for j in range(41):
    yv = LW_Y0 + (LW_Y1 - LW_Y0) * j / 40.0
    rows.append([(LW_X0 + (LW_X1 - LW_X0) * i / 60.0, yv, lawn_z(LW_X0 + (LW_X1 - LW_X0) * i / 60.0, yv)) for i in range(61)])
LN.quadstrip(rows, M["lawn"]); LN.box(LW_X0, LW_X1, WALL_Y + 0.3, WALL_Y + 0.4, ZR - 1.0, ZP + 0.2, M["lawn"]); LN.done()
def ground_now(x, y):
    if LW_X0 < x < LW_X1 and WALL_Y + 0.36 < y < LW_Y1: return lawn_z(x, y)
    return ground(x, y)
# tarmac path climbing into the park (follows the slope), grass edges stay the park_slope
PA = MB("cp70_park_path", C_PK, [M["tarmac_path"]])
rows = []; y = WALL_Y + 0.6; pw = 3.6
path_pts = []
while y < WALL_Y + 70:
    t = (y - WALL_Y) / 70.0; xc = GATE_X + 9.0 * math.sin(t * 1.4)
    z = max(ground_now(xc, y) + 0.03, ZP + 0.0 if y < WALL_Y + 1.5 else -1e9)
    rows.append([(xc - pw / 2, y, z), (xc + pw / 2, y, z)]); path_pts.append((xc, y, z)); y += 1.5
PA.quadstrip(rows, M["tarmac_path"])
for sd in (-1, 1):   # concrete edging either side of the path
    erows = []
    for r in rows:
        xe = r[0][0] if sd < 0 else r[1][0]
        erows.append([(xe - 0.16, r[0][1], r[0][2] + 0.012), (xe + 0.16, r[0][1], r[0][2] + 0.012)])
    PA.quadstrip(erows, M["paving"])
# two park benches beside the path (timber slats, black iron ends)
M["bench"] = mat_noise("CP70_BenchTimber", (0.20, 0.13, 0.07), (0.28, 0.19, 0.10), 0.8, 30.0, 0.03)
for k_, j in enumerate((7, 16)):
    px, py, pz = path_pts[j]; bxx = px + (pw / 2 + 0.9) * (1 if k_ == 0 else -1); fz = ground_now(bxx, py)
    for dy_ in (-0.8, 0.8):
        PA.box(bxx - 0.3, bxx + 0.3, py + dy_ - 0.03, py + dy_ + 0.03, fz, fz + 0.45, M["iron"])
    for i_ in range(4): PA.box(bxx - 0.25 + i_ * 0.13, bxx - 0.25 + i_ * 0.13 + 0.1, py - 0.95, py + 0.95, fz + 0.43, fz + 0.47, M["bench"])
    sxo = 0.3 if k_ == 0 else -0.3
    for i_ in range(3): PA.box(bxx + sxo - 0.02, bxx + sxo + 0.02, py - 0.95, py + 0.95, fz + 0.55 + i_ * 0.13, fz + 0.64 + i_ * 0.13, M["bench"])
PA.done()
# park name board by the gate (I: present-day board, design by eye)
SG = MB("cp70_signs", C_SIGN, [M["park_green"]])
bx = G1 + 2.6; by = WALL_Y + 1.6; bz = ground_now(bx, by)
for dx in (-0.75, 0.75): SG.box(bx + dx - 0.04, bx + dx + 0.04, by - 0.04, by + 0.04, bz, bz + 2.2, M["iron"])
SG.box(bx - 0.95, bx + 0.95, by - 0.03, by + 0.03, bz + 1.2, bz + 2.15, M["park_green"])
# ------------------------------------------------------------------ station signs: Rail Symbol 2 totem + parapet board
BR = [(203.1, 289.5), (203.1, 306.04), (154.68, 306.04), (107.44, 329.66), (203.11, 329.66), (203.11, 346.2), (107.44, 346.2),
      (170.04, 372.18), (127.52, 372.18), (72.01, 346.2), (23.59, 346.2), (23.59, 329.66), (72.01, 329.66), (119.25, 306.04),
      (23.58, 306.04), (23.58, 289.5), (119.25, 289.5), (56.65, 263.52), (99.17, 263.52), (154.68, 289.5)]   # Commons SVG path (y down)
def rail_symbol(mb, cx, y, cz, width, facing=1):
    """facing=+1: readable from +y; -1: from -y (mirror x so the top arrow still points right)."""
    s = width / (203.11 - 23.58); xm = (203.11 + 23.58) / 2; ymn = (263.52 + 372.18) / 2
    pts = [(cx - facing * (px - xm) * s, cz - (py - ymn) * s) for px, py in BR]   # viewer facing -y has +x on the left
    vs = [mb.bm.verts.new((px, y, pz)) for px, pz in pts]; f = mb.bm.faces.new(vs); f.material_index = mb.mi(M["rail_red"])
TX, TY = DOOR_X + 4.5, KERB_S - 1.0
SG.limb((TX, TY, ZP), (TX, TY, ZP + 3.3), 0.07, 0.07, M["grey_steel"], 12)
SG.box(TX - 0.62, TX + 0.62, TY - 0.06, TY + 0.06, ZP + 3.3, ZP + 4.2, M["sign_white"])
SG.box(TX - 0.62, TX + 0.62, TY - 0.065, TY + 0.065, ZP + 3.3, ZP + 3.33, M["rail_red"])
rail_symbol(SG, TX, TY + 0.065, ZP + 3.80, 0.92, 1); rail_symbol(SG, TX, TY - 0.065, ZP + 3.80, 0.92, -1)
SG.box(TX - 1.1, TX + 1.1, TY - 0.09, TY + 0.09, ZP + 2.55, ZP + 3.15, M["sign_white"])                # name board under the symbol
SG.box((XR1 + XL0) / 2 - 4.9, (XR1 + XL0) / 2 + 4.9, FY + 0.05, FY + 0.12, ZB + H_C + 0.05, ZB + H_C + 0.75, M["cream"])
SG.done()
def text(name, body, x, y, z, size, mat, facing=1, align="CENTER"):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size; cu.align_x = align; cu.align_y = "CENTER"; cu.extrude = 0.004
    ob = bpy.data.objects.new(name, cu); C_SIGN.objects.link(ob); ob.data.materials.append(mat)
    ob.rotation_euler = (math.pi / 2, 0, 0 if facing < 0 else math.pi); ob.location = (x, y, z); ob["cp070_now"] = TAG; return ob
text("cp70_txt_totem_N", "Crystal Palace", TX, TY + 0.095, ZP + 2.85, 0.30, M["text_dark"], 1)
text("cp70_txt_totem_S", "Crystal Palace", TX, TY - 0.095, ZP + 2.85, 0.30, M["text_dark"], -1)
text("cp70_txt_parapet", "CRYSTAL PALACE STATION", (XR1 + XL0) / 2, FY + 0.13, ZB + H_C + 0.40, 0.46, M["text_dark"], 1)
text("cp70_txt_park1", "Crystal Palace Park", bx, by + 0.04, bz + 1.85, 0.20, M["sign_white"], 1)
text("cp70_txt_park2", "Bromley  -  open dawn to dusk", bx, by + 0.04, bz + 1.5, 0.11, M["sign_white"], 1)

# ------------------------------------------------------------------ present-day visitors (parametric)
SKIN = [mat_plain(f"CP70_Skin{i}", c, 0.55) for i, c in enumerate([(0.62, 0.45, 0.36), (0.42, 0.28, 0.20), (0.24, 0.15, 0.10), (0.55, 0.40, 0.30)])]
HAIR = [mat_plain(f"CP70_Hair{i}", c, 0.6) for i, c in enumerate([(0.03, 0.02, 0.015), (0.16, 0.09, 0.04), (0.45, 0.33, 0.16), (0.30, 0.30, 0.30)])]
TOP = [mat_plain(f"CP70_Top{i}", c, 0.8) for i, c in enumerate([(0.04, 0.06, 0.12), (0.45, 0.06, 0.05), (0.13, 0.17, 0.09), (0.03, 0.03, 0.03), (0.55, 0.47, 0.33), (0.62, 0.62, 0.60), (0.08, 0.22, 0.35)])]
LEG = [mat_noise(f"CP70_Denim{i}", c0, c1, 0.85, 60.0, 0.02) for i, (c0, c1) in enumerate([((0.05, 0.08, 0.16), (0.09, 0.13, 0.24)), ((0.02, 0.02, 0.025), (0.05, 0.05, 0.05)), ((0.25, 0.21, 0.14), (0.31, 0.27, 0.18))])]
SHOE = [mat_plain("CP70_ShoeWhite", (0.75, 0.75, 0.73), 0.5), mat_plain("CP70_ShoeDark", (0.04, 0.035, 0.03), 0.45)]
BAG = mat_plain("CP70_Backpack", (0.06, 0.07, 0.08), 0.7)
def person_now(name, x, y, facing, H=1.75, top=0, leg=0, skin=0, hair=0, shoe=0, stride=0.0, bag=False, phone=False, coat=False, hat=None):
    mb = MB(name, C_PPL, [SKIN[skin]]); s = H / 1.75
    hip, sh, hc = 0.92 * s, 1.44 * s, 1.63 * s
    for side in (-1, 1):
        fy = side * stride * 0.5
        ank = Vector((side * 0.10 * s, fy, 0.09 * s)); hp = Vector((side * 0.095 * s, 0, hip))
        mb.limb(hp, ank, 0.078 * s, 0.052 * s, LEG[leg], 10)
        mb.box(ank.x - 0.055 * s, ank.x + 0.055 * s, fy - 0.08 * s, fy + 0.19 * s, 0.0, 0.085 * s, SHOE[shoe])
    mb.limb((0, 0, hip - 0.06 * s), (0, 0, hip + 0.08 * s), 0.17 * s, 0.17 * s, LEG[leg], 12)
    zb = (hip - 0.18 * s) if coat else (hip - 0.02 * s)
    mb.limb((0, 0, zb), (0, 0, sh), 0.175 * s if not coat else 0.2 * s, 0.205 * s, TOP[top], 14)
    mb.sphere((0, 0, sh - 0.01 * s), 0.205 * s, TOP[top], sc=(1.0, 0.62, 0.32), u=14, v=8)
    mb.limb((0, 0, sh), (0, 0, sh + 0.09 * s), 0.055 * s, 0.05 * s, SKIN[skin], 8)
    mb.sphere((0, 0.005, hc), 0.112 * s, SKIN[skin], sc=(0.86, 0.95, 1.08), u=14, v=10)
    mb.sphere((0, -0.022 * s, hc + 0.03 * s), 0.112 * s, HAIR[hair], sc=(0.9, 0.95, 0.97), u=14, v=10)
    if hat == "beanie": mb.sphere((0, -0.01 * s, hc + 0.05 * s), 0.118 * s, TOP[(top + 3) % len(TOP)], sc=(0.92, 0.96, 0.85), u=14, v=8)
    for side in (-1, 1):
        shp = Vector((side * 0.215 * s, 0, sh - 0.04 * s))
        if phone and side > 0:
            el = Vector((side * 0.23 * s, 0.10 * s, sh - 0.33 * s)); hd = Vector((side * 0.06 * s, 0.30 * s, sh - 0.30 * s))
            mb.limb(shp, el, 0.055 * s, 0.05 * s, TOP[top], 8); mb.limb(el, hd, 0.05 * s, 0.042 * s, TOP[top], 8)
            mb.sphere(hd, 0.045 * s, SKIN[skin]); mb.box(hd.x - 0.04, hd.x + 0.04, hd.y - 0.01, hd.y + 0.01, hd.z, hd.z + 0.15, SHOE[1])
        else:
            sw = -side * stride * 0.45
            hd = Vector((side * 0.25 * s, sw, sh - 0.62 * s))
            mb.limb(shp, hd, 0.058 * s, 0.045 * s, TOP[top], 8); mb.sphere(hd, 0.047 * s, SKIN[skin])
    if bag:
        mb.box(-0.16 * s, 0.16 * s, -0.27 * s, -0.11 * s, sh - 0.48 * s, sh - 0.04 * s, BAG)
        for side in (-1, 1): mb.limb((side * 0.12 * s, -0.12 * s, sh - 0.05 * s), (side * 0.12 * s, 0.10 * s, sh - 0.02 * s), 0.02 * s, 0.02 * s, BAG, 4)
    ob = mb.done(smooth=True)
    z = ZP if y < WALL_Y else ground_now(x, y) + 0.0
    if WALL_Y - 0.05 < y < WALL_Y + 1.0: z = ZP
    po = bpy.data.objects.get("cp70_park_path")          # on the path: stand on its actual (interpolated) surface
    if po:
        ok_, hit_, n_, i_ = po.ray_cast(Vector((x, y, 400.0)), Vector((0, 0, -1)))
        if ok_: z = hit_.z
    if y < FY: z = ZB
    ob.location = (x, y, z); ob.rotation_euler = (0, 0, math.atan2(-facing[0], facing[1])); ob["H_m"] = round(H, 2); return ob
V = []
V.append(person_now("cp70_ppl_emerging", DOOR_X + 0.1, FY + 1.0, (0.15, 1.0), 1.74, top=1, leg=0, skin=0, hair=1, shoe=0, stride=0.42, bag=True))
V.append(person_now("cp70_ppl_forecourt_phone", TX + 1.6, KERB_S - 1.9, (0.6, 0.6), 1.66, top=4, leg=1, skin=1, hair=0, shoe=1, phone=True, coat=True))
V.append(person_now("cp70_ppl_forecourt_walk", DOOR_X + 12.0, FY + 1.6, (-1.0, 0.0), 1.80, top=0, leg=2, skin=2, hair=0, shoe=1, stride=0.5))
V.append(person_now("cp70_ppl_forecourt_2", DOOR_X + 19.0, FY + 2.4, (1.0, 0.1), 1.70, top=6, leg=0, skin=3, hair=2, shoe=0, stride=0.46, bag=True))
V.append(person_now("cp70_ppl_gate_in", GATE_X + 0.9, WALL_Y + 13.0, (0.05, 1.0), 1.62, top=2, leg=1, skin=0, hair=2, shoe=0, stride=0.4))
V.append(person_now("cp70_ppl_gate_in2", GATE_X - 0.3, WALL_Y + 19.5, (0.05, 1.0), 1.78, top=3, leg=0, skin=1, hair=0, shoe=1, stride=0.38, hat="beanie"))
V.append(person_now("cp70_ppl_parkpath_far", path_pts[22][0] + 0.6, path_pts[22][1], (-0.2, -1.0), 1.72, top=5, leg=0, skin=0, hair=3, shoe=1, stride=0.4, coat=True))
V.append(person_now("cp70_ppl_northpav", GATE_X - 22.0, WALL_Y - 1.2, (1.0, 0.0), 1.68, top=1, leg=1, skin=2, hair=0, shoe=0, stride=0.45))
V.append(person_now("cp70_ppl_northpav2", GATE_X + 14.0, WALL_Y - 1.4, (-1.0, 0.05), 1.76, top=6, leg=2, skin=0, hair=1, shoe=1, stride=0.45, bag=True))
LOG["visitors"] = [(o.name, round(o.location.x, 2), round(o.location.y, 2), round(o.location.z, 2), o["H_m"]) for o in V]

# ------------------------------------------------------------------ park trees (MV20 v2 generator)
PT.LEAF_GAIN = 1.0
trees = [(GATE_X - 9.0, WALL_Y + 6.5, 15.0, "oak"), (GATE_X + 8.5, WALL_Y + 5.5, 17.0, "elm"), (GATE_X - 24.0, WALL_Y + 7.0, 14.0, "oak"),
         (GATE_X + 24.0, WALL_Y + 8.0, 16.0, "oak"), (GATE_X - 3.0, WALL_Y + 26.0, 18.0, "elm"), (GATE_X + 18.0, WALL_Y + 30.0, 15.0, "oak"),
         (GATE_X - 40.0, WALL_Y + 9.0, 15.0, "elm"), (GATE_X + 42.0, WALL_Y + 10.0, 14.0, "oak"), (GATE_X - 18.0, WALL_Y + 38.0, 17.0, "oak"),
         (GATE_X + 33.0, WALL_Y + 44.0, 16.0, "elm")]
LOG["trees"] = []
for i, (tx, ty, H, hab) in enumerate(trees):
    me, info = PT.build_tree(f"cp70_tree_{i:02d}", hab, H, 7000 + i * 37)
    ob = bpy.data.objects.new(f"cp70_tree_{i:02d}", me); C_TR.objects.link(ob)
    ob.location = (tx, ty, ground_now(tx, ty) - 0.05); ob.rotation_euler[2] = R.uniform(0, 2 * math.pi); ob["cp070_now"] = TAG
    LOG["trees"].append((ob.name, hab, H, round(tx, 1), round(ty, 1)))

# placeholder 'lollipop' trees inside the lawn patch -> parametric trees at the same trunk spot (as CP076 D-PM-28)
LOG["replaced_trees"] = []
for o in list(bpy.data.objects):
    if not (o.name.startswith("PLACEHOLDER_park_tree") and o.name.endswith("_crown")) or o.hide_render: continue
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]; cx = sum(v.x for v in bb) / 8; cy = sum(v.y for v in bb) / 8; ztop = max(v.z for v in bb)
    if not (SX - 170 < cx < SX + 170 and WALL_Y + 3 < cy < WALL_Y + 200): continue
    gz = ground_now(cx, cy); H = max(10.0, min(19.0, ztop - gz))
    me, info = PT.build_tree(o.name.replace("_crown", "_now"), "oak" if len(LOG["replaced_trees"]) % 3 else "elm", H, 7700 + len(LOG["replaced_trees"]) * 53)
    t = bpy.data.objects.new("cp70_" + o.name.replace("_crown", "_now"), me); C_TR.objects.link(t)
    t.location = (cx, cy, gz - 0.05); t.rotation_euler[2] = R.uniform(0, 2 * math.pi); t["cp070_now"] = TAG
    o.hide_render = True; LOG["hidden"].append((o.name, "lollipop placeholder replaced by a parametric tree"))
    tr = bpy.data.objects.get(o.name.replace("_crown", "_trunk"))
    if tr and not tr.hide_render: tr.hide_render = True; LOG["hidden"].append((tr.name, "lollipop placeholder replaced by a parametric tree"))
    LOG["replaced_trees"].append((o.name, round(cx, 1), round(cy, 1), round(H, 1)))
# ------------------------------------------------------------------ hide anachronisms / clashes (hide_render only; nothing deleted)
col = bpy.data.collections.get("SY54_railway_colonnade")
if col:
    for o in col.all_objects:
        if not o.hide_render: o.hide_render = True; LOG["hidden"].append((o.name, "1854 covered way, not standing today"))
BOXX = (RX0, RX1, FY - 22.0, WALL_Y + 3.0)
for o in bpy.data.objects:
    if o.name.startswith("PLACEHOLDER_park_tree") or o.name.startswith("pk_tree_") or o.name.startswith("ppl_now"):
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]; cx = sum(v.x for v in bb) / 8; cy = sum(v.y for v in bb) / 8
        if BOXX[0] < cx < BOXX[1] and BOXX[2] < cy < BOXX[3] and not o.hide_render:
            o.hide_render = True; LOG["hidden"].append((o.name, "inside the new station/road footprint"))
# trunk/crown pairs: hide the partner of any hidden placeholder tree part
hid = {n for n, _ in LOG["hidden"]}
for n in list(hid):
    for suf_a, suf_b in (("_crown", "_trunk"), ("_trunk", "_crown")):
        if n.endswith(suf_a):
            o = bpy.data.objects.get(n[: -len(suf_a)] + suf_b)
            if o and not o.hide_render: o.hide_render = True; LOG["hidden"].append((o.name, "partner of hidden tree part"))

# ------------------------------------------------------------------ cameras (both CP070 cams moved to the station)
def aim(name, loc, look):
    c = bpy.data.objects[name]; c.location = Vector(loc); c.rotation_euler = (Vector(look) - c.location).to_track_quat("-Z", "Y").to_euler()
    c.data.lens = 35.0; c["cp070_now"] = TAG; LOG["cams"][name] = {"loc": [round(v, 3) for v in loc], "look": [round(v, 3) for v in look], "lens": 35}
CB = Vector((CB_X, WALL_Y - 1.2, ZP + 1.6))
CE = CB + Vector((WALK, 0.0, 0.0))                                   # 8 m east along the park-side pavement, to the gate
aim("CAM_CP070_begin_walk_35mm", CB, (XL0 + 2.0, FY - 1.0, ZB + 8.2))
aim("CAM_CP070_park_entry_35mm", CE, (GATE_X + 3.0, WALL_Y + 40.0, ZP + 3.2))
LOG["cams"]["walk_m"] = round((CE - CB).length, 3)

bpy.context.scene["cp070_station_candidate"] = TAG
LOG["objects"] = sum(1 for o in bpy.data.objects if "cp070_now" in o.keys())
os.makedirs(os.path.join(os.path.dirname(HERE), "checks"), exist_ok=True)
json.dump(LOG, open(os.path.join(os.path.dirname(HERE), "checks", "cp070_station_candidate.json"), "w"), indent=1)
if not A.no_save:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True, copy=True)
print("CP070_CANDIDATE_SAVED", OUT, "objects", LOG["objects"], "hidden", len(LOG["hidden"]), "station", LOG["station_ngr_model"], "ZR", ZR, flush=True)
