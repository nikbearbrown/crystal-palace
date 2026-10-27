# HP-EMPTY (CP030): late 1851–1852 — packing crates replace exhibits; sparse staff in an emptying aisle.
# DEPARTURES FT44.
exec(open(os.path.join(HERE, "state_common.py")).read())
info = {}; info["doors_open"] = open_south_doors()
# Strip any residual dressing / muse exhibits (MUSE_ON is off for empty, but be safe)
removed = 0
for ob in list(bpy.data.objects):
    if ob.get("dress_kind") or ob.get("part_kind") in ("exhibit_case", "exhibit_plinth", "bench", "statue"):
        bpy.data.objects.remove(ob, do_unlink=True); removed += 1
info["stripped"] = removed
# Packing crates along the nave / transept aisles (where cases stood)
CRATE_M = M_("crate_deal", (0.42, 0.34, 0.22), 0.85)
CRATE_DK = M_("crate_mark", (0.18, 0.14, 0.10), 0.9)
ROPE_M = M_("lashing", (0.50, 0.42, 0.30), 0.95)
def crate_mesh(tag, L=6.0, W=4.0, H=4.5):
    k = Kit([CRATE_M, CRATE_DK, ROPE_M])
    k.box(0, -L/2, L/2, -W/2, W/2, 0, H)
    k.box(1, -L/2 - 0.05, L/2 + 0.05, -0.15, 0.15, H - 0.4, H)  # lid batten
    k.bar(2, (-L/2, 0, H * 0.55), (L/2, 0, H * 0.55), 0.08)
    return k.done("crate_" + tag)
CRATES = coll("EMPTY_CRATES", ROOT)
n_crates = 0
# aisle lines: |x|≈46 (case line) and centre-nave offsets
spots = []
for sy in (-1, 1):
    for j in range(8):
        spots.append((sy * 46.5, sy * (40 + 22 * j), 0 if j % 2 else math.pi / 2))
        spots.append((sy * 38.0, sy * (52 + 24 * j), math.pi / 2 if j % 3 else 0))
for j in range(6):
    spots.append((-12 + (j % 3) * 12, -80 - 18 * (j // 3), 0.2))
    spots.append((-8 + (j % 2) * 16, 70 + 20 * (j // 2), math.pi / 2))
for i, (x, y, rz) in enumerate(spots):
    L = 5.0 + (i % 3) * 1.2; W = 3.5 + (i % 2) * 0.8; H = 3.8 + (i % 4) * 0.6
    prop(f"CRATE_{i:02d}", crate_mesh(f"{i}", L, W, H), x, y, 0, rz, part_kind="crate")
    n_crates += 1
info["crates"] = n_crates
# A few open emptied cases / skids
for i, (x, y) in enumerate([(-46, -20), (46, 30), (-46, 90), (40, -100)]):
    k = Kit([CRATE_M, TIMBER_DK]); k.box(0, -3, 3, -2, 2, 0, 0.4); k.box(1, -2.8, 2.8, -1.8, 1.8, 0.4, 2.2)
    prop(f"OPEN_CASE_{i}", k.done(f"open_case_{i}"), x, y, 0, math.pi / 2 if i % 2 else 0, part_kind="open_case")
# Sparse staff — packers and a clerk
staff_n = 0
packer = [worker_mesh(j) for j in range(4)]
for j, (x, y, rz) in enumerate([
    (-44, -18, heading_rz(1, 0)), (44, 28, heading_rz(-1, 0)), (-10, -78, heading_rz(0, 1)),
    (8, 72, heading_rz(0, -1)), (-46, 88, heading_rz(1, -0.3)), (42, -98, heading_rz(-1, 0.2)),
    (-20, 10, heading_rz(0.5, -1)), (18, -40, heading_rz(-0.3, 1)), (0, -120, heading_rz(0, 1)),
]):
    person(f"PACKER_{j:02d}", packer[j % 4], x, y, 0, rz, trade="packer"); staff_n += 1
    if j % 3 == 0:
        arm_reach(f"PACKER_ARM_{j}", x, y, 0, rz, up=0.6, tool="crank", mat=WK["smock"])
info["staff"] = staff_n
# Winter-garden light: cooler, thinner crowd feel (no ceremony sun)
so_ = bpy.data.objects.get("GT_Sun")
if so_:
    so_.rotation_euler.x = math.radians(28)
    so_.data.color = (0.95, 0.96, 1.0)
    so_.data.energy = getattr(so_.data, "energy", 3.0) * 0.85
info["sun"] = "late-winter pale"
STATE_INFO = info
print("EMPTY", info, flush=True)
