"""2026-11-02 CANDIDATE (Grok Bot executor, no verdict): CP012_bay sheer legs re-pitched (DEPARTURES CN46).
Base: live rounds/candidates/c07_cp012bay.blend (CP012_bay KEEP, CN45; unchanged). Saves a sibling
rounds/candidates/c07_cp012bay_shears.blend (CP012_bay only, same rules as the live blend: never render other shots from it).
Why (open follow-up 1 of CN45): the two sheer legs stood bolt upright in the x=552 plane (feet (552,-196) and (552,-164),
apex (552,-180,36)), so from the square-on 28 mm walk the near (south) leg rose vertically through the middle of the start
frame like a pale post. Upright shears are also not how sheers were worked: they are raked over the load and held by a
back guy (shears are 'raked' and 'guyed'; a vertical pair has no stable lean).
Change:
  * KSHEERLEGS rebuilt: same apex (552,-180,36) over the girder's lift point, same 5 in spar radius, same material
    (GT_ScaffoldPole), feet moved --rake-dx ft along x (both), half-splay --splay ft along y. Candidate: --rake-dx 8 --splay 15:
    feet (560,-195) and (560,-165), rake 12.5 deg from vertical (heels east, head leaning west over the girder),
    spar length 39.8 ft (live 39.4 ft; CN07 says ~37 ft).
  * --move KWORKER_064_CP012=x:y:face: the CN45 watcher stood on the new north heel; moved clear.
  * KSNATCH_BLOCK follows the south foot (same 1 ft offset as live); the fall rope (apex -> block) and the horse haul
    (KHAUL_ROPE: block -> swingletree -> traces) rebuilt to the moved block; horse, boy and swingletree unchanged.
  * back guy added (KROPES_CP012_BACKGUY) from the apex to a ground anchor on the feet side, so the raked pair is held.
    The two live guys (SW, NE) stay.
  * prints CLEAR <object> <ft> (spar surface to nearest surface, both frames 1 and 96) and FRAME projections of the
    south leg; asserts the spar clears every object by >= --min-clear ft (default 1.0).
blender -b rounds/candidates/c07_cp012bay.blend -P scripts/cand_cp012_shears_20261102.py -- [--rake-dx -8] [--splay 15] [--out PATH]"""
import bpy, bmesh, math, os, sys
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
F = 0.3048; IN = 0.0254
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
sc = bpy.context.scene; TAG = "cand_cp012shears_20261102"
DX, S = float(arg("--rake-dx", "-8")), float(arg("--splay", "15"))
APEX = Vector((552.0, -180.0, 36.0))
FEET = [Vector((552.0 + DX, -180.0 - S, 0.0)), Vector((552.0 + DX, -180.0 + S, 0.0))]
R_SPAR = 5 * IN
def cyl(bm, a, b, r, seg):
    a = Vector(a) * F; b = Vector(b) * F; d = b - a
    M = Matrix.Translation((a + b) / 2) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=d.length, matrix=M)
def replace_mesh(ob, segs, r, seg):
    bm = bmesh.new()
    for a, b in segs: cyl(bm, a, b, r, seg)
    me = bpy.data.meshes.new(ob.data.name + "_shears"); bm.to_mesh(me); bm.free()
    for m in ob.data.materials: me.materials.append(m)
    ob.data = me; ob.matrix_world = Matrix.Identity(4)
# explicit figure moves NAME=x:y:face_deg (feet), e.g. the CN45 watcher off the north heel
for spec in [s_ for s_ in (arg("--move", "") or "").split(",") if s_]:
    nm, v = spec.split("="); x, y, rz = map(float, v.split(":"))
    o = bpy.data.objects[nm]; o.location.x, o.location.y = x * F, y * F; o.rotation_euler.z = math.radians(rz); o[TAG + "_move"] = v
# spars: extend 0.3 ft past the apex (lashing overlap, as live) and seat the heel at ground
SL = bpy.data.objects["KSHEERLEGS"]
segs = []
for ft_ in FEET:
    d = (APEX - ft_).normalized(); segs.append((tuple(ft_), tuple(APEX + d * 0.2)))
replace_mesh(SL, segs, R_SPAR, 10)
SL["apex_ft"] = list(APEX); SL["feet_ft"] = [list(f) for f in FEET]; SL[TAG] = f"raked dx {DX:+} ft, half-splay {S} ft (CN46)"
LEN = (APEX - FEET[0]).length; RAKE = math.degrees(math.atan2(abs(DX), APEX.z))
print(f"SPARS length {LEN:.2f} ft rake {RAKE:.1f} deg feet {[tuple(round(v,1) for v in f) for f in FEET]}")
# snatch block follows the south foot (live: block 0.6 ft east, 1 ft north of the foot)
SB = bpy.data.objects["KSNATCH_BLOCK"]; SNATCH = (FEET[0].x + 0.6, FEET[0].y + 1.0)
SB.location.x, SB.location.y = SNATCH[0] * F, SNATCH[1] * F; SB[TAG] = "follows south foot"
# fall + live guys (KROPES_CP012_STATIC) and new back guy
ST = bpy.data.objects["KROPES_CP012_STATIC"]; r = 0.6 * IN
replace_mesh(ST, [(tuple(APEX), (SNATCH[0], SNATCH[1], 1.0)), (tuple(APEX), (530, -236, 0)), (tuple(APEX), (576, -126, 0))], r, 6)
ST[TAG] = "fall re-led to moved block"
ANCH = (552.0 + 4.5 * DX, -188.0, 0.0)
bg = bpy.data.objects.get("KROPES_CP012_BACKGUY")
if bg: bpy.data.objects.remove(bg, do_unlink=True)
me = bpy.data.meshes.new("KROPES_CP012_BACKGUY"); bg = bpy.data.objects.new("KROPES_CP012_BACKGUY", me)
ST.users_collection[0].objects.link(bg); me.materials.append(bpy.data.materials["GT_Rope"])
bm = bmesh.new(); cyl(bm, tuple(APEX), ANCH, r, 6); bm.to_mesh(me); bm.free()
bg["part_kind"] = "rope"; bg["role"] = "back_guy"; bg[TAG] = f"anchor {ANCH}"
# horse haul rope: rebuilt from the moved block, horse/swingletree positions unchanged (same formula as build_construction.py)
HH = bpy.data.objects["KHORSE_haul"]; HX, HY = HH.location.x / F, HH.location.y / F
HD = math.radians(170.0); hdx, hdy = math.cos(HD), math.sin(HD); nx_, ny_ = -hdy, hdx
STX, STY = HX - 4.9 * hdx, HY - 4.9 * hdy
HR = bpy.data.objects["KHAUL_ROPE"]; bm = bmesh.new()
cyl(bm, (SNATCH[0], SNATCH[1], 1.0), (STX, STY, 2.4), r, 6)
cyl(bm, (STX - 1.3 * nx_, STY - 1.3 * ny_, 2.4), (STX + 1.3 * nx_, STY + 1.3 * ny_, 2.4), 1.5 * IN, 8)
for sgn in (-1, 1):
    cyl(bm, (STX + sgn * 1.2 * nx_, STY + sgn * 1.2 * ny_, 2.4), (HX + 1.6 * hdx + sgn * 0.75 * nx_, HY + 1.6 * hdy + sgn * 0.75 * ny_, 4.3), 0.7 * IN, 6)
me = bpy.data.meshes.new("haul_rope_shears"); bm.to_mesh(me); bm.free()
for m in HR.data.materials: me.materials.append(m)
HR.data = me; HR.matrix_world = Matrix.Identity(4); HR[TAG] = "re-led from moved block"
print(f"HORSE {math.hypot(HX - SNATCH[0], HY - SNATCH[1]):.1f} ft from block (K29 wants 15-45)")
# clearance: spar surface to every other visible mesh, frames 1 and 96
dg = bpy.context.evaluated_depsgraph_get()
def clear_report():
    pts = []
    for ft_ in FEET:
        for i in range(1, 60):
            t = i / 60.0; pts.append((ft_ + (APEX - ft_) * t) * F)
    worst = []
    for o in bpy.data.objects:
        if o.type != 'MESH' or o.hide_render or o.name in ("KSHEERLEGS",) or o.name.startswith("KROPES") or o.name in ("KHAUL_ROPE", "KSNATCH_BLOCK", "KGIN_ROPES"): continue
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        lo = Vector([min(v[i] for v in bb) for i in range(3)]); hi = Vector([max(v[i] for v in bb) for i in range(3)])
        if hi.x / F < 520 or lo.x / F > 585 or hi.y / F < -215 or lo.y / F > -145 or (hi - lo).length / F > 200: continue
        oe = o.evaluated_get(dg); bvh = BVHTree.FromObject(oe, dg)
        if bvh is None: continue
        inv = o.matrix_world.inverted(); best = 1e9
        for p in pts:
            hit = bvh.find_nearest(inv @ p)
            if hit[0] is not None: best = min(best, ((o.matrix_world @ hit[0]) - p).length)
        worst.append(((best - R_SPAR) / F, o.name))
    worst.sort(); return worst
MINC = float(arg("--min-clear", "1.0")); ok = True
for fr in (1, 96):
    sc.frame_set(fr); dg.update(); w = clear_report()
    for c, n in w[:6]: print(f"CLEAR f{fr} {n} {c:.2f} ft")
    if w and w[0][0] < MINC: ok = False
print("CLEARANCE_OK", ok)
sc.frame_set(1)
for fr, cn in ((1, "CP012_bay_start"), (96, "CP012_bay_end")):
    sc.frame_set(fr); cam = bpy.data.objects[cn]
    pr = lambda p: world_to_camera_view(sc, cam, p * F)
    s_foot, s_mid, s_hi = pr(FEET[0]), pr(FEET[0].lerp(APEX, 0.5)), pr(FEET[0].lerp(APEX, 0.85))
    print("FRAME", cn, "south foot (%.2f,%.2f) mid (%.2f,%.2f) 0.85 (%.2f,%.2f)" % (s_foot.x, s_foot.y, s_mid.x, s_mid.y, s_hi.x, s_hi.y))
sc.frame_set(1)
if not ok and "--force" not in argv: sys.exit("CLEARANCE FAIL")
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = arg("--out") or os.path.join(here, "rounds", "candidates", "c07_cp012bay_shears.blend")
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True); print("SAVED", out)
