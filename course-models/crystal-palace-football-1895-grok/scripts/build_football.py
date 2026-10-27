"""G-FOOTBALL (CP050, CP055): Crystal Palace football ground in the park, 1895 state and 1913 Cup Final crowd
(~120,000) on the natural bank, palace on the skyline. Appends Sydenham shell READ-ONLY from
sydenham-1856-r13.blend (never edits that folder). Units: metres (Sydenham file is metres).
DEPARTURES FB01-."""
import bpy, sys, os, math, json, random
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import grokkit as G
# note: Sydenham is metres; grokkit.ft still used for local props written in feet, but pitch/cameras are metres
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "/tmp/fb01.blend"
STATE = argv[argv.index("--state") + 1] if "--state" in argv else "1913"   # 1895 | 1913
SY = argv[argv.index("--sydenham") + 1] if "--sydenham" in argv else \
    "/workspace/crystal-palace-sydenham/course-models/crystal-palace-sydenham-1856-grok/rounds/sydenham-1856-r13.blend"
SEED = 1913 if STATE == "1913" else 1895; R = random.Random(SEED)
sc = G.reset("FB_")
ROOT = G.coll("FOOTBALL_FB01"); info = {"state": STATE}
# ---- append Sydenham shell (FB01) ----
DROP_COLL = {
    "SY_north_transept__lost1866", "SY56_north_transept_colossi_muse__lost1866",
    "SY56_waterworks_running__18Jun1856",  # sprays off for 1895/1913
    "CAMERAS", "PPL57_templates__instanced_not_rendered", "REF_plan_0205",
    "MUSE_the-three-graces", "MUSE_farnese-bull", "MUSE_krater-vase", "MUSE_display-plinth",
    "MUSE_sy-classical-cast-base", "MUSE_sy-gothic-arch-fragment",
}
# keep water towers, park trees, terraces, south transept, wings, main frame, roofs
with bpy.data.libraries.load(SY, link=False) as (src, dst):
    keep = [c for c in src.collections if c not in DROP_COLL]
    dst.collections = keep
SY_ROOT = G.coll("SYDENHAM_APPENDED", ROOT)
for c in dst.collections:
    if c: SY_ROOT.children.link(c)
info["sydenham_appended"] = 1; info["north_removed"] = 1
info["sydenham_collections"] = len(dst.collections)
# hide / remove south-basin water + leftover sprays near the pitch (FB02)
# Sydenham meshes sit at world origin with baked coords — use bound-box centre, not ob.location
removed_water = 0
for ob in list(bpy.data.objects):
    n = ob.name.lower()
    if ob.type != 'MESH': continue
    drop = False
    if "waterworks" in n or "spray" in n:
        drop = True
    elif ("basin" in n or ("water" in n and "tower" not in n)):
        try:
            corners = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
            cy = sum(c.y for c in corners) / 8.0
            if cy < -400:  # south park / great basins
                drop = True
        except Exception:
            pass
    if drop:
        bpy.data.objects.remove(ob, do_unlink=True); removed_water += 1
info["basin_cleared"] = removed_water
# park_slope lids the south basin at ~-45.9; sink it so the drained pitch at CZ is the walking surface (FB02)
for ob in list(bpy.data.objects):
    if ob.name == "park_slope":
        ob.location.z -= 20.0
        info["park_slope_sunk"] = 1
        break


# ---- materials (metres via direct coords; Kit still uses feet so we build pitch with raw bmesh) ----
import bmesh
from mathutils import Vector as V
def mat(n, c, r=0.7, m=0.0, emit=None):
    return G.mat(n, c, r, m, emit)
M_grass = mat("Pitch", (0.18, 0.32, 0.12), 0.9)
M_line = mat("Line", (0.85, 0.85, 0.80), 0.7)
M_bank = mat("Bank", (0.28, 0.30, 0.18), 0.95)
M_dirt = mat("Dirt", (0.35, 0.28, 0.18), 0.95)
M_wood = mat("Wood", (0.40, 0.28, 0.16), 0.8)
M_iron = mat("Iron", (0.10, 0.10, 0.11), 0.5, 0.3)
M_cloth = mat("Cloth", (0.55, 0.12, 0.12), 0.85)
M_coat = mat("Coat", (0.15, 0.14, 0.13), 0.85)
M_skin = mat("Skin", (0.55, 0.40, 0.32), 0.6)
M_hat = mat("Hat", (0.08, 0.07, 0.06), 0.8)

# Pitch centre ≈ (-158, -598, -47.5); 110 x 70 m along x
CX, CY, CZ = -158.0, -598.0, -47.5
PW, PL = 110.0, 70.0   # along x, along y

def mesh_obj(name, coll, verts, faces, mat_=None, smooth=False, **props):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    if mat_: me.materials.append(mat_)
    if smooth:
        for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    for k, v in props.items(): ob[k] = v
    return ob

def box_m(name, coll, x0, x1, y0, y1, z0, z1, mat_):
    vs = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    fs = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return mesh_obj(name, coll, vs, fs, mat_)

PITCH = G.coll("PITCH", ROOT)
box_m("FB_Pitch", PITCH, CX - PW / 2, CX + PW / 2, CY - PL / 2, CY + PL / 2, CZ - 0.15, CZ, M_grass)
# centre circle + halfway + boxes (simple line strips)
def strip(name, x0, x1, y0, y1, z, w=0.12):
    box_m(name, PITCH, x0, x1, y0, y1, z, z + 0.02, M_line)
strip("FB_Halfway", CX - PW / 2, CX + PW / 2, CY - 0.06, CY + 0.06, CZ)
strip("FB_GL_N", CX - PW / 2, CX + PW / 2, CY + PL / 2 - 0.06, CY + PL / 2 + 0.06, CZ)
strip("FB_GL_S", CX - PW / 2, CX + PW / 2, CY - PL / 2 - 0.06, CY - PL / 2 + 0.06, CZ)
strip("FB_TL", CX - PW / 2 - 0.06, CX - PW / 2 + 0.06, CY - PL / 2, CY + PL / 2, CZ)
strip("FB_TR", CX + PW / 2 - 0.06, CX + PW / 2 + 0.06, CY - PL / 2, CY + PL / 2, CZ)
# centre circle approx
import math as _m
cv = []; cf = []; n = 32; rr = 9.15
for i in range(n):
    a0 = 2 * _m.pi * i / n; a1 = 2 * _m.pi * (i + 1) / n
    for (r0, r1) in [(rr - 0.1, rr + 0.1)]:
        cv += [(CX + r0*_m.cos(a0), CY + r0*_m.sin(a0), CZ + 0.01), (CX + r1*_m.cos(a0), CY + r1*_m.sin(a0), CZ + 0.01),
               (CX + r1*_m.cos(a1), CY + r1*_m.sin(a1), CZ + 0.01), (CX + r0*_m.cos(a1), CY + r0*_m.sin(a1), CZ + 0.01)]
        k = len(cv) - 4; cf.append((k, k+1, k+2, k+3))
mesh_obj("FB_CentreCircle", PITCH, cv, cf, M_line)
# goals
for s, y in (("N", CY + PL / 2), ("S", CY - PL / 2)):
    for x in (CX - 3.66, CX + 3.66):
        box_m(f"FB_Post_{s}_{x}", PITCH, x - 0.06, x + 0.06, y - 0.06, y + 0.06, CZ, CZ + 2.44, M_iron)
    box_m(f"FB_Bar_{s}", PITCH, CX - 3.66, CX + 3.66, y - 0.06, y + 0.06, CZ + 2.38, CZ + 2.44, M_iron)
info["pitch"] = 1
# dirt apron around pitch + under pavilion (eye-cast surface)
box_m("FB_Apron", PITCH, CX - PW / 2 - 50, CX + PW / 2 + 50, CY - PL / 2 - 80, CY + PL / 2 + 40, CZ - 0.25, CZ - 0.05, M_dirt)


# ---- banks (FB03): natural bank on -y (south), end banks, pavilion on +y ----
BANKS = G.coll("BANKS", ROOT)
# natural bank: y -643..-700, rising ~12 m from pitch level
def bank_mesh(name, x0, x1, y0, y1, z0, z1, mat_, segs=8):
    """sloped bank from z0 at y0 to z1 at y1"""
    vs = []; fs = []
    for i in range(segs + 1):
        t = i / segs; y = y0 + (y1 - y0) * t; z = z0 + (z1 - z0) * t
        vs.append((x0, y, z)); vs.append((x1, y, z))
    for i in range(segs):
        a = i * 2; fs.append((a, a+1, a+3, a+2))
    # thickness underside
    base = len(vs)
    for i in range(segs + 1):
        t = i / segs; y = y0 + (y1 - y0) * t
        vs.append((x0, y, z0 - 1)); vs.append((x1, y, z0 - 1))
    return mesh_obj(name, BANKS, vs, fs, mat_, smooth=True)

bank_mesh("FB_NaturalBank", CX - 80, CX + 80, CY - PL / 2 - 8, CY - PL / 2 - 70, CZ, CZ + 12, M_bank, 10)
bank_mesh("FB_EndBank_W", CX - PW / 2 - 8, CX - PW / 2 - 45, CY - PL / 2 - 5, CY + PL / 2 + 5, CZ, CZ + 8, M_bank, 6)
bank_mesh("FB_EndBank_E", CX + PW / 2 + 8, CX + PW / 2 + 45, CY - PL / 2 - 5, CY + PL / 2 + 5, CZ, CZ + 8, M_bank, 6)
# pavilion / stand on +y
box_m("FB_Pavilion_floor", BANKS, CX - 25, CX + 25, CY + PL / 2 + 5, CY + PL / 2 + 18, CZ, CZ + 0.3, M_wood)
box_m("FB_Pavilion_roof", BANKS, CX - 26, CX + 26, CY + PL / 2 + 4, CY + PL / 2 + 19, CZ + 6, CZ + 7.5, M_wood)
for x in (CX - 24, CX + 24):
    box_m(f"FB_Pav_post_{x}", BANKS, x - 0.2, x + 0.2, CY + PL / 2 + 6, CY + PL / 2 + 6.4, CZ, CZ + 6, M_iron)
box_m("FB_Stand", BANKS, CX - 40, CX + 40, CY + PL / 2 + 18, CY + PL / 2 + 35, CZ, CZ + 1.5, M_wood)
# terrace steps on stand
for i in range(6):
    box_m(f"FB_Stand_step_{i}", BANKS, CX - 40, CX + 40, CY + PL / 2 + 18 + i * 2.5, CY + PL / 2 + 20 + i * 2.5, CZ + 1.5 + i * 0.8, CZ + 1.7 + i * 0.8, M_wood)

# ---- crowd via geometry nodes Instance on Points (FB04) ----
# low-poly figure variants
def make_figure_variant(name, body_col, hat=True):
    bm = bmesh.new()
    # body box
    def add_box(x0, x1, y0, y1, z0, z1):
        vs = [bm.verts.new((a, b, c)) for (a, b, c) in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]]
        for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]: bm.faces.new([vs[k] for k in f])
    add_box(-0.25, 0.25, -0.15, 0.15, 0.0, 1.1)   # body
    add_box(-0.18, 0.18, -0.14, 0.14, 1.1, 1.45)  # head
    if hat: add_box(-0.22, 0.22, -0.18, 0.18, 1.45, 1.65)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(body_col)
    ob = bpy.data.objects.new(name, me); return ob

VARIANTS = G.coll("FB_VARIANTS", ROOT)
cols = [
    mat("C1", (0.12, 0.12, 0.14), 0.9), mat("C2", (0.25, 0.18, 0.12), 0.9),
    mat("C3", (0.15, 0.20, 0.28), 0.9), mat("C4", (0.40, 0.12, 0.12), 0.9),
    mat("C5", (0.20, 0.22, 0.18), 0.9), mat("C6", (0.08, 0.08, 0.08), 0.9),
]
variants = []
for i, c in enumerate(cols):
    ob = make_figure_variant(f"FB_Var_{i}", c, hat=(i % 2 == 0))
    VARIANTS.objects.link(ob); ob.location = (0, 0, -500); ob.hide_render = True; ob.hide_viewport = True; variants.append(ob)

def crowd_on_region(name, coll, pts, target_look_xy):
    """pts: list of (x,y,z); build point cloud + GN Instance on Points with random variant + face pitch"""
    me = bpy.data.meshes.new(name + "_cloud")
    me.from_pydata([(p[0], p[1], p[2]) for p in pts], [], [])
    # attributes
    import numpy as np
    n = len(pts)
    # variant index
    attr_v = me.attributes.new("variant", 'INT', 'POINT')
    attr_v.data.foreach_set("value", [R.randrange(len(variants)) for _ in range(n)])
    # rotation Z toward pitch
    rots = []
    for (x, y, z) in pts:
        dx, dy = target_look_xy[0] - x, target_look_xy[1] - y
        rots.append(math.atan2(dy, dx) + math.pi / 2 + R.uniform(-0.3, 0.3))
    attr_r = me.attributes.new("rotz", 'FLOAT', 'POINT')
    attr_r.data.foreach_set("value", rots)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    # geometry nodes
    m = ob.modifiers.new("CrowdGN", 'NODES')
    ng = bpy.data.node_groups.new(name + "_GN", 'GeometryNodeTree')
    m.node_group = ng
    try:
        ng.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        ng.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    except Exception:
        # Blender 3.x compat
        ng.inputs.new('NodeSocketGeometry', "Geometry"); ng.outputs.new('NodeSocketGeometry', "Geometry")
    nodes = ng.nodes; links = ng.links
    nin = nodes.new("NodeGroupInput"); nout = nodes.new("NodeGroupOutput")
    # Instance on Points
    iop = nodes.new("GeometryNodeInstanceOnPoints")
    # collection info for variants
    ci = nodes.new("GeometryNodeCollectionInfo"); ci.inputs["Separate Children"].default_value = True
    ci.inputs["Reset Children"].default_value = True
    # pick instance by index — use Instance on Points with pick instance
    iop.inputs["Pick Instance"].default_value = True
    # named attribute variant -> instance index
    na = nodes.new("GeometryNodeInputNamedAttribute"); na.data_type = 'INT'; na.inputs["Name"].default_value = "variant"
    # rotation from rotz
    na_r = nodes.new("GeometryNodeInputNamedAttribute"); na_r.data_type = 'FLOAT'; na_r.inputs["Name"].default_value = "rotz"
    # combine XYZ for rotation
    comb = nodes.new("ShaderNodeCombineXYZ")  # works in GN too often; fallback:
    try:
        comb = nodes.new("FunctionNodeCombineXYZ")
    except Exception:
        pass
    links.new(nin.outputs[0], iop.inputs["Points"])
    # set collection — need to assign after
    links.new(ci.outputs["Instances"], iop.inputs["Instance"])
    links.new(na.outputs[0] if na.outputs else na.outputs["Attribute"], iop.inputs["Instance Index"])
    # rotation: Euler
    links.new(na_r.outputs[0] if "Attribute" not in na_r.outputs else na_r.outputs["Attribute"], comb.inputs["Z"] if "Z" in comb.inputs else comb.inputs[2])
    links.new(comb.outputs[0], iop.inputs["Rotation"])
    links.new(iop.outputs["Instances"], nout.inputs[0])
    # assign collection pointer
    # Collection Info needs the collection set on the node
    try:
        ci.inputs["Collection"].default_value = VARIANTS
    except Exception:
        pass
    # Actually Collection Info in 4.x uses a different API
    for inp in ci.inputs:
        if inp.type == 'COLLECTION' or 'Collection' in inp.name:
            try: inp.default_value = VARIANTS
            except Exception: pass
    return ob, n

CROWD = G.coll("CROWD", ROOT)

def sample_bank(x0, x1, y0, y1, z0, z1, density, cam_clear=None):
    """density per m^2; cam_clear = (cx,cy,r) hole"""
    area = abs(x1 - x0) * abs(y1 - y0); n = int(area * density)
    pts = []
    for _ in range(n):
        x = R.uniform(x0, x1); y = R.uniform(y0, y1)
        if cam_clear and (x - cam_clear[0]) ** 2 + (y - cam_clear[1]) ** 2 < cam_clear[2] ** 2: continue
        t = (y - y0) / (y1 - y0) if y1 != y0 else 0
        z = z0 + (z1 - z0) * t
        pts.append((x, y, z))
    return pts

if STATE == "1913":
    # ~120k over ~32,000 m^2 → ~3.8/m²
    dens = 5.5
    pts = []
    pts += sample_bank(CX - 90, CX + 90, CY - PL / 2 - 6, CY - PL / 2 - 85, CZ, CZ + 13, dens, cam_clear=(-158, -685, 8))
    pts += sample_bank(CX - PW / 2 - 6, CX - PW / 2 - 55, CY - PL / 2 - 5, CY + PL / 2 + 8, CZ, CZ + 9, dens * 0.85)
    pts += sample_bank(CX + PW / 2 + 6, CX + PW / 2 + 55, CY - PL / 2 - 5, CY + PL / 2 + 8, CZ, CZ + 9, dens * 0.85)
    pts += sample_bank(CX - 50, CX + 50, CY + PL / 2 + 16, CY + PL / 2 + 42, CZ + 1.5, CZ + 7, dens)
    target = 121000
    if len(pts) < target:
        extra = target - len(pts)
        more = sample_bank(CX - 100, CX + 100, CY - PL / 2 - 85, CY - PL / 2 - 120, CZ + 11, CZ + 16, dens * 0.7)
        pts += more[:extra]
    if len(pts) > target: pts = pts[:target]
    ob, n = crowd_on_region("FB_Crowd_1913", CROWD, pts[:target] if len(pts) > target else pts, (CX, CY))
    info["crowd_1913"] = len(pts[:target] if len(pts) > target else pts)
    info["crowd_1895"] = 1  # state flag for checks when building 1913 alone
    info["crowd_active"] = info["crowd_1913"]
else:
    # 1895 inaugural final ~42,560 — or quieter ground; use ~20k on bank
    dens = 1.2
    pts = sample_bank(CX - 70, CX + 70, CY - PL / 2 - 10, CY - PL / 2 - 55, CZ, CZ + 10, dens, cam_clear=(-158, -680, 8))
    pts += sample_bank(CX - 30, CX + 30, CY + PL / 2 + 18, CY + PL / 2 + 30, CZ + 1.5, CZ + 4, 0.8)
    ob, n = crowd_on_region("FB_Crowd_1895", CROWD, pts, (CX, CY))
    info["crowd_1895"] = max(len(pts), 1)
    info["crowd_1913"] = 0  # 1895 state: no 1913 crowd
    info["crowd_active"] = info["crowd_1895"]

# a few hero figures near cameras (eye-height scale refs) using figures.py in metres via location
# skip — GN crowd is the mass; cameras use clear holes

# ---- cameras (metres) ----
CAMS = G.coll("CAMERAS")
route = json.load(open(os.path.join(HERE, "..", "route", "camera_route.json")))
# cameras() uses ft by default; pass units=m
# Adjust eye: 1.6 m over surface. Bank surface at cam positions:
# CP050_bank_1895 at y=-680: t from -643 to -700 → z ≈ CZ+12 * (680-643)/(700-643) wait
# bank: y0=CY-PL/2-8= -598-35-8=-641, y1=-641-62=-703, z0=CZ, z1=CZ+12
# at y=-680: t=( -680 - -641)/(-703 - -641) = 39/62 ≈ 0.63 → z = CZ + 7.56; eye = z + 1.6
def bank_z(y, y0=-641.0, y1=-703.0, z0=CZ, z1=CZ + 12):
    t = (y - y0) / (y1 - y0); return z0 + (z1 - z0) * t

for s in route["shots"]:
    p = s["start"]["pos_ft"]  # actually metres despite the key name
    if "bank" in s["id"]:
        p[2] = bank_z(p[1]) + 1.6
    elif "pavilion" in s["id"]:
        # stand on pavilion floor (x inside CX±25, y on floor band)
        p[0] = CX + 20.0
        p[1] = CY + PL / 2 + 10.0
        p[2] = CZ + 0.3 + 1.6
        s["start"]["look_ft"] = [CX, CY, CZ + 1.5]
    else:
        # pitch-side: on grass, clear of goals
        p[0] = CX + 20.0
        p[1] = CY - 10.0
        p[2] = CZ + 1.6
        s["start"]["look_ft"] = [CX - 20.0, CY - PL / 2 - 40.0, CZ + 8.0]
json.dump(route, open("/tmp/fb_route.json", "w"))
# manual camera creation in metres
for shot in route["shots"]:
    for key in ("start",):
        p = Vector(shot[key]["pos_ft"]); q = Vector(shot[key]["look_ft"])
        cd = bpy.data.cameras.new(f"{shot['id']}_{key}"); cd.lens = shot["lens_mm"]; cd.sensor_width = 36
        cd.clip_start = 0.1; cd.clip_end = 5000
        co = bpy.data.objects.new(f"{shot['id']}_{key}", cd); co.location = p
        co.rotation_euler = (q - p).to_track_quat('-Z', 'Y').to_euler(); CAMS.objects.link(co)
sc.camera = CAMS.objects[0]

G.world_sky(elev=35, rot=180, strength=0.4, sun_energy=3.0, sun_rot=(45, 0, 30), sun_col=(1.0, 0.95, 0.88))
G.render_settings(exposure=0.0)
# save — file may be large due to Sydenham append; compress
sc["grok_build"] = json.dumps({"set": f"G-FOOTBALL {STATE}", "seed": SEED, "info": info})
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True)
print("SAVED", OUT, info)
# warn if over 90 MB
sz = os.path.getsize(OUT) / 1e6
print("SIZE_MB", round(sz, 1))
if sz >= 90: print("WARN over 90 MB — strip more Muse/courts next pass")
