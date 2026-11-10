"""CP010_foundations "setting out + gravel" CANDIDATE 2026-11-10 (DEPARTURES CN53; Grok Bot executor, no verdict, NOT live).
Loads the LIVE CP010 source rounds/c06.blend (never written) and saves rounds/candidates/c06_cp010found.blend, for
CP010_foundations_start / _end ONLY. Every new object is CP010F_* with only_cams=CP010_foundations; replaced originals get
hide_cams=CP010_foundations; ground materials swap per camera via cam_mat (render_views.py), so other shots in the blend
render as before (people pre-swap excepted, see below).

Why: in live c06 the walk alongside the foundation positions is a flat pale-beige plane with smooth dome heaps and crude
block stand-in workmen; the storyboard beat "a foundation pad and column base exposed beside prepared ground" and Downes'
"setting out" procedure do not read at all.

Changes (sources: Downes 1852 pp. 16-17 "Columns", pp. 54-55 "Setting out the building and fixing the columns"):
 1. Ground (cam_mat CP010F_ground on KGROUND_FOUNDATIONS / SITE_* / WEST_*): trodden summer-1850 park ground, worn turf
    patches on loam at the surface; pit walls show ~1 ft of dark loam over the yellow-brown gravel "stratum of gravel which
    extends over the whole area" (Downes p.16). Loam depth inferred (grade C).
 2. Spoil heaps: camera-scoped copies of every KSPOIL heap within 400 ft, subdivided + displaced (rim held at the ground),
    in CP010F_spoil (gravel with dark loam clods), originals hidden for this shot; the merged far field KFSPOIL takes the
    same material by cam_mat. Volumes unchanged (CN27).
 3. Setting-out stakes (Downes p.54-55): at every dug / poured position of zone A, two stakes 6 ft from the column centre,
    one in line with the row, one at right angles, each with a pin; the centre stake is gone (the pit is sunk).
 4. Hero position (804,-180): the moment of bedding. The lower column with its 2 ft x 1 ft 6 in base plate (existing
    base_piece_2.0x1.5_t1 mesh, D16) stands on the poured pad, and the second triangle (three pieces of wood, right angle
    cut to the column section) lies on the two stakes, its corner at the column. One position ahead of its row (CN53).
 5. People: every crude KWORKER stand-in inside either CP010 frame rebuilt as survey people_lib 1850s_workman
    in dark fustian with explicit poses (as CN44/CN45); render with --no-people.
blender -b rounds/c06.blend -P scripts/cand_cp010_found_20261110.py -- [--out rounds/candidates/c06_cp010found.blend]"""
import bpy, bmesh, math, os, sys, hashlib
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
F = 0.3048
def ft(v): return v * F
def inch(v): return v * F / 12.0
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
OUT = arg("--out", "rounds/candidates/c06_cp010found.blend"); OUT = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
sc = bpy.context.scene; SID = "CP010_foundations"; TAG = "cand_cp010found_20261110"
CAMS = [bpy.data.objects["CP010_foundations_start"], bpy.data.objects["CP010_foundations_end"]]
coll = bpy.data.collections.get("CP010F") or bpy.data.collections.new("CP010F")
if coll.name not in sc.collection.children: sc.collection.children.link(coll)
def scoped(ob):
    ob["only_cams"] = SID; ob[TAG] = True
    if ob.name not in coll.objects: coll.objects.link(ob)
    return ob

# ---------------- materials ----------------
def nodes(name):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); return m, nt.nodes, nt.links
def ramp(n, l, fac, stops):
    r = n.new("ShaderNodeValToRGB"); el = r.color_ramp.elements
    while len(el) < len(stops): el.new(0.5)
    for e, (p, c) in zip(el, stops): e.position = p; e.color = (*c, 1)
    l.new(fac, r.inputs["Fac"]); return r
def noise(n, l, vec, scale, detail=4.0, rough=0.6):
    t = n.new("ShaderNodeTexNoise"); t.inputs["Scale"].default_value = scale; t.inputs["Detail"].default_value = detail
    t.inputs["Roughness"].default_value = rough; l.new(vec, t.inputs["Vector"]); return t
def mix(n, l, fac, a, b):
    m = n.new("ShaderNodeMix"); m.data_type = 'RGBA'; l.new(fac, m.inputs["Factor"])
    l.new(a, m.inputs[6]); l.new(b, m.inputs[7]); return m.outputs[2]

LOAM = (0.075, 0.056, 0.038); LOAM_DRY = (0.110, 0.076, 0.046); TURF = (0.060, 0.068, 0.026); TURF_DRY = (0.115, 0.105, 0.048)
GRAVEL = (0.30, 0.19, 0.09); GRAVEL_LT = (0.42, 0.31, 0.17); GRAVEL_DK = (0.16, 0.10, 0.05)

def ground_mat():
    m, n, l = nodes("CP010F_ground")
    out = n.new("ShaderNodeOutputMaterial"); bs = n.new("ShaderNodeBsdfPrincipled"); bs.inputs["Roughness"].default_value = 0.97
    geo = n.new("ShaderNodeNewGeometry"); sep = n.new("ShaderNodeSeparateXYZ"); l.new(geo.outputs["Position"], sep.inputs[0])
    pos = geo.outputs["Position"]
    # surface: trodden loam with worn dry turf patches + fine grain
    patch = noise(n, l, pos, 0.18, 6.0, 0.62)
    turfm = ramp(n, l, patch.outputs["Fac"], [(0.54, (0, 0, 0)), (0.64, (1, 1, 1))])
    fine = noise(n, l, pos, 9.0, 8.0, 0.7)
    turfc = mix(n, l, ramp(n, l, fine.outputs["Fac"], [(0.35, (0, 0, 0)), (0.65, (1, 1, 1))]).outputs["Color"], n.new("ShaderNodeRGB").outputs[0], n.new("ShaderNodeRGB").outputs[0])
    rgbs = [nd for nd in n if nd.bl_idname == "ShaderNodeRGB"]; rgbs[0].outputs[0].default_value = (*TURF, 1); rgbs[1].outputs[0].default_value = (*TURF_DRY, 1)
    loamc = ramp(n, l, fine.outputs["Fac"], [(0.30, LOAM_DRY), (0.70, (0.15, 0.115, 0.078))])
    tread = noise(n, l, pos, 0.6, 4.0, 0.55)
    tr = ramp(n, l, tread.outputs["Fac"], [(0.38, (0.68, 0.68, 0.68)), (0.62, (1.12, 1.12, 1.12))])
    vm = n.new("ShaderNodeMix"); vm.data_type = 'RGBA'; vm.blend_type = 'MULTIPLY'; vm.inputs["Factor"].default_value = 1.0
    l.new(loamc.outputs["Color"], vm.inputs[6]); l.new(tr.outputs["Color"], vm.inputs[7])
    surf = mix(n, l, turfm.outputs["Color"], vm.outputs[2], turfc)
    # pit walls: loam band over gravel (z in metres; ground at -0.006, pits to ~-0.75)
    vor = n.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 38.0; l.new(pos, vor.inputs["Vector"])
    peb = ramp(n, l, vor.outputs["Distance"], [(0.0, GRAVEL_LT), (0.35, GRAVEL), (0.75, GRAVEL_DK)])
    gnz = noise(n, l, pos, 4.0, 5.0, 0.6)
    gcol = mix(n, l, ramp(n, l, gnz.outputs["Fac"], [(0.4, (0, 0, 0)), (0.6, (0.5, 0.5, 0.5))]).outputs["Color"], peb.outputs["Color"], ramp(n, l, gnz.outputs["Fac"], [(0.0, GRAVEL), (1.0, GRAVEL_DK)]).outputs["Color"])
    loamwall = ramp(n, l, fine.outputs["Fac"], [(0.3, (0.06, 0.045, 0.03)), (0.7, (0.10, 0.075, 0.05))])
    # band masks
    zband = n.new("ShaderNodeMapRange"); zband.inputs["From Min"].default_value = -0.33; zband.inputs["From Max"].default_value = -0.27
    l.new(sep.outputs["Z"], zband.inputs["Value"])          # 0 = gravel (below ~1 ft), 1 = loam band
    zsurf = n.new("ShaderNodeMapRange"); zsurf.inputs["From Min"].default_value = -0.03; zsurf.inputs["From Max"].default_value = -0.012
    l.new(sep.outputs["Z"], zsurf.inputs["Value"])          # 1 = top surface
    wall = mix(n, l, zband.outputs["Result"], gcol, loamwall.outputs["Color"])
    col = mix(n, l, zsurf.outputs["Result"], wall, surf)
    l.new(col, bs.inputs["Base Color"])
    bump = n.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.35; bump.inputs["Distance"].default_value = 0.02
    bmix = n.new("ShaderNodeMath"); bmix.operation = 'ADD'; l.new(fine.outputs["Fac"], bmix.inputs[0]); l.new(vor.outputs["Distance"], bmix.inputs[1])
    l.new(bmix.outputs[0], bump.inputs["Height"]); l.new(bump.outputs["Normal"], bs.inputs["Normal"])
    l.new(bs.outputs[0], out.inputs[0]); m.diffuse_color = (*LOAM_DRY, 1); return m

def spoil_mat():
    m, n, l = nodes("CP010F_spoil")
    out = n.new("ShaderNodeOutputMaterial"); bs = n.new("ShaderNodeBsdfPrincipled"); bs.inputs["Roughness"].default_value = 0.96
    geo = n.new("ShaderNodeNewGeometry"); pos = geo.outputs["Position"]
    clod = noise(n, l, pos, 2.2, 6.0, 0.65)
    clm = ramp(n, l, clod.outputs["Fac"], [(0.42, (0, 0, 0)), (0.50, (1, 1, 1))])
    vor = n.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 55.0; vor.inputs["Randomness"].default_value = 1.0; l.new(pos, vor.inputs["Vector"])
    peb = ramp(n, l, vor.outputs["Distance"], [(0.0, (0.30, 0.20, 0.10)), (0.4, (0.20, 0.13, 0.065)), (0.8, (0.12, 0.08, 0.045))])
    lo = ramp(n, l, clod.outputs["Fac"], [(0.4, (0.07, 0.052, 0.036)), (0.8, (0.12, 0.09, 0.06))])
    col = mix(n, l, clm.outputs["Color"], peb.outputs["Color"], lo.outputs["Color"])
    l.new(col, bs.inputs["Base Color"])
    bump = n.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.6; bump.inputs["Distance"].default_value = 0.04
    h = n.new("ShaderNodeMath"); h.operation = 'ADD'; l.new(clod.outputs["Fac"], h.inputs[0]); l.new(vor.outputs["Distance"], h.inputs[1])
    l.new(h.outputs[0], bump.inputs["Height"]); l.new(bump.outputs["Normal"], bs.inputs["Normal"])
    l.new(bs.outputs[0], out.inputs[0]); m.diffuse_color = (0.25, 0.17, 0.09, 1); return m

def plain(name, c, r=0.9):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF"); b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = r
    m.diffuse_color = (*c, 1); return m
GROUND, SPOIL = ground_mat(), spoil_mat()
for _m in (GROUND, SPOIL): _m.use_fake_user = True   # cam_mat targets have no static users
STAKE = plain("CP010F_stake_deal", (0.36, 0.28, 0.18), 0.85)
PIN = plain("CP010F_pin_iron", (0.05, 0.045, 0.04), 0.5)
TRI = plain("CP010F_triangle_pine", (0.46, 0.36, 0.22), 0.8)
WETCON = plain("CP010F_concrete_fresh", (0.25, 0.24, 0.22), 0.6)

# ---------------- 1. ground by cam_mat ----------------
ng = 0
for o in bpy.data.objects:
    if o.type == 'MESH' and o.name.startswith(("KGROUND_FOUNDATIONS", "KGROUND_SITE_", "KGROUND_WEST_")) and o.data.materials and o.data.materials[0]:
        base = o.data.materials[0].name
        o["base_mat"] = o.get("base_mat", base)
        prev = o.get("cam_mat"); o["cam_mat"] = (prev + "," if prev else "") + f"{SID}=CP010F_ground"; ng += 1
kf = bpy.data.objects.get("KFSPOIL")
if kf:
    kf["base_mat"] = kf.data.materials[0].name; kf["cam_mat"] = f"{SID}=CP010F_spoil"
print("CANDGROUND cam_mat on", ng, "ground objects + KFSPOIL", flush=True)

# ---------------- 2. rough heaps ----------------
tex = bpy.data.textures.get("CP010F_heap_tex") or bpy.data.textures.new("CP010F_heap_tex", 'CLOUDS')
tex.noise_scale = 0.45; tex.noise_depth = 3; tex.noise_basis = 'ORIGINAL_PERLIN'
tex2 = bpy.data.textures.get("CP010F_heap_tex2") or bpy.data.textures.new("CP010F_heap_tex2", 'CLOUDS')
tex2.noise_scale = 0.12; tex2.noise_depth = 2
c0 = (CAMS[0].matrix_world.translation + CAMS[1].matrix_world.translation) / 2
nh = 0
for o in list(bpy.data.objects):
    if not o.name.startswith("KSPOIL_") or o.type != 'MESH': continue
    if (o.matrix_world.translation - c0).length > ft(400): continue
    me = o.data.copy(); me.name = "CP010F_" + o.data.name
    cp = bpy.data.objects.new("CP010F_" + o.name[1:], me); cp.matrix_world = o.matrix_world.copy()
    for k in ("part_kind", "pit", "pit_depth_ft", "pit_vol_ft3", "bulked_ft3", "heap_ft3", "carted_ft3", "heap_h_ft"):
        if k in o: cp[k] = o[k]
    me.materials.clear(); me.materials.append(SPOIL)
    hmax = max(v.co.z for v in me.vertices) or 1.0
    vg = cp.vertex_groups.new(name="rise")
    for v in me.vertices: vg.add([v.index], min(1.0, max(0.0, v.co.z / (0.25 * hmax))), 'REPLACE')
    sub = cp.modifiers.new("sub", 'SUBSURF'); sub.subdivision_type = 'SIMPLE'; sub.levels = sub.render_levels = 3
    d1 = cp.modifiers.new("lumps", 'DISPLACE'); d1.texture = tex; d1.strength = 0.16; d1.mid_level = 0.5; d1.vertex_group = "rise"; d1.texture_coords = 'GLOBAL'
    d2 = cp.modifiers.new("clods", 'DISPLACE'); d2.texture = tex2; d2.strength = 0.05; d2.mid_level = 0.5; d2.vertex_group = "rise"; d2.texture_coords = 'GLOBAL'
    sub2 = cp.modifiers.new("smooth", 'SUBSURF'); sub2.levels = sub2.render_levels = 1
    for p in me.polygons: p.use_smooth = True
    scoped(cp)
    hc = o.get("hide_cams"); o["hide_cams"] = (hc + "," if hc else "") + SID; nh += 1
print("CANDHEAPS", nh, "rough copies", flush=True)

# ---------------- 3. setting-out stakes (Downes pp.54-55) ----------------
FOUND = {852: "dug", 828: "dug", 804: "poured", 780: "poured"}
ROWS = [y for y in (-204.0 + 24 * j for j in range(18)) if abs(y) >= 36]
HERO = (804.0, -180.0)
bm = bmesh.new(); bmp = bmesh.new()
def box(b, x0, x1, y0, y1, z0, z1):
    r = bmesh.ops.create_cube(b, size=1.0)
    for v in r["verts"]:
        v.co.x = x0 if v.co.x < 0 else x1; v.co.y = y0 if v.co.y < 0 else y1; v.co.z = z0 if v.co.z < 0 else z1
ns = 0
for x in FOUND:
    for y in ROWS:
        for (dx, dy) in ((-6.0, 0.0), (0.0, 6.0 if y < 0 else -6.0)):   # in line with the row (west) + at right angles (to the camera walk side)
            sx, sy = x + dx, y + dy; h = 0.55 + 0.1 * ((int(sx * 7 + sy * 3)) % 3) / 2
            s = inch(1.25)
            box(bm, ft(sx) - s, ft(sx) + s, ft(sy) - s, ft(sy) + s, ft(-0.02), ft(h))
            box(bmp, ft(sx) - inch(0.2), ft(sx) + inch(0.2), ft(sy) - inch(0.2), ft(sy) + inch(0.2), ft(h), ft(h) + inch(0.6))
            ns += 1
me = bpy.data.meshes.new("CP010F_stakes"); bm.to_mesh(me); bm.free(); me.materials.append(STAKE)
scoped(bpy.data.objects.new("CP010F_STAKES", me))
me = bpy.data.meshes.new("CP010F_pins"); bmp.to_mesh(me); bmp.free(); me.materials.append(PIN)
scoped(bpy.data.objects.new("CP010F_PINS", me))
print("CANDSTAKES", ns, "stakes at", len(FOUND) * len(ROWS), "positions (6 ft offsets)", flush=True)

# ---------------- 4. hero bedding at (804,-180) ----------------
hx, hy = HERO
bp = bpy.data.meshes.get("base_piece_2.0x1.5_t1")
pad = bpy.data.objects.get(f"KPAD_{hx:+.0f}_{hy:+.0f}")
padtop = -(1.2) if pad is None else -pad.get("pad_top", 1.2)
b = scoped(bpy.data.objects.new("CP010F_BASE_+804_-180", bp)); b.location = (ft(hx), ft(hy), ft(padtop))
b["part_kind"] = "base_piece"; b["plate_L"] = 2.0; b["plate_W"] = 1.5; b["state"] = "bedding (CN53)"
# fresh concrete skim on the pad top (bedding), 1/2 in
if pad:
    bmc = bmesh.new(); L, W = pad["pad_L"], pad["pad_W"]
    box(bmc, ft(hx - L / 2), ft(hx + L / 2), ft(hy - W / 2), ft(hy + W / 2), ft(padtop) - inch(0.1), ft(padtop) + inch(0.5))
    me = bpy.data.meshes.new("CP010F_bedding"); bmc.to_mesh(me); bmc.free(); me.materials.append(WETCON)
    scoped(bpy.data.objects.new("CP010F_BEDDING", me))
# second triangle: three pieces of wood, right angle at the column, legs to the stakes at (x-6,y) and (x,y+6)
TZ = 0.55 + inch(0.0) / F
bmt = bmesh.new()
def bar(b_, a, c, w, t):
    a, c = Vector(a), Vector(c); d = c - a; Lb = d.length; ang = math.atan2(d.y, d.x)
    r = bmesh.ops.create_cube(b_, size=1.0); vs = r["verts"]
    for v in vs: v.co.x = (v.co.x + 0.5) * Lb; v.co.y *= w; v.co.z = (v.co.z + 0.5) * t
    bmesh.ops.rotate(b_, verts=vs, cent=(0, 0, 0), matrix=__import__("mathutils").Matrix.Rotation(ang, 3, 'Z'))
    bmesh.ops.translate(b_, verts=vs, vec=a)
zt = ft(0.62)
corner = (ft(hx - 0.45), ft(hy + 0.45), zt)          # inner corner cut to the column (8 in dia + clearance)
legA = (ft(hx - 6.3), ft(hy + 0.45), zt); legB = (ft(hx - 0.45), ft(hy + 6.3), zt)
bar(bmt, corner, legA, inch(3), inch(1.25)); bar(bmt, corner, legB, inch(3), inch(1.25)); bar(bmt, legA, legB, inch(3), inch(1.25))
me = bpy.data.meshes.new("CP010F_triangle"); bmt.to_mesh(me); bmt.free(); me.materials.append(TRI)
t = scoped(bpy.data.objects.new("CP010F_TRIANGLE_+804_-180", me)); t["source"] = "Downes 1852 pp.54-55 second triangle"
print("CANDHERO base piece on pad top", padtop, "ft; triangle legs 6 ft", flush=True)

# ---------------- 5. people ----------------
sys.path.insert(0, "/workspace/crystal-palace-survey/people"); import people_lib as PL
FUSTIAN = {"blue": (0.030, 0.042, 0.075), "grey": (0.050, 0.050, 0.048), "drab": (0.040, 0.044, 0.034)}
FM = {}
for k, c in FUSTIAN.items():
    m = bpy.data.materials.get(f"CP010F_fustian_{k}") or bpy.data.materials.new(f"CP010F_fustian_{k}")
    m.use_nodes = True; bb = m.node_tree.nodes.get("Principled BSDF")
    bb.inputs["Base Color"].default_value = (*c, 1.0); bb.inputs["Roughness"].default_value = 0.95
    if "Specular IOR Level" in bb.inputs: bb.inputs["Specular IOR Level"].default_value = 0.2
    m.diffuse_color = (*c, 1.0); FM[k] = m
POSEMAP = {"work": "working", "reach": "working", "kneel": "working", "stand": "standing"}
# the bedding gang at the hero position: ganger at the triangle, labourer opposite (feet; face 0 = front toward -Y)
MOVE = {"KWORKER_003_CP010": (hx - 3.0, hy + 5.4, 0.0, 200.0, "standing"),
        "KWORKER_034_CP010": (832.0, -189.0, 0.0, 300.0, "standing"),
        # live c06 bug: the pit digger stood at y -186, 2 ft outside the pit (y -184..-176), buried to the waist in solid ground,
        # so he read as a man sitting on the ground. Moved onto the pit floor (tier-1 pad top 1.2 + 1.25 = 2.45 ft down).
        "KWORKER_000_CP010": (826.5, -181.0, -2.45, 330.0, "working")}
for nm, (x, y, z, r, p) in MOVE.items():
    o = bpy.data.objects.get(nm)
    if o: o.location = (ft(x), ft(y), ft(z)); o.rotation_euler.z = math.radians(r); o["pose"] = "stand"
def in_view(ob, cam, margin=0.06):
    p = ob.matrix_world.translation
    for dz in (0.2, 1.0, 1.7):
        v = world_to_camera_view(sc, cam, p + Vector((0, 0, dz)))
        if v.z > 0 and -margin <= v.x <= 1 + margin and -margin <= v.y <= 1 + margin: return True
    return False
n = 0
for o in sorted([o for o in bpy.data.objects if PL._is_figure(o) and not o.hide_render], key=lambda o: o.name):
    if not any(in_view(o, c) for c in CAMS): continue
    d = min((o.matrix_world.translation - c.matrix_world.translation).length for c in CAMS) / F
    pose = MOVE.get(o.name, (0, 0, 0, 0, None))[4] or POSEMAP.get(o.get("pose"), "standing")
    lod = "hero" if d < 60 else ("mid" if d < 250 else "crowd")
    seed = int(hashlib.md5(o.name.encode()).hexdigest()[:6], 16)
    tmp = PL._build_person("1850s_workman", pose, lod, seed)
    mw = o.matrix_world.copy(); o.data = tmp.data; bpy.data.objects.remove(tmp, do_unlink=True)
    o.matrix_world = mw; o.scale = (1, 1, 1); o["cpl_people"] = PL.PEOPLE_TAG
    k = ("grey", "drab")[n % 2] if lod == "hero" else list(FUSTIAN)[n % 3]   # the blue fustian read as a tight bodysuit at 20-30 ft
    for si, m in enumerate(o.data.materials):
        if m and (m.name.startswith("CPL3_smock") or m.name.startswith("CPL3_waist")): o.data.materials[si] = FM[k]
    o[TAG] = f"people_lib {PL.PEOPLE_VERSION} 1850s_workman {pose} {lod} fustian {k}"; n += 1
    print("PERSON", o.name, pose, lod, k, f"d={d:.0f}ft", flush=True)
print("PEOPLE_SWAPPED", n, flush=True)

sc[TAG] = "CN53 CANDIDATE (CP010_foundations only)"
bpy.ops.wm.save_as_mainfile(filepath=OUT, copy=True, compress=True); print("SAVED", OUT, flush=True)
