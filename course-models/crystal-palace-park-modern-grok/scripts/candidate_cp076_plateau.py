"""CP076 'Turn back toward the empty site' - present-day palace-terrace polish, CANDIDATE 2026-11-11 (Grok; no verdict).
blender -b rounds/parknow-r02.blend -P scripts/candidate_cp076_plateau.py -- [--out rounds/candidates/parknow-r02_cp076plateau.blend] [--p JSON]
Never overwrites the opened (live) blend. PARK-NOW (present day) only; nothing of Hyde Park and no Victorian state.

Fixes / adds (DEPARTURES D-PM-26..D-PM-31):
 1. Upper Palace Terrace grass: pk_grass_plateau (z 0, hidden since dud-fix v4 because it overhung the lower terrace
    down to y -127.5 m) is replaced by pk_grass_upper_palace_terrace, trimmed to the line of the basement/terrace wall
    (y >= -47.9 m) at the wall top (z 0.0). Source: Crystal Palace Park Regeneration Plan (May 2017) App. B 4-7:
    Upper Palace Terrace at palace ground level, Lower Palace Terrace at basement level, ~8 m apart; upper terrace
    'rough grass with rows of semi-mature trees'.
 2. Grounding: every pk_tree_* (upper park) and every PPL-NOW visitor within the upper park box is dropped onto the
    highest render-visible ground under its foot (they floated 3-34 m in CP076: trees on the hidden z 0 plateau over the
    z -7.2 terrace, heroes at z 13/26 m).
 3. Trees: the 28 icosphere 'lollipop' pk_tree_* meshes become parametric broadleaf trees (MV20 v2 generator, oak habit
    as stand-in for the park's mixed oak/plane/lime/sycamore stock); trees that stood on the lower terrace lawn
    (y -127.5..-47.9) move up onto the spoil embankment / upper terrace edge behind the wall (y -46..-30), where the
    regeneration plan records 'self-seeded scrub and trees'. Historic England 1000373: the terraces are laid to grass.
 4. Scrub: a broken band of self-seeded scrub (thorn habit, 2.5-5 m) along the embankment top behind the wall.
 5. Transmitter: the 1956 BBC (now Arqiva) Crystal Palace lattice tower, parametric: 37 m (120 ft) square base,
    12 diminishing panels to a 4.4 m (14.5 ft) square platform at 131 m (429 ft); main structure 196 m, UHF aerial
    cylinder to 219 m (Wikipedia 'Crystal Palace transmitting station'; thebigtower.com). Position registered from
    OS grid refs (subway TQ 33791 70972 = model (0, 60); mast TQ 33947 71220) with the palace axis assumed at
    bearing 22.5 deg -> model (289, 11), nudged to (308, 5) to clear the modelled north water-tower base.
Cameras, exposure, world, look, sphinxes, terraces, people meshes and every other object: unchanged.
"""
import os, sys, json, math, random, argparse, zlib
import bpy, bmesh
from mathutils import Vector, Matrix
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import park_trees_now as PT

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser(); ap.add_argument("--out", default="rounds/candidates/parknow-r02_cp076plateau.blend")
ap.add_argument("--p", default="{}"); a = ap.parse_args(argv)
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = a.out if os.path.isabs(a.out) else os.path.join(here, a.out)
assert os.path.abspath(out) != os.path.abspath(bpy.data.filepath), "refusing to overwrite the opened (live) blend"

FT = 0.3048
P = dict(seed=20261111, wall_y=-47.9, wall_top=0.0, plateau_x=285.1, plateau_y1=87.5,
         upper_box=(-340.0, 340.0, -215.0, 215.0), tree_H=(11.0, 17.0), emb_y=(-46.0, -30.0),
         scrub_n=70, scrub_H=(2.5, 5.0), scrub_y=(-47.0, -41.0), scrub_x=(-240.0, 240.0),
         leaf_gain=1.7, mast_xy=(308.0, 5.0), mast_rgb=(0.20, 0.21, 0.22))
P.update({k: (tuple(v) if isinstance(v, list) else v) for k, v in json.loads(a.p).items()})
PT.LEAF_GAIN = P["leaf_gain"]
R = random.Random(P["seed"])
COLL = bpy.data.collections.get("PARKNOW_grass_trees")
NEW = bpy.data.collections.new("PARKNOW_cp076_plateau_now"); bpy.data.collections["PARK-NOW_present_day"].children.link(NEW)
log = {"version": PT.VERSION, "params": {k: v for k, v in P.items()}, "moved": [], "grounded": [], "scrub": 0}

# ---- 1. trimmed upper palace terrace grass
old = bpy.data.objects["pk_grass_plateau"]; assert old.hide_render, "expected dud-fix v4 hidden plateau"
gm = old.data.materials[0]
bm = bmesh.new(); x = P["plateau_x"]; y0, y1 = P["wall_y"], P["plateau_y1"]; z1 = P["wall_top"] + 0.02; z0 = z1 - 0.07
bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=(2 * x, y1 - y0, z1 - z0), verts=bm.verts)
bmesh.ops.translate(bm, vec=(0, (y0 + y1) / 2, (z0 + z1) / 2), verts=bm.verts)
me = bpy.data.meshes.new("pk_grass_upper_palace_terrace"); bm.to_mesh(me); bm.free(); me.materials.append(gm)
gp = bpy.data.objects.new("pk_grass_upper_palace_terrace", me); NEW.objects.link(gp); gp["cp076_now"] = PT.VERSION

# ---- ground ray helper (render-visible ground only)
SKIP = ("pk_tree", "ppl_now", "ov_", "CAM", "terrace_sphinx", "PLACEHOLDER", "pk_scrub", "pk_mast", "water_tower", "colonnade_roof", "pk_dino")
dg = bpy.context.evaluated_depsgraph_get(); sc = bpy.context.scene
def ground_z(xx, yy, ztop=120.0):
    org = Vector((xx, yy, ztop))
    for _ in range(40):
        ok, loc, n, i, ob, m = sc.ray_cast(dg, org, Vector((0, 0, -1)))
        if not ok: return None, None
        if ob.hide_render or ob.name.startswith(SKIP) or any(c.hide_render for c in ob.users_collection):
            org = loc - Vector((0, 0, 0.02)); continue
        return loc.z, ob.name
    return None, None
def in_upper(xx, yy):
    b = P["upper_box"]; return b[0] <= xx <= b[1] and b[2] <= yy <= b[3]

# ---- 3. trees: replace lollipops, relocate the lower-terrace ones, ground all
trees = sorted([o for o in bpy.data.objects if o.name.startswith("pk_tree_") and not o.name.startswith("pk_tree_nsc")], key=lambda o: o.name)
dg.update()
for o in trees:
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
    # trunk foot = centre of the lowest vertices
    vs = [o.matrix_world @ v.co for v in o.data.vertices]; zmin = min(v.z for v in vs)
    foot = [v for v in vs if v.z < zmin + 0.3]; fx = sum(v.x for v in foot) / len(foot); fy = sum(v.y for v in foot) / len(foot)
    h_old = max(b.z for b in bb) - zmin
    nx, ny = fx, fy
    if P["wall_y"] - 80.0 < fy < P["wall_y"]:            # stood on the lower-terrace lawn: move to the embankment
        ny = R.uniform(*P["emb_y"]); log["moved"].append((o.name, round(fx, 1), round(fy, 1), round(nx, 1), round(ny, 1)))
    H = max(P["tree_H"][0], min(P["tree_H"][1], h_old * 1.15))
    tme, info = PT.build_tree(o.name + "_now", "oak", H, P["seed"] + zlib.crc32(o.name.encode()) % 9973)
    oldme = o.data; o.data = tme; o.location = (0, 0, 0); o.rotation_euler = (0, 0, R.uniform(0, 2 * math.pi)); o.scale = (1, 1, 1)
    o.hide_render = True                                    # exclude from its own ground ray
    dg.update()
    gz, gname = ground_z(nx, ny)
    if gname and ("water" in gname or gname == "pk_parade_road"):   # never in a basin or on the carriageway
        ny = -132.0 if "water" in gname else 82.5
        log["moved"].append((o.name, round(fx, 1), round(fy, 1), round(nx, 1), round(ny, 1), "off " + gname))
        gz, gname = ground_z(nx, ny)
    o.hide_render = False
    o.location = (nx, ny, gz if gz is not None else 0.0)
    o["cp076_now"] = PT.VERSION; o["H_m"] = round(H, 2); o["ground"] = gname or "none"
    log["grounded"].append((o.name, round(nx, 1), round(ny, 1), round(zmin, 2), round(gz, 2) if gz is not None else None, gname, round(H, 1)))
    if oldme.users == 0: bpy.data.meshes.remove(oldme)

# ---- 4. scrub band along the embankment top
nsc = 0
for i in range(P["scrub_n"]):
    xx = R.uniform(*P["scrub_x"]); yy = R.uniform(*P["scrub_y"])
    if R.random() < 0.25: continue                         # broken band, gaps
    gz, gname = ground_z(xx, yy)
    if gz is None or gz < P["wall_top"] - 1.0: continue     # only on the upper terrace / wall top
    H = R.uniform(*P["scrub_H"]); sme, info = PT.build_tree(f"pk_scrub_{i:02d}", "thorn", H, P["seed"] * 7 + i)
    s = bpy.data.objects.new(f"pk_scrub_{i:02d}", sme); NEW.objects.link(s); s.location = (xx, yy, gz)
    s.rotation_euler[2] = R.uniform(0, 2 * math.pi); s["cp076_now"] = PT.VERSION; nsc += 1
log["scrub"] = nsc

# ---- 2. ground PPL-NOW visitors in the upper park
for o in sorted([o for o in bpy.data.objects if o.name.startswith("ppl_now") and o.type == "MESH"], key=lambda o: o.name):
    vs = [o.matrix_world @ v.co for v in o.data.vertices]; zmin = min(v.z for v in vs)
    cx = sum(v.x for v in vs) / len(vs); cy = sum(v.y for v in vs) / len(vs)
    if not in_upper(cx, cy): continue
    o.hide_render = True; dg.update(); gz, gname = ground_z(cx, cy); o.hide_render = False
    if gz is None: continue
    dz = gz - zmin
    if abs(dz) > 0.02:
        o.location.z += dz; log["grounded"].append((o.name, round(cx, 1), round(cy, 1), round(zmin, 2), round(gz, 2), gname, "person"))

# ---- 5. Crystal Palace transmitter (1956), parametric lattice
def tube(bm, a, b, r, seg=6):
    d = b - a
    if d.length < 1e-6: return
    d.normalize(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0))
    s = d.cross(up).normalized(); u = s.cross(d).normalized()
    A = [bm.verts.new(a + (s * math.cos(2 * math.pi * k / seg) + u * math.sin(2 * math.pi * k / seg)) * r) for k in range(seg)]
    B = [bm.verts.new(b + (s * math.cos(2 * math.pi * k / seg) + u * math.sin(2 * math.pi * k / seg)) * r) for k in range(seg)]
    for k in range(seg): bm.faces.new([A[k], A[(k + 1) % seg], B[(k + 1) % seg], B[k]])
B0, B1, ZP, ZM, ZA = 120 * FT / 2, 14.5 * FT / 2, 429 * FT, 196.0, 219.0     # half-widths, platform, main top, aerial top
def hw(z):
    if z <= ZP: return B1 + (B0 - B1) * (1 - z / ZP) ** 1.6
    return B1 - (B1 - 1.3) * (z - ZP) / (ZM - ZP)
# 12 diminishing panels to the platform (panel height ~ local width)
r = 0.86; h0 = ZP * (1 - r) / (1 - r ** 12); zs = [0.0]
for k in range(12): zs.append(zs[-1] + h0 * r ** k)
zs[-1] = ZP
zu = [ZP + (ZM - ZP) * k / 10 for k in range(1, 11)]; zall = zs + zu
bm = bmesh.new()
corners = lambda z: [Vector((sx * hw(z), sy * hw(z), z)) for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
for z_a, z_b in zip(zall, zall[1:]):
    ca, cb = corners(z_a), corners(z_b); rl = 0.75 * (1 - z_a / ZM) + 0.2
    for k in range(4):
        tube(bm, ca[k], cb[k], rl, 8)                                           # legs
        n2 = (k + 1) % 4
        tube(bm, cb[k], cb[n2], rl * 0.45, 5)                                   # girt
        if z_a < ZP:                                                            # K/X bracing per face
            tube(bm, ca[k], cb[n2], rl * 0.35, 5); tube(bm, ca[n2], cb[k], rl * 0.35, 5)
            mid_a = (ca[k] + ca[n2]) / 2; mid_b = (cb[k] + cb[n2]) / 2
            tube(bm, mid_a, (cb[k] + cb[n2]) / 2, rl * 0.2, 4) if hw(z_a) > 8 else None
        else:
            tube(bm, ca[k], cb[n2], rl * 0.3, 4)
# platform at 131 m
bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((0, 0, ZP + 0.4)) @ Matrix.Diagonal((B1 * 2 + 1.2, B1 * 2 + 1.2, 0.8, 1)))
# UHF aerial cylinder to 219 m
bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=1.0, radius2=0.8, depth=ZA - ZM, matrix=Matrix.Translation((0, 0, (ZM + ZA) / 2)))
me = bpy.data.meshes.new("pk_mast_crystal_palace_1956"); bm.to_mesh(me); bm.free()
mm = bpy.data.materials.new("Mast_GalvSteel_Now"); mm.use_nodes = True; pb = PT._p(mm)
pb.inputs["Base Color"].default_value = (*P["mast_rgb"], 1); pb.inputs["Roughness"].default_value = 0.55; pb.inputs["Metallic"].default_value = 0.3
me.materials.append(mm)
mast = bpy.data.objects.new("pk_mast_crystal_palace_1956", me); NEW.objects.link(mast)
gz, gname = ground_z(*P["mast_xy"]); mast.location = (P["mast_xy"][0], P["mast_xy"][1], gz if gz is not None else 0.0)
mast.rotation_euler[2] = math.radians(0.0); mast["cp076_now"] = PT.VERSION
mast["source"] = "Wikipedia 'Crystal Palace transmitting station' (120 ft base, 12 panels to 14.5 ft platform at 429 ft); thebigtower.com (196 m main, 219 m with UHF aerial)"
log["mast"] = dict(xy=P["mast_xy"], ground=gz, ground_obj=gname, faces=len(me.polygons))

bpy.context.scene["cp076_plateau_candidate"] = PT.VERSION
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True)
lp = os.path.join(here, "checks", "cp076_plateau_candidate.json"); json.dump(log, open(lp, "w"), indent=1, default=str)
print("CP076_CANDIDATE_SAVED", out, "trees", len(trees), "moved", len(log["moved"]), "scrub", nsc, "grounded", len(log["grounded"]), "mast", log["mast"], flush=True)
