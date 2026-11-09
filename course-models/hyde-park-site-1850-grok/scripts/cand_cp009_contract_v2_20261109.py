"""CP009 contract CANDIDATE v2 2026-11-09 (DEPARTURES SD28-SD30 kept from v1, SD31 withdrawn, SD32-SD34 new).
v1 (2026-11-04) was REJECTED for its people_lib v3.4 figures and a washed-out after; v2 keeps the table/ground/hoarding
and replaces the figures (c9_figures_v2.py), lifts the primed iron/earth albedo so exposure stays near live (SD33/34).
  blender -b rounds/s02.blend -P scripts/cand_cp009_contract_v2_20261109.py -- [--out PATH]
"""
"""CP009 'The proposal becomes a contract' -- geo/look polish CANDIDATE 2026-11-04 (DEPARTURES SD28-SD31).
Run on the live rounds/s02.blend (never written; saved to rounds/candidates/s02_cp009contract.blend):
  blender -b rounds/s02.blend -P scripts/cand_cp009_contract_20261104.py -- [--out PATH]
Scoped to CP009 only: every new object is ST_-prefixed and base-hidden (grok_states shows ST_ only for CP009),
every changed material is a CP009C_ copy (GT_Deal etc. stay untouched for CM_TABLE / SV_TOOL / other shots).
  * SD28 deal drawing table: planked top with grain (brick-bond planks 9 in wide), warm unpainted deal; drawing
    instruments on the table (ink-stand, steel rule, two lead weights, pencil).
  * SD29 hoarding: weathered close boarding, per-board tone variation, vertical grain, splash-dirt at foot.
  * SD13 kept: iron primed grey-black -- now actually reads dark (matte primer, no metallic sky sheen); dray timber
    weathered/painted, iron tyres dark.
  * SD30 trodden earth: worn ground at the stacks, table and dray (alpha-blended patch over the park grass).
  * SD31 figures: survey people_lib v3.4 period figures, explicit poses, dark fustian -- engineer = 1850s_gentleman
    (top hat, frock), foreman/carter/workmen = 1850s_workman. Old figures renamed OLDST_ and hidden. Render --no-people.
"""
import bpy, bmesh, sys, os, math, hashlib, random
from mathutils import Vector

def arg(k, d=None):
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return a[a.index(k) + 1] if k in a else d

FT = 0.3048
NT = lambda m: m.node_tree

def newmat(name):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(b.outputs[0], out.inputs[0]); return m, nt, b, out

def ramp(nt, fac_socket, cols):
    r = nt.nodes.new("ShaderNodeValToRGB"); e = r.color_ramp
    e.elements[0].position, e.elements[0].color = cols[0][0], (*cols[0][1], 1)
    e.elements[1].position, e.elements[1].color = cols[-1][0], (*cols[-1][1], 1)
    for p, c in cols[1:-1]:
        el = e.elements.new(p); el.color = (*c, 1)
    nt.links.new(fac_socket, r.inputs[0]); return r

def coord(nt, scale=(1, 1, 1), rot=(0, 0, 0), kind="Object"):
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = scale; mp.inputs["Rotation"].default_value = rot
    nt.links.new(tc.outputs[kind], mp.inputs[0]); return mp.outputs[0]

def noise(nt, vec, scale, detail=4, rough=0.55):
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail; n.inputs["Roughness"].default_value = rough
    nt.links.new(vec, n.inputs["Vector"]); return n

def mix(nt, a, b, fac, mode="MIX"):
    m = nt.nodes.new("ShaderNodeMix"); m.data_type = "RGBA"; m.blend_type = mode
    for s, v in ((6, a), (7, b), (0, fac)):
        if isinstance(v, (float, int)): m.inputs[s].default_value = v
        elif isinstance(v, tuple): m.inputs[s].default_value = (*v, 1) if len(v) == 3 else v
        else: nt.links.new(v, m.inputs[s])
    return m.outputs[2]

def bump(nt, b, height, strength):
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = strength
    bp.inputs["Distance"].default_value = 0.01
    nt.links.new(height, bp.inputs["Height"]); nt.links.new(bp.outputs[0], b.inputs["Normal"])

# ---------------- SD28 deal: planked, grained ----------------
def deal_mat(name, base_lo, base_hi, plank_w=0.229, rough=0.62, weather=0.0):
    m, nt, b, _ = newmat(name)
    v = coord(nt)
    br = nt.nodes.new("ShaderNodeTexBrick"); nt.links.new(v, br.inputs["Vector"])
    br.inputs["Scale"].default_value = 1.0; br.inputs["Brick Width"].default_value = 2.6
    br.inputs["Row Height"].default_value = plank_w; br.inputs["Mortar Size"].default_value = 0.004
    br.inputs["Mortar Smooth"].default_value = 0.3; br.offset = 0.37
    br.inputs["Color1"].default_value = (1, 1, 1, 1); br.inputs["Color2"].default_value = (0.78, 0.78, 0.78, 1)
    br.inputs["Mortar"].default_value = (0.25, 0.25, 0.25, 1)
    gr = coord(nt, scale=(0.35, 9.0, 9.0))
    w = nt.nodes.new("ShaderNodeTexWave"); w.wave_type = "BANDS"; w.bands_direction = "Y"
    w.inputs["Scale"].default_value = 3.0; w.inputs["Distortion"].default_value = 6.0
    w.inputs["Detail"].default_value = 3.0; nt.links.new(gr, w.inputs["Vector"])
    r = ramp(nt, w.outputs["Fac"], [(0.0, base_hi), (0.55, base_lo), (1.0, base_hi)])
    col = mix(nt, r.outputs[0], br.outputs["Color"], 1.0, "MULTIPLY")
    if weather:
        n = noise(nt, v, 3.0, 6, 0.6)
        col = mix(nt, col, (0.20, 0.19, 0.17), nt.nodes.new("ShaderNodeMath") and n.outputs["Fac"], "MIX")
    nt.links.new(col, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = rough
    bump(nt, b, br.outputs["Fac"], 0.25); return m

# ---------------- SD29 hoarding: weathered close boarding ----------------
def hoarding_mat():
    m, nt, b, _ = newmat("CP009C_HoardingBoard")
    v = coord(nt)
    # per-board tone: noise sampled along X only at 2 ft boards (stepped via snapping)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(v, sep.inputs[0])
    sn = nt.nodes.new("ShaderNodeMath"); sn.operation = "SNAP"; sn.inputs[1].default_value = 2 * FT
    nt.links.new(sep.outputs[0], sn.inputs[0])
    wn = nt.nodes.new("ShaderNodeTexWhiteNoise"); wn.noise_dimensions = "1D"; nt.links.new(sn.outputs[0], wn.inputs["W"])
    tone = ramp(nt, wn.outputs["Value"], [(0.0, (0.15, 0.115, 0.08)), (0.5, (0.24, 0.19, 0.135)), (1.0, (0.33, 0.29, 0.23))])
    gr = coord(nt, scale=(14.0, 14.0, 0.5))
    w = nt.nodes.new("ShaderNodeTexWave"); w.wave_type = "BANDS"; w.bands_direction = "X"
    w.inputs["Scale"].default_value = 2.0; w.inputs["Distortion"].default_value = 7.0; w.inputs["Detail"].default_value = 4
    nt.links.new(gr, w.inputs["Vector"])
    grain = ramp(nt, w.outputs["Fac"], [(0.0, (0.72, 0.72, 0.72)), (1.0, (1.0, 1.0, 1.0))])
    col = mix(nt, tone.outputs[0], grain.outputs[0], 1.0, "MULTIPLY")
    # splash dirt at the foot (z < ~0.5 m) and weather streaks
    zr = nt.nodes.new("ShaderNodeMapRange"); nt.links.new(sep.outputs[2], zr.inputs[0])
    zr.inputs[1].default_value = 0.65; zr.inputs[2].default_value = 0.05; zr.inputs[3].default_value = 0; zr.inputs[4].default_value = 0.8
    n = noise(nt, v, 6.0, 6, 0.7)
    fm = nt.nodes.new("ShaderNodeMath"); fm.operation = "MULTIPLY"; nt.links.new(zr.outputs[0], fm.inputs[0]); nt.links.new(n.outputs["Fac"], fm.inputs[1])
    col = mix(nt, col, (0.10, 0.085, 0.06), fm.outputs[0])
    st = noise(nt, coord(nt, scale=(30, 30, 0.6)), 1.0, 3, 0.5)
    stc = ramp(nt, st.outputs["Fac"], [(0.35, (1, 1, 1)), (0.75, (0.8, 0.78, 0.76))])
    col = mix(nt, col, stc.outputs[0], 1.0, "MULTIPLY")
    nt.links.new(col, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.9
    bump(nt, b, w.outputs["Fac"], 0.15); return m

# ---------------- SD13 iron primed grey-black, matte ----------------
def iron_mat():
    m, nt, b, _ = newmat("CP009C_IronPrimed1850")
    v = coord(nt); n = noise(nt, v, 9.0, 6, 0.65)
    r = ramp(nt, n.outputs["Fac"], [(0.35, (0.062, 0.062, 0.064)), (0.62, (0.080, 0.080, 0.082)), (0.80, (0.11, 0.075, 0.055))])  # v2 SD34
    nt.links.new(r.outputs[0], b.inputs["Base Color"]); b.inputs["Metallic"].default_value = 0.0
    b.inputs["Roughness"].default_value = 0.7
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.3
    bump(nt, b, n.outputs["Fac"], 0.08); return m

def flat_mat(name, c, rough=0.6, metal=0.0):
    m, nt, b, _ = newmat(name); b.inputs["Base Color"].default_value = (*c, 1)
    b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal; m.diffuse_color = (*c, 1); return m

# ---------------- SD30 trodden earth over grass ----------------
def earth_mat():
    m, nt, b, out = newmat("CP009C_TroddenEarth")
    v = coord(nt); n = noise(nt, v, 1.1, 5, 0.6); nf = noise(nt, v, 14.0, 4, 0.6)
    col = ramp(nt, nf.outputs["Fac"], [(0.3, (0.16, 0.105, 0.055)), (0.55, (0.22, 0.15, 0.08)), (0.78, (0.15, 0.13, 0.06))])  # v2 SD34: browner, less grey dust
    nt.links.new(col.outputs[0], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.95
    bump(nt, b, nf.outputs["Fac"], 0.3)
    # mask: noise x per-vertex 'w' attribute (1 in the core, 0 at the patch rim)
    at = nt.nodes.new("ShaderNodeAttribute"); at.attribute_name = "w"
    mm = nt.nodes.new("ShaderNodeMath"); mm.operation = "MULTIPLY"
    nr = nt.nodes.new("ShaderNodeMapRange"); nt.links.new(n.outputs["Fac"], nr.inputs[0])
    nr.inputs[1].default_value = 0.35; nr.inputs[2].default_value = 0.6
    nt.links.new(nr.outputs[0], mm.inputs[0]); nt.links.new(at.outputs["Fac"], mm.inputs[1])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); ms = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(mm.outputs[0], ms.inputs[0]); nt.links.new(tr.outputs[0], ms.inputs[1]); nt.links.new(b.outputs[0], ms.inputs[2])
    nt.links.new(ms.outputs[0], out.inputs[0]); m.blend_method = "HASHED" if hasattr(m, "blend_method") else None
    return m

scene = bpy.context.scene
coll = bpy.data.collections.get("CP009C") or bpy.data.collections.new("CP009C")
if coll.name not in scene.collection.children: scene.collection.children.link(coll)
TAG = "cp009c_v2_20261109"

def link(o):
    coll.objects.link(o); o.hide_render = True; o[TAG] = True; return o

DEAL_T = deal_mat("CP009C_DealTable", (0.62, 0.45, 0.27), (0.80, 0.63, 0.42))  # v2 SD33: planed deal, paler + warmer
DEAL_D = deal_mat("CP009C_DrayTimber", (0.17, 0.11, 0.065), (0.27, 0.19, 0.12), plank_w=0.17, rough=0.8)
IRON = iron_mat(); HOARD = hoarding_mat(); EARTH = earth_mat()
INK = flat_mat("CP009C_InkStand", (0.02, 0.02, 0.025), 0.25)
STEEL = flat_mat("CP009C_Steel", (0.55, 0.55, 0.56), 0.35, 1.0)
LEAD = flat_mat("CP009C_Lead", (0.13, 0.13, 0.14), 0.5, 0.6)
PENCIL = flat_mat("CP009C_Cedar", (0.45, 0.22, 0.10), 0.5)

def swap(o, old, new):
    for i, s in enumerate(o.material_slots):
        if s.material and s.material.name == old:
            if o.data.users > 1: o.data = o.data.copy()
            o.data.materials[i] = new

for o in bpy.data.objects:
    if o.name.startswith("ST_") and o.type == "MESH":
        swap(o, "GT_IronNew1850", IRON)
        if o.name == "ST_DRAWING_TABLE": swap(o, "GT_Deal", DEAL_T)
        if o.name == "ST_CART": swap(o, "GT_Deal", DEAL_D)
        if o.name == "ST_HOARDING": swap(o, "GT_HoardingBoard", HOARD)
# paper: warm cartridge paper, slight sheen off
for n in ("ST_DRAWING_ON_TABLE", "ST_DRAWING_HANDED"):
    o = bpy.data.objects[n]
    if o.data.users > 1: o.data = o.data.copy()

# ---------------- drawing instruments on the table (SD28) ----------------
def box_obj(name, cx, cy, cz, sx, sy, sz, mat, rz=0.0):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for vv in bm.verts: vv.co = Vector((vv.co.x * sx, vv.co.y * sy, vv.co.z * sz))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
    o = bpy.data.objects.new(name, me); o.location = (cx, cy, cz); o.rotation_euler.z = math.radians(rz); return link(o)

def cyl_obj(name, cx, cy, cz, r, h, mat, seg=20):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=h)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); o.location = (cx, cy, cz + h / 2); return link(o)

tab = bpy.data.objects["ST_DRAWING_TABLE"]
TZ = max((tab.matrix_world @ v.co).z for v in tab.data.vertices)
dr = bpy.data.objects["ST_DRAWING_ON_TABLE"]; dx, dy = dr.location.x, dr.location.y
for vv in dr.data.vertices: pass
dr.location.z = TZ + 0.002
box_obj("ST_C9_INKSTAND", dx - 0.62, dy + 0.18, TZ + 0.025, 0.16, 0.10, 0.05, INK, 8)
cyl_obj("ST_C9_INKWELL", dx - 0.60, dy + 0.18, TZ + 0.05, 0.028, 0.045, INK)
box_obj("ST_C9_RULE", dx + 0.05, dy + 0.22, TZ + 0.004, 0.61, 0.025, 0.003, STEEL, 4)
cyl_obj("ST_C9_WEIGHT_A", dx + 0.42, dy - 0.27, TZ + 0.002, 0.035, 0.03, LEAD)
cyl_obj("ST_C9_WEIGHT_B", dx - 0.43, dy + 0.27, TZ + 0.002, 0.035, 0.03, LEAD)
p = cyl_obj("ST_C9_PENCIL", dx - 0.15, dy - 0.05, TZ + 0.006, 0.0045, 0.18, PENCIL, 8)
p.rotation_euler = (0, math.radians(90), math.radians(30))

# ---------------- SD30 worn ground patch (copy of G_PARK_NEAR faces, lifted 15 mm) ----------------
def worn_patch():
    g = bpy.data.objects["G_PARK_NEAR"]; mw = g.matrix_world
    # ellipses in metres (cx, cy, rx, ry): stacks + dray track, drawing table, cart standing
    ells = [(56.4, -67.6, 7.5, 5.0), (48.3, -74.0, 3.0, 1.6), (61.5, -69.8, 5.5, 2.4)]
    def w_at(p):
        best = 0.0
        for cx, cy, rx, ry in ells:
            d = math.sqrt(((p.x - cx) / rx) ** 2 + ((p.y - cy) / ry) ** 2)
            best = max(best, min(1.0, max(0.0, (1.15 - d) / 0.55)))
        return best
    bm = bmesh.new(); bm.from_mesh(g.data); bm.transform(mw)
    bm.verts.ensure_lookup_table()
    kill = [f for f in bm.faces if max(w_at(v.co) for v in f.verts) <= 0.0]
    bmesh.ops.delete(bm, geom=kill, context="FACES")
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=2, use_grid_fill=True)
    for v in bm.verts: v.co.z += 0.015
    me = bpy.data.meshes.new("ST_C9_GROUND_WORN"); bm.to_mesh(me); bm.free()
    a = me.attributes.new("w", "FLOAT", "POINT")
    for i, v in enumerate(me.vertices): a.data[i].value = w_at(v.co)
    me.materials.append(EARTH)
    o = bpy.data.objects.new("ST_C9_GROUND_WORN", me); link(o)
    # crystal_palace_look._ensure_horizon_ground matches "ground"/"earth" in any object name (hidden or not) and would lift
    # CPL_HorizonGround to this patch top (a pale disk over every s02 shot on the look path). render_shots.py hides objects
    # tagged cpl_not_ground from that scan (temporary rename around apply_look). Name kept: renaming shifts Cycles noise.
    o["cpl_not_ground"] = True
    return len(me.vertices)
print("CP009C worn patch verts", worn_patch())

# ---------------- SD32 (v2) period figures: c9_figures_v2 (HBM head + modelled 1850 dress, hats that sit) ----------------
# v1's people_lib v3.4 swap was REJECTED (bald grey heads, lost top hat / period dress, read barefoot). v2 builds its own
# figures: frock coat + top hat (engineer), jacket + waistcoat + wideawake (foreman), fustian jackets, moleskin trousers,
# caps / wideawakes, neckerchiefs, laced ankle boots (workmen), smock-frock (carter). Old s02 figures renamed OLD and hidden.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import c9_figures_v2 as F
CAST = {  # old figure -> role, palette, pose, height m, hat
    "ST_FIG_engineer": ("engineer", "engineer", "table", 1.80, "top"),
    "ST_FIG_foreman": ("foreman", "foreman", "standing", 1.77, "wide"),
    "ST_FIG_carter": ("carter", "carter", "standing", 1.71, "wide"),
    "ST_FIG_workman_0": ("workman", "workman_b", "hauling", 1.74, "cap"),
    "ST_FIG_workman_1": ("workman", "workman_b", "working", 1.73, "wide"),
    "ST_FIG_workman_2": ("workman", "workman_a", "standing", 1.75, "cap"),
}
rows = []
for i, (old, (role, pal, pose, H, hat)) in enumerate(CAST.items()):
    oo = bpy.data.objects[old]; loc, rot = oo.location.copy(), oo.rotation_euler.copy()
    zfoot = min((oo.matrix_world @ Vector(c)).z for c in oo.bound_box)
    oo.name = "OLD" + old; oo.hide_render = True; oo["cp009c_replaced"] = True
    o = F.build_figure("ST_C9_" + old[3:], role, H, pose, seed=i, mats=F.palette(f"c9_{i}", pal), hat=hat); link(o)
    o.location = (loc.x, loc.y, zfoot); o.rotation_euler = rot; o["part_kind"] = "cp009_fixed_figure"
    o[TAG] = f"c9_figures_v2 {role} {pose} {hat} {H}"; rows.append((o.name, role, pal, pose, hat, H))
for r in rows: print("PERSON", *r)
# handed sheet: people_lib's posed arms leave the (straight) sleeves, so close figures stand with arms down and the
# handed sheet no longer floats in mid-air -- it is being slid across the near table corner toward the foreman.
hd = bpy.data.objects["ST_DRAWING_HANDED"]
hd.location = (dx + 0.52, dy - 0.05, TZ + 0.004); hd.rotation_euler = (0, 0, math.radians(76))

out = arg("--out") or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rounds", "candidates", "s02_cp009contract_v2.blend")
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True); print("CP009C SAVED", out)
