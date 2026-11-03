"""2026-11-03 CANDIDATE (Grok Bot executor, not a verdict): CP011_yard 'Factory and park work together' (O-WORKSHOP, illustrative, CN11 grade C).
Base: rounds/c07.blend (live CP011_yard, unchanged). Saves rounds/candidates/c07_cp011yard.blend for CP011_yard ONLY
(never render other shots from it: it hides the CP014 drainage cutaway collection and rebuilds the yard dressing).
Why: in live c07 the beat 'identical iron members are prepared and stacked; timber parts occupy a separate work area'
reads as an almost empty open shed in a lime field: two low girder piles, two small column pyramids, a few timber blocks
at the far end, three FIGURE block stand-ins, and the white CP014 cutaway backdrop board visible through the east side.
Changes (DEPARTURES CN47):
  * CP014 cutaway collection DETAIL_DRAINAGE hidden in this blend (backdrop, labels, fill light) - it leaked into CP011.
  * factory setting: cinder yard surface; brick works range east of the shed (slate roof, arched windows, chimney);
    brick works block closing the north vista with a second chimney; close-boarded yard fence on the west.
    Illustrative only - no verified Fox Henderson / Smethwick works plan (storyboard B/I/U; CN11).
  * iron stock: girder piles 12 high on timber bearers (three piles east of the aisle, same girder24 mesh = identical members);
    column pyramids 5-4-3-2 on bearers (three piles west), cut from the same 8 in column section.
  * timber bay (separate work area, north end): low board partition with a gap, sash-bar racks on both sides,
    Paxton gutter stack, two trestle benches with sash bars and shavings, workmen planing (fig-38 used for mood/dress only).
  * handling: low iron-wheeled trolley carrying one column in the aisle with two hauling men; a barrow by the girders.
  * people: CP011 FIGURE stand-ins replaced and new figures added with survey people_lib 1850s_workman (cap, dark matte
    fustian, as CP012/CP016), plus one 1850s_gentleman clerk with a tally board; explicit poses; render with --no-people.
blender -b rounds/c07.blend -P scripts/cand_cp011_yard_20261103.py -- [--out PATH]
LIVE (KEEP 2026-11-03, parent viewed the pairs; DEPARTURES CN47):
blender -b rounds/c07.blend -P scripts/cand_cp011_yard_20261103.py -- --live [--out PATH]
  applies the same build to the live c07 IN PLACE, but camera-scoped so no other c07 shot changes:
  every new CP011C_* object gets only_cams="CP011_yard" (render_views.py shows it only for CP011_yard_* cameras, saved
  hide_render True); everything the candidate hid (DETAIL_DRAINAGE incl. the CP014 cutaway backdrop/labels/fill and
  KSITE_GUTTER_WATER, KYARD_GIR_*/KYARD_COLUMNS/KYARD_TIMBER, KWORKER_024-026_CP011) gets hide_cams="CP011_yard"
  (hidden only for CP011_yard_* cameras, otherwise untouched); KYARD_GROUND keeps its saved material (GT_Spoil) and gets
  cam_mat="CP011_yard=CP011C_cinder_yard" (render_views.py swaps the slot for CP011_yard_* cameras only); the people_lib figures are tagged so the render-time
  people swap of other shots ignores them. Idempotent: if CP011_YARD_CAND exists it only checks. Prints CP011_YARD_IN_PLACE.
  -- --check: read-only check, prints CP011_YARD_IN_PLACE and exits (never saves)."""
import bpy, bmesh, math, os, sys, hashlib
from mathutils import Vector, Matrix
F = 0.3048; IN = F / 12
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
TAG = "cand_cp011yard_20261103"
LIVE = "--live" in argv; SID = "CP011_yard"
sc = bpy.context.scene
def in_place():
    c = bpy.data.collections.get("CP011_YARD_CAND")
    if c is None: return False
    new = list(c.all_objects); dd = bpy.data.collections.get("DETAIL_DRAINAGE")
    old = [bpy.data.objects[n] for n in ("KWORKER_024_CP011", "KWORKER_025_CP011", "KWORKER_026_CP011", "KYARD_COLUMNS", "KYARD_TIMBER")]
    old += [o for o in bpy.data.objects if o.name.startswith("KYARD_GIR_")] + (list(dd.all_objects) if dd else [])
    return (len(new) >= 40 and all(o.get("only_cams") == SID for o in new)
            and all(o.get("hide_cams") == SID and not o.hide_render for o in old)
            and bpy.data.objects["KYARD_GROUND"].get("cam_mat") == SID + "=CP011C_cinder_yard"
            and bpy.data.objects["KYARD_GROUND"].data.materials[0].name == bpy.data.objects["KYARD_GROUND"].get("base_mat")
            and "CP011C_cinder_yard" in bpy.data.materials
            and not any(d.name.startswith("CPL3_") for d in list(bpy.data.meshes) + list(bpy.data.materials)))
if "--check" in argv:   # read-only: never builds or saves
    ok = in_place(); print("CP011_YARD_IN_PLACE", ok); sys.exit(0 if ok else 3)
if LIVE and "CP011_YARD_CAND" in bpy.data.collections:
    ok = in_place(); print("CP011_YARD already applied (idempotent, not re-saved)"); print("CP011_YARD_IN_PLACE", ok)
    sys.exit(0 if ok else 3)
def hide_for_cp011(o, why):
    if LIVE: o["hide_cams"] = SID; o[TAG] = why + " (hide_cams CP011_yard only)"
    else: o.hide_render = True; o.hide_viewport = True; o[TAG] = why
OY = bpy.data.collections["OFFSITE_YARD"]
coll = bpy.data.collections.new("CP011_YARD_CAND"); OY.children.link(coll)

# ---------------- hide the CP014 cutaway (leaks into CP011 east side) ----------------
for o in [o for o in bpy.data.objects if o and "DETAIL_DRAINAGE" in [c.name for c in o.users_collection]]:
    hide_for_cp011(o, "hidden in CP011-only blend")

# ---------------- materials ----------------
def pmat(name, col, rough=0.85, fn=None):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.25
    m.diffuse_color = (*col, 1)
    if fn: fn(nt, b)
    return m
def brick_nodes(nt, b):
    tc = nt.nodes.new("ShaderNodeTexCoord"); bt = nt.nodes.new("ShaderNodeTexBrick")
    bt.inputs["Color1"].default_value = (0.23, 0.085, 0.055, 1); bt.inputs["Color2"].default_value = (0.17, 0.07, 0.05, 1)
    bt.inputs["Mortar"].default_value = (0.30, 0.27, 0.23, 1); bt.inputs["Scale"].default_value = 1.0
    bt.inputs["Brick Width"].default_value = 9 * IN; bt.inputs["Row Height"].default_value = 3 * IN
    bt.inputs["Mortar Size"].default_value = 0.35 * IN
    # brick faces are vertical: map world (x+y, z) so courses run horizontally on both wall directions
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); add = nt.nodes.new("ShaderNodeMath"); com = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0]); nt.links.new(sep.outputs[0], add.inputs[0]); nt.links.new(sep.outputs[1], add.inputs[1])
    nt.links.new(add.outputs[0], com.inputs[0]); nt.links.new(sep.outputs[2], com.inputs[1])
    nt.links.new(com.outputs[0], bt.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 0.6
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = 'RGBA'; mix.inputs["Factor"].default_value = 0.25
    nt.links.new(bt.outputs["Color"], mix.inputs[6]); nt.links.new(nz.outputs["Color"], mix.inputs[7])
    soot = nt.nodes.new("ShaderNodeMix"); soot.data_type = 'RGBA'; soot.inputs["Factor"].default_value = 0.55
    nt.links.new(bt.outputs["Color"], soot.inputs[6]); soot.inputs[7].default_value = (0.11, 0.06, 0.045, 1)
    nt.links.new(soot.outputs[2], b.inputs["Base Color"])
def cinder_nodes(nt, b):
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.0; nz.inputs["Detail"].default_value = 8
    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = (0.130, 0.115, 0.095, 1)
    ramp.color_ramp.elements[1].color = (0.250, 0.220, 0.180, 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs[0]); nt.links.new(ramp.outputs[0], b.inputs["Base Color"])
BRICK = pmat("CP011C_brick_sooted", (0.2, 0.08, 0.05), 0.9, brick_nodes)
SLATE = pmat("CP011C_slate", (0.07, 0.075, 0.085), 0.7)
STONE = pmat("CP011C_stone_dressing", (0.42, 0.39, 0.34), 0.9)
WINDOW = pmat("CP011C_window_dark", (0.02, 0.025, 0.03), 0.6)
CINDER = pmat("CP011C_cinder_yard", (0.11, 0.10, 0.08), 0.95, cinder_nodes)
FENCE = pmat("CP011C_fence_tarred", (0.06, 0.05, 0.04), 0.9)
BEARER = pmat("CP011C_bearer_oak_weathered", (0.16, 0.12, 0.08), 0.9)
SHAV = pmat("CP011C_shavings", (0.55, 0.42, 0.26), 0.9)
SOOT = pmat("CP011C_smoke", (0.12, 0.12, 0.12), 1.0)
IRON = bpy.data.materials["GT_IronPrimer_1850"]; WOOD = bpy.data.materials["GT_Timber"]; WAG = bpy.data.materials["GT_WagonTimber"]

def box(bm, x0, x1, y0, y1, z0, z1):
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(((x0 + x1) / 2 * F, (y0 + y1) / 2 * F, (z0 + z1) / 2 * F)) @
                          Matrix.Diagonal((abs(x1 - x0) * F, abs(y1 - y0) * F, abs(z1 - z0) * F, 1)))
def cyl(bm, a, b, r, seg=12):
    a = Vector(a) * F; b = Vector(b) * F; d = b - a
    M = Matrix.Translation((a + b) / 2) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r * F, radius2=r * F, depth=d.length, matrix=M)
def obj(name, bm, mat, props=None):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
    for p in me.polygons: p.use_smooth = False
    o = bpy.data.objects.new(name, me); coll.objects.link(o); o[TAG] = True; o["part_kind"] = (props or {}).get("part_kind", "dressing")
    return o

# ---------------- ground ----------------
bm = bmesh.new(); box(bm, 2930, 3075, -140, 230, -0.08, -0.03); obj("CP011C_CINDER_YARD", bm, CINDER, {"part_kind": "ground"})
KYG = bpy.data.objects["KYARD_GROUND"]
if LIVE:   # camera-scoped material: the saved slot keeps the old material (the yard ground bounces light into CP014/CP010/
    # CP013 frames, max 1-4 of 255 if swapped globally); render_views.py swaps to cam_mat for CP011_yard_* cameras only
    KYG["base_mat"] = KYG.data.materials[0].name; KYG["cam_mat"] = SID + "=" + CINDER.name; KYG[TAG] = "cinder for CP011_yard only (cam_mat)"
else: KYG.data.materials[0] = CINDER

# ---------------- brick works range east, north block, chimneys, west fence ----------------
def gable_range(name, x0, x1, y0, y1, eave, ridge, ridge_axis="y", win_face=None, nwin=0, win_h=(5, 13)):
    bm = bmesh.new(); box(bm, x0, x1, y0, y1, 0, eave)
    # gable ends as triangular prisms
    if ridge_axis == "y":
        xm = (x0 + x1) / 2
        for yy in (y0, y1):
            vs = [bm.verts.new((x * F, yy * F, z * F)) for x, z in ((x0, eave), (x1, eave), (xm, ridge))]; bm.faces.new(vs)
    else:
        ym = (y0 + y1) / 2
        for xx in (x0, x1):
            vs = [bm.verts.new((xx * F, y * F, z * F)) for y, z in ((y0, eave), (y1, eave), (ym, ridge))]; bm.faces.new(vs)
    walls = obj(name + "_BRICK", bm, BRICK, {"part_kind": "works_wall"})
    bm = bmesh.new(); t = 0.4
    if ridge_axis == "y":
        xm = (x0 + x1) / 2
        for side in (-1, 1):
            xe = x0 - 1 if side < 0 else x1 + 1
            vs = [bm.verts.new((x * F, y * F, z * F)) for x, y, z in ((xe, y0 - 1, eave - 0.5), (xm, y0 - 1, ridge + t), (xm, y1 + 1, ridge + t), (xe, y1 + 1, eave - 0.5))]
            bm.faces.new(vs)
    else:
        ym = (y0 + y1) / 2
        for side in (-1, 1):
            ye = y0 - 1 if side < 0 else y1 + 1
            vs = [bm.verts.new((x * F, y * F, z * F)) for x, y, z in ((x0 - 1, ye, eave - 0.5), (x0 - 1, ym, ridge + t), (x1 + 1, ym, ridge + t), (x1 + 1, ye, eave - 0.5))]
            bm.faces.new(vs)
    bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.25 * F)
    obj(name + "_SLATE", bm, SLATE, {"part_kind": "works_roof"})
    if win_face and nwin:
        bm = bmesh.new(); bs = bmesh.new()
        for k in range(nwin):
            if win_face == "w":
                yc = y0 + (y1 - y0) * (k + 0.5) / nwin
                box(bm, x0 - 0.25, x0 + 0.05, yc - 2.2, yc + 2.2, win_h[0], win_h[1])
                box(bs, x0 - 0.45, x0, yc - 2.8, yc + 2.8, win_h[0] - 0.9, win_h[0] - 0.3)     # stone sill
                box(bs, x0 - 0.35, x0, yc - 2.6, yc + 2.6, win_h[1], win_h[1] + 0.9)           # lintel
            else:
                xc = x0 + (x1 - x0) * (k + 0.5) / nwin
                box(bm, xc - 2.2, xc + 2.2, y0 - 0.25, y0 + 0.05, win_h[0], win_h[1])
                box(bs, xc - 2.8, xc + 2.8, y0 - 0.45, y0, win_h[0] - 0.9, win_h[0] - 0.3)
                box(bs, xc - 2.6, xc + 2.6, y0 - 0.35, y0, win_h[1], win_h[1] + 0.9)
        obj(name + "_WINDOWS", bm, WINDOW, {"part_kind": "works_window"}); obj(name + "_STONE", bs, STONE, {"part_kind": "works_dressing"})
    return walls
gable_range("CP011C_WORKS_EAST", 3030, 3062, -110, 150, 22, 33, "y", "w", 11)
gable_range("CP011C_WORKS_NORTH", 2948, 3052, 176, 214, 26, 37, "x", "s", 9, (6, 16))
# big doorway into the north works on the aisle axis (dark opening) with a cart track
bm = bmesh.new(); box(bm, 2993, 3007, 175.6, 176.05, 0, 14); obj("CP011C_WORKS_NORTH_DOOR", bm, WINDOW, {"part_kind": "works_door"})
for nm, (cx, cy, h) in {"CP011C_CHIMNEY_N": (3036, 205, 78), "CP011C_CHIMNEY_E": (3054, 130, 64)}.items():
    bm = bmesh.new(); box(bm, cx - 3.2, cx + 3.2, cy - 3.2, cy + 3.2, 0, h); box(bm, cx - 3.9, cx + 3.9, cy - 3.9, cy + 3.9, h - 2.5, h - 1.2)
    obj(nm, bm, BRICK, {"part_kind": "chimney"})
    bm = bmesh.new()
    for k in range(5):   # thin smoke drift (low, dark, matte blobs leaning east)
        c = Vector((cx + 4 + k * 7, cy - k * 1.5, h + 4 + k * 3.2)); r = 3.0 + k * 1.6
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=r * F, matrix=Matrix.Translation(c * F) @ Matrix.Diagonal((1.4, 1, 0.6, 1)))
    s = obj(nm + "_SMOKE", bm, SOOT, {"part_kind": "smoke"}); s.visible_shadow = False
bm = bmesh.new()   # west close-boarded fence 8 ft on posts, x 2960
for y in range(-130, 176, 8): box(bm, 2959.6, 2960.4, y - 0.25, y + 0.25, 0, 8.5)
box(bm, 2960.4, 2960.8, -130, 176, 0.3, 8.0)
obj("CP011C_FENCE_WEST", bm, FENCE, {"part_kind": "fence"})

# ---------------- iron stock: identical girders and columns on bearers ----------------
for o in [bpy.data.objects[n] for n in bpy.data.objects.keys() if n.startswith("KYARD_GIR_") or n in ("KYARD_COLUMNS", "KYARD_TIMBER")]:
    hide_for_cp011(o, "replaced by CP011C stock")
G24 = bpy.data.meshes["girder24"]
bm_bear = bmesh.new()
for pile, yc in enumerate((2.0, 34.0, 66.0)):              # girders: 12 high, lying flat, bearers every 8 ft
    for yb in (yc - 9, yc, yc + 9): box(bm_bear, 3005.5, 3013.5, yb - 0.25, yb + 0.25, 0, 0.5)
    nh = 12 if pile < 2 else 9
    for k in range(nh):
        o = bpy.data.objects.new(f"CP011C_GIR_{pile}_{k:02d}", G24); coll.objects.link(o)
        o.location = Vector((3009.5, yc, 0.55 + k * 0.36)) * F; o.rotation_euler = (math.pi / 2, 0, math.pi / 2)
        o["part_kind"] = "stock_girder"; o[TAG] = "identical girder24 (24 ft cast girder, K03)"
bm = bmesh.new()
for pile, yc in enumerate((2.0, 34.0, 66.0)):              # columns: 8 in dia, 18 ft 8 in, pyramids 5-4-3-2 on bearers
    for yb in (yc - 7, yc + 7): box(bm_bear, 2985.5, 2993.5, yb - 0.25, yb + 0.25, 0, 0.5)
    rows = (5, 4, 3, 2) if pile < 2 else (5, 4, 3)
    for row, n in enumerate(rows):
        for i in range(n):
            x = 2986.6 + (i + row * 0.5) * 0.70; z = 0.5 + 0.34 + row * 0.60
            cyl(bm, (x, yc - 9.33, z), (x, yc + 9.33, z), 4 / 12, 12)
            for e in (-9.33, 9.33):        # socket flanges at both ends
                cyl(bm, (x, yc + e - 0.06 * (1 if e > 0 else -1), z), (x, yc + e, z), 5.2 / 12, 12)
obj("CP011C_COLUMNS", bm, IRON, {"part_kind": "stock_column"})

# ---------------- timber bay: partition, racks, gutters, benches ----------------
bm = bmesh.new()
for x0, x1 in ((2984.5, 2995.5), (3004.5, 3015.5)):        # 4 ft board partition with a central gap
    box(bm, x0, x1, 86.8, 87.2, 0, 4.2)
    for x in (x0, x1): box(bm, x - 0.2, x + 0.2, 86.6, 87.4, 0, 4.6)
obj("CP011C_TIMBER_PARTITION", bm, WAG, {"part_kind": "partition"})
bm_r = bmesh.new(); bm_t = bmesh.new()
for xs in ((2985.0, 2993.5), (3006.5, 3015.0)):             # racks: uprights + three shelves of sash-bar bundles
    for y in (94, 104, 114, 124):
        for x in xs: box(bm_r, x - 0.25, x + 0.25, y - 0.25, y + 0.25, 0, 7.5)
    for z in (1.0, 3.3, 5.6):
        box(bm_r, xs[0], xs[1], 93.6, 124.4, z - 0.15, z)
        for i in range(5):
            xb = xs[0] + 0.5 + i * (xs[1] - xs[0] - 1.0) / 4.0
            for j in range(3):
                box(bm_t, xb - 0.38 + j * 0.0, xb + 0.38, 94.0, 124.0, z + j * 0.5, z + j * 0.5 + 0.45)
bm_g = bmesh.new()
for k in range(7):                                         # Paxton gutters (24 ft) stacked by the east rack
    for i in range(2): box(bm_g, 3017.0 + i * 1.05, 3017.9 + i * 1.05, 96, 120, k * 0.62, k * 0.62 + 0.55)
bm_s = bmesh.new()
BENCH = []
for bx, by in ((2997.0, 104.0), (3003.0, 112.0)):         # trestle benches along the aisle, 16 ft
    for yy in (by - 6.5, by + 6.5):
        for dx in (-1.1, 1.1): box(bm_r, bx + dx - 0.15, bx + dx + 0.15, yy - 0.15, yy + 0.15, 0, 2.7)
        box(bm_r, bx - 1.3, bx + 1.3, yy - 0.15, yy + 0.15, 1.2, 1.45)
    box(bm_r, bx - 1.2, bx + 1.2, by - 8, by + 8, 2.7, 3.0)
    for i in range(3): box(bm_t, bx - 0.9 + i * 0.6, bx - 0.55 + i * 0.6, by - 7.5, by + 7.5, 3.0, 3.18)
    for k in range(18):                                    # curled shavings on the floor under the bench
        a = k * 2.399; r = 0.6 + (k % 5) * 0.45
        cx, cy = bx + 1.8 * math.cos(a) * 0.8, by + r * 2.5 * math.sin(a)
        bmesh.ops.create_icosphere(bm_s, subdivisions=1, radius=0.22 * F, matrix=Matrix.Translation(Vector((cx, cy, 0.05)) * F) @ Matrix.Diagonal((1.6, 1.0, 0.35, 1)))
    BENCH.append((bx, by))
obj("CP011C_RACKS", bm_r, BEARER, {"part_kind": "rack"})
obj("CP011C_SASHBARS", bm_t, WOOD, {"part_kind": "stock_timber"}); obj("CP011C_GUTTERS", bm_g, WOOD, {"part_kind": "stock_gutter"})
obj("CP011C_SHAVINGS", bm_s, SHAV, {"part_kind": "shavings"})

# ---------------- handling: trolley with one column, barrow ----------------
bm = bmesh.new(); bmw = bmesh.new(); TX, TY = 2999.5, 48.0
box(bm, TX - 1.4, TX + 1.4, TY - 6, TY + 6, 1.0, 1.35)
for yy in (TY - 4.5, TY + 4.5):
    for dx in (-1.55, 1.55): cyl(bmw, (TX + dx - 0.12, yy, 0.85), (TX + dx + 0.12, yy, 0.85), 0.85, 14)
box(bm, TX - 0.15, TX + 0.15, TY - 9.5, TY - 6, 1.1, 1.3)                         # draw bar
obj("CP011C_TROLLEY", bm, WAG, {"part_kind": "trolley"}); obj("CP011C_TROLLEY_WHEELS", bmw, IRON, {"part_kind": "trolley_wheel"})
bm = bmesh.new(); cyl(bm, (TX, TY - 8.5, 1.7), (TX, TY + 10.0, 1.7), 4 / 12, 12); obj("CP011C_TROLLEY_COLUMN", bm, IRON, {"part_kind": "stock_column"})
obj("CP011C_BEARERS", bm_bear, BEARER, {"part_kind": "bearer"})
if "barrow" in bpy.data.meshes:
    b = bpy.data.objects.new("CP011C_BARROW", bpy.data.meshes["barrow"]); coll.objects.link(b)
    b.location = Vector((3004.2, 18.0, 0)) * F; b.rotation_euler.z = math.radians(80); b[TAG] = True

# ---------------- people (people_lib, explicit poses, dark fustian) ----------------
sys.path.insert(0, "/workspace/crystal-palace-survey/people"); import people_lib as PL
FUSTIAN = {"blue": (0.030, 0.042, 0.075), "grey": (0.050, 0.050, 0.048), "drab": (0.040, 0.044, 0.034)}
FM = {}
for k, c in FUSTIAN.items():
    m = bpy.data.materials.get(f"CP011C_fustian_{k}") or bpy.data.materials.new(f"CP011C_fustian_{k}")
    m.use_nodes = True; b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*c, 1.0); b.inputs["Roughness"].default_value = 0.95
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.2
    if "Sheen Weight" in b.inputs: b.inputs["Sheen Weight"].default_value = 0.0
    m.diffuse_color = (*c, 1.0); FM[k] = m
for n in ("KWORKER_024_CP011", "KWORKER_025_CP011", "KWORKER_026_CP011"):
    hide_for_cp011(bpy.data.objects[n], "replaced by people_lib figure")
# name, role, pose, x, y, face_deg (0 = front toward -Y = toward the camera)
CAST = [("CP011C_P01_haul", "1850s_workman", "hauling", 2999.0, 38.6, 0),
        ("CP011C_P02_haul", "1850s_workman", "hauling", 3000.6, 39.4, 10),
        ("CP011C_P03_girders", "1850s_workman", "working", 3005.2, 30.0, 270),
        ("CP011C_P04_clerk", "1850s_gentleman", "standing", 3002.8, 12.0, 300),
        ("CP011C_P05_columns", "1850s_workman", "working", 2994.6, 62.0, 90),
        ("CP011C_P06_bench", "1850s_workman", "working", 2999.0, 102.0, 95),
        ("CP011C_P07_bench", "1850s_workman", "working", 3001.0, 114.0, 265),
        ("CP011C_P08_rack", "1850s_workman", "standing", 3005.4, 120.0, 230),
        ("CP011C_P09_door", "1850s_workman", "walking", 2998.0, 150.0, 0)]
rows = []
for i, (nm, role, pose, x, y, face) in enumerate(CAST):
    seed = int(hashlib.md5(nm.encode()).hexdigest()[:6], 16)
    tmp = PL._build_person(role, pose, "hero" if y < 70 else "mid", seed)
    o = bpy.data.objects.new(nm, tmp.data); bpy.data.objects.remove(tmp, do_unlink=True); coll.objects.link(o)
    o.location = Vector((x, y, 0)) * F; o.rotation_euler.z = math.radians(face); o["cpl_people"] = PL.PEOPLE_TAG
    o["part_kind"] = "person"
    if role == "1850s_workman":
        k = list(FUSTIAN)[i % 3]
        for si, m in enumerate(o.data.materials):
            if m and (m.name.startswith("CPL3_smock") or m.name.startswith("CPL3_waist")): o.data.materials[si] = FM[k]
    else: k = "-"
    o[TAG] = f"people_lib {PL.PEOPLE_VERSION} {role} {pose} fustian {k}"; rows.append((nm, role, pose, k))
# clerk's tally board
bm = bmesh.new(); box(bm, 3003.3, 3004.1, 11.3, 11.4, 3.3, 4.3); obj("CP011C_TALLY_BOARD", bm, WAG, {"part_kind": "prop"})
for r in rows: print("PERSON", *r)

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if LIVE:
    for o in coll.all_objects:
        o["only_cams"] = SID; o.hide_render = True
        if o.get("cpl_people"):    # keep other shots' render-time people swap (people_lib 3.2) from adopting these
            o["cp011_people"] = o["cpl_people"]; del o["cpl_people"]; o["part_kind"] = "cp011_fixed_figure"
    # people_lib caches by datablock name (mesh CPL3_<role>_<pose>_<lod>_<n>, materials CPL3_*): the pre-yard c07 has
    # none, so rename ours, otherwise other shots' render-time swap (v3.2) would reuse these v3.4 meshes / reset colours.
    for db in (bpy.data.meshes, bpy.data.materials):
        for d in list(db):
            if d.name.startswith("CPL3_"): d.name = "CP011P_" + d.name[5:]
    ok = in_place(); print("CP011_YARD_IN_PLACE", ok)
    if not ok: sys.exit(3)
    out = arg("--out") or bpy.data.filepath
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True); print("CP011_YARD saved", out)
else:
    out = arg("--out") or os.path.join(here, "rounds", "candidates", "c07_cp011yard.blend")
    bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True); print("SAVED", out)
