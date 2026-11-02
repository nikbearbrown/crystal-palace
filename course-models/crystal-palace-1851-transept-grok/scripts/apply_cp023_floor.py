"""CANDIDATE (2026-11-02): CP023 start lower-frame floor detail, on the live CP023 source r11_envelope_v2.blend.

  blender -b rounds/candidates/r11_envelope_v2.blend -P scripts/apply_cp023_floor.py -- \
      --out rounds/candidates/r11_envelope_v2_cp023floor.blend

Opens r11_envelope_v2.blend (live CP023 source, never saved over) and writes a NEW candidate blend with:
  F1  floor boards (GT_FloorBoards, FLOOR_BOARDS + HPE2_FLOOR_E): the existing printed 1/2 in open gaps at a 9.5 in
      pitch are kept exactly (Official Catalogue 1851 Intro p.62: boards 1 1/2 in thick, laid half an inch apart;
      Berlyn & Fowler p.37). Added: per-board tone variation of plain deal, staggered tight butt joints (12 ft board
      lengths, inferred), a faint lengthwise grain, light foot-traffic dust, and a small bump at the gap edges so the
      near boards catch the light. DEPARTURES FLR-01/02.
  F2  one dropped Official Catalogue, lying open face-up on the boards in the lower frame (right of the nave axis).
      DEPARTURES FLR-03 (generic paper-wrapped octavo, not a measured copy).
  F3  STATUE_L40 (plinth + figure) nudged 0.30 m south so its plinth corner no longer peeks in at the right frame
      edge as a pale sliver (start frame, about x 1270, y 600). DEPARTURES FLR-04.
No people are touched (render_views does the swap/dressing as for live). No back-facing foreground figures.
Hyde Park 1851 only; Claude's / Codex's / Muse's files are never opened for writing.
"""
import bpy, bmesh, math, os, sys
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
OUT = arg("--out", "rounds/candidates/r11_envelope_v2_cp023floor.blend")
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
for protected in ("rounds/r11.blend", "rounds/r10.blend", "rounds/candidates/r11_envelope.blend",
                  "rounds/candidates/r11_envelope_v2.blend"):
    assert os.path.abspath(out) != os.path.abspath(os.path.join(ROOT, protected)), "refusing to overwrite " + protected
try: bpy.context.preferences.filepaths.save_version = 0
except Exception: pass
sc = bpy.context.scene
CAT_UV = (float(arg("--cat-u", "0.635")), float(arg("--cat-v", "0.11")))   # catalogue centre in the start frame

# ---------------- F1 floor boards ----------------
m = bpy.data.materials["GT_FloorBoards"]
nt = m.node_tree; N = nt.nodes; L = nt.links
bsdf = N["Principled BSDF"]; mix = N["Mix"]; gapgt = N["Math.002"]; sep = N["Separate XYZ"]
PITCH = 1.0 / N["Math"].inputs[1].default_value          # 0.2413 m = 9.5 in (9 in board + 1/2 in gap), unchanged
BOARD_LEN = 12 * 0.3048                                  # inferred 12 ft deal lengths (no source prints board length)
def node(t, **kw):
    n = N.new(t)
    for k, v in kw.items(): setattr(n, k, v)
    return n
def math_(op, a=None, b=None, v1=None):
    n = node("ShaderNodeMath", operation=op)
    if v1 is not None: n.inputs[1].default_value = v1
    if a is not None: L.new(a, n.inputs[0])
    if b is not None: L.new(b, n.inputs[1])
    return n
# board index -> per-board random values
idx = math_('FLOOR', math_('MULTIPLY', sep.outputs["X"], v1=1.0 / PITCH).outputs[0])
wn = node("ShaderNodeTexWhiteNoise", noise_dimensions='1D'); L.new(idx.outputs[0], wn.inputs["W"])
wn2 = node("ShaderNodeTexWhiteNoise", noise_dimensions='1D')
idx2 = math_('ADD', idx.outputs[0], v1=37.0); L.new(idx2.outputs[0], wn2.inputs["W"])
# staggered butt joints: fract((Y + r*L)/L) near 0 -> thin dark line (tight joint, 3 mm)
off = math_('MULTIPLY', wn.outputs["Value"], v1=BOARD_LEN)
yy = math_('ADD', sep.outputs["Y"], off.outputs[0])
fr = math_('FRACT', math_('DIVIDE', yy.outputs[0], v1=BOARD_LEN).outputs[0])
butt = math_('LESS_THAN', fr.outputs[0], v1=0.003 / BOARD_LEN)
# tone: base deal colour scaled 0.80..1.14 per board, plus a weathered grey mix by the second random
toneA = node("ShaderNodeMix", data_type='RGBA', blend_type='MIX')
toneA.inputs["A"].default_value = (0.58, 0.49, 0.37, 1); toneA.inputs["B"].default_value = (0.50, 0.46, 0.41, 1)
L.new(wn2.outputs["Value"], toneA.inputs["Factor"])
bright = math_('ADD', math_('MULTIPLY', wn.outputs["Value"], v1=0.34).outputs[0], v1=0.80)
toneB = node("ShaderNodeMix", data_type='RGBA', blend_type='MULTIPLY'); toneB.inputs["Factor"].default_value = 1.0
L.new(toneA.outputs["Result"], toneB.inputs["A"])
cr = node("ShaderNodeCombineColor"); [L.new(bright.outputs[0], cr.inputs[i]) for i in range(3)]
L.new(cr.outputs[0], toneB.inputs["B"])
# grain: noise stretched along the board length (Y), +-5%
tc = N["Texture Coordinate"]
mp = node("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (60.0, 2.5, 1.0); L.new(tc.outputs["Object"], mp.inputs["Vector"])
gr = node("ShaderNodeTexNoise"); gr.inputs["Scale"].default_value = 1.0; gr.inputs["Detail"].default_value = 4.0
L.new(mp.outputs[0], gr.inputs["Vector"])
grain = node("ShaderNodeMix", data_type='RGBA', blend_type='OVERLAY'); grain.inputs["Factor"].default_value = 0.10
L.new(toneB.outputs["Result"], grain.inputs["A"]); L.new(gr.outputs["Color"], grain.inputs["B"])
# foot-traffic dust: broad soft noise lifting the boards toward a pale grey-buff, 0..12%
dn = node("ShaderNodeTexNoise"); dn.inputs["Scale"].default_value = 0.35; dn.inputs["Detail"].default_value = 3.0
L.new(tc.outputs["Object"], dn.inputs["Vector"])
dr = node("ShaderNodeMapRange"); dr.inputs["From Min"].default_value = 0.45; dr.inputs["From Max"].default_value = 0.75
dr.inputs["To Min"].default_value = 0.0; dr.inputs["To Max"].default_value = 0.12; L.new(dn.outputs["Fac"], dr.inputs["Value"])
dust = node("ShaderNodeMix", data_type='RGBA', blend_type='MIX'); dust.inputs["B"].default_value = (0.62, 0.58, 0.50, 1)
L.new(dr.outputs[0], dust.inputs["Factor"]); L.new(grain.outputs["Result"], dust.inputs["A"])
# butt joints darken to 35%
bj = node("ShaderNodeMix", data_type='RGBA', blend_type='MULTIPLY'); bj.inputs["B"].default_value = (0.35, 0.33, 0.30, 1)
L.new(butt.outputs[0], bj.inputs["Factor"]); L.new(dust.outputs["Result"], bj.inputs["A"])
# feed the existing gap mix (A = board colour, B = dark gap 0.05 unchanged)
L.new(bj.outputs["Result"], mix.inputs["A"])
# roughness 0.84..0.92 per board
rough = math_('ADD', math_('MULTIPLY', wn2.outputs["Value"], v1=0.08).outputs[0], v1=0.84)
L.new(rough.outputs[0], bsdf.inputs["Roughness"])
# bump: gaps and butt joints low
hgt = math_('MAXIMUM', gapgt.outputs[0], butt.outputs[0])
bump = node("ShaderNodeBump", invert=True); bump.inputs["Strength"].default_value = 0.6; bump.inputs["Distance"].default_value = 0.004
L.new(hgt.outputs[0], bump.inputs["Height"]); L.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
print("CP023F_FLOOR pitch_m", round(PITCH, 4), "gap_m", round(PITCH * (1 - gapgt.inputs[1].default_value), 4),
      "board_len_m", round(BOARD_LEN, 3), flush=True)

# ---------------- F3 STATUE_L40 nudge ----------------
for n in ("STATUE_L40_PLINTH", "STATUE_L40_FIGURE"):
    ob = bpy.data.objects.get(n)
    if ob: ob.location.y -= 0.30; print("CP023F_NUDGE", n, tuple(round(x, 3) for x in ob.location), flush=True)

# ---------------- F2 dropped catalogue ----------------
cam = bpy.data.objects["CP023_into_nave_start"]
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
tr, br, bl, tl = [cam.matrix_world @ p for p in cam.data.view_frame(scene=sc)]
u, v = CAT_UV; p = bl + (br - bl) * u + (tl - bl) * v
o = cam.matrix_world.translation; d = (p - o).normalized()
hit, loc, nor, _, hob, _ = sc.ray_cast(dg, o, d)
assert hit and hob.name in ("FLOOR_BOARDS", "HPE2_FLOOR_E"), ("catalogue spot not on boards", hob and hob.name)
print("CP023F_CATALOGUE_SPOT", tuple(round(x, 3) for x in loc), "dist", round((loc - o).length, 2), flush=True)

def pmat(name, rgb, rough=0.75, stripes=None):
    mm = bpy.data.materials.new(name); mm.use_nodes = True
    b = mm.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    if stripes:   # faint print lines across the page (object coords)
        t = mm.node_tree; tcn = t.nodes.new("ShaderNodeTexCoord"); w = t.nodes.new("ShaderNodeTexWave")
        w.wave_type = 'BANDS'; w.bands_direction = 'Y'; w.inputs["Scale"].default_value = stripes; w.inputs["Distortion"].default_value = 0
        cr_ = t.nodes.new("ShaderNodeMapRange"); cr_.inputs["From Min"].default_value = 0.7; cr_.inputs["To Min"].default_value = 0; cr_.inputs["To Max"].default_value = 0.35
        mx = t.nodes.new("ShaderNodeMix"); mx.data_type = 'RGBA'; mx.inputs["A"].default_value = (*rgb, 1); mx.inputs["B"].default_value = (0.12, 0.11, 0.10, 1)
        t.links.new(tcn.outputs["Object"], w.inputs["Vector"]); t.links.new(w.outputs["Fac"], cr_.inputs["Value"])
        t.links.new(cr_.outputs[0], mx.inputs["Factor"]); t.links.new(mx.outputs["Result"], b.inputs["Base Color"])
    return mm
M_COVER = pmat("CP023F_CatalogueWrapper", (0.62, 0.52, 0.36), 0.8)        # buff paper wrapper (generic)
M_PAGE = pmat("CP023F_CataloguePage", (0.86, 0.82, 0.70), 0.85)   # plain cream (print lines read as a grate at 6 m)
coll = bpy.data.collections.new("CP023F_FLOOR_DETAIL"); sc.collection.children.link(coll)
def box(name, sx, sy, sz, mat, loc_, rot=(0, 0, 0), parent=None):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    bm.to_mesh(me); bm.free(); me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    ob.location = loc_; ob.rotation_euler = rot
    if parent: ob.parent = parent
    ob["dress_kind"] = "floor_detail"; ob["cp023f"] = True
    return ob
# open octavo, ~11 x 18 cm per side, ~1 cm page block per side; spine along local Y; leaves tilted up 9 deg at the spine
root = bpy.data.objects.new("CP023F_CATALOGUE", None); coll.objects.link(root)
root.location = (loc.x, loc.y, loc.z); root.rotation_euler = (0, 0, math.radians(-23.0)); root["dress_kind"] = "floor_detail"
W_, H_, T_ = 0.112, 0.180, 0.009
for s in (-1, 1):
    tilt = s * math.radians(9.0)
    box(f"CP023F_CAT_WRAP_{'L' if s < 0 else 'R'}", W_ + 0.004, H_ + 0.006, 0.0012, M_COVER,
        (s * (W_ / 2 + 0.002), 0, 0.0006 + 0.004), (0, -tilt, 0), root)
    box(f"CP023F_CAT_PAGES_{'L' if s < 0 else 'R'}", W_, H_, T_ * (1.25 if s > 0 else 0.75), M_PAGE,
        (s * W_ / 2, 0, 0.0012 + T_ * (1.25 if s > 0 else 0.75) / 2 + 0.004), (0, -tilt, 0), root)
# a loose fold of the right-hand leaf lifting slightly (single page)
box("CP023F_CAT_LEAF", W_ * 0.98, H_ * 0.98, 0.0006, M_PAGE, (W_ * 0.49, 0, T_ * 1.3 + 0.012), (0, -math.radians(14), 0), root)
print("CP023F_CATALOGUE", root.location[:], flush=True)

os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True)
print("SAVED", out, flush=True)
