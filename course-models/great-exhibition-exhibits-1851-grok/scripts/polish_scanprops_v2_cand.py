"""CANDIDATE v2 (2026-11-09): CP025 scan-props follow-up polish, Hyde Park 1851 only. Never writes live e02.

Opens LIVE rounds/e02.blend (= KEEP 68cfae5, md5 fce122da; already holds SCN_SCANPROPS_HP1851) READ-ONLY and saves
rounds/candidates/e02_scanprops_v2.blend. Only SCN_* props and new SCN2_* objects are touched; nothing else moves.
Fixes from the BUILD-PLAN CP025 row (misses after the scan-props KEEP):
  1. Elkington jewel cabinet near-silhouette  -> retint to the RCT photo (gilt + silvered electrotype, blue enamel)
     with a hue-keeping albedo lift (--cab-gain) and partial metal, plus a soft overhead 'roof-glazing' fill
     (--cab-fill W; area light, camera-invisible) over the stand.
  2. Greek Slave small/dim -> true height kept (165.5 cm, Raby marble); statue moved clear of the visitor in front
     (position kept at -3.6,1.7: no closer spot stays in both CP025 frames; --slave X,Y,YAW), whiter marble (--marble-gain), a dark velvet back curtain inside the canopy (the 1851 'dark
     velvet niche', --no-niche to drop) and a soft fill under the canopy tester (--slave-fill W).
  3. W&B vase height verified (no primary dimension; 95 oz 22 ct gold -> 18 in is plausible, kept 0.457 m) and a
     soft fill (--vase-fill W) + brighter gold (--gold-gain); optional glazed case (--vase-case; OFF by default: the
     sources found show/describe no case).
  blender -b -P scripts/polish_scanprops_v2_cand.py -- [--out rounds/candidates/e02_scanprops_v2.blend]
     [--slave -3.6,1.7,35] [--marble-gain 1.8] [--slave-fill 40] [--no-niche] [--cab-gain 2.2] [--cab-metal 0.35]
     [--cab-fill 200] [--stand-fill 50] [--gold-gain 2.6] [--vase-fill 60] [--vase-case]
Units: metres, W.  Departures EX_SCN2_* in DEPARTURES.md.
"""
import bpy, bmesh, math, os, sys
from mathutils import Vector, Matrix
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
def trip(s): x, y, a = [float(v) for v in s.split(",")]; return x, y, math.radians(a)
LIVE = os.path.join(ROOT, "rounds/e02.blend")
BASE = arg("--base", LIVE); BASE = BASE if os.path.isabs(BASE) else os.path.join(ROOT, BASE)
OUT = arg("--out", "rounds/candidates/e02_scanprops_v2.blend"); OUT = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
assert os.path.abspath(OUT) != os.path.abspath(LIVE), "refusing to overwrite live e02"
SLAVE = trip(arg("--slave", "-3.6,1.7,35"))
MARBLE_GAIN = float(arg("--marble-gain", "1.8")); SLAVE_FILL = float(arg("--slave-fill", "40"))
NICHE = "--no-niche" not in argv
CAB_GAIN = float(arg("--cab-gain", "2.2")); CAB_METAL = float(arg("--cab-metal", "0.35")); CAB_FILL = float(arg("--cab-fill", "200")); STAND_FILL = float(arg("--stand-fill", "50"))
GOLD_GAIN = float(arg("--gold-gain", "2.6")); VASE_FILL = float(arg("--vase-fill", "60")); VASE_CASE = "--vase-case" in argv
CAND = "e02_scanprops_v2"; P2 = "SCN2_"

bpy.ops.wm.open_mainfile(filepath=BASE)
OB = bpy.data.objects
for o in list(OB):
    if o.name.startswith(P2): OB.remove(o, do_unlink=True)
coll = bpy.data.collections["SCN_SCANPROPS_HP1851"]
def tag(o, kind):
    o["candidate"] = CAND; o["cp_era"] = "HP1851"; o["cp_state"] = "Hyde Park 1851"; o["part_kind"] = kind
    if o.name not in coll.objects: coll.objects.link(o)
    return o
def area_light(name, loc, size, watts, receivers, spread_deg=70, rgb=(1.0, 0.97, 0.92), sy=None):
    """camera-invisible soft fill, LIGHT-LINKED to its prop only (no floor pools, no change to the hall exposure)"""
    L = bpy.data.lights.new(name, 'AREA'); L.shape = 'RECTANGLE'; L.size = size; L.size_y = sy or size
    L.energy = watts; L.color = rgb; L.spread = math.radians(spread_deg)
    o = bpy.data.objects.new(name, L); o.location = loc
    o.visible_camera = False   # a fill, not a visible lamp (glossy kept: gilt and gold need the specular)
    rc = bpy.data.collections.get(name + "_LL") or bpy.data.collections.new(name + "_LL")
    for r in receivers:
        if r.name not in rc.objects: rc.objects.link(r)
    o.light_linking.receiver_collection = rc; o.light_linking.blocker_collection = None
    return tag(o, "fill_light")
def aim(o, target):
    o.rotation_euler = (Vector(target) - o.location).to_track_quat('-Z', 'Y').to_euler()
CAM_LINEUP = OB.get("EX_lineup_start")
def front_fill(name, prop, receivers, watts, size, dist, height, spread=50):
    """fill from the camera side, up in the roof (stands in for the glazed roof bay in front of the exhibit)"""
    c = prop.location.copy(); c.z += prop.dimensions.z * 0.5
    d = (CAM_LINEUP.location - c); d.z = 0; d.normalize()
    o = area_light(name, (c.x + d.x * dist, c.y + d.y * dist, c.z + height), size, watts, receivers, spread)
    aim(o, c); return o

# ---------------- 1. Greek Slave group ----------------
slave = OB["SCN_fig-52_greek-slave"]; ped = OB["SCN_slave_pedestal"]; can = OB["SCN_slave_canopy"]; rail = OB["SCN_slave_rail"]
ox, oy = slave.location.x, slave.location.y; oyaw = slave.rotation_euler.z
sx, sy, syaw = SLAVE
for o in (slave, ped, can):
    o.location.x = sx; o.location.y = sy; o.rotation_euler.z = syaw
# rail mesh is baked in world coords around (ox, oy): rotate about its centre and translate
rail.data.transform(Matrix.Translation((sx, sy, 0)) @ Matrix.Rotation(syaw - oyaw, 4, 'Z') @ Matrix.Translation((-ox, -oy, 0)))
rail.data.update()
m = slave.data.materials[0]
mul = [n for n in m.node_tree.nodes if n.type == 'MATH' and n.operation == 'MULTIPLY']
assert mul, "marble remap node missing"; mul[0].inputs[1].default_value = MARBLE_GAIN
W = 2.1; CH = 3.9; VAL = 0.42
cw, sw = math.cos(syaw), math.sin(syaw)
def local(px, py, pz): return Vector((sx + px * cw - py * sw, sy + px * sw + py * cw, pz))
if NICHE:
    # gathered dark crimson velvet back curtain on the canopy's back (+Y local) side, floor to valance
    mv = bpy.data.materials.get("SCN2_NicheVelvet") or bpy.data.materials.new("SCN2_NicheVelvet"); mv.use_nodes = True
    nb = mv.node_tree.nodes["Principled BSDF"]; nb.inputs["Base Color"].default_value = (0.16, 0.012, 0.018, 1)
    nb.inputs["Roughness"].default_value = 0.9; nb.inputs["Sheen Weight"].default_value = 0.5; mv.diffuse_color = (0.16, 0.012, 0.018, 1)
    bm = bmesh.new(); NX, NZ = 48, 6; z1 = CH - VAL + 0.02; yb = W / 2 - 0.06
    verts = [[bm.verts.new((-W / 2 + 0.05 + (W - 0.10) * i / NX, yb + 0.045 * math.sin(i * math.pi * 2 / 4.0), z1 * k / NZ)) for k in range(NZ + 1)] for i in range(NX + 1)]
    for i in range(NX):
        for k in range(NZ): bm.faces.new([verts[i][k], verts[i + 1][k], verts[i + 1][k + 1], verts[i][k + 1]])
    me = bpy.data.meshes.new("ME_SCN2_slave_niche"); bm.to_mesh(me); bm.free(); me.materials.append(mv)
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new("SCN2_slave_niche", me); o.location = (sx, sy, 0); o.rotation_euler = (0, 0, syaw); tag(o, "niche_curtain")
if SLAVE_FILL > 0:
    o = area_light("SCN2_slave_fill", local(0, -0.35, CH - VAL - 0.08), 1.2, SLAVE_FILL, [slave], 75); o.rotation_euler = (math.radians(-18), 0, syaw)

# ---------------- 2. Elkington cabinet ----------------
cab = OB["SCN_fig-54_elkington-jewel-cabinet"]
m0 = cab.data.materials[0]; m = m0.copy(); m.name = m0.name + "_gilt_v2"; cab.data.materials[0] = m
nt = m.node_tree; n = nt.nodes; l = nt.links
b = [x for x in n if x.type == 'BSDF_PRINCIPLED'][0]
tex = [x for x in n if x.type == 'TEX_IMAGE' and x.image and x.image.name.startswith("Color")][0]
for inp in ("Metallic", "Roughness", "Base Color"):
    for lk in list(b.inputs[inp].links): l.remove(lk)
hsv = n.new("ShaderNodeHueSaturation"); hsv.inputs["Saturation"].default_value = 1.0; hsv.inputs["Value"].default_value = CAB_GAIN
l.new(tex.outputs["Color"], hsv.inputs["Color"]); l.new(hsv.outputs["Color"], b.inputs["Base Color"])
b.inputs["Metallic"].default_value = CAB_METAL; b.inputs["Roughness"].default_value = 0.34
cx, cy = cab.location.x, cab.location.y
if CAB_FILL > 0: front_fill("SCN2_cabinet_fill", cab, [cab], CAB_FILL, 2.0, 2.6, 3.2)
if STAND_FILL > 0: front_fill("SCN2_cabinet_stand_fill", cab, [OB["SCN_cabinet_stand"]], STAND_FILL, 2.0, 2.6, 3.2)

# ---------------- 3. W&B vase ----------------
vase = OB["SCN_unnumbered_watherston-brogden-vase"]
mv = vase.data.materials[0]
mul = [x for x in mv.node_tree.nodes if x.type == 'MATH' and x.operation == 'MULTIPLY']
assert mul, "gold remap node missing"; mul[0].inputs[1].default_value = GOLD_GAIN
vx, vy = vase.location.x, vase.location.y; vz = vase.location.z
if VASE_FILL > 0: front_fill("SCN2_vase_fill", vase, [vase], VASE_FILL, 1.2, 1.8, 2.6)
if VASE_CASE:
    g = bpy.data.materials.new("SCN2_CaseGlass"); g.use_nodes = True; gb = g.node_tree.nodes["Principled BSDF"]
    gb.inputs["Transmission Weight"].default_value = 1.0; gb.inputs["Roughness"].default_value = 0.02; gb.inputs["IOR"].default_value = 1.5
    bm = bmesh.new(); s = 0.40; h = 0.62
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((0, 0, vz + h / 2)) @ Matrix.Diagonal((s, s, h, 1)))
    me = bpy.data.meshes.new("ME_SCN2_vase_case"); bm.to_mesh(me); bm.free(); me.materials.append(g)
    o = bpy.data.objects.new("SCN2_vase_case", me); o.location = (vx, vy, 0); o.rotation_euler = (0, 0, vase.rotation_euler.z); tag(o, "glass_case")

t = bpy.data.texts.get("CREDIT_SCN2_CAND") or bpy.data.texts.new("CREDIT_SCN2_CAND"); t.clear()
t.write("CANDIDATE e02_scanprops_v2 (2026-11-09, Grok Bot): CP025 scan-props follow-up polish, Hyde Park 1851 only.\n"
        f"slave {SLAVE} marble_gain {MARBLE_GAIN} niche {NICHE} slave_fill {SLAVE_FILL} W | cabinet gain {CAB_GAIN} metal {CAB_METAL} fill {CAB_FILL} W"
        f" stand_fill {STAND_FILL} W | vase gold_gain {GOLD_GAIN} fill {VASE_FILL} W case {VASE_CASE}. Departures EX_SCN2_*.\n")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=False)
print("SCN2_SAVED", OUT, flush=True)
