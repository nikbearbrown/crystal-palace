"""CANDIDATE CP025 sparkle polish: stronger diamond emission + points.
Only keep if clearly better vs live.
  blender -b rounds/e02.blend -P scripts/polish_koh_sparkle.py -- --out rounds/candidates/e02_koh_sparkle.blend
"""
import bpy, os, sys
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FT = 0.3048
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/e02_koh_sparkle.blend"
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "rounds/e02.blend"))

# Stronger diamond emission
for m in bpy.data.materials:
    if "Diamond" not in m.name and "diamond" not in m.name.lower() and "KOH_cand2_Diamond" not in m.name:
        if m.name not in ("KOH_Diamond", "EX_Diamond", "KOH_cand2_Diamond"):
            continue
    if not m.use_nodes:
        continue
    nt = m.node_tree
    for n in nt.nodes:
        if n.type == "EMISSION":
            n.inputs["Strength"].default_value = 4.5
            n.inputs["Color"].default_value = (1.0, 0.98, 0.92, 1)
        if n.type == "MIX_SHADER" or n.type == "ShaderNodeMixShader" or n.bl_idname == "ShaderNodeMixShader":
            if "Fac" in n.inputs:
                n.inputs["Fac"].default_value = 0.42
    print("mat", m.name, flush=True)

# Boost existing sparkle lights; add a tight caustic-cheat spot aimed at diamond
for n in ("KOH_cand2_spark", "KOH_cand2_sky"):
    o = bpy.data.objects.get(n)
    if o and o.type == "LIGHT":
        if "spark" in n:
            o.data.energy = 55.0
            o.data.color = (1.0, 0.95, 0.82)
        else:
            o.data.energy = 22.0

# Tight spot from above-front for caustic-like glint
if "KOH_cand_sparkle_spot" not in bpy.data.objects:
    ld = bpy.data.lights.new("KOH_cand_sparkle_spot_L", type="SPOT")
    ld.energy = 80.0
    ld.color = (1.0, 0.97, 0.9)
    ld.spot_size = 0.35
    ld.spot_blend = 0.35
    ld.shadow_soft_size = 0.02
    lob = bpy.data.objects.new("KOH_cand_sparkle_spot", ld)
    lob.location = Vector((0.15 * FT, -1.2 * FT, 5.8 * FT))
    # aim at diamond ~4.22 ft
    target = Vector((0, 0, 4.22 * FT))
    direction = (target - lob.location).normalized()
    # Blender spot looks down -Z
    from mathutils import Matrix
    world_up = Vector((0, 0, 1))
    right = direction.cross(world_up)
    if right.length < 1e-6:
        right = Vector((1, 0, 0))
    right.normalize()
    up = right.cross(direction).normalized()
    M = Matrix([
        [right.x, up.x, (-direction).x, lob.location.x],
        [right.y, up.y, (-direction).y, lob.location.y],
        [right.z, up.z, (-direction).z, lob.location.z],
        [0, 0, 0, 1],
    ])
    lob.matrix_world = M
    bpy.context.scene.collection.objects.link(lob)
    lob["candidate"] = "CP025_koh_sparkle"
    lob["departure"] = "EX_KOH_SPARKLE_STRONG"

for o in bpy.data.objects:
    if o.name.startswith("KOH_cand") or o.name == "KOH_diamond":
        o["candidate"] = "CP025_koh_sparkle"

txt = bpy.data.texts.get("CREDIT_KOH_SPARKLE") or bpy.data.texts.new("CREDIT_KOH_SPARKLE")
txt.clear()
txt.write("CANDIDATE CP025 sparkle polish — stronger emission Fac 0.42 / str 4.5 + spot caustic cheat.\n")

bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out, flush=True)
