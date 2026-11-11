"""CP013_sash "Downes roof" CANDIDATE 2026-11-11 (DEPARTURES CN54; no verdict, NOT live). Hyde Park 1850, HP-BUILD roof edge.
Loads the LIVE CP013 source rounds/c04.blend (never written; md5 415e5100...) and saves rounds/candidates/c04_cp013sash.blend.
Everything new is camera-scoped to the CP013_sash shot (only_cams / hide_cams, read by render_views.py), so no other c04 camera changes.

Storyboard CP013: "Timber sash bars and flooring are visible beside iron supports; avoid an all-metal roof depiction";
50 mm detail slide across supported sash bars. Live frame = a bleached lattice of over-thick bars, no glass, no iron read.

Changes, all from Downes 1852 (text pp.12-14, 44; Plate XII Figs. 1, 3, 7-10), inside tier-1 south units x 300-420 ft, rows y -204..-132:
 1. Sash bars at Downes section: 1 in wide x 1 3/8 in deep (Plate XII Fig. 10; Muse hp-roof-furrow-bay reads 1 3/8), three strong
    bars 2 1/2 in wide per 24 ft. Bar centres on the printed Plate XII Fig. 3 chain: 5 1/4 in end margins, 10 1/2 in, 11 1/4 in either
    side of the strong bars at 4/12/20 ft (27 per slope, sums to 288 in). Live: 1 1/2 x 2 1/2 in bars (2 1/2 x 2 1/2 strong) at 10.29 in.
 2. Paxton gutter at the Fig. 10 section: single timber 5 in wide x 6 in deep, 3 in rain channel 2 1/2 in deep with a round bottom,
    bevelled top, flared cheeks (~5.7 in at top) and two condensation grooves (lip 3 1/4 in above the base). Live: 6 x 6 in box.
 3. Ridge 3 in square, sides shaped (p.13 "a piece of wood 3 in. square, with the sides shaped"). Live: 2 x 3 in box.
 4. Camber: gutters cambered up 2 1/2 in at the centre by the tie-rods (p.12); "the ridge is consequently cambered like the gutters"
    and all bars are the same length, so the whole unit is cambered.
 5. Iron under the timber: each Paxton gutter between the column lines gets its round-iron tie-rod (7/8 in, enlarged to 1 in at the
    shoe ends) and two cast-iron cross-section struts at the third points (3 in each way at top under a 4 in plate, 1 in at the foot),
    rod ~9 in below the gutter at the struts (scaled off Fig. 3 at the elevation scale), plus the end shoes. Gutters on column lines
    (over the longitudinal girders) have no rods (p.13).
 6. Glazing order (p.14): bars are fixed one at a time with each pane; ahead of the glaziers the ridge stands only on the broad bars.
    So bare "all bars, no glass" bays become: glazed -> glazing front at a wagon -> ridge on the three strong bars -> gutters only.
    Wagon rows keep the live CP016 wagons (front 2.5 ft east of the wagon); the other rows get a parked copy of the live wagon (no
    glaziers; pane crate + putty barrel from the live mesh + a bundle of prepared bars), fronts staggered 375-379.5 ft so the
    parked wagons sit just outside the right edge of both CP013_sash frames (an empty wagon in the foreground dominated the shot).
 7. Panes: 49 in x 10 in, 16 oz sheet glass, one pane per bar space per slope; two slightly different greenish tints (cylinder glass).
 8. Timber: camera-scoped copy of GT_Timber with brushed-paint streaks (p.43: bars dipped in a trough of paint, brushes took the
    surplus off). Colour itself unchanged in kind (1850 paint colour unknown, PROGRESS c02).
The live KPANE_SLIDING_* panes (ahead of the wagons on live bare bars) are hidden in this shot: under Downes' order there are no bars
for them to slide on.
blender -b rounds/c04.blend -P scripts/cand_cp013_sash_20261111.py -- [--out rounds/candidates/c04_cp013sash.blend]"""
import bpy, bmesh, math, sys, os, random
FT = 0.3048
def ft(v): return v * FT
def inch(v): return v * FT / 12.0
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/c04_cp013sash.blend"
OUT = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
SHOT = "CP013_sash"
L, W, RISE, OFF = ft(24), ft(8), ft(1.6), inch(1.3)       # build_construction.py mesh_roof (CN23)
CAMBER = inch(2.5)
NSEG = 12
rnd = random.Random(1311)

# ---------------- bar chain, Plate XII Fig. 3 ----------------
CHAIN = [5.25 + 10.5 * k for k in range(4)] + [48.0] + [59.25 + 10.5 * k for k in range(8)] + [144.0] + \
        [155.25 + 10.5 * k for k in range(8)] + [240.0] + [251.25 + 10.5 * k for k in range(4)]
assert len(CHAIN) == 27 and abs(CHAIN[-1] + 5.25 - 288) < 1e-9
STRONG = {48.0, 144.0, 240.0}
BARX = [(inch(c) - L / 2, c in STRONG) for c in CHAIN]

def camber(x): return CAMBER * (1 - (2 * x / L) ** 2)
def zglass(y): return OFF + RISE * (1 - abs(y) / (W / 2))

# ---------------- materials ----------------
def new_mat(name):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True; m.node_tree.nodes.clear(); return m, m.node_tree
base = bpy.data.materials["GT_Timber"].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value
bc = tuple(base[:3])
m, nt = new_mat("CP013_PaintedDeal"); n, l = nt.nodes, nt.links
o_ = n.new("ShaderNodeOutputMaterial"); p = n.new("ShaderNodeBsdfPrincipled"); p.inputs["Roughness"].default_value = 0.62
tc = n.new("ShaderNodeTexCoord"); mp = n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (2.0, 2.0, 40.0)
nz = n.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 30.0; nz.inputs["Detail"].default_value = 6.0
rp = n.new("ShaderNodeValToRGB"); rp.color_ramp.elements[0].position = 0.35; rp.color_ramp.elements[1].position = 0.7
rp.color_ramp.elements[0].color = (bc[0] * 0.80, bc[1] * 0.78, bc[2] * 0.74, 1); rp.color_ramp.elements[1].color = (*bc, 1)
l.new(tc.outputs["Object"], mp.inputs["Vector"]); l.new(mp.outputs[0], nz.inputs["Vector"]); l.new(nz.outputs["Fac"], rp.inputs["Fac"])
l.new(rp.outputs["Color"], p.inputs["Base Color"]); l.new(p.outputs[0], o_.inputs["Surface"])
DEAL = m; DEAL.diffuse_color = (*bc, 1)
IRON = bpy.data.materials["GT_IronPrimer_1850"]

def glass(name, tint):
    g, nt = new_mat(name); n, l = nt.nodes, nt.links
    o_ = n.new("ShaderNodeOutputMaterial"); tp = n.new("ShaderNodeBsdfTransparent"); gl = n.new("ShaderNodeBsdfGlossy")
    fr = n.new("ShaderNodeFresnel"); mx = n.new("ShaderNodeMixShader"); dif = n.new("ShaderNodeBsdfDiffuse"); mx2 = n.new("ShaderNodeMixShader")
    tp.inputs["Color"].default_value = (*tint, 1); gl.inputs["Roughness"].default_value = 0.10; fr.inputs["IOR"].default_value = 1.52
    dif.inputs["Color"].default_value = (0.55, 0.60, 0.58, 1); mx2.inputs[0].default_value = 0.06    # faint milk so 1/16 in glass reads
    l.new(tp.outputs[0], mx2.inputs[1]); l.new(dif.outputs[0], mx2.inputs[2])
    fm = n.new("ShaderNodeMath"); fm.operation = "MULTIPLY"; fm.inputs[1].default_value = 0.5   # tame the sky mirror so the bars below read
    l.new(fr.outputs[0], fm.inputs[0]); l.new(fm.outputs[0], mx.inputs[0]); l.new(mx2.outputs[0], mx.inputs[1]); l.new(gl.outputs[0], mx.inputs[2]); l.new(mx.outputs[0], o_.inputs["Surface"])
    g.diffuse_color = (*tint, 0.3); return g
GLASS_A = glass("CP013_Glass16oz_a", (0.80, 0.87, 0.84))
GLASS_B = glass("CP013_Glass16oz_b", (0.76, 0.84, 0.80))
MATS = [DEAL, IRON, GLASS_A, GLASS_B]          # 0 timber, 1 iron, 2/3 glass

# ---------------- geometry helpers ----------------
def quad_box(bm, corners, mi):
    """corners: 8 verts (bottom 4 ccw, top 4 ccw)."""
    v = [bm.verts.new(c) for c in corners]
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
        bm.faces.new([v[i] for i in f]).material_index = mi

def extrude_x(bm, prof, y0, z0, x0, x1, nseg, mi, cam=True):
    """prof: closed polygon [(dy,dz)] ccw; swept along x from x0 to x1 with camber."""
    rings = []
    for k in range(nseg + 1):
        x = x0 + (x1 - x0) * k / nseg; c = camber(x) if cam else 0.0
        rings.append([bm.verts.new((x, y0 + dy, z0 + dz + c)) for (dy, dz) in prof])
    npf = len(prof)
    for k in range(nseg):
        a, b = rings[k], rings[k + 1]
        for i in range(npf):
            j = (i + 1) % npf
            bm.faces.new([a[i], a[j], b[j], b[i]]).material_index = mi
    bm.faces.new(list(reversed(rings[0]))).material_index = mi
    bm.faces.new(rings[-1]).material_index = mi

def bar(bm, x, s, w, mi=0):
    """Sash bar at x on slope s (+1/-1): top 3/8 in above the glass plane, 1 3/8 in deep, from gutter shoulder to ridge."""
    ya, yb = s * (W / 2 - inch(2.0)), s * inch(1.5)
    c = camber(x); cs = []
    for zoff in (-inch(1.0), inch(0.375)):
        for (xx, yy) in ((x - w / 2, ya), (x + w / 2, ya), (x + w / 2, yb), (x - w / 2, yb)):
            cs.append((xx, yy, zglass(yy) + zoff + c))
    if s < 0: cs = [cs[1], cs[0], cs[3], cs[2], cs[5], cs[4], cs[7], cs[6]]
    quad_box(bm, cs, mi)

def pane(bm, xa, xb, s, mi):
    ya, yb = s * (W / 2 - inch(2.5)), s * inch(1.5)
    vs = [bm.verts.new((xx, yy, zglass(yy) + camber(xx))) for (xx, yy) in ((xa, ya), (xb, ya), (xb, yb), (xa, yb))]
    f = bm.faces.new(vs if s > 0 else list(reversed(vs))); f.material_index = mi

def cyl_between(bm, p0, p1, r, mi, nside=6):
    import mathutils
    a, b = mathutils.Vector(p0), mathutils.Vector(p1); d = (b - a); ln = d.length; d.normalize()
    up = mathutils.Vector((0, 0, 1)) if abs(d.z) < 0.9 else mathutils.Vector((1, 0, 0))
    u = d.cross(up).normalized(); v = d.cross(u).normalized()
    ra = [bm.verts.new(a + r * (math.cos(2 * math.pi * k / nside) * u + math.sin(2 * math.pi * k / nside) * v)) for k in range(nside)]
    rb = [bm.verts.new(b + r * (math.cos(2 * math.pi * k / nside) * u + math.sin(2 * math.pi * k / nside) * v)) for k in range(nside)]
    for k in range(nside):
        j = (k + 1) % nside; bm.faces.new([ra[k], ra[j], rb[j], rb[k]]).material_index = mi
    bm.faces.new(list(reversed(ra))).material_index = mi; bm.faces.new(rb).material_index = mi

def arc(cx, cz, r, a0, a1, n):
    return [(cx + r * math.cos(a0 + (a1 - a0) * k / n), cz + r * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]

# Paxton gutter, Plate XII Fig. 10 / p.12: 5 in base, 6 in deep (top at +1 in on the live datum), 3 in x 2 1/2 in channel
I = inch
GUT = [(-I(2.5), -I(5)), (I(2.5), -I(5)), (I(2.5), -I(2.6)), (I(2.2), -I(2.4)), (I(2.2), -I(1.95)), (I(2.55), -I(1.75)),
       (I(2.85), I(0.6)), (I(2.6), I(1.0)), (I(1.5), I(1.0)), (I(1.5), I(0.0))] + \
      arc(0.0, 0.0, I(1.5), 0.0, -math.pi, 8)[1:-1] + \
      [(-I(1.5), I(0.0)), (-I(1.5), I(1.0)), (-I(2.6), I(1.0)), (-I(2.85), I(0.6)), (-I(2.55), -I(1.75)), (-I(2.2), -I(1.95)),
       (-I(2.2), -I(2.4)), (-I(2.5), -I(2.6))]
# ccw check (shoelace > 0)
_a = sum(GUT[i][0] * GUT[(i + 1) % len(GUT)][1] - GUT[(i + 1) % len(GUT)][0] * GUT[i][1] for i in range(len(GUT)))
if _a < 0: GUT = list(reversed(GUT))
RIDGE = [(-I(1.5), -I(1.75)), (I(1.5), -I(1.75)), (I(1.5), I(0.4)), (I(0.55), I(1.25)), (-I(0.55), I(1.25)), (-I(1.5), I(0.4))]

def gutter_truss(bm, y0, rods):
    extrude_x(bm, GUT, y0, 0.0, -L / 2, L / 2, NSEG, 0)
    for sx in (-1, 1):                                   # cast-iron shoes at the ends (6 x 3 in base, spreads to 5 in)
        x0 = sx * (L / 2 - I(3)); c = camber(x0)
        quad_box(bm, [(x0 - I(3), y0 - I(1.5), -I(5.6) + c), (x0 + I(3), y0 - I(1.5), -I(5.6) + c), (x0 + I(3), y0 + I(1.5), -I(5.6) + c),
                      (x0 - I(3), y0 + I(1.5), -I(5.6) + c), (x0 - I(3), y0 - I(1.5), -I(4.9) + c), (x0 + I(3), y0 - I(1.5), -I(4.9) + c),
                      (x0 + I(3), y0 + I(1.5), -I(4.9) + c), (x0 - I(3), y0 + I(1.5), -I(4.9) + c)], 1)
    if not rods: return 0
    xs = (-ft(4), ft(4)); foot = {}
    for x in xs:                                         # struts: cross section 3 in at top -> 1 in at foot, 4 in plate on top
        ztop = -I(5) + camber(x); zbot = ztop - I(9)
        foot[x] = zbot
        for (ax, ay) in ((1, 0), (0, 1)):
            t = I(0.6) / 2
            wt, wb = I(1.5), I(0.5)
            if ax:
                cs = [(x - wb, y0 - t, zbot), (x + wb, y0 - t, zbot), (x + wb, y0 + t, zbot), (x - wb, y0 + t, zbot),
                      (x - wt, y0 - t, ztop), (x + wt, y0 - t, ztop), (x + wt, y0 + t, ztop), (x - wt, y0 + t, ztop)]
            else:
                cs = [(x - t, y0 - wb, zbot), (x + t, y0 - wb, zbot), (x + t, y0 + wb, zbot), (x - t, y0 + wb, zbot),
                      (x - t, y0 - wt, ztop), (x + t, y0 - wt, ztop), (x + t, y0 + wt, ztop), (x - t, y0 + wt, ztop)]
            quad_box(bm, cs, 1)
        cyl_between(bm, (x, y0, ztop - I(0.5)), (x, y0, ztop), I(2.0), 1, 10)
    pe = [(-(L / 2 - I(4)), -I(5.4) + camber(L / 2 - I(4))), (xs[0], foot[xs[0]]), (xs[1], foot[xs[1]]), (L / 2 - I(4), -I(5.4) + camber(L / 2 - I(4)))]
    for (xa, za), (xb, zb) in zip(pe, pe[1:]):
        cyl_between(bm, (xa, y0, za), (xb, y0, zb), I(7 / 16), 1, 6)
    return 1

def unit_mesh(name, kind, xf, rods):
    """kind: 'glazed' | 'front' (glazed to local xf, ridge + strong bars beyond) | 'skeleton' | 'gutter'."""
    bm = bmesh.new()
    nr = gutter_truss(bm, -W / 2, rods)
    if kind != "gutter":
        extrude_x(bm, RIDGE, 0.0, RISE, -L / 2, L / 2, NSEG, 0)
        lim = L / 2 + 1 if kind == "glazed" else (xf if kind == "front" else -L)
        for s in (-1, 1):
            placed = []
            for (x, strong) in BARX:
                if strong or x <= lim:
                    bar(bm, x, s, I(2.5) if strong else I(1.0)); placed.append((x, x <= lim))
            gl = [x for (x, ok) in placed if ok]
            edges = ([-L / 2] if lim > -L / 2 else []) + gl + ([L / 2] if kind == "glazed" else [])
            for xa, xb in zip(edges, edges[1:]):
                if xb - xa < I(12): pane(bm, xa, xb, s, 2 if rnd.random() < 0.6 else 3)
    me = bpy.data.meshes.new(name); bm.normal_update(); bm.to_mesh(me); bm.free()
    for mm in MATS: me.materials.append(mm)
    return me, nr

def add_hide(o, shot):
    cur = [s for s in (o.get("hide_cams") or "").split(",") if s]
    if shot not in cur: cur.append(shot)
    o["hide_cams"] = ",".join(cur)

# ---------------- region, fronts ----------------
coll = bpy.data.collections.new("CP013S_DOWNES_ROOF"); bpy.data.collections["CONSTRUCTION_GROK"].children.link(coll)
wag = {round(o.get("ridge_y")): o for o in bpy.data.objects if o.name.startswith("KWAGON_")}
FRONT = {}
for yc, w in wag.items(): FRONT[yc] = w.location.x / FT + 2.5
STAG = {-200: 379.0, -184: 377.5, -168: 376.0, -152: 378.5, -136: 375.0}   # parked wagons fall just outside both frames (right edge)
FRONT.update(STAG)
units = [o for o in bpy.data.objects if o.name.startswith("KROOF1_") and o.get("tier") == 1
         and 300 <= o.location.x / FT <= 420 and -204 <= o.location.y / FT <= -132]
assert len(units) == 45, len(units)
cnt = {}; nrods = 0
for o in units:
    xc, yc = round(o.location.x / FT), round(o.location.y / FT)
    live = o.get("state"); fr = FRONT[yc]
    if live == "gutter": kind, xf = "gutter", None
    elif xc + 12 <= fr: kind, xf = "glazed", None
    elif xc - 12 >= fr: kind, xf = "skeleton", None
    else: kind, xf = "front", ft(fr - xc)
    rods = (yc - 4 + 180) % 24 != 0                    # gutter on a column line rides the longitudinal girder: no tie-rod (p.13)
    me, nr = unit_mesh(f"cp013s_{kind}_{xc}_{yc}", kind, xf, rods); nrods += nr
    ob = bpy.data.objects.new(f"CP013S_ROOF_{kind}_{xc:+d}_{yc:+d}", me); coll.objects.link(ob)
    ob.matrix_world = o.matrix_world.copy()
    ob["only_cams"] = SHOT; ob["part_kind"] = "roof"; ob["state"] = kind; ob["live_state"] = live; ob["departure"] = "CN54"
    add_hide(o, SHOT); cnt[kind] = cnt.get(kind, 0) + 1
print("ROOF units", cnt, "tie-rod trusses", nrods)

# parked wagons (no glaziers) at the staggered fronts, carrying a bundle of prepared bars
src = wag[-192]
bm = bmesh.new()
for k in range(14):                     # 14 bars, 1 x 1 3/8 in, ~4 ft 3 in, two layers, along y on the deck
    lx, lz = k % 7, k // 7
    x0 = -ft(0.9) + I(1.15) * lx; z0 = ft(2.05) + I(1.4) * lz
    quad_box(bm, [(x0, -ft(2.1), z0), (x0 + I(1.0), -ft(2.1), z0), (x0 + I(1.0), ft(2.1), z0), (x0, ft(2.1), z0),
                  (x0, -ft(2.1), z0 + I(1.375)), (x0 + I(1.0), -ft(2.1), z0 + I(1.375)), (x0 + I(1.0), ft(2.1), z0 + I(1.375)), (x0, ft(2.1), z0 + I(1.375))], 0)
bme = bpy.data.meshes.new("cp013s_bar_bundle"); bm.to_mesh(bme); bm.free(); bme.materials.append(DEAL)
for yc, fr in STAG.items():
    w = bpy.data.objects.new(f"CP013S_WAGON_PARKED_{yc:+d}", src.data); coll.objects.link(w)
    w.location = (ft(fr - 2.5), ft(yc), src.location.z); w.rotation_euler = src.rotation_euler
    w["only_cams"] = SHOT; w["part_kind"] = "glazing_wagon"; w["departure"] = "CN54"
    b = bpy.data.objects.new(f"CP013S_BARS_{yc:+d}", bme); coll.objects.link(b); b.parent = w
    b["only_cams"] = SHOT; b["departure"] = "CN54"
for o in bpy.data.objects:
    if o.name.startswith("KPANE_SLIDING_"): add_hide(o, SHOT)
print("FRONTS", {k: round(v, 1) for k, v in sorted(FRONT.items())})
bpy.context.scene["CP013S_CANDIDATE"] = "CN54 2026-11-11"
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=False)
print("SAVED", OUT)
