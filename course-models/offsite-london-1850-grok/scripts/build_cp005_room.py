"""CANDIDATE ln03_cp005 — CP005 "An international ambition": a London committee/planning room, 1849 - January 1850.
Opens rounds/ln02.blend (live for CP005, read-only), replaces the PLANNING_ROOM set and its five figures, and saves a NEW
file. The ln02 INDUSTRY set (x <= 160 ft), world, sun, exposure (-0.10) and the CP005 cameras are untouched.

blender -b rounds/ln02.blend -P scripts/build_cp005_room.py -- --out rounds/candidates/ln03_cp005.blend

Dated state: London, winter 1849-50, before the Royal Commission (3 Jan 1850) and before any building design exists
(Paxton's scheme: June 1850). Interpretive composite room; no portrait likeness; no legible wording (storyboard CP005).
Dimension sources (logged as D-LN-CP005-xx in DEPARTURES.md):
  Room 28 x 22 x 12 ft kept (LN03). First-floor London town-house room: 6-over-6 timber sashes in openings ~3 ft 8 in
  wide, window board at dado height ~3 ft, heads ~10 ft 4 in; panelled folding shutters in the reveals; wall ~14 in
  (1 1/2 brick) thick; skirting ~9 in, dado rail ~3 ft, plaster cornice ~7 in deep (Georgian/early-Victorian London
  house practice: Survey of London house descriptions; Cruickshank & Wyld, London: The Art of Georgian Building).
  Crown-glass panes ~11 x 16 in. Metropolitan Building Act 1844: new streets >= 40 ft wide (here 58 ft face to face).
  Opposite terrace: 4 storeys over a basement, 20 ft frontages, London stock brick over a stucco ground floor.
  Committee table 10 x 6 ft (LN03), green baize top; chairs seat 18 in; men bareheaded indoors (period etiquette).
"""
import bpy, bmesh, sys, os, math, random, json
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grokkit as G
from grokkit import ft, Kit
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "/tmp/ln03_cp005.blend"
TEX = os.path.join(HERE, "..", "textures")
R = random.Random(1849)
sc = bpy.context.scene
RX = 300.0
X0, X1, Y0, Y1, CEIL = RX - 14, RX + 14, -11.0, 11.0, 12.0        # inner faces of the room (unchanged)
WALL_T = 1.15                                                     # 14 in wall
WX = (297.0, 304.0, 311.0)                                        # window centres on the +y (street) wall
WW, SILL, HEAD = 3.67, 3.0, 10.35                                 # 3 ft 8 in openings, board at dado height
STREET_Z = -30.0                                                  # room is a first-floor room over a ground floor + mezzanine/basement
FACE_Y = Y1 + WALL_T + 58.0                                       # opposite terrace face (58 ft face to face, >= 40 ft Act of 1844)

# ---------------------------------------------------------------- remove the ln02 PLANNING_ROOM set + its five lathe figures
old = ["LN_Room_shell", "LN_CommissionTable", "LN_Samples", "LN_Fireplace", "LN_Bookshelf"] + \
      [o.name for o in bpy.data.objects if o.name.startswith(("LN_Chair_", "LN_Plan_", "LN_WallPlan_", "LN_Comm_"))]
removed = []
for nm in old:
    o = bpy.data.objects.get(nm)
    if o: bpy.data.objects.remove(o, do_unlink=True); removed.append(nm)
ROOM = bpy.data.collections.get("PLANNING_ROOM"); FIGC = bpy.data.collections.get("LN_FIGURES")
OUTC = G.coll("LN3_ROOM_OUTSIDE", ROOM)
binfo = json.loads(sc.get("grok_build", "{}")); info = dict(binfo.get("info", {}))
info["figures"] = info.get("figures", 0) - sum(1 for n in removed if n.startswith("LN_Comm_"))
for k in ("table", "plans", "samples"): info[k] = 0

# ---------------------------------------------------------------- materials (tagged cpl_mat_v1: the survey grit pass skips them)
def _nt(name):
    M = bpy.data.materials.new("LN3_" + name); M.use_nodes = True; nt = M.node_tree
    b = nt.nodes["Principled BSDF"]; M["cpl_mat_v1"] = 1
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.3
    return M, nt, b
def _pos(nt):
    g = nt.nodes.new("ShaderNodeNewGeometry"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(g.outputs["Position"], sp.inputs[0]); return g, sp
def _noise(nt, vec, scale, detail=6.0, rough=0.55):
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = detail
    n.inputs["Roughness"].default_value = rough
    if vec is not None: nt.links.new(vec, n.inputs["Vector"])
    return n.outputs["Fac"]
def _ramp(nt, fac, p0, p1, c0, c1):
    r = nt.nodes.new("ShaderNodeValToRGB"); nt.links.new(fac, r.inputs[0])
    e = r.color_ramp.elements; e[0].position = p0; e[1].position = p1; e[0].color = (*c0, 1); e[1].color = (*c1, 1)
    return r.outputs[0]
def _mixc(nt, a, b, fac):
    m = nt.nodes.new("ShaderNodeMix"); m.data_type = 'RGBA'
    if isinstance(fac, float): m.inputs["Factor"].default_value = fac
    else: nt.links.new(fac, m.inputs["Factor"])
    for s, v in ((m.inputs[6], a), (m.inputs[7], b)):
        if isinstance(v, tuple): s.default_value = (*v, 1)
        else: nt.links.new(v, s)
    return m.outputs[2]
def plain(name, c, rough=0.8, metal=0.0, noise=0.0, nscale=14.0, sheen=0.0, emit=None):
    M, nt, b = _nt(name); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if noise:
        g, sp = _pos(nt); col = _ramp(nt, _noise(nt, g.outputs["Position"], nscale), 0.3, 0.75, tuple(v * (1 - noise) for v in c), tuple(min(1, v * (1 + noise)) for v in c))
        nt.links.new(col, b.inputs["Base Color"])
    else: b.inputs["Base Color"].default_value = (*c, 1)
    if sheen and "Sheen Weight" in b.inputs: b.inputs["Sheen Weight"].default_value = sheen
    if emit: b.inputs["Emission Color"].default_value = (*emit[0], 1); b.inputs["Emission Strength"].default_value = emit[1]
    M.diffuse_color = (*c, 1); return M
def wallpaper():
    """drab 1840s paper: fine vertical stripe + small sprig (noise), slightly faded toward the windows"""
    M, nt, b = _nt("Wallpaper"); g, sp = _pos(nt)
    w = nt.nodes.new("ShaderNodeTexWave"); w.wave_type = 'BANDS'; w.bands_direction = 'X'; w.inputs["Scale"].default_value = 1.0
    cb = nt.nodes.new("ShaderNodeCombineXYZ"); ad = nt.nodes.new("ShaderNodeMath"); ad.operation = 'ADD'
    nt.links.new(sp.outputs[0], ad.inputs[0]); nt.links.new(sp.outputs[1], ad.inputs[1]); nt.links.new(ad.outputs[0], cb.inputs[0])
    sc_ = nt.nodes.new("ShaderNodeVectorMath"); sc_.operation = 'SCALE'; sc_.inputs[3].default_value = 3.0 / ft(1.0) / 3.0
    nt.links.new(cb.outputs[0], sc_.inputs[0]); nt.links.new(sc_.outputs[0], w.inputs["Vector"])
    stripe = _ramp(nt, w.outputs["Fac"], 0.45, 0.6, (0.30, 0.27, 0.20), (0.36, 0.33, 0.25))
    vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 9.0; nt.links.new(g.outputs["Position"], vor.inputs["Vector"])
    sprig = _ramp(nt, vor.outputs["Distance"], 0.06, 0.12, (1, 1, 1), (0, 0, 0))
    col = _mixc(nt, stripe, (0.40, 0.25, 0.16), sprig)
    dirt = _ramp(nt, _noise(nt, g.outputs["Position"], 2.0), 0.35, 0.7, (0.85, 0.85, 0.85), (1, 1, 1))
    mm = nt.nodes.new("ShaderNodeMix"); mm.data_type = 'RGBA'; mm.blend_type = 'MULTIPLY'; mm.inputs["Factor"].default_value = 1.0
    nt.links.new(col, mm.inputs[6]); nt.links.new(dirt, mm.inputs[7]); nt.links.new(mm.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.85; M.diffuse_color = (0.34, 0.31, 0.23, 1); return M
def carpet():
    """Brussels/Turkey-pattern carpet: crimson ground, repeating dark-blue/gold lozenges (checker at 45 deg), worn noise"""
    M, nt, b = _nt("Carpet"); g, sp = _pos(nt)
    cb = nt.nodes.new("ShaderNodeCombineXYZ"); a1 = nt.nodes.new("ShaderNodeMath"); a1.operation = 'ADD'; s1 = nt.nodes.new("ShaderNodeMath"); s1.operation = 'SUBTRACT'
    for m_ in (a1, s1): nt.links.new(sp.outputs[0], m_.inputs[0]); nt.links.new(sp.outputs[1], m_.inputs[1])
    nt.links.new(a1.outputs[0], cb.inputs[0]); nt.links.new(s1.outputs[0], cb.inputs[1])
    ch = nt.nodes.new("ShaderNodeTexChecker"); ch.inputs["Scale"].default_value = 4.0; nt.links.new(cb.outputs[0], ch.inputs["Vector"])
    ch.inputs["Color1"].default_value = (0.15, 0.028, 0.022, 1); ch.inputs["Color2"].default_value = (0.10, 0.03, 0.025, 1)
    vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 5.6; nt.links.new(cb.outputs[0], vor.inputs["Vector"])
    gold = _ramp(nt, vor.outputs["Distance"], 0.07, 0.12, (1, 1, 1), (0, 0, 0))
    col = _mixc(nt, ch.outputs["Color"], (0.035, 0.05, 0.03), gold)
    v2 = nt.nodes.new("ShaderNodeTexVoronoi"); v2.inputs["Scale"].default_value = 11.2; nt.links.new(cb.outputs[0], v2.inputs["Vector"])
    col = _mixc(nt, col, (0.22, 0.15, 0.05), _ramp(nt, v2.outputs["Distance"], 0.03, 0.06, (1, 1, 1), (0, 0, 0)))
    wear = _ramp(nt, _noise(nt, g.outputs["Position"], 3.0), 0.3, 0.8, (0.8, 0.8, 0.8), (1.05, 1.05, 1.05))
    mm = nt.nodes.new("ShaderNodeMix"); mm.data_type = 'RGBA'; mm.blend_type = 'MULTIPLY'; mm.inputs["Factor"].default_value = 1.0
    nt.links.new(col, mm.inputs[6]); nt.links.new(wear, mm.inputs[7]); nt.links.new(mm.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.95
    if "Sheen Weight" in b.inputs: b.inputs["Sheen Weight"].default_value = 0.4
    M.diffuse_color = (0.2, 0.05, 0.04, 1); return M
def boards():
    M, nt, b = _nt("FloorBoards"); g, sp = _pos(nt)
    w = nt.nodes.new("ShaderNodeTexWave"); w.wave_type = 'BANDS'; w.bands_direction = 'Y'; w.inputs["Scale"].default_value = 1.0
    sc_ = nt.nodes.new("ShaderNodeVectorMath"); sc_.operation = 'SCALE'; sc_.inputs[3].default_value = 1.0 / ft(0.75) / 1.0
    nt.links.new(g.outputs["Position"], sc_.inputs[0]); nt.links.new(sc_.outputs[0], w.inputs["Vector"])
    gap = _ramp(nt, w.outputs["Fac"], 0.02, 0.07, (0.4, 0.4, 0.4), (1, 1, 1))
    grain = _ramp(nt, _noise(nt, g.outputs["Position"], 25.0, 8, 0.6), 0.3, 0.7, (0.17, 0.10, 0.055), (0.27, 0.17, 0.09))
    mm = nt.nodes.new("ShaderNodeMix"); mm.data_type = 'RGBA'; mm.blend_type = 'MULTIPLY'; mm.inputs["Factor"].default_value = 1.0
    nt.links.new(grain, mm.inputs[6]); nt.links.new(gap, mm.inputs[7]); nt.links.new(mm.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.45; M.diffuse_color = (0.22, 0.14, 0.07, 1); return M
def brick_ext():
    """sooty London stock brick (yellow-grey), coursed: 3 in courses, 9 in stretchers, stretcher bond via brick texture"""
    M, nt, b = _nt("StockBrick"); g, sp = _pos(nt)
    cb = nt.nodes.new("ShaderNodeCombineXYZ"); nt.links.new(sp.outputs[0], cb.inputs[0]); nt.links.new(sp.outputs[2], cb.inputs[1])
    bt = nt.nodes.new("ShaderNodeTexBrick"); nt.links.new(cb.outputs[0], bt.inputs["Vector"]); bt.inputs["Scale"].default_value = 1.0
    bt.inputs["Brick Width"].default_value = ft(0.75); bt.inputs["Row Height"].default_value = ft(0.25); bt.inputs["Mortar Size"].default_value = ft(0.03)
    bt.inputs["Color1"].default_value = (0.20, 0.16, 0.10, 1); bt.inputs["Color2"].default_value = (0.13, 0.10, 0.07, 1); bt.inputs["Mortar"].default_value = (0.16, 0.15, 0.13, 1)
    soot = _ramp(nt, _noise(nt, g.outputs["Position"], 0.6, 4), 0.35, 0.75, (0.45, 0.45, 0.45), (1, 1, 1))
    mm = nt.nodes.new("ShaderNodeMix"); mm.data_type = 'RGBA'; mm.blend_type = 'MULTIPLY'; mm.inputs["Factor"].default_value = 1.0
    nt.links.new(bt.outputs["Color"], mm.inputs[6]); nt.links.new(soot, mm.inputs[7]); nt.links.new(mm.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.93; M.diffuse_color = (0.18, 0.14, 0.09, 1); return M
def thin_glass(name, tint=(0.80, 0.86, 0.82), mix=0.04):
    M = G.mat_thin_glass("x", tint, mix); M.name = "LN3_" + name; M["cpl_mat_v1"] = 1; return M
def image_mat(name, fn, rough=0.85):
    M = G.mat_image("x", os.path.join(TEX, fn), rough); M.name = "LN3_" + name; M["cpl_mat_v1"] = 1; return M

MT = dict(
    boards=boards(), carpet=carpet(), paper_wall=wallpaper(),
    dado=plain("DadoPaint", (0.16, 0.13, 0.09), 0.5, noise=0.12), joinery=plain("JoineryPaint", (0.50, 0.47, 0.39), 0.45, noise=0.06),
    ceiling=plain("CeilingDistemper", (0.62, 0.60, 0.54), 0.95, noise=0.05, nscale=3.0), cornice=plain("CorniceDistemper", (0.60, 0.58, 0.52), 0.9),
    mahog=plain("Mahogany", (0.10, 0.038, 0.02), 0.32, noise=0.18, nscale=30.0), baize=plain("Baize", (0.03, 0.09, 0.035), 0.95, noise=0.15, nscale=40.0, sheen=0.2),
    horsehair=plain("Horsehair", (0.02, 0.018, 0.016), 0.35), brass=plain("Brass", (0.62, 0.45, 0.18), 0.3, 0.9),
    marble=plain("Marble", (0.62, 0.61, 0.57), 0.2, noise=0.08, nscale=6.0), castiron=plain("CastIron", (0.03, 0.03, 0.03), 0.5, 0.6),
    curtain=plain("Moreen", (0.20, 0.025, 0.025), 0.75, noise=0.15, nscale=8.0, sheen=0.8), glass=thin_glass("CrownGlass"),
    paperw=plain("Paper", (0.74, 0.70, 0.58), 0.9, noise=0.05), tape=plain("RedTape", (0.40, 0.05, 0.04), 0.7),
    books=plain("BookCloth", (0.12, 0.06, 0.04), 0.7, noise=0.5, nscale=6.0), gilt=plain("Gilt", (0.55, 0.40, 0.15), 0.35, 0.8),
    stucco=plain("Stucco", (0.40, 0.38, 0.33), 0.9, noise=0.2, nscale=1.5), brick=brick_ext(), darkglass=plain("DarkGlazing", (0.012, 0.012, 0.014), 0.12),
    slate=plain("Slate", (0.07, 0.075, 0.085), 0.6, noise=0.2), setts=plain("Setts", (0.11, 0.10, 0.09), 0.9, noise=0.3, nscale=4.0),
    flags=plain("YorkFlags", (0.24, 0.22, 0.19), 0.9, noise=0.25, nscale=2.0), sashw=plain("SashWhite", (0.58, 0.56, 0.50), 0.4),
    pot=plain("ChimneyPot", (0.26, 0.12, 0.06), 0.8), jug=plain("CreamwareGlaze", (0.70, 0.64, 0.48), 0.15), blue=plain("BlueTransfer", (0.06, 0.10, 0.30), 0.15),
    silver=plain("SilverPlate", (0.80, 0.80, 0.78), 0.15, 1.0), clothr=plain("BroadclothRed", (0.30, 0.03, 0.03), 0.9, sheen=0.5),
    clothb=plain("BroadclothIndigo", (0.02, 0.03, 0.10), 0.9, sheen=0.5), clothf=plain("FustianBuff", (0.42, 0.34, 0.20), 0.9, sheen=0.3),
    ink=plain("Ink", (0.005, 0.005, 0.008), 0.1), quill=plain("Quill", (0.75, 0.72, 0.62), 0.6), deal=plain("DealBox", (0.40, 0.30, 0.18), 0.8, noise=0.2, nscale=12),
    decanter=G.mat_glass("x", (0.92, 0.95, 0.93), 0.02), ember=plain("Ember", (0.05, 0.02, 0.01), 0.9, emit=((1.0, 0.35, 0.08), 3.0)),
    siteplan=image_mat("SitePlan", "cp005_siteplan.png"), alloc=image_mat("Allocation", "cp005_allocation.png"),
    sched=image_mat("Schedule", "cp005_schedule.png"), londonmap=image_mat("LondonMap", "cp005_londonmap.png"),
)
MT["decanter"].name = "LN3_DecanterGlass"; MT["decanter"]["cpl_mat_v1"] = 1
ML = list(MT.values()); IX = {k: i for i, k in enumerate(MT)}
def K(): return Kit(ML)
def I(k): return IX[k]

# ---------------------------------------------------------------- shell: floor, ceiling, four walls (street wall with openings)
k = K()
k.box(I("boards"), X0 - 0.6, X1 + 0.6, Y0 - 0.6, Y1 + WALL_T, -0.6, 0)                     # boarded floor
k.box(I("ceiling"), X0 - 0.6, X1 + 0.6, Y0 - 0.6, Y1 + WALL_T, CEIL, CEIL + 0.6)           # ceiling
for (a, b_) in ((X0 - 0.6, X0), (X1, X1 + 0.6)):                                           # end walls
    k.box(I("paper_wall"), a, b_, Y0, Y1, 0, CEIL)
k.box(I("paper_wall"), X0 - 0.6, X1 + 0.6, Y0 - 0.6, Y0, 0, CEIL)                           # chimney-breast wall (-y)
# street wall (+y) with three openings
xs = [X0 - 0.6] + [v for c in WX for v in (c - WW / 2, c + WW / 2)] + [X1 + 0.6]
for a, b_ in zip(xs[0::2], xs[1::2]): k.box(I("paper_wall"), a, b_, Y1, Y1 + WALL_T, 0, CEIL)   # piers
for c in WX:
    k.box(I("paper_wall"), c - WW / 2, c + WW / 2, Y1, Y1 + WALL_T, 0, SILL)                 # below the board
    k.box(I("paper_wall"), c - WW / 2, c + WW / 2, Y1, Y1 + WALL_T, HEAD, CEIL)              # over the head
k.box(I("carpet"), RX - 10.0, RX + 10.0, -7.5, 7.5, 0, 0.04)                                 # Brussels carpet square (floor boards round it)
k.done("LN3_Room_shell", ROOM)

# dado (paint below the rail), skirting, dado rail, cornice, ceiling rose — run round the walls, broken at the openings
k = K()
DOOR = (-5.2 - 0.5, -1.6 + 0.5)                            # door case on the +x wall (y range incl. architraves)
def run_along(fn):
    """call fn(x0,x1,y0,y1, nx, ny) for each straight wall run; nx,ny = inward normal"""
    fn(X0, X1, Y0, Y0, 0, 1)
    fn(X0, X0, Y0, Y1, 1, 0); fn(X1, X1, Y0, DOOR[0], -1, 0); fn(X1, X1, DOOR[1], Y1, -1, 0)   # +x wall broken at the door case
    for a, b_ in zip(xs[0::2], xs[1::2]): fn(max(a, X0), min(b_, X1), Y1, Y1, 0, -1)
def strip(z0, z1, proud, mat, xf=None):
    def fn(a, b_, c, d, nx, ny):
        if ny:   # along x
            y = c; k.box(I(mat), a, b_, min(y, y + ny * proud), max(y, y + ny * proud), z0, z1)
        else:
            x = a; k.box(I(mat), min(x, x + nx * proud), max(x, x + nx * proud), c, d, z0, z1)
    run_along(fn)
strip(0.0, 3.0, 0.03, "dado")             # painted dado panelling
strip(0.0, 0.75, 0.07, "dado")            # 9 in skirting
strip(2.88, 3.05, 0.10, "joinery")        # dado rail
strip(3.05, 3.1, 0.06, "joinery")
# cornice: three stepped members (7 in deep, 7 in projection) on all four walls (continuous at the top, no openings there)
for z0, z1, p in ((11.42, 11.62, 0.12), (11.62, 11.82, 0.30), (11.82, 12.0, 0.55)):
    k.box(I("cornice"), X0, X1, Y0, Y0 + p, z0, z1); k.box(I("cornice"), X0, X1, Y1 - p, Y1, z0, z1)
    k.box(I("cornice"), X0, X0 + p, Y0, Y1, z0, z1); k.box(I("cornice"), X1 - p, X1, Y0, Y1, z0, z1)
k.lathe(I("cornice"), (RX, 0.0), [(0.0, CEIL - 0.25), (0.8, CEIL - 0.22), (1.3, CEIL - 0.12), (1.6, CEIL - 0.02), (1.65, CEIL)], 32)   # ceiling rose
# panelled dado mouldings (raised fields) on the visible runs
for c in [X0 + 1.2 + i * 3.1 for i in range(9)]:
    k.box(I("joinery"), c, c + 2.5, Y1 - 0.06, Y1 - 0.03, 1.05, 2.6) if all(abs(c + 1.25 - w) > WW / 2 + 1.5 for w in WX) else None
for c in [Y0 + 1.0 + i * 3.1 for i in range(7)]:
    if c + 2.5 > DOOR[0] - 0.1 and c < DOOR[1] + 0.1: continue
    k.box(I("joinery"), X1 - 0.06, X1 - 0.03, c, c + 2.5, 1.05, 2.6)
k.done("LN3_Room_mouldings", ROOM)

# ---------------------------------------------------------------- windows: 6-over-6 sashes, shutters in the reveals, boards, architraves
k = K(); kc = K(); info["windows"] = 0
SY = Y1 + 0.85                                             # sash plane (set back in the 14 in wall: box frame toward the outer face)
for c in WX:
    a, b_ = c - WW / 2, c + WW / 2
    # box frame
    k.box(I("sashw"), a, a + 0.22, SY - 0.12, SY + 0.22, SILL, HEAD); k.box(I("sashw"), b_ - 0.22, b_, SY - 0.12, SY + 0.22, SILL, HEAD)
    k.box(I("sashw"), a, b_, SY - 0.12, SY + 0.22, HEAD - 0.2, HEAD); k.box(I("sashw"), a - 0.05, b_ + 0.05, SY - 0.12, SY + 0.32, SILL - 0.05, SILL + 0.12)
    ia, ib = a + 0.22, b_ - 0.22; mid = (SILL + 0.12 + HEAD - 0.2) / 2
    for (z0, z1, yy) in ((SILL + 0.12, mid + 0.06, SY + 0.06), (mid - 0.06, HEAD - 0.2, SY - 0.06)):   # lower (inner) / upper (outer) sash
        st, rl = 0.16, 0.18
        k.box(I("sashw"), ia, ia + st, yy - 0.08, yy + 0.08, z0, z1); k.box(I("sashw"), ib - st, ib, yy - 0.08, yy + 0.08, z0, z1)
        k.box(I("sashw"), ia, ib, yy - 0.08, yy + 0.08, z0, z0 + (rl if z0 < mid else 0.10)); k.box(I("sashw"), ia, ib, yy - 0.08, yy + 0.08, z1 - (0.10 if z0 < mid else rl), z1)
        gx0, gx1 = ia + st, ib - st; gz0, gz1 = z0 + (rl if z0 < mid else 0.10), z1 - (0.10 if z0 < mid else rl)
        for j in (1, 2): xx = gx0 + (gx1 - gx0) * j / 3; k.box(I("sashw"), xx - 0.035, xx + 0.035, yy - 0.05, yy + 0.05, gz0, gz1)   # glazing bars
        zz = (gz0 + gz1) / 2; k.box(I("sashw"), gx0, gx1, yy - 0.05, yy + 0.05, zz - 0.035, zz + 0.035)
        k.quad(I("glass"), [(gx0, yy, gz0), (gx1, yy, gz0), (gx1, yy, gz1), (gx0, yy, gz1)])
    # window board, architrave on the room face, panelled shutter leaves folded into the reveals
    k.box(I("joinery"), a - 0.3, b_ + 0.3, Y1 - 0.25, SY - 0.12, SILL - 0.08, SILL)
    for (p, q) in ((a - 0.55, a), (b_, b_ + 0.55)): k.box(I("joinery"), p, q, Y1 - 0.08, Y1, SILL - 0.4, HEAD + 0.55)
    k.box(I("joinery"), a - 0.55, b_ + 0.55, Y1 - 0.08, Y1, HEAD, HEAD + 0.55)
    k.box(I("joinery"), a - 0.62, b_ + 0.62, Y1 - 0.14, Y1, HEAD + 0.55, HEAD + 0.68)
    for s, xr in ((1, a), (-1, b_)):
        k.box(I("joinery"), min(xr, xr + s * 0.12), max(xr, xr + s * 0.12), Y1, SY - 0.12, SILL, HEAD)       # leaves (boxed)
        for z0, z1 in ((SILL + 0.3, SILL + 2.4), (SILL + 2.7, HEAD - 2.3), (HEAD - 2.0, HEAD - 0.3)):
            k.box(I("joinery"), min(xr, xr + s * 0.16), max(xr, xr + s * 0.16), Y1 + 0.12, SY - 0.24, z0, z1)
    # curtains: brass pole, two moreen drapes in pleats (drawn back beside the opening), shaped valance
    kc.cyl(I("brass"), (a - 1.5, Y1 - 0.45, HEAD + 0.95), (b_ + 1.5, Y1 - 0.45, HEAD + 0.95), 0.07, 10)
    for e in (a - 1.55, b_ + 1.55): kc.lathe(I("brass"), (e, Y1 - 0.45), [(0.0, HEAD + 0.82), (0.14, HEAD + 0.88), (0.14, HEAD + 1.02), (0.0, HEAD + 1.08)], 12)
    info["windows"] += 1
k.done("LN3_Windows", ROOM)
kc.done("LN3_CurtainPoles", ROOM)

def drape(name, x0, x1, y, z0, z1, folds, depth, tie=None, mat="curtain"):
    """pleated curtain: (nu x nv) grid, depth*sin pleats along x; tie=(z, x_tied) gathers the drape toward x_tied below z"""
    bm = bmesh.new(); nu, nv = folds * 6, 14; rows = []
    for j in range(nv + 1):
        t = j / nv; z = z1 + (z0 - z1) * t; row = []
        for i in range(nu + 1):
            u = i / nu; x = x0 + (x1 - x0) * u; d = depth
            if tie and z < tie[0] + 1.2:
                g = min(1.0, (tie[0] + 1.2 - z) / 1.2) if z > tie[0] else max(0.0, 1.0 - (tie[0] - z) / 3.5)
                x = x + (tie[1] - x) * 0.55 * g; d = depth * (1 + g)
            row.append(bm.verts.new((ft(x), ft(y - d * (0.5 + 0.5 * math.sin(u * folds * 2 * math.pi))), ft(z))))
        rows.append(row)
    for j in range(nv):
        for i in range(nu): bm.faces.new([rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(MT[mat])
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); ROOM.objects.link(o); return o
for n, c in enumerate(WX):
    a, b_ = c - WW / 2, c + WW / 2
    drape(f"LN3_Curtain_{n}L", a - 1.45, a + 0.25, Y1 - 0.5, 0.05, HEAD + 0.9, 5, 0.22, tie=(3.6, a - 0.8))
    drape(f"LN3_Curtain_{n}R", b_ - 0.25, b_ + 1.45, Y1 - 0.5, 0.05, HEAD + 0.9, 5, 0.22, tie=(3.6, b_ + 0.8))
    drape(f"LN3_Valance_{n}", a - 1.6, b_ + 1.6, Y1 - 0.62, HEAD + 0.15, HEAD + 1.1, 9, 0.12)

# ---------------------------------------------------------------- the street outside (first-floor view): our own frontage, setts, flags,
# area railings, and a 4-storey stock-brick terrace opposite with stucco ground floor, parapet, slate roofs, chimney stacks + pots
k = K(); info["terrace_opposite"] = 0
k.box(I("setts"), 220, 440, Y1 + WALL_T + 14, FACE_Y - 14, STREET_Z - 0.5, STREET_Z)
for (y0, y1) in ((Y1 + WALL_T + 6, Y1 + WALL_T + 14), (FACE_Y - 14, FACE_Y - 6)):
    k.box(I("flags"), 220, 440, y0, y1, STREET_Z - 0.5, STREET_Z + 0.5)
    for xx in range(220, 441, 6): k.box(I("castiron"), xx - 0.04, xx + 0.04, (y1 if y0 < 40 else y0) - 0.04, (y1 if y0 < 40 else y0) + 0.04, STREET_Z + 0.5, STREET_Z + 4.0)
    k.box(I("castiron"), 220, 440, (y1 if y0 < 40 else y0) - 0.06, (y1 if y0 < 40 else y0) + 0.06, STREET_Z + 3.7, STREET_Z + 3.85)
k.box(I("stucco"), 220, 440, Y1 + WALL_T, Y1 + WALL_T + 6, STREET_Z - 12, STREET_Z - 11.5)   # basement area floor
# our own building's street face below the room + above it (stucco ground floor, brick over)
k.box(I("stucco"), 240, 360, Y1 + WALL_T - 0.01, Y1 + WALL_T + 0.3, STREET_Z - 12, -0.6)
k.box(I("brick"), 240, 360, Y1, Y1 + WALL_T, CEIL + 0.6, CEIL + 24)
# opposite terrace: houses 20 ft wide, 4 storeys over a basement; floor-to-floor 12/12/10/8 ft above a 13 ft rusticated ground floor
FL = [STREET_Z, STREET_Z + 13, STREET_Z + 26, STREET_Z + 38, STREET_Z + 48, STREET_Z + 56]   # ground, 1st, 2nd, 3rd, attic, parapet base
for hx in range(260, 440, 20):
    x0, x1 = hx, hx + 20
    k.box(I("stucco"), x0, x1, FACE_Y, FACE_Y + 30, STREET_Z - 12, FL[1])                       # stucco ground floor
    for zz in range(int(STREET_Z) + 1, int(FL[1]), 2): k.box(I("stucco"), x0, x1, FACE_Y - 0.08, FACE_Y, zz, zz + 0.12)   # rustication
    k.box(I("brick"), x0, x1, FACE_Y, FACE_Y + 30, FL[1], FL[5] + 3.2)                          # brick upper storeys + parapet
    k.box(I("stucco"), x0, x1, FACE_Y - 0.5, FACE_Y, FL[1] - 0.3, FL[1] + 0.9)                  # first-floor band / balcony shelf
    k.box(I("stucco"), x0, x1, FACE_Y - 0.9, FACE_Y, FL[5] - 0.2, FL[5] + 0.9)                  # main cornice
    k.box(I("stucco"), x0, x1, FACE_Y - 0.25, FACE_Y + 0.4, FL[5] + 3.2, FL[5] + 3.5)           # parapet coping
    k.box(I("brick"), x1 - 0.6, x1 + 0.6, FACE_Y - 0.12, FACE_Y, FL[1], FL[5])                  # party-wall line
    # door + fanlight at one end, two windows ground floor
    k.box(I("darkglass"), x0 + 2.0, x0 + 5.6, FACE_Y - 0.05, FACE_Y + 0.4, STREET_Z + 1.0, STREET_Z + 9.0)
    k.box(I("stucco"), x0 + 1.4, x0 + 6.2, FACE_Y - 0.6, FACE_Y, STREET_Z + 9.0, STREET_Z + 9.6)
    for wx in (x0 + 10.5, x0 + 16.0):
        k.box(I("darkglass"), wx - 1.6, wx + 1.6, FACE_Y - 0.05, FACE_Y + 0.4, STREET_Z + 3.5, STREET_Z + 10.5)
    # upper floors: 3 windows per house, tall on the 1st floor (piano nobile), diminishing upward
    for (fz, h) in ((FL[1] + 2.0, 9.0), (FL[2] + 2.5, 7.0), (FL[3] + 2.3, 5.4), (FL[4] + 1.8, 4.0)):
        for wx in (x0 + 4.0, x0 + 10.0, x0 + 16.0):
            k.box(I("darkglass"), wx - 1.6, wx + 1.6, FACE_Y - 0.05, FACE_Y + 0.4, fz, fz + h)
            k.box(I("sashw"), wx - 1.6, wx + 1.6, FACE_Y - 0.07, FACE_Y + 0.4, fz + h * 0.5 - 0.06, fz + h * 0.5 + 0.06)   # meeting rail
            for j in (1, 2): k.box(I("sashw"), wx - 1.6 + 3.2 * j / 3 - 0.04, wx - 1.6 + 3.2 * j / 3 + 0.04, FACE_Y - 0.07, FACE_Y + 0.4, fz, fz + h)
            k.box(I("stucco"), wx - 1.85, wx + 1.85, FACE_Y - 0.35, FACE_Y, fz - 0.35, fz)                                # sill
            if fz < FL[2]: k.box(I("castiron"), wx - 1.8, wx + 1.8, FACE_Y - 0.9, FACE_Y - 0.8, fz, fz + 2.6)              # balconette rail
    # roof: double-pitch slate behind the parapet (valley roof) + chimney stack on the party wall with pots
    ztop = FL[5] + 3.0
    k.poly(I("slate"), [(x0, FACE_Y + 1, ztop), (x1, FACE_Y + 1, ztop), (x1, FACE_Y + 9, ztop + 6), (x0, FACE_Y + 9, ztop + 6)])
    k.box(I("brick"), x1 - 1.6, x1 + 1.6, FACE_Y + 4, FACE_Y + 7, ztop, ztop + 9.0)
    k.box(I("stucco"), x1 - 1.8, x1 + 1.8, FACE_Y + 3.8, FACE_Y + 7.2, ztop + 9.0, ztop + 9.4)
    for p in range(4): k.cyl(I("pot"), (x1 - 1.2 + p * 0.8, FACE_Y + 5.5, ztop + 9.4), (x1 - 1.2 + p * 0.8, FACE_Y + 5.5, ztop + 11.4 + (p % 2) * 0.6), 0.28, 10, True, 0.22)
    info["terrace_opposite"] += 1
k.done("LN3_StreetOutside", OUTC)

# ---------------------------------------------------------------- chimneypiece (-y wall), marble with a cast-iron register grate and a low fire
k = K()
k.box(I("marble"), RX - 3.0, RX - 2.3, Y0, Y0 + 0.75, 0, 4.3); k.box(I("marble"), RX + 2.3, RX + 3.0, Y0, Y0 + 0.75, 0, 4.3)
k.box(I("marble"), RX - 3.0, RX + 3.0, Y0, Y0 + 0.75, 3.6, 4.3); k.box(I("marble"), RX - 3.3, RX + 3.3, Y0, Y0 + 1.0, 4.3, 4.5)
k.box(I("castiron"), RX - 2.3, RX + 2.3, Y0, Y0 + 0.3, 0, 3.6); k.box(I("ember"), RX - 0.9, RX + 0.9, Y0 + 0.3, Y0 + 0.75, 0.9, 1.3)
k.box(I("marble"), RX - 3.6, RX + 3.6, Y0, Y0 + 2.0, -0.02, 0.06)                              # hearth stone
k.box(I("brass"), RX - 3.2, RX + 3.2, Y0 + 1.9, Y0 + 2.0, 0.06, 0.45)                           # fender
k.done("LN3_Chimneypiece", ROOM)

# ---------------------------------------------------------------- glazed mahogany bookcase on the -x wall (out of the CP005_room frame;
# the ln02 bookcase stood edge-on in front of the camera and filled the left third of the frame — D-LN-CP005-02)
k = K(); r = random.Random(7)
k.box(I("mahog"), X0, X0 + 1.6, 1.0, 9.0, 0, 8.4); k.box(I("mahog"), X0, X0 + 1.9, 0.8, 9.2, 8.4, 8.8)
for s_ in range(4):
    z = 3.2 + s_ * 1.3; k.box(I("mahog"), X0, X0 + 1.5, 1.1, 8.9, z, z + 0.06); bx = 1.15
    while bx < 8.8:
        bw = r.uniform(0.12, 0.28); bh = r.uniform(0.8, 1.15); k.box(I("books" if r.random() > 0.2 else "gilt"), X0 + 0.25, X0 + 1.25, bx, bx + bw, z + 0.06, z + 0.06 + bh); bx += bw + 0.01
k.done("LN3_Bookcase", ROOM)

# ---------------------------------------------------------------- the +x wall: six-panel door + a large London wall map on rollers
k = K()
DY0, DY1 = -5.2, -1.6
k.box(I("mahog"), X1 - 0.08, X1, DY0, DY1, 0, 7.5)
for z0, z1 in ((0.6, 2.9), (3.3, 5.3), (5.6, 7.1)):
    for y0, y1 in ((DY0 + 0.3, (DY0 + DY1) / 2 - 0.15), ((DY0 + DY1) / 2 + 0.15, DY1 - 0.3)): k.box(I("mahog"), X1 - 0.13, X1 - 0.08, y0, y1, z0, z1)
for (p, q) in ((DY0 - 0.5, DY0), (DY1, DY1 + 0.5)): k.box(I("joinery"), X1 - 0.1, X1, p, q, 0, 7.5)
k.box(I("joinery"), X1 - 0.1, X1, DY0 - 0.5, DY1 + 0.5, 7.5, 8.0); k.box(I("joinery"), X1 - 0.18, X1, DY0 - 0.6, DY1 + 0.6, 8.0, 8.15)
k.lathe(I("brass"), (X1 - 0.18, DY1 - 0.45), [(0.0, 3.4), (0.09, 3.42), (0.09, 3.52), (0.0, 3.54)], 10)
MY0, MY1, MZ0, MZ1 = 1.4, 9.4, 4.2, 9.5
k.cyl(I("mahog"), (X1 - 0.12, MY0 - 0.3, MZ1 + 0.1), (X1 - 0.12, MY1 + 0.3, MZ1 + 0.1), 0.11, 12); k.cyl(I("mahog"), (X1 - 0.12, MY0 - 0.3, MZ0 - 0.1), (X1 - 0.12, MY1 + 0.3, MZ0 - 0.1), 0.11, 12)
k.box(I("brass"), X1 - 0.03, X1 - 0.01, (MY0 + MY1) / 2 - 0.02, (MY0 + MY1) / 2 + 0.02, MZ1 + 0.2, MZ1 + 1.3)   # hanging cord
k.quad(I("londonmap"), [(X1 - 0.06, MY1, MZ0), (X1 - 0.06, MY0, MZ0), (X1 - 0.06, MY0, MZ1), (X1 - 0.06, MY1, MZ1)]); info["plans"] += 1
k.done("LN3_DoorAndMap", ROOM)

# ---------------------------------------------------------------- commission table: mahogany, green baize, turned legs (top surface 2.75 ft kept)
k = K()
TX0, TX1, TY0, TY1, TZ = RX - 5.0, RX + 5.0, -3.0, 3.0, 2.75
k.box(I("mahog"), TX0, TX1, TY0, TY1, TZ - 0.13, TZ); k.box(I("baize"), TX0 + 0.35, TX1 - 0.35, TY0 + 0.35, TY1 - 0.35, TZ, TZ + 0.005)
k.box(I("mahog"), TX0 + 0.45, TX1 - 0.45, TY0 + 0.4, TY1 - 0.4, TZ - 0.55, TZ - 0.13)               # frieze / apron
for lx in (TX0 + 0.6, RX, TX1 - 0.6):
    for ly in (TY0 + 0.55, TY1 - 0.55):
        k.lathe(I("mahog"), (lx, ly), [(0.09, 0.0), (0.12, 0.08), (0.10, 0.25), (0.13, 0.7), (0.16, 1.1), (0.12, 1.45), (0.10, 1.7), (0.15, 1.85), (0.17, 2.2), (0.17, TZ - 0.13)], 14)
k.done("LN3_CommissionTable", ROOM); info["table"] = 1

# chairs: mahogany, stuffed horsehair seats (18 in), shaped back rails; pulled out where men stand
def chair(name, x, y, rz):
    k = K(); s = 0.9
    k.box(I("mahog"), -s, s, -s, s, 1.30, 1.42); k.box(I("horsehair"), -s + 0.05, s - 0.05, -s + 0.05, s - 0.05, 1.42, 1.55)
    for a, b_ in ((-0.75, -0.75), (0.75, -0.75)): k.lathe(I("mahog"), (a, b_), [(0.07, 0), (0.09, 0.3), (0.07, 0.8), (0.1, 1.1), (0.09, 1.3)], 10)
    for a in (-0.75, 0.75):
        k.bar(I("mahog"), (a, 0.75, 0), (a, 0.82, 1.30), 0.14); k.bar(I("mahog"), (a, 0.82, 1.30), (a * 0.95, 0.95, 3.0), 0.13, 0.11)
    k.bar(I("mahog"), (-0.85, 0.97, 2.95), (0.85, 0.97, 2.95), 0.11, 0.3); k.bar(I("mahog"), (-0.72, 0.9, 2.15), (0.72, 0.9, 2.15), 0.08, 0.13)
    return k.done(name, ROOM, x, y, 0, rz)
CH = [(297.0, -4.5, 0.0), (300.0, -4.5, 0.15), (303.6, -5.0, -0.25), (300.95, 4.7, math.pi), (294.2, -2.2, math.pi / 2 + 0.5),
      (312.6, -8.6, -math.pi / 2), (288.6, 9.7, math.pi * 0.9)]
for i, (x, y, rz) in enumerate(CH): chair(f"LN3_Chair_{i}", x, y, rz)

# ---------------------------------------------------------------- on the table: the site plan with the large space marked for exhibits (the
# shot's subject), the floor allocation, a schedule of goods, rolled drawings in red tape, inkstand + quill, books, candlesticks
k = K()
def sheet(mat, cx, cy, w, h, rot, z=TZ + 0.012):
    c, s = math.cos(rot), math.sin(rot); pts = [(cx + c * dx - s * dy, cy + s * dx + c * dy, z) for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]
    k.quad(I(mat), pts); info["plans"] += 1
sheet("alloc", 303.2, 0.9, 3.0, 2.06, 0.12, TZ + 0.010)
sheet("sched", 296.6, -1.2, 1.5, 2.0, -0.25, TZ + 0.011)
sheet("siteplan", 299.9, -0.5, 4.3, 2.99, 0.04, TZ + 0.014)
for j, (yy, ln) in enumerate(((2.2, 3.1), (2.45, 2.7), (2.05, 2.5))):
    x0_ = 295.8 + j * 0.15; k.cyl(I("paperw"), (x0_, yy, TZ + 0.13 + (0.2 if j == 2 else 0)), (x0_ + ln, yy, TZ + 0.13 + (0.2 if j == 2 else 0)), 0.12, 14)
    k.cyl(I("tape"), (x0_ + ln / 2 - 0.05, yy, TZ + 0.13 + (0.2 if j == 2 else 0)), (x0_ + ln / 2 + 0.05, yy, TZ + 0.13 + (0.2 if j == 2 else 0)), 0.125, 14); info["plans"] += 1
# inkstand
k.box(I("brass"), 297.2, 298.2, -2.55, -1.95, TZ, TZ + 0.05)
for ix in (297.45, 297.95): k.lathe(I("decanter"), (ix, -2.25), [(0.0, TZ + 0.05), (0.13, TZ + 0.05), (0.13, TZ + 0.22), (0.05, TZ + 0.26), (0.0, TZ + 0.27)], 12)
k.bar(I("quill"), (297.95, -2.25, TZ + 0.25), (298.35, -1.75, TZ + 0.85), 0.03)
# books
for j in range(3): k.box(I("books"), 301.8 - j * 0.04, 302.8 + j * 0.03, -2.6, -1.95, TZ + j * 0.16, TZ + 0.15 + j * 0.16)
# candlesticks (unlit; it is midday)
for cx in (295.6, 304.4):
    k.lathe(I("brass"), (cx, -0.2), [(0.25, TZ), (0.25, TZ + 0.05), (0.08, TZ + 0.12), (0.06, TZ + 0.7), (0.1, TZ + 0.85), (0.07, TZ + 0.95), (0.0, TZ + 0.95)], 16)
    k.cyl(I("paperw"), (cx, -0.2, TZ + 0.95), (cx, -0.2, TZ + 1.4), 0.045, 8)
k.done("LN3_TablePapers", ROOM)

# samples of manufactured goods for comparison (D-LN-CP005-04): a blue-printed creamware jug, a cut-glass decanter, a plated
# teapot, bolts of broadcloth / fustian, a cast-iron gear wheel on a deal block, a stack of printed earthenware plates
k = K()
SX, SY_ = 303.3, 2.2
k.lathe(I("jug"), (SX - 1.4, SY_), [(0.0, TZ), (0.18, TZ), (0.2, TZ + 0.05), (0.27, TZ + 0.35), (0.22, TZ + 0.6), (0.17, TZ + 0.72), (0.21, TZ + 0.8), (0.0, TZ + 0.78)], 20)
k.lathe(I("blue"), (SX - 1.4, SY_), [(0.272, TZ + 0.3), (0.275, TZ + 0.36), (0.265, TZ + 0.42)], 20)
k.bar(I("jug"), (SX - 1.67, SY_, TZ + 0.68), (SX - 1.75, SY_, TZ + 0.3), 0.05, 0.04)
k.lathe(I("decanter"), (SX - 0.6, SY_ + 0.1), [(0.0, TZ), (0.2, TZ), (0.24, TZ + 0.3), (0.12, TZ + 0.55), (0.06, TZ + 0.75), (0.08, TZ + 0.8), (0.1, TZ + 0.86), (0.0, TZ + 0.98)], 20)
k.lathe(I("silver"), (SX + 0.25, SY_ - 0.15), [(0.0, TZ), (0.14, TZ), (0.12, TZ + 0.04), (0.26, TZ + 0.2), (0.24, TZ + 0.4), (0.12, TZ + 0.46), (0.05, TZ + 0.55), (0.0, TZ + 0.58)], 20)
k.bar(I("silver"), (SX + 0.48, SY_ - 0.15, TZ + 0.2), (SX + 0.75, SY_ - 0.15, TZ + 0.45), 0.05)
for j, (m_, yy) in enumerate((("clothr", SY_ + 0.45), ("clothb", SY_ - 0.05), ("clothf", SY_ + 0.2))):
    zz = TZ + 0.24 + (0.42 if j == 2 else 0)
    k.cyl(I(m_), (SX + 1.0, yy, zz), (SX + 2.5, yy, zz), 0.24, 18)
k.box(I("deal"), SX - 0.2, SX + 0.4, SY_ - 1.2, SY_ - 0.75, TZ, TZ + 0.25)
k.wheel(I("castiron"), (SX + 0.1, SY_ - 0.97, TZ + 0.85), "y", 0.6, 0.08, 0.1, 6)
for t in range(16):
    a = 2 * math.pi * t / 16; k.box(I("castiron"), SX + 0.1 + 0.62 * math.cos(a) - 0.04, SX + 0.1 + 0.62 * math.cos(a) + 0.04, SY_ - 1.0, SY_ - 0.94, TZ + 0.85 + 0.62 * math.sin(a) - 0.04, TZ + 0.85 + 0.62 * math.sin(a) + 0.04)
for j in range(3):   # a stack of three blue-printed earthenware plates (Staffordshire)
    zz = TZ + j * 0.05; k.lathe(I("jug" if j < 2 else "blue"), (SX - 2.25, SY_ - 0.75), [(0.0, zz), (0.22, zz), (0.3, zz + 0.02), (0.45, zz + 0.045), (0.46, zz + 0.05), (0.42, zz + 0.05), (0.3, zz + 0.03), (0.0, zz + 0.03)], 24)
k.done("LN3_Samples", ROOM); info["samples"] = 6

# gasolier over the table (London rooms were gas-lit by the 1840s); unlit at midday
k = K()
k.cyl(I("brass"), (RX, 0, CEIL - 0.2), (RX, 0, 8.6), 0.05, 10)
k.lathe(I("brass"), (RX, 0), [(0.0, 8.2), (0.25, 8.3), (0.3, 8.5), (0.12, 8.7), (0.0, 8.75)], 16)
for t in range(3):
    a = 2 * math.pi * t / 3 + 0.3; ex, ey = RX + 1.6 * math.cos(a), 1.6 * math.sin(a)
    k.bar(I("brass"), (RX, 0, 8.45), (RX + 0.9 * math.cos(a), 0.9 * math.sin(a), 8.25), 0.06); k.bar(I("brass"), (RX + 0.9 * math.cos(a), 0.9 * math.sin(a), 8.25), (ex, ey, 8.5), 0.06)
    k.lathe(I("paperw"), (ex, ey), [(0.0, 8.5), (0.15, 8.6), (0.22, 8.85), (0.15, 9.05), (0.09, 9.1)], 14)
k.done("LN3_Gasolier", ROOM)

# ---------------------------------------------------------------- five commissioners/officials in 1849-50 dress, bareheaded indoors
# (vendored cp002_figures.py = the KEEP'd CP009/CP002 modelled-dress builder; names avoid people_lib prefixes so the render-time swap
# leaves them alone). Composite planning activity, no portrait likeness (storyboard CP005).
import cp002_figures as F
_hat0 = F._hat
F._hat = lambda bm, I_, kind, mat, band: None if kind == "bare" else _hat0(bm, I_, kind, mat, band)
def face_rz(dx, dy): return math.atan2(dx, -dy)
CAST = [  # (tag, palette, pose, H m, x ft, y ft, facing dx, dy)
    ("leaning_far_left", "gent", "table", 1.76, 298.0, 4.3, 0.1, -1),
    ("leaning_far_right", "clerk", "table", 1.72, 303.9, 4.05, -0.15, -1),
    ("by_map", "gent", "standing", 1.79, 311.2, 5.6, -1, -0.45),
    ("table_end", "clerk", "standing", 1.74, 306.5, -1.6, -1, 0.35),
    ("table_left_end", "gent", "table", 1.77, 294.1, 1.3, 1, -0.15),
]
for i, (tag, pal, pose, H, x, y, dx, dy) in enumerate(CAST):
    nm = f"LN3_Folk_{i:02d}"; mats = F.palette_street(f"ln3_{i}", pal)
    o = F.build_figure(nm, "engineer", H, pose, seed=500 + i, mats=mats, hat="bare")
    o.location = (ft(x), ft(y), 0.0); o.rotation_euler = (0, 0, face_rz(dx, dy)); FIGC.objects.link(o)
    o["cp005_figure"] = f"{tag}/{pal}/{pose}/bare/{H}"; info["figures"] += 1
F._hat = _hat0

# ---------------------------------------------------------------- daylight: the street windows are the room's light source. Sky fill at each opening
# (area lights inside the reveal, facing in, invisible to camera) + the ln02 ceiling lamp turned down. World, sun and exposure untouched.
for n, c in enumerate(WX):
    L = bpy.data.lights.new(f"LN3_WindowSky_{n}", 'AREA'); L.shape = 'RECTANGLE'; L.size = ft(WW - 0.5); L.size_y = ft(HEAD - SILL - 0.4)
    L.energy = 300.0; L.color = (0.86, 0.90, 1.0)
    o = bpy.data.objects.new(f"LN3_WindowSky_{n}", L); o.location = (ft(c), ft(Y1 + 0.3), ft((SILL + HEAD) / 2)); o.rotation_euler = (math.radians(-90), 0, 0)
    o.visible_camera = False; o.visible_glossy = True; ROOM.objects.link(o)
lamp = bpy.data.objects.get("LN_RoomLamp")
if lamp: lamp.data.energy = 60.0

sc["grok_build"] = json.dumps({"set": "O-LONDON ln03_cp005 CANDIDATE (CP005 1849-50 planning room)", "seed": 1849, "info": info,
                               "base": "rounds/ln02.blend", "script": "scripts/build_cp005_room.py", "removed": removed})
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True, copy=True)
print("SAVED", OUT, info)
