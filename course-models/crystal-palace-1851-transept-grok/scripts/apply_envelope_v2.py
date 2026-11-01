"""CANDIDATE v2 (2026-11-01): Hyde Park 1851 east-nave envelope on live r11, fixing the v1 (r11_envelope) regressions.

  blender -b rounds/r11.blend -P scripts/apply_envelope_v2.py -- \
      --out rounds/candidates/r11_envelope_v2.blend [--rig none|v1]

Starts from live rounds/r11.blend (opened read-only; never saved over). Reuses apply_envelope_r11.py logic with patches:
  1. glass brighten (v1 brighten_host_glass) skips the Osler fountain (Muse MUSE_OSLER_* + our hidden FOUNTAIN_*),
     the exhibit case glass and the deliberately dark end-screen glass (L03).
  2. GROUND_PARK stays visible (v1 hid it with hide_outdoor_leaks()); no outdoor-leak hiding at all.
  3. The plain-white kit box (HPE_walls / 0.35 ft opaque cream slabs + box columns) is NOT built. Instead the east
     nave is continued from the transept's own part library (linked meshes col_22/42/62, girder24, truss72,
     roof_unit, wall_24_* glazed/boarded bays, wall_louvre, railing24): Downes 24 ft grid, tiers 22'2"/42'2"/62'2",
     nave tier-3 strip |y|<60 from x=60, full three-tier section x 132..252, glazed/boarded east end at x=252
     (a truncation; DEPARTURES ENV2-xx).
  4. Owen Jones paint on the new ironwork with per-object coordinates (v1 merged every column/girder into one mesh,
     so its object-space stripe/top-chord masks painted whole girders yellow) and a less saturated yellow.
Hyde Park 1851 only. Claude's / Codex's / Muse's files are never opened for writing.
"""
import bpy, bmesh, math, os, sys
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
OUT = arg("--out", "rounds/candidates/r11_envelope_v2.blend")
RIG = arg("--rig", "none")
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)
SRC = os.path.join(ROOT, "rounds/r11.blend")
assert os.path.abspath(out) != os.path.abspath(SRC), "refusing to overwrite live r11"
for protected in ("rounds/r10.blend", "rounds/candidates/r11_envelope.blend"):
    assert os.path.abspath(out) != os.path.abspath(os.path.join(ROOT, protected)), "refusing to overwrite " + protected

bpy.ops.wm.open_mainfile(filepath=SRC)
try:
    bpy.context.preferences.filepaths.save_version = 0   # no .blend1
except Exception:
    pass
sc = bpy.context.scene
FT = 0.3048
def ft(v): return v * FT
CAND = "HPE_envelope_v2"
GIRDER_TOP = [22 + 2 / 12, 42 + 2 / 12, 62 + 2 / 12]   # D11a-c (build_transept.py)
GIRDER_D = 3.0
LOUVRE_H = 2.5
log = []

# ---------------------------------------------------------------- fix 2: lawn stays
g = bpy.data.objects.get("GROUND_PARK")
assert g is not None
g.hide_render = False; g.hide_viewport = False
log.append("GROUND_PARK visible (fix 2)")

# ---------------------------------------------------------------- fix 1: glass brighten without the fountain
FOUNTAIN_COLLS = ("MUSE_OSLER_FOUNTAIN", "FOUNTAIN")
protect = set()
for o in bpy.data.objects:
    pk = str(o.get("part_kind", ""))
    in_fc = any(c.name in FOUNTAIN_COLLS for c in o.users_collection)
    if pk.startswith("fountain") or in_fc or o.name.startswith(("MUSE_OSLER", "FOUNTAIN_")):
        for s in o.material_slots:
            if s.material: protect.add(s.material.name)
for m in bpy.data.materials:
    n = m.name.lower()
    if any(k in n for k in ("osler", "fountain", "crystal", "water")) or m.name.startswith("MUSE_"):
        protect.add(m.name)
# exhibit case glass (Muse display case) and the deliberately dark end-screen glass (L03) are not envelope glass
protect.update({"Glass", "GT_GlassEndScreen"})

def brighten_host_glass_v2():
    """apply_envelope_r11 / hp_interior_envelope.brighten_host_glass(), minus the protected materials."""
    touched = []
    for m in bpy.data.materials:
        n = m.name.lower()
        if m.name in protect or not m.use_nodes:
            continue
        if not any(k in n for k in ("glass", "roof", "vault", "furrow")):
            continue
        for node in m.node_tree.nodes:
            if node.type == "BSDF_TRANSPARENT":
                c = list(node.inputs[0].default_value)
                node.inputs[0].default_value = (min(1, c[0] + 0.25), min(1, c[1] + 0.25), min(1, c[2] + 0.25), 1)
            if node.type == "BSDF_PRINCIPLED":
                if "Transmission Weight" in node.inputs:
                    node.inputs["Transmission Weight"].default_value = max(node.inputs["Transmission Weight"].default_value, 0.85)
                if "Alpha" in node.inputs:
                    node.inputs["Alpha"].default_value = min(node.inputs["Alpha"].default_value, 0.35)
        touched.append(m.name)
    return touched
touched = brighten_host_glass_v2()
print("ENV2_GLASS_BRIGHTENED", touched, flush=True)
print("ENV2_GLASS_PROTECTED", sorted(protect), flush=True)
log.append("glass brightened: %s; protected: %s" % (touched, sorted(protect)))

# ---------------------------------------------------------------- fix 4: calm Owen Jones paint (per-object coords)
OJ_BLUE = (0.13, 0.25, 0.58)
OJ_RED = (0.58, 0.05, 0.04)
OJ_YELLOW_CALM = (0.74, 0.62, 0.32)   # v1 used (0.86, 0.62, 0.12); less saturated, a shade darker
OJ_WHITE = (0.86, 0.86, 0.82)
def oj_mat(name, mode):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; n = nt.nodes; l = nt.links
    b = n["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.5
    def rgb(c):
        r = n.new("ShaderNodeRGB"); r.outputs[0].default_value = (*c, 1); return r.outputs[0]
    def mix(fac, a, c):
        x = n.new("ShaderNodeMix"); x.data_type = 'RGBA'; l.new(fac, x.inputs["Factor"]); l.new(a, x.inputs["A"]); l.new(c, x.inputs["B"]); return x.outputs["Result"]
    def M(op, a, v=None, a2=None):
        x = n.new("ShaderNodeMath"); x.operation = op; l.new(a, x.inputs[0])
        if a2 is not None: l.new(a2, x.inputs[1])
        elif v is not None: x.inputs[1].default_value = v
        return x.outputs[0]
    tc = n.new("ShaderNodeTexCoord"); sep = n.new("ShaderNodeSeparateXYZ"); l.new(tc.outputs["Object"], sep.inputs[0])
    geo = n.new("ShaderNodeNewGeometry"); sn = n.new("ShaderNodeSeparateXYZ"); l.new(geo.outputs["Normal"], sn.inputs[0])
    down = M('LESS_THAN', sn.outputs[2], -0.5)
    if mode == "column":
        # 8 stripes round the shaft per quarter turn: blue (wide), white, yellow (narrow), white
        ang = M('ARCTAN2', sep.outputs[1], a2=sep.outputs[0])
        q = M('FRACT', M('MULTIPLY', ang, 4 / (2 * math.pi)))
        is_yel = M('LESS_THAN', M('ABSOLUTE', M('SUBTRACT', q, 0.75)), 0.09)          # ~18% yellow (v1: 50%)
        is_wht = M('LESS_THAN', M('ABSOLUTE', M('SUBTRACT', M('ABSOLUTE', M('SUBTRACT', q, 0.75)), 0.13)), 0.04)
        c = mix(is_yel, rgb(OJ_BLUE), rgb(OJ_YELLOW_CALM))
        c = mix(is_wht, c, rgb(OJ_WHITE))
        c = mix(down, c, rgb(OJ_RED))
    elif mode == "girder":
        top = M('GREATER_THAN', sep.outputs[2], -3.2 / 12 * FT)    # top flange only (girder24/truss72 top at z=0)
        c = mix(top, rgb(OJ_BLUE), rgb(OJ_YELLOW_CALM))
        c = mix(down, c, rgb(OJ_RED))
    else:
        c = mix(down, rgb(OJ_BLUE), rgb(OJ_RED))
    l.new(c, b.inputs["Base Color"]); m.diffuse_color = (*OJ_BLUE, 1)
    return m
MAT_COL = oj_mat("GT2_IronColumn_OJcalm", "column")
MAT_GIR = oj_mat("GT2_IronGirder_OJcalm", "girder")

# ---------------------------------------------------------------- fix 3: east nave from the transept part library
LIB = {k: bpy.data.meshes[k] for k in ("col_22", "col_42", "col_62", "girder24", "truss72", "roof_unit",
                                        "wall_louvre", "railing24")}
def mesh_like(prefix):
    for me in bpy.data.meshes:
        if me.name.startswith(prefix): return me
    raise KeyError(prefix)
LIB["wall_g"] = mesh_like("wall_24_14.4"); LIB["wall_g_fill"] = bpy.data.meshes[LIB["wall_g"].name + "_fill"]
LIB["wall_b"] = mesh_like("wall_24_16.6"); LIB["wall_b_fill"] = bpy.data.meshes[LIB["wall_b"].name + "_fill"]
H_G = max(v.co.z for v in LIB["wall_g"].vertices) / FT
H_B = max(v.co.z for v in LIB["wall_b"].vertices) / FT
print("ENV2_WALL_HEIGHTS", round(H_G, 2), round(H_B, 2), flush=True)

coll = bpy.data.collections.new("HPE2_EAST_NAVE")
sc.collection.children.link(coll)
coll["candidate"] = CAND
coll["credit"] = "Grok Bot transept part library continued east on Downes' 24 ft grid (envelope v2 candidate)"
count = {}
def put(key, name, x, y, z, rot=0.0, mat=None, **props):
    o = bpy.data.objects.new("HPE2_" + name, LIB[key])
    o.location = (ft(x), ft(y), ft(z)); o.rotation_euler = (0, 0, rot)
    coll.objects.link(o)
    o["candidate"] = CAND; o["kit"] = "envelope_v2_partlib"
    for k, v in props.items(): o[k] = v
    if mat is not None:
        for s in o.material_slots:
            s.link = 'OBJECT'; s.material = mat
    count[key] = count.get(key, 0) + 1
    return o

# existing columns in r11
cols = {}
for o in bpy.data.objects:
    if o.name.startswith("COL_") and o.type == 'MESH' and "tier" in o:
        cols[(round(o.location.x / FT), round(o.location.y / FT))] = int(o["tier"])
existing = set(cols)
ROWS_Y = [-204 + 24 * j for j in range(18)]
X_NEW = [84, 108, 132, 156, 180, 204, 228, 252]
X_END = 252
def tier_east(y):
    ay = abs(y)
    return 3 if ay <= 60 else (2 if ay <= 132 else 1)
new_cols = {}
for x in X_NEW:
    for y in ROWS_Y:
        if abs(y) < 36 or (x, y) in existing:
            continue
        if x <= 132 and abs(y) > 60:
            continue
        new_cols[(x, y)] = tier_east(y)
for y in (-12, 12):           # end-screen columns across the 72 ft nave at the east end (pattern of C02)
    new_cols[(X_END, y)] = 3
cols.update(new_cols)
COLKEY = {1: "col_22", 2: "col_42", 3: "col_62"}
for (x, y), t in sorted(new_cols.items()):
    put(COLKEY[t], f"COL_X{x:+04d}_Y{y:+04d}", x, y, 0, mat=MAT_COL, part_kind="column", tier=t)

# girders between neighbours (tiers both reach), only for pairs touching a new column
def gird(a, b, along):
    ta, tb = cols.get(a), cols.get(b)
    if not ta or not tb: return
    if a in existing and b in existing: return
    for k in range(min(ta, tb)):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        put("girder24", f"GIR_T{k+1}_{along}_{mx:+.0f}_{my:+.0f}", mx, my, GIRDER_TOP[k],
            math.pi / 2 if along == "Y" else 0.0, mat=MAT_GIR, part_kind="girder", tier=k + 1)
for (x, y) in list(cols):
    if (x, y + 24) in cols: gird((x, y), (x, y + 24), "Y")
    if (x + 24, y) in cols: gird((x, y), (x + 24, y), "X")
gird((X_END, -36), (X_END, -12), "Y"); gird((X_END, 12), (X_END, 36), "Y")   # 12-ft steps not on the 24 grid
for k in range(3):   # (252,-12)-(252,12) is 24 ft: handled by the loop above when both present
    pass

# 72 ft roof trusses across the nave on every column line (light truss, as at x=+-60)
for x in X_NEW:
    put("truss72", f"TRUSS72_X{x:+04d}", x, 0, GIRDER_TOP[2], math.pi / 2, mat=MAT_GIR, part_kind="truss")

# ridge-and-furrow roof units (24 x 8 ft; orientation as the transept arm roofs R01)
for xc in range(72, X_END, 24):                       # tier 3 over |y| < 60
    for yc in range(-56, 57, 8):
        put("roof_unit", f"ROOF3_{xc:+d}_{yc:+d}", xc, yc, GIRDER_TOP[2], part_kind="roof", tier=3)
for xc in range(144, X_END, 24):
    for sy in (-1, 1):
        for yc in range(64, 129, 8):                  # tier 2 over |y| 60..132
            put("roof_unit", f"ROOF2_{xc:+d}_{sy*yc:+d}", xc, sy * yc, GIRDER_TOP[1], part_kind="roof", tier=2)
        for yc in range(136, 201, 8):                 # tier 1 over |y| 132..204
            put("roof_unit", f"ROOF1_{xc:+d}_{sy*yc:+d}", xc, sy * yc, GIRDER_TOP[0], part_kind="roof", tier=1)

# glazed / boarded wall bays (build_transept.wall_run pattern: bay, fill, louvre band on top)
def wall_bay(tag, x, y, z0, glazed, rot):
    k = "wall_g" if glazed else "wall_b"; H = H_G if glazed else H_B
    put(k, f"WALL_{tag}", x, y, z0, rot, part_kind="wall")
    put(k + "_fill", f"WALLF_{tag}", x, y, z0, rot, part_kind="wall_fill")
    put("wall_louvre", f"WLOUV_{tag}", x, y, z0 + H, rot, part_kind="louvre")
for sy in (-1, 1):
    s = "N" if sy > 0 else "S"
    for xc in range(72, X_END, 24):
        wall_bay(f"T3{s}_{xc}", xc, sy * 60, GIRDER_TOP[1], True, 0.0)        # tier-3 clerestory
    for xc in range(144, X_END, 24):
        wall_bay(f"T2{s}_{xc}", xc, sy * 132, GIRDER_TOP[0], True, 0.0)       # tier-2 clerestory
        wall_bay(f"T1{s}_{xc}", xc, sy * 204, 0.0, False, 0.0)                # boarded ground tier
for yc in range(-192, 193, 24):
    wall_bay(f"E1_{yc}", X_END, yc, 0.0, False, math.pi / 2)
for yc in range(-120, 121, 24):
    wall_bay(f"E2_{yc}", X_END, yc, GIRDER_TOP[0], True, math.pi / 2)
for yc in range(-48, 49, 24):
    wall_bay(f"E3_{yc}", X_END, yc, GIRDER_TOP[1], True, math.pi / 2)

# the arms' x=132 tier-2 side walls for |y| 60..132 are now interior (the east block has tier 2 there): hide, don't delete
hidden = []
for o in bpy.data.objects:
    if o.name.startswith(("WALL_A+1", "WALLF_A+1", "WLOUV_A+1")) and abs(o.location.y / FT) < 132:
        o.hide_render = True; o.hide_viewport = True; hidden.append(o.name)

# galleries over the aisles |y| 36..60 and 108..132 east of 132 (GA05 pattern), timber slab 9 in
timber = bpy.data.materials["GT_Timber"]
def slab(name, x0, x1, y0, y1, z_top, t, mat):
    bm = bmesh.new()
    vs = [bm.verts.new((ft(a), ft(b), ft(c))) for (a, b, c) in
          [(x0, y0, z_top - t), (x1, y0, z_top - t), (x1, y1, z_top - t), (x0, y1, z_top - t),
           (x0, y0, z_top), (x1, y0, z_top), (x1, y1, z_top), (x0, y1, z_top)]]
    for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
        bm.faces.new([vs[i] for i in f])
    me = bpy.data.meshes.new("HPE2_" + name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
    o = bpy.data.objects.new("HPE2_" + name, me); coll.objects.link(o)
    o["candidate"] = CAND; o["kit"] = "envelope_v2_partlib"; o["part_kind"] = "gallery"
    return o
GAL_TOP = 22 + 11 / 12; GAL_T = 0.75
for sy in (-1, 1):
    for (a, b) in ((36, 60), (108, 132)):
        y0, y1 = sorted((sy * a, sy * b))
        slab(f"GAL_E_{sy:+d}_{a}", 132, X_END, y0, y1, GAL_TOP, GAL_T, timber)
    for xc in range(72, X_END, 24):
        put("railing24", f"RAIL_NV_{sy:+d}_{xc}", xc, sy * 36, GAL_TOP, part_kind="railing")
    for xc in range(144, X_END, 24):
        for yy in (60, 108):
            put("railing24", f"RAIL_AV_{sy:+d}_{yy}_{xc}", xc, sy * yy, GAL_TOP, part_kind="railing")
# floor boards continued x 144..252 (same GT_FloorBoards, object coords at the world origin so the boards run on)
fb = bpy.data.objects["FLOOR_BOARDS"]
ztop = max((fb.matrix_world @ Vector(c)).z for c in fb.bound_box) / FT
slab("FLOOR_E", 144, X_END + 0.5, -204, 204, ztop, 0.5, bpy.data.materials["GT_FloorBoards"])

# crowd stand-ins that would stand inside a new column: hide (the people swap only replaces visible ones)
crowd_hidden = []
ccoll = bpy.data.collections.get("CROWD")
if ccoll:
    for o in ccoll.all_objects:
        p = (o.location.x / FT, o.location.y / FT)
        for (x, y) in new_cols:
            if abs(p[0] - x) < 1.6 and abs(p[1] - y) < 1.6:
                o.hide_render = True; o.hide_viewport = True; crowd_hidden.append(o.name); break

# ---------------------------------------------------------------- lighting
if RIG == "v1":   # the KEEP r11_envelope rig (HPE_Sun 7.0 + six 5 kW areas), for comparison only
    s = bpy.data.lights.new("HPE_Sun", "SUN"); s.energy = 7.0; s.angle = math.radians(4.5); s.color = (1.0, 0.98, 0.94)
    so = bpy.data.objects.new("HPE_Sun", s); sc.collection.objects.link(so); so.rotation_euler = (0.96, 0, 0.44)
    for i, (x, y) in enumerate(((180, -20), (220, -20), (180, 20), (220, 20), (60, 0), (100, 0))):
        a = bpy.data.lights.new(f"HPE_Area{i}", "AREA"); a.energy = 5000; a.size = ft(30)
        ao = bpy.data.objects.new(f"HPE_Area{i}", a); sc.collection.objects.link(ao); ao.location = (ft(x), ft(y), ft(38))
log.append(f"rig={RIG}")

for cname in ("CP023_into_nave_start", "CP023_into_nave_end"):
    c = bpy.data.objects.get(cname)
    if c: c["candidate"] = CAND

summary = {k: v for k, v in sorted(count.items())}
print("ENV2_PARTS", summary, "new_cols", len(new_cols), "hidden_walls", len(hidden), "crowd_hidden", len(crowd_hidden), flush=True)
txt = bpy.data.texts.get("CREDIT_HPE_V2") or bpy.data.texts.new("CREDIT_HPE_V2")
txt.clear()
txt.write(
    "CANDIDATE HP east-nave envelope v2 on r11 (2026-11-01, scripts/apply_envelope_v2.py)\n"
    "Transept part library continued east: nave tier-3 strip x 60..252, full section x 132..252, end at x=252.\n"
    f"Parts: {summary}; new columns {len(new_cols)}; interior arm walls hidden {len(hidden)}; crowd hidden {len(crowd_hidden)}\n"
    + "\n".join(log) + "\n"
    "GROUND_PARK visible. Osler fountain glass, case glass and end-screen glass not brightened.\n"
    "Host transept / Muse Osler / Claude west nave untouched on disk.\n"
)
sc["grok_envelope_v2"] = f"rig={RIG}; cols={len(new_cols)}; hidden_walls={len(hidden)}; crowd_hidden={len(crowd_hidden)}"
bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out, flush=True)
