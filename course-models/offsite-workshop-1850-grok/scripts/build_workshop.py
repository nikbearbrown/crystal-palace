"""O-WORKSHOP (CP011), autumn 1850: a Fox, Henderson / Chance Brothers style composite workshop study (DEPARTURES W01).
Machine shop (steam engine, line shafting, Paxton's sash-bar and gutter machines), a cylinder-glass house (furnace,
blowing stage over swing pits, cylinders on racks, flattening kiln) and a railway siding with Hyde Park columns and a
24 ft girder on a pair of wagons. Units: metres in Blender, written in feet.
blender -b -P build_workshop.py -- --out ../rounds/w01.blend"""
import bpy, bmesh, math, sys, os, json, random
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
OUT = arg("--out", "../rounds/w01.blend"); HERE = os.path.dirname(os.path.abspath(__file__))
FT = 0.3048; SEED = 1850; R = random.Random(SEED)
def ft(f): return f * FT
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
scene = bpy.context.scene; ROOT = scene.collection
import importlib.util
spec = importlib.util.spec_from_file_location("figures", os.path.join(HERE, "figures.py")); FG = importlib.util.module_from_spec(spec); spec.loader.exec_module(FG)
def coll(n, parent=ROOT):
    c = bpy.data.collections.new(n); parent.children.link(c); return c
CO = {k: coll(k) for k in ("SHED", "SHOP", "GLASSHOUSE", "SIDING", "FIGURES", "CAMERAS", "GROUND")}
def mat(n, c, r=0.7, m=0.0, emit=None):
    M = bpy.data.materials.new("WS_" + n); M.use_nodes = True; b = M.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = r; b.inputs["Metallic"].default_value = m
    if emit:
        b.inputs["Emission Color"].default_value = (*emit[0], 1); b.inputs["Emission Strength"].default_value = emit[1]
    M.diffuse_color = (*c, 1); return M
def mat_glass(n, tint, rough=0.05):
    M = bpy.data.materials.new("WS_" + n); M.use_nodes = True; nt = M.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*tint, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Transmission Weight"].default_value = 1.0; b.inputs["IOR"].default_value = 1.5
    M.diffuse_color = (*tint, 0.4); return M
def mat_rooflight():
    M = bpy.data.materials.new("WS_RoofLight"); M.use_nodes = True; nt = M.node_tree; n = nt.nodes; l = nt.links
    o = n["Material Output"]; [n.remove(x) for x in list(n) if x != o]
    tr = n.new("ShaderNodeBsdfTransparent"); tr.inputs[0].default_value = (0.78, 0.82, 0.80, 1)
    df = n.new("ShaderNodeBsdfDiffuse"); df.inputs[0].default_value = (0.7, 0.72, 0.7, 1)
    mx = n.new("ShaderNodeMixShader"); mx.inputs[0].default_value = 0.12
    l.new(tr.outputs[0], mx.inputs[1]); l.new(df.outputs[0], mx.inputs[2]); l.new(mx.outputs[0], o.inputs[0]); return M
BRICK = mat("brick", (0.36, 0.17, 0.11), 0.9); BRICK_SOOT = mat("brick_soot", (0.13, 0.08, 0.06), 0.95)
LIME = mat("limewash", (0.62, 0.58, 0.50), 0.95); SLATE = mat("slate", (0.13, 0.14, 0.16), 0.6)
TIMB = mat("timber", (0.42, 0.31, 0.20), 0.8); TIMB_NEW = mat("deal_new", (0.70, 0.57, 0.40), 0.75)
IRON = mat("iron", (0.07, 0.07, 0.075), 0.45, 0.7); CAST = mat("cast_iron_primed", (0.20, 0.13, 0.10), 0.7, 0.2)
BRASS = mat("brass", (0.70, 0.52, 0.22), 0.3, 1.0); EARTH = mat("earth_floor", (0.20, 0.16, 0.12), 0.95)
GRAVEL = mat("yard", (0.33, 0.30, 0.26), 0.95); LEATHER = mat("belt", (0.22, 0.12, 0.06), 0.6)
GLOW = mat("furnace_glow", (1.0, 0.5, 0.15), 0.5, 0, ((1.0, 0.42, 0.10), 40.0)); EMBER = mat("kiln_glow", (0.9, 0.35, 0.1), 0.5, 0, ((1.0, 0.32, 0.08), 12.0))
GLASS = mat_glass("cylinder_glass", (0.80, 0.90, 0.84)); HOT = mat("hot_glass", (1.0, 0.55, 0.2), 0.3, 0, ((1.0, 0.45, 0.12), 6.0))
RL = mat_rooflight(); GLASS_PANE = mat_glass("sheet_glass", (0.72, 0.82, 0.78), rough=0.04)  # w02: greener sheet so panes read through
SKIN = [mat("skin_a", (0.72, 0.53, 0.42), 0.6), mat("skin_b", (0.60, 0.43, 0.33), 0.6)]
WK = [mat("fustian", (0.30, 0.24, 0.16), 0.9), mat("cord", (0.36, 0.30, 0.20), 0.9), mat("moleskin", (0.33, 0.31, 0.27), 0.9),
      mat("shirt", (0.70, 0.68, 0.62), 0.9), mat("jacket_blue", (0.08, 0.10, 0.18), 0.9)]
TROU = [mat("trou_dk", (0.10, 0.09, 0.08), 0.9), mat("trou_fawn", (0.38, 0.32, 0.22), 0.9)]
CAP = mat("cap", (0.06, 0.06, 0.06), 0.9); APRON = mat("leather_apron", (0.28, 0.17, 0.10), 0.7)
class Kit:
    def __init__(s, mats): s.bm = bmesh.new(); s.mats = mats
    def _t(s, i, n0):
        s.bm.faces.ensure_lookup_table()
        for k in range(n0, len(s.bm.faces)): s.bm.faces[k].material_index = i
    def box(s, i, x0, x1, y0, y1, z0, z1):
        n0 = len(s.bm.faces); vs = [s.bm.verts.new((ft(a), ft(b), ft(c))) for (a, b, c) in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]]
        for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]: s.bm.faces.new([vs[k] for k in f])
        s._t(i, n0)
    def bar(s, i, a, b, w, t=None):
        t = t or w; A = Vector([ft(v) for v in a]); B = Vector([ft(v) for v in b]); d = B - A
        if d.length < 1e-6: return
        d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0)); sd = d.cross(up).normalized(); u = sd.cross(d).normalized()
        n0 = len(s.bm.faces); pts = [s.bm.verts.new(p + sd * (ii * ft(w) / 2) + u * (jj * ft(t) / 2)) for p in (A, B) for (ii, jj) in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        for f in [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]: s.bm.faces.new([pts[k] for k in f])
        s._t(i, n0)
    def cyl(s, i, a, b, r, seg=16, cap=True, r2=None):
        A = Vector([ft(v) for v in a]); B = Vector([ft(v) for v in b]); d = B - A
        if d.length < 1e-6: return
        d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0)); u = d.cross(up).normalized(); w = u.cross(d).normalized()
        n0 = len(s.bm.faces); r2 = r if r2 is None else r2
        ra = [s.bm.verts.new(A + (u * math.cos(2 * math.pi * k / seg) + w * math.sin(2 * math.pi * k / seg)) * ft(r)) for k in range(seg)]
        rb = [s.bm.verts.new(B + (u * math.cos(2 * math.pi * k / seg) + w * math.sin(2 * math.pi * k / seg)) * ft(r2)) for k in range(seg)]
        for k in range(seg): s.bm.faces.new([ra[k], ra[(k + 1) % seg], rb[(k + 1) % seg], rb[k]])
        if cap: s.bm.faces.new(list(reversed(ra))); s.bm.faces.new(rb)
        s._t(i, n0)
    def wheel(s, i, c, axis, r, w=0.5, rim=0.3, spokes=8):
        ax = Vector((1, 0, 0)) if axis == "x" else Vector((0, 1, 0)); C_ = Vector(c); u = Vector((0, 0, 1)); v = ax.cross(u)
        n = 28; pts = [C_ + (u * math.cos(2 * math.pi * k / n) + v * math.sin(2 * math.pi * k / n)) * (r - rim / 2) for k in range(n + 1)]
        for p, q in zip(pts, pts[1:]): s.bar(i, tuple(p), tuple(q), w, rim)
        for k in range(spokes):
            a = 2 * math.pi * k / spokes; s.bar(i, tuple(C_), tuple(C_ + (u * math.cos(a) + v * math.sin(a)) * (r - rim)), rim * 0.55)
        s.cyl(i, tuple(C_ - ax * w), tuple(C_ + ax * w), r * 0.14, 12)
    def done(s, name, coll_, x=0, y=0, z=0, rz=0, **props):
        me = bpy.data.meshes.new(name); s.bm.normal_update(); s.bm.to_mesh(me); s.bm.free()
        for m in s.mats: me.materials.append(m)
        ob = bpy.data.objects.new(name, me); ob.location = (ft(x), ft(y), ft(z)); ob.rotation_euler = (0, 0, rz); coll_.objects.link(ob)
        for k, v in props.items(): ob[k] = v
        return ob
INFO = {}
# ---------------- shed: 120 x 48 ft brick, timber king-post roof with a glazed ridge light (W02) ----------------
X0, X1, Y0, Y1, EAVE, RIDGE = -60.0, 60.0, -24.0, 24.0, 18.0, 31.0
k = Kit([BRICK, LIME, TIMB, SLATE, BRICK_SOOT])
def wall_x(y, xs, openings, t=1.5, inner=1):
    """long wall at y with openings [(x0,x1,z0,z1)]; piers between; inner limewash face"""
    cuts = sorted(openings); xa = xs[0]
    for (o0, o1, z0, z1) in cuts:
        k.box(0, xa, o0, y - t / 2, y + t / 2, 0, EAVE); k.box(0, o0, o1, y - t / 2, y + t / 2, 0, z0) if z0 > 0 else None
        k.box(0, o0, o1, y - t / 2, y + t / 2, z1, EAVE); xa = o1
    k.box(0, xa, xs[1], y - t / 2, y + t / 2, 0, EAVE)
win = lambda xc: (xc - 2.5, xc + 2.5, 5.0, 13.0)
wall_x(Y1, (X0, X1), [win(x) for x in (-48, -36, -24, -12, 0, 12, 34, 48)], inner=1)
wall_x(Y0, (X0, X1), [win(x) for x in (-48, -36, -24, 34, 48)] + [(-11.0, 7.0, 0, 14.0)], inner=-1)    # loading door to the siding
for xg in (X0, X1):
    k.box(0, xg - 0.75, xg + 0.75, Y0 - 0.75, Y1 + 0.75, 0, EAVE)
    for s_ in range(14):   # gable triangle in courses
        z0 = EAVE + s_ * (RIDGE - EAVE) / 14; w_ = (Y1 + 0.75) * (1 - (s_ + 1) / 14)
        k.box(0, xg - 0.75, xg + 0.75, -w_, w_, z0, z0 + (RIDGE - EAVE) / 14)
# partition between the machine shop and the glass house, with a wide arch-less opening (W03)
k.box(0, 19.25, 20.75, Y0, -9.0, 0, EAVE); k.box(0, 19.25, 20.75, 9.0, Y1, 0, EAVE); k.box(0, 19.25, 20.75, -9.0, 9.0, 15.0, EAVE)
for xs_ in (19.0, 21.0): k.box(4, xs_ - 0.05, xs_ + 0.05, -9, 9, 15.0, EAVE)
# roof: trusses every 12 ft, purlins, slates with a ridge light 8 ft wide each side of the ridge
half = Y1 + 1.0; pitch = (RIDGE - EAVE) / half
for xt in range(-48, 61, 12):
    if abs(xt) == 60: continue
    k.bar(2, (xt, -half, EAVE), (xt, half, EAVE), 0.75, 0.9)                         # tie beam
    k.bar(2, (xt, -half, EAVE + 0.4), (xt, 0, RIDGE - 0.4), 0.7, 0.8); k.bar(2, (xt, half, EAVE + 0.4), (xt, 0, RIDGE - 0.4), 0.7, 0.8)
    k.bar(2, (xt, 0, EAVE), (xt, 0, RIDGE - 0.4), 0.55, 0.55)                        # king post
    for sy in (-1, 1): k.bar(2, (xt, 0, EAVE + 2), (xt, sy * half * 0.5, EAVE + (RIDGE - EAVE) * 0.5 - 0.3), 0.45, 0.45)
for sy in (-1, 1):
    for f in (0.25, 0.5, 0.75):
        yy = sy * half * (1 - f); k.bar(2, (X0, yy, EAVE + f * (RIDGE - EAVE) + 0.5), (X1, yy, EAVE + f * (RIDGE - EAVE) + 0.5), 0.5, 0.6)
roofb = bmesh.new()
def roof_strip(y0, y1, m_i, kit):
    z0 = EAVE + (half - abs(y0)) * pitch + 0.9; z1 = EAVE + (half - abs(y1)) * pitch + 0.9
    n0 = len(kit.bm.faces); vs = [kit.bm.verts.new((ft(x), ft(y), ft(z))) for (x, y, z) in [(X0 - 1, y0, z0), (X1 + 1, y0, z0), (X1 + 1, y1, z1), (X0 - 1, y1, z1)]]
    kit.bm.faces.new(vs); kit._t(m_i, n0)
for sy in (-1, 1):
    roof_strip(sy * half, sy * 8.0, 3, k)
k.done("SHED", CO["SHED"], part_kind="shed")
rl = Kit([RL]); roof_strip(-8.0, 0.0, 0, rl); roof_strip(0.0, 8.0, 0, rl); rl.done("SHED_RIDGE_LIGHT", CO["SHED"], part_kind="rooflight")
# windows: small-paned sheet glass
wk_ = Kit([GLASS_PANE, IRON])
for y in (Y0, Y1):
    for xc in ((-48, -36, -24, 34, 48) if y == Y0 else (-48, -36, -24, -12, 0, 12, 34, 48)):
        wk_.box(0, xc - 2.5, xc + 2.5, y - 0.03, y + 0.03, 5.0, 13.0)
        for zz in (7, 9, 11): wk_.box(1, xc - 2.5, xc + 2.5, y - 0.06, y + 0.06, zz - 0.04, zz + 0.04)
        for xx in (-1.25, 0, 1.25): wk_.box(1, xc + xx - 0.04, xc + xx + 0.04, y - 0.06, y + 0.06, 5.0, 13.0)
wk_.done("SHED_WINDOWS", CO["SHED"], part_kind="window")
g = Kit([EARTH, GRAVEL]); g.box(0, X0, X1, Y0, Y1, -0.2, 0.0); g.done("FLOOR_EARTH", CO["GROUND"])
g = Kit([GRAVEL]); g.box(0, -400, 400, -400, 400, -0.5, -0.02); g.done("YARD", CO["GROUND"])
# ---------------- machine shop: engine, line shaft, sash-bar and gutter machines (W04-W06) ----------------
SHAFT_Z = 15.0
s = Kit([IRON, LEATHER, BRASS, BRICK, TIMB])
s.cyl(0, (-58, 0, SHAFT_Z), (18, 0, SHAFT_Z), 0.13, 10)
for xh in range(-48, 13, 12): s.bar(0, (xh, 0, SHAFT_Z), (xh, 0, EAVE), 0.25, 0.4); s.cyl(2, (xh - 0.3, 0, SHAFT_Z), (xh + 0.3, 0, SHAFT_Z), 0.3, 10)
# horizontal steam engine on a brick bed at the west end, flywheel 9 ft
s.box(3, -58, -44, -6, -1, 0, 2.2); s.cyl(0, (-57, -3.5, 3.6), (-51, -3.5, 3.6), 1.1, 18); s.bar(0, (-51, -3.5, 3.6), (-46, -3.5, 3.6), 0.25)
s.wheel(0, (ft(-45.0), ft(-3.5), ft(5.0)), "y", ft(4.5), ft(0.5), ft(0.45), 8)
s.cyl(0, (-45, -4.6, 5.0), (-45, 1.0, 5.0), 0.3, 10)
s.cyl(1, (-45, 0.0, 5.0), (-45, 0.0, 5.0 + 0.01), 1.6, 18)  # driving pulley
s.bar(1, (-45, 0.0, 6.6), (-45, 0.0, SHAFT_Z + 0.9), 0.55, 0.04); s.bar(1, (-45, 0.0, 3.4), (-45, 0.0, SHAFT_Z - 0.9), 0.55, 0.04)
s.cyl(0, (-45, -0.3, SHAFT_Z), (-45, 0.3, SHAFT_Z), 0.95, 16)
s.cyl(3, (-56, -14, 0), (-56, -14, EAVE + 16), 1.6, 12, r2=1.2)  # engine-house stack through the roof (boiler outside, W07)
s.done("ENGINE_AND_SHAFT", CO["SHOP"], part_kind="engine")
def machine(name, x, y, L, kind):
    m = Kit([IRON, TIMB_NEW, LEATHER, BRASS, TIMB])
    m.box(0, -L / 2, L / 2, -1.2, 1.2, 2.5, 2.9)                                    # cast bed
    for xl in [(-L / 2 + 1) + i * (L - 2) / max(1, int(L // 7)) for i in range(int(L // 7) + 1)]:
        m.box(0, xl - 0.35, xl + 0.35, -1.0, 1.0, 0, 2.5); m.box(0, xl - 0.6, xl + 0.6, -1.3, 1.3, 0, 0.25)
    m.cyl(0, (0, -1.6, 4.2), (0, 1.6, 4.2), 0.22, 10)                               # cutter spindle frame
    for sy in (-1.5, 1.5): m.box(0, -0.4, 0.4, sy - 0.15, sy + 0.15, 2.9, 4.6)
    m.cyl(3, (0, -0.4, 3.4), (0, 0.4, 3.4), 0.9 if kind == "sash" else 1.2, 18)       # cutter / saw head
    m.cyl(2, (0, 1.6, 4.2), (0, 2.3, 4.2), 0.8, 14)                                 # fast-and-loose pulleys
    m.bar(2, (0, 2.0, 4.6), (0, 2.0, SHAFT_Z - y - 0.0 if False else SHAFT_Z - 0.7), 0.4, 0.035)
    for xr in (-L / 2 + 1.2, -2.0, 2.0, L / 2 - 1.2): m.cyl(0, (xr, -0.9, 3.15), (xr, 0.9, 3.15), 0.22, 10)   # feed rollers
    if kind == "sash":     # a deal scantling going in, the profiled bar coming out
        m.box(1, -L / 2 - 2, -0.6, -0.12, 0.12, 2.95, 3.2); m.box(1, 0.6, L / 2 + 1.5, -0.05, 0.05, 2.95, 3.08)
        for sx in (-0.07, 0.07): m.box(1, 0.6, L / 2 + 1.5, sx - 0.02, sx + 0.02, 3.08, 3.12)
    else:                  # gutter timber 24 ft x 5 x 6 in with the Paxton channel and condensation grooves being cut
        m.box(1, -L / 2 + 0.5, L / 2 - 0.5, -0.25, 0.25, 2.95, 3.35)
        m.box(4, 0.0, L / 2 - 0.5, -0.12, 0.12, 3.34, 3.36)
    return m.done(name, CO["SHOP"], x, y, 0, 0, part_kind="machine", machine=kind)
machine("MACHINE_SASHBAR", -30.0, -7.0, 14.0, "sash"); machine("MACHINE_SASHBAR_2", -30.0, -15.0, 14.0, "sash")
machine("MACHINE_GUTTER", -22.0, 9.0, 26.0, "gutter")
# w02: flat leather belts from line shaft down to each machine (was a thin vertical bar only)
belt = Kit([LEATHER, IRON])
for (mx, my, half_w) in ((-30.0, -7.0, 0.55), (-30.0, -15.0, 0.55), (-22.0, 9.0, 0.7)):
    # open belt loop: shaft pulley at (mx, 0, SHAFT_Z) → machine pulley at (mx, my+2.0, 4.2)
    top = (mx, 0.0, SHAFT_Z - 0.1)
    bot = (mx, my + 2.0, 4.6)
    # two strands of the belt (tight / slack)
    for dx in (-half_w * 0.15, half_w * 0.15):
        belt.bar(0, (top[0] + dx, top[1], top[2]), (bot[0] + dx, bot[1], bot[2]), 0.12, 0.025)
    # shaft-side pulley face
    belt.cyl(1, (mx, -0.35, SHAFT_Z), (mx, 0.35, SHAFT_Z), 0.85, 14)
    # floor drip pans under belt runs
    belt.box(1, mx - 0.8, mx + 0.8, min(0, my + 2) - 0.4, max(0, my + 2) + 0.4, 0.02, 0.08)
belt.done("SHOP_BELTS", CO["SHOP"], part_kind="belt")
# w02: wood shavings / deal chips on the shop floor near sash machines
sh = Kit([TIMB_NEW, TIMB])
Rsh = R
for i in range(48):
    x = -34.0 + Rsh.uniform(0, 18); y = -18.0 + Rsh.uniform(0, 14)
    z = 0.01 + Rsh.uniform(0, 0.04)
    L = Rsh.uniform(0.15, 0.55); w = Rsh.uniform(0.03, 0.09); h = Rsh.uniform(0.01, 0.035)
    sh.box(0 if i % 3 else 1, x, x + L, y, y + w, z, z + h)
# larger curled shaving piles
for (px, py) in ((-28.0, -10.5), (-26.5, -16.0), (-18.0, 7.5), (-32.0, -5.0)):
    for j in range(8):
        sh.cyl(0, (px + Rsh.uniform(-0.4, 0.4), py + Rsh.uniform(-0.4, 0.4), 0.02),
               (px + Rsh.uniform(-0.3, 0.3), py + Rsh.uniform(-0.3, 0.3), 0.15 + Rsh.uniform(0, 0.2)),
               Rsh.uniform(0.04, 0.12), 6, True, Rsh.uniform(0.02, 0.06))
sh.done("SHOP_SHAVINGS", CO["SHOP"], part_kind="shavings")
INFO["belts"] = 3; INFO["shaving_clumps"] = 48
# output: sash bars (49 in x 1 x 1.5 in) stacked on trestles; gutters (24 ft) stacked; scantling stack
st = Kit([TIMB_NEW, TIMB])
for tx in (-14.0, -9.5):
    st.box(1, tx - 0.2, tx + 0.2, -19.5, -13.5, 0, 2.6)
nb = 0
for row in range(9):
    for col in range(30):
        y_ = -19.2 + col * 0.18; st.box(0, -16.0, -16.0 + 49 / 12, y_, y_ + 0.09, 2.6 + row * 0.13, 2.72 + row * 0.13); nb += 1
for row in range(5):
    for col in range(5): st.box(0, -45.0, -21.0, 16.0 + col * 0.55, 16.0 + col * 0.55 + 0.42, 0.3 + row * 0.52, 0.3 + row * 0.52 + 0.5)
for xx in (-44, -32, -22): st.box(1, xx - 0.3, xx + 0.3, 15.6, 19.0, 0, 0.3)
st.done("STACK_SASHBARS_GUTTERS", CO["SHOP"], part_kind="product")
INFO["sash_bars_stacked"] = nb
# ---------------- glass house: furnace, blowing stage over swing pits, cylinders, flattening kiln (W08-W11) ----------------
gk = Kit([BRICK_SOOT, GLOW, TIMB, IRON, BRICK])
FX, FY = 40.0, 6.0
gk.cyl(0, (FX, FY, 0), (FX, FY, 9.0), 7.0, 24); gk.cyl(0, (FX, FY, 9.0), (FX, FY, 12.0), 7.0, 24, r2=4.5)
gk.cyl(0, (FX, FY, 12.0), (FX, FY, EAVE + 16), 2.2, 14, r2=1.6)                     # flue through the roof
glory = []
for a in (-150, -110, -70, -30):
    ra = math.radians(a); gx, gy = FX + 7.02 * math.cos(ra), FY + 7.02 * math.sin(ra); glory.append((gx, gy))
    gk.box(1, gx - 0.45, gx + 0.45, gy - 0.45, gy + 0.45, 4.6, 5.5)
# working stage (4 ft) south of the furnace, with three swing pits cut through it (W09)
STZ = 4.0
pits = [(30.0, -10.0), (38.0, -10.0), (46.0, -10.0)]
gk.box(2, 26.0, 54.0, -4.5, -2.5, 0, STZ)                                          # stage front to the furnace
for (px, py) in pits:
    gk.box(2, px - 4.0, px - 1.0, -14.0, -4.5, STZ - 0.3, STZ); gk.box(2, px + 1.0, px + 4.0, -14.0, -4.5, STZ - 0.3, STZ)
    for zz in range(0, 4): gk.box(2, px - 4.0, px + 4.0, -14.0 + zz * 0.0, -14.0 + 0.4, 0, STZ)
    gk.box(4, px - 1.0, px - 0.8, -14.0, -4.5, -10, STZ - 0.3); gk.box(4, px + 0.8, px + 1.0, -14.0, -4.5, -10, STZ - 0.3)
for xs_ in (26.0, 54.0): gk.box(2, xs_ - 0.25, xs_ + 0.25, -14.0, -2.5, 0, STZ)
gk.box(2, 26.0, 54.0, -2.5, -2.4, STZ, STZ + 3.2)                                   # stage rail toward the furnace? no -- low rail
# flattening kiln (W10): brick box with an arched glowing mouth, east end
KX, KY = 52.0, 14.0
gk.box(4, KX - 6, KX + 6, KY - 4.5, KY + 6.5, 0, 6.5); gk.box(4, KX - 5, KX + 5, KY - 3.5, KY + 5.5, 6.5, 8.0)
gk.box(1, KX - 1.8, KX + 1.8, KY - 4.56, KY - 4.5, 2.3, 4.4)
gk.cyl(0, (KX + 3, KY + 3, 8.0), (KX + 3, KY + 3, EAVE + 10), 1.1, 10)
gk.done("GLASSHOUSE", CO["GLASSHOUSE"], part_kind="glasshouse")
# cylinders: on racks (finished, split), a few on the stage; the swing pits carry cylinders on blowpipes (hot)
cy = Kit([GLASS, IRON, TIMB, HOT])
CYL_L, CYL_R = 4.3, 0.55       # ~52 x 13 in cylinders for 49 x 10 in panes (W11, inferred size)
for (rx, ry) in ((24.0, 16.0), (24.0, 20.5)):
    for lv in range(3):
        z = 0.6 + lv * 1.6; cy.box(2, rx - 0.15, rx + 14.0, ry - 1.4, ry + 1.4, z - 0.25, z - 0.1)
        for j in range(11):
            xx = rx + 0.7 + j * 1.25; cy.cyl(0, (xx, ry - CYL_L / 2, z + CYL_R), (xx, ry + CYL_L / 2, z + CYL_R), CYL_R, 14, cap=False)
    for xx in (rx, rx + 7, rx + 14): cy.box(2, xx - 0.15, xx + 0.15, ry - 1.4, ry + 1.4, 0, 0.6 + 2 * 1.6)
ncyl = 66
blowers = []
for j, (px, py) in enumerate(pits):
    # blowpipe from a blower on the stage edge, cylinder swinging down into the pit
    bx, by = px, -5.0; tip = (px, -8.4 - 0.6 * j, STZ - 2.0 - 1.5 * j)
    cy.cyl(1, (bx, by, STZ + 3.6), tip, 0.06, 6)
    cyl_end = (tip[0], tip[1] - 0.3 * (1 + j * 0.3), tip[2] - CYL_L)
    cy.cyl(3 if j == 1 else 0, tip, cyl_end, CYL_R * (0.85 if j == 1 else 1.0), 14)
    blowers.append((bx, by + 0.4, STZ))
cy.done("CYLINDERS", CO["GLASSHOUSE"], part_kind="glass_cylinders")
INFO["cylinders"] = ncyl + 3
# w02: split cylinders (opened for flattening) racked by the kiln mouth
sp = Kit([GLASS, IRON, TIMB, HOT])
for j in range(6):
    xx = KX - 5.5 + (j % 3) * 2.2; yy = KY - 6.5 - (j // 3) * 1.8; zz = 0.4
    # half-cylinder as thin curved shell approx: two quarter slabs + edge
    sp.box(0, xx - CYL_L / 2, xx + CYL_L / 2, yy - 0.05, yy + 0.05, zz, zz + CYL_R * 2.0)
    sp.box(0, xx - CYL_L / 2, xx + CYL_L / 2, yy - CYL_R * 0.15, yy + CYL_R * 1.7, zz, zz + 0.08)
    # iron stilts
    for sx in (-1, 1):
        sp.box(1, xx + sx * CYL_L / 2 - 0.1, xx + sx * CYL_L / 2 + 0.1, yy - 0.2, yy + 1.5, 0.0, zz)
sp.box(2, KX - 6.5, KX + 1.5, KY - 8.5, KY - 5.8, 0.0, 0.25)  # board runway to kiln
sp.done("SPLIT_CYLINDERS", CO["GLASSHOUSE"], part_kind="split_cylinder")
INFO["split_cylinders"] = 6
# ---------------- railway siding: track, two wagons with a 24 ft girder and columns, shear legs (W12-W14) ----------------
rk = Kit([IRON, TIMB, CAST, TIMB_NEW])
TY = -40.0; G2 = 4.708 / 2
for xx in range(-80, 81, 3): rk.box(1, xx - 0.45, xx + 0.45, TY - 4.3, TY + 4.3, -0.05, 0.4)
for sy in (-1, 1): rk.box(0, -80, 80, TY + sy * G2 - 0.1, TY + sy * G2 + 0.1, 0.4, 0.85)
for (wx, ln) in ((-12.0, 15.0), (4.0, 15.0)):
    rk.box(1, wx - ln / 2, wx + ln / 2, TY - 3.75, TY + 3.75, 2.6, 3.0)                  # floor
    for sy in (-1, 1): rk.box(1, wx - ln / 2, wx + ln / 2, TY + sy * 3.75 - 0.15, TY + sy * 3.75 + 0.15, 3.0, 4.0)
    for sx in (-1, 1): rk.box(1, wx + sx * ln / 2 - 0.15, wx + sx * ln / 2 + 0.15, TY - 3.75, TY + 3.75, 3.0, 4.0)
    rk.box(0, wx - ln / 2 + 0.5, wx + ln / 2 - 0.5, TY - 2.6, TY + 2.6, 1.9, 2.6)          # solebar/frame
    for ax in (-4.5, 4.5):
        for sy in (-1, 1): rk.wheel(0, (ft(wx + ax), ft(TY + sy * G2), ft(1.5)), "y", ft(1.5), ft(0.25), ft(0.25), 10)
        rk.cyl(0, (wx + ax, TY - G2, 1.5), (wx + ax, TY + G2, 1.5), 0.2, 8)
    for sx in (-1, 1): rk.box(0, wx + sx * (ln / 2 + 0.4) - 0.2, wx + sx * (ln / 2 + 0.4) + 0.2, TY - 1.6, TY + 1.6, 2.4, 3.0)   # buffer beams
    rk.box(1, wx - 1.0, wx + 1.0, TY - 3.0, TY + 3.0, 4.0, 4.6)                          # bolster
# 24 ft cast girder (3 ft deep, open web) across both wagons' bolsters
GX0, GX1, GZ = -16.0, 8.0, 4.6
for zz in (GZ, GZ + 2.8): rk.box(2, GX0, GX1, TY + 0.55 - 0.35, TY + 0.55 + 0.35, zz, zz + 0.2)
for i in range(9):
    xa = GX0 + i * 3.0; rk.bar(2, (xa, TY + 0.55, GZ + 0.2), (xa + 1.5, TY + 0.55, GZ + 2.8), 0.22, 0.12)
    if xa + 3.0 <= GX1: rk.bar(2, (xa + 1.5, TY + 0.55, GZ + 2.8), (xa + 3.0, TY + 0.55, GZ + 0.2), 0.22, 0.12)
for xa in (GX0, GX1): rk.box(2, xa - 0.15, xa + 0.15, TY + 0.2, TY + 0.9, GZ, GZ + 3.0)
# columns (8 in dia, ~18 ft) lying on the first wagon on chocks, the second loading from the shear legs
ncols = 0
for j in range(3):
    yy = TY - 2.6 + j * 0.8; rk.cyl(2, (-19.0, yy, 3.4 + 0.33), (-1.5, yy, 3.4 + 0.33), 0.33, 12); ncols += 1
    rk.box(3, -19.0 + 0.0, -18.4, yy - 0.3, yy + 0.3, 3.0, 3.4)
# shear legs: two timber legs over the second wagon, tackle and a column hanging
SLX = 11.0; top = (SLX, TY, 26.0)
for (ax_, ay_) in ((SLX - 5, TY - 9), (SLX + 5, TY - 9)): rk.bar(1, (ax_, ay_, 0), top, 0.7, 0.7)
rk.bar(1, (SLX, TY + 13, 0), top, 0.5, 0.5)   # back guy (timber)
rk.cyl(0, top, (SLX, TY + 0.3, 13.5), 0.05, 6); rk.box(0, SLX - 0.4, SLX + 0.4, TY - 0.1, TY + 0.7, 12.0, 13.5)
rk.cyl(2, (SLX - 9.0, TY + 0.3, 11.6), (SLX + 9.0, TY + 0.3, 11.6), 0.33, 12); ncols += 1
rk.bar(0, (SLX - 3, TY + 0.3, 11.9), (SLX, TY + 0.3, 12.0), 0.05); rk.bar(0, (SLX + 3, TY + 0.3, 11.9), (SLX, TY + 0.3, 12.0), 0.05)
rk.done("SIDING_WAGONS", CO["SIDING"], part_kind="railway")
INFO.update({"columns_on_wagons": ncols, "girders": 1})
# ---------------- figures ----------------
_pm = {}
def pm(kind, mats, style, key):
    if key not in _pm: _pm[key] = FG.person_mesh("P_" + key, kind, mats, style=style)
    return _pm[key]
def heading(dx, dy): return math.atan2(dy, dx) + math.pi / 2
def person(name, me, x, y, z, rz, **pr):
    ob = bpy.data.objects.new(name, me); ob.location = (ft(x), ft(y), ft(z)); ob.rotation_euler = (0, 0, rz)
    kk = R.uniform(0.95, 1.04); ob.scale = (kk, kk, kk); CO["FIGURES"].objects.link(ob); ob["part_kind"] = "figure"
    for a, b in pr.items(): ob[a] = b
    return ob
def worker(j, apron=False):
    return pm("man", [APRON if apron else WK[j % 5], TROU[j % 2], SKIN[j % 2], CAP, WK[3]], {"hat": ("cap", "low", "cap")[j % 3]}, f"w{j}_{apron}")
shirt = pm("man", [WK[3], TROU[0], SKIN[0], CAP, WK[3]], {"hat": "cap"}, "shirtsleeves")
foreman = pm("man", [mat("black", (0.03, 0.03, 0.035)), TROU[0], SKIN[1], mat("hat", (0.02, 0.02, 0.02)), WK[3]], {"hat": "top", "frock": True, "cravat": True}, "foreman")
nf = 0
for j, (x, y, tx, ty) in enumerate(((-37.5, -9.2, -30, -7), (-23.0, -9.0, -30, -7), (-37.0, -17.3, -30, -15), (-34.0, 11.4, -22, 9), (-11.0, 6.5, -22, 9),
                                    (-49.0, -7.5, -45, -3.5), (-15.0, -12.2, -13, -16))):
    person(f"FIG_SHOP_{j}", worker(j, apron=j in (0, 3)), x, y, 0, heading(tx - x, ty - y), trade="machine_minder"); nf += 1
person("FIG_FOREMAN", foreman, -14.0, -3.0, 0, heading(-1, -0.5), trade="foreman"); nf += 1
for j, (bx, by, bz) in enumerate(blowers):
    person(f"FIG_BLOWER_{j}", shirt, bx, by, bz, heading(0, -1), trade="glass_blower"); nf += 1
for j, (gx, gy) in enumerate(glory[:3]):
    person(f"FIG_GATHERER_{j}", worker(j + 2, True), gx + 1.6 * math.cos(math.radians(-150 + 40 * j)), gy - 2.0, 0, heading(FX - gx, FY - gy), trade="gatherer"); nf += 1
person("FIG_KILN", worker(4, True), KX - 1.0, KY - 7.5, 0, heading(0, 1), trade="flattener"); nf += 1
person("FIG_RACK", worker(1), 31.0, 13.2, 0, heading(0, 1), trade="warehouseman"); nf += 1
for j, (x, y, tx, ty) in enumerate(((7.0, -46.5, 11, -40), (15.5, -46.0, 11, -40), (-6.0, -46.0, -8, -40), (-20.5, -45.5, -12, -40), (2.0, -30.0, 4, -40))):
    person(f"FIG_YARD_{j}", worker(j + 1), x, y, 0, heading(tx - x, ty - y), trade="porter"); nf += 1
person("FIG_CLERK", foreman, 22.0, -50.0, 0, heading(-1, 1), trade="clerk_of_works"); nf += 1
INFO["figures"] = nf
# ---------------- cameras, world ----------------
route = json.load(open(os.path.join(HERE, "..", "route", "camera_route.json")))
for shot in route["shots"]:
    for key in ("start", "end"):
        if key not in shot: continue
        p = Vector([ft(v) for v in shot[key]["pos_ft"]]); q = Vector([ft(v) for v in shot[key]["look_ft"]])
        cd = bpy.data.cameras.new(f"{shot['id']}_{key}"); cd.lens = shot["lens_mm"]; cd.sensor_width = 36; cd.clip_start = 0.05; cd.clip_end = 2000
        co = bpy.data.objects.new(f"{shot['id']}_{key}", cd); co.location = p
        co.rotation_euler = (q - p).to_track_quat('-Z', 'Y').to_euler(); CO["CAMERAS"].objects.link(co)
scene.camera = CO["CAMERAS"].objects[0]
world = bpy.data.worlds.new("WS_World"); scene.world = world; world.use_nodes = True
bg = world.node_tree.nodes["Background"]; sky = world.node_tree.nodes.new("ShaderNodeTexSky")
try: sky.sky_type = 'NISHITA'
except TypeError: pass
try: sky.sun_elevation = math.radians(24); sky.sun_rotation = math.radians(210)
except AttributeError: pass
world.node_tree.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 0.30
sun = bpy.data.lights.new("WS_Sun", 'SUN'); sun.energy = 3.0; sun.angle = math.radians(1.5); sun.color = (1.0, 0.92, 0.82)
so = bpy.data.objects.new("WS_Sun", sun); ROOT.objects.link(so); so.rotation_euler = (math.radians(62), 0, math.radians(30))
for j, (gx, gy) in enumerate(glory):   # w02: brighter glory bloom + secondary spill
    L = bpy.data.lights.new(f"WS_Glory_{j}", 'POINT'); L.energy = 1600; L.color = (1.0, 0.48, 0.16); L.shadow_soft_size = 0.45
    o = bpy.data.objects.new(f"WS_Glory_{j}", L); o.location = (ft(gx + (gx - FX) * 0.12), ft(gy + (gy - FY) * 0.12), ft(5.0)); ROOT.objects.link(o)
    L2 = bpy.data.lights.new(f"WS_GlorySpill_{j}", 'POINT'); L2.energy = 400; L2.color = (1.0, 0.55, 0.25); L2.shadow_soft_size = 1.2
    o2 = bpy.data.objects.new(f"WS_GlorySpill_{j}", L2); o2.location = (ft(gx + (gx - FX) * 0.55), ft(gy + (gy - FY) * 0.55), ft(4.2)); ROOT.objects.link(o2)
L = bpy.data.lights.new("WS_Kiln", 'POINT'); L.energy = 900; L.color = (1.0, 0.42, 0.12); o = bpy.data.objects.new("WS_Kiln", L); o.location = (ft(KX), ft(KY - 5.5), ft(3.3)); ROOT.objects.link(o)
# w02: darker glass-house ambient (world a touch gloomier so bloom reads)
bg.inputs[1].default_value = 0.22
scene.render.engine = 'CYCLES'; scene.cycles.device = 'CPU'; scene.cycles.samples = 64; scene.cycles.use_denoising = True
scene.cycles.max_bounces = 6; scene.cycles.transparent_max_bounces = 16
scene.render.resolution_x = 1280; scene.render.resolution_y = 720
try: scene.view_settings.view_transform = 'AgX'; scene.view_settings.look = 'AgX - Medium High Contrast'
except TypeError: pass
scene.view_settings.exposure = 0.0
scene["grok_build"] = json.dumps({"set": "O-WORKSHOP", "seed": SEED, "info": INFO})
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True)
print("SAVED", OUT, INFO)
