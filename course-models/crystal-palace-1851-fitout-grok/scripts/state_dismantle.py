# HP-DISMANTLE (CP031): 1852 — joint undone under temporary shore; panes/girders lowered; component stacks.
# Illustrative principle, not a documented daily order. DEPARTURES FT45.
exec(open(os.path.join(HERE, "state_common.py")).read())
info = {}; info["doors_open"] = open_south_doors()
removed = 0
for ob in list(bpy.data.objects):
    if ob.get("dress_kind") or ob.get("part_kind") in ("exhibit_case", "exhibit_plinth", "bench", "statue", "crate"):
        bpy.data.objects.remove(ob, do_unlink=True); removed += 1
info["stripped"] = removed
# Hide a bay of roof glass / end screen on the east nave to open to sky (illustrative)
hidden = []
for ob in list(bpy.data.objects):
    pk = ob.get("part_kind", "")
    if pk in ("ridge_glass", "vault_glass", "sash_glass", "end_glass"):
        x, y = ob.location.x / FT, ob.location.y / FT
        if 60 < x < 120 and -40 < y < 40:
            ob.hide_render = True; ob.hide_viewport = True; hidden.append(ob.name)
info["sky_open"] = len(hidden)
# Temporary timber shores under a transept-line girder (support before release)
SHORE_M = TIMBER; SHORE_DK = TIMBER_DK
def shore(name, x, y, h=24.0):
    k = Kit([SHORE_M, SHORE_DK, IRON_DK])
    k.cyl(0, (0, 0, 0), (0, 0, h), 0.55, 10)
    k.box(1, -1.5, 1.5, -1.5, 1.5, 0, 0.6)          # sole
    k.box(1, -1.2, 1.2, -0.8, 0.8, h - 0.5, h + 0.3)  # cap
    k.bar(2, (-0.4, 0, h * 0.35), (0.4, 0, h * 0.7), 0.12)  # brace
    return prop(name, k.done(name.lower()), x, y, 0, 0, part_kind="shore")
shores = []
for i, (x, y) in enumerate([(36, 12), (36, -12), (-36, 12), (-36, -12), (60, 0), (84, 0)]):
    shores.append(shore(f"SHORE_{i}", x, y, 22 + (i % 3)))
info["shores"] = len(shores)
# Component stacks on the south lawn / east yard: girders, sashes, columns
STACK = coll("DISMANTLE_STACKS", ROOT)
def girder_stack(nm, x, y, n=5):
    k = Kit([IRON_DK, SHORE_M])
    for i in range(n):
        z0 = i * 1.1
        k.box(0, -10, 10, -0.4, 0.4, z0, z0 + 0.9)
    k.box(1, -10.5, 10.5, -1.2, 1.2, -0.3, 0.2)  # sleepers
    return prop(nm, k.done(nm.lower()), x, y, 0, math.pi / 2, part_kind="girder_stack")
def sash_stack(nm, x, y, n=8):
    k = Kit([SHORE_M, IRON_DK])
    for i in range(n):
        z0 = i * 0.35
        k.box(0, -4, 4, -2.2, 2.2, z0, z0 + 0.25)
    return prop(nm, k.done(nm.lower()), x, y, 0, 0.3, part_kind="sash_stack")
girder_stack("STACK_GIRDER_A", 20, -210, 6)
girder_stack("STACK_GIRDER_B", 45, -215, 4)
sash_stack("STACK_SASH_A", -30, -208, 10)
sash_stack("STACK_SASH_B", -50, -212, 7)
# Column sections laid horizontal
k = Kit([IRON_DK, SHORE_M])
for i in range(4):
    k.cyl(0, (-8 + i * 0.1, -2 + i * 1.8, 0.6), (8 + i * 0.1, -2 + i * 1.8, 0.6), 0.7, 12)
k.box(1, -10, 10, -4, 4, 0, 0.25)
prop("STACK_COLUMNS", k.done("col_stack"), 70, -205, 0, 0.4, part_kind="column_stack")
info["stacks"] = 5
# Hero joint: a girder end plate with pins half-withdrawn (50 mm detail subject)
k = Kit([IRON_DK, M_("pin_steel", (0.55, 0.56, 0.58), 0.25, 1.0), SHORE_M])
k.box(0, -1.5, 1.5, -0.6, 0.6, 0, 2.4)           # end plate
k.box(0, -0.4, 12, -0.35, 0.35, 0.8, 1.6)         # girder stub
for pz in (0.5, 1.2, 1.9):
    k.cyl(1, (-1.8, 0, pz), (-0.2, 0, pz), 0.12, 8)   # pins pulled out
k.box(2, -2.5, -1.5, -1.2, 1.2, -0.2, 0.3)        # staging plank
prop("JOINT_HERO", k.done("joint_hero"), 36, 0, 8.0, 0, part_kind="joint_detail")
info["joint"] = "hero end-plate with pins withdrawn"
# Workers at the joint and on the stacks
crew = [worker_mesh(j) for j in range(6)]
poses = [
    (34, 2, 8.0, heading_rz(1, 0)), (38, -2, 8.0, heading_rz(-1, 0)),
    (36, 0, 0, heading_rz(0, 1)), (22, -208, 0, heading_rz(0.5, 1)),
    (45, -212, 0, heading_rz(-1, 0)), (-28, -206, 0, heading_rz(1, 0)),
    (68, -203, 0, heading_rz(-0.5, 1)), (60, 2, 0, heading_rz(0, -1)),
]
for j, (x, y, z, rz) in enumerate(poses):
    person(f"DISM_{j:02d}", crew[j % 6], x, y, z, rz, trade="dismantler")
    if z > 10:
        arm_reach(f"DISM_ARM_{j}", x, y, z, rz, up=0.4, tool="crank", mat=WK["fustian"])
info["crew"] = len(poses)
so_ = bpy.data.objects.get("GT_Sun")
if so_:
    so_.rotation_euler.x = math.radians(35)
    so_.data.color = (1.0, 0.94, 0.82)
info["sun"] = "1852 workday"
STATE_INFO = info
print("DISMANTLE", info, flush=True)
