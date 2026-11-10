"""CP026 shilling-day entrance polish CANDIDATE (2026-11-10, DEPARTURES FT55-FT58). NOT live.
blender -b -P scripts/cand_cp026_shilling_20261110.py -- --src rounds/h03.blend --out rounds/candidates/h03_cp026shilling.blend
Loads live h03 (never saved over), changes the south-entrance apron of the hp51 state only, saves the candidate:
  FT55  shilling-day queue / lane / entering figures and the three constables -> modelled 1851 dress (cp026_figures.py,
        HBM CC0 heads; men in fustian, cord, smock-frocks and best black, women in print dresses, shawls and bonnets).
        Old figures kept but hide_render (so the people_lib v3.1 render-time swap of everything else keeps its LOD order).
        New objects are named C26Q_* / C26P_* with part_kind 'c26_figure' so the v3.1 swap does not touch them.
  FT56  apron: rolled Hyde Park gravel (buff hoggin, pebble bump, trodden darker band under the queue, wheel-worn edge).
  FT57  south end ground-tier boarding + the open south doors: vertical boards (9 in, estimated) with dark joints,
        weathered splash band at the foot, faint paint wear. Copy of GT_Boarding on the south-end objects only.
  FT59  south-entrance pedestals: the two plain 7 ft timber boxes (SOUTH_PEDESTALS, no source) -> Downes Plate XXVI
        octagonal cast-iron pedestals a5, 4 ft 9 in, round the feet of the entrance columns at x = +-12 ft."""
import bpy, sys, os, math, zlib
from mathutils import Vector, Matrix
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
SRC, OUT = arg("--src"), arg("--out")
bpy.ops.wm.open_mainfile(filepath=SRC)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cp026_figures as F
FT = 0.3048
TAG = "cp026_shilling_20261110"
sc = bpy.context.scene
info = {}

# ---------------- FT55 figures ----------------
col = bpy.data.collections.new("C26_FIGURES"); sc.collection.children.link(col)
def h(name): return zlib.crc32(name.encode())
MEN_N, WOM_N = 12, 10
men = [F.man(f"C26M_man_{i}", i, (1.66, 1.72, 1.69, 1.75, 1.63, 1.70)[i % 6], seed=100 + i, pose=("standing", "standing", "hips")[i % 3]) for i in range(MEN_N)]
wom = [F.woman(f"C26M_woman_{i}", i, (1.57, 1.61, 1.54, 1.63, 1.59)[i % 5], seed=200 + i) for i in range(WOM_N)]
boys = [F.man(f"C26M_boy_{i}", (0, 4, 7)[i], (1.28, 1.35, 1.22)[i], seed=300 + i) for i in range(3)]
girls = [F.woman(f"C26M_girl_{i}", (0, 4, 6)[i], (1.24, 1.32, 1.18)[i], seed=310 + i, child=True) for i in range(3)]
# constables 1851: Metropolitan Police blue tail-coat and top hat (FT55: frock-coat builder, interpretive)
F.MEN.append(("police", (0.025, 0.03, 0.075), (0.03, 0.03, 0.045), (0.025, 0.03, 0.075), (0.02, 0.02, 0.025), (0.012, 0.012, 0.014), "engineer", "top"))
police = [F.man(f"C26M_police_{i}", len(F.MEN) - 1, (1.78, 1.81, 1.79)[i], seed=400 + i) for i in range(3)]
LIB = {"man": men, "woman": wom, "boy": boys, "girl": girls}
for m in men + wom + boys + girls + police: m["c26_master"] = 1
n_rep = 0; hidden = []
def replace(ob, me_obj, prefix):
    global n_rep
    # people_lib v3.1 swaps any object whose upper-cased name contains "_POLICE" (etc.), so constables are renamed
    new = bpy.data.objects.new(prefix + ob.name.replace("POLICE", "CONSTABLE"), me_obj.data); new["c26_old"] = ob.name
    for md in me_obj.modifiers:
        nm = new.modifiers.new(md.name, md.type); nm.levels = md.levels; nm.render_levels = md.render_levels
    col.objects.link(new)
    new.matrix_world = ob.matrix_world.copy()
    k = 0.97 + (h(ob.name) % 61) / 1000.0; new.scale = (k, k, k)
    new["part_kind"] = "c26_figure"; new[TAG] = f"replaces {ob.name}"; new["c26_role"] = me_obj["c26_role"]
    ob.hide_render = True; ob[TAG] = "hidden, replaced by " + new.name; hidden.append(ob.name); n_rep += 1
for ob in list(bpy.data.objects):
    if ob.type != "MESH" or ob.get("part_kind") != "figure": continue
    if ob.name.startswith(("QUEUE_", "ENTERING_")):
        kd = ob.get("person", "man"); pool = LIB.get(kd, men)
        replace(ob, pool[h(ob.name) % len(pool)], "C26Q_")
    elif ob.name.startswith("POLICE_"):
        replace(ob, police[int(ob.name[-1]) % 3], "C26P_")
info["figures_replaced"] = n_rep

# ---------------- shader helpers ----------------
def N(nt, t, **kw):
    n = nt.nodes.new(t)
    for k_, v in kw.items(): n.inputs[k_].default_value = v
    return n
def ramp(nt, fac, stops):
    r = nt.nodes.new("ShaderNodeValToRGB"); e = r.color_ramp
    e.elements[0].position, e.elements[0].color = stops[0][0], (*stops[0][1], 1)
    e.elements[1].position, e.elements[1].color = stops[-1][0], (*stops[-1][1], 1)
    for p, c in stops[1:-1]:
        el = e.elements.new(p); el.color = (*c, 1)
    nt.links.new(fac, r.inputs[0]); return r
def mix(nt, a, b, fac, mode="MIX"):
    m = nt.nodes.new("ShaderNodeMix"); m.data_type = "RGBA"; m.blend_type = mode
    nt.links.new(fac, m.inputs["Factor"]); nt.links.new(a, m.inputs[6]); nt.links.new(b, m.inputs[7]); return m.outputs[2]
def val(nt, v):
    n = nt.nodes.new("ShaderNodeValue"); n.outputs[0].default_value = v; return n.outputs[0]
def rgb(nt, c):
    n = nt.nodes.new("ShaderNodeRGB"); n.outputs[0].default_value = (*c, 1); return n.outputs[0]
def newmat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    return m, nt, nt.nodes["Principled BSDF"]

# ---------------- FT56 gravel apron ----------------
m, nt, b = newmat("C26_gravel_hoggin")
tc = nt.nodes.new("ShaderNodeTexCoord"); pos = tc.outputs["Object"]
big = N(nt, "ShaderNodeTexNoise", Scale=0.35, Detail=4.0, Roughness=0.55); nt.links.new(pos, big.inputs["Vector"])
base = ramp(nt, big.outputs["Fac"], [(0.40, (0.29, 0.25, 0.19)), (0.50, (0.39, 0.34, 0.26)), (0.60, (0.50, 0.45, 0.36))])
mot = N(nt, "ShaderNodeTexNoise", Scale=4.0, Detail=6.0, Roughness=0.6); nt.links.new(pos, mot.inputs["Vector"])
motc = ramp(nt, mot.outputs["Fac"], [(0.38, (0.80, 0.80, 0.80)), (0.62, (1.12, 1.10, 1.06))])
base_m = mix(nt, base.outputs[0], motc.outputs[0], val(nt, 1.0), "MULTIPLY")
peb = N(nt, "ShaderNodeTexVoronoi", Scale=55.0, Randomness=1.0); nt.links.new(pos, peb.inputs["Vector"])
pebc = ramp(nt, peb.outputs["Color"], [(0.0, (0.80, 0.78, 0.74)), (0.5, (1.0, 0.98, 0.95)), (1.0, (1.12, 1.08, 1.0))])
c1 = mix(nt, base_m, pebc.outputs[0], val(nt, 0.7), "MULTIPLY")
# fine dark grit specks
spk = N(nt, "ShaderNodeTexVoronoi", Scale=180.0); nt.links.new(pos, spk.inputs["Vector"])
spr = ramp(nt, spk.outputs["Distance"], [(0.0, (0.0, 0.0, 0.0)), (0.12, (1.0, 1.0, 1.0))])
c2 = mix(nt, rgb(nt, (0.16, 0.14, 0.11)), c1, spr.outputs[0])
# trodden band under the queue (object x within ~8 ft of the queue line, darker, smoother, a little grey)
sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(pos, sep.inputs[0])
yy = nt.nodes.new("ShaderNodeMath"); yy.operation = "ADD"; nt.links.new(sep.outputs[1], yy.inputs[0]); yy.inputs[1].default_value = 250 * FT
qy = nt.nodes.new("ShaderNodeMath"); qy.operation = "MINIMUM"; nt.links.new(yy.outputs[0], qy.inputs[0]); qy.inputs[1].default_value = 0.0
shift = nt.nodes.new("ShaderNodeMath"); shift.operation = "MULTIPLY"; nt.links.new(qy.outputs[0], shift.inputs[0]); shift.inputs[1].default_value = -0.35
dx = nt.nodes.new("ShaderNodeMath"); dx.operation = "ADD"; nt.links.new(sep.outputs[0], dx.inputs[0]); nt.links.new(shift.outputs[0], dx.inputs[1])
ax = nt.nodes.new("ShaderNodeMath"); ax.operation = "ABSOLUTE"; nt.links.new(dx.outputs[0], ax.inputs[0])
wn = N(nt, "ShaderNodeTexNoise", Scale=1.6, Detail=3.0); nt.links.new(pos, wn.inputs["Vector"])
wd = nt.nodes.new("ShaderNodeMath"); wd.operation = "MULTIPLY_ADD"; nt.links.new(wn.outputs["Fac"], wd.inputs[0]); wd.inputs[1].default_value = 1.2; wd.inputs[2].default_value = 0.0
ax2 = nt.nodes.new("ShaderNodeMath"); ax2.operation = "ADD"; nt.links.new(ax.outputs[0], ax2.inputs[0]); nt.links.new(wd.outputs[0], ax2.inputs[1])
band = ramp(nt, ax2.outputs[0], [(0.0, (0.0, 0.0, 0.0)), (0.08, (0.0, 0.0, 0.0)), (0.11, (1.0, 1.0, 1.0))])   # ramp uses 0..1 of metres/30
bdiv = nt.nodes.new("ShaderNodeMath"); bdiv.operation = "DIVIDE"; nt.links.new(ax2.outputs[0], bdiv.inputs[0]); bdiv.inputs[1].default_value = 30.0
nt.links.new(bdiv.outputs[0], band.inputs[0])
worn = mix(nt, c2, rgb(nt, (0.70, 0.68, 0.66)), val(nt, 1.0), "MULTIPLY")
inv = nt.nodes.new("ShaderNodeInvert"); nt.links.new(band.outputs[0], inv.inputs["Color"])
cfin = mix(nt, c2, worn, inv.outputs[0])
nt.links.new(cfin, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.96
if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.2
bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.55; bp.inputs["Distance"].default_value = 0.012
nt.links.new(peb.outputs["Distance"], bp.inputs["Height"]); nt.links.new(bp.outputs[0], b.inputs["Normal"])
ap = bpy.data.objects["HP_APRON"]; ap.material_slots[0].link = "OBJECT"; ap.material_slots[0].material = m; ap[TAG] = "FT56 gravel"

# ---------------- FT57 south-end boarding ----------------
def boarding(name, base_c, board_w=9 * 0.0254, axis=0, joint=(0.30, 0.27, 0.22), splash=True, jw=0.035, tv=(0.90, 1.08)):
    m, nt, b = newmat(name)
    tc = nt.nodes.new("ShaderNodeTexCoord"); pos = tc.outputs["Object"]
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(pos, sep.inputs[0])
    d = nt.nodes.new("ShaderNodeMath"); d.operation = "DIVIDE"; nt.links.new(sep.outputs[axis], d.inputs[0]); d.inputs[1].default_value = board_w
    fr = nt.nodes.new("ShaderNodeMath"); fr.operation = "FRACT"; nt.links.new(d.outputs[0], fr.inputs[0])
    jr = ramp(nt, fr.outputs[0], [(0.0, (0, 0, 0)), (jw, (1, 1, 1)), (1.0 - jw * 0.9, (1, 1, 1)), (1.0, (0, 0, 0))])
    # per-board tone: board index -> white noise
    fl = nt.nodes.new("ShaderNodeMath"); fl.operation = "FLOOR"; nt.links.new(d.outputs[0], fl.inputs[0])
    wnz = nt.nodes.new("ShaderNodeTexWhiteNoise"); wnz.noise_dimensions = "1D"; nt.links.new(fl.outputs[0], wnz.inputs["W"])
    tone = ramp(nt, wnz.outputs["Value"], [(0.0, tuple(c * tv[0] for c in base_c)), (1.0, tuple(min(1, c * tv[1]) for c in base_c))])
    grain = N(nt, "ShaderNodeTexNoise", Scale=3.0, Detail=8.0); nt.links.new(pos, grain.inputs["Vector"])
    gm = nt.nodes.new("ShaderNodeMapping"); gm.inputs["Scale"].default_value = (12.0, 12.0, 0.6) if axis == 0 else (0.6, 12.0, 12.0)
    nt.links.new(pos, gm.inputs["Vector"]); nt.links.new(gm.outputs[0], grain.inputs["Vector"])
    gr = ramp(nt, grain.outputs["Fac"], [(0.35, (0.9, 0.9, 0.9)), (0.65, (1.05, 1.05, 1.05))])
    c = mix(nt, tone.outputs[0], gr.outputs[0], val(nt, 1.0), "MULTIPLY")
    c = mix(nt, mix(nt, c, rgb(nt, joint), val(nt, 1.0), "MULTIPLY"), c, jr.outputs[0])
    if splash:   # splash / boot dirt at the foot of the wall, fading out by ~1.2 ft, broken by noise
        zn = N(nt, "ShaderNodeTexNoise", Scale=2.5, Detail=5.0); nt.links.new(pos, zn.inputs["Vector"])
        zz = nt.nodes.new("ShaderNodeMath"); zz.operation = "MULTIPLY_ADD"; nt.links.new(zn.outputs["Fac"], zz.inputs[0]); zz.inputs[1].default_value = 0.25
        nt.links.new(sep.outputs[2], zz.inputs[2])
        sr = ramp(nt, zz.outputs[0], [(0.12, (0.62, 0.56, 0.48)), (0.48, (1, 1, 1))])
        c = mix(nt, c, sr.outputs[0], val(nt, 1.0), "MULTIPLY")
    nt.links.new(c, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.8
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.25
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.6; bp.inputs["Distance"].default_value = 0.004
    nt.links.new(jr.outputs[0], bp.inputs["Height"]); nt.links.new(bp.outputs[0], b.inputs["Normal"])
    return m
gb = bpy.data.materials["GT_Boarding"].node_tree.nodes["Principled BSDF"].inputs[0].default_value
mb = boarding("C26_south_boarding", tuple(gb[:3]), joint=(0.45, 0.42, 0.38))
nb = 0
for o in bpy.data.objects:
    if o.type == "MESH" and (o.name.startswith("WALLF_SE1_") or o.name == "SOUTH_DOORS_OPEN"):
        for sl in o.material_slots:
            if sl.material and sl.material.name == "GT_Boarding": sl.link = "OBJECT"; sl.material = mb; nb += 1
        o[TAG] = "FT57 boarding"
info["boarding_slots"] = nb
# (FT58 pay-box retint dropped 2026-11-10: the pay boxes stand inside the wall line at y=-195 ft and are not in frame;
#  the pale block in the live frame was SOUTH_PEDESTALS, see FT59)

# ---------------- FT59 south-entrance pedestals (Downes Plate XXVI figs 26-27, pp. 38-39; Plate IV) ----------------
# Live had SOUTH_PEDESTALS: two plain 5 x 5 x 7 ft timber boxes in front of the entrance (no source). Downes: the detached
# columns at the south end of the Transept stand on octagonal cast-iron pedestals a5, 4 ft 9 in high (printed), flats to the
# cardinal points. Plate-measured profile (via Muse's models/south-entrance-pedestals NOTES, read-only, dimensions only):
# plinth 5.4 in @20.2 in AF; cyma 6.0 in 14.0->11.9 in; shaft 40.9 in @11.9 in; torus 3.9 in @14.1 in; band 0.8 in @13.5 in;
# bell 3.8 in 13.5->11.9 in. Placed round the feet of the two entrance columns COL_END_X+-012_Y-204 that the camera sees.
import bmesh
IN = 0.0254
PROF = [(0.0, 20.2), (5.4, 20.2), (5.4, 14.0), (7.4, 12.6), (11.4, 11.9), (52.3, 11.9), (53.2, 13.2), (54.2, 14.1), (55.4, 13.9), (56.2, 13.0),
        (56.2, 13.5), (57.0, 13.5), (57.4, 13.5), (60.8, 11.9)]
def octo_ring(bm, z, af):
    r = af * IN / 2 / math.cos(math.pi / 8)
    return [bm.verts.new((r * math.cos(math.pi / 8 + k * math.pi / 4), r * math.sin(math.pi / 8 + k * math.pi / 4), z * IN)) for k in range(8)]
bm = bmesh.new(); rings = [octo_ring(bm, z, af) for z, af in PROF]
for A, Bv in zip(rings, rings[1:]):
    for k in range(8): bm.faces.new([A[k], A[(k + 1) % 8], Bv[(k + 1) % 8], Bv[k]])
bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
for k in range(8):   # countersunk screw heads on each facet: plinth, three down the shaft, torus
    a = k * math.pi / 4
    for z, af in ((2.7, 20.2), (20.0, 11.9), (32.0, 11.9), (44.0, 11.9)):
        d = af * IN / 2 + 0.002
        bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=4, radius=0.011, matrix=Matrix.Translation((d * math.cos(a), d * math.sin(a), z * IN)) @ Matrix.Diagonal((0.5 if abs(math.cos(a)) > 0.5 else 1, 1 if abs(math.cos(a)) > 0.5 else 0.5, 1, 1)))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
me = bpy.data.meshes.new("C26_pedestal_a5"); bm.to_mesh(me); bm.free()
iron = bpy.data.materials.get("GT_Iron"); me.materials.append(iron)
npd = 0
for cname in ("COL_END_X+012_Y-204", "COL_END_X-012_Y-204"):
    c = bpy.data.objects.get(cname)
    if not c: continue
    bb = [c.matrix_world @ Vector(v) for v in c.bound_box]
    cx = sum(v.x for v in bb) / 8; cy = sum(v.y for v in bb) / 8; z0 = min(v.z for v in bb)
    o = bpy.data.objects.new("C26_PEDESTAL_A5_" + cname[8:12], me); col.objects.link(o)
    o.location = (cx, cy, max(0.0, z0)); o["part_kind"] = "pedestal"; o[TAG] = "FT59 Downes pedestal a5 4 ft 9 in"; npd += 1
sp = bpy.data.objects.get("SOUTH_PEDESTALS")
if sp: sp.hide_render = True; sp[TAG] = "hidden: replaced by FT59 Downes pedestals"
info["pedestals"] = npd
sc["cp026_shilling"] = TAG
print("CP026_SHILLING", info, "hidden", len(hidden), flush=True)
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
# masters are not linked to the scene: keep their meshes alive via fake users
for m_ in men + wom + boys + girls + police: m_.data.use_fake_user = True
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
print("SAVED", OUT, flush=True)
