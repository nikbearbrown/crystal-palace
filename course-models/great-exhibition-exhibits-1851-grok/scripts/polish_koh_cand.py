"""CANDIDATE: rebuild Koh-i-Noor diamond (pre-1852 Mughal/rose cut) + enrich
birdcage case detail. Sibling only — live e02 untouched.

  blender -b rounds/e02.blend -P scripts/polish_koh_cand.py -- \
      --out rounds/candidates/e02_koh.blend
"""
import bpy, bmesh, math, os, sys
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
I = 0.0254  # inch → metre

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/e02_koh.blend"
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)

if not bpy.data.filepath:
    bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "rounds/e02.blend"))

# ---- materials ----
def ensure_diamond(name="KOH_cand_Diamond"):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out_n = nt.nodes.new("ShaderNodeOutputMaterial"); out_n.location = (400, 0)
    glass = nt.nodes.new("ShaderNodeBsdfGlass"); glass.location = (0, 80)
    glass.inputs["Color"].default_value = (0.96, 0.97, 1.0, 1)
    glass.inputs["Roughness"].default_value = 0.02
    glass.inputs["IOR"].default_value = 2.417  # diamond
    emit = nt.nodes.new("ShaderNodeEmission"); emit.location = (0, -120)
    emit.inputs["Color"].default_value = (1.0, 0.96, 0.88, 1)
    emit.inputs["Strength"].default_value = 0.35  # gas-jet warm (July enclosure)
    mix = nt.nodes.new("ShaderNodeMixShader"); mix.location = (220, 0)
    mix.inputs["Fac"].default_value = 0.12
    nt.links.new(glass.outputs["BSDF"], mix.inputs[1])
    nt.links.new(emit.outputs["Emission"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out_n.inputs["Surface"])
    return m

def ensure_gilt(name="KOH_cand_Gilt"):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (0.85, 0.68, 0.22, 1)
    b.inputs["Metallic"].default_value = 1.0
    b.inputs["Roughness"].default_value = 0.22
    if "Specular IOR Level" in b.inputs:
        b.inputs["Specular IOR Level"].default_value = 1.0
    if "Coat Weight" in b.inputs:
        b.inputs["Coat Weight"].default_value = 0.35
        b.inputs["Coat Roughness"].default_value = 0.08
    return m

DIAMOND = ensure_diamond()
GILT = ensure_gilt()

# ---- rebuild diamond: pre-1852 Mughal / rose cut ----
# Flat irregular oval base, off-centre peak, concentric rings of triangular
# facets. Dimensions from exhibits NOTES: ~1.55 x 1.3 x 0.68 inches (pre-re-cut).
# Source accounts: ILN 17 May 1851; Illustrated Exhibitor Jun/Jul 1851.
old = bpy.data.objects.get("KOH_diamond")
loc = old.location.copy() if old else Vector((0, 0, 4.22))
# live gem was tilted -65° on X; keep that presentation
tilt = math.radians(-65)

Lin, Win, Din = 1.55 * I, 1.30 * I, 0.68 * I  # metres half? No — full L,W,D inches→m
# We'll build in local space with half-extents Lin/2 etc.

bm = bmesh.new()
# Rose-cut: N rings of facets, M sectors. Flat base at z=0, peak at z=Din.
NRINGS = 6
NSECTORS = 24
# Off-centre peak (Mughal irregularity) — shift +12% along +X
peak = Vector((0.12 * Lin / 2, -0.04 * Win / 2, Din))

# Base rim vertices (irregular oval)
base_ids = []
for k in range(NSECTORS):
    a = 2 * math.pi * k / NSECTORS
    # mild radial wobble for irregular outline
    wobble = 1.0 + 0.06 * math.sin(3 * a) + 0.03 * math.cos(5 * a)
    x = (Lin / 2) * math.cos(a) * wobble
    y = (Win / 2) * math.sin(a) * wobble
    base_ids.append(bm.verts.new((x, y, 0.0)))
bm.verts.ensure_lookup_table()

# Concentric rings rising toward peak
ring_ids = [base_ids]
for r in range(1, NRINGS + 1):
    t = r / (NRINGS + 1)  # 0..1 toward peak
    # interpolate oval → peak; flatten mid rings slightly (rose cut)
    height = Din * (0.55 * t + 0.45 * (t ** 1.6))
    ids = []
    scale = 1.0 - 0.92 * t  # shrink toward peak
    for k in range(NSECTORS):
        a = 2 * math.pi * k / NSECTORS + (math.pi / NSECTORS if r % 2 else 0)
        wobble = 1.0 + 0.05 * math.sin(3 * a + r)
        bx = (Lin / 2) * math.cos(a) * wobble * scale
        by = (Win / 2) * math.sin(a) * wobble * scale
        # drift toward peak
        x = bx * (1 - t) + peak.x * t
        y = by * (1 - t) + peak.y * t
        z = height
        ids.append(bm.verts.new((x, y, z)))
    ring_ids.append(ids)
    bm.verts.ensure_lookup_table()

peak_v = bm.verts.new((peak.x, peak.y, peak.z))
bm.verts.ensure_lookup_table()

# Facet faces: quads split to tris between rings (flat shading = cut crystal)
def add_tri(a, b, c):
    try:
        bm.faces.new([a, b, c])
    except ValueError:
        pass

for ri in range(len(ring_ids) - 1):
    A = ring_ids[ri]
    B = ring_ids[ri + 1]
    n = NSECTORS
    for k in range(n):
        a0, a1 = A[k], A[(k + 1) % n]
        b0, b1 = B[k], B[(k + 1) % n]
        # two tris per sector — alternate diagonal for sparkle
        if (k + ri) % 2 == 0:
            add_tri(a0, a1, b1)
            add_tri(a0, b1, b0)
        else:
            add_tri(a0, a1, b0)
            add_tri(a1, b1, b0)

# Cap to peak
TOP = ring_ids[-1]
for k in range(NSECTORS):
    add_tri(TOP[k], TOP[(k + 1) % NSECTORS], peak_v)

# Flat pavilion underside (Mughal rose: large flat base) — fan tris
base_center = bm.verts.new((0.0, 0.0, -0.002 * Din))
bm.verts.ensure_lookup_table()
for k in range(NSECTORS):
    add_tri(base_ids[k], base_ids[(k + 1) % NSECTORS], base_center)

# Apply tilt
bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0),
                 matrix=Matrix.Rotation(tilt, 3, "X"))

me = bpy.data.meshes.new("ME_KOH_diamond_cand")
bm.to_mesh(me)
bm.free()
for p in me.polygons:
    p.use_smooth = False  # hard facet edges — cut crystal
me.materials.append(DIAMOND)

# Replace live diamond mesh in place (keep object name for shot hooks)
if old:
    old_me = old.data
    old.data = me
    # orphan old mesh if unused
    if old_me.users == 0:
        bpy.data.meshes.remove(old_me)
    old["candidate"] = "CP025_koh"
    old["credit"] = "Grok Bot; pre-1852 Mughal/rose cut rebuilt from ILN/Illustrated Exhibitor accounts"
    diamond_obj = old
else:
    diamond_obj = bpy.data.objects.new("KOH_diamond", me)
    bpy.context.scene.collection.objects.link(diamond_obj)
    diamond_obj.location = loc

print("KOH_diamond verts", len(me.vertices), "faces", len(me.polygons), flush=True)

# ---- also rebuild the two armlet stones with same cut, smaller ----
for name, Lin2, Win2, Din2, loc2 in (
    ("KOH_armlet_L", 0.75, 0.60, 0.35, None),
    ("KOH_armlet_R", 0.75, 0.60, 0.35, None),
):
    o = bpy.data.objects.get(name)
    if not o:
        continue
    bm = bmesh.new()
    NR, NS = 4, 12
    L, W, D = Lin2 * I, Win2 * I, Din2 * I
    peak = Vector((0.08 * L / 2, 0, D))
    base = [bm.verts.new(((L / 2) * math.cos(2 * math.pi * k / NS),
                          (W / 2) * math.sin(2 * math.pi * k / NS), 0)) for k in range(NS)]
    rings = [base]
    for r in range(1, NR + 1):
        t = r / (NR + 1)
        sc = 1.0 - 0.9 * t
        ids = []
        for k in range(NS):
            a = 2 * math.pi * k / NS
            x = (L / 2) * math.cos(a) * sc * (1 - t) + peak.x * t
            y = (W / 2) * math.sin(a) * sc * (1 - t) + peak.y * t
            z = D * (0.5 * t + 0.5 * t * t)
            ids.append(bm.verts.new((x, y, z)))
        rings.append(ids)
    pk = bm.verts.new(tuple(peak))
    bm.verts.ensure_lookup_table()
    for ri in range(len(rings) - 1):
        A, B = rings[ri], rings[ri + 1]
        for k in range(NS):
            try:
                bm.faces.new([A[k], A[(k + 1) % NS], B[(k + 1) % NS]])
                bm.faces.new([A[k], B[(k + 1) % NS], B[k]])
            except ValueError:
                pass
    for k in range(NS):
        try:
            bm.faces.new([rings[-1][k], rings[-1][(k + 1) % NS], pk])
        except ValueError:
            pass
    bc = bm.verts.new((0, 0, -0.001 * D))
    for k in range(NS):
        try:
            bm.faces.new([base[k], base[(k + 1) % NS], bc])
        except ValueError:
            pass
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0),
                     matrix=Matrix.Rotation(tilt, 3, "X"))
    me2 = bpy.data.meshes.new("ME_" + name + "_cand")
    bm.to_mesh(me2); bm.free()
    for p in me2.polygons:
        p.use_smooth = False
    me2.materials.append(DIAMOND)
    old_me = o.data
    o.data = me2
    if old_me.users == 0:
        bpy.data.meshes.remove(old_me)

# ---- enrich cage: add mid-rings, twisted ribbon accents, finer crown fleurons ----
# Keep live KOH_cage; overlay candidate detail objects so revert is easy.
coll = bpy.data.collections.get("CP025_KOH_CAND") or bpy.data.collections.new("CP025_KOH_CAND")
if coll.name not in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.link(coll)

CAGE_R = 1.45 * 0.3048  # metres (build_exhibits used feet; scene is metric)
# Live cage is in feet via ft() at build — check actual KOH_cage bounds
cage = bpy.data.objects.get("KOH_cage")
if cage:
    bb = [cage.matrix_world @ Vector(c) for c in cage.bound_box]
    xs = [v.x for v in bb]; ys = [v.y for v in bb]; zs = [v.z for v in bb]
    r_est = max(max(abs(x) for x in xs), max(abs(y) for y in ys))
    z0, z1 = min(zs), max(zs)
    print("live cage r", round(r_est, 3), "z", round(z0, 3), round(z1, 3), flush=True)
else:
    r_est = 1.45 * 0.3048
    z0, z1 = 3.1 * 0.3048, 7.35 * 0.3048

# Decorative twisted ribbons winding up alternate bars (gilt)
bm = bmesh.new()
NB = 8
for k in range(NB):
    a0 = 2 * math.pi * k / NB + math.pi / (2 * NB)
    pts = []
    nseg = 24
    for j in range(nseg + 1):
        t = j / nseg
        z = z0 + 0.05 + t * (z1 - z0 - 0.55)
        # gentle helix
        a = a0 + 0.35 * math.sin(t * math.pi)
        r = r_est * (0.98 + 0.02 * math.sin(3 * t * math.pi))
        # taper near dome
        if t > 0.75:
            r *= math.cos((t - 0.75) / 0.25 * math.pi / 2) * 0.85 + 0.15
            # follow dome
        pts.append(Vector((r * math.cos(a), r * math.sin(a), z)))
    # tube along polyline
    for i in range(len(pts) - 1):
        p0, p1 = pts[i], pts[i + 1]
        d = (p1 - p0).normalized()
        # local frame
        up = Vector((0, 0, 1))
        if abs(d.dot(up)) > 0.9:
            up = Vector((1, 0, 0))
        x = d.cross(up).normalized()
        y = d.cross(x).normalized()
        rad = 0.012
        ring0, ring1 = [], []
        for s in range(6):
            ang = 2 * math.pi * s / 6
            off = x * (rad * math.cos(ang)) + y * (rad * math.sin(ang))
            ring0.append(bm.verts.new(p0 + off))
            ring1.append(bm.verts.new(p1 + off))
        for s in range(6):
            try:
                bm.faces.new([ring0[s], ring0[(s + 1) % 6], ring1[(s + 1) % 6], ring1[s]])
            except ValueError:
                pass
me = bpy.data.meshes.new("ME_KOH_cand_ribbons")
bm.to_mesh(me); bm.free()
me.materials.append(GILT)
ob = bpy.data.objects.new("KOH_cand_ribbons", me)
coll.objects.link(ob)

# Extra horizontal rings with bead detail
bm = bmesh.new()
for zf, rr in ((0.22, 1.0), (0.48, 1.0), (0.72, 0.92)):
    z = z0 + (z1 - z0) * zf
    r = r_est * rr
    n = 48
    prev = None
    first = None
    for k in range(n):
        a = 2 * math.pi * k / n
        # bead every 4th
        rad = 0.018 if k % 4 == 0 else 0.010
        v = bm.verts.new((r * math.cos(a), r * math.sin(a), z))
        # small sphere-ish bead as short tube segment — just mark verts then connect
        if prev is not None:
            # will build ring after
            pass
        prev = v
        if first is None:
            first = v
    # actual ring tube
    for k in range(n):
        a0 = 2 * math.pi * k / n
        a1 = 2 * math.pi * ((k + 1) % n) / n
        rad = 0.016 if k % 4 == 0 else 0.009
        # 4-gon cross section
        for (za, zb) in ((-rad, -rad), (-rad, rad), (rad, rad), (rad, -rad)):
            pass
        cs = []
        for s in range(5):
            ang = 2 * math.pi * s / 5
            cs.append((rad * math.cos(ang), rad * math.sin(ang)))
        r0 = [bm.verts.new((r * math.cos(a0) + cs[s][0] * math.cos(a0),
                            r * math.sin(a0) + cs[s][0] * math.sin(a0),
                            z + cs[s][1])) for s in range(5)]
        r1 = [bm.verts.new((r * math.cos(a1) + cs[s][0] * math.cos(a1),
                            r * math.sin(a1) + cs[s][0] * math.sin(a1),
                            z + cs[s][1])) for s in range(5)]
        for s in range(5):
            try:
                bm.faces.new([r0[s], r0[(s + 1) % 5], r1[(s + 1) % 5], r1[s]])
            except ValueError:
                pass
me = bpy.data.meshes.new("ME_KOH_cand_rings")
bm.to_mesh(me); bm.free()
me.materials.append(GILT)
ob = bpy.data.objects.new("KOH_cand_bead_rings", me)
coll.objects.link(ob)

# Upgrade live KOH_cage material toward richer gilt if present
for mat_name in ("EX_Gilt", "GILT", "EX_Gold"):
    m = bpy.data.materials.get(mat_name)
    if not m or not m.use_nodes:
        continue
    b = m.node_tree.nodes.get("Principled BSDF")
    if not b:
        continue
    b.inputs["Base Color"].default_value = (0.82, 0.65, 0.20, 1)
    b.inputs["Metallic"].default_value = 1.0
    b.inputs["Roughness"].default_value = min(b.inputs["Roughness"].default_value, 0.28)
    if "Coat Weight" in b.inputs:
        b.inputs["Coat Weight"].default_value = 0.4

# Credit text
txt = bpy.data.texts.get("CREDIT_KOH_CAND") or bpy.data.texts.new("CREDIT_KOH_CAND")
txt.clear()
txt.write(
    "CANDIDATE CP025 — Koh-i-Noor diamond + cage enrich\n"
    "Diamond: pre-1852 Mughal/rose cut (flat base, off-centre peak,\n"
    "concentric triangular facets). Dims from exhibits NOTES (~1.55x1.3x0.68 in).\n"
    "Sources: ILN 17 May 1851; Illustrated Exhibitor Jun/Jul 1851.\n"
    "Cage: overlay gilt ribbons + beaded rings; live KOH_cage kept.\n"
    "Live e02 untouched.\n"
)

bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out, flush=True)
