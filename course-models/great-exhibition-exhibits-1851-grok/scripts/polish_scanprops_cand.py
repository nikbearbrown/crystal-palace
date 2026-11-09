"""CANDIDATE (2026-11-09): CP025 exhibit-court dressing with three cleaned scan-model props, Hyde Park 1851 only.

Props (our cleaned copies, made by scripts/prep_scanprops.py from origin/main e88ee17 scan-models/blend/*;
scan-models/ itself is never edited or checked out):
  assets/scanprops/fig-52_greek-slave_hp1851.blend              Powers, Greek Slave (1851 exhibit = Raby marble, 165.5 cm)
  assets/scanprops/fig-54_elkington-jewel-cabinet_hp1851.blend  Gruner/Elkington jewel cabinet (RCIN 1562, 97 x 132 x 81 cm)
  assets/scanprops/unnumbered_watherston-brogden-vase_hp1851.blend  Watherston & Brogden gold vase (~18 in, verify)
Each ~58.8 k tris (source ~1.4 M). Departures EX_SCN_* in DEPARTURES.md.

Opens LIVE rounds/e02.blend READ-ONLY and saves a NEW candidate (default rounds/candidates/e02_scanprops.blend).
Nothing existing is moved or changed; only the SCN_ collection is added.
  Group A (west of the Koh-i-Noor enclosure, seen in CP025_visitors_start/_end): Greek Slave on a turned revolving
           pedestal under a crimson canopy (SAAM: 'rotating pedestal under a lavish red canopy').
  Group B (open floor south-east of the Koh-i-Noor, under the lit transept skylight in EX_lineup_start): jewel cabinet on a crimson-clothed
           stand; gold vase on a velvet-topped pedestal.
  blender -b -P scripts/polish_scanprops_cand.py -- [--out rounds/candidates/e02_scanprops.blend]
     [--slave X,Y,YAWDEG] [--cabinet X,Y,YAWDEG] [--vase X,Y,YAWDEG] [--no-canopy] [--no-rails]
     [--marble-gain 1.55] [--gold-gain 2.2] [--slave-ped-h 0.80] [--cab-stand-h 0.78] [--vase-ped-h 0.95] [--canopy-w 2.1] [--canopy-h 3.9]
Units: metres.
"""
import bpy, bmesh, math, os, sys
from mathutils import Vector, Matrix
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
def trip(s): x, y, a = [float(v) for v in s.split(",")]; return x, y, math.radians(a)
LIVE = os.path.join(ROOT, "rounds/e02.blend")
OUT = arg("--out", "rounds/candidates/e02_scanprops.blend"); OUT = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
assert os.path.abspath(OUT) != os.path.abspath(LIVE), "refusing to overwrite live e02"
SLAVE = trip(arg("--slave", "-3.6,1.7,35"))
CAB = trip(arg("--cabinet", "1.2,-6.2,-35"))
VASE = trip(arg("--vase", "6.2,-8.6,-40"))
CANOPY = "--no-canopy" not in argv; RAILS = "--no-rails" not in argv
MARBLE_GAIN = float(arg("--marble-gain", "1.55")); GOLD_GAIN = float(arg("--gold-gain", "2.2"))
PED_H = float(arg("--slave-ped-h", "0.80")); CAB_H = float(arg("--cab-stand-h", "0.78")); VPED_H = float(arg("--vase-ped-h", "0.95"))
CAND = "e02_scanprops"; PREFIX = "SCN_"
A = os.path.join(ROOT, "assets/scanprops")

bpy.ops.wm.open_mainfile(filepath=LIVE)
for o in list(bpy.data.objects):
    if o.name.startswith(PREFIX) or o.get("candidate") == CAND: bpy.data.objects.remove(o, do_unlink=True)
coll = bpy.data.collections.new("SCN_SCANPROPS_HP1851"); bpy.context.scene.collection.children.link(coll)
coll["candidate"] = CAND; coll["cp_era"] = "HP1851"; coll["cp_state"] = "Hyde Park 1851"

def mat(name, rgb, rough=0.6, metal=0.0, sheen=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if sheen: b.inputs["Sheen Weight"].default_value = sheen
    m.diffuse_color = (*rgb, 1); return m
M = dict(
    crimson=mat("SCN_CrimsonVelvet", (0.30, 0.025, 0.03), 0.85, sheen=0.6),
    crimson_dk=mat("SCN_CrimsonDrape", (0.20, 0.015, 0.02), 0.9, sheen=0.5),
    mahog=mat("SCN_Mahogany", (0.13, 0.045, 0.022), 0.45),
    gilt=mat("SCN_Gilt", (0.80, 0.58, 0.22), 0.32, 1.0),
    brass=mat("SCN_Brass", (0.62, 0.42, 0.13), 0.32, 1.0),
    rope=mat("SCN_CrimsonRope", (0.36, 0.03, 0.03), 0.85),
    marble_ped=mat("SCN_PedestalMarble", (0.55, 0.52, 0.48), 0.35),
    letter=mat("SCN_LetterCream", (0.85, 0.80, 0.66), 0.6),
)
def put(name, bm, mats, kind, loc=(0, 0, 0), rz=0.0):
    me = bpy.data.meshes.new("ME_" + name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    for p in me.polygons: p.use_smooth = False
    o = bpy.data.objects.new(name, me); coll.objects.link(o); o.location = loc; o.rotation_euler = (0, 0, rz)
    o["candidate"] = CAND; o["cp_era"] = "HP1851"; o["cp_state"] = "Hyde Park 1851"; o["part_kind"] = kind
    return o
def mi(bm, n0, idx):
    bm.faces.ensure_lookup_table()
    for f in bm.faces[n0:]: f.material_index = idx
def lathe(bm, prof, seg=32, M=None):
    rings = [[bm.verts.new((r * math.cos(2 * math.pi * k / seg), r * math.sin(2 * math.pi * k / seg), z)) for k in range(seg)] for r, z in prof]
    if M is not None:
        for ring in rings:
            for v in ring: v.co = M @ v.co
    for a, b in zip(rings, rings[1:]):
        for k in range(seg): bm.faces.new([a[k], a[(k + 1) % seg], b[(k + 1) % seg], b[k]])
    bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
def box(bm, c, s):
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(c) @ Matrix.Diagonal((*s, 1)))
def rod(bm, a, b, r, seg=8):
    a = Vector(a); b = Vector(b); d = b - a
    Mx = Matrix.Translation((a + b) / 2) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=d.length, matrix=Mx)

def rail_ring(name, cx, cy, R, n, rz=0.0, H=0.92):
    """turned brass stanchions on a circle with a sagging crimson rope (as the live Koh rail / MCD rails)"""
    bm = bmesh.new(); n0 = len(bm.faces)
    pts = [(cx + R * math.cos(rz + 2 * math.pi * k / n), cy + R * math.sin(rz + 2 * math.pi * k / n)) for k in range(n)]
    for px, py in pts:
        lathe(bm, [(0, 0), (0.12, 0), (0.12, 0.035), (0.06, 0.07), (0.02, 0.12), (0.018, H - 0.07), (0.03, H - 0.05),
                   (0.04, H - 0.02), (0.03, H + 0.01), (0.0, H + 0.015)], 12, Matrix.Translation((px, py, 0)))
    mi(bm, n0, 0); n1 = len(bm.faces)
    for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1]):
        seg = 8; prev = None
        for k in range(seg + 1):
            t = k / seg; z = H - 0.05 - 0.12 * math.sin(math.pi * t)
            p = (ax + (bx - ax) * t, ay + (by - ay) * t, z)
            if prev: rod(bm, prev, p, 0.012, 6)
            prev = p
    mi(bm, n1, 1)
    return put(name, bm, [M["brass"], M["rope"]], "rail")

def append_prop(slug):
    path = os.path.join(A, slug + "_hp1851.blend")
    with bpy.data.libraries.load(path, link=False) as (src, dst): dst.objects = ["SCN_" + slug]
    o = dst.objects[0]; coll.objects.link(o); o["candidate"] = CAND
    return o

def retint(o, mode):
    """marble: lift the grey generated albedo toward warm statuary marble; gold: map albedo luminance onto gold."""
    m = o.data.materials[0].copy(); m.name = o.data.materials[0].name + "_" + mode; o.data.materials[0] = m
    nt = m.node_tree; n = nt.nodes; l = nt.links
    b = [x for x in n if x.type == 'BSDF_PRINCIPLED'][0]
    tex = [x for x in n if x.type == 'TEX_IMAGE' and x.image and x.image.name.startswith("Color")][0]
    # unhook metallic/roughness from ORM so the material reads as intended
    for inp in ("Metallic", "Roughness"):
        for lk in list(b.inputs[inp].links): l.remove(lk)
    bw = n.new("ShaderNodeRGBToBW"); l.new(tex.outputs["Color"], bw.inputs[0])
    ramp = n.new("ShaderNodeValToRGB"); l.new(bw.outputs[0], ramp.inputs[0])
    if mode == "marble":
        mt = n.new("ShaderNodeMath"); mt.operation = 'MULTIPLY'; mt.inputs[1].default_value = MARBLE_GAIN
        l.new(bw.outputs[0], mt.inputs[0]); l.new(mt.outputs[0], ramp.inputs[0])
        ramp.color_ramp.elements[0].color = (0.42, 0.40, 0.37, 1); ramp.color_ramp.elements[1].color = (0.93, 0.90, 0.84, 1)
        b.inputs["Metallic"].default_value = 0.0; b.inputs["Roughness"].default_value = 0.38
        b.inputs["Subsurface Weight"].default_value = 0.08; b.inputs["Subsurface Radius"].default_value = (0.05, 0.03, 0.02)
        b.inputs["Subsurface Scale"].default_value = 0.02
    else:
        mt = n.new("ShaderNodeMath"); mt.operation = 'MULTIPLY'; mt.inputs[1].default_value = GOLD_GAIN
        l.new(bw.outputs[0], mt.inputs[0]); l.new(mt.outputs[0], ramp.inputs[0])
        ramp.color_ramp.elements[0].color = (0.25, 0.14, 0.04, 1); ramp.color_ramp.elements[1].color = (0.95, 0.72, 0.30, 1)
        b.inputs["Metallic"].default_value = 1.0; b.inputs["Roughness"].default_value = 0.28
    for lk in list(b.inputs["Base Color"].links): l.remove(lk)
    l.new(ramp.outputs[0], b.inputs["Base Color"])

# ---------------- Group A: Greek Slave on revolving pedestal under a crimson canopy ----------------
sx, sy, syaw = SLAVE
bm = bmesh.new(); n0 = len(bm.faces)
H = PED_H   # turned drum pedestal; revolving top disc (Powers' pedestal turned by a handle; shape interpretive)
lathe(bm, [(0, 0), (0.50, 0), (0.50, 0.06), (0.46, 0.09), (0.46, 0.13), (0.38, 0.17), (0.36, H - 0.14),
           (0.40, H - 0.10), (0.44, H - 0.06), (0.44, H - 0.035), (0.0, H - 0.035)], 40)
mi(bm, n0, 0); n1 = len(bm.faces)
lathe(bm, [(0, H - 0.035), (0.40, H - 0.035), (0.40, H), (0, H)], 40)   # revolving disc
mi(bm, n1, 1)
put("SCN_slave_pedestal", bm, [M["marble_ped"], M["gilt"]], "pedestal", (sx, sy, 0), syaw)
slave = append_prop("fig-52_greek-slave"); slave.location = (sx, sy, H); slave.rotation_euler = (0, 0, syaw)
retint(slave, "marble")
if CANOPY:
    # four gilt posts, crimson valance and a flat crimson tester (the 1851 'red canopy'; size/shape interpretive)
    W = float(arg("--canopy-w", "2.1")); CH = float(arg("--canopy-h", "3.9")); VAL = 0.42
    bm = bmesh.new(); n0 = len(bm.faces)
    for kx in (-1, 1):
        for ky in (-1, 1):
            lathe(bm, [(0, 0), (0.07, 0), (0.07, 0.10), (0.04, 0.16), (0.03, CH - 0.05), (0.05, CH), (0, CH)], 12,
                  Matrix.Translation((kx * W / 2, ky * W / 2, 0)))
    mi(bm, n0, 0); n1 = len(bm.faces)
    t = 0.03; z0 = CH - VAL
    for side in range(4):
        a = side * math.pi / 2
        c = Matrix.Rotation(a, 4, 'Z') @ Vector((0, -W / 2 - t, z0 + VAL / 2))
        s = (W + 2 * t, t, VAL) if side % 2 == 0 else (t, W + 2 * t, VAL)
        c = Vector((0, 0, z0 + VAL / 2)) + Vector({0: (0, -W / 2 - t, 0), 1: (W / 2 + t, 0, 0), 2: (0, W / 2 + t, 0), 3: (-W / 2 - t, 0, 0)}[side])
        box(bm, c, s)
    box(bm, (0, 0, CH + 0.01), (W + 0.1, W + 0.1, 0.03))
    mi(bm, n1, 1); n2 = len(bm.faces)
    for side in range(4):   # gilt fringe band along the valance foot
        c = Vector((0, 0, z0 - 0.025)) + Vector({0: (0, -W / 2 - 2 * t, 0), 1: (W / 2 + 2 * t, 0, 0), 2: (0, W / 2 + 2 * t, 0), 3: (-W / 2 - 2 * t, 0, 0)}[side])
        s = (W + 4 * t, 0.012, 0.05) if side % 2 == 0 else (0.012, W + 4 * t, 0.05)
        box(bm, c, s)
    mi(bm, n2, 2)
    put("SCN_slave_canopy", bm, [M["gilt"], M["crimson"], M["gilt"]], "canopy", (sx, sy, 0), syaw)
if RAILS: rail_ring("SCN_slave_rail", sx, sy, 1.25, 8, syaw + math.pi / 8)

# ---------------- Group B: jewel cabinet on a crimson-clothed stand; gold vase on a pedestal ----------------
cx, cy, cyaw = CAB
bm = bmesh.new(); n0 = len(bm.faces)
TW, TD = 1.62, 1.12
box(bm, (0, 0, CAB_H / 2 - 0.02), (TW, TD, CAB_H - 0.04))         # cloth-covered body to the floor
mi(bm, n0, 0); n1 = len(bm.faces)
box(bm, (0, 0, CAB_H - 0.02), (TW + 0.06, TD + 0.06, 0.04))       # gilt-edged top
box(bm, (0, 0, 0.03), (TW + 0.04, TD + 0.04, 0.06))               # plinth
mi(bm, n1, 1)
put("SCN_cabinet_stand", bm, [M["crimson"], M["mahog"]], "stand", (cx, cy, 0), cyaw)
cab = append_prop("fig-54_elkington-jewel-cabinet"); cab.location = (cx, cy, CAB_H); cab.rotation_euler = (0, 0, cyaw)
if RAILS:
    bm = bmesh.new(); o = rail_ring("SCN_cabinet_rail", cx, cy, 1.35, 8, cyaw + math.pi / 8)
vx, vy, vyaw = VASE
bm = bmesh.new(); n0 = len(bm.faces)
box(bm, (0, 0, 0.05), (0.56, 0.56, 0.10)); box(bm, (0, 0, VPED_H / 2), (0.42, 0.42, VPED_H - 0.16))
box(bm, (0, 0, VPED_H - 0.06), (0.52, 0.52, 0.06))
mi(bm, n0, 0); n1 = len(bm.faces)
box(bm, (0, 0, VPED_H - 0.015), (0.46, 0.46, 0.03))                # velvet cushion
mi(bm, n1, 1)
put("SCN_vase_pedestal", bm, [M["marble_ped"], M["crimson"]], "pedestal", (vx, vy, 0), vyaw)
vase = append_prop("unnumbered_watherston-brogden-vase"); vase.location = (vx, vy, VPED_H); vase.rotation_euler = (0, 0, vyaw)
retint(vase, "gold")

t = bpy.data.texts.new("CREDIT_SCN_CAND")
t.write("CANDIDATE e02_scanprops (2026-11-09, Grok Bot): CP025 exhibit-court dressing, Hyde Park 1851 only.\n"
        "Props from origin/main e88ee17 scan-models/ (Tripo H3.1 image-to-3D from 1851 prints; Nik Bear Brown),\n"
        "cleaned + decimated copies in assets/scanprops/ (scripts/prep_scanprops.py). Departures EX_SCN_*.\n"
        f"slave {SLAVE} cabinet {CAB} vase {VASE} canopy={CANOPY} rails={RAILS} marble_gain={MARBLE_GAIN}\n")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=False)
print("SCN_SAVED", OUT, [o.name for o in coll.objects], flush=True)
