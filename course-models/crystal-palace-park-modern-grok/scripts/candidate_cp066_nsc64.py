"""CP066 'A different architecture of recreation' - PARK60 (1960s) polish, CANDIDATE 2026-11-14 (Grok; no verdict).
blender -b rounds/park60-r17.blend -P scripts/candidate_cp066_nsc64.py -- [--out rounds/candidates/park60-r17_cp066nsc64.blend]
Never overwrites the opened (live) blend. PARK60 only (dated 1964-67); nothing of Hyde Park 1851 and no Victorian state is touched.

Live CP066 hero (renders/r17k_park60_CAM_CP066_nsc_stadium_35mm.png, D-PM-05/18) shows the NSC as four white concrete boxes
with flat pure-black tops boxed round a square red ring, a lit box for the sports hall and floodlight sticks. Read at a
glance it is a block-out, not a stadium, and it is the wrong shape for the 1960s: the 1964 stadium had ONE seated stand.

Candidate (DEPARTURES D-PM-42..D-PM-49), dated 1964-67 (stadium opened May 1964, NSC opened 13 Jul 1964; cinder track until
the Tartan track opened 19 May 1968; Jubilee Stand only in 1977):
 1. 440-yard cinder track (R: athleticstracks.co.uk; Guardian 8 Jan 2003) as a true oval: lap 402.34 m on the measurement
    line 0.30 m outside the kerb, bend radius 36.5 m (I), straights 85.56 m (derived), 8 lanes of 4 ft (1.22 m) (I),
    chalk lane lines, raised kerb, grass infield and grass apron.
 2. The 1964 West Stand (R: 'sickle-shaped seating formation, partially covered with a roof', Modernism in Metro-Land
    13 Jul 2024; 'West stand ... integrated into the topography', CPNSC feasibility study 2019) along the +y (west, up-
    slope) home straight, wrapping ~30 deg into each bend; 34 rows of bench seating on concrete treads (I), cantilevered
    canopy over the straight on rear columns (I).
 3. Open concrete terracing + grass banks round the rest of the bowl (east side open: the Jubilee Stand opposite is 1977, R).
 4. The sports centre building after the description 'central concrete A-frame, fully glazed upper level and large
    ventilation tower', 'covers 1.75 acres' (Modernism in Metro-Land): plinth, fully glazed upper storey with mullions,
    low-pitched roof on the A-frame spine, ventilation tower. Footprint rescaled to 1.75 acres; orientation/position U.
 5. Floodlight masts re-grounded (the r17 poles started 5.5 m above the terrain inside the old box banks) with lamp heads;
    the r17 flood lights themselves are left exactly as they were (same lights, energy, position, aim).
 6. Few people for scale: athletes training on the track and infield, spectators scattered on the stand and terraces
    (1960s stand-ins, generic).
Hidden (hide_render only, nothing deleted): the r17 NSC block-out boxes (infield, 4 track strips, 4 banks + seats + mid
tiers, sports hall box/roof/glazing, 4 poles). World, look, exposure, sun, flood lights, every camera: unchanged.
"""
import os, sys, json, math, random, argparse
import bpy, bmesh
from mathutils import Vector, Matrix
HERE = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser(); ap.add_argument("--out", default="rounds/candidates/park60-r17_cp066nsc64.blend")
ap.add_argument("--no-save", action="store_true")
A = ap.parse_args(argv)
SRC = bpy.data.filepath
OUT = A.out if os.path.isabs(A.out) else os.path.join(os.path.dirname(HERE), A.out)
assert os.path.abspath(OUT) != os.path.abspath(SRC), "refusing to overwrite the opened (live) blend"
assert not any("cp066_nsc" in o.keys() for o in bpy.data.objects), "source already carries the CP066 candidate"
TAG = "cp066_nsc64_v1"
R = random.Random(6664)
LOG = {"version": TAG, "src": SRC, "date_range": "1964-05 .. 1968-05 (cinder track; pre-Tartan, pre-Jubilee Stand)", "hidden": [], "objects": 0, "dims": {}}

PS = bpy.data.objects["park_slope"]
def ground(x, y):
    ok, loc, n, i = PS.ray_cast(PS.matrix_world.inverted() @ Vector((x, y, 400.0)), Vector((0, 0, -1)))
    assert ok, (x, y); return (PS.matrix_world @ loc).z

# ------------------------------------------------------------------ layout
CX, CY = -50.0, -550.0            # D-PM-05 stadium centre, unchanged
Z0 = -43.1                        # arena floor: just above the highest terrain inside the bowl (park_slope/central_walk -43.2 at the
                                  # +y outer lanes; -45.9 at the -y side, which the terraces/banks cover); r17 slab was at -40
LAP = 440 * 0.9144                # 440 yd = 402.336 m on the measurement line
RB = 36.5                         # kerb radius of the bends (I)
LS = (LAP - 2 * math.pi * (RB + 0.30)) / 2      # straight length from the lap
NL, LW = 8, 4 * 0.3048            # 8 lanes of 4 ft (I)
TW = NL * LW
LOG["dims"].update(lap_m=round(LAP, 3), bend_r=RB, straight=round(LS, 3), lanes=NL, lane_w=round(LW, 4),
                   track_outer_len=round(LS + 2 * (RB + TW), 2), track_outer_w=round(2 * (RB + TW), 2))

ROOT = bpy.data.collections.new("PARK60_CP066_NSC_1964_67"); bpy.data.collections["PARK60_NationalSportsCentre_1960s"].children.link(ROOT)
def sub(n):
    c = bpy.data.collections.new(n); ROOT.children.link(c); return c
C_TR = sub("CP066_track_440yd_cinder_1964"); C_ST = sub("CP066_west_stand_1964"); C_TE = sub("CP066_terraces_banks_1964")
C_HA = sub("CP066_sports_centre_1964"); C_FL = sub("CP066_floodlight_masts"); C_PP = sub("CP066_people_1960s")

# ------------------------------------------------------------------ materials (names avoid the look clamp keywords)
def _bsdf(m): return next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
def mat_plain(name, col, rough=0.8, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = _bsdf(m)
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal; m.diffuse_color = (*col, 1); return m
def mat_noise(name, c0, c1, rough=0.85, scale=6.0, bump=0.05):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; L = nt.links; b = _bsdf(m)
    tc = N.new("ShaderNodeTexCoord"); nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = scale; nz.inputs["Detail"].default_value = 8
    L.new(tc.outputs["Object"], nz.inputs["Vector"]); rp = N.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (*c0, 1); rp.color_ramp.elements[1].color = (*c1, 1)
    L.new(nz.outputs["Fac"], rp.inputs[0]); L.new(rp.outputs[0], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = rough
    bp = N.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump; L.new(nz.outputs["Fac"], bp.inputs["Height"]); L.new(bp.outputs["Normal"], b.inputs["Normal"])
    m.diffuse_color = (*c0, 1); return m
M = {}
M["cinder"] = mat_noise("CP66_CinderTrack1964", (0.13, 0.065, 0.045), (0.21, 0.105, 0.07), 0.95, 0.9, 0.06)
M["chalk"] = mat_plain("CP66_ChalkLine", (0.78, 0.78, 0.74), 0.9)
M["kerb"] = mat_plain("CP66_KerbWhite", (0.70, 0.70, 0.67), 0.7)
M["grass"] = mat_noise("CP66_InfieldTurf", (0.13, 0.27, 0.08), (0.20, 0.36, 0.12), 0.92, 0.35, 0.04)
M["bank"] = mat_noise("CP66_BankTurf", (0.15, 0.29, 0.09), (0.24, 0.38, 0.14), 0.92, 0.25, 0.05)
M["conc"] = mat_noise("CP66_InSituConcrete", (0.46, 0.45, 0.42), (0.58, 0.57, 0.53), 0.88, 2.5, 0.08)
M["conc_d"] = mat_noise("CP66_ConcreteWeathered", (0.34, 0.33, 0.31), (0.44, 0.43, 0.40), 0.9, 3.0, 0.08)
M["bench"] = mat_plain("CP66_BenchTimber", (0.30, 0.20, 0.12), 0.75)
M["roof"] = mat_plain("CP66_CanopySteelGrey", (0.52, 0.53, 0.54), 0.55, 0.3)
M["fascia"] = mat_plain("CP66_CanopyFascia", (0.66, 0.66, 0.64), 0.6)
M["steel"] = mat_plain("CP66_ColumnSteel", (0.12, 0.125, 0.13), 0.7, 0.0)
M["mast"] = mat_plain("CP66_MastGalvanised", (0.30, 0.31, 0.31), 0.6, 0.0)
M["pane"] = mat_plain("CP66_CurtainPaneDark", (0.05, 0.065, 0.075), 0.08)
M["mullion"] = mat_plain("CP66_MullionAlu", (0.62, 0.63, 0.63), 0.4, 0.7)
M["roofhall"] = mat_plain("CP66_HallRoofFelt", (0.17, 0.17, 0.18), 0.8)
M["lamp"] = mat_plain("CP66_LampLens", (0.80, 0.80, 0.76), 0.3)
M["sand"] = mat_plain("CP66_JumpSand", (0.62, 0.55, 0.40), 0.95)
for _k in ("pane",):
    _bsdf(M[_k]).inputs["Specular IOR Level"].default_value = 0.6

class MB:
    def __init__(self, name, coll):
        self.name, self.coll, self.mats = name, coll, []; self.bm = bmesh.new()
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
    def obox(self, c, u, v, hu, hv, z0, z1, m):
        """oriented box: centre c (x,y), unit axes u, v in plane, half sizes"""
        cs = [Vector(c) + u * su * hu + v * sv * hv for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        b = [self.bm.verts.new((p.x, p.y, z0)) for p in cs]; t = [self.bm.verts.new((p.x, p.y, z1)) for p in cs]
        fs = [self.bm.faces.new(t), self.bm.faces.new(list(reversed(b)))]
        for k in range(4): fs.append(self.bm.faces.new((b[k], b[(k + 1) % 4], t[(k + 1) % 4], t[k])))
        self._faces(fs, m)
    def poly(self, pts3, m):
        vs = [self.bm.verts.new(p) for p in pts3]; self._faces([self.bm.faces.new(vs)], m)
    def limb(self, p0, p1, r0, r1, m, segs=6):
        p0, p1 = Vector(p0), Vector(p1); d = p1 - p0; L = d.length
        q = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_matrix().to_4x4()
        r = bmesh.ops.create_cone(self.bm, cap_ends=True, segments=segs, radius1=r0, radius2=r1, depth=L, matrix=Matrix.Translation((p0 + p1) / 2) @ q)
        self._faces({f for v in r["verts"] for f in v.link_faces}, m)
    def sphere(self, c, rad, m, sc=(1, 1, 1), u=8, v=6):
        r = bmesh.ops.create_uvsphere(self.bm, u_segments=u, v_segments=v, radius=rad, matrix=Matrix.Translation(c) @ Matrix.Diagonal((*sc, 1)))
        self._faces({f for v_ in r["verts"] for f in v_.link_faces}, m)
    def done(self, smooth=False):
        bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)
        me = bpy.data.meshes.new(self.name); self.bm.to_mesh(me); self.bm.free()
        for m in self.mats: me.materials.append(m)
        if smooth:
            for p in me.polygons: p.use_smooth = True
        ob = bpy.data.objects.new(self.name, me); self.coll.objects.link(ob); ob["cp066_nsc"] = TAG; return ob

# ------------------------------------------------------------------ oval geometry: t in [0,4): 0-1 +y straight (x: + -> -),
# 1-2 -x bend, 2-3 -y straight (x: - -> +), 3-4 +x bend. d = offset outward from the inner kerb.
def oval(t, d):
    t = t % 4.0; s, f = int(t), t - int(t)
    if s == 0: return Vector((CX + LS / 2 - f * LS, CY + RB + d)), Vector((0, 1))
    if s == 2: return Vector((CX - LS / 2 + f * LS, CY - RB - d)), Vector((0, -1))
    a = math.radians(90 + f * 180) if s == 1 else math.radians(270 + f * 180)
    c = Vector((CX - LS / 2, CY)) if s == 1 else Vector((CX + LS / 2, CY))
    n = Vector((math.cos(a), math.sin(a))); return c + n * (RB + d), n
def tsamples(t0, t1, per_straight=10, per_bend=40):
    out = [t0]; t = t0
    while t < t1 - 1e-9:
        s = int(math.floor(t + 1e-9)) % 4; step = 1.0 / (per_straight if s in (0, 2) else per_bend)
        nxt = min(t1, math.floor(t + 1e-9) + step * (math.floor(((t + 1e-9) - math.floor(t + 1e-9)) / step) + 1))
        out.append(nxt); t = nxt
    return out
def sweep(mb, prof, t0, t1, m, zb=None, caps=True, mfun=None):
    """prof: top polyline [(d, z)] (d non-decreasing). Builds top surface; if zb given, front/back walls, bottom, end caps."""
    ts = tsamples(t0, t1); rows = []
    for t in ts:
        rows.append([mb.bm.verts.new((*oval(t, d)[0], z)) for d, z in prof])
    fs = []
    for a, b in zip(rows, rows[1:]):
        for k in range(len(prof) - 1):
            if abs(prof[k][0] - prof[k + 1][0]) < 1e-6 and abs(prof[k][1] - prof[k + 1][1]) < 1e-6: continue
            f = mb.bm.faces.new((a[k], a[k + 1], b[k + 1], b[k])); fs.append(f)
            if mfun: f.material_index = mb.mi(mfun(k))
    if not mfun: mb._faces(fs, m)
    else:
        pass
    if zb is not None:
        bot = [[mb.bm.verts.new((*oval(t, d)[0], zb)) for d in (prof[0][0], prof[-1][0])] for t in ts]
        ws = []
        for i in range(len(ts) - 1):
            ws.append(mb.bm.faces.new((bot[i][0], bot[i + 1][0], rows[i + 1][0], rows[i][0])))
            ws.append(mb.bm.faces.new((rows[i][-1], rows[i + 1][-1], bot[i + 1][1], bot[i][1])))
            ws.append(mb.bm.faces.new((bot[i][1], bot[i + 1][1], bot[i + 1][0], bot[i][0])))
        if caps:
            for i, rr in ((0, rows[0]), (len(ts) - 1, rows[-1])):
                for k in range(len(prof) - 1):
                    if abs(prof[k][0] - prof[k + 1][0]) < 1e-6: continue
                    b0 = mb.bm.verts.new((*oval(ts[i], prof[k][0])[0], zb)); b1 = mb.bm.verts.new((*oval(ts[i], prof[k + 1][0])[0], zb))
                    ws.append(mb.bm.faces.new((b0, b1, rr[k + 1], rr[k])))
        mb._faces(ws, m)

# ------------------------------------------------------------------ 1. track, infield, apron
mb = MB("cp66_track_cinder", C_TR)
sweep(mb, [(0.0, Z0 + 0.03), (TW, Z0 + 0.03)], 0.0, 4.0, M["cinder"], zb=Z0 - 3.0, caps=False); mb.done()
mb = MB("cp66_track_kerb", C_TR)
sweep(mb, [(-0.10, Z0 + 0.08), (0.0, Z0 + 0.08)], 0.0, 4.0, M["kerb"], zb=Z0 - 0.3, caps=False); mb.done()
mb = MB("cp66_track_lane_lines_chalk", C_TR)
for k in range(1, NL + 1):
    d = k * LW
    sweep(mb, [(d - 0.025, Z0 + 0.037), (d + 0.025, Z0 + 0.037)], 0.0, 4.0, M["chalk"])
mb.done()
# finish line across the home straight at the +x end of the +y straight (I)
mb = MB("cp66_finish_line_chalk", C_TR)
fx = CX + LS / 2 - 0.05
mb.box(fx - 0.025, fx + 0.025, CY + RB, CY + RB + TW, Z0 + 0.03, Z0 + 0.038, M["chalk"]); mb.done()
mb = MB("cp66_infield_turf", C_TR)
ring = [oval(t, -0.10)[0] for t in tsamples(0.0, 4.0)[:-1]]
mb.poly([(p.x, p.y, Z0 + 0.02) for p in ring], M["grass"])
mb.done()
mb = MB("cp66_apron_turf", C_TR)
sweep(mb, [(TW, Z0 + 0.025), (13.0, Z0 + 0.025)], 0.0, 4.0, M["grass"], zb=Z0 - 3.0, caps=False); mb.done()
# long-jump runway + pit on the apron side of the infield in front of the stand (I: generic 1960s field-event layout)
mb = MB("cp66_jump_runway_pit", C_TR)
ry = CY + RB - 4.0
mb.box(CX - 30.0, CX + 15.0, ry - 0.61, ry + 0.61, Z0 + 0.02, Z0 + 0.045, M["cinder"])
mb.box(CX + 18.0, CX + 27.0, ry - 1.4, ry + 1.4, Z0 + 0.02, Z0 + 0.05, M["sand"]); mb.done()
LOG["dims"]["jump_pit_m"] = [9.0, 2.8]

# ------------------------------------------------------------------ 2. West Stand 1964 (+y straight, sickle into both bends)
ST0, ST1 = 3.83, 5.17            # ~30.6 deg into each bend (ends short of the corner masts)
NR, TREAD, RISE = 34, 0.80, 0.38
D_FRONT = 13.0
prof = [(D_FRONT, Z0 - 0.5), (D_FRONT, Z0 + 1.2), (D_FRONT + 0.3, Z0 + 1.2)]
for k in range(NR):
    d = D_FRONT + 0.3 + k * TREAD; z = Z0 + 1.2 + k * RISE
    prof += [(d, z), (d, z + RISE), (d + TREAD, z + RISE)]
D_BACK = prof[-1][0]; Z_BACK = prof[-1][1]
prof += [(D_BACK, Z_BACK + 1.1), (D_BACK + 0.3, Z_BACK + 1.1)]
mb = MB("cp66_west_stand_terraced_concrete", C_ST)
sweep(mb, prof, ST0, ST1, M["conc"], zb=Z0 - 3.5); mb.done()
mb = MB("cp66_west_stand_benches", C_ST)
for k in range(NR):
    d = D_FRONT + 0.3 + k * TREAD + 0.22; z = Z0 + 1.2 + (k + 1) * RISE
    sweep(mb, [(d, z + 0.40), (d + 0.36, z + 0.40)], ST0, ST1, M["bench"])
mb.done()
# gangway stair strips (lighter concrete) every ~ 14 m along the stand: thin raised strips on the treads
mb = MB("cp66_west_stand_gangways", C_ST)
for tg in [ST0 + 0.04 + i * (ST1 - ST0 - 0.08) / 9 for i in range(10)]:
    for k in range(NR):
        d = D_FRONT + 0.3 + k * TREAD; z = Z0 + 1.2 + (k + 1) * RISE
        p, n = oval(tg, d + TREAD / 2); u = Vector((-n.y, n.x))
        mb.obox(p, u, n, 0.6, TREAD / 2, z, z + 0.03, M["conc_d"])
mb.done()
LOG["dims"]["west_stand"] = dict(rows=NR, tread=TREAD, rise=RISE, front_d=D_FRONT, back_d=round(D_BACK, 2), back_row_h=round(Z_BACK - Z0, 2),
                                 wrap_deg=round((ST1 - 5.0) * 180, 1),
                                 seats_est=int(sum(((LS + 2 * (ST1 - 5.0) * math.pi * (RB + D_FRONT + k * TREAD)) / 0.50) for k in range(NR))))
# cantilevered canopy over the straight (t 0..1), rear columns on the back of the stand
RC_D = D_BACK - 0.4; ROOF_BACK = Z_BACK + 4.2; ROOF_FRONT = Z0 + 14.6; ROOF_D0 = D_FRONT + 13.0
mb = MB("cp66_west_stand_canopy", C_ST)
sweep(mb, [(ROOF_D0, ROOF_FRONT), (RC_D + 1.5, ROOF_BACK)], 0.0, 1.0, M["roof"], zb=None)
sweep(mb, [(ROOF_D0, ROOF_FRONT - 0.35), (RC_D + 1.5, ROOF_BACK - 0.35)], 0.0, 1.0, M["roof"])
sweep(mb, [(ROOF_D0 - 0.05, ROOF_FRONT - 1.1), (ROOF_D0, ROOF_FRONT + 0.15)], 0.0, 1.0, M["fascia"])
mb.done()
mb = MB("cp66_west_stand_canopy_columns", C_ST)
NCOL = 11
for i in range(NCOL):
    t = i / (NCOL - 1); p, n = oval(t, RC_D); u = Vector((-n.y, n.x))
    mb.obox(p, u, n, 0.22, 0.35, Z_BACK, ROOF_BACK, M["steel"])
    # raking cantilever beam under the canopy, column head -> fascia
    a = oval(t, RC_D + 1.2)[0]; b = oval(t, ROOF_D0 + 0.5)[0]
    mb.limb((a.x, a.y, ROOF_BACK - 0.4), (b.x, b.y, ROOF_FRONT - 0.45), 0.25, 0.12, M["steel"], 6)
mb.done()
LOG["dims"]["canopy"] = dict(cantilever_m=round(RC_D - ROOF_D0, 2), length_m=round(LS, 2), front_clear_over_tread=round(ROOF_FRONT - (Z0 + 1.2 + ((ROOF_D0 - D_FRONT - 0.3) / TREAD) * RISE), 2))

# ------------------------------------------------------------------ 3. open terracing + grass banks round the rest
TE0, TE1 = 1.17, 3.83
tp = [(D_FRONT, Z0 - 0.5), (D_FRONT, Z0 + 1.0), (D_FRONT + 0.3, Z0 + 1.0)]
NT, TT, TRI = 14, 0.75, 0.25
for k in range(NT):
    d = D_FRONT + 0.3 + k * TT; z = Z0 + 1.0 + k * TRI
    tp += [(d, z), (d, z + TRI), (d + TT, z + TRI)]
DT = tp[-1][0]; ZT = tp[-1][1]
mb = MB("cp66_east_terraces_concrete", C_TE)
sweep(mb, tp, TE0, TE1, M["conc_d"], zb=Z0 - 3.5); mb.done()
mb = MB("cp66_banks_turf", C_TE)
bank = [(DT, ZT), (DT + 1.8, ZT), (DT + 6.0, ZT - 2.4), (DT + 14.0, Z0 - 4.0)]
sweep(mb, bank, TE0 - 0.02, TE1 + 0.02, M["bank"])
# behind the west stand the slope rises: a turf fill from the stand back to the terrain (stand built into the slope, R)
sweep(mb, [(D_BACK + 0.3, Z_BACK - 3.0), (D_BACK + 10.0, Z_BACK - 9.0), (D_BACK + 16.0, Z0 - 3.0)], ST0, ST1, M["bank"], zb=Z0 - 4.0)
mb.done()
mb = MB("cp66_terrace_crush_barriers", C_TE)
for k in (3, 7, 11):
    d = D_FRONT + 0.3 + k * TT + 0.1; z = Z0 + 1.0 + (k + 1) * TRI
    sweep(mb, [(d, z + 1.02), (d + 0.08, z + 1.02)], TE0, TE1, M["steel"])
    sweep(mb, [(d + 0.04, z + 1.02), (d + 0.04, z + 0.94)], TE0, TE1, M["steel"])
mb.done()
LOG["dims"]["terraces"] = dict(steps=NT, tread=TT, rise=TRI, top_h=round(ZT - Z0, 2))

# ------------------------------------------------------------------ 4. sports centre building (1.75 acres)
HX0, HX1, HY0, HY1 = 72.0, 200.0, -578.0, -523.0     # -x edge moved from the r17 x 45 to clear the +x-bend banks (end x 66.6)
gH = min(ground(x, y) for x in (HX0, HX1) for y in (HY0, HY1))
ZP0 = gH - 0.6; ZP1 = -40.5; ZG1 = -31.0
mb = MB("cp66_sports_centre_plinth", C_HA)
mb.box(HX0, HX1, HY0, HY1, ZP0, ZP1, M["conc_d"]); mb.done()
mb = MB("cp66_sports_centre_glazed_upper", C_HA)
mb.box(HX0 + 0.6, HX1 - 0.6, HY0 + 0.6, HY1 - 0.6, ZP1, ZG1, M["pane"])
mb.box(HX0 - 0.3, HX1 + 0.3, HY0 - 0.3, HY1 + 0.3, ZP1 - 0.05, ZP1 + 0.6, M["conc"])      # floor-slab edge
mb.box(HX0 - 0.3, HX1 + 0.3, HY0 - 0.3, HY1 + 0.3, ZG1 - 0.6, ZG1 + 0.2, M["conc"])      # roof-edge beam
step = 2.5
x = HX0 + 0.6
while x <= HX1 - 0.6 + 1e-6:
    for yy in (HY0 + 0.5, HY1 - 0.5): mb.box(x - 0.08, x + 0.08, yy - 0.15, yy + 0.15, ZP1 + 0.6, ZG1 - 0.6, M["mullion"])
    x += step
y = HY0 + 0.6
while y <= HY1 - 0.6 + 1e-6:
    for xx in (HX0 + 0.5, HX1 - 0.5): mb.box(xx - 0.15, xx + 0.15, y - 0.08, y + 0.08, ZP1 + 0.6, ZG1 - 0.6, M["mullion"])
    y += step
for zz in (ZP1 + 3.6,):   # transom
    mb.box(HX0 + 0.35, HX1 - 0.35, HY0 + 0.35, HY0 + 0.65, zz - 0.06, zz + 0.06, M["mullion"])
    mb.box(HX0 + 0.35, HX1 - 0.35, HY1 - 0.65, HY1 - 0.35, zz - 0.06, zz + 0.06, M["mullion"])
mb.done()
mb = MB("cp66_sports_centre_roof", C_HA)
ym = (HY0 + HY1) / 2; RISE_R = 3.0; OV = 1.8
for s_ in (-1, 1):
    ye = (HY0 - OV) if s_ < 0 else (HY1 + OV)
    mb.poly([(HX0 - OV, ye, ZG1 + 0.2), (HX1 + OV, ye, ZG1 + 0.2), (HX1 + OV, ym, ZG1 + 0.2 + RISE_R), (HX0 - OV, ym, ZG1 + 0.2 + RISE_R)][:: (1 if s_ > 0 else -1)], M["roofhall"])
for xe in (HX0 - OV, HX1 + OV):
    mb.poly([(xe, HY0 - OV, ZG1 + 0.2), (xe, ym, ZG1 + 0.2 + RISE_R), (xe, HY1 + OV, ZG1 + 0.2)], M["conc"])
mb.box(HX0 - OV, HX1 + OV, HY0 - OV, HY1 + OV, ZG1 - 0.1, ZG1 + 0.2, M["conc"])
# A-frame spine expressed at the gable ends (concrete raking legs)
for xe in (HX0 - 0.4, HX1 + 0.4):
    for s_ in (-1, 1):
        mb.limb((xe, ym + s_ * 9.0, ZP1), (xe, ym, ZG1 + RISE_R + 0.2), 0.45, 0.35, M["conc"], 6)
mb.done()
mb = MB("cp66_sports_centre_vent_tower", C_HA)
vx, vy = HX0 + 22.0, HY1 - 8.0
mb.box(vx - 4.0, vx + 4.0, vy - 4.0, vy + 4.0, ZG1, ZG1 + 15.0, M["conc"])
mb.box(vx - 4.3, vx + 4.3, vy - 4.3, vy + 4.3, ZG1 + 12.0, ZG1 + 13.6, M["conc_d"])
mb.done()
LOG["dims"]["sports_centre"] = dict(footprint=[HX1 - HX0, HY1 - HY0], area_m2=(HX1 - HX0) * (HY1 - HY0), acres=round((HX1 - HX0) * (HY1 - HY0) / 4046.86, 3),
                                    plinth_h=round(ZP1 - gH, 2), glazed_h=round(ZG1 - ZP1, 2), vent_tower_h_above_roof=15.0)

# ------------------------------------------------------------------ 5. floodlight masts, re-grounded (lights untouched)
mb = MB("cp66_floodlight_masts", C_FL)
for i in range(4):
    lo = bpy.data.objects[f"nsc_flood_{i}"]; px, py = lo.location.x, lo.location.y; top = lo.location.z + 2.0
    zb = ground(px, py) - 0.8
    mb.limb((px, py, zb), (px, py, top - 2.6), 0.55, 0.32, M["mast"], 8)
    dirv = Vector((CX - px, CY - py)).normalized(); u = Vector((-dirv.y, dirv.x))
    hc = Vector((px, py)) + dirv * 0.3                                                      # open lamp frame
    for zz in (top - 3.4, top - 1.75, top - 0.1):
        mb.obox(hc, u, dirv, 2.4, 0.08, zz - 0.08, zz + 0.08, M["steel"])
    for a_ in (-2.4, -1.2, 0.0, 1.2, 2.4):
        mb.obox(hc + u * a_, u, dirv, 0.08, 0.08, top - 3.4, top, M["steel"])
    for a_ in (-1.8, -0.6, 0.6, 1.8):
        for zz in (top - 2.6, top - 0.9):
            c = hc + dirv * 0.25 + u * a_
            mb.obox(c, u, dirv, 0.42, 0.18, zz - 0.42, zz + 0.42, M["steel"])                # lamp housing (dark)
            mb.obox(c + dirv * 0.2, u, dirv, 0.38, 0.02, zz - 0.38, zz + 0.38, M["lamp"])     # lens, faces the arena
    LOG["dims"][f"mast_{i}"] = dict(x=round(px, 1), y=round(py, 1), base=round(zb, 2), top=round(top, 2), h=round(top - zb, 2))
mb.done()

# ------------------------------------------------------------------ 6. people (1960s stand-ins, generic)
SKIN = [mat_plain(f"CP66_Skin{i}", c, 0.6) for i, c in enumerate([(0.62, 0.45, 0.35), (0.50, 0.34, 0.25), (0.30, 0.19, 0.13)])]
COAT = [mat_plain(f"CP66_Coat{i}", c, 0.85) for i, c in enumerate([(0.10, 0.11, 0.14), (0.25, 0.22, 0.18), (0.30, 0.30, 0.29), (0.05, 0.08, 0.16), (0.36, 0.28, 0.17), (0.50, 0.12, 0.10), (0.55, 0.52, 0.45)])]
TROU = [mat_plain(f"CP66_Trousers{i}", c, 0.85) for i, c in enumerate([(0.06, 0.06, 0.07), (0.16, 0.16, 0.17), (0.20, 0.17, 0.13)])]
VESTW = mat_plain("CP66_AthVestWhite", (0.80, 0.80, 0.78), 0.7); SHORTS = mat_plain("CP66_AthShortsNavy", (0.04, 0.05, 0.12), 0.7)
TRACKSUIT = [mat_plain("CP66_TracksuitNavy", (0.04, 0.06, 0.18), 0.7), mat_plain("CP66_TracksuitRed", (0.45, 0.05, 0.04), 0.7)]
HAIR = mat_plain("CP66_Hair", (0.06, 0.045, 0.03), 0.7)
mb_sp = MB("cp66_people_spectators", C_PP); mb_at = MB("cp66_people_athletes", C_PP)
def person(mb, x, y, z, fac, H=1.74, kind="spect", seated=False, stride=0.0, sk=0):
    s = H / 1.75; ca = math.atan2(fac[1], fac[0]); fw = Vector((math.cos(ca), math.sin(ca), 0)); sd = Vector((-fw.y, fw.x, 0))
    base = Vector((x, y, z))
    if kind == "spect":
        coat = COAT[R.randrange(len(COAT))]; tr = TROU[R.randrange(len(TROU))]
    elif kind == "track":
        coat = tr = TRACKSUIT[R.randrange(2)]
    else:
        coat, tr = VESTW, SHORTS
    leg = SKIN[sk] if kind == "ath" else tr
    hip = (0.92 if not seated else 0.46) * s; sh = hip + 0.52 * s; hc = sh + 0.19 * s
    for side in (-1, 1):
        f0 = base + sd * side * 0.10 * s + Vector((0, 0, hip))
        if seated:
            knee = base + sd * side * 0.10 * s + fw * 0.42 * s + Vector((0, 0, 0.46 * s))
            foot = knee + Vector((0, 0, -0.42 * s)) + fw * 0.04
            mb.limb(f0, knee, 0.08 * s, 0.07 * s, leg); mb.limb(knee, foot, 0.06 * s, 0.05 * s, leg)
        else:
            foot = base + sd * side * 0.10 * s + fw * side * stride * 0.5 + Vector((0, 0, 0.04))
            mb.limb(f0, foot, 0.08 * s, 0.05 * s, leg)
    if kind == "ath": mb.limb(base + Vector((0, 0, hip - 0.12 * s)), base + Vector((0, 0, hip + 0.06 * s)), 0.16 * s, 0.16 * s, SHORTS)
    mb.limb(base + Vector((0, 0, hip - (0.25 if (kind == "spect" and not seated) else 0.02) * s)), base + Vector((0, 0, sh)), 0.18 * s, 0.20 * s, coat)
    for side in (-1, 1):
        a0 = base + sd * side * 0.22 * s + Vector((0, 0, sh - 0.04 * s)); a1 = a0 + Vector((0, 0, -0.55 * s)) - fw * side * stride * 0.4 + (fw * 0.15 * s if seated else Vector())
        mb.limb(a0, a1, 0.055 * s, 0.045 * s, SKIN[sk] if kind == "ath" else coat)
    mb.sphere(base + Vector((0, 0, hc)), 0.11 * s, SKIN[sk]); mb.sphere(base + Vector((0, 0, hc + 0.03 * s)) - fw * 0.02, 0.105 * s, HAIR, sc=(1, 1, 0.9))
P = {"athletes": 0, "spectators": 0}
# athletes: a 400 m group on the back straight, sprinters on the home straight, a few on the bends, two in the infield
for i in range(14):
    if i < 5: t = 2.30 + i * 0.012; d = LW * (0.5 + (i % 3))
    elif i < 9: t = 0.15 + (i - 5) * 0.004; d = LW * (2.5 + (i - 5))
    elif i < 12: t = 1.35 + (i - 9) * 0.21; d = LW * 0.5
    else: t = 0.7 + (i - 12) * 0.9; d = -14.0 - (i - 12) * 6.0
    p, n = oval(t, d); u = Vector((-n.y, n.x)) if (int(t) % 4) in (0, 1) else Vector((-n.y, n.x))
    kind = "track" if i in (12, 13) else "ath"
    person(mb_at, p.x, p.y, Z0 + 0.035, (-u.x, -u.y), H=R.uniform(1.70, 1.86), kind=kind, stride=0.0 if kind == "track" else 0.55, sk=R.randrange(3)); P["athletes"] += 1
# spectators: scattered seated on the stand (front-middle rows), standing on the terraces
for i in range(70):
    k = R.choice(list(range(2, 22)))
    t = R.uniform(ST0 + 0.05, ST1 - 0.05)
    d = D_FRONT + 0.3 + k * TREAD + 0.40; z = Z0 + 1.2 + (k + 1) * RISE
    p, n = oval(t, d)
    person(mb_sp, p.x, p.y, z, (-n.x, -n.y), H=R.uniform(1.62, 1.82), seated=True, sk=R.choice((0, 0, 0, 1))); P["spectators"] += 1
for i in range(18):
    k = R.choice(list(range(1, NT)))
    t = R.uniform(TE0 + 0.1, TE1 - 0.1)
    d = D_FRONT + 0.3 + k * TT + 0.35; z = Z0 + 1.0 + (k + 1) * TRI
    p, n = oval(t, d)
    person(mb_sp, p.x, p.y, z, (-n.x, -n.y), H=R.uniform(1.62, 1.82), sk=R.choice((0, 0, 1))); P["spectators"] += 1
mb_sp.done(smooth=True); mb_at.done(smooth=True); LOG["people"] = P

# ------------------------------------------------------------------ hide the r17 block-outs (hide_render only)
for o in bpy.data.objects:
    if o.type == "MESH" and o.name.startswith("nsc_") and o.name != "nsc_access_road":
        if not o.hide_render:
            o.hide_render = True; LOG["hidden"].append((o.name, "r17 NSC block-out replaced by the 1964-67 build"))
bpy.context.scene["cp066_nsc_candidate"] = TAG
LOG["objects"] = sum(1 for o in bpy.data.objects if "cp066_nsc" in o.keys())
os.makedirs(os.path.join(os.path.dirname(HERE), "checks"), exist_ok=True)
json.dump(LOG, open(os.path.join(os.path.dirname(HERE), "checks", "cp066_nsc64_candidate.json"), "w"), indent=1)
if not A.no_save:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True, copy=True)
print("CP066_CANDIDATE_SAVED", OUT, "objects", LOG["objects"], "hidden", len(LOG["hidden"]), json.dumps(LOG["dims"]), flush=True)
