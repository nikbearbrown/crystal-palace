"""CANDIDATE polish CP028 on h03 → rounds/candidates/h03_cp028.blend. Does not touch live h03."""
import bpy, bmesh, math, sys, os
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath(__file__))
FT = 0.3048
def ft(v): return v * FT

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
SRC = argv[argv.index("--src") + 1] if "--src" in argv else "rounds/h03.blend"
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/h03_cp028.blend"
root = os.path.dirname(HERE)
src = SRC if os.path.isabs(SRC) else os.path.join(root, SRC)
out = OUT if os.path.isabs(OUT) else os.path.join(root, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=src)

def mat(name, col, rough=0.85, metal=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*col, 1)
    b.inputs["Roughness"].default_value = rough
    if "Metallic" in b.inputs: b.inputs["Metallic"].default_value = metal
    return m

IRON = mat("CP028_LouvreIron", (0.14, 0.13, 0.12), 0.5, 0.4)
WOOD = mat("CP028_Batten", (0.38, 0.28, 0.18), 0.88)
GLASS_D = mat("CP028_GlassDark", (0.04, 0.06, 0.09), 0.25, 0.05)

coll = bpy.data.collections.get("CP028_CAND") or bpy.data.collections.new("CP028_CAND")
if coll.name not in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.link(coll)

# Find CP028 camera to place louvres in view
cam = bpy.data.objects.get("CP028_louvre_start")
# North end wall around y=+204 ft from earlier Muse louvre notes; but CP028 cam may look at N wall
# From image: arched wall with louvre band — place thick blades on WLOUV locations visible

# Hide thin existing WLOUV near camera-facing wall by scaling to zero if name matches north
for o in list(bpy.data.objects):
    if not o.name.startswith("WLOUV_"): continue
    # keep but we'll add proud thicker blades in front

bm = bmesh.new()
# Sample WLOUV locations and add thicker tilted blades
added = 0
for o in bpy.data.objects:
    if not o.name.startswith("WLOUV_"): continue
    # only those whose world Y is near the CP028 subject (north wall ~ +62m = 204ft)
    t = o.matrix_world.translation
    if abs(t.y - 62.18) > 3.0 and abs(t.y + 62.18) > 3.0:
        continue
    # 4 thick blades spanning the louvre bay
    for k in range(4):
        z = t.z + ft(0.4 + k * 0.55)
        # parallelogram blade tilted ~30 deg
        dx, dy = ft(3.2), ft(0.08)
        tip = ft(0.22)
        # face camera: offset slightly inward (toward |y| smaller)
        yoff = -ft(0.12) if t.y > 0 else ft(0.12)
        x0, x1 = t.x - dx, t.x + dx
        y0 = t.y + yoff
        verts = [
            bm.verts.new((x0, y0, z - tip)),
            bm.verts.new((x1, y0, z - tip)),
            bm.verts.new((x1, y0 - tip*0.3, z + tip)),
            bm.verts.new((x0, y0 - tip*0.3, z + tip)),
        ]
        try: bm.faces.new(verts); added += 1
        except: pass
me = bpy.data.meshes.new("CP028_cand_louvres"); bm.to_mesh(me); bm.free()
me.materials.append(IRON)
ob = bpy.data.objects.new("CP028_cand_louvres", me); coll.objects.link(ob)
print("louvre blades", added)

# vertical battens on arched WALLF near same wall
bm = bmesh.new()
nbat = 0
for o in bpy.data.objects:
    if not o.name.startswith("WALLF_"): continue
    t = o.matrix_world.translation
    if abs(t.y - 62.18) > 3.0 and abs(t.y + 62.18) > 3.0: continue
    if t.z > ft(14): continue  # lower arches
    yoff = -ft(0.05) if t.y > 0 else ft(0.05)
    for s in (-1, 0, 1):
        x = t.x + s * ft(2.2)
        bm.faces.new([
            bm.verts.new((x - ft(0.06), t.y + yoff, t.z)),
            bm.verts.new((x + ft(0.06), t.y + yoff, t.z)),
            bm.verts.new((x + ft(0.06), t.y + yoff, t.z + ft(4.5))),
            bm.verts.new((x - ft(0.06), t.y + yoff, t.z + ft(4.5))),
        ])
        nbat += 1
me = bpy.data.meshes.new("CP028_cand_battens"); bm.to_mesh(me); bm.free()
me.materials.append(WOOD)
ob = bpy.data.objects.new("CP028_cand_battens", me); coll.objects.link(ob)
print("battens", nbat)

# darken glass-like materials that look flat grey on clerestory (name heuristics)
for m in bpy.data.materials:
    n = m.name.lower()
    if any(k in n for k in ("glass", "glaze", "pane", "sash")):
        if not m.use_nodes: continue
        b = m.node_tree.nodes.get("Principled BSDF")
        if not b: continue
        c = list(b.inputs["Base Color"].default_value)
        # only nudge mid-grey glass darker
        if 0.3 < (c[0]+c[1]+c[2])/3 < 0.85:
            b.inputs["Base Color"].default_value = (0.05, 0.07, 0.1, 1)
            b.inputs["Roughness"].default_value = 0.3

bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out)
