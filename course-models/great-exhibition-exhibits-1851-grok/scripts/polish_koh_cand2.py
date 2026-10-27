"""CANDIDATE CP025v2: rose-cut diamond + sparkle; NO ribbons; reframe july cam
(50 mm, eye 5.25 ft, no roll); whole birdcage in frame; hide grey pole;
open south of July tent (three-wall crimson backdrop). Muse counter skipped.

  blender -b rounds/e02.blend -P scripts/polish_koh_cand2.py -- \
      --out rounds/candidates/e02_koh_v2.blend
"""
import bpy, bmesh, math, os, sys
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
I = 0.0254
FT = 0.3048

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/e02_koh_v2.blend"
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "rounds/e02.blend"))

# Drop prior candidate overlays
for o in list(bpy.data.objects):
    if o.name.startswith("KOH_cand"):
        bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections):
    if c.name.startswith("CP025_KOH_CAND"):
        bpy.data.collections.remove(c)

coll = bpy.data.collections.new("CP025_KOH_CAND2")
bpy.context.scene.collection.children.link(coll)

# Hide occluders: Osler shaft leftover + gas pipe tree that reads as grey pole
for n in ("OSL_shaft_prisms", "OSL_shaft", "OSL_body", "KOH_gas_pipes"):
    o = bpy.data.objects.get(n)
    if o:
        o.hide_render = True
        o.hide_viewport = True
        try:
            o.hide_set(True)
        except Exception:
            pass
        o["hidden_for"] = "CP025_koh_v2_pole_clear"

# Replace closed enclosure with three-wall crimson backdrop (south open for camera)
enc = bpy.data.objects.get("KOH_july_enclosure")
mat = None
if enc:
    if enc.material_slots and enc.material_slots[0].material:
        mat = enc.material_slots[0].material
    enc.hide_render = True
    enc.hide_viewport = True
    try:
        enc.hide_set(True)
    except Exception:
        pass
    enc["hidden_for"] = "CP025_koh_v2_open_south"

if mat is None:
    mat = bpy.data.materials.get("EX_July_crimson") or bpy.data.materials.new("EX_July_crimson")
    mat.use_nodes = True
    b = mat.node_tree.nodes.get("Principled BSDF")
    if b:
        b.inputs["Base Color"].default_value = (0.35, 0.02, 0.05, 1)
        b.inputs["Roughness"].default_value = 0.85

def wall(name, sx, sy, sz, loc):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    me = bpy.data.meshes.new("ME_" + name)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.scale = Vector((sx, sy, sz))
    ob.location = loc
    me.materials.append(mat)
    coll.objects.link(ob)
    ob["candidate"] = "CP025_koh_v2"
    return ob

# Enclosure was ~7 ft; keep similar volume, open on -Y (camera side)
half = 3.5 * FT
h = 7.4 * FT
t = 0.08 * FT
wall("KOH_cand2_wall_N", 2 * half, t, h, Vector((0, +half, h / 2)))
wall("KOH_cand2_wall_E", t, 2 * half, h, Vector((+half, 0, h / 2)))
wall("KOH_cand2_wall_W", t, 2 * half, h, Vector((-half, 0, h / 2)))
# thin roof panel
wall("KOH_cand2_roof", 2 * half, 2 * half, t, Vector((0, 0, h)))

# ---- diamond material with sparkle cheat ----
def ensure_diamond(name="KOH_cand2_Diamond"):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out_n = nt.nodes.new("ShaderNodeOutputMaterial"); out_n.location = (420, 0)
    glass = nt.nodes.new("ShaderNodeBsdfGlass"); glass.location = (0, 100)
    glass.inputs["Color"].default_value = (0.97, 0.98, 1.0, 1)
    glass.inputs["Roughness"].default_value = 0.01
    glass.inputs["IOR"].default_value = 2.417
    emit = nt.nodes.new("ShaderNodeEmission"); emit.location = (0, -100)
    emit.inputs["Color"].default_value = (1.0, 0.97, 0.90, 1)
    emit.inputs["Strength"].default_value = 1.8
    mix = nt.nodes.new("ShaderNodeMixShader"); mix.location = (240, 0)
    mix.inputs["Fac"].default_value = 0.25
    nt.links.new(glass.outputs["BSDF"], mix.inputs[1])
    nt.links.new(emit.outputs["Emission"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out_n.inputs["Surface"])
    return m

DIAMOND = ensure_diamond()

# ---- rebuild rose-cut diamond, screen scale 3.5x ----
old = bpy.data.objects.get("KOH_diamond")
tilt = math.radians(-20)
Lin, Win, Din = 1.55 * I * 3.5, 1.30 * I * 3.5, 0.68 * I * 3.5
bm = bmesh.new()
NRINGS, NSECTORS = 6, 24
peak = Vector((0.10 * Lin / 2, -0.03 * Win / 2, Din))
base_ids = []
for k in range(NSECTORS):
    a = 2 * math.pi * k / NSECTORS
    wobble = 1.0 + 0.06 * math.sin(3 * a) + 0.03 * math.cos(5 * a)
    base_ids.append(bm.verts.new(((Lin / 2) * math.cos(a) * wobble,
                                  (Win / 2) * math.sin(a) * wobble, 0.0)))
bm.verts.ensure_lookup_table()
ring_ids = [base_ids]
for r in range(1, NRINGS + 1):
    t = r / (NRINGS + 1)
    height = Din * (0.55 * t + 0.45 * (t ** 1.6))
    scale = 1.0 - 0.92 * t
    ids = []
    for k in range(NSECTORS):
        a = 2 * math.pi * k / NSECTORS + (math.pi / NSECTORS if r % 2 else 0)
        wobble = 1.0 + 0.05 * math.sin(3 * a + r)
        bx = (Lin / 2) * math.cos(a) * wobble * scale
        by = (Win / 2) * math.sin(a) * wobble * scale
        ids.append(bm.verts.new((bx * (1 - t) + peak.x * t,
                                 by * (1 - t) + peak.y * t, height)))
    ring_ids.append(ids)
    bm.verts.ensure_lookup_table()
peak_v = bm.verts.new((peak.x, peak.y, peak.z))
bm.verts.ensure_lookup_table()

def add_tri(a, b, c):
    try:
        bm.faces.new([a, b, c])
    except ValueError:
        pass

for ri in range(len(ring_ids) - 1):
    A, B = ring_ids[ri], ring_ids[ri + 1]
    for k in range(NSECTORS):
        a0, a1 = A[k], A[(k + 1) % NSECTORS]
        b0, b1 = B[k], B[(k + 1) % NSECTORS]
        if (k + ri) % 2 == 0:
            add_tri(a0, a1, b1); add_tri(a0, b1, b0)
        else:
            add_tri(a0, a1, b0); add_tri(a1, b1, b0)
TOP = ring_ids[-1]
for k in range(NSECTORS):
    add_tri(TOP[k], TOP[(k + 1) % NSECTORS], peak_v)
base_center = bm.verts.new((0.0, 0.0, -0.002 * Din))
bm.verts.ensure_lookup_table()
for k in range(NSECTORS):
    add_tri(base_ids[k], base_ids[(k + 1) % NSECTORS], base_center)
bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0),
                 matrix=Matrix.Rotation(tilt, 3, "X"))
me = bpy.data.meshes.new("ME_KOH_diamond_cand2")
bm.to_mesh(me); bm.free()
for p in me.polygons:
    p.use_smooth = False
me.materials.append(DIAMOND)
if old:
    old_me = old.data
    old.data = me
    if old_me.users == 0:
        bpy.data.meshes.remove(old_me)
    old.location = Vector((0.0, 0.0, 4.22 * FT))
    old["candidate"] = "CP025_koh_v2"
    old["credit"] = "Grok Bot; Mughal/rose cut; 3.5x screen + emission sparkle (EX_KOH_SPARKLE)"
print("diamond", len(me.vertices), "faces", len(me.polygons), flush=True)

# Sparkle lights
for n, energy, color, loc in (
    ("KOH_cand2_spark", 28.0, (1.0, 0.92, 0.75), Vector((0.08 * FT, -0.2 * FT, 4.55 * FT))),
    ("KOH_cand2_sky", 14.0, (0.85, 0.92, 1.0), Vector((0.0, 0.0, 7.0 * FT))),
):
    ld = bpy.data.lights.new(name=n + "_L", type="POINT")
    ld.energy = energy
    ld.color = color
    ld.shadow_soft_size = 0.04
    lob = bpy.data.objects.new(n, ld)
    lob.location = loc
    coll.objects.link(lob)
    lob["departure"] = "EX_KOH_SPARKLE"

# ---- Reframe cam: 50 mm, eye 5.25, no roll; whole cage ----
cam = bpy.data.objects["CP025_july_start"]
target = Vector((0.0, 0.0, 4.1 * FT))
cam.location = Vector((0.0, -10.5 * FT, 5.25 * FT))
look = (target - cam.location).normalized()
world_up = Vector((0, 0, 1))
right = look.cross(world_up).normalized()
up = right.cross(look).normalized()
M = Matrix([
    [right.x, up.x, (-look).x, cam.location.x],
    [right.y, up.y, (-look).y, cam.location.y],
    [right.z, up.z, (-look).z, cam.location.z],
    [0, 0, 0, 1],
])
cam.matrix_world = M
cam.rotation_mode = "XYZ"
cam.data.lens = 50.0
R = cam.matrix_world.to_3x3()
fwd = -(R @ Vector((0, 0, 1)))
xax = R @ Vector((1, 0, 0))
print("CAM", [round(v / FT, 3) for v in cam.location], "lens", cam.data.lens,
      "fwd", [round(x, 4) for x in fwd], "roll", round(xax.z, 6), flush=True)
cam["candidate"] = "CP025_koh_v2_reframe"

txt = bpy.data.texts.get("CREDIT_KOH_CAND2") or bpy.data.texts.new("CREDIT_KOH_CAND2")
txt.clear()
txt.write(
    "CANDIDATE CP025 v2 — Koh-i-Noor\n"
    "NO gilt ribbons. OSL_shaft_prisms + KOH_gas_pipes hidden (grey pole clear).\n"
    "July enclosure south opened via three-wall crimson backdrop (N/E/W + roof).\n"
    "Cam CP025_july_start: 50 mm, eye 5.25 ft, no roll; whole cage in frame.\n"
    "Diamond: Mughal/rose cut, 3.5x screen scale, emission+point sparkle (EX_KOH_SPARKLE).\n"
    "Muse glass-topped-display-counter SKIPPED (12 ft unit vs ~7 ft tent — EX_KOH_COUNTER).\n"
    "Live e02 untouched.\n"
)

bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out, flush=True)
