"""CP068 — The method outlives the building. Present-day study: K-JOINT kit + one prefabricated bay
in today's park light. Reuses parts1851 (same kit as m01 K_JOINT). Lean: no DEP/ARR/MAP.
  blender -b --factory-startup -P scripts/build_legacy_today.py -- --out rounds/m03_legacy.blend
"""
import bpy, bmesh, math, sys, os, json
from mathutils import Vector, Matrix
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
OUT = arg("--out", "rounds/m03_legacy.blend")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOTDIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import parts1851 as P
from common import *
from parts1851 import box, rod, finish, I
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
sc = bpy.context.scene
ROOT = bpy.data.collections.new("LEGACY_TODAY_GROK"); sc.collection.children.link(ROOT)
info = {"scene": "CP068", "note": "analytical model study in present-day park light; not archaeological survival"}

PAINT = mat("GT_IronPaintKit", (0.19, 0.27, 0.40), 0.5, 0.0)
WI = mat("GT_WroughtIronKey", (0.055, 0.055, 0.06), 0.42, 0.7)
OAKK = mat("GT_OakKey", (0.40, 0.27, 0.15), 0.7)
OAK = mat("GT_OakBearer", (0.30, 0.23, 0.16), 0.85)
DEAL = mat("GT_Deal", (0.52, 0.42, 0.30), 0.8)
GRASS = noisy_mat("GT_GrassToday", (0.12, 0.22, 0.07), (0.22, 0.32, 0.11), 0.08, 0.95, 0.15)
PATH = noisy_mat("GT_ParkPath", (0.42, 0.40, 0.34), (0.55, 0.52, 0.44), 1.2, 0.95, 0.35)
PLINTH = mat("GT_StudyPlinth", (0.55, 0.54, 0.50), 0.75)

def ground_patch(name, c, x0, x1, y0, y1, matl, res=8.0):
    bm = bmesh.new(); nx = int((x1 - x0) / res) + 1; ny = int((y1 - y0) / res) + 1
    vs = [[bm.verts.new((x0 + i * (x1 - x0) / (nx - 1), y0 + j * (y1 - y0) / (ny - 1), 0)) for j in range(ny)] for i in range(nx)]
    for i in range(nx - 1):
        for j in range(ny - 1): bm.faces.new([vs[i][j], vs[i + 1][j], vs[i + 1][j + 1], vs[i][j + 1]])
    o = obj(name, finish(bm, name, [matl]), c, part_kind="ground")
    for p in o.data.polygons: p.use_smooth = True
    return o

# ---- park ground (today light will hit grass + path) ----
PC = coll("PARK_TODAY", ROOT)
ground_patch("TODAY_GRASS", PC, -120, 120, -80, 100, GRASS, 12.0)
bm = bmesh.new(); box(bm, -8, 55, -18, 18, -0.02, 0.04)
obj("TODAY_PATH", finish(bm, "path", [PATH]), PC, part_kind="path")
# low study plinth under the kit (explicitly analytical, not a ruin)
bm = bmesh.new(); box(bm, -6, 6, -6, 6, 0.0, 0.35)
obj("TODAY_PLINTH", finish(bm, "plinth", [PLINTH]), PC, part_kind="plinth")

# ---- K-JOINT kit (reuse parts1851 recipe from build_move K region) ----
KC = coll("K_JOINT", ROOT)
Z0 = 1.7
bm = bmesh.new()
box(bm, -1.4, 1.4, -1.4, 1.4, 0.35, 0.85)
for s in (-1, 1): box(bm, -2.6, 2.6, s * 0.9 - 0.3, s * 0.9 + 0.3, 0.35, 0.7)
obj("K_SOLE", finish(bm, "k_sole", [OAK]), KC, part_kind="stand")
bm = bmesh.new(); P.add_column(bm, Z0 - 0.85, bot_flange=False, M=Matrix.Translation((0, 0, 0.85)))
P.add_column(bm, 1.1, top_flange=False, M=Matrix.Translation((0, 0, Z0 + P.CONN_L)))
obj("K_COLUMN_STUBS", finish(bm, "k_col_stubs", [PAINT]), KC, part_kind="column")
bm = bmesh.new(); P.add_connecting_piece(bm, M=Matrix.Translation((0, 0, Z0)))
obj("K_CONNECTING_PIECE", finish(bm, "k_conn", [PAINT]), KC, part_kind="connecting_piece", length_ft=P.CONN_L)
GZ = Z0 + P.GIRDER_TOP_IN_CP
def k_girder(face, pull=0.0, tag=""):
    a = math.radians(90 * face)
    d = P.COL_R + 0.25 * I + P.GIRDER_L / 2 + pull
    M = Matrix.Rotation(a, 4, 'Z') @ Matrix.Translation((d, 0, GZ))
    bm = bmesh.new(); P.add_girder(bm, M)
    o = obj(f"K_GIRDER_{tag}", finish(bm, f"k_girder_{tag}", [PAINT]), KC, part_kind="girder")
    far = Matrix.Rotation(a, 4, 'Z'); tz = GZ - P.GIRDER_D
    bm = bmesh.new()
    for dx in (19.0, 22.0):
        for s in (-1, 1):
            p0 = far @ Vector((dx, s * 1.3, 0.35)); p1 = far @ Vector((dx, s * 0.25, tz))
            rod(bm, p0, p1, 0.12, 6)
        q0 = far @ Vector((dx, 0, tz - 0.25)); box(bm, q0.x - 0.4, q0.x + 0.4, q0.y - 0.4, q0.y + 0.4, tz - 0.3, tz)
    obj(f"K_TRESTLE_{tag}", finish(bm, f"k_trestle_{tag}", [DEAL]), KC, part_kind="trestle")
    return o
k_girder(0, 0.0, "E_ironkeys"); k_girder(1, 0.0, "N_oakkeys"); k_girder(2, 0.0, "W_driven")
bm = bmesh.new(); P.add_keys(bm, Matrix.Translation((0, 0, Z0)), driven=True)
obj("K_KEYS_IRON_E", finish(bm, "k_keys_iron", [WI]), KC, part_kind="key")
bm = bmesh.new(); P.add_keys(bm, Matrix.Translation((0, 0, Z0)) @ Matrix.Rotation(math.radians(90), 4, 'Z'), driven=True)
obj("K_KEYS_OAK_N", finish(bm, "k_keys_oak", [OAKK]), KC, part_kind="key")
info["kjoint"] = {"conn_bottom_ft": Z0, "girder_top_ft": round(GZ, 4)}

# ---- single prefabricated bay (24 ft x 24 ft, tier-1) standing east of the kit ----
BC = coll("PREFAB_BAY", ROOT)
BX, BY = 36.0, 0.0
COL_H = 18 + 8 / 12
bm = bmesh.new()
for sx in (-12.0, 12.0):
    for sy in (-12.0, 12.0):
        P.add_column(bm, COL_H, M=Matrix.Translation((BX + sx, BY + sy, 0.02)))
        P.add_connecting_piece(bm, M=Matrix.Translation((BX + sx, BY + sy, COL_H)))
zg = COL_H + P.GIRDER_TOP_IN_CP
for sx in (-12.0, 12.0):
    P.add_girder(bm, Matrix.Translation((BX + sx, BY, zg)) @ Matrix.Rotation(math.radians(90), 4, 'Z'))
for sy in (-12.0, 12.0):
    P.add_girder(bm, Matrix.Translation((BX, BY + sy, zg)))
obj("BAY_FRAME", finish(bm, "bay_frame", [PAINT]), BC, part_kind="prefab_bay",
    note="one 24ft bay: four columns, four girders, four connecting pieces — analytical, not a ruin")
# thin concrete pad under bay (museum-study feel)
bm = bmesh.new(); box(bm, BX - 14, BX + 14, BY - 14, BY + 14, 0.0, 0.08)
obj("BAY_PAD", finish(bm, "bay_pad", [PLINTH]), BC, part_kind="pad")
info["bay"] = {"span_ft": 24, "columns": 4, "girders": 4}

# ---- present-day park light (clearer, higher sun than 1852 yard) ----
world(sun_elev=48, sun_rot=200, strength=0.42, sun_energy=4.0, exposure=-0.25, sun_color=(1.0, 0.98, 0.94))
sc.cycles.samples = 32
sc.render.resolution_x = 1280; sc.render.resolution_y = 720

# ---- cameras: park establish + kit detail + bay ----
route = {
 "set": "LEGACY TODAY (CP068)",
 "units": "feet; pos z = eye height",
 "grammar": "eye 5.25 ft, 35/50 mm, no roll",
 "shots": [
  {"id": "CP068_park", "storyboard": "CP068", "lens_mm": 35,
   "start": {"pos_ft": [-22.0, -28.0, 5.25], "look_ft": [18.0, 0.0, 10.0], "abs_z": True},
   "note": "present-day park light: kit + bay as study objects on grass"},
  {"id": "CP068_kit", "storyboard": "CP068", "lens_mm": 50, "fstop": 5.6,
   "start": {"pos_ft": [3.2, -4.0, 5.25], "look_ft": [0.2, 0.1, 4.6], "abs_z": True, "focus_ft": 5.0},
   "note": "K-JOINT component detail — analytical study"},
  {"id": "CP068_bay", "storyboard": "CP068", "lens_mm": 35,
   "start": {"pos_ft": [18.0, -32.0, 5.25], "look_ft": [36.0, 0.0, 12.0], "abs_z": True},
   "note": "single prefabricated bay standing alone"}
 ]
}
rp = os.path.join(ROOTDIR, "route", "camera_route_cp068.json")
os.makedirs(os.path.dirname(rp), exist_ok=True)
json.dump(route, open(rp, "w"), indent=1)
# also append CP068 into main route for coverage
main_rp = os.path.join(ROOTDIR, "route", "camera_route.json")
main = json.load(open(main_rp))
ids = {s["id"] for s in main["shots"]}
for s in route["shots"]:
    if s["id"] not in ids: main["shots"].append(s)
json.dump(main, open(main_rp, "w"), indent=1)

cams = cameras(rp, ROOT)
info["cams"] = [c.name for c in cams]; info["objects"] = len(bpy.data.objects)
sc["grok_move"] = json.dumps(info)
print("LEGACY_INFO", json.dumps(info), flush=True)
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True)
print("SAVED", OUT)
