"""CANDIDATE v2 polish CP028 (louvre drive + attendant oiling the shafting) on h03.

v2 (2026-11-02): FT51-FT53 byte-for-byte as v1 (polish_cp028_drive_cand.py); only FT54 restaged
because v1 was REJECTED (the oiler read as floating beside the steps).

rounds/h03.blend -> rounds/candidates/h03_cp028_drive_v2.blend.  Live h03 is never written.

Changes (see DEPARTURES FT51-FT54):
  FT51  Downes/Cowper 1852 LOUVRES: one endless cord on pulley Q + worm P / worm-wheel O drives
        "a length of 108 ft on each side" through 1 in shafting T; intermediate louvres are moved
        by cranks U and rods N' on that shafting, carried in bearings S'.  Live h03 showed three
        pulleys in 24 ft.  Candidate: centre compartment (x=24 ft, the rope the floor attendant
        holds) keeps Muse's pulley/worm station; the compartments at x=16 and x=32 become
        intermediate stations (pulley, rope, worm-wheel, centre rod N, forks, bearing S, cleat
        removed; a copy of Muse's crank U / rod N' / bearing S' station put at their centre).
  FT52  One continuous 1 in shafting T across x=12..36 ft (live: three 7.3 ft stubs with gaps).
  FT53  Stray closed-state blind laths/seams (Muse model_closed leftovers) removed if present.
  FT54  Staging (grade C), v2 (pale moleskin trousers + dark boots for legibility): the attendant faces up the 14 ft steps (climbing side -x), body between the
        stiles, one foot on tread 12 and one on tread 13, top cap in front of his thighs, reaching
        over the cap to bearing S' at x=16 ft.
"""
import bpy, bmesh, math, sys, os
from mathutils import Vector, Matrix

FT = 0.3048
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SRC = argv[argv.index("--src") + 1] if "--src" in argv else "rounds/h03.blend"
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/h03_cp028_drive_v2.blend"
src = SRC if os.path.isabs(SRC) else os.path.join(ROOT, SRC)
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
assert os.path.abspath(out) != os.path.abspath(os.path.join(ROOT, "rounds/h03.blend")), "never overwrite live h03"
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=src)
D = bpy.data
log = {}

LV = D.collections["MUSE_Louvre_by_Muse"]
# FT53: stray closed-state blind pieces (outside the 8 ft compartment, local x > 2.4 m)
stray = [o for o in LV.objects if o.name.startswith(("BlindLath_", "BlindSeam_"))]
for o in stray: LV.objects.unlink(o)
log["FT53_removed"] = [o.name for o in stray]

# FT51: intermediate-station variant of the Muse compartment
DROP = ("PulleyRim_Q", "PulleyHub_Q", "PulleySpoke_", "SpokeTip_", "Rope_R", "WheelTooth_", "WheelSocket_O",
        "Fork_", "Rod_N", "BearingS_", "Cleat_c", "WormP", "Worm_P", "Worm")
def dropped(n):
    if n.startswith(("Rod_N1", "RodN1_")): return False
    return n.startswith(DROP)
IM = D.collections.get("CP028_Louvre_Intermediate") or D.collections.new("CP028_Louvre_Intermediate")
IM.instance_offset = LV.instance_offset
nd = []
for o in list(LV.objects):
    if dropped(o.name): nd.append(o.name); continue
    c = o.copy(); IM.objects.link(c)
    if o.name.startswith(("Crank_U", "CrankPin_U", "Rod_N1", "RodN1_Pin", "BearingS1_")):
        c2 = o.copy(); c2.location.x -= 0.914; c2.name = "CTR_" + o.name; IM.objects.link(c2)
log["FT51_dropped_in_intermediate"] = nd
for k in (0, 2):
    e = D.objects[f"LOUVRE_MUSE_{k}"]; e.instance_collection = IM
log["FT51_intermediate_instances"] = ["LOUVRE_MUSE_0", "LOUVRE_MUSE_2"]

steel = D.materials.get("Steel"); deal = D.materials.get("DealTimber")
props = D.collections.get("PROPS_HP51") or bpy.context.scene.collection
figs = D.collections.get("FIGURES_HP51") or bpy.context.scene.collection

def mesh_obj(name, bm, mats, coll):
    me = D.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    for p in me.polygons: p.use_smooth = False
    o = D.objects.new(name, me); coll.objects.link(o); return o

def bar(bm, a, b, r, seg=8, mi=0):
    a, b = Vector(a), Vector(b); d = b - a; L = d.length
    res = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=L)
    q = d.normalized().to_track_quat('Z', 'Y')
    M = Matrix.Translation((a + b) / 2) @ q.to_matrix().to_4x4()
    bmesh.ops.transform(bm, matrix=M, verts=res["verts"])
    for f in {f for v in res["verts"] for f in v.link_faces}: f.material_index = mi

def box(bm, c, size, rz=0.0, mi=0):
    res = bmesh.ops.create_cube(bm, size=1.0)
    M = Matrix.Translation(c) @ Matrix.Rotation(rz, 4, 'Z') @ Matrix.Diagonal((*size, 1))
    bmesh.ops.transform(bm, matrix=M, verts=res["verts"])
    for f in {f for v in res["verts"] for f in v.link_faces}: f.material_index = mi

# FT52: continuous 1 in shafting T along the louvre run (local y -0.218, z 0.19 of the Muse prop)
ey = D.objects["LOUVRE_MUSE_1"].location.y; ez = D.objects["LOUVRE_MUSE_1"].location.z
sy, sz = ey - 0.218, ez + 0.1905
bm = bmesh.new(); bar(bm, (12.05 * FT, sy, sz), (35.95 * FT, sy, sz), 0.0127, 10)
mesh_obj("CP028_SHAFTING_T", bm, [steel], props)
log["FT52_shaft"] = {"x_ft": [12.05, 35.95], "y_m": round(sy, 3), "z_m": round(sz, 3), "dia_in": 1.0}

# FT54 v2: 14 ft pair of deal steps (top 4.30 m, 14 rises of 0.307 m) side-on to the wall, climbing side
# facing -x.  The attendant stands ON the steps facing up them (+x, turned 10 deg toward the wall so the
# camera sees his right side, not his back): lower foot on tread 12, upper foot on tread 13, body between
# the stiles, top cap at thigh height in front of him; his hand + oil feeder reach bearing S' at x=16 ft.
bx, by = D.objects["LOUVRE_MUSE_0"].location.x, sy            # bearing S' at compartment centre
WALL_Y = 62.10                                                 # boarding face behind the louvre run
top = 4.30; NR = 14; rise = top / NR
k_lo, k_hi = 12, 13                                            # treads under the lower / upper foot
z_lo, z_hi = rise * k_lo, rise * k_hi
lean = 1.20; back = 1.05; hw_t, hw_b = 0.27, 0.36       # 74 deg front, 14 ft steps
SC = D.objects["ATTEND_LOUVRE"].scale.copy()                   # figure scale (x,y ~1.039, z ~1.065)
th = math.radians(10.0)                                        # facing direction (0 = +x, up the steps)
rz = th + math.pi / 2                                          # figure's local -y is its front
R = Matrix.Rotation(rz, 4, 'Z')
HAND_L = Vector((0.66 * 0.7 * FT, -1.55 * FT, (4.4 + 1.1 * 0.6) * FT))   # hand in the (unscaled) arm frame
zf = z_lo + 0.014                                              # figure origin = sole of the lower foot
hxy = (R @ HAND_L)
HAND_OFF = Vector((-0.12, -0.08))                              # hand just short of / in front of the bearing
fx, fy = bx + HAND_OFF.x - hxy.x, by + HAND_OFF.y - hxy.y
src_p, src_a = D.objects["ATTEND_LOUVRE"], D.objects["ATTEND_LOUVRE_ARM"]
man = src_p.copy(); man.name = "ATTEND_OILER"; figs.objects.link(man)
arm = src_a.copy(); arm.name = "ATTEND_OILER_ARM"; figs.objects.link(arm)
for o in (man, arm):
    o.location = (fx, fy, zf); o.rotation_euler = (0, 0, rz)
man["trade"] = "attendant"
# own mesh copy so the shared ATTEND mesh (floor attendant) is untouched; lift his right leg (local x<0,
# the camera side) onto tread 13 (up one rise, centred on that tread; placed below once tx is known).
man.data = man.data.copy(); man.data.name = "ATTEND_OILER_mesh"
bm = bmesh.new(); bm.from_mesh(man.data); bm.verts.ensure_lookup_table()
seen = set(); legs = []
for v in bm.verts:
    if v.index in seen: continue
    stck = [v]; comp = []; seen.add(v.index)
    while stck:
        x = stck.pop(); comp.append(x)
        for e in x.link_edges:
            w2 = e.other_vert(x)
            if w2.index not in seen: seen.add(w2.index); stck.append(w2)
    if max(p.co.z for p in comp) < 0.85 and min(p.co.z for p in comp) < 0.01: legs.append(comp)
assert len(legs) == 2, len(legs)
right = [c for c in legs if sum(p.co.x for p in c) < 0][0]
left = [c for c in legs if c is not right][0]
MW = Matrix.Translation(Vector((fx, fy, zf))) @ R @ Matrix.Diagonal((*SC, 1.0))
stile = lambda z: lean * (1 - z / top)
TD = 0.11                                                      # tread depth (x)
# lower (left) foot on tread k_lo: its toe 1 cm behind the front edge of tread k_hi (so the vertical shin
# clears that tread); the ball of the foot then sits on tread k_lo, heel proud.
toe_lo = max((MW @ p.co).x for p in left)
tx = toe_lo + 0.01 + stile(z_hi) + TD / 2
ty = fy
# upper (right) foot: centred 2.5 cm in front of the centre of tread k_hi, up one rise
c_hi = tx - stile(z_hi) - 0.025
cur = sum((MW @ p.co).x for p in right if p.co.z < 0.01) / len([p for p in right if p.co.z < 0.01])
dW = Vector((c_hi - cur, 0.0, rise))
dL = (R.to_3x3().inverted() @ dW); dL = Vector((dL.x / SC.x, dL.y / SC.y, dL.z / SC.z))
HIP = 0.60                                                     # local z: leg top stays inside the coat
for p in right:                                                # shin swings up/forward, thigh hidden
    w = max(0.0, 1.0 - p.co.z / HIP); p.co += dL * w
# legibility: pale moleskin trousers (period labourers' wear) so the legs read against the dark boarding,
# and dark boots (a box round the bottom 9 cm of each leg) so each foot reads on its pale deal tread.
mole = D.materials.get("CP028_Moleskin") or D.materials.new("CP028_Moleskin")
mole.use_nodes = True; mb = mole.node_tree.nodes["Principled BSDF"]
mb.inputs["Base Color"].default_value = (0.58, 0.54, 0.45, 1); mb.inputs["Roughness"].default_value = 0.9
man.data.materials.append(mole); mi_mole = len(man.data.materials) - 1
mi_boot = [m.name for m in man.data.materials].index("FT_trou_dark")
for comp in (left, right):
    for f in {f for p in comp for f in p.link_faces}:              # only below the coat hem; the leg tops
        if f.calc_center_median().z < 0.42: f.material_index = mi_mole  # in the coat opening stay dark
    z0 = min(p.co.z for p in comp)
    xs = [p.co.x for p in comp]; ys = [p.co.y for p in comp]
    c = Vector(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2 - 0.012, z0 + 0.045))
    res = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(c) @ Matrix.Diagonal((max(xs) - min(xs) + 0.016, max(ys) - min(ys) + 0.04, 0.09, 1)), verts=res["verts"])
    for f in {f for v in res["verts"] for f in v.link_faces}: f.material_index = mi_boot
bm.to_mesh(man.data); bm.free()
assert ty + hw_b * 0.9 + 0.03 < WALL_Y - 0.08, "back legs must clear the boarding"
assert ty + hw_b + 0.035 < WALL_Y - 0.05, "front stiles must clear the boarding"
W = lambda u, w, z: (tx - u, ty + w, z)
sd = D.materials.get("CP028_StepsDeal") or D.materials.new("CP028_StepsDeal")
sd.use_nodes = True; b = sd.node_tree.nodes["Principled BSDF"]
b.inputs["Base Color"].default_value = (0.42, 0.31, 0.19, 1); b.inputs["Roughness"].default_value = 0.85
bm = bmesh.new()
for s in (-1, 1):
    bar(bm, W(0, s * hw_t, top), W(lean, s * hw_b, 0.0), 0.035, 6)             # front stiles
    bar(bm, W(-0.05, s * hw_t * 0.9, top), W(-back, s * hw_b * 0.9, 0.0), 0.03, 6)  # back legs
for i in range(1, NR):
    z = rise * i; f = 1 - z / top
    box(bm, W(lean * f, 0, z), (TD, 2 * (hw_t + (hw_b - hw_t) * f), 0.028))
CAP_U0, CAP_U1 = -0.012, -0.24                                 # cap from just behind the stile top, backwards
box(bm, W((CAP_U0 + CAP_U1) / 2, 0, top + 0.02), (abs(CAP_U1 - CAP_U0), 2 * hw_t + 0.1, 0.04))
for z in (1.2, 2.6):
    f = 1 - z / top; box(bm, W(-0.05 - back * f, 0, z), (0.04, 2 * (hw_t * 0.9 + (hw_b - hw_t) * 0.9 * f), 0.05))
st = mesh_obj("CP028_STEPS", bm, [sd], props)
st["part_kind"] = "steps"
hand = Matrix.Translation(Vector((fx, fy, zf))) @ R @ HAND_L
zinc = D.materials.get("FT_zinc") or steel
bm = bmesh.new()
bar(bm, hand + Vector((0, 0, -0.05)), hand + Vector((0, 0, 0.04)), 0.045, 12)
spout_end = Vector((bx, by - 0.03, sz + 0.03))
bar(bm, hand + Vector((0, 0, 0.03)), spout_end, 0.007, 6)
mesh_obj("CP028_OIL_FEEDER", bm, [zinc], props)
log["FT54"] = {"version": 2, "steps_top_m": top, "rise_m": round(rise, 3), "tread_lo_m": round(z_lo, 3),
               "tread_hi_m": round(z_hi, 3), "man_xy_m": [round(fx, 3), round(fy, 3)], "facing_deg": 10.0,
               "steps_tx_ty_m": [round(tx, 3), round(ty, 3)], "lean_m": lean,
               "back_leg_clear_m": round(WALL_Y - (ty + hw_b * 0.9 + 0.03), 3),
               "hand_m": [round(v, 3) for v in hand], "bearing_m": [round(bx, 3), round(by, 3), round(sz, 3)],
               "reach_gap_m": round((hand - Vector((bx, by, sz))).length, 3)}
print("CP028_DRIVE_LOG", log)
bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out)
