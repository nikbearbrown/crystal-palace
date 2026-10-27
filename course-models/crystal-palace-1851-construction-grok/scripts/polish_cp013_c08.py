"""c08 polish for CP013 — iron joinery straps, sash-bar groove detail, loose panes + putty
dressing on the roof-edge platform. Geometry/materials only (no people). Idempotent via c08_polished flag.
  blender -b rounds/c07.blend -P scripts/polish_cp013_c08.py -- --out rounds/c08.blend
"""
import bpy, bmesh, math, sys, os, json
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None):
    return argv[argv.index(n) + 1] if n in argv else d
OUT = arg("--out", "rounds/c08.blend")
FT = 0.3048
def ft(v): return v * FT
sc = bpy.context.scene
if sc.get("c08_polished"):
    print("already polished"); bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True); raise SystemExit(0)

def ensure_mat(name, color, rough=0.75, metal=0.0, transmit=0.0):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes.get("Principled BSDF")
    if b:
        b.inputs["Base Color"].default_value = (*color, 1)
        b.inputs["Roughness"].default_value = rough
        if "Metallic" in b.inputs: b.inputs["Metallic"].default_value = metal
        if transmit and "Transmission Weight" in b.inputs:
            b.inputs["Transmission Weight"].default_value = transmit
            b.inputs["IOR"].default_value = 1.52
    return m

# ---- warmer timber grit on GT_Timber ----
tim = bpy.data.materials.get("GT_Timber")
if tim and tim.use_nodes and not tim.get("c08_grit"):
    nt = tim.node_tree; b = nt.nodes.get("Principled BSDF")
    if b:
        # warm deal tone
        b.inputs["Base Color"].default_value = (0.48, 0.36, 0.22, 1)
        b.inputs["Roughness"].default_value = 0.82
        # noise grit multiply
        tex = nt.nodes.new("ShaderNodeTexNoise"); tex.inputs["Scale"].default_value = 22; tex.inputs["Detail"].default_value = 10
        tex.location = (-500, 200)
        ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.location = (-300, 200)
        ramp.color_ramp.elements[0].position = 0.4; ramp.color_ramp.elements[0].color = (0.55, 0.45, 0.32, 1)
        ramp.color_ramp.elements[1].position = 0.7; ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
        mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.inputs["Factor"].default_value = 0.22
        mix.location = (-100, 100)
        base_in = b.inputs["Base Color"]
        # feed warm color as A, grit as B
        mix.inputs["A"].default_value = (0.48, 0.36, 0.22, 1)
        nt.links.new(tex.outputs["Fac"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], mix.inputs["B"])
        nt.links.new(mix.outputs["Result"], base_in)
        tim["c08_grit"] = 1
        print("timber grit applied")

# ---- roof glass: slightly greener milk so glazed bays read next to bare bars ----
rg = bpy.data.materials.get("GT_RoofGlassBuild")
if rg and rg.use_nodes and not rg.get("c08_glass"):
    for nd in rg.node_tree.nodes:
        if nd.type == "BSDF_TRANSPARENT":
            nd.inputs[0].default_value = (0.52, 0.60, 0.58, 1)
        if nd.type == "BSDF_DIFFUSE" and nd.inputs[0].default_value[0] > 0.5:
            nd.inputs[0].default_value = (0.50, 0.54, 0.52, 1)
    rg["c08_glass"] = 1
    print("roof glass nudged")

IRON = ensure_mat("GT_IronStrap_c08", (0.10, 0.10, 0.11), 0.45, 0.75)
PUTTY = ensure_mat("GT_Putty_c08", (0.62, 0.58, 0.48), 0.9)
PANE = bpy.data.materials.get("GT_PaneLoose") or ensure_mat("GT_PaneLoose_c08", (0.55, 0.62, 0.60), 0.05, 0.0, 1.0)
WOOD = bpy.data.materials.get("GT_Timber") or ensure_mat("GT_Timber_c08", (0.48, 0.36, 0.22), 0.8)
BARREL = ensure_mat("GT_Barrel_c08", (0.28, 0.18, 0.10), 0.85)

coll = bpy.data.collections.get("K_CP013_POLISH")
if coll is None:
    coll = bpy.data.collections.new("K_CP013_POLISH")
    sc.collection.children.link(coll)

def new_mesh(name, bm, mats, loc=(0, 0, 0)):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    ob = bpy.data.objects.new(name, me); ob.location = loc; coll.objects.link(ob)
    return ob

def box_bm(bm, x0, x1, y0, y1, z0, z1, mi=0):
    n0 = len(bm.faces)
    verts = [bm.verts.new(c) for c in (
        (x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
        (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1))]
    faces = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    for f in faces:
        bm.faces.new([verts[i] for i in f]).material_index = mi

# ---- iron joinery straps at ridge ends of bars units in CP013_sash view (x 360-384, y ~ -192..-160) ----
bm = bmesh.new(); nstrap = 0
for xb in (360, 384):
    for yc in range(-192, -143, 8):
        # strap wrapping ridge: short iron plates along +Y face of ridge
        x = ft(xb); y = ft(yc); z = ft(22.0)  # approx ridge height tier-1
        box_bm(bm, x - ft(0.4), x + ft(0.4), y - ft(0.15), y + ft(0.15), z, z + ft(0.35))
        box_bm(bm, x - ft(0.15), x + ft(0.15), y - ft(0.15), y + ft(0.15), z - ft(0.8), z)
        nstrap += 1
ob = new_mesh("KCP013_IRON_STRAPS", bm, [IRON])
ob["part_kind"] = "iron_strap"; ob["count"] = nstrap
print("straps", nstrap)

# ---- condensation grooves: thin underside ribs along a few sash bars near the camera ----
bm = bmesh.new(); ng = 0
# bars run roughly along Y on each slope; place grooves under bars at x~370 looking from platform
for k in range(14):
    x = ft(368 + k * 0.85)
    y0, y1 = ft(-200), ft(-172)
    z = ft(23.2) - abs(k - 7) * ft(0.12)  # follow slope approx
    box_bm(bm, x - ft(0.03), x + ft(0.03), y0, y1, z - ft(0.08), z)
    ng += 1
ob = new_mesh("KCP013_SASH_GROOVES", bm, [WOOD])
ob["part_kind"] = "sash_groove"; print("grooves", ng)

# ---- set dressing on roof-edge platform near CP013_sash / platform cams ----
# platform deck ~ z 24 ft at y~-212, x 360-420
bm = bmesh.new()
# putty barrels
for i, (x, y) in enumerate(((372, -208), (378, -209), (390, -207))):
    # barrel as short cylinder via stacked boxes approx
    for a in range(8):
        ang = a * math.pi / 4
        cx = ft(x) + math.cos(ang) * ft(0.45); cy = ft(y) + math.sin(ang) * ft(0.45)
        box_bm(bm, cx - ft(0.12), cx + ft(0.12), cy - ft(0.12), cy + ft(0.12), ft(24.0), ft(25.6), 0)
    box_bm(bm, ft(x) - ft(0.5), ft(x) + ft(0.5), ft(y) - ft(0.5), ft(y) + ft(0.5), ft(25.5), ft(25.7), 1)  # lid
# putty pats on boards
for i in range(10):
    x = 370 + (i % 5) * 3.2; y = -210.5 - (i // 5) * 1.2
    box_bm(bm, ft(x), ft(x) + ft(0.35), ft(y), ft(y) + ft(0.25), ft(24.05), ft(24.18), 1)
ob = new_mesh("KCP013_PUTTY", bm, [BARREL, PUTTY])
ob["part_kind"] = "putty_dressing"

# loose panes leaning into sash bars (half-slid) — glass sheets 49x10 in
bm = bmesh.new()
pane_mat_i = 0
for i, (x, y, z, tilt) in enumerate((
    (370.5, -190.0, 24.8, 28), (373.0, -188.0, 25.0, 32), (377.0, -186.0, 25.2, 30),
    (381.0, -184.0, 25.4, 35), (385.0, -182.0, 25.6, 28),
)):
    # thin sheet rotated approx in XY — use flat box along slope
    L = ft(49 / 12); W = ft(10 / 12); T = ft(0.08)
    # place as nearly vertical tipped sheet
    rad = math.radians(tilt)
    # simple axis-aligned approx for lean render
    box_bm(bm, ft(x), ft(x) + T, ft(y), ft(y) + W, ft(z), ft(z) + L * math.cos(math.radians(5)))
ob = new_mesh("KCP013_LOOSE_PANES", bm, [PANE])
ob["part_kind"] = "loose_pane"; print("loose panes", 5)

# timber sash-bar offcuts bundled on platform
bm = bmesh.new()
for row in range(3):
    for col in range(12):
        x = 400 + col * 0.15; y = -209.5 + row * 0.2
        box_bm(bm, ft(x), ft(x) + ft(49/12), ft(y), ft(y) + ft(0.1), ft(24.1 + row * 0.12), ft(24.22 + row * 0.12))
ob = new_mesh("KCP013_BAR_OFFCUTS", bm, [WOOD])
ob["part_kind"] = "sash_offcuts"

# iron ridge straps / bolts visible as small cubes along ridge in view
bm = bmesh.new()
for i in range(10):
    x = 364 + i * 2.2; y = -184
    box_bm(bm, ft(x) - ft(0.12), ft(x) + ft(0.12), ft(y) - ft(0.12), ft(y) + ft(0.12), ft(26.4), ft(26.7))
ob = new_mesh("KCP013_RIDGE_BOLTS", bm, [IRON])
ob["part_kind"] = "ridge_bolt"

sc["c08_polished"] = 1
sc["c08_note"] = "CP013 iron straps, sash grooves, putty/panes/offcuts dressing; timber grit; glass nudge"
info = {"round": "c08", "polish": "CP013 set geometry/materials", "straps": nstrap, "grooves": ng}
print("C08_INFO", json.dumps(info))
os.makedirs(os.path.dirname(os.path.abspath(OUT)) or ".", exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True)
print("SAVED", OUT)
