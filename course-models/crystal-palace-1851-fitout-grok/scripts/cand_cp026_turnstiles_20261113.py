"""CP026 "A shilling changes the audience" turnstiles CANDIDATE (2026-11-13, DEPARTURES FT95-FT100). NOT live, no verdict.
  blender -b -P scripts/cand_cp026_turnstiles_20261113.py -- --src rounds/h03.blend --out rounds/candidates/h03_cp026turnstiles.blend
Hyde Park 1851 HP51 state (h03, shilling days, summer 1851) only; nothing Sydenham.

Live CP026_turnstiles_start (28 mm) stands inside the south entrance at (-8, -174) ft, eye 5.25 ft, looking south-south-east at
(2, -198, 4): the money-takers, the four turnstiles and the lanes, with the shilling queue coming in through the south doors.
In live h03 the central 24 ft bay of the south transept end (x -12..+12, y = -204) has NO wall at all: build_transept.py builds
the ground-tier wall only for x -36..-12 and 12..36 ("doorways left open"), the closed SOUTH_DOORS slabs were the only fill, and
state_common.open_south_doors() (FT06) swings them open, which leaves six 14 ft leaves standing free in a 24 ft x 19 ft hole.
From inside that hole fills the middle of the frame with open sky over a flat lawn running to the horizon (GROUND_PARK is the
only thing south of the apron), so the entrance reads as a gap in a stage set, not as doors in the building.
  FT95  entrance frame for the central bay, Downes Plate XXI (exit doors) / Plate XXII Figs 17-18: wood columns B at x = +-4
        (5 x 6 in, the same section as the wall-frame posts on either side), door posts beside each 6 ft opening, a 6 in square
        door head at 14 ft (the FT06 leaf height), a sash sill and a glazed sash over each door up to the top rail at 16.67 ft
        (the same rail height as the flanking WALL_SE1 frames). No threshold rail across the openings.
  FT96  the tier-1 louvre band over the central bay (16.9-19.0 ft), an instance of the flanking WLOUV_SE1 mesh (wall_louvre).
  FT97  the Kensington Road side tree row seen through the doors: one row at y = -520 +- 12 ft, 115-150 ft spacing, x -700..700
        (the exterior model's rule, crystal-palace-1851-exterior-grok EX22/EX31), as linked instances of this file's three
        transept elms (64/78/84 ft) scaled 0.9-1.05.
  FT98  nothing else changes: figures (people_lib runs at render time), turnstiles, lanes, pay boxes, the FT06 door leaves, the
        FT57 boarding, lighting, world, exposure and cameras are untouched; nothing is hidden or deleted.
"""
import bpy, bmesh, math, os, sys, random, glob, json
from mathutils import Vector, Matrix
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
SRC, OUT = arg("--src"), arg("--out")
assert os.path.abspath(SRC) != os.path.abspath(OUT), "refusing to overwrite the source blend"
HERE = os.path.dirname(os.path.abspath(__file__))
for live in glob.glob(os.path.join(HERE, "..", "rounds", "*.blend*")):
    assert os.path.abspath(OUT) != os.path.abspath(live), "refusing to overwrite a live rounds/*.blend"
assert "/rounds/candidates/" in os.path.abspath(OUT), "candidate must go to rounds/candidates/"
bpy.ops.wm.open_mainfile(filepath=SRC)
info0 = json.loads(bpy.context.scene.get("grok_build", "{}"))
assert info0.get("state") == "hp51", "source must be an hp51 round (live h03)"
assert "SOUTH_DOORS_OPEN" in bpy.data.objects and "WALL_SE1_mid_0" not in bpy.data.objects, "source must have the open south doors and no central SE1 wall"
assert not any(o.name.startswith("C26T_") for o in bpy.data.objects), "source already has the candidate"
try: bpy.context.preferences.filepaths.save_version = 0
except Exception: pass
sc = bpy.context.scene
FT = 0.3048
def ft(v): return v * FT
def inch(v): return v * FT / 12
TAG = "cp026_turnstiles_20261113"
Y = -204.0
col = bpy.data.collections.new("C26T_ENTRANCE"); sc.collection.children.link(col)
coll_t = bpy.data.collections.new("C26T_PARK_TREES"); sc.collection.children.link(coll_t)
TIMBER = bpy.data.materials["GT_Timber"]; GLASS = bpy.data.materials["GT_Glass"]
n_new = {"entrance": 0, "trees": 0}

def box(bm, x0, x1, y0, y1, z0, z1):   # metres
    r = bmesh.ops.create_cube(bm, size=1.0)
    for v in r["verts"]:
        v.co = Vector(((x0 + x1) / 2 + v.co.x * (x1 - x0), (y0 + y1) / 2 + v.co.y * (y1 - y0), (z0 + z1) / 2 + v.co.z * (z1 - z0)))
def obj(name, me, coll, loc=(0, 0, 0), rz=0.0, **props):
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    ob.location = Vector(loc); ob.rotation_euler = (0, 0, rz)
    ob[TAG] = props.pop("ft", ""); ob["credit"] = "Grok"
    for k, v in props.items(): ob[k] = v
    return ob

# ---------------- FT95: entrance frame (x -12..+12 at y = -204) ----------------
DOORS = (-8.0, 0.0, 8.0)            # FT06 door centres; 6 ft openings (leaves hinge at xc +- 2.88)
DOOR_H = 14.0                       # FT06 leaf height = underside of the door head
POST_HALF = 2.5 / 12                # 5 in wide wall-frame posts (mesh_wall_bay), here the wood columns B
DEPTH = 3 / 12                      # +-3 in, the wall-frame depth
H = 16 + 8 / 12                     # top rail top = flanking WALL_SE1 frame height (19.17 - 2.5 louvre)
bm = bmesh.new()
for xb in (-4.0, 4.0):              # wood columns B between the three 8 ft compartments
    box(bm, ft(xb - POST_HALF), ft(xb + POST_HALF), ft(Y - DEPTH), ft(Y + DEPTH), 0, ft(H))
door_posts = []
for xc in DOORS:
    for sx in (-1, 1):              # door posts: from the opening edge to the next column/post face
        xa = xc + 3.0 * sx; xb = (xc + 4.0 * sx) - POST_HALF * sx   # B column at +-4, frame posts at +-12 (WALL_SE1_*)
        lo, hi = sorted((xa, xb)); door_posts.append(hi - lo)
        box(bm, ft(lo), ft(hi), ft(Y - 0.25), ft(Y + 0.25), 0, ft(DOOR_H + 0.5))
box(bm, ft(-12 + POST_HALF), ft(12 - POST_HALF), ft(Y - 0.25), ft(Y + 0.25), ft(DOOR_H), ft(DOOR_H + 0.5))          # door head 6 in sq
box(bm, ft(-12 + POST_HALF), ft(12 - POST_HALF), ft(Y - 0.30), ft(Y + 0.30), ft(DOOR_H + 0.5), ft(DOOR_H + 0.5 + 4.3 / 12))  # sash sill
box(bm, ft(-12 + POST_HALF), ft(12 - POST_HALF), ft(Y - DEPTH), ft(Y + DEPTH), ft(H) - inch(5), ft(H))             # top rail
zs0, zs1 = DOOR_H + 0.5 + 4.3 / 12, H - 5 / 12
for xc in DOORS:                    # sash bars over each door: 2 verticals per 8 ft compartment (as the wall frames' sash bars)
    for dx in (-1.6, 1.6):
        box(bm, ft(xc + dx) - inch(1), ft(xc + dx) + inch(1), ft(Y) - inch(1), ft(Y) + inch(1), ft(zs0), ft(zs1))
me = bpy.data.meshes.new("c26t_entrance_frame"); bm.to_mesh(me); bm.free(); me.materials.append(TIMBER)
obj("C26T_WALL_SE1_mid_frame", me, col, part_kind="wall", ft="FT95 entrance frame")
bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
for xc in DOORS:
    vs = [bm.verts.new((ft(x), ft(Y), ft(z))) for (x, z) in ((xc - 3.0, zs0), (xc + 3.0, zs0), (xc + 3.0, zs1), (xc - 3.0, zs1))]
    f = bm.faces.new(vs)
    for lp in f.loops: lp[uvl].uv = (lp.vert.co.x / FT, lp.vert.co.z / FT)
for x0, x1 in ((-11.79, -11.0), (-5.0, -3.0), (3.0, 5.0), (11.0, 11.79)):   # glass over the door posts / B columns too
    vs = [bm.verts.new((ft(x), ft(Y), ft(z))) for (x, z) in ((x0, zs0), (x1, zs0), (x1, zs1), (x0, zs1))]
    f = bm.faces.new(vs)
    for lp in f.loops: lp[uvl].uv = (lp.vert.co.x / FT, lp.vert.co.z / FT)
me = bpy.data.meshes.new("c26t_entrance_sash_glass"); bm.to_mesh(me); bm.free(); me.materials.append(GLASS)
obj("C26T_WALL_SE1_mid_sash", me, col, part_kind="wall_fill", ft="FT95 sash over the doors")
n_new["entrance"] += 2
# ---------------- FT96: louvre band over the central bay ----------------
lv = bpy.data.objects["WLOUV_SE1_12_0"]
o = obj("C26T_WLOUV_SE1_mid", lv.data, col, (ft(0.0), lv.location.y, lv.location.z), lv.rotation_euler.z, part_kind="louvre", ft="FT96 louvre band")
n_new["entrance"] += 1
# ---------------- FT97: Kensington Road side tree row (exterior EX22/EX31 positions rule, transept elm meshes) ----------------
# Row and spacing as the exterior model (one row at y = -520 +- 12 ft, 115-150 ft apart). The trees themselves are linked
# instances of this file's own three transept elms (ELM_SOUTH 78 ft, ELM_NORTH 84 ft, ELM_NORTH2 64 ft; leaf cards + wood),
# scaled 0.9-1.05, so they match the elms inside the transept; the exterior's icosphere trees read as toy lollipops here.
ELMS = (("ELM_SOUTH", 4.0, -128.0), ("ELM_NORTH", -3.0, 142.0), ("ELM_NORTH2", 12.0, 98.0))
rt = random.Random(1851 + 26); x = -700.0 + rt.uniform(0, 30); rows = []
while x < 700:
    p = (x, -520.0 + rt.uniform(-12, 12)); k = n_new["trees"] % 3; nm, bx, by = ELMS[k]
    e = bpy.data.objects.new(f"C26T_TREE_{n_new['trees']:02d}", None); coll_t.objects.link(e)
    e.location = (ft(p[0]), ft(p[1]), 0); e.rotation_euler = (0, 0, rt.uniform(0, 6.28)); sc_ = rt.uniform(0.9, 1.05); e.scale = (sc_, sc_, sc_)
    e[TAG] = "FT97 Kensington Road side row (EX31 rule, transept elm instance)"; e["part_kind"] = "park_tree"; e["credit"] = "Grok"
    for part in ("LEAVES", "WOOD"):
        src = bpy.data.objects[f"{nm}_{part}"]
        c = obj(f"C26T_TREE_{n_new['trees']:02d}_{part}", src.data, coll_t, (-ft(bx), -ft(by), 0), part_kind="park_tree", ft="FT97")
        c.parent = e; c.matrix_parent_inverse.identity()
    rows.append([round(p[0], 1), round(p[1], 1), nm, round(sc_, 3)]); n_new["trees"] += 1
    x += rt.uniform(115, 150)

info0.setdefault("state_info", {})["cp026_turnstiles_candidate"] = {"tag": TAG, "new": n_new, "door_posts_ft": sorted({round(d, 3) for d in door_posts}), "trees": rows}
sc["grok_build"] = json.dumps(info0)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True)
print("CP026T_CANDIDATE_SAVED", OUT, json.dumps(n_new), "door posts", sorted({round(d, 3) for d in door_posts}), "trees", len(rows))
