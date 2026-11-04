"""2026-11-03 CANDIDATE (Grok Bot executor, no verdict, NOT live; DEPARTURES CN51): CP011_yard "yard2" pass.
Base: live rounds/c07.blend (CN47 yard + CN49 one-tier lattice + CN50 pile KEEP, md5 6920b1e9..., construction 49ae701).
Read only; saves a sibling rounds/candidates/c07_cp011yard2.blend (live c07 is never written). Everything added is a CP011C_*
object in CP011_YARD_CAND with only_cams="CP011_yard"; material changes are object-level links on CP011C_* objects only
(CP011C_brick_sooted / CP011C_fence_tarred are left as they are; shared KYARD_SHED / GT_* materials are NOT edited), so no
other c07 shot can change. The KEEP lattice, near pile and timber bay are untouched.
  1. smoke on a visible chimney (CP011 'next' 2): the CN47 chimneys' tops are above the frame / behind the shed roof from
     both cameras, and the only open sky is west (left) above the fence. A boiler house (brick, slate gable) with a square
     tapered brick boiler chimney (7 ft -> 5 ft, corbelled cap, mouth at 55.5 ft) stands beyond the west fence at about
     (2915, 216) ft, ~18-20 deg left of both cameras, and a soft coal-smoke plume (overlapping volume blobs with radial
     falloff and shared world-space noise, so it reads as one plume) rises out of its mouth and leans west on the wind.
  2. west fence (next 3): CP011C_FENCE_WEST (a 1.2 ft slab) is retagged only_cams="NONE_CN51" and replaced by a
     close-boarded tarred fence: 6 in boards with 1/2 in gaps and ragged tops, two arris rails and a gravel board on the yard
     side, posts at 8 ft centres; per-board tone (face attribute board_rand) + vertical weathering streaks.
  3. brick coursing (next 4): new CP011C_brick_coursed on world Position (9 in x 3 in courses, stretcher bond, recessed
     mortar bump, per-brick tone + soot patches), object-level link on the works ranges, chimneys and the new boiler house.
  4. shed roof underside (next 5): camera-scoped deal boarding under the KYARD_SHED roof slab (boards along the shed) on
     3 x 6 in joists at 2 ft centres, plus a weak upward-facing warm area light at 3 ft (stand-in for cinder-yard bounce;
     camera-invisible).
blender -b rounds/c07.blend -P scripts/cand_cp011_yard2_20261103.py -- [--out PATH] [--no-smoke] [--no-fence] [--no-brick]
        [--no-roof] [--bounce W]
  (candidate mode needs the PRE-yard2 live c07 pinned at construction commit 49ae701; see render_cp011_yard2.sh)
blender -b rounds/c07.blend -P scripts/cand_cp011_yard2_20261103.py -- --live [--out PATH]
  KEEP 2026-11-03 (parent viewed the pairs; DEPARTURES CN51): applies exactly the full candidate build (smoke + fence +
  brick + roof, default bounce 1700 W and smoke density 7; no flags) to the live c07 IN PLACE. Camera-scoped as above: every
  added object is CP011C_* only_cams="CP011_yard"; CP011C_FENCE_WEST is retagged only_cams="NONE_CN51" (kept, never renders).
  Marks CP011_YARD_CAND["cp011_yard2"] = "CN51 KEEP". Idempotent: if the marker exists it only checks (never re-applies).
  --live refuses --no-smoke / --no-fence / --no-brick / --no-roof / --bounce / --smoke-density. Prints CP011_YARD2_IN_PLACE.
  -- --check: read-only check, prints CP011_YARD2_IN_PLACE and exits (never saves)."""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector, Matrix
F = 0.3048
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
TAG = "cand_cp011yard2_20261103"; SID = "CP011_yard"
coll = bpy.data.collections["CP011_YARD_CAND"]
assert coll.get("cp011_pile") == "CN50 KEEP", "base must be the live c07 with the CN50 pile KEEP"
LIVE = "--live" in argv; MARK = "CN51 KEEP"
BRICK_OBJS = ("CP011C_WORKS_EAST_BRICK", "CP011C_WORKS_NORTH_BRICK", "CP011C_CHIMNEY_N", "CP011C_CHIMNEY_E")
def in_place():
    ob = bpy.data.objects
    new = ["CP011C_BOILER_BRICK", "CP011C_BOILER_ROOF", "CP011C_BOILER_FLUE", "CP011C_FENCE_WEST2", "CP011C_SHED_CEILING",
           "CP011C_SHED_BOUNCE"] + [f"CP011C_BOILER_SMOKE_{i:02d}" for i in range(44)]
    retag = {"CP011C_TIMBER_FLOOR": "NONE_CN50", "CP011C_FENCE_WEST": "NONE_CN51"}
    return (coll.get("cp011_yard2") == MARK and all(n in ob and ob[n].name in coll.all_objects for n in new)
            and not any(o.name.startswith("CP011C_BOILER_SMOKE_") and o.name not in new for o in ob)
            and ob["CP011C_FENCE_WEST"].get("only_cams") == "NONE_CN51"
            and all(s.link == 'OBJECT' and s.material.name == "CP011C_brick_coursed" for n in BRICK_OBJS for s in ob[n].material_slots)
            and all(o.hide_render and o.get("only_cams") == retag.get(o.name, SID) for o in coll.all_objects))
if "--check" in argv:   # read-only
    ok = in_place(); print("CP011_YARD2_IN_PLACE", ok); sys.exit(0 if ok else 3)
if coll.get("cp011_yard2"):
    if not LIVE: raise SystemExit("base already carries yard2; build candidates from the pre-yard2 c07 at 49ae701")
    ok = in_place(); print("CP011_YARD2 already applied (idempotent, not re-saved)"); print("CP011_YARD2_IN_PLACE", ok)
    sys.exit(0 if ok else 3)
if LIVE: assert not any(f in argv for f in ("--no-smoke", "--no-fence", "--no-brick", "--no-roof", "--bounce", "--smoke-density")), \
    "--live applies only the full KEEP build"
rng = random.Random(51)
def new_obj(name, data, kind):
    o = bpy.data.objects.new(name, data); coll.objects.link(o)
    o["only_cams"] = SID; o.hide_render = True; o[TAG] = True; o["part_kind"] = kind; return o
def box(bm, x0, x1, y0, y1, z0, z1, mi=0):
    r = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(((x0 + x1) / 2 * F, (y0 + y1) / 2 * F, (z0 + z1) / 2 * F)) @
                              Matrix.Diagonal((abs(x1 - x0) * F, abs(y1 - y0) * F, abs(z1 - z0) * F, 1)))
    fs = {f for v in r["verts"] for f in v.link_faces}
    for f in fs: f.material_index = mi
    return fs
def mesh(name, bm, mats):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in (mats if isinstance(mats, (list, tuple)) else [mats]): me.materials.append(m)
    return me
def N(nt, t, **kw):
    n = nt.nodes.new(t)
    for k, v in kw.items():
        if k == "op": n.operation = v
        elif k == "dt": n.data_type = v
        else: n.inputs[k].default_value = v
    return n
L = lambda nt, a, b: nt.links.new(a, b)

# ---------------- 3. brick coursing ----------------
def brick_mat():
    m = bpy.data.materials.new("CP011C_brick_coursed"); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    geo = N(nt, "ShaderNodeNewGeometry"); sep = N(nt, "ShaderNodeSeparateXYZ"); L(nt, geo.outputs["Position"], sep.inputs[0])
    add = N(nt, "ShaderNodeMath", op="ADD"); L(nt, sep.outputs[0], add.inputs[0]); L(nt, sep.outputs[1], add.inputs[1])
    cmb = N(nt, "ShaderNodeCombineXYZ"); L(nt, add.outputs[0], cmb.inputs[0]); L(nt, sep.outputs[2], cmb.inputs[1])
    bt = N(nt, "ShaderNodeTexBrick", Scale=1.0, **{"Mortar Size": 0.0065, "Mortar Smooth": 0.15, "Bias": 0.0,
           "Brick Width": 0.2286, "Row Height": 0.0762, "Color1": (0.27, 0.092, 0.058, 1), "Color2": (0.13, 0.056, 0.042, 1),
           "Mortar": (0.24, 0.22, 0.19, 1)})
    bt.offset = 0.5; bt.squash = 1.0; L(nt, cmb.outputs[0], bt.inputs["Vector"])
    nz = N(nt, "ShaderNodeTexNoise", Scale=0.18, Detail=4.0, Roughness=0.6); L(nt, geo.outputs["Position"], nz.inputs["Vector"])
    mr = N(nt, "ShaderNodeMapRange", **{"From Min": 0.38, "From Max": 0.66, "To Min": 0.0, "To Max": 0.7}); L(nt, nz.outputs["Fac"], mr.inputs["Value"])
    mix = N(nt, "ShaderNodeMix", dt="RGBA"); mix.inputs[7].default_value = (0.075, 0.05, 0.04, 1)
    L(nt, mr.outputs[0], mix.inputs[0]); L(nt, bt.outputs["Color"], mix.inputs[6]); L(nt, mix.outputs[2], b.inputs["Base Color"])
    bump = N(nt, "ShaderNodeBump", Strength=0.5, Distance=0.006); inv = N(nt, "ShaderNodeMath", op="SUBTRACT"); inv.inputs[0].default_value = 1.0
    L(nt, bt.outputs["Fac"], inv.inputs[1]); L(nt, inv.outputs[0], bump.inputs["Height"]); L(nt, bump.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.9
    return m
BRICK = brick_mat() if "--no-brick" not in argv else bpy.data.materials["CP011C_brick_sooted"]
if "--no-brick" not in argv:
    for n in BRICK_OBJS:
        o = bpy.data.objects[n]
        for s in o.material_slots: s.link = 'OBJECT'; s.material = BRICK

# ---------------- 1. boiler house + chimney + smoke ----------------
if "--no-smoke" not in argv:
    SLATE = bpy.data.materials["CP011C_slate"]; SOOT = bpy.data.materials.new("CP011C_flue_soot"); SOOT.use_nodes = True
    SOOT.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.012, 0.011, 0.01, 1)
    CX, CY, H, B0, B1 = 2915.0, 216.0, 54.0, 7.0, 5.0
    # boiler house: brick walls x 2898-2932, y 190-212, eaves 15 ft; slate gable roof, ridge along x at 21 ft
    bm = bmesh.new(); box(bm, 2898, 2932, 190, 212, 0, 15)
    # chimney: tapered square shaft + corbelled cap (two oversailing courses)
    r = bmesh.ops.create_cone(bm, cap_ends=True, segments=4, radius1=B0 / 2 * F * math.sqrt(2), radius2=B1 / 2 * F * math.sqrt(2),
                              depth=H * F, matrix=Matrix.Translation((CX * F, CY * F, H / 2 * F)) @ Matrix.Rotation(math.pi / 4, 4, 'Z'))
    box(bm, CX - 2.75, CX + 2.75, CY - 2.75, CY + 2.75, H - 6.0, H, 1)            # soot-blackened top of the shaft
    box(bm, CX - 3.0, CX + 3.0, CY - 3.0, CY + 3.0, H, H + 0.75, 1); box(bm, CX - 3.25, CX + 3.25, CY - 3.25, CY + 3.25, H + 0.75, H + 1.5, 1)
    new_obj("CP011C_BOILER_BRICK", mesh("CP011C_BOILER_BRICK", bm, [BRICK, bpy.data.materials["CP011C_brick_sooted"]]), "works_building")
    bm = bmesh.new()
    vs = [bm.verts.new(Vector(p) * F) for p in ((2897, 189, 14.6), (2933, 189, 14.6), (2933, 201, 21), (2897, 201, 21),
                                              (2897, 213, 14.6), (2933, 213, 14.6))]
    bm.faces.new((vs[0], vs[1], vs[2], vs[3])); bm.faces.new((vs[3], vs[2], vs[5], vs[4]))
    bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.3 * F)
    g = [bm.verts.new(Vector(p) * F) for p in ((2898.05, 190, 15), (2898.05, 212, 15), (2898.05, 201, 20.7))]; bm.faces.new(g)
    g = [bm.verts.new(Vector(p) * F) for p in ((2931.95, 190, 15), (2931.95, 212, 15), (2931.95, 201, 20.7))]; bm.faces.new(g)
    me = mesh("CP011C_BOILER_ROOF", bm, [SLATE, BRICK])
    for p in me.polygons: p.material_index = 1 if len(p.vertices) == 3 else 0
    new_obj("CP011C_BOILER_ROOF", me, "works_building")
    bm = bmesh.new(); box(bm, CX - 2.0, CX + 2.0, CY - 2.0, CY + 2.0, H + 1.5, H + 1.53)
    new_obj("CP011C_BOILER_FLUE", mesh("CP011C_BOILER_FLUE", bm, SOOT), "works_building")
    # smoke material: density = object colour R * radial falloff (unit sphere, object coords) * shared world noise
    sm = bpy.data.materials.new("CP011C_coal_smoke"); sm.use_nodes = True; nt = sm.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"]); out = nt.nodes["Material Output"]
    pv = N(nt, "ShaderNodeVolumePrincipled", Color=(0.56, 0.54, 0.51, 1), Anisotropy=0.4)
    L(nt, pv.outputs[0], out.inputs["Volume"])
    tc = N(nt, "ShaderNodeTexCoord"); ln = N(nt, "ShaderNodeVectorMath", op="LENGTH"); L(nt, tc.outputs["Object"], ln.inputs[0])
    sq = N(nt, "ShaderNodeMath", op="POWER"); sq.inputs[1].default_value = 2.0; L(nt, ln.outputs["Value"], sq.inputs[0])
    om = N(nt, "ShaderNodeMath", op="SUBTRACT"); om.use_clamp = True; om.inputs[0].default_value = 1.0; L(nt, sq.outputs[0], om.inputs[1])
    fo = N(nt, "ShaderNodeMath", op="POWER"); fo.inputs[1].default_value = 3.0; L(nt, om.outputs[0], fo.inputs[0])
    geo = N(nt, "ShaderNodeNewGeometry")
    nz = N(nt, "ShaderNodeTexNoise", Scale=0.16, Detail=6.0, Roughness=0.62); L(nt, geo.outputs["Position"], nz.inputs["Vector"])
    mr = N(nt, "ShaderNodeMapRange", **{"From Min": 0.30, "From Max": 0.70, "To Min": 0.0, "To Max": 1.2}); L(nt, nz.outputs["Fac"], mr.inputs["Value"])
    oi = N(nt, "ShaderNodeObjectInfo"); sc_ = N(nt, "ShaderNodeSeparateColor"); L(nt, oi.outputs["Color"], sc_.inputs[0])
    m1 = N(nt, "ShaderNodeMath", op="MULTIPLY"); L(nt, fo.outputs[0], m1.inputs[0]); L(nt, mr.outputs[0], m1.inputs[1])
    m2 = N(nt, "ShaderNodeMath", op="MULTIPLY"); L(nt, m1.outputs[0], m2.inputs[0]); L(nt, sc_.outputs[0], m2.inputs[1])
    L(nt, m2.outputs[0], pv.inputs["Density"])
    sbm = bmesh.new(); bmesh.ops.create_icosphere(sbm, subdivisions=2, radius=1.0); sme = mesh("CP011C_SMOKE_BLOB", sbm, sm)
    D0 = float(arg("--smoke-density", "7"))
    wind = Vector((-0.6, 1.0, 0.0)).normalized(); M = Vector((CX, CY, H + 1.5)); n = 44
    for i in range(n):
        s = i / (n - 1)
        p = M + wind * (110.0 * s ** 1.15) + Vector((0, 0, 11.0 * (1 - math.exp(-5.0 * s)) + 4.0 * s))
        rad = 1.8 + 13.0 * s ** 0.8
        p.z += rad * 0.35 if i == 0 else 0.0
        dens = D0 * (1.8 / rad) ** 0.95 * (1.0 - max(0.0, (s - 0.7) / 0.3)) ** 2 * (0.5 if i == 0 else 1.0)
        o = new_obj(f"CP011C_BOILER_SMOKE_{i:02d}", sme, "smoke")
        o.location = p * F; o.scale = (rad * F * 1.25, rad * F, rad * F * 0.9)
        o.rotation_euler = (0, -math.atan2(11.0 * 5 * math.exp(-5 * s) + 4.0, 110.0 * 1.15 * max(s, 0.02) ** 0.15), math.atan2(wind.y, wind.x))
        o.color = (dens, 0, 0, 1); o.visible_shadow = True
    print("SMOKE blobs", n, "mouth ft", tuple(round(c, 1) for c in M))

# ---------------- 2. west fence ----------------
if "--no-fence" not in argv:
    old = bpy.data.objects["CP011C_FENCE_WEST"]; old["only_cams"] = "NONE_CN51"; old["cn51"] = "replaced by CP011C_FENCE_WEST2"
    fm = bpy.data.materials.new("CP011C_fence_boards"); fm.use_nodes = True; nt = fm.node_tree; b = nt.nodes["Principled BSDF"]
    at = N(nt, "ShaderNodeAttribute"); at.attribute_name = "board_rand"; at.attribute_type = 'GEOMETRY'
    cr = nt.nodes.new("ShaderNodeValToRGB"); e = cr.color_ramp.elements
    e[0].position = 0.0; e[0].color = (0.022, 0.019, 0.016, 1); e[1].position = 1.0; e[1].color = (0.125, 0.105, 0.085, 1)
    mid = e.new(0.55); mid.color = (0.060, 0.050, 0.040, 1)
    L(nt, at.outputs["Fac"], cr.inputs["Fac"])
    geo = N(nt, "ShaderNodeNewGeometry"); mp = N(nt, "ShaderNodeMapping"); mp.inputs["Scale"].default_value = (6.0, 6.0, 0.35)
    L(nt, geo.outputs["Position"], mp.inputs["Vector"])
    nz = N(nt, "ShaderNodeTexNoise", Scale=2.5, Detail=6.0, Roughness=0.65); L(nt, mp.outputs["Vector"], nz.inputs["Vector"])
    mr = N(nt, "ShaderNodeMapRange", **{"From Min": 0.3, "From Max": 0.7, "To Min": 0.7, "To Max": 1.35}); L(nt, nz.outputs["Fac"], mr.inputs["Value"])
    mul = N(nt, "ShaderNodeMix", dt="RGBA"); mul.blend_type = 'MULTIPLY'; mul.inputs[0].default_value = 1.0
    cm = N(nt, "ShaderNodeCombineColor"); L(nt, mr.outputs[0], cm.inputs[0]); L(nt, mr.outputs[0], cm.inputs[1]); L(nt, mr.outputs[0], cm.inputs[2])
    L(nt, cr.outputs["Color"], mul.inputs[6]); L(nt, cm.outputs[0], mul.inputs[7]); L(nt, mul.outputs[2], b.inputs["Base Color"])
    bump = N(nt, "ShaderNodeBump", Strength=0.35, Distance=0.004); L(nt, nz.outputs["Fac"], bump.inputs["Height"]); L(nt, bump.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.88
    bm = bmesh.new(); fr = bm.faces.layers.float.new("board_rand")
    def tag(fs, v):
        for f in fs: f[fr] = v
    Y0, Y1 = -130.0, 176.0
    y = Y0
    while y < Y1 - 0.05:
        w = 0.5; top = 8.35 + rng.uniform(-0.12, 0.12); dx = rng.uniform(-0.012, 0.012)
        tag(box(bm, 2959.70 + dx, 2959.77 + dx, y, min(y + w, Y1), 0.0, top), rng.random() ** 0.8)
        y += w + 0.04
    for z0, z1 in ((1.15, 1.48), (6.75, 7.08)):                                     # arris rails (yard side)
        tag(box(bm, 2959.77, 2960.05, Y0, Y1, z0, z1), 0.55)
    tag(box(bm, 2959.77, 2959.90, Y0, Y1, 0.0, 0.55), 0.25)                        # gravel board
    yp = Y0
    while yp <= Y1 + 0.01:                                                          # posts at 8 ft centres
        tag(box(bm, 2959.77, 2960.19, yp - 0.21, yp + 0.21, 0.0, 8.75), 0.1 + 0.3 * rng.random()); yp += 8.0
    new_obj("CP011C_FENCE_WEST2", mesh("CP011C_FENCE_WEST2", bm, fm), "fence")

# ---------------- 4. shed roof underside ----------------
if "--no-roof" not in argv:
    cm = bpy.data.materials.new("CP011C_shed_boarding"); cm.use_nodes = True; nt = cm.node_tree; b = nt.nodes["Principled BSDF"]
    geo = N(nt, "ShaderNodeNewGeometry"); sep = N(nt, "ShaderNodeSeparateXYZ"); L(nt, geo.outputs["Position"], sep.inputs[0])
    cmb = N(nt, "ShaderNodeCombineXYZ"); L(nt, sep.outputs[1], cmb.inputs[0]); L(nt, sep.outputs[0], cmb.inputs[1])
    bt = N(nt, "ShaderNodeTexBrick", Scale=1.0, **{"Mortar Size": 0.006, "Mortar Smooth": 0.1, "Brick Width": 12 * F,
           "Row Height": 0.75 * F, "Color1": (0.68, 0.58, 0.44, 1), "Color2": (0.57, 0.48, 0.36, 1), "Mortar": (0.08, 0.06, 0.05, 1)})
    bt.offset = 0.37; L(nt, cmb.outputs[0], bt.inputs["Vector"]); L(nt, bt.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.85
    jm = bpy.data.materials["CP011C_bearer_oak_weathered"]
    bm = bmesh.new(); box(bm, 2982.3, 3017.7, -81.7, 129.7, 18.55, 18.59, 0)
    yj = -80.0
    while yj <= 128.0:
        box(bm, 2982.3, 3017.7, yj - 0.125, yj + 0.125, 18.05, 18.55, 1); yj += 2.0
    for xp in (2991.0, 3009.0):                                                     # two binders under the joists
        box(bm, xp - 0.25, xp + 0.25, -81.7, 129.7, 17.6, 18.05, 1)
    new_obj("CP011C_SHED_CEILING", mesh("CP011C_SHED_CEILING", bm, [cm, jm]), "roof")
    W = float(arg("--bounce", "1700"))
    if W > 0:
        ld = bpy.data.lights.new("CP011C_SHED_BOUNCE", 'AREA'); ld.shape = 'RECTANGLE'; ld.size = 34 * F; ld.size_y = 205 * F
        ld.energy = W; ld.color = (1.0, 0.93, 0.84)
        lo = new_obj("CP011C_SHED_BOUNCE", ld, "light"); lo.location = (3000 * F, 24 * F, 3.0 * F); lo.rotation_euler = (math.pi, 0, 0)
        lo.visible_camera = False; lo.visible_glossy = False

for o in coll.all_objects: assert o.get("only_cams"), o.name
if LIVE:
    coll["cp011_yard2"] = MARK
    ok = in_place(); print("CP011_YARD2_IN_PLACE", ok)
    if not ok: sys.exit(3)
    out = arg("--out") or bpy.data.filepath
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True); print("CP011_YARD2 saved", out)
else:
    coll["cp011_yard2"] = "CN51 candidate"
    out = arg("--out") or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rounds", "candidates", "c07_cp011yard2.blend")
    assert os.path.abspath(out) != os.path.abspath(bpy.data.filepath), "never overwrite live c07"
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True); print("SAVED", out)
