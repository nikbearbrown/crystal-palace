"""CP019 "The world arrives in cases" CANDIDATE (2026-11-16, DEPARTURES FT101-FT108). NOT live, no verdict.
  blender -b -P scripts/cand_cp019_cases_20261116.py -- --src rounds/f03.blend --out rounds/candidates/f03_cp019cases.blend
Hyde Park fit-out state only (f03, state "fitout", Feb-Mar 1851, goods arriving from 12 Feb 1851); nothing Sydenham.

Live CP019_doors_start (hero, 28 mm) stands inside the south transept end at (-14, -160) ft, eye 5.25 ft, looking at the open
south doors (0, -214). In live f03 the boarded floor between the camera and the doors is bare except one hand truck, the two wall
flanks either side of the doorway are blank boarding, and through and above the doors there is only flat lawn and open sky: the
shot names "the world arrives in cases" but shows three crates. This candidate dresses the two flanks with consignments that have
just come through the doors, and puts the Kensington Road side tree row, bare in February-March, on the skyline:
  FT101 east flank (frame left), x 14..23, y -191..-202: a stack of deal packing cases (battened board cases, two-man and
        crane sizes) and canvas bales with hoop-iron bands, each with a painted consignment mark (textures/cp019_mark_*.png,
        scripts/make_cp019_stencils.py).
  FT102 west flank (frame right), x -15..-26, y -193..-202: a tall sculpture case with its front boards taken off, a draped
        marble figure standing in it in straw (figures.py "draped", 6 ft 6 in), the front boards laid flat in front of it, and a
        9 ft cast-iron flywheel standing on edge in a timber cradle on skids (machinery arriving in pieces).
  FT103 a second dray with a grey horse queued on the apron at (8, -320), seen through the right-hand door opening.
  FT104 consignment marks: exhibitor's mark in a diamond, case number, country/town, destination (staging; not catalogue).
  FT105 Kensington Road side tree row at y = -520 +- 12 ft, 115-150 ft apart (exterior EX31 rule, as FT97), WOOD ONLY (no leaf
        cards): linked instances of this file's transept elm wood meshes, because elms are bare in February-March.
  FT106 nothing else changes: figures (people_lib runs at render time), walls, doors, trucks, drays, lighting, world, exposure and
        cameras are untouched; nothing is hidden or deleted. No new figures (people_lib seeds by distance order, so new figures
        would reshuffle the existing ones).
"""
import bpy, bmesh, math, os, sys, random, glob, json
from mathutils import Vector, Matrix
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
SRC, OUT = arg("--src"), arg("--out")
assert os.path.abspath(SRC) != os.path.abspath(OUT), "refusing to overwrite the source blend"
HERE = os.path.dirname(os.path.abspath(__file__)); MODEL = os.path.dirname(HERE)
for live in glob.glob(os.path.join(MODEL, "rounds", "*.blend*")):
    assert os.path.abspath(OUT) != os.path.abspath(live), "refusing to overwrite a live rounds/*.blend"
assert "/rounds/candidates/" in os.path.abspath(OUT), "candidate must go to rounds/candidates/"
sys.path.insert(0, HERE)
import figures as FG
bpy.ops.wm.open_mainfile(filepath=SRC)
info0 = json.loads(bpy.context.scene.get("grok_build", "{}"))
assert info0.get("state") == "fitout", "source must be a fitout round (live f03)"
assert not any(o.name.startswith("C19_") for o in bpy.data.objects), "source already has the candidate"
try: bpy.context.preferences.filepaths.save_version = 0
except Exception: pass
sc = bpy.context.scene
FT = 0.3048
def ft(v): return v * FT
TAG = "cp019_cases_20261116"
col = bpy.data.collections.new("C19_ARRIVALS"); sc.collection.children.link(col)
coll_t = bpy.data.collections.new("C19_PARK_TREES"); sc.collection.children.link(coll_t)
n_new = {"cases": 0, "bales": 0, "sculpture": 0, "machinery": 0, "dray": 0, "trees": 0, "marks": 0}
rows = {}

# ---------- materials ----------
def pmat(name, rgb, rough=0.8, metal=0.0, grain=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    m.diffuse_color = (*rgb, 1)
    if grain:   # stretched noise for deal grain / canvas weave variation (generated coords)
        tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (2.0, 2.0, 40.0)
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 6.0; nz.inputs["Detail"].default_value = 6.0
        mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = 'RGBA'; mx.inputs["Factor"].default_value = grain
        mx.inputs["A"].default_value = (*rgb, 1); mx.inputs["B"].default_value = (rgb[0] * 0.62, rgb[1] * 0.58, rgb[2] * 0.55, 1)
        L = nt.links; L.new(tc.outputs["Object"], mp.inputs["Vector"]); L.new(mp.outputs["Vector"], nz.inputs["Vector"])
        L.new(nz.outputs["Fac"], mx.inputs["Factor"]); L.new(mx.outputs["Result"], b.inputs["Base Color"])
    return m
DEAL = pmat("C19_Deal", (0.50, 0.40, 0.27), 0.85, grain=1.0)
DEAL_DK = pmat("C19_DealBatten", (0.34, 0.25, 0.16), 0.85, grain=1.0)
GAP = pmat("C19_CaseGap", (0.05, 0.04, 0.03), 0.9)
CANVAS = pmat("C19_Canvas", (0.58, 0.52, 0.40), 0.95, grain=0.5)
HOOP = pmat("C19_HoopIron", (0.09, 0.08, 0.07), 0.6, 0.6)
CAST = pmat("C19_CastIron", (0.085, 0.085, 0.09), 0.55, 0.5)
STRAW = bpy.data.materials.get("FT_straw") or pmat("C19_Straw", (0.70, 0.58, 0.30), 0.95)
MARBLE = bpy.data.materials.get("Marble") or pmat("C19_Marble", (0.80, 0.78, 0.73), 0.4)
MARKS = {}
def mark_mat(key):
    if key in MARKS: return MARKS[key]
    p = os.path.join(MODEL, "textures", f"cp019_mark_{key}.png"); img = bpy.data.images.load(p); img.pack()
    m = bpy.data.materials.new(f"C19_Mark_{key}"); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = img; t.extension = 'CLIP'
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"]); nt.links.new(t.outputs["Alpha"], b.inputs["Alpha"])
    b.inputs["Roughness"].default_value = 0.9
    try: m.blend_method = 'HASHED'
    except Exception: pass
    MARKS[key] = m; return m

# ---------- mesh kit (feet in, metres out) ----------
class Kit:
    def __init__(s, mats): s.bm = bmesh.new(); s.mats = mats; s.uv = s.bm.loops.layers.uv.new("UVMap")
    def box(s, i, x0, x1, y0, y1, z0, z1):
        r = bmesh.ops.create_cube(s.bm, size=1.0)
        for v in r["verts"]: v.co = Vector((ft((x0 + x1) / 2 + v.co.x * (x1 - x0)), ft((y0 + y1) / 2 + v.co.y * (y1 - y0)), ft((z0 + z1) / 2 + v.co.z * (z1 - z0))))
        for f in {f for v in r["verts"] for f in v.link_faces}: f.material_index = i
        return r
    def quad(s, i, pts):   # pts in ft, CCW seen from outside; uv 0..1
        vs = [s.bm.verts.new(Vector(tuple(ft(c) for c in p))) for p in pts]; f = s.bm.faces.new(vs); f.material_index = i
        for lp, uv in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))): lp[s.uv].uv = uv
    def cyl(s, i, a, b, r, seg=16):
        a, b = Vector(a), Vector(b); d = b - a; L = d.length
        res = bmesh.ops.create_cone(s.bm, cap_ends=True, segments=seg, radius1=ft(r), radius2=ft(r), depth=ft(L))
        q = Vector((0, 0, 1)).rotation_difference(d.normalized())
        M = Matrix.Translation(Vector(tuple(ft(c) for c in (a + b) / 2))) @ q.to_matrix().to_4x4()
        bmesh.ops.transform(s.bm, matrix=M, verts=res["verts"])
        for f in {f for v in res["verts"] for f in v.link_faces}: f.material_index = i
    def done(s, name):
        me = bpy.data.meshes.new(name); s.bm.normal_update(); s.bm.to_mesh(me); s.bm.free()
        for m in s.mats: me.materials.append(m)
        return me
def place(name, me, x, y, z=0.0, rz=0.0, **props):
    ob = bpy.data.objects.new(name, me); col.objects.link(ob)
    ob.location = (ft(x), ft(y), ft(z)); ob.rotation_euler = (0, 0, rz)
    ob[TAG] = props.pop("ftid", ""); ob["credit"] = "Grok"
    for k, v in props.items(): ob[k] = v
    return ob

def case_mesh(name, w, d, h, marks=("", ""), open_front=False):
    """deal packing case, origin base centre, w along x, d along y. Boards 0.07 ft thick with dark gaps, battens 0.3 ft wide and
    0.08 ft proud on all four sides, battened lid. marks = (key on +y face, key on -y face); open_front: no +y boards (sculpture case)."""
    mats = [DEAL, DEAL_DK, GAP] + [mark_mat(k) for k in marks if k]
    k = Kit(mats); t = 0.07; bh = 0.55; hw, hd = w / 2, d / 2
    k.box(2, -hw + t, hw - t, -hd + t, hd - t, 0.0, h - t) if not open_front else k.box(2, -hw + t, hw - t, -hd + t, -hd + 2 * t, 0.0, h - t)
    z = 0.0
    while z < h - t - 0.05:                     # horizontal boards on the sides
        z1 = min(z + bh - 0.03, h - t)
        if not open_front: k.box(0, -hw, hw, hd - t, hd, z, z1)
        k.box(0, -hw, hw, -hd, -hd + t, z, z1)
        k.box(0, -hw, -hw + t, -hd, hd, z, z1); k.box(0, hw - t, hw, -hd, hd, z, z1)
        z += bh
    if open_front:   # sides and back only; the case bottom is a plank floor
        k.box(0, -hw + t, hw - t, -hd + t, hd, 0.0, 0.25)
    for xx in range(int(w / 0.6) + 1):          # lid boards along y
        x0 = -hw + xx * (w / (int(w / 0.6) + 1)); x1 = x0 + w / (int(w / 0.6) + 1) - 0.03
        k.box(0, x0, x1, -hd, hd, h - t, h)
    p, bw = 0.08, 0.3
    faces_y = ([hd] if not open_front else []) + [-hd]
    for sy in faces_y:                          # battens on the +-y faces
        yo = sy + (p if sy > 0 else -p); y0, y1 = sorted((sy, yo))
        for sx in (-1, 1): k.box(1, sx * hw - (bw if sx > 0 else 0), sx * hw + (0 if sx > 0 else bw), y0, y1, 0.0, h)
        for zz in (0.0, h - bw): k.box(1, -hw + bw, hw - bw, y0, y1, zz, zz + bw)
    for sx in (-1, 1):                          # battens on the +-x faces
        xo = sx * (hw + p); x0, x1 = sorted((sx * hw, xo))
        for sy in (-1, 1): k.box(1, x0, x1, sy * hd - (bw if sy > 0 else 0), sy * hd + (0 if sy > 0 else bw), 0.0, h)
        for zz in (0.0, h - bw): k.box(1, x0, x1, -hd + bw, hd - bw, zz, zz + bw)
    for xx in (-hw + 0.25, hw - 0.55): k.box(1, xx, xx + 0.3, -hd, hd, h, h + 0.08)   # lid battens
    mi = 3
    for face, key in zip((1, -1), marks):       # painted mark on the board face between the battens
        if not key or (face > 0 and open_front): continue
        mw = w - 2 * bw - 0.2; mh = min(h - 2 * bw - 0.2, mw * 0.625); zc = h / 2; yy = face * (hd + 0.012)
        if face > 0: k.quad(mi, [(-mw / 2, yy, zc - mh / 2), (mw / 2, yy, zc - mh / 2), (mw / 2, yy, zc + mh / 2), (-mw / 2, yy, zc + mh / 2)])
        else: k.quad(mi, [(mw / 2, yy, zc - mh / 2), (-mw / 2, yy, zc - mh / 2), (-mw / 2, yy, zc + mh / 2), (mw / 2, yy, zc + mh / 2)])
        mi += 1; n_new["marks"] += 1
    return k.done(name)

def bale_mesh(name, w, d, h, mark=""):
    """canvas-wrapped bale of cloth, rounded edges, three hoop-iron bands round the girth; mark on the +y face"""
    mats = [CANVAS, HOOP] + ([mark_mat(mark)] if mark else [])
    k = Kit(mats); r = k.box(0, -w / 2, w / 2, -d / 2, d / 2, 0.0, h)
    bmesh.ops.bevel(k.bm, geom=[e for e in k.bm.edges], offset=ft(0.28), segments=3, affect='EDGES')
    for f in k.bm.faces: f.material_index = 0
    for bx in (-w * 0.38, w * 0.38):            # bands: thin rings approximated by four flat straps
        k.box(1, bx - 0.07, bx + 0.07, -d / 2 - 0.02, d / 2 + 0.02, h - 0.02, h + 0.01); k.box(1, bx - 0.07, bx + 0.07, -d / 2 - 0.02, d / 2 + 0.02, -0.01, 0.02)
        k.box(1, bx - 0.07, bx + 0.07, d / 2 - 0.01, d / 2 + 0.02, 0.1, h - 0.1); k.box(1, bx - 0.07, bx + 0.07, -d / 2 - 0.02, -d / 2 + 0.01, 0.1, h - 0.1)
    if mark:
        mw = w * 0.56; mh = mw * 0.625; mh = min(mh, h - 0.6); yy = d / 2 + 0.025; zc = h / 2
        k.quad(2, [(-mw / 2, yy, zc - mh / 2), (mw / 2, yy, zc - mh / 2), (mw / 2, yy, zc + mh / 2), (-mw / 2, yy, zc + mh / 2)]); n_new["marks"] += 1
    return k.done(name)

def flywheel_mesh(name, D=9.0):
    """cast-iron flywheel on edge (axis along y) in a timber cradle on two skids: rim 0.9 ft deep x 0.6 ft wide, six spokes, hub 1.6 ft"""
    k = Kit([CAST, DEAL_DK]); R = D / 2; zc = R + 1.0; N = 36
    for j in range(N):
        a0, a1 = 2 * math.pi * j / N, 2 * math.pi * (j + 1) / N
        for (ra, rb) in ((R - 0.9, R),):
            p = [(ra * math.cos(a0), ra * math.sin(a0)), (rb * math.cos(a0), rb * math.sin(a0)), (rb * math.cos(a1), rb * math.sin(a1)), (ra * math.cos(a1), ra * math.sin(a1))]
            vs = []
            for yy in (-0.3, 0.3):
                for (u, v) in p: vs.append(k.bm.verts.new(Vector((ft(u), ft(yy), ft(zc + v)))))
            for f in ((0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)):
                k.bm.faces.new([vs[i] for i in f]).material_index = 0
    for j in range(6):
        a = 2 * math.pi * j / 6 + 0.26; ca, sa = math.cos(a), math.sin(a)
        k.cyl(0, (0.7 * ca, 0, zc + 0.7 * sa), ((R - 0.85) * ca, 0, zc + (R - 0.85) * sa), 0.22, 10)
    k.cyl(0, (0, -0.55, zc), (0, 0.55, zc), 0.8, 20); k.cyl(0, (0, -0.75, zc), (0, 0.75, zc), 0.32, 12)
    for sx in (-2.2, 2.2): k.box(1, sx - 0.5, sx + 0.5, -1.4, 1.4, 0.35, 1.25)      # cradle baulks under the rim
    for sy in (-1.1, 1.1): k.box(1, -3.6, 3.6, sy - 0.3, sy + 0.3, 0.0, 0.35)        # skids
    for sx in (-1.0, 1.0):                                                           # chocks against the rim
        k.box(1, sx * 2.6 - 0.35, sx * 2.6 + 0.35, -0.8, 0.8, 1.25, 2.0)
    bm = k.bm; bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005)
    return k.done(name)

def straw_mesh(name, n, rx, ry, seed, rmin=0.5, rmax=1.0):
    rs = random.Random(seed); bm = bmesh.new()
    for _ in range(n):
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=ft(rs.uniform(rmin, rmax)), matrix=Matrix.Translation((ft(rs.uniform(-rx, rx)), ft(rs.uniform(-ry, ry)), 0)))
    for v in bm.verts:
        v.co.z = max(0.0, v.co.z * 0.5); v.co.x += ft(rs.uniform(-0.05, 0.05)); v.co.y += ft(rs.uniform(-0.05, 0.05))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(STRAW); return me

def boards_mesh(name, w, h):
    """a case front taken off in one piece: vertical boards on two battens, lying in the x-z plane, origin bottom centre"""
    k = Kit([DEAL, DEAL_DK]); n = int(w / 0.55) + 1; bw = w / n
    for j in range(n): k.box(0, -w / 2 + j * bw, -w / 2 + (j + 1) * bw - 0.03, 0.0, 0.07, 0.0, h)
    for zz in (0.6, h - 0.9): k.box(1, -w / 2, w / 2, 0.07, 0.15, zz, zz + 0.3)
    return k.done(name)

# ---------------- FT101: east flank (frame left): packing cases and bales from abroad ----------------
CASES_E = [   # name, w, d, h, x, y, z, rz, marks(+y,-y)
    ("C19_CASE_E1", 4.4, 3.0, 3.0, 16.6, -199.6, 0.0, 0.03, ("france", "france")),
    ("C19_CASE_E2", 3.6, 2.6, 2.6, 16.3, -199.4, 3.08, -0.07, ("zoll", "")),
    ("C19_CASE_E3", 3.4, 2.5, 2.5, 21.2, -200.2, 0.0, -0.04, ("usa", "")),
    ("C19_CASE_E4", 5.2, 3.4, 3.6, 20.0, -195.6, 0.0, 0.10, ("belgique", "")),
]
for nm, w, d, h, x, y, z, rz, mk in CASES_E:
    place(nm, case_mesh(nm.lower(), w, d, h, mk), x, y, z, rz, part_kind="crate", ftid="FT101", consignment=mk[0], size_ft=[w, d, h])
    n_new["cases"] += 1; rows[nm] = [x, y, z, w, d, h, mk[0]]
BALES = [("C19_BALE_1", 4.4, 2.3, 2.4, 15.4, -192.0, 0.0, 0.32, "bale"), ("C19_BALE_2", 4.4, 2.3, 2.4, 15.6, -192.1, 2.42, 0.26, ""),
         ("C19_BALE_3", 4.0, 2.2, 2.3, 19.4, -191.2, 0.0, -0.18, "india")]
for nm, w, d, h, x, y, z, rz, mk in BALES:
    place(nm, bale_mesh(nm.lower(), w, d, h, mk), x, y, z, rz, part_kind="bale", ftid="FT101", consignment=mk, size_ft=[w, d, h])
    n_new["bales"] += 1; rows[nm] = [x, y, z, w, d, h, mk]
place("C19_STRAW_E", straw_mesh("c19_straw_e", 7, 2.5, 1.2, 19), 22.6, -193.2, 0, 0.3, part_kind="straw", ftid="FT101")

# ---------------- FT102: west flank (frame right): sculpture case opened, flywheel in its cradle ----------------
SX, SY, SRZ = -17.6, -197.0, -0.12          # case front faces the camera (+y, a little east)
place("C19_SCULPT_CASE", case_mesh("c19_sculpt_case", 3.6, 3.0, 8.6, ("", "care"), open_front=True), SX, SY, 0, SRZ, part_kind="crate_open", ftid="FT102", size_ft=[3.6, 3.0, 8.6])
fig = FG.statue_mesh("draped", ft(6.5), MARBLE)
place("C19_SCULPT_FIGURE", fig, SX + 0.05, SY + 0.15, 0.25, SRZ + math.pi, part_kind="statue_arriving", ftid="FT102", height_ft=6.5)
place("C19_SCULPT_STRAW", straw_mesh("c19_straw_s", 9, 1.6, 1.3, 7, 0.45, 0.85), SX, SY + 0.4, 0.25, 0, part_kind="straw", ftid="FT102")
place("C19_SCULPT_STRAW_OUT", straw_mesh("c19_straw_o", 6, 1.8, 0.9, 8, 0.4, 0.8), SX + 0.3, SY + 2.6, 0, 0.2, part_kind="straw", ftid="FT102")
fb = place("C19_SCULPT_FRONT", boards_mesh("c19_sculpt_front", 3.4, 8.4), SX + 0.6, SY + 3.4, 0.16, SRZ + 0.35, part_kind="case_front", ftid="FT102")
fb.rotation_euler = (math.radians(-90), 0, SRZ + 0.35)     # the front taken off and laid flat on the boards, battens down
n_new["sculpture"] = 1
place("C19_FLYWHEEL", flywheel_mesh("c19_flywheel", 9.0), -24.0, -199.0, 0.0, 0.05, part_kind="machine_part", ftid="FT102", diameter_ft=9.0)
n_new["machinery"] = 1

# ---------------- FT103: a second dray queued on the apron ----------------
dray_me = bpy.data.meshes["dray"]; horse_me = bpy.data.meshes["ft_horse_grey"]
a = math.radians(-90 + 6); ca, sa = math.cos(a), math.sin(a); X0, Y0 = 8.0, -320.0
place("C19_DRAY_Q", dray_me, X0, Y0, 0, a, part_kind="dray", ftid="FT103")
place("C19_DRAY_Q_HORSE", horse_me, X0 + 11.5 * ca, Y0 + 11.5 * sa, 0, a, part_kind="horse", ftid="FT103")
for j, (lx, ly, lz, w, d, h, mk) in enumerate(((-3.5, -1.5, 0, 3.4, 2.5, 2.5, "zoll"), (-3.5, 1.5, 0, 3.4, 2.5, 2.5, ""), (1.0, 0, 0, 4.0, 2.8, 2.8, "usa"), (-3.5, 0, 2.5, 3.2, 2.4, 2.4, ""))):
    nm = f"C19_DRAY_Q_CASE_{j}"
    place(nm, case_mesh(nm.lower(), w, d, h, (mk, mk) if mk else ("", "")), X0 + lx * ca - ly * sa, Y0 + lx * sa + ly * ca, 4.0 + lz, a + math.pi / 2, part_kind="crate", ftid="FT103")
n_new["dray"] = 1

# ---------------- FT105: Kensington Road side tree row, bare (Feb-Mar 1851) ----------------
ELMS = (("ELM_SOUTH", 4.0, -128.0), ("ELM_NORTH", -3.0, 142.0), ("ELM_NORTH2", 12.0, 98.0))
rt = random.Random(1851 + 19); x = -700.0 + rt.uniform(0, 30); trees = []
while x < 700:
    p = (x, -520.0 + rt.uniform(-12, 12)); kk = n_new["trees"] % 3; nm, bx, by = ELMS[kk]
    e = bpy.data.objects.new(f"C19_TREE_{n_new['trees']:02d}", None); coll_t.objects.link(e)
    e.location = (ft(p[0]), ft(p[1]), 0); e.rotation_euler = (0, 0, rt.uniform(0, 6.28)); s_ = rt.uniform(0.9, 1.05); e.scale = (s_, s_, s_)
    e[TAG] = "FT105 Kensington Road side row (EX31 rule), bare elm wood instance"; e["part_kind"] = "park_tree"; e["credit"] = "Grok"
    src = bpy.data.objects[f"{nm}_WOOD"]
    c = bpy.data.objects.new(f"C19_TREE_{n_new['trees']:02d}_WOOD", src.data); coll_t.objects.link(c)
    c.location = (-ft(bx), -ft(by), 0); c.parent = e; c.matrix_parent_inverse.identity(); c["part_kind"] = "park_tree"; c["credit"] = "Grok"; c[TAG] = "FT105"
    trees.append([round(p[0], 1), round(p[1], 1), nm, round(s_, 3)]); n_new["trees"] += 1
    x += rt.uniform(115, 150)

info0.setdefault("state_info", {})["cp019_cases_candidate"] = {"tag": TAG, "new": n_new, "items": rows, "trees": trees}
sc["grok_build"] = json.dumps(info0)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True)
print("CP019_CANDIDATE_SAVED", OUT, json.dumps(n_new))
