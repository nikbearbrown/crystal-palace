"""CP050 CANDIDATE (2026-11-16, no verdict): SY95 football ground on Saturday 20 April 1895 — the first FA Cup Final at
Crystal Palace (Aston Villa 1 West Bromwich Albion 0, attendance 42,560, referee John Lewis).

usage: blender -b rounds/fb02_1895.blend -P scripts/candidate_cp050_cupfinal1895.py -- --out rounds/candidates/fb02_1895_cp050cup.blend
Opens the live round (never writes it; md5 d8b263c0) and saves a copy. Cameras are NOT moved. Lights, world and
exposure are NOT touched. Hides (never deletes) the fb01/fb02 placeholders:
  * FB_Crowd_1895 — ~7,900 GN instances of 3-box 'variant' figures (the pastel block people in the bank foreground);
  * FB_Post_* / FB_Bar_* — goals stood on the 110 m lines, i.e. a 70 m long x 110 m wide pitch (110 m = 120 yd is
    wider than the 1891 maximum breadth of 100 yd, 70 m = 77 yd shorter than the 100 yd minimum length);
  * FB_Halfway — a line along the long axis (the 1891 law marks only a centre mark + 10 yd circle);
  * FB_Hero_pitch_* — 8 visitors (1851 lathe dress) standing on the pitch during the match.
Swaps the mesh data of FB_Hero_bank_* / FB_Hero_pav_* (1851 lathe crinolines / frock coats) for people_lib v3.4
1890s figures at the same positions. Adds dated collection FB95_cup_final__1895-04-20:
  * goals on the 70 m goal lines (8 yd x 8 ft, white square posts), Brodie goal nets (used at Cup Finals from 1892);
  * 1892 IFAB plan markings: 12 yd line full width, 6 yd quarter-circles from each post joined by a 6 yd line;
    4 corner flags (5 ft staffs);
  * 22 players (Aston Villa claret shirts with light-blue sleeves; West Bromwich Albion blue-and-white vertical stripes;
    white knickerbockers, dark stockings, boots), referee, 2 club linesmen with flags, 1 ball (27-28 in circumference);
  * hats seated ~4.5-6 cm down over the cranium and scalp painted as hair on copies of the people_lib meshes;
  * GN crowd of 42,532 people_lib 1890s men and women (+ 28 swapped heroes = 42,560) on the natural bank, end banks,
    behind the goal lines, along the north touchline, on the stand and pavilion floor (jittered grid ~0.55-0.62 m,
    raycast onto the actual ground meshes, facing the pitch).
Sources and grades: DEPARTURES.md D-FB-CP050-01..10.
"""
import bpy, bmesh, sys, os, math, random
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from cpl_people import person_mesh
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/fb02_1895_cp050cup.blend"
STATE = "SY95_FA_Cup_Final_1895-04-20"
R = random.Random(18950420)
YD = 0.9144; FT_ = 0.3048; INCH = 0.0254
CX, CY, CZ = -158.0, -598.0, -47.5
PW, PL = 110.0, 70.0          # along x (length, goal to goal), along y (breadth)
GX = PW / 2                    # goal lines at x = CX +- 55
sc = bpy.context.scene
ROOT = bpy.data.collections.new("FB95_cup_final__1895-04-20"); sc.collection.children.link(ROOT)
ROOT["cp_state"] = STATE
ROOT["evidence"] = ("1895 FA Cup Final 20 Apr 1895, Villa 1-0 WBA, att 42,560, ref John Lewis (Wikipedia/RSSSF); "
                    "IFAB 1891 Law 1 + 1892 Llandudno plan (12 yd line, 6 yd radius at each post); goal nets FA Cup Final 1892; "
                    "kits historicalkits.co.uk (Villa claret + light-blue sleeves 1894; WBA blue/white stripes c.1885)")
def coll(name):
    c = bpy.data.collections.new(name); ROOT.children.link(c); c["cp_state"] = STATE; return c
def mat(n, c, r=0.8, alpha=None):
    m = bpy.data.materials.get(n)
    if m: return m
    m = bpy.data.materials.new(n); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = r; m.diffuse_color = (*c, 1)
    if alpha is not None:
        b.inputs["Alpha"].default_value = alpha
        try: m.surface_render_method = 'BLENDED'
        except Exception: pass
    return m
def tag(o):
    o["cp_state"] = STATE; return o
def mesh_obj(name, col, verts, faces, m):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update(); me.materials.append(m)
    o = bpy.data.objects.new(name, me); col.objects.link(o); return tag(o)
def box(name, col, x0, x1, y0, y1, z0, z1, m):
    vs = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    fs = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return mesh_obj(name, col, vs, fs, m)
N = {"hidden": 0}
def hide(o):
    o.hide_render = True; o.hide_viewport = True; o["cp050_hidden_by"] = "candidate_cp050_cupfinal1895"; N["hidden"] += 1

# ---------------------------------------------------------------- 0. hide placeholders (never delete)
for o in list(bpy.data.objects):
    n = o.name
    if n == "FB_Crowd_1895" or n.startswith(("FB_Post_", "FB_Bar_", "FB_Hero_pitch_")) or n == "FB_Halfway":
        hide(o)
print("CP050 hidden", N["hidden"])

# ---------------------------------------------------------------- 1. goals, nets, 1892 markings, flags (D-FB-CP050-02..04)
PITCH = coll("FB95_pitch_1892_law")
M_line = bpy.data.materials.get("FB_Line") or mat("FB95_line", (0.78, 0.78, 0.72), 0.75)
M_post = mat("FB95_post_white_paint", (0.74, 0.73, 0.68), 0.55)
M_net = mat("FB95_net_cord", (0.80, 0.79, 0.74), 0.9, alpha=0.38)
M_flagstaff = mat("FB95_flagstaff", (0.55, 0.42, 0.25), 0.7)
M_flag = mat("FB95_flag_red", (0.45, 0.04, 0.03), 0.8)
GW, GH, P5 = 8 * YD, 8 * FT_, 5 * INCH      # goal 7.315 m x 2.438 m, posts <= 5 in
ND, NB = 1.8, 0.9                            # net depth at ground / at bar (I)
def strip_y(name, x, y0, y1, w=0.12):        # line running along y at x
    box(name, PITCH, x - w / 2, x + w / 2, y0, y1, CZ + 0.005, CZ + 0.025, M_line)
def arc(name, cx, cy, r, a0, a1, n=14, w=0.12):
    vs, fs = [], []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        for rr in (r - w / 2, r + w / 2): vs.append((cx + rr * math.cos(a), cy + rr * math.sin(a), CZ + 0.026))
    for i in range(n): fs.append((2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2))
    return mesh_obj(name, PITCH, vs, fs, M_line)
for s, sg in (("W", -1), ("E", 1)):
    gx = CX + sg * GX
    for py in (CY - GW / 2, CY + GW / 2):
        box(f"FB95_post_{s}_{py:.1f}", PITCH, gx - P5 / 2, gx + P5 / 2, py - P5 / 2, py + P5 / 2, CZ, CZ + GH, M_post)
    box(f"FB95_bar_{s}", PITCH, gx - P5 / 2, gx + P5 / 2, CY - GW / 2, CY + GW / 2, CZ + GH - P5, CZ + GH, M_post)
    # net: back slope from bar to ground, two sides, roof — one mesh, translucent cord
    bx, gx2 = gx + sg * NB, gx + sg * ND
    y0, y1 = CY - GW / 2, CY + GW / 2
    vs = [(gx, y0, CZ + GH), (gx, y1, CZ + GH), (bx, y1, CZ + GH), (bx, y0, CZ + GH),
          (gx2, y0, CZ), (gx2, y1, CZ), (gx, y0, CZ), (gx, y1, CZ)]
    fs = [(0, 1, 2, 3), (3, 2, 5, 4), (0, 3, 4, 6), (1, 7, 5, 2)]
    mesh_obj(f"FB95_net_{s}", PITCH, vs, fs, M_net)
    # 12 yd line, full width (1891 law / 1892 plan)
    strip_y(f"FB95_12yd_{s}", gx - sg * 12 * YD, CY - PL / 2, CY + PL / 2)
    # goal area: 6 yd quarter circles from each post, joined by a line 6 yd out (1892 plan)
    r6 = 6 * YD; lx = gx - sg * r6
    if sg < 0:
        arc(f"FB95_6yd_arc_{s}_S", gx, CY - GW / 2, r6, -math.pi / 2, 0)
        arc(f"FB95_6yd_arc_{s}_N", gx, CY + GW / 2, r6, 0, math.pi / 2)
    else:
        arc(f"FB95_6yd_arc_{s}_S", gx, CY - GW / 2, r6, math.pi, 1.5 * math.pi)
        arc(f"FB95_6yd_arc_{s}_N", gx, CY + GW / 2, r6, math.pi / 2, math.pi)
    strip_y(f"FB95_6yd_line_{s}", lx, CY - GW / 2, CY + GW / 2)
for i, (fx, fy) in enumerate([(CX - GX, CY - PL / 2), (CX - GX, CY + PL / 2), (CX + GX, CY - PL / 2), (CX + GX, CY + PL / 2)]):
    box(f"FB95_cornerstaff_{i}", PITCH, fx - 0.015, fx + 0.015, fy - 0.015, fy + 0.015, CZ, CZ + 5 * FT_, M_flagstaff)
    mesh_obj(f"FB95_cornerflag_{i}", PITCH, [(fx, fy, CZ + 1.52), (fx, fy, CZ + 1.22), (fx + 0.45, fy + 0.05, CZ + 1.37)], [(0, 1, 2)], M_flag)

# ---------------------------------------------------------------- 2. players, referee, linesmen, ball (D-FB-CP050-05..07)
PLAY = coll("FB95_players_villa_wba")
def kit_mats(team):
    w = mat("FB95_knickers_white", (0.70, 0.69, 0.64), 0.85)
    sock = mat("FB95_stockings_dark", (0.03, 0.03, 0.04), 0.9)
    if team == "AV": return mat("FB95_villa_claret", (0.20, 0.025, 0.05), 0.85), mat("FB95_villa_lightblue", (0.38, 0.58, 0.78), 0.85), w, sock
    if team == "WBA": return mat("FB95_wba_blue", (0.03, 0.05, 0.16), 0.85), mat("FB95_wba_white", (0.70, 0.69, 0.64), 0.85), w, sock
    j = mat("FB95_official_dark", (0.04, 0.04, 0.05), 0.85); return j, j, mat("FB95_official_trou", (0.06, 0.06, 0.07), 0.85), sock
M_skin = mat("FB95_skin", (0.55, 0.40, 0.32), 0.6); M_hair = mat("FB95_hair", (0.06, 0.04, 0.03), 0.8)
M_boot = mat("FB95_boot", (0.02, 0.018, 0.015), 0.5)
PCACHE = {}
def player_mesh(team, pose, seed):
    key = (team, pose, seed % 6)
    if key in PCACHE: return PCACHE[key]
    src = f"fb95_src_{team}_{pose}_{seed % 6}"
    me0 = person_mesh(src, "today_casual_m", style={'role': 'today_casual_m', 'pose': pose, 'lod': 'mid'}, seed=seed % 6 + 3)
    me = me0.copy(); me.name = f"FB95_player_{team}_{pose}_{seed % 6}"
    o = bpy.data.objects.get(src)
    if o: bpy.data.objects.remove(o, do_unlink=True)
    shirt, sleeve, knick, sock = kit_mats(team)
    me.materials.clear()
    for m in (M_skin, shirt, sleeve, knick, sock, M_boot, M_hair): me.materials.append(m)
    H = max(v.co.z for v in me.vertices)
    sh = [abs(v.co.x) for v in me.vertices if abs(v.co.z - 0.82 * H) < 0.03]; sw = max(sh) if sh else 0.2
    for p in me.polygons:
        c = p.center; z = c.z / H; ax = abs(c.x)
        if z > 0.95: i = 6
        elif z > 0.865: i = 0
        elif z > 0.53:
            if ax > sw * 0.80: i = 2 if team != "WBA" else 1
            elif team == "WBA": i = 1 if int((c.x + 0.5) / 0.055) % 2 == 0 else 2
            else: i = 1
        elif ax > sw * 0.72 and z > 0.36: i = 0 if z < 0.47 else (2 if team != "WBA" else 1)
        elif z > 0.30: i = 3
        elif z > 0.045: i = 4
        else: i = 5
        p.material_index = i
    PCACHE[key] = me; return me
BALL = Vector((CX + 21.0, CY + 7.0))
def place(name, me, x, y, look=None, jit=0.5):
    o = bpy.data.objects.new(name, me); PLAY.objects.link(o); o.location = (x, y, CZ)
    t = look if look is not None else BALL
    a = math.atan2(t[1] - y, t[0] - x) + math.pi / 2 + R.uniform(-jit, jit)
    o.rotation_euler = (0, 0, a); o["person"] = 1; return tag(o)
# Villa (2-3-5) attack east in this frame, a few seconds into an attack (I)
VILLA = [(-50, 0, "standing"), (-22, -12, "walking"), (-18, 11, "walking"), (-2, -16, "walking"), (2, 2, "walking"),
         (4, 18, "walking"), (24, -22, "walking"), (19, 7, "walking"), (28, -4, "walking"), (30, 12, "walking"), (26, 25, "walking")]
WBA = [(53, 1, "standing"), (40, -8, "walking"), (37, 9, "walking"), (27, -14, "walking"), (23, 3, "walking"),
       (29, 18, "walking"), (5, -20, "walking"), (9, -6, "walking"), (0, 6, "walking"), (12, 15, "walking"), (-6, 24, "walking")]
for i, (dx, dy, pose) in enumerate(VILLA): place(f"FB95_villa_{i:02d}", player_mesh("AV", pose, i), CX + dx, CY + dy)
for i, (dx, dy, pose) in enumerate(WBA): place(f"FB95_wba_{i:02d}", player_mesh("WBA", pose, i + 11), CX + dx, CY + dy)
place("FB95_referee_JLewis", player_mesh("REF", "walking", 1), CX + 13, CY - 3)
L1 = place("FB95_linesman_S", player_mesh("REF", "standing", 2), CX + 18, CY - PL / 2 - 1.0)
L2 = place("FB95_linesman_N", player_mesh("REF", "standing", 3), CX - 6, CY + PL / 2 + 1.0)
for L in (L1, L2):   # hand flag on a stick (club linesmen, 1891)
    x, y = L.location.x + 0.35, L.location.y
    box(L.name + "_stick", PLAY, x - 0.01, x + 0.01, y - 0.01, y + 0.01, CZ + 0.8, CZ + 1.45, M_flagstaff)
    mesh_obj(L.name + "_flag", PLAY, [(x, y, CZ + 1.45), (x, y, CZ + 1.2), (x + 0.4, y, CZ + 1.32)], [(0, 1, 2)], M_flag)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.111, segments=12, ring_count=8, location=(BALL.x, BALL.y, CZ + 0.111))
ball = bpy.context.active_object; ball.name = "FB95_ball_leather"; ball.data.materials.append(mat("FB95_ball_tan", (0.30, 0.18, 0.08), 0.6))
for c in list(ball.users_collection): c.objects.unlink(ball)
PLAY.objects.link(ball); tag(ball)
print("CP050 players", len(VILLA) + len(WBA), "officials 3")

# ---------------------------------------------------------------- 3. crowd variants (people_lib v3.4, 1890s) (D-FB-CP050-08)
VAR = coll("FB95_crowd_variants__instanced_not_rendered")
M_jackets = [mat(f"FB95_jacket_{i}", c, 0.85) for i, c in enumerate(
    [(0.035, 0.033, 0.032), (0.05, 0.04, 0.03), (0.03, 0.035, 0.05), (0.06, 0.055, 0.05), (0.045, 0.035, 0.03), (0.025, 0.025, 0.028)])]
variants = []
M_hairs = [mat(f"FB95_hair_{i}", c, 0.8) for i, c in enumerate([(0.05, 0.035, 0.025), (0.03, 0.025, 0.02), (0.10, 0.07, 0.04), (0.08, 0.075, 0.07)])]
HAT_DROP = {"1890s_gentleman": 0.06, "1850s_gentleman": 0.055, "1850s_workman": 0.045, "1890s_lady": 0.05}
def seat_hat_and_hair(o, role):
    """people_lib v3.4 perches hats on the crown (hat base ~ crown - 0.01 m) over a bald scalp. On a COPY of the variant
    mesh: drop hat verts so the hat sits down over the cranium (boater/top hat ~6 cm, cap ~4.5 cm) and paint scalp faces
    as hair. Local to this candidate; people_lib itself is not edited."""
    me = o.data.copy(); me.name = o.name + "_seated"; o.data = me
    hat = {i for i, m in enumerate(me.materials) if m and ("hat" in m.name or "bonnet" in m.name)}
    skin = [i for i, m in enumerate(me.materials) if m and "skin" in m.name]
    hv = {v for p in me.polygons if p.material_index in hat for v in p.vertices}
    # people_lib 'trim' (waistcoat/cravat, rust-pink CPL3_waist_*) shows as a jagged band above the frock/jacket shell
    # from behind; on these copies it becomes a dark waistcoat cloth (men) — ladies keep their shawl trim
    if "lady" not in role:
        for k, m in enumerate(me.materials):
            if m and m.name.startswith("CPL3_waist"): me.materials[k] = M_jackets[(k + len(o.name)) % len(M_jackets)]
    d = HAT_DROP.get(role, 0.05)
    for v in hv: me.vertices[v].co.z -= d
    if not skin: return
    sk = skin[0]; top = max(me.vertices[v].co.z for p in me.polygons if p.material_index == sk for v in p.vertices)
    me.materials.append(M_hairs[sum(map(ord, o.name)) % len(M_hairs)]); hi = len(me.materials) - 1
    for p in me.polygons:
        if p.material_index != sk: continue
        c = p.center
        if c.z > top - 0.12 and (c.y > -0.04 or c.z > top - 0.035): p.material_index = hi
        elif c.z > top - 0.19 and c.y > 0.04: p.material_index = hi   # back of the head down to the nape
        elif c.z > top - 0.31 and c.y > 0.0: p.material_index = hi    # nape / jagged collar gap read as hair + dark collar
def add_var(role, seed, recolour=False):
    nm = f"FB95_var_{len(variants):02d}_{role}"
    person_mesh(nm, role, style={'role': role, 'pose': 'standing', 'lod': 'mid', 'era': '1890s'}, seed=seed)
    o = bpy.data.objects[nm]
    if recolour:   # workman smock shell -> dark jacket (1890s working men's sack coat + cap)
        me = o.data.copy(); me.name = nm + "_jacket"; o.data = me
        for k, m in enumerate(me.materials):
            if m and m.name.startswith("CPL3_smock"): me.materials[k] = M_jackets[seed % len(M_jackets)]
    seat_hat_and_hair(o, role)
    for c in list(o.users_collection): c.objects.unlink(o)
    VAR.objects.link(o); o.location = (0, 0, 0); o.hide_render = True; o.hide_viewport = True; o["person"] = 1
    variants.append(o); return o
# mix (I): 11 cap men, 10 boater men, 2 top hats, 2 women -> 44/40/8/8 %
for s in range(11): add_var("1850s_workman", 9500 + s, recolour=True)
for s in range(10): add_var("1890s_gentleman", 9600 + s)
for s in range(2): add_var("1850s_gentleman", 9700 + s)
for s in range(2): add_var("1890s_lady", 9800 + s)
print("CP050 variants", len(variants))

# ---------------------------------------------------------------- 4. crowd points on the real ground (raycast) (D-FB-CP050-09)
dg = bpy.context.evaluated_depsgraph_get()
GROUND = {"FB_NaturalBank", "FB_EndBank_W", "FB_EndBank_E", "FB_Apron", "FB_Pavilion_floor", "FB_Stand", "FB_Turf", "FB_Pitch"}
GROUND |= {o.name for o in bpy.data.objects if o.name.startswith("FB_Stand_step_")}
def ground_z(x, y, top=60.0):
    # fb01 bank meshes have downward face normals (winding), so test |n.z|; step through figures/trees above the ground
    q = Vector((x, y, CZ + top))
    for _ in range(8):
        h, loc, nrm, idx, ob, mw = sc.ray_cast(dg, q, Vector((0, 0, -1)), distance=200)
        if not h: return None, None
        if ob.name in GROUND and abs(nrm.z) > 0.5: return loc.z, ob.name
        if ob.name.startswith(("FB_Hero", "FB95_", "FB_Var", "FB_Crowd")) or ob.get("person") or "tree" in ob.name.lower():
            q = loc + Vector((0, 0, -0.02)); continue
        return None, ob.name
    return None, None
CAM = Vector((-158.0, -680.0))
def off_pitch(x, y, m=1.5):
    return not (CX - GX - m < x < CX + GX + m and CY - PL / 2 - m < y < CY + PL / 2 + m)
def region(x0, x1, y0, y1, step, quota, hole=None, allow=None, top=60.0):
    pts = []
    nx, ny = int(abs(x1 - x0) / step), int(abs(y1 - y0) / step)
    for i in range(nx):
        for j in range(ny):
            x = min(x0, x1) + (i + 0.5 + R.uniform(-0.32, 0.32)) * step
            y = min(y0, y1) + (j + 0.5 + R.uniform(-0.32, 0.32)) * step
            if not off_pitch(x, y): continue
            if hole:
                dv = Vector((x, y)) - hole[0]
                if dv.length < 1.5: continue
                # clear only the wedge the lens looks through (+-50 deg of the view axis), so the patch reads as a gap
                # in the terrace rather than a bald circle from the pavilion side
                if dv.length < hole[1] and (len(hole) < 3 or dv.angle(hole[2]) < math.radians(50)): continue
            z, on = ground_z(x, y, top)
            if z is None or (allow and on not in allow): continue
            pts.append((x, y, z))
    R.shuffle(pts)
    return pts[:quota], len(pts)
TARGET = 42560 - 28   # 28 swapped bank/pavilion heroes stand on the bank and pavilion floor
REG = {}
REG["south_bank"] = region(CX - 79, CX + 79, CY - PL / 2 - 8.5, CY - PL / 2 - 61.5, 0.55, 24900, hole=(CAM, 9.0, Vector((0, 1))), allow={"FB_NaturalBank"})
REG["end_bank_W"] = region(CX - GX - 8.5, CX - GX - 44.5, CY - PL / 2 - 4.5, CY + PL / 2 + 4.5, 0.58, 5000, allow={"FB_EndBank_W"})
REG["end_bank_E"] = region(CX + GX + 8.5, CX + GX + 44.5, CY - PL / 2 - 4.5, CY + PL / 2 + 4.5, 0.58, 5000, allow={"FB_EndBank_E"})
REG["behind_goals"] = region(CX - GX - 7.5, CX + GX + 7.5, CY - PL / 2 + 0.5, CY + PL / 2 - 0.5, 0.55, 2232, allow={"FB_Apron", "FB_Turf", "FB_Pitch"})
REG["north_rail"] = region(CX - 54, CX + 54, CY + PL / 2 + 1.7, CY + PL / 2 + 4.6, 0.55, 1100, allow={"FB_Apron", "FB_Turf", "FB_Pitch"})
REG["stand"] = region(CX - 39.5, CX + 39.5, CY + PL / 2 + 18.3, CY + PL / 2 + 34.5, 0.55, 3700)
REG["pavilion"] = region(CX - 24.5, CX + 24.5, CY + PL / 2 + 8.0, CY + PL / 2 + 17.5, 0.62, 600, hole=(Vector((CX + 20.0, CY + PL / 2 + 10.0)), 6.0, Vector((-20.0, -45.0))), allow={"FB_Pavilion_floor"}, top=4.0)   # under the pavilion roof (CZ+6)
pts = []
for k, (p, avail) in REG.items():
    print("CP050 region", k, len(p), "of", avail); pts += [(x, y, z, k) for (x, y, z) in p]
short = TARGET - len(pts)
if short > 0:   # top up from the natural bank (the famous 'natural terrace'), never inside the camera hole
    extra, _ = region(CX - 79, CX + 79, CY - PL / 2 - 8.5, CY - PL / 2 - 61.5, 0.5, short * 3, hole=(CAM, 9.0, Vector((0, 1))), allow={"FB_NaturalBank"})
    have = {(round(x, 1), round(y, 1)) for (x, y, z, k) in pts}
    extra = [(x, y, z, "south_bank_topup") for (x, y, z) in extra if (round(x, 1), round(y, 1)) not in have][:short]
    pts += extra
pts = pts[:TARGET]
print("CP050 crowd points", len(pts), "target", TARGET)
CROWD = coll("FB95_crowd_cupfinal_42560")
me = bpy.data.meshes.new("FB95_Crowd_cloud"); me.from_pydata([(x, y, z) for (x, y, z, k) in pts], [], []); me.update()
nv = len(variants)
va = me.attributes.new("variant", 'INT', 'POINT'); va.data.foreach_set("value", [R.randrange(nv) for _ in pts])
rot = []
for (x, y, z, k) in pts:
    tx, ty = (CX + max(-GX + 5, min(GX - 5, x - CX)), CY) if k.startswith(("south", "north", "stand", "pav")) else (CX, CY)
    rot.append(math.atan2(ty - y, tx - x) + math.pi / 2 + R.uniform(-0.35, 0.35))
ra = me.attributes.new("rotz", 'FLOAT', 'POINT'); ra.data.foreach_set("value", rot)
sa = me.attributes.new("scl", 'FLOAT', 'POINT'); sa.data.foreach_set("value", [R.uniform(0.96, 1.04) for _ in pts])
ob = tag(bpy.data.objects.new("FB95_Crowd_1895_cupfinal", me)); CROWD.objects.link(ob)
ng = bpy.data.node_groups.new("FB95_Crowd_GN", 'GeometryNodeTree')
ng.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
ng.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
nd, lk = ng.nodes, ng.links
gi, go = nd.new("NodeGroupInput"), nd.new("NodeGroupOutput")
iop = nd.new("GeometryNodeInstanceOnPoints"); iop.inputs["Pick Instance"].default_value = True
ci = nd.new("GeometryNodeCollectionInfo"); ci.inputs["Separate Children"].default_value = True; ci.inputs["Reset Children"].default_value = True
ci.inputs["Collection"].default_value = VAR
nv_ = nd.new("GeometryNodeInputNamedAttribute"); nv_.data_type = 'INT'; nv_.inputs["Name"].default_value = "variant"
nr = nd.new("GeometryNodeInputNamedAttribute"); nr.data_type = 'FLOAT'; nr.inputs["Name"].default_value = "rotz"
ns = nd.new("GeometryNodeInputNamedAttribute"); ns.data_type = 'FLOAT'; ns.inputs["Name"].default_value = "scl"
cmb = nd.new("ShaderNodeCombineXYZ")
lk.new(gi.outputs[0], iop.inputs["Points"]); lk.new(ci.outputs[0], iop.inputs["Instance"])
lk.new(nv_.outputs["Attribute"], iop.inputs["Instance Index"])
lk.new(nr.outputs["Attribute"], cmb.inputs["Z"]); lk.new(cmb.outputs[0], iop.inputs["Rotation"])
lk.new(ns.outputs["Attribute"], iop.inputs["Scale"])
lk.new(iop.outputs["Instances"], go.inputs[0])
mod = ob.modifiers.new("CrowdGN", 'NODES'); mod.node_group = ng

# ---------------------------------------------------------------- 5. heroes: 1851 lathe dress -> people_lib 1890s (D-FB-CP050-10)
nsw = 0
for o in bpy.data.objects:
    if o.name.startswith(("FB_Hero_bank_", "FB_Hero_pav_")) and o.type == 'MESH':
        v = variants[R.randrange(len(variants) - 2)] if R.random() > 0.08 else variants[-1 - R.randrange(2)]
        o.data = v.data; o["cp_state"] = STATE; o["person"] = 1; nsw += 1
        # face the play (fb02 heroes faced -y: the bank ones looked into the CP050 lens, the pavilion ones away from the pitch)
        tx = CX + max(-GX + 5, min(GX - 5, o.location.x - CX))
        o.rotation_euler = (0, 0, math.atan2(CY - o.location.y, tx - o.location.x) + math.pi / 2 + R.uniform(-0.35, 0.35))
print("CP050 heroes swapped", nsw)

import json
info = json.loads(sc.get("grok_build", "{}"))
info["cp050_candidate"] = {"state": STATE, "crowd_points": len(pts), "heroes_swapped": nsw, "people_total": len(pts) + nsw,
                           "players": 22, "officials": 3, "hidden": N["hidden"], "variants": nv}
sc["grok_build"] = json.dumps(info)
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True, compress=True)
print("CP050_CANDIDATE_SAVED", OUT, info["cp050_candidate"])
