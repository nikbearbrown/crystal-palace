"""CP015_blinds CANDIDATE 2026-11-09 (DEPARTURES CN52): "canvas shading reads" pass on the LIVE CP015 source rounds/c04.blend.
Loads rounds/c04.blend (never written; md5 7810ed1f...) and saves rounds/candidates/c04_cp015canvas.blend. Use that blend for
CP015_blinds_start ONLY (it also keeps CP015_louvre_start consistent, but that camera is not part of this candidate).

Changes (all inside the CN09/CN10 canvas + louvre bays, x 228-300 ft, tier-1 south):
 1. Canvas re-draped after Downes 1852 p.44 ("Miscellaneous details"): "The roof was covered with canvas ... nailed to the ridges and
    allowed to hang down between them. It was in two breadths, with the seam in the centre; the rain ... passed through the seam
    and dropped into the Paxton gutter."  The old CN09 sheet was a 4-facet tent offset 5 in above the glass. Now each 8 ft ridge
    unit carries a sagging drape nailed on the ridge cap, one 4 ft breadth each side, hanging to a seam 5 in above the Paxton
    gutter, 12 facets per breadth (concave sag ~1 in at mid-breadth, clearance to the glass checked >= 0.4 in, tightest at the ridge cap), with the seam strip + nail line darker.
 2. Calico shader: unbleached cotton (warm cream), mostly translucent (0.8) so it reads as a lit cloth ceiling from below; slight
    noise for weave/soiling. Glass in the canvas units only gets a clearer tint (0.86 vs shared 0.58-0.64) so the cloth shows
    through; every other roof unit keeps GT_RoofGlassBuild.
 3. Louvres: Downes Plate XXVII text - one worm wheel drives 108 ft of shafting each side, "set in motion simultaneously". The
    0 -> 62 -> 0 deg animation that only bay x 240 had (CN10) is copied to bays 264 and 288 (high + low bands), and the candidate
    scene frame is set to 36 (62 deg open) so CP015_blinds_start shows the open louvre band. Frame 1 (closed) is unchanged.
blender -b rounds/c04.blend -P scripts/cand_cp015_canvas_20261109.py -- [--out rounds/candidates/c04_cp015canvas.blend]"""
import bpy, bmesh, math, sys, os
FT = 0.3048
def ft(v): return v * FT
def inch(v): return v * FT / 12.0
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/c04_cp015canvas.blend"
OUT = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
L, W, RISE, OFF = ft(24), ft(8), ft(1.6), inch(1.3)          # build_construction.py mesh_roof (CN23)
Z_NAIL = RISE + inch(1.5) + inch(0.25)                        # on the ridge cap (ridge box top = rise + 1.5 in)
Z_SEAM = inch(5.0)                                             # seam hangs 5 in above the gutter line (gutter top = 1 in)
P_SAG, NSEG = 1.2, 12

def new_mat(name):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True; m.node_tree.nodes.clear(); return m, m.node_tree

def calico(name, base, dark, trans):
    m, nt = new_mat(name); n, l = nt.nodes, nt.links
    out = n.new("ShaderNodeOutputMaterial"); mix = n.new("ShaderNodeMixShader"); dif = n.new("ShaderNodeBsdfDiffuse"); tr = n.new("ShaderNodeBsdfTranslucent")
    noi = n.new("ShaderNodeTexNoise"); noi.inputs["Scale"].default_value = 6.0; noi.inputs["Detail"].default_value = 4.0
    ramp = n.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = (*dark, 1); ramp.color_ramp.elements[1].color = (*base, 1)
    ramp.color_ramp.elements[0].position = 0.25; ramp.color_ramp.elements[1].position = 0.75
    l.new(noi.outputs["Fac"], ramp.inputs["Fac"])
    l.new(ramp.outputs["Color"], dif.inputs["Color"]); l.new(ramp.outputs["Color"], tr.inputs["Color"])
    mix.inputs[0].default_value = trans
    l.new(dif.outputs[0], mix.inputs[1]); l.new(tr.outputs[0], mix.inputs[2]); l.new(mix.outputs[0], out.inputs["Surface"])
    return m

CALICO = calico("CP015_Calico", (0.93, 0.87, 0.72), (0.84, 0.77, 0.62), 0.80)
SEAM = calico("CP015_CalicoSeam", (0.62, 0.55, 0.43), (0.55, 0.48, 0.37), 0.45)   # double thickness + wet seam / nail strip

g, nt = new_mat("CP015_GlassUnderCanvas"); n, l = nt.nodes, nt.links
o_ = n.new("ShaderNodeOutputMaterial"); tp = n.new("ShaderNodeBsdfTransparent"); gl = n.new("ShaderNodeBsdfGlossy"); fr = n.new("ShaderNodeFresnel"); mx = n.new("ShaderNodeMixShader")
tp.inputs["Color"].default_value = (0.86, 0.88, 0.86, 1); gl.inputs["Roughness"].default_value = 0.04; fr.inputs["IOR"].default_value = 1.52
l.new(fr.outputs[0], mx.inputs[0]); l.new(tp.outputs[0], mx.inputs[1]); l.new(gl.outputs[0], mx.inputs[2]); l.new(mx.outputs[0], o_.inputs["Surface"])

# ---- 1. re-drape the canvas in the shared roof_canvas mesh (27 units, all in bays x 228-300) ----
me = bpy.data.meshes["roof_canvas"]
assert me.materials[2].name == "GT_Canvas", me.materials[2].name
bm = bmesh.new(); bm.from_mesh(me)
old = [f for f in bm.faces if f.material_index == 2]; assert len(old) == 4, len(old)
bmesh.ops.delete(bm, geom=old, context="FACES")
def zc(t): return Z_SEAM + (Z_NAIL - Z_SEAM) * (1 - t) ** P_SAG          # t = |y| / (W/2): 0 at ridge, 1 at gutter seam
def zg(t): return OFF + RISE * (1 - t)                                     # glass plane
clear = min(zc(k / 200) - zg(k / 200) for k in range(201))
assert clear >= inch(0.4) - 1e-6, f"canvas cuts the glass: clearance {clear / inch(1):.2f} in"
nf = 0
for s in (-1, 1):
    ts = [k / NSEG for k in range(NSEG + 1)]
    rows = [[bm.verts.new((sx * L / 2, s * t * W / 2, zc(t))) for t in ts] for sx in (-1, 1)]
    for k in range(NSEG):
        f = bm.faces.new([rows[0][k], rows[1][k], rows[1][k + 1], rows[0][k + 1]] if s > 0 else [rows[0][k + 1], rows[1][k + 1], rows[1][k], rows[0][k]])
        f.material_index = 3 if (k == 0 or k == NSEG - 1) else 2; f.smooth = True; nf += 1
bmesh.ops.remove_doubles(bm, verts=[v for v in bm.verts if abs(v.co.y) < 1e-6 and abs(v.co.z - Z_NAIL) < 1e-6], dist=1e-5)
bm.normal_update()
for f in bm.faces:
    if f.material_index in (2, 3) and f.normal.z < 0: f.normal_flip()
bm.to_mesh(me); bm.free()
me.materials[0] = g; me.materials[2] = CALICO
if len(me.materials) < 4: me.materials.append(SEAM)
else: me.materials[3] = SEAM
print(f"CANVAS faces {nf}, min clearance to glass {clear / inch(1):.2f} in, sag at quarter {(Z_SEAM + (Z_NAIL - Z_SEAM) * 0.5 - zc(0.5)) / inch(1):.2f} in")

# ---- 3. louvre bays 264 / 288 move with bay 240 (one shafting run, Downes Pl. XXVII) ----
src = bpy.data.objects["KLOUVRE_+240_high_0"]
keys = [(int(kp.co[0]), kp.co[1]) for kp in src.animation_data.action.fcurves[0].keyframe_points] if hasattr(src.animation_data.action, "fcurves") and src.animation_data.action.fcurves else None
if not keys:   # Blender 5 layered actions
    ch = src.animation_data.action.layers[0].strips[0].channelbags[0]; keys = [(int(kp.co[0]), kp.co[1]) for kp in ch.fcurves[0].keyframe_points]
nb = 0
for xc in (264, 288):
    for band, n_ in (("low", 3), ("high", 8)):
        for k in range(n_):
            ob = bpy.data.objects[f"KLOUVRE_{xc:+.0f}_{band}_{k}"]
            for fr_, ang in keys:
                ob.rotation_euler.x = ang; ob.keyframe_insert("rotation_euler", index=0, frame=fr_)
            nb += 1
print("LOUVRE keys", [(f, round(math.degrees(a), 1)) for f, a in keys], "copied to", nb, "blades")
bpy.context.scene.frame_set(36)
print("FRAME", bpy.context.scene.frame_current, "blade 264_high_0 deg", round(math.degrees(bpy.data.objects["KLOUVRE_+264_high_0"].rotation_euler.x), 1))
bpy.context.scene["cp015_candidate"] = "CN52 2026-11-09: calico drape + clear glass under canvas + louvres 240/264/288 together; frame 36"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT); print("SAVED", OUT)
