"""2026-11-03 CANDIDATE (Grok Bot executor, no verdict, NOT live; DEPARTURES CN48): CP011_yard follow-ups 1-3.
Base: live rounds/c07.blend (CP011 yard KEEP, CN47, construction 2bdb3ea). Saves rounds/candidates/c07_cp011lattice.blend
(sibling candidate, CP011_yard cameras only; live c07 is never written).
  1. girder piles: the 33 girder24 members (12/12/9) lay flat, web horizontal, 0.36 ft pitch, so end-on they read as a
     plank stack. Re-stacked ON EDGE (web vertical) in rows of 6 at 1.3 ft pitch, two tiers with timber stickers between
     tiers, so the aisle-side girder shows its open diagonal web between top and bottom flanges and the yard reads lattice.
  2. timber bay: haulers + trolley shifted west out of the aisle centre, clerk shifted east against the first girder pile,
     and a pale deal plank floor laid in the bay (y 87.4-126) so the separate timber area reads as its own floor.
  3. smoke: the dark opaque blobs (leaning east, off frame) are hidden; volumetric plumes from both chimneys drift
     west-south-west and flatten (heavy day), crossing the visible sky; no shadows cast.
blender -b rounds/c07.blend -P scripts/cand_cp011_lattice_20261103.py -- [--out PATH] [--no-smoke] [--no-bay]"""
import bpy, bmesh, math, os, sys
from mathutils import Vector, Matrix
F = 0.3048
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
TAG = "cand_cp011lattice_20261103"; SID = "CP011_yard"
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
bm = bmesh.new(); PITCH = 1.3; X0 = 3006.2; T = 0.5; D = 3.0
for pile, (yc, tiers) in enumerate(((2.0, (6, 6)), (34.0, (6, 6)), (66.0, (6, 3)))):
    zb = T                                                   # existing ground bearers top at 0.5 ft
    for tier, n in enumerate(tiers):
        if tier:                                             # stickers (timber packing) between tiers, every 9 ft
            for yb in (yc - 9, yc, yc + 9): box(bm, X0 - 0.6, X0 + (tiers[0] - 1) * PITCH + 0.6, yb - 0.25, yb + 0.25, zb, zb + T)
            zb += T
        for i in range(n):
            x = X0 + (i + (tiers[0] - n) * 0.5 * (tier > 0)) * PITCH
            o = new_obj(f"CP011C_GIR_{pile}_{tier}{i}", G24, "stock_girder")
            o.location = Vector((x, yc, zb + D)) * F; o.rotation_euler = (0, 0, math.pi / 2)
            o[TAG] = "identical girder24 on edge (web vertical), CN48"
        zb += D
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

# ---- 3. volumetric smoke ----
if "--no-smoke" not in argv:
    for n in ("CP011C_CHIMNEY_N_SMOKE", "CP011C_CHIMNEY_E_SMOKE"):
        o = bpy.data.objects[n]; o["only_cams"] = "NONE_CN48"; o[TAG] = "opaque blobs hidden, replaced by volume plume"
    sm = bpy.data.materials.get("CP011C_smoke_volume") or bpy.data.materials.new("CP011C_smoke_volume"); sm.use_nodes = True
    nt = sm.node_tree; nt.nodes.remove(nt.nodes["Principled BSDF"]); out = nt.nodes["Material Output"]
    pv = nt.nodes.new("ShaderNodeVolumePrincipled"); pv.inputs["Color"].default_value = (0.10, 0.095, 0.09, 1); pv.inputs["Absorption Color"].default_value = (0.03, 0.028, 0.025, 1)
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 0.5; nz.inputs["Detail"].default_value = 6; nz.inputs["Roughness"].default_value = 0.6
    tc = nt.nodes.new("ShaderNodeTexCoord"); nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs[1].default_value = 0.45; mr.inputs[2].default_value = 0.72
    mr.inputs[3].default_value = 0.0; mr.inputs[4].default_value = float(arg("--smoke-density", "2.0"))
    nt.links.new(nz.outputs["Fac"], mr.inputs[0]); nt.links.new(mr.outputs[0], pv.inputs["Density"])
    nt.links.new(pv.outputs["Volume"], out.inputs["Volume"])
    # heavy-day downwash: plumes leave the stack, sink and spread west-south-west; the north plume drops into the visible
    # west sky beyond the shed's west column line (polyline control points in ft, radius grows along the path)
    PATHS = {"CP011C_CHIMNEY_N": [(3036, 205, 81), (2995, 196, 72), (2955, 182, 55), (2915, 166, 44), (2870, 150, 38), (2825, 132, 34)],
             "CP011C_CHIMNEY_E": [(3054, 130, 66), (3040, 126, 70), (3015, 118, 68)]}
    for nm, P in PATHS.items():
        bm = bmesh.new(); N = 14 * (len(P) - 1)
        for k in range(N + 1):
            u = k / N * (len(P) - 1); i = min(int(u), len(P) - 2); f = u - i
            c = Vector(P[i]).lerp(Vector(P[i + 1]), f); t = k / N
            r = 4.0 + (18 if nm.endswith("N") else 8) * t
            bmesh.ops.create_icosphere(bm, subdivisions=2, radius=r * F,
                                       matrix=Matrix.Translation(c * F) @ Matrix.Diagonal((1.5, 1.2, 0.7, 1)))
        s = new_obj(nm + "_PLUME", mesh(nm + "_PLUME", bm, sm), "smoke")
        s.visible_shadow = False
out = arg("--out") or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rounds", "candidates", "c07_cp011lattice.blend")
assert os.path.abspath(out) != os.path.abspath(bpy.data.filepath), "never overwrite live c07"
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True); print("SAVED", out)
