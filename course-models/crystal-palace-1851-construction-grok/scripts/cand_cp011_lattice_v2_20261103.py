"""2026-11-03 CANDIDATE v2 (Grok Bot executor, no verdict, NOT live; DEPARTURES CN49): CP011_yard lattice v2.
Supersedes CN48 v1 (REJECTED by the parent 2026-11-03 for the floating smoke plume and the 6/9-point luma drop).
Base: live rounds/c07.blend (CP011 yard KEEP, CN47). Saves a sibling candidate blend (default
rounds/candidates/c07_cp011lattice_v2.blend; live c07 is never written).
  1. girders on edge (kept from CN48): identical girder24 members, web vertical, so the aisle-side girder shows its
     open diagonal web.  --tiers 2 = CN48 layout (rows of 6 at 1.3 ft, two tiers + stickers, ~7 ft, 33 members);
     --tiers 1 (default) = one tier, rows of 8 at 1.2 ft pitch on the existing bearers (extended 1.6 ft east, clear of
     the shed columns at x 3015.6), top at 3.5 ft, 24 members: reads as a stockpile, not a wall.
  2. timber bay sightline + deal floor: unchanged from CN48.
  3. smoke: NO new smoke. The live CN47 chimney smoke objects are not touched (only_cams=CP011_yard as live).
blender -b rounds/c07.blend -P scripts/cand_cp011_lattice_v2_20261103.py -- [--tiers 1|2] [--out PATH] [--no-bay]"""
import bpy, bmesh, math, os, sys
from mathutils import Vector, Matrix
F = 0.3048
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
TAG = "cand_cp011lattice_v2_20261103"; SID = "CP011_yard"
assert "CP011_YARD_CAND" in bpy.data.collections, "base must be the live c07 with the CP011 yard (CN47)"
coll = bpy.data.collections["CP011_YARD_CAND"]
def new_obj(name, data, kind):
    o = bpy.data.objects.new(name, data); coll.objects.link(o)
    o["only_cams"] = SID; o.hide_render = True; o[TAG] = True; o["part_kind"] = kind; return o
def box(bm, x0, x1, y0, y1, z0, z1):
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(((x0 + x1) / 2 * F, (y0 + y1) / 2 * F, (z0 + z1) / 2 * F)) @
                          Matrix.Diagonal((abs(x1 - x0) * F, abs(y1 - y0) * F, abs(z1 - z0) * F, 1)))
def mesh(name, bm, mat):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat); return me

# ---- 1. girders on edge ----
for o in [o for o in bpy.data.objects if o.name.startswith("CP011C_GIR_")]: bpy.data.objects.remove(o, do_unlink=True)
G24 = bpy.data.meshes["girder24"]          # x +-11.76 ft, y +-0.167 ft (web thickness), z -3..0 ft (depth)
BEAR = bpy.data.materials["CP011C_bearer_oak_weathered"]
TIERS = int(arg("--tiers", "1")); bm = bmesh.new(); X0 = 3006.2; T = 0.5; D = 3.0
if TIERS == 2: PITCH, LAYOUT = 1.3, ((2.0, (6, 6)), (34.0, (6, 6)), (66.0, (6, 3)))
else:
    PITCH, LAYOUT = 1.2, ((2.0, (8,)), (34.0, (8,)), (66.0, (8,)))
    for yc in (2.0, 34.0, 66.0):                             # extend the live bearers (x 3005.5-3013.5) east under row 8
        for yb in (yc - 9, yc, yc + 9): box(bm, 3013.5, 3015.1, yb - 0.25, yb + 0.25, 0.0, T)
for pile, (yc, tiers) in enumerate(LAYOUT):
    zb = T                                                   # existing ground bearers top at 0.5 ft
    for tier, n in enumerate(tiers):
        if tier:                                             # stickers (timber packing) between tiers, every 9 ft
            for yb in (yc - 9, yc, yc + 9): box(bm, X0 - 0.6, X0 + (tiers[0] - 1) * PITCH + 0.6, yb - 0.25, yb + 0.25, zb, zb + T)
            zb += T
        for i in range(n):
            x = X0 + (i + (tiers[0] - n) * 0.5 * (tier > 0)) * PITCH
            o = new_obj(f"CP011C_GIR_{pile}_{tier}{i}", G24, "stock_girder")
            o.location = Vector((x, yc, zb + D)) * F; o.rotation_euler = (0, 0, math.pi / 2)
            o[TAG] = f"identical girder24 on edge (web vertical), CN49 tiers={TIERS}"
        zb += D
print("GIRDERS", TIERS, "tiers", sum(sum(t) for _, t in LAYOUT), "members")
new_obj("CP011C_GIR_STICKERS", mesh("CP011C_GIR_STICKERS", bm, BEAR), "bearer")

# ---- 2. timber bay sightline + floor ----
if "--no-bay" not in argv:
    DX_W = -5.5
    for n in ("CP011C_TROLLEY", "CP011C_TROLLEY_WHEELS", "CP011C_TROLLEY_COLUMN"):   # column-pile toes end at x ~2989.8
        bpy.data.objects[n].location.x += DX_W * F
    bpy.data.objects["CP011C_P01_haul"].location.x = 2993.5 * F; bpy.data.objects["CP011C_P02_haul"].location.x = 2995.1 * F
    c = bpy.data.objects["CP011C_P04_clerk"]; c.location = Vector((3004.6, 10.0, 0)) * F
    tb = bpy.data.objects["CP011C_TALLY_BOARD"]; tb.location.x += (3004.6 - 3002.8) * F; tb.location.y += (10.0 - 12.0) * F
    deal = bpy.data.materials.get("CP011C_deal_floor") or bpy.data.materials.new("CP011C_deal_floor"); deal.use_nodes = True
    nt = deal.node_tree; b = nt.nodes["Principled BSDF"]
    bt = nt.nodes.new("ShaderNodeTexBrick"); tc = nt.nodes.new("ShaderNodeTexCoord")
    bt.inputs["Color1"].default_value = (0.50, 0.38, 0.23, 1); bt.inputs["Color2"].default_value = (0.42, 0.31, 0.19, 1)
    bt.inputs["Mortar"].default_value = (0.16, 0.12, 0.08, 1); bt.inputs["Scale"].default_value = 1.0
    bt.inputs["Brick Width"].default_value = 12 * F; bt.inputs["Row Height"].default_value = 0.75 * F; bt.inputs["Mortar Size"].default_value = 0.012
    nt.links.new(tc.outputs["Object"], bt.inputs["Vector"]); nt.links.new(bt.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.85
    bm = bmesh.new(); box(bm, 2984.0, 3016.0, 87.4, 126.0, -0.03, 0.06)
    fl = new_obj("CP011C_TIMBER_FLOOR", mesh("CP011C_TIMBER_FLOOR", bm, deal), "floor")
    # brick texture runs along object x; rotate the planks so they run along the bay (y): rotate mesh 90 about z
    fl.data.transform(Matrix.Translation(Vector((3000.0, 106.7, 0)) * F) @ Matrix.Rotation(math.pi / 2, 4, 'Z') @ Matrix.Translation(-Vector((3000.0, 106.7, 0)) * F))
    fl.data.transform(Matrix.Translation(Vector((3000.0, 106.7, 0)) * F) @ Matrix.Diagonal((38.6 / 32.0, 32.0 / 38.6, 1, 1)) @ Matrix.Translation(-Vector((3000.0, 106.7, 0)) * F))

# ---- 3. smoke: none added; live CN47 CP011C_CHIMNEY_*_SMOKE left exactly as live ----
out = arg("--out") or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rounds", "candidates", "c07_cp011lattice_v2.blend")
assert os.path.abspath(out) != os.path.abspath(bpy.data.filepath), "never overwrite live c07"
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True); print("SAVED", out)
