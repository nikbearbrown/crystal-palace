# r09 exhibition dressing for HP51 (exec'd inside build_transept.py after the Muse exhibits; uses its helpers).
# Everything made here carries a "dress_kind" property so variant builders (HP-EMPTY / HP-DISMANTLE) can strip or swap it.
# Positions follow the 1851 Official Catalogue cell pattern (24 ft cells: rows A-S north->south, K = nave centre,
# column 38 = transept axis): statue lines down cells 37/39, groups on the transept axis, the British/foreign sculpture
# down the nave centre line. The figures are generic classical stand-ins (figures.py), not likenesses. DEPARTURES ST03-ST09.
import random, sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, figures as FG
importlib.reload(FG)
rnd = random.Random(SEED + 51)
STATE = arg("--state", "hp51")
DRESS = coll("DRESSING_R09", ROOT)
SUBC = {n: coll(n, DRESS) for n in ["SCULPTURE", "MACHINERY", "TEXTILES", "BANNERS", "PLANTERS", "CROWD"]}
dressed = {k: 0 for k in SUBC}
def dobj(name, me, sub, x=0.0, y=0.0, z=0.0, rz=0.0, **props):
    ob = new_obj(name, me, SUBC[sub], (ft(x), ft(y), ft(z)), rz, dict(props, dress_kind=sub.lower()))
    dressed[sub] += 1; return ob

# ---------- materials ----------
MARBLE.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.80, 0.78, 0.73, 1)
MARBLE.diffuse_color = (0.80, 0.78, 0.73, 1)
try: MARBLE.node_tree.nodes["Principled BSDF"].inputs["Subsurface Weight"].default_value = 0.08
except KeyError: pass
BRONZE = mat_principled("GT_Bronze", (0.28, 0.18, 0.10), 0.4, 0.85)
PLINTH_ST = mat_principled("GT_PlinthStone", (0.50, 0.47, 0.42), 0.7)
M_IRON = mat_principled("GT_MachIron", (0.07, 0.07, 0.075), 0.45, 0.6)
M_GREEN = mat_principled("GT_MachGreen", (0.10, 0.22, 0.14), 0.35)
M_RED = mat_principled("GT_MachRed", (0.35, 0.06, 0.04), 0.4)
M_BRASS = mat_principled("GT_Brass", (0.75, 0.55, 0.25), 0.25, 1.0)
M_STEEL = mat_principled("GT_Steel", (0.55, 0.56, 0.58), 0.25, 1.0)
M_TUB = mat_principled("GT_TubTimber", (0.28, 0.18, 0.10), 0.7)
M_LEAF = mat_principled("GT_PalmLeaf", (0.07, 0.16, 0.05), 0.6)
M_SOIL = mat_principled("GT_Soil", (0.08, 0.06, 0.04), 0.9)
def textile_mat(name, field, border, accent, scale=7.0):
    """woven-carpet look: Magic-texture field with a border band from the UVs (u,v in 0..1)"""
    m = bpy.data.materials.new(name); m.use_nodes = True; n = m.node_tree.nodes; l = m.node_tree.links
    b = n["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.95
    try: b.inputs["Sheen Weight"].default_value = 0.4
    except KeyError: pass
    tc = n.new("ShaderNodeTexCoord"); sep = n.new("ShaderNodeSeparateXYZ"); l.new(tc.outputs["UV"], sep.inputs[0])
    def absd(src):
        s = n.new("ShaderNodeMath"); s.operation = 'SUBTRACT'; s.inputs[1].default_value = 0.5; l.new(src, s.inputs[0])
        a = n.new("ShaderNodeMath"); a.operation = 'ABSOLUTE'; l.new(s.outputs[0], a.inputs[0]); return a
    au, av = absd(sep.outputs[0]), absd(sep.outputs[1])
    mx = n.new("ShaderNodeMath"); mx.operation = 'MAXIMUM'; l.new(au.outputs[0], mx.inputs[0]); l.new(av.outputs[0], mx.inputs[1])
    gt = n.new("ShaderNodeMath"); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.41; l.new(mx.outputs[0], gt.inputs[0])
    mg = n.new("ShaderNodeTexMagic"); mg.inputs["Scale"].default_value = scale; mg.turbulence_depth = 2; l.new(tc.outputs["UV"], mg.inputs["Vector"])
    ramp = n.new("ShaderNodeValToRGB"); l.new(mg.outputs["Fac"], ramp.inputs[0])
    ramp.color_ramp.elements[0].color = (*field, 1); ramp.color_ramp.elements[1].color = (*accent, 1); ramp.color_ramp.elements[1].position = 0.85
    mix = n.new("ShaderNodeMix"); mix.data_type = 'RGBA'; l.new(gt.outputs[0], mix.inputs[0])
    l.new(ramp.outputs[0], mix.inputs[6]); mix.inputs[7].default_value = (*border, 1)
    l.new(mix.outputs[2], b.inputs["Base Color"]); m.diffuse_color = (*field, 1)
    return m
TEX = [textile_mat("GT_Carpet_crimson", (0.30, 0.03, 0.03), (0.06, 0.05, 0.12), (0.55, 0.38, 0.12)),
       textile_mat("GT_Carpet_indigo", (0.04, 0.06, 0.20), (0.35, 0.05, 0.04), (0.55, 0.45, 0.25)),
       textile_mat("GT_Carpet_green", (0.05, 0.16, 0.08), (0.30, 0.20, 0.06), (0.45, 0.10, 0.08)),
       textile_mat("GT_Carpet_gold", (0.45, 0.30, 0.08), (0.12, 0.04, 0.03), (0.20, 0.10, 0.25))]
def flat(name, rgb): return mat_principled(name, rgb, 0.9)
FLAGC = {"red": flat("GT_Flag_red", (0.45, 0.03, 0.03)), "white": flat("GT_Flag_white", (0.80, 0.78, 0.72)),
         "blue": flat("GT_Flag_blue", (0.03, 0.06, 0.28)), "black": flat("GT_Flag_black", (0.02, 0.02, 0.02)),
         "yellow": flat("GT_Flag_yellow", (0.75, 0.55, 0.05)), "green": flat("GT_Flag_green", (0.03, 0.22, 0.08))}

# ---------- placement registry (feet) ----------
OCC = []     # circles (x, y, r, tag)
RECTS = []   # (x0, x1, y0, y1, tag)
def occupied(x, y, r):
    for (a, b, rr, t) in OCC:
        if math.hypot(x - a, y - b) < r + rr: return t
    for (x0, x1, y0, y1, t) in RECTS:
        if x0 - r < x < x1 + r and y0 - r < y < y1 + r: return t
    return None
OCC.append((0, 0, 24.0, "fountain"))
for (nm, ex, ey, *_r) in ELMS: OCC.append((ex, ey, 4.0, nm))
for xl in X_LINES:
    for yr in ROWS_Y + [Y_HALF]: OCC.append((xl, yr, 1.3, "column"))
for e in exhibits:
    k = e.get("part_kind"); x, y = e.location.x / FT, e.location.y / FT
    OCC.append((x, y, {"exhibit_case": 3.2, "exhibit_plinth": 2.0, "bench": 3.5}.get(k, 3.0), k))
for sx in (-1, 1):
    for sy in (-1, 1):   # stair bays (flights + landing)
        y0, y1 = sorted((sy * 58, sy * 92)); RECTS.append((sx * 96 - 13, sx * 96 + 13, y0, y1, "stair"))
RECTS.append((-14, 14, -210, -198, "south_doors"))
# cameras: walk segments are hard keep-outs; eye-level cones keep the crowd out of the lens
route_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "route", "camera_route.json")
ROUTE = json.load(open(route_path))
CAMSEG, CONES = [], []
for s in ROUTE["shots"]:
    st = s["start"]["pos_ft"]
    if abs(st[0]) > 200 or abs(st[1]) > 300 or s.get("ortho_m"): continue   # exterior / ortho
    en = s.get("end", s["start"])["pos_ft"]
    CAMSEG.append((st[:2], en[:2], st[2], s["id"]))
    for key in ("start", "end"):
        if key in s:
            p, q = s[key]["pos_ft"], s[key]["look_ft"]
            CONES.append((p, (q[0] - p[0], q[1] - p[1]), p[2], s["id"]))
def seg_dist(p, a, b):
    ax, ay = a; bx, by = b; dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)
def cam_conflict(x, y, r, z=0.0, cone_d=30.0, cone_a=15.0, seg_r=10.0):
    for (a, b, cz, cid) in CAMSEG:
        if abs(cz - z - 5) < 12 and seg_dist((x, y), a, b) < seg_r + r: return cid
    for (p, d, cz, cid) in CONES:
        if abs(cz - z - 5) > 12: continue
        vx, vy = x - p[0], y - p[1]; dist = math.hypot(vx, vy)
        if dist < 1e-6 or dist > cone_d: continue
        if math.hypot(*d) < 1e-6: continue
        ang = math.degrees(math.acos(max(-1, min(1, (vx * d[0] + vy * d[1]) / (dist * math.hypot(*d))))))
        if ang < cone_a + math.degrees(math.atan2(r, dist)): return cid
    return None
skipped = []
def try_place(x, y, r, tag, z=0.0, **kw):
    t = occupied(x, y, r) or cam_conflict(x, y, r, z, **kw)
    if t: skipped.append((tag, x, y, t)); return False
    OCC.append((x, y, r, tag)); return True

# ---------- mesh kit (one mesh, several material slots) ----------
class Kit:
    def __init__(s, mats): s.bm = bmesh.new(); s.mats = mats; s.idx = []
    def _tag(s, i, n0):
        s.bm.faces.ensure_lookup_table()
        for k in range(n0, len(s.bm.faces)): s.bm.faces[k].material_index = i
    def box(s, i, x0, x1, y0, y1, z0, z1):
        n0 = len(s.bm.faces); bm_box(s.bm, ft(x0), ft(x1), ft(y0), ft(y1), ft(z0), ft(z1)); s._tag(i, n0)
    def bar(s, i, a, b, w, t=None):
        n0 = len(s.bm.faces); bm_bar(s.bm, [ft(v) for v in a], [ft(v) for v in b], ft(w), ft(t if t else w)); s._tag(i, n0)
    def cyl(s, i, a, b, r, seg=16):
        """capped cylinder between points a and b (feet)"""
        n0 = len(s.bm.faces); A = Vector([ft(v) for v in a]); B = Vector([ft(v) for v in b]); d = B - A
        if d.length < 1e-6: return
        d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0))
        u = d.cross(up).normalized(); w = u.cross(d).normalized(); R = ft(r)
        ra = [s.bm.verts.new(A + (u * math.cos(2 * math.pi * k / seg) + w * math.sin(2 * math.pi * k / seg)) * R) for k in range(seg)]
        rb = [s.bm.verts.new(B + (u * math.cos(2 * math.pi * k / seg) + w * math.sin(2 * math.pi * k / seg)) * R) for k in range(seg)]
        for k in range(seg): s.bm.faces.new([ra[k], ra[(k + 1) % seg], rb[(k + 1) % seg], rb[k]])
        s.bm.faces.new(list(reversed(ra))); s.bm.faces.new(rb); s._tag(i, n0)
    def wheel(s, i, c, axis, r, w=0.6, rim=0.35, spokes=8, hub=None):
        """spoked wheel centred at c (feet), axle along 'x' or 'y'"""
        ax = Vector((1, 0, 0)) if axis == "x" else Vector((0, 1, 0)); C_ = Vector(c)
        u = Vector((0, 0, 1)); v = ax.cross(u)
        n = 32; pts = [C_ + (u * math.cos(2 * math.pi * k / n) + v * math.sin(2 * math.pi * k / n)) * (r - rim / 2) for k in range(n + 1)]
        for p, q in zip(pts, pts[1:]): s.bar(i, tuple(p), tuple(q), w, rim)
        for k in range(spokes):
            a = 2 * math.pi * k / spokes; s.bar(i, tuple(C_), tuple(C_ + (u * math.cos(a) + v * math.sin(a)) * (r - rim)), rim * 0.55)
        s.cyl(i, tuple(C_ - ax * w * 0.8), tuple(C_ + ax * w * 0.8), hub or r * 0.12, 12)
    def done(s, name):
        me = finish(s.bm, name, s.mats[0], s.mats[1:]); return me

# ---------- sculpture ----------
LIBS = {}
def sculpt(kind, h_m, mat):
    key = (kind, round(h_m, 2), mat.name)
    if key not in LIBS: LIBS[key] = FG.statue_mesh(kind, h_m, mat)
    return LIBS[key]
def mplinth(name, w, d, h, x, y, rz=0.0):
    """moulded pedestal: plinth block, base moulding, die, cornice, cap (feet, centred)"""
    k = Kit([PLINTH_ST]); hw, hd = w / 2, d / 2
    for (o, z0, z1) in ((0.0, 0, 0.55), (-0.2, 0.55, 0.8), (-0.45, 0.8, h - 0.75), (-0.2, h - 0.75, h - 0.45), (0.05, h - 0.45, h - 0.25), (-0.1, h - 0.25, h)):
        k.box(0, -hw - o, hw + o, -hd - o, hd + o, z0, z1)
    return dobj(name, k.done(name.lower()), "SCULPTURE", x, y, 0, rz, part_kind="statue_plinth")
def statue_on(name, kind, x, y, face_rz, h_fig=7.5, ph=4.5, pw=4.6, mat=None, cat=""):
    mat = mat or MARBLE
    mplinth(name + "_PLINTH", pw, pw, ph, x, y, face_rz)
    h_m = ft(h_fig) if kind != "seated" else ft(h_fig * 0.72)
    dobj(name + "_FIGURE", sculpt(kind, h_m, mat), "SCULPTURE", x, y, ph, face_rz, part_kind="statue", catalogue=cat)
FACE = lambda x: (math.pi / 2 if x < 0 else -math.pi / 2)   # local front is -y; turn it to face the transept axis
sc_count = 0
if STATE == "hp51":
    # transept statue lines (catalogue columns 37/39 pattern), pulled in to x = +-14 so CP017's aisle walk stays clear
    kinds = ["hero", "draped", "orator", "nude_post", "seated", "draped", "hero", "orator", "nude_post", "draped", "seated", "hero"]
    TALBOT_XY = (24, 116)
    k = 0
    for sx in (-1, 1):
        for sy in (-1, 1):
            for yy in (52, 76, 100, 124, 148, 172):
                x, y = sx * 14, sy * yy
                if (sx, sy, yy) in ((-1, -1, 148),): continue       # Duncan's Horses group stands here
                if math.hypot(x - TALBOT_XY[0], y - TALBOT_XY[1]) < 20: skipped.append(("statue", x, y, "talbot_frame")); continue
                if not try_place(x, y, 3.0, "statue", cone_d=40, cone_a=8): continue
                kind = kinds[k % len(kinds)]; k += 1
                if (sx, sy, yy) == (1, 1, 172): kind = "seated"     # D39 Prometheus Chained (Theed): seated stand-in
                statue_on(f"STATUE_T{sx:+d}{sy:+d}_{yy}", kind, x, y, FACE(x), h_fig=rnd.choice([7.0, 7.5, 8.0]), cat="cell 37/39 line")
                sc_count += 1
    # O38 Thornycroft, Queen Victoria on horseback: equestrian stand-in, pedestal along y, horse facing south (shifted to x=+8 to clear CP008)
    if try_place(8, -88, 3.0, "equestrian", seg_r=7.5, cone_d=0):
        mplinth("GROUP_EQUESTRIAN_PEDESTAL", 6.0, 14.0, 6.5, 8, -88)
        dobj("GROUP_EQUESTRIAN", FG.horse_group_mesh("SCULPT_equestrian", 3.2, MARBLE), "SCULPTURE", 8, -88, 6.5, -math.pi / 2, part_kind="statue", catalogue="O38 Thornycroft (stand-in)")
        RECTS.append((5, 11, -95, -81, "equestrian")); sc_count += 1
    # M38 Engel, Amazons and Argonauts: two-figure group facing south
    if try_place(0, -48, 5.0, "group_M38", cone_d=0):
        mplinth("GROUP_M38_PLINTH", 9.0, 5.5, 4.0, 0, -48)
        dobj("GROUP_M38_A", sculpt("hero", ft(8.0), MARBLE), "SCULPTURE", -1.8, -48, 4.0, 0.35, part_kind="statue", catalogue="M38 group (stand-in)")
        dobj("GROUP_M38_B", sculpt("draped", ft(7.4), MARBLE), "SCULPTURE", 1.9, -47.6, 4.0, -0.4, part_kind="statue")
        RECTS.append((-4.5, 4.5, -50.75, -45.25, "group_M38")); sc_count += 1
    # Q37 Lough, Duncan's Horses (bronze): rearing pair on a long pedestal facing the axis
    if try_place(-14, -150, 4.0, "group_Q37", cone_d=0):
        mplinth("GROUP_Q37_PEDESTAL", 14.0, 6.5, 5.0, -14, -150)
        hA = dobj("GROUP_Q37_HORSE_A", FG.horse_group_mesh("SCULPT_rearing", 2.6, BRONZE, rearing=True, rider=False), "SCULPTURE", -15, -151.2, 5.0, 0.0, part_kind="statue", catalogue="Q37 Lough (stand-in)")
        dobj("GROUP_Q37_HORSE_B", hA.data, "SCULPTURE", -13, -148.6, 5.0, math.pi, part_kind="statue")
        RECTS.append((-21, -7, -153.25, -146.75, "group_Q37")); sc_count += 1
    # nave centre line and J/L rows (catalogue K41, K43, J40, L40, J43; west K36/K35 pattern)
    NAVE = [("J40", 48, 24, "hero", MARBLE), ("L40", 48, -24, "draped", MARBLE), ("K41", 72, 0, "nude_post", MARBLE),
            ("K43", 120, 0, "draped", MARBLE), ("J43", 120, 24, "orator", MARBLE), ("K36", -48, 0, "draped", MARBLE),
            ("K35", -72, 0, "hero", BRONZE)]
    for (cell, x, y, kind, mat) in NAVE:
        if not try_place(x, y, 3.0, "statue_" + cell, cone_d=25, cone_a=8): continue
        rz = 0.0 if y >= 0 else math.pi     # local front -y: centre line faces south, J row faces the nave axis, L row turns round
        statue_on(f"STATUE_{cell}", kind, x, y, rz, h_fig=8.0, ph=5.0, pw=5.0, mat=mat, cat=cell + " (stand-in)")
        sc_count += 1
    if bpy.data.objects.get("STATUE_K43_FIGURE"):   # The Orphans: add two children to the K43 group
        for j, dx in enumerate((-1.3, 1.3)):
            dobj(f"STATUE_K43_CHILD{j}", sculpt("draped", ft(4.6), MARBLE), "SCULPTURE", 120 + dx, -1.2, 5.0, 0.3 * (1 - 2 * j), part_kind="statue")
    # busts on Muse's display plinths (so none stands empty); EbonisedWood recoloured in this file only
    for e in exhibits:
        if e.get("part_kind") != "exhibit_plinth": continue
        x, y = e.location.x / FT, e.location.y / FT
        dobj("BUST_" + e.name[12:], sculpt("bust", 0.82, MARBLE), "SCULPTURE", x, y, 0.9 / FT, e.rotation_euler.z, part_kind="statue")
        sc_count += 1
    if PLINTH:
        for o in PLINTH.objects:
            for sl in o.material_slots:
                if sl.material and sl.material.name.startswith("EbonisedWood"):
                    m = sl.material.copy(); m.name = "GT_PlinthScagliola_from_Muse"
                    b = m.node_tree.nodes.get("Principled BSDF")
                    if b: b.inputs["Base Color"].default_value = (0.50, 0.47, 0.42, 1)
                    m.diffuse_color = (0.50, 0.47, 0.42, 1); sl.link = 'OBJECT'; sl.material = m
print("SCULPTURE", sc_count, flush=True)

# ---------- Una and the Lion (Muse) at its catalogue cell S29, outside this model: hidden unless combined with Claude ----------
UNA = muse_prop("una-and-the-lion", lambda n: n not in ("Ground", "Backdrop", "Floor"), (0.0, 0.0, 0.0), "MUSE_Una_by_Muse")
if UNA and STATE == "hp51":
    put(UNA, "EXH_UNA_S29", -216, -192, 0.0, "statue_una"); u = exhibits[-1]
    u.hide_render = True; u["show_with_claude"] = True; u["catalogue"] = "BSC/24, cell S29 (Official Catalogue p. 844 #24)"

# ---------- machinery block-outs, east nave and east aisles (DEPARTURES MX01: 1851 machinery stood in the west half) ----------
mach_n = 0
def machine(name, x, y, rect, builder, rz=0.0):
    global mach_n
    x0, x1, y0, y1 = rect
    for (cx, cy) in ((x0, y0), (x1, y1), (x0, y1), (x1, y0), (x, y)):
        t = cam_conflict(cx, cy, 1.0, cone_d=0)
        if t: skipped.append((name, x, y, t)); return
    k = Kit([M_IRON, M_GREEN, M_BRASS, WOOD, M_RED, M_STEEL])
    k.box(3, x0 - x, x1 - x, y0 - y, y1 - y, 0, 0.75)        # timber display platform
    for (a, b) in (((x0 - x, y0 - y), (x1 - x, y0 - y)), ((x1 - x, y0 - y), (x1 - x, y1 - y)), ((x1 - x, y1 - y), (x0 - x, y1 - y)), ((x0 - x, y1 - y), (x0 - x, y0 - y))):
        k.bar(0, (a[0], a[1], 3.0), (b[0], b[1], 3.0), 0.12)  # brass-capped rope rail on posts
        for t in (0.0, 0.5): k.bar(2, (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, 0.75), (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, 3.0), 0.18)
    builder(k)
    dobj("MACH_" + name, k.done("mach_" + name.lower()), "MACHINERY", x, y, 0, rz, part_kind="machinery")
    RECTS.append((x0, x1, y0, y1, "mach_" + name)); mach_n += 1
def b_locomotive(k):   # broad-gauge express (8 ft drivers) on display rails, along x
    for yy in (-3.5, 3.5): k.box(5, -16, 16, yy - 0.15, yy + 0.15, 0.75, 1.1)
    k.box(0, -13, 13, -3.6, 3.6, 3.4, 4.6)                      # frames / footplate
    k.cyl(1, (-9, 0, 7.6), (7, 0, 7.6), 2.4, 20)                # boiler
    k.box(1, 7, 12, -2.8, 2.8, 4.6, 10.2)                       # firebox
    k.cyl(0, (-11.5, 0, 7.6), (-9, 0, 7.6), 2.6, 20)            # smokebox
    k.cyl(0, (-10.4, 0, 9.8), (-10.4, 0, 15.0), 0.75, 12)       # chimney
    k.cyl(2, (2, 0, 9.8), (2, 0, 11.6), 0.7, 12)                # brass dome
    for xx, r in ((-8, 2.25), (-1.0, 4.0), (6.5, 2.25)):
        for yy in (-3.0, 3.0): k.wheel(0, (xx, yy, 1.1 + r), "y", r, w=0.45, rim=0.3, spokes=12 if r > 3 else 8)
    k.box(3, 12.5, 15.5, -3.6, 3.6, 4.6, 7.0)                   # tender (short block)
def b_steam_engine(k):  # horizontal engine with a big flywheel, along x
    k.box(0, -8, 6, -1.6, 1.6, 0.75, 3.4)
    k.cyl(1, (-8, 0, 4.6), (-3, 0, 4.6), 1.5, 20); k.cyl(5, (-3, 0, 4.6), (2, 0, 4.6), 0.25, 8)
    k.box(0, 4, 6, -2.4, 2.4, 0.75, 5.0); k.wheel(0, (5, 3.2, 7.2), "y", 6.4, w=0.8, rim=0.6, spokes=8)
    k.cyl(2, (-1, 0, 6.0), (-1, 0, 8.4), 0.12, 6); k.wheel(2, (-1, 0, 8.4), "y", 0.7, w=0.2, rim=0.2, spokes=4)
def b_press(k):          # Bramah hydraulic press (Britannia Bridge type) along x
    for xx in (-4.5, 4.5): k.cyl(0, (xx, 0, 0.75), (xx, 0, 10), 1.6, 20)
    k.box(0, -6.5, 6.5, -2, 2, 10, 12.5); k.box(1, -6.5, 6.5, -2, 2, 0.75, 2.8)
    for (xx, yy) in ((-5.6, -1.4), (5.6, -1.4), (-5.6, 1.4), (5.6, 1.4)): k.cyl(5, (xx, yy, 2.8), (xx, yy, 14), 0.3, 8)
    k.box(4, -3, 3, -1.2, 1.2, 6, 8)
def b_beam_engine(k):    # rotative beam engine: entablature columns, rocking beam, flywheel (under the 22'11" gallery)
    for (xx, yy) in ((-2, -2.5), (-2, 2.5), (2, -2.5), (2, 2.5)): k.cyl(1, (xx, yy, 0.75), (xx, yy, 14.0), 0.45, 12)
    k.box(0, -3, 3, -3.2, 3.2, 14.0, 14.8)
    k.box(0, -8, 8, -0.35, 0.35, 15.5, 17.0); k.cyl(2, (0, -1, 16.2), (0, 1, 16.2), 0.4, 10)
    k.cyl(1, (-6.5, 0, 0.75), (-6.5, 0, 9.0), 1.6, 20); k.cyl(5, (-6.5, 0, 9), (-6.5, 0, 15.6), 0.2, 8)
    k.bar(5, (6.5, 0, 15.6), (6.5, 0, 8.0), 0.35); k.wheel(0, (6.5, 2.0, 8.0), "y", 6.8, w=0.7, rim=0.55, spokes=6)
def b_looms(k):          # a row of power looms with an overhead line shaft
    for j, xx in enumerate((-6.5, -2.2, 2.2, 6.5)):
        k.box(1, xx - 1.8, xx + 1.8, -2.4, 2.4, 0.75, 1.3)
        for (dx, dy) in ((-1.7, -2.3), (1.7, -2.3), (-1.7, 2.3), (1.7, 2.3)): k.bar(0, (xx + dx, dy, 1.3), (xx + dx, dy, 5.6), 0.25)
        k.box(0, xx - 1.8, xx + 1.8, -2.4, 2.4, 5.6, 5.9); k.box(3, xx - 1.6, xx + 1.6, -0.4, 0.4, 3.0, 4.6)
        k.box(4 if j % 2 else 1, xx - 1.5, xx + 1.5, 0.5, 2.0, 3.6, 3.75)   # cloth on the breast beam
    k.cyl(5, (-9, 0, 9.5), (9, 0, 9.5), 0.18, 8)
    for xx in (-6.5, -2.2, 2.2, 6.5): k.wheel(0, (xx, 0, 9.5), "x", 0.9, w=0.25, rim=0.2, spokes=4); k.bar(0, (xx, 0.3, 9.5), (xx, 0.3, 5.9), 0.08)
def b_marine(k):         # oscillating marine engine pair with paddle shaft
    for xx in (-3, 3): k.cyl(1, (xx, 0, 0.75), (xx, 0, 7.5), 2.2, 20); k.cyl(5, (xx, 0, 7.5), (xx, 0, 11), 0.35, 8)
    k.box(0, -6.5, 6.5, -3.6, -2.6, 0.75, 12.5); k.box(0, -6.5, 6.5, 2.6, 3.6, 0.75, 12.5)
    k.cyl(5, (0, -4.5, 12), (0, 4.5, 12), 0.5, 12); k.box(2, -0.8, 0.8, -4.5, 4.5, 12.6, 13.0)
def b_reaper(k):         # McCormick's reaper (US): wooden platform, reel, wheel, shafts
    k.box(3, -4, 4, -3, 3, 1.6, 2.0); k.wheel(4, (0, -3.5, 3.0), "y", 2.2, w=0.3, rim=0.25, spokes=10)
    k.cyl(3, (-4, 0, 4.6), (4, 0, 4.6), 0.15, 8)
    for a in range(6):
        ang = a * math.pi / 3; k.bar(3, (-4, 1.5 * math.cos(ang), 4.6 + 1.5 * math.sin(ang)), (4, 1.5 * math.cos(ang), 4.6 + 1.5 * math.sin(ang)), 0.12)
    for yy in (-0.8, 0.8): k.bar(3, (4, yy, 2.4), (11, yy, 3.0), 0.18)
def b_printing(k):       # Applegath vertical printing machine: tall drum and frames
    k.box(0, -3.5, 3.5, -3.5, 3.5, 0.75, 1.6)
    for (xx, yy) in ((-3, -3), (3, -3), (-3, 3), (3, 3)): k.cyl(1, (xx, yy, 1.6), (xx, yy, 15.0), 0.3, 10)
    k.cyl(0, (0, 0, 2.0), (0, 0, 12.5), 2.6, 24); k.box(1, -3.4, 3.4, -3.4, 3.4, 15.0, 15.6)
    for j in range(8):
        a = 2 * math.pi * j / 8; k.cyl(5, (3.2 * math.cos(a), 3.2 * math.sin(a), 3.0), (3.2 * math.cos(a), 3.2 * math.sin(a), 11.5), 0.35, 8)
if STATE == "hp51":
    machine("LOCOMOTIVE", 84, -28.5, (66, 102, -33.5, -23.5), b_locomotive)
    machine("STEAM_ENGINE", 72, -48, (62, 82, -54, -41), b_steam_engine)
    machine("HYDRAULIC_PRESS", 96, -48, (88, 104, -53, -43), b_press)
    machine("MARINE_ENGINE", 120, -48, (112, 128, -53, -43), b_marine)
    machine("BEAM_ENGINE", 72, 48, (62, 82, 42, 55), b_beam_engine)
    machine("POWER_LOOMS", 96, 48, (86, 106, 44, 52), b_looms)
    machine("REAPER", 92, 20, (86, 104, 15, 25), b_reaper)
    machine("PRINTING_MACHINE", 120, 48, (114, 126, 42, 54), b_printing)
print("MACHINERY", mach_n, flush=True)

# ---------- textiles on the transept gallery fronts, carpets on the floor ----------
def hanging(name, x, y0, y1, ztop, drop, mat, normal_x, sub="TEXTILES", folds=10):
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new(); n = folds * 2
    top, bot = [], []
    for j in range(n + 1):
        yy = y0 + (y1 - y0) * j / n; dx = 0.18 * (1 if j % 2 else -1) * (0 if j in (0, n) else 1)
        top.append(bm.verts.new((ft(x + normal_x * dx * 0.3), ft(yy), ft(ztop))))
        bot.append(bm.verts.new((ft(x + normal_x * (dx + 0.06)), ft(yy), ft(ztop - drop))))
    for j in range(n):
        f = bm.faces.new([bot[j], bot[j + 1], top[j + 1], top[j]])
        for lp, uv in zip(f.loops, ((j / n, 0), ((j + 1) / n, 0), ((j + 1) / n, 1), (j / n, 1))): lp[uvl].uv = uv
    return dobj(name, finish(bm, name.lower(), mat), sub, part_kind="textile")
def floor_carpet(name, x0, x1, y0, y1, mat):
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    vs = [bm.verts.new((ft(a), ft(b), ft(0.04))) for (a, b) in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
    f = bm.faces.new(vs)
    for lp, uv in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))): lp[uvl].uv = uv
    return dobj(name, finish(bm, name.lower(), mat), "TEXTILES", part_kind="carpet")
tex_n = 0
if STATE == "hp51":
    RTOP = GALLERY_TOP + 3.5
    for sx in (-1, 1):
        for sy in (-1, 1):
            for j, yc in enumerate((48, 72, 96, 120, 144)):
                if sx < 0 and sy > 0 and yc >= 120: continue
                if (j + (sx > 0) + (sy > 0)) % 3 == 2: continue     # leave every third bay bare
                hanging(f"TEXTILE_RAIL_{sx:+d}{sy:+d}_{yc}", sx * 35.55, sy * yc - 9, sy * yc + 9, RTOP, 10.0, TEX[(j + (sx > 0) * 2) % 4], -sx); tex_n += 1
    floor_carpet("CARPET_EQUESTRIAN", 2, 14, -97, -79, TEX[0]); floor_carpet("CARPET_M38", -7, 7, -53, -43, TEX[1])
    floor_carpet("CARPET_NAVE_RUNNER", 38, 132, -5, 5, TEX[0]); floor_carpet("CARPET_Q37", -23, -5, -155, -145, TEX[3]); tex_n += 4
print("TEXTILES", tex_n, flush=True)

# ---------- country banners from the east nave gallery fronts (above the rails) and the transept tier-2 girders ----------
FLAGS = {"FRANCE": ("v", ["blue", "white", "red"]), "BELGIUM": ("v", ["black", "yellow", "red"]), "NETHERLANDS": ("h", ["red", "white", "blue"]),
         "AUSTRIA": ("h", ["red", "white", "red"]), "RUSSIA": ("h", ["white", "blue", "red"]), "ZOLLVEREIN": ("h", ["black", "red", "yellow"]),
         "UNITED_STATES": ("h", ["red", "white"] * 3 + ["red"]), "UNITED_KINGDOM": ("h", ["blue", "red", "white", "red", "blue"]),
         "SARDINIA": ("v", ["green", "white", "red"]), "DENMARK": ("h", ["red", "white", "red"])}
def banner(name, country, x, y, along, ztop, w, drop, normal):
    """vertical banner hanging from a batten; 'along' = 'x' or 'y' is the batten direction; stripes as material slots"""
    mode, cols = FLAGS[country]; mats = [FLAGC[c] for c in cols]; uniq = list(dict.fromkeys(mats))
    bm = bmesh.new(); n = len(cols); folds = 6
    def P(s, t, off):  # s along width 0..1, t down 0..1
        a = -w / 2 + w * s; dz = ztop - drop * t; o = off + 0.25 * math.sin(s * math.pi * folds) * (0.4 + t)
        return (ft(x + a), ft(y + normal * o), ft(dz)) if along == "x" else (ft(x + normal * o), ft(y + a), ft(dz))
    for k in range(n):
        if mode == "v": s0, s1, t0, t1 = k / n, (k + 1) / n, 0.0, 1.0
        else: s0, s1, t0, t1 = 0.0, 1.0, k / n, (k + 1) / n
        ss = [s0 + (s1 - s0) * j / 12 for j in range(13)] if mode == "h" else [s0 + (s1 - s0) * j / 4 for j in range(5)]
        n0 = len(bm.faces)
        for sa, sb in zip(ss, ss[1:]):
            bm.faces.new([bm.verts.new(P(sa, t1, 0)), bm.verts.new(P(sb, t1, 0)), bm.verts.new(P(sb, t0, 0)), bm.verts.new(P(sa, t0, 0))])
        bm.faces.ensure_lookup_table()
        for f in range(n0, len(bm.faces)): bm.faces[f].material_index = uniq.index(mats[k])
    n0 = len(bm.faces)
    a0, a1 = P(0, 0, 0), P(1, 0, 0)
    bm_bar(bm, (a0[0], a0[1], a0[2] + ft(0.2)), (a1[0], a1[1], a1[2] + ft(0.2)), inch(3), inch(3))
    bm.faces.ensure_lookup_table()
    for f in range(n0, len(bm.faces)): bm.faces[f].material_index = len(uniq)
    me = finish(bm, name.lower(), uniq[0], uniq[1:] + [WOODDARK])
    return dobj(name, me, "BANNERS", part_kind="banner", country=country, placeholder=True)
ban_n = 0
if STATE == "hp51":
    east = ["FRANCE", "BELGIUM", "NETHERLANDS", "AUSTRIA", "ZOLLVEREIN", "RUSSIA"]
    for j, xc in enumerate((72, 96, 120)):
        banner(f"BANNER_NAVE_N_{xc}", east[j], xc, 35.4, "x", 40.0, 9.0, 12.5, -1); banner(f"BANNER_NAVE_S_{xc}", east[j + 3], xc, -35.4, "x", 40.0, 9.0, 12.5, 1); ban_n += 2
    for sy in (-1, 1):
        for j, yc in enumerate((72, 120)):
            for sx in (-1, 1):
                c = ["UNITED_KINGDOM", "UNITED_STATES", "SARDINIA", "DENMARK"][(j * 2 + (sx > 0)) % 4]
                banner(f"BANNER_TR_{sx:+d}{sy:+d}_{yc}", c, sx * 35.4, sy * yc, "y", 41.0, 8.0, 11.5, -sx); ban_n += 1
print("BANNERS", ban_n, flush=True)

# ---------- planters (timber tubs with palms or clipped shrubs), the Talbot urn ----------
M_LEAF2 = mat_principled("GT_LeafLight", (0.12, 0.22, 0.06), 0.55)
M_ORANGE = mat_principled("GT_OrangeFruit", (0.70, 0.30, 0.03), 0.5)
def palm_mesh(name, h):
    """r10 PL02: arching pinnate fronds (rachis + paired leaflets that hang from it) on a tapered trunk; was 11 flat paddles"""
    k = Kit([M_TUB, M_LEAF, M_SOIL, M_IRON, M_LEAF2])
    k.cyl(0, (0, 0, 0), (0, 0, 2.2), 1.6, 8); k.cyl(3, (0, 0, 0.3), (0, 0, 0.5), 1.65, 8); k.cyl(3, (0, 0, 1.8), (0, 0, 2.0), 1.65, 8)
    k.cyl(2, (0, 0, 2.15), (0, 0, 2.25), 1.45, 8)
    k.cyl(0, (0, 0, 2.2), (0, 0, h * 0.6), 0.26, 8); k.cyl(0, (0, 0, h * 0.6), (0, 0, h), 0.2, 8)
    r2 = random.Random(len(name) * 7)
    for j in range(16):
        a = 2 * math.pi * j / 16 + r2.uniform(-0.15, 0.15); L = r2.uniform(4.5, 6.5)
        up = r2.uniform(0.6, 2.2) if j % 3 else r2.uniform(2.4, 3.4)          # every third frond younger and more upright
        ca, sa = math.cos(a), math.sin(a); mat = 1 if j % 2 else 4
        pts = []
        for t in [i / 8 for i in range(9)]:                                    # parabolic arch, droops at the tip
            pts.append((L * t * ca, L * t * sa, h + up * 2 * t - (up + 1.6) * t * t))
        for p, q in zip(pts, pts[1:]): k.bar(mat, p, q, 0.08)
        for i in range(1, 8):
            p = pts[i]; t = i / 8; ln = 1.5 * math.sin(math.pi * (0.15 + 0.85 * t))
            for sd in (-1, 1):
                ex, ey = -sa * sd, ca * sd
                q = (p[0] + ex * ln + ca * 0.25, p[1] + ey * ln + sa * 0.25, p[2] - 0.45 * ln)
                k.bar(mat, p, q, 0.22, 0.03)
    return k.done(name)
def shrub_mesh(name):
    """r10 PL03: clipped orange / bay tree in a Versailles tub: clear stem and a lumpy crown of ~420 leaf cards with a little
    fruit, in place of the r09 smooth metaball 'green ball'"""
    k = Kit([M_TUB, M_LEAF, M_SOIL, M_IRON, M_LEAF2, M_ORANGE])
    k.box(0, -1.4, 1.4, -1.4, 1.4, 0, 2.2); k.box(2, -1.3, 1.3, -1.3, 1.3, 2.2, 2.3)
    for cx in (-1.42, 1.42):
        for cy in (-1.42, 1.42): k.box(3, cx - 0.1, cx + 0.1, cy - 0.1, cy + 0.1, 0, 2.5)
    k.cyl(0, (0, 0, 2.2), (0, 0, 4.6), 0.14, 6)
    r2 = random.Random(len(name) * 13)
    lobes = [(0, 0, 6.1, 1.5)] + [(1.0 * math.cos(t), 1.0 * math.sin(t), 5.7 + r2.uniform(-0.3, 0.6), 1.0) for t in (0.3, 1.9, 3.4, 4.9)]
    for n in range(420):
        cx, cy, cz, R = lobes[n % len(lobes)]
        while True:
            v = Vector((r2.uniform(-1, 1), r2.uniform(-1, 1), r2.uniform(-1, 1)))
            if 0.55 < v.length <= 1: break
        c = Vector((cx, cy, cz)) + v * R; d = Vector((r2.uniform(-1, 1), r2.uniform(-1, 1), r2.uniform(-0.6, 0.6))).normalized() * 0.28
        k.bar(1 if n % 3 else 4, tuple(c - d), tuple(c + d), 0.24, 0.02)
    for n in range(16):
        cx, cy, cz, R = lobes[n % len(lobes)]; v = Vector((r2.uniform(-1, 1), r2.uniform(-1, 1), r2.uniform(-0.8, 0.5))).normalized() * R * 0.97
        c = Vector((cx, cy, cz)) + v; k.cyl(5, tuple(c - Vector((0, 0, 0.1))), tuple(c + Vector((0, 0, 0.1))), 0.11, 6)
    return k.done(name)
pl_n = 0
if STATE in ("hp51",):
    PALM = palm_mesh("planter_palm", 7.5); SHRUB = shrub_mesh("planter_shrub")
    spots = [(28 * math.cos(math.radians(a)), 28 * math.sin(math.radians(a)), "palm") for a in (45, 135, 225, 315)]
    for sy in (-1, 1):
        for sx in (-1, 1):
            for yy in (64, 88, 136, 160): spots.append((sx * 14, sy * yy, "shrub"))
    spots += [(31, 80, "palm"), (-31, 30, "palm"), (31, -30, "palm")]
    for (x, y, kind) in spots:
        if not try_place(x, y, 2.2, "planter", cone_d=45, cone_a=12): continue
        if kind == "palm": dobj(f"PLANTER_{x:+.0f}_{y:+.0f}", PALM, "PLANTERS", x, y, 0, rnd.uniform(0, 6.28), part_kind="planter")
        else:
            dobj(f"PLANTER_{x:+.0f}_{y:+.0f}", SHRUB, "PLANTERS", x, y, 0, rnd.choice((0, 1.5708, 3.1416, 4.7124)), part_kind="planter")
        pl_n += 1
    # Talbot foreground: a garden urn on a pedestal by the camera's left (DEPARTURES C07)
    if try_place(30, 92, 2.5, "talbot_urn", cone_d=0):
        mplinth("URN_TALBOT_PEDESTAL", 2.8, 2.8, 3.2, 30, 92)
        dobj("URN_TALBOT", lathe([(0.0, 3.2), (0.9, 3.2), (0.5, 3.6), (0.45, 4.0), (1.1, 4.4), (1.5, 5.4), (1.7, 6.0), (1.4, 6.1), (1.3, 5.9), (0.0, 5.9)], "urn_talbot", STONE, 32, 30, 92), "PLANTERS", part_kind="urn")
        pl_n += 1
print("PLANTERS", pl_n, flush=True)

# ---------- crowd stand-ins (HP51 only): shared meshes, period dress, grouped ----------
crowd_n = gal_n = 0
if STATE == "hp51":
    SKIN = [mat_principled("GT_Skin_a", (0.72, 0.53, 0.42), 0.6), mat_principled("GT_Skin_b", (0.60, 0.43, 0.33), 0.6)]
    C_ = lambda n, c: mat_principled("GT_Dress_" + n, c, 0.85)
    coats = [C_("coat_black", (0.025, 0.025, 0.03)), C_("coat_brown", (0.10, 0.06, 0.04)), C_("coat_navy", (0.03, 0.04, 0.09)),
             C_("coat_green", (0.04, 0.07, 0.04)), C_("coat_grey", (0.20, 0.19, 0.18))]
    trous = [C_("trou_grey", (0.25, 0.24, 0.22)), C_("trou_fawn", (0.42, 0.36, 0.26)), C_("trou_black", (0.03, 0.03, 0.03))]
    skirts = [C_("skirt_crimson", (0.32, 0.05, 0.06)), C_("skirt_plum", (0.20, 0.07, 0.17)), C_("skirt_green", (0.08, 0.18, 0.10)),
              C_("skirt_blue", (0.18, 0.22, 0.32)), C_("skirt_tan", (0.45, 0.36, 0.24)), C_("skirt_black", (0.04, 0.035, 0.04)),
              C_("skirt_lilac", (0.42, 0.35, 0.48)), C_("skirt_white", (0.70, 0.68, 0.62))]
    bods = [C_("bod_black", (0.03, 0.03, 0.035)), C_("bod_brown", (0.15, 0.09, 0.06)), C_("bod_shawl", (0.55, 0.45, 0.30))]
    hats = [C_("hat_black", (0.02, 0.02, 0.02)), C_("bonnet_straw", (0.65, 0.55, 0.35)), C_("bonnet_cream", (0.80, 0.76, 0.66)), C_("hat_grey", (0.30, 0.28, 0.26))]
    # r10 F04: 34 variants (was 17): frock / short coats, top / low / cap hats, cravats, canes, shawls, crinoline widths,
    # boys, and a few soldiers (red coat, white belts, shako) of the Guards on duty in the building
    trims = [C_("trim_white", (0.75, 0.74, 0.70)), C_("shawl_paisley", (0.45, 0.18, 0.10)), C_("shawl_grey", (0.38, 0.36, 0.33)),
             C_("shawl_tartan", (0.12, 0.20, 0.14)), C_("shawl_cream", (0.68, 0.62, 0.50))]
    redcoat = C_("coat_scarlet", (0.42, 0.04, 0.035))
    PEOPLE = []; WEIGHTS = []
    HATS_M = ["top", "top", "top", "low", "cap", "top", "low", "top", "top", "cap", "top", "low", "top", "top"]
    for j in range(14):
        st = {"hat": HATS_M[j], "frock": j % 3 != 2, "cravat": j % 2 == 0, "cane": j in (1, 6, 11)}
        PEOPLE.append(("man", FG.person_mesh(f"PERSON_man_{j}", "man", [coats[j % 5], trous[(j * 2) % 3], SKIN[j % 2],
                       hats[3 if st["hat"] == "low" and j % 2 else 0], trims[0]], style=st))); WEIGHTS.append(3)
    for j in range(12):
        st = {"skirt_w": (0.85, 1.0, 1.12, 0.92, 1.05, 1.18)[j % 6], "shawl": j % 3 == 1}
        PEOPLE.append(("woman", FG.person_mesh(f"PERSON_woman_{j}", "woman", [skirts[j % 8], bods[(j + j // 8) % 3], SKIN[j % 2],
                       hats[1 + j % 2], trims[1 + j % 4]], style=st))); WEIGHTS.append(3)
    for j in range(4):
        PEOPLE.append(("girl", FG.person_mesh(f"PERSON_girl_{j}", "girl", [skirts[(7, 3, 6, 4)[j]], bods[2 - j % 2], SKIN[j % 2], hats[2], trims[4]],
                       style={"shawl": j == 2}))); WEIGHTS.append(1.5)
    for j in range(2):
        PEOPLE.append(("boy", FG.person_mesh(f"PERSON_boy_{j}", "boy", [coats[(1, 2)[j]], trous[j], SKIN[0], hats[0], trims[0]]))); WEIGHTS.append(1.5)
    for j in range(2):
        PEOPLE.append(("soldier", FG.person_mesh(f"PERSON_soldier_{j}", "man", [redcoat, trous[2], SKIN[j], hats[0], trims[0]],
                       style={"hat": "shako", "belt": True}))); WEIGHTS.append(0.35)
    def regions_floor():
        return [((-33, 33, 26, 200), 3.0), ((-33, 33, -200, -26), 3.0), ((-34, 34, -34, 34), 1.0),
                ((37, 59, -200, 200), 1.2), ((-59, -37, -200, 200), 1.2), ((37, 132, -34, 34), 2.6), ((61, 131, 37, 59), 0.8), ((61, 131, -59, -37), 0.8)]
    def spawn(region_list, total, z_ft, tag, rlim, seg_r=8.0, cone_d=30.0, cone_a=15.0, face=None):
        n = 0; tries = 0; W = sum(w for _, w in region_list)
        while n < total and tries < total * 60:
            tries += 1
            r = rnd.uniform(0, W); acc = 0
            for (box, w) in region_list:
                acc += w
                if r <= acc: break
            gx, gy = rnd.uniform(box[0], box[1]), rnd.uniform(box[2], box[3])
            size = rnd.choice([1, 1, 2, 2, 2, 3, 3, 4])
            for m in range(size):
                x, y = gx + rnd.uniform(-2.2, 2.2) * (m > 0), gy + rnd.uniform(-2.2, 2.2) * (m > 0)
                if not (box[0] <= x <= box[1] and box[2] <= y <= box[3]): continue
                if rlim and not rlim(x, y): continue
                if occupied(x, y, 1.1) or cam_conflict(x, y, 1.0, z_ft, cone_d=cone_d, cone_a=cone_a, seg_r=seg_r): continue
                kind, me = rnd.choices(PEOPLE, WEIGHTS)[0]
                rz = face(x, y) if face else math.atan2(gy - y, gx - x) + math.pi / 2 if m else rnd.uniform(0, 6.283)
                ob = dobj(f"CROWD_{tag}_{n:03d}", me, "CROWD", x, y, z_ft, rz + rnd.uniform(-0.4, 0.4), part_kind="figure", person=kind)
                k_ = rnd.uniform(0.93, 1.06); ob.scale = (k_ * rnd.uniform(0.95, 1.05), k_, k_ * rnd.uniform(0.97, 1.04))   # r10 F05 build variation
                OCC.append((x, y, 0.9, "person")); n += 1
                if n >= total: break
        return n
    in_ring = lambda x, y: math.hypot(x, y) > 25 if abs(y) < 36 else True
    crowd_n = spawn(regions_floor(), 540, 0.0, "F", in_ring)   # r10 F06: denser (was 260)
    # galleries: visitors along the gallery fronts looking into the transept and nave
    GT = GALLERY_TOP
    face_tr = lambda x, y: (-math.pi / 2 if x > 0 else math.pi / 2)      # look toward the transept axis
    gal_n = spawn([((37.3, 40.0, 40, 178), 1), ((-40.0, -37.3, 40, 178), 1), ((37.3, 40.0, -152, -40), 1), ((-40.0, -37.3, -152, -40), 1)],
                  110, GT, "G", None, seg_r=22, cone_d=40, cone_a=20, face=face_tr)   # r11: denser galleries (was 76)
    face_nv = lambda x, y: (0.0 if y > 0 else math.pi)
    gal_n += spawn([((62, 130, 37.3, 40.0), 1), ((62, 130, -40.0, -37.3), 1)], 40, GT, "GN", None, seg_r=22, cone_d=40, cone_a=20, face=face_nv)
    gal_n += spawn([((-34, 34, 180.5, 183), 1), ((-34, 34, -159.5, -157), 1)], 30, GT, "GX", None, seg_r=22, cone_d=60, cone_a=25,
                   face=lambda x, y: (0.0 if y > 0 else math.pi))
print("CROWD floor", crowd_n, "gallery", gal_n, flush=True)
scene["grok_dressing"] = json.dumps({"state": STATE, "counts": dressed, "skipped": [list(map(str, s)) for s in skipped[:200]], "skipped_n": len(skipped)})
print("DRESSING", dressed, "skipped", len(skipped), flush=True)
