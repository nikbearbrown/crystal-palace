"""2026-11-03 CANDIDATE (Grok Bot executor, no verdict, NOT live; DEPARTURES CN50): CP011_yard near pile + timber bay.
Base: live rounds/c07.blend (CN47 yard + CN49 one-tier lattice KEEP, md5 8cb193fe...). Read only; saves a sibling
rounds/candidates/c07_cp011pile.blend (live c07 is never written). Everything added or changed is a CP011C_* object in
CP011_YARD_CAND with only_cams="CP011_yard" (object-level material links only; shared meshes such as girder24 and shared
materials such as GT_IronPrimer_1850 are NOT edited), so no other c07 shot can change.
  1. near pile heavier: each of the 24 CP011C_GIR_* girder24 members gets a T top flange 9 in x 1.1 in (on top of the
     chord, overall depth 3 ft 1.1 in) and an inverted-T bottom flange 12 in x 1.1 in (inside the 3 ft), after Muse
     lattice-girder-truss-bay (PL.10 Fig.3: overall ~3 ft 1.5 in; flange widths 0.23/0.30 m, thickness 0.028 m, inferred
     there). The girder stock, flanges and column stock take an as-cast dark iron (unprimed foundry skin) via object-level
     material links; Hyde Park girders keep GT_IronPrimer_1850.
  2. timber bay: the CN49 deal floor (whose footprint came out x 2976.7-3023.3, y 93.4-120, i.e. 6 ft short of the
     partition and wider than the bay) is replaced by CP011C_TIMBER_FLOOR2 at x 2984.3-3015.7, y 87.4-126 with the planks
     running along the bay, plus a deal landing through the partition gap (x 2995.5-3004.5, y 74-87.4). Two sticked stacks
     of fresh Baltic deals (3 in x 9 in, 12 ft west / 8 ft cut lengths east, 1 in stickers, ~5.5 ft high) stand in front of the
     partition either side of the gap, clear of the aisle sightline.
  3. smoke: unchanged (live CN47 chimney smoke; no new plumes). --smoke is not implemented on purpose.
blender -b rounds/c07.blend -P scripts/cand_cp011_pile_20261103.py -- [--out PATH] [--no-flanges] [--no-iron] [--no-bay]
  (candidate mode now needs the PRE-pile live c07 pinned at construction commit 8ef6c72; see render_cp011_pile.sh)
LIVE (KEEP 2026-11-03, parent viewed the start + end pairs; DEPARTURES CN50):
blender -b rounds/c07.blend -P scripts/cand_cp011_pile_20261103.py -- --live [--out PATH]
  applies exactly the full candidate build (flanges + as-cast iron + timber bay; no flags) to the live c07 IN PLACE,
  after the CN47 yard and the CN49 one-tier lattice (both required). Camera-scoped by construction: every object it adds
  is a CP011C_* object in CP011_YARD_CAND with only_cams="CP011_yard"; the CN49 CP011C_TIMBER_FLOOR is retagged
  only_cams="NONE_CN50" (never renders); material changes are object-level links on CP011C_GIR_* and single-user meshes
  CP011C_COLUMNS / CP011C_TROLLEY_COLUMN. Marks CP011_YARD_CAND["cp011_pile"] = "CN50 KEEP". Idempotent: if the marker
  exists it only checks (never re-applies). --live refuses --no-flanges / --no-iron / --no-bay. Prints
  CP011_PILE_IN_PLACE True|False.
  -- --check: read-only check, prints CP011_PILE_IN_PLACE and exits (never saves)."""
import bpy, bmesh, math, os, sys
from mathutils import Vector, Matrix
F = 0.3048
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
TAG = "cand_cp011pile_20261103"; SID = "CP011_yard"
coll = bpy.data.collections["CP011_YARD_CAND"]
assert coll.get("cp011_lattice") == "CN49 v2 tiers=1", "base must be the live c07 with the CN49 one-tier lattice"
LIVE = "--live" in argv; MARK = "CN50 KEEP"
def in_place():
    ob = bpy.data.objects; gir = [o for o in ob if o.name.startswith("CP011C_GIR_") and o.name not in ("CP011C_GIR_STICKERS", "CP011C_GIR_FLANGES")]
    new = ("CP011C_GIR_FLANGES", "CP011C_TIMBER_FLOOR2", "CP011C_DEAL_STACKS_A", "CP011C_DEAL_STACKS_B", "CP011C_DEAL_STICKERS")
    return (coll.get("cp011_pile") == MARK and len(gir) == 24 and all(n in ob and ob[n].name in coll.all_objects for n in new)
            and all(o.data.name == "girder24" and o.material_slots[0].link == 'OBJECT'
                    and o.material_slots[0].material.name == "CP011C_iron_ascast" for o in gir)
            and all(ob[n].data.materials[0].name == "CP011C_iron_ascast" for n in ("CP011C_COLUMNS", "CP011C_TROLLEY_COLUMN", "CP011C_GIR_FLANGES"))
            and ob["CP011C_TIMBER_FLOOR"].get("only_cams") == "NONE_CN50"
            and all(o.hide_render and o.get("only_cams") == (SID if o.name != "CP011C_TIMBER_FLOOR" else "NONE_CN50") for o in coll.all_objects)
            and bpy.data.materials["GT_IronPrimer_1850"].name in [m.name for m in bpy.data.meshes["girder24"].materials])
if "--check" in argv:   # read-only
    ok = in_place(); print("CP011_PILE_IN_PLACE", ok); sys.exit(0 if ok else 3)
if coll.get("cp011_pile"):
    if not LIVE: raise SystemExit("base already carries the CP011 pile KEEP (CN50); build candidates from the pre-pile c07 at 8ef6c72")
    ok = in_place(); print("CP011_PILE already applied (idempotent, not re-saved)"); print("CP011_PILE_IN_PLACE", ok)
    sys.exit(0 if ok else 3)
if LIVE: assert not any(f in argv for f in ("--no-flanges", "--no-iron", "--no-bay")), "--live applies only the full KEEP build"
def new_obj(name, data, kind):
    o = bpy.data.objects.new(name, data); coll.objects.link(o)
    o["only_cams"] = SID; o.hide_render = True; o[TAG] = True; o["part_kind"] = kind; return o
def box(bm, x0, x1, y0, y1, z0, z1):
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(((x0 + x1) / 2 * F, (y0 + y1) / 2 * F, (z0 + z1) / 2 * F)) @
                          Matrix.Diagonal((abs(x1 - x0) * F, abs(y1 - y0) * F, abs(z1 - z0) * F, 1)))
def mesh(name, bm, mat):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat); return me
def pmat(name, rgb, rough, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    return m
gir = sorted([o for o in bpy.data.objects if o.name.startswith("CP011C_GIR_") and o.name != "CP011C_GIR_STICKERS"], key=lambda o: o.name)
assert len(gir) == 24

# ---- 1. heavier near pile: flanges + as-cast iron ----
ASCAST = pmat("CP011C_iron_ascast", (0.045, 0.043, 0.042), 0.6, 0.15)
IRONMAT = ASCAST if "--no-iron" not in argv else bpy.data.materials["GT_IronPrimer_1850"]
if "--no-flanges" not in argv:
    TF, BW, TW = 1.1 / 12, 1.0, 0.75                 # flange thickness 1.1 in; bottom 12 in, top 9 in
    bm = bmesh.new()
    for o in gir:
        x, yc, ztop = o.location.x / F, o.location.y / F, o.location.z / F      # ztop = 3.5 ft, bottom at 0.5
        box(bm, x - TW / 2, x + TW / 2, yc - 11.76, yc + 11.76, ztop, ztop + TF)
        box(bm, x - BW / 2, x + BW / 2, yc - 11.76, yc + 11.76, ztop - 3.0, ztop - 3.0 + TF)
    new_obj("CP011C_GIR_FLANGES", mesh("CP011C_GIR_FLANGES", bm, IRONMAT), "stock_girder")
if "--no-iron" not in argv:
    for o in gir:
        o.material_slots[0].link = 'OBJECT'; o.material_slots[0].material = ASCAST
    for n in ("CP011C_COLUMNS", "CP011C_TROLLEY_COLUMN"):
        me = bpy.data.objects[n].data; assert me.users == 1, n; me.materials[0] = ASCAST

# ---- 2. timber bay: floor fixed + landing + deal stacks ----
if "--no-bay" not in argv:
    old = bpy.data.objects["CP011C_TIMBER_FLOOR"]
    old["only_cams"] = "NONE_CN50"; old["cn50"] = "replaced by CP011C_TIMBER_FLOOR2 (footprint fix)"
    deal = bpy.data.materials.new("CP011C_deal_floor2"); deal.use_nodes = True; nt = deal.node_tree; b = nt.nodes["Principled BSDF"]
    bt = nt.nodes.new("ShaderNodeTexBrick"); tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value = (0, 0, math.pi / 2)          # boards run along the bay (world y)
    bt.inputs["Color1"].default_value = (0.56, 0.43, 0.26, 1); bt.inputs["Color2"].default_value = (0.47, 0.35, 0.21, 1)
    bt.inputs["Mortar"].default_value = (0.14, 0.10, 0.07, 1); bt.inputs["Scale"].default_value = 1.0
    bt.inputs["Brick Width"].default_value = 12 * F; bt.inputs["Row Height"].default_value = 0.75 * F; bt.inputs["Mortar Size"].default_value = 0.010
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], bt.inputs["Vector"])
    nt.links.new(bt.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.85
    bm = bmesh.new(); box(bm, 2984.3, 3015.7, 87.4, 126.0, -0.03, 0.07); box(bm, 2995.5, 3004.5, 74.0, 87.4, -0.03, 0.07)
    new_obj("CP011C_TIMBER_FLOOR2", mesh("CP011C_TIMBER_FLOOR2", bm, deal), "floor")
    DEAL_A = pmat("CP011C_deal_fresh_a", (0.60, 0.47, 0.29), 0.8); DEAL_B = pmat("CP011C_deal_fresh_b", (0.52, 0.40, 0.25), 0.8)
    BEAR = bpy.data.materials["CP011C_bearer_oak_weathered"]
    bma, bmb, bms = bmesh.new(), bmesh.new(), bmesh.new()
    W, T, ST, GAP = 0.75, 0.25, 1 / 12, 1 / 12        # deal 9 in x 3 in; sticker 1 in; 1 in air gap between deals
    for (x0, y0, y1, nw, nc) in ((2991.0, 74.5, 86.5, 5, 15), (3005.0, 78.5, 86.5, 5, 15)):   # west 12 ft deals, east 8 ft cut deals
        x1 = x0 + nw * W + (nw - 1) * GAP
        for yb in (y0 + 0.6, (y0 + y1) / 2, y1 - 0.6): box(bms, x0 - 0.2, x1 + 0.2, yb - 0.25, yb + 0.25, 0, 0.5)   # ground bearers
        z = 0.5
        for c in range(nc):
            for i in range(nw):
                xa = x0 + i * (W + GAP); box(bma if (i + c) % 3 else bmb, xa, xa + W, y0, y1, z, z + T)
            z += T
            if c < nc - 1:
                for yb in (y0 + 0.6, (y0 + y1) / 2, y1 - 0.6): box(bms, x0, x1, yb - 0.1, yb + 0.1, z, z + ST)
                z += ST
    new_obj("CP011C_DEAL_STACKS_A", mesh("CP011C_DEAL_STACKS_A", bma, DEAL_A), "timber_stock")
    new_obj("CP011C_DEAL_STACKS_B", mesh("CP011C_DEAL_STACKS_B", bmb, DEAL_B), "timber_stock")
    new_obj("CP011C_DEAL_STICKERS", mesh("CP011C_DEAL_STICKERS", bms, BEAR), "bearer")
    print("DEAL stacks top ft", round(z, 2))

for o in coll.all_objects: assert o.get("only_cams"), o.name
if LIVE:
    coll["cp011_pile"] = MARK
    ok = in_place(); print("CP011_PILE_IN_PLACE", ok)
    if not ok: sys.exit(3)
    out = arg("--out") or bpy.data.filepath
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True); print("CP011_PILE saved", out)
else:
    coll["cp011_pile"] = "CN50 candidate"
    out = arg("--out") or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rounds", "candidates", "c07_cp011pile.blend")
    assert os.path.abspath(out) != os.path.abspath(bpy.data.filepath), "never overwrite live c07"
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True); print("SAVED", out)
