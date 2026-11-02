"""2026-11-02 CANDIDATE (Grok Bot executor, not a verdict): CP012_bay 'One bay, then the next' (HP-PHASES + K-JOINT + PPL-1851).
Base: rounds/c07.blend (live CP012_bay_start, unchanged). Saves rounds/candidates/c07_cp012bay.blend, for CP012_bay ONLY
(never render other shots from it: it moves cameras, swaps people and animates the hoisted girder).
Why: in live c07 the hoisted 24 ft girder (KGIR_HOIST_X552_Y-180) is hidden behind the KSCAF_HEAD564 tower, so the beat
'a crew connects one supported girder between columns' does not read; people_lib's random pose gave a seated, lounging
workman in the foreground and pale smocks read as bare torsos; the haul horse is a white blob.
Changes (DEPARTURES CN45):
  * camera  : 28 mm, eye 5.25 ft, square-on to bay 540-564 (row y -180) from the south, so the girder, both column heads,
              the head scaffolds and the sheer legs read together; end = a sideways walk east, out of the lifting zone.
  * girder  : animated. frame 1 hanging, top 18.0 ft (4 ft 2 in below its seat); frame 96 seated, top 22 ft 2 in (K03 seat),
              sling slack. Lifting ropes rebuilt as two keyed sets (KROPES_CP012_LIFT_F001 / _SEATED); static guys and the
              fall to the snatch block are kept (KROPES_CP012_STATIC). The original KROPES is hidden in this blend.
  * people  : every figure in either camera frustum rebuilt with survey people_lib 1850s_workman (cap, smock, trousers,
              boots) with an explicit pose (no seated, no pointing), smocks/waist in dark matte fustian (as CP016 v3);
              render with --no-people so nothing is re-randomised.
  * horse   : the haul horse takes the existing bay coat mesh (horse_draught_bay) instead of the grey.
blender -b rounds/c07.blend -P scripts/cand_cp012_bay_20261102.py -- [--cam V] [--out PATH]"""
import bpy, bmesh, mathutils, math, os, sys, hashlib
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view
F = 0.3048
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
sc = bpy.context.scene
TAG = "cand_cp012bay_20261102"

# ---------------- cameras ----------------
CAMS = {   # (pos_ft, look_ft) start, end; lens 28
    "square": (((566.0, -221.0, 5.25), (550.0, -180.0, 15.5)), ((578.0, -219.0, 5.25), (556.0, -180.0, 15.0))),
    "square_back": (((568.0, -234.0, 5.25), (550.0, -180.0, 16.0)), ((582.0, -232.0, 5.25), (556.0, -180.0, 15.5))),
    "south": (((566.0, -240.0, 5.25), (552.0, -180.0, 16.5)), ((590.0, -238.0, 5.25), (556.0, -180.0, 16.5))),
    "near": (((552.0, -219.0, 5.25), (552.0, -180.0, 13.5)), ((574.0, -217.0, 5.25), (553.0, -180.0, 14.0))),
    "walk": (((549.0, -219.0, 5.25), (551.5, -180.0, 13.5)), ((566.0, -232.0, 5.25), (553.0, -180.0, 15.0))),
    "bay": (((550.0, -213.5, 5.25), (551.0, -180.0, 10.6)), ((571.0, -213.0, 5.25), (553.0, -180.0, 11.0))),
}
LENS = float(arg("--lens", "28"))
def aim(name, pos, look):
    ob = bpy.data.objects[name]; ob.location = Vector(pos) * F
    d = Vector(look) * F - ob.location
    ob.rotation_mode = 'XYZ'; ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); ob.data.lens = LENS
    ob[TAG] = f"cam {arg('--cam', 'square')}"
cv = CAMS[arg("--cam", "square")]
aim("CP012_bay_start", *cv[0]); aim("CP012_bay_end", *cv[1])
CAMOBS = [bpy.data.objects["CP012_bay_start"], bpy.data.objects["CP012_bay_end"]]

# ---------------- head scaffolds behind the girder ----------------
SCAF_DY = float(arg("--scaf-dy", "0"))      # +14: decks move from y -190..-184 (in front of the girder) to -176..-170 (behind it)
if SCAF_DY:
    for nm in ("KSCAF_HEAD540", "KSCAF_HEAD564"):
        o = bpy.data.objects[nm]; o.location.y += SCAF_DY * F; o[TAG] = f"moved y {SCAF_DY:+} ft (CN45)"
    for nm in ("KWORKER_008_CP012", "KWORKER_009_CP012"):
        o = bpy.data.objects[nm]; o.location.y += SCAF_DY * F; o.rotation_euler.z = math.radians(float(arg("--deck-face", "0")))

# shift whole objects: NAME=dx:dy (feet), e.g. the gate cart group out of the end frame
for spec in [s for s in (arg("--shift", "") or "").split(",") if s]:
    nm, v = spec.split("="); dx, dy = map(float, v.split(":"))
    o = bpy.data.objects[nm]; o.location.x += dx * F; o.location.y += dy * F; o[TAG + "_shift"] = v
# explicit placements: NAME=x:y:z:face_deg (feet; face 0 = people_lib front toward -Y, i.e. toward the south cameras)
for spec in [s for s in (arg("--move", "") or "").split(",") if s]:
    nm, v = spec.split("="); x, y, z, r = map(float, v.split(":"))
    o = bpy.data.objects[nm]; o.location = Vector((x, y, z)) * F; o.rotation_euler.z = math.radians(r); o[TAG + "_move"] = v

# ---------------- girder lift (animated) ----------------
ROPE = bpy.data.materials["GT_Rope"]
G = bpy.data.objects["KGIR_HOIST_X552_Y-180"]
Z0, Z1 = float(arg("--z0", "18.0")), 22.0 + 2.0 / 12.0           # girder top: hanging (frame 1) / seated on the connecting pieces (frame 96)
APEX = Vector((552.0, -180.0, 36.0))
def cyl(bm, a, b, r=0.6 * 0.0254, seg=6):
    a = Vector(a) * F; b = Vector(b) * F; d = b - a
    M = Matrix.Translation((a + b) / 2) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=d.length, matrix=M)
def rope_obj(name, segs):
    old = bpy.data.objects.get(name)
    if old: bpy.data.objects.remove(old, do_unlink=True)
    bm = bmesh.new()
    for a, b in segs: cyl(bm, a, b)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(ROPE)
    ob = bpy.data.objects.new(name, me); G.users_collection[0].objects.link(ob); ob["part_kind"] = "rope"; ob[TAG] = True
    return ob
bpy.data.objects["KROPES"].hide_render = True; bpy.data.objects["KROPES"].hide_viewport = True
rope_obj("KROPES_CP012_STATIC", [(tuple(APEX), (552.6, -195.0, 1.0))] + [(tuple(APEX), (gx, gy, 0.0)) for gx, gy in ((530, -236), (576, -126))])
TAGHAND = tuple(float(v) for v in arg("--tag-hand", "536:-196:3.6").split(":"))
def lift_set(top, slack):
    s = 2.0 if not slack else 0.6       # sling apex above the girder top; slack = hook lowered onto the seated girder
    hook = (552.0, -180.0, top + s)
    segs = [(tuple(APEX), hook), ((546.0, -180.0, top + 0.05), hook), ((558.0, -180.0, top + 0.05), hook)]
    if not slack: segs.append(((541.0, -180.0, top - 3.0), TAGHAND))   # tag line to the ground man (as c01)
    return segs
LA = rope_obj("KROPES_CP012_LIFT_F001", lift_set(Z0, False))
LB = rope_obj("KROPES_CP012_SEATED_F096", lift_set(Z1, True))
sc.frame_start, sc.frame_end = 1, 96
for fr, top, a_hide in ((1, Z0, False), (96, Z1, True)):
    G.location.z = top * F; G.keyframe_insert("location", index=2, frame=fr)
    LA.hide_render = a_hide; LA.keyframe_insert("hide_render", frame=fr)
    LB.hide_render = not a_hide; LB.keyframe_insert("hide_render", frame=fr)
for ob in (G, LA, LB):
    if ob.animation_data and ob.animation_data.action:
        for fc in getattr(ob.animation_data.action, "fcurves", []):
            for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT' if fc.data_path == "hide_render" else 'BEZIER'
G["state"] = "hoisting->seated (animated f1-f96, CN45)"; G[TAG] = f"top {Z0} ft f1 -> {Z1:.2f} ft f96"
sc.frame_set(1)

# ---------------- haul horse: bay coat ----------------
if "horse_draught_bay" in bpy.data.meshes:
    bpy.data.objects["KHORSE_haul"].data = bpy.data.meshes["horse_draught_bay"]; bpy.data.objects["KHORSE_haul"][TAG] = "bay coat"

# ---------------- people ----------------
sys.path.insert(0, "/workspace/crystal-palace-survey/people"); import people_lib as PL
FUSTIAN = {"blue": (0.030, 0.042, 0.075), "grey": (0.050, 0.050, 0.048), "drab": (0.040, 0.044, 0.034)}
FM = {}
for k, c in FUSTIAN.items():
    m = bpy.data.materials.get(f"CP012C_fustian_{k}") or bpy.data.materials.new(f"CP012C_fustian_{k}")
    m.use_nodes = True; b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*c, 1.0); b.inputs["Roughness"].default_value = 0.95
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.2
    if "Sheen Weight" in b.inputs: b.inputs["Sheen Weight"].default_value = 0.0
    m.diffuse_color = (*c, 1.0); FM[k] = m
POSEMAP = {"work": "working", "reach": "working", "kneel": "working", "stand": "standing"}
OVERRIDE = {n: p for n, p in (s.split("=") for s in (arg("--poses", "") or "").split(",") if s)}
HIDE = [s for s in (arg("--hide", "") or "").split(",") if s]
def in_view(ob, cam, margin=0.08):
    p = ob.matrix_world.translation
    for dz in (0.2, 1.0, 1.7):
        v = world_to_camera_view(sc, cam, p + Vector((0, 0, dz)))
        if v.z > 0 and -margin <= v.x <= 1 + margin and -margin <= v.y <= 1 + margin: return True
    return False
figs = [o for o in bpy.data.objects if PL._is_figure(o) and not o.hide_render]
n = 0; rows = []
for o in sorted(figs, key=lambda o: o.name):
    if not any(in_view(o, c) for c in CAMOBS): continue
    if o.name in HIDE:
        o.hide_render = True; o.hide_viewport = True; o[TAG] = "hidden"; rows.append((o.name, "HIDDEN")); continue
    d = min((o.matrix_world.translation - c.matrix_world.translation).length for c in CAMOBS) / F
    lod = "hero" if d < float(arg("--hero-ft", "60")) else "mid"
    pose = OVERRIDE.get(o.name) or POSEMAP.get(o.get("pose"), "standing")
    seed = int(hashlib.md5(o.name.encode()).hexdigest()[:6], 16)
    tmp = PL._build_person("1850s_workman", pose, lod, seed)
    mw = o.matrix_world.copy(); o.data = tmp.data; bpy.data.objects.remove(tmp, do_unlink=True)
    o.matrix_world = mw; o.scale = (1, 1, 1); o["cpl_people"] = PL.PEOPLE_TAG
    me = o.data; k = list(FUSTIAN)[n % 3]
    for si, m in enumerate(me.materials):
        if m and (m.name.startswith("CPL3_smock") or m.name.startswith("CPL3_waist")): me.materials[si] = FM[k]
    o[TAG] = f"people_lib {PL.PEOPLE_VERSION} 1850s_workman {pose} {lod} fustian {k}"; n += 1
    rows.append((o.name, f"{pose} {lod} {k} d={d:.0f}ft"))
for r in rows: print("PERSON", *r)
print("PEOPLE_SWAPPED", n)

# ---------------- framing report ----------------
KEY = {"girder_W": G.matrix_world @ Vector((-11.76 * F, 0, -1.5 * F)), "girder_E": G.matrix_world @ Vector((11.76 * F, 0, -1.5 * F)),
       "apex": APEX * F, "col540_top": Vector((540, -180, 22.2)) * F, "col564_top": Vector((564, -180, 22.2)) * F,
       "deck540": Vector((540, -187 + SCAF_DY, 16)) * F, "deck564": Vector((564, -187 + SCAF_DY, 16)) * F, "horse": bpy.data.objects["KHORSE_haul"].matrix_world.translation + Vector((0, 0, 1.2)),
       "snatch": Vector((552.6, -195, 1)) * F, "ginpole_head": Vector((566, -131, 50)) * F}
for fr, c in ((1, CAMOBS[0]), (96, CAMOBS[1])):
    sc.frame_set(fr)
    KEY["girder_W"] = G.matrix_world @ Vector((-11.76 * F, 0, -1.5 * F)); KEY["girder_E"] = G.matrix_world @ Vector((11.76 * F, 0, -1.5 * F))
    print("FRAME", c.name, " ".join(f"{k}=({v.x:.2f},{v.y:.2f})" for k, v in ((k, world_to_camera_view(sc, c, p)) for k, p in KEY.items())))
sc.frame_set(1)
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = arg("--out") or os.path.join(here, "rounds", "candidates", "c07_cp012bay.blend")
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True); print("SAVED", out)
