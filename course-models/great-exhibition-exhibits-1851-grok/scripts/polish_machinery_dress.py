"""CANDIDATE (2026-11-02): CP024 Machinery Court stand dressing, Hyde Park 1851.

Dressing references (colour/arrangement only, NOT measurements), scan branch
origin/scans/crystal-palace-illustrations-2026-11-01:
  fig-29 Hibbert, Platt & Sons cotton machines behind a rope rail, overhead line
         shafting with pulleys and belts dropping to each machine;
  fig-30 De la Rue envelope machine: brass stanchions + crimson rope, green floor
         cloth inside the rail, painted stand placard, attendant at the machine;
  fig-48 Garrett stand (name-board fascia idea only; no farm implements here);
  fig-21 western nave colour (crimson / gilt / green accents).
Figs 43/54/74 carry generated patches and were not used.

Opens the BASE blend read-only (--base; default rounds/e02.blend.pre_machinery_keep if present,
else live rounds/e02.blend) and saves a NEW candidate blend
(default rounds/candidates/e02_machinery_dress.blend). Live is never written.
The KEEP Nasmyth hammer (EXH_NASMYTH_HAMMER), its barrier/label and the
envelope are not modified. The rejected 2026-11-01 Muse hammer swap and Muse
block-out replacement are NOT repeated: the grey neighbour block-outs stay as
they are and are only dressed around (stand, rail, placard, belt, attendant).

  blender -b rounds/e02.blend -P scripts/polish_machinery_dress.py -- \
      [--out rounds/candidates/e02_machinery_dress.blend] [--shaft-z 15.5] \
      [--no-people] [--no-shafts] [--no-rails] [--no-placards] [--base rounds/e02.blend.pre_machinery_keep]
      [--boiler-placard-dx 1.0] [--boiler-placard-yaw 0]
KEEP 2026-11-02 (approach_start, approach_end, ram_start): promoted to live by
scripts/promote_machinery_live.py; live renders via scripts/render_cp024_machinery.sh.

Units: feet in the parameter tables (converted by parts1851.finish).
"""
import bpy, bmesh, math, os, sys, importlib
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import parts1851 as P
from parts1851 import box, rod, lathe, finish
from common import FT, ft, mat

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
OUT = arg("--out", "rounds/candidates/e02_machinery_dress.blend")
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
LIVE = os.path.join(ROOT, "rounds/e02.blend")
# Base blend to dress. Before the 2026-11-02 KEEP this was live e02; after the KEEP live already carries
# the dressing, so rebuilds start from the pre-KEEP backup (== git 5c4b55d:rounds/e02.blend, md5 ae5355a5...).
_bk = os.path.join(ROOT, "rounds/e02.blend.pre_machinery_keep")
BASE = arg("--base", _bk if os.path.isfile(_bk) else LIVE)
BASE = BASE if os.path.isabs(BASE) else os.path.join(ROOT, BASE)
assert os.path.abspath(out) != os.path.abspath(LIVE), "refusing to overwrite live e02"
os.makedirs(os.path.dirname(out), exist_ok=True)
SHAFT_Z = float(arg("--shaft-z", "15.5"))      # line-shaft centre height, ft (fig-29: well below gallery)
DO_PEOPLE = "--no-people" not in argv
DO_SHAFTS = "--no-shafts" not in argv
DO_RAILS = "--no-rails" not in argv
DO_PLACARDS = "--no-placards" not in argv
# KEEP polish (2026-11-02): boiler CLASS V placard sat 0.8% from the left edge of CP024_approach_start;
# slide it east (inward in that frame) along the rail front. --boiler-placard-dx 0 restores the candidate.
BOILER_PLACARD_DX = float(arg("--boiler-placard-dx", "1.0"))   # ft, +x = east
BOILER_PLACARD_YAW = float(arg("--boiler-placard-yaw", "0"))   # deg about the post, + = turn face toward +x
CAND = "e02_machinery_dress"
PREFIX = "MCD_"

bpy.ops.wm.open_mainfile(filepath=BASE)
print("MCD_BASE", BASE, flush=True)
for o in list(bpy.data.objects):
    if o.name.startswith(PREFIX) or o.get("candidate") == CAND:
        bpy.data.objects.remove(o, do_unlink=True)
coll = bpy.data.collections.get("MCD_MACHINERY_DRESS_1851") or bpy.data.collections.new("MCD_MACHINERY_DRESS_1851")
if coll.name not in [c.name for c in bpy.context.scene.collection.children]:
    bpy.context.scene.collection.children.link(coll)
coll["candidate"] = CAND; coll["cp_era"] = "HP1851"

# ---------------- materials (period paint / brass / leather) ----------------
M = dict(
    brass=mat("MCD_Brass", (0.62, 0.42, 0.13), 0.32, 1.0),
    iron=mat("MCD_IronPost", (0.06, 0.065, 0.07), 0.5, 0.6),
    rope=mat("MCD_CrimsonRope", (0.36, 0.03, 0.03), 0.85),
    rope_buff=mat("MCD_BuffRope", (0.55, 0.45, 0.30), 0.9),
    baize=mat("MCD_GreenBaize", (0.07, 0.17, 0.08), 0.95),
    stand=mat("MCD_StandCrimson", (0.33, 0.05, 0.04), 0.6),
    board=mat("MCD_PlacardBlack", (0.025, 0.025, 0.03), 0.5),
    gilt=mat("MCD_Gilt", (0.80, 0.58, 0.20), 0.3, 1.0),
    letter=mat("MCD_LetterCream", (0.85, 0.80, 0.66), 0.6),
    shaft=mat("MCD_TurnedShaft", (0.62, 0.63, 0.65), 0.25, 1.0),
    pulley=mat("MCD_PulleyIron", (0.30, 0.31, 0.33), 0.45, 0.7),
    hanger=mat("MCD_HangerIron", (0.12, 0.13, 0.14), 0.5, 0.5),
    belt=mat("MCD_LeatherBelt", (0.16, 0.085, 0.04), 0.7),
)

def add(name, bm, mats, part):
    me = finish(bm, "ME_" + name, mats)
    o = bpy.data.objects.new(name, me); coll.objects.link(o)
    o["candidate"] = CAND; o["cp_era"] = "HP1851"; o["part_kind"] = part
    return o

def mi(bm, n0, idx):
    bm.faces.ensure_lookup_table()
    for f in bm.faces[n0:]: f.material_index = idx

# ---------------- stand table (feet) ----------------
# block-out centres/footprints are read from the live HPE_nbr_* objects; rails get margins.
STANDS = {
    #  key        block-out            rail style  margin  placard                                  belt pulley (x,y,z,r) on machine
    "boiler": dict(obj="HPE_nbr_boiler", rail="iron",  margin=2.5, cls="CLASS V.",  sub="MACHINES FOR DIRECT USE", belt=None),
    "engine": dict(obj="HPE_nbr_engine", rail="iron",  margin=3.0, cls="CLASS V.",  sub="MACHINES FOR DIRECT USE", belt="flywheel"),
    "press":  dict(obj="HPE_nbr_press",  rail="brass", margin=2.5, cls="CLASS VI.", sub="MANUFACTURING MACHINES",  belt="side"),
    "lathe":  dict(obj="HPE_nbr_lathe",  rail="brass", margin=2.5, cls="CLASS VI.", sub="MANUFACTURING MACHINES AND TOOLS", belt="top"),
}
COLS_X = [-60 + 24 * k for k in range(9)]
COLS_Y = [-60 + 24 * k for k in range(6)]

def footprint(name):
    o = bpy.data.objects[name]
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    x0 = min(c.x for c in cs) / FT; x1 = max(c.x for c in cs) / FT
    y0 = min(c.y for c in cs) / FT; y1 = max(c.y for c in cs) / FT
    z1 = max(c.z for c in cs) / FT
    return x0, x1, y0, y1, z1

def near_col(x, y, r=1.2):
    return any(abs(x - cx) < r and abs(y - cy) < r for cx in COLS_X for cy in COLS_Y)

# ---------------- rails: stanchions + sagging rope (fig-29 iron / fig-30 brass) ----------------
def rail(key, x0, x1, y0, y1, style):
    bm = bmesh.new()
    H = 3.0; SP = 6.0
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    posts = []
    for (ax, ay), (bx, by) in zip(corners, corners[1:] + corners[:1]):
        L = math.hypot(bx - ax, by - ay); n = max(1, round(L / SP))
        for k in range(n):
            posts.append((ax + (bx - ax) * k / n, ay + (by - ay) * k / n))
    posts = [p for p in posts if not near_col(*p)]
    n0 = len(bm.faces)
    for (px, py) in posts:
        # turned stanchion: weighted round foot, baluster stem, ball finial
        lathe(bm, [(0, 0), (0.42, 0), (0.42, 0.12), (0.22, 0.22), (0.07, 0.4), (0.06, H - 0.25),
                   (0.10, H - 0.18), (0.13, H - 0.08), (0.10, H + 0.02), (0.0, H + 0.05)], 12,
              Matrix.Translation((px, py, 0)))
    mi(bm, n0, 0)
    n1 = len(bm.faces)
    # rope between neighbouring posts (in order), sag 0.35 ft, open on the back side
    ring = posts + posts[:1]
    for (ax, ay), (bx, by) in zip(ring, ring[1:]):
        if math.hypot(bx - ax, by - ay) > SP * 1.8: continue
        segs = 6
        pts = []
        for s in range(segs + 1):
            t = s / segs
            pts.append((ax + (bx - ax) * t, ay + (by - ay) * t, H - 0.12 - 0.35 * 4 * t * (1 - t)))
        for p, q in zip(pts, pts[1:]): rod(bm, p, q, 0.06, 6)
    mi(bm, n1, 1)
    mats = [M["brass"], M["rope"]] if style == "brass" else [M["iron"], M["rope_buff"]]
    o = add(f"{PREFIX}rail_{key}", bm, mats, "stand_rail")
    return posts

def floorcloth(key, x0, x1, y0, y1, colour="baize"):
    bm = bmesh.new()
    box(bm, x0, x1, y0, y1, 0.0, 0.05)  # felt over boards (floor top z=0)
    # crimson-painted plinth kerb along the front (fig-30 stand base)
    n0 = len(bm.faces)
    box(bm, x0, x1, y0 - 0.25, y0, 0.0, 0.35)
    mi(bm, n0, 1)
    add(f"{PREFIX}floorcloth_{key}", bm, [M[colour], M["stand"]], "stand_floor")

# ---------------- placards with painted lettering ----------------
def text_mesh(s, size, align="CENTER"):
    cu = bpy.data.curves.new("MCD_tmp_txt", "FONT"); cu.body = s; cu.size = size
    cu.align_x = align; cu.align_y = "CENTER"; cu.extrude = 0.004
    ob = bpy.data.objects.new("MCD_tmp_txt", cu); bpy.context.scene.collection.objects.link(ob)
    dg = bpy.context.evaluated_depsgraph_get(); ev = ob.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev)
    bpy.data.objects.remove(ob, do_unlink=True); bpy.data.curves.remove(cu)
    return me

def placard(key, px, py, cls, sub, face=(0, -1)):
    """board 3.0 x 1.6 ft on a 4 ft iron post; letters in feet (finish scales)."""
    bm = bmesh.new()
    W, Hb, zc = 3.0, 1.6, 4.6
    rod(bm, (px, py + 0.12, 0), (px, py + 0.12, zc - Hb / 2), 0.07, 8)
    box(bm, px - 0.35, px + 0.35, py - 0.23, py + 0.47, 0, 0.12)
    mi(bm, 0, 0)
    n0 = len(bm.faces)
    box(bm, px - W / 2, px + W / 2, py - 0.04, py + 0.04, zc - Hb / 2, zc + Hb / 2); mi(bm, n0, 1)
    n1 = len(bm.faces)
    t = 0.07  # gilt frame
    for (a0, a1, b0, b1) in ((-W/2 - t, W/2 + t, Hb/2, Hb/2 + t), (-W/2 - t, W/2 + t, -Hb/2 - t, -Hb/2),
                             (-W/2 - t, -W/2, -Hb/2, Hb/2), (W/2, W/2 + t, -Hb/2, Hb/2)):
        box(bm, px + a0, px + a1, py - 0.07, py + 0.05, zc + b0, zc + b1)
    mi(bm, n1, 2)
    n2 = len(bm.faces)
    for s, size, dz in ((cls, 0.48, 0.28), (sub, 0.17 if len(sub) > 24 else 0.21, -0.32)):
        me = text_mesh(s, size)
        tb = bmesh.new(); tb.from_mesh(me); bpy.data.meshes.remove(me)
        # text lies in XY; stand it up facing -Y on the board front
        bmesh.ops.transform(tb, matrix=Matrix.Translation((px, py - 0.05, zc + dz)) @ Matrix.Rotation(math.radians(90), 4, "X"), verts=tb.verts)
        tmp = bpy.data.meshes.new("MCD_tmp"); tb.to_mesh(tmp); tb.free()
        bm.from_mesh(tmp); bpy.data.meshes.remove(tmp)
    mi(bm, n2, 3)
    o = add(f"{PREFIX}placard_{key}", bm, [M["iron"], M["board"], M["gilt"], M["letter"]], "stand_placard")
    if face != (0, -1):
        # rotate about the post
        ang = math.atan2(face[0], -face[1])
        o.data.transform(Matrix.Translation((ft(px), ft(py), 0)) @ Matrix.Rotation(ang, 4, "Z") @ Matrix.Translation((-ft(px), -ft(py), 0)))
    return o

# ---------------- pulleys, line shafts, belts ----------------
def pulley(bm, cx, cy, cz, r, w, spokes=6, axis="X"):
    """flat-faced belt pulley / flywheel: rim, hub, spokes; axis along X (shafts run E-W)."""
    R = Matrix.Rotation(math.radians(90), 4, "Y") if axis == "X" else Matrix.Rotation(math.radians(90), 4, "X")
    T = Matrix.Translation((cx, cy, cz)) @ R
    rim_t = max(0.12, r * 0.08)
    lathe(bm, [(r - rim_t, -w / 2), (r, -w / 2), (r, w / 2), (r - rim_t, w / 2)], 32, T)
    lathe(bm, [(0, -w / 2 - 0.05), (max(0.25, r * 0.16), -w / 2 - 0.05), (max(0.25, r * 0.16), w / 2 + 0.05), (0, w / 2 + 0.05)], 16, T)
    for k in range(spokes):
        a = 2 * math.pi * k / spokes
        p = T @ Vector((0.0, 0.0, 0.0)); q = T @ Vector(((r - rim_t) * math.cos(a), (r - rim_t) * math.sin(a), 0))
        rod(bm, p, q, max(0.05, r * 0.035), 6)

def belt(bm, a, ra, b, rb, w):
    """open flat belt in the Y-Z plane (shaft axes along X): two straight runs tangent to both pulleys."""
    ax, ay, az = a; bx, by, bz = b
    d = Vector((by - ay, bz - az)); L = d.length; u = d / L
    # external tangent: angle offset
    s = math.asin(max(-1, min(1, (ra - rb) / L)))
    nrm = Vector((-u.y, u.x))
    for sign in (1, -1):
        # rotate normal by sign*s
        c, sn = math.cos(sign * s), math.sin(sign * s)
        n = Vector((nrm.x * c - nrm.y * sn, nrm.x * sn + nrm.y * c)) * sign
        pa = Vector((ay, az)) + n * ra; pb = Vector((by, bz)) + n * rb
        t = 0.03
        vs = []
        for (yy, zz) in (pa, pb):
            for dx in (-w / 2, w / 2):
                vs.append(bm.verts.new((ax + dx, yy, zz)))
        # thin double-sided strip with a little thickness
        vs2 = [bm.verts.new((v.co.x, v.co.y + n.x * t, v.co.z + n.y * t)) for v in vs]
        bm.faces.new([vs[0], vs[1], vs[3], vs[2]]); bm.faces.new([vs2[2], vs2[3], vs2[1], vs2[0]])
        bm.faces.new([vs[0], vs[2], vs2[2], vs2[0]]); bm.faces.new([vs[1], vs2[1], vs2[3], vs[3]])

def line_shaft(key, x0, x1, y, z, hangers_x, col_brackets_x):
    bm = bmesh.new()
    rod(bm, (x0, y, z), (x1, y, z), 1.75 / 12, 12)            # 3 1/2 in turned shaft
    # couplings every 12 ft
    x = x0 + 6
    while x < x1:
        lathe(bm, [(0, -0.35), (0.3, -0.35), (0.3, 0.35), (0, 0.35)], 12, Matrix.Translation((x, y, z)) @ Matrix.Rotation(math.radians(90), 4, "Y"))
        x += 12
    mi(bm, 0, 0)
    n0 = len(bm.faces)
    gz = P.GIRDER_D if hasattr(P, "GIRDER_D") else 3.0
    under = 22.0 + 2.0 / 12 - gz  # gallery girder soffit, ft
    for hx in hangers_x:     # drop hangers from the gallery girder (pair of rods + plummer block)
        box(bm, hx - 0.6, hx + 0.6, y - 0.9, y + 0.5, under - 0.12, under)
        for dx in (-0.35, 0.35):
            rod(bm, (hx + dx, y - 0.6, under), (hx + dx, y, z + 0.25), 0.07, 6)
        box(bm, hx - 0.45, hx + 0.45, y - 0.3, y + 0.3, z - 0.25, z + 0.35)
    for cx in col_brackets_x:   # cast bracket bolted to the column face
        cy = min(COLS_Y, key=lambda v: abs(v - y))
        side = 1 if y > cy else -1
        rod(bm, (cx, cy + side * 0.34, z + 1.6), (cx + 0.0, y, z + 0.3), 0.09, 6)
        rod(bm, (cx, cy + side * 0.34, z - 1.2), (cx + 0.0, y, z - 0.2), 0.09, 6)
        box(bm, cx - 0.3, cx + 0.3, cy + side * 0.33 - 0.06, cy + side * 0.33 + 0.06, z - 1.4, z + 1.8)
        box(bm, cx - 0.45, cx + 0.45, y - 0.3, y + 0.3, z - 0.25, z + 0.35)
    mi(bm, n0, 1)
    add(f"{PREFIX}lineshaft_{key}", bm, [M["shaft"], M["hanger"]], "line_shaft")

def drive(key, shaft_pt, r_shaft, mach_pt, r_mach, w, big=False):
    bm = bmesh.new()
    pulley(bm, *shaft_pt, r_shaft, w + 0.15, 6)
    pulley(bm, *mach_pt, r_mach, w + 0.15 if not big else 0.9, 8 if big else 6)
    # stub shaft + bearing pedestal through the machine pulley
    x, y, z = mach_pt
    rod(bm, (x - 0.6, y, z), (x + 1.4, y, z), 0.16, 10)
    mi(bm, 0, 0)
    n0 = len(bm.faces)
    belt(bm, shaft_pt, r_shaft + 0.03, mach_pt, r_mach + 0.03, w)
    mi(bm, n0, 1)
    add(f"{PREFIX}drive_{key}", bm, [M["pulley"], M["belt"]], "belt_drive")

# ---------------- people (vendored people_lib, baked into the candidate) ----------------
def person(name, role, pose, x, y, face_to, lod="hero", seed=None):
    import people_lib as PL   # vendored copy in this scripts/ folder
    body = PL._build_person(role, pose, lod, seed if seed is not None else (abs(hash(name)) % 997))
    body.name = PREFIX + name
    for c in list(body.users_collection): c.objects.unlink(body)
    coll.objects.link(body)
    dx, dy = face_to[0] - x, face_to[1] - y
    body.rotation_euler = (0, 0, math.atan2(dx, -dy))   # HBM faces -Y
    body.location = (ft(x), ft(y), 0)
    body["candidate"] = CAND; body["cp_era"] = "HP1851"; body["mcd_role"] = role
    # baked here with an explicit role; drop the swap tag so render-time swap_scene_people
    # (which re-infers kind from the name and may flip sex) leaves these figures alone
    for k in ("cpl_people",):
        if k in body: del body[k]
    body["mcd_people_baked"] = PL.PEOPLE_VERSION
    return body

# =============================== build ===============================
report = []
for key, S in STANDS.items():
    x0, x1, y0, y1, ztop = footprint(S["obj"]); m = S["margin"]
    S.update(fp=(x0, x1, y0, y1, ztop), rail_box=(x0 - m, x1 + m, y0 - m, y1 + m))
if "engine" in STANDS:   # flywheel stands west of the engine block: widen that side
    rb = STANDS["engine"]["rail_box"]; STANDS["engine"]["rail_box"] = (rb[0] - 2.0, rb[1], rb[2], rb[3])

for key, S in STANDS.items():
    rx0, rx1, ry0, ry1 = S["rail_box"]
    floorcloth(key, rx0 + 0.3, rx1 - 0.3, ry0 + 0.3, ry1 - 0.3)
    if DO_RAILS:
        posts = rail(key, rx0, rx1, ry0, ry1, S["rail"]); report.append((key, "posts", len(posts)))
    if DO_PLACARDS:
        # front (aisle, -Y) side, just outside the rail, offset toward the camera-side end
        px = rx0 + 2.2 if key in ("engine", "lathe") else rx1 - 2.2
        face = (0, -1)
        if key == "boiler":
            px += BOILER_PLACARD_DX
            if BOILER_PLACARD_YAW:
                a = math.radians(BOILER_PLACARD_YAW); face = (math.sin(a), -math.cos(a))
        placard(key, px, ry0 - 1.0, S["cls"], S["sub"], face=face)

if DO_SHAFTS:
    z = SHAFT_Z
    # north line (y=+13 ft, 1 ft off the y=+12 column line): press -> hammer bay -> lathe
    line_shaft("north", 56.0, 140.0, 13.0, z, hangers_x=(72.0, 96.0, 120.0), col_brackets_x=(60.0, 84.0, 108.0, 132.0))
    # south line (y=-13): engine bay only, kept east of the CP024_ram frustum
    line_shaft("south", 113.0, 144.0, -13.0, z, hangers_x=(120.0,), col_brackets_x=(132.0,))
    px0, px1, py0, py1, pz = STANDS["press"]["fp"]
    drive("press", (68.0, 13.0, z), 1.5, (px0 + 2.0, py0 - 0.6, 9.0), 1.1, 0.42)
    lx0, lx1, ly0, ly1, lz = STANDS["lathe"]["fp"]
    drive("lathe", ((lx0 + lx1) / 2, 13.0, z), 1.25, ((lx0 + lx1) / 2, (ly0 + ly1) / 2, lz + 1.2), 0.9, 0.33)
    ex0, ex1, ey0, ey1, ez = STANDS["engine"]["fp"]
    # engine flywheel (drives the south line shaft)
    drive("engine", (ex0 - 1.2, -13.0, z), 1.5, (ex0 - 1.2, (ey0 + ey1) / 2, 4.2), 3.4, 0.5, big=True)

if DO_PEOPLE:
    # attendants inside each rail (frock coat, top hat), an engine-man at the flywheel,
    # and a few visitors at the rails (fig-29 / fig-30 rail-side groups). None in the ram frame.
    G, W, L = "1850s_gentleman", "1850s_workman", "1850s_lady"
    def inside(key, fx, fy):
        rx0, rx1, ry0, ry1 = STANDS[key]["rail_box"]; return rx0 + (rx1 - rx0) * fx, ry0 + (ry1 - ry0) * fy
    ppl = []
    bx, by = inside("boiler", 0.52, 0.20); ppl.append(("attendant_boiler", G, "pointing", bx, by, (bx - 4, by - 10), 11))
    ex, ey = inside("engine", 0.10, 0.30); ppl.append(("engineman_engine", W, "working", ex, ey, (ex + 4, ey), 5))
    ax_, ay_ = inside("engine", 0.70, 0.18); ppl.append(("attendant_engine", G, "standing", ax_, ay_, (ax_ - 6, ay_ - 10), 3))
    lx, ly = inside("lathe", 0.22, 0.25); ppl.append(("attendant_lathe", G, "pointing", lx, ly, (lx + 1, ly + 6), 7))
    # visitors at the engine/lathe rails, facing the machines
    rx0, rx1, ry0, ry1 = STANDS["engine"]["rail_box"]
    ppl.append(("visitor_engine_a", L, "standing", rx0 + 6.0, ry0 - 2.2, (rx0 + 6.5, ry0 + 4), 2))
    ppl.append(("visitor_engine_b", G, "standing", rx0 + 8.2, ry0 - 2.0, (rx0 + 7.5, ry0 + 4), 9))
    rx0, rx1, ry0, ry1 = STANDS["boiler"]["rail_box"]
    ppl.append(("visitor_boiler_a", G, "standing", rx0 + 3.0, ry0 - 2.0, (rx0 + 3.5, ry0 + 5), 13))
    for (n, role, pose, x, y, ft_, sd) in ppl:
        person(n, role, pose, x, y, ft_, seed=sd); report.append((n, round(x, 1), round(y, 1)))

txt = bpy.data.texts.get("CREDIT_MCD_CAND") or bpy.data.texts.new("CREDIT_MCD_CAND")
txt.clear()
txt.write(
    "CANDIDATE e02_machinery_dress (2026-11-02, Grok Bot) — CP024 Machinery Court, Hyde Park 1851\n"
    "Dressing refs (not measurements): scans fig-29 (Hibbert, Platt rail + line shafting),\n"
    "fig-30 (De la Rue brass stanchions, crimson rope, green floor cloth, placard), fig-48, fig-21.\n"
    "Adds: green floor cloths + crimson kerbs, rope rails (iron/buff for Class V, brass/crimson for Class VI),\n"
    "painted class placards, N+S line shafts on column brackets and gallery-girder drop hangers,\n"
    "leather belts to press/lathe and an engine flywheel, attendants + rail visitors (people_lib vendored).\n"
    "Hammer, envelope and block-outs untouched. See DEPARTURES EX_MCD_*.\n")
print("MCD_REPORT", report, flush=True)
bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out, flush=True)
