"""CANDIDATE ln03_cp002 — CP002 "The world that would build it": a representative London railway lane, c.1850.
Opens rounds/ln02.blend (live, read-only), replaces the INDUSTRY set (viaduct, train, factory, terraces, cart, ground,
street figures) and saves a NEW file. The CP005 planning room at x=300 ft, the world, sun and exposure are untouched.

blender -b rounds/ln02.blend -P scripts/build_cp002_street.py -- --out rounds/candidates/ln03_cp002.blend

Dimension sources (logged as D-LN-CP002-xx in DEPARTURES.md):
  London & Greenwich Railway viaduct (1834-36): semicircular brick arches, 20 ft centre-to-centre, ~18 ft span,
  22 ft high, parapets ~4 ft 6 in, grey/yellow London stock brick; arches let as workshops/storage
  (Historic England list entry 1253151; Railway Wonders of the World; Victorian Web).
  Two-up two-down workers' terraces ~13-15 ft frontage, ~18-20 ft eaves; 1840s 2-2-2 express engine (Jenny Lind
  type, 1847) 6 ft drivers, no cab, weatherboard only; 4-wheel carriages; c.1850 mill chimneys 100-150 ft;
  cast-iron gas lamp columns ~9-10 ft to ladder bar; London granite setts ~4x9 in; York stone flags.
"""
import bpy, bmesh, sys, os, math, random, json
from mathutils import Vector, Matrix
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grokkit as G
from grokkit import ft, Kit
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "/tmp/ln03_cp002.blend"
R = random.Random(1850)
G.PFX = "LN2_"
sc = bpy.context.scene

# ---------------------------------------------------------------- remove the ln02 INDUSTRY set (room untouched)
for nm in ("LN_Viaduct", "LN_Train", "LN_Factory", "LN_Terraces", "LN_Cart", "LN_Ground"):
    o = bpy.data.objects.get(nm)
    if o: bpy.data.objects.remove(o, do_unlink=True)
for o in list(bpy.data.objects):
    if o.name.startswith("LN_Street_"): bpy.data.objects.remove(o, do_unlink=True)
IND = bpy.data.collections.get("INDUSTRY")
# D-LN-CP002-12: people_lib's name matcher reads "LN_Fireplace" as a figure ("_FIRE") and at render time swaps it for a
# 1930s fireman standing at the object's origin (0,0,0) — i.e. inside the CP002 viaduct arch. Tag it as an ornament so the
# swap leaves it alone (the CP005 room then keeps its fireplace instead of losing it).
_fp = bpy.data.objects.get("LN_Fireplace")
if _fp: _fp["part_kind"] = "ornament"
FIGC = bpy.data.collections.get("LN_FIGURES")
SMK = G.coll("LN2_SMOKE", IND)
info = {k: v for k, v in json.loads(sc.get("grok_build", "{}")).get("info", {}).items() if k in ("table", "plans", "samples")}  # CP005 room counts carried over

# ---------------------------------------------------------------- shader helpers
# ALB: the ln02 authored light (sun 1.6 + Nishita sky, exposure -0.10, AgX MHC) is kept unchanged for a matched-exposure pair;
# under it a 0.3 albedo already reads near-white (the live peach viaduct), so surface albedos here are scaled to read as sooty
# London stock brick / tarred timber / granite rather than cream. (D-LN-CP002-10)
ALB = 0.63
def _a(c): return tuple(v * ALB for v in c)
def _nt(name):
    M = bpy.data.materials.new("LN2_" + name); M.use_nodes = True; nt = M.node_tree
    b = nt.nodes["Principled BSDF"]; M["cpl_mat_v1"] = 1  # already gritted here; skip survey grit pass
    return M, nt, b
def _pos_uv(nt, mode):
    """mode 'wall': (x+y, z) so bricks course on walls aligned to X or Y; 'floor': (y, x)."""
    tc = nt.nodes.new("ShaderNodeNewGeometry"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Position"], sp.inputs[0])
    cb = nt.nodes.new("ShaderNodeCombineXYZ")
    if mode == "wall":
        ad = nt.nodes.new("ShaderNodeMath"); ad.operation = 'ADD'
        nt.links.new(sp.outputs[0], ad.inputs[0]); nt.links.new(sp.outputs[1], ad.inputs[1])
        nt.links.new(ad.outputs[0], cb.inputs[0]); nt.links.new(sp.outputs[2], cb.inputs[1])
    else:
        nt.links.new(sp.outputs[1], cb.inputs[0]); nt.links.new(sp.outputs[0], cb.inputs[1])
    return cb.outputs[0], sp
def _mix(nt, a, b, fac):
    m = nt.nodes.new("ShaderNodeMix"); m.data_type = 'RGBA'; m.blend_type = 'MIX'
    if isinstance(fac, float): m.inputs["Factor"].default_value = fac
    else: nt.links.new(fac, m.inputs["Factor"])
    for sock, v in ((m.inputs[6], a), (m.inputs[7], b)):
        if isinstance(v, tuple): sock.default_value = (*v, 1)
        else: nt.links.new(v, sock)
    return m.outputs[2]
def _noise(nt, vec, scale, detail=6.0, rough=0.55):
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = detail
    n.inputs["Roughness"].default_value = rough
    if vec is not None: nt.links.new(vec, n.inputs["Vector"])
    return n.outputs["Fac"]
def _ramp(nt, fac, p0, p1, c0=(0, 0, 0), c1=(1, 1, 1)):
    r = nt.nodes.new("ShaderNodeValToRGB"); nt.links.new(fac, r.inputs[0])
    r.color_ramp.elements[0].position = p0; r.color_ramp.elements[1].position = p1
    r.color_ramp.elements[0].color = (*c0, 1); r.color_ramp.elements[1].color = (*c1, 1)
    return r.outputs[0]
def _bump(nt, b, height, strength=0.35, dist=0.01):
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = strength; bp.inputs["Distance"].default_value = dist
    nt.links.new(height, bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
def _math(nt, op, a, b=None):
    m = nt.nodes.new("ShaderNodeMath"); m.operation = op
    for i, v in enumerate((a, b)):
        if v is None: continue
        if isinstance(v, (int, float)): m.inputs[i].default_value = v
        else: nt.links.new(v, m.inputs[i])
    return m.outputs[0]

def mat_brick(name, c1, c2, mortar, soot=(0.035, 0.032, 0.03), soot_amt=0.45, bw=0.23, rh=0.085, top_z=8.9, rough=0.93):
    """English-bond-ish coursing (9 x 3 in brick + 3/8 in joint) from world position; vertical soot streaks
    from the coping down, ground grime, per-brick colour scatter; mortar bump."""
    M, nt, b = _nt(name); uv, sp = _pos_uv(nt, "wall")
    bt = nt.nodes.new("ShaderNodeTexBrick"); nt.links.new(uv, bt.inputs["Vector"])
    bt.inputs["Scale"].default_value = 1.0; bt.inputs["Mortar Size"].default_value = 0.010
    bt.inputs["Brick Width"].default_value = bw; bt.inputs["Row Height"].default_value = rh
    bt.inputs["Color1"].default_value = (*_a(c1), 1); bt.inputs["Color2"].default_value = (*_a(c2), 1)
    bt.inputs["Mortar"].default_value = (*_a(mortar), 1); bt.offset = 0.5; bt.squash = 1.0
    bt.inputs["Bias"].default_value = 0.0
    # soot: vertical streak noise (stretched in z) + top-down gradient + ground grime
    st = nt.nodes.new("ShaderNodeMapping"); st.inputs["Scale"].default_value = (0.26, 0.05, 1.0); nt.links.new(uv, st.inputs["Vector"])
    streak = _ramp(nt, _noise(nt, st.outputs[0], 1.6, 3.0, 0.55), 0.47, 0.60)
    blot = _ramp(nt, _noise(nt, uv, 0.16, 3.0, 0.5), 0.42, 0.66)
    topg = _math(nt, 'MULTIPLY', _math(nt, 'MAXIMUM', _math(nt, 'SUBTRACT', sp.outputs[2], top_z - 3.5), 0.0), 1.0 / 3.5)
    grime = _math(nt, 'MAXIMUM', _math(nt, 'SUBTRACT', 1.0, _math(nt, 'MULTIPLY', sp.outputs[2], 1.4)), 0.0)
    s = _math(nt, 'ADD', _math(nt, 'MULTIPLY', streak, 0.95), _math(nt, 'MULTIPLY', blot, 0.20))
    s = _math(nt, 'ADD', s, _math(nt, 'MULTIPLY', topg, 0.30)); s = _math(nt, 'ADD', s, _math(nt, 'MULTIPLY', grime, 0.45))
    s = _math(nt, 'ADD', _math(nt, 'MULTIPLY', s, soot_amt * 1.15), 0.02); s = _math(nt, 'MINIMUM', _math(nt, 'MAXIMUM', s, 0.0), 0.9)
    col = _mix(nt, bt.outputs["Color"], soot, s)
    nt.links.new(col, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = rough
    _bump(nt, b, _math(nt, 'SUBTRACT', 1.0, bt.outputs["Fac"]), 0.45, 0.012)
    M.diffuse_color = (*c1, 1); return M

def mat_setts(name):
    M, nt, b = _nt(name); uv, sp = _pos_uv(nt, "floor")
    bt = nt.nodes.new("ShaderNodeTexBrick"); nt.links.new(uv, bt.inputs["Vector"])
    bt.inputs["Scale"].default_value = 1.0; bt.inputs["Mortar Size"].default_value = 0.014; bt.inputs["Mortar Smooth"].default_value = 0.4
    bt.inputs["Brick Width"].default_value = 0.24; bt.inputs["Row Height"].default_value = 0.11
    bt.inputs["Color1"].default_value = (*_a((0.15, 0.145, 0.14)), 1); bt.inputs["Color2"].default_value = (*_a((0.22, 0.21, 0.195)), 1)
    bt.inputs["Mortar"].default_value = (*_a((0.07, 0.055, 0.04)), 1); bt.offset = 0.5
    mud = _ramp(nt, _noise(nt, uv, 0.45, 5.0, 0.6), 0.48, 0.70)
    col = _mix(nt, bt.outputs["Color"], _a((0.10, 0.075, 0.05)), _math(nt, 'MULTIPLY', mud, 0.75))
    nt.links.new(col, b.inputs["Base Color"])
    # wet worn tops: lower roughness on stones, mud rough
    nt.links.new(_math(nt, 'ADD', 0.55, _math(nt, 'MULTIPLY', bt.outputs["Fac"], 0.4)), b.inputs["Roughness"])
    _bump(nt, b, _math(nt, 'SUBTRACT', 1.0, bt.outputs["Fac"]), 0.6, 0.02)
    M.diffuse_color = (0.2, 0.19, 0.18, 1); return M

def mat_flags(name):
    M, nt, b = _nt(name); uv, sp = _pos_uv(nt, "floor")
    bt = nt.nodes.new("ShaderNodeTexBrick"); nt.links.new(uv, bt.inputs["Vector"])
    bt.inputs["Scale"].default_value = 1.0; bt.inputs["Mortar Size"].default_value = 0.012
    bt.inputs["Brick Width"].default_value = 0.92; bt.inputs["Row Height"].default_value = 0.61
    bt.inputs["Color1"].default_value = (*_a((0.27, 0.25, 0.21)), 1); bt.inputs["Color2"].default_value = (*_a((0.33, 0.30, 0.25)), 1)
    bt.inputs["Mortar"].default_value = (*_a((0.08, 0.07, 0.06)), 1); bt.offset = 0.37
    dirt = _ramp(nt, _noise(nt, uv, 1.2, 6.0, 0.6), 0.4, 0.75)
    col = _mix(nt, bt.outputs["Color"], _a((0.10, 0.09, 0.075)), _math(nt, 'MULTIPLY', dirt, 0.55))
    nt.links.new(col, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.85
    _bump(nt, b, _math(nt, 'SUBTRACT', 1.0, bt.outputs["Fac"]), 0.4, 0.01)
    return M

def mat_boards(name, c, c_dirty, horizontal=False):
    """tarred / painted timber boarding: 6 in boards (wave bands) + weathering."""
    M, nt, b = _nt(name); uv, sp = _pos_uv(nt, "wall")
    w = nt.nodes.new("ShaderNodeTexWave"); w.wave_type = 'BANDS'; w.bands_direction = 'Y' if horizontal else 'X'
    w.wave_profile = 'SAW'; w.inputs["Scale"].default_value = 1 / 0.15 / 1.0; nt.links.new(uv, w.inputs["Vector"])
    w.inputs["Distortion"].default_value = 0.0
    seam = _ramp(nt, w.outputs["Fac"], 0.90, 0.97)
    grain = _noise(nt, uv, 6.0, 8.0, 0.65)
    wear = _ramp(nt, _noise(nt, uv, 0.8, 4.0, 0.6), 0.45, 0.8)
    col = _mix(nt, _a(c), _a(c_dirty), _math(nt, 'ADD', _math(nt, 'MULTIPLY', wear, 0.7), _math(nt, 'MULTIPLY', grain, 0.2)))
    col = _mix(nt, col, (0.02, 0.018, 0.015), _math(nt, 'MULTIPLY', seam, 0.8))
    nt.links.new(col, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.85
    _bump(nt, b, _math(nt, 'SUBTRACT', 1.0, seam), 0.5, 0.01)
    M.diffuse_color = (*c, 1); return M

def mat_plain(name, c, r=0.8, m=0.0, emit=None):
    M = G.mat(name, _a(c), r, m, emit); M["cpl_mat_v1"] = 1
    b = M.node_tree.nodes["Principled BSDF"]
    if "Specular IOR Level" in b.inputs and r > 0.7: b.inputs["Specular IOR Level"].default_value = 0.3
    return M

def mat_grimy(name, c, c2, scale=3.0, r=0.85, m=0.0):
    M, nt, b = _nt(name)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    n = _ramp(nt, _noise(nt, tc.outputs["Object"], scale, 6.0, 0.6), 0.35, 0.75)
    nt.links.new(_mix(nt, _a(c), _a(c2), n), b.inputs["Base Color"]); b.inputs["Roughness"].default_value = r; b.inputs["Metallic"].default_value = m
    M.diffuse_color = (*c, 1); return M

def mat_window(name):
    """old crown/cylinder glass over a dark interior: dark, slightly mottled, glossy."""
    M, nt, b = _nt(name); tc = nt.nodes.new("ShaderNodeTexCoord")
    n = _noise(nt, tc.outputs["Object"], 9.0, 3.0, 0.5)
    nt.links.new(_mix(nt, (0.010, 0.011, 0.012), (0.035, 0.034, 0.03), n), b.inputs["Base Color"])
    nt.links.new(_math(nt, 'ADD', 0.22, _math(nt, 'MULTIPLY', n, 0.35)), b.inputs["Roughness"]); b.inputs["Specular IOR Level"].default_value = 0.35
    return M

def mat_volume(name, col, dens, aniso=0.2, noise_scale=None, falloff=False, emit=None):
    M = bpy.data.materials.new("LN2_" + name); M.use_nodes = True; nt = M.node_tree; nn = nt.nodes
    out = nn["Material Output"]; [nn.remove(x) for x in list(nn) if x != out]
    pv = nn.new("ShaderNodeVolumePrincipled"); pv.inputs["Color"].default_value = (*col, 1); pv.inputs["Anisotropy"].default_value = aniso
    if emit: pv.inputs["Emission Color"].default_value = (*emit[0], 1); pv.inputs["Emission Strength"].default_value = emit[1]
    if noise_scale is None:
        pv.inputs["Density"].default_value = dens
    else:
        tc = nn.new("ShaderNodeTexCoord")
        nz = nn.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = noise_scale; nz.inputs["Detail"].default_value = 6.0
        nz.inputs["Roughness"].default_value = 0.6; nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
        r = nn.new("ShaderNodeValToRGB"); r.color_ramp.elements[0].position = 0.33; r.color_ramp.elements[1].position = 0.66
        nt.links.new(nz.outputs["Fac"], r.inputs[0])
        d = nn.new("ShaderNodeMath"); d.operation = 'MULTIPLY'; d.inputs[1].default_value = dens
        if falloff:   # spherical falloff in object space (unit sphere mesh)
            ln = nn.new("ShaderNodeVectorMath"); ln.operation = 'LENGTH'; nt.links.new(tc.outputs["Object"], ln.inputs[0])
            f = nn.new("ShaderNodeMapRange"); f.inputs["From Min"].default_value = 1.0; f.inputs["From Max"].default_value = 0.35
            nt.links.new(ln.outputs["Value"], f.inputs["Value"])
            m2 = nn.new("ShaderNodeMath"); m2.operation = 'MULTIPLY'; nt.links.new(r.outputs[0], m2.inputs[0]); nt.links.new(f.outputs[0], m2.inputs[1])
            nt.links.new(m2.outputs[0], d.inputs[0])
        else:
            nt.links.new(r.outputs[0], d.inputs[0])
        nt.links.new(d.outputs[0], pv.inputs["Density"])
    nt.links.new(pv.outputs[0], out.inputs["Volume"]); return M

# ---------------------------------------------------------------- materials
M = dict(
    stock=mat_brick("BrickStock", (0.38, 0.30, 0.19), (0.30, 0.245, 0.165), (0.30, 0.28, 0.24), soot_amt=0.55, top_z=8.9),
    ring=mat_brick("BrickRing", (0.26, 0.17, 0.11), (0.20, 0.14, 0.10), (0.24, 0.22, 0.19), soot_amt=0.50, bw=0.11, rh=0.085, top_z=7.3),
    house=mat_brick("BrickHouse", (0.30, 0.20, 0.13), (0.24, 0.17, 0.12), (0.30, 0.28, 0.24), soot_amt=0.48, top_z=6.1),
    mill=mat_brick("BrickMill", (0.28, 0.16, 0.10), (0.22, 0.13, 0.09), (0.28, 0.26, 0.22), soot_amt=0.50, top_z=19.0),
    inner=mat_brick("BrickInner", (0.12, 0.10, 0.08), (0.09, 0.08, 0.065), (0.12, 0.11, 0.10), soot_amt=0.60, top_z=7.0),
    stone=mat_grimy("StoneDressing", (0.42, 0.40, 0.35), (0.16, 0.15, 0.13), 2.0),
    setts=mat_setts("GraniteSetts"), flags=mat_flags("YorkFlags"),
    kerb=mat_grimy("GraniteKerb", (0.30, 0.29, 0.28), (0.14, 0.13, 0.12), 4.0),
    mud=mat_grimy("Mud", (0.12, 0.09, 0.06), (0.07, 0.055, 0.04), 1.5, 0.95),
    tar=mat_boards("BoardsTarred", (0.035, 0.032, 0.03), (0.08, 0.072, 0.06)),
    green=mat_boards("BoardsGreen", (0.03, 0.06, 0.04), (0.07, 0.075, 0.06)),
    brown=mat_boards("BoardsBrown", (0.10, 0.06, 0.035), (0.07, 0.055, 0.045)),
    door=mat_boards("BoardsDoor", (0.035, 0.045, 0.04), (0.05, 0.045, 0.038)),
    iron=mat_plain("CastIron", (0.035, 0.037, 0.04), 0.5, 0.6),
    ironp=mat_grimy("IronPainted", (0.05, 0.07, 0.06), (0.03, 0.03, 0.03), 5.0, 0.6, 0.3),
    win=mat_window("WindowDark"),
    sash=mat_plain("SashPaint", (0.30, 0.28, 0.24), 0.6),
    slate=mat_grimy("SlateRoof", (0.07, 0.075, 0.085), (0.04, 0.04, 0.045), 6.0, 0.55),
    pot=mat_plain("ChimneyPot", (0.30, 0.15, 0.08), 0.85),
    lampglass=mat_plain("LampGlass", (0.30, 0.29, 0.25), 0.2, 0.0, ((1.0, 0.75, 0.42), 0.12)),
    forge=mat_plain("ForgeGlow", (0.3, 0.1, 0.02), 0.9, 0.0, ((1.0, 0.36, 0.08), 18.0)),
    dark=mat_plain("InteriorDark", (0.012, 0.011, 0.01), 0.95),
    wood=mat_grimy("Wood", (0.15, 0.10, 0.06), (0.08, 0.06, 0.04), 3.0, 0.8),
    wheelred=mat_grimy("WheelRed", (0.17, 0.045, 0.025), (0.08, 0.045, 0.03), 3.0, 0.7),
    horse=mat_grimy("HorseBay", (0.036, 0.018, 0.011), (0.02, 0.012, 0.008), 2.0, 0.5),
    horsedk=mat_plain("HorseBlack", (0.02, 0.016, 0.014), 0.6),
    harness=mat_plain("Harness", (0.025, 0.02, 0.018), 0.35, 0.2),
    brass=mat_plain("Brass", (0.50, 0.38, 0.15), 0.35, 0.8),
    loco=mat_grimy("LocoGreen", (0.05, 0.12, 0.06), (0.03, 0.05, 0.035), 4.0, 0.35),
    carriage=mat_grimy("CarriageBrown", (0.08, 0.035, 0.022), (0.045, 0.028, 0.02), 4.0, 0.4),
    canvas=mat_grimy("Tarpaulin", (0.15, 0.14, 0.11), (0.08, 0.075, 0.06), 3.0, 0.9),
    barrel=mat_grimy("BarrelOak", (0.17, 0.10, 0.05), (0.09, 0.06, 0.035), 5.0, 0.7),
    coal=mat_plain("Coal", (0.02, 0.02, 0.022), 0.4),
    crate=mat_grimy("CrateDeal", (0.22, 0.17, 0.10), (0.11, 0.085, 0.055), 4.0, 0.85),
)
ML = list(M.values()); IX = {k: i for i, k in enumerate(M)}
def K(): return Kit(ML)
def I(k): return IX[k]

# ---------------------------------------------------------------- extra geometry helpers on a Kit
def arch_face(k, mi, x0, x1, yf, span_r, spring, top, seg=24, flip=False):
    """vertical wall face (plane y=yf) for one bay [x0,x1] with a semicircular opening centred in the bay."""
    cx = (x0 + x1) / 2; hw = (x1 - x0) / 2
    pts_in = [(cx - span_r * math.cos(math.pi * j / seg), spring + span_r * math.sin(math.pi * j / seg)) for j in range(seg + 1)]
    def outer(px, pz):  # radial projection of an arc point onto the bay rectangle above springing
        dx, dz = px - cx, pz - spring; ts = []
        if dx < -1e-9: ts.append((x0 - cx) / dx)
        if dx > 1e-9: ts.append((x1 - cx) / dx)
        if dz > 1e-9: ts.append((top - spring) / dz)
        t = min(t for t in ts if t > 0); return (cx + dx * t, spring + dz * t)
    pts_out = [outer(*p) for p in pts_in]
    for j in range(seg):
        a, b = pts_in[j], pts_in[j + 1]; c, d = pts_out[j + 1], pts_out[j]
        quad = [(a[0], yf, a[1]), (b[0], yf, b[1]), (c[0], yf, c[1]), (d[0], yf, d[1])]
        # corner correction: if the projection jumps across a rectangle corner, add the corner as a triangle
        if (abs(c[0] - d[0]) > 1e-6 and abs(c[1] - d[1]) > 1e-6):
            corner = (d[0], yf, c[1]) if abs(d[0] - x0) < 1e-6 or abs(d[0] - x1) < 1e-6 else (c[0], yf, d[1])
            k.poly(mi, [(a[0], yf, a[1]), (b[0], yf, b[1]), (c[0], yf, c[1]), corner, (d[0], yf, d[1])][::(-1 if flip else 1)])
        else:
            k.poly(mi, quad[::(-1 if flip else 1)])
    # piers below springing
    k.poly(mi, [(x0, yf, 0), (cx - span_r, yf, 0), (cx - span_r, yf, spring), (x0, yf, spring)][::(-1 if not flip else 1)])
    k.poly(mi, [(cx + span_r, yf, 0), (x1, yf, 0), (x1, yf, spring), (cx + span_r, yf, spring)][::(-1 if not flip else 1)])
    return pts_in

def soffit(k, mi, cx, r, spring, y0, y1, seg=24):
    for j in range(seg):
        a0 = math.pi * j / seg; a1 = math.pi * (j + 1) / seg
        p0 = (cx - r * math.cos(a0), spring + r * math.sin(a0)); p1 = (cx - r * math.cos(a1), spring + r * math.sin(a1))
        k.poly(mi, [(p0[0], y0, p0[1]), (p0[0], y1, p0[1]), (p1[0], y1, p1[1]), (p1[0], y0, p1[1])])
    k.poly(mi, [(cx - r, y0, 0), (cx - r, y1, 0), (cx - r, y1, spring), (cx - r, y0, spring)])
    k.poly(mi, [(cx + r, y0, spring), (cx + r, y1, spring), (cx + r, y1, 0), (cx + r, y0, 0)])

def ellipsoid(bm_kit, mi, c, radii, rot=(0, 0, 0), seg=14, rings=9):
    """add a UV ellipsoid (feet) to a Kit"""
    k = bm_kit; n0 = len(k.bm.faces)
    mat = Matrix.Translation(Vector([ft(v) for v in c])) @ Matrix.Rotation(rot[2], 4, 'Z') @ Matrix.Rotation(rot[1], 4, 'Y') @ Matrix.Rotation(rot[0], 4, 'X') @ Matrix.Diagonal((ft(radii[0]), ft(radii[1]), ft(radii[2]), 1))
    bmesh.ops.create_uvsphere(k.bm, u_segments=seg, v_segments=rings, radius=1.0, matrix=mat)
    k._t(mi, n0)

def tube(k, mi, pts, r, seg=10):
    """chain of tapered cylinders along points [(x,y,z,r)]"""
    for a, b in zip(pts, pts[1:]): k.cyl(mi, a[:3], b[:3], a[3], seg, True, b[3])

# ================================================================ GROUND
gk = K()
gk.box(I("mud"), -260, 420, -260, 420, -0.6, -0.02)
gk.box(I("setts"), -200, 270, -44, -10, -0.05, 0.0)          # south lane carriageway (setts; CP002_lane eye stands in the road)
gk.box(I("flags"), -200, 270, -10, -6, 0.0, 0.42)            # pavement against the viaduct
gk.box(I("kerb"), -200, 270, -10.6, -10.0, -0.05, 0.42)
gk.box(I("flags"), -200, 270, -56, -44.6, 0.0, 0.42)         # far-side pavement
gk.box(I("kerb"), -200, 270, -44.6, -44.0, -0.05, 0.42)
gk.box(I("setts"), -200, 270, 6, 19, -0.05, 0.0)             # north lane between viaduct and terrace
gk.box(I("flags"), -200, 70, 19, 22, 0.0, 0.42)
gk.box(I("kerb"), -200, 70, 18.6, 19.2, -0.05, 0.42)
gk.box(I("setts"), -6, 6, -6, 6, -0.04, 0.01)                # floors of open arches (paved through)
gk.done("LN2_Ground", IND)

# ================================================================ VIADUCT (L&G pattern: 20 ft c/c, 18 ft span, 22 ft to crown)
CC, SPAN_R, CROWN = 20.0, 9.0, 22.0; SPRING = CROWN - SPAN_R
STRING, PARA, COPE = 24.0, 28.5, 29.2; RAIL = 25.0; YS, YN = -6.0, 6.0
X0, NB = -110.0, 17                     # x -110 .. 230
vk = K(); info["viaduct_arches"] = 0
OPEN = {-10.0, 50.0, 130.0}             # bays left open through (cross-passages), others let as workshops
bay_use = {}
for i in range(NB):
    x0 = X0 + i * CC; x1 = x0 + CC; cx = x0 + CC / 2
    arch_face(vk, I("stock"), x0, x1, YS, SPAN_R, SPRING, STRING, flip=False)
    arch_face(vk, I("stock"), x0, x1, YN, SPAN_R, SPRING, STRING, flip=True)
    soffit(vk, I("inner"), cx, SPAN_R, SPRING, YS, YN)
    # voussoir ring (two header rings, 14 in deep, slightly proud) on both faces
    nv = 27
    for f, yy in ((-1, YS - 0.14), (1, YN + 0.14)):
        for j in range(nv):
            a0 = math.pi * (j + 0.06) / nv; a1 = math.pi * (j + 0.94) / nv
            q = []
            for (a, rr) in ((a0, SPAN_R), (a1, SPAN_R), (a1, SPAN_R + 1.25), (a0, SPAN_R + 1.25)):
                q.append((cx - rr * math.cos(a), yy, SPRING + rr * math.sin(a)))
            vk.poly(I("ring"), q if f < 0 else q[::-1])
    # stone impost band at springing + plinth (plain L&G piers, no pilasters)
    for xb in (x0,):
        vk.box(I("stone"), xb - 1.25, xb + 1.25, YS - 0.6, YS, SPRING - 0.6, SPRING)   # stone impost
        vk.box(I("stone"), xb - 1.25, xb + 1.25, YN, YN + 0.6, SPRING - 0.6, SPRING)
        vk.box(I("stone"), xb - 1.3, xb + 1.3, YS - 0.6, YS, 0, 0.9)                   # plinth
    USE = {-30.0: "workshop", 10.0: "smithy", 30.0: "store", 70.0: "stable"}
    use = "open" if x0 in OPEN else USE.get(x0, ["workshop", "store", "stable", "smithy"][i % 4])
    bay_use[x0] = use
    info["viaduct_arches"] += 1
xe = X0 + NB * CC
# string course, parapets, coping (both sides), end abutment
vk.box(I("stone"), X0 - 2, xe + 2, YS - 0.55, YN + 0.55, STRING, STRING + 0.75)
for (ya, yb) in ((YS - 0.2, YS + 1.2), (YN - 1.2, YN + 0.2)):
    vk.box(I("stock"), X0 - 2, xe + 2, ya, yb, STRING + 0.75, PARA)
    vk.box(I("stone"), X0 - 2, xe + 2, ya - 0.25, yb + 0.25, PARA, PARA + 0.7)
vk.box(I("stock"), xe, xe + 14, YS - 0.5, YN + 0.5, 0, PARA)   # abutment / end block
vk.done("LN2_Viaduct", IND)

# ---- railbed: ballast, rails, sleepers peeking over parapet (inside)
rk = K()
rk.box(I("mud"), X0, xe, YS + 1.2, YN - 1.2, STRING + 0.2, RAIL - 0.4)
for yc in (-2.6, 2.6):     # two tracks, 4 ft 8½ in gauge
    for s in (-2.35, 2.35):
        rk.box(I("iron"), X0, xe, yc + s - 0.1, yc + s + 0.1, RAIL - 0.4, RAIL)
rk.done("LN2_Railbed", IND)

# ================================================================ ARCH INFILLS (arches let as workshops, stores, stables, smithy)
ik = K()
def lunette(k, cx, y, zb, r, mi_frame, mi_glass):
    """semicircular fanlight glazing above a transom (radial glazing bars)"""
    seg = 16
    for j in range(seg):
        a0 = math.pi * j / seg; a1 = math.pi * (j + 1) / seg
        k.poly(mi_glass, [(cx, y, zb), (cx - r * math.cos(a1), y, zb + r * math.sin(a1)), (cx - r * math.cos(a0), y, zb + r * math.sin(a0))])
    for j in range(0, seg + 1, 2):
        a = math.pi * j / seg
        k.bar(mi_frame, (cx, y - 0.08, zb), (cx - r * math.cos(a), y - 0.08, zb + r * math.sin(a)), 0.16, 0.12)
    for rr in (r * 0.45, r * 0.98):
        for j in range(seg):
            a0 = math.pi * j / seg; a1 = math.pi * (j + 1) / seg
            k.bar(mi_frame, (cx - rr * math.cos(a0), y - 0.09, zb + rr * math.sin(a0)), (cx - rr * math.cos(a1), y - 0.09, zb + rr * math.sin(a1)), 0.2, 0.14)

for x0, use in bay_use.items():
    cx = x0 + CC / 2; r = SPAN_R; ys = YS + 1.4   # screens set back ~1 ft 5 in from the face
    if use == "open":
        continue
    mat_b = {"workshop": "green", "smithy": "tar", "stable": "brown", "store": "tar"}[use]
    TR = SPRING - 1.0                               # transom height
    # rear soot wall where the front is part open
    ik.box(I("inner"), cx - r, cx + r, YN - 1.6, YN - 1.2, 0, CROWN)
    if use == "store":
        ik.box(I("house"), cx - r, cx + r, ys, ys + 0.6, 0, CROWN)
        ik.box(I("door"), cx - 2.2, cx + 2.2, ys - 0.12, ys, 0.1, 7.6)
        ik.box(I("ring"), cx - 2.6, cx + 2.6, ys - 0.1, ys, 7.6, 8.4)
        for sx in (-1, 1):
            wx = cx + sx * 5.5
            ik.box(I("win"), wx - 1.2, wx + 1.2, ys - 0.06, ys - 0.02, 4.5, 8.0)
            ik.box(I("stone"), wx - 1.45, wx + 1.45, ys - 0.35, ys, 4.2, 4.5)
            ik.box(I("ring"), wx - 1.45, wx + 1.45, ys - 0.08, ys, 8.0, 8.7)
            for t in range(3): ik.box(I("sash"), wx - 1.25, wx + 1.25, ys - 0.1, ys - 0.06, 4.5 + (t + 1) * 0.875 - 0.05, 4.5 + (t + 1) * 0.875 + 0.05)
            ik.box(I("sash"), wx - 0.05, wx + 0.05, ys - 0.1, ys - 0.06, 4.5, 8.0)
        lunette(ik, cx, ys - 0.02, SPRING + 0.5, 3.2, I("sash"), I("win"))
        ik.box(I("wood"), cx - 4.5, cx + 4.5, ys - 0.35, ys - 0.15, 9.2, 10.4)
        continue
    if use == "smithy":
        # open lower front with a dark interior, forge glow at the back, boarded upper
        ik.box(I(mat_b), cx - r, cx - r + 3.2, ys, ys + 0.3, 0, TR)
        ik.box(I(mat_b), cx + r - 3.2, cx + r, ys, ys + 0.3, 0, TR)
        ik.box(I(mat_b), cx - r, cx + r, ys, ys + 0.3, TR - 1.6, TR)
        ik.box(I("dark"), cx - r + 3.2, cx + r - 3.2, YN - 1.25, YN - 1.15, 0, TR - 1.6)
        ik.box(I("stock"), cx - 2.5, cx + 1.5, YN - 4.5, YN - 1.2, 0, 3.0)        # brick hearth
        ik.box(I("forge"), cx - 1.8, cx + 0.8, YN - 4.0, YN - 1.6, 3.0, 3.35)     # glowing fire bed
        ik.cyl(I("iron"), (cx - 0.5, YN - 2.8, 3.4), (cx - 0.5, YN - 2.8, CROWN - 1), 1.2, 10, True, 0.6)  # hood/flue
        ik.box(I("iron"), cx + 2.4, cx + 4.2, YS + 7.0, YS + 7.7, 2.0, 2.7)       # anvil
        ik.box(I("wood"), cx + 2.9, cx + 3.7, YS + 7.1, YS + 7.6, 0, 2.0)
        ik.box(I("tar"), cx - r, cx + r, ys + 0.05, ys + 0.3, TR, CROWN)               # boarded tympanum
        lunette(ik, cx, ys - 0.02, TR + 0.6, 3.6, I("iron"), I("win"))
        ik.box(I(mat_b), cx - r, cx + r, ys, ys + 0.3, TR, TR + 0.6)
    else:
        # full boarded screen with double doors (and a wicket), transom, fanlight
        ik.box(I(mat_b), cx - r, cx + r, ys, ys + 0.3, 0, TR + 0.6)
        dw = 4.8 if use != "stable" else 3.0
        for side in (-1, 1):
            dx0 = cx + (0 if side > 0 else -dw); dx1 = dx0 + dw
            ik.box(I("door"), dx0 + 0.15, dx1 - 0.15, ys - 0.12, ys, 0.1, TR - 1.5)
            # ledges and braces
            for zz in (1.2, (TR - 1.5) / 2, TR - 2.6):
                ik.box(I("door"), dx0 + 0.25, dx1 - 0.25, ys - 0.22, ys - 0.12, zz, zz + 0.55)
            ik.bar(I("door"), (dx0 + 0.5, ys - 0.2, 1.6), (dx1 - 0.5, ys - 0.2, (TR - 1.5) / 2 + 0.2), 0.5, 0.1)
            ik.box(I("iron"), dx0 + (dw * 0.75 if side < 0 else 0.3), dx0 + (dw * 0.75 if side < 0 else 0.3) + 0.9, ys - 0.26, ys - 0.2, 2.6, 2.75)  # strap hinge
        if use == "stable":   # half-doors, top leaf open onto a dark interior
            ik.box(I("dark"), cx - 2.8, cx + 2.8, ys - 0.13, ys - 0.05, 4.5, TR - 1.7)
        # small-pane side windows
        for sx in (-1, 1):
            wx = cx + sx * 7.0
            ik.box(I("win"), wx - 1.3, wx + 1.3, ys - 0.06, ys - 0.02, 5.0, 8.5)
            for t in range(4):
                ik.box(I("sash"), wx - 1.35, wx + 1.35, ys - 0.12, ys - 0.06, 5.0 + t * 1.165 - 0.06, 5.0 + t * 1.165 + 0.06)
            for t in range(3):
                ik.box(I("sash"), wx - 1.35 + t * 1.3 - 0.06, wx - 1.35 + t * 1.3 + 0.06, ys - 0.12, ys - 0.06, 4.95, 8.55)
        ik.box(I("tar"), cx - r, cx + r, ys + 0.05, ys + 0.3, TR + 0.6, CROWN)       # boarded tympanum
        lunette(ik, cx, ys - 0.02, TR + 0.6, 4.2, I("sash" if use == "workshop" else "iron"), I("win"))
    # sign board (blank / weathered: no invented firm names)
    if use == "workshop":
        ik.box(I("wood"), cx - 4.5, cx + 4.5, ys - 0.35, ys - 0.15, TR - 1.2, TR - 0.1)
ik.done("LN2_ArchInfills", IND)

# ================================================================ TERRACE (continuous two-up two-down row, north lane)
tk = K(); info["terraces"] = 0
TX0, FRONT, NH = -110.0, 14.0, 13; TY = 22.0; DEP = 26.0; EAVES = 19.0; RIDGE = 25.5
for i in range(NH):
    x = TX0 + i * FRONT; xm = x + FRONT / 2
    tk.box(I("house"), x, x + FRONT, TY, TY + DEP, 0, EAVES)
    # pitched slate roof (ridge parallel to street)
    tk.poly(I("slate"), [(x, TY - 0.8, EAVES), (x + FRONT, TY - 0.8, EAVES), (x + FRONT, TY + DEP / 2, RIDGE), (x, TY + DEP / 2, RIDGE)])
    tk.poly(I("slate"), [(x, TY + DEP / 2, RIDGE), (x + FRONT, TY + DEP / 2, RIDGE), (x + FRONT, TY + DEP + 0.8, EAVES), (x, TY + DEP + 0.8, EAVES)])
    tk.box(I("stone"), x, x + FRONT, TY - 0.35, TY, EAVES - 0.8, EAVES)        # gutter/eaves band
    # party-wall chimney stack with pots
    tk.box(I("house"), x - 1.4, x + 1.4, TY + DEP / 2 - 1.5, TY + DEP / 2 + 1.5, RIDGE - 2, RIDGE + 4.5)
    tk.box(I("stone"), x - 1.6, x + 1.6, TY + DEP / 2 - 1.7, TY + DEP / 2 + 1.7, RIDGE + 4.5, RIDGE + 4.9)
    for pp in (-0.7, 0.7):
        tk.cyl(I("pot"), (x + pp, TY + DEP / 2, RIDGE + 4.9), (x + pp, TY + DEP / 2, RIDGE + 6.6), 0.42, 10, True, 0.34)
    # door with fanlight, two sash windows up, one down
    dx = x + 1.5
    tk.box(I("door"), dx, dx + 3.2, TY - 0.15, TY - 0.02, 0.4, 7.2)
    tk.box(I("win"), dx + 0.2, dx + 3.0, TY - 0.08, TY - 0.03, 7.4, 8.6)
    tk.box(I("stone"), dx - 0.2, dx + 3.4, TY - 0.6, TY, 0, 0.4)               # step
    for (wx0, wz0, wz1) in ((x + 7.0, 2.6, 7.6), (x + 2.0, 10.5, 15.5), (x + 7.8, 10.5, 15.5)):
        ww = 3.6 if wx0 != x + 2.0 else 3.4
        tk.box(I("win"), wx0, wx0 + ww, TY - 0.08, TY - 0.03, wz0, wz1)
        tk.box(I("sash"), wx0 - 0.2, wx0 + ww + 0.2, TY - 0.18, TY - 0.08, wz0 - 0.2, wz0)
        tk.box(I("sash"), wx0 - 0.2, wx0 + ww + 0.2, TY - 0.18, TY - 0.08, wz1, wz1 + 0.2)
        tk.box(I("sash"), wx0 - 0.2, wx0, TY - 0.18, TY - 0.08, wz0, wz1)
        tk.box(I("sash"), wx0 + ww, wx0 + ww + 0.2, TY - 0.18, TY - 0.08, wz0, wz1)
        tk.box(I("sash"), wx0, wx0 + ww, TY - 0.16, TY - 0.08, (wz0 + wz1) / 2 - 0.08, (wz0 + wz1) / 2 + 0.08)   # meeting rail
        tk.box(I("sash"), wx0 + ww / 2 - 0.05, wx0 + ww / 2 + 0.05, TY - 0.14, TY - 0.08, wz0, wz1)
        tk.box(I("stone"), wx0 - 0.3, wx0 + ww + 0.3, TY - 0.45, TY, wz0 - 0.45, wz0 - 0.2)       # sill
        tk.box(I("ring"), wx0 - 0.25, wx0 + ww + 0.25, TY - 0.05, TY, wz1 + 0.2, wz1 + 0.9)    # gauged lintel
    info["terraces"] += 1
tk.done("LN2_Terraces", IND)
# smoke wisps from terrace chimneys (coal fires)
info["chimney_pots"] = NH * 2

# ================================================================ MILL / FACTORY (beyond the terrace, north lane)
fk = K(); info["chimneys"] = 0
MX0, MX1, MY0, MY1, MH = 74.0, 170.0, 26.0, 72.0, 62.0
fk.box(I("mill"), MX0, MX1, MY0, MY1, 0, MH)
fk.box(I("slate"), MX0 - 1, MX1 + 1, MY0 - 1, MY1 + 1, MH, MH + 1.2)
fk.poly(I("slate"), [(MX0 - 1, MY0 - 1, MH + 1.2), (MX1 + 1, MY0 - 1, MH + 1.2), (MX1 + 1, (MY0 + MY1) / 2, MH + 9), (MX0 - 1, (MY0 + MY1) / 2, MH + 9)])
fk.poly(I("slate"), [(MX0 - 1, (MY0 + MY1) / 2, MH + 9), (MX1 + 1, (MY0 + MY1) / 2, MH + 9), (MX1 + 1, MY1 + 1, MH + 1.2), (MX0 - 1, MY1 + 1, MH + 1.2)])
for zi in range(5):           # five storeys of iron-framed small-pane mill windows (all four faces)
    z0 = 4 + zi * 11.6
    for xi in range(16):
        wx = MX0 + 3 + xi * 5.9
        for yy, sgn in ((MY0, -1), (MY1, 1)):
            fk.box(I("win"), wx, wx + 3.2, yy + sgn * 0.05 - 0.03, yy + sgn * 0.05 + 0.03, z0, z0 + 6.4)
            fk.box(I("stone"), wx - 0.2, wx + 3.4, yy + sgn * 0.25 - 0.2, yy + sgn * 0.25 + 0.2, z0 - 0.4, z0)
    for yi in range(7):
        wy = MY0 + 3 + yi * 6.2
        for xx, sgn in ((MX0, -1), (MX1, 1)):
            fk.box(I("win"), xx + sgn * 0.05 - 0.03, xx + sgn * 0.05 + 0.03, wy, wy + 3.2, z0, z0 + 6.4)
# engine house + boiler house
fk.box(I("mill"), MX1, MX1 + 26, MY0 + 6, MY0 + 30, 0, 34)
fk.box(I("slate"), MX1 - 0.5, MX1 + 26.5, MY0 + 5.5, MY0 + 30.5, 34, 35.5)
for (cx_, cy_, hh, rb, rt, octo) in [(MX1 + 14, MY0 + 46, 140.0, 6.5, 3.6, False), (MX0 + 20, MY1 + 26, 118.0, 5.5, 3.2, True),
                                     (190.0, 300.0, 150.0, 7.0, 3.8, False), (-40.0, 230.0, 105.0, 5.0, 3.0, True),
                                     (140.0, 410.0, 160.0, 7.5, 4.0, False), (60.0, 420.0, 130.0, 6.0, 3.4, False)]:
    seg = 8 if octo else 18
    fk.box(I("mill"), cx_ - rb - 1.5, cx_ + rb + 1.5, cy_ - rb - 1.5, cy_ + rb + 1.5, 0, 14)             # pedestal
    fk.cyl(I("mill"), (cx_, cy_, 14), (cx_, cy_, hh), rb, seg, True, rt)                                    # tapering shaft
    fk.cyl(I("stone"), (cx_, cy_, hh - 3), (cx_, cy_, hh - 1.5), rt + 0.9, seg, True, rt + 0.9)            # cap band
    fk.cyl(I("mill"), (cx_, cy_, hh - 1.5), (cx_, cy_, hh + 1.2), rt + 0.6, seg, True, rt + 0.3)
    info["chimneys"] += 1
# distant mixed roofs and warehouses (so the skyline is a town, not a void)
for j in range(17):
    bx = -230 + j * 24 + R.uniform(-6, 6); by = R.uniform(110, 330); bh = R.uniform(28, 62)
    fk.box(I(R.choice(["mill", "house", "stock"])), bx, bx + R.uniform(18, 34), by, by + R.uniform(20, 50), 0, bh)
fk.box(I("stock"), 236, 262, 6, 60, 0, 44)            # warehouse closing the north lane vista
fk.done("LN2_Factory", IND)

# ================================================================ TRAIN (c.1847-50 2-2-2 express type, no cab; tender; 4-wheel carriages)
trk = K(); info["train"] = 1
yc = -2.6; zr = RAIL
LX = 56.0                   # leading buffer beam (train heading -x, toward the city)
# loco frame + footplate
trk.box(I("iron"), LX, LX + 21, yc - 3.4, yc + 3.4, zr + 3.4, zr + 3.9)
trk.cyl(I("loco"), (LX + 2.2, yc, zr + 7.0), (LX + 13.5, yc, zr + 7.0), 2.0, 20)       # boiler barrel
trk.cyl(I("iron"), (LX + 0.8, yc, zr + 6.8), (LX + 2.4, yc, zr + 6.8), 2.25, 20)      # smokebox
trk.box(I("loco"), LX + 13.5, LX + 17.5, yc - 2.2, yc + 2.2, zr + 3.9, zr + 9.0)     # firebox
ellipsoid(trk, I("brass"), (LX + 15.5, yc, zr + 9.2), (2.0, 2.2, 1.6))                 # haycock firebox dome (brass)
trk.cyl(I("brass"), (LX + 9.0, yc, zr + 8.6), (LX + 9.0, yc, zr + 10.4), 0.85, 14, True, 0.7)   # steam dome
trk.cyl(I("iron"), (LX + 1.6, yc, zr + 8.6), (LX + 1.6, yc, zr + 13.4), 0.75, 14, True, 0.85)   # tall chimney
trk.cyl(I("iron"), (LX + 1.6, yc, zr + 13.4), (LX + 1.6, yc, zr + 13.9), 1.15, 14)               # copper-cap rim
trk.box(I("iron"), LX + 17.4, LX + 17.6, yc - 3.2, yc + 3.2, zr + 3.9, zr + 10.0)    # weatherboard only (no cab, 1850)
trk.box(I("win"), LX + 17.35, LX + 17.65, yc - 2.4, yc - 0.9, zr + 8.0, zr + 9.3)
for wx_, rr in ((LX + 3.5, 2.0), (LX + 9.5, 3.0), (LX + 16.0, 2.0)):                  # 4 ft / 6 ft / 4 ft wheels
    for ss in (-1, 1):
        trk.wheel(I("iron"), (wx_, yc + ss * 2.35, zr + rr), "y", rr, 0.4, 0.35, 12)
trk.box(I("loco"), LX + 6.3, LX + 12.7, yc - 3.4, yc - 2.8, zr + 3.9, zr + 6.3)      # splashers
trk.box(I("loco"), LX + 6.3, LX + 12.7, yc + 2.8, yc + 3.4, zr + 3.9, zr + 6.3)
trk.box(I("wheelred"), LX - 0.6, LX + 0.2, yc - 3.4, yc + 3.4, zr + 2.6, zr + 4.0)    # buffer beam
# tender
TX = LX + 22.5
trk.box(I("loco"), TX, TX + 15, yc - 3.3, yc + 3.3, zr + 3.4, zr + 8.2)
trk.box(I("coal"), TX + 1, TX + 9, yc - 2.8, yc + 2.8, zr + 8.2, zr + 9.0)
for wx_ in (TX + 3, TX + 12):
    for ss in (-1, 1): trk.wheel(I("iron"), (wx_, yc + ss * 2.35, zr + 1.8), "y", 1.8, 0.35, 0.3, 10)
# carriages: 1st class (3-compartment, panelled), 2nd, 2nd
cxs = TX + 16.5
for ci in range(4):
    L = 21.0; x = cxs + ci * (L + 2.5)
    trk.box(I("carriage"), x, x + L, yc - 3.6, yc + 3.6, zr + 3.6, zr + 10.6)
    trk.box(I("iron"), x - 0.3, x + L + 0.3, yc - 3.9, yc + 3.9, zr + 10.6, zr + 11.3)              # roof
    ellipsoid(trk, I("iron"), (x + L / 2, yc, zr + 11.2), (L / 2 + 0.2, 3.9, 0.6))
    for d in range(3):          # compartment doors + droplights, quarter lights
        dx0 = x + 1.5 + d * 6.6
        for ys_, sgn in ((yc - 3.6, -1), (yc + 3.6, 1)):
            trk.box(I("win"), dx0 + 1.0, dx0 + 3.2, ys_ + sgn * 0.02 - 0.02, ys_ + sgn * 0.02 + 0.02, zr + 7.3, zr + 9.6)
            trk.box(I("win"), dx0 + 3.9, dx0 + 5.6, ys_ + sgn * 0.02 - 0.02, ys_ + sgn * 0.02 + 0.02, zr + 7.6, zr + 9.6)
            trk.box(I("brass"), dx0 + 3.4, dx0 + 3.6, ys_ + sgn * 0.06 - 0.03, ys_ + sgn * 0.06 + 0.03, zr + 6.4, zr + 6.9)
    if ci == 0:  # luggage under tarpaulin on the roof (common c.1850)
        trk.box(I("canvas"), x + 4, x + 16, yc - 2.5, yc + 2.5, zr + 11.3, zr + 12.6)
    for wx_ in (x + 4, x + L - 4):
        for ss in (-1, 1): trk.wheel(I("iron"), (wx_, yc + ss * 2.35, zr + 1.75), "y", 1.75, 0.35, 0.3, 10)
trk.done("LN2_Train", IND)

# ================================================================ GAS LAMPS (cast-iron columns, square lanterns)
lk = K(); info["gas_lamps"] = 0
def gas_lamp(k, x, y):
    k.cyl(I("ironp"), (x, y, 0.42), (x, y, 1.6), 0.55, 10, True, 0.42)               # base
    k.cyl(I("ironp"), (x, y, 1.6), (x, y, 2.0), 0.32, 10, True, 0.25)
    k.cyl(I("ironp"), (x, y, 2.0), (x, y, 9.0), 0.24, 10, True, 0.16)                # tapering column
    k.cyl(I("ironp"), (x, y, 7.6), (x, y, 7.9), 0.24, 10)                            # collar
    k.bar(I("ironp"), (x - 1.3, y, 8.2), (x + 1.3, y, 8.2), 0.12, 0.12)               # ladder bar
    k.cyl(I("ironp"), (x, y, 9.0), (x, y, 9.4), 0.38, 8, True, 0.38)                 # lantern seat
    # square tapered lantern: glazed sides + iron corner posts + pyramid hood and finial
    s0, s1, z0, z1 = 0.62, 0.85, 9.4, 11.2
    for (ax, ay, bx, by) in ((-1, -1, 1, -1), (1, -1, 1, 1), (1, 1, -1, 1), (-1, 1, -1, -1)):
        k.poly(I("lampglass"), [(x + ax * s0, y + ay * s0, z0), (x + bx * s0, y + by * s0, z0), (x + bx * s1, y + by * s1, z1), (x + ax * s1, y + ay * s1, z1)])
        k.bar(I("ironp"), (x + ax * s0, y + ay * s0, z0), (x + ax * s1, y + ay * s1, z1), 0.09, 0.09)
    k.poly(I("ironp"), [(x - 1.0, y - 1.0, z1), (x + 1.0, y - 1.0, z1), (x, y, z1 + 0.9)]); k.poly(I("ironp"), [(x + 1.0, y - 1.0, z1), (x + 1.0, y + 1.0, z1), (x, y, z1 + 0.9)])
    k.poly(I("ironp"), [(x + 1.0, y + 1.0, z1), (x - 1.0, y + 1.0, z1), (x, y, z1 + 0.9)]); k.poly(I("ironp"), [(x - 1.0, y + 1.0, z1), (x - 1.0, y - 1.0, z1), (x, y, z1 + 0.9)])
    k.cyl(I("ironp"), (x, y, z1 + 0.85), (x, y, z1 + 1.5), 0.12, 6, True, 0.03)
for (lx, ly) in ((-14.0, -9.4), (42.0, -9.4), (98.0, -9.4), (158.0, -9.4), (-60.0, -9.4),
                 (14.0, -45.2), (74.0, -45.2), (-46.0, -45.2), (6.0, 18.4), (60.0, 18.4), (-50.0, 18.4)):
    gas_lamp(lk, lx, ly); info["gas_lamps"] += 1
lk.done("LN2_GasLamps", IND)

# ================================================================ HORSE + DRAY (brewer's/coal dray, two horses would be typical; one here)
def horse(k, x, y, heading, mat_body="horse", stride=0.0):
    """~16 hands (5 ft 4 in at withers) draught horse built from ellipsoids/tubes in local coords, then placed.
    local +x = forward."""
    hk_ = Kit(ML)
    ellipsoid(hk_, I(mat_body), (0, 0, 4.25), (3.3, 1.35, 1.45))                      # barrel
    ellipsoid(hk_, I(mat_body), (2.3, 0, 4.55), (1.5, 1.3, 1.5))                       # chest/shoulder
    ellipsoid(hk_, I(mat_body), (-2.4, 0, 4.6), (1.4, 1.35, 1.35))                     # hindquarters
    tube(hk_, I(mat_body), [(2.4, 0, 4.9, 1.1), (3.2, 0, 5.9, 0.9), (3.85, 0, 6.75, 0.64), (4.2, 0, 7.15, 0.5)], 0, 14)   # neck (arched, thick)
    tube(hk_, I(mat_body), [(4.22, 0, 7.22, 0.47), (4.75, 0, 6.6, 0.42), (5.3, 0, 5.95, 0.33), (5.58, 0, 5.62, 0.29)], 0, 12)  # long head, nose down
    ellipsoid(hk_, I(mat_body), (4.45, 0, 6.72), (0.62, 0.46, 0.55), (0, math.radians(-40), 0))                       # jowl
    ellipsoid(hk_, I(mat_body), (5.5, 0, 5.66), (0.36, 0.33, 0.33))                                                   # muzzle
    tube(hk_, I("horsedk"), [(2.5, 0, 6.05, 0.16), (3.35, 0, 6.85, 0.2), (4.1, 0, 7.6, 0.16)], 0, 8)                   # mane crest
    for ex in (-0.24, 0.24): hk_.cyl(I(mat_body), (4.18, ex, 7.5), (4.02, ex * 1.25, 8.12), 0.13, 6, True, 0.02)        # ears
    for ex in (-0.5, 0.5): hk_.box(I("harness"), 4.55, 5.05, ex - 0.04, ex + 0.04, 6.55, 7.05)                      # blinkers
    hk_.bar(I("harness"), (4.3, 0, 7.25), (5.45, 0, 5.85), 0.12, 0.84)                                                 # bridle
    # draught collar (leather roll around the base of the neck) + brass-topped hames
    cc_ = Vector((2.95, 0, 5.55)); Nn = Vector((-0.78, 0, 0.62)); Yy = Vector((0, 1, 0)); ring = []
    for j in range(17):
        a_ = 2 * math.pi * j / 16; ring.append(cc_ + Yy * (math.cos(a_) * 1.18) + Nn * (math.sin(a_) * 1.42))
    for p0, p1 in zip(ring, ring[1:]): hk_.cyl(I("harness"), tuple(p0), tuple(p1), 0.3, 8)
    for ex in (-0.45, 0.45): hk_.cyl(I("brass"), (2.4 + 0.1, ex, 6.6), (2.35, ex * 1.1, 7.25), 0.09, 6, True, 0.12)
    tube(hk_, I("horsedk"), [(-3.6, 0, 5.0, 0.28), (-4.1, 0, 3.6, 0.32), (-4.0, 0, 2.2, 0.2)], 0, 8)   # tail
    for (lx, ly, front, ph) in ((2.3, 0.65, True, 0.0), (2.0, -0.65, True, 1.0), (-2.5, 0.65, False, 1.0), (-2.8, -0.65, False, 0.0)):
        sw = stride * (1 if ph else -1)
        if front:
            pts = [(lx, ly, 3.6, 0.42), (lx + 0.05 + sw * 0.3, ly, 2.2, 0.26), (lx + sw * 0.6, ly, 0.9, 0.2), (lx + sw * 0.7, ly, 0.35, 0.28)]
        else:
            pts = [(lx, ly, 3.7, 0.5), (lx - 0.45 + sw * 0.2, ly, 2.4, 0.3), (lx - 0.1 + sw * 0.5, ly, 1.0, 0.2), (lx + sw * 0.6, ly, 0.35, 0.28)]
        tube(hk_, I(mat_body), pts, 0, 10)
        hk_.cyl(I("horsedk"), (pts[-1][0], ly, 0.0), (pts[-1][0], ly, 0.55), 0.38, 10, True, 0.33)      # feathered hoof
    # harness: saddle pad, back band, breeching and traces
    hk_.box(I("harness"), -0.6, 0.4, -1.42, 1.42, 5.45, 5.75)
    hk_.bar(I("harness"), (-3.4, -1.36, 4.4), (0.0, -1.42, 4.3), 0.2, 0.06); hk_.bar(I("harness"), (-3.4, 1.36, 4.4), (0.0, 1.42, 4.3), 0.2, 0.06)
    hk_.bar(I("harness"), (2.2, -1.25, 4.6), (-1.0, -1.42, 4.6), 0.18, 0.05); hk_.bar(I("harness"), (2.2, 1.25, 4.6), (-1.0, 1.42, 4.6), 0.18, 0.05)
    return hk_.done(f"LN2_Horse_{x:.0f}", IND, x, y, 0, heading, smooth=True)
def dray(k, x, y, heading):
    """4-wheel open dray, ~13 ft bed, loaded with barrels; shafts forward (local +x)."""
    dk = Kit(ML)
    dk.box(I("wood"), -13, 0, -2.9, 2.9, 3.0, 3.5)                              # bed
    dk.box(I("wheelred"), -13, 0, -3.0, -2.8, 3.5, 4.4); dk.box(I("wheelred"), -13, 0, 2.8, 3.0, 3.5, 4.4)   # raves
    for (wx_, rr) in ((-2.2, 1.6), (-10.5, 2.3)):
        for ss in (-1, 1): dk.wheel(I("wheelred"), (wx_, ss * 3.35, rr), "y", rr, 0.3, 0.28, 12)
    for ss in (-1, 1): dk.bar(I("wood"), (0, ss * 1.5, 3.5), (10.5, ss * 1.5, 4.7), 0.3, 0.3)       # shafts
    for (bx, by, lay) in ((-2.5, -1.3, 0), (-2.5, 1.3, 0), (-5.6, -1.3, 0), (-5.6, 1.3, 0), (-8.7, -1.3, 0), (-8.7, 1.3, 0), (-4.1, 0, 1), (-7.2, 0, 1)):
        z0 = 3.5 + lay * 2.4
        dk.cyl(I("barrel"), (bx - 1.4, by, z0 + 1.25), (bx - 0.7, by, z0 + 1.25), 1.15, 14, True, 1.3)
        dk.cyl(I("barrel"), (bx - 0.7, by, z0 + 1.25), (bx + 0.7, by, z0 + 1.25), 1.3, 14, True, 1.3)
        dk.cyl(I("barrel"), (bx + 0.7, by, z0 + 1.25), (bx + 1.4, by, z0 + 1.25), 1.3, 14, True, 1.15)
        for hx in (-1.0, 1.0): dk.cyl(I("iron"), (bx + hx - 0.06, by, z0 + 1.25), (bx + hx + 0.06, by, z0 + 1.25), 1.29, 14)
    dk.box(I("wood"), -1.0, 0.0, -2.0, 2.0, 3.5, 6.2)                           # driver's seat box
    return dk.done(f"LN2_Dray_{x:.0f}", IND, x, y, 0, heading)
info["horses"] = 0
H1 = horse(None, 6.0, -19.0, math.pi, stride=0.35); D1 = dray(None, 14.5 + 0.0, -19.0, math.pi)
# second horse in tandem? keep single; costermonger's barrow + a parked coal cart far right
H2 = horse(None, 92.0, -27.0, 0.0, "horsedk", stride=0.0); D2 = dray(None, 83.5, -27.0, 0.0)
info["horses"] = 2

# ---- street dressing: barrels, crates, cart wheels against the arches, coal sacks, a handbarrow, puddles
sk = K()
for (bx, by) in ((-27.5, -8.1), (-25.2, -8.4), (-26.4, -7.9), (33.0, -8.0), (35.2, -8.2), (67.5, -8.1)):
    sk.cyl(I("barrel"), (bx, by, 0.42), (bx, by, 1.0), 1.0, 14, True, 1.15); sk.cyl(I("barrel"), (bx, by, 1.0), (bx, by, 2.6), 1.15, 14, True, 1.15)
    sk.cyl(I("barrel"), (bx, by, 2.6), (bx, by, 3.2), 1.15, 14, True, 1.0)
    for hz in (0.9, 2.7): sk.cyl(I("iron"), (bx, by, hz - 0.06), (bx, by, hz + 0.06), 1.17, 14)
for (bx, by, w_, h_) in ((-20.5, -8.4, 2.6, 2.0), (-19.2, -8.0, 2.0, 1.6), (37.5, -8.3, 3.0, 2.4), (69.8, -8.2, 2.4, 2.0)):
    sk.box(I("crate"), bx - w_ / 2, bx + w_ / 2, by - 1.0, by + 1.0, 0.42, 0.42 + h_)
for (wx_, wy_) in ((14.0, -7.2), (16.8, -7.4)):   # wheelwright: wheels leaning on the smithy front
    sk.wheel(I("wheelred"), (wx_, wy_, 2.35), "y", 2.3, 0.25, 0.25, 12)
# handbarrow
sk.box(I("wood"), 48, 53, -14.6, -12.4, 1.6, 1.9); sk.bar(I("wood"), (53, -14.2, 1.8), (56, -14.2, 2.4), 0.2); sk.bar(I("wood"), (53, -12.8, 1.8), (56, -12.8, 2.4), 0.2)
sk.wheel(I("wood"), (48.6, -13.5, 1.2), "y", 1.2, 0.15, 0.15, 8)
sk.box(I("crate"), 48.4, 50.6, -14.4, -12.6, 1.9, 3.0); sk.box(I("canvas"), 50.8, 52.8, -14.4, -12.6, 1.9, 2.6)
# dung + puddles (dark glossy)
puddle = mat_plain("Puddle", (0.02, 0.022, 0.025), 0.05); ML.append(puddle); IX["puddle"] = len(ML) - 1
for (px, py, rx, ry) in ((-6, -26, 5, 2.2), (30, -31, 7, 2.5), (58, -21, 4, 1.8), (2, -14, 3, 1.4)):
    pk = Kit([puddle]); seg = 18
    pk.poly(0, [(px + rx * math.cos(2 * math.pi * j / seg) * (1 + 0.15 * math.sin(3 * j)), py + ry * math.sin(2 * math.pi * j / seg), 0.03) for j in range(seg)])
    pk.done(f"LN2_Puddle_{px}", IND)
sk.done("LN2_StreetDressing", IND)

# ================================================================ SMOKE (volumetric: coal smoke from mill chimneys, loco exhaust, house chimneys) + smog
def plume(name, base, rise, drift, n, r0, r1, mat, seed):
    rng = random.Random(seed)
    for s in range(n):
        t = s / max(1, n - 1)
        c = Vector(base) + Vector(drift) * t + Vector((0, 0, rise * (t ** 0.8)))
        r = r0 + (r1 - r0) * t
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1.0, location=tuple(ft(v) for v in c))
        o = bpy.context.active_object; o.name = f"{name}_{s:02d}"
        o.scale = (ft(r) * rng.uniform(1.0, 1.35), ft(r) * rng.uniform(0.85, 1.15), ft(r) * rng.uniform(0.7, 0.95))
        o.rotation_euler = (0, 0, rng.uniform(0, 6.28)); o.data.materials.append(mat)
        for cc in o.users_collection: cc.objects.unlink(o)
        SMK.objects.link(o); o.visible_shadow = True
coal = mat_volume("CoalSmoke", (0.10, 0.095, 0.09), 1.2, 0.25, noise_scale=1.6, falloff=True)
steam = mat_volume("LocoSteam", (0.80, 0.79, 0.76), 3.0, 0.4, noise_scale=1.9, falloff=True)
wisp = mat_volume("HearthSmoke", (0.30, 0.29, 0.27), 0.5, 0.2, noise_scale=2.4, falloff=True)
plume("LN2_SmokeMillA", (MX1 + 14, MY0 + 46, 143), 70, (120, 70, 0), 12, 6, 34, coal, 1)
plume("LN2_SmokeMillB", (MX0 + 20, MY1 + 26, 121), 55, (110, 80, 0), 11, 5, 30, coal, 2)
plume("LN2_SmokeFarA", (190, 300, 152), 60, (120, 90, 0), 8, 9, 40, coal, 3)
plume("LN2_SmokeFarB", (-40, 230, 108), 50, (110, 60, 0), 8, 7, 34, coal, 4)
plume("LN2_SmokeLoco", (LX + 1.6, yc, RAIL + 15.5), 9, (70, -4, 0), 12, 2.0, 11, steam, 5)
for i in range(0, NH, 2):
    x = TX0 + i * FRONT
    plume(f"LN2_SmokeHouse{i}", (x, TY + DEP / 2, RIDGE + 7.5), 16, (22, 10, 0), 4, 1.2, 5.5, wisp, 10 + i)
info["smoke_plumes"] = 5 + (NH + 1) // 2
# smog: thin homogeneous warm-grey scattering volume over the industry set only (stops at x=268 ft: CP005 room at 286-314 is outside)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ft(15), ft(140), ft(80)))
sm = bpy.context.active_object; sm.name = "LN2_Smog"; sm.scale = (ft(506), ft(620), ft(160))
smog = mat_volume("Smog", (0.30, 0.28, 0.25), 0.0028, 0.35); sm.data.materials.append(smog)
for cc in sm.users_collection: cc.objects.unlink(sm)
SMK.objects.link(sm); sm.visible_shadow = False

# ================================================================ PEOPLE (modelled 1850 dress: vendored cp002_figures.py; names avoid
# people_lib figure prefixes/part_kind so the render-time v3 swap leaves them alone)
import cp002_figures as F
def face_rz(dx, dy): return math.atan2(dx, -dy)       # figures face local -y
CAST = [  # (tag, builder, role, palette, pose, H m, hat, x ft, y ft, facing dx, dy, extra)
    ("smith_at_arch", "m", "workman", "coalheaver", "working", 1.72, "cap", 12.6, -8.8, -0.2, -1, {}),
    ("wheelwright", "m", "workman", "navvy", "standing", 1.75, "wide", 18.6, -9.0, -1, -0.4, {}),
    ("coster_barrow", "m", "workman", "costermonger", "hauling", 1.68, "cap", 56.4, -13.5, 1, 0, {}),
    ("woman_basket", "w", None, "woman_a", None, 1.58, "bonnet", -2.0, -8.5, 1, 0.05, {"basket": True}),
    ("woman_shawl", "w", None, "woman_c", None, 1.55, "shawl", -21.8, -8.7, 0.4, -1, {"apron": True}),
    ("clerk_walking", "m", "foreman", "clerk", "standing", 1.74, "top", 25.0, -8.6, -1, 0, {}),
    ("gent_crossing", "m", "engineer", "gent", "standing", 1.78, "top", -9.5, -26.0, 1, 0.25, {}),
    ("woman_crossing", "w", None, "woman_b", None, 1.60, "bonnet", -7.4, -27.2, 1, 0.25, {}),
    ("carter_at_head", "m", "carter", "carter", "hauling", 1.74, "wide", 3.2, -21.6, -1, 0, {}),
    ("navvy_lounging", "m", "workman", "navvy", "standing", 1.80, "wide", 36.4, -10.2, -0.3, -1, {}),
    ("coalheaver_sack", "m", "workman", "coalheaver", "hauling", 1.73, "cap", 64.0, -8.8, -1, 0, {}),
    ("woman_far", "w", None, "woman_c", None, 1.57, "shawl", 79.0, -8.7, -1, 0, {}),
    ("drayman_far", "m", "carter", "carter", "standing", 1.75, "wide", 95.5, -24.5, 0, -1, {}),
    # north lane, seen through the open arches
    ("woman_doorstep", "w", None, "woman_a", None, 1.56, "shawl", -4.0, 20.2, 0, -1, {"apron": True}),
    ("worker_north", "m", "workman", "navvy", "standing", 1.74, "cap", 3.0, 12.0, -1, 0, {}),
    ("clerk_north", "m", "foreman", "clerk", "standing", 1.72, "top", 57.0, 13.5, 1, 0, {}),
    ("woman_north", "w", None, "woman_b", None, 1.58, "bonnet", 63.5, 20.3, 0, -1, {}),
]
info["figures"] = 5
for i, (tag, bld, role, pal, pose, H, hat, x, y, dx, dy, ex) in enumerate(CAST):
    nm = f"LN2_Folk_{i:02d}"
    mats = F.palette_street(f"ln2_{i}", pal)
    if bld == "m": o = F.build_figure(nm, role, H, pose, seed=200 + i, mats=mats, hat=hat)
    else: o = F.build_woman(nm, H, seed=200 + i, mats=mats, headwear=hat, **ex)
    zf = 0.42 if (y < -44 or -10.6 < y < -6 or 19 < y < 22) else 0.0
    o.location = (ft(x), ft(y), ft(zf)); o.rotation_euler = (0, 0, face_rz(dx, dy)); FIGC.objects.link(o)
    o["cp002_figure"] = f"{tag}/{bld}/{role}/{pal}/{pose}/{hat}/{H}"
    info["figures"] += 1

# ---------------------------------------------------------------- render settings for volumes (exposure / world / sun untouched)
sc.cycles.volume_step_rate = 2.0; sc.cycles.volume_max_steps = 256; sc.cycles.volume_bounces = 1
sc["grok_build"] = json.dumps({"set": "O-LONDON ln03_cp002 CANDIDATE (CP002 1850 railway lane)", "seed": 1850, "info": info,
                               "base": "rounds/ln02.blend", "script": "scripts/build_cp002_street.py"})
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True, copy=True)
print("SAVED", OUT, info)
